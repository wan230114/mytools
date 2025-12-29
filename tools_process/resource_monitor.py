#!/usr/bin/env python3
"""
Resource Monitor (Real-time Snapshots & Status Indication)
Requires: pip install docker
"""
import subprocess
import psutil
import time
import sys
import threading
import warnings
import textwrap
import json
from datetime import datetime
from collections import deque
import numpy as np
import os
import uuid
import tempfile
from pathlib import Path

# --- 屏蔽 Matplotlib 的配置警告 ---
warnings.filterwarnings("ignore")
try:
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    import matplotlib.gridspec as gridspec
except ImportError:
    pass

# 检查 Docker SDK
try:
    import docker
    DOCKER_AVAILABLE = True
except ImportError:
    DOCKER_AVAILABLE = False

if 'matplotlib.pyplot' in sys.modules:
    plt.style.use('seaborn-v0_8-white')

class ResourceMonitor:
    def __init__(self, command=None, sampling_interval=0.5, snapshot_interval=60, output_file=None):
        self.original_command = command if command else []
        self.sampling_interval = sampling_interval
        self.snapshot_interval = snapshot_interval # 快照间隔
        self.output_file = output_file             # 用于实时更新的目标文件
        
        # 自动推导 json 文件名
        self.json_file = None
        if self.output_file:
            base = os.path.splitext(self.output_file)[0]
            self.json_file = f"{base}.json"

        # 基础状态
        self.is_docker = False
        self.command_to_run = list(self.original_command)
        self.cid_file = None
        self.monitor_uuid = str(uuid.uuid4())[:8]
        self.docker_client = None
        
        if self.original_command and len(self.original_command) > 0 and self.original_command[0] == 'docker':
            self._init_docker()

        # 数据存储 (增加容量以支持长时间运行，或者改为动态列表)
        # deque maxlen=None 表示无限长，注意内存，但一般监控数据量不大
        self.timestamps = deque() 
        self.cpu_percentages = deque()
        self.memory_usages = deque()
        
        self.process = None
        self.running = False
        self.monitor_thread = None
        self.snapshot_thread = None  # 新增快照线程
        self.container_obj = None
        self.cpu_count = psutil.cpu_count(logical=True)
        self.start_time = None
        self.end_time = None

    def _init_docker(self):
        if not DOCKER_AVAILABLE:
            self._log("Error: pip install docker required.")
            sys.exit(1)
        
        self.is_docker = True
        try:
            self.docker_client = docker.from_env()
            self.docker_client.ping()
        except Exception as e:
            self._log(f"Docker Connection Error: {e}")
            sys.exit(1)

        if 'run' in self.original_command:
            try:
                tmp_dir = tempfile.gettempdir()
                self.cid_file = os.path.join(tmp_dir, f"monitor_{self.monitor_uuid}.cid")
                try:
                    run_idx = self.original_command.index('run')
                    self.command_to_run = self.original_command[:run_idx+1] + \
                                          ['--cidfile', self.cid_file] + \
                                          self.original_command[run_idx+1:]
                    self._log(f"⚓ Strategy: CIDFile Injection -> {self.cid_file}")
                except ValueError: pass
            except Exception: pass

    def _log(self, msg):
        sys.stderr.write(f"{msg}\r\n")
        sys.stderr.flush()

    def _wait_for_cid(self, timeout=5.0):
        start = time.time()
        while time.time() - start < timeout:
            if os.path.exists(self.cid_file):
                try:
                    with open(self.cid_file, 'r') as f:
                        cid = f.read().strip()
                        if cid: return cid
                except: pass
            time.sleep(0.1)
        return None

    def _get_target_container(self):
        if self.container_obj: return self.container_obj
        cid = None
        if self.cid_file: cid = self._wait_for_cid()
        if cid:
            try:
                container = self.docker_client.containers.get(cid)
                self._log(f"✅ Locked Container ID: {cid[:12]}")
                self.container_obj = container
                return container
            except Exception as e:
                self._log(f"Error getting container {cid}: {e}")
        return None

    def _calculate_stats(self, stats):
        cpu_pct, mem_mb = 0.0, 0.0
        try:
            cpu_stats = stats['cpu_stats']
            precpu_stats = stats['precpu_stats']
            cpu_delta = cpu_stats['cpu_usage']['total_usage'] - precpu_stats['cpu_usage']['total_usage']
            system_delta = cpu_stats.get('system_cpu_usage', 0) - precpu_stats.get('system_cpu_usage', 0)
            if system_delta > 0.0 and cpu_delta > 0.0:
                online_cpus = cpu_stats.get('online_cpus', self.cpu_count)
                cpu_pct = (cpu_delta / system_delta) * online_cpus * 100.0

            mem_stats = stats['memory_stats']
            usage = mem_stats.get('usage', 0)
            stats_v1 = mem_stats.get('stats', {})
            if 'total_inactive_file' in stats_v1: cache = stats_v1.get('total_inactive_file', 0)
            elif 'inactive_file' in stats_v1: cache = stats_v1.get('inactive_file', 0)
            else: cache = 0
            
            used_mem = usage - cache
            if used_mem < 0: used_mem = usage
            mem_mb = used_mem / (1024 * 1024)
        except KeyError: pass
        return cpu_pct, mem_mb

    def _monitor_loop(self, pid):
        if not self.is_docker:
            psutil.cpu_percent()
            proc = psutil.Process(pid)

        while self.running:
            try:
                cpu_val, mem_val = 0.0, 0.0
                if self.is_docker:
                    container = self._get_target_container()
                    if container:
                        try:
                            stats = container.stats(stream=False)
                            cpu_val, mem_val = self._calculate_stats(stats)
                        except: pass
                else:
                    try:
                        procs = [proc] + proc.children(recursive=True)
                        for p in procs:
                            cpu_val += p.cpu_percent(interval=None)
                            mem_val += p.memory_info().rss / (1024 * 1024)
                    except: pass

                self.timestamps.append(datetime.now())
                self.cpu_percentages.append(cpu_val)
                self.memory_usages.append(mem_val)
            except: pass
            time.sleep(self.sampling_interval)

    # --- 新增: 定期快照线程 ---
    def _snapshot_loop(self):
        last_snapshot = time.time()
        while self.running:
            time.sleep(1) # 1秒检查一次，避免 sleep 太久无法及时退出
            if time.time() - last_snapshot > self.snapshot_interval:
                if len(self.timestamps) > 2 and self.output_file:
                    try:
                        # 临时保存，不打印 log 避免刷屏
                        self.save_to_json(self.json_file, silent=True)
                        self.plot(self.output_file, silent=True)
                        # 可选：在 stderr 打印一个小点表示 update
                        # sys.stderr.write(".")
                        # sys.stderr.flush()
                    except Exception:
                        pass
                last_snapshot = time.time()

    def execute(self):
        if not self.command_to_run:
            self._log("No command to execute.")
            return 1

        self.start_time = time.perf_counter()
        try:
            env = os.environ.copy()
            env['PYTHONUNBUFFERED'] = '1'
            
            self.process = subprocess.Popen(
                self.command_to_run,
                stdout=sys.stdout,
                stderr=sys.stderr,
                universal_newlines=True,
                env=env
            )
            
            self.running = True
            
            # 1. 启动监控线程
            self.monitor_thread = threading.Thread(
                target=self._monitor_loop,
                args=(self.process.pid,)
            )
            self.monitor_thread.daemon = True
            self.monitor_thread.start()

            # 2. 启动快照线程 (如果指定了输出文件)
            if self.output_file:
                self.snapshot_thread = threading.Thread(
                    target=self._snapshot_loop
                )
                self.snapshot_thread.daemon = True
                self.snapshot_thread.start()
            
            return_code = self.process.wait()
            
        except Exception as e:
            self._log(f"Execution Error: {e}")
            return_code = 1
        finally:
            self.running = False # 这会让两个线程退出
            
            if self.monitor_thread:
                self.monitor_thread.join(timeout=2.0)
            if self.snapshot_thread:
                self.snapshot_thread.join(timeout=2.0)
                
            self.end_time = time.perf_counter()
            
            if self.cid_file and os.path.exists(self.cid_file):
                try: os.remove(self.cid_file)
                except: pass
        
        return return_code

    def get_stats(self):
        if not self.timestamps: return {}
        cpu_l = list(self.cpu_percentages)
        mem_l = list(self.memory_usages)
        
        # 动态计算 duration
        if self.end_time: # 已结束
            duration = self.end_time - self.start_time
        elif self.start_time: # 正在运行
            duration = time.perf_counter() - self.start_time
        elif len(self.timestamps) > 1: # 导入模式
            duration = (self.timestamps[-1] - self.timestamps[0]).total_seconds()
        else:
            duration = 0

        return {
            'duration': duration,
            'samples': len(self.timestamps),
            'max_cpu': max(cpu_l) if cpu_l else 0,
            'avg_cpu': np.mean(cpu_l) if cpu_l else 0,
            'max_mem': max(mem_l) if mem_l else 0,
            'avg_mem': np.mean(mem_l) if mem_l else 0,
            'status': 'Running' if self.running else 'Finished' # 添加状态
        }

    def save_to_json(self, filename, silent=False):
        data = {
            'command': self.original_command,
            'is_docker': self.is_docker,
            'timestamps': [ts.isoformat() for ts in self.timestamps],
            'cpu_percentages': list(self.cpu_percentages),
            'memory_usages': list(self.memory_usages),
            'metadata': {
                'cpu_count': self.cpu_count,
                'start_time': self.start_time,
                'end_time': self.end_time,
                'status': 'Running' if self.running else 'Finished' # 标记状态
            }
        }
        try:
            # 写入临时文件再重命名，原子操作防止读到一半的文件
            tmp_name = filename + ".tmp"
            with open(tmp_name, 'w') as f:
                json.dump(data, f, indent=2)
            os.replace(tmp_name, filename)
            
            if not silent: self._log(f"Data saved to: {filename}")
        except Exception as e:
            if not silent: self._log(f"Error saving data: {e}")

    def load_from_json(self, filename):
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
            
            self.original_command = data.get('command', [])
            self.is_docker = data.get('is_docker', False)
            self.timestamps = deque([datetime.fromisoformat(ts) for ts in data.get('timestamps', [])])
            self.cpu_percentages = deque(data.get('cpu_percentages', []))
            self.memory_usages = deque(data.get('memory_usages', []))
            
            meta = data.get('metadata', {})
            self.cpu_count = meta.get('cpu_count', psutil.cpu_count(logical=True))
            self.start_time = meta.get('start_time')
            self.end_time = meta.get('end_time')
            
            # 如果加载的是一个之前未完成的文件，我们可以手动标记状态
            self.running = (meta.get('status') == 'Running')
            
            self._log(f"Loaded {len(self.timestamps)} samples from {filename}")
            return True
        except Exception as e:
            self._log(f"Error loading data: {e}")
            return False

    def plot(self, output_file, silent=False):
        if len(self.timestamps) < 2:
            if not silent: self._log("Not enough data to plot.")
            return

        # 确保线程安全地复制数据进行绘图
        ts = list(self.timestamps)
        cpu = list(self.cpu_percentages)
        mem = list(self.memory_usages)
        stats = self.get_stats()
        
        max_mem = stats['max_mem']
        if max_mem >= 1024: unit, scale = 'GB', 1024.0
        elif max_mem < 1.0 and max_mem > 0: unit, scale = 'KB', 1.0/1024.0
        else: unit, scale = 'MB', 1.0
        mem_scaled = [x/scale for x in mem]
        
        fig = plt.figure(figsize=(16, 8))
        gs = gridspec.GridSpec(1, 2, width_ratios=[6, 1], wspace=0.02)
        
        ax = fig.add_subplot(gs[0])
        ax_stat = fig.add_subplot(gs[1])
        c_cpu, c_mem = '#1f77b4', '#d62728'
        
        ax.plot(ts, cpu, color=c_cpu, lw=2, label='CPU', alpha=0.9)
        ax.fill_between(ts, 0, cpu, color=c_cpu, alpha=0.1)
        ax.set_ylabel('CPU (%)', color=c_cpu, fontweight='bold')
        ax.tick_params(axis='y', labelcolor=c_cpu)
        ax.set_ylim(0, max(100, max(cpu)*1.1))
        ax.grid(True, ls='--', alpha=0.3, zorder=0)
        
        ax2 = ax.twinx()
        ax2.plot(ts, mem_scaled, color=c_mem, lw=2, label='Memory', alpha=0.9)
        ax2.fill_between(ts, 0, mem_scaled, color=c_mem, alpha=0.1)
        ax2.set_ylabel(f'Memory ({unit})', color=c_mem, fontweight='bold')
        ax2.tick_params(axis='y', labelcolor=c_mem)
        ax2.set_ylim(bottom=0)
        
        for s in ['top']: ax.spines[s].set_visible(False); ax2.spines[s].set_visible(False)
        ax.spines['left'].set_color(c_cpu); ax.spines['left'].set_lw(2)
        ax2.spines['right'].set_color(c_mem); ax2.spines['right'].set_lw(2)
        
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
        ax.set_xlim(ts[0], ts[-1])
        
        # --- 标题显示状态 ---
        base_title = "Resource Usage Monitor" + (" (Docker)" if self.is_docker else "")
        if self.running:
            title = f"{base_title} - [RUNNING...]"
            title_color = '#d62728' # 红色提示正在运行
        else:
            title = f"{base_title} - [FINISHED]"
            title_color = '#333333'
            
        ax.set_title(title, fontsize=16, fontweight='bold', pad=15, color=title_color)
        
        ax_stat.axis('off')
        h, r = divmod(stats['duration'], 3600)
        m, s = divmod(r, 60)
        
        # 状态颜色
        status_color = 'green' if not self.running else 'orange'
        
        lines = [
            ("STATISTICS", 1.5, '#333', True),
            (f"Status:   {stats['status']}", 1.0, status_color, True), # 状态行
            (f"Duration: {int(h):02d}:{int(m):02d}:{int(s):02d}", 1.0, 'black', False),
            (f"Samples:  {stats['samples']}", 2.0, 'black', False),
            ("CPU Usage", 1.5, c_cpu, True),
            (f"Max: {stats['max_cpu']:.1f}%", 1.0, 'black', False),
            (f"Avg: {stats['avg_cpu']:.1f}%", 2.0, 'black', False),
            (f"Memory ({unit})", 1.5, c_mem, True),
            (f"Max: {stats['max_mem']/scale:.2f}", 1.0, 'black', False),
            (f"Avg: {stats['avg_mem']/scale:.2f}", 1.0, 'black', False),
        ]
        
        cur_y = 0.90
        for txt, gap, col, bold in lines:
            fw = 'bold' if bold else 'normal'
            fs = 12 if bold else 10
            ax_stat.text(0.15, cur_y, txt, color=col, fontweight=fw, fontsize=fs, fontfamily='monospace')
            if bold: ax_stat.axhline(y=cur_y-0.015, xmin=0.15, xmax=0.85, color=col, lw=1, alpha=0.5)
            cur_y -= 0.05 * gap

        cmd_str = ' '.join(self.original_command)
        if not cmd_str: cmd_str = "Imported Data"
        wrapped = "\n".join(textwrap.wrap(cmd_str, width=150))
        fig.text(0.5, 0.1, f"Command:\n{wrapped}", ha='center', va='top', 
                 fontsize=9, fontfamily='monospace', color='#555',
                 bbox=dict(boxstyle='round', facecolor='#f8f9fa', ec='#ddd'))

        plt.subplots_adjust(top=0.92, bottom=0.15, left=0.08, right=0.95)
        
        try:
            if output_file:
                Path(output_file).parent.mkdir(parents=True, exist_ok=True)
                plt.savefig(output_file, dpi=300, facecolor='white', bbox_inches='tight')
                if not silent: self._log(f"Chart saved to: {output_file}")
            else:
                plt.tight_layout()
                plt.show()
        except Exception:
            pass # 忽略绘图错误，避免打断主线程
        finally:
            plt.close()

def main():
    if len(sys.argv) < 2:
        sys.stderr.write("Usage:\n")
        sys.stderr.write("  Monitor: python monitor.py [--output plot.png] [--snapshot-interval 60] <command>\n")
        sys.stderr.write("  Replay:  python monitor.py --plot-data data.json [--output plot.png]\n")
        sys.exit(1)
    
    command = []
    interval = 0.5
    snapshot_interval = 60 # 默认 60秒更新一次图表
    output_file = None
    import_file = None
    
    i = 1
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg == '--interval':
            interval = float(sys.argv[i+1]); i += 2
        elif arg == '--snapshot-interval':
            snapshot_interval = float(sys.argv[i+1]); i += 2
        elif arg == '--output':
            output_file = sys.argv[i+1]; i += 2
        elif arg == '--plot-data':
            import_file = sys.argv[i+1]; i += 2
        else:
            command.append(arg); i += 1
            
    # --- 模式 1: 仅绘图模式 ---
    if import_file:
        mon = ResourceMonitor()
        if mon.load_from_json(import_file):
            if not output_file: 
                base_name = os.path.splitext(import_file)[0]
                output_file = f"{base_name}.png"
            mon.plot(output_file)
        else:
            sys.exit(1)
        sys.exit(0)

    # --- 模式 2: 监控模式 ---
    if not command:
        sys.stderr.write("Error: No command specified for monitoring.\n")
        sys.exit(1)

    if command[0] in ['python', 'python3'] and '-u' not in command:
        command.insert(1, '-u')
    
    # 自动生成文件名 (如果用户未指定)
    if not output_file:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        cmd_slug = Path(command[0]).stem
        output_file = f"monitor_{cmd_slug}_{timestamp}.png"
        
    mon = ResourceMonitor(
        command, 
        sampling_interval=interval, 
        snapshot_interval=snapshot_interval,
        output_file=output_file # 传入 output_file 以开启快照功能
    )
    
    ret = mon.execute()
    
    # 结束后的最终保存
    # 重新推导 json 名
    base_name = os.path.splitext(output_file)[0]
    json_file = f"{base_name}.json"

    if len(mon.timestamps) > 0:
        mon.save_to_json(json_file)

    if len(mon.timestamps) > 2:
        mon.plot(output_file)
        
    sys.exit(ret)

if __name__ == "__main__":
    main()
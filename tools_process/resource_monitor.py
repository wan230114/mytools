#!/usr/bin/env python3
"""
Resource Monitor (Clean Output & Raw Mode Fix)
Requires: pip install docker
"""
import subprocess
import psutil
import time
import sys
import threading
import warnings
import textwrap
from datetime import datetime
from collections import deque
import numpy as np
import os
import uuid
import tempfile
from pathlib import Path

# --- 优化1: 屏蔽 Matplotlib 的配置警告 ---
warnings.filterwarnings("ignore")
try:
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    import matplotlib.gridspec as gridspec
except ImportError:
    pass # 延迟报错，或者在下面处理

# 检查 Docker SDK
try:
    import docker
    DOCKER_AVAILABLE = True
except ImportError:
    DOCKER_AVAILABLE = False

# 确保有 plt
if 'matplotlib.pyplot' in sys.modules:
    plt.style.use('seaborn-v0_8-white')

class ResourceMonitor:
    def __init__(self, command, sampling_interval=0.5, max_samples=10000):
        self.original_command = command.copy()
        self.sampling_interval = sampling_interval
        self.max_samples = max_samples
        
        self.is_docker = False
        self.command_to_run = command
        self.cid_file = None
        self.monitor_uuid = str(uuid.uuid4())[:8]
        
        # Docker 识别与参数注入
        if len(command) > 0 and command[0] == 'docker':
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

            # 策略 A: CIDFile (针对 docker run)
            if 'run' in command:
                try:
                    tmp_dir = tempfile.gettempdir()
                    self.cid_file = os.path.join(tmp_dir, f"monitor_{self.monitor_uuid}.cid")
                    
                    run_idx = command.index('run')
                    self.command_to_run = command[:run_idx+1] + \
                                          ['--cidfile', self.cid_file] + \
                                          command[run_idx+1:]
                    self._log(f"⚓ Strategy: CIDFile Injection -> {self.cid_file}")
                except ValueError:
                    pass
            
            # 策略 B: Label 注入 (备用)
            if not self.cid_file and any(x in command for x in ['run', 'exec', 'create']):
                pass # 简化逻辑，保持专注

        # 数据存储
        self.timestamps = deque(maxlen=max_samples)
        self.cpu_percentages = deque(maxlen=max_samples)
        self.memory_usages = deque(maxlen=max_samples)
        
        self.process = None
        self.running = False
        self.monitor_thread = None
        self.container_obj = None
        self.cpu_count = psutil.cpu_count(logical=True)

    def _log(self, msg):
        """
        --- 优化2: 日志输出到 stderr 并修复 Raw Mode 换行问题 ---
        使用 \r\n 确保在 docker -it 模式下光标能正确回退到行首
        """
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
                except:
                    pass
            time.sleep(0.1)
        return None

    def _get_target_container(self):
        if self.container_obj: return self.container_obj

        cid = None
        if self.cid_file: cid = self._wait_for_cid()
        
        if cid:
            try:
                container = self.docker_client.containers.get(cid)
                # 使用优化后的日志输出
                self._log(f"✅ Locked Container ID: {cid[:12]}")
                self.container_obj = container
                return container
            except Exception as e:
                self._log(f"Error getting container {cid}: {e}")
        
        return None

    def _calculate_stats(self, stats):
        # ... (保持原有的计算逻辑不变) ...
        cpu_pct = 0.0
        mem_mb = 0.0
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
        except KeyError:
            pass
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

    def execute(self):
        self.start_time = time.perf_counter()
        try:
            env = os.environ.copy()
            env['PYTHONUNBUFFERED'] = '1'
            
            # 使用 sys.stderr 打印启动信息
            # self._log(f"Running: {' '.join(self.command_to_run)}")
            
            self.process = subprocess.Popen(
                self.command_to_run,
                stdout=sys.stdout,
                stderr=sys.stderr,
                universal_newlines=True,
                env=env
            )
            
            self.running = True
            self.monitor_thread = threading.Thread(
                target=self._monitor_loop,
                args=(self.process.pid,)
            )
            self.monitor_thread.daemon = True
            self.monitor_thread.start()
            
            return_code = self.process.wait()
            
        except Exception as e:
            self._log(f"Execution Error: {e}")
            return_code = 1
        finally:
            self.running = False
            if self.monitor_thread:
                self.monitor_thread.join(timeout=2.0)
            self.end_time = time.perf_counter()
            
            if self.cid_file and os.path.exists(self.cid_file):
                try: os.remove(self.cid_file)
                except: pass
        
        return return_code

    def get_stats(self):
        if not self.timestamps: return {}
        cpu_l = list(self.cpu_percentages)
        mem_l = list(self.memory_usages)
        return {
            'duration': self.end_time - self.start_time,
            'samples': len(self.timestamps),
            'max_cpu': max(cpu_l) if cpu_l else 0,
            'avg_cpu': np.mean(cpu_l) if cpu_l else 0,
            'max_mem': max(mem_l) if mem_l else 0,
            'avg_mem': np.mean(mem_l) if mem_l else 0
        }

    def plot(self, output_file):
        if len(self.timestamps) < 2:
            self._log("Not enough data to plot.")
            return

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
        title = "Resource Usage Monitor" + (" (Docker)" if self.is_docker else "")
        ax.set_title(title, fontsize=16, fontweight='bold', pad=15)
        
        ax_stat.axis('off')
        h, r = divmod(stats['duration'], 3600)
        m, s = divmod(r, 60)
        lines = [
            ("STATISTICS", 1.5, '#333', True),
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
        wrapped = "\n".join(textwrap.wrap(cmd_str, width=150))
        fig.text(0.5, 0.1, f"Command:\n{wrapped}", ha='center', va='top', 
                 fontsize=9, fontfamily='monospace', color='#555',
                 bbox=dict(boxstyle='round', facecolor='#f8f9fa', ec='#ddd'))

        plt.subplots_adjust(top=0.92, bottom=0.15, left=0.08, right=0.95)
        
        if output_file:
            Path(output_file).parent.mkdir(parents=True, exist_ok=True)
            plt.savefig(output_file, dpi=300, facecolor='white', bbox_inches='tight')
            # 同样使用 _log 输出保存信息
            self._log(f"Chart saved to: {output_file}")
        else:
            plt.tight_layout()
            plt.show()
        plt.close()

def main():
    if len(sys.argv) < 2:
        sys.stderr.write("Usage: python resource_monitor.py <command> [args...]\n")
        sys.exit(1)
    
    command = []
    interval = 0.5
    output = None
    
    i = 1
    while i < len(sys.argv):
        if sys.argv[i] == '--interval':
            interval = float(sys.argv[i+1]); i += 2
        elif sys.argv[i] == '--output':
            output = sys.argv[i+1]; i += 2
        else:
            command.append(sys.argv[i]); i += 1
            
    if command[0] in ['python', 'python3'] and '-u' not in command:
        command.insert(1, '-u')
        
    mon = ResourceMonitor(command, interval)
    ret = mon.execute()
    
    if output or len(mon.timestamps) > 2:
        if not output: output = f"monitor_{int(time.time())}.png"
        mon.plot(output)
    sys.exit(ret)

if __name__ == "__main__":
    main()
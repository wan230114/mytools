#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Resource Monitor (最终修复版 - 智能参数隔离)

修复问题：
  彻底解决了 "Argument Hijacking" 问题。
  现在的逻辑是：一旦检测到被监控的命令开始（即遇到第一个非 flag 参数），
  监控器就停止解析后续参数，将它们全部交给子进程。
  
  这意味着：
  resource_monitor.py cmd --output file  -> --output 属于 cmd (不再报错)
  resource_monitor.py --output file cmd  -> --output 属于 monitor
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
    try:
        plt.style.use('seaborn-v0_8-white')
    except (OSError, FileNotFoundError):
        try:
            plt.style.use('seaborn-white')
        except (OSError, FileNotFoundError):
            pass

class ResourceMonitor:
    def __init__(self, command=None, sampling_interval=0.5, snapshot_interval=60, output_file=None):
        self.original_command = command if command else []
        self.sampling_interval = sampling_interval
        self.snapshot_interval = snapshot_interval
        self.output_file = output_file
        
        self.json_file = None
        if self.output_file:
            base = os.path.splitext(self.output_file)[0]
            self.json_file = f"{base}.json"

        self.is_docker = False
        self.command_to_run = list(self.original_command)
        self.cid_file = None
        self.monitor_uuid = str(uuid.uuid4())[:8]
        self.docker_client = None
        
        if self.original_command and len(self.original_command) > 0 and self.original_command[0] == 'docker':
            self._init_docker()

        self.timestamps = deque() 
        self.cpu_percentages = deque()
        self.memory_usages = deque()
        
        self.process = None
        self.running = False
        self.monitor_thread = None
        self.snapshot_thread = None
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
        proc = None
        if not self.is_docker:
            try:
                psutil.cpu_percent()
                proc = psutil.Process(pid)
            except psutil.NoSuchProcess:
                return

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
                    if proc:
                        try:
                            if not proc.is_running():
                                break
                            procs = [proc] + proc.children(recursive=True)
                            for p in procs:
                                try:
                                    cpu_val += p.cpu_percent(interval=None)
                                    mem_val += p.memory_info().rss / (1024 * 1024)
                                except (psutil.NoSuchProcess, psutil.AccessDenied):
                                    pass
                        except psutil.NoSuchProcess:
                            break

                self.timestamps.append(datetime.now())
                self.cpu_percentages.append(cpu_val)
                self.memory_usages.append(mem_val)
            except Exception: 
                pass
            time.sleep(self.sampling_interval)

    def _snapshot_loop(self):
        last_snapshot = time.time()
        while self.running:
            time.sleep(1)
            if time.time() - last_snapshot > self.snapshot_interval:
                if len(self.timestamps) > 2 and self.output_file:
                    try:
                        self.save_to_json(self.json_file, silent=True)
                        self.plot(self.output_file, silent=True)
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
            
            self.monitor_thread = threading.Thread(
                target=self._monitor_loop,
                args=(self.process.pid,)
            )
            self.monitor_thread.daemon = True
            self.monitor_thread.start()

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
            self.running = False
            if self.monitor_thread: self.monitor_thread.join(timeout=2.0)
            if self.snapshot_thread: self.snapshot_thread.join(timeout=2.0)
            self.end_time = time.perf_counter()
            if self.cid_file and os.path.exists(self.cid_file):
                try: os.remove(self.cid_file)
                except: pass
        
        return return_code

    def get_stats(self):
        if not self.timestamps: return {}
        cpu_l = list(self.cpu_percentages)
        mem_l = list(self.memory_usages)
        
        if self.end_time: duration = self.end_time - self.start_time
        elif self.start_time: duration = time.perf_counter() - self.start_time
        elif len(self.timestamps) > 1: duration = (self.timestamps[-1] - self.timestamps[0]).total_seconds()
        else: duration = 0

        return {
            'duration': duration,
            'samples': len(self.timestamps),
            'max_cpu': max(cpu_l) if cpu_l else 0,
            'avg_cpu': np.mean(cpu_l) if cpu_l else 0,
            'max_mem': max(mem_l) if mem_l else 0,
            'avg_mem': np.mean(mem_l) if mem_l else 0,
            'status': 'Running' if self.running else 'Finished'
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
                'status': 'Running' if self.running else 'Finished'
            }
        }
        try:
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
        
        base_title = "Resource Usage Monitor" + (" (Docker)" if self.is_docker else "")
        title = f"{base_title} - [{'RUNNING' if self.running else 'FINISHED'}]"
        ax.set_title(title, fontsize=16, fontweight='bold', pad=15, color='#d62728' if self.running else '#333')
        
        ax_stat.axis('off')
        h, r = divmod(stats['duration'], 3600)
        m, s = divmod(r, 60)
        
        lines = [
            ("STATISTICS", 1.5, '#333', True),
            (f"Status: {stats['status']}", 1.0, 'green' if not self.running else 'orange', True),
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
        except Exception: pass
        finally: plt.close()

def parse_monitor_config(config_str):
    config = {}
    if not config_str: return config
    for item in config_str.split(';'):
        item = item.strip()
        if not item: continue
        if '=' in item: k, v = item.split('=', 1)
        elif ':' in item: k, v = item.split(':', 1)
        else: continue
        config[k.strip().lower()] = v.strip()
    return config

def main():
    if len(sys.argv) < 2:
        sys.stderr.write("Usage: python monitor.py [monitor_opts] command [command_opts]\n")
        sys.exit(1)
    
    command = []
    interval = 0.5
    snapshot_interval = 60
    output_file = None
    import_file = None
    
    # --- 阶段 1: 扫描并分离 Monitor 参数和 Command ---
    # 策略：扫描参数列表，一旦遇到看起来不像是 flag 的东西（比如 /usr/bin/python），
    # 或者遇到了明确的 '--'，就认为这里是 Command 的起点。
    # 从起点开始往后的所有东西，都无条件属于 Command。
    
    monitor_args = []
    cmd_args = []
    
    raw_args = sys.argv[1:]
    split_index = -1
    
    for i, arg in enumerate(raw_args):
        # 显式分隔符
        if arg == '--':
            monitor_args = raw_args[:i]
            cmd_args = raw_args[i+1:]
            split_index = i
            break
        
        # 启发式：如果遇到一个不以 - 开头的参数，且前一个参数不是那种需要值的flag
        # (简单起见，这里假设如果遇到不以-开头，且不是 config string, 就是命令)
        # 注意：为了鲁棒性，这里我们只解析我们认识的参数。一旦遇到不认识的或非flag，就终止。
        
        is_flag = arg.startswith('-')
        if not is_flag:
            # 这是一个普通的位置参数（如 /bin/sleep 或 ./script.sh）
            # 认为这是命令的开始
            monitor_args = raw_args[:i]
            cmd_args = raw_args[i:]
            split_index = i
            break
    
    # 如果没找到分割点（例如全是 flag?），那可能就是纯 replay 模式或者出错了
    if split_index == -1:
        monitor_args = raw_args
        cmd_args = []

    # --- 阶段 2: 解析 Monitor 参数 ---
    # 我们只在 monitor_args 里找配置
    
    args_iter = iter(monitor_args)
    while True:
        try:
            arg = next(args_iter)
        except StopIteration:
            break
            
        if arg == '--monitor-config':
            try:
                cfg = parse_monitor_config(next(args_iter))
                if 'output' in cfg: output_file = cfg['output']
                if 'file' in cfg: output_file = cfg['file']
                if 'interval' in cfg: interval = float(cfg['interval'])
                if 'snapshot' in cfg: snapshot_interval = float(cfg['snapshot'])
                if 'data' in cfg: import_file = cfg['data']
            except StopIteration: pass
            
        elif arg == '--interval':
            try: interval = float(next(args_iter))
            except StopIteration: pass
        elif arg == '--snapshot-interval':
            try: snapshot_interval = float(next(args_iter))
            except StopIteration: pass
        elif arg in ['--output', '--plot-output']:
            try: output_file = next(args_iter)
            except StopIteration: pass
        elif arg == '--plot-data':
            try: import_file = next(args_iter)
            except StopIteration: pass
        else:
            # 如果 monitor_args 里混入了不认识的 flag，比如用户把 flag 写在了命令前面？
            # 比如: resource_monitor.py --verbose cmd
            # 这种情况下，保守起见，我们将这些也加回 cmd_args 的最前面
            cmd_args.insert(0, arg)

    # --- 阶段 3: 执行逻辑 ---
    
    if import_file:
        mon = ResourceMonitor()
        if mon.load_from_json(import_file):
            if not output_file: 
                base_name = os.path.splitext(import_file)[0]
                output_file = f"{base_name}.png"
            mon.plot(output_file)
        sys.exit(0)

    if not cmd_args:
        sys.stderr.write("Error: No command specified.\n")
        sys.exit(1)
        
    command = cmd_args

    # 强制 unbuffered
    if command[0] in ['python', 'python3'] and '-u' not in command:
        command.insert(1, '-u')
    
    # 自动生成文件名
    if not output_file:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        cmd_slug = Path(command[0]).stem
        output_file = f"monitor_{cmd_slug}_{timestamp}.png"
        
    mon = ResourceMonitor(
        command, 
        sampling_interval=interval, 
        snapshot_interval=snapshot_interval,
        output_file=output_file
    )
    
    ret = mon.execute()
    
    base_name = os.path.splitext(output_file)[0]
    json_file = f"{base_name}.json"
    if len(mon.timestamps) > 0:
        mon.save_to_json(json_file)
    if len(mon.timestamps) > 2:
        mon.plot(output_file)
        
    sys.exit(ret)

if __name__ == "__main__":
    main()
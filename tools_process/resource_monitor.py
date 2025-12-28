#!/usr/bin/env python3
"""
Advanced Resource Monitor
"""
import subprocess
import psutil
import time
import sys
import threading
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
from collections import deque
import numpy as np
import os
from pathlib import Path

# 导入配置
try:
    import docker
    DOCKER_AVAILABLE = True
    docker_client = docker.from_env()
except ImportError:
    DOCKER_AVAILABLE = False
    docker_client = None

# 图表样式配置
plt.style.use('seaborn-v0_8-darkgrid')
plt.rcParams['font.size'] = 10
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['axes.labelsize'] = 10
plt.rcParams['legend.fontsize'] = 9
plt.rcParams['figure.titlesize'] = 14

class ResourceMonitor:
    def __init__(self, command, sampling_interval=0.5, max_samples=10000):
        self.command = command
        self.sampling_interval = sampling_interval
        self.max_samples = max_samples
        
        # 数据存储
        self.timestamps = deque(maxlen=max_samples)
        self.cpu_percentages = deque(maxlen=max_samples)
        self.memory_usages = deque(maxlen=max_samples)
        
        # 进程跟踪
        self.process = None
        self.process_stats = {}
        self.cpu_count = psutil.cpu_count(logical=True)
        
        # 控制标志
        self.running = False
        self.start_time = None
        self.end_time = None
        self.monitor_thread = None
        
        # Docker相关
        self.docker_container = None
    
    def _get_process_tree(self, pid):
        """获取进程树"""
        try:
            process = psutil.Process(pid)
            processes = [process]
            try:
                processes.extend(process.children(recursive=True))
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
            return processes
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return []
    
    def _monitor_resources(self, pid):
        """监控资源使用的线程函数"""
        while self.running:
            try:
                # 获取当前进程树
                processes = self._get_process_tree(pid)
                
                # 计算CPU和内存使用
                total_cpu = 0.0
                total_memory = 0.0
                current_time = time.time()
                
                for proc in processes:
                    try:
                        # CPU计算
                        cpu_times = proc.cpu_times()
                        current_cpu = cpu_times.user + cpu_times.system
                        
                        if proc.pid in self.process_stats:
                            time_diff = current_time - self.process_stats[proc.pid]['last_check']
                            cpu_diff = current_cpu - self.process_stats[proc.pid]['cpu_time']
                            
                            if time_diff > 0:
                                cpu_percent = (cpu_diff / time_diff) * 100.0
                                cpu_percent = min(cpu_percent, 100.0 * self.cpu_count)
                                total_cpu += cpu_percent
                        
                        # 更新CPU统计
                        self.process_stats[proc.pid] = {
                            'cpu_time': current_cpu,
                            'last_check': current_time
                        }
                        
                        # 内存计算
                        mem_info = proc.memory_info()
                        total_memory += mem_info.rss / (1024 * 1024)  # 转换为MB
                        
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        if proc.pid in self.process_stats:
                            del self.process_stats[proc.pid]
                
                # 记录数据
                self.timestamps.append(datetime.now())
                self.cpu_percentages.append(total_cpu)
                self.memory_usages.append(total_memory)
                
            except Exception as e:
                print(f"Monitoring error: {e}", file=sys.stderr)
            
            time.sleep(self.sampling_interval)
    
    def execute_with_monitoring(self):
        """执行命令并监控资源使用"""
        self.start_time = time.perf_counter()
        
        try:
            # 启动子进程
            env = os.environ.copy()
            env['PYTHONUNBUFFERED'] = '1'
            
            self.process = subprocess.Popen(
                self.command,
                stdout=sys.stdout,
                stderr=sys.stderr,
                universal_newlines=True,
                env=env
            )
            
            # 启动监控线程
            self.running = True
            self.monitor_thread = threading.Thread(
                target=self._monitor_resources,
                args=(self.process.pid,)
            )
            self.monitor_thread.daemon = True
            self.monitor_thread.start()
            
            # 等待进程完成
            return_code = self.process.wait()
            
        except Exception as e:
            print(f"Execution error: {e}", file=sys.stderr)
            return_code = 1
        finally:
            self.running = False
            if self.monitor_thread:
                self.monitor_thread.join(timeout=2.0)
            self.end_time = time.perf_counter()
        
        return return_code
    
    def get_statistics(self):
        """获取统计信息"""
        if not self.timestamps:
            return {}
        
        stats = {
            'total_time': self.end_time - self.start_time,
            'cpu_cores': self.cpu_count,
            'sample_count': len(self.timestamps)
        }
        
        if self.cpu_percentages:
            cpu_list = list(self.cpu_percentages)
            stats.update({
                'max_cpu': max(cpu_list),
                'avg_cpu': np.mean(cpu_list)
            })
        
        if self.memory_usages:
            memory_list = list(self.memory_usages)
            stats.update({
                'max_memory': max(memory_list),
                'avg_memory': np.mean(memory_list)
            })
        
        return stats
    
    def plot_resource_usage(self, output_file=None):
        """绘制资源使用图表（优化版本）"""
        if len(self.timestamps) < 2:
            print("Warning: Insufficient data points to generate chart")
            return
        
        # 准备数据
        timestamps = list(self.timestamps)
        cpu_data = list(self.cpu_percentages)
        memory_data = list(self.memory_usages)
        stats = self.get_statistics()
        
        # 创建图表
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # 设置标题
        duration = (timestamps[-1] - timestamps[0]).total_seconds()
        if duration <= 60:
            duration_str = f"{duration:.0f}s"
        else:
            duration_str = f"{duration/60:.1f}m"
        
        # 创建图表标题
        title_text = f"Resource Usage Monitor"
        ax.set_title(title_text, fontsize=16, fontweight='bold', pad=20)
        
        # 绘制CPU使用率
        color_cpu = '#1f77b4'
        line_cpu, = ax.plot(timestamps, cpu_data, 
                          color=color_cpu, 
                          linewidth=2.5,
                          alpha=0.8,
                          label='CPU Usage (%)',
                          marker='o',
                          markersize=3)
        ax.set_xlabel('Time', fontsize=12, fontweight='bold')
        ax.set_ylabel('CPU Usage (%)', color=color_cpu, fontsize=12, fontweight='bold')
        ax.tick_params(axis='y', labelcolor=color_cpu)
        ax.grid(True, alpha=0.3, linestyle='--')
        ax.set_ylim(bottom=0)
        
        # 在CPU线下方添加填充
        ax.fill_between(timestamps, 0, cpu_data, color=color_cpu, alpha=0.2)
        
        # 设置x轴时间格式
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
        
        # 创建第二个y轴用于内存
        ax2 = ax.twinx()
        color_memory = '#d62728'
        line_memory, = ax2.plot(timestamps, memory_data, 
                               color=color_memory, 
                               linewidth=2.5,
                               alpha=0.8,
                               label='Memory Usage (MB)',
                               marker='s',
                               markersize=3)
        ax2.set_ylabel('Memory Usage (MB)', color=color_memory, fontsize=12, fontweight='bold')
        ax2.tick_params(axis='y', labelcolor=color_memory)
        ax2.set_ylim(bottom=0)
        
        # 在内存线下方添加填充
        ax2.fill_between(timestamps, 0, memory_data, color=color_memory, alpha=0.1)
        
        # 合并图例
        lines = [line_cpu, line_memory]
        labels = [l.get_label() for l in lines]
        ax.legend(lines, labels, loc='upper left', fontsize=10, framealpha=0.9, ncol=2)
        
        # 添加统计信息到图表内部
        if stats:
            # 格式化运行时间
            elapsed = stats['total_time']
            hours = int(elapsed // 3600)
            minutes = int((elapsed % 3600) // 60)
            seconds = elapsed % 60
            
            if hours > 0:
                time_str = f"{hours:02d}:{minutes:02d}:{seconds:05.2f}"
            elif minutes > 0:
                time_str = f"{minutes:02d}:{seconds:05.2f}"
            else:
                time_str = f"{seconds:05.2f}s"
            
            # 创建统计信息文本
            stats_text = (
                f"Duration: {time_str}\n"
                f"CPU Cores: {stats['cpu_cores']}\n"
                f"Max CPU: {stats.get('max_cpu', 0):.1f}%\n"
                f"Avg CPU: {stats.get('avg_cpu', 0):.1f}%\n"
                f"Max Mem: {stats.get('max_memory', 0):.1f} MB\n"
                f"Avg Mem: {stats.get('avg_memory', 0):.1f} MB\n"
                f"Samples: {stats['sample_count']}"
            )
            
            # 在图表右上角添加统计信息框
            props = dict(boxstyle='round', facecolor='white', alpha=0.9, edgecolor='gray')
            ax.text(0.98, 0.98, stats_text,
                   transform=ax.transAxes,
                   fontsize=9,
                   fontfamily='monospace',
                   verticalalignment='top',
                   horizontalalignment='right',
                   bbox=props)
        
        # 在图表下方添加命令信息
        cmd_text = f"Command: {' '.join(self.command)}"
        plt.figtext(0.5, 0.01, cmd_text,
                   fontsize=9,
                   fontfamily='monospace',
                   ha='center',
                   va='bottom',
                   bbox=dict(boxstyle="round,pad=0.5", facecolor="whitesmoke", alpha=0.8))
        
        plt.tight_layout(rect=[0, 0.05, 1, 0.95])  # 为底部命令留出空间
        
        # 保存或显示图表
        if output_file:
            # 确保目录存在
            output_path = Path(output_file)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
            print(f"Chart saved to: {output_file}")
        else:
            plt.show()
        
        plt.close()


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("""
        Resource Usage Monitor
        ======================
        
        Usage: python resource_monitor.py <command> [args...]
        
        Examples:
          python resource_monitor.py python3 -u script.py
          python resource_monitor.py ./program arg1 arg2
          python resource_monitor.py sleep 5
        
        Options:
          --output FILE     Output chart filename
          --interval SEC    Sampling interval (default: 0.5)
        """)
        sys.exit(1)
    
    # 解析命令行参数
    command = []
    sampling_interval = 0.5
    output_file = None
    
    i = 1
    while i < len(sys.argv):
        if sys.argv[i] == '--interval' and i + 1 < len(sys.argv):
            sampling_interval = float(sys.argv[i + 1])
            i += 2
        elif sys.argv[i] == '--output' and i + 1 < len(sys.argv):
            output_file = sys.argv[i + 1]
            i += 2
        else:
            command.append(sys.argv[i])
            i += 1
    
    if not command:
        print("Error: No command specified")
        sys.exit(1)
    
    # 自动为Python命令添加无缓冲参数
    if command[0] in ['python', 'python3', 'py'] and '-u' not in command:
        command.insert(1, '-u')
        print("Note: Added -u flag for unbuffered output")
    
    # 创建监控器
    monitor = ResourceMonitor(command, sampling_interval)
    
    # 执行命令
    return_code = monitor.execute_with_monitoring()
    
    # 打印简要统计
    stats = monitor.get_statistics()
    if stats:
        print("\n" + "="*60)
        print("RESOURCE USAGE SUMMARY")
        print("="*60)
        print(f"Command: {' '.join(command)}")
        print(f"Duration: {stats['total_time']:.2f}s")
        print(f"CPU: {stats.get('avg_cpu', 0):.1f}% avg, {stats.get('max_cpu', 0):.1f}% max")
        print(f"Memory: {stats.get('avg_memory', 0):.1f} MB avg, {stats.get('max_memory', 0):.1f} MB max")
        print(f"Samples: {stats['sample_count']}")
        print("="*60)
    
    # 生成图表
    if len(monitor.timestamps) >= 2:
        if not output_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            cmd_name = Path(command[0]).stem
            output_file = f"resource_monitor_{cmd_name}_{timestamp}.png"
        
        monitor.plot_resource_usage(output_file)
    
    sys.exit(return_code)


if __name__ == "__main__":
    main()
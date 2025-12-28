#!/usr/bin/env python3
import subprocess
import psutil
import time
import sys
import threading
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
from collections import deque
import numpy as np
import os
import signal

class ResourceMonitor:
    def __init__(self, command, sampling_interval=0.5, max_samples=10000):
        """
        初始化资源监控器
        :param command: 要执行的命令（列表形式）
        :param sampling_interval: 采样间隔（秒）
        :param max_samples: 最大采样点数
        """
        self.command = command
        self.sampling_interval = sampling_interval
        self.max_samples = max_samples
        
        # 资源数据存储
        self.timestamps = deque(maxlen=max_samples)
        self.cpu_percentages = deque(maxlen=max_samples)
        self.memory_usages = deque(maxlen=max_samples)  # 单位：MB
        
        # 进程跟踪
        self.process_tree = set()
        self.process_cpu_times = {}  # 记录每个进程的上次CPU时间
        self.cpu_count = psutil.cpu_count(logical=True)
        
        # 统计信息
        self.start_time = None
        self.end_time = None
        self.process = None
        self.monitor_thread = None
        self.running = False
        self.last_calc_time = None
        
    def _get_process_tree(self, pid):
        """获取进程及其所有子进程的PID列表"""
        try:
            main_process = psutil.Process(pid)
            processes = []
            
            # 添加主进程
            processes.append(main_process)
            
            # 添加所有子进程
            try:
                for child in main_process.children(recursive=True):
                    processes.append(child)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
                
            return processes
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return []
    
    def _calculate_cpu_usage(self, processes):
        """计算进程树的CPU使用率"""
        total_cpu_percent = 0.0
        
        for proc in processes:
            try:
                # 获取进程的CPU时间
                cpu_times = proc.cpu_times()
                current_cpu_time = cpu_times.user + cpu_times.system
                
                # 获取进程的创建时间，用于计算进程生命周期
                create_time = proc.create_time()
                current_time = time.time()
                process_lifetime = current_time - create_time
                
                # 如果是第一次记录这个进程，初始化CPU时间
                if proc.pid not in self.process_cpu_times:
                    self.process_cpu_times[proc.pid] = {
                        'last_cpu_time': current_cpu_time,
                        'last_check_time': current_time
                    }
                    continue
                
                # 计算时间差
                time_diff = current_time - self.process_cpu_times[proc.pid]['last_check_time']
                
                if time_diff > 0:
                    # 计算CPU时间差
                    cpu_time_diff = current_cpu_time - self.process_cpu_times[proc.pid]['last_cpu_time']
                    
                    # 计算CPU使用率百分比
                    # cpu_time_diff是进程在时间间隔内使用的CPU时间（秒）
                    # 对于多核系统，CPU使用率可以超过100%
                    cpu_percent = (cpu_time_diff / time_diff) * 100.0
                    
                    # 限制合理的范围
                    cpu_percent = max(0.0, min(cpu_percent, 100.0 * self.cpu_count))
                    
                    total_cpu_percent += cpu_percent
                
                # 更新记录
                self.process_cpu_times[proc.pid] = {
                    'last_cpu_time': current_cpu_time,
                    'last_check_time': current_time
                }
                
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                # 如果进程已结束，从记录中移除
                if proc.pid in self.process_cpu_times:
                    del self.process_cpu_times[proc.pid]
                continue
        
        return total_cpu_percent
    
    def _calculate_memory_usage(self, processes):
        """计算进程树的内存使用量（MB）"""
        total_memory_mb = 0.0
        
        for proc in processes:
            try:
                mem_info = proc.memory_info()
                total_memory_mb += mem_info.rss / (1024 * 1024)  # 转换为MB
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        
        return total_memory_mb
    
    def _monitor_resources(self, pid):
        """监控资源使用的线程函数"""
        # 第一次调用，初始化
        initial_processes = self._get_process_tree(pid)
        for proc in initial_processes:
            if proc.pid not in self.process_cpu_times:
                try:
                    cpu_times = proc.cpu_times()
                    current_cpu_time = cpu_times.user + cpu_times.system
                    self.process_cpu_times[proc.pid] = {
                        'last_cpu_time': current_cpu_time,
                        'last_check_time': time.time()
                    }
                except:
                    pass
        
        self.last_calc_time = time.time()
        
        # 开始监控循环
        while self.running:
            try:
                # 获取当前进程树
                current_processes = self._get_process_tree(pid)
                
                if not current_processes:
                    # 如果进程树为空，可能是主进程已结束
                    break
                
                # 计算CPU使用率
                cpu_usage = self._calculate_cpu_usage(current_processes)
                
                # 计算内存使用量
                memory_usage = self._calculate_memory_usage(current_processes)
                
                # 记录数据
                current_time = datetime.now()
                self.timestamps.append(current_time)
                self.cpu_percentages.append(cpu_usage)
                self.memory_usages.append(memory_usage)
                
                # 更新最后计算时间
                self.last_calc_time = time.time()
                
            except Exception as e:
                print(f"监控数据收集错误: {e}", file=sys.stderr)
            
            # 固定间隔采样
            time.sleep(self.sampling_interval)
    
    def execute_with_monitoring(self):
        """执行命令并监控资源使用"""
        print(f"开始执行命令: {' '.join(self.command)}")
        print("-" * 60)
        
        # 记录开始时间
        self.start_time = time.perf_counter()
        
        try:
            # 启动子进程，不缓冲输出
            env = os.environ.copy()
            env['PYTHONUNBUFFERED'] = '1'
            
            # 注意：这里我们使用文本模式，但设置bufsize=0（无缓冲）
            self.process = subprocess.Popen(
                self.command,
                stdout=None,  # 直接继承当前进程的stdout
                stderr=None,  # 直接继承当前进程的stderr
                universal_newlines=True,
                bufsize=0,  # 无缓冲
                env=env
            )
            
            # 启动资源监控线程
            self.running = True
            self.monitor_thread = threading.Thread(
                target=self._monitor_resources,
                args=(self.process.pid,)
            )
            self.monitor_thread.daemon = True
            self.monitor_thread.start()
            
            # 等待进程结束
            return_code = self.process.wait()
            
        except FileNotFoundError:
            print(f"错误: 找不到命令 '{self.command[0]}'", file=sys.stderr)
            return_code = 127
        except Exception as e:
            print(f"执行命令时发生错误: {e}", file=sys.stderr)
            return_code = 1
        finally:
            # 停止监控
            self.running = False
            if self.monitor_thread:
                self.monitor_thread.join(timeout=2.0)
            
            # 记录结束时间
            self.end_time = time.perf_counter()
        
        return return_code
    
    def get_statistics(self):
        """获取资源使用统计信息"""
        if not self.timestamps:
            return None
        
        # 计算统计信息
        elapsed_time = self.end_time - self.start_time
        
        if self.cpu_percentages:
            max_cpu = max(self.cpu_percentages)
            avg_cpu = sum(self.cpu_percentages) / len(self.cpu_percentages)
        else:
            max_cpu = 0.0
            avg_cpu = 0.0
            
        if self.memory_usages:
            max_memory = max(self.memory_usages)
            avg_memory = sum(self.memory_usages) / len(self.memory_usages)
        else:
            max_memory = 0.0
            avg_memory = 0.0
        
        return {
            'total_time': elapsed_time,
            'max_cpu': max_cpu,
            'avg_cpu': avg_cpu,
            'max_memory': max_memory,
            'avg_memory': avg_memory,
            'sample_count': len(self.timestamps)
        }
    
    def generate_report(self):
        """生成资源使用报告"""
        stats = self.get_statistics()
        if not stats:
            print("警告: 没有收集到资源监控数据")
            return None
        
        elapsed_time = stats['total_time']
        max_cpu = stats['max_cpu']
        avg_cpu = stats['avg_cpu']
        max_memory = stats['max_memory']
        avg_memory = stats['avg_memory']
        
        hours = int(elapsed_time // 3600)
        minutes = int((elapsed_time % 3600) // 60)
        seconds = elapsed_time % 60
        
        print("\n" + "="*80)
        print("程序资源使用报告")
        print("="*80)
        print(f"执行命令: {' '.join(self.command)}")
        print(f"CPU核心数: {self.cpu_count}")
        print(f"总运行时间: {hours:02d}:{minutes:02d}:{seconds:06.3f}")
        print(f"最大CPU使用率: {max_cpu:.2f}% (峰值占用 {max_cpu/100:.2f} 个核心)")
        print(f"平均CPU使用率: {avg_cpu:.2f}% (平均占用 {avg_cpu/100:.2f} 个核心)")
        print(f"最大内存占用: {max_memory:.2f} MB")
        print(f"平均内存占用: {avg_memory:.2f} MB")
        print(f"采样点数: {stats['sample_count']}")
        
        # 找到峰值的时间点
        if self.cpu_percentages and self.memory_usages and self.timestamps:
            try:
                max_cpu_idx = list(self.cpu_percentages).index(max_cpu)
                max_memory_idx = list(self.memory_usages).index(max_memory)
                
                if max_cpu_idx < len(self.timestamps):
                    max_cpu_time = list(self.timestamps)[max_cpu_idx]
                    print(f"最大CPU使用时间: {max_cpu_time.strftime('%H:%M:%S')}")
                
                if max_memory_idx < len(self.timestamps):
                    max_memory_time = list(self.timestamps)[max_memory_idx]
                    print(f"最大内存占用时间: {max_memory_time.strftime('%H:%M:%S')}")
            except ValueError:
                pass
        
        print("="*80)
        
        return stats
    
    def plot_resource_usage(self, output_file=None, cmd_name="program"):
        """绘制资源使用曲线图"""
        if len(self.timestamps) < 2:
            print("警告: 数据点不足，无法生成图表")
            return
        
        # 准备数据
        timestamps = list(self.timestamps)
        cpu_data = list(self.cpu_percentages)
        memory_data = list(self.memory_usages)
        
        # 创建图表
        fig, ax1 = plt.subplots(figsize=(12, 8))
        
        # 设置标题
        total_duration = timestamps[-1] - timestamps[0]
        total_seconds = total_duration.total_seconds()

        # 根据总时长选择显示格式
        if total_seconds <= 60:
            # 不超过1分钟，显示秒数
            plt.title(f'Program Resource Usage - {cmd_name} (Duration: {int(total_seconds)} seconds)', fontsize=16, pad=20)
        else:
            # 超过1分钟，显示分钟数
            total_minutes = total_seconds / 60
            plt.title(f'Program Resource Usage - {cmd_name} (Duration: {total_minutes:.1f} minutes)', fontsize=16, pad=20)

        # Plot CPU usage (left axis)
        color = 'tab:blue'
        ax1.set_xlabel('Time', fontsize=12)
        ax1.set_ylabel('CPU Usage (%)', color=color, fontsize=12)
        line1 = ax1.plot(timestamps, cpu_data, color=color, linewidth=2, label='CPU Usage')
        ax1.tick_params(axis='y', labelcolor=color)
        ax1.grid(True, alpha=0.3)
        ax1.set_ylim(bottom=0)
        
        # 设置x轴时间格式
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
        plt.xticks(rotation=45, ha='right')
        
        # 创建第二个y轴用于内存
        ax2 = ax1.twinx()
        color = 'tab:red'
        ax2.set_ylabel('Memory Usage (MB)', color=color, fontsize=12)
        line2 = ax2.plot(timestamps, memory_data, color=color, linewidth=2, label='Memory Usage')
        ax2.tick_params(axis='y', labelcolor=color)
        ax2.set_ylim(bottom=0)
        
        # 添加图例
        lines = line1 + line2
        labels = [l.get_label() for l in lines]
        ax1.legend(lines, labels, loc='upper left', fontsize=10)
        
        # 添加统计信息文本
        stats = self.get_statistics()
        if stats:
            stats_text = (
                f"Max CPU: {stats['max_cpu']:.1f}%\n"
                f"Avg CPU: {stats['avg_cpu']:.1f}%\n"
                f"Max Memory: {stats['max_memory']:.1f} MB\n"
                f"Avg Memory: {stats['avg_memory']:.1f} MB\n"
                f"CPU Cores: {self.cpu_count}"
            )
            
            plt.figtext(0.02, 0.02, stats_text, fontsize=9, 
                       bbox=dict(boxstyle="round,pad=0.3", facecolor="wheat", alpha=0.6))
        
        plt.tight_layout()
        
        # 保存或显示图表
        if output_file:
            plt.savefig(output_file, dpi=150, bbox_inches='tight')
            print(f"Chart saved to: {output_file}")
        else:
            plt.show()
        
        plt.close()


def main():
    """主函数：解析命令行参数并启动监控"""
    if len(sys.argv) < 2:
        print("用法: python resource_monitor.py <命令> [参数...]")
        print("示例:")
        print("  python resource_monitor.py python a.py -a 1.txt -b 2.txt -o o.txt")
        print("  python resource_monitor.py python -u a.py -a 1.txt -b 2.txt -o o.txt")
        print("  python resource_monitor.py ./myprogram arg1 arg2")
        print("\n注意: 对于Python程序，建议使用 -u 参数确保无缓冲输出")
        sys.exit(1)
    
    # 获取要监控的命令
    command_to_monitor = sys.argv[1:]
    
    # 检查是否是 Python 程序，如果是则自动添加无缓冲参数
    if command_to_monitor[0] in ['python', 'python3', 'py'] and '-u' not in command_to_monitor:
        print("提示: 检测到Python程序，自动添加 -u 参数确保实时输出")
        print("      如果不需要，请手动指定完整命令")
        command_to_monitor.insert(1, '-u')
    
    # 创建监控器
    monitor = ResourceMonitor(
        command=command_to_monitor,
        sampling_interval=0.5,  # 0.5秒采样间隔
        max_samples=10000
    )
    
    # 执行命令并监控
    return_code = monitor.execute_with_monitoring()
    
    # 生成报告
    stats = monitor.generate_report()
    
    # 绘制图表
    if stats and stats['sample_count'] > 1:
        # 生成图表文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        cmd_name = os.path.basename(command_to_monitor[0]) if command_to_monitor else "program"
        chart_filename = f"resource_usage_{cmd_name}_{timestamp}.png"
        monitor.plot_resource_usage(chart_filename, cmd_name)
        
        # 尝试在命令行显示图表
        # try:
        #     if sys.platform == "darwin":  # macOS
        #         os.system(f"open '{chart_filename}'")
        #     elif sys.platform == "win32":  # Windows
        #         os.system(f"start '{chart_filename}'")
        #     else:  # Linux
        #         os.system(f"xdg-open '{chart_filename}'")
        # except:
        #     print(f"图表文件已生成: {chart_filename}")
        #     print("请手动打开查看")
    
    print(f"\n程序退出代码: {return_code}")
    sys.exit(return_code)


if __name__ == "__main__":
    main()

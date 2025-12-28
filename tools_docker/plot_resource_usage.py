#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import re
import sys


def parse_docker_stats(log_file):
    timestamps = []
    cpu_percentages = []
    memory_gbs = []
    with open(log_file, 'r') as f:
        for line in f:
            try:
                timestamp_match = re.search(
                    r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})', line)
                cpu_match = re.search(r'(\d+\.\d+)%', line)
                memory_match = re.search(r'(\d+\.\d+)GiB /', line)
                if timestamp_match and cpu_match and memory_match:
                    timestamp = timestamp_match.group(1)
                    cpu_pct = float(cpu_match.group(1))
                    memory_gb = float(memory_match.group(1))
                    timestamps.append(timestamp)
                    cpu_percentages.append(cpu_pct)
                    memory_gbs.append(memory_gb)
            except Exception:
                print(f"解析行时出错: {line}")
                continue
    df = pd.DataFrame({
        'timestamp': timestamps,
        'cpu_pct': cpu_percentages,
        'memory_gb': memory_gbs
    })
    return df


def plot_resource_usage(df, output_file='resource_usage.png'):
    df['datetime'] = pd.to_datetime(df['timestamp'])
    df['memory_gb_cum_avg'] = df['memory_gb'].expanding().mean()
    cpu_max_idx = df['cpu_pct'].idxmax()
    mem_max_idx = df['memory_gb'].idxmax()
    cpu_max = df.loc[cpu_max_idx]
    mem_max = df.loc[mem_max_idx]
    plt.figure(figsize=(12, 6))
    ax1 = plt.subplot(111)
    ax2 = ax1.twinx()
    line1, = ax1.plot(
        df['datetime'], df['cpu_pct'], 'b-', label='CPU Usage (%)')
    line2, = ax2.plot(
        df['datetime'], df['memory_gb'], 'r-', label='Memory Usage (GB)')
    line3, = ax2.plot(
        df['datetime'], df['memory_gb_cum_avg'],
        'g--', label='Memory Cumulative Average')
    ax1.annotate(
        f'Peak: {cpu_max["cpu_pct"]:.2f}%\n{cpu_max["timestamp"]}',
        xy=(cpu_max['datetime'], cpu_max['cpu_pct']),
        xytext=(0, 20),
        textcoords='offset points',
        arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=.2'),
        bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.3),
        ha='center',
        va='bottom',
        zorder=100
    )
    ax2.annotate(
        f'Peak: {mem_max["memory_gb"]:.2f}GB\n{mem_max["timestamp"]}',
        xy=(mem_max['datetime'], mem_max['memory_gb']),
        xytext=(20, 0),
        textcoords='offset points',
        arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=.2'),
        bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.3),
        ha='left',
        va='center',
        zorder=100
    )
    start_time = df['datetime'].min()
    end_time = df['datetime'].max()
    total_duration = end_time - start_time
    hours, remainder = divmod(total_duration.seconds, 3600)
    minutes = remainder // 60
    if total_duration.days > 0:
        duration_str = f"{total_duration.days} days {hours}h {minutes}m"
    else:
        duration_str = f"{hours}h {minutes}m"
    # 设置X轴为小时:分钟格式
    ax1.set_xlabel('Time')
    ax1.set_ylabel('CPU Usage (%)', color='b')
    ax2.set_ylabel('Memory Usage (GB)', color='r')
    # 配置X轴日期格式
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d %H:%M'))
    # 设置X轴主要刻度间隔
    # ax1.xaxis.set_major_locator(mdates.MinuteLocator(interval=10))
    # 旋转X轴标签以提高可读性
    plt.xticks(rotation=0)
    # Title with duration
    plt.title('Usage (%s)' % duration_str[:15])
    # Add total duration as text annotation instead of in title
    # text = 'Total Duration: %s' % duration_str
    # plt.figtext(0.5, 0.01, text, ha='center', fontsize=9)
    lines = [line1, line2, line3]
    labels = [line.get_label() for line in lines]
    plt.legend(lines, labels, loc='upper left')
    ax1.grid(True)
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f'Chart saved to {output_file}')
    print(f'Max CPU: {cpu_max["cpu_pct"]:.2f}% at {cpu_max["timestamp"]}')
    # Super short print
    print('Mem: %.0fGB' % mem_max['memory_gb'])
    print('At: %s' % mem_max['timestamp'][:10])


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python plot_resource_usage.py <log_file>")
        sys.exit(1)
    log_file = sys.argv[1]
    if log_file.lower().endswith('.png'):
        print(f"Error: '{log_file}' is a PNG file, please provide a log file.")
        sys.exit(1)
    output_file = log_file.replace('.log', '_resource_usage.png')
    try:
        df = parse_docker_stats(log_file)
        plot_resource_usage(df, output_file)
    except UnicodeDecodeError:
        print(f"Error: '{log_file}' invalid text log file (encoding error)")
        sys.exit(1)
    except FileNotFoundError:
        print(f"Error: Log file '{log_file}' not found")
        sys.exit(1)

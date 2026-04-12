#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AllToolkit - Monitoring Utils Examples

示例代码展示 monitoring_utils 模块的各种用法。
"""

import sys
import os

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    SystemMonitor,
    get_cpu_stats,
    get_memory_stats,
    get_disk_usage,
    get_network_stats,
    get_process_list,
    get_process_info,
    get_top_processes,
    get_system_info,
    get_all_stats,
    get_uptime,
    get_hostname,
    get_cpu_stats_percent
)


# =============================================================================
# Example 1: Basic System Information
# =============================================================================

def example_basic_info():
    """示例 1: 基本系统信息"""
    print("=" * 60)
    print("示例 1: 基本系统信息")
    print("=" * 60)
    
    hostname = get_hostname()
    uptime = get_uptime()
    info = get_system_info()
    
    print(f"主机名：{hostname}")
    
    # 格式化运行时间
    hours = int(uptime // 3600)
    minutes = int((uptime % 3600) // 60)
    seconds = int(uptime % 60)
    print(f"运行时间：{hours}小时 {minutes}分钟 {seconds}秒")
    
    print(f"平台：{info['platform']} {info['release']}")
    print(f"CPU 核心数：{info['cpu_count']}")
    print(f"Python 版本：{info['python_version']}")
    print()


# =============================================================================
# Example 2: CPU Monitoring
# =============================================================================

def example_cpu_monitoring():
    """示例 2: CPU 监控"""
    print("=" * 60)
    print("示例 2: CPU 监控")
    print("=" * 60)
    
    # 基本 CPU 统计
    cpu = get_cpu_stats()
    print("CPU 统计:")
    print(f"  使用率：{cpu.usage_percent:.1f}%")
    print(f"  核心数：{cpu.cores}")
    print(f"  负载平均：{cpu.load_avg}")
    print(f"  用户态：{cpu.user:.1f}%")
    print(f"  内核态：{cpu.system:.1f}%")
    print(f"  空闲：{cpu.idle:.1f}%")
    print(f"  I/O 等待：{cpu.iowait:.1f}%")
    
    # 间隔测量的 CPU 使用率
    print("\n测量 1 秒间隔的 CPU 使用率...")
    cpu_percent = get_cpu_stats_percent(interval=1.0)
    print(f"  实时使用率：{cpu_percent.usage_percent:.1f}%")
    print()


# =============================================================================
# Example 3: Memory Monitoring
# =============================================================================

def example_memory_monitoring():
    """示例 3: 内存监控"""
    print("=" * 60)
    print("示例 3: 内存监控")
    print("=" * 60)
    
    mem = get_memory_stats()
    
    print("内存统计:")
    print(f"  总内存：{mem.total_gb:.2f} GB")
    print(f"  已使用：{mem.used_gb:.2f} GB ({mem.usage_percent:.1f}%)")
    print(f"  可用：{mem.available_gb:.2f} GB")
    print(f"  空闲：{mem.free / 1024**3:.2f} GB")
    print(f"  缓冲：{mem.buffers / 1024**3:.2f} GB")
    print(f"  缓存：{mem.cached / 1024**3:.2f} GB")
    
    if mem.swap_total > 0:
        print("\nSwap:")
        print(f"  总 Swap: {mem.swap_total / 1024**3:.2f} GB")
        print(f"  已使用：{mem.swap_used / 1024**3:.2f} GB ({mem.swap_percent:.1f}%)")
        print(f"  空闲：{mem.swap_free / 1024**3:.2f} GB")
    print()


# =============================================================================
# Example 4: Disk Monitoring
# =============================================================================

def example_disk_monitoring():
    """示例 4: 磁盘监控"""
    print("=" * 60)
    print("示例 4: 磁盘监控")
    print("=" * 60)
    
    # 根目录
    root = get_disk_usage("/")
    print("根目录 (/):")
    print(f"  总容量：{root['total_gb']:.2f} GB")
    print(f"  已使用：{root['used_gb']:.2f} GB ({root['usage_percent']:.1f}%)")
    print(f"  可用：{root['available_gb']:.2f} GB")
    
    # 其他常见挂载点
    for path in ["/home", "/tmp", "/var"]:
        if os.path.exists(path):
            usage = get_disk_usage(path)
            if "error" not in usage:
                print(f"\n{path}:")
                print(f"  总容量：{usage['total_gb']:.2f} GB")
                print(f"  已使用：{usage['used_gb']:.2f} GB ({usage['usage_percent']:.1f}%)")
    print()


# =============================================================================
# Example 5: Network Monitoring
# =============================================================================

def example_network_monitoring():
    """示例 5: 网络监控"""
    print("=" * 60)
    print("示例 5: 网络监控")
    print("=" * 60)
    
    interfaces = get_network_stats()
    
    for iface in interfaces:
        print(f"接口：{iface.name}")
        print(f"  接收:")
        print(f"    字节：{iface.rx_bytes:,}")
        print(f"    MB: {iface.rx_bytes / 1024**2:.2f}")
        print(f"    数据包：{iface.rx_packets:,}")
        print(f"    错误：{iface.rx_errors}")
        print(f"    丢包：{iface.rx_dropped}")
        print(f"  发送:")
        print(f"    字节：{iface.tx_bytes:,}")
        print(f"    MB: {iface.tx_bytes / 1024**2:.2f}")
        print(f"    数据包：{iface.tx_packets:,}")
        print(f"    错误：{iface.tx_errors}")
        print(f"    丢包：{iface.tx_dropped}")
        print()


# =============================================================================
# Example 6: Process Monitoring
# =============================================================================

def example_process_monitoring():
    """示例 6: 进程监控"""
    print("=" * 60)
    print("示例 6: 进程监控")
    print("=" * 60)
    
    # 进程总数
    processes = get_process_list()
    print(f"系统进程总数：{len(processes)}")
    
    # Top 5 CPU
    print("\nTop 5 CPU 使用进程:")
    top_cpu = get_top_processes(5, by="cpu")
    for i, proc in enumerate(top_cpu, 1):
        print(f"  {i}. {proc.name:<20} PID: {proc.pid:<6} CPU: {proc.cpu_percent:>6.1f}%")
    
    # Top 5 Memory
    print("\nTop 5 内存使用进程:")
    top_mem = get_top_processes(5, by="memory")
    for i, proc in enumerate(top_mem, 1):
        print(f"  {i}. {proc.name:<20} PID: {proc.pid:<6} 内存：{proc.memory_percent:>6.2f}%")
    
    # 特定进程信息
    print("\nPID 1 (init/systemd) 信息:")
    proc = get_process_info(1)
    if proc:
        print(f"  名称：{proc.name}")
        print(f"  状态：{proc.status}")
        print(f"  父进程：{proc.ppid}")
        print(f"  线程数：{proc.num_threads}")
        print(f"  命令行：{proc.cmdline[:50]}...")
    print()


# =============================================================================
# Example 7: Complete System Snapshot
# =============================================================================

def example_system_snapshot():
    """示例 7: 完整系统快照"""
    print("=" * 60)
    print("示例 7: 完整系统快照")
    print("=" * 60)
    
    stats = get_all_stats()
    
    print(f"时间戳：{stats['timestamp']}")
    print(f"主机名：{stats['system']['hostname']}")
    print(f"平台：{stats['system']['platform']}")
    print(f"CPU 使用率：{stats['cpu']['usage_percent']:.1f}%")
    print(f"内存使用率：{stats['memory']['usage_percent']:.1f}%")
    print(f"磁盘使用率：{stats['disk']['usage_percent']:.1f}%")
    print(f"网络接口数：{len(stats['network'])}")
    print(f"监控进程数：{len(stats['top_cpu_processes'])}")
    print()


# =============================================================================
# Example 8: System Health Check
# =============================================================================

def example_health_check():
    """示例 8: 系统健康检查"""
    print("=" * 60)
    print("示例 8: 系统健康检查")
    print("=" * 60)
    
    stats = get_all_stats()
    issues = []
    
    # 检查 CPU
    cpu_usage = stats['cpu']['usage_percent']
    if cpu_usage > 90:
        issues.append(f"🔴 CPU 使用率过高：{cpu_usage:.1f}%")
    elif cpu_usage > 70:
        issues.append(f"🟡 CPU 使用率偏高：{cpu_usage:.1f}%")
    
    # 检查内存
    mem_usage = stats['memory']['usage_percent']
    if mem_usage > 90:
        issues.append(f"🔴 内存使用率过高：{mem_usage:.1f}%")
    elif mem_usage > 70:
        issues.append(f"🟡 内存使用率偏高：{mem_usage:.1f}%")
    
    # 检查磁盘
    disk_usage = stats['disk']['usage_percent']
    if disk_usage > 90:
        issues.append(f"🔴 磁盘使用率过高：{disk_usage:.1f}%")
    elif disk_usage > 80:
        issues.append(f"🟡 磁盘使用率偏高：{disk_usage:.1f}%")
    
    # 检查负载
    load_1min = stats['cpu']['load_avg'][0]
    cpu_cores = stats['system']['cpu_count']
    if load_1min > cpu_cores * 2:
        issues.append(f"🔴 系统负载过高：{load_1min:.2f} (核心数：{cpu_cores})")
    elif load_1min > cpu_cores:
        issues.append(f"🟡 系统负载偏高：{load_1min:.2f}")
    
    if issues:
        print("⚠️ 系统问题:")
        for issue in issues:
            print(f"  {issue}")
    else:
        print("✅ 系统健康 - 所有指标正常")
    print()


# =============================================================================
# Example 9: Using SystemMonitor Class
# =============================================================================

def example_monitor_class():
    """示例 9: 使用 SystemMonitor 类"""
    print("=" * 60)
    print("示例 9: 使用 SystemMonitor 类")
    print("=" * 60)
    
    monitor = SystemMonitor()
    
    # 链式调用
    cpu = monitor.get_cpu_stats()
    mem = monitor.get_memory_stats()
    disk = monitor.get_disk_usage("/")
    
    print("使用 SystemMonitor 类:")
    print(f"  CPU: {cpu.usage_percent:.1f}%")
    print(f"  内存：{mem.usage_percent:.1f}%")
    print(f"  磁盘：{disk['usage_percent']:.1f}%")
    
    # 获取磁盘 I/O 统计
    disk_io = monitor.get_disk_io_stats("sda")
    if disk_io.reads > 0 or disk_io.writes > 0:
        print(f"\n磁盘 I/O (sda):")
        print(f"  读取次数：{disk_io.reads:,}")
        print(f"  写入次数：{disk_io.writes:,}")
        print(f"  读取字节：{disk_io.read_bytes / 1024**3:.2f} GB")
        print(f"  写入字节：{disk_io.write_bytes / 1024**3:.2f} GB")
    print()


# =============================================================================
# Example 10: Data Class Usage
# =============================================================================

def example_data_classes():
    """示例 10: 数据类使用"""
    print("=" * 60)
    print("示例 10: 数据类使用")
    print("=" * 60)
    
    mem = get_memory_stats()
    
    # 使用数据类的方法
    print("MemoryStats 对象:")
    print(f"  total_gb 属性：{mem.total_gb:.2f} GB")
    print(f"  available_gb 属性：{mem.available_gb:.2f} GB")
    print(f"  used_gb 属性：{mem.used_gb:.2f} GB")
    
    # 转换为字典
    mem_dict = mem.to_dict()
    print(f"\n转换为字典:")
    print(f"  键数量：{len(mem_dict)}")
    print(f"  total: {mem_dict['total']:,} bytes")
    print()


# =============================================================================
# Main - Run All Examples
# =============================================================================

if __name__ == "__main__":
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 15 + "AllToolkit Monitoring Utils" + " " * 16 + "║")
    print("║" + " " * 20 + "示例代码集合" + " " * 20 + "║")
    print("╚" + "=" * 58 + "╝")
    print("\n")
    
    try:
        example_basic_info()
        example_cpu_monitoring()
        example_memory_monitoring()
        example_disk_monitoring()
        example_network_monitoring()
        example_process_monitoring()
        example_system_snapshot()
        example_health_check()
        example_monitor_class()
        example_data_classes()
        
        print("=" * 60)
        print("所有示例运行完成！")
        print("=" * 60)
        
    except Exception as e:
        print(f"运行示例时出错：{e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

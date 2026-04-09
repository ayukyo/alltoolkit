# -*- coding: utf-8 -*-
"""
AllToolkit - Shell Utilities 基础示例

演示 shell_utils 模块的基本用法。
"""

import sys
import os

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'shell_utils'))

from mod import *


def example_1_basic_command():
    """示例 1: 基本命令执行"""
    print("\n" + "="*50)
    print("示例 1: 基本命令执行")
    print("="*50)
    
    # 执行简单命令
    result = run_command('echo Hello from shell_utils!')
    print(f"输出：{result.stdout.strip()}")
    print(f"耗时：{result.duration:.4f}秒")
    
    # 执行带参数的命令
    result = run_command(['echo', 'Using', 'list', 'format'])
    print(f"列表格式：{result.stdout.strip()}")


def example_2_system_info():
    """示例 2: 系统信息查询"""
    print("\n" + "="*50)
    print("示例 2: 系统信息查询")
    print("="*50)
    
    print(f"操作系统：{get_os_type().value}")
    print(f"主机名：{get_hostname()}")
    print(f"用户名：{get_username()}")
    print(f"主目录：{get_home_directory()}")
    print(f"Python 版本：{get_platform_info()['python_version']}")


def example_3_file_operations():
    """示例 3: 文件操作"""
    print("\n" + "="*50)
    print("示例 3: 文件操作")
    print("="*50)
    
    # 创建测试目录
    test_dir = '/tmp/shell_utils_example'
    create_directory(test_dir, parents=True)
    print(f"✓ 创建目录：{test_dir}")
    
    # 创建测试文件
    test_file = os.path.join(test_dir, 'test.txt')
    with open(test_file, 'w') as f:
        f.write('Hello, World!')
    print(f"✓ 创建文件：{test_file}")
    
    # 获取文件大小
    size = get_file_size(test_file)
    print(f"文件大小：{format_file_size(size)}")
    
    # 复制文件
    backup_file = os.path.join(test_dir, 'test_backup.txt')
    copy_file(test_file, backup_file)
    print(f"✓ 复制文件：{backup_file}")
    
    # 列出目录内容
    result = ls(test_dir, '-la')
    print(f"\n目录内容:\n{result.stdout}")
    
    # 清理
    rm_rf(test_dir)
    print(f"✓ 清理测试目录")


def example_4_process_management():
    """示例 4: 进程管理"""
    print("\n" + "="*50)
    print("示例 4: 进程管理")
    print("="*50)
    
    # 获取进程数量
    count = get_process_count()
    print(f"系统进程数量：{count}")
    
    # 查找 Python 进程
    pids = find_processes_by_name('python')
    print(f"Python 进程数量：{len(pids)}")
    if pids:
        print(f"PID 列表：{pids[:5]}...")  # 只显示前 5 个
    
    # 检查当前进程
    current_pid = os.getpid()
    exists = process_exists(current_pid)
    print(f"当前进程 {current_pid} 存在：{exists}")


def example_5_environment_variables():
    """示例 5: 环境变量"""
    print("\n" + "="*50)
    print("示例 5: 环境变量")
    print("="*50)
    
    # 获取环境变量
    path = get_env_var('PATH', '')
    print(f"PATH 长度：{len(path)} 字符")
    
    # 设置临时环境变量
    set_env_var('MY_TEST_VAR', 'test_value')
    value = get_env_var('MY_TEST_VAR')
    print(f"自定义变量：MY_TEST_VAR={value}")
    
    # 显示部分环境变量
    all_vars = get_all_env_vars()
    print(f"\n环境变量总数：{len(all_vars)}")
    print("部分变量:")
    for i, (key, value) in enumerate(list(all_vars.items())[:5]):
        print(f"  {key}={value[:50]}..." if len(value) > 50 else f"  {key}={value}")


def example_6_network_tools():
    """示例 6: 网络工具"""
    print("\n" + "="*50)
    print("示例 6: 网络工具")
    print("="*50)
    
    # 获取 IP 地址
    local_ip = get_local_ip()
    print(f"本地 IP: {local_ip}")
    
    # Ping 测试
    print("\nPing 测试 (127.0.0.1):")
    result = ping('127.0.0.1', count=2, timeout=2)
    if result['success']:
        print("✓ 网络正常")
    else:
        print("✗ 网络异常")


def example_7_batch_commands():
    """示例 7: 批量命令执行"""
    print("\n" + "="*50)
    print("示例 7: 批量命令执行")
    print("="*50)
    
    # 顺序执行
    commands = [
        'echo Step 1: Starting...',
        'echo Step 2: Processing...',
        'echo Step 3: Completing...',
    ]
    
    print("顺序执行命令:")
    results = run_commands_sequential(commands)
    for i, result in enumerate(results, 1):
        status = "✓" if result.success else "✗"
        print(f"  {status} 命令 {i}: {result.duration:.4f}s")


def example_8_disk_memory():
    """示例 8: 磁盘和内存信息"""
    print("\n" + "="*50)
    print("示例 8: 磁盘和内存信息")
    print("="*50)
    
    # 磁盘使用
    if is_unix():
        disk = get_disk_usage('/')
    else:
        disk = get_disk_usage('C:\\')
    
    print("磁盘使用:")
    print(f"  总计：{format_file_size(disk['total'])}")
    print(f"  已用：{format_file_size(disk['used'])}")
    print(f"  剩余：{format_file_size(disk['free'])}")
    print(f"  使用率：{disk['percent']}%")
    
    # 内存使用
    mem = get_memory_info()
    print("\n内存使用:")
    print(f"  总计：{format_file_size(mem['total'])}")
    print(f"  已用：{format_file_size(mem['used'])}")
    print(f"  可用：{format_file_size(mem['available'])}")
    print(f"  使用率：{mem['percent']}%")


def main():
    """运行所有示例"""
    print("\n" + "="*60)
    print("  AllToolkit - Shell Utilities 基础示例")
    print("="*60)
    
    examples = [
        example_1_basic_command,
        example_2_system_info,
        example_3_file_operations,
        example_4_process_management,
        example_5_environment_variables,
        example_6_network_tools,
        example_7_batch_commands,
        example_8_disk_memory,
    ]
    
    for example in examples:
        try:
            example()
        except Exception as e:
            print(f"\n✗ 示例执行失败：{e}")
    
    print("\n" + "="*60)
    print("  所有示例执行完成!")
    print("="*60 + "\n")


if __name__ == '__main__':
    main()

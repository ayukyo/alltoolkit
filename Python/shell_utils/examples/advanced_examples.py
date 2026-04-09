# -*- coding: utf-8 -*-
"""
AllToolkit - Shell Utilities 高级示例

演示 shell_utils 模块的高级用法和实际场景。
"""

import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'shell_utils'))

from mod import *


def example_1_dev_workflow():
    """示例 1: 开发者工作流自动化"""
    print("\n" + "="*50)
    print("示例 1: 开发者工作流自动化")
    print("="*50)
    
    if not command_exists('git'):
        print("⚠️ Git 未安装，跳过此示例")
        return
    
    # 检查 Git 状态
    result = run_command('git status --short')
    if result.stdout.strip():
        print("当前有未提交的更改:")
        print(result.stdout[:200])
    else:
        print("✓ 工作区干净")
    
    # 获取最近提交
    result = run_command('git log --oneline -3')
    if result.success:
        print("\n最近提交:")
        print(result.stdout)


def example_2_system_monitor():
    """示例 2: 系统监控脚本"""
    print("\n" + "="*50)
    print("示例 2: 系统监控脚本")
    print("="*50)
    
    print(f"监控时间：{time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"主机：{get_hostname()}")
    print(f"系统：{get_os_type().value}")
    
    # 磁盘监控
    if is_unix():
        disk = get_disk_usage('/')
    else:
        disk = get_disk_usage('C:\\')
    
    status = "⚠️" if disk['percent'] > 80 else "✓"
    print(f"\n{status} 磁盘使用：{disk['percent']}%")
    
    # 内存监控
    mem = get_memory_info()
    status = "⚠️" if mem['percent'] > 80 else "✓"
    print(f"{status} 内存使用：{mem['percent']}%")
    
    # 进程数量
    count = get_process_count()
    print(f"进程数量：{count}")


def example_3_log_analyzer():
    """示例 3: 日志分析"""
    print("\n" + "="*50)
    print("示例 3: 日志分析")
    print("="*50)
    
    # 创建测试日志
    test_log = '/tmp/test.log'
    with open(test_log, 'w') as f:
        f.write("2024-01-01 10:00:00 INFO Application started\n")
        f.write("2024-01-01 10:01:00 ERROR Database connection failed\n")
        f.write("2024-01-01 10:02:00 WARN High memory usage\n")
        f.write("2024-01-01 10:03:00 ERROR Timeout exception\n")
        f.write("2024-01-01 10:04:00 INFO Request processed\n")
    
    # 统计错误数量
    if command_exists('grep'):
        result = grep('ERROR', test_log)
        error_count = len(result.stdout.strip().split('\n'))
        print(f"错误数量：{error_count}")
        
        # 显示错误
        if result.success:
            print("\n错误详情:")
            print(result.stdout)
    
    # 清理
    delete_file(test_log)


def example_4_batch_processor():
    """示例 4: 批量文件处理"""
    print("\n" + "="*50)
    print("示例 4: 批量文件处理")
    print("="*50)
    
    # 创建测试目录
    test_dir = '/tmp/batch_test'
    create_directory(test_dir)
    
    # 创建多个测试文件
    for i in range(5):
        file_path = os.path.join(test_dir, f'file_{i}.txt')
        with open(file_path, 'w') as f:
            f.write(f'Content of file {i}')
    
    print(f"✓ 创建 {5} 个测试文件")
    
    # 查找所有文件
    files = find_files(test_dir, '*.txt')
    print(f"✓ 找到 {len(files)} 个文件")
    
    # 批量处理（这里模拟处理）
    for file in files:
        size = get_file_size(file)
        print(f"  处理：{os.path.basename(file)} ({size} bytes)")
    
    # 清理
    rm_rf(test_dir)
    print("✓ 清理完成")


def example_5_async_execution():
    """示例 5: 异步任务执行"""
    print("\n" + "="*50)
    print("示例 5: 异步任务执行")
    print("="*50)
    
    # 启动后台任务
    print("启动后台任务...")
    proc = run_command_async('sleep 2 && echo Task completed!')
    print(f"任务 PID: {proc.pid}")
    
    # 执行其他工作
    print("执行其他工作...")
    time.sleep(1)
    
    # 等待任务完成
    print("等待任务完成...")
    stdout, stderr = proc.communicate()
    print(f"任务输出：{stdout.strip()}")


def example_6_env_loader():
    """示例 6: 环境变量加载器"""
    print("\n" + "="*50)
    print("示例 6: 环境变量加载器")
    print("="*50)
    
    # 创建测试 .env 文件
    env_file = '/tmp/test.env'
    with open(env_file, 'w') as f:
        f.write("# Database config\n")
        f.write("DB_HOST=localhost\n")
        f.write("DB_PORT=5432\n")
        f.write("DB_NAME=myapp\n")
        f.write("DB_USER=admin\n")
        f.write("DB_PASS='secret123'\n")
        f.write("DEBUG=true\n")
    
    print(f"创建测试 .env 文件：{env_file}")
    
    # 加载环境变量
    env_vars = load_env_file(env_file)
    print(f"\n加载了 {len(env_vars)} 个环境变量:")
    for key, value in env_vars.items():
        print(f"  {key}={value}")
    
    # 设置到当前进程
    for key, value in env_vars.items():
        set_env_var(key, value)
    
    # 验证
    print(f"\n验证：DB_HOST={get_env_var('DB_HOST')}")
    
    # 清理
    delete_file(env_file)


def example_7_health_check():
    """示例 7: 健康检查脚本"""
    print("\n" + "="*50)
    print("示例 7: 健康检查脚本")
    print("="*50)
    
    checks = []
    
    # 检查 1: 磁盘空间
    if is_unix():
        disk = get_disk_usage('/')
    else:
        disk = get_disk_usage('C:\\')
    disk_ok = disk['percent'] < 90
    checks.append(('磁盘空间', disk_ok, f"{disk['percent']}%"))
    
    # 检查 2: 内存
    mem = get_memory_info()
    mem_ok = mem['percent'] < 90
    checks.append(('内存使用', mem_ok, f"{mem['percent']}%"))
    
    # 检查 3: 临时目录可写
    temp_writable = os.access(get_temp_directory(), os.W_OK)
    checks.append(('临时目录', temp_writable, get_temp_directory()))
    
    # 检查 4: Python 版本
    py_version = get_platform_info()['python_version']
    checks.append(('Python 版本', True, py_version))
    
    # 显示结果
    print(f"主机：{get_hostname()}")
    print(f"时间：{time.strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    all_passed = True
    for name, passed, detail in checks:
        status = "✓" if passed else "✗"
        print(f"{status} {name}: {detail}")
        if not passed:
            all_passed = False
    
    print(f"\n{'✓ 健康检查通过' if all_passed else '✗ 存在问题需要关注'}")


def example_8_command_chain():
    """示例 8: 命令链/管道"""
    print("\n" + "="*50)
    print("示例 8: 命令链/管道")
    print("="*50)
    
    if not is_unix():
        print("⚠️ 此示例仅适用于 Unix-like 系统")
        return
    
    # 使用管道查找 Python 文件
    result = pipe_commands([
        'find . -name "*.py" -type f',
        'head -10',
        'wc -l'
    ])
    
    if result.success:
        print(f"前 10 个 Python 文件路径行数：{result.stdout.strip()}")
    
    # 另一种方式：使用 grep 过滤
    result = run_command('ls -la | head -5', shell=True)
    if result.success:
        print("\n目录列表前 5 行:")
        print(result.stdout)


def main():
    """运行所有高级示例"""
    print("\n" + "="*60)
    print("  AllToolkit - Shell Utilities 高级示例")
    print("="*60)
    
    examples = [
        example_1_dev_workflow,
        example_2_system_monitor,
        example_3_log_analyzer,
        example_4_batch_processor,
        example_5_async_execution,
        example_6_env_loader,
        example_7_health_check,
        example_8_command_chain,
    ]
    
    for example in examples:
        try:
            example()
        except Exception as e:
            print(f"\n✗ 示例执行失败：{e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "="*60)
    print("  所有高级示例执行完成!")
    print("="*60 + "\n")


if __name__ == '__main__':
    main()

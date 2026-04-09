# -*- coding: utf-8 -*-
"""
AllToolkit - Shell Utilities 测试套件

测试所有 Shell 工具函数的功能。
"""

import sys
import os
import time
import tempfile

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import *
from mod import OSType, CommandResult


# =============================================================================
# 测试工具函数
# =============================================================================

def print_section(title: str):
    """打印测试章节标题"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print('='*60)


def print_test(name: str, passed: bool, details: str = ''):
    """打印测试结果"""
    status = "✓ PASS" if passed else "✗ FAIL"
    print(f"  {status}: {name}")
    if details:
        print(f"         {details}")
    return passed


# =============================================================================
# 测试用例
# =============================================================================

def test_system_info():
    """测试系统信息工具"""
    print_section("测试系统信息工具")
    
    all_passed = True
    
    # 测试获取操作系统类型
    os_type = get_os_type()
    passed = isinstance(os_type, OSType)
    all_passed &= print_test("获取操作系统类型", passed, f"结果：{os_type.value}")
    
    # 测试平台信息
    info = get_platform_info()
    passed = all(k in info for k in ['os', 'system', 'python_version'])
    all_passed &= print_test("获取平台信息", passed, f"OS: {info['os']}, Python: {info['python_version']}")
    
    # 测试主机名
    hostname = get_hostname()
    passed = len(hostname) > 0
    all_passed &= print_test("获取主机名", passed, f"主机名：{hostname}")
    
    # 测试用户名
    username = get_username()
    passed = len(username) > 0
    all_passed &= print_test("获取用户名", passed, f"用户名：{username}")
    
    # 测试主目录
    home = get_home_directory()
    passed = os.path.exists(home)
    all_passed &= print_test("获取主目录", passed, f"主目录：{home}")
    
    return all_passed


def test_command_execution():
    """测试命令执行"""
    print_section("测试命令执行")
    
    all_passed = True
    
    # 测试基本命令执行
    result = run_command('echo Hello, World!')
    passed = result.success and 'Hello, World!' in result.stdout
    all_passed &= print_test("基本命令执行", passed, f"输出：{result.stdout.strip()}")
    
    # 测试命令列表形式
    result = run_command(['echo', 'test'])
    passed = result.success and 'test' in result.stdout
    all_passed &= print_test("命令列表形式", passed)
    
    # 测试工作目录
    result = run_command('pwd', cwd='/tmp')
    passed = result.success and 'tmp' in result.stdout.lower()
    all_passed &= print_test("指定工作目录", passed)
    
    # 测试超时
    result = run_command('sleep 0.1', timeout=1)
    passed = result.success
    all_passed &= print_test("命令超时控制", passed, f"耗时：{result.duration:.2f}s")
    
    # 测试错误命令
    result = run_command('nonexistent_command_xyz123')
    passed = not result.success
    all_passed &= print_test("错误命令处理", passed)
    
    # 测试 stdin 输入
    result = run_command('cat', stdin_input='test input')
    passed = result.success and 'test input' in result.stdout
    all_passed &= print_test("stdin 输入", passed)
    
    # 测试 CommandResult 布尔值
    result = run_command('true')
    passed = bool(result) == True
    all_passed &= print_test("CommandResult 布尔值 (成功)", passed)
    
    result = run_command('false')
    passed = bool(result) == False
    all_passed &= print_test("CommandResult 布尔值 (失败)", passed)
    
    return all_passed


def test_quick_commands():
    """测试快捷命令"""
    print_section("测试快捷命令")
    
    all_passed = True
    
    # 测试 pwd
    current = pwd()
    passed = os.path.exists(current)
    all_passed &= print_test("pwd 命令", passed, f"当前目录：{current}")
    
    # 测试 echo
    result = echo('test message')
    passed = result.success and 'test message' in result.stdout
    all_passed &= print_test("echo 命令", passed)
    
    # 测试 ls
    result = ls('.', '-la')
    passed = result.success and len(result.stdout) > 0
    all_passed &= print_test("ls 命令", passed, f"输出长度：{len(result.stdout)}")
    
    # 测试 which
    python_path = which('python') or which('python3')
    passed = python_path is not None and os.path.exists(python_path)
    all_passed &= print_test("which 命令", passed, f"Python 路径：{python_path}")
    
    # 测试 command_exists
    passed = command_exists('ls') or command_exists('dir')
    all_passed &= print_test("command_exists", passed)
    
    return all_passed


def test_file_operations():
    """测试文件操作"""
    print_section("测试文件操作")
    
    all_passed = True
    
    # 创建测试文件
    test_file = os.path.join(tempfile.gettempdir(), f'shell_utils_test_{int(time.time())}.txt')
    test_dir = os.path.join(tempfile.gettempdir(), f'shell_utils_test_dir_{int(time.time())}')
    
    try:
        # 测试创建目录
        passed = create_directory(test_dir)
        all_passed &= print_test("创建目录", passed, f"目录：{test_dir}")
        
        # 测试目录存在检查
        passed = directory_exists(test_dir)
        all_passed &= print_test("目录存在检查", passed)
        
        # 测试创建文件
        with open(test_file, 'w') as f:
            f.write('test content')
        passed = file_exists(test_file)
        all_passed &= print_test("文件存在检查", passed)
        
        # 测试文件大小
        size = get_file_size(test_file)
        passed = size == 12  # 'test content' = 12 bytes
        all_passed &= print_test("获取文件大小", passed, f"大小：{size} bytes")
        
        # 测试格式化文件大小
        formatted = format_file_size(1536)
        passed = '1.50 KB' in formatted
        all_passed &= print_test("格式化文件大小", passed, f"结果：{formatted}")
        
        # 测试复制文件
        test_file2 = test_file + '.bak'
        passed = copy_file(test_file, test_file2)
        all_passed &= print_test("复制文件", passed)
        
        # 测试移动文件
        test_file3 = test_file + '.moved'
        passed = move_file(test_file2, test_file3)
        all_passed &= print_test("移动文件", passed)
        
        # 测试删除文件
        passed = delete_file(test_file3)
        all_passed &= print_test("删除文件", passed)
        
        # 测试删除目录
        passed = remove_directory(test_dir)
        all_passed &= print_test("删除目录", passed)
        
    finally:
        # 清理
        for f in [test_file, test_file2, test_file3]:
            if os.path.exists(f):
                delete_file(f)
        if os.path.exists(test_dir):
            remove_directory(test_dir)
    
    return all_passed


def test_environment_variables():
    """测试环境变量"""
    print_section("测试环境变量")
    
    all_passed = True
    
    # 测试获取环境变量
    path = get_env_var('PATH', '')
    passed = len(path) > 0
    all_passed &= print_test("获取环境变量", passed, f"PATH 长度：{len(path)}")
    
    # 测试设置环境变量
    test_var = 'SHELL_UTILS_TEST_VAR'
    test_value = 'test_value_123'
    passed = set_env_var(test_var, test_value)
    all_passed &= print_test("设置环境变量", passed)
    
    # 验证设置
    value = get_env_var(test_var)
    passed = value == test_value
    all_passed &= print_test("验证环境变量", passed, f"值：{value}")
    
    # 测试获取所有环境变量
    all_vars = get_all_env_vars()
    passed = isinstance(all_vars, dict) and len(all_vars) > 0
    all_passed &= print_test("获取所有环境变量", passed, f"数量：{len(all_vars)}")
    
    return all_passed


def test_temp_files():
    """测试临时文件"""
    print_section("测试临时文件")
    
    all_passed = True
    
    # 测试获取临时目录
    temp_dir = get_temp_directory()
    passed = os.path.exists(temp_dir)
    all_passed &= print_test("获取临时目录", passed, f"目录：{temp_dir}")
    
    # 测试创建临时文件
    temp_file, fd = create_temp_file(prefix='shell_utils_', suffix='.txt')
    passed = os.path.exists(temp_file)
    all_passed &= print_test("创建临时文件", passed, f"文件：{temp_file}")
    
    # 写入测试
    try:
        with os.fdopen(fd, 'w') as f:
            f.write('test')
    except:
        os.close(fd)
    
    # 测试创建临时目录
    temp_dir2 = create_temp_directory(prefix='shell_utils_')
    passed = os.path.exists(temp_dir2) and os.path.isdir(temp_dir2)
    all_passed &= print_test("创建临时目录", passed, f"目录：{temp_dir2}")
    
    # 清理
    if os.path.exists(temp_file):
        delete_file(temp_file)
    if os.path.exists(temp_dir2):
        remove_directory(temp_dir2)
    
    return all_passed


def test_disk_and_memory():
    """测试磁盘和内存信息"""
    print_section("测试磁盘和内存信息")
    
    all_passed = True
    
    # 测试磁盘使用
    if is_unix():
        usage = get_disk_usage('/')
    else:
        usage = get_disk_usage('C:\\' if is_windows() else '/')
    
    passed = 'total' in usage and 'used' in usage and 'free' in usage
    all_passed &= print_test("获取磁盘使用", passed, f"总计：{format_file_size(usage['total'])}")
    
    # 测试内存信息
    mem = get_memory_info()
    passed = 'total' in mem and 'used' in mem
    all_passed &= print_test("获取内存信息", passed, f"总计：{format_file_size(mem['total'])}")
    
    return all_passed


def test_network_tools():
    """测试网络工具"""
    print_section("测试网络工具")
    
    all_passed = True
    
    # 测试获取本地 IP
    local_ip = get_local_ip()
    passed = len(local_ip) > 0 and '.' in local_ip
    all_passed &= print_test("获取本地 IP", passed, f"IP: {local_ip}")
    
    # 测试 ping (可能失败，取决于网络)
    result = ping('127.0.0.1', count=2, timeout=2)
    # 不强制要求成功，因为某些环境可能禁用 ping
    passed = isinstance(result, dict) and 'success' in result
    all_passed &= print_test("ping 命令", passed, f"成功：{result['success']}")
    
    return all_passed


def test_find_files():
    """测试文件查找"""
    print_section("测试文件查找")
    
    all_passed = True
    
    # 测试查找 Python 文件
    if is_unix():
        files = find_files('/tmp', '*.txt', max_depth=2)
    else:
        files = find_files(tempfile.gettempdir(), '*.txt', max_depth=2)
    
    passed = isinstance(files, list)
    all_passed &= print_test("查找文件", passed, f"找到 {len(files)} 个文件")
    
    return all_passed


def test_sequential_commands():
    """测试顺序执行命令"""
    print_section("测试顺序执行命令")
    
    all_passed = True
    
    # 测试顺序执行
    commands = ['echo first', 'echo second', 'echo third']
    results = run_commands_sequential(commands)
    
    passed = len(results) == 3 and all(r.success for r in results)
    all_passed &= print_test("顺序执行命令", passed, f"执行了 {len(results)} 个命令")
    
    # 测试出错停止
    commands = ['echo before', 'false', 'echo after']
    results = run_commands_sequential(commands, stop_on_error=True)
    
    passed = len(results) == 2  # 应该在 false 处停止
    all_passed &= print_test("出错时停止", passed, f"执行了 {len(results)} 个命令")
    
    return all_passed


def test_process_management():
    """测试进程管理"""
    print_section("测试进程管理")
    
    all_passed = True
    
    # 测试进程计数
    count = get_process_count()
    passed = count > 0
    all_passed &= print_test("获取进程数量", passed, f"数量：{count}")
    
    # 测试查找进程
    pids = find_processes_by_name('python')
    passed = isinstance(pids, list)
    all_passed &= print_test("查找进程", passed, f"找到 {len(pids)} 个 Python 进程")
    
    # 测试进程存在检查
    current_pid = os.getpid()
    passed = process_exists(current_pid)
    all_passed &= print_test("检查进程存在", passed, f"PID: {current_pid}")
    
    return all_passed


def test_async_command():
    """测试异步命令执行"""
    print_section("测试异步命令执行")
    
    all_passed = True
    
    # 测试异步执行
    proc = run_command_async('sleep 0.5')
    passed = proc is not None and proc.pid > 0
    all_passed &= print_test("异步执行命令", passed, f"PID: {proc.pid}")
    
    # 等待完成
    proc.wait()
    passed = proc.returncode == 0
    all_passed &= print_test("等待异步完成", passed)
    
    return all_passed


def test_os_specific():
    """测试操作系统特定功能"""
    print_section("测试操作系统特定功能")
    
    all_passed = True
    
    # 测试 is_windows
    is_win = is_windows()
    is_unx = is_unix()
    passed = (is_win and not is_unx) or (not is_win and is_unx)
    all_passed &= print_test("操作系统检测", passed, f"Windows: {is_win}, Unix: {is_unx}")
    
    # 测试 get_shell
    shell = get_shell()
    passed = len(shell) > 0
    all_passed &= print_test("获取 Shell", passed, f"Shell: {shell}")
    
    return all_passed


def test_edge_cases():
    """测试边界情况"""
    print_section("测试边界情况")
    
    all_passed = True
    
    # 测试空命令 (空命令在 bash 中是合法的 no-op)
    result = run_command('')
    passed = result.success  # 空命令应该成功 (no-op)
    all_passed &= print_test("空命令处理", passed, "空命令是合法的 no-op")
    
    # 测试长输出
    result = run_command('seq 1 100')
    passed = result.success and '100' in result.stdout
    all_passed &= print_test("长输出处理", passed)
    
    # 测试特殊字符
    result = run_command('echo "hello world"')
    passed = result.success and 'hello world' in result.stdout
    all_passed &= print_test("特殊字符处理", passed)
    
    return all_passed


# =============================================================================
# 主测试函数
# =============================================================================

def run_all_tests():
    """运行所有测试"""
    print("\n" + "="*60)
    print("  AllToolkit - Shell Utilities 测试套件")
    print("="*60)
    print(f"  Python 版本：{sys.version.split()[0]}")
    print(f"  操作系统：{get_os_type().value}")
    print(f"  开始时间：{time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    tests = [
        ("系统信息", test_system_info),
        ("命令执行", test_command_execution),
        ("快捷命令", test_quick_commands),
        ("文件操作", test_file_operations),
        ("环境变量", test_environment_variables),
        ("临时文件", test_temp_files),
        ("磁盘和内存", test_disk_and_memory),
        ("网络工具", test_network_tools),
        ("文件查找", test_find_files),
        ("顺序执行", test_sequential_commands),
        ("进程管理", test_process_management),
        ("异步执行", test_async_command),
        ("操作系统特定", test_os_specific),
        ("边界情况", test_edge_cases),
    ]
    
    results = {}
    
    for name, test_func in tests:
        try:
            passed = test_func()
            results[name] = passed
        except Exception as e:
            print(f"\n  ✗ EXCEPTION in {name}: {e}")
            results[name] = False
    
    # 汇总结果
    print("\n" + "="*60)
    print("  测试结果汇总")
    print("="*60)
    
    total = len(results)
    passed = sum(1 for v in results.values() if v)
    
    for name, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"  {status}: {name}")
    
    print(f"\n  总计：{passed}/{total} 通过")
    print(f"  通过率：{passed/total*100:.1f}%")
    
    if passed == total:
        print("\n  🎉 所有测试通过!")
        return True
    else:
        print(f"\n  ⚠️  {total - passed} 个测试失败")
        return False


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)

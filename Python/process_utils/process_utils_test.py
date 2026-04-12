"""
AllToolkit - Python Process Utilities Test Suite

Comprehensive test suite for process management utilities.
Run with: python -m pytest process_utils_test.py -v
      or: python process_utils_test.py
"""

import sys
import os
import time
import signal
import tempfile
import threading

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    ProcessManager,
    ProcessUtils,
    WorkerPool,
    ProcessResult,
    ProcessInfo,
    ProcessConfig,
    ProcessPriority,
    ProcessState,
    run,
    run_shell,
    run_background,
    exists,
    which,
    get_pid,
    get_env,
    set_env,
    DEFAULT_TIMEOUT,
)


# =============================================================================
# Test ProcessResult
# =============================================================================

def test_process_result_creation():
    """Test ProcessResult creation and properties."""
    result = ProcessResult(
        returncode=0,
        stdout="output",
        stderr="",
        execution_time=1.5,
        pid=12345,
        command="test command",
        state=ProcessState.COMPLETED,
    )
    
    assert result.returncode == 0
    assert result.stdout == "output"
    assert result.stderr == ""
    assert result.execution_time == 1.5
    assert result.pid == 12345
    assert result.command == "test command"
    assert result.state == ProcessState.COMPLETED
    print("✓ test_process_result_creation passed")


def test_process_result_success():
    """Test ProcessResult success method."""
    # Successful result
    result1 = ProcessResult(
        returncode=0,
        stdout="",
        stderr="",
        execution_time=1.0,
        state=ProcessState.COMPLETED,
    )
    assert result1.success() is True
    
    # Failed with non-zero return code
    result2 = ProcessResult(
        returncode=1,
        stdout="",
        stderr="error",
        execution_time=1.0,
        state=ProcessState.COMPLETED,
    )
    assert result2.success() is False
    
    # Timeout
    result3 = ProcessResult(
        returncode=-9,
        stdout="",
        stderr="",
        execution_time=30.0,
        state=ProcessState.TIMEOUT,
    )
    assert result3.success() is False
    
    print("✓ test_process_result_success passed")


def test_process_result_to_dict():
    """Test ProcessResult to_dict method."""
    result = ProcessResult(
        returncode=0,
        stdout="out",
        stderr="err",
        execution_time=2.5,
        pid=999,
        command="cmd",
        state=ProcessState.COMPLETED,
    )
    
    d = result.to_dict()
    assert d['returncode'] == 0
    assert d['stdout'] == "out"
    assert d['stderr'] == "err"
    assert d['execution_time'] == 2.5
    assert d['pid'] == 999
    assert d['command'] == "cmd"
    assert d['state'] == "completed"
    assert d['success'] is True
    print("✓ test_process_result_to_dict passed")


def test_process_result_str():
    """Test ProcessResult string representation."""
    result = ProcessResult(
        returncode=0,
        stdout="",
        stderr="",
        execution_time=1.234,
        state=ProcessState.COMPLETED,
    )
    
    s = str(result)
    assert "ProcessResult" in s
    assert "code=0" in s
    assert "time=1.234" in s
    assert "state=completed" in s
    print("✓ test_process_result_str passed")


# =============================================================================
# Test ProcessConfig
# =============================================================================

def test_process_config_defaults():
    """Test ProcessConfig default values."""
    config = ProcessConfig()
    
    assert config.timeout == DEFAULT_TIMEOUT
    assert config.cwd is None
    assert config.env is None
    assert config.shell is False
    assert config.capture_output is True
    assert config.universal_newlines is True
    assert config.priority == ProcessPriority.NORMAL
    print("✓ test_process_config_defaults passed")


def test_process_config_custom():
    """Test ProcessConfig with custom values."""
    config = ProcessConfig(
        timeout=60.0,
        cwd="/tmp",
        env={"KEY": "value"},
        shell=True,
        priority=ProcessPriority.HIGH,
    )
    
    assert config.timeout == 60.0
    assert config.cwd == "/tmp"
    assert config.env == {"KEY": "value"}
    assert config.shell is True
    assert config.priority == ProcessPriority.HIGH
    print("✓ test_process_config_custom passed")


def test_process_config_to_dict():
    """Test ProcessConfig to_dict method."""
    config = ProcessConfig(
        timeout=30.0,
        cwd="/home",
        shell=True,
        priority=ProcessPriority.LOW,
    )
    
    d = config.to_dict()
    assert d['timeout'] == 30.0
    assert d['cwd'] == "/home"
    assert d['shell'] is True
    assert d['priority'] == 10  # LOW = 10
    print("✓ test_process_config_to_dict passed")


# =============================================================================
# Test ProcessPriority Enum
# =============================================================================

def test_process_priority_values():
    """Test ProcessPriority enum values."""
    assert ProcessPriority.VERY_HIGH.value == -20
    assert ProcessPriority.HIGH.value == -10
    assert ProcessPriority.NORMAL.value == 0
    assert ProcessPriority.LOW.value == 10
    assert ProcessPriority.VERY_LOW.value == 19
    print("✓ test_process_priority_values passed")


# =============================================================================
# Test ProcessState Enum
# =============================================================================

def test_process_state_values():
    """Test ProcessState enum values."""
    assert ProcessState.RUNNING.value == "running"
    assert ProcessState.STOPPED.value == "stopped"
    assert ProcessState.COMPLETED.value == "completed"
    assert ProcessState.FAILED.value == "failed"
    assert ProcessState.TIMEOUT.value == "timeout"
    assert ProcessState.UNKNOWN.value == "unknown"
    print("✓ test_process_state_values passed")


# =============================================================================
# Test ProcessManager
# =============================================================================

def test_process_manager_creation():
    """Test ProcessManager creation."""
    manager = ProcessManager()
    assert manager is not None
    assert manager.get_running_count() == 0
    print("✓ test_process_manager_creation passed")


def test_process_manager_run_simple():
    """Test ProcessManager run with simple command."""
    manager = ProcessManager()
    
    # Test with echo command
    result = manager.run("echo hello")
    
    assert result.returncode == 0
    assert "hello" in result.stdout
    assert result.state == ProcessState.COMPLETED
    assert result.success() is True
    assert result.execution_time >= 0
    print("✓ test_process_manager_run_simple passed")


def test_process_manager_run_with_args():
    """Test ProcessManager run with command arguments."""
    manager = ProcessManager()
    
    result = manager.run(["echo", "test", "message"])
    
    assert result.returncode == 0
    assert "test message" in result.stdout
    assert result.success() is True
    print("✓ test_process_manager_run_with_args passed")


def test_process_manager_run_shell():
    """Test ProcessManager run with shell mode."""
    manager = ProcessManager()
    config = ProcessConfig(shell=True)
    
    result = manager.run("echo hello && echo world", config)
    
    assert result.returncode == 0
    assert "hello" in result.stdout
    assert "world" in result.stdout
    print("✓ test_process_manager_run_shell passed")


def test_process_manager_run_timeout():
    """Test ProcessManager run with timeout."""
    manager = ProcessManager()
    config = ProcessConfig(timeout=1.0)
    
    # Sleep for longer than timeout
    result = manager.run("sleep 5", config)
    
    assert result.state == ProcessState.TIMEOUT
    assert result.returncode == -9
    assert result.success() is False
    print("✓ test_process_manager_run_timeout passed")


def test_process_manager_run_with_cwd():
    """Test ProcessManager run with working directory."""
    manager = ProcessManager()
    
    # Create temp directory
    with tempfile.TemporaryDirectory() as tmpdir:
        config = ProcessConfig(cwd=tmpdir)
        result = manager.run("pwd", config)
        
        assert result.returncode == 0
        assert tmpdir in result.stdout
    print("✓ test_process_manager_run_with_cwd passed")


def test_process_manager_run_with_env():
    """Test ProcessManager run with custom environment."""
    manager = ProcessManager()
    config = ProcessConfig(env={"TEST_VAR": "test_value"})
    
    result = manager.run("echo $TEST_VAR", config)
    
    # Note: shell mode needed for env var expansion
    config_shell = ProcessConfig(env={"TEST_VAR": "test_value"}, shell=True)
    result = manager.run("echo $TEST_VAR", config_shell)
    
    assert result.returncode == 0
    assert "test_value" in result.stdout
    print("✓ test_process_manager_run_with_env passed")


def test_process_manager_run_failing_command():
    """Test ProcessManager run with failing command."""
    manager = ProcessManager()
    config = ProcessConfig(shell=True)
    
    result = manager.run("exit 1", config)
    
    assert result.returncode == 1
    assert result.success() is False
    assert result.state == ProcessState.COMPLETED
    print("✓ test_process_manager_run_failing_command passed")


def test_process_manager_run_nonexistent_command():
    """Test ProcessManager run with nonexistent command."""
    manager = ProcessManager()
    
    result = manager.run("nonexistent_command_xyz123")
    
    assert result.returncode != 0
    assert result.state == ProcessState.FAILED
    assert result.success() is False
    print("✓ test_process_manager_run_nonexistent_command passed")


def test_process_manager_get_result():
    """Test ProcessManager get_result method."""
    manager = ProcessManager()
    
    result = manager.run("echo test")
    pid = result.pid
    
    retrieved = manager.get_result(pid)
    assert retrieved is not None
    assert retrieved.pid == pid
    assert "test" in retrieved.stdout
    print("✓ test_process_manager_get_result passed")


def test_process_manager_get_all_results():
    """Test ProcessManager get_all_results method."""
    manager = ProcessManager()
    
    # Run multiple commands
    manager.run("echo one")
    manager.run("echo two")
    manager.run("echo three")
    
    results = manager.get_all_results()
    assert len(results) >= 3
    print("✓ test_process_manager_get_all_results passed")


def test_process_manager_is_running():
    """Test ProcessManager is_running method."""
    manager = ProcessManager()
    
    # Run quick command
    result = manager.run("echo done")
    
    # Should be completed, not running
    assert manager.is_running(result.pid) is False
    print("✓ test_process_manager_is_running passed")


def test_process_manager_running_count():
    """Test ProcessManager get_running_count method."""
    manager = ProcessManager()
    
    # Initially zero
    assert manager.get_running_count() == 0
    
    # Run quick command
    manager.run("echo test")
    
    # Should be zero after completion
    assert manager.get_running_count() == 0
    print("✓ test_process_manager_running_count passed")


# =============================================================================
# Test ProcessUtils
# =============================================================================

def test_process_utils_run():
    """Test ProcessUtils.run static method."""
    result = ProcessUtils.run("echo hello")
    
    assert result.returncode == 0
    assert "hello" in result.stdout
    print("✓ test_process_utils_run passed")


def test_process_utils_run_shell():
    """Test ProcessUtils.run_shell method."""
    result = ProcessUtils.run_shell("echo test123")
    
    assert result.returncode == 0
    assert "test123" in result.stdout
    print("✓ test_process_utils_run_shell passed")


def test_process_utils_run_with_timeout():
    """Test ProcessUtils.run with timeout."""
    result = ProcessUtils.run("sleep 0.5", timeout=2.0)
    
    assert result.success() is True
    print("✓ test_process_utils_run_with_timeout passed")


def test_process_utils_exists_true():
    """Test ProcessUtils.exists with existing command."""
    assert ProcessUtils.exists("python") is True or ProcessUtils.exists("python3") is True
    print("✓ test_process_utils_exists_true passed")


def test_process_utils_exists_false():
    """Test ProcessUtils.exists with nonexistent command."""
    assert ProcessUtils.exists("nonexistent_cmd_xyz789") is False
    print("✓ test_process_utils_exists_false passed")


def test_process_utils_which():
    """Test ProcessUtils.which method."""
    path = ProcessUtils.which("python") or ProcessUtils.which("python3")
    assert path is not None
    assert os.path.isabs(path)
    print("✓ test_process_utils_which passed")


def test_process_utils_get_pid():
    """Test ProcessUtils.get_pid method."""
    pid = ProcessUtils.get_pid()
    assert pid > 0
    assert pid == os.getpid()
    print("✓ test_process_utils_get_pid passed")


def test_process_utils_get_ppid():
    """Test ProcessUtils.get_ppid method."""
    ppid = ProcessUtils.get_ppid()
    assert ppid > 0
    assert ppid == os.getppid()
    print("✓ test_process_utils_get_ppid passed")


def test_process_utils_get_cwd():
    """Test ProcessUtils.get_cwd method."""
    cwd = ProcessUtils.get_cwd()
    assert cwd == os.getcwd()
    print("✓ test_process_utils_get_cwd passed")


def test_process_utils_get_env():
    """Test ProcessUtils.get_env method."""
    # Get existing env var
    path = ProcessUtils.get_env("PATH")
    assert path is not None
    assert len(path) > 0
    
    # Get with default
    value = ProcessUtils.get_env("NONEXISTENT_VAR_XYZ", "default")
    assert value == "default"
    print("✓ test_process_utils_get_env passed")


def test_process_utils_set_env():
    """Test ProcessUtils.set_env method."""
    test_var = "TEST_PROCESS_UTILS_VAR"
    test_value = "test_value_123"
    
    # Set variable
    ProcessUtils.set_env(test_var, test_value)
    assert ProcessUtils.get_env(test_var) == test_value
    
    # Clean up
    ProcessUtils.unset_env(test_var)
    assert ProcessUtils.get_env(test_var) is None
    print("✓ test_process_utils_set_env passed")


def test_process_utils_unset_env():
    """Test ProcessUtils.unset_env method."""
    test_var = "TEST_UNSET_VAR"
    
    # Set then unset
    ProcessUtils.set_env(test_var, "value")
    assert ProcessUtils.get_env(test_var) is not None
    
    ProcessUtils.unset_env(test_var)
    assert ProcessUtils.get_env(test_var) is None
    print("✓ test_process_utils_unset_env passed")


def test_process_utils_get_env_snapshot():
    """Test ProcessUtils.get_env_snapshot method."""
    snapshot = ProcessUtils.get_env_snapshot()
    
    assert isinstance(snapshot, dict)
    assert len(snapshot) > 0
    assert "PATH" in snapshot or len(snapshot) > 0  # Should have some env vars
    print("✓ test_process_utils_get_env_snapshot passed")


def test_process_utils_sleep():
    """Test ProcessUtils.sleep method."""
    start = time.time()
    ProcessUtils.sleep(0.1)
    elapsed = time.time() - start
    
    assert elapsed >= 0.09  # Allow small tolerance
    print("✓ test_process_utils_sleep passed")


# =============================================================================
# Test Convenience Functions
# =============================================================================

def test_run_function():
    """Test module-level run function."""
    result = run("echo test")
    assert result.success() is True
    assert "test" in result.stdout
    print("✓ test_run_function passed")


def test_run_shell_function():
    """Test module-level run_shell function."""
    result = run_shell("echo hello")
    assert result.success() is True
    print("✓ test_run_shell_function passed")


def test_exists_function():
    """Test module-level exists function."""
    assert exists("ls") is True
    assert exists("nonexistent_xyz") is False
    print("✓ test_exists_function passed")


def test_which_function():
    """Test module-level which function."""
    path = which("ls")
    assert path is not None
    assert os.path.exists(path)
    print("✓ test_which_function passed")


def test_get_pid_function():
    """Test module-level get_pid function."""
    pid = get_pid()
    assert pid > 0
    print("✓ test_get_pid_function passed")


def test_get_env_function():
    """Test module-level get_env function."""
    value = get_env("HOME", "/default")
    assert value is not None or value == "/default"
    print("✓ test_get_env_function passed")


# =============================================================================
# Test WorkerPool
# =============================================================================

def worker_square(x):
    """Worker function for testing."""
    return x * x


def worker_slow(x):
    """Slow worker function for testing."""
    time.sleep(0.1)
    return x * 2


def test_worker_pool_creation():
    """Test WorkerPool creation."""
    pool = WorkerPool(num_workers=2)
    assert pool.num_workers == 2
    assert pool._pool is None
    print("✓ test_worker_pool_creation passed")


def test_worker_pool_start_stop():
    """Test WorkerPool start and stop."""
    pool = WorkerPool(num_workers=2)
    
    pool.start()
    assert pool._pool is not None
    
    pool.stop(graceful=True)
    assert pool._pool is None
    print("✓ test_worker_pool_start_stop passed")


def test_worker_pool_map():
    """Test WorkerPool map method."""
    with WorkerPool(num_workers=2) as pool:
        results = pool.map(worker_square, [1, 2, 3, 4, 5])
        
        assert results == [1, 4, 9, 16, 25]
    print("✓ test_worker_pool_map passed")


def test_worker_pool_apply():
    """Test WorkerPool apply method."""
    with WorkerPool(num_workers=2) as pool:
        result = pool.apply(worker_square, args=(5,))
        assert result == 25
    print("✓ test_worker_pool_apply passed")


def test_worker_pool_apply_async():
    """Test WorkerPool apply_async method."""
    with WorkerPool(num_workers=2) as pool:
        async_result = pool.apply_async(worker_square, args=(6,))
        result = async_result.get(timeout=5)
        assert result == 36
    print("✓ test_worker_pool_apply_async passed")


def test_worker_pool_map_async():
    """Test WorkerPool map_async method."""
    with WorkerPool(num_workers=2) as pool:
        async_result = pool.map_async(worker_square, [1, 2, 3])
        results = async_result.get(timeout=5)
        assert results == [1, 4, 9]
    print("✓ test_worker_pool_map_async passed")


def test_worker_pool_get_results():
    """Test WorkerPool get_results method."""
    pool = WorkerPool(num_workers=2)
    pool.start()
    
    pool.map(worker_square, [1, 2, 3])
    
    results = pool.get_results()
    assert results == [1, 4, 9]
    
    pool.stop()
    print("✓ test_worker_pool_get_results passed")


def test_worker_pool_context_manager():
    """Test WorkerPool as context manager."""
    with WorkerPool(num_workers=2) as pool:
        results = pool.map(worker_square, [1, 2, 3, 4])
        assert results == [1, 4, 9, 16]
    
    # Pool should be stopped after context
    assert pool._pool is None
    print("✓ test_worker_pool_context_manager passed")


# =============================================================================
# Test ProcessInfo
# =============================================================================

def test_process_info_creation():
    """Test ProcessInfo creation."""
    info = ProcessInfo(
        pid=12345,
        name="test_process",
        cmdline=["python", "test.py"],
        status="running",
        ppid=1,
        username="admin",
    )
    
    assert info.pid == 12345
    assert info.name == "test_process"
    assert info.cmdline == ["python", "test.py"]
    assert info.status == "running"
    assert info.ppid == 1
    assert info.username == "admin"
    print("✓ test_process_info_creation passed")


def test_process_info_to_dict():
    """Test ProcessInfo to_dict method."""
    info = ProcessInfo(
        pid=999,
        name="myapp",
        cmdline=["myapp", "--flag"],
        status="sleeping",
        ppid=100,
        username="user",
        cpu_percent=5.5,
        memory_percent=2.3,
    )
    
    d = info.to_dict()
    assert d['pid'] == 999
    assert d['name'] == "myapp"
    assert d['cmdline'] == ["myapp", "--flag"]
    assert d['status'] == "sleeping"
    assert d['ppid'] == 100
    assert d['username'] == "user"
    assert d['cpu_percent'] == 5.5
    assert d['memory_percent'] == 2.3
    print("✓ test_process_info_to_dict passed")


# =============================================================================
# Edge Cases and Boundary Tests
# =============================================================================

def test_empty_command():
    """Test handling of empty command."""
    manager = ProcessManager()
    config = ProcessConfig(timeout=1.0)
    
    # Empty command should fail gracefully
    result = manager.run("", config)
    assert result.state in [ProcessState.FAILED, ProcessState.COMPLETED]
    print("✓ test_empty_command passed")


def test_very_long_output():
    """Test handling of very long output."""
    manager = ProcessManager()
    
    # Generate long output using a script file
    script_content = "print('x' * 10000)"
    with open("test_long_output.py", "w") as f:
        f.write(script_content)
    
    try:
        result = manager.run("python test_long_output.py")
        assert result.success() is True
        assert len(result.stdout) >= 10000
    finally:
        import os
        if os.path.exists("test_long_output.py"):
            os.remove("test_long_output.py")
    
    print("✓ test_very_long_output passed")


def test_unicode_output():
    """Test handling of unicode output."""
    manager = ProcessManager()
    
    result = manager.run("echo '你好世界'")
    
    assert result.success() is True
    assert "你好世界" in result.stdout or len(result.stdout) > 0
    print("✓ test_unicode_output passed")


def test_multiline_output():
    """Test handling of multiline output."""
    manager = ProcessManager()
    
    result = manager.run("printf 'line1\\nline2\\nline3'")
    
    assert result.success() is True
    assert "line1" in result.stdout
    assert "line2" in result.stdout
    assert "line3" in result.stdout
    print("✓ test_multiline_output passed")


def test_stderr_capture():
    """Test stderr capture."""
    manager = ProcessManager()
    
    # Command that writes to stderr (use a simple failing command)
    result = manager.run("ls /nonexistent_directory_xyz123 2>&1", 
                         ProcessConfig(shell=True))
    
    # Should have some error output
    assert len(result.stderr) > 0 or len(result.stdout) > 0
    print("✓ test_stderr_capture passed")


def test_both_stdout_stderr():
    """Test capturing both stdout and stderr."""
    manager = ProcessManager()
    
    # Use shell to capture both streams
    result = manager.run("echo 'stdout message' && ls /nonexistent_xyz 2>&1",
                         ProcessConfig(shell=True))
    
    assert "stdout message" in result.stdout
    print("✓ test_both_stdout_stderr passed")


def test_execution_time_accuracy():
    """Test execution time measurement accuracy."""
    manager = ProcessManager()
    
    # Command with known duration
    result = manager.run("sleep 0.5")
    
    assert result.execution_time >= 0.4  # Allow some tolerance
    assert result.execution_time <= 2.0  # Should not be too long
    print("✓ test_execution_time_accuracy passed")


def test_concurrent_executions():
    """Test concurrent process executions."""
    manager = ProcessManager()
    results = []
    
    def run_cmd(cmd):
        result = manager.run(cmd)
        results.append(result)
    
    # Run multiple commands concurrently
    threads = []
    for i in range(3):
        t = threading.Thread(target=run_cmd, args=(f"echo {i}",))
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    
    assert len(results) == 3
    print("✓ test_concurrent_executions passed")


def test_kill_all():
    """Test kill_all method."""
    manager = ProcessManager()
    
    # Start a long-running process
    result = manager.run("sleep 10")
    
    # Kill all (should handle gracefully even if process completed)
    count = manager.kill_all()
    assert count >= 0
    print("✓ test_kill_all passed")


# =============================================================================
# Main Test Runner
# =============================================================================

def run_all_tests():
    """Run all tests and report results."""
    tests = [
        # ProcessResult tests
        test_process_result_creation,
        test_process_result_success,
        test_process_result_to_dict,
        test_process_result_str,
        # ProcessConfig tests
        test_process_config_defaults,
        test_process_config_custom,
        test_process_config_to_dict,
        # Enum tests
        test_process_priority_values,
        test_process_state_values,
        # ProcessManager tests
        test_process_manager_creation,
        test_process_manager_run_simple,
        test_process_manager_run_with_args,
        test_process_manager_run_shell,
        test_process_manager_run_timeout,
        test_process_manager_run_with_cwd,
        test_process_manager_run_with_env,
        test_process_manager_run_failing_command,
        test_process_manager_run_nonexistent_command,
        test_process_manager_get_result,
        test_process_manager_get_all_results,
        test_process_manager_is_running,
        test_process_manager_running_count,
        # ProcessUtils tests
        test_process_utils_run,
        test_process_utils_run_shell,
        test_process_utils_run_with_timeout,
        test_process_utils_exists_true,
        test_process_utils_exists_false,
        test_process_utils_which,
        test_process_utils_get_pid,
        test_process_utils_get_ppid,
        test_process_utils_get_cwd,
        test_process_utils_get_env,
        test_process_utils_set_env,
        test_process_utils_unset_env,
        test_process_utils_get_env_snapshot,
        test_process_utils_sleep,
        # Convenience functions
        test_run_function,
        test_run_shell_function,
        test_exists_function,
        test_which_function,
        test_get_pid_function,
        test_get_env_function,
        # WorkerPool tests
        test_worker_pool_creation,
        test_worker_pool_start_stop,
        test_worker_pool_map,
        test_worker_pool_apply,
        test_worker_pool_apply_async,
        test_worker_pool_map_async,
        test_worker_pool_get_results,
        test_worker_pool_context_manager,
        # ProcessInfo tests
        test_process_info_creation,
        test_process_info_to_dict,
        # Edge cases
        test_empty_command,
        test_very_long_output,
        test_unicode_output,
        test_multiline_output,
        test_stderr_capture,
        test_both_stdout_stderr,
        test_execution_time_accuracy,
        test_concurrent_executions,
        test_kill_all,
    ]
    
    passed = 0
    failed = 0
    errors = []
    
    print("=" * 60)
    print("AllToolkit - Python Process Utilities Test Suite")
    print("=" * 60)
    print()
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            failed += 1
            errors.append((test.__name__, str(e)))
            print(f"✗ {test.__name__} FAILED: {e}")
    
    print()
    print("=" * 60)
    print(f"Results: {passed} passed, {failed} failed, {len(tests)} total")
    print("=" * 60)
    
    if errors:
        print("\nFailed tests:")
        for name, error in errors:
            print(f"  - {name}: {error}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(run_all_tests())

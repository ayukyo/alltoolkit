"""
AllToolkit - Python Process Utilities Usage Examples

Demonstrates common use cases for the process_utils module.
Run individual examples or execute this file directly.
"""

import sys
import os
import time

# Add parent directory to path (go up one level from examples/)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    run,
    run_shell,
    run_background,
    exists,
    which,
    get_pid,
    get_env,
    set_env,
    ProcessManager,
    ProcessUtils,
    ProcessConfig,
    ProcessState,
    WorkerPool,
)


# =============================================================================
# Example 1: Basic Command Execution
# =============================================================================

def example_basic_execution():
    """Basic command execution example."""
    print("\n" + "=" * 60)
    print("Example 1: Basic Command Execution")
    print("=" * 60)
    
    # Simple echo command
    result = run("echo Hello from AllToolkit!")
    
    print(f"Command: echo Hello from AllToolkit!")
    print(f"Return code: {result.returncode}")
    print(f"Output: {result.stdout.strip()}")
    print(f"Execution time: {result.execution_time:.4f}s")
    print(f"Success: {result.success()}")


# =============================================================================
# Example 2: Shell Commands with Pipes
# =============================================================================

def example_shell_commands():
    """Shell commands with pipes and redirections."""
    print("\n" + "=" * 60)
    print("Example 2: Shell Commands with Pipes")
    print("=" * 60)
    
    # Count files
    result = run_shell("ls -1 | wc -l")
    print(f"Files in current directory: {result.stdout.strip()}")
    
    # Find Python files
    result = run_shell("find . -name '*.py' -type f | head -5")
    print(f"Python files (first 5):")
    for line in result.stdout.strip().split('\n'):
        if line:
            print(f"  - {line}")


# =============================================================================
# Example 3: Timeout Handling
# =============================================================================

def example_timeout():
    """Demonstrate timeout handling."""
    print("\n" + "=" * 60)
    print("Example 3: Timeout Handling")
    print("=" * 60)
    
    # Quick command (should succeed)
    result = run("sleep 0.5", timeout=2.0)
    print(f"Quick command (sleep 0.5s, timeout 2s):")
    print(f"  State: {result.state.value}")
    print(f"  Success: {result.success()}")
    
    # Slow command (should timeout)
    result = run("sleep 5", timeout=1.0)
    print(f"\nSlow command (sleep 5s, timeout 1s):")
    print(f"  State: {result.state.value}")
    print(f"  Success: {result.success()}")
    print(f"  Return code: {result.returncode}")


# =============================================================================
# Example 4: Working Directory and Environment
# =============================================================================

def example_cwd_and_env():
    """Demonstrate working directory and environment variables."""
    print("\n" + "=" * 60)
    print("Example 4: Working Directory and Environment")
    print("=" * 60)
    
    # Run with custom working directory
    config = ProcessConfig(cwd="/tmp")
    result = run("pwd", config)
    print(f"Working directory test:")
    print(f"  Output: {result.stdout.strip()}")
    
    # Run with custom environment
    config = ProcessConfig(
        env={"MY_CUSTOM_VAR": "custom_value"},
        shell=True,
    )
    result = run("echo $MY_CUSTOM_VAR", config)
    print(f"\nEnvironment variable test:")
    print(f"  Output: {result.stdout.strip()}")


# =============================================================================
# Example 5: Command Existence Check
# =============================================================================

def example_command_check():
    """Check if commands exist."""
    print("\n" + "=" * 60)
    print("Example 5: Command Existence Check")
    print("=" * 60)
    
    commands = ["python", "python3", "git", "node", "nonexistent_cmd"]
    
    for cmd in commands:
        if exists(cmd):
            path = which(cmd)
            print(f"  ✓ {cmd}: {path}")
        else:
            print(f"  ✗ {cmd}: not found")


# =============================================================================
# Example 6: Environment Variable Management
# =============================================================================

def example_env_management():
    """Manage environment variables."""
    print("\n" + "=" * 60)
    print("Example 6: Environment Variable Management")
    print("=" * 60)
    
    # Get existing variable
    home = get_env("HOME")
    print(f"HOME: {home}")
    
    # Get with default
    value = get_env("NONEXISTENT", "default_value")
    print(f"NONEXISTENT (with default): {value}")
    
    # Set and get
    set_env("MY_TEST_VAR", "test_value_123")
    value = get_env("MY_TEST_VAR")
    print(f"MY_TEST_VAR (after set): {value}")
    
    # Get snapshot
    snapshot = get_env_snapshot()
    print(f"\nTotal environment variables: {len(snapshot)}")
    
    # Cleanup
    os.environ.pop("MY_TEST_VAR", None)


# =============================================================================
# Example 7: Process Manager
# =============================================================================

def example_process_manager():
    """Use ProcessManager for multiple executions."""
    print("\n" + "=" * 60)
    print("Example 7: Process Manager")
    print("=" * 60)
    
    manager = ProcessManager()
    
    # Run multiple commands
    commands = ["echo one", "echo two", "echo three"]
    
    for cmd in commands:
        result = manager.run(cmd)
        print(f"  {cmd}: {result.stdout.strip()}")
    
    # Get all results
    results = manager.get_all_results()
    print(f"\nTotal results stored: {len(results)}")
    print(f"Running processes: {manager.get_running_count()}")


# =============================================================================
# Example 8: Worker Pool - Parallel Processing
# =============================================================================

def worker_square(x):
    """Worker function: calculate square."""
    return x * x


def worker_slow(x):
    """Worker function: slow operation."""
    time.sleep(0.1)
    return x * 2


def example_worker_pool():
    """Use WorkerPool for parallel processing."""
    print("\n" + "=" * 60)
    print("Example 8: Worker Pool - Parallel Processing")
    print("=" * 60)
    
    # Sequential processing (for comparison)
    print("Sequential processing...")
    start = time.time()
    sequential_results = [worker_square(x) for x in range(10)]
    sequential_time = time.time() - start
    print(f"  Time: {sequential_time:.4f}s")
    print(f"  Results: {sequential_results}")
    
    # Parallel processing
    print("\nParallel processing (4 workers)...")
    start = time.time()
    with WorkerPool(num_workers=4) as pool:
        parallel_results = pool.map(worker_square, range(10))
    parallel_time = time.time() - start
    print(f"  Time: {parallel_time:.4f}s")
    print(f"  Results: {parallel_results}")
    
    # Slow operations (parallel shows more benefit)
    print("\nSlow operations (sequential vs parallel)...")
    
    start = time.time()
    sequential_slow = [worker_slow(x) for x in range(10)]
    sequential_slow_time = time.time() - start
    print(f"  Sequential time: {sequential_slow_time:.4f}s")
    
    start = time.time()
    with WorkerPool(num_workers=4) as pool:
        parallel_slow = pool.map(worker_slow, range(10))
    parallel_slow_time = time.time() - start
    print(f"  Parallel time: {parallel_slow_time:.4f}s")
    print(f"  Speedup: {sequential_slow_time / parallel_slow_time:.2f}x")


# =============================================================================
# Example 9: Async Worker Pool
# =============================================================================

def example_async_worker_pool():
    """Use async worker pool with callbacks."""
    print("\n" + "=" * 60)
    print("Example 9: Async Worker Pool with Callbacks")
    print("=" * 60)
    
    def on_success(results):
        print(f"  Callback: Received {len(results)} results")
    
    def on_error(error):
        print(f"  Callback: Error - {error}")
    
    with WorkerPool(num_workers=2) as pool:
        # Async map with callbacks
        async_result = pool.map_async(
            worker_square,
            range(5),
            callback=on_success,
            error_callback=on_error,
        )
        
        print("  Task submitted, waiting for results...")
        results = async_result.get(timeout=10)
        print(f"  Final results: {results}")


# =============================================================================
# Example 10: Error Handling
# =============================================================================

def example_error_handling():
    """Demonstrate error handling."""
    print("\n" + "=" * 60)
    print("Example 10: Error Handling")
    print("=" * 60)
    
    # Nonexistent command
    result = run("nonexistent_command_xyz123")
    print(f"Nonexistent command:")
    print(f"  State: {result.state.value}")
    print(f"  Success: {result.success()}")
    print(f"  Error: {result.stderr[:100] if result.stderr else 'N/A'}")
    
    # Command that fails
    result = run("exit 1")
    print(f"\nCommand with exit code 1:")
    print(f"  Return code: {result.returncode}")
    print(f"  Success: {result.success()}")
    
    # Timeout
    result = run("sleep 10", timeout=0.5)
    print(f"\nTimed out command:")
    print(f"  State: {result.state.value}")
    print(f"  Success: {result.success()}")


# =============================================================================
# Example 11: Process Information
# =============================================================================

def example_process_info():
    """Get process information."""
    print("\n" + "=" * 60)
    print("Example 11: Process Information")
    print("=" * 60)
    
    print(f"Current PID: {get_pid()}")
    print(f"Parent PID: {get_ppid()}")
    print(f"Current directory: {get_cwd()}")


# =============================================================================
# Example 12: Background Process
# =============================================================================

def example_background_process():
    """Run background process."""
    print("\n" + "=" * 60)
    print("Example 12: Background Process")
    print("=" * 60)
    
    # Note: This is a simple example. In real usage, you might want
    # to redirect output to a file for long-running processes.
    pid = run_background("sleep 2")
    print(f"Started background process with PID: {pid}")
    print("Process will run independently...")
    
    # Wait a bit to show it's running
    time.sleep(0.5)
    print("Main program continues while background process runs...")


# =============================================================================
# Example 13: Real-world Use Case - Build Script
# =============================================================================

def example_build_script():
    """Simulate a build script."""
    print("\n" + "=" * 60)
    print("Example 13: Real-world Build Script Simulation")
    print("=" * 60)
    
    manager = ProcessManager()
    
    # Step 1: Check prerequisites
    print("\n[Step 1] Checking prerequisites...")
    for cmd in ["python", "git"]:
        if exists(cmd):
            print(f"  ✓ {cmd} found")
        else:
            print(f"  ✗ {cmd} not found")
    
    # Step 2: Get version info
    print("\n[Step 2] Getting version info...")
    result = run_shell("python --version")
    if result.success():
        print(f"  Python: {result.stdout.strip()}")
    
    # Step 3: Simulate build steps
    print("\n[Step 3] Running build steps...")
    build_steps = [
        ("echo 'Compiling...'", "Compile"),
        ("echo 'Linking...'", "Link"),
        ("echo 'Testing...'", "Test"),
        ("echo 'Packaging...'", "Package"),
    ]
    
    for cmd, name in build_steps:
        result = manager.run(cmd)
        status = "✓" if result.success() else "✗"
        print(f"  {status} {name}: {result.execution_time:.3f}s")
    
    # Step 4: Summary
    print("\n[Step 4] Build Summary")
    results = manager.get_all_results()
    successful = sum(1 for r in results.values() if r.success())
    print(f"  Total steps: {len(build_steps)}")
    print(f"  Successful: {successful}")
    print(f"  Failed: {len(build_steps) - successful}")


# =============================================================================
# Example 14: Parallel File Processing
# =============================================================================

def process_file(filepath):
    """Simulate file processing."""
    time.sleep(0.05)  # Simulate work
    return f"Processed: {filepath}"


def example_parallel_file_processing():
    """Process multiple files in parallel."""
    print("\n" + "=" * 60)
    print("Example 14: Parallel File Processing")
    print("=" * 60)
    
    # Simulate file list
    files = [f"file_{i}.txt" for i in range(20)]
    
    print(f"Processing {len(files)} files...")
    
    start = time.time()
    with WorkerPool(num_workers=4) as pool:
        results = pool.map(process_file, files)
    elapsed = time.time() - start
    
    print(f"Completed in {elapsed:.3f}s")
    print(f"First 5 results:")
    for result in results[:5]:
        print(f"  - {result}")


# =============================================================================
# Main - Run All Examples
# =============================================================================

def run_all_examples():
    """Run all examples."""
    print("\n" + "#" * 60)
    print("# AllToolkit - Python Process Utilities Examples")
    print("#" * 60)
    
    examples = [
        example_basic_execution,
        example_shell_commands,
        example_timeout,
        example_cwd_and_env,
        example_command_check,
        example_env_management,
        example_process_manager,
        example_worker_pool,
        example_async_worker_pool,
        example_error_handling,
        example_process_info,
        example_background_process,
        example_build_script,
        example_parallel_file_processing,
    ]
    
    for example in examples:
        try:
            example()
        except Exception as e:
            print(f"\n✗ Example {example.__name__} failed: {e}")
    
    print("\n" + "#" * 60)
    print("# All examples completed!")
    print("#" * 60 + "\n")


if __name__ == "__main__":
    run_all_examples()

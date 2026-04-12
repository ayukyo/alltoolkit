"""
AllToolkit - Python Process Utilities

A zero-dependency, production-ready process management module.
Supports process execution, management, monitoring, and inter-process communication.

Author: AllToolkit
License: MIT
"""

import subprocess
import os
import sys
import signal
import time
import threading
import multiprocessing
from typing import List, Dict, Tuple, Optional, Any, Callable, Union, TYPE_CHECKING
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict
import tempfile
import shutil
import json

if TYPE_CHECKING:
    from multiprocessing import AsyncResult


# =============================================================================
# Constants and Configuration
# =============================================================================

# Default timeout for process execution (seconds)
DEFAULT_TIMEOUT = 30.0

# Default buffer size for output streaming
DEFAULT_BUFFER_SIZE = 4096

# Process priority levels (Unix nice values)
class ProcessPriority(Enum):
    """Process priority levels."""
    VERY_HIGH = -20  # Highest priority (requires root)
    HIGH = -10
    ABOVE_NORMAL = -5
    NORMAL = 0
    BELOW_NORMAL = 5
    LOW = 10
    VERY_LOW = 19  # Lowest priority


# Process states
class ProcessState(Enum):
    """Process states."""
    RUNNING = "running"
    STOPPED = "stopped"
    COMPLETED = "completed"
    FAILED = "failed"
    TIMEOUT = "timeout"
    UNKNOWN = "unknown"


# =============================================================================
# Data Classes
# =============================================================================

@dataclass
class ProcessResult:
    """Result of a process execution."""
    returncode: int
    stdout: str
    stderr: str
    execution_time: float
    pid: Optional[int] = None
    command: str = ""
    state: ProcessState = ProcessState.COMPLETED
    
    def success(self) -> bool:
        """Check if process completed successfully."""
        return self.returncode == 0 and self.state == ProcessState.COMPLETED
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'returncode': self.returncode,
            'stdout': self.stdout,
            'stderr': self.stderr,
            'execution_time': self.execution_time,
            'pid': self.pid,
            'command': self.command,
            'state': self.state.value,
            'success': self.success(),
        }
    
    def __str__(self) -> str:
        return f"ProcessResult(code={self.returncode}, time={self.execution_time:.3f}s, state={self.state.value})"


@dataclass
class ProcessInfo:
    """Information about a running process."""
    pid: int
    name: str
    cmdline: List[str]
    status: str
    ppid: int
    username: str
    cpu_percent: float = 0.0
    memory_percent: float = 0.0
    num_threads: int = 1
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'pid': self.pid,
            'name': self.name,
            'cmdline': self.cmdline,
            'status': self.status,
            'ppid': self.ppid,
            'username': self.username,
            'cpu_percent': self.cpu_percent,
            'memory_percent': self.memory_percent,
            'num_threads': self.num_threads,
        }


@dataclass
class ProcessConfig:
    """Configuration for process execution."""
    timeout: float = DEFAULT_TIMEOUT
    cwd: Optional[str] = None
    env: Optional[Dict[str, str]] = None
    shell: bool = False
    capture_output: bool = True
    universal_newlines: bool = True  # Use universal_newlines for Python 3.6 compatibility
    encoding: str = 'utf-8'
    errors: str = 'strict'
    stdin: Optional[int] = subprocess.PIPE
    stdout: Optional[int] = subprocess.PIPE
    stderr: Optional[int] = subprocess.PIPE
    preexec_fn: Optional[Callable] = None
    priority: ProcessPriority = ProcessPriority.NORMAL
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'timeout': self.timeout,
            'cwd': self.cwd,
            'env': self.env,
            'shell': self.shell,
            'capture_output': self.capture_output,
            'universal_newlines': self.universal_newlines,
            'encoding': self.encoding,
            'errors': self.errors,
            'priority': self.priority.value,
        }


# =============================================================================
# Process Manager Class
# =============================================================================

class ProcessManager:
    """
    Manages process execution, monitoring, and lifecycle.
    
    Features:
    - Execute commands with timeout
    - Stream output in real-time
    - Manage process groups
    - Graceful shutdown
    - Resource monitoring
    """
    
    def __init__(self, default_config: Optional[ProcessConfig] = None):
        """Initialize process manager."""
        self.default_config = default_config or ProcessConfig()
        self._processes: Dict[int, subprocess.Popen] = {}
        self._results: Dict[int, ProcessResult] = {}
        self._lock = threading.Lock()
    
    def run(
        self,
        command: Union[str, List[str]],
        config: Optional[ProcessConfig] = None,
        callback: Optional[Callable[[str], None]] = None
    ) -> ProcessResult:
        """
        Execute a command and return the result.
        
        Args:
            command: Command to execute (string or list of args)
            config: Execution configuration
            callback: Optional callback for streaming output
            
        Returns:
            ProcessResult with execution details
        """
        cfg = config or self.default_config
        start_time = time.time()
        
        # Prepare command
        if isinstance(command, str) and not cfg.shell:
            cmd_list = command.split()
        else:
            cmd_list = command if isinstance(command, list) else [command]
        
        cmd_str = command if isinstance(command, str) else ' '.join(command)
        
        try:
            # Create subprocess
            process = subprocess.Popen(
                cmd_list,
                stdout=cfg.stdout,
                stderr=cfg.stderr,
                stdin=cfg.stdin,
                shell=cfg.shell,
                cwd=cfg.cwd,
                env=cfg.env,
                universal_newlines=cfg.universal_newlines,
                preexec_fn=cfg.preexec_fn,
            )
            
            pid = process.pid
            with self._lock:
                self._processes[pid] = process
            
            # Wait for completion with timeout
            try:
                stdout, stderr = process.communicate(timeout=cfg.timeout)
                state = ProcessState.COMPLETED
                returncode = process.returncode or 0
            except subprocess.TimeoutExpired:
                process.kill()
                stdout, stderr = process.communicate()
                state = ProcessState.TIMEOUT
                returncode = -9
            
            execution_time = time.time() - start_time
            
            # Create result
            result = ProcessResult(
                returncode=returncode,
                stdout=stdout or '',
                stderr=stderr or '',
                execution_time=execution_time,
                pid=pid,
                command=cmd_str,
                state=state,
            )
            
            with self._lock:
                self._results[pid] = result
                if pid in self._processes:
                    del self._processes[pid]
            
            return result
            
        except Exception as e:
            execution_time = time.time() - start_time
            return ProcessResult(
                returncode=-1,
                stdout='',
                stderr=str(e),
                execution_time=execution_time,
                command=cmd_str,
                state=ProcessState.FAILED,
            )
    
    def run_streaming(
        self,
        command: Union[str, List[str]],
        config: Optional[ProcessConfig] = None,
        stdout_callback: Optional[Callable[[str], None]] = None,
        stderr_callback: Optional[Callable[[str], None]] = None,
    ) -> ProcessResult:
        """
        Execute a command with real-time output streaming.
        
        Args:
            command: Command to execute
            config: Execution configuration
            stdout_callback: Callback for stdout lines
            stderr_callback: Callback for stderr lines
            
        Returns:
            ProcessResult with execution details
        """
        cfg = config or self.default_config
        cfg.capture_output = True
        start_time = time.time()
        
        # Prepare command
        if isinstance(command, str) and not cfg.shell:
            cmd_list = command.split()
        else:
            cmd_list = command if isinstance(command, list) else [command]
        
        cmd_str = command if isinstance(command, str) else ' '.join(command)
        
        stdout_lines = []
        stderr_lines = []
        
        try:
            process = subprocess.Popen(
                cmd_list,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=cfg.stdin,
                shell=cfg.shell,
                cwd=cfg.cwd,
                env=cfg.env,
                universal_newlines=cfg.universal_newlines,
            )
            
            pid = process.pid
            with self._lock:
                self._processes[pid] = process
            
            # Stream output
            def read_stream(stream, callback, lines_list):
                for line in iter(stream.readline, ''):
                    lines_list.append(line)
                    if callback:
                        callback(line)
                stream.close()
            
            # Use threads for non-blocking read
            stdout_thread = threading.Thread(
                target=read_stream,
                args=(process.stdout, stdout_callback, stdout_lines)
            )
            stderr_thread = threading.Thread(
                target=read_stream,
                args=(process.stderr, stderr_callback, stderr_lines)
            )
            
            stdout_thread.start()
            stderr_thread.start()
            
            # Wait for process with timeout
            try:
                process.wait(timeout=cfg.timeout)
                state = ProcessState.COMPLETED
                returncode = process.returncode or 0
            except subprocess.TimeoutExpired:
                process.kill()
                state = ProcessState.TIMEOUT
                returncode = -9
            
            # Wait for threads
            stdout_thread.join(timeout=5)
            stderr_thread.join(timeout=5)
            
            execution_time = time.time() - start_time
            
            result = ProcessResult(
                returncode=returncode,
                stdout=''.join(stdout_lines),
                stderr=''.join(stderr_lines),
                execution_time=execution_time,
                pid=pid,
                command=cmd_str,
                state=state,
            )
            
            with self._lock:
                self._results[pid] = result
                if pid in self._processes:
                    del self._processes[pid]
            
            return result
            
        except Exception as e:
            execution_time = time.time() - start_time
            return ProcessResult(
                returncode=-1,
                stdout='',
                stderr=str(e),
                execution_time=execution_time,
                command=cmd_str,
                state=ProcessState.FAILED,
            )
    
    def kill(self, pid: int, signal_num: int = signal.SIGTERM) -> bool:
        """
        Kill a process by PID.
        
        Args:
            pid: Process ID
            signal_num: Signal to send (default: SIGTERM)
            
        Returns:
            True if successfully killed
        """
        with self._lock:
            if pid in self._processes:
                process = self._processes[pid]
                try:
                    process.send_signal(signal_num)
                    process.wait(timeout=5)
                    del self._processes[pid]
                    return True
                except Exception:
                    try:
                        process.kill()
                        process.wait(timeout=5)
                        del self._processes[pid]
                        return True
                    except Exception:
                        return False
        return False
    
    def kill_all(self, signal_num: int = signal.SIGTERM) -> int:
        """
        Kill all managed processes.
        
        Args:
            signal_num: Signal to send
            
        Returns:
            Number of processes killed
        """
        count = 0
        with self._lock:
            pids = list(self._processes.keys())
        
        for pid in pids:
            if self.kill(pid, signal_num):
                count += 1
        
        return count
    
    def get_result(self, pid: int) -> Optional[ProcessResult]:
        """Get result for a process by PID."""
        with self._lock:
            return self._results.get(pid)
    
    def get_all_results(self) -> Dict[int, ProcessResult]:
        """Get all process results."""
        with self._lock:
            return dict(self._results)
    
    def is_running(self, pid: int) -> bool:
        """Check if a process is still running."""
        with self._lock:
            return pid in self._processes
    
    def get_running_count(self) -> int:
        """Get number of running processes."""
        with self._lock:
            return len(self._processes)


# =============================================================================
# Process Utilities Class
# =============================================================================

class ProcessUtils:
    """
    Static process utility functions.
    
    Provides common process operations without needing to instantiate
    a ProcessManager.
    """
    
    _manager: Optional[ProcessManager] = None
    
    @classmethod
    def get_manager(cls) -> ProcessManager:
        """Get or create the default process manager."""
        if cls._manager is None:
            cls._manager = ProcessManager()
        return cls._manager
    
    @classmethod
    def run(
        cls,
        command: Union[str, List[str]],
        timeout: float = DEFAULT_TIMEOUT,
        shell: bool = False,
        cwd: Optional[str] = None,
        env: Optional[Dict[str, str]] = None,
    ) -> ProcessResult:
        """
        Execute a command with simple interface.
        
        Args:
            command: Command to execute
            timeout: Timeout in seconds
            shell: Run in shell
            cwd: Working directory
            env: Environment variables
            
        Returns:
            ProcessResult
        """
        config = ProcessConfig(
            timeout=timeout,
            shell=shell,
            cwd=cwd,
            env=env,
        )
        return cls.get_manager().run(command, config)
    
    @classmethod
    def run_shell(cls, command: str, **kwargs) -> ProcessResult:
        """Execute a shell command."""
        return cls.run(command, shell=True, **kwargs)
    
    @classmethod
    def run_background(
        cls,
        command: Union[str, List[str]],
        shell: bool = False,
    ) -> int:
        """
        Run a command in background.
        
        Args:
            command: Command to execute
            shell: Run in shell
            
        Returns:
            Process PID
        """
        if isinstance(command, str) and not shell:
            cmd_list = command.split()
        else:
            cmd_list = command if isinstance(command, list) else [command]
        
        process = subprocess.Popen(
            cmd_list,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            shell=shell,
            start_new_session=True,
        )
        return process.pid
    
    @classmethod
    def exists(cls, command: str) -> bool:
        """Check if a command exists in PATH."""
        return shutil.which(command) is not None
    
    @classmethod
    def which(cls, command: str) -> Optional[str]:
        """Find full path of a command."""
        return shutil.which(command)
    
    @classmethod
    def get_pid(cls) -> int:
        """Get current process PID."""
        return os.getpid()
    
    @classmethod
    def get_ppid(cls) -> int:
        """Get parent process PID."""
        return os.getppid()
    
    @classmethod
    def get_cwd(cls) -> str:
        """Get current working directory."""
        return os.getcwd()
    
    @classmethod
    def get_env(cls, name: str, default: Optional[str] = None) -> Optional[str]:
        """Get environment variable."""
        return os.environ.get(name, default)
    
    @classmethod
    def set_env(cls, name: str, value: str) -> None:
        """Set environment variable."""
        os.environ[name] = value
    
    @classmethod
    def unset_env(cls, name: str) -> None:
        """Remove environment variable."""
        if name in os.environ:
            del os.environ[name]
    
    @classmethod
    def get_env_snapshot(cls) -> Dict[str, str]:
        """Get snapshot of all environment variables."""
        return dict(os.environ)
    
    @classmethod
    def sleep(cls, seconds: float) -> None:
        """Sleep for specified seconds."""
        time.sleep(seconds)
    
    @classmethod
    def exit(cls, code: int = 0) -> None:
        """Exit the current process."""
        sys.exit(code)
    
    @classmethod
    def abort(cls) -> None:
        """Abort the current process."""
        os.abort()


# =============================================================================
# Worker Pool
# =============================================================================

class WorkerPool:
    """
    Pool of worker processes for parallel execution.
    
    Features:
    - Configurable number of workers
    - Task queue with results
    - Graceful shutdown
    - Error handling
    """
    
    def __init__(self, num_workers: int = 4):
        """
        Initialize worker pool.
        
        Args:
            num_workers: Number of worker processes
        """
        self.num_workers = num_workers
        self._pool: Optional[multiprocessing.Pool] = None
        self._results: List[Any] = []
        self._errors: List[Exception] = []
    
    def start(self) -> None:
        """Start the worker pool."""
        if self._pool is None:
            self._pool = multiprocessing.Pool(processes=self.num_workers)
    
    def stop(self, graceful: bool = True) -> None:
        """
        Stop the worker pool.
        
        Args:
            graceful: Wait for tasks to complete
        """
        if self._pool is not None:
            if graceful:
                self._pool.close()
                self._pool.join()
            else:
                self._pool.terminate()
            self._pool = None
    
    def map(
        self,
        func: Callable,
        iterable: List[Any],
        chunksize: int = 1,
    ) -> List[Any]:
        """
        Map a function over an iterable using worker processes.
        
        Args:
            func: Function to apply
            iterable: Input data
            chunksize: Size of chunks for each worker
            
        Returns:
            List of results
        """
        if self._pool is None:
            self.start()
        
        try:
            results = self._pool.map(func, iterable, chunksize=chunksize)
            self._results.extend(results)
            return results
        except Exception as e:
            self._errors.append(e)
            raise
    
    def map_async(
        self,
        func: Callable,
        iterable: List[Any],
        callback: Optional[Callable] = None,
        error_callback: Optional[Callable] = None,
    ) -> 'AsyncResult':
        """
        Async map with callbacks.
        
        Args:
            func: Function to apply
            iterable: Input data
            callback: Success callback
            error_callback: Error callback
            
        Returns:
            AsyncResult object
        """
        if self._pool is None:
            self.start()
        
        return self._pool.map_async(func, iterable, callback=callback, error_callback=error_callback)
    
    def apply(
        self,
        func: Callable,
        args: Tuple = (),
        kwds: Optional[Dict] = None,
    ) -> Any:
        """
        Apply a function with arguments.
        
        Args:
            func: Function to apply
            args: Positional arguments
            kwds: Keyword arguments
            
        Returns:
            Function result
        """
        if self._pool is None:
            self.start()
        
        return self._pool.apply(func, args=args, kwds=kwds or {})
    
    def apply_async(
        self,
        func: Callable,
        args: Tuple = (),
        kwds: Optional[Dict] = None,
        callback: Optional[Callable] = None,
        error_callback: Optional[Callable] = None,
    ) -> 'AsyncResult':
        """
        Async apply with callbacks.
        
        Args:
            func: Function to apply
            args: Positional arguments
            kwds: Keyword arguments
            callback: Success callback
            error_callback: Error callback
            
        Returns:
            AsyncResult object
        """
        if self._pool is None:
            self.start()
        
        return self._pool.apply_async(
            func, args=args, kwds=kwds or {},
            callback=callback, error_callback=error_callback
        )
    
    def get_results(self) -> List[Any]:
        """Get all collected results."""
        return list(self._results)
    
    def get_errors(self) -> List[Exception]:
        """Get all collected errors."""
        return list(self._errors)
    
    def __enter__(self):
        """Context manager entry."""
        self.start()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.stop(graceful=exc_type is None)
        return False


# =============================================================================
# Convenience Functions
# =============================================================================

def run(
    command: Union[str, List[str]],
    timeout: float = DEFAULT_TIMEOUT,
    **kwargs
) -> ProcessResult:
    """Execute a command and return result."""
    return ProcessUtils.run(command, timeout=timeout, **kwargs)


def run_shell(command: str, **kwargs) -> ProcessResult:
    """Execute a shell command."""
    return ProcessUtils.run_shell(command, **kwargs)


def run_background(command: Union[str, List[str]], shell: bool = False) -> int:
    """Run a command in background, return PID."""
    return ProcessUtils.run_background(command, shell=shell)


def exists(command: str) -> bool:
    """Check if command exists."""
    return ProcessUtils.exists(command)


def which(command: str) -> Optional[str]:
    """Find command path."""
    return ProcessUtils.which(command)


def get_pid() -> int:
    """Get current PID."""
    return ProcessUtils.get_pid()


def get_env(name: str, default: Optional[str] = None) -> Optional[str]:
    """Get environment variable."""
    return ProcessUtils.get_env(name, default)


def set_env(name: str, value: str) -> None:
    """Set environment variable."""
    ProcessUtils.set_env(name, value)


def unset_env(name: str) -> None:
    """Remove environment variable."""
    ProcessUtils.unset_env(name)


def get_env_snapshot() -> Dict[str, str]:
    """Get snapshot of all environment variables."""
    return ProcessUtils.get_env_snapshot()


# =============================================================================
# Module Exports
# =============================================================================

__all__ = [
    # Classes
    'ProcessManager',
    'ProcessUtils',
    'WorkerPool',
    'ProcessResult',
    'ProcessInfo',
    'ProcessConfig',
    # Enums
    'ProcessPriority',
    'ProcessState',
    # Functions
    'run',
    'run_shell',
    'run_background',
    'exists',
    'which',
    'get_pid',
    'get_env',
    'set_env',
    'unset_env',
    'get_env_snapshot',
    # Constants
    'DEFAULT_TIMEOUT',
    'DEFAULT_BUFFER_SIZE',
]

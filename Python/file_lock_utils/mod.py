"""
file_lock_utils - Cross-process file locking utilities

Provides file locking mechanisms for safe concurrent file access across processes.
Supports exclusive locks, shared locks, non-blocking attempts, and timeout handling.

No external dependencies - uses only Python stdlib (fcntl on Unix, msvcrt on Windows).
"""

import os
import time
import errno
import threading
from typing import Optional, Union, ContextManager
from contextlib import contextmanager


class FileLockError(Exception):
    """Base exception for file lock errors."""
    pass


class LockTimeoutError(FileLockError):
    """Raised when lock acquisition times out."""
    pass


class LockNotHeldError(FileLockError):
    """Raised when trying to release a lock that isn't held."""
    pass


class FileLock:
    """
    A cross-process file lock using OS-level advisory locks.
    
    Features:
    - Exclusive (write) and shared (read) locks
    - Non-blocking attempts
    - Timeout support
    - Context manager interface
    - Cross-platform (Unix via fcntl, Windows via msvcrt)
    
    Example:
        with FileLock('/tmp/myapp.lock'):
            # Critical section - exclusive access
            process_file()
        
        with FileLock('/tmp/shared.lock', shared=True):
            # Shared access - multiple readers allowed
            read_file()
    """
    
    # Process-wide registry of file locks for thread safety
    _registry_lock = threading.Lock()
    _registry: dict = {}  # lockfile -> {"lock": threading.Lock, "count": int}
    
    def __init__(
        self,
        lockfile: str,
        timeout: Optional[float] = None,
        shared: bool = False,
        blocking: bool = True
    ):
        """
        Initialize file lock.
        
        Args:
            lockfile: Path to the lock file (will be created if needed)
            timeout: Maximum seconds to wait for lock (None = wait forever)
            shared: True for shared/read lock, False for exclusive/write lock
            blocking: If False, raise LockTimeoutError immediately if lock unavailable
        """
        self.lockfile = lockfile
        self.timeout = timeout
        self.shared = shared
        self.blocking = blocking
        self._fd: Optional[int] = None
        self._locked = False
        self._instance_lock = threading.Lock()
        
        # Get or create process-wide lock for this lockfile
        with FileLock._registry_lock:
            if lockfile not in FileLock._registry:
                FileLock._registry[lockfile] = {"lock": threading.Lock(), "count": 0}
            self._process_lock = FileLock._registry[lockfile]["lock"]
    
    def _get_lock_flags(self) -> int:
        """Get platform-specific lock flags."""
        if os.name == 'nt':  # Windows
            import msvcrt
            if self.shared:
                return msvcrt.LK_NBLCK  # Will use LOCK_SH equivalent
            return msvcrt.LK_NBLCK
        else:  # Unix
            import fcntl
            flags = fcntl.LOCK_SH if self.shared else fcntl.LOCK_EX
            if not self.blocking:
                flags |= fcntl.LOCK_NB
            return flags
    
    def acquire(self, timeout: Optional[float] = None) -> bool:
        """
        Acquire the lock.
        
        Args:
            timeout: Override instance timeout (None = use instance timeout)
            
        Returns:
            True if lock acquired
            
        Raises:
            LockTimeoutError: If timeout expires or non-blocking fails
        """
        timeout = timeout if timeout is not None else self.timeout
        
        with self._instance_lock:
            if self._locked:
                return True
        
        # Use process-wide lock for thread safety across threads in same process
        # This ensures only one thread in this process holds the lock
        if self.blocking:
            process_timeout = timeout if timeout is not None else -1
            if not self._process_lock.acquire(blocking=True, timeout=process_timeout):
                raise LockTimeoutError(f"Could not acquire process lock within {timeout} seconds")
        else:
            if not self._process_lock.acquire(blocking=False):
                raise LockTimeoutError("Lock not available")
        
        try:
            with self._instance_lock:
                if self._locked:
                    return True
                
                # Ensure lock file directory exists
                lockdir = os.path.dirname(self.lockfile)
                if lockdir and not os.path.exists(lockdir):
                    os.makedirs(lockdir, exist_ok=True)
                
                # Open lock file
                fd = os.open(self.lockfile, os.O_RDWR | os.O_CREAT, 0o644)
                
                try:
                    if os.name == 'nt':  # Windows
                        self._acquire_windows(fd, timeout)
                    else:  # Unix
                        self._acquire_unix(fd, timeout)
                    
                    self._fd = fd
                    self._locked = True
                    return True
                    
                except Exception:
                    os.close(fd)
                    self._process_lock.release()
                    raise
        except Exception:
            self._process_lock.release()
            raise
    
    def _acquire_unix(self, fd: int, timeout: Optional[float]) -> None:
        """Acquire lock on Unix using fcntl."""
        import fcntl
        
        flags = fcntl.LOCK_SH if self.shared else fcntl.LOCK_EX
        
        if self.blocking and timeout is not None:
            # Polling with timeout
            start = time.monotonic()
            while True:
                try:
                    fcntl.flock(fd, flags | fcntl.LOCK_NB)
                    return
                except IOError as e:
                    if e.errno not in (errno.EAGAIN, errno.EWOULDBLOCK):
                        raise
                    elapsed = time.monotonic() - start
                    if elapsed >= timeout:
                        raise LockTimeoutError(
                            f"Could not acquire lock within {timeout} seconds"
                        )
                    time.sleep(min(0.05, timeout - elapsed))
        else:
            try:
                fcntl.flock(fd, flags if self.blocking else flags | fcntl.LOCK_NB)
            except IOError as e:
                if e.errno in (errno.EAGAIN, errno.EWOULDBLOCK):
                    raise LockTimeoutError("Lock not available")
                raise
    
    def _acquire_windows(self, fd: int, timeout: Optional[float]) -> None:
        """Acquire lock on Windows using msvcrt."""
        import msvcrt
        
        if self.blocking and timeout is not None:
            start = time.monotonic()
            while True:
                try:
                    # Windows doesn't have shared locks in the same way
                    msvcrt.locking(fd, msvcrt.LK_NBLCK, 1)
                    return
                except OSError:
                    elapsed = time.monotonic() - start
                    if elapsed >= timeout:
                        raise LockTimeoutError(
                            f"Could not acquire lock within {timeout} seconds"
                        )
                    time.sleep(min(0.05, timeout - elapsed))
        elif self.blocking:
            # Blocking without timeout
            try:
                msvcrt.locking(fd, msvcrt.LK_LOCK, 1)
            except OSError:
                raise LockTimeoutError("Lock not available")
        else:
            # Non-blocking
            try:
                msvcrt.locking(fd, msvcrt.LK_NBLCK, 1)
            except OSError:
                raise LockTimeoutError("Lock not available")
    
    def release(self) -> None:
        """Release the lock."""
        with self._instance_lock:
            if not self._locked:
                raise LockNotHeldError("Lock not held by this instance")
            
            if self._fd is None:
                raise LockNotHeldError("Lock file descriptor is None")
            
            try:
                if os.name == 'nt':  # Windows
                    import msvcrt
                    msvcrt.locking(self._fd, msvcrt.LK_UNLCK, 1)
                else:  # Unix
                    import fcntl
                    fcntl.flock(self._fd, fcntl.LOCK_UN)
            finally:
                os.close(self._fd)
                self._fd = None
                self._locked = False
        
        # Release process-wide lock
        self._process_lock.release()
    
    def __enter__(self) -> 'FileLock':
        self.acquire()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.release()
        return None
    
    @property
    def is_locked(self) -> bool:
        """Check if lock is currently held."""
        return self._locked


class SharedFileLock(FileLock):
    """Convenience class for shared (read) locks."""
    
    def __init__(self, lockfile: str, timeout: Optional[float] = None):
        super().__init__(lockfile, timeout=timeout, shared=True)


class ExclusiveFileLock(FileLock):
    """Convenience class for exclusive (write) locks."""
    
    def __init__(self, lockfile: str, timeout: Optional[float] = None):
        super().__init__(lockfile, timeout=timeout, shared=False)


@contextmanager
def file_lock(
    lockfile: str,
    timeout: Optional[float] = None,
    shared: bool = False,
    blocking: bool = True
):
    """
    Context manager for file locking.
    
    Args:
        lockfile: Path to the lock file
        timeout: Maximum seconds to wait (None = wait forever)
        shared: True for shared lock, False for exclusive
        blocking: If False, raise immediately if lock unavailable
        
    Yields:
        FileLock instance
        
    Example:
        with file_lock('/tmp/myapp.lock', timeout=5):
            process_file()
    """
    lock = FileLock(lockfile, timeout=timeout, shared=shared, blocking=blocking)
    lock.acquire()
    try:
        yield lock
    finally:
        lock.release()


def try_lock(lockfile: str, shared: bool = False) -> bool:
    """
    Non-blocking attempt to acquire a lock.
    
    Args:
        lockfile: Path to the lock file
        shared: True for shared lock, False for exclusive
        
    Returns:
        True if lock was available (not held), False if unavailable
        
    Note:
        This function attempts to acquire and immediately release the lock
        to test if it's available. It does NOT hold the lock.
        
    Example:
        if try_lock('/tmp/myapp.lock'):
            with file_lock('/tmp/myapp.lock'):
                process_file()
    """
    lock = FileLock(lockfile, shared=shared, blocking=False)
    try:
        lock.acquire()
        lock.release()  # Immediately release - we just wanted to test availability
        return True
    except LockTimeoutError:
        return False


def is_locked(lockfile: str) -> bool:
    """
    Check if a lock file is currently locked by another process.
    
    Args:
        lockfile: Path to the lock file
        
    Returns:
        True if locked by another process, False if available
        
    Note:
        This attempts to acquire a shared lock non-blocking,
        so it may return False positives on systems without
        proper advisory locking.
    """
    lock = FileLock(lockfile, shared=True, blocking=False)
    try:
        lock.acquire()
        lock.release()
        return False
    except LockTimeoutError:
        return True


def with_lock(
    lockfile: str,
    func,
    *args,
    timeout: Optional[float] = None,
    shared: bool = False,
    **kwargs
):
    """
    Execute a function with a file lock.
    
    Args:
        lockfile: Path to the lock file
        func: Function to execute
        *args: Arguments for function
        timeout: Lock acquisition timeout
        shared: True for shared lock
        **kwargs: Keyword arguments for function
        
    Returns:
        Result of function call
        
    Example:
        result = with_lock('/tmp/myapp.lock', process_data, data, timeout=10)
    """
    with file_lock(lockfile, timeout=timeout, shared=shared):
        return func(*args, **kwargs)


def create_lock_file(lockfile: str, content: Optional[str] = None) -> None:
    """
    Create a lock file with optional content (e.g., PID).
    
    Args:
        lockfile: Path to the lock file
        content: Optional content to write (default: PID)
        
    Example:
        create_lock_file('/tmp/myapp.lock', 'PID: 12345')
    """
    lockdir = os.path.dirname(lockfile)
    if lockdir and not os.path.exists(lockdir):
        os.makedirs(lockdir, exist_ok=True)
    
    if content is None:
        content = str(os.getpid())
    
    with open(lockfile, 'w') as f:
        f.write(content)


def read_lock_file(lockfile: str) -> Optional[str]:
    """
    Read content from a lock file.
    
    Args:
        lockfile: Path to the lock file
        
    Returns:
        Content of lock file, or None if doesn't exist
        
    Example:
        pid = read_lock_file('/tmp/myapp.lock')
    """
    try:
        with open(lockfile, 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        return None


def remove_lock_file(lockfile: str) -> bool:
    """
    Remove a lock file if it exists.
    
    Warning: This does NOT release the lock. Use release() instead.
    This is for cleanup of stale lock files.
    
    Args:
        lockfile: Path to the lock file
        
    Returns:
        True if file was removed, False if it didn't exist
        
    Example:
        if old_pid_no_longer_running:
            remove_lock_file('/tmp/myapp.lock')
    """
    try:
        os.remove(lockfile)
        return True
    except FileNotFoundError:
        return False


class RLock:
    """
    Reentrant file lock - allows the same process/thread to acquire
    the lock multiple times without deadlock.
    
    Note: Reentrancy is tracked in-memory, so it only works within
    the same Python process.
    
    Example:
        lock = RLock('/tmp/myapp.lock')
        with lock:
            with lock:  # Same thread can re-acquire
                process_file()
    """
    
    def __init__(self, lockfile: str, timeout: Optional[float] = None):
        self.lockfile = lockfile
        self.timeout = timeout
        self._lock = threading.RLock()
        self._file_lock: Optional[FileLock] = None
        self._count = 0
    
    def acquire(self, timeout: Optional[float] = None) -> bool:
        timeout = timeout if timeout is not None else self.timeout
        
        if self._lock.acquire():
            try:
                if self._count == 0:
                    self._file_lock = FileLock(self.lockfile, timeout=timeout)
                    self._file_lock.acquire()
                self._count += 1
                return True
            except Exception:
                self._lock.release()
                raise
        return False
    
    def release(self) -> None:
        self._count -= 1
        if self._count == 0 and self._file_lock:
            self._file_lock.release()
            self._file_lock = None
        self._lock.release()
    
    def __enter__(self) -> 'RLock':
        self.acquire()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.release()
        return None


# Export public API
__all__ = [
    'FileLock',
    'FileLockError',
    'LockTimeoutError',
    'LockNotHeldError',
    'SharedFileLock',
    'ExclusiveFileLock',
    'file_lock',
    'try_lock',
    'is_locked',
    'with_lock',
    'create_lock_file',
    'read_lock_file',
    'remove_lock_file',
    'RLock',
]
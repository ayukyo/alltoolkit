"""
file_lock_utils Examples - Usage demonstrations

Shows how to use file locking for cross-process synchronization.
"""

import os
import sys
import time
import tempfile

# Add the parent directory (where file_lock_utils folder is) for imports
parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, parent_dir)

from file_lock_utils.mod import (
    FileLock,
    SharedFileLock,
    ExclusiveFileLock,
    file_lock,
    try_lock,
    is_locked,
    with_lock,
    create_lock_file,
    read_lock_file,
    remove_lock_file,
    RLock,
    LockTimeoutError,
)


def example_basic_usage():
    """Basic file lock usage."""
    print("\n=== Basic Usage ===")
    
    lockfile = '/tmp/demo_basic.lock'
    
    # Simple lock/unlock
    lock = FileLock(lockfile)
    lock.acquire()
    print(f"Lock acquired on {lockfile}")
    print(f"Is locked: {lock.is_locked}")
    lock.release()
    print("Lock released")
    
    # Context manager
    print("\nUsing context manager:")
    with FileLock(lockfile):
        print("Inside locked section - exclusive access")
    print("Exited locked section")


def example_timeout():
    """Timeout handling."""
    print("\n=== Timeout Handling ===")
    
    lockfile = '/tmp/demo_timeout.lock'
    
    # First lock
    lock1 = FileLock(lockfile)
    lock1.acquire()
    print("First lock acquired")
    
    # Try to get second lock with timeout
    lock2 = FileLock(lockfile, timeout=2.0)
    print("Attempting second lock with 2s timeout...")
    
    try:
        lock2.acquire()
    except LockTimeoutError as e:
        print(f"Timeout: {e}")
    
    lock1.release()
    print("First lock released")
    
    # Now can acquire
    lock2.acquire()
    print("Second lock acquired (after first released)")
    lock2.release()


def example_non_blocking():
    """Non-blocking lock attempt."""
    print("\n=== Non-blocking Lock ===")
    
    lockfile = '/tmp/demo_nonblock.lock'
    
    # First lock
    lock1 = FileLock(lockfile)
    lock1.acquire()
    print("Lock 1 acquired")
    
    # Non-blocking attempt
    lock2 = FileLock(lockfile, blocking=False)
    print("Attempting non-blocking acquire...")
    
    if try_lock(lockfile):
        print("Lock available")
    else:
        print("Lock NOT available (held by another)")
    
    lock1.release()
    print("Lock 1 released")
    
    # Now try again
    if try_lock(lockfile):
        print("Lock now available!")


def example_shared_exclusive():
    """Shared vs exclusive locks."""
    print("\n=== Shared vs Exclusive Locks ===")
    
    lockfile = '/tmp/demo_shared.lock'
    
    # Exclusive lock
    print("Exclusive lock:")
    with ExclusiveFileLock(lockfile):
        print("Only one process can access")
        print("No other locks can be held")
    
    # Shared locks
    print("\nShared locks (multiple readers):")
    lock1 = SharedFileLock(lockfile)
    lock2 = SharedFileLock(lockfile)
    
    lock1.acquire()
    print("First shared lock acquired")
    
    lock2.acquire()
    print("Second shared lock acquired (allowed!)")
    print("Both can read concurrently")
    
    lock1.release()
    lock2.release()
    print("Both shared locks released")


def example_reentrant():
    """Reentrant lock (RLock)."""
    print("\n=== Reentrant Lock (RLock) ===")
    
    lockfile = '/tmp/demo_rlock.lock'
    
    lock = RLock(lockfile)
    
    with lock:
        print("First level acquired")
        
        with lock:
            print("Second level - same thread can re-acquire!")
            
            with lock:
                print("Third level - nested safely")
    
    print("All levels released")


def example_process_sync():
    """Cross-process synchronization pattern."""
    print("\n=== Cross-process Synchronization ===")
    
    lockfile = '/tmp/demo_process.lock'
    datafile = '/tmp/demo_data.txt'
    
    # Write PID to lock file for debugging
    create_lock_file(lockfile, f"PID: {os.getpid()}, Time: {time.time()}")
    print(f"Lock file created with PID: {os.getpid()}")
    
    # Read lock info
    info = read_lock_file(lockfile)
    print(f"Lock file content: {info}")
    
    # Use lock for safe file access
    with ExclusiveFileLock(lockfile):
        print("Writing to shared data file...")
        with open(datafile, 'w') as f:
            f.write(f"Data from PID {os.getpid()}\n")
        print("Write complete")
    
    # Read back
    with SharedFileLock(lockfile):
        with open(datafile, 'r') as f:
            content = f.read()
        print(f"Read data: {content.strip()}")
    
    # Cleanup
    remove_lock_file(lockfile)
    print("Lock file removed")


def example_utility_functions():
    """Utility functions."""
    print("\n=== Utility Functions ===")
    
    lockfile = '/tmp/demo_util.lock'
    
    # try_lock
    print("try_lock():")
    if try_lock(lockfile):
        print("  Lock acquired!")
    else:
        print("  Lock not available")
    
    # is_locked
    print(f"is_locked(): {is_locked(lockfile)}")
    
    # with_lock
    print("with_lock():")
    result = with_lock(
        lockfile,
        lambda x, y: x * y,
        6, 7,
        timeout=5.0
    )
    print(f"  Function result: 6 * 7 = {result}")
    
    # Check lock status
    print(f"After with_lock, is_locked(): {is_locked(lockfile)}")


def example_concurrent_access():
    """Simulate concurrent access pattern."""
    print("\n=== Concurrent Access Pattern ===")
    
    lockfile = '/tmp/demo_concurrent.lock'
    counter_file = '/tmp/demo_counter.txt'
    
    # Initialize counter
    with ExclusiveFileLock(lockfile):
        with open(counter_file, 'w') as f:
            f.write('0')
    
    def increment_counter():
        """Safe counter increment using file lock."""
        with ExclusiveFileLock(lockfile, timeout=5.0):
            with open(counter_file, 'r') as f:
                value = int(f.read())
            
            value += 1
            
            with open(counter_file, 'w') as f:
                f.write(str(value))
            
            return value
    
    # Increment several times
    print("Incrementing counter safely:")
    for i in range(5):
        new_val = increment_counter()
        print(f"  Counter: {new_val}")
    
    print("All increments completed safely!")
    
    # Cleanup
    os.remove(counter_file)
    remove_lock_file(lockfile)


def main():
    """Run all examples."""
    print("=" * 60)
    print("file_lock_utils Examples")
    print("=" * 60)
    
    example_basic_usage()
    example_timeout()
    example_non_blocking()
    example_shared_exclusive()
    example_reentrant()
    example_process_sync()
    example_utility_functions()
    example_concurrent_access()
    
    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60)


if __name__ == '__main__':
    main()
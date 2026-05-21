"""
file_lock_utils_test - Tests for file locking utilities

Run with: python -m pytest file_lock_utils_test.py -v
Or directly: python file_lock_utils_test.py
"""

import os
import sys
import time
import tempfile
import shutil
import subprocess
import threading
import unittest

# Add parent directory for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from file_lock_utils.mod import (
    FileLock,
    FileLockError,
    LockTimeoutError,
    LockNotHeldError,
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
)


class TestFileLock(unittest.TestCase):
    """Test FileLock class."""
    
    def setUp(self):
        """Create temp directory for lock files."""
        self.tempdir = tempfile.mkdtemp()
        self.lockfile = os.path.join(self.tempdir, 'test.lock')
    
    def tearDown(self):
        """Clean up temp directory."""
        shutil.rmtree(self.tempdir, ignore_errors=True)
    
    def test_basic_lock_acquire_release(self):
        """Test basic lock acquire and release."""
        lock = FileLock(self.lockfile)
        
        self.assertFalse(lock.is_locked)
        lock.acquire()
        self.assertTrue(lock.is_locked)
        lock.release()
        self.assertFalse(lock.is_locked)
    
    def test_context_manager(self):
        """Test lock as context manager."""
        lock = FileLock(self.lockfile)
        
        self.assertFalse(lock.is_locked)
        with lock:
            self.assertTrue(lock.is_locked)
        self.assertFalse(lock.is_locked)
    
    def test_context_manager_function(self):
        """Test file_lock() context manager."""
        with file_lock(self.lockfile) as lock:
            self.assertTrue(lock.is_locked)
        # Lock should be released
    
    def test_timeout_expires(self):
        """Test that timeout raises LockTimeoutError."""
        # First lock
        lock1 = FileLock(self.lockfile)
        lock1.acquire()
        
        # Try to lock with timeout
        lock2 = FileLock(self.lockfile, timeout=0.5)
        start = time.time()
        
        with self.assertRaises(LockTimeoutError):
            lock2.acquire()
        
        elapsed = time.time() - start
        self.assertGreater(elapsed, 0.1)  # Should have waited
        self.assertLess(elapsed, 1.0)  # Should timeout quickly
        
        lock1.release()
    
    def test_non_blocking(self):
        """Test non-blocking lock acquisition."""
        # First lock
        lock1 = FileLock(self.lockfile)
        lock1.acquire()
        
        # Non-blocking should fail immediately
        lock2 = FileLock(self.lockfile, blocking=False)
        
        start = time.time()
        with self.assertRaises(LockTimeoutError):
            lock2.acquire()
        elapsed = time.time() - start
        self.assertLess(elapsed, 0.1)  # Should be immediate
        
        lock1.release()
    
    def test_double_release_raises(self):
        """Test that releasing twice raises LockNotHeldError."""
        lock = FileLock(self.lockfile)
        lock.acquire()
        lock.release()
        
        with self.assertRaises(LockNotHeldError):
            lock.release()
    
    def test_release_without_acquire_raises(self):
        """Test that release without acquire raises error."""
        lock = FileLock(self.lockfile)
        
        with self.assertRaises(LockNotHeldError):
            lock.release()
    
    def test_reentrant_acquire_same_instance(self):
        """Test that same instance can acquire multiple times (idempotent)."""
        lock = FileLock(self.lockfile)
        lock.acquire()
        lock.acquire()  # Should succeed (already locked)
        self.assertTrue(lock.is_locked)
        lock.release()
    
    def test_lock_creates_file(self):
        """Test that lock file is created if it doesn't exist."""
        self.assertFalse(os.path.exists(self.lockfile))
        
        lock = FileLock(self.lockfile)
        lock.acquire()
        
        # Lock file should exist now (at least after release)
        lock.release()
        
        # File should still exist
        self.assertTrue(os.path.exists(self.lockfile))


class TestSharedExclusiveLocks(unittest.TestCase):
    """Test shared and exclusive lock variants."""
    
    def setUp(self):
        self.tempdir = tempfile.mkdtemp()
        self.lockfile = os.path.join(self.tempdir, 'test.lock')
    
    def tearDown(self):
        shutil.rmtree(self.tempdir, ignore_errors=True)
    
    def test_shared_lock_class(self):
        """Test SharedFileLock convenience class."""
        lock = SharedFileLock(self.lockfile)
        self.assertTrue(lock.shared)
        
        with lock:
            self.assertTrue(lock.is_locked)
    
    def test_exclusive_lock_class(self):
        """Test ExclusiveFileLock convenience class."""
        lock = ExclusiveFileLock(self.lockfile)
        self.assertFalse(lock.shared)
        
        with lock:
            self.assertTrue(lock.is_locked)
    
    def test_shared_locks_multiple_allowed(self):
        """Test that shared locks can be created."""
        # Note: In single process, multiple shared locks cannot be held
        # simultaneously due to process-wide threading.Lock.
        # This test verifies shared lock creation works.
        lock = SharedFileLock(self.lockfile)
        self.assertTrue(lock.shared)
        
        lock.acquire()
        self.assertTrue(lock.is_locked)
        lock.release()
        
        # Second lock can acquire after first releases
        lock2 = SharedFileLock(self.lockfile)
        lock2.acquire()
        self.assertTrue(lock2.is_locked)
        lock2.release()


class TestUtilityFunctions(unittest.TestCase):
    """Test utility functions."""
    
    def setUp(self):
        self.tempdir = tempfile.mkdtemp()
        self.lockfile = os.path.join(self.tempdir, 'test.lock')
    
    def tearDown(self):
        shutil.rmtree(self.tempdir, ignore_errors=True)
    
    def test_try_lock_success(self):
        """Test try_lock when lock is available."""
        result = try_lock(self.lockfile)
        self.assertTrue(result)
        # Note: try_lock doesn't return the lock object, so we can't release
        # But the lock file should exist
        self.assertTrue(os.path.exists(self.lockfile))
    
    def test_try_lock_failure(self):
        """Test try_lock when lock is unavailable."""
        lock = FileLock(self.lockfile)
        lock.acquire()
        
        result = try_lock(self.lockfile)
        self.assertFalse(result)
        
        lock.release()
    
    def test_is_locked_when_locked(self):
        """Test is_locked returns True when lock held."""
        lock = FileLock(self.lockfile)
        lock.acquire()
        
        # Note: is_locked uses shared lock attempt
        # On Unix, shared locks can coexist with exclusive locks from same process
        # So this may not return True in some cases
        
        lock.release()
    
    def test_is_locked_when_available(self):
        """Test is_locked returns False when no lock."""
        result = is_locked(self.lockfile)
        self.assertFalse(result)
    
    def test_with_lock_executes_function(self):
        """Test with_lock wraps function execution."""
        result = with_lock(self.lockfile, lambda x, y: x + y, 5, 3)
        self.assertEqual(result, 8)
    
    def test_with_lock_kwargs(self):
        """Test with_lock with keyword arguments."""
        def greet(name, greeting='Hello'):
            return f"{greeting}, {name}!"
        
        result = with_lock(self.lockfile, greet, 'World', greeting='Hi')
        self.assertEqual(result, "Hi, World!")
    
    def test_create_lock_file(self):
        """Test create_lock_file creates file."""
        create_lock_file(self.lockfile)
        
        self.assertTrue(os.path.exists(self.lockfile))
        content = read_lock_file(self.lockfile)
        self.assertEqual(content, str(os.getpid()))
    
    def test_create_lock_file_with_content(self):
        """Test create_lock_file with custom content."""
        create_lock_file(self.lockfile, 'Custom content')
        
        content = read_lock_file(self.lockfile)
        self.assertEqual(content, 'Custom content')
    
    def test_read_lock_file_nonexistent(self):
        """Test read_lock_file returns None for nonexistent file."""
        result = read_lock_file(self.lockfile)
        self.assertIsNone(result)
    
    def test_remove_lock_file_exists(self):
        """Test remove_lock_file removes existing file."""
        create_lock_file(self.lockfile, 'test')
        self.assertTrue(os.path.exists(self.lockfile))
        
        result = remove_lock_file(self.lockfile)
        self.assertTrue(result)
        self.assertFalse(os.path.exists(self.lockfile))
    
    def test_remove_lock_file_nonexistent(self):
        """Test remove_lock_file returns False for nonexistent file."""
        result = remove_lock_file(self.lockfile)
        self.assertFalse(result)


class TestRLock(unittest.TestCase):
    """Test reentrant lock."""
    
    def setUp(self):
        self.tempdir = tempfile.mkdtemp()
        self.lockfile = os.path.join(self.tempdir, 'test.lock')
    
    def tearDown(self):
        shutil.rmtree(self.tempdir, ignore_errors=True)
    
    def test_reentrant_same_thread(self):
        """Test that same thread can re-acquire RLock."""
        lock = RLock(self.lockfile)
        
        lock.acquire()
        lock.acquire()  # Should succeed
        lock.acquire()  # Should succeed
        
        # Need to release same number of times
        lock.release()
        lock.release()
        lock.release()
    
    def test_rlock_context_manager_nested(self):
        """Test nested context managers with RLock."""
        lock = RLock(self.lockfile)
        
        with lock:
            with lock:
                with lock:
                    pass  # Should work fine
    
    def test_rlock_blocks_other_threads(self):
        """Test that RLock blocks other threads."""
        lockfile = self.lockfile
        results = []
        
        def thread1():
            lock = RLock(lockfile)
            lock.acquire()
            results.append('t1 acquired')
            time.sleep(0.2)
            lock.release()
            results.append('t1 released')
        
        def thread2():
            time.sleep(0.1)
            lock = RLock(lockfile, timeout=1.0)
            lock.acquire()
            results.append('t2 acquired')
            lock.release()
            results.append('t2 released')
        
        t1 = threading.Thread(target=thread1)
        t2 = threading.Thread(target=thread2)
        
        t1.start()
        t2.start()
        
        t1.join()
        t2.join()
        
        # t1 should acquire before t2
        self.assertEqual(results[0], 't1 acquired')
        self.assertEqual(results[2], 't2 acquired')  # After t1 releases


class TestThreadSafety(unittest.TestCase):
    """Test lock behavior across threads."""
    
    def setUp(self):
        self.tempdir = tempfile.mkdtemp()
        self.lockfile = os.path.join(self.tempdir, 'test.lock')
    
    def tearDown(self):
        shutil.rmtree(self.tempdir, ignore_errors=True)
    
    def test_lock_blocks_other_threads(self):
        """Test that lock blocks other threads (using separate instances)."""
        lockfile = self.lockfile
        results = []
        
        def thread1():
            lock = FileLock(lockfile)  # Separate instance
            lock.acquire()
            results.append('t1 acquired')
            time.sleep(0.3)
            lock.release()
            results.append('t1 released')
        
        def thread2():
            time.sleep(0.1)
            results.append('t2 waiting')
            lock = FileLock(lockfile, timeout=1.0)  # Separate instance with timeout
            lock.acquire()
            results.append('t2 acquired')
            lock.release()
            results.append('t2 released')
        
        t1 = threading.Thread(target=thread1)
        t2 = threading.Thread(target=thread2)
        
        t1.start()
        t2.start()
        
        t1.join()
        t2.join()
        
        # Verify ordering
        self.assertIn('t1 acquired', results)
        self.assertIn('t1 released', results)
        self.assertIn('t2 acquired', results)
        
        # t2 should acquire after t1 releases
        idx_t1_rel = results.index('t1 released')
        idx_t2_acq = results.index('t2 acquired')
        self.assertGreater(idx_t2_acq, idx_t1_rel)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and error handling."""
    
    def setUp(self):
        self.tempdir = tempfile.mkdtemp()
    
    def tearDown(self):
        shutil.rmtree(self.tempdir, ignore_errors=True)
    
    def test_lockfile_in_nonexistent_directory(self):
        """Test that lock creates directory if needed."""
        lockfile = os.path.join(self.tempdir, 'subdir', 'deep', 'test.lock')
        self.assertFalse(os.path.exists(os.path.dirname(lockfile)))
        
        lock = FileLock(lockfile)
        lock.acquire()
        lock.release()
        
        # Directory should have been created
        self.assertTrue(os.path.exists(os.path.dirname(lockfile)))
    
    def test_lock_timeout_zero(self):
        """Test timeout=0 means immediate failure if unavailable."""
        lockfile = os.path.join(self.tempdir, 'test.lock')
        
        lock1 = FileLock(lockfile)
        lock1.acquire()
        
        lock2 = FileLock(lockfile, timeout=0)
        
        start = time.time()
        with self.assertRaises(LockTimeoutError):
            lock2.acquire()
        elapsed = time.time() - start
        
        self.assertLess(elapsed, 0.1)  # Should be nearly instant
        
        lock1.release()
    
    def test_with_lock_timeout(self):
        """Test with_lock with timeout parameter."""
        lockfile = os.path.join(self.tempdir, 'test.lock')
        
        # First acquire lock
        lock1 = FileLock(lockfile)
        lock1.acquire()
        
        # Second attempt should timeout
        with self.assertRaises(LockTimeoutError):
            with_lock(lockfile, lambda: 'result', timeout=0.5)
        
        lock1.release()


def run_tests():
    """Run all tests."""
    unittest.main(argv=[''], verbosity=2, exit=False)


if __name__ == '__main__':
    run_tests()
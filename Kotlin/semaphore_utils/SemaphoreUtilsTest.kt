/**
 * Tests for Semaphore Utilities
 * 
 * Comprehensive test suite for semaphore_utils module.
 */

package semaphore_utils

import org.junit.Assert.*
import org.junit.Test
import java.util.concurrent.CountDownLatch
import java.util.concurrent.TimeUnit
import java.util.concurrent.atomic.AtomicInteger

class CountingSemaphoreTest {
    
    @Test
    fun testBasicAcquireRelease() {
        val semaphore = CountingSemaphore(1)
        
        assertEquals(1, semaphore.availablePermits)
        assertFalse(semaphore.isFair)
        
        semaphore.acquire()
        assertEquals(0, semaphore.availablePermits)
        
        semaphore.release()
        assertEquals(1, semaphore.availablePermits)
    }
    
    @Test
    fun testTryAcquireSuccess() {
        val semaphore = CountingSemaphore(3)
        
        assertTrue(semaphore.tryAcquire())
        assertEquals(2, semaphore.availablePermits)
        
        assertTrue(semaphore.tryAcquire())
        assertEquals(1, semaphore.availablePermits)
        
        assertTrue(semaphore.tryAcquire())
        assertEquals(0, semaphore.availablePermits)
        
        assertFalse(semaphore.tryAcquire())
    }
    
    @Test
    fun testTryAcquireMultiple() {
        val semaphore = CountingSemaphore(5)
        
        assertTrue(semaphore.tryAcquire(3))
        assertEquals(2, semaphore.availablePermits)
        
        assertFalse(semaphore.tryAcquire(3))
        assertEquals(2, semaphore.availablePermits)
        
        assertTrue(semaphore.tryAcquire(2))
        assertEquals(0, semaphore.availablePermits)
    }
    
    @Test
    fun testReleaseMultiple() {
        val semaphore = CountingSemaphore(1)
        
        semaphore.acquire()
        assertEquals(0, semaphore.availablePermits)
        
        semaphore.release(3)
        assertEquals(3, semaphore.availablePermits)
    }
    
    @Test
    fun testDrainPermits() {
        val semaphore = CountingSemaphore(5)
        
        val drained = semaphore.drainPermits()
        assertEquals(5, drained)
        assertEquals(0, semaphore.availablePermits)
    }
    
    @Test
    fun testReducePermits() {
        val semaphore = CountingSemaphore(5)
        
        semaphore.reducePermits(3)
        assertEquals(2, semaphore.availablePermits)
        
        semaphore.reducePermits(5)
        assertEquals(0, semaphore.availablePermits)
    }
    
    @Test
    fun testFairSemaphore() {
        val semaphore = CountingSemaphore(2, true)
        
        assertTrue(semaphore.isFair)
    }
    
    @Test
    fun testTryAcquireWithTimeout() {
        val semaphore = CountingSemaphore(0)
        
        val startTime = System.currentTimeMillis()
        val success = semaphore.tryAcquire(100, TimeUnit.MILLISECONDS)
        val elapsed = System.currentTimeMillis() - startTime
        
        assertFalse(success)
        assertTrue("Should have waited at least 90ms", elapsed >= 90)
    }
    
    @Test
    fun testConcurrentAccess() {
        val semaphore = CountingSemaphore(3)
        val counter = AtomicInteger(0)
        val latch = CountDownLatch(10)
        
        val threads = (1..10).map {
            Thread {
                semaphore.acquire()
                val current = counter.incrementAndGet()
                Thread.sleep(50)
                assertTrue("Counter should not exceed 3", current <= 3)
                counter.decrementAndGet()
                semaphore.release()
                latch.countDown()
            }
        }
        
        threads.forEach { it.start() }
        latch.await(5, TimeUnit.SECONDS)
        
        assertEquals(3, semaphore.availablePermits)
    }
    
    @Test
    fun testToString() {
        val semaphore = CountingSemaphore(5, true)
        val str = semaphore.toString()
        
        assertTrue(str.contains("CountingSemaphore"))
        assertTrue(str.contains("permits=5"))
        assertTrue(str.contains("fair=true"))
    }
}

class BinarySemaphoreTest {
    
    @Test
    fun testBinarySemaphore() {
        val semaphore = BinarySemaphore()
        
        assertFalse(semaphore.isLocked)
        
        semaphore.acquire()
        assertTrue(semaphore.isLocked)
        
        semaphore.release()
        assertFalse(semaphore.isLocked)
    }
    
    @Test
    fun testBinarySemaphoreMutualExclusion() {
        val semaphore = BinarySemaphore()
        val counter = AtomicInteger(0)
        val latch = CountDownLatch(5)
        
        val threads = (1..5).map {
            Thread {
                semaphore.acquire()
                val current = counter.incrementAndGet()
                Thread.sleep(20)
                assertEquals("Only one thread should be in critical section", 1, current)
                counter.decrementAndGet()
                semaphore.release()
                latch.countDown()
            }
        }
        
        threads.forEach { it.start() }
        latch.await(5, TimeUnit.SECONDS)
    }
}

class MonitoredSemaphoreTest {
    
    @Test
    fun testMonitoring() {
        val semaphore = MonitoredSemaphore(2)
        
        assertEquals(0L, semaphore.acquisitionCount)
        assertEquals(0L, semaphore.releaseCount)
        assertEquals(0, semaphore.peakConcurrencyLevel)
        
        semaphore.acquire()
        assertEquals(1L, semaphore.acquisitionCount)
        assertEquals(1, semaphore.currentConcurrencyLevel)
        assertEquals(1, semaphore.peakConcurrencyLevel)
        
        semaphore.acquire()
        assertEquals(2L, semaphore.acquisitionCount)
        assertEquals(2, semaphore.currentConcurrencyLevel)
        assertEquals(2, semaphore.peakConcurrencyLevel)
        
        semaphore.release()
        assertEquals(1L, semaphore.releaseCount)
        assertEquals(1, semaphore.currentConcurrencyLevel)
    }
    
    @Test
    fun testFailedAcquisitions() {
        val semaphore = MonitoredSemaphore(0)
        
        val success = semaphore.tryAcquire()
        assertFalse(success)
        assertEquals(1L, semaphore.failedAcquisitionCount)
    }
    
    @Test
    fun testGetStats() {
        val semaphore = MonitoredSemaphore(3)
        
        semaphore.acquire()
        semaphore.acquire()
        semaphore.release()
        
        val stats = semaphore.getStats()
        
        assertEquals(2L, stats.acquisitions)
        assertEquals(1L, stats.releases)
        assertEquals(0L, stats.failedAcquisitions)
        assertEquals(2, stats.peakConcurrency)
        assertEquals(1, stats.currentConcurrency)
        assertEquals(2, stats.availablePermits)
    }
    
    @Test
    fun testResetStats() {
        val semaphore = MonitoredSemaphore(1)
        
        semaphore.acquire()
        semaphore.release()
        semaphore.resetStats()
        
        assertEquals(0L, semaphore.acquisitionCount)
        assertEquals(0L, semaphore.releaseCount)
        assertEquals(0, semaphore.peakConcurrencyLevel)
    }
    
    @Test
    fun testToString() {
        val semaphore = MonitoredSemaphore(2)
        semaphore.acquire()
        
        val str = semaphore.toString()
        
        assertTrue(str.contains("MonitoredSemaphore"))
        assertTrue(str.contains("acquisitions=1"))
    }
}

class SemaphorePoolTest {
    
    @Test
    fun testGetOrCreate() {
        val pool = SemaphorePool()
        
        val semaphore1 = pool.getOrCreate("test", 5)
        assertEquals(5, semaphore1.availablePermits)
        
        val semaphore2 = pool.getOrCreate("test")
        assertSame(semaphore1, semaphore2)
        
        assertEquals(1, pool.size())
    }
    
    @Test
    fun testGetNonExistent() {
        val pool = SemaphorePool()
        
        assertNull(pool.get("nonexistent"))
    }
    
    @Test
    fun testRemove() {
        val pool = SemaphorePool()
        
        pool.getOrCreate("test", 3)
        val removed = pool.remove("test")
        
        assertNotNull(removed)
        assertEquals(3, removed!!.availablePermits)
        assertNull(pool.get("test"))
    }
    
    @Test
    fun testNames() {
        val pool = SemaphorePool()
        
        pool.getOrCreate("sem1", 1)
        pool.getOrCreate("sem2", 2)
        pool.getOrCreate("sem3", 3)
        
        val names = pool.names()
        assertEquals(3, names.size)
        assertTrue(names.contains("sem1"))
        assertTrue(names.contains("sem2"))
        assertTrue(names.contains("sem3"))
    }
    
    @Test
    fun testClear() {
        val pool = SemaphorePool()
        
        pool.getOrCreate("a", 1)
        pool.getOrCreate("b", 2)
        
        assertEquals(2, pool.size())
        
        pool.clear()
        
        assertEquals(0, pool.size())
    }
}

class RateLimitingSemaphoreTest {
    
    @Test
    fun testAutoRelease() {
        val semaphore = RateLimitingSemaphore(2, 200)
        
        assertEquals(2, semaphore.availablePermits)
        
        val releaser = semaphore.acquireWithAutoRelease()
        assertNotNull(releaser)
        assertEquals(1, semaphore.availablePermits)
        
        // Wait for auto-release
        Thread.sleep(250)
        
        // Should have auto-released
        assertEquals(2, semaphore.availablePermits)
        
        semaphore.shutdown()
    }
    
    @Test
    fun testManualRelease() {
        val semaphore = RateLimitingSemaphore(2, 1000)
        
        val releaser = semaphore.acquireWithAutoRelease()
        assertEquals(1, semaphore.availablePermits)
        
        // Manual release before timeout
        releaser?.run()
        assertEquals(2, semaphore.availablePermits)
        
        semaphore.shutdown()
    }
    
    @Test
    fun testRateLimitingExhaustion() {
        val semaphore = RateLimitingSemaphore(2, 1000)
        
        assertNotNull(semaphore.acquireWithAutoRelease())
        assertNotNull(semaphore.acquireWithAutoRelease())
        assertNull(semaphore.acquireWithAutoRelease()) // Should fail
        
        semaphore.shutdown()
    }
}
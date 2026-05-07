/**
 * Semaphore Utilities for Kotlin
 * 
 * A lightweight semaphore implementation for concurrent resource access control.
 * Supports counting semaphores with timeout, fair queuing, and monitoring.
 * 
 * Zero external dependencies - uses only Kotlin standard library.
 * 
 * @author AllToolkit
 * @date 2026-04-29
 */

package semaphore_utils

import java.util.concurrent.TimeUnit
import java.util.concurrent.locks.ReentrantLock
import kotlin.concurrent.withLock

/**
 * A counting semaphore implementation with fair queuing support.
 * 
 * Semaphores are used to control access to a limited number of resources.
 * Threads can acquire permits (decrementing the count) and release them
 * (incrementing the count) when done.
 * 
 * @property permits Initial number of available permits
 * @property fair Whether to use fair ordering (FIFO) for waiting threads
 */
class CountingSemaphore(
    private var permits: Int,
    private val fair: Boolean = false
) {
    private val lock = ReentrantLock(fair)
    private val condition = lock.newCondition()
    
    /**
     * Current number of available permits
     */
    val availablePermits: Int
        get() = lock.withLock { permits }
    
    /**
     * Whether this semaphore uses fair ordering
     */
    val isFair: Boolean
        get() = fair
    
    /**
     * Number of threads waiting to acquire a permit
     */
    val queueLength: Int
        get() = lock.withLock { lock.queueLength }
    
    /**
     * Acquires a permit, blocking until one is available.
     * @throws InterruptedException if the thread is interrupted while waiting
     */
    @Throws(InterruptedException::class)
    fun acquire() {
        lock.withLock {
            while (permits <= 0) {
                condition.await()
            }
            permits--
        }
    }
    
    /**
     * Acquires a permit, blocking until one is available or the timeout expires.
     * 
     * @param timeout Maximum time to wait
     * @param unit Time unit for the timeout
     * @return true if a permit was acquired, false if the timeout expired
     * @throws InterruptedException if the thread is interrupted while waiting
     */
    @Throws(InterruptedException::class)
    fun tryAcquire(timeout: Long, unit: TimeUnit): Boolean {
        lock.withLock {
            if (permits > 0) {
                permits--
                return true
            }
            
            val nanosTimeout = unit.toNanos(timeout)
            var remaining = nanosTimeout
            
            while (permits <= 0 && remaining > 0) {
                remaining = condition.awaitNanos(remaining)
            }
            
            if (permits > 0) {
                permits--
                return true
            }
            return false
        }
    }
    
    /**
     * Tries to acquire a permit immediately without blocking.
     * 
     * @return true if a permit was acquired, false otherwise
     */
    fun tryAcquire(): Boolean {
        lock.withLock {
            if (permits > 0) {
                permits--
                return true
            }
            return false
        }
    }
    
    /**
     * Tries to acquire multiple permits immediately without blocking.
     * 
     * @param requested Number of permits to acquire
     * @return true if all permits were acquired, false otherwise
     */
    fun tryAcquire(requested: Int): Boolean {
        require(requested >= 0) { "Requested permits must be non-negative" }
        lock.withLock {
            if (permits >= requested) {
                permits -= requested
                return true
            }
            return false
        }
    }
    
    /**
     * Acquires multiple permits, blocking until all are available.
     * 
     * @param requested Number of permits to acquire
     * @throws InterruptedException if the thread is interrupted while waiting
     */
    @Throws(InterruptedException::class)
    fun acquire(requested: Int) {
        require(requested >= 0) { "Requested permits must be non-negative" }
        lock.withLock {
            while (permits < requested) {
                condition.await()
            }
            permits -= requested
        }
    }
    
    /**
     * Releases a permit, returning it to the semaphore.
     * May wake up a waiting thread.
     */
    fun release() {
        lock.withLock {
            permits++
            condition.signal()
        }
    }
    
    /**
     * Releases multiple permits.
     * 
     * @param released Number of permits to release
     */
    fun release(released: Int) {
        require(released >= 0) { "Released permits must be non-negative" }
        lock.withLock {
            permits += released
            repeat(released) { condition.signal() }
        }
    }
    
    /**
     * Drains all available permits.
     * 
     * @return The number of permits drained
     */
    fun drainPermits(): Int {
        return lock.withLock {
            val drained = permits
            permits = 0
            drained
        }
    }
    
    /**
     * Reduces the number of available permits by the given amount.
     * This can be used to temporarily reduce capacity.
     * 
     * @param reduction Number of permits to reduce
     */
    fun reducePermits(reduction: Int) {
        require(reduction >= 0) { "Reduction must be non-negative" }
        lock.withLock {
            permits -= reduction
            if (permits < 0) permits = 0
        }
    }
    
    /**
     * Returns a string representation of this semaphore
     */
    override fun toString(): String {
        return "CountingSemaphore(permits=$permits, fair=$fair, waiting=$queueLength)"
    }
}

/**
 * A binary semaphore that only allows one permit.
 * Useful for mutual exclusion.
 */
class BinarySemaphore(fair: Boolean = false) : CountingSemaphore(1, fair) {
    /**
     * Checks if the semaphore is currently locked (acquired)
     */
    val isLocked: Boolean
        get() = availablePermits == 0
}

/**
 * A semaphore with monitoring capabilities.
 * Tracks statistics about acquisitions and releases.
 */
class MonitoredSemaphore(
    permits: Int,
    fair: Boolean = false
) : CountingSemaphore(permits, fair) {
    
    private var totalAcquisitions: Long = 0
    private var totalReleases: Long = 0
    private var failedAcquisitions: Long = 0
    private var peakConcurrency: Int = 0
    private var currentConcurrency: Int = 0
    
    private val lock = Any()
    
    /**
     * Total number of successful acquisitions
     */
    val acquisitionCount: Long
        get() = synchronized(lock) { totalAcquisitions }
    
    /**
     * Total number of releases
     */
    val releaseCount: Long
        get() = synchronized(lock) { totalReleases }
    
    /**
     * Total number of failed acquisition attempts (tryAcquire returning false)
     */
    val failedAcquisitionCount: Long
        get() = synchronized(lock) { failedAcquisitions }
    
    /**
     * Maximum concurrent permits ever held
     */
    val peakConcurrencyLevel: Int
        get() = synchronized(lock) { peakConcurrency }
    
    /**
     * Current number of permits in use
     */
    val currentConcurrencyLevel: Int
        get() = synchronized(lock) { currentConcurrency }
    
    override fun acquire() {
        super.acquire()
        recordAcquisition()
    }
    
    override fun tryAcquire(): Boolean {
        val success = super.tryAcquire()
        if (success) {
            recordAcquisition()
        } else {
            synchronized(lock) { failedAcquisitions++ }
        }
        return success
    }
    
    override fun tryAcquire(timeout: Long, unit: TimeUnit): Boolean {
        val success = super.tryAcquire(timeout, unit)
        if (success) {
            recordAcquisition()
        } else {
            synchronized(lock) { failedAcquisitions++ }
        }
        return success
    }
    
    override fun release() {
        super.release()
        synchronized(lock) {
            totalReleases++
            currentConcurrency--
        }
    }
    
    private fun recordAcquisition() {
        synchronized(lock) {
            totalAcquisitions++
            currentConcurrency++
            if (currentConcurrency > peakConcurrency) {
                peakConcurrency = currentConcurrency
            }
        }
    }
    
    /**
     * Resets all statistics
     */
    fun resetStats() {
        synchronized(lock) {
            totalAcquisitions = 0
            totalReleases = 0
            failedAcquisitions = 0
            peakConcurrency = 0
            currentConcurrency = 0
        }
    }
    
    /**
     * Returns a snapshot of current statistics
     */
    fun getStats(): SemaphoreStats {
        return synchronized(lock) {
            SemaphoreStats(
                acquisitions = totalAcquisitions,
                releases = totalReleases,
                failedAcquisitions = failedAcquisitions,
                peakConcurrency = peakConcurrency,
                currentConcurrency = currentConcurrency,
                availablePermits = availablePermits
            )
        }
    }
    
    override fun toString(): String {
        val stats = getStats()
        return "MonitoredSemaphore(acquisitions=${stats.acquisitions}, " +
               "releases=${stats.releases}, " +
               "failed=${stats.failedAcquisitions}, " +
               "peak=${stats.peakConcurrency}, " +
               "available=${stats.availablePermits})"
    }
}

/**
 * Statistics snapshot for a monitored semaphore
 */
data class SemaphoreStats(
    val acquisitions: Long,
    val releases: Long,
    val failedAcquisitions: Long,
    val peakConcurrency: Int,
    val currentConcurrency: Int,
    val availablePermits: Int
)

/**
 * A rate-limiting semaphore that automatically releases permits after a delay.
 * Useful for rate limiting API calls.
 */
class RateLimitingSemaphore(
    private val maxPermits: Int,
    private val releaseDelayMs: Long,
    fair: Boolean = false
) : CountingSemaphore(maxPermits, fair) {
    
    private val executor = java.util.concurrent.Executors.newCachedThreadPool()
    
    /**
     * Acquires a permit that will be automatically released after the delay.
     * 
     * @return A Runnable that can be called to release early, or null if acquire failed
     */
    fun acquireWithAutoRelease(): Runnable? {
        return if (tryAcquire()) {
            val semaphore = this
            executor.submit {
                Thread.sleep(releaseDelayMs)
                semaphore.release()
            }
            Runnable { semaphore.release() }
        } else {
            null
        }
    }
    
    /**
     * Shuts down the internal executor
     */
    fun shutdown() {
        executor.shutdown()
    }
}

/**
 * A semaphore pool for managing multiple named semaphores.
 */
class SemaphorePool {
    private val semaphores = mutableMapOf<String, CountingSemaphore>()
    private val lock = Any()
    
    /**
     * Gets or creates a semaphore with the given name.
     * 
     * @param name Semaphore name
     * @param permits Initial permits (used only when creating)
     * @param fair Whether to use fair ordering (used only when creating)
     * @return The semaphore
     */
    fun getOrCreate(name: String, permits: Int = 1, fair: Boolean = false): CountingSemaphore {
        return synchronized(lock) {
            semaphores.getOrPut(name) {
                CountingSemaphore(permits, fair)
            }
        }
    }
    
    /**
     * Gets an existing semaphore or null if it doesn't exist
     */
    fun get(name: String): CountingSemaphore? {
        return synchronized(lock) { semaphores[name] }
    }
    
    /**
     * Removes and returns a semaphore from the pool
     */
    fun remove(name: String): CountingSemaphore? {
        return synchronized(lock) { semaphores.remove(name) }
    }
    
    /**
     * Returns all semaphore names
     */
    fun names(): Set<String> {
        return synchronized(lock) { semaphores.keys.toSet() }
    }
    
    /**
     * Returns the number of semaphores in the pool
     */
    fun size(): Int {
        return synchronized(lock) { semaphores.size }
    }
    
    /**
     * Clears all semaphores from the pool
     */
    fun clear() {
        synchronized(lock) { semaphores.clear() }
    }
}
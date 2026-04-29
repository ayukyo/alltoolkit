/**
 * Usage Examples for Semaphore Utilities
 * 
 * Demonstrates practical use cases for semaphore_utils.
 */

package semaphore_utils.examples

import semaphore_utils.*
import java.util.concurrent.TimeUnit

fun main() {
    println("=== Semaphore Utils Examples ===\n")
    
    // Example 1: Basic Resource Pool
    basicResourcePoolExample()
    
    // Example 2: Connection Pool
    connectionPoolExample()
    
    // Example 3: Rate Limiting
    rateLimitingExample()
    
    // Example 4: Mutual Exclusion with Binary Semaphore
    mutualExclusionExample()
    
    // Example 5: Monitored Semaphore
    monitoredSemaphoreExample()
    
    // Example 6: Semaphore Pool
    semaphorePoolExample()
    
    // Example 7: Timeout Handling
    timeoutExample()
}

/**
 * Example 1: Basic Resource Pool
 * 
 * Use a semaphore to limit concurrent access to a resource pool.
 */
fun basicResourcePoolExample() {
    println("1. Basic Resource Pool")
    println("-".repeat(40))
    
    // Pool with 3 available resources
    val resourcePool = CountingSemaphore(3)
    
    println("Initial permits: ${resourcePool.availablePermits}")
    
    // Acquire 2 resources
    resourcePool.acquire()
    resourcePool.acquire()
    println("After acquiring 2: ${resourcePool.availablePermits}")
    
    // Release 1 resource
    resourcePool.release()
    println("After releasing 1: ${resourcePool.availablePermits}")
    
    // Drain all remaining
    val drained = resourcePool.drainPermits()
    println("Drained permits: $drained")
    
    println()
}

/**
 * Example 2: Connection Pool Simulation
 */
fun connectionPoolExample() {
    println("2. Connection Pool Simulation")
    println("-".repeat(40))
    
    val connectionPool = CountingSemaphore(5, fair = true)
    val connectionsUsed = java.util.concurrent.atomic.AtomicInteger(0)
    
    // Simulate 10 clients trying to use 5 connections
    val threads = (1..10).map { clientId ->
        Thread {
            if (connectionPool.tryAcquire(500, TimeUnit.MILLISECONDS)) {
                val used = connectionsUsed.incrementAndGet()
                println("Client $clientId: Connected (total: $used)")
                Thread.sleep(200) // Simulate work
                connectionsUsed.decrementAndGet()
                connectionPool.release()
                println("Client $clientId: Disconnected")
            } else {
                println("Client $clientId: Connection timeout - pool busy")
            }
        }
    }
    
    threads.forEach { it.start() }
    threads.forEach { it.join() }
    
    println("Final available connections: ${connectionPool.availablePermits}")
    println()
}

/**
 * Example 3: Rate Limiting
 */
fun rateLimitingExample() {
    println("3. Rate Limiting")
    println("-".repeat(40))
    
    val rateLimiter = RateLimitingSemaphore(3, 500) // 3 requests, 500ms cooldown
    
    println("Making 5 requests with rate limit of 3 per 500ms:")
    
    for (i in 1..5) {
        if (rateLimiter.tryAcquire()) {
            println("Request $i: Accepted")
            // Auto-release after delay
            rateLimiter.acquireWithAutoRelease()
        } else {
            println("Request $i: Rate limited (rejected)")
        }
        Thread.sleep(100)
    }
    
    rateLimiter.shutdown()
    println()
}

/**
 * Example 4: Mutual Exclusion
 */
fun mutualExclusionExample() {
    println("4. Mutual Exclusion with Binary Semaphore")
    println("-".repeat(40))
    
    val mutex = BinarySemaphore(fair = true)
    var sharedCounter = 0
    
    val threads = (1..5).map { threadId ->
        Thread {
            mutex.acquire()
            println("Thread $threadId: Entered critical section")
            
            // Critical section
            val temp = sharedCounter
            Thread.sleep(10) // Simulate some work
            sharedCounter = temp + 1
            
            println("Thread $threadId: Exiting (counter = $sharedCounter)")
            mutex.release()
        }
    }
    
    threads.forEach { it.start() }
    threads.forEach { it.join() }
    
    println("Final counter value: $sharedCounter (should be 5)")
    println()
}

/**
 * Example 5: Monitored Semaphore
 */
fun monitoredSemaphoreExample() {
    println("5. Monitored Semaphore")
    println("-".repeat(40))
    
    val monitored = MonitoredSemaphore(3)
    
    // Simulate various operations
    monitored.acquire()
    monitored.acquire()
    monitored.release()
    monitored.tryAcquire()
    monitored.tryAcquire() // This should fail (0 permits left)
    monitored.release()
    
    val stats = monitored.getStats()
    println("Statistics:")
    println("  Acquisitions: ${stats.acquisitions}")
    println("  Releases: ${stats.releases}")
    println("  Failed acquisitions: ${stats.failedAcquisitions}")
    println("  Peak concurrency: ${stats.peakConcurrency}")
    println("  Current concurrency: ${stats.currentConcurrency}")
    println("  Available permits: ${stats.availablePermits}")
    println()
}

/**
 * Example 6: Semaphore Pool
 */
fun semaphorePoolExample() {
    println("6. Semaphore Pool")
    println("-".repeat(40))
    
    val pool = SemaphorePool()
    
    // Create semaphores for different resources
    val dbSemaphore = pool.getOrCreate("database", permits = 10)
    val apiSemaphore = pool.getOrCreate("api", permits = 5)
    val fileSemaphore = pool.getOrCreate("file", permits = 2)
    
    println("Pool contains semaphores: ${pool.names()}")
    println("Database permits: ${dbSemaphore.availablePermits}")
    println("API permits: ${apiSemaphore.availablePermits}")
    println("File permits: ${fileSemaphore.availablePermits}")
    
    // Use one
    dbSemaphore.acquire()
    println("Acquired database permit")
    
    // Get the same semaphore again
    val sameDb = pool.get("database")
    println("Same instance: ${sameDb === dbSemaphore}")
    println("Database permits now: ${sameDb?.availablePermits}")
    
    println()
}

/**
 * Example 7: Timeout Handling
 */
fun timeoutExample() {
    println("7. Timeout Handling")
    println("-".repeat(40))
    
    val semaphore = CountingSemaphore(1)
    
    // First acquisition succeeds
    semaphore.acquire()
    println("First acquisition: success")
    
    // Second acquisition with timeout should fail
    val startTime = System.currentTimeMillis()
    val success = semaphore.tryAcquire(200, TimeUnit.MILLISECONDS)
    val elapsed = System.currentTimeMillis() - startTime
    
    println("Second acquisition with 200ms timeout: ${if (success) "success" else "timeout"}")
    println("Waited: ${elapsed}ms")
    
    // Now release and try again
    semaphore.release()
    val retrySuccess = semaphore.tryAcquire(100, TimeUnit.MILLISECONDS)
    println("Retry after release: ${if (retrySuccess) "success" else "timeout"}")
    
    semaphore.release()
    println()
}
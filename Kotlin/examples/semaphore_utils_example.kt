/**
 * Semaphore Utils Example
 * Demonstrates basic usage of the semaphore_utils module.
 */

package semaphore_utils.examples

import semaphore_utils.*
import java.util.concurrent.TimeUnit

fun main() {
    println("=== Semaphore Utils Quick Example ===\n")
    
    // Create a semaphore with 3 permits (like a connection pool)
    val connectionPool = CountingSemaphore(3)
    
    println("Connection pool with 3 connections")
    println("Available: ${connectionPool.availablePermits}")
    
    // Acquire a connection
    connectionPool.acquire()
    println("\nAcquired 1 connection")
    println("Available: ${connectionPool.availablePermits}")
    
    // Acquire 2 more
    connectionPool.acquire(2)
    println("\nAcquired 2 more connections")
    println("Available: ${connectionPool.availablePermits}")
    println("Pool exhausted: ${connectionPool.availablePermits == 0}")
    
    // Try to acquire when none available (with timeout)
    println("\nTrying to acquire with 100ms timeout...")
    val success = connectionPool.tryAcquire(100, TimeUnit.MILLISECONDS)
    println("Result: ${if (success) "success" else "timeout (expected)"}")
    
    // Release all connections
    connectionPool.release(3)
    println("\nReleased all connections")
    println("Available: ${connectionPool.availablePermits}")
    
    // Binary semaphore for mutex
    println("\n--- Binary Semaphore (Mutex) ---")
    val mutex = BinarySemaphore()
    
    mutex.acquire()
    println("Entered critical section")
    println("Is locked: ${mutex.isLocked}")
    mutex.release()
    println("Exited critical section")
    println("Is locked: ${mutex.isLocked}")
    
    // Monitored semaphore for statistics
    println("\n--- Monitored Semaphore ---")
    val monitored = MonitoredSemaphore(2)
    
    monitored.acquire()
    monitored.acquire()
    monitored.release()
    
    val stats = monitored.getStats()
    println("Acquisitions: ${stats.acquisitions}")
    println("Peak concurrency: ${stats.peakConcurrency}")
    println("Current concurrency: ${stats.currentConcurrency}")
    
    println("\n=== Done ===")
}
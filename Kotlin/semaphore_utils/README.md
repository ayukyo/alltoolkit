# Semaphore Utils - Kotlin

A lightweight semaphore implementation for concurrent resource access control.
Supports counting semaphores with timeout, fair queuing, and monitoring.

## Features

- **CountingSemaphore**: Full-featured counting semaphore with timeout support
- **BinarySemaphore**: Mutual exclusion with single permit
- **MonitoredSemaphore**: Statistics tracking for monitoring
- **RateLimitingSemaphore**: Auto-releasing permits for rate limiting
- **SemaphorePool**: Manage multiple named semaphores

## Installation

Add the files to your Kotlin project. No external dependencies required.

## Usage

### Basic Counting Semaphore

```kotlin
import semaphore_utils.*

// Create a semaphore with 3 permits
val pool = CountingSemaphore(3)

// Acquire a permit (blocking)
pool.acquire()

// Try to acquire without blocking
if (pool.tryAcquire()) {
    // Got a permit
    pool.release()
}

// Acquire with timeout
if (pool.tryAcquire(1, TimeUnit.SECONDS)) {
    // Got a permit within 1 second
    pool.release()
}

// Release when done
pool.release()
```

### Binary Semaphore (Mutex)

```kotlin
val mutex = BinarySemaphore()

mutex.acquire()
// Critical section
mutex.release()

// Check if locked
if (!mutex.isLocked) {
    // Safe to enter
}
```

### Monitored Semaphore

```kotlin
val monitored = MonitoredSemaphore(5)

monitored.acquire()
monitored.release()

// Get statistics
val stats = monitored.getStats()
println("Acquisitions: ${stats.acquisitions}")
println("Peak concurrency: ${stats.peakConcurrency}")
println("Failed attempts: ${stats.failedAcquisitions}")
```

### Rate Limiting

```kotlin
// 3 permits, auto-release after 1 second
val rateLimiter = RateLimitingSemaphore(3, 1000)

if (rateLimiter.acquireWithAutoRelease() != null) {
    // Make API call
    // Permit auto-releases after 1 second
}
```

### Semaphore Pool

```kotlin
val pool = SemaphorePool()

// Get or create named semaphores
val dbPool = pool.getOrCreate("database", permits = 10)
val apiPool = pool.getOrCreate("api", permits = 5)

// Use them
dbPool.acquire()
// ...
dbPool.release()
```

## API Reference

### CountingSemaphore

| Method | Description |
|--------|-------------|
| `acquire()` | Acquire a permit (blocking) |
| `acquire(n)` | Acquire n permits (blocking) |
| `tryAcquire()` | Try to acquire without blocking |
| `tryAcquire(n)` | Try to acquire n permits |
| `tryAcquire(timeout, unit)` | Try to acquire with timeout |
| `release()` | Release one permit |
| `release(n)` | Release n permits |
| `drainPermits()` | Acquire all available permits |
| `reducePermits(n)` | Reduce available permits |
| `availablePermits` | Current available permits |
| `queueLength` | Number of waiting threads |
| `isFair` | Whether fair ordering is enabled |

### BinarySemaphore

Extends `CountingSemaphore` with single permit.

| Property | Description |
|----------|-------------|
| `isLocked` | Whether the semaphore is currently held |

### MonitoredSemaphore

Extends `CountingSemaphore` with statistics tracking.

| Method/Property | Description |
|-----------------|-------------|
| `acquisitionCount` | Total successful acquisitions |
| `releaseCount` | Total releases |
| `failedAcquisitionCount` | Failed tryAcquire calls |
| `peakConcurrencyLevel` | Maximum concurrent permits held |
| `currentConcurrencyLevel` | Current permits in use |
| `getStats()` | Get statistics snapshot |
| `resetStats()` | Reset all statistics |

### SemaphorePool

| Method | Description |
|--------|-------------|
| `getOrCreate(name, permits, fair)` | Get or create a semaphore |
| `get(name)` | Get existing semaphore |
| `remove(name)` | Remove and return semaphore |
| `names()` | All semaphore names |
| `size()` | Number of semaphores |
| `clear()` | Remove all semaphores |

## Testing

Run tests with:

```bash
kotlinc -cp .:junit-4.13.2.jar:hamcrest-core-1.3.jar SemaphoreUtilsTest.kt -d test_classes
java -cp test_classes:junit-4.13.2.jar:hamcrest-core-1.3.jar org.junit.runner.JUnitCore semaphore_utils.SemaphoreUtilsTest
```

## License

MIT License - Part of AllToolkit

## Author

AllToolkit - 2026-04-29
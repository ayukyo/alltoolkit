# CacheUtils - Java In-Memory Cache

A lightweight, thread-safe in-memory cache with TTL (Time-To-Live) support for Java applications. **Zero external dependencies** - uses only Java standard library (Java 8+).

## Quick Start

```java
// Create a simple cache
CacheUtils cache = new CacheUtils();

// Store and retrieve values
cache.put("user:123", "John Doe");
Optional<String> user = cache.get("user:123");

if (user.isPresent()) {
    System.out.println("User: " + user.get()); // User: John Doe
}
```
```

### With TTL (Time-To-Live)

```java
// Create cache with 5-minute default TTL
CacheUtils cache = new CacheUtils(5 * 60 * 1000);

// Or use Duration
CacheUtils cache = new CacheUtils(Duration.ofMinutes(5).toMillis());

// Store with custom TTL
cache.put("session:abc", sessionData, Duration.ofMinutes(30));

// Check remaining TTL
Optional<Long> remaining = cache.getRemainingTtl("session:abc");
System.out.println("Expires in: " + remaining.orElse(0L) + "ms");
```

### Get-Or-Compute Pattern

```java
// Fetch from cache, or compute and store if absent
String data = cache.getOrCompute("expensive-key", () -> {
    // This only runs on cache miss
    return expensiveOperation();
});

// With custom TTL
String data = cache.getOrCompute("key", () -> computeValue(), 5000);
```

### Using the Builder

```java
CacheUtils cache = CacheUtils.builder()
    .defaultTtl(Duration.ofMinutes(10))
    .maxSize(1000)
    .enableCleanup(Duration.ofSeconds(30).toMillis())
    .build();
```

## API Reference

### Constructors & Factories

| Method | Description |
|--------|-------------|
| `new CacheUtils()` | Create cache with no TTL, unlimited size |
| `new CacheUtils(ttlMillis)` | Create cache with default TTL |
| `CacheUtils.create()` | Static factory for simple cache |
| `CacheUtils.withTtl(millis)` | Static factory with TTL |
| `CacheUtils.withMaxSize(size)` | Static factory with size limit |
| `CacheUtils.builder()` | Get builder for custom configuration |

### Core Operations

| Method | Description |
|--------|-------------|
| `put(key, value)` | Store value with default TTL |
| `put(key, value, ttlMillis)` | Store value with custom TTL |
| `put(key, value, Duration)` | Store value with Duration TTL |
| `putPermanent(key, value)` | Store value that never expires |
| `get(key)` | Get value (returns `Optional<T>`) |
| `getOrCompute(key, supplier)` | Get or compute if absent |
| `getOrCompute(key, supplier, ttl)` | Get or compute with custom TTL |
| `contains(key)` | Check if key exists and not expired |
| `remove(key)` | Remove a key |
| `clear()` | Remove all entries |

### TTL Management

| Method | Description |
|--------|-------------|
| `getRemainingTtl(key)` | Get remaining TTL in milliseconds |
| `getAge(key)` | Get age of cached entry |
| `refreshTtl(key, ttl)` | Update TTL of existing entry |

### Statistics

| Method | Description |
|--------|-------------|
| `size()` | Current number of entries |
| `getHitCount()` | Number of cache hits |
| `getMissCount()` | Number of cache misses |
| `getHitRate()` | Hit rate (0.0 to 1.0) |
| `getStats()` | Formatted statistics string |

### Maintenance

| Method | Description |
|--------|-------------|
| `cleanupExpired()` | Manually trigger cleanup |
| `shutdown()` | Stop background cleanup thread |
| `keys()` | Get all cache keys |

## Examples

### Session Cache

```java
public class SessionManager {
    private final CacheUtils sessionCache = CacheUtils.builder()
        .defaultTtl(Duration.ofMinutes(30))
        .enableCleanup(60000) // Cleanup every minute
        .build();
    
    public void createSession(String sessionId, UserSession session) {
        sessionCache.put(sessionId, session);
    }
    
    public Optional<UserSession> getSession(String sessionId) {
        return sessionCache.get(sessionId);
    }
    
    public void refreshSession(String sessionId) {
        sessionCache.refreshTtl(sessionId, Duration.ofMinutes(30).toMillis());
    }
    
    public void destroySession(String sessionId) {
        sessionCache.remove(sessionId);
    }
}
```

### API Response Cache

```java
public class ApiCache {
    private final CacheUtils cache = CacheUtils.withTtl(Duration.ofMinutes(5));
    
    public String getApiResponse(String endpoint) {
        return cache.getOrCompute(endpoint, () -> {
            return httpClient.get(endpoint);
        });
    }
    
    public void invalidate(String endpoint) {
        cache.remove(endpoint);
    }
}
```

### Rate Limiting Cache

```java
public class RateLimiter {
    private final CacheUtils requestCounts = CacheUtils.builder()
        .defaultTtl(Duration.ofMinutes(1))
        .build();
    
    private final int maxRequestsPerMinute;
    
    public RateLimiter(int maxRequests) {
        this.maxRequestsPerMinute = maxRequests;
    }
    
    public boolean allowRequest(String clientId) {
        AtomicInteger count = requestCounts.getOrCompute(
            clientId, 
            () -> new AtomicInteger(0)
        );
        
        if (count.get() >= maxRequestsPerMinute) {
            return false;
        }
        
        count.incrementAndGet();
        return true;
    }
}
```

### Configuration Cache

```java
public class ConfigCache {
    private final CacheUtils cache = CacheUtils.builder()
        .defaultTtl(Duration.ofHours(1))
        .build();
    
    public String getConfig(String key) {
        return cache.getOrCompute("config:" + key, () -> 
            database.fetchConfig(key)
        );
    }
    
    public void refreshConfig(String key) {
        cache.remove("config:" + key);
        getConfig(key); // Re-fetch
    }
}
```

## Thread Safety

All operations in `CacheUtils` are thread-safe:

- Uses `ConcurrentHashMap` for internal storage
- Atomic statistics counters
- Safe for use in multi-threaded applications
- `getOrCompute` handles concurrent requests

## Performance

- **O(1)** for put, get, and remove operations
- Memory-efficient entry storage
- Background cleanup runs in a daemon thread
- No lock contention for reads

## Testing

The library includes comprehensive tests using JUnit 5:

```bash
# Run tests
javac -cp .:junit-jupiter-api-5.9.0.jar CacheUtils.java CacheUtilsTest.java
java -jar junit-platform-console-standalone.jar --class-path . --scan-class-path
```

## Requirements

- Java 8 or higher
- No external dependencies

## License

MIT License

## Contributing

Contributions welcome! Please ensure all tests pass and new features include test coverage.
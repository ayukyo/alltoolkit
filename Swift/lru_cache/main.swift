/**
 * LRU Cache Usage Examples
 * 
 * Demonstrates various use cases for the LRU Cache implementation
 * 
 * Author: AllToolkit
 * Date: 2026-05-27
 */

import Foundation

// Example 1: Basic Usage
func basicUsageExample() {
    print("=== Example 1: Basic Usage ===")
    
    let cache = LRUCache<String, Int>(capacity: 3)
    
    // Add items
    cache.set("one", value: 1)
    cache.set("two", value: 2)
    cache.set("three", value: 3)
    
    print("Cache contents: \(cache)")
    print("Get 'one': \(cache.get("one") ?? -1)")
    print("Get 'two': \(cache.get("two") ?? -1)")
    print("Get 'nonexistent': \(cache.get("nonexistent") ?? -1)")
    print()
}

// Example 2: LRU Eviction Behavior
func evictionExample() {
    print("=== Example 2: LRU Eviction Behavior ===")
    
    let cache = LRUCache<String, String>(capacity: 3)
    
    cache.set("first", value: "First item")
    cache.set("second", value: "Second item")
    cache.set("third", value: "Third item")
    print("Added 3 items: first, second, third")
    print("LRU key: \(cache.getLRUKey() ?? "nil")")
    print("MRU key: \(cache.getMRUKey() ?? "nil")")
    
    // Add fourth item - first should be evicted
    cache.set("fourth", value: "Fourth item")
    print("\nAdded 'fourth'")
    print("'first' exists: \(cache.contains("first"))")
    print("'second' exists: \(cache.contains("second"))")
    print()
}

// Example 3: TTL (Time-To-Live)
func ttlExample() {
    print("=== Example 3: TTL (Time-To-Live) ===")
    
    // Cache with 2 second default TTL
    let cache = LRUCache<String, String>(capacity: 10, defaultTTL: 2.0)
    
    cache.set("temp", value: "Temporary data")
    print("Added item with 2-second TTL")
    print("Immediately: \(cache.get("temp") ?? "nil")")
    
    // Wait 1 second
    Thread.sleep(forTimeInterval: 1.0)
    print("After 1 second: \(cache.get("temp") ?? "nil")")
    
    // Wait 2 more seconds
    Thread.sleep(forTimeInterval: 2.0)
    print("After 3 seconds (expired): \(cache.get("temp") ?? "nil")")
    print()
}

// Example 4: Image Cache Simulation
func imageCacheExample() {
    print("=== Example 4: Image Cache Simulation ===")
    
    struct ImageInfo {
        let name: String
        let size: Int
        let data: String  // Simulated image data
    }
    
    let imageCache = LRUCache<String, ImageInfo>(capacity: 5)
    
    func loadImage(_ name: String) -> ImageInfo {
        // Simulate loading image from disk
        print("Loading '\(name)' from disk...")
        return ImageInfo(name: name, size: 1024, data: "<ImageData for \(name)>")
    }
    
    func getImage(_ name: String) -> ImageInfo {
        if let cached = imageCache.get(name) {
            print("Cache HIT for '\(name)'")
            return cached
        }
        
        print("Cache MISS for '\(name)'")
        let image = loadImage(name)
        imageCache.set(name, value: image)
        return image
    }
    
    // First access - cache miss
    _ = getImage("photo1.jpg")
    
    // Second access - cache hit
    _ = getImage("photo1.jpg")
    
    // Fill up the cache
    _ = getImage("photo2.jpg")
    _ = getImage("photo3.jpg")
    _ = getImage("photo4.jpg")
    _ = getImage("photo5.jpg")
    
    print("\nCache filled with 5 images")
    
    // This will cause eviction
    _ = getImage("photo6.jpg")
    print("\nAdded 6th image, oldest should be evicted")
    print("'photo1.jpg' in cache: \(imageCache.contains("photo1.jpg"))")
    print()
}

// Example 5: API Response Cache
func apiResponseCacheExample() {
    print("=== Example 5: API Response Cache ===")
    
    struct APIResponse: Codable {
        let endpoint: String
        let data: String
        let timestamp: Date
    }
    
    let apiCache = LRUCache<String, APIResponse>(capacity: 50, defaultTTL: 300)  // 5 minutes
    
    func fetchAPI(_ endpoint: String) -> APIResponse {
        // Check cache first
        if let cached = apiCache.get(endpoint) {
            print("Using cached response for '\(endpoint)'")
            return cached
        }
        
        // Simulate API call
        print("Fetching from API: \(endpoint)")
        let response = APIResponse(
            endpoint: endpoint,
            data: "Response data for \(endpoint)",
            timestamp: Date()
        )
        
        apiCache.set(endpoint, value: response)
        return response
    }
    
    // First call - cache miss
    _ = fetchAPI("/users")
    
    // Second call - cache hit
    _ = fetchAPI("/users")
    
    // Different endpoint
    _ = fetchAPI("/products")
    
    print("\nCache stats:")
    print("  Count: \(apiCache.count)")
    print("  Keys: \(apiCache.keys)")
    print()
}

// Example 6: Subscript Syntax
func subscriptExample() {
    print("=== Example 6: Subscript Syntax ===")
    
    let cache = LRUCache<String, Double>(capacity: 3)
    
    // Set using subscript
    cache["pi"] = 3.14159
    cache["e"] = 2.71828
    cache["phi"] = 1.61803
    
    // Get using subscript
    print("pi = \(cache["pi"] ?? 0)")
    print("e = \(cache["e"] ?? 0)")
    
    // Remove using nil
    cache["e"] = nil
    print("After removing 'e': \(cache.keys)")
    print()
}

// Example 7: Iteration and Inspection
func iterationExample() {
    print("=== Example 7: Iteration and Inspection ===")
    
    let cache = LRUCache<String, Int>(capacity: 5)
    
    cache.set("a", value: 1)
    cache.set("b", value: 2)
    cache.set("c", value: 3)
    
    print("Iterating over cache (MRU to LRU):")
    for (key, value) in cache {
        print("  \(key): \(value)")
    }
    
    print("\nAll keys: \(cache.keys)")
    print("All values (MRU to LRU): \(cache.values)")
    print("Least recently used: \(cache.getLRUKey() ?? "empty")")
    print("Most recently used: \(cache.getMRUKey() ?? "empty")")
    print()
}

// Example 8: Session Management
func sessionManagementExample() {
    print("=== Example 8: Session Management ===")
    
    struct UserSession {
        let userId: String
        let username: String
        let loginTime: Date
        var lastActivity: Date
        
        mutating func touch() {
            lastActivity = Date()
        }
    }
    
    let sessionCache = LRUCache<String, UserSession>(capacity: 100, defaultTTL: 3600)  // 1 hour
    
    func login(userId: String, username: String) {
        let session = UserSession(
            userId: userId,
            username: username,
            loginTime: Date(),
            lastActivity: Date()
        )
        sessionCache.set(userId, value: session)
        print("User '\(username)' logged in")
    }
    
    func activity(userId: String) -> Bool {
        guard var session = sessionCache.get(userId) else {
            print("Session expired or not found")
            return false
        }
        
        session.touch()
        sessionCache.set(userId, value: session)
        print("Activity recorded for '\(session.username)'")
        return true
    }
    
    func logout(userId: String) {
        if let session = sessionCache.remove(userId) {
            print("User '\(session.username)' logged out")
        }
    }
    
    // Simulate user activity
    login(userId: "user123", username: "Alice")
    activity(userId: "user123")
    logout(userId: "user123")
    print()
}

// Example 9: Memory-Conscious Caching
func memoryConsciousExample() {
    print("=== Example 9: Memory-Conscious Caching ===")
    
    struct CachedData {
        let content: Data
        let sizeInBytes: Int
    }
    
    // Cache that tracks memory usage
    class MemoryAwareCache<Key: Hashable> {
        private var cache: LRUCache<Key, CachedData>
        private var totalBytes: Int = 0
        private let maxBytes: Int
        
        init(itemCapacity: Int, maxMemoryBytes: Int) {
            self.cache = LRUCache<Key, CachedData>(capacity: itemCapacity)
            self.maxBytes = maxMemoryBytes
        }
        
        func set(_ key: Key, data: Data) {
            let cachedData = CachedData(content: data, sizeInBytes: data.count)
            
            // Remove old entry if updating
            if let existing = cache.peek(key) {
                totalBytes -= existing.sizeInBytes
            }
            
            // Evict if over memory limit
            while totalBytes + data.count > maxBytes, let lruKey = cache.getLRUKey() {
                if let removed = cache.remove(lruKey) {
                    totalBytes -= removed.sizeInBytes
                    print("Evicted '\(lruKey)' to free memory")
                }
            }
            
            cache.set(key, value: cachedData)
            totalBytes += data.count
            
            print("Cached '\(key)': \(data.count) bytes (total: \(totalBytes) bytes)")
        }
        
        func get(_ key: Key) -> Data? {
            return cache.get(key)?.content
        }
        
        var memoryUsage: Int { totalBytes }
    }
    
    let memCache = MemoryAwareCache<String>(itemCapacity: 10, maxMemoryBytes: 1000)
    
    memCache.set("item1", data: Data(repeating: 0, count: 300))
    memCache.set("item2", data: Data(repeating: 0, count: 400))
    memCache.set("item3", data: Data(repeating: 0, count: 400))  // Should trigger eviction
    print()
}

// Example 10: Codable Persistence
func codablePersistenceExample() {
    print("=== Example 10: Codable Persistence ===")
    
    // Create and populate cache
    let cache = LRUCache<String, Int>(capacity: 5)
    cache.set("a", value: 1)
    cache.set("b", value: 2)
    cache.set("c", value: 3)
    
    // Encode to JSON
    do {
        let encoder = JSONEncoder()
        encoder.outputFormatting = .prettyPrinted
        let jsonData = try encoder.encode(cache)
        let jsonString = String(data: jsonData, encoding: .utf8)
        print("Cache as JSON:")
        print(jsonString ?? "")
        
        // Decode back
        let decoder = JSONDecoder()
        let restored = try decoder.decode(LRUCache<String, Int>.self, from: jsonData)
        print("\nRestored cache:")
        print("  Count: \(restored.count)")
        print("  Contents: \(restored.keys)")
    } catch {
        print("Error: \(error)")
    }
    print()
}

// Run all examples
func runAllExamples() {
    print("LRU Cache Examples\n")
    print("========================================\n")
    
    basicUsageExample()
    evictionExample()
    ttlExample()
    imageCacheExample()
    apiResponseCacheExample()
    subscriptExample()
    iterationExample()
    sessionManagementExample()
    memoryConsciousExample()
    codablePersistenceExample()
    
    print("========================================")
    print("All examples completed!")
}

// Run
runAllExamples()
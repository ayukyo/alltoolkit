/**
 * LRU Cache - A Least Recently Used Cache Implementation
 * 
 * A thread-safe, generic LRU (Least Recently Used) cache that automatically
 * evicts the least recently accessed items when the cache reaches its capacity.
 * 
 * Features:
 * - Generic key-value types (Hashable & Equatable)
 * - O(1) average time complexity for get/set operations
 * - Thread-safe with NSLock
 * - Automatic eviction when capacity is reached
 * - Optional expiration time support
 * 
 * Time Complexity:
 * - get(): O(1) average
 * - set(): O(1) average
 * - contains(): O(1) average
 * 
 * Space Complexity: O(n) where n is the capacity
 * 
 * Author: AllToolkit
 * Date: 2026-05-27
 */

import Foundation

/// A doubly linked list node for LRU tracking
fileprivate final class LRUNode<Key, Value> {
    var key: Key
    var value: Value
    var prev: LRUNode?
    var next: LRUNode?
    var expirationTime: Date?
    
    init(key: Key, value: Value, expirationTime: Date? = nil) {
        self.key = key
        self.value = value
        self.expirationTime = expirationTime
    }
}

/// A thread-safe LRU Cache implementation
public final class LRUCache<Key: Hashable, Value> {
    
    // MARK: - Properties
    
    private let capacity: Int
    private var cache: [Key: LRUNode<Key, Value>] = [:]
    private let head: LRUNode<Key, Value>  // Most recently used
    private let tail: LRUNode<Key, Value>  // Least recently used
    private let lock = NSLock()
    private let defaultTTL: TimeInterval?  // Default time-to-live in seconds
    
    /// Current number of items in the cache
    public var count: Int {
        lock.lock()
        defer { lock.unlock() }
        return cache.count
    }
    
    /// Whether the cache is empty
    public var isEmpty: Bool {
        return count == 0
    }
    
    /// All keys currently in the cache
    public var keys: [Key] {
        lock.lock()
        defer { lock.unlock() }
        return Array(cache.keys)
    }
    
    /// All values currently in the cache (most to least recently used)
    public var values: [Value] {
        lock.lock()
        defer { lock.unlock() }
        var result: [Value] = []
        var node = head.next
        while node !== tail {
            result.append(node!.value)
            node = node!.next
        }
        return result
    }
    
    // MARK: - Initialization
    
    /// Creates an LRU cache with the specified capacity
    /// - Parameters:
    ///   - capacity: Maximum number of items to store (must be > 0)
    ///   - defaultTTL: Default time-to-live for items in seconds (optional)
    public init(capacity: Int, defaultTTL: TimeInterval? = nil) {
        precondition(capacity > 0, "Capacity must be greater than 0")
        self.capacity = capacity
        self.defaultTTL = defaultTTL
        
        // Create dummy head and tail nodes
        head = LRUNode(key: Key()!, value: Value()!)
        tail = LRUNode(key: Key()!, value: Value()!)
        head.next = tail
        tail.prev = head
    }
    
    // MARK: - Public Methods
    
    /// Retrieves a value by key, updating its position to most recently used
    /// - Parameter key: The key to look up
    /// - Returns: The value if found and not expired, nil otherwise
    public func get(_ key: Key) -> Value? {
        lock.lock()
        defer { lock.unlock() }
        
        guard let node = cache[key] else {
            return nil
        }
        
        // Check expiration
        if let expTime = node.expirationTime, expTime < Date() {
            removeNode(node)
            cache.removeValue(forKey: key)
            return nil
        }
        
        // Move to front (most recently used)
        moveToHead(node)
        return node.value
    }
    
    /// Sets a value for a key, potentially evicting the least recently used item
    /// - Parameters:
    ///   - key: The key to set
    ///   - value: The value to store
    ///   - ttl: Time-to-live in seconds (overrides defaultTTL)
    public func set(_ key: Key, value: Value, ttl: TimeInterval? = nil) {
        lock.lock()
        defer { lock.unlock() }
        
        let effectiveTTL = ttl ?? defaultTTL
        let expirationTime = effectiveTTL.map { Date().addingTimeInterval($0) }
        
        if let node = cache[key] {
            // Update existing node
            node.value = value
            node.expirationTime = expirationTime
            moveToHead(node)
        } else {
            // Create new node
            let newNode = LRUNode(key: key, value: value, expirationTime: expirationTime)
            cache[key] = newNode
            addToHead(newNode)
            
            // Evict if over capacity
            if cache.count > capacity {
                if let lru = tail.prev, lru !== head {
                    removeNode(lru)
                    cache.removeValue(forKey: lru.key)
                }
            }
        }
    }
    
    /// Checks if a key exists in the cache without updating its position
    /// - Parameter key: The key to check
    /// - Returns: true if the key exists and is not expired
    public func contains(_ key: Key) -> Bool {
        lock.lock()
        defer { lock.unlock() }
        
        guard let node = cache[key] else {
            return false
        }
        
        // Check expiration
        if let expTime = node.expirationTime, expTime < Date() {
            return false
        }
        
        return true
    }
    
    /// Removes a key from the cache
    /// - Parameter key: The key to remove
    /// - Returns: The removed value, or nil if not found
    @discardableResult
    public func remove(_ key: Key) -> Value? {
        lock.lock()
        defer { lock.unlock() }
        
        guard let node = cache.removeValue(forKey: key) else {
            return nil
        }
        removeNode(node)
        return node.value
    }
    
    /// Clears all items from the cache
    public func clear() {
        lock.lock()
        defer { lock.unlock() }
        
        cache.removeAll()
        head.next = tail
        tail.prev = head
    }
    
    /// Gets a value without updating its LRU position
    /// - Parameter key: The key to look up
    /// - Returns: The value if found and not expired, nil otherwise
    public func peek(_ key: Key) -> Value? {
        lock.lock()
        defer { lock.unlock() }
        
        guard let node = cache[key] else {
            return nil
        }
        
        // Check expiration
        if let expTime = node.expirationTime, expTime < Date() {
            return nil
        }
        
        return node.value
    }
    
    /// Removes all expired items from the cache
    /// - Returns: Number of items removed
    @discardableResult
    public func removeExpired() -> Int {
        lock.lock()
        defer { lock.unlock() }
        
        var removed = 0
        let now = Date()
        
        for (key, node) in cache {
            if let expTime = node.expirationTime, expTime < now {
                removeNode(node)
                cache.removeValue(forKey: key)
                removed += 1
            }
        }
        
        return removed
    }
    
    /// Gets the least recently used key
    /// - Returns: The LRU key, or nil if cache is empty
    public func getLRUKey() -> Key? {
        lock.lock()
        defer { lock.unlock() }
        
        guard tail.prev !== head else {
            return nil
        }
        return tail.prev?.key
    }
    
    /// Gets the most recently used key
    /// - Returns: The MRU key, or nil if cache is empty
    public func getMRUKey() -> Key? {
        lock.lock()
        defer { lock.unlock() }
        
        guard head.next !== tail else {
            return nil
        }
        return head.next?.key
    }
    
    // MARK: - Private Helper Methods
    
    private func addToHead(_ node: LRUNode<Key, Value>) {
        node.prev = head
        node.next = head.next
        head.next?.prev = node
        head.next = node
    }
    
    private func removeNode(_ node: LRUNode<Key, Value>) {
        node.prev?.next = node.next
        node.next?.prev = node.prev
    }
    
    private func moveToHead(_ node: LRUNode<Key, Value>) {
        removeNode(node)
        addToHead(node)
    }
}

// MARK: - Convenience Initializers

extension LRUCache {
    /// Creates an LRU cache with a default capacity of 100
    public convenience init() {
        self.init(capacity: 100)
    }
}

// MARK: - Sequence Conformance

extension LRUCache: Sequence {
    public typealias Element = (key: Key, value: Value)
    
    public func makeIterator() -> AnyIterator<Element> {
        var node = head.next
        return AnyIterator {
            guard node !== self.tail, let current = node else {
                return nil
            }
            node = current.next
            return (key: current.key, value: current.value)
        }
    }
}

// MARK: - CustomStringConvertible

extension LRUCache: CustomStringConvertible {
    public var description: String {
        return "LRUCache<\(Key.self), \(Value.self)>(capacity: \(capacity), count: \(count))"
    }
}

// MARK: - Codable Support (when Key and Value are Codable)

extension LRUCache: Codable where Key: Codable, Value: Codable {
    enum CodingKeys: String, CodingKey {
        case capacity
        case items
        case defaultTTL
    }
    
    public convenience init(from decoder: Decoder) throws {
        let container = try decoder.container(keyedBy: CodingKeys.self)
        let capacity = try container.decode(Int.self, forKey: .capacity)
        let items = try container.decode([(key: Key, value: Value)].self, forKey: .items)
        let defaultTTL = try container.decodeIfPresent(TimeInterval.self, forKey: .defaultTTL)
        
        self.init(capacity: capacity, defaultTTL: defaultTTL)
        
        // Insert items in order (first item becomes LRU)
        for item in items {
            set(item.key, value: item.value)
        }
    }
    
    public func encode(to encoder: Encoder) throws {
        var container = encoder.container(keyedBy: CodingKeys.self)
        try container.encode(capacity, forKey: .capacity)
        try container.encode(Array(self), forKey: .items)
        try container.encodeIfPresent(defaultTTL, forKey: .defaultTTL)
    }
}

// MARK: - Operator Overloads

extension LRUCache {
    /// Subscript access for get/set operations
    public subscript(key: Key) -> Value? {
        get { return get(key) }
        set {
            if let value = newValue {
                set(key, value: value)
            } else {
                remove(key)
            }
        }
    }
}
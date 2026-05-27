/**
 * LRU Cache Tests
 * 
 * Comprehensive test suite for LRUCache implementation
 * 
 * Author: AllToolkit
 * Date: 2026-05-27
 */

import XCTest
@testable import LRUCache

final class LRUCacheTests: XCTestCase {
    
    // MARK: - Basic Operations Tests
    
    func testBasicSetAndGet() {
        let cache = LRUCache<String, Int>(capacity: 3)
        
        cache.set("a", value: 1)
        cache.set("b", value: 2)
        cache.set("c", value: 3)
        
        XCTAssertEqual(cache.get("a"), 1)
        XCTAssertEqual(cache.get("b"), 2)
        XCTAssertEqual(cache.get("c"), 3)
        XCTAssertEqual(cache.count, 3)
    }
    
    func testSubscriptAccess() {
        let cache = LRUCache<String, Int>(capacity: 3)
        
        cache["a"] = 1
        cache["b"] = 2
        
        XCTAssertEqual(cache["a"], 1)
        XCTAssertEqual(cache["b"], 2)
        XCTAssertNil(cache["c"])
        
        cache["a"] = nil
        XCTAssertNil(cache["a"])
        XCTAssertEqual(cache.count, 1)
    }
    
    func testUpdateExistingKey() {
        let cache = LRUCache<String, Int>(capacity: 3)
        
        cache.set("a", value: 1)
        cache.set("a", value: 2)
        cache.set("a", value: 3)
        
        XCTAssertEqual(cache.count, 1)
        XCTAssertEqual(cache.get("a"), 3)
    }
    
    // MARK: - Eviction Tests
    
    func testEvictionOrder() {
        let cache = LRUCache<String, Int>(capacity: 3)
        
        cache.set("a", value: 1)  // [a]
        cache.set("b", value: 2)  // [b, a]
        cache.set("c", value: 3)  // [c, b, a]
        cache.set("d", value: 4)  // [d, c, b] - a is evicted
        
        XCTAssertNil(cache.get("a"))  // Should be evicted
        XCTAssertEqual(cache.get("b"), 2)
        XCTAssertEqual(cache.get("c"), 3)
        XCTAssertEqual(cache.get("d"), 4)
    }
    
    func testLRUOrderOnAccess() {
        let cache = LRUCache<String, Int>(capacity: 3)
        
        cache.set("a", value: 1)
        cache.set("b", value: 2)
        cache.set("c", value: 3)
        
        // Access "a" to make it most recently used
        _ = cache.get("a")  // Order: [a, c, b]
        
        // Add new item, "b" should be evicted (least recently used)
        cache.set("d", value: 4)  // [d, a, c]
        
        XCTAssertNil(cache.get("b"))
        XCTAssertEqual(cache.get("a"), 1)
        XCTAssertEqual(cache.get("c"), 3)
        XCTAssertEqual(cache.get("d"), 4)
    }
    
    func testEvictionWithSameCapacity() {
        let cache = LRUCache<Int, String>(capacity: 2)
        
        cache.set(1, value: "one")
        cache.set(2, value: "two")
        cache.set(3, value: "three")  // 1 is evicted
        
        XCTAssertNil(cache.get(1))
        XCTAssertEqual(cache.get(2), "two")
        XCTAssertEqual(cache.get(3), "three")
    }
    
    // MARK: - Removal Tests
    
    func testRemoveExistingKey() {
        let cache = LRUCache<String, Int>(capacity: 3)
        
        cache.set("a", value: 1)
        cache.set("b", value: 2)
        
        let removed = cache.remove("a")
        
        XCTAssertEqual(removed, 1)
        XCTAssertNil(cache.get("a"))
        XCTAssertEqual(cache.count, 1)
    }
    
    func testRemoveNonExistingKey() {
        let cache = LRUCache<String, Int>(capacity: 3)
        
        cache.set("a", value: 1)
        let removed = cache.remove("nonexistent")
        
        XCTAssertNil(removed)
        XCTAssertEqual(cache.count, 1)
    }
    
    func testClear() {
        let cache = LRUCache<String, Int>(capacity: 3)
        
        cache.set("a", value: 1)
        cache.set("b", value: 2)
        cache.set("c", value: 3)
        cache.clear()
        
        XCTAssertEqual(cache.count, 0)
        XCTAssertTrue(cache.isEmpty)
        XCTAssertNil(cache.get("a"))
    }
    
    // MARK: - Contains and Peek Tests
    
    func testContains() {
        let cache = LRUCache<String, Int>(capacity: 3)
        
        cache.set("a", value: 1)
        
        XCTAssertTrue(cache.contains("a"))
        XCTAssertFalse(cache.contains("b"))
    }
    
    func testPeekDoesNotUpdateLRU() {
        let cache = LRUCache<String, Int>(capacity: 2)
        
        cache.set("a", value: 1)
        cache.set("b", value: 2)
        
        // Peek "a" without updating its position
        XCTAssertEqual(cache.peek("a"), 1)
        
        // Add new item, "a" should be evicted (since peek didn't update position)
        cache.set("c", value: 3)
        
        XCTAssertNil(cache.get("a"))
        XCTAssertEqual(cache.get("b"), 2)
        XCTAssertEqual(cache.get("c"), 3)
    }
    
    // MARK: - TTL Tests
    
    func testItemExpiration() {
        let cache = LRUCache<String, Int>(capacity: 3, defaultTTL: 0.1)  // 100ms TTL
        
        cache.set("a", value: 1)
        
        // Should exist immediately
        XCTAssertEqual(cache.get("a"), 1)
        
        // Wait for expiration
        let expectation = XCTestExpectation()
        DispatchQueue.main.asyncAfter(deadline: .now() + 0.2) {
            XCTAssertNil(cache.get("a"))
            expectation.fulfill()
        }
        
        wait(for: [expectation], timeout: 1.0)
    }
    
    func testCustomTTL() {
        let cache = LRUCache<String, Int>(capacity: 3)
        
        cache.set("a", value: 1, ttl: 0.1)  // 100ms TTL
        cache.set("b", value: 2)  // No expiration
        
        let expectation = XCTestExpectation()
        DispatchQueue.main.asyncAfter(deadline: .now() + 0.2) {
            XCTAssertNil(cache.get("a"))
            XCTAssertEqual(cache.get("b"), 2)
            expectation.fulfill()
        }
        
        wait(for: [expectation], timeout: 1.0)
    }
    
    func testContainsWithExpiredItem() {
        let cache = LRUCache<String, Int>(capacity: 3, defaultTTL: 0.1)
        
        cache.set("a", value: 1)
        
        XCTAssertTrue(cache.contains("a"))
        
        let expectation = XCTestExpectation()
        DispatchQueue.main.asyncAfter(deadline: .now() + 0.2) {
            XCTAssertFalse(cache.contains("a"))
            expectation.fulfill()
        }
        
        wait(for: [expectation], timeout: 1.0)
    }
    
    func testRemoveExpired() {
        let cache = LRUCache<String, Int>(capacity: 3, defaultTTL: 0.1)
        
        cache.set("a", value: 1)
        cache.set("b", value: 2, ttl: 10)  // Long TTL
        cache.set("c", value: 3)
        
        let expectation = XCTestExpectation()
        DispatchQueue.main.asyncAfter(deadline: .now() + 0.2) {
            let removed = cache.removeExpired()
            XCTAssertEqual(removed, 2)  // "a" and "c" expired
            XCTAssertEqual(cache.count, 1)
            XCTAssertEqual(cache.get("b"), 2)
            expectation.fulfill()
        }
        
        wait(for: [expectation], timeout: 1.0)
    }
    
    // MARK: - LRU/MRU Key Tests
    
    func testGetLRUKey() {
        let cache = LRUCache<String, Int>(capacity: 3)
        
        XCTAssertNil(cache.getLRUKey())
        
        cache.set("a", value: 1)
        cache.set("b", value: 2)
        cache.set("c", value: 3)
        
        // "a" is least recently used
        XCTAssertEqual(cache.getLRUKey(), "a")
        
        // Access "a" to make it most recently used
        _ = cache.get("a")
        
        // Now "b" is least recently used
        XCTAssertEqual(cache.getLRUKey(), "b")
    }
    
    func testGetMRUKey() {
        let cache = LRUCache<String, Int>(capacity: 3)
        
        XCTAssertNil(cache.getMRUKey())
        
        cache.set("a", value: 1)
        XCTAssertEqual(cache.getMRUKey(), "a")
        
        cache.set("b", value: 2)
        XCTAssertEqual(cache.getMRUKey(), "b")
        
        _ = cache.get("a")
        XCTAssertEqual(cache.getMRUKey(), "a")
    }
    
    // MARK: - Collection Properties Tests
    
    func testKeys() {
        let cache = LRUCache<String, Int>(capacity: 3)
        
        cache.set("a", value: 1)
        cache.set("b", value: 2)
        cache.set("c", value: 3)
        
        let keys = Set(cache.keys)
        XCTAssertEqual(keys, Set(["a", "b", "c"]))
    }
    
    func testValues() {
        let cache = LRUCache<String, Int>(capacity: 3)
        
        cache.set("a", value: 1)
        cache.set("b", value: 2)
        cache.set("c", value: 3)
        
        // Values should be in MRU to LRU order
        XCTAssertEqual(cache.values, [3, 2, 1])
        
        _ = cache.get("a")
        XCTAssertEqual(cache.values, [1, 3, 2])
    }
    
    func testSequenceIteration() {
        let cache = LRUCache<String, Int>(capacity: 3)
        
        cache.set("a", value: 1)
        cache.set("b", value: 2)
        cache.set("c", value: 3)
        
        var items: [(key: String, value: Int)] = []
        for (key, value) in cache {
            items.append((key: key, value: value))
        }
        
        XCTAssertEqual(items.count, 3)
        XCTAssertEqual(items[0].key, "c")
        XCTAssertEqual(items[0].value, 3)
    }
    
    // MARK: - Edge Cases Tests
    
    func testCapacityOne() {
        let cache = LRUCache<String, Int>(capacity: 1)
        
        cache.set("a", value: 1)
        XCTAssertEqual(cache.get("a"), 1)
        
        cache.set("b", value: 2)
        XCTAssertNil(cache.get("a"))
        XCTAssertEqual(cache.get("b"), 2)
    }
    
    func testEmptyCache() {
        let cache = LRUCache<String, Int>(capacity: 3)
        
        XCTAssertTrue(cache.isEmpty)
        XCTAssertEqual(cache.count, 0)
        XCTAssertNil(cache.get("nonexistent"))
        XCTAssertNil(cache.remove("nonexistent"))
        XCTAssertNil(cache.getLRUKey())
        XCTAssertNil(cache.getMRUKey())
    }
    
    func testLargeCapacity() {
        let cache = LRUCache<Int, Int>(capacity: 1000)
        
        for i in 0..<1000 {
            cache.set(i, value: i * 2)
        }
        
        XCTAssertEqual(cache.count, 1000)
        
        for i in 0..<1000 {
            XCTAssertEqual(cache.get(i), i * 2)
        }
    }
    
    // MARK: - Description Tests
    
    func testDescription() {
        let cache = LRUCache<String, Int>(capacity: 3)
        
        let description = cache.description
        XCTAssertTrue(description.contains("LRUCache"))
        XCTAssertTrue(description.contains("capacity: 3"))
        XCTAssertTrue(description.contains("count: 0"))
    }
    
    // MARK: - Thread Safety Tests
    
    func testConcurrentAccess() {
        let cache = LRUCache<Int, Int>(capacity: 100)
        let iterations = 1000
        let queue = DispatchQueue.global(qos: .userInitiated)
        let group = DispatchGroup()
        
        // Concurrent writes
        for i in 0..<iterations {
            group.enter()
            queue.async {
                cache.set(i, value: i * 2)
                group.leave()
            }
        }
        
        // Concurrent reads
        for i in 0..<iterations {
            group.enter()
            queue.async {
                _ = cache.get(i)
                group.leave()
            }
        }
        
        group.wait()
        
        // Cache should still be in valid state
        XCTAssertLessThanOrEqual(cache.count, 100)
    }
}

// MARK: - Codable Tests

final class LRUCacheCodableTests: XCTestCase {
    
    struct TestKey: Codable, Hashable {
        let id: Int
        let name: String
    }
    
    func testCodableRoundTrip() throws {
        let cache = LRUCache<String, Int>(capacity: 3)
        cache.set("a", value: 1)
        cache.set("b", value: 2)
        cache.set("c", value: 3)
        
        let encoder = JSONEncoder()
        let data = try encoder.encode(cache)
        
        let decoder = JSONDecoder()
        let decoded = try decoder.decode(LRUCache<String, Int>.self, from: data)
        
        XCTAssertEqual(decoded.count, 3)
        XCTAssertEqual(decoded.get("a"), 1)
        XCTAssertEqual(decoded.get("b"), 2)
        XCTAssertEqual(decoded.get("c"), 3)
    }
    
    func testCodableWithComplexTypes() throws {
        let cache = LRUCache<TestKey, [String: Int]>(capacity: 5)
        cache.set(TestKey(id: 1, name: "first"), value: ["value": 100])
        cache.set(TestKey(id: 2, name: "second"), value: ["value": 200])
        
        let encoder = JSONEncoder()
        let data = try encoder.encode(cache)
        
        let decoder = JSONDecoder()
        let decoded = try decoder.decode(LRUCache<TestKey, [String: Int]>.self, from: data)
        
        XCTAssertEqual(decoded.count, 2)
        let result = decoded.get(TestKey(id: 1, name: "first"))
        XCTAssertEqual(result?["value"], 100)
    }
    
    func testCodablePreservesTTL() throws {
        let cache = LRUCache<String, Int>(capacity: 3, defaultTTL: 60)
        cache.set("a", value: 1)
        
        let encoder = JSONEncoder()
        let data = try encoder.encode(cache)
        
        let json = try JSONSerialization.jsonObject(with: data) as? [String: Any]
        XCTAssertEqual(json?["defaultTTL"] as? TimeInterval, 60)
    }
}
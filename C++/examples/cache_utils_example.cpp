/**
 * @file cache_utils_example.cpp
 * @brief Example usage of Cache Utilities
 * @version 1.0.0
 *
 * This file demonstrates various features of the Cache Utilities library:
 * - Basic cache operations
 * - TTL (Time To Live) expiration
 * - LRU eviction policy
 * - Statistics tracking
 * - Get or compute pattern
 * - Thread-safe operations
 */

#include <iostream>
#include <string>
#include <chrono>
#include <thread>
#include <vector>
#include "../cache_utils/mod.hpp"

using namespace alltoolkit;

// Example 1: Basic cache usage
void example_basic_usage() {
    std::cout << "\n=== Example 1: Basic Cache Usage ===" << std::endl;

    Cache<std::string, std::string> cache(100);

    // Store values
    cache.set("name", "Alice");
    cache.set("city", "New York");
    cache.set("country", "USA");

    // Retrieve values
    std::string value;
    if (cache.get("name", value)) {
        std::cout << "Name: " << value << std::endl;
    }

    if (cache.get("city", value)) {
        std::cout << "City: " << value << std::endl;
    }

    // Check if key exists
    std::cout << "Has 'name': " << (cache.has("name") ? "yes" : "no") << std::endl;
    std::cout << "Has 'age': " << (cache.has("age") ? "yes" : "no") << std::endl;

    // Remove a key
    cache.remove("city");
    std::cout << "After removal, has 'city': " << (cache.has("city") ? "yes" : "no") << std::endl;

    // Get with default
    std::string age = cache.get_or_default("age", std::string("unknown"));
    std::cout << "Age (with default): " << age << std::endl;
}

// Example 2: TTL (Time To Live)
void example_ttl() {
    std::cout << "\n=== Example 2: TTL (Time To Live) ===" << std::endl;

    Cache<std::string, std::string> cache(100);

    // Set with 2 second TTL
    cache.set("session_token", "abc123", 2);
    std::cout << "Session token set with 2 second TTL" << std::endl;
    std::cout << "Has token: " << (cache.has("session_token") ? "yes" : "no") << std::endl;

    // Wait for expiration
    std::cout << "Waiting 2.5 seconds..." << std::endl;
    std::this_thread::sleep_for(std::chrono::milliseconds(2500));

    std::cout << "Has token after wait: " << (cache.has("session_token") ? "yes" : "no") << std::endl;

    // Permanent entry (no TTL)
    cache.set("config", "app_settings");
    std::cout << "Permanent config entry: " << (cache.has("config") ? "yes" : "no") << std::endl;
}

// Example 3: LRU Eviction
void example_lru_eviction() {
    std::cout << "\n=== Example 3: LRU Eviction Policy ===" << std::endl;

    // Cache with max 3 entries, LRU eviction
    Cache<std::string, int> cache(3, EvictionPolicy::LRU);

    cache.set("a", 1);
    cache.set("b", 2);
    cache.set("c", 3);
    std::cout << "Added a, b, c. Size: " << cache.size() << std::endl;

    // Access 'a' to make it most recently used
    int val;
    cache.get("a", val);
    std::cout << "Accessed 'a'" << std::endl;

    // Add new entry - 'b' should be evicted (least recently used)
    cache.set("d", 4);
    std::cout << "Added 'd'. Size: " << cache.size() << std::endl;

    std::cout << "Has 'a': " << (cache.has("a") ? "yes" : "no") << std::endl;
    std::cout << "Has 'b': " << (cache.has("b") ? "yes" : "no") << " (evicted)" << std::endl;
    std::cout << "Has 'c': " << (cache.has("c") ? "yes" : "no") << std::endl;
    std::cout << "Has 'd': " << (cache.has("d") ? "yes" : "no") << std::endl;
}

// Example 4: Statistics tracking
void example_statistics() {
    std::cout << "\n=== Example 4: Statistics Tracking ===" << std::endl;

    Cache<std::string, int> cache(100);

    // Initial stats
    CacheStats stats = cache.stats();
    std::cout << "Initial - Hits: " << stats.hits << ", Misses: " << stats.misses << std::endl;

    // Some misses
    int val;
    cache.get("missing1", val);
    cache.get("missing2", val);

    // Add and hit
    cache.set("key1", 100);
    cache.get("key1", val);
    cache.get("key1", val);

    stats = cache.stats();
    std::cout << "After operations - Hits: " << stats.hits << ", Misses: " << stats.misses << std::endl;
    std::cout << "Hit rate: " << (stats.hit_rate() * 100) << "%" << std::endl;

    // Reset stats
    cache.reset_stats();
    stats = cache.stats();
    std::cout << "After reset - Hits: " << stats.hits << ", Misses: " << stats.misses << std::endl;
}

// Example 5: Get or compute pattern
void example_get_or_compute() {
    std::cout << "\n=== Example 5: Get or Compute Pattern ===" << std::endl;

    Cache<std::string, int> cache(100);

    int compute_count = 0;

    // Function to simulate expensive computation
    // First call - should compute
    std::cout << "First call for 'hello':" << std::endl;
    int val1 = cache.get_or_compute("hello", [&]() {
        compute_count++;
        std::cout << "  Computing value..." << std::endl;
        return 42;
    });
    std::cout << "Value: " << val1 << std::endl;

    // Second call - should use cache
    std::cout << "Second call for 'hello':" << std::endl;
    int val2 = cache.get_or_compute("hello", [&]() {
        compute_count++;
        std::cout << "  Computing value..." << std::endl;
        return 42;
    });
    std::cout << "Value: " << val2 << std::endl;

    std::cout << "Total computations: " << compute_count << std::endl;
}

// Example 6: Different eviction policies
void example_eviction_policies() {
    std::cout << "\n=== Example 6: Eviction Policies ===" << std::endl;

    // FIFO cache
    {
        std::cout << "\nFIFO Policy:" << std::endl;
        Cache<std::string, int> cache(3, EvictionPolicy::FIFO);

        cache.set("a", 1);
        cache.set("b", 2);
        cache.set("c", 3);
        int val;
        cache.get("a", val); // Access doesn't affect FIFO

        cache.set("d", 4); // Evicts 'a' (first in)

        std::cout << "  Has 'a': " << (cache.has("a") ? "yes" : "no") << std::endl;
        std::cout << "  Has 'b': " << (cache.has("b") ? "yes" : "no") << std::endl;
    }

    // LFU cache (Least Frequently Used)
    {
        std::cout << "\nLFU Policy:" << std::endl;
        Cache<std::string, int> cache(3, EvictionPolicy::LFU);

        cache.set("a", 1);
        cache.set("b", 2);
        cache.set("c", 3);

        // Access 'a' multiple times
        int val;
        cache.get("a", val);
        cache.get("a", val);
        cache.get("b", val);

        cache.set("d", 4); // Evicts 'c' (least frequently used)

        std::cout << "  Has 'a': " << (cache.has("a") ? "yes" : "no") << std::endl;
        std::cout << "  Has 'b': " << (cache.has("b") ? "yes" : "no") << std::endl;
        std::cout << "  Has 'c': " << (cache.has("c") ? "yes" : "no") << " (evicted)" << std::endl;
    }
}

// Example 7: Integer keys
void example_integer_keys() {
    std::cout << "\n=== Example 7: Integer Keys ===" << std::endl;

    Cache<int, std::string> cache(100);

    cache.set(1, "one");
    cache.set(2, "two");
    cache.set(3, "three");
    cache.set(100, "hundred");

    std::string val;
    if (cache.get(1, val)) std::cout << "Key 1: " << val << std::endl;
    if (cache.get(2, val)) std::cout << "Key 2: " << val << std::endl;
    if (cache.get(100, val)) std::cout << "Key 100: " << val << std::endl;

    std::vector<int> keys = cache.keys();
    std::cout << "All keys: ";
    for (size_t i = 0; i < keys.size(); i++) {
        std::cout << keys[i] << " ";
    }
    std::cout << std::endl;
}

// Example 8: Thread-safe operations
void example_thread_safety() {
    std::cout << "\n=== Example 8: Thread-Safe Operations ===" << std::endl;

    Cache<int, int> cache(1000);

    std::vector<std::thread> threads;

    // Writer threads
    for (int i = 0; i < 3; i++) {
        threads.push_back(std::thread([&cache, i]() {
            for (int j = 0; j < 50; j++) {
                cache.set(i * 100 + j, j * j);
            }
        }));
    }

    // Reader threads
    for (int i = 0; i < 2; i++) {
        threads.push_back(std::thread([&cache]() {
            int val;
            for (int j = 0; j < 100; j++) {
                cache.get(j, val);
            }
        }));
    }

    for (size_t i = 0; i < threads.size(); i++) {
        threads[i].join();
    }

    std::cout << "Final cache size after concurrent operations: " << cache.size() << std::endl;
    CacheStats stats = cache.stats();
    std::cout << "Hits: " << stats.hits << ", Misses: " << stats.misses << std::endl;
}

int main() {
    std::cout << "========================================" << std::endl;
    std::cout << "Cache Utilities Examples" << std::endl;
    std::cout << "========================================" << std::endl;

    example_basic_usage();
    example_ttl();
    example_lru_eviction();
    example_statistics();
    example_get_or_compute();
    example_eviction_policies();
    example_integer_keys();
    example_thread_safety();

    std::cout << "\n========================================" << std::endl;
    std::cout << "All examples completed successfully!" << std::endl;
    std::cout << "========================================" << std::endl;

    return 0;
}

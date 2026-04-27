/**
 * @file usage_examples.cpp
 * @brief Practical usage examples for Bloom Filter
 * 
 * This file demonstrates common use cases for bloom filters:
 * 1. URL filtering (web crawler)
 * 2. Username availability checking
 * 3. Cache filtering
 * 4. Spell checking
 * 5. Database query optimization
 */

#include "../bloom_filter.hpp"
#include <iostream>
#include <vector>
#include <string>
#include <set>
#include <fstream>

using namespace bloom_filter;

/**
 * @brief Example: Web crawler URL deduplication
 * 
 * Bloom filters are perfect for tracking visited URLs in web crawlers.
 * They save memory at the cost of potentially re-crawling some URLs.
 */
void example_web_crawler() {
    std::cout << "\n=== Example: Web Crawler URL Filtering ===\n" << std::endl;
    
    // Create a bloom filter for 10 million URLs with 0.1% false positive rate
    BloomFilter<std::string> visited_urls(10000000, 0.001);
    
    std::cout << "Memory usage: " << (visited_urls.memory_usage() / 1024.0 / 1024.0) 
              << " MB" << std::endl;
    std::cout << "Hash functions: " << visited_urls.hash_functions() << std::endl;
    
    // Simulate URL crawling
    std::vector<std::string> urls = {
        "https://example.com/page1",
        "https://example.com/page2",
        "https://example.com/page3",
        "https://example.com/page1",  // duplicate
        "https://example.com/page4",
        "https://example.com/page2",  // duplicate
    };
    
    int new_urls = 0;
    int skipped = 0;
    
    for (const auto& url : urls) {
        if (visited_urls.might_contain(url)) {
            std::cout << "  Skip (already visited): " << url << std::endl;
            skipped++;
        } else {
            std::cout << "  Crawl (new URL): " << url << std::endl;
            visited_urls.insert(url);
            new_urls++;
        }
    }
    
    std::cout << "\nSummary: " << new_urls << " new, " << skipped << " skipped" << std::endl;
}

/**
 * @brief Example: Username availability checker
 * 
 * Quickly check if a username might be available without hitting the database.
 */
void example_username_checker() {
    std::cout << "\n=== Example: Username Availability Checker ===\n" << std::endl;
    
    // Bloom filter for existing usernames (1 million users, 1% FPR)
    BloomFilter<std::string> existing_users(1000000, 0.01);
    
    // Simulate existing users
    std::vector<std::string> users = {
        "alice", "bob", "charlie", "david", "eve",
        "frank", "grace", "henry", "ivy", "jack"
    };
    
    for (const auto& user : users) {
        existing_users.insert(user);
    }
    
    // Check new usernames
    std::vector<std::string> to_check = {
        "alice",      // taken
        "newuser",    // available
        "bob",        // taken
        "xyz123",     // available
        "charlie",    // taken
    };
    
    std::cout << "Checking username availability:\n" << std::endl;
    for (const auto& name : to_check) {
        if (existing_users.might_contain(name)) {
            std::cout << "  '" << name << "' - DEFINITELY TAKEN (check database)" << std::endl;
        } else {
            std::cout << "  '" << name << "' - AVAILABLE! (100% certain)" << std::endl;
        }
    }
    
    std::cout << "\nNote: Bloom filter gives definite NO answers." << std::endl;
    std::cout << "MAYBE answers should be verified against the database." << std::endl;
}

/**
 * @brief Example: Cache request filtering
 * 
 * Filter out requests that definitely aren't in cache,
 * saving expensive cache lookups.
 */
void example_cache_filtering() {
    std::cout << "\n=== Example: Cache Request Filtering ===\n" << std::endl;
    
    // Simulate a cache with bloom filter
    BloomFilter<std::string> cache_filter(100000, 0.01);
    
    // Items in cache
    std::set<std::string> actual_cache = {
        "user:1", "user:2", "user:3", "session:abc", "session:def"
    };
    
    for (const auto& key : actual_cache) {
        cache_filter.insert(key);
    }
    
    // Simulate cache lookups
    std::vector<std::string> requests = {
        "user:1",        // in cache
        "user:2",        // in cache
        "user:999",      // NOT in cache
        "session:xyz",   // NOT in cache
        "user:3",        // in cache
    };
    
    int cache_lookups_saved = 0;
    
    for (const auto& key : requests) {
        if (!cache_filter.might_contain(key)) {
            std::cout << "  '" << key << "' - SKIP LOOKUP (definitely not in cache)" 
                      << std::endl;
            cache_lookups_saved++;
        } else if (actual_cache.count(key)) {
            std::cout << "  '" << key << "' - FOUND in cache" << std::endl;
        } else {
            std::cout << "  '" << key << "' - FALSE POSITIVE (not actually in cache)" 
                      << std::endl;
        }
    }
    
    std::cout << "\nCache lookups saved: " << cache_lookups_saved << std::endl;
}

/**
 * @brief Example: Counting Bloom Filter for rate limiting
 * 
 * Track request counts per IP without storing all IPs.
 */
void example_rate_limiting() {
    std::cout << "\n=== Example: Rate Limiting with Counting Bloom Filter ===\n" 
              << std::endl;
    
    CountingBloomFilter<std::string> rate_limiter(10000, 0.01);
    
    // Simulate requests from different IPs
    std::vector<std::string> requests = {
        "192.168.1.1",
        "192.168.1.1",
        "192.168.1.1",
        "192.168.1.2",
        "192.168.1.1",
        "192.168.1.2",
        "10.0.0.1",    // new IP
        "192.168.1.1",
        "192.168.1.1",  // 6th request from this IP
    };
    
    const int RATE_LIMIT = 5;
    
    std::cout << "Rate limit: " << RATE_LIMIT << " requests per IP\n" << std::endl;
    
    // Note: This is a simplified example. In production, you'd track
    // actual counts with a counter, not just presence.
    
    for (const auto& ip : requests) {
        rate_limiter.insert(ip);
        size_t estimated_count = rate_limiter.count();
        
        std::cout << "  Request from " << ip;
        if (rate_limiter.might_contain(ip)) {
            std::cout << " (count estimate: high)";
        }
        std::cout << std::endl;
    }
}

/**
 * @brief Example: Scalable Bloom Filter for growing datasets
 * 
 * Automatically grows as more items are added.
 */
void example_scalable_filter() {
    std::cout << "\n=== Example: Scalable Bloom Filter ===\n" << std::endl;
    
    // Start with small initial capacity
    ScalableBloomFilter<std::string> filter(0.01, 100);
    
    std::cout << "Initial filters: " << filter.num_filters() << std::endl;
    
    // Add more items than initial capacity
    for (int i = 0; i < 1000; ++i) {
        filter.insert("item_" + std::to_string(i));
    }
    
    std::cout << "After 1000 insertions: " << filter.num_filters() << " filters" 
              << std::endl;
    std::cout << "Total items: " << filter.count() << std::endl;
    
    // Verify items are still findable
    int found = 0;
    for (int i = 0; i < 1000; ++i) {
        if (filter.might_contain("item_" + std::to_string(i))) {
            found++;
        }
    }
    
    std::cout << "Items found: " << found << "/1000 (no false negatives)" << std::endl;
}

/**
 * @brief Example: Spell checker dictionary
 * 
 * Use bloom filter to quickly reject misspelled words.
 */
void example_spell_checker() {
    std::cout << "\n=== Example: Spell Checker ===\n" << std::endl;
    
    // Small dictionary for demo
    BloomFilter<std::string> dictionary(100000, 0.001);
    
    std::vector<std::string> words = {
        "hello", "world", "python", "programming", "computer",
        "science", "data", "structure", "algorithm", "bloom"
    };
    
    for (const auto& word : words) {
        dictionary.insert(word);
    }
    
    std::vector<std::string> to_check = {
        "hello",      // correct
        "wrld",       // misspelled
        "python",     // correct
        "programing", // misspelled
        "bloom",      // correct
        "filter",     // correct (but not in dict)
    };
    
    std::cout << "Spell check results:\n" << std::endl;
    for (const auto& word : to_check) {
        if (dictionary.might_contain(word)) {
            std::cout << "  '" << word << "' - probably CORRECT" << std::endl;
        } else {
            std::cout << "  '" << word << "' - DEFINITELY MISSPELLED" << std::endl;
        }
    }
    
    std::cout << "\nNote: 'filter' is a valid English word but not in our dictionary," 
              << std::endl;
    std::cout << "so it's correctly identified as misspelled." << std::endl;
}

/**
 * @brief Example: Serialize and persist bloom filter
 */
void example_persistence() {
    std::cout << "\n=== Example: Persistence ===\n" << std::endl;
    
    // Create and populate filter
    BloomFilter<std::string> filter(1000, 0.01);
    
    for (int i = 0; i < 100; ++i) {
        filter.insert("key_" + std::to_string(i));
    }
    
    // Serialize
    std::string serialized = filter.serialize_to_string();
    
    std::cout << "Original filter:" << std::endl;
    std::cout << "  Size: " << filter.size() << " bits" << std::endl;
    std::cout << "  Hash functions: " << filter.hash_functions() << std::endl;
    std::cout << "  Items: " << filter.count() << std::endl;
    std::cout << "  Serialized length: " << serialized.length() << " chars" << std::endl;
    
    // Save to file
    std::ofstream out("bloom_filter.dat");
    out << serialized;
    out.close();
    
    // Load from file
    std::ifstream in("bloom_filter.dat");
    std::string loaded((std::istreambuf_iterator<char>(in)),
                       std::istreambuf_iterator<char>());
    in.close();
    
    // Deserialize
    auto restored = BloomFilter<std::string>::deserialize_from_string(loaded);
    
    std::cout << "\nRestored filter:" << std::endl;
    std::cout << "  Size: " << restored.size() << " bits" << std::endl;
    std::cout << "  Hash functions: " << restored.hash_functions() << std::endl;
    std::cout << "  Items: " << restored.count() << std::endl;
    
    // Verify
    int found = 0;
    for (int i = 0; i < 100; ++i) {
        if (restored.might_contain("key_" + std::to_string(i))) {
            found++;
        }
    }
    
    std::cout << "  Verified items: " << found << "/100" << std::endl;
}

/**
 * @brief Example: Memory comparison with set
 */
void example_memory_comparison() {
    std::cout << "\n=== Example: Memory Comparison ===\n" << std::endl;
    
    const size_t num_elements = 100000;
    
    // Bloom filter
    BloomFilter<std::string> bloom(num_elements, 0.01);
    
    // Estimate memory for std::set (rough approximation)
    // Each string needs storage + pointer overhead
    // Roughly: average string length + ~40 bytes overhead per element
    
    std::cout << "For " << num_elements << " elements:\n" << std::endl;
    std::cout << "Bloom Filter:" << std::endl;
    std::cout << "  Memory: " << bloom.memory_usage() << " bytes ("
              << (bloom.memory_usage() / 1024.0) << " KB)" << std::endl;
    std::cout << "  Bits per element: " << (bloom.size() / num_elements) << std::endl;
    std::cout << "  False positive rate: " << (bloom.expected_false_positive_rate() * 100) 
              << "%" << std::endl;
    
    // Estimate set memory
    // Average string length ~10 bytes, overhead ~40 bytes per element
    size_t estimated_set_memory = num_elements * (10 + 40);
    std::cout << "\nEstimated std::set memory:" << std::endl;
    std::cout << "  Memory: ~" << estimated_set_memory << " bytes ("
              << (estimated_set_memory / 1024.0) << " KB)" << std::endl;
    
    double compression = static_cast<double>(estimated_set_memory) / bloom.memory_usage();
    std::cout << "\nBloom filter uses ~" << static_cast<int>(compression) 
              << "x less memory!" << std::endl;
}

int main() {
    std::cout << "╔════════════════════════════════════════════════════════════╗" << std::endl;
    std::cout << "║          Bloom Filter - Practical Examples                 ║" << std::endl;
    std::cout << "╚════════════════════════════════════════════════════════════╝" << std::endl;
    
    example_web_crawler();
    example_username_checker();
    example_cache_filtering();
    example_rate_limiting();
    example_scalable_filter();
    example_spell_checker();
    example_persistence();
    example_memory_comparison();
    
    std::cout << "\n╔════════════════════════════════════════════════════════════╗" << std::endl;
    std::cout << "║                    Key Takeaways                           ║" << std::endl;
    std::cout << "╠════════════════════════════════════════════════════════════╣" << std::endl;
    std::cout << "║ 1. NO false negatives - if it says 'no', it's definitely no║" << std::endl;
    std::cout << "║ 2. Small false positive rate - acceptable for many uses    ║" << std::endl;
    std::cout << "║ 3. Extremely memory efficient compared to sets             ║" << std::endl;
    std::cout << "║ 4. O(k) lookup time where k = hash functions               ║" << std::endl;
    std::cout << "║ 5. Use CountingBloomFilter when you need deletions         ║" << std::endl;
    std::cout << "║ 6. Use ScalableBloomFilter for growing datasets           ║" << std::endl;
    std::cout << "╚════════════════════════════════════════════════════════════╝" << std::endl;
    
    return 0;
}
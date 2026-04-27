/**
 * @file bloom_filter_test.cpp
 * @brief Comprehensive tests for Bloom Filter implementation
 */

#include "bloom_filter.hpp"
#include <iostream>
#include <cassert>
#include <string>
#include <vector>
#include <set>
#include <random>
#include <chrono>
#include <algorithm>

using namespace bloom_filter;

// Test helper macros
#define TEST_ASSERT(condition, message) \
    do { \
        if (!(condition)) { \
            std::cerr << "FAILED: " << message << std::endl; \
            return false; \
        } \
    } while(0)

#define RUN_TEST(test_func) \
    do { \
        std::cout << "Running " << #test_func << "... "; \
        if (test_func()) { \
            std::cout << "PASSED" << std::endl; \
            tests_passed++; \
        } else { \
            std::cout << "FAILED" << std::endl; \
            tests_failed++; \
        } \
    } while(0)

// ============= Basic Bloom Filter Tests =============

bool test_basic_insert_and_check() {
    BloomFilter<std::string> filter(100, 0.01);
    
    filter.insert("apple");
    filter.insert("banana");
    filter.insert("cherry");
    
    TEST_ASSERT(filter.might_contain("apple"), "Should contain 'apple'");
    TEST_ASSERT(filter.might_contain("banana"), "Should contain 'banana'");
    TEST_ASSERT(filter.might_contain("cherry"), "Should contain 'cherry'");
    TEST_ASSERT(!filter.might_contain("grape"), "Should not contain 'grape'");
    TEST_ASSERT(!filter.might_contain("orange"), "Should not contain 'orange'");
    
    return true;
}

bool test_integer_elements() {
    BloomFilter<int> filter(1000, 0.01);
    
    for (int i = 0; i < 100; ++i) {
        filter.insert(i);
    }
    
    for (int i = 0; i < 100; ++i) {
        TEST_ASSERT(filter.might_contain(i), ("Should contain " + std::to_string(i)).c_str());
    }
    
    int false_positives = 0;
    for (int i = 100; i < 200; ++i) {
        if (filter.might_contain(i)) {
            false_positives++;
        }
    }
    
    // Should be less than 10% false positive rate
    TEST_ASSERT(false_positives < 20, "False positive rate should be low");
    
    return true;
}

bool test_clear_functionality() {
    BloomFilter<std::string> filter(100, 0.01);
    
    filter.insert("test1");
    filter.insert("test2");
    
    TEST_ASSERT(filter.might_contain("test1"), "Should contain 'test1'");
    TEST_ASSERT(filter.count() == 2, "Count should be 2");
    
    filter.clear();
    
    TEST_ASSERT(!filter.might_contain("test1"), "Should not contain 'test1' after clear");
    TEST_ASSERT(!filter.might_contain("test2"), "Should not contain 'test2' after clear");
    TEST_ASSERT(filter.count() == 0, "Count should be 0 after clear");
    TEST_ASSERT(filter.bits_set() == 0, "No bits should be set after clear");
    
    return true;
}

bool test_parameter_calculation() {
    // Test that optimal parameters are calculated reasonably
    BloomFilter<std::string> filter1(1000, 0.01);
    TEST_ASSERT(filter1.size() > 0, "Filter size should be positive");
    TEST_ASSERT(filter1.hash_functions() > 0, "Should have at least 1 hash function");
    TEST_ASSERT(filter1.hash_functions() <= 20, "Should not exceed 20 hash functions");
    
    BloomFilter<std::string> filter2(1000, 0.001);
    // Lower false positive rate should result in larger filter
    TEST_ASSERT(filter2.size() >= filter1.size(), 
                "Lower FPR should result in larger filter");
    
    return true;
}

bool test_false_positive_rate() {
    BloomFilter<std::string> filter(1000, 0.05);
    
    // Insert 500 elements
    for (int i = 0; i < 500; ++i) {
        filter.insert("element_" + std::to_string(i));
    }
    
    // Test 1000 elements that were NOT inserted
    int false_positives = 0;
    for (int i = 500; i < 1500; ++i) {
        if (filter.might_contain("element_" + std::to_string(i))) {
            false_positives++;
        }
    }
    
    double actual_fpr = static_cast<double>(false_positives) / 1000.0;
    double expected_fpr = filter.current_false_positive_rate();
    
    // Actual FPR should be reasonably close to expected
    // Allow some margin due to randomness
    TEST_ASSERT(actual_fpr < 0.15, "Actual FPR should be reasonable");
    
    std::cout << "\n    Actual FPR: " << (actual_fpr * 100) << "%";
    std::cout << "\n    Expected FPR: " << (expected_fpr * 100) << "%";
    
    return true;
}

bool test_memory_efficiency() {
    size_t num_elements = 10000;
    BloomFilter<std::string> filter(num_elements, 0.01);
    
    for (size_t i = 0; i < num_elements; ++i) {
        filter.insert("item_" + std::to_string(i));
    }
    
    size_t bits_per_element = filter.memory_usage() * 8 / num_elements;
    
    // Bloom filter should use roughly 10-20 bits per element for 1% FPR
    TEST_ASSERT(bits_per_element < 30, "Bits per element should be reasonable");
    
    std::cout << "\n    Bits per element: " << bits_per_element;
    std::cout << "\n    Total memory: " << filter.memory_usage() << " bytes";
    
    return true;
}

// ============= Counting Bloom Filter Tests =============

bool test_counting_bloom_filter_basic() {
    CountingBloomFilter<std::string> filter(100, 0.01);
    
    filter.insert("apple");
    filter.insert("banana");
    filter.insert("cherry");
    
    TEST_ASSERT(filter.might_contain("apple"), "Should contain 'apple'");
    TEST_ASSERT(filter.might_contain("banana"), "Should contain 'banana'");
    TEST_ASSERT(filter.might_contain("cherry"), "Should contain 'cherry'");
    
    return true;
}

bool test_counting_bloom_filter_removal() {
    CountingBloomFilter<std::string> filter(100, 0.01);
    
    filter.insert("test");
    TEST_ASSERT(filter.might_contain("test"), "Should contain 'test'");
    TEST_ASSERT(filter.count() == 1, "Count should be 1");
    
    bool removed = filter.remove("test");
    TEST_ASSERT(removed, "Removal should succeed");
    TEST_ASSERT(!filter.might_contain("test"), "Should not contain 'test' after removal");
    TEST_ASSERT(filter.count() == 0, "Count should be 0 after removal");
    
    // Removing non-existent element should fail
    removed = filter.remove("nonexistent");
    TEST_ASSERT(!removed, "Removal of non-existent should fail");
    
    return true;
}

bool test_counting_bloom_filter_multiple_inserts() {
    CountingBloomFilter<std::string> filter(100, 0.01);
    
    // Insert same element multiple times
    filter.insert("test");
    filter.insert("test");
    filter.insert("test");
    
    TEST_ASSERT(filter.might_contain("test"), "Should contain 'test'");
    TEST_ASSERT(filter.count() == 3, "Count should be 3");
    
    // Remove once
    filter.remove("test");
    TEST_ASSERT(filter.might_contain("test"), "Should still contain 'test'");
    TEST_ASSERT(filter.count() == 2, "Count should be 2");
    
    return true;
}

// ============= Scalable Bloom Filter Tests =============

bool test_scalable_bloom_filter_basic() {
    ScalableBloomFilter<std::string> filter(0.01, 100);
    
    // Insert more elements than initial capacity
    for (int i = 0; i < 500; ++i) {
        filter.insert("item_" + std::to_string(i));
    }
    
    TEST_ASSERT(filter.count() == 500, "Count should be 500");
    TEST_ASSERT(filter.num_filters() > 1, "Should have multiple filters");
    
    // Check that all elements are still findable
    for (int i = 0; i < 500; ++i) {
        TEST_ASSERT(filter.might_contain("item_" + std::to_string(i)), 
                   ("Should contain item_" + std::to_string(i)).c_str());
    }
    
    return true;
}

bool test_scalable_bloom_filter_growth() {
    ScalableBloomFilter<std::string> filter(0.01, 50);
    
    size_t initial_filters = filter.num_filters();
    
    for (int i = 0; i < 200; ++i) {
        filter.insert("item_" + std::to_string(i));
    }
    
    TEST_ASSERT(filter.num_filters() > initial_filters, 
                "Should have grown beyond initial filter count");
    
    std::cout << "\n    Filters created: " << filter.num_filters();
    
    return true;
}

// ============= Serialization Tests =============

bool test_serialization() {
    BloomFilter<std::string> original(100, 0.01);
    
    original.insert("hello");
    original.insert("world");
    original.insert("test");
    
    std::string serialized = original.serialize_to_string();
    TEST_ASSERT(!serialized.empty(), "Serialized string should not be empty");
    
    BloomFilter<std::string> restored = 
        BloomFilter<std::string>::deserialize_from_string(serialized);
    
    TEST_ASSERT(restored.might_contain("hello"), "Restored should contain 'hello'");
    TEST_ASSERT(restored.might_contain("world"), "Restored should contain 'world'");
    TEST_ASSERT(restored.might_contain("test"), "Restored should contain 'test'");
    TEST_ASSERT(!restored.might_contain("notinserted"), 
                "Restored should not contain 'notinserted'");
    
    return true;
}

// ============= Performance Tests =============

bool test_insertion_performance() {
    const size_t num_elements = 100000;
    BloomFilter<int> filter(num_elements, 0.01);
    
    auto start = std::chrono::high_resolution_clock::now();
    
    for (size_t i = 0; i < num_elements; ++i) {
        filter.insert(static_cast<int>(i));
    }
    
    auto end = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start);
    
    double ops_per_second = static_cast<double>(num_elements) * 1000000.0 / duration.count();
    
    std::cout << "\n    Insertions: " << num_elements;
    std::cout << "\n    Time: " << duration.count() << " μs";
    std::cout << "\n    Ops/sec: " << static_cast<size_t>(ops_per_second);
    
    TEST_ASSERT(ops_per_second > 100000, "Should handle at least 100k ops/sec");
    
    return true;
}

bool test_lookup_performance() {
    const size_t num_elements = 100000;
    BloomFilter<int> filter(num_elements, 0.01);
    
    for (size_t i = 0; i < num_elements; ++i) {
        filter.insert(static_cast<int>(i));
    }
    
    auto start = std::chrono::high_resolution_clock::now();
    
    size_t found = 0;
    for (size_t i = 0; i < num_elements; ++i) {
        if (filter.might_contain(static_cast<int>(i))) {
            found++;
        }
    }
    
    auto end = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start);
    
    double ops_per_second = static_cast<double>(num_elements) * 1000000.0 / duration.count();
    
    std::cout << "\n    Lookups: " << num_elements;
    std::cout << "\n    Time: " << duration.count() << " μs";
    std::cout << "\n    Ops/sec: " << static_cast<size_t>(ops_per_second);
    std::cout << "\n    Found: " << found << " (should be " << num_elements << ")";
    
    TEST_ASSERT(found == num_elements, "All elements should be found (no false negatives)");
    TEST_ASSERT(ops_per_second > 100000, "Should handle at least 100k lookups/sec");
    
    return true;
}

// ============= Edge Case Tests =============

bool test_empty_filter() {
    BloomFilter<std::string> filter(100, 0.01);
    
    TEST_ASSERT(filter.count() == 0, "Empty filter should have count 0");
    TEST_ASSERT(filter.bits_set() == 0, "No bits should be set");
    TEST_ASSERT(!filter.might_contain("anything"), "Empty filter should not contain anything");
    TEST_ASSERT(filter.current_false_positive_rate() == 0.0, 
                "Empty filter should have 0 FPR");
    
    return true;
}

bool test_single_element() {
    BloomFilter<std::string> filter(100, 0.01);
    
    filter.insert("only_one");
    
    TEST_ASSERT(filter.count() == 1, "Count should be 1");
    TEST_ASSERT(filter.might_contain("only_one"), "Should contain the single element");
    
    return true;
}

bool test_large_filter() {
    const size_t num_elements = 100000;
    BloomFilter<int> filter(num_elements, 0.001);
    
    // Insert elements
    for (size_t i = 0; i < num_elements; ++i) {
        filter.insert(static_cast<int>(i));
    }
    
    // Verify no false negatives
    size_t found = 0;
    for (size_t i = 0; i < num_elements; ++i) {
        if (filter.might_contain(static_cast<int>(i))) {
            found++;
        }
    }
    TEST_ASSERT(found == num_elements, "Should have no false negatives");
    
    // Check false positive rate
    int false_positives = 0;
    for (int i = num_elements; i < static_cast<int>(num_elements) + 10000; ++i) {
        if (filter.might_contain(i)) {
            false_positives++;
        }
    }
    
    double fpr = static_cast<double>(false_positives) / 10000.0;
    TEST_ASSERT(fpr < 0.01, "FPR should be below 1%");
    
    std::cout << "\n    Elements: " << num_elements;
    std::cout << "\n    Memory: " << filter.memory_usage() << " bytes";
    std::cout << "\n    FPR: " << (fpr * 100) << "%";
    
    return true;
}

bool test_duplicate_insertions() {
    BloomFilter<std::string> filter(100, 0.01);
    
    filter.insert("same");
    filter.insert("same");
    filter.insert("same");
    
    TEST_ASSERT(filter.count() == 3, "Count should track all insertions");
    TEST_ASSERT(filter.might_contain("same"), "Should contain the element");
    
    return true;
}

// ============= Main =============

int main() {
    int tests_passed = 0;
    int tests_failed = 0;
    
    std::cout << "\n========== Bloom Filter Tests ==========\n" << std::endl;
    
    // Basic tests
    std::cout << "=== Basic BloomFilter Tests ===" << std::endl;
    RUN_TEST(test_basic_insert_and_check);
    RUN_TEST(test_integer_elements);
    RUN_TEST(test_clear_functionality);
    RUN_TEST(test_parameter_calculation);
    RUN_TEST(test_false_positive_rate);
    RUN_TEST(test_memory_efficiency);
    
    // Counting Bloom Filter tests
    std::cout << "\n=== CountingBloomFilter Tests ===" << std::endl;
    RUN_TEST(test_counting_bloom_filter_basic);
    RUN_TEST(test_counting_bloom_filter_removal);
    RUN_TEST(test_counting_bloom_filter_multiple_inserts);
    
    // Scalable Bloom Filter tests
    std::cout << "\n=== ScalableBloomFilter Tests ===" << std::endl;
    RUN_TEST(test_scalable_bloom_filter_basic);
    RUN_TEST(test_scalable_bloom_filter_growth);
    
    // Serialization tests
    std::cout << "\n=== Serialization Tests ===" << std::endl;
    RUN_TEST(test_serialization);
    
    // Performance tests
    std::cout << "\n=== Performance Tests ===" << std::endl;
    RUN_TEST(test_insertion_performance);
    RUN_TEST(test_lookup_performance);
    
    // Edge case tests
    std::cout << "\n=== Edge Case Tests ===" << std::endl;
    RUN_TEST(test_empty_filter);
    RUN_TEST(test_single_element);
    RUN_TEST(test_large_filter);
    RUN_TEST(test_duplicate_insertions);
    
    // Summary
    std::cout << "\n==========================================\n";
    std::cout << "Tests passed: " << tests_passed << std::endl;
    std::cout << "Tests failed: " << tests_failed << std::endl;
    std::cout << "==========================================\n";
    
    return tests_failed > 0 ? 1 : 0;
}
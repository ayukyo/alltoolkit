/**
 * AllToolkit - C++ UUID Utilities Test Suite
 * 
 * Comprehensive tests for uuid_utils module.
 * Compile with: g++ -std=c++17 -o uuid_test uuid_utils_test.cpp
 * 
 * Author: AllToolkit
 * License: MIT
 */

#include "uuid_utils.hpp"
#include <cassert>
#include <chrono>
#include <iostream>
#include <set>
#include <thread>

using namespace alltoolkit;

// Test helper macros
#define TEST(name) void test_##name()
#define RUN_TEST(name) do { \
    std::cout << "Running " #name "... "; \
    test_##name(); \
    std::cout << "PASSED" << std::endl; \
} while(0)

#define ASSERT_TRUE(expr) assert(expr)
#define ASSERT_FALSE(expr) assert(!(expr))
#define ASSERT_EQ(a, b) assert((a) == (b))
#define ASSERT_NE(a, b) assert((a) != (b))
#define ASSERT_THROW(expr) do { \
    bool thrown = false; \
    try { expr; } catch (...) { thrown = true; } \
    assert(thrown); \
} while(0)
#define ASSERT_NO_THROW(expr) do { \
    bool thrown = false; \
    try { expr; } catch (...) { thrown = true; } \
    assert(!thrown); \
} while(0)

// ============================================================================
// UUID Generation Tests
// ============================================================================

TEST(uuid_v4_generation_basic) {
    UUID uuid = UUID::generate_v4();
    
    // Check version is 4
    ASSERT_EQ(uuid.version(), 4);
    
    // Check variant is RFC 4122 (1)
    ASSERT_EQ(uuid.variant(), 1);
    
    // Should not be nil
    ASSERT_FALSE(uuid.is_nil());
    
    // Should be convertible to string
    std::string str = uuid.to_string();
    ASSERT_EQ(str.length(), 36);
    
    // String should have dashes in correct positions
    ASSERT_EQ(str[8], '-');
    ASSERT_EQ(str[13], '-');
    ASSERT_EQ(str[18], '-');
    ASSERT_EQ(str[23], '-');
}

TEST(uuid_v4_generation_uniqueness) {
    const int COUNT = 10000;
    std::set<std::string> uuid_strings;
    
    for (int i = 0; i < COUNT; ++i) {
        UUID uuid = UUID::generate_v4();
        std::string str = uuid.to_string();
        
        // Each UUID should be unique
        auto result = uuid_strings.insert(str);
        ASSERT_TRUE(result.second);
    }
    
    ASSERT_EQ(uuid_strings.size(), static_cast<size_t>(COUNT));
}

TEST(uuid_v4_bulk_generation) {
    const size_t COUNT = 1000;
    std::vector<UUID> uuids = UUID::generate_v4_bulk(COUNT);
    
    ASSERT_EQ(uuids.size(), COUNT);
    
    // Check all are v4
    for (const auto& uuid : uuids) {
        ASSERT_EQ(uuid.version(), 4);
        ASSERT_EQ(uuid.variant(), 1);
    }
    
    // Check uniqueness
    std::set<std::string> unique_strings;
    for (const auto& uuid : uuids) {
        unique_strings.insert(uuid.to_string());
    }
    ASSERT_EQ(unique_strings.size(), COUNT);
}

TEST(uuid_nil) {
    UUID nil_uuid = UUID::nil();
    
    // Should be all zeros
    ASSERT_TRUE(nil_uuid.is_nil());
    
    // String should be all zeros
    ASSERT_EQ(nil_uuid.to_string(), "00000000-0000-0000-0000-000000000000");
    
    // Generated UUID should not be nil
    UUID random_uuid = UUID::generate_v4();
    ASSERT_FALSE(random_uuid.is_nil());
    
    // Nil UUID has version 0
    ASSERT_EQ(nil_uuid.version(), 0);
}

// ============================================================================
// String Parsing Tests
// ============================================================================

TEST(uuid_from_string_with_dashes) {
    std::string input = "550e8400-e29b-41d4-a716-446655440000";
    UUID uuid = UUID::from_string(input);
    
    ASSERT_EQ(uuid.to_string(), input);
}

TEST(uuid_from_string_without_dashes) {
    std::string input = "550e8400e29b41d4a716446655440000";
    UUID uuid = UUID::from_string(input);
    
    ASSERT_EQ(uuid.to_string_no_dashes(), input);
}

TEST(uuid_from_string_uppercase) {
    std::string input = "550E8400-E29B-41D4-A716-446655440000";
    UUID uuid = UUID::from_string(input);
    
    // Lowercase output
    ASSERT_EQ(uuid.to_string(), "550e8400-e29b-41d4-a716-446655440000");
    
    // Uppercase output
    ASSERT_EQ(uuid.to_string(true), "550E8400-E29B-41D4-A716-446655440000");
}

TEST(uuid_from_string_invalid_length) {
    ASSERT_THROW(UUID::from_string("550e8400"));
    ASSERT_THROW(UUID::from_string("550e8400-e29b-41d4-a716"));
    ASSERT_THROW(UUID::from_string("550e8400-e29b-41d4-a716-446655440000-extra"));
}

TEST(uuid_from_string_invalid_chars) {
    ASSERT_THROW(UUID::from_string("550e8400-e29b-41d4-a716-44665544zzzz"));
    ASSERT_THROW(UUID::from_string("550e8400-e29b-41d4-a716-44665544!!!!"));
}

TEST(uuid_try_from_string) {
    UUID uuid;
    
    // Valid UUID should succeed
    ASSERT_TRUE(UUID::try_from_string("550e8400-e29b-41d4-a716-446655440000", uuid));
    ASSERT_EQ(uuid.to_string(), "550e8400-e29b-41d4-a716-446655440000");
    
    // Invalid UUID should fail
    ASSERT_FALSE(UUID::try_from_string("invalid", uuid));
}

TEST(uuid_is_valid) {
    ASSERT_TRUE(UUID::is_valid("550e8400-e29b-41d4-a716-446655440000"));
    ASSERT_TRUE(UUID::is_valid("550e8400e29b41d4a716446655440000"));
    ASSERT_TRUE(UUID::is_valid("550E8400-E29B-41D4-A716-446655440000"));
    
    ASSERT_FALSE(UUID::is_valid("550e8400"));
    ASSERT_FALSE(UUID::is_valid("550e8400-e29b-41d4-a716"));
    ASSERT_FALSE(UUID::is_valid("550e8400-e29b-41d4-a716-44665544zzzz"));
    ASSERT_FALSE(UUID::is_valid(""));
}

// ============================================================================
// String Output Tests
// ============================================================================

TEST(uuid_to_string_lowercase) {
    UUID uuid = UUID::from_string("550e8400-e29b-41d4-a716-446655440000");
    ASSERT_EQ(uuid.to_string(), "550e8400-e29b-41d4-a716-446655440000");
}

TEST(uuid_to_string_uppercase) {
    UUID uuid = UUID::from_string("550e8400-e29b-41d4-a716-446655440000");
    ASSERT_EQ(uuid.to_string(true), "550E8400-E29B-41D4-A716-446655440000");
}

TEST(uuid_to_string_no_dashes) {
    UUID uuid = UUID::from_string("550e8400-e29b-41d4-a716-446655440000");
    ASSERT_EQ(uuid.to_string_no_dashes(), "550e8400e29b41d4a716446655440000");
    ASSERT_EQ(uuid.to_string_no_dashes(true), "550E8400E29B41D4A716446655440000");
}

TEST(uuid_to_urn) {
    UUID uuid = UUID::from_string("550e8400-e29b-41d4-a716-446655440000");
    ASSERT_EQ(uuid.to_urn(), "urn:uuid:550e8400-e29b-41d4-a716-446655440000");
}

// ============================================================================
// Comparison Tests
// ============================================================================

TEST(uuid_equality) {
    UUID uuid1 = UUID::from_string("550e8400-e29b-41d4-a716-446655440000");
    UUID uuid2 = UUID::from_string("550e8400-e29b-41d4-a716-446655440000");
    UUID uuid3 = UUID::from_string("550e8400-e29b-41d4-a716-446655440001");
    
    ASSERT_EQ(uuid1, uuid2);
    ASSERT_NE(uuid1, uuid3);
    ASSERT_NE(uuid2, uuid3);
}

TEST(uuid_ordering) {
    UUID uuid1 = UUID::from_string("00000000-0000-0000-0000-000000000000");
    UUID uuid2 = UUID::from_string("550e8400-e29b-41d4-a716-446655440000");
    UUID uuid3 = UUID::from_string("ffffffff-ffff-ffff-ffff-ffffffffffff");
    
    ASSERT_TRUE(uuid1 < uuid2);
    ASSERT_TRUE(uuid2 < uuid3);
    ASSERT_TRUE(uuid1 < uuid3);
    
    ASSERT_FALSE(uuid2 < uuid1);
    ASSERT_FALSE(uuid3 < uuid2);
    
    ASSERT_TRUE(uuid1 <= uuid2);
    ASSERT_TRUE(uuid2 <= uuid2);
    ASSERT_TRUE(uuid2 > uuid1);
    ASSERT_TRUE(uuid2 >= uuid1);
}

TEST(uuid_comparison_in_containers) {
    std::set<UUID> uuid_set;
    
    UUID uuid1 = UUID::from_string("550e8400-e29b-41d4-a716-446655440000");
    UUID uuid2 = UUID::from_string("550e8400-e29b-41d4-a716-446655440001");
    
    uuid_set.insert(uuid1);
    uuid_set.insert(uuid2);
    uuid_set.insert(uuid1); // Duplicate
    
    ASSERT_EQ(uuid_set.size(), 2);
}

// ============================================================================
// UUID Version and Variant Tests
// ============================================================================

TEST(uuid_version) {
    UUID v4_uuid = UUID::generate_v4();
    ASSERT_EQ(v4_uuid.version(), 4);
    
    UUID nil_uuid = UUID::nil();
    ASSERT_EQ(nil_uuid.version(), 0);
    
    // Parse a known v4 UUID
    UUID parsed_v4 = UUID::from_string("550e8400-e29b-41d4-a716-446655440000");
    ASSERT_EQ(parsed_v4.version(), 4);
}

TEST(uuid_variant) {
    UUID v4_uuid = UUID::generate_v4();
    ASSERT_EQ(v4_uuid.variant(), 1); // RFC 4122
    
    // Parse a known RFC 4122 UUID
    UUID parsed = UUID::from_string("550e8400-e29b-41d4-a716-446655440000");
    ASSERT_EQ(parsed.variant(), 1);
}

// ============================================================================
// UUIDUtils Helper Class Tests
// ============================================================================

TEST(uuid_utils_generate) {
    UUID uuid1 = UUIDUtils::generate();
    UUID uuid2 = UUIDUtils::generate_v4();
    
    ASSERT_EQ(uuid1.version(), 4);
    ASSERT_EQ(uuid2.version(), 4);
    ASSERT_NE(uuid1, uuid2);
}

TEST(uuid_utils_generate_bulk) {
    auto uuids = UUIDUtils::generate_bulk(100);
    ASSERT_EQ(uuids.size(), 100);
    
    for (const auto& uuid : uuids) {
        ASSERT_EQ(uuid.version(), 4);
    }
}

TEST(uuid_utils_parse_and_is_valid) {
    std::string valid = "550e8400-e29b-41d4-a716-446655440000";
    std::string invalid = "not-a-uuid";
    
    ASSERT_TRUE(UUIDUtils::is_valid(valid));
    ASSERT_FALSE(UUIDUtils::is_valid(invalid));
    
    UUID parsed = UUIDUtils::parse(valid);
    ASSERT_EQ(parsed.to_string(), valid);
    
    UUID try_parsed;
    ASSERT_TRUE(UUIDUtils::try_parse(valid, try_parsed));
    ASSERT_FALSE(UUIDUtils::try_parse(invalid, try_parsed));
}

TEST(uuid_utils_nil) {
    UUID nil_uuid = UUIDUtils::nil();
    ASSERT_TRUE(UUIDUtils::is_nil(nil_uuid));
    
    UUID random_uuid = UUIDUtils::generate();
    ASSERT_FALSE(UUIDUtils::is_nil(random_uuid));
}

TEST(uuid_utils_compare) {
    UUID uuid1 = UUID::from_string("00000000-0000-0000-0000-000000000000");
    UUID uuid2 = UUID::from_string("550e8400-e29b-41d4-a716-446655440000");
    UUID uuid3 = UUID::from_string("ffffffff-ffff-ffff-ffff-ffffffffffff");
    
    ASSERT_EQ(UUIDUtils::compare(uuid1, uuid2), -1);
    ASSERT_EQ(UUIDUtils::compare(uuid2, uuid1), 1);
    ASSERT_EQ(UUIDUtils::compare(uuid1, uuid1), 0);
}

TEST(uuid_utils_vector_operations) {
    std::vector<UUID> uuids;
    UUID target = UUID::generate_v4();
    
    for (int i = 0; i < 10; ++i) {
        uuids.push_back(UUID::generate_v4());
    }
    uuids.push_back(target);
    
    // Contains
    ASSERT_TRUE(UUIDUtils::contains(uuids, target));
    
    // Sort
    UUIDUtils::sort(uuids);
    for (size_t i = 1; i < uuids.size(); ++i) {
        ASSERT_TRUE(uuids[i-1] < uuids[i] || uuids[i-1] == uuids[i]);
    }
    
    // Unique
    uuids.push_back(target);
    ASSERT_EQ(uuids.size(), 12);
    UUIDUtils::unique(uuids);
    ASSERT_EQ(uuids.size(), 11);
    
    // Count unique
    uuids.push_back(UUID::from_string("550e8400-e29b-41d4-a716-446655440000"));
    uuids.push_back(UUID::from_string("550e8400-e29b-41d4-a716-446655440000"));
    size_t unique_count = UUIDUtils::count_unique(uuids);
    ASSERT_EQ(unique_count, 12);
}

TEST(uuid_utils_string_conversion) {
    std::vector<UUID> uuids = UUIDUtils::generate_bulk(5);
    
    // To strings
    std::vector<std::string> strings = UUIDUtils::to_strings(uuids);
    ASSERT_EQ(strings.size(), uuids.size());
    
    for (size_t i = 0; i < uuids.size(); ++i) {
        ASSERT_EQ(uuids[i].to_string(), strings[i]);
    }
    
    // From strings
    std::vector<UUID> parsed = UUIDUtils::from_strings(strings);
    ASSERT_EQ(parsed.size(), uuids.size());
    
    for (size_t i = 0; i < uuids.size(); ++i) {
        ASSERT_EQ(uuids[i], parsed[i]);
    }
}

// ============================================================================
// Byte Access Tests
// ============================================================================

TEST(uuid_byte_access) {
    UUID uuid = UUID::from_string("550e8400-e29b-41d4-a716-446655440000");
    
    // Check specific bytes
    ASSERT_EQ(uuid[0], 0x55);
    ASSERT_EQ(uuid[1], 0x0e);
    ASSERT_EQ(uuid[2], 0x84);
    ASSERT_EQ(uuid[3], 0x00);
    
    // Bytes array access
    const auto& bytes = uuid.bytes();
    ASSERT_EQ(bytes.size(), 16);
    ASSERT_EQ(bytes[0], 0x55);
    
    // Out of range access
    ASSERT_THROW(uuid[16]);
}

// ============================================================================
// Performance Benchmarks
// ============================================================================

void benchmark_generation() {
    std::cout << "\n--- Performance Benchmarks ---\n";
    
    // Single generation
    auto start = std::chrono::high_resolution_clock::now();
    for (int i = 0; i < 10000; ++i) {
        UUID::generate_v4();
    }
    auto end = std::chrono::high_resolution_clock::now();
    auto single_duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start);
    std::cout << "Single generation (10000x): " << single_duration.count() << " μs" << std::endl;
    std::cout << "Per UUID: " << single_duration.count() / 10000.0 << " μs" << std::endl;
    
    // Bulk generation
    start = std::chrono::high_resolution_clock::now();
    auto uuids = UUID::generate_v4_bulk(10000);
    end = std::chrono::high_resolution_clock::now();
    auto bulk_duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start);
    std::cout << "\nBulk generation (10000x): " << bulk_duration.count() << " μs" << std::endl;
    std::cout << "Per UUID: " << bulk_duration.count() / 10000.0 << " μs" << std::endl;
    
    // String conversion
    UUID test_uuid = UUID::generate_v4();
    start = std::chrono::high_resolution_clock::now();
    for (int i = 0; i < 10000; ++i) {
        test_uuid.to_string();
    }
    end = std::chrono::high_resolution_clock::now();
    auto string_duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start);
    std::cout << "\nString conversion (10000x): " << string_duration.count() << " μs" << std::endl;
    std::cout << "Per conversion: " << string_duration.count() / 10000.0 << " μs" << std::endl;
    
    // Parsing
    std::string test_str = test_uuid.to_string();
    start = std::chrono::high_resolution_clock::now();
    for (int i = 0; i < 10000; ++i) {
        UUID::from_string(test_str);
    }
    end = std::chrono::high_resolution_clock::now();
    auto parse_duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start);
    std::cout << "\nParsing (10000x): " << parse_duration.count() << " μs" << std::endl;
    std::cout << "Per parse: " << parse_duration.count() / 10000.0 << " μs" << std::endl;
}

// ============================================================================
// Thread Safety Tests
// ============================================================================

TEST(uuid_thread_safety) {
    const int THREADS = 10;
    const int UUIDS_PER_THREAD = 1000;
    
    std::vector<std::thread> threads;
    std::vector<std::vector<UUID>> all_uuids(THREADS);
    
    for (int t = 0; t < THREADS; ++t) {
        threads.emplace_back([t, &all_uuids, UUIDS_PER_THREAD]() {
            for (int i = 0; i < UUIDS_PER_THREAD; ++i) {
                all_uuids[t].push_back(UUID::generate_v4());
            }
        });
    }
    
    for (auto& thread : threads) {
        thread.join();
    }
    
    // Collect all UUIDs and check uniqueness
    std::set<std::string> unique_uuids;
    for (const auto& thread_uuids : all_uuids) {
        for (const auto& uuid : thread_uuids) {
            unique_uuids.insert(uuid.to_string());
        }
    }
    
    // All UUIDs should be unique
    ASSERT_EQ(unique_uuids.size(), static_cast<size_t>(THREADS * UUIDS_PER_THREAD));
}

// ============================================================================
// Main
// ============================================================================

int main() {
    std::cout << "====================================\n";
    std::cout << "AllToolkit UUID Utilities Test Suite\n";
    std::cout << "====================================\n\n";
    
    // Generation tests
    std::cout << "--- UUID Generation Tests ---\n";
    RUN_TEST(uuid_v4_generation_basic);
    RUN_TEST(uuid_v4_generation_uniqueness);
    RUN_TEST(uuid_v4_bulk_generation);
    RUN_TEST(uuid_nil);
    
    // Parsing tests
    std::cout << "\n--- String Parsing Tests ---\n";
    RUN_TEST(uuid_from_string_with_dashes);
    RUN_TEST(uuid_from_string_without_dashes);
    RUN_TEST(uuid_from_string_uppercase);
    RUN_TEST(uuid_from_string_invalid_length);
    RUN_TEST(uuid_from_string_invalid_chars);
    RUN_TEST(uuid_try_from_string);
    RUN_TEST(uuid_is_valid);
    
    // Output tests
    std::cout << "\n--- String Output Tests ---\n";
    RUN_TEST(uuid_to_string_lowercase);
    RUN_TEST(uuid_to_string_uppercase);
    RUN_TEST(uuid_to_string_no_dashes);
    RUN_TEST(uuid_to_urn);
    
    // Comparison tests
    std::cout << "\n--- Comparison Tests ---\n";
    RUN_TEST(uuid_equality);
    RUN_TEST(uuid_ordering);
    RUN_TEST(uuid_comparison_in_containers);
    
    // Version/Variant tests
    std::cout << "\n--- Version and Variant Tests ---\n";
    RUN_TEST(uuid_version);
    RUN_TEST(uuid_variant);
    
    // UUIDUtils tests
    std::cout << "\n--- UUIDUtils Helper Tests ---\n";
    RUN_TEST(uuid_utils_generate);
    RUN_TEST(uuid_utils_generate_bulk);
    RUN_TEST(uuid_utils_parse_and_is_valid);
    RUN_TEST(uuid_utils_nil);
    RUN_TEST(uuid_utils_compare);
    RUN_TEST(uuid_utils_vector_operations);
    RUN_TEST(uuid_utils_string_conversion);
    
    // Byte access tests
    std::cout << "\n--- Byte Access Tests ---\n";
    RUN_TEST(uuid_byte_access);
    
    // Thread safety tests
    std::cout << "\n--- Thread Safety Tests ---\n";
    RUN_TEST(uuid_thread_safety);
    
    // Summary
    std::cout << "\n====================================\n";
    std::cout << "All tests PASSED!\n";
    std::cout << "====================================\n";
    
    // Benchmarks
    benchmark_generation();
    
    return 0;
}
/**
 * @file test_rate_limiter.cpp
 * @brief Unit tests for Rate Limiter utilities
 * 
 * Compile: g++ -std=c++17 -o test_rate_limiter test_rate_limiter.cpp -pthread
 * Run: ./test_rate_limiter
 */

#include "rate_limiter.hpp"
#include <iostream>
#include <cassert>
#include <thread>
#include <vector>
#include <atomic>
#include <sstream>

using namespace alltoolkit;

// Test helper
int tests_passed = 0;
int tests_failed = 0;

#define TEST(name) void test_##name()
#define RUN_TEST(name) do { \
    std::cout << "Running " << #name << "... "; \
    try { \
        test_##name(); \
        std::cout << "PASSED" << std::endl; \
        tests_passed++; \
    } catch (const std::exception& e) { \
        std::cout << "FAILED: " << e.what() << std::endl; \
        tests_failed++; \
    } \
} while(0)

#define ASSERT_TRUE(expr) do { \
    if (!(expr)) { \
        std::ostringstream oss; \
        oss << "Assertion failed: " << #expr << " at line " << __LINE__; \
        throw std::runtime_error(oss.str()); \
    } \
} while(0)

#define ASSERT_FALSE(expr) ASSERT_TRUE(!(expr))
#define ASSERT_EQ(a, b) do { \
    if ((a) != (b)) { \
        std::ostringstream oss; \
        oss << "Assertion failed: " << #a << " == " << #b << " at line " << __LINE__; \
        throw std::runtime_error(oss.str()); \
    } \
} while(0)

#define ASSERT_GT(a, b) do { \
    if (!((a) > (b))) { \
        std::ostringstream oss; \
        oss << "Assertion failed: " << #a << " > " << #b << " at line " << __LINE__; \
        throw std::runtime_error(oss.str()); \
    } \
} while(0)

#define ASSERT_GTE(a, b) do { \
    if (!((a) >= (b))) { \
        std::ostringstream oss; \
        oss << "Assertion failed: " << #a << " >= " << #b << " at line " << __LINE__; \
        throw std::runtime_error(oss.str()); \
    } \
} while(0)

#define ASSERT_LT(a, b) do { \
    if (!((a) < (b))) { \
        std::ostringstream oss; \
        oss << "Assertion failed: " << #a << " < " << #b << " at line " << __LINE__; \
        throw std::runtime_error(oss.str()); \
    } \
} while(0)

#define ASSERT_LTE(a, b) do { \
    if (!((a) <= (b))) { \
        std::ostringstream oss; \
        oss << "Assertion failed: " << #a << " <= " << #b << " at line " << __LINE__; \
        throw std::runtime_error(oss.str()); \
    } \
} while(0)

// ===== Token Bucket Tests =====

TEST(token_bucket_basic) {
    TokenBucket bucket(10, 5.0);  // capacity=10, 5 tokens/sec
    
    // Should be able to acquire up to capacity
    for (int i = 0; i < 10; i++) {
        ASSERT_TRUE(bucket.try_acquire());
    }
    
    // Should fail after capacity exhausted
    ASSERT_FALSE(bucket.try_acquire());
    
    // Available permits should be 0
    ASSERT_EQ(bucket.available_permits(), 0.0);
}

TEST(token_bucket_refill) {
    TokenBucket bucket(10, 10.0);  // 10 tokens/sec
    
    // Use all tokens
    for (int i = 0; i < 10; i++) {
        bucket.try_acquire();
    }
    
    // Wait 200ms, should have ~2 tokens
    std::this_thread::sleep_for(std::chrono::milliseconds(250));
    
    // Should be able to acquire 2 tokens now
    ASSERT_TRUE(bucket.try_acquire());
    ASSERT_TRUE(bucket.try_acquire());
    ASSERT_FALSE(bucket.try_acquire());  // No more tokens
}

TEST(token_bucket_burst) {
    TokenBucket bucket(5, 1.0);  // capacity=5, 1 token/sec
    
    // Burst should allow 5 immediate acquisitions
    ASSERT_TRUE(bucket.try_acquire(5));
    ASSERT_FALSE(bucket.try_acquire());  // No more capacity
}

TEST(token_bucket_invalid_args) {
    bool threw = false;
    try {
        TokenBucket bucket(0, 1.0);  // Invalid capacity
    } catch (const std::invalid_argument&) {
        threw = true;
    }
    ASSERT_TRUE(threw);
    
    threw = false;
    try {
        TokenBucket bucket(10, 0.0);  // Invalid rate
    } catch (const std::invalid_argument&) {
        threw = true;
    }
    ASSERT_TRUE(threw);
}

// ===== Sliding Window Tests =====

TEST(sliding_window_basic) {
    SlidingWindow window(5, 1000);  // 5 requests per second
    
    // Should allow 5 requests
    for (int i = 0; i < 5; i++) {
        ASSERT_TRUE(window.try_acquire());
    }
    
    // Should fail on 6th
    ASSERT_FALSE(window.try_acquire());
}

TEST(sliding_window_expiry) {
    SlidingWindow window(3, 200);  // 3 requests per 200ms
    
    // Use all permits
    for (int i = 0; i < 3; i++) {
        window.try_acquire();
    }
    ASSERT_FALSE(window.try_acquire());
    
    // Wait for window to expire
    std::this_thread::sleep_for(std::chrono::milliseconds(250));
    
    // Should allow new requests
    ASSERT_TRUE(window.try_acquire());
}

TEST(sliding_window_available_permits) {
    SlidingWindow window(10, 1000);
    
    ASSERT_EQ(window.available_permits(), 10.0);
    
    window.try_acquire(3);
    ASSERT_EQ(window.available_permits(), 7.0);
    
    window.try_acquire(5);
    ASSERT_EQ(window.available_permits(), 2.0);
}

// ===== Fixed Window Tests =====

TEST(fixed_window_basic) {
    FixedWindow window(5, 1000);  // 5 requests per second
    
    for (int i = 0; i < 5; i++) {
        ASSERT_TRUE(window.try_acquire());
    }
    
    ASSERT_FALSE(window.try_acquire());
}

TEST(fixed_window_reset) {
    FixedWindow window(3, 100);  // 3 requests per 100ms
    
    for (int i = 0; i < 3; i++) {
        window.try_acquire();
    }
    ASSERT_FALSE(window.try_acquire());
    
    // Wait for window reset
    std::this_thread::sleep_for(std::chrono::milliseconds(150));
    
    ASSERT_TRUE(window.try_acquire());
}

TEST(fixed_window_remaining_time) {
    FixedWindow window(5, 500);  // 5 requests per 500ms
    
    int64_t remaining = window.remaining_window_time();
    ASSERT_GTE(remaining, 0);
    ASSERT_GT(remaining, 400);  // Should be close to 500ms initially
}

// ===== Leaky Bucket Tests =====

TEST(leaky_bucket_basic) {
    LeakyBucket bucket(10, 5.0);  // capacity=10, 5 requests/sec
    
    // Should accept up to capacity
    for (int i = 0; i < 10; i++) {
        ASSERT_TRUE(bucket.try_acquire());
    }
    
    ASSERT_FALSE(bucket.try_acquire());
}

TEST(leaky_bucket_drain) {
    LeakyBucket bucket(5, 10.0);  // capacity=5, drains 10/sec
    
    // Fill the bucket
    for (int i = 0; i < 5; i++) {
        bucket.try_acquire();
    }
    
    // Wait 200ms, should drain ~2
    std::this_thread::sleep_for(std::chrono::milliseconds(250));
    
    // Should have capacity for 1-2 more
    ASSERT_TRUE(bucket.try_acquire());
}

TEST(leaky_bucket_available) {
    LeakyBucket bucket(10, 5.0);
    
    ASSERT_EQ(bucket.available_permits(), 10.0);
    
    bucket.try_acquire(5);
    ASSERT_EQ(bucket.available_permits(), 5.0);
}

// ===== Factory Tests =====

TEST(factory_api_limiter) {
    auto limiter = RateLimiterFactory::create_api_limiter();
    
    // Should allow 100 requests
    for (int i = 0; i < 100; i++) {
        ASSERT_TRUE(limiter.try_acquire());
    }
    ASSERT_FALSE(limiter.try_acquire());
}

TEST(factory_login_limiter) {
    auto limiter = RateLimiterFactory::create_login_limiter();
    
    // Should allow 5 requests
    for (int i = 0; i < 5; i++) {
        ASSERT_TRUE(limiter.try_acquire());
    }
    ASSERT_FALSE(limiter.try_acquire());
}

TEST(factory_custom_token) {
    auto limiter = RateLimiterFactory::create("token", 10.0, 20);
    ASSERT_TRUE(limiter->try_acquire(20));
    ASSERT_FALSE(limiter->try_acquire());
}

TEST(factory_custom_sliding) {
    auto limiter = RateLimiterFactory::create("sliding", 5.0, 5);
    for (int i = 0; i < 5; i++) {
        ASSERT_TRUE(limiter->try_acquire());
    }
    ASSERT_FALSE(limiter->try_acquire());
}

TEST(factory_custom_leaky) {
    auto limiter = RateLimiterFactory::create("leaky", 5.0, 10);
    ASSERT_TRUE(limiter->try_acquire(10));
    ASSERT_FALSE(limiter->try_acquire());
}

// ===== Thread Safety Tests =====

TEST(token_bucket_thread_safety) {
    TokenBucket bucket(100, 1000.0);  // Large capacity, fast refill
    std::atomic<int> success_count{0};
    std::atomic<int> fail_count{0};
    
    std::vector<std::thread> threads;
    for (int t = 0; t < 10; t++) {
        threads.emplace_back([&bucket, &success_count, &fail_count]() {
            for (int i = 0; i < 20; i++) {
                if (bucket.try_acquire()) {
                    success_count++;
                } else {
                    fail_count++;
                }
            }
        });
    }
    
    for (auto& thread : threads) {
        thread.join();
    }
    
    // Should have exactly 100 successes (capacity)
    ASSERT_EQ(success_count.load(), 100);
    ASSERT_EQ(fail_count.load(), 100);
}

TEST(sliding_window_thread_safety) {
    SlidingWindow window(50, 1000);  // 50 requests/sec
    std::atomic<int> success_count{0};
    
    std::vector<std::thread> threads;
    for (int t = 0; t < 10; t++) {
        threads.emplace_back([&window, &success_count]() {
            for (int i = 0; i < 10; i++) {
                if (window.try_acquire()) {
                    success_count++;
                }
            }
        });
    }
    
    for (auto& thread : threads) {
        thread.join();
    }
    
    ASSERT_EQ(success_count.load(), 50);
}

TEST(fixed_window_thread_safety) {
    FixedWindow window(30, 1000);
    std::atomic<int> success_count{0};
    
    std::vector<std::thread> threads;
    for (int t = 0; t < 5; t++) {
        threads.emplace_back([&window, &success_count]() {
            for (int i = 0; i < 10; i++) {
                if (window.try_acquire()) {
                    success_count++;
                }
            }
        });
    }
    
    for (auto& thread : threads) {
        thread.join();
    }
    
    ASSERT_EQ(success_count.load(), 30);
}

// ===== Estimate Tests =====

TEST(token_bucket_estimate) {
    TokenBucketWithEstimate bucket(5, 2.0);  // 5 capacity, 2/sec
    
    // Initially should have no wait
    ASSERT_EQ(bucket.estimate_wait_time(), 0);
    
    // Use all tokens
    bucket.try_acquire(5);
    
    // Should estimate ~500ms for 1 token (0.5 sec * 2 tokens/sec)
    int64_t wait = bucket.estimate_wait_time();
    ASSERT_GT(wait, 400);
    ASSERT_LT(wait, 600);
}

// Main
int main() {
    std::cout << "\n========================================" << std::endl;
    std::cout << "  Rate Limiter Unit Tests" << std::endl;
    std::cout << "========================================\n" << std::endl;
    
    // Token Bucket
    std::cout << "--- Token Bucket Tests ---" << std::endl;
    RUN_TEST(token_bucket_basic);
    RUN_TEST(token_bucket_refill);
    RUN_TEST(token_bucket_burst);
    RUN_TEST(token_bucket_invalid_args);
    
    // Sliding Window
    std::cout << "\n--- Sliding Window Tests ---" << std::endl;
    RUN_TEST(sliding_window_basic);
    RUN_TEST(sliding_window_expiry);
    RUN_TEST(sliding_window_available_permits);
    
    // Fixed Window
    std::cout << "\n--- Fixed Window Tests ---" << std::endl;
    RUN_TEST(fixed_window_basic);
    RUN_TEST(fixed_window_reset);
    RUN_TEST(fixed_window_remaining_time);
    
    // Leaky Bucket
    std::cout << "\n--- Leaky Bucket Tests ---" << std::endl;
    RUN_TEST(leaky_bucket_basic);
    RUN_TEST(leaky_bucket_drain);
    RUN_TEST(leaky_bucket_available);
    
    // Factory
    std::cout << "\n--- Factory Tests ---" << std::endl;
    RUN_TEST(factory_api_limiter);
    RUN_TEST(factory_login_limiter);
    RUN_TEST(factory_custom_token);
    RUN_TEST(factory_custom_sliding);
    RUN_TEST(factory_custom_leaky);
    
    // Thread Safety
    std::cout << "\n--- Thread Safety Tests ---" << std::endl;
    RUN_TEST(token_bucket_thread_safety);
    RUN_TEST(sliding_window_thread_safety);
    RUN_TEST(fixed_window_thread_safety);
    
    // Estimate
    std::cout << "\n--- Estimate Tests ---" << std::endl;
    RUN_TEST(token_bucket_estimate);
    
    // Summary
    std::cout << "\n========================================" << std::endl;
    std::cout << "  Results: " << tests_passed << " passed, " 
              << tests_failed << " failed" << std::endl;
    std::cout << "========================================\n" << std::endl;
    
    return tests_failed > 0 ? 1 : 0;
}
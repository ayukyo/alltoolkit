/**
 * @file example_rate_limiter.cpp
 * @brief Usage examples for Rate Limiter utilities
 * 
 * Compile: g++ -std=c++17 -o example_rate_limiter example_rate_limiter.cpp -pthread
 * Run: ./example_rate_limiter
 */

#include "rate_limiter.hpp"
#include <iostream>
#include <thread>
#include <chrono>
#include <iomanip>

using namespace alltoolkit;

void print_header(const std::string& title) {
    std::cout << "\n" << std::string(50, '=') << std::endl;
    std::cout << "  " << title << std::endl;
    std::cout << std::string(50, '=') << "\n" << std::endl;
}

void example_basic_token_bucket() {
    print_header("Basic Token Bucket Usage");
    
    // Create a bucket with capacity 5, refilling at 2 tokens/second
    TokenBucket bucket(5, 2.0);
    
    std::cout << "Token Bucket: capacity=5, refill_rate=2/sec\n" << std::endl;
    
    // Burst test
    std::cout << "1. Burst test - trying to acquire 5 tokens:" << std::endl;
    for (int i = 0; i < 5; i++) {
        bool success = bucket.try_acquire();
        std::cout << "   Attempt " << (i+1) << ": " 
                  << (success ? "✓ SUCCESS" : "✗ FAILED") << std::endl;
    }
    
    // Should fail - bucket empty
    std::cout << "\n2. Attempting 6th request (should fail):" << std::endl;
    bool success = bucket.try_acquire();
    std::cout << "   Attempt 6: " << (success ? "✓ SUCCESS" : "✗ FAILED (expected)") << std::endl;
    
    // Wait for refill
    std::cout << "\n3. Waiting 1.5 seconds for refill (expect ~3 tokens)..." << std::endl;
    std::this_thread::sleep_for(std::chrono::milliseconds(1500));
    
    std::cout << "   Available permits: " << std::fixed << std::setprecision(1) 
              << bucket.available_permits() << std::endl;
    
    for (int i = 0; i < 3; i++) {
        success = bucket.try_acquire();
        std::cout << "   Attempt " << (i+1) << ": " 
                  << (success ? "✓ SUCCESS" : "✗ FAILED") << std::endl;
    }
}

void example_sliding_window() {
    print_header("Sliding Window Rate Limiter");
    
    // 5 requests per 1 second
    SlidingWindow window(5, 1000);
    
    std::cout << "Sliding Window: max_requests=5, window=1000ms\n" << std::endl;
    
    std::cout << "1. Sending 5 requests rapidly:" << std::endl;
    for (int i = 0; i < 5; i++) {
        bool success = window.try_acquire();
        std::cout << "   Request " << (i+1) << ": " 
                  << (success ? "✓ ALLOWED" : "✗ DENIED") << std::endl;
    }
    
    std::cout << "\n2. 6th request (should be denied):" << std::endl;
    bool success = window.try_acquire();
    std::cout << "   Request 6: " << (success ? "✓ ALLOWED" : "✗ DENIED (expected)") << std::endl;
    
    std::cout << "\n3. Available permits: " << window.available_permits() << std::endl;
    
    std::cout << "\n4. Waiting for window to slide..." << std::endl;
    std::this_thread::sleep_for(std::chrono::milliseconds(1100));
    
    std::cout << "   Available permits after wait: " << window.available_permits() << std::endl;
    success = window.try_acquire();
    std::cout << "   New request: " << (success ? "✓ ALLOWED" : "✗ DENIED") << std::endl;
}

void example_fixed_window() {
    print_header("Fixed Window Rate Limiter");
    
    // 3 requests per 500ms window
    FixedWindow window(3, 500);
    
    std::cout << "Fixed Window: max_requests=3, window=500ms\n" << std::endl;
    
    std::cout << "1. First window - 4 requests:" << std::endl;
    for (int i = 0; i < 4; i++) {
        bool success = window.try_acquire();
        std::cout << "   Request " << (i+1) << ": " 
                  << (success ? "✓ ALLOWED" : "✗ DENIED") << std::endl;
    }
    
    std::cout << "\n2. Remaining time in window: " << window.remaining_window_time() << "ms" << std::endl;
    
    std::cout << "\n3. Waiting for window reset..." << std::endl;
    std::this_thread::sleep_for(std::chrono::milliseconds(600));
    
    std::cout << "4. New window - 3 more requests:" << std::endl;
    for (int i = 0; i < 3; i++) {
        bool success = window.try_acquire();
        std::cout << "   Request " << (i+1) << ": " 
                  << (success ? "✓ ALLOWED" : "✗ DENIED") << std::endl;
    }
}

void example_leaky_bucket() {
    print_header("Leaky Bucket Rate Limiter");
    
    // Capacity 10, drains at 3 requests/second
    LeakyBucket bucket(10, 3.0);
    
    std::cout << "Leaky Bucket: capacity=10, leak_rate=3/sec\n" << std::endl;
    
    std::cout << "1. Adding 10 requests to bucket:" << std::endl;
    for (int i = 0; i < 10; i++) {
        bool success = bucket.try_acquire();
        std::cout << "   Add " << (i+1) << ": " 
                  << (success ? "✓ ACCEPTED" : "✗ OVERFLOW") << std::endl;
    }
    
    std::cout << "\n2. 11th request (should overflow):" << std::endl;
    bool success = bucket.try_acquire();
    std::cout << "   Add 11: " << (success ? "✓ ACCEPTED" : "✗ OVERFLOW (expected)") << std::endl;
    
    std::cout << "\n3. Available capacity: " << bucket.available_permits() << std::endl;
    
    std::cout << "\n4. Waiting 1 second for draining..." << std::endl;
    std::this_thread::sleep_for(std::chrono::milliseconds(1000));
    
    std::cout << "   Available capacity after drain: " << bucket.available_permits() 
              << " (should be ~3)" << std::endl;
}

void example_factory_presets() {
    print_header("Factory Presets");
    
    std::cout << "1. API Limiter (100 req/min):" << std::endl;
    auto api_limiter = RateLimiterFactory::create_api_limiter();
    std::cout << "   Capacity: " << api_limiter.capacity() << std::endl;
    std::cout << "   Rate: " << api_limiter.refill_rate() << " tokens/sec\n" << std::endl;
    
    std::cout << "2. Login Limiter (5 req/min):" << std::endl;
    auto login_limiter = RateLimiterFactory::create_login_limiter();
    std::cout << "   Max requests: " << login_limiter.max_requests() << std::endl;
    std::cout << "   Window: " << login_limiter.window_ms() << "ms\n" << std::endl;
    
    std::cout << "3. Upload Limiter (10 req/hour):" << std::endl;
    auto upload_limiter = RateLimiterFactory::create_upload_limiter();
    std::cout << "   Max requests: " << upload_limiter.max_requests() << std::endl;
    std::cout << "   Window: " << upload_limiter.window_ms() << "ms\n" << std::endl;
    
    std::cout << "4. Message Limiter (30 req/min):" << std::endl;
    auto message_limiter = RateLimiterFactory::create_message_limiter();
    std::cout << "   Capacity: " << message_limiter.capacity() << std::endl;
    std::cout << "   Leak rate: " << message_limiter.leak_rate() << " req/sec\n" << std::endl;
}

void example_custom_factory() {
    print_header("Custom Rate Limiters via Factory");
    
    std::cout << "Creating custom rate limiters:\n" << std::endl;
    
    // Token bucket: 50 req/sec with burst up to 100
    auto token = RateLimiterFactory::create("token", 50.0, 100);
    std::cout << "1. Token Bucket (50/sec, burst=100):" << std::endl;
    std::cout << "   Burst test - acquire 100: " 
              << (token->try_acquire(100) ? "✓ SUCCESS" : "✗ FAILED") << std::endl;
    std::cout << "   After burst - acquire 1: " 
              << (token->try_acquire() ? "✓ SUCCESS" : "✗ FAILED (expected)") << "\n" << std::endl;
    
    // Sliding window: 10 req/sec
    auto sliding = RateLimiterFactory::create("sliding", 10.0, 10);
    std::cout << "2. Sliding Window (10/sec):" << std::endl;
    for (int i = 0; i < 12; i++) {
        bool success = sliding->try_acquire();
        if (!success) {
            std::cout << "   Request " << (i+1) << ": ✗ DENIED" << std::endl;
            break;
        }
    }
    std::cout << std::endl;
    
    // Leaky bucket: 5 req/sec, capacity 15
    auto leaky = RateLimiterFactory::create("leaky", 5.0, 15);
    std::cout << "3. Leaky Bucket (5/sec, capacity=15):" << std::endl;
    std::cout << "   Fill bucket with 15 requests: " 
              << (leaky->try_acquire(15) ? "✓ SUCCESS" : "✗ FAILED") << std::endl;
    std::cout << "   Try 16th request: " 
              << (leaky->try_acquire() ? "✓ SUCCESS" : "✗ FAILED (expected)") << std::endl;
}

void example_blocking_acquire() {
    print_header("Blocking Acquire");
    
    TokenBucket bucket(2, 2.0);  // capacity=2, 2/sec
    
    std::cout << "Token Bucket: capacity=2, refill_rate=2/sec\n" << std::endl;
    
    std::cout << "1. Acquiring 2 tokens (immediate)..." << std::endl;
    auto start = std::chrono::steady_clock::now();
    bucket.acquire();
    bucket.acquire();
    auto end = std::chrono::steady_clock::now();
    auto ms = std::chrono::duration_cast<std::chrono::milliseconds>(end - start).count();
    std::cout << "   Completed in " << ms << "ms (expected ~0ms)\n" << std::endl;
    
    std::cout << "2. Acquiring 2 more tokens (need to wait ~1sec)..." << std::endl;
    start = std::chrono::steady_clock::now();
    bucket.acquire(2);
    end = std::chrono::steady_clock::now();
    ms = std::chrono::duration_cast<std::chrono::milliseconds>(end - start).count();
    std::cout << "   Completed in " << ms << "ms (expected ~1000ms)\n" << std::endl;
}

void example_wait_time_estimation() {
    print_header("Wait Time Estimation");
    
    TokenBucketWithEstimate bucket(5, 2.0);  // 5 capacity, 2/sec
    
    std::cout << "Token Bucket with Estimation: capacity=5, rate=2/sec\n" << std::endl;
    
    std::cout << "1. Initial state:" << std::endl;
    std::cout << "   Available: " << bucket.available_permits() << std::endl;
    std::cout << "   Wait time for 1 token: " << bucket.estimate_wait_time() << "ms\n" << std::endl;
    
    std::cout << "2. After using 5 tokens:" << std::endl;
    bucket.try_acquire(5);
    std::cout << "   Available: " << bucket.available_permits() << std::endl;
    std::cout << "   Wait time for 1 token: ~" << bucket.estimate_wait_time() << "ms" << std::endl;
    std::cout << "   Wait time for 4 tokens: ~" << bucket.estimate_wait_time(4) << "ms\nn" << std::endl;
}

void example_use_case_api_rate_limiting() {
    print_header("Use Case: API Rate Limiting");
    
    auto limiter = RateLimiterFactory::create_api_limiter();
    
    std::cout << "Simulating API requests (100 req/min limit):\n" << std::endl;
    
    int allowed = 0;
    int denied = 0;
    
    // Simulate rapid burst of 120 requests
    for (int i = 0; i < 120; i++) {
        if (limiter.try_acquire()) {
            allowed++;
        } else {
            denied++;
        }
    }
    
    std::cout << "Results after 120 requests:" << std::endl;
    std::cout << "   Allowed: " << allowed << std::endl;
    std::cout << "   Denied: " << denied << std::endl;
    std::cout << "   Available permits: " << limiter.available_permits() << "\n" << std::endl;
    
    std::cout << "API can now be called safely without exceeding rate limits!" << std::endl;
}

int main() {
    std::cout << R"(
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║              AllToolkit Rate Limiter Examples                ║
║                                                              ║
║  Thread-safe rate limiting utilities for C++17               ║
║  Zero external dependencies                                  ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
)" << std::endl;
    
    example_basic_token_bucket();
    example_sliding_window();
    example_fixed_window();
    example_leaky_bucket();
    example_factory_presets();
    example_custom_factory();
    example_blocking_acquire();
    example_wait_time_estimation();
    example_use_case_api_rate_limiting();
    
    std::cout << "\n" << std::string(50, '=') << std::endl;
    std::cout << "  All examples completed successfully!" << std::endl;
    std::cout << std::string(50, '=') << "\n" << std::endl;
    
    return 0;
}
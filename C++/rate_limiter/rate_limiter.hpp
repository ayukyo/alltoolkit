/**
 * @file rate_limiter.hpp
 * @brief Rate Limiter - Thread-safe rate limiting utilities for C++
 * 
 * Provides multiple rate limiting algorithms:
 * - TokenBucket: Smooth rate limiting with burst support
 * - SlidingWindow: Precise rate limiting without burst
 * - FixedWindow: Simple and memory-efficient rate limiting
 * - LeakyBucket: Constant output rate with queue behavior
 * 
 * Zero external dependencies - uses only C++17 standard library.
 * 
 * @author AllToolkit
 * @date 2026-04-17
 * @version 1.0.0
 */

#ifndef ALLTOOLKIT_RATE_LIMITER_HPP
#define ALLTOOLKIT_RATE_LIMITER_HPP

#include <chrono>
#include <mutex>
#include <atomic>
#include <deque>
#include <cmath>
#include <thread>
#include <stdexcept>

namespace alltoolkit {

/**
 * @brief Base class for rate limiters
 */
class RateLimiterBase {
public:
    virtual ~RateLimiterBase() = default;
    
    /**
     * @brief Try to acquire a permit
     * @return true if permit acquired, false if rate limit exceeded
     */
    virtual bool try_acquire() = 0;
    
    /**
     * @brief Try to acquire multiple permits
     * @param permits Number of permits to acquire
     * @return true if all permits acquired, false otherwise
     */
    virtual bool try_acquire(int permits) = 0;
    
    /**
     * @brief Acquire a permit, blocking if necessary
     * @return Time waited in milliseconds
     */
    virtual int64_t acquire() = 0;
    
    /**
     * @brief Get the current available permits
     */
    virtual double available_permits() const = 0;
};

/**
 * @brief Token Bucket Rate Limiter
 * 
 * Allows burst traffic up to bucket capacity while maintaining
 * an average rate. Tokens are replenished at a constant rate.
 * 
 * Thread-safe implementation using mutex.
 */
class TokenBucket : public RateLimiterBase {
public:
    /**
     * @brief Construct a TokenBucket rate limiter
     * @param capacity Maximum number of tokens in the bucket (burst capacity)
     * @param refill_rate Tokens added per second
     */
    TokenBucket(int capacity, double refill_rate)
        : capacity_(capacity)
        , refill_rate_(refill_rate)
        , tokens_(capacity)
        , last_refill_(std::chrono::steady_clock::now()) {
        if (capacity <= 0) {
            throw std::invalid_argument("Capacity must be positive");
        }
        if (refill_rate <= 0) {
            throw std::invalid_argument("Refill rate must be positive");
        }
    }
    
    bool try_acquire() override {
        return try_acquire(1);
    }
    
    bool try_acquire(int permits) override {
        std::lock_guard<std::mutex> lock(mutex_);
        refill();
        
        if (tokens_ >= permits) {
            tokens_ -= permits;
            return true;
        }
        return false;
    }
    
    int64_t acquire() override {
        return acquire(1);
    }
    
    int64_t acquire(int permits) {
        while (true) {
            std::unique_lock<std::mutex> lock(mutex_);
            refill();
            
            if (tokens_ >= permits) {
                tokens_ -= permits;
                return 0;
            }
            
            // Calculate wait time
            double tokens_needed = permits - tokens_;
            int64_t wait_ms = static_cast<int64_t>(
                (tokens_needed / refill_rate_) * 1000.0);
            wait_ms = std::max(wait_ms, static_cast<int64_t>(1));
            
            lock.unlock();
            std::this_thread::sleep_for(std::chrono::milliseconds(wait_ms));
        }
    }
    
    double available_permits() const override {
        std::lock_guard<std::mutex> lock(mutex_);
        const_cast<TokenBucket*>(this)->refill();
        return tokens_;
    }
    
    int capacity() const { return capacity_; }
    double refill_rate() const { return refill_rate_; }

private:
    void refill() {
        auto now = std::chrono::steady_clock::now();
        auto elapsed = std::chrono::duration_cast<std::chrono::milliseconds>(
            now - last_refill_).count();
        
        if (elapsed > 0) {
            double tokens_to_add = (elapsed / 1000.0) * refill_rate_;
            tokens_ = std::min(tokens_ + tokens_to_add, static_cast<double>(capacity_));
            last_refill_ = now;
        }
    }
    
    int capacity_;
    double refill_rate_;
    double tokens_;
    std::chrono::steady_clock::time_point last_refill_;
    mutable std::mutex mutex_;
};

/**
 * @brief Sliding Window Rate Limiter
 * 
 * Precise rate limiting using a sliding time window.
 * Tracks individual requests within the window.
 * 
 * Thread-safe implementation.
 */
class SlidingWindow : public RateLimiterBase {
public:
    /**
     * @brief Construct a SlidingWindow rate limiter
     * @param max_requests Maximum requests allowed in the window
     * @param window_ms Window size in milliseconds
     */
    SlidingWindow(int max_requests, int64_t window_ms)
        : max_requests_(max_requests)
        , window_ms_(window_ms) {
        if (max_requests <= 0) {
            throw std::invalid_argument("Max requests must be positive");
        }
        if (window_ms <= 0) {
            throw std::invalid_argument("Window size must be positive");
        }
    }
    
    bool try_acquire() override {
        return try_acquire(1);
    }
    
    bool try_acquire(int permits) override {
        std::lock_guard<std::mutex> lock(mutex_);
        cleanup();
        
        if (static_cast<int>(timestamps_.size()) + permits <= max_requests_) {
            auto now = std::chrono::steady_clock::now();
            for (int i = 0; i < permits; ++i) {
                timestamps_.push_back(now);
            }
            return true;
        }
        return false;
    }
    
    int64_t acquire() override {
        return acquire(1);
    }
    
    int64_t acquire(int permits) {
        int64_t total_wait = 0;
        
        while (true) {
            {
                std::lock_guard<std::mutex> lock(mutex_);
                cleanup();
                
                if (static_cast<int>(timestamps_.size()) + permits <= max_requests_) {
                    auto now = std::chrono::steady_clock::now();
                    for (int i = 0; i < permits; ++i) {
                        timestamps_.push_back(now);
                    }
                    return total_wait;
                }
            }
            
            // Calculate wait time until oldest request expires
            std::this_thread::sleep_for(std::chrono::milliseconds(10));
            total_wait += 10;
        }
    }
    
    double available_permits() const override {
        std::lock_guard<std::mutex> lock(mutex_);
        const_cast<SlidingWindow*>(this)->cleanup();
        return max_requests_ - static_cast<int>(timestamps_.size());
    }
    
    int max_requests() const { return max_requests_; }
    int64_t window_ms() const { return window_ms_; }

private:
    void cleanup() {
        auto now = std::chrono::steady_clock::now();
        auto cutoff = now - std::chrono::milliseconds(window_ms_);
        
        while (!timestamps_.empty() && timestamps_.front() < cutoff) {
            timestamps_.pop_front();
        }
    }
    
    int max_requests_;
    int64_t window_ms_;
    std::deque<std::chrono::steady_clock::time_point> timestamps_;
    mutable std::mutex mutex_;
};

/**
 * @brief Fixed Window Rate Limiter
 * 
 * Simple rate limiting using fixed time windows.
 * Memory-efficient but may allow burst at window boundaries.
 * 
 * Thread-safe implementation using atomic operations.
 */
class FixedWindow : public RateLimiterBase {
public:
    /**
     * @brief Construct a FixedWindow rate limiter
     * @param max_requests Maximum requests allowed per window
     * @param window_ms Window size in milliseconds
     */
    FixedWindow(int max_requests, int64_t window_ms)
        : max_requests_(max_requests)
        , window_ms_(window_ms)
        , count_(0)
        , window_start_(std::chrono::steady_clock::now()) {
        if (max_requests <= 0) {
            throw std::invalid_argument("Max requests must be positive");
        }
        if (window_ms <= 0) {
            throw std::invalid_argument("Window size must be positive");
        }
    }
    
    bool try_acquire() override {
        return try_acquire(1);
    }
    
    bool try_acquire(int permits) override {
        std::lock_guard<std::mutex> lock(mutex_);
        reset_window();
        
        if (count_ + permits <= max_requests_) {
            count_ += permits;
            return true;
        }
        return false;
    }
    
    int64_t acquire() override {
        return acquire(1);
    }
    
    int64_t acquire(int permits) {
        int64_t total_wait = 0;
        
        while (true) {
            {
                std::lock_guard<std::mutex> lock(mutex_);
                reset_window();
                
                if (count_ + permits <= max_requests_) {
                    count_ += permits;
                    return total_wait;
                }
            }
            
            // Wait and retry
            std::this_thread::sleep_for(std::chrono::milliseconds(10));
            total_wait += 10;
        }
    }
    
    double available_permits() const override {
        std::lock_guard<std::mutex> lock(mutex_);
        const_cast<FixedWindow*>(this)->reset_window();
        return max_requests_ - count_;
    }
    
    int max_requests() const { return max_requests_; }
    int64_t window_ms() const { return window_ms_; }
    
    /**
     * @brief Get remaining time in current window (milliseconds)
     */
    int64_t remaining_window_time() const {
        std::lock_guard<std::mutex> lock(mutex_);
        auto now = std::chrono::steady_clock::now();
        auto elapsed = std::chrono::duration_cast<std::chrono::milliseconds>(
            now - window_start_).count();
        return std::max(static_cast<int64_t>(0), window_ms_ - elapsed);
    }

private:
    void reset_window() {
        auto now = std::chrono::steady_clock::now();
        auto elapsed = std::chrono::duration_cast<std::chrono::milliseconds>(
            now - window_start_).count();
        
        if (elapsed >= window_ms_) {
            count_ = 0;
            window_start_ = now;
        }
    }
    
    int max_requests_;
    int64_t window_ms_;
    int count_;
    std::chrono::steady_clock::time_point window_start_;
    mutable std::mutex mutex_;
};

/**
 * @brief Leaky Bucket Rate Limiter
 * 
 * Processes requests at a constant rate.
 * Requests fill the bucket and "leak" out at a steady rate.
 * Good for smoothing traffic bursts.
 * 
 * Thread-safe implementation.
 */
class LeakyBucket : public RateLimiterBase {
public:
    /**
     * @brief Construct a LeakyBucket rate limiter
     * @param capacity Maximum bucket capacity
     * @param leak_rate Requests processed per second
     */
    LeakyBucket(int capacity, double leak_rate)
        : capacity_(capacity)
        , leak_rate_(leak_rate)
        , water_(0)
        , last_leak_(std::chrono::steady_clock::now()) {
        if (capacity <= 0) {
            throw std::invalid_argument("Capacity must be positive");
        }
        if (leak_rate <= 0) {
            throw std::invalid_argument("Leak rate must be positive");
        }
    }
    
    bool try_acquire() override {
        return try_acquire(1);
    }
    
    bool try_acquire(int permits) override {
        std::lock_guard<std::mutex> lock(mutex_);
        leak();
        
        if (water_ + permits <= capacity_) {
            water_ += permits;
            return true;
        }
        return false;
    }
    
    int64_t acquire() override {
        return acquire(1);
    }
    
    int64_t acquire(int permits) {
        int64_t total_wait = 0;
        
        while (true) {
            {
                std::lock_guard<std::mutex> lock(mutex_);
                leak();
                
                if (water_ + permits <= capacity_) {
                    water_ += permits;
                    return total_wait;
                }
            }
            
            // Calculate wait time
            double overflow = water_ + permits - capacity_;
            int64_t wait_ms = static_cast<int64_t>(
                (overflow / leak_rate_) * 1000.0);
            wait_ms = std::max(wait_ms, static_cast<int64_t>(10));
            
            std::this_thread::sleep_for(std::chrono::milliseconds(wait_ms));
            total_wait += wait_ms;
        }
    }
    
    double available_permits() const override {
        std::lock_guard<std::mutex> lock(mutex_);
        const_cast<LeakyBucket*>(this)->leak();
        return capacity_ - water_;
    }
    
    int capacity() const { return capacity_; }
    double leak_rate() const { return leak_rate_; }

private:
    void leak() {
        auto now = std::chrono::steady_clock::now();
        auto elapsed = std::chrono::duration_cast<std::chrono::milliseconds>(
            now - last_leak_).count();
        
        if (elapsed > 0) {
            double leaked = (elapsed / 1000.0) * leak_rate_;
            water_ = std::max(0.0, water_ - leaked);
            last_leak_ = now;
        }
    }
    
    int capacity_;
    double leak_rate_;
    double water_;
    std::chrono::steady_clock::time_point last_leak_;
    mutable std::mutex mutex_;
};

/**
 * @brief Rate Limiter Factory
 * 
 * Creates rate limiters with common presets.
 */
class RateLimiterFactory {
public:
    /**
     * @brief Create a rate limiter for API calls (100 req/min)
     */
    static TokenBucket create_api_limiter() {
        return TokenBucket(100, 100.0 / 60.0);  // 100 requests per minute
    }
    
    /**
     * @brief Create a rate limiter for login attempts (5 req/min)
     */
    static SlidingWindow create_login_limiter() {
        return SlidingWindow(5, 60000);  // 5 requests per minute
    }
    
    /**
     * @brief Create a rate limiter for file uploads (10 req/hour)
     */
    static FixedWindow create_upload_limiter() {
        return FixedWindow(10, 3600000);  // 10 requests per hour
    }
    
    /**
     * @brief Create a rate limiter for message sending (30 req/min)
     */
    static LeakyBucket create_message_limiter() {
        return LeakyBucket(30, 30.0 / 60.0);  // 30 requests per minute
    }
    
    /**
     * @brief Create a custom rate limiter
     * @param type "token", "sliding", "fixed", or "leaky"
     * @param rate Requests per second
     * @param burst_capacity Maximum burst (for token bucket only)
     */
    static std::unique_ptr<RateLimiterBase> create(
        const std::string& type, 
        double rate, 
        int burst_capacity = 0) {
        
        if (type == "token") {
            int capacity = burst_capacity > 0 ? burst_capacity : static_cast<int>(rate);
            return std::make_unique<TokenBucket>(capacity, rate);
        }
        else if (type == "sliding") {
            int max_requests = burst_capacity > 0 ? burst_capacity : static_cast<int>(rate);
            return std::make_unique<SlidingWindow>(max_requests, 1000);
        }
        else if (type == "fixed") {
            int max_requests = burst_capacity > 0 ? burst_capacity : static_cast<int>(rate);
            return std::make_unique<FixedWindow>(max_requests, 1000);
        }
        else if (type == "leaky") {
            int capacity = burst_capacity > 0 ? burst_capacity : static_cast<int>(rate);
            return std::make_unique<LeakyBucket>(capacity, rate);
        }
        
        throw std::invalid_argument("Unknown rate limiter type: " + type);
    }
};

/**
 * @brief Rate Limiter with Wait Time Estimation
 * 
 * Decorator that adds wait time estimation capability.
 */
template<typename LimiterType>
class RateLimiterWithEstimate : public RateLimiterBase {
public:
    template<typename... Args>
    explicit RateLimiterWithEstimate(Args&&... args)
        : limiter_(std::forward<Args>(args)...) {}
    
    bool try_acquire() override {
        return limiter_.try_acquire();
    }
    
    bool try_acquire(int permits) override {
        return limiter_.try_acquire(permits);
    }
    
    int64_t acquire() override {
        return limiter_.acquire();
    }
    
    double available_permits() const override {
        return limiter_.available_permits();
    }
    
    /**
     * @brief Estimate wait time for acquiring permits
     * @param permits Number of permits needed
     * @return Estimated wait time in milliseconds, 0 if immediately available
     */
    virtual int64_t estimate_wait_time(int permits = 1) const = 0;
    
    LimiterType& limiter() { return limiter_; }
    const LimiterType& limiter() const { return limiter_; }

protected:
    LimiterType limiter_;
};

/**
 * @brief Token Bucket with Wait Time Estimation
 */
class TokenBucketWithEstimate : public RateLimiterWithEstimate<TokenBucket> {
public:
    TokenBucketWithEstimate(int capacity, double refill_rate)
        : RateLimiterWithEstimate<TokenBucket>(capacity, refill_rate) {}
    
    int64_t estimate_wait_time(int permits = 1) const override {
        double available = limiter_.available_permits();
        if (available >= permits) {
            return 0;
        }
        double needed = permits - available;
        return static_cast<int64_t>((needed / limiter_.refill_rate()) * 1000.0);
    }
};

} // namespace alltoolkit

#endif // ALLTOOLKIT_RATE_LIMITER_HPP
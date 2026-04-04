/**
 * @file mod.hpp
 * @brief C++ Cache Utilities - Thread-safe in-memory cache with TTL support
 * @version 1.0.0
 *
 * Features:
 * - Thread-safe operations using std::mutex
 * - TTL (Time To Live) support for automatic expiration
 * - LRU (Least Recently Used) eviction policy
 * - Size-based and count-based eviction
 * - Statistics tracking
 * - Zero dependencies, uses only C++ standard library (C++11+)
 *
 * Example usage:
 * @code
 * #include "cache_utils/mod.hpp"
 * using namespace alltoolkit;
 *
 * // Create cache with max 100 entries
 * Cache<std::string, std::string> cache(100);
 *
 * // Store with TTL (60 seconds)
 * cache.set("key", "value", 60);
 *
 * // Retrieve
 * std::string value;
 * if (cache.get("key", value)) {
 *     std::cout << value << std::endl;
 * }
 * @endcode
 */

#ifndef ALLTOOLKIT_CACHE_UTILS_HPP
#define ALLTOOLKIT_CACHE_UTILS_HPP

#include <string>
#include <unordered_map>
#include <map>
#include <chrono>
#include <mutex>
#include <functional>
#include <algorithm>
#include <cstddef>
#include <memory>
#include <vector>

namespace alltoolkit {

/**
 * @brief Cache entry metadata and value wrapper
 */
template<typename K, typename V>
struct CacheEntry {
    V value;
    std::chrono::steady_clock::time_point created_at;
    std::chrono::steady_clock::time_point last_accessed;
    long long ttl_seconds;
    size_t access_count;

    CacheEntry(const V& val, long long ttl_secs)
        : value(val)
        , created_at(std::chrono::steady_clock::now())
        , last_accessed(created_at)
        , ttl_seconds(ttl_secs)
        , access_count(0) {}

    /**
     * @brief Check if this entry has expired
     * @return true if expired, false otherwise
     */
    bool is_expired() const {
        if (ttl_seconds <= 0) return false;
        auto now = std::chrono::steady_clock::now();
        auto elapsed = std::chrono::duration_cast<std::chrono::seconds>(now - created_at).count();
        return elapsed > ttl_seconds;
    }

    /**
     * @brief Mark as accessed and update timestamp
     */
    void touch() {
        last_accessed = std::chrono::steady_clock::now();
        ++access_count;
    }
};

/**
 * @brief Cache statistics
 */
struct CacheStats {
    size_t hits;           ///< Number of cache hits
    size_t misses;         ///< Number of cache misses
    size_t evictions;      ///< Number of evicted entries
    size_t expirations;    ///< Number of expired entries
    size_t current_size;   ///< Current number of entries
    size_t max_size;       ///< Maximum allowed entries

    CacheStats() : hits(0), misses(0), evictions(0), expirations(0), current_size(0), max_size(0) {}

    /**
     * @brief Calculate hit rate (0.0 to 1.0)
     * @return Hit rate as percentage
     */
    double hit_rate() const {
        size_t total = hits + misses;
        return total == 0 ? 0.0 : static_cast<double>(hits) / total;
    }

    /**
     * @brief Reset all statistics
     */
    void reset() {
        hits = misses = evictions = expirations = 0;
    }
};

/**
 * @brief Eviction policy type
 */
enum class EvictionPolicy {
    LRU,    ///< Least Recently Used
    LFU,    ///< Least Frequently Used
    FIFO,   ///< First In First Out
    RANDOM  ///< Random eviction
};

/**
 * @brief Thread-safe key-value cache with TTL support
 *
 * @tparam K Key type (must be hashable)
 * @tparam V Value type
 */
template<typename K, typename V>
class Cache {
public:
    typedef std::chrono::steady_clock Clock;
    typedef Clock::time_point TimePoint;

private:
    mutable std::mutex mutex_;
    std::unordered_map<K, std::shared_ptr<CacheEntry<K, V> > > data_;
    size_t max_size_;
    EvictionPolicy policy_;
    CacheStats stats_;
    std::function<size_t(const V&)> size_calculator_;
    size_t current_bytes_;
    size_t max_bytes_;

public:
    /**
     * @brief Construct a new Cache
     * @param max_size Maximum number of entries (0 = unlimited)
     * @param policy Eviction policy to use
     * @param max_bytes Maximum memory usage in bytes (0 = unlimited)
     */
    explicit Cache(size_t max_size = 1000,
                   EvictionPolicy policy = EvictionPolicy::LRU,
                   size_t max_bytes = 0)
        : max_size_(max_size)
        , policy_(policy)
        , current_bytes_(0)
        , max_bytes_(max_bytes) {
        stats_.max_size = max_size;
    }

    /**
     * @brief Set a value in the cache
     * @param key The key
     * @param value The value to store
     * @param ttl_seconds Time to live in seconds (0 = no expiration)
     * @return true if successful, false otherwise
     */
    bool set(const K& key, const V& value, long long ttl_seconds = 0) {
        std::lock_guard<std::mutex> lock(mutex_);

        // Remove existing entry if present
        typename std::unordered_map<K, std::shared_ptr<CacheEntry<K, V> > >::iterator it = data_.find(key);
        if (it != data_.end()) {
            current_bytes_ -= entry_size(it->second->value);
            data_.erase(it);
        }

        // Evict entries if necessary
        while (should_evict()) {
            if (!evict_one()) break;
        }

        // Create new entry
        std::shared_ptr<CacheEntry<K, V> > entry(new CacheEntry<K, V>(value, ttl_seconds));
        current_bytes_ += entry_size(value);
        data_[key] = entry;

        return true;
    }

    /**
     * @brief Get a value from the cache
     * @param key The key to look up
     * @param out_value Output parameter for the value
     * @return true if found and not expired, false otherwise
     */
    bool get(const K& key, V& out_value) {
        std::lock_guard<std::mutex> lock(mutex_);

        typename std::unordered_map<K, std::shared_ptr<CacheEntry<K, V> > >::iterator it = data_.find(key);
        if (it == data_.end()) {
            ++stats_.misses;
            return false;
        }

        // Check expiration
        if (it->second->is_expired()) {
            current_bytes_ -= entry_size(it->second->value);
            data_.erase(it);
            ++stats_.expirations;
            ++stats_.misses;
            return false;
        }

        // Update access info
        it->second->touch();
        ++stats_.hits;
        out_value = it->second->value;

        return true;
    }

    /**
     * @brief Check if key exists and is not expired (without updating stats)
     * @param key The key to check
     * @return true if exists and valid
     */
    bool has(const K& key) {
        std::lock_guard<std::mutex> lock(mutex_);

        typename std::unordered_map<K, std::shared_ptr<CacheEntry<K, V> > >::iterator it = data_.find(key);
        if (it == data_.end()) {
            return false;
        }

        if (it->second->is_expired()) {
            current_bytes_ -= entry_size(it->second->value);
            data_.erase(it);
            ++stats_.expirations;
            return false;
        }

        return true;
    }

    /**
     * @brief Get a value with default if not found
     * @param key The key to look up
     * @param default_value Value to return if key not found
     * @return V The cached value or default
     */
    V get_or_default(const K& key, const V& default_value) {
        V result;
        if (get(key, result)) {
            return result;
        }
        return default_value;
    }

    /**
     * @brief Get or compute a value
     * @param key The key to look up
     * @param factory Function to create value if not found
     * @param ttl_seconds Time to live for computed value
     * @return V The cached or computed value
     */
    template<typename Factory>
    V get_or_compute(const K& key, Factory factory, long long ttl_seconds = 0) {
        V result;
        if (get(key, result)) {
            return result;
        }

        V value = factory();
        set(key, value, ttl_seconds);
        return value;
    }

    /**
     * @brief Remove a key from cache
     * @param key The key to remove
     * @return true if removed, false if not found
     */
    bool remove(const K& key) {
        std::lock_guard<std::mutex> lock(mutex_);

        typename std::unordered_map<K, std::shared_ptr<CacheEntry<K, V> > >::iterator it = data_.find(key);
        if (it == data_.end()) {
            return false;
        }

        current_bytes_ -= entry_size(it->second->value);
        data_.erase(it);
        return true;
    }

    /**
     * @brief Clear all entries
     */
    void clear() {
        std::lock_guard<std::mutex> lock(mutex_);
        data_.clear();
        current_bytes_ = 0;
    }

    /**
     * @brief Get current size
     * @return Number of entries
     */
    size_t size() const {
        std::lock_guard<std::mutex> lock(mutex_);
        return data_.size();
    }

    /**
     * @brief Check if cache is empty
     * @return true if empty
     */
    bool empty() const {
        std::lock_guard<std::mutex> lock(mutex_);
        return data_.empty();
    }

    /**
     * @brief Get cache statistics
     * @return CacheStats Current statistics
     */
    CacheStats stats() const {
        std::lock_guard<std::mutex> lock(mutex_);
        CacheStats s = stats_;
        s.current_size = data_.size();
        return s;
    }

    /**
     * @brief Reset statistics
     */
    void reset_stats() {
        std::lock_guard<std::mutex> lock(mutex_);
        stats_.reset();
    }

    /**
     * @brief Remove all expired entries
     * @return Number of entries removed
     */
    size_t purge_expired() {
        std::lock_guard<std::mutex> lock(mutex_);
        size_t count = 0;

        for (typename std::unordered_map<K, std::shared_ptr<CacheEntry<K, V> > >::iterator it = data_.begin(); it != data_.end();) {
            if (it->second->is_expired()) {
                current_bytes_ -= entry_size(it->second->value);
                it = data_.erase(it);
                ++count;
                ++stats_.expirations;
            } else {
                ++it;
            }
        }

        return count;
    }

    /**
     * @brief Get all keys (non-expired only)
     * @return std::vector<K> List of keys
     */
    std::vector<K> keys() const {
        std::lock_guard<std::mutex> lock(mutex_);
        std::vector<K> result;
        result.reserve(data_.size());

        for (typename std::unordered_map<K, std::shared_ptr<CacheEntry<K, V> > >::const_iterator it = data_.begin(); it != data_.end(); ++it) {
            if (!it->second->is_expired()) {
                result.push_back(it->first);
            }
        }

        return result;
    }

    /**
     * @brief Set custom size calculator for memory tracking
     * @param calculator Function to calculate size of value
     */
    void set_size_calculator(std::function<size_t(const V&)> calculator) {
        std::lock_guard<std::mutex> lock(mutex_);
        size_calculator_ = calculator;
    }

    /**
     * @brief Get current memory usage in bytes
     * @return size_t Bytes used
     */
    size_t memory_usage() const {
        std::lock_guard<std::mutex> lock(mutex_);
        return current_bytes_;
    }

private:
    /**
     * @brief Calculate entry size
     */
    size_t entry_size(const V& value) const {
        if (size_calculator_) {
            return size_calculator_(value);
        }
        return sizeof(V);
    }

    /**
     * @brief Check if eviction is needed
     */
    bool should_evict() const {
        if (max_size_ > 0 && data_.size() >= max_size_) {
            return true;
        }
        if (max_bytes_ > 0 && current_bytes_ >= max_bytes_) {
            return true;
        }
        return false;
    }

    /**
     * @brief Evict one entry based on policy
     * @return true if eviction succeeded
     */
    bool evict_one() {
        if (data_.empty()) return false;

        typename std::unordered_map<K, std::shared_ptr<CacheEntry<K, V> > >::iterator victim;

        switch (policy_) {
            case EvictionPolicy::LRU:
                victim = find_lru_victim();
                break;
            case EvictionPolicy::LFU:
                victim = find_lfu_victim();
                break;
            case EvictionPolicy::FIFO:
                victim = find_fifo_victim();
                break;
            case EvictionPolicy::RANDOM:
            default:
                victim = data_.begin();
                break;
        }

        if (victim != data_.end()) {
            current_bytes_ -= entry_size(victim->second->value);
            data_.erase(victim);
            ++stats_.evictions;
            return true;
        }

        return false;
    }

    /**
     * @brief Find LRU victim
     */
    typename std::unordered_map<K, std::shared_ptr<CacheEntry<K, V> > >::iterator find_lru_victim() {
        typename std::unordered_map<K, std::shared_ptr<CacheEntry<K, V> > >::iterator victim = data_.begin();
        TimePoint oldest = victim->second->last_accessed;

        for (typename std::unordered_map<K, std::shared_ptr<CacheEntry<K, V> > >::iterator it = data_.begin(); it != data_.end(); ++it) {
            if (it->second->last_accessed < oldest) {
                oldest = it->second->last_accessed;
                victim = it;
            }
        }
        return victim;
    }

    /**
     * @brief Find LFU victim
     */
    typename std::unordered_map<K, std::shared_ptr<CacheEntry<K, V> > >::iterator find_lfu_victim() {
        typename std::unordered_map<K, std::shared_ptr<CacheEntry<K, V> > >::iterator victim = data_.begin();
        size_t least_used = victim->second->access_count;

        for (typename std::unordered_map<K, std::shared_ptr<CacheEntry<K, V> > >::iterator it = data_.begin(); it != data_.end(); ++it) {
            if (it->second->access_count < least_used) {
                least_used = it->second->access_count;
                victim = it;
            }
        }
        return victim;
    }

    /**
     * @brief Find FIFO victim (oldest created)
     */
    typename std::unordered_map<K, std::shared_ptr<CacheEntry<K, V> > >::iterator find_fifo_victim() {
        typename std::unordered_map<K, std::shared_ptr<CacheEntry<K, V> > >::iterator victim = data_.begin();
        TimePoint oldest = victim->second->created_at;

        for (typename std::unordered_map<K, std::shared_ptr<CacheEntry<K, V> > >::iterator it = data_.begin(); it != data_.end(); ++it) {
            if (it->second->created_at < oldest) {
                oldest = it->second->created_at;
                victim = it;
            }
        }
        return victim;
    }
};

} // namespace alltoolkit

#endif // ALLTOOLKIT_CACHE_UTILS_HPP

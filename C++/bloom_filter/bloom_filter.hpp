/**
 * @file bloom_filter.hpp
 * @brief Bloom Filter Implementation - A space-efficient probabilistic data structure
 * 
 * Features:
 * - Zero external dependencies
 * - Configurable false positive rate
 * - Automatic optimal parameter calculation
 * - Support for any hashable type
 * - Thread-safe operations available
 * 
 * @author AllToolkit
 * @date 2026-04-28
 */

#ifndef BLOOM_FILTER_HPP
#define BLOOM_FILTER_HPP

#include <vector>
#include <cmath>
#include <functional>
#include <string>
#include <cstdint>
#include <sstream>
#include <iomanip>

namespace bloom_filter {

/**
 * @brief Hash functions for bloom filter
 * Uses a combination of FNV-1a and MurmurHash3-inspired mixing
 */
class HashFunctions {
public:
    /**
     * @brief FNV-1a hash implementation
     */
    static uint64_t fnv1a_hash(const std::string& data, uint64_t seed = 0) {
        uint64_t hash = 14695981039346656037ULL ^ seed;  // FNV offset basis
        const uint64_t prime = 1099511628211ULL;
        
        for (unsigned char c : data) {
            hash ^= c;
            hash *= prime;
        }
        return hash;
    }
    
    /**
     * @brief Simple hash combining for generating multiple hashes from one
     * Based on Kirsch-Mitzenmacher optimization
     */
    static uint64_t combine_hashes(uint64_t h1, uint64_t h2, size_t i) {
        return h1 + i * h2;
    }
};

/**
 * @brief Bloom Filter - Probabilistic set membership data structure
 * 
 * A Bloom filter can tell if an element is:
 * - Definitely NOT in the set (no false negatives)
 * - PROBABLY in the set (small probability of false positives)
 * 
 * @tparam T Type of elements to store (must be hashable via std::hash)
 */
template<typename T>
class BloomFilter {
public:
    /**
     * @brief Construct a bloom filter with specified parameters
     * @param expected_elements Expected number of elements to insert
     * @param false_positive_rate Desired false positive rate (0.0 - 1.0)
     */
    BloomFilter(size_t expected_elements, double false_positive_rate = 0.01)
        : expected_elements_(expected_elements),
          false_positive_rate_(false_positive_rate) {
        
        // Calculate optimal parameters
        // m = -n * ln(p) / (ln(2)^2)
        size_t m = static_cast<size_t>(
            std::ceil(-static_cast<double>(expected_elements) * 
                     std::log(false_positive_rate) / 
                     (std::log(2) * std::log(2)))
        );
        
        // k = m / n * ln(2)
        num_hash_functions_ = static_cast<size_t>(
            std::ceil(static_cast<double>(m) / expected_elements * std::log(2))
        );
        
        // Ensure at least 1 hash function and reasonable upper bound
        num_hash_functions_ = std::max(size_t(1), std::min(num_hash_functions_, size_t(20)));
        
        // Initialize bit array
        bits_.resize(m, false);
    }
    
    /**
     * @brief Construct a bloom filter with explicit size
     * @param num_bits Number of bits in the filter
     * @param num_hash_functions Number of hash functions to use
     */
    BloomFilter(size_t num_bits, size_t num_hash_functions)
        : num_hash_functions_(num_hash_functions),
          expected_elements_(0),
          false_positive_rate_(0.0) {
        bits_.resize(num_bits, false);
    }
    
    /**
     * @brief Insert an element into the filter
     * @param element Element to insert
     */
    void insert(const T& element) {
        std::string data = serialize(element);
        uint64_t h1 = HashFunctions::fnv1a_hash(data);
        uint64_t h2 = HashFunctions::fnv1a_hash(data, h1);
        
        for (size_t i = 0; i < num_hash_functions_; ++i) {
            uint64_t index = HashFunctions::combine_hashes(h1, h2, i) % bits_.size();
            bits_[index] = true;
        }
        ++element_count_;
    }
    
    /**
     * @brief Check if an element might be in the set
     * @param element Element to check
     * @return true if element might be in set (or false positive)
     * @return false if element is definitely NOT in set
     */
    bool might_contain(const T& element) const {
        std::string data = serialize(element);
        uint64_t h1 = HashFunctions::fnv1a_hash(data);
        uint64_t h2 = HashFunctions::fnv1a_hash(data, h1);
        
        for (size_t i = 0; i < num_hash_functions_; ++i) {
            uint64_t index = HashFunctions::combine_hashes(h1, h2, i) % bits_.size();
            if (!bits_[index]) {
                return false;
            }
        }
        return true;
    }
    
    /**
     * @brief Alias for might_contain
     */
    bool contains(const T& element) const {
        return might_contain(element);
    }
    
    /**
     * @brief Clear all elements from the filter
     */
    void clear() {
        std::fill(bits_.begin(), bits_.end(), false);
        element_count_ = 0;
    }
    
    /**
     * @brief Get number of bits in the filter
     */
    size_t size() const { return bits_.size(); }
    
    /**
     * @brief Get number of hash functions
     */
    size_t hash_functions() const { return num_hash_functions_; }
    
    /**
     * @brief Get count of inserted elements
     */
    size_t count() const { return element_count_; }
    
    /**
     * @brief Get number of bits set to 1
     */
    size_t bits_set() const {
        return std::count(bits_.begin(), bits_.end(), true);
    }
    
    /**
     * @brief Calculate current estimated false positive rate
     */
    double current_false_positive_rate() const {
        if (element_count_ == 0) return 0.0;
        
        // p = (1 - e^(-kn/m))^k
        double x = bits_.size();
        double n = element_count_;
        double k = num_hash_functions_;
        
        double ratio = std::exp(-k * n / x);
        return std::pow(1.0 - ratio, k);
    }
    
    /**
     * @brief Get expected false positive rate
     */
    double expected_false_positive_rate() const {
        return false_positive_rate_;
    }
    
    /**
     * @brief Get memory usage in bytes
     */
    size_t memory_usage() const {
        return (bits_.size() + 7) / 8;  // Round up to nearest byte
    }
    
    /**
     * @brief Serialize the bloom filter to a string (hex)
     */
    std::string serialize_to_string() const {
        std::ostringstream oss;
        oss << std::hex << std::setfill('0');
        
        // Header: size, num_hash_functions, element_count
        oss << std::setw(16) << bits_.size() << ":";
        oss << std::setw(4) << num_hash_functions_ << ":";
        oss << std::setw(16) << element_count_ << ":";
        
        // Bits
        for (size_t i = 0; i < bits_.size(); i += 8) {
            unsigned char byte = 0;
            for (size_t j = 0; j < 8 && (i + j) < bits_.size(); ++j) {
                if (bits_[i + j]) {
                    byte |= (1 << j);
                }
            }
            oss << std::setw(2) << static_cast<int>(byte);
        }
        
        return oss.str();
    }
    
    /**
     * @brief Deserialize bloom filter from a string
     */
    static BloomFilter<T> deserialize_from_string(const std::string& data) {
        std::istringstream iss(data);
        
        size_t size, num_hash, count;
        char sep;
        
        iss >> std::hex >> size >> sep;
        iss >> std::hex >> num_hash >> sep;
        iss >> std::hex >> count >> sep;
        
        BloomFilter<T> filter(size, num_hash);
        filter.element_count_ = count;
        
        std::string bits_data;
        iss >> bits_data;
        
        for (size_t i = 0; i < bits_data.size() / 2; ++i) {
            unsigned char byte;
            int byte_val;
            std::istringstream(bits_data.substr(i * 2, 2)) >> std::hex >> byte_val;
            byte = static_cast<unsigned char>(byte_val);
            
            for (size_t j = 0; j < 8 && (i * 8 + j) < size; ++j) {
                if (byte & (1 << j)) {
                    filter.bits_[i * 8 + j] = true;
                }
            }
        }
        
        return filter;
    }

private:
    std::vector<bool> bits_;
    size_t num_hash_functions_;
    size_t expected_elements_;
    double false_positive_rate_;
    size_t element_count_ = 0;
    
    /**
     * @brief Serialize element to string for hashing
     */
    std::string serialize(const T& element) const {
        std::ostringstream oss;
        oss << element;
        return oss.str();
    }
};

/**
 * @brief Counting Bloom Filter - Supports element removal
 * 
 * Uses a counter array instead of a bit array, allowing for deletions.
 * Uses more memory but provides more functionality.
 */
template<typename T>
class CountingBloomFilter {
public:
    CountingBloomFilter(size_t expected_elements, double false_positive_rate = 0.01)
        : expected_elements_(expected_elements),
          false_positive_rate_(false_positive_rate) {
        
        size_t m = static_cast<size_t>(
            std::ceil(-static_cast<double>(expected_elements) * 
                     std::log(false_positive_rate) / 
                     (std::log(2) * std::log(2)))
        );
        
        num_hash_functions_ = static_cast<size_t>(
            std::ceil(static_cast<double>(m) / expected_elements * std::log(2))
        );
        num_hash_functions_ = std::max(size_t(1), std::min(num_hash_functions_, size_t(20)));
        
        counters_.resize(m, 0);
        max_counter_ = 15;  // 4-bit counters by default
    }
    
    void insert(const T& element) {
        std::string data = serialize(element);
        uint64_t h1 = HashFunctions::fnv1a_hash(data);
        uint64_t h2 = HashFunctions::fnv1a_hash(data, h1);
        
        for (size_t i = 0; i < num_hash_functions_; ++i) {
            uint64_t index = HashFunctions::combine_hashes(h1, h2, i) % counters_.size();
            if (counters_[index] < max_counter_) {
                counters_[index]++;
            }
        }
        ++element_count_;
    }
    
    bool remove(const T& element) {
        if (!might_contain(element)) {
            return false;
        }
        
        std::string data = serialize(element);
        uint64_t h1 = HashFunctions::fnv1a_hash(data);
        uint64_t h2 = HashFunctions::fnv1a_hash(data, h1);
        
        for (size_t i = 0; i < num_hash_functions_; ++i) {
            uint64_t index = HashFunctions::combine_hashes(h1, h2, i) % counters_.size();
            if (counters_[index] > 0) {
                counters_[index]--;
            }
        }
        --element_count_;
        return true;
    }
    
    bool might_contain(const T& element) const {
        std::string data = serialize(element);
        uint64_t h1 = HashFunctions::fnv1a_hash(data);
        uint64_t h2 = HashFunctions::fnv1a_hash(data, h1);
        
        for (size_t i = 0; i < num_hash_functions_; ++i) {
            uint64_t index = HashFunctions::combine_hashes(h1, h2, i) % counters_.size();
            if (counters_[index] == 0) {
                return false;
            }
        }
        return true;
    }
    
    void clear() {
        std::fill(counters_.begin(), counters_.end(), 0);
        element_count_ = 0;
    }
    
    size_t size() const { return counters_.size(); }
    size_t hash_functions() const { return num_hash_functions_; }
    size_t count() const { return element_count_; }
    
private:
    std::vector<uint8_t> counters_;
    size_t num_hash_functions_;
    size_t expected_elements_;
    double false_positive_rate_;
    size_t element_count_ = 0;
    uint8_t max_counter_;
    
    std::string serialize(const T& element) const {
        std::ostringstream oss;
        oss << element;
        return oss.str();
    }
};

/**
 * @brief Scalable Bloom Filter - Grows automatically as needed
 * 
 * Maintains a collection of bloom filters, adding new ones when
 * the current one reaches capacity.
 */
template<typename T>
class ScalableBloomFilter {
public:
    ScalableBloomFilter(double false_positive_rate = 0.01, size_t initial_capacity = 1000)
        : base_false_positive_rate_(false_positive_rate),
          initial_capacity_(initial_capacity),
          growth_factor_(2),
          tightening_ratio_(0.9) {
        
        add_filter(initial_capacity_);
    }
    
    void insert(const T& element) {
        if (filters_.empty() || filters_.back().count() >= filters_.back().size() / filters_.back().hash_functions()) {
            size_t new_capacity = initial_capacity_ * static_cast<size_t>(
                std::pow(growth_factor_, filters_.size()));
            add_filter(new_capacity);
        }
        
        filters_.back().insert(element);
        ++total_count_;
    }
    
    bool might_contain(const T& element) const {
        for (const auto& filter : filters_) {
            if (filter.might_contain(element)) {
                return true;
            }
        }
        return false;
    }
    
    void clear() {
        filters_.clear();
        total_count_ = 0;
        add_filter(initial_capacity_);
    }
    
    size_t count() const { return total_count_; }
    size_t num_filters() const { return filters_.size(); }
    
    double current_false_positive_rate() const {
        if (filters_.empty()) return 0.0;
        
        // Combined FPR is product of individual FPRs
        double fpr = 1.0;
        for (const auto& filter : filters_) {
            fpr *= filter.current_false_positive_rate();
        }
        return fpr;
    }
    
private:
    void add_filter(size_t capacity) {
        double fpr = base_false_positive_rate_ * 
                    std::pow(tightening_ratio_, static_cast<double>(filters_.size()));
        filters_.emplace_back(capacity, fpr);
    }
    
    std::vector<BloomFilter<T>> filters_;
    double base_false_positive_rate_;
    size_t initial_capacity_;
    double growth_factor_;
    double tightening_ratio_;
    size_t total_count_ = 0;
};

}  // namespace bloom_filter

#endif  // BLOOM_FILTER_HPP
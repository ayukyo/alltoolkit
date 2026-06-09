#ifndef COUNT_MIN_SKETCH_HPP
#define COUNT_MIN_SKETCH_HPP

#include <cstdint>
#include <vector>
#include <string>
#include <stdexcept>
#include <cmath>
#include <algorithm>
#include <functional>
#include <cstring>

namespace alltoolkit {

struct CountMinConfig {
    size_t depth;
    size_t width;
    uint64_t seed;

    CountMinConfig(size_t d, size_t w, uint64_t s = 0xDEADBEEF)
        : depth(std::max(size_t(1), d))
        , width(std::max(size_t(2), w))
        , seed(s) {}
};

static CountMinConfig optimal(double epsilon, double delta) {
    size_t width = static_cast<size_t>(std::ceil(std::exp(1.0) / epsilon));
    size_t depth = static_cast<size_t>(std::ceil(-std::log(delta)));
    return CountMinConfig(depth, width, 0xDEADBEEF);
}

template<typename T>
class CountMinSketch {
private:
    std::vector<std::vector<uint64_t>> table_;
    size_t depth_;
    size_t width_;
    uint64_t seed_;
    uint64_t total_count_;

    std::vector<uint64_t> getHashes(const T& item) const {
        std::hash<T> hasher;
        uint64_t h1 = hasher(item);
        
        std::string seed_str = std::to_string(seed_);
        uint64_t h2 = 0xcbf29ce484222325ULL;
        for (char c : seed_str) {
            h2 = (h2 * 0x100000001b3ULL + static_cast<uint8_t>(c));
        }
        uint64_t item_hash = hasher(item);
        for (size_t b = 0; b < 8; b++) {
            h2 = (h2 * 0x100000001b3ULL + static_cast<uint8_t>((item_hash >> (b * 8)) & 0xFF));
        }
        
        std::vector<uint64_t> hashes(depth_);
        for (size_t i = 0; i < depth_; ++i) {
            hashes[i] = h1 + i * h2;
        }
        return hashes;
    }

public:
    CountMinSketch(size_t depth, size_t width, uint64_t seed = 0xDEADBEEF)
        : depth_(std::max(size_t(1), depth))
        , width_(std::max(size_t(2), width))
        , seed_(seed)
        , total_count_(0) {
        table_.resize(depth_);
        for (auto& row : table_) {
            row.resize(width_, 0);
        }
    }

    static CountMinSketch<T> withRate(double epsilon, double delta) {
        CountMinConfig config = optimal(epsilon, delta);
        return CountMinSketch<T>(config.depth, config.width, config.seed);
    }

    void update(const T& item, uint64_t delta) {
        auto hashes = getHashes(item);
        for (size_t i = 0; i < hashes.size(); ++i) {
            size_t idx = hashes[i] % width_;
            table_[i][idx] += delta;
        }
        total_count_ += delta;
    }

    void increment(const T& item) {
        update(item, 1);
    }

    uint64_t estimate(const T& item) const {
        auto hashes = getHashes(item);
        uint64_t min_val = table_[0][hashes[0] % width_];
        for (size_t i = 1; i < hashes.size(); ++i) {
            size_t idx = hashes[i] % width_;
            uint64_t val = table_[i][idx];
            if (val < min_val) min_val = val;
        }
        return min_val;
    }

    uint64_t totalCount() const { return total_count_; }
    size_t depth() const { return depth_; }
    size_t width() const { return width_; }

    void merge(const CountMinSketch<T>& other) {
        if (depth_ != other.depth_ || width_ != other.width_) {
            throw std::invalid_argument("Dimension mismatch");
        }
        for (size_t i = 0; i < depth_; ++i) {
            for (size_t j = 0; j < width_; ++j) {
                table_[i][j] += other.table_[i][j];
            }
        }
        total_count_ += other.total_count_;
    }

    std::vector<uint8_t> toBytes() const {
        size_t size = 32 + depth_ * width_ * 8;
        std::vector<uint8_t> bytes(size);
        
        size_t offset = 0;
        for (int i = 0; i < 8; ++i) bytes[offset++] = (depth_ >> (i * 8)) & 0xFF;
        for (int i = 0; i < 8; ++i) bytes[offset++] = (width_ >> (i * 8)) & 0xFF;
        for (int i = 0; i < 8; ++i) bytes[offset++] = (seed_ >> (i * 8)) & 0xFF;
        for (int i = 0; i < 8; ++i) bytes[offset++] = (total_count_ >> (i * 8)) & 0xFF;
        
        for (size_t i = 0; i < depth_; ++i) {
            for (size_t j = 0; j < width_; ++j) {
                uint64_t val = table_[i][j];
                for (int k = 0; k < 8; ++k) bytes[offset++] = (val >> (k * 8)) & 0xFF;
            }
        }
        return bytes;
    }

    void clear() {
        for (auto& row : table_) {
            std::fill(row.begin(), row.end(), 0);
        }
        total_count_ = 0;
    }
};

} // namespace alltoolkit

#endif // COUNT_MIN_SKETCH_HPP
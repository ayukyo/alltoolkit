/**
 * AllToolkit - C++ UUID Utilities
 * 
 * A zero-dependency, production-ready UUID generation and manipulation utility module.
 * Supports UUID v4 (random) generation, validation, comparison, and conversion.
 * 
 * Author: AllToolkit
 * License: MIT
 * Date: 2026-04-16
 */

#ifndef ALLTOOLKIT_UUID_UTILS_HPP
#define ALLTOOLKIT_UUID_UTILS_HPP

#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <cstring>
#include <iomanip>
#include <random>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>

namespace alltoolkit {

/**
 * UUID class representing a 128-bit Universally Unique Identifier.
 * 
 * This class provides:
 * - UUID v4 (random) generation
 * - UUID validation
 * - String conversion (uppercase/lowercase)
 * - Comparison operators
 * - Byte access
 */
class UUID {
public:
    /// Size of UUID in bytes
    static constexpr size_t BYTE_SIZE = 16;
    
    /// Size of UUID string representation (without dashes)
    static constexpr size_t HEX_STRING_SIZE = 32;
    
    /// Size of UUID string representation (with dashes)
    static constexpr size_t STRING_SIZE = 36;

    /**
     * Default constructor creates a nil UUID (all zeros).
     */
    UUID() : bytes_{} {}

    /**
     * Construct from a byte array.
     * @param bytes Array of 16 bytes
     */
    explicit UUID(const std::array<uint8_t, BYTE_SIZE>& bytes) : bytes_(bytes) {}

    /**
     * Construct from raw pointer to 16 bytes.
     * @param data Pointer to 16 bytes
     */
    explicit UUID(const uint8_t* data) {
        std::memcpy(bytes_.data(), data, BYTE_SIZE);
    }

    /**
     * Generate a UUID v4 (random-based).
     * Uses a high-quality random number generator.
     * 
     * @return A new random UUID
     */
    static UUID generate_v4() {
        thread_local std::random_device rd;
        thread_local std::mt19937_64 gen(rd());
        
        std::array<uint8_t, BYTE_SIZE> bytes;
        
        // Generate 16 random bytes
        std::uniform_int_distribution<uint64_t> dis;
        uint64_t rand1 = dis(gen);
        uint64_t rand2 = dis(gen);
        
        std::memcpy(bytes.data(), &rand1, 8);
        std::memcpy(bytes.data() + 8, &rand2, 8);
        
        // Set version to 4 (random-based UUID)
        // Version bits: bits 48-51 of time_hi_and_version field
        bytes[6] = (bytes[6] & 0x0F) | 0x40;
        
        // Set variant to RFC 4122
        // Variant bits: bits 64-65 of clock_seq_hi_and_reserved
        bytes[8] = (bytes[8] & 0x3F) | 0x80;
        
        return UUID(bytes);
    }

    /**
     * Generate multiple UUID v4 at once (more efficient for bulk generation).
     * 
     * @param count Number of UUIDs to generate
     * @return Vector of UUIDs
     */
    static std::vector<UUID> generate_v4_bulk(size_t count) {
        thread_local std::random_device rd;
        thread_local std::mt19937_64 gen(rd());
        
        std::vector<UUID> uuids;
        uuids.reserve(count);
        
        std::uniform_int_distribution<uint64_t> dis;
        
        for (size_t i = 0; i < count; ++i) {
            std::array<uint8_t, BYTE_SIZE> bytes;
            
            uint64_t rand1 = dis(gen);
            uint64_t rand2 = dis(gen);
            
            std::memcpy(bytes.data(), &rand1, 8);
            std::memcpy(bytes.data() + 8, &rand2, 8);
            
            bytes[6] = (bytes[6] & 0x0F) | 0x40;
            bytes[8] = (bytes[8] & 0x3F) | 0x80;
            
            uuids.emplace_back(bytes);
        }
        
        return uuids;
    }

    /**
     * Parse a UUID from string.
     * Accepts formats: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx or xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
     * 
     * @param str String representation of UUID
     * @return UUID object
     * @throws std::invalid_argument if string is not a valid UUID
     */
    static UUID from_string(const std::string& str) {
        std::string clean = str;
        
        // Remove dashes if present
        if (clean.length() == STRING_SIZE && 
            clean[8] == '-' && clean[13] == '-' && 
            clean[18] == '-' && clean[23] == '-') {
            clean = clean.substr(0, 8) + clean.substr(9, 4) + clean.substr(14, 4) +
                    clean.substr(19, 4) + clean.substr(24);
        }
        
        if (clean.length() != HEX_STRING_SIZE) {
            throw std::invalid_argument("Invalid UUID string length: " + str);
        }
        
        std::array<uint8_t, BYTE_SIZE> bytes;
        
        for (size_t i = 0; i < BYTE_SIZE; ++i) {
            std::string byte_str = clean.substr(i * 2, 2);
            
            // Validate hex characters
            for (char c : byte_str) {
                if (!is_hex_char(c)) {
                    throw std::invalid_argument("Invalid hex character in UUID: " + str);
                }
            }
            
            bytes[i] = static_cast<uint8_t>(std::stoul(byte_str, nullptr, 16));
        }
        
        return UUID(bytes);
    }

    /**
     * Try to parse a UUID from string without throwing.
     * 
     * @param str String representation of UUID
     * @param uuid Output UUID object (only valid if returns true)
     * @return true if parsing succeeded, false otherwise
     */
    static bool try_from_string(const std::string& str, UUID& uuid) {
        try {
            uuid = from_string(str);
            return true;
        } catch (...) {
            return false;
        }
    }

    /**
     * Check if a string is a valid UUID.
     * 
     * @param str String to validate
     * @return true if string is a valid UUID
     */
    static bool is_valid(const std::string& str) {
        UUID dummy;
        return try_from_string(str, dummy);
    }

    /**
     * Create a nil UUID (all zeros).
     * 
     * @return Nil UUID
     */
    static UUID nil() {
        return UUID();
    }

    /**
     * Check if this UUID is nil (all zeros).
     * 
     * @return true if nil UUID
     */
    bool is_nil() const {
        for (uint8_t byte : bytes_) {
            if (byte != 0) return false;
        }
        return true;
    }

    /**
     * Get UUID version (1-5, or 0 if invalid/unknown).
     * 
     * @return Version number
     */
    int version() const {
        return (bytes_[6] >> 4) & 0x0F;
    }

    /**
     * Get UUID variant.
     * 
     * @return Variant: 0 (NCS), 1 (RFC 4122), 2 (Microsoft), 3 (Reserved)
     */
    int variant() const {
        if ((bytes_[8] & 0x80) == 0) return 0;  // NCS
        if ((bytes_[8] & 0xC0) == 0x80) return 1;  // RFC 4122
        if ((bytes_[8] & 0xE0) == 0xC0) return 2;  // Microsoft
        return 3;  // Reserved
    }

    /**
     * Convert to string with dashes.
     * Format: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
     * 
     * @param uppercase If true, use uppercase letters
     * @return String representation
     */
    std::string to_string(bool uppercase = false) const {
        std::ostringstream oss;
        oss << std::hex << std::setfill('0');
        
        if (uppercase) {
            oss << std::uppercase;
        }
        
        // First group: 4 bytes
        for (int i = 0; i < 4; ++i) {
            oss << std::setw(2) << static_cast<int>(bytes_[i]);
        }
        oss << '-';
        
        // Second group: 2 bytes
        for (int i = 4; i < 6; ++i) {
            oss << std::setw(2) << static_cast<int>(bytes_[i]);
        }
        oss << '-';
        
        // Third group: 2 bytes
        for (int i = 6; i < 8; ++i) {
            oss << std::setw(2) << static_cast<int>(bytes_[i]);
        }
        oss << '-';
        
        // Fourth group: 2 bytes
        for (int i = 8; i < 10; ++i) {
            oss << std::setw(2) << static_cast<int>(bytes_[i]);
        }
        oss << '-';
        
        // Fifth group: 6 bytes
        for (int i = 10; i < 16; ++i) {
            oss << std::setw(2) << static_cast<int>(bytes_[i]);
        }
        
        return oss.str();
    }

    /**
     * Convert to string without dashes.
     * Format: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
     * 
     * @param uppercase If true, use uppercase letters
     * @return String representation without dashes
     */
    std::string to_string_no_dashes(bool uppercase = false) const {
        std::ostringstream oss;
        oss << std::hex << std::setfill('0');
        
        if (uppercase) {
            oss << std::uppercase;
        }
        
        for (uint8_t byte : bytes_) {
            oss << std::setw(2) << static_cast<int>(byte);
        }
        
        return oss.str();
    }

    /**
     * Convert to URN format.
     * Format: urn:uuid:xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
     * 
     * @return URN string
     */
    std::string to_urn() const {
        return "urn:uuid:" + to_string();
    }

    /**
     * Get underlying bytes.
     * 
     * @return Reference to byte array
     */
    const std::array<uint8_t, BYTE_SIZE>& bytes() const {
        return bytes_;
    }

    /**
     * Get byte at index.
     * 
     * @param index Byte index (0-15)
     * @return Byte value
     * @throws std::out_of_range if index >= 16
     */
    uint8_t operator[](size_t index) const {
        if (index >= BYTE_SIZE) {
            throw std::out_of_range("UUID byte index out of range");
        }
        return bytes_[index];
    }

    // Comparison operators
    bool operator==(const UUID& other) const {
        return bytes_ == other.bytes_;
    }

    bool operator!=(const UUID& other) const {
        return bytes_ != other.bytes_;
    }

    bool operator<(const UUID& other) const {
        return bytes_ < other.bytes_;
    }

    bool operator<=(const UUID& other) const {
        return bytes_ <= other.bytes_;
    }

    bool operator>(const UUID& other) const {
        return bytes_ > other.bytes_;
    }

    bool operator>=(const UUID& other) const {
        return bytes_ >= other.bytes_;
    }

private:
    std::array<uint8_t, BYTE_SIZE> bytes_;

    static bool is_hex_char(char c) {
        return (c >= '0' && c <= '9') || 
               (c >= 'a' && c <= 'f') || 
               (c >= 'A' && c <= 'F');
    }
};

/**
 * UUID Utilities class with helper functions.
 */
class UUIDUtils {
public:
    /**
     * Generate a UUID v4 (random-based).
     * 
     * @return New random UUID
     */
    static UUID generate() {
        return UUID::generate_v4();
    }

    /**
     * Generate a UUID v4 (random-based) - explicit version.
     * 
     * @return New random UUID
     */
    static UUID generate_v4() {
        return UUID::generate_v4();
    }

    /**
     * Generate multiple UUIDs at once.
     * 
     * @param count Number of UUIDs to generate
     * @return Vector of UUIDs
     */
    static std::vector<UUID> generate_bulk(size_t count) {
        return UUID::generate_v4_bulk(count);
    }

    /**
     * Parse UUID from string.
     * 
     * @param str String representation
     * @return UUID object
     */
    static UUID parse(const std::string& str) {
        return UUID::from_string(str);
    }

    /**
     * Try to parse UUID from string.
     * 
     * @param str String representation
     * @param uuid Output UUID
     * @return true if successful
     */
    static bool try_parse(const std::string& str, UUID& uuid) {
        return UUID::try_from_string(str, uuid);
    }

    /**
     * Validate UUID string.
     * 
     * @param str String to validate
     * @return true if valid UUID
     */
    static bool is_valid(const std::string& str) {
        return UUID::is_valid(str);
    }

    /**
     * Create nil UUID.
     * 
     * @return Nil UUID
     */
    static UUID nil() {
        return UUID::nil();
    }

    /**
     * Check if UUID is nil.
     * 
     * @param uuid UUID to check
     * @return true if nil
     */
    static bool is_nil(const UUID& uuid) {
        return uuid.is_nil();
    }

    /**
     * Compare two UUIDs.
     * 
     * @param a First UUID
     * @param b Second UUID
     * @return -1 if a < b, 0 if equal, 1 if a > b
     */
    static int compare(const UUID& a, const UUID& b) {
        if (a < b) return -1;
        if (a > b) return 1;
        return 0;
    }

    /**
     * Sort vector of UUIDs in place.
     * 
     * @param uuids Vector of UUIDs to sort
     */
    static void sort(std::vector<UUID>& uuids) {
        std::sort(uuids.begin(), uuids.end());
    }

    /**
     * Check if vector contains a specific UUID.
     * 
     * @param uuids Vector of UUIDs
     * @param uuid UUID to find
     * @return true if found
     */
    static bool contains(const std::vector<UUID>& uuids, const UUID& uuid) {
        return std::find(uuids.begin(), uuids.end(), uuid) != uuids.end();
    }

    /**
     * Remove duplicates from vector of UUIDs.
     * 
     * @param uuids Vector of UUIDs (will be modified)
     */
    static void unique(std::vector<UUID>& uuids) {
        std::sort(uuids.begin(), uuids.end());
        uuids.erase(std::unique(uuids.begin(), uuids.end()), uuids.end());
    }

    /**
     * Count unique UUIDs in vector.
     * 
     * @param uuids Vector of UUIDs
     * @return Number of unique UUIDs
     */
    static size_t count_unique(const std::vector<UUID>& uuids) {
        std::vector<UUID> copy = uuids;
        unique(copy);
        return copy.size();
    }

    /**
     * Convert vector of UUIDs to strings.
     * 
     * @param uuids Vector of UUIDs
     * @param uppercase Use uppercase letters
     * @return Vector of strings
     */
    static std::vector<std::string> to_strings(const std::vector<UUID>& uuids, 
                                                bool uppercase = false) {
        std::vector<std::string> strings;
        strings.reserve(uuids.size());
        
        for (const auto& uuid : uuids) {
            strings.push_back(uuid.to_string(uppercase));
        }
        
        return strings;
    }

    /**
     * Parse vector of strings to UUIDs.
     * 
     * @param strings Vector of strings
     * @return Vector of UUIDs
     * @throws std::invalid_argument if any string is invalid
     */
    static std::vector<UUID> from_strings(const std::vector<std::string>& strings) {
        std::vector<UUID> uuids;
        uuids.reserve(strings.size());
        
        for (const auto& str : strings) {
            uuids.push_back(UUID::from_string(str));
        }
        
        return uuids;
    }
};

} // namespace alltoolkit

#endif // ALLTOOLKIT_UUID_UTILS_HPP
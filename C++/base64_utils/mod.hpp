/**
 * @file mod.hpp
 * @brief Base64 Encoding/Decoding Utilities for C++
 *
 * A zero-dependency, header-only Base64 encoding and decoding library.
 * Supports standard Base64, URL-safe Base64, and binary data handling.
 *
 * @author AllToolkit Contributors
 * @version 1.0.0
 * @license MIT
 */

#ifndef ALLTOOLKIT_BASE64_UTILS_HPP
#define ALLTOOLKIT_BASE64_UTILS_HPP

#include <string>
#include <vector>
#include <cstdint>
#include <stdexcept>

namespace alltoolkit {

/**
 * @brief Base64 encoding and decoding utilities
 *
 * This class provides static methods for Base64 encoding/decoding operations.
 * All methods are stateless and thread-safe.
 */
class Base64Utils {
public:
    /**
     * @brief Encode a string to Base64
     *
     * @param input The input string to encode
     * @param urlSafe If true, use URL-safe alphabet (+/ replaced with -_)
     * @param padding If true, include padding characters (=)
     * @return std::string The Base64 encoded string
     *
     * @example
     *   std::string encoded = Base64Utils::encode("Hello, World!");
     *   // Returns: "SGVsbG8sIFdvcmxkIQ=="
     */
    static std::string encode(const std::string& input, bool urlSafe = false, bool padding = true);

    /**
     * @brief Encode binary data to Base64
     *
     * @param data Pointer to binary data
     * @param length Length of the data in bytes
     * @param urlSafe If true, use URL-safe alphabet
     * @param padding If true, include padding characters
     * @return std::string The Base64 encoded string
     */
    static std::string encode(const uint8_t* data, size_t length, bool urlSafe = false, bool padding = true);

    /**
     * @brief Encode a byte vector to Base64
     *
     * @param data Vector of bytes to encode
     * @param urlSafe If true, use URL-safe alphabet
     * @param padding If true, include padding characters
     * @return std::string The Base64 encoded string
     */
    static std::string encode(const std::vector<uint8_t>& data, bool urlSafe = false, bool padding = true);

    /**
     * @brief Decode a Base64 string
     *
     * @param input The Base64 string to decode
     * @param urlSafe If true, treat input as URL-safe Base64
     * @return std::string The decoded string
     * @throws std::invalid_argument If input is not valid Base64
     *
     * @example
     *   std::string decoded = Base64Utils::decode("SGVsbG8sIFdvcmxkIQ==");
     *   // Returns: "Hello, World!"
     */
    static std::string decode(const std::string& input, bool urlSafe = false);

    /**
     * @brief Decode a Base64 string to binary data
     *
     * @param input The Base64 string to decode
     * @param urlSafe If true, treat input as URL-safe Base64
     * @return std::vector<uint8_t> The decoded binary data
     * @throws std::invalid_argument If input is not valid Base64
     */
    static std::vector<uint8_t> decodeToBytes(const std::string& input, bool urlSafe = false);

    /**
     * @brief Convert standard Base64 to URL-safe Base64
     *
     * @param base64 Standard Base64 string
     * @param padding If true, keep padding characters
     * @return std::string URL-safe Base64 string
     */
    static std::string toUrlSafe(const std::string& base64, bool padding = false);

    /**
     * @brief Convert URL-safe Base64 to standard Base64
     *
     * @param base64Url URL-safe Base64 string
     * @return std::string Standard Base64 string
     */
    static std::string fromUrlSafe(const std::string& base64Url);

    /**
     * @brief Validate if a string is valid Base64
     *
     * @param input The string to validate
     * @param urlSafe If true, validate as URL-safe Base64
     * @return bool True if valid Base64, false otherwise
     */
    static bool isValid(const std::string& input, bool urlSafe = false);

    /**
     * @brief Calculate the encoded length for given input size
     *
     * @param inputLength Length of the input data in bytes
     * @param padding If true, include padding in calculation
     * @return size_t The expected encoded length
     */
    static size_t encodedLength(size_t inputLength, bool padding = true);

    /**
     * @brief Calculate the maximum decoded length for given Base64 string
     *
     * @param base64Length Length of the Base64 string
     * @return size_t The maximum possible decoded length
     */
    static size_t decodedMaxLength(size_t base64Length);

private:
    // Standard Base64 alphabet
    static const char BASE64_CHARS[];
    // URL-safe Base64 alphabet
    static const char BASE64_URL_CHARS[];

    // Private constructor to prevent instantiation
    Base64Utils() = delete;
};

// =============================================================================
// Implementation
// =============================================================================

const char Base64Utils::BASE64_CHARS[] =
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";

const char Base64Utils::BASE64_URL_CHARS[] =
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_";

inline std::string Base64Utils::encode(const std::string& input, bool urlSafe, bool padding) {
    return encode(reinterpret_cast<const uint8_t*>(input.data()), input.length(), urlSafe, padding);
}

inline std::string Base64Utils::encode(const std::vector<uint8_t>& data, bool urlSafe, bool padding) {
    return encode(data.data(), data.size(), urlSafe, padding);
}

inline std::string Base64Utils::encode(const uint8_t* data, size_t length, bool urlSafe, bool padding) {
    if (length == 0) {
        return "";
    }

    const char* alphabet = urlSafe ? BASE64_URL_CHARS : BASE64_CHARS;
    std::string result;
    result.reserve(encodedLength(length, padding));

    size_t i = 0;
    while (i + 2 < length) {
        uint32_t chunk = (static_cast<uint32_t>(data[i]) << 16) |
                        (static_cast<uint32_t>(data[i + 1]) << 8) |
                        static_cast<uint32_t>(data[i + 2]);

        result.push_back(alphabet[(chunk >> 18) & 0x3F]);
        result.push_back(alphabet[(chunk >> 12) & 0x3F]);
        result.push_back(alphabet[(chunk >> 6) & 0x3F]);
        result.push_back(alphabet[chunk & 0x3F]);

        i += 3;
    }

    // Handle remaining bytes
    if (i < length) {
        uint32_t chunk = static_cast<uint32_t>(data[i]) << 16;
        if (i + 1 < length) {
            chunk |= static_cast<uint32_t>(data[i + 1]) << 8;
        }

        result.push_back(alphabet[(chunk >> 18) & 0x3F]);
        result.push_back(alphabet[(chunk >> 12) & 0x3F]);

        if (i + 1 < length) {
            result.push_back(alphabet[(chunk >> 6) & 0x3F]);
        }
    }

    // Add padding if requested
    if (padding) {
        size_t paddingNeeded = (3 - (length % 3)) % 3;
        for (size_t j = 0; j < paddingNeeded; ++j) {
            result.push_back('=');
        }
    }

    return result;
}

inline std::string Base64Utils::decode(const std::string& input, bool urlSafe) {
    std::vector<uint8_t> bytes = decodeToBytes(input, urlSafe);
    return std::string(bytes.begin(), bytes.end());
}

inline std::vector<uint8_t> Base64Utils::decodeToBytes(const std::string& input, bool urlSafe) {
    if (input.empty()) {
        return {};
    }

    // Remove padding and validate
    std::string cleaned;
    cleaned.reserve(input.length());
    for (char c : input) {
        if (c == '=') {
            break;  // Padding ends the meaningful data
        }
        cleaned.push_back(c);
    }

    if (cleaned.empty()) {
        return {};
    }

    // Validate characters
    const std::string validChars = urlSafe
        ? "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_"
        : "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";

    for (char c : cleaned) {
        if (validChars.find(c) == std::string::npos) {
            throw std::invalid_argument("Invalid Base64 character: " + std::string(1, c));
        }
    }

    // Decode
    std::vector<uint8_t> result;
    result.reserve(decodedMaxLength(cleaned.length()));

    auto decodeChar = [urlSafe](char c) -> uint8_t {
        if (c >= 'A' && c <= 'Z') return c - 'A';
        if (c >= 'a' && c <= 'z') return c - 'a' + 26;
        if (c >= '0' && c <= '9') return c - '0' + 52;
        if (c == '+') return 62;
        if (c == '/') return 63;
        if (c == '-') return 62;  // URL-safe
        if (c == '_') return 63;  // URL-safe
        return 0;
    };

    size_t i = 0;
    while (i + 3 < cleaned.length()) {
        uint32_t chunk = (static_cast<uint32_t>(decodeChar(cleaned[i])) << 18) |
                        (static_cast<uint32_t>(decodeChar(cleaned[i + 1])) << 12) |
                        (static_cast<uint32_t>(decodeChar(cleaned[i + 2])) << 6) |
                        static_cast<uint32_t>(decodeChar(cleaned[i + 3]));

        result.push_back(static_cast<uint8_t>((chunk >> 16) & 0xFF));
        result.push_back(static_cast<uint8_t>((chunk >> 8) & 0xFF));
        result.push_back(static_cast<uint8_t>(chunk & 0xFF));

        i += 4;
    }

    // Handle remaining bytes
    if (i < cleaned.length()) {
        size_t remaining = cleaned.length() - i;
        uint32_t chunk = static_cast<uint32_t>(decodeChar(cleaned[i])) << 18;

        if (remaining > 1) {
            chunk |= static_cast<uint32_t>(decodeChar(cleaned[i + 1])) << 12;
            result.push_back(static_cast<uint8_t>((chunk >> 16) & 0xFF));

            if (remaining > 2) {
                chunk |= static_cast<uint32_t>(decodeChar(cleaned[i + 2])) << 6;
                result.push_back(static_cast<uint8_t>((chunk >> 8) & 0xFF));
            }
        }
    }

    return result;
}

inline std::string Base64Utils::toUrlSafe(const std::string& base64, bool padding) {
    std::string result;
    result.reserve(base64.length());

    for (char c : base64) {
        if (c == '+') {
            result.push_back('-');
        } else if (c == '/') {
            result.push_back('_');
        } else if (c == '=') {
            if (padding) {
                result.push_back(c);
            }
        } else {
            result.push_back(c);
        }
    }

    return result;
}

inline std::string Base64Utils::fromUrlSafe(const std::string& base64Url) {
    std::string result;
    result.reserve(base64Url.length());

    for (char c : base64Url) {
        if (c == '-') {
            result.push_back('+');
        } else if (c == '_') {
            result.push_back('/');
        } else {
            result.push_back(c);
        }
    }

    return result;
}

inline bool Base64Utils::isValid(const std::string& input, bool urlSafe) {
    if (input.empty()) {
        return true;
    }

    const size_t len = input.length();
    const size_t remainder = len % 4;
    
    // Fast path: 1 mod 4 is always invalid
    if (remainder == 1) {
        return false;
    }

    // Use lookup table for O(1) character validation
    // Table: 0=invalid, 1=valid data char, 2=padding
    static const uint8_t charTable[256] = {
        // Control chars: 0
        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,  // 0x00-0x0F
        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,  // 0x10-0x1F
        // Space ! " # $ % & ' ( ) * + , - . /
        0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,  // 0x20-0x2F (+ and / are valid)
        // 0 1 2 3 4 5 6 7 8 9 : ; < = > ?
        1,1,1,1,1,1,1,1,1,1,0,0,0,2,0,0,  // 0x30-0x3F (0-9, =)
        // @ A B C D E F G H I J K L M N O
        0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,  // 0x40-0x4F (A-O)
        // P Q R S T U V W X Y Z [ \ ] ^ _
        1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,  // 0x50-0x5F (P-Z)
        // ` a b c d e f g h i j k l m n o
        0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,  // 0x60-0x6F (a-o)
        // p q r s t u v w x y z { | } ~ DEL
        1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,  // 0x70-0x7F (p-z)
        // Extended ASCII: all invalid
        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
    };
    
    // URL-safe variant: '-' (0x2D) and '_' (0x5F) are valid instead of '+' (0x2B) and '/' (0x2F)
    static const uint8_t urlSafeCharTable[256] = {
        // Control chars: 0
        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,  // 0x00-0x0F
        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,  // 0x10-0x1F
        // Space ! " # $ % & ' ( ) * + , - . /
        0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,  // 0x20-0x2F (- is valid, + and / are not)
        // 0 1 2 3 4 5 6 7 8 9 : ; < = > ?
        1,1,1,1,1,1,1,1,1,1,0,0,0,2,0,0,  // 0x30-0x3F (0-9, =)
        // @ A B C D E F G H I J K L M N O
        0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,  // 0x40-0x4F (A-O)
        // P Q R S T U V W X Y Z [ \ ] ^ _
        1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,1,  // 0x50-0x5F (P-Z, _)
        // ` a b c d e f g h i j k l m n o
        0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,  // 0x60-0x6F (a-o)
        // p q r s t u v w x y z { | } ~ DEL
        1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,  // 0x70-0x7F (p-z)
        // Extended ASCII: all invalid
        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
    };
    
    const uint8_t* table = urlSafe ? urlSafeCharTable : charTable;

    size_t meaningfulChars = 0;
    bool foundPadding = false;
    
    for (unsigned char c : input) {
        uint8_t type = table[c];
        
        if (type == 2) {  // Padding
            foundPadding = true;
            continue;
        }
        
        if (foundPadding) {
            // Non-padding character after padding
            return false;
        }
        
        if (type == 0) {  // Invalid character
            return false;
        }
        
        meaningfulChars++;
    }

    // Valid lengths: 0, 2, 3 mod 4 (1 mod 4 is invalid)
    size_t mod = meaningfulChars % 4;
    return mod == 0 || mod == 2 || mod == 3;
}

inline size_t Base64Utils::encodedLength(size_t inputLength, bool padding) {
    if (inputLength == 0) {
        return 0;
    }
    size_t baseLength = ((inputLength + 2) / 3) * 4;
    if (!padding) {
        size_t remainder = inputLength % 3;
        if (remainder == 1) {
            baseLength -= 2;
        } else if (remainder == 2) {
            baseLength -= 1;
        }
    }
    return baseLength;
}

inline size_t Base64Utils::decodedMaxLength(size_t base64Length) {
    return (base64Length / 4) * 3 + (base64Length % 4 ? base64Length % 4 - 1 : 0);
}

} // namespace alltoolkit

#endif // ALLTOOLKIT_BASE64_UTILS_HPP

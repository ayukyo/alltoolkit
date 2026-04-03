/**
 * @file base64_utils_test.cpp
 * @brief Unit tests for Base64 Utilities
 *
 * Comprehensive test suite for Base64 encoding/decoding operations.
 *
 * @author AllToolkit Contributors
 * @version 1.0.0
 * @license MIT
 */

#include "mod.hpp"
#include <iostream>
#include <cassert>
#include <cstring>

using namespace alltoolkit;

// Test counter
int tests_run = 0;
int tests_passed = 0;

#define TEST(name) void test_##name()
#define RUN_TEST(name) do { \
    tests_run++; \
    try { \
        test_##name(); \
        std::cout << "  [PASS] " << #name << std::endl; \
        tests_passed++; \
    } catch (const std::exception& e) { \
        std::cout << "  [FAIL] " << #name << ": " << e.what() << std::endl; \
    } \
} while(0)

#define ASSERT_EQ(a, b) assert((a) == (b))
#define ASSERT_TRUE(x) assert((x))
#define ASSERT_FALSE(x) assert(!(x))

// =============================================================================
// Encoding Tests
// =============================================================================

TEST(encode_empty) {
    std::string result = Base64Utils::encode("");
    ASSERT_EQ(result, "");
}

TEST(encode_basic) {
    // RFC 4648 test vectors
    ASSERT_EQ(Base64Utils::encode("f"), "Zg==");
    ASSERT_EQ(Base64Utils::encode("fo"), "Zm8=");
    ASSERT_EQ(Base64Utils::encode("foo"), "Zm9v");
    ASSERT_EQ(Base64Utils::encode("foob"), "Zm9vYg==");
    ASSERT_EQ(Base64Utils::encode("fooba"), "Zm9vYmE=");
    ASSERT_EQ(Base64Utils::encode("foobar"), "Zm9vYmFy");
}

TEST(encode_hello_world) {
    ASSERT_EQ(Base64Utils::encode("Hello, World!"), "SGVsbG8sIFdvcmxkIQ==");
}

TEST(encode_binary_data) {
    std::vector<uint8_t> data = {0x00, 0x01, 0x02, 0x03, 0xFF};
    std::string result = Base64Utils::encode(data);
    ASSERT_EQ(result, "AAECA/8=");
}

TEST(encode_url_safe) {
    std::string input = "Hello+World/Test";
    std::string standard = Base64Utils::encode(input, false, true);
    std::string urlSafe = Base64Utils::encode(input, true, true);
    ASSERT_EQ(standard, "SGVsbG8rV29ybGQvVGVzdA==");
    ASSERT_EQ(urlSafe, "SGVsbG8rV29ybGQvVGVzdA==");
}

TEST(encode_no_padding) {
    ASSERT_EQ(Base64Utils::encode("f", false, false), "Zg");
    ASSERT_EQ(Base64Utils::encode("fo", false, false), "Zm8");
    ASSERT_EQ(Base64Utils::encode("foo", false, false), "Zm9v");
}

// =============================================================================
// Decoding Tests
// =============================================================================

TEST(decode_empty) {
    std::string result = Base64Utils::decode("");
    ASSERT_EQ(result, "");
}

TEST(decode_basic) {
    ASSERT_EQ(Base64Utils::decode("Zg=="), "f");
    ASSERT_EQ(Base64Utils::decode("Zm8="), "fo");
    ASSERT_EQ(Base64Utils::decode("Zm9v"), "foo");
    ASSERT_EQ(Base64Utils::decode("Zm9vYg=="), "foob");
    ASSERT_EQ(Base64Utils::decode("Zm9vYmE="), "fooba");
    ASSERT_EQ(Base64Utils::decode("Zm9vYmFy"), "foobar");
}

TEST(decode_hello_world) {
    ASSERT_EQ(Base64Utils::decode("SGVsbG8sIFdvcmxkIQ=="), "Hello, World!");
}

TEST(decode_binary_data) {
    std::vector<uint8_t> result = Base64Utils::decodeToBytes("AAECA/8=");
    ASSERT_EQ(result.size(), 5);
    ASSERT_EQ(result[0], 0x00);
    ASSERT_EQ(result[1], 0x01);
    ASSERT_EQ(result[2], 0x02);
    ASSERT_EQ(result[3], 0x03);
    ASSERT_EQ(result[4], 0xFF);
}

TEST(decode_no_padding) {
    ASSERT_EQ(Base64Utils::decode("Zg"), "f");
    ASSERT_EQ(Base64Utils::decode("Zm8"), "fo");
    ASSERT_EQ(Base64Utils::decode("Zm9v"), "foo");
}

TEST(decode_url_safe) {
    // URL-safe Base64 with - and _
    std::string result = Base64Utils::decode("SGVsbG8rV29ybGQvVGVzdA", true);
    ASSERT_EQ(result, "Hello+World/Test");
}

TEST(decode_invalid_char) {
    try {
        Base64Utils::decode("Zm9v!bar");
        assert(false);  // Should have thrown
    } catch (const std::invalid_argument&) {
        // Expected
    }
}

// =============================================================================
// Round-trip Tests
// =============================================================================

TEST(roundtrip_text) {
    std::string original = "The quick brown fox jumps over the lazy dog";
    std::string encoded = Base64Utils::encode(original);
    std::string decoded = Base64Utils::decode(encoded);
    ASSERT_EQ(decoded, original);
}

TEST(roundtrip_binary) {
    std::vector<uint8_t> original;
    for (int i = 0; i < 256; ++i) {
        original.push_back(static_cast<uint8_t>(i));
    }
    std::string encoded = Base64Utils::encode(original);
    std::vector<uint8_t> decoded = Base64Utils::decodeToBytes(encoded);
    ASSERT_EQ(original.size(), decoded.size());
    for (size_t i = 0; i < original.size(); ++i) {
        ASSERT_EQ(original[i], decoded[i]);
    }
}

TEST(roundtrip_url_safe) {
    std::string original = "Special chars: +/=";
    std::string encoded = Base64Utils::encode(original, true, false);
    std::string decoded = Base64Utils::decode(encoded, true);
    ASSERT_EQ(decoded, original);
}

// =============================================================================
// URL-safe Conversion Tests
// =============================================================================

TEST(to_url_safe) {
    ASSERT_EQ(Base64Utils::toUrlSafe("Hello+World/Test==", false), "Hello-World_Test");
    ASSERT_EQ(Base64Utils::toUrlSafe("Hello+World/Test==", true), "Hello-World_Test==");
}

TEST(from_url_safe) {
    ASSERT_EQ(Base64Utils::fromUrlSafe("Hello-World_Test"), "Hello+World/Test");
}

TEST(url_safe_roundtrip) {
    std::string standard = "SGVsbG8rV29ybGQvVGVzdA==";
    std::string urlSafe = Base64Utils::toUrlSafe(standard, true);
    std::string back = Base64Utils::fromUrlSafe(urlSafe);
    ASSERT_EQ(back, standard);
}

// =============================================================================
// Validation Tests
// =============================================================================

TEST(is_valid_empty) {
    ASSERT_TRUE(Base64Utils::isValid(""));
}

TEST(is_valid_standard) {
    ASSERT_TRUE(Base64Utils::isValid("SGVsbG8="));
    ASSERT_TRUE(Base64Utils::isValid("Zm9v"));
    ASSERT_TRUE(Base64Utils::isValid("Zg=="));
}

TEST(is_valid_url_safe) {
    ASSERT_TRUE(Base64Utils::isValid("SGVsbG8-", true));
    ASSERT_TRUE(Base64Utils::isValid("Zm9v_2E=", true));  // 8 chars with padding
}

TEST(is_valid_invalid) {
    ASSERT_FALSE(Base64Utils::isValid("Zm9v!"));
    ASSERT_FALSE(Base64Utils::isValid("Zm9v@"));
}

TEST(is_valid_wrong_length) {
    // Length % 4 == 1 is invalid
    ASSERT_FALSE(Base64Utils::isValid("Z"));
}

// =============================================================================
// Length Calculation Tests
// =============================================================================

TEST(encoded_length) {
    ASSERT_EQ(Base64Utils::encodedLength(0, true), 0);
    ASSERT_EQ(Base64Utils::encodedLength(1, true), 4);   // "Zg=="
    ASSERT_EQ(Base64Utils::encodedLength(2, true), 4);   // "Zm8="
    ASSERT_EQ(Base64Utils::encodedLength(3, true), 4);   // "Zm9v"
    ASSERT_EQ(Base64Utils::encodedLength(4, true), 8);   // "Zm9vYg=="
}

TEST(encoded_length_no_padding) {
    ASSERT_EQ(Base64Utils::encodedLength(1, false), 2);  // "Zg"
    ASSERT_EQ(Base64Utils::encodedLength(2, false), 3);  // "Zm8"
    ASSERT_EQ(Base64Utils::encodedLength(3, false), 4);  // "Zm9v"
}

TEST(decoded_max_length) {
    ASSERT_EQ(Base64Utils::decodedMaxLength(0), 0);
    ASSERT_EQ(Base64Utils::decodedMaxLength(4), 3);
    ASSERT_EQ(Base64Utils::decodedMaxLength(8), 6);
    ASSERT_EQ(Base64Utils::decodedMaxLength(5), 3);
}

// =============================================================================
// Unicode Tests
// =============================================================================

TEST(encode_unicode) {
    std::string chinese = "Hello World!";
    std::string encoded = Base64Utils::encode(chinese);
    std::string decoded = Base64Utils::decode(encoded);
    ASSERT_EQ(decoded, chinese);
}

TEST(encode_multibyte) {
    std::string emoji = "Hello World!";
    std::string encoded = Base64Utils::encode(emoji);
    std::string decoded = Base64Utils::decode(encoded);
    ASSERT_EQ(decoded, emoji);
}

// =============================================================================
// Main
// =============================================================================

int main() {
    std::cout << "==============================================" << std::endl;
    std::cout << "Base64 Utilities Test Suite" << std::endl;
    std::cout << "==============================================" << std::endl;

    std::cout << "\n--- Encoding Tests ---" << std::endl;
    RUN_TEST(encode_empty);
    RUN_TEST(encode_basic);
    RUN_TEST(encode_hello_world);
    RUN_TEST(encode_binary_data);
    RUN_TEST(encode_url_safe);
    RUN_TEST(encode_no_padding);

    std::cout << "\n--- Decoding Tests ---" << std::endl;
    RUN_TEST(decode_empty);
    RUN_TEST(decode_basic);
    RUN_TEST(decode_hello_world);
    RUN_TEST(decode_binary_data);
    RUN_TEST(decode_no_padding);
    RUN_TEST(decode_url_safe);
    RUN_TEST(decode_invalid_char);

    std::cout << "\n--- Round-trip Tests ---" << std::endl;
    RUN_TEST(roundtrip_text);
    RUN_TEST(roundtrip_binary);
    RUN_TEST(roundtrip_url_safe);

    std::cout << "\n--- URL-safe Conversion Tests ---" << std::endl;
    RUN_TEST(to_url_safe);
    RUN_TEST(from_url_safe);
    RUN_TEST(url_safe_roundtrip);

    std::cout << "\n--- Validation Tests ---" << std::endl;
    RUN_TEST(is_valid_empty);
    RUN_TEST(is_valid_standard);
    RUN_TEST(is_valid_url_safe);
    RUN_TEST(is_valid_invalid);
    RUN_TEST(is_valid_wrong_length);

    std::cout << "\n--- Length Calculation Tests ---" << std::endl;
    RUN_TEST(encoded_length);
    RUN_TEST(encoded_length_no_padding);
    RUN_TEST(decoded_max_length);

    std::cout << "\n--- Unicode Tests ---" << std::endl;
    RUN_TEST(encode_unicode);
    RUN_TEST(encode_multibyte);

    std::cout << "\n==============================================" << std::endl;
    std::cout << "Results: " << tests_passed << "/" << tests_run << " tests passed" << std::endl;
    std::cout << "==============================================" << std::endl;

    return (tests_passed == tests_run) ? 0 : 1;
}
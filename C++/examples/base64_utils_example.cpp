/**
 * @file base64_utils_example.cpp
 * @brief Usage examples for Base64 Utilities
 *
 * Demonstrates various use cases for Base64 encoding/decoding.
 *
 * @author AllToolkit Contributors
 * @version 1.0.0
 * @license MIT
 */

#include <iostream>
#include <vector>
#include <cstdint>
#include "../base64_utils/mod.hpp"

using namespace alltoolkit;

int main() {
    std::cout << "==============================================" << std::endl;
    std::cout << "Base64 Utilities - Usage Examples" << std::endl;
    std::cout << "==============================================" << std::endl;

    // =============================================================================
    // Example 1: Basic String Encoding/Decoding
    // =============================================================================
    std::cout << "\n1. Basic String Encoding/Decoding" << std::endl;
    std::cout << "-----------------------------------" << std::endl;

    std::string text = "Hello, World!";
    std::string encoded = Base64Utils::encode(text);
    std::string decoded = Base64Utils::decode(encoded);

    std::cout << "Original: " << text << std::endl;
    std::cout << "Encoded:  " << encoded << std::endl;
    std::cout << "Decoded:  " << decoded << std::endl;

    // =============================================================================
    // Example 2: Binary Data Encoding
    // =============================================================================
    std::cout << "\n2. Binary Data Encoding" << std::endl;
    std::cout << "------------------------" << std::endl;

    std::vector<uint8_t> binaryData = {0x00, 0x01, 0x02, 0x03, 0xFF, 0xFE};
    std::string binaryEncoded = Base64Utils::encode(binaryData);
    std::vector<uint8_t> binaryDecoded = Base64Utils::decodeToBytes(binaryEncoded);

    std::cout << "Original bytes: ";
    for (auto b : binaryData) {
        std::cout << std::hex << "0x" << static_cast<int>(b) << " ";
    }
    std::cout << std::dec << std::endl;
    std::cout << "Encoded: " << binaryEncoded << std::endl;
    std::cout << "Decoded bytes: ";
    for (auto b : binaryDecoded) {
        std::cout << std::hex << "0x" << static_cast<int>(b) << " ";
    }
    std::cout << std::dec << std::endl;

    // =============================================================================
    // Example 3: URL-safe Base64
    // =============================================================================
    std::cout << "\n3. URL-safe Base64" << std::endl;
    std::cout << "-------------------" << std::endl;

    std::string special = "user+name@example.com";
    std::string standardB64 = Base64Utils::encode(special);
    std::string urlSafeB64 = Base64Utils::encode(special, true, false);

    std::cout << "Original: " << special << std::endl;
    std::cout << "Standard Base64: " << standardB64 << std::endl;
    std::cout << "URL-safe Base64: " << urlSafeB64 << std::endl;

    // Demonstrate conversion
    std::string converted = Base64Utils::toUrlSafe(standardB64, false);
    std::cout << "Converted to URL-safe: " << converted << std::endl;

    // =============================================================================
    // Example 4: Padding Control
    // =============================================================================
    std::cout << "\n4. Padding Control" << std::endl;
    std::cout << "-------------------" << std::endl;

    std::string shortText = "Hi";
    std::string withPadding = Base64Utils::encode(shortText, false, true);
    std::string noPadding = Base64Utils::encode(shortText, false, false);

    std::cout << "Original: " << shortText << std::endl;
    std::cout << "With padding: " << withPadding << std::endl;
    std::cout << "No padding:   " << noPadding << std::endl;

    // Both decode to the same value
    std::cout << "Decoded (with padding): " << Base64Utils::decode(withPadding) << std::endl;
    std::cout << "Decoded (no padding):   " << Base64Utils::decode(noPadding) << std::endl;

    // =============================================================================
    // Example 5: Validation
    // =============================================================================
    std::cout << "\n5. Validation" << std::endl;
    std::cout << "--------------" << std::endl;

    std::vector<std::string> testStrings = {
        "SGVsbG8=",      // Valid
        "Zm9vYmFy",      // Valid
        "Invalid!",      // Invalid
        "Z",             // Invalid (wrong length)
        "SGVsbG8-",      // URL-safe valid
        "Zm9v_"          // URL-safe valid
    };

    for (const auto& str : testStrings) {
        bool standard = Base64Utils::isValid(str, false);
        bool urlSafe = Base64Utils::isValid(str, true);
        std::cout << "\"" << str << "\" - Standard: " << (standard ? "Valid" : "Invalid")
                  << ", URL-safe: " << (urlSafe ? "Valid" : "Invalid") << std::endl;
    }

    // =============================================================================
    // Example 6: Length Calculations
    // =============================================================================
    std::cout << "\n6. Length Calculations" << std::endl;
    std::cout << "-----------------------" << std::endl;

    std::vector<size_t> sizes = {1, 2, 3, 10, 100, 1000};
    for (size_t size : sizes) {
        size_t encodedLen = Base64Utils::encodedLength(size, true);
        size_t noPadLen = Base64Utils::encodedLength(size, false);
        std::cout << "Input " << size << " bytes -> Encoded: " << encodedLen
                  << " (no pad: " << noPadLen << ")" << std::endl;
    }

    // =============================================================================
    // Example 7: Practical Use Case - Simple Token Generation
    // =============================================================================
    std::cout << "\n7. Practical: Simple Token Generation" << std::endl;
    std::cout << "--------------------------------------" << std::endl;

    // Simulate a simple token: user_id:timestamp
    std::string userId = "user123";
    std::string timestamp = "1704067200";
    std::string tokenData = userId + ":" + timestamp;
    std::string token = Base64Utils::encode(tokenData, true, false);

    std::cout << "User ID: " << userId << std::endl;
    std::cout << "Timestamp: " << timestamp << std::endl;
    std::cout << "Token: " << token << std::endl;

    // Decode and verify
    std::string decodedToken = Base64Utils::decode(token, true);
    std::cout << "Decoded: " << decodedToken << std::endl;

    // =============================================================================
    // Example 8: Error Handling
    // =============================================================================
    std::cout << "\n8. Error Handling" << std::endl;
    std::cout << "------------------" << std::endl;

    try {
        Base64Utils::decode("Invalid!Base64@");
    } catch (const std::invalid_argument& e) {
        std::cout << "Caught expected error: " << e.what() << std::endl;
    }

    // =============================================================================
    // Example 9: Working with Raw Pointers
    // =============================================================================
    std::cout << "\n9. Raw Pointer Interface" << std::endl;
    std::cout << "-------------------------" << std::endl;

    const uint8_t rawData[] = {0x48, 0x65, 0x6C, 0x6C, 0x6F}; // "Hello"
    std::string rawEncoded = Base64Utils::encode(rawData, sizeof(rawData));
    std::cout << "Raw data encoded: " << rawEncoded << std::endl;

    // =============================================================================
    // Example 10: Round-trip Verification
    // =============================================================================
    std::cout << "\n10. Round-trip Verification" << std::endl;
    std::cout << "----------------------------" << std::endl;

    std::vector<std::string> testData = {
        "",
        "A",
        "AB",
        "ABC",
        "The quick brown fox jumps over the lazy dog",
        "1234567890!@#$%^&*()"
    };

    bool allPassed = true;
    for (const auto& data : testData) {
        std::string enc = Base64Utils::encode(data);
        std::string dec = Base64Utils::decode(enc);
        bool passed = (data == dec);
        allPassed = allPassed && passed;
        std::cout << "\"" << data.substr(0, 20) << (data.length() > 20 ? "..." : "")
                  << "\" -> " << (passed ? "PASS" : "FAIL") << std::endl;
    }

    std::cout << "\nAll tests: " << (allPassed ? "PASSED" : "FAILED") << std::endl;

    std::cout << "\n==============================================" << std::endl;
    std::cout << "Examples completed!" << std::endl;
    std::cout << "==============================================" << std::endl;

    return 0;
}
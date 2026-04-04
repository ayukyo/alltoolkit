import Foundation
@testable import crypto_utils

// MARK: - Test Runner

class CryptoUtilsTest {
    private var passed = 0
    private var failed = 0

    func run() {
        print("Running CryptoUtils Tests...")
        print("=" * 50)

        testHashFunctions()
        testHmacFunctions()
        testBase64Encoding()
        testHexEncoding()
        testUrlEncoding()
        testUuidGeneration()
        testRandomGeneration()
        testXorEncryption()
        testValidation()

        print("=" * 50)
        print("Results: \(passed) passed, \(failed) failed")
    }

    private func assertEqual<T: Equatable>(_ actual: T, _ expected: T, _ message: String) {
        if actual == expected {
            print("✓ \(message)")
            passed += 1
        } else {
            print("✗ \(message): expected \(expected), got \(actual)")
            failed += 1
        }
    }

    private func assertTrue(_ value: Bool, _ message: String) {
        if value {
            print("✓ \(message)")
            passed += 1
        } else {
            print("✗ \(message): expected true")
            failed += 1
        }
    }

    private func assertFalse(_ value: Bool, _ message: String) {
        if !value {
            print("✓ \(message)")
            passed += 1
        } else {
            print("✗ \(message): expected false")
            failed += 1
        }
    }

    // MARK: - Hash Tests

    private func testHashFunctions() {
        print("\n--- Hash Functions ---")

        // MD5 tests
        assertEqual(CryptoUtils.md5("hello"), "5d41402abc4b2a76b9719d911017c592", "MD5 of 'hello'")
        assertEqual(CryptoUtils.md5(""), "d41d8cd98f00b204e9800998ecf8427e", "MD5 of empty string")
        assertEqual(CryptoUtils.md5("The quick brown fox jumps over the lazy dog"), "9e107d9d372bb6826bd81d3542a419d6", "MD5 of pangram")

        // SHA1 tests
        assertEqual(CryptoUtils.sha1("hello"), "aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d", "SHA1 of 'hello'")
        assertEqual(CryptoUtils.sha1(""), "da39a3ee5e6b4b0d3255bfef95601890afd80709", "SHA1 of empty string")

        // SHA256 tests
        assertEqual(CryptoUtils.sha256("hello"), "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824", "SHA256 of 'hello'")
        assertEqual(CryptoUtils.sha256(""), "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855", "SHA256 of empty string")

        // SHA512 tests
        assertEqual(CryptoUtils.sha512("hello"), "9b71d224bd62f3785d96d46ad3ea3d73319bfbc2890caadae2dff72519673ca72323c3d99ba5c11d7c7acc6e14b8c5da0c4663475c2e5c3adef46f73bcdec043", "SHA512 of 'hello'")

        // Hash with data
        let data = "test".data(using: .utf8)!
        assertEqual(CryptoUtils.hash(data: data, algorithm: .md5), CryptoUtils.md5("test"), "Hash data with MD5")
        assertEqual(CryptoUtils.hash(data: data, algorithm: .sha256), CryptoUtils.sha256("test"), "Hash data with SHA256")
    }

    // MARK: - HMAC Tests

    private func testHmacFunctions() {
        print("\n--- HMAC Functions ---")

        let message = "hello"
        let key = "secret"

        // HMAC-SHA256 test
        let hmac256 = CryptoUtils.hmacSha256(message: message, key: key)
        assertEqual(hmac256.count, 64, "HMAC-SHA256 length is 64 chars")
        assertTrue(CryptoUtils.isValidSha256(hmac256), "HMAC-SHA256 is valid hex")

        // HMAC-SHA512 test
        let hmac512 = CryptoUtils.hmacSha512(message: message, key: key)
        assertEqual(hmac512.count, 128, "HMAC-SHA512 length is 128 chars")

        // Verify HMAC
        assertTrue(CryptoUtils.verifyHmacSha256(message: message, key: key, hmac: hmac256), "Verify correct HMAC")
        assertFalse(CryptoUtils.verifyHmacSha256(message: message, key: key, hmac: "wrong"), "Verify wrong HMAC fails")

        // Same message, same key = same HMAC
        let hmac256Again = CryptoUtils.hmacSha256(message: message, key: key)
        assertEqual(hmac256, hmac256Again, "HMAC is deterministic")
    }

    // MARK: - Base64 Tests

    private func testBase64Encoding() {
        print("\n--- Base64 Encoding ---")

        // Basic encoding/decoding
        let original = "Hello, World!"
        let encoded = CryptoUtils.base64Encode(original)
        let decoded = CryptoUtils.base64Decode(encoded)
        assertEqual(encoded, "SGVsbG8sIFdvcmxkIQ==", "Base64 encode")
        assertEqual(decoded, original, "Base64 decode")

        // Empty string
        assertEqual(CryptoUtils.base64Encode(""), "", "Base64 encode empty")
        assertEqual(CryptoUtils.base64Decode(""), "", "Base64 decode empty")

        // URL-safe Base64
        let urlEncoded = CryptoUtils.base64UrlEncode("hello+world/test", padding: true)
        assertFalse(urlEncoded.contains("+"), "URL-safe has no +")
        assertFalse(urlEncoded.contains("/"), "URL-safe has no /")
        let urlDecoded = CryptoUtils.base64UrlDecode(urlEncoded)
        assertEqual(urlDecoded, "hello+world/test", "URL-safe decode")

        // Without padding
        let noPadding = CryptoUtils.base64UrlEncode("hello", padding: false)
        assertFalse(noPadding.contains("="), "No padding when disabled")

        // Validation
        assertTrue(CryptoUtils.isValidBase64("SGVsbG8="), "Valid Base64")
        assertFalse(CryptoUtils.isValidBase64("Invalid!"), "Invalid Base64")
        assertFalse(CryptoUtils.isValidBase64("SGVsbG8"), "Invalid Base64 length")
    }

    // MARK: - Hex Tests

    private func testHexEncoding() {
        print("\n--- Hex Encoding ---")

        // Basic encoding/decoding
        let original = "Hello"
        let encoded = CryptoUtils.hexEncode(original)
        let decoded = CryptoUtils.hexDecode(encoded)
        assertEqual(encoded, "48656c6c6f", "Hex encode")
        assertEqual(decoded, original, "Hex decode")

        // Empty string
        assertEqual(CryptoUtils.hexEncode(""), "", "Hex encode empty")

        // Unicode
        let unicode = "你好"
        let unicodeHex = CryptoUtils.hexEncode(unicode)
        assertEqual(CryptoUtils.hexDecode(unicodeHex), unicode, "Hex encode/decode Unicode")

        // Validation
        assertTrue(CryptoUtils.isValidHex("48656c6c6f"), "Valid hex")
        assertFalse(CryptoUtils.isValidHex("48656c6c6"), "Invalid hex (odd length)")
        assertFalse(CryptoUtils.isValidHex("xyz"), "Invalid hex (bad chars)")
    }

    // MARK: - URL Encoding Tests

    private func testUrlEncoding() {
        print("\n--- URL Encoding ---")

        // Basic encoding
        let encoded = CryptoUtils.urlEncode("hello world")
        assertEqual(encoded, "hello%20world", "URL encode space")

        let decoded = CryptoUtils.urlDecode("hello%20world")
        assertEqual(decoded, "hello world", "URL decode space")

        // Component encoding
        let component = CryptoUtils.urlEncodeComponent("hello world!@#")
        assertTrue(component.contains("%20"), "Component encodes space")
        assertTrue(component.contains("%40"), "Component encodes @")

        // Round-trip
        let original = "test value & more"
        assertEqual(CryptoUtils.urlDecode(CryptoUtils.urlEncode(original)), original, "URL round-trip")
    }

    // MARK: - UUID Tests

    private func testUuidGeneration() {
        print("\n--- UUID Generation ---")

        // Standard UUID
        let uuid = CryptoUtils.uuid()
        assertEqual(uuid.count, 36, "UUID has 36 chars")
        assertTrue(uuid.contains("-"), "UUID contains hyphens")
        assertTrue(CryptoUtils.isValidUuid(uuid), "Generated UUID is valid")

        // Uppercase UUID
        let upper = CryptoUtils.uuidUpper()
        assertEqual(upper, upper.uppercased(), "UUID uppercase is uppercase")

        // Simple UUID (no hyphens)
        let simple = CryptoUtils.uuidSimple()
        assertEqual(simple.count, 32, "Simple UUID has 32 chars")
        assertFalse(simple.contains("-"), "Simple UUID has no hyphens")

        // Uniqueness (basic check)
        let uuid1 = CryptoUtils.uuid()
        let uuid2 = CryptoUtils.uuid()
        assertFalse(uuid1 == uuid2, "UUIDs are unique")

        // Validation
        assertTrue(CryptoUtils.isValidUuid("550e8400-e29b-41d4-a716-446655440000"), "Valid UUID")
        assertFalse(CryptoUtils.isValidUuid("not-a-uuid"), "Invalid UUID")
        assertFalse(CryptoUtils.isValidUuid("550e8400e29b41d4a716446655440000"), "Simple UUID not valid standard")
    }

    // MARK: - Random Generation Tests

    private func testRandomGeneration() {
        print("\n--- Random Generation ---")

        // Random string
        let random10 = CryptoUtils.randomString(length: 10, characters: "abc")
        assertEqual(random10.count, 10, "Random string has correct length")
        assertTrue(random10.allSatisfy { "abc".contains($0) }, "Random string uses only provided chars")

        // Alphanumeric
        let alpha = CryptoUtils.randomAlphanumeric(length: 16)
        assertEqual(alpha.count, 16, "Alphanumeric has correct length")
        assertTrue(alpha.allSatisfy { CryptoUtils.alphanumeric.contains($0) }, "Alphanumeric uses correct chars")

        // Numeric
        let numeric = CryptoUtils.randomNumeric(length: 8)
        assertEqual(numeric.count, 8, "Numeric has correct length")
        assertTrue(numeric.allSatisfy { $0.isNumber }, "Numeric contains only digits")

        // Hex
        let hex = CryptoUtils.randomHex(length: 16)
        assertEqual(hex.count, 16, "Hex has correct length")
        assertTrue(hex.allSatisfy { CryptoUtils.hexCharacters.contains($0) }, "Hex uses correct chars")

        // Password
        let password = CryptoUtils.randomPassword(length: 12)
        assertEqual(password.count, 12, "Password has correct length")
        assertTrue(password.contains { CryptoUtils.lowercaseLetters.contains($0) }, "Password has lowercase")
        assertTrue(password.contains { CryptoUtils.uppercaseLetters.contains($0) }, "Password has uppercase")
        assertTrue(password.contains { CryptoUtils.digits.contains($0) }, "Password has digit")
        assertTrue(password.contains { CryptoUtils.specialCharacters.contains($0) }, "Password has special char")

        // Edge cases
        assertEqual(CryptoUtils.randomString(length: 0, characters: "abc"), "", "Zero length returns empty")
        assertEqual(CryptoUtils.randomString(length: 5, characters: ""), "", "Empty charset returns empty")
    }

    // MARK: - XOR Encryption Tests

    private func testXorEncryption() {
        print("\n--- XOR Encryption ---")

        let message = "Hello, World!"
        let key = "secret"

        // Encrypt and decrypt
        let encrypted = CryptoUtils.xorEncrypt(message, key: key)
        let decrypted = CryptoUtils.xorDecrypt(encrypted, key: key)
        assertEqual(decrypted, message, "XOR round-trip")

        // Different keys produce different results
        let encrypted2 = CryptoUtils.xorEncrypt(message, key: "other")
        assertFalse(encrypted == encrypted2, "Different keys produce different ciphertext")

        // Wrong key fails
        let wrongDecrypt = CryptoUtils.xorDecrypt(encrypted, key: "wrong")
        assertFalse(wrongDecrypt == message, "Wrong key produces wrong plaintext")

        // Empty key returns original
        assertEqual(CryptoUtils.xorEncrypt(message, key: ""), message, "Empty key returns original")

        // Invalid base64 returns nil
        assertEqual(CryptoUtils.xorDecrypt("not-valid-base64!!!", key: key), nil, "Invalid base64 returns nil")
    }

    // MARK: - Validation Tests

    private func testValidation() {
        print("\n--- Validation ---")

        // MD5 validation
        assertTrue(CryptoUtils.isValidMd5("5d41402abc4b2a76b9719d911017c592"), "Valid MD5")
        assertFalse(CryptoUtils.isValidMd5("5d41402abc4b2a76b9719d911017c59"), "Invalid MD5 (short)")
        assertFalse(CryptoUtils.isValidMd5("5d41402abc4b2a76b9719d911017c59g"), "Invalid MD5 (bad char)")

        // SHA1 validation
        assertTrue(CryptoUtils.isValidSha1("aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d"), "Valid SHA1")
        assertFalse(CryptoUtils.isValidSha1("too-short"), "Invalid SHA1")

        // SHA256 validation
        assertTrue(CryptoUtils.isValidSha256("2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"), "Valid SHA256")
        assertFalse(CryptoUtils.isValidSha256("invalid"), "Invalid SHA256")

        // Generic hash validation
        assertTrue(CryptoUtils.isValidHash("5d41402abc4b2a76b9719d911017c592", algorithm: .md5), "Valid hash (MD5)")
        assertTrue(CryptoUtils.isValidHash("2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824", algorithm: .sha256), "Valid hash (SHA256)")
    }
}

// String extension for repeat operator
extension String {
    static func * (left: String, right: Int) -> String {
        return String(repeating: left, count: right)
    }
}

// Run tests
let test = CryptoUtilsTest()
test.run()
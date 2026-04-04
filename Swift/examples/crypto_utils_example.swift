import Foundation

// Import the crypto_utils module
// In a real project: import crypto_utils

// MARK: - Example 1: Hash Functions

func exampleHashFunctions() {
    print("=== Example 1: Hash Functions ===\n")

    let message = "Hello, World!"

    // MD5 (32 characters)
    let md5Hash = CryptoUtils.md5(message)
    print("MD5:    \(md5Hash)")

    // SHA1 (40 characters)
    let sha1Hash = CryptoUtils.sha1(message)
    print("SHA1:   \(sha1Hash)")

    // SHA256 (64 characters)
    let sha256Hash = CryptoUtils.sha256(message)
    print("SHA256: \(sha256Hash)")

    // SHA512 (128 characters)
    let sha512Hash = CryptoUtils.sha512(message)
    print("SHA512: \(sha512Hash)")

    // Hash binary data
    if let data = message.data(using: .utf8) {
        let dataHash = CryptoUtils.hash(data: data, algorithm: .sha256)
        print("Data hash (SHA256): \(dataHash)")
    }

    print()
}

// MARK: - Example 2: HMAC (Message Authentication)

func exampleHmac() {
    print("=== Example 2: HMAC (Message Authentication) ===\n")

    let message = "Important message"
    let secretKey = "my-secret-key-123"

    // Generate HMAC-SHA256
    let hmac = CryptoUtils.hmacSha256(message: message, key: secretKey)
    print("Message: \(message)")
    print("Key: \(secretKey)")
    print("HMAC-SHA256: \(hmac)")

    // Verify the HMAC
    let isValid = CryptoUtils.verifyHmacSha256(message: message, key: secretKey, hmac: hmac)
    print("HMAC valid: \(isValid)")

    // Try with wrong key
    let isInvalid = CryptoUtils.verifyHmacSha256(message: message, key: "wrong-key", hmac: hmac)
    print("HMAC valid with wrong key: \(isInvalid)")

    print()
}

// MARK: - Example 3: Base64 Encoding

func exampleBase64() {
    print("=== Example 3: Base64 Encoding ===\n")

    let original = "Swift is awesome! 🚀"

    // Standard Base64
    let encoded = CryptoUtils.base64Encode(original)
    print("Original: \(original)")
    print("Base64:   \(encoded)")

    // Decode back
    if let decoded = CryptoUtils.base64Decode(encoded) {
        print("Decoded:  \(decoded)")
    }

    // URL-safe Base64 (for URLs and filenames)
    let urlUnsafe = "user+name/file@domain.com"
    let urlSafe = CryptoUtils.base64UrlEncode(urlUnsafe, padding: false)
    print("\nURL-unsafe: \(urlUnsafe)")
    print("URL-safe:   \(urlSafe)")

    if let decoded = CryptoUtils.base64UrlDecode(urlSafe) {
        print("Decoded:    \(decoded)")
    }

    // Validate Base64
    print("\nIs valid Base64: \(CryptoUtils.isValidBase64(encoded))")
    print("Is valid Base64: \(CryptoUtils.isValidBase64("not-valid!"))")

    print()
}

// MARK: - Example 4: Hex Encoding

func exampleHexEncoding() {
    print("=== Example 4: Hex Encoding ===\n")

    let text = "Hello, 世界!"

    // Encode to hex
    let hex = CryptoUtils.hexEncode(text)
    print("Text: \(text)")
    print("Hex:  \(hex)")

    // Decode from hex
    if let decoded = CryptoUtils.hexDecode(hex) {
        print("Back: \(decoded)")
    }

    // Validate hex strings
    print("\nIs valid hex: \(CryptoUtils.isValidHex("48656c6c6f"))")
    print("Is valid hex: \(CryptoUtils.isValidHex("xyz"))")

    print()
}

// MARK: - Example 5: URL Encoding

func exampleUrlEncoding() {
    print("=== Example 5: URL Encoding ===\n")

    let searchQuery = "swift programming language"
    let special = "hello@world.com"

    // Standard URL encoding
    let encoded = CryptoUtils.urlEncode(searchQuery)
    print("Query:   \(searchQuery)")
    print("Encoded: \(encoded)")

    // Decode
    let decoded = CryptoUtils.urlDecode(encoded)
    print("Decoded: \(decoded)")

    // Component encoding (more aggressive)
    let component = CryptoUtils.urlEncodeComponent(special)
    print("\nSpecial:        \(special)")
    print("As component:   \(component)")

    print()
}

// MARK: - Example 6: UUID Generation

func exampleUuid() {
    print("=== Example 6: UUID Generation ===\n")

    // Standard UUID v4
    let uuid = CryptoUtils.uuid()
    print("Standard UUID: \(uuid)")

    // Uppercase
    let uuidUpper = CryptoUtils.uuidUpper()
    print("Uppercase:     \(uuidUpper)")

    // Simple (no hyphens)
    let uuidSimple = CryptoUtils.uuidSimple()
    print("Simple:        \(uuidSimple)")

    // Validate UUID
    print("\nIs valid UUID: \(CryptoUtils.isValidUuid(uuid))")
    print("Is valid UUID: \(CryptoUtils.isValidUuid("not-a-uuid"))")

    // Generate multiple unique IDs
    print("\n5 Unique UUIDs:")
    for i in 1...5 {
        print("  \(i). \(CryptoUtils.uuid())")
    }

    print()
}

// MARK: - Example 7: Random String Generation

func exampleRandomGeneration() {
    print("=== Example 7: Random String Generation ===\n")

    // Random alphanumeric
    let token = CryptoUtils.randomAlphanumeric(length: 32)
    print("32-char token:    \(token)")

    // Random numeric (e.g., OTP code)
    let otp = CryptoUtils.randomNumeric(length: 6)
    print("6-digit OTP:      \(otp)")

    // Random hex
    let hexId = CryptoUtils.randomHex(length: 16)
    print("16-char hex ID:   \(hexId)")

    // Custom character set
    let custom = CryptoUtils.randomString(length: 10, characters: "ABC123")
    print("Custom chars:     \(custom)")

    // Secure password
    let password = CryptoUtils.randomPassword(length: 16)
    print("Secure password:  \(password)")

    // Multiple passwords
    print("\n5 Secure Passwords:")
    for i in 1...5 {
        print("  \(i). \(CryptoUtils.randomPassword(length: 12))")
    }

    print()
}

// MARK: - Example 8: XOR Encryption (Simple)

func exampleXorEncryption() {
    print("=== Example 8: XOR Encryption ===\n")

    let secretMessage = "This is a secret!"
    let key = "my-encryption-key"

    print("Original: \(secretMessage)")
    print("Key:      \(key)")

    // Encrypt
    let encrypted = CryptoUtils.xorEncrypt(secretMessage, key: key)
    print("Encrypted (Base64): \(encrypted)")

    // Decrypt
    if let decrypted = CryptoUtils.xorDecrypt(encrypted, key: key) {
        print("Decrypted: \(decrypted)")
    }

    // Wrong key
    if let wrong = CryptoUtils.xorDecrypt(encrypted, key: "wrong-key") {
        print("With wrong key: \(wrong)")
    }

    print()
}

// MARK: - Example 9: Hash Validation

func exampleHashValidation() {
    print("=== Example 9: Hash Validation ===\n")

    let hashes = [
        "5d41402abc4b2a76b9719d911017c592",  // MD5
        "aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d",  // SHA1
        "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824",  // SHA256
    ]

    for hash in hashes {
        print("Hash: \(hash)")
        print("  Valid MD5:    \(CryptoUtils.isValidMd5(hash))")
        print("  Valid SHA1:   \(CryptoUtils.isValidSha1(hash))")
        print("  Valid SHA256: \(CryptoUtils.isValidSha256(hash))")
        print()
    }

    // Generic validation
    print("Generic validation:")
    print("  MD5:    \(CryptoUtils.isValidHash(hashes[0], algorithm: .md5))")
    print("  SHA1:   \(CryptoUtils.isValidHash(hashes[1], algorithm: .sha1))")
    print("  SHA256: \(CryptoUtils.isValidHash(hashes[2], algorithm: .sha256))")

    print()
}

// MARK: - Example 10: Practical Use Cases

func examplePracticalUseCases() {
    print("=== Example 10: Practical Use Cases ===\n")

    // Use case 1: API request signing
    print("1. API Request Signing:")
    let apiKey = "sk-1234567890abcdef"
    let timestamp = String(Date().timeIntervalSince1970)
    let payload = "GET/api/v1/users\(timestamp)"
    let signature = CryptoUtils.hmacSha256(message: payload, key: apiKey)
    print("   Request signature: \(signature.prefix(16))...")

    // Use case 2: Password reset token
    print("\n2. Password Reset Token:")
    let resetToken = CryptoUtils.randomAlphanumeric(length: 32)
    print("   Token: \(resetToken)")

    // Use case 3: File checksum
    print("\n3. File Checksum:")
    let fileContent = "File contents here..."
    let checksum = CryptoUtils.sha256(fileContent)
    print("   SHA256: \(checksum.prefix(16))...")

    // Use case 4: Session ID
    print("\n4. Session ID:")
    let sessionId = CryptoUtils.uuidSimple()
    print("   Session: \(sessionId)")

    // Use case 5: URL-safe token for email verification
    print("\n5. Email Verification Token:")
    let email = "user@example.com"
    let verificationToken = CryptoUtils.base64UrlEncode(email + "_" + CryptoUtils.randomAlphanumeric(length: 16), padding: false)
    print("   Token: \(verificationToken)")

    print()
}

// MARK: - Main

func main() {
    print("Swift CryptoUtils Examples")
    print("==========================\n")

    exampleHashFunctions()
    exampleHmac()
    exampleBase64()
    exampleHexEncoding()
    exampleUrlEncoding()
    exampleUuid()
    exampleRandomGeneration()
    exampleXorEncryption()
    exampleHashValidation()
    examplePracticalUseCases()

    print("All examples completed!")
}

main()
/**
 * AllToolkit - Kotlin Crypto Utils Example
 * 
 * 展示 crypto_utils 模块的所有功能用法
 */

import crypto_utils.CryptoUtils
import crypto_utils.CharSets

fun main() {
    println("=== Kotlin Crypto Utils Examples ===\n")
    
    // ==================== 1. 哈希计算 ====================
    println("1. Hash Functions")
    println("-".repeat(40))
    
    val message = "Hello, World!"
    println("Message: $message")
    println("MD5:    ${CryptoUtils.md5(message)}")
    println("SHA-1:  ${CryptoUtils.sha1(message)}")
    println("SHA-256: ${CryptoUtils.sha256(message)}")
    println("SHA-512: ${CryptoUtils.sha512(message)}")
    
    // 字节数组哈希
    val bytes = message.toByteArray(Charsets.UTF_8)
    println("SHA-256 (bytes): ${CryptoUtils.sha256Bytes(bytes)}")
    println()
    
    // ==================== 2. HMAC 签名 ====================
    println("2. HMAC Functions")
    println("-".repeat(40))
    
    val key = "secret_key"
    val payload = "important_data"
    val hmac = CryptoUtils.hmacSha256(payload, key)
    println("Payload: $payload")
    println("Key: $key")
    println("HMAC-SHA256: $hmac")
    
    // 验证签名
    val isValid = CryptoUtils.verifyHmacSha256(payload, key, hmac)
    println("Verification: $isValid")
    println()
    
    // ==================== 3. Base64 编码 ====================
    println("3. Base64 Encoding")
    println("-".repeat(40))
    
    val text = "Hello, Kotlin!"
    val base64 = CryptoUtils.base64Encode(text)
    println("Original: $text")
    println("Base64:   $base64")
    println("Decoded:  ${CryptoUtils.base64Decode(base64)}")
    
    // URL 安全 Base64
    val urlText = "user+name/file"
    val urlSafe = CryptoUtils.base64UrlEncode(urlText, padding = false)
    println("URL Safe: $urlSafe")
    println()
    
    // ==================== 4. 十六进制编码 ====================
    println("4. Hex Encoding")
    println("-".repeat(40))
    
    val hexInput = "Binary Data"
    val hex = CryptoUtils.hexEncode(hexInput)
    println("Original: $hexInput")
    println("Hex:      $hex")
    println("Decoded:  ${CryptoUtils.hexDecode(hex)}")
    println()
    
    // ==================== 5. UUID 生成 ====================
    println("5. UUID Generation")
    println("-".repeat(40))
    
    println("Standard UUID: ${CryptoUtils.uuid()}")
    println("Simple UUID:   ${CryptoUtils.uuidSimple()}")
    println("Upper UUID:    ${CryptoUtils.uuidUpper()}")
    
    // 验证 UUID
    val testUuid = "550e8400-e29b-41d4-a716-446655440000"
    println("Is valid UUID: ${CryptoUtils.isValidUuid(testUuid)}")
    println()
    
    // ==================== 6. 随机字符串 ====================
    println("6. Random String Generation")
    println("-".repeat(40))
    
    println("Random 16 chars:  ${CryptoUtils.randomString(16)}")
    println("Alphanumeric 32:  ${CryptoUtils.randomAlphanumeric(32)}")
    println("Numeric 6 (OTP):  ${CryptoUtils.randomNumeric(6)}")
    println("Hex 16:           ${CryptoUtils.randomHex(16)}")
    println("Password 16:      ${CryptoUtils.randomPassword(16)}")
    println()
    
    // ==================== 7. XOR 加密 ====================
    println("7. XOR Encryption")
    println("-".repeat(40))
    
    val secret = "Secret Message"
    val xorKey = "my_secret_key"
    val encrypted = CryptoUtils.xorEncrypt(secret, xorKey)
    val decrypted = CryptoUtils.xorDecrypt(encrypted, xorKey)
    println("Original:  $secret")
    println("Encrypted: $encrypted")
    println("Decrypted: $decrypted")
    println()
    
    // ==================== 8. 格式验证 ====================
    println("8. Format Validation")
    println("-".repeat(40))
    
    val md5Hash = "5d41402abc4b2a76b9719d911017c592"
    val sha256Hash = "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"
    
    println("MD5 valid:    ${CryptoUtils.isValidMd5(md5Hash)}")
    println("SHA256 valid: ${CryptoUtils.isValidSha256(sha256Hash)}")
    println("Base64 valid: ${CryptoUtils.isValidBase64("SGVsbG8=")}")
    println("Hex valid:    ${CryptoUtils.isValidHex("deadbeef")}")
    println()
    
    // ==================== 9. URL 编码 ====================
    println("9. URL Encoding")
    println("-".repeat(40))
    
    val urlText2 = "hello world! @#$"
    val urlEncoded = CryptoUtils.urlEncode(urlText2)
    println("Original: $urlText2")
    println("Encoded:  $urlEncoded")
    println("Decoded:  ${CryptoUtils.urlDecode(urlEncoded)}")
    println()
    
    // ==================== 10. 字符集常量 ====================
    println("10. Character Sets")
    println("-".repeat(40))
    
    println("Lowercase: ${CharSets.LOWERCASE}")
    println("Uppercase: ${CharSets.UPPERCASE}")
    println("Digits:    ${CharSets.DIGITS}")
    println("Special:   ${CharSets.SPECIAL.take(10)}...")
    println()
    
    // ==================== 11. 实际应用场景 ====================
    println("11. Practical Use Cases")
    println("-".repeat(40))
    
    // API 请求签名
    println("API Request Signing:")
    val apiKey = "api_secret_123"
    val requestData = "user_id=123&action=delete"
    val signature = CryptoUtils.hmacSha256(requestData, apiKey)
    println("  Request: $requestData")
    println("  Signature: $signature")
    
    // 密码哈希存储
    println("\nPassword Hashing:")
    val password = "user_password"
    val passwordHash = CryptoUtils.sha256(password)
    println("  Password: $password")
    println("  Hash: $passwordHash")
    
    // 生成 API Token
    println("\nAPI Token Generation:")
    val token = CryptoUtils.randomAlphanumeric(32)
    println("  Token: $token")
    
    // 生成会话 ID
    println("\nSession ID:")
    val sessionId = CryptoUtils.uuidSimple()
    println("  Session ID: $sessionId")
    
    println("\n=== All Examples Completed ===")
}

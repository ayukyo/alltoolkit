/**
 * AllToolkit - Kotlin Crypto Utilities Test
 * 
 * 完整的单元测试套件，覆盖所有加密工具函数
 */

package crypto_utils

fun main() {
    println("=== Kotlin Crypto Utils Test Suite ===\n")
    
    var passed = 0
    var failed = 0
    
    // ==================== 哈希函数测试 ====================
    
    test("MD5 Hash") {
        val hash = CryptoUtils.md5("hello")
        assertEquals("5d41402abc4b2a76b9719d911017c592", hash)
    }.also { if (it) passed++ else failed++ }
    
    test("SHA-256 Hash") {
        val hash = CryptoUtils.sha256("hello")
        assertEquals("2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824", hash)
    }.also { if (it) passed++ else failed++ }
    
    test("SHA-1 Hash") {
        val hash = CryptoUtils.sha1("hello")
        assertEquals("aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d", hash)
    }.also { if (it) passed++ else failed++ }
    
    test("SHA-512 Hash") {
        val hash = CryptoUtils.sha512("hello")
        assertEquals(128, hash.length)
        assertTrue(hash.matches(Regex("^[0-9a-f]{128}$")))
    }.also { if (it) passed++ else failed++ }
    
    test("SHA-256 Bytes") {
        val data = "hello".toByteArray(Charsets.UTF_8)
        val hash = CryptoUtils.sha256Bytes(data)
        assertEquals(CryptoUtils.sha256("hello"), hash)
    }.also { if (it) passed++ else failed++ }
    
    // ==================== HMAC 测试 ====================
    
    test("HMAC-SHA256") {
        val hmac = CryptoUtils.hmacSha256("message", "key")
        assertEquals(64, hmac.length)
        assertTrue(CryptoUtils.isValidSha256(hmac))
    }.also { if (it) passed++ else failed++ }
    
    test("HMAC-SHA512") {
        val hmac = CryptoUtils.hmacSha512("message", "key")
        assertEquals(128, hmac.length)
        assertTrue(CryptoUtils.isValidSha512(hmac))
    }.also { if (it) passed++ else failed++ }
    
    test("Verify HMAC-SHA256") {
        val hmac = CryptoUtils.hmacSha256("message", "key")
        assertTrue(CryptoUtils.verifyHmacSha256("message", "key", hmac))
        assertFalse(CryptoUtils.verifyHmacSha256("message", "key", "invalid"))
    }.also { if (it) passed++ else failed++ }
    
    // ==================== Base64 测试 ====================
    
    test("Base64 Encode/Decode") {
        val original = "Hello, World!"
        val encoded = CryptoUtils.base64Encode(original)
        val decoded = CryptoUtils.base64Decode(encoded)
        assertEquals("SGVsbG8sIFdvcmxkIQ==", encoded)
        assertEquals(original, decoded)
    }.also { if (it) passed++ else failed++ }
    
    test("Base64 Encode Bytes") {
        val data = byteArrayOf(0x00, 0x01, 0x02, 0xFF.toByte())
        val encoded = CryptoUtils.base64EncodeBytes(data)
        val decoded = CryptoUtils.base64DecodeToBytes(encoded)
        assertTrue(data.contentEquals(decoded))
    }.also { if (it) passed++ else failed++ }
    
    test("Base64 URL Safe") {
        val original = "user+name/file"
        val encoded = CryptoUtils.base64UrlEncode(original, padding = false)
        val decoded = CryptoUtils.base64UrlDecode(encoded)
        assertEquals(original, decoded)
        assertFalse(encoded.contains('+'))
        assertFalse(encoded.contains('/'))
        assertFalse(encoded.contains('='))
    }.also { if (it) passed++ else failed++ }
    
    test("Base64 Invalid") {
        val result = CryptoUtils.base64Decode("invalid!!!")
        assertNull(result)
    }.also { if (it) passed++ else failed++ }
    
    // ==================== 十六进制测试 ====================
    
    test("Hex Encode/Decode") {
        val original = "Hello, World!"
        val encoded = CryptoUtils.hexEncode(original)
        val decoded = CryptoUtils.hexDecode(encoded)
        assertEquals(original, decoded)
        assertTrue(CryptoUtils.isValidHex(encoded))
    }.also { if (it) passed++ else failed++ }
    
    test("Bytes To Hex") {
        val bytes = byteArrayOf(0x00, 0x0F, 0xFF.toByte())
        val hex = CryptoUtils.bytesToHex(bytes)
        assertEquals("000fff", hex)
    }.also { if (it) passed++ else failed++ }
    
    test("Hex To Bytes") {
        val hex = "000fff"
        val bytes = CryptoUtils.hexToBytes(hex)
        assertTrue(byteArrayOf(0x00, 0x0F, 0xFF.toByte()).contentEquals(bytes))
    }.also { if (it) passed++ else failed++ }
    
    // ==================== UUID 测试 ====================
    
    test("UUID Generation") {
        val uuid = CryptoUtils.uuid()
        assertEquals(36, uuid.length)
        assertTrue(CryptoUtils.isValidUuid(uuid))
    }.also { if (it) passed++ else failed++ }
    
    test("UUID Simple") {
        val uuid = CryptoUtils.uuidSimple()
        assertEquals(32, uuid.length)
        assertFalse(uuid.contains("-"))
    }.also { if (it) passed++ else failed++ }
    
    test("UUID Upper") {
        val uuid = CryptoUtils.uuidUpper()
        assertTrue(uuid == uuid.uppercase())
    }.also { if (it) passed++ else failed++ }
    
    test("UUID Validation") {
        assertTrue(CryptoUtils.isValidUuid("550e8400-e29b-41d4-a716-446655440000"))
        assertFalse(CryptoUtils.isValidUuid("invalid"))
        assertFalse(CryptoUtils.isValidUuid("550e8400e29b41d4a716446655440000"))
    }.also { if (it) passed++ else failed++ }
    
    // ==================== 随机字符串测试 ====================
    
    test("Random String") {
        val str = CryptoUtils.randomString(16)
        assertEquals(16, str.length)
    }.also { if (it) passed++ else failed++ }
    
    test("Random Alphanumeric") {
        val str = CryptoUtils.randomAlphanumeric(32)
        assertEquals(32, str.length)
        assertTrue(str.all { it.isLetterOrDigit() })
    }.also { if (it) passed++ else failed++ }
    
    test("Random Numeric") {
        val str = CryptoUtils.randomNumeric(6)
        assertEquals(6, str.length)
        assertTrue(str.all { it.isDigit() })
    }.also { if (it) passed++ else failed++ }
    
    test("Random Hex") {
        val str = CryptoUtils.randomHex(16)
        assertEquals(16, str.length)
        assertTrue(str.all { it in '0'..'9' || it in 'a'..'f' })
    }.also { if (it) passed++ else failed++ }
    
    test("Random Password") {
        val password = CryptoUtils.randomPassword(16)
        assertEquals(16, password.length)
        assertTrue(password.any { it.isLowerCase() })
        assertTrue(password.any { it.isUpperCase() })
        assertTrue(password.any { it.isDigit() })
        assertTrue(password.any { !it.isLetterOrDigit() })
    }.also { if (it) passed++ else failed++ }
    
    // ==================== XOR 加密测试 ====================
    
    test("XOR Encrypt/Decrypt") {
        val original = "Secret Message"
        val key = "my_key"
        val encrypted = CryptoUtils.xorEncrypt(original, key)
        val decrypted = CryptoUtils.xorDecrypt(encrypted, key)
        assertEquals(original, decrypted)
    }.also { if (it) passed++ else failed++ }
    
    test("XOR Empty Key") {
        val original = "Hello"
        val encrypted = CryptoUtils.xorEncrypt(original, "")
        val decrypted = CryptoUtils.xorDecrypt(encrypted, "")
        assertEquals(original, decrypted)
    }.also { if (it) passed++ else failed++ }
    
    // ==================== 验证函数测试 ====================
    
    test("Is Valid MD5") {
        assertTrue(CryptoUtils.isValidMd5("5d41402abc4b2a76b9719d911017c592"))
        assertFalse(CryptoUtils.isValidMd5("invalid"))
        assertFalse(CryptoUtils.isValidMd5("5d41402abc4b2a76b9719d911017c59"))
    }.also { if (it) passed++ else failed++ }
    
    test("Is Valid SHA256") {
        assertTrue(CryptoUtils.isValidSha256("2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"))
        assertFalse(CryptoUtils.isValidSha256("invalid"))
        assertFalse(CryptoUtils.isValidSha256("2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b982"))
    }.also { if (it) passed++ else failed++ }
    
    test("Is Valid Base64") {
        assertTrue(CryptoUtils.isValidBase64("SGVsbG8="))
        assertFalse(CryptoUtils.isValidBase64("invalid!!!"))
    }.also { if (it) passed++ else failed++ }
    
    test("Is Valid Hex") {
        assertTrue(CryptoUtils.isValidHex("deadbeef"))
        assertFalse(CryptoUtils.isValidHex("xyz"))
        assertFalse(CryptoUtils.isValidHex("abc"))
    }.also { if (it) passed++ else failed++ }
    
    test("URL Encode/Decode") {
        val original = "hello world"
        val encoded = CryptoUtils.urlEncode(original)
        val decoded = CryptoUtils.urlDecode(encoded)
        assertEquals("hello+world", encoded)
        assertEquals(original, decoded)
    }.also { if (it) passed++ else failed++ }
    
    // ==================== 字符集常量测试 ====================
    
    test("CharSets Constants") {
        assertEquals(26, CharSets.LOWERCASE.length)
        assertEquals(26, CharSets.UPPERCASE.length)
        assertEquals(10, CharSets.DIGITS.length)
        assertEquals(62, CharSets.ALPHANUMERIC.length)
        assertTrue(CharSets.SPECIAL.length > 0)
    }.also { if (it) passed++ else failed++ }
    
    // ==================== 结果输出 ====================
    
    println("\n=== Test Results ===")
    println("Passed: $passed")
    println("Failed: $failed")
    println("Total:  ${passed + failed}")
    
    if (failed > 0) {
        System.exit(1)
    }
}

// ==================== 测试辅助函数 ====================

inline fun test(name: String, block: () -> Unit): Boolean {
    return try {
        block()
        println("✓ $name")
        true
    } catch (e: AssertionError) {
        println("✗ $name: ${e.message}")
        false
    } catch (e: Exception) {
        println("✗ $name: ${e.message}")
        false
    }
}

fun assertEquals(expected: Any?, actual: Any?) {
    if (expected != actual) {
        throw AssertionError("Expected: $expected, Actual: $actual")
    }
}

fun assertTrue(condition: Boolean, message: String = "Expected true") {
    if (!condition) {
        throw AssertionError(message)
    }
}

fun assertFalse(condition: Boolean, message: String = "Expected false") {
    if (condition) {
        throw AssertionError(message)
    }
}

fun assertNull(actual: Any?) {
    if (actual != null) {
        throw AssertionError("Expected null, Actual: $actual")
    }
}

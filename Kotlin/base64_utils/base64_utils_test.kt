package base64_utils

/**
 * Base64 工具类单元测试
 */
fun main() {
    println("Running Base64Utils Tests...")
    println("=".repeat(50))

    var passed = 0
    var failed = 0

    // Test 1: Basic encoding
    try {
        val encoded = Base64Utils.encode("Hello, World!")
        if (encoded == "SGVsbG8sIFdvcmxkIQ==") {
            println("PASSED: Test 1 - Basic encoding")
            passed++
        } else {
            println("FAILED: Test 1 - Expected 'SGVsbG8sIFdvcmxkIQ==' but got '$encoded'")
            failed++
        }
    } catch (e: Exception) {
        println("FAILED: Test 1 - ${e.message}")
        failed++
    }

    // Test 2: Basic decoding
    try {
        val decoded = Base64Utils.decode("SGVsbG8sIFdvcmxkIQ==")
        if (decoded == "Hello, World!") {
            println("PASSED: Test 2 - Basic decoding")
            passed++
        } else {
            println("FAILED: Test 2 - Expected 'Hello, World!' but got '$decoded'")
            failed++
        }
    } catch (e: Exception) {
        println("FAILED: Test 2 - ${e.message}")
        failed++
    }

    // Test 3: Round-trip encoding/decoding
    try {
        val original = "Test string for round-trip"
        val encoded = Base64Utils.encode(original)
        val decoded = Base64Utils.decode(encoded)
        if (decoded == original) {
            println("PASSED: Test 3 - Round-trip")
            passed++
        } else {
            println("FAILED: Test 3 - Round-trip failed")
            failed++
        }
    } catch (e: Exception) {
        println("FAILED: Test 3 - ${e.message}")
        failed++
    }

    // Test 4: URL-safe encoding without padding
    try {
        val encoded = Base64Utils.encodeUrlSafe("user+name/file", padding = false)
        if (encoded == "dXNlcituYW1lL2ZpbGU") {
            println("PASSED: Test 4 - URL-safe encoding without padding")
            passed++
        } else {
            println("FAILED: Test 4 - Expected 'dXNlcituYW1lL2ZpbGU' but got '$encoded'")
            failed++
        }
    } catch (e: Exception) {
        println("FAILED: Test 4 - ${e.message}")
        failed++
    }

    // Test 5: URL-safe encoding with padding
    try {
        val encoded = Base64Utils.encodeUrlSafe("user+name/file", padding = true)
        if (encoded == "dXNlcituYW1lL2ZpbGU=") {
            println("PASSED: Test 5 - URL-safe encoding with padding")
            passed++
        } else {
            println("FAILED: Test 5 - Expected 'dXNlcituYW1lL2ZpbGU=' but got '$encoded'")
            failed++
        }
    } catch (e: Exception) {
        println("FAILED: Test 5 - ${e.message}")
        failed++
    }

    // Test 6: URL-safe decoding
    try {
        val decoded = Base64Utils.decodeUrlSafe("dXNlcituYW1lL2ZpbGU")
        if (decoded == "user+name/file") {
            println("PASSED: Test 6 - URL-safe decoding")
            passed++
        } else {
            println("FAILED: Test 6 - Expected 'user+name/file' but got '$decoded'")
            failed++
        }
    } catch (e: Exception) {
        println("FAILED: Test 6 - ${e.message}")
        failed++
    }

    // Test 7: Empty string encoding
    try {
        val encoded = Base64Utils.encode("")
        if (encoded == "") {
            println("PASSED: Test 7 - Empty string encoding")
            passed++
        } else {
            println("FAILED: Test 7 - Expected '' but got '$encoded'")
            failed++
        }
    } catch (e: Exception) {
        println("FAILED: Test 7 - ${e.message}")
        failed++
    }

    // Test 8: Empty string decoding
    try {
        val decoded = Base64Utils.decode("")
        if (decoded == "") {
            println("PASSED: Test 8 - Empty string decoding")
            passed++
        } else {
            println("FAILED: Test 8 - Expected '' but got '$decoded'")
            failed++
        }
    } catch (e: Exception) {
        println("FAILED: Test 8 - ${e.message}")
        failed++
    }

    // Test 9: Binary data encoding
    try {
        val data = byteArrayOf(0x00, 0x01, 0x02, 0xFF.toByte())
        val encoded = Base64Utils.encode(data)
        if (encoded == "AAEC/w==") {
            println("PASSED: Test 9 - Binary data encoding")
            passed++
        } else {
            println("FAILED: Test 9 - Expected 'AAEC/w==' but got '$encoded'")
            failed++
        }
    } catch (e: Exception) {
        println("FAILED: Test 9 - ${e.message}")
        failed++
    }

    // Test 10: Binary data decoding
    try {
        val decoded = Base64Utils.decodeToBytes("AAEC/w==")
        val expected = byteArrayOf(0x00, 0x01, 0x02, 0xFF.toByte())
        if (decoded.contentEquals(expected)) {
            println("PASSED: Test 10 - Binary data decoding")
            passed++
        } else {
            println("FAILED: Test 10 - Byte arrays not equal")
            failed++
        }
    } catch (e: Exception) {
        println("FAILED: Test 10 - ${e.message}")
        failed++
    }

    // Test 11: Unicode encoding (Chinese)
    try {
        val original = "你好世界"
        val encoded = Base64Utils.encode(original)
        val decoded = Base64Utils.decode(encoded)
        if (decoded == original) {
            println("PASSED: Test 11 - Unicode encoding (Chinese)")
            passed++
        } else {
            println("FAILED: Test 11 - Unicode round-trip failed")
            failed++
        }
    } catch (e: Exception) {
        println("FAILED: Test 11 - ${e.message}")
        failed++
    }

    // Test 12: Unicode encoding (Emoji)
    try {
        val original = "Hello 👋 World 🌍"
        val encoded = Base64Utils.encode(original)
        val decoded = Base64Utils.decode(encoded)
        if (decoded == original) {
            println("PASSED: Test 12 - Unicode encoding (Emoji)")
            passed++
        } else {
            println("FAILED: Test 12 - Emoji round-trip failed")
            failed++
        }
    } catch (e: Exception) {
        println("FAILED: Test 12 - ${e.message}")
        failed++
    }

    // Test 13: Invalid Base64 handling
    try {
        val result = Base64Utils.decodeOrNull("Invalid!@#")
        if (result == null) {
            println("PASSED: Test 13 - Invalid Base64 returns null")
            passed++
        } else {
            println("FAILED: Test 13 - Expected null but got '$result'")
            failed++
        }
    } catch (e: Exception) {
        println("FAILED: Test 13 - ${e.message}")
        failed++
    }

    // Test 14: Valid Base64 check
    try {
        val valid = Base64Utils.isValid("SGVsbG8=")
        val invalid = Base64Utils.isValid("Invalid!")
        if (valid && !invalid) {
            println("PASSED: Test 14 - Valid Base64 check")
            passed++
        } else {
            println("FAILED: Test 14 - Validation check failed")
            failed++
        }
    } catch (e: Exception) {
        println("FAILED: Test 14 - ${e.message}")
        failed++
    }

    // Test 15: Convert standard to URL-safe
    try {
        val standard = "SGVsbG8sIFdvcmxkIQ=="
        val urlSafe = Base64Utils.toUrlSafe(standard, padding = false)
        val decoded = Base64Utils.decodeUrlSafe(urlSafe)
        if (decoded == "Hello, World!") {
            println("PASSED: Test 15 - Convert standard to URL-safe")
            passed++
        } else {
            println("FAILED: Test 15 - Conversion failed")
            failed++
        }
    } catch (e: Exception) {
        println("FAILED: Test 15 - ${e.message}")
        failed++
    }

    // Test 16: Convert URL-safe to standard
    try {
        val urlSafe = "SGVsbG8sIFdvcmxkIQ"
        val standard = Base64Utils.fromUrlSafe(urlSafe)
        val decoded = Base64Utils.decode(standard)
        if (decoded == "Hello, World!") {
            println("PASSED: Test 16 - Convert URL-safe to standard")
            passed++
        } else {
            println("FAILED: Test 16 - Conversion failed")
            failed++
        }
    } catch (e: Exception) {
        println("FAILED: Test 16 - ${e.message}")
        failed++
    }

    // Test 17: Encoded length calculation
    try {
        val len1 = Base64Utils.encodedLength(100, padding = true)
        val len2 = Base64Utils.encodedLength(100, padding = false)
        if (len1 == 136 && len2 == 136) {
            println("PASSED: Test 17 - Encoded length calculation")
            passed++
        } else {
            println("FAILED: Test 17 - Length calculation failed")
            failed++
        }
    } catch (e: Exception) {
        println("FAILED: Test 17 - ${e.message}")
        failed++
    }

    // Test 18: Decoded max length calculation
    try {
        val len = Base64Utils.decodedMaxLength(136)
        if (len == 102) {
            println("PASSED: Test 18 - Decoded max length")
            passed++
        } else {
            println("FAILED: Test 18 - Expected 102 but got $len")
            failed++
        }
    } catch (e: Exception) {
        println("FAILED: Test 18 - ${e.message}")
        failed++
    }

    // Test 19: Extension function - toBase64
    try {
        val encoded = "Hello".toBase64()
        if (encoded == "SGVsbG8=") {
            println("PASSED: Test 19 - Extension function toBase64")
            passed++
        } else {
            println("FAILED: Test 19 - Expected 'SGVsbG8=' but got '$encoded'")
            failed++
        }
    } catch (e: Exception) {
        println("FAILED: Test 19 - ${e.message}")
        failed++
    }

    // Test 20: Extension function - fromBase64
    try {
        val decoded = "SGVsbG8=".fromBase64()
        if (decoded == "Hello") {
            println("PASSED: Test 20 - Extension function fromBase64")
            passed++
        } else {
            println("FAILED: Test 20 - Expected 'Hello' but got '$decoded'")
            failed++
        }
    } catch (e: Exception) {
        println("FAILED: Test 20 - ${e.message}")
        failed++
    }

    // Test 21: Extension function - toBase64UrlSafe
    try {
        val encoded = "user+name/file".toBase64UrlSafe(padding = false)
        if (encoded == "dXNlcituYW1lL2ZpbGU") {
            println("PASSED: Test 21 - Extension function toBase64UrlSafe")
            passed++
        } else {
            println("FAILED: Test 21 - Expected 'dXNlcituYW1lL2ZpbGU' but got '$encoded'")
            failed++
        }
    } catch (e: Exception) {
        println("FAILED: Test 21 - ${e.message}")
        failed++
    }

    // Test 22: ByteArray extension functions
    try {
        val data = byteArrayOf(0x00, 0x01, 0x02, 0x03)
        val encoded = data.toBase64()
        if (encoded == "AAECAw==") {
            println("PASSED: Test 22 - ByteArray toBase64")
            passed++
        } else {
            println("FAILED: Test 22 - Expected 'AAECAw==' but got '$encoded'")
            failed++
        }
    } catch (e: Exception) {
        println("FAILED: Test 22 - ${e.message}")
        failed++
    }

    // Test 23: Long text encoding
    try {
        val original = "Lorem ipsum dolor sit amet, consectetur adipiscing elit."
        val encoded = Base64Utils.encode(original)
        val decoded = Base64Utils.decode(encoded)
        if (decoded == original) {
            println("PASSED: Test 23 - Long text encoding")
            passed++
        } else {
            println("FAILED: Test 23 - Long text round-trip failed")
            failed++
        }
    } catch (e: Exception) {
        println("FAILED: Test 23 - ${e.message}")
        failed++
    }

    // Test 24: Special characters encoding
    try {
        val original = "!@#$%^&*()_+-=[]{}|;':\",./<>?"
        val encoded = Base64Utils.encode(original)
        val decoded = Base64Utils.decode(encoded)
        if (decoded == original) {
            println("PASSED: Test 24 - Special characters encoding")
            passed++
        } else {
            println("FAILED: Test 24 - Special characters round-trip failed")
            failed++
        }
    } catch (e: Exception) {
        println("FAILED: Test 24 - ${e.message}")
        failed++
    }

    // Test 25: Multi-line text encoding
    try {
        val original = "Line 1\nLine 2\r\nLine 3\tTabbed"
        val encoded = Base64Utils.encode(original)
        val decoded = Base64Utils.decode(encoded)
        if (decoded == original) {
            println("PASSED: Test 25 - Multi-line text encoding")
            passed++
        } else {
            println("FAILED: Test 25 - Multi-line round-trip failed")
            failed++
        }
    } catch (e: Exception) {
        println("FAILED: Test 25 - ${e.message}")
        failed++
    }

    println("=".repeat(50))
    println("Tests completed: $passed passed, $failed failed")
    
    if (failed > 0) {
        kotlin.system.exitProcess(1)
    }
}

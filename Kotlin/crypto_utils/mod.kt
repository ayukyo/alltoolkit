/**
 * AllToolkit - Kotlin Crypto Utilities
 * 
 * 零依赖的加密工具模块，仅使用 Kotlin/Java 标准库
 * 支持：哈希计算、HMAC、Base64、UUID、随机字符串生成、XOR加密
 * 
 * @author AllToolkit
 * @version 1.0.0
 */

package crypto_utils

import java.security.MessageDigest
import java.security.SecureRandom
import java.util.*
import javax.crypto.Mac
import javax.crypto.spec.SecretKeySpec

/**
 * 字符集常量
 */
object CharSets {
    const val LOWERCASE = "abcdefghijklmnopqrstuvwxyz"
    const val UPPERCASE = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    const val DIGITS = "0123456789"
    const val SPECIAL = "!@#$%^&*()-_=+[]{}|;:,.<>?"
    const val HEX = "0123456789abcdef"
    const val HEX_UPPER = "0123456789ABCDEF"
    const val ALPHANUMERIC = LOWERCASE + UPPERCASE + DIGITS
    const val ALL = LOWERCASE + UPPERCASE + DIGITS + SPECIAL
}

/**
 * 加密工具类 - 提供完整的哈希、编码、加密功能
 */
object CryptoUtils {
    
    private val secureRandom = SecureRandom()
    
    // ==================== 哈希函数 ====================
    
    fun md5(input: String): String = hash(input, "MD5")
    fun sha1(input: String): String = hash(input, "SHA-1")
    fun sha256(input: String): String = hash(input, "SHA-256")
    fun sha384(input: String): String = hash(input, "SHA-384")
    fun sha512(input: String): String = hash(input, "SHA-512")
    
    fun sha256Bytes(data: ByteArray): String {
        val digest = MessageDigest.getInstance("SHA-256")
        return bytesToHex(digest.digest(data))
    }
    
    fun sha256File(filePath: String): String? {
        return try {
            val file = java.io.File(filePath)
            if (!file.exists()) return null
            val digest = MessageDigest.getInstance("SHA-256")
            file.inputStream().use { stream ->
                val buffer = ByteArray(8192)
                var read: Int
                while (stream.read(buffer).also { read = it } != -1) {
                    digest.update(buffer, 0, read)
                }
            }
            bytesToHex(digest.digest())
        } catch (e: Exception) {
            null
        }
    }
    
    fun hash(input: String, algorithm: String): String {
        val digest = MessageDigest.getInstance(algorithm)
        return bytesToHex(digest.digest(input.toByteArray(Charsets.UTF_8)))
    }
    
    // ==================== HMAC 函数 ====================
    
    fun hmacSha256(message: String, key: String): String = hmac(message, key, "HmacSHA256")
    fun hmacSha512(message: String, key: String): String = hmac(message, key, "HmacSHA512")
    
    fun verifyHmacSha256(message: String, key: String, hmac: String): Boolean {
        return hmacSha256(message, key).equals(hmac, ignoreCase = true)
    }
    
    fun hmac(message: String, key: String, algorithm: String): String {
        val mac = Mac.getInstance(algorithm)
        val secretKey = SecretKeySpec(key.toByteArray(Charsets.UTF_8), algorithm)
        mac.init(secretKey)
        return bytesToHex(mac.doFinal(message.toByteArray(Charsets.UTF_8)))
    }
    
    // ==================== Base64 编码 ====================
    
    fun base64Encode(input: String): String {
        return Base64.getEncoder().encodeToString(input.toByteArray(Charsets.UTF_8))
    }
    
    fun base64Decode(input: String): String? {
        return try {
            String(Base64.getDecoder().decode(input), Charsets.UTF_8)
        } catch (e: IllegalArgumentException) {
            null
        }
    }
    
    fun base64EncodeBytes(data: ByteArray): String = Base64.getEncoder().encodeToString(data)
    
    fun base64DecodeToBytes(input: String): ByteArray? {
        return try {
            Base64.getDecoder().decode(input)
        } catch (e: IllegalArgumentException) {
            null
        }
    }
    
    fun base64UrlEncode(input: String, padding: Boolean = true): String {
        val encoded = Base64.getUrlEncoder().encodeToString(input.toByteArray(Charsets.UTF_8))
        return if (padding) encoded else encoded.trimEnd('=')
    }
    
    fun base64UrlDecode(input: String): String? {
        return try {
            val padded = if (input.length % 4 == 0) input else input + "=".repeat(4 - input.length % 4)
            String(Base64.getUrlDecoder().decode(padded), Charsets.UTF_8)
        } catch (e: IllegalArgumentException) {
            null
        }
    }
    
    // ==================== 十六进制编码 ====================
    
    fun hexEncode(input: String): String = bytesToHex(input.toByteArray(Charsets.UTF_8))
    
    fun hexDecode(input: String): String? {
        return try {
            String(hexToBytes(input), Charsets.UTF_8)
        } catch (e: Exception) {
            null
        }
    }
    
    fun bytesToHex(bytes: ByteArray): String {
        val sb = StringBuilder(bytes.size * 2)
        for (b in bytes) {
            sb.append(String.format("%02x", b))
        }
        return sb.toString()
    }
    
    fun hexToBytes(hex: String): ByteArray {
        val len = hex.length
        require(len % 2 == 0) { "Hex string must have even length" }
        val data = ByteArray(len / 2)
        for (i in 0 until len step 2) {
            data[i / 2] = ((Character.digit(hex[i], 16) shl 4) + Character.digit(hex[i + 1], 16)).toByte()
        }
        return data
    }
    
    // ==================== UUID 生成 ====================
    
    fun uuid(): String = UUID.randomUUID().toString()
    fun uuidSimple(): String = uuid().replace("-", "")
    fun uuidUpper(): String = uuid().uppercase()
    
    fun isValidUuid(input: String): Boolean {
        val uuidRegex = "^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$"
        return input.matches(Regex(uuidRegex))
    }
    
    // ==================== 随机字符串生成 ====================
    
    fun randomString(length: Int, chars: String = CharSets.ALPHANUMERIC): String {
        require(length > 0) { "Length must be positive" }
        require(chars.isNotEmpty()) { "Character set must not be empty" }
        return (1..length).map { chars[secureRandom.nextInt(chars.length)] }.joinToString("")
    }
    
    fun randomAlphanumeric(length: Int): String = randomString(length, CharSets.ALPHANUMERIC)
    fun randomNumeric(length: Int): String = randomString(length, CharSets.DIGITS)
    fun randomHex(length: Int): String = randomString(length, CharSets.HEX)
    fun randomHexUpper(length: Int): String = randomString(length, CharSets.HEX_UPPER)
    
    fun randomPassword(length: Int): String {
        require(length >= 4) { "Password length must be at least 4" }
        val password = StringBuilder(length)
        password.append(CharSets.LOWERCASE[secureRandom.nextInt(CharSets.LOWERCASE.length)])
        password.append(CharSets.UPPERCASE[secureRandom.nextInt(CharSets.UPPERCASE.length)])
        password.append(CharSets.DIGITS[secureRandom.nextInt(CharSets.DIGITS.length)])
        password.append(CharSets.SPECIAL[secureRandom.nextInt(CharSets.SPECIAL.length)])
        val remaining = CharSets.ALL
        for (i in 4 until length) {
            password.append(remaining[secureRandom.nextInt(remaining.length)])
        }
        return password.toString().toList().shuffled(secureRandom).joinToString("")
    }
    
    // ==================== XOR 加密 ====================
    
    fun xorEncrypt(input: String, key: String): String {
        if (key.isEmpty()) return base64Encode(input)
        val encrypted = xorBytes(input.toByteArray(Charsets.UTF_8), key.toByteArray(Charsets.UTF_8))
        return base64EncodeBytes(encrypted)
    }
    
    fun xorDecrypt(input: String, key: String): String? {
        if (key.isEmpty()) return base64Decode(input)
        val decoded = base64DecodeToBytes(input) ?: return null
        return String(xorBytes(decoded, key.toByteArray(Charsets.UTF_8)), Charsets.UTF_8)
    }
    
    private fun xorBytes(data: ByteArray, key: ByteArray): ByteArray {
        return data.mapIndexed { index, byte ->
            (byte.toInt() xor key[index % key.size].toInt()).toByte()
        }.toByteArray()
    }
    
    // ==================== 验证函数 ====================
    
    fun isValidMd5(input: String): Boolean = input.matches(Regex("^[0-9a-fA-F]{32}$"))
    fun isValidSha1(input: String): Boolean = input.matches(Regex("^[0-9a-fA-F]{40}$"))
    fun isValidSha256(input: String): Boolean = input.matches(Regex("^[0-9a-fA-F]{64}$"))
    fun isValidSha384(input: String): Boolean = input.matches(Regex("^[0-9a-fA-F]{96}$"))
    fun isValidSha512(input: String): Boolean = input.matches(Regex("^[0-9a-fA-F]{128}$"))
    
    fun isValidBase64(input: String): Boolean {
        return try {
            Base64.getDecoder().decode(input)
            true
        } catch (e: IllegalArgumentException) {
            false
        }
    }
    
    fun isValidHex(input: String): Boolean {
        return input.length % 2 == 0 && input.all { it.isDigit() || it in 'a'..'f' || it in 'A'..'F' }
    }
    
    // ==================== URL 编码 ====================
    
    fun urlEncode(input: String): String {
        return java.net.URLEncoder.encode(input, Charsets.UTF_8)
    }
    
    fun urlDecode(input: String): String? {
        return try {
            java.net.URLDecoder.decode(input, Charsets.UTF_8)
        } catch (e: IllegalArgumentException) {
            null
        }
    }
}

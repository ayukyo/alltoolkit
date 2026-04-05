package base64_utils

import java.util.Base64

/**
 * Base64 编码解码工具类
 *
 * 提供标准 Base64 和 URL 安全 Base64 (RFC 4648) 的编码解码功能
 * 零依赖，仅使用 Kotlin/Java 标准库
 *
 * @author AllToolkit
 * @since 1.0.0
 */
object Base64Utils {

    /**
     * 将字符串编码为标准 Base64
     *
     * @param input 要编码的字符串
     * @param charset 字符编码，默认为 UTF-8
     * @return Base64 编码后的字符串
     */
    @JvmStatic
    @JvmOverloads
    fun encode(input: String, charset: java.nio.charset.Charset = Charsets.UTF_8): String {
        return Base64.getEncoder().encodeToString(input.toByteArray(charset))
    }

    /**
     * 将字节数组编码为标准 Base64
     *
     * @param data 要编码的字节数组
     * @return Base64 编码后的字符串
     */
    @JvmStatic
    fun encode(data: ByteArray): String {
        return Base64.getEncoder().encodeToString(data)
    }

    /**
     * 将字符串编码为 URL 安全的 Base64 (RFC 4648)
     * 使用 - 和 _ 代替 + 和 /，不包含填充字符 =
     *
     * @param input 要编码的字符串
     * @param charset 字符编码，默认为 UTF-8
     * @param padding 是否包含填充字符，默认为 false
     * @return URL 安全的 Base64 编码后的字符串
     */
    @JvmStatic
    @JvmOverloads
    fun encodeUrlSafe(
        input: String,
        charset: java.nio.charset.Charset = Charsets.UTF_8,
        padding: Boolean = false
    ): String {
        val encoder = if (padding) {
            Base64.getUrlEncoder()
        } else {
            Base64.getUrlEncoder().withoutPadding()
        }
        return encoder.encodeToString(input.toByteArray(charset))
    }

    /**
     * 将字节数组编码为 URL 安全的 Base64
     *
     * @param data 要编码的字节数组
     * @param padding 是否包含填充字符，默认为 false
     * @return URL 安全的 Base64 编码后的字符串
     */
    @JvmStatic
    @JvmOverloads
    fun encodeUrlSafe(data: ByteArray, padding: Boolean = false): String {
        val encoder = if (padding) {
            Base64.getUrlEncoder()
        } else {
            Base64.getUrlEncoder().withoutPadding()
        }
        return encoder.encodeToString(data)
    }

    /**
     * 解码标准 Base64 字符串为普通字符串
     *
     * @param base64 Base64 编码的字符串
     * @param charset 字符编码，默认为 UTF-8
     * @return 解码后的字符串
     * @throws IllegalArgumentException 如果输入不是有效的 Base64
     */
    @JvmStatic
    @JvmOverloads
    fun decode(base64: String, charset: java.nio.charset.Charset = Charsets.UTF_8): String {
        val bytes = Base64.getDecoder().decode(base64)
        return String(bytes, charset)
    }

    /**
     * 解码标准 Base64 字符串为字节数组
     *
     * @param base64 Base64 编码的字符串
     * @return 解码后的字节数组
     * @throws IllegalArgumentException 如果输入不是有效的 Base64
     */
    @JvmStatic
    fun decodeToBytes(base64: String): ByteArray {
        return Base64.getDecoder().decode(base64)
    }

    /**
     * 安全解码标准 Base64，失败时返回 null
     *
     * @param base64 Base64 编码的字符串
     * @param charset 字符编码，默认为 UTF-8
     * @return 解码后的字符串，如果失败则返回 null
     */
    @JvmStatic
    @JvmOverloads
    fun decodeOrNull(base64: String, charset: java.nio.charset.Charset = Charsets.UTF_8): String? {
        return try {
            decode(base64, charset)
        } catch (e: IllegalArgumentException) {
            null
        }
    }

    /**
     * 解码 URL 安全的 Base64 字符串为普通字符串
     *
     * @param base64Url URL 安全的 Base64 编码的字符串
     * @param charset 字符编码，默认为 UTF-8
     * @return 解码后的字符串
     * @throws IllegalArgumentException 如果输入不是有效的 Base64
     */
    @JvmStatic
    @JvmOverloads
    fun decodeUrlSafe(base64Url: String, charset: java.nio.charset.Charset = Charsets.UTF_8): String {
        val bytes = Base64.getUrlDecoder().decode(base64Url)
        return String(bytes, charset)
    }

    /**
     * 解码 URL 安全的 Base64 字符串为字节数组
     *
     * @param base64Url URL 安全的 Base64 编码的字符串
     * @return 解码后的字节数组
     * @throws IllegalArgumentException 如果输入不是有效的 Base64
     */
    @JvmStatic
    fun decodeUrlSafeToBytes(base64Url: String): ByteArray {
        return Base64.getUrlDecoder().decode(base64Url)
    }

    /**
     * 安全解码 URL 安全的 Base64，失败时返回 null
     *
     * @param base64Url URL 安全的 Base64 编码的字符串
     * @param charset 字符编码，默认为 UTF-8
     * @return 解码后的字符串，如果失败则返回 null
     */
    @JvmStatic
    @JvmOverloads
    fun decodeUrlSafeOrNull(base64Url: String, charset: java.nio.charset.Charset = Charsets.UTF_8): String? {
        return try {
            decodeUrlSafe(base64Url, charset)
        } catch (e: IllegalArgumentException) {
            null
        }
    }

    /**
     * 将标准 Base64 转换为 URL 安全的 Base64
     *
     * @param base64 标准 Base64 字符串
     * @param padding 是否包含填充字符，默认为 false
     * @return URL 安全的 Base64 字符串
     */
    @JvmStatic
    @JvmOverloads
    fun toUrlSafe(base64: String, padding: Boolean = false): String {
        // 先解码再编码为 URL 安全格式
        val bytes = Base64.getDecoder().decode(base64)
        val encoder = if (padding) {
            Base64.getUrlEncoder()
        } else {
            Base64.getUrlEncoder().withoutPadding()
        }
        return encoder.encodeToString(bytes)
    }

    /**
     * 将 URL 安全的 Base64 转换为标准 Base64
     *
     * @param base64Url URL 安全的 Base64 字符串
     * @return 标准 Base64 字符串
     */
    @JvmStatic
    fun fromUrlSafe(base64Url: String): String {
        // 先解码再编码为标准格式
        val bytes = Base64.getUrlDecoder().decode(base64Url)
        return Base64.getEncoder().encodeToString(bytes)
    }

    /**
     * 验证字符串是否为有效的标准 Base64
     *
     * @param str 要验证的字符串
     * @return 如果是有效的 Base64 则返回 true
     */
    @JvmStatic
    fun isValid(str: String): Boolean {
        return try {
            Base64.getDecoder().decode(str)
            true
        } catch (e: IllegalArgumentException) {
            false
        }
    }

    /**
     * 验证字符串是否为有效的 URL 安全 Base64
     *
     * @param str 要验证的字符串
     * @return 如果是有效的 URL 安全 Base64 则返回 true
     */
    @JvmStatic
    fun isValidUrlSafe(str: String): Boolean {
        return try {
            Base64.getUrlDecoder().decode(str)
            true
        } catch (e: IllegalArgumentException) {
            false
        }
    }

    /**
     * 计算编码后的字符串长度
     *
     * @param inputLength 输入字节长度
     * @param padding 是否包含填充字符
     * @return 编码后的字符串长度
     */
    @JvmStatic
    @JvmOverloads
    fun encodedLength(inputLength: Int, padding: Boolean = true): Int {
        val baseLength = (inputLength + 2) / 3 * 4
        return if (padding) {
            baseLength
        } else {
            baseLength - when (inputLength % 3) {
                1 -> 2
                2 -> 1
                else -> 0
            }
        }
    }

    /**
     * 计算解码后的最大字节长度
     *
     * @param base64Length Base64 字符串长度
     * @return 解码后的最大字节长度
     */
    @JvmStatic
    fun decodedMaxLength(base64Length: Int): Int {
        return base64Length / 4 * 3
    }
}

/**
 * 字符串扩展函数，提供便捷的 Base64 编码解码
 */
fun String.toBase64(): String = Base64Utils.encode(this)

fun String.toBase64UrlSafe(padding: Boolean = false): String = Base64Utils.encodeUrlSafe(this, padding = padding)

fun String.fromBase64(): String = Base64Utils.decode(this)

fun String.fromBase64OrNull(): String? = Base64Utils.decodeOrNull(this)

fun String.fromBase64UrlSafe(): String = Base64Utils.decodeUrlSafe(this)

fun String.fromBase64UrlSafeOrNull(): String? = Base64Utils.decodeUrlSafeOrNull(this)

fun ByteArray.toBase64(): String = Base64Utils.encode(this)

fun ByteArray.toBase64UrlSafe(padding: Boolean = false): String = Base64Utils.encodeUrlSafe(this, padding = padding)

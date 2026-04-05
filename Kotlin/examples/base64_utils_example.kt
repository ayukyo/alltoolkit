package examples

import base64_utils.Base64Utils
import base64_utils.toBase64
import base64_utils.fromBase64
import base64_utils.toBase64UrlSafe
import base64_utils.fromBase64UrlSafe

/**
 * Base64Utils 使用示例
 * 
 * 展示 Kotlin Base64 编码解码工具的各种用法
 */
fun main() {
    println("=".repeat(60))
    println("Kotlin Base64Utils 使用示例")
    println("=".repeat(60))
    
    // 示例 1: 基本编码解码
    println("\n【示例 1】基本编码解码")
    val text1 = "Hello, World!"
    val encoded1 = Base64Utils.encode(text1)
    val decoded1 = Base64Utils.decode(encoded1)
    println("原文: $text1")
    println("编码: $encoded1")
    println("解码: $decoded1")
    
    // 示例 2: URL 安全 Base64（用于 URL 和文件名）
    println("\n【示例 2】URL 安全 Base64")
    val text2 = "user+name/file/path"
    val urlSafe = Base64Utils.encodeUrlSafe(text2, padding = false)
    val decoded2 = Base64Utils.decodeUrlSafe(urlSafe)
    println("原文: $text2")
    println("URL安全编码: $urlSafe")
    println("解码: $decoded2")
    
    // 示例 3: 中文字符编码
    println("\n【示例 3】中文字符编码")
    val chinese = "你好，世界！"
    val encodedChinese = Base64Utils.encode(chinese)
    val decodedChinese = Base64Utils.decode(encodedChinese)
    println("原文: $chinese")
    println("编码: $encodedChinese")
    println("解码: $decodedChinese")
    
    // 示例 4: Emoji 编码
    println("\n【示例 4】Emoji 编码")
    val emoji = "Kotlin 很棒! 👍🚀✨"
    val encodedEmoji = Base64Utils.encode(emoji)
    val decodedEmoji = Base64Utils.decode(encodedEmoji)
    println("原文: $emoji")
    println("编码: $encodedEmoji")
    println("解码: $decodedEmoji")
    
    // 示例 5: 二进制数据编码
    println("\n【示例 5】二进制数据编码")
    val binaryData = byteArrayOf(0x00, 0x01, 0x02, 0x03, 0xFF.toByte())
    val encodedBinary = Base64Utils.encode(binaryData)
    val decodedBinary = Base64Utils.decodeToBytes(encodedBinary)
    println("二进制数据: ${binaryData.joinToString(", ") { "0x%02X".format(it) }}")
    println("编码: $encodedBinary")
    println("解码: ${decodedBinary.joinToString(", ") { "0x%02X".format(it) }}")
    
    // 示例 6: 使用扩展函数
    println("\n【示例 6】使用扩展函数")
    val text6 = "Extension functions are cool!"
    val encoded6 = text6.toBase64()
    val decoded6 = encoded6.fromBase64()
    println("原文: $text6")
    println("编码 (扩展函数): $encoded6")
    println("解码 (扩展函数): $decoded6")
    
    // 示例 7: 安全的解码（避免异常）
    println("\n【示例 7】安全的解码")
    val validBase64 = "SGVsbG8="
    val invalidBase64 = "NotValid!@#"
    val result1 = Base64Utils.decodeOrNull(validBase64)
    val result2 = Base64Utils.decodeOrNull(invalidBase64)
    println("有效 Base64 '$validBase64' 解码结果: $result1")
    println("无效 Base64 '$invalidBase64' 解码结果: $result2")
    
    // 示例 8: 验证 Base64 格式
    println("\n【示例 8】验证 Base64 格式")
    val testStrings = listOf("SGVsbG8=", "Invalid!", "dXNlcg==", "Not@Base64")
    testStrings.forEach { str ->
        val isValid = Base64Utils.isValid(str)
        println("'$str' 是有效的 Base64: $isValid")
    }
    
    // 示例 9: 标准 Base64 与 URL 安全 Base64 转换
    println("\n【示例 9】标准 Base64 与 URL 安全 Base64 转换")
    val standard = Base64Utils.encode("Hello+World/Test")
    val toUrlSafe = Base64Utils.toUrlSafe(standard, padding = false)
    val backToStandard = Base64Utils.fromUrlSafe(toUrlSafe)
    println("标准 Base64: $standard")
    println("转 URL 安全: $toUrlSafe")
    println("转回标准: $backToStandard")
    
    // 示例 10: 计算编码长度
    println("\n【示例 10】计算编码长度")
    val inputLengths = listOf(1, 10, 100, 1000)
    inputLengths.forEach { len ->
        val encodedLen = Base64Utils.encodedLength(len, padding = true)
        println("输入 $len 字节 -> 编码后约 $encodedLen 字符")
    }
    
    // 示例 11: 实际应用场景 - 简单的数据混淆
    println("\n【示例 11】数据混淆示例")
    val sensitiveData = "password123"
    val obfuscated = sensitiveData.toBase64()
    println("敏感数据: $sensitiveData")
    println("混淆后: $obfuscated")
    println("恢复: ${obfuscated.fromBase64()}")
    
    // 示例 12: 在 URL 参数中使用 URL 安全 Base64
    println("\n【示例 12】URL 参数中的 Base64")
    val dataForUrl = "user@example.com"
    val urlParam = dataForUrl.toBase64UrlSafe(padding = false)
    val fullUrl = "https://example.com/api?data=$urlParam"
    println("原始数据: $dataForUrl")
    println("URL 参数值: $urlParam")
    println("完整 URL: $fullUrl")
    println("从 URL 参数解码: ${urlParam.fromBase64UrlSafe()}")
    
    println("\n" + "=".repeat(60))
    println("示例运行完成!")
    println("=".repeat(60))
}

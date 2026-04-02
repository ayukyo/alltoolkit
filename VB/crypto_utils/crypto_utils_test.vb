' =============================================================================
' AllToolkit - Crypto Utilities Tests for VB.NET
' =============================================================================
' CryptoUtils 模块的单元测试
'
' 运行方式:
'   1. 使用 Visual Studio: 打开测试资源管理器并运行
'   2. 使用命令行: dotnet test (如果配置了 .NET SDK)
'   3. 使用 VSTest: vstest.console.exe crypto_utils_test.dll
'
' 作者: AllToolkit Contributors
' 许可证: MIT
' =============================================================================

Imports System
Imports System.IO
Imports System.Text
Imports Microsoft.VisualStudio.TestTools.UnitTesting
Imports AllToolkit

Namespace AllToolkit.Tests

    ''' <summary>
    ''' CryptoUtils 模块的单元测试类。
    ''' </summary>
    <TestClass>
    Public Class CryptoUtilsTest

        ' =====================================================================
        ' MD5 哈希测试
        ' =====================================================================

        <TestMethod>
        Public Sub TestMd5Hash()
            ' 已知 MD5 值测试
            Assert.AreEqual("5d41402abc4b2a76b9719d911017c592", CryptoUtils.Md5Hash("hello"))
            Assert.AreEqual("d41d8cd98f00b204e9800998ecf8427e", CryptoUtils.Md5Hash(""))
            
            ' 空值测试
            Assert.AreEqual("", CryptoUtils.Md5Hash(Nothing))
            
            ' 中文测试
            Assert.AreEqual(32, CryptoUtils.Md5Hash("你好世界").Length)
        End Sub

        <TestMethod>
        Public Sub TestMd5HashConsistency()
            ' 一致性测试
            Dim hash1 As String = CryptoUtils.Md5Hash("test123")
            Dim hash2 As String = CryptoUtils.Md5Hash("test123")
            Assert.AreEqual(hash1, hash2)
        End Sub

        ' =====================================================================
        ' SHA 哈希测试
        ' =====================================================================

        <TestMethod>
        Public Sub TestSha1Hash()
            Assert.AreEqual(40, CryptoUtils.Sha1Hash("hello").Length)
            Assert.AreEqual("", CryptoUtils.Sha1Hash(Nothing))
            Assert.AreEqual("", CryptoUtils.Sha1Hash(""))
        End Sub

        <TestMethod>
        Public Sub TestSha256Hash()
            Assert.AreEqual(64, CryptoUtils.Sha256Hash("hello").Length)
            Assert.AreEqual("", CryptoUtils.Sha256Hash(Nothing))
            Assert.AreEqual("", CryptoUtils.Sha256Hash(""))
            
            ' 已知 SHA256 值测试
            Dim expected As String = "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"
            Assert.AreEqual(expected, CryptoUtils.Sha256Hash("hello"))
        End Sub

        <TestMethod>
        Public Sub TestSha512Hash()
            Assert.AreEqual(128, CryptoUtils.Sha512Hash("hello").Length)
            Assert.AreEqual("", CryptoUtils.Sha512Hash(Nothing))
        End Sub

        ' =====================================================================
        ' 文件哈希测试
        ' =====================================================================

        <TestMethod>
        Public Sub TestSha256File()
            ' 创建临时文件
            Dim tempFile As String = Path.GetTempFileName()
            File.WriteAllText(tempFile, "test content", Encoding.UTF8)
            
            Try
                Dim hash As String = CryptoUtils.Sha256File(tempFile)
                Assert.AreEqual(64, hash.Length)
                Assert.IsTrue(CryptoUtils.IsValidSha256(hash))
                
                ' 相同内容应产生相同哈希
                Dim hash2 As String = CryptoUtils.Sha256File(tempFile)
                Assert.AreEqual(hash, hash2)
            Finally
                File.Delete(tempFile)
            End Try
        End Sub

        <TestMethod>
        Public Sub TestSha256FileNotExists()
            Assert.AreEqual("", CryptoUtils.Sha256File("/nonexistent/file.txt"))
        End Sub

        ' =====================================================================
        ' HMAC 测试
        ' =====================================================================

        <TestMethod>
        Public Sub TestHmacSha256()
            Dim message As String = "hello"
            Dim secret As String = "secret_key"
            Dim hmac As String = CryptoUtils.HmacSha256(message, secret)
            
            Assert.AreEqual(64, hmac.Length)
            Assert.IsTrue(CryptoUtils.IsValidSha256(hmac))
            
            ' 相同输入应产生相同输出
            Dim hmac2 As String = CryptoUtils.HmacSha256(message, secret)
            Assert.AreEqual(hmac, hmac2)
            
            ' 不同密钥应产生不同输出
            Dim hmac3 As String = CryptoUtils.HmacSha256(message, "different_key")
            Assert.AreNotEqual(hmac, hmac3)
        End Sub

        <TestMethod>
        Public Sub TestHmacSha256Empty()
            Assert.AreEqual("", CryptoUtils.HmacSha256(Nothing, "key"))
            Assert.AreEqual("", CryptoUtils.HmacSha256("message", Nothing))
            Assert.AreEqual("", CryptoUtils.HmacSha256("", ""))
        End Sub

        ' =====================================================================
        ' Base64 编码/解码测试
        ' =====================================================================

        <TestMethod>
        Public Sub TestBase64Encode()
            Assert.AreEqual("aGVsbG8=", CryptoUtils.Base64Encode("hello"))
            Assert.AreEqual("", CryptoUtils.Base64Encode(Nothing))
            Assert.AreEqual("", CryptoUtils.Base64Encode(""))
            
            ' 中文编码
            Dim encoded As String = CryptoUtils.Base64Encode("你好")
            Assert.IsTrue(encoded.Length > 0)
        End Sub

        <TestMethod>
        Public Sub TestBase64Decode()
            Assert.AreEqual("hello", CryptoUtils.Base64Decode("aGVsbG8="))
            Assert.AreEqual("", CryptoUtils.Base64Decode(Nothing))
            Assert.AreEqual("", CryptoUtils.Base64Decode(""))
            
            ' 无效输入
            Assert.AreEqual("", CryptoUtils.Base64Decode("invalid!!!"))
        End Sub

        <TestMethod>
        Public Sub TestBase64RoundTrip()
            Dim original As String = "Hello, 世界! 123 @#$"
            Dim encoded As String = CryptoUtils.Base64Encode(original)
            Dim decoded As String = CryptoUtils.Base64Decode(encoded)
            Assert.AreEqual(original, decoded)
        End Sub

        ' =====================================================================
        ' URL 安全 Base64 测试
        ' =====================================================================

        <TestMethod>
        Public Sub TestBase64UrlEncode()
            ' 包含 + 和 / 的字符串
            Dim input As String = ">>>???"
            Dim encoded As String = CryptoUtils.Base64UrlEncode(input)
            
            ' URL 安全编码不应包含 + / =
            Assert.IsFalse(encoded.Contains("+"))
            Assert.IsFalse(encoded.Contains("/"))
            Assert.IsFalse(encoded.Contains("="))
        End Sub

        <TestMethod>
        Public Sub TestBase64UrlRoundTrip()
            Dim original As String = "Hello+World/Test=Value"
            Dim encoded As String = CryptoUtils.Base64UrlEncode(original)
            Dim decoded As String = CryptoUtils.Base64UrlDecode(encoded)
            Assert.AreEqual(original, decoded)
        End Sub

        <TestMethod>
        Public Sub TestBase64UrlDecodeInvalid()
            Assert.AreEqual("", CryptoUtils.Base64UrlDecode("invalid"))
            Assert.AreEqual("", CryptoUtils.Base64UrlDecode(Nothing))
        End Sub

        ' =====================================================================
        ' 随机字符串测试
        ' =====================================================================

        <TestMethod>
        Public Sub TestRandomString()
            Dim s1 As String = CryptoUtils.RandomString(10)
            Assert.AreEqual(10, s1.Length)
            
            ' 两次生成的字符串应不同（概率极低相同）
            Dim s2 As String = CryptoUtils.RandomString(10)
            Assert.AreEqual(10, s2.Length)
            ' 注意：理论上可能相同，但概率极低
            
            ' 边界值
            Assert.AreEqual("", CryptoUtils.RandomString(0))
            Assert.AreEqual("", CryptoUtils.RandomString(-1))
        End Sub

        <TestMethod>
        Public Sub TestRandomStringCustomChars()
            Dim s As String = CryptoUtils.RandomString(20, "ABC")
            Assert.AreEqual(20, s.Length)
            ' 应只包含指定字符
            For Each c As Char In s
                Assert.IsTrue("ABC".Contains(c))
            Next
        End Sub

        <TestMethod>
        Public Sub TestRandomPassword()
            Dim password As String = CryptoUtils.RandomPassword(12)
            Assert.AreEqual(12, password.Length)
            
            ' 应包含至少一个大写字母
            Assert.IsTrue(password.Any(Function(c) Char.IsUpper(c)))
            ' 应包含至少一个小写字母
            Assert.IsTrue(password.Any(Function(c) Char.IsLower(c)))
            ' 应包含至少一个数字
            Assert.IsTrue(password.Any(Function(c) Char.IsDigit(c)))
            ' 应包含至少一个特殊字符
            Assert.IsTrue(password.Any(Function(c) "!@#$%^&*()_+-=[]{}|;:,.<>?".Contains(c)))
        End Sub

        <TestMethod>
        Public Sub TestRandomPasswordMinLength()
            ' 小于4应调整为8
            Dim p As String = CryptoUtils.RandomPassword(2)
            Assert.AreEqual(8, p.Length)
        End Sub

        ' =====================================================================
        ' UUID 生成测试
        ' =====================================================================

        <TestMethod>
        Public Sub TestGenerateUuid()
            Dim uuid1 As String = CryptoUtils.GenerateUuid()
            Dim uuid2 As String = CryptoUtils.GenerateUuid()
            
            ' 标准 UUID 格式: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
            Assert.AreEqual(36, uuid1.Length)
            Assert.AreEqual(4, uuid1.Split("-"c).Length - 1)
            
            ' 两次生成的 UUID 应不同
            Assert.AreNotEqual(uuid1, uuid2)
        End Sub

        <TestMethod>
        Public Sub TestGenerateUuidSimple()
            Dim uuid As String = CryptoUtils.GenerateUuidSimple()
            Assert.AreEqual(32, uuid.Length)
            Assert.IsFalse(uuid.Contains("-"))
        End Sub

        ' =====================================================================
        ' XOR 加密测试
        ' =====================================================================

        <TestMethod>
        Public Sub TestXorEncryptDecrypt()
            Dim original As String = "Hello, World!"
            Dim key As String = "my_secret_key"
            
            Dim encrypted As String = CryptoUtils.XorEncrypt(original, key)
            Assert.AreNotEqual(original, encrypted)
            
            Dim decrypted As String = CryptoUtils.XorDecrypt(encrypted, key)
            Assert.AreEqual(original, decrypted)
        End Sub

        <TestMethod>
        Public Sub TestXorEncryptEmpty()
            Assert.AreEqual("", CryptoUtils.XorEncrypt(Nothing, "key"))
            Assert.AreEqual("", CryptoUtils.XorEncrypt("text", Nothing))
            Assert.AreEqual("", CryptoUtils.XorDecrypt(Nothing, "key"))
            Assert.AreEqual("", CryptoUtils.XorDecrypt("text", Nothing))
        End Sub

        <TestMethod>
        Public Sub TestXorEncryptDifferentKeys()
            Dim original As String = "test message"
            Dim encrypted1 As String = CryptoUtils.XorEncrypt(original, "key1")
            Dim encrypted2 As String = CryptoUtils.XorEncrypt(original, "key2")
            
            ' 不同密钥应产生不同密文
            Assert.AreNotEqual(encrypted1, encrypted2)
            
            ' 用错误密钥解密应产生乱码（非原始值）
            Dim wrongDecrypt As String = CryptoUtils.XorDecrypt(encrypted1, "key2")
            Assert.AreNotEqual(original, wrongDecrypt)
        End Sub

        ' =====================================================================
        ' 混淆测试
        ' =====================================================================

        <TestMethod>
        Public Sub TestObfuscateDeobfuscate()
            Dim original As String = "Secret Message 123!"
            Dim obfuscated As String = CryptoUtils.Obfuscate(original)
            
            Assert.AreNotEqual(original, obfuscated)
            
            Dim deobfuscated As String = CryptoUtils.Deobfuscate(obfuscated)
            Assert.AreEqual(original, deobfuscated)
        End Sub

        <TestMethod>
        Public Sub TestObfuscateEmpty()
            Assert.AreEqual("", CryptoUtils.Obfuscate(Nothing))
            Assert.AreEqual("", CryptoUtils.Obfuscate(""))
            Assert.AreEqual("", CryptoUtils.Deobfuscate(Nothing))
            Assert.AreEqual("", CryptoUtils.Deobfuscate(""))
        End Sub

        <TestMethod>
        Public Sub TestObfuscateInvalid()
            ' 无效输入应返回空字符串
            Assert.AreEqual("", CryptoUtils.Deobfuscate("not_valid_base64!!!"))
        End Sub

        ' =====================================================================
        ' 验证函数测试
        ' =====================================================================

        <TestMethod>
        Public Sub TestIsValidMd5()
            Assert.IsTrue(CryptoUtils.IsValidMd5("5d41402abc4b2a76b9719d911017c592"))
            Assert.IsTrue(CryptoUtils.IsValidMd5("D41D8CD98F00B204E9800998ECF8427E")) ' 大写
            Assert.IsFalse(CryptoUtils.IsValidMd5("invalid"))
            Assert.IsFalse(CryptoUtils.IsValidMd5(""))
            Assert.IsFalse(CryptoUtils.IsValidMd5(Nothing))
            Assert.IsFalse(CryptoUtils.IsValidMd5("5d41402abc4b2a76b9719d911017c59")) ' 31位
            Assert.IsFalse(CryptoUtils.IsValidMd5("5d41402abc4b2a76b9719d911017c5923")) ' 33位
        End Sub

        <TestMethod>
        Public Sub TestIsValidSha256()
            Assert.IsTrue(CryptoUtils.IsValidSha256("2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"))
            Assert.IsFalse(CryptoUtils.IsValidSha256("invalid"))
            Assert.IsFalse(CryptoUtils.IsValidSha256(""))
            Assert.IsFalse(CryptoUtils.IsValidSha256(Nothing))
            Assert.IsFalse(CryptoUtils.IsValidSha256("abc123")) ' 太短
        End Sub

        <TestMethod>
        Public Sub TestIsValidBase64()
            Assert.IsTrue(CryptoUtils.IsValidBase64("aGVsbG8="))
            Assert.IsTrue(CryptoUtils.IsValidBase64("dGVzdA=="))
            Assert.IsTrue(CryptoUtils.IsValidBase64(""))
            Assert.IsFalse(CryptoUtils.IsValidBase64(Nothing))
            Assert.IsFalse(CryptoUtils.IsValidBase64("invalid!!!"))
            Assert.IsFalse(CryptoUtils.IsValidBase64("aGVsbG8")) ' 缺少填充但可能有效
        End Sub

        ' =====================================================================
        ' 性能/大数据测试
        ' =====================================================================

        <TestMethod>
        Public Sub TestLargeDataHashing()
            Dim largeString As String = New String("a"c, 1000000) ' 1MB 数据
            Dim hash As String = CryptoUtils.Sha256Hash(largeString)
            Assert.AreEqual(64, hash.Length)
            Assert.IsTrue(CryptoUtils.IsValidSha256(hash))
        End Sub

        <TestMethod>
        Public Sub TestUnicodeSupport()
            Dim unicodeStrings As String() = New String() {
                "Hello 世界",
                "🎉 Emoji test 🚀",
                "العربية",
                "עברית",
                "日本語テキスト"
            }
            
            For Each s As String In unicodeStrings
                Dim hash As String = CryptoUtils.Md5Hash(s)
                Assert.AreEqual(32, hash.Length, "Failed for: " & s)
                
                Dim encoded As String = CryptoUtils.Base64Encode(s)
                Dim decoded As String = CryptoUtils.Base64Decode(encoded)
                Assert.AreEqual(s, decoded, "Base64 round-trip failed for: " & s)
            Next
        End Sub

    End Class

End Namespace

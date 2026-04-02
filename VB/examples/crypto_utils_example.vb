' =============================================================================
' AllToolkit - Crypto Utilities Example for VB.NET
' =============================================================================
' 演示 CryptoUtils 模块的各种功能用法
'
' 运行方式:
'   1. 创建新的 VB.NET 控制台应用程序
'   2. 将 mod.vb 添加到项目
'   3. 将此文件内容复制到 Program.vb 或 Main 方法中
'   4. 运行程序
'
' 作者: AllToolkit Contributors
' 许可证: MIT
' =============================================================================

Imports System
Imports System.IO
Imports AllToolkit

Module CryptoUtilsExample

    Sub Main()
        Console.WriteLine("============================================")
        Console.WriteLine("AllToolkit - Crypto Utilities Examples")
        Console.WriteLine("============================================")
        Console.WriteLine()

        ' =================================================================
        ' 1. 哈希计算示例
        ' =================================================================
        Console.WriteLine("1. 哈希计算 (MD5, SHA1, SHA256, SHA512)")
        Console.WriteLine("-----------------------------------------")
        
        Dim message As String = "Hello, World!"
        Console.WriteLine($"原始消息: {message}")
        Console.WriteLine()
        
        ' MD5 哈希
        Dim md5Hash As String = CryptoUtils.Md5Hash(message)
        Console.WriteLine($"MD5:    {md5Hash} (长度: {md5Hash.Length})")
        
        ' SHA1 哈希
        Dim sha1Hash As String = CryptoUtils.Sha1Hash(message)
        Console.WriteLine($"SHA1:   {sha1Hash} (长度: {sha1Hash.Length})")
        
        ' SHA256 哈希
        Dim sha256Hash As String = CryptoUtils.Sha256Hash(message)
        Console.WriteLine($"SHA256: {sha256Hash} (长度: {sha256Hash.Length})")
        
        ' SHA512 哈希
        Dim sha512Hash As String = CryptoUtils.Sha512Hash(message)
        Console.WriteLine($"SHA512: {sha512Hash} (长度: {sha512Hash.Length})")
        Console.WriteLine()

        ' =================================================================
        ' 2. 文件哈希示例
        ' =================================================================
        Console.WriteLine("2. 文件哈希计算")
        Console.WriteLine("----------------")
        
        ' 创建临时文件
        Dim tempFile As String = Path.GetTempFileName()
        File.WriteAllText(tempFile, "This is a test file content.")
        
        Dim fileHash As String = CryptoUtils.Sha256File(tempFile)
        Console.WriteLine($"临时文件: {tempFile}")
        Console.WriteLine($"文件 SHA256: {fileHash}")
        
        ' 清理
        File.Delete(tempFile)
        Console.WriteLine()

        ' =================================================================
        ' 3. HMAC-SHA256 示例
        ' =================================================================
        Console.WriteLine("3. HMAC-SHA256 消息认证")
        Console.WriteLine("------------------------")
        
        Dim apiMessage As String = "user_id=123&action=login"
        Dim apiSecret As String = "my_api_secret_key_12345"
        
        Dim hmac As String = CryptoUtils.HmacSha256(apiMessage, apiSecret)
        Console.WriteLine($"消息: {apiMessage}")
        Console.WriteLine($"密钥: {apiSecret}")
        Console.WriteLine($"HMAC: {hmac}")
        Console.WriteLine()

        ' =================================================================
        ' 4. Base64 编码/解码示例
        ' =================================================================
        Console.WriteLine("4. Base64 编码和解码")
        Console.WriteLine("---------------------")
        
        Dim originalText As String = "Hello, 世界! 🌍"
        Console.WriteLine($"原始文本: {originalText}")
        
        ' 标准 Base64
        Dim base64Encoded As String = CryptoUtils.Base64Encode(originalText)
        Console.WriteLine($"Base64 编码: {base64Encoded}")
        
        Dim base64Decoded As String = CryptoUtils.Base64Decode(base64Encoded)
        Console.WriteLine($"Base64 解码: {base64Decoded}")
        Console.WriteLine()

        ' =================================================================
        ' 5. URL 安全 Base64 示例
        ' =================================================================
        Console.WriteLine("5. URL 安全 Base64")
        Console.WriteLine("-------------------")
        
        Dim urlData As String = "user+test@example.com"
        Console.WriteLine($"原始数据: {urlData}")
        
        Dim urlSafeEncoded As String = CryptoUtils.Base64UrlEncode(urlData)
        Console.WriteLine($"URL 安全编码: {urlSafeEncoded}")
        Console.WriteLine($"  (不含 + / = 字符，适合 URL 传输)")
        
        Dim urlSafeDecoded As String = CryptoUtils.Base64UrlDecode(urlSafeEncoded)
        Console.WriteLine($"URL 安全解码: {urlSafeDecoded}")
        Console.WriteLine()

        ' =================================================================
        ' 6. 随机字符串生成示例
        ' =================================================================
        Console.WriteLine("6. 随机字符串和密码生成")
        Console.WriteLine("------------------------")
        
        ' 随机字符串
        Dim randomStr As String = CryptoUtils.RandomString(16)
        Console.WriteLine($"随机字符串 (16位): {randomStr}")
        
        ' 仅数字
        Dim randomDigits As String = CryptoUtils.RandomString(6, "0123456789")
        Console.WriteLine($"随机数字 (6位): {randomDigits}")
        
        ' 随机密码
        Dim password As String = CryptoUtils.RandomPassword(16)
        Console.WriteLine($"随机密码 (16位): {password}")
        Console.WriteLine()

        ' =================================================================
        ' 7. UUID 生成示例
        ' =================================================================
        Console.WriteLine("7. UUID 生成")
        Console.WriteLine("-------------")
        
        Dim uuid As String = CryptoUtils.GenerateUuid()
        Console.WriteLine($"标准 UUID: {uuid}")
        
        Dim simpleUuid As String = CryptoUtils.GenerateUuidSimple()
        Console.WriteLine($"简化 UUID: {simpleUuid}")
        Console.WriteLine()

        ' =================================================================
        ' 8. XOR 加密/解密示例
        ' =================================================================
        Console.WriteLine("8. XOR 对称加密")
        Console.WriteLine("----------------")
        
        Dim secretMessage As String = "This is a secret message!"
        Dim xorKey As String = "my_xor_key_2024"
        
        Console.WriteLine($"原始消息: {secretMessage}")
        Console.WriteLine($"加密密钥: {xorKey}")
        
        Dim xorEncrypted As String = CryptoUtils.XorEncrypt(secretMessage, xorKey)
        Console.WriteLine($"加密结果: {xorEncrypted}")
        
        Dim xorDecrypted As String = CryptoUtils.XorDecrypt(xorEncrypted, xorKey)
        Console.WriteLine($"解密结果: {xorDecrypted}")
        Console.WriteLine()

        ' =================================================================
        ' 9. 字符串混淆示例
        ' =================================================================
        Console.WriteLine("9. 简单字符串混淆")
        Console.WriteLine("------------------")
        
        Dim sensitiveData As String = "API_KEY_12345_SECRET"
        Console.WriteLine($"敏感数据: {sensitiveData}")
        
        Dim obfuscated As String = CryptoUtils.Obfuscate(sensitiveData)
        Console.WriteLine($"混淆结果: {obfuscated}")
        
        Dim deobfuscated As String = CryptoUtils.Deobfuscate(obfuscated)
        Console.WriteLine($"反混淆:   {deobfuscated}")
        Console.WriteLine()

        ' =================================================================
        ' 10. 哈希格式验证示例
        ' =================================================================
        Console.WriteLine("10. 哈希格式验证")
        Console.WriteLine("-----------------")
        
        Dim validMd5 As String = "5d41402abc4b2a76b9719d911017c592"
        Dim invalidMd5 As String = "not_a_valid_md5_hash"
        
        Console.WriteLine($"验证 MD5 '{validMd5}': {CryptoUtils.IsValidMd5(validMd5)}")
        Console.WriteLine($"验证 MD5 '{invalidMd5}': {CryptoUtils.IsValidMd5(invalidMd5)}")
        
        Dim validBase64 As String = "SGVsbG8gV29ybGQ="
        Dim invalidBase64 As String = "Not@Valid#Base64"
        
        Console.WriteLine($"验证 Base64 '{validBase64}': {CryptoUtils.IsValidBase64(validBase64)}")
        Console.WriteLine($"验证 Base64 '{invalidBase64}': {CryptoUtils.IsValidBase64(invalidBase64)}")
        Console.WriteLine()

        ' =================================================================
        ' 11. 实用场景：密码验证
        ' =================================================================
        Console.WriteLine("11. 实用场景：密码哈希存储与验证")
        Console.WriteLine("----------------------------------")
        
        ' 模拟用户注册
        Dim userPassword As String = "MySecurePassword123!"
        Dim storedHash As String = CryptoUtils.Sha256Hash(userPassword)
        
        Console.WriteLine($"用户密码: {userPassword}")
        Console.WriteLine($"存储哈希: {storedHash}")
        
        ' 模拟用户登录验证
        Dim loginAttempt As String = "MySecurePassword123!"
        Dim loginHash As String = CryptoUtils.Sha256Hash(loginAttempt)
        Dim isValid As Boolean = (storedHash = loginHash)
        
        Console.WriteLine($"登录尝试: {loginAttempt}")
        Console.WriteLine($"验证结果: {If(isValid, "✓ 密码正确", "✗ 密码错误")}")
        Console.WriteLine()

        ' =================================================================
        ' 12. 实用场景：API 签名
        ' =================================================================
        Console.WriteLine("12. 实用场景：API 请求签名")
        Console.WriteLine("---------------------------")
        
        Dim timestamp As String = DateTime.UtcNow.ToString("yyyyMMddHHmmss")
        Dim apiParams As String = $"timestamp={timestamp}&user=admin&action=get_data"
        Dim apiKey As String = "secret_api_key_xyz789"
        
        Dim signature As String = CryptoUtils.HmacSha256(apiParams, apiKey)
        
        Console.WriteLine($"请求参数: {apiParams}")
        Console.WriteLine($"API 密钥: {apiKey}")
        Console.WriteLine($"生成签名: {signature}")
        Console.WriteLine("  (服务器可使用相同算法验证签名)")
        Console.WriteLine()

        ' =================================================================
        ' 13. 实用场景：数据编码传输
        ' =================================================================
        Console.WriteLine("13. 实用场景：URL 参数编码")
        Console.WriteLine("--------------------------")
        
        Dim userData As String = "{""name"": ""张三"", ""age"": 25}"
        Dim encodedData As String = CryptoUtils.Base64UrlEncode(userData)
        Dim apiUrl As String = $"https://api.example.com/data?payload={encodedData}"
        
        Console.WriteLine($"原始 JSON: {userData}")
        Console.WriteLine($"URL 编码: {encodedData}")
        Console.WriteLine($"完整 URL: {apiUrl}")
        Console.WriteLine()

        ' =================================================================
        ' 完成
        ' =================================================================
        Console.WriteLine("============================================")
        Console.WriteLine("示例运行完成！")
        Console.WriteLine("============================================")
        Console.WriteLine()
        Console.WriteLine("按任意键退出...")
        Console.ReadKey()
    End Sub

End Module
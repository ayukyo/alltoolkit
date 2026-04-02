' =============================================================================
' AllToolkit - Crypto Utilities for VB.NET
' =============================================================================
' 一个零依赖的加密工具模块，提供常用的哈希、编码和加密功能。
' 适用于 .NET Framework 4.5+ 和 .NET Core/.NET 5+
'
' 功能列表:
' - MD5/SHA1/SHA256/SHA512 哈希计算
' - HMAC-SHA256 消息认证码
' - Base64 编码/解码
' - URL 安全的 Base64 编码
' - 随机字符串/密码生成
' - 简单的 XOR 加密/解密
' - 字符串混淆/反混淆
'
' 作者: AllToolkit Contributors
' 许可证: MIT
' =============================================================================

Imports System
Imports System.IO
Imports System.Security.Cryptography
Imports System.Text
Imports System.Text.RegularExpressions

Namespace AllToolkit

    ''' <summary>
    ''' 加密工具类，提供常用的哈希、编码和加密功能。
    ''' </summary>
    Public Module CryptoUtils

        ' =========================================================================
        ' 哈希计算
        ' =========================================================================

        ''' <summary>
        ''' 计算字符串的 MD5 哈希值（32位小写十六进制字符串）。
        ''' </summary>
        ''' <param name="input">要哈希的字符串</param>
        ''' <returns>MD5 哈希值的十六进制字符串，输入为空时返回空字符串</returns>
        Public Function Md5Hash(ByVal input As String) As String
            If String.IsNullOrEmpty(input) Then
                Return String.Empty
            End If

            Using md5 As MD5 = MD5.Create()
                Dim bytes As Byte() = Encoding.UTF8.GetBytes(input)
                Dim hashBytes As Byte() = md5.ComputeHash(bytes)
                Return BytesToHex(hashBytes)
            End Using
        End Function

        ''' <summary>
        ''' 计算字符串的 SHA1 哈希值（40位小写十六进制字符串）。
        ''' </summary>
        ''' <param name="input">要哈希的字符串</param>
        ''' <returns>SHA1 哈希值的十六进制字符串，输入为空时返回空字符串</returns>
        Public Function Sha1Hash(ByVal input As String) As String
            If String.IsNullOrEmpty(input) Then
                Return String.Empty
            End If

            Using sha1 As SHA1 = SHA1.Create()
                Dim bytes As Byte() = Encoding.UTF8.GetBytes(input)
                Dim hashBytes As Byte() = sha1.ComputeHash(bytes)
                Return BytesToHex(hashBytes)
            End Using
        End Function

        ''' <summary>
        ''' 计算字符串的 SHA256 哈希值（64位小写十六进制字符串）。
        ''' </summary>
        ''' <param name="input">要哈希的字符串</param>
        ''' <returns>SHA256 哈希值的十六进制字符串，输入为空时返回空字符串</returns>
        Public Function Sha256Hash(ByVal input As String) As String
            If String.IsNullOrEmpty(input) Then
                Return String.Empty
            End If

            Using sha256 As SHA256 = SHA256.Create()
                Dim bytes As Byte() = Encoding.UTF8.GetBytes(input)
                Dim hashBytes As Byte() = sha256.ComputeHash(bytes)
                Return BytesToHex(hashBytes)
            End Using
        End Function

        ''' <summary>
        ''' 计算字符串的 SHA512 哈希值（128位小写十六进制字符串）。
        ''' </summary>
        ''' <param name="input">要哈希的字符串</param>
        ''' <returns>SHA512 哈希值的十六进制字符串，输入为空时返回空字符串</returns>
        Public Function Sha512Hash(ByVal input As String) As String
            If String.IsNullOrEmpty(input) Then
                Return String.Empty
            End If

            Using sha512 As SHA512 = SHA512.Create()
                Dim bytes As Byte() = Encoding.UTF8.GetBytes(input)
                Dim hashBytes As Byte() = sha512.ComputeHash(bytes)
                Return BytesToHex(hashBytes)
            End Using
        End Function

        ''' <summary>
        ''' 计算文件的 SHA256 哈希值。
        ''' </summary>
        ''' <param name="filePath">文件路径</param>
        ''' <returns>SHA256 哈希值的十六进制字符串，文件不存在时返回空字符串</returns>
        Public Function Sha256File(ByVal filePath As String) As String
            If Not File.Exists(filePath) Then
                Return String.Empty
            End If

            Using sha256 As SHA256 = SHA256.Create()
                Using stream As FileStream = File.OpenRead(filePath)
                    Dim hashBytes As Byte() = sha256.ComputeHash(stream)
                    Return BytesToHex(hashBytes)
                End Using
            End Using
        End Function

        ' =========================================================================
        ' HMAC 计算
        ' =========================================================================

        ''' <summary>
        ''' 使用 HMAC-SHA256 计算消息认证码。
        ''' </summary>
        ''' <param name="message">要认证的消息</param>
        ''' <param name="secret">密钥</param>
        ''' <returns>HMAC-SHA256 的十六进制字符串</returns>
        Public Function HmacSha256(ByVal message As String, ByVal secret As String) As String
            If String.IsNullOrEmpty(message) OrElse String.IsNullOrEmpty(secret) Then
                Return String.Empty
            End If

            Using hmac As New HMACSHA256(Encoding.UTF8.GetBytes(secret))
                Dim messageBytes As Byte() = Encoding.UTF8.GetBytes(message)
                Dim hashBytes As Byte() = hmac.ComputeHash(messageBytes)
                Return BytesToHex(hashBytes)
            End Using
        End Function

        ' =========================================================================
        ' Base64 编码/解码
        ' =========================================================================

        ''' <summary>
        ''' 将字符串编码为 Base64。
        ''' </summary>
        ''' <param name="input">要编码的字符串</param>
        ''' <returns>Base64 编码的字符串</returns>
        Public Function Base64Encode(ByVal input As String) As String
            If String.IsNullOrEmpty(input) Then
                Return String.Empty
            End If

            Dim bytes As Byte() = Encoding.UTF8.GetBytes(input)
            Return Convert.ToBase64String(bytes)
        End Function

        ''' <summary>
        ''' 将 Base64 字符串解码为普通字符串。
        ''' </summary>
        ''' <param name="base64">Base64 编码的字符串</param>
        ''' <returns>解码后的字符串，输入无效时返回空字符串</returns>
        Public Function Base64Decode(ByVal base64 As String) As String
            If String.IsNullOrEmpty(base64) Then
                Return String.Empty
            End If

            Try
                Dim bytes As Byte() = Convert.FromBase64String(base64)
                Return Encoding.UTF8.GetString(bytes)
            Catch
                Return String.Empty
            End Try
        End Function

        ''' <summary>
        ''' 将字符串编码为 URL 安全的 Base64（替换 +/ 为 -_，移除填充 =）。
        ''' </summary>
        ''' <param name="input">要编码的字符串</param>
        ''' <returns>URL 安全的 Base64 字符串</returns>
        Public Function Base64UrlEncode(ByVal input As String) As String
            If String.IsNullOrEmpty(input) Then
                Return String.Empty
            End If

            Dim base64 As String = Base64Encode(input)
            ' 替换 URL 不安全的字符
            base64 = base64.Replace("+", "-").Replace("/", "_").TrimEnd("="c)
            Return base64
        End Function

        ''' <summary>
        ''' 将 URL 安全的 Base64 解码为普通字符串。
        ''' </summary>
        ''' <param name="base64Url">URL 安全的 Base64 字符串</param>
        ''' <returns>解码后的字符串，输入无效时返回空字符串</returns>
        Public Function Base64UrlDecode(ByVal base64Url As String) As String
            If String.IsNullOrEmpty(base64Url) Then
                Return String.Empty
            End If

            Try
                ' 还原标准 Base64
                Dim base64 As String = base64Url.Replace("-", "+").Replace("_", "/")
                ' 添加填充
                Select Case base64.Length Mod 4
                    Case 2
                        base64 &= "=="
                    Case 3
                        base64 &= "="
                End Select
                Return Base64Decode(base64)
            Catch
                Return String.Empty
            End Try
        End Function

        ' =========================================================================
        ' 随机字符串生成
        ' =========================================================================

        ''' <summary>
        ''' 生成指定长度的随机字符串。
        ''' </summary>
        ''' <param name="length">字符串长度</param>
        ''' <param name="chars">可选的字符集，默认为字母数字</param>
        ''' <returns>随机字符串</returns>
        Public Function RandomString(ByVal length As Integer, Optional ByVal chars As String = "") As String
            If length <= 0 Then
                Return String.Empty
            End If

            Dim charSet As String = If(String.IsNullOrEmpty(chars), 
                "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789", chars)
            
            Dim result As New StringBuilder(length)
            Dim charArray As Char() = charSet.ToCharArray()
            Dim charLength As Integer = charArray.Length

            Using rng As RandomNumberGenerator = RandomNumberGenerator.Create()
                Dim randomBytes(length - 1) As Byte
                rng.GetBytes(randomBytes)

                For Each b As Byte In randomBytes
                    result.Append(charArray(b Mod charLength))
                Next
            End Using

            Return result.ToString()
        End Function

        ''' <summary>
        ''' 生成指定长度的随机密码（包含大小写字母、数字和特殊字符）。
        ''' </summary>
        ''' <param name="length">密码长度，建议至少8位</param>
        ''' <returns>随机密码字符串</returns>
        Public Function RandomPassword(ByVal length As Integer) As String
            If length < 4 Then
                length = 8
            End If

            Dim upper As String = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            Dim lower As String = "abcdefghijklmnopqrstuvwxyz"
            Dim digits As String = "0123456789"
            Dim special As String = "!@#$%^&*()_+-=[]{}|;:,.<>?"
            Dim all As String = upper & lower & digits & special

            Dim result As New StringBuilder(length)

            ' 确保至少包含每种类型的字符
            result.Append(RandomString(1, upper))
            result.Append(RandomString(1, lower))
            result.Append(RandomString(1, digits))
            result.Append(RandomString(1, special))

            ' 填充剩余长度
            result.Append(RandomString(length - 4, all))

            ' 打乱顺序
            Return ShuffleString(result.ToString())
        End Function

        ''' <summary>
        ''' 生成 UUID v4（随机 UUID）。
        ''' </summary>
        ''' <returns>UUID 字符串（带连字符）</returns>
        Public Function GenerateUuid() As String
            Return Guid.NewGuid().ToString()
        End Function

        ''' <summary>
        ''' 生成无连字符的 UUID。
        ''' </summary>
        ''' <returns>32位 UUID 字符串</returns>
        Public Function GenerateUuidSimple() As String
            Return Guid.NewGuid().ToString("N")
        End Function

        ' =========================================================================
        ' 简单加密
        ' =========================================================================

        ''' <summary>
        ''' 使用 XOR 加密字符串（对称加密，同一密钥可解密）。
        ''' 注意：XOR 加密仅适用于简单混淆，不适用于安全敏感场景。
        ''' </summary>
        ''' <param name="input">要加密的字符串</param>
        ''' <param name="key">加密密钥</param>
        ''' <returns>XOR 加密后的 Base64 字符串</returns>
        Public Function XorEncrypt(ByVal input As String, ByVal key As String) As String
            If String.IsNullOrEmpty(input) OrElse String.IsNullOrEmpty(key) Then
                Return input
            End If

            Dim inputBytes As Byte() = Encoding.UTF8.GetBytes(input)
            Dim keyBytes As Byte() = Encoding.UTF8.GetBytes(key)
            Dim result(inputBytes.Length - 1) As Byte

            For i As Integer = 0 To inputBytes.Length - 1
                result(i) = inputBytes(i) Xor keyBytes(i Mod keyBytes.Length)
            Next

            Return Convert.ToBase64String(result)
        End Function

        ''' <summary>
        ''' 使用 XOR 解密字符串。
        ''' </summary>
        ''' <param name="encrypted">XOR 加密的 Base64 字符串</param>
        ''' <param name="key">解密密钥</param>
        ''' <returns>解密后的字符串</returns>
        Public Function XorDecrypt(ByVal encrypted As String, ByVal key As String) As String
            If String.IsNullOrEmpty(encrypted) OrElse String.IsNullOrEmpty(key) Then
                Return encrypted
            End If

            Try
                Dim encryptedBytes As Byte() = Convert.FromBase64String(encrypted)
                Dim keyBytes As Byte() = Encoding.UTF8.GetBytes(key)
                Dim result(encryptedBytes.Length - 1) As Byte

                For i As Integer = 0 To encryptedBytes.Length - 1
                    result(i) = encryptedBytes(i) Xor keyBytes(i Mod keyBytes.Length)
                Next

                Return Encoding.UTF8.GetString(result)
            Catch
                Return String.Empty
            End Try
        End Function

        ''' <summary>
        ''' 简单的字符串混淆（位移 + 反转）。
        ''' 注意：仅用于简单混淆，不提供真正的安全性。
        ''' </summary>
        ''' <param name="input">要混淆的字符串</param>
        ''' <returns>混淆后的字符串</returns>
        Public Function Obfuscate(ByVal input As String) As String
            If String.IsNullOrEmpty(input) Then
                Return String.Empty
            End If

            Dim bytes As Byte() = Encoding.UTF8.GetBytes(input)
            
            ' 每个字节加1
            For i As Integer = 0 To bytes.Length - 1
                bytes(i) = CByte((bytes(i) + 1) Mod 256)
            Next

            ' 反转
            Array.Reverse(bytes)
            
            Return Convert.ToBase64String(bytes)
        End Function

        ''' <summary>
        ''' 反混淆字符串。
        ''' </summary>
        ''' <param name="obfuscated">混淆后的字符串</param>
        ''' <returns>原始字符串</returns>
        Public Function Deobfuscate(ByVal obfuscated As String) As String
            If String.IsNullOrEmpty(obfuscated) Then
                Return String.Empty
            End If

            Try
                Dim bytes As Byte() = Convert.FromBase64String(obfuscated)
                
                ' 反转回来
                Array.Reverse(bytes)
                
                ' 每个字节减1
                For i As Integer = 0 To bytes.Length - 1
                    bytes(i) = CByte((bytes(i) - 1 + 256) Mod 256)
                Next

                Return Encoding.UTF8.GetString(bytes)
            Catch
                Return String.Empty
            End Try
        End Function

        ' =========================================================================
        ' 验证函数
        ' =========================================================================

        ''' <summary>
        ''' 验证字符串是否为有效的 MD5 哈希格式。
        ''' </summary>
        ''' <param name="hash">要验证的字符串</param>
        ''' <returns>是否为有效的 MD5 格式</returns>
        Public Function IsValidMd5(ByVal hash As String) As Boolean
            If String.IsNullOrEmpty(hash) Then
                Return False
            End If
            Return Regex.IsMatch(hash, "^[a-fA-F0-9]{32}$")
        End Function

        ''' <summary>
        ''' 验证字符串是否为有效的 SHA256 哈希格式。
        ''' </summary>
        ''' <param name="hash">要验证的字符串</param>
        ''' <returns>是否为有效的 SHA256 格式</returns>
        Public Function IsValidSha256(ByVal hash As String) As Boolean
            If String.IsNullOrEmpty(hash) Then
                Return False
            End If
            Return Regex.IsMatch(hash, "^[a-fA-F0-9]{64}$")
        End Function

        ''' <summary>
        ''' 验证字符串是否为有效的 Base64。
        ''' </summary>
        ''' <param name="base64">要验证的字符串</param>
        ''' <returns>是否为有效的 Base64</returns>
        Public Function IsValidBase64(ByVal base64 As String) As Boolean
            If String.IsNullOrEmpty(base64) Then
                Return False
            End If

            Try
                Convert.FromBase64String(base64)
                Return True
            Catch
                Return False
            End Try
        End Function

        ' =========================================================================
        ' 辅助函数
        ' =========================================================================

        ''' <summary>
        ''' 将字节数组转换为十六进制字符串。
        ''' </summary>
        ''' <param name="bytes">字节数组</param>
        ''' <returns>小写十六进制字符串</returns>
        Private Function BytesToHex(ByVal bytes As Byte()) As String
            Dim hex As New StringBuilder(bytes.Length * 2)
            For Each b As Byte In bytes
                hex.AppendFormat("{0:x2}", b)
            Next
            Return hex.ToString()
        End Function

        ''' <summary>
        ''' 随机打乱字符串中的字符顺序。
        ''' </summary>
        ''' <param name="input">输入字符串</param>
        ''' <returns>打乱后的字符串</returns>
        Private Function ShuffleString(ByVal input As String) As String
            Dim chars As Char() = input.ToCharArray()
            Dim n As Integer = chars.Length

            Using rng As RandomNumberGenerator = RandomNumberGenerator.Create()
                Dim randomBytes(3) As Byte

                For i As Integer = n - 1 To 1 Step -1
                    rng.GetBytes(randomBytes)
                    Dim j As Integer = BitConverter.ToInt32(randomBytes, 0) Mod (i + 1)
                    If j < 0 Then j = -j
                    
                    ' 交换
                    Dim temp As Char = chars(i)
                    chars(i) = chars(j)
                    chars(j) = temp
                Next
            End Using

            Return New String(chars)
        End Function

    End Module

End Namespace

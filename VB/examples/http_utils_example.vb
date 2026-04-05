' =============================================================================
' AllToolkit - VB HTTP Utilities Example
' =============================================================================
' HTTP 工具模块使用示例
' 编译: vbc http_utils_example.vb ../http_utils/mod.vb /r:System.Web.Extensions.dll /out:http_example.exe
' 运行: http_example.exe
' =============================================================================

Imports System
Imports System.Collections.Generic
Imports AllToolkit

Module HttpUtilsExample

    Sub Main()
        Console.WriteLine("=== VB HTTP Utilities Examples ===")
        Console.WriteLine()

        ' 示例 1: URL 编码和解码
        Example1_UrlEncoding()

        ' 示例 2: 构建查询字符串
        Example2_QueryString()

        ' 示例 3: 构建完整 URL
        Example3_BuildUrl()

        ' 示例 4: 解析 URL
        Example4_ParseUrl()

        ' 示例 5: URL 验证
        Example5_ValidateUrl()

        ' 示例 6: HTTP 选项配置
        Example6_HttpOptions()

        ' 示例 7: HTTP GET 请求 (需要网络连接)
        ' Example7_GetRequest()

        ' 示例 8: HTTP POST 请求 (需要网络连接)
        ' Example8_PostRequest()

        ' 示例 9: 使用代理和认证
        Example9_ProxyAndAuth()

        Console.WriteLine()
        Console.WriteLine("=== All examples completed ===")
        Console.WriteLine("Note: Network examples (7-8) are commented out to avoid external dependencies.")
        Console.WriteLine("Uncomment them to test with actual HTTP requests.")
    End Sub

    ' 示例 1: URL 编码和解码
    Sub Example1_UrlEncoding()
        Console.WriteLine("--- Example 1: URL Encoding ---")

        ' 基本编码
        Dim encoded1 As String = HttpUtils.UrlEncode("hello world")
        Console.WriteLine("Encode 'hello world': " & encoded1)

        ' 特殊字符编码
        Dim encoded2 As String = HttpUtils.UrlEncode("test@example.com")
        Console.WriteLine("Encode 'test@example.com': " & encoded2)

        ' 中文字符编码
        Dim encoded3 As String = HttpUtils.UrlEncode("你好世界")
        Console.WriteLine("Encode '你好世界': " & encoded3)

        ' URL 解码
        Dim decoded As String = HttpUtils.UrlDecode("hello%20world")
        Console.WriteLine("Decode 'hello%20world': " & decoded)

        Console.WriteLine()
    End Sub

    ' 示例 2: 构建查询字符串
    Sub Example2_QueryString()
        Console.WriteLine("--- Example 2: Query String Building ---")

        ' 创建参数字典
        Dim params As New Dictionary(Of String, String)()
        params.Add("name", "John Doe")
        params.Add("age", "30")
        params.Add("city", "New York")

        ' 构建查询字符串
        Dim queryString As String = HttpUtils.BuildQueryString(params)
        Console.WriteLine("Query string: " & queryString)

        ' 空参数
        Dim emptyParams As New Dictionary(Of String, String)()
        Dim emptyQuery As String = HttpUtils.BuildQueryString(emptyParams)
        Console.WriteLine("Empty params: '" & emptyQuery & "'")

        Console.WriteLine()
    End Sub

    ' 示例 3: 构建完整 URL
    Sub Example3_BuildUrl()
        Console.WriteLine("--- Example 3: URL Building ---")

        ' 基础 URL + 参数
        Dim params1 As New Dictionary(Of String, String)()
        params1.Add("page", "1")
        params1.Add("size", "10")
        Dim url1 As String = HttpUtils.BuildUrl("https://api.example.com/users", params1)
        Console.WriteLine("URL 1: " & url1)

        ' 已有查询参数的 URL + 新参数
        Dim params2 As New Dictionary(Of String, String)()
        params2.Add("sort", "name")
        params2.Add("order", "asc")
        Dim url2 As String = HttpUtils.BuildUrl("https://api.example.com/users?filter=active", params2)
        Console.WriteLine("URL 2: " & url2)

        ' 添加单个参数
        Dim params3 As New Dictionary(Of String, String)()
        params3.Add("q", "search term")
        Dim url3 As String = HttpUtils.AddQueryParams("https://api.example.com/search", params3)
        Console.WriteLine("URL 3: " & url3)

        Console.WriteLine()
    End Sub

    ' 示例 4: 解析 URL
    Sub Example4_ParseUrl()
        Console.WriteLine("--- Example 4: URL Parsing ---")

        Dim url As String = "https://api.example.com:8080/v1/users?id=123&name=test#section"
        Dim parts As Dictionary(Of String, String) = HttpUtils.ParseUrl(url)

        Console.WriteLine("Parsing: " & url)
        Console.WriteLine("  Scheme: " & parts("scheme"))
        Console.WriteLine("  Host: " & parts("host"))
        Console.WriteLine("  Port: " & parts("port"))
        Console.WriteLine("  Path: " & parts("path"))
        Console.WriteLine("  Query: " & parts("query"))
        Console.WriteLine("  Fragment: " & parts("fragment"))

        ' 提取域名和路径
        Console.WriteLine()
        Console.WriteLine("Domain: " & HttpUtils.GetDomain(url))
        Console.WriteLine("Path: " & HttpUtils.GetPath(url))

        Console.WriteLine()
    End Sub

    ' 示例 5: URL 验证
    Sub Example5_ValidateUrl()
        Console.WriteLine("--- Example 5: URL Validation ---")

        Dim urls As String() = New String() {
            "https://www.example.com",
            "http://localhost:8080/api",
            "https://api.example.com/v1/users?page=1",
            "not-a-valid-url",
            "ftp://files.example.com",
            ""
        }

        For Each url As String In urls
            Dim isValid As Boolean = HttpUtils.IsValidUrl(url)
            Console.WriteLine("'" & url & "' is valid: " & isValid)
        Next

        Console.WriteLine()
    End Sub

    ' 示例 6: HTTP 选项配置
    Sub Example6_HttpOptions()
        Console.WriteLine("--- Example 6: HTTP Options ---")

        ' 创建默认选项
        Dim options As New HttpOptions()
        Console.WriteLine("Default timeout: " & options.Timeout & "ms")
        Console.WriteLine("Default allow redirect: " & options.AllowRedirect)

        ' 自定义选项
        options.Timeout = 60000
        options.AllowRedirect = False
        options.ValidateSsl = True
        options.AddHeader("Authorization", "Bearer token123")
        options.AddHeader("Accept", "application/json")

        Console.WriteLine()
        Console.WriteLine("Custom timeout: " & options.Timeout & "ms")
        Console.WriteLine("Custom allow redirect: " & options.AllowRedirect)
        Console.WriteLine("Headers count: " & options.Headers.Count)

        Console.WriteLine()
    End Sub

    ' 示例 7: HTTP GET 请求 (需要网络连接)
    ' 取消注释以测试实际网络请求
    'Sub Example7_GetRequest()
    '    Console.WriteLine("--- Example 7: HTTP GET Request ---")
    '
    '    Try
    '        ' 发送 GET 请求到测试 API
    '        Dim response As HttpResponse = HttpUtils.Get("https://httpbin.org/get")
    '
    '        Console.WriteLine("Status: " & response.StatusCode)
    '        Console.WriteLine("Success: " & response.IsSuccess)
    '        Console.WriteLine("Response time: " & response.ResponseTime & "ms")
    '        Console.WriteLine("Content-Type: " & response.ContentType)
    '
    '        ' 检查是否为 JSON
    '        If response.IsJson() Then
    '            Console.WriteLine("Response is valid JSON")
    '        End If
    '
    '        ' 输出部分响应体
    '        Dim preview As String = response.Body
    '        If preview.Length > 200 Then
    '            preview = preview.Substring(0, 200) & "..."
    '        End If
    '        Console.WriteLine("Body preview: " & preview)
    '
    '    Catch ex As Exception
    '        Console.WriteLine("Error: " & ex.Message)
    '    End Try
    '
    '    Console.WriteLine()
    'End Sub

    ' 示例 8: HTTP POST 请求 (需要网络连接)
    ' 取消注释以测试实际网络请求
    'Sub Example8_PostRequest()
    '    Console.WriteLine("--- Example 8: HTTP POST Request ---")
    '
    '    Try
    '        ' POST JSON 数据
    '        Dim data As New Dictionary(Of String, Object)()
    '        data.Add("name", "John Doe")
    '        data.Add("email", "john@example.com")
    '        data.Add("age", 30)
    '
    '        Dim response As HttpResponse = HttpUtils.PostJson("https://httpbin.org/post", data)
    '
    '        Console.WriteLine("Status: " & response.StatusCode)
    '        Console.WriteLine("Success: " & response.IsSuccess)
    '
    '        ' POST 表单数据
    '        Dim formData As New Dictionary(Of String, String)()
    '        formData.Add("username", "admin")
    '        formData.Add("password", "secret123")
    '
    '        Dim formResponse As HttpResponse = HttpUtils.PostForm("https://httpbin.org/post", formData)
    '        Console.WriteLine("Form POST status: " & formResponse.StatusCode)
    '
    '    Catch ex As Exception
    '        Console.WriteLine("Error: " & ex.Message)
    '    End Try
    '
    '    Console.WriteLine()
    'End Sub

    ' 示例 9: 使用代理和认证
    Sub Example9_ProxyAndAuth()
        Console.WriteLine("--- Example 9: Proxy and Authentication ---")

        ' 创建带认证的选项
        Dim options As New HttpOptions()
        options.Username = "api_user"
        options.Password = "api_secret"
        options.AddHeader("X-API-Key", "my-api-key")
        options.AddHeader("Accept", "application/json")

        ' 代理设置 (示例，非实际代理)
        ' options.Proxy = "http://proxy.example.com:8080"

        Console.WriteLine("Username: " & options.Username)
        Console.WriteLine("Password: " & options.Password)
        Console.WriteLine("Headers:")
        For Each header As KeyValuePair(Of String, String) In options.Headers
            Console.WriteLine("  " & header.Key & ": " & header.Value)
        Next

        Console.WriteLine()
        Console.WriteLine("Note: Uncomment proxy setting to use actual proxy server.")

        Console.WriteLine()
    End Sub

End Module
' =============================================================================
' AllToolkit - VB HTTP Utilities Test
' =============================================================================
' HTTP 工具模块的单元测试
' 运行: vbc http_utils_test.vb mod.vb /r:System.Web.Extensions.dll /out:http_test.exe && http_test.exe
' =============================================================================

Imports System
Imports System.Collections.Generic
Imports AllToolkit

Module HttpUtilsTest

    Sub Main()
        Console.WriteLine("=== VB HTTP Utilities Test Suite ===")
        Console.WriteLine()

        Dim passed As Integer = 0
        Dim failed As Integer = 0

        ' 测试 URL 编码
        Try
            TestUrlEncode()
            passed += 1
            Console.WriteLine("[PASS] TestUrlEncode")
        Catch ex As Exception
            failed += 1
            Console.WriteLine("[FAIL] TestUrlEncode: " & ex.Message)
        End Try

        ' 测试 URL 解码
        Try
            TestUrlDecode()
            passed += 1
            Console.WriteLine("[PASS] TestUrlDecode")
        Catch ex As Exception
            failed += 1
            Console.WriteLine("[FAIL] TestUrlDecode: " & ex.Message)
        End Try

        ' 测试查询字符串构建
        Try
            TestBuildQueryString()
            passed += 1
            Console.WriteLine("[PASS] TestBuildQueryString")
        Catch ex As Exception
            failed += 1
            Console.WriteLine("[FAIL] TestBuildQueryString: " & ex.Message)
        End Try

        ' 测试 URL 构建
        Try
            TestBuildUrl()
            passed += 1
            Console.WriteLine("[PASS] TestBuildUrl")
        Catch ex As Exception
            failed += 1
            Console.WriteLine("[FAIL] TestBuildUrl: " & ex.Message)
        End Try

        ' 测试 URL 验证
        Try
            TestIsValidUrl()
            passed += 1
            Console.WriteLine("[PASS] TestIsValidUrl")
        Catch ex As Exception
            failed += 1
            Console.WriteLine("[FAIL] TestIsValidUrl: " & ex.Message)
        End Try

        ' 测试 URL 解析
        Try
            TestParseUrl()
            passed += 1
            Console.WriteLine("[PASS] TestParseUrl")
        Catch ex As Exception
            failed += 1
            Console.WriteLine("[FAIL] TestParseUrl: " & ex.Message)
        End Try

        ' 测试域名提取
        Try
            TestGetDomain()
            passed += 1
            Console.WriteLine("[PASS] TestGetDomain")
        Catch ex As Exception
            failed += 1
            Console.WriteLine("[FAIL] TestGetDomain: " & ex.Message)
        End Try

        ' 测试路径提取
        Try
            TestGetPath()
            passed += 1
            Console.WriteLine("[PASS] TestGetPath")
        Catch ex As Exception
            failed += 1
            Console.WriteLine("[FAIL] TestGetPath: " & ex.Message)
        End Try

        ' 测试添加查询参数
        Try
            TestAddQueryParams()
            passed += 1
            Console.WriteLine("[PASS] TestAddQueryParams")
        Catch ex As Exception
            failed += 1
            Console.WriteLine("[FAIL] TestAddQueryParams: " & ex.Message)
        End Try

        ' 测试空值处理
        Try
            TestNullHandling()
            passed += 1
            Console.WriteLine("[PASS] TestNullHandling")
        Catch ex As Exception
            failed += 1
            Console.WriteLine("[FAIL] TestNullHandling: " & ex.Message)
        End Try

        ' 测试 HttpOptions
        Try
            TestHttpOptions()
            passed += 1
            Console.WriteLine("[PASS] TestHttpOptions")
        Catch ex As Exception
            failed += 1
            Console.WriteLine("[FAIL] TestHttpOptions: " & ex.Message)
        End Try

        ' 测试 HttpResponse
        Try
            TestHttpResponse()
            passed += 1
            Console.WriteLine("[PASS] TestHttpResponse")
        Catch ex As Exception
            failed += 1
            Console.WriteLine("[FAIL] TestHttpResponse: " & ex.Message)
        End Try

        Console.WriteLine()
        Console.WriteLine("=== Test Summary ===")
        Console.WriteLine("Passed: " & passed)
        Console.WriteLine("Failed: " & failed)
        Console.WriteLine("Total:  " & (passed + failed))

        If failed = 0 Then
            Console.WriteLine("All tests passed!")
        Else
            Console.WriteLine("Some tests failed!")
        End If
    End Sub

    ' 测试 URL 编码
    Sub TestUrlEncode()
        AssertEqual(HttpUtils.UrlEncode("hello world"), "hello%20world", "Basic URL encode")
        AssertEqual(HttpUtils.UrlEncode("test@example.com"), "test%40example.com", "Email encode")
        AssertEqual(HttpUtils.UrlEncode("a+b=c"), "a%2Bb%3Dc", "Special chars encode")
        AssertEqual(HttpUtils.UrlEncode(""), "", "Empty string encode")
        AssertEqual(HttpUtils.UrlEncode(Nothing), "", "Null encode")
    End Sub

    ' 测试 URL 解码
    Sub TestUrlDecode()
        AssertEqual(HttpUtils.UrlDecode("hello%20world"), "hello world", "Basic URL decode")
        AssertEqual(HttpUtils.UrlDecode("test%40example.com"), "test@example.com", "Email decode")
        AssertEqual(HttpUtils.UrlDecode("a%2Bb%3Dc"), "a+b=c", "Special chars decode")
        AssertEqual(HttpUtils.UrlDecode(""), "", "Empty string decode")
        AssertEqual(HttpUtils.UrlDecode(Nothing), "", "Null decode")
    End Sub

    ' 测试查询字符串构建
    Sub TestBuildQueryString()
        Dim params1 As New Dictionary(Of String, String)()
        params1.Add("name", "John")
        params1.Add("age", "30")
        AssertEqual(HttpUtils.BuildQueryString(params1), "name=John&age=30", "Basic query string")

        Dim params2 As New Dictionary(Of String, String)()
        params2.Add("q", "hello world")
        AssertEqual(HttpUtils.BuildQueryString(params2), "q=hello%20world", "Encoded query string")

        Dim params3 As New Dictionary(Of String, String)()
        AssertEqual(HttpUtils.BuildQueryString(params3), "", "Empty params")

        AssertEqual(HttpUtils.BuildQueryString(Nothing), "", "Null params")
    End Sub

    ' 测试 URL 构建
    Sub TestBuildUrl()
        Dim params As New Dictionary(Of String, String)()
        params.Add("page", "1")
        params.Add("size", "10")
        AssertEqual(HttpUtils.BuildUrl("https://api.example.com/users", params), "https://api.example.com/users?page=1&size=10", "Build URL with params")

        Dim params2 As New Dictionary(Of String, String)()
        params2.Add("q", "test")
        AssertEqual(HttpUtils.BuildUrl("https://api.example.com/search?filter=active", params2), "https://api.example.com/search?filter=active&q=test", "Build URL with existing query")

        AssertEqual(HttpUtils.BuildUrl("https://api.example.com/users", Nothing), "https://api.example.com/users", "Build URL without params")
        AssertEqual(HttpUtils.BuildUrl("", params), "", "Empty base URL")
    End Sub

    ' 测试 URL 验证
    Sub TestIsValidUrl()
        AssertTrue(HttpUtils.IsValidUrl("https://www.example.com"), "Valid HTTPS URL")
        AssertTrue(HttpUtils.IsValidUrl("http://localhost:8080"), "Valid HTTP URL with port")
        AssertTrue(HttpUtils.IsValidUrl("https://api.example.com/v1/users"), "Valid URL with path")
        AssertFalse(HttpUtils.IsValidUrl("not-a-url"), "Invalid URL")
        AssertFalse(HttpUtils.IsValidUrl(""), "Empty URL")
        AssertFalse(HttpUtils.IsValidUrl(Nothing), "Null URL")
    End Sub

    ' 测试 URL 解析
    Sub TestParseUrl()
        Dim result As Dictionary(Of String, String) = HttpUtils.ParseUrl("https://api.example.com:8080/v1/users?id=123")
        AssertEqual(result("scheme"), "https", "Parse scheme")
        AssertEqual(result("host"), "api.example.com", "Parse host")
        AssertEqual(result("port"), "8080", "Parse port")
        AssertEqual(result("path"), "/v1/users", "Parse path")
        AssertEqual(result("query"), "?id=123", "Parse query")

        Dim emptyResult As Dictionary(Of String, String) = HttpUtils.ParseUrl("")
        AssertEqual(emptyResult.Count, 0, "Parse empty URL")

        Dim nullResult As Dictionary(Of String, String) = HttpUtils.ParseUrl(Nothing)
        AssertEqual(nullResult.Count, 0, "Parse null URL")
    End Sub

    ' 测试域名提取
    Sub TestGetDomain()
        AssertEqual(HttpUtils.GetDomain("https://www.example.com/path"), "www.example.com", "Get domain")
        AssertEqual(HttpUtils.GetDomain("http://localhost:8080"), "localhost", "Get localhost domain")
        AssertEqual(HttpUtils.GetDomain(""), "", "Get domain from empty URL")
        AssertEqual(HttpUtils.GetDomain(Nothing), "", "Get domain from null URL")
    End Sub

    ' 测试路径提取
    Sub TestGetPath()
        AssertEqual(HttpUtils.GetPath("https://api.example.com/v1/users"), "/v1/users", "Get path")
        AssertEqual(HttpUtils.GetPath("https://example.com"), "/", "Get root path")
        AssertEqual(HttpUtils.GetPath(""), "", "Get path from empty URL")
        AssertEqual(HttpUtils.GetPath(Nothing), "", "Get path from null URL")
    End Sub

    ' 测试添加查询参数
    Sub TestAddQueryParams()
        Dim params As New Dictionary(Of String, String)()
        params.Add("page", "2")
        AssertEqual(HttpUtils.AddQueryParams("https://api.example.com/users", params), "https://api.example.com/users?page=2", "Add params to clean URL")

        Dim params2 As New Dictionary(Of String, String)()
        params2.Add("sort", "name")
        AssertEqual(HttpUtils.AddQueryParams("https://api.example.com/users?page=1", params2), "https://api.example.com/users?page=1&sort=name", "Add params to URL with existing query")
    End Sub

    ' 测试空值处理
    Sub TestNullHandling()
        ' 测试空字符串处理
        AssertEqual(HttpUtils.UrlEncode(""), "", "Empty string URL encode")
        AssertEqual(HttpUtils.UrlDecode(""), "", "Empty string URL decode")
        AssertEqual(HttpUtils.BuildUrl("", Nothing), "", "Empty URL build")
        AssertEqual(HttpUtils.GetDomain(""), "", "Empty domain")
        AssertEqual(HttpUtils.GetPath(""), "", "Empty path")

        ' 测试 null 处理
        AssertEqual(HttpUtils.UrlEncode(Nothing), "", "Null URL encode")
        AssertEqual(HttpUtils.UrlDecode(Nothing), "", "Null URL decode")
        AssertEqual(HttpUtils.GetDomain(Nothing), "", "Null domain")
        AssertEqual(HttpUtils.GetPath(Nothing), "", "Null path")
    End Sub

    ' 测试 HttpOptions
    Sub TestHttpOptions()
        Dim options As New HttpOptions()
        AssertEqual(options.Timeout, 30000, "Default timeout")
        AssertEqual(options.AllowRedirect, True, "Default allow redirect")
        AssertEqual(options.MaxRedirects, 10, "Default max redirects")
        AssertEqual(options.ValidateSsl, True, "Default validate SSL")

        options.AddHeader("Authorization", "Bearer token123")
        AssertEqual(options.Headers("Authorization"), "Bearer token123", "Add header")

        options.Timeout = 60000
        AssertEqual(options.Timeout, 60000, "Set timeout")
    End Sub

    ' 测试 HttpResponse
    Sub TestHttpResponse()
        Dim response As New HttpResponse()
        response.StatusCode = 200
        response.StatusDescription = "OK"
        response.Body = "{\"name\":\"test\"}"
        response.IsSuccess = True
        response.ResponseTime = 150

        AssertEqual(response.StatusCode, 200, "Response status code")
        AssertEqual(response.IsSuccess, True, "Response success")
        AssertEqual(response.ToString(), "HTTP 200 OK (150ms)", "Response toString")

        ' 测试 JSON 检测
        AssertEqual(response.IsJson(), True, "Is JSON")

        response.Body = "not json"
        AssertEqual(response.IsJson(), False, "Is not JSON")

        ' 测试响应头
        response.Headers.Add("Content-Type", "application/json")
        AssertEqual(response.GetHeader("Content-Type"), "application/json", "Get header")
        AssertEqual(response.GetHeader("X-Custom"), "", "Get non-existent header")
    End Sub

    ' ============================================================================
    ' 断言辅助方法
    ' ============================================================================

    Sub AssertEqual(actual As Object, expected As Object, message As String)
        If Not Object.Equals(actual, expected) Then
            Throw New Exception(String.Format("{0}: expected '{1}', got '{2}'", message, expected, actual))
        End If
    End Sub

    Sub AssertTrue(condition As Boolean, message As String)
        If Not condition Then
            Throw New Exception(String.Format("{0}: expected True, got False", message))
        End If
    End Sub

    Sub AssertFalse(condition As Boolean, message As String)
        If condition Then
            Throw New Exception(String.Format("{0}: expected False, got True", message))
        End If
    End Sub

End Module
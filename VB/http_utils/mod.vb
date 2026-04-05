' =============================================================================
' AllToolkit - VB HTTP Utilities
' =============================================================================
' 一个零依赖的 HTTP 请求工具库，仅使用 .NET 标准库
' 支持 .NET Framework 4.5+ / .NET Core / .NET 5+
' =============================================================================

Imports System.IO
Imports System.Net
Imports System.Text
Imports System.Collections.Generic

Namespace AllToolkit

    ''' <summary>
    ''' HTTP 响应类，封装 HTTP 响应数据
    ''' </summary>
    Public Class HttpResponse
        ''' <summary>HTTP 状态码</summary>
        Public Property StatusCode As Integer
        ''' <summary>HTTP 状态描述</summary>
        Public Property StatusDescription As String
        ''' <summary>响应内容</summary>
        Public Property Body As String
        ''' <summary>响应字节数据</summary>
        Public Property BodyBytes As Byte()
        ''' <summary>响应头集合</summary>
        Public Property Headers As Dictionary(Of String, String)
        ''' <summary>请求 URL</summary>
        Public Property Url As String
        ''' <summary>请求是否成功 (状态码 200-299)</summary>
        Public Property IsSuccess As Boolean
        ''' <summary>响应时间 (毫秒)</summary>
        Public Property ResponseTime As Long
        ''' <summary>内容类型</summary>
        Public Property ContentType As String

        ''' <summary>
        ''' 构造函数
        ''' </summary>
        Public Sub New()
            Headers = New Dictionary(Of String, String)(StringComparer.OrdinalIgnoreCase)
            Body = String.Empty
            BodyBytes = New Byte() {}
        End Sub

        ''' <summary>
        ''' 将响应体解析为 JSON 对象
        ''' </summary>
        ''' <returns>解析后的对象，失败返回 Nothing</returns>
        Public Function Json() As Object
            Try
                If String.IsNullOrEmpty(Body) Then Return Nothing
                Dim serializer As New System.Web.Script.Serialization.JavaScriptSerializer()
                Return serializer.DeserializeObject(Body)
            Catch
                Return Nothing
            End Try
        End Function

        ''' <summary>
        ''' 检查响应体是否为有效的 JSON
        ''' </summary>
        Public Function IsJson() As Boolean
            Try
                If String.IsNullOrEmpty(Body) Then Return False
                Dim serializer As New System.Web.Script.Serialization.JavaScriptSerializer()
                serializer.DeserializeObject(Body)
                Return True
            Catch
                Return False
            End Try
        End Function

        ''' <summary>
        ''' 获取指定名称的响应头值
        ''' </summary>
        ''' <param name="name">响应头名称</param>
        ''' <returns>响应头值，不存在返回空字符串</returns>
        Public Function GetHeader(name As String) As String
            If Headers.ContainsKey(name) Then
                Return Headers(name)
            End If
            Return String.Empty
        End Function

        ''' <summary>
        ''' 返回响应的字符串表示
        ''' </summary>
        Public Overrides Function ToString() As String
            Return String.Format("HTTP {0} {1} ({2}ms)", StatusCode, StatusDescription, ResponseTime)
        End Function
    End Class

    ''' <summary>
    ''' HTTP 请求选项类
    ''' </summary>
    Public Class HttpOptions
        ''' <summary>请求头字典</summary>
        Public Property Headers As Dictionary(Of String, String)
        ''' <summary>请求超时 (毫秒)，默认 30000</summary>
        Public Property Timeout As Integer
        ''' <summary>是否跟随重定向，默认 True</summary>
        Public Property AllowRedirect As Boolean
        ''' <summary>最大重定向次数，默认 10</summary>
        Public Property MaxRedirects As Integer
        ''' <summary>请求内容类型</summary>
        Public Property ContentType As String
        ''' <summary>是否验证 SSL 证书，默认 True</summary>
        Public Property ValidateSsl As Boolean
        ''' <summary>代理服务器地址</summary>
        Public Property Proxy As String
        ''' <summary>基本认证用户名</summary>
        Public Property Username As String
        ''' <summary>基本认证密码</summary>
        Public Property Password As String

        ''' <summary>
        ''' 构造函数，设置默认值
        ''' </summary>
        Public Sub New()
            Headers = New Dictionary(Of String, String)(StringComparer.OrdinalIgnoreCase)
            Timeout = 30000
            AllowRedirect = True
            MaxRedirects = 10
            ValidateSsl = True
            ContentType = "application/x-www-form-urlencoded"
        End Sub

        ''' <summary>
        ''' 添加请求头
        ''' </summary>
        ''' <param name="key">请求头名称</param>
        ''' <param name="value">请求头值</param>
        Public Sub AddHeader(key As String, value As String)
            Headers(key) = value
        End Sub
    End Class

    ''' <summary>
    ''' HTTP 工具类，提供各种 HTTP 请求方法
    ''' </summary>
    Public NotInheritable Class HttpUtils

        ' 私有构造函数，防止实例化
        Private Sub New()
        End Sub

        ' ============================================================================
        ' HTTP 请求方法
        ' ============================================================================

        ''' <summary>
        ''' 发送 GET 请求
        ''' </summary>
        ''' <param name="url">请求 URL</param>
        ''' <param name="options">请求选项，可选</param>
        ''' <returns>HTTP 响应对象</returns>
        Public Shared Function Get(url As String, Optional options As HttpOptions = Nothing) As HttpResponse
            Return SendRequest(url, "GET", Nothing, Nothing, options)
        End Function

        ''' <summary>
        ''' 发送 POST 请求
        ''' </summary>
        ''' <param name="url">请求 URL</param>
        ''' <param name="body">请求体内容</param>
        ''' <param name="contentType">内容类型</param>
        ''' <param name="options">请求选项，可选</param>
        ''' <returns>HTTP 响应对象</returns>
        Public Shared Function Post(url As String, body As String, contentType As String, Optional options As HttpOptions = Nothing) As HttpResponse
            Return SendRequest(url, "POST", body, contentType, options)
        End Function

        ''' <summary>
        ''' 发送 POST 请求 (JSON 数据)
        ''' </summary>
        ''' <param name="url">请求 URL</param>
        ''' <param name="jsonData">JSON 数据对象</param>
        ''' <param name="options">请求选项，可选</param>
        ''' <returns>HTTP 响应对象</returns>
        Public Shared Function PostJson(url As String, jsonData As Object, Optional options As HttpOptions = Nothing) As HttpResponse
            Dim serializer As New System.Web.Script.Serialization.JavaScriptSerializer()
            Dim jsonBody As String = serializer.Serialize(jsonData)
            Return SendRequest(url, "POST", jsonBody, "application/json", options)
        End Function

        ''' <summary>
        ''' 发送 POST 请求 (表单数据)
        ''' </summary>
        ''' <param name="url">请求 URL</param>
        ''' <param name="formData">表单数据字典</param>
        ''' <param name="options">请求选项，可选</param>
        ''' <returns>HTTP 响应对象</returns>
        Public Shared Function PostForm(url As String, formData As Dictionary(Of String, String), Optional options As HttpOptions = Nothing) As HttpResponse
            Dim body As String = BuildQueryString(formData)
            Return SendRequest(url, "POST", body, "application/x-www-form-urlencoded", options)
        End Function

        ''' <summary>
        ''' 发送 PUT 请求
        ''' </summary>
        ''' <param name="url">请求 URL</param>
        ''' <param name="body">请求体内容</param>
        ''' <param name="contentType">内容类型</param>
        ''' <param name="options">请求选项，可选</param>
        ''' <returns>HTTP 响应对象</returns>
        Public Shared Function Put(url As String, body As String, contentType As String, Optional options As HttpOptions = Nothing) As HttpResponse
            Return SendRequest(url, "PUT", body, contentType, options)
        End Function

        ''' <summary>
        ''' 发送 DELETE 请求
        ''' </summary>
        ''' <param name="url">请求 URL</param>
        ''' <param name="options">请求选项，可选</param>
        ''' <returns>HTTP 响应对象</returns>
        Public Shared Function Delete(url As String, Optional options As HttpOptions = Nothing) As HttpResponse
            Return SendRequest(url, "DELETE", Nothing, Nothing, options)
        End Function

        ''' <summary>
        ''' 发送 PATCH 请求
        ''' </summary>
        ''' <param name="url">请求 URL</param>
        ''' <param name="body">请求体内容</param>
        ''' <param name="contentType">内容类型</param>
        ''' <param name="options">请求选项，可选</param>
        ''' <returns>HTTP 响应对象</returns>
        Public Shared Function Patch(url As String, body As String, contentType As String, Optional options As HttpOptions = Nothing) As HttpResponse
            Return SendRequest(url, "PATCH", body, contentType, options)
        End Function

        ''' <summary>
        ''' 发送 HEAD 请求
        ''' </summary>
        ''' <param name="url">请求 URL</param>
        ''' <param name="options">请求选项，可选</param>
        ''' <returns>HTTP 响应对象</returns>
        Public Shared Function Head(url As String, Optional options As HttpOptions = Nothing) As HttpResponse
            Return SendRequest(url, "HEAD", Nothing, Nothing, options)
        End Function

        ' ============================================================================
        ' URL 工具方法
        ' ============================================================================

        ''' <summary>
        ''' URL 编码字符串
        ''' </summary>
        ''' <param name="value">要编码的字符串</param>
        ''' <returns>编码后的字符串</returns>
        Public Shared Function UrlEncode(value As String) As String
            If String.IsNullOrEmpty(value) Then Return String.Empty
            Return Uri.EscapeDataString(value)
        End Function

        ''' <summary>
        ''' URL 解码字符串
        ''' </summary>
        ''' <param name="value">要解码的字符串</param>
        ''' <returns>解码后的字符串</returns>
        Public Shared Function UrlDecode(value As String) As String
            If String.IsNullOrEmpty(value) Then Return String.Empty
            Try
                Return Uri.UnescapeDataString(value)
            Catch
                Return value
            End Try
        End Function

        ''' <summary>
        ''' 构建查询字符串
        ''' </summary>
        ''' <param name="parameters">参数字典</param>
        ''' <returns>URL 编码的查询字符串</returns>
        Public Shared Function BuildQueryString(parameters As Dictionary(Of String, String)) As String
            If parameters Is Nothing OrElse parameters.Count = 0 Then Return String.Empty
            Dim sb As New StringBuilder()
            Dim first As Boolean = True
            For Each kvp As KeyValuePair(Of String, String) In parameters
                If Not first Then sb.Append("&")
                sb.Append(UrlEncode(kvp.Key))
                sb.Append("=")
                If Not String.IsNullOrEmpty(kvp.Value) Then
                    sb.Append(UrlEncode(kvp.Value))
                End If
                first = False
            Next
            Return sb.ToString()
        End Function

        ''' <summary>
        ''' 构建完整 URL
        ''' </summary>
        ''' <param name="baseUrl">基础 URL</param>
        ''' <param name="parameters">查询参数</param>
        ''' <returns>完整 URL</returns>
        Public Shared Function BuildUrl(baseUrl As String, parameters As Dictionary(Of String, String)) As String
            If String.IsNullOrEmpty(baseUrl) Then Return String.Empty
            If parameters Is Nothing OrElse parameters.Count = 0 Then Return baseUrl
            Dim queryString As String = BuildQueryString(parameters)
            If String.IsNullOrEmpty(queryString) Then Return baseUrl
            Dim separator As String = If(baseUrl.Contains("?"), "&", "?")
            Return baseUrl & separator & queryString
        End Function

        ''' <summary>
        ''' 解析 URL
        ''' </summary>
        ''' <param name="url">URL 字符串</param>
        ''' <returns>包含 URL 各部分的字典</returns>
        Public Shared Function ParseUrl(url As String) As Dictionary(Of String, String)
            Dim result As New Dictionary(Of String, String)()
            If String.IsNullOrEmpty(url) Then Return result
            Try
                Dim uri As New Uri(url)
                result("scheme") = uri.Scheme
                result("host") = uri.Host
                result("port") = uri.Port.ToString()
                result("path") = uri.AbsolutePath
                result("query") = uri.Query
                result("fragment") = uri.Fragment
                result("userinfo") = uri.UserInfo
                result("authority") = uri.Authority
            Catch
                ' 解析失败返回空字典
            End Try
            Return result
        End Function

        ''' <summary>
        ''' 验证 URL 格式是否有效
        ''' </summary>
        ''' <param name="url">URL 字符串</param>
        ''' <returns>是否有效</returns>
        Public Shared Function IsValidUrl(url As String) As Boolean
            If String.IsNullOrEmpty(url) Then Return False
            Return Uri.IsWellFormedUriString(url, UriKind.Absolute)
        End Function

        ''' <summary>
        ''' 从 URL 中提取域名
        ''' </summary>
        ''' <param name="url">URL 字符串</param>
        ''' <returns>域名</returns>
        Public Shared Function GetDomain(url As String) As String
            If String.IsNullOrEmpty(url) Then Return String.Empty
            Try
                Dim uri As New Uri(url)
                Return uri.Host
            Catch
                Return String.Empty
            End Try
        End Function

        ''' <summary>
        ''' 从 URL 中提取路径
        ''' </summary>
        ''' <param name="url">URL 字符串</param>
        ''' <returns>路径</returns>
        Public Shared Function GetPath(url As String) As String
            If String.IsNullOrEmpty(url) Then Return String.Empty
            Try
                Dim uri As New Uri(url)
                Return uri.AbsolutePath
            Catch
                Return String.Empty
            End Try
        End Function

        ''' <summary>
        ''' 向 URL 添加查询参数
        ''' </summary>
        ''' <param name="url">原始 URL</param>
        ''' <param name="params">要添加的参数</param>
        ''' <returns>新的 URL</returns>
        Public Shared Function AddQueryParams(url As String, params As Dictionary(Of String, String)) As String
            Return BuildUrl(url, params)
        End Function

        ' ============================================================================
        ' 私有辅助方法
        ' ============================================================================

        ''' <summary>
        ''' 发送 HTTP 请求的核心方法
        ''' </summary>
        Private Shared Function SendRequest(url As String, method As String, body As String, contentType As String, options As HttpOptions) As HttpResponse
            Dim response As New HttpResponse()
            Dim stopwatch As New System.Diagnostics.Stopwatch()
            stopwatch.Start()

            If options Is Nothing Then
                options = New HttpOptions()
            End If

            Try
                ' 创建请求
                Dim request As HttpWebRequest = CType(WebRequest.Create(url), HttpWebRequest)
                request.Method = method
                request.Timeout = options.Timeout
                request.AllowAutoRedirect = options.AllowRedirect
                request.MaximumAutomaticRedirections = options.MaxRedirects

                ' SSL 验证设置
                If Not options.ValidateSsl Then
                    ServicePointManager.ServerCertificateValidationCallback = Function(s, cert, chain, sslPolicyErrors) True
                End If

                ' 代理设置
                If Not String.IsNullOrEmpty(options.Proxy) Then
                    request.Proxy = New WebProxy(options.Proxy)
                End If

                ' 基本认证
                If Not String.IsNullOrEmpty(options.Username) Then
                    Dim credentials As String = Convert.ToBase64String(Encoding.UTF8.GetBytes(options.Username & ":" & options.Password))
                    request.Headers.Add("Authorization", "Basic " & credentials)
                End If

                ' 设置请求头
                For Each kvp As KeyValuePair(Of String, String) In options.Headers
                    Try
                        request.Headers.Add(kvp.Key, kvp.Value)
                    Catch
                        ' 某些标准头需要特殊处理
                        If kvp.Key.Equals("Content-Type", StringComparison.OrdinalIgnoreCase) Then
                            request.ContentType = kvp.Value
                        End If
                    End Try
                Next

                ' 写入请求体
                If Not String.IsNullOrEmpty(body) Then
                    Dim bodyBytes As Byte() = Encoding.UTF8.GetBytes(body)
                    request.ContentLength = bodyBytes.Length
                    If Not String.IsNullOrEmpty(contentType) Then
                        request.ContentType = contentType
                    End If
                    Using stream As Stream = request.GetRequestStream()
                        stream.Write(bodyBytes, 0, bodyBytes.Length)
                    End Using
                End If

                ' 获取响应
                Using webResponse As HttpWebResponse = CType(request.GetResponse(), HttpWebResponse)
                    response.StatusCode = CInt(webResponse.StatusCode)
                    response.StatusDescription = webResponse.StatusDescription
                    response.Url = url
                    response.IsSuccess = response.StatusCode >= 200 AndAlso response.StatusCode < 300
                    response.ContentType = webResponse.ContentType

                    ' 读取响应头
                    For Each headerKey As String In webResponse.Headers.AllKeys
                        response.Headers(headerKey) = webResponse.Headers(headerKey)
                    Next

                    ' 读取响应体
                    Using stream As Stream = webResponse.GetResponseStream()
                        Using reader As New StreamReader(stream, Encoding.UTF8)
                            response.Body = reader.ReadToEnd()
                        End Using
                    End Using

                    ' 同时保存字节数据
                    response.BodyBytes = Encoding.UTF8.GetBytes(response.Body)
                End Using

            Catch ex As WebException
                ' 处理 HTTP 错误响应
                If ex.Response IsNot Nothing Then
                    Using webResponse As HttpWebResponse = CType(ex.Response, HttpWebResponse)
                        response.StatusCode = CInt(webResponse.StatusCode)
                        response.StatusDescription = webResponse.StatusDescription
                        response.Url = url
                        response.IsSuccess = False
                        response.ContentType = webResponse.ContentType

                        For Each headerKey As String In webResponse.Headers.AllKeys
                            response.Headers(headerKey) = webResponse.Headers(headerKey)
                        Next

                        Using stream As Stream = webResponse.GetResponseStream()
                            Using reader As New StreamReader(stream, Encoding.UTF8)
                                response.Body = reader.ReadToEnd()
                            End Using
                        End Using
                        response.BodyBytes = Encoding.UTF8.GetBytes(response.Body)
                    End Using
                Else
                    response.StatusCode = 0
                    response.StatusDescription = ex.Message
                    response.Url = url
                    response.IsSuccess = False
                    response.Body = ex.Message
                End If
            Catch ex As Exception
                response.StatusCode = 0
                response.StatusDescription = ex.Message
                response.Url = url
                response.IsSuccess = False
                response.Body = ex.Message
            End Try

            stopwatch.Stop()
            response.ResponseTime = stopwatch.ElapsedMilliseconds
            Return response
        End Function

    End Class

End Namespace
// =============================================================================
// AllToolkit - C# HTTP Utilities
// =============================================================================
// 一个零依赖的 HTTP 请求工具库，仅使用 .NET 标准库
// 支持 .NET 6.0+ / .NET Framework 4.5+ / .NET Standard 2.0+
// =============================================================================

using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Net.Http;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;

namespace AllToolkit.HttpUtils
{
    /// <summary>
    /// HTTP 响应结果封装类
    /// </summary>
    public class HttpResponse
    {
        /// <summary>HTTP 状态码</summary>
        public int StatusCode { get; set; }
        
        /// <summary>响应体内容</summary>
        public string Body { get; set; }
        
        /// <summary>响应头字典</summary>
        public Dictionary<string, string> Headers { get; set; }
        
        /// <summary>是否请求成功 (2xx 状态码)</summary>
        public bool IsSuccess => StatusCode >= 200 && StatusCode < 300;
        
        /// <summary>请求耗时（毫秒）</summary>
        public long ElapsedMs { get; set; }
        
        /// <summary>异常信息（如果发生）</summary>
        public string Error { get; set; }

        public HttpResponse()
        {
            Headers = new Dictionary<string, string>();
        }
    }

    /// <summary>
    /// HTTP 请求配置选项
    /// </summary>
    public class HttpOptions
    {
        /// <summary>连接超时（毫秒），默认 10000</summary>
        public int ConnectTimeoutMs { get; set; } = 10000;
        
        /// <summary>读取超时（毫秒），默认 30000</summary>
        public int ReadTimeoutMs { get; set; } = 30000;
        
        /// <summary>请求头字典</summary>
        public Dictionary<string, string> Headers { get; set; }
        
        /// <summary>是否跟随重定向，默认 true</summary>
        public bool FollowRedirects { get; set; } = true;
        
        /// <summary>User-Agent 字符串</summary>
        public string UserAgent { get; set; } = "AllToolkit-HttpUtils/1.0";
        
        /// <summary>是否验证 SSL 证书，默认 true</summary>
        public bool ValidateSsl { get; set; } = true;

        public HttpOptions()
        {
            Headers = new Dictionary<string, string>();
        }
    }

    /// <summary>
    /// HTTP 工具类 - 提供同步和异步 HTTP 请求方法
    /// </summary>
    public static class HttpUtils
    {
        // 静态 HttpClient 实例（推荐做法，避免端口耗尽）
        private static readonly HttpClient _client = new HttpClient();

        // ============================================================================
        // GET 请求
        // ============================================================================

        /// <summary>
        /// 发送同步 GET 请求
        /// </summary>
        /// <param name="url">请求 URL</param>
        /// <param name="options">请求选项（可选）</param>
        /// <returns>HTTP 响应对象</returns>
        public static HttpResponse Get(string url, HttpOptions options = null)
        {
            return GetAsync(url, options).GetAwaiter().GetResult();
        }

        /// <summary>
        /// 发送异步 GET 请求
        /// </summary>
        /// <param name="url">请求 URL</param>
        /// <param name="options">请求选项（可选）</param>
        /// <returns>HTTP 响应对象</returns>
        public static async Task<HttpResponse> GetAsync(string url, HttpOptions options = null)
        {
            return await SendRequestAsync(url, "GET", null, null, options);
        }

        // ============================================================================
        // POST 请求
        // ============================================================================

        /// <summary>
        /// 发送同步 POST 请求
        /// </summary>
        /// <param name="url">请求 URL</param>
        /// <param name="body">请求体内容</param>
        /// <param name="contentType">内容类型，默认 application/json</param>
        /// <param name="options">请求选项（可选）</param>
        /// <returns>HTTP 响应对象</returns>
        public static HttpResponse Post(string url, string body, string contentType = "application/json", HttpOptions options = null)
        {
            return PostAsync(url, body, contentType, options).GetAwaiter().GetResult();
        }

        /// <summary>
        /// 发送异步 POST 请求
        /// </summary>
        /// <param name="url">请求 URL</param>
        /// <param name="body">请求体内容</param>
        /// <param name="contentType">内容类型，默认 application/json</param>
        /// <param name="options">请求选项（可选）</param>
        /// <returns>HTTP 响应对象</returns>
        public static async Task<HttpResponse> PostAsync(string url, string body, string contentType = "application/json", HttpOptions options = null)
        {
            return await SendRequestAsync(url, "POST", body, contentType, options);
        }

        /// <summary>
        /// 发送同步 POST JSON 请求
        /// </summary>
        /// <param name="url">请求 URL</param>
        /// <param name="jsonData">JSON 对象（会被序列化为字符串）</param>
        /// <param name="options">请求选项（可选）</param>
        /// <returns>HTTP 响应对象</returns>
        public static HttpResponse PostJson(string url, object jsonData, HttpOptions options = null)
        {
            return PostJsonAsync(url, jsonData, options).GetAwaiter().GetResult();
        }

        /// <summary>
        /// 发送异步 POST JSON 请求
        /// </summary>
        /// <param name="url">请求 URL</param>
        /// <param name="jsonData">JSON 对象（会被序列化为字符串）</param>
        /// <param name="options">请求选项（可选）</param>
        /// <returns>HTTP 响应对象</returns>
        public static async Task<HttpResponse> PostJsonAsync(string url, object jsonData, HttpOptions options = null)
        {
            string jsonString = JsonSerializer.Serialize(jsonData);
            return await SendRequestAsync(url, "POST", jsonString, "application/json", options);
        }

        /// <summary>
        /// 发送同步 POST 表单请求
        /// </summary>
        /// <param name="url">请求 URL</param>
        /// <param name="formData">表单数据字典</param>
        /// <param name="options">请求选项（可选）</param>
        /// <returns>HTTP 响应对象</returns>
        public static HttpResponse PostForm(string url, Dictionary<string, string> formData, HttpOptions options = null)
        {
            return PostFormAsync(url, formData, options).GetAwaiter().GetResult();
        }

        /// <summary>
        /// 发送异步 POST 表单请求
        /// </summary>
        /// <param name="url">请求 URL</param>
        /// <param name="formData">表单数据字典</param>
        /// <param name="options">请求选项（可选）</param>
        /// <returns>HTTP 响应对象</returns>
        public static async Task<HttpResponse> PostFormAsync(string url, Dictionary<string, string> formData, HttpOptions options = null)
        {
            var content = new FormUrlEncodedContent(formData);
            return await SendRequestWithContentAsync(url, "POST", content, options);
        }

        // ============================================================================
        // PUT 请求
        // ============================================================================

        /// <summary>
        /// 发送同步 PUT 请求
        /// </summary>
        /// <param name="url">请求 URL</param>
        /// <param name="body">请求体内容</param>
        /// <param name="contentType">内容类型，默认 application/json</param>
        /// <param name="options">请求选项（可选）</param>
        /// <returns>HTTP 响应对象</returns>
        public static HttpResponse Put(string url, string body, string contentType = "application/json", HttpOptions options = null)
        {
            return PutAsync(url, body, contentType, options).GetAwaiter().GetResult();
        }

        /// <summary>
        /// 发送异步 PUT 请求
        /// </summary>
        /// <param name="url">请求 URL</param>
        /// <param name="body">请求体内容</param>
        /// <param name="contentType">内容类型，默认 application/json</param>
        /// <param name="options">请求选项（可选）</param>
        /// <returns>HTTP 响应对象</returns>
        public static async Task<HttpResponse> PutAsync(string url, string body, string contentType = "application/json", HttpOptions options = null)
        {
            return await SendRequestAsync(url, "PUT", body, contentType, options);
        }

        /// <summary>
        /// 发送同步 PUT JSON 请求
        /// </summary>
        /// <param name="url">请求 URL</param>
        /// <param name="jsonData">JSON 对象（会被序列化为字符串）</param>
        /// <param name="options">请求选项（可选）</param>
        /// <returns>HTTP 响应对象</returns>
        public static HttpResponse PutJson(string url, object jsonData, HttpOptions options = null)
        {
            return PutJsonAsync(url, jsonData, options).GetAwaiter().GetResult();
        }

        /// <summary>
        /// 发送异步 PUT JSON 请求
        /// </summary>
        /// <param name="url">请求 URL</param>
        /// <param name="jsonData">JSON 对象（会被序列化为字符串）</param>
        /// <param name="options">请求选项（可选）</param>
        /// <returns>HTTP 响应对象</returns>
        public static async Task<HttpResponse> PutJsonAsync(string url, object jsonData, HttpOptions options = null)
        {
            string jsonString = JsonSerializer.Serialize(jsonData);
            return await SendRequestAsync(url, "PUT", jsonString, "application/json", options);
        }

        // ============================================================================
        // DELETE 请求
        // ============================================================================

        /// <summary>
        /// 发送同步 DELETE 请求
        /// </summary>
        /// <param name="url">请求 URL</param>
        /// <param name="options">请求选项（可选）</param>
        /// <returns>HTTP 响应对象</returns>
        public static HttpResponse Delete(string url, HttpOptions options = null)
        {
            return DeleteAsync(url, options).GetAwaiter().GetResult();
        }

        /// <summary>
        /// 发送异步 DELETE 请求
        /// </summary>
        /// <param name="url">请求 URL</param>
        /// <param name="options">请求选项（可选）</param>
        /// <returns>HTTP 响应对象</returns>
        public static async Task<HttpResponse> DeleteAsync(string url, HttpOptions options = null)
        {
            return await SendRequestAsync(url, "DELETE", null, null, options);
        }

        // ============================================================================
        // PATCH 请求
        // ============================================================================

        /// <summary>
        /// 发送同步 PATCH 请求
        /// </summary>
        /// <param name="url">请求 URL</param>
        /// <param name="body">请求体内容</param>
        /// <param name="contentType">内容类型，默认 application/json</param>
        /// <param name="options">请求选项（可选）</param>
        /// <returns>HTTP 响应对象</returns>
        public static HttpResponse Patch(string url, string body, string contentType = "application/json", HttpOptions options = null)
        {
            return PatchAsync(url, body, contentType, options).GetAwaiter().GetResult();
        }

        /// <summary>
        /// 发送异步 PATCH 请求
        /// </summary>
        /// <param name="url">请求 URL</param>
        /// <param name="body">请求体内容</param>
        /// <param name="contentType">内容类型，默认 application/json</param>
        /// <param name="options">请求选项（可选）</param>
        /// <returns>HTTP 响应对象</returns>
        public static async Task<HttpResponse> PatchAsync(string url, string body, string contentType = "application/json", HttpOptions options = null)
        {
            return await SendRequestAsync(url, "PATCH", body, contentType, options);
        }

        // ============================================================================
        // URL 工具方法
        // ============================================================================

        /// <summary>
        /// URL 编码
        /// </summary>
        /// <param name="value">要编码的字符串</param>
        /// <returns>编码后的字符串</returns>
        public static string UrlEncode(string value)
        {
            if (string.IsNullOrEmpty(value)) return value;
            return Uri.EscapeDataString(value);
        }

        /// <summary>
        /// URL 解码
        /// </summary>
        /// <param name="value">要解码的字符串</param>
        /// <returns>解码后的字符串</returns>
        public static string UrlDecode(string value)
        {
            if (string.IsNullOrEmpty(value)) return value;
            return Uri.UnescapeDataString(value);
        }

        /// <summary>
        /// 构建查询字符串
        /// </summary>
        /// <param name="parameters">参数字典</param>
        /// <returns>查询字符串（如：key1=value1&amp;key2=value2）</returns>
        public static string BuildQueryString(Dictionary<string, string> parameters)
        {
            if (parameters == null || parameters.Count == 0) return "";
            
            var pairs = new List<string>();
            foreach (var kvp in parameters)
            {
                pairs.Add($"{UrlEncode(kvp.Key)}={UrlEncode(kvp.Value)}");
            }
            return string.Join("&", pairs);
        }

        /// <summary>
        /// 构建完整 URL（带查询参数）
        /// </summary>
        /// <param name="baseUrl">基础 URL</param>
        /// <param name="parameters">查询参数</param>
        /// <returns>完整 URL</returns>
        public static string BuildUrl(string baseUrl, Dictionary<string, string> parameters)
        {
            if (parameters == null || parameters.Count == 0) return baseUrl;
            
            string query = BuildQueryString(parameters);
            string separator = baseUrl.Contains("?") ? "&" : "?";
            return $"{baseUrl}{separator}{query}";
        }

        // ============================================================================
        // 内部实现方法
        // ============================================================================

        /// <summary>
        /// 发送 HTTP 请求（内部实现）
        /// </summary>
        private static async Task<HttpResponse> SendRequestAsync(string url, string method, string body, string contentType, HttpOptions options)
        {
            options = options ?? new HttpOptions();
            var stopwatch = Stopwatch.StartNew();
            var response = new HttpResponse();

            try
            {
                // 配置 HttpClient
                _client.Timeout = TimeSpan.FromMilliseconds(options.ReadTimeoutMs);
                _client.DefaultRequestHeaders.Clear();
                _client.DefaultRequestHeaders.Add("User-Agent", options.UserAgent);

                // 添加自定义请求头
                if (options.Headers != null)
                {
                    foreach (var header in options.Headers)
                    {
                        _client.DefaultRequestHeaders.TryAddWithoutValidation(header.Key, header.Value);
                    }
                }

                // 创建请求
                var request = new HttpRequestMessage(new HttpMethod(method), url);
                
                if (!string.IsNullOrEmpty(body))
                {
                    request.Content = new StringContent(body, Encoding.UTF8, contentType ?? "application/json");
                }

                // 发送请求
                var httpResponse = await _client.SendAsync(request);
                
                // 读取响应
                response.StatusCode = (int)httpResponse.StatusCode;
                response.Body = await httpResponse.Content.ReadAsStringAsync();
                
                // 提取响应头
                foreach (var header in httpResponse.Headers)
                {
                    response.Headers[header.Key] = string.Join(",", header.Value);
                }
                foreach (var header in httpResponse.Content.Headers)
                {
                    response.Headers[header.Key] = string.Join(",", header.Value);
                }
            }
            catch (TaskCanceledException)
            {
                response.StatusCode = 0;
                response.Error = "Request timeout";
            }
            catch (Exception ex)
            {
                response.StatusCode = 0;
                response.Error = ex.Message;
            }
            finally
            {
                stopwatch.Stop();
                response.ElapsedMs = stopwatch.ElapsedMilliseconds;
            }

            return response;
        }

        /// <summary>
        /// 发送带 HttpContent 的请求（用于表单提交）
        /// </summary>
        private static async Task<HttpResponse> SendRequestWithContentAsync(string url, string method, HttpContent content, HttpOptions options)
        {
            options = options ?? new HttpOptions();
            var stopwatch = Stopwatch.StartNew();
            var response = new HttpResponse();

            try
            {
                _client.Timeout = TimeSpan.FromMilliseconds(options.ReadTimeoutMs);
                _client.DefaultRequestHeaders.Clear();
                _client.DefaultRequestHeaders.Add("User-Agent", options.UserAgent);

                if (options.Headers != null)
                {
                    foreach (var header in options.Headers)
                    {
                        _client.DefaultRequestHeaders.TryAddWithoutValidation(header.Key, header.Value);
                    }
                }

                var request = new HttpRequestMessage(new HttpMethod(method), url)
                {
                    Content = content
                };

                var httpResponse = await _client.SendAsync(request);
                
                response.StatusCode = (int)httpResponse.StatusCode;
                response.Body = await httpResponse.Content.ReadAsStringAsync();
                
                foreach (var header in httpResponse.Headers)
                {
                    response.Headers[header.Key] = string.Join(",", header.Value);
                }
                foreach (var header in httpResponse.Content.Headers)
                {
                    response.Headers[header.Key] = string.Join(",", header.Value);
                }
            }
            catch (TaskCanceledException)
            {
                response.StatusCode = 0;
                response.Error = "Request timeout";
            }
            catch (Exception ex)
            {
                response.StatusCode = 0;
                response.Error = ex.Message;
            }
            finally
            {
                stopwatch.Stop();
                response.ElapsedMs = stopwatch.ElapsedMilliseconds;
            }

            return response;
        }
    }
}

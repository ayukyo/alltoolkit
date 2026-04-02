// =============================================================================
// AllToolkit - C# HTTP Utilities Example
// =============================================================================
// 使用示例代码
// 运行: dotnet run
// =============================================================================

using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using AllToolkit.HttpUtils;

namespace AllToolkit.Examples
{
    class HttpUtilsExample
    {
        static async Task Main(string[] args)
        {
            Console.WriteLine("========================================");
            Console.WriteLine("AllToolkit - C# HTTP Utilities Example");
            Console.WriteLine("========================================\n");

            // 示例 1: URL 编码和解码
            Console.WriteLine("【示例 1】URL 编码和解码");
            string originalText = "Hello World! 你好世界 @#$%";
            string encoded = HttpUtils.UrlEncode(originalText);
            string decoded = HttpUtils.UrlDecode(encoded);
            Console.WriteLine($"原始文本: {originalText}");
            Console.WriteLine($"编码后:   {encoded}");
            Console.WriteLine($"解码后:   {decoded}\n");

            // 示例 2: 构建查询字符串
            Console.WriteLine("【示例 2】构建查询字符串");
            var searchParams = new Dictionary<string, string>
            {
                { "q", "C# programming" },
                { "page", "1" },
                { "limit", "10" }
            };
            string queryString = HttpUtils.BuildQueryString(searchParams);
            Console.WriteLine($"查询参数: {queryString}\n");

            // 示例 3: 构建完整 URL
            Console.WriteLine("【示例 3】构建完整 URL");
            string baseUrl = "https://api.example.com/search";
            string fullUrl = HttpUtils.BuildUrl(baseUrl, searchParams);
            Console.WriteLine($"基础 URL: {baseUrl}");
            Console.WriteLine($"完整 URL: {fullUrl}\n");

            // 示例 4: 发送 GET 请求
            Console.WriteLine("【示例 4】发送 GET 请求");
            try
            {
                var getResponse = await HttpUtils.GetAsync("https://httpbin.org/get");
                Console.WriteLine($"状态码: {getResponse.StatusCode}");
                Console.WriteLine($"成功: {getResponse.IsSuccess}");
                Console.WriteLine($"耗时: {getResponse.ElapsedMs}ms\n");
            }
            catch (Exception ex)
            {
                Console.WriteLine($"请求异常: {ex.Message}\n");
            }

            // 示例 5: 发送 POST JSON 请求
            Console.WriteLine("【示例 5】发送 POST JSON 请求");
            try
            {
                var userData = new { name = "张三", email = "zhangsan@example.com", age = 28 };
                var postResponse = await HttpUtils.PostJsonAsync("https://httpbin.org/post", userData);
                Console.WriteLine($"状态码: {postResponse.StatusCode}");
                Console.WriteLine($"成功: {postResponse.IsSuccess}");
                Console.WriteLine($"耗时: {postResponse.ElapsedMs}ms\n");
            }
            catch (Exception ex)
            {
                Console.WriteLine($"请求异常: {ex.Message}\n");
            }

            // 示例 6: 发送 POST 表单请求
            Console.WriteLine("【示例 6】发送 POST 表单请求");
            try
            {
                var formData = new Dictionary<string, string>
                {
                    { "username", "admin" },
                    { "password", "secret123" }
                };
                var formResponse = await HttpUtils.PostFormAsync("https://httpbin.org/post", formData);
                Console.WriteLine($"状态码: {formResponse.StatusCode}");
                Console.WriteLine($"成功: {formResponse.IsSuccess}");
                Console.WriteLine($"耗时: {formResponse.ElapsedMs}ms\n");
            }
            catch (Exception ex)
            {
                Console.WriteLine($"请求异常: {ex.Message}\n");
            }

            // 示例 7: 使用自定义选项
            Console.WriteLine("【示例 7】使用自定义请求选项");
            try
            {
                var options = new HttpOptions
                {
                    ConnectTimeoutMs = 5000,
                    ReadTimeoutMs = 10000,
                    UserAgent = "MyApp/1.0",
                    Headers = new Dictionary<string, string>
                    {
                        { "Authorization", "Bearer token123" }
                    }
                };
                var customResponse = await HttpUtils.GetAsync("https://httpbin.org/headers", options);
                Console.WriteLine($"状态码: {customResponse.StatusCode}");
                Console.WriteLine($"成功: {customResponse.IsSuccess}");
                Console.WriteLine($"耗时: {customResponse.ElapsedMs}ms\n");
            }
            catch (Exception ex)
            {
                Console.WriteLine($"请求异常: {ex.Message}\n");
            }

            // 示例 8: 同步请求
            Console.WriteLine("【示例 8】同步 GET 请求");
            try
            {
                var syncResponse = HttpUtils.Get("https://httpbin.org/get");
                Console.WriteLine($"状态码: {syncResponse.StatusCode}");
                Console.WriteLine($"成功: {syncResponse.IsSuccess}");
                Console.WriteLine($"耗时: {syncResponse.ElapsedMs}ms\n");
            }
            catch (Exception ex)
            {
                Console.WriteLine($"请求异常: {ex.Message}\n");
            }

            Console.WriteLine("========================================");
            Console.WriteLine("示例运行完成！");
            Console.WriteLine("========================================");
        }
    }
}

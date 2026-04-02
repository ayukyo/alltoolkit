// =============================================================================
// AllToolkit - C# HTTP Utilities Tests
// =============================================================================
// 单元测试文件 - 使用 MSTest 框架
// =============================================================================

using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using Microsoft.VisualStudio.TestTools.UnitTesting;
using AllToolkit.HttpUtils;

namespace AllToolkit.HttpUtils.Tests
{
    [TestClass]
    public class HttpUtilsTests
    {
        // ============================================================================
        // URL 编码解码测试
        // ============================================================================

        [TestMethod]
        public void UrlEncode_NullOrEmpty_ReturnsSame()
        {
            Assert.IsNull(HttpUtils.UrlEncode(null));
            Assert.AreEqual("", HttpUtils.UrlEncode(""));
        }

        [TestMethod]
        public void UrlEncode_SpecialCharacters_Encoded()
        {
            string input = "hello world!@#$%";
            string encoded = HttpUtils.UrlEncode(input);
            Assert.AreEqual("hello%20world!%40%23%24%25", encoded);
        }

        [TestMethod]
        public void UrlEncode_Chinese_Encoded()
        {
            string input = "你好世界";
            string encoded = HttpUtils.UrlEncode(input);
            Assert.AreEqual("%E4%BD%A0%E5%A5%BD%E4%B8%96%E7%95%8C", encoded);
        }

        [TestMethod]
        public void UrlDecode_EncodedString_Decoded()
        {
            string encoded = "hello%20world";
            string decoded = HttpUtils.UrlDecode(encoded);
            Assert.AreEqual("hello world", decoded);
        }

        [TestMethod]
        public void UrlDecode_Chinese_Decoded()
        {
            string encoded = "%E4%BD%A0%E5%A5%BD%E4%B8%96%E7%95%8C";
            string decoded = HttpUtils.UrlDecode(encoded);
            Assert.AreEqual("你好世界", decoded);
        }

        // ============================================================================
        // 查询字符串构建测试
        // ============================================================================

        [TestMethod]
        public void BuildQueryString_EmptyDictionary_ReturnsEmpty()
        {
            var result = HttpUtils.BuildQueryString(new Dictionary<string, string>());
            Assert.AreEqual("", result);
        }

        [TestMethod]
        public void BuildQueryString_Null_ReturnsEmpty()
        {
            var result = HttpUtils.BuildQueryString(null);
            Assert.AreEqual("", result);
        }

        [TestMethod]
        public void BuildQueryString_SingleParam_ReturnsCorrect()
        {
            var dict = new Dictionary<string, string> { { "key", "value" } };
            var result = HttpUtils.BuildQueryString(dict);
            Assert.AreEqual("key=value", result);
        }

        [TestMethod]
        public void BuildQueryString_MultipleParams_ReturnsCorrect()
        {
            var dict = new Dictionary<string, string>
            {
                { "name", "John Doe" },
                { "age", "25" }
            };
            var result = HttpUtils.BuildQueryString(dict);
            Assert.IsTrue(result.Contains("name=John%20Doe"));
            Assert.IsTrue(result.Contains("age=25"));
        }

        // ============================================================================
        // URL 构建测试
        // ============================================================================

        [TestMethod]
        public void BuildUrl_NoParams_ReturnsBaseUrl()
        {
            var result = HttpUtils.BuildUrl("https://example.com/api", null);
            Assert.AreEqual("https://example.com/api", result);
        }

        [TestMethod]
        public void BuildUrl_WithParams_AddsQuestionMark()
        {
            var dict = new Dictionary<string, string> { { "key", "value" } };
            var result = HttpUtils.BuildUrl("https://example.com/api", dict);
            Assert.AreEqual("https://example.com/api?key=value", result);
        }

        [TestMethod]
        public void BuildUrl_ExistingQuery_AddsAmpersand()
        {
            var dict = new Dictionary<string, string> { { "key2", "value2" } };
            var result = HttpUtils.BuildUrl("https://example.com/api?key1=value1", dict);
            Assert.AreEqual("https://example.com/api?key1=value1&key2=value2", result);
        }

        // ============================================================================
        // HTTP 响应对象测试
        // ============================================================================

        [TestMethod]
        public void HttpResponse_IsSuccess_2xx_ReturnsTrue()
        {
            var response = new HttpResponse { StatusCode = 200 };
            Assert.IsTrue(response.IsSuccess);

            response.StatusCode = 201;
            Assert.IsTrue(response.IsSuccess);

            response.StatusCode = 204;
            Assert.IsTrue(response.IsSuccess);
        }

        [TestMethod]
        public void HttpResponse_IsSuccess_Non2xx_ReturnsFalse()
        {
            var response = new HttpResponse { StatusCode = 404 };
            Assert.IsFalse(response.IsSuccess);

            response.StatusCode = 500;
            Assert.IsFalse(response.IsSuccess);
        }

        [TestMethod]
        public void HttpResponse_DefaultHeaders_NotNull()
        {
            var response = new HttpResponse();
            Assert.IsNotNull(response.Headers);
        }

        // ============================================================================
        // HTTP 选项测试
        // ============================================================================

        [TestMethod]
        public void HttpOptions_DefaultValues_Set()
        {
            var options = new HttpOptions();
            Assert.AreEqual(10000, options.ConnectTimeoutMs);
            Assert.AreEqual(30000, options.ReadTimeoutMs);
            Assert.IsTrue(options.FollowRedirects);
            Assert.AreEqual("AllToolkit-HttpUtils/1.0", options.UserAgent);
            Assert.IsTrue(options.ValidateSsl);
        }

        [TestMethod]
        public void HttpOptions_DefaultHeaders_NotNull()
        {
            var options = new HttpOptions();
            Assert.IsNotNull(options.Headers);
        }
    }
}

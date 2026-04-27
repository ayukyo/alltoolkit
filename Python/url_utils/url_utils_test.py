"""
URL Utilities 测试套件
全面的单元测试覆盖所有功能
"""

import sys
import os
import unittest

# Add module directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mod import (
    URLParser, URLBuilder, URLEncoder, URLNormalizer, URLValidator, URLUtils,
    QueryStringParser,
    parse_url, build_url, encode_url, decode_url, normalize_url,
    validate_url, is_safe_url, clean_url, get_domain, get_query_params,
    set_query_param, remove_query_param, URLInfo
)


class TestURLParser(unittest.TestCase):
    """URLParser 测试"""
    
    def test_parse_basic_url(self):
        """测试基础 URL 解析"""
        url = "https://example.com/path"
        info = URLParser.parse(url)
        self.assertEqual(info.scheme, "https")
        self.assertEqual(info.hostname, "example.com")
        self.assertEqual(info.path, "/path")
    
    def test_parse_full_url(self):
        """测试完整 URL 解析"""
        url = "https://user:pass@example.com:8080/path?query=value#fragment"
        info = URLParser.parse(url)
        self.assertEqual(info.scheme, "https")
        self.assertEqual(info.hostname, "example.com")
        self.assertEqual(info.port, 8080)
        self.assertEqual(info.username, "user")
        self.assertEqual(info.password, "pass")
        self.assertEqual(info.path, "/path")
        self.assertEqual(info.query, "query=value")
        self.assertEqual(info.fragment, "fragment")
    
    def test_parse_ipv4(self):
        """测试 IPv4 地址"""
        url = "http://192.168.1.1:8080"
        info = URLParser.parse(url)
        self.assertEqual(info.hostname, "192.168.1.1")
        self.assertEqual(info.port, 8080)
    
    def test_parse_ipv6(self):
        """测试 IPv6 地址"""
        url = "http://[::1]:8080/path"
        info = URLParser.parse(url)
        self.assertEqual(info.hostname, "::1")
        self.assertEqual(info.port, 8080)
    
    def test_parse_no_path(self):
        """测试无路径 URL"""
        url = "https://example.com"
        info = URLParser.parse(url)
        self.assertEqual(info.hostname, "example.com")
        self.assertEqual(info.path, "")
    
    def test_is_valid_url_valid(self):
        """测试有效 URL"""
        valid_urls = [
            "https://example.com",
            "http://localhost:3000",
            "ftp://ftp.example.com/files",
            "https://user:pass@example.com:8080/path?q=1#frag"
        ]
        for url in valid_urls:
            self.assertTrue(URLParser.is_valid_url(url), f"Should be valid: {url}")
    
    def test_is_valid_url_invalid(self):
        """测试无效 URL"""
        invalid_urls = [
            "not a url",
            "://missing-scheme.com",
            "http://",
            "ftp://",  # 没有 netloc
        ]
        for url in invalid_urls:
            self.assertFalse(URLParser.is_valid_url(url), f"Should be invalid: {url}")
    
    def test_is_valid_scheme(self):
        """测试 scheme 验证"""
        self.assertTrue(URLParser.is_valid_scheme("https"))
        self.assertTrue(URLParser.is_valid_scheme("http"))
        self.assertTrue(URLParser.is_valid_scheme("ws+ssl"))
        self.assertFalse(URLParser.is_valid_scheme("123http"))
        self.assertFalse(URLParser.is_valid_scheme(""))
    
    def test_get_default_port(self):
        """测试默认端口"""
        self.assertEqual(URLParser.get_default_port("http"), 80)
        self.assertEqual(URLParser.get_default_port("https"), 443)
        self.assertEqual(URLParser.get_default_port("ftp"), 21)
        self.assertIsNone(URLParser.get_default_port("unknown"))
    
    def test_is_default_port(self):
        """测试默认端口检查"""
        self.assertTrue(URLParser.is_default_port("http", 80))
        self.assertTrue(URLParser.is_default_port("https", 443))
        self.assertFalse(URLParser.is_default_port("http", 8080))
    
    def test_urlinfo_to_dict(self):
        """测试 URLInfo 字典转换"""
        url = "https://user:pass@example.com:8080/path?q=1#frag"
        info = URLParser.parse(url)
        d = info.to_dict()
        self.assertEqual(d['scheme'], 'https')
        self.assertEqual(d['hostname'], 'example.com')
        self.assertEqual(d['port'], 8080)
        self.assertEqual(d['username'], 'user')
        self.assertEqual(d['password'], 'pass')


class TestURLBuilder(unittest.TestCase):
    """URLBuilder 测试"""
    
    def test_build_simple_url(self):
        """测试构建简单 URL"""
        url = (URLBuilder()
               .scheme("https")
               .host("example.com")
               .path("/api/users")
               .build())
        self.assertEqual(url, "https://example.com/api/users")
    
    def test_build_with_port(self):
        """测试构建带端口的 URL"""
        url = (URLBuilder()
               .scheme("http")
               .host("localhost")
               .port(8080)
               .path("/api")
               .build())
        self.assertEqual(url, "http://localhost:8080/api")
    
    def test_build_with_query(self):
        """测试构建带查询参数的 URL"""
        url = (URLBuilder()
               .scheme("https")
               .host("api.example.com")
               .path("/search")
               .query_param("q", "python")
               .query_param("page", "1")
               .build())
        self.assertIn("q=python", url)
        self.assertIn("page=1", url)
    
    def test_build_with_fragment(self):
        """测试构建带片段的 URL"""
        url = (URLBuilder()
               .scheme("https")
               .host("example.com")
               .path("/docs")
               .fragment("section")
               .build())
        self.assertEqual(url, "https://example.com/docs#section")
    
    def test_build_with_auth(self):
        """测试构建带认证的 URL"""
        url = (URLBuilder()
               .scheme("https")
               .host("api.example.com")
               .user("admin", "secret")
               .path("/api")
               .build())
        self.assertIn("admin:secret@", url)
    
    def test_build_from_base(self):
        """测试从基础 URL 构建"""
        builder = URLBuilder("https://example.com/path?existing=param")
        url = builder.query_param("new", "value").build()
        self.assertIn("existing=param", url)
        self.assertIn("new=value", url)
    
    def test_build_with_multiple_query_values(self):
        """测试多值查询参数"""
        url = (URLBuilder()
               .scheme("https")
               .host("example.com")
               .query_param("tag", ["python", "web", "api"])
               .build())
        self.assertIn("tag=python", url)
        self.assertIn("tag=web", url)
        self.assertIn("tag=api", url)
    
    def test_build_with_query_params_dict(self):
        """测试批量设置查询参数"""
        url = (URLBuilder()
               .scheme("https")
               .host("example.com")
               .query_params({"a": "1", "b": "2", "c": ["x", "y"]})
               .build())
        self.assertIn("a=1", url)
        self.assertIn("b=2", url)
        self.assertIn("c=x", url)


class TestURLEncoder(unittest.TestCase):
    """URLEncoder 测试"""
    
    def test_encode_basic(self):
        """测试基础编码"""
        self.assertEqual(encode_url("hello world"), "hello%20world")
        self.assertEqual(encode_url("a+b=c"), "a%2Bb%3Dc")
    
    def test_decode_basic(self):
        """测试基础解码"""
        self.assertEqual(decode_url("hello%20world"), "hello world")
        self.assertEqual(decode_url("a%2Bb%3Dc"), "a+b=c")
    
    def test_encode_decode_roundtrip(self):
        """测试编解码往返"""
        original = "hello world!@#$%^&*()"
        encoded = URLEncoder.encode(original)
        decoded = URLEncoder.decode(encoded)
        self.assertEqual(decoded, original)
    
    def test_encode_path(self):
        """测试路径编码"""
        path = "/path with spaces/file.txt"
        encoded = URLEncoder.encode_path(path)
        self.assertIn("/path%20with%20spaces", encoded)
        self.assertIn("/", encoded)  # 斜杠不应编码
    
    def test_encode_query(self):
        """测试查询参数编码"""
        value = "a=1&b=2"
        encoded = URLEncoder.encode_query(value)
        self.assertEqual(encoded, "a%3D1%26b%3D2")
    
    def test_encode_component(self):
        """测试组件编码"""
        self.assertEqual(
            URLEncoder.encode_component("hello world"),
            "hello%20world"
        )
    
    def test_decode_component(self):
        """测试组件解码"""
        self.assertEqual(
            URLEncoder.decode_component("hello%20world"),
            "hello world"
        )
    
    def test_unicode_encoding(self):
        """测试 Unicode 编码"""
        encoded = URLEncoder.encode("你好世界")
        decoded = URLEncoder.decode(encoded)
        self.assertEqual(decoded, "你好世界")


class TestQueryStringParser(unittest.TestCase):
    """QueryStringParser 测试"""
    
    def test_parse_simple(self):
        """测试简单查询字符串解析"""
        params = QueryStringParser.parse("a=1&b=2")
        self.assertEqual(params["a"], ["1"])
        self.assertEqual(params["b"], ["2"])
    
    def test_parse_multiple_values(self):
        """测试多值参数"""
        params = QueryStringParser.parse("tag=a&tag=b&tag=c")
        self.assertEqual(params["tag"], ["a", "b", "c"])
    
    def test_parse_to_list(self):
        """测试解析为列表"""
        params = QueryStringParser.parse_to_list("a=1&b=2&c=3")
        self.assertEqual(len(params), 3)
        self.assertIn(("a", "1"), params)
    
    def test_build(self):
        """测试构建查询字符串"""
        params = {"a": ["1"], "b": ["2"]}
        query = QueryStringParser.build(params)
        self.assertIn("a=1", query)
        self.assertIn("b=2", query)
    
    def test_get_param(self):
        """测试获取单个参数"""
        self.assertEqual(
            QueryStringParser.get_param("a=1&b=2", "a"),
            "1"
        )
        self.assertIsNone(QueryStringParser.get_param("a=1", "c"))
        self.assertEqual(
            QueryStringParser.get_param("a=1", "c", "default"),
            "default"
        )
    
    def test_get_params(self):
        """测试获取多值参数"""
        params = QueryStringParser.get_params("tag=a&tag=b&tag=c", "tag")
        self.assertEqual(params, ["a", "b", "c"])
    
    def test_set_param(self):
        """测试设置参数"""
        query = QueryStringParser.set_param("a=1", "b", "2")
        self.assertIn("a=1", query)
        self.assertIn("b=2", query)
    
    def test_remove_param(self):
        """测试移除参数"""
        query = QueryStringParser.remove_param("a=1&b=2&c=3", "b")
        self.assertIn("a=1", query)
        self.assertIn("c=3", query)
        self.assertNotIn("b=2", query)
    
    def test_has_param(self):
        """测试参数存在检查"""
        self.assertTrue(QueryStringParser.has_param("a=1&b=2", "a"))
        self.assertFalse(QueryStringParser.has_param("a=1&b=2", "c"))
    
    def test_empty_query(self):
        """测试空查询字符串"""
        params = QueryStringParser.parse("")
        self.assertEqual(params, {})


class TestURLNormalizer(unittest.TestCase):
    """URLNormalizer 测试"""
    
    def test_normalize_scheme(self):
        """测试 scheme 规范化"""
        url = "HTTPS://EXAMPLE.COM"
        normalized = URLNormalizer.normalize(url)
        self.assertTrue(normalized.startswith("https://example.com"))
    
    def test_normalize_default_port(self):
        """测试默认端口移除"""
        url = "https://example.com:443/path"
        normalized = URLNormalizer.normalize(url, remove_default_port=True)
        self.assertNotIn(":443", normalized)
    
    def test_normalize_keep_custom_port(self):
        """测试保留自定义端口"""
        url = "https://example.com:8443/path"
        normalized = URLNormalizer.normalize(url)
        self.assertIn(":8443", normalized)
    
    def test_normalize_remove_fragment(self):
        """测试移除片段"""
        url = "https://example.com/path#section"
        normalized = URLNormalizer.normalize(url, remove_fragment=True)
        self.assertNotIn("#section", normalized)
    
    def test_normalize_sort_query(self):
        """测试排序查询参数"""
        url = "https://example.com?b=2&a=1&c=3"
        normalized = URLNormalizer.normalize(url, sort_query=True)
        self.assertTrue(normalized.index("a=1") < normalized.index("b=2"))
        self.assertTrue(normalized.index("b=2") < normalized.index("c=3"))
    
    def test_normalize_path(self):
        """测试路径规范化"""
        url = "https://example.com//path///to//page"
        normalized = URLNormalizer.normalize(url)
        self.assertIn("/path/to/page", normalized)
    
    def test_canonical(self):
        """测试规范化 URL"""
        url = "HTTPS://Example.COM:443/Path/?b=2&a=1&utm_source=google#section"
        canonical = URLNormalizer.canonical(url)
        self.assertTrue(canonical.startswith("https://example.com"))
        self.assertIn("a=1", canonical)
        self.assertIn("b=2", canonical)
        self.assertNotIn(":443", canonical)
        self.assertNotIn("#section", canonical)
        self.assertNotIn("utm_source", canonical)
    
    def test_resolve_relative(self):
        """测试相对 URL 解析"""
        base = "https://example.com/path/page.html"
        self.assertEqual(
            URLNormalizer.resolve(base, "other.html"),
            "https://example.com/path/other.html"
        )
        self.assertEqual(
            URLNormalizer.resolve(base, "/absolute"),
            "https://example.com/absolute"
        )
        self.assertEqual(
            URLNormalizer.resolve(base, "https://other.com"),
            "https://other.com"
        )
    
    def test_remove_tracking_params(self):
        """测试移除追踪参数"""
        url = "https://example.com/page?utm_source=google&utm_medium=cpc&id=123&fbclid=xyz"
        clean = URLNormalizer.remove_tracking_params(url)
        self.assertNotIn("utm_source", clean)
        self.assertNotIn("utm_medium", clean)
        self.assertNotIn("fbclid", clean)
        self.assertIn("id=123", clean)


class TestURLValidator(unittest.TestCase):
    """URLValidator 测试"""
    
    def test_validate_valid_urls(self):
        """测试有效 URL 验证"""
        urls = [
            "https://example.com",
            "http://localhost:3000",
            "ftp://ftp.example.com/files",
            "https://user:pass@example.com:8080/path"
        ]
        for url in urls:
            valid, errors = URLValidator.validate(url)
            self.assertTrue(valid, f"Should be valid: {url}, errors: {errors}")
    
    def test_validate_invalid_urls(self):
        """测试无效 URL 验证"""
        urls = [
            "not a url",
            "://missing-scheme.com",
            "http://",
            "ftp://",
        ]
        for url in urls:
            valid, errors = URLValidator.validate(url)
            self.assertFalse(valid, f"Should be invalid: {url}")
            self.assertTrue(len(errors) > 0)
    
    def test_validate_dangerous_scheme(self):
        """测试危险 scheme"""
        valid, errors = URLValidator.validate("javascript:alert('xss')")
        self.assertFalse(valid)
        self.assertTrue(any("dangerous" in e.lower() or "javascript" in e.lower() for e in errors))
    
    def test_validate_invalid_port(self):
        """测试无效端口"""
        valid, errors = URLValidator.validate("http://example.com:99999")
        self.assertFalse(valid)
        self.assertTrue(any("port" in e.lower() for e in errors))
    
    def test_is_safe_url(self):
        """测试安全 URL 检查"""
        self.assertTrue(URLValidator.is_safe_url("https://example.com"))
        self.assertFalse(URLValidator.is_safe_url("javascript:alert(1)"))
        self.assertFalse(URLValidator.is_safe_url("https://user:pass@example.com"))
    
    def test_is_safe_url_private_ip(self):
        """测试私有 IP 检查"""
        self.assertFalse(URLValidator.is_safe_url("http://192.168.1.1"))
        self.assertFalse(URLValidator.is_safe_url("http://10.0.0.1"))
        self.assertFalse(URLValidator.is_safe_url("http://127.0.0.1"))
        
        # 允许私有 IP
        self.assertTrue(URLValidator.is_safe_url("http://192.168.1.1", allow_private_ip=True))
    
    def test_is_same_origin(self):
        """测试同源检查"""
        self.assertTrue(URLValidator.is_same_origin(
            "https://example.com/a",
            "https://example.com/b"
        ))
        self.assertFalse(URLValidator.is_same_origin(
            "https://example.com",
            "https://other.com"
        ))
        self.assertFalse(URLValidator.is_same_origin(
            "https://example.com",
            "http://example.com"  # 不同协议
        ))
    
    def test_is_valid_hostname(self):
        """测试主机名验证"""
        self.assertTrue(URLValidator._is_valid_hostname("example.com"))
        self.assertTrue(URLValidator._is_valid_hostname("sub.example.com"))
        self.assertTrue(URLValidator._is_valid_hostname("a-b.c-d.com"))
        self.assertFalse(URLValidator._is_valid_hostname(""))
        self.assertFalse(URLValidator._is_valid_hostname("-invalid.com"))
        self.assertFalse(URLValidator._is_valid_hostname("a" * 64 + ".com"))  # 标签太长


class TestURLUtils(unittest.TestCase):
    """URLUtils 测试"""
    
    def test_extract_domain(self):
        """测试提取域名"""
        self.assertEqual(
            URLUtils.extract_domain("https://www.example.com/path"),
            "www.example.com"
        )
        self.assertEqual(
            URLUtils.extract_domain("https://user@example.com"),
            "example.com"
        )
    
    def test_extract_root_domain(self):
        """测试提取根域名"""
        self.assertEqual(
            URLUtils.extract_root_domain("https://www.blog.example.com/path"),
            "example.com"
        )
        self.assertEqual(
            URLUtils.extract_root_domain("https://example.co.uk/path"),
            "example.co.uk"
        )
    
    def test_extract_tld(self):
        """测试提取顶级域名"""
        self.assertEqual(URLUtils.extract_tld("https://example.com"), "com")
        self.assertEqual(URLUtils.extract_tld("https://example.co.uk"), "uk")
        self.assertIsNone(URLUtils.extract_tld("http://192.168.1.1"))
    
    def test_extract_path(self):
        """测试提取路径"""
        self.assertEqual(
            URLUtils.extract_path("https://example.com/path/to/page"),
            "/path/to/page"
        )
        self.assertEqual(URLUtils.extract_path("https://example.com"), "")
    
    def test_extract_filename(self):
        """测试提取文件名"""
        self.assertEqual(
            URLUtils.extract_filename("https://example.com/path/file.html"),
            "file.html"
        )
        self.assertIsNone(URLUtils.extract_filename("https://example.com/path/"))
    
    def test_extract_extension(self):
        """测试提取扩展名"""
        self.assertEqual(
            URLUtils.extract_extension("https://example.com/file.tar.gz"),
            "gz"
        )
        self.assertEqual(
            URLUtils.extract_extension("https://example.com/image.PNG"),
            "png"
        )
        self.assertIsNone(URLUtils.extract_extension("https://example.com/path/"))
    
    def test_change_scheme(self):
        """测试更改 scheme"""
        self.assertEqual(
            URLUtils.change_scheme("http://example.com", "https"),
            "https://example.com"
        )
        self.assertEqual(
            URLUtils.change_scheme("https://example.com:443/path", "http"),
            "http://example.com:443/path"
        )
    
    def test_ensure_scheme(self):
        """测试确保 scheme"""
        self.assertEqual(
            URLUtils.ensure_scheme("example.com/path"),
            "https://example.com/path"
        )
        self.assertEqual(
            URLUtils.ensure_scheme("example.com/path", "http"),
            "http://example.com/path"
        )
        self.assertEqual(
            URLUtils.ensure_scheme("https://example.com"),
            "https://example.com"
        )
    
    def test_is_absolute_relative(self):
        """测试绝对/相对 URL 检查"""
        self.assertTrue(URLUtils.is_absolute("https://example.com"))
        self.assertTrue(URLUtils.is_absolute("http://localhost"))
        self.assertFalse(URLUtils.is_absolute("/path/to/page"))
        self.assertFalse(URLUtils.is_relative("https://example.com"))
        self.assertTrue(URLUtils.is_relative("/path/to/page"))
    
    def test_join(self):
        """测试 URL 连接"""
        self.assertEqual(
            URLUtils.join("https://example.com/path/", "page.html"),
            "https://example.com/path/page.html"
        )
        self.assertEqual(
            URLUtils.join("https://example.com/path/page.html", "/other"),
            "https://example.com/other"
        )
    
    def test_get_base_url(self):
        """测试获取基础 URL"""
        self.assertEqual(
            URLUtils.get_base_url("https://example.com:8080/path?q=1#frag"),
            "https://example.com:8080"
        )
    
    def test_split_url(self):
        """测试分割 URL"""
        url = "https://example.com/path?q=1#frag"
        scheme, netloc, path, query, fragment = URLUtils.split_url(url)
        self.assertEqual(scheme, "https")
        self.assertEqual(netloc, "example.com")
        self.assertEqual(path, "/path")
        self.assertEqual(query, "q=1")
        self.assertEqual(fragment, "frag")
    
    def test_unsplit(self):
        """测试从部分构建 URL"""
        parts = ("https", "example.com", "/path", "q=1", "frag")
        url = URLUtils.unsplit(parts)
        self.assertEqual(url, "https://example.com/path?q=1#frag")
    
    def test_get_url_depth(self):
        """测试 URL 深度"""
        self.assertEqual(URLUtils.get_url_depth("https://example.com"), 0)
        self.assertEqual(URLUtils.get_url_depth("https://example.com/"), 0)
        self.assertEqual(URLUtils.get_url_depth("https://example.com/a"), 1)
        self.assertEqual(URLUtils.get_url_depth("https://example.com/a/b/c"), 3)
    
    def test_is_subdomain(self):
        """测试子域名检查"""
        self.assertTrue(URLUtils.is_subdomain("https://blog.example.com", "example.com"))
        self.assertTrue(URLUtils.is_subdomain("https://example.com", "example.com"))
        self.assertFalse(URLUtils.is_subdomain("https://other.com", "example.com"))
    
    def test_batch_resolve(self):
        """测试批量解析"""
        base = "https://example.com/path/"
        urls = ["page1.html", "page2.html", "/absolute"]
        result = URLUtils.batch_resolve(urls, base)
        self.assertEqual(result["page1.html"], "https://example.com/path/page1.html")
        self.assertEqual(result["page2.html"], "https://example.com/path/page2.html")
        self.assertEqual(result["/absolute"], "https://example.com/absolute")


class TestConvenienceFunctions(unittest.TestCase):
    """便捷函数测试"""
    
    def test_parse_url(self):
        """测试 parse_url 函数"""
        info = parse_url("https://example.com:8080/path")
        self.assertEqual(info.scheme, "https")
        self.assertEqual(info.hostname, "example.com")
        self.assertEqual(info.port, 8080)
    
    def test_build_url(self):
        """测试 build_url 函数"""
        builder = build_url("https://example.com")
        self.assertIsInstance(builder, URLBuilder)
    
    def test_encode_decode_url(self):
        """测试 encode_url 和 decode_url"""
        original = "hello world"
        encoded = encode_url(original)
        decoded = decode_url(encoded)
        self.assertEqual(decoded, original)
    
    def test_normalize_url(self):
        """测试 normalize_url 函数"""
        url = "HTTPS://EXAMPLE.COM/path"
        normalized = normalize_url(url)
        self.assertTrue(normalized.startswith("https://example.com"))
    
    def test_validate_url(self):
        """测试 validate_url 函数"""
        valid, errors = validate_url("https://example.com")
        self.assertTrue(valid)
        valid, errors = validate_url("not a url")
        self.assertFalse(valid)
    
    def test_is_safe_url(self):
        """测试 is_safe_url 函数"""
        self.assertTrue(is_safe_url("https://example.com"))
        self.assertFalse(is_safe_url("javascript:alert(1)"))
    
    def test_clean_url(self):
        """测试 clean_url 函数"""
        url = "https://example.com?utm_source=google&id=123"
        clean = clean_url(url)
        self.assertNotIn("utm_source", clean)
        self.assertIn("id=123", clean)
    
    def test_get_domain(self):
        """测试 get_domain 函数"""
        self.assertEqual(get_domain("https://www.example.com/path"), "www.example.com")
    
    def test_get_query_params(self):
        """测试 get_query_params 函数"""
        params = get_query_params("https://example.com?a=1&b=2")
        self.assertEqual(params["a"], ["1"])
        self.assertEqual(params["b"], ["2"])
    
    def test_set_query_param(self):
        """测试 set_query_param 函数"""
        url = set_query_param("https://example.com?a=1", "b", "2")
        self.assertIn("a=1", url)
        self.assertIn("b=2", url)
    
    def test_remove_query_param(self):
        """测试 remove_query_param 函数"""
        url = remove_query_param("https://example.com?a=1&b=2", "a")
        self.assertNotIn("a=1", url)
        self.assertIn("b=2", url)


if __name__ == "__main__":
    # 运行测试
    unittest.main(verbosity=2)
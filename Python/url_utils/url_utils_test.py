"""
Test suite for URL Utilities.

Run with: python url_utils_test.py
Or with pytest: pytest url_utils_test.py -v
"""

import unittest
from url_utils import (
    parse_url, parse_query_string, parse_query_string_flat,
    build_url, build_query_string,
    join_url, resolve_url, normalize_url,
    get_url_path_segments, get_file_extension,
    add_query_param, set_query_param, remove_query_param,
    get_query_param, get_query_params,
    is_valid_domain, extract_domain, extract_root_domain, extract_subdomain,
    is_safe_url, is_absolute_url, is_same_origin, validate_url,
    encode_url_component, decode_url_component, encode_path, encode_query_value,
    is_ip_url, get_ip_version, is_localhost_url, is_private_url,
    parse_data_url, urls_equal,
    URLInfo,
)


class TestURLParsing(unittest.TestCase):
    """Tests for URL parsing functions."""
    
    def test_parse_full_url(self):
        """Test parsing a complete URL with all components."""
        url = "https://user:pass@example.com:8080/path/to/resource?q=hello&r=world#section"
        info = parse_url(url)
        
        self.assertEqual(info.scheme, "https")
        self.assertEqual(info.username, "user")
        self.assertEqual(info.password, "pass")
        self.assertEqual(info.host, "example.com")
        self.assertEqual(info.port, 8080)
        self.assertEqual(info.path, "/path/to/resource")
        self.assertEqual(info.query, {"q": ["hello"], "r": ["world"]})
        self.assertEqual(info.fragment, "section")
    
    def test_parse_minimal_url(self):
        """Test parsing a minimal URL."""
        info = parse_url("https://example.com")
        
        self.assertEqual(info.scheme, "https")
        self.assertEqual(info.host, "example.com")
        self.assertIsNone(info.port)
        self.assertEqual(info.path, "")
        self.assertEqual(info.query, {})
        self.assertEqual(info.fragment, "")
    
    def test_parse_url_no_scheme(self):
        """Test parsing URL without scheme."""
        info = parse_url("//example.com/path")
        
        self.assertEqual(info.scheme, "")
        self.assertEqual(info.host, "example.com")
    
    def test_parse_query_string(self):
        """Test query string parsing."""
        query = parse_query_string("?a=1&b=2&a=3")
        
        self.assertEqual(query, {"a": ["1", "3"], "b": ["2"]})
    
    def test_parse_query_string_flat(self):
        """Test flat query string parsing."""
        query = parse_query_string_flat("a=1&b=2&a=3")
        
        self.assertEqual(query, {"a": "3", "b": "2"})
    
    def test_parse_empty_query_string(self):
        """Test parsing empty query string."""
        self.assertEqual(parse_query_string(""), {})
        self.assertEqual(parse_query_string("?"), {})
    
    def test_url_info_properties(self):
        """Test URLInfo properties."""
        info = parse_url("https://example.com:8443/path")
        
        self.assertEqual(info.netloc, "example.com:8443")
        self.assertEqual(info.origin, "https://example.com:8443")
        self.assertTrue(info.is_secure)
        
        info = parse_url("http://example.com")
        self.assertFalse(info.is_secure)
        self.assertEqual(info.origin, "http://example.com")


class TestURLBuilding(unittest.TestCase):
    """Tests for URL building functions."""
    
    def test_build_simple_url(self):
        """Test building a simple URL."""
        url = build_url(scheme="https", host="example.com", path="/path")
        
        self.assertEqual(url, "https://example.com/path")
    
    def test_build_url_with_port(self):
        """Test building URL with port."""
        url = build_url(scheme="https", host="example.com", port=8080)
        
        self.assertEqual(url, "https://example.com:8080")
    
    def test_build_url_default_port_omitted(self):
        """Test that default ports are omitted."""
        url1 = build_url(scheme="http", host="example.com", port=80)
        url2 = build_url(scheme="https", host="example.com", port=443)
        
        self.assertEqual(url1, "http://example.com")
        self.assertEqual(url2, "https://example.com")
    
    def test_build_url_with_auth(self):
        """Test building URL with authentication."""
        url = build_url(
            scheme="https",
            host="example.com",
            username="user",
            password="pass"
        )
        
        self.assertEqual(url, "https://user:pass@example.com")
    
    def test_build_url_with_query(self):
        """Test building URL with query parameters."""
        url = build_url(
            scheme="https",
            host="example.com",
            query={"a": "1", "b": "2"}
        )
        
        # Order may vary
        self.assertIn("a=1", url)
        self.assertIn("b=2", url)
        self.assertIn("?", url)
    
    def test_build_url_with_fragment(self):
        """Test building URL with fragment."""
        url = build_url(
            scheme="https",
            host="example.com",
            fragment="section"
        )
        
        self.assertEqual(url, "https://example.com#section")
    
    def test_build_query_string_dict(self):
        """Test building query string from dict."""
        qs = build_query_string({"a": "1", "b": "2"})
        
        # Order may vary
        self.assertIn("a=1", qs)
        self.assertIn("b=2", qs)
    
    def test_build_query_string_list(self):
        """Test building query string from list."""
        qs = build_query_string([("a", "1"), ("a", "2")])
        
        self.assertEqual(qs, "a=1&a=2")
    
    def test_build_query_string_sort(self):
        """Test building query string with sorted keys."""
        qs = build_query_string({"b": "2", "a": "1"}, sort_keys=True)
        
        self.assertEqual(qs, "a=1&b=2")


class TestURLManipulation(unittest.TestCase):
    """Tests for URL manipulation functions."""
    
    def test_join_url_relative_path(self):
        """Test joining relative path."""
        # Note: urljoin replaces the last segment if base doesn't end with /
        url = join_url("https://example.com/api/", "users/1")
        
        self.assertEqual(url, "https://example.com/api/users/1")
    
    def test_join_url_absolute_path(self):
        """Test joining absolute path."""
        url = join_url("https://example.com/api/", "/users/1")
        
        self.assertEqual(url, "https://example.com/users/1")
    
    def test_resolve_url(self):
        """Test URL resolution."""
        url = resolve_url("../page.html", "https://example.com/docs/index.html")
        
        self.assertEqual(url, "https://example.com/page.html")
    
    def test_normalize_url_lowercase(self):
        """Test URL normalization - lowercase."""
        url = normalize_url("HTTPS://EXAMPLE.COM/Path")
        
        self.assertEqual(url, "https://example.com/Path")
    
    def test_normalize_url_default_port(self):
        """Test URL normalization - default port removal."""
        url = normalize_url("https://example.com:443/path")
        
        self.assertEqual(url, "https://example.com/path")
    
    def test_normalize_url_sort_query(self):
        """Test URL normalization - sorted query."""
        url = normalize_url("https://example.com?b=2&a=1")
        
        # Normalization adds a / before query if path is empty
        self.assertEqual(url, "https://example.com/?a=1&b=2")
    
    def test_normalize_url_remove_fragment(self):
        """Test URL normalization - remove fragment."""
        url = normalize_url("https://example.com/path#section", remove_fragment=True)
        
        self.assertEqual(url, "https://example.com/path")
    
    def test_get_url_path_segments(self):
        """Test getting path segments."""
        segments = get_url_path_segments("https://example.com/api/v1/users/123")
        
        self.assertEqual(segments, ["api", "v1", "users", "123"])
    
    def test_get_url_path_segments_empty(self):
        """Test getting path segments from root URL."""
        segments = get_url_path_segments("https://example.com/")
        
        self.assertEqual(segments, [])
    
    def test_get_file_extension(self):
        """Test getting file extension."""
        self.assertEqual(get_file_extension("https://example.com/image.png"), "png")
        self.assertEqual(get_file_extension("https://example.com/doc.pdf?q=1"), "pdf")
        self.assertEqual(get_file_extension("https://example.com/page"), "")


class TestQueryParameters(unittest.TestCase):
    """Tests for query parameter operations."""
    
    def test_add_query_param(self):
        """Test adding query parameter."""
        url = add_query_param("https://example.com?a=1", "b", "2")
        
        self.assertIn("a=1", url)
        self.assertIn("b=2", url)
    
    def test_add_query_param_duplicate(self):
        """Test adding duplicate query parameter."""
        url = add_query_param("https://example.com?a=1", "a", "2")
        
        self.assertIn("a=1", url)
        self.assertIn("a=2", url)
    
    def test_set_query_param(self):
        """Test setting query parameter."""
        url = set_query_param("https://example.com?a=1&a=2", "a", "3")
        
        # Should have only one value
        self.assertEqual(url.count("a="), 1)
        self.assertIn("a=3", url)
    
    def test_remove_query_param(self):
        """Test removing query parameter."""
        url = remove_query_param("https://example.com?a=1&b=2", "a")
        
        self.assertNotIn("a=1", url)
        self.assertIn("b=2", url)
    
    def test_get_query_param(self):
        """Test getting query parameter."""
        value = get_query_param("https://example.com?a=1&a=2", "a")
        
        self.assertEqual(value, "2")  # Last value
    
    def test_get_query_param_default(self):
        """Test getting query parameter with default."""
        value = get_query_param("https://example.com", "missing", "default")
        
        self.assertEqual(value, "default")
    
    def test_get_query_params(self):
        """Test getting all query parameter values."""
        values = get_query_params("https://example.com?a=1&a=2&a=3", "a")
        
        self.assertEqual(values, ["1", "2", "3"])


class TestDomainUtilities(unittest.TestCase):
    """Tests for domain utility functions."""
    
    def test_is_valid_domain(self):
        """Test domain validation."""
        self.assertTrue(is_valid_domain("example.com"))
        self.assertTrue(is_valid_domain("sub.example.com"))
        self.assertTrue(is_valid_domain("a-b.c-d.com"))
        self.assertFalse(is_valid_domain(""))
        self.assertFalse(is_valid_domain("-invalid.com"))
        self.assertFalse(is_valid_domain("invalid-.com"))
    
    def test_extract_domain(self):
        """Test domain extraction."""
        self.assertEqual(extract_domain("https://example.com/path"), "example.com")
        self.assertEqual(extract_domain("https://user:pass@sub.example.com:8080"), "sub.example.com")
    
    def test_extract_root_domain(self):
        """Test root domain extraction."""
        self.assertEqual(extract_root_domain("https://www.example.com"), "example.com")
        self.assertEqual(extract_root_domain("https://api.v1.example.co.uk"), "example.co.uk")
        self.assertEqual(extract_root_domain("https://sub.example.com"), "example.com")
    
    def test_extract_subdomain(self):
        """Test subdomain extraction."""
        self.assertEqual(extract_subdomain("https://www.example.com"), "www")
        self.assertEqual(extract_subdomain("https://api.v1.example.com"), "api.v1")
        self.assertIsNone(extract_subdomain("https://example.com"))
    
    def test_extract_root_domain_ip(self):
        """Test root domain extraction with IP address."""
        self.assertEqual(extract_root_domain("https://192.168.1.1"), "192.168.1.1")


class TestURLSafety(unittest.TestCase):
    """Tests for URL safety functions."""
    
    def test_is_safe_url(self):
        """Test URL safety check."""
        self.assertTrue(is_safe_url("https://example.com"))
        self.assertTrue(is_safe_url("http://example.com"))
        self.assertFalse(is_safe_url("javascript:alert(1)"))
        self.assertFalse(is_safe_url("vbscript:msgbox(1)"))
    
    def test_is_safe_url_relative(self):
        """Test relative URL safety."""
        self.assertFalse(is_safe_url("/relative/path"))
        self.assertTrue(is_safe_url("/relative/path", allow_relative=True))
    
    def test_is_absolute_url(self):
        """Test absolute URL check."""
        self.assertTrue(is_absolute_url("https://example.com"))
        self.assertTrue(is_absolute_url("//example.com"))
        self.assertFalse(is_absolute_url("/relative/path"))
        self.assertFalse(is_absolute_url("relative/path"))
    
    def test_is_same_origin(self):
        """Test same origin check."""
        self.assertTrue(is_same_origin(
            "https://example.com/a",
            "https://example.com/b"
        ))
        self.assertFalse(is_same_origin(
            "https://example.com",
            "https://other.com"
        ))
        self.assertFalse(is_same_origin(
            "https://example.com",
            "http://example.com"
        ))
    
    def test_validate_url(self):
        """Test URL validation."""
        valid, error = validate_url("https://example.com")
        self.assertTrue(valid)
        self.assertIsNone(error)
        
        valid, error = validate_url("")
        self.assertFalse(valid)
        self.assertIn("empty", error.lower())
        
        valid, error = validate_url("https://")
        self.assertFalse(valid)
        self.assertIn("host", error.lower())


class TestURLEncoding(unittest.TestCase):
    """Tests for URL encoding functions."""
    
    def test_encode_url_component(self):
        """Test URL component encoding."""
        self.assertEqual(encode_url_component("hello world"), "hello%20world")
        self.assertEqual(encode_url_component("a=1&b=2"), "a%3D1%26b%3D2")
    
    def test_decode_url_component(self):
        """Test URL component decoding."""
        self.assertEqual(decode_url_component("hello%20world"), "hello world")
        self.assertEqual(decode_url_component("a%3D1%26b%3D2"), "a=1&b=2")
    
    def test_encode_path(self):
        """Test path encoding."""
        self.assertEqual(encode_path("/path/file name.txt"), "/path/file%20name.txt")
        self.assertEqual(encode_path("/a/b/c"), "/a/b/c")  # Slashes preserved
    
    def test_encode_query_value(self):
        """Test query value encoding."""
        self.assertEqual(encode_query_value("a=1&b=2"), "a%3D1%26b%3D2")
    
    def test_roundtrip_encoding(self):
        """Test encoding/decoding roundtrip."""
        original = "hello world!@#$%^&*()"
        encoded = encode_url_component(original)
        decoded = decode_url_component(encoded)
        
        self.assertEqual(decoded, original)


class TestSpecialURLs(unittest.TestCase):
    """Tests for special URL handling."""
    
    def test_is_ip_url(self):
        """Test IP URL detection."""
        self.assertTrue(is_ip_url("https://192.168.1.1"))
        self.assertTrue(is_ip_url("https://[::1]"))
        self.assertFalse(is_ip_url("https://example.com"))
    
    def test_get_ip_version(self):
        """Test IP version detection."""
        self.assertEqual(get_ip_version("https://192.168.1.1"), 4)
        self.assertEqual(get_ip_version("https://[::1]"), 6)
        self.assertIsNone(get_ip_version("https://example.com"))
    
    def test_is_localhost_url(self):
        """Test localhost URL detection."""
        self.assertTrue(is_localhost_url("https://localhost"))
        self.assertTrue(is_localhost_url("https://127.0.0.1"))
        self.assertTrue(is_localhost_url("https://[::1]"))
        self.assertFalse(is_localhost_url("https://example.com"))
    
    def test_is_private_url(self):
        """Test private URL detection."""
        self.assertTrue(is_private_url("https://192.168.1.1"))
        self.assertTrue(is_private_url("https://10.0.0.1"))
        self.assertTrue(is_private_url("https://example.local"))
        self.assertFalse(is_private_url("https://example.com"))
    
    def test_parse_data_url(self):
        """Test data URL parsing."""
        result = parse_data_url("data:text/plain;base64,SGVsbG8gV29ybGQ=")
        
        self.assertEqual(result["media_type"], "text/plain")
        self.assertEqual(result["encoding"], "base64")
        self.assertEqual(result["data"], "SGVsbG8gV29ybGQ=")
    
    def test_parse_data_url_minimal(self):
        """Test minimal data URL parsing."""
        result = parse_data_url("data:,Hello")
        
        self.assertEqual(result["media_type"], "text/plain")
        self.assertIsNone(result["encoding"])
        self.assertEqual(result["data"], "Hello")
    
    def test_parse_data_url_not_data(self):
        """Test parsing non-data URL."""
        result = parse_data_url("https://example.com")
        
        self.assertIsNone(result)


class TestURLComparison(unittest.TestCase):
    """Tests for URL comparison functions."""
    
    def test_urls_equal_basic(self):
        """Test basic URL equality."""
        self.assertTrue(urls_equal(
            "https://example.com/path",
            "https://example.com/path"
        ))
    
    def test_urls_equal_case_insensitive_host(self):
        """Test case-insensitive host comparison."""
        self.assertTrue(urls_equal(
            "https://EXAMPLE.COM/path",
            "https://example.com/path"
        ))
    
    def test_urls_equal_trailing_slash(self):
        """Test trailing slash handling."""
        self.assertTrue(urls_equal(
            "https://example.com/path/",
            "https://example.com/path"
        ))
    
    def test_urls_equal_query_order(self):
        """Test query parameter order."""
        self.assertTrue(urls_equal(
            "https://example.com?a=1&b=2",
            "https://example.com?b=2&a=1"
        ))
    
    def test_urls_equal_different_ports(self):
        """Test different ports."""
        self.assertFalse(urls_equal(
            "https://example.com:8080",
            "https://example.com:8443"
        ))
    
    def test_urls_equal_with_fragments(self):
        """Test fragment comparison."""
        self.assertFalse(urls_equal(
            "https://example.com#a",
            "https://example.com#b"
        ))
        
        self.assertTrue(urls_equal(
            "https://example.com#a",
            "https://example.com#b",
            ignore_fragment=True
        ))


class TestEdgeCases(unittest.TestCase):
    """Tests for edge cases."""
    
    def test_empty_url(self):
        """Test handling empty URL."""
        info = parse_url("")
        
        self.assertEqual(info.scheme, "")
        self.assertEqual(info.host, "")
    
    def test_unicode_in_url(self):
        """Test handling Unicode in URL."""
        url = "https://example.com/路径?查询=值"
        
        # Should not raise exception
        info = parse_url(url)
        self.assertEqual(info.scheme, "https")
    
    def test_special_characters_in_query(self):
        """Test special characters in query."""
        url = build_url(
            scheme="https",
            host="example.com",
            query={"q": "hello world & special < chars >"}
        )
        
        # Should encode special characters
        self.assertIn("q=", url)
        
        # Should be able to parse back
        info = parse_url(url)
        self.assertEqual(info.query["q"], ["hello world & special < chars >"])
    
    def test_ipv6_host(self):
        """Test IPv6 address in URL."""
        info = parse_url("https://[::1]:8080/path")
        
        # IPv6 handling may vary by implementation
        # Just check it doesn't crash
        self.assertEqual(info.scheme, "https")


if __name__ == "__main__":
    unittest.main(verbosity=2)
"""
AllToolkit - Python URL Utilities Test Suite

Comprehensive tests for URL parsing, validation, and manipulation.
"""

import sys
import unittest
from typing import List, Tuple

# Import module under test
from mod import (
    URL, URLConfig, URLError, URLValidationError, URLParseError, URLShortener,
    parse_url, validate_url, is_valid_url, normalize_url,
    extract_domain, extract_path, extract_query_params,
    build_url, join_url, sanitize_url, get_url_info
)


class TestURLParsing(unittest.TestCase):
    """Test URL parsing functionality."""
    
    def test_parse_simple_url(self):
        """Test parsing a simple HTTPS URL."""
        url = URL("https://example.com")
        self.assertEqual(url.scheme, "https")
        self.assertEqual(url.host, "example.com")
        self.assertEqual(url.path, "/")
        self.assertIsNone(url.port)
    
    def test_parse_url_with_port(self):
        """Test parsing URL with explicit port."""
        url = URL("https://example.com:8080/path")
        self.assertEqual(url.port, 8080)
        self.assertEqual(url.path, "/path")
    
    def test_parse_url_with_query(self):
        """Test parsing URL with query parameters."""
        url = URL("https://example.com/search?q=test&page=1")
        self.assertEqual(url.query.get("q"), "test")
        self.assertEqual(url.query.get("page"), "1")
    
    def test_parse_url_with_fragment(self):
        """Test parsing URL with fragment."""
        url = URL("https://example.com/page#section1")
        self.assertEqual(url.fragment, "section1")
    
    def test_parse_url_with_auth(self):
        """Test parsing URL with authentication."""
        url = URL("https://user:pass@example.com/path")
        self.assertEqual(url.username, "user")
        self.assertEqual(url.password, "pass")
    
    def test_parse_url_with_multiple_query_values(self):
        """Test parsing URL with multiple values for same param."""
        url = URL("https://example.com/search?tag=python&tag=programming")
        self.assertIsInstance(url.query.get("tag"), list)
        self.assertEqual(len(url.query.get("tag")), 2)
    
    def test_parse_invalid_scheme(self):
        """Test that invalid scheme raises error."""
        with self.assertRaises(URLValidationError):
            URL("invalid://example.com")
    
    def test_parse_url_too_long(self):
        """Test that overly long URLs raise error."""
        long_url = "https://example.com/" + "a" * 3000
        with self.assertRaises(URLParseError):
            URL(long_url)


class TestURLValidation(unittest.TestCase):
    """Test URL validation functionality."""
    
    def test_valid_domains(self):
        """Test validation of valid domain names."""
        valid_domains = [
            "https://example.com",
            "https://sub.example.com",
            "https://example.co.uk",
            "https://my-app.example.io",
        ]
        for url_str in valid_domains:
            with self.subTest(url=url_str):
                url = URL(url_str)
                self.assertTrue(url.is_absolute())
    
    def test_valid_ipv4(self):
        """Test validation of IPv4 addresses."""
        url = URL("https://192.168.1.1:8080/path")
        self.assertEqual(url.host, "192.168.1.1")
        self.assertEqual(url.port, 8080)
    
    def test_valid_ipv6(self):
        """Test validation of IPv6 addresses."""
        url = URL("https://[::1]:8080/path")
        self.assertEqual(url.host, "::1")  # urlparse strips brackets
    
    def test_invalid_port(self):
        """Test that invalid port raises error."""
        with self.assertRaises(URLValidationError):
            URL("https://example.com:99999")
    
    def test_validate_url_function(self):
        """Test validate_url convenience function."""
        valid, error = validate_url("https://example.com")
        self.assertTrue(valid)
        self.assertIsNone(error)
        
        valid, error = validate_url("invalid://url")
        self.assertFalse(valid)
        self.assertIsNotNone(error)
    
    def test_is_valid_url_function(self):
        """Test is_valid_url convenience function."""
        self.assertTrue(is_valid_url("https://example.com"))
        self.assertFalse(is_valid_url("not-a-url"))


class TestURLNormalization(unittest.TestCase):
    """Test URL normalization functionality."""
    
    def test_normalize_scheme_case(self):
        """Test that scheme is lowercased."""
        url = URL("HTTPS://EXAMPLE.COM")
        normalized = url.normalize()
        self.assertEqual(normalized.scheme, "https")
    
    def test_normalize_host_case(self):
        """Test that host is lowercased."""
        url = URL("https://EXAMPLE.COM")
        normalized = url.normalize()
        self.assertEqual(normalized.host, "example.com")
    
    def test_normalize_remove_default_port(self):
        """Test that default ports are removed."""
        url = URL("https://example.com:443/path")
        normalized = url.normalize()
        self.assertIsNone(normalized.port)
    
    def test_normalize_path_trailing_slash(self):
        """Test that trailing slashes are removed from non-root paths."""
        url = URL("https://example.com/path/to/page/")
        normalized = url.normalize()
        self.assertEqual(normalized.path, "/path/to/page")
    
    def test_normalize_path_resolve_dots(self):
        """Test that . and .. are resolved in paths."""
        url = URL("https://example.com/a/b/../c/./d")
        normalized = url.normalize()
        self.assertEqual(normalized.path, "/a/c/d")
    
    def test_normalize_sort_query_params(self):
        """Test that query params are sorted."""
        url = URL("https://example.com?z=1&a=2&m=3")
        normalized = url.normalize()
        keys = list(normalized.query.keys())
        self.assertEqual(keys, ["a", "m", "z"])
    
    def test_normalize_url_function(self):
        """Test normalize_url convenience function."""
        normalized = normalize_url("HTTPS://EXAMPLE.COM:443/Path/")
        self.assertEqual(normalized, "https://example.com/Path")


class TestURLStringConversion(unittest.TestCase):
    """Test URL to string conversion."""
    
    def test_to_string_basic(self):
        """Test basic URL string conversion."""
        url = URL("https://example.com/path")
        self.assertEqual(url.to_string(), "https://example.com/path")
    
    def test_to_string_with_query(self):
        """Test URL string conversion with query params."""
        url = URL(scheme="https", host="example.com", path="/search", query={"q": "test"})
        url_str = url.to_string()
        self.assertIn("q=test", url_str)
    
    def test_to_string_with_fragment(self):
        """Test URL string conversion with fragment."""
        url = URL("https://example.com/page#section")
        self.assertIn("#section", url.to_string())
    
    def test_to_string_exclude_auth(self):
        """Test that auth is excluded by default."""
        url = URL("https://user:pass@example.com/path")
        url_str = url.to_string()
        self.assertNotIn("user", url_str)
        self.assertNotIn("pass", url_str)
    
    def test_to_string_include_auth(self):
        """Test that auth can be included."""
        url = URL("https://user:pass@example.com/path")
        url_str = url.to_string(include_auth=True)
        self.assertIn("user:pass@", url_str)
    
    def test_str_repr(self):
        """Test __str__ and __repr__ methods."""
        url = URL("https://example.com")
        self.assertEqual(str(url), "https://example.com/")
        self.assertIn("example.com", repr(url))


class TestURLQueryMethods(unittest.TestCase):
    """Test URL query parameter methods."""
    
    def setUp(self):
        self.url = URL("https://example.com/search?q=test&page=1")
    
    def test_get_param(self):
        """Test getting query parameters."""
        self.assertEqual(self.url.get_param("q"), "test")
        self.assertEqual(self.url.get_param("page"), "1")
        self.assertEqual(self.url.get_param("missing", "default"), "default")
    
    def test_set_param(self):
        """Test setting query parameters."""
        self.url.set_param("sort", "asc")
        self.assertEqual(self.url.get_param("sort"), "asc")
    
    def test_remove_param(self):
        """Test removing query parameters."""
        self.url.remove_param("q")
        self.assertFalse(self.url.has_param("q"))
    
    def test_has_param(self):
        """Test checking parameter existence."""
        self.assertTrue(self.url.has_param("q"))
        self.assertFalse(self.url.has_param("missing"))
    
    def test_get_params(self):
        """Test getting all parameters."""
        params = self.url.get_params()
        self.assertIn("q", params)
        self.assertIn("page", params)


class TestURLPathMethods(unittest.TestCase):
    """Test URL path manipulation methods."""
    
    def test_get_path_segments(self):
        """Test getting path segments."""
        url = URL("https://example.com/a/b/c")
        self.assertEqual(url.get_path_segments(), ["a", "b", "c"])
    
    def test_set_path(self):
        """Test setting path."""
        url = URL("https://example.com/old")
        url.set_path("/new")
        self.assertEqual(url.path, "/new")
    
    def test_append_path(self):
        """Test appending to path."""
        url = URL("https://example.com/base")
        url.append_path("sub")
        self.assertEqual(url.path, "/base/sub")
    
    def test_get_parent_path(self):
        """Test getting parent path."""
        url = URL("https://example.com/a/b/c")
        self.assertEqual(url.get_parent_path(), "/a/b")
        
        url_root = URL("https://example.com/")
        self.assertEqual(url_root.get_parent_path(), "/")
    
    def test_origin_and_base(self):
        """Test origin and base URL methods."""
        url = URL("https://example.com:8080/path?query=1#frag")
        self.assertEqual(url.get_origin(), "https://example.com:8080")
        self.assertEqual(url.get_base_url(), "https://example.com:8080/path")


class TestURLComparison(unittest.TestCase):
    """Test URL comparison methods."""
    
    def test_same_origin(self):
        """Test same origin comparison."""
        url1 = URL("https://example.com/path1")
        url2 = URL("https://example.com/path2")
        url3 = URL("http://example.com/path1")
        
        self.assertTrue(url1.same_origin(url2))
        self.assertFalse(url1.same_origin(url3))
    
    def test_equals(self):
        """Test URL equality."""
        url1 = URL("https://example.com/path?q=1#frag")
        url2 = URL("https://example.com/path?q=1#frag")
        url3 = URL("https://example.com/path?q=2#frag")
        
        self.assertTrue(url1.equals(url2))
        self.assertFalse(url1.equals(url3))
        self.assertTrue(url1.equals(url3, ignore_query=True))
    
    def test_copy(self):
        """Test URL copying."""
        url1 = URL("https://example.com/path")
        url2 = url1.copy()
        
        self.assertEqual(url1.to_string(), url2.to_string())
        self.assertIsNot(url1, url2)


class TestURLChecks(unittest.TestCase):
    """Test URL property checks."""
    
    def test_is_secure(self):
        """Test secure URL check."""
        secure = URL("https://example.com")
        insecure = URL("http://example.com")
        
        self.assertTrue(secure.is_secure())
        self.assertFalse(insecure.is_secure())
    
    def test_is_absolute(self):
        """Test absolute URL check."""
        absolute = URL("https://example.com")
        # Relative URLs would need different construction
        self.assertTrue(absolute.is_absolute())
    
    def test_has_query(self):
        """Test query presence check."""
        with_query = URL("https://example.com?q=1")
        without_query = URL("https://example.com")
        
        self.assertTrue(with_query.has_query())
        self.assertFalse(without_query.has_query())
    
    def test_has_fragment(self):
        """Test fragment presence check."""
        with_frag = URL("https://example.com#section")
        without_frag = URL("https://example.com")
        
        self.assertTrue(with_frag.has_fragment())
        self.assertFalse(without_frag.has_fragment())
    
    def test_has_auth(self):
        """Test auth presence check."""
        with_auth = URL("https://user@example.com")
        without_auth = URL("https://example.com")
        
        self.assertTrue(with_auth.has_auth())
        self.assertFalse(without_auth.has_auth())


class TestConvenienceFunctions(unittest.TestCase):
    """Test convenience functions."""
    
    def test_parse_url(self):
        """Test parse_url function."""
        url = parse_url("https://example.com/path")
        self.assertIsInstance(url, URL)
        self.assertEqual(url.host, "example.com")
    
    def test_extract_domain(self):
        """Test extract_domain function."""
        domain = extract_domain("https://sub.example.com/path?q=1")
        self.assertEqual(domain, "sub.example.com")
    
    def test_extract_path(self):
        """Test extract_path function."""
        path = extract_path("https://example.com/a/b/c")
        self.assertEqual(path, "/a/b/c")
    
    def test_extract_query_params(self):
        """Test extract_query_params function."""
        params = extract_query_params("https://example.com?a=1&b=2")
        self.assertEqual(params.get("a"), "1")
        self.assertEqual(params.get("b"), "2")
    
    def test_build_url(self):
        """Test build_url function."""
        url = build_url(
            scheme="https",
            host="example.com",
            path="/search",
            query={"q": "test"}
        )
        self.assertIn("https://example.com/search", url)
        self.assertIn("q=test", url)
    
    def test_join_url(self):
        """Test join_url function."""
        result = join_url("https://example.com/a/b", "c")
        self.assertEqual(result, "https://example.com/a/b/c")
        
        result_abs = join_url("https://example.com/a/b", "/c")
        self.assertEqual(result_abs, "https://example.com/c")
    
    def test_sanitize_url(self):
        """Test sanitize_url function."""
        safe = sanitize_url("https://example.com/path")
        self.assertTrue(safe.startswith("https://"))
        
        with self.assertRaises(URLValidationError):
            sanitize_url("javascript:alert(1)")
    
    def test_get_url_info(self):
        """Test get_url_info function."""
        info = get_url_info("https://example.com:8080/path?q=1#frag")
        
        self.assertEqual(info['scheme'], "https")
        self.assertEqual(info['host'], "example.com")
        self.assertEqual(info['port'], 8080)
        self.assertEqual(info['path'], "/path")
        self.assertTrue(info['is_secure'])
        self.assertTrue(info['is_absolute'])


class TestURLShortener(unittest.TestCase):
    """Test URL shortener functionality."""
    
    def test_shorten_and_expand(self):
        """Test shortening and expanding URLs."""
        shortener = URLShortener()
        original = "https://example.com/very/long/path/that/needs/shortening"
        
        short = shortener.shorten(original)
        self.assertTrue(short.startswith("https://short.url/"))
        
        expanded = shortener.expand(short)
        self.assertEqual(expanded, original)
    
    def test_same_url_same_short(self):
        """Test that same URL returns same short URL."""
        shortener = URLShortener()
        url = "https://example.com/test"
        
        short1 = shortener.shorten(url)
        short2 = shortener.shorten(url)
        
        self.assertEqual(short1, short2)
    
    def test_invalid_url_shorten(self):
        """Test that invalid URLs raise error on shorten."""
        shortener = URLShortener()
        
        with self.assertRaises(URLValidationError):
            shortener.shorten("not-a-valid-url")
    
    def test_expand_nonexistent(self):
        """Test expanding non-existent short URL."""
        shortener = URLShortener()
        
        with self.assertRaises(URLError):
            shortener.expand("https://short.url/xyz")


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and boundary conditions."""
    
    def test_empty_query_values(self):
        """Test handling of empty query values."""
        url = URL("https://example.com?empty=&filled=value")
        self.assertEqual(url.get_param("empty"), "")
        self.assertEqual(url.get_param("filled"), "value")
    
    def test_unicode_in_url(self):
        """Test handling of Unicode characters."""
        url = URL("https://example.com/path/中文")
        self.assertIn("中文", url.path)
    
    def test_special_characters_in_query(self):
        """Test handling of special characters in query."""
        url = URL("https://example.com?email=test@example.com&url=https://other.com")
        self.assertEqual(url.get_param("email"), "test@example.com")
    
    def test_very_long_path(self):
        """Test handling of long paths."""
        long_path = "/" + "/".join(["segment"] * 100)
        url = URL(f"https://example.com{long_path}")
        self.assertEqual(len(url.get_path_segments()), 100)
    
    def test_multiple_subdomains(self):
        """Test handling of multiple subdomains."""
        url = URL("https://a.b.c.d.example.com/path")
        self.assertEqual(url.host, "a.b.c.d.example.com")
    
    def test_port_boundary(self):
        """Test port boundary values."""
        url_min = URL("https://example.com:1/path")
        url_max = URL("https://example.com:65535/path")
        
        self.assertEqual(url_min.port, 1)
        self.assertEqual(url_max.port, 65535)
        
        with self.assertRaises(URLValidationError):
            URL("https://example.com:0/path")
        
        with self.assertRaises(URLValidationError):
            URL("https://example.com:65536/path")


class TestURLChaining(unittest.TestCase):
    """Test method chaining."""
    
    def test_query_chaining(self):
        """Test query parameter chaining."""
        url = URL("https://example.com")
        result = (url
            .set_param("a", "1")
            .set_param("b", "2")
            .remove_param("a")
            .set_param("c", "3"))
        
        self.assertIs(result, url)
        self.assertFalse(url.has_param("a"))
        self.assertTrue(url.has_param("b"))
        self.assertTrue(url.has_param("c"))
    
    def test_path_chaining(self):
        """Test path manipulation chaining."""
        url = URL("https://example.com/base")
        result = (url
            .append_path("sub1")
            .append_path("sub2")
            .set_path("/new"))
        
        self.assertIs(result, url)
        self.assertEqual(url.path, "/new")


def run_tests():
    """Run all tests and return results."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    test_classes = [
        TestURLParsing,
        TestURLValidation,
        TestURLNormalization,
        TestURLStringConversion,
        TestURLQueryMethods,
        TestURLPathMethods,
        TestURLComparison,
        TestURLChecks,
        TestConvenienceFunctions,
        TestURLShortener,
        TestEdgeCases,
        TestURLChaining,
    ]
    
    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result


if __name__ == "__main__":
    print("=" * 70)
    print("AllToolkit - Python URL Utilities Test Suite")
    print("=" * 70)
    print()
    
    result = run_tests()
    
    print()
    print("=" * 70)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success: {result.wasSuccessful()}")
    print("=" * 70)
    
    sys.exit(0 if result.wasSuccessful() else 1)

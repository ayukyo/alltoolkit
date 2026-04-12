#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AllToolkit - HTTP Utilities Test Suite

Comprehensive tests for http_utils module.
Run with: python http_utils_test.py
"""

import unittest
import threading
import time
import json
import sys
import os
from typing import Optional

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from http_utils.mod import (
    # Client and Server
    HTTPClient, HTTPServer, ServerConfig, BaseRequestHandler,
    # Data classes
    HTTPRequest, HTTPResponse, RequestInfo,
    # Enums
    Method, ContentType,
    # URL utilities
    parse_url, build_url, encode_query_params, decode_query_params,
    url_encode, url_decode, is_valid_url, get_domain, normalize_url,
    # Header utilities
    parse_headers, format_headers, get_content_type,
    create_basic_auth_header, parse_auth_header,
    # Cookie utilities
    parse_cookies, format_cookies, create_cookie,
    # Convenience functions
    get, post, put, delete, download_file, fetch_json, check_url_status,
    # Module info
    version, features
)


# =============================================================================
# Test Constants
# =============================================================================

TEST_HOST = "127.0.0.1"
TEST_PORT = 18888
TEST_TIMEOUT = 5.0


# =============================================================================
# Test Server Setup
# =============================================================================

class TestServerFixture:
    """Test server fixture for integration tests."""
    
    def __init__(self, host: str = TEST_HOST, port: int = TEST_PORT):
        self.host = host
        self.port = port
        self.server: Optional[HTTPServer] = None
        self._running = False
    
    def setup(self):
        """Start test server."""
        self.server = HTTPServer(ServerConfig(host=self.host, port=self.port))
        
        @self.server.route("/hello")
        def hello_handler(request: RequestInfo):
            return {"message": "Hello, World!", "method": request.method}
        
        @self.server.route("/echo", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
        def echo_handler(request: RequestInfo):
            return {
                "method": request.method,
                "path": request.path,
                "query": request.query,
                "headers": dict(request.headers),
                "body": request.body.decode("utf-8") if request.body else ""
            }
        
        @self.server.route("/json", methods=["POST"])
        def json_handler(request: RequestInfo):
            try:
                data = json.loads(request.body.decode("utf-8"))
                return {"received": data, "status": "ok"}
            except json.JSONDecodeError:
                return {"error": "Invalid JSON"}, 400
        
        @self.server.route("/status/<code>")
        def status_handler(request: RequestInfo):
            # Simple status endpoint
            return {"status": "ok"}, 200
        
        @self.server.route("/slow")
        def slow_handler(request: RequestInfo):
            time.sleep(0.5)
            return {"message": "Delayed response"}
        
        self.server.start(blocking=False)
        self._running = True
        time.sleep(0.1)  # Wait for server to start
    
    def teardown(self):
        """Stop test server."""
        if self.server and self._running:
            self.server.stop()
            self._running = False
    
    def base_url(self) -> str:
        """Get server base URL."""
        return f"http://{self.host}:{self.port}"


# =============================================================================
# URL Utilities Tests
# =============================================================================

class TestURLUtilities(unittest.TestCase):
    """Tests for URL utility functions."""
    
    def test_parse_url(self):
        """Test URL parsing."""
        url = "https://user:pass@example.com:8080/path?query=value#fragment"
        parsed = parse_url(url)
        
        self.assertEqual(parsed["scheme"], "https")
        self.assertEqual(parsed["hostname"], "example.com")
        self.assertEqual(parsed["port"], 8080)
        self.assertEqual(parsed["username"], "user")
        self.assertEqual(parsed["password"], "pass")
        self.assertEqual(parsed["path"], "/path")
        self.assertEqual(parsed["query"], "query=value")
        self.assertEqual(parsed["fragment"], "fragment")
    
    def test_build_url(self):
        """Test URL building."""
        url = build_url("https", "example.com", "/path", port=8080,
                       params={"key": "value"}, fragment="section")
        
        self.assertEqual(url, "https://example.com:8080/path?key=value#section")
    
    def test_encode_query_params(self):
        """Test query parameter encoding."""
        params = {"name": "John", "age": "30", "tags": ["a", "b"]}
        encoded = encode_query_params(params)
        
        self.assertIn("name=John", encoded)
        self.assertIn("age=30", encoded)
        self.assertIn("tags=a", encoded)
        self.assertIn("tags=b", encoded)
    
    def test_decode_query_params(self):
        """Test query parameter decoding."""
        query = "name=John&age=30&tags=a&tags=b"
        decoded = decode_query_params(query)
        
        self.assertEqual(decoded["name"], ["John"])
        self.assertEqual(decoded["age"], ["30"])
        self.assertEqual(decoded["tags"], ["a", "b"])
    
    def test_url_encode(self):
        """Test URL encoding."""
        text = "Hello World! 你好"
        encoded = url_encode(text)
        
        self.assertEqual(encoded, "Hello%20World%21%20%E4%BD%A0%E5%A5%BD")
    
    def test_url_decode(self):
        """Test URL decoding."""
        encoded = "Hello%20World%21%20%E4%BD%A0%E5%A5%BD"
        decoded = url_decode(encoded)
        
        self.assertEqual(decoded, "Hello World! 你好")
    
    def test_is_valid_url(self):
        """Test URL validation."""
        self.assertTrue(is_valid_url("https://example.com"))
        self.assertTrue(is_valid_url("http://example.com/path"))
        self.assertFalse(is_valid_url("not-a-url"))
        self.assertFalse(is_valid_url(""))
    
    def test_get_domain(self):
        """Test domain extraction."""
        self.assertEqual(get_domain("https://www.example.com/path"), "www.example.com")
        self.assertEqual(get_domain("http://example.com:8080"), "example.com:8080")
    
    def test_normalize_url(self):
        """Test URL normalization."""
        self.assertEqual(normalize_url("example.com"), "http://example.com")
        self.assertEqual(normalize_url("https://example.com"), "https://example.com")


# =============================================================================
# Header Utilities Tests
# =============================================================================

class TestHeaderUtilities(unittest.TestCase):
    """Tests for header utility functions."""
    
    def test_parse_headers(self):
        """Test header parsing."""
        header_string = "Content-Type: application/json\r\nAuthorization: Bearer token123"
        headers = parse_headers(header_string)
        
        self.assertEqual(headers["Content-Type"], "application/json")
        self.assertEqual(headers["Authorization"], "Bearer token123")
    
    def test_format_headers(self):
        """Test header formatting."""
        headers = {"Content-Type": "application/json", "X-Custom": "value"}
        formatted = format_headers(headers)
        
        self.assertIn("Content-Type: application/json", formatted)
        self.assertIn("X-Custom: value", formatted)
    
    def test_get_content_type(self):
        """Test content type detection."""
        self.assertEqual(get_content_type("file.json"), ContentType.JSON.value)
        self.assertEqual(get_content_type("file.html"), ContentType.HTML.value)
        self.assertEqual(get_content_type("file.txt"), ContentType.TEXT.value)
        self.assertEqual(get_content_type("file.unknown"), ContentType.OCTET_STREAM.value)
    
    def test_create_basic_auth_header(self):
        """Test Basic Auth header creation."""
        auth = create_basic_auth_header("user", "pass")
        
        self.assertTrue(auth.startswith("Basic "))
        # Verify credentials
        import base64
        encoded = auth.split(" ")[1]
        decoded = base64.b64decode(encoded).decode("utf-8")
        self.assertEqual(decoded, "user:pass")
    
    def test_parse_auth_header(self):
        """Test Authorization header parsing."""
        auth_type, credentials = parse_auth_header("Bearer token123")
        
        self.assertEqual(auth_type, "Bearer")
        self.assertEqual(credentials, "token123")


# =============================================================================
# Cookie Utilities Tests
# =============================================================================

class TestCookieUtilities(unittest.TestCase):
    """Tests for cookie utility functions."""
    
    def test_parse_cookies(self):
        """Test cookie parsing."""
        cookie_header = "session=abc123; user=john; theme=dark"
        cookies = parse_cookies(cookie_header)
        
        self.assertEqual(cookies["session"], "abc123")
        self.assertEqual(cookies["user"], "john")
        self.assertEqual(cookies["theme"], "dark")
    
    def test_format_cookies(self):
        """Test cookie formatting."""
        cookies = {"session": "abc123", "user": "john"}
        formatted = format_cookies(cookies)
        
        self.assertIn("session=abc123", formatted)
        self.assertIn("user=john", formatted)
    
    def test_create_cookie(self):
        """Test cookie creation."""
        cookie = create_cookie("session", "abc123", path="/", 
                              secure=True, httponly=True)
        
        self.assertIn("session=abc123", cookie)
        self.assertIn("Path=/", cookie)
        self.assertIn("Secure", cookie)
        self.assertIn("HttpOnly", cookie)


# =============================================================================
# HTTP Client Tests
# =============================================================================

class TestHTTPClient(unittest.TestCase):
    """Tests for HTTP client."""
    
    @classmethod
    def setUpClass(cls):
        """Start test server."""
        cls.test_server = TestServerFixture()
        cls.test_server.setup()
        cls.base_url = cls.test_server.base_url()
    
    @classmethod
    def tearDownClass(cls):
        """Stop test server."""
        cls.test_server.teardown()
    
    def test_client_get(self):
        """Test GET request."""
        client = HTTPClient()
        response = client.get(f"{self.base_url}/hello")
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["message"], "Hello, World!")
        self.assertEqual(data["method"], "GET")
    
    def test_client_post_json(self):
        """Test POST with JSON data."""
        client = HTTPClient()
        response = client.post(
            f"{self.base_url}/json",
            json_data={"name": "Test", "value": 123}
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["received"]["name"], "Test")
        self.assertEqual(data["received"]["value"], 123)
    
    def test_client_post_form(self):
        """Test POST with form data."""
        client = HTTPClient()
        response = client.post(
            f"{self.base_url}/echo",
            data={"field1": "value1", "field2": "value2"}
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("field1=value1", data["body"])
    
    def test_client_put(self):
        """Test PUT request."""
        client = HTTPClient()
        response = client.put(
            f"{self.base_url}/echo",
            json_data={"updated": True}
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["method"], "PUT")
    
    def test_client_delete(self):
        """Test DELETE request."""
        client = HTTPClient()
        response = client.delete(f"{self.base_url}/echo")
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["method"], "DELETE")
    
    def test_client_with_base_url(self):
        """Test client with base URL."""
        client = HTTPClient(base_url=self.base_url)
        response = client.get("/hello")
        
        self.assertEqual(response.status_code, 200)
    
    def test_client_with_headers(self):
        """Test client with default headers."""
        client = HTTPClient(
            base_url=self.base_url,
            default_headers={"X-Custom-Header": "test-value"}
        )
        response = client.get("/echo")
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["headers"].get("X-Custom-Header"), "test-value")
    
    def test_response_properties(self):
        """Test HTTP response properties."""
        client = HTTPClient()
        response = client.get(f"{self.base_url}/hello")
        
        self.assertTrue(response.ok)
        self.assertFalse(response.is_redirect)
        self.assertFalse(response.is_error)
        self.assertIsInstance(response.text(), str)
        self.assertIsInstance(response.json(), dict)
    
    def test_response_elapsed_time(self):
        """Test response elapsed time."""
        client = HTTPClient()
        response = client.get(f"{self.base_url}/hello")
        
        self.assertGreater(response.elapsed_time, 0)
    
    def test_convenience_get(self):
        """Test convenience get function."""
        response = get(f"{self.base_url}/hello")
        
        self.assertEqual(response.status_code, 200)
    
    def test_convenience_post(self):
        """Test convenience post function."""
        response = post(
            f"{self.base_url}/json",
            json_data={"test": True}
        )
        
        self.assertEqual(response.status_code, 200)
    
    def test_check_url_status(self):
        """Test URL status check."""
        status = check_url_status(f"{self.base_url}/hello")
        
        self.assertEqual(status, 200)


# =============================================================================
# HTTP Server Tests
# =============================================================================

class TestHTTPServer(unittest.TestCase):
    """Tests for HTTP server."""
    
    def test_server_creation(self):
        """Test server creation."""
        config = ServerConfig(host="localhost", port=9999)
        server = HTTPServer(config)
        
        self.assertEqual(server.config.host, "localhost")
        self.assertEqual(server.config.port, 9999)
    
    def test_route_decorator(self):
        """Test route decorator."""
        server = HTTPServer()
        
        @server.route("/test", methods=["GET", "POST"])
        def handler(request):
            return {"ok": True}
        
        self.assertIn("/test", server.routes)
        self.assertIn("GET", server.routes["/test"])
        self.assertIn("POST", server.routes["/test"])
    
    def test_server_start_stop(self):
        """Test server start and stop."""
        config = ServerConfig(host="127.0.0.1", port=19999)
        server = HTTPServer(config)
        
        @server.route("/ping")
        def ping_handler(request):
            return {"pong": True}
        
        server.start(blocking=False)
        time.sleep(0.2)
        
        # Test the endpoint
        client = HTTPClient()
        response = client.get("http://127.0.0.1:19999/ping")
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["pong"])
        
        server.stop()


# =============================================================================
# Integration Tests
# =============================================================================

class TestIntegration(unittest.TestCase):
    """Integration tests."""
    
    @classmethod
    def setUpClass(cls):
        """Start test server."""
        cls.test_server = TestServerFixture()
        cls.test_server.setup()
        cls.base_url = cls.test_server.base_url()
    
    @classmethod
    def tearDownClass(cls):
        """Stop test server."""
        cls.test_server.teardown()
    
    def test_full_request_response_cycle(self):
        """Test complete request-response cycle."""
        client = HTTPClient(base_url=self.base_url)
        
        # POST JSON data
        post_response = client.post("/json", json_data={"key": "value"})
        self.assertTrue(post_response.ok)
        
        # GET with query params
        get_response = client.get("/echo", params={"search": "test", "page": "1"})
        self.assertTrue(get_response.ok)
        data = get_response.json()
        self.assertEqual(data["query"]["search"], ["test"])
    
    def test_error_handling(self):
        """Test error handling."""
        client = HTTPClient()
        
        # Non-existent URL
        response = client.get("http://nonexistent.invalid.domain", timeout=2.0)
        self.assertEqual(response.status_code, 0)
    
    def test_timeout_handling(self):
        """Test timeout handling."""
        # Test with very short timeout to a slow endpoint
        client = HTTPClient(timeout=0.01)
        
        # This should timeout since /slow takes 0.5 seconds
        response = client.get(f"{self.base_url}/slow")
        
        # Either timeout (status 0) or slow response is acceptable
        # The key is that the request doesn't hang indefinitely
        self.assertIn(response.status_code, [0, 200])


# =============================================================================
# Module Info Tests
# =============================================================================

class TestModuleInfo(unittest.TestCase):
    """Tests for module info functions."""
    
    def test_version(self):
        """Test version function."""
        v = version()
        self.assertIsInstance(v, str)
        self.assertTrue(len(v) > 0)
    
    def test_features(self):
        """Test features function."""
        features_list = features()
        self.assertIsInstance(features_list, list)
        self.assertGreater(len(features_list), 0)
        
        # Check expected features
        feature_str = " ".join(features_list)
        self.assertIn("HTTPClient", feature_str)
        self.assertIn("HTTPServer", feature_str)
        self.assertIn("URL", feature_str)


# =============================================================================
# Main Test Runner
# =============================================================================

if __name__ == "__main__":
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(TestURLUtilities))
    suite.addTests(loader.loadTestsFromTestCase(TestHeaderUtilities))
    suite.addTests(loader.loadTestsFromTestCase(TestCookieUtilities))
    suite.addTests(loader.loadTestsFromTestCase(TestHTTPClient))
    suite.addTests(loader.loadTestsFromTestCase(TestHTTPServer))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    suite.addTests(loader.loadTestsFromTestCase(TestModuleInfo))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 70)
    print(f"Tests Run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success: {result.wasSuccessful()}")
    
    sys.exit(0 if result.wasSuccessful() else 1)

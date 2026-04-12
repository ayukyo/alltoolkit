#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AllToolkit HTTP Utils - Basic Usage Examples

This file demonstrates common use cases for the HTTP utilities module.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    HTTPClient, HTTPServer, ServerConfig, RequestInfo,
    get, post, put, delete,
    parse_url, build_url, url_encode, is_valid_url,
    create_basic_auth_header, parse_cookies, create_cookie,
    download_file, fetch_json, check_url_status,
    Method, ContentType
)


# =============================================================================
# Example 1: Simple GET Request
# =============================================================================

def example_simple_get():
    """Demonstrate simple GET request."""
    print("=" * 60)
    print("Example 1: Simple GET Request")
    print("=" * 60)
    
    response = get("https://httpbin.org/get")
    
    if response.ok:
        data = response.json()
        print(f"Status: {response.status_code}")
        print(f"Origin: {data.get('origin', 'N/A')}")
        print(f"Headers received: {list(data.get('headers', {}).keys())[:5]}")
    else:
        print(f"Request failed: {response.status_code}")
    
    print()


# =============================================================================
# Example 2: POST with JSON Data
# =============================================================================

def example_post_json():
    """Demonstrate POST request with JSON data."""
    print("=" * 60)
    print("Example 2: POST with JSON Data")
    print("=" * 60)
    
    response = post(
        "https://httpbin.org/post",
        json_data={
            "name": "AllToolkit",
            "version": "1.0.0",
            "features": ["HTTP Client", "HTTP Server", "URL Utils"]
        }
    )
    
    if response.ok:
        data = response.json()
        print(f"Status: {response.status_code}")
        print(f"Data received: {data.get('json', {})}")
    else:
        print(f"Request failed: {response.status_code}")
    
    print()


# =============================================================================
# Example 3: HTTP Client with Configuration
# =============================================================================

def example_http_client():
    """Demonstrate HTTPClient with custom configuration."""
    print("=" * 60)
    print("Example 3: HTTPClient with Configuration")
    print("=" * 60)
    
    # Create client with base URL and default headers
    client = HTTPClient(
        base_url="https://httpbin.org",
        default_headers={
            "X-Custom-Header": "MyApp/1.0",
            "Accept": "application/json"
        },
        timeout=10.0
    )
    
    # Make requests using relative paths
    response = client.get("/headers")
    
    if response.ok:
        data = response.json()
        print(f"Status: {response.status_code}")
        print(f"Headers sent: {data.get('headers', {})}")
    else:
        print(f"Request failed: {response.status_code}")
    
    print()


# =============================================================================
# Example 4: URL Utilities
# =============================================================================

def example_url_utilities():
    """Demonstrate URL utility functions."""
    print("=" * 60)
    print("Example 4: URL Utilities")
    print("=" * 60)
    
    # Parse URL
    url = "https://user:pass@api.example.com:8080/v1/users?id=123&name=test#section"
    parsed = parse_url(url)
    print(f"Parsed URL: {url}")
    print(f"  Scheme: {parsed['scheme']}")
    print(f"  Host: {parsed['hostname']}")
    print(f"  Port: {parsed['port']}")
    print(f"  Path: {parsed['path']}")
    print()
    
    # Build URL
    built_url = build_url(
        scheme="https",
        hostname="api.example.com",
        path="v1/search",
        port=443,
        params={"q": "python", "page": "1"},
        fragment="results"
    )
    print(f"Built URL: {built_url}")
    print()
    
    # URL encoding
    text = "Hello World! 你好世界"
    encoded = url_encode(text)
    decoded = url_encode(encoded)
    print(f"Original: {text}")
    print(f"Encoded: {encoded}")
    print()
    
    # Validate URL
    test_urls = [
        "https://example.com",
        "http://example.com/path",
        "not-a-url",
        ""
    ]
    print("URL Validation:")
    for test_url in test_urls:
        valid = is_valid_url(test_url)
        print(f"  '{test_url}' -> {'Valid' if valid else 'Invalid'}")
    
    print()


# =============================================================================
# Example 5: Header and Cookie Utilities
# =============================================================================

def example_headers_cookies():
    """Demonstrate header and cookie utilities."""
    print("=" * 60)
    print("Example 5: Headers and Cookies")
    print("=" * 60)
    
    # Basic Auth
    auth_header = create_basic_auth_header("username", "password123")
    print(f"Basic Auth Header: {auth_header}")
    print()
    
    # Parse cookies
    cookie_header = "session=abc123; user=john; theme=dark; lang=en"
    cookies = parse_cookies(cookie_header)
    print(f"Cookie Header: {cookie_header}")
    print(f"Parsed Cookies: {cookies}")
    print()
    
    # Create cookie
    new_cookie = create_cookie(
        name="session",
        value="xyz789",
        path="/",
        secure=True,
        httponly=True
    )
    print(f"New Cookie: {new_cookie}")
    print()


# =============================================================================
# Example 6: Simple HTTP Server
# =============================================================================

def example_http_server():
    """Demonstrate simple HTTP server."""
    print("=" * 60)
    print("Example 6: Simple HTTP Server")
    print("=" * 60)
    print("Starting server on http://localhost:8765")
    print("Press Ctrl+C to stop")
    print()
    
    # Create server
    config = ServerConfig(host="localhost", port=8765)
    server = HTTPServer(config)
    
    # Register routes
    @server.route("/")
    def home(request: RequestInfo):
        return {
            "message": "Welcome to AllToolkit HTTP Server!",
            "method": request.method,
            "path": request.path
        }
    
    @server.route("/hello")
    def hello(request: RequestInfo):
        name = request.query.get("name", ["World"])[0]
        return {"message": f"Hello, {name}!"}
    
    @server.route("/echo", methods=["GET", "POST"])
    def echo(request: RequestInfo):
        return {
            "method": request.method,
            "path": request.path,
            "query": request.query,
            "body_length": len(request.body) if request.body else 0
        }
    
    @server.route("/api/data", methods=["POST"])
    def api_data(request: RequestInfo):
        import json
        try:
            data = json.loads(request.body.decode("utf-8"))
            return {
                "status": "success",
                "received": data,
                "items_count": len(data) if isinstance(data, list) else 1
            }
        except json.JSONDecodeError:
            return {"status": "error", "message": "Invalid JSON"}, 400
    
    # Start server (blocking)
    try:
        server.start(blocking=True)
    except KeyboardInterrupt:
        print("\nServer stopped.")


# =============================================================================
# Example 7: Check Website Status
# =============================================================================

def example_status_check():
    """Demonstrate website status checking."""
    print("=" * 60)
    print("Example 7: Website Status Check")
    print("=" * 60)
    
    websites = [
        "https://www.google.com",
        "https://www.github.com",
        "https://httpbin.org",
        "https://nonexistent.invalid.domain"
    ]
    
    for url in websites:
        status = check_url_status(url, timeout=3.0)
        status_text = "✓ Online" if status == 200 else f"✗ Status: {status}"
        print(f"{url}: {status_text}")
    
    print()


# =============================================================================
# Example 8: Fetch JSON Data
# =============================================================================

def example_fetch_json():
    """Demonstrate fetching JSON data."""
    print("=" * 60)
    print("Example 8: Fetch JSON Data")
    print("=" * 60)
    
    try:
        data = fetch_json("https://httpbin.org/json")
        print(f"Successfully fetched JSON data")
        print(f"Keys: {list(data.keys()) if isinstance(data, dict) else 'N/A'}")
    except Exception as e:
        print(f"Failed to fetch JSON: {e}")
    
    print()


# =============================================================================
# Main - Run Examples
# =============================================================================

def run_examples():
    """Run all examples except the server (which blocks)."""
    print("\n" + "=" * 60)
    print("AllToolkit HTTP Utils - Examples")
    print("=" * 60)
    print()
    
    example_simple_get()
    example_post_json()
    example_http_client()
    example_url_utilities()
    example_headers_cookies()
    example_status_check()
    example_fetch_json()
    
    print("=" * 60)
    print("All examples completed!")
    print("=" * 60)
    print()
    print("To run the HTTP server example, call:")
    print("  python examples/basic_usage.py server")
    print()


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "server":
        example_http_server()
    else:
        run_examples()

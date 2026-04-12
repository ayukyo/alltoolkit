#!/usr/bin/env python3
"""
AllToolkit - URL Utilities Basic Usage Examples

Demonstrates fundamental URL parsing, validation, and manipulation.
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    URL, parse_url, validate_url, is_valid_url, normalize_url,
    extract_domain, extract_path, extract_query_params,
    build_url, join_url, get_url_info
)


def example_1_parse_url():
    """Example 1: Parse a URL into components."""
    print("=" * 60)
    print("Example 1: Parse URL")
    print("=" * 60)
    
    url_str = "https://api.example.com:8080/v1/users?page=1&limit=20#results"
    url = parse_url(url_str)
    
    print(f"Original URL: {url_str}")
    print(f"\nParsed Components:")
    print(f"  Scheme:   {url.scheme}")
    print(f"  Host:     {url.host}")
    print(f"  Port:     {url.port}")
    print(f"  Path:     {url.path}")
    print(f"  Query:    {url.query}")
    print(f"  Fragment: {url.fragment}")
    print()


def example_2_validate_url():
    """Example 2: Validate URLs."""
    print("=" * 60)
    print("Example 2: Validate URLs")
    print("=" * 60)
    
    test_urls = [
        "https://example.com",
        "http://localhost:3000",
        "https://192.168.1.1:8080/api",
        "ftp://files.example.com/download",
        "invalid-url",
        "javascript:alert('xss')",
        "https://example.com:99999",  # Invalid port
    ]
    
    for url_str in test_urls:
        valid, error = validate_url(url_str)
        status = "✓ Valid" if valid else f"✗ Invalid: {error}"
        print(f"  {url_str[:50]:<50} {status}")
    print()


def example_3_normalize_url():
    """Example 3: Normalize URLs."""
    print("=" * 60)
    print("Example 3: Normalize URLs")
    print("=" * 60)
    
    test_urls = [
        "HTTPS://EXAMPLE.COM:443/Path/",
        "https://example.com/a/b/../c/./d",
        "https://example.com/search?z=1&a=2&m=3",
        "https://Example.COM:443/Page%20Title",
    ]
    
    for url_str in test_urls:
        normalized = normalize_url(url_str)
        print(f"  Original:   {url_str}")
        print(f"  Normalized: {normalized}")
        print()


def example_4_extract_components():
    """Example 4: Extract URL components."""
    print("=" * 60)
    print("Example 4: Extract Components")
    print("=" * 60)
    
    url_str = "https://cdn.example.com:443/assets/images/logo.png?v=123"
    
    print(f"URL: {url_str}")
    print(f"  Domain: {extract_domain(url_str)}")
    print(f"  Path:   {extract_path(url_str)}")
    print(f"  Params: {extract_query_params(url_str)}")
    print()


def example_5_build_url():
    """Example 5: Build URL from components."""
    print("=" * 60)
    print("Example 5: Build URL")
    print("=" * 60)
    
    url = build_url(
        scheme="https",
        host="api.github.com",
        port=None,  # Uses default
        path="/repos/ayukyo/alltoolkit",
        query={"branch": "main", "per_page": "30"},
        fragment="files"
    )
    
    print(f"Built URL: {url}")
    print()


def example_6_join_urls():
    """Example 6: Join base and relative URLs."""
    print("=" * 60)
    print("Example 6: Join URLs")
    print("=" * 60)
    
    base = "https://example.com/api/v1"
    
    print(f"Base URL: {base}")
    print(f"  + 'users'        → {join_url(base, 'users')}")
    print(f"  + '/users'       → {join_url(base, '/users')}")
    print(f"  + 'users/123'    → {join_url(base, 'users/123')}")
    print(f"  + '../v2/users'  → {join_url(base, '../v2/users')}")
    print()


def example_7_url_class_operations():
    """Example 7: URL class operations."""
    print("=" * 60)
    print("Example 7: URL Class Operations")
    print("=" * 60)
    
    # Create URL from components
    url = URL(
        scheme="https",
        host="example.com",
        path="/search"
    )
    
    # Chain operations
    (url
     .set_param("q", "python")
     .set_param("page", "1")
     .append_path("results"))
    
    print(f"Modified URL: {url.to_string()}")
    print(f"  Has query:  {url.has_query()}")
    print(f"  Is secure:  {url.is_secure()}")
    print(f"  Path segments: {url.get_path_segments()}")
    print(f"  Origin:     {url.get_origin()}")
    print()


def example_8_url_comparison():
    """Example 8: Compare URLs."""
    print("=" * 60)
    print("Example 8: URL Comparison")
    print("=" * 60)
    
    url1 = URL("https://example.com/page?a=1&b=2#top")
    url2 = URL("https://example.com/page?b=2&a=1#bottom")
    url3 = URL("http://example.com/page?a=1&b=2")
    
    print(f"URL1: {url1.to_string()}")
    print(f"URL2: {url2.to_string()}")
    print(f"URL3: {url3.to_string()}")
    print()
    
    print(f"URL1 == URL2 (exact):     {url1.equals(url2)}")
    print(f"URL1 == URL2 (ignore frag): {url1.equals(url2, ignore_fragment=True)}")
    print(f"URL1 == URL2 (ignore query): {url1.equals(url2, ignore_query=True)}")
    print(f"URL1 same origin as URL2: {url1.same_origin(url2)}")
    print(f"URL1 same origin as URL3: {url1.same_origin(url3)}")
    print()


def example_9_get_url_info():
    """Example 9: Get comprehensive URL info."""
    print("=" * 60)
    print("Example 9: URL Info")
    print("=" * 60)
    
    url_str = "https://user:pass@api.example.com:8080/v1/data?key=value"
    info = get_url_info(url_str)
    
    print(f"URL: {url_str}")
    print(f"\nDetailed Info:")
    for key, value in info.items():
        if isinstance(value, dict):
            print(f"  {key}: {value}")
        else:
            print(f"  {key}: {value}")
    print()


def example_10_path_manipulation():
    """Example 10: Path manipulation."""
    print("=" * 60)
    print("Example 10: Path Manipulation")
    print("=" * 60)
    
    url = URL("https://example.com/blog/2024/posts")
    
    print(f"Original: {url.path}")
    print(f"  Segments:     {url.get_path_segments()}")
    print(f"  Parent:       {url.get_parent_path()}")
    
    url.append_path("123")
    print(f"  After append: {url.path}")
    
    url.set_path("/new/path")
    print(f"  After set:    {url.path}")
    print()


def main():
    """Run all examples."""
    print("\n" + "=" * 60)
    print("AllToolkit - Python URL Utilities - Basic Examples")
    print("=" * 60 + "\n")
    
    example_1_parse_url()
    example_2_validate_url()
    example_3_normalize_url()
    example_4_extract_components()
    example_5_build_url()
    example_6_join_urls()
    example_7_url_class_operations()
    example_8_url_comparison()
    example_9_get_url_info()
    example_10_path_manipulation()
    
    print("=" * 60)
    print("All examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()

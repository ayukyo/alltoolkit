#!/usr/bin/env python3
"""
AllToolkit - URL Utilities Advanced Usage Examples

Demonstrates advanced URL manipulation, security, and real-world scenarios.
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    URL, URLShortener, sanitize_url, URLValidationError,
    validate_url, normalize_url, get_url_info
)


class URLProcessor:
    """Advanced URL processor for web scraping and analysis."""
    
    def __init__(self, base_domain: str, allowed_schemes=None):
        self.base_domain = base_domain.lower()
        self.allowed_schemes = allowed_schemes or ['http', 'https']
        self.visited = set()
        self.to_visit = []
    
    def is_internal_url(self, url_str: str) -> bool:
        """Check if URL belongs to the same domain."""
        try:
            url = URL(url_str)
            # Handle subdomains
            return url.host.lower().endswith(self.base_domain)
        except Exception:
            return False
    
    def is_safe_url(self, url_str: str) -> bool:
        """Check if URL is safe to visit."""
        try:
            # Validate scheme
            url = URL(url_str)
            if url.scheme not in self.allowed_schemes:
                return False
            
            # Check for auth (potential security risk)
            if url.has_auth():
                print(f"  ⚠️  URL contains authentication info")
            
            return True
            
        except URLValidationError:
            return False
    
    def normalize_for_comparison(self, url_str: str) -> str:
        """Normalize URL for deduplication."""
        url = URL(url_str).normalize()
        # Remove fragment for comparison
        url.fragment = ""
        return url.to_string()
    
    def add_to_crawl_queue(self, url_str: str, base_url: str = "") -> bool:
        """
        Add URL to crawl queue if valid and not visited.
        
        Returns True if added, False if skipped.
        """
        try:
            # Handle relative URLs
            if base_url and not url_str.startswith(('http://', 'https://')):
                base = URL(base_url)
                if url_str.startswith('/'):
                    base.path = url_str
                else:
                    base.append_path(url_str)
                url_str = base.to_string()
            
            # Validate
            valid, error = validate_url(url_str)
            if not valid:
                print(f"  ✗ Invalid: {error}")
                return False
            
            # Check safety
            if not self.is_safe_url(url_str):
                print(f"  ✗ Unsafe URL")
                return False
            
            # Normalize and check for duplicates
            normalized = self.normalize_for_comparison(url_str)
            if normalized in self.visited:
                print(f"  ⊘ Already visited")
                return False
            
            # Add to queue
            self.to_visit.append(normalized)
            self.visited.add(normalized)
            print(f"  ✓ Added to queue")
            return True
            
        except Exception as e:
            print(f"  ✗ Error: {e}")
            return False
    
    def get_crawl_stats(self) -> dict:
        """Get crawling statistics."""
        return {
            'visited': len(self.visited),
            'pending': len(self.to_visit),
            'domains': len(set(URL(u).host for u in self.visited))
        }


class APIClient:
    """API client with URL building capabilities."""
    
    def __init__(self, base_url: str, api_key: str = ""):
        self.base = URL(base_url)
        self.api_key = api_key
        self.default_headers = {}
    
    def build_endpoint(self, *path_segments: str, **query_params) -> str:
        """Build API endpoint URL."""
        url = self.base.copy()
        
        # Append path segments
        for segment in path_segments:
            url.append_path(segment)
        
        # Add query params
        for key, value in query_params.items():
            url.set_param(key, value)
        
        # Add API key if configured
        if self.api_key:
            url.set_param('api_key', self.api_key)
        
        return url.to_string()
    
    def build_paginated_url(self, endpoint: str, page: int, per_page: int = 20) -> str:
        """Build paginated API URL."""
        return self.build_endpoint(endpoint, page=str(page), per_page=str(per_page))
    
    def build_filtered_url(self, endpoint: str, **filters) -> str:
        """Build filtered API URL."""
        return self.build_endpoint(endpoint, **filters)


class RedirectChainAnalyzer:
    """Analyze URL redirect chains."""
    
    def __init__(self):
        self.chains = []
    
    def analyze_redirect(self, start_url: str, redirect_urls: list) -> dict:
        """
        Analyze a redirect chain.
        
        Args:
            start_url: Initial URL
            redirect_urls: List of URLs in redirect chain
            
        Returns:
            Analysis dict with security info
        """
        if not redirect_urls:
            return {'error': 'No redirect URLs provided'}
        
        chain = [start_url] + redirect_urls
        analysis = {
            'chain_length': len(chain),
            'urls': [],
            'domain_changes': 0,
            'scheme_changes': 0,
            'security_issues': []
        }
        
        prev_url = None
        prev_domain = None
        prev_scheme = None
        
        for url_str in chain:
            try:
                url = URL(url_str)
                info = {
                    'url': url.to_string(),
                    'domain': url.host,
                    'scheme': url.scheme,
                    'is_secure': url.is_secure()
                }
                analysis['urls'].append(info)
                
                # Check for domain changes
                if prev_domain and url.host != prev_domain:
                    analysis['domain_changes'] += 1
                    analysis['security_issues'].append(
                        f"Domain change: {prev_domain} → {url.host}"
                    )
                
                # Check for scheme changes
                if prev_scheme and url.scheme != prev_scheme:
                    analysis['scheme_changes'] += 1
                    if prev_scheme == 'https' and url.scheme == 'http':
                        analysis['security_issues'].append(
                            f"⚠️ SECURITY: HTTPS downgraded to HTTP!"
                        )
                
                prev_domain = url.host
                prev_scheme = url.scheme
                
            except Exception as e:
                analysis['urls'].append({'url': url_str, 'error': str(e)})
        
        return analysis


def example_1_web_crawler():
    """Example 1: Web crawler URL management."""
    print("=" * 60)
    print("Example 1: Web Crawler URL Management")
    print("=" * 60)
    
    processor = URLProcessor('example.com')
    
    test_urls = [
        "https://example.com/page1",
        "https://example.com/page2",
        "https://sub.example.com/page3",
        "https://other.com/external",
        "javascript:alert(1)",
        "https://example.com/page1",  # Duplicate
        "https://example.com/page4#section",
        "https://example.com/page4",  # Same as above (different fragment)
    ]
    
    print("\nProcessing URLs:")
    for url in test_urls:
        print(f"\n{url[:50]}")
        processor.add_to_crawl_queue(url, "https://example.com/")
    
    print(f"\n📊 Crawl Stats: {processor.get_crawl_stats()}")
    print()


def example_2_api_client():
    """Example 2: API client URL building."""
    print("=" * 60)
    print("Example 2: API Client URL Building")
    print("=" * 60)
    
    client = APIClient(
        "https://api.github.com",
        api_key="ghp_xxxxxxxxxxxx"
    )
    
    print("\nBuilding API URLs:")
    
    # Simple endpoint
    url1 = client.build_endpoint("repos", "ayukyo", "alltoolkit")
    print(f"  Repo:      {url1}")
    
    # Paginated endpoint
    url2 = client.build_paginated_url("issues", page=2, per_page=50)
    print(f"  Issues:    {url2}")
    
    # Filtered endpoint
    url3 = client.build_filtered_url(
        "search/repositories",
        **{"q": "python", "sort": "stars", "order": "desc"}
    )
    print(f"  Search:    {url3}")
    print()


def example_3_redirect_analysis():
    """Example 3: Redirect chain analysis."""
    print("=" * 60)
    print("Example 3: Redirect Chain Analysis")
    print("=" * 60)
    
    analyzer = RedirectChainAnalyzer()
    
    # Simulated redirect chain
    start = "http://example.com"
    redirects = [
        "https://example.com",  # HTTP → HTTPS upgrade
        "https://www.example.com",  # Domain change (subdomain)
        "https://www.example.com/home",
    ]
    
    print(f"\nAnalyzing redirect chain:")
    print(f"  Start: {start}")
    print(f"  Redirects: {len(redirects)}")
    
    analysis = analyzer.analyze_redirect(start, redirects)
    
    print(f"\n📊 Analysis:")
    print(f"  Chain length:    {analysis['chain_length']}")
    print(f"  Domain changes:  {analysis['domain_changes']}")
    print(f"  Scheme changes:  {analysis['scheme_changes']}")
    
    if analysis['security_issues']:
        print(f"\n⚠️  Security Issues:")
        for issue in analysis['security_issues']:
            print(f"    - {issue}")
    
    print(f"\n📋 URL Chain:")
    for i, info in enumerate(analysis['urls']):
        secure = "🔒" if info.get('is_secure') else "⚠️"
        print(f"    {i}. {secure} {info.get('url', info.get('error'))}")
    print()


def example_4_url_shortener():
    """Example 4: URL shortener usage."""
    print("=" * 60)
    print("Example 4: URL Shortener")
    print("=" * 60)
    
    shortener = URLShortener()
    
    urls = [
        "https://example.com/very/long/path/that/needs/shortening/for/sharing",
        "https://example.com/another/long/url",
        "https://example.com/very/long/path/that/needs/shortening/for/sharing",  # Duplicate
    ]
    
    print("\nShortening URLs:")
    short_urls = []
    
    for url in urls:
        short = shortener.shorten(url)
        short_urls.append((url, short))
        print(f"  Original: {url[:60]}...")
        print(f"  Short:    {short}")
        print()
    
    print("Expanding URLs:")
    for original, short in short_urls:
        expanded = shortener.expand(short)
        match = "✓" if expanded == original else "✗"
        print(f"  {match} {short} → {expanded[:60]}...")
    print()


def example_5_security_validation():
    """Example 5: Security validation for user input."""
    print("=" * 60)
    print("Example 5: Security Validation")
    print("=" * 60)
    
    def safe_redirect(user_url: str, allowed_domains: list) -> str:
        """Safely validate and redirect."""
        try:
            # Sanitize
            url = sanitize_url(user_url, allowed_schemes=['http', 'https'])
            parsed = URL(url)
            
            # Check domain whitelist
            if parsed.host.lower() not in [d.lower() for d in allowed_domains]:
                raise URLValidationError(
                    f"Domain '{parsed.host}' not in allowed list"
                )
            
            # Check for auth info (potential credential leak)
            if parsed.has_auth():
                print(f"  ⚠️  Stripping auth info from URL")
                # Rebuild without auth
                safe_url = build_url(
                    scheme=parsed.scheme,
                    host=parsed.host,
                    port=parsed.port,
                    path=parsed.path,
                    query=parsed.query,
                    fragment=parsed.fragment
                )
                return safe_url
            
            return url
            
        except URLValidationError as e:
            print(f"  ✗ Blocked: {e}")
            return "https://example.com/"  # Safe default
    
    # Import build_url for this example
    from mod import build_url
    
    test_urls = [
        "https://allowed.com/page",
        "https://evil.com/malicious",
        "javascript:alert(1)",
        "https://user:pass@allowed.com/page",
        "https://ALLOWED.COM/page",  # Case variation
    ]
    
    allowed_domains = ["allowed.com", "trusted.org"]
    
    print(f"\nAllowed domains: {allowed_domains}\n")
    
    for url in test_urls:
        print(f"Input:  {url}")
        result = safe_redirect(url, allowed_domains)
        print(f"Output: {result}")
        print()


def example_6_url_deduplication():
    """Example 6: URL deduplication for large datasets."""
    print("=" * 60)
    print("Example 6: URL Deduplication")
    print("=" * 60)
    
    # Simulated URL dataset with duplicates
    raw_urls = [
        "https://Example.com/Page",
        "https://example.com/page",
        "https://example.com/page?utm_source=google",
        "https://example.com/page?utm_source=facebook",
        "https://example.com/page#section1",
        "https://example.com/page#section2",
        "HTTPS://EXAMPLE.COM/PAGE",
        "https://example.com:443/page",
    ]
    
    print(f"\nRaw URLs: {len(raw_urls)}")
    
    # Normalize and deduplicate
    normalized = set()
    for url_str in raw_urls:
        try:
            url = URL(url_str).normalize()
            # Remove tracking params and fragment for dedup
            url.fragment = ""
            url.query = {k: v for k, v in url.query.items() 
                        if not k.startswith('utm_')}
            normalized.add(url.to_string())
        except Exception:
            pass
    
    print(f"Normalized & Deduped: {len(normalized)}")
    print(f"Removed: {len(raw_urls) - len(normalized)} duplicates")
    
    print(f"\nUnique URLs:")
    for url in sorted(normalized):
        print(f"  • {url}")
    print()


def example_7_batch_processing():
    """Example 7: Batch URL processing."""
    print("=" * 60)
    print("Example 7: Batch URL Processing")
    print("=" * 60)
    
    # Simulated sitemap URLs
    sitemap_urls = [
        "https://example.com/",
        "https://example.com/about",
        "https://example.com/products",
        "https://example.com/products/item1",
        "https://example.com/products/item2",
        "https://example.com/blog",
        "https://example.com/blog/post1",
        "https://example.com/contact",
    ]
    
    print(f"\nProcessing {len(sitemap_urls)} URLs from sitemap\n")
    
    # Categorize URLs
    categories = {
        'root': [],
        'products': [],
        'blog': [],
        'other': []
    }
    
    for url_str in sitemap_urls:
        url = URL(url_str)
        path = url.path.lower()
        
        if path == '/':
            categories['root'].append(url_str)
        elif '/products' in path:
            categories['products'].append(url_str)
        elif '/blog' in path:
            categories['blog'].append(url_str)
        else:
            categories['other'].append(url_str)
    
    print("📁 Categorized URLs:")
    for category, urls in categories.items():
        print(f"\n  {category.upper()} ({len(urls)}):")
        for url in urls:
            print(f"    • {url}")
    
    # Generate summary
    print(f"\n📊 Summary:")
    print(f"  Total URLs:     {len(sitemap_urls)}")
    print(f"  Root pages:     {len(categories['root'])}")
    print(f"  Product pages:  {len(categories['products'])}")
    print(f"  Blog posts:     {len(categories['blog'])}")
    print(f"  Other pages:    {len(categories['other'])}")
    print()


def main():
    """Run all advanced examples."""
    print("\n" + "=" * 60)
    print("AllToolkit - Python URL Utilities - Advanced Examples")
    print("=" * 60 + "\n")
    
    example_1_web_crawler()
    example_2_api_client()
    example_3_redirect_analysis()
    example_4_url_shortener()
    example_5_security_validation()
    example_6_url_deduplication()
    example_7_batch_processing()
    
    print("=" * 60)
    print("All advanced examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()

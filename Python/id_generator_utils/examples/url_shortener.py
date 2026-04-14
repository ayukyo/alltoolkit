#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ID Generator Utilities - URL Shortener Example

This example shows how to use NanoID for URL shortening.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import NanoID, short_id


class URLShortener:
    """Simple URL shortener using NanoID."""
    
    def __init__(self, code_length: int = 7):
        """
        Initialize URL shortener.
        
        Args:
            code_length: Length of short codes (default 7)
                        7 chars = ~3.5 trillion possibilities
        """
        self.code_length = code_length
        self.url_map = {}  # code -> url
        self.stats = {}    # code -> click_count
    
    def shorten(self, url: str) -> str:
        """
        Create a short code for a URL.
        
        Args:
            url: Original URL
            
        Returns:
            Short code
        """
        # Generate unique code
        while True:
            code = NanoID.generate(
                length=self.code_length,
                alphabet='0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
            )
            if code not in self.url_map:
                break
        
        self.url_map[code] = url
        self.stats[code] = 0
        return code
    
    def expand(self, code: str) -> str:
        """
        Get the original URL for a code.
        
        Args:
            code: Short code
            
        Returns:
            Original URL or None
        """
        if code in self.url_map:
            self.stats[code] += 1
            return self.url_map[code]
        return None
    
    def get_stats(self, code: str) -> dict:
        """Get statistics for a short code."""
        if code not in self.url_map:
            return None
        return {
            'code': code,
            'url': self.url_map[code],
            'clicks': self.stats[code]
        }
    
    def list_all(self):
        """List all shortened URLs."""
        for code in sorted(self.url_map.keys()):
            print(f"  {code} -> {self.url_map[code]} ({self.stats[code]} clicks)")


def main():
    print("=" * 60)
    print("URL Shortener Example - Using NanoID")
    print("=" * 60)
    print()
    
    shortener = URLShortener(code_length=7)
    
    # Shorten some URLs
    urls = [
        'https://www.example.com/very/long/path/to/some/page',
        'https://github.com/user/repo/issues/12345',
        'https://docs.python.org/3/library/functions.html',
        'https://stackoverflow.com/questions/12345/some-question',
        'https://www.google.com/search?q=python+nanoid',
    ]
    
    print("Shortening URLs...")
    print("-" * 60)
    
    codes = []
    for url in urls:
        code = shortener.shorten(url)
        codes.append(code)
        print(f"  {url[:50]}...")
        print(f"    -> {code}")
        print()
    
    print("-" * 60)
    print("Simulating clicks...")
    print()
    
    # Simulate some clicks
    import random
    for _ in range(20):
        code = random.choice(codes)
        shortener.expand(code)
    
    print("Statistics:")
    print("-" * 60)
    shortener.list_all()
    
    print()
    print("Total URLs:", len(shortener.url_map))
    print("Total clicks:", sum(shortener.stats.values()))
    
    print()
    print("=" * 60)
    print("✓ URL Shortener example completed!")
    print("=" * 60)


if __name__ == '__main__':
    main()
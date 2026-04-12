"""
AllToolkit - Python URL Utilities

A zero-dependency, production-ready URL parsing and manipulation utility module.
Supports URL parsing, validation, normalization, query string handling, and path manipulation.
Built entirely with Python standard library.

Author: AllToolkit
License: MIT
"""

import re
from typing import Optional, Dict, List, Tuple, Any, Union
from urllib.parse import urlparse, urlunparse, parse_qs, urlencode, quote, unquote


class URLConfig:
    """Configuration for URL processing."""
    default_scheme: str = "https"
    max_url_length: int = 2048
    max_query_params: int = 100
    allowed_schemes: List[str] = None
    
    def __init__(self):
        self.allowed_schemes = ['http', 'https', 'ftp', 'ftps', 'mailto', 'tel', 'file']


class URLError(Exception):
    """Base exception for URL errors."""
    pass


class URLValidationError(URLError):
    """Raised when URL validation fails."""
    pass


class URLParseError(URLError):
    """Raised when URL parsing fails."""
    pass


class URL:
    """
    Comprehensive URL representation and manipulation.
    
    Provides methods for parsing, validating, normalizing, and manipulating URLs.
    """
    
    # URL component regex patterns
    SCHEME_PATTERN = re.compile(r'^[a-zA-Z][a-zA-Z0-9+.-]*$')
    DOMAIN_PATTERN = re.compile(
        r'^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+'
        r'(?:[a-zA-Z]{2,})$'
    )
    IPV4_PATTERN = re.compile(
        r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}'
        r'(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
    )
    IPV6_PATTERN = re.compile(r'^\[(?:[a-fA-F0-9:]+)\]$')
    PORT_PATTERN = re.compile(r'^[0-9]{1,5}$')
    
    # Common TLDs for validation
    COMMON_TLDS = {
        'com', 'org', 'net', 'edu', 'gov', 'mil', 'int',
        'cn', 'us', 'uk', 'de', 'fr', 'jp', 'au', 'ca',
        'io', 'ai', 'co', 'me', 'tv', 'info', 'biz', 'app', 'dev'
    }
    
    def __init__(
        self,
        url: str = "",
        scheme: str = "",
        host: str = "",
        port: Optional[int] = None,
        path: str = "/",
        query: Optional[Dict[str, Any]] = None,
        fragment: str = "",
        username: str = "",
        password: str = ""
    ):
        """
        Initialize URL from string or components.
        
        Args:
            url: Full URL string to parse (if provided, other args are ignored)
            scheme: URL scheme (http, https, etc.)
            host: Hostname or IP address
            port: Port number
            path: URL path
            query: Query parameters as dict
            fragment: URL fragment (#...)
            username: Username for auth
            password: Password for auth
        """
        self._config = URLConfig()
        
        if url:
            self._parse(url)
        else:
            self.scheme = scheme or self._config.default_scheme
            self.host = host
            self.port = port
            self.path = path or "/"
            self.query = query or {}
            self.fragment = fragment
            self.username = username
            self.password = password
        
        self._validate()
    
    def _parse(self, url: str) -> None:
        """Parse URL string into components."""
        if len(url) > self._config.max_url_length:
            raise URLParseError(f"URL exceeds maximum length of {self._config.max_url_length}")
        
        parsed = urlparse(url)
        
        self.scheme = parsed.scheme.lower()
        self.host = parsed.hostname or ""
        
        # Handle port parsing with error handling
        try:
            self.port = parsed.port
        except ValueError:
            # Port out of range - will be caught in validation
            self.port = None
            # Extract port manually for validation
            if ':' in parsed.netloc:
                port_part = parsed.netloc.split(':')[-1]
                try:
                    self.port = int(port_part.split(']')[0] if ']' in port_part else port_part)
                except ValueError:
                    pass
        
        self.path = parsed.path or "/"
        self.fragment = parsed.fragment or ""
        self.username = parsed.username or ""
        self.password = parsed.password or ""
        
        # Parse query string
        query_dict = parse_qs(parsed.query, keep_blank_values=True)
        self.query = {}
        for key, values in query_dict.items():
            if len(values) == 1:
                self.query[key] = values[0]
            else:
                self.query[key] = values
    
    def _validate(self) -> None:
        """Validate URL components."""
        if not self.SCHEME_PATTERN.match(self.scheme):
            raise URLValidationError(f"Invalid scheme: {self.scheme}")
        
        if self.scheme not in self._config.allowed_schemes:
            raise URLValidationError(f"Scheme '{self.scheme}' not in allowed list")
        
        if self.host:
            if not (self._is_valid_domain(self.host) or 
                    self._is_valid_ipv4(self.host) or 
                    self._is_valid_ipv6(self.host)):
                raise URLValidationError(f"Invalid host: {self.host}")
        
        if self.port is not None:
            if not (1 <= self.port <= 65535):
                raise URLValidationError(f"Port out of range: {self.port}")
    
    def _is_valid_domain(self, host: str) -> bool:
        """Check if host is a valid domain name."""
        if self.DOMAIN_PATTERN.match(host):
            tld = host.split('.')[-1].lower()
            return tld in self.COMMON_TLDS or len(tld) >= 2
        return False
    
    def _is_valid_ipv4(self, host: str) -> bool:
        """Check if host is a valid IPv4 address."""
        return bool(self.IPV4_PATTERN.match(host))
    
    def _is_valid_ipv6(self, host: str) -> bool:
        """Check if host is a valid IPv6 address (with or without brackets)."""
        # urlparse strips brackets, so check both formats
        if self.IPV6_PATTERN.match(host):
            return True
        # Check without brackets
        return bool(re.match(r'^[a-fA-F0-9:]+$', host) and ':' in host)
    
    def __str__(self) -> str:
        """Return full URL string."""
        return self.to_string()
    
    def __repr__(self) -> str:
        return f"URL('{self.to_string()}')"
    
    def to_string(self, include_auth: bool = False) -> str:
        """
        Convert URL to string.
        
        Args:
            include_auth: Whether to include username/password in output
            
        Returns:
            Full URL string
        """
        netloc = self.host
        
        if include_auth and self.username:
            if self.password:
                netloc = f"{self.username}:{self.password}@{netloc}"
            else:
                netloc = f"{self.username}@{netloc}"
        
        if self.port and self._is_default_port():
            pass  # Don't include default ports
        elif self.port:
            netloc = f"{netloc}:{self.port}"
        
        query_string = urlencode(self.query, doseq=True) if self.query else ""
        
        return urlunparse((
            self.scheme,
            netloc,
            self.path,
            "",  # params
            query_string,
            self.fragment
        ))
    
    def _is_default_port(self) -> bool:
        """Check if port is the default for the scheme."""
        default_ports = {'http': 80, 'https': 443, 'ftp': 21, 'ftps': 990}
        return self.port == default_ports.get(self.scheme)
    
    def normalize(self) -> 'URL':
        """
        Normalize URL by applying standard transformations.
        
        - Lowercase scheme and host
        - Remove default ports
        - Decode unreserved characters in path
        - Remove trailing slash from path (unless root)
        - Sort query parameters
        
        Returns:
            New normalized URL instance
        """
        normalized = URL()
        normalized.scheme = self.scheme.lower()
        normalized.host = self.host.lower()
        normalized.port = None if self._is_default_port() else self.port
        normalized.path = self._normalize_path(self.path)
        normalized.fragment = self.fragment
        normalized.username = self.username
        normalized.password = self.password
        
        # Sort query params
        normalized.query = dict(sorted(self.query.items()))
        
        return normalized
    
    def _normalize_path(self, path: str) -> str:
        """Normalize URL path."""
        if not path:
            return "/"
        
        # Decode unreserved characters (Python 3.6 compatible)
        try:
            path = unquote(path)
        except TypeError:
            # Fallback for older Python versions
            path = unquote(path.replace("+", "%2B"))
        
        # Remove trailing slash unless root
        if path != "/" and path.endswith("/"):
            path = path.rstrip("/")
        
        # Resolve . and ..
        segments = path.split("/")
        resolved = []
        for segment in segments:
            if segment == "..":
                if resolved and resolved[-1] != "":
                    resolved.pop()
            elif segment != ".":
                resolved.append(segment)
        
        result = "/".join(resolved)
        return result if result.startswith("/") else "/" + result
    
    def get_origin(self) -> str:
        """Get origin (scheme + host + port)."""
        port_str = f":{self.port}" if self.port and not self._is_default_port() else ""
        return f"{self.scheme}://{self.host}{port_str}"
    
    def get_base_url(self) -> str:
        """Get base URL (origin + path without query/fragment)."""
        return f"{self.get_origin()}{self.path}"
    
    # Query parameter methods
    
    def get_param(self, name: str, default: Any = None) -> Any:
        """Get query parameter value."""
        return self.query.get(name, default)
    
    def set_param(self, name: str, value: Any) -> 'URL':
        """Set query parameter. Returns self for chaining."""
        self.query[name] = value
        return self
    
    def remove_param(self, name: str) -> 'URL':
        """Remove query parameter. Returns self for chaining."""
        self.query.pop(name, None)
        return self
    
    def has_param(self, name: str) -> bool:
        """Check if query parameter exists."""
        return name in self.query
    
    def get_params(self) -> Dict[str, Any]:
        """Get all query parameters."""
        return dict(self.query)
    
    # Path manipulation
    
    def get_path_segments(self) -> List[str]:
        """Get path as list of segments."""
        segments = self.path.strip("/").split("/")
        return [s for s in segments if s]
    
    def set_path(self, path: str) -> 'URL':
        """Set URL path. Returns self for chaining."""
        if not path.startswith("/"):
            path = "/" + path
        self.path = path
        return self
    
    def append_path(self, segment: str) -> 'URL':
        """Append segment to path. Returns self for chaining."""
        segment = segment.strip("/")
        if self.path.endswith("/"):
            self.path += segment
        else:
            self.path += "/" + segment
        return self
    
    def get_parent_path(self) -> str:
        """Get parent path."""
        segments = self.get_path_segments()
        if len(segments) <= 1:
            return "/"
        return "/" + "/".join(segments[:-1])
    
    # Validation
    
    def is_secure(self) -> bool:
        """Check if URL uses HTTPS."""
        return self.scheme == "https"
    
    def is_absolute(self) -> bool:
        """Check if URL is absolute (has scheme and host)."""
        return bool(self.scheme and self.host)
    
    def is_relative(self) -> bool:
        """Check if URL is relative (no scheme/host)."""
        return not self.is_absolute()
    
    def has_query(self) -> bool:
        """Check if URL has query parameters."""
        return bool(self.query)
    
    def has_fragment(self) -> bool:
        """Check if URL has fragment."""
        return bool(self.fragment)
    
    def has_auth(self) -> bool:
        """Check if URL has authentication."""
        return bool(self.username)
    
    # Comparison
    
    def same_origin(self, other: 'URL') -> bool:
        """Check if two URLs have the same origin."""
        return (
            self.scheme == other.scheme and
            self.host == other.host and
            self.port == other.port
        )
    
    def equals(self, other: 'URL', ignore_fragment: bool = False, ignore_query: bool = False) -> bool:
        """
        Check if URLs are equal.
        
        Args:
            ignore_fragment: Ignore fragment in comparison
            ignore_query: Ignore query params in comparison
        """
        if self.scheme != other.scheme or self.host != other.host or self.port != other.port:
            return False
        
        if self.path != other.path:
            return False
        
        if not ignore_query and self.query != other.query:
            return False
        
        if not ignore_fragment and self.fragment != other.fragment:
            return False
        
        return True
    
    # Utility
    
    def copy(self) -> 'URL':
        """Create a copy of this URL."""
        return URL(self.to_string())


# Convenience functions

def parse_url(url: str) -> URL:
    """Parse URL string into URL object."""
    return URL(url)


def validate_url(url: str) -> Tuple[bool, Optional[str]]:
    """
    Validate URL string.
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        URL(url)
        return True, None
    except URLError as e:
        return False, str(e)


def is_valid_url(url: str) -> bool:
    """Quick URL validation check."""
    valid, _ = validate_url(url)
    return valid


def normalize_url(url: str) -> str:
    """Normalize URL string."""
    return URL(url).normalize().to_string()


def extract_domain(url: str) -> str:
    """Extract domain from URL."""
    return URL(url).host


def extract_path(url: str) -> str:
    """Extract path from URL."""
    return URL(url).path


def extract_query_params(url: str) -> Dict[str, Any]:
    """Extract query parameters from URL."""
    return URL(url).query


def build_url(
    scheme: str = "https",
    host: str = "",
    port: Optional[int] = None,
    path: str = "/",
    query: Optional[Dict[str, Any]] = None,
    fragment: str = ""
) -> str:
    """Build URL string from components."""
    url = URL(scheme=scheme, host=host, port=port, path=path, query=query, fragment=fragment)
    return url.to_string()


def join_url(base: str, relative: str) -> str:
    """
    Join base URL with relative URL.
    
    Args:
        base: Base URL
        relative: Relative URL or path
        
    Returns:
        Joined absolute URL
    """
    base_url = URL(base)
    
    # If relative is absolute, return it
    if relative.startswith("http://") or relative.startswith("https://"):
        return relative
    
    # Handle relative path
    if relative.startswith("/"):
        base_url.path = relative
    else:
        # Append to current path
        current_path = base_url.path
        if current_path.endswith("/"):
            base_url.path = current_path + relative
        else:
            base_url.path = current_path + "/" + relative
    
    return base_url.to_string()


def sanitize_url(url: str, allowed_schemes: Optional[List[str]] = None) -> str:
    """
    Sanitize URL for safe use.
    
    - Removes dangerous schemes (javascript:, data:, etc.)
    - Encodes special characters
    - Validates structure
    
    Args:
        url: URL to sanitize
        allowed_schemes: List of allowed schemes (default: http, https)
        
    Returns:
        Sanitized URL string
        
    Raises:
        URLValidationError: If URL is not safe
    """
    allowed = allowed_schemes or ['http', 'https']
    
    try:
        parsed = URL(url)
        
        if parsed.scheme not in allowed:
            raise URLValidationError(f"Scheme '{parsed.scheme}' not allowed")
        
        # Re-encode to ensure safety
        return parsed.normalize().to_string()
        
    except URLError as e:
        raise URLValidationError(f"Unsafe URL: {e}")


def get_url_info(url: str) -> Dict[str, Any]:
    """
    Get comprehensive URL information.
    
    Returns:
        Dict with scheme, host, port, path, query, fragment, origin, etc.
    """
    parsed = URL(url)
    return {
        'url': parsed.to_string(),
        'scheme': parsed.scheme,
        'host': parsed.host,
        'port': parsed.port,
        'path': parsed.path,
        'query': parsed.query,
        'fragment': parsed.fragment,
        'username': parsed.username or None,
        'origin': parsed.get_origin(),
        'base_url': parsed.get_base_url(),
        'is_secure': parsed.is_secure(),
        'is_absolute': parsed.is_absolute(),
        'has_auth': parsed.has_auth(),
        'path_segments': parsed.get_path_segments()
    }


# URL shortening simulation (for demo purposes)

class URLShortener:
    """Simple in-memory URL shortener for demonstration."""
    
    def __init__(self):
        self._urls: Dict[str, str] = {}
        self._counter = 0
        self._base = "https://short.url/"
    
    def shorten(self, url: str) -> str:
        """Shorten a URL."""
        if not is_valid_url(url):
            raise URLValidationError("Invalid URL")
        
        # Check if already shortened
        for short, long in self._urls.items():
            if long == url:
                return short
        
        # Create new short URL
        self._counter += 1
        short_code = self._encode(self._counter)
        short_url = f"{self._base}{short_code}"
        self._urls[short_url] = url
        
        return short_url
    
    def expand(self, short_url: str) -> str:
        """Expand a short URL."""
        if short_url not in self._urls:
            raise URLError("Short URL not found")
        return self._urls[short_url]
    
    def _encode(self, num: int) -> str:
        """Encode number to base62 string."""
        alphabet = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        if num == 0:
            return alphabet[0]
        
        result = []
        while num > 0:
            result.append(alphabet[num % 62])
            num //= 62
        
        return ''.join(reversed(result))


# Module exports
__all__ = [
    'URL',
    'URLConfig',
    'URLError',
    'URLValidationError',
    'URLParseError',
    'URLShortener',
    'parse_url',
    'validate_url',
    'is_valid_url',
    'normalize_url',
    'extract_domain',
    'extract_path',
    'extract_query_params',
    'build_url',
    'join_url',
    'sanitize_url',
    'get_url_info',
]

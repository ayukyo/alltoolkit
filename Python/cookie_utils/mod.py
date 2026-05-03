"""
Cookie Utilities - HTTP Cookie parsing and management.

Zero-dependency HTTP cookie handling with full RFC 6265 compliance.
Supports parsing, formatting, jar management, validation, and matching.

Features:
- Parse Set-Cookie and Cookie headers
- Cookie jar with expiration and domain/path matching
- HttpOnly, Secure, SameSite attribute support
- Cookie validation and serialization
- URL-based cookie filtering
"""

import re
import time
from dataclasses import dataclass, field
from typing import Optional, Dict, List, Any
from urllib.parse import urlparse


@dataclass
class Cookie:
    """
    Represents an HTTP Cookie with all standard attributes.
    
    Attributes:
        name: Cookie name
        value: Cookie value
        domain: Domain scope (e.g., ".example.com")
        path: Path scope (e.g., "/")
        expires: Expiration timestamp (Unix epoch)
        max_age: Max-Age in seconds (alternative to expires)
        secure: Only send over HTTPS
        http_only: Not accessible via JavaScript
        same_site: SameSite attribute ("Strict", "Lax", "None")
        creation_time: When the cookie was created
        last_access_time: When the cookie was last accessed
        persistent: Whether the cookie is persistent
        host_only: Whether the cookie is host-only
    """
    name: str
    value: str
    domain: str = ""
    path: str = "/"
    expires: Optional[float] = None
    max_age: Optional[int] = None
    secure: bool = False
    http_only: bool = False
    same_site: Optional[str] = None
    creation_time: float = field(default_factory=time.time)
    last_access_time: float = field(default_factory=time.time)
    persistent: bool = False
    host_only: bool = True
    
    def __post_init__(self):
        """Normalize attributes after initialization."""
        if self.domain and self.domain.startswith('.'):
            self.domain = self.domain[1:]
        if not self.path:
            self.path = "/"
        if self.max_age is not None:
            self.expires = time.time() + self.max_age
            self.persistent = True
        elif self.expires is not None:
            self.persistent = True
    
    def is_expired(self) -> bool:
        """Check if the cookie has expired."""
        if self.expires is None:
            return False
        return time.time() > self.expires
    
    def matches(self, url: str) -> bool:
        """
        Check if this cookie matches a given URL.
        
        Args:
            url: The URL to match against
            
        Returns:
            True if the cookie should be sent to this URL
        """
        if self.is_expired():
            return False
        
        parsed = urlparse(url)
        host = parsed.hostname or ""
        path = parsed.path or "/"
        
        # Check secure flag
        if self.secure and parsed.scheme != "https":
            return False
        
        # Check domain
        if not self._domain_match(host):
            return False
        
        # Check path
        if not self._path_match(path):
            return False
        
        return True
    
    def _domain_match(self, host: str) -> bool:
        """Check if the host matches the cookie's domain."""
        if not self.domain:
            return host == ""
        
        cookie_domain = self.domain.lower()
        host_lower = host.lower()
        
        if self.host_only:
            return host_lower == cookie_domain
        
        # Domain match: host equals domain or is a subdomain
        if host_lower == cookie_domain:
            return True
        if host_lower.endswith('.' + cookie_domain):
            return True
        return False
    
    def _path_match(self, path: str) -> bool:
        """Check if the path matches the cookie's path."""
        if not self.path or self.path == "/":
            return True
        if path == self.path:
            return True
        if path.startswith(self.path):
            if self.path.endswith('/'):
                return True
            if len(path) > len(self.path) and path[len(self.path)] == '/':
                return True
        return False
    
    def to_header(self) -> str:
        """Convert to Cookie header format (name=value)."""
        return f"{self.name}={self.value}"
    
    def to_set_cookie(self) -> str:
        """Convert to Set-Cookie header format."""
        parts = [f"{self.name}={self.value}"]
        
        if self.domain:
            parts.append(f"Domain={self.domain}")
        
        if self.path and self.path != "/":
            parts.append(f"Path={self.path}")
        
        if self.expires is not None:
            from email.utils import formatdate
            parts.append(f"Expires={formatdate(self.expires, usegmt=True)}")
        
        if self.max_age is not None:
            parts.append(f"Max-Age={self.max_age}")
        
        if self.secure:
            parts.append("Secure")
        
        if self.http_only:
            parts.append("HttpOnly")
        
        if self.same_site:
            parts.append(f"SameSite={self.same_site}")
        
        return "; ".join(parts)
    
    def update_access_time(self) -> None:
        """Update the last access time."""
        self.last_access_time = time.time()
    
    def copy(self) -> "Cookie":
        """Create a copy of this cookie."""
        return Cookie(
            name=self.name,
            value=self.value,
            domain=self.domain,
            path=self.path,
            expires=self.expires,
            max_age=self.max_age,
            secure=self.secure,
            http_only=self.http_only,
            same_site=self.same_site,
            creation_time=self.creation_time,
            last_access_time=self.last_access_time,
            persistent=self.persistent,
            host_only=self.host_only,
        )


def parse_set_cookie(header: str) -> Optional[Cookie]:
    """
    Parse a Set-Cookie header into a Cookie object.
    
    Args:
        header: The Set-Cookie header value
        
    Returns:
        Cookie object or None if parsing fails
    """
    if not header or '=' not in header:
        return None
    
    # Split name=value from attributes
    parts = header.split(';')
    name_value = parts[0].strip()
    
    if '=' not in name_value:
        return None
    
    eq_pos = name_value.index('=')
    name = name_value[:eq_pos].strip()
    value = name_value[eq_pos + 1:].strip()
    
    # Remove quotes from value if present
    if value.startswith('"') and value.endswith('"'):
        value = value[1:-1]
    
    cookie = Cookie(name=name, value=value)
    
    # Parse attributes
    for part in parts[1:]:
        part = part.strip()
        if '=' in part:
            attr_name, attr_value = part.split('=', 1)
            attr_name = attr_name.strip().lower()
            attr_value = attr_value.strip()
        else:
            attr_name = part.lower()
            attr_value = ""
        
        if attr_name == "domain":
            cookie.domain = attr_value.lstrip('.')
            cookie.host_only = False
        elif attr_name == "path":
            cookie.path = attr_value or "/"
        elif attr_name == "expires":
            cookie.expires = _parse_expires(attr_value)
            if cookie.expires:
                cookie.persistent = True
        elif attr_name == "max-age":
            try:
                cookie.max_age = int(attr_value)
                if cookie.max_age > 0:
                    cookie.expires = time.time() + cookie.max_age
                    cookie.persistent = True
            except ValueError:
                pass
        elif attr_name == "secure":
            cookie.secure = True
        elif attr_name == "httponly":
            cookie.http_only = True
        elif attr_name == "samesite":
            cookie.same_site = attr_value.capitalize()
            if cookie.same_site not in ("Strict", "Lax", "None"):
                cookie.same_site = "Lax"  # Default to Lax
    
    return cookie


def _parse_expires(date_str: str) -> Optional[float]:
    """
    Parse an Expires date string into a Unix timestamp.
    
    Supports multiple date formats:
    - RFC 1123: Wed, 09 Jun 2021 10:18:14 GMT
    - RFC 850: Wednesday, 09-Jun-21 10:18:14 GMT
    - ANSI C: Wed Jun 09 10:18:14 2021
    """
    from email.utils import parsedate_to_datetime
    
    try:
        dt = parsedate_to_datetime(date_str)
        return dt.timestamp()
    except (ValueError, TypeError):
        pass
    
    # Try common formats
    formats = [
        "%a, %d %b %Y %H:%M:%S %Z",
        "%a, %d-%b-%Y %H:%M:%S %Z",
        "%a, %d-%b-%y %H:%M:%S %Z",
        "%A, %d-%b-%y %H:%M:%S %Z",
        "%a, %d %b %y %H:%M:%S %Z",
        "%d %b %Y %H:%M:%S %Z",
    ]
    
    for fmt in formats:
        try:
            dt = time.strptime(date_str.strip(), fmt)
            return time.mktime(dt)
        except ValueError:
            continue
    
    return None


def parse_cookie_header(header: str) -> Dict[str, str]:
    """
    Parse a Cookie header into a dictionary.
    
    Args:
        header: The Cookie header value
        
    Returns:
        Dictionary of cookie name-value pairs
    """
    cookies = {}
    
    if not header:
        return cookies
    
    for part in header.split(';'):
        part = part.strip()
        if '=' in part:
            name, value = part.split('=', 1)
            cookies[name.strip()] = value.strip()
    
    return cookies


def build_cookie_header(cookies: Dict[str, str]) -> str:
    """
    Build a Cookie header from a dictionary.
    
    Args:
        cookies: Dictionary of cookie name-value pairs
        
    Returns:
        Cookie header string
    """
    return "; ".join(f"{name}={value}" for name, value in cookies.items())


class CookieJar:
    """
    A cookie jar for storing and managing cookies.
    
    Supports:
    - Adding and removing cookies
    - Domain and path matching
    - Expiration handling
    - URL-based cookie retrieval
    - Serialization and deserialization
    """
    
    def __init__(self):
        """Initialize an empty cookie jar."""
        self._cookies: List[Cookie] = []
    
    def add(self, cookie: Cookie) -> None:
        """
        Add a cookie to the jar.
        
        If a cookie with the same name, domain, and path exists,
        it will be replaced.
        
        Args:
            cookie: The cookie to add
        """
        # Remove existing cookie with same key
        self._cookies = [
            c for c in self._cookies
            if not (c.name == cookie.name and 
                    c.domain == cookie.domain and 
                    c.path == cookie.path)
        ]
        
        # Don't add expired cookies
        if not cookie.is_expired():
            self._cookies.append(cookie)
    
    def get(self, name: str, domain: str = "", path: str = "") -> Optional[Cookie]:
        """
        Get a cookie by name, optionally filtered by domain and path.
        
        Args:
            name: Cookie name
            domain: Optional domain filter
            path: Optional path filter
            
        Returns:
            The cookie or None if not found
        """
        for cookie in self._cookies:
            if cookie.name == name:
                if domain and not cookie._domain_match(domain):
                    continue
                if path and not cookie._path_match(path):
                    continue
                if cookie.is_expired():
                    continue
                cookie.update_access_time()
                return cookie
        return None
    
    def get_all(self) -> List[Cookie]:
        """
        Get all non-expired cookies.
        
        Returns:
            List of all valid cookies
        """
        self._remove_expired()
        return [c for c in self._cookies if not c.is_expired()]
    
    def get_for_url(self, url: str, http_only: Optional[bool] = None) -> List[Cookie]:
        """
        Get all cookies that should be sent to a URL.
        
        Args:
            url: The target URL
            http_only: If True, only HttpOnly cookies; if False, no HttpOnly
            
        Returns:
            List of matching cookies
        """
        self._remove_expired()
        matching = []
        
        for cookie in self._cookies:
            if cookie.matches(url):
                if http_only is not None and cookie.http_only != http_only:
                    continue
                cookie.update_access_time()
                matching.append(cookie)
        
        # Sort by path length (longest first) for proper ordering
        matching.sort(key=lambda c: len(c.path), reverse=True)
        
        return matching
    
    def get_cookie_header(self, url: str) -> str:
        """
        Build a Cookie header for a URL.
        
        Args:
            url: The target URL
            
        Returns:
            Cookie header string
        """
        cookies = self.get_for_url(url, http_only=False)
        return "; ".join(c.to_header() for c in cookies)
    
    def remove(self, name: str, domain: str = "", path: str = "") -> bool:
        """
        Remove a cookie from the jar.
        
        Args:
            name: Cookie name
            domain: Optional domain filter
            path: Optional path filter
            
        Returns:
            True if a cookie was removed
        """
        original_count = len(self._cookies)
        self._cookies = [
            c for c in self._cookies
            if not (c.name == name and
                    (not domain or c.domain == domain) and
                    (not path or c.path == path))
        ]
        return len(self._cookies) < original_count
    
    def clear(self) -> None:
        """Remove all cookies from the jar."""
        self._cookies.clear()
    
    def clear_expired(self) -> int:
        """
        Remove all expired cookies.
        
        Returns:
            Number of cookies removed
        """
        return self._remove_expired()
    
    def _remove_expired(self) -> int:
        """Remove expired cookies and return count."""
        original_count = len(self._cookies)
        self._cookies = [c for c in self._cookies if not c.is_expired()]
        return original_count - len(self._cookies)
    
    def count(self) -> int:
        """Return the number of non-expired cookies."""
        self._remove_expired()
        return len(self._cookies)
    
    def __len__(self) -> int:
        """Return the number of non-expired cookies."""
        return self.count()
    
    def __contains__(self, name: str) -> bool:
        """Check if a cookie with the given name exists."""
        return self.get(name) is not None
    
    def __iter__(self):
        """Iterate over non-expired cookies."""
        return iter(self.get_all())
    
    def to_dict(self) -> List[Dict[str, Any]]:
        """
        Serialize the jar to a list of dictionaries.
        
        Returns:
            List of cookie dictionaries
        """
        return [
            {
                "name": c.name,
                "value": c.value,
                "domain": c.domain,
                "path": c.path,
                "expires": c.expires,
                "max_age": c.max_age,
                "secure": c.secure,
                "http_only": c.http_only,
                "same_site": c.same_site,
            }
            for c in self._cookies
            if not c.is_expired()
        ]
    
    @classmethod
    def from_dict(cls, data: List[Dict[str, Any]]) -> "CookieJar":
        """
        Create a CookieJar from a list of dictionaries.
        
        Args:
            data: List of cookie dictionaries
            
        Returns:
            A new CookieJar instance
        """
        jar = cls()
        for item in data:
            cookie = Cookie(
                name=item.get("name", ""),
                value=item.get("value", ""),
                domain=item.get("domain", ""),
                path=item.get("path", "/"),
                expires=item.get("expires"),
                max_age=item.get("max_age"),
                secure=item.get("secure", False),
                http_only=item.get("http_only", False),
                same_site=item.get("same_site"),
            )
            jar.add(cookie)
        return jar
    
    def update_from_headers(self, headers: List[str]) -> int:
        """
        Update the jar from Set-Cookie headers.
        
        Args:
            headers: List of Set-Cookie header values
            
        Returns:
            Number of cookies added
        """
        count = 0
        for header in headers:
            cookie = parse_set_cookie(header)
            if cookie and not cookie.is_expired():
                self.add(cookie)
                count += 1
        return count


def validate_cookie_name(name: str) -> bool:
    """
    Validate a cookie name according to RFC 6265.
    
    Cookie names must be ASCII and cannot contain:
    Control characters, space, tab, or: ()<>@,;:\"/[]?={}
    
    Args:
        name: The cookie name to validate
        
    Returns:
        True if the name is valid
    """
    if not name:
        return False
    
    # Invalid characters in cookie names
    invalid_chars = set('()<>@,;:"/[]?={} \t')
    
    for char in name:
        if ord(char) < 32 or ord(char) > 126:
            return False
        if char in invalid_chars:
            return False
    
    return True


def validate_cookie_value(value: str) -> bool:
    """
    Validate a cookie value according to RFC 6265.
    
    Cookie values can contain ASCII characters except:
    Control characters, space, tab, comma, semicolon, double quote
    
    Args:
        value: The cookie value to validate
        
    Returns:
        True if the value is valid
    """
    if not value:
        return True  # Empty values are allowed
    
    for char in value:
        if ord(char) < 32 or ord(char) > 126:
            return False
        if char in ' ";,':
            return False
    
    return True


def encode_cookie_value(value: str) -> str:
    """
    Encode a value for safe use in cookies using Base64.
    
    Args:
        value: The value to encode
        
    Returns:
        Base64-encoded value safe for cookies
    """
    import base64
    return base64.b64encode(value.encode('utf-8')).decode('ascii')


def decode_cookie_value(encoded: str) -> str:
    """
    Decode a Base64-encoded cookie value.
    
    Args:
        encoded: The Base64-encoded value
        
    Returns:
        The decoded value
    """
    import base64
    return base64.b64decode(encoded.encode('ascii')).decode('utf-8')


def same_site_matches(same_site: Optional[str], from_site: str, to_site: str, 
                       is_secure: bool) -> bool:
    """
    Check if a cookie's SameSite policy allows sending to a target site.
    
    Args:
        same_site: The cookie's SameSite value ("Strict", "Lax", "None", None)
        from_site: The origin site (e.g., "example.com")
        to_site: The target site (e.g., "other.com")
        is_secure: Whether the request is over HTTPS
        
    Returns:
        True if the cookie can be sent
    """
    # No SameSite = default Lax behavior
    if same_site is None or same_site == "Lax":
        # Lax allows same-site and top-level navigations
        return from_site == to_site or is_secure
    
    if same_site == "Strict":
        # Strict only allows same-site requests
        return from_site == to_site
    
    if same_site == "None":
        # None allows cross-site, but requires Secure
        return is_secure
    
    return True


# Convenience functions

def make_session_cookie(name: str, value: str, path: str = "/", 
                        secure: bool = False, http_only: bool = True,
                        same_site: str = "Lax") -> Cookie:
    """
    Create a session cookie (no expiration).
    
    Args:
        name: Cookie name
        value: Cookie value
        path: Cookie path
        secure: Secure flag
        http_only: HttpOnly flag
        same_site: SameSite value
        
    Returns:
        A new Cookie object
    """
    return Cookie(
        name=name,
        value=value,
        path=path,
        secure=secure,
        http_only=http_only,
        same_site=same_site,
        persistent=False,
    )


def make_persistent_cookie(name: str, value: str, max_age: int,
                          domain: str = "", path: str = "/",
                          secure: bool = False, http_only: bool = True,
                          same_site: str = "Lax") -> Cookie:
    """
    Create a persistent cookie with expiration.
    
    Args:
        name: Cookie name
        value: Cookie value
        max_age: Cookie lifetime in seconds
        domain: Cookie domain
        path: Cookie path
        secure: Secure flag
        http_only: HttpOnly flag
        same_site: SameSite value
        
    Returns:
        A new Cookie object
    """
    return Cookie(
        name=name,
        value=value,
        domain=domain,
        path=path,
        max_age=max_age,
        secure=secure,
        http_only=http_only,
        same_site=same_site,
        persistent=True,
    )
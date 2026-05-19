"""
URL Utilities - A comprehensive URL parsing, building, and manipulation library.

Features:
- Parse URLs into components (scheme, host, port, path, query, fragment)
- Build URLs from components
- Query string parsing and building (with proper encoding/decoding)
- URL joining and resolution
- URL normalization and canonicalization
- Domain extraction and validation
- URL safety checks
- Zero external dependencies

Author: AllToolkit
"""

import re
from typing import Dict, List, Optional, Tuple, Union
from urllib.parse import (
    quote,
    unquote,
    urlencode,
    parse_qs,
    parse_qsl,
    urlparse,
    urlunparse,
    urljoin,
    ParseResult,
)
from dataclasses import dataclass
from ipaddress import ip_address, IPv4Address, IPv6Address
import string


# ============================================================================
# URL Components Dataclass
# ============================================================================

@dataclass
class URLInfo:
    """Structured URL information."""
    scheme: str
    username: Optional[str]
    password: Optional[str]
    host: str
    port: Optional[int]
    path: str
    query: Dict[str, List[str]]
    fragment: str
    
    def __str__(self) -> str:
        return build_url(
            scheme=self.scheme,
            host=self.host,
            port=self.port,
            path=self.path,
            query=self.query,
            fragment=self.fragment,
            username=self.username,
            password=self.password,
        )
    
    @property
    def netloc(self) -> str:
        """Get the network location (host:port)."""
        if self.port:
            return f"{self.host}:{self.port}"
        return self.host
    
    @property
    def origin(self) -> str:
        """Get the origin (scheme://host:port)."""
        if self.port:
            return f"{self.scheme}://{self.host}:{self.port}"
        return f"{self.scheme}://{self.host}"
    
    @property
    def is_secure(self) -> bool:
        """Check if the URL uses a secure scheme."""
        return self.scheme.lower() in ('https', 'wss', 'sftp')


# ============================================================================
# URL Parsing
# ============================================================================

def parse_url(url: str) -> URLInfo:
    """
    Parse a URL into its components.
    
    Args:
        url: The URL string to parse
        
    Returns:
        URLInfo object with all components
        
    Examples:
        >>> info = parse_url("https://user:pass@example.com:8080/path?q=1#frag")
        >>> info.scheme
        'https'
        >>> info.host
        'example.com'
        >>> info.port
        8080
    """
    parsed = urlparse(url)
    
    # Parse query string
    query_dict = parse_qs(parsed.query, keep_blank_values=True)
    
    # Extract port from netloc if not explicitly parsed
    port = parsed.port
    
    # Handle host extraction
    host = parsed.hostname or ''
    
    return URLInfo(
        scheme=parsed.scheme or '',
        username=parsed.username,
        password=parsed.password,
        host=host,
        port=port,
        path=parsed.path or '',
        query=query_dict,
        fragment=parsed.fragment or '',
    )


def parse_query_string(query_string: str, keep_blank: bool = True) -> Dict[str, List[str]]:
    """
    Parse a query string into a dictionary.
    
    Args:
        query_string: The query string (with or without leading ?)
        keep_blank: Whether to keep parameters with empty values
        
    Returns:
        Dictionary with parameter names as keys and lists of values
        
    Examples:
        >>> parse_query_string("a=1&b=2&a=3")
        {'a': ['1', '3'], 'b': ['2']}
    """
    # Remove leading ? if present
    if query_string.startswith('?'):
        query_string = query_string[1:]
    
    if not query_string:
        return {}
    
    result = parse_qs(query_string, keep_blank_values=keep_blank)
    return dict(result)


def parse_query_string_flat(query_string: str) -> Dict[str, str]:
    """
    Parse a query string into a flat dictionary (last value wins).
    
    Args:
        query_string: The query string (with or without leading ?)
        
    Returns:
        Dictionary with parameter names as keys and single values
        
    Examples:
        >>> parse_query_string_flat("a=1&b=2&a=3")
        {'a': '3', 'b': '2'}
    """
    items = parse_qsl(query_string.lstrip('?'))
    return dict(items)


# ============================================================================
# URL Building
# ============================================================================

def build_url(
    scheme: str = '',
    host: str = '',
    port: Optional[int] = None,
    path: str = '',
    query: Optional[Union[Dict[str, str], Dict[str, List[str]]]] = None,
    fragment: str = '',
    username: Optional[str] = None,
    password: Optional[str] = None,
) -> str:
    """
    Build a URL from its components.
    
    Args:
        scheme: URL scheme (http, https, etc.)
        host: Host name or IP
        port: Port number (optional, will be omitted if default for scheme)
        path: URL path
        query: Query parameters as dict
        fragment: URL fragment
        username: Username for authentication
        password: Password for authentication
        
    Returns:
        Complete URL string
        
    Examples:
        >>> build_url(scheme="https", host="example.com", path="/api", query={"q": "test"})
        'https://example.com/api?q=test'
    """
    # Build netloc
    netloc = host
    
    # Add credentials if provided
    if username:
        if password:
            netloc = f"{quote(username, safe='')}:{quote(password, safe='')}@{netloc}"
        else:
            netloc = f"{quote(username, safe='')}@{netloc}"
    
    # Add port if provided and non-default
    if port:
        default_ports = {'http': 80, 'https': 443, 'ftp': 21, 'ssh': 22, 'ws': 80, 'wss': 443}
        if scheme.lower() not in default_ports or port != default_ports.get(scheme.lower()):
            netloc = f"{netloc}:{port}"
    
    # Build query string
    query_string = ''
    if query:
        query_string = build_query_string(query)
    
    # Ensure path starts with /
    if path and not path.startswith('/'):
        path = '/' + path
    
    return urlunparse((scheme, netloc, path, '', query_string, fragment))


def build_query_string(
    params: Union[Dict[str, str], Dict[str, List[str]], List[Tuple[str, str]]],
    sort_keys: bool = False,
) -> str:
    """
    Build a query string from parameters.
    
    Args:
        params: Parameters as dict or list of tuples
        sort_keys: Whether to sort keys alphabetically
        
    Returns:
        Query string without leading ?
        
    Examples:
        >>> build_query_string({"a": "1", "b": "2"})
        'a=1&b=2'
        >>> build_query_string([("a", "1"), ("a", "2")])
        'a=1&a=2'
    """
    if isinstance(params, list):
        items = params
    else:
        items = []
        for key, value in params.items():
            if isinstance(value, list):
                for v in value:
                    items.append((key, v))
            else:
                items.append((key, value))
    
    if sort_keys:
        items = sorted(items, key=lambda x: x[0])
    
    return urlencode(items)


# ============================================================================
# URL Manipulation
# ============================================================================

def join_url(base: str, path: str) -> str:
    """
    Join a base URL with a path or relative URL.
    
    Args:
        base: Base URL
        path: Path or relative URL to join
        
    Returns:
        Combined URL
        
    Examples:
        >>> join_url("https://example.com/api", "users/1")
        'https://example.com/api/users/1'
        >>> join_url("https://example.com/api/", "/users/1")
        'https://example.com/users/1'
    """
    return urljoin(base, path)


def resolve_url(url: str, base: str) -> str:
    """
    Resolve a URL against a base URL.
    
    Args:
        url: URL to resolve (may be relative)
        base: Base URL to resolve against
        
    Returns:
        Absolute URL
        
    Examples:
        >>> resolve_url("../page.html", "https://example.com/docs/index.html")
        'https://example.com/page.html'
    """
    return urljoin(base, url)


def normalize_url(url: str, remove_default_port: bool = True, 
                  remove_fragment: bool = False, sort_query: bool = True) -> str:
    """
    Normalize a URL to a canonical form.
    
    Args:
        url: URL to normalize
        remove_default_port: Remove port if it's the default for the scheme
        remove_fragment: Remove the fragment identifier
        sort_query: Sort query parameters alphabetically
        
    Returns:
        Normalized URL
        
    Examples:
        >>> normalize_url("HTTPS://EXAMPLE.COM:443/Path?b=2&a=1")
        'https://example.com/Path?a=1&b=2'
    """
    parsed = parse_url(url)
    
    # Normalize scheme to lowercase
    scheme = parsed.scheme.lower()
    
    # Normalize host to lowercase
    host = parsed.host.lower()
    
    # Handle default port removal
    port = parsed.port
    if remove_default_port and port:
        default_ports = {'http': 80, 'https': 443, 'ftp': 21, 'ws': 80, 'wss': 443}
        if scheme in default_ports and port == default_ports[scheme]:
            port = None
    
    # Normalize path
    path = parsed.path
    if not path:
        path = '/'
    # Remove duplicate slashes but keep leading/trailing
    while '//' in path:
        path = path.replace('//', '/')
    
    # Build query string
    query = parsed.query
    if sort_query and query:
        query_items = []
        for key in sorted(query.keys()):
            for value in sorted(query[key]):
                query_items.append((key, value))
        query_dict = {k: [v for (key, v) in query_items if key == k] for k in sorted(query.keys())}
    else:
        query_dict = query
    
    # Build normalized URL
    return build_url(
        scheme=scheme,
        host=host,
        port=port,
        path=path,
        query=query_dict,
        fragment='' if remove_fragment else parsed.fragment,
    )


def get_url_path_segments(url: str) -> List[str]:
    """
    Get the path segments of a URL.
    
    Args:
        url: URL to analyze
        
    Returns:
        List of path segments
        
    Examples:
        >>> get_url_path_segments("https://example.com/api/v1/users/123")
        ['api', 'v1', 'users', '123']
    """
    parsed = parse_url(url)
    path = parsed.path.strip('/')
    if not path:
        return []
    return [unquote(segment) for segment in path.split('/')]


def get_file_extension(url: str) -> str:
    """
    Get the file extension from a URL path.
    
    Args:
        url: URL to analyze
        
    Returns:
        File extension (without dot), or empty string if none
        
    Examples:
        >>> get_file_extension("https://example.com/image.png?q=1")
        'png'
        >>> get_file_extension("https://example.com/page")
        ''
    """
    parsed = parse_url(url)
    path = parsed.path
    
    # Remove query string and fragment if still present
    if '?' in path:
        path = path.split('?')[0]
    if '#' in path:
        path = path.split('#')[0]
    
    # Get last segment
    segments = path.split('/')
    if segments:
        filename = segments[-1]
        if '.' in filename:
            return filename.rsplit('.', 1)[-1].lower()
    
    return ''


# ============================================================================
# Query Parameter Operations
# ============================================================================

def add_query_param(url: str, key: str, value: str) -> str:
    """
    Add a query parameter to a URL.
    
    Args:
        url: Original URL
        key: Parameter name
        value: Parameter value
        
    Returns:
        URL with added parameter
        
    Examples:
        >>> add_query_param("https://example.com?x=1", "y", "2")
        'https://example.com?x=1&y=2'
    """
    parsed = parse_url(url)
    query = dict(parsed.query)
    
    if key in query:
        query[key].append(value)
    else:
        query[key] = [value]
    
    return build_url(
        scheme=parsed.scheme,
        username=parsed.username,
        password=parsed.password,
        host=parsed.host,
        port=parsed.port,
        path=parsed.path,
        query=query,
        fragment=parsed.fragment,
    )


def set_query_param(url: str, key: str, value: str) -> str:
    """
    Set a query parameter, replacing any existing value(s).
    
    Args:
        url: Original URL
        key: Parameter name
        value: Parameter value
        
    Returns:
        URL with parameter set
        
    Examples:
        >>> set_query_param("https://example.com?x=1", "x", "2")
        'https://example.com?x=2'
    """
    parsed = parse_url(url)
    query = dict(parsed.query)
    query[key] = [value]
    
    return build_url(
        scheme=parsed.scheme,
        username=parsed.username,
        password=parsed.password,
        host=parsed.host,
        port=parsed.port,
        path=parsed.path,
        query=query,
        fragment=parsed.fragment,
    )


def remove_query_param(url: str, key: str) -> str:
    """
    Remove a query parameter from a URL.
    
    Args:
        url: Original URL
        key: Parameter name to remove
        
    Returns:
        URL with parameter removed
        
    Examples:
        >>> remove_query_param("https://example.com?x=1&y=2", "x")
        'https://example.com?y=2'
    """
    parsed = parse_url(url)
    query = dict(parsed.query)
    query.pop(key, None)
    
    return build_url(
        scheme=parsed.scheme,
        username=parsed.username,
        password=parsed.password,
        host=parsed.host,
        port=parsed.port,
        path=parsed.path,
        query=query if query else None,
        fragment=parsed.fragment,
    )


def get_query_param(url: str, key: str, default: Optional[str] = None) -> Optional[str]:
    """
    Get a single query parameter value from a URL.
    
    Args:
        url: URL to parse
        key: Parameter name
        default: Default value if not found
        
    Returns:
        Parameter value (last value if multiple), or default
        
    Examples:
        >>> get_query_param("https://example.com?a=1&a=2", "a")
        '2'
        >>> get_query_param("https://example.com", "missing", "default")
        'default'
    """
    parsed = parse_url(url)
    values = parsed.query.get(key, [])
    return values[-1] if values else default


def get_query_params(url: str, key: str) -> List[str]:
    """
    Get all values for a query parameter from a URL.
    
    Args:
        url: URL to parse
        key: Parameter name
        
    Returns:
        List of all values for the parameter
        
    Examples:
        >>> get_query_params("https://example.com?a=1&a=2", "a")
        ['1', '2']
    """
    parsed = parse_url(url)
    return parsed.query.get(key, [])


# ============================================================================
# Domain Utilities
# ============================================================================

# Common TLDs for domain extraction
COMMON_TLDS = {
    'com', 'org', 'net', 'edu', 'gov', 'mil', 'io', 'co', 'ai', 'app',
    'dev', 'me', 'info', 'biz', 'xyz', 'tech', 'online', 'site', 'store',
    'blog', 'code', 'cloud', 'design', 'email', 'games', 'health', 'life',
    'live', 'love', 'media', 'money', 'music', 'news', 'photo', 'pics',
    'shop', 'social', 'sport', 'tube', 'video', 'world', 'agency', 'camera',
    'club', 'digital', 'direct', 'guru', 'international', 'law', 'link',
    'marketing', 'photography', 'plus', 'press', 'report', 'science',
    'solutions', 'systems', 'technology', 'today', 'university', 'wiki',
    'work', 'zone', 'uk', 'jp', 'de', 'fr', 'cn', 'ru', 'br', 'it', 'es',
    'au', 'ca', 'nl', 'pl', 'in', 'kr', 'mx', 'id', 'tw', 'be', 'se',
    'ch', 'at', 'dk', 'no', 'fi', 'cz', 'pt', 'ro', 'hu', 'gr', 'ar',
    'za', 'sg', 'hk', 'tr', 'vn', 'my', 'ph', 'ae', 'sa', 'th', 'ng',
    'pk', 'eg', 'ir', 'bd', 'ke', 'co.uk', 'co.jp', 'co.kr', 'com.au',
    'co.in', 'com.br', 'co.za', 'co.nz', 'gov.uk', 'ac.uk', 'edu.au',
}

# Domain regex pattern
DOMAIN_PATTERN = re.compile(
    r'^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)*[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?$'
)


def is_valid_domain(domain: str) -> bool:
    """
    Check if a string is a valid domain name.
    
    Args:
        domain: Domain name to validate
        
    Returns:
        True if valid domain name
        
    Examples:
        >>> is_valid_domain("example.com")
        True
        >>> is_valid_domain("sub.example.com")
        True
        >>> is_valid_domain("invalid..domain")
        False
    """
    # Remove port if present
    if ':' in domain:
        domain = domain.split(':')[0]
    
    # Check overall length
    if len(domain) > 253:
        return False
    
    # Check against pattern
    if not DOMAIN_PATTERN.match(domain):
        return False
    
    # Check each label
    labels = domain.split('.')
    for label in labels:
        if len(label) > 63 or len(label) < 1:
            return False
        if label.startswith('-') or label.endswith('-'):
            return False
    
    return True


def extract_domain(url: str) -> str:
    """
    Extract the domain from a URL.
    
    Args:
        url: URL to extract domain from
        
    Returns:
        Domain name (host)
        
    Examples:
        >>> extract_domain("https://www.example.com/path")
        'www.example.com'
        >>> extract_domain("https://user:pass@example.com:8080")
        'example.com'
    """
    parsed = parse_url(url)
    return parsed.host


def extract_root_domain(url: str) -> str:
    """
    Extract the root domain (SLD + TLD) from a URL.
    
    Args:
        url: URL to extract root domain from
        
    Returns:
        Root domain (e.g., 'example.com' from 'www.sub.example.com')
        
    Examples:
        >>> extract_root_domain("https://www.example.com")
        'example.com'
        >>> extract_root_domain("https://sub.example.co.uk")
        'example.co.uk'
    """
    domain = extract_domain(url)
    
    # Handle IP addresses
    try:
        ip_address(domain)
        return domain
    except ValueError:
        pass
    
    labels = domain.split('.')
    
    if len(labels) < 2:
        return domain
    
    # Check for two-part TLDs
    if len(labels) >= 3:
        potential_tld = f"{labels[-2]}.{labels[-1]}"
        if potential_tld.lower() in COMMON_TLDS:
            return f"{labels[-3]}.{potential_tld}"
    
    return f"{labels[-2]}.{labels[-1]}"


def extract_subdomain(url: str) -> Optional[str]:
    """
    Extract the subdomain from a URL.
    
    Args:
        url: URL to extract subdomain from
        
    Returns:
        Subdomain (without root domain), or None if no subdomain
        
    Examples:
        >>> extract_subdomain("https://www.example.com")
        'www'
        >>> extract_subdomain("https://api.v1.example.com")
        'api.v1'
        >>> extract_subdomain("https://example.com")
        None
    """
    domain = extract_domain(url)
    
    # Handle IP addresses
    try:
        ip_address(domain)
        return None
    except ValueError:
        pass
    
    labels = domain.split('.')
    
    if len(labels) < 3:
        return None
    
    # Check for two-part TLDs
    if len(labels) >= 4:
        potential_tld = f"{labels[-2]}.{labels[-1]}"
        if potential_tld.lower() in COMMON_TLDS:
            if len(labels) == 4:
                return labels[0]
            return '.'.join(labels[:-3])
    
    return '.'.join(labels[:-2])


# ============================================================================
# URL Safety and Validation
# ============================================================================

SAFE_URL_SCHEMES = {'http', 'https', 'ftp', 'sftp', 'ws', 'wss', 'mailto', 'tel', 'data'}
DANGEROUS_URL_SCHEMES = {'javascript', 'vbscript', 'file', 'about', 'blob'}


def is_safe_url(url: str, allow_relative: bool = False) -> bool:
    """
    Check if a URL is safe (not a potential XSS vector).
    
    Args:
        url: URL to check
        allow_relative: Whether to allow relative URLs
        
    Returns:
        True if URL is safe
        
    Examples:
        >>> is_safe_url("https://example.com")
        True
        >>> is_safe_url("javascript:alert(1)")
        False
        >>> is_safe_url("/relative/path", allow_relative=True)
        True
    """
    url = url.strip()
    
    # Empty URL
    if not url:
        return False
    
    # Check for dangerous protocols
    lower_url = url.lower()
    for dangerous in DANGEROUS_URL_SCHEMES:
        if lower_url.startswith(f"{dangerous}:"):
            return False
    
    # Check for relative URLs
    if url.startswith('/') or url.startswith('./') or url.startswith('../'):
        return allow_relative
    
    # Parse and check scheme
    try:
        parsed = parse_url(url)
        if parsed.scheme and parsed.scheme.lower() not in SAFE_URL_SCHEMES:
            return False
    except Exception:
        return False
    
    return True


def is_absolute_url(url: str) -> bool:
    """
    Check if a URL is absolute.
    
    Args:
        url: URL to check
        
    Returns:
        True if URL is absolute
        
    Examples:
        >>> is_absolute_url("https://example.com")
        True
        >>> is_absolute_url("/path/to/resource")
        False
    """
    url = url.strip()
    return '://' in url or url.startswith('//')


def is_same_origin(url1: str, url2: str) -> bool:
    """
    Check if two URLs have the same origin (scheme + host + port).
    
    Args:
        url1: First URL
        url2: Second URL
        
    Returns:
        True if same origin
        
    Examples:
        >>> is_same_origin("https://example.com/a", "https://example.com/b")
        True
        >>> is_same_origin("https://example.com", "https://other.com")
        False
    """
    p1 = parse_url(url1)
    p2 = parse_url(url2)
    
    return (
        p1.scheme.lower() == p2.scheme.lower() and
        p1.host.lower() == p2.host.lower() and
        p1.port == p2.port
    )


def validate_url(url: str, require_scheme: bool = True) -> Tuple[bool, Optional[str]]:
    """
    Validate a URL and return error message if invalid.
    
    Args:
        url: URL to validate
        require_scheme: Whether scheme is required
        
    Returns:
        Tuple of (is_valid, error_message)
        
    Examples:
        >>> validate_url("https://example.com")
        (True, None)
        >>> validate_url("not a url")
        (False, 'Missing or invalid scheme')
    """
    if not url or not url.strip():
        return False, "URL is empty"
    
    url = url.strip()
    
    # Check for control characters
    if any(c in url for c in '\r\n\t'):
        return False, "URL contains control characters"
    
    # Parse URL
    try:
        parsed = parse_url(url)
    except Exception as e:
        return False, f"Failed to parse URL: {str(e)}"
    
    # Check scheme
    if require_scheme and not parsed.scheme:
        return False, "Missing or invalid scheme"
    
    if parsed.scheme and parsed.scheme.lower() not in SAFE_URL_SCHEMES and parsed.scheme.lower() not in DANGEROUS_URL_SCHEMES:
        return False, f"Unsupported scheme: {parsed.scheme}"
    
    # Check host
    if not parsed.host and parsed.scheme and parsed.scheme.lower() not in ('mailto', 'tel', 'data'):
        return False, "Missing host"
    
    # Validate domain or IP
    if parsed.host:
        # Try IP validation
        try:
            ip_address(parsed.host)
            return True, None
        except ValueError:
            pass
        
        # Validate domain
        if not is_valid_domain(parsed.host):
            return False, f"Invalid host: {parsed.host}"
    
    return True, None


# ============================================================================
# URL Encoding Utilities
# ============================================================================

def encode_url_component(s: str, safe: str = '') -> str:
    """
    URL-encode a string component.
    
    Args:
        s: String to encode
        safe: Characters to NOT encode
        
    Returns:
        Encoded string
        
    Examples:
        >>> encode_url_component("hello world")
        'hello%20world'
        >>> encode_url_component("a/b/c", safe="/")
        'a/b/c'
    """
    return quote(s, safe=safe)


def decode_url_component(s: str) -> str:
    """
    URL-decode a string component.
    
    Args:
        s: String to decode
        
    Returns:
        Decoded string
        
    Examples:
        >>> decode_url_component("hello%20world")
        'hello world'
    """
    return unquote(s)


def encode_path(path: str) -> str:
    """
    URL-encode a path, preserving slashes.
    
    Args:
        path: Path to encode
        
    Returns:
        Encoded path
        
    Examples:
        >>> encode_path("/path with spaces/file.txt")
        '/path%20with%20spaces/file.txt'
    """
    return quote(path, safe='/')


def encode_query_value(value: str) -> str:
    """
    URL-encode a query string value.
    
    Args:
        value: Value to encode
        
    Returns:
        Encoded value
        
    Examples:
        >>> encode_query_value("a=1&b=2")
        'a%3D1%26b%3D2'
    """
    return quote(value, safe='')


# ============================================================================
# Special URL Types
# ============================================================================

def is_ip_url(url: str) -> bool:
    """
    Check if URL uses an IP address instead of domain.
    
    Args:
        url: URL to check
        
    Returns:
        True if host is an IP address
    """
    host = extract_domain(url)
    try:
        ip_address(host)
        return True
    except ValueError:
        return False


def get_ip_version(url: str) -> Optional[int]:
    """
    Get IP version (4 or 6) if URL uses IP address.
    
    Args:
        url: URL to check
        
    Returns:
        4 for IPv4, 6 for IPv6, None if not an IP
    """
    host = extract_domain(url)
    try:
        ip = ip_address(host)
        return ip.version
    except ValueError:
        return None


def is_localhost_url(url: str) -> bool:
    """
    Check if URL points to localhost.
    
    Args:
        url: URL to check
        
    Returns:
        True if URL points to localhost
    """
    host = extract_domain(url).lower()
    
    if host in ('localhost', '127.0.0.1', '::1', '0.0.0.0'):
        return True
    
    # Check for localhost ports
    if host.startswith('localhost:') or host.startswith('127.0.0.1:'):
        return True
    
    return False


def is_private_url(url: str) -> bool:
    """
    Check if URL points to a private/internal network.
    
    Args:
        url: URL to check
        
    Returns:
        True if URL points to private network
    """
    host = extract_domain(url)
    
    # Check localhost
    if is_localhost_url(url):
        return True
    
    try:
        ip = ip_address(host)
        return ip.is_private
    except ValueError:
        pass
    
    # Check for private domain patterns
    private_suffixes = ('.local', '.internal', '.lan', '.home', '.localdomain')
    return any(host.lower().endswith(suffix) for suffix in private_suffixes)


def parse_data_url(url: str) -> Optional[Dict[str, str]]:
    """
    Parse a data URL into its components.
    
    Args:
        url: Data URL to parse
        
    Returns:
        Dict with 'media_type', 'encoding', 'data' keys, or None if not a data URL
        
    Examples:
        >>> parse_data_url("data:text/plain;base64,SGVsbG8gV29ybGQ=")
        {'media_type': 'text/plain', 'encoding': 'base64', 'data': 'SGVsbG8gV29ybGQ='}
    """
    if not url.lower().startswith('data:'):
        return None
    
    try:
        # data:[<mediatype>][;base64],<data>
        rest = url[5:]  # Remove 'data:'
        
        # Find the comma separating metadata from data
        comma_idx = rest.find(',')
        if comma_idx == -1:
            return None
        
        metadata = rest[:comma_idx]
        data = rest[comma_idx + 1:]
        
        # Parse metadata
        media_type = 'text/plain'
        encoding = None
        
        if metadata:
            parts = metadata.split(';')
            if parts[0]:
                media_type = parts[0]
            
            for part in parts[1:]:
                if part.lower() == 'base64':
                    encoding = 'base64'
        
        return {
            'media_type': media_type or 'text/plain',
            'encoding': encoding,
            'data': data,
        }
    except Exception:
        return None


# ============================================================================
# URL Comparison
# ============================================================================

def urls_equal(url1: str, url2: str, ignore_trailing_slash: bool = True,
               ignore_fragment: bool = False, ignore_query_order: bool = True) -> bool:
    """
    Compare two URLs for equality.
    
    Args:
        url1: First URL
        url2: Second URL
        ignore_trailing_slash: Ignore trailing slash in path
        ignore_fragment: Ignore fragment identifier
        ignore_query_order: Ignore parameter order in query string
        
    Returns:
        True if URLs are equal
    """
    p1 = parse_url(url1)
    p2 = parse_url(url2)
    
    # Compare scheme and host (case-insensitive)
    if p1.scheme.lower() != p2.scheme.lower():
        return False
    if p1.host.lower() != p2.host.lower():
        return False
    if p1.port != p2.port:
        return False
    
    # Compare path
    path1 = p1.path
    path2 = p2.path
    if ignore_trailing_slash:
        path1 = path1.rstrip('/')
        path2 = path2.rstrip('/')
    if path1 != path2:
        return False
    
    # Compare fragment
    if not ignore_fragment and p1.fragment != p2.fragment:
        return False
    
    # Compare query
    if ignore_query_order:
        q1 = {k: sorted(v) for k, v in p1.query.items()}
        q2 = {k: sorted(v) for k, v in p2.query.items()}
        return q1 == q2
    else:
        return p1.query == p2.query


# ============================================================================
# Main Example
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("URL Utilities - Example Usage")
    print("=" * 60)
    
    # URL Parsing
    print("\n1. URL Parsing:")
    url = "https://user:pass@example.com:8080/api/v1/users?id=123&sort=name#section"
    info = parse_url(url)
    print(f"   URL: {url}")
    print(f"   Scheme: {info.scheme}")
    print(f"   Username: {info.username}")
    print(f"   Host: {info.host}")
    print(f"   Port: {info.port}")
    print(f"   Path: {info.path}")
    print(f"   Query: {info.query}")
    print(f"   Fragment: {info.fragment}")
    print(f"   Origin: {info.origin}")
    print(f"   Is Secure: {info.is_secure}")
    
    # URL Building
    print("\n2. URL Building:")
    built_url = build_url(
        scheme="https",
        host="api.example.com",
        port=443,
        path="/v1/search",
        query={"q": "hello world", "limit": "10"},
        fragment="results"
    )
    print(f"   Built URL: {built_url}")
    
    # Query Parameter Operations
    print("\n3. Query Parameter Operations:")
    url = "https://example.com/search?q=test&page=1"
    url = add_query_param(url, "sort", "date")
    print(f"   Add param: {url}")
    url = set_query_param(url, "page", "2")
    print(f"   Set param: {url}")
    url = remove_query_param(url, "q")
    print(f"   Remove param: {url}")
    
    # Domain Utilities
    print("\n4. Domain Utilities:")
    urls = [
        "https://www.example.com",
        "https://api.v1.example.co.uk",
        "https://subdomain.example.com/path",
    ]
    for u in urls:
        domain = extract_domain(u)
        root = extract_root_domain(u)
        subdomain = extract_subdomain(u)
        print(f"   {u}")
        print(f"      Domain: {domain}, Root: {root}, Subdomain: {subdomain}")
    
    # URL Safety
    print("\n5. URL Safety Checks:")
    test_urls = [
        "https://example.com",
        "javascript:alert(1)",
        "/relative/path",
        "data:text/plain;base64,SGVsbG8=",
    ]
    for u in test_urls:
        safe = is_safe_url(u, allow_relative=True)
        valid, error = validate_url(u, require_scheme=False)
        print(f"   {u[:40]:<40} Safe: {safe}, Valid: {valid}")
    
    # URL Normalization
    print("\n6. URL Normalization:")
    urls = [
        "HTTPS://EXAMPLE.COM:443/Path?b=2&a=1",
        "https://example.com//double//slashes",
    ]
    for u in urls:
        normalized = normalize_url(u)
        print(f"   {u[:45]}")
        print(f"   -> {normalized}")
    
    # Data URL Parsing
    print("\n7. Data URL Parsing:")
    data_url = "data:text/html;base64,PGh0bWw+SGVsbG88L2h0bWw+"
    parsed_data = parse_data_url(data_url)
    print(f"   URL: {data_url}")
    print(f"   Media Type: {parsed_data['media_type']}")
    print(f"   Encoding: {parsed_data['encoding']}")
    print(f"   Data: {parsed_data['data']}")
    
    # URL Comparison
    print("\n8. URL Comparison:")
    url1 = "https://example.com/path?a=1&b=2"
    url2 = "https://EXAMPLE.COM/path?b=2&a=1"
    equal = urls_equal(url1, url2)
    print(f"   {url1}")
    print(f"   {url2}")
    print(f"   Equal (ignoring query order): {equal}")
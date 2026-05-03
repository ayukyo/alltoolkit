# cookie_utils - HTTP Cookie Parsing and Management

Zero-dependency HTTP cookie handling with full RFC 6265 compliance.

## Features

- **Cookie Parsing**: Parse Set-Cookie and Cookie headers
- **Cookie Jar**: Full cookie storage with domain/path matching
- **Expiration Handling**: Automatic expiration detection and cleanup
- **Security**: HttpOnly, Secure, SameSite attribute support
- **URL Matching**: Retrieve cookies for specific URLs
- **Serialization**: JSON-compatible serialization for persistence
- **Validation**: Cookie name and value validation per RFC 6265

## Installation

```python
from cookie_utils.mod import (
    Cookie,
    parse_set_cookie,
    parse_cookie_header,
    build_cookie_header,
    CookieJar,
    validate_cookie_name,
    validate_cookie_value,
    encode_cookie_value,
    decode_cookie_value,
    same_site_matches,
    make_session_cookie,
    make_persistent_cookie,
)
```

## Quick Start

### Parsing Set-Cookie Headers

```python
from cookie_utils.mod import parse_set_cookie

# Parse a Set-Cookie header
cookie = parse_set_cookie("session=abc123; Domain=example.com; Path=/; HttpOnly")

print(cookie.name)       # "session"
print(cookie.value)      # "abc123"
print(cookie.domain)     # "example.com"
print(cookie.http_only)  # True
```

### Parsing Cookie Headers

```python
from cookie_utils.mod import parse_cookie_header, build_cookie_header

# Parse a Cookie header
cookies = parse_cookie_header("session=abc123; user=john")
print(cookies)  # {"session": "abc123", "user": "john"}

# Build a Cookie header
header = build_cookie_header({"session": "abc123", "user": "john"})
print(header)  # "session=abc123; user=john"
```

### Using CookieJar

```python
from cookie_utils.mod import CookieJar, Cookie

jar = CookieJar()

# Add cookies
jar.add(Cookie(name="session", value="abc123", domain="example.com"))
jar.add(Cookie(name="user", value="john", domain="example.com", path="/app"))

# Get cookies for a URL
cookies = jar.get_for_url("https://example.com/app/page")
header = jar.get_cookie_header("https://example.com/app/page")

# Check if cookie exists
if "session" in jar:
    print("Session cookie exists")

# Remove cookie
jar.remove("session")
```

### Creating Cookies

```python
from cookie_utils.mod import make_session_cookie, make_persistent_cookie

# Session cookie (no expiration)
session = make_session_cookie("session", "abc123", http_only=True)

# Persistent cookie (with expiration)
persistent = make_persistent_cookie(
    "remember_me", "user_token",
    max_age=86400,  # 24 hours
    domain="example.com",
    secure=True,
    same_site="Lax"
)

# Convert to Set-Cookie header
print(persistent.to_set_cookie())
# "remember_me=user_token; Domain=example.com; Expires=...; Secure; HttpOnly; SameSite=Lax"
```

## API Reference

### Cookie

Dataclass representing an HTTP cookie.

```python
@dataclass
class Cookie:
    name: str                   # Cookie name
    value: str                  # Cookie value
    domain: str = ""            # Domain scope
    path: str = "/"             # Path scope
    expires: Optional[float]    # Expiration timestamp
    max_age: Optional[int]      # Max-Age in seconds
    secure: bool = False        # HTTPS only
    http_only: bool = False     # Not accessible via JavaScript
    same_site: Optional[str]    # "Strict", "Lax", or "None"
```

**Methods:**

- `is_expired()` - Check if cookie has expired
- `matches(url)` - Check if cookie should be sent to URL
- `to_header()` - Convert to Cookie header format
- `to_set_cookie()` - Convert to Set-Cookie header format
- `copy()` - Create a copy of the cookie

### CookieJar

Cookie storage with domain/path matching.

```python
jar = CookieJar()

# Basic operations
jar.add(cookie)                     # Add a cookie
jar.get("name")                     # Get cookie by name
jar.remove("name")                  # Remove cookie
jar.clear()                         # Clear all cookies
len(jar)                            # Count of cookies
"name" in jar                       # Check existence

# URL-based operations
jar.get_for_url("https://example.com/")     # Get matching cookies
jar.get_cookie_header("https://example.com/")  # Build Cookie header

# Bulk operations
jar.update_from_headers([headers])  # Add from Set-Cookie headers
jar.clear_expired()                 # Remove expired cookies
jar.get_all()                       # Get all cookies

# Serialization
jar.to_dict()                       # Serialize to list of dicts
CookieJar.from_dict(data)           # Deserialize
```

### Parsing Functions

```python
# Parse Set-Cookie header
cookie = parse_set_cookie("name=value; Domain=example.com")

# Parse Cookie header
cookies = parse_cookie_header("name1=value1; name2=value2")

# Build Cookie header
header = build_cookie_header({"name1": "value1", "name2": "value2"})
```

### Validation Functions

```python
# Validate cookie name
validate_cookie_name("session")     # True
validate_cookie_name("bad name")    # False (contains space)

# Validate cookie value
validate_cookie_value("abc123")     # True
validate_cookie_value("bad;value")  # False (contains semicolon)

# Encode/decode values for safe storage
encoded = encode_cookie_value("hello world")  # Base64 encoded
decoded = decode_cookie_value(encoded)        # Original value
```

### SameSite Policy

```python
# Check if SameSite policy allows sending
same_site_matches(
    same_site="Strict",     # Cookie's SameSite value
    from_site="example.com",  # Origin site
    to_site="other.com",     # Target site
    is_secure=True          # HTTPS request
)
```

### Factory Functions

```python
# Create session cookie
session = make_session_cookie(
    name="session",
    value="abc123",
    path="/",
    secure=False,
    http_only=True,
    same_site="Lax"
)

# Create persistent cookie
persistent = make_persistent_cookie(
    name="remember",
    value="token",
    max_age=86400,           # Seconds until expiration
    domain="example.com",
    path="/",
    secure=True,
    http_only=True,
    same_site="Strict"
)
```

## SameSite Values

| Value | Behavior |
|-------|----------|
| `Strict` | Only sent in same-site requests |
| `Lax` | Same-site and top-level GET navigation |
| `None` | Cross-site allowed, requires Secure flag |

## Cookie Matching Rules

A cookie is sent to a URL if:

1. Cookie is not expired
2. URL scheme is HTTPS (if cookie is Secure)
3. URL host matches cookie domain
4. URL path starts with cookie path

## Examples

### Web Session Management

```python
from cookie_utils.mod import CookieJar, parse_set_cookie

# Simulate receiving cookies from server
jar = CookieJar()

headers = [
    "session=abc123; Path=/; HttpOnly; SameSite=Lax",
    "csrf_token=xyz789; Path=/; SameSite=Strict",
]

jar.update_from_headers(headers)

# Send cookies with next request
cookie_header = jar.get_cookie_header("https://example.com/api/users")
# "session=abc123; csrf_token=xyz789"
```

### Cookie Persistence

```python
import json
from cookie_utils.mod import CookieJar

jar = CookieJar()

# Add cookies
jar.add(make_persistent_cookie("user", "john", max_age=86400))

# Save to file
data = jar.to_dict()
with open("cookies.json", "w") as f:
    json.dump(data, f)

# Load from file
with open("cookies.json", "r") as f:
    data = json.load(f)
jar = CookieJar.from_dict(data)
```

### Cookie Expiration

```python
from cookie_utils.mod import Cookie, CookieJar
import time

jar = CookieJar()

# Add cookies with different lifetimes
jar.add(Cookie(name="short", value="1", max_age=60))     # 1 minute
jar.add(Cookie(name="long", value="2", max_age=3600))    # 1 hour
jar.add(Cookie(name="permanent", value="3", expires=time.time() + 365*24*3600))

# Clean up expired cookies
jar.clear_expired()

# Check expiration
cookie = jar.get("short")
if cookie:
    remaining = cookie.expires - time.time()
    print(f"Expires in {remaining} seconds")
```

## RFC 6265 Compliance

This module follows RFC 6265 (HTTP State Management Mechanism):

- Cookie name validation (no special characters)
- Cookie value validation (no control characters, quotes)
- Domain matching (exact or subdomain)
- Path matching (prefix match)
- Expiration parsing (RFC 1123 dates)
- SameSite attribute handling

## Testing

```bash
python Python/cookie_utils/cookie_utils_test.py
```

**Test Coverage:**
- 25 test functions
- 200+ test cases
- Covers parsing, jar operations, matching, validation
- Boundary value tests (empty, long, unicode, expiration edge cases)

## License

MIT License - Part of AllToolkit project
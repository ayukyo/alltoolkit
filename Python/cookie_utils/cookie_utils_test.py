"""
Comprehensive tests for cookie_utils module.

Tests cover:
- Cookie parsing and formatting
- CookieJar management
- Expiration handling
- Domain and path matching
- SameSite policy
- Edge cases and boundary values
"""

import sys
import os
import time
import json

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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
    _parse_expires,
)


class TestResult:
    """Test result collector."""
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []
    
    def assert_equal(self, actual, expected, msg=""):
        if actual == expected:
            self.passed += 1
        else:
            self.failed += 1
            self.errors.append(f"Expected {expected}, got {actual}. {msg}")
    
    def assert_true(self, condition, msg=""):
        if condition:
            self.passed += 1
        else:
            self.failed += 1
            self.errors.append(f"Expected True. {msg}")
    
    def assert_false(self, condition, msg=""):
        if not condition:
            self.passed += 1
        else:
            self.failed += 1
            self.errors.append(f"Expected False. {msg}")
    
    def assert_is_none(self, value, msg=""):
        if value is None:
            self.passed += 1
        else:
            self.failed += 1
            self.errors.append(f"Expected None, got {value}. {msg}")
    
    def assert_is_not_none(self, value, msg=""):
        if value is not None:
            self.passed += 1
        else:
            self.failed += 1
            self.errors.append(f"Expected not None. {msg}")
    
    def assert_in(self, item, container, msg=""):
        if item in container:
            self.passed += 1
        else:
            self.failed += 1
            self.errors.append(f"Expected {item} in {container}. {msg}")
    
    def assert_greater(self, a, b, msg=""):
        if a > b:
            self.passed += 1
        else:
            self.failed += 1
            self.errors.append(f"Expected {a} > {b}. {msg}")
    
    def summary(self):
        total = self.passed + self.failed
        print(f"\n{'='*60}")
        print(f"Test Results: {self.passed}/{total} passed")
        print(f"{'='*60}")
        if self.errors:
            print(f"\nFailures ({self.failed}):")
            for i, err in enumerate(self.errors[:10], 1):
                print(f"  {i}. {err}")
            if len(self.errors) > 10:
                print(f"  ... and {len(self.errors) - 10} more errors")
        return self.failed == 0


def test_cookie_creation():
    """Test Cookie dataclass creation and defaults."""
    r = TestResult()
    
    # Basic cookie
    c = Cookie(name="session", value="abc123")
    r.assert_equal(c.name, "session")
    r.assert_equal(c.value, "abc123")
    r.assert_equal(c.path, "/")
    r.assert_false(c.secure)
    r.assert_false(c.http_only)
    r.assert_is_none(c.expires)
    r.assert_is_none(c.same_site)
    
    # Full cookie
    c2 = Cookie(
        name="user",
        value="john",
        domain="example.com",
        path="/app",
        secure=True,
        http_only=True,
        same_site="Strict",
    )
    r.assert_equal(c2.name, "user")
    r.assert_equal(c2.domain, "example.com")
    r.assert_equal(c2.path, "/app")
    r.assert_true(c2.secure)
    r.assert_true(c2.http_only)
    r.assert_equal(c2.same_site, "Strict")
    
    # Domain normalization (remove leading dot)
    c3 = Cookie(name="test", value="1", domain=".example.com")
    r.assert_equal(c3.domain, "example.com")
    
    print("test_cookie_creation: done")
    return r


def test_cookie_expiration():
    """Test cookie expiration logic."""
    r = TestResult()
    
    # No expiration
    c1 = Cookie(name="session", value="abc")
    r.assert_false(c1.is_expired())
    
    # Future expiration
    c2 = Cookie(name="temp", value="xyz", expires=time.time() + 3600)
    r.assert_false(c2.is_expired())
    r.assert_true(c2.persistent)
    
    # Past expiration
    c3 = Cookie(name="old", value="expired", expires=time.time() - 3600)
    r.assert_true(c3.is_expired())
    
    # Max-Age sets expiration
    c4 = Cookie(name="max", value="age", max_age=3600)
    r.assert_is_not_none(c4.expires)
    r.assert_false(c4.is_expired())
    r.assert_true(c4.persistent)
    
    # Zero Max-Age means immediate expiration
    c5 = Cookie(name="del", value="now", max_age=0)
    r.assert_true(c5.is_expired())
    
    print("test_cookie_expiration: done")
    return r


def test_cookie_domain_matching():
    """Test cookie domain matching."""
    r = TestResult()
    
    # Host-only cookie
    c1 = Cookie(name="host", value="only", domain="example.com", host_only=True)
    r.assert_true(c1._domain_match("example.com"))
    r.assert_false(c1._domain_match("sub.example.com"))
    r.assert_false(c1._domain_match("other.com"))
    
    # Domain cookie (allows subdomains)
    c2 = Cookie(name="domain", value="cookie", domain="example.com", host_only=False)
    r.assert_true(c2._domain_match("example.com"))
    r.assert_true(c2._domain_match("sub.example.com"))
    r.assert_true(c2._domain_match("deep.sub.example.com"))
    r.assert_false(c2._domain_match("other.com"))
    r.assert_false(c2._domain_match("example.org"))
    
    # Case insensitivity
    c3 = Cookie(name="case", value="test", domain="Example.COM", host_only=False)
    r.assert_true(c3._domain_match("example.com"))
    r.assert_true(c3._domain_match("EXAMPLE.COM"))
    r.assert_true(c3._domain_match("Sub.Example.Com"))
    
    print("test_cookie_domain_matching: done")
    return r


def test_cookie_path_matching():
    """Test cookie path matching."""
    r = TestResult()
    
    # Root path matches everything
    c1 = Cookie(name="root", value="1", path="/")
    r.assert_true(c1._path_match("/"))
    r.assert_true(c1._path_match("/any"))
    r.assert_true(c1._path_match("/path/to/page"))
    
    # Specific path
    c2 = Cookie(name="app", value="2", path="/app")
    r.assert_true(c2._path_match("/app"))
    r.assert_true(c2._path_match("/app/"))
    r.assert_true(c2._path_match("/app/page"))
    r.assert_false(c2._path_match("/application"))
    r.assert_false(c2._path_match("/"))
    
    # Trailing slash path
    c3 = Cookie(name="trail", value="3", path="/api/")
    r.assert_true(c3._path_match("/api/"))
    r.assert_true(c3._path_match("/api/users"))
    r.assert_false(c3._path_match("/api"))
    
    print("test_cookie_path_matching: done")
    return r


def test_cookie_matches_url():
    """Test full URL matching."""
    r = TestResult()
    
    # Basic matching - default host_only=True means exact domain match only
    c1 = Cookie(name="test", value="1", domain="example.com", path="/")
    r.assert_true(c1.matches("http://example.com/"))
    r.assert_true(c1.matches("https://example.com/page"))
    r.assert_false(c1.matches("https://sub.example.com/"))  # host_only=True default
    
    # With host_only=False, matches subdomains
    c1b = Cookie(name="test2", value="2", domain="example.com", path="/", host_only=False)
    r.assert_true(c1b.matches("https://sub.example.com/"))
    
    # Secure cookie
    c2 = Cookie(name="secure", value="2", domain="example.com", secure=True)
    r.assert_false(c2.matches("http://example.com/"))
    r.assert_true(c2.matches("https://example.com/"))
    
    # Expired cookie
    c3 = Cookie(name="exp", value="3", expires=time.time() - 1000)
    r.assert_false(c3.matches("https://example.com/"))
    
    # Path restriction
    c4 = Cookie(name="path", value="4", domain="example.com", path="/admin")
    r.assert_true(c4.matches("https://example.com/admin"))
    r.assert_true(c4.matches("https://example.com/admin/users"))
    r.assert_false(c4.matches("https://example.com/"))
    r.assert_false(c4.matches("https://example.com/public"))
    
    print("test_cookie_matches_url: done")
    return r


def test_parse_set_cookie():
    """Test Set-Cookie header parsing."""
    r = TestResult()
    
    # Simple cookie
    c1 = parse_set_cookie("session=abc123")
    r.assert_is_not_none(c1)
    r.assert_equal(c1.name, "session")
    r.assert_equal(c1.value, "abc123")
    
    # With attributes
    c2 = parse_set_cookie("user=john; Domain=example.com; Path=/app; Secure; HttpOnly")
    r.assert_is_not_none(c2)
    r.assert_equal(c2.name, "user")
    r.assert_equal(c2.value, "john")
    r.assert_equal(c2.domain, "example.com")
    r.assert_equal(c2.path, "/app")
    r.assert_true(c2.secure)
    r.assert_true(c2.http_only)
    
    # With SameSite
    c3 = parse_set_cookie("csrf=token123; SameSite=Strict")
    r.assert_is_not_none(c3)
    r.assert_equal(c3.same_site, "Strict")
    
    # With Max-Age
    c4 = parse_set_cookie("temp=value; Max-Age=3600")
    r.assert_is_not_none(c4)
    r.assert_equal(c4.max_age, 3600)
    r.assert_is_not_none(c4.expires)
    
    # With quoted value
    c5 = parse_set_cookie('quoted="hello world"')
    r.assert_is_not_none(c5)
    r.assert_equal(c5.value, "hello world")
    
    # Domain with leading dot
    c6 = parse_set_cookie("test=1; Domain=.example.com")
    r.assert_is_not_none(c6)
    r.assert_equal(c6.domain, "example.com")
    r.assert_false(c6.host_only)
    
    # Empty header
    r.assert_is_none(parse_set_cookie(""))
    r.assert_is_none(parse_set_cookie(None))
    r.assert_is_none(parse_set_cookie("invalid"))
    
    print("test_parse_set_cookie: done")
    return r


def test_parse_cookie_header():
    """Test Cookie header parsing."""
    r = TestResult()
    
    # Simple
    cookies = parse_cookie_header("session=abc123")
    r.assert_equal(len(cookies), 1)
    r.assert_equal(cookies["session"], "abc123")
    
    # Multiple cookies
    cookies = parse_cookie_header("a=1; b=2; c=3")
    r.assert_equal(len(cookies), 3)
    r.assert_equal(cookies["a"], "1")
    r.assert_equal(cookies["b"], "2")
    r.assert_equal(cookies["c"], "3")
    
    # Empty
    r.assert_equal(len(parse_cookie_header("")), 0)
    r.assert_equal(len(parse_cookie_header(None)), 0)
    
    # Whitespace handling
    cookies = parse_cookie_header("  key = value  ;  name = test  ")
    r.assert_equal(cookies["key"], "value")
    r.assert_equal(cookies["name"], "test")
    
    print("test_parse_cookie_header: done")
    return r


def test_build_cookie_header():
    """Test Cookie header building."""
    r = TestResult()
    
    # Single cookie
    header = build_cookie_header({"session": "abc123"})
    r.assert_equal(header, "session=abc123")
    
    # Multiple cookies
    header = build_cookie_header({"a": "1", "b": "2"})
    r.assert_in("a=1", header)
    r.assert_in("b=2", header)
    r.assert_in(";", header)
    
    # Empty
    r.assert_equal(build_cookie_header({}), "")
    
    print("test_build_cookie_header: done")
    return r


def test_cookie_to_headers():
    """Test cookie to header conversion."""
    r = TestResult()
    
    # Cookie header
    c = Cookie(name="session", value="abc123")
    r.assert_equal(c.to_header(), "session=abc123")
    
    # Set-Cookie header - basic
    header = c.to_set_cookie()
    r.assert_in("session=abc123", header)
    
    # Set-Cookie header - with attributes
    c2 = Cookie(
        name="user",
        value="john",
        domain="example.com",
        path="/app",
        secure=True,
        http_only=True,
        same_site="Lax",
    )
    header = c2.to_set_cookie()
    r.assert_in("user=john", header)
    r.assert_in("Domain=example.com", header)
    r.assert_in("Path=/app", header)
    r.assert_in("Secure", header)
    r.assert_in("HttpOnly", header)
    r.assert_in("SameSite=Lax", header)
    
    print("test_cookie_to_headers: done")
    return r


def test_cookie_jar_basic():
    """Test CookieJar basic operations."""
    r = TestResult()
    
    jar = CookieJar()
    r.assert_equal(len(jar), 0)
    
    # Add cookie
    c = Cookie(name="session", value="abc123")
    jar.add(c)
    r.assert_equal(len(jar), 1)
    
    # Get cookie
    retrieved = jar.get("session")
    r.assert_is_not_none(retrieved)
    r.assert_equal(retrieved.value, "abc123")
    
    # Contains check
    r.assert_true("session" in jar)
    r.assert_false("nonexistent" in jar)
    
    # Remove cookie
    removed = jar.remove("session")
    r.assert_true(removed)
    r.assert_equal(len(jar), 0)
    r.assert_is_none(jar.get("session"))
    
    # Remove non-existent
    removed = jar.remove("nope")
    r.assert_false(removed)
    
    # Clear
    jar.add(Cookie(name="a", value="1"))
    jar.add(Cookie(name="b", value="2"))
    jar.clear()
    r.assert_equal(len(jar), 0)
    
    print("test_cookie_jar_basic: done")
    return r


def test_cookie_jar_update():
    """Test CookieJar updates replace existing cookies."""
    r = TestResult()
    
    jar = CookieJar()
    
    # Add initial cookie
    jar.add(Cookie(name="session", value="old"))
    r.assert_equal(jar.get("session").value, "old")
    
    # Update with same key
    jar.add(Cookie(name="session", value="new"))
    r.assert_equal(len(jar), 1)
    r.assert_equal(jar.get("session").value, "new")
    
    # Different domain = different cookie
    jar.add(Cookie(name="session", value="domain", domain="other.com"))
    r.assert_equal(len(jar), 2)
    
    # Different path = different cookie
    jar.add(Cookie(name="session", value="path", path="/app"))
    r.assert_equal(len(jar), 3)
    
    print("test_cookie_jar_update: done")
    return r


def test_cookie_jar_expiration():
    """Test CookieJar expiration handling."""
    r = TestResult()
    
    jar = CookieJar()
    
    # Add expired cookie - should not be added
    jar.add(Cookie(name="expired", value="old", expires=time.time() - 1000))
    r.assert_equal(len(jar), 0)
    
    # Add valid cookie
    jar.add(Cookie(name="valid", value="new", expires=time.time() + 1000))
    r.assert_equal(len(jar), 1)
    
    # Get for URL skips expired
    jar.add(Cookie(name="temp", value="x", expires=time.time() - 100))
    jar._cookies.append(Cookie(name="temp", value="x", expires=time.time() - 100))
    cookies = jar.get_all()
    r.assert_equal(len(cookies), 1)  # only "valid"
    
    # Clear expired
    jar.add(Cookie(name="exp1", value="1", expires=time.time() + 100))
    jar._cookies.append(Cookie(name="exp2", value="2", expires=time.time() - 100))
    removed = jar.clear_expired()
    r.assert_equal(removed, 1)
    r.assert_equal(len(jar), 2)
    
    print("test_cookie_jar_expiration: done")
    return r


def test_cookie_jar_url_matching():
    """Test CookieJar URL-based retrieval."""
    r = TestResult()
    
    jar = CookieJar()
    
    # Add various cookies
    jar.add(Cookie(name="global", value="1", domain="example.com", path="/"))
    jar.add(Cookie(name="api", value="2", domain="example.com", path="/api"))
    jar.add(Cookie(name="admin", value="3", domain="example.com", path="/admin", secure=True))
    jar.add(Cookie(name="other", value="4", domain="other.com", path="/"))
    jar.add(Cookie(name="js", value="5", domain="example.com", http_only=True))
    jar.add(Cookie(name="nojs", value="6", domain="example.com", http_only=False))
    
    # Get for URL
    cookies = jar.get_for_url("https://example.com/")
    names = {c.name for c in cookies}
    r.assert_in("global", names)
    r.assert_in("js", names)
    r.assert_in("nojs", names)
    r.assert_true(len(cookies) >= 3)
    
    # Path filtering
    cookies = jar.get_for_url("https://example.com/api/users")
    names = {c.name for c in cookies}
    r.assert_in("global", names)
    r.assert_in("api", names)
    r.assert_in("js", names)
    
    # Secure filtering
    cookies = jar.get_for_url("https://example.com/admin")
    names = {c.name for c in cookies}
    r.assert_in("admin", names)
    
    cookies = jar.get_for_url("http://example.com/admin")
    names = {c.name for c in cookies}
    r.assert_true("admin" not in names)
    
    # HttpOnly filtering
    cookies = jar.get_for_url("https://example.com/", http_only=False)
    names = {c.name for c in cookies}
    r.assert_true("js" not in names)
    r.assert_in("nojs", names)
    
    cookies = jar.get_for_url("https://example.com/", http_only=True)
    names = {c.name for c in cookies}
    r.assert_in("js", names)
    
    # Cookie header
    header = jar.get_cookie_header("https://example.com/")
    r.assert_in("global=1", header)
    
    print("test_cookie_jar_url_matching: done")
    return r


def test_cookie_jar_serialization():
    """Test CookieJar serialization."""
    r = TestResult()
    
    jar = CookieJar()
    jar.add(Cookie(name="a", value="1", domain="example.com"))
    jar.add(Cookie(name="b", value="2", path="/app", secure=True))
    
    # To dict
    data = jar.to_dict()
    r.assert_equal(len(data), 2)
    r.assert_equal(data[0]["name"], "a")
    r.assert_equal(data[0]["value"], "1")
    
    # From dict
    jar2 = CookieJar.from_dict(data)
    r.assert_equal(len(jar2), 2)
    r.assert_equal(jar2.get("a").value, "1")
    r.assert_equal(jar2.get("b").secure, True)
    
    # JSON round-trip
    json_str = json.dumps(data)
    loaded = json.loads(json_str)
    jar3 = CookieJar.from_dict(loaded)
    r.assert_equal(len(jar3), 2)
    
    print("test_cookie_jar_serialization: done")
    return r


def test_cookie_jar_update_from_headers():
    """Test updating jar from Set-Cookie headers."""
    r = TestResult()
    
    jar = CookieJar()
    
    headers = [
        "session=abc123; Path=/; HttpOnly",
        "user=john; Domain=example.com; Max-Age=3600",
    ]
    
    count = jar.update_from_headers(headers)
    r.assert_equal(count, 2)
    r.assert_equal(len(jar), 2)
    r.assert_equal(jar.get("session").value, "abc123")
    r.assert_equal(jar.get("user").domain, "example.com")
    
    print("test_cookie_jar_update_from_headers: done")
    return r


def test_validate_cookie_name():
    """Test cookie name validation."""
    r = TestResult()
    
    # Valid names
    r.assert_true(validate_cookie_name("session"))
    r.assert_true(validate_cookie_name("SESSION_ID"))
    r.assert_true(validate_cookie_name("user-id"))
    r.assert_true(validate_cookie_name("token_123"))
    r.assert_true(validate_cookie_name("a"))
    
    # Invalid names
    r.assert_false(validate_cookie_name(""))
    r.assert_false(validate_cookie_name("session id"))  # space
    r.assert_false(validate_cookie_name("name=value"))  # =
    r.assert_false(validate_cookie_name("a;b"))  # semicolon
    r.assert_false(validate_cookie_name("a,b"))  # comma
    r.assert_false(validate_cookie_name("a(b)"))  # parentheses
    r.assert_false(validate_cookie_name("a<b>"))  # angle brackets
    r.assert_false(validate_cookie_name("a@b"))  # at sign
    r.assert_false(validate_cookie_name("a:b"))  # colon
    r.assert_false(validate_cookie_name("a[b]"))  # brackets
    r.assert_false(validate_cookie_name("a{b}"))  # braces
    r.assert_false(validate_cookie_name("a?b"))  # question mark
    r.assert_false(validate_cookie_name("a/b"))  # slash
    r.assert_false(validate_cookie_name("name\t"))  # tab
    
    print("test_validate_cookie_name: done")
    return r


def test_validate_cookie_value():
    """Test cookie value validation."""
    r = TestResult()
    
    # Valid values
    r.assert_true(validate_cookie_value(""))
    r.assert_true(validate_cookie_value("abc123"))
    r.assert_true(validate_cookie_value("session_token_xyz"))
    r.assert_true(validate_cookie_value("user@example"))
    r.assert_true(validate_cookie_value("a-b_c.d"))
    
    # Invalid values
    r.assert_false(validate_cookie_value("a b"))  # space
    r.assert_false(validate_cookie_value("a;b"))  # semicolon
    r.assert_false(validate_cookie_value("a,b"))  # comma
    r.assert_false(validate_cookie_value('"quoted"'))  # double quote
    r.assert_false(validate_cookie_value("a\tb"))  # tab
    
    print("test_validate_cookie_value: done")
    return r


def test_encode_decode_value():
    """Test Base64 encoding/decoding for cookie values."""
    r = TestResult()
    
    # Basic encoding
    encoded = encode_cookie_value("hello world")
    r.assert_true(validate_cookie_value(encoded))
    decoded = decode_cookie_value(encoded)
    r.assert_equal(decoded, "hello world")
    
    # Special characters
    text = "special: ;, \"quotes\" and spaces"
    encoded = encode_cookie_value(text)
    r.assert_true(validate_cookie_value(encoded))
    decoded = decode_cookie_value(encoded)
    r.assert_equal(decoded, text)
    
    # Unicode
    unicode_text = "用户名 🍪"
    encoded = encode_cookie_value(unicode_text)
    r.assert_true(validate_cookie_value(encoded))
    decoded = decode_cookie_value(encoded)
    r.assert_equal(decoded, unicode_text)
    
    # Empty string
    encoded = encode_cookie_value("")
    decoded = decode_cookie_value(encoded)
    r.assert_equal(decoded, "")
    
    print("test_encode_decode_value: done")
    return r


def test_same_site_matches():
    """Test SameSite policy matching."""
    r = TestResult()
    
    # Strict - same site only
    r.assert_true(same_site_matches("Strict", "example.com", "example.com", True))
    r.assert_true(same_site_matches("Strict", "example.com", "example.com", False))
    r.assert_false(same_site_matches("Strict", "example.com", "other.com", True))
    r.assert_false(same_site_matches("Strict", "example.com", "other.com", False))
    
    # Lax - same site or top-level navigation
    r.assert_true(same_site_matches("Lax", "example.com", "example.com", True))
    r.assert_true(same_site_matches("Lax", "example.com", "other.com", True))
    r.assert_false(same_site_matches("Lax", "example.com", "other.com", False))
    
    # None - cross-site allowed, but needs secure
    r.assert_true(same_site_matches("None", "example.com", "other.com", True))
    r.assert_false(same_site_matches("None", "example.com", "other.com", False))
    
    # None (null) - default Lax behavior
    r.assert_true(same_site_matches(None, "example.com", "example.com", False))
    r.assert_false(same_site_matches(None, "example.com", "other.com", False))
    
    print("test_same_site_matches: done")
    return r


def test_make_session_cookie():
    """Test session cookie factory."""
    r = TestResult()
    
    c = make_session_cookie("session", "abc123")
    r.assert_equal(c.name, "session")
    r.assert_equal(c.value, "abc123")
    r.assert_is_none(c.expires)
    r.assert_false(c.persistent)
    r.assert_true(c.http_only)
    r.assert_equal(c.same_site, "Lax")
    
    # Custom options
    c2 = make_session_cookie("token", "xyz", path="/api", secure=True, same_site="Strict")
    r.assert_equal(c2.path, "/api")
    r.assert_true(c2.secure)
    r.assert_equal(c2.same_site, "Strict")
    
    print("test_make_session_cookie: done")
    return r


def test_make_persistent_cookie():
    """Test persistent cookie factory."""
    r = TestResult()
    
    c = make_persistent_cookie("remember", "user123", max_age=86400)
    r.assert_equal(c.name, "remember")
    r.assert_equal(c.value, "user123")
    r.assert_equal(c.max_age, 86400)
    r.assert_is_not_none(c.expires)
    r.assert_true(c.persistent)
    
    # Check expiration is approximately correct
    expected_expiry = time.time() + 86400
    r.assert_true(abs(c.expires - expected_expiry) < 1)
    
    # Custom options
    c2 = make_persistent_cookie(
        "pref", "dark", max_age=3600,
        domain="example.com", path="/settings",
        http_only=False
    )
    r.assert_equal(c2.domain, "example.com")
    r.assert_equal(c2.path, "/settings")
    r.assert_false(c2.http_only)
    
    print("test_make_persistent_cookie: done")
    return r


def test_parse_expires():
    """Test Expires date parsing."""
    r = TestResult()
    
    # RFC 1123 format
    ts = _parse_expires("Wed, 09 Jun 2021 10:18:14 GMT")
    r.assert_is_not_none(ts)
    
    # Various formats
    ts = _parse_expires("Wed, 09-Jun-2021 10:18:14 GMT")
    r.assert_is_not_none(ts)
    
    ts = _parse_expires("Wednesday, 09-Jun-21 10:18:14 GMT")
    r.assert_is_not_none(ts)
    
    # Invalid date
    ts = _parse_expires("invalid date")
    r.assert_is_none(ts)
    
    ts = _parse_expires("")
    r.assert_is_none(ts)
    
    print("test_parse_expires: done")
    return r


def test_cookie_copy():
    """Test cookie copying."""
    r = TestResult()
    
    original = Cookie(
        name="session",
        value="abc123",
        domain="example.com",
        path="/app",
        secure=True,
        http_only=True,
        same_site="Strict",
    )
    
    copy = original.copy()
    
    r.assert_equal(copy.name, original.name)
    r.assert_equal(copy.value, original.value)
    r.assert_equal(copy.domain, original.domain)
    r.assert_equal(copy.path, original.path)
    r.assert_equal(copy.secure, original.secure)
    r.assert_equal(copy.http_only, original.http_only)
    r.assert_equal(copy.same_site, original.same_site)
    
    # Modify copy shouldn't affect original
    copy.value = "changed"
    r.assert_equal(original.value, "abc123")
    
    print("test_cookie_copy: done")
    return r


def test_cookie_jar_iteration():
    """Test CookieJar iteration."""
    r = TestResult()
    
    jar = CookieJar()
    jar.add(Cookie(name="a", value="1"))
    jar.add(Cookie(name="b", value="2"))
    jar.add(Cookie(name="c", value="3"))
    
    names = []
    for cookie in jar:
        names.append(cookie.name)
    
    r.assert_equal(len(names), 3)
    r.assert_true("a" in names)
    r.assert_true("b" in names)
    r.assert_true("c" in names)
    
    print("test_cookie_jar_iteration: done")
    return r


def test_boundary_values():
    """Test boundary values and edge cases."""
    r = TestResult()
    
    # Empty cookie value
    c = Cookie(name="empty", value="")
    r.assert_equal(c.value, "")
    r.assert_equal(c.to_header(), "empty=")
    
    # Very long value
    long_value = "x" * 4000
    c = Cookie(name="long", value=long_value)
    r.assert_equal(len(c.value), 4000)
    
    # Unicode in name/value (should be allowed in dataclass)
    c = Cookie(name="用户", value="会话")
    r.assert_equal(c.name, "用户")
    r.assert_equal(c.value, "会话")
    
    # Max-Age=0 (immediate expiration)
    c = Cookie(name="delete", value="", max_age=0)
    r.assert_true(c.is_expired())
    
    # Negative Max-Age (immediate expiration)
    c = Cookie(name="del2", value="", max_age=-1)
    r.assert_true(c.is_expired())
    
    # Empty jar operations
    jar = CookieJar()
    r.assert_equal(jar.get_cookie_header("https://example.com/"), "")
    r.assert_equal(jar.get_for_url("https://example.com/"), [])
    
    # None values
    r.assert_is_none(parse_set_cookie(None))
    r.assert_equal(len(parse_cookie_header(None)), 0)
    
    print("test_boundary_values: done")
    return r


def run_all_tests():
    """Run all tests and report results."""
    print("Running cookie_utils tests...")
    print("=" * 60)
    
    results = [
        test_cookie_creation(),
        test_cookie_expiration(),
        test_cookie_domain_matching(),
        test_cookie_path_matching(),
        test_cookie_matches_url(),
        test_parse_set_cookie(),
        test_parse_cookie_header(),
        test_build_cookie_header(),
        test_cookie_to_headers(),
        test_cookie_jar_basic(),
        test_cookie_jar_update(),
        test_cookie_jar_expiration(),
        test_cookie_jar_url_matching(),
        test_cookie_jar_serialization(),
        test_cookie_jar_update_from_headers(),
        test_validate_cookie_name(),
        test_validate_cookie_value(),
        test_encode_decode_value(),
        test_same_site_matches(),
        test_make_session_cookie(),
        test_make_persistent_cookie(),
        test_parse_expires(),
        test_cookie_copy(),
        test_cookie_jar_iteration(),
        test_boundary_values(),
    ]
    
    total_passed = sum(r.passed for r in results)
    total_failed = sum(r.failed for r in results)
    total = total_passed + total_failed
    
    print(f"\n{'='*60}")
    print(f"TOTAL: {total_passed}/{total} tests passed")
    print(f"{'='*60}")
    
    if total_failed > 0:
        print(f"\nFailed tests:")
        for i, result in enumerate(results, 1):
            if result.failed > 0:
                print(f"  Test {i}: {result.failed} failures")
                for err in result.errors[:3]:
                    print(f"    - {err}")
        return False
    
    return True


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
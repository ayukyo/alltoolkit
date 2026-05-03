"""
Cookie Utils Usage Examples

Demonstrates practical usage of cookie_utils for HTTP cookie handling.
"""

import sys
import os
import json

# Add module directory to path
module_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, module_dir)

from mod import (
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


def example_basic_parsing():
    """Basic cookie parsing examples."""
    print("\n" + "="*60)
    print("Example 1: Basic Cookie Parsing")
    print("="*60)
    
    # Parse Set-Cookie header
    set_cookie = "session=abc123xyz; Domain=example.com; Path=/app; Secure; HttpOnly; SameSite=Lax"
    cookie = parse_set_cookie(set_cookie)
    
    print(f"\nSet-Cookie: {set_cookie}")
    print(f"Parsed cookie:")
    print(f"  Name: {cookie.name}")
    print(f"  Value: {cookie.value}")
    print(f"  Domain: {cookie.domain}")
    print(f"  Path: {cookie.path}")
    print(f"  Secure: {cookie.secure}")
    print(f"  HttpOnly: {cookie.http_only}")
    print(f"  SameSite: {cookie.same_site}")
    
    # Parse Cookie header
    cookie_header = "session=abc123xyz; user=john_doe; theme=dark"
    parsed = parse_cookie_header(cookie_header)
    
    print(f"\nCookie header: {cookie_header}")
    print(f"Parsed: {parsed}")
    
    # Build Cookie header
    rebuilt = build_cookie_header(parsed)
    print(f"Rebuilt: {rebuilt}")


def example_cookie_jar():
    """CookieJar usage examples."""
    print("\n" + "="*60)
    print("Example 2: CookieJar Management")
    print("="*60)
    
    jar = CookieJar()
    
    # Add cookies from various domains
    cookies = [
        Cookie(name="session", value="abc123", domain="example.com", http_only=True),
        Cookie(name="user", value="john", domain="example.com", path="/users"),
        Cookie(name="cart", value="items", domain="shop.example.com"),
        Cookie(name="analytics", value="xyz", domain="analytics.com"),
        Cookie(name="admin", value="token", domain="example.com", path="/admin", secure=True),
    ]
    
    for c in cookies:
        jar.add(c)
    
    print(f"\nAdded {len(cookies)} cookies to jar")
    print(f"Total cookies in jar: {len(jar)}")
    
    # Get cookies for different URLs
    urls = [
        "https://example.com/",
        "https://example.com/users/profile",
        "https://shop.example.com/products",
        "https://example.com/admin/settings",
        "http://example.com/admin",  # Should not include secure cookies
    ]
    
    for url in urls:
        cookies_for_url = jar.get_for_url(url)
        header = jar.get_cookie_header(url)
        print(f"\nURL: {url}")
        print(f"  Cookies: {[c.name for c in cookies_for_url]}")
        print(f"  Header: {header or '(none)'}")


def example_session_vs_persistent():
    """Session vs persistent cookies."""
    print("\n" + "="*60)
    print("Example 3: Session vs Persistent Cookies")
    print("="*60)
    
    # Session cookie
    session = make_session_cookie(
        name="session_id",
        value="user_session_abc123",
        http_only=True,
        same_site="Lax"
    )
    
    print(f"\nSession Cookie:")
    print(f"  Set-Cookie: {session.to_set_cookie()}")
    print(f"  Persistent: {session.persistent}")
    print(f"  Expires: {session.expires or 'None (session)'}")
    
    # Persistent cookie
    remember = make_persistent_cookie(
        name="remember_me",
        value="user_token_xyz",
        max_age=86400 * 30,  # 30 days
        domain="example.com",
        secure=True,
        http_only=True,
        same_site="Strict"
    )
    
    print(f"\nPersistent Cookie (30 days):")
    print(f"  Set-Cookie: {remember.to_set_cookie()}")
    print(f"  Persistent: {remember.persistent}")
    print(f"  Expires: {remember.expires}")
    
    # Calculate remaining time
    if remember.expires:
        import time
        remaining = remember.expires - time.time()
        days = remaining / 86400
        print(f"  Remaining: {days:.1f} days")


def example_expiration_handling():
    """Cookie expiration handling."""
    print("\n" + "="*60)
    print("Example 4: Expiration Handling")
    print("="*60)
    
    import time
    
    jar = CookieJar()
    
    # Add cookies with different expiration times
    now = time.time()
    
    jar.add(Cookie(name="expired", value="old", expires=now - 1000))
    jar.add(Cookie(name="valid", value="good", expires=now + 3600))
    jar.add(Cookie(name="short", value="temp", max_age=60))
    jar.add(Cookie(name="permanent", value="long", expires=now + 365 * 24 * 3600))
    
    print(f"\nAdded 4 cookies (one already expired)")
    print(f"Jar count: {len(jar)} (expired cookie not counted)")
    
    # Check individual expiration
    for name in ["expired", "valid", "short", "permanent"]:
        cookie = jar.get(name)
        if cookie:
            status = "expired" if cookie.is_expired() else "valid"
            remaining = cookie.expires - time.time() if cookie.expires else 0
            print(f"  {name}: {status} ({remaining:.0f} seconds remaining)")
        else:
            print(f"  {name}: not in jar")
    
    # Clear expired
    removed = jar.clear_expired()
    print(f"\nCleared {removed} expired cookies")


def example_validation():
    """Cookie validation examples."""
    print("\n" + "="*60)
    print("Example 5: Cookie Validation")
    print("="*60)
    
    # Name validation
    names = [
        "session_id",      # Valid
        "user-name",       # Valid
        "bad name",        # Invalid (space)
        "name=value",      # Invalid (=)
        "a;b",             # Invalid (;)
        "valid_123",       # Valid
    ]
    
    print("\nName Validation:")
    for name in names:
        valid = validate_cookie_name(name)
        status = "✓" if valid else "✗"
        print(f"  {status} '{name}'")
    
    # Value validation
    values = [
        "abc123",          # Valid
        "hello world",     # Invalid (space)
        "a;b",             # Invalid (;)
        "good_value",      # Valid
        "bad,comma",       # Invalid (,)
    ]
    
    print("\nValue Validation:")
    for value in values:
        valid = validate_cookie_value(value)
        status = "✓" if valid else "✗"
        print(f"  {status} '{value}'")
    
    # Safe encoding for problematic values
    print("\nSafe Encoding:")
    unsafe = "hello world; with,special"
    encoded = encode_cookie_value(unsafe)
    decoded = decode_cookie_value(encoded)
    
    print(f"  Original: '{unsafe}'")
    print(f"  Encoded: '{encoded}'")
    print(f"  Decoded: '{decoded}'")
    print(f"  Encoded valid: {validate_cookie_value(encoded)}")


def example_samesite_policy():
    """SameSite policy examples."""
    print("\n" + "="*60)
    print("Example 6: SameSite Policy")
    print("="*60)
    
    scenarios = [
        ("Strict", "example.com", "example.com", True),
        ("Strict", "example.com", "other.com", True),
        ("Lax", "example.com", "example.com", True),
        ("Lax", "example.com", "other.com", True),
        ("Lax", "example.com", "other.com", False),  # Not HTTPS
        ("None", "example.com", "other.com", True),
        ("None", "example.com", "other.com", False),  # Not HTTPS
    ]
    
    print("\nSameSite Matching Results:")
    print("  SameSite | From        | To          | HTTPS | Result")
    print("  ---------|-------------|-------------|-------|--------")
    
    for same_site, from_site, to_site, is_secure in scenarios:
        matches = same_site_matches(same_site, from_site, to_site, is_secure)
        result = "✓ Allowed" if matches else "✗ Blocked"
        print(f"  {same_site:8} | {from_site:11} | {to_site:11} | {str(is_secure):5} | {result}")


def example_serialization():
    """Cookie serialization examples."""
    print("\n" + "="*60)
    print("Example 7: Serialization")
    print("="*60)
    
    jar = CookieJar()
    
    # Add some cookies
    jar.add(Cookie(name="session", value="abc123", domain="example.com", http_only=True))
    jar.add(Cookie(name="user", value="john", domain="example.com", path="/users"))
    jar.add(Cookie(name="pref", value="dark", domain="example.com", max_age=3600))
    
    # Serialize to dict
    data = jar.to_dict()
    
    print("\nSerialized cookies:")
    for item in data:
        print(f"  {item['name']}: {item['value']}")
    
    # Convert to JSON
    json_str = json.dumps(data, indent=2)
    print(f"\nJSON representation:\n{json_str}")
    
    # Deserialize back
    jar2 = CookieJar.from_dict(data)
    print(f"\nDeserialized jar has {len(jar2)} cookies")
    
    # Verify round-trip
    for name in ["session", "user", "pref"]:
        c1 = jar.get(name)
        c2 = jar2.get(name)
        if c1 and c2:
            match = c1.value == c2.value
            print(f"  {name}: values match ✓")


def example_web_session_simulation():
    """Simulate a web session with cookies."""
    print("\n" + "="*60)
    print("Example 8: Web Session Simulation")
    print("="*60)
    
    jar = CookieJar()
    
    # Step 1: Login response
    print("\nStep 1: User logs in, server sends Set-Cookie headers")
    login_headers = [
        "session=user_session_token_abc123; Domain=example.com; Path=/; HttpOnly; SameSite=Lax",
        "csrf_token=xyz789; Path=/; SameSite=Strict",
        "user_pref=dark_mode; Path=/; Max-Age=86400",
    ]
    
    count = jar.update_from_headers(login_headers)
    print(f"  Received {count} cookies")
    print(f"  Cookies in jar: {[c.name for c in jar.get_all()]}")
    
    # Step 2: API request
    print("\nStep 2: Make API request")
    api_url = "https://example.com/api/users"
    cookie_header = jar.get_cookie_header(api_url)
    print(f"  URL: {api_url}")
    print(f"  Cookie header: {cookie_header}")
    
    # Step 3: Cross-site request
    print("\nStep 3: Cross-site form submission")
    cross_url = "https://other.com/submit"
    cross_header = jar.get_cookie_header(cross_url)
    print(f"  URL: {cross_url}")
    print(f"  Cookie header: {cross_header or '(none - blocked by SameSite)'}")
    
    # Step 4: Admin page
    print("\nStep 4: Admin page (HTTPS)")
    admin_url = "https://example.com/admin/dashboard"
    admin_cookies = jar.get_for_url(admin_url)
    print(f"  URL: {admin_url}")
    print(f"  Cookies sent: {[c.name for c in admin_cookies]}")


def example_cookie_attributes():
    """Cookie attribute combinations."""
    print("\n" + "="*60)
    print("Example 9: Cookie Attribute Combinations")
    print("="*60)
    
    configurations = [
        # Name, cookie params, description
        ("Basic", {"name": "basic", "value": "val"}, "Simple cookie"),
        ("Secure", {"name": "secure", "value": "val", "secure": True}, "HTTPS only"),
        ("HttpOnly", {"name": "http", "value": "val", "http_only": True}, "No JavaScript access"),
        ("Secure+HttpOnly", {"name": "both", "value": "val", "secure": True, "http_only": True}, "Best security"),
        ("SameSite-Strict", {"name": "strict", "value": "val", "same_site": "Strict"}, "Same-site only"),
        ("SameSite-Lax", {"name": "lax", "value": "val", "same_site": "Lax"}, "Top-level navigation OK"),
        ("SameSite-None", {"name": "none", "value": "val", "same_site": "None", "secure": True}, "Cross-site allowed"),
        ("WithPath", {"name": "path", "value": "val", "path": "/api"}, "Path restricted"),
        ("WithDomain", {"name": "domain", "value": "val", "domain": ".example.com"}, "Subdomain shared"),
    ]
    
    print("\nCookie configurations:")
    for desc, params, explanation in configurations:
        cookie = Cookie(**params)
        header = cookie.to_set_cookie()
        print(f"\n{desc} ({explanation}):")
        print(f"  {header}")


def run_all_examples():
    """Run all examples."""
    print("="*60)
    print("Cookie Utils Usage Examples")
    print("="*60)
    
    example_basic_parsing()
    example_cookie_jar()
    example_session_vs_persistent()
    example_expiration_handling()
    example_validation()
    example_samesite_policy()
    example_serialization()
    example_web_session_simulation()
    example_cookie_attributes()
    
    print("\n" + "="*60)
    print("All examples completed!")
    print("="*60)


if __name__ == "__main__":
    run_all_examples()
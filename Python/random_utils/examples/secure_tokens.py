#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AllToolkit - Secure Token Generation Examples

Demonstrates secure token generation for authentication, verification, and API keys.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    secure_random_bytes, secure_random_int, secure_random_float,
    secure_random_choice, random_token, random_password, random_uuid,
    random_string, random_id
)


def generate_api_key():
    """Generate a secure API key."""
    return f"sk-{random_token(32)}"


def generate_verification_code(length=6):
    """Generate a numeric verification code."""
    charset = '0123456789'
    return random_string(length, charset, secure=True)


def generate_session_id():
    """Generate a secure session identifier."""
    return f"sess_{random_uuid()}"


def generate_reset_token():
    """Generate a password reset token."""
    return f"reset_{random_token(24, url_safe=True)}"


def generate_oauth_state():
    """Generate OAuth state parameter."""
    return random_token(16, url_safe=True)


def generate_csrf_token():
    """Generate CSRF protection token."""
    return random_token(32, url_safe=True)


def main():
    print("="*60)
    print("Secure Token Generation Examples")
    print("="*60)
    
    # API Keys
    print("\n1. API Keys")
    print("-"*40)
    for i in range(3):
        print(f"   API Key {i+1}: {generate_api_key()}")
    
    # Verification Codes
    print("\n2. Verification Codes")
    print("-"*40)
    for i in range(5):
        code = generate_verification_code()
        print(f"   Code {i+1}: {code}")
    
    # Session IDs
    print("\n3. Session IDs")
    print("-"*40)
    for i in range(3):
        print(f"   Session {i+1}: {generate_session_id()}")
    
    # Reset Tokens
    print("\n4. Password Reset Tokens")
    print("-"*40)
    for i in range(3):
        print(f"   Reset Token {i+1}: {generate_reset_token()}")
    
    # OAuth State
    print("\n5. OAuth State Parameters")
    print("-"*40)
    for i in range(3):
        print(f"   State {i+1}: {generate_oauth_state()}")
    
    # CSRF Tokens
    print("\n6. CSRF Tokens")
    print("-"*40)
    for i in range(3):
        print(f"   CSRF Token {i+1}: {generate_csrf_token()}")
    
    # Secure Random Values
    print("\n7. Secure Random Values")
    print("-"*40)
    print(f"   Random bytes (32): {secure_random_bytes(32).hex()}")
    print(f"   Random int (1-1000000): {secure_random_int(1, 1000000)}")
    print(f"   Random float: {secure_random_float():.10f}")
    
    # User IDs
    print("\n8. User IDs")
    print("-"*40)
    for i in range(5):
        print(f"   User ID {i+1}: {random_id('user', length=8, timestamp=False)}")
    
    print("\n" + "="*60)
    print("Security Tips:")
    print("  - Always use secure=True for sensitive tokens")
    print("  - Use url_safe=True for tokens in URLs")
    print("  - Store tokens securely (hashed for passwords)")
    print("  - Set appropriate expiration times")
    print("="*60)


if __name__ == "__main__":
    main()

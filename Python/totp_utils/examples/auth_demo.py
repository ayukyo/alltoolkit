#!/usr/bin/env python3
"""
TOTP Authentication Demo

This example demonstrates how to:
1. Generate a TOTP secret for a new user
2. Create an otpauth URL for QR code generation
3. Verify TOTP codes
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import TOTPUtils, generate_secret, generate_backup_codes


def setup_new_account(username: str, issuer: str = "MyApp"):
    """
    Set up TOTP for a new account.
    Returns setup information including QR code URL.
    """
    # Generate a new secret
    secret = generate_secret(20)
    
    # Create TOTP instance
    totp = TOTPUtils(secret)
    
    # Generate otpauth URL for QR code
    otpauth_url = totp.get_otpauth_url(issuer, username)
    
    # Generate QR code URL
    qr_url = totp.get_qr_code_url(issuer, username)
    
    # Generate backup codes
    backup_codes = generate_backup_codes(10, 8)
    
    return {
        'secret': secret,
        'otpauth_url': otpauth_url,
        'qr_url': qr_url,
        'backup_codes': backup_codes
    }


def verify_login(secret: str, user_code: str) -> bool:
    """
    Verify a TOTP code during login.
    Uses tolerance=1 to allow slight time drift.
    """
    totp = TOTPUtils(secret)
    return totp.verify(user_code, tolerance=1)


def main():
    print("=" * 60)
    print("TOTP Authentication Demo")
    print("=" * 60)
    
    # Simulate account setup
    username = "alice@example.com"
    issuer = "SecureApp"
    
    print(f"\n📱 Setting up TOTP for: {username}")
    print("-" * 60)
    
    # Setup new account
    setup = setup_new_account(username, issuer)
    
    print(f"\n🔑 Secret Key: {setup['secret']}")
    print("\n📋 Instructions for user:")
    print("  1. Install Google Authenticator or similar app")
    print("  2. Scan the QR code at the URL below")
    print("  3. Enter the 6-digit code to verify")
    
    print(f"\n📷 QR Code URL:")
    print(f"  {setup['qr_url']}")
    
    print(f"\n🔗 otpauth URL (for manual entry):")
    print(f"  {setup['otpauth_url']}")
    
    print(f"\n💾 Backup Codes (save these safely):")
    for code in setup['backup_codes']:
        print(f"  • {code}")
    
    # Simulate verification
    print("\n" + "-" * 60)
    print("🔐 Verification Demo")
    print("-" * 60)
    
    totp = TOTPUtils(setup['secret'])
    
    # Generate current code (simulating what user sees in their app)
    current_code = totp.generate()
    remaining = totp.get_remaining_seconds()
    
    print(f"\n⏱️  Current code (simulating authenticator app): {current_code}")
    print(f"   Valid for: {remaining} more seconds")
    
    # Verify the code
    is_valid = verify_login(setup['secret'], current_code)
    print(f"\n✅ Verification result: {'SUCCESS' if is_valid else 'FAILED'}")
    
    # Test with wrong code
    wrong_code = "000000"
    is_valid_wrong = verify_login(setup['secret'], wrong_code)
    print(f"❌ Wrong code verification: {'SUCCESS' if is_valid_wrong else 'FAILED (expected)'}")
    
    print("\n" + "=" * 60)
    print("Demo complete!")
    print("=" * 60)


if __name__ == '__main__':
    main()
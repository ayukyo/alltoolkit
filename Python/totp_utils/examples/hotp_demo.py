#!/usr/bin/env python3
"""
HOTP (Counter-based OTP) Demo

This example demonstrates counter-based one-time passwords,
which are useful for offline scenarios or when time-sync isn't reliable.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import HOTPUtils, generate_secret


def main():
    print("=" * 60)
    print("HOTP (Counter-based OTP) Demo")
    print("=" * 60)
    
    # Generate secret
    secret = generate_secret(20)
    print(f"\n🔑 Secret: {secret}")
    
    # Create HOTP instance
    hotp = HOTPUtils(secret)
    
    print("\n📊 Generating codes with incrementing counter:")
    print("-" * 40)
    print("  Counter | Code")
    print("-" * 40)
    
    codes = []
    for counter in range(10):
        code = hotp.generate(counter)
        codes.append(code)
        print(f"    {counter:4d}  | {code}")
    
    print("-" * 40)
    
    # Verification demo
    print("\n🔐 Verification Demo:")
    print("-" * 40)
    
    # Valid verification
    test_counter = 5
    test_code = codes[test_counter]
    is_valid = hotp.verify(test_code, test_counter)
    print(f"  Counter {test_counter}, Code {test_code}: {'✅ VALID' if is_valid else '❌ INVALID'}")
    
    # Wrong counter
    is_valid_wrong_counter = hotp.verify(test_code, test_counter + 1)
    print(f"  Counter {test_counter + 1}, Code {test_code}: {'✅ VALID' if is_valid_wrong_counter else '❌ INVALID (expected)'}")
    
    # Wrong code
    is_valid_wrong_code = hotp.verify("000000", test_counter)
    print(f"  Counter {test_counter}, Code 000000: {'✅ VALID' if is_valid_wrong_code else '❌ INVALID (expected)'}")
    
    # 8-digit codes
    print("\n🔢 8-digit HOTP Demo:")
    hotp8 = HOTPUtils(secret, digits=8)
    for counter in range(3):
        code = hotp8.generate(counter)
        print(f"  Counter {counter}: {code}")
    
    # Different algorithms
    print("\n🔒 Different Hash Algorithms:")
    for algo in ['sha1', 'sha256', 'sha512']:
        hotp_algo = HOTPUtils(secret, algorithm=algo)
        code = hotp_algo.generate(0)
        print(f"  {algo.upper():8s}: {code}")
    
    print("\n" + "=" * 60)
    print("Demo complete!")
    print("=" * 60)
    print("\n💡 Use cases for HOTP:")
    print("  • Offline authentication")
    print("  • SMS/email delivered codes")
    print("  • Print-out backup codes")
    print("  • Hardware tokens without clocks")


if __name__ == '__main__':
    main()
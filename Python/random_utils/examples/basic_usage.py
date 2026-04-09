#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AllToolkit - Random Utils Basic Usage Examples

Demonstrates common use cases for the random_utils module.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    random_string, random_password, random_uuid, random_token,
    random_int, random_float, random_choice, random_sample,
    random_datetime, random_email, random_ipv4, random_color,
    secure_random_bytes, secure_random_int, roll_dice, roll_d20, coin_flip
)


def main():
    print("="*60)
    print("Random Utils - Basic Usage Examples")
    print("="*60)
    
    # 1. Random Strings
    print("\n1. Random Strings")
    print("-"*40)
    print(f"   Simple string (16 chars): {random_string(16)}")
    print(f"   Simple string (32 chars): {random_string(32)}")
    print(f"   Hex string: {random_string(16, charset='0123456789abcdef')}")
    
    # 2. Passwords
    print("\n2. Passwords")
    print("-"*40)
    print(f"   Default password: {random_password(16)}")
    print(f"   No special chars: {random_password(16, use_special=False)}")
    print(f"   Digits only: {random_password(8, use_lowercase=False, use_uppercase=False, use_special=False)}")
    
    # 3. UUIDs and Tokens
    print("\n3. UUIDs and Tokens")
    print("-"*40)
    print(f"   UUID v4: {random_uuid()}")
    print(f"   Token: {random_token()}")
    print(f"   URL-safe token: {random_token(url_safe=True)}")
    
    # 4. Random Numbers
    print("\n4. Random Numbers")
    print("-"*40)
    print(f"   Random int (1-100): {random_int(1, 100)}")
    print(f"   Random float: {random_float():.6f}")
    print(f"   Secure random int: {secure_random_int(1, 100)}")
    
    # 5. Selection
    print("\n5. Random Selection")
    print("-"*40)
    fruits = ['apple', 'banana', 'cherry', 'date', 'elderberry']
    print(f"   From {fruits}")
    print(f"   Choice: {random_choice(fruits)}")
    print(f"   Sample (3): {random_sample(fruits, 3)}")
    
    # 6. Dates
    print("\n6. Random Dates")
    print("-"*40)
    from datetime import datetime
    start = datetime(2020, 1, 1)
    end = datetime(2025, 12, 31)
    dt = random_datetime(start, end)
    print(f"   Between 2020 and 2025: {dt.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 7. Test Data
    print("\n7. Test Data Generation")
    print("-"*40)
    print(f"   Email: {random_email()}")
    print(f"   Email (custom): {random_email('company.com')}")
    print(f"   IPv4: {random_ipv4()}")
    print(f"   IPv4 (private): {random_ipv4(private=True)}")
    print(f"   Color (hex): {random_color('hex')}")
    print(f"   Color (rgb): {random_color('rgb')}")
    
    # 8. Secure Random
    print("\n8. Secure Random")
    print("-"*40)
    print(f"   Secure bytes (16): {secure_random_bytes(16).hex()}")
    print(f"   Secure int (1-1000): {secure_random_int(1, 1000)}")
    
    # 9. Games
    print("\n9. Games")
    print("-"*40)
    print(f"   Roll 2d6: {roll_dice(6, 2)}")
    print(f"   Roll 1d20: {roll_d20()}")
    print(f"   Coin flip: {coin_flip()}")
    
    print("\n" + "="*60)
    print("Examples completed!")
    print("="*60)


if __name__ == "__main__":
    main()

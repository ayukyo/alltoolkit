#!/usr/bin/env python3
"""
TOTP Manager Demo - Multi-Account Management

This example shows how to manage TOTP for multiple accounts.
"""

import sys
import os
import time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import TOTPManager, generate_secret


def print_codes(manager: TOTPManager):
    """Print all current codes."""
    codes = manager.get_all_codes()
    
    print("\n┌" + "─" * 50 + "┐")
    print("│ {:<20} {:<12} {:<12} │".format("Account", "Code", "Expires In"))
    print("├" + "─" * 50 + "┤")
    
    for name, info in codes.items():
        issuer = info.get('issuer', '')
        print("│ {:<20} {:<12} {:<12}s │".format(
            name[:20], info['code'], info['remaining']
        ))
    
    print("└" + "─" * 50 + "┘")


def main():
    print("=" * 60)
    print("TOTP Manager - Multi-Account Demo")
    print("=" * 60)
    
    manager = TOTPManager()
    
    # Add accounts
    print("\n📝 Adding accounts...")
    
    accounts = [
        ("GitHub", "GitHub", generate_secret()),
        ("Google", "Google", generate_secret()),
        ("AWS", "Amazon Web Services", generate_secret()),
        ("Dropbox", "Dropbox", generate_secret()),
        ("Twitter", "Twitter", generate_secret()),
    ]
    
    for name, issuer, secret in accounts:
        manager.add_account(name, secret, issuer)
        print(f"  ✓ Added: {name}")
    
    # List accounts
    print(f"\n📋 Registered accounts: {', '.join(manager.list_accounts())}")
    
    # Display codes
    print("\n🔑 Current TOTP codes:")
    print_codes(manager)
    
    # Watch codes change (demo)
    print("\n⏱️  Watching codes update (5 seconds)...")
    print("   (In a real app, this would auto-refresh)")
    
    for i in range(5, 0, -1):
        print(f"\r   Refreshing in {i}s...  ", end='', flush=True)
        time.sleep(1)
    
    print("\r" + " " * 30 + "\r", end='')
    print_codes(manager)
    
    # Get specific account
    print("\n🔍 Getting code for specific account:")
    result = manager.get_code("GitHub")
    if result:
        code, remaining = result
        print(f"   GitHub: {code} (expires in {remaining}s)")
    
    # Remove an account
    print("\n🗑️  Removing account: Twitter")
    manager.remove_account("Twitter")
    print(f"   Remaining accounts: {', '.join(manager.list_accounts())}")
    
    print("\n" + "=" * 60)
    print("Demo complete!")
    print("=" * 60)


if __name__ == '__main__':
    main()
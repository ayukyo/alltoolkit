#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Shamir's Secret Sharing Examples
==============================================
Practical examples demonstrating Shamir's Secret Sharing usage.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    split_secret, reconstruct_secret,
    split_string, split_bytes, split_int,
    reconstruct_secret_bytes, reconstruct_secret_string,
    verify_secret_hash,
    ShamirSecretSharing,
    Share, ShareSet,
    split_bytes_gf256, reconstruct_bytes_gf256,
    encode_shares_compact, decode_shares_compact
)


def example_basic_usage():
    """Basic usage example."""
    print("\n" + "=" * 60)
    print("Example 1: Basic Secret Sharing")
    print("=" * 60)
    
    # The secret to protect
    secret = "My super secret API key: sk-1234567890abcdef"
    
    # Split into 5 shares, need 3 to reconstruct
    print(f"\nOriginal secret: {secret}")
    print("Splitting into 5 shares (need 3 to reconstruct)...")
    
    shareset = split_string(secret, threshold=3, num_shares=5)
    
    print(f"\nGenerated {len(shareset.shares)} shares:")
    for i, share in enumerate(shareset.shares):
        print(f"  Share {i+1}: x={share.x}")
    
    # Store shares separately (simulated)
    print("\n--- Distributing shares to different parties ---")
    print("Alice gets Share 1")
    print("Bob gets Share 2")
    print("Charlie gets Share 3")
    print("Diana gets Share 4")
    print("Eve gets Share 5")
    
    # Reconstruct with any 3 shares
    print("\n--- Reconstructing with shares from Alice, Bob, Diana ---")
    subset = [shareset.shares[0], shareset.shares[1], shareset.shares[3]]
    reconstructed = reconstruct_secret_string(subset)
    
    print(f"Reconstructed: {reconstructed}")
    print(f"Success: {reconstructed == secret}")


def example_password_sharing():
    """Example: Sharing a master password."""
    print("\n" + "=" * 60)
    print("Example 2: Master Password Sharing")
    print("=" * 60)
    
    # A master password that needs to be backed up
    master_password = "MyM@sterP@ssw0rd!2024#Secure"
    
    print(f"\nMaster password: {master_password}")
    print("Creating backup scheme with 3-of-5 sharing...")
    
    # Create 5 shares, need 3 to reconstruct
    shareset = split_string(master_password, threshold=3, num_shares=5)
    
    # Save shares to different locations (simulated)
    locations = [
        "Encrypted USB drive",
        "Cloud storage (encrypted)",
        "Password manager backup",
        "Physical safe",
        "Trusted family member"
    ]
    
    print("\nStoring shares at different locations:")
    for i, (share, location) in enumerate(zip(shareset.shares, locations)):
        encoded = share.encode()
        print(f"  {i+1}. {location}")
        print(f"     Share: {encoded[:40]}...")
    
    print("\n--- Emergency Recovery Scenario ---")
    print("Need to recover password, but only have access to:")
    print("  - Cloud storage (Share 2)")
    print("  - Physical safe (Share 4)")
    print("  - Family member (Share 5)")
    
    recovery_shares = [shareset.shares[1], shareset.shares[3], shareset.shares[4]]
    recovered = reconstruct_secret_string(recovery_shares)
    
    print(f"\nRecovered password: {recovered}")
    print(f"Match: {recovered == master_password}")


def example_api_key_backup():
    """Example: Backing up API keys."""
    print("\n" + "=" * 60)
    print("Example 3: API Key Backup System")
    print("=" * 60)
    
    # Multiple API keys to protect
    api_keys = {
        "aws_access_key": "AKIAIOSFODNN7EXAMPLE",
        "aws_secret_key": "example_secret_key_for_demo_only",
        "stripe_key": "sk_example_key_for_demonstration",
        "github_token": "ghp_example_token_for_demo_only"
    }
    
    print("\nProtecting multiple API keys with 2-of-3 sharing...")
    
    for name, key in api_keys.items():
        shareset = split_string(key, threshold=2, num_shares=3)
        
        print(f"\n{name}:")
        print(f"  Original: {key[:20]}...")
        print(f"  Share 1 (Primary admin): {shareset.shares[0].encode()[:30]}...")
        print(f"  Share 2 (Backup admin): {shareset.shares[1].encode()[:30]}...")
        print(f"  Share 3 (Emergency contact): {shareset.shares[2].encode()[:30]}...")


def example_encryption_key():
    """Example: Protecting an encryption key."""
    print("\n" + "=" * 60)
    print("Example 4: Encryption Key Protection")
    print("=" * 60)
    
    # A 256-bit encryption key (32 bytes)
    import secrets as sec
    encryption_key = sec.token_bytes(32)
    
    print(f"\n256-bit encryption key: {encryption_key.hex()[:32]}...")
    print("Splitting with 4-of-6 scheme (high security)...")
    
    shareset = split_bytes(encryption_key, threshold=4, num_shares=6)
    
    print(f"\nGenerated {len(shareset.shares)} shares")
    print(f"SHA-256 hash: {shareset.secret_hash}")
    
    # Simulate distribution
    trustees = ["CEO", "CTO", "CFO", "Legal", "Board Member 1", "Board Member 2"]
    
    print("\nDistributing to trustees:")
    for i, (share, trustee) in enumerate(zip(shareset.shares, trustees)):
        print(f"  {trustee}: Share {i+1} (x={share.x})")
    
    print("\n--- Key Ceremony Scenario ---")
    print("4 trustees must be present to recover the key")
    print("Participating: CEO, CTO, Legal, Board Member 1")
    
    ceremony_shares = [
        shareset.shares[0],  # CEO
        shareset.shares[1],  # CTO
        shareset.shares[3],  # Legal
        shareset.shares[4],  # Board Member 1
    ]
    
    recovered_key = reconstruct_secret_bytes(ceremony_shares, expected_length=32)
    
    print(f"\nRecovered key: {recovered_key.hex()[:32]}...")
    print(f"Key matches: {recovered_key == encryption_key}")
    
    # Verify hash
    print(f"Hash verification: {verify_secret_hash(shareset, recovered_key)}")


def example_class_interface():
    """Example: Using the class interface."""
    print("\n" + "=" * 60)
    print("Example 5: Class Interface")
    print("=" * 60)
    
    # Create a reusable sharing instance
    sss = ShamirSecretSharing(threshold=3, num_shares=5)
    
    print("Created ShamirSecretSharing instance (3-of-5)")
    
    # Share different secrets with same parameters
    secrets_to_share = [
        b"Binary data example",
        "Text string example",
        12345678901234567890
    ]
    
    for secret in secrets_to_share:
        print(f"\nSharing: {secret if isinstance(secret, (str, int)) else secret.decode()}")
        
        shares = sss.split(secret)
        
        # Convert int to proper format for comparison
        if isinstance(secret, int):
            reconstructed = sss.reconstruct(shares.shares[:3])
            print(f"  Reconstructed integer: {reconstructed}")
            print(f"  Match: {reconstructed == secret}")
        elif isinstance(secret, str):
            reconstructed = sss.reconstruct_string(shares.shares[:3])
            print(f"  Reconstructed string: {reconstructed}")
            print(f"  Match: {reconstructed == secret}")
        else:
            reconstructed = sss.reconstruct_bytes(shares.shares[:3])
            print(f"  Reconstructed bytes: {reconstructed}")
            print(f"  Match: {reconstructed == secret}")


def example_gf256_binary():
    """Example: GF(2^8) binary data sharing."""
    print("\n" + "=" * 60)
    print("Example 6: GF(2^8) Binary Data Sharing")
    print("=" * 60)
    
    # Binary data of any length
    data = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR..."  # Simulated PNG header
    
    print(f"\nBinary data: {data.hex()}")
    print("Splitting with GF(2^8) arithmetic (efficient for arbitrary-length data)")
    
    shares = split_bytes_gf256(data, threshold=3, num_shares=5)
    
    print(f"\nGenerated {len(shares)} shares:")
    for i, share in enumerate(shares):
        print(f"  Share {i+1}: {share.hex()}")
    
    print("\nReconstructing with shares 1, 3, 5:")
    reconstructed = reconstruct_bytes_gf256([shares[0], shares[2], shares[4]])
    print(f"  Result: {reconstructed.hex()}")
    print(f"  Match: {reconstructed == data}")


def example_serialization():
    """Example: Share serialization and storage."""
    print("\n" + "=" * 60)
    print("Example 7: Share Serialization")
    print("=" * 60)
    
    secret = "Serialize this secret!"
    shareset = split_string(secret, threshold=2, num_shares=3)
    
    print(f"\nOriginal secret: {secret}")
    
    # Method 1: ShareSet encoding
    print("\n--- ShareSet encoding (all shares together) ---")
    encoded_set = shareset.encode()
    print(f"Encoded:\n{encoded_set[:100]}...")
    
    decoded_set = ShareSet.decode(encoded_set)
    reconstructed = reconstruct_secret_string(decoded_set.shares[:2])
    print(f"Reconstructed: {reconstructed}")
    
    # Method 2: Compact encoding
    print("\n--- Compact encoding (for storage/transmission) ---")
    compact = encode_shares_compact(shareset.shares)
    print(f"Compact: {compact[:80]}...")
    
    decoded_shares = decode_shares_compact(compact)
    reconstructed = reconstruct_secret_string(decoded_shares[:2])
    print(f"Reconstructed: {reconstructed}")
    
    # Method 3: Individual share encoding
    print("\n--- Individual share encoding ---")
    for i, share in enumerate(shareset.shares):
        encoded = share.encode()
        decoded = Share.decode(encoded)
        print(f"  Share {i+1}: {encoded[:40]}... (x={decoded.x})")


def example_digital_inheritance():
    """Example: Digital inheritance planning."""
    print("\n" + "=" * 60)
    print("Example 8: Digital Inheritance Planning")
    print("=" * 60)
    
    # A master document containing digital legacy information
    master_document = """
    DIGITAL LEGACY DOCUMENT
    =======================
    Password Manager: LastPass - Master Password: Tr0ub4dor&3
    Email: recovery@protonmail.com - Password: C0rr3ct-H0rs3-B4tt3ry-St4pl3
    Crypto Wallet: Seed phrase: abandon ability able about above absent absorb abstract absurd abuse access accident
    Bank: Chase - Username: john.doe@email.com - Password: MyS3cur3B4nk!
    Social Media: [All passwords stored in Bitwarden backup]
    """
    
    print("\nMaster document length:", len(master_document), "characters")
    print("Creating 5-of-7 inheritance scheme...")
    
    shareset = split_string(master_document, threshold=5, num_shares=7)
    
    heirs = [
        ("Spouse", "Primary heir"),
        ("Eldest child", "Secondary heir"),
        ("Second child", "Tertiary heir"),
        ("Family lawyer", "Legal representative"),
        ("Financial advisor", "Professional trustee"),
        ("Best friend", "Trusted confidant"),
        ("Safety deposit box", "Physical backup")
    ]
    
    print("\nDistributing shares to heirs:")
    for i, (heir, role) in enumerate(heirs):
        print(f"  {i+1}. {heir} ({role})")
        print(f"     Share: {shareset.shares[i].encode()[:50]}...")
    
    print("\n--- Inheritance Ceremony ---")
    print("5 of 7 heirs must be present to access the digital legacy")
    print("Any 4 heirs alone cannot recover the document (information-theoretic security)")


def example_secure_message():
    """Example: Secure message transmission."""
    print("\n" + "=" * 60)
    print("Example 9: Secure Message Transmission")
    print("=" * 60)
    
    message = "The package will arrive at 3 PM. Confirm receipt."
    
    print(f"\nMessage to transmit: {message}")
    print("Splitting into 3 shares, any 2 can reconstruct")
    print("Sending via 3 different channels...")
    
    shareset = split_string(message, threshold=2, num_shares=3)
    
    channels = [
        ("Email", "share1@email.com"),
        ("SMS", "+1-555-0100"),
        ("Encrypted chat", "@secure_user")
    ]
    
    print("\nTransmitting shares:")
    for i, ((channel, dest), share) in enumerate(zip(channels, shareset.shares)):
        print(f"  Channel {i+1} ({channel} to {dest})")
        print(f"    Share: {share.encode()[:40]}...")
    
    print("\n--- Receiver Scenario ---")
    print("Receiver got shares from Email and SMS")
    received = reconstruct_secret_string([shareset.shares[0], shareset.shares[1]])
    print(f"Reconstructed message: {received}")
    
    # Even if one channel is intercepted, attacker can't read message
    print("\n--- Security Analysis ---")
    print("If Email is intercepted (Share 1): Attacker has only 1 share")
    print("Single share reveals ZERO information about the secret")
    print("This is information-theoretic security!")


def run_all_examples():
    """Run all examples."""
    print("=" * 60)
    print("Shamir's Secret Sharing - Practical Examples")
    print("=" * 60)
    
    example_basic_usage()
    example_password_sharing()
    example_api_key_backup()
    example_encryption_key()
    example_class_interface()
    example_gf256_binary()
    example_serialization()
    example_digital_inheritance()
    example_secure_message()
    
    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    run_all_examples()
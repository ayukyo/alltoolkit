"""
AllToolkit - Encryption Utils Basic Usage Examples

Simple examples demonstrating common encryption and security operations.
"""

import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    hash_data, hash_password, verify_password,
    compute_hmac, verify_hmac,
    generate_token, generate_api_key, generate_session_id,
    base64_encode, base64_decode,
    xor_encrypt, xor_decrypt,
    quick_hash, quick_encrypt, quick_decrypt,
    HashAlgorithm,
)


def main():
    print("=" * 60)
    print("AllToolkit - Encryption Utils Basic Examples")
    print("=" * 60)
    print()
    
    # 1. Basic Hashing
    print("1. Basic Hashing")
    print("-" * 40)
    
    data = "Hello, World!"
    result = hash_data(data)
    
    print(f"  Original: {data}")
    print(f"  Algorithm: {result.algorithm}")
    print(f"  SHA256: {result.hex_digest}")
    print(f"  Input length: {result.input_length} bytes")
    print()
    
    # Different algorithms
    print("  Different algorithms:")
    for algo in [HashAlgorithm.SHA256, HashAlgorithm.SHA512, HashAlgorithm.MD5]:
        r = hash_data(data, algorithm=algo)
        print(f"    {algo}: {r.hex_digest[:32]}...")
    print()
    
    # 2. Password Hashing
    print("2. Password Hashing")
    print("-" * 40)
    
    password = "MyS3cur3P@ssw0rd!"
    hashed = hash_password(password)
    
    print(f"  Password: {password}")
    print(f"  Algorithm: {hashed['algorithm']}")
    print(f"  Iterations: {hashed['iterations']}")
    print(f"  Salt: {hashed['salt'][:20]}...")
    print(f"  Hash: {hashed['hash'][:20]}...")
    
    # Verify
    is_valid = verify_password(password, hashed)
    print(f"  Verify (correct): {is_valid}")
    
    is_invalid = verify_password("wrong_password", hashed)
    print(f"  Verify (wrong): {is_invalid}")
    print()
    
    # 3. HMAC Signature
    print("3. HMAC Signature")
    print("-" * 40)
    
    message = "Important message to sign"
    secret_key = "my_secret_key"
    
    signature = compute_hmac(message, secret_key)
    print(f"  Message: {message}")
    print(f"  Signature: {signature}")
    
    # Verify valid
    valid = verify_hmac(message, signature, secret_key)
    print(f"  Verify (valid): {valid}")
    
    # Verify tampered
    invalid = verify_hmac("Tampered message", signature, secret_key)
    print(f"  Verify (tampered): {invalid}")
    print()
    
    # 4. Token Generation
    print("4. Token Generation")
    print("-" * 40)
    
    token = generate_token()
    print(f"  Standard token: {token}")
    
    url_token = generate_token(url_safe=True)
    print(f"  URL-safe token: {url_token}")
    
    api_key = generate_api_key(prefix="sk")
    print(f"  API key: {api_key}")
    
    session_id = generate_session_id()
    print(f"  Session ID: {session_id[:32]}...")
    print()
    
    # 5. Base64 Encoding
    print("5. Base64 Encoding")
    print("-" * 40)
    
    original = "Secret data to encode"
    encoded = base64_encode(original)
    decoded = base64_decode(encoded).decode('utf-8')
    
    print(f"  Original: {original}")
    print(f"  Encoded: {encoded}")
    print(f"  Decoded: {decoded}")
    print(f"  Match: {original == decoded}")
    print()
    
    # 6. XOR Encryption (Educational)
    print("6. XOR Encryption (Educational Only)")
    print("-" * 40)
    
    secret = "Confidential message"
    key = "mykey"
    
    encrypted = xor_encrypt(secret, key)
    decrypted = xor_decrypt(encrypted, key).decode('utf-8')
    
    print(f"  Original: {secret}")
    print(f"  Encrypted (hex): {encrypted.hex()[:40]}...")
    print(f"  Decrypted: {decrypted}")
    print(f"  Match: {secret == decrypted}")
    print()
    
    # 7. Quick Functions
    print("7. Quick Convenience Functions")
    print("-" * 40)
    
    quick = quick_hash("test")
    print(f"  Quick hash: {quick}")
    
    encrypted_quick = quick_encrypt("secret", "key")
    decrypted_quick = quick_decrypt(encrypted_quick, "key").decode('utf-8')
    print(f"  Quick encrypt/decrypt: {decrypted_quick}")
    print()
    
    # 8. Hash Verification
    print("8. Hash Verification")
    print("-" * 40)
    
    from mod import verify_hash
    
    data = "Verify this data"
    h = hash_data(data)
    
    print(f"  Data: {data}")
    print(f"  Hash: {h.hex_digest}")
    
    valid = verify_hash(data, h.hex_digest)
    print(f"  Verify (correct): {valid}")
    
    invalid = verify_hash("Wrong data", h.hex_digest)
    print(f"  Verify (wrong): {invalid}")
    print()
    
    print("=" * 60)
    print("Examples completed!")
    print("=" * 60)


if __name__ == '__main__':
    main()

"""
Passphrase Utilities - Usage Examples

Demonstrates practical usage of password and passphrase generation utilities.
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from passphrase_utils.mod import (
    generate_password,
    generate_passphrase,
    generate_pronounceable,
    generate_pin,
    generate_token,
    generate_hex_token,
    analyze_password,
    check_password_pwned,
    calculate_entropy,
    generate_diceware,
    suggest_improvements,
    is_strong_password,
    generate_password_variants,
    estimate_crack_time,
    create_memorable_password,
    batch_generate,
    get_word_list_stats,
    PasswordStyle,
)


def example_basic_password():
    """Basic password generation examples."""
    print("\n" + "=" * 50)
    print("Example 1: Basic Password Generation")
    print("=" * 50)
    
    # Default 16-character password
    password = generate_password()
    print(f"\nDefault password (16 chars): {password}")
    
    # Short password (8 chars)
    short = generate_password(length=8)
    print(f"Short password (8 chars): {short}")
    
    # Long password (32 chars)
    long = generate_password(length=32)
    print(f"Long password (32 chars): {long}")
    
    # Without symbols (alphanumeric only)
    alphanumeric = generate_password(length=16, symbols=False)
    print(f"Alphanumeric only: {alphanumeric}")
    
    # Only lowercase letters
    lowercase = generate_password(length=12, uppercase=False, digits=False, symbols=False)
    print(f"Lowercase only: {lowercase}")


def example_password_requirements():
    """Password with minimum character requirements."""
    print("\n" + "=" * 50)
    print("Example 2: Password with Minimum Requirements")
    print("=" * 50)
    
    # Require at least 2 lowercase, 2 uppercase, 2 digits, 1 symbol
    password = generate_password(
        length=12,
        min_lowercase=2,
        min_uppercase=2,
        min_digits=2,
        min_symbols=1,
    )
    print(f"\nPassword with min requirements: {password}")
    
    strength = analyze_password(password)
    print(f"Strength: {strength.rating} (score: {strength.score})")
    print(f"Entropy: {strength.entropy} bits")


def example_exclude_ambiguous():
    """Exclude ambiguous characters."""
    print("\n" + "=" * 50)
    print("Example 3: Exclude Ambiguous Characters")
    print("=" * 50)
    
    # Without ambiguous chars (0, O, 1, l, I)
    safe = generate_password(length=16, exclude_ambiguous=True)
    print(f"\nSafe password (no ambiguous chars): {safe}")
    
    # With ambiguous chars (default)
    full = generate_password(length=16, exclude_ambiguous=False)
    print(f"Full charset password: {full}")


def example_custom_chars():
    """Custom character set."""
    print("\n" + "=" * 50)
    print("Example 4: Custom Character Set")
    print("=" * 50)
    
    # Only use specific characters
    simple = generate_password(length=8, custom_chars="abc123XYZ")
    print(f"\nCustom charset (abc123XYZ): {simple}")
    
    # URL-safe characters only
    url_safe = generate_password(length=16, custom_chars="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_")
    print(f"URL-safe password: {url_safe}")


def example_passphrase():
    """Passphrase generation examples."""
    print("\n" + "=" * 50)
    print("Example 5: Passphrase Generation")
    print("=" * 50)
    
    # Default 4-word passphrase with dash separator
    phrase = generate_passphrase()
    print(f"\nDefault passphrase: {phrase}")
    
    # 6 words with space separator
    six_words = generate_passphrase(word_count=6, separator=' ')
    print(f"6 words, space separator: {six_words}")
    
    # Capitalized words
    capitalized = generate_passphrase(capitalize=True)
    print(f"Capitalized: {capitalized}")
    
    # With appended number
    with_number = generate_passphrase(include_number=True)
    print(f"With number: {with_number}")
    
    # Combined: capitalized + number
    combined = generate_passphrase(capitalize=True, include_number=True, separator='_')
    print(f"Capitalized + number + underscore: {combined}")


def example_diceware():
    """Diceware-style passphrase."""
    print("\n" + "=" * 50)
    print("Example 6: Diceware Passphrase")
    print("=" * 50)
    
    # Standard Diceware (5 words)
    dice = generate_diceware()
    print(f"\nStandard Diceware (5 words): {dice}")
    
    # More words for higher security
    dice7 = generate_diceware(word_count=7)
    print(f"7-word Diceware: {dice7}")
    
    entropy = calculate_entropy(dice7)
    print(f"Entropy: {entropy} bits")


def example_pronounceable():
    """Pronounceable password examples."""
    print("\n" + "=" * 50)
    print("Example 7: Pronounceable Passwords")
    print("=" * 50)
    
    # Basic pronounceable
    pron1 = generate_pronounceable()
    print(f"\nBasic pronounceable: {pron1}")
    
    # Longer
    pron2 = generate_pronounceable(length=16)
    print(f"Longer (16 chars): {pron2}")
    
    # With digits
    pron3 = generate_pronounceable(include_digits=True)
    print(f"With digits: {pron3}")
    
    # With symbols
    pron4 = generate_pronounceable(include_symbols=True)
    print(f"With symbols: {pron4}")


def example_pins_and_tokens():
    """PIN and token generation."""
    print("\n" + "=" * 50)
    print("Example 8: PINs and Tokens")
    print("=" * 50)
    
    # Various PIN lengths
    pin4 = generate_pin(length=4)
    pin6 = generate_pin()
    pin8 = generate_pin(length=8)
    
    print(f"\n4-digit PIN: {pin4}")
    print(f"6-digit PIN (default): {pin6}")
    print(f"8-digit PIN: {pin8}")
    
    # Tokens
    token32 = generate_token()
    token16 = generate_token(length=16)
    hex_token = generate_hex_token()
    
    print(f"\nURL-safe token (32 chars): {token32}")
    print(f"Short token (16 chars): {token16}")
    print(f"Hex token: {hex_token}")


def example_strength_analysis():
    """Password strength analysis."""
    print("\n" + "=" * 50)
    print("Example 9: Password Strength Analysis")
    print("=" * 50)
    
    passwords = [
        "password",
        "password123",
        "P@ssw0rd",
        "MySecureP@ssw0rd2024",
        "Correct-Horse-Battery-Staple",
    ]
    
    print("\nAnalyzing various passwords:")
    print("-" * 50)
    
    for pwd in passwords:
        result = analyze_password(pwd)
        print(f"\nPassword: {pwd}")
        print(f"  Score: {result.score}/100")
        print(f"  Rating: {result.rating}")
        print(f"  Entropy: {result.entropy} bits")
        print(f"  Crack time: {result.crack_time}")
        if result.issues:
            print(f"  Issues: {result.issues[0]}")


def example_crack_time():
    """Crack time estimation."""
    print("\n" + "=" * 50)
    print("Example 10: Crack Time Estimation")
    print("=" * 50)
    
    passwords = [
        ("123456", "Very weak"),
        ("password", "Common"),
        ("MyP@ssw0rd", "Medium"),
        ("MyVerySecureP@ssw0rd123!", "Strong"),
        ("Correct-Horse-Battery-Staple-2024!", "Very strong"),
    ]
    
    print("\nCrack time at 10 billion guesses/sec:")
    print("-" * 50)
    
    for pwd, desc in passwords:
        time = estimate_crack_time(pwd)
        print(f"{desc}: {pwd[:20]}... -> {time}")


def example_breach_check():
    """Check for breached passwords."""
    print("\n" + "=" * 50)
    print("Example 11: Breach Detection")
    print("=" * 50)
    
    passwords = ["password", "123456", "qwerty", "MyUniqueP@ssw0rd123!"]
    
    print("\nChecking passwords against breach database:")
    print("-" * 50)
    
    for pwd in passwords:
        is_breached = check_password_pwned(pwd)
        status = "⚠️ BREACHED" if is_breached else "✓ Safe"
        print(f"{pwd}: {status}")


def example_improvements():
    """Password improvement suggestions."""
    print("\n" + "=" * 50)
    print("Example 12: Improvement Suggestions")
    print("=" * 50)
    
    passwords = ["password", "pass123", "mypassword"]
    
    for pwd in passwords:
        print(f"\nPassword: {pwd}")
        suggestions = suggest_improvements(pwd)
        print("Suggestions:")
        for s in suggestions[:3]:
            print(f"  - {s}")


def example_strong_check():
    """Strong password validation."""
    print("\n" + "=" * 50)
    print("Example 13: Password Validation")
    print("=" * 50)
    
    passwords = [
        "short",
        "password",
        "Password123",
        "MySecureP@ssw0rd123",
    ]
    
    print("\nValidating passwords (min 12 chars, all types):")
    print("-" * 50)
    
    for pwd in passwords:
        is_strong, issues = is_strong_password(
            pwd,
            min_length=12,
            require_uppercase=True,
            require_lowercase=True,
            require_digits=True,
            require_symbols=True,
        )
        status = "✓ Pass" if is_strong else "✗ Fail"
        print(f"{pwd}: {status}")
        if issues:
            print(f"  Issues: {', '.join(issues)}")


def example_memorable_password():
    """Memorable password creation."""
    print("\n" + "=" * 50)
    print("Example 14: Memorable Password Creation")
    print("=" * 50)
    
    # With pattern (Word-Number-Symbol-Word)
    mem1 = create_memorable_password()
    print(f"\nWith pattern: {mem1}")
    
    # Without pattern
    mem2 = create_memorable_password(include_pattern=False)
    print(f"Without pattern: {mem2}")
    
    # Custom separator
    mem3 = create_memorable_password(separator='_')
    print(f"Underscore separator: {mem3}")


def example_password_variants():
    """Password variants from a base word."""
    print("\n" + "=" * 50)
    print("Example 15: Password Variants")
    print("=" * 50)
    
    base_word = "security"
    
    print(f"\nVariants from base word '{base_word}':")
    print("-" * 50)
    
    # Mixed style
    mixed = generate_password_variants(base_word, count=5, style="mixed")
    for i, v in enumerate(mixed, 1):
        print(f"  Mixed {i}: {v}")
    
    # Leet style
    leet = generate_password_variants(base_word, count=3, style="leet")
    for i, v in enumerate(leet, 1):
        print(f"  Leet {i}: {v}")
    
    # Numbers style
    nums = generate_password_variants(base_word, count=3, style="numbers")
    for i, v in enumerate(nums, 1):
        print(f"  Numbers {i}: {v}")


def example_batch_generation():
    """Batch password generation."""
    print("\n" + "=" * 50)
    print("Example 16: Batch Generation")
    print("=" * 50)
    
    # Batch of random passwords
    print("\n10 random passwords (12 chars):")
    random_batch = batch_generate(10, PasswordStyle.RANDOM, length=12)
    for i, pwd in enumerate(random_batch, 1):
        print(f"  {i}. {pwd}")
    
    # Batch of passphrases
    print("\n5 passphrases (3 words):")
    phrase_batch = batch_generate(5, PasswordStyle.PASSPHRASE, word_count=3)
    for i, phrase in enumerate(phrase_batch, 1):
        print(f"  {i}. {phrase}")
    
    # Batch of PINs
    print("\n5 4-digit PINs:")
    pin_batch = batch_generate(5, PasswordStyle.PIN, length=4)
    for i, pin in enumerate(pin_batch, 1):
        print(f"  {i}. {pin}")


def example_word_list_stats():
    """Word list statistics."""
    print("\n" + "=" * 50)
    print("Example 17: Word List Statistics")
    print("=" * 50)
    
    # Default word list stats
    stats = get_word_list_stats()
    
    print("\nDefault word list statistics:")
    print("-" * 50)
    print(f"  Word count: {stats['word_count']}")
    print(f"  Min length: {stats['min_length']} chars")
    print(f"  Max length: {stats['max_length']} chars")
    print(f"  Avg length: {stats['avg_length']} chars")
    print(f"  Unique words: {stats['unique_words']}")
    
    # Entropy of passphrase using this word list
    entropy_per_word = math.log2(stats['word_count'])
    print(f"\nEntropy per word: {entropy_per_word:.2f} bits")
    print(f"Entropy for 4 words: {entropy_per_word * 4:.2f} bits")
    print(f"Entropy for 5 words: {entropy_per_word * 5:.2f} bits")


def example_practical_use_cases():
    """Practical use case scenarios."""
    print("\n" + "=" * 50)
    print("Example 18: Practical Use Cases")
    print("=" * 50)
    
    # 1. API Key generation
    print("\n1. API Key:")
    api_key = generate_token(32)
    print(f"   {api_key}")
    
    # 2. User password with requirements
    print("\n2. User password (meeting common requirements):")
    user_pwd = generate_password(
        length=14,
        min_lowercase=1,
        min_uppercase=1,
        min_digits=1,
        min_symbols=1,
        exclude_ambiguous=True,
    )
    print(f"   {user_pwd}")
    is_strong, issues = is_strong_password(user_pwd, min_length=8)
    print(f"   Validation: {is_strong}")
    
    # 3. WiFi password
    print("\n3. WiFi password (memorable passphrase):")
    wifi_pwd = generate_passphrase(word_count=4, capitalize=True, separator='')
    print(f"   {wifi_pwd}")
    
    # 4. Database password
    print("\n4. Database password (strong random):")
    db_pwd = generate_password(length=24)
    print(f"   {db_pwd}")
    print(f"   Strength: {analyze_password(db_pwd).rating}")
    
    # 5. OTP/PIN for authentication
    print("\n5. Authentication OTP:")
    otp = generate_pin(length=6)
    print(f"   {otp}")
    
    # 6. Session token
    print("\n6. Session token:")
    session_token = generate_hex_token(64)
    print(f"   {session_token}")


# Import math for entropy calculation
import math


def run_all_examples():
    """Run all example functions."""
    print("\n" + "=" * 70)
    print("PASSPHRASE UTILITIES - USAGE EXAMPLES")
    print("=" * 70)
    
    example_basic_password()
    example_password_requirements()
    example_exclude_ambiguous()
    example_custom_chars()
    example_passphrase()
    example_diceware()
    example_pronounceable()
    example_pins_and_tokens()
    example_strength_analysis()
    example_crack_time()
    example_breach_check()
    example_improvements()
    example_strong_check()
    example_memorable_password()
    example_password_variants()
    example_batch_generation()
    example_word_list_stats()
    example_practical_use_cases()
    
    print("\n" + "=" * 70)
    print("Examples completed!")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    run_all_examples()
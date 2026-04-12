"""
AllToolkit - Python Password Utilities - Usage Examples

This file demonstrates various use cases for the password_utils module.
Run: python examples/usage_examples.py
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from password_utils.mod import (
    PasswordUtils,
    StrengthLevel,
    generate_password,
    generate_passphrase,
    analyze,
    validate,
    hash_password,
    verify_password,
    is_weak,
    is_strong,
)


def print_section(title: str):
    """Print a section header."""
    print("\n" + "=" * 60)
    print(f" {title}")
    print("=" * 60)


def example_basic_generation():
    """Example 1: Basic Password Generation."""
    print_section("Example 1: Basic Password Generation")
    
    # Generate a default 16-character password
    pwd = generate_password()
    print(f"\nDefault password (16 chars): {pwd}")
    
    # Generate a 24-character password
    pwd = generate_password(length=24)
    print(f"24-character password: {pwd}")
    
    # Generate a 32-character password with no special characters
    pwd = generate_password(length=32, use_special=False)
    print(f"32 chars, no special: {pwd}")
    
    # Generate a password without ambiguous characters
    pwd = generate_password(length=20, exclude_ambiguous=True)
    print(f"No ambiguous chars: {pwd}")


def example_passphrase_generation():
    """Example 2: Passphrase Generation."""
    print_section("Example 2: Passphrase Generation")
    
    # Generate a default 4-word passphrase
    phrase = generate_passphrase()
    print(f"\nDefault passphrase: {phrase}")
    
    # Generate a 6-word passphrase
    phrase = generate_passphrase(word_count=6)
    print(f"6-word passphrase: {phrase}")
    
    # Generate with custom separator
    phrase = generate_passphrase(word_count=4, separator="_")
    print(f"Underscore separator: {phrase}")
    
    # Generate with number for extra security
    phrase = generate_passphrase(word_count=4, add_number=True)
    print(f"With number: {phrase}")
    
    # Generate without capitalization
    phrase = generate_passphrase(word_count=4, use_capitalization=False)
    print(f"Lowercase only: {phrase}")


def example_strength_analysis():
    """Example 3: Password Strength Analysis."""
    print_section("Example 3: Password Strength Analysis")
    
    passwords = [
        "123456",
        "password",
        "MyDog2024",
        "Tr0ub4dor&3",
        "K9#mP2$xL7@nQ5!wR8&vN3^tY6*uI1",
    ]
    
    for pwd in passwords:
        strength = analyze(pwd)
        print(f"\nPassword: {pwd}")
        print(f"  Strength: {strength.level.value}")
        print(f"  Score: {strength.score}/100")
        print(f"  Entropy: {strength.entropy_bits:.1f} bits")
        print(f"  Length: {strength.length}")
        
        if strength.issues:
            print(f"  Issues: {', '.join(strength.issues)}")
        if strength.suggestions:
            print(f"  Tips: {', '.join(strength.suggestions[:2])}")


def example_validation():
    """Example 4: Password Validation."""
    print_section("Example 4: Password Validation")
    
    utils = PasswordUtils()
    test_cases = [
        ("short", "Aa1!", None, None),
        ("no_upper", "abcdefgh1!", None, None),
        ("common", "password", None, None),
        ("with_username", "JohnDoe123!", "johndoe", None),
        ("valid", "K9#mP2$xL7@nQ5!", None, None),
    ]
    
    for name, pwd, username, email in test_cases:
        result = utils.validate(pwd, username=username, email=email)
        status = "✓ VALID" if result.is_valid else "✗ INVALID"
        print(f"\n{name}: {pwd}")
        print(f"  Status: {status}")
        
        if result.error_messages:
            print(f"  Errors: {', '.join(result.error_messages)}")


def example_hashing():
    """Example 5: Password Hashing and Verification."""
    print_section("Example 5: Password Hashing and Verification")
    
    # Hash a password
    password = "MySecurePassword123!"
    pwd_hash, salt = hash_password(password)
    
    print(f"\nOriginal password: {password}")
    print(f"Hash: {pwd_hash}")
    print(f"Salt: {salt}")
    
    # Verify correct password
    is_correct = verify_password(password, pwd_hash, salt)
    print(f"\nVerify correct password: {'✓ Match' if is_correct else '✗ No match'}")
    
    # Verify wrong password
    is_wrong = verify_password("WrongPassword", pwd_hash, salt)
    print(f"Verify wrong password: {'✓ Match' if is_wrong else '✗ No match'}")
    
    # Demo: Store and retrieve (simulated)
    print("\n--- Simulated Database Storage ---")
    stored_user = {
        "username": "alice",
        "password_hash": pwd_hash,
        "password_salt": salt,
    }
    print(f"Stored: {stored_user}")
    
    # Later: Verify login attempt
    login_attempt = "MySecurePassword123!"
    if verify_password(login_attempt, stored_user["password_hash"], 
                      stored_user["password_salt"]):
        print("Login: ✓ Access granted")
    else:
        print("Login: ✗ Access denied")


def example_crack_time():
    """Example 6: Crack Time Estimation."""
    print_section("Example 6: Crack Time Estimation")
    
    utils = PasswordUtils()
    passwords = [
        "123456",
        "password123",
        "MyDog2024",
        "Tr0ub4dor&3",
        "K9#mP2$xL7@nQ5!wR8&vN3^tY6*uI1",
    ]
    
    print("\nAssuming 10 billion guesses/second:\n")
    
    for pwd in passwords:
        info = utils.estimate_crack_time(pwd)
        strength = analyze(pwd)
        print(f"Password: {pwd}")
        print(f"  Entropy: {info['entropy_bits']} bits")
        print(f"  Time to crack: {info['time_to_crack']}")
        print()


def example_security_check():
    """Example 7: Complete Security Check."""
    print_section("Example 7: Complete Security Check")
    
    utils = PasswordUtils()
    
    def security_check(password: str, username: str = None) -> dict:
        """Perform a complete security check on a password."""
        strength = analyze(password)
        validation = utils.validate(password, username=username)
        crack_info = utils.estimate_crack_time(password)
        
        return {
            "password": password,
            "strength_level": strength.level.value,
            "strength_score": strength.score,
            "is_valid": validation.is_valid,
            "validation_errors": validation.error_messages,
            "time_to_crack": crack_info["time_to_crack"],
            "recommendations": strength.suggestions,
        }
    
    # Check a password
    result = security_check("MyPassword2024", username="john")
    
    print(f"\nSecurity Report for: {result['password']}")
    print(f"  Strength: {result['strength_level']} ({result['strength_score']}/100)")
    print(f"  Valid: {'Yes' if result['is_valid'] else 'No'}")
    print(f"  Crack time: {result['time_to_crack']}")
    
    if result['validation_errors']:
        print(f"  Validation issues:")
        for err in result['validation_errors']:
            print(f"    - {err}")
    
    if result['recommendations']:
        print(f"  Recommendations:")
        for rec in result['recommendations'][:3]:
            print(f"    - {rec}")


def example_custom_utils():
    """Example 8: Custom PasswordUtils Configuration."""
    print_section("Example 8: Custom Configuration")
    
    # Create utils with custom length limits
    utils = PasswordUtils(min_length=12, max_length=256)
    
    # Generate with custom settings
    pwd = utils.generate(
        length=24,
        use_lowercase=True,
        use_uppercase=True,
        use_digits=True,
        use_special=True,
        exclude_ambiguous=True,
        ensure_all_types=True,
    )
    print(f"\nCustom generated password: {pwd}")
    
    # Validate with stricter rules
    result = utils.validate(
        "Test123!",
        require_uppercase=True,
        require_lowercase=True,
        require_digit=True,
        require_special=True,
        check_common=True,
        check_sequential=True,
    )
    
    print(f"\nValidation with strict rules: {'✓ Valid' if result.is_valid else '✗ Invalid'}")
    if result.error_messages:
        for msg in result.error_messages:
            print(f"  - {msg}")


def example_batch_generation():
    """Example 9: Batch Password Generation."""
    print_section("Example 9: Batch Password Generation")
    
    # Generate multiple passwords for a team
    team_size = 5
    print(f"\nGenerating {team_size} passwords for new team members:\n")
    
    for i in range(1, team_size + 1):
        pwd = generate_password(length=16)
        print(f"  User {i}: {pwd}")
    
    # Generate recovery codes
    print(f"\nGenerating 10 recovery codes:\n")
    
    for i in range(1, 11):
        code = generate_password(
            length=12, 
            use_lowercase=False, 
            use_special=False,
            exclude_ambiguous=True
        )
        print(f"  Code {i}: {code}")


def main():
    """Run all examples."""
    print("\n" + "=" * 60)
    print(" AllToolkit Password Utilities - Usage Examples")
    print("=" * 60)
    
    example_basic_generation()
    example_passphrase_generation()
    example_strength_analysis()
    example_validation()
    example_hashing()
    example_crack_time()
    example_security_check()
    example_custom_utils()
    example_batch_generation()
    
    print("\n" + "=" * 60)
    print(" Examples completed!")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()

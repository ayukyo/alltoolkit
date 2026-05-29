"""
Tests for Passphrase Utilities

Comprehensive test suite for password and passphrase generation.
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
    PasswordStrength,
)


def test_generate_password():
    """Test random password generation."""
    print("Testing generate_password...")
    
    # Basic generation
    password = generate_password()
    assert len(password) == 16
    print(f"  Default password: {password}")
    
    # Custom length
    short = generate_password(length=8)
    assert len(short) == 8
    print(f"  Short password: {short}")
    
    long = generate_password(length=32)
    assert len(long) == 32
    print(f"  Long password: {long}")
    
    # No symbols
    no_symbols = generate_password(length=16, symbols=False)
    print(f"  No symbols: {no_symbols}")
    
    # Only lowercase
    lowercase_only = generate_password(length=16, uppercase=False, digits=False, symbols=False)
    assert lowercase_only.islower()
    print(f"  Lowercase only: {lowercase_only}")
    
    # Custom characters
    custom = generate_password(length=10, custom_chars="abc123")
    assert all(c in "abc123" for c in custom)
    print(f"  Custom chars: {custom}")
    
    # Minimum requirements
    min_req = generate_password(
        length=12,
        min_lowercase=2,
        min_uppercase=2,
        min_digits=2,
        min_symbols=1,
    )
    print(f"  With min requirements: {min_req}")
    
    # Error cases
    try:
        generate_password(length=0)
        assert False, "Should raise ValueError"
    except ValueError:
        print("  ✓ Zero length raises ValueError")
    
    try:
        generate_password(lowercase=False, uppercase=False, digits=False, symbols=False)
        assert False, "Should raise ValueError"
    except ValueError:
        print("  ✓ No character types raises ValueError")
    
    print("  ✓ generate_password tests passed\n")


def test_generate_passphrase():
    """Test passphrase generation."""
    print("Testing generate_passphrase...")
    
    # Default
    phrase = generate_passphrase()
    words = phrase.split('-')
    assert len(words) == 4
    print(f"  Default passphrase: {phrase}")
    
    # Custom word count
    six_words = generate_passphrase(word_count=6)
    assert len(six_words.split('-')) == 6
    print(f"  Six words: {six_words}")
    
    # Custom separator
    space_sep = generate_passphrase(separator=' ')
    assert len(space_sep.split(' ')) == 4
    print(f"  Space separator: {space_sep}")
    
    # Capitalized
    cap = generate_passphrase(capitalize=True)
    print(f"  Capitalized: {cap}")
    
    # With number
    with_num = generate_passphrase(include_number=True)
    print(f"  With number: {with_num}")
    
    # Custom word list
    custom_words = generate_passphrase(word_list=['alpha', 'beta', 'gamma', 'delta'])
    assert len(custom_words.split('-')) == 4
    print(f"  Custom word list: {custom_words}")
    
    # Error cases
    try:
        generate_passphrase(word_count=0)
        assert False, "Should raise ValueError"
    except ValueError:
        print("  ✓ Zero word count raises ValueError")
    
    try:
        generate_passphrase(word_list=[])
        assert False, "Should raise ValueError"
    except ValueError:
        print("  ✓ Empty word list raises ValueError")
    
    print("  ✓ generate_passphrase tests passed\n")


def test_generate_pronounceable():
    """Test pronounceable password generation."""
    print("Testing generate_pronounceable...")
    
    # Basic
    pron = generate_pronounceable()
    assert len(pron) >= 4
    print(f"  Pronounceable: {pron}")
    
    # Custom length
    pron_20 = generate_pronounceable(length=20)
    assert len(pron_20) >= 18
    print(f"  Length 20: {pron_20}")
    
    # With digits
    pron_digit = generate_pronounceable(include_digits=True)
    print(f"  With digits: {pron_digit}")
    
    # With symbols
    pron_symbol = generate_pronounceable(include_symbols=True)
    print(f"  With symbols: {pron_symbol}")
    
    print("  ✓ generate_pronounceable tests passed\n")


def test_generate_pin():
    """Test PIN generation."""
    print("Testing generate_pin...")
    
    # Default
    pin = generate_pin()
    assert len(pin) == 6
    assert pin.isdigit()
    print(f"  Default PIN: {pin}")
    
    # Custom length
    pin4 = generate_pin(length=4)
    assert len(pin4) == 4
    print(f"  4-digit PIN: {pin4}")
    
    pin8 = generate_pin(length=8)
    assert len(pin8) == 8
    print(f"  8-digit PIN: {pin8}")
    
    print("  ✓ generate_pin tests passed\n")


def test_generate_token():
    """Test token generation."""
    print("Testing generate_token...")
    
    # Default
    token = generate_token()
    assert len(token) == 32
    assert all(c.isalnum() or c in '-_' for c in token)
    print(f"  Default token: {token}")
    
    # Custom length
    token16 = generate_token(length=16)
    assert len(token16) == 16
    print(f"  16-char token: {token16}")
    
    print("  ✓ generate_token tests passed\n")


def test_generate_hex_token():
    """Test hexadecimal token generation."""
    print("Testing generate_hex_token...")
    
    # Default
    hex_token = generate_hex_token()
    assert len(hex_token) == 32
    assert all(c in '0123456789abcdef' for c in hex_token)
    print(f"  Hex token: {hex_token}")
    
    # Custom length
    hex16 = generate_hex_token(length=16)
    assert len(hex16) == 16
    print(f"  16-char hex: {hex16}")
    
    print("  ✓ generate_hex_token tests passed\n")


def test_analyze_password():
    """Test password strength analysis."""
    print("Testing analyze_password...")
    
    # Weak password
    weak = analyze_password("password")
    assert weak.rating == "weak"
    assert weak.score < 30
    assert len(weak.issues) > 0
    print(f"  Weak password: score={weak.score}, rating={weak.rating}")
    print(f"    Issues: {weak.issues[:2]}")
    
    # Strong password
    strong = analyze_password("MyVerySecureP@ssw0rd123!")
    assert strong.rating in ["strong", "excellent"]
    assert strong.score > 60
    print(f"  Strong password: score={strong.score}, rating={strong.rating}")
    print(f"    Entropy: {strong.entropy} bits")
    print(f"    Crack time: {strong.crack_time}")
    
    # Medium password
    medium = analyze_password("password123")
    assert medium.rating in ["weak", "fair"]
    print(f"  Medium password: score={medium.score}, rating={medium.rating}")
    
    # Empty password
    empty = analyze_password("")
    assert empty.score == 0
    assert empty.rating == "weak"
    print(f"  Empty password: score={empty.score}")
    
    # Check PasswordStrength dataclass
    ps = PasswordStrength(
        score=85,
        entropy=60.5,
        crack_time="centuries",
        rating="excellent",
        issues=[],
        suggestions=["Add even more characters"],
    )
    assert ps.score == 85
    print("  ✓ PasswordStrength dataclass works")
    
    print("  ✓ analyze_password tests passed\n")


def test_check_password_pwned():
    """Test breached password checking."""
    print("Testing check_password_pwned...")
    
    # Common password (should be flagged)
    assert check_password_pwned("password") == True
    assert check_password_pwned("123456") == True
    print("  ✓ Common passwords are flagged")
    
    # Uncommon password (should not be flagged)
    assert check_password_pwned("xK9#mP2$vL5") == False
    print("  ✓ Uncommon passwords are not flagged")
    
    print("  ✓ check_password_pwned tests passed\n")


def test_calculate_entropy():
    """Test entropy calculation."""
    print("Testing calculate_entropy...")
    
    # Simple password
    entropy1 = calculate_entropy("password")
    print(f"  'password' entropy: {entropy1} bits")
    assert entropy1 > 0
    
    # Complex password
    entropy2 = calculate_entropy("MyP@ssw0rd!")
    print(f"  'MyP@ssw0rd!' entropy: {entropy2} bits")
    assert entropy2 > entropy1
    
    # Empty
    entropy_empty = calculate_entropy("")
    assert entropy_empty == 0
    print("  ✓ Empty password entropy is 0")
    
    print("  ✓ calculate_entropy tests passed\n")


def test_generate_diceware():
    """Test Diceware-style passphrase generation."""
    print("Testing generate_diceware...")
    
    # Default
    dice = generate_diceware()
    words = dice.split(' ')
    assert len(words) == 5
    print(f"  Diceware: {dice}")
    
    # Custom word count
    dice7 = generate_diceware(word_count=7)
    assert len(dice7.split(' ')) == 7
    print(f"  7 words: {dice7}")
    
    # Custom separator
    dice_sep = generate_diceware(separator='-')
    assert len(dice_sep.split('-')) == 5
    print(f"  Dash separator: {dice_sep}")
    
    print("  ✓ generate_diceware tests passed\n")


def test_suggest_improvements():
    """Test password improvement suggestions."""
    print("Testing suggest_improvements...")
    
    suggestions = suggest_improvements("password")
    assert len(suggestions) > 0
    print(f"  Suggestions for 'password': {suggestions[:3]}")
    
    # Strong password should have fewer suggestions
    strong_suggestions = suggest_improvements("MyVeryLongP@ssw0rd123!")
    print(f"  Suggestions for strong password: {strong_suggestions}")
    
    print("  ✓ suggest_improvements tests passed\n")


def test_is_strong_password():
    """Test password strength checking."""
    print("Testing is_strong_password...")
    
    # Should pass
    is_strong, issues = is_strong_password("MyP@ssw0rd123", min_length=12)
    assert is_strong == True
    assert len(issues) == 0
    print(f"  Strong password: pass={is_strong}")
    
    # Should fail (too short)
    is_strong2, issues2 = is_strong_password("pass", min_length=12)
    assert is_strong2 == False
    assert len(issues2) > 0
    print(f"  Short password: pass={is_strong2}, issues={issues2}")
    
    # Should fail (missing requirements)
    is_strong3, issues3 = is_strong_password("lowercaseonly", min_length=12, require_uppercase=True)
    assert is_strong3 == False
    print(f"  Missing uppercase: pass={is_strong3}, issues={issues3}")
    
    print("  ✓ is_strong_password tests passed\n")


def test_generate_password_variants():
    """Test password variant generation."""
    print("Testing generate_password_variants...")
    
    variants = generate_password_variants("secure", count=5)
    assert len(variants) == 5
    print(f"  Variants from 'secure': {variants}")
    
    # Leet style
    leet = generate_password_variants("pass", count=3, style="leet")
    print(f"  Leet variants: {leet}")
    
    # Numbers style
    nums = generate_password_variants("test", count=3, style="numbers")
    print(f"  Number variants: {nums}")
    
    # Empty base
    empty = generate_password_variants("", count=5)
    assert empty == []
    print("  ✓ Empty base returns empty list")
    
    print("  ✓ generate_password_variants tests passed\n")


def test_estimate_crack_time():
    """Test crack time estimation."""
    print("Testing estimate_crack_time...")
    
    # Weak password
    time1 = estimate_crack_time("password")
    print(f"  'password' crack time: {time1}")
    assert "second" in time1.lower() or time1 == "instant"
    
    # Strong password
    time2 = estimate_crack_time("MyVeryLongSecureP@ssw0rd123!XYZ")
    print(f"  Strong password crack time: {time2}")
    assert "year" in time2.lower() or "centur" in time2.lower() or "millennium" in time2.lower()
    
    # Custom speed
    time3 = estimate_crack_time("password", guesses_per_second=1000)
    print(f"  Slow cracking: {time3}")
    
    print("  ✓ estimate_crack_time tests passed\n")


def test_create_memorable_password():
    """Test memorable password creation."""
    print("Testing create_memorable_password...")
    
    mem = create_memorable_password()
    assert len(mem) > 8
    print(f"  Memorable password: {mem}")
    
    # Without pattern
    mem2 = create_memorable_password(include_pattern=False)
    print(f"  Without pattern: {mem2}")
    
    # Custom separator
    mem3 = create_memorable_password(separator='_')
    print(f"  Underscore separator: {mem3}")
    
    print("  ✓ create_memorable_password tests passed\n")


def test_batch_generate():
    """Test batch password generation."""
    print("Testing batch_generate...")
    
    # Random passwords
    random_batch = batch_generate(5, PasswordStyle.RANDOM, length=12)
    assert len(random_batch) == 5
    assert all(len(p) == 12 for p in random_batch)
    print(f"  Random batch: {random_batch[:2]}...")
    
    # Passphrases
    phrase_batch = batch_generate(3, PasswordStyle.PASSPHRASE, word_count=3)
    assert len(phrase_batch) == 3
    print(f"  Passphrase batch: {phrase_batch}")
    
    # PINs
    pin_batch = batch_generate(5, PasswordStyle.PIN, length=4)
    assert len(pin_batch) == 5
    assert all(len(p) == 4 for p in pin_batch)
    print(f"  PIN batch: {pin_batch}")
    
    # Tokens
    token_batch = batch_generate(3, PasswordStyle.TOKEN, length=16)
    assert len(token_batch) == 3
    print(f"  Token batch: {token_batch}")
    
    # Empty count
    empty_batch = batch_generate(0)
    assert empty_batch == []
    print("  ✓ Zero count returns empty list")
    
    print("  ✓ batch_generate tests passed\n")


def test_get_word_list_stats():
    """Test word list statistics."""
    print("Testing get_word_list_stats...")
    
    # Default list
    stats = get_word_list_stats()
    assert stats['word_count'] > 1000
    assert stats['min_length'] >= 2
    assert stats['max_length'] >= 5
    print(f"  Default list stats: {stats}")
    
    # Custom list
    custom_stats = get_word_list_stats(['alpha', 'beta', 'gamma', 'delta'])
    assert custom_stats['word_count'] == 4
    assert custom_stats['avg_length'] > 0
    print(f"  Custom list stats: {custom_stats}")
    
    # Empty list
    empty_stats = get_word_list_stats([])
    assert empty_stats['word_count'] == 0
    print("  ✓ Empty list handled correctly")
    
    print("  ✓ get_word_list_stats tests passed\n")


def test_uniqueness():
    """Test that generated passwords are unique."""
    print("Testing password uniqueness...")
    
    # Generate multiple passwords and check uniqueness
    passwords = [generate_password() for _ in range(100)]
    unique_count = len(set(passwords))
    assert unique_count > 90  # Should have high uniqueness
    print(f"  100 passwords, {unique_count} unique")
    
    # Check passphrases
    phrases = [generate_passphrase() for _ in range(50)]
    unique_phrases = len(set(phrases))
    assert unique_phrases > 40
    print(f"  50 passphrases, {unique_phrases} unique")
    
    print("  ✓ Uniqueness tests passed\n")


def run_all_tests():
    """Run all test functions."""
    print("=" * 60)
    print("Running Passphrase Utils Tests")
    print("=" * 60 + "\n")
    
    test_generate_password()
    test_generate_passphrase()
    test_generate_pronounceable()
    test_generate_pin()
    test_generate_token()
    test_generate_hex_token()
    test_analyze_password()
    test_check_password_pwned()
    test_calculate_entropy()
    test_generate_diceware()
    test_suggest_improvements()
    test_is_strong_password()
    test_generate_password_variants()
    test_estimate_crack_time()
    test_create_memorable_password()
    test_batch_generate()
    test_get_word_list_stats()
    test_uniqueness()
    
    print("=" * 60)
    print("✓ All tests passed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    run_all_tests()
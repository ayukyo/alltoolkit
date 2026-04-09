#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AllToolkit - Random Utilities Test Suite

Comprehensive tests for random_utils module.
Run with: python random_utils_test.py
"""

import sys
import os
from datetime import datetime, timedelta

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    # Secure random
    secure_random_bytes, secure_random_int, secure_random_float,
    secure_random_choice, secure_random_sample,
    
    # Random strings
    random_string, random_password, random_token, random_uuid,
    random_slug, DEFAULT_CHARSET_ALPHANUMERIC,
    
    # Random numbers
    random_int, random_float, random_gauss, random_bool,
    
    # Selection and shuffling
    random_choice, random_sample, random_shuffle, weighted_choice,
    
    # Random datetime
    random_datetime, random_date, random_time,
    
    # Random data
    random_email, random_phone, random_ipv4, random_color,
    
    # Random IDs
    random_id, random_correlation_id, random_request_id,
    
    # Seeded random
    SeededRandom,
    
    # Math utilities
    random_point_2d, random_point_3d, random_vector, random_matrix,
    
    # Games
    roll_dice, roll_d20, coin_flip, draw_card,
)


class TestRunner:
    """Simple test runner with pass/fail tracking."""
    
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []
    
    def test(self, name: str, condition: bool, error_msg: str = ""):
        """Run a single test."""
        if condition:
            self.passed += 1
            print(f"  ✓ {name}")
        else:
            self.failed += 1
            msg = f"  ✗ {name}"
            if error_msg:
                msg += f" - {error_msg}"
            print(msg)
            self.errors.append(name)
    
    def report(self) -> bool:
        """Print test report and return True if all tests passed."""
        total = self.passed + self.failed
        print(f"\n{'='*60}")
        print(f"Tests: {total} | Passed: {self.passed} | Failed: {self.failed}")
        
        if self.failed == 0:
            print("✓ All tests passed!")
        else:
            print(f"✗ {self.failed} test(s) failed:")
            for error in self.errors:
                print(f"    - {error}")
        
        print('='*60)
        return self.failed == 0


def run_secure_random_tests(runner: TestRunner):
    """Test secure random generation."""
    print("\nSecure Random Tests")
    print("="*60)
    
    # secure_random_bytes
    data = secure_random_bytes(16)
    runner.test("secure_random_bytes: correct length", len(data) == 16)
    runner.test("secure_random_bytes: is bytes", isinstance(data, bytes))
    
    data32 = secure_random_bytes(32)
    runner.test("secure_random_bytes: 32 bytes", len(data32) == 32)
    
    # secure_random_int
    for _ in range(10):
        val = secure_random_int(1, 100)
        runner.test(f"secure_random_int: in range", 1 <= val <= 100)
    
    # Edge cases
    runner.test("secure_random_int: same bounds", secure_random_int(5, 5) == 5)
    runner.test("secure_random_int: negative range", -10 <= secure_random_int(-10, -1) <= -1)
    
    # secure_random_float
    for _ in range(10):
        val = secure_random_float()
        runner.test(f"secure_random_float: in range", 0.0 <= val < 1.0)
    
    # secure_random_choice
    items = ['a', 'b', 'c', 'd', 'e']
    for _ in range(10):
        choice = secure_random_choice(items)
        runner.test(f"secure_random_choice: valid", choice in items)
    
    # secure_random_sample
    sample = secure_random_sample(items, 3)
    runner.test("secure_random_sample: correct length", len(sample) == 3)
    runner.test("secure_random_sample: unique elements", len(set(sample)) == 3)
    runner.test("secure_random_sample: all from original", all(s in items for s in sample))


def run_random_string_tests(runner: TestRunner):
    """Test random string generation."""
    print("\nRandom String Tests")
    print("="*60)
    
    # random_string
    s = random_string(16)
    runner.test("random_string: correct length", len(s) == 16)
    runner.test("random_string: alphanumeric", all(c in DEFAULT_CHARSET_ALPHANUMERIC for c in s))
    
    s32 = random_string(32)
    runner.test("random_string: 32 chars", len(s32) == 32)
    
    # Empty string
    s0 = random_string(0)
    runner.test("random_string: zero length", s0 == "")
    
    # Custom charset
    s_custom = random_string(10, charset="abc")
    runner.test("random_string: custom charset", all(c in "abc" for c in s_custom))
    
    # random_password
    pwd = random_password(16)
    runner.test("random_password: correct length", len(pwd) == 16)
    
    pwd_no_upper = random_password(16, use_uppercase=False)
    runner.test("random_password: no uppercase", not any(c.isupper() for c in pwd_no_upper))
    
    pwd_digits_only = random_password(16, use_lowercase=False, use_uppercase=False, use_special=False)
    runner.test("random_password: digits only", all(c.isdigit() for c in pwd_digits_only))
    
    # random_token
    token = random_token()
    runner.test("random_token: non-empty", len(token) > 0)
    
    token_url = random_token(url_safe=True)
    runner.test("random_token: url safe", all(c in '-_' or c.isalnum() for c in token_url))
    
    # random_uuid
    uid = random_uuid()
    runner.test("random_uuid: correct format", len(uid) == 36)
    runner.test("random_uuid: has hyphens", uid.count('-') == 4)
    
    uid1 = random_uuid(version=1)
    runner.test("random_uuid v1: correct format", len(uid1) == 36)
    
    # random_slug
    slug = random_slug()
    runner.test("random_slug: has separator", '-' in slug)
    runner.test("random_slug: lowercase", slug == slug.lower())
    
    slug_custom = random_slug(length=4, separator='_')
    runner.test("random_slug: custom separator", slug_custom.count('_') == 3)


def run_random_number_tests(runner: TestRunner):
    """Test random number generation."""
    print("\nRandom Number Tests")
    print("="*60)
    
    # random_int
    for _ in range(10):
        val = random_int(1, 100)
        runner.test(f"random_int: in range", 1 <= val <= 100)
    
    val_secure = random_int(1, 100, secure=True)
    runner.test("random_int: secure in range", 1 <= val_secure <= 100)
    
    # random_float
    for _ in range(10):
        val = random_float()
        runner.test(f"random_float: in range", 0.0 <= val < 1.0)
    
    val_range = random_float(10.0, 20.0)
    runner.test("random_float: custom range", 10.0 <= val_range < 20.0)
    
    # random_gauss
    for _ in range(10):
        val = random_gauss()
        runner.test(f"random_gauss: is float", isinstance(val, float))
    
    # random_bool
    results = [random_bool() for _ in range(20)]
    runner.test("random_bool: returns bool", all(isinstance(r, bool) for r in results))
    
    # Probability test (should have both True and False with p=0.5)
    runner.test("random_bool: has True", True in results)
    runner.test("random_bool: has False", False in results)
    
    # Edge probability
    always_true = all(random_bool(1.0) for _ in range(10))
    runner.test("random_bool: probability 1.0", always_true)
    
    always_false = all(not random_bool(0.0) for _ in range(10))
    runner.test("random_bool: probability 0.0", always_false)


def run_selection_tests(runner: TestRunner):
    """Test random selection and shuffling."""
    print("\nSelection and Shuffling Tests")
    print("="*60)
    
    items = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    
    # random_choice
    for _ in range(10):
        choice = random_choice(items)
        runner.test(f"random_choice: valid", choice in items)
    
    # random_sample
    sample = random_sample(items, 5)
    runner.test("random_sample: correct length", len(sample) == 5)
    runner.test("random_sample: unique", len(set(sample)) == 5)
    
    # random_shuffle
    original = items.copy()
    shuffled = random_shuffle(original.copy())
    runner.test("random_shuffle: same elements", set(shuffled) == set(original))
    runner.test("random_shuffle: same length", len(shuffled) == len(original))
    
    # weighted_choice
    weighted_items = ['a', 'b']
    weights = [0.9, 0.1]
    results = [weighted_choice(weighted_items, weights) for _ in range(100)]
    runner.test("weighted_choice: valid results", all(r in weighted_items for r in results))
    # 'a' should appear more often with 0.9 weight
    a_count = results.count('a')
    runner.test("weighted_choice: weighted distribution", a_count > 50)


def run_datetime_tests(runner: TestRunner):
    """Test random datetime generation."""
    print("\nRandom Datetime Tests")
    print("="*60)
    
    # random_datetime
    start = datetime(2020, 1, 1)
    end = datetime(2025, 12, 31)
    for _ in range(10):
        dt = random_datetime(start, end)
        runner.test(f"random_datetime: in range", start <= dt <= end)
    
    # random_date
    for _ in range(10):
        dt = random_date(2000, 2020)
        runner.test(f"random_date: year in range", 2000 <= dt.year <= 2020)
    
    # random_time
    for _ in range(10):
        dt = random_time()
        runner.test(f"random_time: valid hour", 0 <= dt.hour < 24)
        runner.test(f"random_time: valid minute", 0 <= dt.minute < 60)


def run_data_generation_tests(runner: TestRunner):
    """Test random data generation."""
    print("\nRandom Data Generation Tests")
    print("="*60)
    
    # random_email
    email = random_email()
    runner.test("random_email: has @", '@' in email)
    runner.test("random_email: has domain", email.endswith('@example.com'))
    
    email_custom = random_email("test.com")
    runner.test("random_email: custom domain", email_custom.endswith('@test.com'))
    
    # random_phone
    phone = random_phone()
    runner.test("random_phone: has country code", phone.startswith('+1'))
    runner.test("random_phone: correct length", len(phone) == 12)  # +1 + 10 digits
    
    # random_ipv4
    ip = random_ipv4()
    parts = ip.split('.')
    runner.test("random_ipv4: 4 octets", len(parts) == 4)
    runner.test("random_ipv4: valid octets", all(0 <= int(p) <= 255 for p in parts))
    
    ip_private = random_ipv4(private=True)
    parts_private = ip_private.split('.')
    runner.test("random_ipv4 private: valid", len(parts_private) == 4)
    is_private = (
        parts_private[0] == '10' or 
        (parts_private[0] == '172' and 16 <= int(parts_private[1]) <= 31) or
        (parts_private[0] == '192' and parts_private[1] == '168')
    )
    runner.test("random_ipv4 private: is private range", is_private)
    
    # random_color
    color_hex = random_color('hex')
    runner.test("random_color hex: format", color_hex.startswith('#') and len(color_hex) == 7)
    
    color_rgb = random_color('rgb')
    runner.test("random_color rgb: format", color_rgb.startswith('rgb('))
    
    color_hsl = random_color('hsl')
    runner.test("random_color hsl: format", color_hsl.startswith('hsl('))


def run_id_generation_tests(runner: TestRunner):
    """Test random ID generation."""
    print("\nRandom ID Generation Tests")
    print("="*60)
    
    # random_id
    id_val = random_id("user")
    runner.test("random_id: has prefix", id_val.startswith("user_"))
    
    id_no_prefix = random_id()
    runner.test("random_id: no prefix ok", len(id_no_prefix) > 0)
    
    id_ts = random_id("test", timestamp=True)
    runner.test("random_id: with timestamp", "test_" in id_ts)
    
    # random_correlation_id
    corr_id = random_correlation_id()
    runner.test("random_correlation_id: format", corr_id.startswith('corr-'))
    
    # random_request_id
    req_id = random_request_id()
    runner.test("random_request_id: format", req_id.startswith('req-'))
    runner.test("random_request_id: length", len(req_id) > 10)


def run_seeded_random_tests(runner: TestRunner):
    """Test seeded random generator."""
    print("\nSeeded Random Tests")
    print("="*60)
    
    # Reproducibility
    rng1 = SeededRandom(42)
    rng2 = SeededRandom(42)
    
    s1 = rng1.random_string(10)
    s2 = rng2.random_string(10)
    runner.test("SeededRandom: reproducible string", s1 == s2)
    
    rng3 = SeededRandom(42)
    rng4 = SeededRandom(42)
    
    i1 = rng3.random_int(1, 100)
    i2 = rng4.random_int(1, 100)
    runner.test("SeededRandom: reproducible int", i1 == i2)
    
    # Different seeds produce different results
    rng5 = SeededRandom(42)
    rng6 = SeededRandom(43)
    
    s5 = rng5.random_string(10)
    s6 = rng6.random_string(10)
    runner.test("SeededRandom: different seeds different results", s5 != s6)
    
    # Reseeding
    rng7 = SeededRandom(42)
    s7a = rng7.random_string(10)
    rng7.seed(42)
    s7b = rng7.random_string(10)
    runner.test("SeededRandom: reseed works", s7a == s7b)


def run_math_utils_tests(runner: TestRunner):
    """Test random math utilities."""
    print("\nRandom Math Utilities Tests")
    print("="*60)
    
    # random_point_2d
    x, y = random_point_2d()
    runner.test("random_point_2d: x in range", 0 <= x <= 1)
    runner.test("random_point_2d: y in range", 0 <= y <= 1)
    
    # Custom range
    x2, y2 = random_point_2d(10, 20, 30, 40)
    runner.test("random_point_2d: custom x range", 10 <= x2 <= 20)
    runner.test("random_point_2d: custom y range", 30 <= y2 <= 40)
    
    # random_point_3d
    x3, y3, z3 = random_point_3d()
    runner.test("random_point_3d: x in range", 0 <= x3 <= 1)
    runner.test("random_point_3d: y in range", 0 <= y3 <= 1)
    runner.test("random_point_3d: z in range", 0 <= z3 <= 1)
    
    # random_vector
    v = random_vector(5)
    runner.test("random_vector: correct length", len(v) == 5)
    runner.test("random_vector: all floats", all(isinstance(x, float) for x in v))
    
    # random_matrix
    m = random_matrix(3, 4)
    runner.test("random_matrix: correct rows", len(m) == 3)
    runner.test("random_matrix: correct cols", len(m[0]) == 4)


def run_games_tests(runner: TestRunner):
    """Test dice and games utilities."""
    print("\nGames Tests")
    print("="*60)
    
    # roll_dice
    result = roll_dice(6, 2)
    runner.test("roll_dice: correct count", len(result) == 2)
    runner.test("roll_dice: valid values", all(1 <= r <= 6 for r in result))
    
    # Multiple dice
    result20 = roll_dice(20, 5)
    runner.test("roll_dice d20: valid values", all(1 <= r <= 20 for r in result20))
    
    # roll_d20
    d20 = roll_d20()
    runner.test("roll_d20: valid value", 1 <= d20 <= 20)
    
    # coin_flip
    results = [coin_flip() for _ in range(20)]
    runner.test("coin_flip: valid results", all(r in ['heads', 'tails'] for r in results))
    runner.test("coin_flip: has heads", 'heads' in results)
    runner.test("coin_flip: has tails", 'tails' in results)
    
    # draw_card
    cards = [draw_card() for _ in range(10)]
    runner.test("draw_card: valid format", all('♠' in c or '♥' in c or '♦' in c or '♣' in c for c in cards))
    
    # Different deck types
    card_standard = draw_card('standard')
    runner.test("draw_card standard: valid", len(card_standard) >= 2)
    
    card_short = draw_card('short')
    runner.test("draw_card short: valid", len(card_short) >= 2)


def run_error_handling_tests(runner: TestRunner):
    """Test error handling."""
    print("\nError Handling Tests")
    print("="*60)
    
    # secure_random_int with invalid range
    try:
        secure_random_int(10, 5)
        runner.test("secure_random_int: raises on invalid range", False)
    except ValueError:
        runner.test("secure_random_int: raises on invalid range", True)
    
    # secure_random_choice with empty sequence
    try:
        secure_random_choice([])
        runner.test("secure_random_choice: raises on empty", False)
    except ValueError:
        runner.test("secure_random_choice: raises on empty", True)
    
    # secure_random_sample with k > len
    try:
        secure_random_sample([1, 2, 3], 5)
        runner.test("secure_random_sample: raises on k > len", False)
    except ValueError:
        runner.test("secure_random_sample: raises on k > len", True)
    
    # random_password with no character types
    try:
        random_password(16, use_lowercase=False, use_uppercase=False, 
                       use_digits=False, use_special=False)
        runner.test("random_password: raises on no charset", False)
    except ValueError:
        runner.test("random_password: raises on no charset", True)
    
    # random_bool with invalid probability
    try:
        random_bool(1.5)
        runner.test("random_bool: raises on invalid prob", False)
    except ValueError:
        runner.test("random_bool: raises on invalid prob", True)
    
    # weighted_choice with mismatched lengths
    try:
        weighted_choice(['a', 'b'], [0.5])
        runner.test("weighted_choice: raises on length mismatch", False)
    except ValueError:
        runner.test("weighted_choice: raises on length mismatch", True)
    
    # random_color with invalid format
    try:
        random_color('invalid')
        runner.test("random_color: raises on invalid format", False)
    except ValueError:
        runner.test("random_color: raises on invalid format", True)
    
    # roll_dice with invalid sides
    try:
        roll_dice(1)
        runner.test("roll_dice: raises on invalid sides", False)
    except ValueError:
        runner.test("roll_dice: raises on invalid sides", True)
    
    # draw_card with invalid deck type
    try:
        draw_card('invalid')
        runner.test("draw_card: raises on invalid deck", False)
    except ValueError:
        runner.test("draw_card: raises on invalid deck", True)


def run_uniqueness_tests(runner: TestRunner):
    """Test uniqueness of generated values."""
    print("\nUniqueness Tests")
    print("="*60)
    
    # Generate multiple values and check for uniqueness
    uuids = [random_uuid() for _ in range(100)]
    runner.test("UUID uniqueness", len(set(uuids)) == 100)
    
    tokens = [random_token() for _ in range(100)]
    runner.test("Token uniqueness", len(set(tokens)) == 100)
    
    ids = [random_id() for _ in range(100)]
    runner.test("ID uniqueness", len(set(ids)) == 100)
    
    passwords = [random_password(16) for _ in range(100)]
    runner.test("Password uniqueness", len(set(passwords)) == 100)


def main():
    """Run all tests."""
    print("="*60)
    print("AllToolkit - Random Utilities Test Suite")
    print("="*60)
    
    runner = TestRunner()
    
    run_secure_random_tests(runner)
    run_random_string_tests(runner)
    run_random_number_tests(runner)
    run_selection_tests(runner)
    run_datetime_tests(runner)
    run_data_generation_tests(runner)
    run_id_generation_tests(runner)
    run_seeded_random_tests(runner)
    run_math_utils_tests(runner)
    run_games_tests(runner)
    run_error_handling_tests(runner)
    run_uniqueness_tests(runner)
    
    success = runner.report()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

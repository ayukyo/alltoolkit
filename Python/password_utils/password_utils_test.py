"""
AllToolkit - Python Password Utilities Test Suite

Comprehensive test suite for password_utils module.
Covers normal scenarios, edge cases, and error conditions.

Run: python password_utils_test.py
"""

import sys
import os
from typing import Any

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    PasswordUtils,
    StrengthLevel,
    ValidationError,
    PasswordStrength,
    ValidationResult,
    generate_password,
    generate_passphrase,
    analyze,
    validate,
    hash_password,
    verify_password,
    is_weak,
    is_strong,
)


class TestResult:
    """Simple test result tracker."""
    
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []
    
    def add_pass(self, name: str):
        self.passed += 1
        print(f"  ✓ {name}")
    
    def add_fail(self, name: str, expected: Any, actual: Any):
        self.failed += 1
        self.errors.append((name, expected, actual))
        print(f"  ✗ {name}")
        print(f"    Expected: {expected}")
        print(f"    Actual: {actual}")
    
    def summary(self):
        total = self.passed + self.failed
        print(f"\n{'='*60}")
        print(f"Test Results: {self.passed}/{total} passed")
        if self.failed > 0:
            print(f"Failed: {self.failed}")
            print(f"\nFailures:")
            for name, expected, actual in self.errors:
                print(f"  - {name}: expected {expected}, got {actual}")
        else:
            print("All tests passed! ✓")
        print(f"{'='*60}")
        return self.failed == 0


def run_tests():
    """Run all tests."""
    result = TestResult()
    utils = PasswordUtils()
    
    print("\n" + "="*60)
    print("Password Utils Test Suite")
    print("="*60)
    
    # ============== Password Generation Tests ==============
    print("\n[1] Password Generation Tests")
    
    # Test basic generation
    pwd = utils.generate(length=16)
    if len(pwd) == 16:
        result.add_pass("generate length 16")
    else:
        result.add_fail("generate length 16", 16, len(pwd))
    
    # Test different lengths
    for length in [8, 12, 20, 32]:
        pwd = utils.generate(length=length)
        if len(pwd) == length:
            result.add_pass(f"generate length {length}")
        else:
            result.add_fail(f"generate length {length}", length, len(pwd))
    
    # Test character types included
    pwd = utils.generate(length=32, use_lowercase=True, use_uppercase=True, 
                         use_digits=True, use_special=True)
    has_lower = any(c.islower() for c in pwd)
    has_upper = any(c.isupper() for c in pwd)
    has_digit = any(c.isdigit() for c in pwd)
    has_special = any(not c.isalnum() for c in pwd)
    
    if has_lower and has_upper and has_digit and has_special:
        result.add_pass("generate all character types")
    else:
        result.add_fail("generate all character types", "all types", 
                       f"lower={has_lower}, upper={has_upper}, digit={has_digit}, special={has_special}")
    
    # Test exclude ambiguous
    pwd = utils.generate(length=20, exclude_ambiguous=True)
    ambiguous_chars = set("0O1lI|;")
    has_ambiguous = any(c in ambiguous_chars for c in pwd)
    
    if not has_ambiguous:
        result.add_pass("exclude ambiguous characters")
    else:
        result.add_fail("exclude ambiguous characters", "no ambiguous", "found ambiguous")
    
    # Test no special characters
    pwd = utils.generate(length=16, use_special=False)
    has_special = any(not c.isalnum() for c in pwd)
    
    if not has_special:
        result.add_pass("generate without special chars")
    else:
        result.add_fail("generate without special chars", "no special", "has special")
    
    # Test error on invalid length
    try:
        utils.generate(length=0)
        result.add_fail("generate length 0 error", "ValueError", "no error")
    except ValueError:
        result.add_pass("generate length 0 error")
    
    # Test error on no character types
    try:
        utils.generate(length=16, use_lowercase=False, use_uppercase=False,
                      use_digits=False, use_special=False)
        result.add_fail("generate no types error", "ValueError", "no error")
    except ValueError:
        result.add_pass("generate no types error")
    
    # ============== Passphrase Generation Tests ==============
    print("\n[2] Passphrase Generation Tests")
    
    # Test basic passphrase
    phrase = utils.generate_passphrase(word_count=4)
    words = phrase.split("-")
    
    if len(words) == 4:
        result.add_pass("passphrase word count")
    else:
        result.add_fail("passphrase word count", 4, len(words))
    
    # Test custom separator
    phrase = utils.generate_passphrase(word_count=3, separator="_")
    if "_" in phrase and "-" not in phrase:
        result.add_pass("passphrase custom separator")
    else:
        result.add_fail("passphrase custom separator", "underscore", "wrong separator")
    
    # Test with number
    phrase = utils.generate_passphrase(word_count=3, add_number=True)
    has_digit = any(c.isdigit() for c in phrase)
    
    if has_digit:
        result.add_pass("passphrase with number")
    else:
        result.add_fail("passphrase with number", "has digit", "no digit")
    
    # Test capitalization
    phrase = utils.generate_passphrase(word_count=4, use_capitalization=True)
    words = phrase.split("-")
    all_capitalized = all(w[0].isupper() for w in words if w)
    
    if all_capitalized:
        result.add_pass("passphrase capitalization")
    else:
        result.add_fail("passphrase capitalization", "all capitalized", "not all capitalized")
    
    # ============== Strength Analysis Tests ==============
    print("\n[3] Strength Analysis Tests")
    
    # Test very weak password
    strength = utils.analyze_strength("123456")
    if strength.level == StrengthLevel.VERY_WEAK:
        result.add_pass("strength very weak")
    else:
        result.add_fail("strength very weak", StrengthLevel.VERY_WEAK, strength.level)
    
    # Test strong password
    strength = utils.analyze_strength("K9#mP2$xL7@nQ5!w")
    if strength.level in [StrengthLevel.STRONG, StrengthLevel.VERY_STRONG]:
        result.add_pass("strength strong password")
    else:
        result.add_fail("strength strong password", "STRONG+", strength.level)
    
    # Test length affects strength
    strength_short = utils.analyze_strength("Aa1!")
    strength_long = utils.analyze_strength("Aa1!Bb2@Cc3#Dd4$")
    
    if strength_long.score > strength_short.score:
        result.add_pass("length affects strength")
    else:
        result.add_fail("length affects strength", "long > short", 
                       f"{strength_long.score} vs {strength_short.score}")
    
    # Test character diversity
    strength = utils.analyze_strength("aaaaaaaaaaaaaaaa")
    if strength.character_diversity < 0.2:
        result.add_pass("low diversity detected")
    else:
        result.add_fail("low diversity detected", "< 0.2", strength.character_diversity)
    
    # Test entropy calculation
    strength = utils.analyze_strength("K9#mP2$xL7@nQ5!w")
    if strength.entropy_bits > 50:
        result.add_pass("entropy calculation")
    else:
        result.add_fail("entropy calculation", "> 50 bits", strength.entropy_bits)
    
    # Test issues detection
    strength = utils.analyze_strength("password123")
    has_issues = len(strength.issues) > 0
    
    if has_issues:
        result.add_pass("issues detected for weak password")
    else:
        result.add_fail("issues detected for weak password", "has issues", "no issues")
    
    # Test suggestions provided
    strength = utils.analyze_strength("abc")
    has_suggestions = len(strength.suggestions) > 0
    
    if has_suggestions:
        result.add_pass("suggestions provided")
    else:
        result.add_fail("suggestions provided", "has suggestions", "no suggestions")
    
    # Test to_dict method
    strength = utils.analyze_strength("Test123!")
    d = strength.to_dict()
    
    if "level" in d and "score" in d and "entropy_bits" in d:
        result.add_pass("strength to_dict")
    else:
        result.add_fail("strength to_dict", "has keys", d.keys())
    
    # ============== Validation Tests ==============
    print("\n[4] Validation Tests")
    
    # Test valid password
    result_valid = utils.validate("K9#mP2$xL7@nQ5!")
    if result_valid.is_valid:
        result.add_pass("validate strong password")
    else:
        result.add_fail("validate strong password", True, result_valid.is_valid)
    
    # Test too short
    result_short = utils.validate("Aa1!")
    if not result_short.is_valid and ValidationError.TOO_SHORT in result_short.errors:
        result.add_pass("validate too short")
    else:
        result.add_fail("validate too short", "TOO_SHORT", result_short.errors)
    
    # Test no uppercase
    result_no_upper = utils.validate("abcdefgh1!")
    if ValidationError.NO_UPPERCASE in result_no_upper.errors:
        result.add_pass("validate no uppercase")
    else:
        result.add_fail("validate no uppercase", "NO_UPPERCASE", result_no_upper.errors)
    
    # Test no lowercase
    result_no_lower = utils.validate("ABCDEFGH1!")
    if ValidationError.NO_LOWERCASE in result_no_lower.errors:
        result.add_pass("validate no lowercase")
    else:
        result.add_fail("validate no lowercase", "NO_LOWERCASE", result_no_lower.errors)
    
    # Test no digit
    result_no_digit = utils.validate("Abcdefgh!")
    if ValidationError.NO_DIGIT in result_no_digit.errors:
        result.add_pass("validate no digit")
    else:
        result.add_fail("validate no digit", "NO_DIGIT", result_no_digit.errors)
    
    # Test common password
    result_common = utils.validate("password")
    if ValidationError.COMMON_PASSWORD in result_common.errors:
        result.add_pass("validate common password")
    else:
        result.add_fail("validate common password", "COMMON_PASSWORD", result_common.errors)
    
    # Test sequential pattern
    result_seq = utils.validate("Abcdefgh123!")
    if ValidationError.SEQUENTIAL_CHARS in result_seq.errors:
        result.add_pass("validate sequential pattern")
    else:
        result.add_fail("validate sequential pattern", "SEQUENTIAL_CHARS", result_seq.errors)
    
    # Test contains username
    result_user = utils.validate("JohnDoe123!", username="johndoe")
    if ValidationError.CONTAINS_USERNAME in result_user.errors:
        result.add_pass("validate contains username")
    else:
        result.add_fail("validate contains username", "CONTAINS_USERNAME", result_user.errors)
    
    # Test to_dict method
    result_val = utils.validate("short")
    d = result_val.to_dict()
    
    if "is_valid" in d and "errors" in d:
        result.add_pass("validation to_dict")
    else:
        result.add_fail("validation to_dict", "has keys", d.keys())
    
    # ============== Hashing Tests ==============
    print("\n[5] Hashing Tests")
    
    # Test hash generation
    pwd_hash, salt = utils.hash_password("TestPassword123!")
    
    if len(pwd_hash) == 64 and len(salt) == 64:  # SHA256 hex = 64 chars
        result.add_pass("hash password format")
    else:
        result.add_fail("hash password format", "64 chars each", 
                       f"hash={len(pwd_hash)}, salt={len(salt)}")
    
    # Test hash consistency
    pwd_hash1, salt1 = utils.hash_password("SamePassword", salt=bytes.fromhex(salt))
    pwd_hash2, salt2 = utils.hash_password("SamePassword", salt=bytes.fromhex(salt))
    
    if pwd_hash1 == pwd_hash2:
        result.add_pass("hash consistency")
    else:
        result.add_fail("hash consistency", "same hash", f"{pwd_hash1} vs {pwd_hash2}")
    
    # Test different salts produce different hashes
    pwd_hash1, salt1 = utils.hash_password("SamePassword")
    pwd_hash2, salt2 = utils.hash_password("SamePassword")
    
    if pwd_hash1 != pwd_hash2:
        result.add_pass("different salts different hashes")
    else:
        result.add_fail("different salts different hashes", "different", "same")
    
    # Test verification
    pwd = "VerifyThis123!"
    pwd_hash, salt = utils.hash_password(pwd)
    is_correct = utils.verify_password(pwd, pwd_hash, salt)
    
    if is_correct:
        result.add_pass("verify correct password")
    else:
        result.add_fail("verify correct password", True, is_correct)
    
    # Test verification with wrong password
    is_wrong = utils.verify_password("WrongPassword", pwd_hash, salt)
    
    if not is_wrong:
        result.add_pass("verify wrong password")
    else:
        result.add_fail("verify wrong password", False, is_wrong)
    
    # ============== Breach Check Tests ==============
    print("\n[6] Breach Check Tests")
    
    # Test common password detected
    is_breached = utils.is_breached("password")
    if is_breached:
        result.add_pass("breach check common password")
    else:
        result.add_fail("breach check common password", True, is_breached)
    
    # Test unique password not breached
    is_breached = utils.is_breached("X9#kL2$mN7@pQ4!vZ8&wR5^tY1*uI6")
    if not is_breached:
        result.add_pass("breach check unique password")
    else:
        result.add_fail("breach check unique password", False, is_breached)
    
    # ============== Crack Time Estimation Tests ==============
    print("\n[7] Crack Time Estimation Tests")
    
    # Test weak password crack time
    crack_info = utils.estimate_crack_time("123456")
    
    if "time_to_crack" in crack_info and "entropy_bits" in crack_info:
        result.add_pass("crack time has required fields")
    else:
        result.add_fail("crack time has required fields", "fields present", crack_info.keys())
    
    # Test strong password takes longer
    crack_weak = utils.estimate_crack_time("123456")
    crack_strong = utils.estimate_crack_time("K9#mP2$xL7@nQ5!wR8&vN3^tY6*uI1")
    
    if crack_strong["seconds"] > crack_weak["seconds"]:
        result.add_pass("strong password takes longer to crack")
    else:
        result.add_fail("strong password takes longer", "strong > weak", 
                       f"{crack_strong['seconds']} vs {crack_weak['seconds']}")
    
    # ============== Convenience Functions Tests ==============
    print("\n[8] Convenience Functions Tests")
    
    # Test generate_password
    pwd = generate_password(length=16)
    if len(pwd) == 16:
        result.add_pass("generate_password function")
    else:
        result.add_fail("generate_password function", 16, len(pwd))
    
    # Test generate_passphrase
    phrase = generate_passphrase(word_count=3)
    words = phrase.split("-")
    if len(words) == 3:
        result.add_pass("generate_passphrase function")
    else:
        result.add_fail("generate_passphrase function", 3, len(words))
    
    # Test analyze function
    strength = analyze("Test123!")
    if isinstance(strength, PasswordStrength):
        result.add_pass("analyze function")
    else:
        result.add_fail("analyze function", "PasswordStrength", type(strength))
    
    # Test validate function
    result_val = validate("Test123!")
    if isinstance(result_val, ValidationResult):
        result.add_pass("validate function")
    else:
        result.add_fail("validate function", "ValidationResult", type(result_val))
    
    # Test is_weak function
    if is_weak("123456"):
        result.add_pass("is_weak detects weak")
    else:
        result.add_fail("is_weak detects weak", True, False)
    
    if not is_weak("K9#mP2$xL7@nQ5!wR8&vN3^tY6*uI1"):
        result.add_pass("is_weak rejects strong")
    else:
        result.add_fail("is_weak rejects strong", False, True)
    
    # Test is_strong function
    if is_strong("K9#mP2$xL7@nQ5!wR8&vN3^tY6*uI1"):
        result.add_pass("is_strong detects strong")
    else:
        result.add_fail("is_strong detects strong", True, False)
    
    if not is_strong("123456"):
        result.add_pass("is_strong rejects weak")
    else:
        result.add_fail("is_strong rejects weak", False, True)
    
    # ============== Edge Cases Tests ==============
    print("\n[9] Edge Cases Tests")
    
    # Test empty password
    strength = utils.analyze_strength("")
    if strength.length == 0:
        result.add_pass("empty password analysis")
    else:
        result.add_fail("empty password analysis", 0, strength.length)
    
    # Test very long password
    long_pwd = "Aa1!" * 100
    result_long = utils.validate(long_pwd)
    if ValidationError.TOO_LONG in result_long.errors:
        result.add_pass("too long password validation")
    else:
        result.add_fail("too long password validation", "TOO_LONG", result_long.errors)
    
    # Test Unicode password
    unicode_pwd = "密码 Test123!"
    strength = utils.analyze_strength(unicode_pwd)
    if strength.length > 0:
        result.add_pass("unicode password analysis")
    else:
        result.add_fail("unicode password analysis", "> 0", strength.length)
    
    # Test special characters only
    special_pwd = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    strength = utils.analyze_strength(special_pwd)
    if strength.has_special and not strength.has_lowercase:
        result.add_pass("special chars only analysis")
    else:
        result.add_fail("special chars only analysis", "special only", 
                       f"special={strength.has_special}, lower={strength.has_lowercase}")
    
    # Print summary
    result.summary()
    
    return result.failed == 0


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)

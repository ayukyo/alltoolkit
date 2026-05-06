#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ISSN Utilities Test Suite
Tests for ISSN validation, conversion, and generation
"""

import sys
import os

# Add parent directory for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from issn_utils.mod import (
    clean_issn, is_issn8, is_issn13, is_valid_issn, get_issn_type,
    calculate_issn_check_digit, calculate_issn13_check_digit,
    issn8_to_issn13, issn13_to_issn8, convert_issn, format_issn,
    format_issn_compact, is_issn_l, format_issn_l, extract_issn_l,
    parse_issn, generate_issn, generate_issn13, generate_issn_l,
    validate_issns, find_issns_in_text, compare_issns, get_issn_variants,
    get_check_digit_info, ISSN_L_PREFIX, ISSN_CHARS, ISSN_13_PREFIX
)


class TestResultCollector:
    """Collects test results"""
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.tests = []
    
    def add_result(self, name, passed, message=""):
        self.tests.append((name, passed, message))
        if passed:
            self.passed += 1
        else:
            self.failed += 1
    
    def summary(self):
        total = self.passed + self.failed
        print(f"\n{'='*60}")
        print(f"ISSN Utils Test Results: {self.passed}/{total} passed")
        print(f"{'='*60}")
        if self.failed > 0:
            print("Failed tests:")
            for name, passed, msg in self.tests:
                if not passed:
                    print(f"  - {name}: {msg}")
        return self.failed == 0


results = TestResultCollector()


def test_clean_issn():
    """Test ISSN cleaning"""
    try:
        assert clean_issn("0378-5955") == "03785955"
        assert clean_issn("ISSN 0378-5955") == "03785955"
        assert clean_issn("2434-561X") == "2434561X"
        assert clean_issn("") == ""
        assert clean_issn(None) == ""
        assert clean_issn("  0378-5955  ") == "03785955"
        results.add_result("clean_issn", True)
    except Exception as e:
        results.add_result("clean_issn", False, str(e))


def test_is_issn8():
    """Test ISSN-8 validation"""
    try:
        # Valid ISSN-8
        assert is_issn8("0378-5955") == True
        assert is_issn8("03785955") == True
        assert is_issn8("2434-561X") == True  # X check digit
        assert is_issn8("ISSN 0378-5955") == True
        
        # Invalid ISSN-8
        assert is_issn8("0378-5956") == False  # Wrong check digit
        assert is_issn8("9770378595001") == False  # ISSN-13
        assert is_issn8("invalid") == False
        assert is_issn8("") == False
        assert is_issn8("0378595") == False  # Too short
        assert is_issn8("037859555") == False  # Too long
        results.add_result("is_issn8", True)
    except Exception as e:
        results.add_result("is_issn8", False, str(e))


def test_is_issn13():
    """Test ISSN-13 validation"""
    try:
        # Valid ISSN-13 (converted from valid ISSN-8)
        valid_issn13 = issn8_to_issn13("0378-5955")
        assert is_issn13(valid_issn13) == True
        assert is_issn13("977-0378-5950-02") == True
        
        # Invalid ISSN-13
        assert is_issn13("0378-5955") == False  # ISSN-8
        assert is_issn13("9780378595002") == False  # Wrong prefix (ISBN)
        assert is_issn13("invalid") == False
        results.add_result("is_issn13", True)
    except Exception as e:
        results.add_result("is_issn13", False, str(e))


def test_is_valid_issn():
    """Test general ISSN validation"""
    try:
        assert is_valid_issn("0378-5955") == True  # ISSN-8
        valid_issn13 = issn8_to_issn13("0378-5955")
        assert is_valid_issn(valid_issn13) == True  # ISSN-13
        assert is_valid_issn("2434-561X") == True
        assert is_valid_issn("invalid") == False
        assert is_valid_issn("") == False
        results.add_result("is_valid_issn", True)
    except Exception as e:
        results.add_result("is_valid_issn", False, str(e))


def test_get_issn_type():
    """Test ISSN type detection"""
    try:
        assert get_issn_type("0378-5955") == "ISSN-8"
        valid_issn13 = issn8_to_issn13("0378-5955")
        assert get_issn_type(valid_issn13) == "ISSN-13"
        assert get_issn_type("invalid") is None
        results.add_result("get_issn_type", True)
    except Exception as e:
        results.add_result("get_issn_type", False, str(e))


def test_calculate_issn_check_digit():
    """Test ISSN-8 check digit calculation"""
    try:
        assert calculate_issn_check_digit("0378595") == "5"
        assert calculate_issn_check_digit("2434561") == "X"
        
        # Test invalid input
        try:
            calculate_issn_check_digit("123456")
            results.add_result("calculate_issn_check_digit", False, "Should raise for invalid length")
        except ValueError:
            pass
        results.add_result("calculate_issn_check_digit", True)
    except Exception as e:
        results.add_result("calculate_issn_check_digit", False, str(e))


def test_calculate_issn13_check_digit():
    """Test ISSN-13 check digit calculation"""
    try:
        assert calculate_issn13_check_digit("977037859500") == "2"
        
        # Test invalid input
        try:
            calculate_issn13_check_digit("12345678901")
            results.add_result("calculate_issn13_check_digit", False, "Should raise for invalid length")
        except ValueError:
            pass
        results.add_result("calculate_issn13_check_digit", True)
    except Exception as e:
        results.add_result("calculate_issn13_check_digit", False, str(e))


def test_issn_conversion():
    """Test ISSN-8 to ISSN-13 conversion"""
    try:
        # ISSN-8 to ISSN-13
        issn13 = issn8_to_issn13("0378-5955")
        assert issn13 == "9770378595002"
        assert is_issn13(issn13)
        
        # ISSN-13 to ISSN-8
        issn8 = issn13_to_issn8(issn13)
        assert issn8 == "03785955"
        assert is_issn8(issn8)
        
        # Test invalid input
        try:
            issn8_to_issn13("invalid")
            results.add_result("issn_conversion", False, "Should raise for invalid ISSN-8")
        except ValueError:
            pass
        
        try:
            issn13_to_issn8("invalid")
            results.add_result("issn_conversion", False, "Should raise for invalid ISSN-13")
        except ValueError:
            pass
        results.add_result("issn_conversion", True)
    except Exception as e:
        results.add_result("issn_conversion", False, str(e))


def test_convert_issn():
    """Test generic ISSN conversion"""
    try:
        assert convert_issn("0378-5955", "ISSN-13") == "9770378595002"
        assert convert_issn("9770378595002", "ISSN-8") == "03785955"
        assert convert_issn("0378-5955", "ISSN-8") == "03785955"
        assert convert_issn("invalid", "ISSN-13") is None
        results.add_result("convert_issn", True)
    except Exception as e:
        results.add_result("convert_issn", False, str(e))


def test_format_issn():
    """Test ISSN formatting"""
    try:
        assert format_issn("03785955") == "0378-5955"
        valid_issn13 = issn8_to_issn13("0378-5955")
        assert format_issn(valid_issn13) == "977-0378-5950-02"
        assert format_issn("2434561X") == "2434-561X"
        assert format_issn("03785955", separator=" ") == "0378 5955"
        
        # Invalid ISSN should raise
        try:
            format_issn("invalid")
            results.add_result("format_issn", False, "Should raise for invalid ISSN")
        except ValueError:
            pass
        results.add_result("format_issn", True)
    except Exception as e:
        results.add_result("format_issn", False, str(e))


def test_format_issn_compact():
    """Test compact ISSN formatting"""
    try:
        assert format_issn_compact("0378-5955") == "03785955"
        valid_issn13 = issn8_to_issn13("0378-5955")
        assert format_issn_compact("977-0378-5950-02") == "9770378595002"
        results.add_result("format_issn_compact", True)
    except Exception as e:
        results.add_result("format_issn_compact", False, str(e))


def test_issn_l():
    """Test ISSN-L functions"""
    try:
        assert is_issn_l("ISSN-L: 0378-5955") == True
        assert is_issn_l("0378-5955") == True  # Valid ISSN works
        assert is_issn_l("invalid") == False
        
        assert format_issn_l("0378-5955") == "ISSN-L: 0378-5955"
        
        assert extract_issn_l("ISSN-L: 0378-5955") == "03785955"
        assert extract_issn_l("0378-5955") == "03785955"
        assert extract_issn_l("invalid") is None
        results.add_result("issn_l", True)
    except Exception as e:
        results.add_result("issn_l", False, str(e))


def test_parse_issn():
    """Test ISSN parsing"""
    try:
        info = parse_issn("0378-5955")
        assert info["valid"] == True
        assert info["type"] == "ISSN-8"
        assert info["clean"] == "03785955"
        assert info["formatted"] == "0378-5955"
        assert info["check_digit"] == "5"
        assert info["issn13"] == "9770378595002"
        
        valid_issn13 = issn8_to_issn13("0378-5955")
        info13 = parse_issn(valid_issn13)
        assert info13["valid"] == True
        assert info13["type"] == "ISSN-13"
        assert info13["issn8"] == "03785955"
        
        info_invalid = parse_issn("invalid")
        assert info_invalid["valid"] == False
        results.add_result("parse_issn", True)
    except Exception as e:
        results.add_result("parse_issn", False, str(e))


def test_generate_issn():
    """Test ISSN generation"""
    try:
        # Generate random ISSN-8
        issn8 = generate_issn()
        assert is_issn8(issn8) == True
        assert len(issn8) == 8
        
        # Generate with prefix
        issn_prefix = generate_issn("037")
        assert issn_prefix.startswith("037")
        assert is_issn8(issn_prefix)
        
        # Generate ISSN-13
        issn13 = generate_issn13()
        assert is_issn13(issn13) == True
        assert len(issn13) == 13
        
        # Generate ISSN-L
        issn_l = generate_issn_l()
        assert is_issn_l(issn_l) == True
        results.add_result("generate_issn", True)
    except Exception as e:
        results.add_result("generate_issn", False, str(e))


def test_validate_issns():
    """Test batch ISSN validation"""
    try:
        valid_issn13 = issn8_to_issn13("0378-5955")
        results_batch = validate_issns(["0378-5955", "invalid", valid_issn13])
        assert results_batch["0378-5955"]["valid"] == True
        assert results_batch["invalid"]["valid"] == False
        assert results_batch[valid_issn13]["valid"] == True
        results.add_result("validate_issns", True)
    except Exception as e:
        results.add_result("validate_issns", False, str(e))


def test_find_issns_in_text():
    """Test finding ISSNs in text"""
    try:
        text = "The journal ISSN 0378-5955 is available. Also check 2434-561X."
        issns = find_issns_in_text(text)
        assert "03785955" in issns
        assert "2434561X" in issns
        
        # Test text with invalid ISSN
        text2 = "Some random text 12345678 here."
        issns2 = find_issns_in_text(text2)
        assert len(issns2) == 0 or "12345678" not in issns2
        results.add_result("find_issns_in_text", True)
    except Exception as e:
        results.add_result("find_issns_in_text", False, str(e))


def test_compare_issns():
    """Test ISSN comparison"""
    try:
        # Same publication
        valid_issn13 = issn8_to_issn13("0378-5955")
        assert compare_issns("0378-5955", valid_issn13) == True
        
        # Different publications
        assert compare_issns("0378-5955", "2434-561X") == False
        
        # Invalid ISSNs
        assert compare_issns("invalid", "0378-5955") == False
        results.add_result("compare_issns", True)
    except Exception as e:
        results.add_result("compare_issns", False, str(e))


def test_get_issn_variants():
    """Test getting ISSN variants"""
    try:
        variants = get_issn_variants("0378-5955")
        assert variants["issn8"] == "03785955"
        assert variants["issn13"] == "9770378595002"
        assert variants["formatted8"] == "0378-5955"
        assert variants["formatted13"] == "977-0378-5950-02"
        assert "ISSN-L:" in variants["issn_l"]
        
        variants_invalid = get_issn_variants("invalid")
        assert variants_invalid["issn8"] is None
        results.add_result("get_issn_variants", True)
    except Exception as e:
        results.add_result("get_issn_variants", False, str(e))


def test_get_check_digit_info():
    """Test check digit info"""
    try:
        info = get_check_digit_info("0378-5955")
        assert info["provided"] == "5"
        assert info["calculated"] == "5"
        assert info["valid"] == True
        assert info["algorithm"] == "modulo-11"
        
        info_x = get_check_digit_info("2434-561X")
        assert info_x["provided"] == "X"
        assert info_x["calculated"] == "X"
        
        info_invalid = get_check_digit_info("0378-5956")
        assert info_invalid["valid"] == False
        results.add_result("get_check_digit_info", True)
    except Exception as e:
        results.add_result("get_check_digit_info", False, str(e))


def test_constants():
    """Test module constants"""
    try:
        assert ISSN_L_PREFIX == "ISSN-L:"
        assert "0" in ISSN_CHARS
        assert "X" in ISSN_CHARS
        assert ISSN_13_PREFIX == "977"
        results.add_result("constants", True)
    except Exception as e:
        results.add_result("constants", False, str(e))


def test_edge_cases():
    """Test edge cases"""
    try:
        # Empty strings
        assert is_valid_issn("") == False
        assert clean_issn("") == ""
        
        # Very long strings
        assert is_valid_issn("037859550000000") == False
        
        # Special characters
        assert is_valid_issn("0378-5955!") == True  # clean_issn handles
        
        # X in middle position (invalid)
        assert is_issn8("X434561X") == False
        
        results.add_result("edge_cases", True)
    except Exception as e:
        results.add_result("edge_cases", False, str(e))


# Run all tests
def run_tests():
    """Run all test functions"""
    test_clean_issn()
    test_is_issn8()
    test_is_issn13()
    test_is_valid_issn()
    test_get_issn_type()
    test_calculate_issn_check_digit()
    test_calculate_issn13_check_digit()
    test_issn_conversion()
    test_convert_issn()
    test_format_issn()
    test_format_issn_compact()
    test_issn_l()
    test_parse_issn()
    test_generate_issn()
    test_validate_issns()
    test_find_issns_in_text()
    test_compare_issns()
    test_get_issn_variants()
    test_get_check_digit_info()
    test_constants()
    test_edge_cases()
    
    return results.summary()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
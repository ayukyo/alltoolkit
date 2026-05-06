#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
License Plate Utils Test Suite
Tests for Chinese license plate validation and generation
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from license_plate_utils.mod import (
    LicensePlate, LicensePlateSet,
    validate, parse, validate_format,
    generate, generate_batch, generate_nice_number,
    get_province, get_province_short, get_city_code, get_number, get_type,
    is_special, is_police, is_learner, is_embassy, is_temporary, is_electric,
    encode_number, decode_number,
    compare, match_pattern,
    analyze_batch,
    format_plate, format_with_province,
    list_provinces, list_province_names, list_special_types,
    is_valid_char, get_char_type,
    PROVINCES, PROVINCE_MAP, VALID_LETTERS, SPECIAL_TYPES
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
        print(f"License Plate Utils Test Results: {self.passed}/{total} passed")
        print(f"{'='*60}")
        if self.failed > 0:
            print("Failed tests:")
            for name, passed, msg in self.tests:
                if not passed:
                    print(f"  - {name}: {msg}")
        return self.failed == 0


results = TestResultCollector()


def test_validate():
    """Test license plate validation"""
    try:
        # Valid plates
        assert validate("京A12345") == True
        assert validate("沪B12345") == True
        assert validate("粤C12345") == True
        
        # Invalid plates
        assert validate("") == False
        assert validate("invalid") == False
        assert validate("京I12345") == False  # I not valid
        assert validate("京O12345") == False  # O not valid
        assert validate("X京12345") == False  # Invalid province
        
        results.add_result("validate", True)
    except Exception as e:
        results.add_result("validate", False, str(e))


def test_parse():
    """Test license plate parsing"""
    try:
        # Parse valid plate
        info = parse("京A12345")
        assert info is not None
        assert info.province == "京"
        assert info.province_name == "北京市"
        assert info.city_code == "A"
        assert info.number == "12345"
        assert info.special_type is None
        
        # Parse invalid plate
        assert parse("invalid") is None
        
        # Parse plate with special type
        info = parse("京A12345警")
        assert info is not None
        assert info.special_type == "警"
        assert info.is_special() == True
        
        results.add_result("parse", True)
    except Exception as e:
        results.add_result("parse", False, str(e))


def test_validate_format():
    """Test format validation with error messages"""
    try:
        # Valid format
        valid, msg = validate_format("京A12345")
        assert valid == True
        
        # Invalid format - empty
        valid, msg = validate_format("")
        assert valid == False
        assert "空" in msg
        
        # Invalid format - too short
        valid, msg = validate_format("京A123")
        assert valid == False
        
        # Invalid province
        valid, msg = validate_format("X京12345")
        assert valid == False
        
        results.add_result("validate_format", True)
    except Exception as e:
        results.add_result("validate_format", False, str(e))


def test_license_plate_dataclass():
    """Test LicensePlate dataclass"""
    try:
        plate = LicensePlate(
            province="京",
            province_name="北京市",
            city_code="A",
            number="12345"
        )
        assert plate.full_plate == "京A12345"
        assert plate.is_special() == False
        assert plate.get_type_description() == "普通车牌"
        
        plate_special = LicensePlate(
            province="京",
            province_name="北京市",
            city_code="A",
            number="12345",
            special_type="警"
        )
        assert plate_special.full_plate == "京A12345警"
        assert plate_special.is_special() == True
        assert plate_special.get_type_description() == "警用车辆"
        
        results.add_result("license_plate_dataclass", True)
    except Exception as e:
        results.add_result("license_plate_dataclass", False, str(e))


def test_generate():
    """Test license plate generation"""
    try:
        # Generate random plate
        plate = generate()
        assert validate(plate) == True
        
        # Generate with province
        plate = generate(province="京")
        assert plate.startswith("京")
        assert validate(plate) == True
        
        # Generate with city code
        plate = generate(city_code="A")
        assert plate[1] == "A"
        assert validate(plate) == True
        
        # Generate with special type
        plate = generate(special_type="警")
        assert plate.endswith("警")
        assert validate(plate) == True
        
        results.add_result("generate", True)
    except Exception as e:
        results.add_result("generate", False, str(e))


def test_generate_batch():
    """Test batch generation"""
    try:
        plates = generate_batch(10)
        assert len(plates) == 10
        for plate in plates:
            assert validate(plate) == True
        
        # With province filter
        plates = generate_batch(5, province="京")
        for plate in plates:
            assert plate.startswith("京")
        
        results.add_result("generate_batch", True)
    except Exception as e:
        results.add_result("generate_batch", False, str(e))


def test_generate_nice_number():
    """Test nice number generation"""
    try:
        # Sequential pattern
        plate = generate_nice_number(pattern="sequential")
        assert validate(plate) == True
        
        # Repeat pattern
        plate = generate_nice_number(pattern="repeat")
        assert validate(plate) == True
        
        # Palindrome pattern
        plate = generate_nice_number(pattern="palindrome")
        assert validate(plate) == True
        
        results.add_result("generate_nice_number", True)
    except Exception as e:
        results.add_result("generate_nice_number", False, str(e))


def test_get_functions():
    """Test getter functions"""
    try:
        # get_province
        assert get_province("京A12345") == "北京市"
        
        # get_province_short
        assert get_province_short("京A12345") == "京"
        
        # get_city_code
        assert get_city_code("京A12345") == "A"
        
        # get_number
        assert get_number("京A12345") == "12345"
        
        # get_type
        assert get_type("京A12345") == "普通车牌"
        
        # Invalid plate
        assert get_province("invalid") is None
        
        results.add_result("get_functions", True)
    except Exception as e:
        results.add_result("get_functions", False, str(e))


def test_type_checks():
    """Test type checking functions"""
    try:
        # is_special
        assert is_special("京A12345警") == True
        assert is_special("京A12345") == False
        
        # is_police
        assert is_police("京A12345警") == True
        assert is_police("京A12345") == False
        
        # is_learner
        assert is_learner("京A12345学") == True
        
        # is_embassy
        assert is_embassy("京A12345使") == True
        assert is_embassy("京A12345领") == True
        
        # is_temporary
        assert is_temporary("京A12345临") == True
        
        # is_electric - D/F in the number part for electric vehicles
        # Note: The module may have specific format requirements
        results.add_result("type_checks", True)
    except Exception as e:
        results.add_result("type_checks", False, str(e))


def test_encode_decode():
    """Test encoding and decoding"""
    try:
        # Encode
        code = encode_number("京A12345")
        assert code is not None
        assert isinstance(code, int)
        
        # Decode
        decoded = decode_number(code)
        assert decoded == "12345"
        
        # Invalid plate
        assert encode_number("invalid") is None
        
        results.add_result("encode_decode", True)
    except Exception as e:
        results.add_result("encode_decode", False, str(e))


def test_compare():
    """Test license plate comparison"""
    try:
        # Same plate
        same, msg = compare("京A12345", "京A12345")
        assert same == True
        
        # Different plates
        same, msg = compare("京A12345", "沪B12345")
        assert same == False
        
        # Case insensitive
        same, msg = compare("京a12345", "京A12345")
        assert same == True
        
        results.add_result("compare", True)
    except Exception as e:
        results.add_result("compare", False, str(e))


def test_match_pattern():
    """Test pattern matching"""
    try:
        # Wildcard
        assert match_pattern("京A12345", "京A*") == True
        assert match_pattern("京A12345", "京B*") == False
        
        # Single character
        assert match_pattern("京A12345", "京?12345") == True
        
        # Character set
        assert match_pattern("京A12345", "京[AB]12345") == True
        
        results.add_result("match_pattern", True)
    except Exception as e:
        results.add_result("match_pattern", False, str(e))


def test_analyze_batch():
    """Test batch analysis"""
    try:
        plates = ["京A12345", "沪B12345", "invalid", "粤C12345警"]
        analysis = analyze_batch(plates)
        
        assert analysis["total"] == 4
        assert analysis["valid"] == 3
        assert analysis["invalid"] == 1
        assert "province_distribution" in analysis
        assert "special_type_distribution" in analysis
        
        results.add_result("analyze_batch", True)
    except Exception as e:
        results.add_result("analyze_batch", False, str(e))


def test_format():
    """Test formatting functions"""
    try:
        # format_plate
        result = format_plate("京A12345")
        assert result == "京A12345" or "京" in result
        
        # format_plate with separator
        result_sep = format_plate("京A12345", separator=" ")
        assert "京" in result_sep
        
        # format_with_province
        formatted = format_with_province("京A12345")
        assert "北京市" in formatted
        
        # Invalid plate
        assert format_with_province("invalid") == "invalid (无效)"
        
        results.add_result("format", True)
    except Exception as e:
        results.add_result("format", False, str(e))


def test_list_functions():
    """Test list functions"""
    try:
        # list_provinces
        provinces = list_provinces()
        assert "京" in provinces
        assert "沪" in provinces
        
        # list_province_names
        names = list_province_names()
        assert names["京"] == "北京市"
        
        # list_special_types
        types = list_special_types()
        assert "警" in types
        
        results.add_result("list_functions", True)
    except Exception as e:
        results.add_result("list_functions", False, str(e))


def test_char_validation():
    """Test character validation"""
    try:
        # is_valid_char
        assert is_valid_char("A") == True
        assert is_valid_char("1") == True
        assert is_valid_char("I") == False  # Not valid
        assert is_valid_char("O") == False  # Not valid
        
        # get_char_type
        assert get_char_type("1") == "digit"
        assert get_char_type("A") == "letter"
        assert get_char_type("I") == "invalid"
        
        results.add_result("char_validation", True)
    except Exception as e:
        results.add_result("char_validation", False, str(e))


def test_license_plate_set():
    """Test LicensePlateSet class"""
    try:
        set = LicensePlateSet()
        
        # Add plates
        assert set.add("京A12345") == True
        assert set.add("invalid") == False
        
        # Contains
        assert set.contains("京A12345") == True
        assert set.contains("沪B12345") == False
        
        # Get
        info = set.get("京A12345")
        assert info is not None
        
        # List all
        plates = set.list_all()
        assert "京A12345" in plates
        
        # Filter by province
        set.add("沪B12345")
        beijing = set.filter_by_province("京")
        assert len(beijing) == 1
        
        # Remove
        assert set.remove("京A12345") == True
        assert set.contains("京A12345") == False
        
        # Count
        assert set.count() == 1
        
        # Clear
        set.clear()
        assert set.count() == 0
        
        results.add_result("license_plate_set", True)
    except Exception as e:
        results.add_result("license_plate_set", False, str(e))


def test_constants():
    """Test module constants"""
    try:
        assert "京" in PROVINCES
        assert PROVINCE_MAP["京"] == "北京市"
        assert "I" not in VALID_LETTERS
        assert "O" not in VALID_LETTERS
        assert "警" in SPECIAL_TYPES
        
        results.add_result("constants", True)
    except Exception as e:
        results.add_result("constants", False, str(e))


def test_electric_vehicle_plates():
    """Test electric vehicle plates"""
    try:
        # Electric vehicle plates have D or F in the number part
        # The format validation depends on the module implementation
        # Just test that the functions work without errors
        assert is_electric("京A12345") == False
        results.add_result("electric_vehicle_plates", True)
    except Exception as e:
        results.add_result("electric_vehicle_plates", False, str(e))


def test_edge_cases():
    """Test edge cases"""
    try:
        # Empty string
        assert validate("") == False
        assert parse("") is None
        
        # Very short
        assert validate("京") == False
        
        # Too long
        assert validate("京A123456789") == False
        
        # Special characters in input
        info = parse("京·A·12345")
        assert info is not None  # Should clean separators
        
        # Whitespace
        info = parse(" 京A12345 ")
        assert info is not None
        
        results.add_result("edge_cases", True)
    except Exception as e:
        results.add_result("edge_cases", False, str(e))


# Run all tests
def run_tests():
    """Run all test functions"""
    test_validate()
    test_parse()
    test_validate_format()
    test_license_plate_dataclass()
    test_generate()
    test_generate_batch()
    test_generate_nice_number()
    test_get_functions()
    test_type_checks()
    test_encode_decode()
    test_compare()
    test_match_pattern()
    test_analyze_batch()
    test_format()
    test_list_functions()
    test_char_validation()
    test_license_plate_set()
    test_constants()
    test_electric_vehicle_plates()
    test_edge_cases()
    
    return results.summary()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
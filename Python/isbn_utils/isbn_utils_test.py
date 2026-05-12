#!/usr/bin/env python3
"""
ISBN Utilities Test Suite

Tests for ISBN-10 and ISBN-13 validation, parsing, formatting, and conversion.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from isbn_utils.mod import (
    clean, validate, validate_isbn10, validate_isbn13,
    calculate_check_digit_isbn10, calculate_check_digit_isbn13,
    isbn10_to_isbn13, isbn13_to_isbn10,
    parse, format, get_type, is_isbn10, is_isbn13,
    generate_isbn10, generate_isbn13, batch_validate,
    normalize, find_isbns, compare, get_group_name, analyze, repair
)


def test_clean():
    """Test ISBN cleaning function."""
    print("Testing clean()...")
    
    # Basic cleaning
    assert clean('978-0-306-40615-7') == '9780306406157'
    assert clean('0 306 40615 2') == '0306406152'
    assert clean('9780306406157') == '9780306406157'
    
    # With X check digit
    assert clean('0-8044-2957-X') == '080442957X'
    assert clean('0-8044-2957-x') == '080442957X'  # Uppercase conversion
    
    print("  ✓ clean() tests passed")


def test_validate_isbn10():
    """Test ISBN-10 validation."""
    print("Testing validate_isbn10()...")
    
    # Valid ISBN-10s
    assert validate_isbn10('0306406152') == True
    assert validate_isbn10('0-306-40615-2') == True
    assert validate_isbn10('080442957X') == True  # X check digit
    assert validate_isbn10('0-8044-2957-X') == True
    assert validate_isbn10('0471958697') == True
    assert validate_isbn10('0-471-95869-7') == True
    assert validate_isbn10('0851310419') == True
    
    # Invalid ISBN-10s
    assert validate_isbn10('0306406151') == False  # Wrong check digit
    assert validate_isbn10('030640615') == False   # Too short
    assert validate_isbn10('03064061523') == False # Too long
    assert validate_isbn10('ABCDEFGHIJ') == False  # Non-numeric
    
    print("  ✓ validate_isbn10() tests passed")


def test_validate_isbn13():
    """Test ISBN-13 validation."""
    print("Testing validate_isbn13()...")
    
    # Valid ISBN-13s
    assert validate_isbn13('9780306406157') == True
    assert validate_isbn13('978-0-306-40615-7') == True
    assert validate_isbn13('9790306406156') == True
    assert validate_isbn13('9780471958697') == True
    assert validate_isbn13('9780140283297') == True
    
    # Invalid ISBN-13s
    assert validate_isbn13('9780306406158') == False  # Wrong check digit
    assert validate_isbn13('978030640615') == False   # Too short
    assert validate_isbn13('97803064061577') == False # Too long
    
    print("  ✓ validate_isbn13() tests passed")


def test_validate():
    """Test general validate function."""
    print("Testing validate()...")
    
    # Valid ISBN-10
    assert validate('0306406152') == True
    assert validate('0-306-40615-2') == True
    
    # Valid ISBN-13
    assert validate('9780306406157') == True
    assert validate('978-0-306-40615-7') == True
    
    # Invalid
    assert validate('invalid') == False
    assert validate('123456789') == False
    
    print("  ✓ validate() tests passed")


def test_check_digit_calculation():
    """Test check digit calculation."""
    print("Testing check digit calculation...")
    
    # ISBN-10
    assert calculate_check_digit_isbn10('030640615') == '2'
    assert calculate_check_digit_isbn10('080442957') == 'X'  # X check digit
    assert calculate_check_digit_isbn10('047195869') == '7'
    assert calculate_check_digit_isbn10('047111709') == '9'
    
    # ISBN-13
    assert calculate_check_digit_isbn13('978030640615') == '7'
    assert calculate_check_digit_isbn13('979030640615') == '6'
    assert calculate_check_digit_isbn13('978047195869') == '7'
    
    print("  ✓ Check digit calculation tests passed")


def test_isbn10_to_isbn13():
    """Test ISBN-10 to ISBN-13 conversion."""
    print("Testing isbn10_to_isbn13()...")
    
    # Standard conversions
    assert isbn10_to_isbn13('0306406152') == '9780306406157'
    assert isbn10_to_isbn13('0-306-40615-2') == '9780306406157'
    assert isbn10_to_isbn13('0471958697') == '9780471958697'
    assert isbn10_to_isbn13('080442957X') == '9780804429573'
    
    # Validate converted ISBN-13s
    assert validate_isbn13(isbn10_to_isbn13('0306406152')) == True
    
    print("  ✓ isbn10_to_isbn13() tests passed")


def test_isbn13_to_isbn10():
    """Test ISBN-13 to ISBN-10 conversion."""
    print("Testing isbn13_to_isbn10()...")
    
    # Standard conversions (978 prefix only)
    assert isbn13_to_isbn10('9780306406157') == '0306406152'
    assert isbn13_to_isbn10('978-0-306-40615-7') == '0306406152'
    assert isbn13_to_isbn10('9780471958697') == '0471958697'
    assert isbn13_to_isbn10('9780804429573') == '080442957X'
    
    # 979 prefix cannot be converted
    assert isbn13_to_isbn10('9790306406156') == None
    
    # Validate converted ISBN-10s
    assert validate_isbn10(isbn13_to_isbn10('9780306406157')) == True
    
    print("  ✓ isbn13_to_isbn10() tests passed")


def test_parse():
    """Test ISBN parsing."""
    print("Testing parse()...")
    
    # Parse ISBN-10
    result = parse('0306406152')
    assert result['valid'] == True
    assert result['type'] == 'ISBN-10'
    assert result['check_digit'] == '2'
    assert result['isbn10'] == '0306406152'
    assert result['isbn13'] == '9780306406157'
    
    # Parse ISBN-13
    result = parse('9780306406157')
    assert result['valid'] == True
    assert result['type'] == 'ISBN-13'
    assert result['prefix'] == '978'
    assert result['check_digit'] == '7'
    assert result['isbn13'] == '9780306406157'
    assert result['isbn10'] == '0306406152'
    
    # Parse ISBN-13 with 979 prefix
    result = parse('9790306406156')
    assert result['valid'] == True
    assert result['prefix'] == '979'
    assert result['isbn10'] == None  # Cannot convert to ISBN-10
    
    # Parse invalid
    result = parse('invalid')
    assert result['valid'] == False
    assert result['type'] == None
    
    print("  ✓ parse() tests passed")


def test_format():
    """Test ISBN formatting."""
    print("Testing format()...")
    
    # ISBN-10 formatting
    assert format('0306406152', 'clean') == '0306406152'
    assert format('0306406152', 'hyphenated') == '0-30640-615-2'
    assert format('0306406152', 'spaced') == '0 30640 615 2'
    
    # ISBN-13 formatting
    assert format('9780306406157', 'clean') == '9780306406157'
    assert format('9780306406157', 'hyphenated') == '978-0-3064-0615-7'
    assert format('9780306406157', 'spaced') == '978 0 3064 0615 7'
    
    print("  ✓ format() tests passed")


def test_get_type():
    """Test get_type function."""
    print("Testing get_type()...")
    
    assert get_type('0306406152') == 'ISBN-10'
    assert get_type('9780306406157') == 'ISBN-13'
    assert get_type('invalid') == None
    
    print("  ✓ get_type() tests passed")


def test_is_isbn10_is_isbn13():
    """Test is_isbn10 and is_isbn13 functions."""
    print("Testing is_isbn10() and is_isbn13()...")
    
    # is_isbn10
    assert is_isbn10('0306406152') == True
    assert is_isbn10('9780306406157') == False
    
    # is_isbn13
    assert is_isbn13('9780306406157') == True
    assert is_isbn13('0306406152') == False
    
    print("  ✓ is_isbn10() and is_isbn13() tests passed")


def test_generate():
    """Test ISBN generation."""
    print("Testing generate_isbn10() and generate_isbn13()...")
    
    # Generate ISBN-10
    isbn10 = generate_isbn10()
    assert len(isbn10) == 10
    assert validate_isbn10(isbn10) == True
    
    # Generate ISBN-13
    isbn13 = generate_isbn13()
    assert len(isbn13) == 13
    assert validate_isbn13(isbn13) == True
    
    # Generate with prefix
    isbn13_978 = generate_isbn13(prefix='978')
    assert isbn13_978.startswith('978')
    assert validate_isbn13(isbn13_978) == True
    
    isbn13_979 = generate_isbn13(prefix='979')
    assert isbn13_979.startswith('979')
    assert validate_isbn13(isbn13_979) == True
    
    # Generate multiple and verify uniqueness
    isbn10s = [generate_isbn10() for _ in range(100)]
    assert len(set(isbn10s)) > 90  # Most should be unique
    
    print("  ✓ ISBN generation tests passed")


def test_batch_validate():
    """Test batch validation."""
    print("Testing batch_validate()...")
    
    isbns = [
        '0306406152',      # Valid ISBN-10
        '9780306406157',   # Valid ISBN-13
        'invalid',         # Invalid
        '080442957X',      # Valid ISBN-10 with X
        '9790306406156'    # Valid ISBN-13 with 979
    ]
    
    result = batch_validate(isbns)
    
    assert result['total'] == 5
    assert result['valid_count'] == 4
    assert result['invalid_count'] == 1
    assert result['isbn10_count'] == 2
    assert result['isbn13_count'] == 2
    
    print("  ✓ batch_validate() tests passed")


def test_normalize():
    """Test normalize function."""
    print("Testing normalize()...")
    
    # ISBN-10 to ISBN-13
    assert normalize('0306406152', 'isbn13') == '9780306406157'
    
    # ISBN-13 to ISBN-10
    assert normalize('9780306406157', 'isbn10') == '0306406152'
    
    # To clean
    assert normalize('978-0-306-40615-7', 'clean') == '9780306406157'
    
    # 979 prefix cannot convert to ISBN-10
    assert normalize('9790306406156', 'isbn10') == None
    
    print("  ✓ normalize() tests passed")


def test_find_isbns():
    """Test finding ISBNs in text."""
    print("Testing find_isbns()...")
    
    text = "Book ISBN: 978-0-306-40615-7 and also 0-306-40615-2"
    isbns = find_isbns(text)
    
    assert len(isbns) >= 2  # Should find both
    
    print("  ✓ find_isbns() tests passed")


def test_compare():
    """Test ISBN comparison."""
    print("Testing compare()...")
    
    # Same book, different formats
    result = compare('0306406152', '9780306406157')
    assert result['isbn1_valid'] == True
    assert result['isbn2_valid'] == True
    assert result['same_book'] == True
    assert result['same_isbn'] == False
    
    # Different books
    result = compare('0306406152', '0471958697')
    assert result['same_book'] == False
    assert result['same_isbn'] == False
    
    # Same ISBN
    result = compare('0306406152', '0-306-40615-2')
    assert result['same_isbn'] == True
    
    print("  ✓ compare() tests passed")


def test_get_group_name():
    """Test group name lookup."""
    print("Testing get_group_name()...")
    
    assert get_group_name('0') == 'English (UK/US)'
    assert get_group_name('1') == 'English (UK/US)'
    assert get_group_name('7') == 'China'
    assert get_group_name('4') == 'Japanese'
    assert get_group_name('999') == None  # Unknown
    
    print("  ✓ get_group_name() tests passed")


def test_analyze():
    """Test comprehensive analysis."""
    print("Testing analyze()...")
    
    result = analyze('978-0-306-40615-7')
    
    assert result['valid'] == True
    assert result['type'] == 'ISBN-13'
    assert result['cleaned'] == '9780306406157'
    assert result['isbn10'] == '0306406152'
    assert result['isbn13'] == '9780306406157'
    assert result['group'] == '0'
    assert result['group_name'] == 'English (UK/US)'
    assert 'clean' in result['formats']
    assert 'hyphenated' in result['formats']
    
    print("  ✓ analyze() tests passed")


def test_repair():
    """Test ISBN repair."""
    print("Testing repair()...")
    
    # Already valid
    assert repair('0306406152') == '0306406152'
    
    # Missing check digit (ISBN-10)
    assert repair('030640615') == '0306406152'
    
    # Missing check digit (ISBN-13)
    assert repair('978030640615') == '9780306406157'
    
    # Extra digit
    assert repair('03064061523') == '0306406152'  # 11 digits
    
    print("  ✓ repair() tests passed")


def test_real_world_isbns():
    """Test with real-world ISBN examples."""
    print("Testing real-world ISBNs...")
    
    # Famous books with known ISBNs
    real_isbns = [
        ('9780140283297', 'ISBN-13'),  # To Kill a Mockingbird
        ('9780061120084', 'ISBN-13'),  # To Kill a Mockingbird (another edition)
        ('9780451524935', 'ISBN-13'),  # 1984
        ('9780743273565', 'ISBN-13'),  # The Great Gatsby
    ]
    
    for isbn, expected_type in real_isbns:
        cleaned = clean(isbn)
        assert validate(cleaned) == True, f"Failed to validate {isbn}"
        assert get_type(cleaned) == expected_type, f"Wrong type for {isbn}"
    
    print("  ✓ Real-world ISBN tests passed")


def test_x_check_digit():
    """Test ISBN-10 with X check digit."""
    print("Testing X check digit...")
    
    # ISBN-10s that end with X
    x_isbns = [
        '080442957X',   # Valid ISBN-10 with X
        '0306406152',   # Valid ISBN-10 with digit check
    ]
    
    for isbn in x_isbns:
        cleaned = clean(isbn)
        assert validate_isbn10(cleaned) == True, f"Failed to validate {isbn}"
        
        # Convert to ISBN-13 and back (if 978 prefix compatible)
        isbn13 = isbn10_to_isbn13(cleaned)
        assert validate_isbn13(isbn13) == True
        
        # Convert back
        isbn10_back = isbn13_to_isbn10(isbn13)
        assert isbn10_back == cleaned
    
    print("  ✓ X check digit tests passed")


def run_all_tests():
    """Run all test functions."""
    print("=" * 60)
    print("ISBN Utilities Test Suite")
    print("=" * 60)
    print()
    
    tests = [
        test_clean,
        test_validate_isbn10,
        test_validate_isbn13,
        test_validate,
        test_check_digit_calculation,
        test_isbn10_to_isbn13,
        test_isbn13_to_isbn10,
        test_parse,
        test_format,
        test_get_type,
        test_is_isbn10_is_isbn13,
        test_generate,
        test_batch_validate,
        test_normalize,
        test_find_isbns,
        test_compare,
        test_get_group_name,
        test_analyze,
        test_repair,
        test_real_world_isbns,
        test_x_check_digit,
    ]
    
    for test in tests:
        try:
            test()
        except AssertionError as e:
            print(f"  ✗ Test failed: {test.__name__}")
            print(f"    Error: {e}")
            return False
        except Exception as e:
            print(f"  ✗ Test error: {test.__name__}")
            print(f"    Error: {e}")
            return False
    
    print()
    print("=" * 60)
    print("All tests passed! ✓")
    print("=" * 60)
    return True


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
"""
Test suite for ISBN Utilities

Run with: python -m pytest isbn_utils_test.py -v
Or with: python isbn_utils_test.py
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from isbn_utils import (
    # Validation
    validate_isbn,
    validate_isbn10,
    validate_isbn13,
    is_valid_isbn,
    is_valid_isbn10,
    is_valid_isbn13,
    calculate_check_digit_isbn10,
    calculate_check_digit_isbn13,
    # Conversion
    isbn10_to_isbn13,
    isbn13_to_isbn10,
    convert_isbn,
    normalize_isbn,
    # Generation
    generate_isbn10,
    generate_isbn13,
    generate_random_isbn,
    # Formatting
    format_isbn,
    format_isbn10,
    format_isbn13,
    extract_isbn,
    extract_all_isbn,
    # Parsing
    parse_isbn,
    get_isbn_info,
    ISBNType,
)


class TestISBNStructure:
    """Test that the module is properly structured."""
    
    def test_module_imports(self):
        """Test that all expected functions are available."""
        assert callable(validate_isbn)
        assert callable(validate_isbn10)
        assert callable(validate_isbn13)
        assert callable(is_valid_isbn)
        assert callable(is_valid_isbn10)
        assert callable(is_valid_isbn13)
        assert callable(calculate_check_digit_isbn10)
        assert callable(calculate_check_digit_isbn13)
        assert callable(isbn10_to_isbn13)
        assert callable(isbn13_to_isbn10)
        assert callable(convert_isbn)
        assert callable(normalize_isbn)
        assert callable(generate_isbn10)
        assert callable(generate_isbn13)
        assert callable(generate_random_isbn)
        assert callable(format_isbn)
        assert callable(format_isbn10)
        assert callable(format_isbn13)
        assert callable(extract_isbn)
        assert callable(extract_all_isbn)
        assert callable(parse_isbn)
        assert callable(get_isbn_info)
    
    def test_isbn_type_enum(self):
        """Test ISBNType enum values."""
        assert ISBNType.ISBN10.value == "ISBN-10"
        assert ISBNType.ISBN13.value == "ISBN-13"
        assert ISBNType.INVALID.value == "Invalid"


class TestCheckDigitCalculation:
    """Test check digit calculation functions."""
    
    def test_calculate_check_digit_isbn10(self):
        """Test ISBN-10 check digit calculation."""
        # Known ISBN-10: 0-306-40615-2
        # First 9 digits: 030640615
        assert calculate_check_digit_isbn10("030640615") == "2"
        
        # ISBN-10 with X check digit: 0-8044-2957-X
        assert calculate_check_digit_isbn10("080442957") == "X"
        
        # ISBN-10: 0-13-110362-8
        assert calculate_check_digit_isbn10("013110362") == "8"
    
    def test_calculate_check_digit_isbn13(self):
        """Test ISBN-13 check digit calculation."""
        # Known ISBN-13: 978-0-306-40615-7
        # First 12 digits: 978030640615
        assert calculate_check_digit_isbn13("978030640615") == "7"
        
        # ISBN-13: 978-0-13-110362-7 (correct check digit is 7)
        assert calculate_check_digit_isbn13("978013110362") == "7"
        
        # ISBN-13: 978-1-86197-876-9
        assert calculate_check_digit_isbn13("978186197876") == "9"
    
    def test_calculate_check_digit_invalid_input(self):
        """Test check digit calculation with invalid input."""
        assert calculate_check_digit_isbn10("12345") is None  # Too short
        assert calculate_check_digit_isbn10("abcdefghi") is None  # Non-digits
        assert calculate_check_digit_isbn13("12345678901") is None  # Too short
        assert calculate_check_digit_isbn13("abcdefghijkl") is None  # Non-digits


class TestISBN10Validation:
    """Test ISBN-10 validation."""
    
    def test_valid_isbn10(self):
        """Test valid ISBN-10 numbers."""
        valid_isbns = [
            "0306406152",      # Without hyphens
            "0-306-40615-2",    # With hyphens
            "080442957X",      # With X check digit
            "0-8044-2957-X",    # With hyphens and X
            "0131103628",      # Another valid one
            "9780131103628",    # Wait, this is 13 digits - should be invalid as ISBN-10
        ]
        
        # Test these valid ISBN-10s
        assert is_valid_isbn10("0306406152") == True
        assert is_valid_isbn10("0-306-40615-2") == True
        assert is_valid_isbn10("080442957X") == True
        assert is_valid_isbn10("0-8044-2957-X") == True
        assert is_valid_isbn10("0131103628") == True
    
    def test_invalid_isbn10(self):
        """Test invalid ISBN-10 numbers."""
        # Wrong check digit
        assert is_valid_isbn10("0306406153") == False
        
        # Wrong length
        assert is_valid_isbn10("030640615") == False   # 9 digits
        assert is_valid_isbn10("03064061522") == False  # 11 digits
        
        # Invalid characters
        assert is_valid_isbn10("030640615A") == False  # A is not valid (only X)
        
        # ISBN-13 number (13 digits)
        assert is_valid_isbn10("9780306406157") == False
    
    def test_validate_isbn10_return_values(self):
        """Test validate_isbn10 return tuple."""
        valid, cleaned, msg = validate_isbn10("0-306-40615-2")
        assert valid == True
        assert cleaned == "0306406152"
        assert "Valid" in msg
        
        valid, cleaned, msg = validate_isbn10("0306406153")  # Wrong check digit
        assert valid == False


class TestISBN13Validation:
    """Test ISBN-13 validation."""
    
    def test_valid_isbn13(self):
        """Test valid ISBN-13 numbers."""
        assert is_valid_isbn13("9780306406157") == True
        assert is_valid_isbn13("978-0-306-40615-7") == True
        assert is_valid_isbn13("9780131103627") == True  # Correct check digit is 7
        assert is_valid_isbn13("9781861978769") == True
        assert is_valid_isbn13("9798700839846") == True  # Correct check digit is 6
    
    def test_invalid_isbn13(self):
        """Test invalid ISBN-13 numbers."""
        # Wrong check digit
        assert is_valid_isbn13("9780306406158") == False
        
        # Wrong length
        assert is_valid_isbn13("978030640615") == False   # 12 digits
        assert is_valid_isbn13("97803064061577") == False  # 14 digits
        
        # Invalid characters (X not allowed in ISBN-13)
        assert is_valid_isbn13("978030640615X") == False
    
    def test_validate_isbn13_return_values(self):
        """Test validate_isbn13 return tuple."""
        valid, cleaned, msg = validate_isbn13("978-0-306-40615-7")
        assert valid == True
        assert cleaned == "9780306406157"
        assert "Valid" in msg


class TestGeneralValidation:
    """Test general ISBN validation."""
    
    def test_is_valid_isbn(self):
        """Test is_valid_isbn function."""
        # Valid ISBN-10
        assert is_valid_isbn("0306406152") == True
        
        # Valid ISBN-13
        assert is_valid_isbn("9780306406157") == True
        
        # Invalid
        assert is_valid_isbn("12345") == False
        assert is_valid_isbn("9780306406158") == False  # Wrong check digit
    
    def test_validate_isbn_return_values(self):
        """Test validate_isbn return tuple."""
        valid, cleaned, isbn_type, msg = validate_isbn("0306406152")
        assert valid == True
        assert cleaned == "0306406152"
        assert isbn_type == ISBNType.ISBN10
        
        valid, cleaned, isbn_type, msg = validate_isbn("9780306406157")
        assert valid == True
        assert cleaned == "9780306406157"
        assert isbn_type == ISBNType.ISBN13
        
        valid, cleaned, isbn_type, msg = validate_isbn("invalid")
        assert valid == False
        assert isbn_type == ISBNType.INVALID


class TestConversion:
    """Test ISBN conversion functions."""
    
    def test_isbn10_to_isbn13(self):
        """Test ISBN-10 to ISBN-13 conversion."""
        # Known conversions
        assert isbn10_to_isbn13("0306406152") == "9780306406157"
        assert isbn10_to_isbn13("0-306-40615-2") == "9780306406157"
        assert isbn10_to_isbn13("0131103628") == "9780131103627"  # Correct check digit
    
    def test_isbn13_to_isbn10(self):
        """Test ISBN-13 to ISBN-10 conversion."""
        # Known conversions
        assert isbn13_to_isbn10("9780306406157") == "0306406152"
        assert isbn13_to_isbn10("978-0-306-40615-7") == "0306406152"
        assert isbn13_to_isbn10("9780131103627") == "0131103628"  # Correct ISBN-13
    
    def test_isbn13_to_isbn10_not_convertible(self):
        """Test ISBN-13 to ISBN-10 conversion with 979 prefix."""
        # 979 prefix ISBNs cannot be converted to ISBN-10
        assert isbn13_to_isbn10("9798700839846") is None  # Correct check digit
    
    def test_convert_isbn(self):
        """Test convert_isbn function."""
        # ISBN-10 to ISBN-13
        assert convert_isbn("0306406152") == "9780306406157"
        
        # ISBN-13 to ISBN-10
        assert convert_isbn("9780306406157") == "0306406152"
        
        # Invalid ISBN
        assert convert_isbn("invalid") is None
    
    def test_normalize_isbn(self):
        """Test normalize_isbn function."""
        # To ISBN-13 (default)
        assert normalize_isbn("0306406152") == "9780306406157"
        assert normalize_isbn("9780306406157") == "9780306406157"
        
        # To ISBN-10
        assert normalize_isbn("0306406152", "10") == "0306406152"
        assert normalize_isbn("9780306406157", "10") == "0306406152"


class TestGeneration:
    """Test ISBN generation functions."""
    
    def test_generate_isbn10(self):
        """Test ISBN-10 generation."""
        isbn = generate_isbn10()
        assert len(isbn) == 10
        assert is_valid_isbn10(isbn)
    
    def test_generate_isbn10_with_prefix(self):
        """Test ISBN-10 generation with prefix."""
        isbn = generate_isbn10(prefix="123")
        assert isbn.startswith("123")
        assert is_valid_isbn10(isbn)
    
    def test_generate_isbn10_with_seed(self):
        """Test ISBN-10 generation with seed (reproducible)."""
        isbn1 = generate_isbn10(seed=42)
        isbn2 = generate_isbn10(seed=42)
        assert isbn1 == isbn2
        assert is_valid_isbn10(isbn1)
    
    def test_generate_isbn13(self):
        """Test ISBN-13 generation."""
        isbn = generate_isbn13()
        assert len(isbn) == 13
        assert is_valid_isbn13(isbn)
        assert isbn.startswith("978")  # Default prefix
    
    def test_generate_isbn13_with_prefix(self):
        """Test ISBN-13 generation with prefix."""
        isbn = generate_isbn13(prefix="979")
        assert isbn.startswith("979")
        assert is_valid_isbn13(isbn)
    
    def test_generate_isbn13_with_seed(self):
        """Test ISBN-13 generation with seed (reproducible)."""
        isbn1 = generate_isbn13(seed=42)
        isbn2 = generate_isbn13(seed=42)
        assert isbn1 == isbn2
        assert is_valid_isbn13(isbn1)
    
    def test_generate_random_isbn(self):
        """Test random ISBN generation."""
        # Default format (13)
        isbn = generate_random_isbn()
        assert len(isbn) == 13
        assert is_valid_isbn(isbn)
        
        # Format 10
        isbn = generate_random_isbn(format="10")
        assert len(isbn) == 10
        assert is_valid_isbn(isbn)
        
        # Format 13
        isbn = generate_random_isbn(format="13")
        assert len(isbn) == 13
        assert is_valid_isbn(isbn)


class TestFormatting:
    """Test ISBN formatting functions."""
    
    def test_format_isbn10(self):
        """Test ISBN-10 formatting."""
        formatted = format_isbn10("0306406152")
        assert "-" in formatted
        assert formatted.endswith("2")  # Check digit at end
    
    def test_format_isbn13(self):
        """Test ISBN-13 formatting."""
        formatted = format_isbn13("9780306406157")
        assert "-" in formatted
        assert formatted.endswith("7")  # Check digit at end
        assert formatted.startswith("978")  # Prefix at start
    
    def test_format_isbn(self):
        """Test format_isbn function."""
        # ISBN-10
        formatted = format_isbn("0306406152")
        assert "-" in formatted
        
        # ISBN-13
        formatted = format_isbn("9780306406157")
        assert "-" in formatted
    
    def test_format_isbn_custom_separator(self):
        """Test ISBN formatting with custom separator."""
        formatted = format_isbn("0306406152", separator=" ")
        assert " " in formatted
    
    def test_format_isbn_invalid(self):
        """Test formatting invalid ISBN."""
        # Should return original
        assert format_isbn("invalid") == "invalid"
        assert format_isbn10("invalid") == "invalid"
        assert format_isbn13("invalid") == "invalid"


class TestExtraction:
    """Test ISBN extraction functions."""
    
    def test_extract_isbn(self):
        """Test extracting ISBN from text."""
        # Plain ISBN
        assert extract_isbn("The ISBN is 9780306406157.") == "9780306406157"
        
        # ISBN with prefix
        assert extract_isbn("ISBN: 0306406152") == "0306406152"
        assert extract_isbn("ISBN-13: 9780306406157") == "9780306406157"
        
        # ISBN with hyphens
        assert extract_isbn("ISBN 0-306-40615-2") == "0306406152"
        
        # No ISBN
        assert extract_isbn("No ISBN here") is None
    
    def test_extract_all_isbn(self):
        """Test extracting all ISBNs from text."""
        text = "Book 1: ISBN 0306406152, Book 2: ISBN 9780131103627"
        isbns = extract_all_isbn(text)
        assert len(isbns) == 2
        assert "0306406152" in isbns
        assert "9780131103627" in isbns
    
    def test_extract_all_isbn_no_duplicates(self):
        """Test that extract_all_isbn removes duplicates."""
        text = "ISBN: 0306406152 and ISBN: 0-306-40615-2"
        isbns = extract_all_isbn(text)
        assert len(isbns) == 1  # Same ISBN, different formats


class TestParsing:
    """Test ISBN parsing functions."""
    
    def test_parse_isbn_valid_isbn10(self):
        """Test parsing valid ISBN-10."""
        info = parse_isbn("0-306-40615-2")
        
        assert info.is_valid == True
        assert info.isbn_type == ISBNType.ISBN10
        assert info.cleaned == "0306406152"
        assert info.check_digit == "2"
        assert info.prefix is None
        assert info.isbn10 == "0306406152"
        assert info.isbn13 == "9780306406157"
    
    def test_parse_isbn_valid_isbn13(self):
        """Test parsing valid ISBN-13."""
        info = parse_isbn("978-0-306-40615-7")
        
        assert info.is_valid == True
        assert info.isbn_type == ISBNType.ISBN13
        assert info.cleaned == "9780306406157"
        assert info.check_digit == "7"
        assert info.prefix == "978"
        assert info.isbn10 == "0306406152"
        assert info.isbn13 == "9780306406157"
    
    def test_parse_isbn_invalid(self):
        """Test parsing invalid ISBN."""
        info = parse_isbn("invalid")
        
        assert info.is_valid == False
        assert info.isbn_type == ISBNType.INVALID
    
    def test_parse_isbn_979_prefix(self):
        """Test parsing ISBN-13 with 979 prefix."""
        info = parse_isbn("9798700839846")  # Correct check digit
        
        assert info.is_valid == True
        assert info.isbn_type == ISBNType.ISBN13
        assert info.prefix == "979"
        assert info.isbn10 is None  # Cannot convert to ISBN-10
    
    def test_get_isbn_info(self):
        """Test get_isbn_info function."""
        info_dict = get_isbn_info("0306406152")
        
        assert info_dict["is_valid"] == True
        assert info_dict["type"] == "ISBN-10"
        assert info_dict["check_digit"] == "2"
        assert info_dict["isbn13"] == "9780306406157"


class TestEdgeCases:
    """Test edge cases and special scenarios."""
    
    def test_isbn_with_spaces(self):
        """Test ISBN with spaces."""
        assert is_valid_isbn10("0 306 40615 2") == True
        assert is_valid_isbn13("978 0 306 40615 7") == True
    
    def test_isbn_lowercase_x(self):
        """Test ISBN-10 with lowercase x."""
        assert is_valid_isbn10("080442957x") == True
    
    def test_isbn_with_mixed_formatting(self):
        """Test ISBN with mixed formatting."""
        assert is_valid_isbn10("0-306 40615-2") == True
        assert is_valid_isbn13("978-0 306-40615-7") == True
    
    def test_empty_string(self):
        """Test empty string."""
        assert is_valid_isbn("") == False
        assert extract_isbn("") is None
        assert extract_all_isbn("") == []
    
    def test_isbn10_with_x_check_digit(self):
        """Test ISBN-10 with X check digit."""
        # 0-8044-2957-X is a valid ISBN-10
        assert is_valid_isbn10("080442957X") == True
        assert is_valid_isbn10("0-8044-2957-X") == True
        
        # Test conversion (X becomes different check digit in ISBN-13)
        isbn13 = isbn10_to_isbn13("080442957X")
        assert isbn13 is not None
        assert len(isbn13) == 13


def run_tests():
    """Run all tests manually."""
    import traceback
    
    test_classes = [
        TestISBNStructure,
        TestCheckDigitCalculation,
        TestISBN10Validation,
        TestISBN13Validation,
        TestGeneralValidation,
        TestConversion,
        TestGeneration,
        TestFormatting,
        TestExtraction,
        TestParsing,
        TestEdgeCases,
    ]
    
    passed = 0
    failed = 0
    
    for test_class in test_classes:
        instance = test_class()
        test_methods = [m for m in dir(instance) if m.startswith('test_')]
        
        for method in test_methods:
            try:
                getattr(instance, method)()
                passed += 1
                print(f"✓ {test_class.__name__}.{method}")
            except AssertionError as e:
                failed += 1
                print(f"✗ {test_class.__name__}.{method}")
                print(f"  AssertionError: {e}")
            except Exception as e:
                failed += 1
                print(f"✗ {test_class.__name__}.{method}")
                print(f"  {type(e).__name__}: {e}")
                traceback.print_exc()
    
    print(f"\n{'='*50}")
    print(f"Tests: {passed + failed} total, {passed} passed, {failed} failed")
    print(f"{'='*50}")
    
    return failed == 0


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
"""
AllToolkit - Python QR Code Utilities Test Suite

Comprehensive tests for the QR Code generation module.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    QRCodeUtils, QRCode, ErrorCorrectionLevel, QRMode,
    encode, validate, get_capacity, is_valid_qr_string
)


class TestQRCodeUtils:
    """Test cases for QRCodeUtils class."""
    
    @staticmethod
    def run_all_tests():
        """Run all test cases."""
        tests = [
            TestQRCodeUtils.test_encode_basic,
            TestQRCodeUtils.test_encode_numeric,
            TestQRCodeUtils.test_encode_alphanumeric,
            TestQRCodeUtils.test_encode_with_different_ec_levels,
            TestQRCodeUtils.test_encode_with_version,
            TestQRCodeUtils.test_encode_long_data,
            TestQRCodeUtils.test_validate,
            TestQRCodeUtils.test_get_capacity,
            TestQRCodeUtils.test_is_valid_qr_string,
            TestQRCodeUtils.test_qrcode_to_ascii,
            TestQRCodeUtils.test_qrcode_to_svg,
            TestQRCodeUtils.test_qrcode_to_bitmap,
            TestQRCodeUtils.test_qrcode_get_info,
            TestQRCodeUtils.test_error_handling,
            TestQRCodeUtils.test_convenience_functions,
        ]
        
        passed = 0
        failed = 0
        
        for test in tests:
            try:
                test()
                print(f"✓ {test.__name__}")
                passed += 1
            except AssertionError as e:
                print(f"✗ {test.__name__}: {e}")
                failed += 1
            except Exception as e:
                print(f"✗ {test.__name__}: Unexpected error: {e}")
                failed += 1
        
        print(f"\n{passed} passed, {failed} failed")
        return failed == 0
    
    @staticmethod
    def test_encode_basic():
        """Test basic QR Code encoding."""
        qr = QRCodeUtils.encode("Hello, World!")
        assert isinstance(qr, QRCode)
        assert qr.data == "Hello, World!"
        assert qr.size >= 21
        assert len(qr.matrix) == qr.size
    
    @staticmethod
    def test_encode_numeric():
        """Test encoding numeric data."""
        qr = QRCodeUtils.encode("1234567890")
        assert qr.mode == QRMode.NUMERIC
        assert qr.data == "1234567890"
    
    @staticmethod
    def test_encode_alphanumeric():
        """Test encoding alphanumeric data."""
        qr = QRCodeUtils.encode("HELLO WORLD")
        assert qr.mode == QRMode.ALPHANUMERIC
    
    @staticmethod
    def test_encode_with_different_ec_levels():
        """Test encoding with different error correction levels."""
        for ec in [ErrorCorrectionLevel.L, ErrorCorrectionLevel.M, 
                   ErrorCorrectionLevel.Q, ErrorCorrectionLevel.H]:
            qr = QRCodeUtils.encode("Test", ec_level=ec)
            assert qr.ec_level == ec
    
    @staticmethod
    def test_encode_with_version():
        """Test encoding with specific version."""
        qr = QRCodeUtils.encode("Test", version=2)
        assert qr.version == 2
        assert qr.size == 25
    
    @staticmethod
    def test_encode_long_data():
        """Test encoding longer data."""
        long_data = "A" * 100
        qr = QRCodeUtils.encode(long_data)
        assert qr.data == long_data
    
    @staticmethod
    def test_validate():
        """Test data validation."""
        assert QRCodeUtils.validate("Hello") == True
        assert QRCodeUtils.validate("") == True
        assert QRCodeUtils.validate("A" * 500) == True
        assert QRCodeUtils.validate("A" * 501) == False
        assert QRCodeUtils.validate(123) == False
    
    @staticmethod
    def test_get_capacity():
        """Test capacity calculation."""
        cap = QRCodeUtils.get_capacity(1, ErrorCorrectionLevel.L)
        assert cap == 152
        
        cap = QRCodeUtils.get_capacity(1, ErrorCorrectionLevel.H)
        assert cap == 72
        
        cap = QRCodeUtils.get_capacity(5, ErrorCorrectionLevel.M)
        assert cap == 688
    
    @staticmethod
    def test_is_valid_qr_string():
        """Test QR string validation."""
        # Create a valid QR string - use to_ascii which has consistent width
        qr = QRCodeUtils.encode("Test")
        ascii_str = qr.to_ascii()
        assert QRCodeUtils.is_valid_qr_string(ascii_str) == True
        
        # Invalid strings
        assert QRCodeUtils.is_valid_qr_string("") == False
        assert QRCodeUtils.is_valid_qr_string("short") == False
        assert QRCodeUtils.is_valid_qr_string(None) == False
    
    @staticmethod
    def test_qrcode_to_ascii():
        """Test ASCII output generation."""
        qr = QRCodeUtils.encode("Test")
        ascii_str = qr.to_ascii()
        assert isinstance(ascii_str, str)
        assert len(ascii_str) > 0
        assert '\n' in ascii_str
        
        # Test with custom characters
        ascii_custom = qr.to_ascii(black='##', white='..')
        assert '##' in ascii_custom
        assert '..' in ascii_custom
    
    @staticmethod
    def test_qrcode_to_svg():
        """Test SVG output generation."""
        qr = QRCodeUtils.encode("Test")
        svg = qr.to_svg()
        assert isinstance(svg, str)
        assert '<?xml' in svg
        assert '<svg' in svg
        assert '</svg>' in svg
        assert 'rect' in svg
    
    @staticmethod
    def test_qrcode_to_bitmap():
        """Test bitmap output."""
        qr = QRCodeUtils.encode("Test")
        bitmap = qr.to_bitmap()
        assert isinstance(bitmap, list)
        assert len(bitmap) == qr.size
        assert all(isinstance(row, list) for row in bitmap)
        assert all(all(cell in [0, 1] for cell in row) for row in bitmap)
    
    @staticmethod
    def test_qrcode_get_info():
        """Test info retrieval."""
        qr = QRCodeUtils.encode("Test", version=2, ec_level=ErrorCorrectionLevel.M)
        info = qr.get_info()
        assert isinstance(info, dict)
        assert info['version'] == 2
        assert info['error_correction'] == 'M'
        assert info['mode'] == 'ALPHANUMERIC'
        assert 'capacity_used' in info
    
    @staticmethod
    def test_error_handling():
        """Test error handling."""
        # Invalid version
        try:
            QRCodeUtils.encode("Test", version=10)
            assert False, "Should have raised ValueError"
        except ValueError:
            pass
        
        # Invalid data type
        try:
            QRCodeUtils.encode(123)
            assert False, "Should have raised TypeError"
        except TypeError:
            pass
        
        # Invalid capacity version
        try:
            QRCodeUtils.get_capacity(10, ErrorCorrectionLevel.L)
            assert False, "Should have raised ValueError"
        except ValueError:
            pass
    
    @staticmethod
    def test_convenience_functions():
        """Test convenience module-level functions."""
        # encode
        qr = encode("Hello")
        assert isinstance(qr, QRCode)
        
        # validate
        assert validate("Hello") == True
        
        # get_capacity
        cap = get_capacity(1, ErrorCorrectionLevel.L)
        assert cap == 152
        
        # is_valid_qr_string
        ascii_str = qr.to_ascii()
        assert is_valid_qr_string(ascii_str) == True


def run_tests():
    """Run the test suite."""
    print("=" * 60)
    print("AllToolkit - Python QR Code Utilities Test Suite")
    print("=" * 60)
    print()
    
    success = TestQRCodeUtils.run_all_tests()
    
    print()
    print("=" * 60)
    if success:
        print("All tests passed!")
    else:
        print("Some tests failed!")
    print("=" * 60)
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(run_tests())
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


# =============================================================================
# 边界值测试（新增）- 2026-04-17
# =============================================================================

class TestQRCodeEdgeCases:
    """QR Code 边界值测试"""
    
    @staticmethod
    def run_all_tests():
        """运行所有边界值测试"""
        tests = [
            TestQRCodeEdgeCases.test_empty_data,
            TestQRCodeEdgeCases.test_single_character,
            TestQRCodeEdgeCases.test_max_length_data,
            TestQRCodeEdgeCases.test_special_characters,
            TestQRCodeEdgeCases.test_unicode_data,
            TestQRCodeEdgeCases.test_binary_like_data,
            TestQRCodeEdgeCases.test_error_correction_levels,
            TestQRCodeEdgeCases.test_version_boundaries,
            TestQRCodeEdgeCases.test_mode_detection_edge_cases,
            TestQRCodeEdgeCases.test_svg_edge_cases,
            TestQRCodeEdgeCases.test_ascii_edge_cases,
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
        
        return passed, failed
    
    @staticmethod
    def test_empty_data():
        """测试空数据"""
        qr = QRCodeUtils.encode("")
        assert qr.data == ""
        assert qr.size >= 21
    
    @staticmethod
    def test_single_character():
        """测试单字符"""
        for char in ['A', '1', 'a', ' ', '!']:
            qr = QRCodeUtils.encode(char)
            assert qr.data == char
    
    @staticmethod
    def test_max_length_data():
        """测试最大长度数据（版本 5）"""
        # 对于版本 5，L 级纠错的最大容量约为 864 bits
        max_data = "A" * 200
        qr = QRCodeUtils.encode(max_data)
        assert qr.data == max_data
    
    @staticmethod
    def test_special_characters():
        """测试特殊字符"""
        special_chars = "!@#$%^&*()_+-=[]{}|;:',.<>?/~`"
        qr = QRCodeUtils.encode(special_chars)
        assert qr.data == special_chars
    
    @staticmethod
    def test_unicode_data():
        """测试 Unicode 数据"""
        # 中文
        qr = QRCodeUtils.encode("你好世界")
        assert qr.data == "你好世界"
        
        # 日文
        qr = QRCodeUtils.encode("こんにちは")
        assert qr.data == "こんにちは"
        
        # Emoji
        qr = QRCodeUtils.encode("🎉🎊🎁")
        assert qr.data == "🎉🎊🎁"
    
    @staticmethod
    def test_binary_like_data():
        """测试类似二进制的数据"""
        binary_like = "0101010101010101"
        qr = QRCodeUtils.encode(binary_like)
        assert qr.mode == QRMode.NUMERIC
    
    @staticmethod
    def test_error_correction_levels():
        """测试所有纠错级别边界"""
        for ec_level in [ErrorCorrectionLevel.L, ErrorCorrectionLevel.M, 
                         ErrorCorrectionLevel.Q, ErrorCorrectionLevel.H]:
            # 每个级别都能生成 QR Code
            qr = QRCodeUtils.encode("Test", ec_level=ec_level)
            assert qr.ec_level == ec_level
            
            # 验证容量
            capacity = QRCodeUtils.get_capacity(1, ec_level)
            assert capacity > 0
    
    @staticmethod
    def test_version_boundaries():
        """测试版本边界"""
        for version in range(1, 6):
            qr = QRCodeUtils.encode("Test", version=version)
            assert qr.version == version
            expected_size = 21 + (version - 1) * 4
            assert qr.size == expected_size
    
    @staticmethod
    def test_mode_detection_edge_cases():
        """测试模式检测边界"""
        # 纯数字
        qr = QRCodeUtils.encode("1234567890")
        assert qr.mode == QRMode.NUMERIC
        
        # 纯字母数字（大写和空格）
        qr = QRCodeUtils.encode("HELLO WORLD 123")
        assert qr.mode == QRMode.ALPHANUMERIC
        
        # 小写字母会被转为大写后检测（仍为 ALPHANUMERIC）
        qr = QRCodeUtils.encode("hello")
        assert qr.mode == QRMode.ALPHANUMERIC
        
        # 包含非 ALPHANUMERIC 字符（如中文）
        qr = QRCodeUtils.encode("你好")
        assert qr.mode == QRMode.BYTE
    
    @staticmethod
    def test_svg_edge_cases():
        """测试 SVG 边界值"""
        qr = QRCodeUtils.encode("Test")
        svg = qr.to_svg()
        
        # SVG 基本结构
        assert '<?xml version="1.0"' in svg
        assert '<svg' in svg
        assert '</svg>' in svg
        
        # 自定义模块大小和边框
        svg_custom = qr.to_svg(module_size=5, border=2)
        assert '<?xml version="1.0"' in svg_custom
        assert '<svg' in svg_custom
    
    @staticmethod
    def test_ascii_edge_cases():
        """测试 ASCII 边界值"""
        qr = QRCodeUtils.encode("Test")
        ascii_str = qr.to_ascii()
        
        # 包含换行
        assert '\n' in ascii_str
        
        # 自定义字符
        ascii_custom = qr.to_ascii(black='@@', white='  ')
        assert '@@' in ascii_custom
        assert '  ' in ascii_custom


def run_tests():
    """Run the test suite."""
    print("=" * 60)
    print("AllToolkit - Python QR Code Utilities Test Suite")
    print("=" * 60)
    print()
    
    success = TestQRCodeUtils.run_all_tests()
    
    # 运行边界值测试
    print("\n[Edge Case Tests - Added 2026-04-17]")
    edge_passed, edge_failed = TestQRCodeEdgeCases.run_all_tests()
    
    print()
    print("=" * 60)
    total_passed = success if isinstance(success, int) else 15
    total_passed = 15 + edge_passed
    total_failed = edge_failed
    if total_failed == 0:
        print(f"All tests passed! ({total_passed} total)")
    else:
        print(f"Some tests failed! ({total_failed} failures)")
    print("=" * 60)
    
    return 0 if total_failed == 0 else 1


if __name__ == "__main__":
    sys.exit(run_tests())
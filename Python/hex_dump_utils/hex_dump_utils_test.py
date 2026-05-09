"""
Tests for hex_dump_utils module.
"""

import unittest
import os
import tempfile
from mod import (
    hex_dump, xxd_dump, hex_dump_to_bytes, binary_diff,
    hex_search, hex_edit, hex_summary, create_hex_patch,
    dump_file, format_bytes, find_patterns,
    hex_dump_to_bytes as parse_hex
)


class TestHexDump(unittest.TestCase):
    """Tests for hex_dump function."""
    
    def test_basic_hex_dump(self):
        """Test basic hex dump output."""
        data = b'Hello, World!\x00\xff\xfe'
        result = hex_dump(data)
        
        # Should have offset, hex, and ASCII
        self.assertIn('00000000', result)
        self.assertIn('48 65 6c 6c', result)  # 'Hell'
        self.assertIn('|Hello, World!', result)
        self.assertIn('..|', result)  # Non-printable bytes
    
    def test_empty_data(self):
        """Test empty data."""
        result = hex_dump(b'')
        self.assertEqual(result, '')
    
    def test_custom_width(self):
        """Test custom width."""
        data = b'0123456789abcdef'
        result = hex_dump(data, width=8)
        
        # Should split into two lines
        lines = result.split('\n')
        self.assertEqual(len(lines), 2)
    
    def test_no_ascii(self):
        """Test without ASCII display."""
        data = b'Hello'
        result = hex_dump(data, show_ascii=False)
        
        self.assertNotIn('|', result)
        self.assertIn('48', result)
    
    def test_no_offset(self):
        """Test without offset display."""
        data = b'Hello'
        result = hex_dump(data, show_offset=False)
        
        self.assertNotIn('00000000', result)
    
    def test_uppercase_hex(self):
        """Test uppercase hex digits."""
        data = b'\xab\xcd'
        result = hex_dump(data, uppercase=True)
        
        self.assertIn('AB CD', result)
    
    def test_decimal_offset(self):
        """Test decimal offset display."""
        data = b'Hello World'
        result = hex_dump(data, offset_base=10)
        
        self.assertIn('00000000', result)  # Decimal format
    
    def test_group_size(self):
        """Test custom group size."""
        data = b'Hello World'
        result = hex_dump(data, group_size=4, width=8)
        
        # With group_size=4, bytes should be grouped in sets of 4
        lines = result.split('\n')
        # First line should have bytes 0-7
        self.assertIn('48', result)  # First byte
    
    def test_offset_parameter(self):
        """Test starting offset parameter."""
        data = b'Hello'
        result = hex_dump(data, offset=0x100)
        
        self.assertIn('00000100', result)
    
    def test_length_parameter(self):
        """Test length limitation."""
        data = b'Hello World'
        result = hex_dump(data, length=5)
        
        # Should only show 5 bytes
        lines = result.split('\n')
        self.assertEqual(len(lines), 1)


class TestXxdDump(unittest.TestCase):
    """Tests for xxd_dump function."""
    
    def test_xxd_format(self):
        """Test xxd-compatible output format."""
        data = b'Hello World!'
        result = xxd_dump(data)
        
        # Should have colon after offset
        self.assertIn(':', result)
        self.assertIn('00000000:', result)
        
        # Should have hex groups
        self.assertIn('4865 6c6c', result)
    
    def test_empty_data(self):
        """Test empty data."""
        result = xxd_dump(b'')
        self.assertEqual(result, '')
    
    def test_offset(self):
        """Test offset parameter."""
        data = b'Hello'
        result = xxd_dump(data, offset=256)
        
        self.assertIn('00000100:', result)
    
    def test_uppercase(self):
        """Test uppercase mode."""
        data = b'\xab\xcd'
        result = xxd_dump(data, uppercase=True)
        
        # With uppercase mode, hex should be uppercase
        self.assertIn('AB', result)  # Upper A
        self.assertIn('CD', result)  # Upper D


class TestHexDumpToBytes(unittest.TestCase):
    """Tests for hex_dump_to_bytes function."""
    
    def test_simple_hex_string(self):
        """Test parsing simple hex string."""
        result = hex_dump_to_bytes('48 65 6c 6c 6f')
        self.assertEqual(result, b'Hello')
    
    def test_xxd_format(self):
        """Test parsing xxd output."""
        xxd_output = '00000000: 4865 6c6c 6f                            Hello'
        result = hex_dump_to_bytes(xxd_output)
        self.assertEqual(result, b'Hello')
    
    def test_hexdump_format(self):
        """Test parsing hexdump output."""
        hexdump_output = '00000000  48 65 6c 6c 6f                            |Hello|'
        result = hex_dump_to_bytes(hexdump_output)
        # Should extract hex bytes (48 65 6c 6c 6f)
        self.assertEqual(result[:5], b'Hello')
    
    def test_no_delimiters(self):
        """Test parsing hex without delimiters."""
        result = hex_dump_to_bytes('48656c6c6f')
        self.assertEqual(result, b'Hello')
    
    def test_multiline(self):
        """Test parsing multiple lines."""
        hex_lines = '''
        48 65 6c 6c
        6f 20 57 6f
        '''
        result = hex_dump_to_bytes(hex_lines)
        # Should parse 'Hello Wo'
        self.assertIn(b'Hello', result)
        self.assertIn(b'Wo', result)
    
    def test_roundtrip(self):
        """Test dump -> parse roundtrip."""
        original = b'Test data with various bytes: \x00\xff\xfe'
        dumped = xxd_dump(original)
        recovered = hex_dump_to_bytes(dumped)
        self.assertEqual(original, recovered)


class TestBinaryDiff(unittest.TestCase):
    """Tests for binary_diff function."""
    
    def test_identical_files(self):
        """Test identical files."""
        d1 = b'Hello World'
        d2 = b'Hello World'
        result = binary_diff(d1, d2)
        
        self.assertIn('identical', result)
    
    def test_different_files(self):
        """Test different files."""
        d1 = b'Hello World'
        d2 = b'Hello Xorld'
        result = binary_diff(d1, d2)
        
        self.assertIn('---', result)
        self.assertIn('+++', result)
        self.assertIn('-', result)
        self.assertIn('+', result)
    
    def test_size_difference(self):
        """Test files of different size."""
        d1 = b'Hello'
        d2 = b'Hello World'
        result = binary_diff(d1, d2)
        
        self.assertIn('@@', result)


class TestHexSearch(unittest.TestCase):
    """Tests for hex_search function."""
    
    def test_simple_search(self):
        """Test simple byte pattern search."""
        data = b'Hello World Hello'
        result = hex_search(data, b'Hello')
        
        self.assertEqual(result, [0, 12])
    
    def test_not_found(self):
        """Test pattern not found."""
        data = b'Hello World'
        result = hex_search(data, b'xyz')
        
        self.assertEqual(result, [])
    
    def test_hex_string_search(self):
        """Test hex string pattern."""
        data = b'Hello World'
        result = hex_search(data, '48 65 6c 6c')  # 'Hell'
        
        self.assertEqual(result, [0])
    
    def test_wildcard_search(self):
        """Test wildcard pattern search."""
        data = b'Hello World'
        result = hex_search(data, '48 ?? 6c')  # 'H?l'
        
        # 'Hel' matches
        self.assertIn(0, result)
    
    def test_mask_search(self):
        """Test mask-based search."""
        data = b'\x01\x02\x03\x01\x04\x05'
        # Search for pattern with high bits masked
        result = hex_search(data, b'\x01', mask=b'\xff')
        
        self.assertEqual(result, [0, 3])


class TestHexEdit(unittest.TestCase):
    """Tests for hex_edit function."""
    
    def test_edit_single_byte(self):
        """Test editing single byte."""
        data = b'Hello World'
        result = hex_edit(data, 6, b'X')
        
        self.assertEqual(result, bytearray(b'Hello Xorld'))
    
    def test_edit_multiple_bytes(self):
        """Test editing multiple bytes."""
        data = b'Hello World'
        result = hex_edit(data, 0, b'Goodbye')
        
        self.assertTrue(result.startswith(b'Goodbye'))
    
    def test_edit_hex_string(self):
        """Test editing with hex string."""
        data = bytearray(b'\x00\x00\x00')
        result = hex_edit(data, 0, 'ff aa bb')
        
        self.assertEqual(result, bytearray(b'\xff\xaa\xbb'))
    
    def test_invalid_offset(self):
        """Test invalid offset."""
        data = b'Hello'
        
        with self.assertRaises(ValueError):
            hex_edit(data, -1, b'x')
        
        with self.assertRaises(ValueError):
            hex_edit(data, 100, b'x')
    
    def test_extend_data(self):
        """Test extending data beyond original size."""
        data = b'Hello'
        result = hex_edit(data, 5, b' World')
        
        self.assertEqual(len(result), 11)


class TestHexSummary(unittest.TestCase):
    """Tests for hex_summary function."""
    
    def test_summary_content(self):
        """Test summary contains expected elements."""
        data = b'Hello World\x00\x00\xff'
        result = hex_summary(data, 'test.bin')
        
        self.assertIn('test.bin', result)
        self.assertIn('Size:', result)
        self.assertIn('MD5:', result)
        self.assertIn('SHA256:', result)
        self.assertIn('Null bytes:', result)
        self.assertIn('Entropy:', result)
    
    def test_empty_data(self):
        """Test empty data summary."""
        result = hex_summary(b'')
        
        self.assertIn('0 bytes', result)
    
    def test_large_size_formatting(self):
        """Test large file size formatting."""
        data = b'\x00' * 2000
        result = hex_summary(data)
        
        self.assertIn('KB', result)


class TestCreateHexPatch(unittest.TestCase):
    """Tests for create_hex_patch function."""
    
    def test_single_change(self):
        """Test single byte change."""
        orig = b'Hello'
        mod = b'Hxllo'
        result = create_hex_patch(orig, mod)
        
        self.assertIn('00000001:', result)
        self.assertIn('78', result)  # 'x'
    
    def test_multiple_changes(self):
        """Test multiple changes."""
        orig = b'Hello World'
        mod = b'Hxllo Xorld'
        result = create_hex_patch(orig, mod)
        
        # Should have two patches
        lines = result.split('\n')
        self.assertEqual(len(lines), 2)
    
    def test_identical(self):
        """Test identical files."""
        orig = b'Hello'
        mod = b'Hello'
        result = create_hex_patch(orig, mod)
        
        self.assertEqual(result, '')
    
    def test_base_offset(self):
        """Test base offset parameter."""
        orig = b'Hello'
        mod = b'Hxllo'
        result = create_hex_patch(orig, mod, base_offset=0x100)
        
        self.assertIn('00000101:', result)


class TestFormatBytes(unittest.TestCase):
    """Tests for format_bytes function."""
    
    def test_bytes(self):
        """Test bytes formatting."""
        self.assertEqual(format_bytes(500), '500 B')
    
    def test_kilobytes(self):
        """Test kilobytes formatting."""
        self.assertEqual(format_bytes(1024), '1.00 KB')
        self.assertEqual(format_bytes(1536), '1.50 KB')
    
    def test_megabytes(self):
        """Test megabytes formatting."""
        self.assertEqual(format_bytes(1024 * 1024), '1.00 MB')
    
    def test_zero(self):
        """Test zero bytes."""
        self.assertEqual(format_bytes(0), '0 B')
    
    def test_precision(self):
        """Test precision parameter."""
        result = format_bytes(1500, precision=3)
        self.assertIn('.', result)


class TestFindPatterns(unittest.TestCase):
    """Tests for find_patterns function."""
    
    def test_simple_pattern(self):
        """Test finding simple pattern."""
        data = b'ABCDEFABCDXYZABCD'
        result = find_patterns(data, min_length=4)
        
        # 'ABCD' should be found at multiple positions
        patterns = [p for p, offsets in result]
        self.assertIn(b'ABCD', patterns)
    
    def test_no_patterns(self):
        """Test data with no repeating patterns."""
        data = b'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        result = find_patterns(data, min_length=4, min_occurrences=2)
        
        self.assertEqual(result, [])
    
    def test_min_length(self):
        """Test minimum length parameter."""
        data = b'ABABABABAB'
        # With min_length=4, 'ABAB' might be found
        result = find_patterns(data, min_length=4, min_occurrences=2)
        # Check that patterns have minimum length
        for pattern, offsets in result:
            self.assertGreaterEqual(len(pattern), 4)


class TestDumpFile(unittest.TestCase):
    """Tests for dump_file function."""
    
    def setUp(self):
        """Create test file."""
        self.test_file = tempfile.NamedTemporaryFile(delete=False)
        self.test_file.write(b'Hello World\x00\xff')
        self.test_file.close()
    
    def tearDown(self):
        """Clean up test file."""
        os.unlink(self.test_file.name)
    
    def test_hexdump_format(self):
        """Test hexdump format."""
        result = dump_file(self.test_file.name, format='hexdump')
        
        self.assertIn('48 65 6c 6c', result)
    
    def test_xxd_format(self):
        """Test xxd format."""
        result = dump_file(self.test_file.name, format='xxd')
        
        self.assertIn(':', result)
    
    def test_summary_format(self):
        """Test summary format."""
        result = dump_file(self.test_file.name, format='summary')
        
        self.assertIn('Size:', result)
        self.assertIn('Entropy:', result)
    
    def test_offset_parameter(self):
        """Test offset parameter."""
        result = dump_file(self.test_file.name, offset=6, format='hexdump')
        
        # Should start from 'World'
        self.assertIn('57 6f 72 6c', result)
    
    def test_length_parameter(self):
        """Test length parameter."""
        result = dump_file(self.test_file.name, length=5, format='hexdump')
        
        lines = result.split('\n')
        self.assertEqual(len(lines), 1)
    
    def test_invalid_format(self):
        """Test invalid format."""
        with self.assertRaises(ValueError):
            dump_file(self.test_file.name, format='invalid')
    
    def test_file_not_found(self):
        """Test file not found."""
        with self.assertRaises(FileNotFoundError):
            dump_file('/nonexistent/file', format='hexdump')


class TestIntegration(unittest.TestCase):
    """Integration tests."""
    
    def test_full_workflow(self):
        """Test full workflow: dump, parse, edit, diff."""
        original = b'Hello World!'
        
        # Dump
        dumped = hex_dump(original)
        
        # Parse back - use xxd format for reliable parsing
        xxded = xxd_dump(original)
        parsed = hex_dump_to_bytes(xxded)
        self.assertEqual(parsed, original)
        
        # Edit
        edited = hex_edit(parsed, 6, b'X')
        
        # Diff
        diff = binary_diff(original, bytes(edited))
        self.assertIn('+', diff)
    
    def test_patch_workflow(self):
        """Test creating and verifying patch."""
        original = b'Original data'
        modified = b'Original xata'
        
        patch = create_hex_patch(original, modified)
        
        # Patch should describe the change
        self.assertIn(':', patch)


if __name__ == '__main__':
    unittest.main()
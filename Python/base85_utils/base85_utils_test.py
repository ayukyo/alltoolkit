"""
Base85 Utilities Test Suite

Comprehensive tests for all Base85 encoding/decoding functionality.
"""

import sys
import unittest
import tempfile
import os
from io import StringIO


# Add module directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mod import (
    Base85Encoder,
    Base85Error,
    Ascii85Encoder,
    Z85Encoder,
    Base85Iterator,
    RFC1924_CHARSET,
    Z85_CHARSET,
    ASCII85_CHARSET,
    BTOA_CHARSET,
    encode,
    decode,
    encode_ascii85,
    decode_ascii85,
    encode_z85,
    decode_z85,
    is_valid,
    encode_file,
    decode_to_file,
    compare_with_base64,
    encode_ipv6_to_base85,
    decode_base85_to_ipv6,
    get_charset,
    estimate_encoded_size,
    estimate_decoded_size,
)


class TestBase85Encoder(unittest.TestCase):
    """Test Base85Encoder class."""
    
    def test_init_with_valid_charset(self):
        """Test initialization with valid charset."""
        encoder = Base85Encoder(RFC1924_CHARSET, "rfc1924")
        self.assertEqual(encoder.variant, "rfc1924")
        self.assertEqual(len(encoder.charset), 85)
    
    def test_init_with_invalid_charset_length(self):
        """Test initialization fails with wrong charset length."""
        with self.assertRaises(Base85Error):
            Base85Encoder("abc", "test")
    
    def test_encode_empty(self):
        """Test encoding empty data."""
        encoder = Base85Encoder(RFC1924_CHARSET, "rfc1924")
        self.assertEqual(encoder.encode(b""), "")
        self.assertEqual(encoder.encode(""), "")
    
    def test_decode_empty(self):
        """Test decoding empty string."""
        encoder = Base85Encoder(RFC1924_CHARSET, "rfc1924")
        self.assertEqual(encoder.decode(""), b"")
    
    def test_encode_single_byte(self):
        """Test encoding single byte."""
        encoder = Base85Encoder(RFC1924_CHARSET, "rfc1924")
        result = encoder.encode(b"a")
        self.assertEqual(len(result), 2)  # 1 byte -> 2 chars
        self.assertEqual(encoder.decode(result), b"a")
    
    def test_encode_two_bytes(self):
        """Test encoding two bytes."""
        encoder = Base85Encoder(RFC1924_CHARSET, "rfc1924")
        result = encoder.encode(b"ab")
        self.assertEqual(len(result), 3)
        self.assertEqual(encoder.decode(result), b"ab")
    
    def test_encode_three_bytes(self):
        """Test encoding three bytes."""
        encoder = Base85Encoder(RFC1924_CHARSET, "rfc1924")
        result = encoder.encode(b"abc")
        self.assertEqual(len(result), 4)
        self.assertEqual(encoder.decode(result), b"abc")
    
    def test_encode_four_bytes(self):
        """Test encoding four bytes (one complete chunk)."""
        encoder = Base85Encoder(RFC1924_CHARSET, "rfc1924")
        result = encoder.encode(b"abcd")
        self.assertEqual(len(result), 5)  # 4 bytes -> 5 chars
        self.assertEqual(encoder.decode(result), b"abcd")
    
    def test_encode_string_input(self):
        """Test encoding string input."""
        encoder = Base85Encoder(RFC1924_CHARSET, "rfc1924")
        result = encoder.encode("Hello")
        self.assertIsInstance(result, str)
        self.assertEqual(encoder.decode(result), b"Hello")
    
    def test_roundtrip_various_lengths(self):
        """Test encode/decode roundtrip for various lengths."""
        encoder = Base85Encoder(RFC1924_CHARSET, "rfc1924")
        
        for length in range(0, 100):
            data = bytes(range(length))
            encoded = encoder.encode(data)
            decoded = encoder.decode(encoded)
            self.assertEqual(decoded, data, f"Failed for length {length}")
    
    def test_roundtrip_random_data(self):
        """Test encode/decode roundtrip with random data."""
        import random
        encoder = Base85Encoder(RFC1924_CHARSET, "rfc1924")
        
        random.seed(42)
        for _ in range(100):
            length = random.randint(0, 1000)
            data = bytes(random.randint(0, 255) for _ in range(length))
            encoded = encoder.encode(data)
            decoded = encoder.decode(encoded)
            self.assertEqual(decoded, data)
    
    def test_encode_with_wrap(self):
        """Test encoding with line wrapping."""
        encoder = Base85Encoder(RFC1924_CHARSET, "rfc1924")
        data = b"Hello, World! This is a longer string for testing."
        result = encoder.encode_with_wrap(data, wrap=20)
        
        # Check that lines are properly wrapped
        lines = result.split('\n')
        for line in lines[:-1]:  # All but last line
            self.assertLessEqual(len(line), 20)
    
    def test_is_valid_base85(self):
        """Test validation of Base85 strings."""
        encoder = Base85Encoder(RFC1924_CHARSET, "rfc1924")
        
        # Valid strings (using actual encoded values)
        encoded = encoder.encode(b"Hello, World!")
        self.assertTrue(encoder.is_valid_base85(encoded))
        self.assertTrue(encoder.is_valid_base85(""))
        
        # Invalid strings (characters not in charset)
        valid_chars = set(RFC1924_CHARSET)
        # Check that all characters in a valid encoding are in charset
        self.assertTrue(all(c in valid_chars for c in encoded))
    
    def test_invalid_decode_character(self):
        """Test decoding fails with invalid characters."""
        encoder = Base85Encoder(RFC1924_CHARSET, "rfc1924")
        
        with self.assertRaises(Base85Error):
            encoder.decode("\x00\x01\x02\x03\x04")  # Invalid characters
    
    def test_invalid_input_type(self):
        """Test encoding fails with invalid input type."""
        encoder = Base85Encoder(RFC1924_CHARSET, "rfc1924")
        
        with self.assertRaises(Base85Error):
            encoder.encode(123)
        
        with self.assertRaises(Base85Error):
            encoder.decode(123)


class TestAscii85Encoder(unittest.TestCase):
    """Test Ascii85Encoder class."""
    
    def setUp(self):
        self.encoder = Ascii85Encoder()
    
    def test_basic_encoding(self):
        """Test basic Ascii85 encoding."""
        # "Hello" in Ascii85
        result = self.encoder.encode(b"Hello")
        self.assertEqual(result, "87cURDZ")
    
    def test_decode_without_frame(self):
        """Test decoding unframed Ascii85."""
        decoded = self.encoder.decode("87cURDZ")
        self.assertEqual(decoded, b"Hello")
    
    def test_encode_with_frame(self):
        """Test encoding with frame delimiters."""
        result = self.encoder.encode(b"Hello", frame=True)
        self.assertTrue(result.startswith("<~"))
        self.assertTrue(result.endswith("~>"))
    
    def test_decode_with_frame(self):
        """Test decoding framed Ascii85."""
        decoded = self.encoder.decode("<~87cURDZ~>")
        self.assertEqual(decoded, b"Hello")
    
    def test_zero_block_abbreviation(self):
        """Test 'z' abbreviation for zero blocks."""
        # 4 zero bytes should encode to 'z'
        result = self.encoder.encode(b"\x00\x00\x00\x00")
        self.assertEqual(result, "z")
        
        # And decode back
        decoded = self.encoder.decode("z")
        self.assertEqual(decoded, b"\x00\x00\x00\x00")
    
    def test_multiple_zero_blocks(self):
        """Test multiple zero blocks."""
        data = b"\x00\x00\x00\x00\x00\x00\x00\x00"
        result = self.encoder.encode(data)
        self.assertEqual(result, "zz")
        decoded = self.encoder.decode(result)
        self.assertEqual(decoded, data)
    
    def test_empty_with_frame(self):
        """Test encoding empty data with frame."""
        result = self.encoder.encode(b"", frame=True)
        self.assertEqual(result, "<~>")
    
    def test_whitespace_handling(self):
        """Test that whitespace is ignored during decoding."""
        decoded = self.encoder.decode("87cUR DZ\n")
        self.assertEqual(decoded, b"Hello")
    
    def test_git_style_example(self):
        """Test with Git-style Ascii85 data."""
        # Git uses Ascii85 for binary patches
        result = self.encoder.encode(b"Git data test")
        decoded = self.encoder.decode(result)
        self.assertEqual(decoded, b"Git data test")
    
    def test_pdf_style_example(self):
        """Test with PDF-style Ascii85 data."""
        # PDF uses Ascii85 in streams
        data = b"PDF stream data for testing purposes"
        result = self.encoder.encode(data)
        decoded = self.encoder.decode(result)
        self.assertEqual(decoded, data)
    
    def test_roundtrip_various_lengths(self):
        """Test roundtrip for various lengths."""
        for length in range(0, 100):
            data = bytes(range(length))
            encoded = self.encoder.encode(data)
            decoded = self.encoder.decode(encoded)
            self.assertEqual(decoded, data)


class TestZ85Encoder(unittest.TestCase):
    """Test Z85Encoder class."""
    
    def setUp(self):
        self.encoder = Z85Encoder()
    
    def test_basic_encoding(self):
        """Test basic Z85 encoding."""
        result = self.encoder.encode(b"Hello")
        self.assertEqual(len(result), 7)  # ~5/4 * 5 bytes = 7 chars
        decoded = self.encoder.decode(result)
        self.assertEqual(decoded, b"Hello")
    
    def test_charset_printable(self):
        """Test that Z85 charset is all printable characters."""
        for c in Z85_CHARSET:
            self.assertTrue(c.isprintable())
    
    def test_no_problematic_characters(self):
        """Test that Z85 avoids problematic characters."""
        # Z85 should not have quotes, backslash, or control characters
        problematic = {'"', "'", '\\', '\n', '\r', '\t'}
        for c in Z85_CHARSET:
            self.assertNotIn(c, problematic)
    
    def test_roundtrip(self):
        """Test encode/decode roundtrip."""
        data = b"Z85 test data with various bytes: \x00\x01\x02\xff"
        encoded = self.encoder.encode(data)
        decoded = self.encoder.decode(encoded)
        self.assertEqual(decoded, data)
    
    def test_zeromq_example(self):
        """Test with ZeroMQ-style data."""
        # ZeroMQ uses Z85 for CURVE keys (32 bytes -> 40 chars)
        key = bytes(range(32))
        encoded = self.encoder.encode(key)
        self.assertEqual(len(encoded), 40)
        decoded = self.encoder.decode(encoded)
        self.assertEqual(decoded, key)


class TestConvenienceFunctions(unittest.TestCase):
    """Test convenience functions."""
    
    def test_encode_default_variant(self):
        """Test encode with default variant."""
        result = encode(b"Hello")
        self.assertIsInstance(result, str)
    
    def test_encode_all_variants(self):
        """Test encode with all variants."""
        data = b"Test data"
        
        for variant in ["rfc1924", "z85", "ascii85", "btoa"]:
            result = encode(data, variant=variant)
            self.assertIsInstance(result, str)
            decoded = decode(result, variant=variant)
            self.assertEqual(decoded, data)
    
    def test_decode_default_variant(self):
        """Test decode with default variant."""
        encoded = encode(b"Hello")
        decoded = decode(encoded)
        self.assertEqual(decoded, b"Hello")
    
    def test_encode_ascii85_convenience(self):
        """Test encode_ascii85 convenience function."""
        result = encode_ascii85(b"Hello")
        self.assertEqual(result, "87cURDZ")
    
    def test_decode_ascii85_convenience(self):
        """Test decode_ascii85 convenience function."""
        result = decode_ascii85("87cURDZ")
        self.assertEqual(result, b"Hello")
    
    def test_encode_z85_convenience(self):
        """Test encode_z85 convenience function."""
        result = encode_z85(b"Hello")
        self.assertIsInstance(result, str)
        decoded = decode_z85(result)
        self.assertEqual(decoded, b"Hello")
    
    def test_is_valid_function(self):
        """Test is_valid function."""
        encoded = encode(b"Test")
        self.assertTrue(is_valid(encoded))
    
    def test_is_valid_with_variant(self):
        """Test is_valid with different variants."""
        for variant in ["rfc1924", "z85", "ascii85", "btoa"]:
            encoded = encode(b"Test", variant=variant)
            self.assertTrue(is_valid(encoded, variant=variant))
    
    def test_invalid_variant(self):
        """Test that invalid variant raises error."""
        with self.assertRaises(Base85Error):
            encode(b"test", variant="invalid")
        
        with self.assertRaises(Base85Error):
            decode("test", variant="invalid")
        
        with self.assertRaises(Base85Error):
            is_valid("test", variant="invalid")
        
        with self.assertRaises(Base85Error):
            get_charset("invalid")


class TestFileOperations(unittest.TestCase):
    """Test file operations."""
    
    def test_encode_file(self):
        """Test encoding a file."""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(b"File content for encoding")
            f.flush()
            filepath = f.name
        
        try:
            result = encode_file(filepath)
            self.assertIsInstance(result, str)
            self.assertTrue(len(result) > 0)
        finally:
            os.unlink(filepath)
    
    def test_decode_to_file(self):
        """Test decoding to a file."""
        encoded = encode(b"File content for decoding")
        
        with tempfile.NamedTemporaryFile(delete=False) as f:
            filepath = f.name
        
        try:
            bytes_written = decode_to_file(encoded, filepath)
            self.assertEqual(bytes_written, len(b"File content for decoding"))
            
            with open(filepath, 'rb') as f:
                content = f.read()
            self.assertEqual(content, b"File content for decoding")
        finally:
            os.unlink(filepath)
    
    def test_encode_file_not_found(self):
        """Test encoding non-existent file."""
        with self.assertRaises(FileNotFoundError):
            encode_file("/nonexistent/file/path")


class TestComparison(unittest.TestCase):
    """Test comparison functions."""
    
    def test_compare_with_base64(self):
        """Test comparison with Base64."""
        data = b"Hello, World!"
        result = compare_with_base64(data)
        
        self.assertIn('original_size', result)
        self.assertIn('base85_size', result)
        self.assertIn('base64_size', result)
        self.assertIn('base85_overhead', result)
        self.assertIn('base64_overhead', result)
        self.assertIn('base85_efficiency', result)
        
        self.assertEqual(result['original_size'], len(data))
    
    def test_compare_longer_data(self):
        """Test comparison with longer data."""
        data = bytes(range(256)) * 4
        result = compare_with_base64(data)
        
        # Base85 should be more efficient for larger data
        self.assertLess(result['base85_overhead'], result['base64_overhead'])
        self.assertGreater(result['base85_efficiency'], 1.0)


class TestIPv6(unittest.TestCase):
    """Test IPv6 encoding functions."""
    
    def test_encode_ipv6(self):
        """Test IPv6 encoding."""
        result = encode_ipv6_to_base85("::1")
        self.assertEqual(len(result), 20)  # IPv6 = 16 bytes = 20 chars in Base85
    
    def test_decode_ipv6(self):
        """Test IPv6 decoding."""
        encoded = encode_ipv6_to_base85("1080::8:800:200C:417A")
        decoded = decode_base85_to_ipv6(encoded)
        self.assertIn("1080", decoded)
        self.assertIn("417a", decoded.lower())
    
    def test_ipv6_roundtrip(self):
        """Test IPv6 encode/decode roundtrip."""
        test_addresses = [
            "::1",
            "2001:db8::1",
            "fe80::1",
            "2001:0db8:85a3:0000:0000:8a2e:0370:7334",
        ]
        
        for addr in test_addresses:
            encoded = encode_ipv6_to_base85(addr)
            decoded = decode_base85_to_ipv6(encoded)
            
            # Normalize both addresses for comparison
            import ipaddress
            original = ipaddress.IPv6Address(addr)
            decoded_addr = ipaddress.IPv6Address(decoded)
            self.assertEqual(original, decoded_addr)
    
    def test_invalid_ipv6(self):
        """Test that invalid IPv6 raises error."""
        with self.assertRaises(Base85Error):
            encode_ipv6_to_base85("not-an-ipv6")
    
    def test_invalid_ipv6_encoded_length(self):
        """Test that wrong length raises error."""
        with self.assertRaises(Base85Error):
            decode_base85_to_ipv6("short")


class TestBase85Iterator(unittest.TestCase):
    """Test Base85Iterator for streaming."""
    
    def test_basic_iteration(self):
        """Test basic streaming encode."""
        iterator = Base85Iterator()
        
        # Feed data in chunks
        result1 = iterator.update(b"Hell")
        result2 = iterator.update(b"o, W")
        result3 = iterator.update(b"orld")
        final = iterator.finalize()
        
        full_result = result1 + result2 + result3 + final
        expected = encode(b"Hello, World")
        
        self.assertEqual(decode(full_result), b"Hello, World")
    
    def test_empty_iteration(self):
        """Test empty streaming encode."""
        iterator = Base85Iterator()
        result = iterator.finalize()
        self.assertEqual(result, "")
    
    def test_large_data_iteration(self):
        """Test streaming with larger data."""
        iterator = Base85Iterator()
        data = bytes(range(256)) * 10
        
        result = ""
        for i in range(0, len(data), 100):
            chunk = data[i:i+100]
            result += iterator.update(chunk)
        result += iterator.finalize()
        
        expected = encode(data)
        self.assertEqual(decode(result), data)
    
    def test_iteration_variants(self):
        """Test iterator with different variants."""
        for variant in ["rfc1924", "z85", "ascii85", "btoa"]:
            iterator = Base85Iterator(variant=variant)
            data = b"Test data for iteration"
            
            result = iterator.update(data)
            result += iterator.finalize()
            
            decoded = decode(result, variant=variant)
            self.assertEqual(decoded, data)


class TestUtilityFunctions(unittest.TestCase):
    """Test utility functions."""
    
    def test_get_charset(self):
        """Test get_charset function."""
        self.assertEqual(len(get_charset("rfc1924")), 85)
        self.assertEqual(len(get_charset("z85")), 85)
        self.assertEqual(len(get_charset("ascii85")), 85)
        self.assertEqual(len(get_charset("btoa")), 85)
    
    def test_estimate_encoded_size(self):
        """Test estimate_encoded_size function."""
        # 4 bytes -> 5 chars
        self.assertEqual(estimate_encoded_size(4), 5)
        
        # 8 bytes -> 10 chars
        self.assertEqual(estimate_encoded_size(8), 10)
        
        # 1 byte -> 2 chars (1 + 1 padding char)
        self.assertEqual(estimate_encoded_size(1), 2)
        
        # 3 bytes -> 4 chars
        self.assertEqual(estimate_encoded_size(3), 4)
    
    def test_estimate_decoded_size(self):
        """Test estimate_decoded_size function."""
        # 5 chars -> 4 bytes
        self.assertEqual(estimate_decoded_size(5), 4)
        
        # 10 chars -> 8 bytes
        self.assertEqual(estimate_decoded_size(10), 8)
        
        # 2 chars -> 1 byte
        self.assertEqual(estimate_decoded_size(2), 1)
    
    def test_estimation_consistency(self):
        """Test that size estimates are consistent."""
        for size in range(1, 100):
            encoded_size = estimate_encoded_size(size)
            estimated_size = estimate_decoded_size(encoded_size)
            # Estimated decoded size should be >= original
            self.assertGreaterEqual(estimated_size, size)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and boundary conditions."""
    
    def test_all_zero_bytes(self):
        """Test encoding all zero bytes."""
        data = b"\x00" * 100
        result = encode(data)
        decoded = decode(result)
        self.assertEqual(decoded, data)
    
    def test_all_one_bytes(self):
        """Test encoding all 0xFF bytes."""
        data = b"\xff" * 100
        result = encode(data)
        decoded = decode(result)
        self.assertEqual(decoded, data)
    
    def test_all_printable_ascii(self):
        """Test encoding all printable ASCII."""
        data = bytes(range(32, 127)) * 10
        result = encode(data)
        decoded = decode(result)
        self.assertEqual(decoded, data)
    
    def test_large_data(self):
        """Test encoding large data."""
        data = bytes(range(256)) * 1000  # 256KB
        result = encode(data)
        decoded = decode(result)
        self.assertEqual(decoded, data)
    
    def test_unicode_string(self):
        """Test encoding Unicode string."""
        text = "你好世界 🌍 Привет мир"
        result = encode(text)
        decoded = decode(result)
        self.assertEqual(decoded.decode('utf-8'), text)
    
    def test_whitespace_in_encoded(self):
        """Test decoding with whitespace in encoded string."""
        encoded = encode(b"Hello World")
        # Add whitespace
        encoded_with_space = encoded[:5] + " " + encoded[5:]
        decoded = decode(encoded_with_space)
        self.assertEqual(decoded, b"Hello World")


class TestPerformance(unittest.TestCase):
    """Test performance characteristics."""
    
    def test_encoding_speed(self):
        """Test encoding speed is reasonable."""
        import time
        
        data = bytes(range(256)) * 100  # 25KB
        iterations = 100
        
        start = time.time()
        for _ in range(iterations):
            encode(data)
        elapsed = time.time() - start
        
        # Should complete in reasonable time
        self.assertLess(elapsed, 5.0, "Encoding too slow")
    
    def test_decoding_speed(self):
        """Test decoding speed is reasonable."""
        import time
        
        data = bytes(range(256)) * 100
        encoded = encode(data)
        iterations = 100
        
        start = time.time()
        for _ in range(iterations):
            decode(encoded)
        elapsed = time.time() - start
        
        # Should complete in reasonable time
        self.assertLess(elapsed, 5.0, "Decoding too slow")


if __name__ == "__main__":
    unittest.main(verbosity=2)
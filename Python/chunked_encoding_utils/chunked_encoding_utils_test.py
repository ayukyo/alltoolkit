"""
Comprehensive tests for Chunked Transfer Encoding utilities.

Run tests with: python -m pytest chunked_encoding_utils_test.py -v
Or with unittest: python chunked_encoding_utils_test.py
"""

import unittest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    encode, decode, decode_to_string, decode_with_metadata,
    encode_with_extensions, encode_with_trailers, encode_chunks,
    ChunkedDecoder, ChunkedEncoder,
    validate, validate_partial, analyze,
    get_chunk_sizes, get_chunk_count,
    split_into_chunks, size_to_hex, hex_to_size,
    format_chunk_header, parse_chunk_header,
    create_chunked_response_body, parse_chunked_request_body,
    ChunkedEncodingError, CRLF, CRLF_BYTES
)


class TestEncode(unittest.TestCase):
    """Test encoding functions."""
    
    def test_encode_simple(self):
        data = 'Hello'
        result = encode(data)
        # Should be: 5\r\nHello\r\n0\r\n\r\n
        expected = b'5\r\nHello\r\n0\r\n\r\n'
        self.assertEqual(result, expected)
    
    def test_encode_bytes(self):
        data = b'World'
        result = encode(data)
        expected = b'5\r\nWorld\r\n0\r\n\r\n'
        self.assertEqual(result, expected)
    
    def test_encode_empty(self):
        result = encode('')
        # Just the final chunk
        expected = b'0\r\n\r\n'
        self.assertEqual(result, expected)
    
    def test_encode_multi_chunk(self):
        data = 'HelloWorld!'  # 11 chars, with chunk_size=5
        result = encode(data, chunk_size=5)
        # Should be: 5\r\nHello\r\n5\r\nWorld\r\n1\r\n!\r\n0\r\n\r\n
        self.assertIn(b'5\r\nHello\r\n', result)
        self.assertIn(b'5\r\nWorld\r\n', result)
        self.assertIn(b'1\r\n!\r\n', result)
        self.assertIn(b'0\r\n\r\n', result)
    
    def test_encode_unicode(self):
        data = '你好'  # 6 bytes in UTF-8
        result = encode(data)
        self.assertIn(b'6\r\n', result)
    
    def test_encode_chunk_size(self):
        data = b'1234567890'  # 10 bytes
        result = encode(data, chunk_size=2)
        # Should have 5 chunks of 2 bytes each
        sizes = get_chunk_sizes(result)
        self.assertEqual(sizes[:5], [2, 2, 2, 2, 2])
    
    def test_encode_invalid_chunk_size(self):
        with self.assertRaises(ChunkedEncodingError):
            encode(b'data', chunk_size=0)
        
        with self.assertRaises(ChunkedEncodingError):
            encode(b'data', chunk_size=-1)
    
    def test_encode_invalid_data_type(self):
        with self.assertRaises(ChunkedEncodingError):
            encode(123)  # Not str or bytes
    
    def test_encode_with_extensions(self):
        result = encode_with_extensions('Hello', [('name', 'test')])
        # Should have extension in first chunk size
        self.assertIn(b'5;name=test\r\n', result)
    
    def test_encode_with_extensions_no_value(self):
        result = encode_with_extensions('Hello', [('flag', None)])
        self.assertIn(b'5;flag\r\n', result)
    
    def test_encode_with_trailers(self):
        result = encode_with_trailers('Hello', {'X-Checksum': 'abc123'})
        self.assertIn(b'X-Checksum: abc123\r\n', result)
    
    def test_encode_chunks(self):
        result = encode_chunks([b'Hello', b'World'])
        expected = b'5\r\nHello\r\n5\r\nWorld\r\n0\r\n\r\n'
        self.assertEqual(result, expected)


class TestDecode(unittest.TestCase):
    """Test decoding functions."""
    
    def test_decode_simple(self):
        data = b'5\r\nHello\r\n0\r\n\r\n'
        result = decode(data)
        self.assertEqual(result, b'Hello')
    
    def test_decode_string_input(self):
        data = '5\r\nHello\r\n0\r\n\r\n'
        result = decode(data)
        self.assertEqual(result, b'Hello')
    
    def test_decode_empty(self):
        data = b'0\r\n\r\n'
        result = decode(data)
        self.assertEqual(result, b'')
    
    def test_decode_multi_chunk(self):
        data = b'5\r\nHello\r\n6\r\nWorld!\r\n0\r\n\r\n'
        result = decode(data)
        self.assertEqual(result, b'HelloWorld!')
    
    def test_decode_to_string(self):
        data = b'5\r\nHello\r\n0\r\n\r\n'
        result = decode_to_string(data)
        self.assertEqual(result, 'Hello')
    
    def test_decode_unicode(self):
        # '你好' is 6 bytes
        data = b'6\r\n' + '你好'.encode('utf-8') + b'\r\n0\r\n\r\n'
        result = decode_to_string(data)
        self.assertEqual(result, '你好')
    
    def test_decode_with_metadata(self):
        data = b'5\r\nHello\r\n0\r\n\r\n'
        result = decode_with_metadata(data)
        
        self.assertEqual(result['content'], b'Hello')
        self.assertEqual(result['chunk_count'], 1)
        self.assertEqual(result['total_size'], 5)
    
    def test_decode_with_extensions(self):
        data = b'5;name=test\r\nHello\r\n0\r\n\r\n'
        result = decode_with_metadata(data)
        
        self.assertEqual(result['content'], b'Hello')
        self.assertEqual(result['extensions'], [('name', 'test')])
    
    def test_decode_with_trailers(self):
        data = b'5\r\nHello\r\n0\r\nX-Checksum: abc\r\n\r\n'
        result = decode_with_metadata(data)
        
        self.assertEqual(result['trailers'], {'X-Checksum': 'abc'})
    
    def test_decode_invalid_hex(self):
        data = b'xyz\r\nHello\r\n0\r\n\r\n'
        with self.assertRaises(ChunkedEncodingError):
            decode(data)
    
    def test_decode_missing_crlf(self):
        data = b'5Hello\r\n0\r\n\r\n'
        with self.assertRaises(ChunkedEncodingError):
            decode(data)


class TestChunkedDecoder(unittest.TestCase):
    """Test streaming ChunkedDecoder class."""
    
    def test_feed_complete(self):
        decoder = ChunkedDecoder()
        decoder.feed(b'5\r\nHello\r\n0\r\n\r\n')
        
        self.assertTrue(decoder.is_complete())
        self.assertEqual(decoder.get_data(), b'Hello')
    
    def test_feed_incremental(self):
        decoder = ChunkedDecoder()
        
        decoder.feed(b'5\r\n')
        self.assertFalse(decoder.is_complete())
        
        decoder.feed(b'Hello\r\n')
        self.assertFalse(decoder.is_complete())
        
        decoder.feed(b'0\r\n\r\n')
        self.assertTrue(decoder.is_complete())
        self.assertEqual(decoder.get_data(), b'Hello')
    
    def test_feed_multi_chunk(self):
        decoder = ChunkedDecoder()
        decoder.feed(b'5\r\nHello\r\n6\r\nWorld!\r\n0\r\n\r\n')
        
        self.assertEqual(decoder.get_data(), b'HelloWorld!')
        self.assertEqual(decoder.chunk_count, 2)
    
    def test_feed_with_extensions(self):
        decoder = ChunkedDecoder()
        decoder.feed(b'5;name=test\r\nHello\r\n0\r\n\r\n')
        
        self.assertEqual(decoder.extensions, [('name', 'test')])
    
    def test_feed_with_trailers(self):
        decoder = ChunkedDecoder()
        decoder.feed(b'5\r\nHello\r\n0\r\nX-Checksum: abc\r\n\r\n')
        
        self.assertEqual(decoder.trailers, {'X-Checksum': 'abc'})
    
    def test_reset(self):
        decoder = ChunkedDecoder()
        decoder.feed(b'5\r\nHello\r\n0\r\n\r\n')
        
        decoder.reset()
        
        self.assertFalse(decoder.is_complete())
        self.assertEqual(decoder.get_data(), b'')
        self.assertEqual(decoder.chunk_count, 0)


class TestChunkedEncoder(unittest.TestCase):
    """Test streaming ChunkedEncoder class."""
    
    def test_write_and_finish(self):
        encoder = ChunkedEncoder(chunk_size=10)
        
        encoder.write(b'Hello')
        encoder.write(b'World')
        
        result = encoder.finish()
        
        # Should have single chunk (10 bytes total) since buffer size was 10
        self.assertIn(b'a\r\nHelloWorld\r\n', result)  # 10 in hex = a
        self.assertIn(b'0\r\n\r\n', result)
    
    def test_write_flush_chunks(self):
        encoder = ChunkedEncoder(chunk_size=5)
        
        encoder.write(b'HelloWorld')  # 10 bytes
        
        # Should have flushed first chunk (5 bytes)
        self.assertIn(b'5\r\nHello\r\n', encoder.get_encoded())
    
    def test_write_string(self):
        encoder = ChunkedEncoder()
        encoder.write('Hello')
        result = encoder.finish()
        
        self.assertIn(b'Hello', result)
    
    def test_finish_twice(self):
        encoder = ChunkedEncoder()
        encoder.write(b'data')
        encoder.finish()
        
        with self.assertRaises(ChunkedEncodingError):
            encoder.finish()
    
    def test_write_after_finish(self):
        encoder = ChunkedEncoder()
        encoder.write(b'data')
        encoder.finish()
        
        with self.assertRaises(ChunkedEncodingError):
            encoder.write(b'more')


class TestValidation(unittest.TestCase):
    """Test validation functions."""
    
    def test_validate_valid(self):
        self.assertTrue(validate(b'5\r\nHello\r\n0\r\n\r\n'))
    
    def test_validate_empty(self):
        self.assertTrue(validate(b'0\r\n\r\n'))
    
    def test_validate_invalid(self):
        self.assertFalse(validate(b'invalid'))
    
    def test_validate_invalid_hex(self):
        self.assertFalse(validate(b'xyz\r\nHello\r\n0\r\n\r\n'))
    
    def test_validate_partial_valid(self):
        valid, error = validate_partial(b'5\r\nHello\r\n')
        self.assertTrue(valid)
        self.assertIsNone(error)
    
    def test_validate_partial_invalid(self):
        valid, error = validate_partial(b'xyz\r\nHello')
        self.assertFalse(valid)
        self.assertIsNotNone(error)


class TestAnalysis(unittest.TestCase):
    """Test analysis functions."""
    
    def test_analyze_valid(self):
        data = b'5\r\nHello\r\n6\r\nWorld!\r\n0\r\n\r\n'
        result = analyze(data)
        
        self.assertTrue(result['valid'])
        self.assertTrue(result['complete'])
        self.assertEqual(result['chunk_count'], 2)
        self.assertEqual(result['total_size'], 11)
    
    def test_analyze_invalid(self):
        result = analyze(b'invalid')
        
        self.assertFalse(result['valid'])
        self.assertIn('error', result)
    
    def test_analyze_partial(self):
        data = b'5\r\nHello\r\n'  # Missing final chunk
        result = analyze(data)
        
        # Partial data is not complete, valid indicates format correctness
        self.assertFalse(result['complete'])
        # Check that it processed the chunk correctly
        self.assertEqual(result['chunk_count'], 1)
        self.assertEqual(result['total_size'], 5)
    
    def test_get_chunk_sizes(self):
        data = b'5\r\nHello\r\na\r\nWorld!!!!!\r\n0\r\n\r\n'  # 10 bytes for 'a' (hex)
        sizes = get_chunk_sizes(data)
        
        # Should include 0 for final chunk
        self.assertEqual(sizes[:3], [5, 10, 0])  # a in hex = 10
    
    def test_get_chunk_count(self):
        data = b'5\r\nHello\r\n6\r\nWorld!\r\n0\r\n\r\n'
        count = get_chunk_count(data)
        
        self.assertEqual(count, 2)


class TestUtilities(unittest.TestCase):
    """Test utility functions."""
    
    def test_split_into_chunks(self):
        data = b'HelloWorld'
        chunks = split_into_chunks(data, chunk_size=5)
        
        self.assertEqual(chunks, [b'Hello', b'World'])
    
    def test_split_into_chunks_string(self):
        chunks = split_into_chunks('Hello', chunk_size=5)
        self.assertEqual(chunks, [b'Hello'])
    
    def test_size_to_hex(self):
        self.assertEqual(size_to_hex(255), 'ff')
        self.assertEqual(size_to_hex(16), '10')
        self.assertEqual(size_to_hex(0), '0')
    
    def test_hex_to_size(self):
        self.assertEqual(hex_to_size('ff'), 255)
        self.assertEqual(hex_to_size('10'), 16)
        self.assertEqual(hex_to_size('0'), 0)
    
    def test_hex_to_size_invalid(self):
        with self.assertRaises(ChunkedEncodingError):
            hex_to_size('xyz')
    
    def test_format_chunk_header(self):
        result = format_chunk_header(5)
        self.assertEqual(result, b'5')
    
    def test_format_chunk_header_with_extensions(self):
        result = format_chunk_header(5, [('name', 'test')])
        self.assertEqual(result, b'5;name=test')
    
    def test_parse_chunk_header(self):
        size, exts = parse_chunk_header('5')
        self.assertEqual(size, 5)
        self.assertEqual(exts, [])
    
    def test_parse_chunk_header_with_extensions(self):
        size, exts = parse_chunk_header('5;name=test')
        self.assertEqual(size, 5)
        self.assertEqual(exts, [('name', 'test')])
    
    def test_parse_chunk_header_multiple_extensions(self):
        size, exts = parse_chunk_header('5;a;b=c')
        self.assertEqual(size, 5)
        self.assertEqual(exts, [('a', None), ('b', 'c')])
    
    def test_parse_chunk_header_bytes(self):
        size, exts = parse_chunk_header(b'5')
        self.assertEqual(size, 5)


class TestHTTPIntegration(unittest.TestCase):
    """Test HTTP integration helpers."""
    
    def test_create_chunked_response_body(self):
        result = create_chunked_response_body('Hello')
        self.assertIn(b'5\r\nHello\r\n', result)
        self.assertIn(b'0\r\n\r\n', result)
    
    def test_create_chunked_response_body_with_trailers(self):
        result = create_chunked_response_body('Hello', trailers={'X-Checksum': 'abc'})
        self.assertIn(b'X-Checksum: abc\r\n', result)
    
    def test_parse_chunked_request_body(self):
        body = b'5\r\nHello\r\n0\r\n\r\n'
        result = parse_chunked_request_body(body)
        
        self.assertEqual(result['content'], b'Hello')
        self.assertIn('valid', result)
    
    def test_parse_chunked_request_body_with_trailers(self):
        body = b'5\r\nHello\r\n0\r\nX-Checksum: abc\r\n\r\n'
        result = parse_chunked_request_body(body, expected_trailers=['X-Checksum'])
        
        self.assertEqual(result['trailers'], {'X-Checksum': 'abc'})
    
    def test_parse_chunked_request_body_missing_trailer(self):
        body = b'5\r\nHello\r\n0\r\n\r\n'
        result = parse_chunked_request_body(body, expected_trailers=['X-Checksum'])
        
        self.assertIn('missing_trailers', result)
        self.assertFalse(result['valid'])


class TestRoundtrip(unittest.TestCase):
    """Test encode-decode roundtrip."""
    
    def test_roundtrip_simple(self):
        data = b'Hello World!'
        encoded = encode(data)
        decoded = decode(encoded)
        self.assertEqual(decoded, data)
    
    def test_roundtrip_unicode(self):
        data = '你好世界'
        encoded = encode(data)
        decoded = decode_to_string(encoded)
        self.assertEqual(decoded, data)
    
    def test_roundtrip_large_data(self):
        data = b'x' * 10000
        encoded = encode(data, chunk_size=1000)
        decoded = decode(encoded)
        self.assertEqual(decoded, data)
    
    def test_roundtrip_empty(self):
        data = b''
        encoded = encode(data)
        decoded = decode(encoded)
        self.assertEqual(decoded, data)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases."""
    
    def test_zero_size_chunk(self):
        data = b'0\r\n\r\n'
        decoded = decode(data)
        self.assertEqual(decoded, b'')
    
    def test_large_chunk_size(self):
        # Create chunk with size in hex
        data = b'ff\r\n' + b'x' * 255 + b'\r\n0\r\n\r\n'
        decoded = decode(data)
        self.assertEqual(len(decoded), 255)
    
    def test_very_long_chunk_size(self):
        # Size 1000 in hex is 3e8
        data = b'3e8\r\n' + b'x' * 1000 + b'\r\n0\r\n\r\n'
        decoded = decode(data)
        self.assertEqual(len(decoded), 1000)
    
    def test_chunk_size_boundary(self):
        # Test with chunk size exactly at boundary
        data = b'10\r\n' + b'x' * 16 + b'\r\n0\r\n\r\n'
        decoded = decode(data)
        self.assertEqual(len(decoded), 16)
    
    def test_multiple_extensions(self):
        data = b'5;a=1;b=2;c\r\nHello\r\n0\r\n\r\n'
        result = decode_with_metadata(data)
        self.assertEqual(len(result['extensions']), 3)
    
    def test_multiple_trailers(self):
        data = b'5\r\nHello\r\n0\r\nX-A: 1\r\nX-B: 2\r\n\r\n'
        result = decode_with_metadata(data)
        self.assertEqual(len(result['trailers']), 2)
    
    def test_binary_data(self):
        binary = bytes(range(256))
        encoded = encode(binary)
        decoded = decode(encoded)
        self.assertEqual(decoded, binary)


if __name__ == '__main__':
    unittest.main(verbosity=2)
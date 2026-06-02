#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Adler-32 Checksum Utilities Tests

Tests for the adler32_utils module.
"""

import pytest
import os
import tempfile
from mod import (
    adler32,
    adler32_detailed,
    adler32_hex,
    adler32_to_hex,
    hex_to_adler32,
    decompose_adler32,
    compose_adler32,
    compare_adler32,
    verify_adler32,
    adler32_statistics,
    Adler32Streaming,
    adler32_file,
    adler32_file_hex,
    verify_file_adler32,
    compute_combined_checksum,
    verify_combined_checksum,
    test_adler32,
    Adler32Result,
    ADLER32_MOD,
)


class TestAdler32Core:
    """Tests for core Adler-32 functions."""

    def test_empty_bytes(self):
        """Test Adler-32 of empty bytes."""
        assert adler32(b'') == 1

    def test_single_byte(self):
        """Test Adler-32 of single byte 'a'."""
        assert adler32(b'a') == 6422626

    def test_string_hello(self):
        """Test Adler-32 of 'Hello'."""
        assert adler32(b'Hello') == 93061621

    def test_string_abc(self):
        """Test Adler-32 of 'abc'."""
        assert adler32(b'abc') == 38600999

    def test_string_wikipedia(self):
        """Test Adler-32 of 'Wikipedia'."""
        assert adler32(b'Wikipedia') == 300286872

    def test_pangram(self):
        """Test Adler-32 of the quick brown fox pangram."""
        data = b'The quick brown fox jumps over the lazy dog'
        assert adler32(data) == 1541148634

    def test_string_input(self):
        """Test Adler-32 with string input (auto-converted to bytes)."""
        assert adler32('Hello') == adler32(b'Hello')

    def test_bytearray_input(self):
        """Test Adler-32 with bytearray input."""
        assert adler32(bytearray(b'Hello')) == adler32(b'Hello')


class TestAdler32Hex:
    """Tests for hex conversion functions."""

    def test_hello_hex(self):
        """Test hex output for 'Hello'."""
        assert adler32_hex(b'Hello') == '058c01f5'

    def test_empty_hex(self):
        """Test hex output for empty bytes."""
        assert adler32_hex(b'') == '00000001'

    def test_integer_to_hex(self):
        """Test converting integer to hex."""
        assert adler32_to_hex(93061621) == '058c01f5'

    def test_hex_to_integer(self):
        """Test converting hex string to integer."""
        assert hex_to_adler32('058c01f5') == 93061621

    def test_hex_to_integer_invalid(self):
        """Test invalid hex string raises ValueError."""
        with pytest.raises(ValueError):
            hex_to_adler32('invalid')


class TestAdler32Detailed:
    """Tests for detailed result."""

    def test_detailed_result(self):
        """Test detailed result structure."""
        result = adler32_detailed(b'Hello')
        assert isinstance(result, Adler32Result)
        assert result.value == 93061621
        assert result.hex == '058c01f5'
        # A = lower 16 bits, B = upper 16 bits
        assert result.a == 501
        assert result.b == 1420

    def test_detailed_string_input(self):
        """Test detailed result with string input."""
        result = adler32_detailed('Hello')
        assert result.value == 93061621


class TestAdler32Components:
    """Tests for A/B component functions."""

    def test_decompose(self):
        """Test decomposing Adler-32 into A and B."""
        a, b = decompose_adler32(93061621)
        assert a == 501
        assert b == 1420

    def test_compose(self):
        """Test composing Adler-32 from A and B."""
        value = compose_adler32(501, 1420)
        assert value == 93061621

    def test_decompose_compose_roundtrip(self):
        """Test that decompose and compose are inverse operations."""
        original = 93061621
        a, b = decompose_adler32(original)
        recomposed = compose_adler32(a, b)
        assert recomposed == original


class TestCompareAdler32:
    """Tests for comparison functions."""

    def test_identical_data(self):
        """Test comparing identical data."""
        assert compare_adler32(b'Hello', b'Hello') is True

    def test_different_data(self):
        """Test comparing different data."""
        assert compare_adler32(b'Hello', b'World') is False

    def test_empty_vs_nonempty(self):
        """Test comparing empty and non-empty data."""
        assert compare_adler32(b'', b'Hello') is False


class TestVerifyAdler32:
    """Tests for verification functions."""

    def test_verify_integer(self):
        """Test verifying with integer checksum."""
        assert verify_adler32(b'Hello', 93061621) is True

    def test_verify_hex_string(self):
        """Test verifying with hex string checksum."""
        assert verify_adler32(b'Hello', '058c01f5') is True

    def test_verify_mismatch(self):
        """Test verification fails for mismatch."""
        assert verify_adler32(b'Hello', 12345) is False

    def test_verify_invalid_hex(self):
        """Test verification fails for invalid hex string."""
        assert verify_adler32(b'Hello', 'invalid') is False


class TestAdler32Statistics:
    """Tests for statistics function."""

    def test_statistics_structure(self):
        """Test statistics dictionary structure."""
        stats = adler32_statistics(b'Hello')
        assert 'checksum' in stats
        assert 'checksum_hex' in stats
        assert 'a_value' in stats
        assert 'b_value' in stats
        assert 'byte_count' in stats
        assert 'byte_sum' in stats
        assert 'byte_average' in stats

    def test_statistics_hello(self):
        """Test statistics for 'Hello'."""
        stats = adler32_statistics(b'Hello')
        assert stats['checksum'] == 93061621
        assert stats['byte_count'] == 5


class TestAdler32Streaming:
    """Tests for streaming computation."""

    def test_streaming_basic(self):
        """Test basic streaming operation."""
        stream = Adler32Streaming()
        stream.update(b'Hello')
        assert stream.value == adler32(b'Hello')

    def test_streaming_incremental(self):
        """Test incremental streaming updates."""
        stream = Adler32Streaming()
        stream.update(b'Hello')
        stream.update(b' World')
        assert stream.value == adler32(b'Hello World')

    def test_streaming_hex(self):
        """Test streaming hex property."""
        stream = Adler32Streaming()
        stream.update(b'Hello')
        assert stream.hex == adler32_hex(b'Hello')

    def test_streaming_byte_count(self):
        """Test streaming byte count."""
        stream = Adler32Streaming()
        stream.update(b'Hello')
        stream.update(b' World')
        assert stream.byte_count == 11

    def test_streaming_reset(self):
        """Test streaming reset."""
        stream = Adler32Streaming()
        stream.update(b'Hello')
        stream.reset()
        assert stream.value == 1  # Back to initial value

    def test_streaming_get_result(self):
        """Test get_result method."""
        stream = Adler32Streaming()
        stream.update(b'Hello')
        result = stream.get_result()
        assert isinstance(result, Adler32Result)
        assert result.value == adler32(b'Hello')

    def test_streaming_string_input(self):
        """Test streaming with string input."""
        stream = Adler32Streaming()
        stream.update('Hello')
        assert stream.value == adler32(b'Hello')

    def test_streaming_update_returns_value(self):
        """Test that update returns current checksum value."""
        stream = Adler32Streaming()
        result = stream.update(b'Hello')
        assert result == adler32(b'Hello')


class TestAdler32File:
    """Tests for file operations."""

    def test_file_checksum(self, tmp_path):
        """Test file checksum computation."""
        test_file = tmp_path / "test.txt"
        test_file.write_bytes(b'Hello World')
        result = adler32_file(str(test_file))
        assert isinstance(result, Adler32Result)
        assert result.value == adler32(b'Hello World')

    def test_file_checksum_hex(self, tmp_path):
        """Test file checksum as hex."""
        test_file = tmp_path / "test.txt"
        test_file.write_bytes(b'Hello')
        hex_result = adler32_file_hex(str(test_file))
        assert hex_result == adler32_hex(b'Hello')

    def test_verify_file_adler32(self, tmp_path):
        """Test file verification."""
        test_file = tmp_path / "test.txt"
        test_file.write_bytes(b'Hello')
        assert verify_file_adler32(str(test_file), adler32(b'Hello')) is True
        assert verify_file_adler32(str(test_file), adler32_hex(b'Hello')) is True

    def test_verify_file_adler32_mismatch(self, tmp_path):
        """Test file verification with mismatch."""
        test_file = tmp_path / "test.txt"
        test_file.write_bytes(b'Hello')
        assert verify_file_adler32(str(test_file), 12345) is False

    def test_file_not_found(self):
        """Test that non-existent file raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            adler32_file('/nonexistent/path/file.txt')


class TestCombinedChecksum:
    """Tests for combined Adler-32 + CRC-32 functions."""

    def test_compute_combined(self):
        """Test computing combined checksums."""
        adler, crc = compute_combined_checksum(b'Hello')
        assert isinstance(adler, str)
        assert isinstance(crc, str)
        assert len(adler) == 8
        assert len(crc) == 8

    def test_verify_combined(self):
        """Test verifying combined checksums."""
        adler, crc = compute_combined_checksum(b'Hello')
        adler_valid, crc_valid = verify_combined_checksum(b'Hello', adler, crc)
        assert adler_valid is True
        assert crc_valid is True

    def test_verify_combined_mismatch(self):
        """Test combined verification with mismatch."""
        adler_valid, crc_valid = verify_combined_checksum(
            b'Hello', '00000000', '00000000'
        )
        assert adler_valid is False
        assert crc_valid is False


class TestAdler32SelfTest:
    """Tests for built-in self-test function."""

    def test_self_test_passes(self):
        """Test that self-test passes with known values."""
        assert test_adler32() is True


class TestAdler32Initial:
    """Tests for initial value parameter."""

    def test_non_default_initial(self):
        """Test with non-default initial value."""
        result1 = adler32(b'Hello', initial=1)
        result2 = adler32(b'Hello', initial=42)
        assert result1 != result2

    def test_streaming_with_initial(self):
        """Test streaming with custom initial value."""
        stream = Adler32Streaming(initial=1000)
        stream.update(b'Hello')
        expected = adler32(b'Hello', initial=1000)
        assert stream.value == expected


class TestAdler32Constants:
    """Tests for module constants."""

    def test_adler32_mod_is_prime(self):
        """Test that ADLER32_MOD is the expected prime value."""
        assert ADLER32_MOD == 65521


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

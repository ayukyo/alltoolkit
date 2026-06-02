#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - WebSocket Utilities Tests

Tests for the websocket_utils module.
"""

import pytest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from websocket_utils import (
    WebSocketUtils,
    WebSocketFrame,
    Opcode,
    CloseCode,
    compute_accept_key,
    generate_key,
    encode_frame,
    decode_frame,
    encode_text,
    encode_binary,
    encode_ping,
    encode_pong,
    encode_close,
    compute_accept_key,
    generate_key,
)


class TestWebSocketGUID:
    """Tests for WebSocket GUID constant."""

    def test_guid_value(self):
        """Test that WebSocket GUID is correct."""
        assert WebSocketUtils.WEBSOCKET_GUID == "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"


class TestComputeAcceptKey:
    """Tests for accept key computation."""

    def test_compute_accept_key(self):
        """Test computing accept key."""
        key = "dGhlIHNhbXBsZSBub25jZQ=="
        accept = compute_accept_key(key)
        assert accept == "s3pPLMBiTxaQ9kYGzzhZRbK+xOo="

    def test_generate_key(self):
        """Test generating a valid WebSocket key."""
        key = generate_key()
        assert isinstance(key, str)
        assert len(key) > 0
        # Should be valid base64
        import base64
        decoded = base64.b64decode(key)
        assert len(decoded) == 16


class TestOpcode:
    """Tests for Opcode enum."""

    def test_opcode_values(self):
        """Test Opcode enum values."""
        assert Opcode.CONTINUATION == 0x0
        assert Opcode.TEXT == 0x1
        assert Opcode.BINARY == 0x2
        assert Opcode.CLOSE == 0x8
        assert Opcode.PING == 0x9
        assert Opcode.PONG == 0xA

    def test_opcode_names(self):
        """Test Opcode enum names."""
        assert Opcode.TEXT.name == "TEXT"
        assert Opcode.CLOSE.name == "CLOSE"


class TestCloseCode:
    """Tests for CloseCode enum."""

    def test_close_code_normal(self):
        """Test normal close code."""
        assert CloseCode.NORMAL == 1000

    def test_close_code_values(self):
        """Test CloseCode enum values."""
        assert CloseCode.GOING_AWAY == 1001
        assert CloseCode.PROTOCOL_ERROR == 1002
        assert CloseCode.POLICY_VIOLATION == 1008
        assert CloseCode.MESSAGE_TOO_BIG == 1009


class TestWebSocketFrame:
    """Tests for WebSocketFrame class."""

    def test_frame_creation(self):
        """Test creating a WebSocket frame."""
        frame = WebSocketFrame()
        assert frame.fin is True
        assert frame.opcode == Opcode.TEXT
        assert frame.masked is False

    def test_frame_repr(self):
        """Test WebSocket frame string representation."""
        frame = WebSocketFrame(opcode=Opcode.TEXT, payload=b'Hello')
        repr_str = repr(frame)
        assert 'TEXT' in repr_str
        assert 'Hello' in repr_str or 'payload_len' in repr_str


class TestEncodeFrame:
    """Tests for frame encoding."""

    def test_encode_text_frame(self):
        """Test encoding a text frame."""
        data = encode_text("Hello")
        assert isinstance(data, bytes)
        assert len(data) > 0

    def test_encode_binary_frame(self):
        """Test encoding a binary frame."""
        data = encode_binary(b'\x00\x01\x02')
        assert isinstance(data, bytes)
        assert len(data) > 0

    def test_encode_ping_frame(self):
        """Test encoding a ping frame."""
        data = encode_ping(b'test')
        assert isinstance(data, bytes)
        assert len(data) > 0

    def test_encode_pong_frame(self):
        """Test encoding a pong frame."""
        data = encode_pong(b'test')
        assert isinstance(data, bytes)
        assert len(data) > 0

    def test_encode_close_frame(self):
        """Test encoding a close frame."""
        data = encode_close(CloseCode.NORMAL, "Goodbye")
        assert isinstance(data, bytes)
        assert len(data) > 0

    def test_encode_with_mask(self):
        """Test encoding with masking."""
        data = encode_text("Hello", mask=True)
        assert isinstance(data, bytes)
        # Masked frames have bit 7 set in second byte
        assert data[1] & 0x80 != 0

    def test_encode_empty_text(self):
        """Test encoding empty text."""
        data = encode_text("")
        assert isinstance(data, bytes)

    def test_encode_large_payload(self):
        """Test encoding large payload."""
        large_data = "A" * 100000
        data = encode_text(large_data)
        assert len(data) > 100000


class TestDecodeFrame:
    """Tests for frame decoding."""

    def test_decode_text_frame(self):
        """Test decoding a text frame."""
        encoded = encode_text("Hello")
        frame, consumed = decode_frame(encoded)
        assert frame.opcode == Opcode.TEXT
        assert frame.payload == b'Hello'

    def test_decode_binary_frame(self):
        """Test decoding a binary frame."""
        encoded = encode_binary(b'\x00\x01\x02')
        frame, consumed = decode_frame(encoded)
        assert frame.opcode == Opcode.BINARY
        assert frame.payload == b'\x00\x01\x02'

    def test_decode_masked_frame(self):
        """Test decoding a masked frame."""
        encoded = encode_text("Hello", mask=True)
        frame, consumed = decode_frame(encoded)
        # Payload should be unmasked after decoding
        assert frame.payload == b'Hello'
        assert frame.masked is True

    def test_decode_ping_pong(self):
        """Test decoding ping/pong frames."""
        ping_data = encode_ping(b"test")
        ping_frame, _ = decode_frame(ping_data)
        assert ping_frame.opcode == Opcode.PING
        assert ping_frame.payload == b"test"

    def test_decode_close_frame(self):
        """Test decoding close frame."""
        close_data = encode_close(CloseCode.NORMAL, "Goodbye")
        close_frame, _ = decode_frame(close_data)
        assert close_frame.opcode == Opcode.CLOSE
        # Check that close code and reason are extracted
        code, reason = WebSocketUtils.parse_close_payload(close_frame.payload)
        assert code == CloseCode.NORMAL
        assert reason == "Goodbye"

    def test_decode_incomplete_frame(self):
        """Test that incomplete frame raises error."""
        with pytest.raises(ValueError):
            decode_frame(b'\x81')  # Incomplete frame


class TestEncodeDecodeRoundtrip:
    """Tests for encode/decode roundtrip."""

    def test_text_roundtrip(self):
        """Test encoding and decoding text."""
        original = "Hello, WebSocket!"
        encoded = encode_text(original)
        frame, _ = decode_frame(encoded)
        assert frame.payload.decode('utf-8') == original

    def test_binary_roundtrip(self):
        """Test encoding and decoding binary."""
        original = b'\x00\x01\x02\x03\x04'
        encoded = encode_binary(original)
        frame, _ = decode_frame(encoded)
        assert frame.payload == original

    def test_unicode_roundtrip(self):
        """Test encoding and decoding unicode text."""
        original = "你好，WebSocket！世界"
        encoded = encode_text(original)
        frame, _ = decode_frame(encoded)
        assert frame.payload.decode('utf-8') == original

    def test_large_payload_roundtrip(self):
        """Test encoding and decoding large payload."""
        original = "A" * 50000
        encoded = encode_text(original)
        frame, _ = decode_frame(encoded)
        assert frame.payload.decode('utf-8') == original


class TestParseClosePayload:
    """Tests for close payload parsing."""

    def test_parse_normal_close(self):
        """Test parsing normal close payload."""
        payload = b'\x03\xe8' + b'Normal closure'
        code, reason = WebSocketUtils.parse_close_payload(payload)
        assert code == CloseCode.NORMAL
        assert reason == 'Normal closure'

    def test_parse_close_no_reason(self):
        """Test parsing close payload without reason."""
        payload = b'\x03\xe8'
        code, reason = WebSocketUtils.parse_close_payload(payload)
        assert code == CloseCode.NORMAL
        assert reason == ''

    def test_parse_close_empty_payload(self):
        """Test parsing empty close payload."""
        code, reason = WebSocketUtils.parse_close_payload(b'')
        assert code == CloseCode.NO_STATUS


class TestIsControlFrame:
    """Tests for control frame detection."""

    def test_ping_is_control(self):
        """Test that Ping is a control frame."""
        assert WebSocketUtils.is_control_frame(Opcode.PING) is True

    def test_pong_is_control(self):
        """Test that Pong is a control frame."""
        assert WebSocketUtils.is_control_frame(Opcode.PONG) is True

    def test_close_is_control(self):
        """Test that Close is a control frame."""
        assert WebSocketUtils.is_control_frame(Opcode.CLOSE) is True

    def test_text_not_control(self):
        """Test that Text is not a control frame."""
        assert WebSocketUtils.is_control_frame(Opcode.TEXT) is False


class TestValidateUTF8:
    """Tests for UTF-8 validation."""

    def test_valid_utf8(self):
        """Test validating valid UTF-8."""
        assert WebSocketUtils.validate_utf8(b'Hello') is True
        assert WebSocketUtils.validate_utf8('你好'.encode('utf-8')) is True

    def test_invalid_utf8(self):
        """Test validating invalid UTF-8."""
        # Invalid UTF-8 sequence
        assert WebSocketUtils.validate_utf8(b'\xff\xfe') is False


class TestFragmentation:
    """Tests for message fragmentation."""

    def test_fragmentation_small_data(self):
        """Test that small data doesn't fragment."""
        data = "Hello"
        fragments = WebSocketUtils.fragmentation_encode(data, max_frame_size=65536)
        assert len(fragments) == 1

    def test_fragmentation_large_data(self):
        """Test fragmenting large data."""
        large_data = "A" * 100000
        fragments = WebSocketUtils.fragmentation_encode(large_data, max_frame_size=50000)
        assert len(fragments) > 1

    def test_fragmentation_first_frame_opcode(self):
        """Test that first fragment has message opcode."""
        large_data = "A" * 100000
        fragments = WebSocketUtils.fragmentation_encode(large_data, max_frame_size=50000)
        first_frame, _ = decode_frame(fragments[0])
        assert first_frame.opcode == Opcode.TEXT

    def test_fragmentation_continuation_opcode(self):
        """Test that continuation frames have Continuation opcode."""
        large_data = "A" * 100000
        fragments = WebSocketUtils.fragmentation_encode(large_data, max_frame_size=50000)
        if len(fragments) > 1:
            second_frame, _ = decode_frame(fragments[1])
            assert second_frame.opcode == Opcode.CONTINUATION

    def test_fragmentation_last_frame_fin(self):
        """Test that last fragment has FIN bit set."""
        large_data = "A" * 100000
        fragments = WebSocketUtils.fragmentation_encode(large_data, max_frame_size=50000)
        last_frame, _ = decode_frame(fragments[-1])
        assert last_frame.fin is True

    def test_fragmentation_roundtrip(self):
        """Test that fragmented messages can be reassembled."""
        original = "A" * 100000
        fragments = WebSocketUtils.fragmentation_encode(original, max_frame_size=50000)
        
        reassembled = b''
        for fragment in fragments:
            frame, _ = decode_frame(fragment)
            reassembled += frame.payload
        
        assert reassembled.decode('utf-8') == original


class TestEncodeFrameDetails:
    """Tests for specific frame encoding details."""

    def test_frame_first_byte(self):
        """Test first byte of encoded frame."""
        data = encode_text("A")
        first_byte = data[0]
        # FIN bit (bit 7) should be set
        assert first_byte & 0x80 != 0
        # Opcode should be TEXT (0x1)
        assert (first_byte & 0x0F) == Opcode.TEXT

    def test_frame_payload_length_125(self):
        """Test small payload encoding."""
        data = encode_text("Hello")  # 5 bytes
        second_byte = data[1]
        # MASK bit should be 0
        assert second_byte & 0x80 == 0
        # Length should be 5
        assert (second_byte & 0x7F) == 5

    def test_frame_payload_length_126(self):
        """Test medium payload encoding (126-65535)."""
        data = encode_text("A" * 200)
        second_byte = data[1]
        # Length indicator should be 126
        assert (second_byte & 0x7F) == 126
        # Extended length should be 200
        import struct
        extended_len = struct.unpack('!H', data[2:4])[0]
        assert extended_len == 200

    def test_frame_payload_length_127(self):
        """Test large payload encoding (>65535)."""
        data = encode_text("A" * 70000)
        second_byte = data[1]
        # Length indicator should be 127
        assert (second_byte & 0x7F) == 127
        # Extended length should be 70000
        import struct
        extended_len = struct.unpack('!Q', data[2:10])[0]
        assert extended_len == 70000


class TestEdgeCases:
    """Tests for edge cases."""

    def test_encode_none_opcode(self):
        """Test encoding with specific opcode."""
        data = encode_frame(b'test', opcode=Opcode.TEXT)
        assert len(data) > 0

    def test_decode_empty_data(self):
        """Test decoding empty data raises error."""
        with pytest.raises(ValueError):
            decode_frame(b'')

    def test_close_code_invalid(self):
        """Test close frame with custom close code."""
        data = encode_close(9999, "Custom close")
        frame, _ = decode_frame(data)
        code, reason = WebSocketUtils.parse_close_payload(frame.payload)
        assert code == 9999

    def test_generate_multiple_keys(self):
        """Test generating multiple keys."""
        keys = [generate_key() for _ in range(10)]
        # All keys should be unique
        assert len(set(keys)) == 10


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

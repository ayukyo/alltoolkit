"""
WebSocket Utilities 测试套件

测试所有 WebSocket 工具函数。
"""

import unittest
import struct
import base64
import hashlib
import sys
import os

# Add module directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    WebSocketUtils, WebSocketFrame, Opcode, CloseCode,
    compute_accept_key, generate_key, encode_frame, decode_frame,
    encode_text, encode_binary, encode_ping, encode_pong, encode_close
)


class TestHandshake(unittest.TestCase):
    """测试握手相关功能"""
    
    def test_generate_key(self):
        """测试生成 Sec-WebSocket-Key"""
        key1 = generate_key()
        key2 = generate_key()
        
        # 每次生成不同的 key
        self.assertNotEqual(key1, key2)
        
        # key 是 Base64 编码的 16 字节
        decoded = base64.b64decode(key1)
        self.assertEqual(len(decoded), 16)
    
    def test_compute_accept_key(self):
        """测试计算 Sec-WebSocket-Accept"""
        # RFC 6455 示例
        client_key = "dGhlIHNhbXBsZSBub25jZQ=="
        expected_accept = "s3pPLMBiTxaQ9kYGzzhZRbK+xOo="
        
        computed_accept = compute_accept_key(client_key)
        self.assertEqual(computed_accept, expected_accept)
    
    def test_compute_accept_key_consistency(self):
        """测试 Accept Key 计算一致性"""
        key = generate_key()
        accept1 = compute_accept_key(key)
        accept2 = compute_accept_key(key)
        self.assertEqual(accept1, accept2)
    
    def test_accept_key_verification(self):
        """测试 Accept Key 验证逻辑"""
        client_key = generate_key()
        accept_key = compute_accept_key(client_key)
        
        # 验证 Accept Key 格式
        self.assertIsInstance(accept_key, str)
        self.assertTrue(len(accept_key) > 0)
        
        # 验证计算过程
        expected = base64.b64encode(
            hashlib.sha1((client_key + WebSocketUtils.WEBSOCKET_GUID).encode()).digest()
        ).decode()
        self.assertEqual(accept_key, expected)


class TestFrameEncoding(unittest.TestCase):
    """测试帧编码"""
    
    def test_encode_text_simple(self):
        """测试简单文本帧编码"""
        frame = encode_text("Hello")
        
        # 检查基本结构
        self.assertTrue(len(frame) > 5)  # 头部 + 数据
        
        # 第一个字节: FIN=1, Opcode=1 (TEXT)
        self.assertEqual(frame[0], 0x81)
        
        # 第二个字节: MASK=0, 长度=5
        self.assertEqual(frame[1], 5)
    
    def test_encode_text_with_mask(self):
        """测试带掩码的文本帧编码"""
        frame = encode_text("Hello", mask=True)
        
        # 第二个字节最高位应为 1 (masked)
        self.assertTrue(frame[1] & 0x80)
        
        # 解码验证
        decoded_frame, consumed = decode_frame(frame)
        self.assertEqual(decoded_frame.payload.decode('utf-8'), "Hello")
        self.assertTrue(decoded_frame.masked)
    
    def test_encode_binary(self):
        """测试二进制帧编码"""
        data = b'\x00\x01\x02\x03\x04'
        frame = encode_binary(data)
        
        # Opcode 应为 2 (BINARY)
        self.assertEqual(frame[0] & 0x0F, Opcode.BINARY)
        
        # 解码验证
        decoded_frame, _ = decode_frame(frame)
        self.assertEqual(decoded_frame.payload, data)
    
    def test_encode_extended_length_16bit(self):
        """测试 16 位扩展长度编码"""
        # 126 字节，触发 16 位扩展长度
        data = "A" * 126
        frame = encode_text(data)
        
        # 第二个字节应为 126
        self.assertEqual(frame[1], 126)
        
        # 接下来两个字节应为实际长度
        length = struct.unpack('!H', frame[2:4])[0]
        self.assertEqual(length, 126)
        
        # 解码验证
        decoded_frame, _ = decode_frame(frame)
        self.assertEqual(decoded_frame.payload.decode('utf-8'), data)
    
    def test_encode_extended_length_64bit(self):
        """测试 64 位扩展长度编码"""
        # 65536 字节，触发 64 位扩展长度
        data = "B" * 65536
        frame = encode_text(data)
        
        # 第二个字节应为 127
        self.assertEqual(frame[1], 127)
        
        # 接下来 8 个字节应为实际长度
        length = struct.unpack('!Q', frame[2:10])[0]
        self.assertEqual(length, 65536)
        
        # 解码验证
        decoded_frame, _ = decode_frame(frame)
        self.assertEqual(len(decoded_frame.payload), 65536)
    
    def test_encode_empty_payload(self):
        """测试空载荷编码"""
        frame = encode_text("")
        self.assertEqual(frame[1], 0)
        
        decoded_frame, _ = decode_frame(frame)
        self.assertEqual(decoded_frame.payload, b'')
    
    def test_encode_unicode(self):
        """测试 Unicode 文本编码"""
        text = "你好世界 🌍🎉"
        frame = encode_text(text)
        
        decoded_frame, _ = decode_frame(frame)
        self.assertEqual(decoded_frame.payload.decode('utf-8'), text)


class TestFrameDecoding(unittest.TestCase):
    """测试帧解码"""
    
    def test_decode_text_frame(self):
        """测试文本帧解码"""
        frame = encode_text("Test Message")
        decoded, consumed = decode_frame(frame)
        
        self.assertTrue(decoded.fin)
        self.assertEqual(decoded.opcode, Opcode.TEXT)
        self.assertFalse(decoded.masked)
        self.assertEqual(decoded.payload.decode('utf-8'), "Test Message")
    
    def test_decode_binary_frame(self):
        """测试二进制帧解码"""
        data = bytes(range(256))
        frame = encode_binary(data)
        decoded, _ = decode_frame(frame)
        
        self.assertEqual(decoded.opcode, Opcode.BINARY)
        self.assertEqual(decoded.payload, data)
    
    def test_decode_masked_frame(self):
        """测试掩码帧解码"""
        original = "Masked Data"
        frame = encode_text(original, mask=True)
        decoded, _ = decode_frame(frame)
        
        self.assertTrue(decoded.masked)
        self.assertEqual(decoded.payload.decode('utf-8'), original)
    
    def test_decode_partial_frame(self):
        """测试部分帧解码"""
        frame = encode_text("Hello")
        
        # 截断帧数据
        with self.assertRaises(ValueError):
            decode_frame(frame[:1])
        
        with self.assertRaises(ValueError):
            decode_frame(frame[:3])
    
    def test_decode_consumed_bytes(self):
        """测试已解码字节数"""
        messages = ["", "A", "Hello", "A" * 125, "A" * 126, "A" * 65536]
        
        for msg in messages:
            frame = encode_text(msg)
            _, consumed = decode_frame(frame)
            self.assertEqual(consumed, len(frame))


class TestControlFrames(unittest.TestCase):
    """测试控制帧"""
    
    def test_ping_frame(self):
        """测试 Ping 帧"""
        frame = encode_ping(b"ping data")
        
        # Opcode 应为 0x9 (PING)
        self.assertEqual(frame[0] & 0x0F, Opcode.PING)
        
        decoded, _ = decode_frame(frame)
        self.assertEqual(decoded.opcode, Opcode.PING)
        self.assertEqual(decoded.payload, b"ping data")
    
    def test_pong_frame(self):
        """测试 Pong 帧"""
        frame = encode_pong(b"pong data")
        
        # Opcode 应为 0xA (PONG)
        self.assertEqual(frame[0] & 0x0F, Opcode.PONG)
        
        decoded, _ = decode_frame(frame)
        self.assertEqual(decoded.opcode, Opcode.PONG)
        self.assertEqual(decoded.payload, b"pong data")
    
    def test_close_frame(self):
        """测试关闭帧"""
        frame = encode_close(CloseCode.NORMAL, "Goodbye")
        
        # Opcode 应为 0x8 (CLOSE)
        self.assertEqual(frame[0] & 0x0F, Opcode.CLOSE)
        
        decoded, _ = decode_frame(frame)
        self.assertEqual(decoded.opcode, Opcode.CLOSE)
        
        # 解析关闭载荷
        code, reason = WebSocketUtils.parse_close_payload(decoded.payload)
        self.assertEqual(code, CloseCode.NORMAL)
        self.assertEqual(reason, "Goodbye")
    
    def test_close_frame_no_reason(self):
        """测试无原因的关闭帧"""
        frame = encode_close(CloseCode.GOING_AWAY)
        
        decoded, _ = decode_frame(frame)
        code, reason = WebSocketUtils.parse_close_payload(decoded.payload)
        
        self.assertEqual(code, CloseCode.GOING_AWAY)
        self.assertEqual(reason, "")
    
    def test_control_frame_is_control(self):
        """测试控制帧判断"""
        self.assertTrue(WebSocketUtils.is_control_frame(Opcode.CLOSE))
        self.assertTrue(WebSocketUtils.is_control_frame(Opcode.PING))
        self.assertTrue(WebSocketUtils.is_control_frame(Opcode.PONG))
        self.assertFalse(WebSocketUtils.is_control_frame(Opcode.TEXT))
        self.assertFalse(WebSocketUtils.is_control_frame(Opcode.BINARY))
        self.assertFalse(WebSocketUtils.is_control_frame(Opcode.CONTINUATION))


class TestFragmentation(unittest.TestCase):
    """测试分片功能"""
    
    def test_small_message_no_fragmentation(self):
        """测试小消息不分片"""
        data = "Small message"
        frames = WebSocketUtils.fragmentation_encode(data, max_frame_size=100)
        
        self.assertEqual(len(frames), 1)
        
        # 验证解码
        decoded, _ = decode_frame(frames[0])
        self.assertTrue(decoded.fin)
        self.assertEqual(decoded.opcode, Opcode.TEXT)
    
    def test_large_message_fragmentation(self):
        """测试大消息分片"""
        data = "X" * 1000
        frames = WebSocketUtils.fragmentation_encode(data, max_frame_size=300)
        
        # 应分为 4 片
        self.assertEqual(len(frames), 4)
        
        # 验证每片
        for i, frame in enumerate(frames):
            decoded, _ = decode_frame(frame)
            
            if i == 0:
                # 第一片: opcode = TEXT, fin = False
                self.assertEqual(decoded.opcode, Opcode.TEXT)
                self.assertFalse(decoded.fin)
            elif i < len(frames) - 1:
                # 中间片: opcode = CONTINUATION, fin = False
                self.assertEqual(decoded.opcode, Opcode.CONTINUATION)
                self.assertFalse(decoded.fin)
            else:
                # 最后一片: opcode = CONTINUATION, fin = True
                self.assertEqual(decoded.opcode, Opcode.CONTINUATION)
                self.assertTrue(decoded.fin)
    
    def test_fragmentation_preserves_data(self):
        """测试分片保留数据完整性"""
        data = "A" * 50000
        frames = WebSocketUtils.fragmentation_encode(data, max_frame_size=10000)
        
        # 重组数据
        reconstructed = b""
        for frame in frames:
            decoded, _ = decode_frame(frame)
            reconstructed += decoded.payload
        
        self.assertEqual(reconstructed.decode('utf-8'), data)
    
    def test_binary_fragmentation(self):
        """测试二进制数据分片"""
        data = bytes(range(256)) * 100
        frames = WebSocketUtils.fragmentation_encode(
            data, max_frame_size=10000, opcode=Opcode.BINARY
        )
        
        self.assertTrue(len(frames) > 1)
        
        # 第一片应为 BINARY opcode
        first_decoded, _ = decode_frame(frames[0])
        self.assertEqual(first_decoded.opcode, Opcode.BINARY)


class TestUTF8Validation(unittest.TestCase):
    """测试 UTF-8 验证"""
    
    def test_valid_utf8(self):
        """测试有效的 UTF-8"""
        valid_strings = [
            "Hello",
            "你好世界",
            "🌍🎉🚀",
            "日本語テスト",
            "Mix of ASCII and Unicode: éèêë"
        ]
        
        for s in valid_strings:
            self.assertTrue(WebSocketUtils.validate_utf8(s.encode('utf-8')))
    
    def test_invalid_utf8(self):
        """测试无效的 UTF-8"""
        invalid_bytes = [
            b'\xff\xfe',  # 无效的 UTF-8 序列
            b'\x80\x81',  # 无效的延续字节
            b'\xc0\x80',  # 过长编码
            b'\xed\xa0\x80',  # 代理对
        ]
        
        for b in invalid_bytes:
            self.assertFalse(WebSocketUtils.validate_utf8(b))


class TestWebSocketFrame(unittest.TestCase):
    """测试 WebSocketFrame 类"""
    
    def test_frame_repr(self):
        """测试帧的字符串表示"""
        frame = WebSocketFrame(
            fin=True,
            opcode=Opcode.TEXT,
            masked=False,
            payload=b"test"
        )
        
        repr_str = repr(frame)
        self.assertIn("fin=True", repr_str)
        self.assertIn("TEXT", repr_str)
        self.assertIn("payload_len=4", repr_str)
    
    def test_frame_defaults(self):
        """测试帧的默认值"""
        frame = WebSocketFrame()
        
        self.assertTrue(frame.fin)
        self.assertFalse(frame.rsv1)
        self.assertFalse(frame.rsv2)
        self.assertFalse(frame.rsv3)
        self.assertEqual(frame.opcode, Opcode.TEXT)
        self.assertFalse(frame.masked)
        self.assertEqual(frame.payload, b'')


class TestCloseCodes(unittest.TestCase):
    """测试关闭状态码"""
    
    def test_close_code_values(self):
        """测试关闭状态码值"""
        self.assertEqual(CloseCode.NORMAL, 1000)
        self.assertEqual(CloseCode.GOING_AWAY, 1001)
        self.assertEqual(CloseCode.PROTOCOL_ERROR, 1002)
        self.assertEqual(CloseCode.UNSUPPORTED_DATA, 1003)
        self.assertEqual(CloseCode.MESSAGE_TOO_BIG, 1009)
    
    def test_parse_close_payload_empty(self):
        """测试解析空关闭载荷"""
        code, reason = WebSocketUtils.parse_close_payload(b'')
        self.assertEqual(code, CloseCode.NO_STATUS)
        self.assertEqual(reason, "")
    
    def test_parse_close_payload_short(self):
        """测试解析过短的关闭载荷"""
        code, reason = WebSocketUtils.parse_close_payload(b'\x03')
        self.assertEqual(code, CloseCode.NO_STATUS)


class TestEdgeCases(unittest.TestCase):
    """测试边界情况"""
    
    def test_max_payload_size(self):
        """测试最大载荷大小"""
        # 测试接近最大 32 位整数的大小
        # 由于内存限制，我们只测试编码/解码逻辑
        data = "X" * 100000
        frame = encode_text(data)
        decoded, _ = decode_frame(frame)
        self.assertEqual(len(decoded.payload), len(data))
    
    def test_rsv_bits(self):
        """测试 RSV 位"""
        # 创建带有 RSV 位的帧（模拟扩展协商）
        frame = WebSocketFrame(
            fin=True,
            rsv1=True,
            rsv2=False,
            rsv3=False,
            opcode=Opcode.TEXT,
            payload=b"test"
        )
        
        self.assertTrue(frame.rsv1)
        self.assertFalse(frame.rsv2)
        self.assertFalse(frame.rsv3)
    
    def test_continuation_frame(self):
        """测试延续帧"""
        frame = encode_frame(b"partial", opcode=Opcode.CONTINUATION, fin=False)
        decoded, _ = decode_frame(frame)
        
        self.assertEqual(decoded.opcode, Opcode.CONTINUATION)
        self.assertFalse(decoded.fin)


if __name__ == '__main__':
    unittest.main(verbosity=2)
"""
WebSocket Utilities - WebSocket 辅助工具包

提供 WebSocket 协议相关的工具函数，包括：
- 帧解析与构建
- 消息编码解码
- 握手验证
- Ping/Pong 处理

零外部依赖，纯 Python 实现。
"""

import hashlib
import base64
import struct
import random
import os
from typing import Tuple, Optional, Union, List
from enum import IntEnum


class Opcode(IntEnum):
    """WebSocket 操作码"""
    CONTINUATION = 0x0
    TEXT = 0x1
    BINARY = 0x2
    CLOSE = 0x8
    PING = 0x9
    PONG = 0xA


class CloseCode(IntEnum):
    """WebSocket 关闭状态码"""
    NORMAL = 1000
    GOING_AWAY = 1001
    PROTOCOL_ERROR = 1002
    UNSUPPORTED_DATA = 1003
    NO_STATUS = 1005
    ABNORMAL_CLOSURE = 1006
    INVALID_PAYLOAD = 1007
    POLICY_VIOLATION = 1008
    MESSAGE_TOO_BIG = 1009
    MANDATORY_EXTENSION = 1010
    INTERNAL_ERROR = 1011
    SERVICE_RESTART = 1012
    TRY_AGAIN_LATER = 1013
    TLS_HANDSHAKE = 1015


class WebSocketFrame:
    """WebSocket 帧结构"""
    
    def __init__(
        self,
        fin: bool = True,
        rsv1: bool = False,
        rsv2: bool = False,
        rsv3: bool = False,
        opcode: int = Opcode.TEXT,
        masked: bool = False,
        payload: bytes = b''
    ):
        self.fin = fin
        self.rsv1 = rsv1
        self.rsv2 = rsv2
        self.rsv3 = rsv3
        self.opcode = opcode
        self.masked = masked
        self.payload = payload
    
    def __repr__(self):
        return (
            f"WebSocketFrame(fin={self.fin}, opcode={Opcode(self.opcode).name}, "
            f"masked={self.masked}, payload_len={len(self.payload)})"
        )


class WebSocketUtils:
    """WebSocket 工具类"""
    
    WEBSOCKET_GUID = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
    
    @staticmethod
    def compute_accept_key(key: str) -> str:
        """
        计算 Sec-WebSocket-Accept 值
        
        Args:
            key: 客户端发送的 Sec-WebSocket-Key
            
        Returns:
            服务器应返回的 Sec-WebSocket-Accept 值
        """
        sha1 = hashlib.sha1((key + WebSocketUtils.WEBSOCKET_GUID).encode()).digest()
        return base64.b64encode(sha1).decode()
    
    @staticmethod
    def generate_key() -> str:
        """
        生成随机的 Sec-WebSocket-Key
        
        Returns:
            Base64 编码的 16 字节随机值
        """
        return base64.b64encode(os.urandom(16)).decode()
    
    @staticmethod
    def encode_frame(
        data: Union[str, bytes],
        opcode: int = Opcode.TEXT,
        fin: bool = True,
        mask: bool = False,
        mask_key: Optional[bytes] = None
    ) -> bytes:
        """
        编码 WebSocket 帧
        
        Args:
            data: 要发送的数据
            opcode: 操作码
            fin: 是否为最后一帧
            mask: 是否掩码
            mask_key: 掩码密钥（如果为 None 则随机生成）
            
        Returns:
            编码后的字节流
        """
        if isinstance(data, str):
            payload = data.encode('utf-8')
        else:
            payload = data
        
        # 构建帧头
        frame = bytearray()
        
        # 第一个字节: FIN, RSV1-3, Opcode
        first_byte = (int(fin) << 7) | opcode
        frame.append(first_byte)
        
        # 第二个字节: MASK, Payload length
        payload_len = len(payload)
        
        if mask:
            if mask_key is None:
                mask_key = os.urandom(4)
            elif len(mask_key) != 4:
                raise ValueError("Mask key must be 4 bytes")
        
        if payload_len <= 125:
            second_byte = (int(mask) << 7) | payload_len
            frame.append(second_byte)
        elif payload_len <= 65535:
            second_byte = (int(mask) << 7) | 126
            frame.append(second_byte)
            frame.extend(struct.pack('!H', payload_len))
        else:
            second_byte = (int(mask) << 7) | 127
            frame.append(second_byte)
            frame.extend(struct.pack('!Q', payload_len))
        
        # 掩码密钥
        if mask and mask_key:
            frame.extend(mask_key)
            # 掩码处理
            masked_payload = bytearray(payload_len)
            for i in range(payload_len):
                masked_payload[i] = payload[i] ^ mask_key[i % 4]
            frame.extend(masked_payload)
        else:
            frame.extend(payload)
        
        return bytes(frame)
    
    @staticmethod
    def decode_frame(data: bytes) -> Tuple[WebSocketFrame, int]:
        """
        解码 WebSocket 帧
        
        Args:
            data: 原始字节流
            
        Returns:
            (WebSocketFrame 对象, 已解析的字节数)
        """
        if len(data) < 2:
            raise ValueError("Insufficient data for WebSocket frame")
        
        # 解析第一个字节
        first_byte = data[0]
        fin = bool(first_byte & 0x80)
        rsv1 = bool(first_byte & 0x40)
        rsv2 = bool(first_byte & 0x20)
        rsv3 = bool(first_byte & 0x10)
        opcode = first_byte & 0x0F
        
        # 解析第二个字节
        second_byte = data[1]
        masked = bool(second_byte & 0x80)
        payload_len = second_byte & 0x7F
        
        offset = 2
        
        # 扩展长度
        if payload_len == 126:
            if len(data) < 4:
                raise ValueError("Insufficient data for extended length")
            payload_len = struct.unpack('!H', data[2:4])[0]
            offset = 4
        elif payload_len == 127:
            if len(data) < 10:
                raise ValueError("Insufficient data for extended length")
            payload_len = struct.unpack('!Q', data[2:10])[0]
            offset = 10
        
        # 掩码密钥
        mask_key = None
        if masked:
            if len(data) < offset + 4:
                raise ValueError("Insufficient data for mask key")
            mask_key = data[offset:offset + 4]
            offset += 4
        
        # 载荷
        if len(data) < offset + payload_len:
            raise ValueError("Insufficient data for payload")
        
        payload = bytearray(data[offset:offset + payload_len])
        
        # 解掩码
        if masked and mask_key:
            for i in range(len(payload)):
                payload[i] ^= mask_key[i % 4]
        
        frame = WebSocketFrame(
            fin=fin,
            rsv1=rsv1,
            rsv2=rsv2,
            rsv3=rsv3,
            opcode=opcode,
            masked=masked,
            payload=bytes(payload)
        )
        
        return frame, offset + payload_len
    
    @staticmethod
    def encode_text(data: str, mask: bool = False) -> bytes:
        """编码文本消息"""
        return WebSocketUtils.encode_frame(data, Opcode.TEXT, mask=mask)
    
    @staticmethod
    def encode_binary(data: bytes, mask: bool = False) -> bytes:
        """编码二进制消息"""
        return WebSocketUtils.encode_frame(data, Opcode.BINARY, mask=mask)
    
    @staticmethod
    def encode_ping(data: bytes = b'', mask: bool = False) -> bytes:
        """编码 Ping 帧"""
        return WebSocketUtils.encode_frame(data, Opcode.PING, mask=mask)
    
    @staticmethod
    def encode_pong(data: bytes = b'', mask: bool = False) -> bytes:
        """编码 Pong 帧"""
        return WebSocketUtils.encode_frame(data, Opcode.PONG, mask=mask)
    
    @staticmethod
    def encode_close(code: int = CloseCode.NORMAL, reason: str = '', mask: bool = False) -> bytes:
        """
        编码关闭帧
        
        Args:
            code: 关闭状态码
            reason: 关闭原因
            mask: 是否掩码
            
        Returns:
            编码后的关闭帧
        """
        payload = struct.pack('!H', code) + reason.encode('utf-8')
        return WebSocketUtils.encode_frame(payload, Opcode.CLOSE, mask=mask)
    
    @staticmethod
    def parse_close_payload(payload: bytes) -> Tuple[int, str]:
        """
        解析关闭帧载荷
        
        Args:
            payload: 关闭帧载荷
            
        Returns:
            (状态码, 原因字符串)
        """
        if len(payload) < 2:
            return CloseCode.NO_STATUS, ''
        
        code = struct.unpack('!H', payload[:2])[0]
        try:
            reason = payload[2:].decode('utf-8')
        except UnicodeDecodeError:
            reason = ''
        
        return code, reason
    
    @staticmethod
    def is_control_frame(opcode: int) -> bool:
        """检查是否为控制帧"""
        return opcode >= 0x8
    
    @staticmethod
    def validate_utf8(data: bytes) -> bool:
        """验证 UTF-8 编码"""
        try:
            data.decode('utf-8')
            return True
        except UnicodeDecodeError:
            return False
    
    @staticmethod
    def fragmentation_encode(
        data: Union[str, bytes],
        max_frame_size: int = 65536,
        opcode: int = Opcode.TEXT,
        mask: bool = False
    ) -> List[bytes]:
        """
        将大数据分片编码为多个帧
        
        Args:
            data: 要发送的数据
            max_frame_size: 最大帧大小
            opcode: 操作码
            mask: 是否掩码
            
        Returns:
            编码后的帧列表
        """
        if isinstance(data, str):
            data = data.encode('utf-8')
        
        frames = []
        offset = 0
        is_first = True
        
        while offset < len(data):
            chunk = data[offset:offset + max_frame_size]
            offset += max_frame_size
            is_last = offset >= len(data)
            
            if is_first:
                frame_opcode = opcode
            else:
                frame_opcode = Opcode.CONTINUATION
            
            frame = WebSocketUtils.encode_frame(
                chunk,
                opcode=frame_opcode,
                fin=is_last,
                mask=mask
            )
            frames.append(frame)
            is_first = False
        
        return frames


def compute_accept_key(key: str) -> str:
    """计算 Sec-WebSocket-Accept 值"""
    return WebSocketUtils.compute_accept_key(key)


def generate_key() -> str:
    """生成随机的 Sec-WebSocket-Key"""
    return WebSocketUtils.generate_key()


def encode_frame(data: Union[str, bytes], opcode: int = Opcode.TEXT, 
                fin: bool = True, mask: bool = False) -> bytes:
    """编码 WebSocket 帧"""
    return WebSocketUtils.encode_frame(data, opcode, fin, mask)


def decode_frame(data: bytes) -> Tuple[WebSocketFrame, int]:
    """解码 WebSocket 帧"""
    return WebSocketUtils.decode_frame(data)


def encode_text(data: str, mask: bool = False) -> bytes:
    """编码文本消息"""
    return WebSocketUtils.encode_text(data, mask)


def encode_binary(data: bytes, mask: bool = False) -> bytes:
    """编码二进制消息"""
    return WebSocketUtils.encode_binary(data, mask)


def encode_ping(data: bytes = b'', mask: bool = False) -> bytes:
    """编码 Ping 帧"""
    return WebSocketUtils.encode_ping(data, mask)


def encode_pong(data: bytes = b'', mask: bool = False) -> bytes:
    """编码 Pong 帧"""
    return WebSocketUtils.encode_pong(data, mask)


def encode_close(code: int = CloseCode.NORMAL, reason: str = '', mask: bool = False) -> bytes:
    """编码关闭帧"""
    return WebSocketUtils.encode_close(code, reason, mask)


# 示例用法
if __name__ == "__main__":
    # 握手验证
    client_key = generate_key()
    accept_key = compute_accept_key(client_key)
    print(f"Client Key: {client_key}")
    print(f"Accept Key: {accept_key}")
    
    # 文本消息
    text_frame = encode_text("Hello, WebSocket!")
    print(f"\nEncoded text frame: {text_frame.hex()}")
    
    # 解码
    frame, consumed = decode_frame(text_frame)
    print(f"Decoded: {frame}")
    print(f"Payload: {frame.payload.decode('utf-8')}")
    
    # 掩码消息
    masked_frame = encode_text("Hello, Masked!", mask=True)
    frame, _ = decode_frame(masked_frame)
    print(f"\nMasked payload: {frame.payload.decode('utf-8')}")
    
    # Ping/Pong
    ping_frame = encode_ping(b"test")
    print(f"\nPing frame: {ping_frame.hex()}")
    
    # 关闭帧
    close_frame = encode_close(CloseCode.NORMAL, "Goodbye")
    code, reason = WebSocketUtils.parse_close_payload(decode_frame(close_frame)[0].payload)
    print(f"\nClose frame - Code: {code}, Reason: {reason}")
    
    # 分片
    large_data = "A" * 200000
    fragments = WebSocketUtils.fragmentation_encode(large_data, max_frame_size=50000)
    print(f"\nFragmented into {len(fragments)} frames")
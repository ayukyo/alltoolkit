"""
WebSocket Utilities - WebSocket 辅助工具包

提供 WebSocket 协议相关的工具函数。

使用示例:
    from websocket_utils import encode_text, decode_frame, compute_accept_key
    
    # 握手验证
    client_key = generate_key()
    accept_key = compute_accept_key(client_key)
    
    # 编码消息
    frame = encode_text("Hello, WebSocket!")
    
    # 解码消息
    decoded, consumed = decode_frame(frame)
    print(decoded.payload.decode('utf-8'))
"""

from .mod import (
    # 类
    WebSocketUtils,
    WebSocketFrame,
    Opcode,
    CloseCode,
    # 函数
    compute_accept_key,
    generate_key,
    encode_frame,
    decode_frame,
    encode_text,
    encode_binary,
    encode_ping,
    encode_pong,
    encode_close,
)

__all__ = [
    # 类
    'WebSocketUtils',
    'WebSocketFrame',
    'Opcode',
    'CloseCode',
    # 函数
    'compute_accept_key',
    'generate_key',
    'encode_frame',
    'decode_frame',
    'encode_text',
    'encode_binary',
    'encode_ping',
    'encode_pong',
    'encode_close',
]

__version__ = '1.0.0'
"""
WebSocket Utilities 使用示例

演示如何使用 websocket_utils 工具包处理 WebSocket 协议。
"""

from mod import (
    WebSocketUtils, WebSocketFrame, Opcode, CloseCode,
    compute_accept_key, generate_key, encode_frame, decode_frame,
    encode_text, encode_binary, encode_ping, encode_pong, encode_close
)


def example_handshake():
    """示例：WebSocket 握手验证"""
    print("=" * 60)
    print("示例 1: WebSocket 握手验证")
    print("=" * 60)
    
    # 客户端生成 key
    client_key = generate_key()
    print(f"1. 客户端生成 Sec-WebSocket-Key: {client_key}")
    
    # 服务器计算 accept key
    server_accept = compute_accept_key(client_key)
    print(f"2. 服务器计算 Sec-WebSocket-Accept: {server_accept}")
    
    # 客户端验证 accept（模拟）
    expected = compute_accept_key(client_key)
    print(f"3. 客户端验证: {'成功' if server_accept == expected else '失败'}")
    
    print()


def example_text_message():
    """示例：发送文本消息"""
    print("=" * 60)
    print("示例 2: 发送文本消息")
    print("=" * 60)
    
    # 编码文本消息
    message = "你好，WebSocket！"
    frame = encode_text(message)
    print(f"原始消息: {message}")
    print(f"编码后帧: {frame.hex()}")
    
    # 解码帧
    decoded, consumed = decode_frame(frame)
    print(f"解码消息: {decoded.payload.decode('utf-8')}")
    print(f"消耗字节: {consumed}")
    
    print()


def example_binary_message():
    """示例：发送二进制消息"""
    print("=" * 60)
    print("示例 3: 发送二进制消息")
    print("=" * 60)
    
    # 编码二进制数据
    binary_data = bytes([0x01, 0x02, 0x03, 0x04, 0x05])
    frame = encode_binary(binary_data)
    print(f"原始数据: {binary_data.hex()}")
    print(f"编码后帧: {frame.hex()}")
    
    # 解码帧
    decoded, _ = decode_frame(frame)
    print(f"解码数据: {decoded.payload.hex()}")
    print(f"Opcode: {Opcode(decoded.opcode).name}")
    
    print()


def example_masked_message():
    """示例：发送掩码消息（客户端模式）"""
    print("=" * 60)
    print("示例 4: 发送掩码消息（客户端模式）")
    print("=" * 60)
    
    # 客户端发送消息时需要掩码
    message = "Hello from client!"
    frame = encode_text(message, mask=True)
    print(f"原始消息: {message}")
    print(f"掩码帧: {frame.hex()}")
    print(f"帧长度: {len(frame)} 字节")
    
    # 服务器解码（自动解除掩码）
    decoded, _ = decode_frame(frame)
    print(f"解码消息: {decoded.payload.decode('utf-8')}")
    print(f"是否掩码: {decoded.masked}")
    
    print()


def example_ping_pong():
    """示例：Ping/Pong 心跳"""
    print("=" * 60)
    print("示例 5: Ping/Pong 心跳")
    print("=" * 60)
    
    # 发送 Ping
    ping_data = b"heartbeat"
    ping_frame = encode_ping(ping_data)
    print(f"发送 Ping: {ping_data}")
    print(f"Ping 帧: {ping_frame.hex()}")
    
    # 接收 Ping 并回复 Pong
    decoded_ping, _ = decode_frame(ping_frame)
    print(f"收到 Ping: {decoded_ping.payload}")
    print(f"Opcode: {Opcode(decoded_ping.opcode).name}")
    
    # 回复 Pong
    pong_frame = encode_pong(decoded_ping.payload)
    print(f"回复 Pong 帧: {pong_frame.hex()}")
    
    print()


def example_close_connection():
    """示例：关闭连接"""
    print("=" * 60)
    print("示例 6: 关闭连接")
    print("=" * 60)
    
    # 正常关闭
    close_frame = encode_close(CloseCode.NORMAL, "Connection closed normally")
    print(f"关闭帧: {close_frame.hex()}")
    
    # 解析关闭帧
    decoded, _ = decode_frame(close_frame)
    code, reason = WebSocketUtils.parse_close_payload(decoded.payload)
    print(f"关闭码: {code} ({CloseCode(code).name})")
    print(f"关闭原因: {reason}")
    
    print()
    
    # 异常关闭示例
    error_close = encode_close(CloseCode.PROTOCOL_ERROR, "Invalid frame format")
    decoded, _ = decode_frame(error_close)
    code, reason = WebSocketUtils.parse_close_payload(decoded.payload)
    print(f"错误关闭码: {code}")
    print(f"错误原因: {reason}")
    
    print()


def example_fragmentation():
    """示例：消息分片"""
    print("=" * 60)
    print("示例 7: 大消息分片")
    print("=" * 60)
    
    # 大消息分片发送
    large_message = "A" * 1000
    frames = WebSocketUtils.fragmentation_encode(
        large_message,
        max_frame_size=300,
        opcode=Opcode.TEXT
    )
    
    print(f"原始消息长度: {len(large_message)} 字节")
    print(f"分片数量: {len(frames)} 片")
    print(f"每片最大大小: 300 字节")
    
    # 分析每片
    print("\n分片详情:")
    for i, frame in enumerate(frames):
        decoded, _ = decode_frame(frame)
        opcode_name = Opcode(decoded.opcode).name
        print(f"  片 {i+1}: Opcode={opcode_name:12} FIN={decoded.fin} 长度={len(decoded.payload)}")
    
    # 重组验证
    reconstructed = b""
    for frame in frames:
        decoded, _ = decode_frame(frame)
        reconstructed += decoded.payload
    
    print(f"\n重组后长度: {len(reconstructed)} 字节")
    print(f"数据完整: {'是' if reconstructed.decode('utf-8') == large_message else '否'}")
    
    print()


def example_custom_mask_key():
    """示例：自定义掩码密钥"""
    print("=" * 60)
    print("示例 8: 自定义掩码密钥")
    print("=" * 60)
    
    # 使用自定义掩码密钥
    custom_mask = b"\x12\x34\x56\x78"
    message = "Test message"
    
    frame = WebSocketUtils.encode_frame(
        message,
        opcode=Opcode.TEXT,
        mask=True,
        mask_key=custom_mask
    )
    
    print(f"自定义掩码: {custom_mask.hex()}")
    print(f"原始消息: {message}")
    print(f"掩码帧: {frame.hex()}")
    
    # 解码验证
    decoded, _ = decode_frame(frame)
    print(f"解码消息: {decoded.payload.decode('utf-8')}")
    
    print()


def example_frame_structure():
    """示例：帧结构详解"""
    print("=" * 60)
    print("示例 9: WebSocket 帧结构详解")
    print("=" * 60)
    
    # 创建一个简单的文本帧
    frame = encode_text("Hi")
    
    print("帧结构分析:")
    print(f"完整帧: {frame.hex()}")
    print(f"帧长度: {len(frame)} 字节")
    print()
    
    # 解析帧头
    byte0 = frame[0]
    byte1 = frame[1]
    
    fin = bool(byte0 & 0x80)
    rsv1 = bool(byte0 & 0x40)
    rsv2 = bool(byte0 & 0x20)
    rsv3 = bool(byte0 & 0x10)
    opcode = byte0 & 0x0F
    
    masked = bool(byte1 & 0x80)
    payload_len = byte1 & 0x7F
    
    print(f"第 1 字节 (0x{byte0:02x}):")
    print(f"  FIN: {fin}")
    print(f"  RSV1: {rsv1}")
    print(f"  RSV2: {rsv2}")
    print(f"  RSV3: {rsv3}")
    print(f"  Opcode: {opcode} ({Opcode(opcode).name})")
    print()
    
    print(f"第 2 字节 (0x{byte1:02x}):")
    print(f"  MASK: {masked}")
    print(f"  Payload Length: {payload_len}")
    print()
    
    if payload_len < 126:
        print(f"载荷数据: {frame[2:].hex()}")
        print(f"载荷文本: {frame[2:].decode('utf-8')}")
    
    print()


def example_extended_length():
    """示例：扩展长度处理"""
    print("=" * 60)
    print("示例 10: 扩展长度处理")
    print("=" * 60)
    
    # 16 位扩展长度 (> 125 字节)
    data_16bit = "X" * 200
    frame_16bit = encode_text(data_16bit)
    print(f"200 字节数据:")
    print(f"  帧长度: {len(frame_16bit)} 字节")
    print(f"  第 2 字节: {frame_16bit[1]} (应为 126)")
    print(f"  扩展长度: {int.from_bytes(frame_16bit[2:4], 'big')}")
    
    print()
    
    # 64 位扩展长度 (> 65535 字节)
    data_64bit = "Y" * 70000
    frame_64bit = encode_text(data_64bit)
    print(f"70000 字节数据:")
    print(f"  帧长度: {len(frame_64bit)} 字节")
    print(f"  第 2 字节: {frame_64bit[1]} (应为 127)")
    print(f"  扩展长度: {int.from_bytes(frame_64bit[2:10], 'big')}")
    
    print()


def main():
    """运行所有示例"""
    example_handshake()
    example_text_message()
    example_binary_message()
    example_masked_message()
    example_ping_pong()
    example_close_connection()
    example_fragmentation()
    example_custom_mask_key()
    example_frame_structure()
    example_extended_length()
    
    print("=" * 60)
    print("所有示例运行完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
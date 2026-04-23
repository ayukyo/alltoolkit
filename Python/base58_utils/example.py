"""
Base58 工具使用示例

演示 Base58 编码、比特币地址、IPFS CID 等功能
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from base58_utils.mod import (
    Base58Encoder,
    Base58Validator,
    BitcoinAddress,
    IPFSHash,
    Base58Converter,
    encode,
    decode,
    encode_check,
    decode_check,
    BASE58_ALPHABET,
    FLICKR_ALPHABET
)
import hashlib


def example_basic_encoding():
    """基本编码示例"""
    print("=" * 50)
    print("1. 基本 Base58 编码")
    print("=" * 50)
    
    # 简单编码
    text = "Hello, Base58!"
    encoded = encode(text.encode('utf-8'))
    print(f"原文: {text}")
    print(f"Base58: {encoded}")
    
    # 解码
    decoded = decode(encoded)
    print(f"解码: {decoded.decode('utf-8')}")
    
    # 使用编码器对象
    encoder = Base58Encoder()
    data = b"\x00\x00\x00test"  # 带前导零
    encoded = encoder.encode(data)
    print(f"\n带前导零的数据: {data.hex()}")
    print(f"Base58: {encoded}")
    print(f"注意: 前导零变成前导 '1'")
    
    print()


def example_base58_check():
    """Base58Check 示例"""
    print("=" * 50)
    print("2. Base58Check (带校验和)")
    print("=" * 50)
    
    encoder = Base58Encoder()
    
    # 编码带校验和的数据
    data = b"important data"
    encoded = encoder.encode_check(data)
    print(f"原文: {data}")
    print(f"Base58Check: {encoded}")
    
    # 解码并验证
    decoded = encoder.decode_check(encoded)
    print(f"解码: {decoded}")
    
    # 校验和检测篡改
    print("\n篡改检测演示:")
    tampered = encoded[:-1] + ('2' if encoded[-1] != '2' else '3')
    print(f"篡改后: {tampered}")
    try:
        encoder.decode_check(tampered)
        print("错误: 未检测到篡改!")
    except Exception as e:
        print(f"检测到篡改: {e}")
    
    print()


def example_bitcoin_address():
    """比特币地址示例"""
    print("=" * 50)
    print("3. 比特币地址处理")
    print("=" * 50)
    
    btc = BitcoinAddress()
    
    # 验证比特币地址
    addresses = [
        "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa",  # 中本聪创世地址
        "3J98t1WpEZ73CNmQviecrnyiWrnqRhWNLy",  # P2SH 地址
        "invalid_address",
    ]
    
    for addr in addresses:
        is_valid = btc.is_valid_bitcoin_address(addr)
        print(f"\n地址: {addr}")
        print(f"有效: {is_valid}")
        
        if is_valid:
            addr_type = btc.get_address_type(addr)
            print(f"类型: {addr_type}")
            
            version, pubkey_hash = btc.decode_address(addr)
            print(f"版本前缀: {version.hex()}")
            print(f"公钥哈希: {pubkey_hash.hex()}")
    
    # 生成新地址 (模拟)
    print("\n生成新比特币地址:")
    random_hash = hashlib.sha256(b"example public key").digest()[:20]
    new_address = btc.encode_address(random_hash)
    print(f"公钥哈希: {random_hash.hex()}")
    print(f"地址: {new_address}")
    
    print()


def example_ipfs_cid():
    """IPFS CID 示例"""
    print("=" * 50)
    print("4. IPFS CID 编码")
    print("=" * 50)
    
    ipfs = IPFSHash()
    
    # 从内容生成 CID
    content = b"Hello, IPFS World!"
    content_hash = hashlib.sha256(content).digest()
    
    # CIDv0 (传统格式，Qm 开头)
    cid_v0 = ipfs.encode_cid(content_hash, version=0)
    print(f"内容: {content.decode()}")
    print(f"SHA256: {content_hash.hex()}")
    print(f"CIDv0: {cid_v0}")
    
    # CIDv1 (新格式，b 开头)
    cid_v1 = ipfs.encode_cid(content_hash, version=1)
    print(f"CIDv1: {cid_v1}")
    
    # 解析 CID
    print("\n解析 CIDv0:")
    version, codec, hash_back = ipfs.decode_cid(cid_v0)
    print(f"  版本: {version}")
    print(f"  编解码器: {codec:#x}")
    print(f"  哈希: {hash_back.hex()}")
    print(f"  哈希匹配: {hash_back == content_hash}")
    
    print()


def example_converter():
    """进制转换示例"""
    print("=" * 50)
    print("5. 进制转换")
    print("=" * 50)
    
    converter = Base58Converter()
    
    # 十六进制转 Base58
    hex_string = "deadbeef"
    base58 = converter.from_hex(hex_string)
    print(f"十六进制 0x{hex_string} -> Base58: {base58}")
    print(f"Base58 {base58} -> 十六进制: {converter.to_hex(base58)}")
    
    # 整数转 Base58
    numbers = [0, 1, 58, 123456789, 2**64 - 1]
    print("\n整数转 Base58:")
    for num in numbers:
        base58 = converter.from_int(num)
        back = converter.to_int(base58)
        print(f"  {num} -> {base58} -> {back}")
    
    # Base64 转换
    import base64
    data = b"Binary data for conversion"
    b64 = base64.b64encode(data).decode()
    base58_from_b64 = converter.from_base64(b64)
    print(f"\nBase64: {b64}")
    print(f"Base58: {base58_from_b64}")
    
    print()


def example_validator():
    """验证器示例"""
    print("=" * 50)
    print("6. Base58 验证")
    print("=" * 50)
    
    validator = Base58Validator()
    
    # 验证各种字符串
    test_strings = [
        "Hello",
        "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa",
        "QmXZJTjZ7z8s5h5h5h5h5h5h5h5h5h5h5h5h5h5h5h5h",  # 无效 IPFS CID
        "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz",
        "0",  # 无效: 零不在 Base58 中
        "O",  # 无效: 大写 O 不在 Base58 中
    ]
    
    print("字符串验证:")
    for s in test_strings:
        valid = validator.is_valid(s)
        status = "✓ 有效" if valid else "✗ 无效"
        print(f"  {s[:40]:<40} {status}")
    
    # 验证带校验和的字符串
    encoder = Base58Encoder()
    valid_check = encoder.encode_check(b"test data")
    
    print(f"\nBase58Check 验证:")
    print(f"  {valid_check}: {'✓ 有效' if validator.is_valid_check(valid_check) else '✗ 无效'}")
    print(f"  {valid_check[:-1]}X: {'✓ 有效' if validator.is_valid_check(valid_check[:-1] + 'X') else '✗ 无效'}")
    
    print()


def example_custom_alphabet():
    """自定义字母表示例"""
    print("=" * 50)
    print("7. 自定义 Base58 字母表")
    print("=" * 50)
    
    data = b"Same data, different alphabets"
    
    # 标准字母表
    standard = Base58Encoder(BASE58_ALPHABET)
    print(f"数据: {data.decode()}")
    print(f"标准: {standard.encode(data)}")
    
    # Flickr 字母表
    flickr = Base58Encoder(FLICKR_ALPHABET)
    print(f"Flickr: {flickr.encode(data)}")
    
    # 自定义字母表
    custom_alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ123456789"
    custom = Base58Encoder(custom_alphabet)
    print(f"自定义: {custom.encode(data)}")
    
    print("\n注意: 不同字母表产生不同的编码结果，但都可以正确解码回原文")
    
    print()


def example_real_world():
    """实际应用示例"""
    print("=" * 50)
    print("8. 实际应用场景")
    print("=" * 50)
    
    encoder = Base58Encoder()
    
    # 1. 短链接生成
    print("场景 1: 短链接")
    url_id = hashlib.sha256(b"https://example.com/very/long/url/path").digest()[:6]
    short_code = encoder.encode(url_id)
    print(f"  原始 URL ID: {url_id.hex()}")
    print(f"  短链接码: {short_code}")
    print(f"  完整短链接: https://s.example.com/{short_code}")
    
    # 2. 订单号生成
    print("\n场景 2: 友好的订单号")
    import time
    timestamp = int(time.time())
    random_part = os.urandom(4)
    order_data = timestamp.to_bytes(4, 'big') + random_part
    order_id = encoder.encode(order_data)
    print(f"  订单 ID: {order_id}")
    print(f"  长度: {len(order_id)} 字符 (无歧义字符)")
    
    # 3. 文件指纹
    print("\n场景 3: 文件内容指纹")
    file_content = "重要文档内容...".encode('utf-8')
    file_hash = hashlib.sha256(file_content).digest()
    fingerprint = encoder.encode(file_hash)
    print(f"  SHA256: {file_hash.hex()}")
    print(f"  Base58 指纹: {fingerprint}")
    print(f"  长度: {len(fingerprint)} 字符 (比十六进制短 10 字符)")
    
    print()


def main():
    """运行所有示例"""
    print("\n" + "=" * 50)
    print("Base58 工具使用示例")
    print("=" * 50 + "\n")
    
    example_basic_encoding()
    example_base58_check()
    example_bitcoin_address()
    example_ipfs_cid()
    example_converter()
    example_validator()
    example_custom_alphabet()
    example_real_world()
    
    print("=" * 50)
    print("示例运行完成!")
    print("=" * 50)


if __name__ == "__main__":
    main()
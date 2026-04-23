"""
Base58 编码/解码工具测试

测试覆盖：
- 基本编码/解码
- Base58Check 编码/解码
- 比特币地址验证
- IPFS CID 编码/解码
- 进制转换
- 边界情况和错误处理
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from base58_utils.mod import (
    Base58Encoder,
    Base58Validator,
    Base58Error,
    BitcoinAddress,
    IPFSHash,
    Base58Converter,
    encode,
    decode,
    encode_check,
    decode_check,
    is_valid,
    BASE58_ALPHABET,
    FLICKR_ALPHABET,
    RIPPLE_ALPHABET
)
import hashlib


def test_basic_encode_decode():
    """测试基本编码和解码"""
    print("测试基本编码/解码...")
    
    encoder = Base58Encoder()
    
    # 测试用例：已知答案
    test_cases = [
        (b"", ""),  # 空输入
        (b"\x00", "1"),  # 单个零字节
        (b"\x00\x00", "11"),  # 两个零字节
        (b"Hello World", "JxF12TrwUP45BMd"),  # 标准测试向量
        (b"\x00\x00\x00\x00", "1111"),  # 多个前导零
    ]
    
    for data, expected in test_cases:
        encoded = encoder.encode(data)
        if expected:
            assert encoded == expected, f"编码失败: {data} -> {encoded}, 期望 {expected}"
        
        decoded = encoder.decode(encoded) if encoded else b""
        assert decoded == data, f"解码失败: {encoded} -> {decoded}, 期望 {data}"
    
    print("  ✓ 基本编码/解码测试通过")


def test_base58_check():
    """测试 Base58Check 编码"""
    print("测试 Base58Check...")
    
    encoder = Base58Encoder()
    
    # 编码并解码带校验和的数据
    test_data = [
        b"Hello World",
        b"\x00" * 20,  # 模拟比特币公钥哈希
        b"test data 123",
        bytes(range(256)),  # 所有字节值
    ]
    
    for data in test_data:
        encoded = encoder.encode_check(data)
        decoded = encoder.decode_check(encoded)
        assert decoded == data, f"Base58Check 失败: {data} -> {encoded} -> {decoded}"
    
    # 测试校验和错误检测
    valid_encoded = encoder.encode_check(b"test")
    # 修改一个字符
    invalid_encoded = valid_encoded[:-1] + ('2' if valid_encoded[-1] != '2' else '3')
    
    try:
        encoder.decode_check(invalid_encoded)
        assert False, "应该检测到校验和错误"
    except Base58Error:
        pass  # 预期的错误
    
    print("  ✓ Base58Check 测试通过")


def test_bitcoin_address():
    """测试比特币地址功能"""
    print("测试比特币地址...")
    
    btc = BitcoinAddress()
    
    # 已知的比特币地址和对应的公钥哈希
    test_addresses = [
        # 主网 P2PKH 地址 (以 1 开头)
        ("1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa", b'\x00'),  # 创世区块地址
        ("1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2", b'\x00'),
        # 主网 P2SH 地址 (以 3 开头)
        ("3J98t1WpEZ73CNmQviecrnyiWrnqRhWNLy", b'\x05'),
    ]
    
    for address, expected_prefix in test_addresses:
        # 验证地址有效性
        assert btc.is_valid_bitcoin_address(address), f"无效地址: {address}"
        
        # 解码并验证版本
        version, pubkey_hash = btc.decode_address(address)
        assert version == expected_prefix, f"版本前缀错误: {version.hex()}"
        assert len(pubkey_hash) == 20, f"公钥哈希长度错误: {len(pubkey_hash)}"
        
        # 重新编码应该得到相同地址
        reconstructed = btc.encode_address(pubkey_hash, version)
        assert reconstructed == address, f"地址重建失败: {reconstructed} != {address}"
    
    # 测试地址类型识别
    address_type = btc.get_address_type("1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa")
    assert "mainnet" in address_type.lower(), f"地址类型识别错误: {address_type}"
    
    # 测试无效地址
    invalid_addresses = [
        "invalid_address",
        "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfN",  # 少一个字符
        "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfN0",  # 多一个字符
    ]
    
    for addr in invalid_addresses:
        assert not btc.is_valid_bitcoin_address(addr), f"应该检测到无效地址: {addr}"
    
    print("  ✓ 比特币地址测试通过")


def test_ipfs_cid():
    """测试 IPFS CID 编码"""
    print("测试 IPFS CID...")
    
    ipfs = IPFSHash()
    
    # 测试 CIDv0 (Qm 开头)
    content_hash = hashlib.sha256(b"Hello IPFS").digest()
    cid_v0 = ipfs.encode_cid(content_hash, version=0)
    
    assert cid_v0.startswith('Qm'), f"CIDv0 应该以 Qm 开头: {cid_v0}"
    
    version, codec, decoded_hash = ipfs.decode_cid(cid_v0)
    assert version == 0, f"版本应该是 0: {version}"
    assert decoded_hash == content_hash, "内容哈希不匹配"
    
    # 测试 CIDv1
    cid_v1 = ipfs.encode_cid(content_hash, version=1)
    assert cid_v1.startswith('b'), f"CIDv1 应该以 b 开头: {cid_v1}"
    
    version, codec, decoded_hash = ipfs.decode_cid(cid_v1)
    assert version == 1, f"版本应该是 1: {version}"
    assert decoded_hash == content_hash, "内容哈希不匹配"
    
    print("  ✓ IPFS CID 测试通过")


def test_converter():
    """测试进制转换"""
    print("测试进制转换...")
    
    converter = Base58Converter()
    
    # 十六进制转换
    test_hex = "deadbeef"
    base58_from_hex = converter.from_hex(test_hex)
    hex_back = converter.to_hex(base58_from_hex, prefix=False)
    assert hex_back.lower() == test_hex.lower(), f"十六进制转换失败: {test_hex} -> {base58_from_hex} -> {hex_back}"
    
    # 带前缀的十六进制
    base58_from_hex2 = converter.from_hex("0x" + test_hex)
    assert base58_from_hex2 == base58_from_hex, "带前缀的十六进制转换不一致"
    
    # 整数转换
    test_int = 123456789
    base58_from_int = converter.from_int(test_int)
    int_back = converter.to_int(base58_from_int)
    assert int_back == test_int, f"整数转换失败: {test_int} -> {base58_from_int} -> {int_back}"
    
    # 零的特殊处理
    zero_base58 = converter.from_int(0)
    assert zero_base58 == '1', f"零应该编码为 '1': {zero_base58}"
    
    # Base64 转换
    import base64
    test_data = b"Test data for base64"
    b64 = base64.b64encode(test_data).decode()
    base58_from_b64 = converter.from_base64(b64)
    b64_back = converter.to_base64(base58_from_b64)
    assert b64_back == b64, "Base64 转换失败"
    
    print("  ✓ 进制转换测试通过")


def test_validator():
    """测试验证器"""
    print("测试验证器...")
    
    validator = Base58Validator()
    
    # 有效 Base58 字符串
    valid_strings = [
        "1",
        "1111",
        "2NEpo7TZRRrAHB74z6tQZfU",
        "5QXyv",
    ]
    
    for s in valid_strings:
        assert validator.is_valid(s), f"应该有效: {s}"
    
    # 无效 Base58 字符串 (包含非法字符)
    invalid_strings = [
        "0",  # 零不在 Base58 中
        "O",  # 大写 O 不在 Base58 中
        "I",  # 大写 I 不在 Base58 中
        "l",  # 小写 l 不在 Base58 中
        "+",  # 加号不在 Base58 中
        "/",  # 斜杠不在 Base58 中
        "abc0def",  # 包含零
        "hello world",  # 包含空格
    ]
    
    for s in invalid_strings:
        assert not validator.is_valid(s), f"应该无效: {s}"
    
    # 测试 Base58Check 验证
    encoder = Base58Encoder()
    valid_check = encoder.encode_check(b"test")
    assert validator.is_valid_check(valid_check), f"有效的 Base58Check: {valid_check}"
    
    # 篡改校验和
    invalid_check = valid_check[:-1] + ('2' if valid_check[-1] != '2' else '3')
    assert not validator.is_valid_check(invalid_check), f"应该检测到无效校验和: {invalid_check}"
    
    print("  ✓ 验证器测试通过")


def test_custom_alphabet():
    """测试自定义字母表"""
    print("测试自定义字母表...")
    
    # 使用 Flickr 字母表
    flickr_encoder = Base58Encoder(FLICKR_ALPHABET)
    
    data = b"Hello World"
    flickr_encoded = flickr_encoder.encode(data)
    
    # 确保结果只包含 Flickr 字母表中的字符
    assert all(c in FLICKR_ALPHABET for c in flickr_encoded), "Flickr 编码包含无效字符"
    
    # 解码
    decoded = flickr_encoder.decode(flickr_encoded)
    assert decoded == data, f"Flickr 解码失败: {decoded}"
    
    # 使用 Ripple 字母表
    ripple_encoder = Base58Encoder(RIPPLE_ALPHABET)
    ripple_encoded = ripple_encoder.encode(data)
    assert all(c in RIPPLE_ALPHABET for c in ripple_encoded), "Ripple 编码包含无效字符"
    
    decoded = ripple_encoder.decode(ripple_encoded)
    assert decoded == data, f"Ripple 解码失败: {decoded}"
    
    # 不同字母表产生不同结果
    default_encoder = Base58Encoder()
    default_encoded = default_encoder.encode(data)
    assert default_encoded != flickr_encoded, "不同字母表应该产生不同结果"
    
    print("  ✓ 自定义字母表测试通过")


def test_edge_cases():
    """测试边界情况"""
    print("测试边界情况...")
    
    encoder = Base58Encoder()
    
    # 空输入
    assert encoder.encode(b"") == "", "空输入应该返回空字符串"
    assert encoder.decode("") == b"", "空字符串解码应该返回空字节"
    
    # 全零输入
    all_zeros = b"\x00" * 10
    encoded_zeros = encoder.encode(all_zeros)
    assert encoded_zeros == "1" * 10, f"全零应该编码为全 '1': {encoded_zeros}"
    
    # 非常大的数据
    large_data = os.urandom(1024)  # 1KB 随机数据
    encoded_large = encoder.encode(large_data)
    decoded_large = encoder.decode(encoded_large)
    assert decoded_large == large_data, "大数据编码/解码失败"
    
    # 二进制数据边界
    for byte_val in range(256):
        single_byte = bytes([byte_val])
        encoded = encoder.encode(single_byte)
        decoded = encoder.decode(encoded)
        assert decoded == single_byte, f"单字节 {byte_val} 编码/解码失败"
    
    print("  ✓ 边界情况测试通过")


def test_convenience_functions():
    """测试便捷函数"""
    print("测试便捷函数...")
    
    data = b"test data"
    
    # encode/decode
    encoded = encode(data)
    decoded = decode(encoded)
    assert decoded == data, "encode/decode 便捷函数失败"
    
    # encode_check/decode_check
    encoded_check = encode_check(data)
    decoded_check = decode_check(encoded_check)
    assert decoded_check == data, "encode_check/decode_check 便捷函数失败"
    
    # is_valid
    assert is_valid(encoded), "is_valid 便捷函数失败"
    assert not is_valid("invalid!"), "is_valid 应该返回 False"
    
    print("  ✓ 便捷函数测试通过")


def test_error_handling():
    """测试错误处理"""
    print("测试错误处理...")
    
    encoder = Base58Encoder()
    
    # 解码无效字符
    invalid_chars = ["0", "O", "I", "l", "+", "/", "test!"]
    for invalid in invalid_chars:
        try:
            encoder.decode(invalid)
            assert False, f"应该抛出错误: {invalid}"
        except Base58Error:
            pass  # 预期的错误
    
    # 无效的字母表长度
    try:
        Base58Encoder("abc")  # 只有 3 个字符
        assert False, "应该拒绝无效长度的字母表"
    except ValueError:
        pass  # 预期的错误
    
    # Base58Check 数据太短
    try:
        encoder.decode_check("1")  # 太短，无法包含校验和
        assert False, "应该检测到数据太短"
    except Base58Error:
        pass  # 预期的错误
    
    print("  ✓ 错误处理测试通过")


def run_all_tests():
    """运行所有测试"""
    print("\n" + "=" * 50)
    print("Base58 工具测试")
    print("=" * 50 + "\n")
    
    tests = [
        test_basic_encode_decode,
        test_base58_check,
        test_bitcoin_address,
        test_ipfs_cid,
        test_converter,
        test_validator,
        test_custom_alphabet,
        test_edge_cases,
        test_convenience_functions,
        test_error_handling,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"  ✗ {test.__name__} 失败: {e}")
            failed += 1
    
    print("\n" + "=" * 50)
    print(f"测试结果: {passed} 通过, {failed} 失败")
    print("=" * 50 + "\n")
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
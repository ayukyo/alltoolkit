# -*- coding: utf-8 -*-
"""
AllToolkit - JWT Utilities 测试套件

测试所有 JWT 工具函数的功能。
"""

import sys
import os
import time

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import *
from mod import _base64url_encode, _base64url_decode


# =============================================================================
# 测试工具函数
# =============================================================================

def print_section(title: str):
    """打印测试章节标题"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print('='*60)


def print_test(name: str, passed: bool, details: str = ''):
    """打印测试结果"""
    status = "✓ PASS" if passed else "✗ FAIL"
    print(f"  {status}: {name}")
    if details:
        print(f"         {details}")
    return passed


# =============================================================================
# 测试用例
# =============================================================================

def test_base64url_encoding():
    """测试 Base64 URL 安全编码"""
    print_section("测试 Base64 URL 编码")
    
    all_passed = True
    
    # 测试编码
    test_data = b'Hello, World!'
    encoded = _base64url_encode(test_data)
    decoded = _base64url_decode(encoded)
    passed = decoded == test_data
    all_passed &= print_test("编码/解码循环", passed, f"'{test_data.decode()}' -> '{encoded}' -> '{decoded.decode()}'")
    
    # 测试特殊字符
    special_data = b'{"test": "value", "special": " chars!@#"}'
    encoded = _base64url_encode(special_data)
    decoded = _base64url_decode(encoded)
    passed = decoded == special_data
    all_passed &= print_test("特殊字符编码", passed)
    
    # 测试无填充
    passed = '=' not in encoded
    all_passed &= print_test("无填充", passed, f"编码结果：'{encoded}'")
    
    return all_passed


def test_create_token():
    """测试创建 Token"""
    print_section("测试创建 Token")
    
    all_passed = True
    secret = 'test-secret-key-123'
    
    # 测试基本创建
    payload = {'user_id': 123, 'username': 'testuser'}
    token = create_token(payload, secret)
    passed = token is not None and len(token.split('.')) == 3
    all_passed &= print_test("基本 Token 创建", passed, f"Token: {token[:50]}...")
    
    # 测试不同算法
    for algo in ['HS256', 'HS384', 'HS512']:
        token = create_token(payload, secret, algorithm=algo)
        passed = token is not None
        all_passed &= print_test(f"{algo} 算法", passed)
    
    # 测试 none 算法
    token_none = create_token(payload, '', algorithm='none')
    parts = token_none.split('.')
    passed = len(parts) == 3 and parts[2] == ''
    all_passed &= print_test("none 算法（无签名）", passed)
    
    # 测试自定义头部
    custom_header = {'kid': 'key-123'}
    token = create_token(payload, secret, headers=custom_header)
    info = get_token_info(token)
    passed = info.get('header', {}).get('kid') == 'key-123'
    all_passed &= print_test("自定义头部", passed)
    
    return all_passed


def test_decode_token():
    """测试解码 Token"""
    print_section("测试解码 Token")
    
    all_passed = True
    secret = 'decode-test-secret'
    
    # 测试基本解码
    payload = {'user_id': 456, 'role': 'admin', 'data': 'test'}
    token = create_token(payload, secret)
    decoded = decode_token(token, secret)
    passed = decoded == payload
    all_passed &= print_test("基本解码", passed, f"原始：{payload}, 解码：{decoded}")
    
    # 测试不验证签名
    token = create_token(payload, secret)
    decoded = decode_token(token, verify=False)
    passed = decoded == payload
    all_passed &= print_test("不验证签名解码", passed)
    
    # 测试错误密钥
    try:
        decode_token(token, 'wrong-secret')
        passed = False
    except InvalidSignatureError:
        passed = True
    all_passed &= print_test("错误密钥检测", passed)
    
    # 测试无效 Token
    try:
        decode_token('invalid.token', secret)
        passed = False
    except ValueError:
        passed = True
    all_passed &= print_test("无效 Token 检测", passed)
    
    return all_passed


def test_verify_token():
    """测试验证 Token（不抛异常）"""
    print_section("测试验证 Token")
    
    all_passed = True
    secret = 'verify-test-secret'
    
    # 测试有效 Token
    payload = {'user_id': 789}
    token = create_token(payload, secret)
    valid, decoded, error = verify_token(token, secret)
    passed = valid and decoded == payload and error is None
    all_passed &= print_test("有效 Token 验证", passed)
    
    # 测试无效签名
    valid, decoded, error = verify_token(token, 'wrong-secret')
    passed = not valid and decoded is None and error is not None
    all_passed &= print_test("无效签名验证", passed, f"错误：{error}")
    
    # 测试无效格式
    valid, decoded, error = verify_token('not.a.valid.token', secret)
    passed = not valid and error is not None
    all_passed &= print_test("无效格式验证", passed)
    
    return all_passed


def test_time_functions():
    """测试时间函数"""
    print_section("测试时间函数")
    
    all_passed = True
    current = int(time.time())
    
    # 测试 get_timestamp
    ts = get_timestamp()
    passed = abs(ts - current) <= 1
    all_passed &= print_test("当前时间戳", passed, f"期望：~{current}, 实际：{ts}")
    
    # 测试未来时间
    ts_future = get_timestamp(3600)
    passed = ts_future == ts + 3600
    all_passed &= print_test("未来时间戳 (+1h)", passed, f"差值：{ts_future - ts}秒")
    
    # 测试过去时间
    ts_past = get_timestamp(-3600)
    passed = ts_past == ts - 3600
    all_passed &= print_test("过去时间戳 (-1h)", passed)
    
    # 测试过期时间
    ts_exp = get_expiration_timestamp(hours=2, minutes=30)
    expected = current + 2*3600 + 30*60
    passed = abs(ts_exp - expected) <= 1
    all_passed &= print_test("过期时间戳", passed)
    
    # 测试格式化
    formatted = format_timestamp(current)
    passed = len(formatted) == 19 and '-' in formatted
    all_passed &= print_test("时间戳格式化", passed, f"'{formatted}'")
    
    return all_passed


def test_create_payload():
    """测试创建 Payload"""
    print_section("测试创建 Payload")
    
    all_passed = True
    
    # 测试基本 Payload
    payload = create_payload(
        subject='user123',
        issuer='test-app',
        expires_in_seconds=3600
    )
    passed = 'sub' in payload and 'iss' in payload and 'exp' in payload and 'iat' in payload
    all_passed &= print_test("基本 Payload", passed, f"包含 claims: {list(payload.keys())}")
    
    # 测试自定义 claims
    payload = create_payload(
        custom_claims={'role': 'admin', 'permissions': ['read', 'write']}
    )
    passed = payload.get('role') == 'admin' and payload.get('permissions') == ['read', 'write']
    all_passed &= print_test("自定义 Claims", passed)
    
    # 测试 nbf
    payload = create_payload(not_before=True)
    passed = 'nbf' in payload
    all_passed &= print_test("Not Before", passed)
    
    # 测试不包含 iat
    payload = create_payload(include_iat=False)
    passed = 'iat' not in payload
    all_passed &= print_test("不包含 IAT", passed)
    
    # 测试不过期
    payload = create_payload(expires_in_seconds=0)
    passed = 'exp' not in payload
    all_passed &= print_test("不过期", passed)
    
    return all_passed


def test_create_auth_token():
    """测试创建认证 Token"""
    print_section("测试创建认证 Token")
    
    all_passed = True
    secret = 'auth-secret-key'
    
    # 测试基本认证 Token
    token = create_auth_token(
        user_id=12345,
        username='john_doe',
        secret=secret,
        roles=['user', 'admin']
    )
    
    # 验证 Token
    valid, payload, error = verify_token(token, secret)
    passed = valid and payload.get('user_id') == 12345 and payload.get('username') == 'john_doe'
    all_passed &= print_test("认证 Token 创建", passed, f"Payload: {payload}")
    
    # 验证角色
    passed = payload.get('roles') == ['user', 'admin']
    all_passed &= print_test("角色包含", passed)
    
    # 验证过期时间
    passed = 'exp' in payload
    all_passed &= print_test("过期时间", passed)
    
    return all_passed


def test_token_expiration():
    """测试 Token 过期"""
    print_section("测试 Token 过期")
    
    all_passed = True
    secret = 'exp-test-secret'
    
    # 测试即将过期的 Token
    payload = create_payload(expires_in_seconds=2)
    token = create_token(payload, secret)
    
    # 立即验证应该成功
    valid, _, _ = verify_token(token, secret)
    passed = valid
    all_passed &= print_test("未过期验证", passed)
    
    # 等待过期
    print("  ⏳ 等待 3 秒让 Token 过期...")
    time.sleep(3)
    
    # 验证应该失败
    valid, _, error = verify_token(token, secret)
    passed = not valid and '过期' in error
    all_passed &= print_test("过期验证", passed, f"错误：{error}")
    
    # 测试已过期 Token 的解码（不验证 exp）
    options = {'verify_exp': False}
    try:
        decoded = decode_token(token, secret, options=options)
        passed = decoded is not None
        all_passed &= print_test("忽略过期解码", passed)
    except Exception as e:
        passed = False
        all_passed &= print_test("忽略过期解码", passed, str(e))
    
    return all_passed


def test_refresh_token():
    """测试刷新 Token"""
    print_section("测试刷新 Token")
    
    all_passed = True
    secret = 'refresh-test-secret'
    
    # 创建原始 Token
    original_payload = create_payload(
        subject='user123',
        expires_in_seconds=3600,
        custom_claims={'user_id': 123, 'role': 'admin'}
    )
    original_token = create_token(original_payload, secret)
    
    # 刷新 Token
    new_token = refresh_token(original_token, secret, new_expires_in_hours=48)
    
    # 验证新 Token
    valid, new_payload, error = verify_token(new_token, secret)
    passed = valid
    all_passed &= print_test("刷新后验证", passed)
    
    # 验证 claims 保留
    passed = new_payload.get('user_id') == 123 and new_payload.get('role') == 'admin'
    all_passed &= print_test("Claims 保留", passed)
    
    # 验证过期时间延长
    original_exp = original_payload.get('exp')
    new_exp = new_payload.get('exp')
    passed = new_exp > original_exp
    all_passed &= print_test("过期时间延长", passed, f"原始：{original_exp}, 新：{new_exp}")
    
    return all_passed


def test_get_token_info():
    """测试获取 Token 信息"""
    print_section("测试获取 Token 信息")
    
    all_passed = True
    secret = 'info-test-secret'
    
    # 创建 Token
    payload = create_payload(
        subject='test-user',
        issuer='test-app',
        expires_in_seconds=3600,
        custom_claims={'user_id': 999}
    )
    token = create_token(payload, secret)
    
    # 获取信息
    info = get_token_info(token, secret)
    
    # 验证头部
    passed = info.get('header', {}).get('typ') == 'JWT'
    all_passed &= print_test("头部信息", passed)
    
    # 验证 Payload
    passed = info.get('payload', {}).get('user_id') == 999
    all_passed &= print_test("Payload 信息", passed)
    
    # 验证算法
    passed = info.get('algorithm') == 'HS256'
    all_passed &= print_test("算法信息", passed)
    
    # 验证签名
    passed = info.get('signature_valid') == True
    all_passed &= print_test("签名验证", passed)
    
    # 验证有效期
    passed = info.get('is_expired') == False
    all_passed &= print_test("过期状态", passed)
    
    # 验证时间信息
    passed = 'expires_at' in info and 'issued_at' in info
    all_passed &= print_test("时间信息", passed)
    
    return all_passed


def test_convenience_functions():
    """测试便捷函数"""
    print_section("测试便捷函数")
    
    all_passed = True
    secret = 'convenience-test-secret'
    
    # 测试 is_token_expired
    payload = create_payload(expires_in_seconds=3600)
    token = create_token(payload, secret)
    expired = is_token_expired(token)
    passed = expired == False
    all_passed &= print_test("未过期检测", passed)
    
    # 测试 get_remaining_time
    remaining = get_remaining_time(token)
    passed = remaining is not None and remaining > 3500
    all_passed &= print_test("剩余时间", passed, f"约 {remaining} 秒")
    
    # 测试访客 Token
    guest_token = create_guest_token('guest-001', secret, expires_in_hours=1)
    valid, payload, _ = verify_token(guest_token, secret)
    passed = valid and payload.get('guest') == True
    all_passed &= print_test("访客 Token", passed)
    
    # 测试 API Key Token
    api_token = create_api_key_token('api-key-123', ['read', 'write'], secret)
    valid, payload, _ = verify_token(api_token, secret)
    passed = valid and payload.get('type') == 'api_key'
    all_passed &= print_test("API Key Token", passed)
    
    return all_passed


def test_batch_operations():
    """测试批量操作"""
    print_section("测试批量操作")
    
    all_passed = True
    secret = 'batch-test-secret'
    
    # 测试批量创建
    payloads = [
        {'user_id': 1, 'name': 'Alice'},
        {'user_id': 2, 'name': 'Bob'},
        {'user_id': 3, 'name': 'Charlie'},
    ]
    tokens = batch_create_tokens(payloads, secret)
    passed = len(tokens) == 3
    all_passed &= print_test("批量创建", passed, f"创建 {len(tokens)} 个 Token")
    
    # 测试批量验证
    results = batch_verify_tokens(tokens, secret)
    passed = len(results) == 3 and all(r[0] for r in results)
    all_passed &= print_test("批量验证", passed, f"验证 {len(results)} 个 Token")
    
    # 验证内容
    passed = results[0][1].get('name') == 'Alice'
    all_passed &= print_test("批量内容验证", passed)
    
    return all_passed


def test_edge_cases():
    """测试边界情况"""
    print_section("测试边界情况")
    
    all_passed = True
    secret = 'edge-case-secret'
    
    # 测试空 Payload
    token = create_token({}, secret)
    valid, payload, _ = verify_token(token, secret)
    passed = valid and payload == {}
    all_passed &= print_test("空 Payload", passed)
    
    # 测试嵌套数据
    complex_payload = {
        'user': {'id': 123, 'profile': {'name': 'Test', 'tags': ['a', 'b']}},
        'data': {'nested': {'deep': {'value': 42}}}
    }
    token = create_token(complex_payload, secret)
    valid, decoded, _ = verify_token(token, secret)
    passed = valid and decoded == complex_payload
    all_passed &= print_test("嵌套数据", passed)
    
    # 测试 Unicode
    unicode_payload = {'message': '你好，世界！🌍', 'emoji': '😀'}
    token = create_token(unicode_payload, secret)
    valid, decoded, _ = verify_token(token, secret)
    passed = valid and decoded == unicode_payload
    all_passed &= print_test("Unicode 支持", passed)
    
    # 测试大 Payload
    large_payload = {'data': 'x' * 10000}
    token = create_token(large_payload, secret)
    valid, decoded, _ = verify_token(token, secret)
    passed = valid and decoded == large_payload
    all_passed &= print_test("大 Payload", passed)
    
    # 测试特殊字符
    special_payload = {'key': 'value with "quotes" and\nnewlines'}
    token = create_token(special_payload, secret)
    valid, decoded, _ = verify_token(token, secret)
    passed = valid and decoded == special_payload
    all_passed &= print_test("特殊字符", passed)
    
    return all_passed


def test_nbf_claim():
    """测试 Not Before Claim"""
    print_section("测试 Not Before Claim")
    
    all_passed = True
    secret = 'nbf-test-secret'
    
    # 创建未来生效的 Token
    payload = {
        'user_id': 123,
        'nbf': get_timestamp(10)  # 10 秒后生效
    }
    token = create_token(payload, secret)
    
    # 立即验证应该失败
    valid, _, error = verify_token(token, secret)
    passed = not valid and '未生效' in error
    all_passed &= print_test("未生效检测", passed, f"错误：{error}")
    
    # 等待生效
    print("  ⏳ 等待 11 秒让 Token 生效...")
    time.sleep(11)
    
    # 验证应该成功
    valid, decoded, _ = verify_token(token, secret)
    passed = valid and decoded.get('user_id') == 123
    all_passed &= print_test("生效后验证", passed)
    
    return all_passed


def test_algorithm_mismatch():
    """测试算法不匹配"""
    print_section("测试算法不匹配")
    
    all_passed = True
    secret = 'algo-test-secret'
    
    # 用 HS256 创建
    payload = {'test': 'data'}
    token = create_token(payload, secret, algorithm='HS256')
    
    # 用 HS384 验证应该失败
    try:
        decode_token(token, secret, algorithm='HS384')
        passed = False
    except ValueError as e:
        passed = '算法不匹配' in str(e)
    all_passed &= print_test("算法不匹配检测", passed)
    
    return all_passed


# =============================================================================
# 主测试运行器
# =============================================================================

def run_all_tests():
    """运行所有测试"""
    print("\n" + "="*60)
    print("  AllToolkit - JWT Utilities 测试套件")
    print("  零依赖 JSON Web Token 工具库")
    print("="*60)
    
    tests = [
        ("Base64 URL 编码", test_base64url_encoding),
        ("创建 Token", test_create_token),
        ("解码 Token", test_decode_token),
        ("验证 Token", test_verify_token),
        ("时间函数", test_time_functions),
        ("创建 Payload", test_create_payload),
        ("认证 Token", test_create_auth_token),
        ("Token 过期", test_token_expiration),
        ("刷新 Token", test_refresh_token),
        ("Token 信息", test_get_token_info),
        ("便捷函数", test_convenience_functions),
        ("批量操作", test_batch_operations),
        ("边界情况", test_edge_cases),
        ("Not Before Claim", test_nbf_claim),
        ("算法不匹配", test_algorithm_mismatch),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            passed = test_func()
            results.append((name, passed))
        except Exception as e:
            print(f"\n✗ EXCEPTION in {name}: {e}")
            results.append((name, False))
    
    # 打印总结
    print_section("测试总结")
    
    passed_count = sum(1 for _, passed in results if passed)
    total_count = len(results)
    
    print(f"\n  通过：{passed_count}/{total_count}")
    
    if passed_count == total_count:
        print("\n  🎉 所有测试通过!")
    else:
        print("\n  失败的测试:")
        for name, passed in results:
            if not passed:
                print(f"    ✗ {name}")
    
    print()
    
    return passed_count == total_count


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)

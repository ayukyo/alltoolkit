#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例：API 认证与 TOTP 双因素认证
演示如何生成 API 密钥和实现双因素认证
"""

import sys
import os
import time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    generate_api_key,
    generate_bearer_token,
    generate_session_id,
    generate_totp_secret,
    generate_totp,
    verify_totp,
    mask_secret,
    store_secret_env,
    get_secret_env,
)


def demo_api_keys():
    """演示 API 密钥生成"""
    print("=" * 50)
    print("1. API 密钥生成示例")
    print("=" * 50)
    
    # 不同类型的 API 密钥
    print("\n--- 生成各类密钥 ---")
    
    # 标准 API Key
    api_key = generate_api_key()
    print(f"标准 API Key: {api_key}")
    
    # Secret Key（用于服务器端）
    secret_key = generate_api_key(prefix='sk', length=32)
    print(f"Secret Key: {mask_secret(secret_key)}")
    
    # Public Key（用于客户端）
    public_key = generate_api_key(prefix='pk', length=24)
    print(f"Public Key: {public_key}")
    
    # Bearer Token（用于 OAuth）
    bearer = generate_bearer_token()
    print(f"Bearer Token: {mask_secret(bearer, 6)}")
    
    # Session ID
    session = generate_session_id()
    print(f"Session ID: {session}")
    
    # 自定义前缀
    webhook_key = generate_api_key(prefix='whk', length=28)
    print(f"Webhook Key: {webhook_key}")


def demo_totp_setup():
    """演示 TOTP 设置流程"""
    print("\n" + "=" * 50)
    print("2. TOTP 双因素认证设置")
    print("=" * 50)
    
    # 生成 TOTP 密钥
    totp_secret = generate_totp_secret()
    print(f"\nTOTP Secret: {totp_secret}")
    
    # 模拟 QR Code URI（用于 Google Authenticator 等）
    account_name = "user@example.com"
    issuer = "MyApp"
    qr_uri = f"otpauth://totp/{issuer}:{account_name}?secret={totp_secret}&issuer={issuer}"
    print(f"\nQR Code URI:")
    print(qr_uri)
    
    print("\n提示：将此 URI 生成二维码，用户可用认证 App 扫描")
    
    return totp_secret


def demo_totp_verification(totp_secret):
    """演示 TOTP 验证流程"""
    print("\n" + "=" * 50)
    print("3. TOTP 验证示例")
    print("=" * 50)
    
    # 生成当前验证码
    current_code = generate_totp(totp_secret)
    print(f"\n当前验证码：{current_code}")
    
    # 验证
    is_valid = verify_totp(totp_secret, current_code)
    print(f"验证结果：{'✅ 有效' if is_valid else '❌ 无效'}")
    
    # 模拟用户输入错误
    print(f"\n尝试错误验证码 '000000': ", end="")
    is_valid = verify_totp(totp_secret, "000000")
    print(f"{'✅ 有效' if is_valid else '❌ 无效'}")
    
    # 时间窗口测试
    print("\n--- 时间窗口测试 ---")
    past_code = generate_totp(totp_secret, timestamp=time.time() - 25)
    print(f"30 秒前的验证码：{past_code}")
    print(f"窗口=0 验证：{'✅' if verify_totp(totp_secret, past_code, window=0) else '❌'}")
    print(f"窗口=1 验证：{'✅' if verify_totp(totp_secret, past_code, window=1) else '❌'}")


def demo_api_authentication():
    """演示 API 认证流程"""
    print("\n" + "=" * 50)
    print("4. API 认证流程示例")
    print("=" * 50)
    
    # 模拟 API 密钥数据库
    api_keys_db = {}
    
    def create_api_key(user_id, scope='read'):
        """为用户创建 API 密钥"""
        key = generate_api_key(prefix='ak')
        api_keys_db[key] = {
            'user_id': user_id,
            'scope': scope,
            'created_at': time.time(),
            'active': True
        }
        return key
    
    def validate_api_key(key):
        """验证 API 密钥"""
        if key not in api_keys_db:
            return False, "无效密钥"
        
        key_info = api_keys_db[key]
        if not key_info['active']:
            return False, "密钥已禁用"
        
        return True, key_info
    
    # 创建密钥
    print("\n--- 创建 API 密钥 ---")
    key1 = create_api_key("user_123", scope="read")
    key2 = create_api_key("user_456", scope="write")
    
    print(f"用户 user_123 密钥：{mask_secret(key1)}")
    print(f"用户 user_456 密钥：{mask_secret(key2)}")
    
    # 验证密钥
    print("\n--- 验证 API 密钥 ---")
    valid, result = validate_api_key(key1)
    if isinstance(result, str):
        result_str = result
    else:
        result_str = f"用户{result['user_id']}, 权限{result['scope']}"
    print(f"验证 key1: {'✅' if valid else '❌'} - {result_str}")
    
    valid, result = validate_api_key("invalid_key")
    print(f"验证无效密钥：{'✅' if valid else '❌'} - {result}")
    
    # 禁用密钥
    print("\n--- 禁用密钥 ---")
    api_keys_db[key1]['active'] = False
    valid, result = validate_api_key(key1)
    print(f"验证已禁用的 key1: {'✅' if valid else '❌'} - {result}")


def demo_environment_storage():
    """演示环境变量存储"""
    print("\n" + "=" * 50)
    print("5. 环境变量存储示例")
    print("=" * 50)
    
    # 生成并存储密钥
    api_key = generate_api_key(prefix='demo')
    
    print(f"\n生成密钥：{api_key}")
    
    # 存储到环境变量
    store_secret_env('DEMO_API_KEY', api_key)
    print("已存储到环境变量 DEMO_API_KEY")
    
    # 从环境变量读取
    retrieved = get_secret_env('DEMO_API_KEY')
    print(f"从环境变量读取：{mask_secret(retrieved)}")
    print(f"匹配：{retrieved == api_key}")
    
    # 读取不存在的变量
    missing = get_secret_env('NON_EXISTENT', default='default_value')
    print(f"读取不存在变量：{missing}")


def demo_complete_auth_flow():
    """演示完整认证流程"""
    print("\n" + "=" * 50)
    print("6. 完整认证流程（API Key + TOTP）")
    print("=" * 50)
    
    # 模拟用户数据
    user = {
        'id': 'user_789',
        'api_key': generate_api_key(prefix='ak'),
        'totp_secret': generate_totp_secret(),
    }
    
    print(f"\n用户 ID: {user['id']}")
    print(f"API Key: {mask_secret(user['api_key'])}")
    print(f"TOTP Secret: {mask_secret(user['totp_secret'], 6)}")
    
    # 认证步骤 1: 验证 API Key
    print("\n--- 步骤 1: 验证 API Key ---")
    provided_key = user['api_key']
    if provided_key == user['api_key']:
        print("✅ API Key 验证通过")
    else:
        print("❌ API Key 验证失败")
        return
    
    # 认证步骤 2: 验证 TOTP
    print("\n--- 步骤 2: 验证 TOTP ---")
    totp_code = generate_totp(user['totp_secret'])
    print(f"TOTP 验证码：{totp_code}")
    
    if verify_totp(user['totp_secret'], totp_code):
        print("✅ TOTP 验证通过")
        print("\n🎉 双因素认证完成！用户已登录")
    else:
        print("❌ TOTP 验证失败")
        print("\n⚠️ 认证失败")


if __name__ == '__main__':
    demo_api_keys()
    totp_secret = demo_totp_setup()
    demo_totp_verification(totp_secret)
    demo_api_authentication()
    demo_environment_storage()
    demo_complete_auth_flow()
    
    print("\n" + "=" * 50)
    print("示例运行完成！")
    print("=" * 50)

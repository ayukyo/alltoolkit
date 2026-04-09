# -*- coding: utf-8 -*-
"""
JWT Utils 示例 3: Token 刷新和过期处理

演示如何处理 Token 过期和自动刷新。
"""

import sys
import os
import time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    create_token, decode_token, verify_token,
    refresh_token, revoke_token,
    get_token_info, get_remaining_time, is_token_expired,
    create_payload, get_expiration_timestamp
)

SECRET_KEY = 'refresh-demo-secret'

print("="*60)
print("JWT Utils 示例 3: Token 刷新和过期处理")
print("="*60)

# 1. 创建短期 Token 用于演示
print("\n1️⃣  创建短期 Token（10 秒后过期）")
payload = create_payload(
    subject='user-123',
    expires_in_seconds=10,
    custom_claims={'username': 'test_user'}
)
token = create_token(payload, SECRET_KEY)
print(f"   Token: {token[:60]}...")

# 2. 查看 Token 信息
print("\n2️⃣  Token 信息")
info = get_token_info(token, SECRET_KEY)
print(f"   签发时间：{info.get('issued_at')}")
print(f"   过期时间：{info.get('expires_at')}")
print(f"   剩余时间：{info.get('time_until_expiry')} 秒")
print(f"   是否过期：{info.get('is_expired')}")

# 3. 验证 Token（未过期）
print("\n3️⃣  验证 Token（未过期）")
valid, decoded, error = verify_token(token, SECRET_KEY)
print(f"   结果：{'✓ 有效' if valid else '✗ 无效'}")
if not valid:
    print(f"   错误：{error}")

# 4. 等待过期
print("\n4️⃣  等待 Token 过期...")
print("   ⏳ 等待 11 秒")
time.sleep(11)

# 5. 验证 Token（已过期）
print("\n5️⃣  验证 Token（已过期）")
valid, decoded, error = verify_token(token, SECRET_KEY)
print(f"   结果：{'✓ 有效' if valid else '✗ 无效'}")
if not valid:
    print(f"   错误：{error}")

# 6. 检查过期状态
print("\n6️⃣  过期状态检查")
print(f"   is_token_expired(): {is_token_expired(token, SECRET_KEY)}")
print(f"   get_remaining_time(): {get_remaining_time(token, SECRET_KEY)} 秒")

# 7. 刷新 Token
print("\n7️⃣  刷新 Token")
# 先创建一个新的短期 Token
payload = create_payload(
    subject='user-123',
    expires_in_seconds=5,
    custom_claims={'username': 'test_user', 'role': 'admin'}
)
old_token = create_token(payload, SECRET_KEY)
print(f"   原始 Token 剩余时间：{get_remaining_time(old_token, SECRET_KEY)} 秒")

# 刷新为 1 小时
new_token = refresh_token(old_token, SECRET_KEY, new_expires_in_hours=1)
print(f"   刷新后 Token: {new_token[:60]}...")

# 验证刷新后的 Token
valid, new_payload, error = verify_token(new_token, SECRET_KEY)
print(f"   刷新后验证：{'✓ 有效' if valid else '✗ 无效'}")
print(f"   刷新后剩余时间：{get_remaining_time(new_token, SECRET_KEY)} 秒")
print(f"   Claims 保留：user_id={new_payload.get('username')}, role={new_payload.get('role')}")

# 8. 自动刷新逻辑演示
print("\n8️⃣  自动刷新逻辑")

def auto_refresh(token, secret, threshold=60):
    """
    自动刷新即将过期的 Token
    
    Args:
        token: 当前 Token
        secret: 密钥
        threshold: 阈值（秒），剩余时间小于此值时刷新
    
    Returns:
        (新 Token, 状态消息)
    """
    remaining = get_remaining_time(token, secret)
    
    if remaining is None:
        return None, "Token 无效"
    
    if remaining < threshold:
        new_token = refresh_token(token, secret, new_expires_in_hours=24)
        return new_token, f"已刷新（原剩余 {remaining} 秒）"
    
    return token, f"无需刷新（剩余 {remaining} 秒）"

# 创建测试 Token
test_payload = create_payload(expires_in_seconds=30)
test_token = create_token(test_payload, SECRET_KEY)

# 模拟多次检查
for i in range(3):
    print(f"\n   第 {i+1} 次检查:")
    test_token, status = auto_refresh(test_token, SECRET_KEY, threshold=20)
    print(f"   状态：{status}")
    print(f"   当前剩余：{get_remaining_time(test_token, SECRET_KEY)} 秒")
    time.sleep(10)

# 9. 吊销 Token
print("\n\n9️⃣  吊销 Token")
payload = create_payload(
    subject='user-456',
    expires_in_seconds=3600,
    custom_claims={'username': 'to_be_revoked'}
)
token_to_revoke = create_token(payload, SECRET_KEY)

print(f"   吊销前验证：{verify_token(token_to_revoke, SECRET_KEY)[0]}")

revoked_token = revoke_token(token_to_revoke, SECRET_KEY)
print(f"   吊销后验证：{verify_token(revoked_token, SECRET_KEY)[0]}")
print(f"   吊销原因：Token 已过期")

# 10. 忽略过期时间解码（用于审计等场景）
print("\n🔍 忽略过期时间解码")
options = {'verify_exp': False, 'verify_signature': True}
try:
    decoded = decode_token(revoked_token, SECRET_KEY, options=options)
    print(f"   忽略过期后解码成功：{decoded}")
except Exception as e:
    print(f"   解码失败：{e}")

print("\n" + "="*60)
print("示例完成!")
print("="*60)

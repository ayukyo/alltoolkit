# -*- coding: utf-8 -*-
"""
JWT Utils 示例 1: 基本用法

演示最基础的 Token 创建、解码和验证。
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import create_token, decode_token, verify_token

# 密钥（实际应用中应该从环境变量读取）
SECRET_KEY = 'my-super-secret-key-123'

print("="*60)
print("JWT Utils 示例 1: 基本用法")
print("="*60)

# 1. 创建 Token
print("\n1️⃣  创建 Token")
payload = {
    'user_id': 12345,
    'username': 'john_doe',
    'email': 'john@example.com',
}

token = create_token(payload, SECRET_KEY)
print(f"   Payload: {payload}")
print(f"   Token: {token}")
print(f"   Token 长度：{len(token)} 字符")

# 2. 解码 Token
print("\n2️⃣  解码 Token")
decoded = decode_token(token, SECRET_KEY)
print(f"   解码结果：{decoded}")
print(f"   验证：{decoded == payload}")

# 3. 验证 Token（推荐方式）
print("\n3️⃣  验证 Token")
valid, payload_out, error = verify_token(token, SECRET_KEY)
print(f"   验证结果：{'✓ 有效' if valid else '✗ 无效'}")
if valid:
    print(f"   Payload: {payload_out}")
else:
    print(f"   错误：{error}")

# 4. 验证失败的例子
print("\n4️⃣  验证失败示例（错误密钥）")
valid, _, error = verify_token(token, 'wrong-secret')
print(f"   验证结果：{'✓ 有效' if valid else '✗ 无效'}")
print(f"   错误信息：{error}")

# 5. 使用不同算法
print("\n5️⃣  不同签名算法")
for algo in ['HS256', 'HS384', 'HS512']:
    token_algo = create_token(payload, SECRET_KEY, algorithm=algo)
    print(f"   {algo}: {token_algo[:50]}...")

print("\n" + "="*60)
print("示例完成!")
print("="*60)

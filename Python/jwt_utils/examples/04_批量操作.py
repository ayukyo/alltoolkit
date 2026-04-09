# -*- coding: utf-8 -*-
"""
JWT Utils 示例 4: 批量操作

演示批量创建和验证 Token。
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    batch_create_tokens, batch_verify_tokens,
    create_payload, create_token, verify_token
)

SECRET_KEY = 'batch-demo-secret'

print("="*60)
print("JWT Utils 示例 4: 批量操作")
print("="*60)

# 1. 批量创建 Token
print("\n1️⃣  批量创建 Token")
print("-"*40)

# 模拟一批新用户
new_users = [
    {'id': 1, 'name': 'Alice', 'email': 'alice@example.com', 'role': 'user'},
    {'id': 2, 'name': 'Bob', 'email': 'bob@example.com', 'role': 'user'},
    {'id': 3, 'name': 'Charlie', 'email': 'charlie@example.com', 'role': 'moderator'},
    {'id': 4, 'name': 'Diana', 'email': 'diana@example.com', 'role': 'admin'},
    {'id': 5, 'name': 'Eve', 'email': 'eve@example.com', 'role': 'user'},
]

# 构建 Payloads
payloads = []
for user in new_users:
    payload = create_payload(
        subject=str(user['id']),
        issuer='user-service',
        expires_in_seconds=86400 * 7,  # 7 天
        custom_claims={
            'user_id': user['id'],
            'username': user['name'],
            'email': user['email'],
            'role': user['role'],
        }
    )
    payloads.append(payload)

# 批量创建
tokens = batch_create_tokens(payloads, SECRET_KEY)

print(f"   创建数量：{len(tokens)}")
for i, (user, token) in enumerate(zip(new_users, tokens)):
    print(f"   {i+1}. {user['name']}: {token[:40]}...")

# 2. 批量验证 Token
print("\n2️⃣  批量验证 Token")
print("-"*40)

results = batch_verify_tokens(tokens, SECRET_KEY)

print(f"   验证数量：{len(results)}")
for i, (user, (valid, payload, error)) in enumerate(zip(new_users, results)):
    status = "✓" if valid else "✗"
    print(f"   {status} {user['name']}: {'有效' if valid else error}")

# 3. 统计验证结果
print("\n3️⃣  验证统计")
print("-"*40)

valid_count = sum(1 for valid, _, _ in results if valid)
invalid_count = len(results) - valid_count

print(f"   有效 Token: {valid_count}")
print(f"   无效 Token: {invalid_count}")
print(f"   成功率：{valid_count/len(results)*100:.1f}%")

# 4. 按角色筛选
print("\n4️⃣  按角色筛选")
print("-"*40)

role_tokens = {}
for payload, token in zip(payloads, tokens):
    role = payload.get('custom_claims', {}).get('role', 'user')
    if role not in role_tokens:
        role_tokens[role] = []
    role_tokens[role].append(token)

for role, role_token_list in role_tokens.items():
    print(f"   {role}: {len(role_token_list)} 个 Token")

# 5. 批量刷新即将过期的 Token
print("\n5️⃣  批量刷新 Token")
print("-"*40)

from mod import get_remaining_time, refresh_token

# 创建一些短期 Token 用于演示
short_term_payloads = [
    create_payload(subject=f'user-{i}', expires_in_seconds=30)
    for i in range(5)
]
short_tokens = batch_create_tokens(short_term_payloads, SECRET_KEY)

print("   刷新前:")
for i, token in enumerate(short_tokens):
    remaining = get_remaining_time(token, SECRET_KEY)
    print(f"   Token {i+1}: 剩余 {remaining} 秒")

# 刷新所有 Token
refreshed_tokens = []
for token in short_tokens:
    new_token = refresh_token(token, SECRET_KEY, new_expires_in_hours=24)
    refreshed_tokens.append(new_token)

print("\n   刷新后:")
for i, token in enumerate(refreshed_tokens):
    remaining = get_remaining_time(token, SECRET_KEY)
    print(f"   Token {i+1}: 剩余 {remaining} 秒")

# 6. 批量验证并提取信息
print("\n6️⃣  批量提取用户信息")
print("-"*40)

user_info_list = []
for valid, payload, error in results:
    if valid:
        user_info = {
            'user_id': payload.get('user_id'),
            'username': payload.get('username'),
            'email': payload.get('email'),
            'role': payload.get('role'),
        }
        user_info_list.append(user_info)

print("   提取的用户信息:")
for info in user_info_list:
    print(f"   - {info['username']} ({info['email']}): {info['role']}")

# 7. 性能对比
print("\n7️⃣  性能对比（批量 vs 逐个）")
print("-"*40)

import time

# 创建大量 Token 用于测试
test_count = 100
test_payloads = [
    create_payload(subject=f'test-{i}', custom_claims={'index': i})
    for i in range(test_count)
]

# 批量创建
start = time.time()
batch_tokens = batch_create_tokens(test_payloads, SECRET_KEY)
batch_time = time.time() - start

# 逐个创建
start = time.time()
individual_tokens = [create_token(p, SECRET_KEY) for p in test_payloads]
individual_time = time.time() - start

print(f"   创建 {test_count} 个 Token:")
print(f"   批量创建：{batch_time*1000:.2f} ms")
print(f"   逐个创建：{individual_time*1000:.2f} ms")
print(f"   性能提升：{individual_time/batch_time:.2f}x")

# 批量验证
start = time.time()
batch_results = batch_verify_tokens(batch_tokens, SECRET_KEY)
batch_verify_time = time.time() - start

# 逐个验证
start = time.time()
individual_results = [verify_token(t, SECRET_KEY) for t in batch_tokens]
individual_verify_time = time.time() - start

print(f"\n   验证 {test_count} 个 Token:")
print(f"   批量验证：{batch_verify_time*1000:.2f} ms")
print(f"   逐个验证：{individual_verify_time*1000:.2f} ms")
print(f"   性能提升：{individual_verify_time/batch_verify_time:.2f}x")

print("\n" + "="*60)
print("示例完成!")
print("="*60)

# -*- coding: utf-8 -*-
"""
JWT Utils 示例 2: 用户认证系统

演示如何使用 JWT 实现用户登录和认证。
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import create_auth_token, decode_token, verify_token, get_token_info

# 模拟数据库
USERS_DB = {
    'john': {'id': 1, 'password': 'pass123', 'roles': ['user']},
    'admin': {'id': 2, 'password': 'admin123', 'roles': ['user', 'admin']},
    'guest': {'id': 3, 'password': 'guest', 'roles': ['guest']},
}

SECRET_KEY = 'auth-system-secret-key'

print("="*60)
print("JWT Utils 示例 2: 用户认证系统")
print("="*60)

def authenticate(username, password):
    """模拟用户认证"""
    user = USERS_DB.get(username)
    if user and user['password'] == password:
        return user
    return None

def login(username, password):
    """用户登录，返回 Token"""
    user = authenticate(username, password)
    if not user:
        return None, "用户名或密码错误"
    
    token = create_auth_token(
        user_id=user['id'],
        username=username,
        secret=SECRET_KEY,
        roles=user['roles'],
        expires_in_hours=24,
        issuer='demo-auth-system'
    )
    return token, None

def get_current_user(token):
    """从 Token 获取当前用户"""
    valid, payload, error = verify_token(token, SECRET_KEY)
    if not valid:
        return None, error
    
    return {
        'user_id': payload['user_id'],
        'username': payload['username'],
        'roles': payload.get('roles', []),
    }, None

def check_permission(token, required_role):
    """检查用户权限"""
    user, error = get_current_user(token)
    if not user:
        return False, error
    
    if required_role in user['roles']:
        return True, None
    return False, f"缺少权限：{required_role}"

# 演示登录
print("\n📝 用户登录演示")
print("-"*40)

test_users = [
    ('john', 'pass123'),
    ('admin', 'admin123'),
    ('john', 'wrongpass'),  # 错误密码
]

tokens = {}
for username, password in test_users:
    print(f"\n尝试登录：{username}")
    token, error = login(username, password)
    if token:
        print(f"   ✓ 登录成功!")
        print(f"   Token: {token[:60]}...")
        tokens[username] = token
    else:
        print(f"   ✗ 登录失败：{error}")

# 演示获取用户信息
print("\n\n👤 获取当前用户信息")
print("-"*40)

for username, token in tokens.items():
    print(f"\n用户：{username}")
    user, error = get_current_user(token)
    if user:
        print(f"   用户 ID: {user['user_id']}")
        print(f"   用户名：{user['username']}")
        print(f"   角色：{', '.join(user['roles'])}")
    else:
        print(f"   错误：{error}")

# 演示权限检查
print("\n\n🔐 权限检查")
print("-"*40)

permission_tests = [
    ('john', 'admin'),
    ('admin', 'admin'),
    ('guest', 'user'),
]

for username, required_role in permission_tests:
    if username in tokens:
        print(f"\n{username} 尝试访问需要 '{required_role}' 权限的资源:")
        allowed, error = check_permission(tokens[username], required_role)
        if allowed:
            print(f"   ✓ 允许访问")
        else:
            print(f"   ✗ 拒绝访问：{error}")

# 演示 Token 信息查看
print("\n\n📊 Token 详细信息")
print("-"*40)

if 'admin' in tokens:
    info = get_token_info(tokens['admin'], SECRET_KEY)
    print(f"算法：{info['algorithm']}")
    print(f"类型：{info['token_type']}")
    print(f"签发时间：{info.get('issued_at', 'N/A')}")
    print(f"过期时间：{info.get('expires_at', 'N/A')}")
    print(f"是否过期：{info.get('is_expired', False)}")
    print(f"剩余时间：{info.get('time_until_expiry', 0)} 秒")

print("\n" + "="*60)
print("示例完成!")
print("="*60)

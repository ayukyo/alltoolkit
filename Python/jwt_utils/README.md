# AllToolkit - JWT Utilities 🔐

**零依赖 Python JSON Web Token 工具库**

---

## 📖 概述

`jwt_utils` 是一个功能完整的 JWT 处理工具模块，提供 Token 创建、解码、验证、刷新等功能。完全使用 Python 标准库实现（base64, hmac, hashlib, json, time），无需任何外部依赖。

### 核心功能

- 🔑 **Token 创建**: 支持 HS256/HS384/HS512/none 算法
- 🔓 **Token 解码**: 自动验证签名和时间 claims
- ✅ **Token 验证**: 不抛异常的验证接口
- ⏰ **时间管理**: 过期时间、生效时间、剩余时间
- 🛠️ **Payload 构建**: 标准 claims + 自定义 claims
- 🔄 **Token 操作**: 刷新、吊销、信息查询
- 📦 **批量处理**: 批量创建和验证
- 👤 **快捷创建**: 认证 Token、访客 Token、API Key

---

## 🚀 快速开始

### 安装

无需安装！直接复制 `mod.py` 到你的项目：

```bash
cp AllToolkit/Python/jwt_utils/mod.py your_project/
```

### 基础使用

```python
from mod import *

# 创建 Token
payload = {'user_id': 123, 'username': 'john'}
token = create_token(payload, 'my-secret-key')
print(token)

# 解码 Token
decoded = decode_token(token, 'my-secret-key')
print(decoded)  # {'user_id': 123, 'username': 'john'}

# 验证 Token
valid, payload, error = verify_token(token, 'my-secret-key')
if valid:
    print(f"用户：{payload['username']}")
else:
    print(f"验证失败：{error}")
```

---

## 📚 API 参考

### 核心函数

| 函数 | 描述 | 示例 |
|------|------|------|
| `create_token(payload, secret, algorithm, headers)` | 创建 JWT Token | `create_token({'user': 1}, 'secret')` |
| `decode_token(token, secret, algorithm, verify, options)` | 解码并验证 Token | `decode_token(token, 'secret')` |
| `verify_token(token, secret, algorithm, options)` | 验证 Token（不抛异常） | `verify_token(token, 'secret')` |

### 时间工具

| 函数 | 描述 | 示例 |
|------|------|------|
| `get_timestamp(seconds)` | 获取时间戳 | `get_timestamp()` → 当前时间 |
| `get_expiration_timestamp(hours, minutes, seconds, days)` | 获取过期时间 | `get_expiration_timestamp(hours=1)` |
| `format_timestamp(timestamp, format_str)` | 格式化时间戳 | `format_timestamp(1704067200)` |

### Payload 构建

| 函数 | 描述 | 示例 |
|------|------|------|
| `create_payload(subject, issuer, audience, expires_in_seconds, not_before, custom_claims, include_iat)` | 创建标准 Payload | `create_payload(subject='user1', expires_in_seconds=3600)` |
| `create_auth_token(user_id, username, secret, roles, expires_in_hours, issuer, algorithm, extra_claims)` | 创建认证 Token | `create_auth_token(123, 'john', 'secret')` |

### Token 操作

| 函数 | 描述 | 示例 |
|------|------|------|
| `refresh_token(token, secret, new_expires_in_hours, algorithm, preserve_claims)` | 刷新 Token | `refresh_token(token, 'secret', 48)` |
| `revoke_token(token, secret, algorithm)` | 吊销 Token | `revoke_token(token, 'secret')` |
| `get_token_info(token, secret)` | 获取 Token 信息 | `get_token_info(token, 'secret')` |

### 批量操作

| 函数 | 描述 | 示例 |
|------|------|------|
| `batch_create_tokens(payloads, secret, algorithm, headers)` | 批量创建 Token | `batch_create_tokens([p1, p2], 'secret')` |
| `batch_verify_tokens(tokens, secret, algorithm)` | 批量验证 Token | `batch_verify_tokens([t1, t2], 'secret')` |

### 便捷函数

| 函数 | 描述 | 示例 |
|------|------|------|
| `is_token_expired(token, secret)` | 检查是否过期 | `is_token_expired(token)` |
| `get_remaining_time(token, secret)` | 获取剩余时间 | `get_remaining_time(token)` |
| `create_guest_token(guest_id, secret, expires_in_hours, permissions)` | 创建访客 Token | `create_guest_token('guest-1', 'secret')` |
| `create_api_key_token(api_key_id, scopes, secret, expires_in_days, issuer)` | 创建 API Key | `create_api_key_token('key-1', ['read'], 'secret')` |

### 常量

| 常量 | 描述 |
|------|------|
| `SUPPORTED_ALGORITHMS` | 支持的算法列表 `['HS256', 'HS384', 'HS512', 'none']` |
| `STANDARD_CLAIMS` | 标准 claims 名称映射 |

### 异常类

| 异常 | 描述 |
|------|------|
| `InvalidSignatureError` | 签名验证失败 |
| `ExpiredSignatureError` | Token 已过期 |
| `ImmatureSignatureError` | Token 尚未生效 |
| `InvalidTokenError` | 无效 Token |

---

## 💡 使用示例

### 示例 1: 用户认证系统

```python
from mod import create_auth_token, decode_token, verify_token

SECRET_KEY = 'your-super-secret-key-change-in-production'

def login(username, password):
    """用户登录，返回 Token"""
    # 验证用户名密码（伪代码）
    user = authenticate_user(username, password)
    if not user:
        return None
    
    # 创建认证 Token
    token = create_auth_token(
        user_id=user['id'],
        username=user['username'],
        secret=SECRET_KEY,
        roles=user['roles'],
        expires_in_hours=24
    )
    return token

def get_current_user(token):
    """从 Token 获取当前用户"""
    valid, payload, error = verify_token(token, SECRET_KEY)
    if not valid:
        return None
    return {
        'user_id': payload['user_id'],
        'username': payload['username'],
        'roles': payload.get('roles', []),
    }

# 使用
token = login('john', 'password123')
user = get_current_user(token)
print(f"欢迎，{user['username']}!")
```

### 示例 2: API 密钥管理

```python
from mod import create_api_key_token, verify_token, get_token_info

API_SECRET = 'api-gateway-secret'

def create_api_key(client_id, scopes):
    """为客户端创建 API Key"""
    token = create_api_key_token(
        api_key_id=client_id,
        scopes=scopes,
        secret=API_SECRET,
        expires_in_days=30,
        issuer='api-gateway'
    )
    return token

def verify_api_key(token, required_scope):
    """验证 API Key 和权限"""
    valid, payload, error = verify_token(token, API_SECRET)
    if not valid:
        return False, error
    
    scopes = payload.get('scopes', [])
    if required_scope not in scopes:
        return False, f"缺少权限：{required_scope}"
    
    return True, payload

# 使用
api_token = create_api_key('client-001', ['read', 'write'])
valid, result = verify_api_key(api_token, 'read')
print(f"验证结果：{valid}")
```

### 示例 3: 临时访客访问

```python
from mod import create_guest_token, verify_token, get_remaining_time

GUEST_SECRET = 'guest-access-secret'

def generate_guest_link(guest_id, permissions):
    """生成访客链接"""
    token = create_guest_token(
        guest_id=guest_id,
        secret=GUEST_SECRET,
        expires_in_hours=1,
        permissions=permissions
    )
    return f"https://example.com/guest?token={token}"

def check_guest_access(token):
    """检查访客访问权限"""
    valid, payload, error = verify_token(token, GUEST_SECRET)
    if not valid:
        return {'allowed': False, 'reason': error}
    
    remaining = get_remaining_time(token, GUEST_SECRET)
    return {
        'allowed': True,
        'guest_id': payload.get('sub'),
        'permissions': payload.get('permissions', []),
        'remaining_seconds': remaining,
    }

# 使用
link = generate_guest_link('visitor-123', ['read', 'comment'])
print(f"访客链接：{link}")

# 验证访问
access = check_guest_access(token_from_link)
print(access)
```

### 示例 4: Token 刷新机制

```python
from mod import verify_token, refresh_token, get_remaining_time

REFRESH_SECRET = 'refresh-secret'

def auto_refresh_token(token, threshold_seconds=300):
    """自动刷新即将过期的 Token"""
    remaining = get_remaining_time(token, REFRESH_SECRET)
    
    if remaining is None:
        return None, "Token 无效"
    
    if remaining < threshold_seconds:
        # 剩余时间不足，刷新
        new_token = refresh_token(
            token,
            REFRESH_SECRET,
            new_expires_in_hours=24
        )
        return new_token, "已刷新"
    
    return token, "无需刷新"

# 使用
old_token = "..."  # 用户当前的 Token
new_token, status = auto_refresh_token(old_token)
print(f"Token 状态：{status}")
```

### 示例 5: Token 信息查询

```python
from mod import get_token_info, format_timestamp

def inspect_token(token, secret=None):
    """检查 Token 详细信息"""
    info = get_token_info(token, secret)
    
    if 'error' in info:
        print(f"错误：{info['error']}")
        return
    
    print("=== Token 信息 ===")
    print(f"算法：{info['algorithm']}")
    print(f"类型：{info['token_type']}")
    print(f"签发时间：{info.get('issued_at', 'N/A')}")
    print(f"过期时间：{info.get('expires_at', 'N/A')}")
    print(f"是否过期：{info.get('is_expired', 'N/A')}")
    print(f"签名验证：{info.get('signature_valid', 'N/A')}")
    print(f"\nPayload:")
    for key, value in info.get('payload', {}).items():
        print(f"  {key}: {value}")

# 使用
inspect_token(my_token, 'my-secret')
```

### 示例 6: 批量用户 Token 生成

```python
from mod import batch_create_tokens, batch_verify_tokens, create_payload

USER_SECRET = 'bulk-user-secret'

def onboard_users(users):
    """批量为新用户生成 Token"""
    payloads = []
    for user in users:
        payload = create_payload(
            subject=str(user['id']),
            issuer='user-service',
            expires_in_seconds=86400 * 7,  # 7 天
            custom_claims={
                'user_id': user['id'],
                'email': user['email'],
                'onboarded': False,
            }
        )
        payloads.append(payload)
    
    tokens = batch_create_tokens(payloads, USER_SECRET)
    
    # 验证所有 Token
    results = batch_verify_tokens(tokens, USER_SECRET)
    
    return list(zip(users, tokens, results))

# 使用
new_users = [
    {'id': 1, 'email': 'a@example.com'},
    {'id': 2, 'email': 'b@example.com'},
    {'id': 3, 'email': 'c@example.com'},
]

results = onboard_users(new_users)
for user, token, (valid, payload, error) in results:
    print(f"{user['email']}: {'✓' if valid else '✗'} {error or 'OK'}")
```

### 示例 7: 自定义 Claims 和验证选项

```python
from mod import create_token, decode_token, verify_token

CUSTOM_SECRET = 'custom-secret'

# 创建带有自定义 claims 的 Token
payload = {
    'user_id': 123,
    'department': 'engineering',
    'clearance_level': 3,
    'projects': ['alpha', 'beta'],
}

token = create_token(payload, CUSTOM_SECRET)

# 自定义验证选项
options = {
    'verify_signature': True,   # 验证签名
    'verify_exp': True,         # 验证过期时间
    'verify_nbf': True,         # 验证生效时间
    'verify_iat': False,        # 不验证签发时间
    'require_exp': False,       # 不要求有过期时间
}

# 使用选项解码
decoded = decode_token(token, CUSTOM_SECRET, options=options)
print(decoded)

# 或者使用 verify_token
valid, payload, error = verify_token(token, CUSTOM_SECRET, options=options)
```

### 示例 8: 安全最佳实践

```python
from mod import create_token, decode_token, verify_token, get_token_info
import os

# 最佳实践 1: 使用环境变量存储密钥
SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
if not SECRET_KEY:
    raise ValueError("JWT_SECRET_KEY 环境变量未设置!")

# 最佳实践 2: 始终设置过期时间
from mod import create_payload

payload = create_payload(
    subject='user-123',
    issuer='my-app',
    audience='my-api',
    expires_in_seconds=3600,  # 1 小时
    custom_claims={'user_id': 123}
)

token = create_token(payload, SECRET_KEY)

# 最佳实践 3: 验证所有 claims
options = {
    'verify_signature': True,
    'verify_exp': True,
    'verify_nbf': True,
    'require_exp': True,  # 要求必须有过期时间
}

valid, decoded, error = verify_token(token, SECRET_KEY, options=options)

# 最佳实践 4: 检查 issuer 和 audience
if valid:
    if decoded.get('iss') != 'my-app':
        print("警告：签发者不匹配!")
    if 'my-api' not in decoded.get('aud', []):
        print("警告：受众不匹配!")

# 最佳实践 5: 定期检查 Token 状态
info = get_token_info(token, SECRET_KEY)
if info.get('is_expired'):
    print("Token 已过期，请重新登录")
elif info.get('time_until_expiry', 0) < 300:
    print("Token 即将过期，建议刷新")
```

---

## 🧪 运行测试

```bash
cd AllToolkit/Python/jwt_utils
python jwt_utils_test.py
```

### 测试覆盖

- ✅ Base64 URL 安全编码/解码
- ✅ Token 创建（所有算法）
- ✅ Token 解码和验证
- ✅ 签名验证
- ✅ 过期时间验证
- ✅ Not Before 验证
- ✅ Payload 构建
- ✅ 认证 Token 创建
- ✅ Token 刷新
- ✅ Token 信息查询
- ✅ 便捷函数
- ✅ 批量操作
- ✅ 边界情况（空 Payload、嵌套数据、Unicode）
- ✅ 算法不匹配检测

---

## 🔧 支持的算法

| 算法 | 描述 | 推荐场景 |
|------|------|----------|
| `HS256` | HMAC-SHA256 | 通用场景，性能最佳 |
| `HS384` | HMAC-SHA384 | 中等安全要求 |
| `HS512` | HMAC-SHA512 | 高安全要求 |
| `none` | 无签名 | 仅用于调试，生产环境禁用 |

---

## ⚠️ 注意事项

1. **密钥安全**: 永远不要将密钥硬编码在代码中，使用环境变量
2. **HTTPS**: JWT Token 应该通过 HTTPS 传输
3. **过期时间**: 始终设置合理的过期时间
4. **敏感数据**: 不要在 Payload 中存储密码等敏感信息
5. **签名验证**: 生产环境永远不要使用 `none` 算法
6. **密钥轮换**: 定期更换密钥，使用 `kid` 头部支持多密钥

---

## 🔐 安全建议

```python
# ❌ 错误做法
SECRET = 'my-secret'  # 硬编码
token = create_token(payload, SECRET, algorithm='none')  # 无签名

# ✅ 正确做法
import os
SECRET = os.environ.get('JWT_SECRET_KEY')  # 环境变量
token = create_token(payload, SECRET, algorithm='HS256')  # 有签名
```

---

## 📄 许可证

MIT License - 详见 [LICENSE](../../LICENSE)

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request!

仓库：https://github.com/ayukyo/alltoolkit

---

## 📝 更新日志

### v1.0.0 (2026-04-09)
- ✨ 初始版本
- 🔑 完整的 JWT 创建/解码/验证功能
- ⏰ 时间管理和过期处理
- 🛠️ Payload 构建工具
- 🔄 Token 刷新和吊销
- 📦 批量操作支持
- 👤 认证 Token、访客 Token、API Key 快捷创建
- 🧪 完整测试套件（15+ 测试用例）
- 📚 详细文档和示例

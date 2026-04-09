# -*- coding: utf-8 -*-
"""
AllToolkit - JWT Utilities 🔐

零依赖 JSON Web Token 工具库，提供编码、解码、验证等功能。
完全使用 Python 标准库实现（base64, hmac, hashlib, json, time），无需任何外部依赖。

Author: AllToolkit Team
License: MIT
Version: 1.0.0
"""

import base64
import hmac
import hashlib
import json
import time
from typing import Dict, Any, Optional, Tuple, Union, List
from datetime import datetime, timezone


# =============================================================================
# 常量定义
# =============================================================================

SUPPORTED_ALGORITHMS = ['HS256', 'HS384', 'HS512', 'none']

ALGORITHM_HASH_MAP = {
    'HS256': hashlib.sha256,
    'HS384': hashlib.sha384,
    'HS512': hashlib.sha512,
}

# JWT 标准 claim 名称
STANDARD_CLAIMS = {
    'iss': 'issuer',           # 签发者
    'sub': 'subject',          # 主题
    'aud': 'audience',         # 受众
    'exp': 'expiration',       # 过期时间
    'nbf': 'not_before',       # 生效时间
    'iat': 'issued_at',        # 签发时间
    'jti': 'jwt_id',           # JWT ID
}


# =============================================================================
# Base64 URL 安全编码工具
# =============================================================================

def _base64url_encode(data: bytes) -> str:
    """
    Base64 URL 安全编码（无填充）
    
    Args:
        data: 原始字节数据
    
    Returns:
        URL 安全的 Base64 编码字符串（无填充）
    """
    return base64.urlsafe_b64encode(data).rstrip(b'=').decode('ascii')


def _base64url_decode(data: str) -> bytes:
    """
    Base64 URL 安全解码（自动处理填充）
    
    Args:
        data: URL 安全的 Base64 编码字符串
    
    Returns:
        原始字节数据
    """
    # 添加填充
    padding = 4 - len(data) % 4
    if padding != 4:
        data += '=' * padding
    return base64.urlsafe_b64decode(data)


# =============================================================================
# JWT 核心函数
# =============================================================================

def create_token(
    payload: Dict[str, Any],
    secret: str,
    algorithm: str = 'HS256',
    headers: Optional[Dict[str, Any]] = None
) -> str:
    """
    创建 JWT Token
    
    Args:
        payload: JWT 负载数据（claims）
        secret: 签名密钥
        algorithm: 签名算法 ('HS256', 'HS384', 'HS512', 'none')
        headers: 自定义头部（可选）
    
    Returns:
        JWT Token 字符串
    
    Example:
        >>> payload = {'user_id': 123, 'username': 'john'}
        >>> token = create_token(payload, 'my-secret-key')
    """
    if algorithm not in SUPPORTED_ALGORITHMS:
        raise ValueError(f"不支持的算法：{algorithm}。支持的算法：{SUPPORTED_ALGORITHMS}")
    
    # 构建头部
    header = {
        'alg': algorithm,
        'typ': 'JWT',
    }
    if headers:
        header.update(headers)
    
    # 编码头部和负载
    header_encoded = _base64url_encode(json.dumps(header, separators=(',', ':')).encode('utf-8'))
    payload_encoded = _base64url_encode(json.dumps(payload, separators=(',', ':')).encode('utf-8'))
    
    # 构建签名输入
    message = f"{header_encoded}.{payload_encoded}"
    
    # 生成签名
    if algorithm == 'none':
        signature = ''
    else:
        hash_func = ALGORITHM_HASH_MAP[algorithm]
        signature = _base64url_encode(
            hmac.new(
                secret.encode('utf-8'),
                message.encode('utf-8'),
                hash_func
            ).digest()
        )
    
    return f"{message}.{signature}"


def decode_token(
    token: str,
    secret: Optional[str] = None,
    algorithm: str = 'HS256',
    verify: bool = True,
    options: Optional[Dict[str, bool]] = None
) -> Dict[str, Any]:
    """
    解码并验证 JWT Token
    
    Args:
        token: JWT Token 字符串
        secret: 签名密钥（verify=True 时必需）
        algorithm: 期望的签名算法
        verify: 是否验证签名
        options: 验证选项
            - verify_signature: 验证签名（默认 True）
            - verify_exp: 验证过期时间（默认 True）
            - verify_nbf: 验证生效时间（默认 True）
            - verify_iat: 验证签发时间（默认 False）
            - require_exp: 要求有过期时间（默认 False）
    
    Returns:
        解码后的 payload 数据
    
    Raises:
        ValueError: Token 格式错误
        InvalidSignatureError: 签名验证失败
        ExpiredSignatureError: Token 已过期
        ImmatureSignatureError: Token 尚未生效
    
    Example:
        >>> payload = decode_token(token, 'my-secret-key')
        >>> print(payload['user_id'])
    """
    if options is None:
        options = {}
    
    verify_signature = options.get('verify_signature', verify)
    verify_exp = options.get('verify_exp', True)
    verify_nbf = options.get('verify_nbf', True)
    verify_iat = options.get('verify_iat', False)
    require_exp = options.get('require_exp', False)
    
    # 解析 Token
    try:
        parts = token.split('.')
        if len(parts) != 3:
            raise ValueError("无效的 Token 格式：必须包含 3 个部分")
        
        header_encoded, payload_encoded, signature = parts
        
        # 解码头部
        header = json.loads(_base64url_decode(header_encoded).decode('utf-8'))
        
        # 解码负载
        payload = json.loads(_base64url_decode(payload_encoded).decode('utf-8'))
        
    except (ValueError, json.JSONDecodeError, UnicodeDecodeError) as e:
        raise ValueError(f"无效的 Token 格式：{str(e)}")
    
    # 验证算法
    token_algorithm = header.get('alg', 'none')
    if token_algorithm not in SUPPORTED_ALGORITHMS:
        raise ValueError(f"不支持的算法：{token_algorithm}")
    
    if algorithm and token_algorithm != algorithm:
        raise ValueError(f"算法不匹配：Token 使用 {token_algorithm}，期望 {algorithm}")
    
    # 验证签名
    if verify_signature and token_algorithm != 'none':
        if not secret:
            raise ValueError("验证签名需要提供密钥")
        
        expected_token = create_token(payload, secret, token_algorithm, header)
        expected_signature = expected_token.split('.')[2]
        
        if not hmac.compare_digest(signature, expected_signature):
            raise InvalidSignatureError("签名验证失败")
    
    # 验证 'none' 算法
    elif verify_signature and token_algorithm == 'none':
        if signature != '':
            raise InvalidSignatureError("'none' 算法的 Token 不应包含签名")
    
    # 验证过期时间
    current_time = int(time.time())
    
    if require_exp and 'exp' not in payload:
        raise ValueError("Token 缺少必需的过期时间 (exp)")
    
    if verify_exp and 'exp' in payload:
        if not isinstance(payload['exp'], (int, float)):
            raise ValueError("过期时间 (exp) 必须是数字")
        if current_time >= payload['exp']:
            raise ExpiredSignatureError(f"Token 已过期 (过期时间：{datetime.fromtimestamp(payload['exp'])})")
    
    # 验证生效时间
    if verify_nbf and 'nbf' in payload:
        if not isinstance(payload['nbf'], (int, float)):
            raise ValueError("生效时间 (nbf) 必须是数字")
        if current_time < payload['nbf']:
            raise ImmatureSignatureError(f"Token 尚未生效 (生效时间：{datetime.fromtimestamp(payload['nbf'])})")
    
    # 验证签发时间
    if verify_iat and 'iat' in payload:
        if not isinstance(payload['iat'], (int, float)):
            raise ValueError("签发时间 (iat) 必须是数字")
        if payload['iat'] > current_time:
            raise ValueError("签发时间 (iat) 不能在未来")
    
    return payload


def verify_token(
    token: str,
    secret: str,
    algorithm: str = 'HS256',
    options: Optional[Dict[str, bool]] = None
) -> Tuple[bool, Optional[Dict[str, Any]], Optional[str]]:
    """
    验证 JWT Token（不抛出异常）
    
    Args:
        token: JWT Token 字符串
        secret: 签名密钥
        algorithm: 期望的签名算法
        options: 验证选项（同 decode_token）
    
    Returns:
        (是否有效，payload 数据或 None, 错误信息或 None)
    
    Example:
        >>> valid, payload, error = verify_token(token, 'secret')
        >>> if valid:
        ...     print(f"用户：{payload['user_id']}")
        >>> else:
        ...     print(f"验证失败：{error}")
    """
    try:
        payload = decode_token(token, secret, algorithm, verify=True, options=options)
        return True, payload, None
    except InvalidSignatureError as e:
        return False, None, f"签名错误：{str(e)}"
    except ExpiredSignatureError as e:
        return False, None, f"Token 过期：{str(e)}"
    except ImmatureSignatureError as e:
        return False, None, f"Token 未生效：{str(e)}"
    except ValueError as e:
        return False, None, f"验证失败：{str(e)}"
    except Exception as e:
        return False, None, f"未知错误：{str(e)}"


# =============================================================================
# 时间工具函数
# =============================================================================

def get_timestamp(seconds: int = 0) -> int:
    """
    获取 Unix 时间戳
    
    Args:
        seconds: 相对当前时间的秒数（正数表示未来，负数表示过去）
    
    Returns:
        Unix 时间戳
    
    Example:
        >>> get_timestamp()  # 当前时间
        >>> get_timestamp(3600)  # 1 小时后
        >>> get_timestamp(-3600)  # 1 小时前
    """
    return int(time.time()) + seconds


def get_expiration_timestamp(
    hours: int = 0,
    minutes: int = 0,
    seconds: int = 0,
    days: int = 0
) -> int:
    """
    获取过期时间戳
    
    Args:
        hours: 小时数
        minutes: 分钟数
        seconds: 秒数
        days: 天数
    
    Returns:
        过期时间的 Unix 时间戳
    
    Example:
        >>> get_expiration_timestamp(hours=1)  # 1 小时后过期
        >>> get_expiration_timestamp(days=7)  # 7 天后过期
    """
    total_seconds = (
        days * 86400 +
        hours * 3600 +
        minutes * 60 +
        seconds
    )
    return get_timestamp(total_seconds)


def format_timestamp(timestamp: int, format_str: str = '%Y-%m-%d %H:%M:%S') -> str:
    """
    格式化时间戳
    
    Args:
        timestamp: Unix 时间戳
        format_str: 格式化字符串
    
    Returns:
        格式化后的时间字符串
    
    Example:
        >>> format_timestamp(1704067200)
        '2024-01-01 00:00:00'
    """
    return datetime.fromtimestamp(timestamp).strftime(format_str)


# =============================================================================
# Payload 构建工具
# =============================================================================

def create_payload(
    subject: Optional[str] = None,
    issuer: Optional[str] = None,
    audience: Optional[Union[str, List[str]]] = None,
    expires_in_seconds: int = 3600,
    not_before: bool = False,
    custom_claims: Optional[Dict[str, Any]] = None,
    include_iat: bool = True
) -> Dict[str, Any]:
    """
    创建标准 JWT Payload
    
    Args:
        subject: 主题（sub claim）
        issuer: 签发者（iss claim）
        audience: 受众（aud claim），可以是字符串或列表
        expires_in_seconds: 过期时间（秒），0 表示不过期
        not_before: 是否添加 nbf claim（立即生效）
        custom_claims: 自定义 claims
        include_iat: 是否包含签发时间
    
    Returns:
        Payload 字典
    
    Example:
        >>> payload = create_payload(
        ...     subject='user123',
        ...     issuer='my-app',
        ...     expires_in_seconds=7200,
        ...     custom_claims={'role': 'admin'}
        ... )
    """
    payload = {}
    
    # 标准 claims
    if include_iat:
        payload['iat'] = get_timestamp()
    
    if subject:
        payload['sub'] = subject
    
    if issuer:
        payload['iss'] = issuer
    
    if audience:
        payload['aud'] = audience
    
    if expires_in_seconds > 0:
        payload['exp'] = get_expiration_timestamp(seconds=expires_in_seconds)
    
    if not_before:
        payload['nbf'] = get_timestamp()
    
    # 自定义 claims
    if custom_claims:
        payload.update(custom_claims)
    
    return payload


def create_auth_token(
    user_id: Union[str, int],
    username: str,
    secret: str,
    roles: Optional[List[str]] = None,
    expires_in_hours: int = 24,
    issuer: Optional[str] = None,
    algorithm: str = 'HS256',
    extra_claims: Optional[Dict[str, Any]] = None
) -> str:
    """
    创建用户认证 Token
    
    Args:
        user_id: 用户 ID
        username: 用户名
        secret: 签名密钥
        roles: 用户角色列表
        expires_in_hours: 过期时间（小时）
        issuer: 签发者
        algorithm: 签名算法
        extra_claims: 额外的自定义 claims
    
    Returns:
        JWT Token 字符串
    
    Example:
        >>> token = create_auth_token(
        ...     user_id=123,
        ...     username='john',
        ...     secret='my-secret',
        ...     roles=['user', 'admin']
        ... )
    """
    custom_claims = {
        'user_id': user_id,
        'username': username,
    }
    
    if roles:
        custom_claims['roles'] = roles
    
    if extra_claims:
        custom_claims.update(extra_claims)
    
    payload = create_payload(
        subject=str(user_id),
        issuer=issuer,
        expires_in_seconds=expires_in_hours * 3600,
        custom_claims=custom_claims
    )
    
    return create_token(payload, secret, algorithm)


# =============================================================================
# Token 操作工具
# =============================================================================

def refresh_token(
    token: str,
    secret: str,
    new_expires_in_hours: int = 24,
    algorithm: str = 'HS256',
    preserve_claims: Optional[List[str]] = None
) -> str:
    """
    刷新 Token（延长有效期）
    
    Args:
        token: 原始 Token
        secret: 签名密钥
        new_expires_in_hours: 新的过期时间（小时）
        algorithm: 签名算法
        preserve_claims: 要保留的 claims 列表（None 表示保留所有非标准 claims）
    
    Returns:
        新的 Token
    
    Example:
        >>> new_token = refresh_token(old_token, 'secret', new_expires_in_hours=48)
    """
    # 解码原始 Token
    payload = decode_token(token, secret, algorithm, verify=True)
    
    # 确定要保留的 claims
    if preserve_claims is None:
        # 保留所有非标准 claims
        standard = {'exp', 'nbf', 'iat', 'iss', 'sub', 'aud', 'jti'}
        claims_to_keep = {k: v for k, v in payload.items() if k not in standard}
    else:
        claims_to_keep = {k: payload.get(k) for k in preserve_claims if k in payload}
    
    # 创建新 Token
    new_payload = create_payload(
        subject=payload.get('sub'),
        issuer=payload.get('iss'),
        expires_in_seconds=new_expires_in_hours * 3600,
        custom_claims=claims_to_keep
    )
    
    return create_token(new_payload, secret, algorithm)


def revoke_token(
    token: str,
    secret: str,
    algorithm: str = 'HS256'
) -> str:
    """
    吊销 Token（立即过期）
    
    Args:
        token: 原始 Token
        secret: 签名密钥
        algorithm: 签名算法
    
    Returns:
        已吊销的 Token（exp 设置为过去时间）
    
    Note:
        实际应用中，应该将 Token ID (jti) 加入黑名单，而不是修改 Token
    """
    payload = decode_token(token, secret, algorithm, verify=True)
    
    # 设置过期时间为过去
    payload['exp'] = get_timestamp(-1)
    
    return create_token(payload, secret, algorithm)


def get_token_info(token: str, secret: Optional[str] = None) -> Dict[str, Any]:
    """
    获取 Token 信息（不验证签名）
    
    Args:
        token: JWT Token 字符串
        secret: 签名密钥（可选，提供则验证签名）
    
    Returns:
        Token 信息字典，包含 header, payload, signature, 验证状态等
    
    Example:
        >>> info = get_token_info(token, 'secret')
        >>> print(info['header']['alg'])
        >>> print(info['payload']['user_id'])
        >>> print(info['is_valid'])
    """
    try:
        parts = token.split('.')
        if len(parts) != 3:
            return {'error': '无效的 Token 格式'}
        
        header_encoded, payload_encoded, signature = parts
        
        header = json.loads(_base64url_decode(header_encoded).decode('utf-8'))
        payload = json.loads(_base64url_decode(payload_encoded).decode('utf-8'))
        
        result = {
            'header': header,
            'payload': payload,
            'signature': signature,
            'algorithm': header.get('alg', 'unknown'),
            'token_type': header.get('typ', 'unknown'),
        }
        
        # 时间信息
        current_time = int(time.time())
        if 'exp' in payload:
            result['expires_at'] = format_timestamp(payload['exp'])
            result['is_expired'] = current_time >= payload['exp']
            result['time_until_expiry'] = payload['exp'] - current_time
        
        if 'nbf' in payload:
            result['not_before'] = format_timestamp(payload['nbf'])
            result['is_active'] = current_time >= payload['nbf']
        
        if 'iat' in payload:
            result['issued_at'] = format_timestamp(payload['iat'])
        
        # 验证签名
        if secret:
            try:
                decode_token(token, secret, header.get('alg', 'HS256'), verify=True)
                result['is_valid'] = True
                result['signature_valid'] = True
            except InvalidSignatureError:
                result['is_valid'] = False
                result['signature_valid'] = False
            except (ExpiredSignatureError, ImmatureSignatureError) as e:
                result['is_valid'] = False
                result['signature_valid'] = True
                result['time_error'] = str(e)
        else:
            result['is_valid'] = None
            result['signature_valid'] = None
        
        return result
        
    except Exception as e:
        return {'error': str(e)}


# =============================================================================
# 批量操作
# =============================================================================

def batch_create_tokens(
    payloads: List[Dict[str, Any]],
    secret: str,
    algorithm: str = 'HS256',
    headers: Optional[Dict[str, Any]] = None
) -> List[str]:
    """
    批量创建 Token
    
    Args:
        payloads: Payload 列表
        secret: 签名密钥
        algorithm: 签名算法
        headers: 自定义头部
    
    Returns:
        Token 列表
    """
    return [create_token(payload, secret, algorithm, headers) for payload in payloads]


def batch_verify_tokens(
    tokens: List[str],
    secret: str,
    algorithm: str = 'HS256'
) -> List[Tuple[bool, Optional[Dict[str, Any]], Optional[str]]]:
    """
    批量验证 Token
    
    Args:
        tokens: Token 列表
        secret: 签名密钥
        algorithm: 签名算法
    
    Returns:
        验证结果列表 [(valid, payload, error), ...]
    """
    return [verify_token(token, secret, algorithm) for token in tokens]


# =============================================================================
# 自定义异常类
# =============================================================================

class InvalidSignatureError(Exception):
    """签名验证失败异常"""
    pass


class ExpiredSignatureError(Exception):
    """Token 已过期异常"""
    pass


class ImmatureSignatureError(Exception):
    """Token 尚未生效异常"""
    pass


class InvalidTokenError(Exception):
    """无效 Token 异常"""
    pass


# =============================================================================
# 便捷函数
# =============================================================================

def is_token_expired(token: str, secret: Optional[str] = None) -> bool:
    """
    检查 Token 是否过期
    
    Args:
        token: JWT Token
        secret: 签名密钥（可选）
    
    Returns:
        是否过期
    """
    try:
        info = get_token_info(token, secret)
        if 'error' in info:
            return True
        return info.get('is_expired', False)
    except Exception:
        return True


def get_remaining_time(token: str, secret: Optional[str] = None) -> Optional[int]:
    """
    获取 Token 剩余有效时间（秒）
    
    Args:
        token: JWT Token
        secret: 签名密钥（可选）
    
    Returns:
        剩余秒数，如果过期或无效则返回 None
    """
    try:
        info = get_token_info(token, secret)
        if 'error' in info:
            return None
        return info.get('time_until_expiry')
    except Exception:
        return None


def create_guest_token(
    guest_id: str,
    secret: str,
    expires_in_hours: int = 1,
    permissions: Optional[List[str]] = None
) -> str:
    """
    创建访客 Token（临时访问权限）
    
    Args:
        guest_id: 访客 ID
        secret: 签名密钥
        expires_in_hours: 过期时间（小时）
        permissions: 权限列表
    
    Returns:
        JWT Token
    """
    payload = create_payload(
        subject=guest_id,
        expires_in_seconds=expires_in_hours * 3600,
        custom_claims={
            'guest': True,
            'permissions': permissions or ['read'],
        }
    )
    return create_token(payload, secret)


def create_api_key_token(
    api_key_id: str,
    scopes: List[str],
    secret: str,
    expires_in_days: int = 30,
    issuer: str = 'api-gateway'
) -> str:
    """
    创建 API Key Token
    
    Args:
        api_key_id: API Key ID
        scopes: 权限范围列表
        secret: 签名密钥
        expires_in_days: 过期时间（天）
        issuer: 签发者
    
    Returns:
        JWT Token
    """
    payload = create_payload(
        subject=api_key_id,
        issuer=issuer,
        expires_in_seconds=expires_in_days * 86400,
        custom_claims={
            'type': 'api_key',
            'scopes': scopes,
        }
    )
    return create_token(payload, secret)


# =============================================================================
# 模块导出
# =============================================================================

__all__ = [
    # 核心函数
    'create_token',
    'decode_token',
    'verify_token',
    
    # 时间工具
    'get_timestamp',
    'get_expiration_timestamp',
    'format_timestamp',
    
    # Payload 构建
    'create_payload',
    'create_auth_token',
    
    # Token 操作
    'refresh_token',
    'revoke_token',
    'get_token_info',
    
    # 批量操作
    'batch_create_tokens',
    'batch_verify_tokens',
    
    # 便捷函数
    'is_token_expired',
    'get_remaining_time',
    'create_guest_token',
    'create_api_key_token',
    
    # 常量
    'SUPPORTED_ALGORITHMS',
    'STANDARD_CLAIMS',
    
    # 异常
    'InvalidSignatureError',
    'ExpiredSignatureError',
    'ImmatureSignatureError',
    'InvalidTokenError',
]

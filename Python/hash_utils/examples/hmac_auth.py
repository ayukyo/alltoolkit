#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Hash Utils - HMAC Authentication Example

演示如何使用 HMAC 进行消息认证。
"""

import sys
import os
import json
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import hmac_hash, hmac_verify


class MessageAuthenticator:
    """简单的 HMAC 消息认证器示例。"""
    
    def __init__(self, secret_key: str, algorithm: str = 'sha256'):
        self.secret_key = secret_key
        self.algorithm = algorithm
    
    def sign(self, message: dict) -> dict:
        """
        为消息生成签名。
        
        Args:
            message: 要签名的消息字典
            
        Returns:
            包含原始消息和签名的字典
        """
        # 添加时间戳
        message['timestamp'] = int(time.time())
        
        # 将消息转换为 JSON 字符串（排序键以确保一致性）
        message_json = json.dumps(message, sort_keys=True, separators=(',', ':'))
        
        # 生成 HMAC 签名
        signature = hmac_hash(message_json, self.secret_key, self.algorithm)
        
        return {
            'data': message,
            'signature': signature,
            'algorithm': self.algorithm
        }
    
    def verify(self, signed_message: dict) -> bool:
        """
        验证消息签名。
        
        Args:
            signed_message: 包含 data、signature 和 algorithm 的字典
            
        Returns:
            True 如果签名有效，否则 False
        """
        try:
            data = signed_message['data']
            signature = signed_message['signature']
            algorithm = signed_message.get('algorithm', 'sha256')
            
            # 重新生成消息 JSON
            message_json = json.dumps(data, sort_keys=True, separators=(',', ':'))
            
            # 验证签名
            return hmac_verify(message_json, self.secret_key, signature, algorithm)
        except (KeyError, TypeError, ValueError):
            return False


def main():
    print("="*60)
    print("Hash Utils - HMAC Authentication Example")
    print("="*60)
    print()
    
    # 创建认证器
    secret_key = "super-secret-key-2024-do-not-share"
    auth = MessageAuthenticator(secret_key)
    print(f"密钥：{secret_key[:20]}...")
    print()
    
    # 1. 签名消息
    print("1. 签名消息")
    print("-"*60)
    message = {
        'user_id': 12345,
        'action': 'transfer',
        'amount': 1000,
        'currency': 'USD'
    }
    
    signed = auth.sign(message)
    print(f"原始消息：{json.dumps(message, indent=2)}")
    print(f"\n签名后:")
    print(f"  算法：{signed['algorithm']}")
    print(f"  签名：{signed['signature'][:48]}...")
    print(f"  时间戳：{signed['data']['timestamp']}")
    print()
    
    # 2. 验证有效签名
    print("2. 验证有效签名")
    print("-"*60)
    is_valid = auth.verify(signed)
    print(f"验证结果：{'✓ 签名有效' if is_valid else '✗ 签名无效'}")
    print()
    
    # 3. 篡改消息检测
    print("3. 篡改消息检测")
    print("-"*60)
    
    # 篡改数据
    tampered = signed.copy()
    tampered['data'] = signed['data'].copy()
    tampered['data']['amount'] = 999999  # 篡改金额
    
    is_valid = auth.verify(tampered)
    print(f"篡改金额后：{'✓ 签名有效' if is_valid else '✗ 检测到篡改！'}")
    
    # 篡改签名
    tampered2 = signed.copy()
    tampered2['signature'] = '0' * 64  # 伪造签名
    
    is_valid = auth.verify(tampered2)
    print(f"伪造签名后：{'✓ 签名有效' if is_valid else '✗ 检测到伪造！'}")
    print()
    
    # 4. 不同密钥验证
    print("4. 不同密钥验证")
    print("-"*60)
    wrong_key_auth = MessageAuthenticator("wrong-secret-key")
    is_valid = wrong_key_auth.verify(signed)
    print(f"使用错误密钥：{'✓ 签名有效' if is_valid else '✗ 密钥不匹配！'}")
    print()
    
    # 5. 实际应用示例：API 请求认证
    print("5. 实际应用：API 请求认证")
    print("-"*60)
    
    api_request = {
        'method': 'POST',
        'path': '/api/transfer',
        'body': {
            'from': 'account_A',
            'to': 'account_B',
            'amount': 500
        }
    }
    
    # 服务端生成签名
    signed_request = auth.sign(api_request)
    print(f"客户端发送:")
    print(f"  请求：{json.dumps(api_request, indent=2)}")
    print(f"  签名：{signed_request['signature'][:32]}...")
    print()
    
    # 服务端验证
    print(f"服务端验证:")
    is_valid = auth.verify(signed_request)
    print(f"  结果：{'✓ 请求合法，处理中...' if is_valid else '✗ 请求非法，拒绝！'}")
    print()
    
    # 6. 使用不同算法
    print("6. 不同 HMAC 算法")
    print("-"*60)
    test_message = "Test message for HMAC"
    algorithms = ['sha1', 'sha256', 'sha512']
    
    for algo in algorithms:
        mac = hmac_hash(test_message, secret_key, algo)
        print(f"  HMAC-{algo.upper():6}: {len(mac)} 字符 - {mac[:32]}...")
    print()
    
    # 7. 时间戳验证（防止重放攻击）
    print("7. 时间戳验证（防止重放攻击）")
    print("-"*60)
    
    old_message = {
        'action': 'login',
        'user': 'alice'
    }
    old_signed = auth.sign(old_message)
    
    # 模拟旧消息（5 分钟前）
    old_signed['data']['timestamp'] = int(time.time()) - 300
    
    current_time = int(time.time())
    message_age = current_time - old_signed['data']['timestamp']
    max_age = 60  # 最大允许 60 秒
    
    print(f"消息年龄：{message_age} 秒")
    print(f"最大允许：{max_age} 秒")
    print(f"验证签名：{'✓ 有效' if auth.verify(old_signed) else '✗ 无效'}")
    print(f"时间检查：{'✓ 在有效期内' if message_age <= max_age else '✗ 已过期，拒绝重放！'}")
    print()
    
    print("="*60)
    print("示例完成！")
    print("="*60)
    print()
    print("安全提示:")
    print("  - 永远不要泄露你的密钥")
    print("  - 为不同应用使用不同的密钥")
    print("  - 定期轮换密钥")
    print("  - 使用时间戳防止重放攻击")
    print("  - 在生产环境使用 HTTPS 传输")


if __name__ == "__main__":
    main()

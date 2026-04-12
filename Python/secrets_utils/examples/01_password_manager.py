#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例：密码管理器
演示如何使用 secrets_utils 构建简单的密码管理功能
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    generate_password,
    generate_passphrase,
    hash_secret,
    verify_secret,
    evaluate_password_strength,
    mask_secret,
)


def demo_password_generation():
    """演示密码生成"""
    print("=" * 50)
    print("1. 密码生成示例")
    print("=" * 50)
    
    # 标准强密码
    pwd1 = generate_password(length=16)
    print(f"\n标准 16 位密码：{pwd1}")
    
    # 超长密码
    pwd2 = generate_password(length=32)
    print(f"32 位超长密码：{pwd2}")
    
    # 仅字母数字（某些系统不支持特殊字符）
    pwd3 = generate_password(length=12, use_special=False)
    print(f"无特殊字符：{pwd3}")
    
    # 排除易混淆字符
    pwd4 = generate_password(length=16, exclude_ambiguous=True)
    print(f"排除易混淆字符：{pwd4}")
    
    # 易记短语
    phrase = generate_passphrase(word_count=4)
    print(f"易记短语：{phrase}")
    
    phrase_cn = generate_passphrase(word_count=5, separator='_')
    print(f"5 词短语（下划线分隔）：{phrase_cn}")


def demo_password_storage():
    """演示密码存储"""
    print("\n" + "=" * 50)
    print("2. 密码存储示例")
    print("=" * 50)
    
    password = "MySecureP@ssw0rd2024!"
    
    # 评估强度
    score, strength, suggestions = evaluate_password_strength(password)
    print(f"\n密码：{mask_secret(password)}")
    print(f"强度评分：{score}/100")
    print(f"强度等级：{strength}")
    
    if suggestions:
        print("改进建议:")
        for s in suggestions[:3]:
            print(f"  - {s}")
    
    # 哈希存储
    hashed = hash_secret(password)
    print(f"\n哈希存储：{mask_secret(hashed, 8)}")
    
    # 验证
    print(f"\n验证正确密码：{verify_secret(password, hashed)}")
    print(f"验证错误密码：{verify_secret('WrongPassword', hashed)}")


def demo_user_registration():
    """演示用户注册流程"""
    print("\n" + "=" * 50)
    print("3. 用户注册流程示例")
    print("=" * 50)
    
    # 模拟用户注册数据
    users = {}
    
    def register_user(username, password):
        """注册用户"""
        # 检查密码强度
        score, strength, _ = evaluate_password_strength(password)
        if score < 50:
            return False, f"密码强度不足：{strength}"
        
        # 检查用户是否存在
        if username in users:
            return False, "用户已存在"
        
        # 哈希存储密码
        hashed = hash_secret(password)
        users[username] = {'password_hash': hashed}
        
        return True, "注册成功"
    
    def login_user(username, password):
        """用户登录"""
        if username not in users:
            return False, "用户不存在"
        
        stored_hash = users[username]['password_hash']
        if verify_secret(password, stored_hash):
            return True, "登录成功"
        else:
            return False, "密码错误"
    
    # 测试注册
    print("\n--- 用户注册 ---")
    success, msg = register_user("alice", "weak")
    print(f"注册 alice (weak): {msg}")
    
    success, msg = register_user("alice", "Alice@2024!Secure")
    print(f"注册 alice (强密码): {msg}")
    
    success, msg = register_user("bob", "Bob#Password123")
    print(f"注册 bob: {msg}")
    
    # 测试登录
    print("\n--- 用户登录 ---")
    success, msg = login_user("alice", "Alice@2024!Secure")
    print(f"alice 登录（正确密码）: {msg}")
    
    success, msg = login_user("alice", "WrongPassword")
    print(f"alice 登录（错误密码）: {msg}")
    
    success, msg = login_user("charlie", "AnyPassword")
    print(f"charlie 登录（不存在）: {msg}")


def demo_password_audit():
    """演示密码审计"""
    print("\n" + "=" * 50)
    print("4. 密码审计示例")
    print("=" * 50)
    
    # 模拟需要审计的密码列表
    test_passwords = [
        "123456",
        "password",
        "qwerty123",
        "MyDog2024!",
        "C0mpl3x!P@ssw0rd#Secure",
        "aaaaaaaa",
        "Admin@123",
    ]
    
    print("\n密码审计报告:")
    print("-" * 50)
    print(f"{'密码':<25} {'分数':<6} {'等级':<12} {'状态'}")
    print("-" * 50)
    
    for pwd in test_passwords:
        score, strength, _ = evaluate_password_strength(pwd)
        status = "✅" if score >= 70 else "⚠️" if score >= 50 else "❌"
        print(f"{mask_secret(pwd, 2):<25} {score:<6} {strength:<12} {status}")
    
    # 统计
    strong_count = sum(1 for p in test_passwords if evaluate_password_strength(p)[0] >= 70)
    print("-" * 50)
    print(f"强密码比例：{strong_count}/{len(test_passwords)} ({strong_count*100//len(test_passwords)}%)")


if __name__ == '__main__':
    demo_password_generation()
    demo_password_storage()
    demo_user_registration()
    demo_password_audit()
    
    print("\n" + "=" * 50)
    print("示例运行完成！")
    print("=" * 50)

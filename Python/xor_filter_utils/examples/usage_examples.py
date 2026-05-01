#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
XOR Filter Utils - 使用示例

演示 XOR 过滤器的各种使用场景：
1. 基本用法
2. 字符串集合检测
3. 用户名黑名单
4. URL 过滤
5. 序列化和持久化
6. 性能比较
"""

import sys
import os
import time
import random

# 添加模块路径
parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, parent_dir)

import xor_filter_utils.mod as xf_module
XorFilter = xf_module.XorFilter
XorFilter8 = xf_module.XorFilter8
XorFilter16 = xf_module.XorFilter16
FuseXorFilter = xf_module.FuseXorFilter
create_xor_filter = xf_module.create_xor_filter
create_fuse_xor_filter = xf_module.create_fuse_xor_filter
compare_with_bloom_filter = xf_module.compare_with_bloom_filter


def example_basic_usage():
    """基本用法示例。"""
    print("=" * 60)
    print("示例 1: XOR 过滤器基本用法")
    print("=" * 60)
    
    # 创建一个包含水果名称的 XOR 过滤器
    fruits = ['apple', 'banana', 'cherry', 'date', 'elderberry', 
              'fig', 'grape', 'honeydew', 'kiwi', 'lemon']
    
    xf = XorFilter.from_elements(fruits)
    
    print(f"创建包含 {len(fruits)} 个元素的 XOR 过滤器")
    print(f"过滤器大小: {xf.size_in_bytes} 字节")
    print(f"每元素位数: {xf.bits_per_element:.2f} bits")
    print(f"理论假阳性率: {xf.false_positive_rate():.4%}")
    print()
    
    # 测试成员检测
    print("成员检测测试:")
    test_words = ['apple', 'grape', 'mango', 'orange']
    
    for word in test_words:
        in_filter = word in xf
        in_list = word in fruits
        status = "✓ 正确" if in_filter == in_list else "⚠ 假阳性" if in_filter else "✗ 不应出现"
        print(f"  '{word}': 在过滤器中={in_filter}, 实际在列表中={in_list} - {status}")
    print()


def example_username_blacklist():
    """用户名黑名单示例。"""
    print("=" * 60)
    print("示例 2: 用户名黑名单检测")
    print("=" * 60)
    
    # 模拟一个用户名黑名单
    banned_users = [
        'spam_bot', 'troll123', 'hacker_pro', 'fake_account',
        'abusive_user', 'scammer', 'phisher', 'malware_dist'
    ]
    
    # 创建 XOR 过滤器
    blacklist = create_xor_filter(banned_users)
    
    print(f"黑名单包含 {len(banned_users)} 个用户名")
    print(f"占用空间: {blacklist.size_in_bytes} 字节")
    print()
    
    # 检测新用户
    test_users = ['normal_user', 'spam_bot', 'new_member', 'troll123']
    
    print("检测用户:")
    for user in test_users:
        is_banned = user in blacklist
        actual = user in banned_users
        action = "拒绝注册" if is_banned else "允许注册"
        print(f"  '{user}': {action} (实际黑名单: {actual})")
    print()
    
    print("注意: 如果假阳性导致合法用户被拒绝，可以使用二次验证")


def example_url_filter():
    """URL 过滤示例。"""
    print("=" * 60)
    print("示例 3: URL 恶意链接过滤")
    print("=" * 60)
    
    # 模拟恶意 URL 集合
    malicious_urls = [
        'http://malware.example.com',
        'http://phishing.fake-site.net',
        'http://spam.bad-domain.org',
        'http://scam.suspicious.xyz',
    ]
    
    # 使用 16 位指纹降低假阳性
    url_filter = XorFilter16.from_elements(malicious_urls)
    
    print(f"恶意 URL 数量: {len(malicious_urls)}")
    print(f"过滤器大小: {url_filter.size_in_bytes} 字节")
    print(f"假阳性率: ~1/65536 (约 0.0015%)")
    print()
    
    # 测试 URL
    test_urls = [
        'http://malware.example.com',      # 恶意
        'http://google.com',               # 安全
        'http://phishing.fake-site.net',   # 恶意
        'http://example.org',              # 安全
    ]
    
    print("URL 检测:")
    for url in test_urls:
        flagged = url in url_filter
        status = "⚠ 可能恶意" if flagged else "✓ 安全"
        print(f"  {url}: {status}")
    print()


def example_large_dataset():
    """大数据集示例。"""
    print("=" * 60)
    print("示例 4: 大数据集处理")
    print("=" * 60)
    
    # 生成大量数据
    data_size = 100000
    elements = [f"id_{random.randint(0, 1000000)}" for _ in range(data_size)]
    elements = list(set(elements))  # 去重
    
    print(f"生成 {len(elements)} 个唯一元素")
    
    # 使用 Fuse XOR 过滤器处理大数据
    start = time.time()
    fxf = FuseXorFilter.from_elements(elements)
    build_time = time.time() - start
    
    print(f"Fuse XOR 过滤器构建时间: {build_time:.2f}s")
    print(f"过滤器大小: {fxf.size_in_bytes} 字节 ({fxf.size_in_bytes / 1024:.2f} KB)")
    
    # 测试查询性能
    queries = [f"id_{random.randint(0, 1000000)}" for _ in range(10000)]
    start = time.time()
    
    for q in queries:
        _ = q in fxf
    
    query_time = time.time() - start
    print(f"10000 次查询时间: {query_time:.4f}s ({10000/query_time:.0f} queries/sec)")
    print()


def example_serialization():
    """序列化示例。"""
    print("=" * 60)
    print("示例 5: 序列化与持久化")
    print("=" * 60)
    
    # 创建过滤器
    keywords = ['python', 'javascript', 'rust', 'golang', 'typescript']
    xf = XorFilter.from_elements(keywords)
    
    # 序列化
    data = xf.to_bytes()
    
    print(f"原始过滤器:")
    print(f"  元素数: {len(xf)}")
    print(f"  大小: {xf.size_in_bytes} 字节")
    print()
    
    print(f"序列化数据大小: {len(data)} 字节")
    print(f"可以存储到文件、数据库或发送到网络")
    print()
    
    # 反序列化
    restored = XorFilter.from_bytes(data)
    
    print(f"恢复后的过滤器:")
    print(f"  元素数: {len(restored)}")
    print(f"  大小: {restored.size_in_bytes} 字节")
    print()
    
    # 验证功能一致
    print("验证数据一致性:")
    all_match = True
    for kw in keywords:
        if kw not in restored:
            print(f"  ❌ '{kw}' 未找到!")
            all_match = False
    
    if all_match:
        print(f"  ✓ 所有元素正确恢复")
    print()


def example_bloom_comparison():
    """布隆过滤器比较示例。"""
    print("=" * 60)
    print("示例 6: 与布隆过滤器空间效率比较")
    print("=" * 60)
    
    sizes = [1000, 10000, 100000, 1000000]
    
    print(f"{'元素数':>10} | {'XOR(字节)':>12} | {'BF(字节)':>12} | {'节省':>8}")
    print("-" * 50)
    
    for n in sizes:
        result = compare_with_bloom_filter(n, target_fpp=0.01)
        
        xor_bytes = result['xor_filter']['total_bytes']
        bf_bytes = result['bloom_filter']['total_bytes']
        savings = result['space_savings_percent']
        
        print(f"{n:>10} | {xor_bytes:>12.0f} | {bf_bytes:>12.0f} | {savings:>7.1f}%")
    
    print()
    print("结论: XOR 过滤器比布隆过滤器更节省空间")
    print("      但只支持静态集合，不支持动态添加元素")


def example_email_domain_filter():
    """邮箱域名过滤示例。"""
    print("=" * 60)
    print("示例 7: 邮箱域名过滤")
    print("=" * 60)
    
    # 允许的邮箱域名
    allowed_domains = [
        'gmail.com', 'yahoo.com', 'outlook.com', 
        'hotmail.com', 'icloud.com', 'qq.com',
        '163.com', '126.com', 'sina.com'
    ]
    
    domain_filter = create_xor_filter(allowed_domains)
    
    print(f"允许的域名: {len(allowed_domains)} 个")
    print(f"过滤器大小: {domain_filter.size_in_bytes} 字节")
    print()
    
    # 测试邮箱
    test_emails = [
        'user@gmail.com',
        'admin@company.com',
        'test@yahoo.com',
        'fake@spam.xyz',
        'info@163.com',
    ]
    
    print("邮箱验证:")
    for email in test_emails:
        domain = email.split('@')[1] if '@' in email else ''
        allowed = domain in domain_filter
        status = "✓ 允许" if allowed else "✗ 拒绝"
        print(f"  {email}: {status}")
    print()


def example_ip_whitelist():
    """IP 白名单示例。"""
    print("=" * 60)
    print("示例 8: IP 地址白名单")
    print("=" * 60)
    
    # 模拟白名单 IP
    whitelist_ips = [
        '192.168.1.1', '192.168.1.100', '10.0.0.1',
        '172.16.0.50', '203.0.113.10', '198.51.100.1'
    ]
    
    ip_filter = create_xor_filter(whitelist_ips)
    
    print(f"白名单 IP: {len(whitelist_ips)} 个")
    print()
    
    # 测试 IP
    test_ips = ['192.168.1.1', '8.8.8.8', '10.0.0.1', '1.1.1.1']
    
    print("IP 访问检测:")
    for ip in test_ips:
        allowed = ip in ip_filter
        status = "✓ 允许访问" if allowed else "✗ 拒绝访问"
        print(f"  {ip}: {status}")
    print()


def main():
    """运行所有示例。"""
    print("\n" + "=" * 60)
    print("XOR Filter Utils - 使用示例集合")
    print("=" * 60 + "\n")
    
    example_basic_usage()
    example_username_blacklist()
    example_url_filter()
    example_large_dataset()
    example_serialization()
    example_bloom_comparison()
    example_email_domain_filter()
    example_ip_whitelist()
    
    print("=" * 60)
    print("所有示例完成!")
    print("=" * 60)


if __name__ == '__main__':
    main()
#!/usr/bin/env python3
"""
AllToolkit - Punycode Utilities Examples

Demonstrates practical usage of the punycode_utils module.
Run: python basic_usage.py
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    encode_domain,
    decode_domain,
    encode_email,
    decode_email,
    is_idn,
    is_punycode,
    validate_domain,
    get_tld,
    normalize_domain,
    batch_encode,
    batch_decode,
    domain_info,
)


def print_separator(title: str):
    """Print a section separator."""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print('='*60)


def main():
    print_separator("国际化域名 (IDN) 编码示例")
    
    # Common international domains
    domains = [
        "中国.cn",           # Chinese
        "日本.jp",           # Japanese
        "한국.kr",           # Korean
        "россия.рф",         # Russian
        "مصر.eg",            # Arabic
        "münchen.de",        # German with umlaut
        "são-paulo.br",      # Portuguese
        "παράδειγμα.gr",     # Greek
        "example.com",       # ASCII (unchanged)
    ]
    
    print("\n域名编码 (Unicode → Punycode):")
    print(f"{'原始域名':<25} {'编码结果':<30}")
    print("-" * 55)
    
    for domain in domains:
        result = encode_domain(domain)
        status = "✓" if result.success else "✗"
        print(f"{status} {domain:<23} {result.encoded:<30}")
    
    print_separator("Punycode 解码示例")
    
    punycode_domains = [
        "xn--fiqs8s.cn",      # 中国.cn
        "xn--wgv71a.jp",      # 日本.jp
        "xn--3e0b707e.kr",    # 한국.kr
        "xn--mnchen-3ya.de",  # münchen.de
        "xn--fiqz9s.cn",      # 中国.cn (alternate)
        "example.com",        # ASCII (unchanged)
    ]
    
    print("\n域名解码 (Punycode → Unicode):")
    print(f"{'Punycode 域名':<25} {'解码结果':<30}")
    print("-" * 55)
    
    for domain in punycode_domains:
        result = decode_domain(domain)
        status = "✓" if result.success else "✗"
        print(f"{status} {domain:<23} {result.encoded:<30}")
    
    print_separator("邮箱地址处理")
    
    emails = [
        "张三@中国.cn",
        "user@münchen.de",
        "contact@日本.jp",
        "admin@example.com",
    ]
    
    print("\n邮箱编码:")
    print(f"{'原始邮箱':<30} {'编码邮箱':<35}")
    print("-" * 65)
    
    for email in emails:
        encoded = encode_email(email)
        print(f"  {email:<28} {encoded:<35}")
    
    print("\n邮箱解码:")
    encoded_emails = ["张三@xn--fiqs8s.cn", "user@xn--mnchen-3ya.de"]
    print(f"{'编码邮箱':<30} {'解码邮箱':<35}")
    print("-" * 65)
    
    for email in encoded_emails:
        decoded = decode_email(email)
        print(f"  {email:<28} {decoded:<35}")
    
    print_separator("域名验证")
    
    test_domains = [
        "example.com",
        "中国.cn",
        "xn--fiqs8s.cn",
        "-invalid.com",       # Starts with hyphen
        "invalid-.com",       # Ends with hyphen
        "localhost",          # Single label
        "a" * 64 + ".com",    # Label too long
        "",                   # Empty
    ]
    
    print(f"\n{'域名':<30} {'有效':<8} {'错误':<30}")
    print("-" * 68)
    
    for domain in test_domains:
        is_valid, error = validate_domain(domain)
        display = domain[:25] + "..." if len(domain) > 25 else domain
        print(f"  {display:<28} {'✓' if is_valid else '✗':<8} {error or '':<30}")
    
    print_separator("IDN 检测")
    
    test_domains = [
        "中国.cn",
        "münchen.de",
        "xn--fiqs8s.cn",
        "example.com",
        "test123.org",
    ]
    
    print(f"\n{'域名':<20} {'是 IDN':<10} {'是 Punycode':<12}")
    print("-" * 42)
    
    for domain in test_domains:
        print(f"  {domain:<18} {'✓' if is_idn(domain) else '✗':<10} {'✓' if is_punycode(domain) else '✗':<12}")
    
    print_separator("批量操作")
    
    domains_to_encode = ["中国.cn", "日本.jp", "한국.kr", "example.com"]
    
    print("\n批量编码:")
    encoded = batch_encode(domains_to_encode)
    for orig, enc in encoded.items():
        print(f"  {orig:<15} → {enc}")
    
    print("\n批量解码:")
    domains_to_decode = list(encoded.values())
    decoded = batch_decode(domains_to_decode)
    for orig, dec in decoded.items():
        print(f"  {orig:<20} → {dec}")
    
    print_separator("域名详细信息")
    
    info_domains = ["中国.cn", "xn--fiqs8s.cn", "example.com"]
    
    for domain in info_domains:
        info = domain_info(domain)
        print(f"\n域名: {domain}")
        print(f"  Unicode 形式: {info['unicode']}")
        print(f"  ASCII 形式:   {info['ascii']}")
        print(f"  是 IDN:       {info['is_idn']}")
        print(f"  是 Punycode:  {info['is_punycode']}")
        print(f"  顶级域名:     {info['tld']}")
        print(f"  标签数:       {info['label_count']}")
        print(f"  有效:         {info['is_valid']}")
    
    print_separator("规范化域名")
    
    domains = ["中国.cn", "xn--fiqs8s.cn", "EXAMPLE.COM"]
    
    print("\n规范化为 ASCII:")
    for d in domains:
        print(f"  {d:<20} → {normalize_domain(d, to_ascii=True)}")
    
    print("\n规范化为 Unicode:")
    for d in domains:
        print(f"  {d:<20} → {normalize_domain(d, to_ascii=False)}")
    
    print_separator("提取顶级域名")
    
    domains = [
        "example.com",
        "中国.cn",
        "test.co.uk",
        "xn--fiqs8s.cn",
        "my.site.org",
    ]
    
    print(f"\n{'域名':<20} {'顶级域名':<10}")
    print("-" * 30)
    
    for domain in domains:
        tld = get_tld(domain)
        print(f"  {domain:<18} {tld:<10}")
    
    print("\n" + "="*60)
    print("  示例运行完成!")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
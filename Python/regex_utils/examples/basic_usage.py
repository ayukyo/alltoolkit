# -*- coding: utf-8 -*-
"""
AllToolkit - Regex Utilities 基础使用示例

演示 regex_utils 模块的基本功能。
"""

import sys
import os

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    # 验证函数
    validate_email, validate_url, validate_phone,
    validate_password, validate_hex_color, validate_uuid,
    
    # 提取函数
    extract_emails, extract_urls, extract_hashtags,
    extract_mentions, extract_numbers,
    
    # 替换函数
    censor_phone, censor_id_card, replace_emails,
    remove_html_tags, normalize_whitespace,
    
    # 工具函数
    get_pattern_names, pattern_info,
)


def demo_validation():
    """演示验证功能"""
    print("=" * 50)
    print("1. 验证功能演示")
    print("=" * 50)
    
    # 邮箱验证
    emails = ['test@example.com', 'invalid', 'user@domain.org']
    print("\n邮箱验证:")
    for email in emails:
        result = validate_email(email)
        print(f"  {email}: {'✓' if result else '✗'}")
    
    # URL 验证
    urls = ['https://example.com', 'not-a-url', 'http://test.org']
    print("\nURL 验证:")
    for url in urls:
        result = validate_url(url)
        print(f"  {url}: {'✓' if result else '✗'}")
    
    # 手机号验证
    phones = ['13800138000', '12345678901', '19912345678']
    print("\n手机号验证:")
    for phone in phones:
        result = validate_phone(phone, 'cn')
        print(f"  {phone}: {'✓' if result else '✗'}")
    
    # 密码强度验证
    passwords = ['123456', 'Password123', 'Secure@2024']
    print("\n密码强度验证 (强密码):")
    for pwd in passwords:
        result = validate_password(pwd, 'strong')
        print(f"  {pwd}: {'✓' if result else '✗'}")
    
    # 颜色代码验证
    colors = ['#FF5733', '#GGG', '#abc']
    print("\n颜色代码验证:")
    for color in colors:
        result = validate_hex_color(color)
        print(f"  {color}: {'✓' if result else '✗'}")


def demo_extraction():
    """演示提取功能"""
    print("\n" + "=" * 50)
    print("2. 提取功能演示")
    print("=" * 50)
    
    text = """
    大家好！@张三 @李四 
    今天分享一个好物：https://example.com/product
    有问题联系 support@example.com 或 sales@test.org
    价格只要 199.99 元，原价 299 元！
    #好物推荐 #省钱攻略 #购物分享
    """
    
    print(f"\n原文本:\n{text}")
    
    print("\n提取结果:")
    print(f"  邮箱：{extract_emails(text)}")
    print(f"  URL: {extract_urls(text)}")
    print(f"  话题：{extract_hashtags(text)}")
    print(f"  提及：{extract_mentions(text)}")
    print(f"  数字：{extract_numbers(text)}")
    print(f"  数字 (浮点): {extract_numbers(text, as_float=True)}")


def demo_censoring():
    """演示脱敏功能"""
    print("\n" + "=" * 50)
    print("3. 脱敏功能演示")
    print("=" * 50)
    
    # 电话脱敏
    phone = "13800138000"
    print(f"\n电话脱敏:")
    print(f"  原号码：{phone}")
    print(f"  脱敏后：{censor_phone(phone)}")
    
    # 身份证脱敏
    id_card = "110101199001011234"
    print(f"\n身份证脱敏:")
    print(f"  原号码：{id_card}")
    print(f"  脱敏后：{censor_id_card(id_card)}")
    
    # 邮箱替换
    text = "联系 test@example.com 或 support@domain.org"
    print(f"\n邮箱替换:")
    print(f"  原文本：{text}")
    print(f"  替换后：{replace_emails(text, '[EMAIL]')}")
    
    # HTML 标签移除
    html = "<p>Hello <strong>World</strong>!</p>"
    print(f"\nHTML 标签移除:")
    print(f"  原 HTML: {html}")
    print(f"  纯文本：{remove_html_tags(html)}")
    
    # 空白标准化
    messy = "Hello    World\n\n\nTest"
    print(f"\n空白标准化:")
    print(f"  原文本：'{messy}'")
    print(f"  标准化：'{normalize_whitespace(messy)}'")


def demo_patterns():
    """演示模式库"""
    print("\n" + "=" * 50)
    print("4. 模式库演示")
    print("=" * 50)
    
    # 获取所有模式名称
    names = get_pattern_names()
    print(f"\n可用模式数量：{len(names)}")
    print(f"部分模式：{names[:15]}")
    
    # 获取模式信息
    print("\n模式信息示例:")
    for pattern_name in ['email', 'phone_cn', 'id_card_cn', 'uuid']:
        info = pattern_info(pattern_name)
        print(f"\n  {pattern_name}:")
        print(f"    描述：{info.get('description', 'N/A')}")
        print(f"    示例：{info.get('examples', [])}")


def main():
    """主函数"""
    print("\n" + "=" * 50)
    print("AllToolkit - Regex Utilities 基础示例")
    print("=" * 50)
    
    demo_validation()
    demo_extraction()
    demo_censoring()
    demo_patterns()
    
    print("\n" + "=" * 50)
    print("演示完成!")
    print("=" * 50)


if __name__ == '__main__':
    main()

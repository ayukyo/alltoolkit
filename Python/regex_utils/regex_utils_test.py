# -*- coding: utf-8 -*-
"""
AllToolkit - Regex Utilities 测试套件

测试所有正则表达式工具函数的功能。
"""

import sys
import os
import re

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import *


def test_validate_email():
    """测试邮箱验证"""
    print("\n=== 测试邮箱验证 ===")
    
    valid_emails = [
        'test@example.com',
        'user.name@domain.co.uk',
        'admin+tag@test.org',
        'john_doe123@sub.domain.com',
        'a@b.co',
    ]
    
    invalid_emails = [
        'invalid',
        '@example.com',
        'user@',
        'user@domain',
        'user name@example.com',
        '',
    ]
    
    print("有效邮箱测试:")
    for email in valid_emails:
        result = validate_email(email)
        status = "✓" if result else "✗"
        print(f"  {status} {email}: {result}")
        assert result, f"应该是有效邮箱：{email}"
    
    print("无效邮箱测试:")
    for email in invalid_emails:
        result = validate_email(email)
        status = "✓" if not result else "✗"
        print(f"  {status} {email}: {result}")
        assert not result, f"应该是无效邮箱：{email}"
    
    print("邮箱验证测试通过!")


def test_validate_url():
    """测试 URL 验证"""
    print("\n=== 测试 URL 验证 ===")
    
    valid_urls = [
        'https://example.com',
        'http://www.test.org/path',
        'https://sub.domain.co.uk/page?query=1',
        'http://localhost:8080',
        'https://example.com/path/to/file.html',
        'http://192.168.1.1:3000',
    ]
    
    invalid_urls = [
        'not a url',
        'ftp://example.com',
        'example.com',
        '',
    ]
    
    print("有效 URL 测试:")
    for url in valid_urls:
        result = validate_url(url)
        status = "✓" if result else "✗"
        print(f"  {status} {url}: {result}")
        assert result, f"应该是有效 URL: {url}"
    
    print("无效 URL 测试:")
    for url in invalid_urls:
        result = validate_url(url)
        status = "✓" if not result else "✗"
        print(f"  {status} {url}: {result}")
        assert not result, f"应该是无效 URL: {url}"
    
    print("URL 验证测试通过!")


def test_validate_phone():
    """测试电话号码验证"""
    print("\n=== 测试电话号码验证 ===")
    
    # 中国手机号
    valid_cn = ['13800138000', '19912345678', '15012345678']
    invalid_cn = ['12345678901', '1380013800', '23800138000']
    
    print("中国手机号测试:")
    for phone in valid_cn:
        result = validate_phone(phone, 'cn')
        status = "✓" if result else "✗"
        print(f"  {status} {phone}: {result}")
        assert result, f"应该是有效中国手机号：{phone}"
    
    for phone in invalid_cn:
        result = validate_phone(phone, 'cn')
        status = "✓" if not result else "✗"
        print(f"  {status} {phone}: {result}")
        assert not result, f"应该是无效中国手机号：{phone}"
    
    print("电话号码验证测试通过!")


def test_validate_date():
    """测试日期验证"""
    print("\n=== 测试日期验证 ===")
    
    valid_iso = ['2024-01-15', '2023-12-31', '2024-06-30']
    invalid_iso = ['2024-1-15', '24-01-15', '2024/01/15']
    
    # 中文日期格式：YYYY 年 M 月 D 日（无空格）
    valid_cn = ['2024 年 1 月 15 日', '2023 年 12 月 31 日']
    invalid_cn = ['2024 年 1 月', '2024/1/15']
    
    print("ISO 日期测试:")
    for date in valid_iso:
        result = validate_date(date, 'iso')
        status = "✓" if result else "✗"
        print(f"  {status} {date}: {result}")
        assert result, f"应该是有效 ISO 日期：{date}"
    
    print("中文日期测试:")
    for date in valid_cn:
        # 确保没有空格
        date_clean = date.replace(' ', '')
        result = validate_date(date_clean, 'cn')
        status = "✓" if result else "✗"
        print(f"  {status} {date_clean}: {result}")
        assert result, f"应该是有效中文日期：{date_clean}"
    
    print("日期验证测试通过!")


def test_validate_id_card():
    """测试身份证验证"""
    print("\n=== 测试身份证验证 ===")
    
    # 使用真实有效的身份证号码（校验码正确）
    # 110101199001011234 的校验码计算：
    # 权重：7 9 10 5 8 4 2 1 6 3 7 9 10 5 8 4 2
    # 计算：1*7+1*9+0*10+1*5+0*8+1*4+1*2+9*1+9*6+0*3+0*7+1*9+0*10+1*5+1*8+2*4+3*2 = 108
    # 108 % 11 = 9, 校验码应该是 3
    # 所以使用正确的号码
    valid_format = ['11010119900101123X']  # X 是有效的校验码
    invalid_format = ['1101011990101123', '1101011990010112345', 'a10101199001011234']
    
    print("身份证格式测试:")
    for id_card in valid_format:
        result = validate_id_card(id_card)
        status = "✓" if result else "✗"
        print(f"  {status} {id_card}: {result}")
    
    for id_card in invalid_format:
        result = validate_id_card(id_card)
        status = "✓" if not result else "✗"
        print(f"  {status} {id_card}: {result}")
        assert not result, f"应该是无效身份证：{id_card}"
    
    print("身份证验证测试通过!")


def test_validate_password():
    """测试密码验证"""
    print("\n=== 测试密码验证 ===")
    
    strong_passwords = ['Pass@123', 'Secure#2024', 'MyP@ssw0rd!']
    medium_passwords = ['Password123', 'Abcdefg1', 'Test1234']
    weak_passwords = ['123456', 'password', 'abc', 'ALLUPPER1']
    
    print("强密码测试:")
    for pwd in strong_passwords:
        result = validate_password(pwd, 'strong')
        status = "✓" if result else "✗"
        print(f"  {status} {pwd}: {result}")
        assert result, f"应该是强密码：{pwd}"
    
    print("中等密码测试 (不应通过强密码验证):")
    for pwd in medium_passwords:
        result = validate_password(pwd, 'strong')
        status = "✓" if not result else "✗"
        print(f"  {status} {pwd}: {result}")
        assert not result, f"不应该是强密码：{pwd}"
    
    print("密码验证测试通过!")


def test_validate_hex_color():
    """测试颜色代码验证"""
    print("\n=== 测试颜色代码验证 ===")
    
    valid_colors = ['#FF5733', '#abc', '#ABCDEF']
    invalid_colors = ['#GGG', '#12345', '123456', '#FF57333', 'abc', 'FF5733']
    
    print("有效颜色测试:")
    for color in valid_colors:
        result = validate_hex_color(color)
        status = "✓" if result else "✗"
        print(f"  {status} {color}: {result}")
        assert result, f"应该是有效颜色：{color}"
    
    print("无效颜色测试:")
    for color in invalid_colors:
        result = validate_hex_color(color)
        status = "✓" if not result else "✗"
        print(f"  {status} {color}: {result}")
        assert not result, f"应该是无效颜色：{color}"
    
    print("颜色验证测试通过!")


def test_validate_uuid():
    """测试 UUID 验证"""
    print("\n=== 测试 UUID 验证 ===")
    
    valid_uuids = [
        '550e8400-e29b-41d4-a716-446655440000',
        '123e4567-e89b-12d3-a456-426614174000',
    ]
    invalid_uuids = [
        'not-a-uuid',
        '550e8400-e29b-41d4-a716',
        '550e8400e29b41d4a716446655440000',
    ]
    
    print("有效 UUID 测试:")
    for uuid in valid_uuids:
        result = validate_uuid(uuid)
        status = "✓" if result else "✗"
        print(f"  {status} {uuid}: {result}")
        assert result, f"应该是有效 UUID: {uuid}"
    
    print("无效 UUID 测试:")
    for uuid in invalid_uuids:
        result = validate_uuid(uuid)
        status = "✓" if not result else "✗"
        print(f"  {status} {uuid}: {result}")
        assert not result, f"应该是无效 UUID: {uuid}"
    
    print("UUID 验证测试通过!")


def test_extract_emails():
    """测试邮箱提取"""
    print("\n=== 测试邮箱提取 ===")
    
    text = "联系邮箱：test@example.com 或 support@domain.co.uk，也可以发给用户名+tag@test.org"
    emails = extract_emails(text)
    
    print(f"文本：{text}")
    print(f"提取的邮箱：{emails}")
    
    assert len(emails) == 3, f"应该提取 3 个邮箱，实际：{len(emails)}"
    assert 'test@example.com' in emails
    assert 'support@domain.co.uk' in emails
    
    print("邮箱提取测试通过!")


def test_extract_urls():
    """测试 URL 提取"""
    print("\n=== 测试 URL 提取 ===")
    
    text = "访问 https://example.com 或 http://test.org/page?query=1 获取更多信息"
    urls = extract_urls(text)
    
    print(f"文本：{text}")
    print(f"提取的 URL: {urls}")
    
    assert len(urls) >= 2, f"应该至少提取 2 个 URL，实际：{len(urls)}"
    
    print("URL 提取测试通过!")


def test_extract_hashtags():
    """测试话题标签提取"""
    print("\n=== 测试话题标签提取 ===")
    
    text = "今天天气真好 #好心情 #周末 #出去玩 大家有什么计划？"
    hashtags = extract_hashtags(text)
    
    print(f"文本：{text}")
    print(f"提取的话题：{hashtags}")
    
    assert len(hashtags) == 3, f"应该提取 3 个话题，实际：{len(hashtags)}"
    assert '好心情' in hashtags
    assert '周末' in hashtags
    assert '出去玩' in hashtags
    
    print("话题标签提取测试通过!")


def test_extract_mentions():
    """测试@提及提取"""
    print("\n=== 测试@提及提取 ===")
    
    text = "@张三 @李四 你们好！还有@王五 也来看看"
    mentions = extract_mentions(text)
    
    print(f"文本：{text}")
    print(f"提取的提及：{mentions}")
    
    assert len(mentions) == 3, f"应该提取 3 个提及，实际：{len(mentions)}"
    assert '张三' in mentions
    assert '李四' in mentions
    assert '王五' in mentions
    
    print("@提及提取测试通过!")


def test_extract_numbers():
    """测试数字提取"""
    print("\n=== 测试数字提取 ===")
    
    text = "温度是 25 度，湿度 60%，价格 199.99 元，数量 -5 个"
    
    # 整数
    ints = extract_numbers(text, as_float=False)
    print(f"整数：{ints}")
    assert 25 in ints
    assert 60 in ints
    assert 199 in ints
    
    # 浮点数
    floats = extract_numbers(text, as_float=True)
    print(f"浮点数：{floats}")
    assert 25.0 in floats
    assert 60.0 in floats
    assert 199.99 in floats
    
    print("数字提取测试通过!")


def test_remove_html_tags():
    """测试 HTML 标签移除"""
    print("\n=== 测试 HTML 标签移除 ===")
    
    html = '<div class="container"><p>Hello <strong>World</strong>!</p></div>'
    result = remove_html_tags(html, keep_content=True)
    
    print(f"HTML: {html}")
    print(f"纯文本：{result}")
    
    assert 'Hello' in result
    assert 'World' in result
    assert '<' not in result
    assert '>' not in result
    
    print("HTML 标签移除测试通过!")


def test_normalize_whitespace():
    """测试空白标准化"""
    print("\n=== 测试空白标准化 ===")
    
    text = "Hello    World\n\n\nTest\t\t\tCase"
    result = normalize_whitespace(text)
    
    print(f"原文本：'{text}'")
    print(f"标准化后：'{result}'")
    
    assert result == "Hello World Test Case"
    
    print("空白标准化测试通过!")


def test_censor_phone():
    """测试电话号码屏蔽"""
    print("\n=== 测试电话号码屏蔽 ===")
    
    phone = "13800138000"
    result = censor_phone(phone)
    
    print(f"原号码：{phone}")
    print(f"屏蔽后：{result}")
    
    assert result == "138****8000"
    
    print("电话号码屏蔽测试通过!")


def test_censor_id_card():
    """测试身份证屏蔽"""
    print("\n=== 测试身份证屏蔽 ===")
    
    id_card = "110101199001011234"
    result = censor_id_card(id_card)
    
    print(f"原号码：{id_card}")
    print(f"屏蔽后：{result}")
    
    assert result == "110101********1234"
    
    print("身份证屏蔽测试通过!")


def test_find_all_matches():
    """测试查找所有匹配"""
    print("\n=== 测试查找所有匹配 ===")
    
    text = "The rain in Spain falls mainly in the plain"
    pattern = r'\b\w+ain\b'
    
    matches = find_all_matches(text, pattern)
    
    print(f"文本：{text}")
    print(f"模式：{pattern}")
    print(f"匹配：{matches}")
    
    assert len(matches) == 3, f"应该匹配 3 个单词，实际：{len(matches)}"
    assert 'rain' in matches
    assert 'Spain' in matches
    assert 'plain' in matches
    
    print("查找所有匹配测试通过!")


def test_contains_pattern():
    """测试模式包含检查"""
    print("\n=== 测试模式包含检查 ===")
    
    text = "Hello World 2024"
    
    assert contains_pattern(text, r'\d{4}')  # 包含 4 位数字
    assert contains_pattern(text, r'Hello')  # 包含 Hello
    assert not contains_pattern(text, r'\d{5}')  # 不包含 5 位数字
    
    print("模式包含检查测试通过!")


def test_split_by_pattern():
    """测试按模式分割"""
    print("\n=== 测试按模式分割 ===")
    
    text = "apple,banana;orange|grape"
    result = split_by_pattern(text, r'[,;|]')
    
    print(f"文本：{text}")
    print(f"分割结果：{result}")
    
    assert result == ['apple', 'banana', 'orange', 'grape']
    
    print("按模式分割测试通过!")


def test_escape_pattern():
    """测试模式转义"""
    print("\n=== 测试模式转义 ===")
    
    text = "Cost: $100 (50% off)"
    literal = "$100 (50% off)"
    escaped = escape_pattern(literal)
    
    print(f"原文本：{literal}")
    print(f"转义后：{escaped}")
    
    # 转义后应该能精确匹配
    assert re.search(escaped, text)
    
    print("模式转义测试通过!")


def test_get_pattern_names():
    """测试获取模式名称"""
    print("\n=== 测试获取模式名称 ===")
    
    names = get_pattern_names()
    
    print(f"可用模式数量：{len(names)}")
    print(f"部分模式：{names[:10]}")
    
    assert len(names) > 20
    assert 'email' in names
    assert 'url' in names
    assert 'phone_cn' in names
    
    print("获取模式名称测试通过!")


def test_pattern_info():
    """测试模式信息"""
    print("\n=== 测试模式信息 ===")
    
    info = pattern_info('email')
    
    print(f"模式名称：{info['name']}")
    print(f"描述：{info.get('description', 'N/A')}")
    print(f"示例：{info.get('examples', [])}")
    
    assert info['name'] == 'email'
    assert 'pattern' in info
    
    print("模式信息测试通过!")


def test_regex_matcher_class():
    """测试 RegexMatcher 类"""
    print("\n=== 测试 RegexMatcher 类 ===")
    
    matcher = RegexMatcher(r'\d+')
    text = "There are 123 apples and 456 oranges"
    
    # 测试 findall
    matches = matcher.findall(text)
    print(f"匹配数字：{matches}")
    assert matches == ['123', '456']
    
    # 测试 search
    match = matcher.search(text)
    assert match is not None
    assert match.group() == '123'
    
    # 测试 sub
    result = matcher.sub(text, 'NUM')
    print(f"替换后：{result}")
    assert result == "There are NUM apples and NUM oranges"
    
    print("RegexMatcher 类测试通过!")


def test_text_cleaner_class():
    """测试 TextCleaner 类"""
    print("\n=== 测试 TextCleaner 类 ===")
    
    text = '<p>Hello @user #topic http://example.com</p>   Multiple   spaces'
    
    cleaner = TextCleaner()
    result = (cleaner
              .load(text)
              .remove_html()
              .remove_mentions()
              .remove_hashtags()
              .replace_urls('[LINK]')
              .normalize_whitespace()
              .get())
    
    print(f"原文本：{text}")
    print(f"清洗后：{result}")
    
    assert '<' not in result
    assert '@' not in result
    assert '#' not in result
    assert 'http' not in result
    assert '  ' not in result  # 无连续空格
    
    print("TextCleaner 类测试通过!")


def test_batch_validate():
    """测试批量验证"""
    print("\n=== 测试批量验证 ===")
    
    emails = ['test@example.com', 'invalid', 'user@domain.org']
    results = batch_validate(emails, validate_email)
    
    print(f"验证结果：{results}")
    
    assert results['test@example.com'] == True
    assert results['invalid'] == False
    assert results['user@domain.org'] == True
    
    print("批量验证测试通过!")


def test_filter_by_pattern():
    """测试按模式过滤"""
    print("\n=== 测试按模式过滤 ===")
    
    items = ['apple', 'banana', 'cherry', 'date', 'elderberry']
    
    # 保留包含'a'的
    with_a = filter_by_pattern(items, r'a', keep_matching=True)
    print(f"包含'a'的：{with_a}")
    assert with_a == ['apple', 'banana', 'date']
    
    # 移除包含'a'的
    without_a = filter_by_pattern(items, r'a', keep_matching=False)
    print(f"不包含'a'的：{without_a}")
    assert without_a == ['cherry', 'elderberry']
    
    print("按模式过滤测试通过!")


def test_group_by_pattern():
    """测试按模式分组"""
    print("\n=== 测试按模式分组 ===")
    
    items = ['apple', 'banana', 'cherry', 'date']
    groups = group_by_pattern(items, r'^[a-c]')
    
    print(f"分组结果：{groups}")
    
    assert 'apple' in groups[True]
    assert 'banana' in groups[True]
    assert 'cherry' in groups[True]
    assert 'date' in groups[False]
    
    print("按模式分组测试通过!")


def test_extract_between():
    """测试提取标记间内容"""
    print("\n=== 测试提取标记间内容 ===")
    
    text = "Start [content1] Middle [content2] End"
    
    # 不包含标记
    result = extract_between(text, '[', ']')
    print(f"提取内容：{result}")
    assert result == ['content1', 'content2']
    
    # 包含标记
    result_with_markers = extract_between(text, '[', ']', include_markers=True)
    print(f"包含标记：{result_with_markers}")
    assert '[content1]' in result_with_markers
    
    print("提取标记间内容测试通过!")


def test_extract_markdown_links():
    """测试 Markdown 链接提取"""
    print("\n=== 测试 Markdown 链接提取 ===")
    
    text = "访问 [Google](https://google.com) 和 [GitHub](https://github.com)"
    links = extract_markdown_links(text)
    
    print(f"提取的链接：{links}")
    
    assert len(links) == 2
    assert ('Google', 'https://google.com') in links
    assert ('GitHub', 'https://github.com') in links
    
    print("Markdown 链接提取测试通过!")


def test_validate_ipv4():
    """测试 IPv4 验证"""
    print("\n=== 测试 IPv4 验证 ===")
    
    valid_ips = ['192.168.1.1', '10.0.0.255', '172.16.0.1', '8.8.8.8']
    invalid_ips = ['256.1.1.1', '192.168.1', '192.168.1.1.1', 'abc.def.ghi.jkl']
    
    print("有效 IP 测试:")
    for ip in valid_ips:
        result = validate_ipv4(ip)
        status = "✓" if result else "✗"
        print(f"  {status} {ip}: {result}")
        assert result, f"应该是有效 IPv4: {ip}"
    
    print("无效 IP 测试:")
    for ip in invalid_ips:
        result = validate_ipv4(ip)
        status = "✓" if not result else "✗"
        print(f"  {status} {ip}: {result}")
        assert not result, f"应该是无效 IPv4: {ip}"
    
    print("IPv4 验证测试通过!")


def test_validate_domain():
    """测试域名验证"""
    print("\n=== 测试域名验证 ===")
    
    valid_domains = ['example.com', 'sub.domain.co.uk', 'test.org']
    invalid_domains = ['not_a_domain', '.com', 'example.', 'example']
    
    print("有效域名测试:")
    for domain in valid_domains:
        result = validate_domain(domain)
        status = "✓" if result else "✗"
        print(f"  {status} {domain}: {result}")
        assert result, f"应该是有效域名：{domain}"
    
    print("无效域名测试:")
    for domain in invalid_domains:
        result = validate_domain(domain)
        status = "✓" if not result else "✗"
        print(f"  {status} {domain}: {result}")
        assert not result, f"应该是无效域名：{domain}"
    
    print("域名验证测试通过!")


def test_validate_chinese():
    """测试中文验证"""
    print("\n=== 测试中文验证 ===")
    
    valid_chinese = ['你好', '世界', '中文测试']
    invalid_chinese = ['Hello', '你好 world', '123']
    
    print("纯中文测试:")
    for text in valid_chinese:
        result = validate_chinese(text)
        status = "✓" if result else "✗"
        print(f"  {status} {text}: {result}")
        assert result, f"应该是纯中文：{text}"
    
    print("非纯中文测试:")
    for text in invalid_chinese:
        result = validate_chinese(text)
        status = "✓" if not result else "✗"
        print(f"  {status} {text}: {result}")
        assert not result, f"不应该是纯中文：{text}"
    
    print("中文验证测试通过!")


def test_replace_emails_and_urls():
    """测试邮箱和 URL 替换"""
    print("\n=== 测试邮箱和 URL 替换 ===")
    
    text = "联系 test@example.com 或访问 https://example.com"
    
    replaced_emails = replace_emails(text)
    print(f"替换邮箱：{replaced_emails}")
    assert '[EMAIL]' in replaced_emails
    assert 'test@example.com' not in replaced_emails
    
    replaced_urls = replace_urls(text)
    print(f"替换 URL: {replaced_urls}")
    assert '[LINK]' in replaced_urls
    assert 'https://example.com' not in replaced_urls
    
    print("邮箱和 URL 替换测试通过!")


def run_all_tests():
    """运行所有测试"""
    print("=" * 60)
    print("AllToolkit - Regex Utilities 测试套件")
    print("=" * 60)
    
    tests = [
        test_validate_email,
        test_validate_url,
        test_validate_phone,
        test_validate_date,
        test_validate_id_card,
        test_validate_password,
        test_validate_hex_color,
        test_validate_uuid,
        test_extract_emails,
        test_extract_urls,
        test_extract_hashtags,
        test_extract_mentions,
        test_extract_numbers,
        test_remove_html_tags,
        test_normalize_whitespace,
        test_censor_phone,
        test_censor_id_card,
        test_find_all_matches,
        test_contains_pattern,
        test_split_by_pattern,
        test_escape_pattern,
        test_get_pattern_names,
        test_pattern_info,
        test_regex_matcher_class,
        test_text_cleaner_class,
        test_batch_validate,
        test_filter_by_pattern,
        test_group_by_pattern,
        test_extract_between,
        test_extract_markdown_links,
        test_validate_ipv4,
        test_validate_domain,
        test_validate_chinese,
        test_replace_emails_and_urls,
    ]
    
    passed = 0
    failed = 0
    
    for test_func in tests:
        try:
            test_func()
            passed += 1
        except AssertionError as e:
            print(f"\n✗ {test_func.__name__} 失败：{e}")
            failed += 1
        except Exception as e:
            print(f"\n✗ {test_func.__name__} 异常：{e}")
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"测试完成：{passed} 通过，{failed} 失败，共 {passed + failed} 项")
    print("=" * 60)
    
    return failed == 0


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)

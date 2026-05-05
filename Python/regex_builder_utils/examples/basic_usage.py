# -*- coding: utf-8 -*-
"""
Regex Builder Utilities - 使用示例 📚

展示如何使用 RegexBuilder 构建各种正则表达式。
"""

import re
from mod import (
    RegexBuilder,
    builder,
    email_pattern,
    phone_cn_pattern,
    url_pattern,
    date_pattern,
    time_pattern,
    between_delimiters,
    quoted_string,
)


def example_basic():
    """基础用法示例"""
    print("\n=== 基础用法 ===")
    
    # 简单字面匹配
    pattern = RegexBuilder().literal('hello').build()
    print(f"字面匹配: {pattern}")
    print(f"匹配 'hello world': {bool(re.search(pattern, 'hello world'))}")
    
    # 字符范围
    pattern = RegexBuilder().char_range('a', 'z').one_or_more().build()
    print(f"小写字母: {pattern}")
    print(f"匹配 'test': {bool(re.search(pattern, 'test'))}")
    
    # 数字匹配
    pattern = RegexBuilder().digit().one_or_more().build()
    print(f"数字: {pattern}")
    print(f"查找 'abc123def456': {re.findall(pattern, 'abc123def456')}")


def example_email():
    """邮箱正则示例"""
    print("\n=== 邮箱正则 ===")
    
    # 使用构建器
    email = (RegexBuilder()
        .start()
        .one_or_more(RegexBuilder.CHAR_CLASS.WORD)
        .literal('@')
        .one_or_more(RegexBuilder.CHAR_CLASS.WORD)
        .literal('.')
        .min_max(2, 4, RegexBuilder.CHAR_CLASS.WORD)
        .end()
        .build())
    
    print(f"构建器生成的正则: {email}")
    
    # 使用快捷函数
    quick_pattern = email_pattern()
    print(f"快捷函数生成的正则: {quick_pattern}")
    
    # 测试
    test_emails = [
        'test@example.com',
        'user.name@domain.org',
        'invalid',
        'missing@domain',
    ]
    
    pattern = RegexBuilder().compile(email)
    for email_addr in test_emails:
        result = bool(pattern.match(email_addr))
        print(f"  {email_addr}: {result}")


def example_phone():
    """手机号正则示例"""
    print("\n=== 中国手机号正则 ===")
    
    pattern = phone_cn_pattern()
    print(f"正则: {pattern}")
    
    test_phones = [
        '13812345678',
        '18600001111',
        '12812345678',  # 无效
        '1234567890',   # 无效
    ]
    
    compiled = re.compile(pattern)
    for phone in test_phones:
        result = bool(compiled.match(phone))
        print(f"  {phone}: {'有效' if result else '无效'}")


def example_date():
    """日期正则示例"""
    print("\n=== 日期正则 ===")
    
    # ISO 格式
    iso_pattern = date_pattern('iso')
    print(f"ISO 日期正则: {iso_pattern}")
    
    # 中文格式
    cn_pattern = date_pattern('cn')
    print(f"中文日期正则: {cn_pattern}")
    
    # 带命名组的完整日期
    full_date = (RegexBuilder()
        .start()
        .group(r'\d{4}', 'year')
        .literal('-')
        .group(r'\d{2}', 'month')
        .literal('-')
        .group(r'\d{2}', 'day')
        .end()
        .build())
    
    print(f"带命名组的日期正则: {full_date}")
    
    match = re.match(full_date, '2024-05-10')
    if match:
        print(f"  年: {match.group('year')}")
        print(f"  月: {match.group('month')}")
        print(f"  日: {match.group('day')}")


def example_password():
    """密码验证示例"""
    print("\n=== 密码验证 ===")
    
    # 需要：至少8位，包含大小写字母和数字
    password_pattern = (RegexBuilder()
        .start()
        .lookahead(RegexBuilder().min_times(1, RegexBuilder().char_range('a', 'z').build()).build())
        .lookahead(RegexBuilder().min_times(1, RegexBuilder().char_range('A', 'Z').build()).build())
        .lookahead(RegexBuilder().min_times(1, RegexBuilder.CHAR_CLASS.DIGIT).build())
        .min_times(8, RegexBuilder.CHAR_CLASS.WORD)
        .end()
        .build())
    
    print(f"密码正则: {password_pattern}")
    
    test_passwords = [
        'Password1',    # 有效
        'password',     # 无效 (缺少大写)
        'PASSWORD',     # 无效 (缺少小写)
        'Pass1',        # 无效 (少于8位)
        'password123',  # 无效 (缺少大写)
    ]
    
    pattern = re.compile(password_pattern)
    for pwd in test_passwords:
        result = bool(pattern.match(pwd))
        print(f"  {pwd}: {'有效' if result else '无效'}")


def example_url():
    """URL 正则示例"""
    print("\n=== URL 正则 ===")
    
    pattern = url_pattern()
    print(f"URL 正则: {pattern}")
    
    text = '访问 https://example.com 和 http://test.org/path 获取更多信息'
    urls = re.findall(pattern, text)
    print(f"提取的 URL: {urls}")


def example_between_delimiters():
    """分隔符内容提取示例"""
    print("\n=== 分隔符内容提取 ===")
    
    # 方括号内容
    bracket_pattern = between_delimiters('[', ']')
    print(f"方括号正则: {bracket_pattern}")
    
    text = '数组 [1, 2, 3] 和 [a, b, c]'
    matches = re.findall(bracket_pattern, text)
    print(f"提取内容: {matches}")
    
    # 括号内函数名
    func_pattern = between_delimiters('(', ')')
    text = 'func(arg1, arg2) 和 call(param)'
    matches = re.findall(func_pattern, text)
    print(f"函数参数: {matches}")


def example_quoted_string():
    """引号字符串示例"""
    print("\n=== 引号字符串 ===")
    
    pattern = quoted_string('"')
    print(f"双引号字符串正则: {pattern}")
    
    text = '他说 "你好世界" 然后离开了'
    match = re.search(pattern, text)
    if match:
        print(f"提取内容: {match.group(1)}")
    
    # 单引号
    single_pattern = quoted_string("'")
    text = "name = 'John' and age = '25'"
    matches = re.findall(single_pattern, text)
    print(f"单引号内容: {matches}")


def example_complex():
    """复杂模式示例"""
    print("\n=== 复杂模式 ===")
    
    # 构建一个匹配 HTML 标签的正则
    # <tag>content</tag>
    tag_pattern = (RegexBuilder()
        .literal('<')
        .group(r'[a-zA-Z]+', 'tag')
        .literal('>')
        .group(r'.*', 'content')
        .literal('</')
        .backreference('tag')
        .literal('>')
        .build())
    
    print(f"HTML 标签正则: {tag_pattern}")
    
    text = '<div>Hello</div> and <span>World</span>'
    # 注意：这个简单模式可能不完全匹配复杂 HTML
    
    # 构建一个匹配 JSON 字段值的正则
    json_field = (RegexBuilder()
        .literal('"')
        .group(r'\w+', 'key')
        .literal('"')
        .literal(':')
        .whitespace().zero_or_more()
        .either(
            RegexBuilder().quoted_string().build(),
            RegexBuilder().digit().one_or_more().build(),
            RegexBuilder().literal('true').build(),
            RegexBuilder().literal('false').build(),
            RegexBuilder().literal('null').build()
        )
        .build())
    
    print(f"JSON 字段正则（简化）: {json_field}")


def example_test_methods():
    """测试方法示例"""
    print("\n=== 测试方法 ===")
    
    builder = RegexBuilder().literal('hello').one_or_more()
    
    # test 方法
    print(f"test('helloooo'): {builder.test('helloooo')}")
    print(f"test('hi'): {builder.test('hi')}")
    
    # find_all 方法
    builder = RegexBuilder().digit().one_or_more()
    print(f"find_all('a1 b22 c333'): {builder.find_all('a1 b22 c333')}")
    
    # replace 方法
    builder = RegexBuilder().literal('cat')
    print(f"replace('cat and cat', 'dog'): {builder.replace('cat and cat', 'dog')}")
    
    # split 方法
    builder = RegexBuilder().literal(',')
    print(f"split('a,b,c'): {builder.split('a,b,c')}")


def example_flags():
    """标志使用示例"""
    print("\n=== 标志使用 ===")
    
    # 忽略大小写
    builder = RegexBuilder().literal('hello').ignore_case()
    print(f"忽略大小写正则: {builder.build()}")
    print(f"匹配 'HELLO': {builder.test('HELLO')}")
    print(f"匹配 'hello': {builder.test('hello')}")
    
    # 多行模式
    builder = RegexBuilder().start().literal('hello').multiline()
    pattern = builder.compile()
    text = 'world\nhello\nthere'
    print(f"多行匹配 'world\\nhello\\nthere': {bool(pattern.search(text))}")


def main():
    """运行所有示例"""
    print("=" * 60)
    print("Regex Builder Utilities - 使用示例")
    print("=" * 60)
    
    example_basic()
    example_email()
    example_phone()
    example_date()
    example_password()
    example_url()
    example_between_delimiters()
    example_quoted_string()
    example_complex()
    example_test_methods()
    example_flags()
    
    print("\n" + "=" * 60)
    print("示例完成!")
    print("=" * 60)


if __name__ == '__main__':
    main()
# -*- coding: utf-8 -*-
"""
AllToolkit - Regex Utilities 高级使用示例

演示 regex_utils 模块的高级功能和实际应用场景。
"""

import sys
import os

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    # 类
    RegexMatcher, TextCleaner,
    
    # 批量处理
    batch_validate, batch_extract, filter_by_pattern, group_by_pattern,
    
    # 提取函数
    extract_emails, extract_urls, extract_html_tags,
    extract_markdown_links, extract_between,
    
    # 验证函数
    validate_email, validate_url, validate_ipv4,
    
    # 匹配函数
    find_all_matches, match_groups, match_named_groups,
    contains_pattern, split_by_pattern,
    
    # 工具函数
    escape_pattern, compile_pattern, test_pattern,
)


def demo_regex_matcher():
    """演示 RegexMatcher 类"""
    print("=" * 50)
    print("1. RegexMatcher 类演示")
    print("=" * 50)
    
    # 创建匹配器
    matcher = RegexMatcher(r'\d{4}-\d{2}-\d{2}')  # 日期模式
    text = "今天是 2024-01-15，明天是 2024-01-16，后天是 2024-01-17"
    
    print(f"\n文本：{text}")
    print(f"模式：日期 (YYYY-MM-DD)")
    
    # findall
    print(f"\n查找所有：{matcher.findall(text)}")
    
    # search
    match = matcher.search(text)
    if match:
        print(f"第一个匹配：{match.group()} (位置：{match.start()}-{match.end()})")
    
    # sub (替换)
    replaced = matcher.sub(text, '[DATE]')
    print(f"替换后：{replaced}")
    
    # subn (替换并计数)
    result, count = matcher.subn(text, '[DATE]')
    print(f"替换次数：{count}")
    
    # 带分组的匹配
    print("\n" + "-" * 30)
    print("分组匹配示例:")
    group_matcher = RegexMatcher(r'(\w+)@(\w+\.\w+)')
    email_text = "联系 test@example.com 或 support@domain.org"
    
    for match in group_matcher.finditer(email_text):
        print(f"  完整匹配：{match.group()}")
        print(f"  用户名：{match.group(1)}")
        print(f"  域名：{match.group(2)}")


def demo_text_cleaner():
    """演示 TextCleaner 类"""
    print("\n" + "=" * 50)
    print("2. TextCleaner 类演示")
    print("=" * 50)
    
    # 原始文本（包含各种需要清洗的内容）
    dirty_text = """
    <div class="post">
        <h1>标题</h1>
        <p>作者：@张三 @李四</p>
        <p>话题：#技术 #编程 #Python</p>
        <p>链接：https://example.com/article</p>
        <p>联系：test@example.com</p>
        <p>电话：13800138000</p>
    </div>
    
    
    多余空白
    """
    
    print(f"原文本:\n{dirty_text}")
    
    # 链式清洗
    cleaner = TextCleaner()
    cleaned = (cleaner
               .load(dirty_text)
               .remove_html()
               .remove_mentions()
               .remove_hashtags()
               .replace_urls('[LINK]')
               .replace_emails('[EMAIL]')
               .censor_phones()
               .normalize_whitespace()
               .get())
    
    print(f"\n清洗后:\n{cleaned}")
    
    # 分步清洗示例
    print("\n" + "-" * 30)
    print("分步清洗:")
    
    step1 = TextCleaner().load(dirty_text).remove_html().get()
    print(f"1. 移除 HTML: {step1[:50]}...")
    
    step2 = TextCleaner().load(step1).remove_mentions().get()
    print(f"2. 移除提及：{step2[:50]}...")
    
    step3 = TextCleaner().load(step2).normalize_whitespace().get()
    print(f"3. 标准化：{step3[:50]}...")


def demo_batch_processing():
    """演示批量处理"""
    print("\n" + "=" * 50)
    print("3. 批量处理演示")
    print("=" * 50)
    
    # 批量验证
    print("\n批量验证邮箱:")
    emails = [
        'valid@example.com',
        'also.valid@domain.org',
        'invalid',
        'another@valid.co.uk',
        'not-email',
    ]
    
    results = batch_validate(emails, validate_email)
    for email, is_valid in results.items():
        print(f"  {email}: {'✓' if is_valid else '✗'}")
    
    valid_emails = [e for e, v in results.items() if v]
    print(f"\n有效邮箱：{valid_emails}")
    
    # 批量提取
    print("\n" + "-" * 30)
    print("批量提取 URL:")
    texts = [
        "访问 https://google.com 搜索",
        "GitHub: https://github.com",
        "没有链接的文本",
        "多个链接：https://a.com 和 https://b.org",
    ]
    
    extracted = batch_extract(texts, extract_urls)
    for text, urls in extracted.items():
        print(f"  '{text[:30]}...' → {urls}")
    
    # 按模式过滤
    print("\n" + "-" * 30)
    print("按模式过滤:")
    names = ['Alice', 'Bob', 'Charlie', 'David', 'Eve', 'Frank']
    
    # 保留以 A-C 开头的
    filtered = filter_by_pattern(names, r'^[A-C]', keep_matching=True)
    print(f"以 A-C 开头：{filtered}")
    
    # 移除以 A-C 开头的
    filtered_out = filter_by_pattern(names, r'^[A-C]', keep_matching=False)
    print(f"不以 A-C 开头：{filtered_out}")
    
    # 按模式分组
    print("\n" + "-" * 30)
    print("按模式分组:")
    groups = group_by_pattern(names, r'[aeiou]')  # 包含元音字母
    print(f"包含元音：{groups[True]}")
    print(f"不包含元音：{groups[False]}")


def demo_advanced_matching():
    """演示高级匹配"""
    print("\n" + "=" * 50)
    print("4. 高级匹配演示")
    print("=" * 50)
    
    text = "Price: $199.99, Discount: 20%, Final: $159.99"
    
    # 查找所有匹配
    print("\n查找所有价格:")
    prices = find_all_matches(text, r'\$[\d.]+')
    print(f"  结果：{prices}")
    
    # 检查是否包含模式
    print("\n检查是否包含折扣信息:")
    has_discount = contains_pattern(text, r'\d+%')
    print(f"  包含折扣：{has_discount}")
    
    # 分组匹配
    print("\n" + "-" * 30)
    print("分组匹配:")
    log_line = "2024-01-15 10:30:00 ERROR User login failed"
    
    # 普通分组
    pattern = r'(\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}:\d{2}) (\w+) (.+)'
    groups = match_groups(log_line, pattern)
    if groups:
        print(f"  日期：{groups[0]}")
        print(f"  时间：{groups[1]}")
        print(f"  级别：{groups[2]}")
        print(f"  消息：{groups[3]}")
    
    # 命名分组
    print("\n" + "-" * 30)
    print("命名分组:")
    named_pattern = r'(?P<date>\d{4}-\d{2}-\d{2}) (?P<level>\w+) (?P<message>.+)'
    named_groups = match_named_groups(log_line, named_pattern)
    if named_groups:
        for key, value in named_groups.items():
            print(f"  {key}: {value}")
    
    # 分割
    print("\n" + "-" * 30)
    print("按模式分割:")
    csv_like = "apple,banana;orange|grape,melon"
    parts = split_by_pattern(csv_like, r'[,;|]')
    print(f"  分割结果：{parts}")


def demo_html_processing():
    """演示 HTML 处理"""
    print("\n" + "=" * 50)
    print("5. HTML 处理演示")
    print("=" * 50)
    
    html = """
    <html>
        <head><title>测试页面</title></head>
        <body>
            <div class="container">
                <h1 id="main">欢迎</h1>
                <p class="intro">这是一个<b>测试</b>页面</p>
                <a href="https://example.com">链接</a>
                <img src="image.jpg" alt="图片"/>
            </div>
        </body>
    </html>
    """
    
    print("提取 HTML 标签信息:")
    tags = extract_html_tags(html)
    
    for tag in tags[:5]:  # 只显示前 5 个
        print(f"  标签：<{tag['tag_name']}>")
        if tag['attributes']:
            print(f"    属性：{tag['attributes'][:50]}...")
        if tag['content'] and len(tag['content']) < 50:
            print(f"    内容：{tag['content']}")
    
    # 提取特定标签
    print("\n" + "-" * 30)
    print("提取所有链接:")
    link_pattern = r'<a[^>]*href="([^"]*)"[^>]*>([^<]*)</a>'
    links = find_all_matches(html, link_pattern)
    for link in links:
        print(f"  {link[1]}: {link[0]}")


def demo_markdown_processing():
    """演示 Markdown 处理"""
    print("\n" + "=" * 50)
    print("6. Markdown 处理演示")
    print("=" * 50)
    
    markdown = """
# 文章标题

这是 [Google](https://google.com) 和 [GitHub](https://github.com) 的链接。

![图片](image.png)

## 章节

- 列表项 1
- 列表项 2

`代码片段`

```python
print("Hello")
```

#标签 #技术
"""
    
    print("提取 Markdown 链接:")
    links = extract_markdown_links(markdown)
    for text, url in links:
        print(f"  {text}: {url}")
    
    # 提取标记间内容
    print("\n" + "-" * 30)
    print("提取代码块内容:")
    code_blocks = extract_between(markdown, '```', '```')
    for i, code in enumerate(code_blocks):
        print(f"  代码块 {i+1}:")
        print(f"    {code.strip()}")
    
    # 检查 Markdown 元素
    print("\n" + "-" * 30)
    print("检查 Markdown 元素:")
    checks = {
        '包含标题': contains_pattern(markdown, r'^#'),
        '包含链接': contains_pattern(markdown, r'\[.*?\]\(.*?\)'),
        '包含图片': contains_pattern(markdown, r'!\[.*?\]\(.*?\)'),
        '包含代码块': contains_pattern(markdown, r'```'),
        '包含列表': contains_pattern(markdown, r'^[-*] '),
        '包含标签': contains_pattern(markdown, r'#\w+'),
    }
    
    for check, result in checks.items():
        print(f"  {check}: {'✓' if result else '✗'}")


def demo_pattern_testing():
    """演示模式测试"""
    print("\n" + "=" * 50)
    print("7. 模式测试演示")
    print("=" * 50)
    
    # 测试自定义模式
    pattern = r'^[A-Z][a-z]+$'  # 首字母大写
    test_strings = ['Hello', 'WORLD', 'hello', 'World', '123']
    
    print(f"模式：{pattern}")
    print(f"描述：首字母大写的单词\n")
    
    results = test_pattern(pattern, test_strings)
    for string, matches in results.items():
        print(f"  '{string}': {'✓ 匹配' if matches else '✗ 不匹配'}")
    
    # 转义特殊字符
    print("\n" + "-" * 30)
    print("转义特殊字符:")
    literal = "$100 (50% off) [限时]"
    escaped = escape_pattern(literal)
    print(f"  原文本：{literal}")
    print(f"  转义后：{escaped}")
    
    # 验证转义后的模式能正确匹配
    test_text = "价格：$100 (50% off) [限时] 优惠"
    compiled = compile_pattern(escaped)
    match = compiled.search(test_text)
    print(f"  匹配结果：{match.group() if match else '无匹配'}")


def demo_real_world_scenarios():
    """演示实际应用场景"""
    print("\n" + "=" * 50)
    print("8. 实际应用场景")
    print("=" * 50)
    
    # 场景 1: 日志分析
    print("\n场景 1: 日志分析")
    log_data = """
    2024-01-15 10:30:00 INFO Request from 192.168.1.100
    2024-01-15 10:30:01 ERROR ERROR_500 Internal server error
    2024-01-15 10:30:02 INFO Response time: 125ms
    2024-01-15 10:30:03 WARNING WARNING_001 High memory usage
    2024-01-15 10:30:04 INFO Request from 192.168.1.101
    """
    
    # 提取 IP 地址
    ips = find_all_matches(log_data, r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b')
    print(f"  IP 地址：{ips}")
    
    # 提取时间戳
    timestamps = find_all_matches(log_data, r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}')
    print(f"  时间戳数量：{len(timestamps)}")
    
    # 检查错误
    has_errors = contains_pattern(log_data, r'ERROR_\d+')
    print(f"  包含错误：{has_errors}")
    
    # 场景 2: 用户输入清理
    print("\n场景 2: 用户输入清理")
    user_input = "  <script>alert('xss')</script>  Hello   World  "
    cleaned = TextCleaner().load(user_input).remove_html_tags().normalize_whitespace().get()
    print(f"  原始输入：{user_input}")
    print(f"  清理后：{cleaned}")
    
    # 场景 3: 数据验证流水线
    print("\n场景 3: 数据验证流水线")
    user_data = [
        {'email': 'valid@example.com', 'phone': '13800138000'},
        {'email': 'invalid', 'phone': '12345678901'},
        {'email': 'test@domain.org', 'phone': '19912345678'},
    ]
    
    for user in user_data:
        email_ok = validate_email(user['email'])
        phone_ok = validate_phone(user['phone'], 'cn')
        status = "✓" if email_ok and phone_ok else "✗"
        print(f"  {status} {user['email']}: 邮箱{'✓' if email_ok else '✗'}, 电话{'✓' if phone_ok else '✗'}")


def main():
    """主函数"""
    print("\n" + "=" * 50)
    print("AllToolkit - Regex Utilities 高级示例")
    print("=" * 50)
    
    demo_regex_matcher()
    demo_text_cleaner()
    demo_batch_processing()
    demo_advanced_matching()
    demo_html_processing()
    demo_markdown_processing()
    demo_pattern_testing()
    demo_real_world_scenarios()
    
    print("\n" + "=" * 50)
    print("演示完成!")
    print("=" * 50)


if __name__ == '__main__':
    main()

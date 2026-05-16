"""
Escape Utils 使用示例

演示各种转义功能的使用方法
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    escape_html, unescape_html,
    escape_url, unescape_url,
    escape_url_query, unescape_url_query,
    escape_json_string, unescape_json_string,
    escape_shell, escape_shell_args,
    escape_regex,
    escape_glob,
    escape_c_string, unescape_c_string,
    escape_sql_string,
    escape, unescape,
    needs_escape, detect_escapes,
)


def main():
    print("=" * 60)
    print("Escape Utils - 转义工具示例")
    print("=" * 60)
    
    # 1. HTML 转义示例
    print("\n【1. HTML 转义】")
    print("-" * 40)
    
    html_input = '<script>alert("XSS攻击")</script>'
    html_escaped = escape_html(html_input)
    print(f"原始: {html_input}")
    print(f"转义: {html_escaped}")
    print(f"反转义: {unescape_html(html_escaped)}")
    
    # 扩展实体
    print("\n扩展实体示例:")
    extended_text = '© 2024 公司™ 版权所有'
    extended_escaped = escape_html(extended_text, extended=True)
    print(f"原始: {extended_text}")
    print(f"转义: {extended_escaped}")
    
    # 数字实体解码
    numeric = 'Hello&#64;World&#128512;'
    print(f"\n数字实体解码: {numeric} -> {unescape_html(numeric)}")
    
    # 2. URL 编码示例
    print("\n【2. URL 编码】")
    print("-" * 40)
    
    url_input = '你好世界/测试?name=value'
    url_encoded = escape_url(url_input)
    print(f"原始: {url_input}")
    print(f"编码: {url_encoded}")
    print(f"解码: {unescape_url(url_encoded)}")
    
    # 查询字符串
    print("\n查询字符串示例:")
    params = {
        'name': '张三',
        'age': '25',
        'tags': ['开发', '测试'],
        'search': 'hello world'
    }
    query = escape_url_query(params)
    print(f"参数: {params}")
    print(f"编码: {query}")
    parsed = unescape_url_query(query)
    print(f"解码: {parsed}")
    
    # 3. JSON 转义示例
    print("\n【3. JSON 转义】")
    print("-" * 40)
    
    json_input = 'Hello\nWorld\t"测试"'
    json_escaped = escape_json_string(json_input)
    print(f"原始: {repr(json_input)}")
    print(f"转义: {json_escaped}")
    print(f"反转义: {repr(unescape_json_string(json_escaped))}")
    
    # Unicode 模式
    print("\nUnicode 模式:")
    unicode_text = '你好世界🎉'
    ascii_mode = escape_json_string(unicode_text, ensure_ascii=True)
    non_ascii = escape_json_string(unicode_text, ensure_ascii=False)
    print(f"原始: {unicode_text}")
    print(f"ensure_ascii=True: {ascii_mode}")
    print(f"ensure_ascii=False: {non_ascii}")
    
    # 4. Shell 转义示例
    print("\n【4. Shell 转义】")
    print("-" * 40)
    
    shell_examples = [
        'hello world',
        '$HOME',
        'it\'s a test',
        'test & command',
    ]
    
    for example in shell_examples:
        escaped = escape_shell(example)
        print(f"原始: {example}")
        print(f"转义: {escaped}")
        print()
    
    # 参数列表
    print("参数列表转义:")
    args = ['echo', 'hello world', '$USER']
    cmd = escape_shell_args(args)
    print(f"参数: {args}")
    print(f"命令: {cmd}")
    
    # 5. 正则表达式转义示例
    print("\n【5. 正则表达式转义】")
    print("-" * 40)
    
    regex_examples = [
        'a.b',
        'test*value',
        'file[0-9]',
        'http://example.com',
    ]
    
    for example in regex_examples:
        escaped = escape_regex(example)
        print(f"原始: {example}")
        print(f"转义: {escaped}")
        
        # 验证可以安全用于正则
        import re
        pattern = escaped
        test_text = example
        match = re.search(pattern, test_text)
        print(f"匹配验证: {match is not None}")
        print()
    
    # 6. Glob 转义示例
    print("\n【6. Glob 转义】")
    print("-" * 40)
    
    glob_examples = [
        'file*.txt',
        'test?.log',
        'data[2024]',
    ]
    
    for example in glob_examples:
        escaped = escape_glob(example)
        print(f"原始: {example}")
        print(f"转义: {escaped}")
        print()
    
    # 7. C 语言转义示例
    print("\n【7. C 语言转义】")
    print("-" * 40)
    
    c_input = 'Hello\nWorld\t"Test"'
    c_escaped = escape_c_string(c_input)
    print(f"原始: {repr(c_input)}")
    print(f"转义: {c_escaped}")
    print(f"反转义: {repr(unescape_c_string(c_escaped))}")
    
    # 8. SQL 转义示例
    print("\n【8. SQL 转义】")
    print("-" * 40)
    
    sql_examples = [
        "O'Brien",
        "test's value",
        "Hello 'World'",
    ]
    
    for example in sql_examples:
        standard = escape_sql_string(example)
        mysql = escape_sql_string(example, style='mysql')
        postgres = escape_sql_string(example, style='postgres')
        print(f"原始: {example}")
        print(f"标准 SQL: {standard}")
        print(f"MySQL: {mysql}")
        print(f"PostgreSQL: {postgres}")
        print()
    
    # 9. 综合转义示例
    print("\n【9. 综合转义】")
    print("-" * 40)
    
    test_text = '<test>&"special"'
    formats = ['html', 'url', 'json', 'regex', 'shell']
    
    print(f"原始: {test_text}")
    for format in formats:
        escaped = escape(test_text, format)
        print(f"  {format}: {escaped}")
    
    # 10. 检测功能示例
    print("\n【10. 检测功能】")
    print("-" * 40)
    
    # 需要转义检测
    check_texts = [
        ('<script>', 'html'),
        ('hello world', 'url'),
        ('$HOME', 'shell'),
        ('a.b*c', 'regex'),
    ]
    
    print("需要转义检测:")
    for text, format in check_texts:
        needs = needs_escape(text, format)
        print(f"  {repr(text)} 需要 {format} 转义: {needs}")
    
    # 转义格式检测
    print("\n转义格式检测:")
    detect_texts = [
        '&lt;div&gt;Hello',
        'hello%20world',
        'Hello\\nWorld',
        '&lt;test%20value&#64;',
    ]
    
    for text in detect_texts:
        detected = detect_escapes(text)
        print(f"  {text[:30]}... -> {detected}")
    
    # 11. 安全提示示例
    print("\n【11. 安全提示】")
    print("-" * 40)
    
    # XSS 防护
    user_input = '<script>document.cookie</script>'
    safe_html = escape_html(user_input)
    print(f"用户输入 (XSS): {user_input}")
    print(f"安全处理后: {safe_html}")
    
    # URL 安全
    url_param = 'https://example.com?redirect=' + escape_url('https://evil.com')
    print(f"\nURL 参数编码: {url_param}")
    
    # Shell 命令安全
    dangerous_input = '; rm -rf /'
    safe_cmd = escape_shell(dangerous_input)
    print(f"\n危险输入: {dangerous_input}")
    print(f"安全处理: {safe_cmd}")
    
    print("\n" + "=" * 60)
    print("示例完成!")
    print("=" * 60)


if __name__ == "__main__":
    main()
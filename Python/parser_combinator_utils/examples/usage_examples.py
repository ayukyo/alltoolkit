"""
Parser Combinator Utils 使用示例

展示如何使用解析器组合子构建各种解析器。
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    char, string, satisfy, digit, letter, whitespace, spaces, spaces1,
    newline, any_char, none_of, one_of, sequence, choice, optional, many, many1,
    sep_by, sep_by1, between, lazy, eof, regex, integer, float_num,
    quoted_string, identifier, keyword, parse_or_error, parse_json,
    run_parser, Parser, Success, Failure
)


def example_basic_parsers():
    """基础解析器示例"""
    print("=" * 50)
    print("基础解析器示例")
    print("=" * 50)
    
    # 字符解析
    print("\n1. 字符解析:")
    result = char('a').parse("abc")
    print(f"   char('a').parse('abc') = {result}")
    
    result = char('x').parse("abc")
    print(f"   char('x').parse('abc') = {result}")
    
    # 字符串解析
    print("\n2. 字符串解析:")
    result = string("hello").parse("hello world")
    print(f"   string('hello').parse('hello world') = {result}")
    
    # 数字解析
    print("\n3. 数字字符解析:")
    result = many1(digit()).map(lambda cs: ''.join(cs)).parse("12345")
    print(f"   many1(digit()).parse('12345') = {result}")
    
    # 整数解析
    print("\n4. 整数解析:")
    result = integer().parse("12345")
    print(f"   integer().parse('12345') = {result}")
    
    result = integer().parse("-42")
    print(f"   integer().parse('-42') = {result}")
    
    # 浮点数解析
    print("\n5. 浮点数解析:")
    result = float_num().parse("3.14159")
    print(f"   float_num().parse('3.14159') = {result}")
    
    result = float_num().parse("1.5e-3")
    print(f"   float_num().parse('1.5e-3') = {result}")


def example_combinators():
    """组合子示例"""
    print("\n" + "=" * 50)
    print("组合子示例")
    print("=" * 50)
    
    # sequence - 顺序解析
    print("\n1. Sequence (顺序解析):")
    parser = sequence(char('a'), char('b'), char('c'))
    result = parser.parse("abcdef")
    print(f"   sequence(char('a'), char('b'), char('c')).parse('abcdef') = {result}")
    
    # choice - 选择解析
    print("\n2. Choice (选择解析):")
    parser = choice(char('a'), char('b'), char('c'))
    print(f"   choice(char('a'), char('b'), char('c')).parse('abc') = {parser.parse('abc')}")
    print(f"   choice(char('a'), char('b'), char('c')).parse('bcd') = {parser.parse('bcd')}")
    
    # many - 重复解析
    print("\n3. Many (重复解析 0-N 次):")
    parser = many(digit()).map(lambda cs: ''.join(cs))
    print(f"   many(digit()).parse('123abc') = {parser.parse('123abc')}")
    print(f"   many(digit()).parse('abc') = {parser.parse('abc')}")
    
    # many1 - 重复解析至少一次
    print("\n4. Many1 (重复解析 1-N 次):")
    parser = many1(letter()).map(lambda cs: ''.join(cs))
    print(f"   many1(letter()).parse('hello123') = {parser.parse('hello123')}")
    
    # optional - 可选解析
    print("\n5. Optional (可选解析):")
    parser = optional(char('-')).bind(lambda sign: 
        many1(digit()).map(lambda cs: int(''.join(cs)) * (-1 if sign else 1))
    )
    print(f"   optional('-') + digits.parse('42') = {parser.parse('42')}")
    print(f"   optional('-') + digits.parse('-42') = {parser.parse('-42')}")
    
    # sep_by - 分隔解析
    print("\n6. Sep_by (分隔解析):")
    parser = sep_by(integer(), char(','))
    print(f"   sep_by(integer(), char(',')).parse('1,2,3,4') = {parser.parse('1,2,3,4')}")
    
    # between - 两端解析
    print("\n7. Between (两端解析):")
    parser = between(char('('), integer(), char(')'))
    result = parser.parse("(123)")
    print(f"   between('(' , integer(), ')').parse('(123)') = {result}")


def example_map_and_bind():
    """map 和 bind 示例"""
    print("\n" + "=" * 50)
    print("Map 和 Bind 示例")
    print("=" * 50)
    
    # map - 转换结果
    print("\n1. Map (转换结果):")
    parser = many1(digit()).map(lambda cs: int(''.join(cs)))
    result = parser.parse("42")
    print(f"   many1(digit()).map(int).parse('42') = {result}")
    
    # 链式 map
    print("\n2. 链式 Map:")
    parser = integer().map(lambda x: x * 2).map(lambda x: x + 1)
    result = parser.parse("10")
    print(f"   integer().map(x*2).map(x+1).parse('10') = {result}")
    
    # bind - 组合解析器
    print("\n3. Bind (组合解析器):")
    # 解析 "a" 或 "aa" 后面跟着相应数量的 "b"
    parser = many1(char('a')).bind(lambda as_: 
        many1(char('b')).bind(lambda bs: 
            Parser(lambda s, p: Success(as_ + bs, s[p:], p) if len(bs) == len(as_) else Failure("Mismatch", p))
        )
    )
    
    # 使用运算符
    print("\n4. 运算符:")
    # >> (then) - 保留第二个结果
    parser = char('a') >> char('b')
    print(f"   char('a') >> char('b').parse('ab') = {parser.parse('ab')}")
    
    # << (skip) - 保留第一个结果
    parser = char('a') << char('b')
    print(f"   char('a') << char('b').parse('ab') = {parser.parse('ab')}")
    
    # | (or_else) - 选择
    parser = char('a') | char('b')
    print(f"   char('a') | char('b').parse('a') = {parser.parse('a')}")
    print(f"   char('a') | char('b').parse('b') = {parser.parse('b')}")


def example_json_parser():
    """JSON 解析器示例"""
    print("\n" + "=" * 50)
    print("JSON 解析器示例")
    print("=" * 50)
    
    # 解析简单 JSON 值
    print("\n1. 简单值:")
    print(f"   parse_json('null') = {parse_json('null')}")
    print(f"   parse_json('true') = {parse_json('true')}")
    print(f"   parse_json('false') = {parse_json('false')}")
    print(f"   parse_json('42') = {parse_json('42')}")
    print(f"   parse_json('3.14') = {parse_json('3.14')}")
    hello_result = parse_json('"hello"')
    print(f"   parse_json('\"hello\"') = {hello_result}")
    
    # 解析数组
    print("\n2. 数组:")
    print(f"   parse_json('[]') = {parse_json('[]')}")
    print(f"   parse_json('[1, 2, 3]') = {parse_json('[1, 2, 3]')}")
    array_result = parse_json('["a", "b", "c"]')
    print(f"   parse_json('[\"a\", \"b\", \"c\"]') = {array_result}")
    
    # 解析对象
    print("\n3. 对象:")
    empty_obj = parse_json('{}')
    print("   parse_json('{}') = " + str(empty_obj))
    obj_result = parse_json('{"key": "value"}')
    print(f"   parse_json('{{\"key\": \"value\"}}') = {obj_result}")
    
    # 解析嵌套结构
    print("\n4. 嵌套结构:")
    complex_json = '{"users": [{"name": "Alice", "age": 30}, {"name": "Bob", "age": 25}]}'
    result = parse_json(complex_json)
    print(f"   parse_json('{complex_json}') = {result}")
    if result.is_success():
        print(f"   解析结果: {result.value}")


def example_csv_parser():
    """CSV 解析器示例"""
    print("\n" + "=" * 50)
    print("CSV 解析器示例")
    print("=" * 50)
    
    # 定义字段解析器
    field = many(none_of(',\n')).map(lambda cs: ''.join(cs).strip())
    line = sep_by(field, char(','))
    csv = sep_by(line, newline())
    
    print("\n解析 CSV 数据:")
    csv_data = "name,age,city\nAlice,30,NYC\nBob,25,LA"
    result = csv.parse(csv_data)
    print(f"   输入: '{csv_data}'")
    print(f"   结果: {result}")
    if result.is_success():
        print(f"   数据: {result.value}")


def example_url_parser():
    """URL 解析器示例"""
    print("\n" + "=" * 50)
    print("URL 解析器示例")
    print("=" * 50)
    
    # 简化的 URL 解析器
    protocol = (string("http://") | string("https://")).map(lambda s: s.rstrip('://'))
    
    # 域名部分
    domain_char = satisfy(lambda c: c.isalnum() or c in '.-', "domain char")
    domain = many1(domain_char).map(lambda cs: ''.join(cs))
    
    # 路径部分
    path_char = satisfy(lambda c: c not in '?# ', "path char")
    path = many(path_char).map(lambda cs: ''.join(cs) if cs else '/')
    
    # 组合 URL 解析器
    url = sequence(protocol, domain, path).map(lambda parts: {
        'protocol': parts[0],
        'domain': parts[1],
        'path': parts[2]
    })
    
    print("\n解析 URL:")
    urls = [
        "https://example.com",
        "http://example.com/path/to/resource",
        "https://sub.example.com/api/users"
    ]
    
    for url_str in urls:
        result = url.parse(url_str)
        print(f"   '{url_str}' => {result}")


def example_expression_parser():
    """表达式解析器示例"""
    print("\n" + "=" * 50)
    print("表达式解析器示例")
    print("=" * 50)
    
    # 简化的算术表达式解析器
    number = integer()
    
    # 左结合的加法表达式
    def add_expr():
        def parse_func(s, pos):
            # 解析第一个数字
            result = number._parse(s, pos)
            if result.is_failure():
                return result
            
            total = result.value
            pos = result.position
            
            # 解析后续的 + 数字
            while pos < len(s):
                # 跳过空白
                while pos < len(s) and s[pos].isspace():
                    pos += 1
                
                if pos >= len(s) or s[pos] != '+':
                    break
                
                pos += 1  # 跳过 '+'
                
                # 跳过空白
                while pos < len(s) and s[pos].isspace():
                    pos += 1
                
                # 解析下一个数字
                result = number._parse(s, pos)
                if result.is_failure():
                    return result
                
                total += result.value
                pos = result.position
            
            return Success(total, s[pos:], pos)
        
        return Parser(parse_func)
    
    expr = add_expr()
    
    print("\n解析加法表达式:")
    expressions = ["1 + 2", "10 + 20 + 30", "1+2+3+4+5"]
    
    for expr_str in expressions:
        result = expr.parse(expr_str)
        print(f"   '{expr_str}' => {result}")


def example_config_parser():
    """配置文件解析器示例"""
    print("\n" + "=" * 50)
    print("配置文件解析器示例")
    print("=" * 50)
    
    # 简化的配置文件格式: key = value
    key = identifier()
    value = many(none_of('\n')).map(lambda cs: ''.join(cs).strip())
    
    # 单个配置项
    config_line = sequence(
        key,
        spaces().skip(char('=')),
        value
    )
    
    # 多行配置
    config = sep_by(config_line, newline()).map(lambda lines: 
        {line[0]: line[2] for line in lines}
    )
    
    print("\n解析配置文件:")
    config_data = """
name = MyApp
version = 1.0.0
author = John Doe
debug = true
"""
    
    result = config.parse(config_data.strip())
    print(f"   输入: '{config_data.strip()}'")
    print(f"   结果: {result}")
    if result.is_success():
        print(f"   配置字典: {result.value}")


def example_quoted_string():
    """引号字符串解析示例"""
    print("\n" + "=" * 50)
    print("引号字符串解析示例")
    print("=" * 50)
    
    parser = quoted_string('"')
    
    print("\n解析带引号的字符串:")
    strings = [
        '"hello"',
        '"hello world"',
        r'"hello\nworld"',  # 包含转义
        r'"escaped\"quote"',
    ]
    
    for s in strings:
        result = parser.parse(s)
        print(f"   '{s}' => {result}")


def example_error_handling():
    """错误处理示例"""
    print("\n" + "=" * 50)
    print("错误处理示例")
    print("=" * 50)
    
    # 使用 parse_or_error
    print("\n1. 使用 parse_or_error:")
    try:
        value = parse_or_error(integer(), "123")
        print(f"   成功解析: {value}")
    except ValueError as e:
        print(f"   解析失败: {e}")
    
    try:
        value = parse_or_error(integer(), "abc")
        print(f"   成功解析: {value}")
    except ValueError as e:
        print(f"   解析失败: {e}")
    
    # 检查解析结果
    print("\n2. 检查解析结果:")
    result = integer().parse("abc")
    if result.is_success():
        print(f"   成功: {result.value}")
    else:
        print(f"   失败: {result.error}")
    
    # parse_all 完全消费
    print("\n3. 完全消费验证:")
    parser = string("hello")
    result = parser.parse_all("hello world")
    print(f"   parse_all('hello world') => {result}")


def example_recursive_parser():
    """递归解析器示例（括号匹配）"""
    print("\n" + "=" * 50)
    print("递归解析器示例（括号匹配）")
    print("=" * 50)
    
    # 使用 lazy 实现递归
    def bracket_expr():
        def parse_func(s, pos):
            if pos >= len(s) or s[pos] != '(':
                return Failure("Expected '('", pos)
            
            pos += 1
            count = 1
            while pos < len(s) and count > 0:
                if s[pos] == '(':
                    count += 1
                elif s[pos] == ')':
                    count -= 1
                pos += 1
            
            if count != 0:
                return Failure("Unmatched brackets", pos)
            
            return Success("matched", s[pos:], pos)
        
        return Parser(parse_func)
    
    parser = bracket_expr()
    
    print("\n匹配括号:")
    examples = ["()", "(())", "((()))", "()()()", "(a(bc)d)"]
    
    for ex in examples:
        result = parser.parse(ex)
        print(f"   '{ex}' => {result}")


def main():
    """运行所有示例"""
    example_basic_parsers()
    example_combinators()
    example_map_and_bind()
    example_json_parser()
    example_csv_parser()
    example_url_parser()
    example_expression_parser()
    example_config_parser()
    example_quoted_string()
    example_error_handling()
    example_recursive_parser()
    
    print("\n" + "=" * 50)
    print("所有示例完成!")
    print("=" * 50)


if __name__ == "__main__":
    main()
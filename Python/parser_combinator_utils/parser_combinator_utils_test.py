"""
Parser Combinator Utils 测试文件

测试所有解析器组合子功能。
"""

import pytest
import sys
import os

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from parser_combinator_utils.mod import (
    Parser, Success, Failure, ParseResult,
    char, string, satisfy, digit, letter, alphanumeric,
    whitespace, spaces, spaces1, newline, tab, any_char,
    none_of, one_of, sequence, choice, optional, many, many1,
    sep_by, sep_by1, between, lazy, eof, regex, integer,
    float_num, quoted_string, identifier, keyword,
    run_parser, parse_or_error,
    json_parser, parse_json,
    digit_parser, letter_parser, identifier_parser,
    digits, letters, alphanumerics
)


class TestParseResult:
    """测试 ParseResult 类"""
    
    def test_success_is_success(self):
        """测试 Success.is_success()"""
        result = Success(42, "remaining", 5)
        assert result.is_success() is True
        assert result.is_failure() is False
    
    def test_success_get_value(self):
        """测试 Success.get_value()"""
        result = Success("hello", "", 5)
        assert result.get_value() == "hello"
    
    def test_success_map(self):
        """测试 Success.map()"""
        result = Success(10, "", 2)
        mapped = result.map(lambda x: x * 2)
        assert mapped.is_success()
        assert mapped.value == 20
    
    def test_failure_is_failure(self):
        """测试 Failure.is_failure()"""
        result = Failure("error message", 5)
        assert result.is_failure() is True
        assert result.is_success() is False
    
    def test_failure_get_error(self):
        """测试 Failure.get_error()"""
        result = Failure("test error", 10)
        assert result.get_error() == "test error"
    
    def test_failure_get_value_raises(self):
        """测试 Failure.get_value() 抛出异常"""
        result = Failure("error", 0)
        with pytest.raises(ValueError):
            result.get_value()
    
    def test_failure_map(self):
        """测试 Failure.map()"""
        result = Failure("error", 5)
        mapped = result.map(lambda x: x * 2)
        assert mapped.is_failure()


class TestBasicParsers:
    """测试基础解析器"""
    
    def test_char_success(self):
        """测试 char 解析成功"""
        result = char('a').parse("abc")
        assert result.is_success()
        assert result.value == 'a'
        assert result.remaining == 'bc'
    
    def test_char_failure(self):
        """测试 char 解析失败"""
        result = char('x').parse("abc")
        assert result.is_failure()
    
    def test_char_invalid_input(self):
        """测试 char 无效输入"""
        with pytest.raises(ValueError):
            char("abc")  # 应该只接受单个字符
    
    def test_string_success(self):
        """测试 string 解析成功"""
        result = string("hello").parse("hello world")
        assert result.is_success()
        assert result.value == "hello"
        assert result.remaining == " world"
    
    def test_string_failure(self):
        """测试 string 解析失败"""
        result = string("hello").parse("hi there")
        assert result.is_failure()
    
    def test_string_exact_match(self):
        """测试 string 精确匹配"""
        result = string("abc").parse("abc")
        assert result.is_success()
        assert result.value == "abc"
        assert result.remaining == ""
    
    def test_satisfy_success(self):
        """测试 satisfy 解析成功"""
        result = satisfy(lambda c: c.isdigit(), "digit").parse("123")
        assert result.is_success()
        assert result.value == '1'
    
    def test_satisfy_failure(self):
        """测试 satisfy 解析失败"""
        result = satisfy(lambda c: c.isdigit(), "digit").parse("abc")
        assert result.is_failure()
    
    def test_digit(self):
        """测试 digit 解析器"""
        assert digit().parse("5").is_success()
        assert digit().parse("a").is_failure()
    
    def test_letter(self):
        """测试 letter 解析器"""
        assert letter().parse("a").is_success()
        assert letter().parse("A").is_success()
        assert letter().parse("5").is_failure()
    
    def test_alphanumeric(self):
        """测试 alphanumeric 解析器"""
        assert alphanumeric().parse("a").is_success()
        assert alphanumeric().parse("5").is_success()
        assert alphanumeric().parse("-").is_failure()
    
    def test_whitespace(self):
        """测试 whitespace 解析器"""
        assert whitespace().parse(" ").is_success()
        assert whitespace().parse("\t").is_success()
        assert whitespace().parse("\n").is_success()
        assert whitespace().parse("a").is_failure()
    
    def test_spaces(self):
        """测试 spaces 解析器"""
        result = spaces().parse("   abc")
        assert result.is_success()
        assert result.value == "   "
        assert result.remaining == "abc"
    
    def test_spaces_empty(self):
        """测试 spaces 解析空字符串"""
        result = spaces().parse("abc")
        assert result.is_success()
        assert result.value == ""
        assert result.remaining == "abc"
    
    def test_spaces1(self):
        """测试 spaces1 解析器"""
        assert spaces1().parse("  abc").is_success()
        assert spaces1().parse("abc").is_failure()
    
    def test_newline(self):
        """测试 newline 解析器"""
        assert newline().parse("\n").is_success()
        assert newline().parse("\r").is_success()
        assert newline().parse("a").is_failure()
    
    def test_tab(self):
        """测试 tab 解析器"""
        assert tab().parse("\t").is_success()
        assert tab().parse(" ").is_failure()
    
    def test_any_char(self):
        """测试 any_char 解析器"""
        assert any_char().parse("a").is_success()
        assert any_char().parse("1").is_success()
        assert any_char().parse(" ").is_success()
        assert any_char().parse("").is_failure()
    
    def test_none_of(self):
        """测试 none_of 解析器"""
        result = none_of("abc").parse("xyz")
        assert result.is_success()
        assert result.value == 'x'
        
        assert none_of("abc").parse("a").is_failure()
    
    def test_one_of(self):
        """测试 one_of 解析器"""
        result = one_of("abc").parse("cat")
        assert result.is_success()
        assert result.value == 'c'
        
        assert one_of("abc").parse("xyz").is_failure()


class TestCombinators:
    """测试组合子"""
    
    def test_sequence(self):
        """测试 sequence 组合子"""
        parser = sequence(char('a'), char('b'), char('c'))
        result = parser.parse("abcdef")
        assert result.is_success()
        assert result.value == ['a', 'b', 'c']
        assert result.remaining == "def"
    
    def test_sequence_failure(self):
        """测试 sequence 失败"""
        parser = sequence(char('a'), char('b'))
        result = parser.parse("acd")
        assert result.is_failure()
    
    def test_choice(self):
        """测试 choice 组合子"""
        parser = choice(char('a'), char('b'), char('c'))
        assert parser.parse("abc").value == 'a'
        assert parser.parse("bcd").value == 'b'
        assert parser.parse("cde").value == 'c'
    
    def test_choice_failure(self):
        """测试 choice 失败"""
        parser = choice(char('a'), char('b'))
        result = parser.parse("xyz")
        assert result.is_failure()
    
    def test_optional_success(self):
        """测试 optional 解析成功"""
        parser = optional(char('a'))
        result = parser.parse("abc")
        assert result.is_success()
        assert result.value == 'a'
    
    def test_optional_failure_returns_none(self):
        """测试 optional 失败返回 None"""
        parser = optional(char('x'))
        result = parser.parse("abc")
        assert result.is_success()
        assert result.value is None
    
    def test_many_zero(self):
        """测试 many 零次"""
        parser = many(char('x'))
        result = parser.parse("abc")
        assert result.is_success()
        assert result.value == []
    
    def test_many_multiple(self):
        """测试 many 多次"""
        parser = many(char('a'))
        result = parser.parse("aaabc")
        assert result.is_success()
        assert result.value == ['a', 'a', 'a']
    
    def test_many1_success(self):
        """测试 many1 成功"""
        parser = many1(digit())
        result = parser.parse("123abc")
        assert result.is_success()
        assert result.value == ['1', '2', '3']
    
    def test_many1_failure(self):
        """测试 many1 失败"""
        parser = many1(digit())
        result = parser.parse("abc")
        assert result.is_failure()
    
    def test_sep_by(self):
        """测试 sep_by 组合子"""
        parser = sep_by(digit(), char(','))
        result = parser.parse("1,2,3,abc")
        assert result.is_success()
        assert result.value == ['1', '2', '3']
    
    def test_sep_by_empty(self):
        """测试 sep_by 空列表"""
        parser = sep_by(digit(), char(','))
        result = parser.parse("abc")
        assert result.is_success()
        assert result.value == []
    
    def test_sep_by1(self):
        """测试 sep_by1 组合子"""
        parser = sep_by1(digit(), char(','))
        result = parser.parse("1,2,3")
        assert result.is_success()
        assert result.value == ['1', '2', '3']
    
    def test_sep_by1_failure(self):
        """测试 sep_by1 失败"""
        parser = sep_by1(digit(), char(','))
        result = parser.parse("abc")
        assert result.is_failure()
    
    def test_between(self):
        """测试 between 组合子"""
        parser = between(char('('), digit(), char(')'))
        result = parser.parse("(5)")
        assert result.is_success()
        assert result.value == '5'
    
    def test_between_failure(self):
        """测试 between 失败"""
        parser = between(char('('), digit(), char(')'))
        result = parser.parse("(a)")
        assert result.is_failure()
    
    def test_lazy(self):
        """测试 lazy 组合子"""
        # 用于递归定义
        def make_parser():
            return char('a')
        
        parser = lazy(make_parser)
        result = parser.parse("abc")
        assert result.is_success()
        assert result.value == 'a'
    
    def test_eof_success(self):
        """测试 eof 成功"""
        result = eof().parse("")
        assert result.is_success()
    
    def test_eof_failure(self):
        """测试 eof 失败"""
        result = eof().parse("a")
        assert result.is_failure()


class TestParserMethods:
    """测试 Parser 方法"""
    
    def test_map(self):
        """测试 map 方法"""
        parser = digit().map(int)
        result = parser.parse("5")
        assert result.is_success()
        assert result.value == 5
        assert isinstance(result.value, int)
    
    def test_map_chain(self):
        """测试 map 链式调用"""
        parser = digit().map(int).map(lambda x: x * 2)
        result = parser.parse("5")
        assert result.is_success()
        assert result.value == 10
    
    def test_bind(self):
        """测试 bind 方法"""
        parser = digit().bind(lambda d: string(d * 3))
        result = parser.parse("1" + "111")
        assert result.is_success()
        assert result.value == "111"
    
    def test_then(self):
        """测试 then 方法"""
        parser = char('a').then(char('b'))
        result = parser.parse("abc")
        assert result.is_success()
        assert result.value == 'b'
    
    def test_skip(self):
        """测试 skip 方法"""
        parser = char('a').skip(char('b'))
        result = parser.parse("abc")
        assert result.is_success()
        assert result.value == 'a'
    
    def test_or_else(self):
        """测试 or_else 方法"""
        parser = char('a').or_else(char('b'))
        assert parser.parse("abc").value == 'a'
        assert parser.parse("bcd").value == 'b'
    
    def test_parse_all(self):
        """测试 parse_all 方法"""
        parser = string("hello")
        result = parser.parse_all("hello")
        assert result.is_success()
        
        result = parser.parse_all("hello world")
        assert result.is_failure()
    
    def test_operator_or(self):
        """测试 | 运算符"""
        parser = char('a') | char('b')
        assert parser.parse("a").value == 'a'
        assert parser.parse("b").value == 'b'
    
    def test_operator_rshift(self):
        """测试 >> 运算符"""
        parser = char('a') >> char('b')
        result = parser.parse("ab")
        assert result.is_success()
        assert result.value == 'b'
    
    def test_operator_lshift(self):
        """测试 << 运算符"""
        parser = char('a') << char('b')
        result = parser.parse("ab")
        assert result.is_success()
        assert result.value == 'a'


class TestAdvancedParsers:
    """测试高级解析器"""
    
    def test_regex(self):
        """测试 regex 解析器"""
        parser = regex(r'\d+')
        result = parser.parse("123abc")
        assert result.is_success()
        assert result.value == "123"
    
    def test_regex_failure(self):
        """测试 regex 失败"""
        parser = regex(r'\d+')
        result = parser.parse("abc")
        assert result.is_failure()
    
    def test_integer(self):
        """测试 integer 解析器"""
        assert integer().parse("123").value == 123
        assert integer().parse("-456").value == -456
        assert integer().parse("+789").value == 789
    
    def test_integer_failure(self):
        """测试 integer 失败"""
        assert integer().parse("abc").is_failure()
    
    def test_float_num(self):
        """测试 float_num 解析器"""
        assert float_num().parse("3.14").value == 3.14
        assert float_num().parse("-2.5").value == -2.5
        assert float_num().parse("1e10").value == 1e10
        assert float_num().parse("1.5e-3").value == 1.5e-3
    
    def test_quoted_string(self):
        """测试 quoted_string 解析器"""
        parser = quoted_string('"')
        result = parser.parse('"hello"')
        assert result.is_success()
        assert result.value == "hello"
    
    def test_quoted_string_escape(self):
        """测试 quoted_string 转义"""
        parser = quoted_string('"')
        result = parser.parse(r'"hello\nworld"')
        assert result.is_success()
        assert result.value == "hello\nworld"
    
    def test_quoted_string_failure(self):
        """测试 quoted_string 失败"""
        parser = quoted_string('"')
        assert parser.parse('hello"').is_failure()
        assert parser.parse('"hello').is_failure()
    
    def test_identifier(self):
        """测试 identifier 解析器"""
        assert identifier().parse("hello").value == "hello"
        assert identifier().parse("_var").value == "_var"
        assert identifier().parse("var123").value == "var123"
    
    def test_identifier_failure(self):
        """测试 identifier 失败"""
        assert identifier().parse("123").is_failure()
    
    def test_keyword(self):
        """测试 keyword 解析器"""
        parser = keyword("if")
        assert parser.parse("if x").value == "if"
        assert parser.parse("if").value == "if"
    
    def test_keyword_not_identifier(self):
        """测试 keyword 不匹配标识符的一部分"""
        parser = keyword("if")
        # "iffy" 不应该匹配 "if"
        result = parser.parse("iffy")
        assert result.is_failure()


class TestUtilityFunctions:
    """测试工具函数"""
    
    def test_run_parser(self):
        """测试 run_parser"""
        result = run_parser(string("hello"), "hello")
        assert result.is_success()
        assert result.value == "hello"
    
    def test_run_parser_incomplete(self):
        """测试 run_parser 不完整输入"""
        result = run_parser(string("hello"), "hello world")
        assert result.is_failure()
    
    def test_parse_or_error_success(self):
        """测试 parse_or_error 成功"""
        value = parse_or_error(integer(), "123")
        assert value == 123
    
    def test_parse_or_error_failure(self):
        """测试 parse_or_error 失败"""
        with pytest.raises(ValueError):
            parse_or_error(integer(), "abc")


class TestJSONParser:
    """测试 JSON 解析器"""
    
    def test_json_null(self):
        """测试 JSON null"""
        result = parse_json("null")
        assert result.is_success()
        assert result.value is None
    
    def test_json_bool(self):
        """测试 JSON boolean"""
        assert parse_json("true").value is True
        assert parse_json("false").value is False
    
    def test_json_number(self):
        """测试 JSON number"""
        assert parse_json("42").value == 42
        assert parse_json("-17").value == -17
        assert parse_json("3.14").value == 3.14
        assert parse_json("1.5e-3").value == 1.5e-3
    
    def test_json_string(self):
        """测试 JSON string"""
        assert parse_json('"hello"').value == "hello"
        assert parse_json('""').value == ""
        result = parse_json(r'"hello\nworld"')
        assert result.is_success()
        assert result.value == "hello\nworld"
    
    def test_json_array(self):
        """测试 JSON array"""
        assert parse_json("[]").value == []
        assert parse_json("[1]").value == [1]
        assert parse_json("[1, 2, 3]").value == [1, 2, 3]
        assert parse_json('["a", "b"]').value == ["a", "b"]
    
    def test_json_object(self):
        """测试 JSON object"""
        assert parse_json("{}").value == {}
        result = parse_json('{"key": "value"}')
        assert result.value == {"key": "value"}
        result = parse_json('{"a": 1, "b": 2}')
        assert result.value == {"a": 1, "b": 2}
    
    def test_json_nested(self):
        """测试嵌套 JSON"""
        result = parse_json('{"arr": [1, 2, {"nested": true}]}')
        assert result.is_success()
        assert result.value == {"arr": [1, 2, {"nested": True}]}
    
    def test_json_with_whitespace(self):
        """测试带空白的 JSON"""
        result = parse_json('{ "key" : "value" }')
        assert result.is_success()
        assert result.value == {"key": "value"}
    
    def test_json_failure(self):
        """测试 JSON 解析失败"""
        assert parse_json("").is_failure()
        assert parse_json("{").is_failure()
        assert parse_json('{"key"').is_failure()


class TestComplexParsers:
    """测试复杂解析器"""
    
    def test_arithmetic_expression(self):
        """测试算术表达式解析"""
        # 数字解析器
        num = integer()
        
        # 表达式：数字 (运算符 数字)*
        op = one_of("+-*/")
        
        factor = num.map(lambda x: ('num', x))
        
        # 简单的表达式：数字 运算符 数字
        expr = sequence(
            num,
            spaces(),
            op,
            spaces(),
            num
        ).map(lambda parts: (parts[2], parts[0], parts[4]))
        
        result = expr.parse("1 + 2")
        assert result.is_success()
        assert result.value == ('+', 1, 2)
    
    def test_csv_line(self):
        """测试 CSV 行解析"""
        # 字段：非逗号字符序列
        field = many(none_of(',')).map(lambda cs: ''.join(cs))
        # 行：字段 (逗号 字段)*
        line = sep_by(field, char(','))
        
        result = line.parse("a,b,c")
        assert result.is_success()
        assert result.value == ['a', 'b', 'c']
        
        result = line.parse("hello,world,test")
        assert result.value == ['hello', 'world', 'test']
    
    def test_url_simple(self):
        """测试简单 URL 解析"""
        # 协议
        protocol = string("http://") | string("https://")
        # 域名（简化版：字母数字和点）
        domain = many1(one_of("abcdefghijklmnopqrstuvwxyz0123456789.-")).map(''.join)
        
        url = protocol.bind(lambda p: 
            domain.map(lambda d: {'protocol': p.rstrip('://'), 'domain': d})
        )
        
        result = url.parse("https://example.com")
        assert result.is_success()
        assert result.value['protocol'] == 'https'
        assert result.value['domain'] == 'example.com'
    
    def test_key_value_pair(self):
        """测试键值对解析"""
        key = identifier()
        value = many(none_of('=,')).map(lambda cs: ''.join(cs).strip())
        
        pair = sequence(
            key,
            spaces().skip(char('=')),
            value
        ).map(lambda parts: {parts[0]: parts[2]})
        
        result = pair.parse("name=John")
        assert result.is_success()
        assert result.value == {'name': 'John'}
    
    def test_recursive_parser(self):
        """测试递归解析器（括号匹配）"""
        # 使用 lazy 实现递归
        def expr_parser():
            # 表达式：数字 或 (表达式)
            def parse_func(input_str: str, pos: int):
                # 跳过空白
                while pos < len(input_str) and input_str[pos].isspace():
                    pos += 1
                
                if pos >= len(input_str):
                    return Failure("Expected expression", pos)
                
                if input_str[pos] == '(':
                    pos += 1
                    result = expr_parser()._parse(input_str, pos)
                    if result.is_failure():
                        return result
                    
                    # 期望右括号
                    pos = result.position
                    while pos < len(input_str) and input_str[pos].isspace():
                        pos += 1
                    
                    if pos >= len(input_str) or input_str[pos] != ')':
                        return Failure("Expected ')'", pos)
                    
                    return Success(result.value, input_str[pos+1:], pos + 1)
                
                # 解析数字
                start = pos
                while pos < len(input_str) and input_str[pos].isdigit():
                    pos += 1
                
                if pos == start:
                    return Failure("Expected digit", pos)
                
                return Success(int(input_str[start:pos]), input_str[pos:], pos)
            
            return Parser(parse_func)
        
        parser = expr_parser()
        
        # 测试基本数字
        result = parser.parse("123")
        assert result.is_success()
        assert result.value == 123
        
        # 测试括号
        result = parser.parse("(123)")
        assert result.is_success()
        assert result.value == 123
        
        # 测试嵌套括号
        result = parser.parse("((123))")
        assert result.is_success()
        assert result.value == 123


class TestEdgeCases:
    """测试边界情况"""
    
    def test_empty_input(self):
        """测试空输入"""
        assert char('a').parse("").is_failure()
        assert string("hello").parse("").is_failure()
    
    def test_unicode_characters(self):
        """测试 Unicode 字符"""
        result = char('你').parse("你好")
        assert result.is_success()
        assert result.value == '你'
    
    def test_very_long_input(self):
        """测试长输入"""
        long_string = "a" * 10000
        result = many1(char('a')).parse(long_string)
        assert result.is_success()
        assert len(result.value) == 10000
    
    def test_many_as_string(self):
        """测试 many 返回字符串"""
        result = many(letter()).map(lambda cs: ''.join(cs)).parse("hello")
        assert result.is_success()
        assert result.value == "hello"
    
    def test_nested_choice(self):
        """测试嵌套选择"""
        parser = choice(
            string("abc"),
            choice(string("ab"), string("a"))
        )
        # 应该优先匹配更长的
        assert parser.parse("abc").value == "abc"
        assert parser.parse("ab").value == "ab"
        assert parser.parse("a").value == "a"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
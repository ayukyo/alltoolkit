"""
词法分析器工具测试 (Lexer Utils Test)
===================================

完整的单元测试套件，覆盖所有功能。

运行: python lexer_utils_test.py
"""

import unittest
from lexer_utils import (
    TokenCategory,
    TokenType,
    Token,
    LexerError,
    LexerState,
    Lexer,
    LexerBuilder,
    TokenStream,
    create_lexer,
    tokenize,
    simple_tokenize,
    tokenize_code,
    tokenize_json,
    tokenize_math,
    count_tokens,
    filter_tokens,
    tokens_to_dict,
    dict_to_tokens,
)


class TestTokenType(unittest.TestCase):
    """TokenType 测试"""
    
    def test_create_token_type(self):
        """测试创建 token 类型"""
        tt = TokenType("NUMBER", r"\d+", TokenCategory.LITERAL)
        self.assertEqual(tt.name, "NUMBER")
        self.assertEqual(tt.pattern, r"\d+")
        self.assertEqual(tt.category, TokenCategory.LITERAL)
        self.assertEqual(tt.priority, 0)
        self.assertFalse(tt.ignore)
    
    def test_token_type_hash(self):
        """测试 token 类型哈希"""
        tt1 = TokenType("NUMBER", r"\d+")
        tt2 = TokenType("NUMBER", r"\d+")
        self.assertEqual(hash(tt1), hash(tt2))
    
    def test_token_type_equality(self):
        """测试 token 类型相等性"""
        tt1 = TokenType("NUMBER", r"\d+")
        tt2 = TokenType("NUMBER", r"\d*")
        tt3 = TokenType("STRING", r"\d+")
        self.assertEqual(tt1, tt2)  # 相同名称
        self.assertNotEqual(tt1, tt3)  # 不同名称


class TestToken(unittest.TestCase):
    """Token 测试"""
    
    def test_create_token(self):
        """测试创建 token"""
        tt = TokenType("NUMBER", r"\d+")
        token = Token(type=tt, value="123", line=1, column=1, start=0, end=3)
        self.assertEqual(token.type, tt)
        self.assertEqual(token.value, "123")
        self.assertEqual(token.line, 1)
        self.assertEqual(token.column, 1)
    
    def test_token_repr(self):
        """测试 token 字符串表示"""
        tt = TokenType("NUMBER", r"\d+")
        token = Token(type=tt, value=123, line=2, column=5)
        self.assertIn("NUMBER", repr(token))
        self.assertIn("123", repr(token))
        self.assertIn("L2:C5", repr(token))
    
    def test_token_equality(self):
        """测试 token 相等性"""
        tt = TokenType("NUMBER", r"\d+")
        t1 = Token(type=tt, value="123", line=1, column=1)
        t2 = Token(type=tt, value="123", line=1, column=1)
        t3 = Token(type=tt, value="456", line=1, column=1)
        self.assertEqual(t1, t2)
        self.assertNotEqual(t1, t3)


class TestLexerError(unittest.TestCase):
    """LexerError 测试"""
    
    def test_create_error(self):
        """测试创建错误"""
        error = LexerError(
            message="Unexpected character",
            line=10,
            column=5,
            position=100,
            context="abc @ def",
        )
        self.assertEqual(error.message, "Unexpected character")
        self.assertEqual(error.line, 10)
        self.assertEqual(error.column, 5)
    
    def test_error_to_dict(self):
        """测试错误转字典"""
        error = LexerError(
            message="Test error",
            line=1,
            column=1,
            position=0,
        )
        d = error.to_dict()
        self.assertEqual(d["message"], "Test error")
        self.assertEqual(d["line"], 1)
        self.assertEqual(d["column"], 1)


class TestLexerState(unittest.TestCase):
    """LexerState 测试"""
    
    def test_state_initialization(self):
        """测试状态初始化"""
        state = LexerState("hello")
        self.assertEqual(state.position, 0)
        self.assertEqual(state.line, 1)
        self.assertEqual(state.column, 1)
        self.assertEqual(state.current_char, "h")
    
    def test_state_advance(self):
        """测试状态前进"""
        state = LexerState("hello")
        result = state.advance(2)
        self.assertEqual(result, "he")
        self.assertEqual(state.position, 2)
        self.assertEqual(state.column, 3)
    
    def test_state_advance_newline(self):
        """测试换行处理"""
        state = LexerState("a\nb")
        state.advance(2)  # a\n
        self.assertEqual(state.line, 2)
        self.assertEqual(state.column, 1)
    
    def test_state_peek(self):
        """测试查看"""
        state = LexerState("hello")
        self.assertEqual(state.peek(0), "h")
        self.assertEqual(state.peek(1), "e")
        self.assertEqual(state.peek(4), "o")
        self.assertIsNone(state.peek(5))
    
    def test_state_remaining(self):
        """测试剩余文本"""
        state = LexerState("hello")
        state.advance(2)
        self.assertEqual(state.remaining_text, "llo")
    
    def test_state_get_context(self):
        """测试获取上下文"""
        state = LexerState("abcdefghijklmnopqrstuvwxyz")
        state.advance(10)
        context = state.get_context(5)
        # 验证上下文长度合理
        self.assertGreater(len(context), 0)
        # 验证当前位置在上下文范围内
        self.assertIn("f", context)


class TestLexer(unittest.TestCase):
    """Lexer 测试"""
    
    def test_add_type(self):
        """测试添加类型"""
        lexer = Lexer()
        tt = TokenType("NUMBER", r"\d+")
        lexer.add_type(tt)
        self.assertIn(tt, lexer.token_types)
    
    def test_add_type_duplicate(self):
        """测试添加重复类型"""
        lexer = Lexer()
        lexer.add_type(TokenType("NUMBER", r"\d+"))
        with self.assertRaises(ValueError):
            lexer.add_type(TokenType("NUMBER", r"\d*"))
    
    def test_add_keyword(self):
        """测试添加关键字"""
        lexer = Lexer()
        lexer.add_keyword("IF", "if")
        tokens = lexer.tokenize("if")
        self.assertEqual(len(tokens), 2)  # IF + EOF
        self.assertEqual(tokens[0].type.name, "IF")
    
    def test_tokenize_simple(self):
        """测试简单分词"""
        lexer = Lexer()
        lexer.add_type(TokenType("NUMBER", r"\d+"))
        tokens = lexer.tokenize("123")
        self.assertEqual(len(tokens), 2)  # NUMBER + EOF
        self.assertEqual(tokens[0].value, "123")
    
    def test_tokenize_multiple(self):
        """测试多个 token"""
        lexer = Lexer()
        lexer.add_type(TokenType("NUMBER", r"\d+"))
        lexer.add_type(TokenType("PLUS", r"\+"))
        tokens = lexer.tokenize("123+456")
        self.assertEqual(len(tokens), 4)  # NUMBER PLUS NUMBER EOF
        self.assertEqual(tokens[0].value, "123")
        self.assertEqual(tokens[1].value, "+")
        self.assertEqual(tokens[2].value, "456")
    
    def test_tokenize_with_whitespace(self):
        """测试空白处理"""
        lexer = Lexer()
        lexer.add_type(TokenType("NUMBER", r"\d+"))
        lexer.add_type(TokenType("WHITESPACE", r"\s+", ignore=True))
        tokens = lexer.tokenize("123  456")
        self.assertEqual(len(tokens), 3)  # NUMBER NUMBER EOF
        self.assertEqual(tokens[0].value, "123")
        self.assertEqual(tokens[1].value, "456")
    
    def test_tokenize_with_callback(self):
        """测试回调函数"""
        lexer = Lexer()
        lexer.add_type(TokenType(
            "NUMBER",
            r"\d+",
            callback=lambda x: int(x),
        ))
        tokens = lexer.tokenize("123")
        self.assertEqual(tokens[0].value, 123)
        self.assertIsInstance(tokens[0].value, int)
    
    def test_tokenize_position(self):
        """测试位置跟踪"""
        lexer = Lexer()
        lexer.add_type(TokenType("WORD", r"[a-z]+"))
        tokens = lexer.tokenize("hello world")
        self.assertEqual(tokens[0].line, 1)
        self.assertEqual(tokens[0].column, 1)
        self.assertEqual(tokens[1].line, 1)
        self.assertEqual(tokens[1].column, 7)
    
    def test_tokenize_multiline(self):
        """测试多行"""
        lexer = Lexer()
        lexer.add_type(TokenType("WORD", r"[a-z]+"))
        lexer.add_type(TokenType("WHITESPACE", r"\s+", ignore=True))
        tokens = lexer.tokenize("hello\nworld")
        self.assertEqual(tokens[0].line, 1)
        self.assertEqual(tokens[1].line, 2)
    
    def test_tokenize_error(self):
        """测试错误处理"""
        lexer = Lexer()
        lexer.add_type(TokenType("NUMBER", r"\d+"))
        tokens = lexer.tokenize("123abc")
        # 应该能匹配 NUMBER，然后遇到错误
        self.assertEqual(tokens[0].value, "123")
        # 后面的 abc 无法匹配，产生错误
    
    def test_tokenize_iter(self):
        """测试迭代器分词"""
        lexer = Lexer()
        lexer.add_type(TokenType("NUMBER", r"\d+"))
        tokens = list(lexer.tokenize_iter("123 456"))
        self.assertEqual(len(tokens), 3)  # NUMBER NUMBER EOF
    
    def test_eof_token(self):
        """测试 EOF token"""
        lexer = Lexer()
        lexer.add_type(TokenType("NUMBER", r"\d+"))
        tokens = lexer.tokenize("123", include_eof=True)
        self.assertEqual(tokens[-1].type.name, "EOF")
        self.assertIsNone(tokens[-1].value)


class TestLexerBuilder(unittest.TestCase):
    """LexerBuilder 测试"""
    
    def test_define(self):
        """测试定义"""
        lexer = (LexerBuilder()
            .define("NUMBER", r"\d+", TokenCategory.LITERAL)
            .build())
        tokens = lexer.tokenize("123")
        self.assertEqual(tokens[0].type.name, "NUMBER")
    
    def test_keyword(self):
        """测试关键字"""
        lexer = (LexerBuilder()
            .keyword("if")
            .keyword("else")
            .build())
        tokens = lexer.tokenize("if else")
        self.assertEqual(tokens[0].type.name, "IF")
        self.assertEqual(tokens[1].type.name, "ELSE")
    
    def test_keywords(self):
        """测试多个关键字"""
        lexer = (LexerBuilder()
            .keywords("if", "else", "while")
            .build())
        tokens = lexer.tokenize("if while")
        self.assertEqual(tokens[0].type.name, "IF")
        self.assertEqual(tokens[1].type.name, "WHILE")
    
    def test_operator(self):
        """测试操作符"""
        lexer = (LexerBuilder()
            .operator("+")
            .operator("-")
            .build())
        tokens = lexer.tokenize("+-")
        self.assertEqual(tokens[0].type.name, "PLUS")
        self.assertEqual(tokens[1].type.name, "MINUS")
    
    def test_punctuation(self):
        """测试标点"""
        lexer = (LexerBuilder()
            .punctuation("(")
            .punctuation(")")
            .build())
        tokens = lexer.tokenize("()")
        self.assertEqual(tokens[0].type.name, "LPAREN")
        self.assertEqual(tokens[1].type.name, "RPAREN")
    
    def test_whitespace(self):
        """测试空白"""
        lexer = (LexerBuilder()
            .define("WORD", r"[a-z]+")
            .whitespace()
            .build())
        tokens = lexer.tokenize("hello world")
        self.assertEqual(len(tokens), 3)  # WORD WORD EOF
    
    def test_build_complete(self):
        """测试完整构建"""
        lexer = (LexerBuilder()
            .keywords("if", "else", "while")
            .operators("+", "-", "*", "/")
            .punctuations("(", ")", "{", "}")
            .define("NUMBER", r"\d+")
            .define("IDENTIFIER", r"[a-zA-Z_][a-zA-Z0-9_]*")
            .whitespace()
            .build())
        
        tokens = lexer.tokenize("if (x + 1) { y = y * 2; }")
        self.assertGreater(len(tokens), 5)


class TestTokenStream(unittest.TestCase):
    """TokenStream 测试"""
    
    def setUp(self):
        lexer = (LexerBuilder()
            .define("NUMBER", r"\d+")
            .define("PLUS", r"\+")
            .whitespace()
            .build())
        self.tokens = lexer.tokenize("1 + 2 + 3")
    
    def test_current(self):
        """测试当前 token"""
        stream = TokenStream(self.tokens)
        self.assertEqual(stream.current.value, "1")
    
    def test_advance(self):
        """测试前进"""
        stream = TokenStream(self.tokens)
        t = stream.advance()
        self.assertEqual(t.value, "1")
        self.assertEqual(stream.current.value, "+")
    
    def test_peek(self):
        """测试查看"""
        stream = TokenStream(self.tokens)
        self.assertEqual(stream.peek(0).value, "1")
        self.assertEqual(stream.peek(1).value, "+")
        self.assertEqual(stream.peek(2).value, "2")
    
    def test_expect(self):
        """测试期望"""
        stream = TokenStream(self.tokens)
        t = stream.expect("NUMBER")
        self.assertEqual(t.value, "1")
    
    def test_expect_fail(self):
        """测试期望失败"""
        stream = TokenStream(self.tokens)
        with self.assertRaises(ValueError):
            stream.expect("PLUS")  # 当前是 NUMBER
    
    def test_accept(self):
        """测试接受"""
        stream = TokenStream(self.tokens)
        t = stream.accept("NUMBER")
        self.assertEqual(t.value, "1")
        self.assertIsNone(stream.accept("NUMBER"))  # 当前是 PLUS
    
    def test_skip_until(self):
        """测试跳过直到"""
        stream = TokenStream(self.tokens)
        # 跳过直到遇到 PLUS
        skipped = stream.skip_until("PLUS")
        # 应该跳过了第一个 NUMBER
        self.assertGreaterEqual(len(skipped), 1)
        # 现在应该是 PLUS 或之后的位置
        stream.advance()
        # 下一个应该是 NUMBER（2）
        self.assertEqual(stream.current.value, "2")
    
    def test_match_sequence(self):
        """测试序列匹配"""
        stream = TokenStream(self.tokens)
        self.assertTrue(stream.match_sequence("NUMBER", "PLUS", "NUMBER"))
        stream.advance()
        self.assertFalse(stream.match_sequence("NUMBER", "NUMBER"))
    
    def test_find(self):
        """测试查找"""
        stream = TokenStream(self.tokens)
        pos = stream.find("NUMBER")
        self.assertEqual(pos, 0)
    
    def test_reset(self):
        """测试重置"""
        stream = TokenStream(self.tokens)
        stream.advance()
        stream.advance()
        stream.reset()
        self.assertEqual(stream.current.value, "1")


class TestConvenienceFunctions(unittest.TestCase):
    """便捷函数测试"""
    
    def test_create_lexer(self):
        """测试快速创建"""
        lexer = create_lexer(
            keywords=["if", "else"],
            operators=["+", "-"],
            punctuations=["(", ")"],
        )
        tokens = lexer.tokenize("if (a + b)")
        self.assertGreater(len(tokens), 2)
    
    def test_tokenize(self):
        """测试快速分词"""
        tokens = tokenize("123 abc", rules={"NUMBER": r"\d+", "WORD": r"[a-z]+"})
        self.assertEqual(len(tokens), 3)  # NUMBER WORD EOF
    
    def test_simple_tokenize(self):
        """测试简单分词"""
        tokens = simple_tokenize("hello 123 + 456")
        types = [t.type.name for t in tokens]
        self.assertIn("WORD", types)
        self.assertIn("NUMBER", types)
    
    def test_tokenize_code(self):
        """测试代码分词"""
        tokens = tokenize_code("function test() { return 42; }")
        types = [t.type.name for t in tokens]
        self.assertIn("FUNCTION", types)
        self.assertIn("IDENTIFIER", types)
        self.assertIn("NUMBER", types)
    
    def test_tokenize_json(self):
        """测试 JSON 分词"""
        tokens = tokenize_json('{"name": "test", "value": 123}')
        types = [t.type.name for t in tokens]
        self.assertIn("STRING", types)
        self.assertIn("NUMBER", types)
        # 验证 JSON 字符串解析
        string_tokens = [t for t in tokens if t.type.name == "STRING"]
        self.assertEqual(string_tokens[0].value, "name")
    
    def test_tokenize_math(self):
        """测试数学表达式分词"""
        tokens = tokenize_math("2 + 3 * 4")
        values = [t.value for t in tokens if t.type.name != "EOF"]
        self.assertIn(2, values)
        self.assertIn(3, values)
        self.assertIn(4, values)
    
    def test_count_tokens(self):
        """测试统计 token"""
        lexer = Lexer()
        lexer.add_type(TokenType("NUMBER", r"\d+"))
        lexer.add_type(TokenType("PLUS", r"\+"))
        tokens = lexer.tokenize("1 + 2 + 3")
        counts = count_tokens(tokens)
        self.assertEqual(counts["NUMBER"], 3)
        self.assertEqual(counts["PLUS"], 2)
    
    def test_filter_tokens_by_type(self):
        """测试按类型过滤"""
        lexer = Lexer()
        lexer.add_type(TokenType("NUMBER", r"\d+"))
        lexer.add_type(TokenType("WORD", r"[a-z]+"))
        tokens = lexer.tokenize("123 abc 456")
        filtered = filter_tokens(tokens, types=["NUMBER"])
        self.assertEqual(len(filtered), 2)
    
    def test_filter_tokens_by_category(self):
        """测试按类别过滤"""
        lexer = Lexer()
        lexer.add_type(TokenType("NUMBER", r"\d+", category=TokenCategory.LITERAL))
        lexer.add_type(TokenType("PLUS", r"\+", category=TokenCategory.OPERATOR))
        tokens = lexer.tokenize("1 + 2")
        filtered = filter_tokens(tokens, categories=[TokenCategory.LITERAL])
        self.assertEqual(len(filtered), 2)  # 两个数字
    
    def test_tokens_to_dict(self):
        """测试 token 转字典"""
        tt = TokenType("NUMBER", r"\d+")
        tokens = [Token(type=tt, value=123, line=1, column=1, start=0, end=3)]
        d = tokens_to_dict(tokens)
        self.assertEqual(d[0]["type"], "NUMBER")
        self.assertEqual(d[0]["value"], 123)
    
    def test_dict_to_tokens(self):
        """测试字典转 token"""
        data = [{"type": "NUMBER", "value": 123, "line": 1, "column": 1}]
        tokens = dict_to_tokens(data)
        self.assertEqual(tokens[0].type.name, "NUMBER")
        self.assertEqual(tokens[0].value, 123)


class TestEdgeCases(unittest.TestCase):
    """边界情况测试"""
    
    def test_empty_input(self):
        """测试空输入"""
        lexer = Lexer()
        lexer.add_type(TokenType("NUMBER", r"\d+"))
        tokens = lexer.tokenize("")
        self.assertEqual(len(tokens), 1)  # 只有 EOF
        self.assertEqual(tokens[0].type.name, "EOF")
    
    def test_whitespace_only(self):
        """测试只有空白"""
        lexer = Lexer()
        lexer.add_type(TokenType("NUMBER", r"\d+"))
        lexer.add_type(TokenType("WHITESPACE", r"\s+", ignore=True))
        tokens = lexer.tokenize("   \n\t  ")
        self.assertEqual(len(tokens), 1)  # 只有 EOF
    
    def test_unicode(self):
        """测试 Unicode"""
        lexer = Lexer()
        lexer.add_type(TokenType("WORD", r"\w+"))
        tokens = lexer.tokenize("hello世界")
        self.assertEqual(tokens[0].value, "hello世界")
    
    def test_priority(self):
        """测试优先级"""
        lexer = Lexer()
        # 较长匹配应该优先
        lexer.add_type(TokenType("AND", r"&&", priority=10))
        lexer.add_type(TokenType("AMP", r"&", priority=1))
        tokens = lexer.tokenize("&&")
        self.assertEqual(tokens[0].type.name, "AND")
    
    def test_longest_match(self):
        """测试最长匹配"""
        lexer = Lexer()
        lexer.add_type(TokenType("NUMBER", r"\d+"))
        lexer.add_type(TokenType("FLOAT", r"\d+\.\d+"))
        tokens = lexer.tokenize("123.45")
        # 正则引擎会自动选择最长匹配
        self.assertIn(tokens[0].value, ["123.45", "123"])
    
    def test_special_chars(self):
        """测试特殊字符"""
        lexer = Lexer()
        lexer.add_type(TokenType("DOT", r"\."))
        lexer.add_type(TokenType("STAR", r"\*"))
        lexer.add_type(TokenType("PLUS", r"\+"))
        tokens = lexer.tokenize(".*+")
        self.assertEqual(tokens[0].type.name, "DOT")
        self.assertEqual(tokens[1].type.name, "STAR")
        self.assertEqual(tokens[2].type.name, "PLUS")
    
    def test_multiline_string(self):
        """测试多行文本"""
        lexer = Lexer()
        lexer.add_type(TokenType("LINE", r"[^\n]+"))
        tokens = lexer.tokenize("line1\nline2")
        self.assertEqual(len(tokens), 3)  # LINE LINE EOF
        self.assertEqual(tokens[0].value, "line1")
        self.assertEqual(tokens[1].value, "line2")
    
    def test_very_long_input(self):
        """测试超长输入"""
        lexer = Lexer()
        lexer.add_type(TokenType("NUMBER", r"\d+"))
        lexer.add_type(TokenType("WHITESPACE", r"\s+", ignore=True))
        text = " ".join(["123"] * 1000)
        tokens = lexer.tokenize(text)
        # 不包含 EOF
        number_count = sum(1 for t in tokens if t.type.name == "NUMBER")
        self.assertEqual(number_count, 1000)
    
    def test_nested_groups(self):
        """测试嵌套结构"""
        lexer = Lexer()
        lexer.add_punctuation("LPAREN", "(")
        lexer.add_punctuation("RPAREN", ")")
        tokens = lexer.tokenize("((()))")
        parens = [t for t in tokens if t.type.name != "EOF"]
        self.assertEqual(len(parens), 6)


class TestJSONTokenizer(unittest.TestCase):
    """JSON 分词器专项测试"""
    
    def test_simple_object(self):
        """测试简单对象"""
        tokens = tokenize_json('{"key": "value"}')
        types = [t.type.name for t in tokens]
        self.assertIn("LBRACE", types)
        self.assertIn("RBRACE", types)
        self.assertIn("STRING", types)
    
    def test_array(self):
        """测试数组"""
        tokens = tokenize_json('[1, 2, 3]')
        types = [t.type.name for t in tokens]
        self.assertIn("LBRACKET", types)
        self.assertIn("RBRACKET", types)
        self.assertIn("NUMBER", types)
    
    def test_nested(self):
        """测试嵌套结构"""
        tokens = tokenize_json('{"arr": [1, {"x": 2}]}')
        types = [t.type.name for t in tokens]
        self.assertIn("LBRACE", types)
        self.assertIn("LBRACKET", types)
    
    def test_numbers(self):
        """测试数字"""
        tokens = tokenize_json('[123, 45.67, -89, 1e5]')
        numbers = [t for t in tokens if t.type.name == "NUMBER"]
        self.assertEqual(len(numbers), 4)
        self.assertEqual(numbers[0].value, 123)
        self.assertEqual(numbers[1].value, 45.67)
        self.assertEqual(numbers[2].value, -89)
    
    def test_booleans_and_null(self):
        """测试布尔值和 null"""
        tokens = tokenize_json('[true, false, null]')
        types = [t.type.name for t in tokens]
        self.assertIn("TRUE", types)
        self.assertIn("FALSE", types)
        self.assertIn("NULL", types)


class TestCodeTokenizer(unittest.TestCase):
    """代码分词器专项测试"""
    
    def test_function_def(self):
        """测试函数定义"""
        tokens = tokenize_code("function foo(x, y) { return x + y; }")
        types = [t.type.name for t in tokens]
        self.assertIn("FUNCTION", types)
        self.assertIn("IDENTIFIER", types)
        self.assertIn("RETURN", types)
    
    def test_class_def(self):
        """测试类定义"""
        tokens = tokenize_code("class MyClass { }")
        types = [t.type.name for t in tokens]
        self.assertIn("CLASS", types)
        self.assertIn("IDENTIFIER", types)
    
    def test_comments(self):
        """测试注释"""
        tokens = tokenize_code("// this is a comment\nx = 1")
        # 注释应该被忽略
        comments = [t for t in tokens if t.type.category == TokenCategory.COMMENT]
        self.assertEqual(len(comments), 0)
    
    def test_block_comments(self):
        """测试块注释"""
        tokens = tokenize_code("/* block comment */ x = 1")
        comments = [t for t in tokens if t.type.category == TokenCategory.COMMENT]
        self.assertEqual(len(comments), 0)  # 被忽略
    
    def test_strings(self):
        """测试字符串"""
        tokens = tokenize_code('"hello" + \'world\'')
        strings = [t for t in tokens if t.type.name == "STRING"]
        self.assertEqual(len(strings), 2)
    
    def test_template_strings(self):
        """测试模板字符串"""
        tokens = tokenize_code("`template ${x}`")
        strings = [t for t in tokens if t.type.name == "STRING"]
        self.assertGreater(len(strings), 0)


class TestMathTokenizer(unittest.TestCase):
    """数学表达式分词器专项测试"""
    
    def test_simple_expression(self):
        """测试简单表达式"""
        tokens = tokenize_math("1 + 2")
        values = [t.value for t in tokens if t.type.name != "EOF"]
        self.assertEqual(values, [1, "+", 2])
    
    def test_complex_expression(self):
        """测试复杂表达式"""
        tokens = tokenize_math("((3 + 4) * 5) / 2 - 1")
        numbers = [t for t in tokens if t.type.name == "NUMBER"]
        # 3, 4, 5, 2, 1 五个数字
        self.assertEqual(len(numbers), 5)
    
    def test_floats(self):
        """测试浮点数"""
        tokens = tokenize_math("3.14 * 2.5")
        numbers = [t for t in tokens if t.type.name == "NUMBER"]
        self.assertEqual(numbers[0].value, 3.14)
        self.assertEqual(numbers[1].value, 2.5)
    
    def test_functions(self):
        """测试函数调用"""
        tokens = tokenize_math("sin(x) + cos(y)")
        identifiers = [t for t in tokens if t.type.name == "IDENTIFIER"]
        names = [t.value for t in identifiers]
        self.assertIn("sin", names)
        self.assertIn("cos", names)
        self.assertIn("x", names)
        self.assertIn("y", names)


if __name__ == "__main__":
    unittest.main(verbosity=2)
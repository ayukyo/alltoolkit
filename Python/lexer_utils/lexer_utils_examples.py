"""
词法分析器工具使用示例 (Lexer Utils Examples)
==========================================

演示 lexer_utils 的主要功能。

运行: python lexer_utils_examples.py
"""

from lexer_utils import (
    TokenCategory,
    TokenType,
    Token,
    LexerError,
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


def print_section(title: str):
    """打印分节标题"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print('='*60)


def print_tokens(tokens: list, limit: int = 10):
    """打印 token 列表"""
    for i, token in enumerate(tokens[:limit]):
        if token.type.name == "EOF":
            print(f"  [{i}] EOF")
        else:
            print(f"  [{i}] {token.type.name:15} = {token.value!r:20} @ L{token.line}:C{token.column}")
    if len(tokens) > limit:
        print(f"  ... ({len(tokens) - limit} more tokens)")


def example_1_basic_usage():
    """示例1: 基本用法"""
    print_section("示例1: 基本用法 - 创建简单的词法分析器")
    
    # 创建词法分析器
    lexer = Lexer()
    
    # 添加 token 类型
    lexer.add_type(TokenType("NUMBER", r"\d+", TokenCategory.LITERAL))
    lexer.add_type(TokenType("PLUS", r"\+", TokenCategory.OPERATOR))
    lexer.add_type(TokenType("MINUS", r"-", TokenCategory.OPERATOR))
    lexer.add_type(TokenType("WHITESPACE", r"\s+", TokenCategory.WHITESPACE, ignore=True))
    
    # 分析文本
    text = "123 + 456 - 789"
    tokens = lexer.tokenize(text)
    
    print(f"输入: {text}")
    print("Tokens:")
    print_tokens(tokens)


def example_2_builder_pattern():
    """示例2: 构建器模式"""
    print_section("示例2: 构建器模式 - 流畅 API 构建")
    
    # 使用构建器创建词法分析器
    lexer = (LexerBuilder()
        # 添加关键字
        .keywords("if", "else", "while", "for", "return", "function", "var", "let", "const")
        # 添加操作符
        .operators("+", "-", "*", "/", "%", "==", "!=", "<", ">", "<=", ">=", "&&", "||", "!")
        # 添加标点符号
        .punctuations("(", ")", "{", "}", "[", "]", ";", ",", ":", "=")
        # 添加标识符和数字
        .define("IDENTIFIER", r"[a-zA-Z_][a-zA-Z0-9_]*", TokenCategory.IDENTIFIER, priority=1)
        .define("NUMBER", r"\d+(\.\d+)?", TokenCategory.LITERAL)
        .define("STRING", r'"[^"]*"', TokenCategory.LITERAL)
        # 忽略空白
        .whitespace()
        .build())
    
    code = '''
    function factorial(n) {
        if (n <= 1) {
            return 1;
        }
        return n * factorial(n - 1);
    }
    '''
    
    tokens = lexer.tokenize(code)
    print(f"输入代码片段:")
    print(code)
    print("Tokens:")
    print_tokens(tokens, limit=15)


def example_3_callback_transform():
    """示例3: 回调转换"""
    print_section("示例3: 回调转换 - 自动转换 token 值")
    
    lexer = Lexer()
    
    # 数字自动转为 int/float
    lexer.add_type(TokenType(
        name="NUMBER",
        pattern=r"\d+(\.\d+)?",
        category=TokenCategory.LITERAL,
        callback=lambda x: float(x) if "." in x else int(x),
    ))
    
    # 字符串去除引号
    lexer.add_type(TokenType(
        name="STRING",
        pattern=r'"([^"\\]|\\.)*"',
        category=TokenCategory.LITERAL,
        callback=lambda x: x[1:-1].replace('\\"', '"'),
    ))
    
    lexer.add_type(TokenType("WHITESPACE", r"\s+", ignore=True))
    
    text = '42 3.14 "hello world" "test \\"quote\\""'
    tokens = lexer.tokenize(text)
    
    print(f"输入: {text}")
    print("Tokens (值已转换):")
    for token in tokens:
        if token.type.name != "EOF":
            print(f"  {token.type.name:10} = {token.value!r:20} (类型: {type(token.value).__name__})")


def example_4_error_handling():
    """示例4: 错误处理"""
    print_section("示例4: 错误处理 - 自定义错误处理器")
    
    errors = []
    
    def error_handler(error: LexerError) -> bool:
        errors.append(error)
        print(f"  错误: {error}")
        return True  # 继续分析
    
    lexer = Lexer()
    lexer.add_type(TokenType("NUMBER", r"\d+"))
    lexer.add_type(TokenType("WHITESPACE", r"\s+", ignore=True))
    lexer.on_error(error_handler)
    
    text = "123 abc 456 @@@ 789"
    tokens = lexer.tokenize(text)
    
    print(f"输入: {text}")
    print(f"\n成功匹配的 tokens:")
    print_tokens([t for t in tokens if t.type.name != "EOF"])
    print(f"\n遇到 {len(errors)} 个错误")


def example_5_stream_processing():
    """示例5: 流式处理"""
    print_section("示例5: 流式处理 - 迭代器模式")
    
    lexer = Lexer()
    lexer.add_type(TokenType("WORD", r"[a-zA-Z]+"))
    lexer.add_type(TokenType("NUMBER", r"\d+"))
    lexer.add_type(TokenType("WHITESPACE", r"\s+", ignore=True))
    
    text = "hello 123 world 456 foo 789 bar"
    
    print(f"输入: {text}")
    print("流式处理 tokens:")
    
    count = 0
    for token in lexer.tokenize_iter(text):
        if token.type.name == "EOF":
            print(f"  [EOF] 共处理 {count} 个 tokens")
            break
        count += 1
        print(f"  {count:3}. {token.type.name:10} = {token.value}")


def example_6_token_stream():
    """示例6: Token 流导航"""
    print_section("示例6: Token 流导航 - 查找和匹配")
    
    lexer = Lexer()
    lexer.add_type(TokenType("NUMBER", r"\d+"))
    lexer.add_type(TokenType("PLUS", r"\+"))
    lexer.add_type(TokenType("MINUS", r"-"))
    lexer.add_type(TokenType("WHITESPACE", r"\s+", ignore=True))
    
    text = "1 + 2 - 3 + 4 - 5"
    tokens = lexer.tokenize(text)
    stream = TokenStream(tokens)
    
    print(f"输入: {text}")
    print("\n导航操作:")
    
    # 查看当前
    print(f"  当前: {stream.current}")
    
    # 查看后续
    print(f"  peek(1): {stream.peek(1)}")
    print(f"  peek(2): {stream.peek(2)}")
    
    # 匹配序列
    print(f"  匹配 [NUMBER, PLUS, NUMBER]: {stream.match_sequence('NUMBER', 'PLUS', 'NUMBER')}")
    
    # 接受 token
    t = stream.accept("NUMBER")
    print(f"  接受 NUMBER: {t}")
    
    # 期望 token
    t = stream.expect("PLUS")
    print(f"  期望 PLUS: {t}")
    
    # 查找
    stream.reset()
    pos = stream.find("MINUS")
    print(f"  查找 MINUS 位置: {pos}")
    
    # 查找所有
    numbers = stream.find_all("NUMBER")
    print(f"  所有 NUMBER 位置: {numbers}")


def example_7_prebuilt_tokenizers():
    """示例7: 预构建分词器"""
    print_section("示例7: 预构建分词器 - 快速使用")
    
    # 简单分词
    print("\n7.1 simple_tokenize:")
    text = "hello world 123 + 456"
    tokens = simple_tokenize(text)
    print(f"  输入: {text}")
    print_tokens(tokens)
    
    # 代码分词
    print("\n7.2 tokenize_code:")
    code = "function add(a, b) { return a + b; }"
    tokens = tokenize_code(code)
    print(f"  输入: {code}")
    print_tokens(tokens, limit=12)
    
    # JSON 分词
    print("\n7.3 tokenize_json:")
    json_text = '{"name": "test", "value": 42, "active": true}'
    tokens = tokenize_json(json_text)
    print(f"  输入: {json_text}")
    print_tokens(tokens)
    
    # 数学表达式分词
    print("\n7.4 tokenize_math:")
    expr = "sin(x) * cos(y) + 3.14"
    tokens = tokenize_math(expr)
    print(f"  输入: {expr}")
    print_tokens(tokens)


def example_8_custom_language():
    """示例8: 自定义语言分词"""
    print_section("示例8: 自定义语言 - 简单计算器语言")
    
    # 定义一个简单的计算器语言
    lexer = (LexerBuilder()
        # 关键字
        .keyword("let", "LET")
        .keyword("print", "PRINT")
        # 数字（支持整数和小数）
        .define("NUMBER", r"\d+(\.\d+)?", TokenCategory.LITERAL, 
                callback=lambda x: float(x) if "." in x else int(x))
        # 标识符
        .define("IDENTIFIER", r"[a-zA-Z_][a-zA-Z0-9_]*", TokenCategory.IDENTIFIER, priority=1)
        # 操作符
        .operators("+", "-", "*", "/", "%", "^", "=")
        # 标点
        .punctuations("(", ")", ";")
        # 注释
        .define("COMMENT", r"#[^\n]*", TokenCategory.COMMENT, ignore=True)
        # 空白
        .whitespace()
        .build())
    
    program = '''
    # 简单计算器程序
    let x = 10;
    let y = 20;
    let result = (x + y) * 2;
    print result;
    '''
    
    tokens = lexer.tokenize(program)
    print(f"程序代码:{program}")
    print("Tokens:")
    print_tokens(tokens, limit=20)


def example_9_token_statistics():
    """示例9: Token 统计"""
    print_section("示例9: Token 统计和分析")
    
    code = '''
    function quicksort(arr) {
        if (arr.length <= 1) return arr;
        const pivot = arr[0];
        const left = arr.filter(x => x < pivot);
        const right = arr.filter(x => x > pivot);
        return [...quicksort(left), pivot, ...quicksort(right)];
    }
    '''
    
    tokens = tokenize_code(code)
    
    # 统计
    stats = count_tokens(tokens)
    print(f"代码片段:{code}")
    print("\nToken 统计:")
    for name, count in sorted(stats.items(), key=lambda x: -x[1]):
        print(f"  {name:15} : {count}")
    
    # 过滤
    print("\n过滤 - 只要标识符:")
    identifiers = filter_tokens(tokens, types=["IDENTIFIER"])
    id_names = [t.value for t in identifiers]
    print(f"  {id_names}")
    
    # 按类别过滤
    print("\n过滤 - 只要操作符:")
    operators = filter_tokens(tokens, categories=[TokenCategory.OPERATOR])
    op_names = [t.value for t in operators]
    print(f"  {op_names}")


def example_10_serialization():
    """示例10: 序列化"""
    print_section("示例10: Token 序列化 - 导出和导入")
    
    text = "hello + world * 123"
    tokens = simple_tokenize(text)
    
    print(f"原始输入: {text}")
    
    # 导出为字典
    data = tokens_to_dict(tokens)
    print(f"\n导出为字典 (JSON 格式):")
    for item in data:
        print(f"  {item}")
    
    # 从字典导入
    restored = dict_to_tokens(data)
    print(f"\n从字典恢复:")
    for token in restored:
        print(f"  {token}")


def example_11_position_tracking():
    """示例11: 位置跟踪"""
    print_section("示例11: 位置跟踪 - 精确的行列信息")
    
    code = '''line 1
line 2
line 3'''
    
    lexer = Lexer()
    lexer.add_type(TokenType("WORD", r"[a-z]+"))
    lexer.add_type(TokenType("NUMBER", r"\d+"))
    lexer.add_type(TokenType("WHITESPACE", r"\s+", ignore=True))
    
    tokens = lexer.tokenize(code)
    
    print(f"代码:\n{code}")
    print("\nToken 位置信息:")
    for token in tokens:
        if token.type.name != "EOF":
            print(f"  {token.value:8} @ 行 {token.line}, 列 {token.column}, 位置 [{token.start}:{token.end}]")


def example_12_priority_matching():
    """示例12: 优先级匹配"""
    print_section("示例12: 优先级匹配 - 关键字 vs 标识符")
    
    # 创建一个区分关键字和标识符的分词器
    lexer = Lexer()
    
    # 先添加标识符（低优先级）
    lexer.add_type(TokenType(
        name="IDENTIFIER",
        pattern=r"[a-zA-Z_][a-zA-Z0-9_]*",
        category=TokenCategory.IDENTIFIER,
        priority=1,
    ))
    
    # 添加关键字（高优先级）
    lexer.add_keyword("IF", "if", priority=100)
    lexer.add_keyword("WHILE", "while", priority=100)
    lexer.add_keyword("FOR", "for", priority=100)
    
    lexer.add_type(TokenType("WHITESPACE", r"\s+", ignore=True))
    
    text = "if condition while for_loop"
    tokens = lexer.tokenize(text)
    
    print(f"输入: {text}")
    print("Tokens (注意 if/while/for 被识别为关键字):")
    for token in tokens:
        if token.type.name != "EOF":
            print(f"  {token.value:15} -> {token.type.name}")


def example_13_complex_pattern():
    """示例13: 复杂模式匹配"""
    print_section("示例13: 复杂模式 - 正则表达式高级用法")
    
    lexer = Lexer()
    
    # 整数（支持二进制、八进制、十六进制）
    lexer.add_type(TokenType("INT_DEC", r"\d+", category=TokenCategory.LITERAL,
                             callback=lambda x: int(x)))
    lexer.add_type(TokenType("INT_HEX", r"0[xX][0-9a-fA-F]+", category=TokenCategory.LITERAL,
                             callback=lambda x: int(x, 16)))
    lexer.add_type(TokenType("INT_BIN", r"0[bB][01]+", category=TokenCategory.LITERAL,
                             callback=lambda x: int(x, 2)))
    lexer.add_type(TokenType("INT_OCT", r"0[oO][0-7]+", category=TokenCategory.LITERAL,
                             callback=lambda x: int(x, 8)))
    
    # 浮点数（科学计数法）
    lexer.add_type(TokenType("FLOAT", r"\d+\.\d+([eE][+-]?\d+)?", category=TokenCategory.LITERAL,
                             callback=lambda x: float(x)))
    
    # 字符串（支持转义）
    lexer.add_type(TokenType("STRING", r'"(?:[^"\\]|\\.)*"', category=TokenCategory.LITERAL,
                             callback=lambda x: x[1:-1].encode().decode('unicode_escape')))
    
    lexer.add_type(TokenType("WHITESPACE", r"\s+", ignore=True))
    
    text = '42 0xFF 0b1010 0o77 3.14e10 "hello\\nworld"'
    tokens = lexer.tokenize(text)
    
    print(f"输入: {text}")
    print("解析结果:")
    for token in tokens:
        if token.type.name != "EOF":
            print(f"  {token.type.name:10} = {token.value!r:20} (Python 类型: {type(token.value).__name__})")


def main():
    """运行所有示例"""
    example_1_basic_usage()
    example_2_builder_pattern()
    example_3_callback_transform()
    example_4_error_handling()
    example_5_stream_processing()
    example_6_token_stream()
    example_7_prebuilt_tokenizers()
    example_8_custom_language()
    example_9_token_statistics()
    example_10_serialization()
    example_11_position_tracking()
    example_12_priority_matching()
    example_13_complex_pattern()
    
    print("\n" + "="*60)
    print("  所有示例完成!")
    print("="*60)


if __name__ == "__main__":
    main()
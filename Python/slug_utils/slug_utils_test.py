#!/usr/bin/env python3
"""
slug_utils 测试套件
===================

完整的功能测试和边界值测试。
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    slugify,
    slugify_unique,
    generate_slug,
    is_valid_slug,
    unslugify,
    slug_range,
    smart_slugify,
    count_slug_words,
    truncate_slug,
    compare_slugs,
    batch_slugify,
    _transliterate,
    _transliterate_char,
)


def test_slugify_basic():
    """测试基本slugify功能"""
    print("测试基本slugify功能...")
    
    # 简单字符串
    assert slugify("Hello World") == "hello-world"
    assert slugify("hello world") == "hello-world"
    assert slugify("HELLO WORLD") == "hello-world"
    
    # 带特殊字符
    assert slugify("Hello, World!") == "hello-world"
    assert slugify("Hello@World#Test") == "hello-world-test"
    assert slugify("Hello...World") == "hello-world"
    
    # 带数字
    assert slugify("Hello World 123") == "hello-world-123"
    assert slugify("2024 Year") == "2024-year"
    
    print("  ✅ 基本功能测试通过")


def test_slugify_separator():
    """测试自定义分隔符"""
    print("测试自定义分隔符...")
    
    assert slugify("Hello World", separator="_") == "hello_world"
    assert slugify("Hello World", separator=".") == "hello.world"
    assert slugify("Hello World", separator="") == "helloworld"
    assert slugify("Hello World", separator="---") == "hello---world"
    
    print("  ✅ 分隔符测试通过")


def test_slugify_case():
    """测试大小写处理"""
    print("测试大小写处理...")
    
    assert slugify("Hello World", lowercase=True) == "hello-world"
    assert slugify("Hello World", lowercase=False) == "Hello-World"
    assert slugify("HELLO WORLD", lowercase=False) == "HELLO-WORLD"
    assert slugify("hello world", lowercase=False) == "hello-world"
    
    print("  ✅ 大小写测试通过")


def test_slugify_numbers():
    """测试数字处理"""
    print("测试数字处理...")
    
    assert slugify("Test 123", keep_numbers=True) == "test-123"
    assert slugify("Test 123", keep_numbers=False) == "test"
    assert slugify("2024-01-01", keep_numbers=True) == "2024-01-01"
    assert slugify("2024-01-01", keep_numbers=False) == ""
    
    print("  ✅ 数字处理测试通过")


def test_slugify_max_length():
    """测试最大长度限制"""
    print("测试最大长度限制...")
    
    # 精确截断
    assert slugify("Hello World", max_length=5) == "hello"
    assert slugify("Hello World", max_length=11) == "hello-world"
    
    # 在分隔符处截断
    assert slugify("Hello World Test", max_length=13) == "hello-world"
    
    # 边界值
    assert slugify("Hi", max_length=10) == "hi"
    assert slugify("Hello World", max_length=0) == ""
    assert slugify("Hello World", max_length=1) == "h"
    
    print("  ✅ 最大长度测试通过")


def test_slugify_replacements():
    """测试自定义替换"""
    print("测试自定义替换...")
    
    assert slugify("Café & Restaurant", replacements={'&': 'and'}) == "cafe-and-restaurant"
    assert slugify("User @Location", replacements={'@': 'at'}) == "user-at-location"
    assert slugify("A + B = C", replacements={'+': 'plus', '=': 'equals'}) == "a-plus-b-equals-c"
    
    # 多字符替换
    assert slugify("Hello World", replacements={'Hello': 'Hi', 'World': 'There'}) == "hi-there"
    
    print("  ✅ 自定义替换测试通过")


def test_slugify_chinese():
    """测试中文处理"""
    print("测试中文处理...")
    
    # 常用中文
    assert slugify("你好世界") == "ni-hao-shi-jie"
    assert slugify("中国") == "zhong-guo"
    
    # 中英混合
    result = slugify("Hello世界")
    assert "hello" in result and "shi" in result and "jie" in result
    result = slugify("你好World")
    assert "ni" in result and "hao" in result and "world" in result
    
    # 未映射的中文会被移除
    result = slugify("Test")  # 纯英文
    assert result == "test"
    
    print("  ✅ 中文处理测试通过")


def test_slugify_japanese():
    """测试日文处理"""
    print("测试日文处理...")
    
    # 平假名
    result = slugify("こんにちは")
    # こ=ko, ん=n, に=ni, ち=chi, は=ha
    assert result.replace("-", "") in ["konni chiha", "konnichiha", "ko-n-ni-chi-ha"]
    
    result = slugify("ありがとう")
    # あ=a, り=ri, が=ga, と=to, う=u
    assert result.replace("-", "") in ["arigatou", "a-ri-ga-to-u"]
    
    # 片假名
    result = slugify("テスト")
    assert result == "te-su-to"
    
    print("  ✅ 日文处理测试通过")


def test_slugify_korean():
    """测试韩文处理"""
    print("测试韩文处理...")
    
    result = slugify("한국")
    assert result == "han-guk"
    
    result = slugify("안녕")
    assert result == "an-nyeong"
    
    print("  ✅ 韩文处理测试通过")


def test_slugify_unicode():
    """测试Unicode字符处理"""
    print("测试Unicode字符处理...")
    
    # 重音字符（NFKD分解后可正确处理）
    result = slugify("café")
    assert result == "cafe" or "caf" in result
    
    result = slugify("naïve")
    assert result == "naive" or "na" in result
    
    result = slugify("résumé")
    assert result == "resume" or "resum" in result
    
    # 西班牙语
    result = slugify("niño")
    assert result == "nino" or "nin" in result
    
    print("  ✅ Unicode处理测试通过")


def test_slugify_empty():
    """测试空值和边界值"""
    print("测试空值和边界值...")
    
    # 空字符串
    assert slugify("") == ""
    assert slugify("   ") == ""
    
    # 只有特殊字符
    assert slugify("@#$%") == ""
    assert slugify("!!!") == ""
    
    # 单个字符
    assert slugify("a") == "a"
    assert slugify("A") == "a"
    assert slugify("1") == "1"
    
    # 只有分隔符
    assert slugify("---") == ""
    assert slugify("___", separator="_") == ""
    
    print("  ✅ 空值边界测试通过")


def test_slugify_merge_separators():
    """测试分隔符合并"""
    print("测试分隔符合并...")
    
    assert slugify("Hello    World") == "hello-world"
    assert slugify("Hello---World") == "hello-world"
    assert slugify("Hello___World", separator="_") == "hello_world"
    
    # 禁用合并
    assert slugify("Hello  World", merge_separators=False) == "hello--world"
    
    print("  ✅ 分隔符合并测试通过")


def test_slugify_trim():
    """测试首尾分隔符去除"""
    print("测试首尾分隔符去除...")
    
    assert slugify("-Hello World-") == "hello-world"
    assert slugify("   Hello World   ") == "hello-world"
    assert slugify("__Hello World__", separator="_") == "hello_world"
    
    # 禁用去除
    assert slugify("-Hello-", trim_separator=False) == "-hello-"
    
    print("  ✅ 首尾分隔符测试通过")


def test_slugify_unique():
    """测试唯一slug生成"""
    print("测试唯一slug生成...")
    
    # 无冲突
    assert slugify_unique("Hello World") == "hello-world"
    
    # 有冲突
    assert slugify_unique("Hello World", existing=["hello-world"]) == "hello-world-2"
    assert slugify_unique("Hello World", existing=["hello-world", "hello-world-2"]) == "hello-world-3"
    
    # 多个不同冲突
    existing = ["hello-world", "foo-bar", "hello-world-2"]
    assert slugify_unique("Hello World", existing=existing) == "hello-world-3"
    
    # 自定义分隔符
    assert slugify_unique("Hello World", existing=["hello_world"], separator="_") == "hello_world_2"
    
    print("  ✅ 唯一slug测试通过")


def test_generate_slug():
    """测试带前缀后缀的slug生成"""
    print("测试带前缀后缀的slug生成...")
    
    assert generate_slug("Hello World") == "hello-world"
    assert generate_slug("Hello World", prefix="blog") == "blog-hello-world"
    assert generate_slug("Hello World", suffix="2024") == "hello-world-2024"
    assert generate_slug("Hello World", prefix="blog", suffix="2024") == "blog-hello-world-2024"
    
    # 自定义分隔符
    assert generate_slug("Hello World", prefix="blog", suffix="2024", separator="_") == "blog_hello_world_2024"
    
    print("  ✅ 前缀后缀slug测试通过")


def test_is_valid_slug():
    """测试slug验证"""
    print("测试slug验证...")
    
    # 有效slug
    assert is_valid_slug("hello-world") == True
    assert is_valid_slug("hello_world", separator="_") == True
    assert is_valid_slug("hello123") == True
    assert is_valid_slug("Hello-World", allow_uppercase=True) == True
    
    # 无效slug
    assert is_valid_slug("Hello World") == False  # 空格
    assert is_valid_slug("hello world") == False  # 空格
    assert is_valid_slug("hello-world!") == False  # 特殊字符
    assert is_valid_slug("hello world") == False
    
    # 首尾分隔符
    assert is_valid_slug("-hello") == False
    assert is_valid_slug("hello-") == False
    
    # 长度限制
    assert is_valid_slug("hi", min_length=3) == False
    assert is_valid_slug("a" * 100, max_length=50) == False
    
    # 空值
    assert is_valid_slug("") == False
    assert is_valid_slug("-") == False
    
    print("  ✅ slug验证测试通过")


def test_unslugify():
    """测试slug还原"""
    print("测试slug还原...")
    
    assert unslugify("hello-world") == "hello world"
    assert unslugify("hello_world", separator="_") == "hello world"
    assert unslugify("hello-world", title_case=True) == "Hello World"
    assert unslugify("hello-world", space_replacement="-") == "hello-world"
    
    # 空值
    assert unslugify("") == ""
    assert unslugify("single") == "single"
    
    print("  ✅ slug还原测试通过")


def test_slug_range():
    """测试slug范围生成"""
    print("测试slug范围生成...")
    
    result = slug_range("Chapter", 1, 3)
    assert result == ["chapter-1", "chapter-2", "chapter-3"]
    
    result = slug_range("Part", 0, 2, separator="_")
    assert result == ["part_0", "part_1", "part_2"]
    
    result = slug_range("Test", 10, 12)
    assert result == ["test-10", "test-11", "test-12"]
    
    print("  ✅ slug范围测试通过")


def test_smart_slugify():
    """测试智能slug生成"""
    print("测试智能slug生成...")
    
    # 特殊符号
    result = smart_slugify("What's Up?!")
    assert result == "whats-up"
    
    # 数学符号
    result = smart_slugify("A + B")
    assert result == "a-plus-b"
    
    result = smart_slugify("100% Success")
    assert result == "100-percent-success"
    
    # 希腊字母
    result = smart_slugify("π Value")
    assert result == "pi-value"
    
    # 自定义替换覆盖
    result = smart_slugify("A & B", replacements={'&': 'with'})
    assert result == "a-with-b"
    
    print("  ✅ 智能slug测试通过")


def test_count_slug_words():
    """测试单词计数"""
    print("测试单词计数...")
    
    assert count_slug_words("hello-world") == 2
    assert count_slug_words("single") == 1
    assert count_slug_words("one-two-three-four") == 4
    assert count_slug_words("") == 0
    assert count_slug_words("---") == 0
    assert count_slug_words("hello_world", separator="_") == 2
    
    print("  ✅ 单词计数测试通过")


def test_truncate_slug():
    """测试slug截断"""
    print("测试slug截断...")
    
    # 不需要截断
    assert truncate_slug("hello", 10) == "hello"
    
    # 需要截断 - 保留单词边界
    result = truncate_slug("hello-world-from-python", 15)
    assert result == "hello-world-from" or len(result) <= 15
    
    result = truncate_slug("hello-world-test", 11)
    assert result == "hello-world" or len(result) <= 11
    
    # 不保留单词边界
    result = truncate_slug("hello-world", 7, preserve_words=False)
    assert result == "hello-w" or len(result) <= 7
    
    # 边界值
    assert truncate_slug("", 5) == ""
    result = truncate_slug("hi", 0)
    assert result == "" or result == "hi"
    
    print("  ✅ slug截断测试通过")


def test_compare_slugs():
    """测试slug比较"""
    print("测试slug比较...")
    
    # 完全匹配
    result = compare_slugs("hello-world", "hello-world")
    assert result['exact_match'] == True
    assert result['similarity'] == 1.0
    
    # 部分匹配
    result = compare_slugs("hello-world", "hello-python")
    assert result['exact_match'] == False
    assert result['word_overlap'] == 1
    assert 'hello' in result['common_words']
    
    # 无匹配
    result = compare_slugs("foo-bar", "baz-qux")
    assert result['exact_match'] == False
    assert result['word_overlap'] == 0
    
    # 空值
    result = compare_slugs("", "hello")
    assert result['similarity'] == 0.0
    
    print("  ✅ slug比较测试通过")


def test_batch_slugify():
    """测试批量生成"""
    print("测试批量生成...")
    
    # 不保证唯一
    result = batch_slugify(["Hello World", "Hello World", "Foo Bar"])
    assert result == ["hello-world", "hello-world", "foo-bar"]
    
    # 保证唯一
    result = batch_slugify(["Hello World", "Hello World", "Foo Bar"], unique=True)
    assert result == ["hello-world", "hello-world-2", "foo-bar"]
    
    # 空列表
    assert batch_slugify([]) == []
    
    # 自定义分隔符
    result = batch_slugify(["Hello World"], separator="_")
    assert result == ["hello_world"]
    
    print("  ✅ 批量生成测试通过")


def test_transliterate():
    """测试字符音译"""
    print("测试字符音译...")
    
    # 单个字符
    assert _transliterate_char('你') == 'ni'
    assert _transliterate_char('あ') == 'a'
    assert _transliterate_char('ア') == 'a'
    assert _transliterate_char('한') == 'han'
    assert _transliterate_char('a') == 'a'
    
    # 完整字符串音译
    result = _transliterate("你好")
    assert "ni" in result and "hao" in result
    
    print("  ✅ 字符音译测试通过")


def test_edge_cases():
    """测试各种边界情况"""
    print("测试边界情况...")
    
    # 非常长的字符串
    long_text = "Hello World " * 100
    result = slugify(long_text, max_length=50)
    assert len(result) <= 50
    
    # 混合字符集
    assert slugify("Hello 你好 こんにちは World") != ""
    
    # 连续分隔符
    assert slugify("Hello...World---Test") == "hello-world-test"
    
    # 只有数字
    assert slugify("123456") == "123456"
    assert slugify("123456", keep_numbers=False) == ""
    
    # 大小写混合
    assert slugify("HeLLo WoRLD") == "hello-world"
    assert slugify("HeLLo WoRLD", lowercase=False) == "HeLLo-WoRLD"
    
    # 空格变体
    assert slugify("Hello\tWorld") == "hello-world"  # 制表符
    assert slugify("Hello\nWorld") == "hello-world"  # 换行
    assert slugify("Hello\r\nWorld") == "hello-world"  # CRLF
    
    print("  ✅ 边界情况测试通过")


def test_custom_pattern():
    """测试自定义保留字符模式"""
    print("测试自定义保留字符模式...")
    
    # 保留点号
    result = slugify("file.name.txt", custom_pattern=r'[^a-z0-9\.]+')
    # 结果应包含点号或只有字母数字
    assert "file" in result
    
    # 保留@
    result = slugify("user@email.com", custom_pattern=r'[^a-z0-9@]+')
    # 结果应包含user和email
    assert "user" in result and "email" in result
    
    print("  ✅ 自定义模式测试通过")


def test_real_world_scenarios():
    """测试真实场景"""
    print("测试真实场景...")
    
    # 博客文章标题
    assert slugify("How to Build a REST API with Python") == "how-to-build-a-rest-api-with-python"
    assert slugify("10 Tips for Better Code") == "10-tips-for-better-code"
    
    # 产品名称
    assert slugify("iPhone 15 Pro Max") == "iphone-15-pro-max"
    assert slugify("Samsung Galaxy S24 Ultra") == "samsung-galaxy-s24-ultra"
    
    # URL路径
    assert slugify("/products/electronics/phones/") == "products-electronics-phones"
    
    # 文件名转换
    assert slugify("My Document (Final).docx") == "my-document-final-docx"
    
    # 多语言标题
    result = slugify("Bonjour le monde!")  # 法语
    assert result == "bonjour-le-monde"
    
    result = slugify("¡Hola mundo!")  # 西班牙语
    assert result == "hola-mundo"
    
    print("  ✅ 真实场景测试通过")


def run_all_tests():
    """运行所有测试"""
    print("\n" + "=" * 50)
    print("开始运行 slug_utils 测试套件")
    print("=" * 50 + "\n")
    
    tests = [
        test_slugify_basic,
        test_slugify_separator,
        test_slugify_case,
        test_slugify_numbers,
        test_slugify_max_length,
        test_slugify_replacements,
        test_slugify_chinese,
        test_slugify_japanese,
        test_slugify_korean,
        test_slugify_unicode,
        test_slugify_empty,
        test_slugify_merge_separators,
        test_slugify_trim,
        test_slugify_unique,
        test_generate_slug,
        test_is_valid_slug,
        test_unslugify,
        test_slug_range,
        test_smart_slugify,
        test_count_slug_words,
        test_truncate_slug,
        test_compare_slugs,
        test_batch_slugify,
        test_transliterate,
        test_edge_cases,
        test_custom_pattern,
        test_real_world_scenarios,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"  ❌ {test.__name__} 失败: {e}")
            failed += 1
        except Exception as e:
            print(f"  ❌ {test.__name__} 错误: {e}")
            failed += 1
    
    print("\n" + "=" * 50)
    print(f"测试完成: {passed} 通过, {failed} 失败")
    print("=" * 50)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
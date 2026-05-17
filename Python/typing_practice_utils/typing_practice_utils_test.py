#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Typing Practice Utils Test - 打字练习工具测试

测试模块：typing_practice_utils
测试用例数：45+
测试覆盖：文本生成、速度计算、准确率分析、练习会话、统计
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    TextGenerator, TypingAnalyzer, TypingPractice,
    TypingResult, Difficulty, TextType,
    generate_practice_text, analyze_typing, quick_practice
)


def test_result_collector():
    """测试结果收集器"""
    results = []
    
    def add_result(test_name: str, passed: bool, message: str = ""):
        results.append({
            "name": test_name,
            "passed": passed,
            "message": message
        })
    
    return results, add_result


def test_difficulty_enum(results, add_result):
    """测试难度枚举"""
    # test 1: 难度值
    add_result("Difficulty values", 
               Difficulty.EASY.value == "easy" and 
               Difficulty.HARD.value == "hard")


def test_text_type_enum(results, add_result):
    """测试文本类型枚举"""
    # test 2: 文本类型值
    add_result("TextType values", 
               TextType.WORDS.value == "words" and 
               TextType.CODE.value == "code")


def test_generate_words(results, add_result):
    """测试单词生成"""
    # test 3: 简单单词
    words_easy = TextGenerator.generate_words(10, Difficulty.EASY)
    add_result("generate_words easy", len(words_easy.split()) == 10)
    
    # test 4: 中等单词
    words_medium = TextGenerator.generate_words(20, Difficulty.MEDIUM)
    add_result("generate_words medium", len(words_medium.split()) == 20)
    
    # test 5: 困难单词
    words_hard = TextGenerator.generate_words(15, Difficulty.HARD)
    add_result("generate_words hard", len(words_hard.split()) == 15)
    
    # test 6: 专家级别
    words_expert = TextGenerator.generate_words(10, Difficulty.EXPERT)
    add_result("generate_words expert", len(words_expert.split()) == 10)


def test_generate_sentences(results, add_result):
    """测试句子生成"""
    # test 7: 句子生成
    sentence = TextGenerator.generate_sentence(Difficulty.EASY)
    add_result("generate_sentence", len(sentence) > 0)
    
    # test 8: 句子包含标点
    add_result("generate_sentence punctuation", 
               sentence.endswith('.') or sentence.endswith('!') or sentence.endswith('?'))


def test_generate_paragraphs(results, add_result):
    """测试段落生成"""
    # test 9: 段落生成
    paragraph = TextGenerator.generate_paragraph(sentences=2)
    add_result("generate_paragraph", len(paragraph) > 0)
    
    # test 10: 段落包含多个句子
    # 检查是否有多个句号
    periods = paragraph.count('.')
    add_result("generate_paragraph multiple sentences", periods >= 2)


def test_generate_code(results, add_result):
    """测试代码生成"""
    # test 11: 代码生成
    code = TextGenerator.generate_code(lines=3)
    add_result("generate_code", len(code) > 0)
    
    # test 12: 代码包含多行
    add_result("generate_code multiple lines", code.count('\n') >= 2)


def test_generate_numbers(results, add_result):
    """测试数字生成"""
    # test 13: 数字生成
    numbers = TextGenerator.generate_numbers(count=5)
    add_result("generate_numbers", len(numbers.split()) == 5)
    
    # test 14: 数字格式正确
    add_result("generate_numbers format", 
               all(c.isdigit() or c in '.,- ' for c in numbers))


def test_generate_mixed(results, add_result):
    """测试混合生成"""
    # test 15: 混合文本
    mixed = TextGenerator.generate_mixed(length=50)
    add_result("generate_mixed", len(mixed) >= 50)


def test_generate_generic(results, add_result):
    """测试通用生成"""
    # test 16: WORDS 类型
    words = TextGenerator.generate(TextType.WORDS, Difficulty.EASY, count=20)
    add_result("generate WORDS", len(words.split()) == 20)
    
    # test 17: SENTENCES 类型
    sentence = TextGenerator.generate(TextType.SENTENCES, Difficulty.MEDIUM)
    add_result("generate SENTENCES", len(sentence) > 0)
    
    # test 18: PARAGRAPHS 类型
    paragraph = TextGenerator.generate(TextType.PARAGRAPHS, sentences=3)
    add_result("generate PARAGRAPHS", len(paragraph) > 0)
    
    # test 19: CODE 类型
    code = TextGenerator.generate(TextType.CODE, lines=5)
    add_result("generate CODE", len(code) > 0)
    
    # test 20: NUMBERS 类型
    numbers = TextGenerator.generate(TextType.NUMBERS, count=10)
    add_result("generate NUMBERS", len(numbers.split()) == 10)
    
    # test 21: MIXED 类型
    mixed = TextGenerator.generate(TextType.MIXED, length=40)
    add_result("generate MIXED", len(mixed) >= 40)


def test_calculate_wpm(results, add_result):
    """测试 WPM 计算"""
    # test 22: 基础 WPM
    text = "Hello world this is a test"
    wpm = TypingAnalyzer.calculate_wpm(text, 10)  # 10秒
    # 28字符 / 5 = 5.6词, 5.6词 / (10/60分) = 33.6 WPM
    expected = len(text) / 5 / (10 / 60)
    add_result("calculate_wpm basic", abs(wpm - expected) < 0.1)
    
    # test 23: 零时间 WPM
    wpm_zero = TypingAnalyzer.calculate_wpm(text, 0)
    add_result("calculate_wpm zero time", wpm_zero == 0)


def test_calculate_cpm(results, add_result):
    """测试 CPM 计算"""
    # test 24: 基础 CPM
    text = "Hello world"
    cpm = TypingAnalyzer.calculate_cpm(text, 5)  # 5秒
    # 11字符 / (5/60分) = 132 CPM
    expected = len(text) / (5 / 60)
    add_result("calculate_cpm basic", abs(cpm - expected) < 0.1)
    
    # test 25: 零时间 CPM
    cpm_zero = TypingAnalyzer.calculate_cpm(text, 0)
    add_result("calculate_cpm zero time", cpm_zero == 0)


def test_calculate_accuracy(results, add_result):
    """测试准确率计算"""
    # test 26: 100% 准确率
    original = "Hello"
    typed = "Hello"
    accuracy, correct, total, errors = TypingAnalyzer.calculate_accuracy(original, typed)
    add_result("calculate_accuracy 100%", accuracy == 100 and len(errors) == 0)
    
    # test 27: 有错误
    original = "Hello"
    typed = "Helo"
    accuracy, correct, total, errors = TypingAnalyzer.calculate_accuracy(original, typed)
    add_result("calculate_accuracy with errors", accuracy < 100 and len(errors) > 0)
    
    # test 28: 输入更长
    original = "Hello"
    typed = "Hello World"
    accuracy, correct, total, errors = TypingAnalyzer.calculate_accuracy(original, typed)
    add_result("calculate_accuracy longer typed", len(errors) > 0)
    
    # test 29: 输入更短
    original = "Hello World"
    typed = "Hello"
    accuracy, correct, total, errors = TypingAnalyzer.calculate_accuracy(original, typed)
    add_result("calculate_accuracy shorter typed", len(errors) > 0)
    
    # test 30: 空文本
    accuracy, correct, total, errors = TypingAnalyzer.calculate_accuracy("", "")
    add_result("calculate_accuracy empty", accuracy == 100)


def test_typing_result(results, add_result):
    """测试 TypingResult"""
    # test 31: 创建结果
    result = TypingResult(
        original_text="Hello",
        typed_text="Hello",
        time_seconds=5,
        correct_chars=5,
        total_chars=5,
        errors=[],
        wpm=60,
        cpm=60,
        accuracy=100
    )
    
    str_repr = str(result)
    add_result("TypingResult str", "WPM" in str_repr and "准确率" in str_repr)


def test_analyze(results, add_result):
    """测试完整分析"""
    # test 32: 完整分析
    original = "The quick brown fox"
    typed = "The quikc brown fox"
    result = TypingAnalyzer.analyze(original, typed, 5)
    
    add_result("analyze result", 
               result.wpm > 0 and 
               0 <= result.accuracy <= 100 and
               len(result.errors) > 0)


def test_typing_practice(results, add_result):
    """测试 TypingPractice 类"""
    practice = TypingPractice()
    
    # test 33: 开始会话
    text = practice.start_session(TextType.WORDS, Difficulty.EASY, count=20)
    add_result("start_session", len(text.split()) == 20)
    
    # test 34: 获取统计（无历史）
    stats = practice.get_statistics()
    add_result("get_statistics empty", stats["total_sessions"] == 0)
    
    # test 35: 清除历史
    practice.clear_history()
    add_result("clear_history", len(practice.history) == 0)


def test_performance_level(results, add_result):
    """测试性能等级"""
    # test 36: 初级
    add_result("get_performance_level beginner", 
               TypingPractice.get_performance_level(15) == "初级 (Beginner)")
    
    # test 37: 专家
    add_result("get_performance_level expert", 
               TypingPractice.get_performance_level(65) == "专家 (Expert)")
    
    # test 38: 大师
    add_result("get_performance_level master", 
               TypingPractice.get_performance_level(85) == "大师 (Master)")
    
    # test 39: 中级
    add_result("get_performance_level intermediate", 
               TypingPractice.get_performance_level(35) == "中级 (Intermediate)")


def test_convenience_functions(results, add_result):
    """测试便捷函数"""
    # test 40: generate_practice_text
    text = generate_practice_text(TextType.WORDS, Difficulty.EASY, count=10)
    add_result("generate_practice_text", len(text.split()) == 10)
    
    # test 41: analyze_typing
    result = analyze_typing("Test", "Test", 3)
    add_result("analyze_typing convenience", result.accuracy == 100)
    
    # test 42: quick_practice
    text, finish_func = quick_practice(Difficulty.EASY, word_count=10)
    add_result("quick_practice text", len(text.split()) == 10)


def test_statistics_with_history(results, add_result):
    """测试带历史的统计"""
    practice = TypingPractice()
    
    # 模拟多次练习
    for i in range(5):
        practice.start_session(TextType.WORDS, Difficulty.EASY, count=10)
        practice.begin_typing()
        # 直接模拟结果（不实际输入）
        result = TypingResult(
            original_text="test text",
            typed_text="test text",
            time_seconds=5 + i,
            correct_chars=9,
            total_chars=9,
            errors=[],
            wpm=60 + i * 5,
            cpm=100 + i * 10,
            accuracy=100
        )
        practice.history.append(result)
    
    # test 43: 历史统计
    stats = practice.get_statistics()
    add_result("get_statistics with history", 
               stats["total_sessions"] == 5 and
               stats["average_wpm"] > 0)


def test_error_details(results, add_result):
    """测试错误详情"""
    original = "Hello World"
    typed = "Helo Wrld"
    
    accuracy, correct, total, errors = TypingAnalyzer.calculate_accuracy(original, typed)
    
    # test 44: 错误位置
    add_result("error positions", 
               all(isinstance(e[0], int) for e in errors))
    
    # test 45: 错误包含期望和实际
    add_result("error details", 
               all(len(e) == 3 for e in errors))


def main():
    """运行所有测试"""
    results, add_result = test_result_collector()
    
    # 运行各测试组
    test_difficulty_enum(results, add_result)
    test_text_type_enum(results, add_result)
    test_generate_words(results, add_result)
    test_generate_sentences(results, add_result)
    test_generate_paragraphs(results, add_result)
    test_generate_code(results, add_result)
    test_generate_numbers(results, add_result)
    test_generate_mixed(results, add_result)
    test_generate_generic(results, add_result)
    test_calculate_wpm(results, add_result)
    test_calculate_cpm(results, add_result)
    test_calculate_accuracy(results, add_result)
    test_typing_result(results, add_result)
    test_analyze(results, add_result)
    test_typing_practice(results, add_result)
    test_performance_level(results, add_result)
    test_convenience_functions(results, add_result)
    test_statistics_with_history(results, add_result)
    test_error_details(results, add_result)
    
    # 输出结果
    passed = sum(1 for r in results if r["passed"])
    total = len(results)
    
    print("=" * 60)
    print("Typing Practice Utils Test Results")
    print("=" * 60)
    
    for r in results:
        status = "✅" if r["passed"] else "❌"
        print(f"{status} {r['name']}: {r['message']}")
    
    print("-" * 60)
    print(f"Summary: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    print("=" * 60)
    
    return passed, total


if __name__ == "__main__":
    passed, total = main()
    sys.exit(0 if passed == total else 1)
#!/usr/bin/env python3
"""
阅读统计工具 - 基本用法示例

演示如何使用 reading_stats_utils 进行文本分析。
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    analyze_text,
    format_time,
    get_reading_suggestions,
    estimate_audience,
    classify_text_type
)


def example_basic_analysis():
    """基本文本分析示例"""
    print("=" * 60)
    print("基本文本分析")
    print("=" * 60)
    
    text = """
    The quick brown fox jumps over the lazy dog. This sentence contains 
    every letter of the alphabet. It is a classic example used in typing 
    practice and font display testing.
    """
    
    stats = analyze_text(text)
    
    print(f"\n文本预览: {text.strip()[:50]}...")
    print(f"\n【基础统计】")
    print(f"  字符数: {stats.character_count}")
    print(f"  字符数(不含空格): {stats.character_count_no_spaces}")
    print(f"  单词数: {stats.word_count}")
    print(f"  句子数: {stats.sentence_count}")
    print(f"  段落数: {stats.paragraph_count}")
    print(f"  音节数: {stats.syllable_count}")
    
    print(f"\n【时间估算】")
    print(f"  阅读时间: {format_time(stats.reading_time_minutes)}")
    print(f"  朗读时间: {format_time(stats.speaking_time_minutes)}")
    
    print(f"\n【平均值统计】")
    print(f"  平均词长: {stats.avg_word_length:.2f} 字符")
    print(f"  平均句长: {stats.avg_sentence_length:.2f} 词")
    print(f"  每词平均音节: {stats.avg_syllables_per_word:.2f}")
    
    print(f"\n【可读性指数】")
    print(f"  Flesch Reading Ease: {stats.flesch_reading_ease:.1f}")
    print(f"  Flesch-Kincaid Grade: {stats.flesch_kincaid_grade:.1f}")
    print(f"  Gunning Fog Index: {stats.gunning_fog_index:.1f}")
    print(f"  Coleman-Liau Index: {stats.coleman_liau_index:.1f}")
    print(f"  ARI: {stats.automated_readability_index:.1f}")
    
    print(f"\n【复杂度】")
    print(f"  复杂词数: {stats.complex_word_count}")
    print(f"  生僻词数: {stats.difficult_word_count}")
    print(f"  不重复词数: {stats.unique_word_count}")
    print(f"  词汇密度: {stats.vocabulary_density:.2%}")
    
    print(f"\n【可读性评估】")
    print(f"  可读性等级: {stats.readability_level}")
    print(f"  目标受众: {estimate_audience(stats)}")
    print(f"  可能类型: {', '.join(classify_text_type(stats))}")
    
    print(f"\n【改进建议】")
    for suggestion in get_reading_suggestions(stats):
        print(f"  • {suggestion}")


def example_text_comparison():
    """文本比较示例"""
    print("\n" + "=" * 60)
    print("文本比较")
    print("=" * 60)
    
    from mod import compare_texts
    
    text1 = """
    The cat sat on the mat. It was a sunny day. The cat was happy.
    Birds sang in the trees. Everything was peaceful.
    """
    
    text2 = """
    The implementation of sophisticated algorithms necessitates 
    comprehensive understanding of computational complexity, 
    mathematical foundations, and software engineering principles.
    """
    
    print(f"\n文本1预览: {text1.strip()[:40]}...")
    print(f"文本2预览: {text2.strip()[:40]}...")
    
    comparison = compare_texts(text1, text2)
    
    print(f"\n【比较结果】")
    print(f"  单词数: 文本1={comparison['word_count'][0]}, 文本2={comparison['word_count'][1]}")
    print(f"  句子数: 文本1={comparison['sentence_count'][0]}, 文本2={comparison['sentence_count'][1]}")
    print(f"  阅读时间: 文本1={comparison['reading_time'][0]:.2f}分钟, 文本2={comparison['reading_time'][1]:.2f}分钟")
    print(f"  Flesch分数: 文本1={comparison['flesch_reading_ease'][0]:.1f}, 文本2={comparison['flesch_reading_ease'][1]:.1f}")
    print(f"  年级水平: 文本1={comparison['flesch_kincaid_grade'][0]:.1f}, 文本2={comparison['flesch_kincaid_grade'][1]:.1f}")
    print(f"  词汇密度: 文本1={comparison['vocabulary_density'][0]:.2%}, 文本2={comparison['vocabulary_density'][1]:.2%}")


def example_time_estimation():
    """时间估算示例"""
    print("\n" + "=" * 60)
    print("阅读时间估算")
    print("=" * 60)
    
    from mod import reading_time, speaking_time
    
    texts = [
        ("短文本", "Hello world!"),
        ("中等文本", "The quick brown fox jumps over the lazy dog. " * 10),
        ("长文本", "Lorem ipsum dolor sit amet. " * 100),
    ]
    
    print(f"\n{'文本类型':<10} {'阅读时间':<15} {'朗读时间':<15}")
    print("-" * 40)
    
    for name, text in texts:
        read_time = reading_time(text)
        speak_time = speaking_time(text)
        print(f"{name:<10} {format_time(read_time):<15} {format_time(speak_time):<15}")


def example_language_detection():
    """语言检测示例"""
    print("\n" + "=" * 60)
    print("语言检测")
    print("=" * 60)
    
    from mod import detect_language
    
    texts = [
        ("纯英文", "Hello world, how are you today?"),
        ("纯中文", "你好世界，今天天气真好。"),
        ("中日混合", "Hello こんにちは 世界"),
        ("中英混合", "Python 是一门优秀的编程语言"),
    ]
    
    print(f"\n{'文本类型':<10} {'英文占比':<10} {'中文占比':<10} {'日文占比':<10}")
    print("-" * 45)
    
    for name, text in texts:
        lang = detect_language(text)
        print(f"{name:<10} {lang['english']*100:>6.1f}%   {lang['chinese']*100:>6.1f}%   {lang['japanese']*100:>6.1f}%")


def example_readability_levels():
    """可读性等级示例"""
    print("\n" + "=" * 60)
    print("不同可读性等级的文本")
    print("=" * 60)
    
    texts = [
        ("儿童读物", "The cat sat. The dog ran. It was fun."),
        ("新闻文章", "The government announced new policies today. Officials say the changes will benefit many citizens."),
        ("学术论文", "The implementation of sophisticated algorithms necessitates comprehensive understanding of computational complexity."),
    ]
    
    for name, text in texts:
        stats = analyze_text(text)
        print(f"\n【{name}】")
        print(f"  文本: {text[:50]}...")
        print(f"  Flesch分数: {stats.flesch_reading_ease:.1f}")
        print(f"  年级水平: {stats.flesch_kincaid_grade:.1f}")
        print(f"  可读性等级: {stats.readability_level}")
        print(f"  目标受众: {estimate_audience(stats)}")


if __name__ == "__main__":
    example_basic_analysis()
    example_text_comparison()
    example_time_estimation()
    example_language_detection()
    example_readability_levels()
    
    print("\n" + "=" * 60)
    print("示例运行完成!")
    print("=" * 60)
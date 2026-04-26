"""
音节计数工具使用示例

演示功能：
1. 基本单词音节计数
2. 句子音节分析
3. 诗歌韵律分析
4. 俳句建议
5. 可读性分析
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    count_syllables,
    count_sentence_syllables,
    get_syllable_pattern,
    get_syllable_breakdown,
    analyze_rhyme_scheme,
    get_stress_pattern,
    suggest_haiku_lines,
    readability_score,
    count_complex_words,
    split_into_syllables,
    get_word_rhythm,
    batch_count_syllables,
    get_syllable_stats,
    generate_syllable_word_list
)


def example_basic_count():
    """示例1: 基本单词音节计数"""
    print("\n" + "=" * 50)
    print("示例1: 基本单词音节计数")
    print("=" * 50)
    
    words = [
        "hello", "world", "beautiful", "programming",
        "information", "development", "experience",
        "university", "opportunity", "communication"
    ]
    
    print("\n单词音节计数:")
    for word in words:
        syllables = count_syllables(word)
        print(f"  {word}: {syllables} 音节")


def example_sentence_analysis():
    """示例2: 句子音节分析"""
    print("\n" + "=" * 50)
    print("示例2: 句子音节分析")
    print("=" * 50)
    
    sentences = [
        "Hello world",
        "I love programming",
        "The quick brown fox jumps over the lazy dog",
        "Beautiful weather makes for a wonderful day"
    ]
    
    print("\n句子分析:")
    for sentence in sentences:
        total = count_sentence_syllables(sentence)
        pattern = get_syllable_pattern(sentence)
        print(f"  '{sentence}'")
        print(f"    总音节: {total}, 模式: {pattern}")


def example_word_breakdown():
    """示例3: 单词详细分析"""
    print("\n" + "=" * 50)
    print("示例3: 单词详细分析")
    print("=" * 50)
    
    words = ["beautiful", "programming", "information", "extraordinary"]
    
    print("\n单词详细分析:")
    for word in words:
        breakdown = get_syllable_breakdown(word)
        rhythm = get_word_rhythm(word)
        stress = get_stress_pattern(word)
        syllable_parts = split_into_syllables(word)
        
        print(f"\n  {word}:")
        print(f"    音节数: {breakdown['syllables']}")
        print(f"    方法: {breakdown['method']}")
        print(f"    节奏: {rhythm}")
        print(f"    重音: {stress}")
        print(f"    拆分: {syllable_parts}")


def example_poetry_analysis():
    """示例4: 诗歌韵律分析"""
    print("\n" + "=" * 50)
    print("示例4: 诗歌韵律分析")
    print("=" * 50)
    
    poems = [
        """The stars shine bright
In the quiet night
Dreams take their flight
With all their might""",
        """Roses are red
Violets are blue
Sugar is sweet
And so are you"""
    ]
    
    for i, poem in enumerate(poems, 1):
        print(f"\n诗歌 {i}:")
        print("-" * 40)
        print(poem)
        print("-" * 40)
        
        analysis = analyze_rhyme_scheme(poem)
        print(f"  行数: {analysis['line_count']}")
        print(f"  韵脚: {analysis['rhyme_scheme']}")
        print(f"  格律: {analysis['meter']}")
        print(f"  每行音节: {analysis['syllable_counts']}")


def example_haiku():
    """示例5: 俳句建议"""
    print("\n" + "=" * 50)
    print("示例5: 俳句建议 (5-7-5)")
    print("=" * 50)
    
    # 符合5-7-5模式的文本
    text = "The gentle rain falls soft upon the ground below my feet today now"
    
    print(f"\n文本: '{text}'")
    
    haikus = suggest_haiku_lines(text)
    
    if haikus:
        for i, haiku in enumerate(haikus, 1):
            print(f"\n俳句 {i}:")
            print(f"  {haiku['first_line']} (5音节)")
            print(f"  {haiku['second_line']} (7音节)")
            print(f"  {haiku['third_line']} (5音节)")
    else:
        print("  未找到符合5-7-5模式的俳句结构")


def example_readability():
    """示例6: 可读性分析"""
    print("\n" + "=" * 50)
    print("示例6: 可读性分析")
    print("=" * 50)
    
    texts = [
        "The cat sat on the mat.",
        "Programming computers requires logical thinking and problem solving skills.",
        "The extraordinary circumstances necessitated a comprehensive investigation into the multifaceted phenomenological implications."
    ]
    
    for i, text in enumerate(texts, 1):
        print(f"\n文本 {i}: '{text[:50]}...'" if len(text) > 50 else f"\n文本 {i}: '{text}'")
        
        score = readability_score(text)
        print(f"  单词数: {score['words']}")
        print(f"  句子数: {score['sentences']}")
        print(f"  音节数: {score['syllables']}")
        print(f"  平均音节: {score['avg_syllables']}")
        print(f"  难度: {score['difficulty']}")


def example_complex_words():
    """示例7: 复杂词统计"""
    print("\n" + "=" * 50)
    print("示例7: 复杂词统计 (3+音节)")
    print("=" * 50)
    
    text = """Technology has revolutionized the way we communicate, 
    bringing extraordinary opportunities for collaboration and innovation 
    across international boundaries."""
    
    print(f"\n文本: '{text[:60]}...'")
    
    result = count_complex_words(text, threshold=3)
    print(f"\n  复杂词数量: {result['count']}")
    print(f"  总单词数: {result['total_words']}")
    print(f"  复杂词占比: {result['percentage']}%")
    print(f"  复杂词列表: {result['complex_words']}")


def example_batch_processing():
    """示例8: 批量处理"""
    print("\n" + "=" * 50)
    print("示例8: 批量处理")
    print("=" * 50)
    
    words = ["hello", "world", "python", "programming", "beautiful", "code"]
    
    print(f"\n单词列表: {words}")
    
    # 批量计数
    results = batch_count_syllables(words)
    print(f"\n批量音节计数:")
    for word, count in results.items():
        print(f"  {word}: {count}")
    
    # 统计信息
    stats = get_syllable_stats(" ".join(words))
    print(f"\n统计信息:")
    print(f"  总音节: {stats['total_syllables']}")
    print(f"  平均每词: {stats['avg_per_word']}")
    print(f"  音节分布: {stats['distribution']}")


def example_syllable_generation():
    """示例9: 按音节数生成单词"""
    print("\n" + "=" * 50)
    print("示例9: 按音节数生成单词列表")
    print("=" * 50)
    
    for n in [1, 2, 3, 4, 5]:
        words = generate_syllable_word_list(n)
        sample = words[:5] if len(words) > 5 else words
        print(f"\n{n}音节词 ({len(words)}个): {sample}...")


def main():
    """运行所有示例"""
    print("=" * 50)
    print("音节计数工具使用示例")
    print("=" * 50)
    
    example_basic_count()
    example_sentence_analysis()
    example_word_breakdown()
    example_poetry_analysis()
    example_haiku()
    example_readability()
    example_complex_words()
    example_batch_processing()
    example_syllable_generation()
    
    print("\n" + "=" * 50)
    print("示例完成!")
    print("=" * 50)


if __name__ == "__main__":
    main()
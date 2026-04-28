"""
readability_utils 使用示例

展示如何使用文本可读性分析工具
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    ReadabilityAnalyzer,
    ChineseReadabilityAnalyzer,
    analyze_readability,
    get_grade_level,
    count_syllables
)


def example_english_basic():
    """示例1：基础英文可读性分析"""
    print("=" * 60)
    print("示例1：基础英文可读性分析")
    print("=" * 60)
    
    text = """
    The quick brown fox jumps over the lazy dog. This is a simple 
    sentence that demonstrates readability analysis. We will use 
    various formulas to determine how easy or difficult this text 
    is to read.
    """
    
    result = analyze_readability(text)
    
    print(f"文本统计:")
    print(f"  句子数: {result['total_sentences']}")
    print(f"  单词数: {result['total_words']}")
    print(f"  音节数: {result['total_syllables']}")
    print(f"  字符数: {result['total_characters']}")
    print(f"  复杂单词: {result['complex_words']}")
    print()
    print(f"可读性指标:")
    print(f"  Flesch Reading Ease: {result['flesch_reading_ease']}")
    print(f"  Flesch-Kincaid Grade: {result['flesch_kincaid_grade']}")
    print(f"  Gunning Fog Index: {result['gunning_fog_index']}")
    print(f"  SMOG Index: {result['smog_index']}")
    print(f"  Coleman-Liau Index: {result['coleman_liau_index']}")
    print(f"  ARI: {result['ari']}")
    print()
    print(f"综合评估: {result['grade_level']}")


def example_english_complex():
    """示例2：复杂学术文本分析"""
    print("\n" + "=" * 60)
    print("示例2：复杂学术文本分析")
    print("=" * 60)
    
    text = """
    The implementation of sophisticated algorithmic methodologies 
    necessitates comprehensive understanding of computational 
    complexity theory. Contemporary researchers in artificial 
    intelligence leverage advanced mathematical frameworks to 
    optimize machine learning paradigms, thereby enhancing 
    predictive accuracy across heterogeneous datasets.
    """
    
    analyzer = ReadabilityAnalyzer(text)
    result = analyzer.analyze()
    
    print(f"Flesch Reading Ease: {result.flesch_reading_ease}")
    print(f"年级水平: {result.grade_level}")
    print()
    
    # 详细分析
    print(f"平均句长: {result.avg_sentence_length} 词/句")
    print(f"平均音节/词: {result.avg_syllables_per_word}")
    print(f"复杂单词比例: {result.complex_words / result.total_words * 100:.1f}%")


def example_chinese_basic():
    """示例3：中文文本分析"""
    print("\n" + "=" * 60)
    print("示例3：中文文本分析")
    print("=" * 60)
    
    text = """
    小猫坐在垫子上，看着窗外的风景。阳光透过玻璃洒在地板上，
    温暖而舒适。小狗跑过来，摇着尾巴，想要一起玩耍。
    这是一个美好的下午。
    """
    
    result = analyze_readability(text, 'zh')
    
    print(f"文本统计:")
    print(f"  中文字符数: {result['chinese_chars']}")
    print(f"  句子数: {result['sentence_count']}")
    print(f"  段落数: {result['paragraph_count']}")
    print(f"  平均句长: {result['avg_sentence_length']} 字/句")
    print()
    print(f"难度评分: {result['difficulty_score']}")
    print(f"难度等级: {result['difficulty_level']}")


def example_chinese_academic():
    """示例4：中文专业文本分析"""
    print("\n" + "=" * 60)
    print("示例4：中文专业文本分析")
    print("=" * 60)
    
    text = """
    人工智能技术的快速发展对社会经济结构产生了深远影响，
    其复杂性涉及哲学、伦理学、认知科学等多个学科领域的交叉融合。
    从计算理论的角度来看，神经网络的泛化能力与模型架构、训练数据分布、
    优化算法选择等因素存在复杂的非线性关联。
    """
    
    analyzer = ChineseReadabilityAnalyzer(text)
    result = analyzer.analyze()
    
    print(f"中文字符数: {result['chinese_chars']}")
    print(f"难度评分: {result['difficulty_score']}")
    print(f"难度等级: {result['difficulty_level']}")


def example_syllable_counting():
    """示例5：音节计数"""
    print("\n" + "=" * 60)
    print("示例5：英文单词音节计数")
    print("=" * 60)
    
    words = [
        'cat', 'dog', 'hello', 'beautiful', 'information',
        'technology', 'extraordinary', 'university', 'programming'
    ]
    
    for word in words:
        syllables = count_syllables(word)
        print(f"  {word}: {syllables} 音节")


def example_quick_grade_check():
    """示例6：快速年级水平检查"""
    print("\n" + "=" * 60)
    print("示例6：快速年级水平检查")
    print("=" * 60)
    
    texts = [
        ("儿童故事", "See Spot run. Run Spot run. The dog is fast."),
        ("新闻文章", "The president announced new policies today that will affect millions of citizens across the country."),
        ("学术论文", "The epistemological implications of quantum mechanics have profound ramifications for our understanding of reality."),
    ]
    
    for name, text in texts:
        grade = get_grade_level(text)
        print(f"{name}: {grade}")


def example_compare_texts():
    """示例7：对比分析不同文本"""
    print("\n" + "=" * 60)
    print("示例7：对比分析不同难度的文本")
    print("=" * 60)
    
    texts = {
        "简单": "The cat sat on the mat. The dog ran fast.",
        "中等": "Regular exercise contributes significantly to overall health and well-being. Studies show that people who exercise daily live longer.",
        "困难": "The elucidation of molecular mechanisms underlying cellular processes necessitates sophisticated experimental methodologies and rigorous analytical frameworks.",
    }
    
    print(f"{'难度':<8} {'FRE':<8} {'年级':<10} {'评价'}")
    print("-" * 50)
    
    for level, text in texts.items():
        analyzer = ReadabilityAnalyzer(text)
        result = analyzer.analyze()
        print(f"{level:<8} {result.flesch_reading_ease:<8.1f} {result.flesch_kincaid_grade:<10.1f} {result.grade_level}")


def example_custom_analysis():
    """示例8：自定义分析"""
    print("\n" + "=" * 60)
    print("示例8：获取详细统计信息")
    print("=" * 60)
    
    text = "The implementation of advanced algorithms requires careful consideration of time complexity and space efficiency."
    
    # 获取统计信息
    stats = ReadabilityAnalyzer(text).stats
    
    print("文本统计详情:")
    print(f"  句子数: {stats.total_sentences}")
    print(f"  单词数: {stats.total_words}")
    print(f"  字符数: {stats.total_characters}")
    print(f"  音节数: {stats.total_syllables}")
    print(f"  复杂单词数 (3+音节): {stats.complex_words}")
    print(f"  平均句长: {stats.avg_sentence_length:.2f}")
    print(f"  平均音节/词: {stats.avg_syllables_per_word:.2f}")
    print(f"  平均字母/词: {stats.avg_letters_per_word:.2f}")


if __name__ == '__main__':
    example_english_basic()
    example_english_complex()
    example_chinese_basic()
    example_chinese_academic()
    example_syllable_counting()
    example_quick_grade_check()
    example_compare_texts()
    example_custom_analysis()
    
    print("\n" + "=" * 60)
    print("所有示例完成！")
    print("=" * 60)
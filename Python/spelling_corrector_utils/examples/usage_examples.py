"""
spelling_corrector_utils 使用示例

演示拼写纠正工具的各种用法。
"""

import sys
import os

# 直接从父目录导入模块
_module_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _module_dir)

from mod import (
    SpellingCorrector,
    is_correct,
    correct,
    get_suggestions,
    batch_correct,
    correct_text,
    add_word,
    add_words_from_text
)


def example_basic_usage():
    """基础用法示例"""
    print("=" * 60)
    print("示例 1: 基础拼写检查")
    print("=" * 60)
    
    corrector = SpellingCorrector()
    
    # 检查单词是否正确
    words = ['hello', 'world', 'speling', 'wrld', 'computer']
    
    print("\n检查单词拼写:")
    for word in words:
        is_valid = corrector.is_correct(word)
        status = "✓ 正确" if is_valid else "✗ 错误"
        print(f"  {word:15} -> {status}")
    
    print()


def example_spell_correction():
    """自动纠错示例"""
    print("=" * 60)
    print("示例 2: 自动拼写纠正")
    print("=" * 60)
    
    corrector = SpellingCorrector()
    
    # 常见拼写错误
    misspellings = [
        'speling',      # 少了一个 l
        'wrld',         # 少了一个 o
        'korrecter',    # k 开头
        'teh',          # 常见错误
        'recieve',      # ie/ei 错误
        'definately',   # 常见错误
        'occured',      # 双写错误
        'seperate',     # er/ar 错误
    ]
    
    print("\n自动纠正:")
    for word in misspellings:
        correction = corrector.correct(word)
        suggestions = corrector.get_suggestions(word, limit=3)
        suggestion_str = ', '.join([f"{w}({f})" for w, f in suggestions[:3]])
        print(f"  {word:15} -> {correction:15} | 建议: {suggestion_str}")
    
    print()


def example_suggestions():
    """获取建议示例"""
    print("=" * 60)
    print("示例 3: 获取拼写建议")
    print("=" * 60)
    
    corrector = SpellingCorrector()
    
    # 获取多个建议
    words = ['speling', 'wrld', 'pyton', 'languge']
    
    print("\n拼写建议 (前5个):")
    for word in words:
        suggestions = corrector.get_suggestions(word, limit=5)
        print(f"\n  '{word}' 的建议:")
        for i, (suggestion, freq) in enumerate(suggestions, 1):
            print(f"    {i}. {suggestion:15} (频率: {freq})")
    
    print()


def example_batch_operations():
    """批量操作示例"""
    print("=" * 60)
    print("示例 4: 批量纠正")
    print("=" * 60)
    
    corrector = SpellingCorrector()
    
    # 批量纠正单词列表
    words = ['hello', 'wrld', 'python', 'programing', 'is', 'awsome']
    corrected = corrector.batch_correct(words)
    
    print("\n批量纠正:")
    print(f"  原文:   {words}")
    print(f"  纠正后: {corrected}")
    
    # 纠正整段文本
    text = """
    Hello wrld! Python is an amazing programing languge.
    It is used for web devlopment, data sciance, and machine lerning.
    If your loking for a powerfull tool, python is definately the way to go!
    """
    
    corrected_text = corrector.correct_text(text)
    
    print("\n文本纠正:")
    print("  原文:")
    print("  " + text.strip().replace('\n', '\n  '))
    print("\n  纠正后:")
    print("  " + corrected_text.strip().replace('\n', '\n  '))
    
    print()


def example_custom_vocabulary():
    """自定义词典示例"""
    print("=" * 60)
    print("示例 5: 自定义词典")
    print("=" * 60)
    
    corrector = SpellingCorrector()
    
    # 添加专业术语
    print("\n添加编程术语到词典:")
    corrector.add_word('pythonista', 5000)
    corrector.add_word('devops', 4000)
    corrector.add_word('javascript', 8000)
    corrector.add_word('typescript', 6000)
    
    # 测试新添加的词
    words = ['pythonista', 'devops', 'javascript', 'typescript']
    for word in words:
        is_valid = corrector.is_correct(word)
        print(f"  {word:15} -> {'✓ 在词典中' if is_valid else '✗ 不在词典中'}")
    
    # 添加自定义拼写错误映射
    print("\n添加自定义拼写错误映射:")
    corrector.add_misspelling('pyton', 'python')
    corrector.add_misspelling('js', 'javascript')
    corrector.add_misspelling('ts', 'typescript')
    
    errors = ['pyton', 'js', 'ts']
    for word in errors:
        correction = corrector.correct(word)
        print(f"  {word:15} -> {correction}")
    
    print()


def example_learning_from_text():
    """从文本学习示例"""
    print("=" * 60)
    print("示例 6: 从文本学习新词汇")
    print("=" * 60)
    
    corrector = SpellingCorrector()
    
    # 原始词典大小
    original_size = corrector.vocabulary_size
    print(f"\n原始词典大小: {original_size}")
    
    # 从文本学习
    text = """
    TensorFlow is an open-source machine learning framework.
    PyTorch is another popular deep learning library.
    Kubernetes helps with container orchestration.
    Microservices architecture is widely adopted.
    """
    
    print("学习文本中的新词汇...")
    corrector.add_words_from_text(text)
    
    # 新词典大小
    new_size = corrector.vocabulary_size
    print(f"学习后词典大小: {new_size}")
    print(f"新增词汇数量: {new_size - original_size}")
    
    print()


def example_case_preservation():
    """大小写保持示例"""
    print("=" * 60)
    print("示例 7: 保持大小写")
    print("=" * 60)
    
    corrector = SpellingCorrector()
    
    words = [
        'hello',     # 小写
        'Hello',     # 首字母大写
        'HELLO',     # 全大写
        'wrld',      # 小写错误
        'Wrld',      # 首字母大写错误
        'WRLD',      # 全大写错误
    ]
    
    print("\n纠正时保持大小写格式:")
    for word in words:
        correction = corrector.correct(word)
        print(f"  {word:15} -> {correction:15}")
    
    print()


def example_common_errors():
    """常见拼写错误示例"""
    print("=" * 60)
    print("示例 8: 常见拼写错误纠正")
    print("=" * 60)
    
    corrector = SpellingCorrector()
    
    # 常见英语拼写错误
    common_errors = [
        ('accomodate', 'accommodate'),
        ('acheive', 'achieve'),
        ('accross', 'across'),
        ('agressive', 'aggressive'),
        ('apparant', 'apparent'),
        ('beggining', 'beginning'),
        ('calender', 'calendar'),
        ('collegue', 'colleague'),
        ('commitee', 'committee'),
        ('concious', 'conscious'),
        ('embarass', 'embarrass'),
        ('enviroment', 'environment'),
        ('fourty', 'forty'),
        ('freind', 'friend'),
        ('grammer', 'grammar'),
        ('immediatly', 'immediately'),
        ('liason', 'liaison'),
        ('maintainance', 'maintenance'),
        ('millenium', 'millennium'),
        ('neccessary', 'necessary'),
        ('occurence', 'occurrence'),
        ('potatos', 'potatoes'),
        ('reccomend', 'recommend'),
        ('rythm', 'rhythm'),
        ('succesful', 'successful'),
        ('tommorow', 'tomorrow'),
        ('truely', 'truly'),
        ('writting', 'writing'),
    ]
    
    print("\n常见拼写错误纠正:")
    correct_count = 0
    for error, expected in common_errors:
        correction = corrector.correct(error)
        match = "✓" if correction.lower() == expected.lower() else "✗"
        if correction.lower() == expected.lower():
            correct_count += 1
        print(f"  {match} {error:20} -> {correction:20} (期望: {expected})")
    
    print(f"\n准确率: {correct_count}/{len(common_errors)} ({correct_count/len(common_errors)*100:.1f}%)")
    print()


def example_convenience_functions():
    """便捷函数示例"""
    print("=" * 60)
    print("示例 9: 使用便捷函数")
    print("=" * 60)
    
    print("\n使用模块级便捷函数（无需创建实例）:")
    
    # is_correct
    print(f"\n  is_correct('hello'): {is_correct('hello')}")
    print(f"  is_correct('speling'): {is_correct('speling')}")
    
    # correct
    print(f"\n  correct('speling'): {correct('speling')}")
    print(f"  correct('wrld'): {correct('wrld')}")
    
    # get_suggestions
    suggestions = get_suggestions('pyton', limit=3)
    print(f"\n  get_suggestions('pyton', limit=3): {suggestions}")
    
    # batch_correct
    batch = batch_correct(['hello', 'wrld', 'pyton'])
    print(f"\n  batch_correct(['hello', 'wrld', 'pyton']): {batch}")
    
    # correct_text
    text = correct_text("Hello wrld!")
    print(f"\n  correct_text('Hello wrld!'): {text}")
    
    # add_word
    add_word('pythonista', 5000)
    print(f"\n  add_word('pythonista', 5000)")
    print(f"  is_correct('pythonista'): {is_correct('pythonista')}")
    
    print()


def example_statistics():
    """统计信息示例"""
    print("=" * 60)
    print("示例 10: 词典统计")
    print("=" * 60)
    
    corrector = SpellingCorrector()
    
    print(f"\n词典大小: {corrector.vocabulary_size} 词")
    
    # 高频词
    high_freq_words = ['the', 'be', 'to', 'of', 'and', 'a', 'in', 'that']
    print("\n高频词频率:")
    for word in high_freq_words:
        freq = corrector.get_word_frequency(word)
        print(f"  {word:15} : {freq:,}")
    
    # 编程相关词
    prog_words = ['function', 'variable', 'class', 'method', 'object', 'string']
    print("\n编程相关词频率:")
    for word in prog_words:
        freq = corrector.get_word_frequency(word)
        print(f"  {word:15} : {freq:,}")
    
    print()


def main():
    """运行所有示例"""
    print("\n")
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 15 + "拼写纠正工具使用示例" + " " * 15 + "║")
    print("╚" + "═" * 58 + "╝")
    print()
    
    example_basic_usage()
    example_spell_correction()
    example_suggestions()
    example_batch_operations()
    example_custom_vocabulary()
    example_learning_from_text()
    example_case_preservation()
    example_common_errors()
    example_convenience_functions()
    example_statistics()
    
    print("=" * 60)
    print("所有示例完成！")
    print("=" * 60)


if __name__ == '__main__':
    main()
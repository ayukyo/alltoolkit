#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Aho-Corasick 使用示例
====================================
演示 Aho-Corasick 算法的各种应用场景。

Aho-Corasick 算法是一种高效的多模式字符串匹配算法，
可以在 O(n + m + z) 时间复杂度内找到文本中所有模式的出现位置，
其中 n 是文本长度，m 是所有模式的总长度，z 是匹配数量。
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    AhoCorasick,
    SensitiveWordFilter,
    MultiPatternReplacer,
    WildcardAhoCorasick,
    build_automaton,
    find_all,
    contains_any,
    replace_patterns,
    highlight_patterns
)


def example_basic_usage():
    """基本用法示例"""
    print("=" * 60)
    print("示例 1: 基本用法")
    print("=" * 60)
    
    # 创建自动机并添加模式
    patterns = ['he', 'she', 'his', 'hers']
    ac = AhoCorasick(patterns)
    
    # 在文本中搜索
    text = 'ushers'
    matches = ac.findall(text)
    
    print(f"\n模式: {patterns}")
    print(f"文本: '{text}'")
    print(f"匹配结果:")
    for match in matches:
        print(f"  - '{match.pattern}' 位置 [{match.start}:{match.end}]")
    
    print("\n解释: Aho-Corasick 算法可以在一次遍历中找到所有模式的出现")


def example_sensitive_word_filter():
    """敏感词过滤示例"""
    print("\n" + "=" * 60)
    print("示例 2: 敏感词过滤")
    print("=" * 60)
    
    # 创建敏感词过滤器（默认不区分大小写）
    sensitive_words = ['敏感', '违禁', '违规内容', '测试词']
    filter = SensitiveWordFilter(sensitive_words)
    
    # 测试文本
    test_text = "这是一段包含敏感词汇和违禁内容的测试文本，测试词也在其中。"
    
    print(f"\n敏感词: {list(filter.words)}")
    print(f"测试文本: {test_text}")
    
    # 检测是否包含敏感词
    has_sensitive = filter.check(test_text)
    print(f"\n包含敏感词: {has_sensitive}")
    
    # 找出所有敏感词
    found_words = filter.find(test_text)
    print(f"发现的敏感词: {found_words}")
    
    # 替换敏感词
    cleaned_text = filter.clean(test_text, replacement='***')
    print(f"清理后文本: {cleaned_text}")
    
    # 高亮显示敏感词
    highlighted = filter.highlight(test_text)
    print(f"高亮后文本: {highlighted}")


def example_multi_pattern_replacement():
    """多模式替换示例"""
    print("\n" + "=" * 60)
    print("示例 3: 多模式替换（不同替换词）")
    print("=" * 60)
    
    # 创建替换器，每个模式可以有不同的替换词
    replacer = MultiPatternReplacer()
    replacer.add('foo', 'bar')
    replacer.add('hello', 'hi')
    replacer.add('world', 'universe')
    replacer.add('Python', 'Python🐍')
    
    test_text = "Hello, foo! Python world is amazing."
    
    print(f"\n替换规则:")
    print(f"  'foo' → 'bar'")
    print(f"  'hello' → 'hi'")
    print(f"  'world' → 'universe'")
    print(f"  'Python' → 'Python🐍'")
    print(f"\n原文本: {test_text}")
    
    # 不区分大小写的替换
    result = replacer.replace(test_text)
    print(f"替换后: {result}")


def example_keyword_extraction():
    """关键词提取示例"""
    print("\n" + "=" * 60)
    print("示例 4: 关键词提取")
    print("=" * 60)
    
    # 定义关键词
    keywords = ['Python', 'Java', 'JavaScript', 'Go', 'Rust', 
                '机器学习', '深度学习', '人工智能', '算法', '数据结构']
    
    ac = AhoCorasick(keywords)
    
    # 文章文本
    article = """
    在当今的软件开发领域，Python 已经成为最受欢迎的编程语言之一。
    特别是在机器学习和深度学习领域，Python 几乎成为了标准选择。
    而 Go 语言凭借其并发特性在云原生开发中崭露头角，
    Rust 则以其内存安全性正在改变系统编程的格局。
    """
    
    print(f"\n关键词列表: {keywords}")
    print(f"文章内容: {article.strip()}")
    
    # 提取所有出现的关键词
    all_keywords = ac.extract(article)
    print(f"\n提取到的关键词: {all_keywords}")
    
    # 提取唯一关键词
    unique_keywords = ac.extract_unique(article)
    print(f"唯一关键词: {unique_keywords}")
    
    # 获取每个关键词的位置
    positions = ac.get_pattern_positions(article)
    print(f"\n关键词位置:")
    for keyword, pos in sorted(positions.items()):
        print(f"  '{keyword}': 出现 {len(pos)} 次")


def example_stream_processing():
    """流式处理示例"""
    print("\n" + "=" * 60)
    print("示例 5: 流式处理（适合大数据）")
    print("=" * 60)
    
    patterns = ['error', 'warning', 'critical', 'failed']
    ac = AhoCorasick(patterns)
    
    # 模拟日志流
    logs = [
        "2024-01-01 10:00:00 [INFO] System started",
        "2024-01-01 10:01:00 [WARNING] Low memory detected",
        "2024-01-01 10:02:00 [ERROR] Connection failed",
        "2024-01-01 10:03:00 [CRITICAL] Database error",
    ]
    
    print(f"监控模式: {patterns}")
    print(f"\n日志流处理:")
    
    match_count = 0
    for line_num, log in enumerate(logs, 1):
        matches = ac.findall(log)
        if matches:
            match_count += len(matches)
            print(f"  行 {line_num}: 发现 {len(matches)} 个匹配")
            for m in matches:
                print(f"    - '{m.pattern}' at position {m.start}")
    
    print(f"\n总共发现 {match_count} 个匹配")


def example_content_moderation():
    """内容审核示例"""
    print("\n" + "=" * 60)
    print("示例 6: 内容审核系统")
    print("=" * 60)
    
    # 定义审核规则
    spam_words = ['免费', '中奖', '点击链接', '优惠活动', '限时抢购']
    inappropriate_words = ['暴力', '仇恨', '歧视']
    
    spam_filter = SensitiveWordFilter(spam_words, replacement='[已过滤]')
    inappropriate_filter = SensitiveWordFilter(inappropriate_words, replacement='[违规]')
    
    # 用户评论
    comments = [
        "这个产品真的很好用！推荐购买。",
        "免费领取大奖！点击链接参与活动！",
        "我觉得这个设计很有创意，但是有些地方可以改进。",
        "这种暴力内容不应该出现在平台上。",
    ]
    
    print("审核规则:")
    print(f"  垃圾信息关键词: {spam_words}")
    print(f"  不当内容关键词: {inappropriate_words}")
    print("\n评论审核:")
    
    for i, comment in enumerate(comments, 1):
        is_spam = spam_filter.check(comment)
        is_inappropriate = inappropriate_filter.check(comment)
        
        status = "✅ 通过"
        if is_spam:
            status = "⚠️ 垃圾信息"
        elif is_inappropriate:
            status = "🚫 违规内容"
        
        print(f"\n评论 {i}: {status}")
        print(f"  原文: {comment}")
        
        if is_spam:
            cleaned = spam_filter.clean(comment)
            print(f"  过滤后: {cleaned}")
        elif is_inappropriate:
            cleaned = inappropriate_filter.clean(comment)
            print(f"  过滤后: {cleaned}")


def example_url_and_email_detection():
    """URL 和邮箱检测示例"""
    print("\n" + "=" * 60)
    print("示例 7: URL 和邮箱检测")
    print("=" * 60)
    
    # 常见的 URL 和邮箱模式
    url_patterns = ['http://', 'https://', 'www.', '.com', '.org', '.net']
    email_patterns = ['@gmail', '@yahoo', '@outlook', '@qq.com']
    
    url_ac = AhoCorasick(url_patterns)
    email_ac = AhoCorasick(email_patterns)
    
    test_text = """
    联系我们:
    - 官网: https://example.com
    - 备用: www.backup.org
    - 邮箱: support@gmail.com 或 admin@qq.com
    """
    
    print(f"URL 模式: {url_patterns}")
    print(f"邮箱模式: {email_patterns}")
    print(f"\n测试文本: {test_text.strip()}")
    
    # 检测 URL 相关内容
    url_matches = url_ac.findall(test_text)
    print(f"\nURL 相关匹配: {len(url_matches)} 次")
    for m in url_matches:
        print(f"  - '{m.pattern}' at position {m.start}")
    
    # 检测邮箱相关内容
    email_matches = email_ac.findall(test_text)
    print(f"\n邮箱相关匹配: {len(email_matches)} 次")
    for m in email_matches:
        print(f"  - '{m.pattern}' at position {m.start}")


def example_code_analysis():
    """代码分析示例"""
    print("\n" + "=" * 60)
    print("示例 8: 代码分析（检测潜在问题）")
    print("=" * 60)
    
    # 定义潜在问题的模式
    security_patterns = [
        'eval(', 'exec(', 
        'password =', 'secret =', 
        'TODO', 'FIXME', 'HACK',
        'print(', 'console.log(',
    ]
    
    ac = AhoCorasick(security_patterns)
    
    code_snippet = '''
def process_data(user_input):
    # TODO: Add input validation
    result = eval(user_input)  # Dangerous!
    password = "admin123"  # FIXME: Use environment variable
    print("Debug:", result)
    return result
    '''
    
    print(f"检测模式: {security_patterns}")
    print(f"\n代码片段: {code_snippet.strip()}")
    
    matches = ac.findall(code_snippet)
    print(f"\n发现 {len(matches)} 个潜在问题:")
    
    # 按行号分组
    lines = code_snippet.split('\n')
    for match in matches:
        # 找到匹配所在的行
        line_num = code_snippet[:match.start].count('\n') + 1
        print(f"  行 {line_num}: '{match.pattern}' - {match.pattern}")


def example_dna_sequence():
    """DNA 序列分析示例"""
    print("\n" + "=" * 60)
    print("示例 9: DNA 序列分析")
    print("=" * 60)
    
    # 定义 DNA 序列模式（如基因标记）
    gene_markers = ['ATG', 'TAA', 'TAG', 'TGA', 'GGATCC', 'GAATTC']
    ac = AhoCorasick(gene_markers)
    
    # DNA 序列
    dna_sequence = "ATGCGATCGGATCCTTAATGAATGCTAGCGATGA"
    
    print(f"基因标记: {gene_markers}")
    print(f"DNA 序列: {dna_sequence}")
    
    matches = ac.findall(dna_sequence)
    print(f"\n发现 {len(matches)} 个标记:")
    
    for match in matches:
        # 获取周围序列
        context_start = max(0, match.start - 3)
        context_end = min(len(dna_sequence), match.end + 3)
        context = dna_sequence[context_start:context_end]
        print(f"  '{match.pattern}' at [{match.start}:{match.end}] - context: ...{context}...")


def example_serialization():
    """序列化示例"""
    print("\n" + "=" * 60)
    print("示例 10: 序列化和持久化")
    print("=" * 60)
    
    # 创建并保存自动机
    patterns = ['apple', 'banana', 'cherry']
    ac = AhoCorasick(patterns)
    
    # 转换为字典
    data = ac.to_dict()
    print(f"原始模式: {patterns}")
    print(f"序列化为字典: {data}")
    
    # 转换为 JSON
    json_str = ac.to_json()
    print(f"序列化为 JSON: {json_str}")
    
    # 从字典恢复
    ac_restored = AhoCorasick.from_dict(data)
    print(f"\n从字典恢复: {ac_restored}")
    
    # 验证恢复后的功能
    test_text = "I like apple and banana"
    matches = ac_restored.findall(test_text)
    print(f"测试文本: '{test_text}'")
    print(f"匹配结果: {[m.pattern for m in matches]}")


def example_convenience_functions():
    """便捷函数示例"""
    print("\n" + "=" * 60)
    print("示例 11: 便捷函数")
    print("=" * 60)
    
    patterns = ['quick', 'brown', 'fox']
    text = "The quick brown fox jumps over the lazy dog"
    
    print(f"模式: {patterns}")
    print(f"文本: {text}")
    
    # find_all - 找出所有匹配
    matches = find_all(patterns, text)
    print(f"\nfind_all: {[m.pattern for m in matches]}")
    
    # contains_any - 检查是否包含任何模式
    has_match = contains_any(patterns, text)
    print(f"contains_any: {has_match}")
    
    # replace_patterns - 替换所有模式
    replaced = replace_patterns(patterns, text, "***")
    print(f"replace_patterns: {replaced}")
    
    # highlight_patterns - 高亮所有模式
    highlighted = highlight_patterns(patterns, text, "**", "**")
    print(f"highlight_patterns: {highlighted}")


def example_case_sensitivity():
    """大小写敏感示例"""
    print("\n" + "=" * 60)
    print("示例 12: 大小写敏感控制")
    print("=" * 60)
    
    text = "Python python PYTHON"
    
    # 区分大小写
    ac_sensitive = AhoCorasick(['Python'], case_sensitive=True)
    matches_sensitive = ac_sensitive.findall(text)
    print(f"区分大小写: 找到 {len(matches_sensitive)} 个匹配")
    print(f"  匹配: {[m.pattern for m in matches_sensitive]}")
    
    # 不区分大小写
    ac_insensitive = AhoCorasick(['python'], case_sensitive=False)
    matches_insensitive = ac_insensitive.findall(text)
    print(f"\n不区分大小写: 找到 {len(matches_insensitive)} 个匹配")
    print(f"  匹配: {[m.pattern for m in matches_insensitive]}")


def main():
    """运行所有示例"""
    example_basic_usage()
    example_sensitive_word_filter()
    example_multi_pattern_replacement()
    example_keyword_extraction()
    example_stream_processing()
    example_content_moderation()
    example_url_and_email_detection()
    example_code_analysis()
    example_dna_sequence()
    example_serialization()
    example_convenience_functions()
    example_case_sensitivity()
    
    print("\n" + "=" * 60)
    print("所有示例运行完成！")
    print("=" * 60)


if __name__ == '__main__':
    main()
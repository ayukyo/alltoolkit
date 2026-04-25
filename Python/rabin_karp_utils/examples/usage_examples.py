"""
Rabin-Karp 工具模块使用示例

演示各种字符串匹配和文本分析场景
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from rabin_karp_utils.mod import (
    rabin_karp_search,
    multi_pattern_search,
    find_all_occurrences,
    contains_pattern,
    count_occurrences,
    find_with_wildcards,
    find_longest_repeated_substring,
    find_common_substring,
    compute_similarity,
    detect_plagiarism,
    two_d_pattern_search,
    RabinKarpMatcher,
    double_hash_search,
    RollingHash,
)


def example_basic_search():
    """基本字符串搜索示例"""
    print("=" * 60)
    print("基本字符串搜索")
    print("=" * 60)
    
    text = """
    The Rabin-Karp algorithm is a string-searching algorithm that uses 
    hashing to find patterns in text. It was created by Michael O. Rabin 
    and Richard M. Karp in 1987. The algorithm is particularly useful for 
    multiple pattern matching and has applications in plagiarism detection.
    """
    
    # 搜索单个模式
    pattern = "Rabin"
    positions = rabin_karp_search(text, pattern)
    print(f"\n搜索 '{pattern}':")
    print(f"  找到 {len(positions)} 处: {positions}")
    
    # 统计出现次数
    count = count_occurrences(text, "algorithm")
    print(f"\n'algorithm' 出现次数: {count}")
    
    # 检查是否包含
    if contains_pattern(text, "plagiarism"):
        print("  文本包含 'plagiarism'")
    
    # 查找所有出现位置
    matches = find_all_occurrences(text, "the")
    print(f"\n'the' 的所有匹配位置:")
    for m in matches[:5]:  # 只显示前5个
        print(f"  位置 {m.index}: '{text[m.index:m.index+10]}...'")


def example_multi_pattern():
    """多模式搜索示例"""
    print("\n" + "=" * 60)
    print("多模式搜索")
    print("=" * 60)
    
    text = """
    Python is a high-level programming language. Python supports multiple 
    programming paradigms including procedural, object-oriented, and functional 
    programming. Python's design philosophy emphasizes code readability.
    """
    
    keywords = ["Python", "programming", "language", "code"]
    results = multi_pattern_search(text, keywords)
    
    print(f"\n搜索关键词: {keywords}")
    print(f"找到 {len(results)} 处匹配:\n")
    
    for r in results:
        # 显示上下文
        start = max(0, r.index - 10)
        end = min(len(text), r.index + len(r.pattern) + 10)
        context = text[start:end].replace('\n', ' ')
        print(f"  '{r.pattern}' at {r.index}: ...{context}...")


def example_wildcard_search():
    """通配符搜索示例"""
    print("\n" + "=" * 60)
    print("通配符搜索")
    print("=" * 60)
    
    text = "The quick brown fox jumps over the lazy dog"
    
    # 使用 ? 作为通配符
    patterns = [
        "qu?ck",      # quick
        "br?wn",      # brown
        "f?x",        # fox
        "d?g",        # dog
    ]
    
    print(f"\n文本: {text}")
    print("\n通配符模式匹配:")
    for pattern in patterns:
        positions = find_with_wildcards(text, pattern)
        if positions:
            matches = [text[p:p+3] for p in positions]
            print(f"  '{pattern}' -> 匹配位置 {positions}")


def example_repeated_substring():
    """重复子串检测示例"""
    print("\n" + "=" * 60)
    print("最长重复子串检测")
    print("=" * 60)
    
    texts = [
        "banana",
        "abcdabcdabcd",
        "mississippi",
        "abcdefg",
    ]
    
    for text in texts:
        result = find_longest_repeated_substring(text)
        if result:
            substring, positions = result
            print(f"\n'{text}':")
            print(f"  最长重复子串: '{substring}'")
            print(f"  出现位置: {positions}")
        else:
            print(f"\n'{text}': 无重复子串")


def example_common_substring():
    """公共子串查找示例"""
    print("\n" + "=" * 60)
    print("多字符串公共子串")
    print("=" * 60)
    
    groups = [
        ["programming", "programmer", "program"],
        ["international", "internet", "interval"],
        ["apple", "banana", "cherry"],
    ]
    
    for group in groups:
        result = find_common_substring(group)
        print(f"\n字符串组: {group}")
        if result:
            print(f"  最长公共子串: '{result}'")
        else:
            print("  无公共子串")


def example_similarity():
    """文本相似度计算示例"""
    print("\n" + "=" * 60)
    print("文本相似度计算")
    print("=" * 60)
    
    pairs = [
        ("hello world", "hello there"),
        ("The quick brown fox", "The quick brown dog"),
        ("programming in Python", "coding in JavaScript"),
        ("完全不同的文本", "totally different"),
    ]
    
    for text1, text2 in pairs:
        sim = compute_similarity(text1, text2, k=5)
        print(f"\n文本1: '{text1}'")
        print(f"文本2: '{text2}'")
        print(f"相似度: {sim:.2%}")


def example_plagiarism():
    """抄袭检测示例"""
    print("\n" + "=" * 60)
    print("抄袭检测")
    print("=" * 60)
    
    documents = [
        """
        Machine learning is a subset of artificial intelligence that enables 
        systems to learn and improve from experience without being explicitly 
        programmed. It focuses on developing algorithms that can access data 
        and use it to learn for themselves.
        """,
        """
        Machine learning is a subset of AI that allows systems to learn and 
        improve from experience without being explicitly programmed. It focuses 
        on creating algorithms that can access data and use it to learn for 
        themselves.
        """,
        """
        Python is a versatile programming language known for its readability 
        and simplicity. It supports multiple programming paradigms and has a 
        large standard library that makes it suitable for various applications.
        """,
    ]
    
    # 检测相似度超过 50% 的文档对
    results = detect_plagiarism(documents, threshold=0.5, k=8)
    
    print("\n文档相似度分析结果:")
    for doc1_idx, doc2_idx, similarity in results:
        print(f"\n文档 {doc1_idx + 1} 和 文档 {doc2_idx + 1}:")
        print(f"  相似度: {similarity:.2%}")
        print(f"  可能存在抄袭!")


def example_2d_search():
    """二维模式搜索示例"""
    print("\n" + "=" * 60)
    print("二维模式搜索")
    print("=" * 60)
    
    # 文本网格
    text_grid = [
        "ABCDEFGH",
        "IJKLMNOP",
        "QRSTUVWX",
        "YZABCDEF",
    ]
    
    # 搜索模式
    pattern = [
        "JKL",
        "RST",
    ]
    
    print("\n文本网格:")
    for row in text_grid:
        print(f"  {row}")
    
    print(f"\n搜索模式:")
    for row in pattern:
        print(f"  {row}")
    
    positions = two_d_pattern_search(text_grid, pattern)
    
    if positions:
        print(f"\n找到模式位置: {positions}")
        for row, col in positions:
            print(f"  位置 ({row}, {col}):")
            for i, prow in enumerate(pattern):
                print(f"    {text_grid[row + i][col:col+len(prow)]}")
    else:
        print("\n未找到模式")


def example_matcher_class():
    """匹配器类使用示例"""
    print("\n" + "=" * 60)
    print("RabinKarpMatcher 匹配器类")
    print("=" * 60)
    
    # 预编译多个模式
    patterns = ["error", "warning", "critical", "fail", "exception"]
    matcher = RabinKarpMatcher(patterns)
    
    log_text = """
    [2024-01-15 10:30:45] ERROR: Connection timeout
    [2024-01-15 10:30:46] WARNING: Retrying connection...
    [2024-01-15 10:30:47] CRITICAL: Database connection failed
    [2024-01-15 10:30:48] INFO: Switching to backup server
    [2024-01-15 10:30:49] ERROR: Authentication exception
    """
    
    print(f"\n预编译模式: {patterns}")
    print(f"\n日志搜索结果:")
    
    results = matcher.search(log_text)
    for r in results:
        # 找到行的开头
        line_start = log_text.rfind('\n', 0, r.index) + 1
        line_end = log_text.find('\n', r.index)
        line = log_text[line_start:line_end].strip()
        print(f"  [{r.pattern}] {line}")
    
    # 动态添加模式
    print("\n动态添加模式 'INFO'...")
    matcher.add_pattern("INFO")
    
    new_results = matcher.search(log_text)
    print(f"新增后共找到 {len(new_results)} 处匹配")


def example_double_hash():
    """双哈希搜索示例"""
    print("\n" + "=" * 60)
    print("双哈希搜索（高可靠性）")
    print("=" * 60)
    
    text = "This is a sample text for demonstrating double hash search"
    pattern = "demonstrating"
    
    print(f"\n文本: {text}")
    print(f"模式: '{pattern}'")
    
    # 普通搜索
    normal_result = rabin_karp_search(text, pattern)
    print(f"普通搜索结果: {normal_result}")
    
    # 双哈希搜索
    double_result = double_hash_search(text, pattern)
    print(f"双哈希搜索结果: {double_result}")
    
    print("\n双哈希使用两个不同的质数模数，降低哈希冲突概率")


def example_rolling_hash():
    """滚动哈希使用示例"""
    print("\n" + "=" * 60)
    print("RollingHash 滚动哈希类")
    print("=" * 60)
    
    rh = RollingHash(base=256, modulus=10**9 + 7)
    
    # 计算初始哈希
    text = "hello"
    h1 = rh.compute(text)
    print(f"'{text}' 的哈希值: {h1}")
    
    # 不同的字符串有不同的哈希
    h2 = rh.compute("world")
    print(f"'world' 的哈希值: {h2}")
    
    print(f"\n相同字符串哈希相同: {h1 == rh.compute('hello')}")


def example_log_analysis():
    """日志分析实际应用示例"""
    print("\n" + "=" * 60)
    print("实际应用: 日志分析")
    print("=" * 60)
    
    # 模拟日志数据
    logs = """
    [INFO] 2024-01-15 08:00:00 - Application started
    [WARNING] 2024-01-15 08:00:15 - High memory usage detected
    [ERROR] 2024-01-15 08:01:30 - Database connection failed
    [WARNING] 2024-01-15 08:01:31 - Retrying database connection
    [ERROR] 2024-01-15 08:02:00 - Authentication error
    [INFO] 2024-01-15 08:02:30 - User login successful
    [ERROR] 2024-01-15 08:03:00 - API rate limit exceeded
    [WARNING] 2024-01-15 08:03:15 - Cache miss rate high
    [INFO] 2024-01-15 08:04:00 - Scheduled task completed
    [ERROR] 2024-01-15 08:04:30 - File not found exception
    """
    
    # 创建匹配器
    error_patterns = ["ERROR", "FAIL", "exception", "error"]
    matcher = RabinKarpMatcher(error_patterns)
    
    # 搜索错误
    results = matcher.search(logs)
    
    print(f"\n日志错误分析:")
    print(f"发现 {len(results)} 个错误关键词")
    
    # 统计
    error_count = count_occurrences(logs, "ERROR")
    warning_count = count_occurrences(logs, "WARNING")
    
    print(f"\n统计:")
    print(f"  ERROR 数量: {error_count}")
    print(f"  WARNING 数量: {warning_count}")


def example_dna_analysis():
    """DNA序列分析示例"""
    print("\n" + "=" * 60)
    print("实际应用: DNA序列分析")
    print("=" * 60)
    
    # 模拟DNA序列
    dna_sequence = "ATCGATCGATCGATCGATCGATCGATCGATCG"
    
    # 搜索特定模式
    patterns = ["ATCG", "GATC", "CGAT"]
    
    print(f"\nDNA序列: {dna_sequence}")
    print(f"搜索模式: {patterns}")
    
    results = multi_pattern_search(dna_sequence, patterns)
    
    print(f"\n找到 {len(results)} 处匹配:")
    for r in results[:10]:  # 显示前10个
        print(f"  '{r.pattern}' at position {r.index}")
    
    # 查找重复序列
    repeated = find_longest_repeated_substring(dna_sequence, min_length=3)
    if repeated:
        seq, positions = repeated
        print(f"\n最长重复序列: '{seq}' 出现于 {positions}")


if __name__ == "__main__":
    example_basic_search()
    example_multi_pattern()
    example_wildcard_search()
    example_repeated_substring()
    example_common_substring()
    example_similarity()
    example_plagiarism()
    example_2d_search()
    example_matcher_class()
    example_double_hash()
    example_rolling_hash()
    example_log_analysis()
    example_dna_analysis()
    
    print("\n" + "=" * 60)
    print("示例运行完成!")
    print("=" * 60)
"""
Rolling Hash Utils 使用示例

演示滚动哈希的各种使用场景：
1. 基础滚动哈希操作
2. Rabin-Karp 字符串匹配
3. 多模式匹配
4. 重复内容检测
5. 文件指纹比较
6. 最长重复子串
"""

import sys
sys.path.insert(0, '..')

from mod import (
    RollingHash,
    DoubleRollingHash,
    RabinKarp,
    MultiPatternMatcher,
    RollingHashIterator,
    DuplicateDetector,
    FileFingerprint,
    find_all_occurrences,
    find_first_occurrence,
    compute_rolling_hash,
    longest_repeated_substring,
)


def example_basic_rolling_hash():
    """示例1: 基础滚动哈希操作"""
    print("\n=== 示例1: 基础滚动哈希操作 ===")
    
    # 创建窗口大小为5的滚动哈希
    rh = RollingHash(window_size=5)
    
    # 添加字符
    text = "hello world"
    for i, char in enumerate(text):
        rh.append(char)
        if rh.is_full():
            print(f"位置 {i-4}: 窗口='{rh.get_window()}', 哈希={rh.get_hash()}")
    
    # 重置并重新使用
    rh.reset()
    rh.extend("test")
    print(f"\n重置后新哈希: {rh.get_hash()}")
    
    # 相同内容产生相同哈希
    rh1 = RollingHash(4)
    rh2 = RollingHash(4)
    rh1.extend("test")
    rh2.extend("test")
    print(f"相同内容哈希相同: {rh1.get_hash() == rh2.get_hash()}")


def example_double_rolling_hash():
    """示例2: 双重滚动哈希（减少碰撞）"""
    print("\n=== 示例2: 双重滚动哈希 ===")
    
    drh = DoubleRollingHash(window_size=4)
    
    # 计算双重哈希
    text = "hello"
    drh.extend(text)
    
    h1, h2 = drh.get_hash()
    print(f"文本: '{text}'")
    print(f"哈希1: {h1}")
    print(f"哈希2: {h2}")
    print(f"双重哈希元组: ({h1}, {h2})")
    
    # 验证一致性
    drh2 = DoubleRollingHash(4)
    drh2.extend("hello")
    print(f"\n相同内容双重哈希相同: {drh.get_hash() == drh2.get_hash()}")


def example_rabin_karp_search():
    """示例3: Rabin-Karp 字符串匹配"""
    print("\n=== 示例3: Rabin-Karp 字符串匹配 ===")
    
    # 创建匹配器
    pattern = "ab"
    rk = RabinKarp(pattern)
    
    # 查找所有匹配
    text = "abcabcab"
    matches = rk.find_all(text)
    print(f"模式: '{pattern}'")
    print(f"文本: '{text}'")
    print(f"所有匹配位置: {matches}")
    
    # 查找第一个匹配
    first = rk.find_first(text)
    print(f"第一个匹配位置: {first}")
    
    # 统计匹配次数
    count = rk.count(text)
    print(f"匹配次数: {count}")
    
    # 检查是否包含
    contains = rk.contains(text)
    print(f"是否包含: {contains}")
    
    # 使用便捷函数
    print(f"\n便捷函数查找: {find_all_occurrences('hello world hello', 'hello')}")
    print(f"便捷函数首次: {find_first_occurrence('hello world', 'world')}")


def example_multi_pattern_matcher():
    """示例4: 多模式同时匹配"""
    print("\n=== 示例4: 多模式同时匹配 ===")
    
    # 创建多模式匹配器
    patterns = ["error", "warning", "info", "debug"]
    matcher = MultiPatternMatcher(patterns)
    
    # 日志文本
    log_text = """
    [INFO] Application started
    [WARNING] Low memory
    [ERROR] Connection failed
    [INFO] Retrying connection
    [ERROR] Max retries exceeded
    """
    
    # 查找所有匹配
    results = matcher.find_all(log_text)
    
    print("日志分析结果:")
    for pattern, positions in sorted(results.items()):
        print(f"  '{pattern}': {len(positions)} 次，位置 {positions}")
    
    # 查找任意一个匹配
    any_match = matcher.find_any(log_text)
    if any_match:
        print(f"\n首次匹配: '{any_match[0]}' 在位置 {any_match[1]}")
    
    # 统计总数
    counts = matcher.count_all(log_text)
    print(f"\n统计: {counts}")


def example_duplicate_detector():
    """示例5: 重复内容检测"""
    print("\n=== 示例5: 重复内容检测 ===")
    
    detector = DuplicateDetector(min_length=4)
    
    # 检测代码中的重复
    code = """
    function process() {
        console.log("Processing...");
        // some code
    }
    function handle() {
        console.log("Processing...");
        // other code
    }
    """
    
    duplicates = detector.find_duplicates(code)
    
    print("代码重复检测结果:")
    for content, positions in duplicates.items():
        print(f"  重复内容: '{content}'")
        print(f"  出现位置: {positions}")
        print()
    
    # 检查是否有重复
    has_dup = detector.has_duplicates(code)
    print(f"是否有重复: {has_dup}")
    
    # 统计唯一子串
    unique_count = detector.count_unique_substrings("abcabcabc")
    print(f"\n'abcabcabc' 中长度为 4 的唯一子串数: {unique_count}")


def example_file_fingerprint():
    """示例6: 文件指纹比较"""
    print("\n=== 示例6: 文件指纹比较 ===")
    
    fp = FileFingerprint(chunk_size=10)
    
    # 模拟文件内容
    file1 = "Hello, this is a sample text file content."
    file2 = "Hello, this is a sample text file content."  # 完全相同
    file3 = "Hello, this is different text file content."  # 部分相似
    
    # 计算指纹
    fp1 = fp.fingerprint_string(file1)
    fp2 = fp.fingerprint_string(file2)
    fp3 = fp.fingerprint_string(file3)
    
    # 计算相似度
    sim_12 = fp.similarity(fp1, fp2)
    sim_13 = fp.similarity(fp1, fp3)
    
    print(f"文件1长度: {len(file1)}")
    print(f"指纹1块数: {len(fp1)}")
    print()
    print(f"文件1 vs 文件2 (完全相同) 相似度: {sim_12:.2%}")
    print(f"文件1 vs 文件3 (部分相似) 相似度: {sim_13:.2%}")
    
    # Jaccard 距离
    dist_12 = fp.jaccard_distance(fp1, fp2)
    dist_13 = fp.jaccard_distance(fp1, fp3)
    print(f"\nJaccard 距离:")
    print(f"  文件1 vs 文件2: {dist_12:.2f}")
    print(f"  文件1 vs 文件3: {dist_13:.2f}")


def example_rolling_hash_iterator():
    """示例7: 滚动哈希迭代器"""
    print("\n=== 示例7: 滚动哈希迭代器 ===")
    
    text = "abcdefgh"
    window_size = 3
    
    print(f"文本: '{text}', 窗口大小: {window_size}")
    print("所有窗口哈希:")
    
    iterator = RollingHashIterator(text, window_size, double_hash=True)
    
    for pos, (h1, h2), window in iterator:
        print(f"  位置 {pos}: '{window}' -> ({h1 % 10000:04d}, {h2 % 10000:04d})")


def example_longest_repeated_substring():
    """示例8: 最长重复子串"""
    print("\n=== 示例8: 最长重复子串 ===")
    
    texts = [
        "banana",
        "abcdefabcdef",
        "this is a test this is a test",
        "nothing repeated here",
    ]
    
    for text in texts:
        result = longest_repeated_substring(text)
        print(f"'{text}' -> 最长重复子串: {repr(result)}")


def example_plagiarism_detection():
    """示例9: 简单的抄袭检测"""
    print("\n=== 示例9: 简单的抄袭检测 ===")
    
    # 原文
    original = """
    The quick brown fox jumps over the lazy dog.
    This is a sample text for plagiarism detection.
    We want to find similar content in other documents.
    """
    
    # 可疑文档
    suspicious = """
    The quick brown fox jumps over the lazy dog.
    This is different from the original text here.
    We want to find similar content in other documents.
    """
    
    # 计算指纹
    fp = FileFingerprint(chunk_size=20)
    fp_orig = fp.fingerprint_string(original)
    fp_susp = fp.fingerprint_string(suspicious)
    
    # 计算相似度
    similarity = fp.similarity(fp_orig, fp_susp)
    
    print(f"原文长度: {len(original)}")
    print(f"可疑文档长度: {len(suspicious)}")
    print(f"相似度: {similarity:.2%}")
    
    if similarity > 0.7:
        print("⚠️ 警告: 高度相似，可能存在抄袭")
    elif similarity > 0.4:
        print("⚠️ 注意: 中等相似，建议进一步检查")
    else:
        print("✅ 相似度较低")


def example_dna_sequence_analysis():
    """示例10: DNA序列分析"""
    print("\n=== 示例10: DNA序列分析 ===")
    
    # DNA序列
    dna = "ATCGATCGATCGATCGATCG"
    
    # 查找重复序列
    detector = DuplicateDetector(min_length=4)
    duplicates = detector.find_duplicates(dna)
    
    print(f"DNA序列: {dna}")
    print(f"重复序列片段:")
    for seq, positions in duplicates.items():
        print(f"  '{seq}': 出现 {len(positions)} 次")
    
    # 查找最长重复子串
    longest = longest_repeated_substring(dna)
    print(f"\n最长重复子序列: {longest}")
    
    # 统计唯一子序列
    unique = detector.count_unique_substrings(dna)
    print(f"唯一子序列数量: {unique}")


def main():
    """运行所有示例"""
    print("=" * 60)
    print("Rolling Hash Utils 使用示例")
    print("=" * 60)
    
    example_basic_rolling_hash()
    example_double_rolling_hash()
    example_rabin_karp_search()
    example_multi_pattern_matcher()
    example_duplicate_detector()
    example_file_fingerprint()
    example_rolling_hash_iterator()
    example_longest_repeated_substring()
    example_plagiarism_detection()
    example_dna_sequence_analysis()
    
    print("\n" + "=" * 60)
    print("所有示例完成!")
    print("=" * 60)


if __name__ == '__main__':
    main()
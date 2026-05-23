"""
Trie Utilities 使用示例

展示字典树的各种应用场景：
1. 自动补全系统
2. 拼写检查器
3. 搜索建议
4. IP 地址路由表
5. 词频分析
"""

import sys
import os
# 添加 mod.py 所在目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 直接从 mod 导入
import mod as trie_utils_mod
Trie = trie_utils_mod.Trie
CompactTrie = trie_utils_mod.CompactTrie
SuffixTrie = trie_utils_mod.SuffixTrie
build_trie = trie_utils_mod.build_trie
build_word_trie = trie_utils_mod.build_word_trie
autocomplete_from_list = trie_utils_mod.autocomplete_from_list


def example_basic_trie():
    """
    示例 1: 基础字典树操作
    
    展示插入、搜索、删除等基础功能。
    """
    print("\n" + "=" * 60)
    print("示例 1: 基础字典树操作")
    print("=" * 60)
    
    trie = Trie()
    
    # 插入单词
    words = ["apple", "app", "application", "apply", "banana", "band", "bandana"]
    print(f"\n插入单词: {words}")
    for word in words:
        trie.insert(word)
    
    # 搜索
    print("\n搜索结果:")
    test_words = ["apple", "app", "orange", "application"]
    for word in test_words:
        result = trie.search(word)
        print(f"  '{word}': {'存在' if result else '不存在'}")
    
    # 前缀匹配
    print("\n前缀匹配 'app':")
    matches = trie.starts_with("app")
    print(f"  匹配结果: {matches}")
    
    # 删除
    print("\n删除 'apple':")
    trie.delete("apple")
    print(f"  搜索 'apple': {'存在' if trie.search('apple') else '不存在'}")
    print(f"  搜索 'app': {'存在' if trie.search('app') else '不存在'}")
    
    # 统计信息
    stats = trie.get_stats()
    print(f"\n统计信息:")
    print(f"  单词数量: {stats['word_count']}")
    print(f"  节点数量: {stats['node_count']}")
    print(f"  最大深度: {stats['max_depth']}")


def example_autocomplete():
    """
    示例 2: 自动补全系统
    
    实现一个简单的自动补全功能。
    """
    print("\n" + "=" * 60)
    print("示例 2: 自动补全系统")
    print("=" * 60)
    
    # 使用词频构建字典树
    word_frequencies = [
        ("python", 100),
        ("programming", 80),
        ("program", 75),
        ("project", 60),
        ("product", 55),
        ("practice", 50),
        ("practical", 45),
        ("print", 40),
        ("priority", 35),
        ("private", 30),
        ("public", 28),
        ("push", 25),
    ]
    
    trie = build_word_trie(word_frequencies)
    
    print("\n自动补全演示:")
    prefixes = ["pro", "pr", "p", "py"]
    
    for prefix in prefixes:
        suggestions = trie.autocomplete(prefix, limit=5)
        print(f"\n  输入 '{prefix}' 的补全建议:")
        for i, word in enumerate(suggestions, 1):
            count = trie.get_count(word)
            print(f"    {i}. {word} (词频: {count})")


def example_spelling_checker():
    """
    示例 3: 拼写检查器
    
    使用模糊搜索实现拼写检查。
    """
    print("\n" + "=" * 60)
    print("示例 3: 拼写检查器")
    print("=" * 60)
    
    # 加载词库
    dictionary = [
        "hello", "help", "held", "helmet", "helicopter",
        "world", "word", "work", "worm", "worry",
        "python", "pythons", "pyramid",
        "computer", "compute", "computing", "community",
    ]
    
    trie = build_trie(dictionary)
    
    print("\n拼写检查演示:")
    misspelled_words = ["helo", "wrld", "pthon", "compter"]
    
    for word in misspelled_words:
        print(f"\n  检查 '{word}':")
        if trie.search(word):
            print(f"    拼写正确!")
        else:
            suggestions = trie.fuzzy_search(word, max_distance=2)
            print(f"    拼写错误! 可能的正确拼写:")
            for suggestion, distance in suggestions[:5]:
                print(f"      - {suggestion} (编辑距离: {distance})")


def example_search_suggestions():
    """
    示例 4: 搜索建议系统
    
    模拟搜索引擎的搜索建议功能。
    """
    print("\n" + "=" * 60)
    print("示例 4: 搜索建议系统")
    print("=" * 60)
    
    # 搜索历史词库（带频率）
    search_history = [
        ("how to learn python", 150),
        ("how to learn java", 120),
        ("how to learn javascript", 100),
        ("how to learn coding", 90),
        ("how to make money", 80),
        ("how to cook", 75),
        ("how to tie a tie", 70),
        ("how to lose weight", 65),
        ("python tutorial", 200),
        ("python for beginners", 180),
        ("python web scraping", 150),
        ("python machine learning", 140),
    ]
    
    trie = build_word_trie(search_history)
    
    print("\n搜索建议演示:")
    queries = ["how to", "python", "how"]
    
    for query in queries:
        suggestions = trie.autocomplete(query, limit=5)
        print(f"\n  输入 '{query}' 的搜索建议:")
        for i, suggestion in enumerate(suggestions, 1):
            count = trie.get_count(suggestion)
            print(f"    {i}. {suggestion} (搜索次数: {count})")


def example_word_frequency_analysis():
    """
    示例 5: 词频分析
    
    分析文本中的词频分布。
    """
    print("\n" + "=" * 60)
    print("示例 5: 词频分析")
    print("=" * 60)
    
    # 示例文本（已分词）
    text_words = [
        "the", "quick", "brown", "fox", "jumps", "over", "the", "lazy", "dog",
        "the", "fox", "is", "quick", "and", "the", "dog", "is", "lazy",
        "quick", "fox", "lazy", "dog", "the", "the", "the",
    ]
    
    trie = Trie()
    for word in text_words:
        trie.insert(word)
    
    print("\n词频统计:")
    words_with_counts = trie.list_with_counts()
    words_with_counts.sort(key=lambda x: x[1], reverse=True)
    
    for word, count in words_with_counts:
        print(f"  '{word}': {count} 次")
    
    # 高频词前缀分析
    print("\n高频词分析:")
    high_freq_prefixes = trie.autocomplete("", limit=3)
    print(f"  前 3 高频词: {high_freq_prefixes}")


def example_suffix_trie():
    """
    示例 6: 后缀树应用
    
    使用后缀树查找子串和重复模式。
    """
    print("\n" + "=" * 60)
    print("示例 6: 后缀树应用")
    print("=" * 60)
    
    text = "abracadabra"
    suffix_trie = SuffixTrie()
    suffix_trie.build(text)
    
    print(f"\n分析文本: '{text}'")
    
    # 子串查找
    patterns = ["abra", "cad", "bra", "xyz"]
    print("\n子串查找:")
    for pattern in patterns:
        count = suffix_trie.count_occurrences(pattern)
        positions = suffix_trie.find_all_occurrences(pattern)
        print(f"  '{pattern}': 出现 {count} 次, 位置: {positions}")
    
    # 最长重复子串
    lrs = suffix_trie.longest_repeated_substring()
    print(f"\n最长重复子串: '{lrs}'")


def example_longest_prefix_matching():
    """
    示例 7: 最长前缀匹配
    
    类似 IP 路由表或 URL 路由的应用。
    """
    print("\n" + "=" * 60)
    print("示例 7: 最长前缀匹配")
    print("=" * 60)
    
    # URL 路径配置
    routes = [
        "/api/users",
        "/api/users/profile",
        "/api/products",
        "/api/products/list",
        "/static",
        "/static/images",
        "/static/css",
    ]
    
    trie = build_trie(routes)
    
    print("\nURL 路由匹配:")
    test_urls = [
        "/api/users/profile/settings",
        "/api/products/list/123",
        "/api/orders",  # 不存在
        "/static/images/logo.png",
        "/unknown",  # 不存在
    ]
    
    for url in test_urls:
        matched = trie.longest_prefix(url)
        if matched:
            print(f"  '{url}' -> 匹配路由: '{matched}'")
        else:
            print(f"  '{url}' -> 无匹配路由")


def example_serialization():
    """
    示例 8: 序列化和反序列化
    
    保存和加载字典树状态。
    """
    print("\n" + "=" * 60)
    print("示例 8: 序列化和反序列化")
    print("=" * 60)
    
    trie = Trie()
    words = ["hello", "world", "python", "programming"]
    for word in words:
        trie.insert(word)
    
    # 序列化
    json_str = trie.to_json()
    print(f"\n序列化结果 (前 500 字符):")
    print(f"  {json_str[:500]}...")
    
    # 反序列化
    restored = Trie.from_json(json_str)
    print(f"\n反序列化验证:")
    print(f"  单词数量: {len(restored)}")
    print(f"  所有单词: {restored.list_all()}")
    
    # 验证数据一致性
    for word in words:
        print(f"  '{word}': {'匹配' if restored.search(word) else '不匹配'}")


def example_compact_trie():
    """
    示例 9: 压缩字典树
    
    空间优化的字典树实现。
    """
    print("\n" + "=" * 60)
    print("示例 9: 压缩字典树")
    print("=" * 60)
    
    # 大量共享前缀的单词
    words = [
        "inter", "internet", "internal", "international",
        "interface", "interact", "intercept",
    ]
    
    print(f"\n单词列表: {words}")
    
    # 普通 Trie
    regular_trie = Trie()
    for word in words:
        regular_trie.insert(word)
    
    regular_stats = regular_trie.get_stats()
    
    # 压缩 Trie
    compact_trie = CompactTrie()
    for word in words:
        compact_trie.insert(word)
    
    print(f"\n空间效率对比:")
    print(f"  普通 Trie 节点数: {regular_stats['node_count']}")
    print(f"  普通 Trie 单词数: {regular_stats['word_count']}")
    print(f"  压缩 Trie 单词数: {len(compact_trie)}")
    
    # 功能验证
    print(f"\n功能验证:")
    for word in words:
        found = compact_trie.search(word)
        print(f"  '{word}': {'找到' if found else '未找到'}")


def example_dictionary_building():
    """
    示例 10: 构建字典
    
    从文本数据构建词典。
    """
    print("\n" + "=" * 60)
    print("示例 10: 构建字典")
    print("=" * 60)
    
    # 模拟从文本提取的单词
    text_corpus = """
    The Python programming language is widely used for web development,
    data analysis, artificial intelligence, and machine learning.
    Python is known for its simplicity and readability.
    Many developers prefer Python for rapid prototyping.
    """
    
    # 提取单词（简化版）
    words = []
    for word in text_corpus.lower().split():
        # 移除标点
        clean_word = ''.join(c for c in word if c.isalpha())
        if clean_word:
            words.append(clean_word)
    
    # 构建词频字典树
    trie = Trie()
    for word in words:
        trie.insert(word)
    
    print(f"\n从文本构建的字典:")
    print(f"  总单词数: {len(words)}")
    print(f"  不同单词数: {len(trie)}")
    
    # 按频率排序
    words_with_counts = trie.list_with_counts()
    words_with_counts.sort(key=lambda x: x[1], reverse=True)
    
    print(f"\n高频词 (前 10):")
    for word, count in words_with_counts[:10]:
        print(f"  '{word}': {count} 次")


def main():
    """运行所有示例"""
    print("=" * 60)
    print("Trie Utilities 使用示例集")
    print("=" * 60)
    
    example_basic_trie()
    example_autocomplete()
    example_spelling_checker()
    example_search_suggestions()
    example_word_frequency_analysis()
    example_suffix_trie()
    example_longest_prefix_matching()
    example_serialization()
    example_compact_trie()
    example_dictionary_building()
    
    print("\n" + "=" * 60)
    print("所有示例演示完成!")
    print("=" * 60)


if __name__ == "__main__":
    main()
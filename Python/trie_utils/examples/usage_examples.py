"""
Trie 工具模块使用示例

展示核心功能：
1. Trie 基本操作
2. 自动补全系统
3. 拼写检查器
4. 通配符匹配
5. 后缀搜索
"""

import sys
import os

# 直接从父目录导入 mod
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import mod

# 使用 mod 模块中的类
Trie = mod.Trie
SpellChecker = mod.SpellChecker
WordDictionary = mod.WordDictionary
SuffixTrie = mod.SuffixTrie
TrieSet = mod.TrieSet
build_trie_from_words = mod.build_trie_from_words
find_common_prefix = mod.find_common_prefix
group_by_prefix = mod.group_by_prefix
autocomplete_suggestions = mod.autocomplete_suggestions


def example_basic_trie():
    """示例 1: Trie 基本操作"""
    print("=" * 50)
    print("示例 1: Trie 基本操作")
    print("=" * 50)
    
    # 创建 Trie 并插入单词
    trie = Trie()
    words = ["apple", "application", "apply", "appetite", "banana", "band"]
    
    for word in words:
        trie.insert(word)
    
    print(f"\n插入单词: {words}")
    print(f"Trie 中单词数量: {len(trie)}")
    
    # 搜索
    print(f"\n搜索 'apple': {trie.search('apple')}")
    print(f"搜索 'app': {trie.search('app')}")
    print(f"搜索 'orange': {trie.search('orange')}")
    
    # 前缀搜索
    print(f"\n以 'app' 开头的单词: {trie.starts_with('app')}")
    print(f"以 'ban' 开头的单词: {trie.starts_with('ban')}")
    
    # 自动补全
    print(f"\n自动补全 'app' (按字母顺序): {trie.autocomplete('app', limit=3)}")
    
    # 词频统计
    trie.insert("apple")
    trie.insert("apple")
    print(f"\n'apple' 出现次数: {trie.get_count('apple')}")
    
    # 公共前缀
    print(f"\n最长公共前缀: {trie.longest_common_prefix()}")
    
    # 删除
    print(f"\n删除 'apple': {trie.delete('apple')}")
    print(f"删除后 'apple' 是否存在: {trie.search('apple')}")
    
    print()


def example_autocomplete_system():
    """示例 2: 自动补全系统"""
    print("=" * 50)
    print("示例 2: 自动补全系统")
    print("=" * 50)
    
    # 构建搜索引擎的自动补全词库
    search_trie = Trie()
    
    # 模拟搜索词频（多次插入增加词频）
    common_searches = [
        ("python", 10),
        ("python tutorial", 8),
        ("python for loop", 7),
        ("python list comprehension", 6),
        ("python dictionary", 5),
        ("javascript", 9),
        ("javascript async", 4),
        ("java", 8),
        ("java spring", 3),
    ]
    
    for word, count in common_searches:
        for _ in range(count):
            search_trie.insert(word)
    
    # 模拟用户输入，提供补全建议
    user_inputs = ["py", "jav", "python "]
    
    for prefix in user_inputs:
        suggestions = search_trie.autocomplete(prefix, limit=5, sort_by='frequency')
        print(f"\n用户输入: '{prefix}'")
        print(f"补全建议 (按词频): {suggestions}")
    
    print()


def example_spell_checker():
    """示例 3: 拼写检查器"""
    print("=" * 50)
    print("示例 3: 拼写检查器")
    print("=" * 50)
    
    # 创建拼写检查器并加载词典
    checker = SpellChecker(max_edit_distance=2)
    
    # 常见英文单词
    dictionary = [
        "the", "be", "to", "of", "and", "a", "in", "that", "have", "I",
        "it", "for", "not", "on", "with", "he", "as", "you", "do", "at",
        "this", "but", "his", "by", "from", "they", "we", "say", "her", "she",
        "or", "an", "will", "my", "one", "all", "would", "there", "their", "what",
        "hello", "world", "help", "held", "helder", "python", "javascript"
    ]
    
    checker.load_words(dictionary)
    
    # 测试拼写检查
    test_words = ["hello", "helo", "wrld", "pyton", "javascrpt"]
    
    for word in test_words:
        is_correct = checker.is_correct(word)
        suggestions = checker.suggest(word, limit=3)
        
        status = "✓ 正确" if is_correct else "✗ 拼写错误"
        print(f"\n单词: '{word}' - {status}")
        if not is_correct:
            print(f"建议: {suggestions}")
    
    print()


def example_wildcard_matching():
    """示例 4: 通配符匹配"""
    print("=" * 50)
    print("示例 4: 通配符匹配")
    print("=" * 50)
    
    # 创建支持通配符的字典
    wd = WordDictionary()
    
    # 添加编程语言名称
    languages = [
        "python", "python3", "python2",
        "javascript", "java",
        "typescript", "typescript4",
        "ruby", "rust", "go", "golang"
    ]
    
    for lang in languages:
        wd.add_word(lang)
    
    print(f"已添加编程语言: {languages}")
    
    # 使用通配符搜索
    patterns = [
        "python.",      # 匹配 python3, python2
        "java*",        # 匹配 java, javascript
        "type*4",       # 匹配 typescript4
        "go",           # 精确匹配 go
        "r.b.",         # 匹配 ruby
    ]
    
    for pattern in patterns:
        matches = wd.find_all_matches(pattern)
        print(f"\n模式 '{pattern}' 匹配结果: {matches}")
    
    print()


def example_suffix_search():
    """示例 5: 后缀搜索"""
    print("=" * 50)
    print("示例 5: 后缀搜索")
    print("=" * 50)
    
    # 创建后缀 Trie
    text = "mississippi"
    st = SuffixTrie(text)
    
    print(f"文本: '{text}'")
    
    # 子串查找
    patterns = ["iss", "si", "ppi", "xyz"]
    
    for pattern in patterns:
        contains = st.contains(pattern)
        positions = st.find_all(pattern)
        count = st.count_occurrences(pattern)
        
        print(f"\n模式 '{pattern}':")
        print(f"  是否包含: {contains}")
        print(f"  出现位置: {positions}")
        print(f"  出现次数: {count}")
    
    # 查找最长重复子串
    print(f"\n最长重复子串: '{st.longest_repeated_substring()}'")
    
    print()


def example_trie_set():
    """示例 6: TrieSet 集合操作"""
    print("=" * 50)
    print("示例 6: TrieSet 集合操作")
    print("=" * 50)
    
    # 创建两个字符串集合
    set1 = TrieSet(["apple", "banana", "cherry", "date"])
    set2 = TrieSet(["banana", "date", "elderberry", "fig"])
    
    print(f"集合 1: {list(set1)}")
    print(f"集合 2: {list(set2)}")
    
    # 集合操作
    print(f"\n并集: {list(set1.union(set2))}")
    print(f"交集: {list(set1.intersection(set2))}")
    print(f"差集 (set1 - set2): {list(set1.difference(set2))}")
    
    # 集合判断
    print(f"\n是否不相交: {set1.isdisjoint(set2)}")
    
    subset = TrieSet(["banana", "date"])
    print(f"{list(subset)} 是 set1 的子集: {subset.issubset(set1)}")
    
    print()


def example_prefix_analysis():
    """示例 7: 前缀分析工具"""
    print("=" * 50)
    print("示例 7: 前缀分析工具")
    print("=" * 50)
    
    # 文件名列表
    filenames = [
        "document_2023_01.txt",
        "document_2023_02.txt",
        "document_2023_03.txt",
        "image_photo_001.jpg",
        "image_photo_002.jpg",
        "image_screenshot.png",
        "data_export.csv",
        "data_import.csv",
    ]
    
    print("文件名列表:")
    for f in filenames:
        print(f"  {f}")
    
    # 按前缀分组
    groups = group_by_prefix(filenames, prefix_len=4)
    print("\n按前缀分组:")
    for prefix, files in groups.items():
        print(f"  '{prefix}': {files}")
    
    # 查找公共前缀
    docs = [f for f in filenames if f.startswith("document")]
    common = find_common_prefix(docs)
    print(f"\ndocument 文件的公共前缀: '{common}'")
    
    print()


def example_word_dictionary_with_data():
    """示例 8: 带数据的单词字典"""
    print("=" * 50)
    print("示例 8: 带数据的单词字典")
    print("=" * 50)
    
    # 创建带附加数据的 Trie
    trie = Trie()
    
    # 添加单词及其定义
    words_data = [
        ("python", {"type": "noun", "meaning": "a large snake", "programming": True}),
        ("javascript", {"type": "noun", "meaning": "a programming language", "programming": True}),
        ("java", {"type": "noun", "meaning": "coffee", "programming": True}),
        ("trie", {"type": "noun", "meaning": "a tree data structure", "programming": False}),
    ]
    
    for word, data in words_data:
        trie.insert(word, data)
    
    # 查询单词
    query_words = ["python", "javascript", "java", "trie", "ruby"]
    
    for word in query_words:
        if trie.search(word):
            data = trie.get_data(word)
            print(f"\n{word}:")
            print(f"  类型: {data['type']}")
            print(f"  含义: {data['meaning']}")
            print(f"  编程相关: {data['programming']}")
        else:
            print(f"\n{word}: 未找到")
    
    print()


def main():
    """运行所有示例"""
    print("\n" + "=" * 60)
    print("Trie 工具模块 - 使用示例")
    print("=" * 60 + "\n")
    
    example_basic_trie()
    example_autocomplete_system()
    example_spell_checker()
    example_wildcard_matching()
    example_suffix_search()
    example_trie_set()
    example_prefix_analysis()
    example_word_dictionary_with_data()
    
    print("=" * 60)
    print("所有示例运行完成!")
    print("=" * 60)


if __name__ == "__main__":
    main()
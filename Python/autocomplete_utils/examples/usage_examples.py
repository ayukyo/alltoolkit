"""
自动补全工具使用示例
Autocomplete Utilities Usage Examples

演示如何使用 autocomplete_utils 模块的各种功能
"""

from mod import (
    TrieAutocomplete, NGramAutocomplete, HybridAutocomplete,
    create_autocomplete, levenshtein_distance, jaccard_similarity
)


def example_basic_trie():
    """基本 Trie 自动补全示例"""
    print("=" * 50)
    print("基本 Trie 自动补全示例")
    print("=" * 50)
    
    # 创建 Trie 自动补全器
    trie = TrieAutocomplete()
    
    # 添加单词
    programming_words = [
        "python", "javascript", "java", "ruby", "rust",
        "programming", "program", "programmer",
        "function", "functional", "functionality",
        "variable", "value", "var",
        "class", "classic", "classification",
        "object", "objective", "object-oriented"
    ]
    
    for word in programming_words:
        trie.insert(word)
    
    print(f"已添加 {len(trie)} 个单词")
    print()
    
    # 前缀搜索
    print("搜索前缀 'pro':")
    results = trie.search("pro")
    for r in results:
        print(f"  - {r.text} (频率: {r.frequency})")
    print()
    
    print("搜索前缀 'func':")
    results = trie.search("func")
    for r in results:
        print(f"  - {r.text}")
    print()
    
    print("搜索前缀 'var':")
    results = trie.search("var")
    for r in results:
        print(f"  - {r.text}")
    print()


def example_frequency_based():
    """基于频率的排序示例"""
    print("=" * 50)
    print("基于频率的排序示例")
    print("=" * 50)
    
    trie = TrieAutocomplete()
    
    # 添加单词，并设置频率（模拟用户使用频率）
    search_suggestions = [
        ("google", 1000),
        ("github", 500),
        ("gmail", 300),
        ("google maps", 200),
        ("google translate", 150),
        ("google drive", 100),
        ("golang", 80),
        ("good", 50),
        ("go", 40),
        ("godot", 30)
    ]
    
    for word, freq in search_suggestions:
        trie.insert(word, frequency=freq)
    
    print("搜索 'g':")
    results = trie.search("g")
    print("结果按频率排序:")
    for r in results:
        print(f"  - {r.text} (频率: {r.frequency}, 得分: {r.score:.2f})")
    print()
    
    # 模拟用户选择
    print("用户选择了 'google maps'，增加频率...")
    trie.increment_frequency("google maps", 50)
    
    print("再次搜索 'g':")
    results = trie.search("g")
    print("'google maps' 排名应该上升")
    for r in results[:5]:
        print(f"  - {r.text} (频率: {r.frequency})")
    print()


def example_fuzzy_search():
    """模糊搜索示例"""
    print("=" * 50)
    print("模糊搜索示例")
    print("=" * 50)
    
    trie = TrieAutocomplete()
    
    # 添加常见单词
    common_words = [
        "hello", "help", "helicopter", "helium",
        "world", "word", "work", "worker",
        "programming", "program", "progress",
        "computer", "compute", "computing"
    ]
    
    for word in common_words:
        trie.insert(word)
    
    # 模糊搜索 - 有拼写错误的查询
    queries = ["helo", "wrld", "progamming"]
    
    for query in queries:
        print(f"模糊搜索 '{query}' (编辑距离 ≤ 2):")
        results = trie.fuzzy_search(query, max_distance=2)
        for r in results:
            print(f"  - {r.text} (得分: {r.score:.2f})")
        print()


def example_ngram_autocomplete():
    """N-gram 自动补全示例"""
    print("=" * 50)
    print("N-gram 自动补全示例")
    print("=" * 50)
    
    ngram = NGramAutocomplete(n=2)
    
    # 添加单词
    words = [
        "apple", "application", "apply", "appetite",
        "banana", "bandana", "band",
        "cherry", "cherry-pick", "cherish"
    ]
    
    for word in words:
        ngram.insert(word)
    
    print(f"已添加 {len(ngram)} 个单词")
    print()
    
    # 前缀搜索
    print("前缀搜索 'app':")
    results = ngram.prefix_search("app")
    for r in results:
        print(f"  - {r.text}")
    print()
    
    # 模糊匹配
    print("模糊搜索 'aple':")
    results = ngram.search("aple")
    for r in results:
        print(f"  - {r.text} (得分: {r.score:.2f})")
    print()
    
    # 统计信息
    stats = ngram.get_stats()
    print("统计信息:")
    print(f"  - 单词数: {stats['word_count']}")
    print(f"  - N-gram 数: {stats['ngram_count']}")
    print(f"  - N 值: {stats['n']}")
    print()


def example_hybrid_autocomplete():
    """混合自动补全示例"""
    print("=" * 50)
    print("混合自动补全示例")
    print("=" * 50)
    
    hybrid = HybridAutocomplete(fuzzy_weight=0.3)
    
    # 添加编程语言和相关术语
    terms = [
        ("python", 500),
        ("python3", 300),
        ("javascript", 400),
        ("java", 450),
        ("ruby", 200),
        ("rust", 150),
        ("go", 100),
        ("golang", 80),
        ("typescript", 120),
        ("csharp", 90),
        ("cpp", 85),
        ("programming", 1000),
        ("function", 300),
        ("variable", 250)
    ]
    
    for word, freq in terms:
        hybrid.insert(word, frequency=freq)
    
    print(f"已添加 {len(hybrid)} 个术语")
    print()
    
    # 精确前缀搜索
    print("精确前缀搜索 'py' (禁用模糊):")
    results = hybrid.search("py", fuzzy=False)
    for r in results:
        print(f"  - {r.text}")
    print()
    
    # 模糊搜索
    print("模糊搜索 'pythn' (启用模糊):")
    results = hybrid.search("pythn", fuzzy=True)
    for r in results:
        print(f"  - {r.text} (得分: {r.score:.2f})")
    print()
    
    print("模糊搜索 'javascipt' (启用模糊):")
    results = hybrid.search("javascipt", fuzzy=True)
    for r in results:
        print(f"  - {r.text} (得分: {r.score:.2f})")
    print()


def example_case_sensitive():
    """区分大小写示例"""
    print("=" * 50)
    print("区分大小写示例")
    print("=" * 50)
    
    # 区分大小写
    trie = TrieAutocomplete(case_sensitive=True)
    
    # 添加不同大小写的单词
    words = ["Python", "python", "PYTHON", "pyThon"]
    for word in words:
        trie.insert(word)
    
    print(f"已添加 {len(trie)} 个单词（区分大小写）")
    print()
    
    print("搜索 'Py':")
    results = trie.search("Py")
    for r in results:
        print(f"  - {r.text}")
    print()
    
    print("搜索 'py':")
    results = trie.search("py")
    for r in results:
        print(f"  - {r.text}")
    print()
    
    # 不区分大小写
    trie_lower = TrieAutocomplete(case_sensitive=False)
    for word in words:
        trie_lower.insert(word)
    
    print(f"已添加 {len(trie_lower)} 个单词（不区分大小写）")
    print()
    
    print("搜索 'py':")
    results = trie_lower.search("py")
    for r in results:
        print(f"  - {r.text}")
    print("所有变体都被合并为一个")
    print()


def example_serialization():
    """序列化示例"""
    print("=" * 50)
    print("序列化示例")
    print("=" * 50)
    
    trie = TrieAutocomplete()
    
    words = [
        ("hello", 100, {"category": "greeting"}),
        ("world", 80, {"category": "noun"}),
        ("computer", 50, {"category": "noun"}),
        ("programming", 60, {"category": "verb"})
    ]
    
    for word, freq, meta in words:
        trie.insert(word, frequency=freq, metadata=meta)
    
    print("原始 Trie:")
    print(f"  - 单词数: {len(trie)}")
    print(f"  - 统计: {trie.get_stats()}")
    print()
    
    # 序列化为 JSON
    json_str = trie.to_json()
    print("JSON 序列化 (前 200 字符):")
    print(f"  {json_str[:200]}...")
    print()
    
    # 反序列化
    restored = TrieAutocomplete.from_json(json_str)
    print("反序列化后的 Trie:")
    print(f"  - 单词数: {len(restored)}")
    print(f"  - hello 信息: {restored.get_word_info('hello')}")
    print()


def example_real_world_search():
    """实际应用场景：搜索建议"""
    print("=" * 50)
    print("实际应用场景：搜索引擎建议")
    print("=" * 50)
    
    # 创建搜索引擎建议系统
    search_engine = TrieAutocomplete(max_suggestions=8)
    
    # 添加热门搜索词
    hot_searches = [
        ("python教程", 10000),
        ("python安装", 8000),
        ("python爬虫", 7000),
        ("python数据分析", 6000),
        ("python机器学习", 5000),
        ("javascript教程", 9000),
        ("javascript框架", 4000),
        ("java教程", 8500),
        ("java开发", 3000),
        ("人工智能", 12000),
        ("人工智能入门", 6000),
        ("深度学习", 8000),
        ("机器学习", 9000),
        ("数据分析", 7000),
        ("数据可视化", 5000)
    ]
    
    for term, freq in hot_searches:
        search_engine.insert(term, frequency=freq)
    
    print("模拟用户输入:")
    print()
    
    # 用户输入 "py"
    print("输入: 'py'")
    results = search_engine.search("py")
    print("建议:")
    for r in results:
        print(f"  - {r.text} (热度: {r.frequency})")
    print()
    
    # 用户继续输入 "python"
    print("输入: 'python'")
    results = search_engine.search("python")
    print("建议:")
    for r in results:
        print(f"  - {r.text}")
    print()
    
    # 用户输入 "人"
    print("输入: '人'")
    results = search_engine.search("人")
    print("建议:")
    for r in results:
        print(f"  - {r.text}")
    print()


def example_distance_functions():
    """编辑距离和相似度函数示例"""
    print("=" * 50)
    print("编辑距离和相似度函数示例")
    print("=" * 50)
    
    # 编辑距离
    pairs = [
        ("hello", "hello"),
        ("hello", "helo"),
        ("hello", "world"),
        ("kitten", "sitting"),
        ("algorithm", "altruistic")
    ]
    
    print("编辑距离:")
    for s1, s2 in pairs:
        dist = levenshtein_distance(s1, s2)
        print(f"  '{s1}' vs '{s2}' -> {dist}")
    print()
    
    # Jaccard 相似度
    pairs = [
        ("hello", "hello"),
        ("hello", "helo"),
        ("hello", "world"),
        ("programming", "program"),
        ("python", "python3")
    ]
    
    print("Jaccard 相似度 (N=2):")
    for s1, s2 in pairs:
        sim = jaccard_similarity(s1, s2)
        print(f"  '{s1}' vs '{s2}' -> {sim:.2f}")
    print()


def example_quick_create():
    """快速创建自动补全器示例"""
    print("=" * 50)
    print("快速创建自动补全器示例")
    print("=" * 50)
    
    # 快速创建 Trie 自动补全器
    words = ["apple", "banana", "cherry", "date", "elderberry"]
    trie = create_autocomplete(words)
    
    print(f"创建 Trie 自动补全器，包含 {len(trie)} 个单词")
    print("搜索 'a':")
    results = trie.search("a")
    for r in results:
        print(f"  - {r.text}")
    print()
    
    # 快速创建 N-gram 自动补全器
    ngram = create_autocomplete(words, use_ngram=True)
    
    print(f"创建 N-gram 自动补全器，包含 {len(ngram)} 个单词")
    print("搜索 'aple':")
    results = ngram.search("aple")
    for r in results:
        print(f"  - {r.text} (得分: {r.score:.2f})")
    print()


def main():
    """运行所有示例"""
    example_basic_trie()
    example_frequency_based()
    example_fuzzy_search()
    example_ngram_autocomplete()
    example_hybrid_autocomplete()
    example_case_sensitive()
    example_serialization()
    example_real_world_search()
    example_distance_functions()
    example_quick_create()
    
    print("=" * 50)
    print("所有示例完成!")
    print("=" * 50)


if __name__ == "__main__":
    main()
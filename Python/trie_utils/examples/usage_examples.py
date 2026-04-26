"""
Trie 工具模块使用示例

展示 Trie 数据结构的各种应用场景：
1. 自动补全系统
2. 拼写检查
3. IP路由查找
4. 词典实现
5. 搜索建议
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    Trie, SuffixTrie, PrefixSet,
    build_trie, find_common_prefix, word_frequency_analysis
)


def example_autocomplete():
    """示例：自动补全系统"""
    print("=" * 60)
    print("示例 1：自动补全系统")
    print("=" * 60)
    
    # 构建词典（模拟搜索历史）
    trie = Trie()
    search_history = [
        "python tutorial",
        "python basics",
        "python web development",
        "python data science",
        "python machine learning",
        "javascript tutorial",
        "javascript react",
        "java tutorial",
        "java spring boot",
    ]
    
    # 插入搜索历史（多次搜索提高权重）
    for _ in range(5):
        trie.insert("python tutorial")
    for _ in range(3):
        trie.insert("python basics")
    for _ in range(2):
        trie.insert("python web development")
    for _ in range(4):
        trie.insert("javascript tutorial")
    for _ in range(1):
        trie.insert("python data science")
    
    print("\n用户输入 'py'，建议：")
    suggestions = trie.autocomplete("py", max_suggestions=5)
    for word, count in suggestions:
        print(f"  {word} (搜索{count}次)")
    
    print("\n用户输入 'jav'，建议：")
    suggestions = trie.autocomplete("jav", max_suggestions=5)
    for word, count in suggestions:
        print(f"  {word} (搜索{count}次)")
    
    print()


def example_spell_checker():
    """示例：拼写检查器"""
    print("=" * 60)
    print("示例 2：拼写检查器")
    print("=" * 60)
    
    # 构建词典
    trie = Trie()
    dictionary = [
        "hello", "world", "python", "javascript", "programming",
        "computer", "algorithm", "data", "structure", "array",
        "string", "integer", "float", "boolean", "function"
    ]
    for word in dictionary:
        trie.insert(word)
    
    # 检查拼写错误
    misspelled = ["helo", "wrld", "pyton", "prgramming", "computr"]
    
    print("\n拼写检查结果：")
    for word in misspelled:
        if not trie.search(word):
            suggestions = trie.suggest_corrections(word, max_distance=2)[:3]
            print(f"\n'{word}' 可能是拼写错误，建议：")
            for suggestion, distance in suggestions:
                print(f"  {suggestion} (编辑距离: {distance})")
        else:
            print(f"\n'{word}' 拼写正确")
    
    print()


def example_ip_router():
    """示例：IP路由查找"""
    print("=" * 60)
    print("示例 3：IP路由查找")
    print("=" * 60)
    
    # 构建路由表（简化示例）
    routes = PrefixSet()
    routes.update([
        "10.",      # 私有网络 A
        "192.168.", # 私有网络 C
        "172.16.",  # 私有网络 B
        "8.8.",     # Google DNS
        "1.1.",     # Cloudflare DNS
    ])
    
    test_ips = [
        "10.0.0.1",
        "192.168.1.100",
        "8.8.8.8",
        "172.16.0.1",
        "93.184.216.34",  # 无匹配
    ]
    
    print("\nIP路由查找结果：")
    for ip in test_ips:
        prefix = routes.get_matching_prefix(ip)
        if prefix:
            print(f"  {ip} -> 匹配路由: {prefix}...")
        else:
            print(f"  {ip} -> 使用默认路由")
    
    print()


def example_dictionary():
    """示例：词典实现"""
    print("=" * 60)
    print("示例 4：词典实现")
    print("=" * 60)
    
    # 构建英汉词典
    trie = Trie()
    dictionary = {
        "hello": {"meaning": "你好", "pos": "int."},
        "help": {"meaning": "帮助", "pos": "v./n."},
        "helper": {"meaning": "助手", "pos": "n."},
        "helicopter": {"meaning": "直升机", "pos": "n."},
        "world": {"meaning": "世界", "pos": "n."},
        "word": {"meaning": "单词", "pos": "n."},
        "work": {"meaning": "工作", "pos": "v./n."},
    }
    
    for word, info in dictionary.items():
        trie.insert(word, data=info)
    
    print("\n词典查询示例：")
    
    # 查询单词
    word = "hello"
    data = trie.get_data(word)
    if data:
        print(f"\n  {word}: {data['meaning']} ({data['pos']})")
    
    # 前缀查询
    print("\n以 'hel' 开头的单词：")
    for word in trie.starts_with("hel"):
        data = trie.get_data(word)
        print(f"  {word}: {data['meaning']}")
    
    # 通配符查询
    print("\n模式 'w?r?' 匹配：")
    for word in trie.pattern_match("w?r?"):
        data = trie.get_data(word)
        print(f"  {word}: {data['meaning']}")
    
    print()


def example_search_engine():
    """示例：搜索引擎关键词过滤"""
    print("=" * 60)
    print("示例 5：关键词过滤系统")
    print("=" * 60)
    
    # 构建敏感词库
    trie = Trie()
    sensitive_words = ["暴力", "色情", "赌博", "诈骗", "毒品"]
    for word in sensitive_words:
        trie.insert(word)
    
    # 检测文本
    texts = [
        "这是一个正常的内容",
        "这里包含暴力内容",
        "打击网络诈骗是重点",
        "禁毒教育很重要，远离毒品",
    ]
    
    print("\n内容审核结果：")
    for text in texts:
        found = []
        for i in range(len(text)):
            prefix = trie.longest_prefix(text[i:])
            if prefix:
                found.append(prefix)
        
        if found:
            print(f"  '{text}' -> 发现敏感词: {found}")
        else:
            print(f"  '{text}' -> 审核通过")
    
    print()


def example_word_game():
    """示例：单词游戏辅助"""
    print("=" * 60)
    print("示例 6：单词游戏辅助")
    print("=" * 60)
    
    # 加载单词库
    trie = Trie()
    words = [
        "cat", "car", "card", "care", "careful",
        "bat", "bar", "bard", "bare", "barely",
        "rat", "radar", "rare", "rate", "rather"
    ]
    for word in words:
        trie.insert(word)
    
    print("\n游戏场景：拼字游戏")
    
    # 1. 给定前缀，找所有可能的单词
    prefix = "car"
    print(f"\n前缀 '{prefix}' 可以组成：")
    print(f"  {trie.starts_with(prefix)}")
    
    # 2. 给定字母模式，找匹配单词（? 代表任意字母）
    pattern = "?are"
    print(f"\n模式 '{pattern}' 匹配：")
    print(f"  {trie.pattern_match(pattern)}")
    
    # 3. 最长单词
    given = "careful"
    longest = trie.longest_prefix(given)
    print(f"\n给定 '{given}'，最长匹配：")
    print(f"  {longest}")
    
    print()


def example_data_serialization():
    """示例：数据序列化"""
    print("=" * 60)
    print("示例 7：数据持久化")
    print("=" * 60)
    
    # 构建词典
    trie = Trie()
    words = ["apple", "application", "apply", "appreciate"]
    for word in words:
        trie.insert(word)
    
    print(f"\n原始 Trie 大小: {trie.size()} 个单词")
    
    # 序列化为 JSON
    json_str = trie.to_json()
    print(f"序列化后 JSON 长度: {len(json_str)} 字符")
    
    # 反序列化
    new_trie = Trie.from_json(json_str)
    print(f"反序列化后大小: {new_trie.size()} 个单词")
    
    # 验证数据完整性
    print("\n验证数据完整性:")
    for word in words:
        original = trie.search(word)
        restored = new_trie.search(word)
        print(f"  {word}: 原={original}, 恢复={restored}, {'✓' if original == restored else '✗'}")
    
    print()


def example_frequency_analysis():
    """示例：词频分析"""
    print("=" * 60)
    print("示例 8：词频统计与分析")
    print("=" * 60)
    
    # 模拟文本数据
    text = """
    python is a popular programming language
    python is used for web development
    python is used for data science
    python has a simple syntax
    python is easy to learn
    """
    
    words = text.lower().split()
    
    # 使用工具函数分析词频
    freq = word_frequency_analysis(words)
    
    print("\n词频统计结果：")
    for word, count in list(freq.items())[:5]:
        print(f"  {word}: {count}次")
    
    # 查找公共前缀
    word_list = ["programming", "programmer", "program", "progressive"]
    common = find_common_prefix(word_list)
    print(f"\n单词 {word_list} 的公共前缀: '{common}'")
    
    print()


def example_suffix_trie():
    """示例：后缀树"""
    print("=" * 60)
    print("示例 9：后缀树（子串匹配）")
    print("=" * 60)
    
    st = SuffixTrie()
    text = "abracadabra"
    
    print(f"\n构建字符串 '{text}' 的后缀树...")
    st.build_from_string(text)
    
    patterns = ["abra", "cad", "xyz", "bra"]
    
    print("\n子串匹配结果：")
    for pattern in patterns:
        found = st.contains_substring(pattern)
        print(f"  '{pattern}' -> {'找到' if found else '未找到'}")
    
    print()


def main():
    """运行所有示例"""
    print("\n" + "=" * 60)
    print("    Trie 工具模块 - 使用示例")
    print("=" * 60 + "\n")
    
    example_autocomplete()
    example_spell_checker()
    example_ip_router()
    example_dictionary()
    example_search_engine()
    example_word_game()
    example_data_serialization()
    example_frequency_analysis()
    example_suffix_trie()
    
    print("=" * 60)
    print("    所有示例运行完成！")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
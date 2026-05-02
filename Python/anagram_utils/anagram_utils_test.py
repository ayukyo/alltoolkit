"""
Anagram Utils 测试套件

覆盖变位词检测、生成、求解等功能的各种场景。
零外部依赖，使用 Python 标准库。
"""

import sys
import os

# 添加父目录到路径以导入模块
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from anagram_utils.mod import (
    normalize_text,
    get_char_count,
    is_anagram,
    find_anagrams,
    group_anagrams,
    generate_permutations,
    generate_anagrams,
    can_form_word,
    find_formable_words,
    anagram_distance,
    anagram_similarity,
    get_unique_chars,
    get_missing_chars,
    get_extra_chars,
    subtract_chars,
    add_chars,
    sort_chars,
    anagram_signature,
    count_anagram_pairs,
    longest_anagram_group,
    has_anagram_in_list,
    get_anagram_info,
    is_partial_anagram,
    find_all_formable_words,
    multiset_anagram_check,
    find_anagram_subset,
    suggest_anagram_words,
    AnagramSolver
)

# 测试计数器
test_count = 0
pass_count = 0
fail_count = 0


def test(name: str, condition: bool, expected=None, actual=None):
    """测试辅助函数"""
    global test_count, pass_count, fail_count
    test_count += 1
    
    if condition:
        pass_count += 1
        print(f"✓ {name}")
    else:
        fail_count += 1
        print(f"✗ {name}")
        if expected is not None and actual is not None:
            print(f"  预期: {expected}")
            print(f"  实际: {actual}")


def test_normalize_text():
    """测试文本规范化"""
    print("\n=== 测试 normalize_text ===")
    
    test("基本规范化", normalize_text("Listen") == "listen")
    test("移除空格", normalize_text("A gentleman") == "agentleman")
    test("移除标点", normalize_text("Hello, World!") == "helloworld")
    test("混合处理", normalize_text("  Test  123!  ") == "test123")
    test("空字符串", normalize_text("") == "")
    test("仅标点", normalize_text("!@#$%") == "")
    # Unicode 字母会被保留（isalnum 对 Unicode 字母返回 True）
    test("Unicode字符保留", normalize_text("你好世界") == "你好世界")


def test_get_char_count():
    """测试字符计数"""
    print("\n=== 测试 get_char_count ===")
    
    count = get_char_count("hello")
    test("基本计数", count['l'] == 2 and count['h'] == 1)
    
    count = get_char_count("AabB")
    test("大小写归一化", count['a'] == 2 and count['b'] == 2)
    
    count = get_char_count("Hello, World!")
    test("忽略标点", count.get(',', None) is None and count.get('!', None) is None)
    
    count = get_char_count("")
    test("空字符串", len(count) == 0)


def test_is_anagram():
    """测试变位词检测"""
    print("\n=== 测试 is_anagram ===")
    
    test("基本变位词", is_anagram("listen", "silent"))
    test("短语变位词", is_anagram("A gentleman", "Elegant man"))
    test("非变位词", not is_anagram("hello", "world"))
    test("不同长度", not is_anagram("abc", "abcd"))
    test("相同单词", is_anagram("test", "test"))
    
    # 严格模式
    test("严格模式 - 大小写不同", not is_anagram("Listen", "silent", strict=True))
    test("严格模式 - 完全相同", is_anagram("test", "test", strict=True))
    
    # 边界值
    test("空字符串", is_anagram("", ""))
    test("单字符", is_anagram("a", "a"))
    test("单字符不同", not is_anagram("a", "b"))
    
    # 经典变位词
    test("'rail safety' 和 'fairy tales'", 
         is_anagram("rail safety", "fairy tales"))
    test("'William Shakespeare' 和 'I am a weakish speller'", 
         is_anagram("William Shakespeare", "I am a weakish speller"))


def test_find_anagrams():
    """测试查找变位词"""
    print("\n=== 测试 find_anagrams ===")
    
    words = ["listen", "silent", "enlist", "tinsel", "hello", "world"]
    
    result = find_anagrams("listen", words)
    test("查找 listen 的变位词", 
         set(result) == {"silent", "enlist", "tinsel"})
    
    result = find_anagrams("hello", words)
    test("查找无变位词的单词", len(result) == 0)
    
    result = find_anagrams("abc", ["ABC", "bac", "cab"])
    test("大小写归一化", set(result) == {"bac", "cab"})
    
    result = find_anagrams("abc", ["ABC", "bac", "cab"], strict=True)
    test("严格模式 - 区分大小写", "bac" in result and "cab" in result)


def test_group_anagrams():
    """测试变位词分组"""
    print("\n=== 测试 group_anagrams ===")
    
    words = ["listen", "silent", "enlist", "hello", "world", "tinsel"]
    groups = group_anagrams(words)
    
    # 找到 listen 组
    listen_group = [g for g in groups if "listen" in g]
    test("listen 组包含变位词", 
         len(listen_group) == 1 and 
         set(listen_group[0]) == {"listen", "silent", "enlist", "tinsel"})
    
    test("hello 是独立组", any("hello" in g and len(g) == 1 for g in groups))
    
    # 空列表
    test("空列表", group_anagrams([]) == [])
    
    # 所有单词都是变位词
    words = ["abc", "bac", "cab"]
    groups = group_anagrams(words)
    test("所有单词都是变位词", len(groups) == 1 and len(groups[0]) == 3)


def test_generate_permutations():
    """测试排列生成"""
    print("\n=== 测试 generate_permutations ===")
    
    perms = generate_permutations("abc")
    test("abc 的所有排列", set(perms) == {"a", "b", "c", "ab", "ac", "ba", "bc", "ca", "cb", "abc", "acb", "bac", "bca", "cab", "cba"})
    
    perms = generate_permutations("aab")
    test("重复字符去重", "aab" in perms and "aba" in perms and "baa" in perms)
    
    # 限制长度
    perms = generate_permutations("abc", max_length=2)
    test("限制最大长度", all(len(p) <= 2 for p in perms))
    
    perms = generate_permutations("")
    test("空字符串", perms == [])


def test_generate_anagrams():
    """测试变位词生成"""
    print("\n=== 测试 generate_anagrams ===")
    
    anagrams = generate_anagrams("abc")
    test("abc 的变位词", set(anagrams) == {"abc", "acb", "bac", "bca", "cab", "cba"})
    
    anagrams = generate_anagrams("aab")
    test("重复字符去重", set(anagrams) == {"aab", "aba", "baa"})
    
    # 最小长度
    anagrams = generate_anagrams("abcd", min_length=3)
    test("最小长度限制", all(len(a) >= 3 for a in anagrams))
    
    # 计数验证
    anagrams = generate_anagrams("listen")
    test("6 字符排列数", len(anagrams) == 720)  # 6!
    
    anagrams = generate_anagrams("aa")
    test("重复字符", set(anagrams) == {"aa"})


def test_can_form_word():
    """测试字母组成检测"""
    print("\n=== 测试 can_form_word ===")
    
    test("可以组成", can_form_word("abcdef", "cab"))
    test("可以组成 - 相同字母", can_form_word("abc", "abc"))
    test("不可以组成 - 缺少字母", not can_form_word("abc", "abcd"))
    test("不可以组成 - 字母不足", not can_form_word("aab", "aaa"))
    test("可以组成 - 多余字母", can_form_word("abcdef", "cab"))
    test("空目标", can_form_word("abc", ""))
    test("空源", not can_form_word("", "a"))


def test_find_formable_words():
    """测试查找可组成单词"""
    print("\n=== 测试 find_formable_words ===")
    
    words = ["cab", "bad", "ace", "deed", "bead", "ab", "abcde"]
    result = find_formable_words("abcde", words)
    
    test("从 abcde 可组成的单词", 
         set(result) == {"cab", "bad", "ace", "bead", "ab", "abcde"})
    
    # 最小长度
    result = find_formable_words("abcde", words, min_length=3)
    test("最小长度限制", 
         set(result) == {"cab", "bad", "ace", "bead", "abcde"})


def test_anagram_distance():
    """测试变位距离"""
    print("\n=== 测试 anagram_distance ===")
    
    test("完全变位词距离为 0", anagram_distance("listen", "silent") == 0)
    
    dist = anagram_distance("listen", "list")
    test("部分重叠", dist == 2)  # e, n 多余
    
    dist = anagram_distance("abc", "def")
    test("完全不同", dist == 6)  # 3 + 3
    
    test("空字符串", anagram_distance("", "") == 0)
    test("一个空字符串", anagram_distance("abc", "") == 3)


def test_anagram_similarity():
    """测试变位相似度"""
    print("\n=== 测试 anagram_similarity ===")
    
    test("完全变位词相似度为 1", anagram_similarity("listen", "silent") == 1.0)
    
    sim = anagram_similarity("listen", "list")
    # listen 有 6 字符，list 有 4 字符，距离为 2 (e, n 多出)
    # 总字符数 = 6 + 4 = 10，相似度 = 1 - 2/10 = 0.8
    test("部分重叠相似度", abs(sim - 0.8) < 0.01)
    
    test("完全不同相似度为 0", anagram_similarity("abc", "def") == 0.0)
    test("空字符串相似度为 1", anagram_similarity("", "") == 1.0)


def test_get_unique_chars():
    """测试唯一字符获取"""
    print("\n=== 测试 get_unique_chars ===")
    
    test("基本字符集", get_unique_chars("hello") == {'h', 'e', 'l', 'o'})
    test("重复字符", get_unique_chars("aaa") == {'a'})
    test("空字符串", get_unique_chars("") == set())
    test("混合大小写", get_unique_chars("AaBb") == {'a', 'b'})


def test_get_missing_chars():
    """测试缺少字符获取"""
    print("\n=== 测试 get_missing_chars ===")
    
    missing = get_missing_chars("abc", "abcd")
    test("缺少 d", missing == {'d': 1} or dict(missing) == {'d': 1})
    
    missing = get_missing_chars("aabbc", "aabbcc")
    test("缺少 c", missing == {'c': 1} or dict(missing) == {'c': 1})
    
    missing = get_missing_chars("abc", "abc")
    test("不缺少", len(missing) == 0)


def test_get_extra_chars():
    """测试多余字符获取"""
    print("\n=== 测试 get_extra_chars ===")
    
    extra = get_extra_chars("abcde", "abc")
    test("多余 d 和 e", extra == {'d': 1, 'e': 1} or dict(extra) == {'d': 1, 'e': 1})
    
    extra = get_extra_chars("abc", "abc")
    test("不多余", len(extra) == 0)


def test_subtract_chars():
    """测试字符减法"""
    print("\n=== 测试 subtract_chars ===")
    
    result = subtract_chars("listen", "sil")
    test("减去 sil", set(result) == {'t', 'e', 'n'})
    
    result = subtract_chars("aabbbcc", "ab")
    test("减去 ab", "abbc" in result or set(result) == {'a', 'b', 'b', 'c'})
    
    result = subtract_chars("abc", "abc")
    test("减去全部", result == "")


def test_add_chars():
    """测试字符加法"""
    print("\n=== 测试 add_chars ===")
    
    test("添加字符", add_chars("abc", "de") == "abcde")
    test("添加空字符串", add_chars("abc", "") == "abc")
    test("两个空字符串", add_chars("", "") == "")


def test_sort_chars():
    """测试字符排序"""
    print("\n=== 测试 sort_chars ===")
    
    test("基本排序", sort_chars("listen") == "eilnst")
    test("已排序", sort_chars("abc") == "abc")
    test("逆序", sort_chars("cba") == "abc")
    test("重复字符", sort_chars("baba") == "aabb")


def test_anagram_signature():
    """测试变位词签名"""
    print("\n=== 测试 anagram_signature ===")
    
    sig1 = anagram_signature("listen")
    sig2 = anagram_signature("silent")
    test("变位词有相同签名", sig1 == sig2)
    
    sig3 = anagram_signature("hello")
    test("非变位词有不同签名", sig1 != sig3)


def test_count_anagram_pairs():
    """测试变位词对计数"""
    print("\n=== 测试 count_anagram_pairs ===")
    
    words = ["listen", "silent", "enlist", "hello", "world"]
    count = count_anagram_pairs(words)
    test("3 个变位词产生 3 对", count == 3)  # C(3,2) = 3
    
    words = ["a", "b", "c"]
    count = count_anagram_pairs(words)
    test("无变位词", count == 0)
    
    words = ["abc", "bac", "cab", "xyz", "zyx"]
    count = count_anagram_pairs(words)
    test("两组变位词", count == 4)  # C(3,2) + C(2,2) = 3 + 1 = 4


def test_longest_anagram_group():
    """测试最长变位词组"""
    print("\n=== 测试 longest_anagram_group ===")
    
    words = ["listen", "silent", "hello", "enlist", "tinsel", "world"]
    group = longest_anagram_group(words)
    test("最长组有 4 个单词", len(group) == 4 and "listen" in group)
    
    words = ["a", "b", "c"]
    group = longest_anagram_group(words)
    test("无变位词时返回单元素组", len(group) == 1)
    
    group = longest_anagram_group([])
    test("空列表", group == [])


def test_has_anagram_in_list():
    """测试列表中是否有变位词"""
    print("\n=== 测试 has_anagram_in_list ===")
    
    words = ["hello", "silent", "world"]
    test("存在变位词", has_anagram_in_list("listen", words))
    test("不存在变位词", not has_anagram_in_list("hello", words))


def test_get_anagram_info():
    """测试变位词信息获取"""
    print("\n=== 测试 get_anagram_info ===")
    
    info = get_anagram_info("listen")
    test("原始文本", info['original'] == "listen")
    test("规范化文本", info['normalized'] == "listen")
    test("长度", info['length'] == 6)
    test("唯一字符数", info['unique_chars'] == 6)  # listen 有 6 个不同字符
    test("签名", info['signature'] == "eilnst")
    test("非回文", not info['is_palindrome'])
    test("排列数", info['permutation_count'] == 720)  # 6!
    
    info = get_anagram_info("aab")
    test("重复字符排列数", info['permutation_count'] == 3)  # 3!/(2!) = 3


def test_is_partial_anagram():
    """测试部分变位词检测"""
    print("\n=== 测试 is_partial_anagram ===")
    
    test("完全变位词", is_partial_anagram("listen", "silent"))
    test("部分变位词", is_partial_anagram("listening", "silent"))
    test("不是部分变位词", not is_partial_anagram("list", "silent"))
    test("源包含目标", is_partial_anagram("abcd", "abc"))
    test("源不包含目标", not is_partial_anagram("abc", "abcd"))


def test_find_all_formable_words():
    """测试按长度分组的可组成单词"""
    print("\n=== 测试 find_all_formable_words ===")
    
    words = ["cab", "bad", "ace", "deed", "bead", "ab", "abcde"]
    result = find_all_formable_words("abcde", words)
    
    test("包含长度 2", 2 in result and "ab" in result[2])
    test("包含长度 3", 3 in result and set(result[3]) == {"cab", "bad", "ace"})
    test("不包含长度 4 (deed 需要 2 个 d)", 4 not in result or "deed" not in result[4])
    
    # 最大长度限制
    result = find_all_formable_words("abcde", words, max_length=3)
    test("最大长度限制", all(k <= 3 for k in result.keys()))


def test_multiset_anagram_check():
    """测试多字符串变位词检测"""
    print("\n=== 测试 multiset_anagram_check ===")
    
    test("多个变位词", multiset_anagram_check(["listen", "silent", "enlist"]))
    test("不是变位词", not multiset_anagram_check(["listen", "silent", "hello"]))
    test("单个字符串", multiset_anagram_check(["only"]))
    test("空列表", multiset_anagram_check([]))


def test_find_anagram_subset():
    """测试子集变位词计数"""
    print("\n=== 测试 find_anagram_subset ===")
    
    count = find_anagram_subset("abc", 2)
    test("从 abc 中选 2 个排列", count == 6)  # P(3,2) = 6
    
    count = find_anagram_subset("abc", 3)
    test("从 abc 中选 3 个排列", count == 6)  # P(3,3) = 6
    
    count = find_anagram_subset("aab", 2)
    test("从 aab 中选 2 个排列（去重）", count == 3)  # aa, ab, ba
    
    count = find_anagram_subset("abc", 4)
    test("超过长度", count == 0)


def test_suggest_anagram_words():
    """测试变位词建议"""
    print("\n=== 测试 suggest_anagram_words ===")
    
    words = ["cab", "bad", "ace", "deed", "bead"]
    suggestions = suggest_anagram_words("abcde", words, top_n=3)
    
    test("返回建议", len(suggestions) > 0)
    test("按长度排序", suggestions[0][1] >= suggestions[-1][1])
    test("bead 最长", suggestions[0][0] == "bead" and suggestions[0][1] == 4)


def test_anagram_solver():
    """测试 AnagramSolver 类"""
    print("\n=== 测试 AnagramSolver ===")
    
    words = ["listen", "silent", "enlist", "tinsel", "hello", "world"]
    solver = AnagramSolver(words)
    
    # 查找变位词
    anagrams = solver.find_anagrams("listen")
    test("查找变位词", set(anagrams) == {"silent", "enlist", "tinsel"})
    
    # 获取所有变位词组
    groups = solver.get_all_anagram_groups()
    test("变位词组数量", len(groups) == 1)
    
    # 获取指定长度的变位词组
    groups_6 = solver.get_all_anagrams_of_length(6)
    test("6 字符变位词组", len(groups_6) == 1)
    
    # 统计信息
    stats = solver.get_stats()
    test("总单词数", stats['total_words'] == 6)
    test("变位词组数", stats['anagram_groups_count'] == 1)
    
    # 添加单词
    solver.add_word("nestli")
    test("添加单词后", "nestli" in solver.find_anagrams("listen"))
    
    # 移除单词
    result = solver.remove_word("nestli")
    test("移除单词", result and "nestli" not in solver.find_anagrams("listen"))
    
    # 查找可组成单词
    formable = solver.find_formable_words("listen")
    test("从 listen 可组成的单词", "silent" in formable)


def test_edge_cases():
    """测试边界值"""
    print("\n=== 测试边界值 ===")
    
    # 空字符串
    test("空字符串是变位词", is_anagram("", ""))
    test("空字符串与非空", not is_anagram("", "a"))
    
    # 单字符
    test("单字符相同", is_anagram("a", "a"))
    test("单字符不同", not is_anagram("a", "b"))
    
    # 超长字符串
    long_str = "a" * 1000
    test("超长字符串", is_anagram(long_str, long_str))
    
    # Unicode
    test("Unicode 字符", is_anagram("你好", "好你"))
    
    # 数字
    test("数字变位词", is_anagram("123", "321"))
    
    # 混合
    test("字母数字混合", is_anagram("a1b2", "b2a1"))
    
    # 只有空格
    test("只有空格", is_anagram("   ", "   "))
    
    # 只有标点
    test("只有标点", is_anagram("!!!", "!!!"))


def test_performance():
    """性能测试"""
    print("\n=== 测试性能 ===")
    
    import time
    
    # 大量单词分组
    words = ["word" + str(i) for i in range(1000)]
    words.extend(["listen", "silent", "enlist", "tinsel"])  # 添加一些变位词
    
    start = time.time()
    groups = group_anagrams(words)
    elapsed = time.time() - start
    
    test("1000+ 单词分组 < 1 秒", elapsed < 1.0)
    
    # AnagramSolver 索引构建
    start = time.time()
    solver = AnagramSolver(words)
    elapsed = time.time() - start
    
    test("AnagramSolver 初始化 < 1 秒", elapsed < 1.0)
    
    # 查找变位词
    start = time.time()
    anagrams = solver.find_anagrams("listen")
    elapsed = time.time() - start
    
    test("查找变位词 < 0.01 秒", elapsed < 0.01)


def run_all_tests():
    """运行所有测试"""
    print("=" * 60)
    print("Anagram Utils 测试套件")
    print("=" * 60)
    
    test_normalize_text()
    test_get_char_count()
    test_is_anagram()
    test_find_anagrams()
    test_group_anagrams()
    test_generate_permutations()
    test_generate_anagrams()
    test_can_form_word()
    test_find_formable_words()
    test_anagram_distance()
    test_anagram_similarity()
    test_get_unique_chars()
    test_get_missing_chars()
    test_get_extra_chars()
    test_subtract_chars()
    test_add_chars()
    test_sort_chars()
    test_anagram_signature()
    test_count_anagram_pairs()
    test_longest_anagram_group()
    test_has_anagram_in_list()
    test_get_anagram_info()
    test_is_partial_anagram()
    test_find_all_formable_words()
    test_multiset_anagram_check()
    test_find_anagram_subset()
    test_suggest_anagram_words()
    test_anagram_solver()
    test_edge_cases()
    test_performance()
    
    print("\n" + "=" * 60)
    print(f"测试结果: {pass_count}/{test_count} 通过")
    print(f"通过率: {pass_count/test_count*100:.1f}%")
    
    if fail_count > 0:
        print(f"失败: {fail_count} 个测试")
        return False
    return True


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
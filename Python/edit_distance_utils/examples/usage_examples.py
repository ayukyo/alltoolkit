"""
edit_distance_utils 使用示例

展示各种编辑距离和字符串相似度算法的实际应用场景。
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    levenshtein_distance,
    damerau_levenshtein_distance,
    hamming_distance,
    jaro_similarity,
    jaro_winkler_similarity,
    lcs_length,
    lcs_string,
    normalized_levenshtein,
    similarity_ratio,
    fuzzy_match,
    spell_suggest,
    edit_operations,
    diff_ratio,
    soundex_distance,
    ngram_similarity,
    EditDistanceCalculator,
)


def example_levenshtein_basic():
    """Levenshtein 距离基础示例"""
    print("=" * 50)
    print("1. Levenshtein 距离基础")
    print("=" * 50)
    
    pairs = [
        ("kitten", "sitting"),
        ("saturday", "sunday"),
        ("algorithm", "altruistic"),
        ("hello", "hallo"),
        ("世界", "世界您好"),
    ]
    
    for s1, s2 in pairs:
        dist = levenshtein_distance(s1, s2)
        norm = normalized_levenshtein(s1, s2)
        print(f"  '{s1}' vs '{s2}'")
        print(f"    编辑距离: {dist}, 相似度: {norm:.2%}")


def example_damerau_levenshtein():
    """Damerau-Levenshtein 距离示例（支持字符交换）"""
    print("\n" + "=" * 50)
    print("2. Damerau-Levenshtein 距离（支持交换操作）")
    print("=" * 50)
    
    pairs = [
        ("ab", "ba"),  # 一次交换
        ("abc", "acb"),  # 一次交换
        ("ca", "abc"),
    ]
    
    for s1, s2 in pairs:
        lev = levenshtein_distance(s1, s2)
        dl = damerau_levenshtein_distance(s1, s2)
        print(f"  '{s1}' → '{s2}'")
        print(f"    Levenshtein: {lev}, Damerau-Levenshtein: {dl}")
        if dl < lev:
            print(f"    ⚡ 交换操作节省了 {lev - dl} 步！")


def example_hamming_distance():
    """Hamming 距离示例（等长字符串比较）"""
    print("\n" + "=" * 50)
    print("3. Hamming 距离（仅适用于等长字符串）")
    print("=" * 50)
    
    pairs = [
        ("karolin", "kathrin"),
        ("1011101", "1001001"),
        ("000000", "111111"),
    ]
    
    for s1, s2 in pairs:
        dist = hamming_distance(s1, s2)
        similarity = 1 - (dist / len(s1))
        print(f"  '{s1}' vs '{s2}'")
        print(f"    Hamming 距离: {dist}, 相似度: {similarity:.2%}")


def example_jaro_winkler():
    """Jaro-Winkler 相似度示例"""
    print("\n" + "=" * 50)
    print("4. Jaro-Winkler 相似度（擅长处理前缀相似）")
    print("=" * 50)
    
    pairs = [
        ("MARTHA", "MARHTA"),
        ("hello", "hallo"),
        ("docker", "docker-compose"),
        ("package", "packet"),
    ]
    
    for s1, s2 in pairs:
        jaro = jaro_similarity(s1, s2)
        jw = jaro_winkler_similarity(s1, s2)
        print(f"  '{s1}' vs '{s2}'")
        print(f"    Jaro: {jaro:.4f}, Jaro-Winkler: {jw:.4f}")


def example_lcs():
    """最长公共子序列示例"""
    print("\n" + "=" * 50)
    print("5. 最长公共子序列（LCS）")
    print("=" * 50)
    
    pairs = [
        ("ABCDGH", "AEDFHR"),
        ("AGGTAB", "GXTXAYB"),
        ("这是中文测试", "这是测试中文"),
    ]
    
    for s1, s2 in pairs:
        length = lcs_length(s1, s2)
        lcs = lcs_string(s1, s2)
        print(f"  '{s1}' vs '{s2}'")
        print(f"    LCS长度: {length}, LCS: '{lcs}'")


def example_fuzzy_match():
    """模糊匹配示例"""
    print("\n" + "=" * 50)
    print("6. 模糊匹配（搜索建议）")
    print("=" * 50)
    
    dictionary = [
        "apple", "application", "apply", "applet", "appliance",
        "approximate", "apparatus", "apparel", "appeal", "appear"
    ]
    
    queries = ["appl", "aple", "aplication"]
    
    for query in queries:
        print(f"\n  搜索: '{query}'")
        results = fuzzy_match(query, dictionary, threshold=0.7, limit=5)
        for word, score in results:
            print(f"    - {word}: {score:.2%}")


def example_spell_check():
    """拼写检查示例"""
    print("\n" + "=" * 50)
    print("7. 拼写建议")
    print("=" * 50)
    
    dictionary = [
        "hello", "help", "held", "halo", "hero",
        "helicopter", "helmet", "healthy", "heavy"
    ]
    
    typos = ["helo", "hllo", "hrllo", "hel"]
    
    for typo in typos:
        print(f"\n  拼写: '{typo}'")
        suggestions = spell_suggest(typo, dictionary, max_distance=2, limit=5)
        for word, dist in suggestions:
            print(f"    - {word} (距离: {dist})")


def example_edit_operations():
    """编辑操作序列示例"""
    print("\n" + "=" * 50)
    print("8. 编辑操作序列（可视化转换过程）")
    print("=" * 50)
    
    pairs = [
        ("kitten", "sitting"),
        ("hello", "hallo"),
    ]
    
    for s1, s2 in pairs:
        print(f"\n  '{s1}' → '{s2}':")
        ops = edit_operations(s1, s2)
        for op, pos, char in ops:
            if op == 'insert':
                print(f"    在位置 {pos} 插入 '{char}'")
            elif op == 'delete':
                print(f"    删除位置 {pos} 的字符")
            elif op == 'replace':
                print(f"    将位置 {pos} 替换为 '{char}'")
            else:
                print(f"    保持位置 {pos} 不变")


def example_soundex():
    """Soundex 语音编码示例"""
    print("\n" + "=" * 50)
    print("9. Soundex 语音相似度")
    print("=" * 50)
    
    groups = [
        ("Robert", "Rupert", "Rubin"),  # 都发音相似
        ("Smith", "Smythe", "Schmidt"),
        ("Catherine", "Kathryn"),
    ]
    
    for group in groups:
        print(f"\n  词组: {group}")
        for i, word1 in enumerate(group):
            for word2 in group[i+1:]:
                dist = soundex_distance(word1, word2)
                status = "相似" if dist == 0 else "不同"
                print(f"    '{word1}' vs '{word2}': {status}")


def example_ngram():
    """N-gram 相似度示例"""
    print("\n" + "=" * 50)
    print("10. N-gram 相似度")
    print("=" * 50)
    
    pairs = [
        ("hello", "hallo"),
        ("information", "informative"),
        ("testing", "teasing"),
    ]
    
    for s1, s2 in pairs:
        print(f"\n  '{s1}' vs '{s2}':")
        for n in [2, 3, 4]:
            sim = ngram_similarity(s1, s2, n=n)
            print(f"    {n}-gram: {sim:.2%}")


def example_calculator_class():
    """EditDistanceCalculator 类示例"""
    print("\n" + "=" * 50)
    print("11. EditDistanceCalculator 类（带缓存）")
    print("=" * 50)
    
    calc = EditDistanceCalculator(method='jaro_winkler')
    
    # 单次计算
    result = calc.similarity("hello", "hallo")
    print(f"  相似度: {result:.4f}")
    
    # 批量计算
    candidates = ["apple", "apply", "ape", "appeal", "app"]
    results = calc.batch_similarity("appel", candidates)
    
    print("\n  批量相似度计算:")
    for word, score in results:
        print(f"    - {word}: {score:.4f}")
    
    # 切换计算方法
    print("\n  使用 Levenshtein 方法:")
    calc2 = EditDistanceCalculator(method='levenshtein')
    for word, _ in results[:3]:
        score = calc2.similarity("appel", word)
        print(f"    - {word}: {score:.4f}")


def example_different_methods():
    """不同相似度方法对比"""
    print("\n" + "=" * 50)
    print("12. 不同相似度方法对比")
    print("=" * 50)
    
    methods = ['jaro_winkler', 'jaro', 'levenshtein', 'lcs']
    pairs = [
        ("hello", "hallo"),
        ("test", "testing"),
        ("apple", "appel"),
    ]
    
    for s1, s2 in pairs:
        print(f"\n  '{s1}' vs '{s2}':")
        for method in methods:
            score = similarity_ratio(s1, s2, method=method)
            print(f"    {method:15s}: {score:.4f}")


def example_real_world_autocomplete():
    """实际应用：自动补全"""
    print("\n" + "=" * 50)
    print("13. 实际应用：自动补全")
    print("=" * 50)
    
    commands = [
        "git status", "git commit", "git push", "git pull", "git clone",
        "git branch", "git checkout", "git merge", "git rebase", "git log",
        "npm install", "npm update", "npm run", "npm test", "npm build",
        "docker build", "docker run", "docker ps", "docker stop", "docker exec"
    ]
    
    query = "git p"
    print(f"\n  输入: '{query}'")
    results = fuzzy_match(query, commands, threshold=0.3, limit=5, method='jaro_winkler')
    print("  建议:")
    for cmd, score in results:
        print(f"    - {cmd} (相似度: {score:.2%})")


def example_real_world_deduplication():
    """实际应用：数据去重"""
    print("\n" + "=" * 50)
    print("14. 实际应用：数据去重")
    print("=" * 50)
    
    names = [
        "张三", "张三丰", "张山", "李四", "李思",
        "王五", "王武", "赵六", "赵柳"
    ]
    
    print("\n  可能重复的记录:")
    for i, name1 in enumerate(names):
        for name2 in names[i+1:]:
            sim = similarity_ratio(name1, name2, method='jaro_winkler')
            if sim > 0.85:  # 高相似度阈值
                print(f"    '{name1}' ↔ '{name2}': {sim:.2%}")


if __name__ == '__main__':
    example_levenshtein_basic()
    example_damerau_levenshtein()
    example_hamming_distance()
    example_jaro_winkler()
    example_lcs()
    example_fuzzy_match()
    example_spell_check()
    example_edit_operations()
    example_soundex()
    example_ngram()
    example_calculator_class()
    example_different_methods()
    example_real_world_autocomplete()
    example_real_world_deduplication()
    
    print("\n" + "=" * 50)
    print("所有示例执行完成！")
    print("=" * 50)
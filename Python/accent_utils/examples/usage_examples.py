"""
Accent Utils 使用示例

展示文本变音符号处理工具的各种用法。
"""

from mod import (
    remove_accents,
    normalize_text,
    has_accents,
    count_accents,
    get_accent_positions,
    find_accented_words,
    compare_accent_insensitive,
    accent_insensitive_search,
    transliterate_to_ascii,
    detect_language_from_accents,
    AccentNormalizer,
)


def print_section(title: str):
    """打印分隔线"""
    print(f"\n{'=' * 60}")
    print(f"  {title}")
    print('=' * 60)


def demo_basic_accent_removal():
    """演示基本的变音符号移除"""
    print_section("基本变音符号移除")
    
    examples = [
        "café",
        "résumé",
        "naïve",
        "über",
        "façade",
        "coöperate",
        "über",
        "jalapeño",
        "señor",
        "Año Nuevo",
    ]
    
    print("\n原始单词 -> 移除变音符号后:")
    for word in examples:
        result = remove_accents(word)
        print(f"  {word:15} -> {result}")


def demo_language_specific():
    """演示特定语言的处理"""
    print_section("特定语言处理")
    
    # 德语
    print("\n德语处理:")
    german_words = ["über", "Äpfel", "Öffnung", "groß", "Müller"]
    for word in german_words:
        result = remove_accents(word, language='german')
        print(f"  {word:15} -> {result}")
    
    # 法语
    print("\n法语处理:")
    french_words = ["cœur", "œuvre", "sœur"]
    for word in french_words:
        result = remove_accents(word, language='french')
        print(f"  {word:15} -> {result}")
    
    # 土耳其语
    print("\n土耳其语处理:")
    turkish_words = ["İstanbul", "Diyarbakır"]
    for word in turkish_words:
        result = remove_accents(word, language='turkish')
        print(f"  {word:15} -> {result}")


def demo_text_normalization():
    """演示文本规范化"""
    print_section("文本规范化")
    
    texts = [
        "Café au Lait",
        "  Multiple   Spaces  ",
        "Hello, World!",
        "Résumé for café",
        "HELLO WORLD",
    ]
    
    print("\n规范化选项:")
    print("  - lowercase=True")
    print("  - remove_accents_flag=True")
    print("  - remove_punctuation=True")
    print("  - collapse_whitespace=True")
    
    print("\n原始文本 -> 规范化后:")
    for text in texts:
        result = normalize_text(
            text,
            lowercase=True,
            remove_accents_flag=True,
            remove_punctuation=True,
            collapse_whitespace=True
        )
        print(f"  '{text}' -> '{result}'")


def demo_accent_detection():
    """演示变音符号检测"""
    print_section("变音符号检测")
    
    print("\n检测文本是否包含变音符号:")
    texts = ["café", "cafe", "résumé", "resume", "你好"]
    for text in texts:
        has = has_accents(text)
        print(f"  '{text}': {'有变音符号' if has else '无变音符号'}")
    
    print("\n统计变音符号数量:")
    count_examples = ["café", "résumé", "naïve", "cafe"]
    for text in count_examples:
        count = count_accents(text)
        print(f"  '{text}': {count} 个变音符号")


def demo_accent_positions():
    """演示获取变音符号位置"""
    print_section("变音符号位置信息")
    
    texts = ["café", "résumé", "naïve"]
    
    for text in texts:
        positions = get_accent_positions(text)
        print(f"\n'{text}' 中的变音符号位置:")
        for pos, orig, base in positions:
            print(f"  位置 {pos}: '{orig}' -> 基字符 '{base}'")


def demo_find_accented_words():
    """演示查找带变音符号的单词"""
    print_section("查找带变音符号的单词")
    
    texts = [
        "The café has a résumé for the naïve employee",
        "This sentence has no accented characters",
        "São Paulo is in Brazil, and Zürich is in Switzerland",
    ]
    
    for text in texts:
        words = find_accented_words(text)
        print(f"\n文本: '{text}'")
        if words:
            print(f"  带变音符号的单词: {', '.join(words)}")
        else:
            print("  无带变音符号的单词")


def demo_accent_insensitive_compare():
    """演示忽略变音符号的比较"""
    print_section("忽略变音符号比较")
    
    pairs = [
        ("café", "cafe"),
        ("résumé", "resume"),
        ("über", "uber"),
        ("CAFÉ", "cafe"),
        ("naïve", "naive"),
    ]
    
    print("\n比较结果 (case_insensitive=True):")
    for text1, text2 in pairs:
        result = compare_accent_insensitive(text1, text2, case_insensitive=True)
        print(f"  '{text1}' == '{text2}': {result}")


def demo_accent_insensitive_search():
    """演示忽略变音符号的搜索"""
    print_section("忽略变音符号搜索")
    
    text = "I visited a café in São Paulo, then went to another Café in Zürich"
    query = "cafe"
    
    print(f"\n文本: '{text}'")
    print(f"搜索词: '{query}'")
    
    results = accent_insensitive_search(text, query, case_insensitive=True)
    
    print(f"\n找到 {len(results)} 个匹配:")
    for start, end, matched in results:
        print(f"  位置 {start}-{end}: '{matched}'")


def demo_transliterate_to_ascii():
    """演示音译为 ASCII"""
    print_section("音译为 ASCII")
    
    texts = [
        "café",
        "résumé",
        "über",
        "你好世界",
        "Hello café 你好",
    ]
    
    print("\n原始文本 -> ASCII 文本:")
    for text in texts:
        result = transliterate_to_ascii(text, language='german' if 'ü' in text else None)
        print(f"  '{text}' -> '{result}'")


def demo_language_detection():
    """演示语言检测"""
    print_section("根据变音符号检测语言")
    
    texts = [
        "über",
        "café",
        "año",
        "pão",
        "İstanbul",
        "groß",
        "naïve",
        "Ålesund",
        "cœur",
    ]
    
    print("\n文本 -> 可能的语言:")
    for text in texts:
        langs = detect_language_from_accents(text)
        lang_str = ', '.join(langs) if langs else '无法确定'
        print(f"  '{text}': {lang_str}")


def demo_normalizer_class():
    """演示 AccentNormalizer 类"""
    print_section("AccentNormalizer 类")
    
    # 创建德语规范化器
    print("\n德语规范化器:")
    german_normalizer = AccentNormalizer(language='german', lowercase=True)
    words = ["Über", "Äpfel", "groß"]
    for word in words:
        result = german_normalizer.normalize(word)
        print(f"  '{word}' -> '{result}'")
    
    # 使用规范化器比较
    print("\n使用规范化器比较:")
    normalizer = AccentNormalizer(lowercase=True)
    pairs = [("CAFÉ", "cafe"), ("Résumé", "resume")]
    for text1, text2 in pairs:
        result = normalizer.compare(text1, text2)
        print(f"  '{text1}' == '{text2}': {result}")
    
    # 使用规范化器搜索
    print("\n使用规范化器搜索:")
    text = "The Café has a résumé"
    query = "cafe"
    results = normalizer.search(text, query)
    print(f"  文本: '{text}'")
    print(f"  搜索 '{query}': 找到 {len(results)} 个匹配")


def demo_practical_use_cases():
    """演示实际应用场景"""
    print_section("实际应用场景")
    
    # 场景1：数据库搜索
    print("\n场景1: 数据库搜索优化")
    print("  用户输入: 'cafe'")
    print("  可以匹配: 'café', 'cafe', 'CAFÉ' 等")
    
    # 场景2：用户名验证
    print("\n场景2: 用户名唯一性检查")
    username1 = "café_lover"
    username2 = "cafe_lover"
    is_same = compare_accent_insensitive(username1, username2)
    print(f"  '{username1}' 和 '{username2}' 是否冲突: {is_same}")
    
    # 场景3：文本索引
    print("\n场景3: 创建搜索索引")
    documents = ["Café menu", "Resume tips", "Façade design"]
    print("  原始文档:")
    for doc in documents:
        normalized = normalize_text(doc, remove_punctuation=True)
        print(f"    '{doc}' -> 索引键: '{normalized}'")
    
    # 场景4：国际化搜索
    print("\n场景4: 国际化搜索")
    products = [
        ("Bière française", 15.99),
        ("Fromage allemand", 12.50),
        ("Café italien", 8.99),
    ]
    query = "cafe"
    print(f"  搜索 '{query}':")
    for name, price in products:
        if compare_accent_insensitive(name, query, case_insensitive=False):
            print(f"    找到: {name} - ${price}")


def main():
    """运行所有示例"""
    print("\n" + "=" * 60)
    print("  Accent Utils - 文本变音符号处理工具")
    print("  使用示例")
    print("=" * 60)
    
    demo_basic_accent_removal()
    demo_language_specific()
    demo_text_normalization()
    demo_accent_detection()
    demo_accent_positions()
    demo_find_accented_words()
    demo_accent_insensitive_compare()
    demo_accent_insensitive_search()
    demo_transliterate_to_ascii()
    demo_language_detection()
    demo_normalizer_class()
    demo_practical_use_cases()
    
    print("\n" + "=" * 60)
    print("  示例演示完成")
    print("=" * 60 + "\n")


if __name__ == '__main__':
    main()
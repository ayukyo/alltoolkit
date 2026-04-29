"""
Transliteration Utils 使用示例

展示文字系统音译转换的各种用法。
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from transliteration_utils.mod import (
    TransliterationUtils,
    cyrillic_to_latin, latin_to_cyrillic, greek_to_latin,
    hiragana_to_romaji, katakana_to_romaji, japanese_to_romaji,
    hangul_to_romaji, arabic_to_latin, thai_to_latin, hebrew_to_latin,
    detect_script, auto_transliterate, transliterate
)


def separator(title):
    """打印分隔线和标题"""
    print(f"\n{'='*60}")
    print(f" {title}")
    print('='*60)


def demo_cyrillic():
    """演示西里尔字母转换"""
    separator("西里尔字母 (俄语) ↔ 拉丁字母")
    
    # 俄语 → 拉丁
    russian_words = [
        "Привет",      # 你好
        "мир",         # 世界
        "Спасибо",     # 谢谢
        "До свидания", # 再见
        "Россия",      # 俄罗斯
        "Москва",      # 莫斯科
        "Добро пожаловать",  # 欢迎
    ]
    
    print("\n俄语 → 拉丁:")
    for word in russian_words:
        latin = cyrillic_to_latin(word)
        print(f"  {word:20s} → {latin}")
    
    # 拉丁 → 俄语
    print("\n拉丁 → 俄语:")
    latin_words = ["Privet", "mir", "Spasibo", "Moskva"]
    for word in latin_words:
        cyrillic = latin_to_cyrillic(word)
        print(f"  {word:20s} → {cyrillic}")
    
    # 往返转换
    print("\n往返转换测试:")
    original = "Привет"
    to_latin = cyrillic_to_latin(original)
    back = latin_to_cyrillic(to_latin)
    print(f"  原文: {original}")
    print(f"  → 拉丁: {to_latin}")
    print(f"  → 西里尔: {back}")


def demo_greek():
    """演示希腊字母转换"""
    separator("希腊字母 → 拉丁字母")
    
    greek_words = [
        "Γειά",      # 你好
        "σου",       # 你的
        "κόσμε",     # 世界
        "λόγος",     # 词/理性
        "φιλοσοφία", # 哲学
        "Αθήνα",     # 雅典
        "Ελλάδα",    # 希腊
    ]
    
    print("\n希腊语 → 拉丁:")
    for word in greek_words:
        latin = greek_to_latin(word)
        print(f"  {word:15s} → {latin}")
    
    # 希腊字母表
    print("\n希腊字母表:")
    greek_alphabet = "ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩ"
    latin_equivalents = greek_to_latin(greek_alphabet)
    print(f"  大写: {greek_alphabet}")
    print(f"  拉丁: {latin_equivalents}")


def demo_japanese():
    """演示日语假名转换"""
    separator("日语假名 → 罗马音")
    
    # 平假名
    separator("平假名 → 罗马音")
    hiragana_words = [
        "こんにちは",    # 你好
        "ありがとう",    # 谢谢
        "さようなら",    # 再见
        "おはよう",      # 早上好
        "すみません",    # 对不起
        "がっこう",      # 学校 (含促音)
        "きょうと",      # 京都 (含拗音)
    ]
    
    print("\n平假名 → 罗马音:")
    for word in hiragana_words:
        romaji = hiragana_to_romaji(word)
        print(f"  {word:15s} → {romaji}")
    
    # 片假名
    separator("片假名 → 罗马音")
    katakana_words = [
        "コンニチハ",    # 你好
        "アリガトウ",    # 谢谢
        "サヨナラ",      # 再见
        "コーヒー",      # 咖啡
        "コンピューター", # 电脑
        "アイスクリーム", # 冰淇淋
    ]
    
    print("\n片假名 → 罗马音:")
    for word in katakana_words:
        romaji = katakana_to_romaji(word)
        print(f"  {word:15s} → {romaji}")
    
    # 混合假名
    separator("混合假名 → 罗马音")
    mixed = "こんにちは、アリガトウ"
    print(f"\n混合文本: {mixed}")
    print(f"罗马音:   {japanese_to_romaji(mixed)}")


def demo_korean():
    """演示韩语转换"""
    separator("韩语谚文 → 罗马音")
    
    korean_words = [
        "안녕하세요",   # 你好
        "감사합니다",   # 谢谢
        "사랑",        # 爱
        "한국",        # 韩国
        "서울",        # 首尔
        "김치",        # 泡菜
        "불고기",      # 烤肉
        "반갑습니다",  # 很高兴见到你
    ]
    
    print("\n韩语 → 罗马音:")
    for word in korean_words:
        romaji = hangul_to_romaji(word)
        print(f"  {word:15s} → {romaji}")


def demo_arabic():
    """演示阿拉伯语转换"""
    separator("阿拉伯字母 → 拉丁字母")
    
    arabic_words = [
        "مرحبا",      # 你好
        "شكرا",       # 谢谢
        "سلام",       # 和平
        "عربي",       # 阿拉伯
        "كتاب",       # 书
        "مصر",        # 埃及
    ]
    
    print("\n阿拉伯语 → 拉丁:")
    for word in arabic_words:
        latin = arabic_to_latin(word)
        print(f"  {word:15s} → {latin}")


def demo_thai():
    """演示泰语转换"""
    separator("泰语 → 拉丁字母")
    
    thai_words = [
        "สวัสดี",     # 你好
        "ขอบคุณ",    # 谷歌
        "ไทย",       # 泰国
        "กรุงเทพ",   # 曼谷
    ]
    
    print("\n泰语 → 拉丁:")
    for word in thai_words:
        latin = thai_to_latin(word)
        print(f"  {word:15s} → {latin}")


def demo_hebrew():
    """演示希伯来语转换"""
    separator("希伯来字母 → 拉丁字母")
    
    hebrew_words = [
        "שלום",       # 和平/你好
        "תודה",      # 谢谢
        "ישראל",     # 以色列
        "ירושלים",   # 耶路撒冷
    ]
    
    print("\n希伯来语 → 拉丁:")
    for word in hebrew_words:
        latin = hebrew_to_latin(word)
        print(f"  {word:15s} → {latin}")


def demo_detection():
    """演示文字系统自动检测"""
    separator("文字系统自动检测")
    
    test_texts = [
        ("Привет мир", "俄语"),
        ("Γειά σου", "希腊语"),
        ("こんにちは世界", "日语 (平假名)"),
        ("コンニチハ", "日语 (片假名)"),
        ("안녕하세요", "韩语"),
        ("مرحبا بالعالم", "阿拉伯语"),
        ("สวัสดี", "泰语"),
        ("שלום עולם", "希伯来语"),
        ("Hello World", "拉丁字母 (英语)"),
    ]
    
    print("\n自动检测文字系统:")
    for text, description in test_texts:
        script = detect_script(text)
        print(f"  {text:20s} ({description:15s}) → {script}")


def demo_auto_transliterate():
    """演示自动转换"""
    separator("自动转换")
    
    test_texts = [
        "Привет",
        "Γειά σου",
        "こんにちは",
        "안녕하세요",
        "مرحبا",
        "שלום",
    ]
    
    print("\n自动检测并转换:")
    for text in test_texts:
        result, script = auto_transliterate(text)
        print(f"  {text:15s} [{script:10s}] → {result}")


def demo_specified_transliteration():
    """演示指定文字系统转换"""
    separator("指定文字系统转换")
    
    # 日语平假名
    print("\n指定平假名转换:")
    text = "ありがとう"
    result = transliterate(text, "hiragana", "latin")
    print(f"  {text} → {result}")
    
    # 日语片假名
    print("\n指定片假名转换:")
    text = "アリガトウ"
    result = transliterate(text, "katakana", "latin")
    print(f"  {text} → {result}")
    
    # 日语混合
    print("\n指定日语转换 (混合):")
    text = "こんにちはアリガトウ"
    result = transliterate(text, "japanese", "latin")
    print(f"  {text} → {result}")


def demo_supported_scripts():
    """演示获取支持的文字系统"""
    separator("支持的文字系统")
    
    scripts = TransliterationUtils.get_supported_scripts()
    print("\n支持的文字系统:")
    for i, script in enumerate(scripts, 1):
        print(f"  {i:2d}. {script}")


def demo_practical_usage():
    """演示实际应用场景"""
    separator("实际应用场景")
    
    # 1. 处理国际化用户名
    print("\n1. 处理国际化用户名:")
    usernames = [
        "Иван_Петров",
        "田中太郎",
        "김철수",
        "محمد_علي",
    ]
    for username in usernames:
        result, script = auto_transliterate(username)
        print(f"  {username:20s} → {result} ({script})")
    
    # 2. 搜索关键词转换
    print("\n2. 搜索关键词转换:")
    search_terms = ["Москва", "Αθήνα", "東京", "서울"]
    for term in search_terms:
        result, script = auto_transliterate(term)
        print(f"  搜索 '{term}' ({script}) → 关键词: '{result}'")
    
    # 3. 多语言支持
    print("\n3. 多语言消息转换:")
    messages = {
        "ru": "Привет! Добро пожаловать!",
        "el": "Γειά! Καλώς ήρθες!",
        "ja": "こんにちは！ようこそ！",
        "ko": "안녕하세요! 환영합니다!",
    }
    for lang, msg in messages.items():
        result, script = auto_transliterate(msg)
        print(f"  [{lang}] {msg}")
        print(f"        → {result}")


def main():
    """主函数"""
    print("=" * 60)
    print(" Transliteration Utils - 文字系统音译转换工具演示")
    print(" 支持多种文字系统: 西里尔、希腊、日语、韩语、阿拉伯、泰语、希伯来")
    print("=" * 60)
    
    demo_cyrillic()
    demo_greek()
    demo_japanese()
    demo_korean()
    demo_arabic()
    demo_thai()
    demo_hebrew()
    demo_detection()
    demo_auto_transliterate()
    demo_specified_transliteration()
    demo_supported_scripts()
    demo_practical_usage()
    
    print("\n" + "=" * 60)
    print(" 演示完成!")
    print("=" * 60)


if __name__ == "__main__":
    main()
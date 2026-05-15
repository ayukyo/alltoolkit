"""
Unicode Utilities 使用示例

展示各种 Unicode 字符处理功能
"""

from mod import (
    get_char_info,
    is_emoji,
    is_zero_width,
    contains_emoji,
    contains_zero_width,
    remove_zero_width,
    get_all_emojis,
    normalize_text,
    get_string_stats,
    codepoint_to_char,
    char_to_codepoint,
    string_to_codepoints,
    codepoints_to_string,
    hex_to_char,
    char_to_hex,
    is_valid_unicode,
    get_chars_in_range,
    get_chars_by_category,
    get_name,
    get_chars_by_name,
    detect_encoding,
    strip_invisible,
    is_printable,
    is_rtl,
    strip_diacritics,
    get_unicode_version,
    info,
    search,
    stats,
)


def example_char_info():
    """字符信息查询示例"""
    print("=" * 60)
    print("字符信息查询示例")
    print("=" * 60)
    
    # ASCII 字母
    print("\n1. ASCII 字母 'A':")
    char_info = get_char_info('A')
    print(f"  字符: {char_info.char}")
    print(f"  码点: {char_info.codepoint} ({char_info.hex_code})")
    print(f"  名称: {char_info.name}")
    print(f"  分类: {char_info.category_name}")
    print(f"  脚本: {char_info.script}")
    print(f"  是字母: {char_info.is_letter}")
    print(f"  大写: {char_info.uppercase}")
    print(f"  小写: {char_info.lowercase}")
    
    # 中文字符
    print("\n2. 中文字符 '中':")
    char_info = get_char_info('中')
    print(f"  字符: {char_info.char}")
    print(f"  码点: {char_info.codepoint} ({char_info.hex_code})")
    print(f"  名称: {char_info.name}")
    print(f"  分类: {char_info.category_name}")
    print(f"  脚本: {char_info.script}")
    print(f"  Unicode 块: {char_info.block}")
    
    # 表情符号
    print("\n3. 表情符号 '😀':")
    char_info = get_char_info('😀')
    print(f"  字符: {char_info.char}")
    print(f"  码点: {char_info.codepoint} ({char_info.hex_code})")
    print(f"  名称: {char_info.name}")
    print(f"  是表情: {char_info.is_emoji}")
    print(f"  Unicode 版本: {get_unicode_version('😀')}")
    
    # 数字字符
    print("\n4. 数字字符 '5':")
    char_info = get_char_info('5')
    print(f"  字符: {char_info.char}")
    print(f"  分类: {char_info.category_name}")
    print(f"  是数字: {char_info.is_digit}")
    print(f"  数值: {char_info.numeric_value}")


def example_emoji_detection():
    """表情符号检测示例"""
    print("\n" + "=" * 60)
    print("表情符号检测示例")
    print("=" * 60)
    
    # 检测单个表情
    print("\n1. 检测单个字符:")
    print(f"  '😀' 是表情: {is_emoji('😀')}")
    print(f"  'A' 是表情: {is_emoji('A')}")
    print(f"  '❤' 是表情: {is_emoji('❤')}")
    
    # 检测字符串中的表情
    text = "Hello 😃 World! 🌍🔥"
    print(f"\n2. 检测字符串包含表情:")
    print(f"  文本: '{text}'")
    print(f"  包含表情: {contains_emoji(text)}")
    
    # 获取所有表情
    emojis = get_all_emojis(text)
    print(f"\n3. 获取所有表情:")
    print(f"  表情列表: {emojis}")


def example_zero_width():
    """零宽字符示例"""
    print("\n" + "=" * 60)
    print("零宽字符示例")
    print("=" * 60)
    
    # 零宽字符检测
    print("\n1. 零宽字符类型:")
    zw_chars = [
        ('U+200B', 'Zero Width Space'),
        ('U+200C', 'Zero Width Non-Joiner'),
        ('U+200D', 'Zero Width Joiner'),
        ('U+FEFF', 'Zero Width No-Break Space (BOM)'),
    ]
    for code, name in zw_chars:
        char = hex_to_char(code)
        print(f"  {code} ({name}): is_zero_width={is_zero_width(char)}")
    
    # 隐藏字符检测
    text = "Hello\u200B\u200CWorld"
    print(f"\n2. 字符串 '{text}' (包含隐藏零宽字符):")
    print(f"  表观长度: {len(text)}")
    print(f"  包含零宽字符: {contains_zero_width(text)}")
    
    # 移除零宽字符
    clean_text = remove_zero_width(text)
    print(f"\n3. 清理后:")
    print(f"  清理后文本: '{clean_text}'")
    print(f"  清理后长度: {len(clean_text)}")


def example_normalization():
    """Unicode 规范化示例"""
    print("\n" + "=" * 60)
    print("Unicode 规范化示例")
    print("=" * 60)
    
    # 组合字符 vs 预组合字符
    text1 = 'é'  # 预组合 (U+00E9)
    text2 = 'e\u0301'  # 组合 (e + U+0301 组合重音)
    
    print(f"\n1. 同一字符的不同表示:")
    print(f"  预组合 'é': 码点 = {string_to_codepoints(text1)}")
    print(f"  组合 'e' + 重音: 码点 = {string_to_codepoints(text2)}")
    print(f"  视觉相同: {text1 == text2} (直接比较)")
    
    # NFC 规范化
    nfc1 = normalize_text(text1, 'NFC')
    nfc2 = normalize_text(text2, 'NFC')
    print(f"\n2. NFC 规范化后:")
    print(f"  nfc1 码点: {string_to_codepoints(nfc1)}")
    print(f"  nfc2 码点: {string_to_codepoints(nfc2)}")
    print(f"  规范化后相同: {nfc1 == nfc2}")
    
    # NFD 规范化
    nfd1 = normalize_text(text1, 'NFD')
    print(f"\n3. NFD 规范化 (分解):")
    print(f"  'é' NFD 后长度: {len(nfd1)}")
    print(f"  码点: {string_to_codepoints(nfd1)}")


def example_string_stats():
    """字符串统计示例"""
    print("\n" + "=" * 60)
    print("字符串统计示例")
    print("=" * 60)
    
    # 多语言文本
    text = "Hello 你好 مرحبا 123 😃🌍"
    print(f"\n1. 多语言文本分析:")
    print(f"  文本: '{text}'")
    
    s = get_string_stats(text)
    print(f"\n  基本统计:")
    print(f"    总长度: {s['length']}")
    print(f"    字符数: {s['codepoints']}")
    print(f"    唯一字符: {s['unique_chars']}")
    print(f"    UTF-8 字节数: {s['byte_length_utf8']}")
    
    print(f"\n  分类统计:")
    print(f"    字母: {s['letters']}")
    print(f"    数字: {s['digits']}")
    print(f"    标点: {s['punctuation']}")
    print(f"    符号: {s['symbols']}")
    print(f"    空白: {s['whitespace']}")
    print(f"    表情: {s['emoji_count']}")
    
    print(f"\n  脚本分布:")
    for script, count in sorted(s['scripts'].items(), key=lambda x: -x[1]):
        if count > 0:
            print(f"    {script}: {count}")


def example_codepoint_conversion():
    """码点转换示例"""
    print("\n" + "=" * 60)
    print("码点转换示例")
    print("=" * 60)
    
    print("\n1. 字符 → 码点:")
    print(f"  'A' → {char_to_codepoint('A')} ({char_to_hex('A')})")
    print(f"  '中' → {char_to_codepoint('中')} ({char_to_hex('中')})")
    print(f"  '😀' → {char_to_codepoint('😀')} ({char_to_hex('😀')})")
    
    print("\n2. 码点 → 字符:")
    print(f"  65 → '{codepoint_to_char(65)}'")
    print(f"  20013 → '{codepoint_to_char(20013)}'")
    print(f"  128512 → '{codepoint_to_char(128512)}'")
    
    print("\n3. 十六进制 → 字符:")
    print(f"  'U+0041' → '{hex_to_char('U+0041')}'")
    print(f"  '1F600' → '{hex_to_char('1F600')}'")
    
    print("\n4. 字符串 ↔ 码点列表:")
    text = "ABC"
    codepoints = string_to_codepoints(text)
    print(f"  '{text}' → {codepoints}")
    restored = codepoints_to_string(codepoints)
    print(f"  {codepoints} → '{restored}'")


def example_unicode_search():
    """Unicode 字符搜索示例"""
    print("\n" + "=" * 60)
    print("Unicode 字符搜索示例")
    print("=" * 60)
    
    print("\n1. 搜索 'HEART' 相关字符:")
    results = get_chars_by_name('HEART')
    for char, name in results[:10]:  # 只显示前10个
        print(f"  {char} ({char_to_hex(char)}) - {name}")
    
    print("\n2. 搜索 'STAR' 相关字符:")
    results = get_chars_by_name('STAR')
    for char, name in results[:10]:
        print(f"  {char} ({char_to_hex(char)}) - {name}")
    
    print("\n3. 搜索 'SNOW' 相关字符:")
    results = get_chars_by_name('SNOW')
    for char, name in results[:5]:
        print(f"  {char} ({char_to_hex(char)}) - {name}")


def example_encoding_detection():
    """编码分布检测示例"""
    print("\n" + "=" * 60)
    print("编码分布检测示例")
    print("=" * 60)
    
    texts = [
        "Hello World",  # 纯 ASCII
        "你好世界",  # 纯中文
        "مرحبا بالعالم",  # 阿拉伯语
        "Hello 你好 😃",  # 混合
    ]
    
    for text in texts:
        print(f"\n文本: '{text}'")
        encoding = detect_encoding(text)
        for enc, count in sorted(encoding.items(), key=lambda x: -x[1]):
            if count > 0:
                print(f"  {enc}: {count}")


def example_diacritics():
    """变音符号处理示例"""
    print("\n" + "=" * 60)
    print("变音符号处理示例")
    print("=" * 60)
    
    words = [
        'café',  # 法语
        'München',  # 德语
        'José',  # 西班牙语
        'naïve',  # 英语（外来词）
        'Åre',  # 瑞典语
    ]
    
    print("\n移除变音符号:")
    for word in words:
        stripped = strip_diacritics(word)
        print(f"  {word} → {stripped}")


def example_rtl_detection():
    """RTL 文本检测示例"""
    print("\n" + "=" * 60)
    print("RTL 文本检测示例")
    print("=" * 60)
    
    texts = [
        ("Hello World", "英语"),
        ("你好世界", "中文"),
        ("مرحبا بالعالم", "阿拉伯语"),
        ("שלום עולם", "希伯来语"),
        ("Hello مرحبا", "混合"),
    ]
    
    print("\nRTL 检测:")
    for text, lang in texts:
        rtl = is_rtl(text)
        print(f"  '{text}' ({lang}): RTL={rtl}")


def example_unicode_ranges():
    """Unicode 范围示例"""
    print("\n" + "=" * 60)
    print("Unicode 范围示例")
    print("=" * 60)
    
    # ASCII 范围
    print("\n1. ASCII 可见字符 (33-126):")
    chars = get_chars_in_range(33, 126)
    print(f"  字符数: {len(chars)}")
    print(f"  范围: {chars}")
    
    # 希腊字母
    print("\n2. 希腊字母部分 (0x0391-0x03A9):")
    chars = get_chars_in_range(0x0391, 0x03A9)
    print(f"  字符: {chars}")
    
    # 日文平假名开头
    print("\n3. 日文平假名开头 (0x3041-0x304F):")
    chars = get_chars_in_range(0x3041, 0x304F)
    print(f"  字符: {chars}")


def example_invisible_chars():
    """不可见字符处理示例"""
    print("\n" + "=" * 60)
    print("不可见字符处理示例")
    print("=" * 60)
    
    # 包含不可见字符的文本
    text = "Hello\u0000World\u200B!\t\n"
    print(f"\n1. 包含不可见字符的文本:")
    print(f"  原文本长度: {len(text)}")
    print(f"  包含零宽字符: {contains_zero_width(text)}")
    
    # 清理
    clean = strip_invisible(text)
    print(f"\n2. 清理后:")
    print(f"  清理后长度: {len(clean)}")
    print(f"  清理后文本: '{clean}'")
    
    # 可打印判断
    print(f"\n3. 可打印判断:")
    print(f"  'A' 可打印: {is_printable('A')}")
    print(f"  '\\u0000' 可打印: {is_printable('\\u0000')}")
    print(f"  '\\u200B' 可打印: {is_printable('\\u200B')}")


def main():
    """运行所有示例"""
    example_char_info()
    example_emoji_detection()
    example_zero_width()
    example_normalization()
    example_string_stats()
    example_codepoint_conversion()
    example_unicode_search()
    example_encoding_detection()
    example_diacritics()
    example_rtl_detection()
    example_unicode_ranges()
    example_invisible_chars()
    
    print("\n" + "=" * 60)
    print("所有示例完成！")
    print("=" * 60)


if __name__ == '__main__':
    main()
#!/usr/bin/env python3
"""
string_utils/string_utils_test.py - 字符串处理工具测试
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    # 字符串统计
    count_chars, count_words, count_lines, count_sentences,
    get_text_stats, get_char_frequency, get_word_frequency,
    
    # 大小写转换
    to_camel_case, to_snake_case, to_kebab_case,
    to_title_case, to_sentence_case, to_constant_case, swap_case,
    
    # 字符串清理
    strip_whitespace, normalize_whitespace, remove_special_chars,
    remove_html_tags, unescape_html, clean_text, trim_lines,
    
    # 字符串相似度
    levenshtein_distance, similarity_ratio, sequence_similarity, 
    find_similar, jaccard_similarity,
    
    # 字符串反转与排序
    reverse_string, reverse_words, reverse_lines,
    sort_words, sort_lines, unique_lines, unique_chars,
    
    # 模式提取
    extract_emails, extract_urls, extract_phone_numbers,
    extract_numbers, extract_chinese, extract_english,
    extract_dates, extract_hex_colors, extract_pattern,
    
    # 字符串生成
    random_string, random_password, generate_uuid, generate_ordinal,
    generate_ngrams,
    
    # 字符串格式化
    indent_text, wrap_text, align_text, pad_text,
    truncate_text, format_number, center_with_char,
    
    # 实用工具
    is_palindrome, count_vowels, count_consonants,
    is_anagram, split_into_chunks, remove_duplicates,
    repeat_string, is_all_uppercase, is_all_lowercase,
    capitalize_each_word, contains_any, contains_all,
)


def test_count_chars():
    """测试字符统计"""
    assert count_chars("hello") == 5
    assert count_chars("hello world") == 11
    assert count_chars("hello world", include_spaces=False) == 10
    assert count_chars("") == 0
    print("✓ count_chars 测试通过")


def test_count_words():
    """测试单词统计"""
    assert count_words("hello world") == 2
    assert count_words("你好世界") == 4  # 4个中文字符
    assert count_words("hello 你好 world 世界") == 6  # 2英文单词 + 4中文
    assert count_words("") == 0
    print("✓ count_words 测试通过")


def test_count_lines():
    """测试行数统计"""
    assert count_lines("line1\nline2\nline3") == 3
    assert count_lines("line1\n\nline3", exclude_empty=True) == 2
    assert count_lines("") == 1  # 空字符串算1行
    print("✓ count_lines 测试通过")


def test_count_sentences():
    """测试句子统计"""
    assert count_sentences("Hello. World!") == 2
    assert count_sentences("你好。世界！") == 2
    assert count_sentences("Hello. 你好。World! 世界！") == 4
    print("✓ count_sentences 测试通过")


def test_get_text_stats():
    """测试文本统计"""
    text = "Hello world. 你好世界！\n\n这是第二段。"
    stats = get_text_stats(text)
    assert stats['chars'] == len(text)
    assert stats['words'] > 0
    assert stats['lines'] == 3
    assert stats['paragraphs'] == 2
    print("✓ get_text_stats 测试通过")


def test_get_char_frequency():
    """测试字符频率统计"""
    result = get_char_frequency("hello world", top_n=5)
    assert len(result) == 5
    # 'l' 出现3次应该是最多的
    assert result[0][0] == 'l'
    print("✓ get_char_frequency 测试通过")


def test_to_camel_case():
    """测试驼峰转换"""
    assert to_camel_case("hello-world") == "helloWorld"
    assert to_camel_case("hello_world") == "helloWorld"
    assert to_camel_case("hello world") == "helloWorld"
    assert to_camel_case("hello-world", capitalize_first=True) == "HelloWorld"
    assert to_camel_case("HELLO_WORLD") == "helloWorld"
    print("✓ to_camel_case 测试通过")


def test_to_snake_case():
    """测试蛇形转换"""
    assert to_snake_case("helloWorld") == "hello_world"
    assert to_snake_case("HelloWorld") == "hello_world"
    assert to_snake_case("hello-world") == "hello_world"
    assert to_snake_case("hello world") == "hello_world"
    assert to_snake_case("HELLO_WORLD") == "hello_world"
    print("✓ to_snake_case 测试通过")


def test_to_kebab_case():
    """测试短横线转换"""
    assert to_kebab_case("helloWorld") == "hello-world"
    assert to_kebab_case("HelloWorld") == "hello-world"
    assert to_kebab_case("hello_world") == "hello-world"
    assert to_kebab_case("hello world") == "hello-world"
    print("✓ to_kebab_case 测试通过")


def test_to_constant_case():
    """测试常量转换"""
    assert to_constant_case("helloWorld") == "HELLO_WORLD"
    assert to_constant_case("hello-world") == "HELLO_WORLD"
    print("✓ to_constant_case 测试通过")


def test_swap_case():
    """测试大小写交换"""
    assert swap_case("Hello World") == "hELLO wORLD"
    assert swap_case("ABC") == "abc"
    print("✓ swap_case 测试通过")


def test_strip_whitespace():
    """测试空白去除"""
    assert strip_whitespace("  hello  ", mode='both') == "hello"
    assert strip_whitespace("hello world", mode='all') == "helloworld"
    assert strip_whitespace("  hello  world  ", mode='all') == "helloworld"
    print("✓ strip_whitespace 测试通过")


def test_normalize_whitespace():
    """测试空白规范化"""
    assert normalize_whitespace("hello    world") == "hello world"
    assert normalize_whitespace("  hello  \n  world  ") == "hello world"
    print("✓ normalize_whitespace 测试通过")


def test_remove_special_chars():
    """测试特殊字符移除"""
    assert remove_special_chars("hello!@#world") == "helloworld"
    assert remove_special_chars("hello-world_test", keep="-_") == "hello-world_test"
    assert remove_special_chars("你好！世界") == "你好世界"
    print("✓ remove_special_chars 测试通过")


def test_remove_html_tags():
    """测试HTML标签移除"""
    assert remove_html_tags("<p>Hello</p>") == "Hello"
    assert remove_html_tags("<div><span>Test</span></div>") == "Test"
    print("✓ remove_html_tags 测试通过")


def test_unescape_html():
    """测试HTML反转义"""
    assert unescape_html("&lt;div&gt;") == "<div>"
    assert unescape_html("Hello&amp;World") == "Hello&World"
    assert unescape_html("&quot;Test&quot;") == '"Test"'
    print("✓ unescape_html 测试通过")


def test_clean_text():
    """测试文本清理"""
    assert clean_text("hello123 world", remove_numbers=True) == "hello world"
    assert clean_text("hello! world?", remove_punctuation=True) == "hello world"
    print("✓ clean_text 测试通过")


def test_trim_lines():
    """测试行trim"""
    assert trim_lines("  hello  \n  world  ") == "hello\nworld"
    print("✓ trim_lines 测试通过")


def test_levenshtein_distance():
    """测试编辑距离"""
    assert levenshtein_distance("", "") == 0
    assert levenshtein_distance("hello", "hello") == 0
    assert levenshtein_distance("hello", "hallo") == 1
    assert levenshtein_distance("hello", "") == 5
    assert levenshtein_distance("kitten", "sitting") == 3
    print("✓ levenshtein_distance 测试通过")


def test_similarity_ratio():
    """测试相似度"""
    assert similarity_ratio("hello", "hello") == 1.0
    assert similarity_ratio("", "") == 1.0
    assert similarity_ratio("hello", "") == 0.0
    assert 0.0 < similarity_ratio("hello", "hallo") < 1.0
    print("✓ similarity_ratio 测试通过")


def test_find_similar():
    """测试相似查找"""
    candidates = ["hello", "hallo", "help", "world", "shell"]
    results = find_similar("hello", candidates, threshold=0.5, top_n=3)
    assert len(results) > 0
    assert results[0][0] == "hello"  # 完全匹配排第一
    print("✓ find_similar 测试通过")


def test_jaccard_similarity():
    """测试Jaccard相似度"""
    assert jaccard_similarity("abc", "abc") == 1.0
    assert jaccard_similarity("abc", "xyz") == 0.0
    assert 0 < jaccard_similarity("abc", "bcd") < 1
    print("✓ jaccard_similarity 测试通过")


def test_reverse_string():
    """测试字符串反转"""
    assert reverse_string("hello") == "olleh"
    assert reverse_string("你好") == "好你"
    assert reverse_string("") == ""
    print("✓ reverse_string 测试通过")


def test_reverse_words():
    """测试单词反转"""
    assert reverse_words("hello world") == "world hello"
    assert reverse_words("one two three") == "three two one"
    print("✓ reverse_words 测试通过")


def test_reverse_lines():
    """测试行反转"""
    assert reverse_lines("line1\nline2\nline3") == "line3\nline2\nline1"
    print("✓ reverse_lines 测试通过")


def test_sort_words():
    """测试单词排序"""
    assert sort_words("c b a") == "a b c"
    assert sort_words("c b a", reverse=True) == "c b a"
    print("✓ sort_words 测试通过")


def test_sort_lines():
    """测试行排序"""
    text = "z\na\nm"
    assert sort_lines(text) == "a\nm\nz"
    assert sort_lines(text, reverse=True) == "z\nm\na"
    print("✓ sort_lines 测试通过")


def test_unique_lines():
    """测试行去重"""
    text = "a\nb\na\nc\nb"
    assert unique_lines(text) == "a\nb\nc"
    print("✓ unique_lines 测试通过")


def test_unique_chars():
    """测试字符去重"""
    assert unique_chars("hello") == "helo"
    assert unique_chars("aaa") == "a"
    print("✓ unique_chars 测试通过")


def test_extract_emails():
    """测试邮箱提取"""
    text = "联系 test@example.com 或 admin@test.org"
    emails = extract_emails(text)
    assert "test@example.com" in emails
    assert "admin@test.org" in emails
    print("✓ extract_emails 测试通过")


def test_extract_urls():
    """测试URL提取"""
    text = "访问 https://example.com 或 http://test.org/path"
    urls = extract_urls(text)
    assert "https://example.com" in urls
    assert "http://test.org/path" in urls
    print("✓ extract_urls 测试通过")


def test_extract_phone_numbers():
    """测试电话提取"""
    text = "电话：13812345678 或 18600001111"
    phones = extract_phone_numbers(text, country='CN')
    assert "13812345678" in phones
    assert len(phones) == 2
    print("✓ extract_phone_numbers 测试通过")


def test_extract_numbers():
    """测试数字提取"""
    text = "价格 100 元，折扣 0.5，温度 -10"
    numbers = extract_numbers(text)
    assert "100" in numbers
    assert "0.5" in numbers
    assert "-10" in numbers
    print("✓ extract_numbers 测试通过")


def test_extract_chinese():
    """测试中文提取"""
    text = "Hello 你好 World 世界"
    chinese = extract_chinese(text)
    assert "你好" in chinese
    assert "世界" in chinese
    print("✓ extract_chinese 测试通过")


def test_extract_english():
    """测试英文提取"""
    text = "Hello 你好 World 世界"
    english = extract_english(text)
    assert "Hello" in english
    assert "World" in english
    print("✓ extract_english 测试通过")


def test_extract_dates():
    """测试日期提取"""
    text = "日期：2024-01-15 或 2024/02/20 或 2024年3月25日"
    dates = extract_dates(text)
    assert "2024-01-15" in dates
    assert "2024/02/20" in dates
    print("✓ extract_dates 测试通过")


def test_extract_hex_colors():
    """测试颜色提取"""
    text = "颜色：#fff 和 #ff5500"
    colors = extract_hex_colors(text)
    assert "fff" in colors
    print("✓ extract_hex_colors 测试通过")


def test_extract_pattern():
    """测试自定义模式提取"""
    text = "abc123def456"
    numbers = extract_pattern(text, r'\d+')
    assert "123" in numbers
    assert "456" in numbers
    print("✓ extract_pattern 测试通过")


def test_random_string():
    """测试随机字符串"""
    s1 = random_string(16)
    s2 = random_string(16)
    assert len(s1) == 16
    assert len(s2) == 16
    assert s1 != s2  # 极大概率不同
    print("✓ random_string 测试通过")


def test_random_password():
    """测试随机密码"""
    pwd = random_password(16)
    assert len(pwd) == 16
    
    pwd_upper = random_password(20, include_upper=True, include_lower=False, 
                                include_digits=False, include_special=False)
    assert pwd_upper.isupper()
    
    pwd_simple = random_password(8, include_special=False)
    assert len(pwd_simple) == 8
    print("✓ random_password 测试通过")


def test_generate_uuid():
    """测试UUID生成"""
    uuid1 = generate_uuid()
    uuid2 = generate_uuid()
    assert len(uuid1) == 36  # UUID格式
    assert uuid1 != uuid2
    print("✓ generate_uuid 测试通过")


def test_generate_ordinal():
    """测试序数词生成"""
    assert generate_ordinal(1) == "1st"
    assert generate_ordinal(2) == "2nd"
    assert generate_ordinal(3) == "3rd"
    assert generate_ordinal(4) == "4th"
    assert generate_ordinal(11) == "11th"
    assert generate_ordinal(21) == "21st"
    assert generate_ordinal(1, lang='zh') == "第1"
    print("✓ generate_ordinal 测试通过")


def test_generate_ngrams():
    """测试N-gram生成"""
    assert generate_ngrams("hello", 2) == ["he", "el", "ll", "lo"]
    assert generate_ngrams("hello", 3) == ["hel", "ell", "llo"]
    print("✓ generate_ngrams 测试通过")


def test_indent_text():
    """测试缩进"""
    text = "hello\nworld"
    result = indent_text(text, spaces=4)
    assert result.startswith("    hello")
    print("✓ indent_text 测试通过")


def test_wrap_text():
    """测试换行"""
    text = "a" * 100
    result = wrap_text(text, width=50, break_long_words=True)
    assert '\n' in result
    print("✓ wrap_text 测试通过")


def test_align_text():
    """测试对齐"""
    text = "hello"
    assert len(align_text(text, width=20, align='left')) > len(text)
    centered = align_text(text, width=10, align='center')
    assert centered.strip() == "hello"
    print("✓ align_text 测试通过")


def test_truncate_text():
    """测试截断"""
    text = "hello world this is a long text"
    result = truncate_text(text, max_length=15)
    assert len(result) <= 15
    assert result.endswith("...")
    print("✓ truncate_text 测试通过")


def test_format_number():
    """测试数字格式化"""
    assert format_number(1234567.89, decimal_places=2) == "1,234,567.89"
    assert format_number(1000) == "1,000.00"
    print("✓ format_number 测试通过")


def test_center_with_char():
    """测试字符居中填充"""
    assert center_with_char("hello", 11, '-') == "---hello---"
    print("✓ center_with_char 测试通过")


def test_is_palindrome():
    """测试回文检测"""
    assert is_palindrome("racecar") == True
    assert is_palindrome("A man a plan a canal Panama", ignore_spaces=True) == True
    assert is_palindrome("hello") == False
    assert is_palindrome("上海自来水来自海上", ignore_spaces=True) == True
    print("✓ is_palindrome 测试通过")


def test_count_vowels():
    """测试元音统计"""
    vowels = count_vowels("hello world")
    assert vowels['e'] == 1
    assert vowels['o'] == 2
    print("✓ count_vowels 测试通过")


def test_count_consonants():
    """测试辅音统计"""
    assert count_consonants("hello") == 3  # h, l, l
    print("✓ count_consonants 测试通过")


def test_is_anagram():
    """测试变位词检测"""
    assert is_anagram("listen", "silent") == True
    assert is_anagram("hello", "world") == False
    assert is_anagram("Dormitory", "Dirty room", ignore_case=True) == True
    print("✓ is_anagram 测试通过")


def test_split_into_chunks():
    """测试文本分块"""
    text = "abcdefghij"
    chunks = split_into_chunks(text, chunk_size=3)
    assert chunks == ["abc", "def", "ghi", "j"]
    
    chunks_overlap = split_into_chunks(text, chunk_size=5, overlap=2)
    assert len(chunks_overlap) >= 2
    assert chunks_overlap[0] == "abcde"
    print("✓ split_into_chunks 测试通过")


def test_remove_duplicates():
    """测试单词去重"""
    text = "hello world hello test world"
    result = remove_duplicates(text)
    assert result == "hello world test"
    print("✓ remove_duplicates 测试通过")


def test_repeat_string():
    """测试字符串重复"""
    assert repeat_string("ab", 3, "-") == "ab-ab-ab"
    assert repeat_string("ab", 2) == "abab"
    assert repeat_string("ab", 0) == ""
    print("✓ repeat_string 测试通过")


def test_is_all_uppercase():
    """测试全大写检测"""
    assert is_all_uppercase("HELLO") == True
    assert is_all_uppercase("Hello") == False
    assert is_all_uppercase("HELLO123") == True  # 数字不影响
    print("✓ is_all_uppercase 测试通过")


def test_is_all_lowercase():
    """测试全小写检测"""
    assert is_all_lowercase("hello") == True
    assert is_all_lowercase("Hello") == False
    print("✓ is_all_lowercase 测试通过")


def test_capitalize_each_word():
    """测试单词首字母大写"""
    assert capitalize_each_word("hello world") == "Hello World"
    print("✓ capitalize_each_word 测试通过")


def test_contains_any():
    """测试包含任意字符"""
    assert contains_any("hello", "ae") == True
    assert contains_any("hello", "xyz") == False
    print("✓ contains_any 测试通过")


def test_contains_all():
    """测试包含所有字符"""
    assert contains_all("hello", "helo") == True
    assert contains_all("hello", "xyz") == False
    print("✓ contains_all 测试通过")


def run_all_tests():
    """运行所有测试"""
    print("=" * 50)
    print("string_utils 测试套件")
    print("=" * 50)
    
    # 字符串统计测试
    print("\n[字符串统计测试]")
    test_count_chars()
    test_count_words()
    test_count_lines()
    test_count_sentences()
    test_get_text_stats()
    test_get_char_frequency()
    
    # 大小写转换测试
    print("\n[大小写转换测试]")
    test_to_camel_case()
    test_to_snake_case()
    test_to_kebab_case()
    test_to_constant_case()
    test_swap_case()
    
    # 字符串清理测试
    print("\n[字符串清理测试]")
    test_strip_whitespace()
    test_normalize_whitespace()
    test_remove_special_chars()
    test_remove_html_tags()
    test_unescape_html()
    test_clean_text()
    test_trim_lines()
    
    # 字符串相似度测试
    print("\n[字符串相似度测试]")
    test_levenshtein_distance()
    test_similarity_ratio()
    test_find_similar()
    test_jaccard_similarity()
    
    # 字符串反转与排序测试
    print("\n[字符串反转与排序测试]")
    test_reverse_string()
    test_reverse_words()
    test_reverse_lines()
    test_sort_words()
    test_sort_lines()
    test_unique_lines()
    test_unique_chars()
    
    # 模式提取测试
    print("\n[模式提取测试]")
    test_extract_emails()
    test_extract_urls()
    test_extract_phone_numbers()
    test_extract_numbers()
    test_extract_chinese()
    test_extract_english()
    test_extract_dates()
    test_extract_hex_colors()
    test_extract_pattern()
    
    # 字符串生成测试
    print("\n[字符串生成测试]")
    test_random_string()
    test_random_password()
    test_generate_uuid()
    test_generate_ordinal()
    test_generate_ngrams()
    
    # 字符串格式化测试
    print("\n[字符串格式化测试]")
    test_indent_text()
    test_wrap_text()
    test_align_text()
    test_truncate_text()
    test_format_number()
    test_center_with_char()
    
    # 实用工具测试
    print("\n[实用工具测试]")
    test_is_palindrome()
    test_count_vowels()
    test_count_consonants()
    test_is_anagram()
    test_split_into_chunks()
    test_remove_duplicates()
    test_repeat_string()
    test_is_all_uppercase()
    test_is_all_lowercase()
    test_capitalize_each_word()
    test_contains_any()
    test_contains_all()
    
    print("\n" + "=" * 50)
    print("✅ 所有测试通过!")
    print("=" * 50)


if __name__ == '__main__':
    run_all_tests()
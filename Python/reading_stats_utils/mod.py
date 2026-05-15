"""
Reading Statistics Utilities - 阅读统计分析工具

提供文本阅读时间估算、可读性评分、词汇复杂度分析等功能。
零外部依赖，纯 Python 实现。
"""

import re
import math
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass


@dataclass
class ReadingStats:
    """阅读统计数据结构"""
    character_count: int
    character_count_no_spaces: int
    word_count: int
    sentence_count: int
    paragraph_count: int
    syllable_count: int
    reading_time_minutes: float
    speaking_time_minutes: float
    avg_word_length: float
    avg_sentence_length: float
    avg_syllables_per_word: float
    flesch_reading_ease: float
    flesch_kincaid_grade: float
    gunning_fog_index: float
    coleman_liau_index: float
    automated_readability_index: float
    avg_letters_per_word: float
    avg_sentences_per_paragraph: float
    complex_word_count: int
    difficult_word_count: int
    unique_word_count: int
    vocabulary_density: float
    readability_level: str


# 平均阅读速度（词/分钟）
READING_SPEED_SLOW = 150  # 慢速阅读
READING_SPEED_AVERAGE = 200  # 平均阅读速度
READING_SPEED_FAST = 250  # 快速阅读
READING_SPEED_SKIMMING = 400  # 略读

# 平均说话速度（词/分钟）
SPEAKING_SPEED = 150

# 中文阅读速度（字/分钟）
CHINESE_READING_SPEED = 300


def count_syllables_word(word: str) -> int:
    """
    估算英文单词的音节数。
    使用规则方法，适用于大多数英语单词。
    
    Args:
        word: 英文单词
    
    Returns:
        音节数
    
    Examples:
        >>> count_syllables_word("hello")
        2
        >>> count_syllables_word("the")
        1
        >>> count_syllables_word("beautiful")
        3
    """
    word = word.lower().strip()
    
    if not word:
        return 0
    
    # 特殊情况处理
    if len(word) <= 2:
        return 1
    
    # 元音字母
    vowels = "aeiouy"
    
    # 计算音节数
    count = 0
    prev_is_vowel = False
    
    for char in word:
        is_vowel = char in vowels
        if is_vowel and not prev_is_vowel:
            count += 1
        prev_is_vowel = is_vowel
    
    # 处理末尾静音 e
    if word.endswith('e') and count > 1:
        count -= 1
    
    # 处理 le 结尾
    if word.endswith('le') and len(word) > 2 and word[-3] not in vowels:
        count += 1
    
    # 处理 ed 结尾（过去式）
    if word.endswith('ed'):
        if len(word) > 2 and word[-3] not in vowels:
            # 如 "jumped" -> "jump" 本身就有一个音节
            pass
    
    # 至少一个音节
    return max(1, count)


def is_chinese_char(char: str) -> bool:
    """
    判断字符是否为中文字符。
    
    Args:
        char: 单个字符
    
    Returns:
        是否为中文字符
    
    Examples:
        >>> is_chinese_char('中')
        True
        >>> is_chinese_char('a')
        False
    """
    code_point = ord(char)
    # CJK统一汉字范围
    return (
        0x4E00 <= code_point <= 0x9FFF or      # CJK基本区
        0x3400 <= code_point <= 0x4DBF or      # CJK扩展A
        0x20000 <= code_point <= 0x2A6DF or    # CJK扩展B
        0x2A700 <= code_point <= 0x2B73F or    # CJK扩展C
        0x2B740 <= code_point <= 0x2B81F or    # CJK扩展D
        0x2B820 <= code_point <= 0x2CEAF or    # CJK扩展E
        0x2CEB0 <= code_point <= 0x2EBEF      # CJK扩展F
    )


def is_japanese_char(char: str) -> bool:
    """
    判断字符是否为日文字符（假名）。
    
    Args:
        char: 单个字符
    
    Returns:
        是否为日文字符
    """
    code_point = ord(char)
    return (
        0x3040 <= code_point <= 0x309F or      # 平假名
        0x30A0 <= code_point <= 0x30FF         # 片假名
    )


def is_korean_char(char: str) -> bool:
    """
    判断字符是否为韩文字符（谚文）。
    
    Args:
        char: 单个字符
    
    Returns:
        是否为韩文字符
    """
    code_point = ord(char)
    return (
        0xAC00 <= code_point <= 0xD7A3 or      # 韩文字符
        0x1100 <= code_point <= 0x11FF         # 韩文字母
    )


def detect_language(text: str) -> Dict[str, float]:
    """
    检测文本的语言组成比例。
    
    Args:
        text: 输入文本
    
    Returns:
        各语言字符所占比例的字典
    
    Examples:
        >>> detect_language("Hello 世界")
        {'chinese': 0.5, 'english': 0.5, 'other': 0.0}
    """
    if not text:
        return {'chinese': 0.0, 'english': 0.0, 'japanese': 0.0, 'korean': 0.0, 'other': 0.0}
    
    counts = {'chinese': 0, 'english': 0, 'japanese': 0, 'korean': 0, 'other': 0}
    
    for char in text:
        if is_chinese_char(char):
            counts['chinese'] += 1
        elif is_japanese_char(char):
            counts['japanese'] += 1
        elif is_korean_char(char):
            counts['korean'] += 1
        elif char.isalpha() and ord(char) < 128:
            counts['english'] += 1
        elif not char.isspace():
            counts['other'] += 1
    
    total = sum(counts.values())
    if total == 0:
        return {'chinese': 0.0, 'english': 0.0, 'japanese': 0.0, 'korean': 0.0, 'other': 0.0}
    
    return {k: v / total for k, v in counts.items()}


def extract_words(text: str) -> List[str]:
    """
    从文本中提取单词（支持中英文混合）。
    
    Args:
        text: 输入文本
    
    Returns:
        单词列表
    
    Examples:
        >>> extract_words("Hello 世界!")
        ['Hello', '世界']
    """
    # 英文单词
    english_words = re.findall(r'[a-zA-Z]+', text)
    
    # 中文字符（每个字作为一个"词"）
    chinese_chars = [char for char in text if is_chinese_char(char)]
    
    return english_words + chinese_chars


def count_words(text: str) -> int:
    """
    统计单词数（中英文混合）。
    英文按单词计，中文按字符计。
    
    Args:
        text: 输入文本
    
    Returns:
        单词总数
    
    Examples:
        >>> count_words("Hello 世界!")
        3
        >>> count_words("Hello World")
        2
    """
    return len(extract_words(text))


def count_sentences(text: str) -> int:
    """
    统计句子数。
    
    Args:
        text: 输入文本
    
    Returns:
        句子数量
    
    Examples:
        >>> count_sentences("Hello! How are you? Fine.")
        3
    """
    # 匹配句子结束符
    # 英文句号、问号、感叹号、中文句号、问号、感叹号
    pattern = r'[.!?。！？]+'
    sentences = re.findall(pattern, text)
    
    # 如果有文本但没有匹配到句子，算作1句
    if not sentences and text.strip():
        return 1
    
    return len(sentences)


def count_paragraphs(text: str) -> int:
    """
    统计段落数。
    
    Args:
        text: 输入文本
    
    Returns:
        段落数量
    
    Examples:
        >>> count_paragraphs("First para.\\n\\nSecond para.")
        2
    """
    # 按空行分割段落
    paragraphs = re.split(r'\n\s*\n', text.strip())
    paragraphs = [p for p in paragraphs if p.strip()]
    
    return max(1, len(paragraphs))


def count_syllables(text: str) -> int:
    """
    统计音节数（针对英文文本）。
    
    Args:
        text: 输入文本
    
    Returns:
        音节总数
    
    Examples:
        >>> count_syllables("hello world")
        3
    """
    words = re.findall(r'[a-zA-Z]+', text)
    return sum(count_syllables_word(word) for word in words)


def count_complex_words(text: str) -> int:
    """
    统计复杂单词数（音节数>=3的单词）。
    
    Args:
        text: 输入文本
    
    Returns:
        复杂单词数量
    
    Examples:
        >>> count_complex_words("beautiful amazing")
        2
    """
    words = re.findall(r'[a-zA-Z]+', text)
    return sum(1 for word in words if count_syllables_word(word) >= 3)


def count_difficult_words(text: str, known_words: Optional[set] = None) -> int:
    """
    统计生僻词数量。
    如果没有提供已知词表，默认认为音节数>=4的词为生僻词。
    
    Args:
        text: 输入文本
        known_words: 已知词集合
    
    Returns:
        生僻词数量
    """
    words = re.findall(r'[a-zA-Z]+', text)
    
    if known_words:
        return sum(1 for word in words if word.lower() not in known_words)
    else:
        return sum(1 for word in words if count_syllables_word(word) >= 4)


def count_unique_words(text: str) -> int:
    """
    统计不重复单词数。
    
    Args:
        text: 输入文本
    
    Returns:
        不重复单词数量
    
    Examples:
        >>> count_unique_words("hello world hello")
        2
    """
    words = extract_words(text)
    return len(set(word.lower() for word in words))


def reading_time(text: str, wpm: int = READING_SPEED_AVERAGE) -> float:
    """
    估算阅读时间（分钟）。
    自动识别中英文并使用合适的计算方式。
    
    Args:
        text: 输入文本
        wpm: 每分钟阅读字数/词数
    
    Returns:
        阅读时间（分钟）
    
    Examples:
        >>> reading_time("Hello world")
        0.01
    """
    lang_ratio = detect_language(text)
    
    # 中文占比高时按字数计算
    if lang_ratio['chinese'] > 0.5:
        chinese_chars = sum(1 for char in text if is_chinese_char(char))
        english_words = len(re.findall(r'[a-zA-Z]+', text))
        total_chars = chinese_chars + english_words
        return total_chars / CHINESE_READING_SPEED
    else:
        word_count = count_words(text)
        return word_count / wpm


def speaking_time(text: str, wpm: int = SPEAKING_SPEED) -> float:
    """
    估算朗读时间（分钟）。
    
    Args:
        text: 输入文本
        wpm: 每分钟说话字数/词数
    
    Returns:
        朗读时间（分钟）
    
    Examples:
        >>> speaking_time("Hello world")
        0.013...
    """
    word_count = count_words(text)
    return word_count / wpm


def flesch_reading_ease(text: str) -> float:
    """
    计算 Flesch Reading Ease 可读性分数。
    
    分数解读：
    - 90-100: 非常容易（5年级）
    - 80-89: 容易（6年级）
    - 70-79: 较容易（7年级）
    - 60-69: 标准（8-9年级）
    - 50-59: 较难（10-12年级）
    - 30-49: 困难（大学）
    - 0-29: 非常困难（专业）
    
    Args:
        text: 输入文本
    
    Returns:
        Flesch Reading Ease 分数
    
    Examples:
        >>> flesch_reading_ease("The cat sat on the mat.")
        80.0...
    """
    words = re.findall(r'[a-zA-Z]+', text)
    if not words:
        return 0.0
    
    word_count = len(words)
    sentence_count = max(1, count_sentences(text))
    syllable_count = count_syllables(text)
    
    asl = word_count / sentence_count  # 平均句长
    asw = syllable_count / word_count  # 每词平均音节
    
    # Flesch 公式
    score = 206.835 - (1.015 * asl) - (84.6 * asw)
    
    return max(0, min(100, score))


def flesch_kincaid_grade(text: str) -> float:
    """
    计算 Flesch-Kincaid Grade Level。
    
    分数表示理解文本所需的美国年级水平。
    
    Args:
        text: 输入文本
    
    Returns:
        年级水平
    
    Examples:
        >>> flesch_kincaid_grade("The cat sat on the mat.")
        2.0...
    """
    words = re.findall(r'[a-zA-Z]+', text)
    if not words:
        return 0.0
    
    word_count = len(words)
    sentence_count = max(1, count_sentences(text))
    syllable_count = count_syllables(text)
    
    asl = word_count / sentence_count
    asw = syllable_count / word_count
    
    # Flesch-Kincaid 公式
    grade = (0.39 * asl) + (11.8 * asw) - 15.59
    
    return max(0, grade)


def gunning_fog_index(text: str) -> float:
    """
    计算 Gunning Fog Index。
    
    分数表示理解文本所需的受教育年数。
    
    Args:
        text: 输入文本
    
    Returns:
        Gunning Fog 指数
    
    Examples:
        >>> gunning_fog_index("The cat sat on the mat.")
        4.0...
    """
    words = re.findall(r'[a-zA-Z]+', text)
    if not words:
        return 0.0
    
    word_count = len(words)
    sentence_count = max(1, count_sentences(text))
    complex_words = count_complex_words(text)
    
    asl = word_count / sentence_count
    phw = complex_words / word_count  # 复杂词比例
    
    # Gunning Fog 公式
    index = 0.4 * (asl + 100 * phw)
    
    return max(0, index)


def coleman_liau_index(text: str) -> float:
    """
    计算 Coleman-Liau Index。
    
    基于字符数计算的可读性指数。
    
    Args:
        text: 输入文本
    
    Returns:
        Coleman-Liau 指数
    """
    words = re.findall(r'[a-zA-Z]+', text)
    if not words:
        return 0.0
    
    word_count = len(words)
    sentence_count = max(1, count_sentences(text))
    character_count = sum(len(word) for word in words)
    
    # 每百词字符数
    l = (character_count / word_count) * 100
    # 每百词句子数
    s = (sentence_count / word_count) * 100
    
    # Coleman-Liau 公式
    index = (0.0588 * l) - (0.296 * s) - 15.8
    
    return max(0, index)


def automated_readability_index(text: str) -> float:
    """
    计算自动化可读性指数 (ARI)。
    
    基于字符数、单词数和句子数计算。
    
    Args:
        text: 输入文本
    
    Returns:
        ARI 指数
    """
    words = re.findall(r'[a-zA-Z]+', text)
    if not words:
        return 0.0
    
    word_count = len(words)
    sentence_count = max(1, count_sentences(text))
    character_count = sum(len(word) for word in words)
    
    # ARI 公式
    ari = (4.71 * (character_count / word_count)) + (0.5 * (word_count / sentence_count)) - 21.43
    
    return max(0, ari)


def get_readability_level(score: float) -> str:
    """
    根据 Flesch Reading Ease 分数获取可读性等级描述。
    
    Args:
        score: Flesch Reading Ease 分数
    
    Returns:
        可读性等级描述
    
    Examples:
        >>> get_readability_level(85)
        '容易 (6年级)'
    """
    if score >= 90:
        return "非常容易 (5年级)"
    elif score >= 80:
        return "容易 (6年级)"
    elif score >= 70:
        return "较容易 (7年级)"
    elif score >= 60:
        return "标准 (8-9年级)"
    elif score >= 50:
        return "较难 (10-12年级)"
    elif score >= 30:
        return "困难 (大学)"
    else:
        return "非常困难 (专业)"


def analyze_text(text: str, known_words: Optional[set] = None) -> ReadingStats:
    """
    全面分析文本，返回完整的阅读统计数据。
    
    Args:
        text: 输入文本
        known_words: 已知词集合（用于计算生僻词）
    
    Returns:
        ReadingStats 数据对象
    
    Examples:
        >>> stats = analyze_text("Hello world!")
        >>> stats.word_count
        2
    """
    # 基础统计
    character_count = len(text)
    character_count_no_spaces = len(text.replace(' ', '').replace('\n', '').replace('\t', ''))
    word_count = count_words(text)
    sentence_count = count_sentences(text)
    paragraph_count = count_paragraphs(text)
    syllable_count = count_syllables(text)
    
    # 时间估算
    read_time = reading_time(text)
    speak_time = speaking_time(text)
    
    # 平均值
    avg_word_length = sum(len(word) for word in extract_words(text)) / max(1, word_count)
    avg_sentence_length = word_count / max(1, sentence_count)
    avg_syllables_per_word = syllable_count / max(1, len(re.findall(r'[a-zA-Z]+', text)))
    avg_letters_per_word = sum(len(w) for w in re.findall(r'[a-zA-Z]+', text)) / max(1, len(re.findall(r'[a-zA-Z]+', text)))
    avg_sentences_per_paragraph = sentence_count / max(1, paragraph_count)
    
    # 可读性指数
    fre = flesch_reading_ease(text)
    fkg = flesch_kincaid_grade(text)
    gfi = gunning_fog_index(text)
    cli = coleman_liau_index(text)
    ari = automated_readability_index(text)
    
    # 复杂度统计
    complex_word_count = count_complex_words(text)
    difficult_word_count = count_difficult_words(text, known_words)
    unique_word_count = count_unique_words(text)
    
    # 词汇密度
    vocabulary_density = unique_word_count / max(1, word_count)
    
    # 可读性等级
    readability_level = get_readability_level(fre)
    
    return ReadingStats(
        character_count=character_count,
        character_count_no_spaces=character_count_no_spaces,
        word_count=word_count,
        sentence_count=sentence_count,
        paragraph_count=paragraph_count,
        syllable_count=syllable_count,
        reading_time_minutes=read_time,
        speaking_time_minutes=speak_time,
        avg_word_length=avg_word_length,
        avg_sentence_length=avg_sentence_length,
        avg_syllables_per_word=avg_syllables_per_word,
        flesch_reading_ease=fre,
        flesch_kincaid_grade=fkg,
        gunning_fog_index=gfi,
        coleman_liau_index=cli,
        automated_readability_index=ari,
        avg_letters_per_word=avg_letters_per_word,
        avg_sentences_per_paragraph=avg_sentences_per_paragraph,
        complex_word_count=complex_word_count,
        difficult_word_count=difficult_word_count,
        unique_word_count=unique_word_count,
        vocabulary_density=vocabulary_density,
        readability_level=readability_level
    )


def format_time(minutes: float) -> str:
    """
    将分钟数格式化为易读的时间字符串。
    
    Args:
        minutes: 分钟数
    
    Returns:
        格式化的时间字符串
    
    Examples:
        >>> format_time(90)
        '1小时30分钟'
        >>> format_time(5.5)
        '5分钟30秒'
    """
    if minutes < 1:
        seconds = int(minutes * 60)
        return f"{seconds}秒"
    elif minutes < 60:
        mins = int(minutes)
        secs = int((minutes - mins) * 60)
        if secs > 0:
            return f"{mins}分钟{secs}秒"
        return f"{mins}分钟"
    else:
        hours = int(minutes // 60)
        mins = int(minutes % 60)
        if mins > 0:
            return f"{hours}小时{mins}分钟"
        return f"{hours}小时"


def get_reading_suggestions(stats: ReadingStats) -> List[str]:
    """
    根据阅读统计数据提供改进建议。
    
    Args:
        stats: 阅读统计数据
    
    Returns:
        建议列表
    """
    suggestions = []
    
    # 句子长度建议
    if stats.avg_sentence_length > 25:
        suggestions.append("建议缩短句子长度。当前平均每句{}个词，建议控制在15-20词以内。".format(
            int(stats.avg_sentence_length)))
    
    # 复杂词建议
    if stats.complex_word_count > 0:
        complex_ratio = stats.complex_word_count / max(1, stats.word_count)
        if complex_ratio > 0.2:
            suggestions.append(f"复杂词汇占比{complex_ratio*100:.1f}%，考虑使用更简单的替代词。")
    
    # 可读性建议
    if stats.flesch_reading_ease < 50:
        suggestions.append("文本可读性较低。考虑：使用短句、替换复杂词汇、添加过渡词。")
    
    # 词汇多样性建议
    if stats.vocabulary_density > 0.8:
        suggestions.append("词汇多样性很高，但可能增加理解难度。考虑重复使用关键术语。")
    
    if not suggestions:
        suggestions.append("文本可读性良好，适合目标读者阅读。")
    
    return suggestions


def compare_texts(text1: str, text2: str) -> Dict[str, Tuple[float, float]]:
    """
    比较两段文本的阅读统计。
    
    Args:
        text1: 第一段文本
        text2: 第二段文本
    
    Returns:
        比较结果字典
    """
    stats1 = analyze_text(text1)
    stats2 = analyze_text(text2)
    
    return {
        'word_count': (stats1.word_count, stats2.word_count),
        'sentence_count': (stats1.sentence_count, stats2.sentence_count),
        'reading_time': (stats1.reading_time_minutes, stats2.reading_time_minutes),
        'flesch_reading_ease': (stats1.flesch_reading_ease, stats2.flesch_reading_ease),
        'flesch_kincaid_grade': (stats1.flesch_kincaid_grade, stats2.flesch_kincaid_grade),
        'vocabulary_density': (stats1.vocabulary_density, stats2.vocabulary_density),
        'complex_word_count': (stats1.complex_word_count, stats2.complex_word_count)
    }


def estimate_audience(stats: ReadingStats) -> str:
    """
    根据统计数据估算目标受众。
    
    Args:
        stats: 阅读统计数据
    
    Returns:
        目标受众描述
    """
    grade = stats.flesch_kincaid_grade
    
    if grade <= 6:
        return "小学生 (6-12岁)"
    elif grade <= 8:
        return "初中生 (12-15岁)"
    elif grade <= 12:
        return "高中生 (15-18岁)"
    elif grade <= 16:
        return "大学生 (18-22岁)"
    else:
        return "专业人士/研究生"


# 预定义文本类型参考值
TEXT_TYPE_REFERENCE = {
    'children_book': {
        'flesch_reading_ease': (80, 100),
        'avg_sentence_length': (5, 12),
        'description': '儿童读物'
    },
    'news_article': {
        'flesch_reading_ease': (50, 70),
        'avg_sentence_length': (15, 25),
        'description': '新闻文章'
    },
    'academic_paper': {
        'flesch_reading_ease': (0, 50),
        'avg_sentence_length': (20, 35),
        'description': '学术论文'
    },
    'novel': {
        'flesch_reading_ease': (60, 80),
        'avg_sentence_length': (10, 20),
        'description': '小说'
    },
    'technical_doc': {
        'flesch_reading_ease': (40, 60),
        'avg_sentence_length': (15, 25),
        'description': '技术文档'
    },
    'marketing': {
        'flesch_reading_ease': (60, 80),
        'avg_sentence_length': (8, 15),
        'description': '营销文案'
    }
}


def classify_text_type(stats: ReadingStats) -> List[str]:
    """
    根据统计数据分类文本类型。
    
    Args:
        stats: 阅读统计数据
    
    Returns:
        可能的文本类型列表
    """
    matches = []
    
    for text_type, ref in TEXT_TYPE_REFERENCE.items():
        fre_range = ref['flesch_reading_ease']
        asl_range = ref['avg_sentence_length']
        
        if (fre_range[0] <= stats.flesch_reading_ease <= fre_range[1] and
            asl_range[0] <= stats.avg_sentence_length <= asl_range[1]):
            matches.append(ref['description'])
    
    return matches if matches else ['通用文本']


if __name__ == "__main__":
    # 简单测试
    test_text = """
    The quick brown fox jumps over the lazy dog. 
    This sentence contains every letter of the alphabet.
    Reading is a wonderful adventure that opens doors to new worlds.
    """
    
    print("=== 阅读统计分析测试 ===\n")
    
    stats = analyze_text(test_text)
    
    print(f"字符数: {stats.character_count}")
    print(f"单词数: {stats.word_count}")
    print(f"句子数: {stats.sentence_count}")
    print(f"段落数: {stats.paragraph_count}")
    print(f"音节数: {stats.syllable_count}")
    print(f"\n阅读时间: {format_time(stats.reading_time_minutes)}")
    print(f"朗读时间: {format_time(stats.speaking_time_minutes)}")
    print(f"\n平均句长: {stats.avg_sentence_length:.1f} 词")
    print(f"复杂词数: {stats.complex_word_count}")
    print(f"词汇密度: {stats.vocabulary_density:.2%}")
    print(f"\nFlesch Reading Ease: {stats.flesch_reading_ease:.1f}")
    print(f"Flesch-Kincaid Grade: {stats.flesch_kincaid_grade:.1f}")
    print(f"Gunning Fog Index: {stats.gunning_fog_index:.1f}")
    print(f"可读性等级: {stats.readability_level}")
    print(f"目标受众: {estimate_audience(stats)}")
    print(f"可能类型: {', '.join(classify_text_type(stats))}")
    
    print("\n=== 改进建议 ===")
    for suggestion in get_reading_suggestions(stats):
        print(f"- {suggestion}")
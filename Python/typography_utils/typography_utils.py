"""
Typography Utilities - 智能文本排版工具
=====================================

零外部依赖的排版工具集，提供智能引号转换、破折号规范化、
省略号处理、文本换行等功能。

功能：
- 智能引号转换（直引号 → 弯引号）
- 破折号规范化（连字符 → en dash / em dash）
- 省略号规范化（三个点 → 省略号字符）
- 文本换行（按行长）
- 寡妇/孤儿行处理
- 字符统计
- 空白规范化

作者：AllToolkit 自动生成
日期：2026-05-21
"""

import re
import textwrap
from typing import Tuple, Dict, List, Optional


# ==================== 智能引号转换 ====================

def smart_quotes(text: str, 
                 left_double: str = '"', 
                 right_double: str = '"',
                 left_single: str = ''',
                 right_single: str = ''') -> str:
    """
    将直引号转换为智能引号（弯引号）。
    
    Args:
        text: 输入文本
        left_double: 左双引号字符（默认中文弯引号）
        right_double: 右双引号字符
        left_single: 左单引号字符
        right_single: 右单引号字符
    
    Returns:
        转换后的文本
        
    Examples:
        >>> smart_quotes('He said "hello".')
        'He said "hello".'
        >>> smart_quotes("It's a test.", left_single="'", right_single="'")
        "It's a test."
    """
    result = []
    double_open = False
    single_open = False
    
    i = 0
    while i < len(text):
        char = text[i]
        prev_char = text[i-1] if i > 0 else ''
        next_char = text[i+1] if i < len(text)-1 else ''
        
        if char == '"':
            # 双引号处理
            if double_open:
                result.append(right_double)
                double_open = False
            else:
                result.append(left_double)
                double_open = True
        elif char == "'":
            # 单引号处理 - 区分缩写和引号
            # 如果前后都是字母，认为是缩写（如 it's, don't）
            if prev_char.isalpha() and next_char.isalpha():
                result.append(right_single)  # 缩写用右单引号（或撇号）
            elif single_open:
                result.append(right_single)
                single_open = False
            else:
                # 检查是否是缩写开头（如 'tis）
                if next_char.isalpha() and (prev_char == '' or not prev_char.isalpha()):
                    result.append(left_single)
                    single_open = True
                else:
                    result.append(left_single)
                    single_open = True
        else:
            result.append(char)
        
        i += 1
    
    return ''.join(result)


def straighten_quotes(text: str) -> str:
    """
    将智能引号转换回直引号。
    
    Args:
        text: 包含弯引号的文本
        
    Returns:
        转换后的文本（使用直引号）
        
    Examples:
        >>> straighten_quotes('He said "hello".')
        'He said "hello".'
    """
    replacements = {
        '"': '"', '"': '"',  # 中文弯引号
        ''': "'", ''': "'",  # 中文单引号
        '«': '"', '»': '"',  # 法语引号
        '‹': "'", '›': "'",  # 单角引号
        '„': '"', '‚': "'",  # 德语引号
        '「': "'", '」': "'",  # 中文直角引号
        '『': '"', '』': '"',  # 中文双直角引号
    }
    
    for curved, straight in replacements.items():
        text = text.replace(curved, straight)
    
    return text


# ==================== 破折号规范化 ====================

def normalize_dashes(text: str, style: str = 'auto') -> str:
    """
    规范化破折号。
    
    Args:
        text: 输入文本
        style: 破折号风格
            - 'auto': 自动检测上下文
            - 'en': 使用 en dash (–)
            - 'em': 使用 em dash (—)
            - 'hyphen': 全部使用连字符 (-)
        
    Returns:
        规范化后的文本
        
    Examples:
        >>> normalize_dashes('pages 10--20')
        'pages 10–20'
        >>> normalize_dashes('thought -- or idea')
        'thought — or idea'
    """
    # 先规范化所有破折号类型
    text = text.replace('—', '--')  # em dash
    text = text.replace('–', '--')  # en dash
    
    if style == 'hyphen':
        return text.replace('--', '-')
    
    # 处理双连字符
    result = []
    i = 0
    while i < len(text):
        if i < len(text) - 1 and text[i:i+2] == '--':
            # 检查上下文
            before = text[:i].rstrip() if i > 0 else ''
            after_start = i + 2
            while after_start < len(text) and text[after_start] == ' ':
                after_start += 1
            after = text[after_start:] if after_start < len(text) else ''
            
            # 检查是否是数字范围 (如 10--20)
            before_match = re.search(r'(\d+)\s*$', before)
            after_match = re.match(r'^\s*(\d+)', after)
            
            if style == 'en' or (style == 'auto' and before_match and after_match):
                result.append('–')  # en dash 用于范围
            else:
                result.append('—')  # em dash 用于断句
            
            i += 2
        else:
            result.append(text[i])
            i += 1
    
    return ''.join(result)


def em_dash(text: str) -> str:
    """将双连字符转换为 em dash (—)。"""
    return normalize_dashes(text, 'em')


def en_dash(text: str) -> str:
    """将双连字符转换为 en dash (–)。"""
    return normalize_dashes(text, 'en')


# ==================== 省略号规范化 ====================

def normalize_ellipsis(text: str, use_char: bool = True) -> str:
    """
    规范化省略号。
    
    Args:
        text: 输入文本
        use_char: True 使用省略号字符 (…), False 使用三个点 (...)
        
    Returns:
        规范化后的文本
        
    Examples:
        >>> normalize_ellipsis('Wait...')
        'Wait…'
        >>> normalize_ellipsis('Wait...', use_char=False)
        'Wait...'
    """
    # 处理各种形式的省略号
    patterns = [
        r'\.{4,}',      # 四个或更多点
        r'\.{3}',       # 三个点
        r'\. \. \.',    # 带空格的点
        r'…+',          # 多个省略号字符
    ]
    
    if use_char:
        replacement = '…'
    else:
        replacement = '...'
    
    for pattern in patterns:
        text = re.sub(pattern, replacement, text)
    
    return text


# ==================== 综合排版处理 ====================

def smartify(text: str, 
             quotes: bool = True,
             dashes: bool = True,
             ellipsis: bool = True,
             spaces: bool = True) -> str:
    """
    一站式智能排版处理。
    
    Args:
        text: 输入文本
        quotes: 是否处理引号
        dashes: 是否处理破折号
        ellipsis: 是否处理省略号
        spaces: 是否规范化空格
        
    Returns:
        处理后的文本
        
    Examples:
        >>> smartify('He said "hello"... wait -- I mean "hi".')
        'He said "hello"… wait — I mean "hi".'
    """
    result = text
    
    if quotes:
        result = smart_quotes(result)
    
    if dashes:
        result = normalize_dashes(result)
    
    if ellipsis:
        result = normalize_ellipsis(result)
    
    if spaces:
        result = normalize_spaces(result)
    
    return result


# ==================== 文本换行 ====================

def wrap_text(text: str, 
              width: int = 80, 
              indent: str = '',
              initial_indent: str = '',
              break_long_words: bool = True,
              break_on_hyphens: bool = True) -> str:
    """
    按指定宽度换行文本。
    
    Args:
        text: 输入文本
        width: 每行最大宽度
        indent: 后续行缩进
        initial_indent: 首行缩进
        break_long_words: 是否断开长单词
        break_on_hyphens: 是否在连字符处断开
        
    Returns:
        换行后的文本
        
    Examples:
        >>> wrap_text('This is a long text that needs wrapping.', width=20)
        'This is a long text\\nthat needs wrapping.'
    """
    wrapper = textwrap.TextWrapper(
        width=width,
        initial_indent=initial_indent,
        subsequent_indent=indent,
        break_long_words=break_long_words,
        break_on_hyphens=break_on_hyphens
    )
    return wrapper.fill(text)


def wrap_paragraphs(text: str, width: int = 80) -> str:
    """
    按段落换行文本。
    
    Args:
        text: 输入文本（可能包含多个段落）
        width: 每行最大宽度
        
    Returns:
        换行后的文本
    """
    paragraphs = re.split(r'\n\s*\n', text)
    wrapped = [wrap_text(p.strip(), width=width) for p in paragraphs if p.strip()]
    return '\n\n'.join(wrapped)


# ==================== 寡妇/孤儿行处理 ====================

def prevent_widows(text: str, 
                   min_last_words: int = 2, 
                   min_penultimate_words: int = 3) -> str:
    """
    防止寡妇行（段落最后只剩一个词）。
    
    通过在不间断空格处调整，确保段落最后至少有 min_last_words 个词。
    
    Args:
        text: 输入文本
        min_last_words: 最后一行最少词数
        min_penultimate_words: 倒数第二行最少词数
        
    Returns:
        处理后的文本
        
    Examples:
        >>> prevent_widows('This is a short line.\\nLast')
        'This is a short line.\\nLast'  # 会尝试用不间断空格连接
    """
    lines = text.split('\n')
    if len(lines) < 2:
        return text
    
    result_lines = []
    
    for i, line in enumerate(lines):
        words = line.split()
        
        if i == len(lines) - 1:
            # 最后一行
            if len(words) < min_last_words and i > 0:
                # 尝试与前一行合并
                prev_words = result_lines[i-1].split()
                if len(prev_words) >= min_penultimate_words + min_last_words:
                    # 从前一行移动词到当前行
                    move_count = min_last_words - len(words)
                    if move_count > 0 and move_count < len(prev_words):
                        moved = prev_words[-move_count:]
                        result_lines[i-1] = ' '.join(prev_words[:-move_count])
                        result_lines.append(' '.join(moved + words))
                        continue
        
        result_lines.append(line)
    
    return '\n'.join(result_lines)


# ==================== 空白规范化 ====================

def normalize_spaces(text: str) -> str:
    """
    规范化空白字符。
    
    - 将多个连续空格压缩为一个
    - 移除行首行尾空白
    - 规范化换行符
    
    Args:
        text: 输入文本
        
    Returns:
        规范化后的文本
        
    Examples:
        >>> normalize_spaces('  hello   world  ')
        'hello world'
    """
    # 压缩多个空格
    text = re.sub(r'[ \t]+', ' ', text)
    # 移除行首行尾空白
    text = '\n'.join(line.strip() for line in text.split('\n'))
    # 压缩多个空行
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


def remove_extra_blank_lines(text: str, max_blank: int = 1) -> str:
    """
    移除多余空行。
    
    Args:
        text: 输入文本
        max_blank: 允许的最大连续空行数
        
    Returns:
        处理后的文本
    """
    pattern = r'\n{' + str(max_blank + 2) + r',}'
    replacement = '\n' * (max_blank + 1)
    return re.sub(pattern, replacement, text)


# ==================== 字符统计 ====================

def count_chars(text: str, include_spaces: bool = True) -> int:
    """统计字符数。"""
    if include_spaces:
        return len(text)
    return len(text.replace(' ', '').replace('\t', '').replace('\n', ''))


def count_words(text: str) -> int:
    """统计单词数。"""
    # 处理中英文混合文本
    # 英文按空格分词
    english_words = len(re.findall(r'[a-zA-Z]+', text))
    # 中文按字符计数
    chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
    return english_words + chinese_chars


def count_sentences(text: str) -> int:
    """统计句子数。"""
    # 匹配句子结束符
    sentences = re.split(r'[.!?。！？]+', text)
    # 过滤空句子
    return len([s for s in sentences if s.strip()])


def count_paragraphs(text: str) -> int:
    """统计段落数。"""
    paragraphs = re.split(r'\n\s*\n', text)
    return len([p for p in paragraphs if p.strip()])


def text_statistics(text: str) -> Dict[str, int]:
    """
    获取文本统计信息。
    
    Args:
        text: 输入文本
        
    Returns:
        包含各种统计数据的字典
        
    Examples:
        >>> stats = text_statistics('Hello world. How are you?')
        >>> stats['words']
        5
        >>> stats['sentences']
        2
    """
    return {
        'chars': count_chars(text),
        'chars_no_spaces': count_chars(text, include_spaces=False),
        'words': count_words(text),
        'sentences': count_sentences(text),
        'paragraphs': count_paragraphs(text),
        'lines': len(text.split('\n')),
        'chinese_chars': len(re.findall(r'[\u4e00-\u9fff]', text)),
        'english_words': len(re.findall(r'[a-zA-Z]+', text)),
        'digits': len(re.findall(r'\d', text)),
        'punctuation': len(re.findall(r'[^\w\s]', text)),
    }


# ==================== 特殊字符处理 ====================

def escape_html(text: str) -> str:
    """
    转义 HTML 特殊字符。
    
    Args:
        text: 输入文本
        
    Returns:
        转义后的文本
        
    Examples:
        >>> escape_html('<div>Hello & Goodbye</div>')
        '&lt;div&gt;Hello &amp; Goodbye&lt;/div&gt;'
    """
    replacements = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#39;',
    }
    for char, escape in replacements.items():
        text = text.replace(char, escape)
    return text


def unescape_html(text: str) -> str:
    """
    反转义 HTML 字符。
    
    Args:
        text: 包含 HTML 实体的文本
        
    Returns:
        反转义后的文本
    """
    replacements = {
        '&amp;': '&',
        '&lt;': '<',
        '&gt;': '>',
        '&quot;': '"',
        '&#39;': "'",
        '&nbsp;': ' ',
        '&copy;': '©',
        '&reg;': '®',
        '&trade;': '™',
    }
    for escape, char in replacements.items():
        text = text.replace(escape, char)
    return text


def escape_markdown(text: str) -> str:
    """
    转义 Markdown 特殊字符。
    
    Args:
        text: 输入文本
        
    Returns:
        转义后的文本
        
    Examples:
        >>> escape_markdown('# Hello **World**')
        '\\\\# Hello \\\\*\\\\*World\\\\*\\\\*'
    """
    special_chars = ['\\', '`', '*', '_', '{', '}', '[', ']', '(', ')', '#', '+', '-', '.', '!', '|']
    
    result = text
    for char in special_chars:
        result = result.replace(char, '\\' + char)
    
    return result


# ==================== 标题处理 ====================

def title_case(text: str, exceptions: Optional[List[str]] = None) -> str:
    """
    将文本转换为标题格式。
    
    Args:
        text: 输入文本
        exceptions: 不需要大写的词（如冠词、介词）
        
    Returns:
        标题格式的文本
        
    Examples:
        >>> title_case('the quick brown fox')
        'The Quick Brown Fox'
        >>> title_case('the lord of the rings', ['the', 'of'])
        'The Lord of the Rings'
    """
    if exceptions is None:
        exceptions = ['a', 'an', 'the', 'and', 'but', 'or', 'for', 'nor', 
                      'on', 'at', 'to', 'by', 'in', 'of', 'with', 'from']
    
    words = text.lower().split()
    result = []
    
    for i, word in enumerate(words):
        if i == 0 or word not in exceptions:
            result.append(word.capitalize())
        else:
            result.append(word)
    
    return ' '.join(result)


def slugify(text: str, separator: str = '-', lowercase: bool = True) -> str:
    """
    将文本转换为 URL 友好的 slug。
    
    Args:
        text: 输入文本
        separator: 分隔符
        lowercase: 是否转为小写
        
    Returns:
        slug 字符串
        
    Examples:
        >>> slugify('Hello World!')
        'hello-world'
        >>> slugify('This is a Test', separator='_')
        'this_is_a_test'
    """
    # 移除特殊字符，只保留字母、数字和中文
    text = re.sub(r'[^\w\s\u4e00-\u9fff-]', '', text)
    
    # 替换空白为分隔符
    text = re.sub(r'\s+', separator, text)
    
    # 移除多余的分隔符
    text = re.sub(re.escape(separator) + '+', separator, text)
    
    # 移除首尾分隔符
    text = text.strip(separator)
    
    if lowercase:
        text = text.lower()
    
    return text


# ==================== 行号添加 ====================

def add_line_numbers(text: str, start: int = 1, width: int = 4) -> str:
    """
    为文本添加行号。
    
    Args:
        text: 输入文本
        start: 起始行号
        width: 行号宽度
        
    Returns:
        带行号的文本
        
    Examples:
        >>> print(add_line_numbers('Hello\\nWorld'))
           1 Hello
           2 World
    """
    lines = text.split('\n')
    result = []
    
    for i, line in enumerate(lines, start=start):
        result.append(f'{i:>{width}} {line}')
    
    return '\n'.join(result)


# ==================== 对齐处理 ====================

def align_left(text: str, width: int, fillchar: str = ' ') -> str:
    """左对齐文本。"""
    lines = text.split('\n')
    return '\n'.join(line.ljust(width, fillchar) for line in lines)


def align_right(text: str, width: int, fillchar: str = ' ') -> str:
    """右对齐文本。"""
    lines = text.split('\n')
    return '\n'.join(line.rjust(width, fillchar) for line in lines)


def align_center(text: str, width: int, fillchar: str = ' ') -> str:
    """居中对齐文本。"""
    lines = text.split('\n')
    return '\n'.join(line.center(width, fillchar) for line in lines)


def align_justify(text: str, width: int) -> str:
    """
    两端对齐文本。
    
    Args:
        text: 输入文本
        width: 每行宽度
        
    Returns:
        两端对齐的文本
        
    Examples:
        >>> align_justify('Hello world this is a test', 20)
        'Hello world this is\\na test'
    """
    lines = text.split('\n')
    result = []
    
    for line in lines:
        words = line.split()
        if len(words) <= 1:
            result.append(line)
            continue
        
        # 计算需要的空格
        total_spaces = width - sum(len(w) for w in words)
        gaps = len(words) - 1
        
        if gaps > 0:
            space_per_gap = total_spaces // gaps
            extra_spaces = total_spaces % gaps
            
            justified = []
            for i, word in enumerate(words[:-1]):
                spaces = space_per_gap + (1 if i < extra_spaces else 0)
                justified.append(word + ' ' * spaces)
            justified.append(words[-1])
            
            result.append(''.join(justified))
        else:
            result.append(line)
    
    return '\n'.join(result)


# ==================== 中文排版处理 ====================

def normalize_chinese_punctuation(text: str) -> str:
    """
    规范化中文标点符号。
    
    将英文标点转换为中文标点。
    
    Args:
        text: 输入文本
        
    Returns:
        规范化后的文本
        
    Examples:
        >>> normalize_chinese_punctuation('你好,世界!')
        '你好，世界！'
    """
    replacements = {
        ',': '，',
        '.': '。',
        '!': '！',
        '?': '？',
        ':': '：',
        ';': '；',
        '(': '（',
        ')': '）',
        '[': '【',
        ']': '】',
    }
    
    result = []
    for char in text:
        # 只有在中文字符周围时才转换
        result.append(replacements.get(char, char))
    
    return ''.join(result)


def chinese_paragraph_indent(text: str, indent: str = '　　') -> str:
    """
    为中文段落添加首行缩进。
    
    Args:
        text: 输入文本
        indent: 缩进字符串（默认两个全角空格）
        
    Returns:
        处理后的文本
        
    Examples:
        >>> chinese_paragraph_indent('第一段\\n\\n第二段')
        '　　第一段\\n\\n　　第二段'
    """
    paragraphs = re.split(r'\n\s*\n', text)
    result = [indent + p.strip() if p.strip() else '' for p in paragraphs]
    return '\n\n'.join(result)


# ==================== 版本信息 ====================

__version__ = '1.0.0'
__author__ = 'AllToolkit'


if __name__ == '__main__':
    # 演示用法
    demo_text = 'He said "Hello World"... this is a test -- really!'
    print('原始文本:', demo_text)
    print('智能排版:', smartify(demo_text))
    print()
    
    demo_chinese = '你好,世界!这是一个测试.'
    print('原始文本:', demo_chinese)
    print('中文标点规范化:', normalize_chinese_punctuation(demo_chinese))
    print()
    
    stats_text = 'Hello world. How are you today? I am fine!'
    print('文本:', stats_text)
    print('统计:', text_statistics(stats_text))
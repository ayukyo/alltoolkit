"""
text_diff_utils - 文本差异比较工具模块

提供文本对比、差异展示、相似度计算等功能。
零外部依赖，纯 Python 标准库实现。

核心功能：
- 字符级差异检测
- 单词级差异检测  
- 行级差异检测
- 多种差异展示格式（统一格式、上下文格式、并排格式）
- 相似度计算
- 变更统计
"""

from difflib import SequenceMatcher, unified_diff as _unified_diff, context_diff as _context_diff
from typing import List, Tuple, Dict, Optional, NamedTuple
from dataclasses import dataclass
from enum import Enum
import re


class DiffType(Enum):
    """差异类型枚举"""
    EQUAL = "equal"      # 相同
    INSERT = "insert"    # 插入
    DELETE = "delete"    # 删除
    REPLACE = "replace"  # 替换


@dataclass
class DiffOperation:
    """差异操作数据类"""
    diff_type: DiffType
    old_start: int
    old_end: int
    new_start: int
    new_end: int
    old_content: str
    new_content: str


@dataclass
class DiffStats:
    """差异统计数据类"""
    additions: int       # 新增行/字符数
    deletions: int       # 删除行/字符数
    modifications: int   # 修改行/字符数
    unchanged: int       # 未变行/字符数
    similarity: float    # 相似度 (0.0 - 1.0)


class TextDiff:
    """文本差异比较器"""
    
    def __init__(self, text1: str, text2: str):
        """
        初始化文本差异比较器
        
        Args:
            text1: 原始文本
            text2: 新文本
        """
        self.text1 = text1
        self.text2 = text2
        self._lines1 = text1.splitlines(keepends=True)
        self._lines2 = text2.splitlines(keepends=True)
    
    def compare_chars(self) -> List[Tuple[DiffType, str]]:
        """
        字符级差异比较
        
        Returns:
            差异操作列表，每个元素为 (差异类型, 文本片段)
        """
        matcher = SequenceMatcher(None, self.text1, self.text2)
        result = []
        
        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag == 'equal':
                result.append((DiffType.EQUAL, self.text1[i1:i2]))
            elif tag == 'insert':
                result.append((DiffType.INSERT, self.text2[j1:j2]))
            elif tag == 'delete':
                result.append((DiffType.DELETE, self.text1[i1:i2]))
            elif tag == 'replace':
                result.append((DiffType.DELETE, self.text1[i1:i2]))
                result.append((DiffType.INSERT, self.text2[j1:j2]))
        
        return result
    
    def compare_words(self) -> List[Tuple[DiffType, str]]:
        """
        单词级差异比较
        
        Returns:
            差异操作列表，每个元素为 (差异类型, 单词)
        """
        # 分词：保留空格和标点作为分隔符
        words1 = re.findall(r'\S+|\s+', self.text1)
        words2 = re.findall(r'\S+|\s+', self.text2)
        
        matcher = SequenceMatcher(None, words1, words2)
        result = []
        
        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag == 'equal':
                for w in words1[i1:i2]:
                    result.append((DiffType.EQUAL, w))
            elif tag == 'insert':
                for w in words2[j1:j2]:
                    result.append((DiffType.INSERT, w))
            elif tag == 'delete':
                for w in words1[i1:i2]:
                    result.append((DiffType.DELETE, w))
            elif tag == 'replace':
                for w in words1[i1:i2]:
                    result.append((DiffType.DELETE, w))
                for w in words2[j1:j2]:
                    result.append((DiffType.INSERT, w))
        
        return result
    
    def compare_lines(self) -> List[Tuple[DiffType, str]]:
        """
        行级差异比较
        
        Returns:
            差异操作列表，每个元素为 (差异类型, 行内容)
        """
        matcher = SequenceMatcher(None, self._lines1, self._lines2)
        result = []
        
        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag == 'equal':
                for line in self._lines1[i1:i2]:
                    result.append((DiffType.EQUAL, line))
            elif tag == 'insert':
                for line in self._lines2[j1:j2]:
                    result.append((DiffType.INSERT, line))
            elif tag == 'delete':
                for line in self._lines1[i1:i2]:
                    result.append((DiffType.DELETE, line))
            elif tag == 'replace':
                for line in self._lines1[i1:i2]:
                    result.append((DiffType.DELETE, line))
                for line in self._lines2[j1:j2]:
                    result.append((DiffType.INSERT, line))
        
        return result
    
    def get_operations(self) -> List[DiffOperation]:
        """
        获取结构化差异操作列表
        
        Returns:
            DiffOperation 对象列表
        """
        matcher = SequenceMatcher(None, self._lines1, self._lines2)
        operations = []
        
        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            diff_type = DiffType(tag)
            operations.append(DiffOperation(
                diff_type=diff_type,
                old_start=i1 + 1,
                old_end=i2,
                new_start=j1 + 1,
                new_end=j2,
                old_content=''.join(self._lines1[i1:i2]),
                new_content=''.join(self._lines2[j1:j2])
            ))
        
        return operations
    
    def unified_diff(self, n: int = 3, 
                     fromfile: str = 'original', 
                     tofile: str = 'modified') -> str:
        """
        生成统一格式差异（类似 git diff）
        
        Args:
            n: 上下文行数
            fromfile: 原文件名
            tofile: 新文件名
        
        Returns:
            统一格式差异字符串
        """
        diff_lines = list(_unified_diff(
            self._lines1,
            self._lines2,
            fromfile=fromfile,
            tofile=tofile,
            n=n
        ))
        return ''.join(diff_lines)
    
    def context_diff(self, n: int = 3,
                      fromfile: str = 'original',
                      tofile: str = 'modified') -> str:
        """
        生成上下文格式差异
        
        Args:
            n: 上下文行数
            fromfile: 原文件名
            tofile: 新文件名
        
        Returns:
            上下文格式差异字符串
        """
        diff_lines = list(_context_diff(
            self._lines1,
            self._lines2,
            fromfile=fromfile,
            tofile=tofile,
            n=n
        ))
        return ''.join(diff_lines)
    
    def side_by_side_text(self, width: int = 50, 
                          show_line_numbers: bool = True) -> str:
        """
        生成并排格式差异（纯文本版）
        
        Args:
            width: 每侧宽度
            show_line_numbers: 是否显示行号
        
        Returns:
            并排格式差异字符串
        """
        lines1 = self.text1.splitlines()
        lines2 = self.text2.splitlines()
        matcher = SequenceMatcher(None, lines1, lines2)
        
        result = []
        separator = ' | '
        
        # 标题行
        left_title = 'Original'.ljust(width)
        right_title = 'Modified'.ljust(width)
        result.append(f"{left_title}{separator}{right_title}")
        result.append('-' * (width * 2 + len(separator)))
        
        left_lines = []
        right_lines = []
        
        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag == 'equal':
                for idx, (left, right) in enumerate(zip(lines1[i1:i2], lines2[j1:j2])):
                    left_lines.append((' ', left))
                    right_lines.append((' ', right))
            elif tag == 'insert':
                for line in lines2[j1:j2]:
                    left_lines.append((' ', ''))
                    right_lines.append(('+', line))
            elif tag == 'delete':
                for line in lines1[i1:i2]:
                    left_lines.append(('-', line))
                    right_lines.append((' ', ''))
            elif tag == 'replace':
                # 配对显示替换
                old_lines = lines1[i1:i2]
                new_lines = lines2[j1:j2]
                max_len = max(len(old_lines), len(new_lines))
                for i in range(max_len):
                    old_line = old_lines[i] if i < len(old_lines) else ''
                    new_line = new_lines[i] if i < len(new_lines) else ''
                    left_lines.append(('-' if old_line else ' ', old_line))
                    right_lines.append(('+' if new_line else ' ', new_line))
        
        max_lines = max(len(left_lines), len(right_lines))
        
        for i in range(max_lines):
            left_marker, left_content = left_lines[i] if i < len(left_lines) else (' ', '')
            right_marker, right_content = right_lines[i] if i < len(right_lines) else (' ', '')
            
            left_display = left_content[:width].ljust(width)
            right_display = right_content[:width].ljust(width)
            
            if show_line_numbers:
                line_num = str(i + 1).rjust(4)
                result.append(f"{line_num} {left_marker}{left_display}{separator}{right_marker}{right_display}")
            else:
                result.append(f"{left_marker}{left_display}{separator}{right_marker}{right_display}")
        
        return '\n'.join(result)
    
    def similarity(self) -> float:
        """
        计算文本相似度
        
        Returns:
            相似度值 (0.0 - 1.0)
        """
        matcher = SequenceMatcher(None, self.text1, self.text2)
        return matcher.ratio()
    
    def quick_ratio(self) -> float:
        """
        快速计算相似度（上界估计，更快）
        
        Returns:
            相似度上界 (0.0 - 1.0)
        """
        matcher = SequenceMatcher(None, self.text1, self.text2)
        return matcher.quick_ratio()
    
    def stats(self, level: str = 'line') -> DiffStats:
        """
        获取差异统计
        
        Args:
            level: 统计级别 ('char', 'word', 'line')
        
        Returns:
            DiffStats 对象
        """
        if level == 'char':
            ops = self.compare_chars()
            total1 = len(self.text1)
            total2 = len(self.text2)
        elif level == 'word':
            ops = self.compare_words()
            words1 = re.findall(r'\S+', self.text1)
            words2 = re.findall(r'\S+', self.text2)
            total1 = len(words1)
            total2 = len(words2)
        else:  # line
            ops = self.compare_lines()
            total1 = len(self._lines1)
            total2 = len(self._lines2)
        
        additions = 0
        deletions = 0
        modifications = 0
        unchanged = 0
        
        # 追踪上一个操作类型，用于合并相邻的删除+插入为修改
        prev_type = None
        prev_len = 0
        
        for diff_type, content in ops:
            if diff_type == DiffType.EQUAL:
                unchanged += 1
                if prev_type == DiffType.DELETE:
                    # 之前的删除不是修改的一部分
                    deletions += prev_len
                prev_type = DiffType.EQUAL
                prev_len = 0
            elif diff_type == DiffType.INSERT:
                if prev_type == DiffType.DELETE:
                    modifications += 1
                    deletions += max(0, prev_len - 1)
                else:
                    additions += 1
                prev_type = DiffType.INSERT
                prev_len = 0
            elif diff_type == DiffType.DELETE:
                if prev_type == DiffType.DELETE:
                    pass  # 连续删除
                prev_type = DiffType.DELETE
                prev_len = 1
        
        if prev_type == DiffType.DELETE:
            deletions += prev_len
        
        similarity = self.similarity()
        
        return DiffStats(
            additions=additions,
            deletions=deletions,
            modifications=modifications,
            unchanged=unchanged,
            similarity=similarity
        )


def diff_texts(text1: str, text2: str, level: str = 'line') -> List[Tuple[DiffType, str]]:
    """
    快捷函数：比较两个文本
    
    Args:
        text1: 原始文本
        text2: 新文本
        level: 比较级别 ('char', 'word', 'line')
    
    Returns:
        差异操作列表
    """
    differ = TextDiff(text1, text2)
    if level == 'char':
        return differ.compare_chars()
    elif level == 'word':
        return differ.compare_words()
    else:
        return differ.compare_lines()


def generate_unified_diff(text1: str, text2: str, 
                          fromfile: str = 'original',
                          tofile: str = 'modified',
                          n: int = 3) -> str:
    """
    快捷函数：生成统一格式差异
    
    Args:
        text1: 原始文本
        text2: 新文本
        fromfile: 原文件名
        tofile: 新文件名
        n: 上下文行数
    
    Returns:
        统一格式差异字符串
    """
    differ = TextDiff(text1, text2)
    return differ.unified_diff(n=n, fromfile=fromfile, tofile=tofile)


# 别名，保持向后兼容
unified_diff = generate_unified_diff


def similarity(text1: str, text2: str) -> float:
    """
    快捷函数：计算两个文本的相似度
    
    Args:
        text1: 第一个文本
        text2: 第二个文本
    
    Returns:
        相似度值 (0.0 - 1.0)
    """
    return SequenceMatcher(None, text1, text2).ratio()


def find_common_substring(text1: str, text2: str) -> str:
    """
    查找两个文本的最长公共子串
    
    Args:
        text1: 第一个文本
        text2: 第二个文本
    
    Returns:
        最长公共子串
    """
    matcher = SequenceMatcher(None, text1, text2)
    match = matcher.find_longest_match(0, len(text1), 0, len(text2))
    return text1[match.a:match.a + match.size]


def find_common_subsequences(text1: str, text2: str, 
                             min_length: int = 3) -> List[str]:
    """
    查找两个文本的所有公共子串
    
    Args:
        text1: 第一个文本
        text2: 第二个文本
        min_length: 最小子串长度
    
    Returns:
        公共子串列表（按长度降序）
    """
    matcher = SequenceMatcher(None, text1, text2)
    matches = matcher.get_matching_blocks()
    
    subsequences = []
    for match in matches:
        if match.size >= min_length:
            subsequences.append(text1[match.a:match.a + match.size])
    
    return sorted(subsequences, key=len, reverse=True)


def highlight_diff_html(text1: str, text2: str, 
                        level: str = 'word',
                        insert_color: str = '#d4edda',
                        delete_color: str = '#f8d7da') -> str:
    """
    生成 HTML 格式的高亮差异
    
    Args:
        text1: 原始文本
        text2: 新文本
        level: 比较级别 ('char', 'word')
        insert_color: 插入部分背景色
        delete_color: 删除部分背景色
    
    Returns:
        HTML 格式的差异展示
    """
    differ = TextDiff(text1, text2)
    
    if level == 'char':
        ops = differ.compare_chars()
    else:
        ops = differ.compare_words()
    
    html_parts = []
    
    for diff_type, content in ops:
        # HTML 转义
        escaped = content.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        
        if diff_type == DiffType.INSERT:
            html_parts.append(f'<span style="background-color: {insert_color}">{escaped}</span>')
        elif diff_type == DiffType.DELETE:
            html_parts.append(f'<span style="background-color: {delete_color}"><del>{escaped}</del></span>')
        else:
            html_parts.append(escaped)
    
    return ''.join(html_parts)


def count_changes(text1: str, text2: str, level: str = 'line') -> Dict[str, int]:
    """
    统计变更数量
    
    Args:
        text1: 原始文本
        text2: 新文本
        level: 统计级别 ('char', 'word', 'line')
    
    Returns:
        变更统计字典
    """
    differ = TextDiff(text1, text2)
    ops = differ.compare_chars() if level == 'char' else \
          (differ.compare_words() if level == 'word' else differ.compare_lines())
    
    additions = sum(1 for t, _ in ops if t == DiffType.INSERT)
    deletions = sum(1 for t, _ in ops if t == DiffType.DELETE)
    unchanged = sum(1 for t, _ in ops if t == DiffType.EQUAL)
    
    return {
        'additions': additions,
        'deletions': deletions,
        'unchanged': unchanged,
        'total_changes': additions + deletions,
        'similarity': differ.similarity()
    }


def diff_three_texts(text1: str, text2: str, text3: str) -> Dict[str, float]:
    """
    比较三个文本的相似度
    
    Args:
        text1: 第一个文本
        text2: 第二个文本
        text3: 第三个文本
    
    Returns:
        两两相似度字典
    """
    return {
        'text1_vs_text2': similarity(text1, text2),
        'text1_vs_text3': similarity(text1, text3),
        'text2_vs_text3': similarity(text2, text3)
    }


if __name__ == '__main__':
    # 简单演示
    original = """Hello World
This is a test.
Line three.
Line four.
Goodbye!"""
    
    modified = """Hello World
This is a modified test.
Line three.
New line inserted.
Line four.
See you later!"""
    
    diff = TextDiff(original, modified)
    
    print("=== 字符级差异 ===")
    for dtype, content in diff.compare_chars():
        if dtype != DiffType.EQUAL:
            print(f"{dtype.value}: {repr(content)}")
    
    print("\n=== 行级差异 ===")
    for dtype, content in diff.compare_lines():
        marker = {'equal': ' ', 'insert': '+', 'delete': '-'}[dtype.value]
        print(f"{marker} {content.rstrip()}")
    
    print("\n=== 统一格式差异 ===")
    print(diff.unified_diff())
    
    print("\n=== 差异统计 ===")
    stats = diff.stats()
    print(f"新增: {stats.additions}, 删除: {stats.deletions}, 相似度: {stats.similarity:.2%}")
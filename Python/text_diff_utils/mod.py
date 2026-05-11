"""
文本差异比较工具模块 (Text Diff Utils)

功能：
- 比较两段文本的差异
- 生成统一格式差异报告 (Unified Diff)
- 生成并排对比视图
- 行级别和字符级别的差异检测
- 相似度计算
- 差异统计

零外部依赖，仅使用 Python 标准库。
"""

import difflib
from typing import List, Tuple, Dict, Optional, NamedTuple
from dataclasses import dataclass
from enum import Enum


class DiffType(Enum):
    """差异类型枚举"""
    EQUAL = "equal"      # 相同
    INSERT = "insert"    # 新增
    DELETE = "delete"    # 删除
    REPLACE = "replace"  # 替换


@dataclass
class DiffLine:
    """差异行数据结构"""
    line_number_old: Optional[int]  # 原文件行号
    line_number_new: Optional[int]  # 新文件行号
    content: str                      # 行内容
    diff_type: DiffType               # 差异类型


@dataclass
class DiffResult:
    """差异比较结果"""
    old_lines: int           # 原文本行数
    new_lines: int           # 新文本行数
    added_lines: int         # 新增行数
    deleted_lines: int       # 删除行数
    changed_lines: int      # 修改行数
    similarity: float        # 相似度 (0.0 - 1.0)
    diff_lines: List[DiffLine]  # 差异行列表


class TextDiffUtils:
    """文本差异比较工具类"""
    
    def __init__(self, ignore_case: bool = False, 
                 ignore_whitespace: bool = False,
                 ignore_blank_lines: bool = False):
        """
        初始化文本差异比较工具
        
        Args:
            ignore_case: 是否忽略大小写
            ignore_whitespace: 是否忽略空白字符
            ignore_blank_lines: 是否忽略空行
        """
        self.ignore_case = ignore_case
        self.ignore_whitespace = ignore_whitespace
        self.ignore_blank_lines = ignore_blank_lines
    
    def _normalize_text(self, text: str) -> str:
        """标准化文本（应用忽略规则）"""
        if self.ignore_case:
            text = text.lower()
        if self.ignore_whitespace:
            text = ' '.join(text.split())
        return text
    
    def _normalize_lines(self, lines: List[str]) -> List[str]:
        """标准化行列表"""
        result = []
        for line in lines:
            if self.ignore_blank_lines and not line.strip():
                continue
            result.append(self._normalize_text(line))
        return result
    
    def compare_lines(self, old_text: str, new_text: str) -> DiffResult:
        """
        比较两段文本的行级差异
        
        Args:
            old_text: 原文本
            new_text: 新文本
        
        Returns:
            DiffResult: 差异比较结果
        """
        old_lines = old_text.splitlines(keepends=True)
        new_lines = new_text.splitlines(keepends=True)
        
        # 标准化用于比较
        old_normalized = self._normalize_lines(old_lines)
        new_normalized = self._normalize_lines(new_lines)
        
        # 使用 SequenceMatcher 进行差异检测
        matcher = difflib.SequenceMatcher(None, old_normalized, new_normalized)
        
        diff_lines = []
        added = deleted = changed = 0
        
        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag == 'equal':
                for i, line in enumerate(old_lines[i1:i2]):
                    diff_lines.append(DiffLine(
                        line_number_old=i1 + i + 1,
                        line_number_new=j1 + i + 1,
                        content=line,
                        diff_type=DiffType.EQUAL
                    ))
            elif tag == 'insert':
                for j, line in enumerate(new_lines[j1:j2]):
                    diff_lines.append(DiffLine(
                        line_number_old=None,
                        line_number_new=j1 + j + 1,
                        content=line,
                        diff_type=DiffType.INSERT
                    ))
                added += (j2 - j1)
            elif tag == 'delete':
                for i, line in enumerate(old_lines[i1:i2]):
                    diff_lines.append(DiffLine(
                        line_number_old=i1 + i + 1,
                        line_number_new=None,
                        content=line,
                        diff_type=DiffType.DELETE
                    ))
                deleted += (i2 - i1)
            elif tag == 'replace':
                # 先处理删除的行
                for i, line in enumerate(old_lines[i1:i2]):
                    diff_lines.append(DiffLine(
                        line_number_old=i1 + i + 1,
                        line_number_new=None,
                        content=line,
                        diff_type=DiffType.DELETE
                    ))
                deleted += (i2 - i1)
                # 再处理新增的行
                for j, line in enumerate(new_lines[j1:j2]):
                    diff_lines.append(DiffLine(
                        line_number_old=None,
                        line_number_new=j1 + j + 1,
                        content=line,
                        diff_type=DiffType.INSERT
                    ))
                added += (j2 - j1)
        
        similarity = matcher.ratio()
        
        return DiffResult(
            old_lines=len(old_lines),
            new_lines=len(new_lines),
            added_lines=added,
            deleted_lines=deleted,
            changed_lines=changed,
            similarity=similarity,
            diff_lines=diff_lines
        )
    
    def unified_diff(self, old_text: str, new_text: str,
                     old_filename: str = "old",
                     new_filename: str = "new",
                     context_lines: int = 3) -> str:
        """
        生成统一格式的差异报告
        
        Args:
            old_text: 原文本
            new_text: 新文本
            old_filename: 原文件名
            new_filename: 新文件名
            context_lines: 上下文行数
        
        Returns:
            str: 统一格式差异报告
        """
        old_lines = old_text.splitlines(keepends=True)
        new_lines = new_text.splitlines(keepends=True)
        
        diff = difflib.unified_diff(
            old_lines,
            new_lines,
            fromfile=old_filename,
            tofile=new_filename,
            lineterm='',
            n=context_lines
        )
        
        return '\n'.join(diff)
    
    def side_by_side(self, old_text: str, new_text: str, 
                     width: int = 50) -> List[Tuple[str, str, str]]:
        """
        生成并排对比视图
        
        Args:
            old_text: 原文本
            new_text: 新文本
            width: 每列宽度
        
        Returns:
            List[Tuple[str, str, str]]: (左侧内容, 分隔符, 右侧内容)
        """
        old_lines = old_text.splitlines()
        new_lines = new_text.splitlines()
        
        old_normalized = self._normalize_lines(old_lines)
        new_normalized = self._normalize_lines(new_lines)
        
        matcher = difflib.SequenceMatcher(None, old_normalized, new_normalized)
        result = []
        
        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag == 'equal':
                for i in range(i1, i2):
                    result.append((
                        old_lines[i][:width].ljust(width),
                        '  ',
                        new_lines[j1 + (i - i1)][:width].ljust(width)
                    ))
            elif tag == 'insert':
                for j in range(j1, j2):
                    result.append((
                        ' ' * width,
                        ' +',
                        new_lines[j][:width].ljust(width)
                    ))
            elif tag == 'delete':
                for i in range(i1, i2):
                    result.append((
                        old_lines[i][:width].ljust(width),
                        '- ',
                        ' ' * width
                    ))
            elif tag == 'replace':
                # 逐行配对显示
                for i in range(i1, i2):
                    j_offset = i - i1
                    if j1 + j_offset < j2:
                        result.append((
                            old_lines[i][:width].ljust(width),
                            '~ ',
                            new_lines[j1 + j_offset][:width].ljust(width)
                        ))
                    else:
                        result.append((
                            old_lines[i][:width].ljust(width),
                            '~ ',
                            ' ' * width
                        ))
                # 处理剩余的新行
                for j in range(j1 + (i2 - i1), j2):
                    result.append((
                        ' ' * width,
                        ' +',
                        new_lines[j][:width].ljust(width)
                    ))
        
        return result
    
    def char_diff(self, old_text: str, new_text: str) -> List[Tuple[DiffType, str]]:
        """
        字符级别的差异检测
        
        Args:
            old_text: 原文本
            new_text: 新文本
        
        Returns:
            List[Tuple[DiffType, str]]: (差异类型, 文本片段) 列表
        """
        old_normalized = self._normalize_text(old_text)
        new_normalized = self._normalize_text(new_text)
        
        matcher = difflib.SequenceMatcher(None, old_normalized, new_normalized)
        result = []
        
        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag == 'equal':
                result.append((DiffType.EQUAL, old_text[i1:i2]))
            elif tag == 'insert':
                result.append((DiffType.INSERT, new_text[j1:j2]))
            elif tag == 'delete':
                result.append((DiffType.DELETE, old_text[i1:i2]))
            elif tag == 'replace':
                result.append((DiffType.DELETE, old_text[i1:i2]))
                result.append((DiffType.INSERT, new_text[j1:j2]))
        
        return result
    
    def similarity(self, old_text: str, new_text: str) -> float:
        """
        计算两段文本的相似度
        
        Args:
            old_text: 原文本
            new_text: 新文本
        
        Returns:
            float: 相似度 (0.0 - 1.0)
        """
        old_normalized = self._normalize_text(old_text)
        new_normalized = self._normalize_text(new_text)
        
        return difflib.SequenceMatcher(None, old_normalized, new_normalized).ratio()
    
    def diff_stats(self, old_text: str, new_text: str) -> Dict:
        """
        获取差异统计信息
        
        Args:
            old_text: 原文本
            new_text: 新文本
        
        Returns:
            Dict: 差异统计字典
        """
        result = self.compare_lines(old_text, new_text)
        
        return {
            'old_lines': result.old_lines,
            'new_lines': result.new_lines,
            'added_lines': result.added_lines,
            'deleted_lines': result.deleted_lines,
            'changed_lines': result.changed_lines,
            'similarity': round(result.similarity * 100, 2),
            'is_identical': result.similarity == 1.0,
            'diff_percentage': round((1 - result.similarity) * 100, 2)
        }
    
    def find_matches(self, old_text: str, new_text: str, 
                     min_length: int = 3) -> List[Tuple[str, int, int]]:
        """
        查找两段文本中的公共子串
        
        Args:
            old_text: 原文本
            new_text: 新文本
            min_length: 最小子串长度
        
        Returns:
            List[Tuple[str, int, int]]: (子串, 原位置, 新位置)
        """
        matcher = difflib.SequenceMatcher(None, old_text, new_text)
        matches = []
        
        for match in matcher.get_matching_blocks():
            if match.size >= min_length:
                substring = old_text[match.a:match.a + match.size]
                matches.append((substring, match.a, match.b))
        
        return matches
    
    def merge_diff(self, base_text: str, diff_text: str, 
                   diff_format: str = 'unified') -> str:
        """
        应用差异补丁到基础文本
        
        Args:
            base_text: 基础文本
            diff_text: 差异文本（统一格式）
            diff_format: 差异格式（目前仅支持 'unified'）
        
        Returns:
            str: 合并后的文本
        
        Note:
            这是一个简化的实现，仅支持基本的统一格式差异应用
        """
        if diff_format != 'unified':
            raise ValueError(f"不支持的差异格式: {diff_format}")
        
        # 简化实现：解析差异并应用
        base_lines = base_text.splitlines(keepends=True)
        result_lines = []
        
        # 解析统一格式差异
        diff_lines = diff_text.splitlines()
        hunk_start = None
        hunk_changes = []
        
        for line in diff_lines:
            if line.startswith('@@'):
                # 处理上一个 hunk
                if hunk_changes:
                    result_lines.extend(_apply_hunk(base_lines, hunk_start, hunk_changes))
                    hunk_changes = []
                
                # 解析新的 hunk 头
                # 格式: @@ -start,count +start,count @@
                parts = line.split('@@')[1].strip().split()
                if parts:
                    old_info = parts[0]
                    hunk_start = int(old_info[1:].split(',')[0]) - 1  # 转为 0 索引
            elif line.startswith('+') and not line.startswith('+++'):
                hunk_changes.append(('insert', line[1:]))
            elif line.startswith('-') and not line.startswith('---'):
                hunk_changes.append(('delete', line[1:]))
            elif not line.startswith('\\'):
                hunk_changes.append(('equal', line))
        
        # 处理最后一个 hunk
        if hunk_changes:
            result_lines.extend(_apply_hunk(base_lines, hunk_start, hunk_changes))
        
        # 如果没有解析到任何差异，返回原文本
        if not result_lines:
            return base_text
        
        return ''.join(result_lines)


def _apply_hunk(base_lines: List[str], start: int, 
                changes: List[Tuple[str, str]]) -> List[str]:
    """应用单个差异块"""
    result = []
    for change_type, content in changes:
        if change_type != 'delete':
            if content and not content.endswith('\n'):
                result.append(content + '\n')
            else:
                result.append(content)
    return result


def compare_texts(old_text: str, new_text: str, 
                  ignore_case: bool = False,
                  ignore_whitespace: bool = False) -> DiffResult:
    """
    便捷函数：比较两段文本
    
    Args:
        old_text: 原文本
        new_text: 新文本
        ignore_case: 是否忽略大小写
        ignore_whitespace: 是否忽略空白字符
    
    Returns:
        DiffResult: 差异比较结果
    """
    utils = TextDiffUtils(ignore_case=ignore_case, 
                          ignore_whitespace=ignore_whitespace)
    return utils.compare_lines(old_text, new_text)


def get_unified_diff(old_text: str, new_text: str,
                    old_filename: str = "old",
                    new_filename: str = "new") -> str:
    """
    便捷函数：获取统一格式差异
    
    Args:
        old_text: 原文本
        new_text: 新文本
        old_filename: 原文件名
        new_filename: 新文件名
    
    Returns:
        str: 统一格式差异报告
    """
    utils = TextDiffUtils()
    return utils.unified_diff(old_text, new_text, old_filename, new_filename)


def get_similarity(old_text: str, new_text: str) -> float:
    """
    便捷函数：计算文本相似度
    
    Args:
        old_text: 原文本
        new_text: 新文本
    
    Returns:
        float: 相似度 (0.0 - 1.0)
    """
    utils = TextDiffUtils()
    return utils.similarity(old_text, new_text)


def format_diff_summary(result: DiffResult) -> str:
    """
    格式化差异摘要
    
    Args:
        result: 差异比较结果
    
    Returns:
        str: 格式化的摘要文本
    """
    lines = [
        "=== 差异摘要 ===",
        f"原文本行数: {result.old_lines}",
        f"新文本行数: {result.new_lines}",
        f"新增行数: {result.added_lines}",
        f"删除行数: {result.deleted_lines}",
        f"修改行数: {result.changed_lines}",
        f"相似度: {result.similarity:.2%}",
    ]
    return '\n'.join(lines)


def format_side_by_side(pairs: List[Tuple[str, str, str]], 
                       title: str = "并排对比") -> str:
    """
    格式化并排对比视图
    
    Args:
        pairs: 并排对比数据
        title: 标题
    
    Returns:
        str: 格式化的对比文本
    """
    if not pairs:
        return f"=== {title} ===\n无差异"
    
    # 计算宽度
    max_left = max(len(p[0]) for p in pairs)
    max_right = max(len(p[2]) for p in pairs)
    
    lines = [
        f"=== {title} ===",
        f"{'原文本':<{max_left}}  |  {'新文本':<{max_right}}",
        f"{'-' * max_left}  |  {'-' * max_right}",
    ]
    
    for left, sep, right in pairs:
        left_display = left[:max_left].ljust(max_left)
        right_display = right[:max_right].ljust(max_right)
        lines.append(f"{left_display} {sep} {right_display}")
    
    return '\n'.join(lines)


if __name__ == "__main__":
    # 简单演示
    old = """Hello World
This is the original text.
Line 3
Line 4
Line 5"""
    
    new = """Hello World
This is the modified text.
Line 3
Line 4 new content
Line 5
Line 6 added"""
    
    print("=== 文本差异比较演示 ===\n")
    
    utils = TextDiffUtils()
    
    # 比较差异
    result = utils.compare_lines(old, new)
    print(format_diff_summary(result))
    
    # 统一格式差异
    print("\n=== 统一格式差异 ===")
    print(utils.unified_diff(old, new, "original.txt", "modified.txt"))
    
    # 并排对比
    print("\n=== 并排对比 ===")
    pairs = utils.side_by_side(old, new)
    print(format_side_by_side(pairs))
    
    # 字符级差异
    print("\n=== 字符级差异 ===")
    char_diffs = utils.char_diff("Hello World", "Hello New World")
    for diff_type, text in char_diffs:
        symbol = {'equal': '=', 'insert': '+', 'delete': '-', 'replace': '~'}[diff_type.value]
        print(f"  {symbol} {text!r}")
    
    # 差异统计
    print("\n=== 差异统计 ===")
    stats = utils.diff_stats(old, new)
    for key, value in stats.items():
        print(f"  {key}: {value}")
"""
diff_utils - 文本差异比较工具模块

提供文本差异比较、相似度计算、差异高亮等功能。
零外部依赖，全部使用Python标准库实现。

主要功能：
- 行级差异比较（LCS算法）
- 字符级差异比较
- 相似度计算（Levenshtein、Jaccard、Cosine等）
- 差异高亮输出（终端颜色、HTML）
- 合并冲突检测
- 变更统计
- 补丁生成与应用

作者: AllToolkit
日期: 2026-04-13
"""

from typing import List, Tuple, Dict, Optional, Union, Callable
from dataclasses import dataclass, field
from enum import Enum
import difflib
import re
from collections import Counter
import math


class DiffType(Enum):
    """差异类型枚举"""
    EQUAL = "equal"
    INSERT = "insert"
    DELETE = "delete"
    REPLACE = "replace"


@dataclass
class DiffOp:
    """差异操作数据类"""
    type: DiffType
    old_start: int
    old_end: int
    new_start: int
    new_end: int
    old_content: List[str] = field(default_factory=list)
    new_content: List[str] = field(default_factory=list)


@dataclass
class DiffResult:
    """差异比较结果"""
    ops: List[DiffOp]
    similarity: float
    additions: int
    deletions: int
    changes: int
    unchanged: int


@dataclass
class ConflictRegion:
    """合并冲突区域"""
    start_line: int
    end_line: int
    our_content: List[str]
    their_content: List[str]
    base_content: Optional[List[str]] = None


# ==================== 核心差异比较算法 ====================

def diff_lines(old_text: str, new_text: str, 
               line_separator: str = "\n") -> List[Tuple[DiffType, List[str]]]:
    """
    行级差异比较
    
    Args:
        old_text: 原始文本
        new_text: 新文本
        line_separator: 行分隔符
        
    Returns:
        差异操作列表，每个元素为 (操作类型, 内容行列表)
    """
    old_lines = old_text.split(line_separator) if old_text else []
    new_lines = new_text.split(line_separator) if new_text else []
    
    matcher = difflib.SequenceMatcher(None, old_lines, new_lines)
    result = []
    
    for op, i1, i2, j1, j2 in matcher.get_opcodes():
        if op == 'equal':
            result.append((DiffType.EQUAL, old_lines[i1:i2]))
        elif op == 'insert':
            result.append((DiffType.INSERT, new_lines[j1:j2]))
        elif op == 'delete':
            result.append((DiffType.DELETE, old_lines[i1:i2]))
        elif op == 'replace':
            result.append((DiffType.DELETE, old_lines[i1:i2]))
            result.append((DiffType.INSERT, new_lines[j1:j2]))
    
    return result


def diff_chars(old_text: str, new_text: str) -> List[Tuple[DiffType, str]]:
    """
    字符级差异比较
    
    Args:
        old_text: 原始文本
        new_text: 新文本
        
    Returns:
        差异操作列表，每个元素为 (操作类型, 字符串)
    """
    matcher = difflib.SequenceMatcher(None, old_text, new_text)
    result = []
    
    for op, i1, i2, j1, j2 in matcher.get_opcodes():
        if op == 'equal':
            result.append((DiffType.EQUAL, old_text[i1:i2]))
        elif op == 'insert':
            result.append((DiffType.INSERT, new_text[j1:j2]))
        elif op == 'delete':
            result.append((DiffType.DELETE, old_text[i1:i2]))
        elif op == 'replace':
            result.append((DiffType.DELETE, old_text[i1:i2]))
            result.append((DiffType.INSERT, new_text[j1:j2]))
    
    return result


def diff_words(old_text: str, new_text: str) -> List[Tuple[DiffType, List[str]]]:
    """
    词级差异比较
    
    Args:
        old_text: 原始文本
        new_text: 新文本
        
    Returns:
        差异操作列表，每个元素为 (操作类型, 词列表)
    """
    # 使用正则分词，保留空白
    pattern = r'(\S+|\s+)'
    old_words = re.findall(pattern, old_text)
    new_words = re.findall(pattern, new_text)
    
    matcher = difflib.SequenceMatcher(None, old_words, new_words)
    result = []
    
    for op, i1, i2, j1, j2 in matcher.get_opcodes():
        if op == 'equal':
            result.append((DiffType.EQUAL, old_words[i1:i2]))
        elif op == 'insert':
            result.append((DiffType.INSERT, new_words[j1:j2]))
        elif op == 'delete':
            result.append((DiffType.DELETE, old_words[i1:i2]))
        elif op == 'replace':
            result.append((DiffType.DELETE, old_words[i1:i2]))
            result.append((DiffType.INSERT, new_words[j1:j2]))
    
    return result


def compute_diff_result(old_text: str, new_text: str, 
                        level: str = "line") -> DiffResult:
    """
    计算完整的差异比较结果
    
    Args:
        old_text: 原始文本
        new_text: 新文本
        level: 比较级别 ("line", "char", "word")
        
    Returns:
        DiffResult 对象，包含完整的差异信息
    """
    if level == "line":
        diff_ops = diff_lines(old_text, new_text)
        old_units = old_text.split("\n") if old_text else []
        new_units = new_text.split("\n") if new_text else []
    elif level == "char":
        diff_ops = [(t, list(c) if isinstance(c, str) else c) 
                    for t, c in diff_chars(old_text, new_text)]
        old_units = list(old_text)
        new_units = list(new_text)
    elif level == "word":
        diff_ops = diff_words(old_text, new_text)
        pattern = r'(\S+|\s+)'
        old_units = re.findall(pattern, old_text)
        new_units = re.findall(pattern, new_text)
    else:
        raise ValueError(f"Unknown level: {level}")
    
    # 统计变更
    additions = sum(len(content) for op_type, content in diff_ops 
                    if op_type == DiffType.INSERT)
    deletions = sum(len(content) for op_type, content in diff_ops 
                    if op_type == DiffType.DELETE)
    unchanged = sum(len(content) for op_type, content in diff_ops 
                    if op_type == DiffType.EQUAL)
    
    total_old = len(old_units)
    total_new = len(new_units)
    total = max(total_old, total_new)
    
    similarity = unchanged / total if total > 0 else 1.0
    
    # 构建 DiffOp 列表
    ops = []
    old_idx = 0
    new_idx = 0
    
    for op_type, content in diff_ops:
        if op_type == DiffType.EQUAL:
            ops.append(DiffOp(
                type=op_type,
                old_start=old_idx,
                old_end=old_idx + len(content),
                new_start=new_idx,
                new_end=new_idx + len(content),
                old_content=content if isinstance(content, list) else list(content),
                new_content=content if isinstance(content, list) else list(content)
            ))
            old_idx += len(content)
            new_idx += len(content)
        elif op_type == DiffType.DELETE:
            old_end = old_idx + len(content)
            ops.append(DiffOp(
                type=op_type,
                old_start=old_idx,
                old_end=old_end,
                new_start=new_idx,
                new_end=new_idx,
                old_content=content if isinstance(content, list) else list(content),
                new_content=[]
            ))
            old_idx = old_end
        elif op_type == DiffType.INSERT:
            new_end = new_idx + len(content)
            ops.append(DiffOp(
                type=op_type,
                old_start=old_idx,
                old_end=old_idx,
                new_start=new_idx,
                new_end=new_end,
                old_content=[],
                new_content=content if isinstance(content, list) else list(content)
            ))
            new_idx = new_end
    
    return DiffResult(
        ops=ops,
        similarity=similarity,
        additions=additions,
        deletions=deletions,
        changes=additions + deletions,
        unchanged=unchanged
    )


# ==================== 相似度计算 ====================

def levenshtein_distance(s1: str, s2: str) -> int:
    """
    计算Levenshtein编辑距离
    
    Args:
        s1: 字符串1
        s2: 字符串2
        
    Returns:
        编辑距离
    """
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    
    if len(s2) == 0:
        return len(s1)
    
    previous_row = range(len(s2) + 1)
    
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    
    return previous_row[-1]


def levenshtein_similarity(s1: str, s2: str) -> float:
    """
    基于Levenshtein距离的相似度 (0-1)
    
    Args:
        s1: 字符串1
        s2: 字符串2
        
    Returns:
        相似度 (0-1)
    """
    if not s1 and not s2:
        return 1.0
    
    distance = levenshtein_distance(s1, s2)
    max_len = max(len(s1), len(s2))
    return 1.0 - (distance / max_len) if max_len > 0 else 1.0


def jaccard_similarity(s1: str, s2: str, ngram: int = 2) -> float:
    """
    Jaccard相似度（基于n-gram）
    
    Args:
        s1: 字符串1
        s2: 字符串2
        ngram: n-gram大小，默认2（bigram）
        
    Returns:
        相似度 (0-1)
    """
    def get_ngrams(s: str, n: int) -> set:
        return set(s[i:i+n] for i in range(len(s) - n + 1))
    
    if len(s1) < ngram or len(s2) < ngram:
        return 1.0 if s1 == s2 else 0.0
    
    set1 = get_ngrams(s1, ngram)
    set2 = get_ngrams(s2, ngram)
    
    intersection = len(set1 & set2)
    union = len(set1 | set2)
    
    return intersection / union if union > 0 else 0.0


def cosine_similarity(s1: str, s2: str) -> float:
    """
    余弦相似度（基于字符频率）
    
    Args:
        s1: 字符串1
        s2: 字符串2
        
    Returns:
        相似度 (0-1)
    """
    if not s1 and not s2:
        return 1.0
    
    counter1 = Counter(s1)
    counter2 = Counter(s2)
    
    all_chars = set(counter1.keys()) | set(counter2.keys())
    
    dot_product = sum(counter1.get(c, 0) * counter2.get(c, 0) for c in all_chars)
    magnitude1 = math.sqrt(sum(v ** 2 for v in counter1.values()))
    magnitude2 = math.sqrt(sum(v ** 2 for v in counter2.values()))
    
    if magnitude1 == 0 or magnitude2 == 0:
        return 0.0
    
    return dot_product / (magnitude1 * magnitude2)


def damerau_levenshtein_distance(s1: str, s2: str) -> int:
    """
    Damerau-Levenshtein距离（支持相邻字符交换）
    
    Args:
        s1: 字符串1
        s2: 字符串2
        
    Returns:
        编辑距离
    """
    d = {}
    lenstr1 = len(s1)
    lenstr2 = len(s2)
    
    for i in range(-1, lenstr1 + 1):
        d[(i, -1)] = i + 1
    for j in range(-1, lenstr2 + 1):
        d[(-1, j)] = j + 1
    
    for i in range(lenstr1):
        for j in range(lenstr2):
            if s1[i] == s2[j]:
                cost = 0
            else:
                cost = 1
            d[(i, j)] = min(
                d[(i - 1, j)] + 1,  # 删除
                d[(i, j - 1)] + 1,  # 插入
                d[(i - 1, j - 1)] + cost  # 替换
            )
            if i and j and s1[i] == s2[j - 1] and s1[i - 1] == s2[j]:
                d[(i, j)] = min(d[(i, j)], d[i - 2, j - 2] + 1)  # 交换
    
    return d[(lenstr1 - 1, lenstr2 - 1)]


def similarity_score(s1: str, s2: str, method: str = "levenshtein") -> float:
    """
    计算相似度得分
    
    Args:
        s1: 字符串1
        s2: 字符串2
        method: 计算方法 ("levenshtein", "jaccard", "cosine", "damerau")
        
    Returns:
        相似度 (0-1)
    """
    methods = {
        "levenshtein": levenshtein_similarity,
        "jaccard": jaccard_similarity,
        "cosine": cosine_similarity,
    }
    
    if method == "damerau":
        if not s1 and not s2:
            return 1.0
        distance = damerau_levenshtein_distance(s1, s2)
        max_len = max(len(s1), len(s2))
        return 1.0 - (distance / max_len) if max_len > 0 else 1.0
    
    if method in methods:
        return methods[method](s1, s2)
    
    raise ValueError(f"Unknown method: {method}")


# ==================== 差异格式化输出 ====================

def format_diff_unified(old_text: str, new_text: str, 
                        context_lines: int = 3,
                        from_file: str = "a", 
                        to_file: str = "b") -> str:
    """
    生成unified diff格式输出
    
    Args:
        old_text: 原始文本
        new_text: 新文本
        context_lines: 上下文行数
        from_file: 原始文件名
        to_file: 新文件名
        
    Returns:
        unified diff格式的字符串
    """
    old_lines = old_text.splitlines(keepends=True)
    new_lines = new_text.splitlines(keepends=True)
    
    diff = difflib.unified_diff(
        old_lines, new_lines,
        fromfile=from_file,
        tofile=to_file,
        lineterm="",
        n=context_lines
    )
    
    return "".join(diff)


def format_diff_context(old_text: str, new_text: str,
                        context_lines: int = 3,
                        from_file: str = "a",
                        to_file: str = "b") -> str:
    """
    生成context diff格式输出
    
    Args:
        old_text: 原始文本
        new_text: 新文本
        context_lines: 上下文行数
        from_file: 原始文件名
        to_file: 新文件名
        
    Returns:
        context diff格式的字符串
    """
    old_lines = old_text.splitlines(keepends=True)
    new_lines = new_text.splitlines(keepends=True)
    
    diff = difflib.context_diff(
        old_lines, new_lines,
        fromfile=from_file,
        tofile=to_file,
        lineterm="",
        n=context_lines
    )
    
    return "".join(diff)


# 终端颜色代码
class Colors:
    """终端颜色常量"""
    RESET = "\033[0m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    BOLD = "\033[1m"
    DIM = "\033[2m"


def format_diff_colored(old_text: str, new_text: str,
                        level: str = "line") -> str:
    """
    生成带颜色的高亮差异输出（适用于终端）
    
    Args:
        old_text: 原始文本
        new_text: 新文本
        level: 比较级别 ("line", "char")
        
    Returns:
        带ANSI颜色代码的差异文本
    """
    if level == "line":
        diff_ops = diff_lines(old_text, new_text)
        result_lines = []
        
        for op_type, lines in diff_ops:
            if op_type == DiffType.EQUAL:
                for line in lines:
                    result_lines.append(f"{Colors.DIM}  {line}{Colors.RESET}")
            elif op_type == DiffType.DELETE:
                for line in lines:
                    result_lines.append(f"{Colors.RED}- {line}{Colors.RESET}")
            elif op_type == DiffType.INSERT:
                for line in lines:
                    result_lines.append(f"{Colors.GREEN}+ {line}{Colors.RESET}")
        
        return "\n".join(result_lines)
    
    elif level == "char":
        diff_ops = diff_chars(old_text, new_text)
        result_parts = []
        
        for op_type, text in diff_ops:
            if op_type == DiffType.EQUAL:
                result_parts.append(text)
            elif op_type == DiffType.DELETE:
                result_parts.append(f"{Colors.RED}{Colors.BOLD}{text}{Colors.RESET}")
            elif op_type == DiffType.INSERT:
                result_parts.append(f"{Colors.GREEN}{Colors.BOLD}{text}{Colors.RESET}")
        
        return "".join(result_parts)
    
    raise ValueError(f"Unknown level: {level}")


def format_diff_html(old_text: str, new_text: str,
                     level: str = "line") -> str:
    """
    生成HTML格式的差异输出
    
    Args:
        old_text: 原始文本
        new_text: 新文本
        level: 比较级别 ("line", "char")
        
    Returns:
        HTML格式的差异文本
    """
    html_template = """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Diff Result</title>
    <style>
        body {{ font-family: monospace; padding: 20px; background: #f5f5f5; }}
        .diff-container {{ background: white; border-radius: 8px; padding: 15px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .diff-line {{ padding: 2px 5px; white-space: pre-wrap; word-break: break-all; }}
        .equal {{ color: #666; }}
        .delete {{ background: #ffecec; color: #c00; }}
        .insert {{ background: #eaffea; color: #080; }}
        .line-num {{ color: #999; margin-right: 10px; user-select: none; }}
        .stats {{ margin-bottom: 15px; padding: 10px; background: #f0f0f0; border-radius: 4px; }}
        .stat-add {{ color: #080; }}
        .stat-del {{ color: #c00; }}
    </style>
</head>
<body>
    <div class="diff-container">
        <div class="stats">
            <span class="stat-add">+{additions} additions</span> |
            <span class="stat-del">-{deletions} deletions</span> |
            Similarity: {similarity:.1%}
        </div>
        <div class="diff-content">
{content}
        </div>
    </div>
</body>
</html>"""
    
    result = compute_diff_result(old_text, new_text, level)
    
    if level == "line":
        diff_ops = diff_lines(old_text, new_text)
        content_lines = []
        
        for op_type, lines in diff_ops:
            css_class = {
                DiffType.EQUAL: "equal",
                DiffType.DELETE: "delete",
                DiffType.INSERT: "insert"
            }.get(op_type, "equal")
            
            for line in lines:
                escaped = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                prefix = "-" if op_type == DiffType.DELETE else ("+" if op_type == DiffType.INSERT else " ")
                content_lines.append(f'            <div class="diff-line {css_class}">{prefix} {escaped}</div>')
        
        content = "\n".join(content_lines)
    
    elif level == "char":
        diff_ops = diff_chars(old_text, new_text)
        content_parts = []
        
        for op_type, text in diff_ops:
            escaped = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            if op_type == DiffType.EQUAL:
                content_parts.append(escaped)
            elif op_type == DiffType.DELETE:
                content_parts.append(f'<span class="delete">{escaped}</span>')
            elif op_type == DiffType.INSERT:
                content_parts.append(f'<span class="insert">{escaped}</span>')
        
        content = f'            <div class="diff-line">{"".join(content_parts)}</div>'
    
    else:
        raise ValueError(f"Unknown level: {level}")
    
    return html_template.format(
        additions=result.additions,
        deletions=result.deletions,
        similarity=result.similarity,
        content=content
    )


# ==================== 合并冲突检测 ====================

def detect_merge_conflicts(base: str, ours: str, theirs: str,
                           line_separator: str = "\n") -> List[ConflictRegion]:
    """
    检测三方合并冲突
    
    Args:
        base: 基础版本
        ours: 我们的版本
        theirs: 他们的版本
        line_separator: 行分隔符
        
    Returns:
        冲突区域列表
    """
    base_lines = base.split(line_separator) if base else []
    our_lines = ours.split(line_separator) if ours else []
    their_lines = theirs.split(line_separator) if theirs else []
    
    # 计算base与ours的差异
    our_diff = list(difflib.SequenceMatcher(None, base_lines, our_lines).get_opcodes())
    
    # 计算base与theirs的差异
    their_diff = list(difflib.SequenceMatcher(None, base_lines, their_lines).get_opcodes())
    
    conflicts = []
    
    # 找出双方都修改的区域
    for our_op in our_diff:
        if our_op[0] in ('replace', 'insert', 'delete'):
            our_base_start, our_base_end = our_op[1], our_op[2]
            
            for their_op in their_diff:
                if their_op[0] in ('replace', 'insert', 'delete'):
                    their_base_start, their_base_end = their_op[1], their_op[2]
                    
                    # 检查是否有重叠
                    if our_base_start < their_base_end and our_base_end > their_base_start:
                        # 检查内容是否不同
                        our_content = our_lines[our_op[3]:our_op[4]] if our_op[0] != 'delete' else []
                        their_content = their_lines[their_op[3]:their_op[4]] if their_op[0] != 'delete' else []
                        
                        if our_content != their_content:
                            # 找出冲突范围
                            conflict_start = min(our_base_start, their_base_start)
                            conflict_end = max(our_base_end, their_base_end)
                            
                            # 获取base内容
                            base_content = base_lines[conflict_start:conflict_end] if conflict_end > conflict_start else []
                            
                            # 避免重复添加相同的冲突
                            is_duplicate = False
                            for existing in conflicts:
                                if (existing.start_line == conflict_start and 
                                    existing.end_line == conflict_end):
                                    is_duplicate = True
                                    break
                            
                            if not is_duplicate:
                                conflicts.append(ConflictRegion(
                                    start_line=conflict_start,
                                    end_line=conflict_end,
                                    our_content=our_content,
                                    their_content=their_content,
                                    base_content=base_content
                                ))
    
    return conflicts


def format_conflict_markers(conflict: ConflictRegion) -> str:
    """
    生成冲突标记格式的文本
    
    Args:
        conflict: 冲突区域
        
    Returns:
        带冲突标记的文本
    """
    lines = []
    lines.append(f"<<<<<<< OURS")
    lines.extend(conflict.our_content)
    lines.append("=======")
    lines.extend(conflict.their_content)
    lines.append(">>>>>>> THEIRS")
    return "\n".join(lines)


# ==================== 补丁生成与应用 ====================

def generate_patch(old_text: str, new_text: str,
                   from_file: str = "a/file",
                   to_file: str = "b/file") -> str:
    """
    生成补丁文本
    
    Args:
        old_text: 原始文本
        new_text: 新文本
        from_file: 原始文件路径
        to_file: 新文件路径
        
    Returns:
        可应用的补丁文本
    """
    return format_diff_unified(old_text, new_text, 
                               context_lines=3,
                               from_file=from_file,
                               to_file=to_file)


def apply_patch(original_text: str, patch_text: str) -> str:
    """
    应用补丁到原始文本
    
    Args:
        original_text: 原始文本
        patch_text: 补丁文本
        
    Returns:
        应用补丁后的文本
    """
    lines = original_text.splitlines(True)
    
    # 解析补丁
    patch_lines = patch_text.splitlines()
    changes = []
    i = 0
    
    while i < len(patch_lines):
        line = patch_lines[i]
        
        # 解析hunk header: @@ -start,count +start,count @@
        if line.startswith("@@"):
            match = re.match(r"@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@", line)
            if match:
                old_start = int(match.group(1))
                old_count = int(match.group(2) or 1)
                new_start = int(match.group(3))
                new_count = int(match.group(4) or 1)
                
                i += 1
                old_lines = []
                new_lines = []
                
                # 收集变更
                while i < len(patch_lines) and not patch_lines[i].startswith("@@"):
                    pl = patch_lines[i]
                    if pl.startswith(" "):
                        old_lines.append(pl[1:])
                        new_lines.append(pl[1:])
                    elif pl.startswith("-"):
                        old_lines.append(pl[1:])
                    elif pl.startswith("+"):
                        new_lines.append(pl[1:])
                    i += 1
                
                changes.append({
                    'old_start': old_start,
                    'old_lines': old_lines,
                    'new_lines': new_lines
                })
            else:
                i += 1
        else:
            i += 1
    
    # 应用变更（从后向前，避免行号偏移）
    result_lines = list(lines)
    for change in reversed(changes):
        start = change['old_start'] - 1  # 转为0索引
        result_lines[start:start + len(change['old_lines'])] = change['new_lines']
    
    return "".join(result_lines)


# ==================== 差异统计 ====================

def diff_statistics(old_text: str, new_text: str) -> Dict:
    """
    生成详细的差异统计信息
    
    Args:
        old_text: 原始文本
        new_text: 新文本
        
    Returns:
        统计信息字典
    """
    result = compute_diff_result(old_text, new_text, "line")
    
    old_lines = old_text.split("\n") if old_text else []
    new_lines = new_text.split("\n") if new_text else []
    
    # 找出变更的行号
    added_lines = []
    deleted_lines = []
    diff_ops = diff_lines(old_text, new_text)
    
    old_line_num = 0
    new_line_num = 0
    
    for op_type, lines in diff_ops:
        if op_type == DiffType.EQUAL:
            old_line_num += len(lines)
            new_line_num += len(lines)
        elif op_type == DiffType.DELETE:
            for _ in lines:
                deleted_lines.append(old_line_num + 1)
                old_line_num += 1
        elif op_type == DiffType.INSERT:
            for _ in lines:
                added_lines.append(new_line_num + 1)
                new_line_num += 1
    
    return {
        'old_lines': len(old_lines),
        'new_lines': len(new_lines),
        'additions': result.additions,
        'deletions': result.deletions,
        'changes': result.changes,
        'unchanged': result.unchanged,
        'similarity': result.similarity,
        'added_line_numbers': added_lines,
        'deleted_line_numbers': deleted_lines,
        'similarity_levenshtein': levenshtein_similarity(old_text, new_text),
        'similarity_jaccard': jaccard_similarity(old_text, new_text),
        'similarity_cosine': cosine_similarity(old_text, new_text),
    }


# ==================== 实用函数 ====================

def find_longest_common_subsequence(s1: str, s2: str) -> str:
    """
    找出最长公共子序列
    
    Args:
        s1: 字符串1
        s2: 字符串2
        
    Returns:
        最长公共子序列
    """
    matcher = difflib.SequenceMatcher(None, s1, s2)
    match = matcher.find_longest_match(0, len(s1), 0, len(s2))
    return s1[match.a:match.a + match.size]


def find_similar_strings(target: str, candidates: List[str], 
                         threshold: float = 0.6,
                         method: str = "levenshtein") -> List[Tuple[str, float]]:
    """
    在候选列表中找出与目标相似的字符串
    
    Args:
        target: 目标字符串
        candidates: 候选字符串列表
        threshold: 相似度阈值
        method: 相似度计算方法
        
    Returns:
        (字符串, 相似度) 元组列表，按相似度降序排列
    """
    results = []
    for candidate in candidates:
        sim = similarity_score(target, candidate, method)
        if sim >= threshold:
            results.append((candidate, sim))
    
    return sorted(results, key=lambda x: x[1], reverse=True)


def highlight_differences(text1: str, text2: str,
                         marker_start: str = "[[",
                         marker_end: str = "]]") -> Tuple[str, str]:
    """
    高亮两个文本之间的差异
    
    Args:
        text1: 文本1
        text2: 文本2
        marker_start: 差异开始标记
        marker_end: 差异结束标记
        
    Returns:
        (标记后的文本1, 标记后的文本2)
    """
    diff_ops = diff_chars(text1, text2)
    
    result1_parts = []
    result2_parts = []
    
    for op_type, text in diff_ops:
        if op_type == DiffType.EQUAL:
            result1_parts.append(text)
            result2_parts.append(text)
        elif op_type == DiffType.DELETE:
            result1_parts.append(f"{marker_start}{text}{marker_end}")
        elif op_type == DiffType.INSERT:
            result2_parts.append(f"{marker_start}{text}{marker_end}")
    
    return "".join(result1_parts), "".join(result2_parts)


def get_change_summary(old_text: str, new_text: str) -> str:
    """
    生成人类可读的变更摘要
    
    Args:
        old_text: 原始文本
        new_text: 新文本
        
    Returns:
        变更摘要字符串
    """
    stats = diff_statistics(old_text, new_text)
    
    parts = []
    
    if stats['additions'] > 0:
        parts.append(f"添加 {stats['additions']} 行")
    
    if stats['deletions'] > 0:
        parts.append(f"删除 {stats['deletions']} 行")
    
    if not parts:
        return "无变更"
    
    summary = ", ".join(parts)
    summary += f", 相似度 {stats['similarity']:.1%}"
    
    return summary
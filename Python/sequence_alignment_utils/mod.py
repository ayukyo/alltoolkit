"""
Sequence Alignment Utils - 序列比对工具

提供多种序列比对算法，包括：
- Needleman-Wunsch 全局比对
- Smith-Waterman 局部比对
- 编辑距离计算
- 序列相似度计算
- 比对结果可视化

零外部依赖，纯 Python 实现。
"""

from typing import Tuple, List, Optional, Callable, Dict, Any
from enum import Enum


class AlignmentType(Enum):
    """比对类型"""
    GLOBAL = "global"      # 全局比对 (Needleman-Wunsch)
    LOCAL = "local"         # 局部比对 (Smith-Waterman)


class ScoringMatrix:
    """评分矩阵，用于蛋白质/DNA序列比对"""
    
    # DNA 简单评分矩阵
    DNA_SIMPLE = {
        ('A', 'A'): 1, ('A', 'T'): -1, ('A', 'G'): -1, ('A', 'C'): -1,
        ('T', 'A'): -1, ('T', 'T'): 1, ('T', 'G'): -1, ('T', 'C'): -1,
        ('G', 'A'): -1, ('G', 'T'): -1, ('G', 'G'): 1, ('G', 'C'): -1,
        ('C', 'A'): -1, ('C', 'T'): -1, ('C', 'G'): -1, ('C', 'C'): 1,
    }
    
    # BLOSUM62 简化版 (常见氨基酸)
    BLOSUM62_SIMPLE = {
        ('A', 'A'): 4, ('A', 'R'): -1, ('A', 'N'): -2, ('A', 'D'): -2,
        ('R', 'R'): 5, ('R', 'A'): -1, ('R', 'N'): 0, ('R', 'D'): -2,
        ('N', 'N'): 6, ('N', 'A'): -2, ('N', 'R'): 0, ('N', 'D'): 1,
        ('D', 'D'): 6, ('D', 'A'): -2, ('D', 'R'): -2, ('D', 'N'): 1,
        ('C', 'C'): 9, ('C', 'A'): 0, ('C', 'R'): -3, ('C', 'N'): -3,
        ('Q', 'Q'): 5, ('Q', 'A'): -1, ('Q', 'R'): 1, ('Q', 'N'): 0,
        ('E', 'E'): 5, ('E', 'A'): -1, ('E', 'R'): 0, ('E', 'N'): 0,
        ('G', 'G'): 6, ('G', 'A'): 0, ('G', 'R'): -2, ('G', 'N'): 0,
        ('H', 'H'): 8, ('H', 'A'): -2, ('H', 'R'): 0, ('H', 'N'): 1,
        ('I', 'I'): 4, ('I', 'A'): -1, ('I', 'R'): -3, ('I', 'N'): -3,
        ('L', 'L'): 4, ('L', 'A'): -1, ('L', 'R'): -2, ('L', 'N'): -3,
        ('K', 'K'): 5, ('K', 'A'): -1, ('K', 'R'): 2, ('K', 'N'): 0,
        ('M', 'M'): 5, ('M', 'A'): -1, ('M', 'R'): -1, ('M', 'N'): -2,
        ('F', 'F'): 6, ('F', 'A'): -2, ('F', 'R'): -3, ('F', 'N'): -3,
        ('P', 'P'): 7, ('P', 'A'): -1, ('P', 'R'): -2, ('P', 'N'): -2,
        ('S', 'S'): 4, ('S', 'A'): 1, ('S', 'R'): -1, ('S', 'N'): 1,
        ('T', 'T'): 5, ('T', 'A'): 0, ('T', 'R'): -1, ('T', 'N'): 0,
        ('W', 'W'): 11, ('W', 'A'): -3, ('W', 'R'): -3, ('W', 'N'): -4,
        ('Y', 'Y'): 7, ('Y', 'A'): -2, ('Y', 'R'): -2, ('Y', 'N'): -2,
        ('V', 'V'): 4, ('V', 'A'): 0, ('V', 'R'): -3, ('V', 'N'): -3,
    }
    
    @classmethod
    def get_score(cls, char1: str, char2: str, matrix: Optional[Dict] = None) -> int:
        """获取两个字符的比对得分"""
        if matrix is None:
            # 默认使用简单匹配/不匹配
            return 1 if char1 == char2 else -1
        
        key = (char1.upper(), char2.upper())
        if key in matrix:
            return matrix[key]
        # 反向查找
        key_rev = (char2.upper(), char1.upper())
        if key_rev in matrix:
            return matrix[key_rev]
        # 默认不匹配惩罚
        return -1


class AlignmentResult:
    """比对结果"""
    
    def __init__(
        self,
        seq1_aligned: str,
        seq2_aligned: str,
        score: float,
        identity: float,
        similarity: float,
        gaps: int,
        alignment_type: AlignmentType,
        matrix: Optional[List[List[float]]] = None
    ):
        self.seq1_aligned = seq1_aligned
        self.seq2_aligned = seq2_aligned
        self.score = score
        self.identity = identity
        self.similarity = similarity
        self.gaps = gaps
        self.alignment_type = alignment_type
        self.matrix = matrix
    
    def __repr__(self) -> str:
        return (
            f"AlignmentResult(score={self.score}, identity={self.identity:.1%}, "
            f"gaps={self.gaps}, type={self.alignment_type.value})"
        )
    
    def format_alignment(self, width: int = 60) -> str:
        """
        格式化比对结果为可读字符串
        
        Args:
            width: 每行显示的字符数
            
        Returns:
            格式化的比对字符串
        """
        lines = []
        lines.append(f"Score: {self.score}")
        lines.append(f"Identity: {self.identity:.1%} ({int(self.identity * len(self.seq1_aligned.replace('-', '')))}/{len(self.seq1_aligned.replace('-', ''))})")
        lines.append(f"Gaps: {self.gaps}")
        lines.append("")
        
        # 分块显示
        for i in range(0, len(self.seq1_aligned), width):
            chunk1 = self.seq1_aligned[i:i+width]
            chunk2 = self.seq2_aligned[i:i+width]
            
            # 构建匹配行
            match_line = ""
            for c1, c2 in zip(chunk1, chunk2):
                if c1 == '-' or c2 == '-':
                    match_line += ' '
                elif c1 == c2:
                    match_line += '|'
                else:
                    match_line += '.'
            
            # 添加位置标记
            pos1 = i + 1 - chunk1[:i].count('-') if i > 0 else 1
            pos2 = i + 1 - chunk2[:i].count('-') if i > 0 else 1
            
            lines.append(f"Seq1: {chunk1}")
            lines.append(f"      {match_line}")
            lines.append(f"Seq2: {chunk2}")
            lines.append("")
        
        return '\n'.join(lines)


def needleman_wunsch(
    seq1: str,
    seq2: str,
    match_score: int = 1,
    mismatch_score: int = -1,
    gap_penalty: int = -2,
    scoring_matrix: Optional[Dict] = None
) -> AlignmentResult:
    """
    Needleman-Wunsch 全局序列比对算法
    
    Args:
        seq1: 第一条序列
        seq2: 第二条序列
        match_score: 匹配得分
        mismatch_score: 不匹配得分
        gap_penalty: 空位惩罚
        scoring_matrix: 自定义评分矩阵
        
    Returns:
        AlignmentResult 比对结果
    """
    m, n = len(seq1), len(seq2)
    
    # 初始化得分矩阵
    score_matrix = [[0.0] * (n + 1) for _ in range(m + 1)]
    
    # 初始化第一行和第一列
    for i in range(m + 1):
        score_matrix[i][0] = i * gap_penalty
    for j in range(n + 1):
        score_matrix[0][j] = j * gap_penalty
    
    # 填充得分矩阵
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if scoring_matrix:
                match = score_matrix[i-1][j-1] + ScoringMatrix.get_score(
                    seq1[i-1], seq2[j-1], scoring_matrix
                )
            else:
                score = match_score if seq1[i-1] == seq2[j-1] else mismatch_score
                match = score_matrix[i-1][j-1] + score
            
            delete = score_matrix[i-1][j] + gap_penalty
            insert = score_matrix[i][j-1] + gap_penalty
            
            score_matrix[i][j] = max(match, delete, insert)
    
    # 回溯构建比对
    aligned1, aligned2 = [], []
    i, j = m, n
    
    while i > 0 or j > 0:
        if i > 0 and j > 0:
            if scoring_matrix:
                score = ScoringMatrix.get_score(seq1[i-1], seq2[j-1], scoring_matrix)
            else:
                score = match_score if seq1[i-1] == seq2[j-1] else mismatch_score
            
            if score_matrix[i][j] == score_matrix[i-1][j-1] + score:
                aligned1.append(seq1[i-1])
                aligned2.append(seq2[j-1])
                i -= 1
                j -= 1
                continue
        
        if i > 0 and score_matrix[i][j] == score_matrix[i-1][j] + gap_penalty:
            aligned1.append(seq1[i-1])
            aligned2.append('-')
            i -= 1
        elif j > 0:
            aligned1.append('-')
            aligned2.append(seq2[j-1])
            j -= 1
    
    aligned1 = ''.join(reversed(aligned1))
    aligned2 = ''.join(reversed(aligned2))
    
    # 计算统计信息
    identity, similarity, gaps = _calculate_stats(aligned1, aligned2, scoring_matrix)
    
    return AlignmentResult(
        seq1_aligned=aligned1,
        seq2_aligned=aligned2,
        score=score_matrix[m][n],
        identity=identity,
        similarity=similarity,
        gaps=gaps,
        alignment_type=AlignmentType.GLOBAL,
        matrix=score_matrix
    )


def smith_waterman(
    seq1: str,
    seq2: str,
    match_score: int = 2,
    mismatch_score: int = -1,
    gap_penalty: int = -1,
    scoring_matrix: Optional[Dict] = None
) -> AlignmentResult:
    """
    Smith-Waterman 局部序列比对算法
    
    Args:
        seq1: 第一条序列
        seq2: 第二条序列
        match_score: 匹配得分
        mismatch_score: 不匹配得分
        gap_penalty: 空位惩罚
        scoring_matrix: 自定义评分矩阵
        
    Returns:
        AlignmentResult 比对结果
    """
    m, n = len(seq1), len(seq2)
    
    # 初始化得分矩阵（局部比对从0开始）
    score_matrix = [[0.0] * (n + 1) for _ in range(m + 1)]
    
    max_score = 0.0
    max_pos = (0, 0)
    
    # 填充得分矩阵
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if scoring_matrix:
                match = score_matrix[i-1][j-1] + ScoringMatrix.get_score(
                    seq1[i-1], seq2[j-1], scoring_matrix
                )
            else:
                score = match_score if seq1[i-1] == seq2[j-1] else mismatch_score
                match = score_matrix[i-1][j-1] + score
            
            delete = score_matrix[i-1][j] + gap_penalty
            insert = score_matrix[i][j-1] + gap_penalty
            
            score_matrix[i][j] = max(0, match, delete, insert)
            
            if score_matrix[i][j] > max_score:
                max_score = score_matrix[i][j]
                max_pos = (i, j)
    
    # 回溯构建比对（从最高分位置开始）
    aligned1, aligned2 = [], []
    i, j = max_pos
    
    while i > 0 and j > 0 and score_matrix[i][j] > 0:
        if scoring_matrix:
            score = ScoringMatrix.get_score(seq1[i-1], seq2[j-1], scoring_matrix)
        else:
            score = match_score if seq1[i-1] == seq2[j-1] else mismatch_score
        
        if score_matrix[i][j] == score_matrix[i-1][j-1] + score:
            aligned1.append(seq1[i-1])
            aligned2.append(seq2[j-1])
            i -= 1
            j -= 1
        elif i > 0 and score_matrix[i][j] == score_matrix[i-1][j] + gap_penalty:
            aligned1.append(seq1[i-1])
            aligned2.append('-')
            i -= 1
        else:
            aligned1.append('-')
            aligned2.append(seq2[j-1])
            j -= 1
    
    aligned1 = ''.join(reversed(aligned1))
    aligned2 = ''.join(reversed(aligned2))
    
    # 计算统计信息
    identity, similarity, gaps = _calculate_stats(aligned1, aligned2, scoring_matrix)
    
    return AlignmentResult(
        seq1_aligned=aligned1,
        seq2_aligned=aligned2,
        score=max_score,
        identity=identity,
        similarity=similarity,
        gaps=gaps,
        alignment_type=AlignmentType.LOCAL,
        matrix=score_matrix
    )


def edit_distance(
    seq1: str,
    seq2: str,
    insertion_cost: int = 1,
    deletion_cost: int = 1,
    substitution_cost: int = 1
) -> int:
    """
    计算两个序列之间的编辑距离（Levenshtein距离）
    
    Args:
        seq1: 第一条序列
        seq2: 第二条序列
        insertion_cost: 插入操作代价
        deletion_cost: 删除操作代价
        substitution_cost: 替换操作代价
        
    Returns:
        编辑距离
    """
    m, n = len(seq1), len(seq2)
    
    # 优化：使用两行而非完整矩阵
    if m < n:
        seq1, seq2 = seq2, seq1
        m, n = n, m
        insertion_cost, deletion_cost = deletion_cost, insertion_cost
    
    # 只保存两行
    prev = list(range(n + 1))
    curr = [0] * (n + 1)
    
    for i in range(1, m + 1):
        curr[0] = i
        for j in range(1, n + 1):
            if seq1[i-1] == seq2[j-1]:
                curr[j] = prev[j-1]
            else:
                curr[j] = min(
                    prev[j] + deletion_cost,      # 删除
                    curr[j-1] + insertion_cost,   # 插入
                    prev[j-1] + substitution_cost # 替换
                )
        prev, curr = curr, prev
    
    return prev[n]


def damerau_levenshtein_distance(
    seq1: str,
    seq2: str
) -> int:
    """
    计算 Damerau-Levenshtein 距离
    支持相邻字符交换操作
    
    Args:
        seq1: 第一条序列
        seq2: 第二条序列
        
    Returns:
        Damerau-Levenshtein 距离
    """
    m, n = len(seq1), len(seq2)
    
    # 创建距离矩阵
    d = [[0] * (n + 1) for _ in range(m + 1)]
    
    # 初始化
    for i in range(m + 1):
        d[i][0] = i
    for j in range(n + 1):
        d[0][j] = j
    
    # 填充矩阵
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            cost = 0 if seq1[i-1] == seq2[j-1] else 1
            d[i][j] = min(
                d[i-1][j] + 1,      # 删除
                d[i][j-1] + 1,      # 插入
                d[i-1][j-1] + cost  # 替换
            )
            
            # 相邻交换
            if (i > 1 and j > 1 and 
                seq1[i-1] == seq2[j-2] and 
                seq1[i-2] == seq2[j-1]):
                d[i][j] = min(d[i][j], d[i-2][j-2] + 1)
    
    return d[m][n]


def hamming_distance(seq1: str, seq2: str) -> int:
    """
    计算汉明距离（等长序列不同位置的数目）
    
    Args:
        seq1: 第一条序列
        seq2: 第二条序列
        
    Returns:
        汉明距离
        
    Raises:
        ValueError: 当序列长度不等时
    """
    if len(seq1) != len(seq2):
        raise ValueError(f"序列长度不等: {len(seq1)} vs {len(seq2)}")
    
    return sum(c1 != c2 for c1, c2 in zip(seq1, seq2))


def jaro_distance(seq1: str, seq2: str) -> float:
    """
    计算 Jaro 距离
    
    Args:
        seq1: 第一条序列
        seq2: 第二条序列
        
    Returns:
        Jaro 相似度 (0-1)
    """
    if seq1 == seq2:
        return 1.0
    
    m, n = len(seq1), len(seq2)
    
    if m == 0 or n == 0:
        return 0.0
    
    match_distance = max(m, n) // 2 - 1
    if match_distance < 0:
        match_distance = 0
    
    seq1_matches = [False] * m
    seq2_matches = [False] * n
    
    matches = 0
    transpositions = 0
    
    # 找匹配字符
    for i in range(m):
        start = max(0, i - match_distance)
        end = min(i + match_distance + 1, n)
        
        for j in range(start, end):
            if seq2_matches[j] or seq1[i] != seq2[j]:
                continue
            seq1_matches[i] = True
            seq2_matches[j] = True
            matches += 1
            break
    
    if matches == 0:
        return 0.0
    
    # 计算换位数
    k = 0
    for i in range(m):
        if not seq1_matches[i]:
            continue
        while not seq2_matches[k]:
            k += 1
        if seq1[i] != seq2[k]:
            transpositions += 1
        k += 1
    
    return (
        matches / m + 
        matches / n + 
        (matches - transpositions / 2) / matches
    ) / 3


def jaro_winkler_distance(
    seq1: str,
    seq2: str,
    scaling_factor: float = 0.1
) -> float:
    """
    计算 Jaro-Winkler 相似度
    
    Args:
        seq1: 第一条序列
        seq2: 第二条序列
        scaling_factor: 缩放因子（通常为0.1）
        
    Returns:
        Jaro-Winkler 相似度 (0-1)
    """
    jaro_sim = jaro_distance(seq1, seq2)
    
    # 计算公共前缀长度（最多4个字符）
    prefix_len = 0
    for i in range(min(len(seq1), len(seq2), 4)):
        if seq1[i] == seq2[i]:
            prefix_len += 1
        else:
            break
    
    return jaro_sim + prefix_len * scaling_factor * (1 - jaro_sim)


def sequence_identity(seq1: str, seq2: str) -> float:
    """
    计算序列一致性百分比
    
    Args:
        seq1: 第一条序列
        seq2: 第二条序列
        
    Returns:
        一致性百分比 (0-1)
    """
    if not seq1 and not seq2:
        return 1.0
    if not seq1 or not seq2:
        return 0.0
    
    # 先做全局比对
    result = needleman_wunsch(seq1, seq2)
    return result.identity


def multiple_sequence_alignment(
    sequences: List[str],
    match_score: int = 1,
    mismatch_score: int = -1,
    gap_penalty: int = -2
) -> List[str]:
    """
    简单的多序列比对（渐进式方法）
    
    Args:
        sequences: 序列列表
        match_score: 匹配得分
        mismatch_score: 不匹配得分
        gap_penalty: 空位惩罚
        
    Returns:
        比对后的序列列表
    """
    if not sequences:
        return []
    
    if len(sequences) == 1:
        return sequences.copy()
    
    # 简单的渐进式比对：逐个加入序列
    aligned = [sequences[0]]
    
    for i in range(1, len(sequences)):
        new_seq = sequences[i]
        
        # 找最佳比对
        best_result = None
        best_score = float('-inf')
        best_idx = 0
        
        for j, existing in enumerate(aligned):
            result = needleman_wunsch(
                existing, new_seq,
                match_score, mismatch_score, gap_penalty
            )
            if result.score > best_score:
                best_score = result.score
                best_result = result
                best_idx = j
        
        # 更新所有已比对序列
        if best_result:
            aligned[best_idx] = best_result.seq1_aligned
            aligned.insert(best_idx + 1, best_result.seq2_aligned)
            
            # 对齐其他序列的空位
            for k in range(len(aligned)):
                if k != best_idx and k != best_idx + 1:
                    # 添加前导空位以匹配长度
                    diff = len(best_result.seq1_aligned) - len(aligned[k])
                    if diff > 0:
                        aligned[k] += '-' * diff
    
    return aligned


def find_consensus(sequences: List[str]) -> str:
    """
    从比对序列中构建一致序列
    
    Args:
        sequences: 已比对序列列表
        
    Returns:
        一致序列
    """
    if not sequences:
        return ""
    
    length = max(len(s) for s in sequences)
    consensus = []
    
    for i in range(length):
        column = []
        for seq in sequences:
            if i < len(seq):
                column.append(seq[i])
        
        if not column:
            consensus.append('-')
            continue
        
        # 统计非空位字符
        non_gap = [c for c in column if c != '-']
        if not non_gap:
            consensus.append('-')
            continue
        
        # 选择最常见的字符
        counts = {}
        for c in non_gap:
            counts[c] = counts.get(c, 0) + 1
        
        most_common = max(counts.items(), key=lambda x: x[1])
        consensus.append(most_common[0])
    
    return ''.join(consensus)


def _calculate_stats(
    aligned1: str,
    aligned2: str,
    scoring_matrix: Optional[Dict] = None
) -> Tuple[float, float, int]:
    """计算比对统计信息"""
    if not aligned1:
        return 0.0, 0.0, 0
    
    matches = 0
    similar = 0
    gaps = 0
    
    for c1, c2 in zip(aligned1, aligned2):
        if c1 == '-' or c2 == '-':
            gaps += 1
        elif c1 == c2:
            matches += 1
            similar += 1
        else:
            # 检查相似性
            if scoring_matrix:
                score = ScoringMatrix.get_score(c1, c2, scoring_matrix)
                if score > 0:
                    similar += 1
    
    # 计算百分比（基于非空位位置）
    non_gap_len = len(aligned1.replace('-', ''))
    if non_gap_len == 0:
        non_gap_len = 1
    
    identity = matches / non_gap_len
    similarity = similar / non_gap_len
    
    return identity, similarity, gaps


def align(
    seq1: str,
    seq2: str,
    mode: str = "global",
    **kwargs
) -> AlignmentResult:
    """
    便捷比对函数
    
    Args:
        seq1: 第一条序列
        seq2: 第二条序列
        mode: 比对模式 "global" 或 "local"
        **kwargs: 传递给具体算法的参数
        
    Returns:
        AlignmentResult 比对结果
    """
    if mode == "local":
        return smith_waterman(seq1, seq2, **kwargs)
    else:
        return needleman_wunsch(seq1, seq2, **kwargs)


# 便捷函数
def global_alignment(seq1: str, seq2: str, **kwargs) -> AlignmentResult:
    """全局比对（Needleman-Wunsch）"""
    return needleman_wunsch(seq1, seq2, **kwargs)


def local_alignment(seq1: str, seq2: str, **kwargs) -> AlignmentResult:
    """局部比对（Smith-Waterman）"""
    return smith_waterman(seq1, seq2, **kwargs)


if __name__ == "__main__":
    # 简单演示
    seq1 = "ACGTACGT"
    seq2 = "ACGAACGT"
    
    print("全局比对:")
    result = global_alignment(seq1, seq2)
    print(result.format_alignment())
    
    print("\n局部比对:")
    result = local_alignment(seq1, seq2)
    print(result.format_alignment())
    
    print("\n编辑距离:", edit_distance(seq1, seq2))
    print("Jaro-Winkler:", jaro_winkler_distance(seq1, seq2))
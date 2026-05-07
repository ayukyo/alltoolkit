"""
DNA Utils - DNA/RNA 序列工具库

提供完整的 DNA/RNA 序列操作功能，包括：
- DNA/RNA 序列验证
- DNA 转录为 RNA
- RNA 翻译为蛋白质
- 互补链/反向互补链生成
- GC 含量计算
- 密码子查询
- 序列统计分析
- 突变操作
- 序列比对基础功能

零外部依赖，纯 Python 标准库实现。
"""

from typing import Dict, List, Tuple, Optional, Set
from enum import Enum
from collections import Counter
import random


class SequenceType(Enum):
    """序列类型"""
    DNA = "dna"
    RNA = "rna"
    PROTEIN = "protein"


class NucleotideError(Exception):
    """核苷酸相关错误"""
    pass


class CodonError(Exception):
    """密码子相关错误"""
    pass


# ============================================================================
# 常量定义
# ============================================================================

# DNA 碱基
DNA_BASES = set('ATCG')
DNA_BASES_LOWER = set('atcg')
DNA_BASES_ALL = DNA_BASES | DNA_BASES_LOWER

# RNA 碱基
RNA_BASES = set('AUCG')
RNA_BASES_LOWER = set('aucg')
RNA_BASES_ALL = RNA_BASES | RNA_BASES_LOWER

# 模糊碱基 (IUPAC 编码)
IUPAC_DNA = {
    'A': {'A'},
    'C': {'C'},
    'G': {'G'},
    'T': {'T'},
    'R': {'A', 'G'},      # 嘌呤 (A 或 G)
    'Y': {'C', 'T'},      # 嘧啶 (C 或 T)
    'S': {'G', 'C'},      # 强碱基
    'W': {'A', 'T'},      # 弱碱基
    'K': {'G', 'T'},      # 酮基
    'M': {'A', 'C'},      # 氨基
    'B': {'C', 'G', 'T'}, # 非 A
    'D': {'A', 'G', 'T'}, # 非 C
    'H': {'A', 'C', 'T'}, # 非 G
    'V': {'A', 'C', 'G'}, # 非 T
    'N': {'A', 'C', 'G', 'T'},  # 任意碱基
}

# 标准遗传密码表 (RNA → 氨基酸)
CODON_TABLE = {
    # 苯丙氨酸 (F)
    'UUU': 'F', 'UUC': 'F',
    # 亮氨酸 (L)
    'UUA': 'L', 'UUG': 'L', 'CUU': 'L', 'CUC': 'L', 'CUA': 'L', 'CUG': 'L',
    # 异亮氨酸 (I)
    'AUU': 'I', 'AUC': 'I', 'AUA': 'I',
    # 甲硫氨酸/起始密码子 (M)
    'AUG': 'M',
    # 缬氨酸 (V)
    'GUU': 'V', 'GUC': 'V', 'GUA': 'V', 'GUG': 'V',
    # 丝氨酸 (S)
    'UCU': 'S', 'UCC': 'S', 'UCA': 'S', 'UCG': 'S', 'AGU': 'S', 'AGC': 'S',
    # 脯氨酸 (P)
    'CCU': 'P', 'CCC': 'P', 'CCA': 'P', 'CCG': 'P',
    # 苏氨酸 (T)
    'ACU': 'T', 'ACC': 'T', 'ACA': 'T', 'ACG': 'T',
    # 丙氨酸 (A)
    'GCU': 'A', 'GCC': 'A', 'GCA': 'A', 'GCG': 'A',
    # 酪氨酸 (Y)
    'UAU': 'Y', 'UAC': 'Y',
    # 组氨酸 (H)
    'CAU': 'H', 'CAC': 'H',
    # 谷氨酰胺 (Q)
    'CAA': 'Q', 'CAG': 'Q',
    # 天冬酰胺 (N)
    'AAU': 'N', 'AAC': 'N',
    # 赖氨酸 (K)
    'AAA': 'K', 'AAG': 'K',
    # 天冬氨酸 (D)
    'GAU': 'D', 'GAC': 'D',
    # 谷氨酸 (E)
    'GAA': 'E', 'GAG': 'E',
    # 半胱氨酸 (C)
    'UGU': 'C', 'UGC': 'C',
    # 色氨酸 (W)
    'UGG': 'W',
    # 精氨酸 (R)
    'CGU': 'R', 'CGC': 'R', 'CGA': 'R', 'CGG': 'R', 'AGA': 'R', 'AGG': 'R',
    # 甘氨酸 (G)
    'GGU': 'G', 'GGC': 'G', 'GGA': 'G', 'GGG': 'G',
    # 终止密码子
    'UAA': '*', 'UAG': '*', 'UGA': '*',
}

# 氨基酸单字母代码 → 三字母代码
AMINO_ACID_CODES = {
    'A': 'Ala', 'R': 'Arg', 'N': 'Asn', 'D': 'Asp', 'C': 'Cys',
    'E': 'Glu', 'Q': 'Gln', 'G': 'Gly', 'H': 'His', 'I': 'Ile',
    'L': 'Leu', 'K': 'Lys', 'M': 'Met', 'F': 'Phe', 'P': 'Pro',
    'S': 'Ser', 'T': 'Thr', 'W': 'Trp', 'Y': 'Tyr', 'V': 'Val',
    '*': 'Stop',
}

# 氨基酸中文名称
AMINO_ACID_NAMES_ZH = {
    'A': '丙氨酸', 'R': '精氨酸', 'N': '天冬酰胺', 'D': '天冬氨酸', 'C': '半胱氨酸',
    'E': '谷氨酸', 'Q': '谷氨酰胺', 'G': '甘氨酸', 'H': '组氨酸', 'I': '异亮氨酸',
    'L': '亮氨酸', 'K': '赖氨酸', 'M': '甲硫氨酸', 'F': '苯丙氨酸', 'P': '脯氨酸',
    'S': '丝氨酸', 'T': '苏氨酸', 'W': '色氨酸', 'Y': '酪氨酸', 'V': '缬氨酸',
    '*': '终止密码子',
}

# 起始密码子
START_CODONS = {'AUG'}

# 终止密码子
STOP_CODONS = {'UAA', 'UAG', 'UGA'}

# DNA 互补碱基
DNA_COMPLEMENT = {
    'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G',
    'a': 't', 't': 'a', 'g': 'c', 'c': 'g',
}

# RNA 互补碱基
RNA_COMPLEMENT = {
    'A': 'U', 'U': 'A', 'G': 'C', 'C': 'G',
    'a': 'u', 'u': 'a', 'g': 'c', 'c': 'g',
}


# ============================================================================
# 序列验证
# ============================================================================

def is_valid_dna(sequence: str) -> bool:
    """
    验证序列是否为有效 DNA 序列。
    
    Args:
        sequence: 待验证的序列字符串
        
    Returns:
        bool: 是否为有效 DNA 序列
        
    Example:
        >>> is_valid_dna("ATCG")
        True
        >>> is_valid_dna("ATCGN")  # 包含模糊碱基
        True
        >>> is_valid_dna("ATCGU")  # 包含 RNA 碱基
        False
    """
    if not sequence:
        return False
    return all(base.upper() in IUPAC_DNA for base in sequence)


def is_valid_rna(sequence: str) -> bool:
    """
    验证序列是否为有效 RNA 序列。
    
    Args:
        sequence: 待验证的序列字符串
        
    Returns:
        bool: 是否为有效 RNA 序列
        
    Example:
        >>> is_valid_rna("AUCG")
        True
        >>> is_valid_rna("ATCG")  # DNA 碱基
        False
    """
    if not sequence:
        return False
    valid_bases = RNA_BASES | {'N'}  # 支持 N 作为模糊碱基
    return all(base.upper() in valid_bases for base in sequence)


def is_valid_protein(sequence: str) -> bool:
    """
    验证序列是否为有效蛋白质序列。
    
    Args:
        sequence: 待验证的序列字符串
        
    Returns:
        bool: 是否为有效蛋白质序列
        
    Example:
        >>> is_valid_protein("MVLSPADK")
        True
        >>> is_valid_protein("MVLSPADX")
        False
    """
    if not sequence:
        return False
    valid_aa = set(AMINO_ACID_CODES.keys())
    return all(aa.upper() in valid_aa for aa in sequence)


def detect_sequence_type(sequence: str) -> Optional[SequenceType]:
    """
    自动检测序列类型。
    
    Args:
        sequence: 待检测的序列字符串
        
    Returns:
        Optional[SequenceType]: 检测到的序列类型，无法确定时返回 None
        
    Example:
        >>> detect_sequence_type("ATCG")
        <SequenceType.DNA: 'dna'>
        >>> detect_sequence_type("AUCG")
        <SequenceType.RNA: 'rna'>
        >>> detect_sequence_type("MVLSPADK")
        <SequenceType.PROTEIN: 'protein'>
    """
    if not sequence:
        return None
    
    upper_seq = sequence.upper()
    
    # 检查是否包含 U（RNA 特有）
    has_u = 'U' in upper_seq
    # 检查是否包含 T（DNA 特有）
    has_t = 'T' in upper_seq
    
    # 如果同时包含 T 和 U，无效序列
    if has_u and has_t:
        return None
    
    # 检查是否为纯 DNA
    if all(base in DNA_BASES for base in upper_seq):
        return SequenceType.DNA
    
    # 检查是否为纯 RNA
    if all(base in RNA_BASES for base in upper_seq):
        return SequenceType.RNA
    
    # 检查是否为蛋白质
    valid_aa = set(AMINO_ACID_CODES.keys()) - {'*'}
    if all(aa in valid_aa for aa in upper_seq):
        return SequenceType.PROTEIN
    
    # 可能包含模糊碱基的 DNA
    if all(base in IUPAC_DNA for base in upper_seq):
        return SequenceType.DNA
    
    return None


def validate_sequence(sequence: str, seq_type: Optional[SequenceType] = None) -> Tuple[bool, str]:
    """
    验证序列并返回详细信息。
    
    Args:
        sequence: 待验证的序列字符串
        seq_type: 指定的序列类型，None 则自动检测
        
    Returns:
        Tuple[bool, str]: (是否有效, 错误信息或成功信息)
        
    Example:
        >>> validate_sequence("ATCG", SequenceType.DNA)
        (True, '有效 DNA 序列，长度: 4')
        >>> validate_sequence("AUCG", SequenceType.DNA)
        (False, '序列包含非 DNA 碱基: U')
    """
    if not sequence:
        return False, "空序列"
    
    if seq_type is None:
        seq_type = detect_sequence_type(sequence)
        if seq_type is None:
            return False, "无法确定序列类型"
    
    upper_seq = sequence.upper()
    
    if seq_type == SequenceType.DNA:
        invalid_bases = set(upper_seq) - set(IUPAC_DNA.keys())
        if invalid_bases:
            return False, f"序列包含非 DNA 碱基: {', '.join(invalid_bases)}"
        return True, f"有效 DNA 序列，长度: {len(sequence)}"
    
    elif seq_type == SequenceType.RNA:
        valid_bases = RNA_BASES | {'N'}
        invalid_bases = set(upper_seq) - valid_bases
        if invalid_bases:
            return False, f"序列包含非 RNA 碱基: {', '.join(invalid_bases)}"
        return True, f"有效 RNA 序列，长度: {len(sequence)}"
    
    elif seq_type == SequenceType.PROTEIN:
        valid_aa = set(AMINO_ACID_CODES.keys())
        invalid_aa = set(upper_seq) - valid_aa
        if invalid_aa:
            return False, f"序列包含非标准氨基酸: {', '.join(invalid_aa)}"
        return True, f"有效蛋白质序列，长度: {len(sequence)}"
    
    return False, "未知序列类型"


# ============================================================================
# 序列转换
# ============================================================================

def transcribe(dna: str) -> str:
    """
    DNA 转录为 RNA (T → U)。
    
    Args:
        dna: DNA 序列字符串
        
    Returns:
        str: RNA 序列字符串
        
    Raises:
        NucleotideError: 如果序列无效
        
    Example:
        >>> transcribe("ATCG")
        'AUCG'
        >>> transcribe("TACGTA")
        'UACGUA'
    """
    if not is_valid_dna(dna):
        raise NucleotideError(f"无效的 DNA 序列: {dna}")
    return dna.upper().replace('T', 'U')


def reverse_transcribe(rna: str) -> str:
    """
    RNA 逆转录为 DNA (U → T)。
    
    Args:
        rna: RNA 序列字符串
        
    Returns:
        str: DNA 序列字符串
        
    Raises:
        NucleotideError: 如果序列无效
        
    Example:
        >>> reverse_transcribe("AUCG")
        'ATCG'
    """
    if not is_valid_rna(rna):
        raise NucleotideError(f"无效的 RNA 序列: {rna}")
    return rna.upper().replace('U', 'T')


def translate(rna: str, start_offset: int = 0) -> str:
    """
    RNA 翻译为蛋白质。
    
    Args:
        rna: RNA 序列字符串
        start_offset: 翻译起始偏移量 (0, 1, 或 2)
        
    Returns:
        str: 蛋白质序列字符串
        
    Raises:
        NucleotideError: 如果序列无效
        CodonError: 如果遇到未知密码子
        
    Example:
        >>> translate("AUGGCCUAA")  # M-A-Stop
        'MA*'
    """
    if not is_valid_rna(rna):
        raise NucleotideError(f"无效的 RNA 序列: {rna}")
    
    if start_offset < 0 or start_offset > 2:
        raise ValueError("起始偏移量必须为 0, 1 或 2")
    
    rna = rna.upper()
    protein = []
    
    for i in range(start_offset, len(rna) - 2, 3):
        codon = rna[i:i+3]
        if codon in CODON_TABLE:
            aa = CODON_TABLE[codon]
            protein.append(aa)
        else:
            raise CodonError(f"未知密码子: {codon}")
    
    return ''.join(protein)


def translate_dna(dna: str, start_offset: int = 0) -> str:
    """
    DNA 直接翻译为蛋白质。
    
    Args:
        dna: DNA 序列字符串
        start_offset: 翻译起始偏移量
        
    Returns:
        str: 蛋白质序列字符串
        
    Example:
        >>> translate_dna("ATGGCCTAA")
        'MA*'
    """
    rna = transcribe(dna)
    return translate(rna, start_offset)


def complement_dna(dna: str) -> str:
    """
    生成 DNA 互补链。
    
    Args:
        dna: DNA 序列字符串
        
    Returns:
        str: 互补 DNA 序列
        
    Raises:
        NucleotideError: 如果序列无效
        
    Example:
        >>> complement_dna("ATCG")
        'TAGC'
    """
    if not is_valid_dna(dna):
        raise NucleotideError(f"无效的 DNA 序列: {dna}")
    
    result = []
    for base in dna:
        if base.upper() in DNA_COMPLEMENT:
            comp = DNA_COMPLEMENT[base]
            result.append(comp if base.islower() else comp.upper())
        else:
            # 处理模糊碱基
            result.append('N')
    
    return ''.join(result)


def complement_rna(rna: str) -> str:
    """
    生成 RNA 互补链。
    
    Args:
        rna: RNA 序列字符串
        
    Returns:
        str: 互补 RNA 序列
        
    Raises:
        NucleotideError: 如果序列无效
        
    Example:
        >>> complement_rna("AUCG")
        'UAGC'
    """
    if not is_valid_rna(rna):
        raise NucleotideError(f"无效的 RNA 序列: {rna}")
    
    result = []
    for base in rna:
        if base.upper() in RNA_COMPLEMENT:
            comp = RNA_COMPLEMENT[base]
            result.append(comp if base.islower() else comp.upper())
        else:
            result.append('N')
    
    return ''.join(result)


def reverse_complement_dna(dna: str) -> str:
    """
    生成 DNA 反向互补链。
    
    Args:
        dna: DNA 序列字符串
        
    Returns:
        str: 反向互补 DNA 序列
        
    Example:
        >>> reverse_complement_dna("ATCG")
        'CGAT'
    """
    return complement_dna(dna)[::-1]


def reverse_complement_rna(rna: str) -> str:
    """
    生成 RNA 反向互补链。
    
    Args:
        rna: RNA 序列字符串
        
    Returns:
        str: 反向互补 RNA 序列
        
    Example:
        >>> reverse_complement_rna("AUCG")
        'CGAU'
    """
    return complement_rna(rna)[::-1]


# ============================================================================
# GC 含量计算
# ============================================================================

def gc_content(sequence: str, seq_type: Optional[SequenceType] = None) -> float:
    """
    计算 GC 含量百分比。
    
    Args:
        sequence: 核酸序列字符串
        seq_type: 序列类型，None 则自动检测
        
    Returns:
        float: GC 含量百分比 (0-100)
        
    Example:
        >>> gc_content("GCGC")
        100.0
        >>> gc_content("ATCG")
        50.0
    """
    if not sequence:
        return 0.0
    
    seq = sequence.upper()
    
    if seq_type is None:
        seq_type = detect_sequence_type(sequence)
    
    # 将 RNA 的 U 转换为 T 进行计算
    if seq_type == SequenceType.RNA:
        seq = seq.replace('U', 'T')
    
    g_count = seq.count('G')
    c_count = seq.count('C')
    
    # 排除模糊碱基 N
    total = len([b for b in seq if b in 'ATCG'])
    
    if total == 0:
        return 0.0
    
    return (g_count + c_count) / total * 100


def gc_content_window(sequence: str, window_size: int = 100, step: int = 1) -> List[Tuple[int, float]]:
    """
    滑动窗口计算 GC 含量。
    
    Args:
        sequence: 核酸序列字符串
        window_size: 窗口大小
        step: 步长
        
    Returns:
        List[Tuple[int, float]]: [(位置, GC含量), ...]
        
    Example:
        >>> gc_content_window("ATCGATCG", window_size=4)
        [(0, 50.0), (1, 50.0), (2, 50.0), (3, 50.0), (4, 50.0)]
    """
    if len(sequence) < window_size:
        return [(0, gc_content(sequence))]
    
    results = []
    for i in range(0, len(sequence) - window_size + 1, step):
        window = sequence[i:i + window_size]
        gc = gc_content(window)
        results.append((i, gc))
    
    return results


# ============================================================================
# 密码子操作
# ============================================================================

def get_amino_acid(codon: str) -> str:
    """
    根据密码子获取氨基酸。
    
    Args:
        codon: 三碱基密码子 (RNA 或 DNA)
        
    Returns:
        str: 氨基酸单字母代码
        
    Raises:
        CodonError: 如果密码子无效
        
    Example:
        >>> get_amino_acid("AUG")
        'M'
        >>> get_amino_acid("ATG")  # DNA 密码子
        'M'
    """
    codon = codon.upper()
    
    # 如果是 DNA，转换为 RNA
    if 'T' in codon:
        codon = codon.replace('T', 'U')
    
    if len(codon) != 3:
        raise CodonError(f"密码子长度必须为 3: {codon}")
    
    if codon not in CODON_TABLE:
        raise CodonError(f"未知密码子: {codon}")
    
    return CODON_TABLE[codon]


def get_codons(aa: str) -> List[str]:
    """
    获取编码指定氨基酸的所有密码子。
    
    Args:
        aa: 氨基酸单字母代码
        
    Returns:
        List[str]: 密码子列表
        
    Example:
        >>> get_codons('M')  # 甲硫氨酸只有一个密码子
        ['AUG']
        >>> get_codons('L')  # 亮氨酸有 6 个密码子
        ['UUA', 'UUG', 'CUU', 'CUC', 'CUA', 'CUG']
    """
    aa = aa.upper()
    return [codon for codon, amino in CODON_TABLE.items() if amino == aa]


def is_start_codon(codon: str) -> bool:
    """
    判断是否为起始密码子。
    
    Args:
        codon: 三碱基密码子
        
    Returns:
        bool: 是否为起始密码子
        
    Example:
        >>> is_start_codon("AUG")
        True
        >>> is_start_codon("UAA")
        False
    """
    codon = codon.upper()
    if 'T' in codon:
        codon = codon.replace('T', 'U')
    return codon in START_CODONS


def is_stop_codon(codon: str) -> bool:
    """
    判断是否为终止密码子。
    
    Args:
        codon: 三碱基密码子
        
    Returns:
        bool: 是否为终止密码子
        
    Example:
        >>> is_stop_codon("UAA")
        True
        >>> is_stop_codon("AUG")
        False
    """
    codon = codon.upper()
    if 'T' in codon:
        codon = codon.replace('T', 'U')
    return codon in STOP_CODONS


def codon_usage(sequence: str) -> Dict[str, int]:
    """
    统计序列中密码子使用频率。
    
    Args:
        sequence: RNA 或 DNA 序列
        
    Returns:
        Dict[str, int]: {密码子: 使用次数}
        
    Example:
        >>> codon_usage("AUGGCCAUGGCC")
        {'AUG': 2, 'GCC': 2}
    """
    seq = sequence.upper()
    if 'T' in seq:
        seq = seq.replace('T', 'U')
    
    usage = Counter()
    for i in range(0, len(seq) - 2, 3):
        codon = seq[i:i+3]
        if len(codon) == 3:
            usage[codon] += 1
    
    return dict(usage)


# ============================================================================
# 序列统计
# ============================================================================

def nucleotide_count(sequence: str) -> Dict[str, int]:
    """
    统计核苷酸数量。
    
    Args:
        sequence: 核酸序列
        
    Returns:
        Dict[str, int]: {碱基: 数量}
        
    Example:
        >>> nucleotide_count("ATCGATCG")
        {'A': 2, 'T': 2, 'C': 2, 'G': 2}
    """
    if not sequence:
        return {}
    
    seq = sequence.upper()
    result = {}
    for base in 'ATCG':
        count = seq.count(base)
        if count > 0:
            result[base] = count
    return result


def molecular_weight(sequence: str, seq_type: Optional[SequenceType] = None) -> float:
    """
    计算分子量 (道尔顿)。
    
    Args:
        sequence: 核酸序列
        seq_type: 序列类型
        
    Returns:
        float: 分子量 (Da)
        
    Note:
        使用平均分子量计算
        - DNA 单链: dAMP=313.2, dTMP=304.2, dCMP=289.2, dGMP=329.2
        - RNA 单链: AMP=347.2, UMP=324.2, CMP=323.2, GMP=363.2
    """
    if seq_type is None:
        seq_type = detect_sequence_type(sequence)
    
    seq = sequence.upper()
    
    # 分子量 (Da)
    if seq_type == SequenceType.DNA:
        weights = {'A': 313.2, 'T': 304.2, 'C': 289.2, 'G': 329.2}
    else:  # RNA
        weights = {'A': 347.2, 'U': 324.2, 'C': 323.2, 'G': 363.2}
    
    total = 0.0
    for base in seq:
        if base in weights:
            total += weights[base]
    
    # 减去 n-1 个水分子 (每个磷酸二酯键失去一个水分子)
    if len(seq) > 1:
        total -= (len(seq) - 1) * 18.0
    
    return total


def melting_temperature(sequence: str, method: str = 'basic') -> float:
    """
    计算 DNA 序列的熔解温度 (Tm)。
    
    Args:
        sequence: DNA 序列
        method: 计算方法 ('basic', 'wallace', 'salt_adjusted')
        
    Returns:
        float: 熔解温度 (°C)
        
    Note:
        - basic: Tm = 4(G+C) + 2(A+T) (适用于 <14bp)
        - wallace: Tm = 64.9 + 41*(G+C-16.4)/(A+T+G+C) (适用于 14-70bp)
        - salt_adjusted: 考虑盐离子浓度
        
    Example:
        >>> melting_temperature("ATCG", method='basic')
        12.0
    """
    seq = sequence.upper()
    
    g = seq.count('G')
    c = seq.count('C')
    a = seq.count('A')
    t = seq.count('T')
    n = len(seq)
    
    if method == 'basic':
        # 适用于短寡核苷酸 (<14bp)
        return 4 * (g + c) + 2 * (a + t)
    
    elif method == 'wallace':
        # Wallace 规则 (14-70bp)
        if n == 0:
            return 0.0
        return 64.9 + 41 * (g + c - 16.4) / n
    
    elif method == 'salt_adjusted':
        # 盐离子调整公式 (需要盐浓度)
        # 假设 50mM 盐浓度
        if n == 0:
            return 0.0
        gc = (g + c) / n
        return 81.5 + 16.6 * 0.069 + 41 * gc - 675 / n
    
    else:
        raise ValueError(f"未知的 Tm 计算方法: {method}")


def find_orfs(sequence: str, min_length: int = 30) -> List[Dict]:
    """
    查找开放阅读框 (ORF)。
    
    Args:
        sequence: DNA 序列
        min_length: 最小 ORF 长度 (碱基数)
        
    Returns:
        List[Dict]: ORF 信息列表
        
    Example:
        >>> orfs = find_orfs("ATGAAATAGATGTTTTAA", min_length=9)
        >>> len(orfs) > 0
        True
    """
    seq = sequence.upper()
    orfs = []
    
    # 三种阅读框
    for frame in range(3):
        i = frame
        while i < len(seq) - 2:
            # 寻找起始密码子
            codon = seq[i:i+3]
            if codon == 'ATG':
                # 找到了起始密码子，寻找终止密码子
                start = i
                j = i + 3
                found_stop = False
                
                while j < len(seq) - 2:
                    stop_codon = seq[j:j+3]
                    if stop_codon in ['TAA', 'TAG', 'TGA']:
                        # 找到了终止密码子
                        orf_length = j + 3 - start
                        if orf_length >= min_length:
                            orfs.append({
                                'start': start,
                                'end': j + 3,
                                'length': orf_length,
                                'frame': frame + 1,
                                'sequence': seq[start:j+3],
                                'protein': translate_dna(seq[start:j+3])[:-1]  # 去掉终止符
                            })
                        found_stop = True
                        break
                    j += 3
                
                if found_stop:
                    i = j + 3
                else:
                    i += 3
            else:
                i += 3
    
    return orfs


# ============================================================================
# 突变操作
# ============================================================================

def point_mutation(sequence: str, position: int, new_base: str) -> str:
    """
    点突变。
    
    Args:
        sequence: 原始序列
        position: 突变位置 (0-indexed)
        new_base: 新碱基
        
    Returns:
        str: 突变后序列
        
    Raises:
        NucleotideError: 如果位置无效
        
    Example:
        >>> point_mutation("ATCG", 1, "G")
        'AGCG'
    """
    if position < 0 or position >= len(sequence):
        raise NucleotideError(f"位置 {position} 超出序列范围")
    
    return sequence[:position] + new_base + sequence[position + 1:]


def deletion(sequence: str, start: int, length: int = 1) -> str:
    """
    缺失突变。
    
    Args:
        sequence: 原始序列
        start: 缺失起始位置
        length: 缺失长度
        
    Returns:
        str: 突变后序列
        
    Example:
        >>> deletion("ATCGATCG", 2, 3)
        'ATTCG'
    """
    if start < 0 or start + length > len(sequence):
        raise NucleotideError(f"缺失范围超出序列")
    
    return sequence[:start] + sequence[start + length:]


def insertion(sequence: str, position: int, insert_seq: str) -> str:
    """
    插入突变。
    
    Args:
        sequence: 原始序列
        position: 插入位置
        insert_seq: 插入序列
        
    Returns:
        str: 突变后序列
        
    Example:
        >>> insertion("ATCG", 2, "XXX")
        'ATXXXCG'
    """
    if position < 0 or position > len(sequence):
        raise NucleotideError(f"位置 {position} 超出序列范围")
    
    return sequence[:position] + insert_seq + sequence[position:]


def substitution(sequence: str, start: int, new_seq: str) -> str:
    """
    替换突变。
    
    Args:
        sequence: 原始序列
        start: 替换起始位置
        new_seq: 新序列
        
    Returns:
        str: 突变后序列
        
    Example:
        >>> substitution("ATCGATCG", 2, "XXX")
        'ATXXXTCG'
    """
    if start < 0 or start + len(new_seq) > len(sequence):
        raise NucleotideError(f"替换范围超出序列")
    
    return sequence[:start] + new_seq + sequence[start + len(new_seq):]


def random_mutation(sequence: str, mutation_rate: float = 0.01) -> str:
    """
    随机突变。
    
    Args:
        sequence: 原始序列
        mutation_rate: 突变率 (0-1)
        
    Returns:
        str: 突变后序列
        
    Example:
        >>> mutated = random_mutation("AAAAAAAAAA", mutation_rate=0.5)
        >>> mutated != "AAAAAAAAAA"  # 很可能发生突变
        True
    """
    if mutation_rate < 0 or mutation_rate > 1:
        raise ValueError("突变率必须在 0-1 之间")
    
    bases = {'A', 'T', 'C', 'G'}
    result = []
    
    for base in sequence:
        if random.random() < mutation_rate:
            # 选择不同的碱基
            new_base = random.choice(list(bases - {base.upper()}))
            result.append(new_base)
        else:
            result.append(base)
    
    return ''.join(result)


# ============================================================================
# 序列比对辅助
# ============================================================================

def hamming_distance(seq1: str, seq2: str) -> int:
    """
    计算 Hamming 距离（等长序列的差异碱基数）。
    
    Args:
        seq1: 序列 1
        seq2: 序列 2
        
    Returns:
        int: Hamming 距离
        
    Raises:
        ValueError: 如果序列长度不同
        
    Example:
        >>> hamming_distance("ATCG", "ATCC")
        1
        >>> hamming_distance("AAAA", "TTTT")
        4
    """
    if len(seq1) != len(seq2):
        raise ValueError("序列长度必须相同")
    
    return sum(b1.upper() != b2.upper() for b1, b2 in zip(seq1, seq2))


def sequence_identity(seq1: str, seq2: str) -> float:
    """
    计算序列相似度百分比。
    
    Args:
        seq1: 序列 1
        seq2: 序列 2
        
    Returns:
        float: 相似度百分比 (0-100)
        
    Example:
        >>> sequence_identity("ATCG", "ATCC")
        75.0
    """
    if len(seq1) != len(seq2):
        min_len = min(len(seq1), len(seq2))
        seq1 = seq1[:min_len]
        seq2 = seq2[:min_len]
    
    if len(seq1) == 0:
        return 0.0
    
    matches = sum(b1.upper() == b2.upper() for b1, b2 in zip(seq1, seq2))
    return matches / len(seq1) * 100


def find_motif(sequence: str, motif: str) -> List[int]:
    """
    查找序列中的模体位置。
    
    Args:
        sequence: 目标序列
        motif: 要查找的模体
        
    Returns:
        List[int]: 模体出现的起始位置列表
        
    Example:
        >>> find_motif("ATCGATCGATCG", "ATCG")
        [0, 4, 8]
    """
    positions = []
    start = 0
    
    while True:
        pos = sequence.upper().find(motif.upper(), start)
        if pos == -1:
            break
        positions.append(pos)
        start = pos + 1
    
    return positions


def find_palindromes(sequence: str, min_length: int = 4) -> List[Dict]:
    """
    查找 DNA 序列中的回文序列。
    
    Args:
        sequence: DNA 序列
        min_length: 最小回文长度
        
    Returns:
        List[Dict]: 回文序列信息列表
        
    Example:
        >>> find_palindromes("GAATTC", min_length=4)
        [{'start': 0, 'end': 6, 'sequence': 'GAATTC', 'length': 6}]
    """
    seq = sequence.upper()
    palindromes = []
    
    for length in range(min_length, len(seq) + 1):
        for i in range(len(seq) - length + 1):
            subseq = seq[i:i + length]
            if subseq == reverse_complement_dna(subseq):
                palindromes.append({
                    'start': i,
                    'end': i + length,
                    'sequence': subseq,
                    'length': length
                })
    
    return palindromes


# ============================================================================
# 序列生成
# ============================================================================

def random_dna(length: int, gc_content: Optional[float] = None) -> str:
    """
    生成随机 DNA 序列。
    
    Args:
        length: 序列长度
        gc_content: GC 含量 (None 表示随机)
        
    Returns:
        str: 随机 DNA 序列
        
    Example:
        >>> len(random_dna(10))
        10
        >>> gc = gc_content(random_dna(100, gc_content=60))
        >>> 50 < gc < 70  # 大约 60%
        True
    """
    if gc_content is None:
        return ''.join(random.choices('ATCG', k=length))
    else:
        # 根据指定的 GC 含量生成
        gc_count = int(length * gc_content / 100)
        at_count = length - gc_count
        
        gc_bases = random.choices('GC', k=gc_count)
        at_bases = random.choices('AT', k=at_count)
        
        all_bases = gc_bases + at_bases
        random.shuffle(all_bases)
        
        return ''.join(all_bases)


def random_rna(length: int) -> str:
    """
    生成随机 RNA 序列。
    
    Args:
        length: 序列长度
        
    Returns:
        str: 随机 RNA 序列
        
    Example:
        >>> len(random_rna(10))
        10
    """
    return ''.join(random.choices('AUCG', k=length))


def random_protein(length: int) -> str:
    """
    生成随机蛋白质序列。
    
    Args:
        length: 序列长度
        
    Returns:
        str: 随机蛋白质序列
        
    Example:
        >>> len(random_protein(10))
        10
    """
    amino_acids = 'ACDEFGHIKLMNPQRSTVWY'
    return ''.join(random.choices(amino_acids, k=length))


# ============================================================================
# 序列格式化
# ============================================================================

def format_sequence(sequence: str, line_width: int = 80) -> str:
    """
    格式化序列（每行固定宽度）。
    
    Args:
        sequence: 序列字符串
        line_width: 每行宽度
        
    Returns:
        str: 格式化后的序列
        
    Example:
        >>> print(format_sequence("ATCGATCG", line_width=4))
        ATCG
        ATCG
    """
    return '\n'.join(sequence[i:i+line_width] for i in range(0, len(sequence), line_width))


def format_fasta(sequence: str, header: str = "sequence", line_width: int = 60) -> str:
    """
    格式化为 FASTA 格式。
    
    Args:
        sequence: 序列字符串
        header: FASTA 头信息
        line_width: 每行宽度
        
    Returns:
        str: FASTA 格式字符串
        
    Example:
        >>> print(format_fasta("ATCG", "test_seq"))
        >test_seq
        ATCG
    """
    formatted_seq = format_sequence(sequence, line_width)
    return f">{header}\n{formatted_seq}"


def parse_fasta(fasta_text: str) -> Dict[str, str]:
    """
    解析 FASTA 格式文本。
    
    Args:
        fasta_text: FASTA 格式文本
        
    Returns:
        Dict[str, str]: {序列名: 序列}
        
    Example:
        >>> fasta = ">seq1\\nATCG\\n>seq2\\nGCTA"
        >>> parse_fasta(fasta)
        {'seq1': 'ATCG', 'seq2': 'GCTA'}
    """
    sequences = {}
    current_header = None
    current_seq = []
    
    for line in fasta_text.strip().split('\n'):
        line = line.strip()
        if line.startswith('>'):
            if current_header is not None:
                sequences[current_header] = ''.join(current_seq)
            current_header = line[1:].split()[0]
            current_seq = []
        elif line:
            current_seq.append(line)
    
    if current_header is not None:
        sequences[current_header] = ''.join(current_seq)
    
    return sequences


def format_protein(protein: str, line_width: int = 10, group_width: int = 10) -> str:
    """
    格式化蛋白质序列（带位置标记）。
    
    Args:
        protein: 蛋白质序列
        line_width: 每行氨基酸数
        group_width: 分组宽度
        
    Returns:
        str: 格式化后的蛋白质序列
    """
    lines = []
    for i in range(0, len(protein), line_width):
        chunk = protein[i:i + line_width]
        groups = ' '.join(chunk[j:j + group_width] for j in range(0, len(chunk), group_width))
        lines.append(f"{i + 1:4d} {groups}")
    return '\n'.join(lines)


# ============================================================================
# 便捷函数
# ============================================================================

def dna_to_protein(dna: str) -> str:
    """DNA 直接翻译为蛋白质（便捷函数）。"""
    return translate_dna(dna)


def rna_to_protein(rna: str) -> str:
    """RNA 翻译为蛋白质（便捷函数）。"""
    return translate(rna)


def is_coding_strand(dna: str, min_orf_length: int = 100) -> bool:
    """
    判断 DNA 是否可能是编码链。
    
    Args:
        dna: DNA 序列
        min_orf_length: 最小 ORF 长度
        
    Returns:
        bool: 是否可能是编码链
    """
    orfs = find_orfs(dna, min_orf_length)
    return len(orfs) > 0


def get_reading_frames(dna: str) -> Dict[int, str]:
    """
    获取 DNA 的所有阅读框翻译结果。
    
    Args:
        dna: DNA 序列
        
    Returns:
        Dict[int, str]: {阅读框: 蛋白质序列}
    """
    return {
        1: translate_dna(dna, 0),
        2: translate_dna(dna, 1),
        3: translate_dna(dna, 2),
        -1: translate_dna(reverse_complement_dna(dna), 0),
        -2: translate_dna(reverse_complement_dna(dna), 1),
        -3: translate_dna(reverse_complement_dna(dna), 2),
    }


def amino_acid_info(aa: str) -> Dict:
    """
    获取氨基酸详细信息。
    
    Args:
        aa: 氨基酸单字母代码
        
    Returns:
        Dict: 氨基酸信息字典
    """
    aa = aa.upper()
    if aa not in AMINO_ACID_CODES:
        raise ValueError(f"未知氨基酸: {aa}")
    
    return {
        'code': aa,
        'three_letter': AMINO_ACID_CODES[aa],
        'name_zh': AMINO_ACID_NAMES_ZH.get(aa, ''),
        'codons': get_codons(aa),
        'codon_count': len(get_codons(aa)),
    }


# ============================================================================
# 导出
# ============================================================================

__all__ = [
    # 类型
    'SequenceType',
    'NucleotideError',
    'CodonError',
    
    # 常量
    'DNA_BASES',
    'RNA_BASES',
    'IUPAC_DNA',
    'CODON_TABLE',
    'START_CODONS',
    'STOP_CODONS',
    'AMINO_ACID_CODES',
    'AMINO_ACID_NAMES_ZH',
    
    # 验证
    'is_valid_dna',
    'is_valid_rna',
    'is_valid_protein',
    'detect_sequence_type',
    'validate_sequence',
    
    # 转换
    'transcribe',
    'reverse_transcribe',
    'translate',
    'translate_dna',
    'complement_dna',
    'complement_rna',
    'reverse_complement_dna',
    'reverse_complement_rna',
    
    # GC 含量
    'gc_content',
    'gc_content_window',
    
    # 密码子
    'get_amino_acid',
    'get_codons',
    'is_start_codon',
    'is_stop_codon',
    'codon_usage',
    
    # 统计
    'nucleotide_count',
    'molecular_weight',
    'melting_temperature',
    'find_orfs',
    
    # 突变
    'point_mutation',
    'deletion',
    'insertion',
    'substitution',
    'random_mutation',
    
    # 比对
    'hamming_distance',
    'sequence_identity',
    'find_motif',
    'find_palindromes',
    
    # 生成
    'random_dna',
    'random_rna',
    'random_protein',
    
    # 格式化
    'format_sequence',
    'format_fasta',
    'parse_fasta',
    'format_protein',
    
    # 便捷函数
    'dna_to_protein',
    'rna_to_protein',
    'is_coding_strand',
    'get_reading_frames',
    'amino_acid_info',
]
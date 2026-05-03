"""
Sequence Alignment Utils 使用示例

展示序列比对工具的多种应用场景：
1. DNA 序列比对
2. 蛋白质序列比对
3. 文本相似度计算
4. 拼写检查辅助
5. 多序列比对
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    needleman_wunsch,
    smith_waterman,
    edit_distance,
    damerau_levenshtein_distance,
    hamming_distance,
    jaro_distance,
    jaro_winkler_distance,
    sequence_identity,
    multiple_sequence_alignment,
    find_consensus,
    global_alignment,
    local_alignment,
    AlignmentResult,
    ScoringMatrix
)


def example_1_dna_sequence_alignment():
    """
    示例1: DNA 序列比对
    
    比较两条 DNA 序列，找出突变位点
    """
    print("=" * 60)
    print("示例1: DNA 序列比对")
    print("=" * 60)
    
    # 两条 DNA 序列
    dna1 = "ATCGATCGATCG"
    dna2 = "ATCGATAGATCG"  # 有一个点突变
    
    print(f"序列1: {dna1}")
    print(f"序列2: {dna2}")
    print()
    
    # 全局比对
    result = global_alignment(dna1, dna2, scoring_matrix=ScoringMatrix.DNA_SIMPLE)
    print("全局比对结果:")
    print(result.format_alignment())
    
    # 统计信息
    print(f"比对得分: {result.score}")
    print(f"序列一致性: {result.identity:.1%}")
    print(f"空位数: {result.gaps}")


def example_2_protein_sequence_alignment():
    """
    示例2: 蛋白质序列比对
    
    使用 BLOSUM62 评分矩阵进行蛋白质比对
    """
    print("\n" + "=" * 60)
    print("示例2: 蛋白质序列比对")
    print("=" * 60)
    
    # 简短的蛋白质序列
    protein1 = "HELLO"  # 用字母模拟
    protein2 = "HALLO"
    
    print(f"序列1: {protein1}")
    print(f"序列2: {protein2}")
    print()
    
    # 使用 BLOSUM62 评分矩阵
    result = global_alignment(
        protein1, protein2,
        scoring_matrix=ScoringMatrix.BLOSUM62_SIMPLE
    )
    
    print("全局比对结果:")
    print(result.format_alignment())
    
    # 局部比对
    local_result = local_alignment(protein1, protein2)
    print("\n局部比对结果:")
    print(local_result.format_alignment())


def example_3_text_similarity():
    """
    示例3: 文本相似度计算
    
    使用多种距离度量比较文本
    """
    print("\n" + "=" * 60)
    print("示例3: 文本相似度计算")
    print("=" * 60)
    
    texts = [
        ("kitten", "sitting"),
        ("hello", "hallo"),
        ("world", "word"),
        ("algorithm", "altruistic"),
        ("自然语言", "自然处理")
    ]
    
    for text1, text2 in texts:
        print(f"\n'{text1}' vs '{text2}'")
        print(f"  编辑距离: {edit_distance(text1, text2)}")
        print(f"  Damerau-Levenshtein: {damerau_levenshtein_distance(text1, text2)}")
        
        # 汉明距离（等长）
        if len(text1) == len(text2):
            print(f"  汉明距离: {hamming_distance(text1, text2)}")
        
        print(f"  Jaro 相似度: {jaro_distance(text1, text2):.3f}")
        print(f"  Jaro-Winkler: {jaro_winkler_distance(text1, text2):.3f}")
        print(f"  序列一致性: {sequence_identity(text1, text2):.1%}")


def example_4_spell_check_assistant():
    """
    示例4: 拼写检查辅助
    
    从候选词中找出最接近的匹配
    """
    print("\n" + "=" * 60)
    print("示例4: 拼写检查辅助")
    print("=" * 60)
    
    # 用户可能输入的错误拼写
    input_word = "kitten"
    
    # 候选正确词汇
    candidates = ["kitchen", "kitten", "kitting", "sitting", "kittens"]
    
    print(f"输入词: '{input_word}'")
    print("候选词列表:")
    
    # 计算与每个候选词的距离
    results = []
    for candidate in candidates:
        ed = edit_distance(input_word, candidate)
        jw = jaro_winkler_distance(input_word, candidate)
        results.append((candidate, ed, jw))
        print(f"  {candidate}: 编辑距离={ed}, Jaro-Winkler={jw:.3f}")
    
    # 找最佳匹配
    best_by_ed = min(results, key=lambda x: x[1])
    best_by_jw = max(results, key=lambda x: x[2])
    
    print(f"\n最佳匹配 (编辑距离): '{best_by_ed[0]}'")
    print(f"最佳匹配 (Jaro-Winkler): '{best_by_jw[0]}'")


def example_5_multiple_sequence_alignment():
    """
    示例5: 多序列比对
    
    对多条序列进行比对并生成一致序列
    """
    print("\n" + "=" * 60)
    print("示例5: 多序列比对")
    print("=" * 60)
    
    # 多条相关序列
    sequences = [
        "ACGTACGT",
        "ACGAACGT",
        "ACGTACCT",
        "AGGTACGT"
    ]
    
    print("原始序列:")
    for i, seq in enumerate(sequences, 1):
        print(f"  Seq{i}: {seq}")
    
    # 多序列比对
    aligned = multiple_sequence_alignment(sequences)
    
    print("\n比对结果:")
    for i, seq in enumerate(aligned, 1):
        print(f"  Seq{i}: {seq}")
    
    # 生成一致序列
    consensus = find_consensus(aligned)
    print(f"\n一致序列: {consensus}")


def example_6_local_alignment_substring():
    """
    示例6: 局部比对找相似子串
    
    在长序列中找最相似的片段
    """
    print("\n" + "=" * 60)
    print("示例6: 局部比对找相似子串")
    print("=" * 60)
    
    # 长序列和查询序列
    long_seq = "ACGTACGTACGTACGTACGT"
    query_seq = "ACGAACGT"
    
    print(f"长序列: {long_seq}")
    print(f"查询序列: {query_seq}")
    print()
    
    # 局部比对
    result = local_alignment(long_seq, query_seq)
    print("局部比对结果:")
    print(result.format_alignment())
    print(f"\n在长序列中找到相似片段: '{result.seq1_aligned}'")


def example_7_compare_distance_metrics():
    """
    示例7: 比较不同距离度量
    
    对同一对字符串使用不同度量
    """
    print("\n" + "=" * 60)
    print("示例7: 比较不同距离度量")
    print("=" * 60)
    
    pairs = [
        ("abcd", "abcd"),
        ("abcd", "abc"),
        ("abcd", "abce"),
        ("abcd", "bacd"),  # 相邻交换
    ]
    
    print("比较不同字符串对的距离度量:\n")
    
    for s1, s2 in pairs:
        print(f"'{s1}' vs '{s2}'")
        
        # 编辑距离
        ed = edit_distance(s1, s2)
        dl = damerau_levenshtein_distance(s1, s2)
        j = jaro_distance(s1, s2)
        jw = jaro_winkler_distance(s1, s2)
        
        # 汉明距离（等长时）
        hm = hamming_distance(s1, s2) if len(s1) == len(s2) else "N/A"
        
        print(f"  编辑距离: {ed}")
        print(f"  Damerau-Levenshtein: {dl}")
        print(f"  汉明距离: {hm}")
        print(f"  Jaro: {j:.3f}")
        print(f"  Jaro-Winkler: {jw:.3f}")
        print()


def example_8_custom_scoring():
    """
    示例8: 自定义评分参数
    
    使用不同的评分参数影响比对结果
    """
    print("\n" + "=" * 60)
    print("示例8: 自定义评分参数")
    print("=" * 60)
    
    seq1 = "ACGT"
    seq2 = "AC"
    
    print(f"序列1: {seq1}")
    print(f"序列2: {seq2}")
    print()
    
    # 默认参数
    result1 = global_alignment(seq1, seq2)
    print("默认参数:")
    print(result1.format_alignment())
    
    # 严厉的空位惩罚
    result2 = global_alignment(seq1, seq2, gap_penalty=-5)
    print("\n严厉空位惩罚 (gap=-5):")
    print(result2.format_alignment())
    
    # 宽容的空位惩罚
    result3 = global_alignment(seq1, seq2, gap_penalty=-1)
    print("\n宽容空位惩罚 (gap=-1):")
    print(result3.format_alignment())


def example_9_chinese_text():
    """
    示例9: 中文文本比对
    
    对中文字符串进行比对
    """
    print("\n" + "=" * 60)
    print("示例9: 中文文本比对")
    print("=" * 60)
    
    chinese_texts = [
        ("今天天气很好", "今天天气不错"),
        ("机器学习算法", "深度学习算法"),
        ("自然语言处理", "自然语言理解"),
    ]
    
    for text1, text2 in chinese_texts:
        print(f"\n'{text1}' vs '{text2}'")
        
        # 全局比对
        result = global_alignment(text1, text2)
        print(f"  编辑距离: {edit_distance(text1, text2)}")
        print(f"  序列一致性: {result.identity:.1%}")
        print(f"  Jaro-Winkler: {jaro_winkler_distance(text1, text2):.3f}")


def example_10_alignment_statistics():
    """
    示例10: 比对统计信息详解
    
    理解比对结果的各项统计
    """
    print("\n" + "=" * 60)
    print("示例10: 比对统计信息详解")
    print("=" * 60)
    
    seq1 = "ACGTACGTACGT"
    seq2 = "ACGAACGTTCGT"
    
    result = global_alignment(seq1, seq2)
    
    print(f"序列1: {seq1}")
    print(f"序列2: {seq2}")
    print()
    print(result.format_alignment())
    
    print("\n统计信息解释:")
    print(f"  Score: {result.score} - 比对的总得分")
    print(f"  Identity: {result.identity:.1%} - 完全匹配的比例")
    print(f"  Similarity: {result.similarity:.1%} - 相似（含匹配）的比例")
    print(f"  Gaps: {result.gaps} - 空位数量")


def run_all_examples():
    """运行所有示例"""
    example_1_dna_sequence_alignment()
    example_2_protein_sequence_alignment()
    example_3_text_similarity()
    example_4_spell_check_assistant()
    example_5_multiple_sequence_alignment()
    example_6_local_alignment_substring()
    example_7_compare_distance_metrics()
    example_8_custom_scoring()
    example_9_chinese_text()
    example_10_alignment_statistics()
    
    print("\n" + "=" * 60)
    print("所有示例运行完成!")
    print("=" * 60)


if __name__ == "__main__":
    run_all_examples()
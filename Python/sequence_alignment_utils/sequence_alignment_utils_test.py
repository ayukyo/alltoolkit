"""
Sequence Alignment Utils 测试文件

测试所有序列比对功能：
- Needleman-Wunsch 全局比对
- Smith-Waterman 局部比对
- 编辑距离计算
- 其他距离度量
"""

import unittest
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
    align,
    AlignmentType,
    AlignmentResult,
    ScoringMatrix
)


class TestNeedlemanWunsch(unittest.TestCase):
    """Needleman-Wunsch 全局比对测试"""
    
    def test_identical_sequences(self):
        """测试相同序列"""
        result = needleman_wunsch("ACGT", "ACGT")
        self.assertEqual(result.seq1_aligned, "ACGT")
        self.assertEqual(result.seq2_aligned, "ACGT")
        self.assertEqual(result.score, 4)
        self.assertEqual(result.identity, 1.0)
        self.assertEqual(result.gaps, 0)
    
    def test_different_sequences(self):
        """测试不同序列"""
        result = needleman_wunsch("ACGT", "AGCT")
        self.assertEqual(result.seq1_aligned, "ACGT")
        self.assertEqual(result.seq2_aligned, "AGCT")
        self.assertIn(result.score, [0, 2])  # 取决于参数
    
    def test_with_gaps(self):
        """测试包含空位的比对"""
        result = needleman_wunsch("ACGT", "ACT")
        # 应该在某个位置插入空位
        self.assertIn('-', result.seq1_aligned + result.seq2_aligned)
        self.assertTrue(result.gaps > 0)
    
    def test_empty_sequences(self):
        """测试空序列"""
        result = needleman_wunsch("", "")
        self.assertEqual(result.seq1_aligned, "")
        self.assertEqual(result.seq2_aligned, "")
        self.assertEqual(result.score, 0)
    
    def test_one_empty_sequence(self):
        """测试一条空序列"""
        result = needleman_wunsch("ACGT", "")
        self.assertEqual(result.seq1_aligned, "ACGT")
        self.assertEqual(result.seq2_aligned, "----")
        self.assertEqual(result.gaps, 4)
    
    def test_custom_scoring(self):
        """测试自定义评分"""
        result1 = needleman_wunsch("A", "A", match_score=5, mismatch_score=-3, gap_penalty=-2)
        self.assertEqual(result1.score, 5)
        
        result2 = needleman_wunsch("A", "T", match_score=5, mismatch_score=-3, gap_penalty=-2)
        # 可能是替换或两个空位
        self.assertTrue(result2.score < 5)
    
    def test_long_sequences(self):
        """测试较长序列"""
        seq1 = "ACGTACGTACGTACGT"
        seq2 = "ACGAACGTACGTTCGT"
        result = needleman_wunsch(seq1, seq2)
        self.assertTrue(len(result.seq1_aligned) >= len(seq1))
        self.assertTrue(result.identity >= 0.5)
    
    def test_alignment_type(self):
        """测试比对类型"""
        result = needleman_wunsch("AC", "AC")
        self.assertEqual(result.alignment_type, AlignmentType.GLOBAL)


class TestSmithWaterman(unittest.TestCase):
    """Smith-Waterman 局部比对测试"""
    
    def test_identical_sequences(self):
        """测试相同序列"""
        result = smith_waterman("ACGT", "ACGT")
        self.assertEqual(result.seq1_aligned, "ACGT")
        self.assertEqual(result.seq2_aligned, "ACGT")
        self.assertEqual(result.alignment_type, AlignmentType.LOCAL)
    
    def test_partial_match(self):
        """测试部分匹配"""
        result = smith_waterman("ACGTACGT", "TTTACGTTTT")
        self.assertIn("ACGT", result.seq1_aligned)
        self.assertTrue(result.score > 0)
    
    def test_no_match(self):
        """测试无匹配"""
        result = smith_waterman("AAAA", "TTTT")
        # 局部比对如果分数为0可能返回空
        self.assertTrue(result.score >= 0)
    
    def test_substring(self):
        """测试子字符串"""
        result = smith_waterman("ACGT", "ACGTACGTACGT")
        self.assertEqual(result.seq1_aligned, "ACGT")
        self.assertEqual(result.seq2_aligned, "ACGT")
    
    def test_empty_sequences(self):
        """测试空序列"""
        result = smith_waterman("", "")
        self.assertEqual(result.score, 0)
    
    def test_different_parameters(self):
        """测试不同参数"""
        result1 = smith_waterman("ACGT", "ACGT", match_score=1)
        result2 = smith_waterman("ACGT", "ACGT", match_score=3)
        self.assertTrue(result2.score > result1.score)


class TestEditDistance(unittest.TestCase):
    """编辑距离测试"""
    
    def test_identical_strings(self):
        """测试相同字符串"""
        self.assertEqual(edit_distance("hello", "hello"), 0)
    
    def test_one_insertion(self):
        """测试单次插入"""
        self.assertEqual(edit_distance("hello", "helloo"), 1)
    
    def test_one_deletion(self):
        """测试单次删除"""
        self.assertEqual(edit_distance("hello", "helo"), 1)
    
    def test_one_substitution(self):
        """测试单次替换"""
        self.assertEqual(edit_distance("hello", "hallo"), 1)
    
    def test_multiple_operations(self):
        """测试多次操作"""
        self.assertEqual(edit_distance("kitten", "sitting"), 3)
    
    def test_empty_strings(self):
        """测试空字符串"""
        self.assertEqual(edit_distance("", ""), 0)
        self.assertEqual(edit_distance("hello", ""), 5)
        self.assertEqual(edit_distance("", "hello"), 5)
    
    def test_completely_different(self):
        """测试完全不同的字符串"""
        self.assertEqual(edit_distance("abc", "xyz"), 3)
    
    def test_custom_costs(self):
        """测试自定义代价"""
        # 默认代价
        d1 = edit_distance("ab", "ba")
        # 替换代价更高时
        d2 = edit_distance("ab", "ba", substitution_cost=3)
        self.assertTrue(d2 >= d1)


class TestDamerauLevenshtein(unittest.TestCase):
    """Damerau-Levenshtein 距离测试"""
    
    def test_identical_strings(self):
        """测试相同字符串"""
        self.assertEqual(damerau_levenshtein_distance("hello", "hello"), 0)
    
    def test_transposition(self):
        """测试相邻交换"""
        # 普通编辑距离需要2次操作
        self.assertEqual(edit_distance("ab", "ba"), 2)
        # Damerau-Levenshtein 只需要1次交换
        self.assertEqual(damerau_levenshtein_distance("ab", "ba"), 1)
    
    def test_multiple_transpositions(self):
        """测试多次交换"""
        self.assertEqual(damerau_levenshtein_distance("abc", "cba"), 2)
    
    def test_empty_strings(self):
        """测试空字符串"""
        self.assertEqual(damerau_levenshtein_distance("", ""), 0)
        self.assertEqual(damerau_levenshtein_distance("abc", ""), 3)


class TestHammingDistance(unittest.TestCase):
    """汉明距离测试"""
    
    def test_identical_strings(self):
        """测试相同字符串"""
        self.assertEqual(hamming_distance("hello", "hello"), 0)
    
    def test_one_difference(self):
        """测试一个差异"""
        self.assertEqual(hamming_distance("hello", "hallo"), 1)
    
    def test_all_different(self):
        """测试完全不同"""
        self.assertEqual(hamming_distance("abc", "xyz"), 3)
    
    def test_different_lengths(self):
        """测试不同长度"""
        with self.assertRaises(ValueError):
            hamming_distance("abc", "abcd")


class TestJaroDistance(unittest.TestCase):
    """Jaro 距离测试"""
    
    def test_identical_strings(self):
        """测试相同字符串"""
        self.assertEqual(jaro_distance("hello", "hello"), 1.0)
    
    def test_completely_different(self):
        """测试完全不同"""
        self.assertEqual(jaro_distance("abc", "xyz"), 0.0)
    
    def test_empty_strings(self):
        """测试空字符串"""
        self.assertEqual(jaro_distance("", ""), 1.0)
        self.assertEqual(jaro_distance("abc", ""), 0.0)
    
    def test_similar_strings(self):
        """测试相似字符串"""
        # "MARTHA" vs "MARHTA"
        d = jaro_distance("MARTHA", "MARHTA")
        self.assertTrue(0.8 < d < 1.0)
    
    def test_partial_match(self):
        """测试部分匹配"""
        d = jaro_distance("hello", "hallo")
        self.assertTrue(0.5 < d < 1.0)


class TestJaroWinklerDistance(unittest.TestCase):
    """Jaro-Winkler 距离测试"""
    
    def test_identical_strings(self):
        """测试相同字符串"""
        self.assertEqual(jaro_winkler_distance("hello", "hello"), 1.0)
    
    def test_common_prefix(self):
        """测试公共前缀"""
        # Jaro-Winkler 会奖励公共前缀
        jw1 = jaro_winkler_distance("hello", "hallo")
        jw2 = jaro_winkler_distance("xyzlo", "xyalo")
        # hello/hallo 比 xyzlo/xyalo 有更长的公共前缀
        # 但实际上这里前缀相同，所以测试其他情况
        
        jw_short = jaro_winkler_distance("ab", "ac")
        jw_long = jaro_winkler_distance("abcdefgh", "abcdefghi")
        self.assertTrue(jw_long > jw_short)
    
    def test_vs_jaro(self):
        """测试 Jaro-Winkler vs Jaro"""
        j = jaro_distance("hello", "hallo")
        jw = jaro_winkler_distance("hello", "hallo")
        # Jaro-Winkler 应该 >= Jaro
        self.assertTrue(jw >= j)


class TestSequenceIdentity(unittest.TestCase):
    """序列一致性测试"""
    
    def test_identical_sequences(self):
        """测试相同序列"""
        self.assertEqual(sequence_identity("ACGT", "ACGT"), 1.0)
    
    def test_different_sequences(self):
        """测试不同序列"""
        identity = sequence_identity("ACGT", "AGCT")
        self.assertTrue(0 < identity < 1.0)
    
    def test_empty_sequences(self):
        """测试空序列"""
        self.assertEqual(sequence_identity("", ""), 1.0)
        self.assertEqual(sequence_identity("", "ACGT"), 0.0)


class TestMultipleSequenceAlignment(unittest.TestCase):
    """多序列比对测试"""
    
    def test_single_sequence(self):
        """测试单序列"""
        result = multiple_sequence_alignment(["ACGT"])
        self.assertEqual(result, ["ACGT"])
    
    def test_empty_list(self):
        """测试空列表"""
        result = multiple_sequence_alignment([])
        self.assertEqual(result, [])
    
    def test_two_sequences(self):
        """测试两条序列"""
        result = multiple_sequence_alignment(["ACGT", "ACGT"])
        self.assertEqual(len(result), 2)
        self.assertEqual(len(result[0]), len(result[1]))
    
    def test_multiple_sequences(self):
        """测试多条序列"""
        seqs = ["ACGT", "ACGT", "ACGT"]
        result = multiple_sequence_alignment(seqs)
        self.assertEqual(len(result), 3)
        # 所有序列应该等长
        lengths = [len(s) for s in result]
        self.assertEqual(len(set(lengths)), 1)
    
    def test_different_lengths(self):
        """测试不同长度序列"""
        seqs = ["AC", "ACGT", "A"]
        result = multiple_sequence_alignment(seqs)
        # 比对后长度应该一致
        self.assertTrue(all(len(s) == len(result[0]) for s in result))


class TestFindConsensus(unittest.TestCase):
    """一致序列测试"""
    
    def test_identical_sequences(self):
        """测试相同序列"""
        result = find_consensus(["ACGT", "ACGT", "ACGT"])
        self.assertEqual(result, "ACGT")
    
    def test_with_gaps(self):
        """测试包含空位"""
        result = find_consensus(["ACGT", "A-GT", "AC-T"])
        # 应该选择多数票
        self.assertIn(result[0], "A")
        self.assertIn(result[2], "G")  # 位置2: G, -, G -> G
    
    def test_empty_list(self):
        """测试空列表"""
        result = find_consensus([])
        self.assertEqual(result, "")
    
    def test_single_sequence(self):
        """测试单序列"""
        result = find_consensus(["ACGT"])
        self.assertEqual(result, "ACGT")


class TestConvenienceFunctions(unittest.TestCase):
    """便捷函数测试"""
    
    def test_global_alignment(self):
        """测试全局比对便捷函数"""
        result = global_alignment("ACGT", "ACGT")
        self.assertEqual(result.alignment_type, AlignmentType.GLOBAL)
    
    def test_local_alignment(self):
        """测试局部比对便捷函数"""
        result = local_alignment("ACGT", "ACGT")
        self.assertEqual(result.alignment_type, AlignmentType.LOCAL)
    
    def test_align_default(self):
        """测试默认比对模式"""
        result = align("ACGT", "ACGT")
        self.assertEqual(result.alignment_type, AlignmentType.GLOBAL)
    
    def test_align_local(self):
        """测试指定局部比对"""
        result = align("ACGT", "ACGT", mode="local")
        self.assertEqual(result.alignment_type, AlignmentType.LOCAL)


class TestAlignmentResult(unittest.TestCase):
    """比对结果测试"""
    
    def test_repr(self):
        """测试字符串表示"""
        result = needleman_wunsch("AC", "AC")
        repr_str = repr(result)
        self.assertIn("score", repr_str)
        self.assertIn("identity", repr_str)
    
    def test_format_alignment(self):
        """测试格式化输出"""
        result = needleman_wunsch("ACGT", "ACGT")
        formatted = result.format_alignment()
        self.assertIn("Score:", formatted)
        self.assertIn("Identity:", formatted)
        self.assertIn("Seq1:", formatted)
        self.assertIn("Seq2:", formatted)


class TestScoringMatrix(unittest.TestCase):
    """评分矩阵测试"""
    
    def test_dna_matrix(self):
        """测试 DNA 评分矩阵"""
        self.assertEqual(ScoringMatrix.get_score('A', 'A', ScoringMatrix.DNA_SIMPLE), 1)
        self.assertEqual(ScoringMatrix.get_score('A', 'T', ScoringMatrix.DNA_SIMPLE), -1)
    
    def test_default_scoring(self):
        """测试默认评分"""
        self.assertEqual(ScoringMatrix.get_score('A', 'A'), 1)
        self.assertEqual(ScoringMatrix.get_score('A', 'T'), -1)
    
    def test_case_insensitive(self):
        """测试大小写不敏感"""
        self.assertEqual(ScoringMatrix.get_score('a', 'A', ScoringMatrix.DNA_SIMPLE), 1)


class TestDNABioSequences(unittest.TestCase):
    """DNA 生物序列测试"""
    
    def test_dna_alignment(self):
        """测试 DNA 序列比对"""
        seq1 = "ATCGATCGATCG"
        seq2 = "ATCGATCGATCG"
        result = needleman_wunsch(seq1, seq2, scoring_matrix=ScoringMatrix.DNA_SIMPLE)
        self.assertEqual(result.identity, 1.0)
    
    def test_dna_with_mutation(self):
        """测试 DNA 突变检测"""
        seq1 = "ATCGATCGATCG"
        seq2 = "ATCGATAGATCG"  # 一个突变
        result = needleman_wunsch(seq1, seq2, scoring_matrix=ScoringMatrix.DNA_SIMPLE)
        self.assertTrue(result.identity < 1.0)
    
    def test_dna_with_insertion(self):
        """测试 DNA 插入检测"""
        seq1 = "ATCG"
        seq2 = "ATTCG"  # 插入一个 T
        result = needleman_wunsch(seq1, seq2)
        self.assertTrue(result.gaps > 0)


class TestProteinSequences(unittest.TestCase):
    """蛋白质序列测试"""
    
    def test_protein_alignment(self):
        """测试蛋白质序列比对"""
        seq1 = "MAGIC"
        seq2 = "MAGIC"
        result = needleman_wunsch(seq1, seq2, scoring_matrix=ScoringMatrix.BLOSUM62_SIMPLE)
        self.assertEqual(result.identity, 1.0)
    
    def test_protein_with_substitution(self):
        """测试蛋白质替换"""
        seq1 = "MAGIC"
        seq2 = "MAGIS"  # C -> S
        result = needleman_wunsch(seq1, seq2, scoring_matrix=ScoringMatrix.BLOSUM62_SIMPLE)
        self.assertTrue(result.identity < 1.0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
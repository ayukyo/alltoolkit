"""
DNA Utils 测试套件

全面测试 dna_utils 模块的所有功能。
"""

import unittest
from mod import (
    # 类型
    SequenceType, NucleotideError, CodonError,
    # 验证
    is_valid_dna, is_valid_rna, is_valid_protein,
    detect_sequence_type, validate_sequence,
    # 转换
    transcribe, reverse_transcribe, translate, translate_dna,
    complement_dna, complement_rna, reverse_complement_dna, reverse_complement_rna,
    # GC 含量
    gc_content, gc_content_window,
    # 密码子
    get_amino_acid, get_codons, is_start_codon, is_stop_codon, codon_usage,
    # 统计
    nucleotide_count, molecular_weight, melting_temperature, find_orfs,
    # 突变
    point_mutation, deletion, insertion, substitution, random_mutation,
    # 比对
    hamming_distance, sequence_identity, find_motif, find_palindromes,
    # 生成
    random_dna, random_rna, random_protein,
    # 格式化
    format_sequence, format_fasta, parse_fasta, format_protein,
    # 便捷函数
    dna_to_protein, rna_to_protein, is_coding_strand, get_reading_frames,
    amino_acid_info,
)


class TestSequenceValidation(unittest.TestCase):
    """序列验证测试"""
    
    def test_is_valid_dna(self):
        """测试 DNA 验证"""
        self.assertTrue(is_valid_dna("ATCG"))
        self.assertTrue(is_valid_dna("atcg"))
        self.assertTrue(is_valid_dna("ATCGN"))  # 模糊碱基
        self.assertTrue(is_valid_dna("ATCGRYSWKMBDHV"))  # 所有 IUPAC 碱基
        self.assertFalse(is_valid_dna("ATCGU"))  # RNA 碱基
        self.assertFalse(is_valid_dna("ATCGX"))  # 无效碱基
        self.assertFalse(is_valid_dna(""))
        self.assertFalse(is_valid_dna("123"))
    
    def test_is_valid_rna(self):
        """测试 RNA 验证"""
        self.assertTrue(is_valid_rna("AUCG"))
        self.assertTrue(is_valid_rna("aucg"))
        self.assertTrue(is_valid_rna("AUCGN"))  # 模糊碱基
        self.assertFalse(is_valid_rna("ATCG"))  # DNA 碱基
        self.assertFalse(is_valid_rna("AUCGX"))
        self.assertFalse(is_valid_rna(""))
    
    def test_is_valid_protein(self):
        """测试蛋白质验证"""
        self.assertTrue(is_valid_protein("MVLSPADK"))
        self.assertTrue(is_valid_protein("mvlspadk"))
        self.assertTrue(is_valid_protein("MVLSPADK*"))  # 包含终止符
        self.assertFalse(is_valid_protein("MVLSPADX"))
        self.assertFalse(is_valid_protein(""))
    
    def test_detect_sequence_type(self):
        """测试序列类型检测"""
        self.assertEqual(detect_sequence_type("ATCG"), SequenceType.DNA)
        self.assertEqual(detect_sequence_type("AUCG"), SequenceType.RNA)
        self.assertEqual(detect_sequence_type("MVLSPADK"), SequenceType.PROTEIN)
        self.assertIsNone(detect_sequence_type(""))
        self.assertIsNone(detect_sequence_type("ATCGU"))  # 同时含 T 和 U
    
    def test_validate_sequence(self):
        """测试序列验证详情"""
        valid, msg = validate_sequence("ATCG", SequenceType.DNA)
        self.assertTrue(valid)
        self.assertIn("DNA", msg)
        
        valid, msg = validate_sequence("AUCG", SequenceType.RNA)
        self.assertTrue(valid)
        self.assertIn("RNA", msg)
        
        valid, msg = validate_sequence("AUCG", SequenceType.DNA)
        self.assertFalse(valid)
        self.assertIn("非 DNA", msg)
        
        valid, msg = validate_sequence("")
        self.assertFalse(valid)
        self.assertIn("空序列", msg)


class TestSequenceConversion(unittest.TestCase):
    """序列转换测试"""
    
    def test_transcribe(self):
        """测试 DNA 转录"""
        self.assertEqual(transcribe("ATCG"), "AUCG")
        self.assertEqual(transcribe("TTTT"), "UUUU")
        self.assertEqual(transcribe("AAAA"), "AAAA")
        self.assertEqual(transcribe("atcg"), "AUCG")
        
        with self.assertRaises(NucleotideError):
            transcribe("AUCG")  # RNA 不能转录
    
    def test_reverse_transcribe(self):
        """测试 RNA 逆转录"""
        self.assertEqual(reverse_transcribe("AUCG"), "ATCG")
        self.assertEqual(reverse_transcribe("UUUU"), "TTTT")
        
        with self.assertRaises(NucleotideError):
            reverse_transcribe("ATCG")  # DNA 不能逆转录
    
    def test_translate(self):
        """测试 RNA 翻译"""
        # AUG (M) - GCC (A) - UAA (Stop)
        self.assertEqual(translate("AUGGCCUAA"), "MA*")
        # AUG (M) - UUU (F) - UUU (F)
        self.assertEqual(translate("AUGUUUUUU"), "MFF")
        
        with self.assertRaises(NucleotideError):
            translate("ATCG")  # DNA 不能直接翻译
        
        # 长度不是 3 的倍数，最后一个不完整密码子被忽略
        self.assertEqual(translate("AAAAA"), "K")  # AAA = K, 最后两个 A 被忽略
    
    def test_translate_dna(self):
        """测试 DNA 直接翻译"""
        self.assertEqual(translate_dna("ATGGCCTAA"), "MA*")
        # ATG TTT AAA TGA = M F K * (AAA = K/Lysine)
        self.assertEqual(translate_dna("ATGTTTAAATGA"), "MFK*")
    
    def test_complement_dna(self):
        """测试 DNA 互补"""
        self.assertEqual(complement_dna("ATCG"), "TAGC")
        self.assertEqual(complement_dna("AAAA"), "TTTT")
        self.assertEqual(complement_dna("GGGG"), "CCCC")
        self.assertEqual(complement_dna("atcg"), "tagc")
    
    def test_complement_rna(self):
        """测试 RNA 互补"""
        self.assertEqual(complement_rna("AUCG"), "UAGC")
        self.assertEqual(complement_rna("AAAA"), "UUUU")
    
    def test_reverse_complement_dna(self):
        """测试 DNA 反向互补"""
        self.assertEqual(reverse_complement_dna("ATCG"), "CGAT")
        self.assertEqual(reverse_complement_dna("AATT"), "AATT")  # 回文
        self.assertEqual(reverse_complement_dna("GCAT"), "ATGC")
    
    def test_reverse_complement_rna(self):
        """测试 RNA 反向互补"""
        self.assertEqual(reverse_complement_rna("AUCG"), "CGAU")
        self.assertEqual(reverse_complement_rna("AAUU"), "AAUU")  # 回文


class TestGCContent(unittest.TestCase):
    """GC 含量测试"""
    
    def test_gc_content(self):
        """测试 GC 含量计算"""
        self.assertEqual(gc_content("GCGC"), 100.0)
        self.assertEqual(gc_content("ATAT"), 0.0)
        self.assertEqual(gc_content("ATCG"), 50.0)
        self.assertEqual(gc_content("GCGCATAT"), 50.0)
        self.assertEqual(gc_content(""), 0.0)
    
    def test_gc_content_rna(self):
        """测试 RNA GC 含量"""
        self.assertEqual(gc_content("GCGC", SequenceType.RNA), 100.0)
        self.assertEqual(gc_content("AUAU", SequenceType.RNA), 0.0)
    
    def test_gc_content_window(self):
        """测试滑动窗口 GC 含量"""
        results = gc_content_window("ATCGATCG", window_size=4)
        self.assertEqual(len(results), 5)
        for pos, gc in results:
            self.assertEqual(gc, 50.0)
        
        # 小序列
        results = gc_content_window("AT", window_size=100)
        self.assertEqual(len(results), 1)


class TestCodonOperations(unittest.TestCase):
    """密码子操作测试"""
    
    def test_get_amino_acid(self):
        """测试密码子到氨基酸转换"""
        self.assertEqual(get_amino_acid("AUG"), "M")  # 起始密码子
        self.assertEqual(get_amino_acid("UUU"), "F")
        self.assertEqual(get_amino_acid("UAA"), "*")  # 终止密码子
        self.assertEqual(get_amino_acid("ATG"), "M")  # DNA 密码子
    
    def test_get_codons(self):
        """测试氨基酸到密码子列表"""
        self.assertEqual(get_codons('M'), ['AUG'])  # 甲硫氨酸只有一个
        self.assertEqual(len(get_codons('L')), 6)  # 亮氨酸有 6 个密码子
        self.assertEqual(len(get_codons('S')), 6)  # 丝氨酸有 6 个密码子
    
    def test_is_start_codon(self):
        """测试起始密码子判断"""
        self.assertTrue(is_start_codon("AUG"))
        self.assertTrue(is_start_codon("ATG"))  # DNA 格式
        self.assertFalse(is_start_codon("UAA"))
        self.assertFalse(is_start_codon("UUU"))
    
    def test_is_stop_codon(self):
        """测试终止密码子判断"""
        self.assertTrue(is_stop_codon("UAA"))
        self.assertTrue(is_stop_codon("UAG"))
        self.assertTrue(is_stop_codon("UGA"))
        self.assertTrue(is_stop_codon("TAA"))  # DNA 格式
        self.assertFalse(is_stop_codon("AUG"))
        self.assertFalse(is_stop_codon("UUU"))
    
    def test_codon_usage(self):
        """测试密码子使用统计"""
        usage = codon_usage("AUGGCCAUGGCC")
        self.assertEqual(usage['AUG'], 2)
        self.assertEqual(usage['GCC'], 2)
        
        # DNA 格式
        usage = codon_usage("ATGGCCATGGCC")
        self.assertEqual(usage['AUG'], 2)


class TestSequenceStatistics(unittest.TestCase):
    """序列统计测试"""
    
    def test_nucleotide_count(self):
        """测试核苷酸计数"""
        count = nucleotide_count("ATCGATCG")
        self.assertEqual(count['A'], 2)
        self.assertEqual(count['T'], 2)
        self.assertEqual(count['C'], 2)
        self.assertEqual(count['G'], 2)
    
    def test_molecular_weight(self):
        """测试分子量计算"""
        # 单核苷酸
        mw = molecular_weight("A", SequenceType.DNA)
        self.assertAlmostEqual(mw, 313.2, places=1)
        
        # RNA
        mw = molecular_weight("A", SequenceType.RNA)
        self.assertAlmostEqual(mw, 347.2, places=1)
        
        # 多核苷酸（需要减去水分子）
        mw = molecular_weight("AT", SequenceType.DNA)
        expected = 313.2 + 304.2 - 18.0
        self.assertAlmostEqual(mw, expected, places=1)
    
    def test_melting_temperature(self):
        """测试熔解温度计算"""
        # basic 方法
        tm = melting_temperature("ATCG", method='basic')
        self.assertEqual(tm, 12.0)  # 4*2 + 2*2
        
        # Wallace 方法
        tm = melting_temperature("ATCGATCG", method='wallace')
        self.assertGreater(tm, 0)
    
    def test_find_orfs(self):
        """测试 ORF 查找"""
        # 包含一个简单 ORF
        dna = "ATGAAATAG"  # M-K-Stop
        orfs = find_orfs(dna, min_length=9)
        self.assertEqual(len(orfs), 1)
        self.assertEqual(orfs[0]['start'], 0)
        self.assertEqual(orfs[0]['length'], 9)
        self.assertEqual(orfs[0]['protein'], "MK")
        
        # 无有效 ORF
        dna = "AAAAAAAAAA"
        orfs = find_orfs(dna, min_length=9)
        self.assertEqual(len(orfs), 0)


class TestMutations(unittest.TestCase):
    """突变操作测试"""
    
    def test_point_mutation(self):
        """测试点突变"""
        self.assertEqual(point_mutation("ATCG", 1, "G"), "AGCG")
        self.assertEqual(point_mutation("AAAA", 0, "T"), "TAAA")
        self.assertEqual(point_mutation("AAAA", 3, "T"), "AAAT")
        
        with self.assertRaises(NucleotideError):
            point_mutation("ATCG", 10, "A")  # 超出范围
    
    def test_deletion(self):
        """测试缺失突变"""
        self.assertEqual(deletion("ATCGATCG", 2, 3), "ATTCG")
        self.assertEqual(deletion("ATCG", 0, 1), "TCG")
        self.assertEqual(deletion("ATCG", 3, 1), "ATC")
        
        with self.assertRaises(NucleotideError):
            deletion("ATCG", 2, 10)  # 超出范围
    
    def test_insertion(self):
        """测试插入突变"""
        self.assertEqual(insertion("ATCG", 2, "XX"), "ATXXCG")
        self.assertEqual(insertion("ATCG", 0, "XX"), "XXATCG")
        self.assertEqual(insertion("ATCG", 4, "XX"), "ATCGXX")
    
    def test_substitution(self):
        """测试替换突变"""
        self.assertEqual(substitution("ATCGATCG", 2, "XXX"), "ATXXXTCG")
        self.assertEqual(substitution("ATCG", 0, "AAAA"), "AAAA")
    
    def test_random_mutation(self):
        """测试随机突变"""
        # 高突变率应该产生变化
        mutated = random_mutation("AAAAAAAAAA", mutation_rate=1.0)
        self.assertNotEqual(mutated, "AAAAAAAAAA")
        
        # 零突变率应该不变
        mutated = random_mutation("ATCG", mutation_rate=0.0)
        self.assertEqual(mutated, "ATCG")


class TestSequenceAlignment(unittest.TestCase):
    """序列比对测试"""
    
    def test_hamming_distance(self):
        """测试 Hamming 距离"""
        self.assertEqual(hamming_distance("ATCG", "ATCG"), 0)
        self.assertEqual(hamming_distance("ATCG", "ATCC"), 1)
        self.assertEqual(hamming_distance("AAAA", "TTTT"), 4)
        
        with self.assertRaises(ValueError):
            hamming_distance("ATCG", "ATC")  # 长度不同
    
    def test_sequence_identity(self):
        """测试序列相似度"""
        self.assertEqual(sequence_identity("ATCG", "ATCG"), 100.0)
        self.assertEqual(sequence_identity("ATCG", "ATCC"), 75.0)
        self.assertEqual(sequence_identity("AAAA", "TTTT"), 0.0)
        
        # 不同长度
        identity = sequence_identity("ATCG", "AT")
        self.assertEqual(identity, 100.0)  # 只比较重叠部分
    
    def test_find_motif(self):
        """测试模体查找"""
        positions = find_motif("ATCGATCGATCG", "ATCG")
        self.assertEqual(positions, [0, 4, 8])
        
        positions = find_motif("AAAAAAAA", "AA")
        self.assertEqual(len(positions), 7)  # 重叠出现
        
        positions = find_motif("ATCG", "GG")
        self.assertEqual(positions, [])
    
    def test_find_palindromes(self):
        """测试回文序列查找"""
        palindromes = find_palindromes("GAATTC", min_length=4)
        # GAATTC 的反向互补是 GAATTC
        self.assertTrue(len(palindromes) > 0)


class TestSequenceGeneration(unittest.TestCase):
    """序列生成测试"""
    
    def test_random_dna(self):
        """测试随机 DNA 生成"""
        dna = random_dna(100)
        self.assertEqual(len(dna), 100)
        self.assertTrue(is_valid_dna(dna))
        
        # 指定 GC 含量
        dna = random_dna(100, gc_content=60)
        gc = gc_content(dna)
        self.assertGreater(gc, 50)
        self.assertLess(gc, 70)
    
    def test_random_rna(self):
        """测试随机 RNA 生成"""
        rna = random_rna(100)
        self.assertEqual(len(rna), 100)
        self.assertTrue(is_valid_rna(rna))
    
    def test_random_protein(self):
        """测试随机蛋白质生成"""
        protein = random_protein(100)
        self.assertEqual(len(protein), 100)
        self.assertTrue(is_valid_protein(protein))


class TestSequenceFormatting(unittest.TestCase):
    """序列格式化测试"""
    
    def test_format_sequence(self):
        """测试序列格式化"""
        formatted = format_sequence("ATCGATCG", line_width=4)
        self.assertEqual(formatted, "ATCG\nATCG")
        
        formatted = format_sequence("ATCG", line_width=10)
        self.assertEqual(formatted, "ATCG")
    
    def test_format_fasta(self):
        """测试 FASTA 格式化"""
        fasta = format_fasta("ATCG", "test_seq")
        self.assertIn(">test_seq", fasta)
        self.assertIn("ATCG", fasta)
    
    def test_parse_fasta(self):
        """测试 FASTA 解析"""
        fasta_text = ">seq1\nATCG\n>seq2\nGCTA"
        sequences = parse_fasta(fasta_text)
        self.assertEqual(sequences['seq1'], 'ATCG')
        self.assertEqual(sequences['seq2'], 'GCTA')
        
        # 多行序列
        fasta_text = ">seq1\nATCG\nGCTA"
        sequences = parse_fasta(fasta_text)
        self.assertEqual(sequences['seq1'], 'ATCGGCTA')
    
    def test_format_protein(self):
        """测试蛋白质格式化"""
        protein = "MVLSPADKTNVKAAWGKVGAHAGEYGAEALERMFLSFPTTKTYFPHFDLSH"
        formatted = format_protein(protein, line_width=10)
        lines = formatted.split('\n')
        self.assertTrue(lines[0].startswith('   1'))


class TestConvenienceFunctions(unittest.TestCase):
    """便捷函数测试"""
    
    def test_dna_to_protein(self):
        """测试 DNA 到蛋白质"""
        self.assertEqual(dna_to_protein("ATGGCCTAA"), "MA*")
    
    def test_rna_to_protein(self):
        """测试 RNA 到蛋白质"""
        self.assertEqual(rna_to_protein("AUGGCCUAA"), "MA*")
    
    def test_is_coding_strand(self):
        """测试编码链判断"""
        # 包含长 ORF
        dna = "ATG" + "AAA" * 50 + "TAA"
        self.assertTrue(is_coding_strand(dna, min_orf_length=100))
        
        # 无长 ORF
        dna = "AAAAAAAA"
        self.assertFalse(is_coding_strand(dna, min_orf_length=100))
    
    def test_get_reading_frames(self):
        """测试获取所有阅读框"""
        dna = "ATGGCCTAAATGGCCTAA"
        frames = get_reading_frames(dna)
        
        self.assertIn(1, frames)
        self.assertIn(2, frames)
        self.assertIn(3, frames)
        self.assertIn(-1, frames)
        self.assertIn(-2, frames)
        self.assertIn(-3, frames)
        
        # 阅读框 1: ATG GCC TAA ATG GCC TAA = M A * M A *
        self.assertEqual(frames[1], "MA*MA*")
    
    def test_amino_acid_info(self):
        """测试氨基酸信息"""
        info = amino_acid_info('M')
        self.assertEqual(info['code'], 'M')
        self.assertEqual(info['three_letter'], 'Met')
        self.assertEqual(info['name_zh'], '甲硫氨酸')
        self.assertEqual(info['codons'], ['AUG'])
        self.assertEqual(info['codon_count'], 1)
        
        info = amino_acid_info('L')
        self.assertEqual(info['codon_count'], 6)
        
        with self.assertRaises(ValueError):
            amino_acid_info('X')


class TestEdgeCases(unittest.TestCase):
    """边缘情况测试"""
    
    def test_empty_sequences(self):
        """测试空序列"""
        self.assertEqual(gc_content(""), 0.0)
        self.assertEqual(nucleotide_count(""), {})
        self.assertEqual(random_dna(0), "")
        self.assertEqual(format_sequence(""), "")
    
    def test_case_sensitivity(self):
        """测试大小写"""
        # DNA
        self.assertTrue(is_valid_dna("atcg"))
        self.assertEqual(transcribe("atcg"), "AUCG")
        
        # RNA
        self.assertTrue(is_valid_rna("aucg"))
        
        # 蛋白质
        self.assertTrue(is_valid_protein("mvlspadk"))
    
    def test_long_sequences(self):
        """测试长序列"""
        long_seq = "ATCG" * 1000
        self.assertTrue(is_valid_dna(long_seq))
        self.assertEqual(gc_content(long_seq), 50.0)
        
        translated = translate_dna(long_seq)
        self.assertEqual(len(translated), len(long_seq) // 3)


if __name__ == '__main__':
    unittest.main(verbosity=2)
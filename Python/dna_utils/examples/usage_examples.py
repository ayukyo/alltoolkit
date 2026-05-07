"""
DNA Utils 使用示例

展示 dna_utils 模块的主要功能。
"""

import sys
sys.path.insert(0, '..')

from mod import (
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


def print_section(title):
    """打印章节标题"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print('='*60)


def main():
    print_section("DNA Utils - DNA/RNA 序列工具库示例")
    
    # =========================================================================
    # 1. 序列验证
    # =========================================================================
    print_section("1. 序列验证")
    
    print("\nDNA 验证:")
    print(f"  is_valid_dna('ATCG'): {is_valid_dna('ATCG')}")
    print(f"  is_valid_dna('ATCGN'): {is_valid_dna('ATCGN')}")  # 模糊碱基
    print(f"  is_valid_dna('AUCG'): {is_valid_dna('AUCG')}")   # RNA 碱基
    
    print("\nRNA 验证:")
    print(f"  is_valid_rna('AUCG'): {is_valid_rna('AUCG')}")
    print(f"  is_valid_rna('ATCG'): {is_valid_rna('ATCG')}")   # DNA 碱基
    
    print("\n蛋白质验证:")
    print(f"  is_valid_protein('MVLSPADK'): {is_valid_protein('MVLSPADK')}")
    
    print("\n自动检测序列类型:")
    print(f"  detect_sequence_type('ATCG'): {detect_sequence_type('ATCG')}")
    print(f"  detect_sequence_type('AUCG'): {detect_sequence_type('AUCG')}")
    print(f"  detect_sequence_type('MVLSPADK'): {detect_sequence_type('MVLSPADK')}")
    
    print("\n详细验证:")
    valid, msg = validate_sequence("ATCGATCG")
    print(f"  validate_sequence('ATCGATCG'): {valid}, {msg}")
    
    # =========================================================================
    # 2. 序列转换
    # =========================================================================
    print_section("2. 序列转换")
    
    dna_seq = "ATGCGTAACGTATGA"
    print(f"\n原始 DNA: {dna_seq}")
    
    # 转录
    rna_seq = transcribe(dna_seq)
    print(f"转录为 RNA: {rna_seq}")
    
    # 逆转录
    back_to_dna = reverse_transcribe(rna_seq)
    print(f"逆转录为 DNA: {back_to_dna}")
    
    # 翻译
    protein = translate_dna(dna_seq)
    print(f"翻译为蛋白质: {protein}")
    
    # 互补链
    complement = complement_dna(dna_seq)
    print(f"互补链: {complement}")
    
    # 反向互补链
    rev_comp = reverse_complement_dna(dna_seq)
    print(f"反向互补链: {rev_comp}")
    
    # =========================================================================
    # 3. GC 含量计算
    # =========================================================================
    print_section("3. GC 含量计算")
    
    seq = "ATGCGTAACGTATGACGATCGATCG"
    print(f"\n序列: {seq}")
    print(f"GC 含量: {gc_content(seq):.2f}%")
    
    # 滑动窗口
    print("\n滑动窗口 GC 含量 (窗口=10):")
    windows = gc_content_window(seq, window_size=10, step=5)
    for pos, gc in windows:
        print(f"  位置 {pos}: {gc:.2f}%")
    
    # =========================================================================
    # 4. 密码子操作
    # =========================================================================
    print_section("4. 密码子操作")
    
    print("\n密码子 → 氨基酸:")
    codons = ["AUG", "UUU", "UAA", "GGG"]
    for codon in codons:
        aa = get_amino_acid(codon)
        print(f"  {codon} → {aa} ({amino_acid_info(aa)['name_zh'] if aa != '*' else '终止'})")
    
    print("\n氨基酸 → 密码子:")
    amino_acids = ["M", "L", "S", "*"]
    for aa in amino_acids:
        codon_list = get_codons(aa)
        print(f"  {aa}: {', '.join(codon_list)} ({len(codon_list)} 个密码子)")
    
    print("\n起始/终止密码子判断:")
    print(f"  AUG 是起始密码子: {is_start_codon('AUG')}")
    print(f"  UAA 是终止密码子: {is_stop_codon('UAA')}")
    
    # 密码子使用统计
    print("\n密码子使用统计:")
    gene_seq = "ATGAAAGGGCCCTTTTAAATGCGTGA"
    usage = codon_usage(gene_seq)
    print(f"  序列: {gene_seq}")
    print(f"  使用统计: {usage}")
    
    # =========================================================================
    # 5. 序列统计
    # =========================================================================
    print_section("5. 序列统计")
    
    seq = "ATGCGTAACGTATGACGATCGATCG"
    print(f"\n序列: {seq}")
    
    # 核苷酸计数
    counts = nucleotide_count(seq)
    print(f"核苷酸计数: {counts}")
    
    # 分子量
    mw = molecular_weight(seq, detect_sequence_type(seq))
    print(f"分子量: {mw:.2f} Da")
    
    # 熔解温度
    tm = melting_temperature(seq, method='wallace')
    print(f"熔解温度 (Wallace): {tm:.2f}°C")
    
    # =========================================================================
    # 6. ORF 查找
    # =========================================================================
    print_section("6. 开放阅读框 (ORF) 查找")
    
    # 构造一个包含 ORF 的序列
    gene = "TTTATGAAAGGGCCCTTTTAAATGCGTGACCCC"
    print(f"\n序列: {gene}")
    
    orfs = find_orfs(gene, min_length=15)
    print(f"\n找到 {len(orfs)} 个 ORF:")
    for i, orf in enumerate(orfs, 1):
        print(f"  ORF {i}:")
        print(f"    位置: {orf['start']}-{orf['end']}")
        print(f"    长度: {orf['length']} bp")
        print(f"    阅读框: {orf['frame']}")
        print(f"    序列: {orf['sequence']}")
        print(f"    蛋白质: {orf['protein']}")
    
    # =========================================================================
    # 7. 突变操作
    # =========================================================================
    print_section("7. 突变操作")
    
    original = "ATGCGTAACGTATGA"
    print(f"\n原始序列: {original}")
    
    # 点突变
    mutated = point_mutation(original, 3, "A")
    print(f"点突变 (位置 3, G→A): {mutated}")
    
    # 缺失
    deleted = deletion(original, 3, 3)
    print(f"缺失 (位置 3, 长度 3): {deleted}")
    
    # 插入
    inserted = insertion(original, 3, "NNN")
    print(f"插入 (位置 3, NNN): {inserted}")
    
    # 替换
    substituted = substitution(original, 3, "NNN")
    print(f"替换 (位置 3, NNN): {substituted}")
    
    # 随机突变
    random_mut = random_mutation(original, mutation_rate=0.1)
    print(f"随机突变 (10%): {random_mut}")
    
    # =========================================================================
    # 8. 序列比对辅助
    # =========================================================================
    print_section("8. 序列比对辅助")
    
    seq1 = "ATGCGTAACGTATGA"
    seq2 = "ATGCGTAACGTCTGA"
    print(f"\n序列 1: {seq1}")
    print(f"序列 2: {seq2}")
    
    # Hamming 距离
    dist = hamming_distance(seq1, seq2)
    print(f"Hamming 距离: {dist}")
    
    # 序列相似度
    identity = sequence_identity(seq1, seq2)
    print(f"序列相似度: {identity:.2f}%")
    
    # 模体查找
    motif_seq = "ATGCGTAACGTATGACGATCGATCGATGCGTAACGTATGA"
    motif = "ATGA"
    positions = find_motif(motif_seq, motif)
    print(f"\n模体 '{motif}' 在序列中出现的位置: {positions}")
    
    # 回文序列
    palindromic = "GAATTC"
    palindromes = find_palindromes(palindromic, min_length=4)
    print(f"\n序列 '{palindromic}' 中的回文序列:")
    for p in palindromes:
        print(f"  {p['sequence']} (位置 {p['start']}-{p['end']})")
    
    # =========================================================================
    # 9. 序列生成
    # =========================================================================
    print_section("9. 随机序列生成")
    
    # 随机 DNA
    random_dna_seq = random_dna(50)
    print(f"\n随机 DNA (50 bp): {random_dna_seq}")
    
    # 指定 GC 含量的 DNA
    gc_rich = random_dna(50, gc_content=70)
    print(f"GC 丰富 DNA (GC=70%): {gc_rich}")
    print(f"实际 GC 含量: {gc_content(gc_rich):.2f}%")
    
    # 随机 RNA
    random_rna_seq = random_rna(30)
    print(f"\n随机 RNA (30 nt): {random_rna_seq}")
    
    # 随机蛋白质
    random_prot = random_protein(20)
    print(f"\n随机蛋白质 (20 aa): {random_prot}")
    
    # =========================================================================
    # 10. 序列格式化
    # =========================================================================
    print_section("10. 序列格式化")
    
    seq = "ATGCGTAACGTATGACGATCGATCGATGCGTAACGTATGACGATCGATCG"
    
    # 格式化序列
    print("\n格式化序列 (每行 20 字符):")
    print(format_sequence(seq, line_width=20))
    
    # FASTA 格式
    fasta = format_fasta(seq, "example_gene", line_width=30)
    print("\nFASTA 格式:")
    print(fasta)
    
    # 解析 FASTA
    fasta_text = """>gene1
ATGCGTAACGTATGA
>gene2
GCTAGCTAGCTA"""
    parsed = parse_fasta(fasta_text)
    print("\n解析 FASTA:")
    for name, sequence in parsed.items():
        print(f"  {name}: {sequence}")
    
    # 蛋白质格式化
    protein = "MVLSPADKTNVKAAWGKVGAHAGEYGAEALERMFLSFPTTKTYFPHFDLSH"
    print("\n蛋白质格式化:")
    print(format_protein(protein, line_width=10))
    
    # =========================================================================
    # 11. 便捷函数
    # =========================================================================
    print_section("11. 便捷函数")
    
    # DNA 直接翻译
    dna = "ATGGCCTGA"
    print(f"\nDNA: {dna}")
    print(f"翻译: {dna_to_protein(dna)}")
    
    # RNA 翻译
    rna = "AUGGCCUGA"
    print(f"\nRNA: {rna}")
    print(f"翻译: {rna_to_protein(rna)}")
    
    # 判断编码链
    coding_dna = "ATG" + "AAA" * 50 + "TGA"
    print(f"\n长编码序列是否可能是编码链: {is_coding_strand(coding_dna, min_orf_length=100)}")
    
    # 获取所有阅读框
    dna = "ATGGCCTGAATGGCCTGA"
    frames = get_reading_frames(dna)
    print(f"\n序列 {dna} 的所有阅读框翻译:")
    for frame, protein in frames.items():
        print(f"  阅读框 {frame}: {protein}")
    
    # 氨基酸信息
    print("\n氨基酸详细信息:")
    for aa in ['M', 'L', 'S', '*']:
        info = amino_acid_info(aa)
        print(f"  {info['code']} ({info['three_letter']}, {info['name_zh']}): {info['codon_count']} 个密码子")
    
    # =========================================================================
    # 12. 实际应用示例
    # =========================================================================
    print_section("12. 实际应用示例")
    
    # 示例 1: 分析基因序列
    print("\n示例 1: 分析基因序列")
    gene_sequence = "ATGAAAGGGCCCTTTTAAATGCGTGACCCC"
    print(f"基因序列: {gene_sequence}")
    print(f"长度: {len(gene_sequence)} bp")
    print(f"GC 含量: {gc_content(gene_sequence):.2f}%")
    print(f"翻译产物: {translate_dna(gene_sequence)}")
    print(f"分子量: {molecular_weight(gene_sequence, detect_sequence_type(gene_sequence)):.2f} Da")
    
    # 示例 2: 设计引物
    print("\n示例 2: 设计引物")
    primer = "ATGCGTAACGTATGA"
    print(f"引物序列: {primer}")
    print(f"Tm (Wallace): {melting_temperature(primer, method='wallace'):.1f}°C")
    print(f"GC 含量: {gc_content(primer):.1f}%")
    print(f"反向互补: {reverse_complement_dna(primer)}")
    
    # 示例 3: 序列比对
    print("\n示例 3: 序列比对")
    wild_type = "ATGCGTAACGTATGA"
    mutant = "ATGCGTAACGTCTGA"
    print(f"野生型: {wild_type}")
    print(f"突变型: {mutant}")
    print(f"差异位置: {hamming_distance(wild_type, mutant)}")
    print(f"相似度: {sequence_identity(wild_type, mutant):.1f}%")
    
    print("\n" + "="*60)
    print("示例完成!")
    print("="*60)


if __name__ == "__main__":
    main()
//! DNA Sequence Utils - 使用示例

use dna_sequence_utils::{
    DNASequence, RNASequence, ProteinSequence,
    parse_fasta, consensus_sequence, sequence_identity,
};

fn main() {
    println!("=== DNA Sequence Utils 示例 ===\n");

    // 1. 创建和基本操作
    println!("【1. DNA 序列创建和基本操作】");
    let dna = DNASequence::new("ATGCGATCGATCGATCGATCGATCG").unwrap();
    println!("原始序列: {}", dna);
    println!("序列长度: {} bp", dna.len());
    println!("GC 含量: {:.2}%", dna.gc_content());
    println!("AT 含量: {:.2}%", dna.at_content());
    
    let counts = dna.nucleotide_counts();
    println!("核苷酸分布: A={}, T={}, G={}, C={}",
             counts.get(&'A').unwrap_or(&0),
             counts.get(&'T').unwrap_or(&0),
             counts.get(&'G').unwrap_or(&0),
             counts.get(&'C').unwrap_or(&0));
    println!();

    // 2. 序列转换
    println!("【2. 序列转换】");
    println!("互补链: {}", dna.complement());
    println!("反向互补: {}", dna.reverse_complement());
    println!("转录 RNA: {}", dna.transcribe());
    println!();

    // 3. 蛋白质翻译
    println!("【3. 蛋白质翻译】");
    let coding_seq = DNASequence::new("ATGGCTAAAGCTTAA").unwrap();
    let protein = coding_seq.translate();
    println!("DNA: {}", coding_seq);
    println!("蛋白质: {}", protein);
    println!("蛋白质长度: {} aa", protein.len());
    println!("分子量: {:.2} Da", protein.molecular_weight());
    println!();

    // 4. RNA 操作
    println!("【4. RNA 序列操作】");
    let rna = RNASequence::new("AUGGCUAAAGCUUAA").unwrap();
    println!("RNA 序列: {}", rna);
    println!("反向转录: {}", rna.reverse_transcribe());
    let rna_protein = rna.translate();
    println!("翻译蛋白: {}", rna_protein);
    println!();

    // 5. 模式匹配
    println!("【5. 模式匹配】");
    let pattern_seq = DNASequence::new("ATGCGATCGATGCATCGATGC").unwrap();
    println!("序列: {}", pattern_seq);
    let atg_positions = pattern_seq.find_pattern("ATG");
    println!("ATG 起始密码子位置: {:?}", atg_positions);
    let gat_positions = pattern_seq.find_pattern("GAT");
    println!("GAT 位置: {:?}", gat_positions);
    println!("ATG 计数: {}", pattern_seq.count_pattern("ATG"));
    println!();

    // 6. Hamming 距离和突变
    println!("【6. Hamming 距离和突变分析】");
    let seq1 = DNASequence::new("ATGCGATCG").unwrap();
    let seq2 = DNASequence::new("ATGCGCTCG").unwrap();
    let distance = seq1.hamming_distance(&seq2).unwrap();
    println!("序列 1: {}", seq1);
    println!("序列 2: {}", seq2);
    println!("Hamming 距离: {}", distance);
    
    let mutations = seq1.find_mutations(&seq2).unwrap();
    println!("突变位点:");
    for (pos, from, to) in &mutations {
        println!("  位置 {}: {} -> {}", pos, from, to);
    }
    println!();

    // 7. ORF 查找
    println!("【7. 开放阅读框 (ORF) 查找】");
    let gene_seq = DNASequence::new("ATGAAATAAGATGCGATCGTAAATGCCGTGA").unwrap();
    let orfs = gene_seq.find_orfs(3);
    println!("序列: {}", gene_seq);
    println!("发现 {} 个 ORF:", orfs.len());
    for orf in &orfs {
        println!("  {} (框架 {}, {}..{}, {} bp)", 
                 orf.sequence, orf.frame, orf.start, orf.end, orf.len());
        println!("    翻译: {}", orf.translate());
    }
    println!();

    // 8. 回文检测（限制酶切位点）
    println!("【8. 回文检测（限制酶切位点）】");
    let ecoRI_seq = DNASequence::new("GAATTCGCGAATTC").unwrap();
    println!("序列: {}", ecoRI_seq);
    println!("EcoRI 位点 (GAATTC) 是否回文: {}", 
             DNASequence::new("GAATTC").unwrap().is_palindromic());
    
    let palindromes = ecoRI_seq.find_palindromes(4, 8);
    println!("回文序列:");
    for (pos, seq) in &palindromes {
        println!("  位置 {}: {}", pos, seq);
    }
    println!();

    // 9. 物理化学性质
    println!("【9. 物理化学性质】");
    let phys_seq = DNASequence::new("ATGCGATCGATCG").unwrap();
    println!("序列: {}", phys_seq);
    println!("分子量: {:.2} g/mol", phys_seq.molecular_weight());
    println!("熔解温度: {:.2}°C", phys_seq.melting_temperature());
    println!("序列复杂性 (Shannon 熵): {:.4}", phys_seq.complexity());
    println!();

    // 10. 蛋白质分析
    println!("【10. 蛋白质序列分析】");
    let prot = ProteinSequence::new("MFPKRST").unwrap();
    println!("蛋白质序列: {}", prot);
    println!("氨基酸计数:");
    let aa_counts = prot.amino_acid_counts();
    for (aa, count) in &aa_counts {
        println!("  {}: {}", aa, count);
    }
    println!("疏水性氨基酸: {}", prot.hydrophobic_count());
    println!("亲水性氨基酸: {}", prot.hydrophilic_count());
    println!("疏水性得分: {:.2}", prot.hydrophobicity());
    println!("等电点 (估算): {:.2}", prot.isoelectric_point());
    println!("分子量: {:.2} Da", prot.molecular_weight());
    println!();

    // 11. FASTA 格式
    println!("【11. FASTA 格式处理】");
    let fasta_seq = DNASequence::new("ATGCGATCGATCGATCG").unwrap();
    println!("FASTA 输出:");
    println!("{}", fasta_seq.to_fasta("example_gene"));
    println!();

    // 12. FASTA 解析
    println!("【12. FASTA 解析】");
    let fasta_input = ">gene1\nATGCGATCG\n>gene2\nGCTAGCTAG";
    let parsed = parse_fasta(fasta_input);
    println!("解析结果:");
    for (header, sequence) in &parsed {
        println!("  {}: {}", header, sequence);
    }
    println!();

    // 13. 序列一致性
    println!("【13. 序列一致性】");
    let id_seq1 = DNASequence::new("ATGCGATCG").unwrap();
    let id_seq2 = DNASequence::new("ATGCGATCG").unwrap();
    let id_seq3 = DNASequence::new("ATGCGCTCG").unwrap();
    
    let identity12 = sequence_identity(&id_seq1, &id_seq2).unwrap();
    let identity13 = sequence_identity(&id_seq1, &id_seq3).unwrap();
    println!("序列 1 vs 序列 2: {:.1}% 一致", identity12);
    println!("序列 1 vs 序列 3: {:.1}% 一致", identity13);
    println!();

    // 14. 共识序列
    println!("【14. 共识序列生成】");
    let seqs = vec![
        DNASequence::new("ATGCG").unwrap(),
        DNASequence::new("ATGCG").unwrap(),
        DNASequence::new("ATGCG").unwrap(),
        DNASequence::new("ATGTG").unwrap(),  // 一个突变
    ];
    let consensus = consensus_sequence(&seqs).unwrap();
    println!("输入序列:");
    for seq in &seqs {
        println!("  {}", seq);
    }
    println!("共识序列: {}", consensus);
    println!();

    // 15. 序列突变
    println!("【15. 模拟序列突变】");
    let original = DNASequence::new("ATGCGATCG").unwrap();
    let mutated = original.mutate(4).unwrap(); // 突变位置 4
    println!("原始: {}", original);
    println!("突变后: {}", mutated);
    println!("突变位置: 4");
    println!();

    println!("=== 示例完成 ===");
}
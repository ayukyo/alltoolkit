//! 基因序列工具库使用示例
//!
//! 展示 DNA/RNA 序列处理、翻译、突变分析等功能

use genetics_utils::{
    AminoAcid, CodonTable, DnaValidator, GeneSequence, Mutation,
    Nucleotide, PrimerDesigner, SequenceAligner, Translator,
};

fn main() {
    println!("=== 基因序列工具库使用示例 ===\n");

    // ================================
    // 1. 基本序列操作
    // ================================
    println!("【1. 基本序列操作】");

    let dna = GeneSequence::new("ATGCGATCGATCG");
    println!("DNA 序列: {}", dna.to_dna_string());
    println!("序列长度: {} bp", dna.len());
    println!("序列类型: {:?}", dna.sequence_type());

    // RNA 转录
    let rna = dna.transcribe();
    println!("转录为 RNA: {}", rna.to_rna_string());

    // 互补链
    let complement = dna.complement();
    println!("互补链: {}", complement.to_dna_string());

    // 反向互补链
    let rev_comp = dna.reverse_complement();
    println!("反向互补链: {}", rev_comp.to_dna_string());

    println!();

    // ================================
    // 2. 序列分析
    // ================================
    println!("【2. 序列分析】");

    let seq = GeneSequence::new("ATGCGATCGATCG");
    
    // GC 含量
    println!("GC 含量: {:.2}%", seq.gc_content());
    println!("AT 含量: {:.2}%", seq.at_content());

    // 核苷酸计数
    let counts = seq.nucleotide_counts();
    println!("核苷酸计数:");
    for (base, count) in &counts {
        if *count > 0 {
            println!("  {}: {}", base, count);
        }
    }

    // 分子量
    println!("分子量: {:.2} Da", seq.molecular_weight());

    // 序列验证
    println!("是否为有效 DNA: {}", DnaValidator::is_valid_dna("ATGC"));
    println!("是否为有效 RNA: {}", DnaValidator::is_valid_rna("AUGC"));

    println!();

    // ================================
    // 3. 核苷酸属性
    // ================================
    println!("【3. 核苷酸属性】");

    let nucleotides = vec![
        Nucleotide::Adenine,
        Nucleotide::Thymine,
        Nucleotide::Guanine,
        Nucleotide::Cytosine,
    ];

    println!("核苷酸属性:");
    for n in &nucleotides {
        println!(
            "  {:?}: DNA={}, RNA={}, 嘌呤={}, 嘧啶={}",
            n,
            n.to_dna_char(),
            n.to_rna_char(),
            n.is_purine(),
            n.is_pyrimidine()
        );
    }

    println!();

    // ================================
    // 4. 密码子表
    // ================================
    println!("【4. 密码子表】");

    let codon_table = CodonTable::standard();

    // 翻译密码子
    let codons = vec!["AUG", "UUU", "UUC", "UAA", "UGG", "AAA"];
    println!("密码子翻译:");
    for codon in &codons {
        if let Some(aa) = codon_table.translate_codon(codon) {
            println!("  {} -> {} ({})", codon, aa.code(), aa.name());
        }
    }

    println!("起始密码子: {:?}", CodonTable::start_codons());
    println!("终止密码子: {:?}", CodonTable::stop_codons());

    println!();

    // ================================
    // 5. 蛋白质翻译
    // ================================
    println!("【5. 蛋白质翻译】");

    let mrna = GeneSequence::new("AUGUUUUUCUAA"); // Met-Phe-Phe-Stop
    println!("mRNA 序列: {}", mrna.to_rna_string());

    let translator = Translator::new();
    let protein = translator.translate(&mrna);

    println!("翻译结果:");
    for (i, aa) in protein.iter().enumerate() {
        println!("  {}: {} ({})", i + 1, aa.code(), aa.name());
    }

    // 蛋白质序列字符串
    let protein_str = translator.translate_to_protein_string(&mrna);
    println!("蛋白质序列: {}", protein_str);

    println!();

    // ================================
    // 6. 开放阅读框 (ORF) 查找
    // ================================
    println!("【6. 开放阅读框 (ORF) 查找】");

    let genome = GeneSequence::new(
        "GCCAUGGCAAAGGGCCAAAUGCCCUAAUUAAUGCCCAUGCCCUAG",
    );
    println!("基因组序列: {}", genome.to_rna_string());

    let orfs = translator.find_orfs(&genome, 3);
    println!("找到 {} 个 ORF:", orfs.len());

    for (i, orf) in orfs.iter().enumerate() {
        println!(
            "  ORF {}: 位置 {}-{}, 阅读框 {}, 长度 {} bp",
            i + 1,
            orf.start,
            orf.end,
            orf.frame,
            orf.length()
        );
        println!("    蛋白质: {}", orf.protein_string());
    }

    println!();

    // ================================
    // 7. 序列比对
    // ================================
    println!("【7. 序列比对】");

    let seq1 = GeneSequence::new("ATGCGATCGA");
    let seq2 = GeneSequence::new("ATGCAATCAA");

    println!("序列 1: {}", seq1.to_dna_string());
    println!("序列 2: {}", seq2.to_dna_string());

    // 汉明距离
    match SequenceAligner::hamming_distance(&seq1, &seq2) {
        Ok(dist) => println!("汉明距离: {}", dist),
        Err(e) => println!("错误: {}", e),
    }

    // 相似度
    let similarity = SequenceAligner::similarity(&seq1, &seq2);
    println!("相似度: {:.2}%", similarity);

    // 变异位点
    let mutations = SequenceAligner::find_mutations(&seq1, &seq2);
    println!("发现 {} 个变异位点:", mutations.len());
    for m in &mutations {
        println!("  {}", m.description());
    }

    println!();

    // ================================
    // 8. 变异分析
    // ================================
    println!("【8. 变异分析】");

    let test_mutations = vec![
        Mutation {
            position: 0,
            original: 'A',
            mutated: 'G',
        }, // 转换
        Mutation {
            position: 1,
            original: 'A',
            mutated: 'T',
        }, // 颠换
        Mutation {
            position: 2,
            original: '-',
            mutated: 'C',
        }, // 插入
        Mutation {
            position: 3,
            original: 'G',
            mutated: '-',
        }, // 缺失
    ];

    for m in &test_mutations {
        println!(
            "  {} - 转换: {}, 颠换: {}",
            m.description(),
            m.is_transition(),
            m.is_transversion()
        );
    }

    println!();

    // ================================
    // 9. 引物设计
    // ================================
    println!("【9. 引物设计】");

    let template = GeneSequence::new("ATGCTAGCTAGCTAGCTAGCGATCGATCG");
    println!("模板序列: {}", template.to_dna_string());

    // 设计正向引物
    if let Some(fwd) = PrimerDesigner::design_forward_primer(&template, 3, 8) {
        println!("正向引物 (位置 3, 长度 8): {}", fwd);
        println!("  Tm (Wallace): {:.1}°C", PrimerDesigner::calculate_tm(&fwd));
        println!("  是否有二聚体: {}", PrimerDesigner::has_dimer(&fwd));
    }

    // 设计反向引物
    if let Some(rev) = PrimerDesigner::design_reverse_primer(&template, 20, 8) {
        println!("反向引物 (位置 20, 长度 8): {}", rev);
        println!("  Tm (Wallace): {:.1}°C", PrimerDesigner::calculate_tm(&rev));
        println!("  是否有二聚体: {}", PrimerDesigner::has_dimer(&rev));
    }

    // PCR 产物长度
    let product_len = PrimerDesigner::pcr_product_length(3, 20);
    println!("PCR 产物长度: {} bp", product_len);

    println!();

    // ================================
    // 10. 实用场景示例
    // ================================
    println!("【10. 实用场景示例】");

    // 场景1: 分析基因序列
    let gene = GeneSequence::new("ATGGCCATTGTAATGGGCCGCTGAAAGGGTGCCCGATAG");
    println!("基因序列分析:");
    println!("  长度: {} bp", gene.len());
    println!("  GC 含量: {:.2}%", gene.gc_content());
    println!("  分子量: {:.2} Da", gene.molecular_weight());

    // 场景2: 查找基因序列中的特定模式
    let pattern = "ATG";
    let positions = gene.find(pattern);
    println!("  '{}' 出现位置: {:?}", pattern, positions);

    // 场景3: 翻译并分析蛋白质
    let orfs = Translator::new().find_orfs(&gene, 10);
    if !orfs.is_empty() {
        println!("  找到 ORF: 长度 {} bp, 蛋白质 {}", orfs[0].length(), orfs[0].protein_string());
    }

    // 场景4: 比较野生型和突变型
    let wild_type = GeneSequence::new("ATGCGATCG");
    let mutant = GeneSequence::new("ATGCAATCG");
    let similarity = SequenceAligner::similarity(&wild_type, &mutant);
    println!("  野生型 vs 突变型相似度: {:.2}%", similarity);

    println!();

    // ================================
    // 11. 氨基酸信息查询
    // ================================
    println!("【11. 氨基酸信息查询】");

    let amino_acids = vec![
        AminoAcid::Met,
        AminoAcid::Phe,
        AminoAcid::Trp,
        AminoAcid::Stop,
    ];

    println!("氨基酸信息:");
    for aa in &amino_acids {
        println!(
            "  {} ({}) - {}",
            aa.code(),
            aa.symbol(),
            aa.name()
        );
    }

    println!();

    // ================================
    // 12. 性能测试
    // ================================
    println!("【12. 性能测试】");

    use std::time::Instant;

    // 创建长序列
    let long_seq = GeneSequence::new(&"ATGC".repeat(1000));
    println!("测试序列长度: {} bp", long_seq.len());

    // GC 含量计算
    let start = Instant::now();
    for _ in 0..1000 {
        let _ = long_seq.gc_content();
    }
    println!("1000 次 GC 含量计算: {:?}", start.elapsed());

    // 反向互补
    let start = Instant::now();
    for _ in 0..1000 {
        let _ = long_seq.reverse_complement();
    }
    println!("1000 次反向互补计算: {:?}", start.elapsed());

    // 翻译
    let start = Instant::now();
    let translator = Translator::new();
    for _ in 0..100 {
        let _ = translator.translate(&long_seq);
    }
    println!("100 次序列翻译: {:?}", start.elapsed());

    println!();
    println!("=== 示例完成 ===");
}
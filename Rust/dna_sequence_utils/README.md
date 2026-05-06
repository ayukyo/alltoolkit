# DNA Sequence Utils

DNA/RNA 序列分析和操作工具库，专为生物信息学应用设计。

## 功能特性

### DNA 序列操作
- 序列验证和清理
- GC/AT 含量计算
- 互补链和反向互补链生成
- RNA 转录
- 蛋白质翻译
- 序列突变分析

### RNA 序列操作
- 序列验证
- 反向转录为 DNA
- 蛋白质翻译

### 蛋白质序列分析
- 氨基酸组成分析
- 分子量计算
- 等电点估算
- 亲疏水性分析

### 高级功能
- Hamming 距离计算
- 开放阅读框 (ORF) 查找
- 模式匹配
- 回文序列检测（限制酶切位点）
- 序列复杂性计算（Shannon 熵）
- FASTA 格式解析和生成
- 共识序列生成

## 安装

```toml
[dependencies]
dna_sequence_utils = "0.1.0"
```

## 快速开始

```rust
use dna_sequence_utils::{DNASequence, RNASequence, ProteinSequence};

fn main() {
    // 创建 DNA 序列
    let dna = DNASequence::new("ATGCGATCGATCG").unwrap();
    
    // 计算属性
    println!("序列长度: {}", dna.len());
    println!("GC 含量: {:.2}%", dna.gc_content());
    println!("分子量: {:.2} g/mol", dna.molecular_weight());
    println!("熔解温度: {:.2}°C", dna.melting_temperature());
    
    // 序列操作
    println!("互补链: {}", dna.complement());
    println!("反向互补: {}", dna.reverse_complement());
    println!("转录 RNA: {}", dna.transcribe());
    
    // 蛋白质翻译
    let protein = dna.translate();
    println!("翻译蛋白: {}", protein);
    
    // 查找 ORF
    let orfs = dna.find_orfs(100);
    for orf in &orfs {
        println!("ORF: {} (位置: {}..{})", orf.sequence, orf.start, orf.end);
    }
    
    // 模式匹配
    let positions = dna.find_pattern("GAT");
    println!("GAT 位置: {:?}", positions);
    
    // 回文检测
    let palindromes = dna.find_palindromes(4, 8);
    println!("回文序列: {:?}", palindromes);
}
```

## API 文档

### DNASequence

```rust
// 创建序列
let dna = DNASequence::new("ATGCGATCG")?;

// 基本信息
dna.len();              // 序列长度
dna.gc_content();        // GC 含量 (%)
dna.at_content();        // AT 含量 (%)
dna.nucleotide_counts(); // 核苷酸计数

// 序列转换
dna.complement();          // 互补链
dna.reverse_complement();  // 反向互补
dna.transcribe();          // 转录为 RNA
dna.translate();           // 翻译为蛋白质

// 序列分析
dna.hamming_distance(&other);  // Hamming 距离
dna.find_mutations(&other);    // 突变位点
dna.molecular_weight();        // 分子量
dna.melting_temperature();     // 熔解温度
dna.complexity();              // 序列复杂性

// 模式查找
dna.find_pattern("ATG");       // 查找模式位置
dna.count_pattern("ATG");      // 计数模式
dna.find_start_codons();       // 起始密码子
dna.find_stop_codons();        // 终止密码子

// ORF 分析
dna.find_orfs(min_length);     // 查找 ORF
dna.reading_frames();          // 读取框架

// 回文检测
dna.is_palindromic();          // 是否回文
dna.find_palindromes(4, 8);    // 查找回文

// 格式化
dna.to_fasta("sequence1");    // FASTA 格式
```

### RNASequence

```rust
let rna = RNASequence::new("AUGCGAUCG")?;

rna.reverse_transcribe();  // 反向转录为 DNA
rna.translate();          // 翻译为蛋白质
rna.nucleotide_counts(); // 核苷酸计数
```

### ProteinSequence

```rust
let protein = ProteinSequence::new("MFPK")?;

protein.molecular_weight();   // 分子量 (kDa)
protein.isoelectric_point();  // 等电点
protein.hydrophobicity();     // 亲疏水性
protein.amino_acid_counts();  // 氨基酸计数
protein.to_fasta("protein1"); // FASTA 格式
```

### 工具函数

```rust
// FASTA 解析
let sequences = parse_fasta(fasta_content);

// 序列一致性
let identity = sequence_identity(&seq1, &seq2)?;

// 共识序列
let consensus = consensus_sequence(&[seq1, seq2, seq3])?;
```

## 示例

### 分析基因序列

```rust
use dna_sequence_utils::DNASequence;

fn main() {
    let gene = DNASequence::new("ATGCGATCGATCGATCG").unwrap();
    
    // 基本信息
    println!("基因长度: {} bp", gene.len());
    println!("GC 含量: {:.1}%", gene.gc_content());
    
    // 查找所有 ORF
    let orfs = gene.find_orfs(30);
    println!("发现 {} 个 ORF", orfs.len());
    
    for orf in &orfs {
        let protein = orf.translate();
        println!("ORF (框架{}): {} bp -> {} aa", 
                 orf.frame, orf.len(), protein.len());
    }
}
```

### 比对序列

```rust
use dna_sequence_utils::{DNASequence, sequence_identity};

fn main() {
    let seq1 = DNASequence::new("ATGCGATCGA").unwrap();
    let seq2 = DNASequence::new("ATGCGCTCGA").unwrap();
    
    // Hamming 距离
    let dist = seq1.hamming_distance(&seq2).unwrap();
    println!("Hamming 距离: {}", dist);
    
    // 突变位点
    let mutations = seq1.find_mutations(&seq2).unwrap();
    for (pos, from, to) in &mutations {
        println!("位置 {}: {} -> {}", pos, from, to);
    }
    
    // 序列一致性
    let identity = sequence_identity(&seq1, &seq2).unwrap();
    println!("序列一致性: {:.1}%", identity);
}
```

### 检测限制酶切位点

```rust
use dna_sequence_utils::DNASequence;

fn main() {
    let dna = DNASequence::new("GAATTCGCGAATTCTTT").unwrap();
    
    // EcoRI 位点 (GAATTC) 是回文序列
    let palindromes = dna.find_palindromes(4, 8);
    for (pos, seq) in &palindromes {
        println!("回文位点 {} 处: {}", pos, seq);
    }
    
    // 直接查找 EcoRI
    let ecori_sites = dna.find_pattern("GAATTC");
    println!("EcoRI 位点: {:?}", ecori_sites);
}
```

## 许可证

MIT License
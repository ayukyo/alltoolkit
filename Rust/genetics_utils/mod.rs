//! 基因序列工具库 - 零外部依赖
//!
//! 提供完整的 DNA/RNA 序列处理功能
//! 支持序列验证、转录、翻译、互补链生成等核心功能

use std::collections::HashMap;

/// 核苷酸类型
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub enum Nucleotide {
    /// 腺嘌呤 (DNA/RNA)
    Adenine,
    /// 胸腺嘧啶 (DNA)
    Thymine,
    /// 尿嘧啶 (RNA)
    Uracil,
    /// 鸟嘌呤 (DNA/RNA)
    Guanine,
    /// 胞嘧啶 (DNA/RNA)
    Cytosine,
    /// 未知/其他
    Unknown(char),
}

impl Nucleotide {
    /// 从字符创建核苷酸
    pub fn from_char(c: char) -> Self {
        match c.to_ascii_uppercase() {
            'A' => Nucleotide::Adenine,
            'T' => Nucleotide::Thymine,
            'U' => Nucleotide::Uracil,
            'G' => Nucleotide::Guanine,
            'C' => Nucleotide::Cytosine,
            other => Nucleotide::Unknown(other),
        }
    }

    /// 转换为字符 (DNA格式)
    pub fn to_dna_char(&self) -> char {
        match self {
            Nucleotide::Adenine => 'A',
            Nucleotide::Thymine => 'T',
            Nucleotide::Uracil => 'T', // U -> T
            Nucleotide::Guanine => 'G',
            Nucleotide::Cytosine => 'C',
            Nucleotide::Unknown(c) => *c,
        }
    }

    /// 转换为字符 (RNA格式)
    pub fn to_rna_char(&self) -> char {
        match self {
            Nucleotide::Adenine => 'A',
            Nucleotide::Thymine => 'U', // T -> U
            Nucleotide::Uracil => 'U',
            Nucleotide::Guanine => 'G',
            Nucleotide::Cytosine => 'C',
            Nucleotide::Unknown(c) => *c,
        }
    }

    /// 获取互补核苷酸 (DNA)
    pub fn dna_complement(&self) -> Self {
        match self {
            Nucleotide::Adenine => Nucleotide::Thymine,
            Nucleotide::Thymine => Nucleotide::Adenine,
            Nucleotide::Uracil => Nucleotide::Adenine,
            Nucleotide::Guanine => Nucleotide::Cytosine,
            Nucleotide::Cytosine => Nucleotide::Guanine,
            Nucleotide::Unknown(c) => Nucleotide::Unknown(*c),
        }
    }

    /// 获取互补核苷酸 (RNA)
    pub fn rna_complement(&self) -> Self {
        match self {
            Nucleotide::Adenine => Nucleotide::Uracil,
            Nucleotide::Thymine => Nucleotide::Adenine,
            Nucleotide::Uracil => Nucleotide::Adenine,
            Nucleotide::Guanine => Nucleotide::Cytosine,
            Nucleotide::Cytosine => Nucleotide::Guanine,
            Nucleotide::Unknown(c) => Nucleotide::Unknown(*c),
        }
    }

    /// 是否为嘌呤 (A, G)
    pub fn is_purine(&self) -> bool {
        matches!(self, Nucleotide::Adenine | Nucleotide::Guanine)
    }

    /// 是否为嘧啶 (T, U, C)
    pub fn is_pyrimidine(&self) -> bool {
        matches!(self, Nucleotide::Thymine | Nucleotide::Uracil | Nucleotide::Cytosine)
    }
}

/// 序列类型
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum SequenceType {
    DNA,
    RNA,
    Mixed,
    Invalid,
}

/// 氨基酸
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub enum AminoAcid {
    Ala, Arg, Asn, Asp, Cys, Gln, Glu, Gly, His, Ile,
    Leu, Lys, Met, Phe, Pro, Ser, Thr, Trp, Tyr, Val,
    Start, Stop,
}

impl AminoAcid {
    /// 获取三字母缩写
    pub fn code(&self) -> &'static str {
        match self {
            AminoAcid::Ala => "Ala",
            AminoAcid::Arg => "Arg",
            AminoAcid::Asn => "Asn",
            AminoAcid::Asp => "Asp",
            AminoAcid::Cys => "Cys",
            AminoAcid::Gln => "Gln",
            AminoAcid::Glu => "Glu",
            AminoAcid::Gly => "Gly",
            AminoAcid::His => "His",
            AminoAcid::Ile => "Ile",
            AminoAcid::Leu => "Leu",
            AminoAcid::Lys => "Lys",
            AminoAcid::Met => "Met",
            AminoAcid::Phe => "Phe",
            AminoAcid::Pro => "Pro",
            AminoAcid::Ser => "Ser",
            AminoAcid::Thr => "Thr",
            AminoAcid::Trp => "Trp",
            AminoAcid::Tyr => "Tyr",
            AminoAcid::Val => "Val",
            AminoAcid::Start => "Met",
            AminoAcid::Stop => "Stop",
        }
    }

    /// 获取单字母缩写
    pub fn symbol(&self) -> char {
        match self {
            AminoAcid::Ala => 'A',
            AminoAcid::Arg => 'R',
            AminoAcid::Asn => 'N',
            AminoAcid::Asp => 'D',
            AminoAcid::Cys => 'C',
            AminoAcid::Gln => 'Q',
            AminoAcid::Glu => 'E',
            AminoAcid::Gly => 'G',
            AminoAcid::His => 'H',
            AminoAcid::Ile => 'I',
            AminoAcid::Leu => 'L',
            AminoAcid::Lys => 'K',
            AminoAcid::Met => 'M',
            AminoAcid::Phe => 'F',
            AminoAcid::Pro => 'P',
            AminoAcid::Ser => 'S',
            AminoAcid::Thr => 'T',
            AminoAcid::Trp => 'W',
            AminoAcid::Tyr => 'Y',
            AminoAcid::Val => 'V',
            AminoAcid::Start => 'M',
            AminoAcid::Stop => '*',
        }
    }

    /// 获取氨基酸全名
    pub fn name(&self) -> &'static str {
        match self {
            AminoAcid::Ala => "Alanine",
            AminoAcid::Arg => "Arginine",
            AminoAcid::Asn => "Asparagine",
            AminoAcid::Asp => "Aspartic acid",
            AminoAcid::Cys => "Cysteine",
            AminoAcid::Gln => "Glutamine",
            AminoAcid::Glu => "Glutamic acid",
            AminoAcid::Gly => "Glycine",
            AminoAcid::His => "Histidine",
            AminoAcid::Ile => "Isoleucine",
            AminoAcid::Leu => "Leucine",
            AminoAcid::Lys => "Lysine",
            AminoAcid::Met => "Methionine",
            AminoAcid::Phe => "Phenylalanine",
            AminoAcid::Pro => "Proline",
            AminoAcid::Ser => "Serine",
            AminoAcid::Thr => "Threonine",
            AminoAcid::Trp => "Tryptophan",
            AminoAcid::Tyr => "Tyrosine",
            AminoAcid::Val => "Valine",
            AminoAcid::Start => "Methionine (Start)",
            AminoAcid::Stop => "Stop codon",
        }
    }

    /// 是否为终止密码子
    pub fn is_stop(&self) -> bool {
        matches!(self, AminoAcid::Stop)
    }
}

/// 基因序列
#[derive(Debug, Clone, PartialEq)]
pub struct GeneSequence {
    sequence: Vec<Nucleotide>,
    seq_type: SequenceType,
}

impl GeneSequence {
    /// 从字符串创建基因序列
    pub fn new(sequence: &str) -> Self {
        let nucleotides: Vec<Nucleotide> = sequence
            .chars()
            .filter(|c| !c.is_whitespace())
            .map(Nucleotide::from_char)
            .collect();
        
        let seq_type = Self::detect_sequence_type(sequence);
        GeneSequence {
            sequence: nucleotides,
            seq_type,
        }
    }

    /// 检测序列类型
    pub fn detect_sequence_type(sequence: &str) -> SequenceType {
        let mut has_t = false;
        let mut has_u = false;
        let mut has_invalid = false;

        for c in sequence.chars() {
            match c.to_ascii_uppercase() {
                'T' => has_t = true,
                'U' => has_u = true,
                'A' | 'G' | 'C' => {}
                ' ' | '\n' | '\r' | '\t' => {}
                _ => has_invalid = true,
            }
        }

        if has_invalid {
            SequenceType::Invalid
        } else if has_t && has_u {
            SequenceType::Mixed
        } else if has_u {
            SequenceType::RNA
        } else {
            SequenceType::DNA
        }
    }

    /// 获取序列长度
    pub fn len(&self) -> usize {
        self.sequence.len()
    }

    /// 判断序列是否为空
    pub fn is_empty(&self) -> bool {
        self.sequence.is_empty()
    }

    /// 获取序列类型
    pub fn sequence_type(&self) -> SequenceType {
        self.seq_type
    }

    /// 获取序列字符串 (DNA格式)
    pub fn to_dna_string(&self) -> String {
        self.sequence.iter()
            .map(|n| n.to_dna_char())
            .collect()
    }

    /// 获取序列字符串 (RNA格式)
    pub fn to_rna_string(&self) -> String {
        self.sequence.iter()
            .map(|n| n.to_rna_char())
            .collect()
    }

    /// 转录 (DNA -> RNA)
    pub fn transcribe(&self) -> Self {
        GeneSequence {
            sequence: self.sequence.clone(),
            seq_type: SequenceType::RNA,
        }
    }

    /// 反转录 (RNA -> DNA)
    pub fn reverse_transcribe(&self) -> Self {
        GeneSequence {
            sequence: self.sequence.clone(),
            seq_type: SequenceType::DNA,
        }
    }

    /// 获取互补链 (DNA)
    pub fn complement(&self) -> Self {
        let complement_seq: Vec<Nucleotide> = self.sequence
            .iter()
            .map(|n| n.dna_complement())
            .collect();
        GeneSequence {
            sequence: complement_seq,
            seq_type: self.seq_type,
        }
    }

    /// 获取反向互补链 (DNA)
    pub fn reverse_complement(&self) -> Self {
        let rev_comp: Vec<Nucleotide> = self.sequence
            .iter()
            .rev()
            .map(|n| n.dna_complement())
            .collect();
        GeneSequence {
            sequence: rev_comp,
            seq_type: self.seq_type,
        }
    }

    /// 计算 GC 含量
    pub fn gc_content(&self) -> f64 {
        if self.sequence.is_empty() {
            return 0.0;
        }

        let gc_count = self.sequence
            .iter()
            .filter(|n| matches!(n, Nucleotide::Guanine | Nucleotide::Cytosine))
            .count();

        (gc_count as f64 / self.sequence.len() as f64) * 100.0
    }

    /// 计算 AT/AU 含量
    pub fn at_content(&self) -> f64 {
        100.0 - self.gc_content()
    }

    /// 计算分子量 (Da, 道尔顿)
    pub fn molecular_weight(&self) -> f64 {
        let mut weight = 0.0;
        
        for nucleotide in &self.sequence {
            weight += match nucleotide {
                Nucleotide::Adenine => 313.21,
                Nucleotide::Thymine => 304.19,
                Nucleotide::Uracil => 290.17,
                Nucleotide::Guanine => 329.21,
                Nucleotide::Cytosine => 289.18,
                Nucleotide::Unknown(_) => 0.0,
            };
        }

        // 减去磷酸二酯键的水分子
        if self.sequence.len() > 1 {
            weight -= (self.sequence.len() - 1) as f64 * 18.015;
        }

        weight
    }

    /// 获取核苷酸计数
    pub fn nucleotide_counts(&self) -> HashMap<char, usize> {
        let mut counts = HashMap::new();
        counts.insert('A', 0);
        counts.insert('T', 0);
        counts.insert('U', 0);
        counts.insert('G', 0);
        counts.insert('C', 0);
        counts.insert('N', 0);

        for nucleotide in &self.sequence {
            match nucleotide {
                Nucleotide::Adenine => *counts.get_mut(&'A').unwrap() += 1,
                Nucleotide::Thymine => *counts.get_mut(&'T').unwrap() += 1,
                Nucleotide::Uracil => *counts.get_mut(&'U').unwrap() += 1,
                Nucleotide::Guanine => *counts.get_mut(&'G').unwrap() += 1,
                Nucleotide::Cytosine => *counts.get_mut(&'C').unwrap() += 1,
                Nucleotide::Unknown(_) => *counts.get_mut(&'N').unwrap() += 1,
            }
        }

        counts
    }

    /// 查找子序列位置
    pub fn find(&self, pattern: &str) -> Vec<usize> {
        let pattern_seq: Vec<Nucleotide> = pattern
            .chars()
            .filter(|c| !c.is_whitespace())
            .map(Nucleotide::from_char)
            .collect();

        if pattern_seq.is_empty() || pattern_seq.len() > self.sequence.len() {
            return Vec::new();
        }

        let mut positions = Vec::new();
        let search_str: String = self.sequence.iter()
            .map(|n| n.to_dna_char())
            .collect();
        let pattern_str: String = pattern_seq.iter()
            .map(|n| n.to_dna_char())
            .collect();

        let mut start = 0;
        while let Some(pos) = search_str[start..].find(&pattern_str) {
            positions.push(start + pos);
            start += pos + 1;
            if start >= search_str.len() {
                break;
            }
        }

        positions
    }

    /// 验证序列是否有效
    pub fn is_valid(&self) -> bool {
        !matches!(self.seq_type, SequenceType::Invalid)
    }
}

/// 遗传密码子表 (标准遗传密码)
pub struct CodonTable {
    table: HashMap<String, AminoAcid>,
}

impl CodonTable {
    /// 创建标准遗传密码表
    pub fn standard() -> Self {
        let mut table = HashMap::new();
        
        // 苯丙氨酸 (Phe)
        table.insert("UUU".to_string(), AminoAcid::Phe);
        table.insert("UUC".to_string(), AminoAcid::Phe);
        
        // 亮氨酸 (Leu)
        table.insert("UUA".to_string(), AminoAcid::Leu);
        table.insert("UUG".to_string(), AminoAcid::Leu);
        table.insert("CUU".to_string(), AminoAcid::Leu);
        table.insert("CUC".to_string(), AminoAcid::Leu);
        table.insert("CUA".to_string(), AminoAcid::Leu);
        table.insert("CUG".to_string(), AminoAcid::Leu);
        
        // 异亮氨酸 (Ile)
        table.insert("AUU".to_string(), AminoAcid::Ile);
        table.insert("AUC".to_string(), AminoAcid::Ile);
        table.insert("AUA".to_string(), AminoAcid::Ile);
        
        // 甲硫氨酸 (Met / 起始密码子)
        table.insert("AUG".to_string(), AminoAcid::Met);
        
        // 缬氨酸 (Val)
        table.insert("GUU".to_string(), AminoAcid::Val);
        table.insert("GUC".to_string(), AminoAcid::Val);
        table.insert("GUA".to_string(), AminoAcid::Val);
        table.insert("GUG".to_string(), AminoAcid::Val);
        
        // 丝氨酸 (Ser)
        table.insert("UCU".to_string(), AminoAcid::Ser);
        table.insert("UCC".to_string(), AminoAcid::Ser);
        table.insert("UCA".to_string(), AminoAcid::Ser);
        table.insert("UCG".to_string(), AminoAcid::Ser);
        table.insert("AGU".to_string(), AminoAcid::Ser);
        table.insert("AGC".to_string(), AminoAcid::Ser);
        
        // 脯氨酸 (Pro)
        table.insert("CCU".to_string(), AminoAcid::Pro);
        table.insert("CCC".to_string(), AminoAcid::Pro);
        table.insert("CCA".to_string(), AminoAcid::Pro);
        table.insert("CCG".to_string(), AminoAcid::Pro);
        
        // 苏氨酸 (Thr)
        table.insert("ACU".to_string(), AminoAcid::Thr);
        table.insert("ACC".to_string(), AminoAcid::Thr);
        table.insert("ACA".to_string(), AminoAcid::Thr);
        table.insert("ACG".to_string(), AminoAcid::Thr);
        
        // 丙氨酸 (Ala)
        table.insert("GCU".to_string(), AminoAcid::Ala);
        table.insert("GCC".to_string(), AminoAcid::Ala);
        table.insert("GCA".to_string(), AminoAcid::Ala);
        table.insert("GCG".to_string(), AminoAcid::Ala);
        
        // 酪氨酸 (Tyr)
        table.insert("UAU".to_string(), AminoAcid::Tyr);
        table.insert("UAC".to_string(), AminoAcid::Tyr);
        
        // 组氨酸 (His)
        table.insert("CAU".to_string(), AminoAcid::His);
        table.insert("CAC".to_string(), AminoAcid::His);
        
        // 谷氨酰胺 (Gln)
        table.insert("CAA".to_string(), AminoAcid::Gln);
        table.insert("CAG".to_string(), AminoAcid::Gln);
        
        // 天冬酰胺 (Asn)
        table.insert("AAU".to_string(), AminoAcid::Asn);
        table.insert("AAC".to_string(), AminoAcid::Asn);
        
        // 赖氨酸 (Lys)
        table.insert("AAA".to_string(), AminoAcid::Lys);
        table.insert("AAG".to_string(), AminoAcid::Lys);
        
        // 天冬氨酸 (Asp)
        table.insert("GAU".to_string(), AminoAcid::Asp);
        table.insert("GAC".to_string(), AminoAcid::Asp);
        
        // 谷氨酸 (Glu)
        table.insert("GAA".to_string(), AminoAcid::Glu);
        table.insert("GAG".to_string(), AminoAcid::Glu);
        
        // 半胱氨酸 (Cys)
        table.insert("UGU".to_string(), AminoAcid::Cys);
        table.insert("UGC".to_string(), AminoAcid::Cys);
        
        // 色氨酸 (Trp)
        table.insert("UGG".to_string(), AminoAcid::Trp);
        
        // 精氨酸 (Arg)
        table.insert("CGU".to_string(), AminoAcid::Arg);
        table.insert("CGC".to_string(), AminoAcid::Arg);
        table.insert("CGA".to_string(), AminoAcid::Arg);
        table.insert("CGG".to_string(), AminoAcid::Arg);
        table.insert("AGA".to_string(), AminoAcid::Arg);
        table.insert("AGG".to_string(), AminoAcid::Arg);
        
        // 甘氨酸 (Gly)
        table.insert("GGU".to_string(), AminoAcid::Gly);
        table.insert("GGC".to_string(), AminoAcid::Gly);
        table.insert("GGA".to_string(), AminoAcid::Gly);
        table.insert("GGG".to_string(), AminoAcid::Gly);
        
        // 终止密码子
        table.insert("UAA".to_string(), AminoAcid::Stop);
        table.insert("UAG".to_string(), AminoAcid::Stop);
        table.insert("UGA".to_string(), AminoAcid::Stop);

        CodonTable { table }
    }

    /// 翻译密码子为氨基酸
    pub fn translate_codon(&self, codon: &str) -> Option<AminoAcid> {
        let codon_upper: String = codon.to_uppercase()
            .replace('T', "U"); // 转换为 RNA 格式
        self.table.get(&codon_upper).copied()
    }

    /// 获取起始密码子
    pub fn start_codons() -> Vec<&'static str> {
        vec!["AUG"]
    }

    /// 获取终止密码子
    pub fn stop_codons() -> Vec<&'static str> {
        vec!["UAA", "UAG", "UGA"]
    }
}

/// 翻译器
pub struct Translator {
    codon_table: CodonTable,
}

impl Translator {
    /// 创建新的翻译器
    pub fn new() -> Self {
        Translator {
            codon_table: CodonTable::standard(),
        }
    }

    /// 翻译 RNA 序列为氨基酸序列
    pub fn translate(&self, rna_sequence: &GeneSequence) -> Vec<AminoAcid> {
        let rna_str = rna_sequence.to_rna_string();
        let mut amino_acids = Vec::new();
        
        let chars: Vec<char> = rna_str.chars().collect();
        
        for chunk in chars.chunks(3) {
            if chunk.len() == 3 {
                let codon: String = chunk.iter().collect();
                if let Some(aa) = self.codon_table.translate_codon(&codon) {
                    amino_acids.push(aa);
                }
            }
        }

        amino_acids
    }

    /// 翻译 DNA 序列为氨基酸序列
    pub fn translate_dna(&self, dna_sequence: &GeneSequence) -> Vec<AminoAcid> {
        let rna = dna_sequence.transcribe();
        self.translate(&rna)
    }

    /// 获取蛋白质序列 (单字母缩写)
    pub fn translate_to_protein_string(&self, rna_sequence: &GeneSequence) -> String {
        let amino_acids = self.translate(rna_sequence);
        amino_acids.iter()
            .map(|aa| aa.symbol())
            .collect()
    }

    /// 从第一个起始密码子开始翻译
    pub fn translate_from_start(&self, rna_sequence: &GeneSequence) -> Vec<AminoAcid> {
        let rna_str = rna_sequence.to_rna_string();
        
        // 查找起始密码子 AUG
        if let Some(start_pos) = rna_str.find("AUG") {
            let from_start = GeneSequence::new(&rna_str[start_pos..]);
            let amino_acids = self.translate(&from_start);
            
            // 在第一个终止密码子处停止
            let mut result = Vec::new();
            for aa in amino_acids {
                if aa.is_stop() {
                    break;
                }
                result.push(aa);
            }
            
            return result;
        }
        
        Vec::new()
    }

    /// 查找所有开放阅读框 (ORF)
    pub fn find_orfs(&self, sequence: &GeneSequence, min_length: usize) -> Vec<OpenReadingFrame> {
        let rna_str = sequence.to_rna_string();
        let mut orfs = Vec::new();

        // 检查所有三个阅读框
        for frame in 0..3 {
            let mut i = frame;
            while i + 3 <= rna_str.len() {
                let codon = &rna_str[i..i + 3];
                if codon == "AUG" {
                    // 找到起始密码子，尝试找到对应的终止密码子
                    if let Some(orflen) = self.find_orf_end(&rna_str, i) {
                        if orflen >= min_length * 3 {
                            orfs.push(OpenReadingFrame {
                                start: i,
                                end: i + orflen,
                                frame: frame + 1,
                                amino_acids: self.translate(&GeneSequence::new(&rna_str[i..i + orflen])),
                            });
                        }
                    }
                }
                i += 3;
            }
        }

        orfs
    }

    /// 找到 ORF 的结束位置
    fn find_orf_end(&self, rna: &str, start: usize) -> Option<usize> {
        let stop_codons = CodonTable::stop_codons();
        
        for i in (start..rna.len()).step_by(3) {
            if i + 3 > rna.len() {
                break;
            }
            let codon = &rna[i..i + 3];
            if stop_codons.contains(&codon) {
                return Some(i + 3 - start);
            }
        }
        
        None
    }
}

impl Default for Translator {
    fn default() -> Self {
        Self::new()
    }
}

/// 开放阅读框
#[derive(Debug, Clone)]
pub struct OpenReadingFrame {
    /// 起始位置 (0-indexed)
    pub start: usize,
    /// 结束位置 (不含)
    pub end: usize,
    /// 阅读框 (1, 2, 3)
    pub frame: usize,
    /// 氨基酸序列
    pub amino_acids: Vec<AminoAcid>,
}

impl OpenReadingFrame {
    /// 获取 ORF 长度 (核苷酸数)
    pub fn length(&self) -> usize {
        self.end - self.start
    }

    /// 获取蛋白质序列字符串
    pub fn protein_string(&self) -> String {
        self.amino_acids.iter()
            .map(|aa| aa.symbol())
            .collect()
    }
}

/// 序列比对工具
pub struct SequenceAligner;

impl SequenceAligner {
    /// 计算两个序列的汉明距离
    /// 两个序列必须等长
    pub fn hamming_distance(seq1: &GeneSequence, seq2: &GeneSequence) -> Result<usize, String> {
        if seq1.len() != seq2.len() {
            return Err("Sequences must have equal length for Hamming distance".to_string());
        }

        let distance = seq1.sequence.iter()
            .zip(seq2.sequence.iter())
            .filter(|(a, b)| {
                a.to_dna_char().to_ascii_uppercase() != b.to_dna_char().to_ascii_uppercase()
            })
            .count();

        Ok(distance)
    }

    /// 计算序列相似度 (百分比)
    pub fn similarity(seq1: &GeneSequence, seq2: &GeneSequence) -> f64 {
        if seq1.len() == 0 || seq2.len() == 0 {
            return 0.0;
        }

        let min_len = seq1.len().min(seq2.len());
        let matches = seq1.sequence.iter()
            .zip(seq2.sequence.iter())
            .filter(|(a, b)| {
                a.to_dna_char().to_ascii_uppercase() == b.to_dna_char().to_ascii_uppercase()
            })
            .count();

        (matches as f64 / min_len as f64) * 100.0
    }

    /// 查找变异位点
    pub fn find_mutations(seq1: &GeneSequence, seq2: &GeneSequence) -> Vec<Mutation> {
        let mut mutations = Vec::new();
        let min_len = seq1.len().min(seq2.len());

        for i in 0..min_len {
            let n1 = seq1.sequence[i].to_dna_char();
            let n2 = seq2.sequence[i].to_dna_char();
            
            if n1 != n2 {
                mutations.push(Mutation {
                    position: i,
                    original: n1,
                    mutated: n2,
                });
            }
        }

        // 处理插入/缺失
        if seq1.len() > seq2.len() {
            for i in min_len..seq1.len() {
                mutations.push(Mutation {
                    position: i,
                    original: seq1.sequence[i].to_dna_char(),
                    mutated: '-',
                });
            }
        } else if seq2.len() > seq1.len() {
            for i in min_len..seq2.len() {
                mutations.push(Mutation {
                    position: i,
                    original: '-',
                    mutated: seq2.sequence[i].to_dna_char(),
                });
            }
        }

        mutations
    }
}

/// 变异位点
#[derive(Debug, Clone)]
pub struct Mutation {
    /// 位置 (0-indexed)
    pub position: usize,
    /// 原始碱基
    pub original: char,
    /// 变异后碱基
    pub mutated: char,
}

impl Mutation {
    /// 是否为转换突变 (嘌呤↔嘌呤 或 嘧啶↔嘧啶)
    pub fn is_transition(&self) -> bool {
        let is_purine = |c: char| c == 'A' || c == 'G';
        let is_pyrimidine = |c: char| c == 'T' || c == 'C' || c == 'U';
        
        (is_purine(self.original) && is_purine(self.mutated)) ||
        (is_pyrimidine(self.original) && is_pyrimidine(self.mutated))
    }

    /// 是否为颠换突变 (嘌呤↔嘧啶)
    pub fn is_transversion(&self) -> bool {
        let is_purine = |c: char| c == 'A' || c == 'G';
        let is_pyrimidine = |c: char| c == 'T' || c == 'C' || c == 'U';
        
        (is_purine(self.original) && is_pyrimidine(self.mutated)) ||
        (is_pyrimidine(self.original) && is_purine(self.mutated))
    }

    /// 获取变异描述
    pub fn description(&self) -> String {
        if self.original == '-' {
            format!("Insertion at {}: {}", self.position, self.mutated)
        } else if self.mutated == '-' {
            format!("Deletion at {}: {}", self.position, self.original)
        } else if self.is_transition() {
            format!("Transition at {}: {} → {}", self.position, self.original, self.mutated)
        } else if self.is_transversion() {
            format!("Transversion at {}: {} → {}", self.position, self.original, self.mutated)
        } else {
            format!("Mutation at {}: {} → {}", self.position, self.original, self.mutated)
        }
    }
}

/// DNA 验证器
pub struct DnaValidator;

impl DnaValidator {
    /// 验证是否为有效 DNA 序列
    pub fn is_valid_dna(sequence: &str) -> bool {
        for c in sequence.chars() {
            match c.to_ascii_uppercase() {
                'A' | 'T' | 'G' | 'C' => {}
                ' ' | '\n' | '\r' | '\t' => {}
                _ => return false,
            }
        }
        true
    }

    /// 验证是否为有效 RNA 序列
    pub fn is_valid_rna(sequence: &str) -> bool {
        for c in sequence.chars() {
            match c.to_ascii_uppercase() {
                'A' | 'U' | 'G' | 'C' => {}
                ' ' | '\n' | '\r' | '\t' => {}
                _ => return false,
            }
        }
        true
    }

    /// 清理序列 (移除空白和非标准字符)
    pub fn clean_sequence(sequence: &str) -> String {
        sequence.chars()
            .filter(|c| matches!(c.to_ascii_uppercase(), 'A' | 'T' | 'U' | 'G' | 'C'))
            .collect()
    }

    /// 验证序列长度是否为 3 的倍数 (完整密码子)
    pub fn is_complete_codons(sequence: &GeneSequence) -> bool {
        sequence.len() % 3 == 0
    }
}

/// 引物设计工具
pub struct PrimerDesigner;

impl PrimerDesigner {
    /// 设计 PCR 正向引物
    pub fn design_forward_primer(
        sequence: &GeneSequence,
        target_start: usize,
        primer_length: usize,
    ) -> Option<String> {
        if target_start + primer_length > sequence.len() {
            return None;
        }

        let primer: String = sequence.sequence[target_start..target_start + primer_length]
            .iter()
            .map(|n| n.to_dna_char())
            .collect();

        Some(primer)
    }

    /// 设计 PCR 反向引物
    pub fn design_reverse_primer(
        sequence: &GeneSequence,
        target_end: usize,
        primer_length: usize,
    ) -> Option<String> {
        if target_end < primer_length || target_end > sequence.len() {
            return None;
        }

        let primer: String = sequence.sequence[target_end - primer_length..target_end]
            .iter()
            .rev()
            .map(|n| n.dna_complement().to_dna_char())
            .collect();

        Some(primer)
    }

    /// 计算 PCR 产物长度
    pub fn pcr_product_length(forward_pos: usize, reverse_pos: usize) -> usize {
        if reverse_pos > forward_pos {
            reverse_pos - forward_pos + 1
        } else {
            0
        }
    }

    /// 计算引物熔解温度 (Tm) - 使用 Wallace 规则
    /// Tm = 4(G+C) + 2(A+T)
    pub fn calculate_tm(primer: &str) -> f64 {
        let gc = primer.chars()
            .filter(|c| matches!(c.to_ascii_uppercase(), 'G' | 'C'))
            .count();
        let at = primer.chars()
            .filter(|c| matches!(c.to_ascii_uppercase(), 'A' | 'T'))
            .count();

        (4 * gc + 2 * at) as f64
    }

    /// 检查引物是否存在二聚体
    pub fn has_dimer(primer: &str) -> bool {
        let rev_comp: String = primer.chars()
            .rev()
            .map(|c| match c.to_ascii_uppercase() {
                'A' => 'T',
                'T' => 'A',
                'G' => 'C',
                'C' => 'G',
                _ => c,
            })
            .collect();

        // 简单检查: 如果引物末尾与反向互补序列有连续3个以上匹配
        let primer_upper: String = primer.to_uppercase();
        for i in 0..primer.len() - 3 {
            let sub = &primer_upper[i..i + 4];
            if rev_comp.contains(sub) {
                return true;
            }
        }

        false
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_nucleotide_creation() {
        assert_eq!(Nucleotide::from_char('A'), Nucleotide::Adenine);
        assert_eq!(Nucleotide::from_char('T'), Nucleotide::Thymine);
        assert_eq!(Nucleotide::from_char('U'), Nucleotide::Uracil);
        assert_eq!(Nucleotide::from_char('G'), Nucleotide::Guanine);
        assert_eq!(Nucleotide::from_char('C'), Nucleotide::Cytosine);
    }

    #[test]
    fn test_nucleotide_complement() {
        assert_eq!(Nucleotide::Adenine.dna_complement(), Nucleotide::Thymine);
        assert_eq!(Nucleotide::Thymine.dna_complement(), Nucleotide::Adenine);
        assert_eq!(Nucleotide::Guanine.dna_complement(), Nucleotide::Cytosine);
        assert_eq!(Nucleotide::Cytosine.dna_complement(), Nucleotide::Guanine);
    }

    #[test]
    fn test_gene_sequence_creation() {
        let seq = GeneSequence::new("ATGC");
        assert_eq!(seq.len(), 4);
        assert_eq!(seq.sequence_type(), SequenceType::DNA);
    }

    #[test]
    fn test_gc_content() {
        let seq = GeneSequence::new("ATGC");
        let gc = seq.gc_content();
        assert!((gc - 50.0).abs() < 0.01);
    }

    #[test]
    fn test_reverse_complement() {
        let seq = GeneSequence::new("ATGC");
        let rev_comp = seq.reverse_complement();
        assert_eq!(rev_comp.to_dna_string(), "GCAT");
    }

    #[test]
    fn test_transcription() {
        let dna = GeneSequence::new("ATGC");
        let rna = dna.transcribe();
        assert_eq!(rna.to_rna_string(), "AUGC");
    }

    #[test]
    fn test_translation() {
        let rna = GeneSequence::new("AUGUUUUAA"); // Met-Phe-Stop
        let translator = Translator::new();
        let protein = translator.translate(&rna);
        
        assert_eq!(protein.len(), 3);
        assert_eq!(protein[0], AminoAcid::Met);
        assert_eq!(protein[1], AminoAcid::Phe);
        assert_eq!(protein[2], AminoAcid::Stop);
    }

    #[test]
    fn test_codon_table() {
        let table = CodonTable::standard();
        
        assert_eq!(table.translate_codon("AUG"), Some(AminoAcid::Met));
        assert_eq!(table.translate_codon("UUU"), Some(AminoAcid::Phe));
        assert_eq!(table.translate_codon("UAA"), Some(AminoAcid::Stop));
    }

    #[test]
    fn test_hamming_distance() {
        let seq1 = GeneSequence::new("ATGC");
        let seq2 = GeneSequence::new("ATGG");
        
        let distance = SequenceAligner::hamming_distance(&seq1, &seq2).unwrap();
        assert_eq!(distance, 1);
    }

    #[test]
    fn test_dna_validator() {
        assert!(DnaValidator::is_valid_dna("ATGC"));
        assert!(!DnaValidator::is_valid_dna("ATGX"));
        assert!(DnaValidator::is_valid_rna("AUGC"));
        assert!(!DnaValidator::is_valid_rna("AUGT"));
    }

    #[test]
    fn test_primer_design() {
        let seq = GeneSequence::new("ATGCTAGCTAGCTAGCTAGC");
        let forward = PrimerDesigner::design_forward_primer(&seq, 0, 6);
        assert_eq!(forward, Some("ATGCTA".to_string()));
        
        let tm = PrimerDesigner::calculate_tm("ATGCTA");
        assert!(tm > 0.0);
    }

    #[test]
    fn test_find_mutations() {
        let seq1 = GeneSequence::new("ATGC");
        let seq2 = GeneSequence::new("ATGG");
        
        let mutations = SequenceAligner::find_mutations(&seq1, &seq2);
        assert_eq!(mutations.len(), 1);
        assert_eq!(mutations[0].position, 3);
        assert_eq!(mutations[0].original, 'C');
        assert_eq!(mutations[0].mutated, 'G');
    }

    #[test]
    fn test_find_subsequence() {
        let seq = GeneSequence::new("ATGCTAGCTAGC");
        let positions = seq.find("TAG");
        assert_eq!(positions, vec![4, 8]);
    }

    #[test]
    fn test_amino_acid_properties() {
        assert_eq!(AminoAcid::Met.code(), "Met");
        assert_eq!(AminoAcid::Met.symbol(), 'M');
        assert_eq!(AminoAcid::Met.name(), "Methionine");
        assert!(AminoAcid::Stop.is_stop());
    }

    #[test]
    fn test_orf_finding() {
        // Sequence with clear AUG start and UAA stop
        // RNA: AUGUUUUAA -> positions 0-8, contains start and stop
        let seq = GeneSequence::new("ATGTTTTAA"); // DNA version
        let translator = Translator::new();
        let orfs = translator.find_orfs(&seq, 1);
        
        assert!(!orfs.is_empty(), "Should find at least one ORF");
    }
}
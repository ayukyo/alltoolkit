//! DNA Sequence Utils - DNA/RNA Sequence Analysis and Manipulation
//!
//! A comprehensive toolkit for DNA and RNA sequence operations without external dependencies.
//! Perfect for bioinformatics applications, genetic analysis, and sequence manipulation.
//!
//! # Features
//! - DNA validation and cleaning
//! - RNA transcription
//! - Complement and reverse complement
//! - GC content calculation
//! - Protein translation with codon tables
//! - Sequence mutations and variations
//! - Hamming distance for sequences
//! - Motif finding and pattern matching
//! - Sequence statistics
//!
//! # Example
//! ```
//! use dna_sequence_utils::{DNASequence, RNASequence, ProteinSequence};
//!
//! let dna = DNASequence::new("ATGCGATCGATCG").unwrap();
//! println!("GC Content: {:.2}%", dna.gc_content());
//! println!("Complement: {}", dna.complement());
//! println!("RNA: {}", dna.transcribe().as_str());
//! ```

use std::collections::HashMap;
use std::fmt;

/// Standard DNA nucleotides
pub const DNA_NUCLEOTIDES: &str = "ATCG";
/// Standard RNA nucleotides
pub const RNA_NUCLEOTIDES: &str = "AUCG";
/// Ambiguous DNA nucleotides (IUPAC codes)
pub const AMBIGUOUS_DNA: &str = "ATCGNWSMKRYBDHV";
/// Ambiguous RNA nucleotides (IUPAC codes)
pub const AMBIGUOUS_RNA: &str = "AUCGNWSMKRYBDHV";

/// Codon table for standard genetic code (NCBI standard table 1)
pub fn get_codon_table() -> HashMap<&'static str, char> {
    let mut table = HashMap::new();
    
    // Phenylalanine (F)
    table.insert("UUU", 'F'); table.insert("UUC", 'F');
    // Leucine (L)
    table.insert("UUA", 'L'); table.insert("UUG", 'L');
    table.insert("CUU", 'L'); table.insert("CUC", 'L');
    table.insert("CUA", 'L'); table.insert("CUG", 'L');
    // Isoleucine (I)
    table.insert("AUU", 'I'); table.insert("AUC", 'I');
    table.insert("AUA", 'I');
    // Methionine (M) - Start codon
    table.insert("AUG", 'M');
    // Valine (V)
    table.insert("GUU", 'V'); table.insert("GUC", 'V');
    table.insert("GUA", 'V'); table.insert("GUG", 'V');
    // Serine (S)
    table.insert("UCU", 'S'); table.insert("UCC", 'S');
    table.insert("UCA", 'S'); table.insert("UCG", 'S');
    table.insert("AGU", 'S'); table.insert("AGC", 'S');
    // Proline (P)
    table.insert("CCU", 'P'); table.insert("CCC", 'P');
    table.insert("CCA", 'P'); table.insert("CCG", 'P');
    // Threonine (T)
    table.insert("ACU", 'T'); table.insert("ACC", 'T');
    table.insert("ACA", 'T'); table.insert("ACG", 'T');
    // Alanine (A)
    table.insert("GCU", 'A'); table.insert("GCC", 'A');
    table.insert("GCA", 'A'); table.insert("GCG", 'A');
    // Tyrosine (Y)
    table.insert("UAU", 'Y'); table.insert("UAC", 'Y');
    // Histidine (H)
    table.insert("CAU", 'H'); table.insert("CAC", 'H');
    // Glutamine (Q)
    table.insert("CAA", 'Q'); table.insert("CAG", 'Q');
    // Asparagine (N)
    table.insert("AAU", 'N'); table.insert("AAC", 'N');
    // Lysine (K)
    table.insert("AAA", 'K'); table.insert("AAG", 'K');
    // Aspartic acid (D)
    table.insert("GAU", 'D'); table.insert("GAC", 'D');
    // Glutamic acid (E)
    table.insert("GAA", 'E'); table.insert("GAG", 'E');
    // Cysteine (C)
    table.insert("UGU", 'C'); table.insert("UGC", 'C');
    // Tryptophan (W)
    table.insert("UGG", 'W');
    // Arginine (R)
    table.insert("CGU", 'R'); table.insert("CGC", 'R');
    table.insert("CGA", 'R'); table.insert("CGG", 'R');
    table.insert("AGA", 'R'); table.insert("AGG", 'R');
    // Glycine (G)
    table.insert("GGU", 'G'); table.insert("GGC", 'G');
    table.insert("GGA", 'G'); table.insert("GGG", 'G');
    // Stop codons (*)
    table.insert("UAA", '*'); table.insert("UAG", '*');
    table.insert("UGA", '*');
    
    table
}

/// IUPAC ambiguous nucleotide codes
pub fn get_iupac_codes() -> HashMap<char, &'static str> {
    let mut codes = HashMap::new();
    codes.insert('A', "A");
    codes.insert('C', "C");
    codes.insert('G', "G");
    codes.insert('T', "T");
    codes.insert('U', "U");
    codes.insert('R', "AG");      // Purine
    codes.insert('Y', "CT");      // Pyrimidine
    codes.insert('S', "GC");       // Strong
    codes.insert('W', "AT");       // Weak
    codes.insert('K', "GT");       // Keto
    codes.insert('M', "AC");       // Amino
    codes.insert('B', "CGT");      // Not A
    codes.insert('D', "AGT");      // Not C
    codes.insert('H', "ACT");      // Not G
    codes.insert('V', "ACG");      // Not T
    codes.insert('N', "ACGT");     // Any
    codes
}

/// Complementary base mapping
pub fn get_complement_table() -> HashMap<char, char> {
    let mut table = HashMap::new();
    table.insert('A', 'T');
    table.insert('T', 'A');
    table.insert('C', 'G');
    table.insert('G', 'C');
    table.insert('U', 'A');       // RNA complement
    table.insert('R', 'Y');       // Purine -> Pyrimidine
    table.insert('Y', 'R');
    table.insert('S', 'S');
    table.insert('W', 'W');
    table.insert('K', 'M');
    table.insert('M', 'K');
    table.insert('B', 'V');
    table.insert('D', 'H');
    table.insert('H', 'D');
    table.insert('V', 'B');
    table.insert('N', 'N');
    table
}

/// DNA Sequence error types
#[derive(Debug, Clone, PartialEq)]
pub enum DNAError {
    InvalidCharacter(char),
    EmptySequence,
    InvalidLength { expected: usize, actual: usize },
    InvalidCodon(String),
    InvalidFormat(String),
}

impl fmt::Display for DNAError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            DNAError::InvalidCharacter(c) => write!(f, "Invalid nucleotide character: '{}'", c),
            DNAError::EmptySequence => write!(f, "Sequence cannot be empty"),
            DNAError::InvalidLength { expected, actual } => {
                write!(f, "Invalid sequence length: expected {}, got {}", expected, actual)
            }
            DNAError::InvalidCodon(codon) => write!(f, "Invalid codon: '{}'", codon),
            DNAError::InvalidFormat(msg) => write!(f, "Invalid format: {}", msg),
        }
    }
}

impl std::error::Error for DNAError {}

/// DNA Sequence representation
#[derive(Debug, Clone, PartialEq)]
pub struct DNASequence {
    sequence: String,
}

impl DNASequence {
    /// Create a new DNA sequence from a string
    pub fn new(seq: &str) -> Result<Self, DNAError> {
        let seq = seq.to_uppercase().replace(" ", "").replace("\n", "").replace("\t", "");
        if seq.is_empty() {
            return Err(DNAError::EmptySequence);
        }
        
        for c in seq.chars() {
            if !AMBIGUOUS_DNA.contains(c) {
                return Err(DNAError::InvalidCharacter(c));
            }
        }
        
        Ok(DNASequence { sequence: seq })
    }
    
    /// Create a DNA sequence without validation (use with caution)
    pub fn new_unchecked(seq: &str) -> Self {
        let seq = seq.to_uppercase().replace(" ", "").replace("\n", "").replace("\t", "");
        DNASequence { sequence: seq }
    }
    
    /// Get the sequence as a string slice
    pub fn as_str(&self) -> &str {
        &self.sequence
    }
    
    /// Get the length of the sequence
    pub fn len(&self) -> usize {
        self.sequence.len()
    }
    
    /// Check if the sequence is empty
    pub fn is_empty(&self) -> bool {
        self.sequence.is_empty()
    }
    
    /// Get the sequence as a vector of characters
    pub fn to_vec(&self) -> Vec<char> {
        self.sequence.chars().collect()
    }
    
    /// Get a subsequence
    pub fn subsequence(&self, start: usize, end: usize) -> Result<Self, DNAError> {
        if start >= self.len() || end > self.len() || start >= end {
            return Err(DNAError::InvalidFormat("Invalid subsequence range".to_string()));
        }
        Ok(DNASequence { sequence: self.sequence[start..end].to_string() })
    }
    
    /// Calculate GC content as a percentage (0-100)
    pub fn gc_content(&self) -> f64 {
        let gc = self.sequence.chars()
            .filter(|&c| c == 'G' || c == 'C')
            .count();
        (gc as f64 / self.len() as f64) * 100.0
    }
    
    /// Calculate AT content as a percentage (0-100)
    pub fn at_content(&self) -> f64 {
        100.0 - self.gc_content()
    }
    
    /// Get nucleotide counts
    pub fn nucleotide_counts(&self) -> HashMap<char, usize> {
        let mut counts = HashMap::new();
        for c in self.sequence.chars() {
            *counts.entry(c).or_insert(0) += 1;
        }
        counts
    }
    
    /// Get the complement sequence
    pub fn complement(&self) -> Self {
        let complement_table = get_complement_table();
        let complemented: String = self.sequence.chars()
            .map(|c| *complement_table.get(&c).unwrap_or(&c))
            .collect();
        DNASequence { sequence: complemented }
    }
    
    /// Get the reverse complement sequence
    pub fn reverse_complement(&self) -> Self {
        let complement_table = get_complement_table();
        let rev_comp: String = self.sequence.chars()
            .rev()
            .map(|c| *complement_table.get(&c).unwrap_or(&c))
            .collect();
        DNASequence { sequence: rev_comp }
    }
    
    /// Transcribe DNA to RNA
    pub fn transcribe(&self) -> RNASequence {
        let rna: String = self.sequence.chars()
            .map(|c| if c == 'T' { 'U' } else { c })
            .collect();
        RNASequence { sequence: rna }
    }
    
    /// Translate DNA to protein sequence
    pub fn translate(&self) -> ProteinSequence {
        self.transcribe().translate()
    }
    
    /// Translate DNA to protein with frame offset (0, 1, or 2)
    pub fn translate_with_frame(&self, frame: usize) -> Result<ProteinSequence, DNAError> {
        if frame > 2 {
            return Err(DNAError::InvalidFormat("Frame must be 0, 1, or 2".to_string()));
        }
        Ok(self.transcribe().translate_with_offset(frame))
    }
    
    /// Find all occurrences of a pattern
    pub fn find_pattern(&self, pattern: &str) -> Vec<usize> {
        let pattern = pattern.to_uppercase();
        let mut positions = Vec::new();
        
        for i in 0..self.sequence.len().saturating_sub(pattern.len() - 1) {
            if self.sequence[i..].starts_with(&pattern) {
                positions.push(i);
            }
        }
        positions
    }
    
    /// Count occurrences of a pattern
    pub fn count_pattern(&self, pattern: &str) -> usize {
        self.find_pattern(pattern).len()
    }
    
    /// Calculate Hamming distance to another sequence
    pub fn hamming_distance(&self, other: &DNASequence) -> Result<usize, DNAError> {
        if self.len() != other.len() {
            return Err(DNAError::InvalidLength {
                expected: self.len(),
                actual: other.len(),
            });
        }
        
        let distance = self.sequence.chars()
            .zip(other.sequence.chars())
            .filter(|(a, b)| a != b)
            .count();
        Ok(distance)
    }
    
    /// Find mutation positions compared to another sequence
    pub fn find_mutations(&self, other: &DNASequence) -> Result<Vec<(usize, char, char)>, DNAError> {
        if self.len() != other.len() {
            return Err(DNAError::InvalidLength {
                expected: self.len(),
                actual: other.len(),
            });
        }
        
        let mutations = self.sequence.chars()
            .zip(other.sequence.chars())
            .enumerate()
            .filter_map(|(i, (a, b))| {
                if a != b {
                    Some((i, a, b))
                } else {
                    None
                }
            })
            .collect();
        Ok(mutations)
    }
    
    /// Calculate molecular weight (g/mol)
    /// Average molecular weights: A=313.21, T=304.19, G=329.21, C=289.18
    pub fn molecular_weight(&self) -> f64 {
        let weights: HashMap<char, f64> = [
            ('A', 313.21),
            ('T', 304.19),
            ('G', 329.21),
            ('C', 289.18),
        ].iter().cloned().collect();
        
        self.sequence.chars()
            .map(|c| weights.get(&c).copied().unwrap_or(0.0))
            .sum()
    }
    
    /// Calculate melting temperature (Tm) using Wallace rule
    /// Tm = 2°C × (A + T) + 4°C × (G + C) for oligos < 14 bp
    /// For longer sequences, uses more accurate formula
    pub fn melting_temperature(&self) -> f64 {
        let counts = self.nucleotide_counts();
        let a = counts.get(&'A').copied().unwrap_or(0) as f64;
        let t = counts.get(&'T').copied().unwrap_or(0) as f64;
        let g = counts.get(&'G').copied().unwrap_or(0) as f64;
        let c = counts.get(&'C').copied().unwrap_or(0) as f64;
        
        if self.len() < 14 {
            // Wallace rule
            2.0 * (a + t) + 4.0 * (g + c)
        } else {
            // More accurate formula for longer sequences
            64.9 + 41.0 * (g + c - 16.4) / (a + t + g + c)
        }
    }
    
    /// Check if sequence contains a start codon (ATG)
    pub fn has_start_codon(&self) -> bool {
        self.find_pattern("ATG").len() > 0
    }
    
    /// Find all start codon positions
    pub fn find_start_codons(&self) -> Vec<usize> {
        self.find_pattern("ATG")
    }
    
    /// Find all stop codon positions (TAA, TAG, TGA)
    pub fn find_stop_codons(&self) -> Vec<usize> {
        let mut positions = Vec::new();
        positions.extend(self.find_pattern("TAA"));
        positions.extend(self.find_pattern("TAG"));
        positions.extend(self.find_pattern("TGA"));
        positions.sort();
        positions
    }
    
    /// Get the reading frames (three possible for each strand)
    pub fn reading_frames(&self) -> Vec<DNASequence> {
        let mut frames = Vec::new();
        for i in 0..3 {
            let len = (self.len() - i) / 3 * 3 + i;
            frames.push(DNASequence { 
                sequence: self.sequence[i..len].to_string() 
            });
        }
        frames
    }
    
    /// Find open reading frames (ORFs)
    pub fn find_orfs(&self, min_length: usize) -> Vec<ORF> {
        let mut orfs = Vec::new();
        let stop_codons = ["TAA", "TAG", "TGA"];
        
        for frame in 0..3 {
            let mut in_orf = false;
            let mut orf_start = 0;
            
            for i in (frame..self.len().saturating_sub(2)).step_by(3) {
                let codon = &self.sequence[i..i+3];
                
                if codon == "ATG" && !in_orf {
                    in_orf = true;
                    orf_start = i;
                } else if stop_codons.contains(&codon) && in_orf {
                    let length = i + 3 - orf_start;
                    if length >= min_length {
                        orfs.push(ORF {
                            start: orf_start,
                            end: i + 3,
                            frame: frame + 1,
                            sequence: self.sequence[orf_start..i+3].to_string(),
                        });
                    }
                    in_orf = false;
                }
            }
        }
        orfs
    }
    
    /// Convert to FASTA format
    pub fn to_fasta(&self, header: &str) -> String {
        let mut fasta = format!(">{}\n", header);
        for (i, chunk) in self.sequence.as_bytes().chunks(60).enumerate() {
            if i > 0 {
                fasta.push('\n');
            }
            fasta.push_str(&String::from_utf8_lossy(chunk));
        }
        fasta
    }
    
    /// Check if sequence is a palindrome (reads same on both strands)
    pub fn is_palindromic(&self) -> bool {
        *self == self.reverse_complement()
    }
    
    /// Find palindromic sequences (restriction enzyme sites)
    pub fn find_palindromes(&self, min_len: usize, max_len: usize) -> Vec<(usize, String)> {
        let mut palindromes = Vec::new();
        
        for len in min_len..=max_len.min(self.len()) {
            for i in 0..=self.len() - len {
                let subseq = &self.sequence[i..i + len];
                let dna = DNASequence::new_unchecked(subseq);
                if dna.is_palindromic() {
                    palindromes.push((i, subseq.to_string()));
                }
            }
        }
        palindromes
    }
    
    /// Calculate sequence complexity (Shannon entropy)
    pub fn complexity(&self) -> f64 {
        let counts = self.nucleotide_counts();
        let total = self.len() as f64;
        
        let mut entropy = 0.0;
        for &count in counts.values() {
            if count > 0 {
                let p = count as f64 / total;
                entropy -= p * p.log2();
            }
        }
        entropy
    }
    
    /// Generate random mutation at a position
    pub fn mutate(&self, position: usize) -> Result<Self, DNAError> {
        if position >= self.len() {
            return Err(DNAError::InvalidFormat("Position out of bounds".to_string()));
        }
        
        let bases = ['A', 'T', 'C', 'G'];
        let current = self.sequence.chars().nth(position).unwrap();
        let new_base = bases.iter()
            .filter(|&&b| b != current)
            .nth(rand_simple(position) % 3)
            .unwrap();
        
        let mut mutated = self.sequence.clone();
        mutated.replace_range(position..position+1, &new_base.to_string());
        Ok(DNASequence { sequence: mutated })
    }
    
    /// Concatenate with another DNA sequence
    pub fn concat(&self, other: &DNASequence) -> DNASequence {
        DNASequence { 
            sequence: format!("{}{}", self.sequence, other.sequence) 
        }
    }
}

impl fmt::Display for DNASequence {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}", self.sequence)
    }
}

/// RNA Sequence representation
#[derive(Debug, Clone, PartialEq)]
pub struct RNASequence {
    sequence: String,
}

impl RNASequence {
    /// Create a new RNA sequence
    pub fn new(seq: &str) -> Result<Self, DNAError> {
        let seq = seq.to_uppercase().replace(" ", "").replace("\n", "").replace("\t", "");
        if seq.is_empty() {
            return Err(DNAError::EmptySequence);
        }
        
        for c in seq.chars() {
            if !AMBIGUOUS_RNA.contains(c) {
                return Err(DNAError::InvalidCharacter(c));
            }
        }
        
        Ok(RNASequence { sequence: seq })
    }
    
    /// Get the sequence as a string slice
    pub fn as_str(&self) -> &str {
        &self.sequence
    }
    
    /// Get the length
    pub fn len(&self) -> usize {
        self.sequence.len()
    }
    
    /// Check if empty
    pub fn is_empty(&self) -> bool {
        self.sequence.is_empty()
    }
    
    /// Reverse transcribe RNA to DNA
    pub fn reverse_transcribe(&self) -> DNASequence {
        let dna: String = self.sequence.chars()
            .map(|c| if c == 'U' { 'T' } else { c })
            .collect();
        DNASequence { sequence: dna }
    }
    
    /// Translate RNA to protein
    pub fn translate(&self) -> ProteinSequence {
        self.translate_with_offset(0)
    }
    
    /// Translate with frame offset
    pub fn translate_with_offset(&self, offset: usize) -> ProteinSequence {
        let codon_table = get_codon_table();
        let mut protein = String::new();
        
        for i in (offset..self.sequence.len().saturating_sub(2)).step_by(3) {
            let codon = &self.sequence[i..i+3.min(self.sequence.len() - i)];
            if codon.len() == 3 {
                if let Some(&aa) = codon_table.get(codon) {
                    if aa == '*' {
                        break; // Stop codon
                    }
                    protein.push(aa);
                } else {
                    protein.push('X'); // Unknown
                }
            }
        }
        
        ProteinSequence { sequence: protein }
    }
    
    /// Get nucleotide counts
    pub fn nucleotide_counts(&self) -> HashMap<char, usize> {
        let mut counts = HashMap::new();
        for c in self.sequence.chars() {
            *counts.entry(c).or_insert(0) += 1;
        }
        counts
    }
}

impl fmt::Display for RNASequence {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}", self.sequence)
    }
}

/// Protein Sequence representation
#[derive(Debug, Clone, PartialEq)]
pub struct ProteinSequence {
    sequence: String,
}

impl ProteinSequence {
    /// Create a new protein sequence
    pub fn new(seq: &str) -> Result<Self, DNAError> {
        let seq = seq.to_uppercase().replace(" ", "").replace("\n", "").replace("\t", "");
        if seq.is_empty() {
            return Err(DNAError::EmptySequence);
        }
        
        let valid_aa = "ACDEFGHIKLMNPQRSTVWY*";
        for c in seq.chars() {
            if !valid_aa.contains(c) && c != 'X' {
                return Err(DNAError::InvalidCharacter(c));
            }
        }
        
        Ok(ProteinSequence { sequence: seq })
    }
    
    /// Get the sequence as a string slice
    pub fn as_str(&self) -> &str {
        &self.sequence
    }
    
    /// Get the length
    pub fn len(&self) -> usize {
        self.sequence.len()
    }
    
    /// Check if empty
    pub fn is_empty(&self) -> bool {
        self.sequence.is_empty()
    }
    
    /// Get amino acid counts
    pub fn amino_acid_counts(&self) -> HashMap<char, usize> {
        let mut counts = HashMap::new();
        for c in self.sequence.chars() {
            *counts.entry(c).or_insert(0) += 1;
        }
        counts
    }
    
    /// Calculate molecular weight of protein (kDa)
    pub fn molecular_weight(&self) -> f64 {
        // Average amino acid molecular weights in Daltons
        let weights: HashMap<char, f64> = [
            ('A', 89.09), ('C', 121.15), ('D', 133.10), ('E', 147.13),
            ('F', 165.19), ('G', 75.07), ('H', 155.16), ('I', 131.17),
            ('K', 146.19), ('L', 131.17), ('M', 149.21), ('N', 132.12),
            ('P', 115.13), ('Q', 146.15), ('R', 174.20), ('S', 105.09),
            ('T', 119.12), ('V', 117.15), ('W', 204.23), ('Y', 181.19),
        ].iter().cloned().collect();
        
        let total: f64 = self.sequence.chars()
            .filter_map(|c| weights.get(&c).copied())
            .sum();
        
        // Subtract water for peptide bonds
        total - 18.015 * (self.sequence.len().saturating_sub(1)) as f64
    }
    
    /// Calculate isoelectric point (approximate)
    pub fn isoelectric_point(&self) -> f64 {
        // Simplified calculation based on amino acid composition
        let counts = self.amino_acid_counts();
        let acidic = counts.get(&'D').copied().unwrap_or(0) + counts.get(&'E').copied().unwrap_or(0);
        let basic = counts.get(&'K').copied().unwrap_or(0) + counts.get(&'R').copied().unwrap_or(0) 
                  + counts.get(&'H').copied().unwrap_or(0);
        
        // Approximate pI based on charge balance
        let total = acidic + basic;
        if total == 0 {
            7.0
        } else {
            7.0 + (basic as f64 - acidic as f64) / total as f64 * 2.0
        }
    }
    
    /// Count hydrophobic amino acids
    pub fn hydrophobic_count(&self) -> usize {
        let hydrophobic = "AILMFWYV";
        self.sequence.chars().filter(|c| hydrophobic.contains(*c)).count()
    }
    
    /// Count hydrophilic amino acids
    pub fn hydrophilic_count(&self) -> usize {
        let hydrophilic = "DEKNQRHST";
        self.sequence.chars().filter(|c| hydrophilic.contains(*c)).count()
    }
    
    /// Calculate hydrophobicity score
    pub fn hydrophobicity(&self) -> f64 {
        // Kyte-Doolittle scale values
        let kd_values: HashMap<char, f64> = [
            ('A', 1.8), ('C', 2.5), ('D', -3.5), ('E', -3.5),
            ('F', 2.8), ('G', -0.4), ('H', -3.2), ('I', 4.5),
            ('K', -3.9), ('L', 3.8), ('M', 1.9), ('N', -3.5),
            ('P', -1.6), ('Q', -3.5), ('R', -4.5), ('S', -0.8),
            ('T', -0.7), ('V', 4.2), ('W', -0.9), ('Y', -1.3),
        ].iter().cloned().collect();
        
        let total: f64 = self.sequence.chars()
            .filter_map(|c| kd_values.get(&c).copied())
            .sum();
        
        total / self.sequence.len() as f64
    }
    
    /// Convert to FASTA format
    pub fn to_fasta(&self, header: &str) -> String {
        let mut fasta = format!(">{}\n", header);
        for (i, chunk) in self.sequence.as_bytes().chunks(60).enumerate() {
            if i > 0 {
                fasta.push('\n');
            }
            fasta.push_str(&String::from_utf8_lossy(chunk));
        }
        fasta
    }
}

impl fmt::Display for ProteinSequence {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}", self.sequence)
    }
}

/// Open Reading Frame representation
#[derive(Debug, Clone)]
pub struct ORF {
    pub start: usize,
    pub end: usize,
    pub frame: usize,
    pub sequence: String,
}

impl ORF {
    /// Get the length of the ORF
    pub fn len(&self) -> usize {
        self.end - self.start
    }
    
    /// Check if empty
    pub fn is_empty(&self) -> bool {
        self.start == self.end
    }
    
    /// Get the translated protein sequence
    pub fn translate(&self) -> ProteinSequence {
        DNASequence::new_unchecked(&self.sequence).translate()
    }
}

impl fmt::Display for ORF {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "ORF[{}]: {}..{} ({})", self.frame, self.start, self.end, self.sequence)
    }
}

/// Simple pseudo-random number generator for deterministic "randomness"
fn rand_simple(seed: usize) -> usize {
    let mut x = seed.wrapping_add(1);
    x ^= x << 13;
    x ^= x >> 17;
    x ^= x << 5;
    x
}

/// Parse a FASTA format string into sequences
pub fn parse_fasta(content: &str) -> Vec<(String, String)> {
    let mut sequences = Vec::new();
    let mut current_header = String::new();
    let mut current_seq = String::new();
    
    for line in content.lines() {
        let line = line.trim();
        if line.starts_with('>') {
            if !current_header.is_empty() && !current_seq.is_empty() {
                sequences.push((current_header.clone(), current_seq.clone()));
            }
            current_header = line[1..].to_string();
            current_seq = String::new();
        } else {
            current_seq.push_str(line);
        }
    }
    
    if !current_header.is_empty() && !current_seq.is_empty() {
        sequences.push((current_header, current_seq));
    }
    
    sequences
}

/// Calculate sequence identity between two sequences
pub fn sequence_identity(seq1: &DNASequence, seq2: &DNASequence) -> Result<f64, DNAError> {
    if seq1.len() != seq2.len() {
        return Err(DNAError::InvalidLength {
            expected: seq1.len(),
            actual: seq2.len(),
        });
    }
    
    let matches = seq1.as_str().chars()
        .zip(seq2.as_str().chars())
        .filter(|(a, b)| a == b)
        .count();
    
    Ok((matches as f64 / seq1.len() as f64) * 100.0)
}

/// Generate a consensus sequence from multiple sequences
pub fn consensus_sequence(sequences: &[DNASequence]) -> Result<DNASequence, DNAError> {
    if sequences.is_empty() {
        return Err(DNAError::EmptySequence);
    }
    
    let len = sequences[0].len();
    for seq in sequences {
        if seq.len() != len {
            return Err(DNAError::InvalidFormat("All sequences must have the same length".to_string()));
        }
    }
    
    let mut consensus = String::new();
    for i in 0..len {
        let mut counts: HashMap<char, usize> = HashMap::new();
        for seq in sequences {
            let c = seq.as_str().chars().nth(i).unwrap();
            *counts.entry(c).or_insert(0) += 1;
        }
        
        let most_common = counts.iter()
            .max_by_key(|&(_, count)| count)
            .map(|(&c, _)| c)
            .unwrap_or('N');
        consensus.push(most_common);
    }
    
    Ok(DNASequence { sequence: consensus })
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_dna_creation() {
        let dna = DNASequence::new("ATGCGATCG").unwrap();
        assert_eq!(dna.len(), 9);
        assert_eq!(dna.as_str(), "ATGCGATCG");
    }
    
    #[test]
    fn test_dna_invalid() {
        assert!(DNASequence::new("").is_err());
        assert!(DNASequence::new("ATGX").is_err());
    }
    
    #[test]
    fn test_gc_content() {
        let dna = DNASequence::new("GCGC").unwrap();
        assert_eq!(dna.gc_content(), 100.0);
        
        let dna2 = DNASequence::new("ATAT").unwrap();
        assert_eq!(dna2.gc_content(), 0.0);
        
        let dna3 = DNASequence::new("ATGC").unwrap();
        assert_eq!(dna3.gc_content(), 50.0);
    }
    
    #[test]
    fn test_complement() {
        let dna = DNASequence::new("ATGC").unwrap();
        assert_eq!(dna.complement().as_str(), "TACG");
    }
    
    #[test]
    fn test_reverse_complement() {
        let dna = DNASequence::new("ATGC").unwrap();
        assert_eq!(dna.reverse_complement().as_str(), "GCAT");
    }
    
    #[test]
    fn test_transcribe() {
        let dna = DNASequence::new("ATGC").unwrap();
        let rna = dna.transcribe();
        assert_eq!(rna.as_str(), "AUGC");
    }
    
    #[test]
    fn test_translate() {
        let dna = DNASequence::new("ATGGCTTAA").unwrap(); // M A Stop
        let protein = dna.translate();
        assert_eq!(protein.as_str(), "MA");
    }
    
    #[test]
    fn test_hamming_distance() {
        let dna1 = DNASequence::new("ATGC").unwrap();
        let dna2 = DNASequence::new("ATGG").unwrap();
        assert_eq!(dna1.hamming_distance(&dna2).unwrap(), 1);
        
        let dna3 = DNASequence::new("AAAA").unwrap();
        assert_eq!(dna1.hamming_distance(&dna3).unwrap(), 3);
    }
    
    #[test]
    fn test_find_pattern() {
        let dna = DNASequence::new("ATGCGATCGATGC").unwrap();
        let positions = dna.find_pattern("ATG");
        assert_eq!(positions, vec![0, 9]);
    }
    
    #[test]
    fn test_find_orfs() {
        let dna = DNASequence::new("ATGAAATAA").unwrap();
        let orfs = dna.find_orfs(0);
        assert!(!orfs.is_empty());
        assert_eq!(orfs[0].start, 0);
        assert_eq!(orfs[0].sequence, "ATGAAATAA");
    }
    
    #[test]
    fn test_melting_temperature() {
        let dna = DNASequence::new("ATGC").unwrap();
        let tm = dna.melting_temperature();
        assert!(tm > 0.0);
    }
    
    #[test]
    fn test_palindrome() {
        let dna = DNASequence::new("GAATTC").unwrap();
        assert!(dna.is_palindromic());
        
        let dna2 = DNASequence::new("GAATTA").unwrap();
        assert!(!dna2.is_palindromic());
    }
    
    #[test]
    fn test_protein_molecular_weight() {
        let protein = ProteinSequence::new("MFP").unwrap();
        let mw = protein.molecular_weight();
        assert!(mw > 0.0);
    }
    
    #[test]
    fn test_sequence_identity() {
        let dna1 = DNASequence::new("ATGC").unwrap();
        let dna2 = DNASequence::new("ATGC").unwrap();
        assert_eq!(sequence_identity(&dna1, &dna2).unwrap(), 100.0);
        
        let dna3 = DNASequence::new("ATGG").unwrap();
        assert_eq!(sequence_identity(&dna1, &dna3).unwrap(), 75.0);
    }
    
    #[test]
    fn test_consensus() {
        let seqs = vec![
            DNASequence::new("ATGC").unwrap(),
            DNASequence::new("ATGC").unwrap(),
            DNASequence::new("ATGC").unwrap(),
        ];
        let consensus = consensus_sequence(&seqs).unwrap();
        assert_eq!(consensus.as_str(), "ATGC");
    }
    
    #[test]
    fn test_fasta_parsing() {
        let fasta = ">seq1\nATGC\n>seq2\nGCTA";
        let parsed = parse_fasta(fasta);
        assert_eq!(parsed.len(), 2);
        assert_eq!(parsed[0], ("seq1".to_string(), "ATGC".to_string()));
        assert_eq!(parsed[1], ("seq2".to_string(), "GCTA".to_string()));
    }
    
    #[test]
    fn test_rna_creation() {
        let rna = RNASequence::new("AUGC").unwrap();
        assert_eq!(rna.len(), 4);
        assert_eq!(rna.as_str(), "AUGC");
    }
    
    #[test]
    fn test_reverse_transcribe() {
        let rna = RNASequence::new("AUGC").unwrap();
        let dna = rna.reverse_transcribe();
        assert_eq!(dna.as_str(), "ATGC");
    }
    
    #[test]
    fn test_nucleotide_counts() {
        let dna = DNASequence::new("AATTGGCC").unwrap();
        let counts = dna.nucleotide_counts();
        assert_eq!(*counts.get(&'A').unwrap_or(&0), 2);
        assert_eq!(*counts.get(&'T').unwrap_or(&0), 2);
        assert_eq!(*counts.get(&'G').unwrap_or(&0), 2);
        assert_eq!(*counts.get(&'C').unwrap_or(&0), 2);
    }
    
    #[test]
    fn test_complexity() {
        let dna1 = DNASequence::new("AAAA").unwrap();
        let dna2 = DNASequence::new("ATGC").unwrap();
        assert!(dna2.complexity() > dna1.complexity());
    }
}
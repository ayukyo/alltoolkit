//! Diff Utils 使用示例
//! 
//! 运行方式: rustc --edition 2021 basic.rs -o basic && ./basic

// 直接包含模块
mod diff_utils {
    use std::fmt;

    /// 差异操作类型
    #[derive(Debug, Clone, Copy, PartialEq, Eq)]
    pub enum DiffOp {
        Equal,
        Insert,
        Delete,
    }

    /// 单个差异块
    #[derive(Debug, Clone)]
    pub struct DiffItem {
        pub op: DiffOp,
        pub content: String,
        pub old_line: Option<usize>,
        pub new_line: Option<usize>,
    }

    /// 差异结果
    #[derive(Debug, Clone)]
    pub struct DiffResult {
        pub items: Vec<DiffItem>,
        pub stats: DiffStats,
    }

    /// 差异统计信息
    #[derive(Debug, Clone, Default)]
    pub struct DiffStats {
        pub equal: usize,
        pub insertions: usize,
        pub deletions: usize,
    }

    impl DiffStats {
        pub fn total_changes(&self) -> usize {
            self.insertions + self.deletions
        }

        pub fn has_changes(&self) -> bool {
            self.total_changes() > 0
        }
    }

    /// 输出格式
    #[derive(Debug, Clone, Copy)]
    pub enum DiffFormat {
        Unified,
        Compact,
        Plain,
    }

    /// ANSI 颜色代码
    struct AnsiColor;
    impl AnsiColor {
        const RESET: &'static str = "\x1b[0m";
        const RED: &'static str = "\x1b[31m";
        const GREEN: &'static str = "\x1b[32m";
        const CYAN: &'static str = "\x1b[36m";
    }

    /// 差异比较引擎
    pub struct DiffEngine {
        ignore_whitespace: bool,
        ignore_case: bool,
    }

    impl Default for DiffEngine {
        fn default() -> Self {
            Self::new()
        }
    }

    impl DiffEngine {
        pub fn new() -> Self {
            Self { ignore_whitespace: false, ignore_case: false }
        }

        pub fn ignore_whitespace(mut self, ignore: bool) -> Self {
            self.ignore_whitespace = ignore;
            self
        }

        pub fn ignore_case(mut self, ignore: bool) -> Self {
            self.ignore_case = ignore;
            self
        }

        fn normalize(&self, text: &str) -> String {
            let mut result = text.to_string();
            if self.ignore_case {
                result = result.to_lowercase();
            }
            if self.ignore_whitespace {
                result = result.split_whitespace().collect::<Vec<_>>().join(" ");
            }
            result
        }

        pub fn diff_lines(&self, old_text: &str, new_text: &str) -> DiffResult {
            let old_lines: Vec<&str> = old_text.lines().collect();
            let new_lines: Vec<&str> = new_text.lines().collect();
            self.diff_sequences(&old_lines, &new_lines)
        }

        pub fn diff_chars(&self, old_text: &str, new_text: &str) -> DiffResult {
            let old_chars: Vec<char> = old_text.chars().collect();
            let new_chars: Vec<char> = new_text.chars().collect();
            self.diff_sequences(&old_chars, &new_chars)
        }

        pub fn diff_words(&self, old_text: &str, new_text: &str) -> DiffResult {
            let old_words: Vec<&str> = old_text.split_whitespace().collect();
            let new_words: Vec<&str> = new_text.split_whitespace().collect();
            self.diff_sequences(&old_words, &new_words)
        }

        fn diff_sequences<T>(&self, old: &[T], new: &[T]) -> DiffResult 
        where T: std::fmt::Display
        {
            let old_norm: Vec<String> = old.iter().map(|x| self.normalize(&x.to_string())).collect();
            let new_norm: Vec<String> = new.iter().map(|x| self.normalize(&x.to_string())).collect();
            
            let lcs = self.compute_lcs(&old_norm, &new_norm);
            
            let mut items = Vec::new();
            let mut stats = DiffStats::default();
            
            let mut old_idx = 0usize;
            let mut new_idx = 0usize;
            let mut lcs_idx = 0usize;
            
            let mut old_line_num = 1usize;
            let mut new_line_num = 1usize;
            
            while old_idx < old.len() || new_idx < new.len() {
                if lcs_idx < lcs.len() {
                    let lcs_item = &lcs[lcs_idx];
                    
                    while old_idx < old.len() && old_norm[old_idx] != *lcs_item {
                        items.push(DiffItem {
                            op: DiffOp::Delete,
                            content: old[old_idx].to_string(),
                            old_line: Some(old_line_num),
                            new_line: None,
                        });
                        stats.deletions += 1;
                        old_idx += 1;
                        old_line_num += 1;
                    }
                    
                    while new_idx < new.len() && new_norm[new_idx] != *lcs_item {
                        items.push(DiffItem {
                            op: DiffOp::Insert,
                            content: new[new_idx].to_string(),
                            old_line: None,
                            new_line: Some(new_line_num),
                        });
                        stats.insertions += 1;
                        new_idx += 1;
                        new_line_num += 1;
                    }
                    
                    if old_idx < old.len() && new_idx < new.len() {
                        items.push(DiffItem {
                            op: DiffOp::Equal,
                            content: old[old_idx].to_string(),
                            old_line: Some(old_line_num),
                            new_line: Some(new_line_num),
                        });
                        stats.equal += 1;
                        old_idx += 1;
                        new_idx += 1;
                        old_line_num += 1;
                        new_line_num += 1;
                        lcs_idx += 1;
                    }
                } else {
                    while old_idx < old.len() {
                        items.push(DiffItem {
                            op: DiffOp::Delete,
                            content: old[old_idx].to_string(),
                            old_line: Some(old_line_num),
                            new_line: None,
                        });
                        stats.deletions += 1;
                        old_idx += 1;
                        old_line_num += 1;
                    }
                    
                    while new_idx < new.len() {
                        items.push(DiffItem {
                            op: DiffOp::Insert,
                            content: new[new_idx].to_string(),
                            old_line: None,
                            new_line: Some(new_line_num),
                        });
                        stats.insertions += 1;
                        new_idx += 1;
                        new_line_num += 1;
                    }
                }
            }
            
            DiffResult { items, stats }
        }

        fn compute_lcs(&self, old: &[String], new: &[String]) -> Vec<String> {
            let m = old.len();
            let n = new.len();
            
            let mut dp = vec![vec![0usize; n + 1]; m + 1];
            
            for i in 1..=m {
                for j in 1..=n {
                    if old[i - 1] == new[j - 1] {
                        dp[i][j] = dp[i - 1][j - 1] + 1;
                    } else {
                        dp[i][j] = dp[i - 1][j].max(dp[i][j - 1]);
                    }
                }
            }
            
            let mut lcs = Vec::new();
            let mut i = m;
            let mut j = n;
            
            while i > 0 && j > 0 {
                if old[i - 1] == new[j - 1] {
                    lcs.push(old[i - 1].clone());
                    i -= 1;
                    j -= 1;
                } else if dp[i - 1][j] > dp[i][j - 1] {
                    i -= 1;
                } else {
                    j -= 1;
                }
            }
            
            lcs.reverse();
            lcs
        }
    }

    impl DiffResult {
        pub fn format(&self, format: DiffFormat) -> String {
            match format {
                DiffFormat::Unified => self.format_unified(),
                DiffFormat::Compact => self.format_compact(),
                DiffFormat::Plain => self.format_plain(),
            }
        }

        fn format_unified(&self) -> String {
            let mut output = String::new();
            for item in &self.items {
                match item.op {
                    DiffOp::Equal => output.push_str(&format!("  {}\n", item.content)),
                    DiffOp::Delete => output.push_str(&format!(
                        "{}-{}{}\n", AnsiColor::RED, item.content, AnsiColor::RESET
                    )),
                    DiffOp::Insert => output.push_str(&format!(
                        "{}+{}{}\n", AnsiColor::GREEN, item.content, AnsiColor::RESET
                    )),
                }
            }
            output
        }

        fn format_compact(&self) -> String {
            let mut output = String::new();
            for item in &self.items {
                if item.op == DiffOp::Equal { continue; }
                match item.op {
                    DiffOp::Delete => output.push_str(&format!(
                        "{}[- {}]{} ", AnsiColor::RED, item.content, AnsiColor::RESET
                    )),
                    DiffOp::Insert => output.push_str(&format!(
                        "{}[+ {}]{} ", AnsiColor::GREEN, item.content, AnsiColor::RESET
                    )),
                    _ => {}
                }
            }
            output.push('\n');
            output
        }

        fn format_plain(&self) -> String {
            let mut output = String::new();
            for item in &self.items {
                match item.op {
                    DiffOp::Equal => output.push_str(&format!("  {}\n", item.content)),
                    DiffOp::Delete => output.push_str(&format!("- {}\n", item.content)),
                    DiffOp::Insert => output.push_str(&format!("+ {}\n", item.content)),
                }
            }
            output
        }
    }

    pub struct TextDiff;
    impl TextDiff {
        pub fn quick_diff(old: &str, new: &str) -> DiffResult {
            DiffEngine::new().diff_lines(old, new)
        }

        pub fn similarity(old: &str, new: &str) -> f64 {
            let result = DiffEngine::new().diff_lines(old, new);
            let total = result.stats.equal + result.stats.insertions + result.stats.deletions;
            if total == 0 { return 1.0; }
            result.stats.equal as f64 / total as f64
        }

        pub fn summary(old: &str, new: &str) -> String {
            let result = Self::quick_diff(old, new);
            if !result.stats.has_changes() {
                return "文件内容相同".to_string();
            }
            format!(
                "共 {} 处变化: +{} -{}",
                result.stats.total_changes(),
                result.stats.insertions,
                result.stats.deletions
            )
        }
    }

    pub struct StringDistance;
    impl StringDistance {
        pub fn levenshtein(a: &str, b: &str) -> usize {
            let a_chars: Vec<char> = a.chars().collect();
            let b_chars: Vec<char> = b.chars().collect();
            let m = a_chars.len();
            let n = b_chars.len();
            
            if m == 0 { return n; }
            if n == 0 { return m; }
            
            let mut dp = vec![vec![0; n + 1]; m + 1];
            
            for i in 0..=m { dp[i][0] = i; }
            for j in 0..=n { dp[0][j] = j; }
            
            for i in 1..=m {
                for j in 1..=n {
                    let cost = if a_chars[i - 1] == b_chars[j - 1] { 0 } else { 1 };
                    dp[i][j] = dp[i - 1][j].min(dp[i][j - 1] + 1).min(dp[i - 1][j - 1] + cost);
                }
            }
            
            dp[m][n]
        }

        pub fn similarity(a: &str, b: &str) -> f64 {
            let distance = Self::levenshtein(a, b);
            let max_len = a.len().max(b.len());
            if max_len == 0 { return 1.0; }
            1.0 - (distance as f64 / max_len as f64)
        }
    }
}

use diff_utils::{DiffEngine, DiffFormat, TextDiff, StringDistance};

fn main() {
    println!("=== Diff Utils 示例 ===\n");
    
    // 示例 1: 基本的行级别比较
    println!("【示例 1】基本行级别比较：");
    let old_text = "Hello World\nThis is a test\nGoodbye";
    let new_text = "Hello Rust\nThis is a test\nSee you later";
    
    let engine = DiffEngine::new();
    let diff = engine.diff_lines(old_text, new_text);
    
    println!("{}", diff.format(DiffFormat::Unified));
    println!("统计: +{} -{} 相同: {}\n", 
        diff.stats.insertions, 
        diff.stats.deletions, 
        diff.stats.equal
    );
    
    // 示例 2: 简洁格式
    println!("【示例 2】简洁格式（只显示变化）：");
    println!("{}", diff.format(DiffFormat::Compact));
    
    // 示例 3: 字符级别比较
    println!("【示例 3】字符级别比较：");
    let old_word = "kitten";
    let new_word = "sitting";
    let char_diff = engine.diff_chars(old_word, new_word);
    println!("比较 '{}' vs '{}':", old_word, new_word);
    println!("{}", char_diff.format(DiffFormat::Compact));
    
    // 示例 4: 使用 TextDiff 工具函数
    println!("【示例 4】快速比较工具：");
    let text1 = "The quick brown fox";
    let text2 = "The lazy brown dog";
    
    let similarity = TextDiff::similarity(text1, text2);
    println!("相似度: {:.2}%", similarity * 100.0);
    
    let summary = TextDiff::summary(text1, text2);
    println!("摘要: {}", summary);
    
    // 示例 5: 忽略大小写比较
    println!("【示例 5】忽略大小写比较：");
    let text_a = "Hello World";
    let text_b = "hello world";
    
    let normal_diff = DiffEngine::new().diff_lines(text_a, text_b);
    let ignore_case_diff = DiffEngine::new().ignore_case(true).diff_lines(text_a, text_b);
    
    println!("普通比较: +{} -{}", normal_diff.stats.insertions, normal_diff.stats.deletions);
    println!("忽略大小写: +{} -{}", ignore_case_diff.stats.insertions, ignore_case_diff.stats.deletions);
    
    // 示例 6: Levenshtein 编辑距离
    println!("\n【示例 6】Levenshtein 编辑距离：");
    let pairs = [
        ("kitten", "sitting"),
        ("book", "back"),
        ("hello", "hallo"),
        ("", "test"),
    ];
    
    for (a, b) in pairs {
        let distance = StringDistance::levenshtein(a, b);
        let sim = StringDistance::similarity(a, b);
        println!("'{}' -> '{}' : 距离={}, 相似度={:.2}%", a, b, distance, sim * 100.0);
    }
    
    // 示例 7: 单词级别比较
    println!("\n【示例 7】单词级别比较：");
    let sentence1 = "The quick brown fox jumps over the lazy dog";
    let sentence2 = "The fast brown cat leaps over the tired dog";
    let word_diff = engine.diff_words(sentence1, sentence2);
    println!("{}", word_diff.format(DiffFormat::Compact));
    
    println!("\n=== 示例完成 ===");
}
//! # Diff Utils - 文本差异比较工具
//!
//! 一个零外部依赖的文本差异比较库，实现 LCS（最长公共子序列）算法。
//!
//! ## 功能特性
//! - 行级别和字符级别的差异比较
//! - 支持彩色输出（ANSI 颜色）
//! - 统一差异格式（Unified Diff）
//! - 并排对比格式
//! - 差异统计信息
//!
//! ## 示例
//! ```rust
//! use diff_utils::{DiffEngine, DiffFormat};
//!
//! let old_text = "Hello World\nFoo Bar";
//! let new_text = "Hello Rust\nFoo Baz";
//! 
//! let engine = DiffEngine::new();
//! let diff = engine.diff_lines(old_text, new_text);
//! 
//! println!("{}", diff.format(DiffFormat::Unified));
//! ```

use std::fmt;

/// 差异操作类型
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum DiffOp {
    /// 保持不变
    Equal,
    /// 新增
    Insert,
    /// 删除
    Delete,
}

/// 单个差异块
#[derive(Debug, Clone)]
pub struct DiffItem {
    /// 操作类型
    pub op: DiffOp,
    /// 内容
    pub content: String,
    /// 原始行号（对于 Equal 和 Delete）
    pub old_line: Option<usize>,
    /// 新行号（对于 Equal 和 Insert）
    pub new_line: Option<usize>,
}

/// 差异结果
#[derive(Debug, Clone)]
pub struct DiffResult {
    /// 差异项列表
    pub items: Vec<DiffItem>,
    /// 统计信息
    pub stats: DiffStats,
}

/// 差异统计信息
#[derive(Debug, Clone, Default)]
pub struct DiffStats {
    /// 相同行数
    pub equal: usize,
    /// 新增行数
    pub insertions: usize,
    /// 删除行数
    pub deletions: usize,
}

impl DiffStats {
    /// 总变化行数
    pub fn total_changes(&self) -> usize {
        self.insertions + self.deletions
    }

    /// 是否有变化
    pub fn has_changes(&self) -> bool {
        self.total_changes() > 0
    }
}

/// 输出格式
#[derive(Debug, Clone, Copy)]
pub enum DiffFormat {
    /// 统一差异格式（类似 diff -u）
    Unified,
    /// 并排对比
    SideBySide,
    /// 简洁格式（只显示变化）
    Compact,
    /// 无颜色格式
    Plain,
}

/// ANSI 颜色代码
struct AnsiColor;

impl AnsiColor {
    const RESET: &str = "\x1b[0m";
    const RED: &str = "\x1b[31m";
    const GREEN: &str = "\x1b[32m";
    const CYAN: &str = "\x1b[36m";
    const DIM: &str = "\x1b[2m";
    const BOLD: &str = "\x1b[1m";
}

/// 差异比较引擎
pub struct DiffEngine {
    /// 是否忽略空白差异
    ignore_whitespace: bool,
    /// 是否忽略大小写
    ignore_case: bool,
}

impl Default for DiffEngine {
    fn default() -> Self {
        Self::new()
    }
}

impl DiffEngine {
    /// 创建新的差异引擎
    pub fn new() -> Self {
        Self {
            ignore_whitespace: false,
            ignore_case: false,
        }
    }

    /// 设置是否忽略空白
    pub fn ignore_whitespace(mut self, ignore: bool) -> Self {
        self.ignore_whitespace = ignore;
        self
    }

    /// 设置是否忽略大小写
    pub fn ignore_case(mut self, ignore: bool) -> Self {
        self.ignore_case = ignore;
        self
    }

    /// 标准化文本用于比较
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

    /// 比较两个文本（行级别）
    pub fn diff_lines(&self, old_text: &str, new_text: &str) -> DiffResult {
        let old_lines: Vec<&str> = old_text.lines().collect();
        let new_lines: Vec<&str> = new_text.lines().collect();
        
        self.diff_sequences(&old_lines, &new_lines)
    }

    /// 比较两个文本（字符级别）
    pub fn diff_chars(&self, old_text: &str, new_text: &str) -> DiffResult {
        let old_chars: Vec<char> = old_text.chars().collect();
        let new_chars: Vec<char> = new_text.chars().collect();
        
        self.diff_sequences(&old_chars, &new_chars)
    }

    /// 比较两个单词序列
    pub fn diff_words(&self, old_text: &str, new_text: &str) -> DiffResult {
        let old_words: Vec<&str> = old_text.split_whitespace().collect();
        let new_words: Vec<&str> = new_text.split_whitespace().collect();
        
        self.diff_sequences(&old_words, &new_words)
    }

    /// 通用序列比较（使用 LCS 算法）
    fn diff_sequences<T>(&self, old: &[T], new: &[T]) -> DiffResult 
    where
        T: std::fmt::Display,
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
                
                // 处理删除
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
                
                // 处理新增
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
                
                // 处理相等
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
                // 处理剩余的删除
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
                
                // 处理剩余的新增
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

    /// 计算最长公共子序列（LCS）
    fn compute_lcs(&self, old: &[String], new: &[String]) -> Vec<String> {
        let m = old.len();
        let n = new.len();
        
        // 构建 DP 表
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
        
        // 回溯获取 LCS
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
    /// 格式化输出差异
    pub fn format(&self, format: DiffFormat) -> String {
        match format {
            DiffFormat::Unified => self.format_unified(),
            DiffFormat::SideBySide => self.format_side_by_side(),
            DiffFormat::Compact => self.format_compact(),
            DiffFormat::Plain => self.format_plain(),
        }
    }

    /// 统一差异格式
    fn format_unified(&self) -> String {
        let mut output = String::new();
        
        for item in &self.items {
            match item.op {
                DiffOp::Equal => {
                    output.push_str(&format!("  {}\n", item.content));
                }
                DiffOp::Delete => {
                    output.push_str(&format!(
                        "{}-{}{}\n",
                        AnsiColor::RED,
                        item.content,
                        AnsiColor::RESET
                    ));
                }
                DiffOp::Insert => {
                    output.push_str(&format!(
                        "{}+{}{}\n",
                        AnsiColor::GREEN,
                        item.content,
                        AnsiColor::RESET
                    ));
                }
            }
        }
        
        output
    }

    /// 并排对比格式
    fn format_side_by_side(&self) -> String {
        let width = 40;
        let mut output = String::new();
        
        output.push_str(&format!(
            "{}{:<width$} | {}{}\n",
            AnsiColor::DIM,
            "旧文本",
            "新文本",
            AnsiColor::RESET,
            width = width
        ));
        output.push_str(&format!("{}{}\n", "─".repeat(width * 2 + 3), AnsiColor::RESET));
        
        let mut i = 0;
        while i < self.items.len() {
            let item = &self.items[i];
            
            match item.op {
                DiffOp::Equal => {
                    output.push_str(&format!(
                        "{:<width$} | {}\n",
                        item.content,
                        item.content,
                        width = width
                    ));
                }
                DiffOp::Delete => {
                    // 查找对应的新增
                    let next = if i + 1 < self.items.len() {
                        &self.items[i + 1]
                    } else {
                        &DiffItem {
                            op: DiffOp::Equal,
                            content: String::new(),
                            old_line: None,
                            new_line: None,
                        }
                    };
                    
                    if next.op == DiffOp::Insert {
                        // 显示为修改
                        output.push_str(&format!(
                            "{}-{:<width$}{} | {}+{}{}\n",
                            AnsiColor::RED,
                            item.content,
                            AnsiColor::RESET,
                            AnsiColor::GREEN,
                            next.content,
                            AnsiColor::RESET,
                            width = width - 1
                        ));
                        i += 1;
                    } else {
                        output.push_str(&format!(
                            "{}-{:<width$}{} | \n",
                            AnsiColor::RED,
                            item.content,
                            AnsiColor::RESET,
                            width = width - 1
                        ));
                    }
                }
                DiffOp::Insert => {
                    output.push_str(&format!(
                        "{:<width$} | {}+{}{}\n",
                        "",
                        AnsiColor::GREEN,
                        item.content,
                        AnsiColor::RESET,
                        width = width
                    ));
                }
            }
            i += 1;
        }
        
        output
    }

    /// 简洁格式（只显示变化）
    fn format_compact(&self) -> String {
        let mut output = String::new();
        
        for item in &self.items {
            if item.op == DiffOp::Equal {
                continue;
            }
            
            match item.op {
                DiffOp::Delete => {
                    output.push_str(&format!(
                        "{}[- {}]{} ",
                        AnsiColor::RED,
                        item.content,
                        AnsiColor::RESET
                    ));
                }
                DiffOp::Insert => {
                    output.push_str(&format!(
                        "{}[+ {}]{} ",
                        AnsiColor::GREEN,
                        item.content,
                        AnsiColor::RESET
                    ));
                }
                _ => {}
            }
        }
        
        output.push('\n');
        output
    }

    /// 无颜色格式
    fn format_plain(&self) -> String {
        let mut output = String::new();
        
        for item in &self.items {
            match item.op {
                DiffOp::Equal => {
                    output.push_str(&format!("  {}\n", item.content));
                }
                DiffOp::Delete => {
                    output.push_str(&format!("- {}\n", item.content));
                }
                DiffOp::Insert => {
                    output.push_str(&format!("+ {}\n", item.content));
                }
            }
        }
        
        output
    }
}

impl fmt::Display for DiffResult {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        writeln!(f, "{}", self.format(DiffFormat::Unified))?;
        writeln!(
            f,
            "{}统计: {} 行相同, {} 行新增, {} 行删除{}",
            AnsiColor::CYAN,
            self.stats.equal,
            self.stats.insertions,
            self.stats.deletions,
            AnsiColor::RESET
        )
    }
}

/// 文本比较工具函数
pub struct TextDiff;

impl TextDiff {
    /// 快速比较两个字符串
    pub fn quick_diff(old: &str, new: &str) -> DiffResult {
        DiffEngine::new().diff_lines(old, new)
    }

    /// 检查两个字符串是否相同
    pub fn is_equal(old: &str, new: &str) -> bool {
        old == new
    }

    /// 计算相似度（0.0 - 1.0）
    pub fn similarity(old: &str, new: &str) -> f64 {
        let engine = DiffEngine::new();
        let result = engine.diff_lines(old, new);
        
        let total = result.stats.equal + result.stats.insertions + result.stats.deletions;
        if total == 0 {
            return 1.0;
        }
        
        result.stats.equal as f64 / total as f64
    }

    /// 获取变化摘要
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

    /// 生成统一差异格式的 patch
    pub fn unified_diff(old: &str, new: &str, old_name: &str, new_name: &str) -> String {
        let mut output = String::new();
        
        output.push_str(&format!("--- {}\n", old_name));
        output.push_str(&format!("+++ {}\n", new_name));
        
        let engine = DiffEngine::new();
        let result = engine.diff_lines(old, new);
        
        // 找到变化的范围
        let mut hunks: Vec<(usize, usize, Vec<&DiffItem>)> = Vec::new();
        let mut current_hunk: Vec<&DiffItem> = Vec::new();
        let mut hunk_start = 0;
        
        for (i, item) in result.items.iter().enumerate() {
            if item.op != DiffOp::Equal {
                if current_hunk.is_empty() {
                    hunk_start = i.saturating_sub(3);
                }
                current_hunk.push(item);
            } else if !current_hunk.is_empty() {
                // 添加上下文
                current_hunk.push(item);
                if current_hunk.len() > 6 {
                    hunks.push((hunk_start, i, current_hunk.clone()));
                    current_hunk.clear();
                }
            }
        }
        
        if !current_hunk.is_empty() {
            hunks.push((hunk_start, result.items.len(), current_hunk));
        }
        
        for (_, _, hunk) in hunks {
            let old_count = hunk.iter().filter(|i| i.op != DiffOp::Insert).count();
            let new_count = hunk.iter().filter(|i| i.op != DiffOp::Delete).count();
            
            output.push_str(&format!("@@ -1,{} +1,{} @@\n", old_count, new_count));
            
            for item in hunk {
                match item.op {
                    DiffOp::Equal => output.push_str(&format!(" {}\n", item.content)),
                    DiffOp::Delete => output.push_str(&format!("-{}\n", item.content)),
                    DiffOp::Insert => output.push_str(&format!("+{}\n", item.content)),
                }
            }
        }
        
        output
    }
}

/// 字符串距离计算
pub struct StringDistance;

impl StringDistance {
    /// 计算 Levenshtein 编辑距离
    pub fn levenshtein(a: &str, b: &str) -> usize {
        let a_chars: Vec<char> = a.chars().collect();
        let b_chars: Vec<char> = b.chars().collect();
        
        let m = a_chars.len();
        let n = b_chars.len();
        
        if m == 0 {
            return n;
        }
        if n == 0 {
            return m;
        }
        
        let mut dp = vec![vec![0; n + 1]; m + 1];
        
        for i in 0..=m {
            dp[i][0] = i;
        }
        for j in 0..=n {
            dp[0][j] = j;
        }
        
        for i in 1..=m {
            for j in 1..=n {
                let cost = if a_chars[i - 1] == b_chars[j - 1] { 0 } else { 1 };
                dp[i][j] = dp[i - 1][j]  // 删除
                    .min(dp[i][j - 1] + 1)  // 插入
                    .min(dp[i - 1][j - 1] + cost);  // 替换
            }
        }
        
        dp[m][n]
    }

    /// 计算相似度（基于 Levenshtein 距离）
    pub fn similarity(a: &str, b: &str) -> f64 {
        let distance = Self::levenshtein(a, b);
        let max_len = a.len().max(b.len());
        
        if max_len == 0 {
            return 1.0;
        }
        
        1.0 - (distance as f64 / max_len as f64)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_diff_equal() {
        let old = "Hello\nWorld";
        let new = "Hello\nWorld";
        
        let engine = DiffEngine::new();
        let result = engine.diff_lines(old, new);
        
        assert_eq!(result.stats.equal, 2);
        assert_eq!(result.stats.insertions, 0);
        assert_eq!(result.stats.deletions, 0);
        assert!(!result.stats.has_changes());
    }

    #[test]
    fn test_diff_insert() {
        let old = "Hello";
        let new = "Hello\nWorld";
        
        let engine = DiffEngine::new();
        let result = engine.diff_lines(old, new);
        
        assert_eq!(result.stats.equal, 1);
        assert_eq!(result.stats.insertions, 1);
        assert_eq!(result.stats.deletions, 0);
    }

    #[test]
    fn test_diff_delete() {
        let old = "Hello\nWorld";
        let new = "Hello";
        
        let engine = DiffEngine::new();
        let result = engine.diff_lines(old, new);
        
        assert_eq!(result.stats.equal, 1);
        assert_eq!(result.stats.insertions, 0);
        assert_eq!(result.stats.deletions, 1);
    }

    #[test]
    fn test_diff_modify() {
        let old = "Hello World";
        let new = "Hello Rust";
        
        let engine = DiffEngine::new();
        let result = engine.diff_lines(old, new);
        
        assert_eq!(result.stats.insertions, 1);
        assert_eq!(result.stats.deletions, 1);
    }

    #[test]
    fn test_diff_complex() {
        let old = "line1\nline2\nline3\nline4";
        let new = "line1\nline2modified\nline3\nline5";
        
        let engine = DiffEngine::new();
        let result = engine.diff_lines(old, new);
        
        assert!(result.stats.has_changes());
    }

    #[test]
    fn test_similarity() {
        let result = TextDiff::similarity("Hello World", "Hello Rust");
        // 相似度范围 [0.0, 1.0]，部分匹配应该在中间值
        assert!(result >= 0.0 && result <= 1.0);
        
        let result = TextDiff::similarity("Hello", "Hello");
        assert_eq!(result, 1.0);
    }

    #[test]
    fn test_levenshtein() {
        assert_eq!(StringDistance::levenshtein("kitten", "sitting"), 3);
        assert_eq!(StringDistance::levenshtein("", "hello"), 5);
        assert_eq!(StringDistance::levenshtein("hello", ""), 5);
        assert_eq!(StringDistance::levenshtein("same", "same"), 0);
    }

    #[test]
    fn test_diff_chars() {
        let old = "Hello";
        let new = "Hella";
        
        let engine = DiffEngine::new();
        let result = engine.diff_chars(old, new);
        
        assert!(result.stats.has_changes());
    }

    #[test]
    fn test_ignore_case() {
        let old = "Hello World";
        let new = "hello world";
        
        let engine = DiffEngine::new().ignore_case(true);
        let result = engine.diff_lines(old, new);
        
        assert_eq!(result.stats.equal, 1);
        assert_eq!(result.stats.insertions, 0);
        assert_eq!(result.stats.deletions, 0);
    }

    #[test]
    fn test_summary() {
        let old = "Hello\nWorld";
        let new = "Hello\nRust";
        
        let summary = TextDiff::summary(old, new);
        assert!(summary.contains("变化"));
    }

    #[test]
    fn test_format_plain() {
        let old = "Hello";
        let new = "Rust";
        
        let engine = DiffEngine::new();
        let result = engine.diff_lines(old, new);
        
        let plain = result.format(DiffFormat::Plain);
        assert!(plain.contains("- Hello"));
        assert!(plain.contains("+ Rust"));
    }
}
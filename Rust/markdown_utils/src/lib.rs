//! Markdown 文本处理工具模块
//! 
//! 提供零外部依赖的 Markdown 解析和处理功能：
//! - 解析标题结构
//! - 提取链接和图片
//! - 自动生成目录
//! - 格式化代码块
//! - 统计字数和阅读时间
//!
//! # 示例
//! ```
//! use markdown_utils::{MarkdownParser, Heading, Link, Stats};
//! 
//! let md = "# Hello\n## World\n[link](https://example.com)";
//! let parser = MarkdownParser::new(md);
//! let headings = parser.extract_headings();
//! let links = parser.extract_links();
//! let stats = parser.calculate_stats();
//! ```

// No external dependencies needed

/// Markdown 标题
#[derive(Debug, Clone, PartialEq)]
pub struct Heading {
    /// 标题级别 (1-6)
    pub level: usize,
    /// 标题文本
    pub text: String,
    /// 标题锚点 ID
    pub anchor: String,
    /// 在文档中的行号
    pub line_number: usize,
}

/// Markdown 链接
#[derive(Debug, Clone, PartialEq)]
pub struct Link {
    /// 链接文本
    pub text: String,
    /// 链接 URL
    pub url: String,
    /// 链接标题（可选）
    pub title: Option<String>,
    /// 是否为图片链接
    pub is_image: bool,
    /// 在文档中的行号
    pub line_number: usize,
}

/// 代码块信息
#[derive(Debug, Clone, PartialEq)]
pub struct CodeBlock {
    /// 语言标识符
    pub language: Option<String>,
    /// 代码内容
    pub code: String,
    /// 在文档中的行号范围
    pub start_line: usize,
    pub end_line: usize,
}

/// 文档统计信息
#[derive(Debug, Clone, PartialEq)]
pub struct Stats {
    /// 总字符数
    pub characters: usize,
    /// 总单词数（按空格分隔，适用于英文）
    pub words: usize,
    /// 总行数
    pub lines: usize,
    /// 中文字符数
    pub chinese_chars: usize,
    /// 预估阅读时间（分钟）
    pub reading_time_minutes: usize,
    /// 标题数量
    pub heading_count: usize,
    /// 链接数量
    pub link_count: usize,
    /// 图片数量
    pub image_count: usize,
    /// 代码块数量
    pub code_block_count: usize,
}

/// 列表项
#[derive(Debug, Clone, PartialEq)]
pub struct ListItem {
    /// 列表项文本
    pub text: String,
    /// 缩进级别
    pub indent: usize,
    /// 是否为有序列表项
    pub ordered: bool,
    /// 序号（有序列表）
    pub number: Option<usize>,
    /// 在文档中的行号
    pub line_number: usize,
}

/// Markdown 解析器
pub struct MarkdownParser<'a> {
    content: &'a str,
    lines: Vec<&'a str>,
}

impl<'a> MarkdownParser<'a> {
    /// 创建新的 Markdown 解析器
    pub fn new(content: &'a str) -> Self {
        Self {
            content,
            lines: content.lines().collect(),
        }
    }

    /// 提取所有标题
    pub fn extract_headings(&self) -> Vec<Heading> {
        let mut headings = Vec::new();
        
        for (idx, line) in self.lines.iter().enumerate() {
            let trimmed = line.trim_start();
            
            // ATX 风格标题 (# 开头)
            if trimmed.starts_with('#') {
                let hash_count = trimmed.chars().take_while(|&c| c == '#').count();
                if hash_count >= 1 && hash_count <= 6 {
                    let text = trimmed[hash_count..].trim_start().to_string();
                    let anchor = generate_anchor(&text);
                    headings.push(Heading {
                        level: hash_count,
                        text,
                        anchor,
                        line_number: idx + 1,
                    });
                }
            }
            
            // Setext 风格标题 (下划线)
            if idx > 0 {
                let prev_line = self.lines[idx - 1].trim();
                if !prev_line.is_empty() {
                    if trimmed.chars().all(|c| c == '=') && !trimmed.is_empty() {
                        headings.push(Heading {
                            level: 1,
                            text: prev_line.to_string(),
                            anchor: generate_anchor(prev_line),
                            line_number: idx,
                        });
                    } else if trimmed.chars().all(|c| c == '-') && !trimmed.is_empty() {
                        headings.push(Heading {
                            level: 2,
                            text: prev_line.to_string(),
                            anchor: generate_anchor(prev_line),
                            line_number: idx,
                        });
                    }
                }
            }
        }
        
        headings
    }

    /// 提取所有链接和图片
    pub fn extract_links(&self) -> Vec<Link> {
        let mut links = Vec::new();
        
        for (idx, line) in self.lines.iter().enumerate() {
            // 行内链接: [text](url) 或 ![alt](url)
            let chars: Vec<char> = line.chars().collect();
            let mut i = 0;
            
            while i < chars.len() {
                // 检查是否为图片 ![...](...)
                if i < chars.len() - 1 && chars[i] == '!' && chars[i + 1] == '[' {
                    if let Some(link) = Self::parse_inline_link_from_pos(&chars, i, idx + 1) {
                        let consumed = link.text.len() + link.url.len() + 6; // 估算长度
                        links.push(link);
                        i += consumed;
                        continue;
                    }
                }
                
                // 检查是否为普通链接 [...](...)
                if chars[i] == '[' {
                    if let Some(link) = Self::parse_inline_link_from_pos(&chars, i, idx + 1) {
                        let consumed = link.text.len() + link.url.len() + 4; // 估算长度
                        links.push(link);
                        i += consumed;
                        continue;
                    }
                }
                
                i += 1;
            }
        }
        
        // 处理引用式链接
        let refs = self.extract_reference_links();
        links.extend(refs);
        
        links
    }
    
    /// 从指定位置解析行内链接
    fn parse_inline_link_from_pos(chars: &[char], start: usize, line_number: usize) -> Option<Link> {
        let is_image = start < chars.len() - 1 && chars[start] == '!' && chars[start + 1] == '[';
        let actual_start = if is_image { start + 1 } else { start };
        
        if chars[actual_start] != '[' {
            return None;
        }
        
        // 找到 ] 确定文本
        let mut text_end = None;
        for i in (actual_start + 1)..chars.len() {
            if chars[i] == ']' {
                text_end = Some(i);
                break;
            }
        }
        let text_end = text_end?;
        
        let text: String = chars[actual_start + 1..text_end].iter().collect();
        
        // 检查后面是否有 (
        if text_end + 1 >= chars.len() || chars[text_end + 1] != '(' {
            return None;
        }
        
        // 找到 ) 确定 URL
        let mut url_end = None;
        for i in (text_end + 2)..chars.len() {
            if chars[i] == ')' {
                url_end = Some(i);
                break;
            }
        }
        let url_end = url_end?;
        
        let url_part: String = chars[text_end + 2..url_end].iter().collect();
        let (url, title) = parse_url_and_title(&url_part);
        
        Some(Link {
            text,
            url,
            title,
            is_image,
            line_number,
        })
    }

    /// 提取引用式链接定义
    fn extract_reference_links(&self) -> Vec<Link> {
        let mut links = Vec::new();
        let re_pattern = |s: &str| {
            // 简单匹配 [id]: url "title"
            let trimmed = s.trim();
            if !trimmed.starts_with('[') {
                return None;
            }
            let end_bracket = trimmed.find(']')?;
            let _id = &trimmed[1..end_bracket];
            let rest = trimmed[end_bracket + 1..].trim_start();
            if !rest.starts_with(':') {
                return None;
            }
            let url_part = rest[1..].trim_start();
            let url_end = url_part.find(|c: char| c.is_whitespace() || c == '"').unwrap_or(url_part.len());
            let url = url_part[..url_end].to_string();
            let title = if url_end < url_part.len() {
                let title_part = url_part[url_end..].trim();
                if title_part.starts_with('"') && title_part.ends_with('"') {
                    Some(title_part[1..title_part.len()-1].to_string())
                } else if title_part.starts_with('\'') && title_part.ends_with('\'') {
                    Some(title_part[1..title_part.len()-1].to_string())
                } else {
                    None
                }
            } else {
                None
            };
            Some(Link {
                text: String::new(),
                url,
                title,
                is_image: false,
                line_number: 0,
            })
        };
        
        for (idx, line) in self.lines.iter().enumerate() {
            if let Some(link) = re_pattern(line) {
                links.push(Link {
                    line_number: idx + 1,
                    ..link
                });
            }
        }
        
        links
    }

    /// 提取所有代码块
    pub fn extract_code_blocks(&self) -> Vec<CodeBlock> {
        let mut blocks = Vec::new();
        let mut in_code_block = false;
        let mut current_block = String::new();
        let mut language: Option<String> = None;
        let mut start_line = 0;
        
        for (idx, line) in self.lines.iter().enumerate() {
            if line.trim_start().starts_with("```") {
                if !in_code_block {
                    in_code_block = true;
                    start_line = idx + 1;
                    let lang = line.trim_start()[3..].trim();
                    language = if lang.is_empty() { None } else { Some(lang.to_string()) };
                    current_block.clear();
                } else {
                    blocks.push(CodeBlock {
                        language,
                        code: current_block.trim_end().to_string(),
                        start_line,
                        end_line: idx + 1,
                    });
                    in_code_block = false;
                    language = None;
                }
            } else if in_code_block {
                current_block.push_str(line);
                current_block.push('\n');
            }
        }
        
        blocks
    }

    /// 提取列表项
    pub fn extract_list_items(&self) -> Vec<ListItem> {
        let mut items = Vec::new();
        
        for (idx, line) in self.lines.iter().enumerate() {
            let trimmed = line.trim_start();
            let indent = line.len() - trimmed.len();
            let indent_level = indent / 2; // 假设每级缩进 2 空格
            
            // 无序列表: - * +
            if trimmed.starts_with("- ") || trimmed.starts_with("* ") || trimmed.starts_with("+ ") {
                let text = trimmed[2..].trim().to_string();
                items.push(ListItem {
                    text,
                    indent: indent_level,
                    ordered: false,
                    number: None,
                    line_number: idx + 1,
                });
            }
            
            // 有序列表: 1. 2. etc.
            if let Some(dot_pos) = trimmed.find(". ") {
                if dot_pos > 0 && dot_pos < 10 {
                    let num_str = &trimmed[..dot_pos];
                    if num_str.chars().all(|c| c.is_ascii_digit()) {
                        if let Ok(num) = num_str.parse::<usize>() {
                            let text = trimmed[dot_pos + 2..].trim().to_string();
                            items.push(ListItem {
                                text,
                                indent: indent_level,
                                ordered: true,
                                number: Some(num),
                                line_number: idx + 1,
                            });
                        }
                    }
                }
            }
        }
        
        items
    }

    /// 计算文档统计信息
    pub fn calculate_stats(&self) -> Stats {
        let characters = self.content.chars().count();
        let words = self.content.split_whitespace().count();
        let lines = self.lines.len();
        
        // 统计中文字符
        let chinese_chars = self.content.chars()
            .filter(|&c| matches!(c, '\u{4E00}'..='\u{9FFF}'))
            .count();
        
        // 预估阅读时间：中文约 400 字/分钟，英文约 200 词/分钟
        let reading_time = if chinese_chars > words {
            // 主要是中文内容
            (chinese_chars as f64 / 400.0).ceil() as usize
        } else {
            // 主要是英文内容
            (words as f64 / 200.0).ceil() as usize
        };
        
        let headings = self.extract_headings();
        let links = self.extract_links();
        let code_blocks = self.extract_code_blocks();
        
        Stats {
            characters,
            words,
            lines,
            chinese_chars,
            reading_time_minutes: reading_time.max(1),
            heading_count: headings.len(),
            link_count: links.iter().filter(|l| !l.is_image).count(),
            image_count: links.iter().filter(|l| l.is_image).count(),
            code_block_count: code_blocks.len(),
        }
    }

    /// 生成目录 (TOC)
    pub fn generate_toc(&self, max_level: usize) -> String {
        let headings = self.extract_headings();
        let mut toc = String::new();
        
        for heading in headings.iter().filter(|h| h.level <= max_level) {
            let indent = "  ".repeat(heading.level - 1);
            let anchor = &heading.anchor;
            toc.push_str(&format!("{}- [{}](#{})\n", indent, heading.text, anchor));
        }
        
        toc
    }

    /// 提取纯文本（移除所有 Markdown 格式）
    pub fn extract_plain_text(&self) -> String {
        let mut result = String::new();
        let mut in_code_block = false;
        
        for line in &self.lines {
            // 跳过代码块
            if line.trim_start().starts_with("```") {
                in_code_block = !in_code_block;
                continue;
            }
            if in_code_block {
                continue;
            }
            
            let mut cleaned = line.to_string();
            
            // 移除标题标记
            cleaned = remove_heading_markers(&cleaned);
            
            // 移除链接，保留文本
            cleaned = remove_link_syntax(&cleaned);
            
            // 移除图片，保留 alt 文本
            cleaned = remove_image_syntax(&cleaned);
            
            // 移除粗体和斜体
            cleaned = remove_emphasis(&cleaned);
            
            // 移除删除线
            while cleaned.contains("~~") {
                if let Some(start) = cleaned.find("~~") {
                    if let Some(end) = cleaned[start + 2..].find("~~") {
                        let text = &cleaned[start + 2..start + 2 + end];
                        cleaned = format!("{}{}{}", &cleaned[..start], text, &cleaned[start + 2 + end + 2..]);
                    } else {
                        break;
                    }
                }
            }
            
            // 移除行内代码
            cleaned = remove_inline_code(&cleaned);
            
            // 移除列表标记
            cleaned = remove_list_markers(&cleaned);
            
            // 移除引用标记
            cleaned = remove_blockquote_markers(&cleaned);
            
            result.push_str(&cleaned);
            result.push('\n');
        }
        
        result.trim().to_string()
    }

    /// 查找所有标题并返回层级结构
    pub fn get_heading_tree(&self) -> Vec<HeadingNode> {
        let headings = self.extract_headings();
        let mut root: Vec<HeadingNode> = Vec::new();
        
        for heading in headings {
            let node = HeadingNode {
                heading: heading.clone(),
                children: Vec::new(),
            };
            
            // 查找合适的父节点（从根节点递归查找）
            let inserted = insert_heading_node(&mut root, node);
            if !inserted {
                root.push(HeadingNode {
                    heading: heading,
                    children: Vec::new(),
                });
            }
        }
        
        root
    }
}

/// 将标题节点插入到合适的位置
fn insert_heading_node(tree: &mut Vec<HeadingNode>, node: HeadingNode) -> bool {
    // 从最后一个节点开始查找
    if let Some(last) = tree.last_mut() {
        if last.heading.level < node.heading.level {
            // 尝试插入到最后一个节点的子树中
            let inserted = insert_heading_node(&mut last.children, node.clone());
            if inserted {
                return true;
            }
            // 如果没有找到合适的子节点，插入到这里
            last.children.push(node);
            return true;
        }
    }
    false
}

/// 标题树节点
#[derive(Debug, Clone)]
pub struct HeadingNode {
    /// 标题信息
    pub heading: Heading,
    /// 子标题
    pub children: Vec<HeadingNode>,
}

/// 生成标题锚点 ID
fn generate_anchor(text: &str) -> String {
    text.chars()
        .map(|c| {
            if c.is_whitespace() {
                '-'
            } else if c.is_alphanumeric() || c == '-' || c == '_' {
                c.to_ascii_lowercase()
            } else {
                '-'
            }
        })
        .collect::<String>()
        .trim_matches('-')
        .to_string()
}

/// 解析 URL 和可选的标题
fn parse_url_and_title(s: &str) -> (String, Option<String>) {
    let trimmed = s.trim();
    
    // 查找空格分隔的标题
    if let Some(space_pos) = trimmed.find(|c: char| c.is_whitespace()) {
        let url = trimmed[..space_pos].to_string();
        let title_part = trimmed[space_pos..].trim();
        
        let title = if (title_part.starts_with('"') && title_part.ends_with('"'))
            || (title_part.starts_with('\'') && title_part.ends_with('\''))
        {
            Some(title_part[1..title_part.len()-1].to_string())
        } else {
            Some(title_part.to_string())
        };
        
        (url, title)
    } else {
        (trimmed.to_string(), None)
    }
}

/// 移除标题标记
fn remove_heading_markers(s: &str) -> String {
    let trimmed = s.trim_start();
    if trimmed.starts_with('#') {
        let hash_count = trimmed.chars().take_while(|&c| c == '#').count();
        if hash_count <= 6 {
            return trimmed[hash_count..].trim_start().to_string();
        }
    }
    s.to_string()
}

/// 移除链接语法，保留文本
fn remove_link_syntax(s: &str) -> String {
    let mut result = s.to_string();
    
    while let Some(start) = result.find("](") {
        if let Some(text_end) = result[..start].rfind('[') {
            if let Some(url_end) = result[start..].find(')') {
                let text = &result[text_end + 1..start];
                result = format!("{}{}{}", &result[..text_end], text, &result[start + url_end + 1..]);
            } else {
                break;
            }
        } else {
            break;
        }
    }
    
    result
}

/// 移除图片语法，保留 alt 文本
fn remove_image_syntax(s: &str) -> String {
    let mut result = s.to_string();
    
    while let Some(start) = result.find("![") {
        if let Some(text_end) = result[start..].find("](") {
            if let Some(url_end) = result[start + text_end..].find(')') {
                let text = &result[start + 2..start + text_end];
                result = format!("{}{}{}", &result[..start], text, &result[start + text_end + url_end + 1..]);
            } else {
                break;
            }
        } else {
            break;
        }
    }
    
    result
}

/// 移除强调标记
fn remove_emphasis(s: &str) -> String {
    let mut result = s.to_string();
    
    // 移除 ** 和 __
    for marker in &["**", "__"] {
        while result.contains(marker) {
            if let Some(pos) = result.find(marker) {
                result = format!("{}{}", &result[..pos], &result[pos + 2..]);
            }
        }
    }
    
    // 移除 * 和 _（单独出现的强调标记）
    for marker in &["*", "_"] {
        let chars: Vec<char> = result.chars().collect();
        let mut new_chars = Vec::new();
        
        for (i, &c) in chars.iter().enumerate() {
            if c == marker.chars().next().unwrap() {
                let prev_is_space = i == 0 || chars[i - 1].is_whitespace();
                let next_is_space = i == chars.len() - 1 || chars[i + 1].is_whitespace();
                
                // 只在两侧都有空格时保留（不是强调标记）
                if prev_is_space && next_is_space {
                    new_chars.push(c);
                }
                // 否则跳过（移除强调标记）
            } else {
                new_chars.push(c);
            }
        }
        
        result = new_chars.into_iter().collect();
    }
    
    result
}

/// 移除行内代码
fn remove_inline_code(s: &str) -> String {
    let mut result = s.to_string();
    
    while let Some(start) = result.find('`') {
        if let Some(end) = result[start + 1..].find('`') {
            let code = &result[start + 1..start + 1 + end];
            result = format!("{}{}{}", &result[..start], code, &result[start + 1 + end + 1..]);
        } else {
            break;
        }
    }
    
    result
}

/// 移除列表标记
fn remove_list_markers(s: &str) -> String {
    let trimmed = s.trim_start();
    
    // 无序列表
    if trimmed.starts_with("- ") || trimmed.starts_with("* ") || trimmed.starts_with("+ ") {
        return trimmed[2..].to_string();
    }
    
    // 有序列表
    if let Some(dot_pos) = trimmed.find(". ") {
        if dot_pos > 0 && dot_pos < 10 {
            let num_str = &trimmed[..dot_pos];
            if num_str.chars().all(|c| c.is_ascii_digit()) {
                return trimmed[dot_pos + 2..].to_string();
            }
        }
    }
    
    s.to_string()
}

/// 移除引用标记
fn remove_blockquote_markers(s: &str) -> String {
    let trimmed = s.trim_start();
    if trimmed.starts_with("> ") {
        trimmed[2..].to_string()
    } else if trimmed.starts_with(">") {
        trimmed[1..].to_string()
    } else {
        s.to_string()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_extract_headings() {
        let md = "# Title\n## Subtitle\n### Section\n";
        let parser = MarkdownParser::new(md);
        let headings = parser.extract_headings();
        
        assert_eq!(headings.len(), 3);
        assert_eq!(headings[0].level, 1);
        assert_eq!(headings[0].text, "Title");
        assert_eq!(headings[1].level, 2);
        assert_eq!(headings[2].level, 3);
    }

    #[test]
    fn test_extract_links() {
        let md = "[Example](https://example.com \"Example Site\")\n![Image](image.png)";
        let parser = MarkdownParser::new(md);
        let links = parser.extract_links();
        
        assert_eq!(links.len(), 2);
        assert_eq!(links[0].text, "Example");
        assert_eq!(links[0].url, "https://example.com");
        assert_eq!(links[0].title, Some("Example Site".to_string()));
        assert!(!links[0].is_image);
        
        assert!(links[1].is_image);
        assert_eq!(links[1].text, "Image");
    }

    #[test]
    fn test_extract_code_blocks() {
        let md = "```rust\nfn main() {}\n```\n\n```python\nprint('hello')\n```";
        let parser = MarkdownParser::new(md);
        let blocks = parser.extract_code_blocks();
        
        assert_eq!(blocks.len(), 2);
        assert_eq!(blocks[0].language, Some("rust".to_string()));
        assert_eq!(blocks[1].language, Some("python".to_string()));
    }

    #[test]
    fn test_calculate_stats() {
        let md = "# Title\n\n这是一段中文内容。\n\n[link](url)\n\n![img](img.png)\n\n```\ncode\n```";
        let parser = MarkdownParser::new(md);
        let stats = parser.calculate_stats();
        
        assert!(stats.chinese_chars > 0);
        assert_eq!(stats.heading_count, 1);
        assert_eq!(stats.link_count, 1);
        assert_eq!(stats.image_count, 1);
        assert_eq!(stats.code_block_count, 1);
    }

    #[test]
    fn test_generate_toc() {
        let md = "# Main\n## Section 1\n### Subsection\n## Section 2";
        let parser = MarkdownParser::new(md);
        let toc = parser.generate_toc(3);
        
        assert!(toc.contains("[Main](#main)"));
        assert!(toc.contains("[Section 1](#section-1)"));
    }

    #[test]
    fn test_extract_plain_text() {
        let md = "# Title\n\nThis is **bold** and *italic*.\n\n[Link](url)";
        let parser = MarkdownParser::new(md);
        let plain = parser.extract_plain_text();
        
        assert!(!plain.contains("#"));
        assert!(!plain.contains("**"));
        assert!(!plain.contains("*"));
        assert!(!plain.contains("["));
        assert!(plain.contains("Title"));
        assert!(plain.contains("bold"));
        assert!(plain.contains("italic"));
        assert!(plain.contains("Link"));
    }

    #[test]
    fn test_generate_anchor() {
        assert_eq!(generate_anchor("Hello World"), "hello-world");
        assert_eq!(generate_anchor("Test_Title-123"), "test_title-123");
    }

    #[test]
    fn test_extract_list_items() {
        let md = "- Item 1\n- Item 2\n  1. Nested\n  2. Items\n- Item 3";
        let parser = MarkdownParser::new(md);
        let items = parser.extract_list_items();
        
        assert_eq!(items.len(), 5);
        assert!(!items[0].ordered);
        assert_eq!(items[0].text, "Item 1");
    }

    #[test]
    fn test_heading_tree() {
        let md = "# H1\n## H2\n### H3\n## H2-2\n# H1-2";
        let parser = MarkdownParser::new(md);
        let tree = parser.get_heading_tree();
        
        assert_eq!(tree.len(), 2); // Two H1 nodes
        assert_eq!(tree[0].children.len(), 2); // H1 has two H2 children
        assert_eq!(tree[0].children[0].children.len(), 1); // First H2 has one H3 child
    }
}
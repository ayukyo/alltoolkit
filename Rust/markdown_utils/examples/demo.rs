//! Markdown 工具使用示例

use markdown_utils::{MarkdownParser, HeadingNode};

fn main() {
    println!("=== Markdown Utils Demo ===\n");

    // 示例 Markdown 文档
    let markdown = r#"
# Rust 编程指南

## 简介

Rust 是一门系统编程语言，专注于**安全**、*并发*和性能。

## 基础语法

### 变量声明

```rust
let x = 5;
let mut y = 10;
```

### 函数定义

```rust
fn add(a: i32, b: i32) -> i32 {
    a + b
}
```

## 进阶特性

1. 所有权系统
2. 借用检查
3. 生命周期

## 资源链接

- [Rust 官网](https://rust-lang.org)
- [Rust 文档](https://doc.rust-lang.org "官方文档")
- ![Rust Logo](rust-logo.png)

## 总结

Rust 是一门优秀的编程语言！
"#;

    let parser = MarkdownParser::new(markdown);

    // 1. 提取标题
    println!("--- 标题列表 ---");
    let headings = parser.extract_headings();
    for h in &headings {
        println!("{}{} (Level {})", "  ".repeat(h.level - 1), h.text, h.level);
    }
    println!();

    // 2. 提取链接和图片
    println!("--- 链接和图片 ---");
    let links = parser.extract_links();
    for link in &links {
        if link.is_image {
            println!("[图片] {} -> {}", link.text, link.url);
        } else {
            println!("[链接] {} -> {}{}", 
                link.text, 
                link.url, 
                link.title.as_ref().map(|t| format!(" ({})", t)).unwrap_or_default()
            );
        }
    }
    println!();

    // 3. 提取代码块
    println!("--- 代码块 ---");
    let code_blocks = parser.extract_code_blocks();
    for (i, block) in code_blocks.iter().enumerate() {
        println!("代码块 #{} (语言: {})", 
            i + 1, 
            block.language.as_ref().unwrap_or(&"未知".to_string())
        );
        println!("行 {} - {}", block.start_line, block.end_line);
        println!("内容预览: {}...\n", &block.code.lines().next().unwrap_or(""));
    }

    // 4. 统计信息
    println!("--- 文档统计 ---");
    let stats = parser.calculate_stats();
    println!("字符数: {}", stats.characters);
    println!("单词数: {}", stats.words);
    println!("行数: {}", stats.lines);
    println!("中文字符: {}", stats.chinese_chars);
    println!("预估阅读时间: {} 分钟", stats.reading_time_minutes);
    println!("标题数量: {}", stats.heading_count);
    println!("链接数量: {}", stats.link_count);
    println!("图片数量: {}", stats.image_count);
    println!("代码块数量: {}", stats.code_block_count);
    println!();

    // 5. 生成目录
    println!("--- 自动生成的目录 ---");
    let toc = parser.generate_toc(3);
    println!("{}", toc);

    // 6. 提取纯文本
    println!("--- 纯文本内容 ---");
    let plain = parser.extract_plain_text();
    println!("{}", plain.lines().take(10).collect::<Vec<_>>().join("\n"));
    println!("...\n");

    // 7. 提取列表项
    println!("--- 列表项 ---");
    let items = parser.extract_list_items();
    for item in &items {
        let indent = "  ".repeat(item.indent);
        let marker = if item.ordered {
            format!("{}. ", item.number.unwrap_or(1))
        } else {
            "- ".to_string()
        };
        println!("{}{}{}", indent, marker, item.text);
    }
    println!();

    // 8. 标题树结构
    println!("--- 标题树结构 ---");
    let tree = parser.get_heading_tree();
    print_heading_tree(&tree, 0);
}

fn print_heading_tree(nodes: &[HeadingNode], depth: usize) {
    for node in nodes {
        let indent = "  ".repeat(depth);
        println!("{}{}", indent, node.heading.text);
        print_heading_tree(&node.children, depth + 1);
    }
}
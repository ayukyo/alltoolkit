# Markdown Utils

零外部依赖的 Rust Markdown 解析和处理工具库。

## 功能特性

- ✅ **标题提取** - 支持 ATX (#) 和 Setext 风格标题
- ✅ **链接提取** - 支持行内链接、图片链接、引用式链接
- ✅ **代码块提取** - 支持围栏代码块，自动识别语言
- ✅ **列表提取** - 支持有序和无序列表
- ✅ **目录生成** - 自动生成带层级缩进的 TOC
- ✅ **统计信息** - 字数统计、阅读时间预估
- ✅ **纯文本提取** - 移除所有 Markdown 格式
- ✅ **标题树结构** - 构建层级化的标题树

## 零依赖

本模块使用纯 Rust 标准库实现，无任何外部依赖。

## 安装

```toml
[dependencies]
markdown_utils = { path = "./markdown_utils" }
```

## 快速开始

```rust
use markdown_utils::MarkdownParser;

fn main() {
    let md = "# Hello\n## World\n[link](https://example.com)";
    let parser = MarkdownParser::new(md);
    
    // 提取标题
    let headings = parser.extract_headings();
    for h in &headings {
        println!("{}: {}", h.level, h.text);
    }
    
    // 提取链接
    let links = parser.extract_links();
    for link in &links {
        println!("{} -> {}", link.text, link.url);
    }
    
    // 生成目录
    let toc = parser.generate_toc(3);
    println!("{}", toc);
    
    // 统计信息
    let stats = parser.calculate_stats();
    println!("阅读时间约 {} 分钟", stats.reading_time_minutes);
}
```

## API 文档

### `MarkdownParser`

主要的解析器结构体。

#### 方法

| 方法 | 返回类型 | 描述 |
|------|----------|------|
| `new(content: &str)` | `Self` | 创建新的解析器 |
| `extract_headings()` | `Vec<Heading>` | 提取所有标题 |
| `extract_links()` | `Vec<Link>` | 提取所有链接和图片 |
| `extract_code_blocks()` | `Vec<CodeBlock>` | 提取所有代码块 |
| `extract_list_items()` | `Vec<ListItem>` | 提取所有列表项 |
| `calculate_stats()` | `Stats` | 计算文档统计信息 |
| `generate_toc(max_level: usize)` | `String` | 生成目录 (Markdown 格式) |
| `extract_plain_text()` | `String` | 提取纯文本内容 |
| `get_heading_tree()` | `Vec<HeadingNode>` | 获取层级标题树 |

### 数据结构

```rust
pub struct Heading {
    pub level: usize,        // 标题级别 (1-6)
    pub text: String,        // 标题文本
    pub anchor: String,      // 锚点 ID
    pub line_number: usize,  // 行号
}

pub struct Link {
    pub text: String,        // 链接文本/alt 文本
    pub url: String,         // URL
    pub title: Option<String>, // 可选标题
    pub is_image: bool,      // 是否为图片
    pub line_number: usize,  // 行号
}

pub struct CodeBlock {
    pub language: Option<String>, // 语言标识符
    pub code: String,             // 代码内容
    pub start_line: usize,        // 起始行号
    pub end_line: usize,          // 结束行号
}

pub struct Stats {
    pub characters: usize,        // 字符数
    pub words: usize,             // 单词数
    pub lines: usize,             // 行数
    pub chinese_chars: usize,     // 中文字符数
    pub reading_time_minutes: usize, // 预估阅读时间
    pub heading_count: usize,     // 标题数量
    pub link_count: usize,        // 链接数量
    pub image_count: usize,       // 图片数量
    pub code_block_count: usize,  // 代码块数量
}
```

## 运行示例

```bash
cd Rust/markdown_utils
cargo run --example demo
```

## 运行测试

```bash
cd Rust/markdown_utils
cargo test
```

## 许可证

MIT License
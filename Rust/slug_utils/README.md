# Slug Utils

一个零外部依赖的 Rust URL Slug 生成工具库，支持中文字符转拼音。

## 功能特性

- ✅ 字符串转 URL 友好 slug
- ✅ 内置中文转拼音支持（常用 300+ 汉字）
- ✅ 自定义分隔符
- ✅ 大小写转换选项
- ✅ 最大长度限制
- ✅ 去除停用词
- ✅ 批量处理
- ✅ 生成唯一 slug
- ✅ 零外部依赖

## 安装

将以下内容添加到 `Cargo.toml`:

```toml
[dependencies]
slug_utils = { path = "./slug_utils" }
```

## 快速开始

### 基本用法

```rust
use slug_utils::{slugify, SlugGenerator};

// 使用便捷函数
let slug = slugify("Hello World");
assert_eq!(slug, "hello-world");

// 使用生成器（更多配置选项）
let gen = SlugGenerator::default();
let slug = gen.slugify("This is a Test");
assert_eq!(slug, "this-is-a-test");
```

### 中文支持

```rust
use slug_utils::slugify;

let slug = slugify("中文标题测试");
// 输出类似: "zhong-wen-biao-ti-ce-shi"
```

### 自定义分隔符

```rust
use slug_utils::{slugify_with_separator, SlugOptions, SlugGenerator};

// 使用便捷函数
let slug = slugify_with_separator("Hello World", "_");
assert_eq!(slug, "hello_world");

// 使用生成器配置
let options = SlugOptions {
    separator: "_".to_string(),
    ..Default::default()
};
let gen = SlugGenerator::new(options);
let slug = gen.slugify("Test Case");
assert_eq!(slug, "test_case");
```

### 最大长度限制

```rust
use slug_utils::{slugify_with_max_length, SlugOptions, SlugGenerator};

// 使用便捷函数
let slug = slugify_with_max_length("This is a very long string", 10);
assert_eq!(slug, "this-is-a");

// 使用生成器配置
let options = SlugOptions {
    max_length: 15,
    ..Default::default()
};
let gen = SlugGenerator::new(options);
let slug = gen.slugify("Hello World Example");
assert_eq!(slug, "hello-world-exa");
```

### 保留大小写

```rust
use slug_utils::{SlugOptions, SlugGenerator};

let options = SlugOptions {
    lowercase: false,
    ..Default::default()
};
let gen = SlugGenerator::new(options);
let slug = gen.slugify("Hello World");
assert_eq!(slug, "Hello-World");
```

### 去除停用词

```rust
use slug_utils::{SlugOptions, SlugGenerator};

let options = SlugOptions {
    remove_stop_words: true,
    ..Default::default()
};
let gen = SlugGenerator::new(options);
let slug = gen.slugify("The Quick Brown Fox");
// "the" 被移除
assert_eq!(slug, "quick-brown-fox");
```

### 批量处理

```rust
use slug_utils::{slugify_batch, SlugGenerator};

// 使用便捷函数
let slugs = slugify_batch(&["Hello World", "Test Case", "Example"]);
assert_eq!(slugs, vec!["hello-world", "test-case", "example"]);

// 使用生成器
let gen = SlugGenerator::default();
let slugs = gen.slugify_batch(&["First", "Second Item", "Third One Here"]);
```

### 生成唯一 Slug

```rust
use slug_utils::SlugGenerator;

let gen = SlugGenerator::default();
let existing = vec!["hello-world".to_string()];

// 如果 slug 已存在，自动添加数字后缀
let unique = gen.unique_slug("Hello World", &existing);
assert_eq!(unique, "hello-world-1");

let existing2 = vec!["hello-world".to_string(), "hello-world-1".to_string()];
let unique2 = gen.unique_slug("Hello World", &existing2);
assert_eq!(unique2, "hello-world-2");
```

### 从文件名生成 Slug

```rust
use slug_utils::{slugify_filename, SlugGenerator};

// 使用便捷函数
let slug = slugify_filename("My Document.pdf");
assert_eq!(slug, "my-document");

// 使用生成器
let gen = SlugGenerator::default();
let slug = gen.from_filename("report_2024.xlsx");
assert_eq!(slug, "report-2024");
```

## 配置选项

| 选项 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `separator` | `String` | `"-"` | slug 单词分隔符 |
| `lowercase` | `bool` | `true` | 转换为小写 |
| `max_length` | `usize` | `0` | 最大长度（0 表示不限制） |
| `remove_stop_words` | `bool` | `false` | 去除英文停用词 |
| `keep_numbers` | `bool` | `true` | 保留数字 |

## 停用词列表

默认支持的英文停用词：

```
a, an, the, and, or, but, in, on, at, to, for, of,
is, are, was, were, be, been
```

可以使用自定义停用词列表：

```rust
use slug_utils::SlugGenerator;

let gen = SlugGenerator::default()
    .with_stop_words(vec![
        "a".to_string(),
        "the".to_string(),
        "custom".to_string(),
    ]);
```

## 中文拼音映射

内置了 300+ 常用汉字的拼音映射，包括：

- 数字：一二三四五六七八九十
- 时间：年月日时分秒
- 常用动词：做写说听看跑跳
- 常用名词：人事物地时
- 技术词汇：程序代码算法模块
- 等等...

## 性能特点

- 零外部依赖，编译后体积小
- 使用 HashMap 存储拼音映射，O(1) 查找
- 单次遍历字符串，时间复杂度 O(n)
- 内存占用低，适合高并发场景

## 应用场景

- 博客/文章 URL 生成
- 产品名称转 URL slug
- 文件名规范化
- 标签/分类名转换
- 用户名规范化
- SEO 友好 URL 生成

## License

MIT
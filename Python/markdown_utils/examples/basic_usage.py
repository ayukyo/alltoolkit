#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Markdown Utilities Basic Usage Examples
=====================================================
演示 markdown_utils 模块的基础用法。
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import *


def demo_conversion():
    """演示 Markdown 与 HTML 互转"""
    print("\n" + "="*60)
    print("1. Markdown 与 HTML 互转")
    print("="*60)
    
    # Markdown to HTML
    md = """
# Hello World

这是一个 **加粗** 和 *斜体* 的示例。

- 列表项 1
- 列表项 2

[链接](https://example.com)

```python
print("Hello")
```
"""
    
    print("\n原始 Markdown:")
    print(md)
    
    html = markdown_to_html(md)
    print("\n转换后的 HTML:")
    print(html[:500] + "..." if len(html) > 500 else html)
    
    # HTML to Markdown
    html_input = "<h1>Title</h1><p>Some <strong>bold</strong> text</p>"
    md_output = html_to_markdown(html_input)
    print(f"\nHTML 转 Markdown:")
    print(f"  输入：{html_input}")
    print(f"  输出：{md_output}")


def demo_extraction():
    """演示内容提取"""
    print("\n" + "="*60)
    print("2. 内容提取")
    print("="*60)
    
    md = """
# 第一章：开始

欢迎来到本书。

## 1.1 简介

这是简介内容。[了解更多](https://example.com)

## 1.2 快速开始

```python
def hello():
    print("Hello World")
```

| 步骤 | 描述 |
|:---|:---|
| 1 | 安装 |
| 2 | 配置 |
| 3 | 运行 |

![图示](diagram.png)
"""
    
    # 提取标题
    print("\n提取标题:")
    headings = extract_headings(md)
    for h in headings:
        print(f"  {'#' * h.level} {h.text} (行 {h.line_number})")
    
    # 提取链接
    print("\n提取链接:")
    links = extract_links(md)
    for link in links:
        type_str = "图片" if link.is_image else "链接"
        print(f"  [{type_str}] {link.text} → {link.url}")
    
    # 提取代码块
    print("\n提取代码块:")
    blocks = extract_code_blocks(md)
    for block in blocks:
        if not block.is_inline:
            print(f"  语言：{block.language}, 行数：{block.code.count(chr(10)) + 1}")
    
    # 提取表格
    print("\n提取表格:")
    tables = extract_tables(md)
    for table in tables:
        print(f"  列：{table.headers}")
        print(f"  行数：{len(table.rows)}")


def demo_generation():
    """演示内容生成"""
    print("\n" + "="*60)
    print("3. 内容生成")
    print("="*60)
    
    # 创建表格
    print("\n创建表格:")
    table = create_table(
        ["姓名", "年龄", "城市"],
        [["张三", "28", "北京"], ["李四", "25", "上海"], ["王五", "30", "广州"]],
        ["left", "center", "right"]
    )
    print(table)
    
    # 创建链接和图片
    print("\n创建链接和图片:")
    print(f"  链接：{create_link('Google', 'https://google.com', '搜索引擎')}")
    print(f"  图片：{create_image('Logo', 'logo.png', '公司标志')}")
    
    # 创建代码块
    print("\n创建代码块:")
    code = "print('Hello World')"
    print(create_code_block(code, "python"))
    
    # 创建列表
    print("\n创建列表:")
    print("无序列表:")
    print(create_list(["苹果", "香蕉", "橙子"]))
    
    print("\n有序列表:")
    print(create_list(["第一步", "第二步", "第三步"], ordered=True))
    
    # 创建引用
    print("\n创建引用:")
    print(create_blockquote("这是一段引用的文字。\n可以有多行。"))
    
    # 创建标题
    print("\n创建标题:")
    for i in range(1, 7):
        print(create_heading(f"{i} 级标题", i))


def demo_validation():
    """演示验证功能"""
    print("\n" + "="*60)
    print("4. 验证功能")
    print("="*60)
    
    # 有效的 Markdown
    valid_md = """# 标题

这是内容。

## 子标题

更多内容。
"""
    
    is_valid, issues = validate_markdown(valid_md)
    print(f"\n有效 Markdown 验证:")
    print(f"  结果：{'✓ 有效' if is_valid else '✗ 无效'}")
    if issues:
        print(f"  问题：{issues}")
    
    # 无效的 Markdown
    invalid_md = """# 标题

**未闭合的粗体

```python
未闭合的代码块
"""
    
    is_valid, issues = validate_markdown(invalid_md)
    print(f"\n无效 Markdown 验证:")
    print(f"  结果：{'✓ 有效' if is_valid else '✗ 无效'}")
    for issue in issues:
        print(f"  - {issue}")


def demo_transformation():
    """演示转换功能"""
    print("\n" + "="*60)
    print("5. 转换功能")
    print("="*60)
    
    md = """# 主标题

## 子标题 1

### 孙标题

## 子标题 2
"""
    
    # 标题级别转换
    print("\n原始标题结构:")
    for h in extract_headings(md):
        print(f"  {h.to_markdown()}")
    
    print("\n标题级别 +1 (降级):")
    transformed = transform_headings(md, 1)
    for h in extract_headings(transformed):
        print(f"  {h.to_markdown()}")
    
    # 移除格式
    print("\n移除所有格式:")
    plain = remove_formatting(md)
    print(plain)
    
    # 词数统计
    stats = word_count(md)
    print(f"\n词数统计:")
    print(f"  单词数：{stats['word_count']}")
    print(f"  字符数：{stats['char_count']}")
    print(f"  行数：{stats['line_count']}")


def demo_utilities():
    """演示工具函数"""
    print("\n" + "="*60)
    print("6. 工具函数")
    print("="*60)
    
    # 合并文档
    doc1 = "# 文档一\n内容一"
    doc2 = "# 文档二\n内容二"
    
    print("\n合并文档:")
    combined = join_markdown(doc1, doc2)
    print(combined)
    
    # 按标题分割
    print("\n按标题分割:")
    md = "# 章节 A\n内容 A\n# 章节 B\n内容 B\n# 章节 C\n内容 C"
    sections = split_by_heading(md)
    for title, content in sections.items():
        print(f"  [{title}]: {content[:20]}...")
    
    # 移除注释
    print("\n移除 HTML 注释:")
    md_with_comments = "Hello <!-- 这是注释 --> World"
    cleaned = strip_comments(md_with_comments)
    print(f"  原始：{md_with_comments}")
    print(f"  清理后：{cleaned}")


def demo_html_entities():
    """演示 HTML 实体处理"""
    print("\n" + "="*60)
    print("7. HTML 实体处理")
    print("="*60)
    
    text = '<script>alert("XSS")</script>'
    
    print(f"\n原始文本：{text}")
    
    escaped = escape_html(text)
    print(f"转义后：{escaped}")
    
    unescaped = unescape_html(escaped)
    print(f"还原后：{unescaped}")
    
    print(f"\n验证：{unescaped == text}")


def main():
    """运行所有演示"""
    print("\n" + "#"*60)
    print("# AllToolkit - Markdown Utilities 基础使用演示")
    print("#"*60)
    
    demo_conversion()
    demo_extraction()
    demo_generation()
    demo_validation()
    demo_transformation()
    demo_utilities()
    demo_html_entities()
    
    print("\n" + "="*60)
    print("演示完成!")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()

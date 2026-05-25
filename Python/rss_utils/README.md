# rss_utils - RSS/Atom 订阅工具

RSS 2.0 和 Atom 订阅源的解析和生成工具，零外部依赖。

## 功能特性

- **解析 RSS 2.0** - 解析标准 RSS 订阅源
- **解析 Atom** - 解析 Atom 格式订阅源
- **生成 RSS 2.0** - 生成标准 RSS XML
- **生成 Atom** - 生成 Atom 格式 XML
- **验证订阅源** - 检查订阅源结构有效性
- **提取链接** - 从订阅源提取所有链接
- **合并订阅源** - 合并多个订阅源

## 主要类

### FeedEntry
订阅条目类，表示单个 RSS/Atom 条目。

属性：
- `title` - 标题
- `link` - 链接
- `description` - 描述
- `author` - 作者
- `published` - 发布时间
- `updated` - 更新时间
- `categories` - 分类列表

### FeedInfo
订阅源信息类，包含订阅源元数据。

### RSSParser
RSS 2.0 解析器。

### AtomParser
Atom 解析器。

### RSSGenerator
RSS 2.0 生成器。

### AtomGenerator
Atom 生成器。

## 主要函数

### parse(content)
解析订阅源内容，自动检测格式。

```python
entries = parse(rss_xml_content)
for entry in entries:
    print(entry.title, entry.link)
```

### validate(content)
验证订阅源结构。

```python
is_valid, errors = validate(rss_xml_content)
print(f"Valid: {is_valid}, Errors: {errors}")
```

### generate_rss(entries, feed_info)
生成 RSS 2.0 XML。

```python
xml = generate_rss(entries, feed_info)
```

### generate_atom(entries, feed_info)
生成 Atom XML。

### extract_links(content)
从订阅源提取所有链接。

### find_entries(content, keyword)
搜索包含关键词的条目。

### merge_feeds(feeds)
合并多个订阅源。

## 使用示例

```python
from rss_utils import parse, generate_rss, FeedEntry, FeedInfo

# 解析订阅源
with open('feed.xml', 'r') as f:
    entries = parse(f.read())

for entry in entries:
    print(f"{entry.title}: {entry.link}")

# 生成订阅源
entries = [
    FeedEntry(title="文章标题", link="https://example.com/article"),
    FeedEntry(title="另一篇文章", link="https://example.com/article2"),
]

feed_info = FeedInfo(
    title="我的订阅源",
    link="https://example.com/feed",
    description="最新文章"
)

rss_xml = generate_rss(entries, feed_info)
```

## 测试

运行测试：
```bash
python rss_utils/rss_utils_test.py
```

测试覆盖率：35 个测试用例，100% 通过。

---

*最后更新: 2026-05-26*
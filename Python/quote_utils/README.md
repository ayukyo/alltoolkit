# Quote Utils

名言警句工具模块，提供名言获取、管理、格式化和输出功能。

## 功能

- **内置名言库** - 中英文名言，按主题分类
- **随机获取** - 随机获取名言或按类别筛选
- **多种格式输出** - 简洁、卡片、横幅、签名档等样式
- **收藏管理** - 收藏、取消收藏、获取收藏列表
- **名言卡片** - 生成美观的名言卡片
- **每日推荐** - 基于日期的每日名言推荐

## 安装

```python
from quote_utils.mod import QuoteManager, Quote, QuoteCategory
```

## 快速开始

### 获取名言

```python
from quote_utils.mod import QuoteManager, QuoteCategory

manager = QuoteManager()

# 获取随机名言
quote = manager.get_random_quote()
print(f"{quote.text} —— {quote.author}")

# 按类别获取
quote = manager.get_random_quote_by_category(QuoteCategory.WISDOM)

# 获取每日名言（基于日期）
quote = manager.get_quote_of_the_day()
```

### 名言分类

支持多种名言类别：

- `LIFE` - 人生
- `SUCCESS` - 成功
- `WISDOM` - 智慧
- `LOVE` - 爱情
- `COURAGE` - 勇气
- `MOTIVATION` - 激励
- `LEARNING` - 学习
- `WORK` - 工作
- `HEALTH` - 健康
- `FRIENDSHIP` - 友谊
- `TIME` - 时间
- `HAPPINESS` - 幸福
- `PHILOSOPHY` - 哲学
- `NATURE` - 自然
- `HUMOR` - 幽默
- `CHINESE` - 中国古语

### 格式化输出

```python
from quote_utils.mod import QuoteStyle

# 简洁样式
text = manager.format_quote(quote, QuoteStyle.SIMPLE)
# "名言内容 —— 作者"

# 卡片样式
text = manager.format_quote(quote, QuoteStyle.CARD)
# ┌──────────────────────┐
# │ 名言内容             │
# │                      │
# │                —— 作者 │
# └──────────────────────┘

# 横幅样式
text = manager.format_quote(quote, QuoteStyle.BANNER)
# ═══════════════════════════════════
# 名言内容
#                                 —— 作者
# ═══════════════════════════════════

# 极简样式
text = manager.format_quote(quote, QuoteStyle.MINIMAL)
# 名言内容
# —— 作者
```

### 名言收藏

```python
# 收藏名言
manager.add_to_favorites(quote)

# 取消收藏
manager.remove_from_favorites(quote)

# 获取所有收藏
favorites = manager.get_favorites()
```

### 搜索名言

```python
# 按关键词搜索
results = manager.search_quotes("人生")
for quote in results:
    print(f"{quote.text} —— {quote.author}")

# 按作者搜索
results = manager.search_quotes(author="鲁迅")
```

### 自定义名言

```python
from quote_utils.mod import Quote

# 创建自定义名言
custom_quote = Quote(
    text="知识就是力量",
    author="培根",
    category=QuoteCategory.WISDOM,
    language="zh",
    tags=["知识", "力量"]
)

# 添加到管理器
manager.add_quote(custom_quote)
```

### 导出和导入

```python
# 导出为 JSON
json_data = manager.export_to_json()

# 从 JSON 导入
manager.import_from_json(json_data)
```

## API 参考

### QuoteManager

| 方法 | 说明 |
|------|------|
| `get_random_quote()` | 获取随机名言 |
| `get_random_quote_by_category(category)` | 按类别获取随机名言 |
| `get_quote_of_the_day()` | 获取每日名言 |
| `search_quotes(keyword)` | 搜索名言 |
| `format_quote(quote, style)` | 格式化名言 |
| `add_to_favorites(quote)` | 添加到收藏 |
| `get_favorites()` | 获取收藏列表 |

### Quote

| 属性 | 说明 |
|------|------|
| `text` | 名言内容 |
| `author` | 作者 |
| `category` | 类别 |
| `language` | 语言 (zh/en) |
| `source` | 出处 |
| `tags` | 标签列表 |
| `rating` | 评分 (1-5) |
| `is_favorite` | 是否收藏 |

## 测试

```bash
cd Python/quote_utils
python quote_utils_test.py
```

测试覆盖率：60 个测试用例，100% 通过 ✅

## 许可证

MIT License
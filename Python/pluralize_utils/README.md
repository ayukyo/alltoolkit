# Pluralize Utils


pluralize_utils - 英文单词单复数转换工具

提供英文单词的单数/复数形式转换功能，支持规则变化和不规则变化。
零外部依赖，纯 Python 实现。

功能:
- 单数转复数 (singular_to_plural)
- 复数转单数 (plural_to_singular)
- 判断是否为复数 (is_plural)
- 获取单词的单复数形式 (get_plural_form)
- 批量转换 (batch_pluralize, batch_singularize)


## 功能

### 函数

- **singular_to_plural(word, count**) - 将英文单词从单数转换为复数形式。
- **plural_to_singular(word**) - 将英文单词从复数转换为单数形式。
- **is_plural(word**) - 判断单词是否为复数形式。
- **get_plural_form(word, count**) - 根据数量返回单词的正确形式。
- **batch_pluralize(words**) - 批量将单词转换为复数形式。
- **batch_singularize(words**) - 批量将单词转换为单数形式。
- **pluralize_word(word, count**) - 智能判断并转换单词形式（singular_to_plural 的别名）。
- **singularize_word(word**) - 智能判断并转换单词形式（plural_to_singular 的别名）。
- **get_article(word, count**) - 获取适合单词的冠词。
- **format_count(word, count, include_article**) - 格式化数量和单词的组合。

## 使用示例

```python
from mod import singular_to_plural

# 使用 singular_to_plural
result = singular_to_plural()
```

## 测试

运行测试：

```bash
python *_test.py
```

## 文件结构

```
{module_name}/
├── mod.py              # 主模块
├── *_test.py           # 测试文件
├── README.md           # 本文档
└── examples/           # 示例代码
    └── usage_examples.py
```

---

**Last updated**: 2026-04-28

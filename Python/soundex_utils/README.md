# Soundex Utils


SOUNDEX 语音编码工具模块

SOUNDEX 是一种语音算法，用于按发音索引姓名。由 Robert C. Russell 于1918年发明，
广泛用于家谱研究、姓名匹配和模糊字符串匹配。

功能特点:
- 标准 SOUNDEX 编码（美国人口普查局版本）
- 增强 SOUNEX 变体（处理前缀和特殊字符）
- 姓名相似度比较
- 批量编码和匹配
- 支持多语言字符转写

零外部依赖，纯 Python 实现。


## 功能

### 类

- **SoundexEncoder**: SOUNDEX 编码器类

提供完整的 SOUNDEX 编码功能，支持自定义规则和变体。

示例:
    >>> encoder = SoundexEncoder()
    >>> encoder
  方法: encode, encode_batch, similarity, matches, find_similar ... (7 个方法)
- **SoundexRefinedEncoder**: 改进的 SOUNDEX 编码器（Refined Soundex）

使用更精细的编码映射，减少误匹配。

示例:
    >>> encoder = SoundexRefinedEncoder()
    >>> encoder
- **SoundexSQL**: SOUNDEX SQL 辅助工具类

提供 SQL 数据库相关的 SOUNDEX 功能。
  方法: where_clause, create_index_sql

### 函数

- **encode(name**) - 使用默认编码器编码姓名
- **similarity(name1, name2**) - 计算两个姓名的相似度
- **matches(name1, name2, threshold**) - 判断两个姓名是否匹配
- **find_similar(target, candidates, threshold**) - 在候选列表中查找与目标相似的姓名
- **group_by_sound(names**) - 按发音将姓名分组
- **get_common_code(name**) - 获取常见姓名的 SOUNDEX 编码
- **encode(self, name**) - 将姓名编码为 SOUNDEX 代码
- **encode_batch(self, names**) - 批量编码姓名
- **similarity(self, name1, name2**) - 计算两个姓名的 SOUNDEX 相似度
- **matches(self, name1, name2**, ...) - 判断两个姓名是否匹配

... 共 15 个函数

## 使用示例

```python
from mod import encode

# 使用 encode
result = encode()
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

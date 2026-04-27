# Metaphone Utils


Metaphone Utils - 语音编码工具模块

提供 Metaphone 和 Double Metaphone 算法实现，用于单词的语音相似度匹配。
Metaphone 比 Soundex 更准确，特别适用于英语单词的模糊搜索和拼写纠正。

核心功能：
- Metaphone 编码（原始算法）
- Double Metaphone 编码（改进版本，返回主要和次要编码）
- 语音相似度比较
- 批量编码处理

零外部依赖，纯 Python 实现。


## 功能

### 类

- **Metaphone**: Metaphone 语音编码器

将单词转换为其语音表示，用于模糊匹配和拼写检查。
基于发音规则而非精确拼写。

Note:
    优化版本（v2）：
    - 预编译字符处理查找表，避免多次条件判断
    - 预定义规则映射，减少运行时计算
    - 边界处理：空输入、非字符串、过长输入
    - 性能优化：单次遍历处理，减少字符串操作
  方法: encode
- **DoubleMetaphone**: Double Metaphone 编码器

改进版的 Metaphone 算法，返回主要和次要编码，
能更好地处理多语言单词（尤其是斯拉夫语系和德语）。
  方法: encode
- **PhoneticMatcher**: 语音匹配器

提供基于 Metaphone 编码的语音相似度匹配功能。
  方法: encode, encode_double, sounds_like, similarity, build_index ... (7 个方法)

### 函数

- **metaphone(word, max_length**) - 计算单词的 Metaphone 编码
- **double_metaphone(word, max_length**) - 计算单词的 Double Metaphone 编码
- **sounds_like(word1, word2**) - 检查两个单词是否发音相似
- **phonetic_similarity(word1, word2**) - 计算两个单词的语音相似度
- **encode(self, word**) - 将单词编码为 Metaphone 代码
- **encode(self, word**) - 将单词编码为 Double Metaphone 代码
- **encode(self, word**) - 编码单词（单编码模式）
- **encode_double(self, word**) - 编码单词（双编码模式）
- **sounds_like(self, word1, word2**, ...) - 检查两个单词是否发音相似
- **similarity(self, word1, word2**) - 计算两个单词的语音相似度

... 共 13 个函数

## 使用示例

```python
from mod import metaphone

# 使用 metaphone
result = metaphone()
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

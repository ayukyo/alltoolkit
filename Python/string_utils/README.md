# string_utils - 字符串处理工具集

零外部依赖的 Python 字符串处理工具库，纯标准库实现。

## 功能概览

### 字符串统计
- `count_chars` - 统计字符数（可选包含空白）
- `count_words` - 统计单词数（支持中英文混合）
- `count_lines` - 统计行数
- `count_sentences` - 统计句子数
- `get_text_stats` - 获取完整文本统计
- `get_char_frequency` - 字符频率统计
- `get_word_frequency` - 单词频率统计

### 大小写转换
- `to_camel_case` - 转换为驼峰命名（camelCase/PascalCase）
- `to_snake_case` - 转换为蛇形命名（snake_case）
- `to_kebab_case` - 转换为短横线命名（kebab-case）
- `to_constant_case` - 转换为常量命名（CONSTANT_CASE）
- `to_title_case` - 转换为标题格式
- `to_sentence_case` - 转换为句子格式
- `swap_case` - 交换大小写

### 字符串清理
- `strip_whitespace` - 去除空白（多种模式）
- `normalize_whitespace` - 规范化空白
- `remove_special_chars` - 移除特殊字符
- `remove_html_tags` - 移除HTML标签
- `unescape_html` - 反转义HTML实体
- `clean_text` - 综合文本清理
- `trim_lines` - 去除每行空白

### 字符串相似度
- `levenshtein_distance` - Levenshtein编辑距离
- `similarity_ratio` - 相似度比例（0-1）
- `sequence_similarity` - SequenceMatcher相似度
- `find_similar` - 在列表中查找相似字符串
- `jaccard_similarity` - Jaccard相似度

### 字符串反转与排序
- `reverse_string` - 反转字符串
- `reverse_words` - 反转单词顺序
- `reverse_lines` - 反转行顺序
- `sort_words` - 对单词排序
- `sort_lines` - 对行排序
- `unique_lines` - 去除重复行
- `unique_chars` - 去除重复字符

### 模式提取
- `extract_emails` - 提取邮箱地址
- `extract_urls` - 提取URL
- `extract_phone_numbers` - 提取电话号码
- `extract_numbers` - 提取数字
- `extract_chinese` - 提取中文
- `extract_english` - 提取英文单词
- `extract_dates` - 提取日期
- `extract_hex_colors` - 提取颜色值
- `extract_pattern` - 自定义正则提取

### 字符串生成
- `random_string` - 生成随机字符串
- `random_password` - 生成随机密码
- `generate_uuid` - 生成UUID
- `generate_ordinal` - 生成序数词（1st, 第1）
- `generate_ngrams` - 生成N-gram序列

### 字符串格式化
- `indent_text` - 缩进文本
- `wrap_text` - 文本换行
- `align_text` - 文本对齐
- `pad_text` - 字符填充
- `truncate_text` - 截断文本
- `format_number` - 格式化数字（千位分隔符）
- `center_with_char` - 字符居中填充

### 实用工具
- `is_palindrome` - 回文检测
- `count_vowels` - 统计元音
- `count_consonants` - 统计辅音
- `is_anagram` - 变位词检测
- `split_into_chunks` - 文本分块
- `remove_duplicates` - 单词去重
- `repeat_string` - 重复字符串
- `is_all_uppercase/lowercase` - 大小写检测
- `capitalize_each_word` - 每词首字母大写
- `contains_any/all` - 字符包含检测

## 使用示例

```python
from string_utils.mod import *

# 文本统计
text = "Hello World! 你好世界！"
print(get_text_stats(text))
# {'chars': 20, 'words': 6, 'lines': 1, 'sentences': 2, ...}

# 大小写转换
print(to_camel_case("hello-world-test"))  # helloWorldTest
print(to_snake_case("HelloWorld"))         # hello_world
print(to_constant_case("hello world"))     # HELLO_WORLD

# 相似度计算
print(levenshtein_distance("kitten", "sitting"))  # 3
print(similarity_ratio("hello", "hallo"))         # 0.8

# 模式提取
text = "联系 test@example.com，电话 13812345678"
print(extract_emails(text))      # ['test@example.com']
print(extract_phone_numbers(text)) # ['13812345678']

# 随机生成
print(random_string(16))         # aB3dE7fG9hJ2kL5m
print(random_password(12))       # Kj#mN8pQ@2xY
print(generate_uuid())           # 550e8400-e29b-41d4-a716-...

# 格式化
print(format_number(1234567.89))  # 1,234,567.89
print(truncate_text("很长的文本...", 10))  # 很长的文本...

# 实用工具
print(is_palindrome("racecar"))   # True
print(is_anagram("listen", "silent"))  # True
```

## 测试

```bash
python string_utils_test.py
```

所有功能均包含完整的单元测试。

## 特性

- ✅ 零外部依赖（纯Python标准库）
- ✅ 支持中英文混合处理
- ✅ 类型提示完整
- ✅ 文档字符串详细
- ✅ 60+ 字符串处理函数

## 许可

MIT License
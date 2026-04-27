# Braille Utils


Braille Utilities - 盲文编码/解码工具

功能：
- 文本与盲文点字互转
- 支持多语言（英文、数字、基本标点）
- 盲文 Unicode 与点阵表示互转
- 盲文等级支持（Grade 1 / Grade 2 缩写）
- 音乐盲文基础支持

盲文基础：
- 盲文单元格由 6 个点组成（2列×3行）
- 点位编号：左列从上到下 1-2-3，右列从上到下 4-5-6
- Unicode 盲文字符范围: U+2800 - U+283F


## 功能

### 类

- **BrailleGrade**: 盲文等级
- **BrailleCell**: 盲文单元格类
  方法: to_unicode, from_unicode, to_dots_pattern, from_dots_pattern, to_binary_matrix
- **BrailleEncoder**: 盲文编码器
  方法: encode, decode
- **BrailleUtils**: 盲文工具类
  方法: text_to_braille, braille_to_text, dots_to_unicode, unicode_to_dots, is_braille_char ... (12 个方法)

### 函数

- **text_to_braille(text, grade**) - 文本转盲文（便捷函数）
- **braille_to_text(braille**) - 盲文转文本（便捷函数）
- **dots_to_unicode(dots_pattern**) - 点位转 Unicode（便捷函数）
- **unicode_to_dots(char**) - Unicode 转点位（便捷函数）
- **display_braille(char**) - 显示盲文矩阵（便捷函数）
- **to_unicode(self**) - 转换为 Unicode 盲文字符
- **from_unicode(cls, char**) - 从 Unicode 盲文字符创建单元格
- **to_dots_pattern(self**) - 转换为点位模式字符串，如 '⠓' -> '125'
- **from_dots_pattern(cls, pattern**) - 从点位模式创建，如 '125' -> '⠓'
- **to_binary_matrix(self**) - 转换为 2x3 二进制矩阵

... 共 24 个函数

## 使用示例

```python
from mod import text_to_braille

# 使用 text_to_braille
result = text_to_braille()
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

# Morse Utils


Morse Utils - 摩尔斯电码工具

零依赖的摩尔斯电码库，支持：
- 文本转摩尔斯电码编码
- 摩尔斯电码转文本解码
- 音频信号生成（正弦波）
- 支持多语言字符（A-Z、数字、常见符号）
- 自定义分隔符和时间参数
- 摩尔斯电码验证
- 常见缩写和Q代码支持

Author: AllToolkit
License: MIT


## 功能

### 类

- **MorseError**: 摩尔斯电码错误基类
- **InvalidCharacterError**: 无效字符错误
- **InvalidMorseError**: 无效摩尔斯电码错误
- **MorseConfig**: 摩尔斯电码配置
  方法: unit
- **MorseCode**: 摩尔斯电码类，提供面向对象的API
  方法: encode, decode, to_audio, duration

### 函数

- **encode(text, letter_separator, word_separator**, ...) - 将文本编码为摩尔斯电码
- **decode(morse, letter_separator, word_separator**, ...) - 将摩尔斯电码解码为文本
- **encode_file(input_path, output_path, letter_separator**, ...) - 编码文件内容
- **decode_file(input_path, output_path, letter_separator**, ...) - 解码文件内容
- **is_valid_morse(morse**) - 检查字符串是否为有效的摩尔斯电码
- **is_valid_text_for_encoding(text**) - 检查文本是否可以完全编码
- **get_supported_characters(**) - 获取所有支持的字符
- **get_morse_for_char(char**) - 获取字符对应的摩尔斯电码
- **get_char_for_morse(morse**) - 获取摩尔斯电码对应的字符
- **normalize_morse(morse**) - 标准化摩尔斯电码字符串

... 共 30 个函数

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

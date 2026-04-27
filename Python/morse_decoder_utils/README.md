# Morse Decoder Utils


Morse Code Decoder Utils - Morse码解码工具

功能：
1. 文本 Morse 码解码（支持多种分隔符格式）
2. 音频信号解码（通过波形分析）
3. 自动速率检测
4. 噪声过滤
5. 信号质量分析

零外部依赖，纯 Python 实现


## 功能

### 类

- **MorseDecoder**: Morse码解码器
  方法: decode_text, decode_signal, analyze_signal_quality

### 函数

- **decode_morse(morse, char_sep, word_sep**) - 快速解码 Morse 码文本的便捷函数
- **decode_signal(signal, sample_rate, threshold**) - 快速解码信号的便捷函数
- **analyze_signal(signal, sample_rate**) - 分析信号质量的便捷函数
- **quick_decode(morse**) - 快速解码，优先使用常用短语
- **decode_text(self, morse, char_sep**, ...) - 解码文本形式的 Morse 码
- **decode_signal(self, signal, sample_rate**, ...) - 从信号序列解码 Morse 码
- **analyze_signal_quality(self, signal, sample_rate**) - 分析信号质量

## 使用示例

```python
from mod import decode_morse

# 使用 decode_morse
result = decode_morse()
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

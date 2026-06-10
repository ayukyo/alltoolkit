# Baudot Utils - 博多码工具

博多码（Baudot Code）编码/解码工具，用于老式电报系统，零依赖。

## 功能特性

- **编码/解码**: 文本与博多码互转
- **ITA2 标准**: 支持国际ITA2字母表
- **LTRS/FIGS 切换**: 正确处理字符集切换
- **摩尔斯码支持**: 可选转换为摩尔斯电码

## 快速开始

```python
from baudot_utils.mod import encode_baudot, decode_baudot

# 编码
code = encode_baudot("HELLO")
print(code)  # 二进制字符串

# 解码
text = decode_baudot(code)
print(text)  # "HELLO"
```

## API 参考

| 函数 | 说明 |
|------|------|
| `encode_baudot(text)` | 文本转博多码 |
| `decode_baudot(code)` | 博多码转文本 |
| `text_to_baudot_binary(text)` | 转二进制字符串 |
| `baudot_binary_to_text(binary)` | 二进制转文本 |

## 博多码原理

博多码是一种5位编码，最初由 Emile Baudot 发明。每个字符用5个单位表示，支持LTRS（字母）和FIGS（数字/符号）两个切换状态。

---

**测试覆盖**: 29 passed
# Morse Code Utils

一个功能完整的摩尔斯电码编解码工具库，零外部依赖。

## 功能特性

- **文本编码** - 将文本转换为摩尔斯电码
- **电码解码** - 将摩尔斯电码转换回文本
- **自定义符号** - 支持自定义点和划的表示符号
- **时序生成** - 根据速度(WPM)生成音频时序
- **可视表示** - 生成易读的可视化摩尔斯电码
- **电码分析** - 分析摩尔斯电码字符串
- **Prosigns** - 支持常用程序信号(如 AR, SK, SOS)

## 快速开始

### 基本用法

```python
from mod import encode, decode

# 编码
morse = encode('HELLO WORLD')
# 输出: .... . .-.. .-.. --- / .-- --- .-. .-.. -..

# 解码
text = decode('... --- ...')
# 输出: SOS
```

### 自定义符号

```python
from mod import MorseEncoder, MorseDecoder

# 使用自定义符号
encoder = MorseEncoder(dot_symbol='●', dash_symbol='—')
morse = encoder.encode('SOS')
# 输出: ●●● ——— ●●●

# 解码时使用相同符号
decoder = MorseDecoder(dot_symbol='●', dash_symbol='—')
text = decoder.decode(morse)
# 输出: SOS
```

### 时序计算

```python
from mod import calculate_speed, get_timing_sequence

# 计算指定速度的时序参数
timing = calculate_speed(wpm=15)
# 返回: dot_ms, dash_ms, gaps 等

# 生成播放时序
sequence = get_timing_sequence('SOS', wpm=15)
# 返回: [(True, 80), (False, 80), ...] - (是否发声, 持续毫秒)
```

### 可视化表示

```python
from mod import text_to_visual

visual = text_to_visual('HELLO WORLD')
# 输出:
# ●●●● ● ●—●● ●—●● ——— / ●—— ——— ●—● ●—●● ●——●
```

### 便捷函数

```python
from mod import sos, hello_world, is_morse

# 常用信号
sos_signal = sos()  # '... --- ...'
hw = hello_world()  # '.... . .-.. .-.. --- / .-- --- .-. .-.. -..'

# 检测是否为摩尔斯电码
is_morse('... --- ...')  # True
is_morse('Hello')        # False
```

## API 参考

### 编码器类 `MorseEncoder`

```python
encoder = MorseEncoder(
    dot_symbol='.',      # 点符号
    dash_symbol='-',     # 划符号
    char_separator=' ',  # 字符分隔符
    word_separator=' / '  # 单词分隔符
)

encoder.encode(text)      # 编码文本
encoder.encode_char(char) # 编码单字符
encoder.encode_prosign(name)  # 编码程序信号
```

### 解码器类 `MorseDecoder`

```python
decoder = MorseDecoder(
    dot_symbol='.',
    dash_symbol='-',
    char_separator=' ',
    word_separator=' / '
)

decoder.decode(morse)      # 解码电码
decoder.decode_char(morse) # 解码单字符
decoder.normalize_morse(morse)  # 标准化符号
```

### 工具函数

| 函数 | 说明 |
|------|------|
| `encode(text, dot, dash)` | 快速编码文本 |
| `decode(morse, dot, dash)` | 快速解码电码 |
| `is_morse(text)` | 检测是否为电码 |
| `calculate_speed(wpm)` | 计算时序参数 |
| `get_timing_sequence(text, wpm)` | 生成播放时序 |
| `text_to_visual(text, width)` | 可视化表示 |
| `get_morse_reference()` | 获取电码字典 |
| `analyze_morse(morse)` | 分析电码 |
| `sos()` | 获取 SOS 信号 |
| `hello_world()` | 获取示例电码 |

## 支持的字符

### 字母
```
A .-      B -...    C -.-.    D -..     E .
F ..-.    G --.     H ....    I ..      J .---
K -.-     L .-..    M --      N -.      O ---
P .--.    Q --.-    R .-.     S ...     T -
U ..-     V ...-    W .--     X -..-    Y -.--
Z --..
```

### 数字
```
0 -----   1 .----   2 ..---   3 ...--   4 ....-
5 .....   6 -....   7 --...   8 ---..   9 ----.
```

### 标点符号
```
. .-.-.-   , --..--   ? ..--..   ' .----.
! -.-.--   / -..-.    ( -.--.    ) -.--.-
& .-...    : ---...   ; -.-.-.   = -...-
+ .-.-.    - -....-   _ ..--.-   " .-..-.
$ ...-..-  @ .--.-.
```

### 程序信号 (Prosigns)
```
AA  .-.-     结束消息
AR  .-.-.    结束传输
AS  .-...    等待
BT  -...-    中断/暂停
SK  ...-.-   结束工作
```

## 示例

### 运行演示

```bash
python mod.py
```

### 运行测试

```bash
python -m pytest morse_utils_test.py -v
```

## 技术细节

### 时序标准

基于 PARIS 标准计算时序：
- 点 = 1 单位
- 划 = 3 单位
- 元素间隔 = 1 单位
- 字符间隔 = 3 单位
- 单词间隔 = 7 单位

15 WPM 时，单位时长约 80ms。

## 许可证

MIT License
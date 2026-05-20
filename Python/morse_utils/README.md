# Morse Utils - 摩尔斯电码工具

摩尔斯电码编码、解码、音频生成工具模块。零依赖，纯 Python 标准库实现。

## 功能特性

- ✅ 文本转摩尔斯电码 (编码)
- ✅ 尔斯电码转文本 (解码)
- ✅ WAV 音频生成 (可配置频率/速度)
- ✅ 支持完整国际摩尔斯电码表
- ✅ 支持字母、数字、标点符号
- ✅ 常用无线电缩写支持
- ✅ 统计信息 (点划计数、播放时长)
- ✅ 多种可视化格式 (标准/圆点/竖线/音效拟声)
- ✅ 练习功能 (随机/指定字符)
- ✅ 电码验证
- ✅ 可自定义符号和分隔符
- ✅ 未知字符灵活处理

## 快速开始

### 基本使用

```python
from morse_utils.mod import encode, decode

# 编码
morse = encode('HELLO WORLD')
print(morse)
# 输出: '.... . .-.. .-.. --- / .-- --- .-. .-.. -..'

# 解码
text = decode('... --- ...')
print(text)
# 输出: 'SOS'
```

### 使用类

```python
from morse_utils.mod import MorseUtils

utils = MorseUtils()

# 编码
morse = utils.encode('SOS')  # '... --- ...'

# 解码
text = utils.decode('... --- ...')  # 'SOS'

# 统计信息
stats = utils.get_statistics('HELLO')
print(stats['dot_count'])    # 点的数量
print(stats['duration_seconds'])  # 播放时长

# 可视化
sound = utils.visualize('SOS', style='sound')
print(sound)  # 'di-di-dit da-da-dah di-di-dit'
```

### 音频生成

```python
from morse_utils.mod import MorseAudioGenerator

generator = MorseAudioGenerator()

# 生成音频数据
audio = generator.generate_audio('SOS')

# 保存为 WAV 文件
generator.save_audio('HELLO', 'hello.wav')
```

## API 文档

### 便捷函数

| 函数 | 描述 |
|------|------|
| `encode(text)` | 编码文本为摩尔斯电码 |
| `decode(morse)` | 解码摩尔斯电码为文本 |
| `generate_audio(text)` | 生成 WAV 音频数据 |
| `save_audio(text, filepath)` | 保存音频到文件 |
| `get_morse_table()` | 获取完整电码表 |
| `get_abbreviations()` | 获取常用缩写表 |

### MorseEncoder 类

```python
encoder = MorseEncoder()
encoder.encode(text)          # 编码文本
encoder.encode_letter(char)   # 编码单字符
```

### MorseDecoder 类

```python
decoder = MorseDecoder()
decoder.decode(morse)           # 解码电码
decoder.decode_letter(morse)    # 解码单字母电码
decoder.is_valid_morse(morse)   # 验证电码有效性
```

### MorseAudioGenerator 类

```python
generator = MorseAudioGenerator()
generator.generate_audio(text)    # 生成音频数据
generator.save_audio(text, path)  # 保存音频文件
```

### MorseUtils 类 (综合工具)

```python
utils = MorseUtils()
utils.encode(text)               # 编码
utils.decode(morse)              # 解码
utils.generate_audio(text)       # 生成音频
utils.save_audio(text, path)     # 保存音频
utils.calculate_duration(text)   # 计算播放时长
utils.get_statistics(text)       # 获取统计信息
utils.visualize(text, style)     # 可视化
utils.practice(char)             # 生成练习材料
utils.is_valid_morse(morse)      # 验证电码
```

### MorseConfig 配置

```python
config = MorseConfig(
    dot_symbol='.',           # 点符号
    dash_symbol='-',          # 划符号
    symbol_separator=' ',     # 符号间隔
    letter_separator=' ',     # 字母间隔
    word_separator=' / ',     # 单词间隔
    frequency=700,            # 音频频率 (Hz)
    sample_rate=44100,        # 采样率
    dot_duration=0.06,        # 点持续时间 (秒)
    unknown_char='?',         # 未知字符替换
    ignore_unknown=False,     # 是否忽略未知字符
)
```

## 摩尔斯电码表

### 字母

| 字符 | 电码 | 字符 | 电码 |
|------|------|------|------|
| A | .- | N | -. |
| B | -... | O | --- |
| C | -.-. | P | .--. |
| D | -.. | Q | --.- |
| E | . | R | .-. |
| F | ..-. | S | ... |
| G | --. | T | - |
| H | .... | U | ..- |
| I | .. | V | ...- |
| J | .--- | W | .-- |
| K | -.- | X | -..- |
| L | .-.. | Y | -.-- |
| M | -- | Z | --.. |

### 数字

| 数字 | 电码 |
|------|------|
| 0 | ----- |
| 1 | .---- |
| 2 | ..--- |
| 3 | ...-- |
| 4 | ....- |
| 5 | ..... |
| 6 | -.... |
| 7 | --... |
| 8 | ---.. |
| 9 | ----. |

### 标点符号

| 符号 | 电码 | 符号 | 电码 |
|------|------|------|------|
| . | .-.-.- | , | --..-- |
| ? | ..--.. | ' | .----. |
| ! | -.-.-- | / | -..-. |
| ( | -.--. | ) | -.--.- |
| & | .-... | : | ---... |
| ; | -.-.-. | = | -...- |
| + | .-.-. | - | -....- |
| _ | ..--.- | " | .-..-. |
| $ | ...-..- | @ | .--.-. |

### 常用缩写

| 缩写 | 电码 | 含义 |
|------|------|------|
| SOS | ... --- ... | 求救信号 |
| CQ | -.-. --.- | 呼叫所有台站 |
| DE | -.. . | 来自 |
| K | -.- | 邀请回复 |
| R | .-. | 收到/确认 |
| 73 | --... ...-- | 致意 |
| 88 | ---.. ---.. | 爱与吻 |

## 时间单位标准

国际摩尔斯电码时间单位:

- 点 (dot): 1 单位
- 划 (dash): 3 单位
- 符号内间隔: 1 单位
- 字母间隔: 3 单位
- 单词间隔: 7 单位

默认配置下，点时间为 60ms，完整 SOS 消息约 0.9 秒。

## 示例

### 编码解码

```python
>>> from morse_utils.mod import MorseUtils
>>> utils = MorseUtils()
>>> utils.encode('THE QUICK BROWN FOX')
'- .... . / --.- ..- .. -.-. -.- / -... .-. --- .-- -. / ..-. --- -..-'
>>> utils.decode('- .... . / --.- ..- .. -.-. -.-')
'THE QUICK'
```

### 统计信息

```python
>>> stats = utils.get_statistics('HELLO WORLD')
>>> stats['dot_count']  # 15
>>> stats['dash_count']  # 8
>>> stats['total_symbols']  # 23
>>> stats['duration_seconds']  # ~1.7
```

### 可视化

```python
>>> utils.visualize('SOS', 'standard')
'... --- ...'
>>> utils.visualize('SOS', 'dots')
'••• ——— •••'
>>> utils.visualize('SOS', 'sound')
'di-di-dit da-da-dah di-di-dit'
```

### 练习功能

```python
>>> practice = utils.practice('A')
>>> practice['character']  # 'A'
>>> practice['morse_code']  # '.-'
>>> practice['description']  # 'Alpha - 点划'
>>> practice['mnemonic']  # 'A (点划): a-PART (划比点长)'
```

### 音频生成

```python
>>> generator = MorseAudioGenerator()
>>> audio = generator.generate_audio('SOS')
>>> len(audio)  # WAV 文件大小 (约 50KB)
>>> generator.save_audio('HELLO', 'hello.wav')
```

## 测试

运行测试:

```bash
python Python/morse_utils/morse_utils_test.py
```

测试覆盖:
- 编码功能 (字母/数字/标点/未知字符)
- 解码功能 (标准符号/替代符号)
- 往返一致性
- 音频生成 (格式验证/时序)
- 配置验证
- 统计计算
- 可视化
- 验证功能

## 文件结构

```
Python/morse_utils/
├── mod.py              # 主模块
├── morse_utils_test.py # 测试文件
├── README.md           # 文档
└── examples/
    └── usage_examples.py  # 使用示例
```

## 许可证

MIT License
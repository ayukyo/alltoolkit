# NATO Phonetic Alphabet Utils - 北约音标字母工具

零依赖的北约音标字母工具库，支持文本与北约音标字母之间的编码和解码。

## 功能特性

- ✅ **文本编码**: 将文本转换为北约音标字母
- ✅ **音标解码**: 将北约音标字母解码为文本
- ✅ **多种格式**: 支持默认、编号、表格、音标等输出格式
- ✅ **数字支持**: 支持 0-9 的音标转换
- ✅ **特殊字符**: 支持常见特殊符号的音标转换
- ✅ **呼号验证**: 验证呼号有效性并返回音标拼写
- ✅ **电话号码**: 支持电话号码的音标发音
- ✅ **无线电通信**: 生成标准无线电通话格式
- ✅ **零外部依赖**: 仅使用 Python 标准库

## 安装

将 `nato_phonetic_utils` 目录复制到您的项目中即可使用。

## 快速开始

```python
from nato_phonetic_utils.mod import encode, decode, spell

# 基本编码
encode('SOS')        # 'Sierra Oscar Sierra'
encode('ABC')        # 'Alpha Bravo Charlie'
encode('123')        # 'One Two Three'

# 解码
decode('Alpha Bravo Charlie')  # 'ABC'
decode('One Two Three')        # '123'

# 不同格式拼写
spell('ABC', 'default')   # 'Alpha Bravo Charlie'
spell('ABC', 'numbered')  # '1. Alpha\n2. Bravo\n3. Charlie'
spell('ABC', 'table')     # 'A = Alpha\nB = Bravo\nC = Charlie'
```

## API 文档

### 编码函数

#### `encode(text, separator=' ', include_original=False, skip_unknown=False, unknown_placeholder='?')`

将文本编码为北约音标字母。

**参数:**
- `text` (str): 要编码的文本
- `separator` (str): 字符之间的分隔符，默认为空格
- `include_original` (bool): 是否在输出中包含原始字符
- `skip_unknown` (bool): 是否跳过无法识别的字符
- `unknown_placeholder` (str): 未知字符的占位符

**返回:** 北约音标编码字符串

```python
encode('ABC')                              # 'Alpha Bravo Charlie'
encode('ABC', separator='-')               # 'Alpha-Bravo-Charlie'
encode('ABC', include_original=True)      # 'A-Alpha B-Bravo C-Charlie'
```

### 解码函数

#### `decode(nato_text, separator=None, case_sensitive=False)`

将北约音标字母解码为文本。

**参数:**
- `nato_text` (str): 北约音标文本
- `separator` (str): 输入的分隔符，默认自动检测
- `case_sensitive` (bool): 是否区分大小写

**返回:** 解码后的文本

```python
decode('Alpha Bravo Charlie')  # 'ABC'
decode('alpha bravo charlie')  # 'ABC' (大小写不敏感)
decode('Alpha-Bravo-Charlie', separator='-')  # 'ABC'
```

### 拼写函数

#### `spell(text, format_type='default')`

以指定格式拼写文本。

**格式类型:**
- `'default'`: 默认格式，如 "Alpha Bravo Charlie"
- `'numbered'`: 编号格式，如 "1. Alpha 2. Bravo 3. Charlie"
- `'table'`: 表格格式，如 "A = Alpha"
- `'phonetic'`: 音标格式，如 "A as in Alpha"

```python
spell('ABC', 'default')   # 'Alpha Bravo Charlie'
spell('ABC', 'numbered')  # '1. Alpha\n2. Bravo\n3. Charlie'
spell('ABC', 'table')     # 'A = Alpha\nB = Bravo\nC = Charlie'
spell('ABC', 'phonetic')  # 'A as in Alpha\nB as in Bravo\nC as in Charlie'
```

### 单字符操作

#### `get_nato_word(char)`

获取单个字符对应的北约音标词。

```python
get_nato_word('A')   # 'Alpha'
get_nato_word('5')   # 'Five'
get_nato_word('.')   # 'Decimal'
```

#### `get_char_from_nato(nato_word)`

从北约音标词获取对应的字符。

```python
get_char_from_nato('Alpha')  # 'A'
get_char_from_nato('Five')   # '5'
get_char_from_nato('alpha')  # 'A' (大小写不敏感)
```

#### `is_nato_word(word)`

检查单词是否为有效的北约音标词。

```python
is_nato_word('Alpha')  # True
is_nato_word('Hello')  # False
```

### 实用函数

#### `pronounce_number(number)`

将数字转换为北约音标发音。

```python
pronounce_number(123)    # 'One Two Three'
pronounce_number(3.14)   # 'Three Decimal One Four'
```

#### `pronounce_phone_number(phone)`

将电话号码转换为北约音标发音格式。

```python
pronounce_phone_number('911')              # 'Nine One One'
pronounce_phone_number('+1-555-123-4567')  # 'Plus One Dash Five Five Five...'
```

#### `pronounce_callsign(callsign)`

将呼号转换为北约音标发音格式。

```python
pronounce_callsign('KLM123')  # 'Kilo Lima Mike One Two Three'
```

#### `verify_callsign(callsign)`

验证呼号并返回音标拼写。

```python
valid, spelling = verify_callsign('ABC123')
# valid = True
# spelling = ['Alpha', 'Bravo', 'Charlie', 'One', 'Two', 'Three']
```

#### `text_to_radio_speech(text, include_spelling=False)`

将文本转换为无线电通话格式。

```python
text_to_radio_speech('ABC')                        # 'Alpha Bravo Charlie'
text_to_radio_speech('ABC', include_spelling=True) # 'A as in Alpha, B as in Bravo, C as in Charlie'
```

### NATOConverter 类

面向对象的接口：

```python
from nato_phonetic_utils.mod import NATOConverter

converter = NATOConverter(separator=' ')

converter.encode('ABC')           # 'Alpha Bravo Charlie'
converter.decode('Alpha Bravo')   # 'AB'
converter.spell('ABC')            # 'Alpha Bravo Charlie'
converter.get_word('A')           # 'Alpha'
converter.get_char('Bravo')       # 'B'
converter.is_valid_word('Alpha')  # True
converter.pronounce('ABC')        # 'Alpha Bravo Charlie'
```

## NATO 音标字母表

### 字母

| 字母 | 音标词 | 字母 | 音标词 |
|------|--------|------|--------|
| A | Alpha | N | November |
| B | Bravo | O | Oscar |
| C | Charlie | P | Papa |
| D | Delta | Q | Quebec |
| E | Echo | R | Romeo |
| F | Foxtrot | S | Sierra |
| G | Golf | T | Tango |
| H | Hotel | U | Uniform |
| I | India | V | Victor |
| J | Juliet | W | Whiskey |
| K | Kilo | X | X-ray |
| L | Lima | Y | Yankee |
| M | Mike | Z | Zulu |

### 数字

| 数字 | 音标词 | 数字 | 音标词 |
|------|--------|------|--------|
| 0 | Zero | 5 | Five |
| 1 | One | 6 | Six |
| 2 | Two | 7 | Seven |
| 3 | Three | 8 | Eight |
| 4 | Four | 9 | Nine |

### 特殊符号

| 符号 | 音标词 | 符号 | 音标词 |
|------|--------|------|--------|
| . | Decimal | + | Plus |
| - | Dash | * | Star |
| / | Slash | = | Equals |
| @ | At | # | Hash |

## 使用场景

- 🛫 航空通信
- 🚢 海事通信
- 📻 业余无线电
- 📞 电话客服
- 🔤 拼写确认
- 🔐 密码朗读

## 运行测试

```bash
cd nato_phonetic_utils
python nato_phonetic_utils_test.py
```

## 运行示例

```bash
cd nato_phonetic_utils
python examples/basic_usage.py
python examples/radio_communication.py
```

## 许可证

MIT License

## 作者

AllToolkit
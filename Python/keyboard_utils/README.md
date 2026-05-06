# Keyboard Utils - 键盘布局工具库

多键盘布局支持、按键距离计算、打字分析、效率评分。零外部依赖，纯 Python 标准库实现。

## 功能特性

### 键盘布局支持
- **QWERTY** - 标准美式布局
- **Dvorak** - Dvorak 简化键盘布局
- **Colemak** - Colemak 现代优化布局
- **AZERTY** - 法语键盘布局
- **QWERTZ** - 德语键盘布局

### 核心功能
- 📍 **按键位置查询** - 获取任意字符的行、列、手指、手信息
- 📏 **距离计算** - 欧几里得距离，支持单键和文本总行程
- 📊 **打字分析** - 手交替、手指使用、行分布、滚动序列
- 🎯 **效率评分** - 综合打字效率分数（0-100分）
- 🔍 **模式检测** - 连续键、同指序列、直线模式
- 💡 **改进建议** - 针对低效序列提供优化建议

## 安装使用

```python
from keyboard_utils import KeyboardUtils, distance, analyze, efficiency_score

# 创建工具实例
ku = KeyboardUtils("qwerty")

# 或使用便捷函数
dist = distance('a', 's')  # 计算两键距离
analysis = analyze("hello")  # 分析文本
score = efficiency_score("asdf")  # 效率评分
```

## API 参考

### KeyboardUtils 类

```python
from keyboard_utils import KeyboardUtils

ku = KeyboardUtils("qwerty")  # 支持: qwerty, dvorak, colemak, azerty, qwertz
```

#### 布局查询

```python
# 获取按键位置
pos = ku.layout.get_key_position('a')
# KeyPosition(key='a', row=2, col=1, finger=Finger.LEFT_PINKY, hand=Hand.LEFT)

# 获取坐标
x, y = ku.layout.get_coordinates('a')  # (1.25, 2.0)

# 获取手指
finger = ku.layout.get_finger('a')  # Finger.LEFT_PINKY

# 获取手
hand = ku.layout.get_hand('a')  # Hand.LEFT
```

#### 距离计算

```python
# 两键距离
dist = ku.distance('a', 's')  # 约 1.0 键宽

# 文本总行程
total = ku.total_distance("hello")  # 约 12.5 键宽
```

#### 打字分析

```python
analysis = ku.analyze("the quick brown fox")

# 分析结果
analysis.total_distance      # 总行程距离
analysis.average_distance    # 平均每键距离
analysis.hand_alternations   # 手交替次数
analysis.same_hand_sequences # 同手连续次数
analysis.finger_usage        # 各手指使用次数
analysis.hand_usage          # 各手使用次数
analysis.rolling_sequences   # 滚动序列数
analysis.home_row_usage      # 基准行使用次数
analysis.top_row_usage       # 上行使用次数
analysis.bottom_row_usage    # 下行使用次数
analysis.number_row_usage    # 数字行使用次数
```

#### 布局判断

```python
ku.is_home_row('a')       # True (基准行)
ku.is_top_row('q')        # True (上行)
ku.is_bottom_row('z')     # True (下行)
ku.is_number_row('1')     # True (数字行)
ku.is_same_hand('a', 's') # True (同手)
ku.is_same_finger('a', 'q') # True (同指)
ku.is_adjacent_finger('a', 's') # True (相邻手指)
ku.is_consecutive('a', 's') # True (相邻键)
```

#### 模式检测

```python
patterns = ku.get_keyboard_patterns("asd")

# 返回模式列表
# [{"type": "consecutive", "start": 0, "end": 1, "chars": "as"}, ...]
# 类型: consecutive, same_finger, straight_line
```

#### 效率评分

```python
score = ku.get_efficiency_score("asdfjkl;")  # 0-100分
# 基于: 基准行使用率、手交替率、行程距离、滚动序列
```

#### 改进建议

```python
suggestions = ku.suggest_alternatives("aq")

# 返回建议列表
# [{"type": "same_finger", "message": "...", ...}]
# 类型: same_finger, long_jump, double_pinky
```

### 便捷函数

```python
from keyboard_utils import (
    distance,         # 两键距离
    total_distance,   # 文本总距离
    analyze,          # 打字分析
    get_key_position, # 按键位置
    get_coordinates,  # 按键坐标
    get_finger,       # 手指
    get_hand,         # 手
    efficiency_score, # 效率评分
    get_keyboard_patterns,  # 模式检测
    suggest_improvements,    # 改进建议
    available_layouts,       # 可用布局
)

distance('a', 's')              # 1.0
total_distance("hello")         # 12.5
analysis = analyze("test")
score = efficiency_score("asdf")
layouts = available_layouts()  # ['qwerty', 'dvorak', 'colemak', 'azerty', 'qwertz']
```

### 枚举类型

```python
from keyboard_utils import Finger, Hand

# 手指
Finger.LEFT_PINKY   # 左小指
Finger.LEFT_RING    # 左无名指
Finger.LEFT_MIDDLE  # 左中指
Finger.LEFT_INDEX   # 左食指
Finger.LEFT_THUMB   # 左拇指
Finger.RIGHT_THUMB  # 右拇指
Finger.RIGHT_INDEX  # 右食指
Finger.RIGHT_MIDDLE # 右中指
Finger.RIGHT_RING   # 右无名指
Finger.RIGHT_PINKY  # 右小指

# 手
Hand.LEFT   # 左手
Hand.RIGHT  # 右手
Hand.BOTH   # 双手（拇指）
```

## 使用示例

### 比较不同布局效率

```python
from keyboard_utils import KeyboardUtils

text = "the quick brown fox jumps over the lazy dog"
for layout in ["qwerty", "dvorak", "colemak"]:
    ku = KeyboardUtils(layout)
    score = ku.get_efficiency_score(text)
    analysis = ku.analyze(text)
    print(f"{layout}: 评分={score:.1f}, 基准行={analysis.home_row_usage}")
```

### 分析密码键盘特征

```python
from keyboard_utils import KeyboardUtils

ku = KeyboardUtils("qwerty")
password = "qwerty123"

patterns = ku.get_keyboard_patterns(password)
analysis = ku.analyze(password)
score = ku.get_efficiency_score(password)

print(f"效率评分: {score}")
print(f"键盘模式: {len(patterns)}")
print(f"行程距离: {analysis.total_distance}")
```

### 手指工作负荷分析

```python
from keyboard_utils import KeyboardUtils, Finger

ku = KeyboardUtils("qwerty")
analysis = ku.analyze("programming")

for finger in [Finger.LEFT_PINKY, Finger.LEFT_INDEX, Finger.RIGHT_INDEX, Finger.RIGHT_PINKY]:
    count = analysis.finger_usage.get(finger, 0)
    print(f"{finger.value}: {count}")
```

## 设计原理

### 距离计算
使用欧几里得距离，单位为键宽（约19mm）：
- 同行相邻键：约1.0键宽
- 跨行相邻键：约1.12键宽
- 行偏移：上行偏移0.25，中行偏移0.5，下行偏移0.75

### 效率评分
综合四个指标：
1. **基准行使用率** (30%) - 越高越好
2. **手交替率** (30%) - 越高越好
3. **行程距离** (30%) - 越短越好
4. **滚动序列** (10%) - 越多越好

### 手指分配
标准触控打字指法：
- 左小指: a, q, z, 1, !
- 左无名指: s, w, x, 2, @
- 左中指: d, e, c, 3, #
- 左食指: f, g, r, t, v, b, 4, 5
- 右食指: j, h, u, y, m, n, 6, 7
- 右中指: k, i, ,, 8, *
- 右无名指: l, o, ., 9, (
- 右小指: ;, p, /, 0, ), -, =

## 测试

```bash
python test.py
```

共 80+ 单元测试，覆盖所有主要功能。

## 许可证

MIT License
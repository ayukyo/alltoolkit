# Cellular Automata Utils

元胞自动机工具包 - 提供多种经典元胞自动机的实现。

## 功能

### 生命游戏变体
- **GameOfLife** - 康威生命游戏
- **HighLife** - 带复制子规则
- **Seeds** - 爆炸性增长
- **DayAndNight** - 黑白对称规则
- **CustomLife** - 自定义 B/S 规则

### 一维元胞自动机
- **ElementaryCA** - 沃尔夫勒姆初等元胞自动机 (Rule 0-255)

### 蚂蚁规则
- **LangtonsAnt** - 兰顿蚂蚁
- **MultiColorAnt** - 多色蚂蚁扩展

### 多态元胞自动机
- **BriansBrain** - 三态大脑
- **Wireworld** - 电子电路模拟

## 使用示例

```python
from cellular_automata_utils.mod import GameOfLife, ElementaryCA

# 生命游戏
gol = GameOfLife(20, 20)
gol.add_glider(0, 0)
gol.evolve(10)
print(gol.to_string())

# 初等元胞自动机 - Rule 90 (谢尔宾斯基三角形)
ca = ElementaryCA(63, rule=90)
ca.initialize_single()
history = ca.run_with_history(31)
print(ca.to_string_history())
```

## 经典图案

### GameOfLife
- `add_glider()` - 滑翔机
- `add_blinker()` - 闪烁器
- `add_pulsar()` - 脉冲星
- `add_gosper_glider_gun()` - 高斯帕滑翔机枪

### ElementaryCA 著名规则
- Rule 30 - 混沌图案
- Rule 90 - 谢尔宾斯基三角形
- Rule 110 - 图灵完备
- Rule 184 - 交通流模型

## 零外部依赖

纯 Python 标准库实现，无需任何第三方包。

## 测试

```bash
python cellular_automata_utils_test.py
```

## 作者

AllToolkit

## 日期

2026-04-24
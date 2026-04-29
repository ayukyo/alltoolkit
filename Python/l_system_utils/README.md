# l_system_utils - L-系统（Lindenmayer 系统）工具

[![Test Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen)](./l_system_utils_test.py)

零依赖的 L-系统工具，用于生成分形、植物结构和复杂图案。

## 特性

- **确定性 L-系统**: D0L 系统（最常见类型）
- **随机 L-系统**: 带概率权重的规则
- **上下文敏感 L-系统**: 规则依赖相邻字符
- **参数化 L-系统**: 带条件和参数的规则
- **龟标图形解释**: 生成可视化坐标点
- **内置经典分形**: Koch 曲线、Sierpinski、Dragon 等
- **零依赖**: 纯 Python 实现

## 安装

```python
from l_system_utils import LSystem, LSystemRule, TurtleState
```

## 快速开始

### Koch 曲线

```python
from l_system_utils import LSystem

# 创建 Koch 曲线 L-系统
lsystem = LSystem(
    axiom="F",
    rules={"F": "F+F-F-F+F"},
    angle=90
)

# 生成 4 次迭代
result = lsystem.generate(iterations=4)

# 解释为龟标图形
points = lsystem.interpret(result, step=10)
print(f"生成 {len(points)} 个点")
```

### Sierpinski 三角形

```python
from l_system_utils import LSystem

lsystem = LSystem(
    axiom="F-G-G",
    rules={"F": "F-G+F+G-F", "G": "GG"},
    angle=120
)

result = lsystem.generate(iterations=6)
points = lsystem.interpret(result)
```

### 龙曲线

```python
from l_system_utils import LSystem

lsystem = LSystem(
    axiom="FX",
    rules={"X": "X+YF+", "Y": "-FX-Y"},
    angle=90
)

result = lsystem.generate(iterations=12)
```

### 随机 L-系统

```python
from l_system_utils import LSystem

# 带概率的规则
lsystem = LSystem(
    axiom="F",
    rules={"F": {"F+F": 0.5, "F-F": 0.5}},
    angle=90,
    system_type="stochastic"
)

# 每次生成结果不同
result1 = lsystem.generate(iterations=5)
result2 = lsystem.generate(iterations=5)
```

### 植物结构

```python
from l_system_utils import LSystem

# 简单植物
plant = LSystem(
    axiom="X",
    rules={"X": "F[+X]F[-X]+X", "F": "FF"},
    angle=25
)

result = plant.generate(iterations=5)
points = plant.interpret(result, step=5)
```

## 内置经典 L-系统

```python
from l_system_utils import get_classic_lsystem

# 获取经典分形
koch = get_classic_lsystem("koch")
sierpinski = get_classic_lsystem("sierpinski")
dragon = get_classic_lsystem("dragon")
hilbert = get_classic_lsystem("hilbert")
plant = get_classic_lsystem("plant")

# 直接生成
result = koch.generate(iterations=4)
```

## API 参考

### LSystem 类

```python
LSystem(axiom, rules, angle=90, step=10, system_type="deterministic")
```

**参数:**
- `axiom`: 初始字符串
- `rules`: 规则字典
- `angle`: 转向角度（度）
- `step`: 前进步长
- `system_type`: 系统类型

**方法:**

| 方法 | 说明 |
|-----|------|
| `generate(iterations)` | 迭代生成字符串 |
| `interpret(string, step)` | 解释为坐标点 |
| `get_rules()` | 获取规则 |
| `set_rule(predecessor, successor)` | 设置规则 |

### LSystemRule 数据类

```python
LSystemRule(predecessor, successor, left_context="", right_context="")
```

### TurtleState 数据类

龟标图形状态，包含：
- `x, y`: 当前位置
- `angle`: 当前角度
- `stack`: 状态栈

## 龟标图形解释

| 符号 | 动作 |
|-----|------|
| `F` | 前进并画线 |
| `f` | 前进不画线 |
| `+` | 左转 angle 度 |
| `-` | 右转 angle 度 |
| `[` | 保存状态（入栈） |
| `]` | 恢复状态（出栈） |
| `X, Y` | 不绘制（用于规则） |

## 经典 L-系统列表

| 名称 | 描述 |
|------|------|
| `koch` | Koch 曲线 |
| `koch_snowflake` | Koch 雪花 |
| `sierpinski` | Sierpinski 三角形 |
| `sierpinski_carpet` | Sierpinski 地毯 |
| `dragon` | 龙曲线 |
| `hilbert` | Hilbert 曲线 |
| `levy_c` | Lévy C 曲线 |
| `plant` | 简单植物结构 |
| `tree` | 分形树 |
| `bush` | 灌木结构 |

## 测试

```bash
python -m pytest l_system_utils_test.py -v
```

## 许可证

MIT License
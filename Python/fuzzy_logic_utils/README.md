# Fuzzy Logic Utils 🌫️

模糊逻辑工具，提供隶属函数和模糊推理系统。

## 特性

- ✅ **隶属函数** - 三角、梯形、高斯、sigmoid 等
- ✅ **模糊推理** - Mamdani 风格推理
- ✅ **规则评估** - 模糊规则执行
- ✅ **去模糊化** - 重心法、最大值法
- ✅ **零依赖** - 仅使用 Python 标准库

## 快速开始

```python
from fuzzy_logic_utils import FuzzyVariable, FuzzySystem

# 定义模糊变量
temperature = FuzzyVariable("temperature")
temperature.add_triangular("cold", 0, 0, 20)
temperature.add_triangular("warm", 15, 25, 35)
temperature.add_triangular("hot", 30, 40, 50)

# 创建系统
system = FuzzySystem()
system.add_input(temperature)
system.add_rule("IF temperature IS hot THEN fan IS high")
```

## API 参考

| 类 | 说明 |
|---|---|
| `FuzzyVariable` | 模糊变量 |
| `FuzzySystem` | 模糊推理系统 |
| `MembershipFunction` | 隶属函数基类 |

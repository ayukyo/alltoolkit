# Temperature Utils


Temperature Utils - 温度转换工具

零依赖的温度转换库，支持：
- 摄氏度(Celsius)、华氏度(Fahrenheit)、开尔文(Kelvin)、兰氏度(Rankine)
- 批量转换
- 温度范围验证
- 常见温度参考点
- 温度比较和运算

Author: AllToolkit
License: MIT


## 功能

### 类

- **TemperatureUnit**: 温度单位枚举
- **TemperatureError**: 温度相关错误的基类
- **InvalidTemperatureError**: 无效的温度值（低于绝对零度）
- **InvalidUnitError**: 无效的温度单位

### 函数

- **celsius_to_fahrenheit(celsius**) - 摄氏度 → 华氏度
- **celsius_to_kelvin(celsius**) - 摄氏度 → 开尔文
- **celsius_to_rankine(celsius**) - 摄氏度 → 兰氏度
- **fahrenheit_to_celsius(fahrenheit**) - 华氏度 → 摄氏度
- **fahrenheit_to_kelvin(fahrenheit**) - 华氏度 → 开尔文
- **fahrenheit_to_rankine(fahrenheit**) - 华氏度 → 兰氏度
- **kelvin_to_celsius(kelvin**) - 开尔文 → 摄氏度
- **kelvin_to_fahrenheit(kelvin**) - 开尔文 → 华氏度
- **kelvin_to_rankine(kelvin**) - 开尔文 → 兰氏度
- **rankine_to_celsius(rankine**) - 兰氏度 → 摄氏度

... 共 32 个函数

## 使用示例

```python
from mod import celsius_to_fahrenheit

# 使用 celsius_to_fahrenheit
result = celsius_to_fahrenheit()
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

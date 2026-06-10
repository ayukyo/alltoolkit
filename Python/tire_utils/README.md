# Tire Utils - 轮胎参数工具

轮胎规格参数解析与转换工具，零依赖。

## 功能特性

- **规格解析**: 解析轮胎尺寸字符串（如 205/55R16）
- **参数计算**: 计算直径、周长、接地面积等
- **单位转换**: mm/inch 互换
- **尺寸匹配**: 检查轮毂兼容性和速度等级

## 快速开始

```python
from tire_utils.mod import parse_tire_size, calculate_diameter

# 解析轮胎规格
tire = parse_tire_size("205/55R16")
print(tire.width)   # 205
print(tire.aspect_ratio)  # 55
print(tire.rim_diameter)  # 16

# 计算直径
diameter = calculate_diameter("205/55R16")
print(f"直径: {diameter:.2f} mm")
```

## API 参考

| 函数 | 说明 |
|------|------|
| `parse_tire_size(size_str)` | 解析轮胎规格字符串 |
| `calculate_diameter(size_str)` | 计算直径(mm) |
| `calculate_circumference(size_str)` | 计算周长(mm) |
| `speed_rating(load_index, speed_rating)` | 获取速度等级信息 |
| `validate_tire_size(size_str)` | 验证规格是否有效 |

---

**测试覆盖**: 53 passed
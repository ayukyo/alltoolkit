# Wind Scale Utils 💨

风级和风寒计算工具，支持蒲福风级和风寒指数。

## 特性

- ✅ **蒲福风级** - 0-17 级风速描述
- ✅ **风速转换** - km/h, m/s, knots, mph
- ✅ **风寒指数** - 体感温度计算
- ✅ **风玫瑰图** - 风向频率数据
- ✅ **零依赖** - 仅使用 Python 标准库

## 快速开始

```python
from wind_scale_utils import beaufort_scale, wind_speed_convert, wind_chill

# 蒲福风级
description = beaufort_scale(5)
print(description)  # {'knots': 17, 'description': 'Fresh breeze'}

# 风速转换
kmh = wind_speed_convert(10, from_unit="m/s", to_unit="km/h")
print(kmh)  # 36.0

# 风寒指数
wc = wind_chill(temperature=-10, wind_speed=20)
print(wc)  # -17.5 (体感温度)
```

## API 参考

| 函数 | 说明 |
|------|------|
| `beaufort_scale(knots)` | 蒲福风级 |
| `wind_speed_convert(value, from_unit, to_unit)` | 风速转换 |
| `wind_chill(temperature, wind_speed)` | 风寒指数 |
| `wind_rose(data)` | 风玫瑰图数据 |

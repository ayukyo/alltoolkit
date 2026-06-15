# Beer Utils 🍺

啤酒酿造工具，计算酒精度、苦度、色度等酿造参数。

## 特性

- ✅ **ABV 计算** - 酒精度计算
- ✅ **IBU 计算** - 国际苦度单位
- ✅ **SRM 色度** - 啤酒颜色计算
- ✅ **OG/FG** - 原始/最终比重
- ✅ ** Plato 转换** - 比标转换
- ✅ **零依赖** - 仅使用 Python 标准库

## 快速开始

```python
from beer_utils import calculate_abv, calculate_ibu, srm_to_rgb

# 酒精度
abv = calculate_abv(og=1.050, fg=1.010)
print(f"ABV: {abv:.1f}%")  # 5.3%

# 苦度 IBU
ibu = calculate_ibu(alpha_acid=0.05, grams=10, volume=20, og=1.050)
print(f"IBU: {ibu:.1f}")  # ~20

# 色度颜色
rgb = srm_to_rgb(10)
print(rgb)  # (255, 198, 76)
```

## API 参考

| 函数 | 说明 |
|------|------|
| `calculate_abv(og, fg)` | 计算酒精度 |
| `calculate_ibu(alpha, grams, volume, og)` | 计算苦度 |
| `srm_to_rgb(srm)` | SRM 转 RGB |
| `plato_to_sg(plato)` | Plato 转比重 |
| `calculate_attenuation(og, fg)` | 发酵度 |

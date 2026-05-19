# Cocktail Utils 🍹

**鸡尾酒配方工具库 - 零依赖，生产就绪**

经典鸡尾酒数据库，包含搜索、筛选、酒精度计算、购物清单生成等功能。

---

## ✨ 功能特性

- **经典鸡尾酒数据库** - 40+ 款 IBA 官方及经典鸡尾酒配方
- **多维度搜索** - 按名称、原料、基酒、口味、酒杯筛选
- **智能推荐** - 相似鸡尾酒推荐、菜品配对建议
- **酒精度计算** - 自动计算混合饮料酒精度
- **购物清单** - 批量生成原料清单，支持份数计算
- **派对估算** - 智能估算派对所需饮料量
- **容量转换** - 支持多种单位互转 (ml, oz, cl, l, tbsp, tsp)
- **零依赖** - 仅使用 Python 标准库

---

## 🚀 快速开始

```python
from cocktail_utils.mod import (
    get_cocktail_by_name,
    get_random_cocktail,
    format_recipe,
)

# 搜索鸡尾酒
martini = get_cocktail_by_name("Martini")
print(martini.name_zh)  # 马天尼
print(martini.abv)      # 36.4%

# 打印完整配方
print(format_recipe(martini))

# 随机推荐
random_cocktail = get_random_cocktail()
print(f"今日推荐: {random_cocktail.name_zh}")
```

---

## 📚 主要功能

### 1. 搜索鸡尾酒

```python
# 按名称搜索 (支持中英文)
martini = get_cocktail_by_name("Martini")
mojito = get_cocktail_by_name("莫吉托")

# 搜索包含特定原料的鸡尾酒
vodka_cocktails = search_cocktails("vodka")

# 按原料筛选
lime_cocktails = get_cocktails_by_ingredient("lime juice")
```

### 2. 筛选鸡尾酒

```python
from cocktail_utils.mod import SpiritType, Flavor, GlassType

# 按基酒筛选
gin_cocktails = get_cocktails_by_spirit(SpiritType.GIN)
rum_cocktails = get_cocktails_by_spirit(SpiritType.RUM)

# 按口味筛选
sweet_cocktails = get_cocktails_by_flavor(Flavor.SWEET)
sour_cocktails = get_cocktails_by_flavor(Flavor.SOUR)

# 按酒杯类型筛选
martini_glass = get_cocktails_by_glass(GlassType.MARTINI)

# 按酒精度范围筛选
low_abv = get_cocktails_by_abv_range(0, 15)   # 低度 (<15%)
high_abv = get_cocktails_by_abv_range(30, 50) # 高度 (>30%)

# 简单易做鸡尾酒
easy_cocktails = get_easy_cocktails()  # 难度 <= 2
```

### 3. 随机推荐

```python
# 随机一个
cocktail = get_random_cocktail()

# 随机多个
cocktails = get_random_cocktails(5)
```

### 4. 相似推荐

```python
# 推荐相似鸡尾酒
negroni = get_cocktail_by_name("Negroni")
similar = suggest_similar_cocktails(negroni)

for cocktail, score in similar:
    print(f"{cocktail.name_zh}: 相似度 {score:.2f}")
```

### 5. 购物清单

```python
# 为多种鸡尾酒生成购物清单
cocktails = [
    get_cocktail_by_name("Mojito"),
    get_cocktail_by_name("Daiquiri"),
    get_cocktail_by_name("Piña Colada"),
]

shopping = generate_shopping_list(cocktails)
print(format_shopping_list(shopping, servings=10))
```

### 6. 派对估算

```python
# 估算派对所需饮料
estimate = estimate_drinks_for_party(50, 3)
print(f"总饮品数: {estimate['total_drinks']}")
print(f"总容量: {estimate['total_liters']} 升")
print(f"建议鸡尾酒种类: {estimate['suggested_cocktails']}")
```

### 7. 酒精度计算

```python
# 计算自定义混合饮料酒精度
ingredients = [
    {"name": "Vodka", "amount_ml": 50, "abv": 40},
    {"name": "Juice", "amount_ml": 100, "abv": 0},
]
abv = calculate_abv(ingredients)  # 13.3%

# 鸡尾酒自动计算
martini = get_cocktail_by_name("Martini")
print(martini.abv)  # 36.4%

# 酒精度描述
print(get_abv_description(10))  # "中等 🟡"
```

### 8. 容量转换

```python
# 单位转换
oz = convert_volume(60, "ml", "oz")  # 2.03 oz
ml = convert_volume(1.5, "oz", "ml") # 44.36 ml

# 支持多种单位: ml, oz, cl, l, tbsp, tsp, dash, drop
```

### 9. 菜品配对

```python
# 根据菜品推荐鸡尾酒
seafood_pairing = get_pairing_suggestion("seafood")
meat_pairing = get_pairing_suggestion("meat")
spicy_pairing = get_pairing_suggestion("spicy")

# 支持: seafood, meat, spicy, dessert, cheese, salad, bbq, asian, italian, mexican
```

### 10. IBA 官方鸡尾酒

```python
# 获取所有 IBA 官方鸡尾酒
iba_cocktails = get_iba_cocktails()

# 按分类筛选
unforgettables = get_cocktails_by_iba_category("Unforgettables")
contemporary = get_cocktails_by_iba_category("Contemporary")
```

---

## 📊 数据统计

```python
stats = get_statistics()

print(f"总鸡尾酒数: {stats['total_cocktails']}")
print(f"IBA 官方: {stats['iba_cocktails']}")
print(f"平均酒精度: {stats['avg_abv']}%")
print(f"基酒分布: {stats['spirits_distribution']}")
```

---

## 🍹 经典鸡尾酒列表

### 马天尼家族
| 名称 | 中文名 | 基酒 | 酒精度 |
|------|--------|------|--------|
| Martini | 马天尼 | Gin | 36.4% |
| Dirty Martini | 脏马天尼 | Gin | 32.7% |
| Vodka Martini | 伏特加马天尼 | Vodka | 36.4% |

### 酸酒家族
| 名称 | 中文名 | 基酒 | 酒精度 |
|------|--------|------|--------|
| Margarita | 玛格丽特 | Tequila | 33.3% |
| Daiquiri | 黛琪莉 | Rum | 24% |
| Whiskey Sour | 威士忌酸 | Whiskey | 24% |
| Sidecar | 侧车 | Cognac | 31.3% |

### 高球系列
| 名称 | 中文名 | 基酒 | 酒精度 |
|------|--------|------|--------|
| Mojito | 莫吉托 | Rum | ~13% |
| Moscow Mule | 莫斯科骡子 | Vodka | ~12% |
| Gin Tonic | 金汤力 | Gin | ~8% |

### 热带风情
| 名称 | 中文名 | 基酒 | 精度 |
|------|--------|------|--------|
| Piña Colada | 椰林飘香 | Rum | ~16% |
| Mai Tai | 迈泰 | Rum | ~27% |
| Hurricane | 飓风 | Rum | ~20% |

### 经典名酒
| 名称 | 中文名 | 基酒 | 酒精度 |
|------|--------|------|--------|
| Old Fashioned | 古典鸡尾酒 | Whiskey | ~32% |
| Negroni | 尼格罗尼 | Gin | 26.5% |
| Manhattan | 曼哈顿 | Whiskey | 32.3% |

---

## 🔬 测试

```bash
# 运行测试
python Python/cocktail_utils/cocktail_utils_test.py

# 测试覆盖:
# - 数据完整性验证
# - 搜索功能测试
# - 筛选功能测试
# - 随机推荐测试
# - 购物清单测试
# - 酒精度计算测试
# - 容量转换测试
# - 相似推荐测试
# - 边界值测试
```

---

## 📁 文件结构

```
Python/cocktail_utils/
├── mod.py                 # 主模块 (50KB)
├── cocktail_utils_test.py # 测试文件 (25KB, 100+ 测试)
├── README.md              # 文档
└── examples/
    └── usage_examples.py  # 使用示例
```

---

## 📋 IBA 分类说明

- **The Unforgettables** - IBA 官方经典鸡尾酒
- **Contemporary Classics** - 当代经典
- **New Era Drinks** - 新时代饮品

---

## 🌍 适用场景

- 🍹 家庭酒吧管理
- 📖 尾酒配方查询
- 🛒 派对购物清单
- 🎉 酒吧经营辅助
- 📱 鸡尾酒 App 开发
- 🍽️ 菜品配对推荐

---

## 📝 更新日志

- **2026-05-19**: 初始版本发布
  - 40+ 经典鸡尾酒配方
  - 完整搜索筛选功能
  - 智能推荐系统
  - 购物清单生成
  - 派对估算功能
  - 100+ 测试用例

---

**License**: MIT

**作者**: AllToolkit 自动生成
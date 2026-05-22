# Decision Matrix Utils - 加权决策矩阵工具

**多准则决策分析工具 - 支持多种评分方法**

## 功能特性

- ✅ **决策矩阵创建** - 灵活定义选项和评价标准
- ✅ **加权评分计算** - 支持多种评分方法
- ✅ **敏感性分析** - 观察权重变化对结果的影响
- ✅ **雷达图数据** - 生成可视化数据
- ✅ **JSON导入导出** - 便于存储和共享
- ✅ **预定义模板** - 购车、工作选择、购房等常用模板

## 支持的评分方法

| 方法 | 说明 |
|------|------|
| WEIGHTED_AVERAGE | 加权平均法（归一化分数后加权） |
| WEIGHTED_SUM | 加权求和法（直接加权） |
| TOPSIS | 理想解相似排序法 |
| AHP_SIMPLIFIED | 简化层次分析法 |

## 快速开始

### 1. 基本使用

```python
from mod import DecisionMatrix, CriteriaType

# 创建决策矩阵
matrix = DecisionMatrix(name="产品选择")

# 添加评价标准
matrix.add_criteria_simple("价格", 0.3, CriteriaType.COST)    # 成本型
matrix.add_criteria_simple("质量", 0.5, CriteriaType.BENEFIT) # 效益型
matrix.add_criteria_simple("服务", 0.2, CriteriaType.BENEFIT)

# 添加选项
matrix.add_option_simple("产品A", {"价格": 100, "质量": 85, "服务": 90})
matrix.add_option_simple("产品B", {"价格": 80, "质量": 90, "服务": 80})
matrix.add_option_simple("产品C", {"价格": 120, "质量": 95, "服务": 85})

# 计算结果
results = matrix.calculate()

# 输出排名
for r in results:
    print(f"{r.rank}. {r.option_name}: {r.total_score:.4f}")
```

### 2. 使用预定义模板

```python
from mod import DecisionTemplates

# 购车决策模板
car_matrix = DecisionTemplates.car_purchase()

# 工作选择模板
job_matrix = DecisionTemplates.job_selection()

# 购房决策模板
house_matrix = DecisionTemplates.house_purchase()

# 产品对比模板
product_matrix = DecisionTemplates.product_comparison()

# 旅游目的地模板
travel_matrix = DecisionTemplates.travel_destination()
```

### 3. 快速比较函数

```python
from mod import compare_options

results = compare_options(
    criteria=[
        ("性价比", 0.4, "benefit"),
        ("品质", 0.3, "benefit"),
        ("服务", 0.3, "benefit")
    ],
    options={
        "选项A": {"性价比": 90, "品质": 85, "服务": 80},
        "选项B": {"性价比": 70, "品质": 90, "服务": 85}
    }
)

print(f"推荐: {results[0].option_name}")
```

### 4. 敏感性分析

```python
# 分析权重变化对结果的影响
sensitivity = matrix.sensitivity_analysis("价格", weight_range=(0.1, 0.9))

for weight, winner in sensitivity.winner_changes:
    print(f"权重 {weight:.2f} -> 获胜者: {winner}")
```

### 5. 雷达图数据

```python
radar = matrix.get_radar_chart_data()

# 输出格式
{
    "labels": ["价格", "质量", "服务"],
    "datasets": [
        {"label": "产品A", "data": [75, 85, 90]},
        {"label": "产品B", "data": [90, 90, 80]}
    ],
    "weights": {"价格": 30, "质量": 50, "服务": 20}
}
```

## 核心类说明

### DecisionMatrix

决策矩阵主类，管理选项和标准。

| 方法 | 说明 |
|------|------|
| `add_criteria(criteria)` | 添加评价标准 |
| `add_criteria_simple(name, weight, type)` | 简化添加标准 |
| `add_option(option)` | 添加选项 |
| `add_option_simple(name, scores)` | 简化添加选项 |
| `set_score(option, criteria, score)` | 设置分数 |
| `calculate(method)` | 计算决策结果 |
| `get_winner()` | 获取最优选项 |
| `get_ranking()` | 获取排名列表 |
| `sensitivity_analysis(criteria)` | 敏感性分析 |
| `get_radar_chart_data()` | 生成雷达图数据 |
| `to_report()` | 生成文本报告 |
| `to_json()` | 导出JSON |
| `from_json(json_str)` | 从JSON导入 |

### Criteria

评价标准类。

| 属性 | 说明 |
|------|------|
| `name` | 标准名称 |
| `weight` | 权重 |
| `criteria_type` | 类型（BENEFIT/COST） |
| `description` | 描述 |

### Option

选项类。

| 属性 | 说明 |
|------|------|
| `name` | 选项名称 |
| `description` | 描述 |
| `scores` | 各标准分数 |
| `metadata` | 额外元数据 |

### DecisionResult

决策结果类。

| 属性 | 说明 |
|------|------|
| `option_name` | 选项名称 |
| `total_score` | 总得分 |
| `normalized_score` | 归一化得分 |
| `rank` | 排名 |
| `criteria_scores` | 各标准归一化得分 |
| `weighted_scores` | 各标准加权得分 |

## 标准类型

- **BENEFIT（效益型）**：数值越大越好（如质量、性能）
- **COST（成本型）**：数值越小越好（如价格、时间）

## 评分方法详解

### WEIGHTED_AVERAGE（加权平均法）

最常用的方法，将分数归一化到0-1后加权平均。

特点：
- 分数会被归一化处理
- 适合不同量纲的标准
- 结果稳定可靠

### TOPSIS（理想解相似排序法）

计算每个选项与理想解的距离，选择最接近理想解的选项。

特点：
- 考虑正理想解和负理想解
- 适合多属性决策
- 对极端值敏感

### AHP_SIMPLIFIED（简化层次分析法）

使用几何平均计算综合得分。

特点：
- 适合权重差异大的情况
- 对低分标准惩罚更重
- 简化版不需要两两比较矩阵

## 实际应用场景

| 场景 | 模板 |
|------|------|
| 购车决策 | `DecisionTemplates.car_purchase()` |
| 工作选择 | `DecisionTemplates.job_selection()` |
| 购房决策 | `DecisionTemplates.house_purchase()` |
| 产品对比 | `DecisionTemplates.product_comparison()` |
| 旅游选择 | `DecisionTemplates.travel_destination()` |

## 测试

```bash
python decision_matrix_utils_test.py
```

## 示例

```bash
python examples/usage_examples.py
```

## 零依赖

仅使用 Python 标准库：
- `math` - 数学运算
- `dataclasses` - 数据类
- `typing` - 类型提示
- `enum` - 枚举
- `json` - JSON处理

## 许可证

MIT License
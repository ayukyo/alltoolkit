# stress_utils - 压力评估工具模块

综合压力评估和管理工具，基于感知压力量表 (PSS) 设计。零外部依赖，纯 Python 实现。

## 功能列表

| 功能 | 说明 |
|------|------|
| 压力指数计算 | 基于 PSS 的科学压力评估 |
| 压力等级分类 | 5 级压力等级（极低、低、中等、高、极高） |
| 个人化减压建议 | 根据压力类型提供针对性建议 |
| 压力类型识别 | 工作压力、生活压力、健康压力等 |
| 压力历史追踪 | 历史记录与趋势分析 |
| 压力因素权重系统 | 多维度压力因素评估 |
| 职业倦怠风险评估 | Burnout 风险预警 |
| 恢复建议生成 | 根据压力模式生成恢复建议 |

## 快速使用

```python
from stress_utils.mod import (
    StressAssessment,
    StressLevel,
    StressType,
    calculate_stress_index,
    get_stress_recommendations,
    quick_stress_check
)

# 快速压力检查
result = quick_stress_check(
    sleep_quality=3,      # 睡眠质量 (1-5)
    work_pressure=4,      # 工作压力 (1-5)
    life_pressure=3,      # 生活压力 (1-5)
    health_status=4       # 健康状态 (1-5)
)
print(f"压力指数: {result['index']}")
print(f"压力等级: {result['level']}")
print(f"建议: {result['recommendations']}")

# 详细压力评估
assessment = StressAssessment()

# 添加压力因素
assessment.add_factor('work', 'workload', 80)  # 工作量压力 80%
assessment.add_factor('work', 'deadline', 70)  # 截止日期压力 70%
assessment.add_factor('life', 'financial', 60) # 经济压力 60%

# 计算综合压力指数
stress_index = assessment.calculate_index()
print(f"综合压力指数: {stress_index}")

# 获取压力等级
level = assessment.get_level()
print(f"压力等级: {level.label}")  # 例如: "中等"

# 获取减压建议
recommendations = assessment.get_recommendations()
for rec in recommendations:
    print(f"- {rec}")
```

## 压力等级说明

| 等级 | 范围 | 说明 | 建议措施 |
|------|------|------|----------|
| 极低 | 0-20 | 心理状态良好 | 保持健康生活方式 |
| 低 | 20-40 | 正常生活压力 | 保持规律作息 |
| 中等 | 40-60 | 需要关注调节 | 增加休息时间，学习压力管理 |
| 高 | 60-80 | 可能影响生活 | 强烈建议减压措施 |
| 极高 | 80-100 | 可能影响健康 | 建议寻求专业帮助 |

## 压力因素类型

### 工作压力 (`work`)
- `workload` - 工作量
- `deadline` - 截止日期压力
- `conflict` - 工作冲突
- `achievement` - 成就感缺失
- `uncertainty` - 工作不确定性

### 生活压力 (`life`)
- `financial` - 经济压力
- `relationship` - 人际关系
- `family` - 家庭压力
- `housing` -住房压力
- `social` - 社交压力

### 健康压力 (`health`)
- `physical` - 身体健康
- `mental` - 心理健康
- `sleep` - 睡眠问题
- `nutrition` - 饮营养
- `exercise` - 运动不足

## 详细示例

### 压力评估与追踪

```python
from stress_utils.mod import StressTracker

tracker = StressTracker()

# 记录每日压力
tracker.record_daily(
    date="2026-05-11",
    stress_index=45,
    factors={'work': 60, 'life': 30, 'health': 20}
)

# 查看趋势
trend = tracker.analyze_trend(days=7)
print(f"7日平均压力: {trend['average']}")
print(f"趋势方向: {trend['direction']}")  # "上升" / "稳定" / "下降"

# 压力高峰时段
peak_times = tracker.get_peak_times()
print(f"压力高峰时段: {peak_times}")
```

### 职业倦怠风险评估

```python
from stress_utils.mod import BurnoutAssessment

burnout = BurnoutAssessment()

# 评估倦怠风险因素
burnout.evaluate(
    exhaustion_level=70,      # 情感耗竭程度
    detachment_level=60,      # 疏离程度
    efficacy_level=40,        # 自我效能感下降
    work_hours_per_week=55    # 每周工作时长
)

# 获取风险评估
risk = burnout.get_risk_level()
print(f"倦怠风险等级: {risk}")  # "低风险" / "中风险" / "高风险"

# 获取干预建议
interventions = burnout.get_intervention_suggestions()
```

## API 参考

### StressAssessment

| 方法 | 参数 | 返回值 | 说明 |
|------|------|--------|------|
| `add_factor(category, factor, value)` | 类别、因素、值 | None | 添加压力因素 |
| `calculate_index()` | None | float | 计算综合压力指数 |
| `get_level()` | None | StressLevel | 获取压力等级 |
| `get_recommendations()` | None | List[str] | 获取减压建议 |

### StressTracker

| 方法 | 参数 | 返回值 | 说明 |
|------|------|--------|------|
| `record_daily(date, stress_index, factors)` | 日期、指数、因素 | None | 记录每日压力 |
| `analyze_trend(days)` | 天数 | Dict | 分析趋势 |
| `get_peak_times()` | None | List | 获取压力高峰时段 |

## 测试

运行测试：

```bash
python stress_utils/stress_utils_test.py
```

测试覆盖：
- 55 个测试用例
- 覆盖压力计算、等级分类、建议生成
- 边界值测试（极端压力值、零压力、组合因素）

---

**最后更新**: 2026-05-11
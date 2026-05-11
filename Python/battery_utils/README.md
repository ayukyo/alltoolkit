# Battery Utils - 电池计算工具 🔋

电池相关计算工具，支持充电时间估算、续航计算、健康度评估等。零外部依赖。

## 功能

- **充电时间估算**: 根据容量和充电电流计算充电时间
- **电池续航**: 根据功耗估算运行时间
- **健康度评估**: SOH（State of Health）计算
- **循环寿命**: DOD（放电深度）对寿命的影响
- **衰减模型**: 长期使用后的容量衰减预测
- **充电效率**: 实际存储能量与输入能量比值
- **电池配置**: 串联/并联计算
- **完整报告**: 一键生成电池状态报告

## 支持的电池类型

- 锂离子电池 (Li-ion)
- 锂聚合物电池 (Li-po)
- 磷酸铁锂电池 (LiFePO4)
- 镍氢电池 (NiMH)
- 镍镉电池 (NiCd)
- 铅酸电池 (Lead-acid)
- 碱性电池 (Alkaline)

## 快速开始

### 充电时间计算

```python
from battery_utils import calculate_charge_time, BatteryCalculator

# 基本计算: 3000mAh 电池, 1000mA 充电电流
result = calculate_charge_time(3000, 1000)
print(result['formatted'])  # "3小时 0分钟"

# 考虑当前电量 (50%) 和效率 (85%)
result = BatteryCalculator.calculate_charge_time(3000, 1000, 0.85, 50)
print(result['total_hours'])  # 约 1.5 小时
```

### 续航估算

```python
from battery_utils import estimate_runtime

# 3000mAh 电池, 3.7V, 2W 功耗
runtime = estimate_runtime(3000, 3.7, 2)
print(f"续航: {runtime} 小时")

# 考虑效率
result = BatteryCalculator.estimate_runtime(3000, 3.7, 2, efficiency=0.9)
print(result['formatted'])  # "X小时 Y分钟"
```

### 健康度评估

```python
from battery_utils import calculate_battery_health, BatteryType

# 当前容量 2400mAh, 设计容量 3000mAh, 循环 100 次
health = calculate_battery_health(2400, 3000, 100)
print(f"健康度: {health}%")

# 详细报告
result = BatteryCalculator.calculate_battery_health(2400, 3000, 100, BatteryType.LI_ION)
print(result['grade'])  # 'A', 'B', 'C', 'D', 'E'
print(result['remaining_cycles'])  # 剩余循环寿命
```

### 衰减模型预测

```python
from battery_utils import BatteryCalculator, BatteryType

# 5年后的衰减预测
result = BatteryCalculator.model_degradation(5, BatteryType.LI_ION)
print(f"剩余容量: {result['remaining_capacity_percent']}%")
print(f"达到80%需要: {result['prediction']['years_to_80_percent']}年")

# 高温影响
result = BatteryCalculator.model_degradation(2, BatteryType.LI_ION, 365, 40)  # 40°C
print(f"高温衰减: {result['total_degradation_percent']}%")
```

### 充电器推荐

```python
# 推荐 3000mAh 电池的充电器
result = BatteryCalculator.recommend_charger(3000)
print(f"推荐电流: {result['recommended_current_ma']}mA")

# 快充推荐
result = BatteryCalculator.recommend_charger(3000, BatteryType.LI_ION, fast_charge=True)
print(f"快充电流: {result['recommended_current_ma']}mA")
```

### 电池配置计算

```python
# 两块电池并联
result = BatteryCalculator.calculate_parallel_series(2, 3000, 3.7, 'parallel')
print(f"总容量: {result['total_capacity_mah']}mAh")  # 6000mAh
print(f"电压: {result['total_voltage']}V")  # 3.7V

# 两块电池串联
result = BatteryCalculator.calculate_parallel_series(2, 3000, 3.7, 'series')
print(f"总容量: {result['total_capacity_mah']}mAh")  # 3000mAh
print(f"电压: {result['total_voltage']}V")  # 7.4V
```

### 完整报告

```python
# 生成完整电池报告
report = BatteryCalculator.full_battery_report(3000, 3.7)
print(report['specs'])  # 规格
print(report['charging'])  # 充电信息
print(report['runtime'])  # 续航估算
print(report['tips'])  # 使用建议

# 带健康度的报告
report = BatteryCalculator.full_battery_report(3000, 3.7, BatteryType.LI_ION, 100, 2800)
print(report['health'])  # 健康度详情
```

## API 参考

### calculate_charge_time(capacity_mah, current_ma)

返回充电时间字典:
- `total_hours`: 总小时数
- `formatted`: 格式化字符串

### estimate_runtime(capacity_mah, voltage, power_w)

返回续航小时数

### calculate_battery_health(current_mah, design_mah, cycles)

返回健康度百分比

### BatteryCalculator 类

| 方法 | 描述 |
|------|------|
| `calculate_charge_time()` | 详细充电时间计算 |
| `estimate_runtime()` | 详细续航估算 |
| `calculate_battery_health()` | 详细健康度评估 |
| `calculate_cycle_count()` | 循环次数计算 |
| `model_degradation()` | 衰减模型预测 |
| `recommend_charger()` | 充电器推荐 |
| `full_battery_report()` | 完整报告生成 |

## 测试

```bash
python battery_utils_test.py
```

**测试覆盖**: 44 个测试用例，100% 通过 ✅

---

*最后更新: 2026-05-12*
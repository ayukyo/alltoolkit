# One Rep Max Utilities (单次最大重量计算工具)

**零依赖**的 Python 单次最大重量（1RM）估算和力量训练规划工具库。

## 功能特性

### 🏋️ 多种科学公式

支持 8 种主流 1RM 估算公式：

| 公式 | 特点 | 适用范围 |
|------|------|----------|
| **Brzycki** | 最常用，精确度高 | 1-10 次 |
| **Epley** | 简单计算，适合高次数 | 1-10 次 |
| **Lander** | 与 Brzycki 类似 | 1-10 次 |
| **Lombardi** | 幂函数，适合各种次数 | 1-10 次 |
| **O'Conner** | 简单线性公式 | 1-10 次 |
| **Wathan** | 指数衰减，更精确 | 1-10 次 |
| **Mayhew** | 类似 Wathan | 1-10 次 |
| **Baechle** | Wathan 别名 | 1-10 次 |

### 📊 核心功能

1. **1RM 估算** - 根据训练重量和次数计算单次最大重量
2. **反向计算** - 根据 1RM 和目标次数计算训练重量
3. **训练表生成** - nRM 表、百分比表
4. **进度追踪** - 比较进步、计算变化百分比
5. **力量等级评估** - 基于力量体重比评估训练水平
6. **Wilks 得分** - 力量举标准化评分
7. **热身建议** - 自动生成热身组重量和次数
8. **杠铃片四舍五入** - 调整到可用杠铃片组合

## 快速开始

### 基本 1RM 计算

```python
from one_rep_max_utils.mod import calculate_1rm

# 你卧推 80kg 做了 8 次
one_rm = calculate_1rm(80, 8)
print(f"估算 1RM: {one_rm:.2f}kg")  # 约 99kg

# 使用不同公式
one_rm = calculate_1rm(80, 8, formula='epley')
```

### 多公式对比

```python
from one_rep_max_utils.mod import calculate_all_formulas, average_1rm

# 所有公式结果对比
results = calculate_all_formulas(80, 8)
for name, value in results.items():
    print(f"{name}: {value:.2f}kg")

# 平均值
avg = average_1rm(80, 8)
```

### 训练计划生成

```python
from one_rep_max_utils.mod import generate_rep_max_table, generate_percentage_table

# 假设深蹲 1RM 是 150kg
one_rm = 150

# nRM 表
table = generate_rep_max_table(one_rm, max_reps=10)
# {1: 150, 2: 147.2, 3: 144.4, 5: 130.5, ...}

# 百分比表
pct_table = generate_percentage_table(one_rm)
# {95: 142.5, 90: 135, 85: 127.5, ...}
```

### 反向计算

```python
from one_rep_max_utils.mod import calculate_weight_for_reps

# 1RM 100kg，要做 5×5 训练，应该用多少重量？
weight = calculate_weight_for_reps(100, 5)
# 约 86kg
```

### 力量等级评估

```python
from one_rep_max_utils.mod import calculate_strength_level, calculate_wilks_score

# 男性，体重 80kg，卧推 100kg
level = calculate_strength_level(100, 80, 'male', 'bench_press')
# 'Advanced' (力量体重比 1.25)

wilks = calculate_wilks_score(100, 80, 'male')
# Wilks 得分约 72
```

### 使用计算器类

```python
from one_rep_max_utils.mod import OneRepMaxCalculator

calc = OneRepMaxCalculator(formula='epley')

# 计算 1RM
one_rm = calc.calculate(80, 8)

# 生成训练表
table = calc.generate_table(one_rm)

# 热身建议
warmup = calc.suggest_warmup(one_rm, 80)
```

## API 参考

### 核心公式函数

```python
brzycki(weight, reps)      # Brzycki 公式
epley(weight, reps)        # Epley 公式
lander(weight, reps)       # Lander 公式
lombardi(weight, reps)     # Lombardi 公式
oconner(weight, reps)      # O'Conner 公式
wathan(weight, reps)       # Wathan 公式
mayhew(weight, reps)       # Mayhew 公式
baechle(weight, reps)      # Baechle 公式（= Wathan）
```

### 综合计算

```python
calculate_1rm(weight, reps, formula='brzycki')
    # 使用指定公式计算 1RM

calculate_all_formulas(weight, reps)
    # 返回所有公式的结果字典

average_1rm(weight, reps, formulas=None)
    # 计算平均 1RM（默认全部公式）
```

### 反向计算

```python
calculate_weight_for_reps(one_rm, reps, formula='brzycki')
    # 根据目标 1RM 和次数计算训练重量

calculate_percentage_weight(one_rm, percentage)
    # 计算 1RM 百分比的重量
```

### 训练计划

```python
generate_rep_max_table(one_rm, formula='brzycki', max_reps=12)
    # 生成 nRM 表 {次数: 重量}

generate_percentage_table(one_rm, percentages=None)
    # 生成百分比表 {百分比: 重量}

estimate_reps_at_weight(one_rm, weight, formula='brzycki')
    # 估算指定重量可完成的次数
```

### 进度追踪

```python
calculate_strength_level(one_rm, bodyweight, gender='male', exercise='bench_press')
    # 评估力量等级: Beginner/Novice/Intermediate/Advanced/Elite

calculate_wilks_score(one_rm, bodyweight, gender='male', unit='kg')
    # 计算 Wilks 得分

compare_1rm(old_1rm, new_1rm)
    # 比较两次 1RM 的变化
    # 返回: {'change': 差值, 'percentage': 百分比, 'is_improvement': 是否进步}
```

### 辅助功能

```python
round_to_plate(weight, plate_sizes=None, unit='kg')
    # 四舍五入到可用杠铃片组合

suggest_warmup_weights(one_rm, working_weight, unit='kg')
    # 返回热身组列表 [(重量, 次数), ...]

validate_input(weight, reps)
    # 验证输入参数，返回 (是否有效, 错误信息)

get_available_formulas()
    # 获取所有可用公式名称列表

get_formula_description(formula)
    # 获取公式描述
```

### OneRepMaxCalculator 类

```python
calc = OneRepMaxCalculator(formula='brzycki')

calc.calculate(weight, reps)           # 计算 1RM
calc.calculate_all(weight, reps)       # 所有公式结果
calc.calculate_average(weight, reps)   # 平均值
calc.calculate_weight_for_reps(one_rm, reps)  # 反向计算
calc.generate_table(one_rm, max_reps=12)      # nRM 表
calc.estimate_reps(one_rm, weight)            # 估算次数
calc.suggest_warmup(one_rm, working_weight)   # 热身建议
calc.compare(old_1rm, new_1rm)                # 比较进步
```

## 力量等级标准

### 卧推 (Bench Press)

| 等级 | 男性 (力量体重比) | 女性 (力量体重比) |
|------|-------------------|-------------------|
| Elite | ≥ 1.5 | ≥ 1.0 |
| Advanced | ≥ 1.2 | ≥ 0.8 |
| Intermediate | ≥ 1.0 | ≥ 0.6 |
| Novice | ≥ 0.75 | ≥ 0.4 |
| Beginner | < 0.75 | < 0.4 |

### 深蹲 (Squat)

| 等级 | 男性 | 女性 |
|------|------|------|
| Elite | ≥ 2.0 | ≥ 1.5 |
| Advanced | ≥ 1.7 | ≥ 1.2 |
| Intermediate | ≥ 1.4 | ≥ 1.0 |
| Novice | ≥ 1.0 | ≥ 0.7 |
| Beginner | < 1.0 | < 0.7 |

### 硬拉 (Deadlift)

| 等级 | 男性 | 女性 |
|------|------|------|
| Elite | ≥ 2.5 | ≥ 1.8 |
| Advanced | ≥ 2.0 | ≥ 1.4 |
| Intermediate | ≥ 1.7 | ≥ 1.1 |
| Novice | ≥ 1.2 | ≥ 0.8 |
| Beginner | < 1.2 | < 0.8 |

## 使用建议

1. **最佳次数范围**: 所有公式在 3-10 范围内最准确
2. **公式选择**: Brzycki 最常用，Epley 简单快速
3. **平均值**: 使用多公式平均值可减少单一公式误差
4. **实际调整**: 计算结果需要四舍五入到可用杠铃片组合

## 测试覆盖

- ✅ 8 种公式基本计算
- ✅ 边界值测试（1次、高次数、零/负值）
- ✅ 所有公式一致性验证
- ✅ 反向计算验证
- ✅ 力量等级评估
- ✅ Wilks 得分计算
- ✅ 进度追踪比较
- ✅ 辅助功能验证
- ✅ 真实场景模拟

**总测试数: 80+**

## 许可证

MIT License

---

**最后更新**: 2026-05-24
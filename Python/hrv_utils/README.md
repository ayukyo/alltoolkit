# HRV Utils - 心率变异性分析工具

HRV (Heart Rate Variability) 心率变异性是连续心跳间隔时间的变化程度，是评估自律神经系统功能和心血管健康的重要指标。本模块提供完整的 HRV 分析功能。

## 功能特性

- ✅ **时域分析** - SDNN、RMSSD、pNN50、NN50 等
- ✅ **频域分析** - VLF、LF、HF 功率及 LF/HF 比率
- ✅ **非线性分析** - Poincaré 图、SD1/SD2、近似熵、样本熵
- ✅ **健康评估** - 压力指数、恢复状态、心脏年龄
- ✅ **心律异常检测** - 异位搏动、漏搏、不规则指数
- ✅ **零外部依赖** - 仅使用 Python 标准库（含 FFT 实现）

## 安装

```python
# 直接复制 mod.py 到项目中使用
from hrv_utils import analyze_hrv, calculate_stress_index
```

## 快速开始

### 综合分析

```python
from mod import analyze_hrv, get_hrv_summary

# RR 间期数据（毫秒）
rr_intervals = [800, 810, 795, 820, 815, 805, 825, 810, 790, 800,
                805, 815, 790, 810, 805, 820, 795, 810, 805, 815]

# 一站式综合分析
result = analyze_hrv(rr_intervals, age=30)

# 输出结果
print(result['time_domain'])      # 时域指标
print(result['frequency_domain']) # 频域指标
print(result['nonlinear'])        # 非线性指标
print(result['health_assessment']) # 健康评估

# 获取文本摘要
summary = get_hrv_summary(rr_intervals, age=30)
print(summary)
```

### 快速评估

```python
from mod import calculate_stress_index, calculate_recovery_score, check_readiness

# 快速计算压力指数（0-100）
stress = calculate_stress_index(rr_intervals)
# 输出: 35.2（数值越高压力越大）

# 快速计算恢复分数（0-100）
recovery = calculate_recovery_score(rr_intervals)
# 输出: 72.5（数值越高恢复越好）

# 训练准备状态
status = check_readiness(rr_intervals)
# 输出: {'ready': True, 'readiness_score': 75, 'readiness_level': '中等'}
```

### 时域分析

```python
from mod import calculate_time_domain_metrics

metrics = calculate_time_domain_metrics(rr_intervals)

print(f"平均 NN 间期: {metrics.mean_nn:.1f} ms")
print(f"SDNN: {metrics.sdnn:.2f} ms")      # 整体变异性
print(f"RMSSD: {metrics.rmssd:.2f} ms")    # 短期变异性
print(f"pNN50: {metrics.pnn50:.1f}%")      # 相邻间期差>50ms的百分比
```

### 频域分析

```python
from mod import calculate_frequency_domain_metrics

freq_metrics = calculate_frequency_domain_metrics(rr_intervals)

print(f"总功率: {freq_metrics.total_power:.2f} ms²")
print(f"LF 功率: {freq_metrics.lf:.2f} ms²")  # 低频 (0.04-0.15 Hz)
print(f"HF 功率: {freq_metrics.hf:.2f} ms²")  # 高频 (0.15-0.4 Hz)
print(f"LF/HF 比率: {freq_metrics.lf_hf_ratio:.2f}")  # 自律神经平衡指标
```

### 非线性分析

```python
from mod import calculate_nonlinear_metrics

nonlinear = calculate_nonlinear_metrics(rr_intervals)

print(f"SD1: {nonlinear.sd1:.2f} ms")       # 短期变异性
print(f"SD2: {nonlinear.sd2:.2f} ms")       # 长期变异性
print(f"SD1/SD2: {nonlinear.sd1_sd2_ratio:.4f}")
if nonlinear.apen:
    print(f"近似熵: {nonlinear.apen:.4f}")  # 复杂度指标
```

### 心律异常检测

```python
from mod import detect_arrhythmias

detection = detect_arrhythmias(rr_intervals)

if detection.has_arrhythmia:
    print(f"检测到异常！")
    print(f"异位搏动: {detection.ectopic_beats} 次")
    print(f"漏搏: {detection.missed_beats} 次")
    print(f"不规则指数: {detection.irregularity_score:.2%}")
```

### 数据预处理

```python
from mod import preprocess_rr_intervals

# 去除伪影和异常值
clean_rr, artifacts = preprocess_rr_intervals(
    rr_intervals,
    artifact_threshold=0.2,  # 相邻变化超过20%视为伪影
    min_rr=300,              # 最小有效间期
    max_rr=2000              # 最大有效间期
)

print(f"原始数据: {len(rr_intervals)} 个")
print(f"清理后: {len(clean_rr)} 个")
print(f"异常值: {len(artifacts)} 个")
```

## 指标说明

### 时域指标

| 指标 | 说明 | 正常范围 |
|------|------|----------|
| SDNN | NN 间期标准差 | 50-100 ms |
| RMSSD | 相邻间期差值均方根 | 20-100 ms |
| pNN50 | 相邻差>50ms百分比 | >5% |
| NN50 | 相邻差>50ms次数 | - |

### 频域指标

| 指标 | 说明 | 正常范围 |
|------|------|----------|
| VLF | 极低频 (0.0033-0.04 Hz) | - |
| LF | 低频 (0.04-0.15 Hz) | 交感+副交感 |
| HF | 高频 (0.15-0.4 Hz) | 副交感 |
| LF/HF | 自律神经平衡 | 1-2 |

### 健康评估

| 压力等级 | 压力指数 | 说明 |
|----------|----------|------|
| 低 | 0-25 | 放松状态 |
| 中等 | 25-50 | 正常 |
| 高 | 50-75 | 需关注 |
| 很高 | 75-100 | 建议休息 |

## 数据要求

- **最短分析**: 至少 10 个 RR 间期
- **推荐时长**: 5 分钟以上（用于频域分析）
- **数据格式**: 毫秒单位的 RR 间期列表

## API 参考

### `analyze_hrv(rr_intervals, age=None, preprocess=True, include_frequency=True, include_nonlinear=True)`

一站式 HRV 综合分析。

**返回：**
- dict: 包含时域、频域、非线性、心律异常、健康评估、元数据

### `calculate_time_domain_metrics(nn_intervals, segment_duration=300)`

时域指标计算。

### `calculate_frequency_domain_metrics(nn_intervals, sample_rate=4.0, method='welch')`

频域指标计算（内置 Welch PSD 估计）。

### `calculate_nonlinear_metrics(nn_intervals)`

非线性指标计算（Poincaré 图、熵）。

### `detect_arrhythmias(nn_intervals, ectopic_threshold=0.2, pause_threshold=1.5)`

心律异常检测。

### `assess_health_status(time_metrics, freq_metrics=None, nonlinear_metrics=None, age=None)`

健康状态综合评估。

## 测试

```bash
python hrv_utils_test.py
```

**测试覆盖：**
- 46 个测试用例
- 100% 通过率 ✅

## 参考文献

- Task Force of the European Society of Cardiology and the North American Society of Pacing and Electrophysiology. (1996). Heart rate variability: standards of measurement, physiological interpretation and clinical use.

## 许可证

MIT License

---

**最后更新**: 2026-05-23
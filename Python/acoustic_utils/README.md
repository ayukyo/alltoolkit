# Acoustic Utilities - 声学计算工具模块

零外部依赖的声学和声音计算工具库，提供全面的声学分析功能。

## 功能特性

### 核心分贝计算
- **功率分贝**: `db_from_power()` - 功率转换为分贝
- **强度分贝**: `db_from_intensity()` - 声强转换为分贝
- **声压级**: `db_from_pressure()` - 声压转换为声压级 (SPL)
- **反向转换**: `power_from_db()`, `intensity_from_db()`, `pressure_from_db()`

### 声级运算
- **声级叠加**: `add_decibels()` - 多声源叠加（非相干叠加）
- **声级扣除**: `subtract_decibels()` - 扣除背景噪声
- **声级平均**: `average_decibels()` - 能量平均声级
- **声级差**: `decibel_difference()` - 计算声级差

### 声音传播
- **距离衰减**: `distance_attenuation()` - 球面波扩散衰减（平方反比定律）
- **距离声级**: `sound_level_at_distance()` - 计算特定距离的声级
- **距离估算**: `distance_from_sound_level()` - 从声级估算距离

### 波长与频率
- **波长计算**: `wavelength()` - 频率转波长
- **频率计算**: `frequency_from_wavelength()` - 波长转频率
- **声速计算**: `speed_of_sound()` - 温度对声速的影响

### 多普勒效应
- **多普勒频率**: `doppler_frequency()` - 计算多普勒频移后的频率
- **频移量**: `doppler_shift()` - 计算频率偏移量

### 频率加权
- **A加权**: `a_weighting()` - A计权修正（模拟人耳响应）
- **C加权**: `c_weighting()` - C计权修正（平坦响应）
- **应用加权**: `apply_weighting()` - 应用频率加权到声级

### 响度转换
- **Phon转Sone**: `phon_to_sone()` - 响度级转换为响度
- **Sone转Phon**: `sone_to_phon()` - 响度转换为响度级
- **dB转Phon**: `db_to_phon()` - 分贝转换为响度级

### 房间声学
- **Sabine RT60**: `sabine_rt60()` - Sabine公式计算混响时间
- **Eyring RT60**: `eyring_rt60()` - Eyring公式计算混响时间
- **房间模式**: `room_modes()` - 计算房间共振频率
- **临界距离**: `critical_distance()` - 直达声与混响声相等的位置
- **推荐RT60**: `recommended_rt60()` - 不同房间类型的推荐混响时间

### 噪声准则
- **NC评级**: `noise_criteria()` - 从频谱估算噪声准则(NC)评级

### 噪声暴露
- **声暴露级**: `sound_exposure_level()` - SEL/LEQ计算
- **等效连续级**: `equivalent_continuous_level()` - Leq计算
- **噪声剂量**: `noise_dose()` - 职业噪声暴露剂量百分比
- **时间加权平均**: `time_weighted_average()` - TWA计算

### 工具函数
- **dB转线性**: `db_to_linear()`
- **线性转dB**: `linear_to_db()`
- **增益转换**: `db_gain()`
- **幅度比dB**: `amplitude_ratio_db()`
- **声功率级**: `sound_power_level()`
- **声强级**: `sound_intensity_level()`
- **听力阈值偏移**: `hearing_threshold_shift()`

## 安装使用

```python
from acoustic_utils import (
    db_from_pressure,
    wavelength,
    add_decibels,
    sabine_rt60,
    RoomAcoustics,
    AcousticUtils
)
```

## 使用示例

### 基本分贝计算

```python
from acoustic_utils import db_from_pressure, pressure_from_db

# 声压转换为声压级
spl = db_from_pressure(0.02)  # 20 Pa = 60 dB
print(f"声压级: {spl} dB")

# 声压级转换为声压
pressure = pressure_from_db(60)  # 60 dB ≈ 0.02 Pa
print(f"声压: {pressure} Pa")
```

### 多声源叠加

```python
from acoustic_utils import add_decibels

# 两个相同的60 dB声源叠加
combined = add_decibels(60, 60)  # ≈ 63 dB (+3 dB)
print(f"叠加声级: {combined:.1f} dB")

# 三个声源叠加
combined = add_decibels(60, 65, 70)
print(f"三声源叠加: {combined:.1f} dB")
```

### 距离衰减

```python
from acoustic_utils import sound_level_at_distance

# 距离1m处100 dB的声源，在10m处的声级
level_at_10m = sound_level_at_distance(100, 10, 1)
print(f"10米处声级: {level_at_10m:.1f} dB")  # ≈ 80 dB
```

### 波长计算

```python
from acoustic_utils import wavelength, frequency_from_wavelength

# A4音符 (440 Hz) 的波长
wl = wavelength(440)
print(f"A4波长: {wl:.3f} m")  # ≈ 0.78 m

# 波长转频率
freq = frequency_from_wavelength(0.343)
print(f"频率: {freq:.0f} Hz")  # 1000 Hz
```

### 多普勒效应

```python
from acoustic_utils import doppler_frequency

# 汽车以30 m/s靠近，喇叭频率440 Hz
observed_freq = doppler_frequency(440, source_velocity=30, approaching=True)
print(f"观察频率: {observed_freq:.1f} Hz")  # ≈ 485 Hz (更高)

# 汽车远离
observed_freq = doppler_frequency(440, source_velocity=30, approaching=False)
print(f"观察频率: {observed_freq:.1f} Hz")  # ≈ 402 Hz (更低)
```

### A计权滤波

```python
from acoustic_utils import a_weighting, apply_weighting, FrequencyWeighting

# 100 Hz的A计权修正
correction = a_weighting(100)
print(f"A计权修正: {correction:.1f} dB")  # ≈ -19 dB

# 应用A计权
weighted_level = apply_weighting(60, 100, FrequencyWeighting.A)
print(f"A计权声级: {weighted_level:.1f} dB")  # ≈ 41 dB
```

### 响度转换

```python
from acoustic_utils import phon_to_sone, sone_to_phon

# 40 phon = 1 sone (参考)
sone = phon_to_sone(40)
print(f"响度: {sone} sone")

# 50 phon = 2 sone (双倍响度)
sone = phon_to_sone(50)
print(f"响度: {sone} sone")

# 反向转换
phon = sone_to_phon(2)
print(f"响度级: {phon} phon")
```

### 房间声学

```python
from acoustic_utils import (
    RoomAcoustics,
    sabine_rt60,
    room_modes,
    critical_distance,
    recommended_rt60,
    RoomType
)

# 定义房间尺寸
room = RoomAcoustics(length=5, width=4, height=3)
print(f"体积: {room.volume} m³")
print(f"表面积: {room.surface_area} m²")

# 计算RT60 (平均吸声系数0.2)
rt60 = sabine_rt60(room, 0.2)
print(f"混响时间: {rt60:.2f} s")

# 计算房间模式
modes = room_modes(room, 2)
for nx, ny, nz, freq in modes[:5]:
    print(f"模式({nx},{ny},{nz}): {freq:.1f} Hz")

# 计算临界距离
rc = critical_distance(1, room, 0.2)
print(f"临界距离: {rc:.2f} m")

# 推荐RT60
min_rt, max_rt = recommended_rt60(RoomType.RECORDING_STUDIO)
print(f"录音室推荐RT60: {min_rt}-{max_rt} s")
```

### 噪声剂量计算

```python
from acoustic_utils import noise_dose, equivalent_continuous_level

# 85 dB暴露8小时的剂量
dose = noise_dose(85, 8)
print(f"噪声剂量: {dose:.1f}%")  # 100%

# 88 dB暴露4小时 (3 dB交换率)
dose = noise_dose(88, 4)
print(f"噪声剂量: {dose:.1f}%")  # 100%

# 计算Leq
leq = equivalent_continuous_level((80, 3600), (90, 3600))
print(f"等效连续声级: {leq:.1f} dB")
```

### 使用 AcousticUtils 类

```python
from acoustic_utils import AcousticUtils, RoomAcoustics, FrequencyWeighting

# 使用类方法
utils = AcousticUtils

# 分贝计算
spl = utils.db_from_pressure(0.02)

# 波长
wl = utils.wavelength(440)

# 声级叠加
combined = utils.add_decibels(60, 60)

# 房间声学
room = RoomAcoustics(5, 4, 3)
rt60 = utils.rt60_sabine(room, 0.2)
```

### 综合报告

```python
from acoustic_utils import calculate_rt60, sound_level_summary

# 房间声学综合报告
result = calculate_rt60(5, 4, 3, 0.2)
print(result)

# 声级综合报告
summary = sound_level_summary(0.02)  # 60 dB
print(summary)
```

## 物理常数

| 参数 | 值 | 说明 |
|------|-----|------|
| 声速 (20°C) | 343 m/s | 空气中声速 |
| 参考声压 | 20 µPa | 听觉阈值 |
| 参考声强 | 10⁻¹² W/m² | 参考声强 |
| 参考声功率 | 10⁻¹² W | 参考声功率 |

## 参考文献

- ISO 1999: 噪声暴露评估
- IEC 61672-1: 声级计规范
- Sabine, Wallace C.: 混响时间理论
- Fletcher-Munson 曲线: 等响度曲线
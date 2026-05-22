# Ergonomics Utils - 人体工程学工具集

人体工程学工具集，提供工作站设置建议、休息提醒、姿势评估、伸展运动建议等功能。

**零外部依赖**，使用 Python 标准库实现。

---

## 功能概览

| 功能 | 说明 |
|------|------|
| 工作站设置计算 | 根据身高计算理想的屏幕、椅子、桌子高度 |
| 休息间隔建议 | 根据工作强度计算最佳休息频率 |
| 伸展运动建议 | 提供针对性的伸展运动指导 |
| 姿势风险评估 | 评估当前姿势的健康风险等级 |
| RSI风险评估 | 评估重复性劳损风险 |
| 眼睛保护计划 | 制定眼睛疲劳预防方案 |
| 显示器设置计算 | 计算最佳显示器配置 |
| 坐立比例建议 | 分析坐姿/站姿工作比例 |

---

## 快速开始

```python
from ergonomics_utils.mod import quick_setup

# 根据身高快速获取工作站设置建议
setup = quick_setup(175)  # 175cm身高

print(setup['workstation'])
# {'screen_height': '79.9 cm (屏幕顶部高度)', ...}

print(setup['break_reminder'])
# 每45分钟休息5分钟，每20分钟看远处20秒
```

---

## 核心功能

### 1. 工作站设置计算

```python
from ergonomics_utils.mod import calculate_workstation_setup

# 坐姿工作站
setup = calculate_workstation_setup(175)  # 用户身高175cm
print(f"椅子高度: {setup.chair_height} cm")  # ~49 cm
print(f"桌子高度: {setup.desk_height} cm")  # ~75 cm
print(f"屏幕距离: {setup.screen_distance} cm")  # ~30 cm

# 站姿工作站
standing_setup = calculate_workstation_setup(175, seated=False)
print(f"桌子高度: {standing_setup.desk_height} cm")  # ~93 cm
```

**返回参数：**
- `screen_height` - 屏幕顶部高度（cm）
- `screen_distance` - 眼睛到屏幕距离（cm）
- `chair_height` - 椅子高度（cm）
- `desk_height` - 桌子高度（cm）
- `keyboard_height` - 键盘高度（cm）
- `monitor_tilt` - 显示器倾斜角度（度）
- `armrest_height` - 扶手高度（cm）
- `footrest_needed` - 是否需要脚踏
- `footrest_height` - 脚踏高度（cm，如果需要）

---

### 2. 休息间隔计算

```python
from ergonomics_utils.mod import calculate_break_intervals, WorkIntensity

# 4小时中等强度工作
breaks = calculate_break_intervals(4, WorkIntensity.MODERATE)

for b in breaks[:3]:
    print(f"{b.break_type}: {b.duration_minutes}分钟 - {b.activity}")

# 20-20-20法则（眼睛保护）
breaks = calculate_break_intervals(4, use_20_20_20_rule=True)
```

**工作强度等级：**
- `LIGHT` - 轻度工作，每60分钟休息
- `MODERATE` - 中度工作，每45分钟休息
- `INTENSIVE` - 高强度工作，每30分钟休息
- `EXTREME` - 极高强度工作，每20分钟休息

---

### 3. 伸展运动建议

```python
from ergonomics_utils.mod import get_stretch_exercises, BodyPart

# 获取所有伸展运动
all_exercises = get_stretch_exercises()

# 针对特定部位
neck_exercises = get_stretch_exercises([BodyPart.NECK])
wrist_exercises = get_stretch_exercises([BodyPart.WRISTS])
eye_exercises = get_stretch_exercises([BodyPart.EYES])

# 每个运动包含详细信息
for exercise in neck_exercises:
    print(f"【{exercise.name}】")
    print(f"  时长: {exercise.duration_seconds}秒 × {exercise.repetitions}次")
    print(f"  步骤: {exercise.instructions}")
    print(f"  好处: {exercise.benefits}")
```

**支持的身体部位：**
- `NECK` - 颈部
- `SHOULDERS` - 肩膀
- `UPPER_BACK` - 上背
- `LOWER_BACK` - 下背
- `WRISTS` - 手腕
- `HIPS` - 髋部
- `EYES` - 眼睛

---

### 4. 姿势风险评估

```python
from ergonomics_utils.mod import assess_posture

assessment = assess_posture(
    screen_distance_cm=60,      # 眼睛到屏幕距离
    screen_height_relative="level",  # 屏幕相对眼睛高度
    back_support=True,          # 是否有背支撑
    feet_flat=True,             # 双脚是否平放
    elbows_angle=95,            # 手肘角度
    breaks_taken=3,             # 已休息次数
    work_duration_minutes=120   # 已工作时间
)

print(f"风险等级: {assessment.risk_level.value}")  # low/medium/high/critical
print(f"评分: {assessment.score}/100")
print(f"问题: {assessment.issues}")
print(f"建议: {assessment.recommendations}")
print(f"受影响部位: {assessment.affected_areas}")
```

**风险等级：**
- `LOW` - 低风险（80-100分）
- `MEDIUM` - 中风险（60-79分）
- `HIGH` - 高风险（40-59分）
- `CRITICAL` - 严重风险（0-39分）

---

### 5. RSI风险评估

```python
from ergonomics_utils.mod import assess_rsi_risk

rsi = assess_rsi_risk(
    typing_hours_per_day=6,     # 每天打字时间
    mouse_hours_per_day=3,      # 每天鼠标时间
    breaks_per_day=4,           # 每天休息次数
    keyboard_position="ideal",  # 键盘位置
    mouse_position="ideal",     # 鼠标位置
    wrist_support=True,         # 是否使用手腕托
    previous_injury=False       # 是否有过往伤病
)

print(f"风险分数: {rsi.risk_score}")
print(f"风险等级: {rsi.risk_level}")
print(f"各因素分数: {rsi.factors}")
print(f"建议: {rsi.recommendations}")
print(f"警示信号: {rsi.warning_signs}")
```

**设备位置选项：**
- `keyboard_position`: "ideal" / "high" / "low"
- `mouse_position`: "ideal" / "far" / "close"

---

### 6. 眼睛保护计划

```python
from ergonomics_utils.mod import create_eye_care_plan

plan = create_eye_care_plan(
    screen_hours_per_day=8,     # 每天屏幕使用时间
    has_glasses=True,           # 是否佩戴眼镜
    screen_brightness="medium", # 屏幕亮度
    ambient_light="medium"      # 环境光线
)

print(f"休息间隔: 每{plan.break_interval_minutes}分钟")
print(f"远眺距离: {plan.focus_distance_meters}米")
print(f"眼保健操: {plan.eye_exercises}")
print(f"照明建议: {plan.lighting_recommendations}")
```

---

### 7. 显示器设置计算

```python
from ergonomics_utils.mod import calculate_optimal_monitor_setup

setup = calculate_optimal_monitor_setup(
    monitor_size_inches=24,     # 显示器尺寸
    resolution_width=1920,      # 水平分辨率
    resolution_height=1080,     # 垂直分辨率
    user_height_cm=175          # 用户身高
)

print(f"显示器尺寸: {setup['monitor_dimensions']}")
print(f"像素密度: {setup['pixel_density_ppi']} PPI")
print(f"推荐观看距离: {setup['recommended_viewing_distance_cm']} cm")
print(f"缩放建议: {setup['scaling_recommendation']}")
print(f"字体大小建议: {setup['font_size_recommendation']}")
```

---

### 8. 工作模式分析

```python
from ergonomics_utils.mod import get_work_period_analysis

analysis = get_work_period_analysis(
    work_periods=[
        {"start": "09:00", "end": "12:00"},
        {"start": "13:00", "end": "17:00"}
    ],
    break_periods=[
        {"start": "12:00", "end": "13:00"}
    ]
)

print(f"总工作时间: {analysis['total_work_hours']}小时")
print(f"休息比例: {analysis['break_ratio']}")
print(f"最长连续工作: {analysis['longest_continuous_work_minutes']}分钟")
print(f"工作强度: {analysis['work_intensity']}")
print(f"问题: {analysis['issues']}")
print(f"休息建议: {analysis['daily_break_suggestions']}")
```

---

### 9. 坐立比例建议

```python
from ergonomics_utils.mod import get_sitting_vs_standing_recommendation

result = get_sitting_vs_standing_recommendation(
    sitting_hours=5,            # 坐姿工作时间
    standing_hours=3,           # 站姿工作时间
    total_work_hours=8          # 总工作时间
)

print(f"当前坐姿比例: {result['current_sitting_ratio']}")
print(f"理想坐姿时间: {result['ideal_sitting_hours']}小时")
print(f"建议切换间隔: {result['recommended_switch_interval_minutes']}分钟")
print(f"问题: {result['issues']}")
print(f"提示: {result['tips']}")
```

---

## 数据结构

### WorkstationSetup

```python
@dataclass
class WorkstationSetup:
    screen_height: float           # 屏幕顶部高度 (cm)
    screen_distance: float         # 眼睛到屏幕距离 (cm)
    chair_height: float            # 椅子高度 (cm)
    desk_height: float             # 桌子高度 (cm)
    keyboard_height: float         # 键盘高度 (cm)
    monitor_tilt: float            # 显示器倾斜角度 (度)
    armrest_height: float          # 扶手高度 (cm)
    footrest_needed: bool          # 是否需要脚踏
    footrest_height: Optional[float]  # 脚踏高度 (cm)
```

### StretchExercise

```python
@dataclass
class StretchExercise:
    name: str                      # 名称
    body_parts: List[BodyPart]     # 目标部位
    duration_seconds: int          # 持续时间（秒）
    repetitions: int               # 重复次数
    instructions: List[str]        # 步骤说明
    benefits: List[str]            # 好处
```

### PostureAssessment

```python
@dataclass
class PostureAssessment:
    risk_level: PostureRisk        # 风险等级
    score: int                     # 0-100分
    issues: List[str]              # 问题列表
    recommendations: List[str]     # 建议列表
    affected_areas: List[BodyPart] # 受影响部位
```

---

## 常见用例

### 程序员健康工作指南

```python
from ergonomics_utils.mod import (
    calculate_workstation_setup,
    calculate_break_intervals,
    get_stretch_exercises,
    assess_rsi_risk,
    create_eye_care_plan,
    WorkIntensity,
    BodyPart
)

height = 175

# 1. 工作站设置
workstation = calculate_workstation_setup(height)

# 2. 休息计划（高强度编程）
breaks = calculate_break_intervals(8, WorkIntensity.INTENSIVE)

# 3. 重点伸展（颈部、手腕、眼睛）
stretches = get_stretch_exercises([BodyPart.NECK, BodyPart.WRISTS, BodyPart.EYES])

# 4. RSI风险评估
rsi = assess_rsi_risk(
    typing_hours_per_day=6,
    mouse_hours_per_day=3,
    breaks_per_day=6,
    keyboard_position="ideal",
    mouse_position="ideal",
    wrist_support=True,
    previous_injury=False
)

# 5. 眼睛保护
eye_plan = create_eye_care_plan(8)
```

### 使用升降桌的正确姿势

```python
from ergonomics_utils.mod import (
    calculate_workstation_setup,
    get_sitting_vs_standing_recommendation
)

height = 175

# 坐姿设置
sitting = calculate_workstation_setup(height, seated=True)

# 站姿设置
standing = calculate_workstation_setup(height, seated=False)

# 建议比例
ratio = get_sitting_vs_standing_recommendation(
    sitting_hours=5,
    standing_hours=3,
    total_work_hours=8
)

print(f"建议切换间隔: {ratio['recommended_switch_interval_minutes']}分钟")
# 输出：建议切换间隔: 30分钟
```

---

## 测试

运行完整测试套件：

```bash
python ergonomics_utils_test.py
```

测试覆盖：
- 工作站设置计算（不同身高、站立模式、边界值）
- 休息间隔计算（不同强度、20-20-20法则）
- 伸展运动建议（按部位筛选、数据结构验证）
- 姿势风险评估（理想/不良姿势、各因素影响）
- RSI风险评估（时间/设备/伤病影响）
- 眼睛保护计划（亮度/环境光）
- 显示器设置计算（分辨率/尺寸）
- 工作模式分析
- 坐立比例建议

---

## 许可证

MIT License

---

## 相关模块

- `posture_utils` - 姿势检测和提醒
- `eye_exercise_utils` - 眼保健操定时器
- `workstation_utils` - 工作站配置管理
- `rsi_prevention_utils` - RSI预防指南
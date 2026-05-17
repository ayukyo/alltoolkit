# 钓鱼助手工具模块 (fishing_utils)

🎣 钓鱼爱好者的全方位智能助手，提供气象评估、装备推荐、打窝计算、渔获记录等功能。

---

## ✨ 功能概览

| 功能 | 描述 |
|------|------|
| 钓鱼气象指数 | 综合评估天气对钓鱼的影响，给出评分和建议 |
| 月相钓鱼质量 | 计算月相周期，分析月相对钓鱼的影响 |
| 最佳钓鱼时间 | 根据季节推荐最佳钓鱼时段 |
| 鱼竿推荐 | 根据目标鱼种、水域类型推荐合适的鱼竿 |
| 鱼线配置 | 根据目标鱼大小推荐主线和子线规格 |
| 打窝料计算 | 根据鱼种、季节、时长计算窝料配方 |
| 渔获记录 | 记录和管理钓鱼会话及渔获 |
| 报告生成 | 自动生成格式化的钓鱼报告 |

---

## 🚀 快速开始

### 基本使用

```python
from fishing_utils.mod import (
    get_fishing_weather_index,
    get_best_fishing_times,
    get_moon_phase_info,
    recommend_rod,
)

# 1. 获取钓鱼气象指数
weather_index = get_fishing_weather_index(
    temperature=22,      # 温度（摄氏度）
    pressure=1013,       # 气压（hPa）
    humidity=65,         # 湿度（%）
    wind_speed=3.0,      # 风速（m/s）
    condition="多云"      # 天气状况
)
print(f"钓鱼指数: {weather_index['total_score']}分")
print(f"等级: {weather_index['level']}")
print(f"建议: {weather_index['recommendation']}")

# 2. 获取最佳钓鱼时间
best_times = get_best_fishing_times()
print(f"当前季节: {best_times['season']}")
for t in best_times['recommended_times']:
    print(f"  {t['period']}: {t['time_range']}")

# 3. 获取月相信息
moon_info = get_moon_phase_info()
print(f"月相: {moon_info['phase']}")
print(f"照明度: {moon_info['illumination']}%")
print(f"钓鱼质量评分: {moon_info['score']}")

# 4. 推荐鱼竿
rods = recommend_rod(
    fish_types=["鲫鱼", "鲤鱼"],
    water_type="池塘",
    style="casual",
    budget="medium"
)
for rod in rods:
    print(f"推荐: {rod['name']}")
    print(f"  建议长度: {rod['recommended_length']}")
    print(f"  建议材料: {rod['recommended_material']}")
```

---

## 📚 详细用法

### 钓鱼气象指数

综合评估温度、气压、湿度、风速、天气状况对钓鱼的影响。

```python
from fishing_utils.mod import FishingWeatherIndex, WeatherData, WeatherCondition

weather = WeatherData(
    temperature=22.0,
    pressure=1013.0,
    humidity=65.0,
    wind_speed=3.0,
    wind_direction="东南",
    condition=WeatherCondition.CLOUDY,
    visibility=15.0
)

result = FishingWeatherIndex.calculate_index(weather)

# 输出结构
{
    "total_score": 85.0,       # 综合评分（0-100）
    "level": "很好",           # 等级描述
    "recommendation": "...",   # 建议
    "details": {
        "temperature": 90,     # 温度评分
        "pressure": 95,        # 气压评分
        "humidity": 100,       # 湿度评分
        "wind": 85,            # 风速评分
        "condition": 90,       # 天气状况评分
        "visibility": 100      # 能见度评分
    }
}
```

**评分标准：**
- ≥90: 极好 - 绝佳钓鱼天气
- 75-89: 很好 - 良好钓鱼天气
- 60-74: 较好 - 可以出钓
- 45-59: 一般 - 选择早晚时段
- 30-44: 较差 - 等待更好天气
- <30: 不宜 - 不建议出钓

---

### 月相钓鱼质量

月相周期对鱼的活动有显著影响，此功能计算当前月相并给出钓鱼建议。

```python
from fishing_utils.mod import MoonPhaseCalculator, MoonPhase
from datetime import datetime

# 获取当前月相
date = datetime.now()
phase = MoonPhaseCalculator.get_moon_phase(date)
illumination = MoonPhaseCalculator.get_moon_illumination(date)

print(f"月相: {phase.value}")           # 如 "新月"
print(f"照明度: {illumination}%")       # 0-100%

# 获取钓鱼质量评估
quality = MoonPhaseCalculator.get_fishing_quality(date)
print(f"评分: {quality['score']}")
print(f"建议时段: {quality['best_time']}")

# 查找未来14天最佳时段
best_periods = MoonPhaseCalculator.find_next_best_period(datetime.now(), days=14)
```

**月相钓鱼指南：**
- 新月（评分90）：夜间无光，白天钓鱼最佳
- 蛾眉月（评分80）：鱼儿活跃
- 满月（评分50）：夜间觅食活跃，白天效果一般
- 残月（评分80）：白天钓鱼效果佳

---

### 最佳钓鱼时间

根据季节推荐最佳钓鱼时段。

```python
from fishing_utils.mod import FishingTimePredictor

times = FishingTimePredictor.get_best_times(datetime.now())
print(f"季节: {times['season']}")
print(f"描述: {times['description']}")

for t in times['recommended_times']:
    print(f"{t['period']}: {t['time_range']} - {t['quality']}")
```

**季节推荐：**
| 季节 | 最佳时段 | 特点 |
|------|----------|------|
| 春季 | 5:00-9:00, 17:00-20:00 | 早晚最佳 |
| 夏季 | 4:00-8:00, 18:00-22:00, 夜钓 | 避开正午炎热 |
| 秋季 | 5:00-9:00, 16:00-19:00 | 全天适宜 |
| 冬季 | 10:00-15:00 | 中午温暖时段 |

---

### 鱼竿推荐

根据目标鱼种、水域类型、钓鱼风格和预算推荐合适的鱼竿。

```python
from fishing_utils.mod import RodSelector, FishType

recommendations = RodSelector.recommend(
    target_fish=[FishType.CRUCIAN, FishType.CARP],
    water_type="水库",
    fishing_style="casual",
    budget="high"
)

for rec in recommendations:
    print(f"鱼竿: {rec['name']}")
    print(f"匹配度: {rec['match_score']}")
    print(f"建议长度: {rec['recommended_length']}")
    print(f"建议材料: {rec['recommended_material']}")
    print(f"适合鱼种: {rec['suitable_fish']}")
```

**鱼竿类型：**
- 手竿：适合池塘、水库钓鲫鲤
- 伸缩竿：适合大水域远投
- 台钓竿：适合竞技池精细钓
- 路亚竿：适合鲈鱼、狗鱼等掠食性鱼
- 飞钓竿：适合鳟鱼、鲈鱼

---

### 鱼线配置

根据目标鱼大小推荐主线和子线规格。

```python
from fishing_utils.mod import FishingLineCalculator, FishType

config = FishingLineCalculator.recommend_line(
    target_fish=FishType.CARP,
    max_fish_weight=5.0,   # 最大目标鱼重（kg）
    water_type="still",    # 水域类型
    line_type="nylon"      # 线材类型
)

print(f"主线直径: {config['main_line']['diameter']}mm")
print(f"主线强度: {config['main_line']['strength']}kg")
print(f"子线直径: {config['subline']['diameter']}mm")
print(f"线材特性: {config['line_properties']}")
print(f"使用建议: {config['tips']}")
```

**线材类型：**
| 类型 | 特点 | 适用场景 |
|------|------|----------|
| 尼龙线 | 经济实惠，结节好 | 新手通用 |
| 碳氟线 | 隐蔽性好，耐磨 | 精细钓 |
| PE线 | 强度极高，无延展 | 大鱼、路亚 |

---

### 打窝料计算

根据目标鱼种、季节、作钓时长计算窝料配方。

```python
from fishing_utils.mod import BaitCalculator, FishType

recipe = BaitCalculator.calculate_bait(
    target_fish=[FishType.CARP, FishType.GRASS_CARP],
    session_duration=6.0,   # 作钓时长（小时）
    season="summer",
    water_area=200          # 水域面积（平方米）
)

print(f"配方: {recipe['recipe_name']}")
print(f"总重量: {recipe['total_weight']}g")

for ingredient in recipe['ingredients']:
    print(f"  {ingredient['name']}: {ingredient['amount']}{ingredient['unit']}")

print(f"加水比例: {recipe['water_ratio']}")
print(f"制备建议: {recipe['preparation_tips']}")
```

**季节配方：**
- 春季：素窝为主，商品饵+玉米+小麦
- 夏季：果蔬窝，发酵玉米+豆饼
- 秋季：高蛋白窝，蚕蛹粉+麝香米
- 冬季：暖窝，红虫+蚯蚓+腥味饵

---

### 渔获记录与报告

记录钓鱼会话和渔获，生成专业报告。

```python
from fishing_utils.mod import (
    FishingSession,
    FishCatch,
    FishType,
    FishingReportGenerator,
    WeatherData,
    WeatherCondition
)

# 创建钓鱼会话
session = FishingSession(
    start_time=datetime.now() - timedelta(hours=4),
    location="某水库",
    weather=WeatherData(
        temperature=22.0,
        pressure=1013.0,
        humidity=65.0,
        wind_speed=3.0,
        wind_direction="东南",
        condition=WeatherCondition.CLOUDY
    )
)

# 添加渔获
catch1 = FishCatch(
    fish_type=FishType.CARP,
    weight=2.5,
    length=45.0,
    catch_time=datetime.now() - timedelta(hours=2),
    location="北岸",
    bait="玉米",
    depth=2.5,
    notes="漂亮的大鲤鱼"
)
session.add_catch(catch1)

catch2 = FishCatch(
    fish_type=FishType.CRUCIAN,
    weight=0.3,
    length=20.0,
    catch_time=datetime.now() - timedelta(hours=1),
    location="北岸",
    bait="蚯蚓",
    depth=1.5
)
session.add_catch(catch2)

# 结束会话
session.end_time = datetime.now()

# 生成报告
report = FishingReportGenerator.generate_report(session, include_analysis=True)
print(report)
```

---

## 🧪 测试

```bash
cd Python/fishing_utils
python fishing_utils_test.py
```

测试覆盖：
- 钓鱼气象指数计算（8个测试）
- 月相计算（7个测试）
- 最佳钓鱼时间预测（4个测试）
- 鱼竿推荐（5个测试）
- 鱼线配置（7个测试）
- 打窝料计算（6个测试）
- 渔获记录（3个测试）
- 报告生成（4个测试）
- 便捷函数（4个测试）
- 边界值测试（12个测试）

---

## 📦 数据结构

### FishType - 鱼种枚举
```python
CARP = "鲤鱼"
CRUCIAN = "鲫鱼"
CATFISH = "鲶鱼"
GRASS_CARP = "草鱼"
SILVER_CARP = "鲢鱼"
TILAPIA = "罗非鱼"
BASS = "鲈鱼"
TROUT = "鳟鱼"
PERCH = "河鲈"
PIKE = "狗鱼"
```

### WeatherCondition - 天气状况
```python
SUNNY = "晴天"
CLOUDY = "多云"
OVERCAST = "阴天"
LIGHT_RAIN = "小雨"
MODERATE_RAIN = "中雨"
HEAVY_RAIN = "大雨"
FOGGY = "雾天"
WINDY = "大风"
```

### MoonPhase - 月相
```python
NEW_MOON = "新月"
WAXING_CRESCENT = "蛾眉月"
FIRST_QUARTER = "上弦月"
WAXING_GIBBOUS = "盈凸月"
FULL_MOON = "满月"
WANING_GIBBOUS = "亏凸月"
LAST_QUARTER = "下弦月"
WANING_CRESCENT = "残月"
```

---

## 🎯 设计原则

1. **零外部依赖** - 仅使用 Python 标准库
2. **科学依据** - 参考钓鱼气象学和鱼类行为学
3. **实用性强** - 所有参数可自定义调整
4. **中文友好** - 所有输出为中文，符合中国钓鱼习惯

---

## 📝 更新日志

### 2026-05-18
- 初始版本发布
- 实现钓鱼气象指数计算
- 实现月相计算和钓鱼质量评估
- 实现最佳钓鱼时间预测
- 实现鱼竿/鱼线推荐系统
- 实现打窝料计算
- 实现渔获记录和报告生成
- 60个测试用例，100%通过率

---

## 👤 作者

AllToolkit 自动化开发系统

---

## 📄 许可证

MIT License
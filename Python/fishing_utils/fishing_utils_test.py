"""
钓鱼助手工具测试模块

测试内容：
- 钓鱼气象指数计算
- 月相计算和钓鱼质量评估
- 最佳钓鱼时间预测
- 鱼竿选择推荐
- 鱼线配置计算
- 打窝料计算
- 渔获记录和报告生成
"""

import sys
import os
from datetime import datetime, timedelta

# 添加路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fishing_utils.mod import (
    FishType,
    WeatherCondition,
    MoonPhase,
    WeatherData,
    FishCatch,
    FishingSession,
    FishingWeatherIndex,
    MoonPhaseCalculator,
    FishingTimePredictor,
    RodSelector,
    FishingLineCalculator,
    BaitCalculator,
    FishingReportGenerator,
    get_fishing_weather_index,
    get_best_fishing_times,
    get_moon_phase_info,
    recommend_rod,
)


class ResultCollector:
    """测试结果收集器"""
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []

    def add_pass(self, test_name: str):
        self.passed += 1
        print(f"✅ {test_name}")

    def add_fail(self, test_name: str, reason: str):
        self.failed += 1
        self.errors.append((test_name, reason))
        print(f"❌ {test_name}: {reason}")

    def summary(self):
        total = self.passed + self.failed
        print(f"\n{'='*50}")
        print(f"测试结果: 通过 {self.passed}/{total}")
        if self.failed > 0:
            print(f"失败的测试:")
            for name, reason in self.errors:
                print(f"  - {name}: {reason}")
        print(f"{'='*50}")
        return self.failed == 0


results = ResultCollector()


# ==================== 钓鱼气象指数测试 ====================

def test_weather_index_basic():
    """测试基本气象指数计算"""
    weather = WeatherData(
        temperature=22.0,
        pressure=1013.0,
        humidity=65.0,
        wind_speed=3.0,
        wind_direction="东南",
        condition=WeatherCondition.CLOUDY,
    )
    result = FishingWeatherIndex.calculate_index(weather)

    results.add_pass("test_weather_index_basic") if "total_score" in result and result["total_score"] >= 60 else results.add_fail("test_weather_index_basic", "评分应大于60")


def test_weather_index_optimal():
    """测试最佳天气条件"""
    weather = WeatherData(
        temperature=23.0,
        pressure=1010.0,
        humidity=70.0,
        wind_speed=1.5,
        wind_direction="东",
        condition=WeatherCondition.CLOUDY,
    )
    result = FishingWeatherIndex.calculate_index(weather)

    results.add_pass("test_weather_index_optimal") if result["total_score"] >= 85 else results.add_fail("test_weather_index_optimal", f"评分应为85+，实际{result['total_score']}")


def test_weather_index_extreme_temp():
    """测试极端温度"""
    # 高温
    hot_weather = WeatherData(
        temperature=38.0,
        pressure=1010.0,
        humidity=60.0,
        wind_speed=2.0,
        wind_direction="南",
        condition=WeatherCondition.SUNNY,
    )
    hot_result = FishingWeatherIndex.calculate_index(hot_weather)

    # 低温
    cold_weather = WeatherData(
        temperature=5.0,
        pressure=1015.0,
        humidity=70.0,
        wind_speed=2.0,
        wind_direction="北",
        condition=WeatherCondition.CLOUDY,
    )
    cold_result = FishingWeatherIndex.calculate_index(cold_weather)

    results.add_pass("test_weather_index_extreme_temp") if hot_result["total_score"] < cold_result["total_score"] else results.add_fail("test_weather_index_extreme_temp", "低温应比高温评分更高")


def test_weather_index_heavy_rain():
    """测试大雨天气"""
    weather = WeatherData(
        temperature=20.0,
        pressure=995.0,
        humidity=95.0,
        wind_speed=10.0,
        wind_direction="西",
        condition=WeatherCondition.HEAVY_RAIN,
    )
    result = FishingWeatherIndex.calculate_index(weather)

    results.add_pass("test_weather_index_heavy_rain") if result["total_score"] < 30 else results.add_fail("test_weather_index_heavy_rain", f"大雨评分应低于30，实际{result['total_score']}")


def test_weather_index_high_wind():
    """测试大风天气"""
    weather = WeatherData(
        temperature=22.0,
        pressure=1010.0,
        humidity=65.0,
        wind_speed=12.0,
        wind_direction="北",
        condition=WeatherCondition.WINDY,
    )
    result = FishingWeatherIndex.calculate_index(weather)

    results.add_pass("test_weather_index_high_wind") if result["total_score"] < 40 else results.add_fail("test_weather_index_high_wind", f"大风评分应低于40，实际{result['total_score']}")


def test_weather_index_levels():
    """测试等级划分"""
    # 极好 (>90)
    excellent = WeatherData(
        temperature=24.0, pressure=1012.0, humidity=70.0,
        wind_speed=1.0, wind_direction="东", condition=WeatherCondition.CLOUDY,
    )
    ex_result = FishingWeatherIndex.calculate_index(excellent)

    # 不宜 (<30)
    bad = WeatherData(
        temperature=35.0, pressure=985.0, humidity=95.0,
        wind_speed=15.0, wind_direction="西", condition=WeatherCondition.HEAVY_RAIN,
    )
    bad_result = FishingWeatherIndex.calculate_index(bad)

    results.add_pass("test_weather_index_levels") if ex_result["level"] == "极好" and bad_result["level"] == "不宜" else results.add_fail("test_weather_index_levels", "等级划分错误")


def test_weather_index_details():
    """测试详细评分"""
    weather = WeatherData(
        temperature=22.0,
        pressure=1015.0,
        humidity=65.0,
        wind_speed=3.0,
        wind_direction="东南",
        condition=WeatherCondition.CLOUDY,
        visibility=15.0,
    )
    result = FishingWeatherIndex.calculate_index(weather)

    has_details = "details" in result
    has_all_scores = all(k in result["details"] for k in ["temperature", "pressure", "humidity", "wind", "condition", "visibility"])

    results.add_pass("test_weather_index_details") if has_details and has_all_scores else results.add_fail("test_weather_index_details", "缺少详细评分")


def test_weather_index_recommendation():
    """测试建议生成"""
    good_weather = WeatherData(
        temperature=24.0, pressure=1012.0, humidity=70.0,
        wind_speed=1.0, wind_direction="东", condition=WeatherCondition.CLOUDY,
    )
    good_result = FishingWeatherIndex.calculate_index(good_weather)

    has_recommendation = "recommendation" in good_result and len(good_result["recommendation"]) > 0

    results.add_pass("test_weather_index_recommendation") if has_recommendation else results.add_fail("test_weather_index_recommendation", "缺少建议")


# ==================== 月相计算测试 ====================

def test_moon_phase_new_moon():
    """测试新月计算"""
    # 已知新月时间
    new_moon_date = datetime(2000, 1, 6, 18, 14, 0)
    phase = MoonPhaseCalculator.get_moon_phase(new_moon_date)

    results.add_pass("test_moon_phase_new_moon") if phase == MoonPhase.NEW_MOON else results.add_fail("test_moon_phase_new_moon", f"应为新月，实际{phase.value}")


def test_moon_phase_full_moon():
    """测试满月计算"""
    # 满月约在新月后14.77天
    full_moon_date = datetime(2000, 1, 21, 18, 14, 0)
    phase = MoonPhaseCalculator.get_moon_phase(full_moon_date)

    results.add_pass("test_moon_phase_full_moon") if phase == MoonPhase.FULL_MOON else results.add_fail("test_moon_phase_full_moon", f"应为满月，实际{phase.value}")


def test_moon_phase_cycle():
    """测试月相周期"""
    start_date = datetime(2000, 1, 6)
    phases = []

    for i in range(30):
        phase = MoonPhaseCalculator.get_moon_phase(start_date + timedelta(days=i))
        phases.append(phase)

    # 应包含新月和满月
    has_new_moon = MoonPhase.NEW_MOON in phases
    has_full_moon = MoonPhase.FULL_MOON in phases

    results.add_pass("test_moon_phase_cycle") if has_new_moon and has_full_moon else results.add_fail("test_moon_phase_cycle", "周期内应包含新月和满月")


def test_moon_illumination():
    """测试月照明度"""
    # 新月照明度应为0或接近0
    new_moon = datetime(2000, 1, 6, 18, 14, 0)
    new_illum = MoonPhaseCalculator.get_moon_illumination(new_moon)

    # 满月照明度应为100或接近100
    full_moon = datetime(2000, 1, 21, 18, 14, 0)
    full_illum = MoonPhaseCalculator.get_moon_illumination(full_moon)

    results.add_pass("test_moon_illumination") if new_illum < 5 and full_illum > 95 else results.add_fail("test_moon_illumination", f"新月{new_illum}%, 满月{full_illum}%")


def test_moon_fishing_quality():
    """测试月相钓鱼质量"""
    new_moon = datetime(2000, 1, 6, 18, 14, 0)
    quality = MoonPhaseCalculator.get_fishing_quality(new_moon)

    has_score = "score" in quality
    has_description = "description" in quality
    has_best_time = "best_time" in quality

    results.add_pass("test_moon_fishing_quality") if has_score and has_description and has_best_time else results.add_fail("test_moon_fishing_quality", "缺少钓鱼质量信息")


def test_moon_quality_scores():
    """测试各月相钓鱼评分"""
    # 新月和残月评分应较高（白天钓鱼好）
    phases_to_test = [
        (MoonPhase.NEW_MOON, datetime(2000, 1, 6)),
        (MoonPhase.FULL_MOON, datetime(2000, 1, 21)),
        (MoonPhase.WAXING_CRESCENT, datetime(2000, 1, 10)),
    ]

    scores = []
    for _, date in phases_to_test:
        quality = MoonPhaseCalculator.get_fishing_quality(date)
        scores.append(quality["score"])

    results.add_pass("test_moon_quality_scores") if all(s >= 50 for s in scores) else results.add_fail("test_moon_quality_scores", "评分过低")


def test_find_next_best_period():
    """测试查找最佳时段"""
    start = datetime.now()
    periods = MoonPhaseCalculator.find_next_best_period(start, days=30)

    # 应返回列表
    is_list = isinstance(periods, list)

    results.add_pass("test_find_next_best_period") if is_list else results.add_fail("test_find_next_best_period", "应返回列表")


# ==================== 最佳钓鱼时间测试 ====================

def test_best_times_season_detection():
    """测试季节检测"""
    # 春季
    spring = datetime(2024, 3, 15)
    spring_times = FishingTimePredictor.get_best_times(spring)

    # 夏季
    summer = datetime(2024, 6, 15)
    summer_times = FishingTimePredictor.get_best_times(summer)

    # 冬季
    winter = datetime(2024, 12, 15)
    winter_times = FishingTimePredictor.get_best_times(winter)

    correct_seasons = (
        spring_times["season"] == "spring" and
        summer_times["season"] == "summer" and
        winter_times["season"] == "winter"
    )

    results.add_pass("test_best_times_season_detection") if correct_seasons else results.add_fail("test_best_times_season_detection", "季节检测错误")


def test_best_times_recommended():
    """测试推荐时段"""
    times = FishingTimePredictor.get_best_times(datetime.now())

    has_times = "recommended_times" in times and len(times["recommended_times"]) > 0
    has_period = any("period" in t for t in times["recommended_times"])
    has_quality = any("quality" in t for t in times["recommended_times"])

    results.add_pass("test_best_times_recommended") if has_times and has_period and has_quality else results.add_fail("test_best_times_recommended", "缺少推荐时段信息")


def test_best_times_winter():
    """测试冬季时段"""
    winter = datetime(2024, 12, 15)
    times = FishingTimePredictor.get_best_times(winter)

    # 冬季应有中午时段
    has_midday = any("中午" in t["period"] for t in times["recommended_times"])

    results.add_pass("test_best_times_winter") if has_midday else results.add_fail("test_best_times_winter", "冬季应推荐中午时段")


def test_best_times_summer():
    """测试夏季时段"""
    summer = datetime(2024, 6, 15)
    times = FishingTimePredictor.get_best_times(summer)

    # 夏季应有夜钓时段
    has_night = any("夜间" in t["period"] for t in times["recommended_times"])

    results.add_pass("test_best_times_summer") if has_night else results.add_fail("test_best_times_summer", "夏季应推荐夜钓")


# ==================== 鱼竿选择测试 ====================

def test_rod_recommend_basic():
    """测试基本鱼竿推荐"""
    recommendations = RodSelector.recommend(
        target_fish=[FishType.CRUCIAN, FishType.CARP],
        water_type="池塘",
        fishing_style="casual",
        budget="medium",
    )

    has_recommendations = len(recommendations) > 0
    has_name = any("name" in r for r in recommendations)

    results.add_pass("test_rod_recommend_basic") if has_recommendations and has_name else results.add_fail("test_rod_recommend_basic", "缺少推荐")


def test_rod_recommend_lure():
    """测试路亚竿推荐"""
    recommendations = RodSelector.recommend(
        target_fish=[FishType.BASS, FishType.PIKE],
        water_type="湖泊",
        fishing_style="sport",
        budget="high",
    )

    # 应推荐路亚竿
    has_lure_rod = any("lure" in r["type"] for r in recommendations)

    results.add_pass("test_rod_recommend_lure") if has_lure_rod else results.add_fail("test_rod_recommend_lure", "应推荐路亚竿")


def test_rod_recommend_competition():
    """测试竞技竿推荐"""
    recommendations = RodSelector.recommend(
        target_fish=[FishType.CRUCIAN],
        water_type="竞技池",
        fishing_style="competition",
        budget="high",
    )

    # 应推荐台钓竿
    has_pole_rod = any("pole" in r["type"] for r in recommendations)

    results.add_pass("test_rod_recommend_competition") if has_pole_rod else results.add_fail("test_rod_recommend_competition", "竞技应推荐台钓竿")


def test_rod_recommend_length():
    """测试长度推荐"""
    recommendations = RodSelector.recommend(
        target_fish=[FishType.CARP],
        water_type="水库",
    )

    has_length = any("recommended_length" in r for r in recommendations)

    results.add_pass("test_rod_recommend_length") if has_length else results.add_fail("test_rod_recommend_length", "缺少长度推荐")


def test_rod_recommend_material():
    """测试材料推荐"""
    recommendations_high = RodSelector.recommend(
        target_fish=[FishType.CARP],
        water_type="水库",
        budget="high",
    )

    recommendations_low = RodSelector.recommend(
        target_fish=[FishType.CARP],
        water_type="水库",
        budget="low",
    )

    # 高预算应推荐碳素，低预算应推荐玻璃钢
    has_material_rec = all("recommended_material" in r for r in recommendations_high + recommendations_low)

    results.add_pass("test_rod_recommend_material") if has_material_rec else results.add_fail("test_rod_recommend_material", "缺少材料推荐")


# ==================== 鱼线配置测试 ====================

def test_line_recommend_basic():
    """测试基本鱼线推荐"""
    result = FishingLineCalculator.recommend_line(
        target_fish=FishType.CRUCIAN,
        max_fish_weight=1.0,
        water_type="still",
        line_type="nylon",
    )

    has_main = "main_line" in result
    has_sub = "subline" in result

    results.add_pass("test_line_recommend_basic") if has_main and has_sub else results.add_fail("test_line_recommend_basic", "缺少主线或子线信息")


def test_line_recommend_big_fish():
    """测试大鱼线配置"""
    small_fish = FishingLineCalculator.recommend_line(
        target_fish=FishType.CRUCIAN,
        max_fish_weight=0.5,
    )

    big_fish = FishingLineCalculator.recommend_line(
        target_fish=FishType.CARP,
        max_fish_weight=10.0,
    )

    # 大鱼线应该更粗
    small_diameter = small_fish["main_line"]["diameter"]
    big_diameter = big_fish["main_line"]["diameter"]

    results.add_pass("test_line_recommend_big_fish") if big_diameter > small_diameter else results.add_fail("test_line_recommend_big_fish", "大鱼线应更粗")


def test_line_recommend_water_type():
    """测试水域类型影响"""
    still_line = FishingLineCalculator.recommend_line(
        target_fish=FishType.CARP,
        max_fish_weight=5.0,
        water_type="still",
    )

    sea_line = FishingLineCalculator.recommend_line(
        target_fish=FishType.CARP,
        max_fish_weight=5.0,
        water_type="sea",
    )

    # 海钓线应更粗
    results.add_pass("test_line_recommend_water_type") if sea_line["main_line"]["diameter"] >= still_line["main_line"]["diameter"] else results.add_fail("test_line_recommend_water_type", "海钓线应更粗")


def test_line_types():
    """测试不同线材"""
    nylon = FishingLineCalculator.recommend_line(
        target_fish=FishType.CRUCIAN,
        max_fish_weight=1.0,
        line_type="nylon",
    )

    pe = FishingLineCalculator.recommend_line(
        target_fish=FishType.BASS,
        max_fish_weight=2.0,
        line_type="pe",
    )

    fluorocarbon = FishingLineCalculator.recommend_line(
        target_fish=FishType.TROUT,
        max_fish_weight=1.5,
        line_type="fluorocarbon",
    )

    all_have_properties = all("line_properties" in r for r in [nylon, pe, fluorocarbon])

    results.add_pass("test_line_types") if all_have_properties else results.add_fail("test_line_types", "缺少线材特性")


def test_line_properties():
    """测试线材特性详情"""
    result = FishingLineCalculator.recommend_line(
        target_fish=FishType.CARP,
        max_fish_weight=3.0,
        line_type="nylon",
    )

    props = result["line_properties"]
    has_required = all(k in props for k in ["name", "stretch", "pros", "cons"])

    results.add_pass("test_line_properties") if has_required else results.add_fail("test_line_properties", "缺少线材特性详情")


def test_line_tips():
    """测试使用建议"""
    result = FishingLineCalculator.recommend_line(
        target_fish=FishType.PIKE,
        max_fish_weight=5.0,
    )

    has_tips = "tips" in result and len(result["tips"]) > 0

    results.add_pass("test_line_tips") if has_tips else results.add_fail("test_line_tips", "缺少使用建议")


def test_line_strength():
    """测试线强度"""
    # 子线强度应小于主线
    result = FishingLineCalculator.recommend_line(
        target_fish=FishType.CARP,
        max_fish_weight=5.0,
    )

    main_strength = result["main_line"]["strength"]
    sub_strength = result["subline"]["strength"]

    results.add_pass("test_line_strength") if sub_strength < main_strength else results.add_fail("test_line_strength", "子线强度应小于主线")


# ==================== 打窝料测试 ====================

def test_bait_calculation_basic():
    """测试基本打窝料计算"""
    result = BaitCalculator.calculate_bait(
        target_fish=[FishType.CRUCIAN, FishType.CARP],
        session_duration=4.0,
        season="spring",
        water_area=100,
    )

    has_recipe = "recipe_name" in result
    has_ingredients = "ingredients" in result and len(result["ingredients"]) > 0

    results.add_pass("test_bait_calculation_basic") if has_recipe and has_ingredients else results.add_fail("test_bait_calculation_basic", "缺少配方或成分")


def test_bait_calculation_duration():
    """测试时长影响"""
    short_session = BaitCalculator.calculate_bait(
        target_fish=[FishType.CARP],
        session_duration=2.0,
        season="summer",
    )

    long_session = BaitCalculator.calculate_bait(
        target_fish=[FishType.CARP],
        session_duration=8.0,
        season="summer",
    )

    # 长时钓应需要更多窝料
    short_weight = short_session["total_weight"]
    long_weight = long_session["total_weight"]

    results.add_pass("test_bait_calculation_duration") if long_weight > short_weight else results.add_fail("test_bait_calculation_duration", "长时钓应需要更多窝料")


def test_bait_calculation_season():
    """测试季节配方"""
    spring = BaitCalculator.calculate_bait(
        target_fish=[FishType.CARP],
        session_duration=4.0,
        season="spring",
    )

    winter = BaitCalculator.calculate_bait(
        target_fish=[FishType.CRUCIAN],
        session_duration=4.0,
        season="winter",
    )

    # 不同季节应有不同配方
    different_recipe = spring["recipe_name"] != winter["recipe_name"]

    results.add_pass("test_bait_calculation_season") if different_recipe else results.add_fail("test_bait_calculation_season", "不同季节应有不同配方")


def test_bait_catfish():
    """测试鲶鱼窝料"""
    result = BaitCalculator.calculate_bait(
        target_fish=[FishType.CATFISH],
        session_duration=4.0,
        season="summer",
    )

    # 鲶鱼窝料应含腥味成分
    has腥 = any("腥" in i["name"] or "肝" in i["name"] or "蚯蚓" in i["name"] for i in result["ingredients"])

    results.add_pass("test_bait_catfish") if has腥 else results.add_fail("test_bait_catfish", "鲶鱼窝料应含腥味成分")


def test_bait_preparation_tips():
    """测试制备建议"""
    result = BaitCalculator.calculate_bait(
        target_fish=[FishType.CARP],
        session_duration=4.0,
        season="autumn",
    )

    has_tips = "preparation_tips" in result and len(result["preparation_tips"]) > 0

    results.add_pass("test_bait_preparation_tips") if has_tips else results.add_fail("test_bait_preparation_tips", "缺少制备建议")


def test_bait_lure_special():
    """测试路亚饵"""
    result = BaitCalculator.calculate_bait(
        target_fish=[FishType.BASS, FishType.PIKE],
        session_duration=4.0,
        season="summer",
    )

    # 路亚饵配方应提到假饵
    is_lure = "lure" in result["recipe_key"] or any("饵" in i["name"] for i in result["ingredients"])

    results.add_pass("test_bait_lure_special") if is_lure else results.add_fail("test_bait_lure_special", "路亚应推荐假饵")


# ==================== 渔获记录测试 ====================

def test_fishing_session_basic():
    """测试基本钓鱼会话"""
    session = FishingSession(
        start_time=datetime.now() - timedelta(hours=4),
        end_time=datetime.now(),
        location="某水库",
    )

    has_duration = session.get_duration().total_seconds() > 0

    results.add_pass("test_fishing_session_basic") if has_duration else results.add_fail("test_fishing_session_basic", "会话时长计算错误")


def test_fishing_session_add_catch():
    """测试添加渔获"""
    session = FishingSession(
        start_time=datetime.now() - timedelta(hours=2),
        location="某池塘",
    )

    catch1 = FishCatch(
        fish_type=FishType.CRUCIAN,
        weight=0.3,
        length=25.0,
        catch_time=datetime.now() - timedelta(minutes=30),
        location="北岸",
        bait="蚯蚓",
        depth=1.5,
    )

    catch2 = FishCatch(
        fish_type=FishType.CARP,
        weight=2.0,
        length=45.0,
        catch_time=datetime.now() - timedelta(minutes=15),
        location="北岸",
        bait="玉米",
        depth=2.0,
    )

    session.add_catch(catch1)
    session.add_catch(catch2)

    correct_count = session.total_count == 2
    correct_weight = session.total_weight == 2.3

    results.add_pass("test_fishing_session_add_catch") if correct_count and correct_weight else results.add_fail("test_fishing_session_add_catch", "渔获统计错误")


def test_fishing_session_rate():
    """测试渔获率"""
    session = FishingSession(
        start_time=datetime.now() - timedelta(hours=2),
        end_time=datetime.now() - timedelta(hours=1),
        location="某池塘",
    )

    # 1小时内钓3条
    for i in range(3):
        catch = FishCatch(
            fish_type=FishType.CRUCIAN,
            weight=0.3,
            length=20.0,
            catch_time=datetime.now() - timedelta(hours=1, minutes=i*20),
            location="北岸",
            bait="蚯蚓",
            depth=1.5,
        )
        session.add_catch(catch)

    rate = session.get_catch_rate()

    results.add_pass("test_fishing_session_rate") if abs(rate - 3.0) < 0.01 else results.add_fail("test_fishing_session_rate", f"渔获率应为3，实际{rate}")


# ==================== 报告生成测试 ====================

def test_report_basic():
    """测试基本报告生成"""
    session = FishingSession(
        start_time=datetime.now() - timedelta(hours=4),
        end_time=datetime.now(),
        location="某水库",
    )

    catch = FishCatch(
        fish_type=FishType.CARP,
        weight=1.5,
        length=40.0,
        catch_time=datetime.now() - timedelta(hours=2),
        location="南岸",
        bait="玉米",
        depth=2.5,
    )
    session.add_catch(catch)

    report = FishingReportGenerator.generate_report(session, include_analysis=False)

    has_basic_info = "基本信息" in report and "渔获统计" in report

    results.add_pass("test_report_basic") if has_basic_info else results.add_fail("test_report_basic", "缺少基本信息")


def test_report_with_weather():
    """测试带天气信息的报告"""
    weather = WeatherData(
        temperature=22.0,
        pressure=1013.0,
        humidity=65.0,
        wind_speed=3.0,
        wind_direction="东南",
        condition=WeatherCondition.CLOUDY,
    )

    session = FishingSession(
        start_time=datetime.now() - timedelta(hours=2),
        end_time=datetime.now(),
        location="某水库",
        weather=weather,
    )

    report = FishingReportGenerator.generate_report(session)

    has_weather = "天气情况" in report

    results.add_pass("test_report_with_weather") if has_weather else results.add_fail("test_report_with_weather", "缺少天气信息")


def test_report_analysis():
    """测试分析建议"""
    session = FishingSession(
        start_time=datetime.now() - timedelta(hours=3),
        end_time=datetime.now(),
        location="某水库",
    )

    for i in range(5):
        catch = FishCatch(
            fish_type=FishType.CRUCIAN,
            weight=0.25,
            length=18.0,
            catch_time=datetime.now() - timedelta(hours=2, minutes=i*10),
            location="北岸",
            bait="蚯蚓",
            depth=1.5,
        )
        session.add_catch(catch)

    report = FishingReportGenerator.generate_report(session, include_analysis=True)

    has_analysis = "分析建议" in report

    results.add_pass("test_report_analysis") if has_analysis else results.add_fail("test_report_analysis", "缺少分析建议")


def test_report_statistics():
    """测试渔获统计"""
    session = FishingSession(
        start_time=datetime.now() - timedelta(hours=4),
        end_time=datetime.now(),
        location="某水库",
    )

    # 不同鱼种
    session.add_catch(FishCatch(
        fish_type=FishType.CRUCIAN, weight=0.3, length=20.0,
        catch_time=datetime.now() - timedelta(hours=3),
        location="北岸", bait="蚯蚓", depth=1.5,
    ))
    session.add_catch(FishCatch(
        fish_type=FishType.CARP, weight=2.0, length=40.0,
        catch_time=datetime.now() - timedelta(hours=2),
        location="北岸", bait="玉米", depth=2.0,
    ))
    session.add_catch(FishCatch(
        fish_type=FishType.CRUCIAN, weight=0.25, length=18.0,
        catch_time=datetime.now() - timedelta(hours=1),
        location="北岸", bait="蚯蚓", depth=1.5,
    ))

    report = FishingReportGenerator.generate_report(session)

    has_details = "渔获明细" in report
    has_stats = "总尾数" in report and "总重量" in report

    results.add_pass("test_report_statistics") if has_details and has_stats else results.add_fail("test_report_statistics", "缺少统计信息")


# ==================== 便捷函数测试 ====================

def test_get_fishing_weather_index_func():
    """测试便捷气象指数函数"""
    result = get_fishing_weather_index(
        temperature=22,
        pressure=1013,
        humidity=65,
        wind_speed=3.0,
        condition="多云",
    )

    has_score = "total_score" in result
    has_level = "level" in result

    results.add_pass("test_get_fishing_weather_index_func") if has_score and has_level else results.add_fail("test_get_fishing_weather_index_func", "缺少评分或等级")


def test_get_best_fishing_times_func():
    """测试便捷时间推荐函数"""
    result = get_best_fishing_times()

    has_season = "season" in result
    has_times = "recommended_times" in result

    results.add_pass("test_get_best_fishing_times_func") if has_season and has_times else results.add_fail("test_get_best_fishing_times_func", "缺少季节或时间")


def test_get_moon_phase_info_func():
    """测试便捷月相函数"""
    result = get_moon_phase_info()

    has_phase = "phase" in result
    has_score = "score" in result

    results.add_pass("test_get_moon_phase_info_func") if has_phase and has_score else results.add_fail("test_get_moon_phase_info_func", "缺少月相或评分")


def test_recommend_rod_func():
    """测试便捷鱼竿推荐函数"""
    result = recommend_rod(
        fish_types=["鲫鱼", "鲤鱼"],
        water_type="池塘",
    )

    is_list = isinstance(result, list) and len(result) > 0

    results.add_pass("test_recommend_rod_func") if is_list else results.add_fail("test_recommend_rod_func", "应返回列表")


# ==================== 边界值测试 ====================

def test_edge_extreme_pressure():
    """测试极端气压"""
    # 极低气压（台风）
    low_pressure = WeatherData(
        temperature=25.0, pressure=950.0, humidity=90.0,
        wind_speed=20.0, wind_direction="东", condition=WeatherCondition.HEAVY_RAIN,
    )
    result = FishingWeatherIndex.calculate_index(low_pressure)

    results.add_pass("test_edge_extreme_pressure") if result["total_score"] < 20 else results.add_fail("test_edge_extreme_pressure", f"极端气压评分应很低，实际{result['total_score']}")


def test_edge_zero_catch():
    """测试零渔获"""
    session = FishingSession(
        start_time=datetime.now() - timedelta(hours=4),
        end_time=datetime.now(),
        location="某水库",
    )

    rate = session.get_catch_rate()

    results.add_pass("test_edge_zero_catch") if rate == 0 else results.add_fail("test_edge_zero_catch", f"零渔获率应为0，实际{rate}")


def test_edge_very_long_session():
    """测试超长会话"""
    start = datetime.now() - timedelta(hours=24)
    session = FishingSession(
        start_time=start,
        end_time=datetime.now(),
        location="某水库",
    )

    duration = session.get_duration()
    hours = duration.total_seconds() / 3600

    results.add_pass("test_edge_very_long_session") if abs(hours - 24.0) < 0.1 else results.add_fail("test_edge_very_long_session", f"时长计算错误，实际{hours}小时")


def test_edge_zero_weight_fish():
    """测试零重量鱼"""
    catch = FishCatch(
        fish_type=FishType.CRUCIAN,
        weight=0.0,
        length=10.0,
        catch_time=datetime.now(),
        location="某池塘",
        bait="蚯蚓",
        depth=1.0,
    )

    results.add_pass("test_edge_zero_weight_fish") if catch.weight == 0 else results.add_fail("test_edge_zero_weight_fish", "零重量记录错误")


def test_edge_all_weather_conditions():
    """测试所有天气条件"""
    conditions = [
        WeatherCondition.SUNNY,
        WeatherCondition.CLOUDY,
        WeatherCondition.OVERCAST,
        WeatherCondition.LIGHT_RAIN,
        WeatherCondition.MODERATE_RAIN,
        WeatherCondition.HEAVY_RAIN,
        WeatherCondition.FOGGY,
        WeatherCondition.WINDY,
    ]

    all_have_score = True
    for condition in conditions:
        weather = WeatherData(
            temperature=22.0, pressure=1010.0, humidity=70.0,
            wind_speed=3.0, wind_direction="东", condition=condition,
        )
        result = FishingWeatherIndex.calculate_index(weather)
        if "total_score" not in result:
            all_have_score = False
            break

    results.add_pass("test_edge_all_weather_conditions") if all_have_score else results.add_fail("test_edge_all_weather_conditions", "某些天气条件计算失败")


def test_edge_all_moon_phases():
    """测试所有月相"""
    phases = list(MoonPhase)

    all_have_quality = True
    for phase in phases:
        # 找到对应月相的大致日期
        for i in range(30):
            date = datetime(2000, 1, 6) + timedelta(days=i)
            calc_phase = MoonPhaseCalculator.get_moon_phase(date)
            if calc_phase == phase:
                quality = MoonPhaseCalculator.get_fishing_quality(date)
                if "score" not in quality:
                    all_have_quality = False
                break

    results.add_pass("test_edge_all_moon_phases") if all_have_quality else results.add_fail("test_edge_all_moon_phases", "某些月相质量计算失败")


def test_edge_all_fish_types():
    """测试所有鱼种"""
    fish_types = list(FishType)

    all_have_line_rec = True
    for fish in fish_types:
        result = FishingLineCalculator.recommend_line(
            target_fish=fish,
            max_fish_weight=1.0,
        )
        if "main_line" not in result:
            all_have_line_rec = False
            break

    results.add_pass("test_edge_all_fish_types") if all_have_line_rec else results.add_fail("test_edge_all_fish_types", "某些鱼种鱼线推荐失败")


def test_edge_zero_duration():
    """测试零时长"""
    result = BaitCalculator.calculate_bait(
        target_fish=[FishType.CARP],
        session_duration=0.0,
        season="spring",
    )

    # 零时长也应返回配方
    has_recipe = "recipe_name" in result

    results.add_pass("test_edge_zero_duration") if has_recipe else results.add_fail("test_edge_zero_duration", "零时长应仍返回配方")


def test_edge_future_date():
    """测试未来日期"""
    future = datetime.now() + timedelta(days=100)
    moon_info = MoonPhaseCalculator.get_fishing_quality(future)

    has_info = "phase" in moon_info and "score" in moon_info

    results.add_pass("test_edge_future_date") if has_info else results.add_fail("test_edge_future_date", "未来日期月相计算失败")


def test_edge_past_date():
    """测试过去日期"""
    past = datetime(1990, 1, 1)
    moon_info = MoonPhaseCalculator.get_fishing_quality(past)

    has_info = "phase" in moon_info and "score" in moon_info

    results.add_pass("test_edge_past_date") if has_info else results.add_fail("test_edge_past_date", "过去日期月相计算失败")


def test_edge_negative_values():
    """测试负值处理"""
    # 负温度
    cold_weather = WeatherData(
        temperature=-10.0,
        pressure=1015.0,
        humidity=70.0,
        wind_speed=2.0,
        wind_direction="北",
        condition=WeatherCondition.CLOUDY,
    )
    result = FishingWeatherIndex.calculate_index(cold_weather)

    has_score = "total_score" in result and result["total_score"] >= 0

    results.add_pass("test_edge_negative_values") if has_score else results.add_fail("test_edge_negative_values", "负值处理错误")


def test_edge_large_area():
    """测试大面积水域"""
    result = BaitCalculator.calculate_bait(
        target_fish=[FishType.CARP],
        session_duration=4.0,
        season="summer",
        water_area=10000,  # 10000平方米
    )

    # 大面积需要更多窝料
    large_weight = result["total_weight"]

    small_result = BaitCalculator.calculate_bait(
        target_fish=[FishType.CARP],
        session_duration=4.0,
        season="summer",
        water_area=100,
    )
    small_weight = small_result["total_weight"]

    results.add_pass("test_edge_large_area") if large_weight > small_weight else results.add_fail("test_edge_large_area", "大面积应需更多窝料")


# ==================== 运行所有测试 ====================

def run_all_tests():
    """运行所有测试"""
    print("=" * 50)
    print("🎣 钓鱼助手工具测试")
    print("=" * 50)
    print()

    # 气象指数测试
    print("【钓鱼气象指数测试】")
    test_weather_index_basic()
    test_weather_index_optimal()
    test_weather_index_extreme_temp()
    test_weather_index_heavy_rain()
    test_weather_index_high_wind()
    test_weather_index_levels()
    test_weather_index_details()
    test_weather_index_recommendation()
    print()

    # 月相测试
    print("【月相计算测试】")
    test_moon_phase_new_moon()
    test_moon_phase_full_moon()
    test_moon_phase_cycle()
    test_moon_illumination()
    test_moon_fishing_quality()
    test_moon_quality_scores()
    test_find_next_best_period()
    print()

    # 最佳时间测试
    print("【最佳钓鱼时间测试】")
    test_best_times_season_detection()
    test_best_times_recommended()
    test_best_times_winter()
    test_best_times_summer()
    print()

    # 鱼竿选择测试
    print("【鱼竿选择测试】")
    test_rod_recommend_basic()
    test_rod_recommend_lure()
    test_rod_recommend_competition()
    test_rod_recommend_length()
    test_rod_recommend_material()
    print()

    # 鱼线配置测试
    print("【鱼线配置测试】")
    test_line_recommend_basic()
    test_line_recommend_big_fish()
    test_line_recommend_water_type()
    test_line_types()
    test_line_properties()
    test_line_tips()
    test_line_strength()
    print()

    # 打窝料测试
    print("【打窝料测试】")
    test_bait_calculation_basic()
    test_bait_calculation_duration()
    test_bait_calculation_season()
    test_bait_catfish()
    test_bait_preparation_tips()
    test_bait_lure_special()
    print()

    # 渔获记录测试
    print("【渔获记录测试】")
    test_fishing_session_basic()
    test_fishing_session_add_catch()
    test_fishing_session_rate()
    print()

    # 报告生成测试
    print("【报告生成测试】")
    test_report_basic()
    test_report_with_weather()
    test_report_analysis()
    test_report_statistics()
    print()

    # 便捷函数测试
    print("【便捷函数测试】")
    test_get_fishing_weather_index_func()
    test_get_best_fishing_times_func()
    test_get_moon_phase_info_func()
    test_recommend_rod_func()
    print()

    # 边界值测试
    print("【边界值测试】")
    test_edge_extreme_pressure()
    test_edge_zero_catch()
    test_edge_very_long_session()
    test_edge_zero_weight_fish()
    test_edge_all_weather_conditions()
    test_edge_all_moon_phases()
    test_edge_all_fish_types()
    test_edge_zero_duration()
    test_edge_future_date()
    test_edge_past_date()
    test_edge_negative_values()
    test_edge_large_area()
    print()

    # 返回结果
    return results.summary()


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
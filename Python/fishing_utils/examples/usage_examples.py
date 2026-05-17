"""
钓鱼助手工具使用示例

演示各种钓鱼辅助功能的使用方法
"""

from datetime import datetime, timedelta
from fishing_utils.mod import (
    FishType,
    WeatherCondition,
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


def example_weather_index():
    """钓鱼气象指数示例"""
    print("=" * 50)
    print("【钓鱼气象指数示例】")
    print("=" * 50)

    # 场景1：晴朗温和的天气
    print("\n场景1：晴朗温和天气")
    result1 = get_fishing_weather_index(
        temperature=23,
        pressure=1012,
        humidity=70,
        wind_speed=1.5,
        condition="晴"
    )
    print(f"综合评分: {result1['total_score']}分")
    print(f"等级: {result1['level']}")
    print(f"建议: {result1['recommendation']}")

    # 场景2：阴雨天气
    print("\n场景2：阴雨天气")
    result2 = get_fishing_weather_index(
        temperature=18,
        pressure=1005,
        humidity=85,
        wind_speed=5.0,
        condition="小雨"
    )
    print(f"综合评分: {result2['total_score']}分")
    print(f"等级: {result2['level']}")
    print(f"建议: {result2['recommendation']}")

    # 场景3：恶劣天气
    print("\n场景3：恶劣天气（不宜钓鱼）")
    result3 = get_fishing_weather_index(
        temperature=35,
        pressure=985,
        humidity=95,
        wind_speed=12.0,
        condition="大雨"
    )
    print(f"综合评分: {result3['total_score']}分")
    print(f"等级: {result3['level']}")
    print(f"建议: {result3['recommendation']}")

    print()


def example_moon_phase():
    """月相钓鱼质量示例"""
    print("=" * 50)
    print("【月相钓鱼质量示例】")
    print("=" * 50)

    # 当前月相
    print("\n当前月相信息:")
    moon_info = get_moon_phase_info()
    print(f"月相: {moon_info['phase']}")
    print(f"照明度: {moon_info['illumination']}%")
    print(f"钓鱼评分: {moon_info['score']}")
    print(f"描述: {moon_info['description']}")
    print(f"最佳时段: {', '.join(moon_info['best_time'])}")

    # 查找未来14天最佳时段
    print("\n未来14天最佳钓鱼时段:")
    best_periods = MoonPhaseCalculator.find_next_best_period(datetime.now(), days=14)

    if best_periods:
        for period in best_periods[:5]:
            print(f"  {period['date']} - {period['phase']} (评分{period['score']})")
    else:
        print("  未来14天内暂无特别理想的时段")

    print()


def example_best_times():
    """最佳钓鱼时间示例"""
    print("=" * 50)
    print("【最佳钓鱼时间示例】")
    print("=" * 50)

    # 当前季节推荐
    print("\n当前季节推荐:")
    times = get_best_fishing_times()
    print(f"季节: {times['season']}")
    print(f"说明: {times['description']}")

    print("\n推荐时段:")
    for t in times['recommended_times']:
        print(f"  {t['period']}: {t['time_range']} (质量: {t['quality']})")

    # 不同季节对比
    print("\n不同季节对比:")
    seasons = {
        "春季": datetime(2024, 3, 15),
        "夏季": datetime(2024, 6, 15),
        "秋季": datetime(2024, 9, 15),
        "冬季": datetime(2024, 12, 15),
    }

    for season_name, season_date in seasons.items():
        season_times = FishingTimePredictor.get_best_times(season_date)
        periods = [t['period'] for t in season_times['recommended_times']]
        print(f"  {season_name}: {', '.join(periods)}")

    print()


def example_rod_recommendation():
    """鱼竿推荐示例"""
    print("=" * 50)
    print("【鱼竿推荐示例】")
    print("=" * 50)

    # 场景1：池塘钓鲫鱼鲤鱼
    print("\n场景1：池塘钓鲫鱼鲤鱼（休闲钓）")
    rods1 = recommend_rod(
        fish_types=["鲫鱼", "鲤鱼"],
        water_type="池塘",
        style="casual",
        budget="medium"
    )
    for rod in rods1:
        print(f"  推荐: {rod['name']}")
        print(f"    长度: {rod['recommended_length']}")
        print(f"    材料: {rod['recommended_material']}")
        print(f"    适合: {rod['suitable_fish']}")

    # 场景2：水库钓大鱼
    print("\n场景2：水库钓大鱼")
    rods2 = recommend_rod(
        fish_types=["鲤鱼", "草鱼"],
        water_type="水库",
        style="casual",
        budget="high"
    )
    for rod in rods2:
        print(f"  推荐: {rod['name']}")
        print(f"    长度: {rod['recommended_length']}")
        print(f"    材料: {rod['recommended_material']}")

    # 场景3：路亚钓鲈鱼
    print("\n场景3：湖泊路亚钓鲈鱼")
    rods3 = recommend_rod(
        fish_types=["鲈鱼"],
        water_type="湖泊",
        style="sport",
        budget="high"
    )
    for rod in rods3:
        print(f"  推荐: {rod['name']}")
        print(f"    长度: {rod['recommended_length']}")
        print(f"    材料: {rod['recommended_material']}")

    # 场景4：竞技钓
    print("\n场景4：竞技池精细钓")
    rods4 = recommend_rod(
        fish_types=["鲫鱼"],
        water_type="竞技池",
        style="competition",
        budget="high"
    )
    for rod in rods4:
        print(f"  推荐: {rod['name']}")
        print(f"    长度: {rod['recommended_length']}")
        print(f"    材料: {rod['recommended_material']}")

    print()


def example_line_config():
    """鱼线配置示例"""
    print("=" * 50)
    print("【鱼线配置示例】")
    print("=" * 50)

    # 场景1：钓鲫鱼
    print("\n场景1：钓鲫鱼（小鱼）")
    config1 = FishingLineCalculator.recommend_line(
        target_fish=FishType.CRUCIAN,
        max_fish_weight=0.5,
        water_type="still",
        line_type="nylon"
    )
    print(f"  主线: {config1['main_line']['diameter']}mm, 强度{config1['main_line']['strength']}kg")
    print(f"  子线: {config1['subline']['diameter']}mm, 强度{config1['subline']['strength']}kg")
    print(f"  线材: {config1['line_properties']['name']}")
    print(f"  建议: {config1['tips']}")

    # 场景2：钓大鲤鱼
    print("\n场景2：钓大鲤鱼（大鱼）")
    config2 = FishingLineCalculator.recommend_line(
        target_fish=FishType.CARP,
        max_fish_weight=8.0,
        water_type="still",
        line_type="nylon"
    )
    print(f"  主线: {config2['main_line']['diameter']}mm, 强度{config2['main_line']['strength']}kg")
    print(f"  子线: {config2['subline']['diameter']}mm, 强度{config2['subline']['strength']}kg")
    print(f"  线材: {config2['line_properties']['name']}")

    # 场景3：路亚用PE线
    print("\n场景3：路亚钓鲈鱼（PE线）")
    config3 = FishingLineCalculator.recommend_line(
        target_fish=FishType.BASS,
        max_fish_weight=3.0,
        water_type="still",
        line_type="pe"
    )
    print(f"  线材: {config3['line_properties']['name']}")
    print(f"  特点: {config3['line_properties']['pros']}")

    # 场景4：海钓
    print("\n场景4：海钓")
    config4 = FishingLineCalculator.recommend_line(
        target_fish=FishType.BASS,
        max_fish_weight=5.0,
        water_type="sea",
        line_type="nylon"
    )
    print(f"  海钓主线: {config4['main_line']['diameter']}mm")
    print(f"  注意: 海钓线需要更粗更强")

    print()


def example_bait_calculation():
    """打窝料计算示例"""
    print("=" * 50)
    print("【打窝料计算示例】")
    print("=" * 50)

    # 场景1：春季钓鲫鱼
    print("\n场景1：春季钓鲫鱼（4小时）")
    bait1 = BaitCalculator.calculate_bait(
        target_fish=[FishType.CRUCIAN],
        session_duration=4.0,
        season="spring",
        water_area=100
    )
    print(f"  配方: {bait1['recipe_name']}")
    print(f"  总重: {bait1['total_weight']}g")
    print(f"  成分:")
    for ing in bait1['ingredients']:
        print(f"    - {ing['name']}: {ing['amount']}{ing['unit']}")
    print(f"  加水比例: {bait1['water_ratio']}")
    print(f"  制备建议: {bait1['preparation_tips'][0]}")

    # 场景2：夏季钓大鱼
    print("\n场景2：夏季钓大鱼（8小时）")
    bait2 = BaitCalculator.calculate_bait(
        target_fish=[FishType.CARP, FishType.GRASS_CARP],
        session_duration=8.0,
        season="summer",
        water_area=500
    )
    print(f"  配方: {bait2['recipe_name']}")
    print(f"  总重: {bait2['total_weight']}g")
    print(f"  成分:")
    for ing in bait2['ingredients']:
        print(f"    - {ing['name']}: {ing['amount']}{ing['unit']}")

    # 场景3：冬季钓鲫鱼
    print("\n场景3：冬季钓鲫鱼（4小时）")
    bait3 = BaitCalculator.calculate_bait(
        target_fish=[FishType.CRUCIAN],
        session_duration=4.0,
        season="winter",
        water_area=100
    )
    print(f"  配方: {bait3['recipe_name']}")
    print(f"  成分:")
    for ing in bait3['ingredients']:
        print(f"    - {ing['name']}: {ing['amount']}{ing['unit']}")

    # 场景4：钓鲶鱼
    print("\n场景4：钓鲶鱼")
    bait4 = BaitCalculator.calculate_bait(
        target_fish=[FishType.CATFISH],
        session_duration=4.0,
        season="summer"
    )
    print(f"  配方: {bait4['recipe_name']}")
    print(f"  成分:")
    for ing in bait4['ingredients']:
        print(f"    - {ing['name']}: {ing['amount']}{ing['unit']}")

    print()


def example_fishing_session_and_report():
    """钓鱼会话和报告示例"""
    print("=" * 50)
    print("【钓鱼会话和报告示例】")
    print("=" * 50)

    # 创建钓鱼会话
    weather = WeatherData(
        temperature=22.0,
        pressure=1013.0,
        humidity=65.0,
        wind_speed=3.0,
        wind_direction="东南",
        condition=WeatherCondition.CLOUDY,
    )

    session = FishingSession(
        start_time=datetime.now() - timedelta(hours=4),
        end_time=datetime.now(),
        location="城郊水库",
        weather=weather,
    )

    # 添加渔获
    catches = [
        FishCatch(
            fish_type=FishType.CARP,
            weight=2.5,
            length=45.0,
            catch_time=datetime.now() - timedelta(hours=3, minutes=30),
            location="北岸钓位",
            bait="发酵玉米",
            depth=2.5,
            notes="漂亮的金黄色鲤鱼！",
        ),
        FishCatch(
            fish_type=FishType.CRUCIAN,
            weight=0.35,
            length=22.0,
            catch_time=datetime.now() - timedelta(hours=2),
            location="北岸钓位",
            bait="蚯蚓",
            depth=1.8,
        ),
        FishCatch(
            fish_type=FishType.CARP,
            weight=1.2,
            length=35.0,
            catch_time=datetime.now() - timedelta(hours=1),
            location="北岸钓位",
            bait="商品饵",
            depth=2.0,
        ),
        FishCatch(
            fish_type=FishType.CRUCIAN,
            weight=0.28,
            length=20.0,
            catch_time=datetime.now() - timedelta(minutes=45),
            location="北岸钓位",
            bait="蚯蚓",
            depth=1.5,
        ),
        FishCatch(
            fish_type=FishType.GRASS_CARP,
            weight=3.0,
            length=50.0,
            catch_time=datetime.now() - timedelta(minutes=20),
            location="北岸钓位",
            bait="嫩玉米",
            depth=3.0,
            notes="大草鱼，冲劲十足！",
        ),
    ]

    for catch in catches:
        session.add_catch(catch)

    # 生成报告
    report = FishingReportGenerator.generate_report(session, include_analysis=True)
    print(report)


def main():
    """运行所有示例"""
    print("\n" + "=" * 60)
    print("   🎣 钓鱼助手工具 - 使用示例演示")
    print("=" * 60 + "\n")

    example_weather_index()
    example_moon_phase()
    example_best_times()
    example_rod_recommendation()
    example_line_config()
    example_bait_calculation()
    example_fishing_session_and_report()

    print("\n" + "=" * 60)
    print("   示例演示完成！祝钓鱼愉快！🎣")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
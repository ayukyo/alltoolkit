"""
plant_care_utils 使用示例

这个示例展示了如何使用 plant_care_utils 工具包来管理植物养护
"""

import sys
import os
from datetime import datetime, timedelta

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from plant_care_utils.mod import (
    Plant,
    PlantCareScheduler,
    PlantType,
    Season,
    LightLevel,
    HealthStatus,
    GrowthStage,
    calculate_water_needs,
    analyze_light_requirements,
    get_seasonal_fertilizer_recommendation,
    diagnose_plant_issue,
    create_plant_care_calendar,
    quick_water_check,
    list_all_plant_types
)


def example_basic_plant_management():
    """示例：基础植物管理"""
    print("\n" + "=" * 60)
    print("示例 1: 基础植物管理")
    print("=" * 60)
    
    # 创建植物实例
    my_monstera = Plant(
        name="客厅龟背竹",
        plant_type=PlantType.TROPICAL,
        location="客厅",
        purchase_date=datetime(2025, 1, 15),
        notes="买自花市，已经长出3片新叶"
    )
    
    # 获取植物信息
    info = my_monstera.get_info()
    print(f"\n植物信息:")
    print(f"  名称: {info['name']}")
    print(f"  类型: {info['type_name']}")
    print(f"  位置: {info['location']}")
    print(f"  已养护: {info['age_days']} 天")
    
    # 记录养护活动
    my_monstera.record_watering(amount_ml=300)
    my_monstera.record_fertilizing(fertilizer_type="复合肥")
    my_monstera.record_health_check(HealthStatus.GOOD, "叶片健康，生长良好")
    
    print(f"\n养护记录:")
    print(f"  上次浇水: {my_monstera.last_watered.strftime('%Y-%m-%d %H:%M')}")
    print(f"  上次施肥: {my_monstera.last_fertilized.strftime('%Y-%m-%d')}")
    
    # 获取养护历史
    history = my_monstera.get_care_history(days=30)
    print(f"\n近30天养护记录数: {len(history)}")


def example_plant_collection_management():
    """示例：植物集合管理"""
    print("\n" + "=" * 60)
    print("示例 2: 植物集合管理")
    print("=" * 60)
    
    # 创建调度器
    scheduler = PlantCareScheduler()
    
    # 添加多株植物
    plants_data = [
        ("龟背竹", PlantType.TROPICAL, "客厅"),
        ("仙人掌", PlantType.CACTUS, "阳台"),
        ("蕨类", PlantType.FERN, "浴室"),
        ("多肉组合", PlantType.SUCCULENT, "书房窗台"),
        ("绿萝", PlantType.FOLIAGE, "办公室")
    ]
    
    for name, type_, location in plants_data:
        plant = Plant(name=name, plant_type=type_, location=location)
        scheduler.add_plant(plant)
    
    print(f"\n植物集合: {len(scheduler.plants)} 株")
    
    # 获取浇水计划（春季）
    print("\n春季浇水计划:")
    water_schedule = scheduler.get_watering_schedule(
        season=Season.SPRING,
        indoor_temperature=22,
        humidity=50
    )
    
    for item in water_schedule[:5]:
        print(f"  {item['plant_name']}: {item['days_until_watering']}天后浇水 "
              f"[紧急度: {item['urgency']}]")
    
    # 获取施肥计划
    print("\n施肥计划:")
    fertilize_schedule = scheduler.get_fertilizing_schedule()
    
    for item in fertilize_schedule[:5]:
        status = "需要施肥" if item['needs_fertilizer'] else "暂不需要"
        print(f"  {item['plant_name']}: {status} "
              f"(每{item['frequency_days']}天施肥一次)")


def example_water_needs_calculation():
    """示例：需水量计算"""
    print("\n" + "=" * 60)
    print("示例 3: 需水量计算")
    print("=" * 60)
    
    # 不同季节的需水量对比
    seasons = [Season.SPRING, Season.SUMMER, Season.AUTUMN, Season.WINTER]
    plant_type = PlantType.TROPICAL
    pot_diameter = 25  # cm
    
    print(f"\n{plant_type.value} (25cm花盆) 不同季节需水量:")
    
    for season in seasons:
        result = calculate_water_needs(
            plant_type,
            pot_diameter_cm=pot_diameter,
            season=season,
            temperature=22,
            humidity=50
        )
        
        print(f"\n{season.value}:")
        print(f"  每次浇水量: {result['water_amount_ml']} 毫升")
        print(f"  浇水频率: 每 {result['watering_frequency_days']} 天")
        print(f"  建议: {result['recommendations'][0]}")


def example_light_analysis():
    """示例：光照需求分析"""
    print("\n" + "=" * 60)
    print("示例 4: 光照需求分析")
    print("=" * 60)
    
    # 分析不同植物在不同光照环境下的情况
    scenarios = [
        (PlantType.CACTUS, LightLevel.LOW, "浴室"),
        (PlantType.FERN, LightLevel.DIRECT, "南向阳台"),
        (PlantType.ORCHID, LightLevel.MEDIUM, "客厅"),
        (PlantType.SUCCULENT, LightLevel.BRIGHT, "东向窗台")
    ]
    
    print("\n光照需求分析:")
    
    for plant_type, light_level, location in scenarios:
        result = analyze_light_requirements(plant_type, light_level)
        
        print(f"\n{plant_type.value} 在 {location}:")
        print(f"  当前光照: {light_level.value}")
        print(f"  状态: {result['status']}")
        print(f"  建议: {result['suggestions'][0]}")


def example_fertilizer_recommendation():
    """示例：施肥建议"""
    print("\n" + "=" * 60)
    print("示例 5: 季节性施肥建议")
    print("=" * 60)
    
    # 不同生长阶段的施肥建议
    stages = [
        GrowthStage.SEEDLING,
        GrowthStage.VEGETATIVE,
        GrowthStage.BUDDING,
        GrowthStage.FLOWERING
    ]
    
    plant_type = PlantType.FLOWERING
    season = Season.SPRING
    
    print(f"\n{plant_type.value} 春季施肥建议:")
    
    for stage in stages:
        result = get_seasonal_fertilizer_recommendation(
            plant_type,
            season,
            stage
        )
        
        formula = result['stage_formula']
        print(f"\n{stage.value}阶段:")
        print(f"  配方: N={formula['N']} P={formula['P']} K={formula['K']}")
        print(f"  说明: {formula['note']}")
        print(f"  季节建议: {result['seasonal_advice']['type']}")


def example_problem_diagnosis():
    """示例：问题诊断"""
    print("\n" + "=" * 60)
    print("示例 6: 植物问题诊断")
    print("=" * 60)
    
    # 诊断常见问题
    symptoms_cases = [
        (PlantType.TROPICAL, ["叶尖枯黄", "叶片发黄"]),
        (PlantType.SUCCULENT, ["叶片脱落", "根部腐烂"]),
        (PlantType.FERN, ["叶缘焦枯", "生长缓慢"])
    ]
    
    for plant_type, symptoms in symptoms_cases:
        result = diagnose_plant_issue(plant_type, symptoms)
        
        print(f"\n{plant_type.value} 症状诊断:")
        print(f"  症状: {', '.join(symptoms)}")
        
        for diagnosis in result['diagnoses']:
            print(f"\n  {diagnosis['symptom']}:")
            print(f"    可能原因: {', '.join(diagnosis['possible_causes'][:2])}")
            print(f"    解决方案: {diagnosis['solutions'][0]}")
            print(f"    严重程度: {diagnosis['severity']}")


def example_care_calendar():
    """示例：养护日历"""
    print("\n" + "=" * 60)
    print("示例 7: 月度养护日历")
    print("=" * 60)
    
    # 创建一些植物
    plants = [
        Plant("龟背竹", PlantType.TROPICAL, "客厅"),
        Plant("仙人掌", PlantType.CACTUS, "阳台"),
        Plant("绿萝", PlantType.FOLIAGE, "办公室")
    ]
    
    # 创建5月养护日历
    calendar = create_plant_care_calendar(
        year=2026,
        month=5,
        plants=plants,
        location="north"
    )
    
    print(f"\n{calendar['year']}年{calendar['month']}月养护日历 (北半球{calendar['season']}季):")
    
    # 按植物分组显示任务
    plant_tasks = {}
    for task in calendar['tasks']:
        if task['plant'] not in plant_tasks:
            plant_tasks[task['plant']] = []
        plant_tasks[task['plant']].append(task)
    
    for plant_name, tasks in plant_tasks.items():
        print(f"\n{plant_name}:")
        watering_days = [t['day'] for t in tasks if t['type'] == 'watering']
        fertilizing_days = [t['day'] for t in tasks if t['type'] == 'fertilizing']
        print(f"  浇水日: 第 {', '.join(map(str, watering_days))} 天")
        print(f"  施肥日: 第 {', '.join(map(str, fertilizing_days))} 天")
    
    print(f"\n月度总结:")
    print(f"  浇水任务总数: {calendar['monthly_summary']['total_watering_tasks']}")
    print(f"  施肥任务总数: {calendar['monthly_summary']['total_fertilizing_tasks']}")
    print(f"  季节建议:")
    for tip in calendar['monthly_summary']['seasonal_tips']:
        print(f"    - {tip}")


def example_quick_water_check():
    """示例：快速浇水检查"""
    print("\n" + "=" * 60)
    print("示例 8: 快速浇水检查")
    print("=" * 60)
    
    # 检查不同植物是否需要浇水
    plants_to_check = [
        (PlantType.TROPICAL, 7, "龟背竹"),
        (PlantType.CACTUS, 15, "仙人掌"),
        (PlantType.FERN, 4, "蕨类"),
        (PlantType.HERB, 2, "薄荷")
    ]
    
    print("\n浇水状态检查 (春季):")
    
    for plant_type, days_since, name in plants_to_check:
        result = quick_water_check(
            plant_type,
            days_since_watering=days_since,
            season=Season.SPRING
        )
        
        print(f"\n{name} (上次浇水{days_since}天前):")
        print(f"  状态: {result['urgency']}")
        print(f"  建议间隔: 每{result['recommended_interval']}天")
        if result['next_watering_in_days'] > 0:
            print(f"  下次浇水: {result['next_watering_in_days']}天后")
        else:
            print(f"  下次浇水: 立即")


def example_all_plant_types():
    """示例：所有植物类型列表"""
    print("\n" + "=" * 60)
    print("示例 9: 所有植物类型")
    print("=" * 60)
    
    types = list_all_plant_types()
    
    print(f"\n支持的植物类型 ({len(types)} 种):")
    
    for i, t in enumerate(types, 1):
        print(f"  {i}. {t['name']} ({t['type']})")


def main():
    """运行所有示例"""
    print("\n" + "=" * 60)
    print("plant_care_utils 使用示例")
    print("=" * 60)
    
    example_basic_plant_management()
    example_plant_collection_management()
    example_water_needs_calculation()
    example_light_analysis()
    example_fertilizer_recommendation()
    example_problem_diagnosis()
    example_care_calendar()
    example_quick_water_check()
    example_all_plant_types()
    
    print("\n" + "=" * 60)
    print("示例运行完成!")
    print("=" * 60)


if __name__ == "__main__":
    main()
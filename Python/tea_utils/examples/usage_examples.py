"""
茶道工具模块使用示例

演示：
- 茶叶信息查询
- 水温推荐
- 冲泡计划
- 计时器使用
- 心情推荐
- 搜索功能
"""

import sys
sys.path.insert(0, '..')

from mod import (
    get_tea_info,
    list_teas_by_category,
    get_water_temp_recommendation,
    calculate_steep_time,
    get_brewing_schedule,
    recommend_teaware,
    get_caffeine_info,
    search_tea,
    get_tea_benefits,
    get_tea_flavor_notes,
    TeaTimer,
    format_time,
    get_all_categories,
    get_tea_count,
    compare_teas,
    suggest_tea_by_mood,
    TeaCategory,
)


def example_basic_info():
    """示例1：基础信息查询"""
    print("=" * 50)
    print("【示例1】茶叶基础信息查询")
    print("=" * 50)
    
    # 获取龙井信息
    tea = get_tea_info("龙井")
    if tea:
        print(f"\n茶叶名称：{tea.name}")
        print(f"茶叶类别：{tea.category.value}")
        print(f"产地：{tea.origin}")
        print(f"推荐水温：{tea.water_temp_min}-{tea.water_temp_max}°C")
        print(f"第一泡时间：{tea.first_steep_sec}秒")
        print(f"最大泡数：{tea.max_steeps}泡")
        print(f"风味特点：{', '.join(tea.flavor_notes)}")
        print(f"健康功效：{', '.join(tea.health_benefits)}")
        print(f"咖啡因：{tea.caffeine_level}")
        print(f"\n描述：{tea.description}")


def example_water_temp():
    """示例2：水温推荐"""
    print("\n" + "=" * 50)
    print("【示例2】水温推荐")
    print("=" * 50)
    
    teas = ["龙井", "铁观音", "熟普", "玫瑰花茶"]
    
    for name in teas:
        min_temp, max_temp, note = get_water_temp_recommendation(name)
        print(f"\n{name}:")
        print(f"  推荐水温：{min_temp}-{max_temp}°C")
        print(f"  说明：{note}")


def example_brewing_schedule():
    """示例3：冲泡计划"""
    print("\n" + "=" * 50)
    print("【示例3】冲泡计划")
    print("=" * 50)
    
    # 铁观音冲泡计划
    schedule = get_brewing_schedule("铁观音")
    
    print("\n铁观音完整冲泡计划：")
    print("-" * 40)
    for item in schedule:
        print(f"第{item['steep']}泡：{format_time(item['seconds'])} | 水温 {item['water_temp_min']}-{item['water_temp_max']}°C")
    
    print(f"\n铁观音"七泡有余香"，共可冲泡{len(schedule)}次！")


def example_steep_time():
    """示例4：冲泡时间计算"""
    print("\n" + "=" * 50)
    print("【示例4】冲泡时间计算")
    print("=" * 50)
    
    # 计算大红袍各泡时间
    tea_name = "大红袍"
    print(f"\n{tea_name}冲泡时间表：")
    
    for steep in range(1, 6):
        time_sec, note = calculate_steep_time(tea_name, steep)
        print(f"  第{steep}泡：{time_sec}秒  ({note})")


def example_teaware():
    """示例5：茶具推荐"""
    print("\n" + "=" * 50)
    print("【示例5】茶具推荐")
    print("=" * 50)
    
    teas = ["龙井", "铁观音", "白毫银针", "正山小种"]
    
    for name in teas:
        teaware, note = recommend_teaware(name)
        print(f"\n{name}:")
        print(f"  推荐茶具：{', '.join(teaware)}")
        print(f"  说明：{note}")


def example_timer():
    """示例6：计时器使用"""
    print("\n" + "=" * 50)
    print("【示例6】泡茶计时器")
    print("=" * 50)
    
    # 创建计时器
    timer = TeaTimer("铁观音")
    
    print(f"\n初始化计时器：{timer.tea_name}")
    print(f"状态：{timer.get_status()}")
    
    # 开始第一泡
    print("\n开始第一泡...")
    result = timer.start()
    print(f"第{result['steep']}泡，需浸泡{result['duration_sec']}秒")
    
    # 模拟等待（实际使用时不需要sleep）
    import time as t
    t.sleep(2)  # 模拟2秒后检查
    
    # 检查状态
    status = timer.check()
    print(f"当前状态：{status['status']}")
    print(f"已浸泡：{status['elapsed_sec']}秒")
    print(f"剩余：{status['remaining_sec']}秒")
    print(f"进度：{status['progress']*100:.1f}%")
    
    # 停止计时
    timer.stop()
    print("\n第一泡完成！")
    
    # 第二泡
    print("\n开始第二泡...")
    result = timer.start()
    print(f"第{result['steep']}泡，需浸泡{result['duration_sec']}秒")
    timer.stop()
    
    # 获取当前状态
    print(f"\n当前进度：已完成{timer.current_steep}泡，还可泡{timer.total_steeps - timer.current_steep}次")


def example_search():
    """示例7：搜索功能"""
    print("\n" + "=" * 50)
    print("【示例7】茶叶搜索")
    print("=" * 50)
    
    # 搜索绿茶
    print("\n搜索'绿茶'：")
    results = search_tea("绿茶")
    for name, category, score in results:
        print(f"  {name} ({category}) - 匹配度: {score}")
    
    # 搜索花香
    print("\n搜索'花香'：")
    results = search_tea("花香")
    for name, category, score in results[:5]:  # 只显示前5个
        print(f"  {name} ({category}) - 匹配度: {score}")
    
    # 按产地搜索
    print("\n搜索'福建'：")
    results = search_tea("福建")
    print(f"  找到{len(results)}种福建茶叶")
    for name, category, score in results[:5]:
        print(f"  {name} ({category})")


def example_caffeine():
    """示例8：咖啡因信息"""
    print("\n" + "=" * 50)
    print("【示例8】咖啡因信息对比")
    print("=" * 50)
    
    teas = ["大红袍", "龙井", "白毫银针", "熟普", "玫瑰花茶", "抹茶"]
    
    print("\n咖啡因含量对比：")
    print("-" * 40)
    for name in teas:
        level, percent = get_caffeine_info(name)
        bar = "█" * (percent // 10) + "░" * (10 - percent // 10)
        print(f"  {name:10s} [{bar}] {level}")


def example_mood():
    """示例9：心情推荐"""
    print("\n" + "=" * 50)
    print("【示例9】心情推荐")
    print("=" * 50)
    
    moods = ["提神", "放松", "消化", "减肥", "养颜", "晚上"]
    
    for mood in moods:
        print(f"\n需求'{mood}'，推荐：")
        suggestions = suggest_tea_by_mood(mood)
        for name, reason in suggestions:
            print(f"  🍵 {name} - {reason}")


def example_compare():
    """示例10：茶叶对比"""
    print("\n" + "=" * 50)
    print("【示例10】茶叶对比")
    print("=" * 50)
    
    # 对比几种代表性茶叶
    comparison = compare_teas(["龙井", "铁观音", "大红袍", "熟普"])
    
    print("\n茶叶对比表：")
    print("-" * 80)
    print(f"{'名称':<10} {'类别':<10} {'产地':<12} {'水温':<10} {'首泡':<8} {'泡数':<6} {'咖啡因':<8}")
    print("-" * 80)
    
    for item in comparison:
        print(f"{item['name']:<10} {item['category']:<10} {item['origin']:<12} {item['water_temp']:<10} {item['first_steep']:<8} {item['max_steeps']:<6} {item['caffeine']:<8}")
    
    print("\n风味对比：")
    for item in comparison:
        print(f"  {item['name']}: {', '.join(item['flavor_notes'])}")


def example_categories():
    """示例11：茶叶类别统计"""
    print("\n" + "=" * 50)
    print("【示例11】茶叶类别统计")
    print("=" * 50)
    
    print(f"\n数据库中共有{get_tea_count()}种茶叶")
    
    categories = get_all_categories()
    print("\n各类别茶叶数量：")
    for cat, count in categories:
        print(f"  {cat}: {count}种")
    
    # 列出某个类别的所有茶叶
    print("\n乌龙茶类茶叶：")
    oolongs = list_teas_by_category(TeaCategory.OOLONG)
    for name in oolongs:
        tea = get_tea_info(name)
        print(f"  {name} ({tea.origin})")


def example_benefits_flavor():
    """示例12：功效和风味"""
    print("\n" + "=" * 50)
    print("【示例12】健康功效与风味")
    print("=" * 50)
    
    teas = ["龙井", "铁观音", "熟普", "玫瑰花茶"]
    
    for name in teas:
        print(f"\n{name}:")
        
        # 功效
        benefits = get_tea_benefits(name)
        print(f"  健康功效：{', '.join(benefits)}")
        
        # 风味
        flavors = get_tea_flavor_notes(name)
        print(f"  风味特点：{', '.join(flavors)}")


def example_matcha():
    """示例13：抹茶特殊处理"""
    print("\n" + "=" * 50)
    print("【示例13】抹茶特殊处理")
    print("=" * 50)
    
    tea = get_tea_info("抹茶")
    if tea:
        print(f"\n抹茶信息：")
        print(f"  类别：{tea.category.value}")
        print(f"  水温：{tea.water_temp_min}-{tea.water_temp_max}°C（不宜过热）")
        print(f"  冲泡方式：直接点茶，无需浸泡")
        print(f"  茶具：{', '.join(tea.recommended_teaware)}")
        print(f"  描述：{tea.description}")


def main():
    """运行所有示例"""
    example_basic_info()
    example_water_temp()
    example_brewing_schedule()
    example_steep_time()
    example_teaware()
    example_timer()
    example_search()
    example_caffeine()
    example_mood()
    example_compare()
    example_categories()
    example_benefits_flavor()
    example_matcha()
    
    print("\n" + "=" * 50)
    print("示例演示完成！")
    print("=" * 50)


if __name__ == "__main__":
    main()
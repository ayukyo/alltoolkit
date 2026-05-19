"""
wheel_picker_utils 使用示例

展示转盘选择器的各种使用场景
"""

import sys
import os

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    WheelPicker,
    create_simple_wheel,
    create_weighted_wheel,
    quick_pick,
    weighted_pick,
    pair_up,
    group_items,
    deterministic_pick,
    shuffle_with_seed,
    generate_rotation_schedule,
    TournamentWheel,
    PrizeWheel,
    DecisionWheel
)


def example_basic_wheel():
    """示例1: 基础转盘选择"""
    print("=" * 50)
    print("示例1: 基础转盘选择")
    print("=" * 50)
    
    # 创建简单转盘
    items = ["选项A", "选项B", "选项C", "选项D"]
    wheel = WheelPicker(items, title="基础选择转盘")
    
    # 进行选择
    print("\n单次选择:")
    result = wheel.spin()
    print(f"  选中: {result['item']}")
    print(f"  概率: {result['probability']:.2%}")
    print(f"  时间: {result['timestamp']}")
    
    # 多次选择
    print("\n多次选择（3次，唯一）:")
    results = wheel.spin_multiple(3, unique=True)
    for i, res in enumerate(results, 1):
        print(f"  第{i}次: {res['item']}")
    
    # 查看历史
    print("\n选择历史:")
    history = wheel.get_history(limit=5)
    for h in history:
        print(f"  - {h['item']} @ {h['timestamp']}")


def example_weighted_wheel():
    """示例2: 加权转盘选择"""
    print("\n" + "=" * 50)
    print("示例2: 加权转盘选择")
    print("=" * 50)
    
    # 创建加权转盘（抽奖场景）
    prizes = ["特等奖", "一等奖", "二等奖", "三等奖", "未中奖"]
    weights = [0.001, 0.01, 0.05, 0.15, 0.789]  # 不同的中奖概率
    
    wheel = WheelPicker(prizes, weights=weights, title="抽奖转盘")
    
    print("\n奖品概率分布:")
    for prize, weight in zip(prizes, weights):
        print(f"  {prize}: {weight:.2%}")
    
    print("\n模拟抽奖10次:")
    for i in range(10):
        result = wheel.spin()
        print(f"  第{i+1}次: {result['item']}")
    
    # 查看统计
    stats = wheel.get_statistics()
    print("\n抽奖统计:")
    print(f"  总抽奖次数: {stats['total_spins']}")
    print(f"  分布: {stats['distribution']}")


def example_decision_wheel():
    """示例3: 决策转盘"""
    print("\n" + "=" * 50)
    print("示例3: 决策转盘 - 今天吃什么？")
    print("=" * 50)
    
    # 使用预设
    wheel = DecisionWheel(preset="food")
    
    print("\n可选食物:")
    for food in wheel.options:
        print(f"  - {food}")
    
    print("\n随机决策:")
    decision = wheel.make_decision(person="小明")
    print(f"  {decision['person']} 决定吃: {decision['decision']}")
    
    # 连续决策，避免重复
    print("\n连续决策（排除最近选择）:")
    for i in range(5):
        decision = wheel.make_decision(exclude_recent=3)
        print(f"  第{i+1}天吃: {decision['decision']}")


def example_pairing_and_grouping():
    """示例4: 配对和分组"""
    print("\n" + "=" * 50)
    print("示例4: 配对和分组")
    print("=" * 50)
    
    people = ["张三", "李四", "王五", "赵六", "钱七", "孙八"]
    
    # 配对
    print("\n配对（乒乓球双打）:")
    pairs = pair_up(people)
    for i, (p1, p2) in enumerate(pairs, 1):
        if p2:
            print(f"  第{i}组: {p1} & {p2}")
        else:
            print(f"  {p1} (等待配对)")
    
    # 分组
    print("\n分组（比赛小组）:")
    groups = group_items(people, group_count=3, balance=True)
    for i, group in enumerate(groups, 1):
        print(f"  第{i}组: {', '.join(group)}")


def example_tournament():
    """示例5: 锦标赛对阵"""
    print("\n" + "=" * 50)
    print("示例5: 锦标赛对阵生成")
    print("=" * 50)
    
    participants = ["选手A", "选手B", "选手C", "选手D", "选手E", "选手F"]
    tournament = TournamentWheel(participants, title="羽毛球比赛")
    
    print("\n参赛选手:")
    for p in participants:
        print(f"  - {p}")
    
    # 生成对阵
    matches = tournament.generate_matches(rounds=1, randomize=True)
    
    print("\n对阵表:")
    for match in matches:
        if match["player2"]:
            print(f"  第{match['match_number']}场: {match['player1']} vs {match['player2']}")
        else:
            print(f"  {match['player1']} 自动晋级")
    
    # 模拟比赛结果
    print("\n模拟比赛结果:")
    for match in matches:
        if match["status"] == "pending":
            winner = tournament.pick_winner(1, match["match_number"])
            print(f"  第{match['match_number']}场胜者: {winner}")


def example_prize_wheel():
    """示例6: 抽奖活动"""
    print("\n" + "=" * 50)
    print("示例6: 抽奖活动")
    print("=" * 50)
    
    prizes = ["iPhone", "iPad", "耳机", "充电宝", "优惠券", "谢谢参与"]
    # 奖品概率（高价值奖品概率低）
    weights = [0.001, 0.005, 0.02, 0.05, 0.10, 0.824]
    
    wheel = PrizeWheel(prizes, weights=weights, allow_repeat=True)
    
    participants = ["张三", "李四", "王五", "赵六", "钱七"]
    
    print("\n抽奖活动开始:")
    print(f"  参与者: {', '.join(participants)}")
    print("\n  奖品池:")
    for prize, weight in zip(prizes, weights):
        print(f"    {prize}: {weight:.2%}")
    
    print("\n抽奖结果:")
    results = wheel.draw_multiple(participants)
    for result in results:
        if result["success"]:
            print(f"  {result['participant']} 获得: {result['prize']}")
        else:
            print(f"  {result['participant']}: {result['message']}")
    
    # 中奖名单
    print("\n中奖名单:")
    winners = wheel.get_winners()
    for winner in winners:
        if winner["success"]:
            print(f"  {winner['participant']}: {winner['prize']}")


def example_rotation_schedule():
    """示例7: 轮转排班"""
    print("\n" + "=" * 50)
    print("示例7: 轮转排班表")
    print("=" * 50)
    
    staff = ["张三", "李四", "王五"]
    
    print("\n值班人员:")
    for s in staff:
        print(f"  - {s}")
    
    # 生成一周排班
    schedule = generate_rotation_schedule(staff, days=7, start_date="2024-01-01", shuffle=False)
    
    print("\n一周排班表:")
    for entry in schedule:
        print(f"  {entry['date']} ({entry['day_of_week']}): {entry['item']}")


def example_deterministic_selection():
    """示例8: 确定性选择（可复现）"""
    print("\n" + "=" * 50)
    print("示例8: 确定性选择")
    print("=" * 50)
    
    items = ["A", "B", "C", "D", "E"]
    
    print("\n相同种子产生相同结果:")
    
    for seed in ["seed1", "seed2", "test123"]:
        result1 = deterministic_pick(items, seed)
        result2 = deterministic_pick(items, seed)
        
        print(f"\n  种子 '{seed}':")
        print(f"    第1次选择: {result1}")
        print(f"    第2次选择: {result2}")
        print(f"    结果一致: {result1 == result2}")
    
    # 打乱也是确定性的
    print("\n确定性打乱:")
    shuffled1 = shuffle_with_seed(items, "shuffle_seed")
    shuffled2 = shuffle_with_seed(items, "shuffle_seed")
    
    print(f"  第1次: {shuffled1}")
    print(f"  第2次: {shuffled2}")
    print(f"  结果一致: {shuffled1 == shuffled2}")


def example_quick_selection():
    """示例9: 快速选择"""
    print("\n" + "=" * 50)
    print("示例9: 快速选择工具")
    print("=" * 50)
    
    items = ["A", "B", "C", "D", "E"]
    
    # 快速唯一选择
    print("\n快速选择（3项，唯一）:")
    result = quick_pick(items, count=3, unique=True)
    print(f"  结果: {result}")
    
    # 快速可重复选择
    print("\n快速选择（5项，可重复）:")
    result = quick_pick(items, count=5, unique=False)
    print(f"  结果: {result}")
    
    # 加权快速选择
    print("\n加权快速选择:")
    weights = [1, 2, 3, 4, 5]  # E 被选中的概率最高
    result = weighted_pick(items, weights, count=3, unique=True)
    print(f"  结果: {result}")


def example_custom_wheel():
    """示例10: 自定义转盘"""
    print("\n" + "=" * 50)
    print("示例10: 自定义转盘")
    print("=" * 50)
    
    # 创建自定义转盘
    options = ["看电影", "玩游戏", "运动", "阅读", "休息", "外出"]
    colors = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#FFEAA7", "#DDA0DD"]
    
    wheel = WheelPicker(
        options,
        weights=[1, 2, 1, 1, 3, 2],  # 休息权重最高
        colors=colors,
        title="周末活动选择"
    )
    
    print("\n周末活动选项及概率:")
    config = wheel.get_wheel_config()
    for segment in config["segments"]:
        print(f"  {segment['item']}: {segment['weight']:.2%}")
    
    print("\n随机选择周末活动:")
    result = wheel.spin()
    print(f"  建议: {result['item']}")
    
    # 动态调整
    print("\n添加新选项:")
    wheel.add_item("做饭", weight=2)
    print(f"  当前选项数: {len(wheel.items)}")
    
    print("\n更新权重（增加运动权重）:")
    wheel.update_weight("运动", 5)
    
    result = wheel.spin()
    print(f"  新选择: {result['item']}")


def example_statistics_analysis():
    """示例11: 统计分析"""
    print("\n" + "=" * 50)
    print("示例11: 选择统计分析")
    print("=" * 50)
    
    items = ["A", "B", "C", "D"]
    wheel = WheelPicker(items, title="分析转盘")
    
    # 进行大量选择
    print("\n进行1000次选择...")
    for _ in range(1000):
        wheel.spin()
    
    # 查看统计
    stats = wheel.get_statistics()
    
    print("\n统计结果:")
    print(f"  总选择次数: {stats['total_spins']}")
    print(f"  分布:")
    for item, count in stats["distribution"].items():
        expected = stats["expected_distribution"][item]
        actual = stats["probability_distribution"][item]
        deviation = stats["deviation"][item]
        print(f"    {item}: 实际 {actual:.2%}, 期望 {expected:.2%}, 偏差 {deviation:.2%}")
    
    print(f"\n  最频繁: {stats['most_frequent']}")
    print(f"  最少: {stats['least_frequent']}")
    print(f"  平均偏差: {stats['average_deviation']:.4f}")


def example_all_presets():
    """示例12: 所有预设模板"""
    print("\n" + "=" * 50)
    print("示例12: 所有决策预设模板")
    print("=" * 50)
    
    presets = DecisionWheel(preset="food").get_presets()
    
    for preset_name, options in presets.items():
        print(f"\n预设 '{preset_name}':")
        print(f"  选项: {', '.join(options[:5])}...")
        
        wheel = DecisionWheel(preset=preset_name)
        decision = wheel.make_decision()
        print(f"  快速决策: {decision['decision']}")


def main():
    """运行所有示例"""
    example_basic_wheel()
    example_weighted_wheel()
    example_decision_wheel()
    example_pairing_and_grouping()
    example_tournament()
    example_prize_wheel()
    example_rotation_schedule()
    example_deterministic_selection()
    example_quick_selection()
    example_custom_wheel()
    example_statistics_analysis()
    example_all_presets()
    
    print("\n" + "=" * 50)
    print("所有示例完成!")
    print("=" * 50)


if __name__ == "__main__":
    main()
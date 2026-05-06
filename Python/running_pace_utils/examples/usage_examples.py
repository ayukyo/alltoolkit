"""
Running Pace Utils 使用示例

演示跑步配速计算工具的各种功能
"""

from mod import (
    calculate_pace, calculate_time, calculate_distance, calculate_speed,
    convert_pace, predict_race_time, calculate_splits,
    vdot_to_pace, pace_to_vdot, calculate_training_zones,
    format_pace, get_race_distance, pace, finish_time,
    PaceUnit, DistanceUnit, RACE_DISTANCES
)


def example_basic_pace():
    """基本配速计算示例"""
    print("=" * 50)
    print("基本配速计算")
    print("=" * 50)
    
    # 示例1: 计算5公里跑25分钟的配速
    result = calculate_pace(5, "25:00")
    print(f"\n5公里用时25分钟:")
    print(f"  配速: {result}")
    print(f"  每公里: {result.pace_str}")
    
    # 示例2: 计算10公里跑50分30秒的配速
    result = calculate_pace(10, "50:30")
    print(f"\n10公里用时50分30秒:")
    print(f"  配速: {result}")
    
    # 示例3: 马拉松3小时30分钟的配速
    result = calculate_pace(42.195, "3:30:00")
    print(f"\n马拉松用时3小时30分钟:")
    print(f"  配速: {result}")


def example_time_calculation():
    """时间计算示例"""
    print("\n" + "=" * 50)
    print("时间计算")
    print("=" * 50)
    
    # 示例1: 10公里配速5:30/km的完赛时间
    result = calculate_time(10, "5:30")
    print(f"\n10公里配速5:30/km:")
    print(f"  完赛时间: {result}")
    
    # 示例2: 马拉松配速5:00/km的完赛时间
    result = calculate_time(42.195, "5:00")
    print(f"\n马拉松配速5:00/km:")
    print(f"  完赛时间: {result}")
    
    # 示例3: 半马配速4:30/km的完赛时间
    result = calculate_time(21.0975, "4:30")
    print(f"\n半马配速4:30/km:")
    print(f"  完赛时间: {result}")


def example_distance_calculation():
    """距离计算示例"""
    print("\n" + "=" * 50)
    print("距离计算")
    print("=" * 50)
    
    # 示例1: 1小时配速6:00/km能跑多远
    distance = calculate_distance("1:00:00", "6:00")
    print(f"\n1小时配速6:00/km:")
    print(f"  距离: {distance} 公里")
    
    # 示例2: 30分钟配速5:00/km能跑多远
    distance = calculate_distance("30:00", "5:00")
    print(f"\n30分钟配速5:00/km:")
    print(f"  距离: {distance} 公里")


def example_speed_calculation():
    """速度计算示例"""
    print("\n" + "=" * 50)
    print("速度计算")
    print("=" * 50)
    
    # 示例1: 10公里50分钟的速度
    result = calculate_speed(10, "50:00")
    print(f"\n10公里用时50分钟:")
    print(f"  速度: {result}")
    
    # 示例2: 马拉松3小时的速度
    result = calculate_speed(42.195, "3:00:00")
    print(f"\n马拉松用时3小时:")
    print(f"  速度: {result}")


def example_pace_conversion():
    """配速转换示例"""
    print("\n" + "=" * 50)
    print("配速转换")
    print("=" * 50)
    
    # 示例1: 公里配速转英里配速
    result = convert_pace("5:00", PaceUnit.MIN_PER_KM, PaceUnit.MIN_PER_MI)
    print(f"\n5:00 /km 转换为英里:")
    print(f"  配速: {result}")
    
    # 示例2: 英里配速转公里配速
    result = convert_pace("8:00", PaceUnit.MIN_PER_MI, PaceUnit.MIN_PER_KM)
    print(f"\n8:00 /mi 转换为公里:")
    print(f"  配速: {result}")


def example_race_prediction():
    """比赛预测示例"""
    print("\n" + "=" * 50)
    print("比赛预测（Riegel公式）")
    print("=" * 50)
    
    # 基于不同距离预测
    known_distance = 5
    known_time = "25:00"
    
    print(f"\n已知: {known_distance}公里 用时 {known_time}")
    
    distances = [
        ("10K", 10),
        ("半马", 21.0975),
        ("马拉松", 42.195)
    ]
    
    for name, dist in distances:
        predicted = predict_race_time(known_distance, known_time, dist)
        print(f"  预测{name} ({dist}km): {predicted}")


def example_splits():
    """分段用时示例"""
    print("\n" + "=" * 50)
    print("分段用时计算")
    print("=" * 50)
    
    # 示例: 10公里配速5:30/km的分段
    print("\n10公里配速5:30/km分段表:")
    splits = calculate_splits(10, "5:30")
    
    print(f"{'公里':<8}{'累计距离':<12}{'本段用时':<12}{'累计用时':<12}")
    print("-" * 44)
    for split in splits:
        print(f"{split['split']:<8}{split['distance']:<12.1f}{split['split_time']:<12}{split['total_time']:<12}")


def example_vdot():
    """VDOT相关示例"""
    print("\n" + "=" * 50)
    print("VDOT训练系统")
    print("=" * 50)
    
    # VDOT转配速
    print("\nVDOT值对应的配速:")
    for vdot in [40, 50, 60]:
        pace_5k = vdot_to_pace(vdot, "5K")
        pace_marathon = vdot_to_pace(vdot, "马拉松")
        print(f"  VDOT {vdot}: 5K {pace_5k.pace_str}/km, 马拉松 {pace_marathon.pace_str}/km")
    
    # 配速转VDOT
    print("\n配速估算VDOT:")
    for pace_str in ["6:00", "5:00", "4:00"]:
        vdot = pace_to_vdot(pace_str)
        print(f"  {pace_str}/km → VDOT {vdot}")


def example_training_zones():
    """训练区间示例"""
    print("\n" + "=" * 50)
    print("训练配速区间")
    print("=" * 50)
    
    # 阈值配速5:00/km的训练区间
    threshold_pace = "5:00"
    print(f"\n阈值配速: {threshold_pace}/km")
    print("\n训练区间:")
    
    zones = calculate_training_zones(threshold_pace)
    zone_names = {
        "E": "轻松跑 (Easy)",
        "M": "马拉松配速 (Marathon)",
        "T": "阈值配速 (Threshold)",
        "I": "间歇跑 (Interval)",
        "R": "重复跑 (Repetition)"
    }
    
    for zone, pace_result in zones.items():
        print(f"  {zone} - {zone_names[zone]}: {pace_result.pace_str}/km")


def example_race_distances():
    """标准比赛距离"""
    print("\n" + "=" * 50)
    print("标准比赛距离")
    print("=" * 50)
    
    print("\n内置比赛距离:")
    for name, meters in RACE_DISTANCES.items():
        km = meters / 1000
        print(f"  {name}: {km} km")


def example_convenience_functions():
    """便捷函数示例"""
    print("\n" + "=" * 50)
    print("便捷函数")
    print("=" * 50)
    
    # 快速计算配速
    result = pace("25:00", 5)
    print(f"\npace('25:00', 5) → {result}")
    
    # 快速计算完赛时间
    result = finish_time(10, "5:30")
    print(f"finish_time(10, '5:30') → {result}")


def example_real_world_scenarios():
    """实际应用场景"""
    print("\n" + "=" * 50)
    print("实际应用场景")
    print("=" * 50)
    
    print("\n【场景1: 马拉松目标配速计算】")
    print("目标: 马拉松跑进3小时30分钟")
    target_time = "3:30:00"
    result = calculate_pace(42.195, target_time)
    print(f"  目标时间: {target_time}")
    print(f"  需要配速: {result.pace_str}/km")
    
    print("\n【场景2: 训练计划制定】")
    print("基于10公里PB 50分钟制定训练配速:")
    threshold_pace = calculate_pace(10, "50:00")
    print(f"  阈值配速: {threshold_pace.pace_str}/km")
    zones = calculate_training_zones(threshold_pace.pace_str)
    print(f"  E区(轻松跑): {zones['E'].pace_str}/km")
    print(f"  T区(节奏跑): {zones['T'].pace_str}/km")
    print(f"  I区(间歇跑): {zones['I'].pace_str}/km")
    
    print("\n【场景3: 比赛目标评估】")
    print("当前5公里成绩25分钟，评估各距离目标:")
    splits_5k = calculate_splits(5, "5:00")
    print(f"  5K配速: 5:00/km")
    print(f"  预测10K: {predict_race_time(5, '25:00', 10)}")
    print(f"  预测半马: {predict_race_time(5, '25:00', 21.0975)}")
    print(f"  预测全马: {predict_race_time(5, '25:00', 42.195)}")


def main():
    """运行所有示例"""
    example_basic_pace()
    example_time_calculation()
    example_distance_calculation()
    example_speed_calculation()
    example_pace_conversion()
    example_race_prediction()
    example_splits()
    example_vdot()
    example_training_zones()
    example_race_distances()
    example_convenience_functions()
    example_real_world_scenarios()
    
    print("\n" + "=" * 50)
    print("示例演示完成！")
    print("=" * 50)


if __name__ == "__main__":
    main()
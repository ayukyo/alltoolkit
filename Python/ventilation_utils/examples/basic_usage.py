"""
Ventilation Utils 使用示例

展示室内通风计算工具的各种应用场景
"""

import sys
sys.path.insert(0, '..')

from mod import (
    RoomInfo,
    analyze_room_ventilation,
    predict_co2_decay,
    calculate_ventilation_time,
    calculate_natural_ventilation,
    calculate_fresh_air_duct_size,
    estimate_occupancy_from_co2,
    calculate_pollutant_decay,
    calculate_hvac_requirements,
    quick_ventilation_check,
    get_air_quality_level,
    calculate_co2_steady_state,
    calculate_required_ventilation,
)


def example_office_analysis():
    """示例：办公室通风分析"""
    print("=" * 60)
    print("示例1：办公室通风分析")
    print("=" * 60)
    
    # 创建一个典型办公室
    # 10m x 8m x 3m，20人办公
    room = RoomInfo(length=10, width=8, height=3, occupants=20)
    
    print(f"\n房间参数:")
    print(f"  尺寸: {room.length}m x {room.width}m x {room.height}m")
    print(f"  体积: {room.volume}m³")
    print(f"  面积: {room.floor_area}m²")
    print(f"  人数: {room.occupants}人")
    print(f"  人均面积: {room.floor_area / room.occupants}m²/人")
    
    # 分析通风需求
    result = analyze_room_ventilation(room, room_type="office")
    
    print(f"\n通风分析结果:")
    print(f"  所需换气次数: {result.required_ach:.2f} ACH")
    print(f"  所需风量: {result.required_airflow:.0f} m³/h")
    print(f"  推荐风量: {result.recommended_airflow:.0f} m³/h")
    print(f"  通风类型: {result.ventilation_type.value}")
    print(f"  稳态CO2: {result.co2_steady_state:.0f} ppm")
    print(f"  空气质量: {result.quality_level.value}")
    print(f"\n建议:")
    for note in result.notes:
        print(f"  • {note}")


def example_classroom_co2():
    """示例：教室CO2预测"""
    print("\n" + "=" * 60)
    print("示例2：教室CO2浓度预测")
    print("=" * 60)
    
    # 创建教室：8m x 6m x 3m，30名学生
    classroom = RoomInfo(length=8, width=6, height=3, occupants=30)
    volume = classroom.volume
    
    print(f"\n教室信息:")
    print(f"  体积: {volume}m³")
    print(f"  学生数: {classroom.occupants}人")
    
    # 假设课间后CO2浓度较高
    initial_co2 = 1200  # ppm
    print(f"\n课间后CO2: {initial_co2} ppm")
    
    # 分析通风需求
    result = analyze_room_ventilation(classroom, room_type="classroom")
    airflow = result.recommended_airflow
    
    print(f"\n通风设置:")
    print(f"  推荐风量: {airflow:.0f} m³/h")
    print(f"  换气次数: {result.required_ach:.1f} ACH")
    
    # 预测上课45分钟后的CO2变化
    print(f"\n上课45分钟CO2变化预测:")
    for minutes in [15, 30, 45]:
        prediction = predict_co2_decay(
            volume=volume,
            initial_co2=initial_co2,
            airflow=airflow,
            time_minutes=minutes
        )
        quality = get_air_quality_level(prediction.final_ppm)
        print(f"  {minutes}分钟后: {prediction.final_ppm:.0f} ppm ({quality.value})")
    
    # 计算降至良好水平需要的时间
    time_to_good = calculate_ventilation_time(
        volume=volume,
        initial_co2=initial_co2,
        target_co2=800,
        airflow=airflow
    )
    print(f"\n降至800ppm需要: {time_to_good:.1f} 分钟")


def example_natural_ventilation():
    """示例：自然通风计算"""
    print("\n" + "=" * 60)
    print("示例3：自然通风计算")
    print("=" * 60)
    
    # 比较不同条件下的自然通风效果
    scenarios = [
        {"name": "微风凉爽天", "wind": 1.0, "temp_diff": 3},
        {"name": "正常通风天", "wind": 2.5, "temp_diff": 5},
        {"name": "大风天", "wind": 5.0, "temp_diff": 2},
        {"name": "无风炎热天", "wind": 0.5, "temp_diff": 8},
    ]
    
    opening_area = 1.5  # m² 窗户开口面积
    
    print(f"\n开口面积: {opening_area}m²")
    print(f"\n不同天气条件下的通风量:")
    print("-" * 60)
    
    for scenario in scenarios:
        result = calculate_natural_ventilation(
            opening_area=opening_area,
            wind_speed=scenario["wind"],
            temperature_diff=scenario["temp_diff"]
        )
        
        print(f"\n{scenario['name']}:")
        print(f"  风速: {scenario['wind']} m/s, 温差: {scenario['temp_diff']}°C")
        print(f"  风压通风: {result['wind_airflow']:.0f} m³/h")
        print(f"  热压通风: {result['stack_airflow']:.0f} m³/h")
        print(f"  总通风量: {result['total_airflow']:.0f} m³/h")
        print(f"  主要驱动: {'风力' if result['primary_driver'] == 'wind' else '热压'}")


def example_hvac_design():
    """示例：新风系统设计"""
    print("\n" + "=" * 60)
    print("示例4：会议室新风系统设计")
    print("=" * 60)
    
    # 大会议室：15m x 10m x 4m，50人
    room = RoomInfo(length=15, width=10, height=4, occupants=50)
    
    print(f"\n会议室参数:")
    print(f"  尺寸: {room.length}m x {room.width}m x {room.height}m")
    print(f"  体积: {room.volume}m³")
    print(f"  人数: {room.occupants}人")
    
    # 分析通风需求
    result = analyze_room_ventilation(room, room_type="office", standard="comfort")
    
    print(f"\n新风系统设计参数:")
    print(f"  所需风量: {result.required_airflow:.0f} m³/h")
    print(f"  推荐风量: {result.recommended_airflow:.0f} m³/h")
    
    # 计算管道尺寸
    duct = calculate_fresh_air_duct_size(result.recommended_airflow)
    
    print(f"\n管道尺寸建议:")
    print(f"  设计风速: {duct['velocity_m_s']} m/s")
    print(f"  所需面积: {duct['area_m2']*1000000:.0f} mm²")
    print(f"  圆管直径: {duct['diameter_mm']:.0f} mm")
    print(f"  推荐标准管: Φ{duct['recommended_diameter_mm']} mm")
    
    # 夏季制冷负荷
    print(f"\n夏季通风热负荷 (室外35°C → 室内24°C):")
    hvac = calculate_hvac_requirements(
        room=room,
        outdoor_temp=35,
        indoor_temp_target=24,
        ventilation_rate=result.required_ach
    )
    print(f"  热负荷: {hvac['ventilation_heat_load_kw']:.2f} kW")
    print(f"  冷量需求: {hvac['btu_per_hour']:.0f} BTU/h")


def example_air_quality_monitoring():
    """示例：空气质量监测"""
    print("\n" + "=" * 60)
    print("示例5：空气质量监测分析")
    print("=" * 60)
    
    # 创建一个房间
    room = RoomInfo(length=12, width=8, height=3)
    
    # 模拟一天中不同时段的CO2读数
    readings = [
        (8, 450, "早上开窗后"),
        (10, 650, "上午工作"),
        (12, 850, "午餐后"),
        (14, 980, "下午会议"),
        (16, 1100, "下午困倦"),
        (18, 550, "下班通风后"),
    ]
    
    print(f"\n房间体积: {room.volume}m³")
    print(f"\n一天中CO2变化与空气质量:")
    print("-" * 50)
    
    # 假设风量
    airflow = 400  # m³/h
    
    for hour, co2, description in readings:
        quality = get_air_quality_level(co2)
        
        # 估算人数
        est_occupancy = estimate_occupancy_from_co2(room, co2, airflow)
        
        print(f"\n{hour}:00 {description}")
        print(f"  CO2: {co2} ppm")
        print(f"  空气质量: {quality.value}")
        print(f"  估算人数: {est_occupancy}人")
        
        # 如果CO2偏高，计算需要多长时间通风
        if co2 > 800:
            time_to_good = calculate_ventilation_time(
                volume=room.volume,
                initial_co2=co2,
                target_co2=600,
                airflow=600  # 加强通风
            )
            print(f"  建议: 开大通风{time_to_good:.0f}分钟可降至良好水平")


def example_pollutant_removal():
    """示例：污染物去除"""
    print("\n" + "=" * 60)
    print("示例6：室内污染物去除计算")
    print("=" * 60)
    
    room_volume = 200  # m³
    
    # 模拟甲醛去除
    print("\n甲醛去除分析:")
    print(f"房间体积: {room_volume}m³")
    print(f"初始浓度: 0.15 mg/m³")
    print(f"目标浓度: 0.08 mg/m³ (国标限值)")
    
    # 不同通风方式比较
    ventilation_rates = [
        ("自然通风", 50),
        ("普通新风", 200),
        ("加强新风", 500),
    ]
    
    print(f"\n不同通风方式效果:")
    print("-" * 50)
    
    for name, airflow in ventilation_rates:
        result = calculate_pollutant_decay(
            volume=room_volume,
            initial_concentration=0.15,
            airflow=airflow,
            decay_rate=0.01,  # 甲醛自然衰减
            time_hours=2
        )
        
        ach = airflow / room_volume
        
        print(f"\n{name} ({airflow}m³/h = {ach:.1f}ACH):")
        print(f"  2小时后浓度: {result['final_concentration']:.3f} mg/m³")
        print(f"  去除率: {result['removal_percentage']:.1f}%")
        print(f"  半衰期: {result['half_life_hours']:.1f}小时")


def example_quick_check():
    """示例：快速检查"""
    print("\n" + "=" * 60)
    print("示例7：一键通风检查")
    print("=" * 60)
    
    result = quick_ventilation_check(
        room_length=8,
        room_width=6,
        room_height=3,
        occupants=15,
        room_type="office"
    )
    
    print(f"\n快速检查结果:")
    print("-" * 40)
    for key, value in result.items():
        if key == "notes":
            continue
        if isinstance(value, float):
            print(f"  {key}: {value:.2f}")
        else:
            print(f"  {key}: {value}")
    
    print(f"\n建议:")
    for note in result["notes"]:
        print(f"  • {note}")


if __name__ == "__main__":
    # 运行所有示例
    example_office_analysis()
    example_classroom_co2()
    example_natural_ventilation()
    example_hvac_design()
    example_air_quality_monitoring()
    example_pollutant_removal()
    example_quick_check()
    
    print("\n" + "=" * 60)
    print("所有示例运行完成！")
    print("=" * 60)
"""
风力等级工具基本使用示例

演示风速转换、风级查询、风向转换等基本功能。
"""

import sys
import os

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from wind_scale_utils.mod import (
    WindScaleConverter,
    WindDirection,
    WIND_DIRECTION_ENGLISH,
    get_wind_level,
    get_wind_name,
    convert_speed,
    wind_chill,
    get_wind_warning,
)


def main():
    print("=" * 60)
    print("风力等级工具基本使用示例")
    print("=" * 60)
    
    converter = WindScaleConverter()
    
    # 1. 风速单位转换
    print("\n【1. 风速单位转换】")
    print("-" * 40)
    
    speeds_ms = [5.0, 10.0, 15.0, 20.0, 30.0]
    
    print("风速转换表：")
    print(f"{'m/s':>8} | {'km/h':>10} | {'节':>10} | {'mph':>10}")
    print("-" * 44)
    
    for speed in speeds_ms:
        kmh = converter.ms_to_kmh(speed)
        knot = converter.ms_to_knot(speed)
        mph = converter.ms_to_mph(speed)
        print(f"{speed:>8.1f} | {kmh:>10.1f} | {knot:>10.1f} | {mph:>10.1f}")
    
    # 2. 蒲福风级查询
    print("\n【2. 蒲福风级查询】")
    print("-" * 40)
    
    test_speeds = [0.0, 0.5, 2.0, 4.0, 7.0, 10.0, 15.0, 20.0, 25.0, 30.0, 40.0]
    
    print("风速对应风级：")
    print(f"{'风速(m/s)':>10} | {'等级':>6} | {'中文名':>8} | {'英文名':>20}")
    print("-" * 50)
    
    for speed in test_speeds:
        info = converter.get_wind_info(speed)
        print(f"{speed:>10.1f} | {info.beaufort_level:>6} | {info.beaufort_name_cn:>8} | {info.beaufort_name_en:>20}")
    
    # 3. 风向转换
    print("\n【3. 风向转换】")
    print("-" * 40)
    
    angles = [0, 45, 90, 135, 180, 225, 270, 315]
    
    print("角度转风向：")
    print(f"{'角度':>6} | {'中文':>10} | {'英文':>20} | {'缩写':>6}")
    print("-" * 50)
    
    for angle in angles:
        direction = converter.angle_to_direction(angle)
        cn_name = direction.value
        en_name = WIND_DIRECTION_ENGLISH[direction]
        abbr = direction.name
        print(f"{angle:>6}° | {cn_name:>10} | {en_name:>20} | {abbr:>6}")
    
    # 4. 风寒指数
    print("\n【4. 风寒指数计算】")
    print("-" * 40)
    
    temperatures = [-10, -5, 0, 5]
    wind_speeds = [5, 10, 15, 20]
    
    print("体感温度表：")
    print(f"{'气温(°C)':>10} | {'风速(m/s)':>10} | {'体感(°C)':>10} | {'降低(°C)':>10}")
    print("-" * 50)
    
    for temp in temperatures:
        for speed in wind_speeds:
            chill = converter.calculate_wind_chill(temp, speed)
            diff = temp - chill
            print(f"{temp:>10} | {speed:>10} | {chill:>10.1f} | {diff:>10.1f}")
    
    # 5. 台风等级
    print("\n【5. 台风等级判断】")
    print("-" * 40)
    
    typhoon_speeds = [15.0, 20.0, 30.0, 35.0, 45.0, 55.0]
    
    print("风速对应台风等级：")
    for speed in typhoon_speeds:
        level = converter.get_typhoon_level(speed)
        if level:
            print(f"  {speed} m/s -> {level.level}: {level.description}")
    
    # 6. 飓风等级
    print("\n【6. 飓风等级判断（萨菲尔-辛普森）】")
    print("-" * 40)
    
    hurricane_speeds = [35.0, 45.0, 55.0, 65.0, 80.0]
    
    print("风速对应飓风等级：")
    for speed in hurricane_speeds:
        cat = converter.get_hurricane_category(speed)
        if cat:
            print(f"  {speed} m/s -> {cat.name}")
            print(f"    风速范围: {cat.wind_speed_min_ms}-{cat.wind_speed_max_ms} m/s")
            print(f"    风暴潮: {cat.storm_surge_min}-{cat.storm_surge_max} 米")
    
    # 7. 风力预警
    print("\n【7. 风力预警等级】")
    print("-" * 40)
    
    warning_speeds = [5.0, 10.0, 15.0, 20.0, 25.0, 30.0, 35.0]
    
    print("风速对应预警等级：")
    for speed in warning_speeds:
        warning = converter.get_wind_warning_level(speed)
        print(f"  {speed} m/s -> [{warning['color']}] {warning['name']}")
    
    # 8. 风能功率
    print("\n【8. 风能功率密度】")
    print("-" * 40)
    
    power_speeds = [5.0, 10.0, 15.0, 20.0]
    
    print("风速对应功率密度：")
    print(f"{'风速(m/s)':>10} | {'功率(W/m²)':>15}")
    print("-" * 30)
    
    for speed in power_speeds:
        power = converter.calculate_wind_power(speed)
        print(f"{speed:>10.1f} | {power:>15.1f}")
    
    # 9. 便捷函数演示
    print("\n【9. 便捷函数演示】")
    print("-" * 40)
    
    print("get_wind_level(15.0) =", get_wind_level(15.0))
    print("get_wind_name(15.0, 'cn') =", get_wind_name(15.0, 'cn'))
    print("get_wind_name(15.0, 'en') =", get_wind_name(15.0, 'en'))
    print("convert_speed(10, 'ms', 'kmh') =", convert_speed(10, 'ms', 'kmh'))
    print("wind_chill(0, 10) =", wind_chill(0, 10))
    print("get_wind_warning(20) =", get_wind_warning(20)['name'])
    
    print("\n" + "=" * 60)
    print("示例演示完成")
    print("=" * 60)


if __name__ == "__main__":
    main()
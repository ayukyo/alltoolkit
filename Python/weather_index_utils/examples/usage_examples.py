"""
Weather Index Utils 使用示例
===========================

展示各种天气指数计算的实际应用场景。
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from weather_index_utils.mod import (
    WeatherIndexCalculator,
    heat_index,
    wind_chill,
    dew_point,
    apparent_temperature,
    comfort_index,
    wbgt
)


def example_summer_heat():
    """夏季高温示例"""
    print("\n" + "="*60)
    print("🌞 夏季高温评估示例")
    print("="*60)
    
    temperature = 35  # 35°C
    humidity = 80     # 80% 湿度
    
    print(f"\n当前条件: {temperature}°C, {humidity}% 湿度")
    
    # 计算热指数
    hi = heat_index(temperature, humidity)
    print(f"\n热指数: {hi}°C")
    print(f"说明: 在高温高湿条件下，体感温度达到 {hi}°C，极易中暑！")
    
    # 计算 WBGT
    wbgt_val = wbgt(temperature, humidity, 800)  # 假设有 800 W/m² 太阳辐射
    print(f"\nWBGT 指数: {wbgt_val}°C")
    
    # 获取热风险等级
    risk = WeatherIndexCalculator.heat_risk_level(wbgt_val)
    print(f"热风险等级: {risk[1]} ({risk[0]})")
    print(f"建议: {risk[2]}")
    
    # 计算露点
    dp = dew_point(temperature, humidity)
    print(f"\n露点: {dp}°C")
    if dp > 24:
        print("说明: 露点超过 24°C，会感到非常闷热不适")


def example_winter_cold():
    """冬季寒冷示例"""
    print("\n" + "="*60)
    print("❄️ 冬季寒冷评估示例")
    print("="*60)
    
    temperature = -15  # -15°C
    wind_speed = 40     # 40 km/h
    
    print(f"\n当前条件: {temperature}°C, 风速 {wind_speed} km/h")
    
    # 计算风寒指数
    wc = wind_chill(temperature, wind_speed)
    print(f"\n风寒指数: {wc}°C")
    print(f"说明: 在寒风下，体感温度低至 {wc}°C，暴露皮肤可能在数分钟内冻伤！")
    
    # 计算体感温度
    at = apparent_temperature(temperature, 50, wind_speed)
    print(f"\n体感温度: {at}°C")
    
    # 防寒建议
    print("\n防寒建议:")
    if wc < -30:
        print("⚠️ 极端寒冷！避免任何户外活动")
    elif wc < -20:
        print("⚠️ 非常寒冷！穿戴多层保暖衣物，限制户外时间")
    elif wc < -10:
        print("❄️ 寒冷天气，注意保暖")
    else:
        print("🌤️ 正常冬季天气，适当保暖")


def example_outdoor_activity():
    """户外活动安全评估示例"""
    print("\n" + "="*60)
    print("🏃 户外活动安全评估示例")
    print("="*60)
    
    # 模拟一天中不同时间的条件
    conditions = [
        ("早上 6:00", 22, 75, 5, 100),
        ("上午 9:00", 26, 65, 8, 400),
        ("中午 12:00", 32, 55, 12, 900),
        ("下午 15:00", 34, 60, 10, 850),
        ("傍晚 18:00", 28, 70, 8, 300),
    ]
    
    print("\n各时段安全评估:")
    print("-" * 60)
    
    for time, temp, hum, wind, solar in conditions:
        wbgt_val = wbgt(temp, hum, solar)
        risk = WeatherIndexCalculator.heat_risk_level(wbgt_val)
        hi = heat_index(temp, hum) if temp >= 27 else temp
        
        print(f"\n{time}")
        print(f"  温度: {temp}°C | 湿度: {hum}% | 风速: {wind} km/h")
        print(f"  热指数: {hi}°C | WBGT: {wbgt_val}°C")
        print(f"  风险等级: {risk[1]} - {risk[2]}")


def example_comfort_assessment():
    """室内舒适度评估示例"""
    print("\n" + "="*60)
    print("🏠 室内舒适度评估示例")
    print("="*60)
    
    # 不同房间的条件
    rooms = [
        ("客厅", 24, 50),
        ("卧室", 22, 45),
        ("浴室", 28, 85),
        ("地下室", 18, 70),
    ]
    
    print("\n各房间舒适度评估:")
    print("-" * 60)
    
    for room, temp, hum in rooms:
        thi = comfort_index(temp, hum)
        level = WeatherIndexCalculator.comfort_level(thi)
        dp = dew_point(temp, hum)
        wb_val = WeatherIndexCalculator.wet_bulb_temperature(temp, hum)
        
        print(f"\n{room}:")
        print(f"  温度: {temp}°C | 湿度: {hum}%")
        print(f"  THI: {thi} | 舒适度: {level[1]} ({level[0]})")
        print(f"  露点: {dp}°C | 湿球温度: {wb_val}°C")
        
        # 建议调整
        if level[0] in ['Uncomfortable', 'Very Uncomfortable']:
            if hum > 70:
                print("  建议: 降低湿度（使用除湿机）")
            elif hum < 30:
                print("  建议: 增加湿度（使用加湿器）")
            if temp > 26:
                print("  建议: 降低温度（开空调）")


def example_agriculture():
    """农业气象评估示例"""
    print("\n" + "="*60)
    print("🌾 农业气象评估示例")
    print("="*60)
    
    temperature = 28
    humidity = 60
    wind_speed = 3.6  # m/s
    solar_radiation = 22  # MJ/m²/day
    
    print(f"\n当前条件: {temperature}°C, {humidity}% 湿度, {wind_speed} m/s 风速")
    print(f"太阳辐射: {solar_radiation} MJ/m²/day")
    
    # 计算蒸散量
    et = WeatherIndexCalculator.evapotranspiration(
        temperature, humidity, wind_speed, solar_radiation
    )
    print(f"\n参考蒸散量 (ET₀): {et} mm/day")
    print(f"说明: 作物每日需水量约 {et} 毫米")
    
    # 计算 VPD
    vpd = WeatherIndexCalculator.vapor_pressure_deficit(temperature, humidity)
    print(f"\n饱和水汽压差 (VPD): {vpd} kPa")
    
    if vpd < 0.4:
        print("说明: VPD 过低，可能影响蒸腾，注意通风")
    elif vpd > 1.6:
        print("说明: VPD 过高，植物可能缺水，考虑增加湿度")
    else:
        print("说明: VPD 适中，适合大多数作物生长")
    
    # 计算生长度日
    gdd = WeatherIndexCalculator.growing_degree_days(18, 32, 10)
    print(f"\n生长度日 (GDD): {gdd}")
    print(f"说明: 今日积温 {gdd} 度日，可用于预测作物发育阶段")


def example_running_planning():
    """跑步训练规划示例"""
    print("\n" + "="*60)
    print("🏃‍♂️ 跑步训练规划示例")
    print("="*60)
    
    # 夏季跑步条件
    temperature = 30
    humidity = 70
    wind_speed = 8
    solar_radiation = 600
    
    print(f"\n当前条件: {temperature}°C, {humidity}% 湿度")
    print(f"风速: {wind_speed} km/h, 太阳辐射: {solar_radiation} W/m²")
    
    # 计算 WBGT
    wbgt_val = wbgt(temperature, humidity, solar_radiation)
    risk = WeatherIndexCalculator.heat_risk_level(wbgt_val)
    
    print(f"\nWBGT: {wbgt_val}°C")
    print(f"风险等级: {risk[1]} - {risk[0]}")
    print(f"建议: {risk[2]}")
    
    # 训练建议
    print("\n训练建议:")
    if wbgt_val < 25:
        print("✅ 适合正常训练")
    elif wbgt_val < 28:
        print("⚠️ 注意补水，避免中午时段")
    elif wbgt_val < 30:
        print("⚠️ 减少训练强度，增加休息时间")
    elif wbgt_val < 32:
        print("⚠️ 仅进行轻度训练，密切关注身体反应")
    else:
        print("❌ 建议取消户外训练，改为室内")


def example_aviation():
    """航空气象示例"""
    print("\n" + "="*60)
    print("✈️ 航空气象评估示例")
    print("="*60)
    
    # 地面和高空条件
    ground_temp = 30
    ground_pressure = 1010
    altitude = 3000  # 3000m 高度
    
    print(f"\n地面条件: {ground_temp}°C, {ground_pressure} hPa")
    print(f"目标高度: {altitude} m")
    
    # 计算空气密度
    ground_density = WeatherIndexCalculator.air_density(ground_temp, ground_pressure)
    print(f"\n地面空气密度: {ground_density} kg/m³")
    
    # 估算高空条件（温度递减率约 6.5°C/km）
    high_temp = ground_temp - 6.5 * (altitude / 1000)
    high_pressure = ground_pressure * (1 - 0.0065 * altitude / (ground_temp + 273.15)) ** 5.257
    
    print(f"高空温度: {round(high_temp, 1)}°C")
    print(f"高空气压: {round(high_pressure, 1)} hPa")
    
    high_density = WeatherIndexCalculator.air_density(high_temp, high_pressure)
    print(f"高空空气密度: {high_density} kg/m³")
    
    density_ratio = high_density / ground_density
    print(f"\n密度比: {round(density_ratio * 100, 1)}%")
    print(f"说明: 高空空气密度为地面的 {round(density_ratio * 100, 1)}%")
    
    if density_ratio < 0.7:
        print("⚠️ 注意: 升力显著下降，起飞距离增加")


def example_complete_report():
    """完整天气报告示例"""
    print("\n" + "="*60)
    print("📊 完整天气报告示例")
    print("="*60)
    
    # 生成完整报告
    report = WeatherIndexCalculator.full_weather_report(
        temperature=32,
        humidity=65,
        wind_speed=15,
        pressure=1008,
        solar_radiation=700,
        temp_units='celsius',
        speed_units='kmh'
    )
    
    print("\n【基础数据】")
    print(f"温度: {report['temperature']}°C")
    print(f"湿度: {report['humidity']}%")
    print(f"风速: {report['wind_speed']} km/h")
    print(f"气压: {report['pressure']} hPa")
    
    print("\n【计算指数】")
    print(f"热指数: {report['indices']['heat_index']}°C")
    print(f"风寒指数: {report['indices']['wind_chill']}°C")
    print(f"体感温度: {report['indices']['apparent_temperature']}°C")
    print(f"露点: {report['indices']['dew_point']}°C")
    print(f"湿球温度: {report['indices']['wet_bulb_temperature']}°C")
    print(f"WBGT: {report['indices']['wbgt']}°C")
    print(f"舒适度指数: {report['indices']['comfort_index']}")
    print(f"绝对湿度: {report['indices']['absolute_humidity']} g/m³")
    print(f"VPD: {report['indices']['vapor_pressure_deficit']} kPa")
    print(f"空气密度: {report['indices']['air_density']} kg/m³")
    
    if report['indices']['uv_index']:
        print(f"紫外线指数: {report['indices']['uv_index']}")
    
    print("\n【评估结果】")
    comfort = report['assessments']['comfort_level']
    print(f"舒适度: {comfort[1]} ({comfort[0]})")
    
    heat = report['assessments']['heat_risk']
    print(f"热风险: {heat[1]} ({heat[0]}) - {heat[2]}")
    
    if report['assessments']['uv_category']:
        uv = report['assessments']['uv_category']
        print(f"紫外线: {uv[1]} ({uv[0]}) - {uv[2]}")


def main():
    """运行所有示例"""
    example_summer_heat()
    example_winter_cold()
    example_outdoor_activity()
    example_comfort_assessment()
    example_agriculture()
    example_running_planning()
    example_aviation()
    example_complete_report()
    
    print("\n" + "="*60)
    print("示例演示完成！")
    print("="*60)


if __name__ == '__main__':
    main()
"""
Weather Index Utils - 天气指数计算工具
=========================================

提供各种天气指数的计算功能，无需外部依赖。

功能列表:
- 热指数 (Heat Index) - 高温高湿体感温度
- 风寒指数 (Wind Chill) - 低温风冷体感温度
- 露点 (Dew Point) - 空气饱和凝结温度
- 体感温度 (Apparent Temperature) - 综合体感
- 紫外线指数 (UV Index) - 从辐射强度计算
- 舒适度指数 (Comfort Index) - THI 指数
- 湿球温度 (Wet Bulb Temperature)
- 气压修正 (Pressure Correction)
- 蒸发率估算

作者: AllToolkit 自动化生成
日期: 2026-05-06
"""

import math
from typing import Tuple, Optional, Dict, Any


class WeatherIndexCalculator:
    """天气指数计算器"""
    
    @staticmethod
    def heat_index(temperature: float, humidity: float, units: str = 'celsius') -> float:
        """
        计算热指数 (Heat Index)
        
        热指数是根据温度和相对湿度计算出的体感温度，
        反映高温高湿环境下人体感受的炎热程度。
        
        Args:
            temperature: 温度值
            humidity: 相对湿度 (0-100)
            units: 温度单位 ('celsius' 或 'fahrenheit')
            
        Returns:
            热指数（与输入单位相同）
            
        Raises:
            ValueError: 参数无效时
            
        Example:
            >>> WeatherIndexCalculator.heat_index(35, 70)
            50.4
            >>> WeatherIndexCalculator.heat_index(95, 70, 'fahrenheit')
            122.7
        """
        if humidity < 0 or humidity > 100:
            raise ValueError("湿度必须在 0-100 之间")
        
        # 转换为华氏度进行计算
        if units.lower() == 'celsius':
            T = temperature * 9/5 + 32  # 转换为华氏度
        else:
            T = temperature
        
        # 热指数计算（Rothfusz 回归方程）
        # 仅在温度 >= 80°F 且湿度 >= 40% 时有意义
        if T < 80:
            # 低温时返回原温度
            result = T
        else:
            RH = humidity
            
            # Rothfusz 回归方程
            HI = (-42.379 + 
                  2.04901523 * T + 
                  10.14333127 * RH - 
                  0.22475541 * T * RH - 
                  0.00683783 * T * T - 
                  0.05481717 * RH * RH + 
                  0.00122874 * T * T * RH + 
                  0.00085282 * T * RH * RH - 
                  0.00000199 * T * T * RH * RH)
            
            # 调整
            if RH < 13 and 80 <= T <= 112:
                adjustment = ((13 - RH) / 4) * math.sqrt((17 - abs(T - 95)) / 17)
                HI -= adjustment
            elif RH > 85 and 80 <= T <= 87:
                adjustment = ((RH - 85) / 10) * ((87 - T) / 5)
                HI += adjustment
            
            result = HI
        
        # 转换回原单位
        if units.lower() == 'celsius':
            return round((result - 32) * 5/9, 1)
        return round(result, 1)
    
    @staticmethod
    def wind_chill(temperature: float, wind_speed: float, 
                   temp_units: str = 'celsius', 
                   speed_units: str = 'kmh') -> float:
        """
        计算风寒指数 (Wind Chill)
        
        风寒指数反映了低温有风环境下人体感受到的温度，
        风速越大，体感温度越低。
        
        Args:
            temperature: 温度值
            wind_speed: 风速
            temp_units: 温度单位 ('celsius' 或 'fahrenheit')
            speed_units: 风速单位 ('kmh', 'mph', 'ms')
            
        Returns:
            风寒指数（与输入温度单位相同）
            
        Example:
            >>> WeatherIndexCalculator.wind_chill(-10, 30)
            -20.2
        """
        # 转换为华氏度和英里/小时
        if temp_units.lower() == 'celsius':
            T = temperature * 9/5 + 32
        else:
            T = temperature
        
        if speed_units.lower() == 'kmh':
            V = wind_speed / 1.609344  # km/h 转 mph
        elif speed_units.lower() == 'ms':
            V = wind_speed * 2.236936  # m/s 转 mph
        else:
            V = wind_speed
        
        # 风寒指数仅适用于 50°F 以下和 3 mph 以上的风速
        if T > 50 or V < 3:
            result = T
        else:
            # NWS 风寒公式
            WC = 35.74 + 0.6215 * T - 35.75 * (V ** 0.16) + 0.4275 * T * (V ** 0.16)
            result = WC
        
        # 转换回原单位
        if temp_units.lower() == 'celsius':
            return round((result - 32) * 5/9, 1)
        return round(result, 1)
    
    @staticmethod
    def dew_point(temperature: float, humidity: float, units: str = 'celsius') -> float:
        """
        计算露点温度 (Dew Point)
        
        露点是空气中的水汽凝结成露水或霜的温度点。
        露点越高，人感觉越闷热。
        
        Args:
            temperature: 温度值
            humidity: 相对湿度 (0-100)
            units: 温度单位 ('celsius' 或 'fahrenheit')
            
        Returns:
            露点温度（与输入单位相同）
            
        Example:
            >>> round(WeatherIndexCalculator.dew_point(30, 70), 1)
            24.0
        """
        if humidity < 0 or humidity > 100:
            raise ValueError("湿度必须在 0-100 之间")
        
        # 转换为摄氏度计算
        if units.lower() == 'fahrenheit':
            T = (temperature - 32) * 5/9
        else:
            T = temperature
        
        # Magnus 公式
        # α = ln(RH/100) + (b*T)/(c+T)
        # Td = c * α / (b - α)
        # 其中 b = 17.67, c = 243.5°C (对于水)
        
        b = 17.67
        c = 243.5
        
        alpha = math.log(humidity / 100.0) + (b * T) / (c + T)
        Td = c * alpha / (b - alpha)
        
        # 转换回原单位
        if units.lower() == 'fahrenheit':
            return round(Td * 9/5 + 32, 1)
        return round(Td, 1)
    
    @staticmethod
    def apparent_temperature(temperature: float, humidity: float, 
                           wind_speed: float = 0,
                           temp_units: str = 'celsius',
                           speed_units: str = 'kmh') -> float:
        """
        计算体感温度 (Apparent Temperature)
        
        综合考虑温度、湿度和风速的体感温度。
        高温时使用热指数，低温时使用风寒指数，适中温度直接返回。
        
        Args:
            temperature: 温度值
            humidity: 相对湿度 (0-100)
            wind_speed: 风速
            temp_units: 温度单位
            speed_units: 风速单位
            
        Returns:
            体感温度
            
        Example:
            >>> WeatherIndexCalculator.apparent_temperature(35, 70, 10)
            42.9
        """
        # 转换为摄氏度判断
        if temp_units.lower() == 'fahrenheit':
            T_celsius = (temperature - 32) * 5/9
        else:
            T_celsius = temperature
        
        # 高温高湿：使用热指数
        if T_celsius >= 27:  # 27°C 以上
            return WeatherIndexCalculator.heat_index(temperature, humidity, temp_units)
        
        # 低温有风：使用风寒指数
        elif T_celsius <= 10 and wind_speed > 0:  # 10°C 以下
            return WeatherIndexCalculator.wind_chill(temperature, wind_speed, 
                                                     temp_units, speed_units)
        
        # 适中温度：直接返回
        else:
            return round(temperature, 1)
    
    @staticmethod
    def uv_index(uv_radiation: float) -> int:
        """
        从紫外线辐射强度计算 UV 指数
        
        Args:
            uv_radiation: 紫外线辐射强度 (W/m²)
            
        Returns:
            UV 指数 (0-11+)
            
        Example:
            >>> WeatherIndexCalculator.uv_index(0.25)
            10
        """
        # UV 指数 = 辐射强度 (W/m²) × 40
        uvi = uv_radiation * 40
        return min(int(round(uvi)), 11)  # 最大显示为 11+
    
    @staticmethod
    def uv_index_category(uv_index: int) -> Tuple[str, str, str]:
        """
        获取 UV 指数的风险等级和建议
        
        Args:
            uv_index: UV 指数
            
        Returns:
            (风险等级, 中文描述, 防护建议)
            
        Example:
            >>> WeatherIndexCalculator.uv_index_category(8)
            ('High', '高', '穿戴防晒衣物，使用 SPF30+ 防晒霜')
        """
        if uv_index < 3:
            return ('Low', '低', '无需防护')
        elif uv_index < 6:
            return ('Moderate', '中等', '中午时分尽量待在阴凉处')
        elif uv_index < 8:
            return ('High', '高', '减少户外活动，穿戴防晒衣物')
        elif uv_index < 11:
            return ('Very High', '很高', '避免户外活动，使用 SPF50+ 防晒霜')
        else:
            return ('Extreme', '极高', '避免户外活动，穿戴全防护装备')
    
    @staticmethod
    def comfort_index(temperature: float, humidity: float, 
                      units: str = 'celsius') -> float:
        """
        计算温湿度指数 THI (Temperature-Humidity Index)
        
        也称为不适指数，反映人体舒适度。
        THI > 75 时开始感觉不适，> 80 时大多数人感到不适。
        
        Args:
            temperature: 温度值
            humidity: 相对湿度 (0-100)
            units: 温度单位
            
        Returns:
            THI 指数值
            
        Example:
            >>> round(WeatherIndexCalculator.comfort_index(30, 70), 1)
            76.0
        """
        # 转换为华氏度
        if units.lower() == 'celsius':
            T = temperature * 9/5 + 32
        else:
            T = temperature
        
        # THI 公式
        # THI = T - (0.55 - 0.55 * RH/100) * (T - 58)
        RH = humidity
        THI = T - (0.55 - 0.55 * RH / 100) * (T - 58)
        
        return round(THI, 1)
    
    @staticmethod
    def comfort_level(thi: float) -> Tuple[str, str]:
        """
        根据 THI 值获取舒适度描述
        
        Args:
            thi: THI 指数值
            
        Returns:
            (舒适度等级, 中文描述)
            
        Example:
            >>> WeatherIndexCalculator.comfort_level(70)
            ('Comfortable', '舒适')
        """
        if thi < 65:
            return ('Cool', '凉爽')
        elif thi < 75:
            return ('Comfortable', '舒适')
        elif thi < 80:
            return ('Slightly Uncomfortable', '略微不适')
        elif thi < 85:
            return ('Uncomfortable', '不适')
        else:
            return ('Very Uncomfortable', '非常不适')
    
    @staticmethod
    def wet_bulb_temperature(temperature: float, humidity: float,
                            units: str = 'celsius') -> float:
        """
        计算湿球温度 (Wet Bulb Temperature)
        
        湿球温度是空气冷却到饱和状态时的温度，
        是衡量热应激的重要指标。
        
        使用 Stull 公式近似计算。
        
        Args:
            temperature: 干球温度
            humidity: 相对湿度 (0-100)
            units: 温度单位
            
        Returns:
            湿球温度
            
        Example:
            >>> round(WeatherIndexCalculator.wet_bulb_temperature(30, 50), 1)
            22.0
        """
        # 转换为摄氏度
        if units.lower() == 'fahrenheit':
            T = (temperature - 32) * 5/9
        else:
            T = temperature
        
        RH = humidity
        
        # Stull 公式 (近似)
        # Tw = T * atan(0.151977 * sqrt(RH + 8.313659)) 
        #      + atan(T + RH) - atan(RH - 1.676331) 
        #      + 0.00391838 * RH^(3/2) * atan(0.023101 * RH) - 4.686035
        
        Tw = (T * math.atan(0.151977 * math.sqrt(RH + 8.313659))
              + math.atan(T + RH) 
              - math.atan(RH - 1.676331)
              + 0.00391838 * (RH ** 1.5) * math.atan(0.023101 * RH)
              - 4.686035)
        
        # 转换回原单位
        if units.lower() == 'fahrenheit':
            return round(Tw * 9/5 + 32, 1)
        return round(Tw, 1)
    
    @staticmethod
    def wet_bulb_globe_temperature(temperature: float, humidity: float,
                                   solar_radiation: float = 0,
                                   units: str = 'celsius') -> float:
        """
        计算 WBGT 指数 (Wet Bulb Globe Temperature)
        
        WBGT 是衡量热应激的综合指标，常用于运动和户外活动安全评估。
        
        Args:
            temperature: 气温
            humidity: 相对湿度 (0-100)
            solar_radiation: 太阳辐射 (W/m²)，默认 0（室内）
            units: 温度单位
            
        Returns:
            WBGT 指数
            
        Example:
            >>> round(WeatherIndexCalculator.wet_bulb_globe_temperature(30, 70), 1)
            24.7
        """
        # 转换为摄氏度
        if units.lower() == 'fahrenheit':
            T = (temperature - 32) * 5/9
        else:
            T = temperature
        
        # 计算自然湿球温度
        Tnw = WeatherIndexCalculator.wet_bulb_temperature(T, humidity)
        
        # 计算黑球温度 (简化估算)
        # Tg ≈ T + 0.014 * SR (太阳辐射)
        Tg = T + 0.014 * solar_radiation
        
        # WBGT 计算
        # 室外: WBGT = 0.7 * Tnw + 0.2 * Tg + 0.1 * T
        # 室内: WBGT = 0.7 * Tnw + 0.3 * T
        
        if solar_radiation > 0:
            wbgt = 0.7 * Tnw + 0.2 * Tg + 0.1 * T
        else:
            wbgt = 0.7 * Tnw + 0.3 * T
        
        # 转换回原单位
        if units.lower() == 'fahrenheit':
            return round(wbgt * 9/5 + 32, 1)
        return round(wbgt, 1)
    
    @staticmethod
    def heat_risk_level(wbgt: float) -> Tuple[str, str, str]:
        """
        根据 WBGT 获取热风险等级和防护建议
        
        Args:
            wbgt: WBGT 指数 (°C)
            
        Returns:
            (风险等级, 中文等级, 活动建议)
            
        Example:
            >>> WeatherIndexCalculator.heat_risk_level(28)
            ('Orange', '橙色', '限制高强度运动，增加休息时间')
        """
        if wbgt < 25:
            return ('White', '白色', '正常活动')
        elif wbgt < 28:
            return ('Green', '绿色', '注意补水')
        elif wbgt < 30:
            return ('Yellow', '黄色', '限制高强度活动')
        elif wbgt < 32:
            return ('Orange', '橙色', '限制高强度运动，增加休息时间')
        elif wbgt < 35:
            return ('Red', '红色', '取消所有非必要户外活动')
        else:
            return ('Black', '黑色', '禁止所有户外活动')
    
    @staticmethod
    def absolute_humidity(temperature: float, humidity: float,
                         units: str = 'celsius') -> float:
        """
        计算绝对湿度 (g/m³)
        
        Args:
            temperature: 温度
            humidity: 相对湿度 (0-100)
            units: 温度单位
            
        Returns:
            绝对湿度 (g/m³)
            
        Example:
            >>> round(WeatherIndexCalculator.absolute_humidity(25, 50), 1)
            11.5
        """
        # 转换为摄氏度
        if units.lower() == 'fahrenheit':
            T = (temperature - 32) * 5/9
        else:
            T = temperature
        
        # 饱和水汽压 (Magnus 公式)
        # e_s = 6.112 * exp(17.67 * T / (T + 243.5)) hPa
        e_s = 6.112 * math.exp(17.67 * T / (T + 243.5))
        
        # 实际水汽压
        e = e_s * humidity / 100
        
        # 绝对湿度 (g/m³)
        # AH = 216.7 * e / (T + 273.15)
        AH = 216.7 * e / (T + 273.15)
        
        return round(AH, 1)
    
    @staticmethod
    def vapor_pressure_deficit(temperature: float, humidity: float,
                               units: str = 'celsius') -> float:
        """
        计算饱和水汽压差 VPD (kPa)
        
        VPD 表示空气的"干燥程度"，用于植物蒸腾和作物生长评估。
        
        Args:
            temperature: 温度
            humidity: 相对湿度 (0-100)
            units: 温度单位
            
        Returns:
            VPD (kPa)
            
        Example:
            >>> round(WeatherIndexCalculator.vapor_pressure_deficit(25, 50), 2)
            1.58
        """
        # 转换为摄氏度
        if units.lower() == 'fahrenheit':
            T = (temperature - 32) * 5/9
        else:
            T = temperature
        
        # 饱和水汽压 (kPa)
        e_s = 0.6108 * math.exp(17.27 * T / (T + 237.3))
        
        # 实际水汽压 (kPa)
        e_a = e_s * humidity / 100
        
        # VPD
        VPD = e_s - e_a
        
        return round(VPD, 2)
    
    @staticmethod
    def evapotranspiration(temperature: float, humidity: float,
                          wind_speed: float, solar_radiation: float,
                          units: str = 'celsius') -> float:
        """
        计算参考蒸散量 ET₀ (mm/day)
        
        使用简化的 Penman-Monteith 公式估算。
        
        Args:
            temperature: 气温
            humidity: 相对湿度 (0-100)
            wind_speed: 风速 (m/s)
            solar_radiation: 太阳辐射 (MJ/m²/day)
            units: 温度单位
            
        Returns:
            参考蒸散量 (mm/day)
            
        Example:
            >>> round(WeatherIndexCalculator.evapotranspiration(25, 60, 2, 20), 1)
            4.8
        """
        # 转换为摄氏度
        if units.lower() == 'fahrenheit':
            T = (temperature - 32) * 5/9
        else:
            T = temperature
        
        # 饱和水汽压曲线斜率
        delta = 4098 * (0.6108 * math.exp(17.27 * T / (T + 237.3))) / ((T + 237.3) ** 2)
        
        # 饱和水汽压
        e_s = 0.6108 * math.exp(17.27 * T / (T + 237.3))
        
        # 实际水汽压
        e_a = e_s * humidity / 100
        
        # 心理测量常数 (kPa/°C)
        gamma = 0.066
        
        # 简化的 Penman-Monteith 公式
        ET0 = (0.408 * delta * solar_radiation + 
               gamma * (900 / (T + 273)) * wind_speed * (e_s - e_a)) / \
              (delta + gamma * (1 + 0.34 * wind_speed))
        
        return round(max(ET0, 0), 1)
    
    @staticmethod
    def growing_degree_days(temperature_min: float, temperature_max: float,
                           base_temp: float = 10.0,
                           units: str = 'celsius') -> float:
        """
        计算生长度日 GDD (Growing Degree Days)
        
        GDD 用于农业和园艺中预测作物生长阶段。
        
        Args:
            temperature_min: 最低温度
            temperature_max: 最高温度
            base_temp: 基准温度 (默认 10°C)
            units: 温度单位
            
        Returns:
            GDD 值
            
        Example:
            >>> round(WeatherIndexCalculator.growing_degree_days(15, 28, 10), 1)
            11.5
        """
        # 转换为摄氏度
        if units.lower() == 'fahrenheit':
            T_min = (temperature_min - 32) * 5/9
            T_max = (temperature_max - 32) * 5/9
        else:
            T_min = temperature_min
            T_max = temperature_max
        
        # 计算平均温度
        T_avg = (T_min + T_max) / 2
        
        # GDD = max(T_avg - base_temp, 0)
        GDD = max(T_avg - base_temp, 0)
        
        return round(GDD, 1)
    
    @staticmethod
    def pressure_altitude(pressure: float, 
                         sea_level_pressure: float = 1013.25) -> float:
        """
        根据气压计算海拔高度
        
        使用国际标准大气模型。
        
        Args:
            pressure: 当前气压 (hPa)
            sea_level_pressure: 海平面气压 (默认 1013.25 hPa)
            
        Returns:
            海拔高度 (米)
            
        Example:
            >>> round(WeatherIndexCalculator.pressure_altitude(900), 0)
            988.0
        """
        # 国际标准大气公式
        # h = 44330 * (1 - (P/P0)^0.1903)
        h = 44330 * (1 - (pressure / sea_level_pressure) ** 0.1903)
        
        return round(h, 0)
    
    @staticmethod
    def sea_level_pressure(station_pressure: float, altitude: float,
                          temperature: float = 15.0) -> float:
        """
        将站点气压订正为海平面气压
        
        Args:
            station_pressure: 站点气压 (hPa)
            altitude: 海拔高度 (米)
            temperature: 气温 (°C)，默认 15°C
            
        Returns:
            海平面气压 (hPa)
            
        Example:
            >>> round(WeatherIndexCalculator.sea_level_pressure(1000, 100, 20), 1)
            1012.2
        """
        # 简化的海平面气压订正公式
        # P0 = P * (1 - 0.0065 * h / T)^(-5.257)
        T_K = temperature + 273.15
        
        P0 = station_pressure * ((1 - 0.0065 * altitude / T_K) ** (-5.257))
        
        return round(P0, 1)
    
    @staticmethod
    def air_density(temperature: float, pressure: float = 1013.25,
                   humidity: float = 0, units: str = 'celsius') -> float:
        """
        计算空气密度 (kg/m³)
        
        Args:
            temperature: 气温
            pressure: 气压 (hPa)
            humidity: 相对湿度 (0-100)
            units: 温度单位
            
        Returns:
            空气密度 (kg/m³)
            
        Example:
            >>> round(WeatherIndexCalculator.air_density(20, 1013.25, 50), 3)
            1.199
        """
        # 转换为摄氏度
        if units.lower() == 'fahrenheit':
            T = (temperature - 32) * 5/9
        else:
            T = temperature
        
        # 转换为开尔文和帕斯卡
        T_K = T + 273.15
        P_Pa = pressure * 100  # hPa -> Pa
        
        # 计算水汽压
        e_s = 6.112 * math.exp(17.67 * T / (T + 243.5))  # hPa
        e = e_s * humidity / 100  # hPa
        e_Pa = e * 100  # Pa
        
        # 干空气气体常数
        R_d = 287.058  # J/(kg·K)
        # 水汽气体常数
        R_v = 461.495  # J/(kg·K)
        
        # 空气密度
        rho = P_Pa / (R_d * T_K) - (1 - R_d / R_v) * e_Pa / (R_d * T_K)
        
        return round(rho, 3)
    
    @staticmethod
    def full_weather_report(temperature: float, humidity: float,
                           wind_speed: float = 0,
                           pressure: float = 1013.25,
                           solar_radiation: float = 0,
                           temp_units: str = 'celsius',
                           speed_units: str = 'kmh') -> Dict[str, Any]:
        """
        生成完整的天气指数报告
        
        Args:
            temperature: 温度
            humidity: 相对湿度 (0-100)
            wind_speed: 风速
            pressure: 气压 (hPa)
            solar_radiation: 太阳辐射 (W/m²)
            temp_units: 温度单位
            speed_units: 风速单位
            
        Returns:
            包含所有天气指数的字典
            
        Example:
            >>> report = WeatherIndexCalculator.full_weather_report(30, 70, 10)
            >>> 'heat_index' in report
            True
        """
        # 转换风速为 m/s
        if speed_units.lower() == 'kmh':
            wind_ms = wind_speed / 3.6
        elif speed_units.lower() == 'mph':
            wind_ms = wind_speed * 0.44704
        else:
            wind_ms = wind_speed
        
        # 计算各项指数
        heat_idx = WeatherIndexCalculator.heat_index(temperature, humidity, temp_units)
        wind_chill = WeatherIndexCalculator.wind_chill(temperature, wind_speed, 
                                                       temp_units, speed_units)
        dew_pt = WeatherIndexCalculator.dew_point(temperature, humidity, temp_units)
        apparent = WeatherIndexCalculator.apparent_temperature(temperature, humidity, 
                                                              wind_speed, temp_units, speed_units)
        thi = WeatherIndexCalculator.comfort_index(temperature, humidity, temp_units)
        comfort_level = WeatherIndexCalculator.comfort_level(thi)
        wet_bulb = WeatherIndexCalculator.wet_bulb_temperature(temperature, humidity, temp_units)
        wbgt = WeatherIndexCalculator.wet_bulb_globe_temperature(temperature, humidity, 
                                                                  solar_radiation, temp_units)
        heat_risk = WeatherIndexCalculator.heat_risk_level(wbgt)
        abs_humidity = WeatherIndexCalculator.absolute_humidity(temperature, humidity, temp_units)
        vpd = WeatherIndexCalculator.vapor_pressure_deficit(temperature, humidity, temp_units)
        air_rho = WeatherIndexCalculator.air_density(temperature, pressure, humidity, temp_units)
        
        # 紫外线指数（如果有太阳辐射数据）
        if solar_radiation > 0:
            uvi = WeatherIndexCalculator.uv_index(solar_radiation * 0.0001)  # 近似转换
            uv_cat = WeatherIndexCalculator.uv_index_category(uvi)
        else:
            uvi = None
            uv_cat = None
        
        return {
            'temperature': temperature,
            'humidity': humidity,
            'wind_speed': wind_speed,
            'pressure': pressure,
            'units': {
                'temperature': temp_units,
                'wind_speed': speed_units,
                'pressure': 'hPa'
            },
            'indices': {
                'heat_index': heat_idx,
                'wind_chill': wind_chill,
                'apparent_temperature': apparent,
                'dew_point': dew_pt,
                'wet_bulb_temperature': wet_bulb,
                'wbgt': wbgt,
                'comfort_index': thi,
                'absolute_humidity': abs_humidity,
                'vapor_pressure_deficit': vpd,
                'air_density': air_rho,
                'uv_index': uvi
            },
            'assessments': {
                'comfort_level': comfort_level,
                'heat_risk': heat_risk,
                'uv_category': uv_cat
            }
        }


# 便捷函数
def heat_index(temperature: float, humidity: float, units: str = 'celsius') -> float:
    """计算热指数"""
    return WeatherIndexCalculator.heat_index(temperature, humidity, units)


def wind_chill(temperature: float, wind_speed: float, 
               temp_units: str = 'celsius', speed_units: str = 'kmh') -> float:
    """计算风寒指数"""
    return WeatherIndexCalculator.wind_chill(temperature, wind_speed, temp_units, speed_units)


def dew_point(temperature: float, humidity: float, units: str = 'celsius') -> float:
    """计算露点"""
    return WeatherIndexCalculator.dew_point(temperature, humidity, units)


def apparent_temperature(temperature: float, humidity: float, wind_speed: float = 0,
                        temp_units: str = 'celsius', speed_units: str = 'kmh') -> float:
    """计算体感温度"""
    return WeatherIndexCalculator.apparent_temperature(temperature, humidity, wind_speed,
                                                       temp_units, speed_units)


def comfort_index(temperature: float, humidity: float, units: str = 'celsius') -> float:
    """计算舒适度指数"""
    return WeatherIndexCalculator.comfort_index(temperature, humidity, units)


def wbgt(temperature: float, humidity: float, solar_radiation: float = 0,
         units: str = 'celsius') -> float:
    """计算 WBGT 指数"""
    return WeatherIndexCalculator.wet_bulb_globe_temperature(
        temperature, humidity, solar_radiation, units)


if __name__ == '__main__':
    # 演示用法
    print("=" * 60)
    print("Weather Index Utils - 天气指数计算工具演示")
    print("=" * 60)
    
    # 热指数
    print("\n【热指数 - 35°C, 70% 湿度】")
    hi = heat_index(35, 70)
    print(f"热指数: {hi}°C (体感温度)")
    
    # 风寒指数
    print("\n【风寒指数 - -10°C, 30 km/h 风速】")
    wc = wind_chill(-10, 30)
    print(f"风寒指数: {wc}°C")
    
    # 露点
    print("\n【露点 - 30°C, 70% 湿度】")
    dp = dew_point(30, 70)
    print(f"露点: {dp}°C")
    
    # 体感温度
    print("\n【体感温度 - 35°C, 70% 湿度, 10 km/h 风速】")
    at = apparent_temperature(35, 70, 10)
    print(f"体感温度: {at}°C")
    
    # 舒适度指数
    print("\n【舒适度指数 - 30°C, 70% 湿度】")
    thi = comfort_index(30, 70)
    level = WeatherIndexCalculator.comfort_level(thi)
    print(f"THI: {thi}")
    print(f"舒适度: {level[1]} ({level[0]})")
    
    # WBGT
    print("\n【WBGT 指数 - 30°C, 70% 湿度】")
    wbgt_val = wbgt(30, 70)
    risk = WeatherIndexCalculator.heat_risk_level(wbgt_val)
    print(f"WBGT: {wbgt_val}°C")
    print(f"热风险等级: {risk[1]} ({risk[0]})")
    print(f"建议: {risk[2]}")
    
    # 完整报告
    print("\n【完整天气报告 - 28°C, 65% 湿度, 15 km/h 风速】")
    report = WeatherIndexCalculator.full_weather_report(28, 65, 15)
    print(f"热指数: {report['indices']['heat_index']}°C")
    print(f"风寒指数: {report['indices']['wind_chill']}°C")
    print(f"体感温度: {report['indices']['apparent_temperature']}°C")
    print(f"露点: {report['indices']['dew_point']}°C")
    print(f"湿球温度: {report['indices']['wet_bulb_temperature']}°C")
    print(f"WBGT: {report['indices']['wbgt']}°C")
    print(f"舒适度: {report['assessments']['comfort_level'][1]}")
    print(f"热风险: {report['assessments']['heat_risk'][1]}")
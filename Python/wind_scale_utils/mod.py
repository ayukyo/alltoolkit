"""
Wind Scale Utilities - 风力等级工具

提供完整的风力等级功能，包括：
- 风速到风力等级转换（蒲福风级 Beaufort Scale）
- 风力等级到风速范围转换
- 风力等级详细描述（海面状况、陆地状况）
- 台风/飓风等级分类（Saffir-Simpson 飓风等级）
- 风向角度与名称转换
- 风玫瑰图数据生成
- 风寒指数计算

零外部依赖，纯 Python 实现。
"""

from dataclasses import dataclass
from enum import Enum
from typing import List, Dict, Tuple, Optional
import math


class WindDirection(Enum):
    """风向枚举（16方位）"""
    N = "北风"
    NNE = "北东北风"
    NE = "东北风"
    ENE = "东东北风"
    E = "东风"
    ESE = "东东南风"
    SE = "东南风"
    SSE = "南东南风"
    S = "南风"
    SSW = "南西南风"
    SW = "西南风"
    WSW = "西西南风"
    W = "西风"
    WNW = "西西北风"
    NW = "西北风"
    NNW = "北西北风"


# 风向角度范围（度）
WIND_DIRECTION_RANGES = {
    WindDirection.N: (348.75, 11.25),
    WindDirection.NNE: (11.25, 33.75),
    WindDirection.NE: (33.75, 56.25),
    WindDirection.ENE: (56.25, 78.75),
    WindDirection.E: (78.75, 101.25),
    WindDirection.ESE: (101.25, 123.75),
    WindDirection.SE: (123.75, 146.25),
    WindDirection.SSE: (146.25, 168.75),
    WindDirection.S: (168.75, 191.25),
    WindDirection.SSW: (191.25, 213.75),
    WindDirection.SW: (213.75, 236.25),
    WindDirection.WSW: (236.25, 258.75),
    WindDirection.W: (258.75, 281.25),
    WindDirection.WNW: (281.25, 303.75),
    WindDirection.NW: (303.75, 326.25),
    WindDirection.NNW: (326.25, 348.75),
}

# 风向英文名称
WIND_DIRECTION_ENGLISH = {
    WindDirection.N: "North",
    WindDirection.NNE: "North-Northeast",
    WindDirection.NE: "Northeast",
    WindDirection.ENE: "East-Northeast",
    WindDirection.E: "East",
    WindDirection.ESE: "East-Southeast",
    WindDirection.SE: "Southeast",
    WindDirection.SSE: "South-Southeast",
    WindDirection.S: "South",
    WindDirection.SSW: "South-Southwest",
    WindDirection.SW: "Southwest",
    WindDirection.WSW: "West-Southwest",
    WindDirection.W: "West",
    WindDirection.WNW: "West-Northwest",
    WindDirection.NW: "Northwest",
    WindDirection.NNW: "North-Northwest",
}

# 风向缩写
WIND_DIRECTION_ABBR = {
    WindDirection.N: "N",
    WindDirection.NNE: "NNE",
    WindDirection.NE: "NE",
    WindDirection.ENE: "ENE",
    WindDirection.E: "E",
    WindDirection.ESE: "ESE",
    WindDirection.SE: "SE",
    WindDirection.SSE: "SSE",
    WindDirection.S: "S",
    WindDirection.SSW: "SSW",
    WindDirection.SW: "SW",
    WindDirection.WSW: "WSW",
    WindDirection.W: "W",
    WindDirection.WNW: "WNW",
    WindDirection.NW: "NW",
    WindDirection.NNW: "NNW",
}


@dataclass
class BeaufortLevel:
    """蒲福风级等级数据"""
    level: int                    # 风力等级（0-12）
    name_cn: str                  # 中文名称
    name_en: str                  # 英文名称
    wind_speed_min: float         # 最小风速（m/s）
    wind_speed_max: float         # 最大风速（m/s）
    wind_speed_min_kmh: float     # 最小风速（km/h）
    wind_speed_max_kmh: float     # 最大风速（km/h）
    wind_speed_min_knot: float    # 最小风速（节）
    wind_speed_max_knot: float    # 最大风速（节）
    sea_description: str          # 海面状况描述
    land_description: str         # 陆地状况描述
    wave_height_min: float        # 最小浪高（米）
    wave_height_max: float        # 最大浪高（米）


# 蒲福风级表（Beaufort Wind Scale）
BEAUFORT_SCALE: List[BeaufortLevel] = [
    BeaufortLevel(
        level=0,
        name_cn="无风",
        name_en="Calm",
        wind_speed_min=0.0, wind_speed_max=0.2,
        wind_speed_min_kmh=0.0, wind_speed_max_kmh=1.0,
        wind_speed_min_knot=0.0, wind_speed_max_knot=1.0,
        sea_description="海面如镜",
        land_description="烟直上",
        wave_height_min=0.0, wave_height_max=0.0
    ),
    BeaufortLevel(
        level=1,
        name_cn="软风",
        name_en="Light Air",
        wind_speed_min=0.3, wind_speed_max=1.5,
        wind_speed_min_kmh=1.0, wind_speed_max_kmh=5.0,
        wind_speed_min_knot=1.0, wind_speed_max_knot=3.0,
        sea_description="海面有鳞状波纹，无浪花",
        land_description="烟能表示风向，风向标不能转动",
        wave_height_min=0.0, wave_height_max=0.1
    ),
    BeaufortLevel(
        level=2,
        name_cn="轻风",
        name_en="Light Breeze",
        wind_speed_min=1.6, wind_speed_max=3.3,
        wind_speed_min_kmh=6.0, wind_speed_max_kmh=11.0,
        wind_speed_min_knot=4.0, wind_speed_max_knot=6.0,
        sea_description="小波，波峰平滑，无浪花",
        land_description="人面感觉有风，树叶微响，风向标能转动",
        wave_height_min=0.1, wave_height_max=0.3
    ),
    BeaufortLevel(
        level=3,
        name_cn="微风",
        name_en="Gentle Breeze",
        wind_speed_min=3.4, wind_speed_max=5.4,
        wind_speed_min_kmh=12.0, wind_speed_max_kmh=19.0,
        wind_speed_min_knot=7.0, wind_speed_max_knot=10.0,
        sea_description="小波加大，波峰开始破碎，间有白浪花",
        land_description="树叶和小枝摇动，旗帜展开",
        wave_height_min=0.3, wave_height_max=1.0
    ),
    BeaufortLevel(
        level=4,
        name_cn="和风",
        name_en="Moderate Breeze",
        wind_speed_min=5.5, wind_speed_max=7.9,
        wind_speed_min_kmh=20.0, wind_speed_max_kmh=28.0,
        wind_speed_min_knot=11.0, wind_speed_max_knot=16.0,
        sea_description="小浪，波峰开始破碎，白浪较多",
        land_description="能吹起地面的灰尘和纸张，树枝摇动",
        wave_height_min=1.0, wave_height_max=1.5
    ),
    BeaufortLevel(
        level=5,
        name_cn="清风",
        name_en="Fresh Breeze",
        wind_speed_min=8.0, wind_speed_max=10.7,
        wind_speed_min_kmh=29.0, wind_speed_max_kmh=38.0,
        wind_speed_min_knot=17.0, wind_speed_max_knot=21.0,
        sea_description="中浪，波峰较长，白浪更多，间有浪花飞溅",
        land_description="有叶的小树摇摆，内陆水面有微波",
        wave_height_min=1.5, wave_height_max=2.5
    ),
    BeaufortLevel(
        level=6,
        name_cn="强风",
        name_en="Strong Breeze",
        wind_speed_min=10.8, wind_speed_max=13.8,
        wind_speed_min_kmh=39.0, wind_speed_max_kmh=49.0,
        wind_speed_min_knot=22.0, wind_speed_max_knot=27.0,
        sea_description="大浪开始形成，白浪到处可见，有浪花飞溅",
        land_description="大树枝摇动，电线呼呼有声，举伞困难",
        wave_height_min=2.5, wave_height_max=4.0
    ),
    BeaufortLevel(
        level=7,
        name_cn="疾风",
        name_en="Near Gale",
        wind_speed_min=13.9, wind_speed_max=17.1,
        wind_speed_min_kmh=50.0, wind_speed_max_kmh=61.0,
        wind_speed_min_knot=28.0, wind_speed_max_knot=33.0,
        sea_description="海面堆积，波峰破碎成浪花，沿风向成条纹",
        land_description="全树摇动，行人感觉不便",
        wave_height_min=4.0, wave_height_max=5.5
    ),
    BeaufortLevel(
        level=8,
        name_cn="大风",
        name_en="Gale",
        wind_speed_min=17.2, wind_speed_max=20.7,
        wind_speed_min_kmh=62.0, wind_speed_max_kmh=74.0,
        wind_speed_min_knot=34.0, wind_speed_max_knot=40.0,
        sea_description="大浪，波峰边缘开始破碎成浪花，条纹更明显",
        land_description="树枝折断，人向前行阻力很大",
        wave_height_min=5.5, wave_height_max=7.5
    ),
    BeaufortLevel(
        level=9,
        name_cn="烈风",
        name_en="Strong Gale",
        wind_speed_min=20.8, wind_speed_max=24.4,
        wind_speed_min_kmh=75.0, wind_speed_max_kmh=88.0,
        wind_speed_min_knot=41.0, wind_speed_max_knot=47.0,
        sea_description="巨浪，波峰倒卷，浪花密集，能见度降低",
        land_description="建筑物有损坏，屋顶瓦片掀起",
        wave_height_min=7.0, wave_height_max=10.0
    ),
    BeaufortLevel(
        level=10,
        name_cn="狂风",
        name_en="Storm",
        wind_speed_min=24.5, wind_speed_max=28.4,
        wind_speed_min_kmh=89.0, wind_speed_max_kmh=102.0,
        wind_speed_min_knot=48.0, wind_speed_max_knot=55.0,
        sea_description="狂涛，海面白茫茫，能见度差",
        land_description="树木连根拔起，建筑物损坏严重",
        wave_height_min=9.0, wave_height_max=12.5
    ),
    BeaufortLevel(
        level=11,
        name_cn="暴风",
        name_en="Violent Storm",
        wind_speed_min=28.5, wind_speed_max=32.6,
        wind_speed_min_kmh=103.0, wind_speed_max_kmh=117.0,
        wind_speed_min_knot=56.0, wind_speed_max_knot=63.0,
        sea_description="异常狂涛，海面完全被浪花覆盖，能见度很差",
        land_description="大范围破坏，少见",
        wave_height_min=11.5, wave_height_max=16.0
    ),
    BeaufortLevel(
        level=12,
        name_cn="飓风",
        name_en="Hurricane",
        wind_speed_min=32.7, wind_speed_max=999.0,
        wind_speed_min_kmh=118.0, wind_speed_max_kmh=999.0,
        wind_speed_min_knot=64.0, wind_speed_max_knot=999.0,
        sea_description="空中充满浪花和飞沫，海面完全变白，能见度极差",
        land_description="毁灭性破坏",
        wave_height_min=14.0, wave_height_max=999.0
    ),
]


@dataclass
class HurricaneCategory:
    """萨菲尔-辛普森飓风等级"""
    category: int                 # 等级（1-5）
    name: str                     # 名称
    wind_speed_min_knot: float    # 最小风速（节）
    wind_speed_max_knot: float    # 最大风速（节）
    wind_speed_min_kmh: float     # 最小风速（km/h）
    wind_speed_max_kmh: float     # 最大风速（km/h）
    wind_speed_min_ms: float      # 最小风速（m/s）
    wind_speed_max_ms: float      # 最大风速（m/s）
    description: str              # 破坏程度描述
    storm_surge_min: float        # 最小风暴潮高度（米）
    storm_surge_max: float        # 最大风暴潮高度（米）


# 萨菲尔-辛普森飓风等级
SAFFIR_SIMPSON_SCALE: List[HurricaneCategory] = [
    HurricaneCategory(
        category=1,
        name="一级飓风",
        wind_speed_min_knot=64.0, wind_speed_max_knot=82.0,
        wind_speed_min_kmh=119.0, wind_speed_max_kmh=153.0,
        wind_speed_min_ms=33.0, wind_speed_max_ms=42.0,
        description="部分屋顶材料、屋架和门损坏；部分海岸道路和低水位出口道路洪水泛滥；小型船只可能断锚",
        storm_surge_min=1.2, storm_surge_max=1.5
    ),
    HurricaneCategory(
        category=2,
        name="二级飓风",
        wind_speed_min_knot=83.0, wind_speed_max_knot=95.0,
        wind_speed_min_kmh=154.0, wind_speed_max_kmh=177.0,
        wind_speed_min_ms=43.0, wind_speed_max_ms=49.0,
        description="屋顶和门窗损坏严重；低水位出口道路被淹；小型船只断锚；机动船只可能遇险",
        storm_surge_min=1.8, storm_surge_max=2.4
    ),
    HurricaneCategory(
        category=3,
        name="三级飓风",
        wind_speed_min_knot=96.0, wind_speed_max_knot=112.0,
        wind_speed_min_kmh=178.0, wind_speed_max_kmh=208.0,
        wind_speed_min_ms=50.0, wind_speed_max_ms=58.0,
        description="小建筑屋顶被毁；大型建筑被浪击损坏；可能发生洪水；近海小建筑被摧毁；大型建筑漂浮物增多",
        storm_surge_min=2.7, storm_surge_max=3.7
    ),
    HurricaneCategory(
        category=4,
        name="四级飓风",
        wind_speed_min_knot=113.0, wind_speed_max_knot=136.0,
        wind_speed_min_kmh=209.0, wind_speed_max_kmh=251.0,
        wind_speed_min_ms=58.0, wind_speed_max_ms=70.0,
        description="小型建筑屋顶彻底损坏；风暴潮和浪击造成海滩侵蚀；低水位地区可能被淹没数公里",
        storm_surge_min=4.0, storm_surge_max=5.5
    ),
    HurricaneCategory(
        category=5,
        name="五级飓风",
        wind_speed_min_knot=137.0, wind_speed_max_knot=999.0,
        wind_speed_min_kmh=252.0, wind_speed_max_kmh=999.0,
        wind_speed_min_ms=70.0, wind_speed_max_ms=999.0,
        description="许多建筑和工业建筑屋顶彻底损坏；小型建筑翻转或吹飞；低水位地区洪水泛滥严重",
        storm_surge_min=5.5, storm_surge_max=999.0
    ),
]


@dataclass
class TyphoonLevel:
    """台风等级（中国标准）"""
    level: str                    # 等级名称
    wind_speed_min_ms: float     # 最小风速（m/s）
    wind_speed_max_ms: float      # 最大风速（m/s）
    description: str             # 描述


# 台风等级（中国气象局标准）
TYPHOON_LEVELS: List[TyphoonLevel] = [
    TyphoonLevel(
        level="热带低压",
        wind_speed_min_ms=10.8, wind_speed_max_ms=17.1,
        description="中心附近最大风力6-7级"
    ),
    TyphoonLevel(
        level="热带风暴",
        wind_speed_min_ms=17.2, wind_speed_max_ms=24.4,
        description="中心附近最大风力8-9级"
    ),
    TyphoonLevel(
        level="强热带风暴",
        wind_speed_min_ms=24.5, wind_speed_max_ms=32.6,
        description="中心附近最大风力10-11级"
    ),
    TyphoonLevel(
        level="台风",
        wind_speed_min_ms=32.7, wind_speed_max_ms=41.4,
        description="中心附近最大风力12-13级"
    ),
    TyphoonLevel(
        level="强台风",
        wind_speed_min_ms=41.5, wind_speed_max_ms=50.9,
        description="中心附近最大风力14-15级"
    ),
    TyphoonLevel(
        level="超强台风",
        wind_speed_min_ms=51.0, wind_speed_max_ms=999.0,
        description="中心附近最大风力16级或以上"
    ),
]


@dataclass
class WindInfo:
    """风速转换结果"""
    beaufort_level: int                    # 蒲福风级
    beaufort_name_cn: str                   # 蒲福风级中文名
    beaufort_name_en: str                   # 蒲福风级英文名
    wind_speed_ms: float                    # 风速（m/s）
    wind_speed_kmh: float                   # 风速（km/h）
    wind_speed_knot: float                  # 风速（节）
    wind_speed_mph: float                   # 风速（英里/小时）
    sea_description: str                    # 海面状况
    land_description: str                   # 陆地状况
    wave_height_range: Tuple[float, float]  # 浪高范围（米）


class WindScaleConverter:
    """风力等级转换工具类"""
    
    def __init__(self):
        self.beaufort_scale = BEAUFORT_SCALE
        self.hurricane_scale = SAFFIR_SIMPSON_SCALE
        self.typhoon_levels = TYPHOON_LEVELS
    
    def ms_to_kmh(self, speed_ms: float) -> float:
        """风速 m/s 转 km/h"""
        return speed_ms * 3.6
    
    def ms_to_knot(self, speed_ms: float) -> float:
        """风速 m/s 转 节"""
        return speed_ms * 1.94384
    
    def ms_to_mph(self, speed_ms: float) -> float:
        """风速 m/s 转 英里/小时"""
        return speed_ms * 2.23694
    
    def kmh_to_ms(self, speed_kmh: float) -> float:
        """风速 km/h 转 m/s"""
        return speed_kmh / 3.6
    
    def knot_to_ms(self, speed_knot: float) -> float:
        """风速 节 转 m/s"""
        return speed_knot / 1.94384
    
    def mph_to_ms(self, speed_mph: float) -> float:
        """风速 英里/小时 转 m/s"""
        return speed_mph / 2.23694
    
    def get_beaufort_level(self, speed_ms: float) -> BeaufortLevel:
        """
        根据风速获取蒲福风级
        
        Args:
            speed_ms: 风速（m/s）
            
        Returns:
            BeaufortLevel 对象
        """
        for level in self.beaufort_scale:
            if speed_ms <= level.wind_speed_max:
                return level
        return self.beaufort_scale[-1]  # 返回最大等级
    
    def get_wind_info(self, speed_ms: float) -> WindInfo:
        """
        获取风速详细信息
        
        Args:
            speed_ms: 风速（m/s）
            
        Returns:
            WindInfo 对象
        """
        level = self.get_beaufort_level(speed_ms)
        
        return WindInfo(
            beaufort_level=level.level,
            beaufort_name_cn=level.name_cn,
            beaufort_name_en=level.name_en,
            wind_speed_ms=speed_ms,
            wind_speed_kmh=self.ms_to_kmh(speed_ms),
            wind_speed_knot=self.ms_to_knot(speed_ms),
            wind_speed_mph=self.ms_to_mph(speed_ms),
            sea_description=level.sea_description,
            land_description=level.land_description,
            wave_height_range=(level.wave_height_min, level.wave_height_max)
        )
    
    def get_hurricane_category(self, speed_ms: float) -> Optional[HurricaneCategory]:
        """
        获取飓风等级（萨菲尔-辛普森等级）
        
        Args:
            speed_ms: 风速（m/s）
            
        Returns:
            HurricaneCategory 对象，如果低于飓风级别返回 None
        """
        speed_knot = self.ms_to_knot(speed_ms)
        
        # 检查是否达到飓风级别（最小64节）
        if speed_knot < 64.0:
            return None
        
        for cat in self.hurricane_scale:
            if speed_knot <= cat.wind_speed_max_knot:
                return cat
        return self.hurricane_scale[-1]
    
    def get_typhoon_level(self, speed_ms: float) -> Optional[TyphoonLevel]:
        """
        获取台风等级（中国标准）
        
        Args:
            speed_ms: 风速（m/s）
            
        Returns:
            TyphoonLevel 对象，如果低于热带低压返回 None
        """
        # 检查是否达到热带低压级别（最小10.8 m/s）
        if speed_ms < 10.8:
            return None
        
        for level in self.typhoon_levels:
            if speed_ms <= level.wind_speed_max_ms:
                return level
        return self.typhoon_levels[-1]
    
    def angle_to_direction(self, angle: float) -> WindDirection:
        """
        角度转风向
        
        Args:
            angle: 风向角度（0-360度，北为0度，顺时针）
            
        Returns:
            WindDirection 枚举
        """
        angle = angle % 360
        
        for direction, (min_angle, max_angle) in WIND_DIRECTION_RANGES.items():
            if direction == WindDirection.N:
                # 北风是特殊情况，跨越 360/0 度
                if angle >= min_angle or angle < max_angle:
                    return direction
            else:
                if min_angle <= angle < max_angle:
                    return direction
        
        return WindDirection.N
    
    def direction_to_angle(self, direction: WindDirection) -> float:
        """
        风向转角度
        
        Args:
            direction: WindDirection 枚举
            
        Returns:
            风向角度（北为0度，顺时针）
        """
        # 16方位的中心角度
        direction_angles = {
            WindDirection.N: 0.0,
            WindDirection.NNE: 22.5,
            WindDirection.NE: 45.0,
            WindDirection.ENE: 67.5,
            WindDirection.E: 90.0,
            WindDirection.ESE: 112.5,
            WindDirection.SE: 135.0,
            WindDirection.SSE: 157.5,
            WindDirection.S: 180.0,
            WindDirection.SSW: 202.5,
            WindDirection.SW: 225.0,
            WindDirection.WSW: 247.5,
            WindDirection.W: 270.0,
            WindDirection.WNW: 292.5,
            WindDirection.NW: 315.0,
            WindDirection.NNW: 337.5,
        }
        return direction_angles[direction]
    
    def calculate_wind_chill(
        self,
        temperature_c: float,
        speed_ms: float
    ) -> float:
        """
        计算风寒指数（体感温度）
        
        使用美国国家气象局公式：
        Wind Chill = 13.12 + 0.6215*T - 11.37*V^0.16 + 0.3965*T*V^0.16
        
        Args:
            temperature_c: 气温（摄氏度）
            speed_ms: 风速（m/s）
            
        Returns:
            体感温度（摄氏度）
        """
        # 只在气温低于 10°C 且风速大于 1.3 m/s 时计算风寒指数
        if temperature_c >= 10.0 or speed_ms <= 1.3:
            return temperature_c
        
        # 转换风速为 km/h
        speed_kmh = self.ms_to_kmh(speed_ms)
        
        # 计算风寒指数
        wind_chill = (
            13.12
            + 0.6215 * temperature_c
            - 11.37 * (speed_kmh ** 0.16)
            + 0.3965 * temperature_c * (speed_kmh ** 0.16)
        )
        
        return round(wind_chill, 1)
    
    def generate_wind_rose_data(
        self,
        wind_data: List[Dict[str, float]]
    ) -> Dict[str, Dict[str, float]]:
        """
        生成风玫瑰图数据
        
        Args:
            wind_data: 风向风速数据列表，每个元素包含 'direction' (角度) 和 'speed' (m/s)
            
        Returns:
            按风向分组的统计数据
        """
        result = {}
        
        # 初始化所有方向
        for direction in WindDirection:
            result[direction.name] = {
                'count': 0,
                'total_speed': 0.0,
                'max_speed': 0.0,
                'min_speed': float('inf'),
                'direction_cn': direction.value,
                'direction_en': WIND_DIRECTION_ENGLISH[direction],
                'angle': self.direction_to_angle(direction),
            }
        
        # 统计数据
        for data in wind_data:
            angle = data.get('direction', 0)
            speed = data.get('speed', 0)
            
            direction = self.angle_to_direction(angle)
            key = direction.name
            
            result[key]['count'] += 1
            result[key]['total_speed'] += speed
            result[key]['max_speed'] = max(result[key]['max_speed'], speed)
            result[key]['min_speed'] = min(result[key]['min_speed'], speed)
        
        # 计算平均风速
        for key in result:
            if result[key]['count'] > 0:
                result[key]['avg_speed'] = round(
                    result[key]['total_speed'] / result[key]['count'], 2
                )
                result[key]['min_speed'] = round(result[key]['min_speed'], 2)
                result[key]['max_speed'] = round(result[key]['max_speed'], 2)
            else:
                result[key]['avg_speed'] = 0.0
                result[key]['min_speed'] = 0.0
                result[key]['max_speed'] = 0.0
        
        return result
    
    def get_wind_warning_level(self, speed_ms: float) -> Dict[str, any]:
        """
        获取风力预警等级（中国标准）
        
        Args:
            speed_ms: 风速（m/s）
            
        Returns:
            预警等级信息
        """
        level = self.get_beaufort_level(speed_ms)
        
        # 中国风力预警信号标准
        if speed_ms < 10.8:
            return {
                'level': 0,
                'name': '无预警',
                'color': '绿色',
                'description': '风力正常'
            }
        elif speed_ms < 17.2:
            return {
                'level': 1,
                'name': '蓝色预警',
                'color': '蓝色',
                'description': '24小时内可能受大风影响，平均风力可达6级以上'
            }
        elif speed_ms < 24.5:
            return {
                'level': 2,
                'name': '黄色预警',
                'color': '黄色',
                'description': '12小时内可能受大风影响，平均风力可达8级以上'
            }
        elif speed_ms < 32.7:
            return {
                'level': 3,
                'name': '橙色预警',
                'color': '橙色',
                'description': '6小时内可能受大风影响，平均风力可达10级以上'
            }
        else:
            return {
                'level': 4,
                'name': '红色预警',
                'color': '红色',
                'description': '6小时内可能受大风影响，平均风力可达12级以上'
            }
    
    def calculate_wind_power(self, speed_ms: float, area: float = 1.0) -> float:
        """
        计算风能功率密度（单位面积）
        
        P = 0.5 * ρ * v³
        
        Args:
            speed_ms: 风速（m/s）
            area: 面积（m²），默认 1 m²
            
        Returns:
            功率（瓦特）
        """
        # 空气密度（标准大气压，15°C）
        air_density = 1.225  # kg/m³
        
        power = 0.5 * air_density * (speed_ms ** 3) * area
        return round(power, 2)


# 便捷函数
def get_wind_level(speed_ms: float) -> int:
    """获取蒲福风级的便捷函数"""
    converter = WindScaleConverter()
    level = converter.get_beaufort_level(speed_ms)
    return level.level


def get_wind_name(speed_ms: float, lang: str = 'cn') -> str:
    """获取风力名称的便捷函数"""
    converter = WindScaleConverter()
    level = converter.get_beaufort_level(speed_ms)
    return level.name_cn if lang == 'cn' else level.name_en


def convert_speed(value: float, from_unit: str, to_unit: str) -> float:
    """
    风速单位转换便捷函数
    
    Args:
        value: 风速值
        from_unit: 原单位（ms/kmh/knot/mph）
        to_unit: 目标单位（ms/kmh/knot/mph）
        
    Returns:
        转换后的风速值
    """
    converter = WindScaleConverter()
    
    # 先转成 m/s
    speed_ms = value
    if from_unit == 'kmh':
        speed_ms = converter.kmh_to_ms(value)
    elif from_unit == 'knot':
        speed_ms = converter.knot_to_ms(value)
    elif from_unit == 'mph':
        speed_ms = converter.mph_to_ms(value)
    
    # 再转成目标单位
    if to_unit == 'kmh':
        return converter.ms_to_kmh(speed_ms)
    elif to_unit == 'knot':
        return converter.ms_to_knot(speed_ms)
    elif to_unit == 'mph':
        return converter.ms_to_mph(speed_ms)
    
    return speed_ms


def wind_chill(temperature_c: float, speed_ms: float) -> float:
    """计算风寒指数的便捷函数"""
    converter = WindScaleConverter()
    return converter.calculate_wind_chill(temperature_c, speed_ms)


def get_wind_warning(speed_ms: float) -> Dict[str, any]:
    """获取风力预警的便捷函数"""
    converter = WindScaleConverter()
    return converter.get_wind_warning_level(speed_ms)


if __name__ == "__main__":
    print("=== 风力等级工具演示 ===\n")
    
    converter = WindScaleConverter()
    
    # 测试风速转换
    print("--- 风速转换 ---")
    speed_ms = 15.0
    print(f"风速: {speed_ms} m/s")
    print(f"  = {converter.ms_to_kmh(speed_ms):.1f} km/h")
    print(f"  = {converter.ms_to_knot(speed_ms):.1f} 节")
    print(f"  = {converter.ms_to_mph(speed_ms):.1f} mph")
    
    # 测试蒲福风级
    print("\n--- 蒲福风级 ---")
    info = converter.get_wind_info(speed_ms)
    print(f"等级: {info.beaufort_level} ({info.beaufort_name_cn} / {info.beaufort_name_en})")
    print(f"海面状况: {info.sea_description}")
    print(f"陆地状况: {info.land_description}")
    print(f"浪高范围: {info.wave_height_range[0]}-{info.wave_height_range[1]} 米")
    
    # 测试风向转换
    print("\n--- 风向转换 ---")
    angle = 225
    direction = converter.angle_to_direction(angle)
    print(f"角度 {angle}° = {direction.value} ({WIND_DIRECTION_ENGLISH[direction]})")
    print(f"{direction.value} 的角度 = {converter.direction_to_angle(direction)}°")
    
    # 测试风寒指数
    print("\n--- 风寒指数 ---")
    temp = 5.0
    wind_speed = 10.0
    chill = converter.calculate_wind_chill(temp, wind_speed)
    print(f"气温: {temp}°C, 风速: {wind_speed} m/s")
    print(f"体感温度: {chill}°C")
    
    # 测试台风等级
    print("\n--- 台风等级 ---")
    typhoon_speeds = [15.0, 25.0, 35.0, 45.0, 55.0]
    for speed in typhoon_speeds:
        level = converter.get_typhoon_level(speed)
        if level:
            print(f"风速 {speed} m/s -> {level.level}: {level.description}")
    
    # 测试飓风等级
    print("\n--- 飓风等级 ---")
    hurricane_speeds = [35.0, 45.0, 55.0, 65.0, 80.0]
    for speed in hurricane_speeds:
        cat = converter.get_hurricane_category(speed)
        if cat:
            print(f"风速 {speed} m/s -> {cat.name}")
    
    # 测试预警等级
    print("\n--- 风力预警 ---")
    warning_speeds = [8.0, 15.0, 22.0, 30.0, 40.0]
    for speed in warning_speeds:
        warning = converter.get_wind_warning_level(speed)
        print(f"风速 {speed} m/s -> {warning['name']}: {warning['description']}")
    
    # 测试风能功率
    print("\n--- 风能功率 ---")
    power_speeds = [5.0, 10.0, 15.0, 20.0]
    for speed in power_speeds:
        power = converter.calculate_wind_power(speed)
        print(f"风速 {speed} m/s -> 功率密度: {power:.1f} W/m²")
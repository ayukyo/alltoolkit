"""
astronomy_utils - 天文学工具

提供天文学计算功能：行星数据、星座位置、天体升起/落下时间、
儒略日计算、天体距离等。

零外部依赖，纯 Python 实现。

Author: AllToolkit
Date: 2026-05-24
"""

from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from math import sin, cos, tan, asin, acos, atan2, radians, degrees, sqrt, pi, floor
from datetime import datetime, timedelta


@dataclass
class CelestialBody:
    """天体数据"""
    name: str                    # 英文名
    name_cn: str                 # 中文名
    body_type: str               # 类型 (planet, moon, star, dwarf_planet)
    mass_kg: float               # 质量 (千克)
    radius_km: float             # 半径 (千米)
    orbital_period_days: float   # 公转周期 (地球日)
    rotation_period_hours: float # 自转周期 (小时)
    distance_au: float           # 与太阳平均距离 (天文单位)
    moons: int                   # 卫星数量
    magnitude: float             # 视星等
    color: str                   # 颜色描述
    
    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "name_cn": self.name_cn,
            "body_type": self.body_type,
            "mass_kg": self.mass_kg,
            "radius_km": self.radius_km,
            "orbital_period_days": self.orbital_period_days,
            "rotation_period_hours": self.rotation_period_hours,
            "distance_au": self.distance_au,
            "moons": self.moons,
            "magnitude": self.magnitude,
            "color": self.color,
        }


@dataclass
class Constellation:
    """星座数据"""
    name: str                    # 英文名
    name_cn: str                 # 中文名
    abbreviation: str            # 缩写
    area_sq_deg: float           # 面积 (平方度)
    brightest_star: str          # 最亮星
    best_month: int              # 最佳观测月份 (1-12)
    description: str             # 描述
    
    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "name_cn": self.name_cn,
            "abbreviation": self.abbreviation,
            "area_sq_deg": self.area_sq_deg,
            "brightest_star": self.brightest_star,
            "best_month": self.best_month,
            "description": self.description,
        }


@dataclass
class RiseSetTimes:
    """升起落下时间"""
    rise_time: datetime          # 升起时间
    transit_time: datetime       # 中天时间
    set_time: datetime           # 落下时间
    is_circumpolar: bool         # 是否拱极星（永不落下）
    is_never_rises: bool         # 是否永不升起
    
    def to_dict(self) -> Dict:
        return {
            "rise_time": self.rise_time.isoformat() if self.rise_time else None,
            "transit_time": self.transit_time.isoformat() if self.transit_time else None,
            "set_time": self.set_time.isoformat() if self.set_time else None,
            "is_circumpolar": self.is_circumpolar,
            "is_never_rises": self.is_never_rises,
        }


class SolarSystemData:
    """太阳系数据"""
    
    # 太阳数据
    SUN = CelestialBody(
        name="Sun", name_cn="太阳", body_type="star",
        mass_kg=1.989e30, radius_km=696340,
        orbital_period_days=0, rotation_period_hours=609.12,
        distance_au=0, moons=0, magnitude=-26.74, color="黄白色"
    )
    
    # 行星数据
    PLANETS = {
        "Mercury": CelestialBody(
            name="Mercury", name_cn="水星", body_type="planet",
            mass_kg=3.285e23, radius_km=2439.7,
            orbital_period_days=87.97, rotation_period_hours=1407.6,
            distance_au=0.387, moons=0, magnitude=-0.42, color="灰色"
        ),
        "Venus": CelestialBody(
            name="Venus", name_cn="金星", body_type="planet",
            mass_kg=4.867e24, radius_km=6051.8,
            orbital_period_days=224.7, rotation_period_hours=-5832.5,  # 逆向自转
            distance_au=0.723, moons=0, magnitude=-4.14, color="黄白色"
        ),
        "Earth": CelestialBody(
            name="Earth", name_cn="地球", body_type="planet",
            mass_kg=5.972e24, radius_km=6371,
            orbital_period_days=365.25, rotation_period_hours=23.93,
            distance_au=1.0, moons=1, magnitude=-3.99, color="蓝绿色"
        ),
        "Mars": CelestialBody(
            name="Mars", name_cn="火星", body_type="planet",
            mass_kg=6.39e23, radius_km=3389.5,
            orbital_period_days=687, rotation_period_hours=24.62,
            distance_au=1.524, moons=2, magnitude=-1.52, color="红色"
        ),
        "Jupiter": CelestialBody(
            name="Jupiter", name_cn="木星", body_type="planet",
            mass_kg=1.898e27, radius_km=69911,
            orbital_period_days=4333, rotation_period_hours=9.93,
            distance_au=5.203, moons=95, magnitude=-2.20, color="橙黄色条纹"
        ),
        "Saturn": CelestialBody(
            name="Saturn", name_cn="土星", body_type="planet",
            mass_kg=5.683e26, radius_km=58232,
            orbital_period_days=10759, rotation_period_hours=10.7,
            distance_au=9.537, moons=146, magnitude=0.46, color="淡黄色"
        ),
        "Uranus": CelestialBody(
            name="Uranus", name_cn="天王星", body_type="planet",
            mass_kg=8.681e25, radius_km=25362,
            orbital_period_days=30687, rotation_period_hours=-17.24,  # 逆向自转
            distance_au=19.19, moons=28, magnitude=5.68, color="青蓝色"
        ),
        "Neptune": CelestialBody(
            name="Neptune", name_cn="海王星", body_type="planet",
            mass_kg=1.024e26, radius_km=24622,
            orbital_period_days=60190, rotation_period_hours=16.11,
            distance_au=30.07, moons=16, magnitude=7.78, color="深蓝色"
        ),
    }
    
    # 矮行星
    DWARF_PLANETS = {
        "Pluto": CelestialBody(
            name="Pluto", name_cn="冥王星", body_type="dwarf_planet",
            mass_kg=1.303e22, radius_km=1188.3,
            orbital_period_days=90560, rotation_period_hours=-153.3,
            distance_au=39.48, moons=5, magnitude=13.65, color="褐黄色"
        ),
        "Ceres": CelestialBody(
            name="Ceres", name_cn="谷神星", body_type="dwarf_planet",
            mass_kg=9.393e20, radius_km=469.73,
            orbital_period_days=1682, rotation_period_hours=9.07,
            distance_au=2.77, moons=0, magnitude=6.64, color="深灰色"
        ),
        "Eris": CelestialBody(
            name="Eris", name_cn="阋神星", body_type="dwarf_planet",
            mass_kg=1.66e22, radius_km=1163,
            orbital_period_days=203830, rotation_period_hours=25.9,
            distance_au=67.7, moons=1, magnitude=18.7, color="灰白色"
        ),
    }
    
    # 月球数据
    MOON = CelestialBody(
        name="Moon", name_cn="月球", body_type="moon",
        mass_kg=7.342e22, radius_km=1737.4,
        orbital_period_days=27.32, rotation_period_hours=655.7,
        distance_au=0.00257, moons=0, magnitude=-12.74, color="灰白色"
    )
    
    @classmethod
    def get_all_planets(cls) -> List[CelestialBody]:
        """获取所有行星"""
        return list(cls.PLANETS.values())
    
    @classmethod
    def get_planet(cls, name: str) -> Optional[CelestialBody]:
        """根据名称获取行星（支持中英文名）"""
        name_lower = name.lower()
        for planet in cls.PLANETS.values():
            if planet.name.lower() == name_lower or planet.name_cn == name:
                return planet
        return None


class ConstellationData:
    """星座数据"""
    
    # 黄道十二宫
    ZODIAC = {
        "Aries": Constellation(
            name="Aries", name_cn="白羊座", abbreviation="Ari",
            area_sq_deg=441, brightest_star="娄宿三",
            best_month=12, description="黄道第一宫，象征勇气与活力"
        ),
        "Taurus": Constellation(
            name="Taurus", name_cn="金牛座", abbreviation="Tau",
            area_sq_deg=797, brightest_star="毕宿五",
            best_month=1, description="黄道第二宫，象征稳定与力量"
        ),
        "Gemini": Constellation(
            name="Gemini", name_cn="双子座", abbreviation="Gem",
            area_sq_deg=514, brightest_star="北河三",
            best_month=2, description="黄道第三宫，象征沟通与变化"
        ),
        "Cancer": Constellation(
            name="Cancer", name_cn="巨蟹座", abbreviation="Cnc",
            area_sq_deg=506, brightest_star="柳宿增三",
            best_month=3, description="黄道第四宫，象征家庭与情感"
        ),
        "Leo": Constellation(
            name="Leo", name_cn="狮子座", abbreviation="Leo",
            area_sq_deg=947, brightest_star="轩辕十四",
            best_month=4, description="黄道第五宫，象征领导与自信"
        ),
        "Virgo": Constellation(
            name="Virgo", name_cn="室女座", abbreviation="Vir",
            area_sq_deg=1294, brightest_star="角宿一",
            best_month=5, description="黄道第六宫，象征分析与服务"
        ),
        "Libra": Constellation(
            name="Libra", name_cn="天秤座", abbreviation="Lib",
            area_sq_deg=538, brightest_star="氐宿一",
            best_month=6, description="黄道第七宫，象征平衡与和谐"
        ),
        "Scorpius": Constellation(
            name="Scorpius", name_cn="天蝎座", abbreviation="Sco",
            area_sq_deg=497, brightest_star="心宿二",
            best_month=7, description="黄道第八宫，象征神秘与洞察"
        ),
        "Sagittarius": Constellation(
            name="Sagittarius", name_cn="人马座", abbreviation="Sgr",
            area_sq_deg=867, brightest_star="箕宿三",
            best_month=8, description="黄道第九宫，象征探索与自由"
        ),
        "Capricornus": Constellation(
            name="Capricornus", name_cn="摩羯座", abbreviation="Cap",
            area_sq_deg=414, brightest_star="牛宿一",
            best_month=9, description="黄道第十宫，象征责任与成就"
        ),
        "Aquarius": Constellation(
            name="Aquarius", name_cn="宝瓶座", abbreviation="Aqr",
            area_sq_deg=980, brightest_star="虚宿一",
            best_month=10, description="黄道第十一宫，象征创新与独立"
        ),
        "Pisces": Constellation(
            name="Pisces", name_cn="双鱼座", abbreviation="Psc",
            area_sq_deg=889, brightest_star="外屏七",
            best_month=11, description="黄道第十二宫，象征梦想与直觉"
        ),
    }
    
    # 北半球常见星座
    NORTHERN = {
        "Ursa Major": Constellation(
            name="Ursa Major", name_cn="大熊座", abbreviation="UMa",
            area_sq_deg=1280, brightest_star="北斗一",
            best_month=4, description="北斗七星所在星座，全年可见"
        ),
        "Ursa Minor": Constellation(
            name="Ursa Minor", name_cn="小熊座", abbreviation="UMi",
            area_sq_deg=256, brightest_star="北极星",
            best_month=6, description="包含北极星，指引方向"
        ),
        "Cassiopeia": Constellation(
            name="Cassiopeia", name_cn="仙后座", abbreviation="Cas",
            area_sq_deg=598, brightest_star="王良四",
            best_month=11, description="W形或M形，全年可见"
        ),
        "Cygnus": Constellation(
            name="Cygnus", name_cn="天鹅座", abbreviation="Cyg",
            area_sq_deg=804, brightest_star="天津四",
            best_month=9, description="夏季大三角之一，形似天鹅"
        ),
        "Lyra": Constellation(
            name="Lyra", name_cn="天琴座", abbreviation="Lyr",
            area_sq_deg=286, brightest_star="织女一",
            best_month=8, description="夏季大三角之一，织女星所在"
        ),
        "Aquila": Constellation(
            name="Aquila", name_cn="天鹰座", abbreviation="Aql",
            area_sq_deg=652, brightest_star="河鼓二",
            best_month=9, description="夏季大三角之一，牛郎星所在"
        ),
        "Orion": Constellation(
            name="Orion", name_cn="猎户座", abbreviation="Ori",
            area_sq_deg=594, brightest_star="参宿七",
            best_month=1, description="冬季代表星座，易辨认"
        ),
        "Perseus": Constellation(
            name="Perseus", name_cn="英仙座", abbreviation="Per",
            area_sq_deg=615, brightest_star="天船三",
            best_month=12, description="包含著名的英仙座流星雨辐射点"
        ),
    }
    
    @classmethod
    def get_zodiac(cls) -> List[Constellation]:
        """获取黄道十二宫"""
        return list(cls.ZODIAC.values())
    
    @classmethod
    def get_constellation(cls, name: str) -> Optional[Constellation]:
        """根据名称获取星座（支持中英文名）"""
        name_lower = name.lower()
        for constellation in {**cls.ZODIAC, **cls.NORTHERN}.values():
            if (constellation.name.lower() == name_lower or 
                constellation.name_cn == name or
                constellation.abbreviation.lower() == name_lower):
                return constellation
        return None
    
    @classmethod
    def get_constellation_by_month(cls, month: int) -> List[Constellation]:
        """获取某月份最佳观测的星座"""
        results = []
        for c in {**cls.ZODIAC, **cls.NORTHERN}.values():
            if c.best_month == month:
                results.append(c)
        return results


class AstronomyCalculator:
    """天文学计算器"""
    
    # 天文单位（千米）
    AU_KM = 149597870.7
    
    # 光年（千米）
    LIGHT_YEAR_KM = 9.461e12
    
    # 地球赤道半径（千米）
    EARTH_RADIUS_KM = 6378.137
    
    @staticmethod
    def date_to_julian_day(dt: datetime) -> float:
        """将日期转换为儒略日
        
        Args:
            dt: 日期时间
            
        Returns:
            float: 儒略日
        """
        year = dt.year
        month = dt.month
        day = dt.day + dt.hour / 24.0 + dt.minute / 1440.0 + dt.second / 86400.0
        
        if month <= 2:
            year -= 1
            month += 12
        
        a = int(year / 100)
        b = 2 - a + int(a / 4)
        
        jd = int(365.25 * (year + 4716)) + int(30.6001 * (month + 1)) + day + b - 1524.5
        
        return jd
    
    @staticmethod
    def julian_day_to_date(jd: float) -> datetime:
        """将儒略日转换为日期
        
        Args:
            jd: 儒略日
            
        Returns:
            datetime: 日期时间
        """
        jd = jd + 0.5
        z = int(jd)
        f = jd - z
        
        if z < 2299161:
            a = z
        else:
            alpha = int((z - 1867216.25) / 36524.25)
            a = z + 1 + alpha - int(alpha / 4)
        
        b = a + 1524
        c = int((b - 122.1) / 365.25)
        d = int(365.25 * c)
        e = int((b - d) / 30.6001)
        
        day = b - d - int(30.6001 * e) + f
        month = e - 1 if e < 14 else e - 13
        year = c - 4716 if month > 2 else c - 4715
        
        # 提取时分秒
        day_frac = day - int(day)
        hour = int(day_frac * 24)
        minute = int((day_frac * 24 - hour) * 60)
        second = int(((day_frac * 24 - hour) * 60 - minute) * 60)
        
        return datetime(int(year), int(month), int(day), hour, minute, second)
    
    @staticmethod
    def calculate_greenwich_sidereal_time(dt: datetime) -> float:
        """计算格林尼治恒星时
        
        Args:
            dt: 日期时间
            
        Returns:
            float: 格林尼治恒星时（度）
        """
        jd = AstronomyCalculator.date_to_julian_day(dt)
        t = (jd - 2451545.0) / 36525.0
        
        # 格林尼治恒星时（度）
        theta = 280.46061837 + 360.98564736629 * (jd - 2451545.0) + 0.000387933 * t * t - t * t * t / 38710000.0
        
        # 归一化到 0-360
        theta = theta % 360.0
        if theta < 0:
            theta += 360.0
        
        return theta
    
    @staticmethod
    def calculate_local_sidereal_time(dt: datetime, longitude: float) -> float:
        """计算本地恒星时
        
        Args:
            dt: 日期时间
            longitude: 经度（度，东经为正）
            
        Returns:
            float: 本地恒星时（度）
        """
        gst = AstronomyCalculator.calculate_greenwich_sidereal_time(dt)
        lst = gst + longitude
        
        lst = lst % 360.0
        if lst < 0:
            lst += 360.0
        
        return lst
    
    @staticmethod
    def equatorial_to_horizontal(
        ra: float, 
        dec: float, 
        latitude: float, 
        longitude: float, 
        dt: datetime
    ) -> Tuple[float, float]:
        """将赤道坐标转换为地平坐标
        
        Args:
            ra: 赤经（度）
            dec: 赤纬（度）
            latitude: 观测者纬度（度）
            longitude: 观测者经度（度，东经为正）
            dt: 观测时间
            
        Returns:
            Tuple[float, float]: (方位角, 高度角) 单位：度
        """
        # 计算本地恒星时
        lst = AstronomyCalculator.calculate_local_sidereal_time(dt, longitude)
        
        # 计算时角
        ha = lst - ra
        ha = ha % 360.0
        if ha > 180:
            ha -= 360.0
        
        # 转换为弧度
        ha_rad = radians(ha)
        dec_rad = radians(dec)
        lat_rad = radians(latitude)
        
        # 计算高度角
        sin_alt = sin(dec_rad) * sin(lat_rad) + cos(dec_rad) * cos(lat_rad) * cos(ha_rad)
        alt = degrees(asin(sin_alt))
        
        # 计算方位角
        cos_az = (sin(dec_rad) - sin(lat_rad) * sin_alt) / (cos(lat_rad) * cos(radians(alt)))
        az = degrees(acos(max(-1, min(1, cos_az))))
        
        if sin(ha_rad) > 0:
            az = 360 - az
        
        return az, alt
    
    @staticmethod
    def calculate_rise_set_times(
        ra: float,
        dec: float,
        latitude: float,
        longitude: float,
        dt: datetime,
        altitude: float = 0.0
    ) -> RiseSetTimes:
        """计算天体升起、中天、落下时间
        
        Args:
            ra: 赤经（度）
            dec: 赤纬（度）
            latitude: 观测者纬度（度）
            longitude: 观测者经度（度，东经为正）
            dt: 计算日期（只使用日期部分）
            altitude: 目标高度角（度，默认0为地平线）
            
        Returns:
            RiseSetTimes: 升起落下时间
        """
        # 计算是否拱极星或永不升起
        dec_rad = radians(dec)
        lat_rad = radians(latitude)
        
        h0 = radians(altitude)
        
        # 计算时角
        cos_ha = -sin(lat_rad) * sin(dec_rad) + cos(lat_rad) * cos(dec_rad) * cos(h0)
        cos_ha = cos_ha / (cos(lat_rad) * cos(dec_rad))
        
        # 拱极星（永不落下）
        if dec > 90 - latitude:
            return RiseSetTimes(
                rise_time=None, transit_time=None, set_time=None,
                is_circumpolar=True, is_never_rises=False
            )
        
        # 永不升起
        if dec < latitude - 90:
            return RiseSetTimes(
                rise_time=None, transit_time=None, set_time=None,
                is_circumpolar=False, is_never_rises=True
            )
        
        ha = degrees(acos(max(-1, min(1, cos_ha))))
        
        # 计算本地恒星时
        base_date = datetime(dt.year, dt.month, dt.day, 0, 0, 0)
        jd = AstronomyCalculator.date_to_julian_day(base_date)
        
        # 中天时的本地恒星时 = 赤经
        # 升起时的本地恒星时 = 赤经 - 时角
        # 落下时的本地恒星时 = 赤经 + 时角
        
        lst_transit = ra
        lst_rise = ra - ha
        lst_set = ra + ha
        
        # 归一化
        lst_rise = lst_rise % 360.0
        if lst_rise < 0:
            lst_rise += 360.0
        lst_set = lst_set % 360.0
        
        # 转换为世界时
        def lst_to_utc(lst, jd):
            t = (jd - 2451545.0) / 36525.0
            gst0 = 280.46061837 + 360.98564736629 * (jd - 2451545.0)
            gst0 = gst0 % 360.0
            if gst0 < 0:
                gst0 += 360.0
            
            # GST at transit time
            gst = lst - longitude
            gst = gst % 360.0
            if gst < 0:
                gst += 360.0
            
            # UT in days
            ut_days = (gst - gst0) / 360.98564736629
            if ut_days < 0:
                ut_days += 1
            
            return ut_days * 24  # 返回小时
        
        rise_hours = lst_to_utc(lst_rise, jd)
        transit_hours = lst_to_utc(lst_transit, jd)
        set_hours = lst_to_utc(lst_set, jd)
        
        # 创建时间
        rise_time = base_date + timedelta(hours=rise_hours)
        transit_time = base_date + timedelta(hours=transit_hours)
        set_time = base_date + timedelta(hours=set_hours)
        
        return RiseSetTimes(
            rise_time=rise_time,
            transit_time=transit_time,
            set_time=set_time,
            is_circumpolar=False,
            is_never_rises=False
        )
    
    @staticmethod
    def calculate_distance_km(au: float) -> float:
        """将天文单位转换为千米
        
        Args:
            au: 天文单位
            
        Returns:
            float: 千米
        """
        return au * AstronomyCalculator.AU_KM
    
    @staticmethod
    def calculate_distance_ly(km: float) -> float:
        """将千米转换为光年
        
        Args:
            km: 千米
            
        Returns:
            float: 光年
        """
        return km / AstronomyCalculator.LIGHT_YEAR_KM
    
    @staticmethod
    def calculate_angular_diameter(
        actual_diameter_km: float, 
        distance_km: float
    ) -> float:
        """计算角直径
        
        Args:
            actual_diameter_km: 实际直径（千米）
            distance_km: 距离（千米）
            
        Returns:
            float: 角直径（角秒）
        """
        # 角直径 = 实际直径 / 距离（弧度）
        angular_diameter_rad = actual_diameter_km / distance_km
        # 转换为角秒
        return degrees(angular_diameter_rad) * 3600
    
    @staticmethod
    def calculate_planet_position(
        planet: CelestialBody,
        dt: datetime
    ) -> Tuple[float, float]:
        """估算行星在给定日期的赤经赤纬（简化计算）
        
        注意：这是简化计算，精度有限。精确计算需要更复杂的轨道模型。
        
        Args:
            planet: 行星数据
            dt: 日期时间
            
        Returns:
            Tuple[float, float]: (赤经, 赤纬) 单位：度
        """
        # 使用简单的轨道近似
        # 参考日期：J2000.0 (2000-01-01 12:00 UTC)
        j2000 = datetime(2000, 1, 1, 12, 0, 0)
        
        # 天数差
        days = (dt - j2000).total_seconds() / 86400.0
        
        # 平黄经（简化）
        # 实际上每颗行星有不同的轨道参数，这里使用简化近似
        if planet.name == "Mercury":
            l = 252.25 + 4.09233445 * days
            b = 7.0  # 轨道倾角
        elif planet.name == "Venus":
            l = 181.98 + 1.60213036 * days
            b = 3.4
        elif planet.name == "Earth":
            l = 100.46 + 0.9856091 * days
            b = 0.0
        elif planet.name == "Mars":
            l = 355.45 + 0.524033 * days
            b = 1.9
        elif planet.name == "Jupiter":
            l = 34.40 + 0.08308876 * days
            b = 1.3
        elif planet.name == "Saturn":
            l = 50.08 + 0.03351491 * days
            b = 2.5
        elif planet.name == "Uranus":
            l = 314.06 + 0.01172627 * days
            b = 0.8
        elif planet.name == "Neptune":
            l = 304.35 + 0.00598181 * days
            b = 1.8
        else:
            l = 0.0
            b = 0.0
        
        # 归一化黄经
        l = l % 360.0
        
        # 简化：假设行星在黄道上
        # 实际应该考虑轨道倾角和黄赤交角
        # 这里直接返回近似值
        ra = l  # 简化：假设赤经 ≈ 黄经
        dec = b if planet.name != "Earth" else 0  # 简化：假设赤纬 ≈ 黄纬
        
        return ra, dec
    
    @staticmethod
    def calculate_light_travel_time(distance_km: float) -> timedelta:
        """计算光传播时间
        
        Args:
            distance_km: 距离（千米）
            
        Returns:
            timedelta: 光传播时间
        """
        # 光速 (km/s)
        c = 299792.458
        seconds = distance_km / c
        return timedelta(seconds=seconds)


class MoonPhaseCalculator:
    """月相计算器"""
    
    # 月相名称
    PHASES_CN = {
        0: "新月",
        1: "蛾眉月",
        2: "上弦月",
        3: "盈凸月",
        4: "满月",
        5: "亏凸月",
        6: "下弦月",
        7: "残月"
    }
    
    PHASES_EN = {
        0: "New Moon",
        1: "Waxing Crescent",
        2: "First Quarter",
        3: "Waxing Gibbous",
        4: "Full Moon",
        5: "Waning Gibbous",
        6: "Last Quarter",
        7: "Waning Crescent"
    }
    
    @staticmethod
    def calculate_moon_phase(dt: datetime) -> Tuple[float, int, str, str]:
        """计算月相
        
        Args:
            dt: 日期时间
            
        Returns:
            Tuple[float, int, str, str]: (月龄, 月相索引, 中文名, 英文名)
        """
        # 已知的新月日期：2000年1月6日 18:14 UTC
        known_new_moon = datetime(2000, 1, 6, 18, 14, 0)
        
        # 月球公转周期（天）
        synodic_month = 29.530588853
        
        # 计算月龄
        days = (dt - known_new_moon).total_seconds() / 86400.0
        moon_age = days % synodic_month
        
        if moon_age < 0:
            moon_age += synodic_month
        
        # 确定月相
        phase_index = int((moon_age / synodic_month) * 8) % 8
        
        # 特殊处理：上弦月和下弦月
        if 6.5 < moon_age < 7.5:
            phase_index = 2  # 上弦月
        elif 21.5 < moon_age < 22.5:
            phase_index = 6  # 下弦月
        elif moon_age < 1.5:
            phase_index = 0  # 新月
        elif 13.5 < moon_age < 15.5:
            phase_index = 4  # 满月
        
        return (
            moon_age,
            phase_index,
            MoonPhaseCalculator.PHASES_CN[phase_index],
            MoonPhaseCalculator.PHASES_EN[phase_index]
        )
    
    @staticmethod
    def calculate_next_moon_phase(dt: datetime, target_phase: int) -> datetime:
        """计算下一个特定月相的日期
        
        Args:
            dt: 当前日期时间
            target_phase: 目标月相索引 (0-7)
            
        Returns:
            datetime: 下一个该月相的日期
        """
        synodic_month = 29.530588853
        known_new_moon = datetime(2000, 1, 6, 18, 14, 0)
        
        # 当前月龄
        days = (dt - known_new_moon).total_seconds() / 86400.0
        current_age = days % synodic_month
        
        # 目标月龄
        target_age = (target_phase / 8.0) * synodic_month
        
        # 下一个目标月相的天数
        days_to_target = target_age - current_age
        if days_to_target <= 0:
            days_to_target += synodic_month
        
        return dt + timedelta(days=days_to_target)
    
    @staticmethod
    def calculate_moon_distance(dt: datetime) -> float:
        """计算月球距离（简化计算）
        
        Args:
            dt: 日期时间
            
        Returns:
            float: 月球距离（千米）
        """
        # 近地点距离
        perigee = 356500  # km
        # 远地点距离
        apogee = 406700  # km
        # 平均距离
        average = 384400  # km
        
        # 简化：使用周期变化
        # 月球轨道周期约27.3天
        known_perigee = datetime(2000, 1, 10, 0, 0, 0)
        orbital_period = 27.3
        
        days = (dt - known_perigee).total_seconds() / 86400.0
        phase = (days % orbital_period) / orbital_period * 2 * pi
        
        # 使用椭圆近似
        distance = average - (apogee - perigee) / 2 * cos(phase)
        
        return distance


class StarData:
    """恒星数据"""
    
    # 最亮的20颗恒星
    BRIGHT_STARS = {
        "Sirius": {
            "name_cn": "天狼星",
            "ra": 101.29,  # 赤经（度）
            "dec": -16.72,  # 赤纬（度）
            "magnitude": -1.46,
            "constellation": "Canis Major",
            "distance_ly": 8.6,
            "color": "白色"
        },
        "Canopus": {
            "name_cn": "老人星",
            "ra": 95.99,
            "dec": -52.70,
            "magnitude": -0.74,
            "constellation": "Carina",
            "distance_ly": 310,
            "color": "黄白色"
        },
        "Alpha Centauri": {
            "name_cn": "南门二",
            "ra": 219.90,
            "dec": -60.83,
            "magnitude": -0.27,
            "constellation": "Centaurus",
            "distance_ly": 4.37,
            "color": "黄白色"
        },
        "Arcturus": {
            "name_cn": "大角星",
            "ra": 213.92,
            "dec": 19.18,
            "magnitude": -0.05,
            "constellation": "Boötes",
            "distance_ly": 37,
            "color": "橙红色"
        },
        "Vega": {
            "name_cn": "织女一",
            "ra": 279.23,
            "dec": 38.78,
            "magnitude": 0.03,
            "constellation": "Lyra",
            "distance_ly": 25,
            "color": "白色"
        },
        "Capella": {
            "name_cn": "五车二",
            "ra": 79.17,
            "dec": 45.99,
            "magnitude": 0.08,
            "constellation": "Auriga",
            "distance_ly": 43,
            "color": "黄色"
        },
        "Rigel": {
            "name_cn": "参宿七",
            "ra": 78.63,
            "dec": -8.20,
            "magnitude": 0.13,
            "constellation": "Orion",
            "distance_ly": 860,
            "color": "蓝白色"
        },
        "Procyon": {
            "name_cn": "南河三",
            "ra": 114.83,
            "dec": 5.22,
            "magnitude": 0.34,
            "constellation": "Canis Minor",
            "distance_ly": 11,
            "color": "黄白色"
        },
        "Betelgeuse": {
            "name_cn": "参宿四",
            "ra": 88.79,
            "dec": 7.41,
            "magnitude": 0.50,
            "constellation": "Orion",
            "distance_ly": 700,
            "color": "红色"
        },
        "Achernar": {
            "name_cn": "水委一",
            "ra": 24.43,
            "dec": -57.24,
            "magnitude": 0.46,
            "constellation": "Eridanus",
            "distance_ly": 140,
            "color": "蓝白色"
        },
        "Hadar": {
            "name_cn": "马腹一",
            "ra": 210.96,
            "dec": -60.37,
            "magnitude": 0.61,
            "constellation": "Centaurus",
            "distance_ly": 390,
            "color": "蓝白色"
        },
        "Altair": {
            "name_cn": "河鼓二",
            "ra": 297.70,
            "dec": 8.87,
            "magnitude": 0.76,
            "constellation": "Aquila",
            "distance_ly": 17,
            "color": "白色"
        },
        "Aldebaran": {
            "name_cn": "毕宿五",
            "ra": 68.98,
            "dec": 16.51,
            "magnitude": 0.87,
            "constellation": "Taurus",
            "distance_ly": 65,
            "color": "橙红色"
        },
        "Antares": {
            "name_cn": "心宿二",
            "ra": 247.35,
            "dec": -26.43,
            "magnitude": 0.96,
            "constellation": "Scorpius",
            "distance_ly": 550,
            "color": "红色"
        },
        "Spica": {
            "name_cn": "角宿一",
            "ra": 201.30,
            "dec": -11.16,
            "magnitude": 0.97,
            "constellation": "Virgo",
            "distance_ly": 250,
            "color": "蓝白色"
        },
        "Pollux": {
            "name_cn": "北河三",
            "ra": 116.33,
            "dec": 28.03,
            "magnitude": 1.14,
            "constellation": "Gemini",
            "distance_ly": 34,
            "color": "橙色"
        },
        "Fomalhaut": {
            "name_cn": "北落师门",
            "ra": 344.41,
            "dec": -29.62,
            "magnitude": 1.16,
            "constellation": "Piscis Austrinus",
            "distance_ly": 25,
            "color": "白色"
        },
        "Deneb": {
            "name_cn": "天津四",
            "ra": 310.36,
            "dec": 45.28,
            "magnitude": 1.25,
            "constellation": "Cygnus",
            "distance_ly": 2600,
            "color": "白色"
        },
        "Regulus": {
            "name_cn": "轩辕十四",
            "ra": 152.09,
            "dec": 11.97,
            "magnitude": 1.36,
            "constellation": "Leo",
            "distance_ly": 79,
            "color": "蓝白色"
        },
        "Castor": {
            "name_cn": "北河二",
            "ra": 113.65,
            "dec": 31.89,
            "magnitude": 1.58,
            "constellation": "Gemini",
            "distance_ly": 51,
            "color": "白色"
        },
    }
    
    @classmethod
    def get_star(cls, name: str) -> Optional[Dict]:
        """获取恒星信息
        
        Args:
            name: 恒星名称（支持中英文）
            
        Returns:
            Optional[Dict]: 恒星信息
        """
        name_lower = name.lower()
        for star_name, data in cls.BRIGHT_STARS.items():
            if star_name.lower() == name_lower or data["name_cn"] == name:
                return {"name": star_name, **data}
        return None
    
    @classmethod
    def get_visible_stars(cls, latitude: float, dec_limit: float = None) -> List[Dict]:
        """获取在给定纬度可见的恒星
        
        Args:
            latitude: 观测者纬度（度）
            dec_limit: 赤纬限制（可选，默认根据纬度计算）
            
        Returns:
            List[Dict]: 可见恒星列表
        """
        if dec_limit is None:
            # 简化：纬度±90度范围内的恒星理论上可见
            dec_limit = -90
        
        visible = []
        for star_name, data in cls.BRIGHT_STARS.items():
            # 简化判断：赤纬大于（纬度-90）的恒星可见
            if data["dec"] >= latitude - 90:
                visible.append({"name": star_name, **data})
        
        # 按星等排序
        visible.sort(key=lambda x: x["magnitude"])
        return visible


# 便捷函数

def get_planet(name: str) -> Optional[CelestialBody]:
    """获取行星信息
    
    Args:
        name: 行星名称（支持中英文）
        
    Returns:
        Optional[CelestialBody]: 行星数据
    """
    return SolarSystemData.get_planet(name)


def get_all_planets() -> List[CelestialBody]:
    """获取所有行星列表"""
    return SolarSystemData.get_all_planets()


def get_constellation(name: str) -> Optional[Constellation]:
    """获取星座信息
    
    Args:
        name: 星座名称（支持中英文和缩写）
        
    Returns:
        Optional[Constellation]: 星座数据
    """
    return ConstellationData.get_constellation(name)


def get_zodiac_constellations() -> List[Constellation]:
    """获取黄道十二宫"""
    return ConstellationData.get_zodiac()


def calculate_moon_phase(dt: datetime = None) -> Tuple[float, int, str, str]:
    """计算月相
    
    Args:
        dt: 日期时间（默认当前时间）
        
    Returns:
        Tuple[float, int, str, str]: (月龄, 月相索引, 中文名, 英文名)
    """
    if dt is None:
        dt = datetime.now()
    return MoonPhaseCalculator.calculate_moon_phase(dt)


def get_star_info(name: str) -> Optional[Dict]:
    """获取恒星信息
    
    Args:
        name: 恒星名称（支持中英文）
        
    Returns:
        Optional[Dict]: 恒星信息
    """
    return StarData.get_star(name)


def date_to_julian_day(dt: datetime) -> float:
    """日期转儒略日"""
    return AstronomyCalculator.date_to_julian_day(dt)


def julian_day_to_date(jd: float) -> datetime:
    """儒略日转日期"""
    return AstronomyCalculator.julian_day_to_date(jd)


def au_to_km(au: float) -> float:
    """天文单位转千米"""
    return AstronomyCalculator.calculate_distance_km(au)


def km_to_light_year(km: float) -> float:
    """千米转光年"""
    return AstronomyCalculator.calculate_distance_ly(km)


def calculate_light_travel_time(distance_km: float) -> timedelta:
    """计算光传播时间"""
    return AstronomyCalculator.calculate_light_travel_time(distance_km)
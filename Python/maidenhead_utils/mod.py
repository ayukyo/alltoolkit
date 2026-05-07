"""
Maidenhead Grid Locator Utils (梅登黑德网格定位器工具)

业余无线电常用的网格定位系统 (QTH Locator)
将地球表面划分为网格，使用字母和数字编码表示位置
例如: FN31pr 表示一个精确位置

零外部依赖，纯 Python 标准库实现
"""

import math
import re
from typing import Tuple, List, Optional, Dict


class MaidenheadUtils:
    """梅登黑德网格定位器工具类"""
    
    # 基础网格参数
    # 第一层：18个字段 × 18个字段，每个字段 10°经度 × 20°纬度
    FIELD_CHARS = 'ABCDEFGHIJKLMNOPQR'  # 18个字母
    
    # 第二层：每个字段划分为 10 × 10 的方格
    SQUARE_DIGITS = '0123456789'  # 10个数字
    
    # 第三层及以后：每个方格划分为 24 × 24 的子网格
    SUBSQUARE_CHARS = 'abcdefghijklmnopqrstuvwx'  # 24个字母
    
    # 地球参数
    EARTH_RADIUS_KM = 6371.0  # 平均半径（公里）
    EARTH_RADIUS_MI = 3958.8  # 平均半径（英里）
    
    @staticmethod
    def validate(locator: str) -> bool:
        """
        验证梅登黑德定位器格式
        
        Args:
            locator: 定位器字符串
            
        Returns:
            bool: 是否为有效格式
        """
        if not locator:
            return False
        
        locator = locator.strip().upper()
        length = len(locator)
        
        # 长度必须是偶数且在 2-10 之间
        if length % 2 != 0 or length < 2 or length > 10:
            return False
        
        # 检查每对的格式
        pairs = length // 2
        for i in range(pairs):
            char1 = locator[2*i]
            char2 = locator[2*i + 1]
            
            if i == 0:  # 第一对：字段（A-R）
                if char1 not in MaidenheadUtils.FIELD_CHARS or \
                   char2 not in MaidenheadUtils.FIELD_CHARS:
                    return False
            elif i == 1:  # 第二对：方格（0-9）
                if char1 not in MaidenheadUtils.SQUARE_DIGITS or \
                   char2 not in MaidenheadUtils.SQUARE_DIGITS:
                    return False
            else:  # 第三对及以后：子网格（a-x）
                if char1 not in MaidenheadUtils.SUBSQUARE_CHARS.upper() or \
                   char2 not in MaidenheadUtils.SUBSQUARE_CHARS.upper():
                    return False
        
        return True
    
    @staticmethod
    def to_latlon(locator: str) -> Tuple[float, float]:
        """
        将梅登黑德定位器转换为经纬度中心点
        
        Args:
            locator: 定位器字符串
            
        Returns:
            Tuple[float, float]: (纬度, 经度) 中心点坐标
            
        Raises:
            ValueError: 如果定位器格式无效
        """
        if not MaidenheadUtils.validate(locator):
            raise ValueError(f"无效的梅登黑德定位器: {locator}")
        
        locator = locator.strip().upper()
        length = len(locator)
        pairs = length // 2
        
        # 起始坐标（西南角）
        lon = -180.0
        lat = -90.0
        
        # 第一对：字段
        field_lon = MaidenheadUtils.FIELD_CHARS.index(locator[0])
        field_lat = MaidenheadUtils.FIELD_CHARS.index(locator[1])
        lon += field_lon * 20  # 每个字段宽度 20°
        lat += field_lat * 10  # 每个字段高度 10°
        
        lon_width = 20.0
        lat_height = 10.0
        
        if pairs >= 2:
            # 第二对：方格
            square_lon = int(locator[2])
            square_lat = int(locator[3])
            lon += square_lon * 2  # 每个方格宽度 2°
            lat += square_lat * 1  # 每个方格高度 1°
            
            lon_width = 2.0
            lat_height = 1.0
        
        if pairs >= 3:
            # 第三对：子网格
            subsquare_lon = MaidenheadUtils.SUBSQUARE_CHARS.upper().index(locator[4])
            subsquare_lat = MaidenheadUtils.SUBSQUARE_CHARS.upper().index(locator[5])
            lon += subsquare_lon * (2.0 / 24)  # 每个子网格宽度 2/24°
            lat += subsquare_lat * (1.0 / 24)  # 每个子网格高度 1/24°
            
            lon_width = 2.0 / 24
            lat_height = 1.0 / 24
        
        if pairs >= 4:
            # 第四对：扩展子网格
            ext_lon = MaidenheadUtils.SUBSQUARE_CHARS.upper().index(locator[6])
            ext_lat = MaidenheadUtils.SUBSQUARE_CHARS.upper().index(locator[7])
            lon += ext_lon * (2.0 / 24 / 24)
            lat += ext_lat * (1.0 / 24 / 24)
            
            lon_width = 2.0 / 24 / 24
            lat_height = 1.0 / 24 / 24
        
        if pairs >= 5:
            # 第五对：更精细子网格
            fine_lon = MaidenheadUtils.SUBSQUARE_CHARS.upper().index(locator[8])
            fine_lat = MaidenheadUtils.SUBSQUARE_CHARS.upper().index(locator[9])
            lon += fine_lon * (2.0 / 24 / 24 / 24)
            lat += fine_lat * (1.0 / 24 / 24 / 24)
            
            lon_width = 2.0 / 24 / 24 / 24
            lat_height = 1.0 / 24 / 24 / 24
        
        # 返回中心点
        center_lon = lon + lon_width / 2
        center_lat = lat + lat_height / 2
        
        return (round(center_lat, 10), round(center_lon, 10))
    
    @staticmethod
    def from_latlon(lat: float, lon: float, precision: int = 6) -> str:
        """
        将经纬度转换为梅登黑德定位器
        
        Args:
            lat: 纬度（-90 到 90）
            lon: 经度（-180 到 180）
            precision: 精度（字符数），2/4/6/8/10
            
        Returns:
            str: 梅登黑德定位器字符串
            
        Raises:
            ValueError: 如果坐标超出范围或精度无效
        """
        if lat < -90 or lat > 90:
            raise ValueError(f"纬度超出范围: {lat}")
        if lon < -180 or lon > 180:
            raise ValueError(f"经度超出范围: {lon}")
        if precision % 2 != 0 or precision < 2 or precision > 10:
            raise ValueError(f"精度必须是 2/4/6/8/10: {precision}")
        
        # 确保坐标在有效范围内
        lon = lon + 180  # 转换为 0-360
        lat = lat + 90   # 转换为 0-180
        
        locator = ""
        
        # 第一对：字段（A-R）
        field_lon = int(lon / 20)
        field_lat = int(lat / 10)
        locator += MaidenheadUtils.FIELD_CHARS[field_lon]
        locator += MaidenheadUtils.FIELD_CHARS[field_lat]
        
        if precision == 2:
            return locator
        
        lon = lon - field_lon * 20
        lat = lat - field_lat * 10
        
        # 第二对：方格（0-9）
        square_lon = int(lon / 2)
        square_lat = int(lat / 1)
        locator += str(square_lon)
        locator += str(square_lat)
        
        if precision == 4:
            return locator
        
        lon = lon - square_lon * 2
        lat = lat - square_lat * 1
        
        # 第三对：子网格（a-x）
        subsquare_lon = int(lon / (2.0 / 24))
        subsquare_lat = int(lat / (1.0 / 24))
        locator += MaidenheadUtils.SUBSQUARE_CHARS[subsquare_lon]
        locator += MaidenheadUtils.SUBSQUARE_CHARS[subsquare_lat]
        
        if precision == 6:
            return locator
        
        lon = lon - subsquare_lon * (2.0 / 24)
        lat = lat - subsquare_lat * (1.0 / 24)
        
        # 第四对：扩展子网格
        ext_lon = int(lon / (2.0 / 24 / 24))
        ext_lat = int(lat / (1.0 / 24 / 24))
        locator += MaidenheadUtils.SUBSQUARE_CHARS[ext_lon]
        locator += MaidenheadUtils.SUBSQUARE_CHARS[ext_lat]
        
        if precision == 8:
            return locator
        
        lon = lon - ext_lon * (2.0 / 24 / 24)
        lat = lat - ext_lat * (1.0 / 24 / 24)
        
        # 第五对：更精细子网格
        fine_lon = int(lon / (2.0 / 24 / 24 / 24))
        fine_lat = int(lat / (1.0 / 24 / 24 / 24))
        locator += MaidenheadUtils.SUBSQUARE_CHARS[fine_lon]
        locator += MaidenheadUtils.SUBSQUARE_CHARS[fine_lat]
        
        return locator
    
    @staticmethod
    def get_bounds(locator: str) -> Dict[str, float]:
        """
        获取定位器的边界坐标
        
        Args:
            locator: 定位器字符串
            
        Returns:
            Dict: 包含 north, south, east, west 边界坐标
        """
        if not MaidenheadUtils.validate(locator):
            raise ValueError(f"无效的梅登黑德定位器: {locator}")
        
        locator = locator.strip().upper()
        length = len(locator)
        pairs = length // 2
        
        # 起始坐标（西南角）
        west = -180.0
        south = -90.0
        
        # 计算网格大小
        lon_width = 20.0
        lat_height = 10.0
        
        # 第一对：字段
        west += MaidenheadUtils.FIELD_CHARS.index(locator[0]) * 20
        south += MaidenheadUtils.FIELD_CHARS.index(locator[1]) * 10
        
        if pairs >= 2:
            west += int(locator[2]) * 2
            south += int(locator[3]) * 1
            lon_width = 2.0
            lat_height = 1.0
        
        if pairs >= 3:
            west += MaidenheadUtils.SUBSQUARE_CHARS.upper().index(locator[4]) * (2.0 / 24)
            south += MaidenheadUtils.SUBSQUARE_CHARS.upper().index(locator[5]) * (1.0 / 24)
            lon_width = 2.0 / 24
            lat_height = 1.0 / 24
        
        if pairs >= 4:
            west += MaidenheadUtils.SUBSQUARE_CHARS.upper().index(locator[6]) * (2.0 / 24 / 24)
            south += MaidenheadUtils.SUBSQUARE_CHARS.upper().index(locator[7]) * (1.0 / 24 / 24)
            lon_width = 2.0 / 24 / 24
            lat_height = 1.0 / 24 / 24
        
        if pairs >= 5:
            west += MaidenheadUtils.SUBSQUARE_CHARS.upper().index(locator[8]) * (2.0 / 24 / 24 / 24)
            south += MaidenheadUtils.SUBSQUARE_CHARS.upper().index(locator[9]) * (1.0 / 24 / 24 / 24)
            lon_width = 2.0 / 24 / 24 / 24
            lat_height = 1.0 / 24 / 24 / 24
        
        return {
            'north': round(south + lat_height, 10),
            'south': round(south, 10),
            'east': round(west + lon_width, 10),
            'west': round(west, 10),
            'lat_height': round(lat_height, 10),
            'lon_width': round(lon_width, 10)
        }
    
    @staticmethod
    def get_grid_size(locator: str) -> Dict[str, float]:
        """
        获取定位器网格的大小
        
        Args:
            locator: 定位器字符串
            
        Returns:
            Dict: 包含经度宽度、纬度高度、面积（平方公里）
        """
        bounds = MaidenheadUtils.get_bounds(locator)
        
        # 使用中心点计算面积（考虑地球曲率）
        center_lat, center_lon = MaidenheadUtils.to_latlon(locator)
        
        # 在给定纬度下的经度距离
        lat_rad = math.radians(center_lat)
        lon_km = bounds['lon_width'] * (MaidenheadUtils.EARTH_RADIUS_KM * math.cos(lat_rad) * math.pi / 180)
        lat_km = bounds['lat_height'] * (MaidenheadUtils.EARTH_RADIUS_KM * math.pi / 180)
        
        area_km2 = lon_km * lat_km
        
        return {
            'lon_width_deg': bounds['lon_width'],
            'lat_height_deg': bounds['lat_height'],
            'lon_width_km': round(lon_km, 4),
            'lat_height_km': round(lat_km, 4),
            'area_km2': round(area_km2, 4),
            'area_mi2': round(area_km2 * 0.386102, 4)
        }
    
    @staticmethod
    def distance(locator1: str, locator2: str, unit: str = 'km') -> float:
        """
        计算两个定位器之间的距离
        
        Args:
            locator1: 第一个定位器
            locator2: 第二个定位器
            unit: 单位（'km' 公里 或 'mi' 英里）
            
        Returns:
            float: 距离
        """
        lat1, lon1 = MaidenheadUtils.to_latlon(locator1)
        lat2, lon2 = MaidenheadUtils.to_latlon(locator2)
        
        return MaidenheadUtils.haversine_distance(lat1, lon1, lat2, lon2, unit)
    
    @staticmethod
    def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float, 
                           unit: str = 'km') -> float:
        """
        使用 Haversine 公式计算两点之间的距离
        
        Args:
            lat1, lon1: 第一个点的经纬度
            lat2, lon2: 第二个点的经纬度
            unit: 单位
            
        Returns:
            float: 距离
        """
        # 转换为弧度
        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        lon1_rad = math.radians(lon1)
        lon2_rad = math.radians(lon2)
        
        # Haversine 公式
        dlat = lat2_rad - lat1_rad
        dlon = lon2_rad - lon1_rad
        
        a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        
        radius = MaidenheadUtils.EARTH_RADIUS_KM if unit == 'km' else MaidenheadUtils.EARTH_RADIUS_MI
        
        return round(radius * c, 4)
    
    @staticmethod
    def bearing(locator1: str, locator2: str) -> float:
        """
        计算从 locator1 到 locator2 的方位角
        
        Args:
            locator1: 起点定位器
            locator2: 终点定位器
            
        Returns:
            float: 方位角（度，0-360）
        """
        lat1, lon1 = MaidenheadUtils.to_latlon(locator1)
        lat2, lon2 = MaidenheadUtils.to_latlon(locator2)
        
        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        dlon_rad = math.radians(lon2 - lon1)
        
        x = math.sin(dlon_rad) * math.cos(lat2_rad)
        y = math.cos(lat1_rad) * math.sin(lat2_rad) - math.sin(lat1_rad) * math.cos(lat2_rad) * math.cos(dlon_rad)
        
        bearing = math.degrees(math.atan2(x, y))
        
        # 转换为 0-360
        return round((bearing + 360) % 360, 2)
    
    @staticmethod
    def neighbors(locator: str, level: int = 1) -> List[str]:
        """
        获取定位器的相邻网格
        
        Args:
            locator: 定位器字符串
            level: 邻域层级（1=直接相邻，2=包含周围一圈）
            
        Returns:
            List[str]: 相邻定位器列表
        """
        lat, lon = MaidenheadUtils.to_latlon(locator)
        precision = len(locator.strip())
        
        neighbors_list = []
        
        bounds = MaidenheadUtils.get_bounds(locator)
        lat_step = bounds['lat_height']
        lon_step = bounds['lon_width']
        
        for dy in range(-level, level + 1):
            for dx in range(-level, level + 1):
                if dx == 0 and dy == 0:
                    continue
                
                new_lat = lat + dy * lat_step
                new_lon = lon + dx * lon_step
                
                # 检查边界
                if new_lat >= -90 and new_lat <= 90 and \
                   new_lon >= -180 and new_lon <= 180:
                    try:
                        neighbor = MaidenheadUtils.from_latlon(new_lat, new_lon, precision)
                        neighbors_list.append(neighbor)
                    except ValueError:
                        pass
        
        return neighbors_list
    
    @staticmethod
    def encode_path(locators: List[str]) -> str:
        """
        将定位器列表编码为压缩字符串
        
        Args:
            locators: 定位器列表
            
        Returns:
            str: 压缩后的字符串
        """
        if not locators:
            return ""
        
        # 使用逗号分隔
        return ','.join(locators)
    
    @staticmethod
    def decode_path(encoded: str) -> List[str]:
        """
        将压缩字符串解码为定位器列表
        
        Args:
            encoded: 压缩字符串
            
        Returns:
            List[str]: 定位器列表
        """
        if not encoded:
            return []
        
        return [loc.strip() for loc in encoded.split(',')]
    
    @staticmethod
    def path_distance(locators: List[str], unit: str = 'km') -> float:
        """
        计算路径的总距离
        
        Args:
            locators: 定位器列表（路径）
            unit: 单位
            
        Returns:
            float: 总距离
        """
        if len(locators) < 2:
            return 0.0
        
        total = 0.0
        for i in range(len(locators) - 1):
            total += MaidenheadUtils.distance(locators[i], locators[i+1], unit)
        
        return round(total, 4)
    
    @staticmethod
    def path_length(locators: List[str]) -> int:
        """
        获取路径中的定位器数量
        
        Args:
            locators: 定位器列表
            
        Returns:
            int: 定位器数量
        """
        return len(locators)
    
    @staticmethod
    def intermediate_point(locator1: str, locator2: str, fraction: float) -> str:
        """
        计算两点之间的中间点
        
        Args:
            locator1: 起点
            locator2: 终点
            fraction: 分数（0.0 到 1.0）
            
        Returns:
            str: 中间点的定位器
        """
        lat1, lon1 = MaidenheadUtils.to_latlon(locator1)
        lat2, lon2 = MaidenheadUtils.to_latlon(locator2)
        
        # 简单线性插值
        new_lat = lat1 + (lat2 - lat1) * fraction
        new_lon = lon1 + (lon2 - lon1) * fraction
        
        precision = min(len(locator1.strip()), len(locator2.strip()))
        
        return MaidenheadUtils.from_latlon(new_lat, new_lon, precision)
    
    @staticmethod
    def format_location(locator: str, style: str = 'standard') -> str:
        """
        格式化定位器显示
        
        Args:
            locator: 定位器字符串
            style: 显示风格（'standard', 'compact', 'detailed'）
            
        Returns:
            str: 格式化后的字符串
        """
        if not MaidenheadUtils.validate(locator):
            return "无效定位器"
        
        locator = locator.strip().upper()
        
        if style == 'compact':
            return locator
        
        lat, lon = MaidenheadUtils.to_latlon(locator)
        
        if style == 'detailed':
            bounds = MaidenheadUtils.get_bounds(locator)
            size = MaidenheadUtils.get_grid_size(locator)
            return f"{locator} ({lat:.6f}, {lon:.6f}) - {size['area_km2']} km²"
        
        return f"{locator} ({lat:.4f}°, {lon:.4f}°)"
    
    @staticmethod
    def precision_description(precision: int) -> str:
        """
        获取精度的描述
        
        Args:
            precision: 字符数
            
        Returns:
            str: 精度描述
        """
        descriptions = {
            2: "字段级 (约 400×800 km)",
            4: "方格级 (约 20×40 km)",
            6: "子网格级 (约 1×2 km)",
            8: "扩展级 (约 50×100 m)",
            10: "精细级 (约 2×5 m)"
        }
        return descriptions.get(precision, f"未知精度 ({precision}字符)")
    
    @staticmethod
    def normalize(locator: str) -> str:
        """
        标准化定位器格式
        
        Args:
            locator: 输入定位器
            
        Returns:
            str: 标准化后的定位器（大写）
        """
        if not locator:
            return ""
        return locator.strip().upper()


# 创建全局实例
maidenhead = MaidenheadUtils()


# 便捷函数
def validate_locator(locator: str) -> bool:
    """验证定位器格式"""
    return maidenhead.validate(locator)


def latlon_to_locator(lat: float, lon: float, precision: int = 6) -> str:
    """经纬度转定位器"""
    return maidenhead.from_latlon(lat, lon, precision)


def locator_to_latlon(locator: str) -> Tuple[float, float]:
    """定位器转经纬度"""
    return maidenhead.to_latlon(locator)


def locator_distance(locator1: str, locator2: str, unit: str = 'km') -> float:
    """计算两个定位器的距离"""
    return maidenhead.distance(locator1, locator2, unit)


def locator_bearing(locator1: str, locator2: str) -> float:
    """计算方位角"""
    return maidenhead.bearing(locator1, locator2)
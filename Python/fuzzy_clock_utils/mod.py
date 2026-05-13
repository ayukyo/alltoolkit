"""
模糊时钟工具模块 (Fuzzy Clock Utils)
将精确时间转换为人类可读的模糊时间表达

支持功能：
- 转换为模糊时间描述（如 "三点过一刻"、"快四点了"）
- 支持多语言（中文、英文）
- 支持自定义精度级别
- 支持口语化时间表达
"""

from datetime import datetime, time, timedelta
from typing import Optional, Tuple, Union

# 类型别名，兼容各版本 Python
LanguageType = str  # "zh" 或 "en"
PrecisionType = str  # "exact", "fuzzy", "approximate"


class FuzzyClock:
    """模糊时钟转换器"""
    
    # 精确到分钟的时钟位置描述（中文）
    MINUTE_EXPRESSIONS_CN = {
        0: "整",
        5: "过五分",
        10: "过十分",
        15: "一刻",
        20: "过二十分",
        25: "过二十五分",
        30: "半",
        35: "差二十五分",
        40: "差二十分",
        45: "差一刻",
        50: "差十分",
        55: "差五分",
    }
    
    # 模糊的时钟位置描述（中文）
    FUZZY_EXPRESSIONS_CN = {
        0: "整",
        15: "过一刻",
        30: "半",
        45: "差一刻",
    }
    
    # 英文分钟表达
    MINUTE_EXPRESSIONS_EN = {
        0: "o'clock",
        5: "five past",
        10: "ten past",
        15: "quarter past",
        20: "twenty past",
        25: "twenty-five past",
        30: "half past",
        35: "twenty-five to",
        40: "twenty to",
        45: "quarter to",
        50: "ten to",
        55: "five to",
    }
    
    # 中文小时数字
    HOUR_CN = {
        0: "十二", 1: "一", 2: "二", 3: "三", 4: "四",
        5: "五", 6: "六", 7: "七", 8: "八", 9: "九",
        10: "十", 11: "十一", 12: "十二", 13: "十三",
        14: "十四", 15: "十五", 16: "十六", 17: "十七",
        18: "十八", 19: "十九", 20: "二十", 21: "二十一",
        22: "二十二", 23: "二十三", 24: "二十四"
    }
    
    # 英文小时
    HOUR_EN = {
        0: "twelve", 1: "one", 2: "two", 3: "three", 4: "four",
        5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine",
        10: "ten", 11: "eleven", 12: "twelve"
    }
    
    def __init__(self, language: LanguageType = "zh", precision: PrecisionType = "fuzzy"):
        """
        初始化模糊时钟
        
        Args:
            language: 语言，支持 "zh" (中文) 或 "en" (英文)
            precision: 精度级别
                - "exact": 精确到最近5分钟
                - "fuzzy": 使用一刻/半小时表达
                - "approximate": 非常模糊的表达
        """
        self.language = language
        self.precision = precision
    
    def _round_to_nearest(self, value: int, base: int) -> int:
        """四舍五入到最近的基数的倍数"""
        return round(value / base) * base
    
    def _get_hour_display(self, hour: int, next_hour: bool = False, twelve_hour: bool = True) -> str:
        """获取小时显示"""
        if next_hour:
            hour = (hour + 1) % 24
        
        if twelve_hour:
            hour = hour % 12
            if hour == 0:
                hour = 12
        
        if self.language == "zh":
            return self.HOUR_CN.get(hour, str(hour))
        else:
            return self.HOUR_EN.get(hour, str(hour))
    
    def _get_minute_expression(self, minute: int) -> Tuple[str, bool]:
        """
        获取分钟表达
        
        Returns:
            (表达文本, 是否需要下一小时)
        """
        if self.precision == "exact":
            # 精确到5分钟
            rounded = self._round_to_nearest(minute, 5)
            if rounded >= 60:
                rounded = 0
            expressions = self.MINUTE_EXPRESSIONS_CN if self.language == "zh" else self.MINUTE_EXPRESSIONS_EN
        elif self.precision == "fuzzy":
            # 使用一刻/半小时表达
            if minute < 8:
                rounded = 0
            elif minute < 23:
                rounded = 15
            elif minute < 38:
                rounded = 30
            elif minute < 53:
                rounded = 45
            else:
                rounded = 0
            expressions = self.MINUTE_EXPRESSIONS_CN if self.language == "zh" else self.MINUTE_EXPRESSIONS_EN
        else:  # approximate
            # 非常模糊
            if minute < 15:
                return ("刚过" if self.language == "zh" else "just after", False)
            elif minute < 45:
                return ("半" if self.language == "zh" else "half past", False)
            else:
                return ("快" if self.language == "zh" else "almost", True)
        
        need_next_hour = rounded > 30
        return expressions.get(rounded, ""), need_next_hour
    
    def fuzzy_time(self, dt: Optional[datetime] = None, hour: Optional[int] = None, minute: Optional[int] = None) -> str:
        """
        将时间转换为模糊表达
        
        Args:
            dt: datetime 对象，如果提供则忽略 hour 和 minute
            hour: 小时 (0-23)
            minute: 分钟 (0-59)
        
        Returns:
            模糊时间字符串
        """
        if dt is not None:
            hour = dt.hour
            minute = dt.minute
        elif hour is None or minute is None:
            now = datetime.now()
            hour = now.hour
            minute = now.minute
        
        minute_expr, next_hour = self._get_minute_expression(minute)
        
        if self.language == "zh":
            hour_display = self._get_hour_display(hour, next_hour)
            
            if minute_expr == "整":
                return f"{hour_display}点整"
            elif minute_expr == "半":
                return f"{hour_display}点半"
            elif minute_expr == "一刻":
                return f"{hour_display}点一刻"
            elif minute_expr == "差一刻":
                real_hour = self._get_hour_display(hour, True)
                return f"差一刻{real_hour}点"
            elif minute_expr.startswith("差"):
                real_hour = self._get_hour_display(hour, True)
                return f"{minute_expr}{real_hour}点"
            elif minute_expr.startswith("过"):
                return f"{hour_display}点{minute_expr}"
            else:
                return f"{hour_display}点{minute_expr}"
        else:
            hour_display = self._get_hour_display(hour, next_hour)
            
            if minute_expr == "o'clock":
                return f"{hour_display} o'clock"
            elif "to" in minute_expr:
                return f"{minute_expr} {hour_display}"
            else:
                return f"{minute_expr} {hour_display}"
    
    def to_colloquial(self, dt: Optional[datetime] = None, hour: Optional[int] = None, minute: Optional[int] = None) -> str:
        """
        转换为口语化时间表达
        
        Args:
            dt: datetime 对象
            hour: 小时
            minute: 分钟
        
        Returns:
            口语化时间字符串
        """
        if dt is not None:
            hour = dt.hour
            minute = dt.minute
        elif hour is None or minute is None:
            now = datetime.now()
            hour = now.hour
            minute = now.minute
        
        if self.language == "zh":
            # 中文口语化表达
            if minute == 0:
                if hour == 0:
                    return "半夜十二点"
                elif hour < 6:
                    return f"凌晨{self.HOUR_CN[hour]}点"
                elif hour < 9:
                    return f"早上{self.HOUR_CN[hour]}点"
                elif hour < 12:
                    return f"上午{self.HOUR_CN[hour]}点"
                elif hour == 12:
                    return "中午十二点"
                elif hour < 14:
                    return f"中午{self.HOUR_CN[hour]}点"
                elif hour < 18:
                    return f"下午{self.HOUR_CN[hour]}点"
                elif hour < 22:
                    return f"晚上{self.HOUR_CN[hour]}点"
                else:
                    return f"夜里{self.HOUR_CN[hour]}点"
            else:
                # 有分钟的情况
                fuzzy = self.fuzzy_time(hour=hour, minute=minute)
                # 根据时间段添加前缀
                if hour < 6 or (hour == 5 and minute > 30):
                    prefix = "凌晨"
                elif hour < 9:
                    prefix = "早上"
                elif hour < 12:
                    prefix = "上午"
                elif hour < 14:
                    prefix = "中午"
                elif hour < 18:
                    prefix = "下午"
                elif hour < 22:
                    prefix = "晚上"
                else:
                    prefix = "夜里"
                return f"{prefix}{fuzzy}"
        else:
            # 英文口语化表达
            fuzzy = self.fuzzy_time(hour=hour, minute=minute)
            period = ""
            
            if hour < 12:
                period = " in the morning"
            elif hour < 17:
                period = " in the afternoon"
            elif hour < 21:
                period = " in the evening"
            else:
                period = " at night"
            
            return f"{fuzzy}{period}"
    
    def time_range(self, dt: Optional[datetime] = None, hour: Optional[int] = None, minute: Optional[int] = None) -> str:
        """
        返回时间范围描述
        
        Args:
            dt: datetime 对象
            hour: 小时
            minute: 分钟
        
        Returns:
            时间范围描述
        """
        if dt is not None:
            hour = dt.hour
            minute = dt.minute
        elif hour is None or minute is None:
            now = datetime.now()
            hour = now.hour
            minute = now.minute
        
        if self.language == "zh":
            if hour < 5:
                return "深夜"
            elif hour < 8:
                return "清晨"
            elif hour < 11:
                return "上午"
            elif hour < 13:
                return "中午"
            elif hour < 14:
                return "午后"
            elif hour < 17:
                return "下午"
            elif hour < 19:
                return "傍晚"
            elif hour < 22:
                return "晚上"
            else:
                return "深夜"
        else:
            if hour < 5:
                return "late night"
            elif hour < 8:
                return "early morning"
            elif hour < 12:
                return "morning"
            elif hour < 14:
                return "noon"
            elif hour < 17:
                return "afternoon"
            elif hour < 19:
                return "evening"
            elif hour < 22:
                return "night"
            else:
                return "late night"
    
    def relative_time(self, dt: Optional[datetime] = None) -> str:
        """
        转换为相对时间描述
        
        Args:
            dt: 目标时间
        
        Returns:
            相对时间描述
        """
        if dt is None:
            dt = datetime.now()
        
        now = datetime.now()
        diff = dt - now
        total_seconds = int(diff.total_seconds())
        
        if total_seconds < 0:
            past = True
            total_seconds = abs(total_seconds)
        else:
            past = False
        
        if self.language == "zh":
            if total_seconds < 60:
                return "刚刚" if past else "马上"
            elif total_seconds < 3600:
                minutes = total_seconds // 60
                return f"{minutes}分钟前" if past else f"{minutes}分钟后"
            elif total_seconds < 86400:
                hours = total_seconds // 3600
                return f"{hours}小时前" if past else f"{hours}小时后"
            elif total_seconds < 604800:
                days = total_seconds // 86400
                return f"{days}天前" if past else f"{days}天后"
            else:
                weeks = total_seconds // 604800
                return f"{weeks}周前" if past else f"{weeks}周后"
        else:
            if total_seconds < 60:
                return "just now" if past else "in a moment"
            elif total_seconds < 3600:
                minutes = total_seconds // 60
                return f"{minutes} minutes ago" if past else f"in {minutes} minutes"
            elif total_seconds < 86400:
                hours = total_seconds // 3600
                return f"{hours} hours ago" if past else f"in {hours} hours"
            elif total_seconds < 604800:
                days = total_seconds // 86400
                return f"{days} days ago" if past else f"in {days} days"
            else:
                weeks = total_seconds // 604800
                return f"{weeks} weeks ago" if past else f"in {weeks} weeks"
    
    def to_approximate_time(self, dt: Optional[datetime] = None, hour: Optional[int] = None, minute: Optional[int] = None) -> str:
        """
        转换为近似时间表达
        
        Args:
            dt: datetime 对象
            hour: 小时
            minute: 分钟
        
        Returns:
            近似时间表达
        """
        if dt is not None:
            hour = dt.hour
            minute = dt.minute
        elif hour is None or minute is None:
            now = datetime.now()
            hour = now.hour
            minute = now.minute
        
        if self.language == "zh":
            if minute < 7:
                return f"{self.HOUR_CN[hour % 12] if hour % 12 != 0 else '十二'}点刚过"
            elif minute < 23:
                return f"{self.HOUR_CN[hour % 12] if hour % 12 != 0 else '十二'}点左右"
            elif minute < 37:
                return f"{self.HOUR_CN[hour % 12] if hour % 12 != 0 else '十二'}点半左右"
            elif minute < 53:
                next_h = (hour + 1) % 12
                if next_h == 0:
                    next_h = 12
                return f"快{self.HOUR_CN[next_h]}点了"
            else:
                next_h = (hour + 1) % 12
                if next_h == 0:
                    next_h = 12
                return f"快{self.HOUR_CN[next_h]}点了"
        else:
            hour_12 = hour % 12 if hour % 12 != 0 else 12
            hour_en = self.HOUR_EN.get(hour_12, str(hour_12))
            next_h = (hour + 1) % 12
            if next_h == 0:
                next_h = 12
            next_hour_en = self.HOUR_EN.get(next_h, str(next_h))
            
            if minute < 7:
                return f"just after {hour_en}"
            elif minute < 23:
                return f"around {hour_en}"
            elif minute < 37:
                return f"around half past {hour_en}"
            elif minute < 53:
                return f"almost {next_hour_en}"
            else:
                return f"almost {next_hour_en}"


def fuzzy_time(dt: Optional[datetime] = None, hour: Optional[int] = None, minute: Optional[int] = None, 
               language: LanguageType = "zh", precision: PrecisionType = "fuzzy") -> str:
    """
    便捷函数：将时间转换为模糊表达
    
    Args:
        dt: datetime 对象
        hour: 小时
        minute: 分钟
        language: 语言 ("zh" 或 "en")
        precision: 精度级别
    
    Returns:
        模糊时间字符串
    """
    clock = FuzzyClock(language=language, precision=precision)
    return clock.fuzzy_time(dt=dt, hour=hour, minute=minute)


def colloquial_time(dt: Optional[datetime] = None, hour: Optional[int] = None, minute: Optional[int] = None,
                    language: LanguageType = "zh") -> str:
    """
    便捷函数：转换为口语化时间
    
    Args:
        dt: datetime 对象
        hour: 小时
        minute: 分钟
        language: 语言
    
    Returns:
        口语化时间字符串
    """
    clock = FuzzyClock(language=language)
    return clock.to_colloquial(dt=dt, hour=hour, minute=minute)


def time_range(dt: Optional[datetime] = None, hour: Optional[int] = None, minute: Optional[int] = None,
               language: LanguageType = "zh") -> str:
    """
    便捷函数：获取时间范围描述
    
    Args:
        dt: datetime 对象
        hour: 小时
        minute: 分钟
        language: 语言
    
    Returns:
        时间范围描述
    """
    clock = FuzzyClock(language=language)
    return clock.time_range(dt=dt, hour=hour, minute=minute)


def approximate_time(dt: Optional[datetime] = None, hour: Optional[int] = None, minute: Optional[int] = None,
                     language: LanguageType = "zh") -> str:
    """
    便捷函数：转换为近似时间
    
    Args:
        dt: datetime 对象
        hour: 小时
        minute: 分钟
        language: 语言
    
    Returns:
        近似时间表达
    """
    clock = FuzzyClock(language=language)
    return clock.to_approximate_time(dt=dt, hour=hour, minute=minute)


def relative_time(dt: Optional[datetime] = None, language: LanguageType = "zh") -> str:
    """
    便捷函数：转换为相对时间
    
    Args:
        dt: 目标时间
        language: 语言
    
    Returns:
        相对时间描述
    """
    clock = FuzzyClock(language=language)
    return clock.relative_time(dt=dt)


# 导出
__all__ = [
    'FuzzyClock',
    'fuzzy_time',
    'colloquial_time', 
    'time_range',
    'approximate_time',
    'relative_time',
]
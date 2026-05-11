"""
自然语言日期解析工具库
Natural Language Date Parser Utilities

解析中文自然语言日期表达式，转换为精确的 datetime 对象。
支持相对日期、周期日期、时间组合等多种表达式。

零外部依赖，仅使用 Python 标准库。
"""

from datetime import datetime, timedelta, time
from typing import Optional, Tuple, List, Dict, Any
from dataclasses import dataclass
from enum import Enum
import re


class DateType(Enum):
    """日期类型枚举"""
    ABSOLUTE = "absolute"       # 绝对日期（2024年1月1日）
    RELATIVE = "relative"       # 相对日期（今天、明天、昨天）
    WEEKDAY = "weekday"         # 星期日期（周一、下周三）
    MONTHLY = "monthly"         # 月度日期（每月15号、下月最后一天）
    YEARLY = "yearly"           # 年度日期（明年元旦）
    RANGE = "range"            # 日期范围（这周、下个月）
    UNKNOWN = "unknown"         # 未知/无法解析


@dataclass
class ParseResult:
    """解析结果"""
    success: bool
    datetime_obj: Optional[datetime]
    original_text: str
    normalized_text: str
    date_type: DateType
    confidence: float          # 解析置信度 0.0-1.0
    has_time: bool             # 是否包含时间
    error_message: Optional[str] = None


class NaturalDateParser:
    """自然语言日期解析器"""
    
    # 星期映射（包含中文和数字版本）
    WEEKDAY_MAP = {
        '周一': 0, '星期一': 0, '礼拜一': 0, '一': 0, '1': 0, '周1': 0,
        '周二': 1, '星期二': 1, '礼拜二': 1, '二': 1, '2': 1, '周2': 1,
        '周三': 2, '星期三': 2, '礼拜三': 2, '三': 2, '3': 2, '周3': 2,
        '周四': 3, '星期四': 3, '礼拜四': 3, '四': 3, '4': 3, '周4': 3,
        '周五': 4, '星期五': 4, '礼拜五': 4, '五': 4, '5': 4, '周5': 4,
        '周六': 5, '星期六': 5, '礼拜六': 5, '六': 5, '6': 5, '周6': 5,
        '周天': 6, '周日': 6, '星期日': 6, '礼拜日': 6, '天': 6, '日': 6, '7': 6, '0': 6, '周7': 6, '周0': 6,
    }
    
    # 月份映射
    MONTH_MAP = {
        '一月': 1, '1月': 1, '正月': 1,
        '二月': 2, '2月': 2,
        '三月': 3, '3月': 3,
        '四月': 4, '4月': 4,
        '五月': 5, '5月': 5,
        '六月': 6, '6月': 6,
        '七月': 7, '7月': 7,
        '八月': 8, '8月': 8,
        '九月': 9, '9月': 9,
        '十月': 10, '10月': 10,
        '十一月': 11, '11月': 11,
        '十二月': 12, '12月': 12, '腊月': 12,
    }
    
    # 时间段映射
    TIME_PERIOD_MAP = {
        '凌晨': (0, 6),
        '早上': (6, 9),
        '早晨': (6, 9),
        '上午': (9, 12),
        '中午': (11, 14),
        '下午': (14, 18),
        '傍晚': (17, 19),
        '晚上': (18, 22),
        '夜晚': (19, 23),
        '深夜': (22, 24),
        '半夜': (23, 2),
    }
    
    # 节日映射（公历）
    HOLIDAYS = {
        '元旦': (1, 1),
        '情人节': (2, 14),
        '妇女节': (3, 8),
        '植树节': (3, 12),
        '愚人节': (4, 1),
        '劳动节': (5, 1),
        '青年节': (5, 4),
        '儿童节': (6, 1),
        '建党节': (7, 1),
        '建军节': (8, 1),
        '教师节': (9, 10),
        '国庆节': (10, 1),
        '万圣节': (10, 31),
        '光棍节': (11, 11),
        '双十二': (12, 12),
        '平安夜': (12, 24),
        '圣诞节': (12, 25),
    }
    
    def __init__(self, now: Optional[datetime] = None, strict: bool = False):
        """
        初始化解析器
        
        Args:
            now: 参考时间，默认为当前时间
            strict: 严格模式，无效日期返回错误而非猜测
        """
        self.now = now or datetime.now()
        self.strict = strict
    
    def parse(self, text: str) -> ParseResult:
        """
        解析自然语言日期表达式
        
        Args:
            text: 自然语言日期文本
            
        Returns:
            ParseResult 解析结果
        """
        # 标准化文本
        normalized = self._normalize_text(text)
        original = text
        
        # 尝试各种解析策略
        parsers = [
            self._parse_relative,
            self._parse_weekday,
            self._parse_holiday,      # 节日在年度之前处理
            self._parse_yearly,
            self._parse_monthly,
            self._parse_absolute,
            self._parse_range,
            self._parse_number_days,
        ]
        
        for parser in parsers:
            result = parser(normalized, original)
            if result.success:
                return result
        
        return ParseResult(
            success=False,
            datetime_obj=None,
            original_text=original,
            normalized_text=normalized,
            date_type=DateType.UNKNOWN,
            confidence=0.0,
            has_time=False,
            error_message=f"无法解析日期表达式: {original}"
        )
    
    def _normalize_text(self, text: str) -> str:
        """标准化文本"""
        normalized = text.strip()
        # 移除多余空格
        normalized = re.sub(r'\s+', '', normalized)
        # 数字转换
        normalized = self._convert_chinese_numbers(normalized)
        return normalized
    
    def _convert_chinese_numbers(self, text: str) -> str:
        """将中文数字转换为阿拉伯数字"""
        chinese_nums = {
            '零': '0', '〇': '0', '一': '1', '二': '2', '三': '3',
            '四': '4', '五': '5', '六': '6', '七': '7', '八': '8',
            '九': '9', '十': '10', '廿': '20', '卅': '30',
        }
        
        result = text
        for cn, ar in chinese_nums.items():
            result = result.replace(cn, ar)
        
        # 处理"十X"格式，如 "十五" -> "15"
        result = re.sub(r'10(\d)', lambda m: str(10 + int(m.group(1))), result)
        
        return result
    
    def _parse_time(self, text: str) -> Tuple[Optional[int], Optional[int], int, str]:
        """
        解析时间部分
        
        Returns:
            (hour, minute, confidence, remaining_text)
        """
        hour, minute = None, None
        remaining = text
        time_period_name = None
        
        # 先检测具体时间 XX点XX分（优先级高于时间段）
        time_match = re.search(r'(\d{1,2})[点时:：](\d{1,2})?[分]?', remaining)
        if time_match:
            hour = int(time_match.group(1))
            minute = int(time_match.group(2)) if time_match.group(2) else 0
            # 使用分隔符避免数字合并
            remaining = remaining[:time_match.start()] + '|' + remaining[time_match.end():]
        else:
            # 只有小時
            hour_match = re.search(r'(\d{1,2})[点时]', remaining)
            if hour_match:
                hour = int(hour_match.group(1))
                minute = 0
                remaining = remaining[:hour_match.start()] + '|' + remaining[hour_match.end():]
        
        # 解析时间段（上午、下午等）
        time_period = None
        for period, (start_h, end_h) in self.TIME_PERIOD_MAP.items():
            if period in remaining:
                time_period = (start_h, end_h)
                time_period_name = period
                remaining = remaining.replace(period, '')
                break
        
        # 如果只有时间段没有具体时间，使用默认值
        if hour is None and time_period:
            hour = time_period[0]
            minute = 0
        
        # 处理时间段对hour的影响（下午/晚上需要加12小时）
        if hour is not None and time_period_name:
            if time_period_name in ('下午', '傍晚', '晚上', '夜晚', '深夜') and hour < 12:
                hour += 12
            elif time_period_name == '中午' and hour < 11:
                # 中午一般11-14点，如果是中午3点理解为下午
                pass  # 保持原值
        
        # 清理分隔符
        remaining = remaining.replace('|', '')
        
        confidence = 1 if hour is not None else 0
        
        return hour, minute, confidence, remaining
    
    def _parse_relative(self, text: str, original: str) -> ParseResult:
        """解析相对日期（今天、明天、昨天等）"""
        relative_map = {
            '今天': 0,
            '今日': 0,
            '当天': 0,
            '明天': 1,
            '明日': 1,
            '次日': 1,
            '后天': 2,
            '大后天': 3,
            '昨天': -1,
            '昨日': -1,
            '前天': -2,
            '大前天': -3,
        }
        
        # 按长度降序排序，确保先匹配长关键词（如"大后天"优先于"后天"）
        sorted_map = sorted(relative_map.items(), key=lambda x: len(x[0]), reverse=True)
        
        for keyword, days in sorted_map:
            if keyword in text:
                # 解析时间
                hour, minute, _, remaining = self._parse_time(text)
                
                # 计算日期
                target_date = self.now.date() + timedelta(days=days)
                
                # 如果有具体时间
                if hour is not None:
                    # 处理凌晨跨天
                    if hour >= 24:
                        hour = hour - 24
                        target_date += timedelta(days=1)
                    result_dt = datetime.combine(target_date, time(hour, minute or 0))
                else:
                    result_dt = datetime.combine(target_date, time(0, 0))
                
                return ParseResult(
                    success=True,
                    datetime_obj=result_dt,
                    original_text=original,
                    normalized_text=text,
                    date_type=DateType.RELATIVE,
                    confidence=1.0,
                    has_time=hour is not None
                )
        
        return ParseResult(
            success=False,
            datetime_obj=None,
            original_text=original,
            normalized_text=text,
            date_type=DateType.RELATIVE,
            confidence=0.0,
            has_time=False
        )
    
    def _parse_weekday(self, text: str, original: str) -> ParseResult:
        """解析星期日期（周一、下周三等）"""
        # 匹配模式：这/本/下/上 + 周/星期/礼拜 + X（使用非捕获组处理多字前缀）
        patterns = [
            (r'下(?:周|星期|礼拜)(.)', 1),    # 下周X
            (r'上(?:周|星期|礼拜)(.)', -1),   # 上周X
            (r'[这本](?:周|星期|礼拜)(.)', 0), # 这周X
            (r'(?:周|星期|礼拜)(.)', 0),       # 周X（本周）
        ]
        
        for pattern, week_offset in patterns:
            match = re.search(pattern, text)
            if match:
                weekday_str = match.group(1)
                if weekday_str in self.WEEKDAY_MAP:
                    target_weekday = self.WEEKDAY_MAP[weekday_str]
                    current_weekday = self.now.weekday()
                    
                    # 计算天数差
                    days_diff = target_weekday - current_weekday
                    
                    # 对于"上周"，确保日期确实在过去的一周
                    if week_offset == -1:
                        # 上周X：先减去7天到上一周，再调整
                        days_diff -= 7
                        # 如果上一周的X还没过去（相对于上一周的周一），再减7
                        # 即确保日期 < 当前周
                        if days_diff >= 0:
                            days_diff -= 7
                    elif week_offset == 1:
                        # 下周X：确保日期在未来的一周
                        days_diff += 7
                        # 如果这周的X还没过去，可能需要再加一周
                        if days_diff <= 0:
                            days_diff += 7
                    else:
                        # 这周X：如果目标天已经过了，跳到下周
                        if days_diff <= 0:
                            days_diff += 7
                    
                    # 解析时间
                    hour, minute, _, remaining = self._parse_time(text)
                    
                    target_date = self.now.date() + timedelta(days=days_diff)
                    
                    if hour is not None:
                        result_dt = datetime.combine(target_date, time(hour, minute or 0))
                    else:
                        result_dt = datetime.combine(target_date, time(0, 0))
                    
                    return ParseResult(
                        success=True,
                        datetime_obj=result_dt,
                        original_text=original,
                        normalized_text=text,
                        date_type=DateType.WEEKDAY,
                        confidence=1.0,
                        has_time=hour is not None
                    )
        
        return ParseResult(
            success=False,
            datetime_obj=None,
            original_text=original,
            normalized_text=text,
            date_type=DateType.WEEKDAY,
            confidence=0.0,
            has_time=False
        )
    
    def _parse_monthly(self, text: str, original: str) -> ParseResult:
        """解析月度日期（下个月、每月15号等）"""
        # 下个月/上个月
        month_match = re.search(r'([下上])个?月', text)
        if month_match:
            direction = month_match.group(1)
            month_offset = 1 if direction == '下' else -1
            
            # 解析具体日期
            day_match = re.search(r'(\d{1,2})[号日]', text)
            if day_match:
                target_day = int(day_match.group(1))
            else:
                target_day = self.now.day
            
            # 解析时间
            hour, minute, _, _ = self._parse_time(text)
            
            # 计算目标月份
            target_year = self.now.year
            target_month = self.now.month + month_offset
            if target_month > 12:
                target_year += 1
                target_month -= 12
            elif target_month < 1:
                target_year -= 1
                target_month += 12
            
            try:
                target_date = datetime(target_year, target_month, target_day).date()
                if hour is not None:
                    result_dt = datetime.combine(target_date, time(hour, minute or 0))
                else:
                    result_dt = datetime.combine(target_date, time(0, 0))
                
                return ParseResult(
                    success=True,
                    datetime_obj=result_dt,
                    original_text=original,
                    normalized_text=text,
                    date_type=DateType.MONTHLY,
                    confidence=1.0,
                    has_time=hour is not None
                )
            except ValueError:
                pass
        
        # 月底/月末
        if '月底' in text or '月末' in text:
            month_offset = 1 if '下个' in text else (0 if '这' in text or '本' in text else 0)
            # 计算下月第一天再减一天
            target_year = self.now.year
            target_month = self.now.month + month_offset + 1
            if target_month > 12:
                target_year += 1
                target_month -= 12
            
            try:
                target_date = datetime(target_year, target_month, 1).date() - timedelta(days=1)
                hour, minute, _, _ = self._parse_time(text)
                
                if hour is not None:
                    result_dt = datetime.combine(target_date, time(hour, minute or 0))
                else:
                    result_dt = datetime.combine(target_date, time(0, 0))
                
                return ParseResult(
                    success=True,
                    datetime_obj=result_dt,
                    original_text=original,
                    normalized_text=text,
                    date_type=DateType.MONTHLY,
                    confidence=1.0,
                    has_time=hour is not None
                )
            except:
                pass
        
        return ParseResult(
            success=False,
            datetime_obj=None,
            original_text=original,
            normalized_text=text,
            date_type=DateType.MONTHLY,
            confidence=0.0,
            has_time=False
        )
    
    def _parse_yearly(self, text: str, original: str) -> ParseResult:
        """解析年度日期（明年、今年等）"""
        year_patterns = [
            (r'明年', 1),
            (r'今年', 0),
            (r'去年', -1),
            (r'前年', -2),
            (r'后年', 2),
        ]
        
        for pattern, year_offset in year_patterns:
            if re.search(pattern, text):
                target_year = self.now.year + year_offset
                
                # 解析月份
                month = self.now.month
                for m_name, m_num in self.MONTH_MAP.items():
                    if m_name in text:
                        month = m_num
                        break
                
                # 解析日期
                day = self.now.day
                day_match = re.search(r'(\d{1,2})[号日]', text)
                if day_match:
                    day = int(day_match.group(1))
                
                # 解析时间
                hour, minute, _, _ = self._parse_time(text)
                
                try:
                    target_date = datetime(target_year, month, day).date()
                    if hour is not None:
                        result_dt = datetime.combine(target_date, time(hour, minute or 0))
                    else:
                        result_dt = datetime.combine(target_date, time(0, 0))
                    
                    return ParseResult(
                        success=True,
                        datetime_obj=result_dt,
                        original_text=original,
                        normalized_text=text,
                        date_type=DateType.YEARLY,
                        confidence=1.0,
                        has_time=hour is not None
                    )
                except ValueError:
                    pass
        
        return ParseResult(
            success=False,
            datetime_obj=None,
            original_text=original,
            normalized_text=text,
            date_type=DateType.YEARLY,
            confidence=0.0,
            has_time=False
        )
    
    def _parse_holiday(self, text: str, original: str) -> ParseResult:
        """解析节日日期"""
        for holiday_name, (month, day) in self.HOLIDAYS.items():
            if holiday_name in text:
                # 确定年份
                year = self.now.year
                if '明年' in text:
                    year += 1
                elif '去年' in text:
                    year -= 1
                
                # 解析时间
                hour, minute, _, remaining = self._parse_time(text)
                
                try:
                    target_date = datetime(year, month, day).date()
                    if hour is not None:
                        result_dt = datetime.combine(target_date, time(hour, minute or 0))
                    else:
                        result_dt = datetime.combine(target_date, time(0, 0))
                    
                    return ParseResult(
                        success=True,
                        datetime_obj=result_dt,
                        original_text=original,
                        normalized_text=text,
                        date_type=DateType.ABSOLUTE,
                        confidence=1.0,
                        has_time=hour is not None
                    )
                except ValueError:
                    pass
        
        return ParseResult(
            success=False,
            datetime_obj=None,
            original_text=original,
            normalized_text=text,
            date_type=DateType.ABSOLUTE,
            confidence=0.0,
            has_time=False
        )
    
    def _parse_absolute(self, text: str, original: str) -> ParseResult:
        """解析绝对日期（2024年1月1日、1月15号等）"""
        # 完整日期：YYYY年MM月DD日
        full_match = re.search(r'(\d{4})年(\d{1,2})月(\d{1,2})[号日]', text)
        if full_match:
            year, month, day = int(full_match.group(1)), int(full_match.group(2)), int(full_match.group(3))
            hour, minute, _, _ = self._parse_time(text)
            
            try:
                target_date = datetime(year, month, day).date()
                if hour is not None:
                    result_dt = datetime.combine(target_date, time(hour, minute or 0))
                else:
                    result_dt = datetime.combine(target_date, time(0, 0))
                
                return ParseResult(
                    success=True,
                    datetime_obj=result_dt,
                    original_text=original,
                    normalized_text=text,
                    date_type=DateType.ABSOLUTE,
                    confidence=1.0,
                    has_time=hour is not None
                )
            except ValueError:
                pass
        
        # 月份日期：MM月DD日
        month_day_match = re.search(r'(\d{1,2})月(\d{1,2})[号日]', text)
        if month_day_match:
            month, day = int(month_day_match.group(1)), int(month_day_match.group(2))
            year = self.now.year
            
            # 如果日期已经过了，假设是明年
            try:
                target_date = datetime(year, month, day).date()
                if target_date < self.now.date():
                    year += 1
                    target_date = datetime(year, month, day).date()
            except ValueError:
                return ParseResult(
                    success=False,
                    datetime_obj=None,
                    original_text=original,
                    normalized_text=text,
                    date_type=DateType.ABSOLUTE,
                    confidence=0.0,
                    has_time=False
                )
            
            hour, minute, _, _ = self._parse_time(text)
            if hour is not None:
                result_dt = datetime.combine(target_date, time(hour, minute or 0))
            else:
                result_dt = datetime.combine(target_date, time(0, 0))
            
            return ParseResult(
                success=True,
                datetime_obj=result_dt,
                original_text=original,
                normalized_text=text,
                date_type=DateType.ABSOLUTE,
                confidence=0.9,
                has_time=hour is not None
            )
        
        return ParseResult(
            success=False,
            datetime_obj=None,
            original_text=original,
            normalized_text=text,
            date_type=DateType.ABSOLUTE,
            confidence=0.0,
            has_time=False
        )
    
    def _parse_range(self, text: str, original: str) -> ParseResult:
        """解析日期范围（这周、下个月等）"""
        # 这周/下周/上周
        week_patterns = [
            (r'这[周星期]', 0),
            (r'本[周星期]', 0),
            (r'下[周星期]', 1),
            (r'上[周星期]', -1),
        ]
        
        for pattern, week_offset in week_patterns:
            if re.search(pattern, text):
                current_weekday = self.now.weekday()
                # 一周的开始（周一）
                days_to_monday = current_weekday
                monday = self.now.date() - timedelta(days=days_to_monday)
                
                # 应用偏移
                monday += timedelta(weeks=week_offset)
                sunday = monday + timedelta(days=6)
                
                # 解析时间
                hour, minute, _, _ = self._parse_time(text)
                
                # 返回周一开始
                if hour is not None:
                    result_dt = datetime.combine(monday, time(hour, minute or 0))
                else:
                    result_dt = datetime.combine(monday, time(0, 0))
                
                return ParseResult(
                    success=True,
                    datetime_obj=result_dt,
                    original_text=original,
                    normalized_text=text,
                    date_type=DateType.RANGE,
                    confidence=1.0,
                    has_time=hour is not None
                )
        
        # 这个月/下个月
        month_patterns = [
            (r'这个月', 0),
            (r'本月', 0),
            (r'下个月', 1),
            (r'上个月', -1),
        ]
        
        for pattern, month_offset in month_patterns:
            if re.search(pattern, text):
                target_year = self.now.year
                target_month = self.now.month + month_offset
                
                if target_month > 12:
                    target_year += 1
                    target_month -= 12
                elif target_month < 1:
                    target_year -= 1
                    target_month += 12
                
                try:
                    target_date = datetime(target_year, target_month, 1).date()
                    hour, minute, _, _ = self._parse_time(text)
                    
                    if hour is not None:
                        result_dt = datetime.combine(target_date, time(hour, minute or 0))
                    else:
                        result_dt = datetime.combine(target_date, time(0, 0))
                    
                    return ParseResult(
                        success=True,
                        datetime_obj=result_dt,
                        original_text=original,
                        normalized_text=text,
                        date_type=DateType.RANGE,
                        confidence=1.0,
                        has_time=hour is not None
                    )
                except ValueError:
                    pass
        
        return ParseResult(
            success=False,
            datetime_obj=None,
            original_text=original,
            normalized_text=text,
            date_type=DateType.RANGE,
            confidence=0.0,
            has_time=False
        )
    
    def _parse_number_days(self, text: str, original: str) -> ParseResult:
        """解析数字天数（3天后、两周后等）"""
        # X天后/前
        days_match = re.search(r'(\d+)[天日][以]?[后前]', text)
        if days_match:
            days = int(days_match.group(1))
            if '前' in text:
                days = -days
            
            hour, minute, _, _ = self._parse_time(text)
            target_date = self.now.date() + timedelta(days=days)
            
            if hour is not None:
                result_dt = datetime.combine(target_date, time(hour, minute or 0))
            else:
                result_dt = datetime.combine(target_date, time(0, 0))
            
            return ParseResult(
                success=True,
                datetime_obj=result_dt,
                original_text=original,
                normalized_text=text,
                date_type=DateType.RELATIVE,
                confidence=1.0,
                has_time=hour is not None
            )
        
        # X周后/前
        weeks_match = re.search(r'(\d+)周[以]?[后前]', text)
        if weeks_match:
            weeks = int(weeks_match.group(1))
            if '前' in text:
                weeks = -weeks
            
            hour, minute, _, _ = self._parse_time(text)
            target_date = self.now.date() + timedelta(weeks=weeks)
            
            if hour is not None:
                result_dt = datetime.combine(target_date, time(hour, minute or 0))
            else:
                result_dt = datetime.combine(target_date, time(0, 0))
            
            return ParseResult(
                success=True,
                datetime_obj=result_dt,
                original_text=original,
                normalized_text=text,
                date_type=DateType.RELATIVE,
                confidence=1.0,
                has_time=hour is not None
            )
        
        # X个月后/前
        months_match = re.search(r'(\d+)个?月[以]?[后前]', text)
        if months_match:
            months = int(months_match.group(1))
            if '前' in text:
                months = -months
            
            target_year = self.now.year
            target_month = self.now.month + months
            
            while target_month > 12:
                target_year += 1
                target_month -= 12
            while target_month < 1:
                target_year -= 1
                target_month += 12
            
            try:
                target_date = datetime(target_year, target_month, self.now.day).date()
                hour, minute, _, _ = self._parse_time(text)
                
                if hour is not None:
                    result_dt = datetime.combine(target_date, time(hour, minute or 0))
                else:
                    result_dt = datetime.combine(target_date, time(0, 0))
                
                return ParseResult(
                    success=True,
                    datetime_obj=result_dt,
                    original_text=original,
                    normalized_text=text,
                    date_type=DateType.RELATIVE,
                    confidence=0.9,
                    has_time=hour is not None
                )
            except ValueError:
                pass
        
        # X年后/前
        years_match = re.search(r'(\d+)年[以]?[后前]', text)
        if years_match:
            years = int(years_match.group(1))
            if '前' in text:
                years = -years
            
            target_year = self.now.year + years
            try:
                target_date = datetime(target_year, self.now.month, self.now.day).date()
                hour, minute, _, _ = self._parse_time(text)
                
                if hour is not None:
                    result_dt = datetime.combine(target_date, time(hour, minute or 0))
                else:
                    result_dt = datetime.combine(target_date, time(0, 0))
                
                return ParseResult(
                    success=True,
                    datetime_obj=result_dt,
                    original_text=original,
                    normalized_text=text,
                    date_type=DateType.RELATIVE,
                    confidence=0.9,
                    has_time=hour is not None
                )
            except ValueError:
                pass
        
        return ParseResult(
            success=False,
            datetime_obj=None,
            original_text=original,
            normalized_text=text,
            date_type=DateType.RELATIVE,
            confidence=0.0,
            has_time=False
        )


# 便捷函数
def parse(text: str, now: Optional[datetime] = None) -> Optional[datetime]:
    """
    快速解析自然语言日期
    
    Args:
        text: 自然语言日期文本
        now: 参考时间
        
    Returns:
        解析后的 datetime 对象，失败返回 None
    """
    parser = NaturalDateParser(now=now)
    result = parser.parse(text)
    return result.datetime_obj


def parse_with_info(text: str, now: Optional[datetime] = None) -> ParseResult:
    """
    解析自然语言日期，返回详细信息
    
    Args:
        text: 自然语言日期文本
        now: 参考时间
        
    Returns:
        ParseResult 解析结果
    """
    parser = NaturalDateParser(now=now)
    return parser.parse(text)


def is_valid(text: str, now: Optional[datetime] = None) -> bool:
    """
    检查是否能解析为有效日期
    
    Args:
        text: 自然语言日期文本
        now: 参考时间
        
    Returns:
        是否能解析
    """
    parser = NaturalDateParser(now=now)
    result = parser.parse(text)
    return result.success


def get_date_type(text: str, now: Optional[datetime] = None) -> DateType:
    """
    获取日期表达式类型
    
    Args:
        text: 自然语言日期文本
        now: 参考时间
        
    Returns:
        DateType 日期类型
    """
    parser = NaturalDateParser(now=now)
    result = parser.parse(text)
    return result.date_type


def parse_range(text: str, now: Optional[datetime] = None) -> Tuple[Optional[datetime], Optional[datetime]]:
    """
    解析日期范围
    
    Args:
        text: 自然语言日期范围文本（这周、下个月等）
        now: 参考时间
        
    Returns:
        (开始日期, 结束日期) 元组
    """
    parser = NaturalDateParser(now=now)
    result = parser.parse(text)
    
    if not result.success:
        return None, None
    
    if result.date_type != DateType.RANGE:
        return result.datetime_obj, result.datetime_obj
    
    # 处理范围
    start = result.datetime_obj
    
    if '周' in text or '星期' in text:
        # 一周
        end = datetime.combine(start.date() + timedelta(days=6), time(23, 59, 59))
    elif '月' in text:
        # 一个月
        import calendar
        _, last_day = calendar.monthrange(start.year, start.month)
        end = datetime(start.year, start.month, last_day, 23, 59, 59)
    else:
        end = start
    
    return start, end


# 批量解析
def parse_batch(texts: List[str], now: Optional[datetime] = None) -> List[ParseResult]:
    """
    批量解析日期表达式
    
    Args:
        texts: 日期文本列表
        now: 参考时间
        
    Returns:
        ParseResult 列表
    """
    parser = NaturalDateParser(now=now)
    return [parser.parse(text) for text in texts]


# 提取文本中的日期
def extract_dates(text: str, now: Optional[datetime] = None) -> List[Tuple[str, datetime]]:
    """
    从文本中提取日期
    
    Args:
        text: 包含日期的文本
        now: 参考时间
        
    Returns:
        [(原始文本, 解析结果), ...] 列表
    """
    parser = NaturalDateParser(now=now)
    results = []
    
    # 可能的日期关键词
    keywords = [
        '今天', '明天', '后天', '昨天', '前天',
        '下周', '这周', '上周',
        '下月', '这个月', '上月',
        '明年', '今年', '去年',
    ]
    
    # 添加周几
    for day in ['一', '二', '三', '四', '五', '六', '天', '日']:
        keywords.extend([f'周{day}', f'星期{day}'])
    
    for keyword in keywords:
        if keyword in text:
            result = parser.parse(keyword)
            if result.success:
                results.append((keyword, result.datetime_obj))
    
    return results
"""
Natural Time Parser Utilities - 自然语言时间解析工具模块

解析人类友好的时间表达式，支持中英文混合输入。
零依赖，仅使用 Python 标准库。

支持的格式：
- 相对时间：in 5 minutes, 2小时后, 3天后的下午
- 绝对时间：tomorrow, next monday, 下周三
- 时间点：at 3pm, 早上8点, 下午3点半
- 组合表达式：tomorrow at 3pm, 下周一早上9点

Author: AllToolkit
Version: 1.0.0
"""

import re
from datetime import datetime, timedelta, time
from typing import Optional, Tuple, Dict, List, Any, Union
from calendar import monthrange


class ParseError(Exception):
    """解析错误异常"""
    pass


class NaturalTimeParser:
    """自然语言时间解析器"""
    
    # 中文数字映射
    CN_NUMBERS = {
        '零': 0, '一': 1, '二': 2, '三': 3, '四': 4,
        '五': 5, '六': 6, '七': 7, '八': 8, '九': 9,
        '十': 10, '十一': 11, '十二': 12, '十三': 13, '十四': 14,
        '十五': 15, '十六': 16, '十七': 17, '十八': 18, '十九': 19,
        '二十': 20, '二十一': 21, '二十二': 22, '二十三': 23, '二十四': 24,
        '两': 2,
    }
    
    # 英文数字映射
    EN_NUMBERS = {
        'zero': 0, 'one': 1, 'two': 2, 'three': 3, 'four': 4,
        'five': 5, 'six': 6, 'seven': 7, 'eight': 8, 'nine': 9,
        'ten': 10, 'eleven': 11, 'twelve': 12, 'thirteen': 13,
        'fourteen': 14, 'fifteen': 15, 'sixteen': 16, 'seventeen': 17,
        'eighteen': 18, 'nineteen': 19, 'twenty': 20, 'thirty': 30,
        'forty': 40, 'fifty': 50, 'sixty': 60,
    }
    
    # 英文星期映射
    EN_WEEKDAYS = {
        'monday': 0, 'tuesday': 1, 'wednesday': 2, 'thursday': 3,
        'friday': 4, 'saturday': 5, 'sunday': 6,
        'mon': 0, 'tue': 1, 'tues': 1, 'wed': 2, 'thu': 3, 'thur': 3, 'thurs': 3,
        'fri': 4, 'sat': 5, 'sun': 6,
    }
    
    # 中文星期映射
    CN_WEEKDAYS = {
        '周一': 0, '周二': 1, '周三': 2, '周四': 3, '周五': 4, '周六': 5, '周日': 6,
        '星期一': 0, '星期二': 1, '星期三': 2, '星期四': 3, '星期五': 4,
        '星期六': 5, '星期日': 6, '星期天': 6,
        '礼拜一': 0, '礼拜二': 1, '礼拜三': 2, '礼拜四': 3, '礼拜五': 4,
        '礼拜六': 5, '礼拜日': 6, '礼拜天': 6,
    }
    
    # 时间单位映射（英文）
    EN_UNITS = {
        'second': 'seconds', 'seconds': 'seconds', 'sec': 'seconds', 's': 'seconds',
        'minute': 'minutes', 'minutes': 'minutes', 'min': 'minutes', 'm': 'minutes',
        'hour': 'hours', 'hours': 'hours', 'hr': 'hours', 'h': 'hours',
        'day': 'days', 'days': 'days', 'd': 'days',
        'week': 'weeks', 'weeks': 'weeks', 'w': 'weeks',
        'month': 'months', 'months': 'months',
        'year': 'years', 'years': 'years', 'y': 'years',
    }
    
    # 时间单位映射（中文）
    CN_UNITS = {
        '秒': 'seconds', '秒钟': 'seconds',
        '分钟': 'minutes', '分': 'minutes',
        '小时': 'hours', '钟头': 'hours', '个钟头': 'hours',
        '天': 'days', '日': 'days',
        '周': 'weeks', '星期': 'weeks', '个星期': 'weeks',
        '月': 'months', '个月': 'months',
        '年': 'years',
    }
    
    # 时间段关键词（英文）
    EN_PERIODS = {
        'morning': (6, 12), 'am': None,  # am 需要特殊处理
        'afternoon': (12, 18), 'pm': None,
        'evening': (18, 22),
        'night': (22, 6), 'midnight': (0, 0),
        'noon': (12, 12),
    }
    
    # 时间段关键词（中文）
    CN_PERIODS = {
        '早上': (6, 9), '上午': (9, 12), '中午': (12, 14),
        '下午': (14, 18), '傍晚': (18, 20), '晚上': (18, 22),
        '深夜': (22, 2), '凌晨': (0, 6), '半夜': (0, 3),
    }
    
    def __init__(self, reference_time: Optional[datetime] = None):
        """
        初始化解析器
        
        Args:
            reference_time: 参考时间（默认为当前时间）
        """
        self.reference_time = reference_time or datetime.now()
    
    def parse(self, text: str) -> datetime:
        """
        解析自然语言时间表达式
        
        Args:
            text: 时间表达式字符串
            
        Returns:
            解析后的 datetime 对象
            
        Raises:
            ParseError: 无法解析表达式
        """
        text = text.strip().lower()
        if not text:
            raise ParseError("Empty input")
        
        # 尝试各种解析策略（组合表达式优先，因为它能处理更复杂的情况）
        parsers = [
            self._parse_combined,      # 组合表达式优先
            self._parse_relative,
            self._parse_absolute,
            self._parse_time_only,
        ]
        
        for parser in parsers:
            try:
                result = parser(text)
                if result:
                    return result
            except Exception:
                continue
        
        raise ParseError(f"Cannot parse time expression: {text}")
    
    def _parse_relative(self, text: str) -> Optional[datetime]:
        """解析相对时间表达式"""
        # 英文模式: in X unit(s), X unit(s) later, after X unit(s)
        # 中文模式: X单位后, X个单位后
        
        # 英文: in X minutes/hours/days/weeks/months/years
        pattern_en = r'(?:in\s+)?(\d+)\s+(second|seconds|sec|minute|minutes|min|hour|hours|hr|day|days|d|week|weeks|w|month|months|year|years|y)s?'
        match = re.search(pattern_en, text)
        if match:
            amount = int(match.group(1))
            unit = self.EN_UNITS.get(match.group(2))
            if unit:
                return self._add_time(amount, unit)
        
        # 英文数字: in five minutes
        pattern_en_word = r'(?:in\s+)?(zero|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|forty|fifty|sixty)\s+(second|seconds|minute|minutes|hour|hours|day|days|week|weeks|month|months|year|years)s?'
        match = re.search(pattern_en_word, text)
        if match:
            amount = self.EN_NUMBERS.get(match.group(1), 0)
            unit = self.EN_UNITS.get(match.group(2))
            if unit:
                return self._add_time(amount, unit)
        
        # 中文: X分钟/小时/天/周/月/年后
        pattern_cn = r'([一二三四五六七八九十两]+|\d+)\s*(秒|秒钟|分钟|分|小时|钟头|天|日|周|星期|个月|月|年)\s*后'
        match = re.search(pattern_cn, text)
        if match:
            amount_str = match.group(1)
            amount = self._parse_chinese_number(amount_str)
            unit = self.CN_UNITS.get(match.group(2))
            if unit:
                return self._add_time(amount, unit)
        
        # 中文: 半小时后, 一刻钟后
        if '半小时后' in text or '半个钟头后' in text:
            return self._add_time(30, 'minutes')
        if '一刻钟后' in text or '一刻后' in text:
            return self._add_time(15, 'minutes')
        
        return None
    
    def _parse_absolute(self, text: str) -> Optional[datetime]:
        """解析绝对时间表达式"""
        result = self.reference_time
        
        # today / 今天
        if 'today' in text or '今天' in text:
            result = self._set_date_from_relative(0)
        # tomorrow / 明天
        elif 'tomorrow' in text or '明天' in text:
            result = self._set_date_from_relative(1)
        # yesterday / 昨天
        elif 'yesterday' in text or '昨天' in text:
            result = self._set_date_from_relative(-1)
        # day after tomorrow / 后天
        elif 'day after tomorrow' in text or '后天' in text:
            result = self._set_date_from_relative(2)
        # day before yesterday / 前天
        elif 'day before yesterday' in text or '前天' in text:
            result = self._set_date_from_relative(-2)
        # next week / 下周
        elif 'next week' in text:
            days_ahead = 7 - self.reference_time.weekday()
            result = self.reference_time + timedelta(days=days_ahead)
        elif '下周' in text:
            return self._parse_chinese_week(text, week_offset=1)
        # this week / 本周
        elif 'this week' in text or '本周' in text:
            pass  # 保持当前日期
        # last week / 上周
        elif 'last week' in text:
            result = self.reference_time - timedelta(weeks=1)
        elif '上周' in text:
            return self._parse_chinese_week(text, week_offset=-1)
        # next/last + weekday (English: "next X" means nearest upcoming, not necessarily next week)
        elif 'next' in text:
            match = re.search(r'next\s+(monday|tuesday|wednesday|thursday|friday|saturday|sunday|mon|tue|wed|thu|fri|sat|sun)', text)
            if match:
                weekday_name = match.group(1)
                target_weekday = self.EN_WEEKDAYS.get(weekday_name)
                if target_weekday is not None:
                    # "next Monday" in English usually means the nearest upcoming Monday
                    return self._get_nearest_weekday(target_weekday)
        elif 'last' in text:
            match = re.search(r'last\s+(monday|tuesday|wednesday|thursday|friday|saturday|sunday|mon|tue|tues|wed|thu|thur|thurs|fri|sat|sun)', text)
            if match:
                weekday_name = match.group(1)
                target_weekday = self.EN_WEEKDAYS.get(weekday_name)
                if target_weekday is not None:
                    return self._get_last_weekday(target_weekday)
        
        # 中文星期: 周一/星期一/礼拜一 + 下周/本周
        for cn_weekday, weekday_num in self.CN_WEEKDAYS.items():
            if cn_weekday in text:
                # 判断是下周还是本周
                if '下' in text:
                    return self._get_next_weekday(weekday_num, week_offset=1)
                elif '上' in text:
                    return self._get_last_weekday(weekday_num)
                else:
                    # 本周或最近的
                    return self._get_nearest_weekday(weekday_num)
        
        # 解析时间段并更新时间
        time_result = self._parse_time_period(text, result)
        if time_result:
            result = time_result
        
        return result if result != self.reference_time else None
    
    def _parse_time_only(self, text: str) -> Optional[datetime]:
        """解析纯时间表达式（无日期部分）"""
        # 中文时间优先检查（因为英文正则可能误匹配中文表达式）
        # 检查时间段关键词
        period_keywords = ['早上', '上午', '中午', '下午', '傍晚', '晚上', '深夜', '凌晨', '半夜']
        detected_period = None
        for period in period_keywords:
            if period in text:
                detected_period = period
                break
        
        # 中文时间: 3点, 3点半, 3点15分
        pattern_time_cn = r'(\d{1,2})\s*点\s*(\d{1,2})?\s*分?\s*(半|一刻)?'
        match = re.search(pattern_time_cn, text)
        if match:
            hour = int(match.group(1))
            minute = 0
            if match.group(2):
                minute = int(match.group(2))
            elif match.group(3) == '半':
                minute = 30
            elif match.group(3) == '一刻':
                minute = 15
            
            # 根据时间段调整小时
            if detected_period:
                if detected_period == '下午' and hour < 12:
                    hour += 12
                elif detected_period == '晚上' and hour < 12:
                    hour += 12
                elif detected_period == '傍晚' and hour < 12:
                    hour += 12
                # 凌晨、深夜、半夜、早上、上午、中午 保持原样
            
            if 0 <= hour < 24 and 0 <= minute < 60:
                return self.reference_time.replace(hour=hour, minute=minute, second=0, microsecond=0)
        
        # 英文时间: at 3pm, at 3:30pm, at 15:30 (需要明确的英文上下文)
        # 必须有 'at' 或 am/pm 标记才会匹配
        pattern_time_en = r'(?:at\s+)(\d{1,2})(?::(\d{2}))?\s*(am|pm)?|(\d{1,2})(?::(\d{2}))?\s*(am|pm)'
        match = re.search(pattern_time_en, text)
        if match:
            # Determine which group matched
            if match.group(1):  # 'at X' pattern
                hour = int(match.group(1))
                minute = int(match.group(2)) if match.group(2) else 0
                ampm = match.group(3)
            else:  # 'X am/pm' pattern
                hour = int(match.group(4))
                minute = int(match.group(5)) if match.group(5) else 0
                ampm = match.group(6)
            
            if ampm == 'pm' and hour < 12:
                hour += 12
            elif ampm == 'am' and hour == 12:
                hour = 0
            
            if 0 <= hour < 24 and 0 <= minute < 60:
                return self.reference_time.replace(hour=hour, minute=minute, second=0, microsecond=0)
        
        return None
    
    def _parse_combined(self, text: str) -> Optional[datetime]:
        """解析组合表达式"""
        # 先解析日期部分
        date_part = None
        
        # tomorrow at X, 明天X点
        if 'tomorrow' in text or '明天' in text:
            date_part = self._set_date_from_relative(1)
        elif 'today' in text or '今天' in text:
            date_part = self._set_date_from_relative(0)
        elif '后天' in text:
            date_part = self._set_date_from_relative(2)
        
        # 解析英文星期 next/last + weekday ("next X" means nearest upcoming)
        if 'next' in text:
            match = re.search(r'next\s+(monday|tuesday|wednesday|thursday|friday|saturday|sunday|mon|tue|wed|thu|fri|sat|sun)', text)
            if match:
                weekday_name = match.group(1)
                target_weekday = self.EN_WEEKDAYS.get(weekday_name)
                if target_weekday is not None:
                    date_part = self._get_nearest_weekday(target_weekday)
        
        # 解析中文星期: 周一/星期一/礼拜一 + 下周/上周/本周
        for cn_weekday, weekday_num in self.CN_WEEKDAYS.items():
            if cn_weekday in text:
                if '下' in text:
                    date_part = self._get_next_weekday(weekday_num, week_offset=1)
                elif '上' in text:
                    date_part = self._get_last_weekday(weekday_num)
                else:
                    date_part = self._get_nearest_weekday(weekday_num)
                break
        
        # 如果找到日期部分，尝试解析时间部分
        if date_part:
            time_result = self._parse_time_only(text)
            if time_result:
                return date_part.replace(
                    hour=time_result.hour,
                    minute=time_result.minute,
                    second=0,
                    microsecond=0
                )
            # 尝试解析时间段
            period_result = self._parse_time_period(text, date_part)
            if period_result:
                return period_result
            return date_part
        
        return None
    
    def _parse_time_period(self, text: str, base_date: datetime) -> Optional[datetime]:
        """解析时间段（早上、下午等）"""
        # 中文时间段
        for period, (start_hour, end_hour) in self.CN_PERIODS.items():
            if period in text:
                # 如果没有具体时间，使用时间段的开始时间
                if not re.search(r'\d+\s*点', text):
                    return base_date.replace(hour=start_hour, minute=0, second=0, microsecond=0)
        
        # 英文时间段
        if 'morning' in text and not re.search(r'\d+\s*(?:am|pm)', text):
            if not re.search(r'\d{1,2}:?\d*\s*(?:am|pm)?', text):
                return base_date.replace(hour=9, minute=0, second=0, microsecond=0)
        if 'afternoon' in text and not re.search(r'\d+\s*(?:am|pm)', text):
            if not re.search(r'\d{1,2}:?\d*\s*(?:am|pm)?', text):
                return base_date.replace(hour=14, minute=0, second=0, microsecond=0)
        if 'evening' in text and not re.search(r'\d+\s*(?:am|pm)', text):
            if not re.search(r'\d{1,2}:?\d*\s*(?:am|pm)?', text):
                return base_date.replace(hour=19, minute=0, second=0, microsecond=0)
        if 'noon' in text:
            return base_date.replace(hour=12, minute=0, second=0, microsecond=0)
        if 'midnight' in text:
            return base_date.replace(hour=0, minute=0, second=0, microsecond=0)
        
        return None
    
    def _parse_chinese_week(self, text: str, week_offset: int = 0) -> datetime:
        """解析中文星期表达式"""
        for cn_weekday, weekday_num in self.CN_WEEKDAYS.items():
            if cn_weekday in text:
                return self._get_next_weekday(weekday_num, week_offset=week_offset)
        return self.reference_time
    
    def _parse_chinese_number(self, text: str) -> int:
        """解析中文数字"""
        if text.isdigit():
            return int(text)
        
        # 直接匹配
        if text in self.CN_NUMBERS:
            return self.CN_NUMBERS[text]
        
        # 处理二十、三十等
        if text.startswith('二十'):
            rest = text[2:]
            if rest:
                return 20 + self.CN_NUMBERS.get(rest, 0)
            return 20
        if text.startswith('三十'):
            rest = text[2:]
            if rest:
                return 30 + self.CN_NUMBERS.get(rest, 0)
            return 30
        
        return 0
    
    def _add_time(self, amount: int, unit: str) -> datetime:
        """添加时间"""
        kwargs = {unit: amount}
        return self.reference_time + timedelta(**kwargs) if unit != 'months' and unit != 'years' else self._add_months_or_years(amount, unit)
    
    def _add_months_or_years(self, amount: int, unit: str) -> datetime:
        """添加月份或年份"""
        if unit == 'months':
            new_month = self.reference_time.month + amount
            new_year = self.reference_time.year + (new_month - 1) // 12
            new_month = (new_month - 1) % 12 + 1
        elif unit == 'years':
            new_year = self.reference_time.year + amount
            new_month = self.reference_time.month
        else:
            return self.reference_time
        
        # 处理日期溢出（如1月31日加一个月）
        max_day = monthrange(new_year, new_month)[1]
        new_day = min(self.reference_time.day, max_day)
        
        return self.reference_time.replace(year=new_year, month=new_month, day=new_day)
    
    def _set_date_from_relative(self, days: int) -> datetime:
        """设置相对日期"""
        new_date = self.reference_time + timedelta(days=days)
        return new_date.replace(hour=0, minute=0, second=0, microsecond=0)
    
    def _get_next_weekday(self, target_weekday: int, week_offset: int = 0) -> datetime:
        """获取下一个指定星期几
        
        Args:
            target_weekday: 目标星期几 (0=Monday, 6=Sunday)
            week_offset: 周偏移量
                - 0: 本周最近的（如果今天已过则取下周最近）
                - 1: 下周的（跳过本周，从下周开始算）
                - -1: 上周的
        """
        current_weekday = self.reference_time.weekday()
        
        if week_offset == 1:
            # 下周：明确要下周的某天，跳过本周
            days_ahead = 7 + (target_weekday - current_weekday)
        elif week_offset == -1:
            # 上周
            days_ahead = -7 + (target_weekday - current_weekday)
        else:
            # 本周最近的：如果目标日还没到或就是今天，取本周；否则取下周
            days_ahead = target_weekday - current_weekday
            if days_ahead < 0:
                days_ahead += 7
        
        result = self.reference_time + timedelta(days=days_ahead)
        return result.replace(hour=0, minute=0, second=0, microsecond=0)
    
    def _get_last_weekday(self, target_weekday: int) -> datetime:
        """获取上一个指定星期几"""
        current_weekday = self.reference_time.weekday()
        days_behind = current_weekday - target_weekday
        if days_behind <= 0:
            days_behind += 7
        result = self.reference_time - timedelta(days=days_behind)
        return result.replace(hour=0, minute=0, second=0, microsecond=0)
    
    def _get_nearest_weekday(self, target_weekday: int) -> datetime:
        """获取最近的指定星期几（如果已过则取下周）"""
        current_weekday = self.reference_time.weekday()
        days_ahead = target_weekday - current_weekday
        if days_ahead < 0:
            days_ahead += 7
        result = self.reference_time + timedelta(days=days_ahead)
        return result.replace(hour=0, minute=0, second=0, microsecond=0)


class DurationParser:
    """时长解析器"""
    
    # 时长单位映射（英文）
    EN_DURATION_UNITS = {
        's': 'seconds', 'sec': 'seconds', 'second': 'seconds', 'seconds': 'seconds',
        'm': 'minutes', 'min': 'minutes', 'minute': 'minutes', 'minutes': 'minutes',
        'h': 'hours', 'hr': 'hours', 'hour': 'hours', 'hours': 'hours',
        'd': 'days', 'day': 'days', 'days': 'days',
        'w': 'weeks', 'wk': 'weeks', 'week': 'weeks', 'weeks': 'weeks',
    }
    
    # 时长单位映射（中文）
    CN_DURATION_UNITS = {
        '秒': 'seconds', '秒钟': 'seconds',
        '分': 'minutes', '分钟': 'minutes',
        '小时': 'hours', '钟头': 'hours',
        '天': 'days', '日': 'days',
        '周': 'weeks', '星期': 'weeks',
    }
    
    @classmethod
    def parse(cls, text: str) -> timedelta:
        """
        解析时长表达式
        
        Args:
            text: 时长表达式（如 "2h 30m", "1小时30分钟", "90 seconds"）
            
        Returns:
            timedelta 对象
            
        Raises:
            ParseError: 无法解析表达式
        """
        text = text.strip().lower()
        if not text:
            raise ParseError("Empty input")
        
        total_seconds = 0
        
        # 模式1: 数字+单位格式（可多个组合）
        # 英文: 2h 30m, 1h30m, 2 hours 30 minutes
        pattern_en = r'(\d+)\s*(s|sec|second|seconds|m|min|minute|minutes|h|hr|hour|hours|d|day|days|w|wk|week|weeks)s?\b'
        matches = re.findall(pattern_en, text)
        for amount_str, unit in matches:
            amount = int(amount_str)
            unit_name = cls.EN_DURATION_UNITS.get(unit)
            if unit_name == 'seconds':
                total_seconds += amount
            elif unit_name == 'minutes':
                total_seconds += amount * 60
            elif unit_name == 'hours':
                total_seconds += amount * 3600
            elif unit_name == 'days':
                total_seconds += amount * 86400
            elif unit_name == 'weeks':
                total_seconds += amount * 604800
        
        # 中文: 2小时30分钟, 1小时30分, 90秒
        pattern_cn = r'(\d+)\s*(秒|秒钟|分|分钟|小时|钟头|天|日|周|星期)'
        matches = re.findall(pattern_cn, text)
        for amount_str, unit in matches:
            amount = int(amount_str)
            unit_name = cls.CN_DURATION_UNITS.get(unit)
            if unit_name == 'seconds':
                total_seconds += amount
            elif unit_name == 'minutes':
                total_seconds += amount * 60
            elif unit_name == 'hours':
                total_seconds += amount * 3600
            elif unit_name == 'days':
                total_seconds += amount * 86400
            elif unit_name == 'weeks':
                total_seconds += amount * 604800
        
        # 中文特殊: 半小时, 一刻钟
        if '半小时' in text or '半个钟头' in text:
            total_seconds += 30 * 60
        if '一刻钟' in text or '一刻' in text:
            total_seconds += 15 * 60
        
        # 冒号格式: 1:30:00, 2:30
        pattern_colon = r'(\d+):(\d+)(?::(\d+))?'
        match = re.search(pattern_colon, text)
        if match:
            hours = int(match.group(1))
            minutes = int(match.group(2))
            seconds = int(match.group(3)) if match.group(3) else 0
            total_seconds += hours * 3600 + minutes * 60 + seconds
        
        if total_seconds == 0:
            raise ParseError(f"Cannot parse duration: {text}")
        
        return timedelta(seconds=total_seconds)
    
    @classmethod
    def format_duration(cls, duration: timedelta, language: str = 'en') -> str:
        """
        格式化时长
        
        Args:
            duration: timedelta 对象
            language: 语言 ('en' 或 'cn')
            
        Returns:
            格式化后的时长字符串
        """
        total_seconds = int(duration.total_seconds())
        
        weeks = total_seconds // 604800
        days = (total_seconds % 604800) // 86400
        hours = (total_seconds % 86400) // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        
        parts = []
        
        if language == 'cn':
            if weeks:
                parts.append(f"{weeks}周")
            if days:
                parts.append(f"{days}天")
            if hours:
                parts.append(f"{hours}小时")
            if minutes:
                parts.append(f"{minutes}分钟")
            if seconds or not parts:
                parts.append(f"{seconds}秒")
        else:
            if weeks:
                parts.append(f"{weeks} week{'s' if weeks > 1 else ''}")
            if days:
                parts.append(f"{days} day{'s' if days > 1 else ''}")
            if hours:
                parts.append(f"{hours} hour{'s' if hours > 1 else ''}")
            if minutes:
                parts.append(f"{minutes} minute{'s' if minutes > 1 else ''}")
            if seconds or not parts:
                parts.append(f"{seconds} second{'s' if seconds != 1 else ''}")
        
        return ' '.join(parts) if language == 'en' else ''.join(parts)


class TimeExpressionExtractor:
    """时间表达式提取器"""
    
    # 时间表达式模式
    PATTERNS = [
        # 英文相对时间
        r'(?:in\s+)?(\d+)\s+(?:second|minute|hour|day|week|month|year)s?',
        r'(?:in\s+)?(?:one|two|three|four|five|six|seven|eight|nine|ten)\s+(?:second|minute|hour|day|week|month|year)s?',
        # 英文绝对时间
        r'\b(?:today|tomorrow|yesterday)\b',
        r'\b(?:next|last)\s+(?:monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b',
        # 时间点
        r'\b(?:at\s+)?\d{1,2}(?::\d{2})?\s*(?:am|pm)?\b',
        # 中文相对时间
        r'[一二三四五六七八九十两\d]+\s*(?:秒|分钟|小时|天|周|月|年)\s*后',
        # 中文绝对时间
        r'(?:今天|明天|昨天|后天|前天)',
        r'(?:下|上|本)?(?:周|星期|礼拜)[一二三四五六日天]',
        # 中文时间点
        r'(?:早上|上午|中午|下午|傍晚|晚上|深夜|凌晨)?\d{1,2}\s*点(?:\d{1,2}\s*分?)?(?:半|一刻)?',
    ]
    
    @classmethod
    def extract(cls, text: str) -> List[Dict[str, Any]]:
        """
        从文本中提取时间表达式
        
        Args:
            text: 输入文本
            
        Returns:
            提取结果列表，每个元素包含:
            - match: 匹配的文本
            - start: 起始位置
            - end: 结束位置
            - parsed: 解析后的 datetime（如果可解析）
        """
        results = []
        parser = NaturalTimeParser()
        
        for pattern in cls.PATTERNS:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                matched_text = match.group(0)
                start = match.start()
                end = match.end()
                
                try:
                    parsed = parser.parse(matched_text)
                except ParseError:
                    parsed = None
                
                results.append({
                    'match': matched_text,
                    'start': start,
                    'end': end,
                    'parsed': parsed,
                })
        
        # 按位置排序并去重
        results.sort(key=lambda x: (x['start'], -len(x['match'])))
        unique_results = []
        seen_positions = set()
        
        for result in results:
            pos = (result['start'], result['end'])
            if pos not in seen_positions:
                seen_positions.add(pos)
                unique_results.append(result)
        
        return unique_results


class RelativeTimeFormatter:
    """相对时间格式化器"""
    
    # 中文时间描述
    CN_RELATIVE = {
        'just_now': '刚刚',
        'seconds_ago': '{seconds}秒前',
        'minutes_ago': '{minutes}分钟前',
        'hours_ago': '{hours}小时前',
        'yesterday': '昨天',
        'days_ago': '{days}天前',
        'weeks_ago': '{weeks}周前',
        'months_ago': '{months}个月前',
        'years_ago': '{years}年前',
        'in_seconds': '{seconds}秒后',
        'in_minutes': '{minutes}分钟后',
        'in_hours': '{hours}小时后',
        'tomorrow': '明天',
        'in_days': '{days}天后',
        'in_weeks': '{weeks}周后',
        'in_months': '{months}个月后',
        'in_years': '{years}年后',
    }
    
    # 英文时间描述
    EN_RELATIVE = {
        'just_now': 'just now',
        'seconds_ago': '{seconds} seconds ago',
        'minutes_ago': '{minutes} minutes ago',
        'hours_ago': '{hours} hours ago',
        'yesterday': 'yesterday',
        'days_ago': '{days} days ago',
        'weeks_ago': '{weeks} weeks ago',
        'months_ago': '{months} months ago',
        'years_ago': '{years} years ago',
        'in_seconds': 'in {seconds} seconds',
        'in_minutes': 'in {minutes} minutes',
        'in_hours': 'in {hours} hours',
        'tomorrow': 'tomorrow',
        'in_days': 'in {days} days',
        'in_weeks': 'in {weeks} weeks',
        'in_months': 'in {months} months',
        'in_years': 'in {years} years',
    }
    
    @classmethod
    def format(cls, dt: datetime, reference: Optional[datetime] = None, 
               language: str = 'auto') -> str:
        """
        格式化相对时间
        
        Args:
            dt: 目标时间
            reference: 参考时间（默认为当前时间）
            language: 语言 ('en', 'cn', 或 'auto')
            
        Returns:
            相对时间描述
        """
        if reference is None:
            reference = datetime.now()
        
        # 自动检测语言
        if language == 'auto':
            language = 'cn'  # 默认中文
        
        templates = cls.CN_RELATIVE if language == 'cn' else cls.EN_RELATIVE
        
        diff = dt - reference
        total_seconds = abs(diff.total_seconds())
        
        # 判断是过去还是未来
        is_future = diff.total_seconds() > 0
        
        if total_seconds < 10:
            return templates['just_now']
        elif total_seconds < 60:
            seconds = int(total_seconds)
            key = 'in_seconds' if is_future else 'seconds_ago'
            return templates[key].format(seconds=seconds)
        elif total_seconds < 3600:
            minutes = int(total_seconds // 60)
            key = 'in_minutes' if is_future else 'minutes_ago'
            return templates[key].format(minutes=minutes)
        elif total_seconds < 86400:
            hours = int(total_seconds // 3600)
            key = 'in_hours' if is_future else 'hours_ago'
            return templates[key].format(hours=hours)
        elif total_seconds < 172800:  # 2天
            key = 'tomorrow' if is_future else 'yesterday'
            return templates[key]
        elif total_seconds < 604800:  # 1周
            days = int(total_seconds // 86400)
            key = 'in_days' if is_future else 'days_ago'
            return templates[key].format(days=days)
        elif total_seconds < 2592000:  # 30天
            weeks = int(total_seconds // 604800)
            key = 'in_weeks' if is_future else 'weeks_ago'
            return templates[key].format(weeks=weeks)
        elif total_seconds < 31536000:  # 1年
            months = int(total_seconds // 2592000)
            key = 'in_months' if is_future else 'months_ago'
            return templates[key].format(months=months)
        else:
            years = int(total_seconds // 31536000)
            key = 'in_years' if is_future else 'years_ago'
            return templates[key].format(years=years)


# ============================================================================
# 便捷函数
# ============================================================================

def parse_time(text: str, reference: Optional[datetime] = None) -> datetime:
    """
    解析自然语言时间表达式
    
    Args:
        text: 时间表达式
        reference: 参考时间（默认为当前时间）
        
    Returns:
        解析后的 datetime
    """
    parser = NaturalTimeParser(reference)
    return parser.parse(text)


def parse_duration(text: str) -> timedelta:
    """
    解析时长表达式
    
    Args:
        text: 时长表达式
        
    Returns:
        timedelta 对象
    """
    return DurationParser.parse(text)


def format_duration(duration: timedelta, language: str = 'cn') -> str:
    """
    格式化时长
    
    Args:
        duration: timedelta 对象
        language: 语言 ('en' 或 'cn')
        
    Returns:
        格式化后的字符串
    """
    return DurationParser.format_duration(duration, language)


def extract_times(text: str) -> List[Dict[str, Any]]:
    """
    从文本中提取时间表达式
    
    Args:
        text: 输入文本
        
    Returns:
        提取结果列表
    """
    return TimeExpressionExtractor.extract(text)


def relative_time(dt: datetime, reference: Optional[datetime] = None, 
                  language: str = 'auto') -> str:
    """
    格式化相对时间
    
    Args:
        dt: 目标时间
        reference: 参考时间（默认为当前时间）
        language: 语言 ('en', 'cn', 或 'auto')
        
    Returns:
        相对时间描述
    """
    return RelativeTimeFormatter.format(dt, reference, language)


def when(text: str, reference: Optional[datetime] = None) -> datetime:
    """
    when() 函数别名，用于解析自然语言时间
    
    Args:
        text: 时间表达式
        reference: 参考时间
        
    Returns:
        解析后的 datetime
    """
    return parse_time(text, reference)


def how_long(text: str) -> timedelta:
    """
    how_long() 函数别名，用于解析时长表达式
    
    Args:
        text: 时长表达式
        
    Returns:
        timedelta 对象
    """
    return parse_duration(text)
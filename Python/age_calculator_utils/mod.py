"""
Age Calculator Utilities - 年龄计算工具模块

提供完整的年龄计算功能，包括精确年龄、生日倒计时、年龄里程碑、
代际分类、年龄差计算等。零依赖，仅使用 Python 标准库。

Author: AllToolkit
Version: 1.0.0
"""

from datetime import datetime, date, timedelta
from typing import Optional, Union, List, Dict, Tuple
from enum import Enum


class Generation(Enum):
    """代际分类"""
    GREATEST = "最伟大一代"      # 1901-1927
    SILENT = "沉默的一代"        # 1928-1945
    BABY_BOOMER = "婴儿潮一代"   # 1946-1964
    GENERATION_X = "X世代"       # 1965-1980
    MILLENNIAL = "千禧一代"      # 1981-1996
    GENERATION_Z = "Z世代"       # 1997-2012
    GENERATION_ALPHA = "阿尔法世代"  # 2013-2025


class AgeCalculatorUtils:
    """年龄计算工具类"""
    
    @staticmethod
    def calculate_age(
        birth_date: Union[date, datetime, str],
        reference_date: Optional[Union[date, datetime, str]] = None,
        date_format: Optional[str] = None
    ) -> int:
        """
        计算年龄（周岁）
        
        Args:
            birth_date: 出生日期，支持 date/datetime/str 类型
            reference_date: 参考日期，默认为今天
            date_format: 字符串日期格式，默认 "%Y-%m-%d"
            
        Returns:
            int: 周岁年龄
            
        Example:
            >>> AgeCalculatorUtils.calculate_age("1990-05-15")
            33  # 假设今天是2024年
            >>> AgeCalculatorUtils.calculate_age("1990-05-15", "2024-05-14")
            33
            >>> AgeCalculatorUtils.calculate_age("1990-05-15", "2024-05-15")
            34
        """
        birth = AgeCalculatorUtils._parse_date(birth_date, date_format)
        ref = AgeCalculatorUtils._parse_date(reference_date, date_format) if reference_date else date.today()
        
        age = ref.year - birth.year
        if (ref.month, ref.day) < (birth.month, birth.day):
            age -= 1
        return age
    
    @staticmethod
    def calculate_exact_age(
        birth_date: Union[date, datetime, str],
        reference_date: Optional[Union[date, datetime, str]] = None,
        date_format: Optional[str] = None
    ) -> Tuple[int, int, int]:
        """
        计算精确年龄（年、月、日）
        
        Args:
            birth_date: 出生日期
            reference_date: 参考日期，默认为今天
            date_format: 字符串日期格式
            
        Returns:
            Tuple[int, int, int]: (年, 月, 日)
            
        Example:
            >>> AgeCalculatorUtils.calculate_exact_age("1990-03-15", "2024-05-20")
            (34, 2, 5)  # 34岁2个月5天
        """
        birth = AgeCalculatorUtils._parse_date(birth_date, date_format)
        ref = AgeCalculatorUtils._parse_date(reference_date, date_format) if reference_date else date.today()
        
        years = ref.year - birth.year
        months = ref.month - birth.month
        days = ref.day - birth.day
        
        if days < 0:
            months -= 1
            # 获取上个月的天数
            prev_month = ref.month - 1 if ref.month > 1 else 12
            prev_year = ref.year if ref.month > 1 else ref.year - 1
            days_in_prev_month = AgeCalculatorUtils._days_in_month(prev_month, prev_year)
            days += days_in_prev_month
        
        if months < 0:
            years -= 1
            months += 12
        
        return (years, months, days)
    
    @staticmethod
    def calculate_age_in_days(
        birth_date: Union[date, datetime, str],
        reference_date: Optional[Union[date, datetime, str]] = None,
        date_format: Optional[str] = None
    ) -> int:
        """
        计算年龄（天数）
        
        Returns:
            int: 存活天数
        """
        birth = AgeCalculatorUtils._parse_date(birth_date, date_format)
        ref = AgeCalculatorUtils._parse_date(reference_date, date_format) if reference_date else date.today()
        return (ref - birth).days
    
    @staticmethod
    def calculate_age_in_weeks(
        birth_date: Union[date, datetime, str],
        reference_date: Optional[Union[date, datetime, str]] = None,
        date_format: Optional[str] = None
    ) -> Tuple[int, int]:
        """
        计算年龄（周数和剩余天数）
        
        Returns:
            Tuple[int, int]: (完整周数, 剩余天数)
        """
        total_days = AgeCalculatorUtils.calculate_age_in_days(birth_date, reference_date, date_format)
        weeks = total_days // 7
        remaining_days = total_days % 7
        return (weeks, remaining_days)
    
    @staticmethod
    def calculate_age_in_months(
        birth_date: Union[date, datetime, str],
        reference_date: Optional[Union[date, datetime, str]] = None,
        date_format: Optional[str] = None
    ) -> int:
        """
        计算年龄（月数）
        
        Returns:
            int: 总月数
        """
        birth = AgeCalculatorUtils._parse_date(birth_date, date_format)
        ref = AgeCalculatorUtils._parse_date(reference_date, date_format) if reference_date else date.today()
        
        months = (ref.year - birth.year) * 12 + (ref.month - birth.month)
        if ref.day < birth.day:
            months -= 1
        return months
    
    @staticmethod
    def calculate_age_in_hours(
        birth_date: Union[date, datetime, str],
        reference_date: Optional[Union[date, datetime, str]] = None,
        date_format: Optional[str] = None
    ) -> int:
        """
        计算年龄（小时数）
        
        Returns:
            int: 总小时数
        """
        birth = AgeCalculatorUtils._parse_date(birth_date, date_format)
        ref = AgeCalculatorUtils._parse_date(reference_date, date_format) if reference_date else date.today()
        delta = ref - birth
        return delta.days * 24
    
    @staticmethod
    def days_until_birthday(
        birth_date: Union[date, datetime, str],
        reference_date: Optional[Union[date, datetime, str]] = None,
        date_format: Optional[str] = None
    ) -> int:
        """
        计算距离下一个生日的天数
        
        Returns:
            int: 距离生日的天数（0表示今天是生日）
        """
        birth = AgeCalculatorUtils._parse_date(birth_date, date_format)
        ref = AgeCalculatorUtils._parse_date(reference_date, date_format) if reference_date else date.today()
        
        # 今年的生日
        this_year_birthday = date(ref.year, birth.month, birth.day)
        
        # 如果今年的生日已过，计算明年的
        if this_year_birthday < ref:
            next_birthday = date(ref.year + 1, birth.month, birth.day)
        elif this_year_birthday > ref:
            next_birthday = this_year_birthday
        else:
            return 0  # 今天是生日
        
        return (next_birthday - ref).days
    
    @staticmethod
    def next_birthday_date(
        birth_date: Union[date, datetime, str],
        reference_date: Optional[Union[date, datetime, str]] = None,
        date_format: Optional[str] = None
    ) -> date:
        """
        获取下一个生日的日期
        
        Returns:
            date: 下一个生日的日期
        """
        birth = AgeCalculatorUtils._parse_date(birth_date, date_format)
        ref = AgeCalculatorUtils._parse_date(reference_date, date_format) if reference_date else date.today()
        
        this_year_birthday = date(ref.year, birth.month, birth.day)
        
        if this_year_birthday <= ref:
            return date(ref.year + 1, birth.month, birth.day)
        return this_year_birthday
    
    @staticmethod
    def get_birthday_info(
        birth_date: Union[date, datetime, str],
        reference_date: Optional[Union[date, datetime, str]] = None,
        date_format: Optional[str] = None
    ) -> Dict:
        """
        获取生日详细信息
        
        Returns:
            Dict: 包含各种生日相关信息的字典
        """
        birth = AgeCalculatorUtils._parse_date(birth_date, date_format)
        ref = AgeCalculatorUtils._parse_date(reference_date, date_format) if reference_date else date.today()
        
        age = AgeCalculatorUtils.calculate_age(birth, ref)
        exact_age = AgeCalculatorUtils.calculate_exact_age(birth, ref)
        days_until = AgeCalculatorUtils.days_until_birthday(birth, ref)
        next_bday = AgeCalculatorUtils.next_birthday_date(birth, ref)
        
        # 判断今天是否是生日
        is_birthday_today = (ref.month, ref.day) == (birth.month, birth.day)
        
        # 即将到来的生日年龄
        next_age = age + 1
        
        return {
            "birth_date": birth,
            "current_age": age,
            "exact_age": {
                "years": exact_age[0],
                "months": exact_age[1],
                "days": exact_age[2]
            },
            "is_birthday_today": is_birthday_today,
            "days_until_birthday": days_until,
            "next_birthday_date": next_bday,
            "next_birthday_age": next_age,
            "total_days_lived": AgeCalculatorUtils.calculate_age_in_days(birth, ref),
            "total_weeks_lived": AgeCalculatorUtils.calculate_age_in_weeks(birth, ref)[0]
        }
    
    @staticmethod
    def get_generation(
        birth_date: Union[date, datetime, str],
        date_format: Optional[str] = None
    ) -> Generation:
        """
        获取代际分类
        
        Returns:
            Generation: 代际枚举值
        """
        birth = AgeCalculatorUtils._parse_date(birth_date, date_format)
        year = birth.year
        
        if 1901 <= year <= 1927:
            return Generation.GREATEST
        elif 1928 <= year <= 1945:
            return Generation.SILENT
        elif 1946 <= year <= 1964:
            return Generation.BABY_BOOMER
        elif 1965 <= year <= 1980:
            return Generation.GENERATION_X
        elif 1981 <= year <= 1996:
            return Generation.MILLENNIAL
        elif 1997 <= year <= 2012:
            return Generation.GENERATION_Z
        else:  # 2013+
            return Generation.GENERATION_ALPHA
    
    @staticmethod
    def get_generation_info(
        birth_date: Union[date, datetime, str],
        date_format: Optional[str] = None
    ) -> Dict:
        """
        获取代际详细信息
        
        Returns:
            Dict: 包含代际名称、年份范围、特征描述等
        """
        generation = AgeCalculatorUtils.get_generation(birth_date, date_format)
        
        generation_info = {
            Generation.GREATEST: {
                "name": "最伟大一代",
                "english_name": "Greatest Generation",
                "year_range": (1901, 1927),
                "description": "经历了大萧条和二战，以坚韧、责任感和牺牲精神著称",
                "characteristics": ["坚韧", "责任感强", "忠诚", "节俭"]
            },
            Generation.SILENT: {
                "name": "沉默的一代",
                "english_name": "Silent Generation",
                "year_range": (1928, 1945),
                "description": "成长于二战和战后重建期，重视稳定和传统价值观",
                "characteristics": ["稳重", "保守", "勤奋", "尊重权威"]
            },
            Generation.BABY_BOOMER: {
                "name": "婴儿潮一代",
                "english_name": "Baby Boomer",
                "year_range": (1946, 1964),
                "description": "战后生育高峰期出生，经历了社会变革和经济繁荣",
                "characteristics": ["乐观", "工作狂", "理想主义", "重视教育"]
            },
            Generation.GENERATION_X: {
                "name": "X世代",
                "english_name": "Generation X",
                "year_range": (1965, 1980),
                "description": "成长于双职工家庭普遍化时期，独立自主",
                "characteristics": ["独立", "务实", "怀疑主义", "适应性强"]
            },
            Generation.MILLENNIAL: {
                "name": "千禧一代",
                "english_name": "Millennial (Gen Y)",
                "year_range": (1981, 1996),
                "description": "数字时代的第一批原住民，重视体验和意义",
                "characteristics": ["精通科技", "重视工作生活平衡", "开放包容", "追求意义"]
            },
            Generation.GENERATION_Z: {
                "name": "Z世代",
                "english_name": "Generation Z",
                "year_range": (1997, 2012),
                "description": "真正的数字原住民，从出生就接触互联网和智能手机",
                "characteristics": ["数字原生", "多元化", "社会意识强", "快速学习"]
            },
            Generation.GENERATION_ALPHA: {
                "name": "阿尔法世代",
                "english_name": "Generation Alpha",
                "year_range": (2013, 2025),
                "description": "完全在数字时代出生成长的一代，技术融入生活的方方面面",
                "characteristics": ["技术原住民", "全球化视野", "创造力强", "信息处理能力强"]
            }
        }
        
        info = generation_info[generation].copy()
        info["generation"] = generation
        return info
    
    @staticmethod
    def calculate_age_difference(
        date1: Union[date, datetime, str],
        date2: Union[date, datetime, str],
        date_format: Optional[str] = None
    ) -> Dict:
        """
        计算两个日期之间的年龄差异
        
        Returns:
            Dict: 包含各种单位的年龄差
        """
        d1 = AgeCalculatorUtils._parse_date(date1, date_format)
        d2 = AgeCalculatorUtils._parse_date(date2, date_format)
        
        if d1 > d2:
            older, younger = d2, d1
        else:
            older, younger = d1, d2
        
        delta_days = (younger - older).days
        
        years, months, days = AgeCalculatorUtils.calculate_exact_age(older, younger)
        
        return {
            "older_date": older,
            "younger_date": younger,
            "difference_days": delta_days,
            "difference_years": years,
            "difference_months": months,
            "difference_weeks": delta_days // 7,
            "difference_hours": delta_days * 24
        }
    
    @staticmethod
    def get_age_milestones(
        birth_date: Union[date, datetime, str],
        date_format: Optional[str] = None
    ) -> List[Dict]:
        """
        获取年龄里程碑（特殊生日、天数里程碑等）
        
        Returns:
            List[Dict]: 里程碑列表
        """
        birth = AgeCalculatorUtils._parse_date(birth_date, date_format)
        today = date.today()
        
        milestones = []
        
        # 重要年龄生日
        important_ages = [1, 7, 10, 16, 18, 20, 21, 25, 30, 40, 50, 60, 70, 80, 90, 100]
        for age in important_ages:
            milestone_date = date(birth.year + age, birth.month, birth.day)
            status = "已过" if milestone_date < today else ("今天" if milestone_date == today else "未到")
            milestones.append({
                "type": "年龄生日",
                "description": f"{age}岁生日",
                "date": milestone_date,
                "status": status,
                "age": age
            })
        
        # 天数里程碑
        day_milestones = [100, 1000, 5000, 10000, 15000, 20000, 25000, 30000, 36500]  # 36500天 = 100岁
        for days in day_milestones:
            milestone_date = birth + timedelta(days=days)
            status = "已过" if milestone_date < today else ("今天" if milestone_date == today else "未到")
            years_approx = days // 365
            milestones.append({
                "type": "天数里程碑",
                "description": f"出生{days}天（约{years_approx}岁）",
                "date": milestone_date,
                "status": status,
                "days": days
            })
        
        # 周数里程碑
        week_milestones = [100, 500, 1000, 2000, 5000]
        for weeks in week_milestones:
            milestone_date = birth + timedelta(weeks=weeks)
            status = "已过" if milestone_date < today else ("今天" if milestone_date == today else "未到")
            years_approx = weeks // 52
            milestones.append({
                "type": "周数里程碑",
                "description": f"出生{weeks}周（约{years_approx}岁）",
                "date": milestone_date,
                "status": status,
                "weeks": weeks
            })
        
        # 按日期排序
        milestones.sort(key=lambda x: x["date"])
        return milestones
    
    @staticmethod
    def get_next_milestone(
        birth_date: Union[date, datetime, str],
        date_format: Optional[str] = None
    ) -> Dict:
        """
        获取下一个里程碑
        
        Returns:
            Dict: 下一个里程碑信息
        """
        milestones = AgeCalculatorUtils.get_age_milestones(birth_date, date_format)
        today = date.today()
        
        for milestone in milestones:
            if milestone["date"] > today:
                days_until = (milestone["date"] - today).days
                milestone["days_until"] = days_until
                return milestone
        
        return None
    
    @staticmethod
    def calculate_age_at_date(
        birth_date: Union[date, datetime, str],
        target_date: Union[date, datetime, str],
        date_format: Optional[str] = None
    ) -> int:
        """
        计算在某个特定日期时的年龄
        
        这是 calculate_age 方法使用 target_date 作为 reference_date 的便捷别名
        """
        return AgeCalculatorUtils.calculate_age(birth_date, target_date, date_format)
    
    @staticmethod
    def get_chinese_zodiac(
        birth_date: Union[date, datetime, str],
        date_format: Optional[str] = None
    ) -> str:
        """
        获取中国生肖（简化版，基于农历年份简化为公历年份）
        
        Returns:
            str: 生肖名称
        """
        birth = AgeCalculatorUtils._parse_date(birth_date, date_format)
        zodiacs = ["鼠", "牛", "虎", "兔", "龙", "蛇", "马", "羊", "猴", "鸡", "狗", "猪"]
        # 2008年是鼠年
        index = (birth.year - 2008) % 12
        return zodiacs[index]
    
    @staticmethod
    def is_leap_year_baby(
        birth_date: Union[date, datetime, str],
        date_format: Optional[str] = None
    ) -> bool:
        """
        判断是否是闰年宝宝（2月29日出生）
        """
        birth = AgeCalculatorUtils._parse_date(birth_date, date_format)
        return birth.month == 2 and birth.day == 29
    
    @staticmethod
    def get_leap_year_birthday_info(
        birth_date: Union[date, datetime, str],
        reference_date: Optional[Union[date, datetime, str]] = None,
        date_format: Optional[str] = None
    ) -> Dict:
        """
        获取闰年生日宝宝的特殊信息
        
        Returns:
            Dict: 包含闰年生日相关信息
        """
        birth = AgeCalculatorUtils._parse_date(birth_date, date_format)
        ref = AgeCalculatorUtils._parse_date(reference_date, date_format) if reference_date else date.today()
        
        if not AgeCalculatorUtils.is_leap_year_baby(birth):
            return {"is_leap_year_baby": False}
        
        def is_leap_year(year):
            return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)
        
        # 找出已经过的真实生日
        real_birthdays = []
        for year in range(birth.year, ref.year + 1):
            if is_leap_year(year):
                real_birthdays.append(date(year, 2, 29))
        
        # 真实生日计数
        real_birthday_count = len([d for d in real_birthdays if d <= ref])
        
        # 下一个真实生日
        next_real_birthday = None
        for year in range(ref.year, ref.year + 5):
            if is_leap_year(year):
                candidate = date(year, 2, 29)
                if candidate > ref:
                    next_real_birthday = candidate
                    break
        
        return {
            "is_leap_year_baby": True,
            "real_birthday_count": real_birthday_count,
            "next_real_birthday": next_real_birthday,
            "celebrated_birthdays": real_birthday_count - 1  # 减去出生那年
        }
    
    @staticmethod
    def format_age(
        birth_date: Union[date, datetime, str],
        reference_date: Optional[Union[date, datetime, str]] = None,
        date_format: Optional[str] = None,
        format_type: str = "full"
    ) -> str:
        """
        格式化年龄显示
        
        Args:
            birth_date: 出生日期
            reference_date: 参考日期
            date_format: 日期格式
            format_type: 格式类型 ("full", "simple", "days", "weeks")
            
        Returns:
            str: 格式化的年龄字符串
        """
        if format_type == "full":
            years, months, days = AgeCalculatorUtils.calculate_exact_age(birth_date, reference_date, date_format)
            return f"{years}岁{months}个月{days}天"
        elif format_type == "simple":
            age = AgeCalculatorUtils.calculate_age(birth_date, reference_date, date_format)
            return f"{age}岁"
        elif format_type == "days":
            days = AgeCalculatorUtils.calculate_age_in_days(birth_date, reference_date, date_format)
            return f"{days}天"
        elif format_type == "weeks":
            weeks, days = AgeCalculatorUtils.calculate_age_in_weeks(birth_date, reference_date, date_format)
            return f"{weeks}周{days}天"
        else:
            age = AgeCalculatorUtils.calculate_age(birth_date, reference_date, date_format)
            return f"{age}岁"
    
    @staticmethod
    def _parse_date(
        date_input: Union[date, datetime, str, None],
        date_format: Optional[str] = None
    ) -> date:
        """解析各种格式的日期输入"""
        if date_input is None:
            return date.today()
        
        if isinstance(date_input, date):
            return date_input
        
        if isinstance(date_input, datetime):
            return date_input.date()
        
        if isinstance(date_input, str):
            fmt = date_format or "%Y-%m-%d"
            try:
                return datetime.strptime(date_input, fmt).date()
            except ValueError:
                # 尝试其他常见格式
                for alt_fmt in ["%Y/%m/%d", "%d-%m-%Y", "%d/%m/%Y", "%Y%m%d"]:
                    try:
                        return datetime.strptime(date_input, alt_fmt).date()
                    except ValueError:
                        continue
                raise ValueError(f"无法解析日期: {date_input}")
        
        raise TypeError(f"不支持的日期类型: {type(date_input)}")
    
    @staticmethod
    def _days_in_month(month: int, year: int) -> int:
        """获取某月的天数"""
        if month in [1, 3, 5, 7, 8, 10, 12]:
            return 31
        elif month in [4, 6, 9, 11]:
            return 30
        else:  # February
            if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
                return 29
            return 28


# 便捷函数
def calculate_age(birth_date: Union[date, datetime, str], 
                  reference_date: Optional[Union[date, datetime, str]] = None,
                  date_format: Optional[str] = None) -> int:
    """计算年龄（便捷函数）"""
    return AgeCalculatorUtils.calculate_age(birth_date, reference_date, date_format)


def calculate_exact_age(birth_date: Union[date, datetime, str],
                        reference_date: Optional[Union[date, datetime, str]] = None,
                        date_format: Optional[str] = None) -> Tuple[int, int, int]:
    """计算精确年龄（便捷函数）"""
    return AgeCalculatorUtils.calculate_exact_age(birth_date, reference_date, date_format)


def days_until_birthday(birth_date: Union[date, datetime, str],
                        reference_date: Optional[Union[date, datetime, str]] = None,
                        date_format: Optional[str] = None) -> int:
    """计算距离生日的天数（便捷函数）"""
    return AgeCalculatorUtils.days_until_birthday(birth_date, reference_date, date_format)


def get_generation(birth_date: Union[date, datetime, str],
                   date_format: Optional[str] = None) -> Generation:
    """获取代际分类（便捷函数）"""
    return AgeCalculatorUtils.get_generation(birth_date, date_format)


def format_age(birth_date: Union[date, datetime, str],
               reference_date: Optional[Union[date, datetime, str]] = None,
               date_format: Optional[str] = None,
               format_type: str = "full") -> str:
    """格式化年龄显示（便捷函数）"""
    return AgeCalculatorUtils.format_age(birth_date, reference_date, date_format, format_type)


if __name__ == "__main__":
    # 简单演示
    print("=== 年龄计算工具演示 ===\n")
    
    # 计算年龄
    birth = "1990-05-15"
    print(f"出生日期: {birth}")
    print(f"当前年龄: {calculate_age(birth)}岁")
    print(f"精确年龄: {format_age(birth)}")
    print(f"距离下次生日: {days_until_birthday(birth)}天")
    print(f"代际: {get_generation(birth).value}")
    print()
    
    # 年龄里程碑
    print("即将到来的里程碑:")
    milestone = AgeCalculatorUtils.get_next_milestone(birth)
    if milestone:
        print(f"  {milestone['description']} - {milestone['days_until']}天后")
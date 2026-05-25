"""
节气工具模块 (Jieqi Utils)

提供二十四节气计算功能，包括：
- 计算任意年份的节气日期
- 获取当前节气和下一个节气
- 节气详细信息查询
- 节气养生建议
- 节气传统习俗

纯 Python 实现，零外部依赖，使用近似公式计算节气日期。
"""

import math
from datetime import datetime, date, timedelta
from typing import Tuple, List, Dict, Optional, NamedTuple


class JieqiInfo(NamedTuple):
    """节气信息"""
    name: str           # 节气名称
    date: date          # 节气日期
    index: int          # 节气序号（0-23）
    is_jieqi: bool      # 是否为"节气"（每月前一个）
    season: str         # 所属季节
    month: int          # 对应农历月份（近似）
    description: str    # 节气含义描述


# 二十四节气数据（按节气序号排列）
JIEQI_DATA: Dict[int, Dict[str, str]] = {
    0: {"name": "小寒", "season": "冬", "month": 12, "description": "气候开始寒冷，但还未到最冷"},
    1: {"name": "大寒", "season": "冬", "month": 12, "description": "一年中最冷的时期"},
    2: {"name": "立春", "season": "春", "month": 1, "description": "春季开始，万物复苏"},
    3: {"name": "雨水", "season": "春", "month": 1, "description": "降雨开始，雨量渐增"},
    4: {"name": "惊蛰", "season": "春", "month": 2, "description": "春雷乍动，惊醒蛰伏昆虫"},
    5: {"name": "春分", "season": "春", "month": 2, "description": "昼夜平分，春季过半"},
    6: {"name": "清明", "season": "春", "month": 3, "description": "天气清朗，草木繁茂"},
    7: {"name": "谷雨", "season": "春", "month": 3, "description": "雨水增多，利于谷物生长"},
    8: {"name": "立夏", "season": "夏", "month": 4, "description": "夏季开始，万物生长旺盛"},
    9: {"name": "小满", "season": "夏", "month": 4, "description": "麦类等作物籽粒开始饱满"},
    10: {"name": "芒种", "season": "夏", "month": 5, "description": "麦类等有芒作物成熟"},
    11: {"name": "夏至", "season": "夏", "month": 5, "description": "太阳直射北回归线，白昼最长"},
    12: {"name": "小暑", "season": "夏", "month": 6, "description": "气候开始炎热，但未到最热"},
    13: {"name": "大暑", "season": "夏", "month": 6, "description": "一年中最热的时期"},
    14: {"name": "立秋", "season": "秋", "month": 7, "description": "秋季开始，暑去凉来"},
    15: {"name": "处暑", "season": "秋", "month": 7, "description": "暑气结束，天气转凉"},
    16: {"name": "白露", "season": "秋", "month": 8, "description": "天气转凉，出现露水"},
    17: {"name": "秋分", "season": "秋", "month": 8, "description": "昼夜平分，秋季过半"},
    18: {"name": "寒露", "season": "秋", "month": 9, "description": "露水增多，天气更凉"},
    19: {"name": "霜降", "season": "秋", "month": 9, "description": "开始降霜，天气渐冷"},
    20: {"name": "立冬", "season": "冬", "month": 10, "description": "冬季开始，万物收藏"},
    21: {"name": "小雪", "season": "冬", "month": 10, "description": "开始降雪，雪量较小"},
    22: {"name": "大雪", "season": "冬", "month": 11, "description": "降雪量增多，地面积雪"},
    23: {"name": "冬至", "season": "冬", "month": 11, "description": "太阳直射南回归线，白昼最短"},
}


# 节气养生建议
JIEQI_HEALTH_ADVICE: Dict[str, List[str]] = {
    "小寒": ["注意保暖，预防感冒", "适当进补，增强体质", "早睡晚起，养精蓄锐"],
    "大寒": ["继续保暖，避免寒邪", "饮食温补，补益肝肾", "适度运动，增强抵抗力"],
    "立春": ["养肝护肝，调畅情志", "饮食清淡，多吃蔬菜", "早起早睡，舒展身体"],
    "雨水": ["健脾祛湿，调养脾胃", "少吃酸食，多吃甜食", "注意保暖，防止湿气"],
    "惊蛰": ["养肝护脾，调和情志", "多吃时令蔬菜", "早睡早起，运动适度"],
    "春分": ["阴阳平衡，调和气血", "饮食均衡，营养全面", "春游踏青，舒畅心情"],
    "清明": ["养肝健脾，疏肝解郁", "多吃绿色蔬菜", "户外运动，呼吸新鲜空气"],
    "谷雨": ["健脾除湿，调理脾胃", "多吃山药、薏米", "预防过敏，注意饮食"],
    "立夏": ["养心安神，调理心火", "饮食清淡，多吃水果", "适度午休，避免劳累"],
    "小满": ["清热祛湿，调理脾胃", "多吃清淡食物", "注意防暑，避免出汗过多"],
    "芒种": ["健脾养胃，清热利湿", "多吃瓜果蔬菜", "早睡早起，精神饱满"],
    "夏至": ["养心安神，清热消暑", "饮食清淡，多喝水", "避免暴晒，适度午休"],
    "小暑": ["清热解暑，养心安神", "多吃绿豆、苦瓜", "避免中暑，减少户外"],
    "大暑": ["防暑降温，清热解毒", "多吃清凉食物", "避免高温时段外出"],
    "立秋": ["滋阴润燥，养肺护肺", "多吃梨、百合", "早睡早起，适量运动"],
    "处暑": ["润燥养肺，调理肠胃", "多吃润燥食物", "保持心情舒畅"],
    "白露": ["养肺润燥，预防秋燥", "多吃润肺食物", "注意保暖，早晚添衣"],
    "秋分": ["阴阳平衡，养肺润燥", "饮食均衡，营养全面", "户外运动，感受秋色"],
    "寒露": ["养肺润燥，防寒保暖", "多吃滋阴食物", "早睡早起，避免感冒"],
    "霜降": ["保暖防寒，调理肠胃", "多吃温补食物", "适度运动，增强体质"],
    "立冬": ["补肾养肾，藏精养神", "多吃黑色食物", "早睡晚起，减少户外"],
    "小雪": ["养肾防寒，调理肠胃", "饮食温补，多吃坚果", "注意保暖，预防感冒"],
    "大雪": ["补肾养阳，温补气血", "多吃羊肉、牛肉", "早睡晚起，养精蓄锐"],
    "冬至": ["养肾补阳，藏精固本", "饮食温补，多吃热食", "早睡晚起，避免劳累"],
}


# 节气传统习俗
JIEQI_TRADITIONS: Dict[str, List[str]] = {
    "小寒": ["腊八节喝腊八粥", "腌制腊味", "准备年货"],
    "大寒": ["扫尘洁物", "准备过年", "祭灶神"],
    "立春": ["吃春饼", "踏春赏花", "打春牛"],
    "雨水": ["回娘家", "拉保保", "接寿"],
    "惊蛰": ["吃梨", "打小人", "祭白虎"],
    "春分": ["竖蛋游戏", "踏青放风筝", "吃春菜"],
    "清明": ["扫墓祭祖", "踏青郊游", "吃青团"],
    "谷雨": ["赏牡丹", "喝谷雨茶", "祭祀仓颉"],
    "立夏": ["尝三新", "吃蛋", "称体重"],
    "小满": ["祭三神", "吃苦菜", "抢水"],
    "芒种": ["送花神", "煮梅", "安苗"],
    "夏至": ["吃面条", "祭神祀祖", "消夏避伏"],
    "小暑": ["吃饺子", "晒书画", "吃绿豆芽"],
    "大暑": ["晒伏姜", "喝伏茶", "烧伏香"],
    "立秋": ["贴秋膘", "啃秋瓜", "秋收忙"],
    "处暑": ["吃鸭子", "放河灯", "开渔节"],
    "白露": ["收清露", "喝白露茶", "吃龙眼"],
    "秋分": ["祭月", "吃秋菜", "送秋牛"],
    "寒露": ["登高赏菊", "饮菊花酒", "吃芝麻"],
    "霜降": ["赏菊花", "吃柿子", "登高远眺"],
    "立冬": ["吃饺子", "贺冬", "祭祖"],
    "小雪": ["腌腊肉", "吃糍粑", "晒鱼干"],
    "大雪": ["腌肉", "观赏封河", "进补"],
    "冬至": ["吃饺子/汤圆", "祭祖", "数九开始"],
}


# 节气名称列表（按节气序号排列）
JIEQI_NAMES: List[str] = [data["name"] for data in JIEQI_DATA.values()]


# 节气日期基准（基于寿星万年历的近似公式）
# 每个节气在一年中的基准天数（从1月0日开始）
# 使用天文算法计算节气日期的简化版本
JIEQI_BASE_DAYS: Dict[int, float] = {
    0: 5.5,     # 小寒约在1月5-6日
    1: 20.5,    # 大寒约在1月20-21日
    2: 34.5,    # 立春约在2月3-4日（从1月0日起第34天）
    3: 49.5,    # 雨水约在2月18-19日
    4: 64.5,    # 惊蛰约在3月5-6日
    5: 79.5,    # 春分约在3月20-21日
    6: 94.5,    # 清明约在4月4-5日
    7: 109.5,   # 谷雨约在4月19-20日
    8: 124.5,   # 立夏约在5月5-6日
    9: 140.5,   # 小满约在5月20-21日
    10: 155.5,  # 芒种约在6月5-6日
    11: 171.5,  # 夏至约在6月20-21日
    12: 186.5,  # 小暑约在7月6-7日
    13: 202.5,  # 大暑约在7月22-23日
    14: 217.5,  # 立秋约在8月6-8日
    15: 233.5,  # 处暑约在8月22-23日
    16: 248.5,  # 白露约在9月7-8日
    17: 263.5,  # 秋分约在9月22-23日
    18: 278.5,  # 寒露约在10月8-9日
    19: 293.5,  # 霜降约在10月23-24日
    20: 308.5,  # 立冬约在11月7-8日
    21: 323.5,  # 小雪约在11月22-23日
    22: 338.5,  # 大雪约在12月6-7日
    23: 355.5,  # 冬至约在12月21-22日
}


def _calculate_jieqi_day(year: int, jieqi_index: int) -> int:
    """
    计算节气在一年中的天数（从1月0日开始）
    
    使用寿星万年历的近似公式，考虑年份修正
    
    Args:
        year: 年份
        jieqi_index: 节气序号（0-23）
    
    Returns:
        天数（从1月0日开始）
    """
    # 基准天数
    base_day = JIEQI_BASE_DAYS[jieqi_index]
    
    # 年份修正（考虑地球公转周期变化）
    # 使用简化公式：节气日期每年约有0.2422天的变化
    # 每4年有一个闰年修正
    
    # C值（世纪数）
    c = (year - 1) // 100
    
    # 年份修正系数（基于寿星公式）
    # 不同节气有不同的修正公式
    
    # 简化的年份修正（考虑闰年和回归年变化）
    # 回归年约365.2422天，公历年365或366天
    year_offset = (year - 2000) * 0.2422
    
    # 闰年修正（每4年多一天，需要回退）
    leap_count = (year - 2000) // 4
    
    # 世纪修正（400年周期）
    century_skip = (year - 2000) // 400
    century_add = (year - 2000) // 100 - century_skip
    
    # 总修正
    correction = year_offset - leap_count + century_skip - century_add
    
    # 节气特定修正
    # 根据节气类型调整
    if jieqi_index in [0, 1]:  # 小寒大寒
        correction -= 0.5
    elif jieqi_index in [11]:  # 夏至
        correction += 0.2
    elif jieqi_index in [23]:  # 冬至
        correction -= 0.3
    
    # 计算总天数
    total_day = base_day + correction
    
    return int(round(total_day))


def _day_to_date(year: int, day_number: int) -> date:
    """
    将天数转换为日期
    
    Args:
        year: 年份
        day_number: 天数（从1月0日开始，即1月1日为第1天）
    
    Returns:
        对应的日期
    """
    # 使用Python的datetime来转换
    # 1月0日作为基准（实际上是上一年的12月31日）
    jan0 = date(year, 1, 1) - timedelta(days=1)
    
    result = jan0 + timedelta(days=day_number)
    
    return result


def _find_jieqi_date(year: int, jieqi_index: int) -> date:
    """
    计算指定年份指定节气的日期
    
    Args:
        year: 年份
        jieqi_index: 节气序号（0-23）
    
    Returns:
        节气日期
    """
    day_number = _calculate_jieqi_day(year, jieqi_index)
    return _day_to_date(year, day_number)


def get_jieqi_date(year: int, jieqi_name: str) -> Optional[date]:
    """
    获取指定年份指定节气的日期
    
    Args:
        year: 年份
        jieqi_name: 节气名称
    
    Returns:
        节气日期，如果节气名称无效则返回 None
    
    Example:
        >>> get_jieqi_date(2024, "立春")
        datetime.date(2024, 2, 4)
        >>> get_jieqi_date(2024, "冬至")
        datetime.date(2024, 12, 21)
    """
    if jieqi_name not in JIEQI_NAMES:
        return None
    
    jieqi_index = JIEQI_NAMES.index(jieqi_name)
    return _find_jieqi_date(year, jieqi_index)


def get_year_jieqi_list(year: int) -> List[JieqiInfo]:
    """
    获取指定年份所有节气列表（从小寒开始到冬至）
    
    Args:
        year: 年份
    
    Returns:
        节气信息列表（从小寒开始，按节气顺序）
    
    Example:
        >>> jieqi_list = get_year_jieqi_list(2024)
        >>> len(jieqi_list)
        24
        >>> jieqi_list[0].name
        '小寒'
        >>> jieqi_list[2].name
        '立春'
    """
    result = []
    
    for i in range(24):
        jieqi_date = _find_jieqi_date(year, i)
        data = JIEQI_DATA[i]
        
        info = JieqiInfo(
            name=data["name"],
            date=jieqi_date,
            index=i,
            is_jieqi=(i % 2 == 0),  # 节气（每月第一个）
            season=data["season"],
            month=data["month"],
            description=data["description"]
        )
        result.append(info)
    
    return result


def get_current_jieqi(target_date: Optional[date] = None) -> Optional[JieqiInfo]:
    """
    获取当前（或指定日期）所处的节气
    
    Args:
        target_date: 目标日期，默认为今天
    
    Returns:
        当前节气信息
    
    Example:
        >>> get_current_jieqi(date(2024, 2, 10))
        JieqiInfo(name='立春', date=datetime.date(2024, 2, 4), ...)
    """
    if target_date is None:
        target_date = date.today()
    
    year = target_date.year
    
    # 获取该年份所有节气
    jieqi_list = get_year_jieqi_list(year)
    
    # 找到当前所处的节气
    current_jieqi = None
    
    for info in jieqi_list:
        if info.date <= target_date:
            current_jieqi = info
        else:
            break
    
    # 如果在当年小寒之前，需要看上一年的节气
    if current_jieqi is None:
        prev_year_list = get_year_jieqi_list(year - 1)
        # 从上一年的冬至开始查找（冬至在12月）
        for info in reversed(prev_year_list):
            if info.date <= target_date:
                current_jieqi = info
                break
    
    return current_jieqi


def get_next_jieqi(target_date: Optional[date] = None) -> Optional[JieqiInfo]:
    """
    获取下一个节气
    
    Args:
        target_date: 目标日期，默认为今天
    
    Returns:
        下一个节气信息
    
    Example:
        >>> get_next_jieqi(date(2024, 2, 1))
        JieqiInfo(name='立春', date=datetime.date(2024, 2, 4), ...)
    """
    if target_date is None:
        target_date = date.today()
    
    year = target_date.year
    jieqi_list = get_year_jieqi_list(year)
    
    # 找下一个节气
    for info in jieqi_list:
        if info.date > target_date:
            return info
    
    # 如果当年已经过了冬至，返回下一年的小寒
    next_year_list = get_year_jieqi_list(year + 1)
    return next_year_list[0]


def get_days_to_next_jieqi(target_date: Optional[date] = None) -> int:
    """
    计算距离下一个节气的天数
    
    Args:
        target_date: 目标日期，默认为今天
    
    Returns:
        天数
    
    Example:
        >>> get_days_to_next_jieqi(date(2024, 2, 1))
        3  # 距离立春还有3天
    """
    next_jieqi = get_next_jieqi(target_date)
    if next_jieqi is None:
        return -1
    
    if target_date is None:
        target_date = date.today()
    
    delta = next_jieqi.date - target_date
    return delta.days


def get_jieqi_health_advice(jieqi_name: str) -> Optional[List[str]]:
    """
    获取节气养生建议
    
    Args:
        jieqi_name: 节气名称
    
    Returns:
        养生建议列表
    
    Example:
        >>> get_jieqi_health_advice("立春")
        ['养肝护肝，调畅情志', '饮食清淡，多吃蔬菜', '早起早睡，舒展身体']
    """
    return JIEQI_HEALTH_ADVICE.get(jieqi_name)


def get_jieqi_traditions(jieqi_name: str) -> Optional[List[str]]:
    """
    获取节气传统习俗
    
    Args:
        jieqi_name: 节气名称
    
    Returns:
        传统习俗列表
    
    Example:
        >>> get_jieqi_traditions("清明")
        ['扫墓祭祖', '踏青郊游', '吃青团']
    """
    return JIEQI_TRADITIONS.get(jieqi_name)


def get_jieqi_info(jieqi_name: str) -> Optional[Dict[str, any]]:
    """
    获取节气详细信息
    
    Args:
        jieqi_name: 节气名称
    
    Returns:
        节气详细信息字典
    
    Example:
        >>> info = get_jieqi_info("立春")
        >>> info['season']
        '春'
        >>> info['description']
        '春季开始，万物复苏'
    """
    if jieqi_name not in JIEQI_NAMES:
        return None
    
    index = JIEQI_NAMES.index(jieqi_name)
    data = JIEQI_DATA[index]
    
    return {
        "name": data["name"],
        "index": index,
        "season": data["season"],
        "month": data["month"],
        "description": data["description"],
        "is_jieqi": index % 2 == 0,
        "health_advice": JIEQI_HEALTH_ADVICE.get(jieqi_name, []),
        "traditions": JIEQI_TRADITIONS.get(jieqi_name, [])
    }


def get_season_jieqi(season: str) -> List[str]:
    """
    获取指定季节的所有节气
    
    Args:
        season: 季节名称（春/夏/秋/冬）
    
    Returns:
        节气名称列表
    
    Example:
        >>> get_season_jieqi("春")
        ['立春', '雨水', '惊蛰', '春分', '清明', '谷雨']
    """
    result = []
    for i, data in JIEQI_DATA.items():
        if data["season"] == season:
            result.append(data["name"])
    return result


def is_jieqi_day(target_date: Optional[date] = None) -> bool:
    """
    判断指定日期是否为节气日
    
    Args:
        target_date: 目标日期，默认为今天
    
    Returns:
        是否为节气日
    
    Example:
        >>> is_jieqi_day(date(2024, 2, 4))
        True  # 立春
    """
    if target_date is None:
        target_date = date.today()
    
    year = target_date.year
    
    # 检查当年节气
    jieqi_list = get_year_jieqi_list(year)
    for info in jieqi_list:
        if info.date == target_date:
            return True
    
    # 检查上一年的节气（可能在上一年12月的小寒大寒）
    prev_list = get_year_jieqi_list(year - 1)
    for info in prev_list:
        if info.date == target_date:
            return True
    
    return False


def get_jieqi_by_month(month: int) -> List[str]:
    """
    获取指定月份对应的节气
    
    Args:
        month: 月份（1-12）
    
    Returns:
        节气名称列表（通常两个节气）
    
    Example:
        >>> get_jieqi_by_month(2)
        ['立春', '雨水']
        >>> get_jieqi_by_month(6)
        ['芒种', '夏至']
    """
    # 节气序号与月份的对应关系：
    # month 1: 小寒(0)大寒(1)
    # month 2: 立春(2)雨水(3)
    # month 3: 惊蛰(4)春分(5)
    # ...依此类推
    
    index1 = (month - 1) * 2
    index2 = index1 + 1
    
    result = []
    for idx in [index1, index2]:
        if idx < 24:
            result.append(JIEQI_DATA[idx]["name"])
    
    return result


def format_jieqi_report(jieqi_info: JieqiInfo) -> str:
    """
    格式化节气报告
    
    Args:
        jieqi_info: 节气信息
    
    Returns:
        格式化的节气报告字符串
    
    Example:
        >>> info = get_current_jieqi(date(2024, 2, 10))
        >>> format_jieqi_report(info)
        '【立春】春季开始，万物复苏...'
    """
    lines = []
    lines.append(f"【{jieqi_info.name}】")
    lines.append(f"日期：{jieqi_info.date.strftime('%Y年%m月%d日')}")
    lines.append(f"季节：{jieqi_info.season}")
    lines.append(f"含义：{jieqi_info.description}")
    
    # 养生建议
    advice = get_jieqi_health_advice(jieqi_info.name)
    if advice:
        lines.append("养生建议：")
        for a in advice:
            lines.append(f"  • {a}")
    
    # 传统习俗
    traditions = get_jieqi_traditions(jieqi_info.name)
    if traditions:
        lines.append("传统习俗：")
        for t in traditions:
            lines.append(f"  • {t}")
    
    return "\n".join(lines)


def get_jieqi_name_list() -> List[str]:
    """
    获取二十四节气名称列表
    
    Returns:
        节气名称列表（从小寒开始）
    
    Example:
        >>> get_jieqi_name_list()
        ['小寒', '大寒', '立春', '雨水', ..., '冬至']
    """
    return JIEQI_NAMES.copy()


def get_current_season(target_date: Optional[date] = None) -> str:
    """
    获取当前季节
    
    Args:
        target_date: 目标日期，默认为今天
    
    Returns:
        季节名称
    
    Example:
        >>> get_current_season(date(2024, 2, 10))
        '春'
    """
    current = get_current_jieqi(target_date)
    if current:
        return current.season
    return "冬"  # 默认冬季


def get_quarter_jieqi() -> Dict[str, str]:
    """
    获取四时八节（四个季节的开始和中分点）
    
    Returns:
        四时八节字典
    
    Example:
        >>> get_quarter_jieqi()
        {'立春': '春之始', '春分': '春之半', '立夏': '夏之始', ...}
    """
    return {
        "立春": "春之始",
        "春分": "春之半",
        "立夏": "夏之始",
        "夏至": "夏之半",
        "立秋": "秋之始",
        "秋分": "秋之半",
        "立冬": "冬之始",
        "冬至": "冬之半"
    }


def search_jieqi(keyword: str) -> List[str]:
    """
    搜索节气（根据关键词）
    
    Args:
        keyword: 搜索关键词
    
    Returns:
        匹配的节气名称列表
    
    Example:
        >>> search_jieqi("春")
        ['立春', '春分']
    """
    result = []
    for name in JIEQI_NAMES:
        if keyword.lower() in name.lower():
            result.append(name)
    return result


# 导出所有公共函数和类
__all__ = [
    'JieqiInfo',
    'get_jieqi_date',
    'get_year_jieqi_list',
    'get_current_jieqi',
    'get_next_jieqi',
    'get_days_to_next_jieqi',
    'get_jieqi_health_advice',
    'get_jieqi_traditions',
    'get_jieqi_info',
    'get_season_jieqi',
    'is_jieqi_day',
    'get_jieqi_by_month',
    'format_jieqi_report',
    'get_jieqi_name_list',
    'get_current_season',
    'get_quarter_jieqi',
    'search_jieqi',
    'JIEQI_NAMES',
    'JIEQI_DATA',
]
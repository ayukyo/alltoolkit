"""
茶道工具模块 (Tea Utils)

提供泡茶计时、茶知识库、水温推荐、冲泡次数建议等功能。
零外部依赖，纯 Python 标准库实现。

功能：
- 茶叶数据库：包含常见茶类的特性、冲泡参数
- 水温推荐：根据茶叶种类推荐最佳冲泡水温
- 冲泡计时：倒计时器，支持多泡
- 浸泡时间计算：根据茶叶种类和泡数计算浸泡时间
- 茶知识：茶类介绍、功效、产地等
- 茶具推荐：不同茶类适合的茶具
"""

from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional, Tuple
import time


class TeaCategory(Enum):
    """茶叶类别枚举"""
    GREEN = "绿茶"          # 不发酵
    WHITE = "白茶"          # 轻微发酵
    YELLOW = "黄茶"          # 轻发酵
    OOLONG = "乌龙茶"        # 半发酵
    BLACK = "红茶"          # 全发酵
    DARK = "黑茶"          # 后发酵
    PUERH_RAW = "生普"       # 生普洱
    PUERH_RIPE = "熟普"      # 熟普洱
    HERBAL = "花草茶"        # 花草茶
    MATCHA = "抹茶"          # 抹茶


@dataclass
class TeaInfo:
    """茶叶信息数据类"""
    name: str                      # 茶叶名称
    category: TeaCategory           # 茶叶类别
    origin: str                     # 产地
    water_temp_min: int             # 最低水温(°C)
    water_temp_max: int             # 最高水温(°C)
    first_steep_sec: int            # 第一泡时间(秒)
    steep_increment: int            # 每泡增加时间(秒)
    max_steeps: int                 # 最大冲泡次数
    recommended_teaware: List[str]  # 推荐茶具
    flavor_notes: List[str]         # 风味特点
    health_benefits: List[str]      # 健康功效
    caffeine_level: str             # 咖啡因含量: low/medium/high
    description: str                # 描述


# ==================== 茶叶数据库 ====================

TEA_DATABASE: Dict[str, TeaInfo] = {
    # 绿茶类
    "龙井": TeaInfo(
        name="龙井",
        category=TeaCategory.GREEN,
        origin="浙江杭州",
        water_temp_min=75,
        water_temp_max=80,
        first_steep_sec=30,
        steep_increment=5,
        max_steeps=4,
        recommended_teaware=["玻璃杯", "盖碗"],
        flavor_notes=["豆香", "兰花香", "甘甜"],
        health_benefits=["抗氧化", "降血脂", "提神醒脑"],
        caffeine_level="medium",
        description="中国十大名茶之首，以「色绿、香郁、味甘、形美」四绝著称。"
    ),
    "碧螺春": TeaInfo(
        name="碧螺春",
        category=TeaCategory.GREEN,
        origin="江苏苏州",
        water_temp_min=70,
        water_temp_max=75,
        first_steep_sec=25,
        steep_increment=5,
        max_steeps=4,
        recommended_teaware=["玻璃杯", "盖碗"],
        flavor_notes=["花果香", "蜜香", "鲜爽"],
        health_benefits=["抗氧化", "清热解毒", "养颜"],
        caffeine_level="medium",
        description="产于太湖洞庭山，以形美、色艳、香浓、味醇「四绝」闻名。"
    ),
    "毛峰": TeaInfo(
        name="毛峰",
        category=TeaCategory.GREEN,
        origin="安徽黄山",
        water_temp_min=80,
        water_temp_max=85,
        first_steep_sec=35,
        steep_increment=5,
        max_steeps=4,
        recommended_teaware=["玻璃杯", "盖碗"],
        flavor_notes=["兰花香", "板栗香", "甘醇"],
        health_benefits=["抗氧化", "清热降火", "利尿"],
        caffeine_level="medium",
        description="黄山毛峰，中国历史名茶，清香高长，滋味鲜爽。"
    ),
    "信阳毛尖": TeaInfo(
        name="信阳毛尖",
        category=TeaCategory.GREEN,
        origin="河南信阳",
        water_temp_min=80,
        water_temp_max=85,
        first_steep_sec=30,
        steep_increment=5,
        max_steeps=4,
        recommended_teaware=["玻璃杯", "盖碗"],
        flavor_notes=["清香", "板栗香", "鲜醇"],
        health_benefits=["抗氧化", "降血压", "清心明目"],
        caffeine_level="medium",
        description="河南名茶，以「细、圆、光、直、多白毫」著称。"
    ),
    
    # 白茶类
    "白毫银针": TeaInfo(
        name="白毫银针",
        category=TeaCategory.WHITE,
        origin="福建福鼎/政和",
        water_temp_min=85,
        water_temp_max=90,
        first_steep_sec=40,
        steep_increment=10,
        max_steeps=6,
        recommended_teaware=["盖碗", "玻璃杯"],
        flavor_notes=["毫香", "花香", "清甜"],
        health_benefits=["抗氧化", "降火", "养颜"],
        caffeine_level="low",
        description="白茶中的珍品，满披白毫，如银似雪。"
    ),
    "白牡丹": TeaInfo(
        name="白牡丹",
        category=TeaCategory.WHITE,
        origin="福建福鼎/政和",
        water_temp_min=85,
        water_temp_max=90,
        first_steep_sec=35,
        steep_increment=8,
        max_steeps=6,
        recommended_teaware=["盖碗", "玻璃杯"],
        flavor_notes=["花香", "毫香", "醇厚"],
        health_benefits=["抗氧化", "清热解毒", "护肝"],
        caffeine_level="low",
        description="以一芽一叶或一芽二叶为原料，形似花朵。"
    ),
    
    # 黄茶类
    "君山银针": TeaInfo(
        name="君山银针",
        category=TeaCategory.YELLOW,
        origin="湖南岳阳",
        water_temp_min=80,
        water_temp_max=85,
        first_steep_sec=40,
        steep_increment=8,
        max_steeps=5,
        recommended_teaware=["玻璃杯", "盖碗"],
        flavor_notes=["甘醇", "甜香", "鲜爽"],
        health_benefits=["助消化", "清热", "养胃"],
        caffeine_level="medium",
        description="黄茶珍品，产于洞庭湖君山岛，「金镶玉色」。"
    ),
    
    # 乌龙茶类
    "铁观音": TeaInfo(
        name="铁观音",
        category=TeaCategory.OOLONG,
        origin="福建安溪",
        water_temp_min=95,
        water_temp_max=100,
        first_steep_sec=30,
        steep_increment=5,
        max_steeps=8,
        recommended_teaware=["紫砂壶", "盖碗"],
        flavor_notes=["兰花香", "音韵", "回甘"],
        health_benefits=["减肥", "降血脂", "抗衰老"],
        caffeine_level="medium",
        description="闽南乌龙代表，独具「观音韵」，七泡有余香。"
    ),
    "大红袍": TeaInfo(
        name="大红袍",
        category=TeaCategory.OOLONG,
        origin="福建武夷山",
        water_temp_min=95,
        water_temp_max=100,
        first_steep_sec=25,
        steep_increment=5,
        max_steeps=10,
        recommended_teaware=["紫砂壶", "盖碗"],
        flavor_notes=["岩韵", "花香", "果香"],
        health_benefits=["降血脂", "抗氧化", "健胃"],
        caffeine_level="high",
        description="武夷岩茶之王，独具「岩骨花香」。"
    ),
    "凤凰单丛": TeaInfo(
        name="凤凰单丛",
        category=TeaCategory.OOLONG,
        origin="广东潮州",
        water_temp_min=95,
        water_temp_max=100,
        first_steep_sec=15,
        steep_increment=3,
        max_steeps=12,
        recommended_teaware=["紫砂壶", "盖碗"],
        flavor_notes=["蜜香", "花香", "果香"],
        health_benefits=["减肥", "降火", "助消化"],
        caffeine_level="medium",
        description="广东乌龙代表，香型丰富，「一树一香」。"
    ),
    "冻顶乌龙": TeaInfo(
        name="冻顶乌龙",
        category=TeaCategory.OOLONG,
        origin="台湾南投",
        water_temp_min=90,
        water_temp_max=95,
        first_steep_sec=35,
        steep_increment=5,
        max_steeps=7,
        recommended_teaware=["紫砂壶", "盖碗"],
        flavor_notes=["兰花香", "蜜香", "甘醇"],
        health_benefits=["抗氧化", "降血脂", "提神"],
        caffeine_level="medium",
        description="台湾名茶，发酵程度中等，香气清雅。"
    ),
    
    # 红茶类
    "正山小种": TeaInfo(
        name="正山小种",
        category=TeaCategory.BLACK,
        origin="福建武夷山",
        water_temp_min=90,
        water_temp_max=95,
        first_steep_sec=40,
        steep_increment=8,
        max_steeps=6,
        recommended_teaware=["紫砂壶", "盖碗", "瓷杯"],
        flavor_notes=["松烟香", "桂圆香", "甜醇"],
        health_benefits=["暖胃", "抗氧化", "提神"],
        caffeine_level="high",
        description="红茶鼻祖，独具松烟香，世界最早的红茶。"
    ),
    "金骏眉": TeaInfo(
        name="金骏眉",
        category=TeaCategory.BLACK,
        origin="福建武夷山",
        water_temp_min=90,
        water_temp_max=95,
        first_steep_sec=35,
        steep_increment=5,
        max_steeps=8,
        recommended_teaware=["盖碗", "玻璃杯"],
        flavor_notes=["蜜香", "花香", "果香"],
        health_benefits=["暖胃", "养颜", "抗氧化"],
        caffeine_level="high",
        description="高端红茶，全芽制作，金毫显露。"
    ),
    "祁门红茶": TeaInfo(
        name="祁门红茶",
        category=TeaCategory.BLACK,
        origin="安徽祁门",
        water_temp_min=90,
        water_temp_max=95,
        first_steep_sec=45,
        steep_increment=10,
        max_steeps=5,
        recommended_teaware=["紫砂壶", "盖碗", "瓷杯"],
        flavor_notes=["蜜糖香", "兰花香", "醇厚"],
        health_benefits=["暖胃", "提神", "消食"],
        caffeine_level="high",
        description="世界三大高香红茶之一，「祁门香」享誉全球。"
    ),
    "滇红": TeaInfo(
        name="滇红",
        category=TeaCategory.BLACK,
        origin="云南临沧/凤庆",
        water_temp_min=90,
        water_temp_max=95,
        first_steep_sec=40,
        steep_increment=8,
        max_steeps=6,
        recommended_teaware=["紫砂壶", "盖碗"],
        flavor_notes=["蜜香", "麦芽香", "甜醇"],
        health_benefits=["暖胃", "养胃", "抗氧化"],
        caffeine_level="high",
        description="云南大叶种红茶，金毫显露，滋味浓醇。"
    ),
    
    # 黑茶类
    "安化黑茶": TeaInfo(
        name="安化黑茶",
        category=TeaCategory.DARK,
        origin="湖南安化",
        water_temp_min=100,
        water_temp_max=100,
        first_steep_sec=30,
        steep_increment=10,
        max_steeps=8,
        recommended_teaware=["紫砂壶", "陶壶"],
        flavor_notes=["陈香", "菌花香", "醇厚"],
        health_benefits=["降脂", "消食", "解毒"],
        caffeine_level="medium",
        description="湖南黑茶，含有「金花」益生菌，有助消化。"
    ),
    
    # 普洱茶类
    "生普": TeaInfo(
        name="生普",
        category=TeaCategory.PUERH_RAW,
        origin="云南西双版纳/临沧",
        water_temp_min=95,
        water_temp_max=100,
        first_steep_sec=20,
        steep_increment=5,
        max_steeps=15,
        recommended_teaware=["紫砂壶", "盖碗"],
        flavor_notes=["蜜香", "花香", "回甘"],
        health_benefits=["降脂", "减肥", "抗氧化"],
        caffeine_level="high",
        description="普洱生茶，未经渥堆发酵，口感鲜活，可长期存放陈化。"
    ),
    "熟普": TeaInfo(
        name="熟普",
        category=TeaCategory.PUERH_RIPE,
        origin="云南西双版纳/临沧",
        water_temp_min=95,
        water_temp_max=100,
        first_steep_sec=20,
        steep_increment=5,
        max_steeps=12,
        recommended_teaware=["紫砂壶", "盖碗"],
        flavor_notes=["陈香", "枣香", "醇厚"],
        health_benefits=["暖胃", "降脂", "助消化"],
        caffeine_level="low",
        description="普洱熟茶，经渥堆发酵，汤色红浓，口感醇厚。"
    ),
    
    # 花草茶类
    "茉莉花茶": TeaInfo(
        name="茉莉花茶",
        category=TeaCategory.HERBAL,
        origin="福建福州/广西横县",
        water_temp_min=85,
        water_temp_max=90,
        first_steep_sec=40,
        steep_increment=10,
        max_steeps=4,
        recommended_teaware=["玻璃杯", "盖碗"],
        flavor_notes=["茉莉香", "鲜爽", "甘甜"],
        health_benefits=["安神", "理气", "解郁"],
        caffeine_level="low",
        description="以绿茶为茶坯窨制而成，「在中国的花茶里，可闻春天的气味」。"
    ),
    "玫瑰花茶": TeaInfo(
        name="玫瑰花茶",
        category=TeaCategory.HERBAL,
        origin="多地生产",
        water_temp_min=80,
        water_temp_max=85,
        first_steep_sec=180,
        steep_increment=30,
        max_steeps=3,
        recommended_teaware=["玻璃杯"],
        flavor_notes=["玫瑰香", "甜润", "清雅"],
        health_benefits=["美容养颜", "调经止痛", "疏肝解郁"],
        caffeine_level="none",
        description="以玫瑰花蕾制成，香气浓郁，美容养颜佳品。"
    ),
    "菊花茶": TeaInfo(
        name="菊花茶",
        category=TeaCategory.HERBAL,
        origin="浙江桐乡/安徽黄山",
        water_temp_min=90,
        water_temp_max=95,
        first_steep_sec=120,
        steep_increment=30,
        max_steeps=3,
        recommended_teaware=["玻璃杯"],
        flavor_notes=["菊花香", "清甜", "微苦"],
        health_benefits=["清热解毒", "明目", "降火"],
        caffeine_level="none",
        description="以干菊花冲泡，可加枸杞、蜂蜜，清肝明目。"
    ),
    
    # 抹茶类
    "抹茶": TeaInfo(
        name="抹茶",
        category=TeaCategory.MATCHA,
        origin="日本宇治/中国杭州",
        water_temp_min=75,
        water_temp_max=80,
        first_steep_sec=0,  # 抹茶不需要浸泡，直接点茶
        steep_increment=0,
        max_steeps=1,
        recommended_teaware=["茶碗", "茶筅"],
        flavor_notes=["海苔香", "青草香", "鲜爽"],
        health_benefits=["抗氧化", "提神", "减肥"],
        caffeine_level="high",
        description="碾茶研磨成粉，日本茶道核心，茶汤同饮。"
    ),
}


# ==================== 核心功能函数 ====================

def get_tea_info(tea_name: str) -> Optional[TeaInfo]:
    """
    获取茶叶信息
    
    Args:
        tea_name: 茶叶名称
        
    Returns:
        TeaInfo对象，未找到返回None
    """
    return TEA_DATABASE.get(tea_name)


def list_teas_by_category(category: Optional[TeaCategory] = None) -> List[str]:
    """
    按类别列出茶叶
    
    Args:
        category: 茶叶类别，None表示列出所有
        
    Returns:
        茶叶名称列表
    """
    if category is None:
        return list(TEA_DATABASE.keys())
    return [name for name, info in TEA_DATABASE.items() if info.category == category]


def get_water_temp_recommendation(tea_name: str) -> Tuple[int, int, str]:
    """
    获取水温推荐
    
    Args:
        tea_name: 茶叶名称
        
    Returns:
        (最低水温, 最高水温, 推荐说明)
    """
    tea = get_tea_info(tea_name)
    if tea is None:
        return (85, 95, "未找到该茶叶，使用通用推荐")
    
    temp_avg = (tea.water_temp_min + tea.water_temp_max) // 2
    note = f"{tea.category.value}，推荐{tea.water_temp_min}-{tea.water_temp_max}°C"
    if tea.water_temp_max >= 95:
        note += "，建议沸水冲泡"
    elif tea.water_temp_min <= 75:
        note += "，注意水温不宜过高，避免烫伤茶叶"
    
    return (tea.water_temp_min, tea.water_temp_max, note)


def calculate_steep_time(tea_name: str, steep_number: int) -> Tuple[int, str]:
    """
    计算指定泡数的浸泡时间
    
    Args:
        tea_name: 茶叶名称
        steep_number: 第几泡(从1开始)
        
    Returns:
        (浸泡秒数, 说明)
    """
    tea = get_tea_info(tea_name)
    if tea is None:
        return (30, "未找到该茶叶，使用默认时间")
    
    if steep_number < 1:
        return (tea.first_steep_sec, "泡数从1开始")
    
    if steep_number > tea.max_steeps:
        return (
            tea.first_steep_sec + (tea.max_steeps - 1) * tea.steep_increment,
            f"已超过推荐最大泡数({tea.max_steeps}泡)，使用最后一泡时间"
        )
    
    steep_time = tea.first_steep_sec + (steep_number - 1) * tea.steep_increment
    note = f"第{steep_number}泡，浸泡{steep_time}秒"
    return (steep_time, note)


def get_brewing_schedule(tea_name: str) -> List[Dict[str, int]]:
    """
    获取完整冲泡计划
    
    Args:
        tea_name: 茶叶名称
        
    Returns:
        冲泡计划列表，每项包含泡数、时间
    """
    tea = get_tea_info(tea_name)
    if tea is None:
        return []
    
    schedule = []
    for i in range(1, tea.max_steeps + 1):
        time_sec, _ = calculate_steep_time(tea_name, i)
        schedule.append({
            "steep": i,
            "seconds": time_sec,
            "water_temp_min": tea.water_temp_min,
            "water_temp_max": tea.water_temp_max,
        })
    return schedule


def recommend_teaware(tea_name: str) -> Tuple[List[str], str]:
    """
    推荐茶具
    
    Args:
        tea_name: 茶叶名称
        
    Returns:
        (推荐茶具列表, 说明)
    """
    tea = get_tea_info(tea_name)
    if tea is None:
        return (["盖碗", "紫砂壶"], "未找到该茶叶，使用通用推荐")
    
    note = f"{tea.category.value}类茶叶，"
    if tea.category == TeaCategory.GREEN:
        note += "宜用透明茶具观赏茶叶舒展"
    elif tea.category in [TeaCategory.OOLONG, TeaCategory.PUERH_RAW, TeaCategory.PUERH_RIPE]:
        note += "宜用紫砂壶或盖碗，高温激发香气"
    elif tea.category == TeaCategory.BLACK:
        note += "可用紫砂壶或瓷杯，温润香气"
    elif tea.category == TeaCategory.WHITE:
        note += "宜用白瓷盖碗或玻璃杯，品味毫香"
    
    return (tea.recommended_teaware, note)


def get_caffeine_info(tea_name: str) -> Tuple[str, int]:
    """
    获取咖啡因信息
    
    Args:
        tea_name: 茶叶名称
        
    Returns:
        (咖啡因等级, 相对含量百分比估算)
    """
    tea = get_tea_info(tea_name)
    if tea is None:
        return ("unknown", 0)
    
    caffeine_map = {
        "none": ("无咖啡因", 0),
        "low": ("低", 20),
        "medium": ("中等", 50),
        "high": ("高", 80),
    }
    
    level, percent = caffeine_map.get(tea.caffeine_level, ("未知", 0))
    return (level, percent)


def search_tea(query: str) -> List[Tuple[str, str, float]]:
    """
    搜索茶叶
    
    Args:
        query: 搜索关键词
        
    Returns:
        匹配结果列表：(名称, 类别, 匹配度)
    """
    results = []
    query_lower = query.lower()
    
    for name, info in TEA_DATABASE.items():
        score = 0.0
        if query_lower in name.lower():
            score = 1.0
        elif query_lower in info.category.value:
            score = 0.8
        elif query_lower in info.origin:
            score = 0.6
        elif any(query_lower in note.lower() for note in info.flavor_notes):
            score = 0.5
        elif query_lower in info.description.lower():
            score = 0.3
        
        if score > 0:
            results.append((name, info.category.value, score))
    
    return sorted(results, key=lambda x: x[2], reverse=True)


def get_tea_benefits(tea_name: str) -> List[str]:
    """
    获取茶叶健康功效
    
    Args:
        tea_name: 茶叶名称
        
    Returns:
        功效列表
    """
    tea = get_tea_info(tea_name)
    if tea is None:
        return ["未找到该茶叶信息"]
    return tea.health_benefits


def get_tea_flavor_notes(tea_name: str) -> List[str]:
    """
    获取茶叶风味特点
    
    Args:
        tea_name: 茶叶名称
        
    Returns:
        风味列表
    """
    tea = get_tea_info(tea_name)
    if tea is None:
        return ["未找到该茶叶信息"]
    return tea.flavor_notes


# ==================== 计时器类 ====================

class TeaTimer:
    """泡茶计时器"""
    
    def __init__(self, tea_name: str, total_steeps: Optional[int] = None):
        """
        初始化计时器
        
        Args:
            tea_name: 茶叶名称
            total_steeps: 总泡数，None则使用茶叶推荐值
        """
        self.tea_name = tea_name
        self.tea_info = get_tea_info(tea_name)
        
        if self.tea_info is None:
            raise ValueError(f"未找到茶叶: {tea_name}")
        
        self.total_steeps = total_steeps or self.tea_info.max_steeps
        self.current_steep = 0
        self.start_time: Optional[float] = None
        self.is_running = False
    
    def start(self) -> Dict[str, any]:
        """
        开始计时
        
        Returns:
            当前泡信息
        """
        if self.current_steep >= self.total_steeps:
            return {"error": "已达最大泡数"}
        
        self.current_steep += 1
        self.start_time = time.time()
        self.is_running = True
        
        steep_time, note = calculate_steep_time(self.tea_name, self.current_steep)
        
        return {
            "steep": self.current_steep,
            "duration_sec": steep_time,
            "note": note,
            "started_at": self.start_time,
        }
    
    def check(self) -> Dict[str, any]:
        """
        检查当前状态
        
        Returns:
            状态信息
        """
        if not self.is_running:
            return {"status": "not_running"}
        
        elapsed = time.time() - (self.start_time or 0)
        steep_time, _ = calculate_steep_time(self.tea_name, self.current_steep)
        remaining = max(0, steep_time - elapsed)
        
        return {
            "status": "running" if remaining > 0 else "completed",
            "steep": self.current_steep,
            "elapsed_sec": round(elapsed, 1),
            "remaining_sec": round(remaining, 1),
            "target_sec": steep_time,
            "progress": min(1.0, elapsed / steep_time) if steep_time > 0 else 1.0,
        }
    
    def stop(self) -> Dict[str, any]:
        """
        停止计时
        
        Returns:
            最终状态
        """
        if not self.is_running:
            return {"status": "not_running"}
        
        elapsed = time.time() - (self.start_time or 0)
        self.is_running = False
        
        return {
            "status": "stopped",
            "steep": self.current_steep,
            "elapsed_sec": round(elapsed, 1),
        }
    
    def reset(self) -> Dict[str, any]:
        """
        重置计时器
        
        Returns:
            重置状态
        """
        self.current_steep = 0
        self.start_time = None
        self.is_running = False
        
        return {"status": "reset", "total_steeps": self.total_steeps}
    
    def get_status(self) -> Dict[str, any]:
        """
        获取完整状态
        
        Returns:
            状态信息
        """
        return {
            "tea_name": self.tea_name,
            "tea_category": self.tea_info.category.value if self.tea_info else None,
            "current_steep": self.current_steep,
            "total_steeps": self.total_steeps,
            "is_running": self.is_running,
            "water_temp": f"{self.tea_info.water_temp_min}-{self.tea_info.water_temp_max}°C" if self.tea_info else None,
        }


# ==================== 辅助函数 ====================

def format_time(seconds: int) -> str:
    """
    格式化时间显示
    
    Args:
        seconds: 秒数
        
    Returns:
        格式化时间字符串
    """
    if seconds < 60:
        return f"{seconds}秒"
    minutes = seconds // 60
    secs = seconds % 60
    if secs == 0:
        return f"{minutes}分钟"
    return f"{minutes}分{secs}秒"


def get_all_categories() -> List[Tuple[str, int]]:
    """
    获取所有茶叶类别及其数量
    
    Returns:
        [(类别名, 数量), ...]
    """
    category_count: Dict[TeaCategory, int] = {}
    for tea in TEA_DATABASE.values():
        category_count[tea.category] = category_count.get(tea.category, 0) + 1
    
    return [(cat.value, count) for cat, count in sorted(category_count.items(), key=lambda x: -x[1])]


def get_tea_count() -> int:
    """获取茶叶数据库中的茶叶数量"""
    return len(TEA_DATABASE)


def compare_teas(tea_names: List[str]) -> List[Dict[str, any]]:
    """
    对比多种茶叶
    
    Args:
        tea_names: 茶叶名称列表
        
    Returns:
        对比数据列表
    """
    comparison = []
    for name in tea_names:
        tea = get_tea_info(name)
        if tea:
            comparison.append({
                "name": name,
                "category": tea.category.value,
                "origin": tea.origin,
                "water_temp": f"{tea.water_temp_min}-{tea.water_temp_max}°C",
                "first_steep": format_time(tea.first_steep_sec),
                "max_steeps": tea.max_steeps,
                "caffeine": tea.caffeine_level,
                "flavor_notes": tea.flavor_notes,
            })
    return comparison


def suggest_tea_by_mood(mood: str) -> List[Tuple[str, str]]:
    """
    根据心情推荐茶叶
    
    Args:
        mood: 心情描述
        
    Returns:
        [(茶叶名称, 推荐理由), ...]
    """
    suggestions = []
    mood_lower = mood.lower()
    
    # 心情映射规则
    mood_keywords = {
        "提神": [("铁观音", "半发酵茶，香气高扬提神"), ("生普", "茶气足，回甘强，提神醒脑")],
        "放松": [("熟普", "醇厚温和，安神舒缓"), ("玫瑰花茶", "花香怡人，疏肝解郁")],
        "消化": [("安化黑茶", "金花菌助消化"), ("熟普", "温润养胃，助消化")],
        "减肥": [("生普", "降脂减肥效果好"), ("铁观音", "促进新陈代谢")],
        "养颜": [("玫瑰花茶", "美容养颜"), ("白毫银针", "抗氧化，延缓衰老")],
        "清热": [("菊花茶", "清热解毒明目"), ("龙井", "清热降火")],
        "暖胃": [("熟普", "温润养胃"), ("滇红", "温润甜醇，暖胃")],
        "工作": [("龙井", "提神醒脑，口感清爽"), ("碧螺春", "清香怡人，适合工作时饮用")],
        "下午": [("茉莉花茶", "香气清雅，下午茶首选"), ("铁观音", "香气持久，回味悠长")],
        "晚上": [("熟普", "咖啡因低，不影响睡眠"), ("玫瑰花茶", "安神助眠")],
    }
    
    for keyword, teas in mood_keywords.items():
        if keyword in mood_lower:
            suggestions.extend(teas)
    
    if not suggestions:
        suggestions = [
            ("铁观音", "香气高扬，适合日常饮用"),
            ("熟普", "温和醇厚，老少皆宜"),
        ]
    
    return suggestions[:3]


# ==================== 常量导出 ====================

__all__ = [
    # 数据类
    "TeaCategory",
    "TeaInfo",
    "TEA_DATABASE",
    # 核心函数
    "get_tea_info",
    "list_teas_by_category",
    "get_water_temp_recommendation",
    "calculate_steep_time",
    "get_brewing_schedule",
    "recommend_teaware",
    "get_caffeine_info",
    "search_tea",
    "get_tea_benefits",
    "get_tea_flavor_notes",
    # 计时器
    "TeaTimer",
    # 辅助函数
    "format_time",
    "get_all_categories",
    "get_tea_count",
    "compare_teas",
    "suggest_tea_by_mood",
]
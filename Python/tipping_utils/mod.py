"""
Tipping Utils - 小费计算工具

支持多国家小费文化、账单分割、百分比计算等功能。
零外部依赖，仅使用 Python 标准库。
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
from enum import Enum
from decimal import Decimal, ROUND_HALF_UP


class Country(Enum):
    """国家枚举，包含不同的小费文化"""
    # 北美 - 小费文化较强
    USA = "USA"
    CANADA = "Canada"
    MEXICO = "Mexico"
    
    # 欧洲 - 小费文化多样
    UK = "UK"
    FRANCE = "France"
    GERMANY = "Germany"
    ITALY = "Italy"
    SPAIN = "Spain"
    PORTUGAL = "Portugal"
    NETHERLANDS = "Netherlands"
    BELGIUM = "Belgium"
    SWITZERLAND = "Switzerland"
    AUSTRIA = "Austria"
    GREECE = "Greece"
    
    # 亚洲 - 小费文化较弱或无
    JAPAN = "Japan"
    CHINA = "China"
    SOUTH_KOREA = "South Korea"
    SINGAPORE = "Singapore"
    THAILAND = "Thailand"
    VIETNAM = "Vietnam"
    INDONESIA = "Indonesia"
    MALAYSIA = "Malaysia"
    PHILIPPINES = "Philippines"
    INDIA = "India"
    
    # 大洋洲
    AUSTRALIA = "Australia"
    NEW_ZEALAND = "New Zealand"
    
    # 南美洲
    BRAZIL = "Brazil"
    ARGENTINA = "Argentina"
    CHILE = "Chile"
    COLOMBIA = "Colombia"
    PERU = "Peru"
    
    # 非洲
    SOUTH_AFRICA = "South Africa"
    EGYPT = "Egypt"
    MOROCCO = "Morocco"
    
    # 中东
    UAE = "UAE"
    ISRAEL = "Israel"
    TURKEY = "Turkey"
    
    # 其他
    RUSSIA = "Russia"
    POLAND = "Poland"
    CZECH = "Czech Republic"
    HUNGARY = "Hungary"
    SWEDEN = "Sweden"
    NORWAY = "Norway"
    DENMARK = "Denmark"
    FINLAND = "Finland"
    IRELAND = "Ireland"


class ServiceType(Enum):
    """服务类型"""
    RESTAURANT = "restaurant"
    BAR = "bar"
    CAFE = "cafe"
    DELIVERY = "delivery"
    TAXI = "taxi"
    RIDESHARE = "rideshare"
    HOTEL = "hotel"
    HAIR_SALON = "hair_salon"
    SPA = "spa"
    TOUR = "tour"
    BELLBOY = "bellboy"
    VALET = "valet"
    ROOM_SERVICE = "room_service"
    CONCIERGE = "concierge"


@dataclass
class TipRecommendation:
    """小费建议"""
    country: Country
    service_type: ServiceType
    min_percent: float
    max_percent: float
    standard_percent: float
    is_customary: bool
    is_expected: bool
    is_included: bool  # 服务费是否已包含
    notes: str


@dataclass
class BillSplit:
    """账单分割结果"""
    subtotal: float
    tax: float
    tip: float
    total: float
    per_person: float
    people_count: int
    individual_amounts: Optional[List[float]] = None


@dataclass
class TipCalculation:
    """小费计算结果"""
    bill_amount: float
    tip_percent: float
    tip_amount: float
    total: float
    tax: Optional[float] = None
    tax_included: bool = False
    grand_total: Optional[float] = None


# 国家小费文化数据库
TIPPING_DATA: Dict[Country, Dict[ServiceType, TipRecommendation]] = {
    Country.USA: {
        ServiceType.RESTAURANT: TipRecommendation(Country.USA, ServiceType.RESTAURANT, 15.0, 25.0, 18.0, True, True, False, "15%为最低，18-20%标准，优质服务25%"),
        ServiceType.BAR: TipRecommendation(Country.USA, ServiceType.BAR, 15.0, 20.0, 18.0, True, True, False, "每杯$1-2或账单的15-20%"),
        ServiceType.CAFE: TipRecommendation(Country.USA, ServiceType.CAFE, 0.0, 20.0, 15.0, True, False, False, "可选项，通常留零钱或10-15%"),
        ServiceType.DELIVERY: TipRecommendation(Country.USA, ServiceType.DELIVERY, 10.0, 20.0, 15.0, True, True, False, "最低$3-5，恶劣天气加价"),
        ServiceType.TAXI: TipRecommendation(Country.USA, ServiceType.TAXI, 15.0, 20.0, 18.0, True, True, False, "15-20%，行李每件$1-2"),
        ServiceType.RIDESHARE: TipRecommendation(Country.USA, ServiceType.RIDESHARE, 15.0, 20.0, 18.0, True, False, False, "App内打赏，15-20%"),
        ServiceType.HOTEL: TipRecommendation(Country.USA, ServiceType.HOTEL, 0.0, 0.0, 0.0, True, True, False, "参考其他酒店服务"),
        ServiceType.BELLBOY: TipRecommendation(Country.USA, ServiceType.BELLBOY, 1.0, 2.0, 1.0, True, True, False, "每件行李$1-2"),
        ServiceType.VALET: TipRecommendation(Country.USA, ServiceType.VALET, 2.0, 5.0, 3.0, True, True, False, "取车时给$2-5"),
        ServiceType.ROOM_SERVICE: TipRecommendation(Country.USA, ServiceType.ROOM_SERVICE, 15.0, 20.0, 18.0, True, True, True, "服务费通常已含，额外5-10%"),
        ServiceType.CONCIERGE: TipRecommendation(Country.USA, ServiceType.CONCIERGE, 5.0, 20.0, 10.0, True, False, False, "特殊服务$5-20"),
        ServiceType.HAIR_SALON: TipRecommendation(Country.USA, ServiceType.HAIR_SALON, 15.0, 20.0, 18.0, True, True, False, "15-20%，助理$5"),
        ServiceType.SPA: TipRecommendation(Country.USA, ServiceType.SPA, 15.0, 20.0, 18.0, True, True, False, "15-20%"),
        ServiceType.TOUR: TipRecommendation(Country.USA, ServiceType.TOUR, 10.0, 20.0, 15.0, True, False, False, "一日游$10-20"),
    },
    Country.CANADA: {
        ServiceType.RESTAURANT: TipRecommendation(Country.CANADA, ServiceType.RESTAURANT, 15.0, 20.0, 15.0, True, True, False, "与美国类似，15-20%"),
        ServiceType.BAR: TipRecommendation(Country.CANADA, ServiceType.BAR, 15.0, 20.0, 15.0, True, True, False, "15-20%"),
        ServiceType.TAXI: TipRecommendation(Country.CANADA, ServiceType.TAXI, 10.0, 15.0, 15.0, True, True, False, "10-15%"),
        ServiceType.DELIVERY: TipRecommendation(Country.CANADA, ServiceType.DELIVERY, 10.0, 15.0, 15.0, True, True, False, "10-15%"),
    },
    Country.MEXICO: {
        ServiceType.RESTAURANT: TipRecommendation(Country.MEXICO, ServiceType.RESTAURANT, 10.0, 15.0, 15.0, True, True, False, "10-15%，高档餐厅可能更高"),
        ServiceType.BAR: TipRecommendation(Country.MEXICO, ServiceType.BAR, 10.0, 15.0, 10.0, True, False, False, "10%或留零钱"),
        ServiceType.TAXI: TipRecommendation(Country.MEXICO, ServiceType.TAXI, 0.0, 10.0, 0.0, True, False, False, "不强制，可四舍五入"),
    },
    Country.UK: {
        ServiceType.RESTAURANT: TipRecommendation(Country.UK, ServiceType.RESTAURANT, 10.0, 15.0, 12.5, True, False, True, "服务费常已含，额外10-15%"),
        ServiceType.BAR: TipRecommendation(Country.UK, ServiceType.BAR, 0.0, 0.0, 0.0, False, False, False, "酒吧不期望小费"),
        ServiceType.TAXI: TipRecommendation(Country.UK, ServiceType.TAXI, 10.0, 15.0, 10.0, True, False, False, "10-15%或四舍五入"),
    },
    Country.FRANCE: {
        ServiceType.RESTAURANT: TipRecommendation(Country.FRANCE, ServiceType.RESTAURANT, 0.0, 5.0, 0.0, False, False, True, "服务费已含，小费非强制"),
        ServiceType.BAR: TipRecommendation(Country.FRANCE, ServiceType.BAR, 0.0, 0.0, 0.0, False, False, False, "不期望小费"),
        ServiceType.TAXI: TipRecommendation(Country.FRANCE, ServiceType.TAXI, 0.0, 5.0, 0.0, False, False, False, "可四舍五入"),
    },
    Country.GERMANY: {
        ServiceType.RESTAURANT: TipRecommendation(Country.GERMANY, ServiceType.RESTAURANT, 5.0, 10.0, 5.0, True, False, True, "服务费已含，5-10%已足够"),
        ServiceType.BAR: TipRecommendation(Country.GERMANY, ServiceType.BAR, 0.0, 5.0, 0.0, False, False, False, "可留零钱"),
        ServiceType.TAXI: TipRecommendation(Country.GERMANY, ServiceType.TAXI, 5.0, 10.0, 5.0, True, False, False, "5-10%或四舍五入"),
    },
    Country.ITALY: {
        ServiceType.RESTAURANT: TipRecommendation(Country.ITALY, ServiceType.RESTAURANT, 0.0, 10.0, 0.0, False, False, True, "服务费已含，可留小额"),
        ServiceType.BAR: TipRecommendation(Country.ITALY, ServiceType.BAR, 0.0, 0.0, 0.0, False, False, False, "站立饮用不需小费"),
        ServiceType.TAXI: TipRecommendation(Country.ITALY, ServiceType.TAXI, 0.0, 5.0, 0.0, False, False, False, "可四舍五入"),
    },
    Country.SPAIN: {
        ServiceType.RESTAURANT: TipRecommendation(Country.SPAIN, ServiceType.RESTAURANT, 0.0, 10.0, 5.0, True, False, False, "5-10%已足够"),
        ServiceType.BAR: TipRecommendation(Country.SPAIN, ServiceType.BAR, 0.0, 0.0, 0.0, False, False, False, "不期望小费"),
        ServiceType.TAXI: TipRecommendation(Country.SPAIN, ServiceType.TAXI, 0.0, 5.0, 0.0, False, False, False, "可四舍五入"),
    },
    Country.JAPAN: {
        ServiceType.RESTAURANT: TipRecommendation(Country.JAPAN, ServiceType.RESTAURANT, 0.0, 0.0, 0.0, False, False, False, "不期望小费，可能被视为无礼"),
        ServiceType.BAR: TipRecommendation(Country.JAPAN, ServiceType.BAR, 0.0, 0.0, 0.0, False, False, False, "无小费文化"),
        ServiceType.TAXI: TipRecommendation(Country.JAPAN, ServiceType.TAXI, 0.0, 0.0, 0.0, False, False, False, "无需小费"),
        ServiceType.HOTEL: TipRecommendation(Country.JAPAN, ServiceType.HOTEL, 0.0, 0.0, 0.0, False, False, False, "无需小费"),
    },
    Country.CHINA: {
        ServiceType.RESTAURANT: TipRecommendation(Country.CHINA, ServiceType.RESTAURANT, 0.0, 0.0, 0.0, False, False, False, "无小费文化"),
        ServiceType.BAR: TipRecommendation(Country.CHINA, ServiceType.BAR, 0.0, 0.0, 0.0, False, False, False, "无小费文化"),
        ServiceType.TAXI: TipRecommendation(Country.CHINA, ServiceType.TAXI, 0.0, 0.0, 0.0, False, False, False, "无需小费"),
        ServiceType.HOTEL: TipRecommendation(Country.CHINA, ServiceType.HOTEL, 0.0, 0.0, 0.0, False, False, False, "无需小费"),
    },
    Country.SOUTH_KOREA: {
        ServiceType.RESTAURANT: TipRecommendation(Country.SOUTH_KOREA, ServiceType.RESTAURANT, 0.0, 0.0, 0.0, False, False, False, "无小费文化"),
        ServiceType.TAXI: TipRecommendation(Country.SOUTH_KOREA, ServiceType.TAXI, 0.0, 0.0, 0.0, False, False, False, "无需小费"),
    },
    Country.SINGAPORE: {
        ServiceType.RESTAURANT: TipRecommendation(Country.SINGAPORE, ServiceType.RESTAURANT, 0.0, 10.0, 0.0, False, False, True, "服务费通常已含10%"),
        ServiceType.TAXI: TipRecommendation(Country.SINGAPORE, ServiceType.TAXI, 0.0, 0.0, 0.0, False, False, False, "无需小费"),
    },
    Country.THAILAND: {
        ServiceType.RESTAURANT: TipRecommendation(Country.THAILAND, ServiceType.RESTAURANT, 0.0, 10.0, 5.0, True, False, False, "可留5-10%"),
        ServiceType.TAXI: TipRecommendation(Country.THAILAND, ServiceType.TAXI, 0.0, 0.0, 0.0, False, False, False, "可四舍五入"),
    },
    Country.AUSTRALIA: {
        ServiceType.RESTAURANT: TipRecommendation(Country.AUSTRALIA, ServiceType.RESTAURANT, 0.0, 10.0, 10.0, False, False, False, "非强制，10%已足够"),
        ServiceType.BAR: TipRecommendation(Country.AUSTRALIA, ServiceType.BAR, 0.0, 0.0, 0.0, False, False, False, "不期望小费"),
        ServiceType.TAXI: TipRecommendation(Country.AUSTRALIA, ServiceType.TAXI, 0.0, 10.0, 0.0, False, False, False, "可四舍五入"),
    },
    Country.NEW_ZEALAND: {
        ServiceType.RESTAURANT: TipRecommendation(Country.NEW_ZEALAND, ServiceType.RESTAURANT, 0.0, 10.0, 0.0, False, False, False, "非强制"),
        ServiceType.TAXI: TipRecommendation(Country.NEW_ZEALAND, ServiceType.TAXI, 0.0, 0.0, 0.0, False, False, False, "可四舍五入"),
    },
    Country.BRAZIL: {
        ServiceType.RESTAURANT: TipRecommendation(Country.BRAZIL, ServiceType.RESTAURANT, 10.0, 10.0, 10.0, True, True, True, "通常已含10%服务费"),
        ServiceType.TAXI: TipRecommendation(Country.BRAZIL, ServiceType.TAXI, 0.0, 10.0, 0.0, False, False, False, "可四舍五入"),
    },
    Country.ARGENTINA: {
        ServiceType.RESTAURANT: TipRecommendation(Country.ARGENTINA, ServiceType.RESTAURANT, 10.0, 15.0, 10.0, True, True, False, "10-15%"),
        ServiceType.TAXI: TipRecommendation(Country.ARGENTINA, ServiceType.TAXI, 0.0, 10.0, 0.0, False, False, False, "可四舍五入"),
    },
    Country.SOUTH_AFRICA: {
        ServiceType.RESTAURANT: TipRecommendation(Country.SOUTH_AFRICA, ServiceType.RESTAURANT, 10.0, 15.0, 10.0, True, True, False, "10-15%"),
        ServiceType.TAXI: TipRecommendation(Country.SOUTH_AFRICA, ServiceType.TAXI, 10.0, 10.0, 10.0, True, False, False, "约10%"),
    },
    Country.UAE: {
        ServiceType.RESTAURANT: TipRecommendation(Country.UAE, ServiceType.RESTAURANT, 10.0, 15.0, 10.0, True, False, True, "服务费常已含，额外10%"),
        ServiceType.TAXI: TipRecommendation(Country.UAE, ServiceType.TAXI, 0.0, 10.0, 0.0, False, False, False, "可四舍五入"),
    },
    Country.INDIA: {
        ServiceType.RESTAURANT: TipRecommendation(Country.INDIA, ServiceType.RESTAURANT, 5.0, 15.0, 10.0, True, False, False, "5-15%，高档餐厅更高"),
        ServiceType.TAXI: TipRecommendation(Country.INDIA, ServiceType.TAXI, 0.0, 10.0, 0.0, False, False, False, "可四舍五入"),
    },
}


def get_tip_recommendation(country: Country, service_type: ServiceType) -> Optional[TipRecommendation]:
    """
    获取特定国家和服务的建议小费
    
    Args:
        country: 国家
        service_type: 服务类型
    
    Returns:
        TipRecommendation 或 None（如果无数据）
    """
    if country in TIPPING_DATA:
        if service_type in TIPPING_DATA[country]:
            return TIPPING_DATA[country][service_type]
    return None


def calculate_tip(
    bill_amount: float,
    tip_percent: float,
    tax: float = 0.0,
    tax_included: bool = True
) -> TipCalculation:
    """
    计算小费
    
    Args:
        bill_amount: 账单金额
        tip_percent: 小费百分比（如 15 表示 15%）
        tax: 税金金额
        tax_included: 税金是否已包含在账单金额中
    
    Returns:
        TipCalculation 对象
    """
    tip_amount = bill_amount * (tip_percent / 100)
    total = bill_amount + tip_amount
    
    grand_total = None
    if tax > 0:
        if tax_included:
            grand_total = total  # 税已包含，不重复加
        else:
            grand_total = total + tax
    
    return TipCalculation(
        bill_amount=bill_amount,
        tip_percent=tip_percent,
        tip_amount=round(tip_amount, 2),
        total=round(total, 2),
        tax=tax if tax > 0 else None,
        tax_included=tax_included,
        grand_total=round(grand_total, 2) if grand_total else None
    )


def calculate_tip_with_tax(
    bill_amount: float,
    tip_percent: float,
    tax_percent: float,
    tip_on_pre_tax: bool = True
) -> TipCalculation:
    """
    计算含税小费
    
    Args:
        bill_amount: 账单金额（税前）
        tip_percent: 小费百分比
        tax_percent: 税率百分比
        tip_on_pre_tax: 是否在税前基础上计算小费
    
    Returns:
        TipCalculation 对象
    """
    tax_amount = bill_amount * (tax_percent / 100)
    
    if tip_on_pre_tax:
        tip_amount = bill_amount * (tip_percent / 100)
    else:
        tip_amount = (bill_amount + tax_amount) * (tip_percent / 100)
    
    total = bill_amount + tax_amount + tip_amount
    
    return TipCalculation(
        bill_amount=bill_amount,
        tip_percent=tip_percent,
        tip_amount=round(tip_amount, 2),
        total=round(bill_amount + tip_amount, 2),
        tax=round(tax_amount, 2),
        tax_included=False,
        grand_total=round(total, 2)
    )


def split_bill(
    bill_amount: float,
    people_count: int,
    tip_percent: float = 0.0,
    tax: float = 0.0,
    tax_included: bool = True,
    round_up: bool = False,
    individual_amounts: Optional[List[float]] = None
) -> BillSplit:
    """
    分割账单
    
    Args:
        bill_amount: 账单金额
        people_count: 分摊人数
        tip_percent: 小费百分比
        tax: 税金金额
        tax_included: 税金是否已包含
        round_up: 是否向上取整
        individual_amounts: 各人消费金额（如果非均摊）
    
    Returns:
        BillSplit 对象
    """
    if people_count <= 0:
        raise ValueError("人数必须大于0")
    
    if bill_amount < 0:
        raise ValueError("账单金额不能为负")
    
    # 计算小费
    tip_amount = bill_amount * (tip_percent / 100)
    
    # 计算总价
    total = bill_amount + tip_amount
    if tax > 0 and not tax_included:
        total += tax
    
    # 计算每人金额
    if individual_amounts:
        if len(individual_amounts) != people_count:
            raise ValueError("个人消费金额数量与人数不匹配")
        if abs(sum(individual_amounts) - bill_amount) > 0.01:
            raise ValueError("个人消费金额总和与账单金额不符")
        
        # 按比例分摊小费和税
        per_person_list = []
        for amount in individual_amounts:
            ratio = amount / bill_amount if bill_amount > 0 else 1 / people_count
            person_tip = tip_amount * ratio
            person_tax = tax * ratio if not tax_included else 0
            per_person_list.append(round(amount + person_tip + person_tax, 2))
        
        per_person = sum(per_person_list) / people_count
    else:
        per_person = total / people_count
        
        # 创建均摊列表
        base_per_person = total / people_count
        per_person_list = [round(base_per_person, 2) for _ in range(people_count)]
        
        # 处理分摊后的差额
        diff = round(total - sum(per_person_list), 2)
        if diff != 0:
            per_person_list[0] = round(per_person_list[0] + diff, 2)
    
    if round_up:
        per_person = -(-per_person // 0.01) * 0.01  # 向上取整到分
        per_person_list = [round(-(-p // 0.01) * 0.01, 2) for p in per_person_list]
    
    return BillSplit(
        subtotal=bill_amount,
        tax=tax,
        tip=round(tip_amount, 2),
        total=round(total, 2),
        per_person=round(per_person, 2),
        people_count=people_count,
        individual_amounts=per_person_list if individual_amounts else None
    )


def split_by_items(
    items: List[Tuple[str, float]],  # [(name, price), ...]
    tip_percent: float = 0.0,
    tax: float = 0.0,
    tax_percent: float = 0.0,
    tax_included: bool = True
) -> Dict[str, float]:
    """
    按项目分摊账单
    
    Args:
        items: 项目列表 [(名称, 价格), ...]
        tip_percent: 小费百分比
        tax: 税金金额（优先使用）
        tax_percent: 税率百分比（如无税金金额则使用）
        tax_included: 税金是否已包含
    
    Returns:
        Dict[str, float] 每人应付金额
    """
    if not items:
        return {}
    
    subtotal = sum(price for _, price in items)
    
    # 计算税金
    if tax == 0 and tax_percent > 0:
        tax = subtotal * (tax_percent / 100)
    
    # 计算小费
    tip_amount = subtotal * (tip_percent / 100)
    
    # 总额外费用（小费 + 税，如果税未包含）
    extra = tip_amount
    if not tax_included:
        extra += tax
    
    # 计算每个人应付（按比例分摊额外费用）
    result = {}
    for name, price in items:
        ratio = price / subtotal if subtotal > 0 else 0
        person_extra = extra * ratio
        result[name] = round(price + person_extra, 2)
    
    return result


def round_tip(
    tip_amount: float,
    method: str = "nearest",
    precision: float = 0.25
) -> float:
    """
    四舍五入小费金额
    
    Args:
        tip_amount: 小费金额
        method: 方法 ("nearest", "up", "down", "round")
        precision: 精度（如 0.25 表示四舍五入到 25 分）
    
    Returns:
        四舍五入后的小费
    """
    if method == "up":
        return -(-tip_amount // precision) * precision
    elif method == "down":
        return (tip_amount // precision) * precision
    elif method == "round":
        return round(tip_amount / precision) * precision
    else:  # nearest
        return round(tip_amount / precision) * precision


def suggest_tip(
    bill_amount: float,
    country: Country,
    service_type: ServiceType = ServiceType.RESTAURANT,
    service_quality: str = "good"
) -> Tuple[float, str]:
    """
    根据国家和场合建议小费
    
    Args:
        bill_amount: 账单金额
        country: 国家
        service_type: 服务类型
        service_quality: 服务质量 ("poor", "average", "good", "excellent")
    
    Returns:
        (建议小费金额, 说明)
    """
    recommendation = get_tip_recommendation(country, service_type)
    
    if not recommendation:
        return 0.0, f"无 {country.value} 的 {service_type.value} 小费数据"
    
    if not recommendation.is_customary:
        return 0.0, recommendation.notes
    
    # 根据服务质量确定百分比
    quality_map = {
        "poor": recommendation.min_percent,
        "average": (recommendation.min_percent + recommendation.standard_percent) / 2,
        "good": recommendation.standard_percent,
        "excellent": recommendation.max_percent
    }
    
    percent = quality_map.get(service_quality, recommendation.standard_percent)
    tip = bill_amount * (percent / 100)
    
    return round(tip, 2), recommendation.notes


def calculate_percentage(
    bill_amount: float,
    tip_amount: float
) -> float:
    """
    计算小费百分比
    
    Args:
        bill_amount: 账单金额
        tip_amount: 小费金额
    
    Returns:
        小费百分比
    """
    if bill_amount == 0:
        return 0.0
    return round((tip_amount / bill_amount) * 100, 2)


def calculate_quick_tips(bill_amount: float) -> Dict[str, TipCalculation]:
    """
    快速计算多个常用小费比例
    
    Args:
        bill_amount: 账单金额
    
    Returns:
        Dict[str, TipCalculation] 不同比例的计算结果
    """
    result = {}
    for percent in [10, 15, 18, 20, 25]:
        result[f"{percent}%"] = calculate_tip(bill_amount, percent)
    return result


def is_tipping_customary(country: Country, service_type: ServiceType = ServiceType.RESTAURANT) -> bool:
    """
    检查某国家/服务是否需要给小费
    
    Args:
        country: 国家
        service_type: 服务类型
    
    Returns:
        bool 是否需要给小费
    """
    recommendation = get_tip_recommendation(country, service_type)
    return recommendation.is_customary if recommendation else False


def get_countries_by_tipping_culture() -> Dict[str, List[Country]]:
    """
    按小费文化分类国家
    
    Returns:
        Dict[str, List[Country]] 分类后的国家列表
    """
    strong_tip = []  # 强小费文化
    moderate_tip = []  # 中等小费文化
    weak_tip = []  # 弱小费文化
    no_tip = []  # 无小费文化
    
    for country in Country:
        rec = get_tip_recommendation(country, ServiceType.RESTAURANT)
        if rec:
            if rec.is_expected and rec.standard_percent >= 15:
                strong_tip.append(country)
            elif rec.is_customary and rec.standard_percent > 0:
                moderate_tip.append(country)
            elif rec.standard_percent > 0:
                weak_tip.append(country)
            else:
                no_tip.append(country)
        else:
            # 默认无小费
            no_tip.append(country)
    
    return {
        "strong": strong_tip,
        "moderate": moderate_tip,
        "weak": weak_tip,
        "none": no_tip
    }


def convert_tip_for_currency(
    tip_amount: float,
    from_currency: str,
    to_currency: str,
    exchange_rate: float
) -> float:
    """
    货币换算小费
    
    Args:
        tip_amount: 小费金额
        from_currency: 原货币
        to_currency: 目标货币
        exchange_rate: 汇率
    
    Returns:
        换算后的小费金额
    """
    return round(tip_amount * exchange_rate, 2)


def calculate_tip_range(
    bill_amount: float,
    min_percent: float = 15.0,
    max_percent: float = 25.0
) -> Tuple[float, float]:
    """
    计算小费范围
    
    Args:
        bill_amount: 账单金额
        min_percent: 最低百分比
        max_percent: 最高百分比
    
    Returns:
        (最低小费, 最高小费)
    """
    min_tip = bill_amount * (min_percent / 100)
    max_tip = bill_amount * (max_percent / 100)
    return round(min_tip, 2), round(max_tip, 2)


def calculate_tip_with_rounding(
    bill_amount: float,
    tip_percent: float,
    round_to: float = 0.50,
    round_method: str = "nearest"
) -> Tuple[float, float, float]:
    """
    计算小费并四舍五入
    
    Args:
        bill_amount: 账单金额
        tip_percent: 小费百分比
        round_to: 四舍五入精度（如 0.50 表示四舍五入到 50 分）
        round_method: 方法 ("nearest", "up", "down")
    
    Returns:
        (原始小费, 四舍五入后小费, 总计)
    """
    raw_tip = bill_amount * (tip_percent / 100)
    rounded_tip = round_tip(raw_tip, round_method, round_to)
    total = bill_amount + rounded_tip
    
    return round(raw_tip, 2), round(rounded_tip, 2), round(total, 2)


def format_tip_summary(
    bill_amount: float,
    tip_percent: float,
    tax: float = 0.0,
    tax_included: bool = True,
    currency_symbol: str = "$"
) -> str:
    """
    格式化小费摘要
    
    Args:
        bill_amount: 账单金额
        tip_percent: 小费百分比
        tax: 税金
        tax_included: 税金是否已包含
        currency_symbol: 货币符号
    
    Returns:
        格式化的摘要字符串
    """
    calc = calculate_tip(bill_amount, tip_percent, tax, tax_included)
    
    lines = [
        f"账单: {currency_symbol}{bill_amount:.2f}",
        f"小费 ({tip_percent}%): {currency_symbol}{calc.tip_amount:.2f}",
    ]
    
    if calc.tax is not None:
        tax_label = "税金" if tax_included else "税金 (额外)"
        lines.append(f"{tax_label}: {currency_symbol}{calc.tax:.2f}")
    
    lines.append(f"总计: {currency_symbol}{calc.grand_total or calc.total:.2f}")
    
    return "\n".join(lines)


def calculate_shared_tip(
    bill_amount: float,
    tip_percent: float,
    people_count: int,
    individual_bills: Optional[List[float]] = None
) -> Dict[str, float]:
    """
    计算分摊小费
    
    Args:
        bill_amount: 总账单金额
        tip_percent: 小费百分比
        people_count: 人数
        individual_bills: 每人账单金额列表（如果非均摊）
    
    Returns:
        Dict 包含每人应付金额
    """
    total_tip = bill_amount * (tip_percent / 100)
    total = bill_amount + total_tip
    
    if individual_bills:
        if len(individual_bills) != people_count:
            raise ValueError("个人账单数量与人数不匹配")
        
        result = {}
        for i, bill in enumerate(individual_bills, 1):
            ratio = bill / bill_amount if bill_amount > 0 else 1 / people_count
            person_tip = total_tip * ratio
            result[f"person_{i}"] = round(bill + person_tip, 2)
        
        return result
    else:
        per_person = total / people_count
        return {f"person_{i}": round(per_person, 2) for i in range(1, people_count + 1)}


# 便捷函数
def tip(bill: float, percent: float = 18.0) -> Tuple[float, float]:
    """
    快速计算小费（便捷函数）
    
    Args:
        bill: 账单金额
        percent: 小费百分比
    
    Returns:
        (小费, 总计)
    """
    t = bill * (percent / 100)
    return round(t, 2), round(bill + t, 2)


def split(bill: float, people: int, percent: float = 18.0) -> float:
    """
    快速分割账单（便捷函数）
    
    Args:
        bill: 账单金额
        people: 人数
        percent: 小费百分比
    
    Returns:
        每人应付金额
    """
    total = bill * (1 + percent / 100)
    return round(total / people, 2)


if __name__ == "__main__":
    # 示例用法
    print("=== 小费计算器示例 ===\n")
    
    # 基本小费计算
    calc = calculate_tip(100.0, 18.0)
    print(f"账单 $100, 小费 18%: ${calc.tip_amount}, 总计 ${calc.total}")
    
    # 含税计算
    calc_with_tax = calculate_tip_with_tax(100.0, 18.0, 8.25, tip_on_pre_tax=True)
    print(f"\n含税计算 (税前 $100, 小费 18%, 税 8.25%):")
    print(f"  小费: ${calc_with_tax.tip_amount}")
    print(f"  税金: ${calc_with_tax.tax}")
    print(f"  总计: ${calc_with_tax.grand_total}")
    
    # 账单分割
    split_result = split_bill(150.0, 3, 18.0, round_up=True)
    print(f"\n分割 $150 账单给 3 人 (18% 小费):")
    print(f"  每人: ${split_result.per_person}")
    
    # 多人分摊示例
    items = [("Alice", 45.0), ("Bob", 35.0), ("Charlie", 20.0)]
    split_items = split_by_items(items, tip_percent=18.0)
    print(f"\n按消费分摊 ($100 总计, 18% 小费):")
    for name, amount in split_items.items():
        print(f"  {name}: ${amount:.2f}")
    
    # 国家小费建议
    for country in [Country.USA, Country.JAPAN, Country.FRANCE, Country.CHINA]:
        tip_amt, note = suggest_tip(100.0, country, ServiceType.RESTAURANT, "good")
        print(f"\n{country.value}: 小费 ${tip_amt:.2f} - {note}")
    
    # 快速小费计算
    print("\n快速小费参考 ($100 账单):")
    quick = calculate_quick_tips(100.0)
    for pct, calc in quick.items():
        print(f"  {pct}: ${calc.tip_amount:.2f}")
    
    # 格式化输出
    print("\n" + format_tip_summary(100.0, 18.0, 8.25, False))
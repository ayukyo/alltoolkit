"""
Bill Splitter Utils - 账单分账工具

提供账单分割、小费计算、费用分摊等功能。
零外部依赖，纯 Python 标准库实现。

功能:
- 账单均分
- 按比例分账
- 小费计算（支持多种百分比）
- 税费处理
- 多人分账（支持不等金额）
- 账单历史记录
- 支持自定义货币符号
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from decimal import Decimal, ROUND_HALF_UP
from datetime import datetime
import json


@dataclass
class Person:
    """参与分账的人员"""
    name: str
    items: List[str] = field(default_factory=list)  # 消费的项目索引
    custom_amount: Optional[Decimal] = None  # 自定义金额（如果不需要按项目计算）


@dataclass
class BillItem:
    """账单项目"""
    name: str
    price: Decimal
    shared_by: List[str] = field(default_factory=list)  # 分享此项目的人员名称
    
    def __post_init__(self):
        if isinstance(self.price, (int, float)):
            self.price = Decimal(str(self.price))


@dataclass
class SplitResult:
    """分账结果"""
    person_name: str
    subtotal: Decimal  # 小计（不含税和小费）
    tax_amount: Decimal  # 税费
    tip_amount: Decimal  # 小费
    total: Decimal  # 总计
    
    def to_dict(self) -> dict:
        return {
            'person_name': self.person_name,
            'subtotal': str(self.subtotal),
            'tax_amount': str(self.tax_amount),
            'tip_amount': str(self.tip_amount),
            'total': str(self.total)
        }


@dataclass
class BillSummary:
    """账单汇总"""
    subtotal: Decimal
    tax_rate: Decimal
    tax_amount: Decimal
    tip_rate: Decimal
    tip_amount: Decimal
    discount: Decimal
    grand_total: Decimal
    splits: List[SplitResult]
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> dict:
        return {
            'subtotal': str(self.subtotal),
            'tax_rate': str(self.tax_rate),
            'tax_amount': str(self.tax_amount),
            'tip_rate': str(self.tip_rate),
            'tip_amount': str(self.tip_amount),
            'discount': str(self.discount),
            'grand_total': str(self.grand_total),
            'splits': [s.to_dict() for s in self.splits],
            'created_at': self.created_at
        }


class BillSplitter:
    """
    账单分账器
    
    支持多种分账模式:
    1. 均分模式 - 所有人平摊费用
    2. 按项目模式 - 根据每个人消费的项目计算
    3. 自定义模式 - 每个人指定自己的金额
    4. 比例模式 - 按预设比例分摊
    
    Example:
        >>> splitter = BillSplitter()
        >>> splitter.add_item("Pizza", 30.00)
        >>> splitter.add_item("Salad", 15.00)
        >>> splitter.set_participants(["Alice", "Bob", "Charlie"])
        >>> splitter.set_tax_rate(0.10)  # 10% 税
        >>> splitter.set_tip_rate(0.15)  # 15% 小费
        >>> result = splitter.split_equally()
    """
    
    def __init__(self, currency_symbol: str = "$"):
        """
        初始化账单分账器
        
        Args:
            currency_symbol: 货币符号，默认为 "$"
        """
        self.items: List[BillItem] = []
        self.participants: List[Person] = []
        self.tax_rate: Decimal = Decimal("0")
        self.tip_rate: Decimal = Decimal("0")
        self.discount: Decimal = Decimal("0")
        self.currency_symbol = currency_symbol
        self._history: List[BillSummary] = []
    
    def add_item(self, name: str, price: float, shared_by: Optional[List[str]] = None) -> 'BillSplitter':
        """
        添加账单项目
        
        Args:
            name: 项目名称
            price: 价格
            shared_by: 分享此项目的人员列表（可选）
            
        Returns:
            self，支持链式调用
        """
        item = BillItem(name=name, price=Decimal(str(price)), shared_by=shared_by or [])
        self.items.append(item)
        return self
    
    def set_participants(self, names: List[str]) -> 'BillSplitter':
        """
        设置参与分账的人员
        
        Args:
            names: 人员名称列表
            
        Returns:
            self，支持链式调用
        """
        self.participants = [Person(name=name) for name in names]
        return self
    
    def add_participant(self, name: str, items: Optional[List[str]] = None, 
                        custom_amount: Optional[float] = None) -> 'BillSplitter':
        """
        添加一个参与者
        
        Args:
            name: 人员名称
            items: 该人消费的项目名称列表
            custom_amount: 自定义金额
            
        Returns:
            self，支持链式调用
        """
        person = Person(
            name=name,
            items=items or [],
            custom_amount=Decimal(str(custom_amount)) if custom_amount else None
        )
        self.participants.append(person)
        return self
    
    def set_tax_rate(self, rate: float) -> 'BillSplitter':
        """
        设置税率
        
        Args:
            rate: 税率（如 0.10 表示 10%）
            
        Returns:
            self，支持链式调用
        """
        self.tax_rate = Decimal(str(rate))
        return self
    
    def set_tip_rate(self, rate: float) -> 'BillSplitter':
        """
        设置小费比例
        
        Args:
            rate: 小费比例（如 0.15 表示 15%）
            
        Returns:
            self，支持链式调用
        """
        self.tip_rate = Decimal(str(rate))
        return self
    
    def set_discount(self, amount: float) -> 'BillSplitter':
        """
        设置折扣金额
        
        Args:
            amount: 折扣金额
            
        Returns:
            self，支持链式调用
        """
        self.discount = Decimal(str(amount))
        return self
    
    def _calculate_subtotal(self) -> Decimal:
        """计算小计（所有项目之和）"""
        return sum(item.price for item in self.items)
    
    def _round_money(self, amount: Decimal) -> Decimal:
        """
        四舍五入到分
        
        Args:
            amount: 金额
            
        Returns:
            四舍五入后的金额
        """
        return amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    
    def split_equally(self) -> BillSummary:
        """
        均分账单
        
        所有参与者平分总费用
        
        Returns:
            分账汇总结果
            
        Raises:
            ValueError: 如果没有参与者或项目
        """
        if not self.participants:
            raise ValueError("没有参与者，请先使用 set_participants() 设置")
        if not self.items:
            raise ValueError("没有账单项目，请先使用 add_item() 添加")
        
        subtotal = self._calculate_subtotal()
        discounted = subtotal - self.discount
        tax_amount = self._round_money(discounted * self.tax_rate)
        tip_amount = self._round_money((discounted + tax_amount) * self.tip_rate)
        grand_total = discounted + tax_amount + tip_amount
        
        num_people = len(self.participants)
        per_person = self._round_money(grand_total / num_people)
        
        splits = []
        for person in self.participants:
            person_subtotal = self._round_money(discounted / num_people)
            person_tax = self._round_money(tax_amount / num_people)
            person_tip = self._round_money(tip_amount / num_people)
            
            splits.append(SplitResult(
                person_name=person.name,
                subtotal=person_subtotal,
                tax_amount=person_tax,
                tip_amount=person_tip,
                total=per_person
            ))
        
        summary = BillSummary(
            subtotal=subtotal,
            tax_rate=self.tax_rate,
            tax_amount=tax_amount,
            tip_rate=self.tip_rate,
            tip_amount=tip_amount,
            discount=self.discount,
            grand_total=grand_total,
            splits=splits
        )
        self._history.append(summary)
        return summary
    
    def split_by_items(self) -> BillSummary:
        """
        按项目分账
        
        根据每个人消费的项目计算应付金额
        
        Returns:
            分账汇总结果
            
        Raises:
            ValueError: 如果没有参与者或项目
        """
        if not self.participants:
            raise ValueError("没有参与者，请先设置参与者")
        if not self.items:
            raise ValueError("没有账单项目，请先使用 add_item() 添加")
        
        # 计算每个人的小计
        person_subtotals: Dict[str, Decimal] = {p.name: Decimal("0") for p in self.participants}
        
        for item in self.items:
            if item.shared_by:
                # 如果项目指定了分享者，只在这些人间分
                shares = len(item.shared_by)
                per_share = self._round_money(item.price / shares)
                for name in item.shared_by:
                    if name in person_subtotals:
                        person_subtotals[name] += per_share
            else:
                # 否则按参与者消费的项目列表分
                consumers = [p for p in self.participants if item.name in p.items]
                if consumers:
                    per_consumer = self._round_money(item.price / len(consumers))
                    for person in consumers:
                        person_subtotals[person.name] += per_consumer
                else:
                    # 如果没有人消费此项目，所有人平分
                    per_person = self._round_money(item.price / len(self.participants))
                    for name in person_subtotals:
                        person_subtotals[name] += per_person
        
        # 四舍五入
        for name in person_subtotals:
            person_subtotals[name] = self._round_money(person_subtotals[name])
        
        subtotal = self._calculate_subtotal()
        discounted = subtotal - self.discount
        tax_amount = self._round_money(discounted * self.tax_rate)
        tip_amount = self._round_money((discounted + tax_amount) * self.tip_rate)
        grand_total = discounted + tax_amount + tip_amount
        
        splits = []
        total_assigned = sum(person_subtotals.values())
        
        for person in self.participants:
            person_subtotal = person_subtotals[person.name]
            # 按比例计算税费和小费
            if total_assigned > 0:
                person_tax = self._round_money(tax_amount * person_subtotal / total_assigned)
                person_tip = self._round_money(tip_amount * person_subtotal / total_assigned)
            else:
                person_tax = Decimal("0")
                person_tip = Decimal("0")
            
            person_total = person_subtotal + person_tax + person_tip
            
            splits.append(SplitResult(
                person_name=person.name,
                subtotal=person_subtotal,
                tax_amount=person_tax,
                tip_amount=person_tip,
                total=self._round_money(person_total)
            ))
        
        summary = BillSummary(
            subtotal=subtotal,
            tax_rate=self.tax_rate,
            tax_amount=tax_amount,
            tip_rate=self.tip_rate,
            tip_amount=tip_amount,
            discount=self.discount,
            grand_total=grand_total,
            splits=splits
        )
        self._history.append(summary)
        return summary
    
    def split_by_ratio(self, ratios: Dict[str, float]) -> BillSummary:
        """
        按比例分账
        
        Args:
            ratios: 人员名称到比例的映射（如 {"Alice": 0.5, "Bob": 0.3, "Charlie": 0.2}）
            
        Returns:
            分账汇总结果
            
        Raises:
            ValueError: 如果比例不匹配或没有参与者
        """
        if not self.participants:
            raise ValueError("没有参与者，请先设置参与者")
        if not self.items:
            raise ValueError("没有账单项目，请先使用 add_item() 添加")
        
        # 验证比例
        for name in ratios:
            if name not in [p.name for p in self.participants]:
                raise ValueError(f"未知参与者: {name}")
        
        # 转换为 Decimal
        decimal_ratios = {k: Decimal(str(v)) for k, v in ratios.items()}
        total_ratio = sum(decimal_ratios.values())
        
        if total_ratio <= 0:
            raise ValueError("比例总和必须大于 0")
        
        subtotal = self._calculate_subtotal()
        discounted = subtotal - self.discount
        tax_amount = self._round_money(discounted * self.tax_rate)
        tip_amount = self._round_money((discounted + tax_amount) * self.tip_rate)
        grand_total = discounted + tax_amount + tip_amount
        
        splits = []
        for person in self.participants:
            ratio = decimal_ratios.get(person.name, Decimal("0"))
            person_subtotal = self._round_money(discounted * ratio / total_ratio)
            person_tax = self._round_money(tax_amount * ratio / total_ratio)
            person_tip = self._round_money(tip_amount * ratio / total_ratio)
            person_total = self._round_money(person_subtotal + person_tax + person_tip)
            
            splits.append(SplitResult(
                person_name=person.name,
                subtotal=person_subtotal,
                tax_amount=person_tax,
                tip_amount=person_tip,
                total=person_total
            ))
        
        summary = BillSummary(
            subtotal=subtotal,
            tax_rate=self.tax_rate,
            tax_amount=tax_amount,
            tip_rate=self.tip_rate,
            tip_amount=tip_amount,
            discount=self.discount,
            grand_total=grand_total,
            splits=splits
        )
        self._history.append(summary)
        return summary
    
    def split_custom(self) -> BillSummary:
        """
        自定义金额分账
        
        根据每个参与者设置的 custom_amount 进行分账
        
        Returns:
            分账汇总结果
            
        Raises:
            ValueError: 如果没有参与者或有人未设置自定义金额
        """
        if not self.participants:
            raise ValueError("没有参与者，请先设置参与者")
        
        # 验证每个人都设置了自定义金额
        for person in self.participants:
            if person.custom_amount is None:
                raise ValueError(f"参与者 {person.name} 未设置自定义金额")
        
        subtotal = self._calculate_subtotal()
        tax_amount = self._round_money(subtotal * self.tax_rate)
        tip_amount = self._round_money((subtotal + tax_amount) * self.tip_rate)
        grand_total = subtotal + tax_amount + tip_amount
        
        # 计算自定义金额总和
        total_custom = sum(p.custom_amount for p in self.participants)
        
        splits = []
        for person in self.participants:
            ratio = person.custom_amount / total_custom if total_custom > 0 else Decimal("0")
            person_subtotal = person.custom_amount
            person_tax = self._round_money(tax_amount * ratio)
            person_tip = self._round_money(tip_amount * ratio)
            person_total = self._round_money(person_subtotal + person_tax + person_tip)
            
            splits.append(SplitResult(
                person_name=person.name,
                subtotal=person_subtotal,
                tax_amount=person_tax,
                tip_amount=person_tip,
                total=person_total
            ))
        
        summary = BillSummary(
            subtotal=subtotal,
            tax_rate=self.tax_rate,
            tax_amount=tax_amount,
            tip_rate=self.tip_rate,
            tip_amount=tip_amount,
            discount=self.discount,
            grand_total=grand_total,
            splits=splits
        )
        self._history.append(summary)
        return summary
    
    def get_history(self) -> List[BillSummary]:
        """获取分账历史"""
        return self._history.copy()
    
    def clear(self) -> 'BillSplitter':
        """
        清空当前账单（保留历史）
        
        Returns:
            self，支持链式调用
        """
        self.items = []
        self.participants = []
        self.tax_rate = Decimal("0")
        self.tip_rate = Decimal("0")
        self.discount = Decimal("0")
        return self
    
    def clear_history(self) -> 'BillSplitter':
        """
        清空历史记录
        
        Returns:
            self，支持链式调用
        """
        self._history = []
        return self
    
    def format_summary(self, summary: BillSummary) -> str:
        """
        格式化输出分账结果
        
        Args:
            summary: 分账汇总
            
        Returns:
            格式化的字符串
        """
        lines = [
            "═" * 40,
            "              账单汇总",
            "═" * 40,
            f"小计:     {self.currency_symbol}{summary.subtotal:.2f}",
            f"折扣:    -{self.currency_symbol}{summary.discount:.2f}",
            f"税费 ({float(summary.tax_rate)*100:.1f}%):  {self.currency_symbol}{summary.tax_amount:.2f}",
            f"小费 ({float(summary.tip_rate)*100:.1f}%):  {self.currency_symbol}{summary.tip_amount:.2f}",
            "-" * 40,
            f"总计:     {self.currency_symbol}{summary.grand_total:.2f}",
            "═" * 40,
            "",
            "              分账明细",
            "═" * 40,
        ]
        
        for split in summary.splits:
            lines.append(f"  {split.person_name}:")
            lines.append(f"    小计: {self.currency_symbol}{split.subtotal:.2f}")
            lines.append(f"    税费: {self.currency_symbol}{split.tax_amount:.2f}")
            lines.append(f"    小费: {self.currency_symbol}{split.tip_amount:.2f}")
            lines.append(f"    总计: {self.currency_symbol}{split.total:.2f}")
            lines.append("-" * 40)
        
        return "\n".join(lines)


# ============= 便捷函数 =============

def split_bill_equally(total: float, num_people: int, tax_rate: float = 0, 
                       tip_rate: float = 0) -> Dict[str, float]:
    """
    快速均分账单
    
    Args:
        total: 账单总额
        num_people: 人数
        tax_rate: 税率（默认0）
        tip_rate: 小费比例（默认0）
        
    Returns:
        包含分账详情的字典
        
    Example:
        >>> split_bill_equally(100, 4, tax_rate=0.1, tip_rate=0.15)
        {'per_person': 28.75, 'subtotal': 100.0, 'tax': 10.0, 'tip': 16.5, 'total': 115.0}
    """
    from decimal import Decimal
    subtotal = Decimal(str(total))
    tax = subtotal * Decimal(str(tax_rate))
    tip = (subtotal + tax) * Decimal(str(tip_rate))
    grand_total = subtotal + tax + tip
    per_person = grand_total / num_people
    
    return {
        'per_person': float(per_person.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)),
        'subtotal': float(subtotal),
        'tax': float(tax.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)),
        'tip': float(tip.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)),
        'total': float(grand_total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))
    }


def calculate_tip(amount: float, tip_rate: float) -> float:
    """
    计算小费
    
    Args:
        amount: 金额
        tip_rate: 小费比例（如 0.15 表示 15%）
        
    Returns:
        小费金额
        
    Example:
        >>> calculate_tip(100, 0.15)
        15.0
    """
    return round(amount * tip_rate, 2)


def suggest_tip(amount: float) -> Dict[str, float]:
    """
    根据金额建议小费
    
    Args:
        amount: 账单金额
        
    Returns:
        不同小费比例的建议
        
    Example:
        >>> suggest_tip(100)
        {'15%': 15.0, '18%': 18.0, '20%': 20.0, '22%': 22.0}
    """
    rates = [0.15, 0.18, 0.20, 0.22]
    suggestions = {}
    for rate in rates:
        suggestions[f"{int(rate*100)}%"] = round(amount * rate, 2)
    return suggestions


def split_with_tip(subtotal: float, num_people: int, tip_rate: float) -> float:
    """
    计算含小费的人均金额
    
    Args:
        subtotal: 小计
        num_people: 人数
        tip_rate: 小费比例
        
    Returns:
        人均金额
        
    Example:
        >>> split_with_tip(100, 4, 0.15)
        28.75
    """
    total = subtotal * (1 + tip_rate)
    return round(total / num_people, 2)


def calculate_split_with_different_items(
    items: List[Dict[str, any]],
    participants: List[str],
    tax_rate: float = 0,
    tip_rate: float = 0
) -> Dict[str, float]:
    """
    根据不同项目计算分账
    
    Args:
        items: 项目列表，每项为 {"name": str, "price": float, "shared_by": List[str]}
        participants: 参与者列表
        tax_rate: 税率
        tip_rate: 小费比例
        
    Returns:
        每人应付金额
        
    Example:
        >>> items = [
        ...     {"name": "Pizza", "price": 30, "shared_by": ["Alice", "Bob"]},
        ...     {"name": "Salad", "price": 15, "shared_by": ["Charlie"]}
        ... ]
        >>> calculate_split_with_different_items(items, ["Alice", "Bob", "Charlie"])
        {'Alice': 15.0, 'Bob': 15.0, 'Charlie': 15.0}
    """
    splitter = BillSplitter()
    splitter.set_participants(participants)
    splitter.set_tax_rate(tax_rate)
    splitter.set_tip_rate(tip_rate)
    
    for item in items:
        splitter.add_item(item["name"], item["price"], item.get("shared_by", []))
    
    summary = splitter.split_by_items()
    return {s.person_name: float(s.total) for s in summary.splits}


def format_currency(amount: float, symbol: str = "$") -> str:
    """
    格式化货币
    
    Args:
        amount: 金额
        symbol: 货币符号
        
    Returns:
        格式化后的货币字符串
        
    Example:
        >>> format_currency(123.45)
        '$123.45'
    """
    return f"{symbol}{amount:.2f}"


def parse_currency(value: str) -> float:
    """
    解析货币字符串
    
    Args:
        value: 货币字符串（如 "$123.45" 或 "¥100"）
        
    Returns:
        金额数值
        
    Example:
        >>> parse_currency("$123.45")
        123.45
        >>> parse_currency("¥100")
        100.0
    """
    import re
    # 移除货币符号和逗号，保留数字、小数点和负号
    # 使用更精确的正则：移除开头的货币符号，然后清理千位分隔符
    cleaned = value.strip()
    # 移除常见货币符号
    cleaned = re.sub(r'^[$¥€£₹₽₩₪₴฿₡₫₭₮₯₰₱₲₳₵₶₷₸₹₺₻₼₽₾₿]+\s*', '', cleaned)
    # 移除千位分隔符逗号
    cleaned = cleaned.replace(',', '')
    return float(cleaned) if cleaned else 0.0
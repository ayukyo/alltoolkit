"""
Menstrual Cycle Calculator - 月经周期计算工具

功能：
- 计算月经周期各阶段（月经期、卵泡期、排卵期、黄体期）
- 预测下次月经日期
- 计算排卵日和易孕期
- 计算安全期和危险期
- 周期规律性分析
- 多周期预测

零外部依赖，纯 Python 实现
"""

from datetime import datetime, timedelta
from typing import Optional, List, Dict, Tuple
from dataclasses import dataclass
from enum import Enum


class CyclePhase(Enum):
    """月经周期阶段"""
    MENSTRUAL = "menstrual"      # 月经期
    FOLLICULAR = "follicular"    # 卵泡期
    OVULATION = "ovulation"      # 排卵期
    LUTEAL = "luteal"           # 黄体期


class FertilityLevel(Enum):
    """生育能力等级"""
    LOW = "low"           # 低（安全期）
    MEDIUM = "medium"     # 中等
    HIGH = "high"         # 高（易孕期）


@dataclass
class CycleDay:
    """周期某天的详细信息"""
    date: datetime
    day_of_cycle: int           # 周期第几天
    phase: CyclePhase           # 当前阶段
    fertility: FertilityLevel   # 生育能力等级
    is_period: bool             # 是否经期
    is_ovulation: bool          # 是否排卵日
    is_fertile: bool            # 是否易孕期
    is_safe: bool               # 是否安全期
    description: str            # 描述


@dataclass
class CyclePrediction:
    """周期预测结果"""
    next_period_start: datetime    # 下次月经开始日期
    next_period_end: datetime      # 下次月经结束日期
    ovulation_date: datetime       # 排卵日
    fertile_window_start: datetime # 易孕期开始
    fertile_window_end: datetime   # 易孕期结束
    safe_days_before: Tuple[datetime, datetime]  # 经期后安全期
    safe_days_after: Tuple[datetime, datetime]   # 经期前安全期


@dataclass
class CycleAnalysis:
    """周期规律性分析"""
    average_length: float          # 平均周期长度
    min_length: int                # 最短周期
    max_length: int                # 最长周期
    variance: float                # 周期方差
    is_regular: bool               # 是否规律
    regularity_score: float        # 规律性评分 (0-100)


class MenstrualCycleCalculator:
    """月经周期计算器"""
    
    # 默认参数
    DEFAULT_CYCLE_LENGTH = 28      # 默认周期长度
    DEFAULT_PERIOD_LENGTH = 5      # 默认经期长度
    DEFAULT_LUTEAL_LENGTH = 14     # 黄体期长度（固定）
    OVULATION_WINDOW = 2           # 排卵窗口（前后各2天）
    
    # 规律性判断标准
    REGULAR_THRESHOLD = 7          # 周期波动小于7天视为规律
    
    def __init__(
        self,
        last_period_start: datetime,
        cycle_length: int = DEFAULT_CYCLE_LENGTH,
        period_length: int = DEFAULT_PERIOD_LENGTH,
        cycle_history: Optional[List[int]] = None
    ):
        """
        初始化月经周期计算器
        
        Args:
            last_period_start: 上次月经开始日期
            cycle_length: 周期长度（天数）
            period_length: 经期长度（天数）
            cycle_history: 历史周期长度列表，用于分析规律性
        """
        self.last_period_start = last_period_start
        self.cycle_length = cycle_length
        self.period_length = period_length
        self.cycle_history = cycle_history or []
        
    def get_phase(self, day_of_cycle: int) -> CyclePhase:
        """
        根据周期天数获取当前阶段
        
        Args:
            day_of_cycle: 周期第几天（1开始）
            
        Returns:
            CyclePhase: 当前阶段
        """
        # 排卵日 = 周期长度 - 黄体期长度
        ovulation_day = self.cycle_length - self.DEFAULT_LUTEAL_LENGTH
        ovulation_start = ovulation_day - self.OVULATION_WINDOW
        ovulation_end = ovulation_day + self.OVULATION_WINDOW
        
        if day_of_cycle <= self.period_length:
            return CyclePhase.MENSTRUAL
        elif day_of_cycle < ovulation_start:
            return CyclePhase.FOLLICULAR
        elif day_of_cycle <= ovulation_end:
            return CyclePhase.OVULATION
        else:
            return CyclePhase.LUTEAL
    
    def get_fertility(self, day_of_cycle: int) -> FertilityLevel:
        """
        获取生育能力等级
        
        Args:
            day_of_cycle: 周期第几天
            
        Returns:
            FertilityLevel: 生育能力等级
        """
        ovulation_day = self.cycle_length - self.DEFAULT_LUTEAL_LENGTH
        ovulation_start = ovulation_day - self.OVULATION_WINDOW
        ovulation_end = ovulation_day + self.OVULATION_WINDOW
        
        # 易孕期：排卵日前5天到排卵日后1天
        fertile_start = ovulation_day - 5
        fertile_end = ovulation_day + 1
        
        if fertile_start <= day_of_cycle <= fertile_end:
            if ovulation_start <= day_of_cycle <= ovulation_end:
                return FertilityLevel.HIGH
            return FertilityLevel.MEDIUM
        else:
            return FertilityLevel.LOW
    
    def is_safe_day(self, day_of_cycle: int) -> bool:
        """
        判断是否为安全期
        
        安全期计算规则：
        - 经期后安全期：经期结束后的前几天（排卵前）
        - 经期前安全期：下次月经前的一周（黄体期后半段）
        
        Args:
            day_of_cycle: 周期第几天
            
        Returns:
            bool: 是否为安全期
        """
        fertility = self.get_fertility(day_of_cycle)
        return fertility == FertilityLevel.LOW and not self.is_period_day(day_of_cycle)
    
    def is_period_day(self, day_of_cycle: int) -> bool:
        """判断是否为经期"""
        return 1 <= day_of_cycle <= self.period_length
    
    def is_ovulation_day(self, day_of_cycle: int) -> bool:
        """判断是否为排卵日"""
        ovulation_day = self.cycle_length - self.DEFAULT_LUTEAL_LENGTH
        return day_of_cycle == ovulation_day
    
    def is_fertile_day(self, day_of_cycle: int) -> bool:
        """判断是否为易孕期"""
        fertility = self.get_fertility(day_of_cycle)
        return fertility in (FertilityLevel.HIGH, FertilityLevel.MEDIUM)
    
    def get_day_info(self, date: datetime) -> CycleDay:
        """
        获取某天的详细信息
        
        Args:
            date: 查询日期
            
        Returns:
            CycleDay: 该天的详细信息
        """
        days_diff = (date - self.last_period_start).days
        day_of_cycle = (days_diff % self.cycle_length) + 1
        
        phase = self.get_phase(day_of_cycle)
        fertility = self.get_fertility(day_of_cycle)
        is_period = self.is_period_day(day_of_cycle)
        is_ovulation = self.is_ovulation_day(day_of_cycle)
        is_fertile = self.is_fertile_day(day_of_cycle)
        is_safe = self.is_safe_day(day_of_cycle)
        
        # 生成描述
        descriptions = {
            CyclePhase.MENSTRUAL: "月经期",
            CyclePhase.FOLLICULAR: "卵泡期",
            CyclePhase.OVULATION: "排卵期",
            CyclePhase.LUTEAL: "黄体期"
        }
        
        desc_parts = [f"周期第{day_of_cycle}天", descriptions[phase]]
        if is_period:
            desc_parts.append("经期中")
        if is_ovulation:
            desc_parts.append("排卵日")
        if is_fertile:
            desc_parts.append("易孕期")
        if is_safe:
            desc_parts.append("安全期")
        
        return CycleDay(
            date=date,
            day_of_cycle=day_of_cycle,
            phase=phase,
            fertility=fertility,
            is_period=is_period,
            is_ovulation=is_ovulation,
            is_fertile=is_fertile,
            is_safe=is_safe,
            description=" | ".join(desc_parts)
        )
    
    def predict(self) -> CyclePrediction:
        """
        预测下一个周期
        
        Returns:
            CyclePrediction: 预测结果
        """
        # 下次月经
        next_period_start = self.last_period_start + timedelta(days=self.cycle_length)
        next_period_end = next_period_start + timedelta(days=self.period_length - 1)
        
        # 排卵日
        ovulation_day = self.cycle_length - self.DEFAULT_LUTEAL_LENGTH
        ovulation_date = self.last_period_start + timedelta(days=ovulation_day)
        
        # 易孕期窗口（排卵前5天到排卵后1天）
        fertile_start = ovulation_date - timedelta(days=5)
        fertile_end = ovulation_date + timedelta(days=1)
        
        # 安全期
        # 经期后安全期：经期结束后到易孕期开始前
        safe_before_start = self.last_period_start + timedelta(days=self.period_length)
        safe_before_end = fertile_start - timedelta(days=1)
        
        # 经期前安全期：易孕期结束后到下次月经前
        safe_after_start = fertile_end + timedelta(days=1)
        safe_after_end = next_period_start - timedelta(days=1)
        
        return CyclePrediction(
            next_period_start=next_period_start,
            next_period_end=next_period_end,
            ovulation_date=ovulation_date,
            fertile_window_start=fertile_start,
            fertile_window_end=fertile_end,
            safe_days_before=(safe_before_start, safe_before_end),
            safe_days_after=(safe_after_start, safe_after_end)
        )
    
    def predict_multiple(self, num_cycles: int = 3) -> List[CyclePrediction]:
        """
        预测多个周期
        
        Args:
            num_cycles: 预测周期数
            
        Returns:
            List[CyclePrediction]: 预测结果列表
        """
        predictions = []
        current_start = self.last_period_start
        
        for _ in range(num_cycles):
            calc = MenstrualCycleCalculator(
                current_start,
                self.cycle_length,
                self.period_length
            )
            pred = calc.predict()
            predictions.append(pred)
            current_start = pred.next_period_start
        
        return predictions
    
    def analyze_regularity(self) -> CycleAnalysis:
        """
        分析周期规律性
        
        Returns:
            CycleAnalysis: 规律性分析结果
        """
        if len(self.cycle_history) < 2:
            return CycleAnalysis(
                average_length=self.cycle_length,
                min_length=self.cycle_length,
                max_length=self.cycle_length,
                variance=0,
                is_regular=True,
                regularity_score=100
            )
        
        avg = sum(self.cycle_history) / len(self.cycle_history)
        min_len = min(self.cycle_history)
        max_len = max(self.cycle_history)
        variance = sum((x - avg) ** 2 for x in self.cycle_history) / len(self.cycle_history)
        
        # 计算规律性评分
        range_len = max_len - min_len
        regularity_score = max(0, 100 - (range_len * 10))
        is_regular = range_len <= self.REGULAR_THRESHOLD
        
        return CycleAnalysis(
            average_length=round(avg, 1),
            min_length=min_len,
            max_length=max_len,
            variance=round(variance, 2),
            is_regular=is_regular,
            regularity_score=round(regularity_score, 1)
        )
    
    def get_cycle_calendar(
        self,
        start_date: Optional[datetime] = None,
        num_days: int = 30
    ) -> List[CycleDay]:
        """
        获取周期日历
        
        Args:
            start_date: 开始日期，默认为今天
            num_days: 天数
            
        Returns:
            List[CycleDay]: 日历列表
        """
        if start_date is None:
            start_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        
        calendar = []
        for i in range(num_days):
            date = start_date + timedelta(days=i)
            calendar.append(self.get_day_info(date))
        
        return calendar
    
    def get_phase_description(self, phase: CyclePhase) -> str:
        """获取阶段描述"""
        descriptions = {
            CyclePhase.MENSTRUAL: "月经期：子宫内膜脱落出血，持续3-7天。身体可能感到疲惫、腹痛。",
            CyclePhase.FOLLICULAR: "卵泡期：卵泡发育成熟，雌激素水平上升。精力充沛，适合运动。",
            CyclePhase.OVULATION: "排卵期：卵子释放，最容易受孕。性欲可能增强，体温略有上升。",
            CyclePhase.LUTEAL: "黄体期：黄体形成，孕激素上升。可能出现经前综合征症状。"
        }
        return descriptions.get(phase, "")
    
    def get_recommendations(self, date: datetime) -> Dict[str, List[str]]:
        """
        获取某天的建议
        
        Args:
            date: 查询日期
            
        Returns:
            Dict: 各类建议
        """
        day_info = self.get_day_info(date)
        
        recommendations = {
            "饮食": [],
            "运动": [],
            "生活": []
        }
        
        if day_info.phase == CyclePhase.MENSTRUAL:
            recommendations["饮食"] = [
                "多吃富含铁的食物，如红肉、菠菜",
                "避免生冷食物",
                "补充维生素B族"
            ]
            recommendations["运动"] = [
                "适合轻度运动，如散步、瑜伽",
                "避免剧烈运动"
            ]
            recommendations["生活"] = [
                "注意休息",
                "保持心情愉悦",
                "注意保暖"
            ]
        elif day_info.phase == CyclePhase.FOLLICULAR:
            recommendations["饮食"] = [
                "增加蛋白质摄入",
                "多吃新鲜蔬果"
            ]
            recommendations["运动"] = [
                "适合中高强度运动",
                "是锻炼的好时机"
            ]
            recommendations["生活"] = [
                "精力充沛，适合社交",
                "皮肤状态较好"
            ]
        elif day_info.phase == CyclePhase.OVULATION:
            recommendations["饮食"] = [
                "保持均衡饮食",
                "避免过度刺激性食物"
            ]
            recommendations["运动"] = [
                "能量充沛，适合运动",
                "可以进行力量训练"
            ]
            recommendations["生活"] = [
                "注意避孕或备孕计划",
                "可能情绪波动"
            ]
        else:  # LUTEAL
            recommendations["饮食"] = [
                "减少盐分摄入，预防水肿",
                "补充钙镁缓解症状",
                "避免咖啡因和酒精"
            ]
            recommendations["运动"] = [
                "适合舒缓运动",
                "瑜伽、冥想有帮助"
            ]
            recommendations["生活"] = [
                "可能出现经前综合征",
                "保证充足睡眠",
                "注意情绪管理"
            ]
        
        return recommendations


# 便捷函数
def calculate_next_period(
    last_period: datetime,
    cycle_length: int = 28,
    period_length: int = 5
) -> Tuple[datetime, datetime]:
    """
    计算下次月经日期
    
    Args:
        last_period: 上次月经开始日期
        cycle_length: 周期长度
        period_length: 经期长度
        
    Returns:
        Tuple[datetime, datetime]: (下次月经开始日期, 下次月经结束日期)
    """
    calc = MenstrualCycleCalculator(last_period, cycle_length, period_length)
    pred = calc.predict()
    return pred.next_period_start, pred.next_period_end


def get_fertile_days(
    last_period: datetime,
    cycle_length: int = 28
) -> Tuple[datetime, datetime]:
    """
    获取易孕期日期范围
    
    Args:
        last_period: 上次月经开始日期
        cycle_length: 周期长度
        
    Returns:
        Tuple[datetime, datetime]: (易孕期开始日期, 易孕期结束日期)
    """
    calc = MenstrualCycleCalculator(last_period, cycle_length)
    pred = calc.predict()
    return pred.fertile_window_start, pred.fertile_window_end


def get_ovulation_date(
    last_period: datetime,
    cycle_length: int = 28
) -> datetime:
    """
    获取排卵日期
    
    Args:
        last_period: 上次月经开始日期
        cycle_length: 周期长度
        
    Returns:
        datetime: 排卵日期
    """
    calc = MenstrualCycleCalculator(last_period, cycle_length)
    pred = calc.predict()
    return pred.ovulation_date


def format_date(date: datetime) -> str:
    """格式化日期"""
    return date.strftime("%Y-%m-%d")


# 示例用法
if __name__ == "__main__":
    # 示例：使用今天作为参考
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    
    # 假设上次月经是20天前，周期28天
    last_period = today - timedelta(days=20)
    
    calc = MenstrualCycleCalculator(last_period, cycle_length=28, period_length=5)
    
    # 预测下一个周期
    pred = calc.predict()
    print("=" * 50)
    print("月经周期预测")
    print("=" * 50)
    print(f"上次月经: {format_date(last_period)}")
    print(f"下次月经: {format_date(pred.next_period_start)} - {format_date(pred.next_period_end)}")
    print(f"排卵日: {format_date(pred.ovulation_date)}")
    print(f"易孕期: {format_date(pred.fertile_window_start)} - {format_date(pred.fertile_window_end)}")
    print(f"安全期(前): {format_date(pred.safe_days_before[0])} - {format_date(pred.safe_days_before[1])}")
    print(f"安全期(后): {format_date(pred.safe_days_after[0])} - {format_date(pred.safe_days_after[1])}")
    
    # 今天的状态
    print("\n" + "=" * 50)
    print("今日状态")
    print("=" * 50)
    today_info = calc.get_day_info(today)
    print(f"日期: {format_date(today)}")
    print(f"周期第{today_info.day_of_cycle}天")
    print(f"阶段: {today_info.phase.value}")
    print(f"生育能力: {today_info.fertility.value}")
    print(f"描述: {today_info.description}")
    
    # 获取建议
    recommendations = calc.get_recommendations(today)
    print("\n建议:")
    for category, items in recommendations.items():
        print(f"  {category}:")
        for item in items:
            print(f"    - {item}")
    
    # 分析周期规律性（使用模拟的历史数据）
    print("\n" + "=" * 50)
    print("周期规律性分析")
    print("=" * 50)
    history = [27, 28, 29, 28, 27, 28, 30, 28]
    calc_with_history = MenstrualCycleCalculator(
        last_period,
        cycle_length=28,
        period_length=5,
        cycle_history=history
    )
    analysis = calc_with_history.analyze_regularity()
    print(f"历史周期: {history}")
    print(f"平均周期: {analysis.average_length} 天")
    print(f"最短周期: {analysis.min_length} 天")
    print(f"最长周期: {analysis.max_length} 天")
    print(f"周期波动: {analysis.max_length - analysis.min_length} 天")
    print(f"规律性评分: {analysis.regularity_score}/100")
    print(f"是否规律: {'是' if analysis.is_regular else '否'}")
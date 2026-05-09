"""
lottery_utils - 中国彩票工具模块

提供中国主流彩票（双色球、大乐透、排列三/五）的号码生成、中奖计算、概率分析等功能。
零外部依赖，纯 Python 标准库实现。

支持的彩票类型：
- 双色球 (SSQ): 6红球(1-33) + 1蓝球(1-16)
- 大乐透 (DLT): 5前区(1-35) + 2后区(1-12)
- 排列三 (P3): 3位数字(0-9)
- 排列五 (P5): 5位数字(0-9)
- 七星彩 (QXC): 7位数字(0-9)

Author: AllToolkit
Date: 2026-05-09
"""

import random
import hashlib
from typing import List, Tuple, Dict, Optional, Any
from dataclasses import dataclass
from enum import Enum
from datetime import datetime
from collections import Counter
import json


class LotteryType(Enum):
    """彩票类型枚举"""
    SSQ = "双色球"       # 双色球
    DLT = "大乐透"       # 大乐透
    P3 = "排列三"        # 排列三
    P5 = "排列五"        # 排列五
    QXC = "七星彩"       # 七星彩


@dataclass
class LotteryResult:
    """彩票开奖结果"""
    lottery_type: LotteryType
    numbers: List[int]
    special_numbers: List[int]  # 特别号码（蓝球、后区等）
    draw_date: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "lottery_type": self.lottery_type.value,
            "numbers": self.numbers,
            "special_numbers": self.special_numbers,
            "draw_date": self.draw_date
        }
    
    def __str__(self) -> str:
        if self.special_numbers:
            main = " ".join(map(str, sorted(self.numbers)))
            special = " ".join(map(str, self.special_numbers))
            return f"{self.lottery_type.value}: {main} + {special}"
        else:
            return f"{self.lottery_type.value}: {' '.join(map(str, self.numbers))}"


@dataclass
class PrizeInfo:
    """中奖信息"""
    prize_level: int
    prize_name: str
    prize_amount: int  # 奖金（分）
    match_count: int   # 中奖号码数量
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "prize_level": self.prize_level,
            "prize_name": self.prize_name,
            "prize_amount": self.prize_amount,
            "match_count": self.match_count
        }


class SSQUtils:
    """双色球工具类
    
    规则：
    - 红球：从01-33中选择6个（不重复）
    - 蓝球：从01-16中选择1个
    """
    
    RED_MIN, RED_MAX = 1, 33
    BLUE_MIN, BLUE_MAX = 1, 16
    RED_COUNT = 6
    BLUE_COUNT = 1
    
    # 奖项配置 (匹配红球数, 匹配蓝球数) -> (奖项名称, 默认奖金/分)
    PRIZE_TABLE = {
        (6, 1): ("一等奖", 5_0000_0000),   # 500万
        (6, 0): ("二等奖", 100_0000),       # 100万
        (5, 1): ("三等奖", 3000_00),        # 3000
        (5, 0): ("四等奖", 200_00),         # 200
        (4, 1): ("四等奖", 200_00),         # 200
        (4, 0): ("五等奖", 10_00),          # 10
        (3, 1): ("五等奖", 10_00),          # 10
        (2, 1): ("六等奖", 5_00),           # 5
        (1, 1): ("六等奖", 5_00),           # 5
        (0, 1): ("六等奖", 5_00),           # 5
    }
    
    @classmethod
    def generate(cls, seed: Optional[int] = None) -> LotteryResult:
        """生成一组双色球号码
        
        Args:
            seed: 随机种子，用于可重复生成
            
        Returns:
            LotteryResult: 生成的号码
        """
        rng = random.Random(seed) if seed is not None else random
        
        red_balls = sorted(rng.sample(range(cls.RED_MIN, cls.RED_MAX + 1), cls.RED_COUNT))
        blue_ball = [rng.randint(cls.BLUE_MIN, cls.BLUE_MAX)]
        
        return LotteryResult(
            lottery_type=LotteryType.SSQ,
            numbers=red_balls,
            special_numbers=blue_ball
        )
    
    @classmethod
    def generate_multiple(cls, count: int = 5, seed: Optional[int] = None) -> List[LotteryResult]:
        """生成多组号码
        
        Args:
            count: 生成组数
            seed: 随机种子
            
        Returns:
            List[LotteryResult]: 号码列表
        """
        return [cls.generate(seed + i if seed else None) for i in range(count)]
    
    @classmethod
    def check_prize(cls, my_numbers: LotteryResult, winning_numbers: LotteryResult) -> Optional[PrizeInfo]:
        """检查中奖情况
        
        Args:
            my_numbers: 我的号码
            winning_numbers: 开奖号码
            
        Returns:
            Optional[PrizeInfo]: 中奖信息，未中奖返回 None
        """
        if my_numbers.lottery_type != LotteryType.SSQ or winning_numbers.lottery_type != LotteryType.SSQ:
            raise ValueError("必须是双色球号码")
        
        my_red = set(my_numbers.numbers)
        my_blue = set(my_numbers.special_numbers)
        win_red = set(winning_numbers.numbers)
        win_blue = set(winning_numbers.special_numbers)
        
        red_match = len(my_red & win_red)
        blue_match = len(my_blue & win_blue)
        
        key = (red_match, blue_match)
        if key in cls.PRIZE_TABLE:
            name, amount = cls.PRIZE_TABLE[key]
            return PrizeInfo(
                prize_level=list(cls.PRIZE_TABLE.keys()).index(key) + 1,
                prize_name=name,
                prize_amount=amount,
                match_count=red_match + blue_match
            )
        return None
    
    @classmethod
    def calculate_probability(cls, prize_level: int) -> float:
        """计算指定奖项的中奖概率
        
        Args:
            prize_level: 奖项等级 (1-6)
            
        Returns:
            float: 中奖概率
        """
        # 总组合数
        total = cls._combination(33, 6) * 16
        
        prize_counts = {
            1: cls._combination(6, 6) * cls._combination(27, 0) * 1,  # 一等奖
            2: cls._combination(6, 6) * cls._combination(27, 0) * 15,  # 二等奖
            3: cls._combination(6, 5) * cls._combination(27, 1) * 1,  # 三等奖
            4: cls._combination(6, 5) * cls._combination(27, 1) * 15 + cls._combination(6, 4) * cls._combination(27, 2) * 1,  # 四等奖
            5: cls._combination(6, 4) * cls._combination(27, 2) * 15 + cls._combination(6, 3) * cls._combination(27, 3) * 1,  # 五等奖
            6: (cls._combination(6, 2) * cls._combination(27, 4) + cls._combination(6, 1) * cls._combination(27, 5) + cls._combination(6, 0) * cls._combination(27, 6)) * 1,  # 六等奖
        }
        
        if prize_level in prize_counts:
            return prize_counts[prize_level] / total
        return 0.0
    
    @staticmethod
    def _combination(n: int, r: int) -> int:
        """计算组合数 C(n, r)"""
        if r > n or r < 0:
            return 0
        if r == 0 or r == n:
            return 1
        r = min(r, n - r)
        result = 1
        for i in range(r):
            result = result * (n - i) // (i + 1)
        return result


class DLTUtils:
    """大乐透工具类
    
    规则：
    - 前区：从01-35中选择5个（不重复）
    - 后区：从01-12中选择2个（不重复）
    """
    
    FRONT_MIN, FRONT_MAX = 1, 35
    BACK_MIN, BACK_MAX = 1, 12
    FRONT_COUNT = 5
    BACK_COUNT = 2
    
    # 奖项配置 (匹配前区数, 匹配后区数) -> (奖项名称, 默认奖金/分)
    PRIZE_TABLE = {
        (5, 2): ("一等奖", 10_0000_0000),  # 1000万
        (5, 1): ("二等奖", 100_0000),       # 100万
        (5, 0): ("三等奖", 10_0000),        # 10万
        (4, 2): ("四等奖", 3000_00),        # 3000
        (4, 1): ("五等奖", 300_00),         # 300
        (3, 2): ("五等奖", 300_00),        # 300
        (4, 0): ("六等奖", 200_00),        # 200
        (3, 1): ("六等奖", 200_00),        # 200
        (2, 2): ("六等奖", 200_00),        # 200
        (3, 0): ("七等奖", 10_00),         # 10
        (2, 1): ("七等奖", 10_00),         # 10
        (1, 2): ("七等奖", 10_00),         # 10
        (1, 1): ("八等奖", 5_00),          # 5
        (0, 2): ("八等奖", 5_00),          # 5
    }
    
    @classmethod
    def generate(cls, seed: Optional[int] = None) -> LotteryResult:
        """生成一组大乐透号码"""
        rng = random.Random(seed) if seed is not None else random
        
        front_balls = sorted(rng.sample(range(cls.FRONT_MIN, cls.FRONT_MAX + 1), cls.FRONT_COUNT))
        back_balls = sorted(rng.sample(range(cls.BACK_MIN, cls.BACK_MAX + 1), cls.BACK_COUNT))
        
        return LotteryResult(
            lottery_type=LotteryType.DLT,
            numbers=front_balls,
            special_numbers=back_balls
        )
    
    @classmethod
    def generate_multiple(cls, count: int = 5, seed: Optional[int] = None) -> List[LotteryResult]:
        """生成多组号码"""
        return [cls.generate(seed + i if seed else None) for i in range(count)]
    
    @classmethod
    def check_prize(cls, my_numbers: LotteryResult, winning_numbers: LotteryResult) -> Optional[PrizeInfo]:
        """检查中奖情况"""
        if my_numbers.lottery_type != LotteryType.DLT or winning_numbers.lottery_type != LotteryType.DLT:
            raise ValueError("必须是大乐透号码")
        
        my_front = set(my_numbers.numbers)
        my_back = set(my_numbers.special_numbers)
        win_front = set(winning_numbers.numbers)
        win_back = set(winning_numbers.special_numbers)
        
        front_match = len(my_front & win_front)
        back_match = len(my_back & win_back)
        
        key = (front_match, back_match)
        if key in cls.PRIZE_TABLE:
            name, amount = cls.PRIZE_TABLE[key]
            return PrizeInfo(
                prize_level=list(cls.PRIZE_TABLE.keys()).index(key) + 1,
                prize_name=name,
                prize_amount=amount,
                match_count=front_match + back_match
            )
        return None
    
    @staticmethod
    def _comb(n: int, r: int) -> int:
        """计算组合数 C(n, r)"""
        if r > n or r < 0:
            return 0
        if r == 0 or r == n:
            return 1
        r = min(r, n - r)
        result = 1
        for i in range(r):
            result = result * (n - i) // (i + 1)
        return result
    
    @classmethod
    def calculate_probability(cls, prize_level: int) -> float:
        """计算指定奖项的中奖概率"""
        comb = cls._comb
        
        # 总组合数
        total = comb(35, 5) * comb(12, 2)
        
        # 各奖项组合数
        prize_counts = {
            1: comb(5, 5) * comb(30, 0) * comb(2, 2),  # 一等奖
            2: comb(5, 5) * comb(30, 0) * comb(2, 1) * comb(10, 1),  # 二等奖
            3: comb(5, 5) * comb(30, 0) * comb(2, 0) * comb(10, 2),  # 三等奖
            4: comb(5, 4) * comb(30, 1) * comb(2, 2),  # 四等奖
            5: comb(5, 4) * comb(30, 1) * comb(2, 1) * comb(10, 1) + comb(5, 3) * comb(30, 2) * comb(2, 2),  # 五等奖
            6: comb(5, 4) * comb(30, 1) * comb(2, 0) * comb(10, 2) + comb(5, 3) * comb(30, 2) * comb(2, 1) * comb(10, 1) + comb(5, 2) * comb(30, 3) * comb(2, 2),  # 六等奖
            7: comb(5, 3) * comb(30, 2) * comb(2, 0) * comb(10, 2) + comb(5, 2) * comb(30, 3) * comb(2, 1) * comb(10, 1) + comb(5, 1) * comb(30, 4) * comb(2, 2),  # 七等奖
            8: comb(5, 1) * comb(30, 4) * comb(2, 1) * comb(10, 1) + comb(5, 0) * comb(30, 5) * comb(2, 2),  # 八等奖
        }
        
        if prize_level in prize_counts:
            return prize_counts[prize_level] / total
        return 0.0


class P3P5Utils:
    """排列三/排列五工具类
    
    规则：
    - 排列三：从000-999中选择一个三位数，每位独立
    - 排列五：从00000-99999中选择一个五位数，每位独立
    """
    
    @staticmethod
    def generate_p3(seed: Optional[int] = None) -> LotteryResult:
        """生成排列三号码"""
        rng = random.Random(seed) if seed is not None else random
        numbers = [rng.randint(0, 9) for _ in range(3)]
        return LotteryResult(
            lottery_type=LotteryType.P3,
            numbers=numbers,
            special_numbers=[]
        )
    
    @staticmethod
    def generate_p5(seed: Optional[int] = None) -> LotteryResult:
        """生成排列五号码"""
        rng = random.Random(seed) if seed is not None else random
        numbers = [rng.randint(0, 9) for _ in range(5)]
        return LotteryResult(
            lottery_type=LotteryType.P5,
            numbers=numbers,
            special_numbers=[]
        )
    
    @staticmethod
    def check_prize_p3(my_numbers: LotteryResult, winning_numbers: LotteryResult) -> Optional[PrizeInfo]:
        """检查排列三中奖
        
        排列三奖项：
        - 直选：完全匹配，奖金1040元
        - 组选三：三个数字有两个相同，匹配不分顺序，奖金346元
        - 组选六：三个数字各不相同，匹配不分顺序，奖金173元
        """
        if my_numbers.lottery_type != LotteryType.P3 or winning_numbers.lottery_type != LotteryType.P3:
            raise ValueError("必须是排列三号码")
        
        my_nums = my_numbers.numbers
        win_nums = winning_numbers.numbers
        
        # 直选：完全匹配
        if my_nums == win_nums:
            return PrizeInfo(prize_level=1, prize_name="直选", prize_amount=1040_00, match_count=3)
        
        # 组选匹配
        my_counter = Counter(my_nums)
        win_counter = Counter(win_nums)
        
        if my_counter == win_counter:
            # 判断是组选三还是组选六
            if len(set(my_nums)) == 2:  # 有两个相同数字
                return PrizeInfo(prize_level=2, prize_name="组选三", prize_amount=346_00, match_count=3)
            elif len(set(my_nums)) == 3:  # 三个都不同
                return PrizeInfo(prize_level=3, prize_name="组选六", prize_amount=173_00, match_count=3)
        
        return None
    
    @staticmethod
    def check_prize_p5(my_numbers: LotteryResult, winning_numbers: LotteryResult) -> Optional[PrizeInfo]:
        """检查排列五中奖
        
        排列五只有直选奖，完全匹配奖金10万元
        """
        if my_numbers.lottery_type != LotteryType.P5 or winning_numbers.lottery_type != LotteryType.P5:
            raise ValueError("必须是排列五号码")
        
        if my_numbers.numbers == winning_numbers.numbers:
            return PrizeInfo(prize_level=1, prize_name="直选", prize_amount=10_0000_00, match_count=5)
        
        return None
    
    @staticmethod
    def calculate_probability_p3(prize_type: str) -> float:
        """计算排列三中奖概率
        
        Args:
            prize_type: 'direct' 直选, 'group3' 组选三, 'group6' 组选六
        """
        if prize_type == 'direct':
            return 1 / 1000
        elif prize_type == 'group3':
            # 组选三：有两个相同数字，共 90 种情况
            return 3 / 1000
        elif prize_type == 'group6':
            # 组选六：三个数字各不相同
            return 6 / 1000
        return 0.0
    
    @staticmethod
    def calculate_probability_p5() -> float:
        """计算排列五中奖概率"""
        return 1 / 100000


class QXCUtils:
    """七星彩工具类
    
    规则：
    - 从0000000-9999999中选择一个七位数
    - 第7位为特别号码
    """
    
    @staticmethod
    def generate(seed: Optional[int] = None) -> LotteryResult:
        """生成七星彩号码"""
        rng = random.Random(seed) if seed is not None else random
        numbers = [rng.randint(0, 9) for _ in range(7)]
        return LotteryResult(
            lottery_type=LotteryType.QXC,
            numbers=numbers[:-1],  # 前6位
            special_numbers=[numbers[-1]]  # 第7位特别号
        )
    
    @staticmethod
    def check_prize(my_numbers: LotteryResult, winning_numbers: LotteryResult) -> Optional[PrizeInfo]:
        """检查七星彩中奖"""
        if my_numbers.lottery_type != LotteryType.QXC or winning_numbers.lottery_type != LotteryType.QXC:
            raise ValueError("必须是七星彩号码")
        
        my_all = my_numbers.numbers + my_numbers.special_numbers
        win_all = winning_numbers.numbers + winning_numbers.special_numbers
        
        # 从后向前匹配连续相同数字
        match_count = 0
        for i in range(6, -1, -1):
            if my_all[i] == win_all[i]:
                match_count += 1
            else:
                break
        
        # 奖项配置（连续匹配位数 -> 奖项）
        prize_config = {
            7: ("一等奖", 500_0000_00),
            6: ("二等奖", 30_0000_00),
            5: ("三等奖", 3000_00),
            4: ("四等奖", 500_00),
            3: ("五等奖", 20_00),
            2: ("六等奖", 5_00),
        }
        
        if match_count in prize_config:
            name, amount = prize_config[match_count]
            return PrizeInfo(
                prize_level=7 - match_count + 1,
                prize_name=name,
                prize_amount=amount,
                match_count=match_count
            )
        
        return None
    
    @staticmethod
    def calculate_probability(match_count: int) -> float:
        """计算连续匹配指定位数的概率"""
        if match_count < 1 or match_count > 7:
            return 0.0
        return 1 / (10 ** match_count)


class LotteryAnalyzer:
    """彩票分析工具类"""
    
    @staticmethod
    def analyze_frequency(results: List[LotteryResult], lottery_type: LotteryType) -> Dict[str, Counter]:
        """分析历史开奖号码频率
        
        Args:
            results: 历史开奖结果列表
            lottery_type: 彩票类型
            
        Returns:
            Dict[str, Counter]: 各位置号码频率统计
        """
        if not results:
            return {}
        
        main_counter = Counter()
        special_counter = Counter()
        
        for result in results:
            if result.lottery_type == lottery_type:
                main_counter.update(result.numbers)
                if result.special_numbers:
                    special_counter.update(result.special_numbers)
        
        return {
            "main": main_counter,
            "special": special_counter
        }
    
    @staticmethod
    def find_hot_cold_numbers(results: List[LotteryResult], lottery_type: LotteryType, 
                               top_n: int = 5) -> Dict[str, List[int]]:
        """找出热号和冷号
        
        Args:
            results: 历史开奖结果列表
            lottery_type: 彩票类型
            top_n: 返回前N个热号/冷号
            
        Returns:
            Dict: {"hot": [...], "cold": [...]}
        """
        freq = LotteryAnalyzer.analyze_frequency(results, lottery_type)
        
        if not freq or "main" not in freq:
            return {"hot": [], "cold": []}
        
        main_freq = freq["main"]
        sorted_nums = main_freq.most_common()
        
        hot = [num for num, _ in sorted_nums[:top_n]]
        cold = [num for num, _ in sorted_nums[-top_n:]]
        
        return {"hot": hot, "cold": cold}
    
    @staticmethod
    def calculate_odd_even_ratio(result: LotteryResult) -> Dict[str, int]:
        """计算奇偶比
        
        Args:
            result: 开奖结果
            
        Returns:
            Dict: {"odd": 奇数个数, "even": 偶数个数}
        """
        all_nums = result.numbers + (result.special_numbers or [])
        odd_count = sum(1 for n in all_nums if n % 2 == 1)
        even_count = len(all_nums) - odd_count
        
        return {"odd": odd_count, "even": even_count}
    
    @staticmethod
    def calculate_sum(result: LotteryResult) -> int:
        """计算号码和值
        
        Args:
            result: 开奖结果
            
        Returns:
            int: 所有号码之和
        """
        return sum(result.numbers) + sum(result.special_numbers or [])
    
    @staticmethod
    def calculate_span(result: LotteryResult) -> int:
        """计算号码跨度（最大值-最小值）
        
        Args:
            result: 开奖结果
            
        Returns:
            int: 跨度值
        """
        all_nums = result.numbers + (result.special_numbers or [])
        return max(all_nums) - min(all_nums)
    
    @staticmethod
    def find_consecutive(result: LotteryResult) -> List[List[int]]:
        """找出连号
        
        Args:
            result: 开奖结果
            
        Returns:
            List[List[int]]: 连号组列表
        """
        sorted_nums = sorted(set(result.numbers))
        consecutive_groups = []
        current_group = [sorted_nums[0]] if sorted_nums else []
        
        for i in range(1, len(sorted_nums)):
            if sorted_nums[i] == sorted_nums[i-1] + 1:
                current_group.append(sorted_nums[i])
            else:
                if len(current_group) >= 2:
                    consecutive_groups.append(current_group)
                current_group = [sorted_nums[i]]
        
        if len(current_group) >= 2:
            consecutive_groups.append(current_group)
        
        return consecutive_groups


class LotterySimulator:
    """彩票模拟器"""
    
    @staticmethod
    def simulate_ssq(tickets: int, winning_result: Optional[LotteryResult] = None, seed: Optional[int] = None) -> Dict[str, Any]:
        """模拟双色球购票
        
        Args:
            tickets: 购买注数
            winning_result: 开奖号码（随机生成如果为None）
            seed: 随机种子
            
        Returns:
            Dict: 模拟结果统计
        """
        if winning_result is None:
            winning_result = SSQUtils.generate(seed=seed)
        
        prize_stats = Counter()
        total_prize = 0
        cost = tickets * 200  # 每注2元 = 200分
        
        for _ in range(tickets):
            my_result = SSQUtils.generate()
            prize = SSQUtils.check_prize(my_result, winning_result)
            if prize:
                prize_stats[prize.prize_name] += 1
                total_prize += prize.prize_amount
        
        return {
            "winning_numbers": str(winning_result),
            "tickets": tickets,
            "cost": cost,
            "total_prize": total_prize,
            "profit": total_prize - cost,
            "prize_breakdown": dict(prize_stats),
            "roi": (total_prize - cost) / cost if cost > 0 else 0
        }
    
    @staticmethod
    def simulate_dlt(tickets: int, winning_result: Optional[LotteryResult] = None, seed: Optional[int] = None) -> Dict[str, Any]:
        """模拟大乐透购票
        
        Args:
            tickets: 购买注数
            winning_result: 开奖号码（随机生成如果为None）
            seed: 随机种子
            
        Returns:
            Dict: 模拟结果统计
        """
        if winning_result is None:
            winning_result = DLTUtils.generate(seed=seed)
        
        prize_stats = Counter()
        total_prize = 0
        cost = tickets * 200  # 每注2元
        
        for _ in range(tickets):
            my_result = DLTUtils.generate()
            prize = DLTUtils.check_prize(my_result, winning_result)
            if prize:
                prize_stats[prize.prize_name] += 1
                total_prize += prize.prize_amount
        
        return {
            "winning_numbers": str(winning_result),
            "tickets": tickets,
            "cost": cost,
            "total_prize": total_prize,
            "profit": total_prize - cost,
            "prize_breakdown": dict(prize_stats),
            "roi": (total_prize - cost) / cost if cost > 0 else 0
        }


def format_prize_amount(amount_fen: int) -> str:
    """格式化奖金金额（分转人民币显示）
    
    Args:
        amount_fen: 金额（分）
        
    Returns:
        str: 格式化后的金额字符串
    """
    if amount_fen >= 100_0000_00:  # 100万
        return f"{amount_fen / 100_0000_00:.2f}万元"
    elif amount_fen >= 1_0000_00:  # 1万
        return f"{amount_fen / 1_0000_00:.2f}元"
    else:
        return f"{amount_fen / 100:.2f}元"


def generate_lucky_numbers(lottery_type: LotteryType, seed: Optional[int] = None) -> LotteryResult:
    """生成幸运号码（统一接口）
    
    Args:
        lottery_type: 彩票类型
        seed: 随机种子
        
    Returns:
        LotteryResult: 生成的号码
    """
    if seed is None:
        # 使用当前时间戳生成种子
        seed = int(datetime.now().timestamp() * 1000000)
    
    if lottery_type == LotteryType.SSQ:
        return SSQUtils.generate(seed)
    elif lottery_type == LotteryType.DLT:
        return DLTUtils.generate(seed)
    elif lottery_type == LotteryType.P3:
        return P3P5Utils.generate_p3(seed)
    elif lottery_type == LotteryType.P5:
        return P3P5Utils.generate_p5(seed)
    elif lottery_type == LotteryType.QXC:
        return QXCUtils.generate(seed)
    else:
        raise ValueError(f"不支持的彩票类型: {lottery_type}")


def quick_pick(lottery_type: str, count: int = 5) -> List[LotteryResult]:
    """快速选号（便捷接口）
    
    Args:
        lottery_type: 彩票类型名称 ("双色球", "大乐透", "排列三", "排列五", "七星彩")
        count: 生成注数
        
    Returns:
        List[LotteryResult]: 号码列表
    """
    type_map = {
        "双色球": LotteryType.SSQ,
        "大乐透": LotteryType.DLT,
        "排列三": LotteryType.P3,
        "排列五": LotteryType.P5,
        "七星彩": LotteryType.QXC,
    }
    
    if lottery_type not in type_map:
        raise ValueError(f"不支持的彩票类型: {lottery_type}")
    
    lot_type = type_map[lottery_type]
    results = []
    
    for i in range(count):
        results.append(generate_lucky_numbers(lot_type))
    
    return results


if __name__ == "__main__":
    # 演示用法
    print("=" * 50)
    print("双色球号码生成")
    print("=" * 50)
    
    ssq_result = SSQUtils.generate()
    print(f"单注: {ssq_result}")
    print(f"五注: ")
    for r in SSQUtils.generate_multiple(5):
        print(f"  {r}")
    
    print("\n" + "=" * 50)
    print("大乐透号码生成")
    print("=" * 50)
    
    dlt_result = DLTUtils.generate()
    print(f"单注: {dlt_result}")
    
    print("\n" + "=" * 50)
    print("中奖概率")
    print("=" * 50)
    
    print("双色球一等奖概率: 1/{:.0f}".format(1/SSQUtils.calculate_probability(1)))
    print("大乐透一等奖概率: 1/{:.0f}".format(1/DLTUtils.calculate_probability(1)))
    print("排列三直选概率: 1/{:.0f}".format(1/P3P5Utils.calculate_probability_p3('direct')))
    print("排列五直选概率: 1/{:.0f}".format(1/P3P5Utils.calculate_probability_p5()))
    
    print("\n" + "=" * 50)
    print("模拟购票")
    print("=" * 50)
    
    sim_result = LotterySimulator.simulate_ssq(100)
    print(f"双色球模拟100注:")
    print(f"  开奖号码: {sim_result['winning_numbers']}")
    print(f"  花费: {sim_result['cost']/100}元")
    print(f"  中奖: {sim_result['prize_breakdown']}")
    print(f"  收益: {sim_result['profit']/100}元")
    print(f"  ROI: {sim_result['roi']*100:.2f}%")
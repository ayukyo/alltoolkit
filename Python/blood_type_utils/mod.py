"""
Blood Type Utilities - 血型工具模块

提供血型兼容性检测、遗传计算、分布统计等功能。
零依赖，仅使用 Python 标准库。

Author: AllToolkit
Version: 1.0.0
"""

from typing import Optional, Union, List, Dict, Tuple, Set
from enum import Enum
from dataclasses import dataclass


class BloodType(Enum):
    """血型枚举"""
    A_POSITIVE = "A+"
    A_NEGATIVE = "A-"
    B_POSITIVE = "B+"
    B_NEGATIVE = "B-"
    AB_POSITIVE = "AB+"
    AB_NEGATIVE = "AB-"
    O_POSITIVE = "O+"
    O_NEGATIVE = "O-"


class ABOType(Enum):
    """ABO血型系统"""
    A = "A"
    B = "B"
    AB = "AB"
    O = "O"


class RhFactor(Enum):
    """Rh因子"""
    POSITIVE = "+"
    NEGATIVE = "-"


@dataclass
class BloodTypeInfo:
    """血型详细信息"""
    blood_type: BloodType
    abo_type: ABOType
    rh_factor: RhFactor
    can_donate_to: List[BloodType]
    can_receive_from: List[BloodType]
    population_percentage: float
    is_universal_donor: bool
    is_universal_recipient: bool
    possible_genotypes: List[str]
    antigens: List[str]
    antibodies: List[str]


# 血型分布数据（全球平均，百分比）
_POPULATION_DISTRIBUTION: Dict[BloodType, float] = {
    BloodType.O_POSITIVE: 38.0,
    BloodType.A_POSITIVE: 34.0,
    BloodType.B_POSITIVE: 8.0,
    BloodType.AB_POSITIVE: 4.0,
    BloodType.O_NEGATIVE: 7.0,
    BloodType.A_NEGATIVE: 6.0,
    BloodType.B_NEGATIVE: 2.0,
    BloodType.AB_NEGATIVE: 1.0,
}

# 中国人群血型分布（百分比）
_CHINA_DISTRIBUTION: Dict[BloodType, float] = {
    BloodType.A_POSITIVE: 32.0,
    BloodType.B_POSITIVE: 28.0,
    BloodType.O_POSITIVE: 35.0,
    BloodType.AB_POSITIVE: 4.0,
    BloodType.A_NEGATIVE: 0.5,
    BloodType.B_NEGATIVE: 0.3,
    BloodType.O_NEGATIVE: 0.5,
    BloodType.AB_NEGATIVE: 0.2,
}

# 美国人群血型分布（百分比）
_USA_DISTRIBUTION: Dict[BloodType, float] = {
    BloodType.O_POSITIVE: 37.4,
    BloodType.A_POSITIVE: 35.7,
    BloodType.B_POSITIVE: 8.5,
    BloodType.O_NEGATIVE: 6.6,
    BloodType.A_NEGATIVE: 6.3,
    BloodType.AB_POSITIVE: 3.4,
    BloodType.B_NEGATIVE: 1.5,
    BloodType.AB_NEGATIVE: 0.6,
}

# ABO基因型对应表
_ABO_GENOTYPES: Dict[ABOType, List[str]] = {
    ABOType.A: ["AA", "AO"],
    ABOType.B: ["BB", "BO"],
    ABOType.AB: ["AB"],
    ABOType.O: ["OO"],
}

# Rh因子基因型
_RH_GENOTYPES: Dict[RhFactor, List[str]] = {
    RhFactor.POSITIVE: ["++", "+-"],
    RhFactor.NEGATIVE: ["--"],
}

# 抗原和抗体信息
_ANTIGENS_ANTIBODIES: Dict[BloodType, Tuple[List[str], List[str]]] = {
    BloodType.A_POSITIVE: (["A", "D"], ["Anti-B"]),
    BloodType.A_NEGATIVE: (["A"], ["Anti-B", "Anti-D"]),
    BloodType.B_POSITIVE: (["B", "D"], ["Anti-A"]),
    BloodType.B_NEGATIVE: (["B"], ["Anti-A", "Anti-D"]),
    BloodType.AB_POSITIVE: (["A", "B", "D"], []),
    BloodType.AB_NEGATIVE: (["A", "B"], ["Anti-D"]),
    BloodType.O_POSITIVE: (["D"], ["Anti-A", "Anti-B"]),
    BloodType.O_NEGATIVE: ([], ["Anti-A", "Anti-B", "Anti-D"]),
}


class BloodTypeUtils:
    """血型工具类"""
    
    @staticmethod
    def parse_blood_type(blood_type_str: str) -> Optional[BloodType]:
        """
        解析血型字符串
        
        Args:
            blood_type_str: 血型字符串，如 "A+", "B-", "AB+", "O+"
            
        Returns:
            BloodType 枚举值，无效则返回 None
        """
        blood_type_str = blood_type_str.upper().strip()
        
        mapping = {
            "A+": BloodType.A_POSITIVE,
            "A-": BloodType.A_NEGATIVE,
            "B+": BloodType.B_POSITIVE,
            "B-": BloodType.B_NEGATIVE,
            "AB+": BloodType.AB_POSITIVE,
            "AB-": BloodType.AB_NEGATIVE,
            "O+": BloodType.O_POSITIVE,
            "O-": BloodType.O_NEGATIVE,
            "A POSITIVE": BloodType.A_POSITIVE,
            "A NEGATIVE": BloodType.A_NEGATIVE,
            "B POSITIVE": BloodType.B_POSITIVE,
            "B NEGATIVE": BloodType.B_NEGATIVE,
            "AB POSITIVE": BloodType.AB_POSITIVE,
            "AB NEGATIVE": BloodType.AB_NEGATIVE,
            "O POSITIVE": BloodType.O_POSITIVE,
            "O NEGATIVE": BloodType.O_NEGATIVE,
        }
        
        return mapping.get(blood_type_str)
    
    @staticmethod
    def get_abo_type(blood_type: BloodType) -> ABOType:
        """获取ABO血型"""
        mapping = {
            BloodType.A_POSITIVE: ABOType.A,
            BloodType.A_NEGATIVE: ABOType.A,
            BloodType.B_POSITIVE: ABOType.B,
            BloodType.B_NEGATIVE: ABOType.B,
            BloodType.AB_POSITIVE: ABOType.AB,
            BloodType.AB_NEGATIVE: ABOType.AB,
            BloodType.O_POSITIVE: ABOType.O,
            BloodType.O_NEGATIVE: ABOType.O,
        }
        return mapping[blood_type]
    
    @staticmethod
    def get_rh_factor(blood_type: BloodType) -> RhFactor:
        """获取Rh因子"""
        return RhFactor.POSITIVE if "+" in blood_type.value else RhFactor.NEGATIVE
    
    @staticmethod
    def can_donate_to(donor: BloodType, recipient: BloodType) -> bool:
        """
        判断献血者是否可以向受血者献血
        
        Args:
            donor: 献血者血型
            recipient: 受血者血型
            
        Returns:
            是否可以献血
        """
        donor_abo = BloodTypeUtils.get_abo_type(donor)
        donor_rh = BloodTypeUtils.get_rh_factor(donor)
        recipient_abo = BloodTypeUtils.get_abo_type(recipient)
        recipient_rh = BloodTypeUtils.get_rh_factor(recipient)
        
        # Rh阴性可以给Rh阳性献血，但反之不行
        if donor_rh == RhFactor.POSITIVE and recipient_rh == RhFactor.NEGATIVE:
            return False
        
        # ABO兼容性检查
        if donor_abo == ABOType.O:
            # O型是万能献血者（ABO层面）
            return True
        elif donor_abo == ABOType.A:
            # A型可以给A型或AB型
            return recipient_abo in [ABOType.A, ABOType.AB]
        elif donor_abo == ABOType.B:
            # B型可以给B型或AB型
            return recipient_abo in [ABOType.B, ABOType.AB]
        elif donor_abo == ABOType.AB:
            # AB型只能给AB型
            return recipient_abo == ABOType.AB
        
        return False
    
    @staticmethod
    def can_receive_from(recipient: BloodType, donor: BloodType) -> bool:
        """
        判断受血者是否可以接受献血者的血
        
        Args:
            recipient: 受血者血型
            donor: 献血者血型
            
        Returns:
            是否可以受血
        """
        return BloodTypeUtils.can_donate_to(donor, recipient)
    
    @staticmethod
    def get_compatible_donors(recipient: BloodType) -> List[BloodType]:
        """获取所有可献血给指定血型的献血者"""
        compatible = []
        for bt in BloodType:
            if BloodTypeUtils.can_donate_to(bt, recipient):
                compatible.append(bt)
        return compatible
    
    @staticmethod
    def get_compatible_recipients(donor: BloodType) -> List[BloodType]:
        """获取指定血型可以献血的所有受血者"""
        compatible = []
        for bt in BloodType:
            if BloodTypeUtils.can_donate_to(donor, bt):
                compatible.append(bt)
        return compatible
    
    @staticmethod
    def is_universal_donor(blood_type: BloodType) -> bool:
        """是否为万能献血者（O-）"""
        return blood_type == BloodType.O_NEGATIVE
    
    @staticmethod
    def is_universal_recipient(blood_type: BloodType) -> bool:
        """是否为万能受血者（AB+）"""
        return blood_type == BloodType.AB_POSITIVE
    
    @staticmethod
    def get_blood_type_info(blood_type: BloodType) -> BloodTypeInfo:
        """获取血型完整信息"""
        can_donate = BloodTypeUtils.get_compatible_recipients(blood_type)
        can_receive = BloodTypeUtils.get_compatible_donors(blood_type)
        antigens, antibodies = _ANTIGENS_ANTIBODIES[blood_type]
        
        return BloodTypeInfo(
            blood_type=blood_type,
            abo_type=BloodTypeUtils.get_abo_type(blood_type),
            rh_factor=BloodTypeUtils.get_rh_factor(blood_type),
            can_donate_to=can_donate,
            can_receive_from=can_receive,
            population_percentage=_POPULATION_DISTRIBUTION[blood_type],
            is_universal_donor=BloodTypeUtils.is_universal_donor(blood_type),
            is_universal_recipient=BloodTypeUtils.is_universal_recipient(blood_type),
            possible_genotypes=_ABO_GENOTYPES[BloodTypeUtils.get_abo_type(blood_type)],
            antigens=antigens,
            antibodies=antibodies,
        )
    
    @staticmethod
    def calculate_child_blood_types(
        parent1: BloodType, 
        parent2: BloodType
    ) -> Dict[BloodType, float]:
        """
        计算父母血型组合可能产生的孩子血型及概率
        
        Args:
            parent1: 父母一方血型
            parent2: 父母另一方血型
            
        Returns:
            可能的血型及其概率（百分比）
        """
        # 获取ABO基因型
        p1_abo = BloodTypeUtils.get_abo_type(parent1)
        p2_abo = BloodTypeUtils.get_abo_type(parent2)
        p1_rh = BloodTypeUtils.get_rh_factor(parent1)
        p2_rh = BloodTypeUtils.get_rh_factor(parent2)
        
        # 可能的ABO基因组合
        p1_abo_alleles = []
        if p1_abo == ABOType.A:
            p1_abo_alleles = ["A", "O"]  # 简化处理
        elif p1_abo == ABOType.B:
            p1_abo_alleles = ["B", "O"]
        elif p1_abo == ABOType.AB:
            p1_abo_alleles = ["A", "B"]
        elif p1_abo == ABOType.O:
            p1_abo_alleles = ["O", "O"]
        
        p2_abo_alleles = []
        if p2_abo == ABOType.A:
            p2_abo_alleles = ["A", "O"]
        elif p2_abo == ABOType.B:
            p2_abo_alleles = ["B", "O"]
        elif p2_abo == ABOType.AB:
            p2_abo_alleles = ["A", "B"]
        elif p2_abo == ABOType.O:
            p2_abo_alleles = ["O", "O"]
        
        # 计算ABO组合
        abo_results: Dict[str, int] = {}
        for a1 in p1_abo_alleles:
            for a2 in p2_abo_alleles:
                # 排序以处理AB情况
                pair = tuple(sorted([a1, a2], key=lambda x: {'A': 1, 'B': 2, 'O': 3}[x]))
                if pair[0] == 'A' and pair[1] == 'B':
                    genotype = "AB"
                else:
                    genotype = pair[0] if pair[0] != pair[1] else pair[0]
                    if genotype == "O":
                        genotype = "O"
                    elif genotype == "A":
                        genotype = "A"
                    elif genotype == "B":
                        genotype = "B"
                abo_results[genotype] = abo_results.get(genotype, 0) + 1
        
        # Rh因子组合
        p1_rh_alleles = ["+"] if p1_rh == RhFactor.POSITIVE else ["-"]
        p1_rh_alleles.extend(["+", "-"] if p1_rh == RhFactor.POSITIVE else [])
        if len(p1_rh_alleles) == 1:
            p1_rh_alleles = ["+", "-"]  # Rh+可能是++或+-
        
        p2_rh_alleles = ["+"] if p2_rh == RhFactor.POSITIVE else ["-"]
        p2_rh_alleles.extend(["+", "-"] if p2_rh == RhFactor.POSITIVE else [])
        if len(p2_rh_alleles) == 1:
            p2_rh_alleles = ["+", "-"]
        
        rh_results: Dict[str, int] = {}
        # 简化计算
        rh_pos_prob = 0.75 if (p1_rh == RhFactor.POSITIVE and p2_rh == RhFactor.POSITIVE) else (
            0.5 if (p1_rh == RhFactor.POSITIVE or p2_rh == RhFactor.POSITIVE) else 0
        )
        
        # 组合结果
        total_combinations = len(p1_abo_alleles) * len(p2_abo_alleles)
        results: Dict[BloodType, float] = {}
        
        for abo, count in abo_results.items():
            abo_prob = count / total_combinations
            rh_pos = abo_prob * rh_pos_prob * 100
            rh_neg = abo_prob * (1 - rh_pos_prob) * 100
            
            if abo == "A":
                if rh_pos > 0:
                    results[BloodType.A_POSITIVE] = results.get(BloodType.A_POSITIVE, 0) + rh_pos
                if rh_neg > 0:
                    results[BloodType.A_NEGATIVE] = results.get(BloodType.A_NEGATIVE, 0) + rh_neg
            elif abo == "B":
                if rh_pos > 0:
                    results[BloodType.B_POSITIVE] = results.get(BloodType.B_POSITIVE, 0) + rh_pos
                if rh_neg > 0:
                    results[BloodType.B_NEGATIVE] = results.get(BloodType.B_NEGATIVE, 0) + rh_neg
            elif abo == "AB":
                if rh_pos > 0:
                    results[BloodType.AB_POSITIVE] = results.get(BloodType.AB_POSITIVE, 0) + rh_pos
                if rh_neg > 0:
                    results[BloodType.AB_NEGATIVE] = results.get(BloodType.AB_NEGATIVE, 0) + rh_neg
            elif abo == "O":
                if rh_pos > 0:
                    results[BloodType.O_POSITIVE] = results.get(BloodType.O_POSITIVE, 0) + rh_pos
                if rh_neg > 0:
                    results[BloodType.O_NEGATIVE] = results.get(BloodType.O_NEGATIVE, 0) + rh_neg
        
        return results
    
    @staticmethod
    def possible_blood_types_from_parents(
        parent1: BloodType,
        parent2: BloodType
    ) -> Set[BloodType]:
        """
        获取父母血型组合可能产生的孩子血型（不含概率）
        
        Args:
            parent1: 父母一方血型
            parent2: 父母另一方血型
            
        Returns:
            可能的血型集合
        """
        probs = BloodTypeUtils.calculate_child_blood_types(parent1, parent2)
        return set(probs.keys())
    
    @staticmethod
    def can_be_parent(
        parent: BloodType,
        child: BloodType
    ) -> bool:
        """
        判断指定血型是否可能是孩子的父母
        
        Args:
            parent: 可能的父母血型
            child: 孩子血型
            
        Returns:
            是否可能为父母
        """
        # 遍历所有血型，看是否有某种组合能产生这个孩子
        for potential_parent in BloodType:
            possible_children = BloodTypeUtils.possible_blood_types_from_parents(
                parent, potential_parent
            )
            if child in possible_children:
                return True
        return False
    
    @staticmethod
    def find_possible_parents(child: BloodType) -> List[Tuple[BloodType, BloodType]]:
        """
        找出可能产生指定血型孩子的父母组合
        
        Args:
            child: 孩子血型
            
        Returns:
            可能的父母血型组合列表
        """
        possible_pairs = []
        for p1 in BloodType:
            for p2 in BloodType:
                if child in BloodTypeUtils.possible_blood_types_from_parents(p1, p2):
                    possible_pairs.append((p1, p2))
        return possible_pairs
    
    @staticmethod
    def get_population_percentage(
        blood_type: BloodType,
        population: str = "global"
    ) -> float:
        """
        获取血型在特定人群中的分布比例
        
        Args:
            blood_type: 血型
            population: 人群类型 ("global", "china", "usa")
            
        Returns:
            百分比（0-100）
        """
        distributions = {
            "global": _POPULATION_DISTRIBUTION,
            "china": _CHINA_DISTRIBUTION,
            "usa": _USA_DISTRIBUTION,
        }
        
        dist = distributions.get(population.lower(), _POPULATION_DISTRIBUTION)
        return dist.get(blood_type, 0.0)
    
    @staticmethod
    def is_rare_blood_type(
        blood_type: BloodType,
        population: str = "global",
        threshold: float = 5.0
    ) -> bool:
        """
        判断是否为稀有血型
        
        Args:
            blood_type: 血型
            population: 人群类型
            threshold: 稀有度阈值（百分比低于此值视为稀有）
            
        Returns:
            是否为稀有血型
        """
        percentage = BloodTypeUtils.get_population_percentage(blood_type, population)
        return percentage < threshold
    
    @staticmethod
    def get_rare_blood_types(
        population: str = "global",
        threshold: float = 5.0
    ) -> List[BloodType]:
        """获取指定人群中的稀有血型列表"""
        rare = []
        for bt in BloodType:
            if BloodTypeUtils.is_rare_blood_type(bt, population, threshold):
                rare.append(bt)
        return rare
    
    @staticmethod
    def format_blood_type(blood_type: BloodType, style: str = "short") -> str:
        """
        格式化血型显示
        
        Args:
            blood_type: 血型
            style: 格式风格 ("short": "A+", "full": "A型阳性", "chinese": "A型血")
            
        Returns:
            格式化后的字符串
        """
        if style == "short":
            return blood_type.value
        elif style == "full":
            abo = BloodTypeUtils.get_abo_type(blood_type).value
            rh = "阳性" if BloodTypeUtils.get_rh_factor(blood_type) == RhFactor.POSITIVE else "阴性"
            return f"{abo}型{rh}"
        elif style == "chinese":
            abo = BloodTypeUtils.get_abo_type(blood_type).value
            return f"{abo}型血"
        else:
            return blood_type.value
    
    @staticmethod
    def get_all_blood_types() -> List[BloodType]:
        """获取所有血型列表"""
        return list(BloodType)
    
    @staticmethod
    def get_distribution_by_population(population: str = "global") -> Dict[BloodType, float]:
        """获取指定人群的血型分布"""
        distributions = {
            "global": _POPULATION_DISTRIBUTION,
            "china": _CHINA_DISTRIBUTION,
            "usa": _USA_DISTRIBUTION,
        }
        return distributions.get(population.lower(), _POPULATION_DISTRIBUTION).copy()


# 便捷函数
def parse_blood_type(blood_type_str: str) -> Optional[BloodType]:
    """解析血型字符串"""
    return BloodTypeUtils.parse_blood_type(blood_type_str)


def can_donate(donor: Union[str, BloodType], recipient: Union[str, BloodType]) -> bool:
    """判断是否可以献血"""
    if isinstance(donor, str):
        donor = BloodTypeUtils.parse_blood_type(donor)
    if isinstance(recipient, str):
        recipient = BloodTypeUtils.parse_blood_type(recipient)
    if donor is None or recipient is None:
        return False
    return BloodTypeUtils.can_donate_to(donor, recipient)


def get_compatible_donors(recipient: Union[str, BloodType]) -> List[BloodType]:
    """获取兼容的献血者"""
    if isinstance(recipient, str):
        recipient = BloodTypeUtils.parse_blood_type(recipient)
    if recipient is None:
        return []
    return BloodTypeUtils.get_compatible_donors(recipient)


def get_compatible_recipients(donor: Union[str, BloodType]) -> List[BloodType]:
    """获取可以献血的受血者"""
    if isinstance(donor, str):
        donor = BloodTypeUtils.parse_blood_type(donor)
    if donor is None:
        return []
    return BloodTypeUtils.get_compatible_recipients(donor)


def child_blood_types(
    parent1: Union[str, BloodType],
    parent2: Union[str, BloodType]
) -> Dict[BloodType, float]:
    """计算孩子可能的血型"""
    if isinstance(parent1, str):
        parent1 = BloodTypeUtils.parse_blood_type(parent1)
    if isinstance(parent2, str):
        parent2 = BloodTypeUtils.parse_blood_type(parent2)
    if parent1 is None or parent2 is None:
        return {}
    return BloodTypeUtils.calculate_child_blood_types(parent1, parent2)


def get_blood_type_info(blood_type: Union[str, BloodType]) -> Optional[BloodTypeInfo]:
    """获取血型详细信息"""
    if isinstance(blood_type, str):
        blood_type = BloodTypeUtils.parse_blood_type(blood_type)
    if blood_type is None:
        return None
    return BloodTypeUtils.get_blood_type_info(blood_type)


if __name__ == "__main__":
    # 简单演示
    print("=" * 50)
    print("Blood Type Utils Demo")
    print("=" * 50)
    
    # 测试血型兼容性
    donor = BloodType.O_NEGATIVE
    print(f"\n{donor.value} (万能献血者) 可以献血给:")
    for recipient in BloodTypeUtils.get_compatible_recipients(donor):
        print(f"  - {recipient.value}")
    
    recipient = BloodType.AB_POSITIVE
    print(f"\n{recipient.value} (万能受血者) 可以接受:")
    for d in BloodTypeUtils.get_compatible_donors(recipient):
        print(f"  - {d.value}")
    
    # 测试遗传计算
    print("\n父母 A+ 和 B+ 的孩子可能血型:")
    child_types = BloodTypeUtils.calculate_child_blood_types(
        BloodType.A_POSITIVE, BloodType.B_POSITIVE
    )
    for bt, prob in sorted(child_types.items(), key=lambda x: -x[1]):
        print(f"  - {bt.value}: {prob:.1f}%")
    
    # 测试稀有血型
    print("\n全球稀有血型 (< 5%):")
    for bt in BloodTypeUtils.get_rare_blood_types("global"):
        pct = BloodTypeUtils.get_population_percentage(bt, "global")
        print(f"  - {bt.value}: {pct}%")
"""
Medication Utilities - 药物剂量计算工具

用于安全计算和管理药物剂量的实用工具集。

核心功能:
- 按体重计算药物剂量
- 儿童剂量计算（多种方法）
- 药物浓度单位转换
- 给药间隔验证
- 剂量范围安全检查
- 输液速度计算
- 半衰期和稳态浓度估算

零外部依赖，纯 Python 实现。

警告: 此工具仅供学习和参考用途，不应替代专业医疗建议。
实际用药请遵医嘱。
"""

from typing import Tuple, List, Optional, Dict, Union
from dataclasses import dataclass
from enum import Enum
import math


class DoseUnit(Enum):
    """剂量单位"""
    MG = "mg"
    G = "g"
    MCG = "mcg"  # 微克
    ML = "ml"
    UNITS = "units"  # 胰岛素等单位


class WeightUnit(Enum):
    """体重单位"""
    KG = "kg"
    LB = "lb"


class TimeUnit(Enum):
    """时间单位"""
    HOURS = "hours"
    DAYS = "days"
    MINUTES = "minutes"


class Route(Enum):
    """给药途径"""
    ORAL = "oral"
    IV = "intravenous"
    IM = "intramuscular"
    SC = "subcutaneous"
    TOPICAL = "topical"
    INHALATION = "inhalation"


@dataclass
class DoseRange:
    """剂量范围"""
    min_dose: float
    max_dose: float
    unit: DoseUnit
    
    def contains(self, dose: float) -> bool:
        """检查剂量是否在安全范围内"""
        return self.min_dose <= dose <= self.max_dose
    
    def is_too_low(self, dose: float) -> bool:
        """检查剂量是否过低"""
        return dose < self.min_dose
    
    def is_too_high(self, dose: float) -> bool:
        """检查剂量是否过高"""
        return dose > self.max_dose


@dataclass
class MedicationInfo:
    """药物信息"""
    name: str
    standard_dose_per_kg: float  # 每公斤标准剂量
    dose_unit: DoseUnit
    dose_range: Optional[DoseRange] = None
    max_daily_dose: Optional[float] = None
    half_life_hours: Optional[float] = None
    routes: List[Route] = None
    bioavailability: float = 1.0  # 生物利用度 (0-1)
    
    def __post_init__(self):
        if self.routes is None:
            self.routes = [Route.ORAL]


class MedicationCalculator:
    """药物剂量计算器"""
    
    def __init__(self, medication: MedicationInfo):
        self.medication = medication
    
    def calculate_weight_based_dose(
        self,
        weight: float,
        weight_unit: WeightUnit = WeightUnit.KG
    ) -> float:
        """
        按体重计算剂量
        
        Args:
            weight: 体重
            weight_unit: 体重单位
            
        Returns:
            计算后的剂量
        """
        # 转换为公斤
        weight_kg = self._to_kg(weight, weight_unit)
        
        # 计算剂量
        dose = weight_kg * self.medication.standard_dose_per_kg
        
        return dose
    
    def calculate_pediatric_dose_fried(
        self,
        age_months: float
    ) -> float:
        """
        Fried 规则计算儿童剂量（适用于 1-2 岁以下婴儿）
        
        公式: 儿童剂量 = 成人剂量 × (年龄月数 / 150)
        
        Args:
            age_months: 月龄
            
        Returns:
            计算后的剂量
        """
        # 成人标准剂量（按 70kg 成人计算）
        adult_dose = 70 * self.medication.standard_dose_per_kg
        
        return adult_dose * (age_months / 150)
    
    def calculate_pediatric_dose_young(
        self,
        age_years: float
    ) -> float:
        """
        Young 规则计算儿童剂量（适用于 2-12 岁）
        
        公式: 儿童剂量 = 成人剂量 × (年龄 / (年龄 + 12))
        
        Args:
            age_years: 年龄（岁）
            
        Returns:
            计算后的剂量
        """
        adult_dose = 70 * self.medication.standard_dose_per_kg
        return adult_dose * (age_years / (age_years + 12))
    
    def calculate_pediatric_dose_clark(
        self,
        weight: float,
        weight_unit: WeightUnit = WeightUnit.KG
    ) -> float:
        """
        Clark 规则计算儿童剂量（按体重）
        
        公式: 儿童剂量 = 成人剂量 × (体重磅数 / 150)
        
        Args:
            weight: 体重
            weight_unit: 体重单位
            
        Returns:
            计算后的剂量
        """
        # 转换为磅
        weight_lb = self._to_lb(weight, weight_unit)
        adult_dose = 70 * self.medication.standard_dose_per_kg
        
        return adult_dose * (weight_lb / 150)
    
    def calculate_pediatric_dose_body_surface(
        self,
        weight: float,
        height: float,
        weight_unit: WeightUnit = WeightUnit.KG,
        height_unit: str = "cm"
    ) -> float:
        """
        体表面积法计算儿童剂量
        
        使用 Mosteller 公式计算体表面积
        
        Args:
            weight: 体重
            height: 身高
            weight_unit: 体重单位
            height_unit: 身高单位
            
        Returns:
            计算后的剂量
        """
        # 转换单位
        weight_kg = self._to_kg(weight, weight_unit)
        height_cm = height if height_unit == "cm" else height * 2.54
        
        # Mosteller 公式: BSA (m²) = √(身高cm × 体重kg / 3600)
        bsa = math.sqrt((height_cm * weight_kg) / 3600)
        
        # 成人体表面积约 1.73 m²
        adult_bsa = 1.73
        adult_dose = 70 * self.medication.standard_dose_per_kg
        
        return adult_dose * (bsa / adult_bsa)
    
    def validate_dose(
        self,
        dose: float,
        weight: Optional[float] = None,
        weight_unit: WeightUnit = WeightUnit.KG
    ) -> Dict[str, Union[bool, str, float]]:
        """
        验证剂量安全性
        
        Args:
            dose: 待验证剂量（绝对值）
            weight: 体重（可选，用于每公斤剂量验证）
            weight_unit: 体重单位
            
        Returns:
            验证结果字典
        """
        result = {
            "dose": dose,
            "is_valid": True,
            "warnings": [],
            "errors": []
        }
        
        # 检查负值
        if dose <= 0:
            result["is_valid"] = False
            result["errors"].append("剂量必须为正数")
            return result
        
        # 检查剂量范围（如果有体重，验证每公斤剂量）
        if self.medication.dose_range:
            if weight is not None:
                # 验证每公斤剂量
                weight_kg = self._to_kg(weight, weight_unit)
                dose_per_kg = dose / weight_kg
                
                if self.medication.dose_range.is_too_low(dose_per_kg):
                    result["is_valid"] = False
                    result["errors"].append(
                        f"每公斤剂量过低: {dose_per_kg:.2f}{self.medication.dose_unit.value}/kg "
                        f"< 最小剂量 {self.medication.dose_range.min_dose}{self.medication.dose_unit.value}/kg"
                    )
                elif self.medication.dose_range.is_too_high(dose_per_kg):
                    result["is_valid"] = False
                    result["errors"].append(
                        f"每公斤剂量过高: {dose_per_kg:.2f}{self.medication.dose_unit.value}/kg "
                        f"> 最大剂量 {self.medication.dose_range.max_dose}{self.medication.dose_unit.value}/kg"
                    )
            else:
                # 没有体重，验证绝对剂量是否超过每公斤最大剂量的70kg等效
                max_absolute = self.medication.dose_range.max_dose * 70
                if dose > max_absolute:
                    result["warnings"].append(
                        f"剂量可能过高（假设70kg成人）: {dose}{self.medication.dose_unit.value} "
                        f"> 建议最大 {max_absolute}{self.medication.dose_unit.value}"
                    )
        
        # 检查是否超过每日最大剂量
        if self.medication.max_daily_dose and dose > self.medication.max_daily_dose:
            result["is_valid"] = False
            result["errors"].append(
                f"超过每日最大剂量: {dose}{self.medication.dose_unit.value} "
                f"> {self.medication.max_daily_dose}{self.medication.dose_unit.value}"
            )
        
        return result
    
    @staticmethod
    def _to_kg(weight: float, unit: WeightUnit) -> float:
        """转换体重到公斤"""
        if unit == WeightUnit.KG:
            return weight
        elif unit == WeightUnit.LB:
            return weight * 0.453592
        raise ValueError(f"未知体重单位: {unit}")
    
    @staticmethod
    def _to_lb(weight: float, unit: WeightUnit) -> float:
        """转换体重到磅"""
        if unit == WeightUnit.LB:
            return weight
        elif unit == WeightUnit.KG:
            return weight * 2.20462
        raise ValueError(f"未知体重单位: {unit}")


class InfusionCalculator:
    """输液计算器"""
    
    @staticmethod
    def calculate_drip_rate(
        volume_ml: float,
        time_minutes: float,
        drop_factor: int = 20
    ) -> float:
        """
        计算输液滴速
        
        Args:
            volume_ml: 输液量 (毫升)
            time_minutes: 输液时间 (分钟)
            drop_factor: 滴系数 (滴/毫升)
                        常见值: 10 (血液), 15 (普通), 20 (微滴), 60 (小儿)
            
        Returns:
            滴速 (滴/分钟)
        """
        return (volume_ml * drop_factor) / time_minutes
    
    @staticmethod
    def calculate_infusion_time(
        volume_ml: float,
        rate_ml_per_hour: float
    ) -> float:
        """
        计算输液所需时间
        
        Args:
            volume_ml: 输液量 (毫升)
            rate_ml_per_hour: 输液速度 (毫升/小时)
            
        Returns:
            输液时间 (小时)
        """
        if rate_ml_per_hour <= 0:
            raise ValueError("输液速度必须为正数")
        return volume_ml / rate_ml_per_hour
    
    @staticmethod
    def calculate_volume(
        dose_mg: float,
        concentration_mg_per_ml: float
    ) -> float:
        """
        计算需要抽取的液体体积
        
        Args:
            dose_mg: 所需剂量 (毫克)
            concentration_mg_per_ml: 药物浓度 (毫克/毫升)
            
        Returns:
            所需体积 (毫升)
        """
        if concentration_mg_per_ml <= 0:
            raise ValueError("药物浓度必须为正数")
        return dose_mg / concentration_mg_per_ml


class HalfLifeCalculator:
    """药物半衰期计算器"""
    
    @staticmethod
    def calculate_remaining_dose(
        initial_dose: float,
        half_life_hours: float,
        elapsed_hours: float
    ) -> float:
        """
        计算经过一段时间后体内剩余药物量
        
        公式: 剩余量 = 初始量 × (1/2)^(经过时间/半衰期)
        
        Args:
            initial_dose: 初始剂量
            half_life_hours: 半衰期 (小时)
            elapsed_hours: 经过时间 (小时)
            
        Returns:
            剩余药物量
        """
        return initial_dose * math.pow(0.5, elapsed_hours / half_life_hours)
    
    @staticmethod
    def calculate_time_to_eliminate(
        initial_dose: float,
        half_life_hours: float,
        target_dose: float
    ) -> float:
        """
        计算药物消除到目标量所需时间
        
        Args:
            initial_dose: 初始剂量
            half_life_hours: 半衰期 (小时)
            target_dose: 目标剂量
            
        Returns:
            所需时间 (小时)
        """
        if target_dose <= 0:
            raise ValueError("目标剂量必须为正数")
        if target_dose >= initial_dose:
            return 0
        
        # t = t½ × log2(初始量/目标量)
        return half_life_hours * math.log2(initial_dose / target_dose)
    
    @staticmethod
    def estimate_steady_state_time(half_life_hours: float) -> float:
        """
        估算达到稳态浓度所需时间
        
        一般需要 4-5 个半衰期达到稳态
        
        Args:
            half_life_hours: 半衰期 (小时)
            
        Returns:
            达到稳态所需时间 (小时)
        """
        return half_life_hours * 5
    
    @staticmethod
    def calculate_dosing_interval(
        half_life_hours: float,
        min_therapeutic_ratio: float = 0.5
    ) -> float:
        """
        根据半衰期计算给药间隔
        
        Args:
            half_life_hours: 半衰期 (小时)
            min_therapeutic_ratio: 最小治疗浓度比率 (峰谷比)
            
        Returns:
            建议给药间隔 (小时)
        """
        # 使谷浓度不低于峰浓度的 min_therapeutic_ratio
        # 峰浓度 × (1/2)^(间隔/半衰期) >= 峰浓度 × min_therapeutic_ratio
        # 解得: 间隔 <= 半衰期 × log2(1/min_therapeutic_ratio)
        return half_life_hours * math.log2(1 / min_therapeutic_ratio)


class DoseConverter:
    """剂量单位转换器"""
    
    @staticmethod
    def mg_to_g(mg: float) -> float:
        """毫克转克"""
        return mg / 1000
    
    @staticmethod
    def g_to_mg(g: float) -> float:
        """克转毫克"""
        return g * 1000
    
    @staticmethod
    def mg_to_mcg(mg: float) -> float:
        """毫克转微克"""
        return mg * 1000
    
    @staticmethod
    def mcg_to_mg(mcg: float) -> float:
        """微克转毫克"""
        return mcg / 1000
    
    @staticmethod
    def kg_to_lb(kg: float) -> float:
        """公斤转磅"""
        return kg * 2.20462
    
    @staticmethod
    def lb_to_kg(lb: float) -> float:
        """磅转公斤"""
        return lb * 0.453592
    
    @staticmethod
    def convert_dose(
        dose: float,
        from_unit: DoseUnit,
        to_unit: DoseUnit
    ) -> float:
        """
        通用剂量单位转换
        
        Args:
            dose: 原始剂量
            from_unit: 原单位
            to_unit: 目标单位
            
        Returns:
            转换后的剂量
        """
        conversions = {
            (DoseUnit.G, DoseUnit.MG): 1000,
            (DoseUnit.MG, DoseUnit.G): 0.001,
            (DoseUnit.MG, DoseUnit.MCG): 1000,
            (DoseUnit.MCG, DoseUnit.MG): 0.001,
            (DoseUnit.G, DoseUnit.MCG): 1000000,
            (DoseUnit.MCG, DoseUnit.G): 0.000001,
        }
        
        if from_unit == to_unit:
            return dose
        
        key = (from_unit, to_unit)
        if key in conversions:
            return dose * conversions[key]
        
        raise ValueError(f"不支持从 {from_unit.value} 到 {to_unit.value} 的转换")


class RenalDoseAdjuster:
    """肾功能剂量调整器"""
    
    @staticmethod
    def calculate_creatinine_clearance(
        age: int,
        weight_kg: float,
        serum_creatinine: float,
        is_female: bool = False
    ) -> float:
        """
        Cockcroft-Gault 公式计算肌酐清除率
        
        Args:
            age: 年龄
            weight_kg: 体重 (公斤)
            serum_creatinine: 血清肌酐 (mg/dL)
            is_female: 是否为女性
            
        Returns:
            肌酐清除率 (mL/min)
        """
        # 基础公式
        ccr = ((140 - age) * weight_kg) / (72 * serum_creatinine)
        
        # 女性修正
        if is_female:
            ccr *= 0.85
        
        return ccr
    
    @staticmethod
    def adjust_dose_for_renal(
        standard_dose: float,
        ccr: float
    ) -> Tuple[float, str]:
        """
        根据肾功能调整剂量
        
        Args:
            standard_dose: 标准剂量
            ccr: 肌酐清除率 (mL/min)
            
        Returns:
            (调整后剂量, 调整说明)
        """
        if ccr >= 90:
            return standard_dose, "肾功能正常，使用标准剂量"
        elif ccr >= 60:
            return standard_dose * 0.9, "轻度肾功能不全，剂量减少 10%"
        elif ccr >= 30:
            return standard_dose * 0.75, "中度肾功能不全，剂量减少 25%"
        elif ccr >= 15:
            return standard_dose * 0.5, "重度肾功能不全，剂量减少 50%"
        else:
            return standard_dose * 0.25, "终末期肾病，剂量减少 75%（或避免使用）"


class DrugInteractionChecker:
    """药物相互作用检查器"""
    
    # 常见药物相互作用类别
    INTERACTION_TYPES = {
        "synergistic": "协同作用（增强效果）",
        "antagonistic": "拮抗作用（减弱效果）",
        "additive": "相加作用",
        "toxicity_risk": "毒性风险",
        "absorption_interference": "吸收干扰",
        "metabolism_interference": "代谢干扰"
    }
    
    # 常见药物相互作用数据库
    KNOWN_INTERACTIONS = {
        ("warfarin", "aspirin"): {
            "type": "toxicity_risk",
            "severity": "high",
            "description": "增加出血风险"
        },
        ("warfarin", "vitamin_k"): {
            "type": "antagonistic",
            "severity": "medium",
            "description": "维生素K可降低华法林抗凝效果"
        },
        ("metformin", "alcohol"): {
            "type": "toxicity_risk",
            "severity": "medium",
            "description": "增加乳酸酸中毒风险"
        },
        ("ssri", "maoi"): {
            "type": "toxicity_risk",
            "severity": "critical",
            "description": "5-羟色胺综合征风险"
        },
        ("tetracycline", "antacid"): {
            "type": "absorption_interference",
            "severity": "low",
            "description": "抗酸药可减少四环素吸收"
        },
        ("ciprofloxacin", "dairy"): {
            "type": "absorption_interference",
            "severity": "medium",
            "description": "乳制品可减少环丙沙星吸收"
        },
        ("statin", "grapefruit"): {
            "type": "metabolism_interference",
            "severity": "medium",
            "description": "西柚汁可增加他汀类药物血药浓度"
        },
    }
    
    @classmethod
    def check_interaction(
        cls,
        drug1: str,
        drug2: str
    ) -> Optional[Dict]:
        """
        检查两种药物之间的相互作用
        
        Args:
            drug1: 药物1名称（小写）
            drug2: 药物2名称（小写）
            
        Returns:
            相互作用信息，无相互作用返回 None
        """
        drug1 = drug1.lower().strip()
        drug2 = drug2.lower().strip()
        
        # 双向检查
        key1 = (drug1, drug2)
        key2 = (drug2, drug1)
        
        if key1 in cls.KNOWN_INTERACTIONS:
            return cls.KNOWN_INTERACTIONS[key1]
        if key2 in cls.KNOWN_INTERACTIONS:
            return cls.KNOWN_INTERACTIONS[key2]
        
        return None
    
    @classmethod
    def check_multiple_interactions(
        cls,
        drugs: List[str]
    ) -> List[Dict]:
        """
        检查多种药物之间的相互作用
        
        Args:
            drugs: 药物名称列表
            
        Returns:
            相互作用列表
        """
        interactions = []
        
        for i, drug1 in enumerate(drugs):
            for drug2 in drugs[i+1:]:
                interaction = cls.check_interaction(drug1, drug2)
                if interaction:
                    interactions.append({
                        "drug1": drug1,
                        "drug2": drug2,
                        **interaction
                    })
        
        return interactions


# 常用药物数据库
COMMON_MEDICATIONS = {
    "paracetamol": MedicationInfo(
        name="Paracetamol (Acetaminophen)",
        standard_dose_per_kg=10,  # 10-15 mg/kg
        dose_unit=DoseUnit.MG,
        dose_range=DoseRange(10, 15, DoseUnit.MG),
        max_daily_dose=4000,  # 成人最大日剂量
        half_life_hours=2,
        bioavailability=0.85
    ),
    "ibuprofen": MedicationInfo(
        name="Ibuprofen",
        standard_dose_per_kg=10,  # 5-10 mg/kg
        dose_unit=DoseUnit.MG,
        dose_range=DoseRange(5, 10, DoseUnit.MG),
        max_daily_dose=3200,
        half_life_hours=2,
        bioavailability=0.8
    ),
    "amoxicillin": MedicationInfo(
        name="Amoxicillin",
        standard_dose_per_kg=25,  # 20-40 mg/kg/day divided
        dose_unit=DoseUnit.MG,
        dose_range=DoseRange(20, 40, DoseUnit.MG),
        max_daily_dose=3000,
        half_life_hours=1.3,
        routes=[Route.ORAL, Route.IV],
        bioavailability=0.9
    ),
    "prednisone": MedicationInfo(
        name="Prednisone",
        standard_dose_per_kg=0.5,  # 0.5-2 mg/kg/day
        dose_unit=DoseUnit.MG,
        dose_range=DoseRange(0.5, 2, DoseUnit.MG),
        max_daily_dose=60,
        half_life_hours=3.5,
        bioavailability=0.8
    ),
    "insulin_regular": MedicationInfo(
        name="Regular Insulin",
        standard_dose_per_kg=0.1,  # 0.1-0.3 units/kg/day
        dose_unit=DoseUnit.UNITS,
        dose_range=DoseRange(0.1, 0.3, DoseUnit.UNITS),
        half_life_hours=0.25,  # 约15分钟
        routes=[Route.SC, Route.IV]
    ),
}


def get_medication(name: str) -> Optional[MedicationInfo]:
    """
    获取常用药物信息
    
    Args:
        name: 药物名称（通用名）
        
    Returns:
        药物信息，未找到返回 None
    """
    return COMMON_MEDICATIONS.get(name.lower().replace("-", "_").replace(" ", "_"))


def calculate_dose(
    medication_name: str,
    weight: float,
    weight_unit: WeightUnit = WeightUnit.KG
) -> Dict[str, Union[float, str, bool]]:
    """
    便捷函数：计算药物剂量
    
    Args:
        medication_name: 药物名称
        weight: 体重
        weight_unit: 体重单位
        
    Returns:
        计算结果字典
    """
    med = get_medication(medication_name)
    if not med:
        return {
            "success": False,
            "error": f"未找到药物: {medication_name}"
        }
    
    calculator = MedicationCalculator(med)
    dose = calculator.calculate_weight_based_dose(weight, weight_unit)
    validation = calculator.validate_dose(dose)
    
    return {
        "success": True,
        "medication": med.name,
        "weight_kg": MedicationCalculator._to_kg(weight, weight_unit),
        "calculated_dose": dose,
        "unit": med.dose_unit.value,
        "is_valid": validation["is_valid"],
        "warnings": validation.get("warnings", []),
        "errors": validation.get("errors", [])
    }
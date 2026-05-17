"""
Heart Rate Utils - 心率工具库

提供心率计算、训练区间、燃脂心率等功能，零外部依赖。

功能:
- 最大心率计算（多种公式：220-age, Tanaka, Gellish, Arena等）
- 心率训练区间（Zone 1-5）
- 目标心率计算（燃脂/有氧/无氧）
- 心率储备（Karvonen公式）
- 运动强度评估
- 年龄调整计算
- 卡路里消耗估算
- 心率变异性分析
- 恢复心率评估
"""

from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple, Callable
from enum import Enum
import math


class HeartRateZone(Enum):
    """心率训练区间"""
    ZONE_1 = "Zone 1"  # 恢复区间 50-60%
    ZONE_2 = "Zone 2"  # 有氧基础 60-70%
    ZONE_3 = "Zone 3"  # 有氧耐力 70-80%
    ZONE_4 = "Zone 4"  # 无氧阈值 80-90%
    ZONE_5 = "Zone 5"  # 最大努力 90-100%


class MaxHrFormula(Enum):
    """最大心率计算公式"""
    STANDARD = "standard"  # 220 - age
    TANAKA = "tanaka"  # 208 - 0.7 * age
    GELLISH = "gellish"  # 207 - 0.7 * age
    ARENA = "arena"  # 209.3 - 0.72 * age
    INBAR = "inbar"  # 205.8 - 0.685 * age
    NES = "nes"  # 211 - 0.64 * age
    RANSDAL = "ralsdal"  # 205.8 - 0.69 * age
    HUNT = "hunt"  # 211 - 0.64 * age (for healthy adults)
    GELLISH2 = "gellish2"  # 192 - 0.007 * age² (quadratic)


@dataclass
class HeartRateRange:
    """心率范围"""
    min_hr: int
    max_hr: int
    
    def __contains__(self, hr: int) -> bool:
        return self.min_hr <= hr <= self.max_hr
    
    def to_dict(self) -> Dict:
        return {"min": self.min_hr, "max": self.max_hr}


@dataclass
class ZoneInfo:
    """训练区间信息"""
    zone: HeartRateZone
    name: str
    description: str
    hr_range: HeartRateRange
    percentage_range: Tuple[int, int]
    benefits: List[str]
    duration_minutes: Tuple[int, int]  # 建议持续时间范围
    
    def to_dict(self) -> Dict:
        return {
            "zone": self.zone.value,
            "name": self.name,
            "description": self.description,
            "hr_range": self.hr_range.to_dict(),
            "percentage_range": self.percentage_range,
            "benefits": self.benefits,
            "duration_minutes": self.duration_minutes
        }


@dataclass
class HeartRateResult:
    """心率计算结果"""
    max_hr: int
    resting_hr: Optional[int]
    heart_rate_reserve: Optional[int]
    zones: Dict[str, ZoneInfo]
    formula_used: str
    
    def to_dict(self) -> Dict:
        return {
            "max_hr": self.max_hr,
            "resting_hr": self.resting_hr,
            "heart_rate_reserve": self.heart_rate_reserve,
            "zones": {k: v.to_dict() for k, v in self.zones.items()},
            "formula_used": self.formula_used
        }


class HeartRateUtils:
    """心率工具类"""
    
    # Zone 配置 (相对于最大心率的百分比)
    ZONE_CONFIG = {
        HeartRateZone.ZONE_1: {
            "name": "恢复区间",
            "description": "极轻强度，用于热身、冷身和恢复",
            "percentage": (50, 60),
            "benefits": [
                "促进恢复",
                "增强基础有氧能力",
                "适合初学者",
                "减少受伤风险"
            ],
            "duration": (20, 60)
        },
        HeartRateZone.ZONE_2: {
            "name": "有氧基础",
            "description": "轻强度，主要燃脂区间",
            "percentage": (60, 70),
            "benefits": [
                "提高脂肪燃烧效率",
                "增强心肺功能",
                "提高耐力",
                "适合长时间训练"
            ],
            "duration": (30, 120)
        },
        HeartRateZone.ZONE_3: {
            "name": "有氧耐力",
            "description": "中等强度，提高有氧能力",
            "percentage": (70, 80),
            "benefits": [
                "提高有氧能力",
                "增强心肺耐力",
                "提高乳酸阈值",
                "适合马拉松训练"
            ],
            "duration": (20, 60)
        },
        HeartRateZone.ZONE_4: {
            "name": "无氧阈值",
            "description": "高强度，接近乳酸阈值",
            "percentage": (80, 90),
            "benefits": [
                "提高最大摄氧量",
                "提高速度耐力",
                "增强快肌纤维",
                "提高竞技水平"
            ],
            "duration": (2, 10)
        },
        HeartRateZone.ZONE_5: {
            "name": "最大努力",
            "description": "极高强度，无氧区间",
            "percentage": (90, 100),
            "benefits": [
                "提高爆发力",
                "提高神经肌肉协调",
                "竞技训练",
                "间歇训练"
            ],
            "duration": (0, 5)
        }
    }
    
    @staticmethod
    def calculate_max_hr(age: int, formula: MaxHrFormula = MaxHrFormula.TANAKA) -> int:
        """
        计算最大心率
        
        Args:
            age: 年龄（岁）
            formula: 计算公式
        
        Returns:
            最大心率（bpm）
        
        Raises:
            ValueError: 年龄不在有效范围内
        """
        if not 1 <= age <= 120:
            raise ValueError("年龄应在1-120岁之间")
        
        if formula == MaxHrFormula.STANDARD:
            # 传统公式：220 - age
            return 220 - age
        elif formula == MaxHrFormula.TANAKA:
            # Tanaka公式（2001）：最准确
            return int(208 - 0.7 * age)
        elif formula == MaxHrFormula.GELLISH:
            # Gellish公式（2007）
            return int(207 - 0.7 * age)
        elif formula == MaxHrFormula.ARENA:
            # Arena公式（最大摄氧量相关）
            return int(209.3 - 0.72 * age)
        elif formula == MaxHrFormula.INBAR:
            # Inbar公式
            return int(205.8 - 0.685 * age)
        elif formula == MaxHrFormula.NES:
            # Nes公式（适用于健康成年人）
            return int(211 - 0.64 * age)
        elif formula == MaxHrFormula.RANSDAL:
            # Ransdal公式
            return int(205.8 - 0.69 * age)
        elif formula == MaxHrFormula.HUNT:
            # Hunt公式（适用于健康成年人）
            return int(211 - 0.64 * age)
        elif formula == MaxHrFormula.GELLISH2:
            # Gellish二次公式
            return int(192 - 0.007 * age * age)
        else:
            return 220 - age
    
    @staticmethod
    def calculate_max_hr_average(age: int) -> int:
        """
        使用多个公式计算平均最大心率
        
        Args:
            age: 年龄（岁）
        
        Returns:
            平均最大心率（bpm）
        """
        formulas = [
            MaxHrFormula.TANAKA,
            MaxHrFormula.GELLISH,
            MaxHrFormula.ARENA,
            MaxHrFormula.INBAR
        ]
        values = [HeartRateUtils.calculate_max_hr(age, f) for f in formulas]
        return int(sum(values) / len(values))
    
    @staticmethod
    def calculate_max_hr_range(age: int) -> Dict[str, int]:
        """
        计算最大心率范围（所有公式）
        
        Args:
            age: 年龄（岁）
        
        Returns:
            各公式的计算结果
        """
        return {
            MaxHrFormula.STANDARD.value: HeartRateUtils.calculate_max_hr(age, MaxHrFormula.STANDARD),
            MaxHrFormula.TANAKA.value: HeartRateUtils.calculate_max_hr(age, MaxHrFormula.TANAKA),
            MaxHrFormula.GELLISH.value: HeartRateUtils.calculate_max_hr(age, MaxHrFormula.GELLISH),
            MaxHrFormula.ARENA.value: HeartRateUtils.calculate_max_hr(age, MaxHrFormula.ARENA),
            MaxHrFormula.INBAR.value: HeartRateUtils.calculate_max_hr(age, MaxHrFormula.INBAR),
            MaxHrFormula.NES.value: HeartRateUtils.calculate_max_hr(age, MaxHrFormula.NES),
            MaxHrFormula.GELLISH2.value: HeartRateUtils.calculate_max_hr(age, MaxHrFormula.GELLISH2),
            "average": HeartRateUtils.calculate_max_hr_average(age)
        }
    
    @staticmethod
    def calculate_heart_rate_reserve(max_hr: int, resting_hr: int) -> int:
        """
        计算心率储备（Karvonen公式基础）
        
        HRR = Max HR - Resting HR
        
        Args:
            max_hr: 最大心率
            resting_hr: 静息心率
        
        Returns:
            心率储备
        """
        if resting_hr >= max_hr:
            raise ValueError("静息心率应小于最大心率")
        if resting_hr < 30:
            raise ValueError("静息心率应在30 bpm以上")
        return max_hr - resting_hr
    
    @staticmethod
    def calculate_target_hr_karvonen(max_hr: int, resting_hr: int, intensity: float) -> int:
        """
        使用Karvonen公式计算目标心率
        
        Target HR = (HRR × intensity) + resting_hr
        
        Args:
            max_hr: 最大心率
            resting_hr: 静息心率
            intensity: 目标强度（0.5-1.0，表示50%-100%）
        
        Returns:
            目标心率
        """
        if not 0.5 <= intensity <= 1.0:
            raise ValueError("强度应在50%-100%之间")
        
        hrr = HeartRateUtils.calculate_heart_rate_reserve(max_hr, resting_hr)
        return int(hrr * intensity + resting_hr)
    
    @staticmethod
    def calculate_target_hr_simple(max_hr: int, percentage: float) -> int:
        """
        使用简单百分比计算目标心率
        
        Target HR = Max HR × percentage
        
        Args:
            max_hr: 最大心率
            percentage: 目标百分比（0.5-1.0）
        
        Returns:
            目标心率
        """
        if not 0.5 <= percentage <= 1.0:
            raise ValueError("百分比应在50%-100%之间")
        return int(max_hr * percentage)
    
    @staticmethod
    def calculate_zones(
        age: int,
        resting_hr: Optional[int] = None,
        formula: MaxHrFormula = MaxHrFormula.TANAKA,
        use_karvonen: bool = False
    ) -> HeartRateResult:
        """
        计算所有心率训练区间
        
        Args:
            age: 年龄
            resting_hr: 静息心率（用于Karvonen公式）
            formula: 最大心率计算公式
            use_karvonen: 是否使用Karvonen公式
        
        Returns:
            HeartRateResult 包含所有区间信息
        """
        max_hr = HeartRateUtils.calculate_max_hr(age, formula)
        hrr = None
        
        if use_karvonen and resting_hr:
            hrr = HeartRateUtils.calculate_heart_rate_reserve(max_hr, resting_hr)
        
        zones = {}
        for zone_enum in HeartRateZone:
            config = HeartRateUtils.ZONE_CONFIG[zone_enum]
            pct_min, pct_max = config["percentage"]
            
            if use_karvonen and resting_hr:
                # Karvonen公式
                hr_min = int(hrr * (pct_min / 100) + resting_hr)
                hr_max = int(hrr * (pct_max / 100) + resting_hr)
            else:
                # 简单百分比
                hr_min = int(max_hr * pct_min / 100)
                hr_max = int(max_hr * pct_max / 100)
            
            zones[zone_enum.value] = ZoneInfo(
                zone=zone_enum,
                name=config["name"],
                description=config["description"],
                hr_range=HeartRateRange(hr_min, hr_max),
                percentage_range=(pct_min, pct_max),
                benefits=config["benefits"],
                duration_minutes=config["duration"]
            )
        
        return HeartRateResult(
            max_hr=max_hr,
            resting_hr=resting_hr,
            heart_rate_reserve=hrr,
            zones=zones,
            formula_used=formula.value
        )
    
    @staticmethod
    def get_zone_for_hr(
        hr: int,
        age: int,
        resting_hr: Optional[int] = None,
        formula: MaxHrFormula = MaxHrFormula.TANAKA,
        use_karvonen: bool = False
    ) -> Optional[ZoneInfo]:
        """
        根据心率获取当前训练区间
        
        Args:
            hr: 当前心率
            age: 年龄
            resting_hr: 静息心率
            formula: 最大心率公式
            use_karvonen: 是否使用Karvonen公式
        
        Returns:
            ZoneInfo 或 None（如果心率超出范围）
        """
        result = HeartRateUtils.calculate_zones(age, resting_hr, formula, use_karvonen)
        
        for zone_info in result.zones.values():
            if hr in zone_info.hr_range:
                return zone_info
        
        return None
    
    @staticmethod
    def calculate_fat_burning_zone(age: int, resting_hr: Optional[int] = None) -> Dict:
        """
        计算最佳燃脂心率区间
        
        燃脂区间通常在最大心率的60-70%
        
        Args:
            age: 年龄
            resting_hr: 静息心率（可选）
        
        Returns:
            燃脂区间信息
        """
        result = HeartRateUtils.calculate_zones(age, resting_hr)
        zone2 = result.zones["Zone 2"]
        
        return {
            "zone_name": zone2.name,
            "hr_range": zone2.hr_range.to_dict(),
            "percentage": (60, 70),
            "optimal_hr": int((zone2.hr_range.min_hr + zone2.hr_range.max_hr) / 2),
            "description": "此区间脂肪供能比例最高，适合减脂训练",
            "recommended_duration_minutes": (30, 90)
        }
    
    @staticmethod
    def calculate_cardio_zone(age: int, resting_hr: Optional[int] = None) -> Dict:
        """
        计算有氧训练心率区间
        
        有氧区间在最大心率的70-80%
        
        Args:
            age: 年龄
            resting_hr: 静息心率（可选）
        
        Returns:
            有氧区间信息
        """
        result = HeartRateUtils.calculate_zones(age, resting_hr)
        zone3 = result.zones["Zone 3"]
        
        return {
            "zone_name": zone3.name,
            "hr_range": zone3.hr_range.to_dict(),
            "percentage": (70, 80),
            "description": "此区间提高有氧能力，适合提高心肺耐力",
            "recommended_duration_minutes": (20, 60)
        }
    
    @staticmethod
    def calculate_anaerobic_zone(age: int, resting_hr: Optional[int] = None) -> Dict:
        """
        计算无氧训练心率区间
        
        无氧区间在最大心率的80-90%
        
        Args:
            age: 年龄
            resting_hr: 静息心率（可选）
        
        Returns:
            无氧区间信息
        """
        result = HeartRateUtils.calculate_zones(age, resting_hr)
        zone4 = result.zones["Zone 4"]
        
        return {
            "zone_name": zone4.name,
            "hr_range": zone4.hr_range.to_dict(),
            "percentage": (80, 90),
            "description": "此区间提高无氧能力和乳酸阈值",
            "recommended_duration_minutes": (2, 10)
        }
    
    @staticmethod
    def estimate_calories_burned(
        hr: int,
        duration_minutes: float,
        weight_kg: float,
        age: int,
        gender: str = "male"
    ) -> Dict:
        """
        估算卡路里消耗（基于心率）
        
        使用Keytel公式（心率法）
        
        Args:
            hr: 平均心率
            duration_minutes: 运动时长（分钟）
            weight_kg: 体重（公斤）
            age: 年龄
            gender: 性别（male/female）
        
        Returns:
            卡路里消耗信息
        """
        if gender.lower() not in ("male", "female", "m", "f"):
            raise ValueError("性别应为 male 或 female")
        
        is_male = gender.lower() in ("male", "m")
        
        # Keytel公式
        if is_male:
            calories = (-55.0969 + 0.6309 * hr + 0.1988 * weight_kg + 0.2017 * age) * duration_minutes / 4.184
        else:
            calories = (-20.4022 + 0.4472 * hr - 0.1263 * weight_kg + 0.074 * age) * duration_minutes / 4.184
        
        calories = max(0, int(calories))
        
        # 计算MET值估算
        # 粗略估算：休息=1，轻度=3，中度=5，重度=7，极重=9+
        max_hr = HeartRateUtils.calculate_max_hr(age)
        hr_percentage = hr / max_hr
        
        if hr_percentage < 0.5:
            met = 2
            intensity = "极轻"
        elif hr_percentage < 0.6:
            met = 3
            intensity = "轻度"
        elif hr_percentage < 0.7:
            met = 5
            intensity = "中等"
        elif hr_percentage < 0.8:
            met = 7
            intensity = "较高"
        elif hr_percentage < 0.9:
            met = 9
            intensity = "高强度"
        else:
            met = 11
            intensity = "极高强度"
        
        return {
            "calories": calories,
            "duration_minutes": duration_minutes,
            "average_hr": hr,
            "intensity": intensity,
            "met_estimate": met,
            "formula": "Keytel (heart rate based)"
        }
    
    @staticmethod
    def calculate_recovery_hr(
        hr_exercise: int,
        hr_recovery_1min: int,
        hr_recovery_2min: Optional[int] = None
    ) -> Dict:
        """
        计算恢复心率（评估心脏健康）
        
        Args:
            hr_exercise: 运动时心率
            hr_recovery_1min: 运动后1分钟心率
            hr_recovery_2min: 运动后2分钟心率（可选）
        
        Returns:
            恢复评估结果
        """
        drop_1min = hr_exercise - hr_recovery_1min
        
        # 恢复评估
        if drop_1min >= 25:
            rating = "优秀"
            risk = "低风险"
            description = "心脏恢复能力很好"
        elif drop_1min >= 15:
            rating = "良好"
            risk = "较低风险"
            description = "心脏恢复能力正常"
        elif drop_1min >= 10:
            rating = "一般"
            risk = "中等风险"
            description = "心脏恢复能力一般，建议加强锻炼"
        else:
            rating = "较差"
            risk = "较高风险"
            description = "心脏恢复能力较差，建议咨询医生"
        
        result = {
            "hr_drop_1min": drop_1min,
            "recovery_rating": rating,
            "health_risk": risk,
            "description": description,
            "hr_exercise": hr_exercise,
            "hr_recovery_1min": hr_recovery_1min
        }
        
        if hr_recovery_2min:
            drop_2min = hr_exercise - hr_recovery_2min
            result["hr_drop_2min"] = drop_2min
            result["hr_recovery_2min"] = hr_recovery_2min
            
            # 2分钟恢复评估
            if drop_2min >= 40:
                result["rating_2min"] = "优秀"
            elif drop_2min >= 30:
                result["rating_2min"] = "良好"
            elif drop_2min >= 20:
                result["rating_2min"] = "一般"
            else:
                result["rating_2min"] = "较差"
        
        return result
    
    @staticmethod
    def assess_cardiovascular_fitness(
        resting_hr: int,
        age: int,
        gender: str = "male"
    ) -> Dict:
        """
        评估心血管健康水平（基于静息心率）
        
        Args:
            resting_hr: 静息心率
            age: 年龄
            gender: 性别
        
        Returns:
            心血管健康评估
        """
        if gender.lower() not in ("male", "female", "m", "f"):
            raise ValueError("性别应为 male 或 female")
        
        is_male = gender.lower() in ("male", "m")
        
        # 基于年龄和性别的静息心率评估
        if is_male:
            if resting_hr < 50:
                level = "运动员级别"
                rating = "优秀"
            elif resting_hr < 60:
                level = "优秀"
                rating = "很好"
            elif resting_hr < 70:
                level = "良好"
                rating = "良好"
            elif resting_hr < 80:
                level = "一般"
                rating = "一般"
            elif resting_hr < 90:
                level = "偏低"
                rating = "需要改善"
            else:
                level = "较差"
                rating = "建议就医"
        else:
            if resting_hr < 54:
                level = "运动员级别"
                rating = "优秀"
            elif resting_hr < 64:
                level = "优秀"
                rating = "很好"
            elif resting_hr < 74:
                level = "良好"
                rating = "良好"
            elif resting_hr < 84:
                level = "一般"
                rating = "一般"
            elif resting_hr < 94:
                level = "偏低"
                rating = "需要改善"
            else:
                level = "较差"
                rating = "建议就医"
        
        return {
            "resting_hr": resting_hr,
            "age": age,
            "gender": gender,
            "fitness_level": level,
            "rating": rating,
            "reference_range": "60-100 bpm (正常范围)",
            "description": f"您的静息心率{resting_hr} bpm，心血管健康水平为{level}"
        }
    
    @staticmethod
    def calculate_training_intensity(
        hr: int,
        age: int,
        resting_hr: Optional[int] = None,
        formula: MaxHrFormula = MaxHrFormula.TANAKA
    ) -> Dict:
        """
        计算训练强度百分比
        
        Args:
            hr: 当前心率
            age: 年龄
            resting_hr: 静息心率
            formula: 最大心率公式
        
        Returns:
            训练强度信息
        """
        max_hr = HeartRateUtils.calculate_max_hr(age, formula)
        
        if hr > max_hr:
            raise ValueError(f"心率{hr}超过计算的最大心率{max_hr}")
        
        # 简单百分比
        simple_pct = (hr / max_hr) * 100
        
        # Karvonen百分比
        karvonen_pct = None
        if resting_hr:
            hrr = HeartRateUtils.calculate_heart_rate_reserve(max_hr, resting_hr)
            karvonen_pct = ((hr - resting_hr) / hrr) * 100
        
        # 获取区间
        zone_info = HeartRateUtils.get_zone_for_hr(hr, age, resting_hr, formula)
        
        # 强度描述
        if simple_pct < 50:
            intensity = "极轻"
            color = "灰色"
        elif simple_pct < 60:
            intensity = "轻度"
            color = "蓝色"
        elif simple_pct < 70:
            intensity = "中等"
            color = "绿色"
        elif simple_pct < 80:
            intensity = "较高"
            color = "黄色"
        elif simple_pct < 90:
            intensity = "高强度"
            color = "橙色"
        else:
            intensity = "极量"
            color = "红色"
        
        return {
            "current_hr": hr,
            "max_hr": max_hr,
            "percentage_of_max": round(simple_pct, 1),
            "karvonen_percentage": round(karvonen_pct, 1) if karvonen_pct else None,
            "intensity_level": intensity,
            "color_code": color,
            "zone": zone_info.name if zone_info else "超出范围",
            "zone_description": zone_info.description if zone_info else ""
        }
    
    @staticmethod
    def calculate_lactate_threshold_hr(
        age: int,
        resting_hr: Optional[int] = None,
        method: str = "percentage"
    ) -> Dict:
        """
        估算乳酸阈值心率
        
        乳酸阈值通常在最大心率的85-90%
        
        Args:
            age: 年龄
            resting_hr: 静息心率
            method: 计算方法 ('percentage' 或 'formula')
        
        Returns:
            乳酸阈值心率信息
        """
        max_hr = HeartRateUtils.calculate_max_hr(age)
        
        if method == "percentage":
            # 使用百分比法
            lt_min = int(max_hr * 0.85)
            lt_max = int(max_hr * 0.90)
        else:
            # 使用公式法（更保守）
            lt_min = int(max_hr * 0.83)
            lt_max = int(max_hr * 0.88)
        
        return {
            "lactate_threshold_range": {
                "min": lt_min,
                "max": lt_max
            },
            "percentage_of_max_hr": "85-90%",
            "max_hr": max_hr,
            "description": "乳酸阈值心率是高强度训练的重要参考值",
            "training_tip": "接近或超过此区间时，乳酸积累加快，难以长时间维持"
        }
    
    @staticmethod
    def hr_to_pace_estimate(
        hr: int,
        age: int,
        weight_kg: float,
        activity: str = "running"
    ) -> Dict:
        """
        根据心率估算运动配速（仅作参考）
        
        Args:
            hr: 心率
            age: 年龄
            weight_kg: 体重
            activity: 运动类型 (running, cycling, swimming)
        
        Returns:
            配速估算
        """
        max_hr = HeartRateUtils.calculate_max_hr(age)
        percentage = hr / max_hr
        
        if activity == "running":
            # 跑步配速估算（分钟/公里）
            # 假设最大心率对应4分钟/公里
            if percentage >= 0.95:
                pace = 4.0
                intensity = "冲刺"
            elif percentage >= 0.90:
                pace = 4.5
                intensity = "5公里比赛配速"
            elif percentage >= 0.85:
                pace = 5.0
                intensity = "10公里比赛配速"
            elif percentage >= 0.80:
                pace = 5.5
                intensity = "半马配速"
            elif percentage >= 0.75:
                pace = 6.0
                intensity = "马拉松配速"
            elif percentage >= 0.70:
                pace = 6.5
                intensity = "节奏跑"
            elif percentage >= 0.65:
                pace = 7.5
                intensity = "轻松跑"
            elif percentage >= 0.60:
                pace = 8.5
                intensity = "恢复跑"
            else:
                pace = 10.0
                intensity = "热身/冷身"
            
            pace_min = pace - 0.3
            pace_max = pace + 0.3
            
            return {
                "activity": "跑步",
                "estimated_pace_min_per_km": round(pace, 2),
                "pace_range": {
                    "min": round(pace_min, 2),
                    "max": round(pace_max, 2)
                },
                "intensity": intensity,
                "note": "配速估算因个人能力差异较大，仅供参考"
            }
        
        elif activity == "cycling":
            # 骑行速度估算（公里/小时）
            if percentage >= 0.90:
                speed = 35
                intensity = "冲刺"
            elif percentage >= 0.80:
                speed = 30
                intensity = "高强度"
            elif percentage >= 0.70:
                speed = 25
                intensity = "中等"
            elif percentage >= 0.60:
                speed = 20
                intensity = "轻松"
            else:
                speed = 15
                intensity = "恢复"
            
            return {
                "activity": "骑行",
                "estimated_speed_kmh": speed,
                "intensity": intensity,
                "note": "速度估算受地形、风速、自行车类型影响较大"
            }
        
        elif activity == "swimming":
            # 游泳配速估算（分钟/100米）
            if percentage >= 0.85:
                pace = 1.5
                intensity = "比赛配速"
            elif percentage >= 0.75:
                pace = 1.8
                intensity = "高强度"
            elif percentage >= 0.65:
                pace = 2.2
                intensity = "中等"
            else:
                pace = 2.8
                intensity = "轻松"
            
            return {
                "activity": "游泳",
                "estimated_pace_min_per_100m": pace,
                "intensity": intensity,
                "note": "配速受游泳技术影响较大"
            }
        
        else:
            raise ValueError("运动类型应为 running, cycling 或 swimming")
    
    @staticmethod
    def analyze_hr_trend(hr_readings: List[int], timestamps: Optional[List[float]] = None) -> Dict:
        """
        分析心率趋势
        
        Args:
            hr_readings: 心率读数列表
            timestamps: 时间戳列表（可选）
        
        Returns:
            心率趋势分析结果
        """
        if not hr_readings:
            raise ValueError("心率读数不能为空")
        
        n = len(hr_readings)
        
        # 基本统计
        avg_hr = sum(hr_readings) / n
        min_hr = min(hr_readings)
        max_hr = max(hr_readings)
        
        # 排序后计算中位数
        sorted_hr = sorted(hr_readings)
        median_hr = sorted_hr[n // 2] if n % 2 == 1 else (sorted_hr[n // 2 - 1] + sorted_hr[n // 2]) / 2
        
        # 标准差
        variance = sum((x - avg_hr) ** 2 for x in hr_readings) / n
        std_dev = math.sqrt(variance)
        
        # 变异系数
        cv = (std_dev / avg_hr) * 100 if avg_hr > 0 else 0
        
        # 心率变异性（RMSSD估算，简化版）
        if n >= 2:
            differences = [abs(hr_readings[i + 1] - hr_readings[i]) for i in range(n - 1)]
            rmssd = math.sqrt(sum(d * d for d in differences) / len(differences))
        else:
            rmssd = 0
        
        # 趋势方向（基于首尾比较）
        if n >= 3:
            # 使用前后段平均值比较
            first_third = hr_readings[:n // 3]
            last_third = hr_readings[-(n // 3):] if n // 3 > 0 else hr_readings[-1:]
            first_avg = sum(first_third) / len(first_third)
            last_avg = sum(last_third) / len(last_third)
            diff = last_avg - first_avg
            if diff > 2:
                trend = "上升"
            elif diff < -2:
                trend = "下降"
            else:
                trend = "平稳"
        else:
            trend = "数据不足"
        
        return {
            "count": n,
            "average_hr": round(avg_hr, 1),
            "min_hr": min_hr,
            "max_hr": max_hr,
            "median_hr": round(median_hr, 1),
            "std_deviation": round(std_dev, 2),
            "coefficient_of_variation": round(cv, 2),
            "hr_range": max_hr - min_hr,
            "rmssd_estimate": round(rmssd, 2),
            "trend": trend,
            "stability": "稳定" if cv < 5 else "较稳定" if cv < 10 else "波动较大"
        }


# 便捷函数
def calculate_max_hr(age: int, formula: str = "tanaka") -> int:
    """便捷函数：计算最大心率"""
    formula_map = {
        "standard": MaxHrFormula.STANDARD,
        "tanaka": MaxHrFormula.TANAKA,
        "gellish": MaxHrFormula.GELLISH,
        "arena": MaxHrFormula.ARENA,
        "inbar": MaxHrFormula.INBAR,
        "nes": MaxHrFormula.NES,
        "gellish2": MaxHrFormula.GELLISH2
    }
    f = formula_map.get(formula.lower(), MaxHrFormula.TANAKA)
    return HeartRateUtils.calculate_max_hr(age, f)


def get_zones(age: int, resting_hr: Optional[int] = None, use_karvonen: bool = False) -> Dict:
    """便捷函数：获取心率区间"""
    result = HeartRateUtils.calculate_zones(age, resting_hr, use_karvonen=use_karvonen)
    return result.to_dict()


def get_fat_burning_hr(age: int) -> Dict:
    """便捷函数：获取燃脂心率区间"""
    return HeartRateUtils.calculate_fat_burning_zone(age)


def get_current_zone(hr: int, age: int, resting_hr: Optional[int] = None) -> Optional[Dict]:
    """便捷函数：获取当前心率区间"""
    zone = HeartRateUtils.get_zone_for_hr(hr, age, resting_hr)
    return zone.to_dict() if zone else None


def estimate_calories(hr: int, duration_min: float, weight_kg: float, age: int, gender: str = "male") -> int:
    """便捷函数：估算卡路里消耗"""
    result = HeartRateUtils.estimate_calories_burned(hr, duration_min, weight_kg, age, gender)
    return result["calories"]


def assess_fitness(resting_hr: int, age: int, gender: str = "male") -> Dict:
    """便捷函数：评估心血管健康"""
    return HeartRateUtils.assess_cardiovascular_fitness(resting_hr, age, gender)


if __name__ == "__main__":
    # 示例使用
    print("=== 心率工具库示例 ===\n")
    
    age = 30
    
    # 最大心率
    print(f"最大心率（Tanaka公式）: {HeartRateUtils.calculate_max_hr(age)} bpm")
    print(f"最大心率（传统公式）: {HeartRateUtils.calculate_max_hr(age, MaxHrFormula.STANDARD)} bpm")
    
    # 各公式对比
    print("\n各公式计算结果:")
    for formula, value in HeartRateUtils.calculate_max_hr_range(age).items():
        print(f"  {formula}: {value} bpm")
    
    # 心率区间
    print("\n心率训练区间:")
    result = HeartRateUtils.calculate_zones(age)
    for zone_name, zone_info in result.zones.items():
        print(f"  {zone_name} ({zone_info.name}): {zone_info.hr_range.min_hr}-{zone_info.hr_range.max_hr} bpm")
    
    # 燃脂区间
    print("\n燃脂区间:")
    fat_zone = HeartRateUtils.calculate_fat_burning_zone(age)
    print(f"  心率范围: {fat_zone['hr_range']['min']}-{fat_zone['hr_range']['max']} bpm")
    print(f"  最佳心率: {fat_zone['optimal_hr']} bpm")
    
    # 卡路里消耗
    print("\n卡路里消耗估算（心率150，运动45分钟，体重70kg，30岁男性）:")
    calories = HeartRateUtils.estimate_calories_burned(150, 45, 70, 30, "male")
    print(f"  消耗: {calories['calories']} kcal")
    print(f"  强度: {calories['intensity']}")
    
    # 恢复心率评估
    print("\n恢复心率评估（运动心率160，1分钟后120）:")
    recovery = HeartRateUtils.calculate_recovery_hr(160, 120)
    print(f"  1分钟下降: {recovery['hr_drop_1min']} bpm")
    print(f"  评估: {recovery['recovery_rating']} ({recovery['health_risk']})")
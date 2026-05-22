"""
Water Intake Utils - 饮水量计算工具
==========================================

提供各种饮水量相关的计算功能，无需外部依赖。

功能列表:
- 每日饮水量建议计算（基于体重）
- 运动量调整系数
- 气温环境调整系数
- 饮水记录管理
- 饮水提醒时间表生成
- 饮水进度跟踪
- 健康饮水建议

作者: AllToolkit 自动化生成
日期: 2026-05-23
"""

from typing import Dict, Any, Tuple, List, Optional
from enum import Enum
from datetime import datetime, timedelta
import math


class ActivityLevel(Enum):
    """活动水平枚举"""
    SEDENTARY = "sedentary"          # 久坐（很少或无运动）
    LIGHT = "light"                  # 轻度活动（每周1-3天轻度运动）
    MODERATE = "moderate"            # 中度活动（每周3-5天中度运动）
    ACTIVE = "active"                # 活跃（每周6-7天运动）
    VERY_ACTIVE = "very_active"      # 非常活跃（剧烈运动或体力劳动）


class ClimateType(Enum):
    """气候类型枚举"""
    COLD = "cold"                    # 寒冷（<10°C）
    MILD = "mild"                    # 温和（10-20°C）
    WARM = "warm"                    # 温暖（20-25°C）
    HOT = "hot"                      # 炎热（25-35°C）
    VERY_HOT = "very_hot"            # 酷热（>35°C）
    HUMID = "humid"                  # 潮湿（高湿度）


class HydrationStatus(Enum):
    """补水状态枚举"""
    DEHYDRATED_SEVERE = "dehydrated_severe"   # 严重脱水
    DEHYDRATED = "dehydrated"                  # 脱水
    SLIGHTLY_DEHYDRATED = "slightly_dehydrated"  # 轻度脱水
    WELL_HYDRATED = "well_hydrated"           # 补水良好
    OPTIMAL = "optimal"                        # 最佳状态
    OVERHYDRATED = "overhydrated"              # 饮水过量


class WaterIntakeCalculator:
    """饮水量计算器"""
    
    # 基础饮水量系数（毫升/公斤体重/天）
    BASE_WATER_COEFFICIENT = 30  # 常用标准：30ml/kg
    
    # 活动水平调整系数
    ACTIVITY_MULTIPLIERS = {
        ActivityLevel.SEDENTARY: 1.0,
        ActivityLevel.LIGHT: 1.1,
        ActivityLevel.MODERATE: 1.2,
        ActivityLevel.ACTIVE: 1.3,
        ActivityLevel.VERY_ACTIVE: 1.5
    }
    
    # 运动时额外补水量（毫升/30分钟运动）
    EXERCISE_WATER_ADDITION = 350
    
    # 气候调整系数
    CLIMATE_MULTIPLIERS = {
        ClimateType.COLD: 0.9,
        ClimateType.MILD: 1.0,
        ClimateType.WARM: 1.1,
        ClimateType.HOT: 1.2,
        ClimateType.VERY_HOT: 1.4,
        ClimateType.HUMID: 1.15
    }
    
    # 特殊情况调整（毫升）
    SPECIAL_CONDITIONS = {
        'pregnancy': 300,           # 孕期
        'breastfeeding': 700,       # 哺乳期
        'illness_fever': 500,       # 发烧
        'altitude_high': 500,       # 高海拔
        'alcohol': 500,             # 饮酒后
        'caffeine': 200,            # 高咖啡因摄入
        'high_protein_diet': 250,   # 高蛋白饮食
        'high_fiber_diet': 200      # 高纤维饮食
    }
    
    # 饮水时间建议
    RECOMMENDED_DRINKING_TIMES = [
        (7, 0, "起床后"),          # 7:00
        (9, 0, "工作开始"),        # 9:00
        (11, 30, "午饭前"),        # 11:30
        (13, 0, "午饭后"),         # 13:00
        (15, 0, "下午茶时间"),     # 15:00
        (17, 30, "下班前"),        # 17:30
        (19, 0, "晚餐时"),         # 19:00
        (21, 0, "睡前一小时")      # 21:00
    ]
    
    def __init__(self):
        """初始化饮水计算器"""
        self.records: List[Dict[str, Any]] = []
    
    def calculate_daily_intake(
        self,
        weight_kg: float,
        activity_level: ActivityLevel = ActivityLevel.MODERATE,
        climate: ClimateType = ClimateType.MILD,
        exercise_minutes: int = 0,
        special_conditions: Optional[List[str]] = None,
        age: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        计算每日建议饮水量
        
        Args:
            weight_kg: 体重（公斤）
            activity_level: 活动水平
            climate: 气候类型
            exercise_minutes: 额外运动时间（分钟）
            special_conditions: 特殊情况列表
            age: 年龄（可选，用于调整）
        
        Returns:
            包含详细计算结果的字典
        """
        if weight_kg <= 0:
            raise ValueError("体重必须大于0")
        
        special_conditions = special_conditions or []
        
        # 基础饮水量
        base_intake = weight_kg * self.BASE_WATER_COEFFICIENT
        
        # 活动水平调整
        activity_multiplier = self.ACTIVITY_MULTIPLIERS.get(activity_level, 1.0)
        activity_adjusted = base_intake * activity_multiplier
        
        # 运动量调整
        exercise_addition = (exercise_minutes / 30) * self.EXERCISE_WATER_ADDITION
        
        # 气候调整
        climate_multiplier = self.CLIMATE_MULTIPLIERS.get(climate, 1.0)
        climate_adjusted = (activity_adjusted + exercise_addition) * climate_multiplier
        
        # 特殊情况调整
        special_addition = sum(
            self.SPECIAL_CONDITIONS.get(condition, 0)
            for condition in special_conditions
        )
        
        # 年龄调整
        age_adjustment = 0
        if age is not None:
            if age < 18:
                # 青少年需要相对更多的水
                age_adjustment = base_intake * 0.1
            elif age > 65:
                # 老年人可能需要减少（肾脏功能下降）
                age_adjustment = -base_intake * 0.05
        
        # 总饮水量
        total_intake = climate_adjusted + special_addition + age_adjustment
        
        # 确保在合理范围内
        min_intake = 1500  # 最小1500ml
        max_intake = 4500  # 最大4500ml
        total_intake = max(min_intake, min(max_intake, total_intake))
        
        return {
            'base_intake_ml': round(base_intake),
            'activity_level': activity_level.value,
            'activity_multiplier': activity_multiplier,
            'activity_adjusted_ml': round(activity_adjusted),
            'exercise_minutes': exercise_minutes,
            'exercise_addition_ml': round(exercise_addition),
            'climate': climate.value,
            'climate_multiplier': climate_multiplier,
            'climate_adjusted_ml': round(climate_adjusted),
            'special_conditions': special_conditions,
            'special_addition_ml': round(special_addition),
            'age_adjustment_ml': round(age_adjustment),
            'total_intake_ml': round(total_intake),
            'total_intake_liters': round(total_intake / 1000, 2),
            'glasses_of_water': round(total_intake / 250),  # 约250ml一杯
            'weight_kg': weight_kg
        }
    
    def calculate_hourly_intake(
        self,
        daily_intake_ml: float,
        waking_hours: int = 16
    ) -> Dict[str, Any]:
        """
        计算每小时建议饮水量
        
        Args:
            daily_intake_ml: 每日总饮水量（毫升）
            waking_hours: 清醒时间（小时）
        
        Returns:
            包含每小时饮水建议的字典
        """
        if daily_intake_ml <= 0:
            raise ValueError("每日饮水量必须大于0")
        if waking_hours <= 0:
            raise ValueError("清醒时间必须大于0")
        
        hourly_intake = daily_intake_ml / waking_hours
        
        return {
            'daily_intake_ml': round(daily_intake_ml),
            'waking_hours': waking_hours,
            'hourly_intake_ml': round(hourly_intake),
            'suggested_interval_minutes': round(60 / (hourly_intake / 250) * 30),
            'sips_per_hour': round(hourly_intake / 30),  # 每口约30ml
            'bottles_500ml': round(daily_intake_ml / 500, 1)
        }
    
    def generate_drinking_schedule(
        self,
        daily_intake_ml: float,
        wake_time: Tuple[int, int] = (7, 0),
        sleep_time: Tuple[int, int] = (23, 0),
        num_reminders: int = 8
    ) -> List[Dict[str, Any]]:
        """
        生成饮水时间表
        
        Args:
            daily_intake_ml: 每日总饮水量
            wake_time: 起床时间（小时，分钟）
            sleep_time: 睡眠时间（小时，分钟）
            num_reminders: 提醒次数
        
        Returns:
            饮水时间表列表
        """
        if daily_intake_ml <= 0:
            raise ValueError("每日饮水量必须大于0")
        
        wake_minutes = wake_time[0] * 60 + wake_time[1]
        sleep_minutes = sleep_time[0] * 60 + sleep_time[1]
        
        if sleep_minutes <= wake_minutes:
            sleep_minutes += 24 * 60  # 跨日
        
        total_minutes = sleep_minutes - wake_minutes
        interval = total_minutes / (num_reminders + 1)
        amount_per_reminder = daily_intake_ml / num_reminders
        
        schedule = []
        for i in range(num_reminders):
            reminder_minutes = wake_minutes + interval * (i + 1)
            hours = int(reminder_minutes // 60) % 24
            minutes = int(reminder_minutes % 60)
            
            # 根据时间段调整饮水量
            adjustment = 1.0
            time_note = ""
            
            if 7 <= hours < 9:
                time_note = "早晨补水，唤醒身体"
            elif 11 <= hours < 13:
                time_note = "午餐前补水"
            elif 17 <= hours < 19:
                time_note = "晚餐时段，适量饮水"
            elif hours >= 21:
                adjustment = 0.7
                time_note = "睡前，减少饮水避免夜起"
            else:
                time_note = "日常补水时间"
            
            schedule.append({
                'reminder_number': i + 1,
                'time': f"{hours:02d}:{minutes:02d}",
                'hours': hours,
                'minutes': minutes,
                'amount_ml': round(amount_per_reminder * adjustment),
                'cumulative_ml': round(amount_per_reminder * (i + 1)),
                'percentage': round((i + 1) / num_reminders * 100, 1),
                'note': time_note
            })
        
        return schedule
    
    def record_intake(
        self,
        amount_ml: float,
        timestamp: Optional[datetime] = None,
        beverage_type: str = "water",
        note: str = ""
    ) -> Dict[str, Any]:
        """
        记录饮水量
        
        Args:
            amount_ml: 饮水量（毫升）
            timestamp: 时间戳（可选，默认当前时间）
            beverage_type: 饮料类型
            note: 备注
        
        Returns:
            记录详情
        """
        if amount_ml <= 0:
            raise ValueError("饮水量必须大于0")
        
        timestamp = timestamp or datetime.now()
        
        record = {
            'id': len(self.records) + 1,
            'amount_ml': round(amount_ml),
            'timestamp': timestamp.isoformat(),
            'date': timestamp.strftime('%Y-%m-%d'),
            'time': timestamp.strftime('%H:%M:%S'),
            'beverage_type': beverage_type,
            'note': note
        }
        
        self.records.append(record)
        return record
    
    def get_daily_summary(
        self,
        date: Optional[str] = None,
        target_intake_ml: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        获取每日饮水摘要
        
        Args:
            date: 日期字符串（YYYY-MM-DD），默认今天
            target_intake_ml: 目标饮水量（可选）
        
        Returns:
            每日摘要
        """
        date = date or datetime.now().strftime('%Y-%m-%d')
        
        daily_records = [
            r for r in self.records
            if r['date'] == date
        ]
        
        total_intake = sum(r['amount_ml'] for r in daily_records)
        
        # 按饮料类型分组
        by_type: Dict[str, float] = {}
        for r in daily_records:
            beverage = r['beverage_type']
            by_type[beverage] = by_type.get(beverage, 0) + r['amount_ml']
        
        result = {
            'date': date,
            'total_intake_ml': round(total_intake),
            'total_intake_liters': round(total_intake / 1000, 2),
            'record_count': len(daily_records),
            'records': daily_records,
            'by_beverage_type': {k: round(v) for k, v in by_type.items()},
            'average_per_record': round(total_intake / len(daily_records)) if daily_records else 0
        }
        
        if target_intake_ml:
            progress = (total_intake / target_intake_ml) * 100
            result.update({
                'target_intake_ml': round(target_intake_ml),
                'progress_percentage': round(min(progress, 100), 1),
                'remaining_ml': round(max(0, target_intake_ml - total_intake)),
                'target_met': total_intake >= target_intake_ml
            })
        
        return result
    
    def assess_hydration(
        self,
        current_intake_ml: float,
        target_intake_ml: float,
        urine_color: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        评估补水状态
        
        Args:
            current_intake_ml: 当前饮水量
            target_intake_ml: 目标饮水量
            urine_color: 尿液颜色（可选：pale_yellow, yellow, dark_yellow, amber, clear）
        
        Returns:
            补水状态评估
        """
        if target_intake_ml <= 0:
            raise ValueError("目标饮水量必须大于0")
        
        ratio = current_intake_ml / target_intake_ml
        
        # 基于饮水量比例确定状态
        if ratio < 0.5:
            status = HydrationStatus.DEHYDRATED_SEVERE
            warning = "严重脱水！请立即增加饮水量"
        elif ratio < 0.7:
            status = HydrationStatus.DEHYDRATED
            warning = "脱水状态，需要增加饮水"
        elif ratio < 0.9:
            status = HydrationStatus.SLIGHTLY_DEHYDRATED
            warning = "轻度脱水，继续补水"
        elif ratio <= 1.1:
            status = HydrationStatus.OPTIMAL
            warning = "补水状态良好"
        elif ratio <= 1.3:
            status = HydrationStatus.WELL_HYDRATED
            warning = "补水充足"
        else:
            status = HydrationStatus.OVERHYDRATED
            warning = "饮水过量，适当减少"
        
        # 尿液颜色辅助判断
        urine_assessment = None
        if urine_color:
            color_map = {
                'pale_yellow': ('补水良好', True),
                'yellow': ('需要补水', False),
                'dark_yellow': ('脱水', False),
                'amber': ('严重脱水', False),
                'clear': ('饮水过量', True)
            }
            if urine_color in color_map:
                urine_assessment = {
                    'color': urine_color,
                    'assessment': color_map[urine_color][0],
                    'normal': color_map[urine_color][1]
                }
        
        return {
            'status': status.value,
            'status_display': {
                HydrationStatus.DEHYDRATED_SEVERE: '严重脱水',
                HydrationStatus.DEHYDRATED: '脱水',
                HydrationStatus.SLIGHTLY_DEHYDRATED: '轻度脱水',
                HydrationStatus.WELL_HYDRATED: '补水良好',
                HydrationStatus.OPTIMAL: '最佳状态',
                HydrationStatus.OVERHYDRATED: '饮水过量'
            }.get(status, '未知'),
            'current_intake_ml': round(current_intake_ml),
            'target_intake_ml': round(target_intake_ml),
            'progress_ratio': round(ratio, 2),
            'remaining_ml': round(max(0, target_intake_ml - current_intake_ml)),
            'warning': warning,
            'urine_color_assessment': urine_assessment,
            'recommendations': self._get_recommendations(status, ratio)
        }
    
    def _get_recommendations(
        self,
        status: HydrationStatus,
        ratio: float
    ) -> List[str]:
        """获取补水建议"""
        recommendations = []
        
        if status == HydrationStatus.DEHYDRATED_SEVERE:
            recommendations = [
                "立即停止活动，补充水分",
                "小口慢饮，避免一次大量饮水",
                "可饮用含电解质的运动饮料",
                "如症状严重，请就医"
            ]
        elif status == HydrationStatus.DEHYDRATED:
            recommendations = [
                "增加饮水量，每小时250-500ml",
                "避免含咖啡因和酒精的饮料",
                "设置定时提醒饮水"
            ]
        elif status == HydrationStatus.SLIGHTLY_DEHYDRATED:
            recommendations = [
                "继续补水，保持饮水节奏",
                "可以喝一杯水（约250ml）",
                "注意观察身体信号"
            ]
        elif status == HydrationStatus.OPTIMAL:
            recommendations = [
                "继续保持当前饮水习惯",
                "维持规律饮水节奏"
            ]
        elif status == HydrationStatus.WELL_HYDRATED:
            recommendations = [
                "补水充足，注意不要过量",
                "可以维持当前饮水节奏"
            ]
        else:  # OVERHYDRATED
            recommendations = [
                "减少饮水量",
                "避免一次性大量饮水",
                "注意水中毒症状（头痛、恶心）"
            ]
        
        return recommendations
    
    def calculate_sweat_loss(
        self,
        weight_before_kg: float,
        weight_after_kg: float,
        fluid_intake_ml: float = 0,
        urine_output_ml: float = 0,
        duration_minutes: int = 60
    ) -> Dict[str, Any]:
        """
        计算出汗量和补水需求
        
        Args:
            weight_before_kg: 运动前体重（公斤）
            weight_after_kg: 运动后体重（公斤）
            fluid_intake_ml: 运动中饮水量（毫升）
            urine_output_ml: 运动中排尿量（毫升）
            duration_minutes: 运动时长（分钟）
        
        Returns:
            出汗量和补水建议
        """
        if weight_before_kg <= 0 or weight_after_kg <= 0:
            raise ValueError("体重必须大于0")
        
        # 计算体重变化
        weight_loss = weight_before_kg - weight_after_kg
        
        # 考虑饮水和排尿
        sweat_loss = (weight_loss * 1000) + fluid_intake_ml - urine_output_ml
        sweat_rate = sweat_loss / (duration_minutes / 60)  # 每小时出汗量
        
        # 脱水百分比
        dehydration_percent = (weight_loss / weight_before_kg) * 100
        
        # 补水建议
        if dehydration_percent < 2:
            rehydration_need = sweat_loss * 1.0
            urgency = "正常"
        elif dehydration_percent < 4:
            rehydration_need = sweat_loss * 1.25
            urgency = "轻度脱水"
        elif dehydration_percent < 6:
            rehydration_need = sweat_loss * 1.5
            urgency = "中度脱水"
        else:
            rehydration_need = sweat_loss * 2.0
            urgency = "严重脱水"
        
        return {
            'weight_before_kg': weight_before_kg,
            'weight_after_kg': weight_after_kg,
            'weight_loss_kg': round(weight_loss, 2),
            'weight_loss_percent': round(dehydration_percent, 1),
            'sweat_loss_ml': round(sweat_loss),
            'sweat_rate_ml_per_hour': round(sweat_rate),
            'fluid_intake_ml': fluid_intake_ml,
            'urine_output_ml': urine_output_ml,
            'duration_minutes': duration_minutes,
            'rehydration_needed_ml': round(rehydration_need),
            'dehydration_severity': urgency,
            'recommendations': [
                f"需要在2-4小时内补充{round(rehydration_need)}ml液体",
                "建议饮用含电解质的运动饮料" if dehydration_percent > 3 else "饮水即可",
                "避免饮用酒精和大量咖啡因" if dehydration_percent > 2 else None
            ]
        }
    
    def get_beverage_equivalent(
        self,
        water_ml: float
    ) -> Dict[str, float]:
        """
        获取等效饮料量
        
        Args:
            water_ml: 水量（毫升）
        
        Returns:
            各种饮料的等效量
        """
        # 饮料含水率（相对于纯水的补水效果）
        hydration_factors = {
            'water': 1.0,           # 纯水
            'tea': 0.98,            # 茶
            'coffee': 0.85,         # 咖啡（轻微利尿）
            'juice': 0.9,           # 果汁
            'milk': 0.87,           # 牛奶
            'soda': 0.8,            # 碳酸饮料
            'sports_drink': 0.95,   # 运动饮料
            'soup': 0.85,           # 汤
            'beer': 0.6,            # 啤酒
            'wine': 0.4,            # 葡萄酒
            'coconut_water': 0.95   # 椰子水
        }
        
        equivalents = {}
        for beverage, factor in hydration_factors.items():
            equivalent = water_ml / factor
            equivalents[beverage] = {
                'equivalent_ml': round(equivalent),
                'hydration_factor': factor,
                'note': self._get_beverage_note(beverage)
            }
        
        return equivalents
    
    def _get_beverage_note(self, beverage: str) -> str:
        """获取饮料备注"""
        notes = {
            'water': '最佳补水选择',
            'tea': '补水效果好，含抗氧化物',
            'coffee': '有轻微利尿作用，适量饮用',
            'juice': '含糖分和维生素，注意热量',
            'milk': '含蛋白质和钙，营养全面',
            'soda': '含糖量高，不推荐作为主要补水来源',
            'sports_drink': '运动时补水效果好，含电解质',
            'soup': '补水兼补充营养',
            'beer': '酒精有利尿作用，脱水效果',
            'wine': '酒精含量较高，补水效果差',
            'coconut_water': '天然电解质饮料，补水效果好'
        }
        return notes.get(beverage, '')
    
    def calculate_for_sport(
        self,
        sport_type: str,
        duration_minutes: int,
        intensity: str = "moderate",
        weight_kg: float = 70,
        temperature_c: float = 20
    ) -> Dict[str, Any]:
        """
        计算运动补水方案
        
        Args:
            sport_type: 运动类型
            duration_minutes: 运动时长（分钟）
            intensity: 运动强度（low, moderate, high, extreme）
            weight_kg: 体重（公斤）
            temperature_c: 环境温度（摄氏度）
        
        Returns:
            运动补水方案
        """
        # 不同运动的出汗率系数
        sport_sweat_factors = {
            'running': 1.2,
            'cycling': 1.0,
            'swimming': 0.6,
            'basketball': 1.1,
            'football': 1.15,
            'tennis': 1.0,
            'yoga': 0.5,
            'weightlifting': 0.7,
            'hiking': 0.9,
            'dancing': 0.85,
            'golf': 0.6,
            'boxing': 1.3,
            'crossfit': 1.2
        }
        
        # 强度系数
        intensity_multipliers = {
            'low': 0.6,
            'moderate': 1.0,
            'high': 1.3,
            'extreme': 1.6
        }
        
        # 温度系数
        if temperature_c < 15:
            temp_factor = 0.8
        elif temperature_c < 25:
            temp_factor = 1.0
        elif temperature_c < 30:
            temp_factor = 1.2
        else:
            temp_factor = 1.4
        
        # 计算出汗量（基础：每公斤体重每小时约10ml）
        base_sweat_rate = 10  # ml/kg/hour
        sport_factor = sport_sweat_factors.get(sport_type.lower(), 1.0)
        intensity_factor = intensity_multipliers.get(intensity.lower(), 1.0)
        
        hourly_sweat = weight_kg * base_sweat_rate * sport_factor * intensity_factor * temp_factor
        total_sweat = hourly_sweat * (duration_minutes / 60)
        
        # 补水建议
        before_exercise = round(400 + weight_kg * 5)  # 运动前
        during_per_15min = round(total_sweat / (duration_minutes / 15) * 0.7) if duration_minutes > 0 else 0
        after_exercise = round(total_sweat * 1.25)  # 运动后（补水量的1.25倍）
        
        return {
            'sport_type': sport_type,
            'duration_minutes': duration_minutes,
            'intensity': intensity,
            'weight_kg': weight_kg,
            'temperature_c': temperature_c,
            'estimated_sweat_loss_ml': round(total_sweat),
            'hourly_sweat_rate_ml': round(hourly_sweat),
            'hydration_plan': {
                'before_exercise_ml': before_exercise,
                'during_exercise': {
                    'per_15_minutes_ml': during_per_15min,
                    'total_ml': round(total_sweat * 0.7)
                },
                'after_exercise_ml': after_exercise
            },
            'total_recommended_ml': round(before_exercise + total_sweat * 0.7 + after_exercise),
            'tips': [
                "运动前2小时补水400-500ml",
                "运动中每15-20分钟补水150-250ml",
                "运动后按体重损失的1.25倍补水",
                "高强度或长时间运动建议使用运动饮料",
                "监测尿液颜色，淡黄色为最佳"
            ]
        }
    
    def clear_records(self, date: Optional[str] = None):
        """
        清除饮水记录
        
        Args:
            date: 指定日期（可选，默认清除全部）
        """
        if date:
            self.records = [r for r in self.records if r['date'] != date]
        else:
            self.records = []
    
    def export_records(self, format: str = "dict") -> Any:
        """
        导出饮水记录
        
        Args:
            format: 导出格式（dict, json）
        
        Returns:
            导出的数据
        """
        if format == "json":
            import json
            return json.dumps(self.records, ensure_ascii=False, indent=2)
        return self.records.copy()


# 便捷函数
def calculate_daily_water(
    weight_kg: float,
    activity_level: str = "moderate",
    climate: str = "mild",
    exercise_minutes: int = 0
) -> Dict[str, Any]:
    """
    快速计算每日饮水量的便捷函数
    
    Args:
        weight_kg: 体重（公斤）
        activity_level: 活动水平（sedentary, light, moderate, active, very_active）
        climate: 气候类型（cold, mild, warm, hot, very_hot, humid）
        exercise_minutes: 运动时间（分钟）
    
    Returns:
        每日饮水建议
    """
    activity_map = {
        'sedentary': ActivityLevel.SEDENTARY,
        'light': ActivityLevel.LIGHT,
        'moderate': ActivityLevel.MODERATE,
        'active': ActivityLevel.ACTIVE,
        'very_active': ActivityLevel.VERY_ACTIVE
    }
    
    climate_map = {
        'cold': ClimateType.COLD,
        'mild': ClimateType.MILD,
        'warm': ClimateType.WARM,
        'hot': ClimateType.HOT,
        'very_hot': ClimateType.VERY_HOT,
        'humid': ClimateType.HUMID
    }
    
    calculator = WaterIntakeCalculator()
    
    activity = activity_map.get(activity_level.lower(), ActivityLevel.MODERATE)
    climate_type = climate_map.get(climate.lower(), ClimateType.MILD)
    
    return calculator.calculate_daily_intake(
        weight_kg=weight_kg,
        activity_level=activity,
        climate=climate_type,
        exercise_minutes=exercise_minutes
    )


def get_quick_schedule(total_ml: float, wake_hour: int = 7) -> List[Dict[str, Any]]:
    """
    快速生成饮水时间表
    
    Args:
        total_ml: 总饮水量（毫升）
        wake_hour: 起床时间（小时）
    
    Returns:
        饮水时间表
    """
    calculator = WaterIntakeCalculator()
    return calculator.generate_drinking_schedule(
        daily_intake_ml=total_ml,
        wake_time=(wake_hour, 0)
    )


if __name__ == "__main__":
    # 演示用法
    calc = WaterIntakeCalculator()
    
    # 计算每日饮水量
    result = calc.calculate_daily_intake(
        weight_kg=70,
        activity_level=ActivityLevel.ACTIVE,
        climate=ClimateType.WARM,
        exercise_minutes=60
    )
    print(f"每日建议饮水量: {result['total_intake_ml']}ml ({result['total_intake_liters']}L)")
    
    # 生成饮水时间表
    schedule = calc.generate_drinking_schedule(result['total_intake_ml'])
    print("\n饮水时间表:")
    for s in schedule:
        print(f"  {s['time']} - {s['amount_ml']}ml ({s['note']})")
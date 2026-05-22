"""
人体工程学工具集 (Ergonomics Utils)

提供工作站设置建议、休息提醒、姿势评估、伸展运动建议等功能。
零外部依赖，使用 Python 标准库实现。

功能：
- 工作站设置计算（屏幕高度、椅子高度、键盘位置等）
- 工作休息间隔建议（番茄钟变体、20-20-20法则等）
- 姿势风险评估
- 眼睛疲劳预防
- 伸展运动建议
- 重复性劳损(RSI)风险评估
"""

from dataclasses import dataclass
from typing import List, Dict, Tuple, Optional
from enum import Enum
import math


class WorkIntensity(Enum):
    """工作强度等级"""
    LIGHT = "light"  # 轻度工作
    MODERATE = "moderate"  # 中度工作
    INTENSIVE = "intensive"  # 高强度工作
    EXTREME = "extreme"  # 极高强度工作


class PostureRisk(Enum):
    """姿势风险等级"""
    LOW = "low"  # 低风险
    MEDIUM = "medium"  # 中风险
    HIGH = "high"  # 高风险
    CRITICAL = "critical"  # 严重风险


class BodyPart(Enum):
    """身体部位"""
    NECK = "neck"  # 颈部
    SHOULDERS = "shoulders"  # 肩膀
    UPPER_BACK = "upper_back"  # 上背
    LOWER_BACK = "lower_back"  # 下背
    WRISTS = "wrists"  # 手腕
    HIPS = "hips"  # 髋部
    EYES = "eyes"  # 眼睛


@dataclass
class WorkstationSetup:
    """工作站设置建议"""
    screen_height: float  # 屏幕顶部高度 (cm)
    screen_distance: float  # 眼睛到屏幕距离 (cm)
    chair_height: float  # 椅子高度 (cm)
    desk_height: float  # 桌子高度 (cm)
    keyboard_height: float  # 键盘高度 (cm)
    monitor_tilt: float  # 显示器倾斜角度 (度)
    armrest_height: float  # 扶手高度 (cm)
    footrest_needed: bool  # 是否需要脚踏
    footrest_height: Optional[float]  # 脚踏高度 (cm)


@dataclass
class BreakSuggestion:
    """休息建议"""
    break_type: str  # 休息类型
    duration_minutes: int  # 持续时间（分钟）
    activity: str  # 活动内容
    reason: str  # 原因


@dataclass
class StretchExercise:
    """伸展运动"""
    name: str  # 名称
    body_parts: List[BodyPart]  # 目标部位
    duration_seconds: int  # 持续时间（秒）
    repetitions: int  # 重复次数
    instructions: List[str]  # 步骤说明
    benefits: List[str]  # 好处


@dataclass
class PostureAssessment:
    """姿势评估结果"""
    risk_level: PostureRisk
    score: int  # 0-100分
    issues: List[str]  # 问题列表
    recommendations: List[str]  # 建议列表
    affected_areas: List[BodyPart]  # 受影响部位


@dataclass
class RSIAssessment:
    """重复性劳损评估结果"""
    risk_score: int  # 0-100风险分数
    risk_level: str  # 风险等级
    factors: Dict[str, int]  # 各因素分数
    recommendations: List[str]  # 建议
    warning_signs: List[str]  # 警示信号


@dataclass
class EyeCarePlan:
    """眼睛保护计划"""
    break_interval_minutes: int  # 休息间隔
    focus_distance_meters: float  # 远眺距离
    eye_exercises: List[Dict]  # 眼保健操
    lighting_recommendations: List[str]  # 照明建议


def calculate_workstation_setup(
    user_height_cm: float,
    seated: bool = True,
    screen_size_inches: float = 24.0
) -> WorkstationSetup:
    """
    根据用户身高计算理想的工作站设置
    
    Args:
        user_height_cm: 用户身高（厘米）
        seated: 是否坐姿工作（False为站姿）
        screen_size_inches: 显示器尺寸（英寸）
    
    Returns:
        WorkstationSetup: 工作站设置建议
    """
    if user_height_cm <= 0:
        raise ValueError("身高必须为正数")
    
    if seated:
        # 坐姿工作设置
        # 椅子高度约为身高的28%
        chair_height = round(user_height_cm * 0.28, 1)
        
        # 桌子高度约为身高的43%
        desk_height = round(user_height_cm * 0.43, 1)
        
        # 键盘高度与桌子高度相同或略低
        keyboard_height = round(desk_height - 5, 1)
        
        # 屏幕顶部应与眼睛水平或略低
        # 眼睛高度约为身高的47%（坐姿）
        eye_height = user_height_cm * 0.47
        screen_height = round(eye_height - 3, 1)  # 屏幕顶部略低于眼睛
        
        # 屏幕距离为手臂长度的60-80%
        # 手臂长度约为身高的40%
        arm_length = user_height_cm * 0.40
        screen_distance = round(arm_length * 0.75, 1)
        
        # 扶手高度
        armrest_height = round(chair_height + 5, 1)
        
        # 判断是否需要脚踏
        # 如果大腿不能平放，需要脚踏
        lower_leg_length = user_height_cm * 0.25
        footrest_needed = chair_height > lower_leg_length + 5
        footrest_height = round(chair_height - lower_leg_length, 1) if footrest_needed else None
    else:
        # 站姿工作设置
        chair_height = 0.0
        desk_height = round(user_height_cm * 0.53, 1)  # 站姿桌子高度
        
        eye_height = user_height_cm * 0.94  # 站姿眼睛高度
        screen_height = round(eye_height - 5, 1)
        screen_distance = round(user_height_cm * 0.35, 1)
        keyboard_height = round(desk_height - 10, 1)
        armrest_height = 0.0
        footrest_needed = False
        footrest_height = None
    
    # 显示器倾斜角度（通常略微向后倾斜）
    monitor_tilt = 10.0
    
    return WorkstationSetup(
        screen_height=screen_height,
        screen_distance=screen_distance,
        chair_height=chair_height,
        desk_height=desk_height,
        keyboard_height=keyboard_height,
        monitor_tilt=monitor_tilt,
        armrest_height=armrest_height,
        footrest_needed=footrest_needed,
        footrest_height=footrest_height
    )


def calculate_break_intervals(
    work_hours: float,
    intensity: WorkIntensity = WorkIntensity.MODERATE,
    use_20_20_20_rule: bool = True
) -> List[BreakSuggestion]:
    """
    计算工作休息间隔建议
    
    Args:
        work_hours: 计划工作时间（小时）
        intensity: 工作强度
        use_20_20_20_rule: 是否使用20-20-20法则（眼睛保护）
    
    Returns:
        List[BreakSuggestion]: 休息建议列表
    """
    breaks = []
    total_minutes = work_hours * 60
    
    # 根据工作强度确定休息间隔
    intensity_intervals = {
        WorkIntensity.LIGHT: 60,  # 每60分钟休息
        WorkIntensity.MODERATE: 45,  # 每45分钟休息
        WorkIntensity.INTENSIVE: 30,  # 每30分钟休息
        WorkIntensity.EXTREME: 20,  # 每20分钟休息
    }
    
    interval = intensity_intervals[intensity]
    short_break_duration = 5 if intensity in [WorkIntensity.LIGHT, WorkIntensity.MODERATE] else 10
    
    # 计算休息次数
    num_breaks = int(total_minutes / interval)
    
    for i in range(num_breaks):
        break_time = (i + 1) * interval
        
        if (i + 1) % 3 == 0:  # 每3次短休息后建议一次长休息
            breaks.append(BreakSuggestion(
                break_type="long_break",
                duration_minutes=15,
                activity="离开工作区域，进行散步或其他活动",
                reason=f"已工作 {break_time} 分钟，需要恢复精力"
            ))
        else:
            breaks.append(BreakSuggestion(
                break_type="short_break",
                duration_minutes=short_break_duration,
                activity="站起来伸展、喝水、远眺",
                reason=f"已工作 {break_time} 分钟，需要放松"
            ))
    
    # 添加20-20-20法则眼睛休息
    if use_20_20_20_rule:
        eye_breaks = int(total_minutes / 20)
        for i in range(eye_breaks):
            breaks.append(BreakSuggestion(
                break_type="eye_break",
                duration_minutes=0,  # 实际上是20秒
                activity="注视20英尺（约6米）外的物体20秒",
                reason=f"已工作 {(i + 1) * 20} 分钟，保护眼睛"
            ))
    
    return breaks


def get_stretch_exercises(
    body_parts: Optional[List[BodyPart]] = None,
    work_duration_minutes: int = 60
) -> List[StretchExercise]:
    """
    获取伸展运动建议
    
    Args:
        body_parts: 目标身体部位（None表示全部）
        work_duration_minutes: 已工作时间（分钟）
    
    Returns:
        List[StretchExercise]: 伸展运动列表
    """
    all_exercises = [
        # 颈部伸展
        StretchExercise(
            name="颈部侧倾",
            body_parts=[BodyPart.NECK],
            duration_seconds=15,
            repetitions=3,
            instructions=[
                "坐直或站直，肩膀放松",
                "慢慢将右耳倾向右肩，保持15秒",
                "换左侧重复",
                "动作要缓慢，避免弹动"
            ],
            benefits=["缓解颈部紧张", "改善颈部灵活性", "预防颈椎病"]
        ),
        StretchExercise(
            name="颈部旋转",
            body_parts=[BodyPart.NECK],
            duration_seconds=10,
            repetitions=5,
            instructions=[
                "坐直，肩膀放松",
                "缓慢将头转向右侧，保持10秒",
                "转向左侧，保持10秒",
                "重复5次"
            ],
            benefits=["缓解颈部僵硬", "改善血液循环"]
        ),
        # 肩膀伸展
        StretchExercise(
            name="肩膀耸肩",
            body_parts=[BodyPart.SHOULDERS],
            duration_seconds=5,
            repetitions=10,
            instructions=[
                "坐直或站直",
                "将肩膀向上耸起，保持5秒",
                "放松肩膀落下",
                "重复10次"
            ],
            benefits=["缓解肩部紧张", "放松斜方肌"]
        ),
        StretchExercise(
            name="肩膀后转",
            body_parts=[BodyPart.SHOULDERS, BodyPart.UPPER_BACK],
            duration_seconds=10,
            repetitions=8,
            instructions=[
                "站直或坐直",
                "双肩向后画圆圈，做8次",
                "然后向前画圆圈，做8次",
                "动作要缓慢流畅"
            ],
            benefits=["改善肩部活动", "缓解上背紧张"]
        ),
        # 手腕伸展
        StretchExercise(
            name="手腕伸展",
            body_parts=[BodyPart.WRISTS],
            duration_seconds=15,
            repetitions=3,
            instructions=[
                "伸出手臂，手掌朝下",
                "用另一只手轻轻向下压手背，保持15秒",
                "换手重复",
                "然后手掌朝上，轻压手掌"
            ],
            benefits=["预防腕管综合症", "缓解手腕疲劳", "适合长时间使用键盘鼠标"]
        ),
        StretchExercise(
            name="手腕旋转",
            body_parts=[BodyPart.WRISTS],
            duration_seconds=10,
            repetitions=5,
            instructions=[
                "握拳，手腕放松",
                "顺时针旋转5圈",
                "逆时针旋转5圈",
                "动作要缓慢"
            ],
            benefits=["增加手腕灵活性", "缓解重复性劳损"]
        ),
        # 上背伸展
        StretchExercise(
            name="胸部展开",
            body_parts=[BodyPart.UPPER_BACK, BodyPart.SHOULDERS],
            duration_seconds=15,
            repetitions=3,
            instructions=[
                "双手在背后交握",
                "挺胸，将肩膀向后拉",
                "保持15秒",
                "可以配合深呼吸"
            ],
            benefits=["纠正前倾姿势", "打开胸腔", "改善呼吸"]
        ),
        # 下背伸展
        StretchExercise(
            name="坐姿扭转",
            body_parts=[BodyPart.LOWER_BACK],
            duration_seconds=15,
            repetitions=3,
            instructions=[
                "坐在椅子上，双脚平放",
                "右手扶住椅背，身体向右转",
                "保持15秒，换边",
                "可以配合呼吸加深扭转"
            ],
            benefits=["缓解腰背紧张", "增加脊柱灵活性"]
        ),
        StretchExercise(
            name="猫牛式",
            body_parts=[BodyPart.LOWER_BACK, BodyPart.UPPER_BACK],
            duration_seconds=5,
            repetitions=10,
            instructions=[
                "坐在椅子边缘，双手放在膝盖上",
                "吸气，挺胸抬头（牛式）",
                "呼气，拱背低头（猫式）",
                "配合呼吸，重复10次"
            ],
            benefits=["放松整个脊柱", "改善姿态", "缓解背痛"]
        ),
        # 髋部伸展
        StretchExercise(
            name="坐姿髋部伸展",
            body_parts=[BodyPart.HIPS],
            duration_seconds=30,
            repetitions=2,
            instructions=[
                "坐在椅子上，将右脚踝放在左膝上",
                "保持背部挺直，身体略微前倾",
                "感受右髋部的拉伸，保持30秒",
                "换腿重复"
            ],
            benefits=["缓解久坐髋部紧张", "改善髋关节灵活性"]
        ),
        # 眼部运动
        StretchExercise(
            name="眼部放松",
            body_parts=[BodyPart.EYES],
            duration_seconds=20,
            repetitions=1,
            instructions=[
                "闭眼，用手掌轻轻捂住眼睛",
                "深呼吸10次",
                "睁眼，眨眼10次",
                "看向远处（6米外）20秒"
            ],
            benefits=["缓解眼疲劳", "预防近视加深", "放松眼部肌肉"]
        ),
        StretchExercise(
            name="眼球运动",
            body_parts=[BodyPart.EYES],
            duration_seconds=30,
            repetitions=1,
            instructions=[
                "保持头部不动，眼球向上看5秒",
                "向下看5秒",
                "向左看5秒",
                "向右看5秒",
                "画8字形10秒"
            ],
            benefits=["增强眼部肌肉", "改善聚焦能力", "缓解眼疲劳"]
        ),
    ]
    
    # 根据身体部位筛选
    if body_parts:
        filtered = []
        for exercise in all_exercises:
            if any(bp in exercise.body_parts for bp in body_parts):
                filtered.append(exercise)
        return filtered
    
    # 根据工作时间选择
    if work_duration_minutes >= 120:
        # 长时间工作，返回更多运动
        return all_exercises
    elif work_duration_minutes >= 60:
        # 中等时间，返回重点运动
        return all_exercises[:8]
    else:
        # 短时间，返回基础运动
        return all_exercises[:5]


def assess_posture(
    screen_distance_cm: float,
    screen_height_relative: str,  # "above", "level", "below"
    back_support: bool,
    feet_flat: bool,
    elbows_angle: float,
    breaks_taken: int,
    work_duration_minutes: int
) -> PostureAssessment:
    """
    评估当前姿势的风险等级
    
    Args:
        screen_distance_cm: 眼睛到屏幕距离（厘米）
        screen_height_relative: 屏幕相对眼睛高度
        back_support: 是否有背部支撑
        feet_flat: 双脚是否平放
        elbows_angle: 手肘角度（度）
        breaks_taken: 已休息次数
        work_duration_minutes: 已工作时间（分钟）
    
    Returns:
        PostureAssessment: 姿势评估结果
    """
    score = 100
    issues = []
    affected_areas = []
    
    # 屏幕距离评估（理想：50-70cm）
    if screen_distance_cm < 30:
        score -= 20
        issues.append("屏幕距离过近，容易导致眼睛疲劳")
        affected_areas.append(BodyPart.EYES)
    elif screen_distance_cm < 50:
        score -= 10
        issues.append("屏幕距离略近，建议调整到50-70cm")
        affected_areas.append(BodyPart.EYES)
    elif screen_distance_cm > 80:
        score -= 10
        issues.append("屏幕距离过远，可能导致前倾姿势")
        affected_areas.append(BodyPart.NECK)
    
    # 屏幕高度评估
    if screen_height_relative == "above":
        score -= 15
        issues.append("屏幕位置过高，需要仰视，增加颈部压力")
        affected_areas.append(BodyPart.NECK)
        affected_areas.append(BodyPart.SHOULDERS)
    elif screen_height_relative == "below":
        score -= 10
        issues.append("屏幕位置过低，需要低头，增加颈椎负担")
        affected_areas.append(BodyPart.NECK)
        affected_areas.append(BodyPart.UPPER_BACK)
    
    # 背部支撑
    if not back_support:
        score -= 15
        issues.append("缺乏背部支撑，增加下背压力")
        affected_areas.append(BodyPart.LOWER_BACK)
    
    # 脚部位置
    if not feet_flat:
        score -= 10
        issues.append("双脚未平放，影响血液循环和姿势稳定")
        affected_areas.append(BodyPart.HIPS)
        affected_areas.append(BodyPart.LOWER_BACK)
    
    # 手肘角度评估（理想：90-110度）
    if elbows_angle < 80:
        score -= 10
        issues.append("手肘角度过小，手腕可能受压")
        affected_areas.append(BodyPart.WRISTS)
    elif elbows_angle > 120:
        score -= 10
        issues.append("手肘角度过大，肩膀可能紧张")
        affected_areas.append(BodyPart.SHOULDERS)
    
    # 休息频率评估
    expected_breaks = work_duration_minutes // 45
    if breaks_taken < expected_breaks // 2:
        score -= 20
        issues.append(f"休息次数不足，建议每45分钟休息一次")
        affected_areas.append(BodyPart.EYES)
        affected_areas.append(BodyPart.LOWER_BACK)
    elif breaks_taken < expected_breaks:
        score -= 10
        issues.append("休息频率略低")
    
    # 确保分数在0-100范围
    score = max(0, min(100, score))
    
    # 确定风险等级
    if score >= 80:
        risk_level = PostureRisk.LOW
    elif score >= 60:
        risk_level = PostureRisk.MEDIUM
    elif score >= 40:
        risk_level = PostureRisk.HIGH
    else:
        risk_level = PostureRisk.CRITICAL
    
    # 生成建议
    recommendations = []
    if screen_distance_cm < 50 or screen_distance_cm > 70:
        recommendations.append("调整屏幕距离到50-70cm")
    if screen_height_relative != "level":
        recommendations.append("调整屏幕高度使顶部与眼睛平齐或略低")
    if not back_support:
        recommendations.append("使用有良好背部支撑的椅子")
    if not feet_flat:
        recommendations.append("使用脚踏板使双脚平放")
    if elbows_angle < 90 or elbows_angle > 110:
        recommendations.append("调整椅子高度使手肘保持90-110度")
    if breaks_taken < expected_breaks:
        recommendations.append(f"增加休息频率，建议每45分钟休息5分钟")
    
    # 去重受影响部位
    affected_areas = list(set(affected_areas))
    
    return PostureAssessment(
        risk_level=risk_level,
        score=score,
        issues=issues,
        recommendations=recommendations,
        affected_areas=affected_areas
    )


def assess_rsi_risk(
    typing_hours_per_day: float,
    mouse_hours_per_day: float,
    breaks_per_day: int,
    keyboard_position: str,  # "ideal", "high", "low"
    mouse_position: str,  # "ideal", "far", "close"
    wrist_support: bool,
    previous_injury: bool
) -> RSIAssessment:
    """
    评估重复性劳损(RSI)风险
    
    Args:
        typing_hours_per_day: 每天打字时间（小时）
        mouse_hours_per_day: 每天使用鼠标时间（小时）
        breaks_per_day: 每天休息次数
        keyboard_position: 键盘位置
        mouse_position: 鼠标位置
        wrist_support: 是否使用手腕托
        previous_injury: 是否有过往伤病
    
    Returns:
        RSIAssessment: RSI评估结果
    """
    factors = {}
    
    # 打字时间评分（0-25分）
    if typing_hours_per_day <= 2:
        factors["typing_time"] = 0
    elif typing_hours_per_day <= 4:
        factors["typing_time"] = 10
    elif typing_hours_per_day <= 6:
        factors["typing_time"] = 20
    else:
        factors["typing_time"] = 25
    
    # 鼠标时间评分（0-20分）
    if mouse_hours_per_day <= 1:
        factors["mouse_time"] = 0
    elif mouse_hours_per_day <= 3:
        factors["mouse_time"] = 8
    elif mouse_hours_per_day <= 5:
        factors["mouse_time"] = 15
    else:
        factors["mouse_time"] = 20
    
    # 休息频率评分（0-20分）
    total_work_hours = typing_hours_per_day + mouse_hours_per_day
    ideal_breaks = int(total_work_hours * 60 / 45)  # 每45分钟一次
    break_ratio = breaks_per_day / max(ideal_breaks, 1) if ideal_breaks > 0 else 1
    
    if break_ratio >= 1:
        factors["break_frequency"] = 0
    elif break_ratio >= 0.5:
        factors["break_frequency"] = 10
    else:
        factors["break_frequency"] = 20
    
    # 键盘位置评分（0-10分）
    if keyboard_position == "ideal":
        factors["keyboard_position"] = 0
    elif keyboard_position == "high":
        factors["keyboard_position"] = 8
    else:
        factors["keyboard_position"] = 5
    
    # 鼠标位置评分（0-10分）
    if mouse_position == "ideal":
        factors["mouse_position"] = 0
    elif mouse_position == "far":
        factors["mouse_position"] = 8
    else:
        factors["mouse_position"] = 5
    
    # 手腕支撑评分（0-10分）
    factors["wrist_support"] = 0 if wrist_support else 10
    
    # 过往伤病评分（0-25分）
    factors["previous_injury"] = 25 if previous_injury else 0
    
    # 计算总分
    total_score = sum(factors.values())
    total_score = min(100, total_score)  # 上限100
    
    # 确定风险等级
    if total_score <= 20:
        risk_level = "低风险"
    elif total_score <= 40:
        risk_level = "中等风险"
    elif total_score <= 60:
        risk_level = "高风险"
    else:
        risk_level = "极高风险"
    
    # 生成建议
    recommendations = []
    if factors["typing_time"] > 10:
        recommendations.append("减少连续打字时间，使用语音输入或休息")
    if factors["mouse_time"] > 8:
        recommendations.append("考虑使用键盘快捷键替代鼠标操作")
        recommendations.append("尝试垂直鼠标或触控板")
    if factors["break_frequency"] > 5:
        recommendations.append("增加休息频率，每45分钟休息5分钟")
        recommendations.append("使用番茄钟或定时器提醒")
    if keyboard_position != "ideal":
        recommendations.append("调整键盘高度，使手肘保持90度")
    if mouse_position != "ideal":
        recommendations.append("将鼠标放在键盘旁边，手臂靠近身体")
    if not wrist_support:
        recommendations.append("考虑使用手腕托，但不要在打字时依赖它")
    if previous_injury:
        recommendations.append("咨询医生或物理治疗师")
        recommendations.append("考虑使用人体工程学键盘和鼠标")
    
    # 警示信号
    warning_signs = [
        "手指、手腕或手臂麻木或刺痛",
        "手部无力或笨拙",
        "疼痛在夜间加重",
        "无法完成日常精细动作",
        "前臂或手掌有烧灼感"
    ]
    
    return RSIAssessment(
        risk_score=total_score,
        risk_level=risk_level,
        factors=factors,
        recommendations=recommendations,
        warning_signs=warning_signs
    )


def create_eye_care_plan(
    screen_hours_per_day: float,
    has_glasses: bool = False,
    screen_brightness: str = "medium",  # "low", "medium", "high"
    ambient_light: str = "medium"  # "dim", "medium", "bright"
) -> EyeCarePlan:
    """
    创建眼睛保护计划
    
    Args:
        screen_hours_per_day: 每天屏幕使用时间（小时）
        has_glasses: 是否佩戴眼镜
        screen_brightness: 屏幕亮度
        ambient_light: 环境光线
    
    Returns:
        EyeCarePlan: 眼睛保护计划
    """
    # 根据使用时间确定休息间隔
    if screen_hours_per_day <= 4:
        break_interval = 30  # 每30分钟
    elif screen_hours_per_day <= 8:
        break_interval = 20  # 每20分钟（20-20-20法则）
    else:
        break_interval = 15  # 每15分钟
    
    # 远眺距离（建议6米以上）
    focus_distance = 6.0  # 米
    
    # 眼保健操
    eye_exercises = [
        {
            "name": "远近交替聚焦",
            "duration_seconds": 60,
            "steps": [
                "选择一个近处物体（30cm）和一个远处物体（6米外）",
                "看近处物体15秒",
                "看远处物体15秒",
                "重复2次"
            ]
        },
        {
            "name": "眼球画圈",
            "duration_seconds": 30,
            "steps": [
                "保持头部不动",
                "眼球顺时针画圈10圈",
                "逆时针画圈10圈",
                "动作缓慢流畅"
            ]
        },
        {
            "name": "手掌捂眼",
            "duration_seconds": 60,
            "steps": [
                "双手搓热",
                "闭眼，用手掌轻轻捂住眼睛",
                "深呼吸，放松",
                "持续60秒"
            ]
        },
        {
            "name": "眨眼练习",
            "duration_seconds": 20,
            "steps": [
                "正常眨眼10次",
                "快速眨眼10次",
                "闭眼保持5秒，再睁开"
            ]
        }
    ]
    
    # 照明建议
    lighting_recommendations = []
    
    if screen_brightness == "high":
        lighting_recommendations.append("降低屏幕亮度到舒适水平")
    elif screen_brightness == "low":
        lighting_recommendations.append("适当提高屏幕亮度，但不要过高")
    
    if ambient_light == "dim":
        lighting_recommendations.append("增加环境光线，避免屏幕成为唯一光源")
        lighting_recommendations.append("考虑使用台灯补充照明")
    elif ambient_light == "bright":
        lighting_recommendations.append("避免窗户或灯光直接照射屏幕")
        lighting_recommendations.append("使用窗帘或遮光罩")
    
    lighting_recommendations.extend([
        "屏幕亮度应与环境光线相近",
        "屏幕应无眩光和反射",
        "考虑使用护眼模式或蓝光滤镜",
        "显示器顶部应与眼睛平齐或略低"
    ])
    
    if has_glasses:
        lighting_recommendations.append("确保眼镜镜片清洁")
        lighting_recommendations.append("考虑防蓝光镜片")
    
    return EyeCarePlan(
        break_interval_minutes=break_interval,
        focus_distance_meters=focus_distance,
        eye_exercises=eye_exercises,
        lighting_recommendations=lighting_recommendations
    )


def calculate_optimal_monitor_setup(
    monitor_size_inches: float,
    resolution_width: int,
    resolution_height: int,
    user_height_cm: float
) -> Dict:
    """
    计算最佳显示器设置
    
    Args:
        monitor_size_inches: 显示器尺寸（英寸）
        resolution_width: 水平分辨率
        resolution_height: 垂直分辨率
        user_height_cm: 用户身高（厘米）
    
    Returns:
        Dict: 显示器设置建议
    """
    # 计算显示器物理尺寸（假设16:9比例）
    aspect_ratio = 16 / 9
    diagonal_cm = monitor_size_inches * 2.54
    
    width_cm = diagonal_cm * math.sqrt(1 / (1 + (1 / aspect_ratio) ** 2))
    height_cm = width_cm / aspect_ratio
    
    # 计算像素密度
    ppi = math.sqrt(resolution_width ** 2 + resolution_height ** 2) / monitor_size_inches
    
    # 计算推荐观看距离（基于分辨率和尺寸）
    # 对于1080p，推荐距离约为屏幕高度的3倍
    # 对于更高分辨率，可以更近
    base_distance = height_cm * 3
    
    # 根据分辨率调整
    if resolution_height >= 2160:  # 4K
        distance_multiplier = 0.8
    elif resolution_height >= 1440:  # 2K
        distance_multiplier = 0.9
    else:  # 1080p
        distance_multiplier = 1.0
    
    recommended_distance = round(base_distance * distance_multiplier, 1)
    
    # 根据用户身高调整屏幕高度
    eye_height_seated = user_height_cm * 0.47
    optimal_screen_top_height = eye_height_seated - 3  # 略低于眼睛
    
    # 计算缩放建议
    if ppi >= 150:  # 高DPI显示器
        scaling_recommendation = "150% 或 200%"
    elif ppi >= 100:
        scaling_recommendation = "100% 或 125%"
    else:
        scaling_recommendation = "100%"
    
    # 文字大小建议
    if resolution_height >= 2160:
        font_size_recommendation = "14-16pt"
    else:
        font_size_recommendation = "12-14pt"
    
    return {
        "monitor_dimensions": {
            "width_cm": round(width_cm, 1),
            "height_cm": round(height_cm, 1),
            "diagonal_cm": round(diagonal_cm, 1)
        },
        "pixel_density_ppi": round(ppi, 1),
        "recommended_viewing_distance_cm": recommended_distance,
        "optimal_screen_top_height_cm": round(optimal_screen_top_height, 1),
        "scaling_recommendation": scaling_recommendation,
        "font_size_recommendation": font_size_recommendation,
        "tips": [
            "显示器应略微向后倾斜10-20度",
            "屏幕中心应略低于视线水平",
            "保持屏幕清洁",
            "避免强光直射屏幕"
        ]
    }


def get_work_period_analysis(
    work_periods: List[Dict],  # [{"start": "09:00", "end": "12:00"}, ...]
    break_periods: List[Dict]  # [{"start": "12:00", "end": "13:00"}, ...]
) -> Dict:
    """
    分析工作模式并提供建议
    
    Args:
        work_periods: 工作时间段列表
        break_periods: 休息时间段列表
    
    Returns:
        Dict: 工作分析结果
    """
    def parse_time(time_str: str) -> int:
        """将时间字符串转换为分钟数"""
        parts = time_str.split(":")
        return int(parts[0]) * 60 + int(parts[1])
    
    total_work_minutes = 0
    total_break_minutes = 0
    
    for period in work_periods:
        start = parse_time(period["start"])
        end = parse_time(period["end"])
        total_work_minutes += (end - start) if end > start else (24 * 60 - start + end)
    
    for period in break_periods:
        start = parse_time(period["start"])
        end = parse_time(period["end"])
        total_break_minutes += (end - start) if end > start else (24 * 60 - start + end)
    
    # 计算最长连续工作时间
    max_continuous = 0
    for period in work_periods:
        start = parse_time(period["start"])
        end = parse_time(period["end"])
        duration = (end - start) if end > start else (24 * 60 - start + end)
        max_continuous = max(max_continuous, duration)
    
    # 分析
    work_hours = total_work_minutes / 60
    break_ratio = total_break_minutes / total_work_minutes if total_work_minutes > 0 else 0
    
    # 评估
    issues = []
    recommendations = []
    
    if work_hours > 10:
        issues.append("工作时间过长，超出健康范围")
        recommendations.append("将每日工作时间控制在8小时以内")
    elif work_hours > 8:
        issues.append("工作时间略长")
        recommendations.append("考虑减少工作时间或增加休息")
    
    if max_continuous > 120:
        issues.append(f"最长连续工作时间为{max_continuous}分钟，过长")
        recommendations.append("每45-60分钟休息5-10分钟")
    elif max_continuous > 90:
        issues.append(f"最长连续工作时间为{max_continuous}分钟")
        recommendations.append("建议在长时间工作中间加入休息")
    
    if break_ratio < 0.1:
        issues.append("休息时间比例过低")
        recommendations.append("建议休息时间占工作时间至少10-15%")
    
    # 工作强度评估
    if work_hours <= 4:
        intensity = WorkIntensity.LIGHT
    elif work_hours <= 6:
        intensity = WorkIntensity.MODERATE
    elif work_hours <= 9:
        intensity = WorkIntensity.INTENSIVE
    else:
        intensity = WorkIntensity.EXTREME
    
    return {
        "total_work_hours": round(work_hours, 1),
        "total_break_hours": round(total_break_minutes / 60, 1),
        "break_ratio": round(break_ratio, 2),
        "longest_continuous_work_minutes": max_continuous,
        "work_intensity": intensity.value,
        "issues": issues,
        "recommendations": recommendations,
        "daily_break_suggestions": calculate_break_intervals(work_hours, intensity)
    }


def get_sitting_vs_standing_recommendation(
    sitting_hours: float,
    standing_hours: float,
    total_work_hours: float
) -> Dict:
    """
    分析坐立比例并提供建议
    
    Args:
        sitting_hours: 坐姿工作时间
        standing_hours: 站姿工作时间
        total_work_hours: 总工作时间
    
    Returns:
        Dict: 坐立建议
    """
    total = sitting_hours + standing_hours
    sitting_ratio = sitting_hours / total if total > 0 else 0
    standing_ratio = standing_hours / total if total > 0 else 0
    
    issues = []
    recommendations = []
    
    # 理想比例：坐60-70%，站30-40%
    if sitting_ratio > 0.8:
        issues.append("坐姿时间占比过高（超过80%）")
        recommendations.append("增加站立工作时间，使用升降桌或定时站立")
        recommendations.append("建议比例：坐60-70%，站30-40%")
    elif sitting_ratio > 0.7:
        issues.append("坐姿时间略多")
        recommendations.append("适当增加站立时间")
    
    if standing_ratio > 0.5:
        issues.append("站立时间占比过高，可能导致腿部疲劳")
        recommendations.append("增加坐姿时间，穿舒适的鞋子")
        recommendations.append("长时间站立时使用防疲劳垫")
    
    # 计算建议的时间分配
    ideal_sitting = total_work_hours * 0.65
    ideal_standing = total_work_hours * 0.35
    
    # 建议的切换频率
    if total_work_hours > 0:
        switch_frequency = min(30, max(15, int(total_work_hours * 5)))
    else:
        switch_frequency = 30
    
    return {
        "current_sitting_ratio": round(sitting_ratio, 2),
        "current_standing_ratio": round(standing_ratio, 2),
        "ideal_sitting_hours": round(ideal_sitting, 1),
        "ideal_standing_hours": round(ideal_standing, 1),
        "recommended_switch_interval_minutes": switch_frequency,
        "issues": issues,
        "recommendations": recommendations,
        "tips": [
            "每30-45分钟切换坐立姿势",
            "站立时保持重心均匀分布",
            "坐姿时保持良好姿势",
            "使用提醒工具定时切换"
        ]
    }


# 便捷函数
def quick_setup(height_cm: float) -> Dict:
    """
    快速获取工作站设置建议
    
    Args:
        height_cm: 用户身高（厘米）
    
    Returns:
        Dict: 快速设置建议
    """
    setup = calculate_workstation_setup(height_cm)
    stretches = get_stretch_exercises()[:5]
    
    return {
        "workstation": {
            "screen_height": f"{setup.screen_height} cm (屏幕顶部高度)",
            "screen_distance": f"{setup.screen_distance} cm (眼睛到屏幕)",
            "chair_height": f"{setup.chair_height} cm",
            "desk_height": f"{setup.desk_height} cm",
            "keyboard_height": f"{setup.keyboard_height} cm"
        },
        "footrest": "需要" if setup.footrest_needed else "不需要",
        "recommended_stretches": [s.name for s in stretches],
        "break_reminder": "每45分钟休息5分钟，每20分钟看远处20秒"
    }


if __name__ == "__main__":
    # 示例使用
    print("=== 工作站设置建议 ===")
    setup = calculate_workstation_setup(175)  # 175cm身高
    print(f"屏幕高度: {setup.screen_height} cm")
    print(f"屏幕距离: {setup.screen_distance} cm")
    print(f"椅子高度: {setup.chair_height} cm")
    print(f"桌子高度: {setup.desk_height} cm")
    
    print("\n=== 休息建议（4小时工作）===")
    breaks = calculate_break_intervals(4)
    for b in breaks[:5]:
        print(f"- {b.break_type}: {b.duration_minutes}分钟, {b.activity}")
    
    print("\n=== 姿势评估 ===")
    assessment = assess_posture(
        screen_distance_cm=60,
        screen_height_relative="level",
        back_support=True,
        feet_flat=True,
        elbows_angle=95,
        breaks_taken=2,
        work_duration_minutes=120
    )
    print(f"风险等级: {assessment.risk_level.value}")
    print(f"得分: {assessment.score}/100")
    
    print("\n=== RSI风险评估 ===")
    rsi = assess_rsi_risk(
        typing_hours_per_day=6,
        mouse_hours_per_day=3,
        breaks_per_day=4,
        keyboard_position="ideal",
        mouse_position="far",
        wrist_support=True,
        previous_injury=False
    )
    print(f"风险分数: {rsi.risk_score}")
    print(f"风险等级: {rsi.risk_level}")
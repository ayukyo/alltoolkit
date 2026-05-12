"""
Breathing Exercise Utils - 呼吸练习工具

支持多种呼吸技巧、节奏计算、练习指导等功能。
零外部依赖，仅使用 Python 标准库。

包含的呼吸技巧:
- 4-7-8 放松呼吸 (Relaxation Breath)
- 箱式呼吸 (Box Breathing)
- 乌加依呼吸 (Ujjayi Breath)
- 腹式呼吸 (Diaphragmatic Breathing)
- 交替鼻孔呼吸 (Alternate Nostril)
- 激活呼吸 (Energizing Breath)
- 冥想呼吸 (Meditation Breath)
- 睡眠呼吸 (Sleep Breath)
- 生理性叹息 (Physiological Sigh)
- 战术呼吸 (Tactical Breathing)
"""

from dataclasses import dataclass
from typing import List, Optional, Tuple, Dict, Callable
from enum import Enum
import time
import math


class BreathPhase(Enum):
    """呼吸阶段"""
    INHALE = "inhale"           # 吸气
    HOLD_IN = "hold_in"         # 屏气（吸气后）
    EXHALE = "exhale"           # 呼气
    HOLD_OUT = "hold_out"       # 屏气（呼气后）
    INHALE_LEFT = "inhale_left" # 左鼻孔吸气
    INHALE_RIGHT = "inhale_right" # 右鼻孔吸气


class BreathingTechnique(Enum):
    """呼吸技巧类型"""
    RELAXATION_478 = "relaxation_478"           # 4-7-8 放松呼吸
    BOX_BREATHING = "box_breathing"             # 箱式呼吸 4-4-4-4
    UJJAYI = "ujjayi"                           # 乌加依呼吸
    DIAPHRAGMATIC = "diaphragmatic"             # 腹式呼吸
    ALTERNATE_NOSTRIL = "alternate_nostril"     # 交替鼻孔呼吸
    ENERGIZING = "energizing"                   # 激活呼吸
    MEDITATION = "meditation"                   # 冥想呼吸
    SLEEP_BREATH = "sleep_breath"               # 睡眠呼吸 4-6
    PHYSIOLOGICAL_SIGH = "physiological_sigh"   # 生理性叹息
    TACTICAL = "tactical"                       # 战术呼吸 4-4-4-4
    COHERENT = "coherent"                       # 连贯呼吸 5-5
    RESONANT = "resonant"                       # 共振呼吸
    WIM_HOF = "wim_hof"                         # Wim Hof 呼吸法
    CALMING = "calming"                         # 镇静呼吸
    FOCUS = "focus"                             # 专注呼吸


@dataclass
class BreathingStep:
    """单个呼吸步骤"""
    phase: BreathPhase
    duration: float  # 秒
    description: str
    instruction: str  # 简短指令


@dataclass
class BreathingPattern:
    """呼吸模式"""
    name: str
    technique: BreathingTechnique
    steps: List[BreathingStep]
    cycles: int  # 建议循环次数
    total_duration: float  # 单循环总时长（秒）
    benefits: List[str]
    contraindications: List[str]
    difficulty: str  # easy, medium, hard
    description: str


@dataclass
class ExerciseSession:
    """练习会话"""
    technique: BreathingTechnique
    pattern: BreathingPattern
    cycles_completed: int
    total_time: float
    start_time: float
    end_time: Optional[float] = None


@dataclass
class SessionStats:
    """练习统计"""
    total_sessions: int
    total_time: float
    total_cycles: int
    favorite_technique: Optional[BreathingTechnique]
    average_session_time: float
    techniques_used: Dict[str, int]


# ==================== 预定义呼吸模式 ====================

def create_478_relaxation() -> BreathingPattern:
    """4-7-8 放松呼吸：安德鲁·韦尔博士开发的放松技术"""
    steps = [
        BreathingStep(BreathPhase.INHALE, 4.0, "通过鼻子缓慢吸气", "吸气"),
        BreathingStep(BreathPhase.HOLD_IN, 7.0, "屏住呼吸，保持放松", "屏气"),
        BreathingStep(BreathPhase.EXHALE, 8.0, "通过嘴巴缓慢呼气，发出轻微声音", "呼气"),
    ]
    return BreathingPattern(
        name="4-7-8 放松呼吸",
        technique=BreathingTechnique.RELAXATION_478,
        steps=steps,
        cycles=4,
        total_duration=19.0,
        benefits=[
            "快速缓解焦虑和压力",
            "帮助入睡",
            "降低心率和血压",
            "平静神经系统"
        ],
        contraindications=[
            "呼吸系统疾病患者谨慎",
            "初学者可能感到头晕"
        ],
        difficulty="medium",
        description="安德鲁·韦尔博士开发的放松技术，被称为'天然镇静剂'"
    )


def create_box_breathing() -> BreathingPattern:
    """箱式呼吸：海豹突击队使用的压力管理技术"""
    steps = [
        BreathingStep(BreathPhase.INHALE, 4.0, "缓慢吸气", "吸气"),
        BreathingStep(BreathPhase.HOLD_IN, 4.0, "屏住呼吸", "屏气"),
        BreathingStep(BreathPhase.EXHALE, 4.0, "缓慢呼气", "呼气"),
        BreathingStep(BreathPhase.HOLD_OUT, 4.0, "屏住呼吸", "屏气"),
    ]
    return BreathingPattern(
        name="箱式呼吸",
        technique=BreathingTechnique.BOX_BREATHING,
        steps=steps,
        cycles=4,
        total_duration=16.0,
        benefits=[
            "提高专注力",
            "减少压力",
            "增强肺活量",
            "帮助应对高压情况"
        ],
        contraindications=[
            "心脏病患者请咨询医生",
            "如果感到头晕请停止"
        ],
        difficulty="easy",
        description="海豹突击队使用的压力管理技术，四个阶段等长"
    )


def create_ujjayi() -> BreathingPattern:
    """乌加依呼吸：瑜伽中常用的呼吸法"""
    steps = [
        BreathingStep(BreathPhase.INHALE, 5.0, "通过鼻子吸气，轻微收缩喉咙", "吸气"),
        BreathingStep(BreathPhase.HOLD_IN, 2.0, "短暂屏息", "屏气"),
        BreathingStep(BreathPhase.EXHALE, 5.0, "通过鼻子呼气，发出轻微海浪声", "呼气"),
    ]
    return BreathingPattern(
        name="乌加依呼吸",
        technique=BreathingTechnique.UJJAYI,
        steps=steps,
        cycles=10,
        total_duration=12.0,
        benefits=[
            "增强专注力",
            "产生身体热量",
            "平衡神经系统",
            "支持瑜伽练习"
        ],
        contraindications=[
            "低血压患者谨慎",
            "心脏病患者请咨询医生"
        ],
        difficulty="medium",
        description="瑜伽中常用的呼吸法，又称'胜利呼吸'"
    )


def create_diaphragmatic() -> BreathingPattern:
    """腹式呼吸：基础呼吸训练"""
    steps = [
        BreathingStep(BreathPhase.INHALE, 4.0, "用鼻子缓慢吸气，腹部扩张", "吸气"),
        BreathingStep(BreathPhase.HOLD_IN, 1.0, "短暂停顿", "停顿"),
        BreathingStep(BreathPhase.EXHALE, 6.0, "用嘴缓慢呼气，腹部收缩", "呼气"),
    ]
    return BreathingPattern(
        name="腹式呼吸",
        technique=BreathingTechnique.DIAPHRAGMATIC,
        steps=steps,
        cycles=10,
        total_duration=11.0,
        benefits=[
            "增强肺功能",
            "减少压力和焦虑",
            "改善核心稳定性",
            "促进放松"
        ],
        contraindications=[],
        difficulty="easy",
        description="最基础也是最有效的呼吸训练方法"
    )


def create_alternate_nostril() -> BreathingPattern:
    """交替鼻孔呼吸：瑜伽经典呼吸法"""
    steps = [
        BreathingStep(BreathPhase.INHALE_LEFT, 4.0, "按住右鼻孔，左鼻孔吸气", "左吸"),
        BreathingStep(BreathPhase.HOLD_IN, 2.0, "按住双鼻孔屏息", "屏气"),
        BreathingStep(BreathPhase.EXHALE, 4.0, "按住左鼻孔，右鼻孔呼气", "右呼"),
        BreathingStep(BreathPhase.INHALE_RIGHT, 4.0, "按住左鼻孔，右鼻孔吸气", "右吸"),
        BreathingStep(BreathPhase.HOLD_IN, 2.0, "按住双鼻孔屏息", "屏气"),
        BreathingStep(BreathPhase.EXHALE, 4.0, "按住右鼻孔，左鼻孔呼气", "左呼"),
    ]
    return BreathingPattern(
        name="交替鼻孔呼吸",
        technique=BreathingTechnique.ALTERNATE_NOSTRIL,
        steps=steps,
        cycles=5,
        total_duration=20.0,
        benefits=[
            "平衡左右大脑",
            "清理鼻腔",
            "增强专注力",
            "平衡神经系统"
        ],
        contraindications=[
            "感冒鼻塞时不宜",
            "高血压患者谨慎"
        ],
        difficulty="medium",
        description="瑜伽经典呼吸法，称Nadi Shodhana"
    )


def create_energizing() -> BreathingPattern:
    """激活呼吸：提高能量和警觉性"""
    steps = [
        BreathingStep(BreathPhase.INHALE, 1.0, "快速有力吸气", "快吸"),
        BreathingStep(BreathPhase.EXHALE, 1.0, "快速有力呼气", "快呼"),
    ]
    return BreathingPattern(
        name="激活呼吸",
        technique=BreathingTechnique.ENERGIZING,
        steps=steps,
        cycles=20,
        total_duration=2.0,
        benefits=[
            "快速提升能量",
            "增加警觉性",
            "激活交感神经",
            "清晨唤醒"
        ],
        contraindications=[
            "高血压患者不宜",
            "心脏病患者禁止",
            "孕妇不宜",
            "焦虑症患者谨慎"
        ],
        difficulty="medium",
        description="快速呼吸技巧，激活交感神经系统"
    )


def create_meditation() -> BreathingPattern:
    """冥想呼吸：自然呼吸观察"""
    steps = [
        BreathingStep(BreathPhase.INHALE, 5.0, "自然吸气，观察呼吸", "吸气"),
        BreathingStep(BreathPhase.HOLD_IN, 1.0, "短暂停顿", "停顿"),
        BreathingStep(BreathPhase.EXHALE, 6.0, "自然呼气，保持觉知", "呼气"),
        BreathingStep(BreathPhase.HOLD_OUT, 1.0, "短暂停顿", "停顿"),
    ]
    return BreathingPattern(
        name="冥想呼吸",
        technique=BreathingTechnique.MEDITATION,
        steps=steps,
        cycles=15,
        total_duration=13.0,
        benefits=[
            "增强正念",
            "减少杂念",
            "提升意识",
            "深度放松"
        ],
        contraindications=[],
        difficulty="easy",
        description="正念冥想的基础呼吸练习"
    )


def create_sleep_breath() -> BreathingPattern:
    """睡眠呼吸：帮助入睡的呼吸法"""
    steps = [
        BreathingStep(BreathPhase.INHALE, 4.0, "缓慢吸气", "吸气"),
        BreathingStep(BreathPhase.EXHALE, 6.0, "非常缓慢呼气", "呼气"),
    ]
    return BreathingPattern(
        name="睡眠呼吸",
        technique=BreathingTechnique.SLEEP_BREATH,
        steps=steps,
        cycles=20,
        total_duration=10.0,
        benefits=[
            "促进睡眠",
            "降低心率",
            "激活副交感神经",
            "减少入睡时间"
        ],
        contraindications=[],
        difficulty="easy",
        description="呼气长于吸气的呼吸模式，促进放松和睡眠"
    )


def create_physiological_sigh() -> BreathingPattern:
    """生理性叹息：斯坦福大学研究的快速减压法"""
    steps = [
        BreathingStep(BreathPhase.INHALE, 1.5, "深吸一口气", "吸气"),
        BreathingStep(BreathPhase.INHALE, 0.5, "再短吸一口", "补吸"),
        BreathingStep(BreathPhase.EXHALE, 4.0, "长而缓慢地呼气", "呼气"),
    ]
    return BreathingPattern(
        name="生理性叹息",
        technique=BreathingTechnique.PHYSIOLOGICAL_SIGH,
        steps=steps,
        cycles=3,
        total_duration=6.0,
        benefits=[
            "快速减压",
            "恢复肺泡功能",
            "减少二氧化碳",
            "立竿见影的放松效果"
        ],
        contraindications=[],
        difficulty="easy",
        description="斯坦福大学研究证实的高效减压呼吸法"
    )


def create_tactical() -> BreathingPattern:
    """战术呼吸：军事和执法部门使用"""
    steps = [
        BreathingStep(BreathPhase.INHALE, 4.0, "吸气 4 秒", "吸气"),
        BreathingStep(BreathPhase.HOLD_IN, 4.0, "屏气 4 秒", "屏气"),
        BreathingStep(BreathPhase.EXHALE, 4.0, "呼气 4 秒", "呼气"),
        BreathingStep(BreathPhase.HOLD_OUT, 4.0, "屏气 4 秒", "屏气"),
    ]
    return BreathingPattern(
        name="战术呼吸",
        technique=BreathingTechnique.TACTICAL,
        steps=steps,
        cycles=4,
        total_duration=16.0,
        benefits=[
            "降低应激反应",
            "提高战术表现",
            "控制恐慌",
            "增强决策能力"
        ],
        contraindications=[],
        difficulty="easy",
        description="军事和执法部门用于控制战斗应激的呼吸技术"
    )


def create_coherent() -> BreathingPattern:
    """连贯呼吸：心脏相干性呼吸"""
    steps = [
        BreathingStep(BreathPhase.INHALE, 5.0, "均匀吸气", "吸气"),
        BreathingStep(BreathPhase.EXHALE, 5.0, "均匀呼气", "呼气"),
    ]
    return BreathingPattern(
        name="连贯呼吸",
        technique=BreathingTechnique.COHERENT,
        steps=steps,
        cycles=12,
        total_duration=10.0,
        benefits=[
            "心脏相干性",
            "心率变异性平衡",
            "情绪稳定",
            "自主神经平衡"
        ],
        contraindications=[],
        difficulty="easy",
        description="每分钟 6 次呼吸，促进心脏相干性"
    )


def create_resonant() -> BreathingPattern:
    """共振呼吸：个性化最佳呼吸频率"""
    steps = [
        BreathingStep(BreathPhase.INHALE, 5.5, "缓慢均匀吸气", "吸气"),
        BreathingStep(BreathPhase.EXHALE, 5.5, "缓慢均匀呼气", "呼气"),
    ]
    return BreathingPattern(
        name="共振呼吸",
        technique=BreathingTechnique.RESONANT,
        steps=steps,
        cycles=11,
        total_duration=11.0,
        benefits=[
            "优化心率变异性",
            "增强自主神经功能",
            "降低血压",
            "改善情绪"
        ],
        contraindications=[],
        difficulty="medium",
        description="接近每分钟 5.5 次呼吸的共振频率"
    )


def create_wim_hof() -> BreathingPattern:
    """Wim Hof 呼吸法：强力呼吸技术"""
    steps = [
        BreathingStep(BreathPhase.INHALE, 1.0, "深吸气", "吸"),
        BreathingStep(BreathPhase.EXHALE, 0.5, "自然呼气（不主动）", "呼"),
    ]
    return BreathingPattern(
        name="Wim Hof 呼吸法",
        technique=BreathingTechnique.WIM_HOF,
        steps=steps,
        cycles=30,  # 30 次快速呼吸
        total_duration=1.5,
        benefits=[
            "增强免疫力",
            "提高耐寒能力",
            "增加能量",
            "精神清晰"
        ],
        contraindications=[
            "不要在水中练习",
            "心脏病患者禁止",
            "癫痫患者禁止",
            "孕妇禁止",
            "驾驶或水中附近不要练习"
        ],
        difficulty="hard",
        description="Wim Hof 开发的强力呼吸技术，需要谨慎练习"
    )


def create_calming() -> BreathingPattern:
    """镇静呼吸：快速平静情绪"""
    steps = [
        BreathingStep(BreathPhase.INHALE, 4.0, "缓慢吸气", "吸气"),
        BreathingStep(BreathPhase.HOLD_IN, 2.0, "短暂屏息", "屏气"),
        BreathingStep(BreathPhase.EXHALE, 8.0, "非常缓慢呼气", "呼气"),
    ]
    return BreathingPattern(
        name="镇静呼吸",
        technique=BreathingTechnique.CALMING,
        steps=steps,
        cycles=5,
        total_duration=14.0,
        benefits=[
            "快速镇静",
            "减少恐慌",
            "降低心率",
            "缓解焦虑"
        ],
        contraindications=[],
        difficulty="easy",
        description="呼气时间为吸气两倍，激活副交感神经"
    )


def create_focus() -> BreathingPattern:
    """专注呼吸：提高注意力和认知能力"""
    steps = [
        BreathingStep(BreathPhase.INHALE, 4.0, "集中注意力吸气", "吸气"),
        BreathingStep(BreathPhase.HOLD_IN, 4.0, "保持专注屏气", "屏气"),
        BreathingStep(BreathPhase.EXHALE, 6.0, "专注呼气", "呼气"),
    ]
    return BreathingPattern(
        name="专注呼吸",
        technique=BreathingTechnique.FOCUS,
        steps=steps,
        cycles=8,
        total_duration=14.0,
        benefits=[
            "提高专注力",
            "增强认知能力",
            "改善注意力",
            "准备工作学习"
        ],
        contraindications=[],
        difficulty="easy",
        description="用于提高注意力和准备高强度认知任务的呼吸法"
    )


# 技巧到创建函数的映射
TECHNIQUE_CREATORS: Dict[BreathingTechnique, Callable[[], BreathingPattern]] = {
    BreathingTechnique.RELAXATION_478: create_478_relaxation,
    BreathingTechnique.BOX_BREATHING: create_box_breathing,
    BreathingTechnique.UJJAYI: create_ujjayi,
    BreathingTechnique.DIAPHRAGMATIC: create_diaphragmatic,
    BreathingTechnique.ALTERNATE_NOSTRIL: create_alternate_nostril,
    BreathingTechnique.ENERGIZING: create_energizing,
    BreathingTechnique.MEDITATION: create_meditation,
    BreathingTechnique.SLEEP_BREATH: create_sleep_breath,
    BreathingTechnique.PHYSIOLOGICAL_SIGH: create_physiological_sigh,
    BreathingTechnique.TACTICAL: create_tactical,
    BreathingTechnique.COHERENT: create_coherent,
    BreathingTechnique.RESONANT: create_resonant,
    BreathingTechnique.WIM_HOF: create_wim_hof,
    BreathingTechnique.CALMING: create_calming,
    BreathingTechnique.FOCUS: create_focus,
}


# ==================== 核心功能函数 ====================

def get_pattern(technique: BreathingTechnique) -> BreathingPattern:
    """
    获取指定技巧的呼吸模式
    
    Args:
        technique: 呼吸技巧类型
    
    Returns:
        BreathingPattern 对象
    """
    if technique not in TECHNIQUE_CREATORS:
        raise ValueError(f"未知的呼吸技巧: {technique}")
    return TECHNIQUE_CREATORS[technique]()


def list_techniques() -> List[BreathingTechnique]:
    """列出所有可用的呼吸技巧"""
    return list(TECHNIQUE_CREATORS.keys())


def get_technique_by_name(name: str) -> Optional[BreathingTechnique]:
    """
    通过名称获取呼吸技巧
    
    Args:
        name: 技巧名称（支持中英文）
    
    Returns:
        BreathingTechnique 或 None
    """
    name_lower = name.lower().strip()
    
    # 名称映射
    name_map = {
        # 英文名称
        "4-7-8": BreathingTechnique.RELAXATION_478,
        "relaxation": BreathingTechnique.RELAXATION_478,
        "relaxation_478": BreathingTechnique.RELAXATION_478,
        "box": BreathingTechnique.BOX_BREATHING,
        "box_breathing": BreathingTechnique.BOX_BREATHING,
        "ujjayi": BreathingTechnique.UJJAYI,
        "diaphragmatic": BreathingTechnique.DIAPHRAGMATIC,
        "alternate_nostril": BreathingTechnique.ALTERNATE_NOSTRIL,
        "energizing": BreathingTechnique.ENERGIZING,
        "meditation": BreathingTechnique.MEDITATION,
        "sleep": BreathingTechnique.SLEEP_BREATH,
        "sleep_breath": BreathingTechnique.SLEEP_BREATH,
        "physiological_sigh": BreathingTechnique.PHYSIOLOGICAL_SIGH,
        "tactical": BreathingTechnique.TACTICAL,
        "coherent": BreathingTechnique.COHERENT,
        "resonant": BreathingTechnique.RESONANT,
        "wim_hof": BreathingTechnique.WIM_HOF,
        "calming": BreathingTechnique.CALMING,
        "focus": BreathingTechnique.FOCUS,
        # 中文名称
        "放松": BreathingTechnique.RELAXATION_478,
        "放松呼吸": BreathingTechnique.RELAXATION_478,
        "箱式呼吸": BreathingTechnique.BOX_BREATHING,
        "乌加依": BreathingTechnique.UJJAYI,
        "腹式呼吸": BreathingTechnique.DIAPHRAGMATIC,
        "交替鼻孔": BreathingTechnique.ALTERNATE_NOSTRIL,
        "激活": BreathingTechnique.ENERGIZING,
        "冥想": BreathingTechnique.MEDITATION,
        "睡眠": BreathingTechnique.SLEEP_BREATH,
        "生理性叹息": BreathingTechnique.PHYSIOLOGICAL_SIGH,
        "战术": BreathingTechnique.TACTICAL,
        "连贯": BreathingTechnique.COHERENT,
        "共振": BreathingTechnique.RESONANT,
        "镇静": BreathingTechnique.CALMING,
        "专注": BreathingTechnique.FOCUS,
    }
    
    return name_map.get(name_lower)


def calculate_total_duration(pattern: BreathingPattern, cycles: int) -> float:
    """
    计算指定循环次数的总时长
    
    Args:
        pattern: 呼吸模式
        cycles: 循环次数
    
    Returns:
        总时长（秒）
    """
    return pattern.total_duration * cycles


def calculate_breaths_per_minute(pattern: BreathingPattern) -> float:
    """
    计算每分钟呼吸次数
    
    Args:
        pattern: 呼吸模式
    
    Returns:
        每分钟呼吸次数
    """
    return 60.0 / pattern.total_duration


def generate_session_steps(
    pattern: BreathingPattern,
    cycles: Optional[int] = None
) -> List[Tuple[int, BreathingStep]]:
    """
    生成完整练习会话的所有步骤
    
    Args:
        pattern: 呼吸模式
        cycles: 循环次数（默认使用模式建议）
    
    Returns:
        List[(循环编号, 步骤)]
    """
    if cycles is None:
        cycles = pattern.cycles
    
    result = []
    for cycle in range(1, cycles + 1):
        for step in pattern.steps:
            result.append((cycle, step))
    
    return result


def create_custom_pattern(
    name: str,
    inhale: float,
    hold_in: float = 0,
    exhale: float = 0,
    hold_out: float = 0,
    cycles: int = 10,
    benefits: Optional[List[str]] = None,
    description: str = ""
) -> BreathingPattern:
    """
    创建自定义呼吸模式
    
    Args:
        name: 模式名称
        inhale: 吸气时长（秒）
        hold_in: 屏气时长（秒）
        exhale: 呼气时长（秒）
        hold_out: 呼气后屏气时长（秒）
        cycles: 建议循环次数
        benefits: 益处列表
        description: 描述
    
    Returns:
        BreathingPattern 对象
    """
    steps = []
    total_duration = 0
    
    if inhale > 0:
        steps.append(BreathingStep(BreathPhase.INHALE, inhale, "吸气", "吸气"))
        total_duration += inhale
    
    if hold_in > 0:
        steps.append(BreathingStep(BreathPhase.HOLD_IN, hold_in, "屏气", "屏气"))
        total_duration += hold_in
    
    if exhale > 0:
        steps.append(BreathingStep(BreathPhase.EXHALE, exhale, "呼气", "呼气"))
        total_duration += exhale
    
    if hold_out > 0:
        steps.append(BreathingStep(BreathPhase.HOLD_OUT, hold_out, "屏气", "屏气"))
        total_duration += hold_out
    
    return BreathingPattern(
        name=name,
        technique=BreathingTechnique.MEDITATION,  # 使用默认技巧类型
        steps=steps,
        cycles=cycles,
        total_duration=total_duration,
        benefits=benefits or [],
        contraindications=[],
        difficulty="custom",
        description=description
    )


def format_timer_display(seconds: float) -> str:
    """
    格式化时间显示
    
    Args:
        seconds: 秒数
    
    Returns:
        格式化的时间字符串
    """
    mins = int(seconds // 60)
    secs = int(seconds % 60)
    if mins > 0:
        return f"{mins}:{secs:02d}"
    return f"{secs}s"


def get_recommended_technique(
    goal: str,
    time_available: Optional[float] = None
) -> BreathingTechnique:
    """
    根据目标推荐呼吸技巧
    
    Args:
        goal: 目标（sleep, relax, energy, focus, anxiety, calm）
        time_available: 可用时间（秒）
    
    Returns:
        推荐的 BreathingTechnique
    """
    goal_map = {
        "sleep": [BreathingTechnique.SLEEP_BREATH, BreathingTechnique.CALMING],
        "relax": [BreathingTechnique.RELAXATION_478, BreathingTechnique.CALMING],
        "relaxation": [BreathingTechnique.RELAXATION_478, BreathingTechnique.CALMING],
        "energy": [BreathingTechnique.ENERGIZING, BreathingTechnique.WIM_HOF],
        "energize": [BreathingTechnique.ENERGIZING, BreathingTechnique.WIM_HOF],
        "focus": [BreathingTechnique.FOCUS, BreathingTechnique.BOX_BREATHING],
        "concentration": [BreathingTechnique.FOCUS, BreathingTechnique.MEDITATION],
        "anxiety": [BreathingTechnique.PHYSIOLOGICAL_SIGH, BreathingTechnique.CALMING],
        "anxious": [BreathingTechnique.PHYSIOLOGICAL_SIGH, BreathingTechnique.CALMING],
        "calm": [BreathingTechnique.CALMING, BreathingTechnique.COHERENT],
        "meditation": [BreathingTechnique.MEDITATION, BreathingTechnique.COHERENT],
        "stress": [BreathingTechnique.BOX_BREATHING, BreathingTechnique.TACTICAL],
        "performance": [BreathingTechnique.TACTICAL, BreathingTechnique.BOX_BREATHING],
    }
    
    goal_lower = goal.lower().strip()
    techniques = goal_map.get(goal_lower, [BreathingTechnique.BOX_BREATHING])
    
    # 如果有时间限制，选择时间合适的技巧
    if time_available is not None:
        for tech in techniques:
            pattern = get_pattern(tech)
            if pattern.total_duration * pattern.cycles <= time_available:
                return tech
    
    return techniques[0]


def get_techniques_by_difficulty(difficulty: str) -> List[BreathingTechnique]:
    """
    获取指定难度的所有技巧
    
    Args:
        difficulty: 难度级别（easy, medium, hard）
    
    Returns:
        技巧列表
    """
    result = []
    for tech in TECHNIQUE_CREATORS:
        pattern = get_pattern(tech)
        if pattern.difficulty == difficulty.lower():
            result.append(tech)
    return result


def get_techniques_by_benefit(benefit: str) -> List[BreathingTechnique]:
    """
    根据益处查找技巧
    
    Args:
        benefit: 益处关键词
    
    Returns:
        匹配的技巧列表
    """
    result = []
    benefit_lower = benefit.lower()
    
    for tech in TECHNIQUE_CREATORS:
        pattern = get_pattern(tech)
        for b in pattern.benefits:
            if benefit_lower in b.lower():
                result.append(tech)
                break
    
    return result


def calculate_oxygen_efficiency(
    pattern: BreathingPattern,
    tidal_volume_liters: float = 0.5
) -> Dict[str, float]:
    """
    计算呼吸模式的氧气效率估算
    
    Args:
        pattern: 呼吸模式
        tidal_volume_liters: 潮气量（升），默认 0.5L
    
    Returns:
        包含各项指标的字典
    """
    # 每分钟呼吸次数
    breaths_per_min = calculate_breaths_per_minute(pattern)
    
    # 每分钟通气量
    minute_volume = breaths_per_min * tidal_volume_liters
    
    # 估算吸气比例
    inhale_time = sum(s.duration for s in pattern.steps if s.phase == BreathPhase.INHALE or s.phase == BreathPhase.INHALE_LEFT or s.phase == BreathPhase.INHALE_RIGHT)
    inhale_ratio = inhale_time / pattern.total_duration if pattern.total_duration > 0 else 0.5
    
    # 估算呼气比例
    exhale_time = sum(s.duration for s in pattern.steps if s.phase == BreathPhase.EXHALE)
    exhale_ratio = exhale_time / pattern.total_duration if pattern.total_duration > 0 else 0.5
    
    return {
        "breaths_per_minute": round(breaths_per_min, 2),
        "minute_volume_liters": round(minute_volume, 2),
        "inhale_ratio": round(inhale_ratio, 2),
        "exhale_ratio": round(exhale_ratio, 2),
        "estimated_relaxation_score": round(exhale_ratio / inhale_ratio, 2) if inhale_ratio > 0 else 1.0
    }


def compare_techniques(
    techniques: List[BreathingTechnique]
) -> List[Dict]:
    """
    比较多个呼吸技巧
    
    Args:
        techniques: 要比较的技巧列表
    
    Returns:
        比较结果列表
    """
    result = []
    for tech in techniques:
        if tech not in TECHNIQUE_CREATORS:
            continue
        
        pattern = get_pattern(tech)
        efficiency = calculate_oxygen_efficiency(pattern)
        
        result.append({
            "technique": tech.value,
            "name": pattern.name,
            "total_duration": pattern.total_duration,
            "recommended_cycles": pattern.cycles,
            "difficulty": pattern.difficulty,
            "breaths_per_minute": efficiency["breaths_per_minute"],
            "relaxation_score": efficiency["estimated_relaxation_score"],
            "benefits": pattern.benefits,
        })
    
    return result


def generate_breathing_text_guide(
    pattern: BreathingPattern,
    cycles: Optional[int] = None
) -> str:
    """
    生成文本指导脚本
    
    Args:
        pattern: 呼吸模式
        cycles: 循环次数
    
    Returns:
        文本指导脚本
    """
    if cycles is None:
        cycles = pattern.cycles
    
    lines = [
        f"=== {pattern.name} ===",
        f"难度: {pattern.difficulty}",
        f"建议循环: {cycles} 次",
        f"单循环时长: {pattern.total_duration} 秒",
        f"总时长: {calculate_total_duration(pattern, cycles):.0f} 秒",
        "",
        "益处:",
    ]
    
    for benefit in pattern.benefits:
        lines.append(f"  • {benefit}")
    
    if pattern.contraindications:
        lines.append("")
        lines.append("注意事项:")
        for contra in pattern.contraindications:
            lines.append(f"  ⚠️ {contra}")
    
    lines.extend([
        "",
        "--- 开始练习 ---",
        "",
    ])
    
    for cycle in range(1, cycles + 1):
        lines.append(f"【第 {cycle}/{cycles} 轮】")
        for step in pattern.steps:
            lines.append(f"  {step.instruction} ({step.duration}秒): {step.description}")
        lines.append("")
    
    lines.append("练习完成！")
    
    return "\n".join(lines)


def get_quick_relief_sequence() -> List[BreathingStep]:
    """
    获取快速缓解序列（生理性叹息的简化版）
    
    Returns:
        快速缓解步骤列表
    """
    return [
        BreathingStep(BreathPhase.INHALE, 1.0, "深吸气", "吸"),
        BreathingStep(BreathPhase.INHALE, 1.0, "再吸一口气", "补吸"),
        BreathingStep(BreathPhase.EXHALE, 3.0, "缓慢呼气", "呼"),
    ]


def calculate_hrv_estimate(pattern: BreathingPattern) -> float:
    """
    估算呼吸模式对心率变异性的影响
    
    Args:
        pattern: 呼吸模式
    
    Returns:
        HRV 影响分数（0-100）
    """
    bpm = calculate_breaths_per_minute(pattern)
    
    # 5-7 次/分钟的呼吸通常最优 HRV
    if 5 <= bpm <= 7:
        return 95.0
    elif 4 <= bpm <= 8:
        return 85.0
    elif 3 <= bpm <= 10:
        return 70.0
    elif bpm < 3:
        return 60.0  # 太慢可能不好
    else:
        return max(30.0, 100 - bpm * 5)


# ==================== 练习会话管理 ====================

class BreathingSession:
    """呼吸练习会话管理器"""
    
    def __init__(self, technique: BreathingTechnique):
        """
        初始化练习会话
        
        Args:
            technique: 呼吸技巧
        """
        self.technique = technique
        self.pattern = get_pattern(technique)
        self.cycles_completed = 0
        self.current_cycle = 0
        self.current_step_index = 0
        self.start_time: Optional[float] = None
        self.end_time: Optional[float] = None
        self.elapsed_time = 0.0
        self.is_running = False
        self.is_paused = False
        self._step_start_time: Optional[float] = None
    
    def start(self, cycles: Optional[int] = None):
        """
        开始练习
        
        Args:
            cycles: 循环次数
        """
        if cycles is not None:
            self.target_cycles = cycles
        else:
            self.target_cycles = self.pattern.cycles
        
        self.start_time = time.time()
        self.current_cycle = 1
        self.current_step_index = 0
        self.cycles_completed = 0
        self.is_running = True
        self.is_paused = False
        self._step_start_time = time.time()
    
    def pause(self):
        """暂停练习"""
        self.is_paused = True
    
    def resume(self):
        """恢复练习"""
        self.is_paused = False
    
    def stop(self):
        """停止练习"""
        self.is_running = False
        self.end_time = time.time()
        if self.start_time:
            self.elapsed_time = self.end_time - self.start_time
    
    def get_current_step(self) -> Optional[BreathingStep]:
        """获取当前步骤"""
        if not self.is_running:
            return None
        return self.pattern.steps[self.current_step_index]
    
    def get_remaining_time_in_step(self) -> float:
        """获取当前步骤剩余时间"""
        if not self.is_running or self._step_start_time is None:
            return 0.0
        
        elapsed = time.time() - self._step_start_time
        step = self.get_current_step()
        if step:
            return max(0, step.duration - elapsed)
        return 0.0
    
    def update(self) -> Optional[Tuple[int, BreathingStep, float]]:
        """
        更新状态
        
        Returns:
            (循环编号, 当前步骤, 步骤剩余时间) 或 None（如果已完成）
        """
        if not self.is_running or self.is_paused:
            return None
        
        step = self.get_current_step()
        if step is None:
            return None
        
        elapsed_in_step = time.time() - self._step_start_time if self._step_start_time else 0
        
        if elapsed_in_step >= step.duration:
            # 进入下一步
            self.current_step_index += 1
            
            if self.current_step_index >= len(self.pattern.steps):
                # 完成一轮
                self.cycles_completed += 1
                self.current_cycle += 1
                self.current_step_index = 0
                
                if self.current_cycle > self.target_cycles:
                    self.stop()
                    return None
            
            self._step_start_time = time.time()
            step = self.get_current_step()
        
        remaining = step.duration - elapsed_in_step if step else 0
        
        return (self.current_cycle, step, max(0, remaining))
    
    def get_progress(self) -> Dict:
        """获取进度信息"""
        total_steps = len(self.pattern.steps) * self.target_cycles
        completed_steps = (self.cycles_completed * len(self.pattern.steps) + 
                          (self.current_cycle - 1) * len(self.pattern.steps) + 
                          self.current_step_index)
        
        return {
            "cycles_completed": self.cycles_completed,
            "current_cycle": self.current_cycle,
            "total_cycles": self.target_cycles,
            "current_step": self.current_step_index + 1,
            "total_steps_per_cycle": len(self.pattern.steps),
            "progress_percent": round(completed_steps / total_steps * 100, 1) if total_steps > 0 else 0,
            "elapsed_time": round(time.time() - self.start_time, 1) if self.start_time else 0,
            "remaining_time": round(calculate_total_duration(self.pattern, self.target_cycles) - 
                                   (time.time() - self.start_time), 1) if self.start_time else 0,
        }
    
    def get_summary(self) -> ExerciseSession:
        """获取练习摘要"""
        return ExerciseSession(
            technique=self.technique,
            pattern=self.pattern,
            cycles_completed=self.cycles_completed,
            total_time=self.elapsed_time,
            start_time=self.start_time or 0,
            end_time=self.end_time
        )


# ==================== 便捷函数 ====================

def quick_relax(cycles: int = 3) -> BreathingPattern:
    """
    快速放松（返回 4-7-8 呼吸模式）
    
    Args:
        cycles: 循环次数
    
    Returns:
        BreathingPattern
    """
    pattern = get_pattern(BreathingTechnique.RELAXATION_478)
    return BreathingPattern(
        name=pattern.name,
        technique=pattern.technique,
        steps=pattern.steps,
        cycles=cycles,
        total_duration=pattern.total_duration,
        benefits=pattern.benefits,
        contraindications=pattern.contraindications,
        difficulty=pattern.difficulty,
        description=pattern.description
    )


def quick_sleep(cycles: int = 10) -> BreathingPattern:
    """
    快速睡眠（返回睡眠呼吸模式）
    
    Args:
        cycles: 循环次数
    
    Returns:
        BreathingPattern
    """
    pattern = get_pattern(BreathingTechnique.SLEEP_BREATH)
    return BreathingPattern(
        name=pattern.name,
        technique=pattern.technique,
        steps=pattern.steps,
        cycles=cycles,
        total_duration=pattern.total_duration,
        benefits=pattern.benefits,
        contraindications=pattern.contraindications,
        difficulty=pattern.difficulty,
        description=pattern.description
    )


def quick_energy(cycles: int = 20) -> BreathingPattern:
    """
    快速激活（返回激活呼吸模式）
    
    Args:
        cycles: 循环次数
    
    Returns:
        BreathingPattern
    """
    pattern = get_pattern(BreathingTechnique.ENERGIZING)
    return BreathingPattern(
        name=pattern.name,
        technique=pattern.technique,
        steps=pattern.steps,
        cycles=cycles,
        total_duration=pattern.total_duration,
        benefits=pattern.benefits,
        contraindications=pattern.contraindications,
        difficulty=pattern.difficulty,
        description=pattern.description
    )


def print_pattern_info(technique: BreathingTechnique):
    """
    打印技巧信息
    
    Args:
        technique: 呼吸技巧
    """
    pattern = get_pattern(technique)
    guide = generate_breathing_text_guide(pattern)
    print(guide)


if __name__ == "__main__":
    # 示例用法
    print("=== 呼吸练习工具示例 ===\n")
    
    # 列出所有技巧
    print("可用技巧:")
    for tech in list_techniques():
        pattern = get_pattern(tech)
        print(f"  • {pattern.name} ({tech.value})")
    
    print("\n" + "=" * 50 + "\n")
    
    # 获取 4-7-8 呼吸模式
    pattern_478 = get_pattern(BreathingTechnique.RELAXATION_478)
    print(f"4-7-8 呼吸:")
    print(f"  单循环时长: {pattern_478.total_duration} 秒")
    print(f"  建议循环: {pattern_478.cycles} 次")
    print(f"  总时长: {calculate_total_duration(pattern_478, pattern_478.cycles):.0f} 秒")
    print(f"  每分钟呼吸: {calculate_breaths_per_minute(pattern_478):.1f} 次")
    
    print("\n" + "=" * 50 + "\n")
    
    # 创建自定义模式
    custom = create_custom_pattern(
        name="我的放松呼吸",
        inhale=4.0,
        hold_in=4.0,
        exhale=6.0,
        cycles=8,
        benefits=["放松", "减压"],
        description="自定义呼吸模式"
    )
    print(f"自定义模式: {custom.name}")
    print(f"  总时长: {custom.total_duration} 秒")
    
    print("\n" + "=" * 50 + "\n")
    
    # 根据目标推荐
    recommended = get_recommended_technique("sleep")
    rec_pattern = get_pattern(recommended)
    print(f"睡眠推荐: {rec_pattern.name}")
    
    print("\n" + "=" * 50 + "\n")
    
    # 生成文本指导
    print(generate_breathing_text_guide(get_pattern(BreathingTechnique.PHYSIOLOGICAL_SIGH), 3))
    
    print("\n" + "=" * 50 + "\n")
    
    # 比较技巧
    comparison = compare_techniques([
        BreathingTechnique.RELAXATION_478,
        BreathingTechnique.BOX_BREATHING,
        BreathingTechnique.COHERENT
    ])
    print("技巧比较:")
    for c in comparison:
        print(f"  {c['name']}: {c['breaths_per_minute']} 次/分, 放松分数: {c['relaxation_score']}")
"""
Tabata Utilities - Tabata 高强度间歇训练工具

提供完整的 Tabata 训练支持，包括：
- 标准 Tabata 计时器（20秒运动 + 10秒休息 × 8组）
- 可自定义的训练参数
- 多种预设训练方案
- 训练统计和进度追踪
- 语音提示接口

零外部依赖，纯 Python 实现。

Tabata 训练简介：
Tabata 是由日本科学家 Izumi Tabata 博士发明的高强度间歇训练方法。
标准格式：20 秒高强度运动 + 10 秒休息，重复 8 轮，总时长 4 分钟。
研究表明这种训练方式能有效提升有氧和无氧能力。
"""

from typing import List, Dict, Optional, Callable, Tuple
from dataclasses import dataclass, field
from enum import Enum
import time
import math


class PhaseType(Enum):
    """训练阶段类型"""
    PREPARE = "prepare"  # 准备阶段
    WORK = "work"       # 运动阶段
    REST = "rest"       # 休息阶段
    COMPLETE = "complete"  # 训练完成


@dataclass
class TabataRound:
    """单个训练轮次"""
    round_number: int
    work_duration: float  # 秒
    rest_duration: float  # 秒
    
    @property
    def total_duration(self) -> float:
        """该轮次总时长"""
        return self.work_duration + self.rest_duration


@dataclass
class TabataSession:
    """Tabata 训练会话"""
    rounds: int                    # 总轮数
    work_duration: float           # 运动时长（秒）
    rest_duration: float           # 休息时长（秒）
    prepare_duration: float = 10   # 准备时长（秒）
    name: str = "Tabata"          # 训练名称
    exercises: List[str] = field(default_factory=list)  # 每轮运动名称
    
    @property
    def total_duration(self) -> float:
        """训练总时长（秒）"""
        return self.prepare_duration + (self.work_duration + self.rest_duration) * self.rounds
    
    @property
    def total_work_time(self) -> float:
        """总运动时长"""
        return self.work_duration * self.rounds
    
    @property
    def total_rest_time(self) -> float:
        """总休息时长"""
        return self.rest_duration * self.rounds
    
    def get_exercise(self, round_num: int) -> str:
        """获取指定轮次的运动名称"""
        if not self.exercises:
            return f"Round {round_num}"
        return self.exercises[(round_num - 1) % len(self.exercises)]


@dataclass
class SessionStats:
    """训练统计"""
    session: TabataSession
    start_time: float = 0
    end_time: float = 0
    completed_rounds: int = 0
    total_paused_time: float = 0
    calories_burned_estimate: float = 0
    
    @property
    def actual_duration(self) -> float:
        """实际训练时长"""
        if self.start_time == 0 or self.end_time == 0:
            return 0
        return self.end_time - self.start_time - self.total_paused_time
    
    @property
    def completion_rate(self) -> float:
        """完成率"""
        if self.session.rounds == 0:
            return 0
        return self.completed_rounds / self.session.rounds * 100
    
    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            'name': self.session.name,
            'completed_rounds': self.completed_rounds,
            'total_rounds': self.session.rounds,
            'completion_rate': f"{self.completion_rate:.1f}%",
            'total_work_time': f"{self.session.total_work_time:.0f}s",
            'actual_duration': f"{self.actual_duration:.0f}s",
            'calories_burned_estimate': f"{self.calories_burned_estimate:.0f} kcal"
        }


class TabataTimer:
    """
    Tabata 计时器
    
    核心计时功能，支持：
    - 标准和自定义 Tabata 格式
    - 准备阶段
    - 暂停/继续
    - 回调通知
    """
    
    def __init__(self, session: TabataSession):
        """
        初始化计时器
        
        Args:
            session: 训练会话配置
        """
        self.session = session
        self._is_running = False
        self._is_paused = False
        self._current_phase = PhaseType.PREPARE
        self._current_round = 0
        self._elapsed_in_phase = 0.0
        self._start_time = 0.0
        self._paused_time = 0.0
        self._total_paused = 0.0
        
        # 回调函数
        self._on_phase_change: Optional[Callable[[PhaseType, int], None]] = None
        self._on_tick: Optional[Callable[[PhaseType, int, float], None]] = None
        self._on_complete: Optional[Callable[[SessionStats], None]] = None
        
        # 统计
        self._stats = SessionStats(session=session)
    
    @property
    def is_running(self) -> bool:
        return self._is_running
    
    @property
    def is_paused(self) -> bool:
        return self._is_paused
    
    @property
    def current_phase(self) -> PhaseType:
        return self._current_phase
    
    @property
    def current_round(self) -> int:
        return self._current_round
    
    @property
    def remaining_time(self) -> float:
        """当前阶段剩余时间"""
        if self._current_phase == PhaseType.PREPARE:
            return self.session.prepare_duration - self._elapsed_in_phase
        elif self._current_phase == PhaseType.WORK:
            return self.session.work_duration - self._elapsed_in_phase
        elif self._current_phase == PhaseType.REST:
            return self.session.rest_duration - self._elapsed_in_phase
        return 0
    
    @property
    def total_remaining(self) -> float:
        """训练总剩余时间"""
        if self._current_phase == PhaseType.COMPLETE:
            return 0
        
        remaining = self.remaining_time
        
        if self._current_phase == PhaseType.PREPARE:
            # 准备阶段后还有所有轮次
            remaining += self.session.total_work_time + self.session.total_rest_time
        elif self._current_phase == PhaseType.WORK:
            # 当前轮次的休息 + 剩余轮次
            remaining += self.session.rest_duration
            remaining_rounds = self.session.rounds - self._current_round
            remaining += remaining_rounds * (self.session.work_duration + self.session.rest_duration)
        elif self._current_phase == PhaseType.REST:
            # 剩余轮次
            remaining_rounds = self.session.rounds - self._current_round
            remaining += remaining_rounds * (self.session.work_duration + self.session.rest_duration)
        
        return remaining
    
    def set_callbacks(self, 
                     on_phase_change: Optional[Callable[[PhaseType, int], None]] = None,
                     on_tick: Optional[Callable[[PhaseType, int, float], None]] = None,
                     on_complete: Optional[Callable[[SessionStats], None]] = None):
        """设置回调函数"""
        self._on_phase_change = on_phase_change
        self._on_tick = on_tick
        self._on_complete = on_complete
    
    def start(self) -> None:
        """开始训练"""
        if self._is_running:
            return
        
        self._is_running = True
        self._is_paused = False
        self._start_time = time.time()
        self._current_phase = PhaseType.PREPARE
        self._current_round = 0
        self._elapsed_in_phase = 0.0
        self._stats = SessionStats(session=self.session)
        self._stats.start_time = self._start_time
        
        self._notify_phase_change()
        self._run()
    
    def pause(self) -> None:
        """暂停训练"""
        if not self._is_running or self._is_paused:
            return
        self._is_paused = True
        self._paused_time = time.time()
    
    def resume(self) -> None:
        """继续训练"""
        if not self._is_paused:
            return
        self._is_paused = False
        self._total_paused += time.time() - self._paused_time
        self._stats.total_paused_time = self._total_paused
        self._run()
    
    def stop(self) -> SessionStats:
        """停止训练"""
        self._is_running = False
        self._is_paused = False
        self._stats.end_time = time.time()
        self._stats.completed_rounds = self._current_round
        return self._stats
    
    def _run(self) -> None:
        """运行计时器"""
        last_tick = time.time()
        
        while self._is_running:
            if self._is_paused:
                time.sleep(0.01)
                continue
            
            now = time.time()
            delta = now - last_tick
            last_tick = now
            
            self._elapsed_in_phase += delta
            
            # 触发 tick 回调
            if self._on_tick:
                self._on_tick(self._current_phase, self._current_round, self.remaining_time)
            
            # 检查阶段是否结束
            if self.remaining_time <= 0:
                self._advance_phase()
            
            time.sleep(0.01)  # 100Hz 更新频率
    
    def _advance_phase(self) -> None:
        """推进到下一阶段"""
        if self._current_phase == PhaseType.PREPARE:
            # 进入第一轮运动
            self._current_phase = PhaseType.WORK
            self._current_round = 1
            self._elapsed_in_phase = 0
            
        elif self._current_phase == PhaseType.WORK:
            # 进入休息
            self._current_phase = PhaseType.REST
            self._elapsed_in_phase = 0
            
        elif self._current_phase == PhaseType.REST:
            # 检查是否还有下一轮
            if self._current_round >= self.session.rounds:
                # 训练完成
                self._current_phase = PhaseType.COMPLETE
                self._is_running = False
                self._stats.end_time = time.time()
                self._stats.completed_rounds = self.session.rounds
                
                # 估算卡路里消耗（约每分钟 15 kcal，高强度）
                self._stats.calories_burned_estimate = (
                    self.session.total_duration / 60 * 15
                )
                
                if self._on_complete:
                    self._on_complete(self._stats)
                return
            else:
                # 进入下一轮
                self._current_round += 1
                self._current_phase = PhaseType.WORK
                self._elapsed_in_phase = 0
        
        self._notify_phase_change()
    
    def _notify_phase_change(self) -> None:
        """通知阶段变化"""
        if self._on_phase_change:
            self._on_phase_change(self._current_phase, self._current_round)


class TabataPresets:
    """
    Tabata 预设训练方案
    """
    
    # 标准 Tabata：20秒运动 + 10秒休息 × 8轮
    STANDARD = TabataSession(
        rounds=8,
        work_duration=20,
        rest_duration=10,
        prepare_duration=10,
        name="Standard Tabata"
    )
    
    # 双倍 Tabata：16轮
    DOUBLE = TabataSession(
        rounds=16,
        work_duration=20,
        rest_duration=10,
        prepare_duration=10,
        name="Double Tabata"
    )
    
    # 半 Tabata：4轮
    HALF = TabataSession(
        rounds=4,
        work_duration=20,
        rest_duration=10,
        prepare_duration=10,
        name="Half Tabata"
    )
    
    # 延长 Tabata：30秒运动 + 15秒休息
    EXTENDED = TabataSession(
        rounds=8,
        work_duration=30,
        rest_duration=15,
        prepare_duration=10,
        name="Extended Tabata"
    )
    
    # HIIT 基础：45秒运动 + 15秒休息
    HIIT_BASIC = TabataSession(
        rounds=8,
        work_duration=45,
        rest_duration=15,
        prepare_duration=10,
        name="HIIT Basic"
    )
    
    # EMOM 风格：60秒运动
    EMOM = TabataSession(
        rounds=10,
        work_duration=60,
        rest_duration=0,
        prepare_duration=10,
        name="EMOM Style"
    )
    
    # 有氧间歇：40秒运动 + 20秒休息
    CARDIO = TabataSession(
        rounds=10,
        work_duration=40,
        rest_duration=20,
        prepare_duration=10,
        name="Cardio Intervals"
    )
    
    # 力量间歇：30秒运动 + 30秒休息
    STRENGTH = TabataSession(
        rounds=6,
        work_duration=30,
        rest_duration=30,
        prepare_duration=10,
        name="Strength Intervals"
    )
    
    # Tabata 核心训练
    CORE = TabataSession(
        rounds=8,
        work_duration=20,
        rest_duration=10,
        prepare_duration=10,
        name="Core Tabata",
        exercises=[
            "Plank Hold",
            "Crunches",
            "Bicycle Crunches",
            "Leg Raises",
            "Russian Twists",
            "Mountain Climbers",
            "Plank Jacks",
            "Dead Bug"
        ]
    )
    
    # Tabata 下肢训练
    LOWER_BODY = TabataSession(
        rounds=8,
        work_duration=20,
        rest_duration=10,
        prepare_duration=10,
        name="Lower Body Tabata",
        exercises=[
            "Squats",
            "Lunges",
            "Jump Squats",
            "Alternating Lunges",
            "Glute Bridges",
            "Sumo Squats",
            "Jump Lunges",
            "Wall Sit"
        ]
    )
    
    # Tabata 上肢训练
    UPPER_BODY = TabataSession(
        rounds=8,
        work_duration=20,
        rest_duration=10,
        prepare_duration=10,
        name="Upper Body Tabata",
        exercises=[
            "Push-ups",
            "Diamond Push-ups",
            "Tricep Dips",
            "Shoulder Taps",
            "Pike Push-ups",
            "Wide Push-ups",
            "Arm Circles",
            "Burpees"
        ]
    )
    
    @classmethod
    def get_all_presets(cls) -> List[TabataSession]:
        """获取所有预设方案"""
        return [
            cls.STANDARD,
            cls.DOUBLE,
            cls.HALF,
            cls.EXTENDED,
            cls.HIIT_BASIC,
            cls.EMOM,
            cls.CARDIO,
            cls.STRENGTH,
            cls.CORE,
            cls.LOWER_BODY,
            cls.UPPER_BODY,
        ]
    
    @classmethod
    def get_by_name(cls, name: str) -> Optional[TabataSession]:
        """按名称获取预设"""
        presets = cls.get_all_presets()
        for preset in presets:
            if preset.name.lower() == name.lower():
                return preset
        return None


class TabataBuilder:
    """
    Tabata 训练构建器
    
    用于创建自定义训练方案。
    """
    
    def __init__(self):
        self._rounds = 8
        self._work_duration = 20
        self._rest_duration = 10
        self._prepare_duration = 10
        self._name = "Custom Tabata"
        self._exercises: List[str] = []
    
    def rounds(self, count: int) -> 'TabataBuilder':
        """设置轮数"""
        if count < 1:
            raise ValueError("Rounds must be at least 1")
        self._rounds = count
        return self
    
    def work(self, seconds: float) -> 'TabataBuilder':
        """设置运动时长"""
        if seconds < 1:
            raise ValueError("Work duration must be at least 1 second")
        self._work_duration = seconds
        return self
    
    def rest(self, seconds: float) -> 'TabataBuilder':
        """设置休息时长"""
        if seconds < 0:
            raise ValueError("Rest duration cannot be negative")
        self._rest_duration = seconds
        return self
    
    def prepare(self, seconds: float) -> 'TabataBuilder':
        """设置准备时长"""
        if seconds < 0:
            raise ValueError("Prepare duration cannot be negative")
        self._prepare_duration = seconds
        return self
    
    def name(self, name: str) -> 'TabataBuilder':
        """设置训练名称"""
        self._name = name
        return self
    
    def exercises(self, *exercises: str) -> 'TabataBuilder':
        """设置运动列表"""
        self._exercises = list(exercises)
        return self
    
    def build(self) -> TabataSession:
        """构建训练会话"""
        return TabataSession(
            rounds=self._rounds,
            work_duration=self._work_duration,
            rest_duration=self._rest_duration,
            prepare_duration=self._prepare_duration,
            name=self._name,
            exercises=self._exercises.copy()
        )


class TabataFormatter:
    """
    Tabata 格式化工具
    
    用于格式化显示训练信息。
    """
    
    @staticmethod
    def format_duration(seconds: float) -> str:
        """格式化时长"""
        if seconds < 60:
            return f"{int(seconds)}s"
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        if secs == 0:
            return f"{minutes}m"
        return f"{minutes}m {secs}s"
    
    @staticmethod
    def format_countdown(seconds: float) -> str:
        """格式化倒计时显示"""
        if seconds < 0:
            seconds = 0
        mins = int(seconds // 60)
        secs = int(seconds % 60)
        ms = int((seconds % 1) * 10)
        if mins > 0:
            return f"{mins:02d}:{secs:02d}.{ms}"
        return f"{secs:02d}.{ms}"
    
    @staticmethod
    def format_session(session: TabataSession) -> str:
        """格式化训练会话信息"""
        lines = [
            f"=== {session.name} ===",
            f"Rounds: {session.rounds}",
            f"Work: {session.work_duration}s",
            f"Rest: {session.rest_duration}s",
            f"Prepare: {session.prepare_duration}s",
            f"Total: {TabataFormatter.format_duration(session.total_duration)}",
        ]
        if session.exercises:
            lines.append("Exercises:")
            for i, ex in enumerate(session.exercises[:session.rounds], 1):
                lines.append(f"  {i}. {ex}")
        return "\n".join(lines)
    
    @staticmethod
    def format_stats(stats: SessionStats) -> str:
        """格式化训练统计"""
        lines = [
            f"=== {stats.session.name} Complete ===",
            f"Rounds: {stats.completed_rounds}/{stats.session.rounds}",
            f"Completion: {stats.completion_rate:.1f}%",
            f"Duration: {TabataFormatter.format_duration(stats.actual_duration)}",
            f"Calories (est.): {stats.calories_burned_estimate:.0f} kcal",
        ]
        return "\n".join(lines)
    
    @staticmethod
    def format_progress(current: int, total: int, width: int = 20) -> str:
        """格式化进度条"""
        if total == 0:
            return "[" + " " * width + "] 0%"
        progress = current / total
        filled = int(progress * width)
        bar = "█" * filled + "░" * (width - filled)
        return f"[{bar}] {progress * 100:.0f}%"


class TabataCalculator:
    """
    Tabata 计算工具
    """
    
    @staticmethod
    def calories_burned(session: TabataSession, weight_kg: float = 70, intensity: float = 1.0) -> float:
        """
        估算卡路里消耗
        
        Args:
            session: 训练会话
            weight_kg: 体重（公斤）
            intensity: 强度系数 (0.5-1.5)
            
        Returns:
            估算卡路里消耗（kcal）
        """
        # MET (Metabolic Equivalent of Task)
        # Tabata: ~8-12 METs，取平均 10
        # 卡路里/分钟 = MET × 体重(kg) × 3.5 / 200
        # 或简化: Calories = MET × 体重 × 时间(分钟) × 0.0175
        met = 10 * intensity
        duration_minutes = session.total_work_time / 60
        return met * weight_kg * duration_minutes * 0.0175
    
    @staticmethod
    def heart_rate_zones(age: int) -> Dict[str, Tuple[int, int]]:
        """
        计算心率区间
        
        Args:
            age: 年龄
            
        Returns:
            心率区间字典 {区间名: (最低, 最高)}
        """
        max_hr = 220 - age
        return {
            "recovery": (int(max_hr * 0.5), int(max_hr * 0.6)),
            "aerobic": (int(max_hr * 0.6), int(max_hr * 0.7)),
            "tempo": (int(max_hr * 0.7), int(max_hr * 0.8)),
            "threshold": (int(max_hr * 0.8), int(max_hr * 0.9)),
            "vo2max": (int(max_hr * 0.9), max_hr),
        }
    
    @staticmethod
    def recommended_rounds(fitness_level: str) -> int:
        """
        根据健身水平推荐轮数
        
        Args:
            fitness_level: 健身水平 (beginner/intermediate/advanced/elite)
            
        Returns:
            推荐轮数
        """
        recommendations = {
            "beginner": 4,
            "intermediate": 6,
            "advanced": 8,
            "elite": 10,
        }
        return recommendations.get(fitness_level.lower(), 8)
    
    @staticmethod
    def work_rest_ratio(session: TabataSession) -> float:
        """
        计算运动休息比
        
        Args:
            session: 训练会话
            
        Returns:
            运动休息比 (如 2:1 返回 2.0)
        """
        if session.rest_duration == 0:
            return float('inf')
        return session.work_duration / session.rest_duration


# 便捷函数
def create_tabata(rounds: int = 8, work: float = 20, rest: float = 10, 
                  prepare: float = 10, name: str = "Custom Tabata") -> TabataSession:
    """
    快速创建 Tabata 训练会话
    
    Args:
        rounds: 轮数
        work: 运动时长（秒）
        rest: 休息时长（秒）
        prepare: 准备时长（秒）
        name: 训练名称
        
    Returns:
        TabataSession 实例
    """
    return TabataSession(
        rounds=rounds,
        work_duration=work,
        rest_duration=rest,
        prepare_duration=prepare,
        name=name
    )


def get_preset(name: str) -> Optional[TabataSession]:
    """按名称获取预设训练方案"""
    return TabataPresets.get_by_name(name)


def list_presets() -> List[str]:
    """列出所有预设名称"""
    return [p.name for p in TabataPresets.get_all_presets()]


if __name__ == "__main__":
    # 演示
    print("=== Tabata 训练工具演示 ===\n")
    
    # 显示预设
    print("可用预设:")
    for name in list_presets():
        print(f"  - {name}")
    
    print("\n" + "=" * 40)
    
    # 显示标准 Tabata
    standard = TabataPresets.STANDARD
    print(TabataFormatter.format_session(standard))
    
    print("\n" + "=" * 40)
    
    # 计算示例
    print(f"\n卡路里消耗估算 (70kg): {TabataCalculator.calories_burned(standard, 70):.0f} kcal")
    print(f"运动休息比: {TabataCalculator.work_rest_ratio(standard):.1f}:1")
    
    # 心率区间
    zones = TabataCalculator.heart_rate_zones(30)
    print(f"\n心率区间 (30岁):")
    for zone, (low, high) in zones.items():
        print(f"  {zone}: {low}-{high} bpm")
    
    # 构建自定义训练
    print("\n" + "=" * 40)
    custom = (TabataBuilder()
              .name("My Custom Workout")
              .rounds(5)
              .work(30)
              .rest(15)
              .prepare(5)
              .exercises("Burpees", "Push-ups", "Squats", "Plank", "Jumping Jacks")
              .build())
    print(TabataFormatter.format_session(custom))
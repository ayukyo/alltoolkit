"""
Focus Session Utils - 深度工作/专注会话跟踪工具

零外部依赖，专注于专注力训练和深度工作效率提升。

功能：
- 专注会话创建、启动、暂停、结束
- 打断分类（微信/邮件/通知/其他）
- 专注质量评分（基于打断次数、时长、完成度）
- 番茄钟模式支持
- 每日/每周专注报告
- 最佳专注时段分析
- 专注目标进度追踪
- 数据导出（CSV格式）

Author: AllToolkit
License: MIT
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta, date
from typing import List, Dict, Optional, Tuple, Set
from enum import Enum
import csv
import io


class SessionStatus(Enum):
    """会话状态"""
    IDLE = "idle"           # 空闲
    RUNNING = "running"     # 进行中
    PAUSED = "paused"       # 已暂停
    COMPLETED = "completed" # 已完成
    ABANDONED = "abandoned" # 已放弃


class DistractionCategory(Enum):
    """打断来源分类"""
    WEIXIN = "weixin"        # 微信
    EMAIL = "email"          # 邮件
    PHONE_CALL = "phone"    # 电话
    NOTIFICATION = "notification"  # 系统通知
    COLLEAGUE = "colleague"  # 同事/他人
    PERSONAL = "personal"   # 个人事务
    UNKNOWN = "unknown"      # 未知
    NONE = "none"            # 无打断


@dataclass
class Distraction:
    """打断记录"""
    timestamp: datetime
    category: DistractionCategory
    duration_seconds: int = 0
    note: str = ""


@dataclass
class FocusSession:
    """单次专注会话"""
    id: str
    planned_duration_minutes: int
    task_name: str = ""
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    status: SessionStatus = SessionStatus.IDLE
    distractions: List[Distraction] = field(default_factory=list)
    pause_time_seconds: int = 0
    notes: str = ""

    @property
    def actual_duration_seconds(self) -> int:
        """实际专注时长（不含暂停）"""
        if not self.start_time:
            return 0
        end = self.end_time or datetime.now()
        total = (end - self.start_time).total_seconds()
        return max(0, int(total - self.pause_time_seconds))

    @property
    def actual_duration_minutes(self) -> float:
        return self.actual_duration_seconds / 60.0

    @property
    def distraction_count(self) -> int:
        return len(self.distractions)

    @property
    def distraction_free_seconds(self) -> int:
        """无打断专注时长"""
        total = self.actual_duration_seconds
        for d in self.distractions:
            total -= d.duration_seconds
        return max(0, total)

    @property
    def completion_rate(self) -> float:
        """完成度（%）"""
        if self.planned_duration_minutes == 0:
            return 0.0
        ratio = self.actual_duration_minutes / self.planned_duration_minutes
        return min(100.0, ratio * 100)

    @property
    def quality_score(self) -> float:
        """专注质量评分（0-100）"""
        if self.status == SessionStatus.IDLE:
            return 0.0
        score = 100.0
        # 扣分：完成度不足
        score -= max(0, 30 - self.completion_rate) * 0.5
        # 扣分：打断次数
        dc = self.distraction_count
        if dc == 0:
            score += 5
        elif dc <= 2:
            pass
        elif dc <= 5:
            score -= (dc - 2) * 5
        else:
            score -= (dc - 2) * 8 + 5
        # 扣分：打断总时长
        total_distract = sum(d.duration_seconds for d in self.distractions)
        score -= min(20, total_distract / 60 * 2)
        return max(0.0, min(100.0, score))


@dataclass
class DailyFocusReport:
    """每日专注报告"""
    date: date
    total_sessions: int
    completed_sessions: int
    abandoned_sessions: int
    total_focus_minutes: float
    distraction_free_minutes: float
    avg_quality_score: float
    top_distraction_category: Optional[DistractionCategory]
    focus_goal_minutes: float
    goal_achievement_rate: float
    session_details: List[Dict]


class FocusSessionManager:
    """专注会话管理器"""

    DEFAULT_GOAL_MINUTES = 240  # 默认目标：4小时

    def __init__(self, daily_goal_minutes: int = DEFAULT_GOAL_MINUTES):
        self.sessions: List[FocusSession] = []
        self.daily_goal_minutes = daily_goal_minutes

    def create_session(
        self,
        planned_minutes: int,
        task_name: str = "",
        session_id: Optional[str] = None
    ) -> FocusSession:
        """创建并返回一个新的专注会话"""
        sid = session_id or datetime.now().strftime("%Y%m%d%H%M%S%f")
        session = FocusSession(
            id=sid,
            planned_duration_minutes=planned_minutes,
            task_name=task_name
        )
        self.sessions.append(session)
        return session

    def start_session(self, session: FocusSession) -> FocusSession:
        """启动一个会话"""
        session.start_time = datetime.now()
        session.status = SessionStatus.RUNNING
        return session

    def pause_session(self, session: FocusSession) -> Distraction:
        """暂停会话并记录打断开始"""
        if session.status != SessionStatus.RUNNING:
            return None
        session.status = SessionStatus.PAUSED
        return Distraction(timestamp=datetime.now(), category=DistractionCategory.UNKNOWN)

    def resume_session(self, session: FocusSession, distraction: Distraction, category: DistractionCategory, note: str = "") -> FocusSession:
        """恢复会话并完成打断记录"""
        if session.status != SessionStatus.PAUSED or not distraction:
            return session
        now = datetime.now()
        distraction.category = category
        distraction.duration_seconds = int((now - distraction.timestamp).total_seconds())
        distraction.note = note
        session.distractions.append(distraction)
        session.status = SessionStatus.RUNNING
        return session

    def log_distraction(
        self,
        session: FocusSession,
        category: DistractionCategory,
        duration_seconds: int = 0,
        note: str = ""
    ) -> FocusSession:
        """记录一次打断"""
        if session.status != SessionStatus.RUNNING:
            return session
        session.distractions.append(Distraction(
            timestamp=datetime.now(),
            category=category,
            duration_seconds=duration_seconds,
            note=note
        ))
        return session

    def end_session(self, session: FocusSession, abandoned: bool = False) -> FocusSession:
        """结束会话"""
        session.end_time = datetime.now()
        if abandoned:
            session.status = SessionStatus.ABANDONED
        else:
            session.status = SessionStatus.COMPLETED
        return session

    def get_daily_report(self, target_date: Optional[date] = None) -> DailyFocusReport:
        """获取每日专注报告"""
        d = target_date or date.today()
        sessions = [s for s in self.sessions
                    if s.start_time and s.start_time.date() == d]

        completed = [s for s in sessions if s.status == SessionStatus.COMPLETED]
        abandoned = [s for s in sessions if s.status == SessionStatus.ABANDONED]

        total_minutes = sum(s.actual_duration_minutes for s in sessions)
        distraction_free = sum(s.distraction_free_seconds / 60 for s in sessions)
        scores = [s.quality_score for s in completed if s.status == SessionStatus.COMPLETED]
        avg_score = sum(scores) / len(scores) if scores else 0.0

        # 统计打断来源
        cat_counts: Dict[DistractionCategory, int] = {}
        for s in sessions:
            for d_rec in s.distractions:
                cat_counts[d_rec.category] = cat_counts.get(d_rec.category, 0) + 1
        top_cat = max(cat_counts, key=cat_counts.get) if cat_counts else None

        goal_rate = min(100.0, (total_minutes / self.daily_goal_minutes) * 100) if self.daily_goal_minutes else 0.0

        return DailyFocusReport(
            date=d,
            total_sessions=len(sessions),
            completed_sessions=len(completed),
            abandoned_sessions=len(abandoned),
            total_focus_minutes=round(total_minutes, 1),
            distraction_free_minutes=round(distraction_free, 1),
            avg_quality_score=round(avg_score, 1),
            top_distraction_category=top_cat,
            focus_goal_minutes=self.daily_goal_minutes,
            goal_achievement_rate=round(goal_rate, 1),
            session_details=[self._session_to_dict(s) for s in sessions]
        )

    def get_best_focus_hours(self, days_back: int = 7) -> List[Tuple[int, float]]:
        """分析最佳专注时段，返回 (hour, avg_score) 列表"""
        cutoff = datetime.now() - timedelta(days=days_back)
        hour_scores: Dict[int, List[float]] = {}

        for s in self.sessions:
            if not s.start_time or s.start_time < cutoff:
                continue
            if s.status not in (SessionStatus.COMPLETED, SessionStatus.ABANDONED):
                continue
            hour = s.start_time.hour
            hour_scores.setdefault(hour, []).append(s.quality_score)

        result = [(h, sum(scores) / len(scores)) for h, scores in hour_scores.items()]
        result.sort(key=lambda x: x[1], reverse=True)
        return result

    def export_to_csv(self, sessions: Optional[List[FocusSession]] = None) -> str:
        """导出会话数据为CSV字符串"""
        rows = sessions or self.sessions
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow([
            "id", "task_name", "start_time", "end_time", "status",
            "planned_minutes", "actual_minutes", "distraction_count",
            "distraction_free_minutes", "completion_rate", "quality_score", "notes"
        ])
        for s in rows:
            writer.writerow([
                s.id,
                s.task_name,
                s.start_time.isoformat() if s.start_time else "",
                s.end_time.isoformat() if s.end_time else "",
                s.status.value,
                s.planned_duration_minutes,
                round(s.actual_duration_minutes, 1),
                s.distraction_count,
                round(s.distraction_free_seconds / 60, 1),
                round(s.completion_rate, 1),
                round(s.quality_score, 1),
                s.notes
            ])
        return output.getvalue()

    def _session_to_dict(self, s: FocusSession) -> Dict:
        return {
            "id": s.id,
            "task_name": s.task_name,
            "planned_minutes": s.planned_duration_minutes,
            "actual_minutes": round(s.actual_duration_minutes, 1),
            "status": s.status.value,
            "distraction_count": s.distraction_count,
            "quality_score": round(s.quality_score, 1),
        }

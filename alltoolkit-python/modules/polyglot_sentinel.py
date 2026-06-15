"""
polyglot_sentinel.py — 编程语言哨兵 (Polyglot Sentinel)
====================================================================
一个与 language_rotation.json 深度集成的语言学习健康监测模块。

核心理念：学习编程语言就像健身——
不仅要练（轮换），还要监控「哪些肌肉被忽视」。
Polyglot Sentinel 是你的学习健康仪表盘。

核心逻辑：
  1. 读取 language_rotation.json，按 current_index 取当前轮换语言
  2. 读取历史记录，构建每种语言的「最近活跃度」矩阵
  3. 生成学习健康报告：
     - 🚦 健康状态：绿（平衡）/ 黄（偏科）/ 红（严重落后）
     - 📊 雷达图（ASCII）展示各语言活跃度
     - 🔔 哨兵警报：提醒哪些语言长期未练
     - 💡 恢复建议：针对落后语言的学习提示
     - 📈 连续挑战天数 + 连胜统计
  4. 支持多来源历史（codex_log + companion_history + quiz_history 等）
  5. 完成后将 current_index 前移一位并更新 updated_at

语言轮换顺序（8 种核心语言）：
  Rust → Go → Swift → Kotlin → TypeScript → JavaScript → Java → C/C++ → Rust（循环）

Distinct from existing tools:
  - language_tools:        轮换 + 徽章 + 连击记录
  - polyglot_codex:        韬略宝鉴（kata + skeleton + test）
  - polyglot_companion:    学习伴侣（特性 + 练习题）
  - polyglot_quiz:         语言身份猜谜
  - polyglot_snippet_vault: 片段知识库
  - polyglot_ink:          每日墨讯（谚语 + 能量）
  - polyglot_paradigm_weaver: 范式织锦
  - polyglot_cartographer:  语言地图

Polyglot Sentinel 的独特视角：
  不是生成内容，而是「监测学习健康」——
  通过聚合所有轮换工具的历史记录，
  告诉你：你真的均衡地学习了所有语言吗？
  哪个语言被你忽视了？哪个是你最弱的？

作者：AllToolkit 全自动生成
依赖：仅 Python 标准库（json, datetime, pathlib, collections）
====================================================================
"""

import json
import math
import os
import sys
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# ─────────────────────────────────────────────
# 路径配置
# ─────────────────────────────────────────────
_MODULE_DIR = Path(__file__).parent.parent              # alltoolkit-python/
_WORKSPACE_ROOT = _MODULE_DIR.parent                    # workspace/
DEFAULT_LANGUAGE_ROTATION_JSON = str(_WORKSPACE_ROOT / "language_rotation.json")

# 多来源历史日志路径
_LOG_PATHS: Dict[str, str] = {
    "codex":    str(_WORKSPACE_ROOT / "polyglot_codex_log.json"),
    "companion": str(_WORKSPACE_ROOT / "polyglot_companion_history.json"),
    "quiz":     str(_WORKSPACE_ROOT / "polyglot_quiz_history.json"),
    "ink":      str(_WORKSPACE_ROOT / "polyglot_ink_log.json"),
    "snippet":  str(_WORKSPACE_ROOT / "polyglot_snippet_vault_log.json"),
    "map":      str(_WORKSPACE_ROOT / "polyglot_cartographer_log.json"),
}

# 固定的 8 种核心语言
CORE_LANGUAGES: List[str] = [
    "Rust", "Go", "Swift", "Kotlin",
    "TypeScript", "JavaScript", "Java", "C/C++",
]

LANGUAGE_EMOJI: Dict[str, str] = {
    "Rust": "🦀", "Go": "🐹", "Swift": "🦅", "Kotlin": "🟣",
    "TypeScript": "🔷", "JavaScript": "🟡", "Java": "☕", "C/C++": "🔩",
}

LANGUAGE_EXT: Dict[str, str] = {
    "Rust": "rs", "Go": "go", "Swift": "swift", "Kotlin": "kt",
    "TypeScript": "ts", "JavaScript": "js", "Java": "java", "C/C++": "cpp",
}

# 活跃度阈值（天数）
_STALE_THRESHOLD_DAYS = 3      # 超过 3 天未练 → 黄灯
_CRITICAL_THRESHOLD_DAYS = 7   # 超过 7 天未练 → 红灯
_FIRST_THRESHOLD_DAYS = 14     # 超过 14 天 → 严重警告

# 哨兵建议数据库（每种语言的「恢复学习计划」）
SENTINEL_ADVICE: Dict[str, Dict[str, Any]] = {
    "Rust": {
        "weakness": "所有权和生命周期的直觉",
        "tip": "每天花 10 分钟在 Rust Playground 写一个小的借用检查程序",
        "practice": "实现一个自定义 SmartPtr，带 drop 逻辑",
        "resources": ["rustlings", "exercism rust track", "Rust By Example"],
    },
    "Go": {
        "weakness": "goroutine 和 channel 的并发直觉",
        "tip": "用 goroutine 实现一个简单的生产者-消费者流水线",
        "practice": "用 sync.WaitGroup 协调多个并发任务",
        "resources": ["Go Tour", "A Tour of Go", "Go by Example"],
    },
    "Swift": {
        "weakness": "协议扩展和泛型约束",
        "tip": "给 Array 写扩展方法，理解 where 子句的威力",
        "practice": "用 Swift 实现一个简单的链表数据结构",
        "resources": ["Swift Doc", "Hacking with Swift", "Swift by Sundell"],
    },
    "Kotlin": {
        "weakness": "协程和 Flow 的异步直觉",
        "tip": "用 runBlocking 和 launch 写一个并发任务协调器",
        "practice": "用 Kotlin Flow 实现一个事件流处理器",
        "resources": ["Kotlin Docs", "Kotlinlang", "Jetbrains Academy Kotlin"],
    },
    "TypeScript": {
        "weakness": "高级类型工具（条件类型/映射类型）",
        "tip": "手动实现一个 DeepPartial 或Exclude",
        "practice": "用 TypeScript 写一个类型安全的 ORM 迷你实现",
        "resources": ["TypeScript Deep Dive", "advanced-typescript-book", "type-challenges"],
    },
    "JavaScript": {
        "weakness": "事件循环和异步回调深度理解",
        "tip": "不用 async/await，手写一个 Promise.all 实现",
        "practice": "用原生 Promise 实现一个限流并发调度器",
        "resources": ["You Don't Know JS", "javascript.info", "MDN Promise"],
    },
    "Java": {
        "weakness": "JVM 调优和 GC 策略直觉",
        "tip": "用 jstat 和 jmap 观察 GC 日志，理解分代回收",
        "practice": "用 CompletableFuture 实现一个异步任务编排器",
        "resources": ["Effective Java", "Oracle Java Docs", "JVM Performance Tuning"],
    },
    "C/C++": {
        "weakness": "指针操作和手动内存管理",
        "tip": "手写一个简单的内存分配器（malloc 实现）",
        "practice": "用 RAII 模式实现一个线程安全的资源包装器",
        "resources": ["cppreference", "LearnCPP", "Effective C++"],
    },
}


# ─────────────────────────────────────────────
# 内部工具函数
# ─────────────────────────────────────────────

def _read_json(path: str) -> Any:
    """安全读取 JSON，不存在则返回空结构"""
    if not os.path.exists(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return None


def _parse_dt(ts_str: str) -> Optional[datetime]:
    """解析 ISO 时间字符串"""
    for fmt in ("%Y-%m-%dT%H:%M:%S+08:00",
               "%Y-%m-%dT%H:%M:%S%z",
               "%Y-%m-%dT%H:%M:%S"):
        try:
            return datetime.strptime(ts_str.replace("+08:00", ""), fmt)
        except ValueError:
            pass
    return None


def _days_ago(ts_str: str) -> float:
    """计算时间戳距离今天的天数（float）"""
    dt = _parse_dt(ts_str)
    if dt is None:
        return float("inf")
    delta = datetime.now() - dt
    return delta.total_seconds() / 86400.0


# ─────────────────────────────────────────────
# 核心：读取所有历史，构建活跃度矩阵
# ─────────────────────────────────────────────

def _build_activity_matrix() -> Dict[str, List[Dict[str, Any]]]:
    """
    从所有日志源读取历史记录，按语言分组。
    Returns:
        {
          "Rust": [{"ts": "...", "source": "codex", "title": "..."}, ...],
          "Go": [...],
          ...
        }
    """
    matrix: Dict[str, List[Dict[str, Any]]] = {
        lang: [] for lang in CORE_LANGUAGES
    }

    for source_name, log_path in _LOG_PATHS.items():
        data = _read_json(log_path)
        if data is None:
            continue

        # codex_log: {"attempts": [{"language": ..., "generated_at": ..., "title": ...}]}
        if source_name == "codex" and isinstance(data, dict):
            for entry in data.get("attempts", []):
                lang = entry.get("language", "")
                if lang in matrix:
                    matrix[lang].append({
                        "ts": entry.get("generated_at", ""),
                        "source": source_name,
                        "title": entry.get("title", ""),
                    })

        # companion_history: {"entries": [{"language": ..., "timestamp": ...}]}
        elif source_name == "companion" and isinstance(data, dict):
            for entry in data.get("entries", []):
                lang = entry.get("language", "")
                if lang in matrix:
                    matrix[lang].append({
                        "ts": entry.get("timestamp", ""),
                        "source": source_name,
                        "title": entry.get("feature_name", ""),
                    })

        # quiz_history: {"attempts": [{"language": ..., "timestamp": ...}]}
        elif source_name == "quiz" and isinstance(data, dict):
            for entry in data.get("attempts", []):
                lang = entry.get("language", "")
                if lang in matrix:
                    matrix[lang].append({
                        "ts": entry.get("timestamp", ""),
                        "source": source_name,
                        "title": entry.get("quiz_title", ""),
                    })

        # ink_log: {"entries": [{"language": ..., "timestamp": ...}]}
        elif source_name == "ink" and isinstance(data, dict):
            for entry in data.get("entries", []):
                lang = entry.get("language", "")
                if lang in matrix:
                    matrix[lang].append({
                        "ts": entry.get("timestamp", ""),
                        "source": source_name,
                        "title": entry.get("title", ""),
                    })

        # snippet_vault_log: {"entries": [{"language": ..., "retrieved_at": ...}]}
        elif source_name == "snippet" and isinstance(data, dict):
            for entry in data.get("entries", []):
                lang = entry.get("language", "")
                if lang in matrix:
                    matrix[lang].append({
                        "ts": entry.get("retrieved_at", ""),
                        "source": source_name,
                        "title": entry.get("title", ""),
                    })

        # cartographer_log: {"entries": [{"language": ..., "generated_at": ...}]}
        elif source_name == "map" and isinstance(data, dict):
            for entry in data.get("entries", []):
                lang = entry.get("language", "")
                if lang in matrix:
                    matrix[lang].append({
                        "ts": entry.get("generated_at", ""),
                        "source": source_name,
                        "title": entry.get("title", ""),
                    })

    return matrix


def _compute_health_score(matrix: Dict[str, List[Dict[str, Any]]]) -> Dict[str, Any]:
    """
    基于活跃度矩阵计算每种语言的健康分和整体健康状态。

    健康分算法（0~100）：
      - 最近 24h 内有活动 → 100 分
      - 最近 3 天内 → 80 分
      - 最近 7 天内 → 60 分
      - 最近 14 天内 → 40 分
      - 超过 14 天 → 10 分
      - 从未见过 → 0 分
    """
    scores: Dict[str, int] = {}
    last_seen: Dict[str, float] = {}

    for lang in CORE_LANGUAGES:
        entries = matrix.get(lang, [])
        if not entries:
            scores[lang] = 0
            last_seen[lang] = float("inf")
            continue

        # 找最近一次活动
        latest_ts = max((_parse_dt(e["ts"]) or datetime.min for e in entries), default=datetime.min)
        days_ago = (datetime.now() - latest_ts).total_seconds() / 86400.0 if latest_ts != datetime.min else float("inf")
        last_seen[lang] = days_ago

        if days_ago <= 1:
            scores[lang] = 100
        elif days_ago <= 3:
            scores[lang] = 80
        elif days_ago <= 7:
            scores[lang] = 60
        elif days_ago <= 14:
            scores[lang] = 40
        else:
            scores[lang] = 10

    # 整体健康状态
    avg_score = sum(scores.values()) / len(scores) if scores else 0
    if avg_score >= 80:
        overall = "🟢 EXCELLENT"
        status_color = "green"
    elif avg_score >= 60:
        overall = "🟡 HEALTHY"
        status_color = "yellow"
    elif avg_score >= 40:
        overall = "🟠 NEEDS_ATTENTION"
        status_color = "orange"
    else:
        overall = "🔴 CRITICAL"
        status_color = "red"

    return {
        "scores": scores,
        "last_seen_days": last_seen,
        "overall_score": round(avg_score, 1),
        "overall_status": overall,
        "status_color": status_color,
    }


def _build_radar_ascii(scores: Dict[str, int]) -> str:
    """
    用 ASCII 构建一个简化的雷达图（8 语言）。
    使用字符填充来展示活跃度。
    """
    # 将 8 种语言排成环形，每种语言 45 度
    # 计算每个语言的"臂长"（基于分数 0~100）
    langs = CORE_LANGUAGES
    n = len(langs)

    # ASCII 雷达图（用字符密度表示强度）
    # 分 5 圈：最内圈 0，外圈 100
    rings = [
        "                                       ",
        "          🦀 Rust                      ",
        "    🐹 Go              🦅 Swift       ",
        "  🔷 TS    [RADAR]    🟣 Kotlin        ",
        "  🟡 JS              ☕ Java           ",
        "          🔩 C/C++                     ",
        "                                       ",
    ]

    # 更简洁的实现：显示每种语言的活跃度条
    lines = [
        "  ┌──────────────────────────────────────┐",
        "  │       📡 Language Activity Radar     │",
        "  ├──────────────────────────────────────┤",
    ]

    bar_chars = "▇▇▇"
    max_bar = 16  # 最长条长度

    for lang in langs:
        score = scores.get(lang, 0)
        filled = int(score / 100 * max_bar)
        bar = bar_chars[0] * filled + "░" * (max_bar - filled)
        emoji = LANGUAGE_EMOJI.get(lang, "📦")
        lines.append(
            f"  │  {emoji} {lang:<12} {bar} {score:>3} │"
        )

    lines.append("  └──────────────────────────────────────┘")
    return "\n".join(lines)


def _generate_alerts(
    scores: Dict[str, int],
    last_seen: Dict[str, float],
) -> List[Dict[str, Any]]:
    """生成哨兵警报列表"""
    alerts = []
    for lang in CORE_LANGUAGES:
        days = last_seen.get(lang, float("inf"))
        score = scores.get(lang, 0)
        advice = SENTINEL_ADVICE.get(lang, {})

        if score == 0:
            alerts.append({
                "level": "critical",
                "language": lang,
                "emoji": LANGUAGE_EMOJI.get(lang, "📦"),
                "message": f"从未接触过 {lang}！建议立即开始学习。",
                "days_ago": None,
                "advice": advice,
            })
        elif score <= 10:
            alerts.append({
                "level": "critical",
                "language": lang,
                "emoji": LANGUAGE_EMOJI.get(lang, "📦"),
                "message": f"{lang} 已 {int(days)} 天未练习，处于严重落后状态！",
                "days_ago": round(days, 1),
                "advice": advice,
            })
        elif score <= 40:
            alerts.append({
                "level": "warning",
                "language": lang,
                "emoji": LANGUAGE_EMOJI.get(lang, "📦"),
                "message": f"{lang} 已 {int(days)} 天未练习，需要关注。",
                "days_ago": round(days, 1),
                "advice": advice,
            })
        elif score <= 60:
            alerts.append({
                "level": "info",
                "language": lang,
                "emoji": LANGUAGE_EMOJI.get(lang, "📦"),
                "message": f"{lang} 有 {int(days)} 天未练习，保持节奏。",
                "days_ago": round(days, 1),
                "advice": advice,
            })

    return alerts


def _compute_streak(matrix: Dict[str, List[Dict[str, Any]]]) -> Dict[str, Any]:
    """
    计算连续挑战天数和连胜统计。
    通过合并所有来源的记录，按日期去重，计算连续活跃天数。
    """
    # 收集所有活动的日期（去重）
    all_dates: set = set()
    all_entries: List[Dict[str, Any]] = []

    for lang, entries in matrix.items():
        for e in entries:
            dt = _parse_dt(e["ts"])
            if dt:
                date_str = dt.strftime("%Y-%m-%d")
                all_dates.add(date_str)
                all_entries.append({"ts": e["ts"], "lang": lang})

    sorted_dates = sorted(all_dates)
    if not sorted_dates:
        return {
            "total_active_days": 0,
            "current_streak": 0,
            "longest_streak": 0,
            "last_active_date": None,
            "is_active_today": False,
        }

    today = datetime.now().strftime("%Y-%m-%d")
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    last_active = sorted_dates[-1]

    # 当前连续天数（从昨天往前推）
    current_streak = 0
    check_date = datetime.now()
    while True:
        ds = check_date.strftime("%Y-%m-%d")
        if ds in all_dates:
            current_streak += 1
            check_date -= timedelta(days=1)
        elif ds == today and yesterday in all_dates:
            # 今天还没活动但昨天有，继续往前推
            check_date -= timedelta(days=1)
        else:
            break
        if current_streak > 1000:  # 防止死循环
            break

    # 最长连续天数
    longest_streak = 0
    run = 0
    prev_date: Optional[datetime] = None
    for ds in sorted_dates:
        dt = datetime.strptime(ds, "%Y-%m-%d")
        if prev_date is None or (dt - prev_date).days == 1:
            run += 1
        else:
            run = 1
        longest_streak = max(longest_streak, run)
        prev_date = dt

    return {
        "total_active_days": len(sorted_dates),
        "current_streak": current_streak,
        "longest_streak": longest_streak,
        "last_active_date": last_active,
        "is_active_today": today in all_dates,
    }


# ─────────────────────────────────────────────
# 核心 API
# ─────────────────────────────────────────────

def get_sentinel_report(
    json_path: str = DEFAULT_LANGUAGE_ROTATION_JSON,
) -> Dict[str, Any]:
    """
    获取完整的语言学习健康报告。

    流程：
      1. 读取 language_rotation.json，取 current_index 所指语言
      2. 从所有日志源构建活跃度矩阵
      3. 计算健康分和整体状态
      4. 生成警报和建议
      5. 将 current_index 前移一位并更新 updated_at
      6. 返回完整报告

    Returns:
        {
            "current_language": str,
            "overall_score": float,
            "overall_status": str,
            "status_color": str,
            "scores": {lang: 0~100},
            "last_seen_days": {lang: float},
            "radar_chart": str,
            "alerts": [...],
            "streak": {...},
            "total_entries": int,
            "language_rankings": [(lang, score), ...],
        }
    """
    # 读取当前轮换语言
    rot_data = _read_json(json_path) or {}
    languages = rot_data.get("languages", CORE_LANGUAGES)
    idx = rot_data.get("current_index", 0) % len(languages)
    current_language = languages[idx]

    # 构建活跃度矩阵
    matrix = _build_activity_matrix()

    # 计算健康分
    health = _compute_health_score(matrix)

    # 雷达图
    radar = _build_radar_ascii(health["scores"])

    # 警报
    alerts = _generate_alerts(health["scores"], health["last_seen_days"])

    # 连胜统计
    streak = _compute_streak(matrix)

    # 排名（按分数降序）
    rankings = sorted(
        health["scores"].items(),
        key=lambda x: x[1],
        reverse=True,
    )

    # 总记录数
    total_entries = sum(len(entries) for entries in matrix.values())

    # 更新 language_rotation.json（index 前移）
    next_idx = (idx + 1) % len(languages)
    rot_data["current_index"] = next_idx
    rot_data["last_language"] = current_language
    rot_data["updated_at"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00")

    # 安全写入（先写临时文件再 rename，减少损坏风险）
    _tmp = json_path + ".sentinel_tmp"
    try:
        with open(_tmp, "w", encoding="utf-8") as f:
            json.dump(rot_data, f, ensure_ascii=False, indent=2)
        os.replace(_tmp, json_path)
    except IOError:
        pass  # 忽略写入错误（只读环境等）

    return {
        "current_language": current_language,
        "emoji": LANGUAGE_EMOJI.get(current_language, "📦"),
        "overall_score": health["overall_score"],
        "overall_status": health["overall_status"],
        "status_color": health["status_color"],
        "scores": health["scores"],
        "last_seen_days": {k: round(v, 1) for k, v in health["last_seen_days"].items()},
        "radar_chart": radar,
        "alerts": alerts,
        "streak": streak,
        "total_entries": total_entries,
        "language_rankings": rankings,
        "next_language": languages[next_idx],
    }


def get_sentinel_preview(
    json_path: str = DEFAULT_LANGUAGE_ROTATION_JSON,
) -> Dict[str, Any]:
    """
    查询当前健康状态（不推进索引）。
    """
    rot_data = _read_json(json_path) or {}
    languages = rot_data.get("languages", CORE_LANGUAGES)
    idx = rot_data.get("current_index", 0) % len(languages)
    current_language = languages[idx]

    matrix = _build_activity_matrix()
    health = _compute_health_score(matrix)
    streak = _compute_streak(matrix)

    return {
        "current_language": current_language,
        "emoji": LANGUAGE_EMOJI.get(current_language, "📦"),
        "overall_score": health["overall_score"],
        "overall_status": health["overall_status"],
        "scores": health["scores"],
        "streak": streak,
        "next_language": languages[(idx + 1) % len(languages)],
    }


def format_sentinel_console(report: Dict[str, Any]) -> str:
    """
    将报告格式化为 ASCII 控制台输出。
    """
    lines = [
        "  ╔══════════════════════════════════════════════════════════╗",
        "  ║  🚨 Polyglot Sentinel — 语言学习健康仪表盘              ║",
        "  ╠══════════════════════════════════════════════════════════╣",
        f"  ║  当前语言：{report['emoji']} {report['current_language']:<10}  "
        f"整体健康：{report['overall_status']:<18} 得分：{report['overall_score']:>5}  ║",
        "  ╠══════════════════════════════════════════════════════════╣",
    ]

    # 雷达图
    for radar_line in report["radar_chart"].split("\n"):
        lines.append(f"  ║  {radar_line:<57}║")

    lines += [
        "  ╠══════════════════════════════════════════════════════════╣",
        "  ║  📊 语言活跃度排名                                     ║",
    ]
    for rank, (lang, score) in enumerate(report["language_rankings"], 1):
        emoji = LANGUAGE_EMOJI.get(lang, "📦")
        bar_len = int(score / 100 * 12)
        bar = "█" * bar_len + "░" * (12 - bar_len)
        lines.append(
            f"  ║  {rank:>2}. {emoji} {lang:<10} {bar} {score:>3}  ║"
        )

    # 警报
    if report["alerts"]:
        lines += [
            "  ╠══════════════════════════════════════════════════════════╣",
            "  ║  🔔 哨兵警报                                             ║",
        ]
        for alert in report["alerts"][:5]:  # 最多显示 5 条
            level_icon = {
                "critical": "🔴",
                "warning": "🟠",
                "info": "🟡",
            }.get(alert["level"], "⚪")
            msg = alert["message"][:48]
            lines.append(f"  ║  {level_icon} {msg:<54}║")

    # 连胜统计
    streak = report["streak"]
    lines += [
        "  ╠══════════════════════════════════════════════════════════╣",
        "  ║  📈 学习连续性                                           ║",
        f"  ║  🔥 当前连续 {streak['current_streak']:>3} 天  "
        f"|  历史最长 {streak['longest_streak']:>3} 天  "
        f"|  总活跃天数 {streak['total_active_days']:>3}         ║",
        f"  ║  📅 最后活跃：{streak['last_active_date'] or 'N/A':<36}    ║",
        "  ╠══════════════════════════════════════════════════════════╣",
        f"  ║  📝 总记录数：{report['total_entries']:<48}║",
        f"  ║  ⏭️  下个语言：{report['next_language']:<46}║",
        "  ╚══════════════════════════════════════════════════════════╝",
    ]

    return "\n".join(lines)


def format_sentinel_markdown(report: Dict[str, Any]) -> str:
    """
    将报告格式化为 Markdown 输出。
    """
    lines = [
        f"## 🚨 Polyglot Sentinel — 语言学习健康报告",
        "",
        f"**当前语言**：{report['emoji']} {report['current_language']}",
        f"**整体健康**：{report['overall_status']}  |  **得分**：{report['overall_score']}/100",
        "",
        "### 📊 语言活跃度",
        "",
        "| 语言 | 活跃度 | 得分 |",
        "|------|--------|------|",
    ]

    for lang, score in report["language_rankings"]:
        emoji = LANGUAGE_EMOJI.get(lang, "📦")
        bar_len = int(score / 100 * 10)
        bar = "▇" * bar_len + "░" * (10 - bar_len)
        lines.append(f"| {emoji} {lang} | {bar} | {score} |")

    if report["alerts"]:
        lines += [
            "",
            "### 🔔 哨兵警报",
            "",
        ]
        for alert in report["alerts"][:5]:
            level_icon = {
                "critical": "🔴 CRITICAL",
                "warning": "🟠 WARNING",
                "info": "🟡 INFO",
            }.get(alert["level"], "⚪")
            lines.append(f"- {level_icon}: **{alert['language']}** — {alert['message']}")

            advice = alert.get("advice", {})
            if advice:
                lines.append(f"  - 💡 建议：{advice.get('tip', 'N/A')}")

    streak = report["streak"]
    lines += [
        "",
        "### 📈 学习连续性",
        "",
        f"- 🔥 当前连续：**{streak['current_streak']} 天**",
        f"- 🏆 历史最长：{streak['longest_streak']} 天",
        f"- 📅 总活跃天数：{streak['total_active_days']} 天",
        f"- 📝 总记录数：{report['total_entries']}",
        "",
        f"⏭️ **下一个语言**：{report['next_language']}",
    ]

    return "\n".join(lines)


# ─────────────────────────────────────────────
# CLI 入口
# ─────────────────────────────────────────────

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Polyglot Sentinel — 语言学习健康监测")
    sub = parser.add_subparsers(dest="cmd")

    sub.add_parser("report", help="生成完整健康报告（推进轮换）")
    sub.add_parser("preview", help="预览健康状态（不推进轮换）")
    sub.add_parser("alerts", help="仅显示警报")
    sub.add_parser("rankings", help="显示语言排名")

    args = parser.parse_args()

    if args.cmd == "report":
        result = get_sentinel_report()
        print(format_sentinel_console(result))
    elif args.cmd == "preview":
        result = get_sentinel_preview()
        emoji = LANGUAGE_EMOJI.get(result["current_language"], "📦")
        print(f"{emoji} {result['current_language']} | 健康：{result['overall_status']} ({result['overall_score']}/100)")
        for lang, score in result["scores"].items():
            em = LANGUAGE_EMOJI.get(lang, "📦")
            print(f"  {em} {lang}: {score}")
    elif args.cmd == "alerts":
        result = get_sentinel_report()
        for alert in result["alerts"]:
            print(f"[{alert['level'].upper()}] {alert['emoji']} {alert['message']}")
    elif args.cmd == "rankings":
        result = get_sentinel_report()
        for rank, (lang, score) in enumerate(result["language_rankings"], 1):
            print(f"{rank:>2}. {LANGUAGE_EMOJI.get(lang,'📦')} {lang}: {score}")
    else:
        parser.print_help()
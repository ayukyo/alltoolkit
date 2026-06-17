"""
polyglot_pulse.py — 编程语言脉搏监测仪 (Polyglot Pulse)
====================================================================
创意：每种语言都有"脉搏"——它记录了该语言最近被轮换的活跃程度。
本工具追踪所有历史轮换日志，实时计算每种语言的：
  - 🔴 脉搏率（高频/低频）
  - 🔥 余温（最近一次轮换距今多久）
  - 📈 活跃曲线（ASCII 波形展示）
  - 🎯 今日推荐（基于脉搏，推荐此刻最应该练习的语言）
  - ⏰ 冷却提醒（太久没练的语言发出警告）

与 language_rotation.json 深度集成：
  1. 读取 language_rotation.json 和各模块历史日志
  2. 聚合计算所有语言的脉搏数据
  3. 生成脉搏监测报告 + 今日推荐
  4. 生成 ASCII 心电图 + 语言活跃度排行榜
  5. 支持轮换：推进 current_index

语言轮换顺序（8 种核心语言）：
  Rust → Go → Swift → Kotlin → TypeScript → JavaScript → Java → C/C++ → Rust（循环）

Distinct from existing modules:
  - polyglot_sentinel:   学习健康仪表盘（整体平衡性监测）
  - polyglot_resonator:  时间-语言共振分析（此刻适合什么语言）
  - polyglot_pulse:      轮换历史脉搏追踪（每种语言的活跃热度）

Polyglot Pulse 的独特视角：
  不是教你写代码，不是范式对照，而是——
  把语言当作有"生命体征"的存在来追踪。
  Rust 最近被练了 3 次 → 脉搏强劲 🔥
  C/C++ 已经 5 天没出现 → 脉搏微弱 😴
  凌晨做 Rust 题目效率最高 — 这个信号被 pulse 记录下来

作者：AllToolkit 全自动生成
依赖：仅 Python 标准库（json, datetime, pathlib, collections）
====================================================================
"""

import json
import math
import os
import random
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

# 各模块历史日志路径
_LOG_PATHS: Dict[str, str] = {
    "codex":     str(_WORKSPACE_ROOT / "polyglot_codex_log.json"),
    "companion": str(_WORKSPACE_ROOT / "polyglot_companion_history.json"),
    "quiz":      str(_WORKSPACE_ROOT / "polyglot_quiz_history.json"),
    "ink":       str(_WORKSPACE_ROOT / "polyglot_ink_log.json"),
    "snippet":   str(_WORKSPACE_ROOT / "polyglot_snippet_vault_log.json"),
    "map":       str(_WORKSPACE_ROOT / "polyglot_cartographer_log.json"),
    "kata":      str(_WORKSPACE_ROOT / "polyglot_kata_log.json"),
}

# 固定 8 种核心语言
CORE_LANGUAGES: List[str] = [
    "Rust", "Go", "Swift", "Kotlin",
    "TypeScript", "JavaScript", "Java", "C/C++",
]

LANGUAGE_EMOJI: Dict[str, str] = {
    "Rust": "🦀", "Go": "🐹", "Swift": "🦅", "Kotlin": "🟣",
    "TypeScript": "🔷", "JavaScript": "🟡", "Java": "☕", "C/C++": "🔩",
}

# 脉搏温度区间（小时）
_PULSE_ZONES: Dict[str, Tuple[float, str]] = {
    # (max_hours_ago, label)
    "blazing":   (2,   "🔥 炽热"),
    "hot":       (6,   "⚡ 活跃"),
    "warm":      (24,  "🌡️ 温热"),
    "cool":      (72,  "🧊 冷却"),
    "cold":      (168, "❄️ 寒冷"),
    "frozen":    (999, "💀 冻结"),
}


# ─────────────────────────────────────────────
# 辅助函数
# ─────────────────────────────────────────────

def _parse_dt(s: Optional[str]) -> Optional[datetime]:
    """解析 +08:00 北京时间字符串。"""
    if not s:
        return None
    s = s.replace("+08:00", "").strip()
    for fmt in ("%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M:%S.%f"):
        try:
            return datetime.strptime(s, fmt)
        except ValueError:
            pass
    return None


def _hours_ago(dt: datetime, now: datetime) -> float:
    """计算 dt 距 now 多少小时（浮点数）。"""
    delta = now - dt
    return delta.total_seconds() / 3600.0


def _read_json(path: str) -> Optional[Dict[str, Any]]:
    if not os.path.exists(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return None


def _write_json(path: str, data: Dict[str, Any]) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def _pulse_zone(hours: float) -> str:
    """根据小时数返回脉搏区间标签。"""
    for zone, (max_hours, label) in _PULSE_ZONES.items():
        if hours <= max_hours:
            return label
    return "💀 冻结"


def _pulse_rate(hours: float) -> float:
    """
    将小时数映射为 0.0~1.0 的脉搏率。
    0小时前 = 1.0（最强），越久越小。
    使用指数衰减：rate = exp(-hours/24)
    """
    return math.exp(-hours / 24.0)


def _build_ecg_line(rate: float, width: int = 50) -> str:
    """
    根据脉搏率生成一行 ASCII 心电图。

    字符映射（row 0=顶 → 6=底）：
      0: ╭  (R峰顶)
      1: ╮
      2: │
      3: ─  (baseline, 当 v=0)
      4: │
      5: ╰
      6: ╯  (最低)
      7: ░  (心电图平线/无信号时的填充)
    """
    if rate <= 0.0:
        return "░" * width

    chars = []
    for i in range(width):
        x = i / width  # 0..1
        # 模拟心电图：PQRST 波形
        if rate > 0.7:
            # 完整心电图
            if 0.10 <= x <= 0.15:
                v = -0.2 * math.sin((x - 0.10) / 0.05 * math.pi)  # P波（向下）
            elif 0.25 <= x <= 0.27:
                v = -0.25  # Q（向下）
            elif 0.27 <= x <= 0.33:
                # R 尖峰（根据 rate 调整高度，越高越尖）
                t = (x - 0.27) / 0.06
                v = 1.0 * rate - abs(t - 0.5) * 2.0  # 尖峰
            elif 0.33 <= x <= 0.35:
                v = -0.2  # S（向下）
            elif 0.45 <= x <= 0.55:
                v = 0.15 * math.sin((x - 0.45) / 0.10 * math.pi)  # T波（向上）
            else:
                v = 0.0
        elif rate > 0.3:
            # 弱心电图：只剩 R 峰
            t = abs(x - 0.30) / 0.10
            v = max(0.0, rate * (1.0 - t))
        else:
            # 微弱心电图：微弱 R 峰
            t = abs(x - 0.30) / 0.15
            v = max(0.0, rate * 0.6 * (1.0 - t))

        # 映射：v=-1.0 → row=0（顶=╭），v=0 → row=7（底=░），v=1.0 → row=0（顶=╭）
        # baseline 在 row=7
        baseline_row = 7
        row = int(round(baseline_row - v * (baseline_row - 0)))
        row = max(0, min(7, row))
        chars.append("╭╮│─││╰╯░"[row])
    return "".join(chars)


def _build_activity_bar(rate: float, width: int = 20) -> str:
    """将脉搏率转换为 ASCII 进度条。"""
    filled = int(round(rate * width))
    if rate > 0.75:
        return "█" * filled + "░" * (width - filled)
    elif rate > 0.4:
        return "▓" * filled + "▒" * (width - filled)
    elif rate > 0.15:
        return "▒" * filled + "░" * (width - filled)
    else:
        return "░" * width


# ─────────────────────────────────────────────
# 核心：聚合所有历史日志，构建脉搏数据
# ─────────────────────────────────────────────

def _collect_all_entries() -> Dict[str, List[datetime]]:
    """
    从所有日志文件中收集每种语言的所有活跃时间点。
    返回 {language: [datetime1, datetime2, ...]}
    """
    entries: Dict[str, List[datetime]] = defaultdict(list)
    now = datetime.now()

    for source, path in _LOG_PATHS.items():
        data = _read_json(path)
        if not data:
            continue

        # 不同的日志格式
        if source == "codex":
            attempts = data.get("attempts", [])
            for a in attempts:
                lang = a.get("language", "")
                dt_str = a.get("generated_at", "") or a.get("timestamp", "")
                dt = _parse_dt(dt_str)
                if dt and lang in CORE_LANGUAGES:
                    entries[lang].append(dt)

        elif source == "companion":
            sessions = data.get("sessions", [])
            for s in sessions:
                lang = s.get("language", "")
                dt_str = s.get("timestamp", "") or s.get("generated_at", "")
                dt = _parse_dt(dt_str)
                if dt and lang in CORE_LANGUAGES:
                    entries[lang].append(dt)

        elif source == "quiz":
            history = data.get("history", []) if isinstance(data, dict) else data if isinstance(data, list) else []
            if isinstance(data, dict) and "history" in data:
                history = data["history"]
            elif isinstance(data, dict) and "attempts" in data:
                history = data["attempts"]
            else:
                history = []
            for h in history:
                lang = h.get("language", "")
                dt_str = h.get("timestamp", "") or h.get("generated_at", "")
                dt = _parse_dt(dt_str)
                if dt and lang in CORE_LANGUAGES:
                    entries[lang].append(dt)

        elif source in ("ink", "snippet", "map", "kata"):
            # 统一处理：找 attempts 或 history
            if isinstance(data, dict):
                for key in ("attempts", "history", "entries", "sessions"):
                    items = data.get(key, [])
                    if isinstance(items, list):
                        for item in items:
                            lang = item.get("language", "")
                            dt_str = item.get("timestamp", "") or item.get("generated_at", "")
                            dt = _parse_dt(dt_str)
                            if dt and lang in CORE_LANGUAGES:
                                entries[lang].append(dt)
                        break

    # 对每种语言的记录按时间排序
    for lang in entries:
        entries[lang] = sorted(set(entries[lang]))

    return entries


def _compute_pulse_data(
    entries: Dict[str, List[datetime]],
    now: datetime,
) -> Dict[str, Dict[str, Any]]:
    """
    根据 entries 计算每种语言的脉搏数据。
    """
    pulse_data: Dict[str, Dict[str, Any]] = {}

    for lang in CORE_LANGUAGES:
        times = entries.get(lang, [])
        if not times:
            # 从未练习过
            pulse_data[lang] = {
                "language": lang,
                "emoji": LANGUAGE_EMOJI.get(lang, "📦"),
                "pulse_rate": 0.0,
                "pulse_zone": "💀 冻结",
                "hours_since_last": None,
                "total_sessions": 0,
                "last_practiced": None,
                "activity_bar": _build_activity_bar(0.0),
                "ecg_line": _build_ecg_line(0.0),
                "daily_intensity": [0.0] * 24,
                "streak_days": 0,
                "recommendation_score": 0.0,
            }
            continue

        # 最近一次练习
        last = max(times)
        hours = _hours_ago(last, now)
        rate = _pulse_rate(hours)
        zone = _pulse_zone(hours)

        # 活跃天数（去重日期）
        practice_days = set(t.replace(hour=0, minute=0, second=0, microsecond=0) for t in times)
        streak = len(practice_days)

        # 每日活跃强度（统计每小时练习次数，归一化）
        hourly = [0] * 24
        for t in times:
            hourly[t.hour] += 1
        max_count = max(hourly) if max(hourly) > 0 else 1
        daily_intensity = [c / max_count for c in hourly]

        # 推荐得分：结合脉搏率 + 今日小时匹配度
        current_hour_score = hourly[now.hour] / max_count if max_count > 0 else 0.0
        rec_score = rate * 0.7 + current_hour_score * 0.3

        pulse_data[lang] = {
            "language": lang,
            "emoji": LANGUAGE_EMOJI.get(lang, "📦"),
            "pulse_rate": rate,
            "pulse_zone": zone,
            "hours_since_last": round(hours, 1),
            "total_sessions": len(times),
            "last_practiced": last.strftime("%Y-%m-%d %H:%M"),
            "activity_bar": _build_activity_bar(rate),
            "ecg_line": _build_ecg_line(rate),
            "daily_intensity": daily_intensity,
            "streak_days": streak,
            "recommendation_score": rec_score,
        }

    return pulse_data


def _get_pulse_rankings(pulse_data: Dict[str, Dict[str, Any]]) -> List[Tuple[str, float]]:
    """按脉搏率排序。"""
    return sorted(
        [(lang, d["pulse_rate"]) for lang, d in pulse_data.items()],
        key=lambda x: x[1],
        reverse=True,
    )


def _format_hourly_chart(daily_intensity: List[float], width: int = 24) -> str:
    """将 24 小时活跃强度绘制为 ASCII 柱状图。"""
    if not daily_intensity or len(daily_intensity) != 24:
        return "░" * 24

    lines = []
    # 找最高点作为参考
    max_val = max(daily_intensity) if max(daily_intensity) > 0 else 1.0
    rows = 4
    for row in range(rows, -1, -1):
        threshold = (row / rows) * max_val
        line = ""
        for v in daily_intensity:
            if v >= threshold:
                line += "█"
            else:
                line += "░"
        lines.append(line)
    return "\n".join(lines)


# ─────────────────────────────────────────────
# 主 API
# ─────────────────────────────────────────────

def get_pulse_report(
    json_path: str = DEFAULT_LANGUAGE_ROTATION_JSON,
    now: Optional[datetime] = None,
) -> Dict[str, Any]:
    """
    生成语言脉搏监测报告。

    步骤：
      1. 读取 language_rotation.json（获取 current_index）
      2. 聚合所有模块历史日志，构建脉搏数据
      3. 计算推荐语言（脉搏 + 时间匹配度）
      4. 推进 current_index

    Returns:
        {
            "current_language": str,
            "next_language": str,
            "pulse_data": {lang: {...}},
            "rankings": [(lang, rate), ...],
            "recommended_language": str,
            "recommended_reason": str,
            "json_updated": bool,
            "timestamp": str,
        }
    """
    if now is None:
        now = datetime.now()

    # 读取 language_rotation.json
    data = _read_json(json_path)
    if data is None:
        raise FileNotFoundError(f"Cannot find {json_path}")

    languages = data["languages"]
    idx = data.get("current_index", 0) % len(languages)
    current = languages[idx]
    next_idx = (idx + 1) % len(languages)
    next_language = languages[next_idx]

    # 收集历史，构脉搏数据
    all_entries = _collect_all_entries()
    pulse_data = _compute_pulse_data(all_entries, now)

    # 计算推荐语言（脉搏率 + 时间匹配度）
    rankings = _get_pulse_rankings(pulse_data)
    top_lang, top_rate = rankings[0]

    # 推荐逻辑：
    # - 如果最热的语言最近 2 小时内练过 → 推荐次热语言（避免重复）
    # - 否则推荐最热的
    if top_rate > 0.8 and pulse_data[top_lang]["hours_since_last"] is not None and pulse_data[top_lang]["hours_since_last"] < 2:
        # 刚练过，推荐次热
        if len(rankings) > 1:
            recommended_lang = rankings[1][0]
            recommended_reason = f"{top_lang} 刚刚练过（余温尚在），推荐换个口味 → {recommended_lang}"
        else:
            recommended_lang = top_lang
            recommended_reason = f"{top_lang} 是唯一选择，继续挑战！"
    elif top_rate < 0.1:
        # 所有语言都冷了，推荐最冷的反面——最近最少练的语言
        cold_lang = min(pulse_data.items(), key=lambda x: x[1]["total_sessions"])[0]
        recommended_lang = cold_lang
        recommended_reason = f"所有语言都在冷却，推荐重新激活 {cold_lang}！"
    else:
        recommended_lang = top_lang
        recommended_reason = f"{top_lang} 当前脉搏最旺，是今日推荐的练习语言"

    # 更新 language_rotation.json
    data["current_index"] = next_idx
    data["last_language"] = current
    data["updated_at"] = now.strftime("%Y-%m-%dT%H:%M:%S+08:00")
    _write_json(json_path, data)

    return {
        "current_language": current,
        "next_language": next_language,
        "pulse_data": pulse_data,
        "rankings": rankings,
        "recommended_language": recommended_lang,
        "recommended_reason": recommended_reason,
        "json_updated": True,
        "timestamp": now.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
    }


def get_pulse_preview(
    json_path: str = DEFAULT_LANGUAGE_ROTATION_JSON,
    now: Optional[datetime] = None,
) -> Dict[str, Any]:
    """
    查询脉搏数据（不推进索引，不写 JSON）。
    """
    if now is None:
        now = datetime.now()

    data = _read_json(json_path)
    if data is None:
        raise FileNotFoundError(f"Cannot find {json_path}")

    languages = data["languages"]
    idx = data.get("current_index", 0) % len(languages)
    current = languages[idx]

    all_entries = _collect_all_entries()
    pulse_data = _compute_pulse_data(all_entries, now)
    rankings = _get_pulse_rankings(pulse_data)

    return {
        "current_language": current,
        "pulse_data": pulse_data,
        "rankings": rankings,
        "timestamp": now.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
    }


def format_pulse_console(report: Dict[str, Any]) -> str:
    """将脉搏报告格式化为友好的控制台输出。"""
    pulse_data = report["pulse_data"]
    rankings = report["rankings"]

    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    lines = [
        f"  ╔══════════════════════════════════════════════════════════╗",
        f"  ║  💓 Polyglot Pulse — 语言脉搏监测仪                      ║",
        f"  ╠══════════════════════════════════════════════════════════╣",
        f"  ║  时刻：{now}（北京时间）                        ║",
        f"  ╠══════════════════════════════════════════════════════════╣",
    ]

    # 排行榜
    lines.append(f"  ║  🏆 脉搏排行榜                                       ║")
    for rank, (lang, rate) in enumerate(rankings, 1):
        pd = pulse_data[lang]
        zone = pd["pulse_zone"]
        bar = pd["activity_bar"]
        lines.append(
            f"  ║  {rank}. {pd['emoji']} {lang:<10} {zone:<8} {bar}    {rate:.2f} ║"
        )

    lines += [
        f"  ╠══════════════════════════════════════════════════════════╣",
        f"  ║  🎯 今日推荐：{report['recommended_language']:<26}   ║",
        f"  ║     {report['recommended_reason']:<44}   ║",
        f"  ╠══════════════════════════════════════════════════════════╣",
        f"  ║  📊 每种语言的实时脉搏                                  ║",
    ]

    for lang, pd in pulse_data.items():
        hours_str = f"{pd['hours_since_last']}小时前" if pd['hours_since_last'] is not None else "从未"
        sessions_str = f"{pd['total_sessions']}次"
        streak_str = f"连续{pd['streak_days']}天" if pd['streak_days'] > 0 else "无连续"
        lines.append(
            f"  ║  {pd['emoji']} {lang:<10} {pd['pulse_zone']:<8} "
            f"距今:{hours_str:<10} 练习:{sessions_str:<6} {streak_str:<10} ║"
        )
        lines.append(f"  ║    心电图: {pd['ecg_line']} ║")

    lines += [
        f"  ╠══════════════════════════════════════════════════════════╣",
        f"  ║  ⏭️  轮换: {report['current_language']} → {report['next_language']}                         ║",
        f"  ╚══════════════════════════════════════════════════════════╝",
    ]

    return "\n".join(lines)


def format_pulse_markdown(report: Dict[str, Any]) -> str:
    """将脉搏报告格式化为 Markdown。"""
    pulse_data = report["pulse_data"]
    rankings = report["rankings"]

    lines = [
        f"# 💓 语言脉搏监测报告",
        "",
        f"**时刻**：{report['timestamp']}（北京时间）",
        "",
        f"## 🏆 脉搏排行榜",
        "",
        f"| 排名 | 语言 | 脉搏状态 | 活跃条 | 脉搏率 |",
        f"|------|------|----------|--------|--------|",
    ]

    for rank, (lang, rate) in enumerate(rankings, 1):
        pd = pulse_data[lang]
        lines.append(
            f"| {rank} | {pd['emoji']} {lang} | {pd['pulse_zone']} | "
            f"{pd['activity_bar']} | {rate:.3f} |"
        )

    lines += [
        "",
        f"## 🎯 今日推荐",
        "",
        f"> **{report['recommended_language']}** — {report['recommended_reason']}",
        "",
        f"## 📊 实时脉搏详情",
        "",
        f"| 语言 | 状态 | 距今 | 练习次数 | 连续天数 | 心电图 |",
        f"|------|------|------|----------|----------|--------|",
    ]

    for lang, pd in pulse_data.items():
        hours_str = f"{pd['hours_since_last']}h" if pd['hours_since_last'] is not None else "从未"
        lines.append(
            f"| {pd['emoji']} {lang} | {pd['pulse_zone']} | "
            f"{hours_str} | {pd['total_sessions']} | "
            f"{pd['streak_days']} | `{pd['ecg_line']}` |"
        )

    lines.append("")
    lines.append(f"---")
    lines.append(f"⏭️ 轮换：**{report['current_language']}** → **{report['next_language']}**")

    return "\n".join(lines)


def get_language_pulse(
    language: str,
    json_path: str = DEFAULT_LANGUAGE_ROTATION_JSON,
    now: Optional[datetime] = None,
) -> Dict[str, Any]:
    """
    查询指定语言的详细脉搏数据（不推进索引）。
    """
    if now is None:
        now = datetime.now()

    all_entries = _collect_all_entries()
    pulse_data = _compute_pulse_data(all_entries, now)

    if language not in pulse_data:
        raise ValueError(f"Language '{language}' not in core languages")

    pd = pulse_data[language]
    hourly_chart = _format_hourly_chart(pd["daily_intensity"])

    return {
        "language": language,
        "emoji": pd["emoji"],
        "pulse_rate": pd["pulse_rate"],
        "pulse_zone": pd["pulse_zone"],
        "hours_since_last": pd["hours_since_last"],
        "total_sessions": pd["total_sessions"],
        "last_practiced": pd["last_practiced"],
        "activity_bar": pd["activity_bar"],
        "ecg_line": pd["ecg_line"],
        "daily_intensity_chart": hourly_chart,
        "streak_days": pd["streak_days"],
        "recommendation_score": pd["recommendation_score"],
        "timestamp": now.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
    }


# ─────────────────────────────────────────────
# CLI 入口
# ─────────────────────────────────────────────

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Polyglot Pulse — 语言脉搏监测仪")
    sub = parser.add_subparsers(dest="cmd")

    sub.add_parser("report", help="生成脉搏报告（推进轮换）")
    sub.add_parser("preview", help="预览脉搏数据（不推进）")
    sub.add_parser("rankings", help="查看脉搏排行榜")

    lp = sub.add_parser("pulse", help="查看指定语言的详细脉搏")
    lp.add_argument("language", help="语言名称")

    args = parser.parse_args()

    if args.cmd == "report":
        result = get_pulse_report()
        print(format_pulse_console(result))
    elif args.cmd == "preview":
        result = get_pulse_preview()
        pulse_data = result["pulse_data"]
        print(f"\n💓 语言脉搏预览（不推进轮换）\n")
        for rank, (lang, rate) in enumerate(result["rankings"], 1):
            pd = pulse_data[lang]
            hours_str = f"{pd['hours_since_last']}h" if pd['hours_since_last'] else "从未"
            print(f"  {rank}. {pd['emoji']} {lang:<12} {pd['pulse_zone']:<8} 距今:{hours_str}")
    elif args.cmd == "rankings":
        result = get_pulse_preview()
        print(f"\n🏆 脉搏排行榜\n")
        for rank, (lang, rate) in enumerate(result["rankings"], 1):
            pd = result["pulse_data"][lang]
            print(f"  {rank}. {pd['emoji']} {lang:<12} {pd['activity_bar']}  {rate:.3f}")
    elif args.cmd == "pulse":
        result = get_language_pulse(args.language)
        print(f"\n💓 {result['emoji']} {result['language']} 脉搏详情\n")
        print(f"  脉搏状态：{result['pulse_zone']}")
        print(f"  脉搏率：{result['pulse_rate']:.3f}")
        print(f"  距今：{result['hours_since_last']}h" if result['hours_since_last'] else "  距今：从未练习")
        print(f"  练习次数：{result['total_sessions']}")
        print(f"  连续天数：{result['streak_days']}")
        print(f"  活跃条：{result['activity_bar']}")
        print(f"  心电图：{result['ecg_line']}")
        print(f"\n  📊 24小时活跃分布：")
        print(result['daily_intensity_chart'])
    else:
        parser.print_help()

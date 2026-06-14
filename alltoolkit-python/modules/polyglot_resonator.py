"""
polyglot_resonator.py — 编程语言共振分析仪 (Polyglot Resonator)
====================================================================
每次轮换语言时，生成一份"语言共振报告"——
将每种语言映射为特定频率，结合当前时间（小时/星期/月份）
计算"共振强度"，并用 ASCII 波形图可视化。

核心创意：语言不只是工具，它是「频率」——
每种语言有其独特的思维节奏：Rust 的低频稳重、JS 的高频敏捷...
共振越强，学习效果越好；本工具帮你找到当前时刻最共振的语言。

与 language_rotation.json 深度集成：
  1. 读取 current_index，取出当前轮换语言
  2. 结合当前时间计算共振参数
  3. 生成 ASCII 波形图 + 共振分析报告
  4. 将 current_index 前移一位，更新 updated_at

语言轮换顺序（8 种核心语言）：
  Rust → Go → Swift → Kotlin → TypeScript → JavaScript → Java → C/C++ → Rust（循环）

Distinct from existing tools:
  - language_tools:        轮换 + 徽章 + 连击记录
  - kata_generator:        代码道场 kata
  - polyglot_companion:     语言学习伴侣
  - polyglot_quiz:          语言身份猜谜
  - polyglot_snippet_vault: 片段知识库
  - polyglot_ink:           每日墨讯
  - polyglot_paradigm_weaver: 范式对照报告
  - polyglot_codex:         韬略宝鉴

Polyglot Resonator 的独特视角：
  不是教你写代码，不是练习题，而是——
  用物理学的"共振"比喻，量化你在什么时间适合什么语言。
  凌晨 4 点脑子清醒 → Rust（精密低频）；下午犯困 → Go（稳健中频）...

作者：AllToolkit 全自动生成
依赖：仅 Python 标准库（json, datetime, pathlib, math）
====================================================================
"""

import json
import math
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

# ─────────────────────────────────────────────
# 路径配置
# ─────────────────────────────────────────────
_MODULE_DIR = Path(__file__).parent.parent              # alltoolkit-python/
_WORKSPACE_ROOT = _MODULE_DIR.parent                   # workspace/
DEFAULT_LANGUAGE_ROTATION_JSON = str(_WORKSPACE_ROOT / "language_rotation.json")


# ─────────────────────────────────────────────
# 语言频率映射（Hz — 人文隐喻，非物理真实频率）
# ─────────────────────────────────────────────
LANGUAGE_FREQUENCIES: Dict[str, float] = {
    "Rust":      27.5,   # 🦀 超低频 — 精密、沉稳、编译时铁律
    "Go":        82.5,   # 🐹 中频    — 轻快、务实、goroutine 并行
    "Swift":    220.0,   # 🦅 次高频  — 安全、高雅、iOS 原生
    "Kotlin":   329.6,   # 🟣 中高频  — 现代、JVM、协程流畅
    "TypeScript": 440.0, # 🔷 高频 A  — 类型安全、高密度、大规模工程
    "JavaScript": 493.9, # 🟡 最高频  — 动态、灵活、Web 之王
    "Java":      146.8,  # ☕ 低中频  — 成熟、企业、稳定压倒一切
    "C/C++":     55.0,   # 🔩 超低频  — 底层、操控、接近硬件
}

# 时段偏好因子（小时 → 0.0~1.0，1.0=最偏好）
_HOUR_PREFERENCE: Dict[str, float] = {
    # 凌晨深夜 → Rust / C/C++（精密冷静）
    0: 0.9, 1: 1.0, 2: 1.0, 3: 0.9, 4: 0.8,
    # 清晨 → Go / Java（稳健起步）
    5: 0.6, 6: 0.7, 7: 0.6,
    # 上午 → JavaScript / TypeScript（高频活跃）
    8: 0.8, 9: 0.9, 10: 1.0, 11: 0.9,
    # 午后 → Swift / Kotlin（优雅流畅）
    12: 0.7, 13: 0.8, 14: 0.9, 15: 0.8,
    # 下午后半段 → Go / Java（稳健回归）
    16: 0.7, 17: 0.8, 18: 0.7,
    # 傍晚 → TypeScript / JavaScript（高效收尾）
    19: 0.9, 20: 1.0, 21: 0.9,
    # 深夜前半段 → Rust（深度专注）
    22: 0.8, 23: 0.7,
}

# 星期偏好因子（0=周一 ... 6=周日）
_WEEK_PREFERENCE: Dict[int, float] = {
    0: 0.8,   # 周一：攻坚日 → Rust
    1: 0.7,   # 周二：稳健 → Java
    2: 0.9,   # 周三：高峰期 → TypeScript
    3: 0.7,   # 周四：调整 → Go
    4: 0.8,   # 周五：冲刺 → JavaScript
    5: 0.6,   # 周六：学习 → Swift
    6: 0.5,   # 周日：休闲 → Kotlin
}

# 月份季节因子
_MONTH_SEASON: Dict[int, float] = {
    1: 0.9, 2: 0.9,   # 冬末初春 → 低频语言（Rust/C/C++）
    3: 0.7, 4: 0.7,   # 春季       → Swift/Kotlin
    5: 0.8, 6: 0.8,   # 初夏       → JavaScript/TypeScript
    7: 0.6, 8: 0.6,   # 盛夏       → Go/Java（室内作业）
    9: 0.8, 10: 0.9,  # 秋季       → TypeScript/Rust
    11: 0.7, 12: 0.8, # 冬季       → C/C++/Java
}


# ─────────────────────────────────────────────
# 辅助：ASCII 波形生成
# ─────────────────────────────────────────────

def _waveform(freq: float, amplitude: float, width: int = 60, period: float = 1.0) -> str:
    """
    生成一条简谐波 ASCII 图形。

    Args:
        freq:      频率（Hz，人文隐喻值）
        amplitude: 振幅（行数高度）
        width:     宽度（字符数）
        period:    周期数（波峰数）

    Returns:
        多行 ASCII 波形字符串
    """
    # 将人文频率归一化到可视范围：freq 27.5~493.9 → scale 0.3~2.0
    scale = 0.3 + (freq - 27.5) / (493.9 - 27.5) * 1.7
    lines = []
    chars = " ·•●○■□"
    rows = max(2, int(amplitude * 2))
    mid = rows // 2

    for row in range(rows):
        line = []
        for col in range(width):
            t = (col / width) * period * 2 * math.pi
            # y = sin(2π * freq_normalized * t) 映射到 row 空间
            y = math.sin(2 * math.pi * scale * t)
        y_row = y * (amplitude - 0.5)
        target = mid - row
        if abs(y_row - target) < 0.7:
            line.append("●")
        elif y_row > target + 0.3:
            line.append("~")
        elif y_row < target - 0.3:
            line.append("_")
        else:
            line.append(" ")
        lines.append("".join(line))
    return "\n".join(lines)


def _resonance_bar(value: float, max_val: float = 1.0, width: int = 30) -> str:
    """生成一条比例条。"""
    filled = int(round(value / max_val * width))
    return "█" * filled + "░" * (width - filled)


# ─────────────────────────────────────────────
# 核心共振计算
# ─────────────────────────────────────────────

def _calc_resonance(language: str, now: datetime) -> Dict[str, float]:
    """
    计算某语言在给定时刻的共振强度（0.0 ~ 1.0+）。
    公式：R = base_resonance * hour_factor * week_factor * season_factor

    base_resonance：语言频率越高，学习密度越高（归一化）
    hour_factor：时段偏好
    week_factor：星期偏好
    season_factor：月份季节
    """
    freq = LANGUAGE_FREQUENCIES.get(language, 220.0)
    # 频率归一化到 0.0~1.0（493.9 Hz 对应 1.0）
    base = freq / 493.9

    hour = now.hour
    week = now.weekday()
    month = now.month

    hour_f = _HOUR_PREFERENCE.get(hour, 0.5)
    week_f = _WEEK_PREFERENCE.get(week, 0.5)
    season_f = _MONTH_SEASON.get(month, 0.5)

    resonance = base * hour_f * week_f * season_f
    # 归一化到 0.0~1.0 区间（理论最大值约为 1.0 * 1.0 * 1.0 * 1.0 = 1.0）
    resonance = min(resonance, 1.0)
    return {
        "raw": resonance,
        "hour_factor": hour_f,
        "week_factor": week_f,
        "season_factor": season_f,
        "frequency": freq,
    }


def _build_wave_panel(language: str, resonance_data: Dict[str, float], width: int = 58) -> str:
    """生成语言波形面板。"""
    freq = resonance_data["frequency"]
    amp = 4 + resonance_data["raw"] * 4  # 振幅随共振强度变化
    wave = _waveform(freq, amp, width, period=2.0)

    lines = ["```", wave, "```"]
    return "\n".join(lines)


# ─────────────────────────────────────────────
# 报告生成
# ─────────────────────────────────────────────

def _time_label(now: datetime) -> str:
    """生成人类可读的时间标签。"""
    hour = now.hour
    if 5 <= hour < 12:
        period = "清晨 🌅"
    elif 12 <= hour < 14:
        period = "午间 ☀️"
    elif 14 <= hour < 18:
        period = "下午 🌤️"
    elif 18 <= hour < 21:
        period = "傍晚 🌆"
    elif 21 <= hour < 24:
        period = "深夜 🌙"
    else:
        period = "凌晨 🌑"

    weekdays = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    day = weekdays[now.weekday()]
    date = now.strftime("%Y-%m-%d")
    return f"{date} {day} {period}（{hour:02d}:00）"


def _generate_resonance_report(
    language: str,
    resonance_data: Dict[str, float],
    wave_panel: str,
    all_resonances: Dict[str, float],
    now: datetime,
) -> str:
    """生成完整的共振报告 Markdown。"""
    freq = resonance_data["frequency"]
    raw = resonance_data["raw"]
    emoji_map = {
        "Rust": "🦀", "Go": "🐹", "Swift": "🦅", "Kotlin": "🟣",
        "TypeScript": "🔷", "JavaScript": "🟡", "Java": "☕", "C/C++": "🔩",
    }
    emoji = emoji_map.get(language, "📦")

    # 强度等级
    if raw >= 0.8:
        level = "🔥 极强共振"
        level_color = "极强"
    elif raw >= 0.6:
        level = "⚡ 强共振"
        level_color = "强"
    elif raw >= 0.4:
        level = "～平稳共振～"
        level_color = "平稳"
    elif raw >= 0.2:
        level = "░ 弱共振"
        level_color = "弱"
    else:
        level = "✗ 几乎无共振"
        level_color = "几乎无"

    # 共振条
    bar = _resonance_bar(raw, max_val=1.0, width=28)

    # 全语言横向对比
    sorted_langs = sorted(all_resonances.items(), key=lambda x: x[1], reverse=True)
    rank = next(i for i, (l, _) in enumerate(sorted_langs, 1) if l == language)

    comparison_lines = []
    max_r = max(all_resonances.values()) or 1.0
    for lang, r in sorted_langs:
        mark = "👉" if lang == language else "  "
        comp_bar = _resonance_bar(r, max_val=max_r, width=22)
        comparison_lines.append(f"{mark} {emoji_map.get(lang,'📦')} {lang:<12} {comp_bar}  {r:.3f}")

    # 时段建议
    hour = now.hour
    if 0 <= hour < 6:
        tip = "🌑 深夜模式：适合 Rust / C/C++ — 低频精密作业"
    elif 6 <= hour < 9:
        tip = "🌅 清晨模式：适合 Go / Java — 稳健启动"
    elif 9 <= hour < 12:
        tip = "☀️ 上午模式：适合 TypeScript / JavaScript — 高频冲刺"
    elif 12 <= hour < 15:
        tip = "🌤️ 午后模式：适合 Swift / Kotlin — 优雅流畅"
    elif 15 <= hour < 18:
        tip = "🌆 下午后半：适合 Go / Java — 稳健回归"
    elif 18 <= hour < 21:
        tip = "🌇 傍晚模式：适合 JavaScript / TypeScript — 高效收尾"
    else:
        tip = "🌙 夜间模式：适合 Rust / C/C++ — 深度专注"

    lines = [
        f"# 🌀 语言共振报告 — {language} {emoji}",
        "",
        f"**时刻**：{_time_label(now)}",
        "",
        f"| 指标 | 数值 |",
        f"|------|------|",
        f"| 🔊 语言频率 | {freq:.1f} Hz（人文隐喻） |",
        f"| ⚡ 共振强度 | {bar} **{raw:.3f}** |",
        f"| 📊 共振等级 | {level} |",
        f"| 🏆 当前排名 | 第 {rank} 名（共 {len(sorted_langs)} 种语言） |",
        "",
        f"### 📐 振动波形",
        wave_panel,
        "",
        f"### 🔍 共振因子拆解",
        f"| 因子 | 权重 | 说明 |",
        f"|------|------|------|",
        f"| 🕐 时段因子 | `{resonance_data['hour_factor']:.1f}` | {tip.split('：')[0]} |",
        f"| 📅 星期因子 | `{resonance_data['week_factor']:.1f}` | {['周一攻坚', '周二稳健', '周三高峰', '周四调整', '周五冲刺', '周六学习', '周日休闲'][now.weekday()]} |",
        f"| 🌿 季节因子 | `{resonance_data['season_factor']:.1f}` | {['冬末初春', '冬末初春', '春季', '春季', '初夏', '初夏', '盛夏', '盛夏', '秋季', '秋季', '秋季', '冬季'][now.month - 1]} |",
        "",
        f"### 📊 全语言共振排行",
        "```",
        "\n".join(comparison_lines),
        "```",
        "",
        f"### 💡 当前时段建议",
        f"> {tip}",
        "",
        f"---",
        f"> 📌 **下一个语言**: {next_lang(language)}  — 继续探索共振！",
    ]
    return "\n".join(lines)


def next_lang(current: str) -> str:
    """获取当前语言的下一个语言。"""
    order = ["Rust", "Go", "Swift", "Kotlin", "TypeScript", "JavaScript", "Java", "C/C++"]
    try:
        idx = order.index(current)
        return order[(idx + 1) % len(order)]
    except ValueError:
        return "Rust"


# ─────────────────────────────────────────────
# 主 API
# ─────────────────────────────────────────────

def generate_resonance_report(
    json_path: str = DEFAULT_LANGUAGE_ROTATION_JSON,
    now: Optional[datetime] = None,
) -> Dict[str, Any]:
    """
    读取 language_rotation.json，按 current_index 取当前语言，
    计算该语言在当前时刻的共振报告，并将 current_index 前移一位。

    Args:
        json_path: language_rotation.json 路径
        now:       可选，指定时间（用于测试）

    Returns:
        {
            "language": str,
            "next_language": str,
            "resonance": {raw, hour_factor, week_factor, season_factor, frequency},
            "wave_panel": str,
            "report": str,          # Markdown 格式报告
            "rank": int,
            "all_resonances": dict,
            "json_updated": bool,
            "timestamp": str,
        }
    """
    if now is None:
        now = datetime.now()

    # 读取 JSON
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    languages = data["languages"]
    idx = data.get("current_index", 0) % len(languages)
    current = languages[idx]
    next_idx = (idx + 1) % len(languages)
    next_language = languages[next_idx]

    # 计算共振
    resonance_data = _calc_resonance(current, now)

    # 全语言共振排行
    all_resonances = {lang: _calc_resonance(lang, now)["raw"] for lang in languages}
    sorted_langs = sorted(all_resonances.items(), key=lambda x: x[1], reverse=True)
    rank = next(i for i, (l, _) in enumerate(sorted_langs, 1) if l == current)

    # 波形面板
    wave_panel = _build_wave_panel(current, resonance_data, width=58)

    # 完整报告
    report = _generate_resonance_report(
        language=current,
        resonance_data=resonance_data,
        wave_panel=wave_panel,
        all_resonances=all_resonances,
        now=now,
    )

    # 更新 JSON
    data["current_index"] = next_idx
    data["last_language"] = current
    data["updated_at"] = now.strftime("%Y-%m-%dT%H:%M:%S+08:00")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return {
        "language": current,
        "next_language": next_language,
        "resonance": resonance_data,
        "wave_panel": wave_panel,
        "report": report,
        "rank": rank,
        "all_resonances": all_resonances,
        "json_updated": True,
        "timestamp": now.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
    }


def get_resonance_only(
    language: Optional[str] = None,
    json_path: str = DEFAULT_LANGUAGE_ROTATION_JSON,
    now: Optional[datetime] = None,
) -> Dict[str, Any]:
    """
    查询共振数据（不推进索引，不写 JSON）。
    如果不指定 language，使用当前轮换语言。
    """
    if now is None:
        now = datetime.now()

    if language is None:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        languages = data["languages"]
        idx = data.get("current_index", 0) % len(languages)
        language = languages[idx]

    resonance = _calc_resonance(language, now)

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    languages = data["languages"]
    all_resonances = {lang: _calc_resonance(lang, now)["raw"] for lang in languages}
    sorted_langs = sorted(all_resonances.items(), key=lambda x: x[1], reverse=True)
    rank = next(i for i, (l, _) in enumerate(sorted_langs, 1) if l == language)

    return {
        "language": language,
        "resonance": resonance,
        "rank": rank,
        "all_resonances": all_resonances,
        "timestamp": now.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
    }


# ─────────────────────────────────────────────
# CLI 入口
# ─────────────────────────────────────────────

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Polyglot Resonator — 编程语言共振分析仪"
    )
    sub = parser.add_subparsers(dest="cmd")

    gen = sub.add_parser("generate", help="生成共振报告（推进轮换）")
    gen.add_argument("--json", default=DEFAULT_LANGUAGE_ROTATION_JSON, help="JSON 路径")

    q = sub.add_parser("query", help="查询共振（不推进轮换）")
    q.add_argument("language", nargs="?", help="语言名称（可选）")
    q.add_argument("--json", default=DEFAULT_LANGUAGE_ROTATION_JSON)

    args = parser.parse_args()

    if args.cmd == "generate":
        result = generate_resonance_report(json_path=args.json)
        print(result["report"])
    elif args.cmd == "query":
        result = get_resonance_only(
            language=args.language if args.language else None,
            json_path=args.json,
        )
        lang = result["language"]
        r = result["resonance"]
        print(f"\n🔊 {lang} — 共振强度: {r['raw']:.3f}")
        print(f"   时段因子: {r['hour_factor']} | 星期因子: {r['week_factor']} | 季节因子: {r['season_factor']}")
        print(f"   频率: {r['frequency']:.1f} Hz | 排名: 第 {result['rank']} 名")
        print("\n全语言排行：")
        for l, v in sorted(result["all_resonances"].items(), key=lambda x: x[1], reverse=True):
            print(f"  {l}: {v:.3f}")
    else:
        parser.print_help()
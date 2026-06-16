"""
polyglot_archetype_canvas.py — 编程语言原神殿堂 (Polyglot Archetype Canvas)
=============================================================================
每个程序员心中都住着一个原神 — 每种编程语言也有其「命之座」。
本模块将语言映射为神话/奇幻原型角色，结合当前时间生成「角色今日运势」。

核心逻辑：
  1. 读取 language_rotation.json，按 current_index 取当前轮换语言
  2. 将语言映射为独特原型（Archetype）：战士、法师、刺客、圣职者...
  3. 结合当前时间（小时）计算「今日状态」— 精力、创意、专注、社交
  4. 生成 ASCII 角色立绘 + 属性面板 + 今日建议
  5. 完成后将 current_index 前移一位并更新 updated_at

语言轮换顺序（8 种核心语言）：
  Rust → Go → Swift → Kotlin → TypeScript → JavaScript → Java → C/C++ → Rust（循环）

Distinct from existing modules:
  - polyglot_resonator:    频率共振波形图
  - polyglot_codex:        代码韬略 kata
  - polyglot_companion:    学习伴侣
  - polyglot_quiz:         语言身份猜谜
  - polyglot_ink:          每日墨讯
  - polyglot_paradigm_weaver: 范式对照
  - polyglot_snippet_vault:   片段库

Polyglot Archetype Canvas 的独特视角：
  不是教你写代码，不是练习题，而是——
  把语言当作角色来「抽卡」，看今天你 code 的「命之座」是哪位原神。
  Rust = 无功之勋的守护者、Go = 轻盈的风之精灵、Swift = 优雅的银鹰...

作者：AllToolkit 全自动生成
依赖：仅 Python 标准库（json, datetime, pathlib）
====================================================================
"""

import json
import math
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

# ─────────────────────────────────────────────
# 路径配置
# ─────────────────────────────────────────────
_MODULE_DIR = Path(__file__).parent.parent              # alltoolkit-python/
_WORKSPACE_ROOT = _MODULE_DIR.parent                   # workspace/
DEFAULT_LANGUAGE_ROTATION_JSON = str(_WORKSPACE_ROOT / "language_rotation.json")


# ─────────────────────────────────────────────
# 语言 → 原型（Archetype）映射
# ─────────────────────────────────────────────
LANGUAGE_ARCHETYPES: Dict[str, Dict[str, Any]] = {
    "Rust": {
        "archetype": "守护者 Guardian",
        "element": "🪨 大地",
        "domain": "内存安全 · 所有权铁律",
        "personality": "严谨、沉默、不妥协",
        "strengths": ["零成本抽象", "编译期铁律", "内存安全", "并发无忧"],
        "weaknesses": ["编译时间漫长", "学习曲线陡峭", "错误信息复杂"],
        "emoji": "🦀",
        "quote": "「无功之勋，不受天禄。」",
        "color": (139, 69, 19),   # 铁锈棕
    },
    "Go": {
        "archetype": "风之精灵 Sylph",
        "element": "🌬️ 风",
        "domain": "并发 · 云原生 · 简洁务实",
        "personality": "轻盈、务实、热爱和平",
        "strengths": ["goroutine 并发", "部署简单", "学习平缓", "标准库强大"],
        "weaknesses": ["泛型姗姗来迟", "错误处理冗长", "编译产物大"],
        "emoji": "🐹",
        "quote": "「上善若水，水善利万物而不争。」",
        "color": (0, 175, 240),   # Go 蓝
    },
    "Swift": {
        "archetype": "银鹰 Silver Eagle",
        "element": "🌿 风木",
        "domain": "iOS/macOS · 安全优雅",
        "personality": "高贵、优雅、追求完美",
        "strengths": ["安全性高", "语法优雅", "性能卓越", "Apple 生态"],
        "weaknesses": ["平台锁定", "生态系统封闭", "版本兼容问题"],
        "emoji": "🦅",
        "quote": "「银羽划破长空，一击即中。」",
        "color": (250, 95, 47),   # Swift 橙红
    },
    "Kotlin": {
        "archetype": "灵溪法师 Stream Sage",
        "element": "💧 水",
        "domain": "JVM · 协程 · 现代语法",
        "personality": "灵动、包容、与时俱进",
        "strengths": ["协程原生支持", "空安全", "与 Java 互操作", "扩展函数"],
        "weaknesses": ["JVM 启动慢", "编译时间中", "生态依赖 Java"],
        "emoji": "🟣",
        "quote": "「柔能克刚，灵动如溪。」",
        "color": (169, 92, 220),  # Kotlin 紫
    },
    "TypeScript": {
        "archetype": "符文大师 Rune Master",
        "element": "⚡ 雷光",
        "domain": "Web 工程化 · 类型安全",
        "personality": "精密、严谨、追求秩序",
        "strengths": ["类型系统", "IDE 支持极佳", "npm 生态庞大", "前端标配"],
        "weaknesses": ["类型复杂时难以驾驭", "运行时仍有漏洞", "编译开销"],
        "emoji": "🔷",
        "quote": "「符文字字珠玑，秩序即是力量。」",
        "color": (49, 120, 198),  # TS 蓝
    },
    "JavaScript": {
        "archetype": "幻术师 Illusionist",
        "element": "🔥 火焰",
        "domain": "Web 全栈 · 灵活多变",
        "personality": "自由、奔放、充满惊喜",
        "strengths": ["全能全栈", "生态最大", "灵活动态", "实时反馈"],
        "weaknesses": ["类型混乱", "回调地狱", "版本碎片", "奇怪隐式转换"],
        "emoji": "🟡",
        "quote": "「幻中藏真，真中藏幻。」",
        "color": (247, 223, 30),  # JS 黄
    },
    "Java": {
        "archetype": "圣殿武士 Temple Knight",
        "element": "☀️ 圣光",
        "domain": "企业级 · JVM · 跨平台",
        "personality": "沉稳、公正、纪律严明",
        "strengths": ["生态成熟", "跨平台 Write Once", "框架丰富", "人才众多"],
        "weaknesses": ["语法冗长", "启动慢", "占用高", "更新保守"],
        "emoji": "☕",
        "quote": "「圣殿永固，律令长存。」",
        "color": (237, 139, 0),   # Java 橙
    },
    "C/C++": {
        "archetype": "龙裔 Dragonborn",
        "element": "🌋 熔岩",
        "domain": "系统级 · 极致性能",
        "personality": "力量至上、掌控一切、不惧危险",
        "strengths": ["硬件直控", "极致性能", "零抽象", "无所不能"],
        "weaknesses": ["内存危险", "未定义行为多", "调试困难", "学习成本极高"],
        "emoji": "🔩",
        "quote": "「龙之血脉，熔岩铸魂。」",
        "color": (8, 87, 158),    # 深蓝
    },
}

ALL_LANGUAGES = list(LANGUAGE_ARCHETYPES.keys())


# ─────────────────────────────────────────────
# 今日状态计算（基于小时）
# ─────────────────────────────────────────────

def _hour_to_vitality(hour: int) -> float:
    """精力值：0.0~1.0，清晨高，深夜也高，午后低谷"""
    if 6 <= hour < 9:
        return 0.6 + (hour - 6) * 0.1
    elif 9 <= hour < 12:
        return 0.9
    elif 12 <= hour < 15:
        return 0.4 + (hour - 12) * 0.05  # 午后低谷
    elif 15 <= hour < 18:
        return 0.6 + (hour - 15) * 0.1
    elif 18 <= hour < 21:
        return 0.7
    elif 21 <= hour < 24:
        return 0.5 + (24 - hour) * 0.05  # 夜间缓慢下降
    else:  # 0~5
        return 0.3 + (5 - hour) * 0.02  # 凌晨低谷


def _hour_to_creativity(hour: int) -> float:
    """创意值：深夜和清晨最高，午后次之"""
    if 0 <= hour < 5:
        return 0.9
    elif 5 <= hour < 9:
        return 0.7
    elif 9 <= hour < 12:
        return 0.6
    elif 12 <= hour < 15:
        return 0.5
    elif 15 <= hour < 18:
        return 0.7
    elif 18 <= hour < 21:
        return 0.8
    else:
        return 0.7


def _hour_to_focus(hour: int) -> float:
    """专注值：上午和深夜最高，社交时段最低"""
    if 0 <= hour < 5:
        return 0.9
    elif 5 <= hour < 9:
        return 0.7
    elif 9 <= hour < 12:
        return 1.0  # 黄金专注时段
    elif 12 <= hour < 15:
        return 0.6
    elif 15 <= hour < 18:
        return 0.8
    elif 18 <= hour < 21:
        return 0.5  # 社交时段
    else:
        return 0.7


def _hour_to_social(hour: int) -> float:
    """社交值：白天和傍晚高，深夜凌晨低"""
    if 0 <= hour < 6:
        return 0.1
    elif 6 <= hour < 9:
        return 0.5
    elif 9 <= hour < 12:
        return 0.6
    elif 12 <= hour < 15:
        return 0.7
    elif 15 <= hour < 18:
        return 0.8
    elif 18 <= hour < 21:
        return 0.9  # 社交高峰
    else:
        return 0.6


def _time_to_mood(hour: int) -> str:
    """根据小时返回心情描述"""
    if 0 <= hour < 5:
        return "🌑 深夜独处 · 万籁俱寂"
    elif 5 <= hour < 7:
        return "🌅 黎明破晓 · 万物初醒"
    elif 7 <= hour < 9:
        return "🌄 朝霞满天 · 蓄势待发"
    elif 9 <= hour < 12:
        return "☀️ 旭日东升 · 黄金专注"
    elif 12 <= hour < 14:
        return "🌤️ 午后暖阳 · 慵懒时分"
    elif 14 <= hour < 17:
        return "🌤 下午时光 · 稳中求进"
    elif 17 <= hour < 19:
        return "🌆 夕阳西下 · 收网整理"
    elif 19 <= hour < 21:
        return "🌇 华灯初上 · 社交时刻"
    else:
        return "🌙 夜幕降临 · 沉淀反思"


def _calc_daily_state(now: datetime) -> Dict[str, float]:
    """计算今日四维状态"""
    return {
        "精力 Vitality": _hour_to_vitality(now.hour),
        "创意 Creativity": _hour_to_creativity(now.hour),
        "专注 Focus": _hour_to_focus(now.hour),
        "社交 Social": _hour_to_social(now.hour),
    }


# ─────────────────────────────────────────────
# ASCII 角色立绘生成
# ─────────────────────────────────────────────

def _build_stat_bar(value: float, width: int = 18) -> str:
    """生成属性条（彩色效果用 ASCII）"""
    filled = int(round(value * width))
    return "█" * filled + "░" * (width - filled)


def _attribute_rating(state: Dict[str, float], archetype: str) -> Dict[str, float]:
    """
    根据原型调整基础属性系数（±20%）。
    比如"守护者"专注高、社交低；"幻术师"创意高、精力波动大。
    """
    multipliers = {
        "守护者 Guardian":   {"精力": 1.1, "创意": 0.85, "专注": 1.15, "社交": 0.7},
        "风之精灵 Sylph":    {"精力": 0.9, "创意": 1.1, "专注": 0.9, "社交": 1.1},
        "银鹰 Silver Eagle": {"精力": 1.0, "创意": 1.1, "专注": 1.0, "社交": 0.9},
        "灵溪法师 Stream Sage": {"精力": 0.85, "创意": 1.2, "专注": 0.9, "社交": 1.0},
        "符文大师 Rune Master": {"精力": 0.9, "创意": 1.0, "专注": 1.2, "社交": 0.8},
        "幻术师 Illusionist": {"精力": 0.9, "创意": 1.3, "专注": 0.8, "社交": 1.1},
        "圣殿武士 Temple Knight": {"精力": 1.1, "创意": 0.8, "专注": 1.0, "社交": 1.0},
        "龙裔 Dragonborn":   {"精力": 1.2, "创意": 0.9, "专注": 1.1, "社交": 0.7},
    }
    m = multipliers.get(archetype, {})
    adjusted = {}
    for key, val in state.items():
        short_key = key.split()[0]  # "精力 Vitality" → "精力"
        mult = m.get(short_key, 1.0)
        adjusted[key] = min(val * mult, 1.0)
    return adjusted


def _generate_ascii_portrait(language: str, archetype: str) -> str:
    """生成简短的 ASCII 角色立绘（文本框风格）"""
    emoji_map = {
        "Rust": "🦀", "Go": "🐹", "Swift": "🦅", "Kotlin": "🟣",
        "TypeScript": "🔷", "JavaScript": "🟡", "Java": "☕", "C/C++": "🔩",
    }
    emoji = emoji_map.get(language, "📦")

    # 不同原型用不同 ASCII 符号（预计算，避免 f-string 里的 \ 语法问题）
    symbol_map = {
        "守护者 Guardian":   "/\\",
        "风之精灵 Sylph":    "~^",
        "银鹰 Silver Eagle": "/V",
        "灵溪法师 Stream Sage": "~~",
        "符文大师 Rune Master": "◆◇",
        "幻术师 Illusionist": "*★",
        "圣殿武士 Temple Knight": "[+]",
        "龙裔 Dragonborn":   "/\\",
    }
    sym = symbol_map.get(archetype, "()")
    inner_sym = "/\\" if ("Guardian" in archetype or "Dragonborn" in archetype) else "~~"

    lines = [
        "```",
        "╔══════════════════════════╗",
        f"║        {emoji}  {archetype:<20} ║",
        f"║     Language: {language:<15} ║",
        "║                             ║",
        f"║   {sym[0]}    {sym[1]}    {sym[0]}    {sym[1]}   ║",
        f"║     {inner_sym}   {inner_sym}     ║",
        "╚══════════════════════════╝",
        "```",
    ]
    return "\n".join(lines)


# ─────────────────────────────────────────────
# 今日运势生成
# ─────────────────────────────────────────────

def _fortune_rating(state: Dict[str, float]) -> str:
    """综合评分（四个属性的加权平均）"""
    total = (
        state["精力 Vitality"] * 0.2 +
        state["创意 Creativity"] * 0.3 +
        state["专注 Focus"] * 0.35 +
        state["社交 Social"] * 0.15
    )
    if total >= 0.85:
        return "🌟 大吉 — 今日诸事皆宜！"
    elif total >= 0.7:
        return "✨ 中吉 — 适合推进重要项目"
    elif total >= 0.55:
        return "🌓 平吉 — 稳扎稳打，控制节奏"
    elif total >= 0.4:
        return "🌧️ 小凶 — 适合学习和维护"
    else:
        return "💀 凶 — 今日宜休息，忌强行推进"


def _build_tips(language: str, archetype: str, state: Dict[str, float]) -> List[str]:
    """根据语言原型和今日状态生成建议"""
    tips = []
    vit = state["精力 Vitality"]
    cre = state["创意 Creativity"]
    foc = state["专注 Focus"]
    soc = state["社交 Social"]

    # 基于语言特点
    if language == "Rust":
        tips.append("🦀 今日适合：重构内存敏感模块、编写 WASM")
        if foc > 0.8:
            tips.append("⚡ 专注力极佳：挑战复杂的所有权问题！")
        if vit < 0.5:
            tips.append("💡 精力不足时：先阅读文档，不要硬写编译不过的代码")
    elif language == "Go":
        tips.append("🐹 今日适合：写微服务、写工具、写胶水代码")
        if cre > 0.8:
            tips.append("⚡ 创意迸发：用 Go 写一个有意思的小工具")
        if vit < 0.5:
            tips.append("💡 简洁即力量：不要过度工程")
    elif language == "Swift":
        tips.append("🦅 今日适合：iOS 界面开发、SwiftUI 尝鲜")
        if foc > 0.8:
            tips.append("⚡ 专注力极佳：写一个完整的 View 组件")
        if soc > 0.7:
            tips.append("💡 社交日：参与 Swift 社区讨论")
    elif language == "Kotlin":
        tips.append("🟣 今日适合：Android 开发、协程练习")
        if cre > 0.8:
            tips.append("⚡ 创意时刻：用扩展函数写 DSL")
        if vit < 0.5:
            tips.append("💡 疲惫时：用 Kotlin 写简洁的业务逻辑")
    elif language == "TypeScript":
        tips.append("🔷 今日适合：类型设计、重构大型前端项目")
        if foc > 0.8:
            tips.append("⚡ 专注极佳：写一个复杂的泛型工具类型")
        if soc > 0.7:
            tips.append("💡 社交日：review 他人的 TypeScript PR")
    elif language == "JavaScript":
        tips.append("🟡 今日适合：快速原型、Node.js 脚本、前端交互")
        if cre > 0.8:
            tips.append("⚡ 灵感迸发：写一个有意思的算法可视化")
        if vit < 0.5:
            tips.append("💡 低精力时：用 JS 写轻量脚本最省力")
    elif language == "Java":
        tips.append("☕ 今日适合：企业级后端、Spring 开发")
        if foc > 0.8:
            tips.append("⚡ 专注极佳：做架构设计或代码评审")
        if soc > 0.7:
            tips.append("💡 社交日：参加 Java 社区活动")
    elif language == "C/C++":
        tips.append("🔩 今日适合：性能优化、游戏引擎、嵌入式")
        if vit > 0.8 and foc > 0.8:
            tips.append("⚡ 巅峰状态：挑战底层系统编程！")
        if vit < 0.5:
            tips.append("💡 精力不足时避免手动内存管理")

    # 基于时间
    hour = datetime.now().hour
    if 0 <= hour < 6:
        tips.append("🌑 深夜时光：适合深度思考，避免高风险操作")
    elif 9 <= hour < 12:
        tips.append("☀️ 上午黄金期：最适合处理复杂逻辑")
    elif 14 <= hour < 17:
        tips.append("🌤️ 下午时光：适合常规任务和代码review")
    elif 19 <= hour < 21:
        tips.append("🌇 傍晚社交时段：适合讨论和知识分享")
    return tips


def _generate_archetype_report(
    language: str,
    state: Dict[str, float],
    now: datetime,
) -> str:
    """生成完整的原型报告 Markdown"""
    meta = LANGUAGE_ARCHETYPES[language]
    arch = meta["archetype"]
    adjusted = _attribute_rating(state, arch)

    # 心情
    mood = _time_to_mood(now.hour)

    # 综合运势
    fortune = _fortune_rating(state)

    # 建议
    tips = _build_tips(language, arch, state)

    # 属性条
    stat_lines = []
    for key, val in adjusted.items():
        bar = _build_stat_bar(val, width=18)
        short_key = key.split()[0]
        stat_lines.append(f"| {short_key:<6} | {bar} | {val:.2f} |")

    # 立绘
    portrait = _generate_ascii_portrait(language, arch)

    # 时间标签
    weekdays = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    day = weekdays[now.weekday()]
    time_label = f"{now.strftime('%Y-%m-%d')} {day} {now.strftime('%H:%M')}"

    lines = [
        f"# 🎭 语言原神殿堂 — {language} {meta['emoji']}",
        "",
        f"**今日时刻**：{time_label} | {mood}",
        f"**运势**：{fortune}",
        "",
        f"### 🖼️ 角色立绘",
        portrait,
        "",
        f"### ⚔️ {arch}",
        f"**元素**：{meta['element']}  **领域**：{meta['domain']}",
        f"**性格**：{meta['personality']}",
        "",
        f"> 💬 「{meta['quote']}」",
        "",
        f"### 📊 今日四维属性（基于 {now.hour}:00 调整）",
        "| 属性 | 条 | 数值 |",
        "|------|-----|------|",
        *stat_lines,
        "",
        f"### 🗡️ 角色天赋",
        f"**优势**：{', '.join(meta['strengths'])}",
        "",
        f"**弱点**：{', '.join(meta['weaknesses'])}",
        "",
        f"### 💡 今日建议",
        *[f"- {tip}" for tip in tips],
        "",
        f"---",
        f"> 🎲 **下一个角色**: {next_lang(language)}  — 命之座轮换中...",
    ]
    return "\n".join(lines)


def next_lang(current: str) -> str:
    """获取当前语言的下一个语言（用于循环轮换）"""
    try:
        idx = ALL_LANGUAGES.index(current)
        return ALL_LANGUAGES[(idx + 1) % len(ALL_LANGUAGES)]
    except ValueError:
        return ALL_LANGUAGES[0]


# ─────────────────────────────────────────────
# 主 API
# ─────────────────────────────────────────────

def generate_archetype_report(
    json_path: str = DEFAULT_LANGUAGE_ROTATION_JSON,
    now: Optional[datetime] = None,
) -> Dict[str, Any]:
    """
    读取 language_rotation.json，按 current_index 取当前语言，
    生成该语言的原型殿堂报告，并将 current_index 前移一位。

    Args:
        json_path: language_rotation.json 路径
        now:       可选，指定时间（用于测试）

    Returns:
        {
            "language": str,
            "archetype": str,
            "element": str,
            "daily_state": dict,
            "fortune": str,
            "report": str,
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

    # 计算今日状态
    daily_state = _calc_daily_state(now)

    # 获取语言元数据
    meta = LANGUAGE_ARCHETYPES.get(current, LANGUAGE_ARCHETYPES["Rust"])

    # 生成报告
    report = _generate_archetype_report(current, daily_state, now)

    # 更新 JSON
    data["current_index"] = next_idx
    data["last_language"] = current
    data["updated_at"] = now.strftime("%Y-%m-%dT%H:%M:%S+08:00")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return {
        "language": current,
        "archetype": meta["archetype"],
        "element": meta["element"],
        "daily_state": daily_state,
        "fortune": _fortune_rating(daily_state),
        "report": report,
        "json_updated": True,
        "timestamp": now.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
        "next_language": next_language,
    }


def get_archetype_only(
    language: Optional[str] = None,
    json_path: str = DEFAULT_LANGUAGE_ROTATION_JSON,
    now: Optional[datetime] = None,
) -> Dict[str, Any]:
    """
    查询语言原型（不推进轮换，不写 JSON）。
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

    meta = LANGUAGE_ARCHETYPES.get(language, LANGUAGE_ARCHETYPES["Rust"])
    daily_state = _calc_daily_state(now)

    return {
        "language": language,
        "archetype": meta["archetype"],
        "element": meta["element"],
        "domain": meta["domain"],
        "personality": meta["personality"],
        "strengths": meta["strengths"],
        "weaknesses": meta["weaknesses"],
        "daily_state": daily_state,
        "fortune": _fortune_rating(daily_state),
        "timestamp": now.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
    }


# ─────────────────────────────────────────────
# CLI 入口
# ─────────────────────────────────────────────

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Polyglot Archetype Canvas — 编程语言原神殿堂"
    )
    sub = parser.add_subparsers(dest="cmd")

    gen = sub.add_parser("generate", help="生成原型报告（推进轮换）")
    gen.add_argument("--json", default=DEFAULT_LANGUAGE_ROTATION_JSON)

    q = sub.add_parser("query", help="查询原型（不推进轮换）")
    q.add_argument("language", nargs="?", help="语言名称（可选）")
    q.add_argument("--json", default=DEFAULT_LANGUAGE_ROTATION_JSON)

    args = parser.parse_args()

    if args.cmd == "generate":
        result = generate_archetype_report(json_path=args.json)
        print(result["report"])
    elif args.cmd == "query":
        result = get_archetype_only(
            language=args.language if args.language else None,
            json_path=args.json,
        )
        print(f"\n🎭 {result['language']} — {result['archetype']}")
        print(f"   元素: {result['element']} | 领域: {result['domain']}")
        print(f"   性格: {result['personality']}")
        print(f"   运势: {result['fortune']}")
        print(f"\n四维状态：")
        for k, v in result["daily_state"].items():
            bar = _build_stat_bar(v, 18)
            print(f"  {k.split()[0]}: {bar} {v:.2f}")
        print(f"\n优势: {', '.join(result['strengths'])}")
        print(f"弱点: {', '.join(result['weaknesses'])}")
    else:
        parser.print_help()
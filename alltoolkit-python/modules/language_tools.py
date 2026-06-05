"""
语言轮换工具模块 (Polyglot Toolkit)
支持按顺序轮换编程语言、生成语言徽章、追踪连续学习记录
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any

# 模块内嵌的 language_rotation.json 路径（与 alltoolkit-python 平级的 workspace 根目录）
_MODULE_DIR = Path(__file__).parent.parent  # alltoolkit-python/
_WORKSPACE_ROOT = _MODULE_DIR.parent       # workspace/

DEFAULT_LANGUAGE_ROTATION_JSON = str(_WORKSPACE_ROOT / "language_rotation.json")


# ─────────────────────────────────────────────
# 语言元数据：每种语言的花名册、简介、Hello World 示例
# ─────────────────────────────────────────────
LANGUAGE_METADATA: Dict[str, Dict[str, Any]] = {
    "Rust": {
        "emoji": "🦀",
        "tagline": "Safe, concurrent, practical.",
        "hello_world": 'fn main() { println!("Hello, World!"); }',
        "file_ext": "rs",
        "year": 2015,
        "paradigm": "Systems / Memory-safe",
    },
    "Go": {
        "emoji": "🐹",
        "tagline": "Go is expressive, concise, and clean.",
        "hello_world": 'package main\n\nimport "fmt"\n\nfunc main() {\n    fmt.Println("Hello, World!")\n}',
        "file_ext": "go",
        "year": 2009,
        "paradigm": "Concurrent / Compiled",
    },
    "Swift": {
        "emoji": "🦅",
        "tagline": "Anyone who writes software should read Swift.",
        "hello_world": 'print("Hello, World!")',
        "file_ext": "swift",
        "year": 2014,
        "paradigm": "Multi-paradigm / Safe",
    },
    "Kotlin": {
        "emoji": "🟣",
        "tagline": "Better language for Android and JVM.",
        "hello_world": 'fun main() {\n    println("Hello, World!")\n}',
        "file_ext": "kt",
        "year": 2011,
        "paradigm": "OO / Functional / JVM",
    },
    "TypeScript": {
        "emoji": "🔷",
        "tagline": "JavaScript that scales.",
        "hello_world": 'console.log("Hello, World!");',
        "file_ext": "ts",
        "year": 2012,
        "paradigm": "Typed Superset of JS",
    },
    "JavaScript": {
        "emoji": "🟡",
        "tagline": "The language of the web.",
        "hello_world": 'console.log("Hello, World!");',
        "file_ext": "js",
        "year": 1995,
        "paradigm": "Dynamic / Prototype-based",
    },
    "Java": {
        "emoji": "☕",
        "tagline": "Write once, run anywhere.",
        "hello_world": 'public class Hello {\n    public static void main(String[] args) {\n        System.out.println("Hello, World!");\n    }\n}',
        "file_ext": "java",
        "year": 1995,
        "paradigm": "OO / Class-based / JVM",
    },
    "C/C++": {
        "emoji": "🔩",
        "tagline": "Close to the metal, close to perfection.",
        "hello_world": '#include <stdio.h>\n\nint main() {\n    printf("Hello, World!\\n");\n    return 0;\n}',
        "file_ext": "cpp",
        "year": 1983,
        "paradigm": "Systems / Low-level",
    },
}


# ─────────────────────────────────────────────
# 核心：读写 language_rotation.json
# ─────────────────────────────────────────────

def _read_rotation_json(json_path: str) -> Dict[str, Any]:
    """读取语言轮换配置 JSON。"""
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)


def _write_rotation_json(json_path: str, data: Dict[str, Any]) -> None:
    """写回语言轮换配置 JSON。"""
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# ─────────────────────────────────────────────
# API：轮换选择 + 状态查询 + 徽章生成
# ─────────────────────────────────────────────

def rotate_and_get_next(
    json_path: str = DEFAULT_LANGUAGE_ROTATION_JSON,
) -> Dict[str, Any]:
    """
    读取 language_rotation.json，按 current_index 取出当前语言，
    然后将 current_index 向前移动一位（循环），并更新 JSON。

    Returns:
        {
            "current_language": str,
            "next_language": str,
            "hello_world": str,
            "emoji": str,
            "tagline": str,
            "file_ext": str,
            "year": int,
            "paradigm": str,
            "index": int,
            "total": int,
        }
    """
    data = _read_rotation_json(json_path)
    languages = data["languages"]
    total = len(languages)
    idx = data.get("current_index", 0) % total

    current = languages[idx]
    meta = LANGUAGE_METADATA.get(current, {})

    # 循环前进
    next_idx = (idx + 1) % total
    data["current_index"] = next_idx
    data["last_language"] = current
    data["updated_at"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00")
    _write_rotation_json(json_path, data)

    return {
        "current_language": current,
        "next_language": languages[next_idx],
        "hello_world": meta.get("hello_world", ""),
        "emoji": meta.get("emoji", "📦"),
        "tagline": meta.get("tagline", ""),
        "file_ext": meta.get("file_ext", ""),
        "year": meta.get("year", 0),
        "paradigm": meta.get("paradigm", ""),
        "index": idx,
        "total": total,
    }


def get_rotation_status(
    json_path: str = DEFAULT_LANGUAGE_ROTATION_JSON,
) -> Dict[str, Any]:
    """
    查询当前轮换状态（不推进索引）。
    """
    data = _read_rotation_json(json_path)
    languages = data["languages"]
    idx = data.get("current_index", 0) % len(languages)
    current = languages[idx]

    return {
        "languages": languages,
        "current_language": current,
        "current_index": idx,
        "next_language": languages[(idx + 1) % len(languages)],
        "total": len(languages),
        "last_language": data.get("last_language", ""),
        "updated_at": data.get("updated_at", ""),
    }


def get_language_badge(language: Optional[str] = None, json_path: str = DEFAULT_LANGUAGE_ROTATION_JSON) -> str:
    """
    生成语言徽章文本（ASCII-art 风格）。如果不指定 language，使用当前轮换语言。
    """
    if language is None:
        data = _read_rotation_json(json_path)
        languages = data["languages"]
        idx = data.get("current_index", 0) % len(languages)
        language = languages[idx]

    meta = LANGUAGE_METADATA.get(language, {})
    emoji = meta.get("emoji", "📦")
    tagline = meta.get("tagline", "")
    year = meta.get("year", 0)
    paradigm = meta.get("paradigm", "")
    ext = meta.get("file_ext", "")
    hw = meta.get("hello_world", "")

    lines = [
        f"  ╔══════════════════════════════════════╗",
        f"  ║  {emoji}  {language:<36}║",
        f"  ╠══════════════════════════════════════╣",
        f"  ║  {tagline:<40}║",
        f"  ║  📅 Since: {year}  |  📁 .{ext:<6}  |  {paradigm:<20}║",
        f"  ╠══════════════════════════════════════╣",
        f"  ║  💻 Hello, World!                    ║",
    ]
    # 分行显示 hello world（每行最多 38 字符）
    for hw_line in hw.split("\n"):
        wrapped = [hw_line[i:i+38] for i in range(0, len(hw_line), 38)]
        for w in wrapped:
            lines.append(f"  ║    {w:<36}║")
    lines.append(f"  ╚══════════════════════════════════════╝")
    return "\n".join(lines)


def get_all_badges(json_path: str = DEFAULT_LANGUAGE_ROTATION_JSON) -> str:
    """
    生成所有语言的徽章文本。
    """
    data = _read_rotation_json(json_path)
    languages = data["languages"]
    separator = "\n" + "  " + "─" * 42 + "\n"
    parts = []
    for lang in languages:
        meta = LANGUAGE_METADATA.get(lang, {})
        parts.append(
            f"{meta.get('emoji', '📦')} **{lang}** — {meta.get('tagline', '')} "
            f"(.{meta.get('file_ext', '')}, {meta.get('year', '')})"
        )
    return ("\n".join(parts))


def get_streak_info(
    json_path: str = DEFAULT_LANGUAGE_ROTATION_JSON,
) -> Dict[str, Any]:
    """
    从 language_rotation.json 中读取 updated_at，
    计算距今的"活跃天数"（每天至少轮换一次视为活跃）。
    """
    data = _read_rotation_json(json_path)
    updated_at_str = data.get("updated_at", "")
    if not updated_at_str:
        return {"streak_days": 0, "last_active": "", "is_active_today": False}

    def _parse_bj_time(s: str):
        """解析北京时间字符串，返回 '今天 YYYY-MM-DD' 的 date 对象"""
        # s 的形式：2026-06-06T02:10:00+08:00
        # +08:00 本身就是北京时间，不需要做加减转换
        s_clean = s.replace("+08:00", "")
        for fmt in ("%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M:%S.%f"):
            try:
                return datetime.strptime(s_clean, fmt)
            except ValueError:
                pass
        raise ValueError(f"无法解析时间: {s}")

    try:
        last_active = _parse_bj_time(updated_at_str)
    except ValueError:
        return {"streak_days": 0, "last_active": updated_at_str, "is_active_today": False}

    # 当前北京时间
    now_utc = datetime.utcnow()
    now_bj = now_utc + timedelta(hours=8)
    today_start_bj = now_bj.replace(hour=0, minute=0, second=0, microsecond=0)
    last_start_bj = last_active.replace(hour=0, minute=0, second=0, microsecond=0)
    days_diff = (today_start_bj - last_start_bj).days

    is_active_today = days_diff == 0

    return {
        "streak_days": days_diff,
        "last_active": updated_at_str,
        "is_active_today": is_active_today,
    }


# CLI 入口
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Polyglot Toolkit — 语言轮换工具")
    sub = parser.add_subparsers(dest="cmd")

    sub.add_parser("rotate", help="轮换到下一个语言并打印徽章")
    sub.add_parser("status", help="查看当前轮换状态")
    sub.add_parser("badges", help="查看所有语言徽章")
    sub.add_parser("streak", help="查看学习连续记录")
    sub.add_parser("badge", help="打印指定语言的徽章").add_argument("language")

    args = parser.parse_args()

    if args.cmd == "rotate":
        result = rotate_and_get_next()
        print(f"\n🌐 当前语言：{result['emoji']} **{result['current_language']}**\n")
        print(get_language_badge(result["current_language"]))
        print(f"\n⏭️  下一个语言：{result['next_language']}")
    elif args.cmd == "status":
        st = get_rotation_status()
        print(f"语言列表：{st['languages']}")
        print(f"当前语言：{st['current_language']} (索引 {st['current_index']}/{st['total'] - 1})")
        print(f"下一个语言：{st['next_language']}")
        print(f"最近一次轮换：{st['updated_at']}")
    elif args.cmd == "badges":
        print(get_all_badges())
    elif args.cmd == "streak":
        st = get_streak_info()
        print(f"连续活跃天数：{st['streak_days']} 天")
        print(f"最近活跃：{st['last_active']}")
        print(f"今日已活跃：{'✅ 是' if st['is_active_today'] else '❌ 否'}")
    elif args.cmd == "badge":
        print(get_language_badge(args.language))
    else:
        parser.print_help()

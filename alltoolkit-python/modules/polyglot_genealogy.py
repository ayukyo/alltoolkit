"""
polyglot_genealogy.py — 编程语言谱系学家 (Polyglot Genealogy)
====================================================================
将编程语言视为有「族谱」的存在：
C++ 的祖先是 C，Rust 的祖先是 ML 和 C，JavaScript 身上流着 Java 的血。
本工具在语言轮换时生成「族谱分析报告」——展示该语言的：
  👨‍👩‍👧 直系祖先（一代）
  👴‍👵 祖先链（三代追溯）
  👶 子嗣与分支（哪些语言继承/影响了它）
  🌳 ASCII 家族树可视化
  🪦 消亡语言（已停用的方言/前辈）

与 language_rotation.json 深度集成：
  1. 读取 language_rotation.json，取出 current_index 所指语言
  2. 查族谱数据库，生成谱系分析报告
  3. 将 current_index 循环前移一位，更新 updated_at
  4. 返回完整报告（祖先链 + ASCII 树 + 亲属关系）

语言轮换顺序（8 种核心语言）：
  Rust → Go → Swift → Kotlin → TypeScript → JavaScript → Java → C/C++ → Rust（循环）

Distinct from existing modules:
  - polyglot_genome:       语言 DNA 序列（基因组成交叉）
  - polyglot_resonator:    语言共振（频率/波形）
  - polyglot_archetype_canvas: 语言原神/命之座
  - polyglot_pulse:        语言脉搏（活跃度追踪）
  - polyglot_sentinel:     学习健康（平衡监测）
  - polyglot_cartographer: 语言生态地图
  - polyglot_ink:          每日墨讯
  - polyglot_quiz:         语言身份猜谜

Polyglot Genealogy 的独特视角：
  不是教你写代码，不是练习题，而是——
  把语言当作有「血脉传承」的生命体。
  当你学习 Rust 时，你的基因里写着 ML 的函数式血脉 + C 的系统级灵魂。
  了解祖先，才能理解语言的设计哲学为何如此。

作者：AllToolkit 全自动生成
依赖：仅 Python 标准库（json, datetime, pathlib）
====================================================================
"""

import json
import os
import sys
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
# 语言谱系数据库
# ─────────────────────────────────────────────

GENEALOGY_DB: Dict[str, Dict[str, Any]] = {
    "Rust": {
        "year": 2015,
        "death_year": None,
        "ancestors": ["ML", "C"],
        "philosophy": "内存安全 + 零成本抽象 + 并发安全，三位一体",
        "quote": "如果它编译了，它就是对的。",
        "famous_quote_author": "Graydon Hoare (Rust 之父)",
        "descendants": [],
        "sibling_influence": ["Haskell", "Erlang"],
        "notable_facts": [
            "名字灵感来自「锈菌」（rust fungi），一种顽强生存的真菌",
            "Mozilla 内部项目出身，编译器由 LLVM 驱动",
            "连续多年获评 '最受开发者喜爱的语言' (Stack Overflow Survey)",
        ],
    },
    "Go": {
        "year": 2009,
        "death_year": None,
        "ancestors": ["C", "Pascal", "CSP"],
        "philosophy": "简洁、务实、编译快、goroutine 并发",
        "quote": "不要通过共享内存通信，要通过通信共享内存。",
        "famous_quote_author": "Rob Pike (Go 之父)",
        "descendants": ["Go+", "Gleam"],
        "sibling_influence": ["Alef", "Limbo"],
        "notable_facts": [
            "三位父亲：Rob Pike、Ken Thompson、Robert Griesemer",
            "最初叫 'Wolfram'，第二个名字是 'Cox'（借鉴 Go+Channel 的梗）",
            "goroutine 一词创造者 Rob Pike 原话：'goroutine 是与其他函数并发运行的函数'",
        ],
    },
    "Swift": {
        "year": 2014,
        "death_year": None,
        "ancestors": ["Objective-C", "Rust", "Haskell", "C#"],
        "philosophy": "安全、快速、表达力强、现代感十足",
        "quote": "Anyone who writes software should read Swift.",
        "famous_quote_author": "Chris Lattner (Swift 之父)",
        "descendants": ["SwiftUI", "Swift Package Manager modules"],
        "sibling_influence": ["D语言", "Objective-C"],
        "notable_facts": [
            "Chris Lattner 在开发 Swift 前是 LLVM 编译器基础设施的核心贡献者",
            "Swift 1.0 发布时，所有 iOS/Mac 开发者都可以免费使用",
            "从 Objective-C 的 '遗老' 风格一跃成为现代语言的标杆",
        ],
    },
    "Kotlin": {
        "year": 2011,
        "death_year": None,
        "ancestors": ["Java", "Scala", "Groovy", "C#"],
        "philosophy": "更简洁的空安全 + 协程 + JVM 生态共享",
        "quote": "Better language for Android and JVM. 且不止于 JVM。",
        "famous_quote_author": "JetBrains 团队 (Kotlin 缔造者)",
        "descendants": ["Kotlin Multiplatform", "Kotlin Script"],
        "sibling_influence": ["Scala", "Xtend"],
        "notable_facts": [
            "名字来自 Kotlin 岛——圣彼得堡附近的一个小岛",
            "最初目标是解决 Java 的语法冗长，没有要取代 Java",
            "JetBrains 花了数年时间让 Kotlin 和 Java 100% 互操作",
        ],
    },
    "TypeScript": {
        "year": 2012,
        "death_year": None,
        "ancestors": ["JavaScript", "Java", "C#"],
        "philosophy": "JavaScript that scales — 编译时类型安全 + 最新 ES 特性",
        "quote": "如果它编译了，它大概率是对的。",
        "famous_quote_author": "Anders Hejlsberg (TypeScript 之父 / C# 之父)",
        "descendants": ["TSX", "Deno", "Bun"],
        "sibling_influence": ["CoffeeScript", "PureScript", "Elm"],
        "notable_facts": [
            "Anders Hejlsberg 同时是 Turbo Pascal、Delphi、C# 和 TypeScript 的设计者",
            "最初内部代号是 'JavaScript 2.0'",
            "Google 内部早在 Angular 2 就开始大规模使用 TS",
        ],
    },
    "JavaScript": {
        "year": 1995,
        "death_year": None,
        "ancestors": ["Scheme", "Self", "Java"],
        "philosophy": "世界最广泛部署的运行时：浏览器就是它的舞台",
        "quote": " Brendan Eich 只用了 10 天就写出了 JavaScript。",
        "famous_quote_author": "Brendan Eich (JavaScript 之父)",
        "descendants": ["TypeScript", "CoffeeScript", "ActionScript", "Dart"],
        "sibling_influence": ["Perl", "Python"],
        "notable_facts": [
            "最初叫 Mocha → LiveScript → 最终因 Java 授权改名 JavaScript",
            "Java 和 JavaScript 的关系：就像 car 和 carpet 的关系",
            "Node.js 让 JavaScript 进入服务器端，开启全栈时代",
        ],
    },
    "Java": {
        "year": 1995,
        "death_year": None,
        "ancestors": ["C++", "Objective-C", "Ada"],
        "philosophy": "一次编写，到处运行 — JVM 虚拟机是核心资产",
        "quote": "Write once, run anywhere.",
        "famous_quote_author": "James Gosling (Java 之父)",
        "descendants": ["Kotlin", "Scala", "Groovy", "Clojure"],
        "sibling_influence": ["Oak (Java 原名)"],
        "notable_facts": [
            "最初叫 Oak（橡树），因为 Gosling 办公室窗外有一棵橡树",
            "改名 Java 是因为 Oak 是注册商标，只好用 Java 咖啡豆的名字",
            "Duke 是 Java 的吉祥物，就是那个咖啡杯",
        ],
    },
    "C/C++": {
        "year": 1983,
        "death_year": None,
        "ancestors": ["C", "Simula", "Algol"],
        "philosophy": "接近硬件，零抽象代价，最大性能，完全控制",
        "quote": "C++ 的问题在于它给了你所有这些锤子，却没有告诉你什么时候该放下。",
        "famous_quote_author": "Bjarne Stroustrup (C++ 之父)",
        "descendants": ["Java", "C#", "Objective-C", "Perl", "Python"],
        "sibling_influence": ["Ada", "BCPL"],
        "notable_facts": [
            "最初叫 'C with Classes'，1983 年正式改名为 C++",
            "C++ 的 ++ 是 C 的自增操作符，意思是 'C 的进化'",
            "标准库（STL）到 C++98 才引入，是 C++ 最强大的部分之一",
        ],
    },
    "C": {
        "year": 1972,
        "death_year": None,
        "ancestors": ["B", "BCPL", "Algol"],
        "philosophy": "close to the metal — 硬件之上的抽象，最小语言内核",
        "quote": "C is a razor blade — sharp and dangerous, but powerful in the right hands.",
        "famous_quote_author": "Dennis Ritchie (C 之父)",
        "descendants": ["C++", "Objective-C", "Java", "C#", "JavaScript", "Go", "Rust", "Perl", "Python"],
        "sibling_influence": [],
        "notable_facts": [
            "Dennis Ritchie 创造，用于重写 Unix，从此操作系统走进现代",
            "K&R 的 C 语言书是计算机史上最有影响力的书籍之一",
            "Linux 内核、Git、Redis 等都是用 C 写的",
        ],
    },
    "Haskell": {
        "year": 1990,
        "death_year": None,
        "ancestors": ["ML", "Miranda"],
        "philosophy": "纯函数式、惰性求值、强类型系统 — 学术语言的骄傲",
        "quote": "Haskell is the most advanced language in the world.",
        "famous_quote_author": "Simon Peyton Jones (Haskell 之父)",
        "descendants": ["Rust", "Elm", "PureScript", "Idris"],
        "sibling_influence": [],
        "notable_facts": [
            "至今活跃，Rust 的类型系统和错误处理大量借鉴 Haskell 的设计",
            "Haskell 的 monad 概念影响了几乎所有现代函数式语言",
            "Cardano 区块链的智能合约语言 Plutus 就是 Haskell",
        ],
    },
}

# 消亡语言（已停止维护或被取代的语言）
EXTINCT_LANGUAGES: Dict[str, Dict[str, Any]] = {
    "Pascal": {
        "year": 1970,
        "death_year": 1995,
        "ancestors": ["Algol"],
        "descendants": ["Delphi", "Object Pascal"],
        "philosophy": "结构化编程入门语言，曾是计算机教育主流",
        "notable_fact": "Niklaus Wirth 设计，名字来自 Blaise Pascal。Delphi (Object Pascal) 是其最后的主要后裔。",
    },
    "Objective-C": {
        "year": 1983,
        "death_year": 2014,
        "ancestors": ["C", "Smalltalk"],
        "descendants": ["Swift"],
        "philosophy": "C 的系统级能力 + Smalltalk 的消息传递 OO 模型",
        "notable_fact": "Steve Neally 和 Brad Cox 创造，乔布斯离开苹果后创立 NeXT 时带走了它，macOS/iOS 的 Cocoa 框架用它写了 20 年。Swift 发布后逐渐退场。",
    },
    "Perl": {
        "year": 1987,
        "death_year": 2019,
        "ancestors": ["C", "Sed", "Awk", "Shell"],
        "descendants": ["Raku (Perl 6)"],
        "philosophy": "There's more than one way to do it (TMTOWTDI) — 灵活到失控",
        "notable_fact": "Larry Wall 创造，RNA 生物学背景用到了语言设计中（正则表达式）。2019 年 Perl 5 停止活跃开发，Raku 接过衣钵。",
    },
    "Ada": {
        "year": 1980,
        "death_year": 2012,
        "ancestors": ["Pascal", "Algol"],
        "descendants": ["SPARK"],
        "philosophy": "美国军方资助，高可靠性嵌入式系统专用语言",
        "notable_fact": "名字来自 Ada Lovelace（人类第一位程序员）。2012 年最后更新，被 SPARK（形式化验证子集）继承。",
    },
    "Simula": {
        "year": 1967,
        "death_year": 1977,
        "ancestors": ["Algol"],
        "descendants": ["Smalltalk", "C++", "Objective-C"],
        "philosophy": "第一个面向对象语言（Simula I 和 Simula 67），OO 之父",
        "notable_fact": "Ole-Johan Dahl 和 Kristen Nygaard 在挪威创造，是 Smalltalk 和 C++ 的祖先。OO 的 class、inheritance、coroutine 概念全部诞生于此。",
    },
    "ML": {
        "year": 1973,
        "death_year": 2002,
        "ancestors": ["ISWIM"],
        "descendants": ["Rust", "Haskell", "OCaml", "F#", "Scala"],
        "philosophy": "函数式 + 类型推导 + 模式匹配，学术与工程的桥梁",
        "notable_fact": "Robin Milner 创造。Haskell、Scala、OCaml、Rust 的祖先。Standard ML 于 2002 年停止维护，但 OCaml 接过火炬。",
    },
    "Smalltalk": {
        "year": 1972,
        "death_year": 2001,
        "ancestors": ["Simula", "Logo"],
        "descendants": ["Objective-C", "Ruby", "Python", "Dart"],
        "philosophy": "纯 OO：一切皆对象，对象通过消息通信",
        "notable_fact": "Alan Kay 创造，OO 之父，真正的 '未来语言'。iOS/Android 的 OO 哲学全部来自 Smalltalk。Python 和 Ruby 直接继承其消息传递模型。",
    },
    "Algol": {
        "year": 1958,
        "death_year": 1972,
        "ancestors": [],
        "descendants": ["Pascal", "C", "Simula", "Ada", "C++"],
        "philosophy": "算法语言 — 为表达算法而生的设计语言",
        "notable_fact": "影响了 C、Pascal、Simula、Ada 的诞生。if/else、for、while 语法几乎全部来自 Algol。几乎所有现代语言的 Control Flow 都流着 Algol 的血。",
    },
}


# ─────────────────────────────────────────────
# 核心 API
# ─────────────────────────────────────────────

def _read_json(json_path: str) -> Dict[str, Any]:
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)


def _write_json(json_path: str, data: Dict[str, Any]) -> None:
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# ─────────────────────────────────────────────
# 谱系查询
# ─────────────────────────────────────────────

def get_language_info(language: str) -> Dict[str, Any]:
    """查询指定语言的谱系信息。"""
    if language in GENEALOGY_DB:
        return {
            "status": "active",
            "language": language,
            **GENEALOGY_DB[language],
        }
    elif language in EXTINCT_LANGUAGES:
        return {
            "status": "extinct",
            "language": language,
            **EXTINCT_LANGUAGES[language],
        }
    else:
        return {
            "status": "unknown",
            "language": language,
            "ancestors": [],
            "descendants": [],
        }


def get_ancestor_chain(language: str, depth: int = 3) -> List[Dict[str, Any]]:
    """
    向上追溯祖先链（最多 depth 代）。
    Returns: [{"language": str, "year": int, "status": str}, ...]
    """
    chain = []
    current = language
    visited = set()
    for _ in range(depth):
        if current in visited:
            break
        visited.add(current)
        info = get_language_info(current)
        ancestors = info.get("ancestors", [])
        if not ancestors:
            break
        parent = ancestors[0]  # 取最直接的祖先
        parent_info = get_language_info(parent)
        chain.append({
            "language": parent,
            "year": parent_info.get("year", 0),
            "status": parent_info.get("status", "unknown"),
            "philosophy": parent_info.get("philosophy", ""),
        })
        current = parent
    return chain


def get_descendants(language: str) -> List[Dict[str, Any]]:
    """
    查询某语言的所有后裔（递归向下）。
    Returns: [{"language": str, "year": int, "status": str}, ...]
    """
    result = []
    queue = list(get_language_info(language).get("descendants", []))
    visited = set()
    while queue:
        lang = queue.pop(0)
        if lang in visited:
            continue
        visited.add(lang)
        info = get_language_info(lang)
        if info["status"] != "unknown":
            result.append({
                "language": lang,
                "year": info.get("year", 0),
                "status": info["status"],
                "philosophy": info.get("philosophy", ""),
            })
            queue.extend(info.get("descendants", []))
    return result


def get_sibling_influence(language: str) -> List[str]:
    """查询某语言的旁系影响（同一祖先的兄弟姐妹语言）。"""
    info = get_language_info(language)
    ancestors = info.get("ancestors", [])
    if not ancestors:
        return []
    primary_ancestor = ancestors[0]
    ancestor_info = get_language_info(primary_ancestor)
    siblings = [
        d for d in ancestor_info.get("descendants", [])
        if d != language
    ]
    return siblings


# ─────────────────────────────────────────────
# ASCII 家族树生成器
# ─────────────────────────────────────────────

def _build_tree_lines(
    language: str,
    visited: set,
    prefix: str = "",
    is_last: bool = True,
) -> List[str]:
    """递归构建 ASCII 树。"""
    info = get_language_info(language)
    emoji = _emoji_for(language)
    year = info.get("year", "?")
    status_mark = _status_mark(info.get("status", "active"))
    lines = []
    connector = "└── " if is_last else "├── "
    lines.append(f"{prefix}{connector}{emoji} {language} ({year}) {status_mark}")
    lines.append(f"{prefix}{'    ' if is_last else '│   '}{info.get('philosophy', '')}")

    descendants = info.get("descendants", [])
    new_prefix = prefix + ("    " if is_last else "│   ")
    for i, child in enumerate(descendants):
        if child in visited:
            continue
        visited.add(child)
        child_is_last = (i == len(descendants) - 1)
        child_lines = _build_tree_lines(child, visited, new_prefix, child_is_last)
        lines.extend(child_lines)
    return lines


def build_family_tree(language):
    """Build ASCII family tree for a programming language."""
    ancestors_result = get_ancestor_chain(language, depth=3)
    descendants_result = get_descendants(language)
    info = get_language_info(language)
    emoji = _emoji_for(language)
    sep = "-" * 56
    equals = "=" * 56
    lines = []

    # Title
    lines.append("")
    lines.append("  +" + equals + "+")
    header = "  |  " + emoji + "  " + language + " - Language Family Tree" + (" " * max(0, 28 - len(language))) + "|"
    lines.append(header)
    lines.append("  +" + equals + "+")

    # Ancestors
    if ancestors_result:
        lines.append("  |  Ancestors (3 generations)" + (" " * 32) + "|")
        total_anc = len(ancestors_result)
        for idx, anc in enumerate(ancestors_result):
            anc_lang = anc["language"]
            anc_year = str(anc["year"])
            anc_stat = _status_mark(anc["status"])
            connector = "+-- " if idx == total_anc - 1 else "|-- "
            lines.append("  |    " + connector + _emoji_for(anc_lang) + " " + anc_lang + " (" + anc_year + ") " + anc_stat)
        lines.append("  +" + sep + "+")

    # Current language
    year_str = str(info.get("year", "?"))
    lines.append("  |  " + emoji + "  " + language + " (" + year_str + ") - YOU ARE HERE")
    phil = info.get("philosophy", "")
    if phil:
        lines.append("  |    " + phil[:60])

    # Quote
    quote = info.get("quote", "")
    quote_author = info.get("famous_quote_author", "")
    if quote and quote_author:
        lines.append("  +" + sep + "+")
        q_trunc = quote[:50]
        lines.append("  |  Quote: \"" + q_trunc + "\"")
        lines.append("  |    -- " + quote_author)

    # Descendants
    if descendants_result:
        lines.append("  +" + sep + "+")
        d_count = str(len(descendants_result))
        lines.append("  |  Descendants (" + d_count + ")")
        for desc in descendants_result[:6]:
            d_lang = desc["language"]
            d_year = str(desc["year"])
            d_stat = _status_mark(desc["status"])
            lines.append("  |    +-- " + _emoji_for(d_lang) + " " + d_lang + " (" + d_year + ") " + d_stat)
        if len(descendants_result) > 6:
            lines.append("  |    ... and " + str(len(descendants_result) - 6) + " more")

    # Siblings
    siblings_result = get_sibling_influence(language)
    if siblings_result:
        lines.append("  +" + sep + "+")
        lines.append("  |  Sibling languages (same ancestor)")
        sib_names = ", ".join(siblings_result[:6])
        lines.append("  |    " + sib_names)

    # Notable facts
    facts = info.get("notable_facts", [])
    if facts:
        lines.append("  +" + sep + "+")
        lines.append("  |  Fun Facts:")
        for fact in facts[:2]:
            for chunk in [fact[i:i+55] for i in range(0, len(fact), 55)]:
                lines.append("  |    * " + chunk)

    lines.append("  +" + equals + "+")
    return lines


def _emoji_for(language: str) -> str:
    emoji_map = {
        "Rust": "🦀",
        "Go": "🐹",
        "Swift": "🦅",
        "Kotlin": "🟣",
        "TypeScript": "🔷",
        "JavaScript": "🟡",
        "Java": "☕",
        "C/C++": "🔩",
        "C": "🔩",
        "Pascal": "📗",
        "Objective-C": "📱",
        "Perl": "🐪",
        "Haskell": "🎓",
        "Ada": "🏛️",
        "Simula": "🔮",
        "ML": "📐",
        "Smalltalk": "🌱",
        "Algol": "🔢",
        "Ruby": "💎",
        "Python": "🐍",
        "C#": "🎵",
        "OCaml": "🐪",
        "F#": "🎵",
        "Scala": "🎼",
        "Go+": "➕",
        "Gleam": "✨",
        "Dart": "🎯",
        "D": "🔺",
        "Erlang": "📡",
        "Elm": "🌿",
        "PureScript": "🌙",
        "Idris": "⚔️",
        "Raku": "🦋",
        "SPARK": "⭐",
        "Delphi": "🏛️",
        "Object Pascal": "📘",
        "TypeScript": "🔷",
        "TSX": "⚛️",
        "Deno": "🦕",
        "Bun": "🥯",
        "SwiftUI": "🖼️",
        "Kotlin Multiplatform": "🌐",
        "Kotlin Script": "📜",
        "BCPL": "🖥️",
        "B": "🧮",
        "Logo": "🐢",
        "ISWIM": "🏔️",
        "Miranda": "🧙",
        "Scheme": "📜",
        "Self": "🪞",
        "Sed": "📝",
        "Awk": "📊",
        "Shell": "🐚",
        "Cox": "🌊",
        "Wolfram": "🧮",
        "Alef": "✈️",
        "Limbo": "🌑",
        "Xtend": "🔧",
        "CoffeeScript": "☕",
        "ActionScript": "⚡",
        "Groovy": "🎸",
        "Clojure": "🌀",
        "BCPL": "🖥️",
        "Ada": "🏛️",
        "Turbo Pascal": "🚀",
        "BASIC": "📘",
    }
    return emoji_map.get(language, "📦")


def _status_mark(status: str) -> str:
    marks = {
        "active": "✅ 活跃",
        "extinct": "🪦 消亡",
        "unknown": "❓ 未知",
    }
    return marks.get(status, "")


# ─────────────────────────────────────────────
# 轮换 API（与 language_rotation.json 集成）
# ─────────────────────────────────────────────

def rotate_and_get_genealogy(
    json_path: str = DEFAULT_LANGUAGE_ROTATION_JSON,
) -> Dict[str, Any]:
    """
    读取 language_rotation.json，取出 current_index 所指语言，
    生成族谱分析报告，然后循环前进 current_index。

    Returns:
        {
            "current_language": str,
            "next_language": str,
            "genealogy": {
                "info": {...},
                "ancestor_chain": [...],
                "descendants": [...],
                "siblings": [...],
                "tree_lines": [str, ...],
            },
            "rotated_at": str,
        }
    """
    data = _read_json(json_path)
    languages = data["languages"]
    total = len(languages)
    idx = data.get("current_index", 0) % total

    current = languages[idx]
    next_idx = (idx + 1) % total
    next_lang = languages[next_idx]

    # 生成族谱报告
    info = get_language_info(current)
    ancestor_chain = get_ancestor_chain(current, depth=3)
    descendants = get_descendants(current)
    siblings = get_sibling_influence(current)
    tree_lines = build_family_tree(current)

    # 更新 JSON
    data["current_index"] = next_idx
    data["last_language"] = current
    data["updated_at"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00")
    _write_json(json_path, data)

    return {
        "current_language": current,
        "next_language": next_lang,
        "genealogy": {
            "info": info,
            "ancestor_chain": ancestor_chain,
            "descendants": descendants,
            "siblings": siblings,
            "tree_lines": tree_lines,
        },
        "rotated_at": data["updated_at"],
    }


def get_genealogy_preview(
    language: Optional[str] = None,
    json_path: str = DEFAULT_LANGUAGE_ROTATION_JSON,
) -> Dict[str, Any]:
    """
    预览指定语言（或当前轮换语言）的族谱报告（不推进索引）。
    """
    data = _read_json(json_path)
    if language is None:
        languages = data["languages"]
        idx = data.get("current_index", 0) % len(languages)
        language = languages[idx]

    info = get_language_info(language)
    ancestor_chain = get_ancestor_chain(language, depth=3)
    descendants = get_descendants(language)
    siblings = get_sibling_influence(language)
    tree_lines = build_family_tree(language)

    return {
        "current_language": language,
        "genealogy": {
            "info": info,
            "ancestor_chain": ancestor_chain,
            "descendants": descendants,
            "siblings": siblings,
            "tree_lines": tree_lines,
        },
    }


# ─────────────────────────────────────────────
# 格式化输出
# ─────────────────────────────────────────────

def format_genealogy_console(result: Dict[str, Any]) -> str:
    """将族谱报告格式化为控制台输出。"""
    lines = result["genealogy"]["tree_lines"]
    next_lang = result.get("next_language", "")
    rotated_at = result.get("rotated_at", "")
    parts = [
        "\n".join(lines),
        f"\n  ⏭️  下一个语言：{next_lang}   rotated at: {rotated_at}",
    ]
    return "\n".join(parts)


def format_genealogy_markdown(result: Dict[str, Any]) -> str:
    """将族谱报告格式化为 Markdown。"""
    lang = result["current_language"]
    info = result["genealogy"]["info"]
    ancestors = result["genealogy"]["ancestor_chain"]
    descendants = result["genealogy"]["descendants"]
    siblings = result["genealogy"]["siblings"]

    emoji = _emoji_for(lang)
    parts = [
        f"## 🌳 Polyglot Genealogy — {lang} {emoji}",
        "",
        f"**状态：** {_status_mark(info.get('status', 'unknown'))}",
        f"**诞生年份：** {info.get('year', '?')}",
        f"**设计哲学：** {info.get('philosophy', '')}",
        "",
        f"**💬 名言：** \"{info.get('quote', '')}\"",
        f"— {info.get('famous_quote_author', '')}",
        "",
    ]

    if ancestors:
        parts.append("### 👴 祖先链（三代）")
        for anc in ancestors:
            a_emoji = _emoji_for(anc["language"])
            a_status = _status_mark(anc["status"])
            parts.append(f"- {a_emoji} **{anc['language']}** ({anc['year']}) {a_status} — {anc.get('philosophy', '')}")
        parts.append("")

    if descendants:
        parts.append(f"### 👶 直接后裔 ({len(descendants)} 个)")
        for desc in descendants:
            d_emoji = _emoji_for(desc["language"])
            d_status = _status_mark(desc["status"])
            parts.append(f"- {d_emoji} **{desc['language']}** ({desc['year']}) {d_status}")
        parts.append("")

    if siblings:
        parts.append(f"### 👫 旁系同族")
        sib_emoji_list = [_emoji_for(s) for s in siblings]
        parts.append(", ".join(f"{e} {s}" for e, s in zip(sib_emoji_list, siblings)))
        parts.append("")

    facts = info.get("notable_facts", [])
    if facts:
        parts.append("### 🪦 族谱趣闻")
        for fact in facts:
            parts.append(f"- {fact}")
        parts.append("")

    parts.append(f"\n⏭️ **下一个语言：** {result.get('next_language', '')}")
    return "\n".join(parts)


# ─────────────────────────────────────────────
# CLI 入口
# ─────────────────────────────────────────────

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Polyglot Genealogy — 编程语言谱系分析")
    sub = parser.add_subparsers(dest="cmd")

    sub.add_parser("genealogy", help="生成当前语言的族谱报告并轮换")
    sub.add_parser("preview", help="预览当前语言族谱（不轮换）")
    sub.add_parser("info", help="查看指定语言的族谱信息（不轮换）").add_argument("language")
    sub.add_parser("tree", help="查看指定语言的 ASCII 家族树（不轮换）").add_argument("language")

    args = parser.parse_args()

    if args.cmd == "genealogy":
        result = rotate_and_get_genealogy()
        print(format_genealogy_console(result))
    elif args.cmd == "preview":
        result = get_genealogy_preview()
        print(format_genealogy_console({"current_language": result["current_language"], "genealogy": result["genealogy"], "next_language": "", "rotated_at": ""}))
    elif args.cmd == "info":
        info = get_language_info(args.language)
        print(json.dumps(info, indent=2, ensure_ascii=False))
    elif args.cmd == "tree":
        lines = build_family_tree(args.language)
        print("\n".join(lines))
    else:
        parser.print_help()

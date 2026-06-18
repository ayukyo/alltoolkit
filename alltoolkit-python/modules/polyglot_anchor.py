"""
polyglot_anchor.py — 编程语言锚定仪式 (Polyglot Anchor)
====================================================================
一个与 language_rotation.json 深度集成的学习专注力锚定生成器。

核心理念：每一种语言都有独特的「思维节奏」和学习仪式。
Polyglot Anchor 在你开始学习每种语言之前，
生成一个专属的「专注锚」——包含：

  🧘 呼吸节奏：语言特有的思维呼吸模式（吸气/呼气时长比）
  🗺️ 心理地图：进入该语言思维模式的引导步骤
  📿 锚定口令：一句话咒语，激活该语言的思维回路
  🌅 晨间仪式：适合该语言的经典开篇练习
  🧩 专注图腾：该语言最标志性代码片段作为视觉锚点

核心逻辑：
  1. 读取 language_rotation.json，按 current_index 取当前轮换语言
  2. 根据语言特质生成个性化的「专注锚」
  3. 完成后将 current_index 前移一位并更新 updated_at

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
  - polyglot_sentinel:     学习健康监测（监测 + 警报）
  - polyglot_resonator:    语言共鸣频率

Polyglot Anchor 的独特视角：
  不是生成内容，不是监测健康，
  而是创造一个「进入该语言思维模式」的认知锚点。
  每次切换语言时，用一个仪式感强烈的专注锚，
  帮助大脑快速切换到该语言的思维范式。

作者：AllToolkit 全自动生成
依赖：仅 Python 标准库（json, datetime, pathlib, random）
====================================================================
"""

import json
import os
import random
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

# ─────────────────────────────────────────────
# 路径配置
# ─────────────────────────────────────────────
_MODULE_DIR = Path(__file__).parent.parent              # alltoolkit-python/
_WORKSPACE_ROOT = _MODULE_DIR.parent                    # workspace/
DEFAULT_LANGUAGE_ROTATION_JSON = str(_WORKSPACE_ROOT / "language_rotation.json")

# 固定的 8 种核心语言
CORE_LANGUAGES: List[str] = [
    "Rust", "Go", "Swift", "Kotlin",
    "TypeScript", "JavaScript", "Java", "C/C++",
]

LANGUAGE_EMOJI: Dict[str, str] = {
    "Rust": "🦀", "Go": "🐹", "Swift": "🦅", "Kotlin": "🟣",
    "TypeScript": "🔷", "JavaScript": "🟡", "Java": "☕", "C/C++": "🔩",
}


# ─────────────────────────────────────────────
# 锚定数据库
# ─────────────────────────────────────────────

ANCHOR_DB: Dict[str, Dict[str, Any]] = {
    "Rust": {
        "breath": {"inhale": 4, "hold": 7, "exhale": 8, "pattern": "4-7-8 镇静呼吸"},
        "mindset": [
            "所有权是你的朋友，不是敌人",
            "编译器是最严格的老师，倾听它的每一个抱怨",
            "借用检查器在保护你，让它引导你",
            "每一个值都有明确的生命周期，明确它",
        ],
        "mantra": "🦀 借我力量，护我边界（Borrow with grace, own with care）",
        "ritual": "在 Rust Playground 写一个带所有权转移的小程序，感受 'move' 的力量",
        "totem_code": """fn main() {
    let s1 = String::from("hello");
    let s2 = s1; // s1 移动到 s2
    // println!("{}", s1); // 编译错误！s1 已无效
    println!("{}", s2); // ✓ s2 拥有所有权
}""",
        "focus_word": "所有权 · 生命周期 · 借用检查",
        "energy_tip": "Rust 学习需要深度专注，建议在安静时段进行",
    },
    "Go": {
        "breath": {"inhale": 3, "hold": 0, "exhale": 3, "pattern": "3-0-3 对称呼吸"},
        "mindset": [
            "简单是 Go 的哲学，拒绝过度设计",
            "goroutine 是轻量级的，不要害怕并发",
            "channel 是 goroutine 之间的桥梁，善用它",
            "错误处理要显式，不要忽略它",
        ],
        "mantra": "🐹 保持简单，并发天生（Keep it simple, concurrency is natural）",
        "ritual": "用 go run 跑一个 hello world，感受 goroutine 的轻盈",
        "totem_code": """package main

import "fmt"

func main() {
    ch := make(chan string)

    go func() {
        ch <- "Hello from goroutine!"
    }()

    msg := <-ch
    fmt.Println(msg)
}""",
        "focus_word": "简洁 · 并发 · 组合性",
        "energy_tip": "Go 鼓励边想边写，不要过度准备",
    },
    "Swift": {
        "breath": {"inhale": 4, "hold": 4, "exhale": 6, "pattern": "4-4-6 平衡呼吸"},
        "mindset": [
            "类型安全是一种承诺，Swift 在乎你的承诺",
            "协议是行为的契约，遵循它而不是继承它",
            "Optional 是安全的边界，拥抱它而不是逃避它",
            "值类型和引用类型有不同的生命哲学，了解它们的边界",
        ],
        "mantra": "🦅 类型安全，协议至上（Types bind, protocols guide）",
        "ritual": "在 Xcode Playground 写一个 Optional 链式解包，感受 ?. 的优雅",
        "totem_code": """let scores: [String: Int?] = [
    "Alice": 98,
    "Bob": nil,
    "Carol": 100,
]

for (name, score) in scores {
    // Optional 绑定，安全解包
    if let s = score {
        print("\\(name): \\(s)")
    } else {
        print("\\(name): 未评分")
    }
}""",
        "focus_word": "类型安全 · 协议扩展 · Optional",
        "energy_tip": "Swift 学习需要感受 Apple 生态的设计美学",
    },
    "Kotlin": {
        "breath": {"inhale": 4, "hold": 4, "exhale": 6, "pattern": "4-4-6 协同呼吸"},
        "mindset": [
            "协程是非阻塞的思维，但代码是顺序的",
            "扩展函数是你给已有类型添加超能力的方式",
            "数据类是不可变思维的体现，优先使用它",
            "null 安全是 Kotlin 的核心承诺，不要绕过它",
        ],
        "mantra": "🟣 协程异步，扩展无限（Coroutines async, extensions endless）",
        "ritual": "写一个 suspend 函数，用 runBlocking 感受协程的协作式调度",
        "totem_code": """import kotlinx.coroutines.*

fun main() = runBlocking {
    val job = launch {
        delay(100L)
        println("World!")
    }
    print("Hello, ")
    job.join()
    println("Done!")
}""",
        "focus_word": "协程 · 扩展函数 · 空安全",
        "energy_tip": "Kotlin 的空安全值得用小例子反复体会",
    },
    "TypeScript": {
        "breath": {"inhale": 4, "hold": 3, "exhale": 5, "pattern": "4-3-5 类型呼吸"},
        "mindset": [
            "类型是你的文档，也是你的测试",
            "泛型是类型的抽象，不要写重复的类型",
            "keyof 和 typeof 是类型层面的反射",
            "用条件类型写出编译期逻辑，感受类型的力量",
        ],
        "mantra": "🔷 类型即契约，泛型为桥梁（Types contract, generics bridge）",
        "ritual": "手写一个工具类型（如 DeepPartial），理解 TypeScript 类型系统的深度",
        "totem_code": """type DeepPartial<T> = {
    [P in keyof T]?: T[P] extends object
        ? DeepPartial<T[P]>
        : T[P]
}

// 使用示例
interface User {
    name: string;
    address: { city: string; zip: number };
}

type PartialUser = DeepPartial<User>;
// { name?: string; address?: { city?: string; zip?: number } }""",
        "focus_word": "类型系统 · 泛型约束 · 工具类型",
        "energy_tip": "TypeScript 的类型体操适合在早晨进行，头脑清醒时效果最佳",
    },
    "JavaScript": {
        "breath": {"inhale": 3, "hold": 0, "exhale": 3, "pattern": "3-0-3 即时呼吸"},
        "mindset": [
            "事件循环是 JavaScript 的心脏，理解它就理解了一切",
            "Promise 是异步的承诺，then/catch/finally 是它的三部曲",
            "闭包是记忆的容器，记住它捕获的是变量的引用",
            "原型链是 JavaScript 的遗产，理解它但不一定要用它",
        ],
        "mantra": "🟡 异步非阻塞，原型自有道（Async not blocking, prototype legacy）",
        "ritual": "手写一个 Promise.all 实现，理解 Promise 的内部状态机",
        "totem_code": """// 手写 Promise.all
function promiseAll(promises) {
    return new Promise((resolve, reject) => {
        const results = [];
        let settled = 0;

        promises.forEach((p, i) => {
            Promise.resolve(p)
                .then(val => {
                    results[i] = val;
                    settled++;
                    if (settled === promises.length) resolve(results);
                })
                .catch(reject);
        });
    });
}""",
        "focus_word": "事件循环 · Promise · 闭包 · 原型",
        "energy_tip": "JavaScript 适合碎片化学习，随时写一小段感受即时反馈",
    },
    "Java": {
        "breath": {"inhale": 5, "hold": 3, "exhale": 5, "pattern": "5-3-5 JVM 呼吸"},
        "mindset": [
            "一切皆对象，类是世界的蓝图",
            "JVM 是你的运行时舞台，理解它的 GC 分代模型",
            "Stream API 是函数式的入口，拥抱它",
            "接口是行为的契约，优先面向接口编程",
        ],
        "mantra": "☕ 一切皆对象，JVM 为舞台（All is object, JVM is stage）",
        "ritual": "用 Stream API 重写一个 for 循环，感受函数式的优雅",
        "totem_code": """import java.util.*;
import java.util.stream.*;

List<String> names = Arrays.asList("Alice", "Bob", "Charlie");

List<String> result = names.stream()
    .filter(name -> name.length() > 3)
    .map(String::toUpperCase)
    .sorted()
    .collect(Collectors.toList());

System.out.println(result); // [ALICE, CHARLIE]""",
        "focus_word": "面向对象 · Stream API · JVM",
        "energy_tip": "Java 适合系统性学习，一个模块一个模块地攻破",
    },
    "C/C++": {
        "breath": {"inhale": 6, "hold": 4, "exhale": 8, "pattern": "6-4-8 深度呼吸"},
        "mindset": [
            "指针是地址，地址是力量，但要谨慎",
            "内存管理是你的责任，RAII 是你的守护者",
            "模板是编译期的超能力，谨慎使用",
            "C/C++ 给你最大的控制权，也给你最大的责任",
        ],
        "mantra": "🔩 内存在手，责任在心（Memory in hand, responsibility in heart）",
        "ritual": "用 RAII 模式实现一个线程安全的资源包装器，感受 C++ 的安全网",
        "totem_code": """#include <mutex>
#include <iostream>

class SafeCounter {
    std::mutex mtx_;
    int count = 0;
public:
    void incr() {
        std::lock_guard<std::mutex> lock(mtx_);
        ++count;
    }
    int get() const {
        std::lock_guard<std::mutex> lock(mtx_);
        return count;
    }
};""",
        "focus_word": "指针 · RAII · 模板 · 内存管理",
        "energy_tip": "C/C++ 是最底层的语言，建议在精力最充沛的时段学习",
    },
}


# ─────────────────────────────────────────────
# 内部工具函数
# ─────────────────────────────────────────────

def _read_json(json_path: str) -> Dict[str, Any]:
    if not os.path.exists(json_path):
        return {}
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}


def _write_json(json_path: str, data: Dict[str, Any]) -> None:
    tmp = json_path + ".anchor_tmp"
    try:
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        os.replace(tmp, json_path)
    except IOError:
        pass


# ─────────────────────────────────────────────
# 核心 API
# ─────────────────────────────────────────────

def get_anchor(
    json_path: str = DEFAULT_LANGUAGE_ROTATION_JSON,
    seed: Optional[int] = None,
) -> Dict[str, Any]:
    """
    获取当前轮换语言的专注锚。

    流程：
      1. 读取 language_rotation.json，取 current_index 所指语言
      2. 根据语言从 ANCHOR_DB 读取锚定数据
      3. 随机选择一条 mindset（随机种子可选）
      4. 将 current_index 前移一位并更新 updated_at
      5. 返回完整的锚字典

    Returns:
        {
            "language": str,
            "emoji": str,
            "breath": {inhale: int, hold: int, exhale: int, pattern: str},
            "mindset": [str, ...],       # 完整列表
            "mantra": str,
            "ritual": str,
            "totem_code": str,
            "focus_word": str,
            "energy_tip": str,
            "anchor_index": int,          # 在 CORE_LANGUAGES 中的位置
            "next_language": str,
        }
    """
    data = _read_json(json_path)
    languages = data.get("languages", CORE_LANGUAGES)
    total = len(languages)
    idx = data.get("current_index", 0) % total
    current = languages[idx]

    anchor = ANCHOR_DB.get(current, ANCHOR_DB.get("JavaScript"))  # 兜底

    rng = random.Random(seed)
    # 从完整 mindset 列表中随机选择一条作为 active_focus
    all_mindsets = anchor["mindset"]
    active_mindset = rng.choice(all_mindsets)

    # 更新 language_rotation.json
    next_idx = (idx + 1) % total
    data["current_index"] = next_idx
    data["last_language"] = current
    data["updated_at"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00")
    _write_json(json_path, data)

    return {
        "language": current,
        "emoji": LANGUAGE_EMOJI.get(current, "📦"),
        "breath": anchor["breath"],
        "mindset": all_mindsets,           # 完整列表
        "active_mindset": active_mindset,   # 随机选中的专注点
        "mantra": anchor["mantra"],
        "ritual": anchor["ritual"],
        "totem_code": anchor["totem_code"],
        "focus_word": anchor["focus_word"],
        "energy_tip": anchor["energy_tip"],
        "anchor_index": idx,
        "next_language": languages[next_idx],
    }


def get_anchor_preview(
    json_path: str = DEFAULT_LANGUAGE_ROTATION_JSON,
) -> Dict[str, Any]:
    """
    查询当前语言的锚定信息（不推进索引）。
    """
    data = _read_json(json_path)
    languages = data.get("languages", CORE_LANGUAGES)
    total = len(languages)
    idx = data.get("current_index", 0) % total
    current = languages[idx]

    anchor = ANCHOR_DB.get(current, ANCHOR_DB.get("JavaScript"))
    return {
        "language": current,
        "emoji": LANGUAGE_EMOJI.get(current, "📦"),
        "breath": anchor["breath"],
        "mantra": anchor["mantra"],
        "focus_word": anchor["focus_word"],
        "anchor_index": idx,
        "next_language": languages[(idx + 1) % total],
    }


def format_anchor_console(anchor: Dict[str, Any]) -> str:
    """
    将锚定信息格式化为 ASCII 控制台展示。
    """
    breath = anchor["breath"]
    lines = [
        "  ╔══════════════════════════════════════════════════════════╗",
        "  ║  ⚓ Polyglot Anchor — 专注锚定仪式                      ║",
        "  ╠══════════════════════════════════════════════════════════╣",
        f"  ║  {anchor['emoji']}  {anchor['language']:<12} 专注锚                      ║",
        f"  ║  ⏭️  下个语言：{anchor['next_language']:<46}║",
        "  ╠══════════════════════════════════════════════════════════╣",
        "  ║  🫁 呼吸节奏                                            ║",
        f"  ║    {breath['pattern']}                         ║",
        f"  ║    吸气 {breath['inhale']} 秒 → 屏息 {breath['hold']} 秒 → 呼气 {breath['exhale']} 秒        ║",
        "  ╠══════════════════════════════════════════════════════════╣",
        "  ║  🧠 专注思维                                            ║",
        f"  ║    {anchor['active_mindset']:<57}║",
        "  ╠══════════════════════════════════════════════════════════╣",
        "  ║  📿 锚定口令                                            ║",
        f"  ║    {anchor['mantra']:<57}║",
        "  ╠══════════════════════════════════════════════════════════╣",
        "  ║  🌅 晨间仪式                                            ║",
        f"  ║    {anchor['ritual']:<57}║",
        "  ╠══════════════════════════════════════════════════════════╣",
        "  ║  🧩 专注图腾（标志代码片段）                            ║",
    ]

    # 代码片段（每行最多 54 字符）
    for code_line in anchor["totem_code"].split("\n"):
        wrapped = [code_line[i:i+54] for i in range(0, len(code_line), 54)]
        for w in wrapped:
            lines.append(f"  ║    {w:<57}║")

    lines += [
        "  ╠══════════════════════════════════════════════════════════╣",
        "  ║  🎯 专注关键词                                          ║",
        f"  ║    {anchor['focus_word']:<57}║",
        "  ╠══════════════════════════════════════════════════════════╣",
        "  ║  ⚡ 能量提示                                            ║",
        f"  ║    {anchor['energy_tip']:<57}║",
        "  ╠══════════════════════════════════════════════════════════╣",
        "  ║  🧘 完整思维清单                                        ║",
    ]
    for ms in anchor["mindset"]:
        if len(ms) > 54:
            ms = ms[:51] + "..."
        lines.append(f"  ║    • {ms:<55}║")

    lines.append("  ╚══════════════════════════════════════════════════════════╝")
    return "\n".join(lines)


def format_anchor_markdown(anchor: Dict[str, Any]) -> str:
    """
    将锚定信息格式化为 Markdown。
    """
    breath = anchor["breath"]
    lines = [
        f"## ⚓ Polyglot Anchor — {anchor['language']} 专注锚定仪式",
        "",
        f"**语言**：{anchor['emoji']} {anchor['language']}",
        f"**下一个**：{anchor['next_language']}",
        "",
        "### 🫁 呼吸节奏",
        f"- 模式：{breath['pattern']}",
        f"- 吸气 {breath['inhale']}s → 屏息 {breath['hold']}s → 呼气 {breath['exhale']}s",
        "",
        "### 🧠 专注思维",
        f"> {anchor['active_mindset']}",
        "",
        "### 📿 锚定口令",
        f"> *{anchor['mantra']}*",
        "",
        "### 🌅 晨间仪式",
        f"- {anchor['ritual']}",
        "",
        "### 🧩 专注图腾",
        "```" + anchor["language"].lower().replace("/", "") + "\n" + anchor["totem_code"] + "\n```",
        "",
        "### 🎯 专注关键词",
        f"- *{anchor['focus_word']}*",
        "",
        "### ⚡ 能量提示",
        f"- {anchor['energy_tip']}",
        "",
        "### 🧘 完整思维清单",
    ]
    for ms in anchor["mindset"]:
        lines.append(f"- {ms}")

    return "\n".join(lines)


# ─────────────────────────────────────────────
# CLI 入口
# ─────────────────────────────────────────────

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Polyglot Anchor — 专注锚定仪式")
    sub = parser.add_subparsers(dest="cmd")

    sub.add_parser("anchor", help="获取当前语言的专注锚（推进轮换）")
    sub.add_parser("preview", help="预览当前语言锚定信息（不推进）")
    sub.add_parser("breathe", help="仅显示呼吸节奏")

    args = parser.parse_args()

    if args.cmd == "anchor":
        result = get_anchor()
        print(format_anchor_console(result))
    elif args.cmd == "preview":
        result = get_anchor_preview()
        print(f"{result['emoji']} {result['language']} | 专注词：{result['focus_word']}")
        print(f"  呼吸：{result['breath']['pattern']}")
        print(f"  口令：{result['mantra']}")
    elif args.cmd == "breathe":
        result = get_anchor_preview()
        breath = result["breath"]
        print(f"呼吸节奏练习（{result['language']}）：")
        print(f"  吸气 {breath['inhale']} 秒")
        print(f"  屏息 {breath['hold']} 秒")
        print(f"  呼气 {breath['exhale']} 秒")
        print(f"  重复 4 次，感受 {result['language']} 的思维节奏")
    else:
        parser.print_help()


# 兼容性别名
rotate_and_get_anchor = get_anchor
get_anchor_preview_alias = get_anchor_preview

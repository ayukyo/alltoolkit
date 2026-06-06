"""
Polyglot Ink — 多语言每日墨讯 (Daily Language Briefing)

按 language_rotation.json 的轮换顺序，每次为当前语言生成一份
每日墨讯：语言界谚语、今日能量、项目推荐、趣闻、惯用法代码片。

创意概念："每种语言都有它的墨迹 — 每日一则，让你贴近它的思维方式。"

Distinct from existing tools:
  - kata_generator:     编程练习挑战（有 starter_code / solution）
  - language_tools:      轮换 + 徽章 + 连击记录
  - polyglot_codex:     每日语言画像（个性 + 生态 + 实战技巧）
  - polyglot_digest:     语法平行视图（多语言同义代码并排）
  - dev_metrics:         代码复杂度分析

Polyglot Ink 的独特视角：每日"语言简报" —
  把语言当作一个有性格、有情绪、有故事的伙伴，
  通过谚语、能量、推荐项目、趣闻、惯用法五个维度，
  每天让你对当前语言多一点"手感"。

旋转顺序：Rust → Go → Swift → Kotlin → TypeScript → JavaScript → Java → C/C++ → Rust（循环）
"""

import json
import os
import random
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

# ── 路径配置 ─────────────────────────────────────────────────────────────────
_MODULE_DIR = Path(__file__).parent.parent
_WORKSPACE_ROOT = _MODULE_DIR.parent
DEFAULT_LANGUAGE_ROTATION_JSON = str(_WORKSPACE_ROOT / "language_rotation.json")

# ── 旋转顺序（9种语言）──────────────────────────────────────────────────────
ROTATION_ORDER: List[str] = [
    "Rust", "Go", "Swift", "Kotlin",
    "TypeScript", "JavaScript", "Java", "C/C++",
]


# ── 每日墨讯数据库 ────────────────────────────────────────────────────────────
# 每种语言包含：
#   proverb         : 语言社区谚语（英文 + 中文翻译）
#   energy_map      : 不同时段的能量描述
#   project_tips    : 适合今天做的项目类型列表
#   trivia          : 有趣的冷知识或社区故事
#   idiom_snippet   : 惯用法代码示例（展示语言独特思维）

INK_DATABASE: Dict[str, Dict[str, Any]] = {
    "Rust": {
        "proverb": {
            "en": "The compiler knows best — fight it and lose.",
            "zh": "编译器永远是对的——硬刚只会输得更惨。",
        },
        "energy_map": {
            "morning":   "🔋 精力充沛，类型系统全速运转，适合攻克复杂的所有权逻辑",
            "afternoon": "🧠 深度专注，Trait 对象和生命周期注释齐飞",
            "evening":   "🌙 静谧沉思，适合阅读他人代码或写文档",
            "night":     "🦀 硬核模式，unsafe 代码只在深夜才安全",
        },
        "project_tips": [
            "实现一个并发 HTTP 服务器（tokio）",
            "写一个自定义错误类型并实现 `From` 转换",
            "用 `Iterator` 实现惰性序列",
            "构建一个 CLI 工具并发布到 crates.io",
        ],
        "trivia": (
            "Rust 的官方 mascot 'Ferris' 是一只可爱的螃蟹。"
            "但你知道吗？Rust 编译器内部昵称违禁词检查器为 'the borrow checker'——"
            "它在所有错误信息里扮演法官角色，平均每天让全球开发者多喝 3 杯咖啡。"
        ),
        "idiom_snippet": {
            "title": "用 ? 运算符优雅传播错误",
            "code": (
                "use std::fs;\n"
                "use std::io;\n\n"
                "fn read_username() -> Result<String, io::Error> {\n"
                "    let f = fs::File::open(\"user.txt\")?;\n"
                "    let mut s = String::new();\n"
                "    f.read_to_string(&mut s)?;\n"
                "    Ok(s)\n"
                "}\n\n"
                "// 比起 match 嵌套，? 让错误传播干净利落"
            ),
        },
    },
    "Go": {
        "proverb": {
            "en": "Don't communicate by sharing memory; share memory by communicating.",
            "zh": "不要通过共享内存来通信，要通过通信来共享内存。",
        },
        "energy_map": {
            "morning":   "☀️ 清新直接，Goroutine 轻装上阵，适合快速原型",
            "afternoon": "🐹 务实下午，error 处理和接口组合",
            "evening":   "🔧 整理模式，整理项目结构或写单元测试",
            "night":     "🌃 部署时间，dockerize 项目或 CI/CD 调优",
        },
        "project_tips": [
            "实现一个 channel-based 生产者-消费者",
            "写一个中间件（middleware）封装日志和认证",
            "构建 RESTful API 并写 Swagger 文档",
            "用 go embed 打包静态资源",
        ],
        "trivia": (
            "Go 的创造者 Rob Pike、Ken Thompson 和 Robert Griesemer "
            "当初设计 Go 时，核心目标之一就是'编译比 Python 跑得还快'。"
            "结果 Go 1.0 诞生时，编译速度真的接近 C 的 10 倍以上，"
            "而语法简洁程度却和脚本语言有得一拼。"
        ),
        "idiom_snippet": {
            "title": "Goroutine + Channel 并发模式",
            "code": (
                "func worker(jobs <-chan int, results chan<- int) {\n"
                "    for j := range jobs {\n"
                "        results <- j * 2\n"
                "    }\n"
                "}\n\n"
                "jobs := make(chan int, 100)\n"
                "results := make(chan int, 100)\n\n"
                "for w := 1; w <= 3; w++ {\n"
                "    go worker(jobs, results)\n"
                "}"
            ),
        },
    },
    "Swift": {
        "proverb": {
            "en": "Swift is like Objective-C, but without the baggage.",
            "zh": "Swift 就是 Objective-C 的灵魂，去掉了历史包袱。",
        },
        "energy_map": {
            "morning":   "🦅 敏捷清晨，Option/Result 处理加 guard let",
            "afternoon": "📱 移动时刻，SwiftUI 或 UIKit 界面搭建",
            "evening":   "🧩 架构时光，Protocol-Oriented Programming",
            "night":     "🌌 深夜创意，Swift Macros 元编程实验",
        },
        "project_tips": [
            "用 SwiftUI 构建一个天气应用 UI",
            "实现一个自定义 Collection 类型",
            "写一个 Result 类型的链式错误处理扩展",
            "探索 Swift Actors 实现并发安全",
        ],
        "trivia": (
            "Swift 的创造者 Chris Lattner 在开发 Swift 之前是 LLVM 编译器的核心贡献者。"
            "所以 Swift 的编译速度和优化能力之所以优秀，某种程度上是因为"
            "它的设计者就是世界上最懂编译器的人之一。"
        ),
        "idiom_snippet": {
            "title": "Protocol-Oriented 扩展 + where 子句",
            "code": (
                "protocol Drawable {\n"
                "    func draw()\n"
                "}\n\n"
                "extension Array where Element: Drawable {\n"
                "    func drawAll() {\n"
                "        forEach { $0.draw() }\n"
                "    }\n"
                "}"
            ),
        },
    },
    "Kotlin": {
        "proverb": {
            "en": "Null safety isn't a feature; it's a lifestyle.",
            "zh": "空安全不是特性，是一种生活方式。",
        },
        "energy_map": {
            "morning":   "🟣 优雅清晨，扩展函数和 DSL 构建",
            "afternoon": "☕ JVM 下午，与 Java 互调或 Spring 集成",
            "evening":   "📱 协程时光，suspend 函数和 Flow",
            "night":     "🔮 泛型深夜，reified 和内联函数",
        },
        "project_tips": [
            "用 Kotlin Coroutines 重构一个异步任务链",
            "构建一个类型安全的 DSL 配置器",
            "实现一个自定义 Scope Function 链",
            "用 Kotlin Scripting 写构建脚本",
        ],
        "trivia": (
            "Kotlin 最初是 JetBrains 为了解决 Java 的冗长问题而内部开发的。"
            "名字来自 Kotlin 岛（圣彼得堡附近的一个小岛），"
            "而团队在命名时还考虑过 'Saturn' 和 'Kotlin' 这两个选项，"
            "前者因为太明显而被否决。"
        ),
        "idiom_snippet": {
            "title": "Scope Functions + 可空安全链",
            "code": (
                "data class Person(val name: String, val city: City?)\n"
                "data class City(val name: String, val country: Country?)\n"
                "data class Country(val code: String)\n\n"
                "val countryCode = person\n"
                "    ?.city\n"
                "    ?.country\n"
                "    ?.code\n"
                "    ?: \"UNKNOWN\""
            ),
        },
    },
    "TypeScript": {
        "proverb": {
            "en": "If it compiles, it probably works — mostly.",
            "zh": "能编译就能跑——大概吧。",
        },
        "energy_map": {
            "morning":   "🔷 类型游戏，泛型约束和 conditional types",
            "afternoon": "⚡ 前端时光，React/Vue 组件 + TS 集成",
            "evening":   "📦 npm 探索，类型定义包发布",
            "night":     "🧙 高级咒语，模板字面量类型和 mapped types",
        },
        "project_tips": [
            "写一个工具库，完整类型声明（export types）",
            "用 TypeScript 实现一个 'deep partial' 工具类型",
            "搭建一个 ESLint 插件（用 TypeScript）",
            "探索 Zod 或 tRPC 做运行时类型校验",
        ],
        "trivia": (
            "TypeScript 最初是微软内部项目，由 Anders Hejlsberg（C# 之父）主导。"
            "最初的名字其实是 'JavaScript 2.0'，后来才改名为 TypeScript，"
            "因为他们觉得这个名字更能体现'带类型的 JavaScript 超集'这一核心价值。"
        ),
        "idiom_snippet": {
            "title": "泛型约束 + infer 条件类型",
            "code": (
                "type DeepReadonly<T> = T extends (infer U)[]\n"
                "    ? ReadonlyArray<DeepReadonly<U>>\n"
                "    : T extends object\n"
                "    ? { readonly [K in keyof T]: DeepReadonly<T[K]> }\n"
                "    : T;\n\n"
                "type X = DeepReadonly<{ a: { b: string[] } }>;\n"
                "// { readonly a: { readonly b: ReadonlyArray<string> } }"
            ),
        },
    },
    "JavaScript": {
        "proverb": {
            "en": "console.log is the new var dump.",
            "zh": "console.log 才是新时代的 var_dump。",
        },
        "energy_map": {
            "morning":   "🟡 活力早晨，ES2024 新特性实验",
            "afternoon": "🌐 前端时光，DOM 操作或 Node.js 脚本",
            "evening":   "⚙️ 工具链傍晚，Vite/Webpack 配置调优",
            "night":     "🌀 异步深渊，Promise 链和 Event Loop 调试",
        },
        "project_tips": [
            "写一个 Node.js CLI 小工具发布到 npm",
            "用 Proxy 实现一个简易响应式系统",
            "探索 BigInt 处理大数运算",
            "用 WebAssembly 包装一个 C 函数",
        ],
        "trivia": (
            "JavaScript 最初叫 Mocha，然后改名为 LiveScript，"
            "最后因为和 SUN 的 Java 品牌授权协议，才改名为 JavaScript——"
            "尽管两种语言几乎没有关系。"
            "Brendan Eich 只用了 10 天就写出了第一个版本。"
        ),
        "idiom_snippet": {
            "title": "Proxy 实现数据绑定",
            "code": (
                "const reactive = (obj, onChange) => {\n"
                "    return new Proxy(obj, {\n"
                "        set(target, key, value) {\n"
                "            const old = target[key]\n"
                "            target[key] = value\n"
                "            onChange(key, old, value)\n"
                "            return true\n"
                "        }\n"
                "    })\n"
                "}"
            ),
        },
    },
    "Java": {
        "proverb": {
            "en": "Write once, debug everywhere.",
            "zh": "写一次，到处调试（误）。其实：一次编写，到处运行。",
        },
        "energy_map": {
            "morning":   "☕ 咖啡时光，Stream API 和 Lambda 表达式",
            "afternoon": "🏗️ 架构下午，Spring Boot + DI",
            "evening":   "📚 集合深处，HashMap 底层实现探索",
            "night":     "🔧 JVM 调优，GC 算法和字节码阅读",
        },
        "project_tips": [
            "用 Stream API 重构一个命令式循环",
            "写一个自定义注解（@Interface）并用反射处理",
            "实现一个简易的 LRUCache",
            "用 Virtual Threads（Project Loom）重写一个并发任务",
        ],
        "trivia": (
            "Java 的吉祥物 'Duke' 是一个卡通风格的咖啡杯，"
            "灵感来自 Java 名称与 Java 咖啡豆（Java coffee）的双关。"
            "James Gosling 在 Sun 工作时，最初把语言命名为 'Oak'，"
            "后来因为商标冲突才改名为 Java。"
        ),
        "idiom_snippet": {
            "title": "Stream API + Lambda 链式过滤",
            "code": (
                "List<String> result = persons.stream()\n"
                "    .filter(p -> p.getAge() > 18)\n"
                "    .map(p -> p.getName().toUpperCase())\n"
                "    .distinct()\n"
                "    .sorted()\n"
                "    .collect(Collectors.toList());"
            ),
        },
    },
    "C/C++": {
        "proverb": {
            "en": "It's not a bug; it's an undocumented feature.",
            "zh": "这不是 bug，是未文档化的特性。（每个 C/C++ 程序员都懂的痛）",
        },
        "energy_map": {
            "morning":   "🔩 系统级清醒，指针运算和内存布局",
            "afternoon": "⚡ 性能下午，手写 SIMD 或内存池",
            "evening":   "🛠️ 工具制作，宏技巧和 Makefile",
            "night":     "💀 极限挑战，UB（未定义行为）和竞态条件",
        },
        "project_tips": [
            "实现一个简易的 slab allocator",
            "用模板元编程写一个类型列表",
            "手写一个 lock-free 的 ring buffer",
            "写一段 SIMD 代码（AVX2）做向量加法",
        ],
        "trivia": (
            "C++ 的创造者 Bjarne Stroustrup 最初把语言叫 'C with Classes'，"
            "后来才改名为 C++（++ 是 C 的自增操作符）。"
            "而 C++ 的标准库里有大约 100 万行代码，"
            "但 C++ 本身的核心语言特性却少得惊人——大部分能力都来自库。"
        ),
        "idiom_snippet": {
            "title": "RAII + 智能指针",
            "code": (
                "#include <memory>\n\n"
                "class NetworkConnection {\npublic:\n"
                "    ~NetworkConnection() {\n"
                "        close(); // 自动释放资源\n"
                "    }\n"
                "    void send(const std::string& data);\n"
                "};\n\n"
                "void demo() {\n"
                "    auto conn = std::make_unique<NetworkConnection>();\n"
                "    conn->send(\"hello\");\n"
                "    // 自动析构，无需手动 close\n"
                "}"
            ),
        },
    },
}


# ─────────────────────────────────────────────────────────────────────────────
# 核心：读写 language_rotation.json
# ─────────────────────────────────────────────────────────────────────────────

def _read_json(json_path: str) -> Dict[str, Any]:
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)


def _write_json(json_path: str, data: Dict[str, Any]) -> None:
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# ─────────────────────────────────────────────────────────────────────────────
# 核心 API：旋转 + 生成墨讯
# ─────────────────────────────────────────────────────────────────────────────

def rotate_and_get_ink(
    json_path: str = DEFAULT_LANGUAGE_ROTATION_JSON,
) -> Dict[str, Any]:
    """
    读取 language_rotation.json，取出当前语言，
    然后将 current_index 循环前进一步（基于 ROTATION_ORDER 而非 JSON 中的 languages），
    并更新 JSON。

    注意：JSON 中的 languages 数组可能有 22 种语言，
    但轮换顺序由 ROTATION_ORDER 固定指定（9 种），只涉及前 9 种。

    Returns:
        {
            "current_language": str,        # 当前被选中的语言
            "next_language": str,           # 下一个语言
            "ink": {                         # 墨讯内容
                "proverb": {"en": str, "zh": str},
                "energy": str,               # 当前时段的能量描述
                "project_tip": str,          # 今日推荐项目
                "trivia": str,
                "idiom": {"title": str, "code": str},
            },
            "rotated_at": str,              # ISO 时间戳
        }
    """
    data = _read_json(json_path)

    # 使用固定的 ROTATION_ORDER（9种语言）来确定索引
    idx = data.get("current_index", 0) % len(ROTATION_ORDER)
    current = ROTATION_ORDER[idx]

    # 循环前进
    next_idx = (idx + 1) % len(ROTATION_ORDER)
    next_lang = ROTATION_ORDER[next_idx]

    # 更新 JSON
    data["current_index"] = next_idx
    data["last_language"] = current
    data["updated_at"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00")
    _write_json(json_path, data)

    # 查墨讯数据库
    lang_data = INK_DATABASE.get(current, {})
    energy = _get_energy_of_now(lang_data.get("energy_map", {}))
    project_tip = random.choice(lang_data.get("project_tips", ["写点代码吧"]))

    return {
        "current_language": current,
        "next_language": next_lang,
        "ink": {
            "proverb": lang_data.get("proverb", {"en": "", "zh": ""}),
            "energy": energy,
            "project_tip": project_tip,
            "trivia": lang_data.get("trivia", ""),
            "idiom": lang_data.get("idiom_snippet", {}),
        },
        "rotated_at": data["updated_at"],
    }


def get_ink_preview(
    language: Optional[str] = None,
    json_path: str = DEFAULT_LANGUAGE_ROTATION_JSON,
) -> Dict[str, Any]:
    """
    预览指定语言（或当前轮换语言）的墨讯（不推进索引）。
    """
    data = _read_json(json_path)
    if language is None:
        idx = data.get("current_index", 0) % len(ROTATION_ORDER)
        language = ROTATION_ORDER[idx]

    lang_data = INK_DATABASE.get(language, {})
    energy = _get_energy_of_now(lang_data.get("energy_map", {}))
    project_tip = random.choice(lang_data.get("project_tips", ["写点代码吧"]))

    return {
        "current_language": language,
        "ink": {
            "proverb": lang_data.get("proverb", {"en": "", "zh": ""}),
            "energy": energy,
            "project_tip": project_tip,
            "trivia": lang_data.get("trivia", ""),
            "idiom": lang_data.get("idiom_snippet", {}),
        },
    }


# ─────────────────────────────────────────────────────────────────────────────
# 辅助
# ─────────────────────────────────────────────────────────────────────────────

def _get_energy_of_now(energy_map: Dict[str, str]) -> str:
    """根据当前北京时间，返回合适的能量描述。"""
    now_utc = datetime.utcnow()
    now_bj = now_utc + timedelta(hours=8)
    hour = now_bj.hour
    if 6 <= hour < 12:
        key = "morning"
    elif 12 <= hour < 18:
        key = "afternoon"
    elif 18 <= hour < 23:
        key = "evening"
    else:
        key = "night"
    return energy_map.get(key, energy_map.get("morning", ""))


# ─────────────────────────────────────────────────────────────────────────────
# 格式化输出
# ─────────────────────────────────────────────────────────────────────────────

def format_ink_console(result: Dict[str, Any]) -> str:
    """将墨讯格式化为控制台友好输出（ASCII-art 框）。"""
    lang = result["current_language"]
    ink = result["ink"]
    next_lang = result["next_language"]

    emoji_map = {
        "Rust": "🦀", "Go": "🐹", "Swift": "🦅", "Kotlin": "🟣",
        "TypeScript": "🔷", "JavaScript": "🟡", "Java": "☕", "C/C++": "🔩",
    }
    emoji = emoji_map.get(lang, "📦")

    lines = [
        f"  ┌{'─' * 50}┐",
        f"  │ 🍶 Polyglot Ink — {lang:<38}│",
        f"  ├{'─' * 50}┤",
        f"  │ 💬 谚语                                 │",
        f"  │   \"{ink['proverb']['en']:<44}│",
        f"  │   {ink['proverb']['zh']:<46}│",
        f"  ├{'─' * 50}┤",
        f"  │ ⚡ 今日能量                            │",
        f"  │   {ink['energy']:<46}│",
        f"  ├{'─' * 50}┤",
        f"  │ 🛠️  今日项目                            │",
        f"  │   {ink['project_tip']:<46}│",
        f"  ├{'─' * 50}┤",
        f"  │ 🧩 惯用法                               │",
        f"  │   {ink['idiom'].get('title', ''):<46}│",
    ]
    # 分行显示代码（每行最多 46 字符）
    code_lines = ink['idiom'].get('code', '').split('\n')
    for cl in code_lines:
        wrapped = [cl[i:i+46] for i in range(0, len(cl), 46)]
        for w in wrapped:
            lines.append(f"  │     {w:<46}│")
    lines += [
        f"  ├{'─' * 50}┤",
        f"  │ 📚 趣闻                                 │",
    ]
    #趣闻换行
    trivia = ink['trivia']
    for i in range(0, len(trivia), 46):
        lines.append(f"  │   {trivia[i:i+46]:<46}│")
    lines += [
        f"  ├{'─' * 50}┤",
        f"  │ ⏭️  下一个语言：{next_lang:<36}│",
        f"  └{'─' * 50}┘",
        f"  rotated at: {result['rotated_at']}",
    ]
    return "\n".join(lines)


def format_ink_markdown(result: Dict[str, Any]) -> str:
    """将墨讯格式化为 Markdown，适合直接复制到文档。"""
    lang = result["current_language"]
    ink = result["ink"]

    emoji_map = {
        "Rust": "🦀", "Go": "🐹", "Swift": "🦅", "Kotlin": "🟣",
        "TypeScript": "🔷", "JavaScript": "🟡", "Java": "☕", "C/C++": "🔩",
    }
    emoji = emoji_map.get(lang, "📦")

    md = [
        f"## 🍶 Polyglot Ink — {lang} {emoji}",
        "",
        f"**EN:** _{ink['proverb']['en']}_",
        f"**ZH:** {ink['proverb']['zh']}",
        "",
        f"### ⚡ 今日能量",
        f"{ink['energy']}",
        "",
        f"### 🛠️ 今日项目推荐",
        f"- {ink['project_tip']}",
        "",
        f"### 🧩 惯用法示例",
        f"**{ink['idiom'].get('title', '')}**",
        "```" + _ext_for_lang(lang),
        ink['idiom'].get('code', ''),
        "```",
        "",
        f"### 📚 趣闻",
        ink['trivia'],
        "",
        f"⏭️ **下一个语言：** {result['next_language']}",
        f"_rotated at: {result['rotated_at']}_",
    ]
    return "\n".join(md)


def _ext_for_lang(lang: str) -> str:
    exts = {
        "Rust": "rust", "Go": "go", "Swift": "swift", "Kotlin": "kotlin",
        "TypeScript": "typescript", "JavaScript": "javascript",
        "Java": "java", "C/C++": "cpp",
    }
    return exts.get(lang, "text")


# ─────────────────────────────────────────────────────────────────────────────
# CLI 入口
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Polyglot Ink — 每日语言墨讯")
    sub = parser.add_subparsers(dest="cmd")

    sub.add_parser("ink", help="生成当前语言的每日墨讯并轮换")
    sub.add_parser("preview", help="预览当前语言墨讯（不轮换）")
    sub.add_parser("list", help="列出所有墨讯支持的语言")
    preview_lang = sub.add_parser("preview-lang", help="预览指定语言墨讯（不轮换）")
    preview_lang.add_argument("language", help="语言名称")

    args = parser.parse_args()

    if args.cmd == "ink":
        result = rotate_and_get_ink()
        print(format_ink_console(result))
    elif args.cmd == "preview":
        result = get_ink_preview()
        print(format_ink_console({"current_language": result["current_language"], "ink": result["ink"], "next_language": "", "rotated_at": ""}))
    elif args.cmd == "preview-lang":
        result = get_ink_preview(args.language)
        print(format_ink_console({"current_language": result["current_language"], "ink": result["ink"], "next_language": "", "rotated_at": ""}))
    elif args.cmd == "list":
        print("支持的语言：", ", ".join(ROTATION_ORDER))
    else:
        parser.print_help()
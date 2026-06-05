"""
Polyglot Codex — 多语言每日代码百科
每天为当前轮换语言生成一份语言画像：个性特质、生态亮点、实战技巧、代码片段、彩蛋 trivia。

工作流程：
  1. 读取 language_rotation.json 的 current_index，取出当前语言
  2. 从 CODEX 数据库取出该语言的完整画像
  3. 将 current_index 循环前进一步，写回 JSON
  4. 返回格式化后的 Codex 条目（控制台打印 / API 返回）

Distinct from existing tools:
  - kata_generator:     编程练习挑战（有 starter_code / solution）
  - language_compass:   学习路径地图（分 stage 的里程碑计划）
  - language_synapse:   跨语言概念桥梁（同一概念在不同语言的思维差异）
  - polyglot_digest:    语法平行视图（多语言同义代码并排展示）
  - language_archaeology: 历史演变（时间维度）
  - language_sage:      惯用法/最佳实践（使用维度）
  - language_ecohub:     包生态指南（工具链维度）

Polyglot Codex 的独特视角：每日语言"肖像画" —
  集个性画像 + 生态速览 + 实战 tip + 彩蛋为一体，
  帮助你每天"认识一种语言的性格"。
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


# ─────────────────────────────────────────────────────────────────────────────
# CODEX 数据库：每种语言的完整画像
# ─────────────────────────────────────────────────────────────────────────────
CODEX: Dict[str, Dict[str, Any]] = {
    "Rust": {
        "personality": "严谨的守门人 · 编译器即导师",
        "tagline": "让编译器替你操心内存，放心去解决真正的问题。",
        "superpowers": ["所有权系统", "零成本抽象", "无畏并发", "内存安全"],
        "blindspots": ["编译时间", "动态大小类型(DST)", "async 生态年轻"],
        "famous_projects": [
            ("Rust Analyzer", "IDE 语言服务器"),
            ("Tokio", "异步运行时"),
            ("Ripgrep", "极速搜索工具"),
            ("Firecracker", "AWS Lambda 底层 VM"),
        ],
        "ecosystem": {
            "pkg_manager": "crates.io (Cargo)",
            "testing": "内置 #[test] + cargo test",
            "docs": "cargo doc --open",
            "fmt": "rustfmt",
            "linter": "clippy",
        },
        "quick_tip": (
            "善用 `?` 运算符自动传播 Result/Option，"
            "比 match 手写干净 10 倍：\n"
            "  let content = std::fs::read_to_string(\"file\")?;"
        ),
        "real_world_snippet": {
            "title": "并发-safe 计数器（Arc<Mutex<T>>）",
            "code": (
                "use std::sync::{Arc, Mutex};\n"
                "use std::thread;\n\n"
                "let counter = Arc::new(Mutex::new(0));\n"
                "let mut handles = vec![];\n\n"
                "for _ in 0..8 {\n"
                "    let c = Arc::clone(&counter);\n"
                "    handles.push(thread::spawn(move || {\n"
                "        let mut n = c.lock().unwrap();\n"
                "        *n += 1;\n"
                "    }));\n"
                "}\n\n"
                "for h in handles { h.join().unwrap(); }\n"
                "println!(\"Result: {}\", *counter.lock().unwrap());"
            ),
        },
        "trivia": [
            "Rust 连续 8 年（2016–2024）在 Stack Overflow 开发者调查中获评「最受喜爱语言」",
            "Rust 的吉祥物 Ferris 是一只可爱的螃蟹 — 来自 `crab` 的双关",
            "Rust 编译器 rustc 本身也是用 Rust 写的（自举）",
            "Linux 内核 6.1 起正式支持 Rust，成为除 C 之外第二种内核开发语言",
        ],
        "color": "🔴",
    },
    "Go": {
        "personality": "务实的建筑工 · 简单即力量",
        "tagline": "Go 的设计哲学：少即是多。清晰的代码比聪明的代码更有价值。",
        "superpowers": ["goroutine + channel", "简单语法", "极速编译", "标准库统治"],
        "blindspots": ["泛型历史短暂(1.18)", "错误处理冗长", "无泛型时的代码重复"],
        "famous_projects": [
            ("Docker", "容器化平台"),
            ("Kubernetes", "容器编排"),
            ("Terraform", "IaC 工具"),
            ("Prometheus", "监控系统"),
        ],
        "ecosystem": {
            "pkg_manager": "go mod（内置）",
            "testing": "testing 包 + go test",
            "docs": "go doc / pkg.go.dev",
            "fmt": "gofmt（内置）",
            "linter": "golangci-lint",
        },
        "quick_tip": (
            "goroutine 是 Go 并发的核心，便宜到可以开百万个：\n"
            "  go func() { doWork() }()  // 启动异步 goroutine\n"
            "  ch <- value              // 发送到 channel\n"
            "  <-ch                     // 从 channel 接收"
        ),
        "real_world_snippet": {
            "title": "Worker Pool（ Goroutine 池）",
            "code": (
                "func worker(jobs <-chan int, results chan<- int) {\n"
                "    for j := range jobs {\n"
                "        results <- j * 2\n"
                "    }\n"
                "}\n\n"
                "func main() {\n"
                "    jobs := make(chan int, 100)\n"
                "    results := make(chan int, 100)\n\n"
                "    for w := 1; w <= 3; w++ {\n"
                "        go worker(jobs, results)\n"
                "    }\n\n"
                "    for i := 1; i <= 5; i++ { jobs <- i }\n"
                "    close(jobs)\n\n"
                "    for a := 1; a <= 5; a++ { println(<-results) }\n"
                "}"
            ),
        },
        "trivia": [
            "Go 的三位创始人 Rob Pike、Ken Thompson、Robert Griesemer 都来自 Bell Labs",
            "Go 最初是 Google 内部项目，目标是解决 C++ 编译慢的问题",
            "Go 的吉祥物是 Gopher（囊地鼠），由 Renée French 设计",
            "goroutine 调度器叫 M:N 调度器（ M 个 goroutine 映射到 N 个 OS 线程）",
        ],
        "color": "🔵",
    },
    "Swift": {
        "personality": "优雅的魔术师 · 安全与表现力并存",
        "tagline": "Swift 的目标：让编写代码成为一种快乐，同时保证运行时安全。",
        "superpowers": ["可选类型安全", "协议扩展", "值类型（struct）", "SwiftUI"],
        "blindspots": ["Linux 生态较弱", "ABI 稳定性历史问题", "编译时间"],
        "famous_projects": [
            ("Swift.org", "官方开源项目"),
            ("SwiftUI", "声明式 UI"),
            ("Swift Package Manager", "官方包管理"),
            ("IBM Swift Sandbox", "在线 REPL"),
        ],
        "ecosystem": {
            "pkg_manager": "Swift Package Manager（内置）",
            "testing": "XCTest + @testable import",
            "docs": "jazzy（Apple 官方文档工具）",
            "fmt": "swift-format",
            "linter": "SwiftLint",
        },
        "quick_tip": (
            "Swift 的可选类型（Optional）让你显式处理 nil：\n"
            "  let name: String? = maybeHasValue\n"
            "  // 安全解包：\n"
            "  if let n = name { print(n) }\n"
            "  // 或：name?.uppercased()"
        ),
        "real_world_snippet": {
            "title": "Protocol Extension 默认实现",
            "code": (
                "protocol Greeting {\n"
                "    var name: String { get }\n"
                "    func greet() -> String\n"
                "}\n\n"
                "extension Greeting {\n"
                "    // 默认实现 — 遵守协议的类型自动获得此方法\n"
                "    func greet() -> String {\n"
                "        \"Hello, \\(name)!\"\n"
                "    }\n"
                "}\n\n"
                "struct User: Greeting {\n"
                "    let name: String\n"
                "}\n\n"
                "let user = User(name: \"Polyglot\")\n"
                "print(user.greet()) // Hello, Polyglot!"
            ),
        },
        "trivia": [
            "Swift 由 Chris Lattner 设计，最初为了解决 Objective-C 的局限性",
            "Swift 1.0 于 2014 年 WWDC 发布，2015年 开源",
            "Swift 的 == 比较比 Objective-C 的 isEqual: 更安全（不需要手动实现）",
            "Swift 的 guard 语句是早期退出的最佳实践，减少嵌套层级",
        ],
        "color": "🟠",
    },
    "Kotlin": {
        "personality": "务实的 JVM 诗人 · 简洁与安全兼顾",
        "tagline": "Kotlin：现代 JVM 语言，把 Java 的冗长变成优雅。",
        "superpowers": ["空安全", "扩展函数", "协程", "与 Java 100% 互操作"],
        "blindspots": ["编译速度比 Java 慢", "Ktor 生态不如 Spring", "DSL 学习曲线"],
        "famous_projects": [
            ("Jetpack Compose", "Android UI 框架"),
            ("Spring Boot + Kotlin", "后端开发"),
            ("Ktor", "Web 框架"),
            ("Exposed", "轻量级 ORM"),
        ],
        "ecosystem": {
            "pkg_manager": "Maven Central / Gradle",
            "testing": "JUnit 5 + Kotlin Test",
            "docs": "dokka",
            "fmt": "ktfmt / ktlint",
            "linter": "ktlint / detekt",
        },
        "quick_tip": (
            "Kotlin 协程让异步代码看起来像同步：\n"
            "  suspend fun fetchData(): String {\n"
            "      delay(1000)  // 非阻塞挂起\n"
            "      return \"Done!\"\n"
            "  }\n\n"
            "  GlobalScope.launch { println(fetchData()) }"
        ),
        "real_world_snippet": {
            "title": "Data Class + 扩展函数",
            "code": (
                "data class User(val name: String, val age: Int)\n\n"
                "// 扩展函数 — 给已有类添加方法\n"
                "fun User.greet(): String = \"Hi, I'm $name!\"\n\n"
                "fun User.isAdult(): Boolean = age >= 18\n\n"
                "fun main() {\n"
                "    val user = User(\"Alice\", 30)\n"
                "    println(user.greet())   // Hi, I'm Alice!\n"
                "    println(user.isAdult()) // true\n"
                "    // 解构：\n"
                "    val (n, a) = user\n"
                "    println(\"$n is $a years old\")\n"
                "}"
            ),
        },
        "trivia": [
            "Kotlin 由 JetBrains 开发，名字来自圣彼得堡附近的一个 Kotlin 岛",
            "Google 2017 年 I/O 大会正式宣布 Kotlin 为 Android 一级开发语言",
            "Kotlin 的空安全（Null Safety）让 NullPointerException 大幅减少",
            "Kotlin 1.0 于 2016 年发布，现在同时支持 JVM / JS / Native",
        ],
        "color": "🟣",
    },
    "TypeScript": {
        "personality": "严谨的类型侦探 · JavaScript 的超集守护者",
        "tagline": "TypeScript：给你的 JavaScript 装上类型安全的安全气囊。",
        "superpowers": ["静态类型", "接口/泛型", "IDE 智能提示", "渐进式类型"],
        "blindspots": ["编译配置复杂", "any 类型滥用", "大型项目构建时间"],
        "famous_projects": [
            ("VS Code", "宇宙最强 IDE"),
            ("Angular", "企业级前端框架"),
            ("React + TypeScript", "现代前端标配"),
            ("Denode / NestJS", "Node.js 后端框架"),
        ],
        "ecosystem": {
            "pkg_manager": "npm / yarn / pnpm",
            "testing": "Jest / Vitest / Mocha",
            "docs": "TypeDoc / Storybook",
            "fmt": "Prettier（包含格式化）",
            "linter": "ESLint + @typescript-eslint",
        },
        "quick_tip": (
            "TypeScript 的类型守卫（type guard）让你在运行时安全检查类型：\n"
            "  function isString(x: unknown): x is string {\n"
            "      return typeof x === 'string';\n"
            "  }\n"
            "  if (isString(value)) { value.toUpperCase(); } // TS 知道是 string"
        ),
        "real_world_snippet": {
            "title": "泛型约束 + 接口组合",
            "code": (
                "interface Id {\n"
                "    readonly id: string;\n"
                "}\n\n"
                "interface Named {\n"
                "    readonly name: string;\n"
                "}\n\n"
                "// 泛型约束：T 必须同时满足 Id 和 Named\n"
                "function getDisplay<T extends Id & Named>(obj: T): string {\n"
                "    return `${obj.name} (${obj.id})`;\n"
                "}\n\n"
                "const user = { id: 'u1', name: 'Alice', age: 30 };\n"
                "console.log(getDisplay(user)); // Alice (u1)"
            ),
        },
        "trivia": [
            "TypeScript 由微软 Anders Hejlsberg（C# 之父）主导设计",
            "TypeScript 是 JavaScript 的严格超集，任何 .js 文件都是合法的 .ts 文件",
            "Angular 2+ 完全使用 TypeScript 编写，是最早大规模采用 TS 的框架",
            "TypeScript 的 `infer` 关键字让你在条件类型中推导类型",
        ],
        "color": "🔷",
    },
    "JavaScript": {
        "personality": "自由的叛逆者 · Web 的灵魂",
        "tagline": "JavaScript：只要能在浏览器运行，世界就是你的舞台。",
        "superpowers": ["无处不在", "事件循环", "原型继承", "动态生态"],
        "blindspots": ["类型系统缺失", "回调地狱", "this 绑定陷阱", "精度问题"],
        "famous_projects": [
            ("Node.js", "服务端正则化"),
            ("React", "UI 库"),
            ("V8 Engine", "极速 JS 引擎"),
            ("npm", "最大包 registry"),
        ],
        "ecosystem": {
            "pkg_manager": "npm / yarn / pnpm",
            "testing": "Jest / Vitest",
            "docs": "JSDoc / Storybook",
            "fmt": "Prettier",
            "linter": "ESLint",
        },
        "quick_tip": (
            "async/await 让异步代码可读如同步：\n"
            "  async function fetchUser(id) {\n"
            "    const res = await fetch(`/api/users/${id}`);\n"
            "    const data = await res.json();\n"
            "    return data;\n"
            "  }\n\n"
            "  // 错误处理：\n"
            "  try {\n"
            "    const user = await fetchUser(1);\n"
            "  } catch (e) { console.error(e); }"
        ),
        "real_world_snippet": {
            "title": "Promise + 链式调用",
            "code": (
                "const fetchUser = (id) =>\n"
                "  new Promise((resolve, reject) => {\n"
                "    setTimeout(() => {\n"
                "      if (id > 0) resolve({ id, name: 'Alice' });\n"
                "      else reject(new Error('Invalid ID'));\n"
                "    }, 100);\n"
                "  });\n\n"
                "fetchUser(1)\n"
                "  .then(u => { console.log(u.name); return u.id; })\n"
                "  .then(id => fetchUser(id + 1))\n"
                "  .then(u => console.log('Next:', u.name))\n"
                "  .catch(err => console.error(err));"
            ),
        },
        "trivia": [
            "JavaScript 由 Brendan Eich 于 1995 年用 10 天设计完成",
            "JavaScript 与 Java 除了名字相似，没有任何关系",
            "Node.js 让 JavaScript 进入服务端，npm 成为世界最大包管理器（100万+ 包）",
            "V8 引擎将 JS 编译成机器码，性能提升数十倍，催生了现代 Web",
        ],
        "color": "🟡",
    },
    "Java": {
        "personality": "企业级老将 · 稳定压倒一切",
        "tagline": "Java：一次编写，到处运行。30年企业级首选。",
        "superpowers": ["JVM 生态", "强类型", "Spring 生态", "向后兼容"],
        "blindspots": ["语法冗长", "启动慢", "无原语泛型", "版本碎片化"],
        "famous_projects": [
            ("Spring Boot", "Java 后端标准框架"),
            ("Hadoop", "大数据处理"),
            ("Elasticsearch", "搜索引擎"),
            ("Apache Kafka", "消息队列"),
        ],
        "ecosystem": {
            "pkg_manager": "Maven / Gradle",
            "testing": "JUnit 5 + Mockito",
            "docs": "Javadoc",
            "fmt": "google-java-format",
            "linter": "Checkstyle / SpotBugs",
        },
        "quick_tip": (
            "Java 的 Stream API 让集合操作函数式化：\n"
            "  List<String> names = List.of(\"Alice\", \"Bob\", \"Charlie\");\n\n"
            "  List<String> result = names.stream()\n"
            "      .filter(n -> n.length() > 3)\n"
            "      .map(String::toUpperCase)\n"
            "      .sorted()\n"
            "      .collect(Collectors.toList());\n\n"
            "  // result: [ALICE, CHARLIE]"
        ),
        "real_world_snippet": {
            "title": "Record 类（Java 16+）+ Pattern Matching",
            "code": (
                "// Record = 更简洁的数据类（自动生成 equals/hashCode/toString）\n"
                "public record User(long id, String name, int age) {}\n\n"
                "// Pattern Matching for switch (Java 21+)\n"
                "String describe(Object obj) {\n"
                "    return switch (obj) {\n"
                "        case Integer i -> \"Int: \" + i;\n"
                "        case String s -> \"Str: \" + s.length() + \" chars\";\n"
                "        case User u   -> \"User: \" + u.name();\n"
                "        case null     -> \"null\";\n"
                "        default      -> \"Unknown\";\n"
                "    };\n"
                "}\n\n"
                "public static void main(String[] args) {\n"
                "    System.out.println(describe(new User(1, \"Alice\", 30)));\n"
                "}"
            ),
        },
        "trivia": [
            "Java 由 James Gosling 于 1995 年在 Sun Microsystems 设计",
            "Java 的 logo 是一杯热咖啡 — Java 是印度尼西亚的咖啡名",
            "JVM（Java 虚拟机）是 Java 跨平台的核心，也是 Kotlin/Scala 的运行基础",
            "Java 21 引入虚拟线程（Virtual Threads），彻底改变高并发编程模型",
        ],
        "color": "☕",
    },
    "C/C++": {
        "personality": "掌控一切的机械大师 · 性能至上",
        "tagline": "C/C++：给你最高性能，也给你最彻底的复杂性。",
        "superpowers": ["零开销抽象", "手动内存管理", "指针魔法", "硬件直接控制"],
        "blindspots": ["内存安全依赖程序员", "未定义行为多", "编译错误信息晦涩"],
        "famous_projects": [
            ("Linux 内核", "操作系统"),
            ("Redis", "内存数据库"),
            ("Git", "版本控制"),
            ("Unreal Engine", "游戏引擎"),
        ],
        "ecosystem": {
            "pkg_manager": "vcpkg / Conan",
            "testing": "Google Test / Catch2",
            "docs": "Doxygen",
            "fmt": "clang-format",
            "linter": "clang-tidy",
        },
        "quick_tip": (
            "C++ 智能指针让手动 new/delete 成为历史：\n"
            "  #include <memory>\n\n"
            "  auto ptr = std::make_unique<int>(42);\n"
            "  // 无需手动 delete，作用域结束时自动释放\n"
            "  std::cout << *ptr << std::endl;\n\n"
            "  // 共享所有权用 std::shared_ptr\n"
            "  auto sptr = std::make_shared<int>(100);"
        ),
        "real_world_snippet": {
            "title": "C++20 概念（Concepts）约束模板",
            "code": (
                "#include <concepts>\n"
                "#include <iostream>\n"
                "#include <vector>\n"
                "#include <algorithm>\n\n"
                "// 用 concept 约束泛型参数类型\n"
                "template <std::integral T>\n"
                "T square(T n) { return n * n; }\n\n"
                "template <std::ranges::range R>\n"
                "void printAll(const R& r) {\n"
                "    for (const auto& elem : r)\n"
                "        std::cout << elem << ' ';\n"
                "    std::cout << '\\n';\n"
                "}\n\n"
                "int main() {\n"
                "    std::vector<int> v = {1, 2, 3, 4, 5};\n"
                "    std::for_each(v.begin(), v.end(),\n"
                "        [](int& n) { n = square(n); });\n"
                "    printAll(v); // 1 4 9 16 25\n"
                "}"
            ),
        },
        "trivia": [
            "C 由 Dennis Ritchie 于 1972 年在 Bell Labs 设计，用于重写 Unix",
            "C++ 由 Bjarne Stroustrup 于 1983 年创建，最初叫「C with Classes」",
            "C 是现代所有系统语言的祖先：Python/Rust/Go/JS 编译器都用 C/C++ 编写",
            "C++20 的三路比较运算符（<=>）让排序和比较代码大幅简化",
        ],
        "color": "🔩",
    },
}


# ─────────────────────────────────────────────────────────────────────────────
# 辅助函数
# ─────────────────────────────────────────────────────────────────────────────

def _read_rotation_json(json_path: str) -> Dict[str, Any]:
    """读取语言轮换配置 JSON。"""
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)


def _write_rotation_json(json_path: str, data: Dict[str, Any]) -> None:
    """写回语言轮换配置 JSON。"""
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# ─────────────────────────────────────────────────────────────────────────────
# 核心 API
# ─────────────────────────────────────────────────────────────────────────────

def rotate_and_get_codex(
    json_path: str = DEFAULT_LANGUAGE_ROTATION_JSON,
) -> Dict[str, Any]:
    """
    读取 language_rotation.json，取出当前语言，从 CODEX 取出画像，
    将 current_index 循环前进一步，写回 JSON。

    Returns:
        {
            "language": str,
            "color": str,
            "personality": str,
            "tagline": str,
            "superpowers": List[str],
            "blindspots": List[str],
            "famous_projects": List[Tuple[str, str]],
            "ecosystem": Dict[str, str],
            "quick_tip": str,
            "real_world_snippet": {"title": str, "code": str},
            "trivia": List[str],
            "index": int,
            "total": int,
            "next_language": str,
        }
    """
    data = _read_rotation_json(json_path)
    languages = data["languages"]
    total = len(languages)
    idx = data.get("current_index", 0) % total

    current_lang = languages[idx]
    codex_entry = CODEX.get(current_lang)

    if codex_entry is None:
        raise ValueError(f"CODEX 中没有收录语言: {current_lang}")

    # 循环前进
    next_idx = (idx + 1) % total
    data["current_index"] = next_idx
    data["last_language"] = current_lang
    data["updated_at"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00")
    _write_rotation_json(json_path, data)

    return {
        "language": current_lang,
        **codex_entry,
        "index": idx,
        "total": total,
        "next_language": languages[next_idx],
    }


def get_codex_preview(
    json_path: str = DEFAULT_LANGUAGE_ROTATION_JSON,
) -> Dict[str, Any]:
    """
    预览当前语言画像（不推进索引）。
    """
    data = _read_rotation_json(json_path)
    languages = data["languages"]
    idx = data.get("current_index", 0) % len(languages)
    current_lang = languages[idx]
    codex_entry = CODEX.get(current_lang, {})
    return {
        "language": current_lang,
        "color": codex_entry.get("color", "📦"),
        "personality": codex_entry.get("personality", ""),
        "tagline": codex_entry.get("tagline", ""),
        "index": idx,
        "total": len(languages),
        "next_language": languages[(idx + 1) % len(languages)],
    }


def format_codex_markdown(codex: Dict[str, Any]) -> str:
    """
    将 Codex 条目格式化为 Markdown，适合打印/展示。
    """
    lang = codex["language"]
    color = codex.get("color", "📦")
    personality = codex.get("personality", "")
    tagline = codex.get("tagline", "")
    superpowers = codex.get("superpowers", [])
    blindspots = codex.get("blindspots", [])
    famous = codex.get("famous_projects", [])
    ecosystem = codex.get("ecosystem", {})
    quick_tip = codex.get("quick_tip", "")
    snippet = codex.get("real_world_snippet", {})
    trivia = codex.get("trivia", [])
    idx = codex.get("index", 0)
    total = codex.get("total", 0)
    next_lang = codex.get("next_language", "")

    lines = [
        f"## {color} Polyglot Codex — {lang}",
        f"**个性画像**: {personality}",
        f"> {tagline}",
        "",
        f"📍 第 {idx + 1}/{total} 站 · 下一个: **{next_lang}**",
        "",
        "---",
        "",
        "### 🦸 超能力",
    ]
    for sp in superpowers:
        lines.append(f"- {sp}")

    lines += ["", "### ⚠️ 盲区"]
    for bs in blindspots:
        lines.append(f"- {bs}")

    lines += ["", "### 🏗 生态工具链"]
    for k, v in ecosystem.items():
        lines.append(f"- **{k}**: {v}")

    lines += ["", "### 🌟 代表项目"]
    for name, desc in famous:
        lines.append(f"- **{name}** — {desc}")

    lines += ["", "### 💡 实战技巧"]
    for tip_line in quick_tip.split("\n"):
        lines.append(f"    {tip_line}")

    if snippet:
        lines += ["", f"### 🧩 代码示例: {snippet.get('title', '')}"]
        code_lines = snippet.get("code", "").split("\n")
        for cl in code_lines:
            lines.append(f"    {cl}")

    if trivia:
        lines += ["", "### 🎉 彩蛋Trivia"]
        for t in trivia:
            lines.append(f"- {t}")

    lines += ["", "---", f"*Polyglot Codex · auto-generated · {datetime.now().strftime('%Y-%m-%d %H:%M')}*"]
    return "\n".join(lines)


def format_codex_console(codex: Dict[str, Any]) -> str:
    """
    将 Codex 条目格式化为控制台彩色 ASCII 输出。
    """
    lang = codex["language"]
    color = codex.get("color", "📦")
    personality = codex.get("personality", "")
    tagline = codex.get("tagline", "")
    superpowers = codex.get("superpowers", [])
    famous = codex.get("famous_projects", [])
    quick_tip = codex.get("quick_tip", "")
    snippet = codex.get("real_world_snippet", {})
    trivia = codex.get("trivia", [])
    next_lang = codex.get("next_language", "")
    idx = codex.get("index", 0)
    total = codex.get("total", 0)

    # Pick one random trivia
    trivia_pick = random.choice(trivia) if trivia else ""

    W = 60
    def hr(): return "  " + "─" * W
    def box(lines): return "\n".join(
        f"  ║ {l:<{W}} ║" for l in lines
    )

    parts = [
        "",
        f"  ╔{'═' * W}╗",
        f"  ║ {color}  POLYGLOT CODEX  ·  {lang:<{W - 30}}║",
        f"  ╠{'═' * W}╣",
    ]

    # personality
    for chunk in [personality[i:i+W] for i in range(0, len(personality), W)]:
        parts.append(f"  ║ {chunk:<{W}} ║")
    parts.append(f"  ╠{'═' * W}╣")

    # tagline
    parts.append(f"  ║ {tagline:<{W}} ║")
    parts.append(f"  ╠{'═' * W}╣")

    # superpowers
    parts.append(f"  ║ {'🟢 SUPERPOWERS':<{W}} ║")
    for sp in superpowers:
        for chunk in [sp[i:i+W-4] for i in range(0, len(sp), W-4)]:
            parts.append(f"  ║   · {chunk:<{W-4}} ║")
    parts.append(f"  ╠{'═' * W}╣")

    # quick tip
    parts.append(f"  ║ {'💡 QUICK TIP':<{W}} ║")
    for tip_line in quick_tip.split("\n"):
        for chunk in [tip_line[i:i+W-4] for i in range(0, len(tip_line), W-4)]:
            parts.append(f"  ║   {chunk:<{W-4}} ║")
    parts.append(f"  ╠{'═' * W}╣")

    # snippet
    if snippet:
        parts.append(f"  ║ {'🧩 SNIPPET: ' + snippet.get('title', ''):<{W}} ║")
        for code_line in snippet.get("code", "").split("\n"):
            for chunk in [code_line[i:i+W-4] for i in range(0, len(code_line), W-4)]:
                parts.append(f"  ║   {chunk:<{W-4}} ║")
    parts.append(f"  ╠{'═' * W}╣")

    # famous projects
    parts.append(f"  ║ {'🏗 FAMOUS PROJECTS':<{W}} ║")
    for name, desc in famous[:3]:
        line = f"   {name}: {desc}"
        for chunk in [line[i:i+W-4] for i in range(0, len(line), W-4)]:
            parts.append(f"  ║   {chunk:<{W-4}} ║")
    parts.append(f"  ╠{'═' * W}╣")

    # trivia
    if trivia_pick:
        parts.append(f"  ║ {'🎉 TRIVIA':<{W}} ║")
        for chunk in [trivia_pick[i:i+W-4] for i in range(0, len(trivia_pick), W-4)]:
            parts.append(f"  ║   {chunk:<{W-4}} ║")
        parts.append(f"  ╠{'═' * W}╣")

    # footer
    parts.append(f"  ║  #{idx+1}/{total} · Next: {next_lang:<{W-20}} ║")
    parts.append(f"  ╚{'═' * W}╝")

    return "\n".join(parts)


# ─────────────────────────────────────────────────────────────────────────────
# CLI 入口
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="🗺 Polyglot Codex — 多语言每日代码百科"
    )
    sub = parser.add_subparsers(dest="cmd")

    sub.add_parser("today", help="生成今日语言 Codex（推进轮换）")
    sub.add_parser("preview", help="预览当前语言 Codex（不推进）")
    sub.add_parser("all", help="打印所有语言快速总览")

    args = parser.parse_args()

    if args.cmd == "today":
        codex = rotate_and_get_codex()
        print(format_codex_console(codex))
    elif args.cmd == "preview":
        preview = get_codex_preview()
        lang = preview["language"]
        entry = CODEX.get(lang, {})
        print(f"\n{entry.get('color', '📦')} {lang}")
        print(f"   {entry.get('personality', '')}")
        print(f"   {entry.get('tagline', '')}")
        print(f"   Index: {preview['index']+1}/{preview['total']} | Next: {preview['next_language']}")
    elif args.cmd == "all":
        data = _read_rotation_json(DEFAULT_LANGUAGE_ROTATION_JSON)
        for lang in data["languages"]:
            entry = CODEX.get(lang, {})
            print(f"{entry.get('color', '📦')} {lang}: {entry.get('personality', '')}")
    else:
        parser.print_help()
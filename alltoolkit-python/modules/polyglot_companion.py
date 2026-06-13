"""
polyglot_companion.py — 编程语言学习伴侣 (Polyglot Companion)
====================================================================
一个与 language_rotation.json 深度集成的 AI 学习伙伴模块。

核心逻辑：
  1. 读取 language_rotation.json，按 current_index 取当前轮换语言
  2. 生成一份"语言探险报告"：今日语言特性速览、代码示例、
     趣味冷知识、一道迷你练习题
  3. 支持 Pomodoro 学习法（25 min / 5 min break 节奏）
  4. 记录探险历史（history log）到 JSON
  5. 完成后将 current_index 前移一位并更新 updated_at

语言轮换顺序（8 种核心语言）：
  Rust → Go → Swift → Kotlin → TypeScript → JavaScript → Java → C/C++ → Rust（循环）

作者：AllToolkit 全自动生成
依赖：仅 Python 标准库（json, random, datetime, pathlib）
====================================================================
"""

import json
import random
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any

# ─────────────────────────────────────────────
# 路径配置
# ─────────────────────────────────────────────
_MODULE_DIR = Path(__file__).parent.parent          # alltoolkit-python/
_WORKSPACE_ROOT = _MODULE_DIR.parent               # workspace/
DEFAULT_LANGUAGE_ROTATION_JSON = str(_WORKSPACE_ROOT / "language_rotation.json")
DEFAULT_COMPANION_HISTORY_JSON = str(_WORKSPACE_ROOT / "polyglot_companion_history.json")


# ─────────────────────────────────────────────
# 语言探险知识库：每种语言的特性速览 + 冷知识 + 练习题
# ─────────────────────────────────────────────
LANGUAGE_ADVENTURES: Dict[str, Dict[str, Any]] = {
    "Rust": {
        "emoji": "🦀",
        "file_ext": "rs",
        "feature_name": "所有权系统 (Ownership & Borrowing)",
        "feature_blurb": (
            "Rust 的核心创新：每个值有且只有一个所有者，"
            "所有者离开作用域时值被丢弃（drop），无需垃圾回收。"
            "借用（& 和 &mut）让你临时访问数据而不获取所有权。"
        ),
        "code_example": (
            "fn main() {\n"
            "    let s1 = String::from(\"hello\");\n"
            "    let s2 = s1;        // s1 被 move 进 s2\n"
            "    // println!(\"{}\", s1); // ❌ 编译错误！s1 已无效\n"
            "    println!(\"{}\", s2); // ✅ OK\n"
            "\n"
            "    let s3 = String::from(\"world\");\n"
            "    let s4 = &s3;        // 借用，不获取所有权\n"
            "    println!(\"{} {}\", s3, s4); // ✅ s3 仍然有效\n"
            "}"
        ),
        "fun_fact": "Rust 编译器根据所有权的「生命周期」在编译期插入 drop 调用，故又称「编译时内存管理」。",
        "mini_exercise": {
            "title": "修复借用错误",
            "description": (
                "下面这段代码无法编译。请分析哪里违反了所有权规则，"
                "然后用两种方式修复：①改用克隆（clone）②改用借用（&）。"
            ),
            "broken_code": (
                "fn main() {\n"
                "    let msg = String::from(\"Rust\");\n"
                "    let a = msg;\n"
                "    let b = msg;\n"
                "    println!(\"{} {}\", a, b);\n"
                "}"
            ),
            "hint": "String 在赋值时是 Move 语义。要么 clone，要么借用引用。",
        },
        "study_tips": [
            "先理解 Owned vs Borrowed 的区别，这是 Rust 的心智模型核心",
            "遇到编译错误时，耐心读编译器提示——它会告诉你如何修",
            "用 rustlings 交互式练习工具边学边练",
        ],
    },
    "Go": {
        "emoji": "🐹",
        "file_ext": "go",
        "feature_name": "Goroutine 并发模型",
        "feature_blurb": (
            "Go 的并发核心是 goroutine——由 Go 运行时管理的轻量级线程。"
            "通过 channel 在 goroutine 之间传递数据，实现'不要通过共享内存来通信；"
            "要通信就共享内存'的哲学。"
        ),
        "code_example": (
            "package main\n\n"
            "import (\n"
            "    \"fmt\"\n"
            "    \"time\"\n"
            ")\n\n"
            "func speak(msg string) {\n"
            "    for i := 0; i < 3; i++ {\n"
            "        fmt.Println(msg, \"-\", i)\n"
            "        time.Sleep(time.Millisecond * 100)\n"
            "    }\n"
            "}\n\n"
            "func main() {\n"
            "    go speak(\"hello\")   // 启动 goroutine\n"
            "    go speak(\"world\")\n"
            "    time.Sleep(time.Second) // 等待并发完成\n"
            "}"
        ),
        "fun_fact": "goroutine 的初始栈只有 2KB（线程栈约 1MB），支持同时运行数十万个 goroutine。",
        "mini_exercise": {
            "title": "用 channel 同步并发",
            "description": (
                "启动两个 goroutine 分别打印'你好'和'世界'，"
                "用无缓冲 channel 确保'你好'一定先于'世界'打印。"
            ),
            "broken_code": (
                "package main\n\n"
                "import \"fmt\"\n\n"
                "func main() {\n"
                "    // 启动两个 goroutine\n"
                "    // 用 channel 确保顺序\n"
                "    fmt.Println(\"你好\")\n"
                "    fmt.Println(\"世界\")\n"
                "}"
            ),
            "hint": "用 make(chan bool) 创建 channel，在一个 goroutine 结束时往 channel 写入 true，另一个 goroutine 在打印前先从 channel 读取。",
        },
        "study_tips": [
            "先学会用 goroutine + channel，这才是 Go 的精髓",
            "WaitGroup 适合批量等待，context 适合取消信号",
            "避免 mutex——优先用 channel 共享数据",
        ],
    },
    "Swift": {
        "emoji": "🦅",
        "file_ext": "swift",
        "feature_name": "Optional 类型与空安全",
        "feature_blurb": (
            "Swift 的核心安全特性：每个变量必须显式声明是否可以为 nil。"
            "Optional 类型 T? 表示值可能存在也可能不存在，"
            "使用 if let / guard let / ?? 解包，安全又优雅。"
        ),
        "code_example": (
            "let name: String? = nil\n"
            "let greeting = name ?? \"Hello, stranger\"\n"
            "print(greeting) // \"Hello, stranger\"\n\n"
            "if let actualName = name {\n"
            "    print(\"Hello, \\(actualName)\")\n"
            "} else {\n"
            "    print(\"Hello, stranger\")\n"
            "}"
        ),
        "fun_fact": "Swift 的 Optional 甚至可以用在 Int? 上，实现类型层面的'无值'语义，比 Java 的 null 安全得多。",
        "mini_exercise": {
            "title": "安全解包 Optional",
            "description": (
                "定义一个返回 Optional String 的函数 findUser(id: Int)，"
                "id==1 返回 \"Alice\"，id==2 返回 nil。"
                "调用它并用 guard let 安全打印。"
            ),
            "broken_code": (
                "func findUser(id: Int) -> String? {\n"
                "    if id == 1 { return \"Alice\" }\n"
                "    return nil\n"
                "}\n\n"
                "let user = findUser(id: 1)\n"
                "print(\"User: \\(user)\") // 打印 Optional 值\n"
                "// 改成安全打印方式"
            ),
            "hint": "用 guard let user = findUser(id: 1) else { return } 解包，并在 else 分支处理未找到用户的情况。",
        },
        "study_tips": [
            "养成习惯：声明变量时优先用 let，只有需要修改时才用 var",
            "Optional 是 Swift 的核心——彻底搞懂它能让代码减少 80% 的崩溃",
            "善用 Xcode Playground 边写边看即时结果",
        ],
    },
    "Kotlin": {
        "emoji": "🟣",
        "file_ext": "kt",
        "feature_name": "协程 (Coroutines)",
        "feature_blurb": (
            "Kotlin 协程让异步编程变得像写同步代码一样自然。"
            "suspend 函数可以在不阻塞线程的情况下'暂停'执行，"
            "launch / async 让你轻松启动并发任务。"
        ),
        "code_example": (
            "import kotlinx.coroutines.*\n\n"
            "suspend fun fetchUser(id: Int): String {\n"
            "    delay(1000L) // 模拟网络请求（不阻塞线程）\n"
            "    return \"User#$id\"\n"
            "}\n\n"
            "fun main() = runBlocking {\n"
            "    val user = async { fetchUser(1) }\n"
            "    println(\"Waiting...\")\n"
            "    println(\"User: ${user.await()}\")\n"
            "}"
        ),
        "fun_fact": "Kotlin 协程在 JVM 上编译成字节码后，通过 Continuation 对象在 Suspend 函数间跳转，实现非阻塞挂起。",
        "mini_exercise": {
            "title": "启动并等待协程",
            "description": (
                "用 launch 启动两个协程，分别打印'你好'和'世界'，"
                "每个之间 delay 500ms，用 runBlocking 等待两者完成。"
            ),
            "broken_code": (
                "import kotlinx.coroutines.*\n\n"
                "fun main() = runBlocking {\n"
                "    // 启动两个协程\n"
                "    println(\"Start\")\n"
                "    delay(500)\n"
                "    println(\"End\")\n"
                "}"
            ),
            "hint": "launch 返回 Job，调用 .join() 或用 coroutineScope { } 等待子协程。",
        },
        "study_tips": [
            "协程是 Kotlin 最强大的特性——用它替代 AsyncTask 和线程池",
            "Flow 是响应式流，适合处理异步数据序列",
            "Structured Concurrency（结构化并发）确保不会协程泄露",
        ],
    },
    "TypeScript": {
        "emoji": "🔷",
        "file_ext": "ts",
        "feature_name": "类型系统与泛型",
        "feature_blurb": (
            "TypeScript 在 JavaScript 基础上加入了静态类型系统。"
            "泛型让你写出类型安全且可复用的代码，"
            "interface / type alias 让数据结构清晰明确。"
        ),
        "code_example": (
            "interface Response<T> {\n"
            "    data: T;\n"
            "    status: number;\n"
            "    message: string;\n"
            "}\n\n"
            "function parseResponse<T>(raw: unknown): Response<T> {\n"
            "    const r = raw as Response<T>;\n"
            "    return { data: r.data, status: r.status, message: r.message };\n"
            "}\n\n"
            "const res = parseResponse<{ name: string }>({\n"
            "    data: { name: \"Alice\" }, status: 200, message: \"OK\"\n"
            "});\n"
            "console.log(res.data.name); // \"Alice\" — 类型安全！"
        ),
        "fun_fact": "TypeScript 的类型系统是图灵完备的——你甚至可以用类型做计算！Conditional Types 和模板字面量类型是其典型代表。",
        "mini_exercise": {
            "title": "实现一个类型安全的 pick 函数",
            "description": (
                "实现一个工具类型 MyPick<T, K>，从对象类型 T 中选取键 K 组成新类型。"
                "然后用它在函数参数中限制只能传入特定字段。"
            ),
            "broken_code": (
                "// 尝试写出 MyPick\n"
                "type MyPick<T, K> = ...\n\n"
                "interface User { name: string; age: number; email: string; }\n"
                "type UserName = MyPick<User, 'name'>;\n"
                "// 期望 UserName = { name: string }"
            ),
            "hint": "用 { [P in K]: T[P] } 映射类型语法，P in K 遍历键集合。",
        },
        "study_tips": [
            "先用 unknown 代替 any，逐步细化类型",
            "善用 utility types（Partial, Required, Pick, Omit）避免重复造轮子",
            "类型推断优先，写不出类型时再加注解",
        ],
    },
    "JavaScript": {
        "emoji": "🟡",
        "file_ext": "js",
        "feature_name": "异步编程：Promise 与 async/await",
        "feature_blurb": (
            "JavaScript 是单线程异步语言，Promise 是处理异步操作的现代方式。"
            "async/await 让异步代码看起来像同步代码，"
            "彻底告别回调地狱（callback hell）。"
        ),
        "code_example": (
            "// 模拟异步请求\n"
            "const delay = (ms) => new Promise(res => setTimeout(res, ms));\n\n"
            "async function fetchUser(id) {\n"
            "    await delay(1000); // 模拟网络延迟\n"
            "    return { id, name: `User#${id}` };\n"
            "}\n\n"
            "(async () => {\n"
            "    const user = await fetchUser(1);\n"
            "    console.log(`Hello, ${user.name}!`);\n"
            "})();"
        ),
        "fun_fact": "Promise 有三种状态：pending（待定）、fulfilled（已兑现）、rejected（已拒绝），且状态一旦改变就不能再变。",
        "mini_exercise": {
            "title": "Promise 链与错误处理",
            "description": (
                "创建一个 Promise 链：先延迟 500ms 返回数字 1，"
                "再延迟 500ms 将其乘以 2，最后捕获任何可能的错误并打印。"
            ),
            "broken_code": (
                "const delay = (ms) => new Promise(res => setTimeout(res, ms));\n\n"
                "// 写出 Promise 链\n"
                "delay(500)\n"
                "    .then(...) // ...\n"
                "    .catch(err => console.error(err));"
            ),
            "hint": "第一个 .then 接收 (resolve) 回调，返回一个新值或 Promise；.catch 捕获链中任意位置的错误。",
        },
        "study_tips": [
            "先搞懂事件循环（Event Loop）——理解它你就理解了 JS 并发模型",
            "async/await 只是 Promise 的语法糖，理解 Promise 是根本",
            "用 Promise.all() 并行执行多个异步任务，比串行 await 高效",
        ],
    },
    "Java": {
        "emoji": "☕",
        "file_ext": "java",
        "feature_name": "OOP 继承与多态",
        "feature_blurb": (
            "Java 是纯面向对象语言，'一切皆对象'（原始类型除外）。"
            "继承（extends）、接口（implements）、"
            "方法重写（@Override）构成灵活的多态体系。"
        ),
        "code_example": (
            "interface Drawable {\n"
            "    void draw(); // 接口方法默认 public abstract\n"
            "}\n\n"
            "class Circle implements Drawable {\n"
            "    private double radius;\n"
            "    public Circle(double r) { this.radius = r; }\n"
            "    @Override\n"
            "    public void draw() {\n"
            "        System.out.println(\"Drawing circle r=\" + radius);\n"
            "    }\n"
            "}\n\n"
            "public class Main {\n"
            "    public static void main(String[] args) {\n"
            "        Drawable shape = new Circle(2.5); // 多态：父类引用指向子类对象\n"
            "        shape.draw(); // 调用 Circle 的实现\n"
            "    }\n"
            "}"
        ),
        "fun_fact": "Java 的 instanceof 既可以检查类型，还可以同时强制转换（Pattern Matching for Switch 从 Java 17 开始支持更优雅的模式匹配）。",
        "mini_exercise": {
            "title": "用策略模式消除 if-else",
            "description": (
                "设计一个简单的策略模式：定义 PaymentStrategy 接口，"
                "实现 CreditCardPayment 和 AlipayPayment 两个策略类。"
                "在 ShoppingCart 中根据策略执行支付。"
            ),
            "broken_code": (
                "// 接口\n"
                "interface PaymentStrategy { void pay(double amount); }\n\n"
                "// 两个策略实现...\n\n"
                "// 购物车\n"
                "class ShoppingCart {\n"
                "    private PaymentStrategy strategy;\n"
                "    // 用 setStrategy 切换支付方式\n"
                "    public void checkout(double amount) {\n"
                "        // 用策略支付，而不是 if-else\n"
                "    }\n"
                "}"
            ),
            "hint": "策略类实现 pay(amount) 方法，ShoppingCart 持有 PaymentStrategy 引用，checkout 时调用 strategy.pay(amount)。",
        },
        "study_tips": [
            "优先组合（has-a）而非继承（is-a），更灵活",
            "SOLID 原则（尤其里氏替换和依赖倒置）是写出好 OOP 代码的关键",
            "Stream API + Lambda 表达式让集合操作优雅 10 倍",
        ],
    },
    "C/C++": {
        "emoji": "🔩",
        "file_ext": "cpp",
        "feature_name": "指针与内存管理",
        "feature_blurb": (
            "C/C++ 直接操作内存地址，指针是力量也是风险。"
            "现代 C++（C++11+）提供了智能指针（unique_ptr, shared_ptr, weak_ptr）"
            "让内存安全与手动控制兼得。"
        ),
        "code_example": (
            "#include <iostream>\n"
            "#include <memory>\n\n"
            "int main() {\n"
            "    // 传统裸指针（需手动 delete）\n"
            "    int* raw = new int(42);\n"
            "    std::cout << *raw << std::endl;\n"
            "    delete raw; // 忘记这行就内存泄露！\n\n"
            "    // 现代智能指针（自动析构）\n"
            "    auto smart = std::make_unique<int>(42);\n"
            "    std::cout << *smart << std::endl;\n"
            "    // 无需手动 delete，unique_ptr 离开作用域自动释放\n"
            "}"
        ),
        "fun_fact": "C++ 的 RAII（Resource Acquisition Is Initialization）惯用法让构造函数获取资源、析构函数释放资源，配合智能指针实现'作用域自管理内存'。",
        "mini_exercise": {
            "title": "用 unique_ptr 替代裸指针",
            "description": (
                "将以下裸指针代码改写为使用 std::unique_ptr 的版本，"
                "体会自动内存管理的优雅。"
            ),
            "broken_code": (
                "#include <iostream>\n"
                "int* createBuffer(int size) {\n"
                "    int* buf = new int[size];\n"
                "    for (int i = 0; i < size; i++) buf[i] = i;\n"
                "    return buf;\n"
                "}\n\n"
                "int main() {\n"
                "    int* data = createBuffer(10);\n"
                "    for (int i = 0; i < 10; i++) std::cout << data[i] << ' ';\n"
                "    delete[] data; // 容易忘记！\n"
                "}"
            ),
            "hint": "用 std::unique_ptr<int[]> buf = std::make_unique<int[]>(size)，返回时直接返回 std::move(buf)，main 中无需 delete。",
        },
        "study_tips": [
            "优先用 stack 变量而非 heap，只有需要时才 new",
            "RAII + 智能指针是现代 C++ 的黄金组合",
            "学习 valgrind / AddressSanitizer 帮助你发现内存问题",
        ],
    },
}


# ─────────────────────────────────────────────
# Pomodoro 学习节奏
# ─────────────────────────────────────────────
POMODORO_STEPS = [
    {"step": 1, "label": "🧠 学习", "minutes": 25, "action": "深入理解语言特性"},
    {"step": 2, "label": "⚡ 练习", "minutes": 25, "action": "动手编写代码示例"},
    {"step": 3, "label": "🎯 挑战", "minutes": 25, "action": "完成迷你练习题"},
    {"step": 4, "label": "📝 复盘", "minutes": 5, "action": "总结今日收获"},
]


# ─────────────────────────────────────────────
# 内部工具
# ─────────────────────────────────────────────

def _read_json(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _write_json(path: str, data: Dict[str, Any]) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def _init_history(history_path: str) -> None:
    if not os.path.exists(history_path):
        _write_json(history_path, {"sessions": [], "total_sessions": 0})


def _save_session(history_path: str, session: Dict[str, Any]) -> None:
    _init_history(history_path)
    hist = _read_json(history_path)
    hist["sessions"].insert(0, session)
    hist["sessions"] = hist["sessions"][:50]  # 最多保留 50 条
    hist["total_sessions"] = hist.get("total_sessions", 0) + 1
    _write_json(history_path, hist)


# ─────────────────────────────────────────────
# 核心 API
# ─────────────────────────────────────────────

def generate_adventure(
    json_path: str = DEFAULT_LANGUAGE_ROTATION_JSON,
    history_path: str = DEFAULT_COMPANION_HISTORY_JSON,
) -> Dict[str, Any]:
    """
    读取 language_rotation.json，取出当前语言，生成探险报告，
    更新 JSON 索引，记录历史。

    Returns:
        {
            "language": str,
            "emoji": str,
            "feature_name": str,
            "feature_blurb": str,
            "code_example": str,
            "fun_fact": str,
            "mini_exercise": dict,
            "study_tips": list,
            "pomodoro_steps": list,
            "session_id": str,
            "generated_at": str,
        }
    """
    data = _read_json(json_path)
    languages = data["languages"]
    total = len(languages)
    idx = data.get("current_index", 0) % total
    current = languages[idx]

    adventure = LANGUAGE_ADVENTURES.get(current, {})
    session_id = datetime.now().strftime("%Y%m%d%H%M%S%f")

    result = {
        "language": current,
        "emoji": adventure.get("emoji", "📦"),
        "feature_name": adventure.get("feature_name", "语言特性"),
        "feature_blurb": adventure.get("feature_blurb", ""),
        "code_example": adventure.get("code_example", ""),
        "fun_fact": adventure.get("fun_fact", ""),
        "mini_exercise": adventure.get("mini_exercise", {}),
        "study_tips": adventure.get("study_tips", []),
        "pomodoro_steps": POMODORO_STEPS,
        "session_id": session_id,
        "generated_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00"),
    }

    # 推进索引
    next_idx = (idx + 1) % total
    data["current_index"] = next_idx
    data["last_language"] = current
    data["updated_at"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00")
    _write_json(json_path, data)

    # 记录历史
    _save_session(history_path, {
        "session_id": session_id,
        "language": current,
        "feature_name": adventure.get("feature_name", ""),
        "generated_at": result["generated_at"],
    })

    return result


def get_adventure_report(
    language: Optional[str] = None,
    json_path: str = DEFAULT_LANGUAGE_ROTATION_JSON,
) -> str:
    """
    生成语言探险报告文本（Markdown 格式，便于直接展示）。
    不指定 language 时使用当前轮换语言（不推进索引）。
    """
    if language is None:
        data = _read_json(json_path)
        languages = data["languages"]
        idx = data.get("current_index", 0) % len(languages)
        language = languages[idx]

    adventure = LANGUAGE_ADVENTURES.get(language, {})
    emoji = adventure.get("emoji", "📦")
    feature = adventure.get("feature_name", "语言特性")
    blurb = adventure.get("feature_blurb", "")
    code = adventure.get("code_example", "")
    fact = adventure.get("fun_fact", "")
    exercise = adventure.get("mini_exercise", {})
    tips = adventure.get("study_tips", [])

    lines = [
        f"# 🌐 语言探险报告 | {emoji} **{language}**",
        f"",
        f"## 📌 今日特性：{feature}",
        f"",
        f"{blurb}",
        f"",
        f"## 💻 代码示例",
        f"```" + language.lower().replace("/", "") + f"\n{code}\n```",
        f"",
        f"## 🧪 迷你练习",
        f"**{exercise.get('title', '练习')}**",
        f"",
        f"{exercise.get('description', '')}",
        f"",
        f"```\n{exercise.get('broken_code', '')}\n```",
        f"",
        f"> 💡 提示：{exercise.get('hint', '')}",
        f"",
        f"## 📚 学习小贴士",
    ]
    for tip in tips:
        lines.append(f"- {tip}")

    lines.extend([
        f"",
        f"## 🍅 Pomodoro 学习节奏（100 分钟）",
    ])
    for step in POMODORO_STEPS:
        lines.append(f"- **{step['label']}** ({step['minutes']}min)：{step['action']}")

    lines.extend([
        f"",
        f"## 🔍 你知道吗？",
        f"{fact}",
        f"",
        f"---",
        f"*探险报告自动生成 | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*",
    ])
    return "\n".join(lines)


def get_companion_stats(
    history_path: str = DEFAULT_COMPANION_HISTORY_JSON,
) -> Dict[str, Any]:
    """
    查询陪伴历史统计（不推进索引）。
    """
    _init_history(history_path)
    hist = _read_json(history_path)
    sessions = hist.get("sessions", [])

    # 语言统计
    lang_counts: Dict[str, int] = {}
    for s in sessions:
        lang = s.get("language", "Unknown")
        lang_counts[lang] = lang_counts.get(lang, 0) + 1

    return {
        "total_sessions": hist.get("total_sessions", 0),
        "session_count": len(sessions),
        "language_counts": lang_counts,
        "recent_sessions": sessions[:5],
    }


# ─────────────────────────────────────────────
# CLI 入口
# ─────────────────────────────────────────────
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Polyglot Companion — 语言学习伴侣")
    sub = parser.add_subparsers(dest="cmd")

    sub.add_parser("adventure", help="生成语言探险报告（推进索引）")
    sub.add_parser("report", help="查看当前语言探险报告（不推进索引）")
    sub.add_parser("stats", help="查看学习统计")
    sub.add_parser("history", help="查看最近探险历史")

    report_parser = sub.add_parser("report", help="查看指定语言的探险报告")
    report_parser.add_argument("language", nargs="?", default=None, help="语言名称（可选）")

    args = parser.parse_args()

    if args.cmd == "adventure":
        result = generate_adventure()
        print(get_adventure_report(result["language"]))
        print(f"\n✅ 探险记录已保存，索引已推进。下一站：{result['language']} → ...")
    elif args.cmd == "report":
        lang = args.language
        print(get_adventure_report(language=lang))
    elif args.cmd == "stats":
        st = get_companion_stats()
        print(f"📊 总探险次数：{st['total_sessions']}")
        print(f"📋 最近记录数：{st['session_count']}")
        print("\n各语言探险次数：")
        for lang, cnt in st["language_counts"].items():
            print(f"  {lang}: {cnt} 次")
    elif args.cmd == "history":
        st = get_companion_stats()
        print("📜 最近 5 次探险：")
        for s in st["recent_sessions"]:
            print(f"  [{s['generated_at']}] {s['language']} — {s['feature_name']}")
    else:
        parser.print_help()

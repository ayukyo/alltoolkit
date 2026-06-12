"""
polyglot_snippet_vault.py — 编程语言代码片段知识库 (Polyglot Snippet Vault)
====================================================================
每次轮换语言时，从该语言的片段库中抽取一条"今日精选片段"——
按类别（算法/惯用法/模式/工具/API）、难度、场景标签组织，
让你每天积累一个可复用的代码片段。

与 language_rotation.json 深度集成：
  1. 读取 current_index，取出当前轮换语言
  2. 从该语言的片段库中随机抽取（或按类别过滤）
  3. 将 current_index 前移一位，更新 updated_at
  4. 记录收藏历史到 vault_log.json

语言轮换顺序（8 种核心语言）：
  Rust → Go → Swift → Kotlin → TypeScript → JavaScript → Java → C/C++ → Rust（循环）

Distinct from existing tools:
  - language_tools:        轮换 + 徽章 + 连击记录
  - polyglot_codex:        代码挑战韬略宝鉴（kata + skeleton + test）
  - polyglot_companion:    语言学习伴侣（特性 + 练习题 + Pomodoro）
  - polyglot_ink:          每日墨讯（谚语 + 能量 + 趣闻）
  - kata_generator:       代码道场（kata 生成器）
  - dev_metrics:           代码复杂度分析
  - compile_cache:         编译缓存行为模拟

Polyglot Snippet Vault 的独特视角：
  代码片段是最小可复用单元——不是完整的 kata，
  不是特性讲解，而是一个"这个语言就是这样写"的真实参照。
  收录惯用法、算法实现、API 调用、错误处理等实用片段，
  配合场景标签，让你需要时能快速检索。

作者：AllToolkit 全自动生成
依赖：仅 Python 标准库（json, datetime, pathlib, random）
====================================================================
"""

import json
import os
import random
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

# ─────────────────────────────────────────────
# 路径配置
# ─────────────────────────────────────────────
_MODULE_DIR = Path(__file__).parent.parent              # alltoolkit-python/
_WORKSPACE_ROOT = _MODULE_DIR.parent                     # workspace/
DEFAULT_LANGUAGE_ROTATION_JSON = str(_WORKSPACE_ROOT / "language_rotation.json")
DEFAULT_VAULT_LOG_JSON = str(_WORKSPACE_ROOT / "polyglot_snippet_vault_log.json")


# ─────────────────────────────────────────────
# 片段类别定义
# ─────────────────────────────────────────────
class Category:
    ALGORITHM   = "algorithm"    # 算法实现
    IDIOM       = "idiom"         # 语言惯用法
    PATTERN     = "pattern"       # 设计模式
    TOOL        = "tool"          # 工具/CLI
    API         = "api"           # 标准库/API 调用
    ERROR       = "error"         # 错误处理
    CONCURRENCY = "concurrency"   # 并发编程
    FP          = "fp"           # 函数式编程
    METAPROGRAM = "metaprogram"   # 元编程/泛编程


CATEGORIES = [
    Category.ALGORITHM, Category.IDIOM, Category.PATTERN,
    Category.TOOL, Category.API, Category.ERROR,
    Category.CONCURRENCY, Category.FP, Category.METAPROGRAM,
]

CATEGORY_LABELS: Dict[str, str] = {
    Category.ALGORITHM:   "⚡ 算法",
    Category.IDIOM:       "🏛️ 惯用法",
    Category.PATTERN:     "🏗️ 模式",
    Category.TOOL:       "🛠️ 工具",
    Category.API:        "🔌 API",
    Category.ERROR:      "🛡️ 错误处理",
    Category.CONCURRENCY:"🔀 并发",
    Category.FP:         "λ 函数式",
    Category.METAPROGRAM:"🔮 元编程",
}


# ─────────────────────────────────────────────
# 代码片段知识库（每种语言多类别）
# ─────────────────────────────────────────────
# 每个片段包含：
#   title          : 片段标题
#   category      : 类别
#   difficulty    : 难度 1-3（☆/☆☆/☆☆☆）
#   scenario      : 适用场景描述
#   code          : 代码内容
#   why           : 为什么这个写法好（一句话解释）
#   tags          : 标签列表（便于检索）

SNIPPET_DB: Dict[str, List[Dict[str, Any]]] = {

    "Rust": [
        {
            "title": "Result 链式错误传播",
            "category": Category.ERROR,
            "difficulty": 1,
            "scenario": "多层函数调用中逐层传递错误，用 ? 运算符简化",
            "code": (
                "fn read_config(path: &str) -> Result<Config, Box<dyn std::error::Error>> {\n"
                "    let content = std::fs::read_to_string(path)?;\n"
                "    let config: Config = toml::from_str(&content)?;\n"
                "    Ok(config)\n"
                "}"
            ),
            "why": "? 运算符自动向上传播错误，无需 match 嵌套",
            "tags": ["error-handling", " Result", " ergonomics"],
        },
        {
            "title": "迭代器链式变换",
            "category": Category.FP,
            "difficulty": 1,
            "scenario": "对集合做过滤→映射→收集，常用数据结构操作",
            "code": (
                "let words = vec![\"hello\", \"world\", \"rust\"];\n"
                "let result: Vec<String> = words\n"
                "    .iter()\n"
                "    .filter(|w| w.len() > 4)\n"
                "    .map(|w| w.to_uppercase())\n"
                "    .collect();\n"
                "// result == [\"HELLO\", \"WORLD\"]"
            ),
            "why": "Iterator API 是惰性的，零成本抽象，编译器内联优化",
            "tags": ["iterator", "functional", "collections"],
        },
        {
            "title": "Option 安全解包三剑客",
            "category": Category.IDIOM,
            "difficulty": 2,
            "scenario": "处理可能为空的值，if let / map / unwrap_or 各有所长",
            "code": (
                "let maybe_val: Option<i32> = Some(42);\n\n"
                "// ① map：存在时转换，不存在返回 None\n"
                "let doubled = maybe_val.map(|v| v * 2);\n\n"
                "// ② unwrap_or：不存在时提供默认值\n"
                "let val = maybe_val.unwrap_or(0);\n\n"
                "// ③ if let：匹配单一分支\n"
                "if let Some(v) = maybe_val {\n"
                "    println!(\"got {}\", v);\n"
                "}"
            ),
            "why": "Option 是 Rust 空安全的基础，三种解包方式覆盖不同场景",
            "tags": ["optional", "null-safety", "idiom"],
        },
        {
            "title": "线程安全计数器（Arc + Mutex）",
            "category": Category.CONCURRENCY,
            "difficulty": 2,
            "scenario": "多线程共享状态，需要原子修改",
            "code": (
                "use std::sync::{Arc, Mutex};\n"
                "use std::thread;\n\n"
                "let counter = Arc::new(Mutex::new(0));\n"
                "let mut handles = vec![];\n\n"
                "for _ in 0..10 {\n"
                "    let cnt = Arc::clone(&counter);\n"
                "    handles.push(thread::spawn(move || {\n"
                "        let mut c = cnt.lock().unwrap();\n"
                "        *c += 1;\n"
                "    }));\n"
                "}\n"
                "for h in handles { h.join().unwrap(); }\n"
                "println!(\"{}\", *counter.lock().unwrap()); // 10"
            ),
            "why": "Arc 共享所有权，Mutex 互斥访问，lock() 返回 RAII guard",
            "tags": ["concurrency", "arc", "mutex", "thread"],
        },
        {
            "title": "自定义错误类型 + From",
            "category": Category.ERROR,
            "difficulty": 2,
            "scenario": "定义应用层错误类型，让标准库错误自动转换为你的错误",
            "code": (
                "use std::fmt;\n\n"
                "#[derive(Debug)]\n"
                "enum AppError {\n"
                "    Io(std::io::Error),\n"
                "    Parse(std::num::ParseIntError),\n"
                "    Custom(String),\n"
                "}\n\n"
                "impl From<std::io::Error> for AppError {\n"
                "    fn from(e: std::io::Error) -> Self { AppError::Io(e) }\n"
                "}\n\n"
                "impl From<std::num::ParseIntError> for AppError {\n"
                "    fn from(e: std::num::ParseIntError) -> Self { AppError::Parse(e) }\n"
                "}\n\n"
                "fn parse_port(s: &str) -> Result<u16, AppError> {\n"
                "    let n: i64 = s.parse()?; // 自动 From 转换\n"
                "    Ok(n as u16)\n"
                "}"
            ),
            "why": "impl From 让 ? 运算符自动完成类型转换，错误处理统一又简洁",
            "tags": ["error", "trait", "from", "custom-error"],
        },
        {
            "title": "match 穷举枚举",
            "category": Category.PATTERN,
            "difficulty": 1,
            "scenario": "枚举类型全覆盖处理，编译器保证无遗漏",
            "code": (
                "enum Direction { North, South, East, West }\n\n"
                "fn heading(d: Direction) -> &'static str {\n"
                "    match d {\n"
                "        Direction::North => \"北\",\n"
                "        Direction::South => \"南\",\n"
                "        Direction::East  => \"东\",\n"
                "        Direction::West  => \"西\",\n"
                "    }\n"
                "}"
            ),
            "why": "match 穷尽检查让编译器帮你补漏，新增枚举变体时编译期即报错",
            "tags": ["enum", "pattern-matching", "exhaustive"],
        },
    ],

    "Go": [
        {
            "title": "goroutine + channel 生产者消费者",
            "category": Category.CONCURRENCY,
            "difficulty": 2,
            "scenario": "并发流水线：生产者放入 channel，消费者取出处理",
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
                "}\n\n"
                "for j := 1; j <= 10; j++ { jobs <- j }\n"
                "close(jobs)\n\n"
                "for r := range results {\n"
                "    fmt.Println(\"Result:\", r)\n"
                "}"
            ),
            "why": "goroutine 廉价并发，channel 传递数据而非共享内存，天然避免数据竞争",
            "tags": ["goroutine", "channel", "pipeline", "concurrency"],
        },
        {
            "title": "error 包装与链式检查",
            "category": Category.ERROR,
            "difficulty": 1,
            "scenario": "分层错误处理，每层包装更多上下文，顶层用 errors.Is 检查",
            "code": (
                "package main\n\n"
                "import (\n"
                "    \"errors\"\n"
                "    \"fmt\"\n"
                ")\n\n"
                "var ErrNotFound = errors.New(\"not found\")\n\n"
                "func f3() error {\n"
                "    return fmt.Errorf(\"f3: %w\", ErrNotFound)\n"
                "}\n\n"
                "func f2() error { return f3() }\n\n"
                "func f1() error { return f2() }\n\n"
                "func main() {\n"
                "    if err := f1(); err != nil {\n"
                "        if errors.Is(err, ErrNotFound) {\n"
                "            fmt.Println(\"got not found\")\n"
                "        }\n"
                "    }\n"
                "}"
            ),
            "why": "%w 包装错误保留链条，errors.Is 可以顺着链条向上查找根源",
            "tags": ["error", "wrap", "errors-is", "propagation"],
        },
        {
            "title": "切片引用 vs 拷贝",
            "category": Category.IDIOM,
            "difficulty": 1,
            "scenario": "理解 Go 切片的底层结构（ptr + len + cap），避免意外修改原数据",
            "code": (
                "original := []int{1, 2, 3, 4, 5}\n\n"
                "// 引用切片（共享底层数组）\n"
                "sliceA := original[1:4] // [2, 3, 4]\n\n"
                "// 完全拷贝（独立副本）\n"
                "sliceB := make([]int, len(original))\n"
                "copy(sliceB, original)\n\n"
                "sliceA[0] = 99 // 影响 original！\n"
                "sliceB[0] = 88 // 不影响 original\n"
                "// original 现在是 [1, 99, 3, 4, 5]"
            ),
            "why": "切片是底层数组的视图（view），理解这一点才能避免踩坑",
            "tags": ["slice", "copy", "reference", "idiom"],
        },
        {
            "title": "defer 释放资源",
            "category": Category.IDIOM,
            "difficulty": 1,
            "scenario": "打开文件/连接后必须释放，用 defer 确保调用",
            "code": (
                "func readFile(path string) (string, error) {\n"
                "    f, err := os.Open(path)\n"
                "    if err != nil {\n"
                "        return \"\", err\n"
                "    }\n"
                "    defer f.Close() // 无论函数怎么返回都会执行\n\n"
                "    content, err := io.ReadAll(f)\n"
                "    if err != nil {\n"
                "        return \"\", err\n"
                "    }\n"
                "    return string(content), nil\n"
                "}"
            ),
            "why": "defer 在函数退出时逆序执行，资源释放和打开总是配对",
            "tags": ["defer", "resource", "file", "cleanup"],
        },
        {
            "title": "WaitGroup 等待并发任务",
            "category": Category.CONCURRENCY,
            "difficulty": 1,
            "scenario": "启动多个 goroutine，主线程等待所有子任务完成后再继续",
            "code": (
                "package main\n\n"
                "import (\n"
                "    \"fmt\"\n"
                "    \"sync\"\n"
                "    \"time\"\n"
                ")\n\n"
                "func main() {\n"
                "    var wg sync.WaitGroup\n"
                "    for i := 0; i < 5; i++ {\n"
                "        wg.Add(1)\n"
                "        go func(id int) {\n"
                "            defer wg.Done()\n"
                "            time.Sleep(100 * time.Millisecond)\n"
                "            fmt.Println(\"done\", id)\n"
                "        }(i)\n"
                "    }\n"
                "    wg.Wait() // 等待所有 goroutine 完成\n"
                "    fmt.Println(\"all done\")\n"
                "}"
            ),
            "why": "Add/Done/Wait 三步走，结构清晰，比 channel 更适合批量等待",
            "tags": ["waitgroup", "concurrency", "sync", "goroutine"],
        },
        {
            "title": "interface 空接口与类型断言",
            "category": Category.API,
            "difficulty": 2,
            "scenario": "接受任意类型参数，根据具体类型做不同处理",
            "code": (
                "func printAny(v interface{}) {\n"
                "    switch val := v.(type) {\n"
                "    case string:\n"
                "        fmt.Println(\"string:\", val)\n"
                "    case int:\n"
                "        fmt.Println(\"int:\", val)\n"
                "    case []int:\n"
                "        fmt.Println(\"slice of int:\", val)\n"
                "    default:\n"
                "        fmt.Printf(\"unknown: %T\\n\", v)\n"
                "    }\n"
                "}"
            ),
            "why": "空接口（interface{}）可存任意类型，type switch 做运行时类型分支",
            "tags": ["interface", "type-assertion", "polymorphism", "any"],
        },
    ],

    "Swift": [
        {
            "title": "guard let 安全解包",
            "category": Category.IDIOM,
            "difficulty": 1,
            "scenario": "提前退出（early return）场景，guard let 是最佳选择",
            "code": (
                "func greet(name: String?) {\n"
                "    guard let name = name else {\n"
                "        print(\"Hello, stranger!\")\n"
                "        return\n"
                "    }\n"
                "    print(\"Hello, \\(name)!\")\n"
                "    // 这里 name 是非 Optional，作用域持续到函数结束\n"
                "}"
            ),
            "why": "guard let 在 else 分支必须 return/throw，Optional 变量在主路径可用",
            "tags": ["optional", "guard", "safe", "unwrap"],
        },
        {
            "title": "map / compactMap / filter 链",
            "category": Category.FP,
            "difficulty": 1,
            "scenario": "集合的函数式变换：过滤 nil → 转换 → 收集",
            "code": (
                "let strings = [\"1\", \"2\", \"hello\", \"3\"]\n\n"
                "// compactMap：过滤 nil，同时类型转换\n"
                "let numbers = strings.compactMap { Int($0) }\n"
                "// numbers == [1, 2, 3]\n\n"
                "// filter + map 链\n"
                "let doubleEvens = strings\n"
                "    .compactMap { Int($0) }\n"
                "    .filter { $0 % 2 == 0 }\n"
                "    .map { $0 * 2 }\n"
                "// doubleEvens == [4]"
            ),
            "why": "链式 API 表达力强，compactMap 同时完成过滤 nil 和类型转换两件事",
            "tags": ["map", "filter", "compactMap", "functional", "optional"],
        },
        {
            "title": "Codable JSON 序列化",
            "category": Category.API,
            "difficulty": 1,
            "scenario": "JSON 和 Swift 模型之间自动转换，一行搞定",
            "code": (
                "struct User: Codable {\n"
                "    let id: Int\n"
                "    let name: String\n"
                "    let email: String?\n"
                "}\n\n"
                "let json = '''\n"
                "{\"id\": 1, \"name\": \"Alice\", \"email\": \"alice@example.com\"}\n"
                "'''.data(using: .utf8)!\n\n"
                "let user = try JSONDecoder().decode(User.self, from: json)\n"
                "print(user.name) // \"Alice\"\n\n"
                "let encoded = try JSONEncoder().encode(user)\n"
                "print(String(data: encoded, encoding: .utf8)!)\n"
                "// {\"id\":1,\"name\":\"Alice\",...}"
            ),
            "why": "Codable 协议让序列化零成本，自动处理嵌套结构和可选类型",
            "tags": ["codable", "json", "serialization", "decode", "encode"],
        },
        {
            "title": "actor 隔离并发状态",
            "category": Category.CONCURRENCY,
            "difficulty": 3,
            "scenario": "多线程访问共享状态，用 actor 确保每次只有一个任务访问",
            "code": (
                "actor Counter {\n"
                "    private var count = 0\n\n"
                "    func increment() {\n"
                "        count += 1\n"
                "    }\n\n"
                "    func getCount() -> Int {\n"
                "        return count\n"
                "    }\n"
                "}\n\n"
                "let counter = Counter()\n"
                "await counter.increment()\n"
                "await counter.increment()\n"
                "let value = await counter.getCount()\n"
                "// value == 2"
            ),
            "why": "actor 是 Swift 并发模型的核心，保证内部状态访问的互斥安全",
            "tags": ["actor", "concurrency", "swifts-concurrency", "isolation"],
        },
        {
            "title": "enum 关联值 + switch 穷举",
            "category": Category.PATTERN,
            "difficulty": 1,
            "scenario": "用 sealed enum 建模有限状态，编译器保证全覆盖",
            "code": (
                "enum Result<T> {\n"
                "    case success(T)\n"
                "    case failure(String)\n"
                "}\n\n"
                "func describe<T>(_ r: Result<T>) -> String {\n"
                "    switch r {\n"
                "    case .success(let v): return \"Got: \\(v)\"\n"
                "    case .failure(let msg): return \"Error: \\(msg)\"\n"
                "    }\n"
                "}"
            ),
            "why": "关联值 enum 让每种状态携带数据，switch 穷尽检查保证无遗漏",
            "tags": ["enum", "result", "pattern-matching", "exhaustive"],
        },
        {
            "title": "Lazy 懒加载属性",
            "category": Category.IDIOM,
            "difficulty": 1,
            "scenario": "属性第一次访问时才初始化，避免浪费计算资源",
            "code": (
                "class DataLoader {\n"
                "    lazy var heavyData: [Byte] = {\n"
                "        print(\"Loading heavy data...\")\n"
                "        return loadFromDisk()\n"
                "    }()\n\n"
                "    func loadFromDisk() -> [Byte] {\n"
                "        // 模拟耗时操作\n"
                "        return [0, 1, 2, 3]\n"
                "    }\n"
                "}\n\n"
                "let loader = DataLoader()\n"
                "// heavyData 尚未加载\n"
                "_ = loader.heavyData // 此刻才触发加载\n"
                "_ = loader.heavyData // 已有缓存，不再加载"
            ),
            "why": "lazy var 是延迟初始化的惯用法，只在首次访问时执行闭包",
            "tags": ["lazy", "property", "performance", "initialization"],
        },
    ],

    "Kotlin": [
        {
            "title": "协程 + suspend 异步函数",
            "category": Category.CONCURRENCY,
            "difficulty": 2,
            "scenario": "非阻塞式异步调用，用 suspend 函数写同步风格代码",
            "code": (
                "import kotlinx.coroutines.*\n\n"
                "suspend fun fetchUser(id: Int): String {\n"
                "    delay(1000L) // 模拟网络请求（不阻塞线程）\n"
                "    return \"User#$id\"\n"
                "}\n\n"
                "fun main() = runBlocking {\n"
                "    val name = async { fetchUser(1) }\n"
                "    println(\"Waiting...\")\n"
                "    println(\"User: ${name.await()}\")\n"
                "}"
            ),
            "why": "suspend 函数可以在不阻塞线程的情况下'暂停'，协程比线程轻量得多",
            "tags": ["coroutine", "suspend", "async", "concurrency"],
        },
        {
            "title": "Scope Functions 链",
            "category": Category.FP,
            "difficulty": 2,
            "scenario": "对同一对象连续执行多个操作，用 with / apply / run 简化",
            "code": (
                "data class Person(var name: String, var age: Int, var city: String)\n\n"
                "val person = Person(\"\", 0, \"\")\n\n"
                "// run：接收者作为 lambda 参数，返回 lambda 结果\n"
                "val result = person.run {\n"
                "    name = \"Alice\"\n"
                "    age = 30\n"
                "    city = \"Beijing\"\n"
                "    \"${this.name} lives in ${this.city}\" // 最后一行是返回值\n"
                "}\n"
                "// result == \"Alice lives in Beijing\""
            ),
            "why": "let/run/with/apply/also 五个 Scope Functions 各有分工，链式调用极简",
            "tags": ["scope-function", "lambda", "chain", "fp"],
        },
        {
            "title": "data class + 解构",
            "category": Category.IDIOM,
            "difficulty": 1,
            "scenario": "数据类自动生成 equals/hashCode/toString 和 componentN 解构函数",
            "code": (
                "data class Point(val x: Int, val y: Int)\n\n"
                "val p = Point(3, 4)\n\n"
                "// 自动生成 component1, component2\n"
                "val (a, b) = p // 解构声明\n"
                "println(\"$a, $b\") // \"3, 4\"\n\n"
                "// copy：创建修改了部分属性的副本\n"
                "val p2 = p.copy(x = 5)\n"
                "// p2 == Point(5, 4)"
            ),
            "why": "data class 自动生成样板代码，copy 让你创建不可变修改版本",
            "tags": ["data-class", "destructuring", "copy", "immutable"],
        },
        {
            "title": "sealed class 穷举状态建模",
            "category": Category.PATTERN,
            "difficulty": 1,
            "scenario": "用 sealed 限制继承，when 表达式自动覆盖所有分支",
            "code": (
                "sealed class Result<out T>\n"
                "data class Success<T>(val data: T): Result<T>()\n"
                "data class Error(val message: String): Result<Nothing>()\n"
                "object Loading : Result<Nothing>()\n\n"
                "fun <T> handle(result: Result<T>) = when(result) {\n"
                "    is Success -> \"Got: ${result.data}\"\n"
                "    is Error -> \"Error: ${result.message}\"\n"
                "    is Loading -> \"Loading...\"\n"
                "    // 编译器保证全覆盖，添加新变体时强制处理"
            ),
            "why": "sealed 限制子类型数量，编译器穷尽检查让 when 无需 else 分支",
            "tags": ["sealed", "when", "pattern-matching", "exhaustive"],
        },
        {
            "title": "lateinit 延迟初始化",
            "category": Category.IDIOM,
            "difficulty": 1,
            "scenario": "属性暂时无法初始化（如依赖注入），在首次使用前赋值即可",
            "code": (
                "class NetworkClient {\n"
                "    lateinit var baseUrl: String // 非空类型，延迟赋值\n\n"
                "    fun connect() {\n"
                "        if (::baseUrl.isInitialized) {\n"
                "            println(\"Connecting to $baseUrl\")\n"
                "        }\n"
                "    }\n"
                "}\n\n"
                "val client = NetworkClient()\n"
                "client.baseUrl = \"https://api.example.com\"\n"
                "client.connect()"
            ),
            "why": "lateinit 让你延迟赋值，避免在构造函数中强制初始化",
            "tags": ["lateinit", "property", "initialization", "dependency-injection"],
        },
        {
            "title": "inline 泛型 + reified 类型参数",
            "category": Category.METAPROGRAM,
            "difficulty": 3,
            "scenario": "在泛型函数内获取运行时的实际类型，用于 JSON 解析等场景",
            "code": (
                "import kotlinx.serialization.json.*\n\n"
                "inline fun <reified T: Any> parseJson(json: String): T {\n"
                "    return Json.decodeFromString<T>(json)\n"
                "}\n\n"
                "data class User(val name: String, val age: Int)\n\n"
                "val user = parseJson<User>('{\"name\":\"Bob\",\"age\":25}')\n"
                "// user 的类型在运行时依然可知（普通泛型会擦除）"
            ),
            "why": "reified 让 T 在运行时可见，内联函数避免类型擦除，配合 kotlinx.serialization",
            "tags": ["reified", "inline", "generics", "reflection", "serialization"],
        },
    ],

    "TypeScript": [
        {
            "title": "泛型约束 + 索引访问",
            "category": Category.METAPROGRAM,
            "difficulty": 2,
            "scenario": "从对象类型中提取部分键值，类型安全且灵活",
            "code": (
                "function pick<T, K extends keyof T>(\n"
                "    obj: T,\n"
                "    keys: K[]\n"
                "): Pick<T, K> {\n"
                "    return keys.reduce((acc, k) => {\n"
                "        acc[k] = obj[k]\n"
                "        return acc\n"
                "    }, {} as Pick<T, K>)\n"
                "}\n\n"
                "const user = { name: \"Alice\", age: 30, active: true }\n"
                "const picked = pick(user, [\"name\", \"age\"])\n"
                "// typed as { name: string; age: number } ✓"
            ),
            "why": "泛型约束 K extends keyof T 保证键属于对象，Pick<T, K> 精确返回子集",
            "tags": ["generics", "pick", "keyof", "mapped-types"],
        },
        {
            "title": "唯象类型映射",
            "category": Category.METAPROGRAM,
            "difficulty": 2,
            "scenario": "将对象所有属性递归设为只读，用于配置等不可变数据",
            "code": (
                "type DeepReadonly<T> = T extends (infer U)[]\n"
                "    ? ReadonlyArray<DeepReadonly<U>>\n"
                "    : T extends object\n"
                "    ? { readonly [K in keyof T]: DeepReadonly<T[K]> }\n"
                "    : T;\n\n"
                "type Config = DeepReadonly<{\n"
                "    api: { url: string; timeout: number };\n"
                "    tags: string[];\n"
                "}>;\n"
                "// Config.api.url 是 readonly string\n"
                "// Config.tags 是 ReadonlyArray<string>"
            ),
            "why": "条件类型 + 映射类型组合实现递归深度只读，数组元素也一并处理",
            "tags": ["deep-readonly", "mapped-types", "conditional-types", "recursive"],
        },
        {
            "title": "infer 条件类型提取",
            "category": Category.METAPROGRAM,
            "difficulty": 3,
            "scenario": "从类型中提取特定部分，如从 Promise 提取 resolve 的类型",
            "code": (
                "// 提取 Promise<T> 中的 T\n"
                "type Awaited<T> = T extends Promise<infer U>\n"
                "    ? Awaited<U>\n"
                "    : T;\n\n"
                "type R = Awaited<Promise<Promise<string>>>;\n"
                "// R == string（递归提取到最内层）\n\n"
                "// 提取函数返回类型\n"
                "type ReturnType<T extends (...args: any) => any> =\n"
                "    T extends (...args: any) => infer R ? R : never;"
            ),
            "why": "infer 在条件类型中'捕获'未知部分，配合 extends 实现类型模式匹配",
            "tags": ["infer", "conditional-types", "promise", "return-type"],
        },
        {
            "title": "satisfies 运算符",
            "category": Category.IDIOM,
            "difficulty": 2,
            "scenario": "验证对象字面量满足类型约束，同时保留字面量类型推断",
            "code": (
                "type Config = {\n"
                "    endpoint: string;\n"
                "    port: number;\n"
                "    retries: number;\n"
                "}\n\n"
                "const config = {\n"
                "    endpoint: \"https://api.example.com\",\n"
                "    port: 443,\n"
                "    retries: 3,\n"
                "} satisfies Config;\n\n"
                "// config.endpoint 是 \"https://api.example.com\"（字面量类型）\n"
                "// 而非 string（宽类型）\n"
                "type Endpoint = typeof config.endpoint;\n"
                "// Endpoint == \"https://api.example.com\""
            ),
            "why": "satisfies 让你既能验证类型，又能保留字面量推断，避免类型拓宽（widening）",
            "tags": ["satisfies", "type-inference", "object-literal", "nARRowing"],
        },
        {
            "title": "Record 类型构造",
            "category": Category.API,
            "difficulty": 1,
            "scenario": "用联合类型键构建精确类型的字典对象",
            "code": (
                "type Status = \"active\" | \"inactive\" | \"pending\"\n\n"
                "const statusMap: Record<Status, { label: string; color: string }> = {\n"
                "    active: { label: \"Active\", color: \"green\" },\n"
                "    inactive: { label: \"Inactive\", color: \"gray\" },\n"
                "    pending: { label: \"Pending\", color: \"yellow\" },\n"
                "}\n\n"
                "// statusMap.inactive.color == \"gray\" ✓\n"
                "// statusMap.something // 类型错误 ✓"
            ),
            "why": "Record<Keys, Values> 保证键集合精确匹配，遗漏或多余键都有类型错误",
            "tags": ["record", "mapped-types", "object", "dictionary"],
        },
        {
            "title": "namespace 批量导出工具函数",
            "category": Category.TOOL,
            "difficulty": 1,
            "scenario": "将相关工具函数组织在同一个命名空间下，避免全局污染",
            "code": (
                "namespace StringUtils {\n"
                "    export function capitalize(s: string): string {\n"
                "        return s.charAt(0).toUpperCase() + s.slice(1)\n"
                "    }\n\n"
                "    export function camelCase(s: string): string {\n"
                "        return s.replace(/[-_](\\w)/g, (_, c) => c.toUpperCase())\n"
                "    }\n"
                "}\n\n"
                "console.log(StringUtils.capitalize(\"hello world\"))\n"
                "// \"Hello world\""
            ),
            "why": "namespace 是 TS 的模块化语法，比 IIFE 更清晰，支持类型和值混合导出",
            "tags": ["namespace", "module", "utility", "export"],
        },
    ],

    "JavaScript": [
        {
            "title": "async/await 顺序延时",
            "category": Category.CONCURRENCY,
            "difficulty": 1,
            "scenario": "依次执行多个异步任务（串行），比 Promise 链更可读",
            "code": (
                "const delay = ms => new Promise(res => setTimeout(res, ms));\n\n"
                "async function runTasks() {\n"
                "    await delay(100); console.log(\"Task 1 done\");\n"
                "    await delay(100); console.log(\"Task 2 done\");\n"
                "    await delay(100); console.log(\"Task 3 done\");\n"
                "}\n\n"
                "runTasks(); // 总耗时约 300ms"
            ),
            "why": "async/await 让异步代码写成同步风格，await 顺序执行保证串行",
            "tags": ["async", "await", "promise", "delay", "serial"],
        },
        {
            "title": "Proxy 实现响应式数据绑定",
            "category": Category.PATTERN,
            "difficulty": 3,
            "scenario": "监听对象属性的读写操作，实现简单的响应式系统",
            "code": (
                "function reactive(obj, onChange) {\n"
                "    return new Proxy(obj, {\n"
                "        set(target, key, value) {\n"
                "            const old = target[key]\n"
                "            target[key] = value\n"
                "            onChange(key, old, value)\n"
                "            return true\n"
                "        },\n"
                "        get(target, key) {\n"
                "            return target[key]\n"
                "        }\n"
                "    })\n"
                "}\n\n"
                "const state = reactive({ count: 0 }, (k, o, n) => {\n"
                "    console.log(`${k}: ${o} → ${n}`)\n"
                "})\n"
                "state.count++ // count: 0 → 1"
            ),
            "why": "Proxy 是 JS 的元对象协议，拦截 get/set 实现数据绑定无需框架",
            "tags": ["proxy", "reactivity", "observable", "metaprogramming"],
        },
        {
            "title": "BigInt 大数运算",
            "category": Category.ALGORITHM,
            "difficulty": 2,
            "scenario": "处理超过 Number.MAX_SAFE_INTEGER 的整数运算",
            "code": (
                "// 超过安全整数的计算\n"
                "const safe = BigInt(Number.MAX_SAFE_INTEGER) // 9007199254740991n\n"
                "const larger = safe + BigInt(1)\n"
                "console.log(larger) // 9007199254740992n\n\n"
                "// 任意精度整数\n"
                "const fact100 = factorial(100n)\n"
                "function factorial(n) {\n"
                "    return n === 0n ? 1n : n * factorial(n - 1n)\n"
                "}\n\n"
                "// fact100 是 158 位数字"
            ),
            "why": "BigInt 是 ES2020 内置的任意精度整数，不存在精度丢失问题",
            "tags": ["bigint", "arbitrary-precision", "integer", "math"],
        },
        {
            "title": "WeakMap 私有属性",
            "category": Category.PATTERN,
            "difficulty": 2,
            "scenario": "用 WeakMap 存储实例私有属性，比 Symbol 更高效且可被 GC",
            "code": (
                "const _cache = new WeakMap();\n\n"
                "class Heavy {\n"
                "    constructor(data) {\n"
                "        _cache.set(this, { data, accessCount: 0 });\n"
                "    }\n\n"
                "    getData() {\n"
                "        const entry = _cache.get(this)\n"
                "        entry.accessCount++\n"
                "        return entry.data\n"
                "    }\n"
                "}\n\n"
                "const h = new Heavy([1, 2, 3])\n"
                "h.getData() // { data: [1,2,3], accessCount: 1 }\n"
                "// WeakMap 的 key 是对象引用，无额外内存负担"
            ),
            "why": "WeakMap 的键是弱引用（不影响 GC），适合存储实例私有数据",
            "tags": ["weakmap", "private", "memory", "gc"],
        },
        {
            "title": "Iterator 实现二叉树前序遍历",
            "category": Category.ALGORITHM,
            "difficulty": 3,
            "scenario": "用 Generator 实现二叉树的前序遍历迭代器，支持懒消费",
            "code": (
                "function* inorderTraversal(node) {\n"
                "    if (!node) return\n"
                "    yield* inorderTraversal(node.left)\n"
                "    yield node.val\n"
                "    yield* inorderTraversal(node.right)\n"
                "}\n\n"
                "const tree = {\n"
                "    val: 1,\n"
                "    left: { val: 2, left: null, right: null },\n"
                "    right: { val: 3, left: null, right: null }\n"
                "}\n\n"
                "for (const v of inorderTraversal(tree)) {\n"
                "    console.log(v) // 2, 1, 3"
            ),
            "why": "Generator 实现迭代器协议，yield* 委托遍历子树，内存高效（按需）",
            "tags": ["iterator", "generator", "tree", "traversal", "algorithm"],
        },
        {
            "title": "Web API — fetch + AbortController 取消请求",
            "category": Category.API,
            "difficulty": 2,
            "scenario": "用 AbortController 在组件卸载或超时时取消正在进行的网络请求",
            "code": (
                "const controller = new AbortController();\n"
                "const timeout = setTimeout(() => controller.abort(), 5000);\n\n"
                "try {\n"
                "    const res = await fetch(url, { signal: controller.signal });\n"
                "    clearTimeout(timeout);\n"
                "    const data = await res.json();\n"
                "    console.log(data);\n"
                "} catch (err) {\n"
                "    if (err.name === 'AbortError') {\n"
                "        console.log('Request cancelled');\n"
                "    } else {\n"
                "        throw err;\n"
                "    }\n"
                "}"
            ),
            "why": "AbortController 是标准的请求取消 API，配合 timeout 实现双重保障",
            "tags": ["fetch", "abort", "cancel", "request", "web-api"],
        },
    ],

    "Java": [
        {
            "title": "Stream API 链式数据流",
            "category": Category.FP,
            "difficulty": 1,
            "scenario": "对集合做过滤→映射→收集，用函数式风格替代循环",
            "code": (
                "List<String> names = List.of(\"Alice\", \"Bob\", \"Charlie\");\n\n"
                "List<String> result = names.stream()\n"
                "    .filter(s -> s.length() > 3)\n"
                "    .map(String::toUpperCase)\n"
                "    .sorted()\n"
                "    .collect(Collectors.toList());\n\n"
                "// result == [\"ALICE\", \"CHARLIE\"]"
            ),
            "why": "Stream API 将数据处理表达为流水线，filter/map/sorted 都是惰性的",
            "tags": ["stream", "lambda", "filter", "map", "collect"],
        },
        {
            "title": "record 简洁数据类（Java 16+）",
            "category": Category.IDIOM,
            "difficulty": 1,
            "scenario": "定义不可变的载体类（DTO、复合键等），record 自动生成构造器和访问器",
            "code": (
                "record Point(int x, int y) {\n"
                "    // 自动生成：\n"
                "    // - 构造器 Point(int x, int y)\n"
                "    // - 访问器 x(), y()\n"
                "    // - equals()、hashCode()、toString()\n\n"
                "    // 可以加验证\n"
                "    public Point {\n"
                "        if (x < 0 || y < 0) throw new IllegalArgumentException();\n"
                "    }\n\n"
                "    // 可以加方法\n"
                "    public double distance() {\n"
                "        return Math.sqrt(x*x + y*y);\n"
                "    }\n"
                "}\n\n"
                "var p = new Point(3, 4);\n"
                "System.out.println(p.x()); // 3"
            ),
            "why": "record 让数据载体类从 20 行减少到 3 行，编译器自动生成标准成员",
            "tags": ["record", "immutable", "data-class", "java16"],
        },
        {
            "title": "Optional 链式空安全",
            "category": Category.ERROR,
            "difficulty": 2,
            "scenario": "链式调用处理可能为空的值，避免嵌套 if (x != null)",
            "code": (
                "Optional<String> name = Optional.of(\"Alice\");\n\n"
                "String result = name\n"
                "    .map(String::toUpperCase)\n"
                "    .filter(s -> s.length() > 3)\n"
                "    .orElse(\"DEFAULT\");\n\n"
                "// result == \"ALICE\"\n\n"
                "// flatMap：处理 Optional 类型的映射\n"
                "Optional<String> city = Optional.of(person)\n"
                "    .flatMap(Person::getAddress)\n"
                "    .flatMap(Address::getCity)\n"
                "    .orElse(\"Unknown\");"
            ),
            "why": "Optional 将'无值'语义提升到类型层面，map/flatMap/orElse 组合覆盖各种空处理场景",
            "tags": ["optional", "null-safety", "map", "flatMap"],
        },
        {
            "title": "CompletableFuture 并发组合",
            "category": Category.CONCURRENCY,
            "difficulty": 3,
            "scenario": "多个异步任务并发执行，然后组合结果，比 Future 更强大",
            "code": (
                "CompletableFuture<String> f1 = CompletableFuture\n"
                "    .supplyAsync(() -> fetchUser());\n"
                "CompletableFuture<Integer> f2 = CompletableFuture\n"
                "    .supplyAsync(() -> calculateScore());\n\n"
                "CompletableFuture<String> combined = f1.thenCombine(f2,\n"
                "    (user, score) -> String.format(\"%s: %d\", user, score)\n"
                ");\n\n"
                "System.out.println(combined.get()); // 等待两者完成"
            ),
            "why": "thenCombine 让你合并两个独立 CompletableFuture 的结果，无需等待",
            "tags": ["completable-future", "async", "concurrency", "combine"],
        },
        {
            "title": "Virtual Threads（Project Loom）",
            "category": Category.CONCURRENCY,
            "difficulty": 2,
            "scenario": "用虚拟线程替代线程池处理大量并发连接，高吞吐低内存",
            "code": (
                "try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {\n"
                "    IntStream.range(0, 100_000).forEach(i -> {\n"
                "        executor.submit(() -> {\n"
                "            Thread.sleep(Duration.ofSeconds(1));\n"
                "            return i;\n"
                "        });\n"
                "    });\n"
                "} // 100k 并发，内存占用的只是虚拟线程栈\n"
                "// 传统线程池：100k 线程 → OOM\n"
                "// 虚拟线程：轻松支持百万并发"
            ),
            "why": "虚拟线程（Virtual Threads）是 Java 21 的重大特性，线程不再占用 OS 栈",
            "tags": ["virtual-threads", "loom", "concurrency", "java21"],
        },
        {
            "title": "模式匹配 + switch（Java 21）",
            "category": Category.PATTERN,
            "difficulty": 2,
            "scenario": "switch 支持模式匹配和条件，告别多层 if-else",
            "code": (
                "static String describe(Object obj) {\n"
                "    return switch (obj) {\n"
                "        case Integer i when i > 0 -> \"正整数: \" + i;\n"
                "        case Integer i -> \"非正整数: \" + i;\n"
                "        case String s && s.length() > 5 -> \"长字符串: \" + s;\n"
                "        case String s -> \"短字符串: \" + s;\n"
                "        case null -> \"null\";\n"
                "        default -> \"其他类型: \" + obj;\n"
                "    };\n"
                "}"
            ),
            "why": "switch 的 pattern matching 让类型分支和条件合并，代码极简且类型安全",
            "tags": ["switch", "pattern-matching", "java21", "polymorphism"],
        },
    ],

    "C/C++": [
        {
            "title": "RAII + 智能指针自动析构",
            "category": Category.IDIOM,
            "difficulty": 1,
            "scenario": "用 unique_ptr 管理堆内存，析构函数自动释放，无需手动 delete",
            "code": (
                "#include <memory>\n\n"
                "#include <iostream>\n\n"
                "class NetworkConnection {\npublic:\n"
                "    NetworkConnection() { std::cout << \"Connected\\n\"; }\n"
                "    ~NetworkConnection() { std::cout << \"Disconnected\\n\"; }\n"
                "    void send(const std::string& data) { /* ... */ }\n"
                "};\n\n\n"
                "void demo() {\n"
                "    auto conn = std::make_unique<NetworkConnection>();\n"
                "    conn->send(\"hello\");\n"
                "    // 函数退出时 conn 析构，~NetworkConnection 自动调用\n"
                "    // 无需手动 close() 或 delete\n"
                "}"
            ),
            "why": "RAII（资源获取即初始化）让析构函数自动释放资源，智能指针确保安全",
            "tags": ["raii", "smart-pointer", "unique-ptr", "resource", "destructor"],
        },
        {
            "title": "模板元编程编译期计算",
            "category": Category.METAPROGRAM,
            "difficulty": 4,
            "scenario": "用模板递归在编译期计算斐波那契第 N 项，无运行时开销",
            "code": (
                "template<int N>\n"
                "struct Fib {\n"
                "    static constexpr int value = Fib<N-1>::value + Fib<N-2>::value;\n"
                "};\n\n"
                "template<>\n"
                "struct Fib<0> { static constexpr int value = 0; };\n\n"
                "template<>\n"
                "struct Fib<1> { static constexpr int value = 1; };\n\n"
                "static_assert(Fib<10>::value == 55, \"Fib(10) must be 55\");\n"
                "static_assert(Fib<20>::value == 6765, \"Fib(20) must be 6765\");"
            ),
            "why": "模板递归在编译期展开，value 是 constexpr，无任何运行时开销",
            "tags": ["template", "metaprogram", "constexpr", "fibonacci", "compile-time"],
        },
        {
            "title": "std::variant 替代联合体",
            "category": Category.PATTERN,
            "difficulty": 2,
            "scenario": "类型安全的联合体，用 std::visit 自动分发到对应处理函数",
            "code": (
                "#include <variant>\n"
                "#include <iostream>\n\n"
                "using Var = std::variant<int, double, std::string>;\n\n"
                "void print(const Var& v) {\n"
                "    std::visit([](const auto& val) {\n"
                "        std::cout << val << '\\n';\n"
                "    }, v);\n"
                "}\n\n"
                "Var v1 = 42;\n"
                "Var v2 = 3.14;\n"
                "Var v3 = std::string(\"hello\");\n\n"
                "print(v1); // 42\n"
                "print(v2); // 3.14\n"
                "print(v3); // hello"
            ),
            "why": "std::variant 是类型安全的 union，std::visit 自动匹配类型处理函数",
            "tags": ["variant", "union", "visitor", "type-safe", "pattern-matching"],
        },
        {
            "title": "原子变量无锁计数",
            "category": Category.CONCURRENCY,
            "difficulty": 2,
            "scenario": "多线程并发修改共享计数器，用 atomic 避免锁",
            "code": (
                "#include <atomic>\n"
                "#include <thread>\n"
                "#include <vector>\n\n"
                "std::atomic<int> counter(0);\n\n"
                "void incr() {\n"
                "    for (int i = 0; i < 1000; ++i) {\n"
                "        counter.fetch_add(1, std::memory_order_relaxed);\n"
                "    }\n"
                "}\n\n"
                "int main() {\n"
                "    std::vector<std::thread> threads;\n"
                "    for (int i = 0; i < 10; ++i) {\n"
                "        threads.emplace_back(incr);\n"
                "    }\n"
                "    for (auto& t : threads) t.join();\n"
                "    std::cout << counter.load() << '\\n'; // 10000"
            ),
            "why": "atomic 变量提供硬件级别的无锁原子操作，比 mutex 更高效",
            "tags": ["atomic", "lock-free", "concurrency", "counter"],
        },
        {
            "title": "Lambda 捕获列表详解",
            "category": Category.FP,
            "difficulty": 2,
            "scenario": "Lambda 表达式的各种捕获方式：值捕获、引用捕获、this、init",
            "code": (
                "int x = 10;\n"
                "auto l1 = [x](int y) { return x + y; }; // 值捕获（副本）\n"
                "auto l2 = [&x](int y) { return x + y; }; // 引用捕获\n"
                "auto l3 = [=](int y) { return x + y; }; // 按值捕获所有\n"
                "auto l4 = [&](int y) { x++; return x + y; }; // 按引用捕获所有\n"
                "auto l5 = [x, &y](int z) { return x + y + z; }; // 混合\n"
                "auto l6 = [str = x * 2](int y) { return str + y; }; // 初始化捕获\n\n"
                "x = 20;\n"
                "// l1(5) == 15（x 仍是 10 的副本）\n"
                "// l4(5) == 25（x 已被 l4 修改为 20）"
            ),
            "why": "捕获列表决定 Lambda 如何访问外部变量，混合使用满足不同需求",
            "tags": ["lambda", "capture", "closure", "functional"],
        },
        {
            "title": "移动语义 + std::move",
            "category": Category.IDIOM,
            "difficulty": 2,
            "scenario": "用移动语义避免大型对象的深拷贝，提升性能",
            "code": (
                "#include <vector>\n"
                "#include <utility> // std::move\n\n"
                "std::vector<int> makeBigVector() {\n"
                "    std::vector<int> v(1000, 42);\n"
                "    return v; // NRVO 优化，无需移动\n"
                "}\n\n"
                "void process(std::vector<int> v) { /* ... */ }\n\n\n"
                "std::vector<int> big = makeBigVector();\n"
                "process(std::move(big)); // 移动而非拷贝\n"
                "// big 现在是空 vector（已转移内部指针）\n"
                "// process 内部拥有 1000 个 int 的堆内存"
            ),
            "why": "移动语义将资源所有权转移而非拷贝，std::move 是类型转换提示",
            "tags": ["move", "semantics", "rvalue", "performance", "vector"],
        },
    ],
}


# ─────────────────────────────────────────────
# 工具函数
# ─────────────────────────────────────────────

def _read_json(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    if not content:
        return {"entries": [], "total_snippets": 0}
    return json.loads(content)


def _write_json(path: str, data: Dict[str, Any]) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def _init_log(log_path: str) -> None:
    if not os.path.exists(log_path):
        _write_json(log_path, {"entries": [], "total_snippets": 0})


def _save_entry(log_path: str, entry: Dict[str, Any]) -> None:
    _init_log(log_path)
    log = _read_json(log_path)
    log["entries"].insert(0, entry)
    log["entries"] = log["entries"][:200]   # 最多保留 200 条
    log["total_snippets"] = log.get("total_snippets", 0) + 1
    _write_json(log_path, log)


# ─────────────────────────────────────────────
# 核心 API
# ─────────────────────────────────────────────

# 核心语言轮换顺序（8 种）
CORE_LANGUAGES: List[str] = [
    "Rust", "Go", "Swift", "Kotlin",
    "TypeScript", "JavaScript", "Java", "C/C++",
]


def get_snippet(
    language: Optional[str] = None,
    category: Optional[str] = None,
    difficulty: Optional[int] = None,
    json_path: str = DEFAULT_LANGUAGE_ROTATION_JSON,
    log_path: str = DEFAULT_VAULT_LOG_JSON,
    seed: Optional[int] = None,
) -> Dict[str, Any]:
    """
    获取一个代码片段。

    搜索策略（优先级递减）：
      1. 若指定了 language + category + difficulty → 精确匹配
      2. 若指定了 language + category → 语言内类别筛选
      3. 若指定了 language → 语言内随机
      4. 否则读取 language_rotation.json，按 current_index 取当前语言，随机抽取

    抽取后：
      - 将 language_rotation.json 的 current_index 前移一位
      - 将本次记录追加到 vault_log.json

    Returns:
        {
            "language": str,
            "category": str,
            "category_label": str,
            "difficulty": int,
            "difficulty_stars": str,
            "title": str,
            "scenario": str,
            "code": str,
            "why": str,
            "tags": list,
            "next_language": str,
            "vault_index": int,      # 第几次收藏
            "generated_at": str,
        }
    """
    # ── 1. 读取 rotation JSON ─────────────────────────────────────
    data = _read_json(json_path)
    languages = data["languages"]
    total = len(languages)
    idx = data.get("current_index", 0) % total

    # 确定目标语言
    if language is None:
        target_lang = languages[idx]
    else:
        target_lang = language

    # ── 2. 筛选片段 ──────────────────────────────────────────────
    pool = SNIPPET_DB.get(target_lang, [])
    if not pool:
        # 兜底：生成通用片段
        return _fallback_snippet(target_lang, idx, languages, log_path, json_path)

    # 按类别过滤
    if category:
        pool = [s for s in pool if s["category"] == category]

    # 按难度过滤
    if difficulty is not None:
        pool = [s for s in pool if s["difficulty"] == difficulty]

    if not pool:
        # 兜底：放宽难度限制，语言内任意难度
        pool = SNIPPET_DB.get(target_lang, [])
        if not pool:
            return _fallback_snippet(target_lang, idx, languages, log_path, json_path)

    # 随机抽取
    rng = random.Random(seed)
    snippet = rng.choice(pool)

    # ── 3. 推进索引（只有未指定 language 时才推进）───
    if language is None:
        next_idx = (idx + 1) % total
        data["current_index"] = next_idx
        data["last_language"] = target_lang
        data["updated_at"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00")
        _write_json(json_path, data)

    # ── 4. 记录到 vault log ─────────────────────────────────────
    _init_log(log_path)
    log = _read_json(log_path)
    vault_index = log.get("total_snippets", 0) + 1
    entry = {
        "vault_index": vault_index,
        "language": target_lang,
        "category": snippet["category"],
        "title": snippet["title"],
        "difficulty": snippet["difficulty"],
        "generated_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00"),
    }
    _save_entry(log_path, entry)

    # ── 5. 构建返回结果 ─────────────────────────────────────────
    diff = snippet["difficulty"]
    diff_stars = "☆" * diff + "☆" * (3 - diff)

    return {
        "language": target_lang,
        "category": snippet["category"],
        "category_label": CATEGORY_LABELS.get(snippet["category"], snippet["category"]),
        "difficulty": diff,
        "difficulty_stars": diff_stars,
        "title": snippet["title"],
        "scenario": snippet["scenario"],
        "code": snippet["code"],
        "why": snippet["why"],
        "tags": snippet["tags"],
        "next_language": languages[(idx + 1) % total] if language is None else languages[(idx + 1) % total],
        "vault_index": vault_index,
        "generated_at": entry["generated_at"],
    }


def _fallback_snippet(
    language: str,
    idx: int,
    languages: List[str],
    log_path: str,
    json_path: str,
) -> Dict[str, Any]:
    """兜底片段（语言库为空时使用）"""
    now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00")
    return {
        "language": language,
        "category": Category.IDIOM,
        "category_label": CATEGORY_LABELS[Category.IDIOM],
        "difficulty": 1,
        "difficulty_stars": "☆☆☆",
        "title": f"{language} Hello World",
        "scenario": f"用 {language} 打印 'Hello, World!'",
        "code": f"// 在这里用 {language} 写你的第一个程序",
        "why": f"{language} 是现代主流编程语言之一",
        "tags": [language.lower()],
        "next_language": languages[(idx + 1) % len(languages)],
        "vault_index": 0,
        "generated_at": now,
    }


def search_snippets(
    keyword: str,
    language: Optional[str] = None,
    category: Optional[str] = None,
    difficulty: Optional[int] = None,
) -> List[Dict[str, Any]]:
    """
    在片段库中检索标题/场景/标签包含 keyword 的片段。

    Returns:
        匹配的片段列表（不推进索引，不记录日志）
    """
    results = []
    langs = [language] if language else CORE_LANGUAGES

    for lang in langs:
        pool = SNIPPET_DB.get(lang, [])
        for s in pool:
            if category and s["category"] != category:
                continue
            if difficulty is not None and s["difficulty"] != difficulty:
                continue
            k = keyword.lower()
            if (k in s["title"].lower() or
                k in s["scenario"].lower() or
                k in s["why"].lower() or
                any(k in tag.lower() for tag in s["tags"])):
                results.append({
                    "language": lang,
                    "title": s["title"],
                    "category": s["category"],
                    "category_label": CATEGORY_LABELS.get(s["category"], s["category"]),
                    "difficulty": s["difficulty"],
                    "scenario": s["scenario"],
                    "tags": s["tags"],
                })
    return results


def get_vault_stats(log_path: str = DEFAULT_VAULT_LOG_JSON) -> Dict[str, Any]:
    """
    从 vault_log.json 读取收藏统计。
    """
    _init_log(log_path)
    log = _read_json(log_path)
    entries = log.get("entries", [])

    lang_counts: Dict[str, int] = {}
    cat_counts: Dict[str, int] = {}
    for e in entries:
        lang_counts[e["language"]] = lang_counts.get(e["language"], 0) + 1
        cat_counts[e["category"]] = cat_counts.get(e["category"], 0) + 1

    return {
        "total_snippets": log.get("total_snippets", 0),
        "language_counts": lang_counts,
        "category_counts": cat_counts,
        "recent_entries": entries[:10],
    }


def get_supported_categories() -> List[Dict[str, str]]:
    """返回所有支持的类别列表。"""
    return [{"id": k, "label": v} for k, v in CATEGORY_LABELS.items()]


# ─────────────────────────────────────────────
# 格式化输出
# ─────────────────────────────────────────────

def format_snippet_console(snippet: Dict[str, Any]) -> str:
    """将片段格式化为控制台 ASCII-art 输出。"""
    lang = snippet["language"]
    emoji_map = {
        "Rust": "🦀", "Go": "🐹", "Swift": "🦅", "Kotlin": "🟣",
        "TypeScript": "🔷", "JavaScript": "🟡", "Java": "☕", "C/C++": "🔩",
    }
    emoji = emoji_map.get(lang, "📦")

    lines = [
        f"  ┌{'─' * 56}┐",
        f"  │ 🍽️  Polyglot Snippet Vault                        #{snippet['vault_index']} │",
        f"  ├{'─' * 56}┤",
        f"  │ {emoji}  {lang:<10}  {snippet['category_label']:<18} "
        f"[{snippet['difficulty_stars']}]         │",
        f"  ├{'─' * 56}┤",
        f"  │ 📝 {snippet['title']:<50}│",
        f"  ├{'─' * 56}┤",
        f"  │ 🎯 场景                                        │",
    ]
    # 分行显示场景（每行最多 52 字符）
    scenario = snippet["scenario"]
    for i in range(0, len(scenario), 52):
        lines.append(f"  │   {scenario[i:i+52]:<52}│")

    lines += [
        f"  ├{'─' * 56}┤",
        f"  │ 💻 代码                                        │",
    ]
    code_lines = snippet["code"].split("\n")
    for cl in code_lines:
        wrapped = [cl[i:i+52] for i in range(0, len(cl), 52)]
        for w in wrapped:
            lines.append(f"  │   {w:<52}│")

    lines += [
        f"  ├{'─' * 56}┤",
        f"  │ 💡 {snippet['why']:<51}│",
    ]

    if snippet["tags"]:
        tags_str = "  ".join(f"#{t}" for t in snippet["tags"])
        for i in range(0, len(tags_str), 52):
            lines.append(f"  │   {tags_str[i:i+52]:<52}│")

    lines += [
        f"  ├{'─' * 56}┤",
        f"  │ ⏭️  下一个语言：{snippet['next_language']:<41}│",
        f"  └{'─' * 56}┘",
        f"  saved at: {snippet['generated_at']}",
    ]
    return "\n".join(lines)


def format_snippet_markdown(snippet: Dict[str, Any]) -> str:
    """将片段格式化为 Markdown 文档。"""
    lang = snippet["language"]
    emoji_map = {
        "Rust": "🦀", "Go": "🐹", "Swift": "🦅", "Kotlin": "🟣",
        "TypeScript": "🔷", "JavaScript": "🟡", "Java": "☕", "C/C++": "🔩",
    }
    emoji = emoji_map.get(lang, "📦")

    ext_map = {
        "Rust": "rust", "Go": "go", "Swift": "swift", "Kotlin": "kotlin",
        "TypeScript": "typescript", "JavaScript": "javascript",
        "Java": "java", "C/C++": "cpp",
    }
    ext = ext_map.get(lang, "txt")

    md = [
        f"## 🍽️ Snippet Vault | {lang} {emoji}",
        "",
        f"**{snippet['category_label']}**  [{snippet['difficulty_stars']}]",
        f"",
        f"### 📝 {snippet['title']}",
        "",
        f"**场景：** {snippet['scenario']}",
        "",
        f"``` {ext}",
        snippet["code"],
        "```",
        "",
        f"> 💡 **为什么这样写：** {snippet['why']}",
        "",
        f"**标签：** {'  '.join(f'`{t}`' for t in snippet['tags'])}",
        "",
        f"---",
        f"*#{snippet['vault_index']} · {lang} → {snippet['next_language']} · {snippet['generated_at']}*",
    ]
    return "\n".join(md)


# ─────────────────────────────────────────────
# CLI 入口
# ─────────────────────────────────────────────

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Polyglot Snippet Vault — 代码片段知识库")
    sub = parser.add_subparsers(dest="cmd")

    sub.add_parser("snippet", help="抽取当前轮换语言的代码片段（推进索引）")
    sub.add_parser("stats", help="查看收藏统计")
    sub.add_parser("categories", help="列出所有支持的类别")
    sub.add_parser("search", help="搜索片段").add_argument("keyword", help="搜索关键词")

    snippet_parser = sub.add_parser("get", help="获取指定语言的片段（不推进索引）")
    snippet_parser.add_argument("language", nargs="?", default=None, help="语言名称")
    snippet_parser.add_argument("--category", "-c", default=None, help="类别")
    snippet_parser.add_argument("--difficulty", "-d", type=int, default=None, help="难度 1-3")

    args = parser.parse_args()

    if args.cmd == "snippet":
        result = get_snippet()
        print(format_snippet_console(result))
    elif args.cmd == "get":
        result = get_snippet(language=args.language, category=args.category, difficulty=args.difficulty)
        print(format_snippet_console(result))
    elif args.cmd == "stats":
        st = get_vault_stats()
        print(f"📊 总收藏片段数：{st['total_snippets']}")
        print("\n按语言统计：")
        for lang, cnt in st["language_counts"].items():
            print(f"  {lang}: {cnt} 条")
        print("\n按类别统计：")
        for cat, cnt in st["category_counts"].items():
            print(f"  {cat}: {cnt} 条")
        if st["recent_entries"]:
            print("\n最近 10 条：")
            for e in st["recent_entries"]:
                print(f"  #{e['vault_index']} {e['language']} | {e['category']} | {e['title']}")
    elif args.cmd == "search":
        results = search_snippets(args.keyword)
        print(f"找到 {len(results)} 条匹配：")
        for r in results:
            print(f"  [{r['language']}] {r['title']} ({r['category_label']})")
    elif args.cmd == "categories":
        print("支持的类别：")
        for cat in get_supported_categories():
            print(f"  {cat['id']:<15} {cat['label']}")
    else:
        parser.print_help()
"""
polyglot_codex.py - 编程语言韬略宝鉴 (Polyglot Codex)
====================================================================
一个与 language_rotation.json 深度集成的代码挑战生成器。

核心逻辑：
  1. 读取 language_rotation.json，按 current_index 取当前轮换语言
  2. 生成该语言的代码韬略（kata），包含：主题标签、难度星级、
     问题描述、参考解决骨架、验收测试片段
  3. 记录挑战历史（attempt log）到 JSON
  4. 完成后将 current_index 前移一位并更新 updated_at

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
# 路径配置（与 language_tools.py 保持一致）
# ─────────────────────────────────────────────
_MODULE_DIR = Path(__file__).parent.parent          # alltoolkit-python/
_WORKSPACE_ROOT = _MODULE_DIR.parent                # workspace/
DEFAULT_LANGUAGE_ROTATION_JSON = str(_WORKSPACE_ROOT / "language_rotation.json")
DEFAULT_CODEX_LOG_JSON        = str(_WORKSPACE_ROOT / "polyglot_codex_log.json")


# ─────────────────────────────────────────────
# 语言元数据（精简版，与 language_tools.py 互补）
# ─────────────────────────────────────────────
LANGUAGE_ECOSYSTEM: Dict[str, Dict[str, Any]] = {
    "Rust": {
        "emoji": "🦀",
        "file_ext": "rs",
        "paradigm": "Systems / Memory-safe",
        "kata_templates": [
            {
                "theme": "所有权转移",
                "difficulty": 3,
                "title": "自定义智能指针",
                "description": (
                    "实现一个简化的 Box<T> 智能指针 struct，"
                    "包含 new(data) 构造器、drop 实现（打印 \"dropped!\"）、"
                    "以及 Deref<Target=T> trait，实现解引用返回内部数据。"
                ),
                "skeleton": (
                    "use std::ops::Deref;\n\nstruct MyBox<T>(T);\n\n"
                    "impl<T> MyBox<T> {\n    fn new(data: T) -> Self {{ ... }}\n}}\n\n"
                    "// 实现 Deref trait\nimpl<T> Deref for MyBox<T> {{\n    type Target = T;\n    fn deref(&self) -> &T {{ ... }}\n}}\n\n"
                    "// 实现 Drop trait\nimpl<T> Drop for MyBox<T> {{\n    fn drop(&mut self) {{ println!(\"dropped!\"); }}\n}}"
                ),
                "test_snippet": (
                    "fn main() {{\n    let b = MyBox::new(42);\n    assert_eq!(*b, 42);\n    // drop 被调用时打印 \"dropped!\"\n}}"
                ),
            },
            {
                "theme": "并发安全",
                "difficulty": 4,
                "title": "线程间消息通道",
                "description": (
                    "使用 std::sync::mpsc 实现：主线程向子线程发送一个整数，"
                    "子线程乘以 2 后回传，主线程打印结果。"
                ),
                "skeleton": (
                    "use std::sync::mpsc;\nuse std::thread;\n\nfn main() {{\n    let (tx, rx) = mpsc::channel();\n    // 启动子线程...\n    tx.send(21_i32).unwrap();\n    let result = rx.recv().unwrap();\n    println!(\"Result: {{}}\", result);  // 期望 42\n}}"
                ),
                "test_snippet": (
                    "// 验收：result == 42，且无 panic\n"
                    "// 提示：子线程中 result = x * 2"
                ),
            },
            {
                "theme": "模式匹配",
                "difficulty": 2,
                "title": "Result 链式处理",
                "description": (
                    "给定一个返回 Result<i32, &str> 的函数，"
                    "用 ? 操作符和 match 两种方式处理错误并打印结果。"
                ),
                "skeleton": (
                    "fn try_parse(s: &str) -> Result<i32, &str> {{\n    s.parse::<i32>()\n        .map_err(|_| \"not a number\")\n}}\n\nfn main() {{\n    // 使用 ? 操作符\n    let n = try_parse(\"123\")?;\n    println!(\"Parsed: {{}}\", n);\n}}"
                ),
                "test_snippet": (
                    "assert_eq!(try_parse(\"42\").unwrap(), 42);\n"
                    "assert!(try_parse(\"oops\").is_err());"
                ),
            },
        ],
    },
    "Go": {
        "emoji": "🐹",
        "file_ext": "go",
        "paradigm": "Concurrent / Compiled",
        "kata_templates": [
            {
                "theme": "接口与多态",
                "difficulty": 2,
                "title": "动物叫声模拟器",
                "description": (
                    "定义 Speaker interface（含 Speak() string 方法）。"
                    "实现 Dog、Say、Human 三种类型，实现 Speak。"
                    "写函数 MakeThemSpeak([]Speaker) 依次调用 Speak() 并打印。"
                ),
                "skeleton": (
                    "package main\n\nimport \"fmt\"\n\ntype Speaker interface {\n    Speak() string\n}\n\n// 实现 Dog、Say、Human...\n\nfunc MakeThemSpeak(speakers []Speaker) {{\n    for _, s := range speakers {{\n        fmt.Println(s.Speak())\n    }}\n}}"
                ),
                "test_snippet": (
                    "func TestInterface(t *testing.T) {{\n    animals := []Speaker{{&Dog{{}}, &Say{{word: \"hi\"}}, &Human{{}}}\n    MakeThemSpeak(animals)\n}}"
                ),
            },
            {
                "theme": "goroutine",
                "difficulty": 3,
                "title": "并发累加器",
                "description": (
                    "启动 N 个 goroutine，每个对共享的 sync/atomic Int32 累加 1。"
                    "等待所有 goroutine 结束后验证最终值为 N。"
                ),
                "skeleton": (
                    "package main\n\nimport (\n    \"sync/atomic\"\n    \"fmt\"\n)\n\nfunc main() {{\n    var counter int32\n    N := 1000\n    // 启动 N 个 goroutine...\n    // 每个执行 atomic.AddInt32(&counter, 1)\n    // 等待（sync.WaitGroup）\n    fmt.Println(counter)  // 期望 N\n}}"
                ),
                "test_snippet": (
                    "// 验收：counter == int32(N)，无 data race（用 go run -race 验证）"
                ),
            },
            {
                "theme": "错误处理",
                "difficulty": 2,
                "title": "链式错误包装",
                "description": (
                    "实现三个函数 f1 → f2 → f3，每层返回 error。"
                    "最顶层 main 用 %w 格式化错误，"
                    "用 errors.Is 验证错误链中是否包含特定错误。"
                ),
                "skeleton": (
                    "package main\n\nimport (\n    \"errors\"\n    \"fmt\"\n)\n\nvar ErrNotFound = errors.New(\"not found\")\n\nfunc f3() error {{ return fmt.Errorf(\"f3: %w\", ErrNotFound) }}\nfunc f2() error {{ return f3() }}\nfunc f1() error {{ return f2() }}"
                ),
                "test_snippet": (
                    "func TestErrorChain(t *testing.T) {{\n    err := f1()\n    if !errors.Is(err, ErrNotFound) {{\n        t.Fatal(\"expected ErrNotFound in chain\")\n    }}\n}}"
                ),
            },
        ],
    },
    "Swift": {
        "emoji": "🦅",
        "file_ext": "swift",
        "paradigm": "Multi-paradigm / Safe",
        "kata_templates": [
            {
                "theme": "协议扩展",
                "difficulty": 3,
                "title": "可求和集合",
                "description": (
                    "给 Array extension 添加 sum() 方法（返回 Int），"
                    "要求：只对 Int 元素生效，使用泛型约束 where Element == Int。"
                ),
                "skeleton": (
                    "extension Array where Element == Int {{\n    func sum() -> Int {{\n        // reduce(0, +)\n    }}\n}}"
                ),
                "test_snippet": (
                    "let arr = [1, 2, 3, 4, 5]\n"
                    "assertEqual(arr.sum(), 15)\n"
                    "// [1, 2, 3].sum() == 6"
                ),
            },
            {
                "theme": "Optional",
                "difficulty": 2,
                "title": "安全解包工具",
                "description": (
                    "实现 func safeGet<T>(_ dict: [String: T], key: String) -> T?"
                    "当 key 存在且值非 nil 时返回 Some(value)，否则返回 nil。"
                ),
                "skeleton": (
                    "func safeGet<T>(_ dict: [String: T], key: String) -> T? {{\n    return dict[key]\n}}"
                ),
                "test_snippet": (
                    "let d = [\"name\": \"Alice\" as String?]\n"
                    "assert(safeGet(d, key: \"name\") == \"Alice\")\n"
                    "assert(safeGet(d, key: \"age\") == nil)"
                ),
            },
            {
                "theme": "枚举关联值",
                "difficulty": 3,
                "title": "状态机枚举",
                "description": (
                    "定义 enum NetworkState:关联值 { case loading, success(Data), error(String) }。"
                    "实现 switch 处理三种状态，打印或返回对应字符串。"
                ),
                "skeleton": (
                    "enum NetworkState {{\n    case loading\n    case success(Data)\n    case error(String)\n}}"
                ),
                "test_snippet": (
                    "let s = NetworkState.success(Data(\"hello\"))\n"
                    "// switch s { case .success(let d): assertEqual(d, Data(\"hello\")) ... }"
                ),
            },
        ],
    },
    "Kotlin": {
        "emoji": "🟣",
        "file_ext": "kt",
        "paradigm": "OO / Functional / JVM",
        "kata_templates": [
            {
                "theme": "协程基础",
                "difficulty": 3,
                "title": "顺序执行 vs 并发",
                "description": (
                    "用 runBlocking 启动两个 launch 协程。"
                    "协程1 睡眠 100ms 后打印 \"A\"，"
                    "协程2 睡眠 50ms 后打印 \"B\"，"
                    "验证打印顺序为 B → A（因为 B 先完成）。"
                ),
                "skeleton": (
                    "import kotlinx.coroutines.*\n\nfun main() = runBlocking {{\n    // launch 协程1...\n    // launch 协程2...\n}}"
                ),
                "test_snippet": (
                    "// 验收：收集到的打印顺序为 listOf(\"B\", \"A\")\n"
                    "// 提示：use ArrayList 收集 println 输出"
                ),
            },
            {
                "theme": "数据类与解构",
                "difficulty": 1,
                "title": "坐标点运算",
                "description": (
                    "定义 data class Point(val x: Int, val y: Int)。"
                    "实现 operator fun Point.plus(other: Point) = Point(x+y, y+y)。"
                    "实现 component1/component2（数据类自动提供）。"
                ),
                "skeleton": (
                    "data class Point(val x: Int, val y: Int) {{\n    operator fun plus(other: Point) = Point(x + other.x, y + other.y)\n}}"
                ),
                "test_snippet": (
                    "val p = Point(1, 2) + Point(3, 4)\n"
                    "assertEquals(Point(4, 6), p)"
                ),
            },
            {
                "theme": "扩展函数",
                "difficulty": 2,
                "title": "String 扩展工具",
                "description": (
                    "给 String 扩展两个函数："
                    "isPalindrome(): Boolean（判断回文）和"
                    "wordCount(): Int（统计单词数，按空格分割）。"
                ),
                "skeleton": (
                    "fun String.isPalindrome(): Boolean {{\n    val clean = this.lowercase().filter {{ it.isLetterOrDigit() }}\n    return clean == clean.reversed()\n}}\n\nfun String.wordCount(): Int = this.split(\" \").filter {{ it.isNotBlank() }}.size"
                ),
                "test_snippet": (
                    "assert(\"racecar\".isPalindrome())\n"
                    "assert(!\"hello\".isPalindrome())\n"
                    "assertEquals(3, \"hello world foo\".wordCount())"
                ),
            },
        ],
    },
    "TypeScript": {
        "emoji": "🔷",
        "file_ext": "ts",
        "paradigm": "Typed Superset of JS",
        "kata_templates": [
            {
                "theme": "泛型约束",
                "difficulty": 2,
                "title": "类型安全的键值提取",
                "description": (
                    "实现 function pick<K extends keyof T, T>(\n"
                    "obj: T, keys: K[]): Pick<T, K>，"
                    "从 obj 中提取指定键，返回 Pick<T, K> 类型。"
                ),
                "skeleton": (
                    "function pick<T, K extends keyof T>(obj: T, keys: K[]): Pick<T, K> {{\n    // keys.reduce((acc, k) => ..., {} as Pick<T, K>)\n}}"
                ),
                "test_snippet": (
                    "const user = {{ name: \"Alice\", age: 30, active: true }};\n"
                    "const picked = pick(user, [\"name\", \"age\"]);\n"
                    "// typed as { name: string; age: number }"
                ),
            },
            {
                "theme": "装饰器",
                "difficulty": 4,
                "title": "方法耗时日志装饰器",
                "description": (
                    "实现 @logged 装饰器：包装类方法，"
                    "在调用前后打印 \"[LOG] Entering <method>\" "
                    "和 \"[LOG] Exiting <method> (<elapsed>ms)\"。"
                ),
                "skeleton": (
                    "function logged(target: any, propertyKey: string, descriptor: PropertyDescriptor) {{\n    const original = descriptor.value;\n    descriptor.value = function(...args: any[]) {{\n        console.log(`[LOG] Entering {{propertyKey}}`);\n        const start = Date.now();\n        const result = original.apply(this, args);\n        console.log(`[LOG] Exiting {{propertyKey}} ({{Date.now() - start}}ms)`);\n        return result;\n    }};\n}}"
                ),
                "test_snippet": (
                    "class MyService {{\n    @logged\n    doWork() {{ return 42; }}\n}}\n"
                    "// 验收：调用 doWork() 前后打印日志，无报错"
                ),
            },
            {
                "theme": "工具类型",
                "difficulty": 3,
                "title": "深度只读转换",
                "description": (
                    "实现 DeepReadonly<T>，将对象所有嵌套属性递归设为 readonly。"
                    "提示： mapped types + indexed access types。"
                ),
                "skeleton": (
                    "type DeepReadonly<T> = {{\n    readonly [P in keyof T]: T[P] extends object ? DeepReadonly<T[P]> : T[P]\n}};"
                ),
                "test_snippet": (
                    "type X = DeepReadonly<{{ a: {{ b: number }} }}>;\n"
                    "// X = { readonly a: { readonly b: number } }"
                ),
            },
        ],
    },
    "JavaScript": {
        "emoji": "🟡",
        "file_ext": "js",
        "paradigm": "Dynamic / Prototype-based",
        "kata_templates": [
            {
                "theme": "Proxy 拦截",
                "difficulty": 3,
                "title": "唯读代理",
                "description": (
                    "使用 Proxy 实现只读对象包装器 readOnly(obj)，"
                    "任何写入操作抛出 TypeError。"
                ),
                "skeleton": (
                    "function readOnly(obj) {{\n    return new Proxy(obj, {{\n        set(target, prop, value) {{ throw new TypeError(`\\`${{prop}}\\` is read-only`) }}\n    }});\n}}"
                ),
                "test_snippet": (
                    "const safe = readOnly({{ x: 1 }});\n"
                    "try {{ safe.x = 2; }} catch (e) {{\n    console.log(e instanceof TypeError); // true\n}}"
                ),
            },
            {
                "theme": "迭代器协议",
                "difficulty": 3,
                "title": "无限斐波那契迭代器",
                "description": (
                    "实现斐波那契生成器函数 fibonacci()，"
                    "遵循 iterator protocol，支持 for...of 消费。"
                ),
                "skeleton": (
                    "function* fibonacci() {{\n    let [a, b] = [0, 1];\n    while (true) {{\n        yield a;\n        [a, b] = [b, a + b];\n    }}\n}}"
                ),
                "test_snippet": (
                    "const gen = fibonacci();\n"
                    "[...gen.next(), ...gen.next(), ...gen.next(), ...gen.next()]\n"
                    "// 前四个值：0, 1, 1, 2"
                ),
            },
            {
                "theme": "Promise 链",
                "difficulty": 2,
                "title": "顺序延时执行",
                "description": (
                    "实现 function delay(ms) -> Promise，"
                    "然后用 Promise 链顺序执行 3 个延时任务，"
                    "累计耗时约 300ms（每个 100ms）。"
                ),
                "skeleton": (
                    "const delay = ms => new Promise(resolve => setTimeout(resolve, ms));\n\ndelay(100)\n    .then(() => console.log(\"Task 1\"))\n    .then(() => delay(100))\n    .then(() => console.log(\"Task 2\"))\n    .then(() => delay(100))\n    .then(() => console.log(\"Task 3\"));"
                ),
                "test_snippet": (
                    "// 验收：三个 console.log 顺序执行，总耗时约 300ms\n"
                    "// 提示：用 Promise.all 可并行化"
                ),
            },
        ],
    },
    "Java": {
        "emoji": "☕",
        "file_ext": "java",
        "paradigm": "OO / Class-based / JVM",
        "kata_templates": [
            {
                "theme": "Stream API",
                "difficulty": 2,
                "title": "交易流水处理",
                "description": (
                    "定义 record Transaction(String id, int amount, String type)。"
                    "用 Stream API 筛选 type=\"DEBIT\" 的交易，"
                    "按 amount 降序排列，取前 3 条并计算总额。"
                ),
                "skeleton": (
                    "record Transaction(String id, int amount, String type) {{}}\n\nList<Transaction> result = transactions.stream()\n    .filter(t -> t.type().equals(\"DEBIT\"))\n    .sorted(Comparator.comparingInt(Transaction::amount).reversed())\n    .limit(3)\n    .toList();\nint total = result.stream().mapToInt(Transaction::amount).sum();"
                ),
                "test_snippet": (
                    "// 验收：result 包含 amount 最大的3条DEBIT，total 为其加总"
                ),
            },
            {
                "theme": "函数式接口",
                "difficulty": 2,
                "title": "链式校验器",
                "description": (
                    "实现一个 Validator<T> 类，支持 chain："
                    "validator.add(t -> t > 0, \"must be positive\")"
                    ".add(t -> t < 100, \"must be < 100\")"
                    "，返回 Optional<String>（首个错误信息）。"
                ),
                "skeleton": (
                    "class Validator<T> {{\n    private final List<Predicate<T>> rules = new ArrayList<>();\n    private final List<String> messages = new ArrayList<>();\n\n    public Validator<T> add(Predicate<T> rule, String msg) {{\n        rules.add(rule);\n        messages.add(msg);\n        return this;\n    }}\n\n    public Optional<String> validate(T value) {{\n        // ...\n    }}\n}}"
                ),
                "test_snippet": (
                    "Validator<Integer> v = new Validator<Integer>()\n    .add(x -> x > 0, \"positive\")\n    .add(x -> x < 100, \"< 100\");\n"
                    "assertEquals(Optional.of(\"positive\"), v.validate(-5));\n"
                    "assertEquals(Optional.empty(), v.validate(42));"
                ),
            },
            {
                "theme": "泛型",
                "difficulty": 2,
                "title": "栈数据结构",
                "description": (
                    "实现一个泛型 Stack<T>，包含 push(T)、pop(): T、"
                    "peek(): T、isEmpty(): boolean 方法。"
                ),
                "skeleton": (
                    "class Stack<T> {{\n    private final List<T> items = new ArrayList<>();\n    public void push(T item) {{ items.add(item); }}\n    public T pop() {{ return items.remove(items.size() - 1); }}\n    public T peek() {{ return items.get(items.size() - 1); }}\n    public boolean isEmpty() {{ return items.isEmpty(); }}\n}}"
                ),
                "test_snippet": (
                    "Stack<Integer> s = new Stack<>();\n"
                    "s.push(1); s.push(2); s.push(3);\n"
                    "assertEquals(3, s.pop());\n"
                    "assertEquals(2, s.peek());"
                ),
            },
        ],
    },
    "C/C++": {
        "emoji": "🔩",
        "file_ext": "cpp",
        "paradigm": "Systems / Low-level",
        "kata_templates": [
            {
                "theme": "模板元编程",
                "difficulty": 4,
                "title": "编译期斐波那契",
                "description": (
                    "用 C++ constexpr 模板元编程在编译期计算第 N 个斐波那契数。"
                    "要求：template<int N> struct Fib { static constexpr int value = ...; }。"
                ),
                "skeleton": (
                    "template<int N>\nstruct Fib {{\n    static constexpr int value = Fib<N-1>::value + Fib<N-2>::value;\n}};\n\ntemplate<>\nstruct Fib<0> {{ static constexpr int value = 0; }};\ntemplate<>\nstruct Fib<1> {{ static constexpr int value = 1; }};\n\n// Fib<10>::value == 55"
                ),
                "test_snippet": (
                    "static_assert(Fib<10>::value == 55, \"Fib(10) must be 55\");\n"
                    "static_assert(Fib<20>::value == 6765, \"Fib(20) must be 6765\");"
                ),
            },
            {
                "theme": "RAII",
                "difficulty": 2,
                "title": "作用域锁",
                "description": (
                    "使用 std::lock_guard 实现一个线程安全的 Counter 类。"
                    "incr() 和 decr() 方法在多线程环境下安全递增/递减。"
                ),
                "skeleton": (
                    "class Counter {{\n    std::mutex mtx;\n    int count = 0;\npublic:\n    void incr() {{\n        std::lock_guard<std::mutex> lock(mtx);\n        ++count;\n    }}\n    void decr() {{\n        std::lock_guard<std::mutex> lock(mtx);\n        --count;\n    }}\n    int get() const {{\n        std::lock_guard<std::mutex> lock(mtx);\n        return count;\n    }}\n}};"
                ),
                "test_snippet": (
                    "// 验收：N 个线程各 incr 一次，最终 count == N"
                ),
            },
            {
                "theme": "指针操作",
                "difficulty": 2,
                "title": "手动实现 memcpy",
                "description": (
                    "用 C 风格实现 void* my_memcpy(void* dest, const void* src, size_t n)。"
                    "逐字节复制，处理重叠情况（用 memmove 语义处理重叠）。"
                ),
                "skeleton": (
                    "void* my_memcpy(void* dest, const void* src, size_t n) {{\n    char* d = (char*)dest;\n    const char* s = (const char*)src;\n    for (size_t i = 0; i < n; ++i) {{\n        d[i] = s[i];\n    }}\n    return dest;\n}}"
                ),
                "test_snippet": (
                    "int src[] = {{1,2,3,4,5}};\n"
                    "int dst[5];\n"
                    "my_memcpy(dst, src, sizeof(src));\n"
                    "// dst[2] == 3"
                ),
            },
        ],
    },
}


# ─────────────────────────────────────────────
# 核心：读取语言轮换配置
# ─────────────────────────────────────────────

def _read_rotation_json(json_path: str) -> Dict[str, Any]:
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)


def _write_rotation_json(json_path: str, data: Dict[str, Any]) -> None:
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def _read_codex_log(json_path: str) -> Dict[str, Any]:
    if not os.path.exists(json_path):
        return {"attempts": [], "total_katas": 0}
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)


def _write_codex_log(json_path: str, data: Dict[str, Any]) -> None:
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# ─────────────────────────────────────────────
# 核心 API
# ─────────────────────────────────────────────

# 核心语言轮换顺序（8 种）
CORE_LANGUAGES = [
    "Rust", "Go", "Swift", "Kotlin",
    "TypeScript", "JavaScript", "Java", "C/C++",
]


def generate_kata(
    json_path: str = DEFAULT_LANGUAGE_ROTATION_JSON,
    log_path: str = DEFAULT_CODEX_LOG_JSON,
    seed: Optional[int] = None,
) -> Dict[str, Any]:
    """
    生成当前轮换语言的代码韬略（kata）。

    流程：
      1. 读取 language_rotation.json，取 current_index 所指语言
      2. 从该语言的 kata_templates 列表中随机抽取一个
      3. 将本次挑战记录追加到 polyglot_codex_log.json
      4. 将 language_rotation.json 的 current_index 前移一位，更新 updated_at
      5. 返回完整的 kata 字典

    Returns:
        {
            "language": str,
            "emoji": str,
            "file_ext": str,
            "paradigm": str,
            "theme": str,
            "difficulty": int,        # 1-5 星级
            "title": str,
            "description": str,
            "skeleton": str,
            "test_snippet": str,
            "difficulty_stars": str,  # "★★☆" 风格
            "attempt_index": int,     # 本次是第几次挑战
            "rotation_index": int,    # 当前在轮换表中的位置
            "next_language": str,
        }
    """
    data = _read_rotation_json(json_path)
    languages = data["languages"]
    total = len(languages)
    idx = data.get("current_index", 0) % total
    current = languages[idx]

    # 获取 kata 模板
    ecosystem = LANGUAGE_ECOSYSTEM.get(current)
    if ecosystem is None or not ecosystem.get("kata_templates"):
        # 兜底：生成一个通用 kata
        kata = _generate_fallback_kata(current)
    else:
        rng = random.Random(seed)
        kata = rng.choice(ecosystem["kata_templates"])

    # 更新 language_rotation.json（index 前移）
    next_idx = (idx + 1) % total
    data["current_index"] = next_idx
    data["last_language"] = current
    data["updated_at"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00")
    _write_rotation_json(json_path, data)

    # 追加挑战记录到 log
    log_data = _read_codex_log(log_path)
    attempt_index = log_data["total_katas"] + 1
    log_entry = {
        "attempt": attempt_index,
        "language": current,
        "theme": kata["theme"],
        "title": kata["title"],
        "difficulty": kata["difficulty"],
        "generated_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00"),
    }
    log_data["attempts"].append(log_entry)
    log_data["total_katas"] = attempt_index
    _write_codex_log(log_path, log_data)

    difficulty_stars = "★" * kata["difficulty"] + "☆" * (5 - kata["difficulty"])

    return {
        "language": current,
        "emoji": ecosystem.get("emoji", "📦") if ecosystem else "📦",
        "file_ext": ecosystem.get("file_ext", "txt") if ecosystem else "txt",
        "paradigm": ecosystem.get("paradigm", "") if ecosystem else "",
        "theme": kata["theme"],
        "difficulty": kata["difficulty"],
        "title": kata["title"],
        "description": kata["description"],
        "skeleton": kata["skeleton"],
        "test_snippet": kata["test_snippet"],
        "difficulty_stars": difficulty_stars,
        "attempt_index": attempt_index,
        "rotation_index": idx,
        "next_language": languages[next_idx],
    }


def _generate_fallback_kata(language: str) -> Dict[str, Any]:
    """当语言没有kata模板时的兜底生成"""
    return {
        "theme": "基础练习",
        "difficulty": 1,
        "title": f"{language} Hello World",
        "description": f"用 {language} 打印 'Hello, World!' 到标准输出。",
        "skeleton": "// 在此编写你的代码",
        "test_snippet": "// 验收：程序运行无错误，输出包含 'Hello, World!'",
    }


def get_current_language(
    json_path: str = DEFAULT_LANGUAGE_ROTATION_JSON,
) -> Dict[str, Any]:
    """
    查询当前轮换语言（不推进索引）。
    """
    data = _read_rotation_json(json_path)
    languages = data["languages"]
    idx = data.get("current_index", 0) % len(languages)
    current = languages[idx]
    ecosystem = LANGUAGE_ECOSYSTEM.get(current, {})
    return {
        "language": current,
        "emoji": ecosystem.get("emoji", "📦"),
        "file_ext": ecosystem.get("file_ext", "txt"),
        "paradigm": ecosystem.get("paradigm", ""),
        "index": idx,
        "total": len(languages),
        "next_language": languages[(idx + 1) % len(languages)],
    }


def get_codex_stats(
    log_path: str = DEFAULT_CODEX_LOG_JSON,
) -> Dict[str, Any]:
    """
    从 polyglot_codex_log.json 读取挑战统计。
    """
    log_data = _read_codex_log(log_path)
    attempts = log_data.get("attempts", [])

    # 统计每种语言出现次数
    lang_counts: Dict[str, int] = {}
    for a in attempts:
        lang_counts[a["language"]] = lang_counts.get(a["language"], 0) + 1

    # 统计每种难度出现次数
    diff_counts: Dict[int, int] = {}
    for a in attempts:
        diff_counts[a["difficulty"]] = diff_counts.get(a["difficulty"], 0) + 1

    return {
        "total_katas": log_data.get("total_katas", 0),
        "per_language": lang_counts,
        "per_difficulty": diff_counts,
        "recent_attempts": attempts[-5:],  # 最近 5 次
    }


def format_kata(kata: Dict[str, Any]) -> str:
    """
    将 kata 字典格式化为美观的 ASCII 文本展示。
    """
    lines = [
        f"  ╔══════════════════════════════════════════════════════╗",
        f"  ║  🏆 Polyglot Codex                                 ║",
        f"  ╠══════════════════════════════════════════════════════╣",
        f"  ║  {kata['emoji']}  {kata['language']:<10}  [{kata['difficulty_stars']}]  "
        f"挑战 #{kata['attempt_index']}                             ║",
        f"  ╠══════════════════════════════════════════════════════╣",
        f"  ║  📖 主题：{kata['theme']:<40}║",
        f"  ║  📝 标题：{kata['title']:<40}║",
        f"  ║  📁 文件：.{kata['file_ext']:<8}  |  {kata['paradigm']:<27}║",
        f"  ╠══════════════════════════════════════════════════════╣",
        f"  ║  📋 问题描述                                        ║",
    ]
    # 分行描述（每行最多 52 字符）
    desc = kata["description"]
    for i in range(0, len(desc), 52):
        lines.append(f"  ║    {desc[i:i+52]:<52}║")

    lines += [
        f"  ╠══════════════════════════════════════════════════════╣",
        f"  ║  💻 代码骨架                                        ║",
    ]
    for skel_line in kata["skeleton"].split("\n"):
        wrapped = [skel_line[j:j+52] for j in range(0, len(skel_line), 52)]
        for w in wrapped:
            lines.append(f"  ║    {w:<52}║")

    lines += [
        f"  ╠══════════════════════════════════════════════════════╣",
        f"  ║  ✅ 验收测试                                        ║",
    ]
    for test_line in kata["test_snippet"].split("\n"):
        wrapped = [test_line[j:j+52] for j in range(0, len(test_line), 52)]
        for w in wrapped:
            lines.append(f"  ║    {w:<52}║")

    lines += [
        f"  ╠══════════════════════════════════════════════════════╣",
        f"  ║  ⏭️  下一个语言：{kata['next_language']:<39}║",
        f"  ╚══════════════════════════════════════════════════════╝",
    ]
    return "\n".join(lines)


# ─────────────────────────────────────────────
# CLI 入口
# ─────────────────────────────────────────────

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Polyglot Codex — 编程语言韬略宝鉴")
    sub = parser.add_subparsers(dest="cmd")

    sub.add_parser("kata", help="生成当前语言的代码挑战（kata）")
    sub.add_parser("current", help="查看当前轮换语言")
    sub.add_parser("stats", help="查看挑战统计")
    sub.add_parser("badge", help="格式化输出当前语言的kata徽章")

    args = parser.parse_args()

    if args.cmd == "kata":
        result = generate_kata()
        print(format_kata(result))
    elif args.cmd == "current":
        st = get_current_language()
        print(f"当前语言：{st['emoji']} {st['language']} (索引 {st['index']}/{st['total']-1})")
        print(f"下一个语言：{st['next_language']}")
    elif args.cmd == "stats":
        st = get_codex_stats()
        print(f"总挑战数：{st['total_katas']}")
        print(f"按语言统计：{st['per_language']}")
        print(f"按难度统计：{st['per_difficulty']}")
        if st["recent_attempts"]:
            print("最近 5 次挑战：")
            for a in st["recent_attempts"]:
                print(f"  #{a['attempt']} {a['language']} | {a['theme']} | {a['title']}")
    elif args.cmd == "badge":
        current = get_current_language()
        ecosystem = LANGUAGE_ECOSYSTEM.get(current["language"], {})
        print(f"{ecosystem.get('emoji', '📦')} **{current['language']}**")
        print(f" paradigm: {current['paradigm']}")
        print(f" file_ext: .{current['file_ext']}")
    else:
        parser.print_help()
# Alias for compatibility with __init__.py exports
rotate_and_get_codex = generate_kata
get_codex_preview = get_current_language

def format_codex_markdown(kata):
    """Compatibility alias - format as markdown from kata dict."""
    return format_kata(kata)

def format_codex_console(kata):
    """Compatibility alias - format as console from kata dict."""
    return format_kata(kata)

"""
polyglot_paradigm_weaver.py — 编程范式织锦 (Polyglot Paradigm Weaver)
======================================================================
每次轮换语言时，生成一份"跨语言范式对照报告"——
用一个核心编程范式概念，穿透所有 8 种语言，
展示每种语言如何以自己的方式实现/表达该概念。

与 language_rotation.json 深度集成：
  1. 读取 current_index，取出当前轮换语言
  2. 从预设的范式列表中按轮换顺序选择本次主题
  3. 为所有 8 种语言各生成一个代码示例
  4. 将 current_index 前移一位，更新 updated_at
  5. 返回完整报告

语言轮换顺序（8 种核心语言）：
  Rust → Go → Swift → Kotlin → TypeScript → JavaScript → Java → C/C++ → Rust（循环）

核心范式主题（每个主题 8 个语言实现）：
  1. 并发安全（Concurrency Safety）
  2. 错误处理（Error Handling）
  3. 泛型与多态（Generics & Polymorphism）
  4. 内存管理（Memory Management）
  5. 函数式转换（Functional Transformations）
  6. 异步编程（Asynchronous Programming）
  7. 接口与协议（Interfaces & Protocols）
  8. 数据抽象（Data Abstraction）

作者：AllToolkit 全自动生成
依赖：仅 Python 标准库（json, datetime, pathlib）
======================================================================
"""

import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

# ─────────────────────────────────────────────
# 路径配置
# ─────────────────────────────────────────────
_MODULE_DIR = Path(__file__).parent.parent           # alltoolkit-python/
_WORKSPACE_ROOT = _MODULE_DIR.parent                  # workspace/
DEFAULT_LANGUAGE_ROTATION_JSON = str(_WORKSPACE_ROOT / "language_rotation.json")

# 固定的 8 种核心语言轮换顺序
CORE_LANGUAGES: List[str] = [
    "Rust", "Go", "Swift", "Kotlin",
    "TypeScript", "JavaScript", "Java", "C/C++",
]

LANGUAGE_EMOJI: Dict[str, str] = {
    "Rust": "🦀", "Go": "🐹", "Swift": "🦅", "Kotlin": "🟣",
    "TypeScript": "🔷", "JavaScript": "🟡", "Java": "☕", "C/C++": "🔩",
}

LANGUAGE_EXT: Dict[str, str] = {
    "Rust": "rs", "Go": "go", "Swift": "swift", "Kotlin": "kt",
    "TypeScript": "ts", "JavaScript": "js", "Java": "java", "C/C++": "cpp",
}


# ─────────────────────────────────────────────
# 范式数据库：每种语言对同一范式的实现
# ─────────────────────────────────────────────
# 每个范式主题包含 title、description、concepts（每个语言的代码示例）
PARADIGM_DATABASE: Dict[str, Dict[str, Any]] = {

    "concurrency_safety": {
        "title": "并发安全",
        "title_en": "Concurrency Safety",
        "description": (
            "在多线程/并发环境中，如何安全地共享和修改数据。"
            "本示例展示：启动 N 个并发任务，共享一个计数器，"
            "最终验证计数结果正确（无数据竞争）。"
        ),
        "concepts": {
            "Rust": {
                "code": (
                    "use std::sync::Arc;\n"
                    "use std::sync::atomic::{AtomicUsize, Ordering};\n"
                    "use std::thread;\n\n"
                    "fn main() {{\n"
                    "    let counter = Arc::new(AtomicUsize::new(0));\n"
                    "    let mut handles = vec![];\n\n"
                    "    for _ in 0..10 {{\n"
                    "        let counter = Arc::clone(&counter);\n"
                    "        let handle = thread::spawn(move || {{\n"
                    "            counter.fetch_add(1, Ordering::SeqCst);\n"
                    "        }});\n"
                    "        handles.push(handle);\n"
                    "    }}\n\n"
                    "    for h in handles {{\n"
                    "        h.join().unwrap();\n"
                    "    }}\n\n"
                    "    println!(\"Result: {{}}\", counter.load(Ordering::SeqCst));\n"
                    "    // 期望输出：Result: 10\n"
                    "}}"
                ),
                "explanation": "使用 Arc<AtomicUsize> 实现无锁原子操作，fetch_add 保证原子性。",
            },
            "Go": {
                "code": (
                    "package main\n\n"
                    "import (\n"
                    "    \"fmt\"\n"
                    "    \"sync/atomic\"\n"
                    ")\n\n"
                    "func main() {{\n"
                    "    var counter int64\n"
                    "    var wg sync.WaitGroup\n\n"
                    "    for i := 0; i < 10; i++ {{\n"
                    "        wg.Add(1)\n"
                    "        go func() {{\n"
                    "            atomic.AddInt64(&counter, 1)\n"
                    "            wg.Done()\n"
                    "        }}()\n"
                    "    }}\n\n"
                    "    wg.Wait()\n"
                    "    fmt.Printf(\"Result: %d\\n\", counter)\n"
                    "    // 期望输出：Result: 10\n"
                    "}}"
                ),
                "explanation": "使用 sync/atomic 的原子操作，无需锁即可并发修改共享变量。",
            },
            "Swift": {
                "code": (
                    "import Foundation\n\n"
                    "class SafeCounter {{\n"
                    "    private let lock = NSLock()\n"
                    "    private var _count = 0\n\n"
                    "    var count: Int {{\n"
                    "        lock.lock()\n"
                    "        defer {{ lock.unlock() }}\n"
                    "        return _count\n"
                    "    }}\n\n"
                    "    func increment() {{\n"
                    "        lock.lock()\n"
                    "        _count += 1\n"
                    "        lock.unlock()\n"
                    "    }}\n"
                    "}}\n\n"
                    "let counter = SafeCounter()\n"
                    "let queue = DispatchQueue.concurrentBodyPool(maxConcurrent: 10)\n\n"
                    "for _ in 0..<10 {{\n"
                    "    queue.async {{\n"
                    "        counter.increment()\n"
                    "    }}\n"
                    "}}\n\n"
                    "queue.sync {{ }}\n"
                    "print(\"Result: \\(counter.count)\")\n"
                    "// 期望输出：Result: 10"
                ),
                "explanation": "使用 NSLock 保护临界区，DispatchQueue 并发执行任务。",
            },
            "Kotlin": {
                "code": (
                    "import kotlinx.coroutines.*\n\n"
                    "fun main() = runBlocking {{\n"
                    "    var counter = 0\n"
                    "    val lock = java.util.concurrent.locks.ReentrantLock()\n\n"
                    "    List(10) {{\n"
                    "        launch {\n"
                    "            lock.withLock {{\n"
                    "                counter++\n"
                    "            }}\n"
                    "        }}\n"
                    "    }}.joinAll()\n\n"
                    "    println(\"Result: $counter\")\n"
                    "    // 期望输出：Result: 10\n"
                    "}}"
                ),
                "explanation": "使用 ReentrantLock 保护共享变量，Kotlin 协程并发执行。",
            },
            "TypeScript": {
                "code": (
                    "// TypeScript 单线程模型：本示例展示 Worker 线程通信\n"
                    "// 主线程模拟并发安全\n\n"
                    "const counter = {{ value: 0 }};\n"
                    "const mutex = new Promise(async (resolve) => {{\n"
                    "    // 简化的互斥锁模拟\n"
                    "    resolve();\n"
                    "}});\n\n"
                    "async function increment() {{\n"
                    "    await mutex;\n"
                    "    // 实际场景需要 Atomics 或 SharedArrayBuffer\n"
                    "    // 此处演示概念，实际请用 Worker\n"
                    "    counter.value++;\n"
                    "}}\n\n"
                    "// 注意：TS 单线程环境，真正的并发需 Web Worker\n"
                    "console.log(\"TypeScript uses single-threaded event loop\");\n"
                    "console.log(\"Concurrency via async/await and Worker threads\");"
                ),
                "explanation": "TypeScript 运行在 JS 引擎（V8），单线程 + 事件循环，真正的并发依赖 Worker 或 Atomics。",
            },
            "JavaScript": {
                "code": (
                    "// JavaScript 单线程模型：使用 Atomics 进行并发计数\n"
                    "// 注意：需要 SharedArrayBuffer（在安全上下文中启用）\n\n"
                    "// 本示例演示 Promise 并发模拟\n"
                    "let counter = 0;\n"
                    "const N = 10;\n\n"
                    "async function increment() {{\n"
                    "    // 模拟原子操作\n"
                    "    await Promise.resolve();\n"
                    "    counter++;\n"
                    "}}\n\n"
                    "Promise.all(Array.from({{ length: N }}, () => increment()))\n"
                    "    .then(() => console.log(`Result: ${{counter}}`));\n"
                    "// 期望输出：Result: 10（Promise.all 等待全部完成）"
                ),
                "explanation": "JS 单线程环境，并发依靠 Promise/async/await + Worker。原子操作需 Atomics API。",
            },
            "Java": {
                "code": (
                    "import java.util.concurrent.CountDownLatch;\n"
                    "import java.util.concurrent.atomic.AtomicInteger;\n\n"
                    "public class SafeCounter {{\n"
                    "    public static void main(String[] args) throws InterruptedException {{\n"
                    "        AtomicInteger counter = new AtomicInteger(0);\n"
                    "        CountDownLatch latch = new CountDownLatch(10);\n\n"
                    "        for (int i = 0; i < 10; i++) {{\n"
                    "            new Thread(() -> {{\n"
                    "                counter.incrementAndGet();\n"
                    "                latch.countDown();\n"
                    "            }}).start();\n"
                    "        }}\n\n"
                    "        latch.await();\n"
                    "        System.out.println(\"Result: \" + counter.get());\n"
                    "        // 期望输出：Result: 10\n"
                    "    }}\n"
                    "}}"
                ),
                "explanation": "使用 AtomicInteger.incrementAndGet() 实现无锁原子操作，CountDownLatch 等待所有线程。",
            },
            "C/C++": {
                "code": (
                    "#include <stdio.h>\n"
                    "#include <pthread.h>\n"
                    "#include <stdatomic.h>\n\n"
                    "_Atomic int counter = 0;\n\n"
                    "void* increment(void* arg) {{\n"
                    "    atomic_fetch_add_explicit(&counter, 1, memory_order_seq_cst);\n"
                    "    return NULL;\n"
                    "}}\n\n"
                    "int main() {{\n"
                    "    pthread_t threads[10];\n"
                    "    for (int i = 0; i < 10; i++) {{\n"
                    "        pthread_create(&threads[i], NULL, increment, NULL);\n"
                    "    }}\n"
                    "    for (int i = 0; i < 10; i++) {{\n"
                    "        pthread_join(threads[i], NULL);\n"
                    "    }}\n"
                    "    printf(\"Result: %d\\n\", atomic_load(&counter));\n"
                    "    // 期望输出：Result: 10\n"
                    "    return 0;\n"
                    "}}"
                ),
                "explanation": "使用 C11 _Atomic 指定符和 atomic_fetch_add_explicit 实现无锁原子操作。",
            },
        },
    },

    "error_handling": {
        "title": "错误处理",
        "title_en": "Error Handling",
        "description": (
            "如何表示、处理和传播错误。"
            "本示例展示：实现一个除法函数，处理除以零错误，"
            "用每种语言的惯用方式返回/传播错误。"
        ),
        "concepts": {
            "Rust": {
                "code": (
                    "fn divide(a: f64, b: f64) -> Result<f64, &'static str> {{\n"
                    "    if b == 0.0 {{\n"
                    "        return Err(\"division by zero\");\n"
                    "    }}\n"
                    "    Ok(a / b)\n"
                    "}}\n\n"
                    "fn main() {{\n"
                    "    match divide(10.0, 0.0) {{\n"
                    "        Ok(v)  => println!(\"Result: {{}}\", v),\n"
                    "        Err(e) => println!(\"Error: {{}}\", e),\n"
                    "    }}\n"
                    "    // 使用 ? 操作符传播\n"
                    "    let result: Result<f64, _> = divide(10.0, 2.0);\n"
                    "    println!(\"Ok: {{:?}}\", result);\n"
                    "}}"
                ),
                "explanation": "Result<T, E> + ? 操作符，编译期强制处理错误，无异常机制。",
            },
            "Go": {
                "code": (
                    "package main\n\n"
                    "import (\n"
                    "    \"errors\"\n"
                    "    \"fmt\"\n"
                    ")\n\n"
                    "func divide(a, b float64) (float64, error) {{\n"
                    "    if b == 0.0 {{\n"
                    "        return 0, errors.New(\"division by zero\")\n"
                    "    }}\n"
                    "    return a / b, nil\n"
                    "}}\n\n"
                    "func main() {{\n"
                    "    result, err := divide(10.0, 0.0)\n"
                    "    if err != nil {{\n"
                    "        fmt.Println(\"Error:\", err)\n"
                    "        return\n"
                    "    }}\n"
                    "    fmt.Printf(\"Result: %f\\n\", result)\n"
                    "}}"
                ),
                "explanation": "多返回值 + error 接口，显式错误检查，无异常机制（error as value）。",
            },
            "Swift": {
                "code": (
                    "enum MathError: Error {{\n"
                    "    case divisionByZero\n"
                    "}}\n\n"
                    "func divide(_ a: Double, _ b: Double) throws -> Double {{\n"
                    "    guard b != 0 else {{ throw MathError.divisionByZero }}\n"
                    "    return a / b\n"
                    "}}\n\n"
                    "do {{\n"
                    "    let result = try divide(10.0, 0.0)\n"
                    "    print(\"Result: \\(result)\")\n"
                    "}} catch MathError.divisionByZero {{\n"
                    "    print(\"Error: division by zero\")\n"
                    "}} catch {{\n"
                    "    print(\"Error: \\(error)\")\n"
                    "}}"
                ),
                "explanation": "throws + do/try/catch，Swift Error 协议，编译期提示必须处理错误。",
            },
            "Kotlin": {
                "code": (
                    "fun divide(a: Double, b: Double): Result<Double> {{\n"
                    "    return if (b == 0.0) {{\n"
                    "        Result.failure(ArithmeticException(\"division by zero\"))\n"
                    "    }} else {{\n"
                    "        Result.success(a / b)\n"
                    "    }}\n"
                    "}}\n\n"
                    "fun main() {{\n"
                    "    val result = divide(10.0, 0.0)\n"
                    "    result.fold(\n"
                    "        onSuccess = {{ println(\"Result: $it\") }},\n"
                    "        onFailure = {{ println(\"Error: ${it.message}\") }}\n"
                    "    )\n"
                    "    // Kotlin 也有 throw 方式：throw IllegalArgumentException(...)\n"
                    "}}"
                ),
                "explanation": "Result<T> 类（Kotlin 1.3+），或使用 @Throws 注解的异常方式。Result.fold() 提供函数式处理。",
            },
            "TypeScript": {
                "code": (
                    "type Result<T, E = string> = \n"
                    "    | {{ ok: true; value: T }}\n"
                    "    | {{ ok: false; error: E }};\n\n"
                    "function divide(a: number, b: number): Result<number> {{\n"
                    "    if (b === 0) {{\n"
                    "        return {{ ok: false, error: 'division by zero' }};\n"
                    "    }}\n"
                    "    return {{ ok: true, value: a / b }};\n"
                    "}}\n\n"
                    "const result = divide(10, 0);\n"
                    "if (!result.ok) {{\n"
                    "    console.log('Error:', result.error);\n"
                    "}} else {{\n"
                    "    console.log('Result:', result.value);\n"
                    "}}"
                ),
                "explanation": "TS 没有内置 Result 类型，用联合类型手动模拟（类似 Rust Result）。也可使用 throw。",
            },
            "JavaScript": {
                "code": (
                    "function divide(a, b) {{\n"
                    "    if (b === 0) {{\n"
                    "        throw new Error('division by zero');\n"
                    "    }}\n"
                    "    return a / b;\n"
                    "}}\n\n"
                    "try {{\n"
                    "    const result = divide(10, 0);\n"
                    "    console.log('Result:', result);\n"
                    "}} catch (e) {{\n"
                    "    console.log('Error:', e.message);\n"
                    "}} finally {{\n"
                    "    console.log('Done');\n"
                    "}}"
                ),
                "explanation": "try/catch/throw 异常机制，JS 传统方式。没有编译期检查，运行期捕获。",
            },
            "Java": {
                "code": (
                    "import java.util.Optional;\n\n"
                    "public class MathUtil {{\n"
                    "    public static Optional<Double> divide(double a, double b) {{\n"
                    "        if (b == 0.0) {{\n"
                    "            return Optional.empty();\n"
                    "        }}\n"
                    "        return Optional.of(a / b);\n"
                    "    }}\n\n"
                    "    public static void main(String[] args) {{\n"
                    "        divide(10.0, 0.0)\n"
                    "            .ifPresentOrElse(\n"
                    "                v -> System.out.println(\"Result: \" + v),\n"
                    "                () -> System.out.println(\"Error: division by zero\")\n"
                    "            );\n"
                    "    }}\n"
                    "}}"
                ),
                "explanation": "Java 传统使用异常（try/catch），Java 8+ 可用 Optional<T> 表示可能无值的情况。",
            },
            "C/C++": {
                "code": (
                    "#include <stdio.h>\n"
                    "#include <stdbool.h>\n\n"
                    "// 返回 false 表示错误，result 通过指针输出\n"
                    "bool divide(double a, double b, double* out) {{\n"
                    "    if (b == 0.0) {{\n"
                    "        return false;\n"
                    "    }}\n"
                    "    *out = a / b;\n"
                    "    return true;\n"
                    "}}\n\n"
                    "int main() {{\n"
                    "    double result;\n"
                    "    if (divide(10.0, 0.0, &result)) {{\n"
                    "        printf(\"Result: %f\\n\", result);\n"
                    "    }} else {{\n"
                    "        printf(\"Error: division by zero\\n\");\n"
                    "    }}\n"
                    "    return 0;\n"
                    "}}"
                ),
                "explanation": "C/C++ 无内建 Result 类型，传统方式：返回错误码（bool/int）+ 通过指针输出结果。",
            },
        },
    },

    "generics_polymorphism": {
        "title": "泛型与多态",
        "title_en": "Generics & Polymorphism",
        "description": (
            "如何编写与类型无关的可复用代码。"
            "本示例展示：实现一个通用的 'pair'（两个元素的元组），"
            "包含获取第一个/第二个元素的函数，"
            "每种语言都展示泛型如何实现类型安全的多态。"
        ),
        "concepts": {
            "Rust": {
                "code": (
                    "struct Pair<T, U> {{\n"
                    "    first: T,\n"
                    "    second: U,\n"
                    "}}\n\n"
                    "impl<T, U> Pair<T, U> {{\n"
                    "    fn new(first: T, second: U) -> Self {{\n"
                    "        Self {{ first, second }}\n"
                    "    }}\n"
                    "    fn first(&self) -> &T {{ &self.first }}\n"
                    "    fn second(&self) -> &U {{ &self.second }}\n"
                    "}}\n\n"
                    "fn main() {{\n"
                    "    let p: Pair<i32, &str> = Pair::new(42, \"hello\");\n"
                    "    println!(\"First: {{}}, Second: {{}}\", p.first(), p.second());\n"
                    "    // First: 42, Second: hello\n"
                    "}}"
                ),
                "explanation": "Rust 泛型 struct + impl 方法，编译时单态化（monomorphization），零运行时成本。",
            },
            "Go": {
                "code": (
                    "package main\n\n"
                    "import \"fmt\"\n\n"
                    "// Go 1.18+ 泛型\n"
                    "type Pair[T, U any] struct {{\n"
                    "    First  T\n"
                    "    Second U\n"
                    "}}\n\n"
                    "func (p Pair[T, U]) First() T  {{ return p.First }}\n"
                    "func (p Pair[T, U]) Second() U {{ return p.Second }}\n\n"
                    "func main() {{\n"
                    "    p := Pair[int, string]{{ First: 42, Second: \"hello\" }}\n"
                    "    fmt.Printf(\"First: %d, Second: %s\\n\", p.First(), p.Second())\n"
                    "    // First: 42, Second: hello\n"
                    "}}"
                ),
                "explanation": "Go 1.18+ 泛型，语法 type Pair[T, U any]，使用类型参数实例化。",
            },
            "Swift": {
                "code": (
                    "struct Pair<First, Second> {{\n"
                    "    let first: First\n"
                    "    let second: Second\n"
                    "}}\n\n"
                    "let p = Pair(first: 42, second: \"hello\")\n"
                    "print(\"First: \\(p.first), Second: \\(p.second)\")\n"
                    "// First: 42, Second: hello\n\n"
                    "// Swift 还支持泛型约束\n"
                    "func swap<T, U>(_ pair: Pair<T, U>) -> Pair<U, T> {{\n"
                    "    Pair(first: pair.second, second: pair.first)\n"
                    "}}"
                ),
                "explanation": "Swift 泛型 struct，与 Rust 类似但语法不同，支持 where 子句约束关联类型。",
            },
            "Kotlin": {
                "code": (
                    "data class Pair<out A, out B>(val first: A, val second: B)\n\n"
                    "fun <T, U> makePair(first: T, second: U) = Pair(first, second)\n\n"
                    "fun main() {{\n"
                    "    val p: Pair<Int, String> = Pair(42, \"hello\")\n"
                    "    println(\"First: ${p.first}, Second: ${p.second}\")\n"
                    "    // First: 42, Second: hello\n"
                    "    \n"
                    "    // 解构\n"
                    "    val (a, b) = p\n"
                    "    println(\"Destructured: $a, $b\")\n"
                    "}}"
                ),
                "explanation": "Kotlin 自带 Pair 类（A, B 两个泛型参数），data class 自动提供 toString/copy/解构。",
            },
            "TypeScript": {
                "code": (
                    "interface Pair<A, B> {{\n"
                    "    first: A;\n"
                    "    second: B;\n"
                    "}}\n\n"
                    "function makePair<A, B>(first: A, second: B): Pair<A, B> {{\n"
                    "    return {{ first, second }};\n"
                    "}}\n\n"
                    "const p: Pair<number, string> = makePair(42, \"hello\");\n"
                    "console.log(`First: ${p.first}, Second: ${p.second}`);\n"
                    "// First: 42, Second: hello\n\n"
                    "// TypeScript 还支持 keyof、infer 等高级泛型特性\n"
                    "type ValueOf<T> = T[keyof T];"
                ),
                "explanation": "TypeScript 泛型接口 + 函数泛型，编译时类型擦除（ erasure），运行时无泛型信息。",
            },
            "JavaScript": {
                "code": (
                    "// JS 无泛型，使用普通对象模拟\n"
                    "function makePair(first, second) {{\n"
                    "    return {{ first, second }};\n"
                    "}}\n\n"
                    "const p = makePair(42, \"hello\");\n"
                    "console.log(`First: ${p.first}, Second: ${p.second}`);\n"
                    "// First: 42, Second: hello\n\n"
                    "// 使用 JSDoc 注释提供类型提示（TypeScript 项目中自动推导）\n"
                    "/**\n"
                    " * @template T, U\n"
                    " * @param {T} first\n"
                    " * @param {U} second\n"
                    " * @returns {{ first: T, second: U }}\n"
                    " */"
                ),
                "explanation": "JavaScript 本身无泛型，使用 JSDoc 注释配合 TypeScript 提供类型安全。运行时就是普通对象。",
            },
            "Java": {
                "code": (
                    "public class Pair<A, B> {{\n"
                    "    private final A first;\n"
                    "    private final B second;\n\n"
                    "    public Pair(A first, B second) {{\n"
                    "        this.first = first;\n"
                    "        this.second = second;\n"
                    "    }}\n\n"
                    "    public A getFirst()  {{ return first; }}\n"
                    "    public B getSecond() {{ return second; }}\n"
                    "}}\n\n"
                    "public class Main {{\n"
                    "    public static void main(String[] args) {{\n"
                    "        Pair<Integer, String> p = new Pair<>(42, \"hello\");\n"
                    "        System.out.println(\"First: \" + p.getFirst() + \", Second: \" + p.getSecond());\n"
                    "        // First: 42, Second: hello\n"
                    "    }}\n"
                    "}}"
                ),
                "explanation": "Java 泛型类，编译时类型擦除（Type Erasure），运行时不保留泛型信息（Pair<A,B> → Pair<Object>）。",
            },
            "C/C++": {
                "code": (
                    "#include <stdio.h>\n\n"
                    "// C++ 模板\n"
                    "template<typename T, typename U>\n"
                    "struct Pair {{\n"
                    "    T first;\n"
                    "    U second;\n"
                    "}};\n\n"
                    "template<typename T, typename U>\n"
                    "U second(const Pair<T, U>& p) {{\n"
                    "    return p.second;\n"
                    "}}\n\n"
                    "int main() {{\n"
                    "    Pair<int, const char*> p {{ 42, \"hello\" }};\n"
                    "    printf(\"First: %d, Second: %s\\n\", p.first, p.second);\n"
                    "    // First: 42, Second: hello\n"
                    "    return 0;\n"
                    "}}"
                ),
                "explanation": "C++ 模板（template），编译时实例化（monomorphization），每个模板实例是独立的代码。",
            },
        },
    },

    "memory_management": {
        "title": "内存管理",
        "title_en": "Memory Management",
        "description": (
            "如何管理程序的内存生命周期。"
            "本示例展示：创建一个在堆上分配的对象，"
            "传递引用（或所有权），然后释放。"
            "每种语言展示了其独特的内存管理哲学。"
        ),
        "concepts": {
            "Rust": {
                "code": (
                    "struct Resource {{\n"
                    "    id: u32,\n"
                    "}}\n\n"
                    "impl Drop for Resource {{\n"
                    "    fn drop(&mut self) {{\n"
                    "        println!(\"Dropping Resource {{}}\", self.id);\n"
                    "    }}\n"
                    "}}\n\n"
                    "fn main() {{\n"
                    "    let r = Resource {{ id: 1 }};\n"
                    "    let r2 = r; // 所有权转移，r 不再有效\n"
                    "    // println!(\"{{}}\", r); // 编译错误！\n"
                    "    println!(\"Resource id: {{}}\", r2.id);\n"
                    "    // r2 离开作用域时，自动调用 Drop\n"
                    "}}"
                ),
                "explanation": "Rust 的所有权系统（ownership）+ _drop_ + borrow checker，编译期确保无泄漏/无悬垂指针。",
            },
            "Go": {
                "code": (
                    "package main\n\n"
                    "import \"fmt\"\n\n"
                    "type Resource struct {{\n"
                    "    ID int\n"
                    "}}\n\n"
                    "func main() {{\n"
                    "    r := &Resource{{ ID: 1 }}\n"
                    "    r2 := r // 复制指针，共享底层数据\n"
                    "    fmt.Printf(\"Resource: %+v\\n\", r2)\n"
                    "    // Go 有 GC，无需手动释放\n"
                    "    // 离开函数时，所有引用消失后 GC 回收\n"
                    "}}"
                ),
                "explanation": "Go 使用垃圾回收器（GC）自动管理内存，值语义 vs 指针语义由程序员控制。",
            },
            "Swift": {
                "code": (
                    "class Resource {{\n"
                    "    let id: Int\n"
                    "    init(id: Int) {{ self.id = id }}\n"
                    "    deinit {{\n"
                    "        print(\"Releasing Resource \\(id)\")\n"
                    "    }}\n"
                    "}}\n\n"
                    "var r: Resource? = Resource(id: 1)\n"
                    "var r2 = r // 引用计数 +1\n"
                    "r = nil    // 引用数减 1，但 r2 仍持有\n"
                    "r2 = nil   // 引用数归 0，deinit 被调用，内存释放\n"
                    "// ARC 自动管理引用计数"
                ),
                "explanation": "Swift 使用 ARC（Automatic Reference Counting），编译期插入 retain/release，循环引用需 weak/unowned 打破。",
            },
            "Kotlin": {
                "code": (
                    "class Resource(val id: Int) {{\n"
                    "    protected fun finalize() {{\n"
                    "        println(\"Releasing Resource $id\")\n"
                    "    }}\n"
                    "}}\n\n"
                    "fun main() {{\n"
                    "    var r: Resource? = Resource(1)\n"
                    "    var r2 = r    // 共享引用\n"
                    "    r = null      // 仍可达（r2 持有）\n"
                    "    r2 = null     // 无引用，GC 可回收（finalize 被调用）\n"
                    "    // Kotlin 主要依赖 JVM GC，无需手动管理\n"
                    "}}"
                ),
                "explanation": "Kotlin 运行在 JVM 上，依赖 GC 自动回收内存。AnyRef.finalize()（Kotlin 1.0）是早期方式，官方建议避免依赖。",
            },
            "TypeScript": {
                "code": (
                    "// TypeScript/JavaScript 使用 GC 自动管理内存\n"
                    "class Resource {{\n"
                    "    constructor(public id: number) {{ }}\n"
                    "    [Symbol.dispose]?.() {{\n"
                    "        console.log(`Releasing Resource ${this.id}`);\n"
                    "    }}\n"
                    "}}\n\n"
                    "// 使用 Resource Allocation (TC39 Stage 3)\n"
                    "const r = new Resource(1);\n"
                    "const r2 = r;\n"
                    "// r 和 r2 离开作用域后，GC 回收\n"
                    "// 或使用显式 dispose（如果 Symbol.dispose 被调用）\n"
                    "console.log(`Resource: ${r2.id}`);"
                ),
                "explanation": "TS/JS 使用 GC 自动管理内存。TC39 Disposable Resources (Symbol.dispose) 提供显式资源释放语法。",
            },
            "JavaScript": {
                "code": (
                    "// JavaScript 使用 GC 自动管理内存\n"
                    "function createResource(id) {{\n"
                    "    return {{\n"
                    "        id,\n"
                    "        [Symbol.dispose]() {{\n"
                    "            console.log(`Releasing Resource ${{id}}`);\n"
                    "        }}\n"
                    "    }};\n"
                    "}}\n\n"
                    "const r = createResource(1);\n"
                    "const r2 = r;\n"
                    "// GC 负责回收（不再可达时）\n"
                    "// 或使用显式 dispose（需 using 或手动调用）\n"
                    "console.log(`Resource: ${{r2.id}}`);"
                ),
                "explanation": "JS 使用 GC 自动管理内存。TC39 Disposable Resources (Symbol.dispose) 提供 using 语句或显式释放。",
            },
            "Java": {
                "code": (
                    "public class Resource {{\n"
                    "    private int id;\n"
                    "    public Resource(int id) {{ this.id = id; }}\n"
                    "    @Override\n"
                    "    protected void finalize() throws Throwable {{\n"
                    "        System.out.println(\"Releasing Resource \" + id);\n"
                    "    }}\n\n"
                    "    public static void main(String[] args) {{\n"
                    "        Resource r = new Resource(1);\n"
                    "        Resource r2 = r; // 引用复制\n"
                    "        r = null;        // 仍可达（r2 持有）\n"
                    "        r2 = null;       // 无引用，GC 回收\n"
                    "        // JVM GC 自动管理\n"
                    "    }}\n"
                    "}}"
                ),
                "explanation": "Java 依赖 JVM GC 自动回收内存。finalize() 已被废弃（deprecated），try-with-resources 是推荐的资源管理模式。",
            },
            "C/C++": {
                "code": (
                    "#include <stdio.h>\n"
                    "#include <stdlib.h>\n\n"
                    "typedef struct {{\n"
                    "    int id;\n"
                    "}} Resource;\n\n"
                    "void resource_free(Resource* r) {{\n"
                    "    if (r) {{\n"
                    "        printf(\"Releasing Resource %d\\n\", r->id);\n"
                    "        free(r);\n"
                    "    }}\n"
                    "}}\n\n"
                    "int main() {{\n"
                    "    Resource* r = (Resource*)malloc(sizeof(Resource));\n"
                    "    r->id = 1;\n"
                    "    Resource* r2 = r; // 复制指针\n"
                    "    printf(\"Resource id: %d\\n\", r2->id);\n"
                    "    // 手动释放（两次 free 会 UB！）\n"
                    "    r = NULL;\n"
                    "    resource_free(r2); // 只释放一次\n"
                    "    return 0;\n"
                    "}}"
                ),
                "explanation": "C/C++ 手动管理内存（malloc/free 或 new/delete），RAII 惯用模式利用构造/析构函数自动释放资源。",
            },
        },
    },

    "functional_transforms": {
        "title": "函数式转换",
        "title_en": "Functional Transformations",
        "description": (
            "如何用函数式风格转换数据。"
            "本示例展示：对一个数字列表进行链式转换——"
            "过滤（保留偶数）→ 映射（翻倍）→ 归约（求和），"
            "每种语言的函数式 API 各有特色。"
        ),
        "concepts": {
            "Rust": {
                "code": (
                    "fn main() {{\n"
                    "    let numbers = vec![1, 2, 3, 4, 5, 6, 7, 8, 9, 10];\n\n"
                    "    let result: i32 = numbers\n"
                    "        .iter()\n"
                    "        .filter(|&&x| x % 2 == 0)  // 过滤偶数\n"
                    "        .map(|&&x| x * 2)           // 翻倍\n"
                    "        .sum();                    // 求和\n\n"
                    "    println!(\"Result: {{}}\", result);\n"
                    "    // 期望：60  (2+4+6+8+10 = 30 → ×2 = 60)\n"
                    "}}"
                ),
                "explanation": "Rust 的 Iterator API：filter、map、sum 等惰性迭代器，零成本抽象，编译期内联。",
            },
            "Go": {
                "code": (
                    "package main\n\n"
                    "import \"fmt\"\n\n"
                    "func main() {{\n"
                    "    numbers := []int{{1, 2, 3, 4, 5, 6, 7, 8, 9, 10}}\n\n"
                    "    // Go 1.21+ 引入 slices.Concat / slices.DeleteFunc\n"
                    "    // 但标准库没有 map/filter/reduce，需手动循环或用第三方库\n"
                    "    var sum int\n"
                    "    for _, x := range numbers {{\n"
                    "        if x%2 == 0 {{\n"
                    "            sum += x * 2\n"
                    "        }}\n"
                    "    }}\n"
                    "    fmt.Printf(\"Result: %d\\n\", sum)\n"
                    "    // 期望：60\n"
                    "}}"
                ),
                "explanation": "Go 标准库没有内置 map/filter/reduce（1.21+ slices 包提供了部分函数）。社区惯用 'golang.org/x/exp/slices' 或手写循环。",
            },
            "Swift": {
                "code": (
                    "let numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]\n\n"
                    "let result = numbers\n"
                    "    .filter {{ $0 % 2 == 0 }}  // 过滤偶数\n"
                    "    .map    {{ $0 * 2 }}       // 翻倍\n"
                    "    .reduce(0, +)              // 求和\n\n"
                    "print(\"Result: \\(result)\")\n"
                    "// 期望：60"
                ),
                "explanation": "Swift Array 的函数式 API：filter、map、reduce，链式调用，$0 是隐式闭包参数。",
            },
            "Kotlin": {
                "code": (
                    "fun main() {{\n"
                    "    val numbers = listOf(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)\n\n"
                    "    val result = numbers\n"
                    "        .filter {{ it % 2 == 0 }}  // 过滤偶数\n"
                    "        .map    {{ it * 2 }}        // 翻倍\n"
                    "        .sum()                     // 求和\n\n"
                    "    println(\"Result: $result\")\n"
                    "    // 期望：60\n"
                    "}}"
                ),
                "explanation": "Kotlin Collections API：filter、map、sum，链式调用，it 是隐式 lambda 参数。与 Java Stream API 类似但更简洁。",
            },
            "TypeScript": {
                "code": (
                    "const numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];\n\n"
                    "const result = numbers\n"
                    "    .filter(x => x % 2 === 0)  // 过滤偶数\n"
                    "    .map(x => x * 2)            // 翻倍\n"
                    "    .reduce((acc, x) => acc + x, 0); // 求和\n\n"
                    "console.log(`Result: ${result}`);\n"
                    "// 期望：60"
                ),
                "explanation": "TypeScript Array.prototype：filter、map、reduce 原生支持，链式调用，返回新数组（不修改原数组）。",
            },
            "JavaScript": {
                "code": (
                    "const numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];\n\n"
                    "const result = numbers\n"
                    "    .filter(x => x % 2 === 0)           // 过滤偶数\n"
                    "    .map(x => x * 2)                     // 翻倍\n"
                    "    .reduce((acc, x) => acc + x, 0);     // 求和\n\n"
                    "console.log(`Result: ${result}`);\n"
                    "// 期望：60"
                ),
                "explanation": "JavaScript ES5+ Array.prototype：filter、map、reduce，链式调用，不修改原数组。",
            },
            "Java": {
                "code": (
                    "import java.util.*;\n\n"
                    "public class Main {{\n"
                    "    public static void main(String[] args) {{\n"
                    "        List<Integer> numbers = List.of(1, 2, 3, 4, 5, 6, 7, 8, 9, 10);\n\n"
                    "        int result = numbers.stream()\n"
                    "            .filter(x -> x % 2 == 0)   // 过滤偶数\n"
                    "            .mapToInt(x -> x * 2)       // 翻倍\n"
                    "            .sum();                     // 求和\n\n"
                    "        System.out.println(\"Result: \" + result);\n"
                    "        // 期望：60\n"
                    "    }}\n"
                    "}}"
                ),
                "explanation": "Java Stream API：filter、mapToInt、sum，惰性求值（lazy evaluation），parallelStream() 可并行化。",
            },
            "C/C++": {
                "code": (
                    "#include <stdio.h>\n"
                    "#include <stdlib.h>\n\n"
                    "int is_even(int x) {{ return x % 2 == 0; }}\n"
                    "int double_it(int x) {{ return x * 2; }}\n\n"
                    "int main() {{\n"
                    "    int nums[] = {{1, 2, 3, 4, 5, 6, 7, 8, 9, 10}};\n"
                    "    int n = 10;\n"
                    "    int sum = 0;\n"
                    "    for (int i = 0; i < n; i++) {{\n"
                    "        if (is_even(nums[i])) {{\n"
                    "            sum += double_it(nums[i]);\n"
                    "        }}\n"
                    "    }}\n"
                    "    printf(\"Result: %d\\n\", sum);\n"
                    "    // 期望：60\n"
                    "    return 0;\n"
                    "}}"
                ),
                "explanation": "C/C++ 无内置 filter/map/reduce，手写循环实现。STL 有 std::accumulate、std::copy_if、std::transform 可组合使用。",
            },
        },
    },

    "async_programming": {
        "title": "异步编程",
        "title_en": "Asynchronous Programming",
        "description": (
            "如何处理非阻塞 I/O 和并发任务。"
            "本示例展示：发起两个异步任务（各自延时后返回），"
            "等待全部完成，收集结果。"
        ),
        "concepts": {
            "Rust": {
                "code": (
                    "use tokio::task;\n\n"
                    "#[tokio::main]\n"
                    "async fn main() {{\n"
                    "    let r1 = task::spawn(async {{\n"
                    "        tokio::time::sleep(tokio::time::Duration::from_millis(100)).await;\n"
                    "        1\n"
                    "    }});\n"
                    "    let r2 = task::spawn(async {{\n"
                    "        tokio::time::sleep(tokio::time::Duration::from_millis(50)).await;\n"
                    "        2\n"
                    "    }});\n\n"
                    "    let (a, b) = tokio::join!(r1, r2);\n"
                    "    println!(\"Results: {{}} {{}}\", a.unwrap(), b.unwrap());\n"
                    "    // 两个任务并发执行，总耗时约 100ms（最长那个）\n"
                    "}}"
                ),
                "explanation": "Rust 的 tokio 异步运行时，async/await + tokio::spawn + tokio::join!，绿色线程模型。",
            },
            "Go": {
                "code": (
                    "package main\n\n"
                    "import (\n"
                    "    \"context\"\n"
                    "    \"fmt\"\n"
                    "    \"time\"\n"
                    ")\n\n"
                    "func main() {{\n"
                    "    ctx, cancel := context.WithCancel(context.Background())\n"
                    "    defer cancel()\n\n"
                    "    resultCh := make(chan int, 2)\n\n"
                    "    go func() {{\n"
                    "        time.Sleep(100 * time.Millisecond)\n"
                    "        resultCh <- 1\n"
                    "    }}()\n\n"
                    "    go func() {{\n"
                    "        time.Sleep(50 * time.Millisecond)\n"
                    "        resultCh <- 2\n"
                    "    }}()\n\n"
                    "    for i := 0; i < 2; i++ {{\n"
                    "        fmt.Println(<-resultCh)\n"
                    "    }}\n"
                    "}}"
                ),
                "explanation": "Go 使用 goroutine + channel 实现并发，自然的非阻塞模型，无需 async 关键字。",
            },
            "Swift": {
                "code": (
                    "import Foundation\n\n"
                    "Task {{\n"
                    "    async let r1 = try await Task.sleep(nanoseconds: 100_000_000).map {{ 1 }}\n"
                    "    async let r2 = try await Task.sleep(nanoseconds: 50_000_000).map {{ 2 }}\n\n"
                    "    \n"
                    "    let (a, b) = await (try! r1, try! r2)\n"
                    "    print(\"Results: \\(a) \\(b)\")\n"
                    "}}"
                ),
                "explanation": "Swift 5.5+ async/await + Task group，并发任务用 async let 声明，Structured Concurrency 模型。",
            },
            "Kotlin": {
                "code": (
                    "import kotlinx.coroutines.*\n\n"
                    "fun main() = runBlocking {{\n"
                    "    val r1 = async { delay(100); 1 }\n"
                    "    val r2 = async { delay(50); 2 }\n\n"
                    "    val results = awaitAll(r1, r2)\n"
                    "    println(\"Results: ${results}\")\n"
                    "    // 并发执行，总耗时约 100ms\n"
                    "}}"
                ),
                "explanation": "Kotlin Coroutines：async {} + awaitAll，并发任务用 async 启动，launch 用于不需返回值的任务。",
            },
            "TypeScript": {
                "code": (
                    "async function task(ms: number, value: number) {{\n"
                    "    await new Promise(resolve => setTimeout(resolve, ms));\n"
                    "    return value;\n"
                    "}}\n\n"
                    "async function main() {{\n"
                    "    const [a, b] = await Promise.all([\n"
                    "        task(100, 1),\n"
                    "        task(50, 2)\n"
                    "    ]);\n"
                    "    console.log(`Results: ${a} ${b}`);\n"
                    "    // 总耗时约 100ms（最长那个）\n"
                    "}}\n\n"
                    "main();"
                ),
                "explanation": "TypeScript async/await + Promise.all，并发任务用 Promise.all 组合，Node.js 和浏览器均支持。",
            },
            "JavaScript": {
                "code": (
                    "function task(ms, value) {{\n"
                    "    return new Promise(resolve => setTimeout(() => resolve(value), ms));\n"
                    "}}\n\n"
                    "Promise.all([task(100, 1), task(50, 2)])\n"
                    "    .then(([a, b]) => console.log(`Results: ${a} ${b}`));\n"
                    "// 总耗时约 100ms（最长那个）"
                ),
                "explanation": "JavaScript Promise.all + setTimeout，经典的回调转 Promise 模式，现代 JS 异步基础。",
            },
            "Java": {
                "code": (
                    "import java.util.concurrent.*;\n\n"
                    "public class AsyncDemo {{\n"
                    "    public static void main(String[] args) throws Exception {{\n"
                    "        ExecutorService exec = Executors.newFixedThreadPool(2);\n\n"
                    "        Future<Integer> f1 = exec.submit(() -> {{\n"
                    "            Thread.sleep(100);\n"
                    "            return 1;\n"
                    "        }});\n"
                    "        Future<Integer> f2 = exec.submit(() -> {{\n"
                    "            Thread.sleep(50);\n"
                    "            return 2;\n"
                    "        }});\n\n"
                    "        System.out.println(\"Results: \" + f1.get() + \" \" + f2.get());\n"
                    "        exec.shutdown();\n"
                    "    }}\n"
                    "}}"
                ),
                "explanation": "Java ExecutorService + Future，submit Callable/Runnable 获取 Future，get() 阻塞等待结果。Java 21+ Virtual Threads 提供更轻量的并发。",
            },
            "C/C++": {
                "code": (
                    "// C/C++ 标准库没有内置异步，推荐使用 libuv (Node.js底层)\n"
                    "// 或 POSIX threads + condition variables\n\n"
                    "#include <stdio.h>\n"
                    "#include <stdlib.h>\n"
                    "#include <unistd.h>\n\n"
                    "// 模拟：sleep 同步阻塞，不推荐在实际异步 I/O 中使用\n"
                    "int task1() {{\n"
                    "    usleep(100000); // 100ms\n"
                    "    return 1;\n"
                    "}}\n\n"
                    "int main() {{\n"
                    "    // 串行执行（演示用）\n"
                    "    int a = task1();\n"
                    "    int b = 2; // 假设 task2 是即时的\n"
                    "    printf(\"Results: %d %d\\n\", a, b);\n"
                    "    // 实际异步 I/O 推荐 libuv、Boost.Asio 或 ASIO (C++20)\n"
                    "    return 0;\n"
                    "}}"
                ),
                "explanation": "C/C++ 标准库无内置异步 I/O 框架。常用 libuv（Node.js 底层）、Boost.Asio、C++20 std::format/asio。同步模型使用 usleep。",
            },
        },
    },

    "interfaces_protocols": {
        "title": "接口与协议",
        "title_en": "Interfaces & Protocols",
        "description": (
            "如何定义行为契约，实现多态。"
            "本示例展示：定义一个 'Drawable' 接口/协议/特征，"
            "让 Circle 和 Rectangle 两种类型实现它，"
            "然后用统一接口绘制所有图形。"
        ),
        "concepts": {
            "Rust": {
                "code": (
                    "trait Drawable {{\n"
                    "    fn draw(&self);\n"
                    "    fn area(&self) -> f64;\n"
                    "}}\n\n"
                    "struct Circle {{ radius: f64 }}\n"
                    "struct Rectangle {{ width: f64, height: f64 }}\n\n"
                    "impl Drawable for Circle {{\n"
                    "    fn draw(&self) {{ println!(\"Drawing Circle\") }}\n"
                    "    fn area(&self) -> f64 {{ 3.14159 * self.radius * self.radius }}\n"
                    "}}\n\n"
                    "impl Drawable for Rectangle {{\n"
                    "    fn draw(&self) {{ println!(\"Drawing Rectangle\") }}\n"
                    "    fn area(&self) -> f64 {{ self.width * self.height }}\n"
                    "}}\n\n"
                    "fn render_all(drawables: &[&dyn Drawable]) {{\n"
                    "    for d in drawables {{\n"
                    "        d.draw();\n"
                    "    }}\n"
                    "}}\n\n"
                    "fn main() {{\n"
                    "    let c = Circle {{ radius: 1.0 }};\n"
                    "    let r = Rectangle {{ width: 2.0, height: 3.0 }};\n"
                    "    render_all(&[&c, &r]);\n"
                    "}}"
                ),
                "explanation": "Rust trait（特征）= 接口，dyn Trait 动态分发，impl Trait 静态分发。trait 可以有默认实现。",
            },
            "Go": {
                "code": (
                    "package main\n\n"
                    "import \"fmt\"\n\n"
                    "type Drawable interface {{\n"
                    "    Draw()\n"
                    "    Area() float64\n"
                    "}}\n\n"
                    "type Circle    struct {{ Radius float64 }}\n"
                    "type Rectangle struct {{ W, H float64 }}\n\n"
                    "func (c Circle)    Draw() {{ fmt.Println(\"Drawing Circle\") }}\n"
                    "func (c Circle)    Area() float64 {{ return 3.14159 * c.Radius * c.Radius }}\n"
                    "func (r Rectangle) Draw() {{ fmt.Println(\"Drawing Rectangle\") }}\n"
                    "func (r Rectangle) Area() float64 {{ return r.W * r.H }}\n\n"
                    "func render_all(drawables []Drawable) {{\n"
                    "    for _, d := range drawables {{\n"
                    "        d.Draw()\n"
                    "    }}\n"
                    "}}\n\n"
                    "func main() {{\n"
                    "    var drawables []Drawable = []Drawable{{\n"
                    "        Circle{{Radius: 1.0}},\n"
                    "        Rectangle{{W: 2.0, H: 3.0}},\n"
                    "    }}\n"
                    "    render_all(drawables)\n"
                    "}}"
                ),
                "explanation": "Go interface 是隐式实现（无需关键字），所有方法满足即实现接口，空 interface 可承载任何类型。",
            },
            "Swift": {
                "code": (
                    "protocol Drawable {{\n"
                    "    func draw()\n"
                    "    var area: Double {{ get }}\n"
                    "}}\n\n"
                    "struct Circle    {{ let radius: Double }}\n"
                    "struct Rectangle {{ let w: Double, h: Double }}\n\n"
                    "extension Circle: Drawable {{\n"
                    "    func draw() {{ print(\"Drawing Circle\") }}\n"
                    "    var area: Double {{ 3.14159 * radius * radius }}\n"
                    "}}\n\n"
                    "extension Rectangle: Drawable {{\n"
                    "    func draw() {{ print(\"Drawing Rectangle\") }}\n"
                    "    var area: Double {{ w * h }}\n"
                    "}}\n\n"
                    "func renderAll(_ drawables: [Drawable]) {{\n"
                    "    drawables.forEach {{ $0.draw() }}\n"
                    "}}"
                ),
                "explanation": "Swift protocol（协议），与 Rust trait 类似但语法不同。支持默认实现（extension）、class-only 协议、泛型约束。",
            },
            "Kotlin": {
                "code": (
                    "interface Drawable {{\n"
                    "    fun draw()\n"
                    "    val area: Double get()\n"
                    "}}\n\n"
                    "data class Circle(val radius: Double) : Drawable {{\n"
                    "    override fun draw() = println(\"Drawing Circle\")\n"
                    "    override val area: Double get() = 3.14159 * radius * radius\n"
                    "}}\n\n"
                    "data class Rectangle(val w: Double, val h: Double) : Drawable {{\n"
                    "    override fun draw() = println(\"Drawing Rectangle\")\n"
                    "    override val area: Double get() = w * h\n"
                    "}}\n\n"
                    "fun renderAll(drawables: List<Drawable>) {{\n"
                    "    drawables.forEach { it.draw() }\n"
                    "}}"
                ),
                "explanation": "Kotlin interface 与 Java 类似，但支持默认实现（Java 8+ 也支持）。实现用冒号（:），override 显式标注。",
            },
            "TypeScript": {
                "code": (
                    "interface Drawable {{\n"
                    "    draw(): void;\n"
                    "    area: number;\n"
                    "}}\n\n"
                    "class Circle implements Drawable {{\n"
                    "    constructor(public radius: number) {{ }}\n"
                    "    draw() {{ console.log('Drawing Circle'); }}\n"
                    "    get area() {{ return 3.14159 * this.radius ** 2; }}\n"
                    "}}\n\n"
                    "class Rectangle implements Drawable {{\n"
                    "    constructor(public w: number, public h: number) {{ }}\n"
                    "    draw() {{ console.log('Drawing Rectangle'); }}\n"
                    "    get area() {{ return this.w * this.h; }}\n"
                    "}}\n\n"
                    "function renderAll(drawables: Drawable[]) {{\n"
                    "    drawables.forEach(d => d.draw());\n"
                    "}}"
                ),
                "explanation": "TypeScript interface + class implements，编译时类型检查，运行时无接口元数据（结构化类型系统）。",
            },
            "JavaScript": {
                "code": (
                    "// JS 无接口机制，使用 duck typing 模拟\n"
                    "class Circle {{\n"
                    "    constructor(radius) {{ this.radius = radius; }}\n"
                    "    draw() {{ console.log('Drawing Circle'); }}\n"
                    "    get area() {{ return 3.14159 * this.radius ** 2; }}\n"
                    "}}\n\n"
                    "class Rectangle {{\n"
                    "    constructor(w, h) {{ this.w = w; this.h = h; }}\n"
                    "    draw() {{ console.log('Drawing Rectangle'); }}\n"
                    "    get area() {{ return this.w * this.h; }}\n"
                    "}}\n\n"
                    "function renderAll(drawables) {{\n"
                    "    drawables.forEach(d => d.draw());\n"
                    "}}\n\n"
                    "renderAll([new Circle(1), new Rectangle(2, 3)]);"
                ),
                "explanation": "JavaScript 无 interface 关键字，使用 duck typing：对象只要有 draw() 方法就可以用，无需显式声明实现。",
            },
            "Java": {
                "code": (
                    "interface Drawable {{\n"
                    "    void draw();\n"
                    "    double area();\n"
                    "}}\n\n"
                    "record Circle(double radius) implements Drawable {{\n"
                    "    public void draw() {{ System.out.println(\"Drawing Circle\"); }}\n"
                    "    public double area() {{ return Math.PI * radius * radius; }}\n"
                    "}}\n\n"
                    "record Rectangle(double w, double h) implements Drawable {{\n"
                    "    public void draw() {{ System.out.println(\"Drawing Rectangle\"); }}\n"
                    "    public double area() {{ return w * h; }}\n"
                    "}}\n\n"
                    "static void renderAll(List<Drawable> drawables) {{\n"
                    "    drawables.forEach(Drawable::draw);\n"
                    "}}"
                ),
                "explanation": "Java interface（Java 8+ 支持 default 方法），record 自动生成 constructor + getters + equals + hashCode + toString。",
            },
            "C/C++": {
                "code": (
                    "#include <stdio.h>\n\n"
                    "// 纯虚基类模拟接口\n"
                    "class Drawable {{\n"
                    "public:\n"
                    "    virtual ~Drawable() = default;\n"
                    "    virtual void draw() = 0;\n"
                    "    virtual double area() = 0;\n"
                    "}};\n\n"
                    "class Circle : public Drawable {{\n"
                    "    double radius;\npublic:\n"
                    "    Circle(double r) : radius(r) {{ }}\n"
                    "    void draw() override {{ printf(\"Drawing Circle\\n\"); }}\n"
                    "    double area() override {{ return 3.14159 * radius * radius; }}\n"
                    "}};\n\n"
                    "class Rectangle : public Drawable {{\n"
                    "    double w, h;\npublic:\n"
                    "    Rectangle(double w_, double h_) : w(w_), h(h_) {{ }}\n"
                    "    void draw() override {{ printf(\"Drawing Rectangle\\n\"); }}\n"
                    "    double area() override {{ return w * h; }}\n"
                    "}};\n\n"
                    "void render_all(Drawable* drawables[], size_t n) {{\n"
                    "    for (size_t i = 0; i < n; i++) {{\n"
                    "        drawables[i]->draw();\n"
                    "    }}\n"
                    "}}"
                ),
                "explanation": "C++ 使用抽象基类（abstract base class）：纯虚函数（= 0）定义接口，virtual + override 实现多态。",
            },
        },
    },

    "data_abstraction": {
        "title": "数据抽象",
        "title_en": "Data Abstraction",
        "description": (
            "如何封装和抽象数据。"
            "本示例展示：实现一个 'Stack'（栈）数据结构，"
            "包含 push、pop、peek、is_empty 操作，"
            "每种语言展示其封装和抽象数据的方式。"
        ),
        "concepts": {
            "Rust": {
                "code": (
                    "struct Stack<T> {{\n"
                    "    items: Vec<T>,\n"
                    "}}\n\n"
                    "impl<T> Stack<T> {{\n"
                    "    fn new() -> Self {{\n"
                    "        Self {{ items: Vec::new() }}\n"
                    "    }}\n"
                    "    fn push(&mut self, item: T) {{\n"
                    "        self.items.push(item);\n"
                    "    }}\n"
                    "    fn pop(&mut self) -> Option<T> {{\n"
                    "        self.items.pop()\n"
                    "    }}\n"
                    "    fn peek(&self) -> Option<&T> {{\n"
                    "        self.items.last()\n"
                    "    }}\n"
                    "    fn is_empty(&self) -> bool {{\n"
                    "        self.items.is_empty()\n"
                    "    }}\n"
                    "}}\n\n"
                    "fn main() {{\n"
                    "    let mut s = Stack::new();\n"
                    "    s.push(1); s.push(2); s.push(3);\n"
                    "    println!(\"Peek: {{:?}}\", s.peek());\n"
                    "    println!(\"Pop: {{:?}}\", s.pop());\n"
                    "    println!(\"Empty: {{}}\", s.is_empty());\n"
                    "}}"
                ),
                "explanation": "Rust struct + impl 方法范式，Option<T> 编码可能为空的情况，Vec<T> 提供动态数组，push/pop 均为 O(1)。",
            },
            "Go": {
                "code": (
                    "package main\n\n"
                    "import \"fmt\"\n\n"
                    "type Stack[T any] struct {{\n"
                    "    items []T\n"
                    "}}\n\n"
                    "func (s *Stack[T]) Push(item T) {{\n"
                    "    s.items = append(s.items, item)\n"
                    "}}\n\n"
                    "func (s *Stack[T]) Pop() (T, bool) {{\n"
                    "    if len(s.items) == 0 {{\n"
                    "        var zero T\n"
                    "        return zero, false\n"
                    "    }}\n"
                    "    item := s.items[len(s.items)-1]\n"
                    "    s.items = s.items[:len(s.items)-1]\n"
                    "    return item, true\n"
                    "}}\n\n"
                    "func (s *Stack[T]) Peek() (T, bool) {{\n"
                    "    if len(s.items) == 0 {{\n"
                    "        var zero T\n"
                    "        return zero, false\n"
                    "    }}\n"
                    "    return s.items[len(s.items)-1], true\n"
                    "}}\n\n"
                    "func (s *Stack[T]) IsEmpty() bool {{\n"
                    "    return len(s.items) == 0\n"
                    "}}"
                ),
                "explanation": "Go 1.18+ 泛型 struct + receiver method，append 动态扩容，slice 实现栈，空切片判断用 len == 0。",
            },
            "Swift": {
                "code": (
                    "struct Stack<Element> {{\n"
                    "    private var items: [Element] = []\n\n"
                    "    mutating func push(_ item: Element) {{\n"
                    "        items.append(item)\n"
                    "    }}\n\n"
                    "    mutating func pop() -> Element? {{\n"
                    "        items.popLast()\n"
                    "    }}\n\n"
                    "    func peek() -> Element? {{\n"
                    "        items.last\n"
                    "    }}\n\n"
                    "    var isEmpty: Bool {{\n"
                    "        items.isEmpty\n"
                    "    }}\n"
                    "}}\n\n"
                    "var s = Stack<Int>()\n"
                    "s.push(1); s.push(2); s.push(3)\n"
                    "print(\"Peek: \\(s.peek())\")\n"
                    "print(\"Pop: \\(s.pop())\")"
                ),
                "explanation": "Swift struct + mutating 方法（修改 self 需要 mutating），Array.last / popLast() 实现栈操作，泛型 Stack<Element>。",
            },
            "Kotlin": {
                "code": (
                    "class Stack<T> {{\n"
                    "    private val items = mutableListOf<T>()\n\n"
                    "    fun push(item: T) = items.add(item)\n"
                    "    fun pop(): T? = if (items.isNotEmpty()) items.removeAt(items.size - 1) else null\n"
                    "    fun peek(): T? = items.lastOrNull()\n"
                    "    val isEmpty: Boolean get() = items.isEmpty()\n"
                    "}}\n\n"
                    "fun main() {{\n"
                    "    val s = Stack<Int>()\n"
                    "    s.push(1); s.push(2); s.push(3)\n"
                    "    println(\"Peek: ${s.peek()}\")\n"
                    "    println(\"Pop: ${s.pop()}\")\n"
                    "}}"
                ),
                "explanation": "Kotlin class + private val（不可变引用），mutableListOf<T>() 提供可变列表，removeAt 实现 pop，lastOrNull 实现 peek。",
            },
            "TypeScript": {
                "code": (
                    "class Stack<T> {{\n"
                    "    private items: T[] = [];\n\n\n"
                    "    push(item: T): void {{\n"
                    "        this.items.push(item);\n"
                    "    }}\n\n"
                    "    pop(): T | undefined {{\n"
                    "        return this.items.pop();\n"
                    "    }}\n\n"
                    "    peek(): T | undefined {{\n"
                    "        return this.items[this.items.length - 1];\n"
                    "    }}\n\n"
                    "    get isEmpty(): boolean {{\n"
                    "        return this.items.length === 0;\n"
                    "    }}\n"
                    "}}\n\n"
                    "const s = new Stack<number>();\n"
                    "s.push(1); s.push(2); s.push(3);\n"
                    "console.log(`Peek: ${s.peek()}`);\n"
                    "console.log(`Pop: ${s.pop()}`);"
                ),
                "explanation": "TypeScript class，private 字段（# 开头的为真正私有字段），get 访问器实现 isEmpty，泛型类。",
            },
            "JavaScript": {
                "code": (
                    "class Stack {{\n"
                    "    #items = []; // 私有字段（ES2022+）\n\n\n"
                    "    push(item) {{\n"
                    "        this.#items.push(item);\n"
                    "    }}\n\n"
                    "    pop() {{\n"
                    "        return this.#items.pop();\n"
                    "    }}\n\n"
                    "    peek() {{\n"
                    "        return this.#items.at(-1);\n"
                    "    }}\n\n"
                    "    get isEmpty() {{\n"
                    "        return this.#items.length === 0;\n"
                    "    }}\n"
                    "}}\n\n"
                    "const s = new Stack();\n"
                    "s.push(1); s.push(2); s.push(3);\n"
                    "console.log(`Peek: ${s.peek()}`);\n"
                    "console.log(`Pop: ${s.pop()}`);"
                ),
                "explanation": "JavaScript ES2022 私有字段（# 前缀），class 语法，Array.prototype.push/pop/at()，无 TypeScript 时用 Symbol 模拟私有。",
            },
            "Java": {
                "code": (
                    "import java.util.ArrayList;\n"
                    "import java.util.Optional;\n\n"
                    "public class Stack<T> {{\n"
                    "    private final ArrayList<T> items = new ArrayList<>();\n\n"
                    "    public void push(T item) {{\n"
                    "        items.add(item);\n"
                    "    }}\n\n"
                    "    public Optional<T> pop() {{\n"
                    "        if (items.isEmpty()) return Optional.empty();\n"
                    "        return Optional.of(items.remove(items.size() - 1));\n"
                    "    }}\n\n"
                    "    public Optional<T> peek() {{\n"
                    "        return items.isEmpty() ? Optional.empty() : Optional.of(items.get(items.size() - 1));\n"
                    "    }}\n\n"
                    "    public boolean isEmpty() {{\n"
                    "        return items.isEmpty();\n"
                    "    }}\n"
                    "}}"
                ),
                "explanation": "Java 泛型类，ArrayList<T> 实现动态数组，Optional<T> 表示 pop/peek 的可能无值情况，public/private 访问控制。",
            },
            "C/C++": {
                "code": (
                    "#include <stdio.h>\n"
                    "#include <stdlib.h>\n\n"
                    "typedef struct {{\n"
                    "    int* items;\n"
                    "    size_t size;\n"
                    "    size_t capacity;\n"
                    "}} Stack;\n\n"
                    "Stack* stack_new() {{\n"
                    "    Stack* s = malloc(sizeof(Stack));\n"
                    "    s->items = NULL;\n"
                    "    s->size = 0;\n"
                    "    s->capacity = 0;\n"
                    "    return s;\n"
                    "}}\n\n"
                    "void stack_push(Stack* s, int val) {{\n"
                    "    if (s->size == s->capacity) {{\n"
                    "        s->capacity = s->capacity == 0 ? 4 : s->capacity * 2;\n"
                    "        s->items = realloc(s->items, s->capacity * sizeof(int));\n"
                    "    }}\n"
                    "    s->items[s->size++] = val;\n"
                    "}}\n\n"
                    "int stack_pop(Stack* s) {{\n"
                    "    return s->items[--s->size];\n"
                    "}}"
                ),
                "explanation": "C 语言手写 ADT：struct + malloc/realloc 实现动态栈，capacity 模式支持自动扩容，手动管理内存（需要 free）。",
            },
        },
    },
}


# ─────────────────────────────────────────────
# 范式主题列表（8 个，循环使用）
# ─────────────────────────────────────────────
PARADIGM_KEYS: List[str] = list(PARADIGM_DATABASE.keys())  # 8 个主题


# ─────────────────────────────────────────────
# 工具：读写 JSON
# ─────────────────────────────────────────────

def _read_json(json_path: str) -> Dict[str, Any]:
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)


def _write_json(json_path: str, data: Dict[str, Any]) -> None:
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# ─────────────────────────────────────────────
# 核心 API
# ─────────────────────────────────────────────

def rotate_and_weave(
    json_path: str = DEFAULT_LANGUAGE_ROTATION_JSON,
) -> Dict[str, Any]:
    """
    读取 language_rotation.json，取出 current_index，
    选择本次轮换的范式主题（按顺序循环），
    为所有 8 种语言生成代码示例，
    将 current_index 前移一位并更新 JSON。

    Returns:
        {
            "current_language": str,
            "next_language": str,
            "paradigm": {
                "key": str,
                "title": str,
                "title_en": str,
                "description": str,
            },
            "language_examples": {
                "Rust":    { "code": str, "explanation": str, "emoji": str },
                "Go":      { "code": str, "explanation": str, "emoji": str },
                ...
            },
            "rotation_index": int,
            "paradigm_index": int,   # 当前是第几个范式主题（0-7）
            "rotated_at": str,
        }
    """
    data = _read_json(json_path)
    languages = data["languages"]
    total = len(languages)
    lang_idx = data.get("current_index", 0) % total
    current_lang = languages[lang_idx]

    # 确定本次范式主题（按 PARADIGM_KEYS 循环）
    # 每次轮换语言时，paradigm_index 也前进一位
    # paradigm_idx 紧跟 current_index（而不是除以 total）
    paradigm_idx = data.get("current_index", 0) % len(PARADIGM_KEYS)
    paradigm_key = PARADIGM_KEYS[paradigm_idx]
    paradigm_info = PARADIGM_DATABASE[paradigm_key]

    # 更新 language_rotation.json
    next_lang_idx = (lang_idx + 1) % total
    data["current_index"] = next_lang_idx
    data["last_language"] = current_lang
    data["updated_at"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00")
    _write_json(json_path, data)

    # 构建语言示例字典
    language_examples: Dict[str, Dict[str, str]] = {}
    for lang in CORE_LANGUAGES:
        concept = paradigm_info["concepts"].get(lang, {})
        language_examples[lang] = {
            "code": concept.get("code", "// Not available"),
            "explanation": concept.get("explanation", ""),
            "emoji": LANGUAGE_EMOJI.get(lang, "📦"),
        }

    return {
        "current_language": current_lang,
        "next_language": languages[next_lang_idx],
        "paradigm": {
            "key": paradigm_key,
            "title": paradigm_info["title"],
            "title_en": paradigm_info["title_en"],
            "description": paradigm_info["description"],
        },
        "language_examples": language_examples,
        "rotation_index": lang_idx,
        "paradigm_index": paradigm_idx,
        "rotated_at": data["updated_at"],
    }


def get_weave_preview(
    language: Optional[str] = None,
    json_path: str = DEFAULT_LANGUAGE_ROTATION_JSON,
) -> Dict[str, Any]:
    """
    预览当前（或指定）语言的范式示例（不推进索引）。
    """
    data = _read_json(json_path)
    languages = data["languages"]
    if language is None:
        idx = data.get("current_index", 0) % len(languages)
        language = languages[idx]

    # 确定当前范式主题（与 rotate_and_weave 保持一致）
    paradigm_idx = data.get("current_index", 0) % len(PARADIGM_KEYS)
    paradigm_key = PARADIGM_KEYS[paradigm_idx]
    paradigm_info = PARADIGM_DATABASE[paradigm_key]

    concept = paradigm_info["concepts"].get(language, {})
    return {
        "language": language,
        "paradigm": {
            "key": paradigm_key,
            "title": paradigm_info["title"],
            "title_en": paradigm_info["title_en"],
            "description": paradigm_info["description"],
        },
        "example": {
            "code": concept.get("code", "// Not available"),
            "explanation": concept.get("explanation", ""),
        },
    }


# ─────────────────────────────────────────────
# 格式化输出
# ─────────────────────────────────────────────

def format_weave_console(result: Dict[str, Any]) -> str:
    """将范式对照报告格式化为控制台输出（ASCII-art 框）。"""
    paradigm = result["paradigm"]
    examples = result["language_examples"]

    header = [
        f"  ╔══════════════════════════════════════════════════════════════╗",
        f"  ║  🧩 Polyglot Paradigm Weaver — 编程范式织锦               ║",
        f"  ╠══════════════════════════════════════════════════════════════╣",
        f"  ║  📖 范式主题：{paradigm['title']} ({paradigm['title_en']})            ║",
    ]
    # 描述分行
    desc = paradigm["description"]
    for i in range(0, len(desc), 50):
        header.append(f"  ║    {desc[i:i+50]:<52}║")
    header.append(f"  ║  🌐 当前语言：{result['current_language']} {LANGUAGE_EMOJI.get(result['current_language'], ''):<38}║")
    header.append(f"  ║  ⏭️  下一个语言：{result['next_language']:<40}║")
    header.append(f"  ╠══════════════════════════════════════════════════════════════╣")

    # 8 种语言示例
    lines = header
    for lang in CORE_LANGUAGES:
        ex = examples[lang]
        emoji = ex["emoji"]
        lang_lines = ex["code"].split("\n")
        lines.append(f"  ║  {emoji} {lang:<10}│ {lang_lines[0]:<40}║")
        for ll in lang_lines[1:]:
            lines.append(f"  ║            │ {ll:<40}║")
        # 解释（截取）
        expl = ex["explanation"]
        for i in range(0, len(expl), 50):
            lines.append(f"  ║  💡        │ {expl[i:i+50]:<40}║")
        lines.append(f"  ╠══════════════════════════════════════════════════════════════╣")

    lines.append(f"  ║  🌀 Paradigm Index: {result['paradigm_index']}  |  Rotation Index: {result['rotation_index']}                   ║")
    lines.append(f"  ╚══════════════════════════════════════════════════════════════╝")
    return "\n".join(lines)


def format_weave_markdown(result: Dict[str, Any]) -> str:
    """将范式对照报告格式化为 Markdown，适合复制到文档。"""
    paradigm = result["paradigm"]
    examples = result["language_examples"]

    md = [
        f"## 🧩 Polyglot Paradigm Weaver — {paradigm['title']} ({paradigm['title_en']})",
        "",
        f"**描述**：{paradigm['description']}",
        "",
        f"**当前语言**：{result['current_language']} | **下一个语言**：{result['next_language']}",
        "",
        f"## 各语言实现",
        "",
    ]

    for lang in CORE_LANGUAGES:
        ex = examples[lang]
        emoji = ex["emoji"]
        ext = LANGUAGE_EXT.get(lang, "txt")
        md.append(f"### {emoji} {lang}")
        md.append(f"**解释**：{ex['explanation']}")
        md.append(f"```{ext}")
        md.append(ex["code"])
        md.append("```")
        md.append("")

    return "\n".join(md)


# ─────────────────────────────────────────────
# CLI 入口
# ─────────────────────────────────────────────

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Polyglot Paradigm Weaver — 编程范式织锦")
    sub = parser.add_subparsers(dest="cmd")

    sub.add_parser("weave", help="生成当前范式主题的跨语言对照报告并轮换语言")
    sub.add_parser("preview", help="预览当前语言的范式示例（不轮换）")
    sub.add_parser("list", help="列出所有支持的范式主题")
    preview_cmd = sub.add_parser("preview-lang", help="预览指定语言的范式示例（不轮换）")
    preview_cmd.add_argument("language", help="语言名称")

    args = parser.parse_args()

    if args.cmd == "weave":
        result = rotate_and_weave()
        print(format_weave_console(result))
    elif args.cmd == "preview":
        result = get_weave_preview()
        print(f"语言：{result['language']}")
        print(f"范式：{result['paradigm']['title']}")
        print(f"代码：\n{result['example']['code']}")
    elif args.cmd == "preview-lang":
        result = get_weave_preview(args.language)
        print(f"语言：{result['language']}")
        print(f"范式：{result['paradigm']['title']}")
        print(f"代码：\n{result['example']['code']}")
    elif args.cmd == "list":
        print("支持的范式主题：")
        for i, key in enumerate(PARADIGM_KEYS):
            info = PARADIGM_DATABASE[key]
            print(f"  {i+1}. {info['title']} ({info['title_en']})")
    else:
        parser.print_help()
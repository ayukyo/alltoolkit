"""
Polyglot Kata Generator — 多语言代码道场生成器

按 language_rotation.json 的轮换顺序，每次为当前语言生成一道
编程练习（kata）：包含题目描述、起始代码、提示和难度等级。

功能特性：
- 读取当前轮换语言
- 从语言专属题库随机抽取一道 kata
- 更新 JSON 索引
- 支持 CLI 指定语言或难度
- 生成格式化输出（Markdown 格式，便于直接复制）
"""

import json
import os
import random
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

# ── 路径配置 ────────────────────────────────────────────────
_MODULE_DIR = Path(__file__).parent.parent
_WORKSPACE_ROOT = _MODULE_DIR.parent
DEFAULT_LANGUAGE_ROTATION_JSON = str(_WORKSPACE_ROOT / "language_rotation.json")


# ── Kata 题库：每种语言 3 道题 ───────────────────────────────
KATA_DATABASE: Dict[str, List[Dict[str, Any]]] = {
    "Rust": [
        {
            "id": "rust-001",
            "title": "所有权转移 (Ownership Transfer)",
            "difficulty": "medium",
            "concept": "ownership & borrowing",
            "description": (
                "实现一个函数 `safe_transfer`，接受一个 `String`，\n"
                "将其转换为大写后返回，原始字符串被消耗（move）。\n"
                "不能使用 `.clone()`。"
            ),
            "starter_code": (
                "fn safe_transfer(s: String) -> String {\n"
                "    // 实现...\n"
                "}\n\n"
                "fn main() {\n"
                "    let original = String::from(\"hello world\");\n"
                "    let upper = safe_transfer(original);\n"
                "    // println!(\"{}\", original); // 这行应该编译错误\n"
                "    println!(\"{}\", upper);\n"
                "}"
            ),
            "hints": [
                "String 在 Rust 中默认是 Move 语义",
                "利用 `.to_uppercase()` 方法",
                "不需要 clone，因为所有权会转移进函数再转移出来",
            ],
            "solution": (
                "fn safe_transfer(s: String) -> String {\n"
                "    s.to_uppercase()\n"
                "}"
            ),
        },
        {
            "id": "rust-002",
            "title": "Result 错误处理 (Result Error Handling)",
            "difficulty": "easy",
            "concept": "Result type & ? operator",
            "description": (
                "实现 `parse_and_double` 函数，解析一个 &str 为 i32，\n"
                "成功则返回其两倍，失败则返回错误。"
            ),
            "starter_code": (
                "use std::num::ParseIntError;\n\n"
                "fn parse_and_double(s: &str) -> Result<i32, ParseIntError> {\n"
                "    // 实现...\n"
                "}\n\n"
                "fn main() {\n"
                "    println!(\"{:?}\", parse_and_double(\"42\"));\n"
                "    println!(\"{:?}\", parse_and_double(\"oops\"));\n"
                "}"
            ),
            "hints": [
                "使用 `?` 运算符传播 ParseIntError",
                "或者使用 `match` 手动处理",
            ],
            "solution": (
                "fn parse_and_double(s: &str) -> Result<i32, ParseIntError> {\n"
                "    let n: i32 = s.parse()?;\n"
                "    Ok(n * 2)\n"
                "}"
            ),
        },
        {
            "id": "rust-003",
            "title": "迭代器链 (Iterator Chaining)",
            "difficulty": "hard",
            "concept": "iterators & closures",
            "description": (
                "给定一个整数 vector，过滤掉奇数，对偶数平方，\n"
                "然后求和。使用迭代器链完成，一行流式调用。"
            ),
            "starter_code": (
                "fn sum_of_squared_evens(numbers: Vec<i32>) -> i32 {\n"
                "    // 使用迭代器链实现...\n"
                "}\n\n"
                "fn main() {\n"
                "    let nums = vec![1, 2, 3, 4, 5, 6, 7, 8, 9, 10];\n"
                "    println!(\"{}\", sum_of_squared_evens(nums));\n"
                "}"
            ),
            "hints": [
                "`.filter()` 过滤条件 `.into_iter().filter(|x| ...)`",
                "`.map()` 做转换 `.map(|x| x * x)`",
                "`.sum()` 汇总",
            ],
            "solution": (
                "fn sum_of_squared_evens(numbers: Vec<i32>) -> i32 {\n"
                "    numbers.into_iter()\n"
                "        .filter(|x| x % 2 == 0)\n"
                "        .map(|x| x * x)\n"
                "        .sum()\n"
                "}"
            ),
        },
    ],
    "Go": [
        {
            "id": "go-001",
            "title": "Goroutine 通道 (Goroutine & Channel)",
            "difficulty": "medium",
            "concept": "concurrency",
            "description": (
                "实现 `FanOut` 函数：启动 N 个 goroutine，\n"
                "每个计算 1..M 的和，结果通过 channel 收集，\n"
                "返回总和。"
            ),
            "starter_code": (
                "package main\n\n"
                "import \"sync\"\n\n"
                "func FanOut(n, m int) int {\n"
                "    // 启动 n 个 goroutine 计算 1..m 的和，汇总结果\n"
                "}\n\n"
                "func main() {\n"
                "    println(FanOut(4, 100))\n"
                "}"
            ),
            "hints": [
                "创建 buffered channel: `ch := make(chan int, n)`",
                "用 sync.WaitGroup 等待所有 goroutine 完成",
                "每个 goroutine 计算完往 channel 发数据",
            ],
            "solution": (
                "func FanOut(n, m int) int {\n"
                "    ch := make(chan int, n)\n"
                "    var wg sync.WaitGroup\n"
                "    for i := 0; i < n; i++ {\n"
                "        wg.Add(1)\n"
                "        go func() {\n"
                "            defer wg.Done()\n"
                "            sum := 0\n"
                "            for j := 1; j <= m; j++ {\n"
                "                sum += j\n"
                "            }\n"
                "            ch <- sum\n"
                "        }()\n"
                "    }\n"
                "    wg.Wait()\n"
                "    close(ch)\n"
                "    total := 0\n"
                "    for v := range ch {\n"
                "        total += v\n"
                "    }\n"
                "    return total\n"
                "}"
            ),
        },
        {
            "id": "go-002",
            "title": "Slice 追加陷阱 (Slice Append Gotcha)",
            "difficulty": "easy",
            "concept": "slice internals",
            "description": (
                "实现 `ExtendSlice` 函数，接受两个 slice，\n"
                "将第二个追加到第一个，返回新的 slice。\n"
                "不要使用内建的 `append`，手动实现。"
            ),
            "starter_code": (
                "package main\n\n"
                "func ExtendSlice(a, b []int) []int {\n"
                "    // 手动实现追加逻辑\n"
                "}\n\n"
                "func main() {\n"
                "    a := []int{1, 2, 3}\n"
                "    b := []int{4, 5, 6}\n"
                "    println(ExtendSlice(a, b))\n"
                "}"
            ),
            "hints": [
                "创建新 slice：`result := make([]int, len(a), len(a)+len(b))`",
                "用 copy 复制 a，再用 append 追加 b",
            ],
            "solution": (
                "func ExtendSlice(a, b []int) []int {\n"
                "    result := make([]int, len(a), len(a)+len(b))\n"
                "    copy(result, a)\n"
                "    result = append(result, b...)\n"
                "    return result\n"
                "}"
            ),
        },
        {
            "id": "go-003",
            "title": "HTTP 中间件链 (Middleware Chain)",
            "difficulty": "hard",
            "concept": "functional options & http.Handler",
            "description": (
                "实现一个简单的 HTTP 中间件链：\n"
                "`Chain(handler http.Handler, middlewares ...func(http.Handler) http.Handler) http.Handler`\n"
                "从左到右依次应用中间件。"
            ),
            "starter_code": (
                "package main\n\n"
                "import (\n"
                "    \"fmt\"\n"
                "    \"net/http\"\n"
                ")\n\n"
                "func Chain(handler http.Handler, middlewares ...func(http.Handler) http.Handler) http.Handler {\n"
                "    // 实现...\n"
                "}\n\n"
                "func main() {\n"
                "    handler := http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {\n"
                "        fmt.Fprintln(w, \"Hello!\")\n"
                "    })\n"
                "    // 用 Chain 包装 handler\n"
                "}"
            ),
            "hints": [
                "从后往前应用中间件，形成嵌套",
                "从右向左：`for i := len(middlewares)-1; i >= 0; i--`",
            ],
            "solution": (
                "func Chain(handler http.Handler, middlewares ...func(http.Handler) http.Handler) http.Handler {\n"
                "    for i := len(middlewares) - 1; i >= 0; i-- {\n"
                "        handler = middlewares[i](handler)\n"
                "    }\n"
                "    return handler\n"
                "}"
            ),
        },
    ],
    "Swift": [
        {
            "id": "swift-001",
            "title": "Result 类型 (Result Type)",
            "difficulty": "easy",
            "concept": "Result type & error handling",
            "description": (
                "实现一个函数 `divide`，接受两个整数，\n"
                "返回 Result<Int, DivisionError>，\n"
                "除数为 0 时返回 .failure(.divideByZero)。"
            ),
            "starter_code": (
                "enum DivisionError: Error {\n"
                "    case divideByZero\n"
                "}\n\n"
                "func divide(_ a: Int, by b: Int) -> Result<Int, DivisionError> {\n"
                "    // 实现...\n"
                "}\n\n"
                "print(divide(10, by: 2))\n"
                "print(divide(10, by: 0))"
            ),
            "hints": [
                "使用 `guard` 检查除数是否为 0",
                "返回 `.success(value)` 或 `.failure(.divideByZero)`",
            ],
            "solution": (
                "func divide(_ a: Int, by b: Int) -> Result<Int, DivisionError> {\n"
                "    guard b != 0 else {\n"
                "        return .failure(.divideByZero)\n"
                "    }\n"
                "    return .success(a / b)\n"
                "}"
            ),
        },
        {
            "id": "swift-002",
            "title": "Optional Chain 安全访问 (Safe Optional Chaining)",
            "difficulty": "medium",
            "concept": "optionals & guard",
            "description": (
                "给定嵌套的 Optional 字典，\n"
                "安全地提取最深层的值，避免嵌套 if-let。\n"
                "使用 optional chaining 和 flatMap。"
            ),
            "starter_code": (
                "let data: [String: [String: [String: Int]]] = [\n"
                "    \"user\": [\n"
                "        \"profile\": [\n"
                "            \"age\": 28\n"
                "        ]\n"
                "    ]\n"
                "]\n\n"
                "// 安全地获取 data[\"user\"][\"profile\"][\"age\"]\n"
                "func getAge(from data: [String: [String: [String: Int]]]) -> Int? {\n"
                "    // 实现...\n"
                "}\n\n"
                "print(getAge(from: data))"
            ),
            "hints": [
                "用 `flatMap` 链式解包每一层",
                "或者使用 `if let` 但保持扁平化",
            ],
            "solution": (
                "func getAge(from data: [String: [String: [String: Int]]]) -> Int? {\n"
                "    return data[\"user\"]?.flatMap { $0[\"profile\"] }?.flatMap { $0[\"age\"] }\n"
                "}"
            ),
        },
        {
            "id": "swift-003",
            "title": "Protocol + Generic 约束 (Protocol Constrained Generics)",
            "difficulty": "hard",
            "concept": "generics & protocol composition",
            "description": (
                "实现一个通用的 `batchProcess` 函数，\n"
                "接受一个遵循 `Sequence` 和 `Encodable` 的元素列表，\n"
                "将每个元素编码为 JSON Data 并返回数组。"
            ),
            "starter_code": (
                "import Foundation\n\n"
                "func batchProcess<T: Sequence & Encodable>(_ items: T) -> [Data] where T.Element: Encodable {\n"
                "    // 实现...\n"
                "}\n\n"
                "let names = [\"Alice\", \"Bob\", \"Charlie\"]\n"
                "let result = batchProcess(names)\n"
                "print(result.map { String(data: $0, encoding: .utf8) })"
            ),
            "hints": [
                "T 本身就是 Sequence，无需再迭代 T.Element",
                "使用 JSONEncoder 和 `encode` 方法",
            ],
            "solution": (
                "import Foundation\n\n"
                "func batchProcess<T: Sequence & Encodable>(_ items: T) -> [Data] where T.Element: Encodable {\n"
                "    let encoder = JSONEncoder()\n"
                "    return items.compactMap { try? encoder.encode($0) }\n"
                "}"
            ),
        },
    ],
    "Kotlin": [
        {
            "id": "kotlin-001",
            "title": "Sealed Class 状态建模 (Sealed Class State)",
            "difficulty": "easy",
            "concept": "sealed classes & when expression",
            "description": (
                "用 sealed class 建模网络请求状态：\n"
                "Loading, Success(data: String), Error(message: String)。\n"
                "写一个 `handleState` 函数处理每种状态。"
            ),
            "starter_code": (
                "sealed class Result<out T> {\n"
                "    data class Success<T>(val data: T): Result<T>()\n"
                "    data class Error(val message: String): Result<Nothing>()\n"
                "    object Loading : Result<Nothing>()\n"
                "}\n\n"
                "fun handleState(result: Result<String>) = when(result) {\n"
                "    // 实现各分支...\n"
                "}\n\n"
                "fun main() {\n"
                "    println(handleState(Result.Loading))\n"
                "    println(handleState(Result.Success(\"data\")))\n"
                "    println(handleState(Result.Error(\"oops\")))\n"
                "}"
            ),
            "hints": [
                "when 表达式必须覆盖所有分支，sealed class 保证 exhaustive",
                "data class 可以用 `is` 判断或解构",
            ],
            "solution": (
                "fun handleState(result: Result<String>) = when(result) {\n"
                "    is Result.Loading -> \"Loading...\"\n"
                "    is Result.Success -> \"Got: ${result.data}\"\n"
                "    is Result.Error -> \"Error: ${result.message}\"\n"
                "}"
            ),
        },
        {
            "id": "kotlin-002",
            "title": "Coroutine Flow 转换 (Flow Transformation)",
            "difficulty": "medium",
            "concept": "Kotlin Coroutines & Flow",
            "description": (
                "实现 `wordsFlow`，一个每秒发射一个单词的 Flow：\n"
                "[\"Hello\", \"Kotlin\", \"Flow\"]，\n"
                "使用 flow { emit() } 构建器，\n"
                "然后用 map + filter 转换，只保留长度 > 4 的单词。"
            ),
            "starter_code": (
                "import kotlinx.coroutines.*\nimport kotlinx.coroutines.flow.*\n\n"
                "fun wordsFlow() = flow {\n"
                "    // 每 1 秒 emit 一个词...\n"
                "}\n\n"
                "fun main() = runBlocking {\n"
                "    wordsFlow()\n"
                "        .map { it.uppercase() }\n"
                "        .filter { it.length > 4 }\n"
                "        .collect { println(it) }\n"
                "}"
            ),
            "hints": [
                "使用 `delay(1000)` 暂停",
                "emit 发射每个单词",
            ],
            "solution": (
                "fun wordsFlow() = flow {\n"
                "    val words = listOf(\"Hello\", \"Kotlin\", \"Flow\")\n"
                "    for (w in words) {\n"
                "        delay(1000)\n"
                "        emit(w)\n"
                "    }\n"
                "}.flowOn(Dispatchers.Default)"
            ),
        },
        {
            "id": "kotlin-003",
            "title": "Extension Function 作用域 (Scoped Extension Functions)",
            "difficulty": "hard",
            "concept": "extension functions & DSL",
            "description": (
                "实现一个 `applyIf` 扩展函数：\n"
                "仅当条件为 true 时，才在 receiver 对象上执行 block，\n"
                "然后返回 receiver。使用泛型。"
            ),
            "starter_code": (
                "inline fun <T> T.applyIf(\n"
                "    condition: Boolean,\n"
                "    block: T.() -> Unit\n"
                "): T {\n"
                "    // 实现...\n"
                "}\n\n"
                "fun main() {\n"
                "    val name = \"Kotlin\"\n"
                "    name.applyIf(name.length > 3) { println(\"Name is long!\") }\n"
                "    name.applyIf(name.length < 3) { println(\"Name is short!\") }\n"
                "    println(\"Final: $name\")\n"
                "}"
            ),
            "hints": [
                "if (condition) block() 在 receiver 作用域调用",
                "T.() -> Unit 表示在 T 的扩展作用域内调用",
            ],
            "solution": (
                "inline fun <T> T.applyIf(\n"
                "    condition: Boolean,\n"
                "    block: T.() -> Unit\n"
                "): T {\n"
                "    if (condition) block()\n"
                "    return this\n"
                "}"
            ),
        },
    ],
    "TypeScript": [
        {
            "id": "ts-001",
            "title": "Utility Types 变换 (Mapped & Conditional Types)",
            "difficulty": "medium",
            "concept": "advanced type system",
            "description": (
                "实现一个 `DeepReadonly<T>` 类型，\n"
                "将对象的所有嵌套属性递归设为 readonly。\n"
                "不使用任何运行时代码，纯类型实现。"
            ),
            "starter_code": (
                "type DeepReadonly<T> = // 实现...\n\n"
                "interface Config {\n"
                "    api: { url: string; timeout: number };\n"
                "    features: string[];\n"
                "}\n\n"
                "type ReadonlyConfig = DeepReadonly<Config>;\n"
                "// 验证: ReadonlyConfig['api']['url'] 是 string 且只读"
            ),
            "hints": [
                "使用 `[P in keyof T]: T[P] extends object ? ... : T[P]`",
                "递归地应用 DeepReadonly 到嵌套对象",
                "用 `Readonly<T>` 或 `{ readonly [P in keyof T]: ... }`",
            ],
            "solution": (
                "type DeepReadonly<T> = T extends (infer U)[]\n"
                "    ? ReadonlyArray<DeepReadonly<U>>\n"
                "    : T extends object\n"
                "        ? { readonly [P in keyof T]: DeepReadonly<T[P]> }\n"
                "        : T;"
            ),
        },
        {
            "id": "ts-002",
            "title": "Async Iterator 聚合 (Async Iterator Aggregation)",
            "difficulty": "easy",
            "concept": "async/await & generators",
            "description": (
                "实现 `asyncSum`，接受一个异步迭代器，\n"
                "返回所有数字的和。\n"
                "处理可能出现的错误。"
            ),
            "starter_code": (
                "async function asyncSum(\n"
                "    iter: AsyncIterable<number>\n"
                "): Promise<number> {\n"
                "    // 实现...\n"
                "}\n\n"
                "async function main() {\n"
                "    async function* gen() {\n"
                "        yield* [1, 2, 3, 4, 5];\n"
                "    }\n"
                "    console.log(await asyncSum(gen()));\n"
                "}\n"
                "main();"
            ),
            "hints": [
                "使用 `for await (const x of iter)` 遍历",
            ],
            "solution": (
                "async function asyncSum(\n"
                "    iter: AsyncIterable<number>\n"
                "): Promise<number> {\n"
                "    let sum = 0;\n"
                "    for await (const x of iter) {\n"
                "        sum += x;\n"
                "    }\n"
                "    return sum;\n"
                "}"
            ),
        },
        {
            "id": "ts-003",
            "title": "Decorator 记账 (Method Decorator Logging)",
            "difficulty": "hard",
            "concept": "decorators & reflection",
            "description": (
                "实现一个 `@logged` 方法装饰器，\n"
                "在方法调用前后打印参数和返回值。\n"
                "支持传递 `threshold` 参数控制哪些调用需要日志。"
            ),
            "starter_code": (
                "function logged(threshold?: number) {\n"
                "    return function <T>(\n"
                "        _target: T,\n"
                "        propertyKey: string,\n"
                "        descriptor: PropertyDescriptor\n"
                "    ) {\n"
                "        const original = descriptor.value;\n"
                "        descriptor.value = function(...args: any[]) {\n"
                "            // 实现...\n"
                "            const result = original.apply(this, args);\n"
                "            // 打印返回值...\n"
                "            return result;\n"
                "        };\n"
                "    };\n"
                "}\n\n"
                "class Calculator {\n"
                "    @logged()\n"
                "    add(a: number, b: number) { return a + b; }\n"
                "}\n"
                "new Calculator().add(1, 2);"
            ),
            "hints": [
                "用 `target` 和 `propertyKey` 组成日志前缀",
                "decorator factory 可以接受参数",
            ],
            "solution": (
                "function logged(threshold?: number) {\n"
                "    return function <T>(\n"
                "        target: T,\n"
                "        propertyKey: string,\n"
                "        descriptor: PropertyDescriptor\n"
                "    ) {\n"
                "        const original = descriptor.value;\n"
                "        descriptor.value = function(...args: any[]) {\n"
                "            console.log(`[${String(propertyKey)}] CALL:`, args);\n"
                "            const result = original.apply(this, args);\n"
                "            console.log(`[${String(propertyKey)}] RETURN:`, result);\n"
                "            return result;\n"
                "        };\n"
                "    };\n"
                "}"
            ),
        },
    ],
    "JavaScript": [
        {
            "id": "js-001",
            "title": "Promise 链式处理 (Promise Chain Pipeline)",
            "difficulty": "easy",
            "concept": "promises & async/await",
            "description": (
                "实现 `pipeline` 函数，\n"
                "接受多个异步函数作为管道步骤，\n"
                "依次调用并将上一步结果传给下一步。\n"
                "类似 Unix 管道或 RxJS 的 pipe。"
            ),
            "starter_code": (
                "async function pipeline(initialValue, ...fns) {\n"
                "    // 实现...\n"
                "}\n\n"
                "const addOne = x => Promise.resolve(x + 1);\n"
                "const double = x => Promise.resolve(x * 2);\n"
                "const toString = x => Promise.resolve(String(x));\n\n"
                "pipeline(5, addOne, double, toString)\n"
                "    .then(console.log); // \"12\""
            ),
            "hints": [
                "使用 `reduce` 遍历所有函数",
                "每个步骤的输出是 Promise，记得 await",
            ],
            "solution": (
                "async function pipeline(initialValue, ...fns) {\n"
                "    return fns.reduce(\n"
                "        (acc, fn) => acc.then(fn),\n"
                "        Promise.resolve(initialValue)\n"
                "    );\n"
                "}"
            ),
        },
        {
            "id": "js-002",
            "title": "Proxy 响应式对象 (Proxy-Based Reactivity)",
            "difficulty": "medium",
            "concept": "Proxy & Reflect",
            "description": (
                "实现 `reactive` 函数，\n"
                "返回一个 Proxy，拦截所有 get/set 操作，\n"
                "在属性变化时调用 `onChange(key, value)` 回调。"
            ),
            "starter_code": (
                "function reactive(obj, onChange) {\n"
                "    // 使用 Proxy 实现...\n"
                "}\n\n"
                "const state = reactive({ count: 0, name: 'Alice' }, (key, value) => {\n"
                "    console.log(`Changed ${key} -> ${value}`);\n"
                "});\n"
                "state.count = 1; // Changed count -> 1\n"
                "state.name = 'Bob'; // Changed name -> Bob"
            ),
            "hints": [
                "get handler 用 Reflect.get 返回值",
                "set handler 调用 onChange 后用 Reflect.set",
            ],
            "solution": (
                "function reactive(obj, onChange) {\n"
                "    return new Proxy(obj, {\n"
                "        get(target, prop, receiver) {\n"
                "            return Reflect.get(target, prop, receiver);\n"
                "        },\n"
                "        set(target, prop, value) {\n"
                "            onChange(prop, value);\n"
                "            return Reflect.set(target, prop, value);\n"
                "        }\n"
                "    });\n"
                "}"
            ),
        },
        {
            "id": "js-003",
            "title": "WeakMap 私有字段 (WeakMap Private Fields)",
            "difficulty": "hard",
            "concept": "WeakMap & privacy",
            "description": (
                "用 WeakMap 实现一个类 `SecureCounter`，\n"
                "计数器的 `count` 属性是真正私有的，\n"
                "外部无法直接访问或修改。"
            ),
            "starter_code": (
                "const _counters = new WeakMap();\n\n"
                "class SecureCounter {\n"
                "    constructor() {\n"
                "        // 初始化私有计数器...\n"
                "    }\n"
                "    increment() {\n"
                "        // 私有计数器 +1\n"
                "    }\n"
                "    getCount() {\n"
                "        // 返回计数\n"
                "    }\n"
                "}\n\n"
                "const c = new SecureCounter();\n"
                "c.increment(); c.increment();\n"
                "console.log(c.getCount()); // 2\n"
                "// console.log(c.count); // undefined"
            ),
            "hints": [
                "每个实例用 `new WeakMap()` 作为私有存储",
                "用 `this` 作为 key 存储/读取",
            ],
            "solution": (
                "const _counters = new WeakMap();\n\n"
                "class SecureCounter {\n"
                "    constructor() {\n"
                "        _counters.set(this, 0);\n"
                "    }\n"
                "    increment() {\n"
                "        _counters.set(this, _counters.get(this) + 1);\n"
                "    }\n"
                "    getCount() {\n"
                "        return _counters.get(this);\n"
                "    }\n"
                "}"
            ),
        },
    ],
    "Java": [
        {
            "id": "java-001",
            "title": "Stream 收集器 (Custom Stream Collector)",
            "difficulty": "medium",
            "concept": "Stream API & Collectors",
            "description": (
                "实现一个自定义 Collector，\n"
                "将字符串 Stream 收集为一个「按长度分组」的 Map：\n"
                "key=长度，value=该长度的所有字符串。\n"
                "使用 `Collector.of(...)`。"
            ),
            "starter_code": (
                "import java.util.*;\n"
                "import java.util.stream.*;\n\n"
                "public class GroupByLength {\n"
                "    public static Collector<String, ?, Map<Integer, List<String>>> groupByLength() {\n"
                "        // 实现...\n"
                "    }\n\n"
                "    public static void main(String[] args) {\n"
                "        List<String> words = Arrays.asList(\"hi\", \"hello\", \"hey\", \"yo\", \"greetings\");\n"
                "        Map<Integer, List<String>> grouped = words.stream().collect(groupByLength());\n"
                "        System.out.println(grouped);\n"
                "    }\n"
                "}"
            ),
            "hints": [
                "使用 `Collectors.groupingBy` 作为 supplier 的下游",
                "或手动实现 `supplier`, `accumulator`, `combiner`, `finisher`",
            ],
            "solution": (
                "public static Collector<String, ?, Map<Integer, List<String>>> groupByLength() {\n"
                "    return Collectors.groupingBy(String::length);\n"
                "}"
            ),
        },
        {
            "id": "java-002",
            "title": "Optional 链式调用 (Chained Optional Operations)",
            "difficulty": "easy",
            "concept": "Optional API",
            "description": (
                "实现 `getCityName`，接受一个 `Person` 对象，\n"
                "安全地链式提取 city：\n"
                "Person → Address → City → name。\n"
                "任一层为 null 都返回 \"Unknown\"。"
            ),
            "starter_code": (
                "import java.util.Optional;\n\n"
                "class Person {\n"
                "    Optional<Address> address = Optional.empty();\n"
                "}\n"
                "class Address {\n"
                "    Optional<City> city = Optional.empty();\n"
                "}\n"
                "class City {\n"
                "    String name = \"Beijing\";\n"
                "}\n\n"
                "String getCityName(Person p) {\n"
                "    // 实现...\n"
                "}"
            ),
            "hints": [
                "使用 `.flatMap()` 和 `.map()` 链式调用",
                "最后用 `.orElse(\"Unknown\")` 提供默认值",
            ],
            "solution": (
                "String getCityName(Person p) {\n"
                "    return p.address\n"
                "        .flatMap(Address::getCity)\n"
                "        .map(City::getName)\n"
                "        .orElse(\"Unknown\");\n"
                "}"
            ),
        },
        {
            "id": "java-003",
            "title": "CompletableFuture 组合 (CompletableFuture Pipeline)",
            "difficulty": "hard",
            "concept": "CompletableFuture & async",
            "description": (
                "实现 `fetchAndProcess`：\n"
                "1) 异步获取用户 ID（返回 CompletableFuture<Integer>）\n"
                "2) 用 ID 异步获取用户详情\n"
                "3) 转换用户名为大写\n"
                "使用 `thenCompose` 和 `thenApply`。"
            ),
            "starter_code": (
                "import java.util.concurrent.*;\n\n"
                "public class AsyncPipeline {\n"
                "    static CompletableFuture<Integer> fetchUserId() {\n"
                "        return CompletableFuture.supplyAsync(() -> 42);\n"
                "    }\n"
                "    static CompletableFuture<String> fetchUserName(int id) {\n"
                "        return CompletableFuture.supplyAsync(() -> \"user_\" + id);\n"
                "    }\n\n"
                "    public static CompletableFuture<String> fetchAndProcess() {\n"
                "        // 实现...\n"
                "    }\n\n"
                "    public static void main(String[] args) throws Exception {\n"
                "        System.out.println(fetchAndProcess().get());\n"
                "    }\n"
                "}"
            ),
            "hints": [
                "`thenCompose` 用于返回另一个 CompletableFuture 的链式调用",
                "`thenApply` 用于同步转换结果",
            ],
            "solution": (
                "public static CompletableFuture<String> fetchAndProcess() {\n"
                "    return fetchUserId()\n"
                "        .thenCompose(id -> fetchUserName(id))\n"
                "        .thenApply(String::toUpperCase);\n"
                "}"
            ),
        },
    ],
    "C/C++": [
        {
            "id": "cpp-001",
            "title": "模板元编程阶乘 (Template Metaprogramming Factorial)",
            "difficulty": "hard",
            "concept": "template metaprogramming",
            "description": (
                "用模板元编程在编译期计算阶乘。\n"
                "定义 `Factorial<N>::value` 在编译期求 N!。\n"
                "不能使用运行时循环或递归（函数递归除外）。"
            ),
            "starter_code": (
                "#include <iostream>\n\n"
                "template <int N>\n"
                "struct Factorial {\n"
                "    static constexpr int value = // 实现...\n"
                "};\n\n"
                "int main() {\n"
                "    std::cout << Factorial<5>::value << std::endl;  // 120\n"
                "    std::cout << Factorial<10>::value << std::endl; // 3628800\n"
                "}"
            ),
            "hints": [
                "使用模板特化作为递归终止条件",
                "主模板：`value = N * Factorial<N-1>::value`",
                "特化模板：`Factorial<0>::value = 1`",
            ],
            "solution": (
                "template <int N>\n"
                "struct Factorial {\n"
                "    static constexpr int value = N * Factorial<N - 1>::value;\n"
                "};\n\n"
                "template <>\n"
                "struct Factorial<0> {\n"
                "    static constexpr int value = 1;\n"
                "};"
            ),
        },
        {
            "id": "cpp-002",
            "title": "智能指针管理 (Smart Pointer Resource Management)",
            "difficulty": "medium",
            "concept": "shared_ptr & unique_ptr",
            "description": (
                "实现一个 `Factory` 类，\n"
                "用 `unique_ptr` 管理内部创建的资源，\n"
                "通过 `shared_ptr` 对外暴露。\n"
                "展示 `unique_ptr` 转 `shared_ptr` 的用法。"
            ),
            "starter_code": (
                "#include <memory>\n"
                "#include <iostream>\n\n"
                "class Resource {\n"
                "public:\n"
                "    Resource(int v): value(v) {}\n"
                "    int value;\n"
                "};\n\n"
                "class Factory {\n"
                "public:\n"
                "    std::shared_ptr<Resource> create(int v) {\n"
                "        // 用 unique_ptr 创建，转为 shared_ptr 返回\n"
                "    }\n"
                "};\n\n"
                "int main() {\n"
                "    Factory f;\n"
                "    auto r = f.create(42);\n"
                "    std::cout << r->value << std::endl;\n"
                "}"
            ),
            "hints": [
                "用 `std::make_unique` 创建 unique_ptr",
                "`std::move(unique_ptr)` 可以转为 shared_ptr",
            ],
            "solution": (
                "std::shared_ptr<Resource> create(int v) {\n"
                "    std::unique_ptr<Resource> p = std::make_unique<Resource>(v);\n"
                "    return std::move(p);\n"
                "}"
            ),
        },
        {
            "id": "cpp-003",
            "title": "Lambda 捕获与 std::function (Lambda Capture Pitfalls)",
            "difficulty": "easy",
            "concept": "lambda & closures",
            "description": (
                "实现 `makeMultiplier` 函数，\n"
                "返回一个 lambda，捕获一个整数倍数，\n"
                "返回的 lambda 接受一个数并返回其与倍数的乘积。\n"
                "展示按值捕获和按引用捕获的区别。"
            ),
            "starter_code": (
                "#include <functional>\n"
                "#include <iostream>\n\n"
                "std::function<int(int)> makeMultiplier(int multiplier) {\n"
                "    // 返回一个 lambda...\n"
                "}\n\n"
                "int main() {\n"
                "    auto times3 = makeMultiplier(3);\n"
                "    auto times5 = makeMultiplier(5);\n"
                "    std::cout << times3(10) << std::endl; // 30\n"
                "    std::cout << times5(10) << std::endl; // 50\n"
                "}"
            ),
            "hints": [
                "Lambda 捕获列表：`[multiplier]` 按值捕获",
                "返回类型 `std::function<int(int)>`",
            ],
            "solution": (
                "std::function<int(int)> makeMultiplier(int multiplier) {\n"
                "    return [multiplier](int x) {\n"
                "        return x * multiplier;\n"
                "    };\n"
                "}"
            ),
        },
    ],
}


# ── 辅助函数 ────────────────────────────────────────────────

def _read_rotation_json(json_path: str) -> Dict[str, Any]:
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)


def _write_rotation_json(json_path: str, data: Dict[str, Any]) -> None:
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def _format_kata_markdown(
    kata: Dict[str, Any],
    language: str,
    next_language: Optional[str] = None,
) -> str:
    """将 kata 对象格式化为友好的 Markdown 输出。"""
    diff_emoji = {
        "easy": "🟢",
        "medium": "🟡",
        "hard": "🔴",
    }.get(kata.get("difficulty", "medium"), "⚪")

    lines = [
        f"## 🏋️ Kata: {kata['title']}",
        f"",
        f"| 项目 | 内容 |",
        f"|------|------|",
        f"| 🎯 难度 | {diff_emoji} {kata['difficulty'].upper()} |",
        f"| 📚 概念 | {kata.get('concept', 'N/A')} |",
        f"| 🆔 ID | `{kata['id']}` |",
        f"",
        f"### 📋 题目描述",
        f"```\n{kata['description']}\n```",
        f"",
        f"### 💻 起始代码",
        f"```{_file_ext(language)}\n{kata['starter_code']}\n```",
        f"",
        f"### 💡 提示",
    ]
    for i, hint in enumerate(kata.get("hints", []), 1):
        lines.append(f"{i}. {hint}")

    lines.extend([
        "",
        f"### ✅ 参考解答",
        f"```{_file_ext(language)}\n{kata.get('solution', '// 稍后公布')}\n```",
    ])

    if next_language:
        lines.extend([
            "",
            f"---",
            f"📌 **下一个语言**: {next_language}  — 继续挑战！",
        ])

    return "\n".join(lines)


def _file_ext(language: str) -> str:
    exts = {
        "Rust": "rust", "Go": "go", "Swift": "swift",
        "Kotlin": "kotlin", "TypeScript": "typescript",
        "JavaScript": "javascript", "Java": "java", "C/C++": "cpp",
    }
    return exts.get(language, "text")


def _select_kata(language: str, difficulty: Optional[str] = None) -> Dict[str, Any]:
    """从题库中选取一道 kata。"""
    pool = KATA_DATABASE.get(language, [])
    if not pool:
        raise ValueError(f"未找到语言 '{language}' 的题库")
    if difficulty:
        filtered = [k for k in pool if k.get("difficulty") == difficulty]
        pool = filtered if filtered else pool
    return random.choice(pool)


# ── 主 API ──────────────────────────────────────────────────

def generate_kata(
    json_path: str = DEFAULT_LANGUAGE_ROTATION_JSON,
    difficulty: Optional[str] = None,
    seed: Optional[int] = None,
) -> Dict[str, Any]:
    """
    读取 language_rotation.json，按 current_index 确定当前语言，
    随机选一道 kata，返回 kata 详情（Markdown 格式），
    并将 current_index 前移一位。

    Args:
        json_path: language_rotation.json 路径
        difficulty: 可选难度过滤 ("easy" | "medium" | "hard")
        seed: 可选随机种子（用于测试可重现性）

    Returns:
        {
            "language": str,
            "next_language": str,
            "kata": {...},         # kata 字典
            "markdown": str,       # 格式化的 Markdown
            "json_updated": bool,
        }
    """
    if seed is not None:
        random.seed(seed)

    data = _read_rotation_json(json_path)
    languages = data["languages"]
    total = len(languages)
    idx = data.get("current_index", 0) % total

    current = languages[idx]
    next_idx = (idx + 1) % total
    next_lang = languages[next_idx]

    kata = _select_kata(current, difficulty)

    # 更新轮换索引
    data["current_index"] = next_idx
    data["last_language"] = current
    data["updated_at"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00")
    _write_rotation_json(json_path, data)

    markdown = _format_kata_markdown(kata, current, next_lang)

    return {
        "language": current,
        "next_language": next_lang,
        "kata": kata,
        "markdown": markdown,
        "json_updated": True,
    }


def preview_kata(
    language: Optional[str] = None,
    json_path: str = DEFAULT_LANGUAGE_ROTATION_JSON,
    difficulty: Optional[str] = None,
    seed: Optional[int] = None,
) -> Dict[str, Any]:
    """
    预览 kata（不推进索引）。
    如果不指定 language，使用当前轮换语言。
    """
    if seed is not None:
        random.seed(seed)

    if language is None:
        data = _read_rotation_json(json_path)
        languages = data["languages"]
        idx = data.get("current_index", 0) % len(languages)
        language = languages[idx]

    kata = _select_kata(language, difficulty)
    markdown = _format_kata_markdown(kata, language)

    return {
        "language": language,
        "kata": kata,
        "markdown": markdown,
    }


def list_katas_by_language(language: Optional[str] = None) -> Dict[str, Any]:
    """
    列出所有语言或指定语言的 kata 列表。
    """
    if language:
        pool = KATA_DATABASE.get(language, [])
        return {
            "language": language,
            "count": len(pool),
            "katas": [
                {
                    "id": k["id"],
                    "title": k["title"],
                    "difficulty": k["difficulty"],
                    "concept": k.get("concept", ""),
                }
                for k in pool
            ],
        }
    else:
        return {
            language: len(katas)
            for language, katas in KATA_DATABASE.items()
        }


def available_difficulties() -> List[str]:
    return ["easy", "medium", "hard"]


# ── CLI 入口 ────────────────────────────────────────────────

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Polyglot Kata Generator — 多语言代码道场"
    )
    sub = parser.add_subparsers(dest="cmd")

    gen = sub.add_parser("generate", help="生成 kata 并轮换语言")
    gen.add_argument(
        "--difficulty", "-d",
        choices=["easy", "medium", "hard"],
        help="按难度过滤"
    )
    gen.add_argument("--seed", "-s", type=int, help="随机种子（测试用）")

    sub.add_parser("preview", help="预览当前语言 kata（不轮换）")
    sub.add_parser("list", help="列出所有 kata")
    sub.add_parser("difficulties", help="列出可用难度")

    ls = sub.add_parser("ls", help="列出指定语言的 kata")
    ls.add_argument("language", nargs="?", help="语言名称")

    args = parser.parse_args()

    if args.cmd == "generate":
        result = generate_kata(difficulty=args.difficulty, seed=args.seed)
        print(f"\n🎯 语言: {result['language']}  →  下一个: {result['next_language']}\n")
        print(result["markdown"])
    elif args.cmd == "preview":
        result = preview_kata()
        print(f"\n🎯 语言: {result['language']}  (预览，不影响轮换)\n")
        print(result["markdown"])
    elif args.cmd == "list":
        summary = list_katas_by_language()
        print("\n📚 各语言 kata 数量：")
        for lang, count in summary.items():
            print(f"  {lang}: {count} 道")
    elif args.cmd == "difficulties":
        print("可用难度等级:", ", ".join(available_difficulties()))
    elif args.cmd == "ls":
        result = list_katas_by_language(args.language)
        if "count" in result:
            print(f"\n📚 {result['language']} — {result['count']} 道 kata:\n")
            for k in result["katas"]:
                diff_emoji = {"easy": "🟢", "medium": "🟡", "hard": "🔴"}.get(k["difficulty"], "⚪")
                print(f"  [{k['id']}] {diff_emoji} {k['title']} ({k['difficulty']})")
                print(f"      概念: {k['concept']}")
        else:
            print(result)
    else:
        parser.print_help()
r"""
polyglot_quiz.py — 编程语言身份猜谜 (Polyglot Quiz)
====================================================================
一个与 language_rotation.json 深度集成的代码模式识别 Quiz 模块。

核心逻辑：
  1. 读取 language_rotation.json，按 current_index 取当前轮换语言
  2. 从该语言的 idiom 题库中抽取一道题（展示代码片段，隐藏语言名）
  3. 提供 4 选 1 选项，用户可猜答，答对加分，答错显示解析
  4. 支持简答题模式（直接输入语言名）
  5. 记录 Quiz 历史到 JSON，追踪准确率
  6. 完成后将 current_index 前移一位并更新 updated_at

语言轮换顺序（8 种核心语言）：
  Rust → Go → Swift → Kotlin → TypeScript → JavaScript → Java → C/C++ → Rust（循环）

作者：AllToolkit 全自动生成
依赖：仅 Python 标准库（json, random, datetime, pathlib）
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
_MODULE_DIR = Path(__file__).parent.parent          # alltoolkit-python/
_WORKSPACE_ROOT = _MODULE_DIR.parent               # workspace/
DEFAULT_LANGUAGE_ROTATION_JSON = str(_WORKSPACE_ROOT / "language_rotation.json")
DEFAULT_QUIZ_HISTORY_JSON = str(_WORKSPACE_ROOT / "polyglot_quiz_history.json")


# ─────────────────────────────────────────────
# 语言元数据（与 language_tools.py 保持一致）
# ─────────────────────────────────────────────
LANGUAGE_METADATA: Dict[str, Dict[str, Any]] = {
    "Rust": {
        "emoji": "\U0001f980",
        "tagline": "Safe, concurrent, practical.",
        "hello_world": r"fn main() { println!('Hello, World!'); }",
        "file_ext": "rs",
        "year": 2015,
        "paradigm": "Systems / Memory-safe",
    },
    "Go": {
        "emoji": "\U0001f43b",
        "tagline": "Go is expressive, concise, and clean.",
        "hello_world": r"package main@@import 'fmt'@@func main() {@@    fmt.Println('Hello, World!')@@}",
        "file_ext": "go",
        "year": 2009,
        "paradigm": "Concurrent / Compiled",
    },
    "Swift": {
        "emoji": "\U0001f985",
        "tagline": "Anyone who writes software should read Swift.",
        "hello_world": r"print('Hello, World!')",
        "file_ext": "swift",
        "year": 2014,
        "paradigm": "Multi-paradigm / Safe",
    },
    "Kotlin": {
        "emoji": "\U0001f7eb",
        "tagline": "Better language for Android and JVM.",
        "hello_world": r"fun main() {@@    println('Hello, World!')@@}",
        "file_ext": "kt",
        "year": 2011,
        "paradigm": "OO / Functional / JVM",
    },
    "TypeScript": {
        "emoji": "\U0001f534",
        "tagline": "JavaScript that scales.",
        "hello_world": r"console.log('Hello, World!');",
        "file_ext": "ts",
        "year": 2012,
        "paradigm": "Typed Superset of JS",
    },
    "JavaScript": {
        "emoji": "\U0001f7e1",
        "tagline": "The language of the web.",
        "hello_world": r"console.log('Hello, World!');",
        "file_ext": "js",
        "year": 1995,
        "paradigm": "Dynamic / Prototype-based",
    },
    "Java": {
        "emoji": "\u2615",
        "tagline": "Write once, run anywhere.",
        "hello_world": r"public class Hello {@@    public static void main(String[] args) {@@        System.out.println('Hello, World!');@@    }@@}",
        "file_ext": "java",
        "year": 1995,
        "paradigm": "OO / Class-based / JVM",
    },
    "C/C++": {
        "emoji": "\U0001f529",
        "tagline": "Close to the metal, close to perfection.",
        "hello_world": r"#include <stdio.h>@@int main() {@@    printf('Hello, World!\n');@@    return 0;@@}",
        "file_ext": "cpp",
        "year": 1983,
        "paradigm": "Systems / Low-level",
    },
}

CORE_LANGUAGES = list(LANGUAGE_METADATA.keys())


def _join_lines(text: str) -> str:
    """将用 @@ 分隔符存储的多行代码片段还原为带换行的字符串。"""
    return text.replace("@@", "\n")


# ─────────────────────────────────────────────
# 题库：每种语言 3+ 道 idiom 题目
# 使用 @@ 作为行分隔符避免引号冲突
# 题目 = { "code": str, "hint": str, "distractors": [str] }
# ─────────────────────────────────────────────
QUIZ_DB: Dict[str, List[Dict[str, Any]]] = {
    "Rust": [
        {
            "code": r"let mut x = 5;@@x = 6;@@println!('{:?}', x);",
            "hint": "变量默认不可变，且用 println! 宏打印调试信息",
            "distractors": ["Go", "Swift", "Kotlin"],
        },
        {
            "code": r"fn add(a: i32, b: i32) -> i32 {@@    a + b@@}@@let result = add(1, 2);",
            "hint": "函数返回值不需要 return 关键字，表达式隐式返回值",
            "distractors": ["Go", "Swift", "Kotlin"],
        },
        {
            "code": (r"match value {@@"
                     r"    Some(x) if x > 0 => println!('positive'),@@"
                     r"    None => println!('none'),@@"
                     r"    _ => println!('other'),@@"
                     r"}"),
            "hint": "强大的模式匹配，带守卫条件",
            "distractors": ["Swift", "Kotlin", "JavaScript"],
        },
        {
            "code": (r"struct Point { x: f64, y: f64 }@@"
                     r"impl Point {@@"
                     r"    fn distance(&self) -> f64 {@@"
                     r"        (self.x.powi(2) + self.y.powi(2)).sqrt()@@"
                     r"    }@@"
                     r"}"),
            "hint": "结构体带方法实现，用 impl 块定义",
            "distractors": ["Go", "Swift", "Kotlin"],
        },
    ],
    "Go": [
        {
            "code": (r"func main() {@@"
                     r"    ch := make(chan int)@@"
                     r"    go func() { ch <- 42 }()@@"
                     r"    fmt.Println(<-ch)@@"
                     r"}"),
            "hint": "goroutine + channel 并发模型，用 make 创建 channel",
            "distractors": ["Rust", "Swift", "Kotlin"],
        },
        {
            "code": (r"type User struct {@@"
                     r"    Name string `json:'name'`@@"
                     r"    Age  int    `json:'age'`@@"
                     r"}@@"
                     r"data, _ := json.Marshal(user)@@"
                     r"fmt.Println(string(data))"),
            "hint": "结构体标签（struct tags）用于 JSON 序列化",
            "distractors": ["Rust", "Swift", "Kotlin"],
        },
        {
            "code": (r"func worker(ctx context.Context) {@@"
                     r"    for {@@"
                     r"        select {@@"
                     r"        case <-ctx.Done():@@"
                     r"            return@@"
                     r"        default:@@"
                     r"        }@@"
                     r"    }@@"
                     r"}"),
            "hint": "context 包用于 Cancellation，支持 select 多路复用",
            "distractors": ["Rust", "Swift", "Kotlin"],
        },
        {
            "code": (r"m := map[string]int{'a': 1, 'b': 2}@@"
                     r"for k, v := range m {@@"
                     r"    fmt.Println(k, v)@@"
                     r"}"),
            "hint": "内置 map 类型，range 遍历 key-value 对",
            "distractors": ["Rust", "Swift", "Kotlin"],
        },
    ],
    "Swift": [
        {
            "code": (r"var items = [1, 2, 3, 4, 5]@@"
                     r"let filtered = items.filter { $0 % 2 == 0 }@@"
                     r"print(filtered)"),
            "hint": "闭包简写形式 $0 代表第一个参数，filter 高阶函数",
            "distractors": ["Kotlin", "Rust", "JavaScript"],
        },
        {
            "code": (r"protocol Drawable {@@"
                     r"    func draw()@@"
                     r"}@@"
                     r"struct Circle: Drawable {@@"
                     r"    func draw() { print('circle') }@@"
                     r"}"),
            "hint": "protocol 定义接口，struct 通过 : 实现协议（不是 implements）",
            "distractors": ["Go", "Rust", "Kotlin"],
        },
        {
            "code": (r"guard let name = optionalName else {@@"
                     r"    return@@"
                     r"}@@"
                     r"print(name)"),
            "hint": "guard 语句解包可选值，失败时提前退出",
            "distractors": ["Rust", "Go", "Kotlin"],
        },
        {
            "code": (r"let result: Result<Int, Error> = .success(42)@@"
                     r"switch result {@@"
                     r"case .success(let v): print(v)@@"
                     r"case .failure(let e): print(e)@@"
                     r"}"),
            "hint": "Result 类型，.success / .failure 构造器，switch 模式匹配",
            "distractors": ["Rust", "Kotlin", "JavaScript"],
        },
    ],
    "Kotlin": [
        {
            "code": (r"val list = listOf(1, 2, 3).map { it * 2 }.filter { it > 2 }@@"
                     r"println(list)"),
            "hint": "链式调用，it 是单个参数的隐式名称，支持 JVM 函数式编程",
            "distractors": ["Swift", "JavaScript", "Rust"],
        },
        {
            "code": (r"sealed class Result<out T>@@"
                     r"class Success<T>(val data: T): Result<T>()@@"
                     r"class Failure(val error: String): Result<Nothing>()"),
            "hint": "密封类（sealed class）定义受限类型层次结构",
            "distractors": ["Rust", "Swift", "Go"],
        },
        {
            "code": (r"suspend fun fetchData(): String {@@"
                     r"    return withContext(Dispatchers.IO) {@@"
                     r"        'data'@@"
                     r"    }@@"
                     r"}"),
            "hint": "协程关键字 suspend，withContext 切换调度器",
            "distractors": ["Rust", "Go", "JavaScript"],
        },
        {
            "code": (r"val map = mapOf('a' to 1, 'b' to 2)@@"
                     r"for ((k, v) in map) println('$k -> $v')"),
            "hint": "字符串模板 $var，to 中缀运算符创建 Pair",
            "distractors": ["Go", "Rust", "Swift"],
        },
    ],
    "TypeScript": [
        {
            "code": (r"type Maybe<T> = T | undefined;@@"
                     r"function greet(name: Maybe<string>): string {@@"
                     r"    return `Hello, ${name ?? 'World'}!`;@@"
                     r"}"),
            "hint": "类型别名 type，?? 空值合并运算符，模板字符串",
            "distractors": ["JavaScript", "Kotlin", "Swift"],
        },
        {
            "code": (r"interface Config {@@"
                     r"    timeout?: number;@@"
                     r"    readonly endpoint: string;@@"
                     r"}@@"
                     r"const cfg: Config = { endpoint: '/api' };"),
            "hint": "interface 可选属性 (?) 和只读属性 (readonly)",
            "distractors": ["Java", "Go", "Kotlin"],
        },
        {
            "code": (r"type Event = 'click' | 'scroll' | 'mousemove';@@"
                     r"function handle(e: Event): void {@@"
                     r"    if (e === 'click') {}@@"
                     r"}"),
            "hint": "字符串字面量类型（union of literals），严格类型枚举替代",
            "distractors": ["Rust", "Swift", "Kotlin"],
        },
        {
            "code": (r"async function fetchUser(id: number): Promise<User> {@@"
                     r"    const res = await fetch(`/users/${id}`);@@"
                     r"    return res.json();@@"
                     r"}"),
            "hint": "async/await，内置 Promise 泛型，fetch API",
            "distractors": ["JavaScript", "Go", "Rust"],
        },
    ],
    "JavaScript": [
        {
            "code": (r"const obj = { a: 1, b: 2 };@@"
                     r"const keys = Object.keys(obj);@@"
                     r"const entries = Object.entries(obj);"),
            "hint": "Object.keys / Object.entries 是静态方法，数组方法链式调用",
            "distractors": ["TypeScript", "Kotlin", "Python"],
        },
        {
            "code": (r"async function* gen() {@@"
                     r"    yield 1;@@"
                     r"    yield 2;@@"
                     r"    yield 3;@@"
                     r"}@@"
                     r"for await (const v of gen()) console.log(v);"),
            "hint": "async generator 函数，yield 暂停，for await...of 消费",
            "distractors": ["Python", "Rust", "TypeScript"],
        },
        {
            "code": (r"const merged = [...arr1, ...arr2];@@"
                     r"const { a, ...rest } = obj;@@"
                     r"const rounded = Number(price.toFixed(2));"),
            "hint": "展开运算符 ...，解构赋值，余运算符",
            "distractors": ["TypeScript", "Python", "Rust"],
        },
        {
            "code": (r"const cache = new Map();@@"
                     r"cache.set('key', 'value');@@"
                     r"const val = cache.get('key') ?? 'default';"),
            "hint": "Map 对象，?? 空值合并（ES2020+）",
            "distractors": ["TypeScript", "Kotlin", "Java"],
        },
    ],
    "Java": [
        {
            "code": (r"public class Box<T> {@@"
                     r"    private T value;@@"
                     r"    public T get() { return value; }@@"
                     r"    public void set(T value) { this.value = value; }@@"
                     r"}"),
            "hint": "泛型类声明 <T>，实例方法泛型返回类型",
            "distractors": ["Kotlin", "C/C++", "TypeScript"],
        },
        {
            "code": (r"try (var conn = DriverManager.getConnection(url)) {@@"
                     r"    var stmt = conn.prepareStatement(sql);@@"
                     r"    var rs = stmt.executeQuery();@@"
                     r"} catch (SQLException e) {@@"
                     r"    e.printStackTrace();@@"
                     r"}"),
            "hint": "try-with-resources 自动资源管理，var 类型推断（JDK 10+）",
            "distractors": ["Kotlin", "Go", "Python"],
        },
        {
            "code": (r"record Point(int x, int y) {@@"
                     r"    public double distance() {@@"
                     r"        return Math.sqrt(x*x + y*y);@@"
                     r"    }@@"
                     r"}"),
            "hint": "record 类型（JDK 16+），自动生成 equals/hashCode/toString",
            "distractors": ["Kotlin", "Rust", "Swift"],
        },
        {
            "code": (r"@FunctionalInterface@@"
                     r"interface Calculator {@@"
                     r"    int compute(int a, int b);@@"
                     r"}@@"
                     r"Calculator add = (a, b) -> a + b;"),
            "hint": "@FunctionalInterface，lambda 表达式 (a, b) -> expr",
            "distractors": ["Kotlin", "JavaScript", "TypeScript"],
        },
    ],
    "C/C++": [
        {
            "code": (r"int* ptr = malloc(sizeof(int) * 10);@@"
                     r"free(ptr);@@"
                     r"printf('Value: %d\n', *ptr);"),
            "hint": "malloc/free 手动内存管理，指针运算，printf 格式化输出",
            "distractors": ["Java", "Rust", "Go"],
        },
        {
            "code": (r"template<typename T>@@"
                     r"T max(T a, T b) {@@"
                     r"    return a > b ? a : b;@@"
                     r"}"),
            "hint": "template<typename T> 模板元编程，编译期多态",
            "distractors": ["Java", "Kotlin", "Rust"],
        },
        {
            "code": (r"std::vector<int> v = {1, 2, 3};@@"
                     r"std::sort(v.begin(), v.end(), [](int a, int b) {@@"
                     r"    return a > b;@@"
                     r"});"),
            "hint": "STL 容器 std::vector，std::sort，lambda 比较器",
            "distractors": ["Java", "Kotlin", "TypeScript"],
        },
        {
            "code": (r"struct Node {@@"
                     r"    int value;@@"
                     r"    struct Node* next;@@"
                     r"};@@"
                     r"typedef struct Node* NodePtr;"),
            "hint": "struct 自引用指针，typedef 定义类型别名",
            "distractors": ["Rust", "Go", "Java"],
        },
    ],
}


# ─────────────────────────────────────────────
# 核心 API
# ─────────────────────────────────────────────

def _read_json(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _write_json(path: str, data: Dict[str, Any]) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def _get_rotation_state(json_path: str = DEFAULT_LANGUAGE_ROTATION_JSON) -> Dict[str, Any]:
    """读取当前轮换状态（不推进索引）"""
    data = _read_json(json_path)
    languages = data["languages"]
    idx = data.get("current_index", 0) % len(languages)
    return {
        "languages": languages,
        "current_language": languages[idx],
        "current_index": idx,
        "next_language": languages[(idx + 1) % len(languages)],
        "total": len(languages),
        "last_language": data.get("last_language", ""),
        "updated_at": data.get("updated_at", ""),
    }


def _advance_rotation(json_path: str = DEFAULT_LANGUAGE_ROTATION_JSON) -> str:
    """推进轮换索引，返回当前语言名称"""
    data = _read_json(json_path)
    languages = data["languages"]
    idx = data.get("current_index", 0) % len(languages)
    current = languages[idx]
    next_idx = (idx + 1) % len(languages)
    data["current_index"] = next_idx
    data["last_language"] = current
    data["updated_at"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00")
    _write_json(json_path, data)
    return current


def generate_quiz(
    language: Optional[str] = None,
    difficulty: str = "medium",
    quiz_db: Optional[Dict[str, List[Dict[str, Any]]]] = None,
) -> Dict[str, Any]:
    """
    生成一道 Quiz 题。

    Args:
        language: 指定语言，默认为当前轮换语言
        difficulty: 预留参数（暂未细分难度）
        quiz_db: 题目数据库，默认使用内置 QUIZ_DB

    Returns:
        {
            "question_id": str,
            "language": str,
            "emoji": str,
            "code": str,
            "hint": str,
            "options": [{"label": str, "value": str}],   # 4 选 1
            "correct_answer": str,
            "explanation": str,
            "topic": str,
        }
    """
    if quiz_db is None:
        quiz_db = QUIZ_DB

    if language is None:
        state = _get_rotation_state()
        language = state["current_language"]

    if language not in quiz_db:
        raise ValueError("language '''' + language + ''' not in quiz DB")

    questions = quiz_db[language]
    question = random.choice(questions)

    # Build 4-option multiple choice
    all_langs = list(quiz_db.keys())
    correct = language
    distractors = question.get("distractors", [])

    valid_distractors = [d for d in distractors if d != correct and d in all_langs]
    while len(valid_distractors) < 3:
        pool = [l for l in all_langs if l != correct and l not in valid_distractors]
        random.shuffle(pool)
        valid_distractors.append(pool.pop())

    options = [{"label": valid_distractors[i], "value": valid_distractors[i]} for i in range(3)]
    options.append({"label": correct, "value": correct})
    random.shuffle(options)

    meta = LANGUAGE_METADATA.get(correct, {})
    emoji = meta.get("emoji", "\U0001f4e6")
    tagline = meta.get("tagline", "")
    paradigm = meta.get("paradigm", "")

    return {
        "question_id": "q_" + correct.lower() + "_" + datetime.now().strftime("%H%M%S"),
        "language": correct,
        "emoji": emoji,
        "code": _join_lines(question["code"]),
        "hint": question["hint"],
        "options": options,
        "correct_answer": correct,
        "explanation": (
            emoji + " 这段代码来自 ***" + correct + "***！\n"
            "   " + tagline + "\n"
            "   范式：" + paradigm + "\n"
            "   提示：" + question["hint"]
        ),
        "topic": paradigm,
    }


def check_answer(
    question_id: str,
    user_answer: str,
    language: str,
    quiz_db: Optional[Dict[str, List[Dict[str, Any]]]] = None,
) -> Dict[str, Any]:
    """
    检查用户答案，返回判定结果。（大小写不敏感）
    """
    correct = user_answer.strip().lower() == language.strip().lower()
    meta = LANGUAGE_METADATA.get(language, {})
    emoji = meta.get("emoji", "\U0001f4e6")
    tagline = meta.get("tagline", "")

    return {
        "correct": correct,
        "correct_answer": language,
        "explanation": (
            emoji + " 正确答案：***" + language + "***！\n"
            "   " + tagline
        ) if correct else (
            "\u274c 答错了！正确答案是 ***" + language + "***。\n"
            "   " + emoji + " " + tagline
        ),
        "emoji": emoji,
    }


def get_quiz_stats(
    history_path: str = DEFAULT_QUIZ_HISTORY_JSON,
) -> Dict[str, Any]:
    """
    读取 Quiz 历史，返回统计信息。
    """
    if not os.path.exists(history_path) or os.path.getsize(history_path) == 0:
        return {
            "total_attempts": 0,
            "correct_count": 0,
            "accuracy": 0.0,
            "by_language": {},
        }

    data = _read_json(history_path)
    attempts = data.get("attempts", [])
    if not attempts:
        return {
            "total_attempts": 0,
            "correct_count": 0,
            "accuracy": 0.0,
            "by_language": {},
        }

    correct_count = sum(1 for a in attempts if a.get("correct"))
    total = len(attempts)
    accuracy = round(correct_count / total * 100, 1) if total > 0 else 0.0

    by_lang: Dict[str, Dict[str, Any]] = {}
    for a in attempts:
        lang = a.get("language", "unknown")
        if lang not in by_lang:
            by_lang[lang] = {"total": 0, "correct": 0}
        by_lang[lang]["total"] += 1
        if a.get("correct"):
            by_lang[lang]["correct"] += 1

    for lang, stats in by_lang.items():
        stats["accuracy"] = round(stats["correct"] / stats["total"] * 100, 1) if stats["total"] > 0 else 0.0

    return {
        "total_attempts": total,
        "correct_count": correct_count,
        "accuracy": accuracy,
        "by_language": by_lang,
    }


def record_attempt(
    question_id: str,
    language: str,
    user_answer: str,
    correct: bool,
    history_path: str = DEFAULT_QUIZ_HISTORY_JSON,
) -> None:
    """
    记录一次答题尝试到历史 JSON。
    """
    if os.path.exists(history_path) and os.path.getsize(history_path) > 0:
        data = _read_json(history_path)
    else:
        data = {"attempts": [], "summary": {}}

    data["attempts"].append({
        "question_id": question_id,
        "language": language,
        "user_answer": user_answer,
        "correct": correct,
        "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00"),
    })

    data["summary"] = {
        "total": len(data["attempts"]),
        "correct": sum(1 for a in data["attempts"] if a.get("correct")),
    }

    _write_json(history_path, data)


def rotate_and_get_quiz(
    language: Optional[str] = None,
    difficulty: str = "medium",
    json_path: str = DEFAULT_LANGUAGE_ROTATION_JSON,
) -> Dict[str, Any]:
    """
    完整 Quiz 流程：
    1. 推进语言轮换（读取 current_index，更新 JSON）
    2. 生成该语言的 Quiz 题

    Returns: generate_quiz() 的返回字典
    """
    current_lang = _advance_rotation(json_path=json_path)
    target_lang = language or current_lang
    return generate_quiz(language=target_lang, difficulty=difficulty)


def format_quiz_console(quiz: Dict[str, Any]) -> str:
    """
    将 Quiz 对象格式化为控制台展示文本。
    """
    emoji = quiz.get("emoji", "\U0001f4e6")
    code = quiz.get("code", "")
    hint = quiz.get("hint", "")
    options = quiz.get("options", [])

    code_lines = code.split("\n")
    max_len = max(len(line) for line in code_lines) if code_lines else 0
    width = max(max_len + 4, 50)

    header = "  " + "\u250c" + "\u2500" * (width - 2) + "\u2510"
    footer = "  " + "\u2514" + "\u2500" * (width - 2) + "\u2518"

    code_block = [header]
    for line in code_lines:
        code_block.append("  " + "\u2502" + " " + line.ljust(width - 4) + " " + "\u2502")
    code_block.append(footer)

    option_labels = ["  [" + chr(65 + i) + "] " + opt["label"] for i, opt in enumerate(options)]

    parts = [
        "  " + "\u2554" + "\u2550" * 48 + "\u2557",
        "  " + "\u2551" + "  " + emoji + "  Polyglot Quiz \u2014 \u731c\u731c\u8fd9\u662f\u4ec0\u4e48\u8bed\u8a00\uff1f               " + "\u2551",
        "  " + "\u2560" + "\u2550" * 48 + "\u2563",
        "  " + "\u2551" + "  \U0001f4a1  " + hint + (" " * max(0, 40 - len(hint))) + "\u2551",
        "  " + "\u2560" + "\u2550" * 48 + "\u2563",
        "  " + "\u2551" + "  \U0001f4bb \u4ee3\u7801\u7247\u6bb5\uff1a                                           " + "\u2551",
    ]
    parts.extend(code_block)
    parts.append("  " + "\u2560" + "\u2550" * 48 + "\u2563")
    parts.append("  " + "\u2551" + "  \U0001f4c4 \u8bf7\u9009\u62e9\u6b63\u786e\u7b54\u6848\uff1a                                   " + "\u2551")
    for opt in option_labels:
        parts.append("  " + "\u2551" + "    " + opt.ljust(46) + "\u2551")
    parts.append("  " + "\u255a" + "\u2550" * 48 + "\u255d")
    return "\n".join(parts)


def format_quiz_markdown(quiz: Dict[str, Any]) -> str:
    """
    将 Quiz 对象格式化为 Markdown 展示文本。
    """
    emoji = quiz.get("emoji", "\U0001f4e6")
    code = quiz.get("code", "")
    hint = quiz.get("hint", "")
    options = quiz.get("options", [])

    parts = [
        "## " + emoji + " Polyglot Quiz",
        "",
        "**\U0001f4a1 \u63d0\u793a：** " + hint,
        "",
        "**\U0001f4bb \u4ee3\u7801\u7247\u65ad：**",
        "```",
        code,
        "```",
        "",
        "**\U0001f4c4 \u9009\u9879：**",
    ]
    for i, opt in enumerate(options):
        parts.append("  - [" + chr(65 + i) + "] " + opt["label"])
    parts.append("")
    return "\n".join(parts)


def format_stats_console(stats: Dict[str, Any]) -> str:
    """
    将 Quiz 统计数据格式化为控制台展示文本。
    """
    total = stats.get("total_attempts", 0)
    correct = stats.get("correct_count", 0)
    accuracy = stats.get("accuracy", 0.0)
    by_lang = stats.get("by_language", {})

    lines = [
        "  " + "\u2554" + "\u2550" * 40 + "\u2557",
        "  " + "\u2551" + "  \U0001f4ca Polyglot Quiz \u7edf\u8ba1                 " + "\u2551",
        "  " + "\u2560" + "\u2550" * 40 + "\u2563",
        "  " + "\u2551" + "  \u603b\u7b54\u9898\u6b21\u6570\uff1a" + str(total) + (" " * max(0, 20 - len(str(total)))) + "\u2551",
        "  " + "\u2551" + "  \u6b63\u786e\u6b21\u6570\uff1a  " + str(correct) + (" " * max(0, 20 - len(str(correct)))) + "\u2551",
        "  " + "\u2551" + "  \u6b63\u786e\u7387\uff1a    " + str(accuracy) + "%" + (" " * max(0, 15 - len(str(accuracy)))) + "\u2551",
        "  " + "\u2560" + "\u2550" * 40 + "\u2563",
        "  " + "\u2551" + "  \U0001f4cb \u5404\u8bed\u8a00\u51c0\u786e\u7387\uff1a                    " + "\u2551",
    ]

    if by_lang:
        for lang, s in sorted(by_lang.items(), key=lambda x: -x[1]["accuracy"]):
            meta = LANGUAGE_METADATA.get(lang, {})
            em = meta.get("emoji", "\U0001f4e6")
            acc = s["accuracy"]
            bar = "\u2588" * int(acc / 10) + "\u2591" * (10 - int(acc / 10))
            lines.append("  " + "\u2551" + "  " + em + " " + lang.ljust(10) + " " + bar + " " + str(acc).rjust(5) + "%  " + "\u2551")
    else:
        lines.append("  " + "\u2551" + "  \u6682\u65e0\u6570\u636e                           " + "\u2551")

    lines.append("  " + "\u255a" + "\u2550" * 40 + "\u255d")
    return "\n".join(lines)


# ─────────────────────────────────────────────
# CLI 入口
# ─────────────────────────────────────────────

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Polyglot Quiz \u2014 \u7f16\u7a0b\u8bed\u8a00\u731c\u8c1c")
    sub = parser.add_subparsers(dest="cmd")

    sub.add_parser("quiz", help="\u751f\u6210\u4e00\u9053 Quiz \u9898\uff08\u63a8\u8fdb\u8f6e\u6362\uff09")
    sub.add_parser("stats", help="\u67e5\u770b Quiz \u7edf\u8ba1")
    sub.add_parser("answer", help="\u68c0\u67e5\u7b54\u6848").add_argument("language")
    sub.add_parser("format", help="\u683c\u5f0f\u5316\u5f53\u524d Quiz\uff08\u9700\u914d\u5408 quiz \u547d\u4ee4\uff09")

    args = parser.parse_args()

    if args.cmd == "quiz":
        quiz = rotate_and_get_quiz()
        print(format_quiz_console(quiz))
    elif args.cmd == "stats":
        stats = get_quiz_stats()
        print(format_stats_console(stats))
    elif args.cmd == "answer":
        print("\u8bf7\u5148\u8fd0\u884c `python -m modules.polyglot_quiz quiz` \u83b7\u53d6\u9898\u76ee\uff0c\u518d\u7528 answer \u547d\u4ee4\u7b54\u9898")
    elif args.cmd == "format":
        print("\u8bf7\u5148\u8fd0\u884c quiz \u547d\u4ee4\u83b7\u53d6\u9898\u76ee")
    else:
        parser.print_help()
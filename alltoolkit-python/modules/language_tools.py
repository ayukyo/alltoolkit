"""
语言轮换工具模块 (Language Router / Polyglot Dispatcher)
从 language_rotation.json 读取语言列表，按顺序轮换选择语言，
并为当前语言生成特定的能力概览和使用指导。

语言轮换顺序：Rust → Go → Swift → Kotlin → TypeScript → JavaScript → Java → C/C++ → Rust（循环）
"""

import json
import os
from typing import Optional, Dict, List, Any
from pathlib import Path
from datetime import datetime, timedelta, timezone


# 各语言的能力画像（personas）
LANGUAGE_PERSONAS: Dict[str, Dict[str, Any]] = {
    "Rust": {
        "emoji": "🦀",
        "tagline": "内存安全 · 零成本抽象 · 无畏并发",
        "strengths": [
            "系统编程 / 嵌入式 / WASM",
            "高性能网络服务",
            "命令行工具 (CLI)",
            "内存安全（无 GC）",
            "优秀的编译时检查",
        ],
        "typical_projects": ["游戏引擎", "操作系统组件", "WebAssembly模块", "网络工具", "加密货币"],
        "key_concepts": ["所有权 (Ownership)", "借用 (Borrowing)", "生命周期 (Lifetimes)", "trait", "Result"],
        "code_example": 'fn main() { println!("Hello, Rust!"); }',
        "resources": {
            "docs": "https://doc.rust-lang.org/",
            "crates_io": "https://crates.io/",
            "playground": "https://play.rust-lang.org/",
        },
        "quirks": [
            "所有权规则需要适应",
            "编译时间较长",
            "错误处理用 Result 而不是异常",
        ],
    },
    "Go": {
        "emoji": "🐹",
        "tagline": "简洁并发 · 轻量goroutine · 部署友好",
        "strengths": [
            "云原生 / 微服务",
            "网络编程 / API服务",
            "DevOps 工具 (Docker/K8s)",
            "快速编译 · 快速部署",
            "出色的并发模型",
        ],
        "typical_projects": ["REST/gRPC API", "Docker/Kubernetes插件", "CLI工具", "数据管道", "网关服务"],
        "key_concepts": ["goroutine", "channel", "defer", "interface", "context"],
        "code_example": 'package main\n\nimport "fmt"\n\nfunc main() { fmt.Println("Hello, Go!") }',
        "resources": {
            "docs": "https://go.dev/doc/",
            "pkg": "https://pkg.go.dev/",
            "playground": "https://go.dev/play/",
        },
        "quirks": [
            "错误处理需要显式处理每个错误",
            "没有泛型（旧版）/ 泛型支持有限",
            "GC 延迟敏感场景需谨慎",
        ],
    },
    "Swift": {
        "emoji": "🦅",
        "tagline": "苹果生态 · 安全高效 · 现代语法",
        "strengths": [
            "iOS/macOS 应用开发",
            "服务器端 Swift",
            "安全性高 · 无空指针",
            "快速性能",
            "playground 交互式开发",
        ],
        "typical_projects": ["iOS App", "macOS App", "Server-side API", "SwiftUI 界面", "脚本工具"],
        "key_concepts": ["optional", "protocol", "struct vs class", "closure", "@State/@Observable"],
        "code_example": 'print("Hello, Swift!")',
        "resources": {
            "docs": "https://docs.swift.org/",
            "apple_dev": "https://developer.apple.com/",
            "playground": "https://swift.org/play/",
        },
        "quirks": [
            "可选类型 (Optional) 处理",
            "ABI 稳定性历史问题",
            "苹果平台强绑定（Linux支持在改善）",
        ],
    },
    "Kotlin": {
        "emoji": "🧃",
        "tagline": "JVM 现代化 · 空安全 · 协程异步",
        "strengths": [
            "Android 开发首选",
            "JVM 生态无缝接入",
            "协程 · 轻量级并发",
            "空安全 (Null Safety)",
            "与 Java 100% 互操作",
        ],
        "typical_projects": ["Android App", "Spring Boot 服务", "Gradle 脚本", "数据处理", "桌面应用"],
        "key_concepts": ["nullable types", "data class", "coroutine", "extension function", "sealed class"],
        "code_example": 'fun main() = println("Hello, Kotlin!")',
        "resources": {
            "docs": "https://kotlinlang.org/docs/home.html",
            "koans": "https://kotlinlang.org/docs/koans.html",
            "playground": "https://play.kotlinlang.org/",
        },
        "quirks": [
            "编译速度比 Java 慢",
            "伤仲永（Google曾力推但Android凉了？）",
            "Kotlin Multiplatform 还在成熟中",
        ],
    },
    "TypeScript": {
        "emoji": "🔷",
        "tagline": "JS的超集 · 类型安全 · 渐进式类型",
        "strengths": [
            "前端/后端/全栈开发",
            "类型安全 + 运行时灵活",
            "VS Code 原生支持",
            "NPM 生态最丰富",
            "渐进式迁移",
        ],
        "typical_projects": ["Web App", "Node.js API", "React/Vue/Angular", "CLI工具", "类型定义库"],
        "key_concepts": ["interface vs type", "generic", "utility types", "decorator", "module augmentation"],
        "code_example": 'console.log("Hello, TypeScript!");',
        "resources": {
            "docs": "https://www.typescriptlang.org/docs/",
            "handbook": "https://www.typescriptlang.org/docs/handbook/",
            "playground": "https://www.typescriptlang.org/play/",
        },
        "quirks": [
            "any 类型绕过类型检查",
            "编译配置复杂",
            "鸭子类型导致隐式类型错误",
        ],
    },
    "JavaScript": {
        "emoji": "🟨",
        "tagline": "Web唯一语言 · 异步事件 · 亿级生态",
        "strengths": [
            "浏览器唯一原生语言",
            "前端交互核心",
            "Node.js 后端",
            "NPM 生态最大",
            "事件循环模型",
        ],
        "typical_projects": ["Web交互逻辑", "Express/Koa API", "Electron桌面应用", "Webpack插件", "自动化脚本"],
        "key_concepts": ["prototype", "closure", "event loop", "promise/async-await", "this binding"],
        "code_example": 'console.log("Hello, JavaScript!");',
        "resources": {
            "mdn": "https://developer.mozilla.org/",
            "node_docs": "https://nodejs.org/",
            "npm": "https://www.npmjs.com/",
        },
        "quirks": [
            "类型强制转换陷阱",
            "this 指向问题",
            "callback hell（虽可用 async/await 缓解）",
        ],
    },
    "Java": {
        "emoji": "☕",
        "tagline": "企业级稳健 · JVM生态 · 一次编译",
        "strengths": [
            "企业级后端服务",
            "Android（Kotlin替代中）",
            "Spring 生态",
            "JVM 调优成熟",
            "泛型 · 反射 · 注解",
        ],
        "typical_projects": ["Spring Boot API", "Android App", "大数据处理", "企业ERP", "金融系统"],
        "key_concepts": ["JVM", "GC调优", "泛型", "多线程 / ExecutorService", "stream / lambda"],
        "code_example": 'public class Main { public static void main(String[] args) { System.out.println("Hello, Java!"); } }',
        "resources": {
            "docs": "https://docs.oracle.com/en/java/",
            "spring": "https://spring.io/projects/spring-boot",
            "mavencentral": "https://search.maven.org/",
        },
        "quirks": [
            "啰嗦的语法（模板代码多）",
            "GC 暂停 (stop-the-world)",
            "更新换代慢（大版本发布周期长）",
        ],
    },
    "C/C++": {
        "emoji": "⚙️",
        "tagline": "系统级控制 · 极致性能 · 底层硬件",
        "strengths": [
            "操作系统 / 驱动开发",
            "游戏引擎核心",
            "嵌入式/实时系统",
            "极致性能控制",
            "几乎无运行时开销",
        ],
        "typical_projects": ["OS内核", "数据库引擎", "游戏引擎", "GUI框架", "编译器"],
        "key_concepts": ["指针/引用", "手动内存管理", "模板元编程", "RAII", "虚函数/多态"],
        "code_example": '#include <stdio.h>\nint main() { printf("Hello, C!\\n"); return 0; }',
        "resources": {
            "c_docs": "https://en.cppreference.com/",
            "cpp_guides": "https://isocpp.org/get-started",
            "cppreference": "https://en.cppreference.com/w/",
        },
        "quirks": [
            "手动内存管理（悬挂指针/缓冲区溢出）",
            "未定义行为多",
            "编译宏预处理复杂",
        ],
    },
}


def _get_rotation_file_path() -> str:
    """获取语言轮换配置文件的路径"""
    # 优先使用 workspace 下的文件
    workspace_path = Path("/home/admin/.openclaw/workspace/language_rotation.json")
    if workspace_path.exists():
        return str(workspace_path)
    # 回退到 alltoolkit-python 目录
    alt_path = Path(__file__).parent.parent / "language_rotation.json"
    if alt_path.exists():
        return str(alt_path)
    return str(workspace_path)


def load_rotation_config(path: Optional[str] = None) -> Dict[str, Any]:
    """
    加载语言轮换配置

    Args:
        path: 配置文件路径，None 则自动查找

    Returns:
        包含 languages 列表、current_index、last_language、updated_at 的字典
    """
    if path is None:
        path = _get_rotation_file_path()
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_rotation_config(config: Dict[str, Any], path: Optional[str] = None) -> None:
    """
    保存语言轮换配置

    Args:
        config: 配置字典
        path: 配置文件路径，None 则自动查找
    """
    if path is None:
        path = _get_rotation_file_path()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)


def rotate_language(config: Optional[Dict[str, Any]] = None,
                    path: Optional[str] = None,
                    force_language: Optional[str] = None) -> Dict[str, Any]:
    """
    轮换到下一个语言，并更新配置文件的 current_index

    Args:
        config: 配置字典，None 则从文件加载
        path: 配置文件路径
        force_language: 强制指定本次选择的语言（如 "Rust"），
                       忽略 current_index。常用于 cron 强制选特定语言。

    Returns:
        轮换结果字典：
        {
            "current_language": "Rust",
            "current_index": 0,
            "next_language": "Go",
            "next_index": 1,
            "persona": { ... },  # 当前语言画像
            "rotation_sequence": [ ... ],  # 本轮完整语言序列
        }
    """
    if config is None:
        config = load_rotation_config(path)

    languages = config["languages"]
    current_index = config.get("current_index", 0)
    n = len(languages)

    # 取当前语言（或强制指定）
    if force_language:
        if force_language not in languages:
            raise ValueError(f"Unknown language: {force_language}. Available: {languages}")
        current_language = force_language
        current_index = languages.index(force_language)
    else:
        current_language = languages[current_index]

    # 计算下一个
    next_index = (current_index + 1) % n
    next_language = languages[next_index]

    # 更新配置：移动到下一个（下次轮到这个语言）
    updated_config = dict(config)
    updated_config["current_index"] = next_index
    updated_config["last_language"] = current_language
    updated_config["updated_at"] = datetime.now(timezone(timedelta(hours=8))).isoformat()

    # 保存
    save_rotation_config(updated_config, path)

    # 构造返回结果
    result = {
        "current_language": current_language,
        "current_index": current_index,
        "next_language": next_language,
        "next_index": next_index,
        "rotation_sequence": languages,  # 本轮语言顺序
        "updated_config": updated_config,
    }

    return result


def get_language_persona(language: str) -> Optional[Dict[str, Any]]:
    """
    获取指定语言的能力画像

    Args:
        language: 语言名称

    Returns:
        语言画像字典（包含 emoji、tagline、strengths 等）
    """
    return LANGUAGE_PERSONAS.get(language)


def get_current_persona(config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    获取当前语言（按轮换配置）的画像

    Args:
        config: 配置字典，None 则从文件加载

    Returns:
        当前语言的完整画像字典
    """
    if config is None:
        config = load_rotation_config()
    languages = config["languages"]
    idx = config.get("current_index", 0)
    current_lang = languages[idx]
    persona = get_language_persona(current_lang)
    return {
        "language": current_lang,
        "index": idx,
        "persona": persona or {},
    }


def suggest_language_for_project(project_type: str) -> List[Dict[str, Any]]:
    """
    根据项目类型推荐语言

    Args:
        project_type: 项目类型关键词（如 "web"、"cli"、"mobile"）

    Returns:
        推荐语言列表（按匹配度排序），每个元素含 language、persona、match_score
    """
    project_keywords: Dict[str, List[str]] = {
        "web": ["TypeScript", "JavaScript"],
        "frontend": ["TypeScript", "JavaScript"],
        "backend": ["Go", "Java", "TypeScript", "Rust"],
        "api": ["Go", "TypeScript", "Java", "Rust"],
        "cli": ["Rust", "Go", "Swift"],
        "mobile": ["Swift", "Kotlin", "Java"],
        "ios": ["Swift"],
        "android": ["Kotlin", "Java"],
        "embedded": ["Rust", "C/C++"],
        "system": ["Rust", "C/C++"],
        "wasm": ["Rust", "TypeScript"],
        "game": ["C/C++", "Rust"],
        "database": ["Rust", "C/C++", "Go"],
        "devops": ["Go", "Python"],
        "data": ["Python", "Java", "Kotlin"],
        "script": ["Python", "JavaScript"],
    }

    project_type_lower = project_type.lower()
    matched_langs: List[str] = []

    for key, langs in project_keywords.items():
        if key in project_type_lower:
            for lang in langs:
                if lang not in matched_langs:
                    matched_langs.append(lang)

    results = []
    for lang in matched_langs:
        persona = get_language_persona(lang)
        if persona:
            results.append({
                "language": lang,
                "persona": persona,
                "match_score": len([l for l in matched_langs if l == lang]),
            })
    # 按匹配度排序
    results.sort(key=lambda x: x["match_score"], reverse=True)
    return results


def get_rotation_summary() -> str:
    """
    获取轮换概览表格（适合打印/展示）

    Returns:
        多行字符串，包含轮换顺序表格
    """
    try:
        config = load_rotation_config()
    except FileNotFoundError:
        return "language_rotation.json 未找到"

    languages = config["languages"]
    current_idx = config.get("current_index", 0)
    current_lang = languages[current_idx]

    lines = ["=" * 50, "🔄 语言轮换概览", "=" * 50, ""]

    for i, lang in enumerate(languages):
        persona = get_language_persona(lang)
        emoji = persona.get("emoji", "📄") if persona else "📄"
        marker = " ▶ " if i == current_idx else "   "
        next_marker = " ← next" if i == (current_idx + 1) % len(languages) else ""
        lines.append(f"{marker}{emoji} {lang}{next_marker}")

    lines.append("")
    lines.append(f"当前语言：{current_lang}")
    lines.append(f"当前索引：{current_idx} / {len(languages) - 1}")
    lines.append(f"下次语言：{languages[(current_idx + 1) % len(languages)]}")
    lines.append("=" * 50)
    return "\n".join(lines)

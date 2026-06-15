"""
polyglot_cartographer.py — 编程语言代码地理测绘仪 (Polyglot Cartographer)
============================================================================
每次轮换语言时，生成该语言的"代码地理地图"——
将语言的生态系统、项目结构、依赖关系、命名Convention
以 ASCII 艺术地图的形式呈现，让你对该语言的项目组织方式
建立一个直观的空间感。

核心创意：每种语言的代码库都有自己的「地貌」——
  Rust 的模块树深沉而扁平、Go 的 GOPATH 清晰明了、
  JavaScript 的 node_modules 像热带雨林、Kotlin 的包结构层次分明……
  本工具用 ASCII 拓扑图、命名Convention光谱、依赖关系图，
  让你"身临其境"地理解每种语言的代码组织哲学。

Distinct from existing tools:
  - language_tools:         轮换 + 徽章 + 连击记录
  - polyglot_codex:        每日语言韬略（生态 + 职业 + 趋势）
  - polyglot_companion:    语言学习伴侣（特性 + 练习 + Pomodoro）
  - polyglot_quiz:         代码模式猜谜（4选1）
  - polyglot_resonator:    语言频率波形图（共振分析）
  - polyglot_ink:          每日墨讯（谚语 + 能量 + 趣闻）
  - polyglot_snippet_vault: 代码片段库（按类别检索）
  - polyglot_paradigm_weaver: 跨语言范式对照（8语言×8范式）
  - kata_generator:        代码道场 kata
  - dev_metrics:           代码复杂度分析
  - compile_cache:         编译缓存行为模拟

Polyglot Cartographer 的独特视角：
  不是教你写代码，而是让你理解每种语言的"城市布局"——
  项目从哪里进去、主要建筑在哪里、依赖如何连接。
  当你对一种语言有了地理感，写代码时就知道"该往哪走"。

语言轮换顺序（8 种核心语言）：
  Rust → Go → Swift → Kotlin → TypeScript → JavaScript → Java → C/C++ → Rust（循环）

作者：AllToolkit 全自动生成
依赖：仅 Python 标准库（json, random, datetime, pathlib）
============================================================================
"""

import json
import os
import random
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# ── 路径配置 ─────────────────────────────────────────────────────────────────
_MODULE_DIR = Path(__file__).parent.parent
_WORKSPACE_ROOT = _MODULE_DIR.parent
DEFAULT_LANGUAGE_ROTATION_JSON = str(_WORKSPACE_ROOT / "language_rotation.json")


# ══════════════════════════════════════════════════════════════════════════════
# 语言代码地理数据库
# ══════════════════════════════════════════════════════════════════════════════
# 每种语言包含：
#   ecosystem_map     : ASCII 生态系统拓扑图（模块/包/目录结构）
#   entry_point       : 入口文件/函数标注
#   naming_conventions: 命名惯例光谱（文件/函数/变量/类型）
#   dependency_style  : 依赖管理方式（ASCII 流程图）
#   project_sketch    : 典型项目目录草图
#   key_locations     : 语言特有的"必去之地"标注
#   trivia            : 代码地理趣闻

CARTOGRAPHER_DB: Dict[str, Dict[str, Any]] = {
    "Rust": {
        "emoji": "🦀",
        "ecosystem_map": """
                    ┌─────────────────────┐
                    │    Cargo.toml       │ ← 项目元数据 + 依赖
                    └──────────┬──────────┘
                               │
              ┌────────────────┼────────────────┐
              ▼                ▼                ▼
        ┌──────────┐    ┌──────────┐    ┌──────────┐
        │  src/    │    │  src/    │    │ tests/   │
        │ lib.rs   │    │ main.rs  │    │ integration│
        │ (库入口) │    │ (二进制) │    │ tests    │
        └────┬─────┘    └────┬─────┘    └──────────┘
             │                │
             ▼                ▼
       ┌───────────┐  ┌─────────────────┐
       │ modules/  │  │  src/bin/*.rs   │
       │ (子模块)  │  │  (多二进制)      │
       └───────────┘  └─────────────────┘
        """,
        "entry_point": "src/main.rs → fn main() / src/lib.rs → pub mod",
        "naming_conventions": {
            "file": "kebab-case:  my_module.rs, utils_helper.rs",
            "function": "snake_case:  fn calculate_total()",
            "variable": "snake_case:  let max_buffer_size = 1024",
            "type": "PascalCase:  struct ConfigManager",
            "constant": "SCREAMING_SNAKE:  const MAX_RETRIES: u32",
            "macro": "snake_case!:  macro_rules! my_macro",
        },
        "dependency_style": """
  ┌──────────────┐     cargo build      ┌──────────────┐
  │  Cargo.toml  │ ──────────────────▶  │  crates.io   │
  │  [deps]     │      在线解析          │ ( crates )  │
  └──────────────┘                       └──────────────┘
        """,
        "project_sketch": [
            "my_project/",
            "├── Cargo.toml        ← 清单（项目名、依赖、特性标志）",
            "├── Cargo.lock        ← 精确版本锁定（提交到 VCS）",
            "├── src/",
            "│   ├── lib.rs        ← 库入口，pub mod 暴露模块",
            "│   ├── main.rs        ← 二进制入口，fn main()",
            "│   └── bin/           ← 多个二进制目标",
            "├── tests/",
            "│   └── integration_tests/",
            "├── benches/          ← 性能基准测试",
            "└── examples/         ← 用法示例",
        ],
        "key_locations": [
            ("Cargo.toml", "项目配置心脏：依赖声明、特性标志、元数据"),
            ("src/lib.rs", "库的公共 API 边界：pub mod / pub use"),
            ("src/main.rs", "程序入口：fn main() 是旅程起点"),
            ("target/debug/", "编译产物迷宫：第一次 cargo build 后出现"),
            ("tests/", "集成测试区：文件即测试，cargo test 自动发现"),
        ],
        "trivia": (
            "Rust 的模块系统从文件系统的物理布局到模块树的逻辑布局，"
            "必须通过 mod xxx; 显式声明——编译器不会自动引入文件，"
            "所以'文件存在但编译报错找不到模块'是新手必经之路。"
        ),
    },
    "Go": {
        "emoji": "🐹",
        "ecosystem_map": """
                    ┌─────────────────────┐
                    │      go.mod         │ ← 模块定义（1.11+）
                    └──────────┬──────────┘
                               │
              ┌────────────────┼────────────────┐
              ▼                ▼                ▼
        ┌──────────┐    ┌──────────┐    ┌──────────┐
        │ internal/│    │   cmd/   │    │  pkg/    │
        │ (内部包)  │    │ (可执行) │    │ (公共库) │
        └────┬─────┘    └────┬─────┘    └──────────┘
             │                │
             ▼                ▼
       ┌───────────┐  ┌─────────────┐
       │ domain/   │  │  main.go    │
       │ (领域层)  │  │ (入口文件)   │
       └───────────┘  └─────────────┘
        """,
        "entry_point": "cmd/myapp/main.go → package main → func main()",
        "naming_conventions": {
            "file": "lowercase:  user_service.go, http_helper.go",
            "function": "PascalCase:  func GetUserByID(id int) (*User, error)",
            "variable": "camelCase:  maxRetries := 3",
            "type": "PascalCase:  type ConfigManager struct { ... }",
            "constant": "PascalCase:  const MaxBufferSize = 1024",
            "interface": "PascalCase + er:  Reader, Writer, Closer",
        },
        "dependency_style": """
  ┌──────────────┐    go get / go mod tidy   ┌──────────────┐
  │   go.mod     │ ──────────────────────▶  │ proxy.golang │
  │  go.sum     │      依赖解析 + 校验        │   org        │
  └──────────────┘                           └──────────────┘
        """,
        "project_sketch": [
            "my_project/",
            "├── go.mod              ← 模块定义（路径 + Go 版本）",
            "├── go.sum              ← 依赖精确校验（提交到 VCS）",
            "├── cmd/",
            "│   └── myapp/",
            "│       └── main.go     ← 应用入口",
            "├── internal/",
            "│   ├── domain/         ← 领域实体和业务规则",
            "│   ├── repository/     ← 数据持久化",
            "│   └── service/        ← 应用服务层",
            "├── pkg/                ← 可对外发布的工具库",
            "├── api/                ← 协议定义（protobuf/openapi）",
            "└── Makefile           ← 构建自动化",
        ],
        "key_locations": [
            ("go.mod", "模块边界：module path 决定 import 路径前缀"),
            ("cmd/", "应用入口集合：每个子目录是一个可执行程序"),
            ("internal/", "私有包禁区：只能被父模块导入，外部无法访问"),
            ("pkg/", "公共库区：可被外部项目 import 的工具集"),
            ("GOPATH/bin/", "编译产物：go install 后可执行文件去哪里"),
        ],
        "trivia": (
            "Go 1.11 引入 modules 之前的 GOPATH 时代，"
            "所有项目必须放在 $GOPATH/src/ 下——"
            "一个强制性的'所有人住同一个小区'时代。"
            "现在 go.mod 让项目彻底自由，但'包路径即身份证号'的哲学从未改变。"
        ),
    },
    "Swift": {
        "emoji": "🦅",
        "ecosystem_map": """
                    ┌─────────────────────┐
                    │   Package.swift     │ ← SPM 清单
                    └──────────┬──────────┘
                               │
              ┌────────────────┼────────────────┐
              ▼                ▼                ▼
        ┌──────────┐    ┌──────────┐    ┌──────────┐
        │ Sources/ │    │  Tests/  │    │  Xcode   │
        │ (源码)    │    │ (测试)    │    │ .xcodeproj│
        └────┬─────┘    └──────────┘    └──────────┘
             │
             ▼
       ┌───────────┐  ┌──────────────────┐
       │ MyMod/    │  │  MyApp/          │
       │ (模块)    │  │  (应用目标)       │
       └───────────┘  └──────────────────┘
        """,
        "entry_point": "@main / AppDelegate.swift → UIApplicationMain / App 入口",
        "naming_conventions": {
            "file": "PascalCase:  UserService.swift, ConfigManager.swift",
            "function": "PascalCase:  func fetchUser(id: Int) -> User?",
            "variable": "camelCase:  var maxRetryCount = 3",
            "type": "PascalCase:  struct User, class AuthManager",
            "protocol": "PascalCase + Protocol:  Runnable, DataConvertible",
            "constant": "PascalCase:  let maxConnectionCount = 100",
        },
        "dependency_style": """
  ┌──────────────┐   swift package resolve   ┌──────────────┐
  │ Package.swift│ ──────────────────────▶  │ Swift Package│
  │              │      SPM 依赖解析         │   Registry   │
  └──────────────┘                           └──────────────┘

  ┌──────────────┐      pod install         ┌──────────────┐
  │ Podfile      │ ──────────────────────▶  │  CocoaPods   │
  └──────────────┘      CocoaPods 依赖      │  Specs Repo  │
                                             └──────────────┘
        """,
        "project_sketch": [
            "MyApp/",
            "├── MyApp/",
            "│   ├── AppDelegate.swift  ← iOS 应用生命周期入口",
            "│   ├── SceneDelegate.swift ← 多场景支持（iOS 13+）",
            "│   ├── Models/            ← 数据模型",
            "│   ├── Views/             ← SwiftUI Views / UIKit VCs",
            "│   ├── ViewModels/        ← 状态管理",
            "│   ├── Services/          ← 网络、存储等公共服务",
            "│   └── Resources/         ← Assets.xcassets, 本地化",
            "├── project.yml           ← XcodeGen 生成配置",
            "├── Podfile               ← CocoaPods 依赖（可选）",
            "└── Package.swift         ← Swift PM 依赖（可选）",
        ],
        "key_locations": [
            ("AppDelegate.swift", "iOS 应用生命周期的心脏：didFinishLaunching 起点"),
            ("SceneDelegate.swift", "多窗口应用支持：UIWindow 的诞生地"),
            ("Sources/", "Swift PM 项目源码根目录"),
            ("Assets.xcassets", "图片、颜色、App Icon 的资源仓库"),
            ("Info.plist", "应用的元数据配置文件：Bundle ID、权限、URL Schemes"),
        ],
        "trivia": (
            "Swift 5.3 之前，iOS 项目依赖管理有 CocoaPods 和 Carthage 两大流派，"
            "Swift Package Manager（SPM）长期不支持 iOS 目标。"
            "现在 SPM 已一统 Apple 平台，但 CocoaPods 生态仍有数十万存量依赖。"
        ),
    },
    "Kotlin": {
        "emoji": "🟣",
        "ecosystem_map": """
                    ┌─────────────────────┐
                    │  build.gradle.kts   │ ← 项目构建配置
                    │  settings.gradle.kts │ ← 模块定义
                    └──────────┬──────────┘
                               │
              ┌────────────────┼────────────────┐
              ▼                ▼                ▼
        ┌──────────┐    ┌──────────┐    ┌──────────┐
        │  src/    │    │  src/    │    │  build/  │
        │ main/kotlin│  │ test/    │    │ (编译产物)│
        └────┬─────┘    └──────────┘    └──────────┘
             │
             ▼
       ┌─────────────────────────────────────┐
       │ com.example.myapp/                  │
       │   ├── domain/    ← 领域模型          │
       │   ├── data/     ← 数据层实现        │
       │   ├── repository/ ← 仓储抽象         │
       │   └── presentation/ ← UI 层          │
       └─────────────────────────────────────┘
        """,
        "entry_point": "fun main(args: Array<String>) / class MyApp",
        "naming_conventions": {
            "file": "PascalCase:  UserService.kt, HttpClient.kt",
            "function": "camelCase:  fun fetchUser(id: Int): User?",
            "variable": "camelCase:  val maxRetries = 3",
            "type": "PascalCase:  data class UserProfile",
            "package": "lowercase dot:  com.example.myapp",
            "constant": "SCREAMING_SNAKE in companion:  companion object { const val MAX_SIZE = 100 }",
        },
        "dependency_style": """
  ┌──────────────┐   gradle build / resolve   ┌──────────────┐
  │ build.gradle │ ────────────────────────▶  │  Maven       │
  │ (Kotlin DSL) │      依赖解析              │  Central     │
  └──────────────┘                           └──────────────┘

  ┌──────────────┐   Gradle Kotlin DSL       ┌──────────────┐
  │ settings.gradle.kts │ ──────────────▶  │ Kotlin       │
  │                      │   插件解析        │   Evolutions │
  └──────────────┘                           └──────────────┘
        """,
        "project_sketch": [
            "my-app/",
            "├── build.gradle.kts      ← 根项目构建脚本",
            "├── settings.gradle.kts   ← 模块树定义",
            "├── gradle.properties     ← Gradle 配置属性",
            "├── app/",
            "│   ├── build.gradle.kts  ← App 模块构建脚本",
            "│   └── src/",
            "│       ├── main/kotlin/com/example/app/",
            "│       │   ├── MainActivity.kt ← Android 入口",
            "│       │   ├── domain/          ← 领域模型",
            "│       │   ├── data/            ← 数据层",
            "│       │   └── presentation/    ← UI 层",
            "│       └── test/",
            "└── kotlin/"
        ],
        "key_locations": [
            ("build.gradle.kts", "Gradle Kotlin DSL：项目依赖和插件在此声明"),
            ("src/main/kotlin/", "Kotlin 源码根目录，按包路径组织子目录"),
            ("domain/", "领域模型层：纯业务逻辑，无任何框架依赖"),
            ("build/", "Gradle 编译产物目录：.class、APK 都藏在这里"),
            ("gradle.properties", "Gradle 全局配置：org.gradle.jvmargs 等"),
        ],
        "trivia": (
            "Kotlin 的包名声明（package com.example.app）与目录结构（src/.../）"
            "不必强制一致——这是与 Java 的最大区别之一，"
            "允许你在同一目录放多个包的类，打破 Java 的'一个文件一个类'限制。"
        ),
    },
    "TypeScript": {
        "emoji": "🔷",
        "ecosystem_map": """
                    ┌─────────────────────┐
                    │     tsconfig.json    │ ← TypeScript 配置
                    └──────────┬──────────┘
                               │
              ┌────────────────┼────────────────┐
              ▼                ▼                ▼
        ┌──────────┐    ┌──────────┐    ┌──────────┐
        │  src/    │    │  dist/   │    │  node_   │
        │ (源码)   │    │ (编译输出)│    │ modules/ │
        └────┬─────┘    └──────────┘    └──────────┘
             │
             ▼
       ┌───────────┐  ┌─────────────────┐
       │ modules/  │  │  types/          │
       │ (子模块)  │  │ (类型定义)       │
       └───────────┘  └─────────────────┘
        """,
        "entry_point": "src/index.ts → 编译后 → dist/index.js",
        "naming_conventions": {
            "file": "camelCase / kebab-case:  userService.ts, my-util.ts",
            "function": "camelCase:  function fetchUser(id: number): User",
            "variable": "camelCase:  let maxRetries = 3",
            "type": "PascalCase:  type UserProfile = { name: string }",
            "interface": "PascalCase + I prefix (legacy):  IUserProps",
            "constant": "PascalCase:  const MaxBufferSize = 1024",
        },
        "dependency_style": """
  ┌──────────────┐    npm install / yarn add   ┌──────────────┐
  │ package.json │ ────────────────────────▶  │   npm        │
  │              │     依赖安装                 │   registry   │
  └──────────────┘                              └──────────────┘

  ┌──────────────┐    npx tsc / vite build    ┌──────────────┐
  │ tsconfig.json│ ────────────────────────▶  │  JavaScript  │
  │              │     类型检查 + 转译          │  output      │
  └──────────────┘                              └──────────────┘
        """,
        "project_sketch": [
            "my-ts-app/",
            "├── tsconfig.json        ← TypeScript 编译配置",
            "├── package.json         ← 项目元数据 + npm scripts",
            "├── node_modules/        ← 依赖森林（.gitignore 排除）",
            "├── src/",
            "│   ├── index.ts         ← 应用入口",
            "│   ├── api/             ← API 调用层",
            "│   ├── components/       ← UI 组件",
            "│   ├── hooks/           ← 自定义 React hooks",
            "│   ├── types/           ← 全局类型定义",
            "│   └── utils/           ← 工具函数",
            "├── dist/                ← 编译产物（可部署）",
            "└── vite.config.ts      ← Vite 构建配置（可选）",
        ],
        "key_locations": [
            ("tsconfig.json", "TypeScript 配置核心：target、module、strict 模式"),
            ("src/index.ts", "Web 应用入口：编译后注入 HTML"),
            ("types/", "全局类型定义区：.d.ts 声明文件的老巢"),
            ("node_modules/", "npm 依赖热带雨林：庞大但必须，了解它的结构很重要"),
            ("vite.config.ts", "Vite 构建配置：热更新、构建优化、插件链"),
        ],
        "trivia": (
            "TypeScript 的类型系统是图灵完备的——"
            "你甚至可以在类型层面做加减乘除（利用条件类型和模板字面量）。"
            "这意味着 TypeScript 的编译器本身就是一个类型计算器。"
        ),
    },
    "JavaScript": {
        "emoji": "🟡",
        "ecosystem_map": """
                    ┌─────────────────────┐
                    │    package.json      │ ← 项目元数据
                    └──────────┬──────────┘
                               │
              ┌────────────────┼────────────────┐
              ▼                ▼                ▼
        ┌──────────┐    ┌──────────┐    ┌──────────┐
        │  src/    │    │  dist/   │    │  node_   │
        │ (源码)   │    │ (打包输出)│    │ modules/ │
        └────┬─────┘    └──────────┘    └──────────┘
             │
             ▼
       ┌───────────┐  ┌─────────────────┐
       │ lib/      │  │  tests/         │
       │ (工具库)  │  │  (Jest 测试)     │
       └───────────┘  └─────────────────┘
        """,
        "entry_point": "src/index.js → 运行时 → node src/index.js",
        "naming_conventions": {
            "file": "kebab-case:  my-util.js, http-helper.js",
            "function": "camelCase:  function fetchUser(id) { }",
            "variable": "camelCase:  let maxRetries = 3",
            "class": "PascalCase:  class ConfigManager { }",
            "type": "PascalCase (class names serve as types in JS)",
            "constant": "UPPER_SNAKE:  const MAX_BUFFER_SIZE = 1024",
            "private": "_underscore:  let _privateVar = 42",
        },
        "dependency_style": """
  ┌──────────────┐    npm install / yarn add   ┌──────────────┐
  │ package.json │ ────────────────────────▶  │   npm        │
  │              │     依赖安装                 │   registry   │
  └──────────────┘                              └──────────────┘

  ┌──────────────┐   webpack / vite / rollup   ┌──────────────┐
  │  src/        │ ────────────────────────▶  │  bundle.js  │
  │  (源码)      │      打包为单文件             │  (可部署)    │
  └──────────────┘                              └──────────────┘
        """,
        "project_sketch": [
            "my-js-app/",
            "├── package.json         ← 项目元数据 + npm scripts",
            "├── node_modules/        ← npm 依赖（.gitignore 排除）",
            "├── src/",
            "│   ├── index.js        ← 应用入口",
            "│   ├── lib/             ← 工具函数库",
            "│   ├── routes/          ← 路由定义",
            "│   ├── middleware/      ← Express 中间件",
            "│   └── models/          ← 数据模型（ORM）",
            "├── dist/               ← 打包产物",
            "└── tests/              ← Jest 测试套件",
        ],
        "key_locations": [
            ("package.json", "项目元数据心脏：scripts、dependencies、version"),
            ("src/index.js", "Node.js 应用入口：模块加载的起点"),
            ("node_modules/", "npm 依赖热带雨林：所有第三方代码的栖身地"),
            (".gitignore", "必须排除 node_modules/、dist/、*.log"),
            ("dist/", "构建产物：生产环境部署的就是这里"),
        ],
        "trivia": (
            "JavaScript 诞生于 1995 年，仅用 10 天设计完成，"
            "创造者 Brendan Eich 称之为'remarkably funky'（相当 funky）。"
            "它的原型继承模型（prototype-based）是当时主流 class-based OOP 的异类，"
            "造就了今天 JS 的独特灵活性和'什么都能转'的类型系统。"
        ),
    },
    "Java": {
        "emoji": "☕",
        "ecosystem_map": """
                    ┌─────────────────────┐
                    │    pom.xml / build.gradle │ ← 构建系统配置
                    └──────────┬──────────┘
                               │
              ┌────────────────┼────────────────┐
              ▼                ▼                ▼
        ┌──────────┐    ┌──────────┐    ┌──────────┐
        │  src/    │    │  src/    │    │ target/  │
        │ main/java│    │ test/java│    │ (编译产物)│
        └────┬─────┘    └──────────┘    └──────────┘
             │
             ▼
       ┌─────────────────────────────────────────────┐
       │  com.example.myapp/                          │
       │    ├── model/    ← POJO、Entity、DTO         │
       │    ├── repository/ ← 数据访问层               │
       │    ├── service/  ← 业务逻辑层                │
       │    ├── controller/ ← HTTP / API 层            │
       │    └── config/   ← Spring 配置               │
       └─────────────────────────────────────────────┘
        """,
        "entry_point": "src/main/java/.../Main.java → public static void main(String[] args)",
        "naming_conventions": {
            "file": "PascalCase:  UserService.java, HttpClient.java",
            "function": "camelCase:  public User findUserById(Long id)",
            "variable": "camelCase:  private int maxRetries",
            "type": "PascalCase:  class UserProfile, interface Repository<T>",
            "constant": "UPPER_SNAKE:  public static final int MAX_SIZE = 100",
            "package": "全小写:  com.example.myapp",
        },
        "dependency_style": """
  ┌──────────────┐   mvn install / gradle build   ┌──────────────┐
  │   pom.xml    │ ────────────────────────────▶  │   Maven     │
  │              │     依赖解析 + 编译             │   Central   │
  └──────────────┘                                └──────────────┘

  ┌──────────────┐   Spring Boot 自动配置         ┌──────────────┐
  │ application.yml │ ──────────────────────▶  │  Spring     │
  │                  │   约定优于配置              │  Boot       │
  └──────────────┘                                └──────────────┘
        """,
        "project_sketch": [
            "my-java-app/",
            "├── pom.xml              ← Maven 构建配置（或 build.gradle）",
            "├── src/",
            "│   ├── main/java/com/example/app/",
            "│   │   ├── MyApplication.java ← Spring Boot 启动类",
            "│   │   ├── controller/       ← REST API 层",
            "│   │   ├── service/          ← 业务逻辑层",
            "│   │   ├── repository/        ← 数据访问层（JPA）",
            "│   │   ├── model/             ← 实体和 DTO",
            "│   │   └── config/            ← 配置类",
            "│   └── test/java/             ← JUnit 测试",
            "├── resources/",
            "│   └── application.yml         ← Spring 配置",
            "└── target/                    ← 编译产物（Maven）",
        ],
        "key_locations": [
            ("pom.xml / build.gradle", "构建系统配置心脏：依赖、插件、profile"),
            ("src/main/java/", "Java 源码根目录：按包路径组织，完全与目录结构一致"),
            ("MyApplication.java", "Spring Boot 启动类：@SpringBootApplication 注解"),
            ("application.yml", "配置文件：数据库、端口、日志级别"),
            ("target/", "Maven 编译产物目录：.class 文件和可执行的 JAR 包"),
        ],
        "trivia": (
            "Java 的'一个文件一个公共类'规则（文件名必须与公共类名一致）"
            "是 C++ 时代遗留的产物——当时编译器需要这个对应关系。"
            "而 Kotlin 完全打破了这个规则，可以在同一个文件里放多个类。"
            "但 Java 开发者至今仍保留'一个类一个文件'的习惯。"
        ),
    },
    "C/C++": {
        "emoji": "🔩",
        "ecosystem_map": """
                    ┌─────────────────────┐
                    │  CMakeLists.txt     │ ← CMake 构建配置
                    │  Makefile / .pro    │ ← 其他构建系统
                    └──────────┬──────────┘
                               │
              ┌────────────────┼────────────────┐
              ▼                ▼                ▼
        ┌──────────┐    ┌──────────┐    ┌──────────┐
        │  include/│    │   src/   │    │  build/  │
        │ (头文件)  │    │ (实现)   │    │ (编译产物)│
        └────┬─────┘    └────┬─────┘    └──────────┘
             │                │
             ▼                ▼
       ┌───────────┐  ┌──────────────┐
       │ .h / .hpp │  │  .cpp / .c   │
       └───────────┘  └──────────────┘
        """,
        "entry_point": "int main(int argc, char* argv[]) { ... }",
        "naming_conventions": {
            "file": "snake_case:  my_utility.cpp, user_service.hpp",
            "function": "snake_case / PascalCase:  calculate_total() 或 CalculateTotal()",
            "variable": "snake_case:  int max_buffer_size = 1024",
            "type": "PascalCase:  class ConfigManager, struct UserData",
            "macro": "UPPER_SNAKE:  #define MAX_BUFFER_SIZE 1024",
            "namespace": "lowercase:  namespace my_project { }",
        },
        "dependency_style": """
  ┌──────────────┐   cmake .. && make / g++      ┌──────────────┐
  │ CMakeLists.txt│ ──────────────────────────▶  │  Native     │
  │              │     编译为可执行文件            │  binary     │
  └──────────────┘                                └──────────────┘

  ┌──────────────┐   Conan / vcpkg / fetch_content  ┌──────────┐
  │ conanfile.py │ ──────────────────────────────▶  │ Conan   │
  │              │     C++ 包管理器                 │ Center  │
  └──────────────┘                                   └──────────┘
        """,
        "project_sketch": [
            "my-cpp-app/",
            "├── CMakeLists.txt       ← CMake 构建脚本（主配置）",
            "├── Makefile             ← GNU Make 简化构建（可选）",
            "├── include/",
            "│   └── myapp/           ← 头文件目录（对外 API）",
            "│       ├── api.h        ← 公共接口声明",
            "│       └── types.hpp    ← 类型定义",
            "├── src/",
            "│   ├── main.cpp         ← 程序入口",
            "│   ├── api.cpp          ← 接口实现",
            "│   └── utils.cpp        ← 工具函数",
            "├── lib/                 ← 静态/动态库（可选）",
            "├── build/               ← 编译产物（out-of-source）",
            "└── tests/               ← GoogleTest / Catch2 测试",
        ],
        "key_locations": [
            ("CMakeLists.txt", "CMake 构建脚本：定义目标、源文件、依赖关系"),
            ("include/", "头文件目录：.h/.hpp 对外声明，-I 编译选项指向这里"),
            ("src/", "实现文件目录：.cpp/.c 藏在这里，include 头文件使用"),
            ("build/", "构建目录：cmake 推荐 out-of-source 构建，保持源码整洁"),
            ("main.cpp", "程序入口：int main(int argc, char* argv[]) 是旅程起点"),
        ],
        "trivia": (
            "C/C++ 没有官方的包管理器——这是它与所有现代语言最大的差距之一。"
            "Conan、vcpkg、Hunter 是社区方案，但碎片化严重。"
            "C++20 引入的 Modules TS 试图解决头文件重复编译的世纪难题，"
            "但编译器支持尚不完整，这场战争远未结束。"
        ),
    },
}


# ══════════════════════════════════════════════════════════════════════════════
# 工具函数
# ══════════════════════════════════════════════════════════════════════════════

def _read_json(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _write_json(path: str, data: Dict[str, Any]) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# ══════════════════════════════════════════════════════════════════════════════
# 核心 API
# ══════════════════════════════════════════════════════════════════════════════

def generate_map(
    json_path: str = DEFAULT_LANGUAGE_ROTATION_JSON,
) -> Dict[str, Any]:
    """
    读取 language_rotation.json，取出当前语言，
    生成该语言的代码地理报告（不推进索引）。

    Returns:
        {
            "language": str,
            "emoji": str,
            "ecosystem_map": str,
            "entry_point": str,
            "naming_conventions": dict,
            "dependency_style": str,
            "project_sketch": list[str],
            "key_locations": list[tuple[str, str]],
            "trivia": str,
            "generated_at": str,
        }
    """
    data = _read_json(json_path)
    languages = data["languages"]
    idx = data.get("current_index", 0) % len(languages)
    current = languages[idx]

    map_data = CARTOGRAPHER_DB.get(current, {})
    return {
        "language": current,
        "emoji": map_data.get("emoji", "📦"),
        "ecosystem_map": map_data.get("ecosystem_map", ""),
        "entry_point": map_data.get("entry_point", ""),
        "naming_conventions": map_data.get("naming_conventions", {}),
        "dependency_style": map_data.get("dependency_style", ""),
        "project_sketch": map_data.get("project_sketch", []),
        "key_locations": map_data.get("key_locations", []),
        "trivia": map_data.get("trivia", ""),
        "generated_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00"),
    }


def format_map_markdown(
    result: Optional[Dict[str, Any]] = None,
    json_path: str = DEFAULT_LANGUAGE_ROTATION_JSON,
) -> str:
    """
    生成代码地理报告（Markdown 格式）。
    不指定 result 时，使用当前轮换语言（不推进索引）。
    """
    if result is None:
        result = generate_map(json_path=json_path)

    lang = result["language"]
    emoji = result["emoji"]
    lines = [
        f"# 🗺️ 代码地理报告 | {emoji} **{lang}**",
        f"",
        f"> 本报告将带你「身临其境」地探索 {lang} 的代码世界——",
        f"> 从项目入口到模块布局，从命名惯例到依赖管理，",
        f"> 让你对 {lang} 的项目组织方式有一个直观的空间感。",
        f"",
        f"---",
        f"",
        f"## 🌍 生态系统拓扑图",
        f"",
        f"```\n{result['ecosystem_map'].strip()}\n```",
        f"",
        f"## 🚪 入口点定位",
        f"",
        f"```{lang.lower().replace('/', '')}",
        f"{result['entry_point']}",
        f"```",
        f"",
        f"## 📝 命名Convention光谱",
        f"",
    ]

    naming = result["naming_conventions"]
    convention_labels = {
        "file": "文件",
        "function": "函数",
        "variable": "变量",
        "type": "类型",
        "constant": "常量",
        "macro": "宏",
        "package": "包",
        "interface": "接口",
    }
    for key, label in convention_labels.items():
        if key in naming:
            lines.append(f"- **{label}**：{naming[key]}")

    lines.extend([
        f"",
        f"## 🔗 依赖管理方式",
        f"",
        f"```\n{result['dependency_style'].strip()}\n```",
        f"",
        f"## 📐 典型项目目录草图",
        f"",
    ])
    for sketch_line in result["project_sketch"]:
        lines.append(f"    {sketch_line}")

    lines.extend([
        f"",
        f"## 🗝️ 语言必去之地",
        f"",
    ])
    for loc, desc in result["key_locations"]:
        lines.append(f"- **{loc}**：{desc}")

    lines.extend([
        f"",
        f"## 🧩 代码地理趣闻",
        f"",
        f"{result['trivia']}",
        f"",
        f"---",
    f"*⟩ 代码地理报告 | {lang} | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
    ])
    return "\n".join(lines)


def format_map_console(
    result: Optional[Dict[str, Any]] = None,
    json_path: str = DEFAULT_LANGUAGE_ROTATION_JSON,
) -> str:
    """
    生成代码地理报告（终端彩色控制台格式）。
    """
    if result is None:
        result = generate_map(json_path=json_path)

    lang = result["language"]
    emoji = result["emoji"]

    border = "  " + "═" * 52
    parts = [
        border,
        f"  🗺️  代码地理报告  {emoji}  {lang}",
        border,
        f"  📍 入口：{result['entry_point']}",
        border,
        f"  📝 命名惯例：",
    ]
    naming = result["naming_conventions"]
    convention_labels = {
        "file": "文件", "function": "函数", "variable": "变量",
        "type": "类型", "constant": "常量", "macro": "宏",
        "package": "包", "interface": "接口",
    }
    for key, label in convention_labels.items():
        if key in naming:
            parts.append(f"     {label:8} {naming[key]}")

    parts.extend([border, f"  🗂️ 典型项目结构："])
    for sketch_line in result["project_sketch"]:
        parts.append(f"  {sketch_line}")

    parts.extend([border, f"  🗝️ 必去之地："])
    for loc, desc in result["key_locations"]:
        parts.append(f"     • {loc} → {desc}")

    parts.extend([border, f"  🧩 趣闻：{result['trivia'][:80]}…"])
    parts.append(border)
    return "\n".join(parts)


# ─────────────────────────────────────────────
# CLI 入口
# ─────────────────────────────────────────────
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Polyglot Cartographer — 代码地理测绘仪")
    sub = parser.add_subparsers(dest="cmd")

    sub.add_parser("map", help="生成当前语言的代码地理报告（Markdown）")
    sub.add_parser("console", help="生成当前语言的代码地理报告（控制台）")

    report_parser = sub.add_parser("report", help="查看指定语言的代码地理报告")
    report_parser.add_argument("language", nargs="?", default=None, help="语言名称（可选）")
    report_parser.add_argument("--format", choices=["md", "console"], default="md")

    args = parser.parse_args()

    if args.cmd == "map":
        result = generate_map()
        print(format_map_markdown(result))
    elif args.cmd == "console":
        result = generate_map()
        print(format_map_console(result))
    elif args.cmd == "report":
        if args.language:
            map_data = CARTOGRAPHER_DB.get(args.language, {})
            if not map_data:
                print(f"未知语言: {args.language}")
                sys.exit(1)
            result = {
                "language": args.language,
                "emoji": map_data.get("emoji", "📦"),
                "ecosystem_map": map_data.get("ecosystem_map", ""),
                "entry_point": map_data.get("entry_point", ""),
                "naming_conventions": map_data.get("naming_conventions", {}),
                "dependency_style": map_data.get("dependency_style", ""),
                "project_sketch": map_data.get("project_sketch", []),
                "key_locations": map_data.get("key_locations", []),
                "trivia": map_data.get("trivia", ""),
                "generated_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00"),
            }
        else:
            result = generate_map()

        if args.format == "console":
            print(format_map_console(result))
        else:
            print(format_map_markdown(result))
    else:
        parser.print_help()
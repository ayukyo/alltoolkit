# AllToolkit 🧰

**多语言工具函数库 - 零依赖，生产就绪**

[![Build Status](https://github.com/ayukyo/alltoolkit/actions/workflows/ci.yml/badge.svg)](https://github.com/ayukyo/alltoolkit/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## ✨ 特性

- **零依赖** - 仅使用各语言标准库
- **生产就绪** - 完整测试、详细文档、错误处理
- **多语言支持** - 20+ 编程语言，100+ 工具模块
- **统一结构** - 每个模块包含主文件、测试、示例、文档
- **自动化维护** - 每小时自动生成新工具，每日优化代码

---

## 📦 支持的语言

| 语言 | 模块数 | 状态 |
|------|--------|------|
| Python | 15+ | ✅ 活跃 |
| Go | 15+ | ✅ 活跃 |
| Rust | 10+ | ✅ 活跃 |
| Java | 10+ | ✅ 活跃 |
| JavaScript | 10+ | ✅ 活跃 |
| TypeScript | 10+ | ✅ 活跃 |
| C# | 10+ | ✅ 活跃 |
| C++ | 5+ | ✅ 活跃 |
| C | 5+ | ✅ 活跃 |
| PHP | 10+ | ✅ 活跃 |
| Ruby | 5+ | ✅ 活跃 |
| MATLAB | 5+ | ✅ 活跃 |
| R | 5+ | ✅ 活跃 |
| Fortran | 5+ | ✅ 活跃 |
| Delphi | 5+ | ✅ 活跃 |
| Perl | 6+ | ✅ 活跃 |
| Kotlin | 6+ | ✅ 活跃 |

*完整列表见 [docs/languages.md](docs/languages.md)*

---

## 🚀 快速开始

### Python 示例

```bash
# 安装
pip install alltoolkit-text-utils

# 使用
from alltoolkit import text_utils

text = "  Hello World  "
cleaned = text_utils.strip(text)  # "Hello World"
```

### Go 示例

```go
import "github.com/ayukyo/alltoolkit/go/queue_utils"

q := queue_utils.NewQueue[int]()
q.Enqueue(1)
q.Enqueue(2)
val := q.Dequeue()  // 1
```

### Rust 示例

```rust
use alltoolkit_string_utils::truncate;

let text = "Hello World";
let truncated = truncate(text, 5);  // "He..."
```

---

## 📁 项目结构

```
AllToolkit/
├── Python/
│   ├── text_utils/
│   │   ├── mod.py              # 主模块
│   │   ├── text_utils_test.py  # 测试
│   │   ├── README.md           # 详细文档
│   │   └── examples/
│   │       └── usage_examples.py
│   └── ...
├── Go/
│   ├── queue_utils/
│   │   ├── mod.go
│   │   ├── queue_utils_test.go
│   │   └── README.md
│   └── ...
├── docs/
│   ├── languages.md            # 语言支持列表
│   └── contributing.md         # 贡献指南
├── CHANGELOG.md                # 更新日志
└── README.md                   # 本文件
```

---

## 📚 文档

- **主文档**: [docs/languages.md](docs/languages.md) - 所有语言模块列表
- **贡献指南**: [docs/contributing.md](docs/contributing.md)
- **更新日志**: [CHANGELOG.md](CHANGELOG.md)
- **各模块文档**: `{Language}/{module}/README.md`

---

## 🤝 贡献

欢迎贡献代码、测试、文档！

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

详见 [docs/contributing.md](docs/contributing.md)

---

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE)

---

## 🔗 链接

- **GitHub**: https://github.com/ayukyo/alltoolkit
- **文档**: https://github.com/ayukyo/alltoolkit/docs
- **问题反馈**: https://github.com/ayukyo/alltoolkit/issues

---

## 🧪 测试

每个模块都包含完整的测试套件，覆盖正常场景、边界值和异常情况：

```bash
# Python 测试
python Python/text_utils/text_utils_test.py
python Python/network_utils/network_utils_test.py

# Kotlin 测试
kotlinc Kotlin/zip_utils/zip_utils_test.kt -include-runtime -d zip_test.jar && java -jar zip_test.jar

# Perl 测试
perl Perl/csv_utils/csv_utils_test.pl
```

### 最近新增测试

- **Kotlin zip_utils**: 新增 15 个测试用例，覆盖文件压缩、解压、目录处理、排除模式等
- **Perl csv_utils**: 新增 30+ 测试用例，覆盖 CSV 解析、生成、过滤、排序等
- **Python network_utils**: 已有 70+ 测试用例，覆盖 URL/IP/MAC/端口/HTTP 等
- **Python text_utils**: 已有 60+ 测试用例，覆盖字符串清理、格式化、分析等

---

**最后更新**: 2026-04-09

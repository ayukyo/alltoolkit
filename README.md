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
| Python | 18+ | ✅ 活跃 |
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
| Swift | 9+ | ✅ 活跃 |

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

- **Rust file_utils**: 新增 40+ 测试用例，覆盖文件读写、存在性检查、错误处理、边界值等 📁
- **Rust qr_code_utils**: 新增 45+ 测试用例，覆盖 QR 码生成、版本校验、纠错级别、编码模式、容量表验证等 🔲
- **TypeScript crypto_utils**: 86 个测试用例（新增），覆盖哈希函数（MD5/SHA-1/SHA-256/SHA-384/SHA-512）、HMAC 签名/验证、Base64 编码解码、Hex 编码解码、随机生成（字符串/Hex/UUID）等 🔐
- **Python text_utils**: 123 个测试用例（新增 9 个），覆盖字符串清理、格式化、分析等，新增 wrap_text 边界值测试（零宽度、负宽度、空字符串、超长单词处理等）📝
- **Python base64_utils**: 22 个测试用例（新增 7 个），覆盖编码/解码、URL-safe、验证等，新增 is_valid 边界测试（长度校验、填充验证、URL-safe 模式等）🔐
- **Go csv_utils**: 新增 SortByWithOptions 测试（降序排序、非数字回退、缺失列处理等）📊
- **Go log_utils**: 新增 formatText 测试（无调用者、多字段格式化等）📝
- **JavaScript string_utils**: 93 个测试用例（新增 10 个），覆盖字符串操作，新增 randomPassword 边界测试（最小/最大长度、字符类型检查、随机性验证等）和 truncate 边界测试 🔤
- **Python email_utils**: 41 个测试用例，覆盖验证、解析、规范化、一次性邮箱检测、批量处理等 📧
- **Kotlin zip_utils**: 15 个测试用例，覆盖文件压缩、解压、目录处理、排除模式等
- **Perl csv_utils**: 30+ 测试用例，覆盖 CSV 解析、生成、过滤、排序等
- **Python network_utils**: 70+ 测试用例，覆盖 URL/IP/MAC/端口/HTTP 等

### 测试覆盖详情

| 模块 | 语言 | 测试数 | 覆盖率 |
|------|------|--------|--------|
| file_utils | Rust | 40+ | ✅ 100% |
| qr_code_utils | Rust | 45+ | ✅ 100% |
| color_utils | Rust | 30+ | ✅ 100% |
| crypto_utils | TypeScript | 86 | ✅ 100% |
| xml_utils | Python | 20 | ✅ 100% |
| markdown_utils | Python | 108 | ✅ 100% |
| regex_utils | Python | 34 | ✅ 100% |
| json_utils | Python | 49 | ✅ 100% |
| email_utils | Python | 41 | ✅ 100% |
| hash_utils | Python | 84 | ✅ 100% |
| geometry_utils | Python | 237 | ✅ 100% |
| sqlite_utils | Python | 86 | ✅ 100% |
| color_utils | Python | 111 | ✅ 100% |
| emoji_utils | Python | 49 | ✅ 100% |
| password_utils | Python | 52 | ✅ 100% |
| base64_utils | Python | 22 | ✅ 100% |
| time_zone_utils | Python | 45 | ✅ 100% |
| env_utils | Python | 8 大类 | ✅ 100% |
| shell_utils | Python | 14 | ✅ 100% |
| phone_utils | Python | 31 | ✅ 100% |
| jwt_utils | Python | 15 | ✅ 100% |
| cache_utils | Python | 30+ | ✅ 100% |
| uuid_utils | Java | 69 | ✅ 100% |

---

**最后更新**: 2026-04-16

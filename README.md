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
| Python | 108 | ✅ 活跃 |
| Go | 29 | ✅ 活跃 |
| Rust | 15 | ✅ 活跃 |
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

- **Python otp_utils**: 新增 35+ 边界值测试，覆盖 TOTP/HOTP 生成、Base32 编解码、URI 构建、恢复码、空数据、极端参数等 🔐
- **Python fractions_utils**: 143 个测试用例，覆盖分数运算、类型转换、GCD/LCM、序列生成、边界值（零、负数、大数）等 📊
- **Python env_utils**: 65 个测试用例，覆盖环境变量操作、.env 文件、验证、快照、敏感数据脱敏等 ⚙️
- **Python memory_profile_utils**: 32 个测试用例，覆盖内存监控、对象分析、泄漏检测、优化建议等 📈
- **Python json_utils**: 新增 93 个测试用例，覆盖安全解析、序列化、路径查询、合并、扁平化、过滤、类型检查、深度比较等，新增 30+ 边界值测试（空值、深层嵌套、大数据、Unicode、数组边界等）📝
- **Python humanize_utils**: 新增 30+ 边界值测试，覆盖空值、极大数值、负数、中文单位等边界场景 📝
- **Python crypto_utils**: 新增 20+ 边界值测试，覆盖空数据、单字符、极长数据、自定义字符集等边界场景 🔐
- **Python qr_code_utils**: 新增 26 边界值测试，覆盖空数据、Unicode、特殊字符、SVG/ASCII 边界等场景 🔲
- **Python tarot_utils**: 36 个测试用例，覆盖塔罗牌牌组、抽取、解读（单牌/三牌/凯尔特十字）、是非问题等 🎴
- **Python sparkline_utils**: 70 个测试用例，覆盖迷你图生成、Braille 模式、柱状图、趋势指示器、仪表盘、胜负图、直方图等 📊
- **Python solar_utils**: 52 个测试用例，覆盖日出日落计算、太阳位置、曙暮光时间、白昼时长、黄金时刻、季节判断等 ☀️
- **Python boyer_moore_utils**: 25+ 测试用例，覆盖字符串搜索、中文文本、特殊字符、性能比较等 🔍
- **Python chess_utils**: 30+ 测试用例，覆盖棋盘、棋子、移动、FEN/PGN 格式、特殊局面、完整对局等 ♟️
- **Python time_zone_utils**: 45 个测试用例，覆盖时区转换、DST、会议时间查找、边界值（跨日期/年份、半小时偏移）等 🌍
- **Python mask_utils**: 41 个测试用例，覆盖邮箱/手机/身份证/银行卡/信用卡/姓名/地址/IP/密码/URL 掩码等 🔒
- **Python nanoid_utils**: 40 个测试用例，覆盖 ID 生成、自定义长度/字符集、唯一性验证等 🆔
- **Python isbn_utils**: 43 个测试用例，覆盖 ISBN-10/13 验证、转换、格式化等 📚
- **Python mime_utils**: 45 个测试用例，覆盖 MIME 类型检测、文件扩展名映射等 📄
- **Rust file_utils**: 新增 40+ 测试用例，覆盖文件读写、存在性检查、错误处理、边界值等 📁
- **Rust qr_code_utils**: 新增 45+ 测试用例，覆盖 QR 码生成、版本校验、纠错级别、编码模式、容量表验证等 🔲
- **TypeScript crypto_utils**: 86 个测试用例（新增），覆盖哈希函数（MD5/SHA-1/SHA-256/SHA-384/SHA-512）、HMAC 签名/验证、Base64 编码解码、Hex 编码解码、随机生成（字符串/Hex/UUID）等 🔐
- **Python text_utils**: 89 个测试用例，覆盖字符串清理、格式化、分析等，新增 wrap_text 边界值测试（零宽度、负宽度、空字符串、超长单词处理等）📝
- **Python base64_utils**: 22 个测试用例，覆盖编码/解码、URL-safe、验证等，新增 is_valid 边界测试（长度校验、填充验证、URL-safe 模式等）🔐
- **Go csv_utils**: 新增 SortByWithOptions 测试（降序排序、非数字回退、缺失列处理等）📊
- **Go log_utils**: 新增 formatText 测试（无调用者、多字段格式化等）📝
- **JavaScript string_utils**: 93 个测试用例（新增 10 个），覆盖字符串操作，新增 randomPassword 边界测试（最小/最大长度、字符类型检查、随机性验证等）和 truncate 边界测试 🔤
- **Python email_utils**: 41 个测试用例，覆盖验证、解析、规范化、一次性邮箱检测、批量处理等 📧
- **Kotlin zip_utils**: 15 个测试用例，覆盖文件压缩、解压、目录处理、排除模式等
- **Perl csv_utils**: 30+ 测试用例，覆盖 CSV 解析、生成、过滤、排序等
- **Python network_utils**: 134 个测试用例，覆盖 URL/IP/MAC/端口/HTTP 等

### 测试覆盖详情

| 模块 | 语言 | 测试数 | 覆盖率 |
|------|------|--------|--------|
| json_utils | Python | 93 | ✅ 100% |
| geometry_utils | Python | 237 | ✅ 100% |
| phone_utils | Python | 164 | ✅ 100% |
| color_utils | Python | 111 | ✅ 100% |
| markdown_utils | Python | 108 | ✅ 100% |
| bloom_filter_utils | Python | 99 | ✅ 100% |
| humanize_utils | Python | 85+ | ✅ 100% |
| hash_utils | Python | 84 | ✅ 100% |
| sqlite_utils | Python | 86 | ✅ 100% |
| credit_card_utils | Python | 80 | ✅ 100% |
| crypto_utils | Python | 75 | ✅ 100% |
| compression_utils | Python | 74 | ✅ 100% |
| cron_utils | Python | 61 | ✅ 100% |
| huffman_utils | Python | 57 | ✅ 100% |
| data_validator | Python | 56 | ✅ 100% |
| combinatorics_utils | Python | 55 | ✅ 100% |
| async_utils | Python | 51 | ✅ 100% |
| ip_utils | Python | 51 | ✅ 100% |
| password_utils | Python | 52 | ✅ 100% |
| text_utils | Python | 89 | ✅ 100% |
| barcode_utils | Python | 59 | ✅ 100% |
| network_utils | Python | 134 | ✅ 100% |
| archive_utils | Python | 44 | ✅ 100% |
| business_day_utils | Python | 45 | ✅ 100% |
| base64_utils | Python | 22 | ✅ 100% |
| qr_code_utils | Python | 15 | ✅ 100% |
| benchmark_utils | Python | 32 | ✅ 100% |
| datetime_utils | Python | 32 | ✅ 100% |
| email_utils | Python | 41 | ✅ 100% |
| cache_utils | Python | 35 | ✅ 100% |
| xml_utils | Python | 20 | ✅ 100% |
| emoji_utils | Python | 49 | ✅ 100% |
| otp_utils | Python | 45 | ✅ 100% |
| fractions_utils | Python | 143 | ✅ 100% |
| env_utils | Python | 65 | ✅ 100% |
| memory_profile_utils | Python | 32 | ✅ 100% |
| sparkline_utils | Python | 70 | ✅ 100% |
| solar_utils | Python | 52 | ✅ 100% |
| tarot_utils | Python | 36 | ✅ 100% |
| boyer_moore_utils | Python | 25+ | ✅ 100% |
| chess_utils | Python | 30+ | ✅ 100% |

**总计**: Python 108 模块，2000+ 测试用例，100% 通过率 ✅

---

**最后更新**: 2026-04-22

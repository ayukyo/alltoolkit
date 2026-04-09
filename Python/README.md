# AllToolkit - Python 工具模块 🐍

**Python 工具函数集合 - 零依赖，生产就绪**

---

## 📦 可用模块

| 模块 | 描述 | 状态 |
|------|------|------|
| `base64_utils` | Base64 编码/解码工具 | ✅ |
| **`cache_utils`** | **内存缓存（TTL/LRU/线程安全/统计）** | ✅ **NEW** |
| **`color_utils`** | **颜色处理（转换/操作/调色板/无障碍检测）** | ✅ **NEW** |
| **`compression_utils`** | **压缩工具（gzip/zip/tar 归档）** | ✅ **NEW** |
| `crypto_utils` | 加密解密工具 | ✅ |
| `csv_utils` | CSV 文件处理 | ✅ |
| `data_structures_utils` | 数据结构实现（栈、队列、链表、树等） | ✅ |
| `datetime_utils` | 日期时间处理工具 | ✅ |
| **`env_utils`** | **环境变量管理（读写/.env 文件/验证/快照/脱敏）** | ✅ **NEW** |
| **`email_utils`** | **电子邮件处理（验证/解析/规范化/分类/批量处理）** | ✅ **NEW** |
| `file_utils` | 文件操作工具 | ✅ |
| **`hash_utils`** | **哈希工具（MD5/SHA/HMAC/文件哈希）** | ✅ **NEW** |
| **`jwt_utils`** | **JWT 处理（创建/解码/验证/刷新/批量操作）** | ✅ **NEW** |
| **`log_utils`** | **日志处理（解析/过滤/分析/格式化/轮转）** | ✅ **NEW** |
| **`markdown_utils`** | **Markdown 处理（转换/提取/生成/验证）** | ✅ **NEW** |
| `ini_config_utils` | INI 配置文件处理 | ✅ |
| `json_utils` | JSON 处理工具 | ✅ |
| `network_utils` | 网络工具 | ✅ |
| `phone_utils` | 电话号码处理 | ✅ |
| `qr_code_utils` | 二维码生成/识别 | ✅ |
| `random_utils` | 随机数生成工具 | ✅ |
| **`regex_utils`** | **正则表达式（验证/提取/替换/匹配/文本清洗）** | ✅ **NEW** |
| **`shell_utils`** | **Shell 命令执行与系统操作** | ✅ **NEW** |
| `text_utils` | 文本处理工具 | ✅ |
| `validation_utils` | 数据验证工具 | ✅ |
| **`xml_utils`** | **XML 解析与生成** | ✅ **NEW** |

---

## 🚀 快速开始

### 安装

无需安装！直接复制模块到你的项目：

```bash
# 复制单个模块
cp AllToolkit/Python/hash_utils/mod.py your_project/

# 或克隆整个仓库
git clone https://github.com/ayukyo/alltoolkit.git
```

### 使用示例

```python
# 缓存工具
from mod import Cache, cached

# 创建缓存
cache = Cache(max_size=100, default_ttl=300.0)
cache.set("key", "value")
print(cache.get("key"))  # "value"

# 使用装饰器缓存函数结果
@cached(ttl=60.0)
def expensive_query(user_id):
    return {"id": user_id, "name": f"User_{user_id}"}

# CSV 工具
from mod import read_csv, write_csv, filter_by_value, sort_rows

# 读取 CSV
data = read_csv('employees.csv')

# 过滤数据
hr_staff = filter_by_value(data, 'dept', 'HR')

# 排序
sorted_data = sort_rows(data, 'salary', reverse=True)

# 写入 CSV
write_csv('output.csv', sorted_data)

# 哈希工具
from mod import sha256, hmac_hash, hash_file

# 计算哈希
h = sha256("Hello, World!")
print(h)  # 2cf24dba5fb0a30e26e83b2ac5b9e29e...

# HMAC 认证
mac = hmac_hash("message", "secret_key")

# 文件哈希
file_hash = hash_file("document.pdf")

# 正则表达式工具
from mod import validate_email, extract_urls, censor_phone, TextCleaner

# 验证邮箱
if validate_email("test@example.com"):
    print("有效邮箱")

# 提取 URL
urls = extract_urls("访问 https://example.com 获取信息")
print(urls)  # ['https://example.com']

# 电话脱敏
print(censor_phone("13800138000"))  # 138****8000

# 文本清洗
cleaner = TextCleaner()
text = (cleaner
        .load("<p>Hello @user #topic</p>   Extra   spaces")
        .remove_html()
        .remove_mentions()
        .normalize_whitespace()
        .get())
print(text)  # "Hello #topic"

# JWT 工具
from mod import create_token, decode_token, verify_token, create_auth_token

# 创建认证 Token
token = create_auth_token(
    user_id=123,
    username='john',
    secret='my-secret-key',
    roles=['user', 'admin'],
    expires_in_hours=24
)

# 验证 Token
valid, payload, error = verify_token(token, 'my-secret-key')
if valid:
    print(f"用户：{payload['username']}, 角色：{payload['roles']}")
else:
    print(f"验证失败：{error}")

# 刷新 Token
new_token = refresh_token(token, 'my-secret-key', new_expires_in_hours=48)
```

---

## 📁 模块结构

每个模块遵循统一结构：

```
module_name/
├── mod.py              # 主要实现
├── module_name_test.py # 测试套件
├── README.md           # 详细文档
└── examples/           # 使用示例
    ├── basic_usage.py
    └── advanced_example.py
```

---

## 🧪 运行测试

```bash
cd hash_utils
python hash_utils_test.py
```

---

## 📊 测试覆盖

- ✅ 基本哈希函数（MD5/SHA1/SHA256/SHA512）
- ✅ HMAC 生成和验证
- ✅ 文件哈希计算
- ✅ 目录批量哈希
- ✅ 编码转换（Hex/Base64/Bytes）
- ✅ 增量哈希
- ✅ 密码哈希
- ✅ Unicode 支持
- ✅ 边界情况处理

---

## 🔒 安全注意事项

1. **密码存储**：生产环境请使用 bcrypt/argon2
2. **HMAC 密钥**：使用足够长的随机密钥
3. **算法选择**：推荐使用 SHA256 或 SHA512
4. **定时攻击防护**：所有比较使用 `hmac.compare_digest`

---

## 📄 许可证

MIT License

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

仓库：https://github.com/ayukyo/alltoolkit

# AllToolkit 更新日志

## [2026-04-09]

### 新增
- **Python: cache_utils (70+ 测试，完整内存缓存工具)** 🧠
  - TTL 过期（按条目设置生存时间）
  - LRU 淘汰（自动淘汰最少使用条目）
  - 大小限制（可配置最大缓存容量）
  - 线程安全（支持并发访问）
  - 统计追踪（命中率、驱逐数等指标）
  - 批量操作（get_many/set_many/delete_many）
  - 原子计数（increment/decrement）
  - 懒加载（get_or_set 模式）
  - @cached 装饰器（一键缓存函数结果）
  - 缓存预热（warm 方法批量填充）
  - 零依赖，纯 Python 标准库实现

- **Python: jwt_utils (15 测试，完整 JWT 处理工具)** 🔐
  - Token 创建（HS256/HS384/HS512/none 算法）
  - Token 解码与签名验证
  - 过期时间/生效时间验证
  - Payload 构建工具（标准 claims + 自定义）
  - Token 刷新与吊销
  - 批量创建和验证
  - 快捷创建（认证 Token、访客 Token、API Key）
  - 零依赖，纯 Python 标准库实现

- **Python: markdown_utils (108 测试，完整 Markdown 处理工具)** 📝
  - Markdown ↔ HTML 双向转换
  - 内容提取（标题/链接/代码块/表格）
  - 文档生成（表格/链接/代码/列表/引用）
  - 语法验证（检测未闭合标记/空链接/层级跳跃）
  - 内容转换（标题级别调整/格式移除/词数统计）
  - 实用工具（文档合并/分割/注释清理）
  - 零依赖，纯 Python 标准库实现

- **Python: email_utils (41 测试，完整电子邮件处理工具)** 📧
  - RFC 5322 兼容验证
  - 智能解析（支持显示名称）
  - Gmail 规范化（点号、+ 标签处理）
  - 200+ 一次性邮箱域名检测
  - 免费邮箱服务商识别
  - 批量处理（去重、排序、分组、提取）
  - 隐私保护混淆显示

### 优化
- 无

## [2026-04-08]

### 新增
- Python: text_utils (116 测试，40+ 函数)
- Go: semaphore_utils (20 测试，信号量池)
- Rust: ini_utils (INI 配置文件解析)

### 优化
- Go/string_utils: Truncate 函数提前返回优化
- Python/file_utils: get_file_size O(n)→O(1)
- JavaScript/string_utils: randomPassword 拒绝采样消除模偏差
- Rust/string_utils: is_valid_email RFC 1035 验证
- Java/http_utils: readStream 8KB 缓冲区优化

## [2026-04-07]

### 新增
- Fortran: file_utils, random_utils
- C#: number_utils (40+ 函数)
- Go: semaphore_utils
- MATLAB: stats_utils, http_utils

### 优化
- 5 个工具函数性能优化

## [2026-04-06]

### 新增
- PHP: validation_utils, number_utils, uuid_utils, encoding_utils
- TypeScript: queue_utils, file_utils
- Delphi: qr_code_utils
- C: uuid_utils, qr_code_utils

---

*完整更新历史见 Git 提交记录*

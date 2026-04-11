# AllToolkit 更新日志

## [2026-04-12]

### 新增
- **Swift: array_utils (47 测试，完整数组/集合工具)** 📦
  - 空值与安全访问（isEmpty/isNotEmpty/firstSafe/lastSafe/safeGet/firstOr）
  - 切片操作（take/skip/takeLast/slice）
  - 去重与过滤（unique/filterNot/compacted/hasDuplicates/duplicates）
  - 转换与映射（compactMapNotNull/join）
  - 统计与聚合（sum/average/max/min/product/standardDeviation/median）
  - 搜索与查找（index/contains/findAll）
  - 分组与分区（groupBy/partition）
  - 排序（sortBy/isSortedAscending/isSortedDescending）
  - 组合与连接（concat）
  - 随机与打乱（randomElement/sample）
  - 工具函数（range/arithmeticSequence/geometricSequence/merge/interleave/transpose/filled/incrementingArray）
  - 类型安全扩展（Comparable/Hashable/Numeric/BinaryFloatingPoint 专用方法）
  - 零依赖，纯 Swift 标准库实现
  - 完整示例（基础用法 + 高级应用场景）
  - 边界值测试（空数组/单元素/负数/大数组）

## [2026-04-11]

### 新增
- **Python: emoji_utils (49 测试，完整表情符号处理工具)** 🎭
  - 表情符号提取（支持所有 Unicode 表情范围，包括扩展区）
  - 计数统计（总数/唯一数/频率统计）
  - 检测判断（has_emoji/is_emoji）
  - 移除替换（remove_emojis/replace_emojis）
  - Unicode 转换（to_unicode_escape/from_unicode_escape）
  - 肤色处理（strip_skin_tone/get_skin_tone_variants）
  - 文本转换（emoji_to_text/text_to_emoji）
  - 分类过滤（按类别筛选表情符号）
  - 位置追踪（get_emoji_positions）
  - 安全反转（reverse 保持表情符号完整）
  - 全面分析（EmojiAnalysis 包含密度/类别/详细信息）
  - 支持复杂表情（ZWJ 序列/变体选择器/肤色修饰符）
  - 零依赖，纯 Python 标准库实现
  - 完整示例（12 个使用场景演示）

- **Rust: process_utils (9 测试，完整进程管理工具)** 🔄
  - 进程配置（ProcessConfig 构建器，支持命令/参数/环境变量/工作目录/超时）
  - 进程管理器（ProcessManager，支持启动/运行/终止/监控）
  - 超时控制（可配置超时，自动终止超时进程）
  - 输出捕获（stdout/stderr 独立捕获，支持异步读取）
  - 进程信息（PID/PPID/名称/状态/内存/线程数，仅 Unix）
  - 进程树（获取子进程和完整进程树，仅 Unix）
  - 信号支持（SIGTERM 优雅关闭，SIGKILL 强制终止，仅 Unix）
  - 多进程管理（并发管理多个进程，线程安全）
  - 批处理支持（并行执行多个任务，可配置并发数）
  - 零依赖，纯 Rust 标准库实现
  - 三个完整示例（基础用法/进程监控/批处理）

## [2026-04-10]

### 新增
- **Python: audio_utils (33 测试，完整音频处理工具)** 🎵
  - 支持格式（WAV/AIFF/AU，纯标准库 wave/aifc/sunau）
  - 音频信息提取（格式/采样率/声道数/时长/元数据）
  - 文件读写（安全读写，自动创建目录，原子写入）
  - 音量调整（放大/衰减/静音，audioop.mul）
  - 淡入淡出（线性渐变效果，手动实现）
  - 音频拼接（多文件顺序拼接，参数一致性检查）
  - 片段提取（任意时间段裁剪）
  - 声道转换（立体声转单声道，分离左右声道）
  - 音频反转（倒放效果，audioop.reverse）
  - 波形生成（正弦波/方波/锯齿波，多采样率支持）
  - 静音检测（阈值检测，返回时间段列表）
  - 峰值检测（RMS/峰值振幅计算）
  - 音频标准化（自动增益到目标峰值）
  - 便捷函数（create_tone 快速生成音调）
  - 零依赖，纯 Python 标准库实现

- **Python: html_utils (65 测试，完整 HTML 解析工具)** 🌐
  - HTML 解析（标准 html.parser，零依赖）
  - 元素查找（按标签/ID/类名/属性/文本）
  - 数据提取（链接/图片/标题/元数据）
  - HTML 清理（XSS 防护，移除危险标签和事件处理器）
  - HTML 生成（标签/链接/图片/表格/表单）
  - 格式转换（HTML 转纯文本/压缩/美化）
  - DOM 分析（标签统计/深度计算/结构验证）
  - Unicode 支持（完整国际化）
  - 线程安全（所有操作支持并发）
  - 零依赖，纯 Python 标准库实现

- **Python: rate_limit_utils (24+ 测试，完整速率限制工具)** 🚦
  - Token Bucket（令牌桶，支持突发流量）
  - Sliding Window Counter（滑动窗口计数器，平衡精度和性能）
  - Sliding Window Log（滑动窗口日志，精确限流）
  - Fixed Window Counter（固定窗口，简单高效）
  - 多 Key 限流（按用户/IP/API Key 独立限流）
  - 装饰器支持（@rate_limit 一键限流）
  - 严格模式（@rate_limit_strict 超限抛异常）
  - 上下文管理器（rate_limit_context）
  - 线程安全（所有操作支持并发）
  - 零依赖，纯 Python 标准库实现

- **Python: encryption_utils (62 测试，完整加密安全工具)** 🔐
  - 哈希函数（SHA256/SHA512/MD5/BLAKE2 等 9 种算法）
  - 文件哈希（高效分块读取大文件）
  - 密码哈希（PBKDF2 安全存储，100000 次迭代）
  - HMAC 签名（消息认证码，防篡改）
  - XOR 加密（教育用途对称加密）
  - 替换密码（经典密码学教学）
  - Base64 编码（标准及 URL 安全）
  - 令牌生成（API 密钥、会话 ID、安全令牌）
  - 校验和（CRC32/Adler32）
  - 一次一密（OTP，理论不可破解）
  - 密钥派生（PBKDF2）
  - 安全比较（防时序攻击）
  - 哈希链（数据完整性验证）
  - SecureString（安全字符串处理）
  - 零依赖，纯 Python 标准库实现

- **Python: config_utils (28 测试，完整配置管理工具)** ⚙️
  - 多格式支持（Key-Value/JSON/INI/.env）
  - 环境变量替换（${VAR}/$VAR/${VAR:-default}）
  - Schema 验证（类型/必填/范围/正则/选项）
  - 类型转换（int/float/bool/list/dict）
  - 嵌套配置（点号访问 database.host）
  - 不可变配置（freeze/immutable 模式）
  - 预定义 Schema（DATABASE/SERVER/LOGGING）
  - 零依赖，纯 Python 标准库实现

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

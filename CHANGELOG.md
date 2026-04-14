# AllToolkit 更新日志

## [2026-04-14]

### 新增
- **Python: bloom_filter_utils (99 单元测试，完整布隆过滤器工具)** 🔍
  - 标准布隆过滤器 (BloomFilter) - 高效空间利用，无假阴性
  - 可扩展布隆过滤器 (ScalableBloomFilter) - 自动扩容，适应未知规模
  - 计数布隆过滤器 (CountingBloomFilter) - 支持删除操作和计数估计
  - 多种哈希函数 (MurmurHash3/FNV-1a/DJB2/SHA-256)
  - 紧凑 BitArray 实现（高效位操作）
  - 自动计算最优参数（位数组大小/哈希函数数量）
  - 完整序列化/反序列化（to_bytes/from_bytes）
  - 文件持久化（save/load）
  - 过滤器操作（union/intersect）
  - 统计信息和分析工具
  - 构建器模式（流畅 API）
  - 内存使用估算工具
  - 哈希函数性能对比工具
  - 14 个完整示例（基础/去重/缓存过滤/爬虫/数据库优化等）
  - 零外部依赖，纯 Python 标准库实现

## [2026-04-14]

### 新增
- **Rust: env_utils (11 单元测试，零依赖环境变量工具)** 🌍
  - 从 `.env` 文件加载环境变量
  - 多类型解析：String, i16, i32, i64, u16, u32, u64, usize, f32, f64, bool
  - 布尔值智能解析（支持 true/false/1/0/yes/no/on/off）
  - 默认值支持（get_env_or）
  - 必需变量验证（require_env, validate_required）
  - 列表解析（逗号分隔字符串转 Vec）
  - 键值对映射（解析为 HashMap）
  - 环境变量设置/删除/检查
  - 获取所有环境变量
  - 完整错误处理（EnvError 枚举）
  - 3 个完整示例（basic/dotenv/validation）

## [2026-04-14]

### 新增
- **Go: set_utils (30+ 测试，完整泛型集合工具)** 📦
  - 泛型 Set 类型（支持任意可比较类型）
  - 集合创建（空集合/从切片创建）
  - 基本操作（添加/删除/包含检查/大小/清空）
  - 集合运算（并集/交集/差集/对称差集）
  - 子集判断（子集/超集/真子集/真超集/相等/不相交）
  - 函数式操作（过滤/映射/遍历/任意/全部）
  - 切片工具（去重/包含检查/多切片并集/交集/差集）
  - 统计函数（元素计数/最频繁元素/最少出现元素）
  - 零外部依赖，Go 1.18+ 泛型支持
  - 完整示例（10+ 使用场景演示）
  - 基准测试（Add/Contains/Union 性能测试）

## [2026-04-14]

### 新增
- **Go: uuid_utils (50+ 测试，完整 UUID 工具)** 🔑
  - UUID 生成（V3 MD5/V4 随机/V5 SHA-1）
  - UUID 解析（标准格式/无连字符/带括号/URN 格式）
  - UUID 属性（版本检测/变体检测/空值检查/有效性验证）
  - 字符串格式（标准/无连字符/URN/短格式/大小写）
  - JSON 序列化（MarshalText/UnmarshalText）
  - 二进制序列化（MarshalBinary/UnmarshalBinary）
  - UUID 比较（相等判断/字典序比较）
  - 集合操作（排序/去重/包含/索引/删除/过滤/映射）
  - 批量生成（GenerateV4Batch）
  - 带前缀生成器（Generator 类）
  - UUID 分析（版本分布/变体分布统计）
  - 零外部依赖，纯 Go 标准库实现
  - 完整示例（10 个使用场景演示）
  - 边界测试（空 UUID/无效输入/格式边界）

## [2026-04-13]

### 新增
- **Python: lexer_utils (78 测试，完整词法分析器工具)** 🔤
  - Token 类型定义（字符串匹配/正则匹配/优先级设置）
  - 词法分析器构建（Lexer/LexerBuilder 流畅 API）
  - 流式处理（迭代器模式/TokenStream 导航）
  - 位置跟踪（行号/列号/字符索引）
  - 错误处理（自定义处理器/恢复继续）
  - Token 类别（LITERAL/KEYWORD/IDENTIFIER/OPERATOR/PUNCTUATION/WHITESPACE/COMMENT/EOF）
  - 预构建分词器（simple_tokenize/tokenize_code/tokenize_json/tokenize_math）
  - Token 工具（统计/过滤/序列化/查找/匹配序列）
  - 回调转换（自动转换 token 值类型）
  - 零依赖，纯 Python 标准库实现
  - 完整示例（13 个使用场景演示）
  - Python 3.6+ 兼容

- **Python: graph_utils (74 测试，完整图算法工具)** 📊
  - 图表示（邻接表/邻接矩阵，有向图/无向图）
  - 图遍历（BFS 广度优先/DFS 深度优先，递归/迭代版本）
  - 最短路径（Dijkstra/Bellman-Ford/Floyd-Warshall）
  - 最小生成树（Kruskal/Prim 算法）
  - 拓扑排序（Kahn 算法/DFS 算法）
  - 连通分量（无向图连通分量/有向图强连通分量 Kosaraju）
  - 环检测（环存在检测/环路径查找）
  - 二分图检测（BFS 着色法）
  - 欧拉路径（Hierholzer 算法/欧拉路径/欧拉回路）
  - 图分析（割点 Tarjan/桥检测/孤立顶点）
  - 图工具（图统计信息/反转图/树检测/最短路径树）
  - 零依赖，纯 Python 标准库实现
  - 完整示例（15 个使用场景演示）
  - 边界测试（空图/单顶点/自环/数字顶点/元组顶点）

- **Python: diff_utils (64 测试，完整文本差异比较工具)** 📝
  - 差异比较（行级/字符级/词级差异分析）
  - 相似度算法（Levenshtein/Jaccard/Cosine/Damerau-Levenshtein）
  - 格式化输出（Unified Diff/Context Diff/彩色终端/HTML）
  - 合并冲突检测（三方合并冲突识别与标记）
  - 补丁生成（标准 Git 风格补丁文件生成）
  - 差异统计（详细变更统计/相似度分析/变更摘要）
  - 工具函数（最长公共子序列/相似字符串查找/差异高亮）
  - 零依赖，纯 Python 标准库实现
  - 完整示例（基础用法/高级功能演示）
  - Unicode 支持（完整中文等 Unicode 字符处理）

- **Python: math_utils (75 测试，完整数学运算工具)** 🔢
  - 基础运算（阶乘/斐波那契/GCD/LCM/幂运算/根）
  - 数论工具（素数检测/素数生成/质因数分解/因数/欧拉函数/完全数）
  - 几何计算（距离/面积/体积/周长/角度）
  - 统计扩展（均值/中位数/众数/方差/标准差/百分位数/相关系数）
  - 数值处理（四舍五入/取整/截断/范围限制/百分比）
  - 向量运算（加减/数乘/点积/叉积/模长/归一化）
  - 序列生成（等差数列/等比数列/linspace/浮点数范围）
  - 数值检查（奇偶/整数/幂次/完全平方/阿姆斯特朗数/回文数）
  - 随机函数（随机整数/浮点数/选择/抽样/打乱）
  - 零依赖，纯 Python 标准库实现
  - 完整示例（9 个使用场景演示）
  - 边界测试（负数/零向量/空数据/数值边界）

- **Python: state_machine_utils (50+ 测试，完整状态机工具)** 🔄
  - 状态定义（状态类/转换规则/条件验证）
  - 进入/退出回调（状态生命周期管理）
  - 状态历史（完整转换记录/时间戳）
  - 异步支持（异步转换/异步回调）
  - 持久化（JSON 序列化/状态恢复）
  - 事件驱动（事件触发转换/副作用）
  - 零依赖，纯 Python 标准库实现
  - 完整示例（订单状态/工作流/游戏角色）

- **Swift: http_utils (80+ 测试，完整 HTTP 客户端工具)** 🌐
  - 全 HTTP 方法支持（GET/POST/PUT/PATCH/DELETE/HEAD/OPTIONS）
  - JSON 编码/解码（自动 Codable 支持）
  - 认证助手（Bearer Token、Basic Auth）
  - URL 构建器（查询参数链式构建）
  - 表单编码（URL-encoded、Multipart）
  - 文件上传（Multipart 文件上传支持）
  - 响应处理（状态码分类、字符串/JSON 解析）
  - 错误处理（超时/网络/HTTP 错误类型）
  - 可配置超时（请求级别超时控制）
  - 默认请求头（客户端级别全局配置）
  - 自定义 URLSession 配置支持
  - 零外部依赖，纯 Swift Foundation 实现
  - 完整示例（18 个实际使用场景）
  - 边界测试（状态码边界/空数据/Unicode/错误处理）

## [2026-04-12]

### 新增
- **ArkTS: array_utils (130+ 测试，完整数组/集合工具)** 📦
  - 空值检查（isEmpty/isNotEmpty/size）
  - 安全访问（first/last/get/getOrThrow，支持负索引）
  - 查找与过滤（find/findIndex/contains/filter/filterNull）
  - 转换（map/mapNotNull/flatMap/flatten/flattenDeep）
  - 排序（sort/sortBy/sortByDesc/reverse/shuffle/isSorted）
  - 集合操作（unique/union/intersection/difference/duplicates）
  - 分组（groupBy/partition/chunk/splitAt）
  - 切片（take/takeLast/takeWhile/drop/dropWhile/slice）
  - 聚合（sum/average/min/max/count/countBy）
  - 随机（randomElement/randomElements/sample）
  - 修改（insert/removeAt/append/prepend/concat/updateAt）
  - 比较（equals/equalsIgnoreOrder/startsWith/endsWith）
  - 生成（range/fill/fillFn）
  - 工具（forEach/reduce/every/some/join/zip/unzip/rotate/interleave）
  - 类 API（ArrayUtils 静态方法）
  - 零依赖，纯 ArkTS 标准库实现
  - 完整示例（16 个 HarmonyOS 应用场景）
  - 边界值测试（空数组/null/undefined/负索引/越界）

- **Python: process_utils (61 测试，完整进程管理工具)** ⚙️
  - 命令执行（run/run_shell，支持超时控制）
  - 流式输出（run_streaming，实时捕获 stdout/stderr）
  - 进程管理（ProcessManager，启动/监控/终止进程）
  - 环境变量（get_env/set_env/unset_env/get_env_snapshot）
  - 进程池（WorkerPool，多进程并行执行任务）
  - 命令检查（exists/which，检查命令是否存在）
  - 进程信息（get_pid/get_ppid/get_cwd）
  - 配置系统（ProcessConfig，超时/工作目录/环境变量/优先级）
  - 状态枚举（ProcessState：running/stopped/completed/failed/timeout）
  - 优先级枚举（ProcessPriority：VERY_HIGH 到 VERY_LOW）
  - 结果数据类（ProcessResult：returncode/stdout/stderr/execution_time）
  - 异步支持（map_async/apply_async，带回调函数）
  - 上下文管理器（with WorkerPool 自动资源清理）
  - 零依赖，纯 Python 标准库实现（subprocess/multiprocessing/threading）
  - 完整示例（14 个使用场景演示）
  - 边界测试（超时/Unicode/多行输出/并发执行/错误处理）

- **Python: qr_utils (21 测试，完整二维码生成工具)** 📱
  - QR 码矩阵生成（版本 1-10，自动选择版本）
  - 多种纠错级别（L/M/Q/H，7%-30% 恢复能力）
  - ASCII 艺术渲染（终端预览/日志输出）
  - Emoji 艺术渲染（社交媒体分享）
  - PNG 图片生成（纯 Python PNG 编码，零依赖）
  - Data URL 生成（直接嵌入 HTML）
  - 多种数据编码（URL/vCard/WiFi/Email/SMS/文本）
  - 批量生成支持（一次性生成多个 QR 码）
  - 数据验证和统计（格式验证/矩阵分析）
  - 自定义颜色（支持颜色名和#RRGGBB）
  - 零依赖，纯 Python 标准库实现
  - 完整示例（11 个使用场景演示）
  - 边界测试（超长数据/特殊字符/Unicode/Emoji）

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

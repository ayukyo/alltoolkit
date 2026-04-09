# AllToolkit - TypeScript 工具模块集合 📘

**零依赖的 TypeScript 工具函数集合 - 生产就绪，开箱即用**

---

## 📦 可用模块

| 模块 | 描述 | 状态 |
|------|------|------|
| `crypto_utils` | 加密解密工具（哈希、Base64、UUID） | ✅ |
| `csv_utils` | CSV 文件处理（读取/写入/过滤/排序） | ✅ |
| **`date_utils`** | **日期时间处理（格式化/解析/运算/比较/相对时间）** | ✅ **NEW** |
| `file_utils` | 文件操作工具 | ✅ |
| `http_utils` | HTTP 请求工具 | ✅ |
| `queue_utils` | 队列实现（FIFO、优先级队列） | ✅ |
| `template_utils` | 模板引擎工具 | ✅ |
| `uuid_utils` | UUID 生成和验证 | ✅ |

---

## 🚀 快速开始

### 安装

无需安装！直接复制模块到你的项目：

```bash
# 复制单个模块
cp -r AllToolkit/TypeScript/date_utils your_project/

# 或克隆整个仓库
git clone https://github.com/ayukyo/alltoolkit.git
```

### 使用示例

```typescript
// 日期工具
import { DateUtils } from './date_utils/mod.ts';

const formatted = DateUtils.formatDate(new Date(), 'YYYY-MM-DD');
const nextWeek = DateUtils.addDays(new Date(), 7);
const isWeekend = DateUtils.isWeekend(new Date());

// UUID 工具
import { UuidUtils } from './uuid_utils/mod.ts';

const uuid = UuidUtils.v4();
const isValid = UuidUtils.isValid(uuid);

// CSV 工具
import { CsvUtils } from './csv_utils/mod.ts';

const data = CsvUtils.parse('name,age\nAlice,25\nBob,30');
const csv = CsvUtils.stringify(data);
```

---

## 📁 模块结构

每个模块遵循统一结构：

```
module_name/
├── mod.ts              # 主要实现
├── module_name_test.ts # 测试套件
├── README.md           # 详细文档
├── verify.js           # 验证脚本
└── examples/           # 使用示例
    ├── basic_usage.ts
    └── advanced_example.ts
```

---

## 🧪 运行测试

```bash
# 使用 Deno
cd date_utils
deno test date_utils_test.ts

# 使用 Bun
bun test date_utils_test.ts

# 使用 Node.js + ts-node
npx ts-node date_utils_test.node.ts

# 验证模块结构
node verify.js
```

---

## 📊 特性对比

| 特性 | date_utils | uuid_utils | crypto_utils |
|------|------------|------------|--------------|
| 零依赖 | ✅ | ✅ | ✅ |
| TypeScript | ✅ | ✅ | ✅ |
| 浏览器支持 | ✅ | ✅ | ✅ |
| Node.js 支持 | ✅ | ✅ | ✅ |
| Deno 支持 | ✅ | ✅ | ✅ |
| Bun 支持 | ✅ | ✅ | ✅ |

---

## 🔧 配置

### TypeScript 配置

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true
  }
}
```

### Deno 配置

```json
{
  "compilerOptions": {
    "strict": true
  }
}
```

---

## 📄 许可证

MIT License

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

仓库：https://github.com/ayukyo/alltoolkit

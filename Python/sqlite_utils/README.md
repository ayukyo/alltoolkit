# AllToolkit - Python SQLite Utilities 🐍

**零依赖、生产就绪的 SQLite 数据库工具模块**

支持连接管理、查询构建、CRUD 操作、事务处理、Schema 管理和数据导入/导出。完全使用 Python 标准库构建。

---

## 📦 快速开始

### 安装

无需安装！直接复制模块到你的项目：

```bash
# 复制单个模块
cp AllToolkit/Python/sqlite_utils/mod.py your_project/
```

### 基础使用

```python
from mod import Database, Table, Column, connect, create_in_memory

# 方式 1: 连接文件数据库
db = Database("myapp.db")
db.connect()

# 方式 2: 使用便捷函数
db = connect("myapp.db")

# 方式 3: 内存数据库（测试用）
db = create_in_memory()

# 使用上下文管理器（自动关闭连接）
with Database("myapp.db") as db:
    # 你的操作
    pass
```

---

## 📖 功能概览

| 功能 | 描述 | 状态 |
|------|------|------|
| **Schema 管理** | 创建/删除表、添加列、创建索引 | ✅ |
| **CRUD 操作** | 插入、查询、更新、删除 | ✅ |
| **查询构建器** | 流式 SQL 构建 | ✅ |
| **事务支持** | 自动提交/回滚 | ✅ |
| **连接池** | 线程安全连接池 | ✅ |
| **数据导出** | JSON/CSV 导出 | ✅ |
| **数据导入** | JSON/CSV 导入 | ✅ |
| **备份恢复** | 数据库备份与恢复 | ✅ |
| **工具函数** | 统计、大小、版本查询 | ✅ |

---

## 🚀 使用示例

### 定义表和列

```python
from mod import Table, Column

# 定义列
id_col = Column("id", "INTEGER", primary_key=True)
name_col = Column("name", "TEXT", nullable=False)
email_col = Column("email", "TEXT", unique=True)
age_col = Column("age", "INTEGER", default=0)

# 定义表
users_table = Table(
    name="users",
    columns=[id_col, name_col, email_col, age_col],
    unique_constraints=[["name", "email"]]  # 复合唯一约束
)

# 创建表
db.create_table(users_table)
```

### 插入数据

```python
# 插入单行
user_id = db.insert("users", {
    "name": "Alice",
    "email": "alice@example.com",
    "age": 25
})

# 插入多行
users = [
    {"name": "Bob", "email": "bob@example.com", "age": 30},
    {"name": "Charlie", "email": "charlie@example.com", "age": 35},
]
ids = db.insert_many("users", users)

# 插入或替换（Upsert）
db.insert_or_replace("users", {
    "id": 1,
    "name": "Updated",
    "email": "updated@example.com"
})
```

### 查询数据

```python
# 查询所有
result = db.select("users")
for row in result.to_dicts():
    print(row)

# 指定列
result = db.select("users", columns=["id", "name"])

# 条件查询
result = db.select(
    "users",
    where="age > ?",
    params=(18,),
    order_by="age DESC",
    limit=10
)

# 查找单个
user = db.find_one("users", "email = ?", ("alice@example.com",))
user = db.find_by_id("users", 1)

# 计数和存在检查
count = db.count("users", "age > ?", (18,))
exists = db.exists("users", "id = ?", (1,))
```

### 更新和删除

```python
# 更新
rows = db.update(
    "users",
    {"age": 26, "name": "Alice Updated"},
    "id = ?",
    (user_id,)
)

# 删除
rows = db.delete("users", "id = ?", (user_id,))
rows = db.delete_by_id("users", user_id)
```

### 使用查询构建器

```python
from mod import QueryBuilder

# 获取构建器
qb = db.table("users")

# 构建复杂查询
sql, params = (qb
    .select("id", "name", "email")
    .where("age > ?", 18)
    .where_eq("status", "active")
    .where_in("role", ["admin", "user"])
    .order_by("name")
    .limit(10)
    .offset(0)
    .build_select())

result = db.query(sql, *params)

# 构建 DELETE
sql, params = qb.where_eq("id", 1).build_delete()
db.execute(sql, *params)

# 构建 UPDATE
sql, params = qb.where_eq("id", 1).build_update({"name": "New Name"})
db.execute(sql, *params)
```

### 事务处理

```python
# 使用上下文管理器（推荐）
try:
    with db.transaction():
        db.insert("users", {"name": "A", "email": "a@example.com"})
        db.insert("users", {"name": "B", "email": "b@example.com"})
        # 自动提交，出错自动回滚
except Exception as e:
    print(f"Transaction failed: {e}")

# 手动控制
db.begin()
try:
    db.insert(...)
    db.update(...)
    db.commit()
except:
    db.rollback()
    raise
```

### 连接池（多线程）

```python
# 启用连接池
db = Database("myapp.db")
db.connect(use_pool=True, max_connections=10)

# 线程安全操作
import threading

def worker(db, worker_id):
    for i in range(100):
        db.insert("logs", {"worker": worker_id, "seq": i})

threads = [threading.Thread(target=worker, args=(db, i)) for i in range(5)]
for t in threads:
    t.start()
for t in threads:
    t.join()

db.close()
```

### 数据导出

```python
# 导出为 JSON
count = db.export_to_json("users", "users.json")
count = db.export_to_json("users", "active_users.json", where="status = 'active'")

# 导出为 CSV
count = db.export_to_csv("users", "users.csv")
```

### 数据导入

```python
# 从 JSON 导入
count = db.import_from_json("users", "users.json")

# 从 CSV 导入
count = db.import_from_csv("users", "users.csv", skip_header=True)
```

### 备份和恢复

```python
# 创建备份
db.backup("backups/myapp_backup_20260410.db")

# 恢复（会关闭当前连接并替换数据库）
db.restore("backups/myapp_backup_20260410.db")
```

### 数据库信息

```python
# 获取所有表
tables = db.get_tables()

# 检查表是否存在
exists = db.table_exists("users")

# 获取表结构
info = db.get_table_info("users")
for col in info:
    print(f"{col['name']}: {col['type']}")

# 数据库大小
size = db.get_size()  # 字节
size_str = db.get_size_formatted()  # "1.5 MB"

# SQLite 版本
version = db.get_version()

# 完整统计
stats = db.get_stats()
print(stats)
# {
#   "path": "myapp.db",
#   "size": 1572864,
#   "size_formatted": "1.50 MB",
#   "version": "3.40.0",
#   "tables": ["users", "posts"],
#   "table_count": 2
# }

# 优化
db.vacuum()   # 回收空间
db.analyze()  # 更新统计
```

### 添加列和索引

```python
# 添加列
db.add_column("users", Column("phone", "TEXT"))
db.add_column("users", Column("active", "INTEGER", default=1))

# 创建索引
db.create_index("users", ["email"])
db.create_index("users", ["name", "age"], index_name="idx_users_name_age")
db.create_index("users", ["email"], unique=True)  # 唯一索引
```

### 原始 SQL 执行

```python
# 查询
result = db.query("SELECT * FROM users WHERE age > ?", 18)
for row in result.to_dicts():
    print(row)

# 标量查询
count = db.query_scalar("SELECT COUNT(*) FROM users")

# 单行字典
user = db.query_dict("SELECT * FROM users WHERE id = ?", 1)

# 多行字典
users = db.query_dicts("SELECT * FROM users ORDER BY name")

# 执行语句
rows = db.execute("DELETE FROM logs WHERE created_at < ?", (cutoff_date,))

# 批量执行
params = [
    ("user1", "email1@example.com"),
    ("user2", "email2@example.com"),
]
rows = db.executemany(
    "INSERT INTO users (name, email) VALUES (?, ?)",
    params
)
```

---

## 📁 模块结构

```
sqlite_utils/
├── mod.py                      # 主要实现
├── sqlite_utils_test.py        # 测试套件
├── README.md                   # 文档
└── examples/                   # 使用示例
    ├── basic_usage.py
    ├── advanced_example.py
    └── multi_thread_example.py
```

---

## 🧪 运行测试

```bash
cd sqlite_utils
python sqlite_utils_test.py
```

### 测试覆盖

- ✅ Column 和 Table 定义
- ✅ QueryResult 转换
- ✅ QueryBuilder 所有方法
- ✅ CRUD 操作
- ✅ 事务提交/回滚
- ✅ 连接池和线程安全
- ✅ JSON/CSV 导入导出
- ✅ 备份恢复
- ✅ Unicode 和特殊字符
- ✅ 边界情况处理

---

## 🔧 配置选项

```python
from mod import SQLiteConfig, Database

config = SQLiteConfig(
    timeout=30.0,              # 锁等待超时（秒）
    isolation_level="DEFERRED", # 隔离级别
    enable_foreign_keys=True,   # 启用外键约束
    enable_wal_mode=True        # 启用 WAL 模式
)

db = Database("myapp.db", config=config)
db.connect()
```

---

## ⚠️ 注意事项

1. **线程安全**: 使用连接池时确保 `use_pool=True`
2. **外键约束**: SQLite 默认不启用外键，模块会自动启用
3. **WAL 模式**: 提高并发性能，但会生成额外的 `-wal` 和 `-shm` 文件
4. **内存数据库**: 使用 `:memory:` 或 `create_in_memory()`，关闭后数据丢失
5. **备份**: 备份前确保没有未提交的事务

---

## 🔒 安全建议

1. **参数化查询**: 始终使用参数化防止 SQL 注入
   ```python
   # ✅ 正确
   db.find_one("users", "email = ?", (email,))
   
   # ❌ 错误
   db.find_one("users", f"email = '{email}'")
   ```

2. **输入验证**: 在插入前验证数据
3. **权限控制**: 数据库文件设置适当的文件系统权限
4. **敏感数据**: 密码等敏感数据应加密存储

---

## 📊 性能提示

1. **批量操作**: 使用 `insert_many` 而非多次 `insert`
2. **事务**: 大量操作时包裹在事务中
3. **索引**: 为常用查询条件创建索引
4. **连接池**: 多线程应用使用连接池
5. **WAL 模式**: 高并发场景启用 WAL

```python
# 批量插入（快）
data = [{"name": f"user{i}"} for i in range(1000)]
db.insert_many("users", data)

# 事务包裹（更快）
with db.transaction():
    for item in data:
        db.insert("users", item)
```

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

仓库：https://github.com/ayukyo/alltoolkit

---

## 📄 许可证

MIT License

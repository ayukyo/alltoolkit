# Database Utils - Python 数据库工具模块

AllToolkit 的 Python 数据库工具模块，提供统一的 SQLite、CSV、JSON 数据存储接口。

## 📦 功能特性

### SQLite 数据库
- **连接池管理** - 支持多线程并发访问
- **事务支持** - 自动提交/回滚
- **表操作** - 创建、删除、查询表结构
- **CRUD 操作** - 插入、查询、更新、删除
- **批量操作** - 高效批量插入
- **原始 SQL** - 支持执行任意 SQL 语句

### CSV 文件数据库
- **读写操作** - 完整的 CSV 文件操作
- **追加模式** - 高效追加数据
- **条件查询** - 支持 where、columns、order、limit
- **更新删除** - 基于条件的数据修改

### JSON 文件数据库
- **结构化存储** - 支持列表和字典
- **条件查询** - 支持 where 过滤
- **增量更新** - 插入、更新、删除操作
- **Unicode 支持** - 完整的多语言支持

### 数据转换
- **CSV ↔ JSON** - 格式互转
- **导入导出** - 统一的数据交换接口

## 🚀 快速开始

### 安装

无需安装，直接使用：

```python
import sys
sys.path.insert(0, '/path/to/AllToolkit/Python/database_utils')
from mod import SQLiteDatabase, CSVDatabase, JSONDatabase
```

### 基本用法

#### SQLite 示例

```python
from mod import SQLiteDatabase

# 创建数据库连接
db = SQLiteDatabase("example.db")

# 创建表
db.create_table("users", {
    "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
    "name": "TEXT NOT NULL",
    "email": "TEXT UNIQUE",
    "age": "INTEGER"
})

# 插入数据
user_id = db.insert("users", {
    "name": "Alice",
    "email": "alice@example.com",
    "age": 30
})

# 批量插入
db.insert_many("users", [
    {"name": "Bob", "email": "bob@example.com", "age": 25},
    {"name": "Charlie", "email": "charlie@example.com", "age": 35}
])

# 查询数据
all_users = db.query("users")
alice = db.query("users", where={"name": "Alice"})
young_users = db.query("users", where={"age": 25})

# 更新数据
db.update("users", {"age": 31}, where={"name": "Alice"})

# 删除数据
db.delete("users", where={"id": 1})

# 使用事务
with db.transaction() as conn:
    db.insert("users", {"name": "Eve", "email": "eve@example.com"}, _conn=conn)
    db.insert("users", {"name": "Frank", "email": "frank@example.com"}, _conn=conn)
# 自动提交，异常时自动回滚

# 关闭连接
db.close()
```

#### CSV 示例

```python
from mod import CSVDatabase

# 创建 CSV 数据库
csv_db = CSVDatabase("data.csv")

# 写入数据
data = [
    {"product": "Laptop", "price": "999.99", "stock": "50"},
    {"product": "Mouse", "price": "29.99", "stock": "200"}
]
csv_db.write(data)

# 追加数据
csv_db.append({"product": "Keyboard", "price": "79.99", "stock": "150"})

# 查询数据
all_products = csv_db.read()
expensive = [p for p in csv_db.query() if float(p['price']) > 100]

# 更新数据
csv_db.update({"price": "24.99"}, where={"product": "Mouse"})

# 删除数据
csv_db.delete(where={"product": "Keyboard"})

csv_db.close()
```

#### JSON 示例

```python
from mod import JSONDatabase

# 创建 JSON 数据库
json_db = JSONDatabase("config.json")

# 写入配置
config = {
    "app_name": "MyApp",
    "version": "1.0.0",
    "settings": {
        "debug": True,
        "max_connections": 100
    }
}
json_db.write(config)

# 读取配置
loaded = json_db.read()
print(loaded["app_name"])

# 数组数据
users = [
    {"id": 1, "name": "Alice", "active": True},
    {"id": 2, "name": "Bob", "active": False}
]
json_db.write(users)

# 查询
active_users = json_db.query(where={"active": "True"})

# 插入
json_db.insert({"id": 3, "name": "Charlie", "active": True})

json_db.close()
```

## 📁 文件结构

```
database_utils/
├── mod.py                      # 主模块（所有工具函数）
├── database_utils_test.py      # 测试套件（80+ 个测试）
├── README.md                   # 本文档
└── examples/
    └── usage_examples.py       # 使用示例
```

## ✅ 测试

运行测试套件：

```bash
cd /path/to/AllToolkit/Python/database_utils
python3 database_utils_test.py
```

预期输出：
```
============================================================
  SQLite Database Tests
============================================================
  ✓ create_table creates table
  ✓ table_exists returns True for existing table
  ...
============================================================
Tests: 80+ | Passed: 80+ | Failed: 0
🎉 All tests passed!
============================================================
```

## 📖 示例

运行使用示例：

```bash
cd /path/to/AllToolkit/Python/database_utils/examples
python3 usage_examples.py
```

## 💡 实际应用场景

### 1. 简单缓存系统

```python
from mod import JSONDatabase

class SimpleCache:
    def __init__(self, cache_file="cache.json"):
        self.cache = JSONDatabase(cache_file)
    
    def get(self, key):
        data = self.cache.read()
        return data.get(key)
    
    def set(self, key, value, ttl=3600):
        data = self.cache.read() or {}
        data[key] = {
            "value": value,
            "timestamp": time.time(),
            "ttl": ttl
        }
        self.cache.write(data)
    
    def is_valid(self, key):
        data = self.cache.read()
        if key not in data:
            return False
        entry = data[key]
        return time.time() - entry["timestamp"] < entry["ttl"]
```

### 2. 配置管理

```python
from mod import JSONDatabase

class ConfigManager:
    def __init__(self, config_file="config.json"):
        self.config = JSONDatabase(config_file)
    
    def get(self, *keys, default=None):
        data = self.config.read()
        for key in keys:
            if isinstance(data, dict):
                data = data.get(key, default)
            else:
                return default
        return data
    
    def set(self, value, *keys):
        data = self.config.read() or {}
        current = data
        for key in keys[:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]
        current[keys[-1]] = value
        self.config.write(data)
```

### 3. 事件日志

```python
from mod import CSVDatabase

class EventLogger:
    def __init__(self, log_file="events.csv"):
        self.log = CSVDatabase(log_file)
    
    def log(self, level, message, **extra):
        entry = {
            "timestamp": datetime.now().isoformat(),
            "level": level,
            "message": message,
            **extra
        }
        self.log.append(entry)
    
    def get_errors(self):
        return self.log.query(where={"level": "ERROR"})
    
    def get_recent(self, limit=100):
        return self.log.query(order_by="-timestamp", limit=limit)
```

### 4. 产品库存管理

```python
from mod import SQLiteDatabase

class InventoryManager:
    def __init__(self, db_path="inventory.db"):
        self.db = SQLiteDatabase(db_path)
        self._init_db()
    
    def _init_db(self):
        self.db.create_table("products", {
            "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
            "sku": "TEXT UNIQUE",
            "name": "TEXT",
            "price": "REAL",
            "quantity": "INTEGER",
            "category": "TEXT"
        })
    
    def add_product(self, sku, name, price, quantity, category=""):
        return self.db.insert("products", {
            "sku": sku, "name": name, "price": price,
            "quantity": quantity, "category": category
        })
    
    def get_low_stock(self, threshold=10):
        return self.db.execute(
            f"SELECT * FROM products WHERE quantity < {threshold}"
        )
    
    def update_stock(self, sku, delta):
        with self.db.transaction() as conn:
            self.db.execute(
                "UPDATE products SET quantity = quantity + ? WHERE sku = ?",
                (delta, sku),
                _conn=conn
            )
```

### 5. 数据导出工具

```python
from mod import (
    SQLiteDatabase, export_to_csv, export_to_json,
    convert_csv_to_json
)

def export_database_to_csv(db_path, output_dir):
    """将 SQLite 数据库导出为 CSV 文件"""
    db = SQLiteDatabase(db_path)
    tables = db.get_tables()
    
    for table in tables:
        data = db.query(table)
        csv_path = os.path.join(output_dir, f"{table}.csv")
        export_to_csv(data, csv_path)
        print(f"Exported {table}: {len(data)} rows")
    
    db.close()

def migrate_csv_to_sqlite(csv_path, db_path, table_name):
    """将 CSV 数据迁移到 SQLite"""
    data = import_from_csv(csv_path)
    db = SQLiteDatabase(db_path)
    
    if data:
        columns = {k: "TEXT" for k in data[0].keys()}
        columns["id"] = "INTEGER PRIMARY KEY AUTOINCREMENT"
        db.create_table(table_name, columns)
        db.insert_many(table_name, data)
    
    db.close()
```

## 🔒 安全特性

- **参数化查询** - 防止 SQL 注入
- **事务支持** - 数据一致性保证
- **线程安全** - 连接池和锁机制
- **输入验证** - 所有函数处理 None 安全

## 📊 性能特点

- **连接池** - SQLite 连接复用
- **批量操作** - 减少数据库往返
- **流式处理** - 大文件内存友好
- **最小依赖** - 仅使用 Python 标准库

## 🔧 API 参考

### SQLiteDatabase

| 方法 | 描述 |
|------|------|
| `create_table(name, columns)` | 创建表 |
| `drop_table(name)` | 删除表 |
| `insert(table, data)` | 插入单行 |
| `insert_many(table, data_list)` | 批量插入 |
| `query(table, columns, where, order_by, limit)` | 查询 |
| `update(table, data, where)` | 更新 |
| `delete(table, where)` | 删除 |
| `execute(sql, params)` | 执行原始 SQL |
| `get_table_info(table)` | 获取表结构 |
| `table_exists(table)` | 检查表是否存在 |
| `get_tables()` | 获取所有表名 |
| `transaction()` | 事务上下文管理器 |

### CSVDatabase

| 方法 | 描述 |
|------|------|
| `read()` | 读取所有行 |
| `write(data)` | 写入（覆盖） |
| `append(data)` | 追加 |
| `query(columns, where, order_by, limit)` | 查询 |
| `update(data, where)` | 更新 |
| `delete(where)` | 删除 |

### JSONDatabase

| 方法 | 描述 |
|------|------|
| `read()` | 读取数据 |
| `write(data)` | 写入数据 |
| `insert(data)` | 插入 |
| `query(where, limit)` | 查询 |
| `update(data, where)` | 更新 |
| `delete(where)` | 删除 |

### 工具函数

| 函数 | 描述 |
|------|------|
| `export_to_csv(data, path)` | 导出为 CSV |
| `import_from_csv(path)` | 从 CSV 导入 |
| `export_to_json(data, path)` | 导出为 JSON |
| `import_from_json(path)` | 从 JSON 导入 |
| `convert_csv_to_json(csv, json)` | CSV 转 JSON |
| `convert_json_to_csv(json, csv)` | JSON 转 CSV |
| `sqlite_connect(path)` | 创建 SQLite 连接 |
| `csv_connect(path)` | 创建 CSV 连接 |
| `json_connect(path)` | 创建 JSON 连接 |

## 📝 许可证

MIT License - 详见 AllToolkit 主项目 LICENSE 文件

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📞 支持

如有问题，请在 AllToolkit 仓库提交 Issue。

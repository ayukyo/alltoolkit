"""
AllToolkit - SQLite Utils Basic Usage Examples

演示 sqlite_utils 模块的基础用法。

Run from sqlite_utils directory:
    python examples/basic_usage.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import Database, Table, Column, connect, create_in_memory


def example_basic_crud():
    """基础 CRUD 操作示例。"""
    print("=" * 60)
    print("基础 CRUD 操作示例")
    print("=" * 60)
    
    # 创建内存数据库
    db = create_in_memory()
    
    # 定义并创建表
    users_table = Table(
        name="users",
        columns=[
            Column("id", "INTEGER", primary_key=True),
            Column("name", "TEXT", nullable=False),
            Column("email", "TEXT", unique=True),
            Column("age", "INTEGER", default=0),
        ]
    )
    db.create_table(users_table)
    print("✅ 创建 users 表")
    
    # 插入数据
    user_id = db.insert("users", {
        "name": "Alice",
        "email": "alice@example.com",
        "age": 25
    })
    print(f"✅ 插入用户，ID={user_id}")
    
    # 批量插入
    users = [
        {"name": "Bob", "email": "bob@example.com", "age": 30},
        {"name": "Charlie", "email": "charlie@example.com", "age": 35},
        {"name": "Diana", "email": "diana@example.com", "age": 28},
    ]
    ids = db.insert_many("users", users)
    print(f"✅ 批量插入 {len(ids)} 个用户")
    
    # 查询所有
    result = db.select("users")
    print(f"\n📋 所有用户 ({result.row_count} 人):")
    for row in result.to_dicts():
        print(f"   {row['id']}. {row['name']} ({row['age']}岁) - {row['email']}")
    
    # 条件查询
    result = db.select("users", where="age > ?", params=(30,))
    print(f"\n📋 年龄大于 30 岁的用户:")
    for row in result.to_dicts():
        print(f"   {row['name']} ({row['age']}岁)")
    
    # 查找单个
    user = db.find_by_id("users", 1)
    print(f"\n📋 ID=1 的用户：{user['name']}")
    
    # 更新
    db.update("users", {"age": 26}, "id = ?", (user_id,))
    print(f"✅ 更新用户年龄为 26")
    
    # 计数
    count = db.count("users")
    print(f"📊 总用户数：{count}")
    
    # 删除
    db.delete_by_id("users", 2)
    print(f"✅ 删除 ID=2 的用户")
    
    # 验证删除
    count = db.count("users")
    print(f"📊 剩余用户数：{count}")
    
    db.close()
    print("\n")


def example_query_builder():
    """查询构建器示例。"""
    print("=" * 60)
    print("查询构建器示例")
    print("=" * 60)
    
    db = create_in_memory()
    
    # 创建表
    db.create_table(Table(
        name="products",
        columns=[
            Column("id", "INTEGER", primary_key=True),
            Column("name", "TEXT"),
            Column("category", "TEXT"),
            Column("price", "REAL"),
            Column("stock", "INTEGER"),
        ]
    ))
    
    # 插入测试数据
    products = [
        {"name": "Laptop", "category": "Electronics", "price": 999.99, "stock": 50},
        {"name": "Mouse", "category": "Electronics", "price": 29.99, "stock": 200},
        {"name": "Desk", "category": "Furniture", "price": 299.99, "stock": 30},
        {"name": "Chair", "category": "Furniture", "price": 199.99, "stock": 100},
        {"name": "Monitor", "category": "Electronics", "price": 399.99, "stock": 75},
    ]
    db.insert_many("products", products)
    
    # 使用查询构建器
    qb = db.table("products")
    
    # 构建复杂查询
    sql, params = (qb
        .select("name", "price", "category")
        .where("price > ?", 100)
        .where_eq("category", "Electronics")
        .order_by("price", desc=True)
        .limit(10)
        .build_select())
    
    print("📋 价格>100 的电子产品（按价格降序）:")
    result = db.query(sql, *params)
    for row in result.to_dicts():
        print(f"   {row['name']}: ¥{row['price']}")
    
    # 构建 COUNT 查询
    sql, params = (db.table("products")
        .where("stock < ?", 100)
        .build_count())
    result = db.query(sql, *params)
    print(f"\n📊 库存<100 的商品数：{result.rows[0][0]}")
    
    db.close()
    print("\n")


def example_transaction():
    """事务处理示例。"""
    print("=" * 60)
    print("事务处理示例")
    print("=" * 60)
    
    db = create_in_memory()
    
    # 创建账户表
    db.create_table(Table(
        name="accounts",
        columns=[
            Column("id", "INTEGER", primary_key=True),
            Column("name", "TEXT"),
            Column("balance", "REAL", default=0),
        ]
    ))
    
    # 初始化账户
    db.insert("accounts", {"name": "Alice", "balance": 1000})
    db.insert("accounts", {"name": "Bob", "balance": 500})
    
    def show_balances():
        result = db.select("accounts", order_by="name")
        for row in result.to_dicts():
            print(f"   {row['name']}: ¥{row['balance']}")
    
    print("初始余额:")
    show_balances()
    
    # 成功的事务：转账
    print("\n💰 执行转账：Alice -> Bob ¥200")
    try:
        with db.transaction():
            db.execute("UPDATE accounts SET balance = balance - 200 WHERE name = ?", "Alice")
            db.execute("UPDATE accounts SET balance = balance + 200 WHERE name = ?", "Bob")
        print("✅ 转账成功")
    except Exception as e:
        print(f"❌ 转账失败：{e}")
    
    print("\n转账后余额:")
    show_balances()
    
    # 失败的事务：余额不足（演示回滚）
    print("\n💰 尝试转账：Bob -> Alice ¥1000（余额不足）")
    try:
        with db.transaction():
            bob_balance = db.query_scalar("SELECT balance FROM accounts WHERE name = ?", "Bob")
            if bob_balance < 1000:
                raise ValueError("余额不足")
            # 这行不会执行
            db.execute("UPDATE accounts SET balance = balance - 1000 WHERE name = ?", "Bob")
        print("✅ 转账成功")
    except Exception as e:
        print(f"❌ 转账失败（已回滚）: {e}")
    
    print("\n最终余额:")
    show_balances()
    
    db.close()
    print("\n")


def example_import_export():
    """数据导入导出示例。"""
    print("=" * 60)
    print("数据导入导出示例")
    print("=" * 60)
    
    import tempfile
    import os
    import json
    
    db = create_in_memory()
    
    # 创建表
    db.create_table(Table(
        name="contacts",
        columns=[
            Column("id", "INTEGER", primary_key=True),
            Column("name", "TEXT"),
            Column("phone", "TEXT"),
            Column("email", "TEXT"),
        ]
    ))
    
    # 插入数据
    contacts = [
        {"name": "张三", "phone": "13800138000", "email": "zhangsan@example.com"},
        {"name": "李四", "phone": "13900139000", "email": "lisi@example.com"},
        {"name": "王五", "phone": "13700137000", "email": "wangwu@example.com"},
    ]
    db.insert_many("contacts", contacts)
    print(f"✅ 插入 {len(contacts)} 条联系人数据")
    
    # 导出到 JSON
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json_path = f.name
    count = db.export_to_json("contacts", json_path)
    print(f"✅ 导出 {count} 条数据到 JSON: {json_path}")
    
    # 读取 JSON 验证
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    print(f"📋 JSON 内容预览:")
    for item in data[:2]:
        print(f"   {item['name']}: {item['phone']}")
    
    # 导出到 CSV
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        csv_path = f.name
    count = db.export_to_csv("contacts", csv_path)
    print(f"\n✅ 导出 {count} 条数据到 CSV: {csv_path}")
    
    # 读取 CSV 验证
    with open(csv_path, 'r', encoding='utf-8') as f:
        print(f"📋 CSV 内容预览:")
        for i, line in enumerate(f):
            if i < 3:
                print(f"   {line.strip()}")
    
    # 清理临时文件
    os.remove(json_path)
    os.remove(csv_path)
    
    db.close()
    print("\n")


def example_database_info():
    """数据库信息示例。"""
    print("=" * 60)
    print("数据库信息示例")
    print("=" * 60)
    
    import tempfile
    
    # 创建临时数据库文件
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
        db_path = f.name
    
    db = Database(db_path)
    db.connect()
    
    # 创建几个表
    db.create_table(Table(
        name="users",
        columns=[
            Column("id", "INTEGER", primary_key=True),
            Column("name", "TEXT"),
        ]
    ))
    
    db.create_table(Table(
        name="posts",
        columns=[
            Column("id", "INTEGER", primary_key=True),
            Column("user_id", "INTEGER"),
            Column("title", "TEXT"),
        ]
    ))
    
    # 获取数据库信息
    print("📊 数据库统计:")
    stats = db.get_stats()
    print(f"   路径：{stats['path']}")
    print(f"   大小：{stats['size_formatted']}")
    print(f"   SQLite 版本：{stats['version']}")
    print(f"   表数量：{stats['table_count']}")
    print(f"   表列表：{', '.join(stats['tables'])}")
    
    # 获取表结构
    print("\n📋 users 表结构:")
    info = db.get_table_info("users")
    for col in info:
        print(f"   {col['name']}: {col['type']} (nullable={col['notnull'] == 0})")
    
    # 创建索引
    db.create_index("posts", ["user_id"])
    db.create_index("posts", ["title"], unique=False)
    print("\n✅ 创建索引")
    
    # 添加列
    db.add_column("users", Column("email", "TEXT"))
    print("✅ 添加 email 列到 users 表")
    
    # 验证
    info = db.get_table_info("users")
    column_names = [col['name'] for col in info]
    print(f"   users 表现在的列：{', '.join(column_names)}")
    
    db.close()
    
    # 清理
    import os
    os.remove(db_path)
    
    print("\n")


if __name__ == "__main__":
    example_basic_crud()
    example_query_builder()
    example_transaction()
    example_import_export()
    example_database_info()
    
    print("=" * 60)
    print("✅ 所有示例运行完成！")
    print("=" * 60)

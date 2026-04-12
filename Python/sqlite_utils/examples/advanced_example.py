"""
AllToolkit - SQLite Utils Advanced Examples

高级用法示例：多线程、连接池、复杂查询等。

Run from sqlite_utils directory:
    python examples/advanced_example.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import Database, Table, Column, create_in_memory, connect
import threading
import time
from datetime import datetime


def example_connection_pool():
    """连接池多线程示例。"""
    print("=" * 60)
    print("连接池多线程示例")
    print("=" * 60)
    
    import tempfile
    import os
    
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
        db_path = f.name
    
    # 创建带连接池的数据库
    db = Database(db_path)
    db.connect(use_pool=True, max_connections=5)
    
    # 创建日志表
    db.create_table(Table(
        name="worker_logs",
        columns=[
            Column("id", "INTEGER", primary_key=True),
            Column("worker_id", "INTEGER"),
            Column("message", "TEXT"),
            Column("timestamp", "TEXT"),
        ]
    ))
    
    results = {"success": 0, "errors": []}
    lock = threading.Lock()
    
    def worker(worker_id, num_operations):
        """工作线程函数。"""
        try:
            for i in range(num_operations):
                db.insert("worker_logs", {
                    "worker_id": worker_id,
                    "message": f"Operation {i} from worker {worker_id}",
                    "timestamp": datetime.now().isoformat()
                })
            with lock:
                results["success"] += 1
        except Exception as e:
            with lock:
                results["errors"].append(f"Worker {worker_id}: {e}")
    
    # 启动多个工作线程
    num_workers = 5
    ops_per_worker = 100
    threads = []
    
    start_time = time.time()
    
    for i in range(num_workers):
        t = threading.Thread(target=worker, args=(i, ops_per_worker))
        threads.append(t)
        t.start()
    
    # 等待所有线程完成
    for t in threads:
        t.join()
    
    elapsed = time.time() - start_time
    
    # 统计结果
    total_count = db.count("worker_logs")
    print(f"✅ {num_workers} 个工作线程完成")
    print(f"   成功线程：{results['success']}/{num_workers}")
    print(f"   总记录数：{total_count}")
    print(f"   预期记录数：{num_workers * ops_per_worker}")
    print(f"   耗时：{elapsed:.2f}秒")
    print(f"   写入速度：{total_count/elapsed:.0f} 记录/秒")
    
    if results["errors"]:
        print(f"\n❌ 错误:")
        for error in results["errors"]:
            print(f"   {error}")
    
    # 验证每个工人的记录数
    print(f"\n📋 各工人记录数:")
    for i in range(num_workers):
        count = db.count("worker_logs", "worker_id = ?", (i,))
        print(f"   Worker {i}: {count} 条")
    
    db.close()
    os.remove(db_path)
    print("\n")


def example_batch_operations():
    """批量操作性能示例。"""
    print("=" * 60)
    print("批量操作性能示例")
    print("=" * 60)
    
    db = create_in_memory()
    
    # 创建表
    db.create_table(Table(
        name="events",
        columns=[
            Column("id", "INTEGER", primary_key=True),
            Column("event_type", "TEXT"),
            Column("data", "TEXT"),
            Column("created_at", "TEXT"),
        ]
    ))
    
    # 生成测试数据
    num_records = 10000
    events = [
        {
            "event_type": f"type_{i % 10}",
            "data": f"Event data {i}",
            "created_at": datetime.now().isoformat()
        }
        for i in range(num_records)
    ]
    
    # 方法 1: 单条插入（慢）
    print(f"📝 单条插入 {num_records} 条记录...")
    start = time.time()
    for event in events[:100]:  # 只测 100 条
        db.insert("events", event)
    single_time = time.time() - start
    print(f"   耗时：{single_time:.3f}秒 (100 条)")
    
    # 清空表
    db.execute("DELETE FROM events")
    
    # 方法 2: 批量插入（快）
    print(f"\n📝 批量插入 {num_records} 条记录...")
    start = time.time()
    db.insert_many("events", events)
    batch_time = time.time() - start
    print(f"   耗时：{batch_time:.3f}秒 ({num_records} 条)")
    print(f"   速度：{num_records/batch_time:.0f} 记录/秒")
    
    # 方法 3: 事务包裹批量插入（更快）
    db.execute("DELETE FROM events")
    
    print(f"\n📝 事务包裹批量插入 {num_records} 条记录...")
    start = time.time()
    with db.transaction():
        db.insert_many("events", events)
    transaction_time = time.time() - start
    print(f"   耗时：{transaction_time:.3f}秒 ({num_records} 条)")
    print(f"   速度：{num_records/transaction_time:.0f} 记录/秒")
    
    # 性能对比
    print(f"\n📊 性能对比:")
    print(f"   批量插入比单条快：{single_time/(batch_time/100):.0f}x (推算)")
    print(f"   事务批量比单条快：{single_time/(transaction_time/100):.0f}x (推算)")
    
    db.close()
    print("\n")


def example_complex_queries():
    """复杂查询示例。"""
    print("=" * 60)
    print("复杂查询示例")
    print("=" * 60)
    
    db = create_in_memory()
    
    # 创建订单表
    db.create_table(Table(
        name="orders",
        columns=[
            Column("id", "INTEGER", primary_key=True),
            Column("customer_id", "INTEGER"),
            Column("product_id", "INTEGER"),
            Column("quantity", "INTEGER"),
            Column("price", "REAL"),
            Column("status", "TEXT"),
            Column("order_date", "TEXT"),
        ]
    ))
    
    # 插入测试数据
    import random
    orders = []
    for i in range(100):
        orders.append({
            "customer_id": random.randint(1, 10),
            "product_id": random.randint(1, 5),
            "quantity": random.randint(1, 10),
            "price": round(random.uniform(10, 100), 2),
            "status": random.choice(["pending", "shipped", "delivered", "cancelled"]),
            "order_date": f"2026-{random.randint(1,4):02d}-{random.randint(1,28):02d}"
        })
    db.insert_many("orders", orders)
    
    # 查询 1: 按客户统计订单
    print("📊 按客户统计订单:")
    sql = """
        SELECT customer_id, 
               COUNT(*) as order_count,
               SUM(quantity) as total_items,
               SUM(quantity * price) as total_amount
        FROM orders
        WHERE status != 'cancelled'
        GROUP BY customer_id
        ORDER BY total_amount DESC
        LIMIT 5
    """
    result = db.query(sql)
    for row in result.to_dicts():
        print(f"   客户{row['customer_id']}: {row['order_count']}单，"
              f"{row['total_items']}件，¥{row['total_amount']:.2f}")
    
    # 查询 2: 按月统计
    print(f"\n📊 按月统计订单:")
    sql = """
        SELECT substr(order_date, 1, 7) as month,
               COUNT(*) as order_count,
               SUM(quantity * price) as revenue
        FROM orders
        GROUP BY month
        ORDER BY month
    """
    result = db.query(sql)
    for row in result.to_dicts():
        print(f"   {row['month']}: {row['order_count']}单，¥{row['revenue']:.2f}")
    
    # 查询 3: 使用查询构建器
    print(f"\n📊 高价值订单（>¥500）:")
    qb = db.table("orders")
    sql, params = (qb
        .select("id", "customer_id", "quantity", "price")
        .where("status = ?", "delivered")
        .order_by("price", desc=True)
        .limit(5)
        .build_select())
    
    result = db.query(sql, *params)
    for row in result.to_dicts():
        total = row['quantity'] * row['price']
        if total > 500:
            print(f"   订单{row['id']}: {row['quantity']}件 x ¥{row['price']} = ¥{total:.2f}")
    
    db.close()
    print("\n")


def example_backup_restore():
    """备份恢复示例。"""
    print("=" * 60)
    print("备份恢复示例")
    print("=" * 60)
    
    import tempfile
    import os
    
    # 创建主数据库
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
        main_db_path = f.name
    
    # 创建备份文件路径
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
        backup_path = f.name
    
    try:
        # 初始化数据库
        db = Database(main_db_path)
        db.connect()
        
        db.create_table(Table(
            name="important_data",
            columns=[
                Column("id", "INTEGER", primary_key=True),
                Column("value", "TEXT"),
            ]
        ))
        
        db.insert("important_data", {"value": "Critical data 1"})
        db.insert("important_data", {"value": "Critical data 2"})
        
        print("📋 初始数据:")
        for row in db.query_dicts("SELECT * FROM important_data"):
            print(f"   {row['value']}")
        
        # 创建备份
        db.backup(backup_path)
        print(f"\n✅ 备份已创建：{backup_path}")
        
        # 修改原数据库
        db.insert("important_data", {"value": "New data after backup"})
        print("\n📋 添加新数据后:")
        for row in db.query_dicts("SELECT * FROM important_data"):
            print(f"   {row['value']}")
        
        # 恢复备份
        db.restore(backup_path)
        print("\n✅ 已恢复备份")
        
        # 验证恢复
        print("\n📋 恢复后的数据:")
        for row in db.query_dicts("SELECT * FROM important_data"):
            print(f"   {row['value']}")
        
        db.close()
        
    finally:
        # 清理
        if os.path.exists(main_db_path):
            os.remove(main_db_path)
        if os.path.exists(backup_path):
            os.remove(backup_path)
    
    print("\n")


def example_advanced_features():
    """高级功能示例。"""
    print("=" * 60)
    print("高级功能示例")
    print("=" * 60)
    
    db = create_in_memory()
    
    # 1. 外键约束
    print("1️⃣ 外键约束:")
    db.execute("PRAGMA foreign_keys = ON")
    
    db.create_table(Table(
        name="categories",
        columns=[
            Column("id", "INTEGER", primary_key=True),
            Column("name", "TEXT", unique=True),
        ]
    ))
    
    db.create_table(Table(
        name="products",
        columns=[
            Column("id", "INTEGER", primary_key=True),
            Column("name", "TEXT"),
            Column("category_id", "INTEGER", references="categories(id)"),
        ]
    ))
    
    db.insert("categories", {"name": "Electronics"})
    db.insert("categories", {"name": "Books"})
    
    db.insert("products", {"name": "Laptop", "category_id": 1})
    db.insert("products", {"name": "Novel", "category_id": 2})
    
    print("   ✅ 创建带外键的表")
    
    # 2. 检查约束
    print("\n2️⃣ 检查约束:")
    db.create_table(Table(
        name="employees",
        columns=[
            Column("id", "INTEGER", primary_key=True),
            Column("name", "TEXT"),
            Column("age", "INTEGER", check="age >= 18 AND age <= 65"),
            Column("salary", "REAL", check="salary > 0"),
        ]
    ))
    
    db.insert("employees", {"name": "John", "age": 30, "salary": 50000})
    print("   ✅ 插入有效数据成功")
    
    try:
        db.insert("employees", {"name": "Kid", "age": 15, "salary": 30000})
        print("   ❌ 插入无效年龄（应失败）")
    except Exception as e:
        print(f"   ✅ 正确拒绝无效年龄：CHECK 约束生效")
    
    # 3. 复合唯一约束
    print("\n3️⃣ 复合唯一约束:")
    db.create_table(Table(
        name="enrollments",
        columns=[
            Column("id", "INTEGER", primary_key=True),
            Column("student_id", "INTEGER"),
            Column("course_id", "INTEGER"),
            Column("enrolled_at", "TEXT"),
        ],
        unique_constraints=[["student_id", "course_id"]]
    ))
    
    db.insert("enrollments", {"student_id": 1, "course_id": 101, "enrolled_at": "2026-01-01"})
    print("   ✅ 插入第一条选课记录")
    
    try:
        db.insert("enrollments", {"student_id": 1, "course_id": 101, "enrolled_at": "2026-01-02"})
        print("   ❌ 插入重复选课（应失败）")
    except Exception as e:
        print(f"   ✅ 正确拒绝重复选课：UNIQUE 约束生效")
    
    # 4. 索引优化
    print("\n4️⃣ 索引优化:")
    db.create_table(Table(
        name="logs",
        columns=[
            Column("id", "INTEGER", primary_key=True),
            Column("level", "TEXT"),
            Column("message", "TEXT"),
            Column("created_at", "TEXT"),
        ]
    ))
    
    # 创建索引
    db.create_index("logs", ["level"])
    db.create_index("logs", ["created_at"])
    db.create_index("logs", ["level", "created_at"], index_name="idx_logs_level_time")
    
    print("   ✅ 创建多个索引")
    
    # 插入大量数据测试
    logs = [
        {"level": random.choice(["INFO", "WARNING", "ERROR"]), 
         "message": f"Log message {i}",
         "created_at": f"2026-01-{(i % 28) + 1:02d}"}
        for i in range(1000)
    ]
    
    start = time.time()
    with db.transaction():
        db.insert_many("logs", logs)
    elapsed = time.time() - start
    
    print(f"   ✅ 插入 1000 条日志：{elapsed:.3f}秒")
    
    # 查询性能
    start = time.time()
    for _ in range(100):
        db.query("SELECT * FROM logs WHERE level = ? ORDER BY created_at DESC LIMIT 10", ("ERROR",))
    elapsed = time.time() - start
    
    print(f"   ✅ 100 次索引查询：{elapsed:.3f}秒")
    
    db.close()
    print("\n")


if __name__ == "__main__":
    import random
    
    example_connection_pool()
    example_batch_operations()
    example_complex_queries()
    example_backup_restore()
    example_advanced_features()
    
    print("=" * 60)
    print("✅ 所有高级示例运行完成！")
    print("=" * 60)

"""
XID Utils 使用示例

演示XID（全局唯一、时间排序ID）的各种使用场景。
"""

import sys
import os
import time
from datetime import datetime, timezone

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from xid_utils.mod import (
    XID,
    XIDError,
    XIDGenerator,
    generate,
    from_string,
    from_bytes,
    is_valid,
    extract_timestamp,
    extract_datetime,
    compare,
    batch_generate,
    parse_info,
    min_xid,
    max_xid,
)


def example_basic_usage():
    """基本用法示例"""
    print("=" * 50)
    print("示例1: 基本用法")
    print("=" * 50)
    
    # 生成新的XID
    xid = generate()
    print(f"生成的XID: {xid}")
    print(f"字符串表示: {str(xid)}")
    print(f"字节长度: {len(xid)} 字节")
    print(f"字符串长度: {len(str(xid))} 字符")
    
    # 提取信息
    print(f"\nXID信息:")
    print(f"  时间戳: {xid.timestamp}")
    print(f"  日期时间: {xid.datetime.isoformat()}")
    print(f"  机器ID: {xid.machine_id.hex()}")
    print(f"  进程ID: {xid.process_id}")
    print(f"  计数器: {xid.counter}")
    
    print()


def example_parse_xid():
    """解析XID示例"""
    print("=" * 50)
    print("示例2: 解析现有XID")
    print("=" * 50)
    
    # 从字符串解析
    xid_str = "9m4e2mr0ui3e8a215n4g"
    xid = from_string(xid_str)
    
    print(f"解析XID: {xid_str}")
    print(f"时间戳: {xid.timestamp}")
    print(f"日期时间: {extract_datetime(xid).strftime('%Y-%m-%d %H:%M:%S UTC')}")
    
    # 从字节创建
    xid_bytes = bytes.fromhex("49c7a7c6a0000000a00f1f01")
    xid = from_bytes(xid_bytes)
    print(f"\n从字节创建: {xid}")
    
    # 解析所有信息
    info = parse_info(xid)
    print(f"\n完整解析信息:")
    for key, value in info.items():
        print(f"  {key}: {value}")
    
    print()


def example_database_usage():
    """数据库使用示例"""
    print("=" * 50)
    print("示例3: 数据库场景")
    print("=" * 50)
    
    # 模拟数据库记录
    records = []
    for i in range(5):
        record = {
            'id': str(generate()),
            'name': f"记录{i+1}",
            'created_at': datetime.now(timezone.utc).isoformat()
        }
        records.append(record)
        time.sleep(0.01)  # 模拟时间流逝
    
    print("数据库记录（按XID自动排序）:")
    print("-" * 60)
    for record in records:
        print(f"ID: {record['id']} | 名称: {record['name']}")
    
    # XID可以自然排序
    sorted_ids = sorted([r['id'] for r in records])
    print("\n排序后的ID:")
    for sid in sorted_ids:
        print(f"  {sid}")
    
    # 范围查询：查找某个时间范围内的记录
    print("\n范围查询示例:")
    timestamp = int(time.time())
    start_xid = min_xid(timestamp - 3600)  # 1小时前
    end_xid = max_xid(timestamp)
    print(f"  开始XID: {start_xid}")
    print(f"  结束XID: {end_xid}")
    
    print()


def example_validation():
    """验证示例"""
    print("=" * 50)
    print("示例4: XID验证")
    print("=" * 50)
    
    test_cases = [
        ("9m4e2mr0ui3e8a215n4g", "有效XID"),
        ("00000000000000000000", "全零XID"),
        ("VVVVVVVVVVVVVVVVVVVV", "最大XID"),
        ("short", "太短"),
        ("toolongstringexactly", "长度正确但可能包含无效字符"),
        ("9m4e2mr0ui3e8a215n4!", "包含无效字符"),
        ("", "空字符串"),
    ]
    
    for test_str, description in test_cases:
        valid = is_valid(test_str)
        status = "✓ 有效" if valid else "✗ 无效"
        print(f"  {status} | {test_str:24s} | {description}")
    
    print()


def example_custom_generator():
    """自定义生成器示例"""
    print("=" * 50)
    print("示例5: 自定义生成器")
    print("=" * 50)
    
    # 创建自定义生成器（模拟分布式环境）
    print("模拟分布式环境（不同机器和进程）:")
    
    # 机器1
    generator1 = XIDGenerator(
        machine_id=b'\x01\x00\x00',
        process_id=1000
    )
    
    # 机器2
    generator2 = XIDGenerator(
        machine_id=b'\x02\x00\x00',
        process_id=2000
    )
    
    # 各生成一些XID
    print("\n机器1生成的XID:")
    for i in range(3):
        xid = generator1.generate()
        print(f"  {xid} (机器ID: {xid.machine_id.hex()}, PID: {xid.process_id})")
    
    print("\n机器2生成的XID:")
    for i in range(3):
        xid = generator2.generate()
        print(f"  {xid} (机器ID: {xid.machine_id.hex()}, PID: {xid.process_id})")
    
    print()


def example_sorting():
    """排序示例"""
    print("=" * 50)
    print("示例6: 时间排序特性")
    print("=" * 50)
    
    print("生成XID并验证时间排序:")
    xids = []
    for i in range(10):
        xid = generate()
        xids.append(xid)
        time.sleep(0.05)  # 50ms间隔
    
    # 显示原始顺序
    print("\n原始生成顺序:")
    for i, xid in enumerate(xids):
        ts = extract_datetime(xid).strftime('%H:%M:%S.%f')[:-3]
        print(f"  {i+1:2d}. {xid} | {ts}")
    
    # 打乱并重新排序
    import random
    shuffled = xids.copy()
    random.shuffle(shuffled)
    
    print("\n打乱后:")
    for i, xid in enumerate(shuffled):
        print(f"  {i+1:2d}. {xid}")
    
    # 排序后恢复原始顺序
    sorted_xids = sorted(shuffled)
    print("\n排序后（恢复原始顺序）:")
    for i, xid in enumerate(sorted_xids):
        print(f"  {i+1:2d}. {xid}")
    
    # 验证排序正确
    assert sorted_xids == xids, "排序结果不一致"
    print("\n✓ 排序验证通过！XID按时间正确排序。")
    
    print()


def example_comparison():
    """比较示例"""
    print("=" * 50)
    print("示例7: XID比较")
    print("=" * 50)
    
    # 生成三个XID
    xid1 = generate()
    time.sleep(0.01)
    xid2 = generate()
    time.sleep(0.01)
    xid3 = generate()
    
    print(f"XID1: {xid1}")
    print(f"XID2: {xid2}")
    print(f"XID3: {xid3}")
    
    # 比较
    print(f"\n比较结果:")
    print(f"  XID1 < XID2: {xid1 < xid2}")
    print(f"  XID2 < XID3: {xid2 < xid3}")
    print(f"  XID1 == XID1: {xid1 == xid1}")
    
    # 使用compare函数
    print(f"\n使用compare函数:")
    print(f"  compare(XID1, XID2): {compare(xid1, xid2)}")
    print(f"  compare(XID2, XID1): {compare(xid2, xid1)}")
    print(f"  compare(XID1, XID1): {compare(xid1, xid1)}")
    
    print()


def example_batch_generation():
    """批量生成示例"""
    print("=" * 50)
    print("示例8: 批量生成")
    print("=" * 50)
    
    import time
    start = time.time()
    xids = batch_generate(1000)
    elapsed = time.time() - start
    
    print(f"生成1000个XID")
    print(f"耗时: {elapsed*1000:.2f}ms")
    print(f"平均每个: {elapsed*1000000/1000:.2f}μs")
    
    # 验证唯一性
    unique = len(set(str(x) for x in xids))
    print(f"唯一性: {unique}/1000 (100%)")
    
    # 显示前几个
    print(f"\n前5个XID:")
    for xid in xids[:5]:
        print(f"  {xid}")
    
    print()


def example_use_in_class():
    """在类中使用示例"""
    print("=" * 50)
    print("示例9: 在数据类中使用")
    print("=" * 50)
    
    class User:
        def __init__(self, name, email):
            self.id = generate()
            self.name = name
            self.email = email
            self.created_at = self.id.datetime
        
        def __repr__(self):
            return f"User(id={self.id}, name={self.name})"
    
    # 创建用户
    users = [
        User("张三", "zhangsan@example.com"),
        User("李四", "lisi@example.com"),
        User("王五", "wangwu@example.com"),
    ]
    
    print("用户列表:")
    for user in users:
        print(f"  {user}")
        print(f"    ID: {user.id}")
        print(f"    名称: {user.name}")
        print(f"    邮箱: {user.email}")
        print(f"    创建时间: {user.created_at.isoformat()}")
        print()
    
    print()


def example_as_dict_key():
    """作为字典键示例"""
    print("=" * 50)
    print("示例10: 作为字典键和集合元素")
    print("=" * 50)
    
    # 作为字典键
    cache = {}
    
    # 存储数据
    xid1 = generate()
    xid2 = generate()
    
    cache[xid1] = {"data": "第一个数据"}
    cache[xid2] = {"data": "第二个数据"}
    
    print("作为字典键:")
    print(f"  cache[{xid1}] = {cache[xid1]}")
    print(f"  cache[{xid2}] = {cache[xid2]}")
    
    # 作为集合元素
    seen_ids = set()
    new_xids = [generate() for _ in range(5)]
    
    print("\n作为集合元素（去重）:")
    for xid in new_xids:
        if xid in seen_ids:
            print(f"  {xid} - 已存在")
        else:
            seen_ids.add(xid)
            print(f"  {xid} - 新增")
    
    print(f"\n集合大小: {len(seen_ids)}")
    
    print()


def main():
    """运行所有示例"""
    print()
    print("╔════════════════════════════════════════════════════════╗")
    print("║          XID Utils 使用示例                            ║")
    print("║   全局唯一、时间排序的ID生成与解析                      ║")
    print("╚════════════════════════════════════════════════════════╝")
    print()
    
    example_basic_usage()
    example_parse_xid()
    example_database_usage()
    example_validation()
    example_custom_generator()
    example_sorting()
    example_comparison()
    example_batch_generation()
    example_use_in_class()
    example_as_dict_key()
    
    print("=" * 50)
    print("所有示例运行完成！")
    print("=" * 50)


if __name__ == '__main__':
    main()
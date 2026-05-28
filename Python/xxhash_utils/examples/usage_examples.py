"""
XXHash 工具模块使用示例

演示 XXHash 的各种应用场景：
- 基本哈希计算
- 文件哈希
- 分布式系统分片
- 缓存键生成
- 数据指纹
- 流式处理
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    XXHash32, XXHash64,
    xxhash32, xxhash64,
    xxhash32_hex, xxhash64_hex,
    hash_file_32, hash_file_64,
    hash_list_32, hash_list_64,
    distributed_shard, consistent_hash,
    XXHashStreamer,
    fingerprint_32, fingerprint_64,
    multi_hash, hash_dict
)


def example_basic_hashing():
    """基本哈希计算示例"""
    print("=" * 60)
    print("1. 基本哈希计算")
    print("=" * 60)
    
    # 字符串哈希
    text = "hello world"
    print(f"\n文本: {text}")
    print(f"XXHash32: {xxhash32_hex(text)}")
    print(f"XXHash64: {xxhash64_hex(text)}")
    
    # 字节哈希
    data = b"\x01\x02\x03\x04\x05"
    print(f"\n字节: {data.hex()}")
    print(f"XXHash32: {xxhash32_hex(data)}")
    print(f"XXHash64: {xxhash64_hex(data)}")
    
    # Unicode 字符串
    chinese = "你好，世界！"
    print(f"\n中文: {chinese}")
    print(f"XXHash32: {xxhash32_hex(chinese)}")
    print(f"XXHash64: {xxhash64_hex(chinese)}")


def example_with_seed():
    """使用种子的哈希示例"""
    print("\n" + "=" * 60)
    print("2. 使用种子（改变哈希结果）")
    print("=" * 60)
    
    data = b"important data"
    print(f"\n数据: {data}")
    
    seeds = [0, 1, 100, 0xDEADBEEF]
    for seed in seeds:
        result = xxhash64_hex(data, seed)
        print(f"  种子 {seed}: {result}")
    
    # 种子用于：
    # - 分布式系统中不同节点使用不同种子避免冲突
    # - 安全场景中使用私有种子值
    # - 多个哈希函数（布隆过滤器）


def example_streaming():
    """流式处理示例"""
    print("\n" + "=" * 60)
    print("3. 流式处理（分块计算）")
    print("=" * 60)
    
    # 一次性计算
    full_data = b"hello beautiful world"
    print(f"完整数据: {full_data}")
    print(f"一次性计算: {xxhash64_hex(full_data)}")
    
    # 分块计算（结果相同）
    h = XXHash64()
    h.update(b"hello ")
    h.update(b"beautiful ")
    h.update(b"world")
    print(f"分块计算: {h.hexdigest()}")
    
    # 使用流式处理器
    print("\n使用 XXHashStreamer:")
    streamer = XXHashStreamer(bits=64, seed=0)
    streamer.push("chunk1").push("chunk2").push("chunk3")
    print(f"流式结果: {streamer.hexdigest()}")
    
    # 流式处理适用于：
    # - 大文件处理
    # - 网络数据流
    # - 日志处理


def example_fingerprint():
    """数据指纹示例"""
    print("\n" + "=" * 60)
    print("4. 数据指纹（快速比较）")
    print("=" * 60)
    
    # 比较两个数据块是否相同
    data1 = b"This is some content for comparison"
    data2 = b"This is some content for comparison"
    data3 = b"This is different content"
    
    fp1 = fingerprint_64(data1)
    fp2 = fingerprint_64(data2)
    fp3 = fingerprint_64(data3)
    
    print(f"\n数据1指纹: {fp1}")
    print(f"数据2指纹: {fp2}")
    print(f"数据3指纹: {fp3}")
    
    print(f"\n数据1 == 数据2: {fp1 == fp2}")
    print(f"数据1 == 数据3: {fp1 == fp3}")
    
    # 用于：
    # - 内容去重
    # - 数据库记录比较
    # - 缓存键生成


def example_distributed_sharding():
    """分布式分片示例"""
    print("\n" + "=" * 60)
    print("5. 分布式系统分片")
    print("=" * 60)
    
    # 电商系统分片示例
    num_shards = 8
    user_keys = [f"user:{i}" for i in range(1, 21)]
    order_keys = [f"order:{i}" for i in range(1, 21)]
    
    print(f"\n分片数量: {num_shards}")
    print("\n用户分片分布:")
    for key in user_keys[:10]:
        shard = distributed_shard(key, num_shards)
        print(f"  {key} -> 分片 {shard}")
    
    print("\n订单分片分布:")
    for key in order_keys[:10]:
        shard = distributed_shard(key, num_shards)
        print(f"  {key} -> 分片 {shard}")
    
    # 分片分布统计
    distribution = {}
    for key in user_keys + order_keys:
        shard = distributed_shard(key, num_shards)
        distribution[shard] = distribution.get(shard, 0) + 1
    
    print("\n分片负载分布:")
    for shard, count in sorted(distribution.items()):
        print(f"  分片 {shard}: {count} 条数据")


def example_consistent_hashing():
    """一致性哈希示例"""
    print("\n" + "=" * 60)
    print("6. 一致性哈希（缓存/负载均衡）")
    print("=" * 60)
    
    num_servers = 5
    sessions = [f"session:{i}" for i in range(1, 16)]
    
    print(f"\n服务器数量: {num_servers}")
    print("\n会话分配:")
    for session in sessions:
        server = consistent_hash(session, num_servers)
        print(f"  {session} -> 服务器 {server}")
    
    # 一致性哈希特点：
    # - 相同键总是分配到相同服务器
    # - 服务器变化时只影响部分数据


def example_cache_key():
    """缓存键生成示例"""
    print("\n" + "=" * 60)
    print("7. 缓存键生成")
    print("=" * 60)
    
    # 生成稳定的缓存键
    cache_inputs = [
        {"query": "SELECT * FROM users", "params": {"id": 1}},
        {"query": "SELECT * FROM users", "params": {"id": 2}},
        {"query": "SELECT * FROM orders", "params": {"user_id": 1}},
    ]
    
    print("\n数据库查询缓存键:")
    for input_data in cache_inputs:
        key = fingerprint_64(str(input_data))
        print(f"  {input_data} -> {key}")
    
    # API 请求缓存键
    api_requests = [
        {"endpoint": "/users", "method": "GET", "params": {"page": 1}},
        {"endpoint": "/users", "method": "GET", "params": {"page": 2}},
    ]
    
    print("\nAPI请求缓存键:")
    for req in api_requests:
        key = fingerprint_64(str(req))
        print(f"  {req} -> {key}")


def example_bloom_filter():
    """布隆过滤器多哈希示例"""
    print("\n" + "=" * 60)
    print("8. 布隆过滤器多哈希")
    print("=" * 60)
    
    # 布隆过滤器通常需要多个独立哈希函数
    data = "email@example.com"
    seeds = [0, 1, 2, 3, 4, 5, 6]  # 7个哈希函数
    
    print(f"\n数据: {data}")
    print(f"种子列表: {seeds}")
    
    hashes = multi_hash(data, seeds)
    print("\n多哈希结果:")
    for seed, h in hashes.items():
        print(f"  种子 {seed}: {h:016x}")
    
    # 用于：
    # - 布隆过滤器
    # - 概率性数据结构
    # - 去重系统


def example_dict_hash():
    """字典哈希示例"""
    print("\n" + "=" * 60)
    print("9. 字典哈希（稳定哈希）")
    print("=" * 60)
    
    # 字典哈希不受顺序影响
    dict1 = {"name": "Alice", "age": 30, "city": "NYC"}
    dict2 = {"city": "NYC", "name": "Alice", "age": 30}  # 顺序不同
    
    h1 = hash_dict(dict1)
    h2 = hash_dict(dict2)
    
    print(f"\n字典1: {dict1}")
    print(f"哈希: {h1:016x}")
    
    print(f"\n字典2: {dict2}（顺序不同）")
    print(f"哈希: {h2:016x}")
    
    print(f"\n哈希相等: {h1 == h2}")
    
    # 嵌套字典
    nested = {"user": {"name": "Bob", "settings": {"theme": "dark"}}}
    h_nested = hash_dict(nested)
    print(f"\n嵌套字典: {nested}")
    print(f"哈希: {h_nested:016x}")


def example_list_hash():
    """列表哈希示例"""
    print("\n" + "=" * 60)
    print("10. 列表哈希")
    print("=" * 60)
    
    # 列表哈希（顺序敏感）
    list1 = [1, 2, 3, "hello"]
    list2 = ["hello", 1, 2, 3]  # 顺序不同
    
    h1 = hash_list_64(list1)
    h2 = hash_list_64(list2)
    
    print(f"\n列表1: {list1}")
    print(f"哈希: {h1:016x}")
    
    print(f"\n列表2: {list2}（顺序不同）")
    print(f"哈希: {h2:016x}")
    
    print(f"\n哈希相等: {h1 == h2}")
    
    # 用于：
    # - 列表比较
    # - 队列状态指纹
    # - 批处理任务标识


def example_copy_and_reset():
    """复制和重置示例"""
    print("\n" + "=" * 60)
    print("11. 哈希器复制与重置")
    print("=" * 60)
    
    # 复制哈希器状态
    h = XXHash64()
    h.update(b"shared prefix")
    
    # 创建两个分支
    h1 = h.copy()
    h2 = h.copy()
    
    h1.update(b" branch 1")
    h2.update(b" branch 2")
    
    print(f"\n共享前缀 + 分支1: {h1.hexdigest()}")
    print(f"共享前缀 + 分支2: {h2.hexdigest()}")
    
    # 重置哈希器
    h.reset()
    h.update(b"new data")
    print(f"\n重置后新数据: {h.hexdigest()}")


def example_performance_comparison():
    """性能说明"""
    print("\n" + "=" * 60)
    print("12. XXHash 性能特点")
    print("=" * 60)
    
    print("""
XXHash vs 其他哈希算法性能对比：

算法          吞吐量         用途
───────────────────────────────────────
XXHash64      ~5 GB/s       高速哈希（非加密）
XXHash32      ~6 GB/s       更快，更短
MD5           ~400 MB/s     慢，安全性问题
SHA-256       ~200 MB/s     安全，但慢
CRC32         ~2 GB/s       校验，不适合哈希表

推荐使用场景：
• 哈希表键生成
• 缓存键
• 数据分片
• 快速数据指纹
• 分布式系统负载均衡

不推荐使用场景：
• 密码存储（使用 bcrypt/Argon2）
• 数字签名（使用 SHA-256/SHA-3）
• 加密（使用 AES）
""")


def main():
    """运行所有示例"""
    example_basic_hashing()
    example_with_seed()
    example_streaming()
    example_fingerprint()
    example_distributed_sharding()
    example_consistent_hashing()
    example_cache_key()
    example_bloom_filter()
    example_dict_hash()
    example_list_hash()
    example_copy_and_reset()
    example_performance_comparison()
    
    print("\n" + "=" * 60)
    print("所有示例完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
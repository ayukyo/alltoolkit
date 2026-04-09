#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Hash Utils - Incremental Hashing Example

演示如何使用增量哈希处理大文件和流式数据。
"""

import sys
import os
import tempfile
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import IncrementalHasher, sha256


def main():
    print("="*60)
    print("Hash Utils - Incremental Hashing Example")
    print("="*60)
    print()
    
    # 1. 基本增量哈希
    print("1. 基本增量哈希")
    print("-"*60)
    
    data = "Hello, World!"
    
    # 批量哈希
    bulk_hash = sha256(data)
    
    # 增量哈希
    hasher = IncrementalHasher('sha256')
    for char in data:
        hasher.update(char)
    incremental_hash = hasher.hexdigest()
    
    print(f"数据：{data}")
    print(f"批量哈希：{bulk_hash}")
    print(f"增量哈希：{incremental_hash}")
    print(f"结果一致：{bulk_hash == incremental_hash}")
    print()
    
    # 2. 流式数据处理
    print("2. 流式数据处理（模拟网络流）")
    print("-"*60)
    
    # 模拟从网络接收数据块
    stream_data = [
        b"GET /api/data HTTP/1.1\r\n",
        b"Host: example.com\r\n",
        b"Content-Type: application/json\r\n",
        b"\r\n",
        b'{"status": "ok", "data": [1, 2, 3]}'
    ]
    
    hasher = IncrementalHasher('sha256')
    total_bytes = 0
    
    print("接收数据块:")
    for i, chunk in enumerate(stream_data, 1):
        hasher.update(chunk)
        total_bytes += len(chunk)
        print(f"  块 {i}: {len(chunk)} 字节")
    
    print(f"\n总字节数：{total_bytes}")
    print(f"最终哈希：{hasher.hexdigest()}")
    print()
    
    # 3. 大文件分块哈希
    print("3. 大文件分块哈希")
    print("-"*60)
    
    # 创建临时大文件
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    temp_path = temp_file.name
    
    # 写入 10MB 数据
    chunk_size = 1024 * 1024  # 1MB
    total_size = 10 * chunk_size
    test_data = b"x" * chunk_size
    
    print(f"创建测试文件：{total_size / (1024*1024):.1f} MB")
    
    start_time = time.time()
    with open(temp_path, 'wb') as f:
        for i in range(10):
            f.write(test_data)
    write_time = time.time() - start_time
    print(f"写入时间：{write_time:.3f} 秒")
    
    # 分块读取并哈希
    hasher = IncrementalHasher('sha256')
    start_time = time.time()
    
    with open(temp_path, 'rb') as f:
        chunk_num = 0
        while chunk := f.read(chunk_size):
            chunk_num += 1
            hasher.update(chunk)
    
    hash_time = time.time() - start_time
    file_hash = hasher.hexdigest()
    
    print(f"读取块数：{chunk_num}")
    print(f"哈希时间：{hash_time:.3f} 秒")
    print(f"文件哈希：{file_hash[:48]}...")
    
    # 清理
    temp_file.close()
    os.unlink(temp_path)
    print()
    
    # 4. 哈希器状态复制
    print("4. 哈希器状态复制（分支计算）")
    print("-"*60)
    
    hasher = IncrementalHasher('sha256')
    hasher.update("common prefix ")
    
    # 复制状态
    hasher1 = hasher.copy()
    hasher2 = hasher.copy()
    
    # 不同分支
    hasher1.update("branch A")
    hasher2.update("branch B")
    
    print(f"公共前缀：'common prefix '")
    print(f"分支 A 哈希：{hasher1.hexdigest()[:32]}...")
    print(f"分支 B 哈希：{hasher2.hexdigest()[:32]}...")
    print(f"哈希不同：{hasher1.hexdigest() != hasher2.hexdigest()}")
    print()
    
    # 5. 链式调用
    print("5. 链式调用")
    print("-"*60)
    
    result = (IncrementalHasher('md5')
              .update("Hello")
              .update(" ")
              .update("World")
              .hexdigest())
    
    print(f"链式哈希：{result}")
    print(f"验证：{result == 'b10a8db164e0754105b7a99be72e3fe5'}")  # MD5 of "Hello World"
    print()
    
    # 6. 重置哈希器
    print("6. 重置哈希器（复用）")
    print("-"*60)
    
    hasher = IncrementalHasher('sha256')
    
    # 第一次哈希
    hasher.update("first")
    hash1 = hasher.hexdigest()
    print(f"第一次：'first' -> {hash1[:32]}...")
    
    # 重置
    hasher.reset()
    
    # 第二次哈希
    hasher.update("second")
    hash2 = hasher.hexdigest()
    print(f"第二次：'second' -> {hash2[:32]}...")
    
    # 验证独立
    expected1 = sha256("first")
    expected2 = sha256("second")
    print(f"第一次正确：{hash1 == expected1}")
    print(f"第二次正确：{hash2 == expected2}")
    print()
    
    # 7. 不同算法
    print("7. 不同哈希算法")
    print("-"*60)
    
    test_data = "Incremental hash test"
    algorithms = ['md5', 'sha1', 'sha256', 'sha512']
    
    for algo in algorithms:
        hasher = IncrementalHasher(algo)
        hasher.update(test_data)
        print(f"  {algo.upper():8}: {hasher.hexdigest()[:48]}...")
    print()
    
    # 8. 实际场景：日志文件完整性
    print("8. 实际场景：日志文件流式完整性校验")
    print("-"*60)
    
    # 模拟日志写入
    log_hasher = IncrementalHasher('sha256')
    log_entries = [
        '{"timestamp": "2024-01-01T00:00:00Z", "level": "INFO", "msg": "Server started"}',
        '{"timestamp": "2024-01-01T00:00:01Z", "level": "DEBUG", "msg": "Connection accepted"}',
        '{"timestamp": "2024-01-01T00:00:02Z", "level": "INFO", "msg": "User logged in"}',
        '{"timestamp": "2024-01-01T00:00:03Z", "level": "WARN", "msg": "High memory usage"}',
        '{"timestamp": "2024-01-01T00:00:04Z", "level": "INFO", "msg": "Request processed"}',
    ]
    
    print("日志流:")
    for entry in log_entries:
        log_hasher.update(entry + "\n")
        print(f"  {entry[:50]}...")
    
    final_hash = log_hasher.hexdigest()
    print(f"\n日志文件哈希：{final_hash}")
    print("（可用于后续完整性验证）")
    print()
    
    print("="*60)
    print("示例完成！")
    print("="*60)
    print()
    print("增量哈希优势:")
    print("  - 内存高效：不需要一次性加载全部数据")
    print("  - 流式处理：适合网络流、文件流")
    print("  - 状态保存：可以复制和恢复哈希状态")
    print("  - 灵活复用：可以重置后重复使用")


if __name__ == "__main__":
    main()

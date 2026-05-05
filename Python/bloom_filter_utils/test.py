"""
Bloom Filter Utils 测试套件

测试布隆过滤器的各种功能
"""

import sys
import random
import string
import time

sys.path.insert(0, '.')
from mod import (
    BloomFilter,
    ScalableBloomFilter,
    CountingBloomFilter,
    create_filter,
    create_scalable,
    estimate_size
)


def test_basic_operations():
    """测试基本操作"""
    print("测试基本操作...")
    bf = BloomFilter(1000, 0.01)
    
    # 添加元素
    bf.add("hello")
    bf.add("world")
    bf.add("test")
    
    # 检查存在
    assert "hello" in bf, "应找到已添加的元素"
    assert "world" in bf, "应找到已添加的元素"
    assert "test" in bf, "应找到已添加的元素"
    
    # 检查不存在
    assert "notexist" not in bf, "不应找到未添加的元素"
    assert "another" not in bf, "不应找到未添加的元素"
    
    print("✓ 基本操作测试通过")


def test_bytes_items():
    """测试字节项"""
    print("测试字节项...")
    bf = BloomFilter(100)
    
    bf.add(b"binary_data")
    bf.add("string_data")
    
    assert b"binary_data" in bf
    assert "string_data" in bf
    
    print("✓ 字节项测试通过")


def test_false_positive_rate():
    """测试误判率"""
    print("测试误判率...")
    
    n = 10000  # 元素数量
    p = 0.01   # 目标误判率
    
    bf = BloomFilter(n, p)
    
    # 添加 n 个元素
    items = [f"item_{i}" for i in range(n)]
    for item in items:
        bf.add(item)
    
    # 测试误判率
    test_items = [f"test_{i}" for i in range(n)]
    false_positives = sum(1 for item in test_items if item in bf)
    actual_fp_rate = false_positives / n
    
    print(f"  目标误判率: {p:.4f}")
    print(f"  实际误判率: {actual_fp_rate:.4f}")
    
    # 允许 2 倍误差
    assert actual_fp_rate < p * 2, f"误判率过高: {actual_fp_rate}"
    
    print("✓ 误判率测试通过")


def test_no_false_negatives():
    """测试零漏判"""
    print("测试零漏判...")
    
    bf = BloomFilter(1000, 0.01)
    items = [f"item_{i}" for i in range(1000)]
    
    for item in items:
        bf.add(item)
    
    # 所有已添加元素都应该能找到
    for item in items:
        assert item in bf, f"漏判: {item}"
    
    print("✓ 零漏判测试通过")


def test_serialization():
    """测试序列化/反序列化"""
    print("测试序列化...")
    
    bf1 = BloomFilter(1000, 0.05)
    items = [f"serialize_{i}" for i in range(100)]
    
    for item in items:
        bf1.add(item)
    
    # 序列化
    data = bf1.serialize()
    
    # 反序列化
    bf2 = BloomFilter.deserialize(data)
    
    # 验证所有元素仍然存在
    for item in items:
        assert item in bf2, f"反序列化后丢失: {item}"
    
    print(f"  序列化大小: {len(data)} bytes")
    print("✓ 序列化测试通过")


def test_union():
    """测试并集操作"""
    print("测试并集...")
    
    bf1 = BloomFilter(100, 0.01)
    bf2 = BloomFilter(100, 0.01)
    
    bf1.add("a")
    bf1.add("b")
    
    bf2.add("c")
    bf2.add("d")
    
    bf_union = bf1.union(bf2)
    
    assert "a" in bf_union
    assert "b" in bf_union
    assert "c" in bf_union
    assert "d" in bf_union
    
    print("✓ 并集测试通过")


def test_intersection():
    """测试交集操作"""
    print("测试交集...")
    
    bf1 = BloomFilter(100, 0.01)
    bf2 = BloomFilter(100, 0.01)
    
    bf1.add("a")
    bf1.add("b")
    bf1.add("c")
    
    bf2.add("b")
    bf2.add("c")
    bf2.add("d")
    
    bf_inter = bf1.intersection(bf2)
    
    # 交集应包含 b 和 c
    assert "b" in bf_inter
    assert "c" in bf_inter
    
    print("✓ 交集测试通过")


def test_counting_filter():
    """测试计数布隆过滤器"""
    print("测试计数布隆过滤器...")
    
    cbf = CountingBloomFilter(1000, 0.01)
    
    # 添加元素
    cbf.add("apple")
    cbf.add("banana")
    cbf.add("apple")  # 重复添加
    
    assert "apple" in cbf
    assert "banana" in cbf
    assert "orange" not in cbf
    
    # 删除元素
    assert cbf.remove("apple")
    assert "apple" in cbf  # 还有一次计数
    
    assert cbf.remove("apple")
    assert "apple" not in cbf  # 完全删除
    
    assert not cbf.remove("orange")  # 删除不存在的元素
    
    print("✓ 计数布隆过滤器测试通过")


def test_counting_filter_count():
    """测试计数功能"""
    print("测试计数功能...")
    
    cbf = CountingBloomFilter(100, 0.01)
    
    # 多次添加同一元素
    for _ in range(5):
        cbf.add("counted")
    
    # 计数应该接近 5
    count = cbf.count("counted")
    assert count >= 1, "计数应该至少为 1"
    
    print(f"  计数值: {count}")
    print("✓ 计数功能测试通过")


def test_scalable_filter():
    """测试可扩展布隆过滤器"""
    print("测试可扩展布隆过滤器...")
    
    sbf = ScalableBloomFilter(initial_capacity=100, false_positive_rate=0.01)
    
    # 添加超过初始容量的元素
    items = [f"scalable_{i}" for i in range(1000)]
    for item in items:
        sbf.add(item)
    
    # 检查所有元素
    for item in items:
        assert item in sbf, f"可扩展过滤器丢失: {item}"
    
    print(f"  层数: {len(sbf._filters)}")
    print("✓ 可扩展布隆过滤器测试通过")


def test_scalable_no_duplicates():
    """测试可扩展过滤器去重"""
    print("测试可扩展过滤器去重...")
    
    sbf = ScalableBloomFilter(100)
    
    sbf.add("unique")
    sbf.add("unique")
    sbf.add("unique")
    
    assert len(sbf) == 1, "应只计数一次"
    
    print("✓ 去重测试通过")


def test_clear():
    """测试清空功能"""
    print("测试清空功能...")
    
    bf = BloomFilter(100)
    bf.add("item1")
    bf.add("item2")
    
    assert len(bf) == 2
    
    bf.clear()
    
    assert len(bf) == 0
    assert "item1" not in bf
    assert "item2" not in bf
    
    print("✓ 清空测试通过")


def test_estimate_size():
    """测试资源估算"""
    print("测试资源估算...")
    
    info = estimate_size(1000000, 0.01)
    
    print(f"  100万元素，1%误判率:")
    print(f"  - 比特数: {info['bits']:,}")
    print(f"  - 字节数: {info['bytes']:,}")
    print(f"  - KB: {info['kb']}")
    print(f"  - MB: {info['mb']}")
    print(f"  - 哈希函数数: {info['hash_functions']}")
    
    assert info['bits'] > 0
    assert info['hash_functions'] > 0
    
    print("✓ 资源估算测试通过")


def test_load_factor():
    """测试负载因子"""
    print("测试负载因子...")
    
    bf = BloomFilter(1000, 0.01)
    
    # 空过滤器
    assert bf.load_factor == 0
    
    # 添加元素
    for i in range(100):
        bf.add(f"load_{i}")
    
    lf = bf.load_factor
    print(f"  添加100元素后负载因子: {lf:.4f}")
    assert 0 < lf < 1
    
    print("✓ 负载因子测试通过")


def test_convenience_functions():
    """测试便捷函数"""
    print("测试便捷函数...")
    
    bf = create_filter(1000, 0.05)
    assert isinstance(bf, BloomFilter)
    
    sbf = create_scalable(100, 0.05)
    assert isinstance(sbf, ScalableBloomFilter)
    
    print("✓ 便捷函数测试通过")


def test_edge_cases():
    """测试边界情况"""
    print("测试边界情况...")
    
    # 最小容量
    bf = BloomFilter(1, 0.5)
    bf.add("only_one")
    assert "only_one" in bf
    
    # 低误判率
    bf2 = BloomFilter(100, 0.001)
    for i in range(50):
        bf2.add(f"low_fp_{i}")
    
    for i in range(50):
        assert f"low_fp_{i}" in bf2
    
    print("✓ 边界情况测试通过")


def test_thread_safety():
    """测试线程安全"""
    print("测试线程安全...")
    
    import threading
    
    bf = BloomFilter(10000, 0.01)
    errors = []
    
    def add_items(start, end):
        try:
            for i in range(start, end):
                bf.add(f"thread_{i}")
        except Exception as e:
            errors.append(str(e))
    
    threads = []
    for i in range(4):
        t = threading.Thread(target=add_items, args=(i*1000, (i+1)*1000))
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    
    assert len(errors) == 0, f"线程安全错误: {errors}"
    print("✓ 线程安全测试通过")


def run_performance_test():
    """性能测试"""
    print("\n========== 性能测试 ==========")
    
    n = 100000
    bf = BloomFilter(n, 0.01)
    
    # 插入性能
    start = time.time()
    for i in range(n):
        bf.add(f"perf_{i}")
    insert_time = time.time() - start
    print(f"插入 {n:,} 元素: {insert_time:.2f}s ({n/insert_time:,.0f} ops/s)")
    
    # 查询性能
    start = time.time()
    for i in range(n):
        _ = f"perf_{i}" in bf
    query_time = time.time() - start
    print(f"查询 {n:,} 元素: {query_time:.2f}s ({n/query_time:,.0f} ops/s)")
    
    # 内存估算
    info = estimate_size(n, 0.01)
    print(f"内存使用: ~{info['mb']} MB")
    
    # 序列化性能
    start = time.time()
    data = bf.serialize()
    serialize_time = time.time() - start
    print(f"序列化大小: {len(data):,} bytes ({len(data)/1024/1024:.2f} MB)")
    print(f"序列化时间: {serialize_time:.2f}s")
    
    # 反序列化性能
    start = time.time()
    bf2 = BloomFilter.deserialize(data)
    deserialize_time = time.time() - start
    print(f"反序列化时间: {deserialize_time:.2f}s")
    
    print("✓ 性能测试完成")


def main():
    print("=" * 50)
    print("Bloom Filter Utils 测试套件")
    print("=" * 50)
    
    tests = [
        test_basic_operations,
        test_bytes_items,
        test_false_positive_rate,
        test_no_false_negatives,
        test_serialization,
        test_union,
        test_intersection,
        test_counting_filter,
        test_counting_filter_count,
        test_scalable_filter,
        test_scalable_no_duplicates,
        test_clear,
        test_estimate_size,
        test_load_factor,
        test_convenience_functions,
        test_edge_cases,
        test_thread_safety,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"✗ {test.__name__} 失败: {e}")
            failed += 1
    
    print("\n" + "=" * 50)
    print(f"测试结果: {passed} 通过, {failed} 失败")
    print("=" * 50)
    
    # 性能测试
    run_performance_test()
    
    return failed == 0


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
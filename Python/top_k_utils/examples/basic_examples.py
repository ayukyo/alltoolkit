"""
Top-K 工具集示例

演示各种 Top-K 功能的用法。
"""

import sys
sys.path.insert(0, '..')

from mod import (
    top_k_heap,
    top_k_quickselect,
    top_k_sort,
    StreamingTopK,
    FrequentItems,
    TopKFrequent,
    merge_top_k,
    top_k_unique,
    top_k_with_threshold,
    top_k_percentile,
    nth_element,
    median,
)


def example_basic_top_k():
    """基本 Top-K 示例"""
    print("=" * 50)
    print("基本 Top-K 示例")
    print("=" * 50)
    
    data = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
    
    print(f"数据: {data}")
    
    # 堆方法
    print(f"\n堆方法 Top-3 最大: {top_k_heap(data, 3)}")
    print(f"堆方法 Top-3 最小: {top_k_heap(data, 3, largest=False)}")
    
    # QuickSelect
    quick_result = top_k_quickselect(data, 5)
    print(f"\nQuickSelect Top-5: {sorted(quick_result, reverse=True)}")
    
    # 排序方法
    print(f"\n排序方法 Top-3: {top_k_sort(data, 3)}")


def example_custom_key():
    """自定义键函数示例"""
    print("\n" + "=" * 50)
    print("自定义键函数示例")
    print("=" * 50)
    
    students = [
        {'name': 'Alice', 'score': 85},
        {'name': 'Bob', 'score': 92},
        {'name': 'Charlie', 'score': 78},
        {'name': 'Diana', 'score': 95},
        {'name': 'Eve', 'score': 88},
    ]
    
    print("学生成绩:")
    for s in students:
        print(f"  {s['name']}: {s['score']}")
    
    # 找成绩最高的3个学生
    top_students = top_k_heap(students, 3, key=lambda x: x['score'])
    print(f"\n成绩 Top-3:")
    for i, s in enumerate(top_students, 1):
        print(f"  #{i}: {s['name']} - {s['score']}分")


def example_streaming():
    """流式 Top-K 示例"""
    print("\n" + "=" * 50)
    print("流式 Top-K 示例")
    print("=" * 50)
    
    stream = StreamingTopK(5)
    
    # 模拟数据流
    import random
    random.seed(42)
    
    print("模拟接收1000个随机数据...")
    for _ in range(1000):
        stream.add(random.randint(1, 10000))
    
    print(f"\n当前最大的5个元素: {stream.get_top_k()}")
    
    # 添加更多数据
    print("\n添加一些超大数据...")
    stream.add_all([10001, 10002, 10003])
    
    print(f"更新后的 Top-5: {stream.get_top_k()}")


def example_frequent_items():
    """频繁元素统计示例"""
    print("\n" + "=" * 50)
    print("频繁元素统计示例")
    print("=" * 50)
    
    # 模拟网站访问日志
    page_views = [
        'home', 'products', 'home', 'cart', 'products',
        'home', 'checkout', 'home', 'products', 'cart',
        'home', 'products', 'home', 'checkout', 'home',
        'products', 'cart', 'home', 'about', 'home',
    ]
    
    # 使用 FrequentItems（Space-Saving 算法）
    freq = FrequentItems(5)
    freq.add_all(page_views)
    
    print("页面访问 Top-5:")
    for page, count in freq.get_top_k():
        print(f"  {page}: {count} 次")
    
    print(f"\n总访问量: {freq.get_total()}")
    
    # 使用精确版本
    print("\n--- 精确统计 ---")
    exact_freq = TopKFrequent()
    exact_freq.add_all(page_views)
    
    print("所有页面统计:")
    for page, count in exact_freq.get_top_k(10):
        print(f"  {page}: {count} 次")
    
    print(f"\n唯一页面数: {exact_freq.get_unique_count()}")


def example_distributed():
    """分布式合并示例"""
    print("\n" + "=" * 50)
    print("分布式 Top-K 合并示例")
    print("=" * 50)
    
    # 模拟3个分片的 Top-K 结果
    shard1 = [98, 95, 90, 88]
    shard2 = [99, 87, 85, 83]
    shard3 = [100, 92, 88, 82]
    
    print("分片结果:")
    print(f"  Shard 1: {shard1}")
    print(f"  Shard 2: {shard2}")
    print(f"  Shard 3: {shard3}")
    
    # 合并为全局 Top-5
    global_top_5 = merge_top_k([shard1, shard2, shard3], 5)
    print(f"\n全局 Top-5: {global_top_5}")


def example_special_purpose():
    """特殊用途示例"""
    print("\n" + "=" * 50)
    print("特殊用途 Top-K 示例")
    print("=" * 50)
    
    data = [3, 1, 4, 1, 5, 9, 2, 6, 5, 9, 8, 7]
    
    print(f"数据: {data}")
    
    # 唯一元素 Top-K
    unique_top = top_k_unique(data, 5)
    print(f"\n唯一元素 Top-5: {unique_top}")
    
    # 超过阈值
    threshold_result = top_k_with_threshold(data, 5)
    print(f"\n超过5的元素: {threshold_result}")
    
    # 百分位
    percentile_80 = top_k_percentile([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 80)
    print(f"\n80百分位以上的元素: {percentile_80}")


def example_utility():
    """工具函数示例"""
    print("\n" + "=" * 50)
    print("工具函数示例")
    print("=" * 50)
    
    data = [3, 1, 4, 1, 5, 9, 2, 6]
    
    print(f"数据: {data}")
    
    # 第n大元素
    print(f"\n第1大: {nth_element(data, 1)}")
    print(f"第2大: {nth_element(data, 2)}")
    print(f"第3大: {nth_element(data, 3)}")
    
    # 第n小元素
    print(f"\n第1小: {nth_element(data, 1, largest=False)}")
    print(f"第2小: {nth_element(data, 2, largest=False)}")
    
    # 中位数
    print(f"\n中位数: {median(data)}")
    print(f"中位数 (偶数个): {median([1, 2, 3, 4])}")


def example_text_analysis():
    """文本分析示例"""
    print("\n" + "=" * 50)
    print("文本分析示例")
    print("=" * 50)
    
    # 模拟词频统计
    text = "the quick brown fox jumps over the lazy dog the fox is quick"
    words = text.split()
    
    freq = TopKFrequent()
    freq.add_all(words)
    
    print(f"文本: {text}")
    print(f"\n词频 Top-5:")
    for word, count in freq.get_top_k(5):
        print(f"  '{word}': {count} 次")


def example_large_dataset():
    """大数据集性能演示"""
    print("\n" + "=" * 50)
    print("大数据集性能演示")
    print("=" * 50)
    
    import random
    import time
    
    random.seed(42)
    data = [random.randint(1, 1000000) for _ in range(100000)]
    
    print(f"数据规模: {len(data)} 个元素")
    
    # 堆方法
    start = time.time()
    heap_result = top_k_heap(data, 100)
    heap_time = time.time() - start
    print(f"\n堆方法 Top-100: {heap_time:.4f} 秒")
    
    # QuickSelect
    start = time.time()
    quick_result = top_k_quickselect(data, 100)
    quick_time = time.time() - start
    print(f"QuickSelect Top-100: {quick_time:.4f} 秒")
    
    # 排序方法
    start = time.time()
    sort_result = top_k_sort(data, 100)
    sort_time = time.time() - start
    print(f"排序方法 Top-100: {sort_time:.4f} 秒")
    
    # 验证结果一致性
    heap_set = set(heap_result)
    quick_set = set(quick_result)
    sort_set = set(sort_result)
    
    print(f"\n结果一致性: 堆={len(heap_set)} Quick={len(quick_set)} 排序={len(sort_set)}")


if __name__ == '__main__':
    example_basic_top_k()
    example_custom_key()
    example_streaming()
    example_frequent_items()
    example_distributed()
    example_special_purpose()
    example_utility()
    example_text_analysis()
    example_large_dataset()
    
    print("\n" + "=" * 50)
    print("示例完成!")
    print("=" * 50)
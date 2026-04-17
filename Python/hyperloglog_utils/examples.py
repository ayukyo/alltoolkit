"""
HyperLogLog Utils 使用示例

展示各种使用场景和功能。
"""

from hyperloglog_utils import (
    HyperLogLog,
    HyperLogLogPlusPlus,
    SparseHyperLogLog,
    HyperLogLogBuilder,
    create_hll,
    from_iterable,
    merge_multiple,
    estimate_memory,
    compare_precision,
)


def example_basic_usage():
    """基本使用示例"""
    print("\n" + "=" * 60)
    print("示例 1: 基本使用")
    print("=" * 60)
    
    # 创建 HyperLogLog
    hll = HyperLogLog(precision=12)
    
    # 添加元素
    users = ["user_1", "user_2", "user_3", "user_4", "user_5"]
    for user in users:
        hll.add(user)
    
    # 获取估计的基数
    print(f"添加的元素: {users}")
    print(f"估计的基数: {hll.count():.2f}")
    print(f"整数形式: {len(hll)}")
    
    # 显示统计信息
    stats = hll.get_stats()
    print(f"\n统计信息:")
    print(f"  精度: {stats.precision}")
    print(f"  寄存器数量: {stats.num_registers}")
    print(f"  内存使用: {stats.memory_bytes} 字节")
    print(f"  标准误差: {stats.standard_error * 100:.2f}%")


def example_uv_counting():
    """UV 统计示例"""
    print("\n" + "=" * 60)
    print("示例 2: 网站独立访客(UV)统计")
    print("=" * 60)
    
    # 创建高精度 HyperLogLog（误差约 0.8%）
    hll = HyperLogLog(precision=14)
    
    # 模拟一天的用户访问
    # 假设每个用户访问多次
    user_ids = []
    for user in range(10000):  # 10000 个独立用户
        # 每个用户访问 1-10 次
        visits = range(1, 10)
        for _ in visits:
            user_ids.append(f"user_{user}")
    
    # 添加所有访问记录
    for user_id in user_ids:
        hll.add(user_id)
    
    # 总访问次数 vs 独立用户数
    total_visits = len(user_ids)
    unique_users = hll.count()
    
    print(f"总访问次数: {total_visits}")
    print(f"估计的独立用户(UV): {unique_users:.2f}")
    print(f"实际独立用户: 10000")
    print(f"误差: {abs(unique_users - 10000) / 10000 * 100:.2f}%")


def example_large_scale():
    """大规模数据示例"""
    print("\n" + "=" * 60)
    print("示例 3: 大规模数据统计")
    print("=" * 60)
    
    # 创建 precision=16 的 HyperLogLog（误差约 0.4%）
    hll = HyperLogLog(precision=16)
    
    # 模拟 100 万用户 ID
    print("添加 100,000 个元素...")
    for i in range(100000):
        hll.add(f"million_user_{i}")
    
    estimate = hll.count()
    
    print(f"估计基数: {estimate:.2f}")
    print(f"实际基数: 100000")
    print(f"相对误差: {abs(estimate - 100000) / 100000 * 100:.2f}%")
    
    # 显示内存使用
    mem_info = estimate_memory(16)
    print(f"\n内存使用:")
    print(f"  字节: {mem_info['bytes']}")
    print(f"  KB: {mem_info['kilobytes']}")
    print(f"  MB: {mem_info['megabytes']}")


def example_merge():
    """合并示例"""
    print("\n" + "=" * 60)
    print("示例 4: 合并多个数据集")
    print("=" * 60)
    
    # 创建三个 HyperLogLog，代表不同时间段的用户
    hll_day1 = HyperLogLog(precision=12)
    hll_day2 = HyperLogLog(precision=12)
    hll_day3 = HyperLogLog(precision=12)
    
    # 第一天：用户 0-3000
    for i in range(3000):
        hll_day1.add(f"user_{i}")
    
    # 第二天：用户 1000-4000（部分重叠）
    for i in range(1000, 4000):
        hll_day2.add(f"user_{i}")
    
    # 第三天：用户 2000-5000（更多重叠）
    for i in range(2000, 5000):
        hll_day3.add(f"user_{i}")
    
    print(f"第一天 UV: {hll_day1.count():.0f}")
    print(f"第二天 UV: {hll_day2.count():.0f}")
    print(f"第三天 UV: {hll_day3.count():.0f}")
    
    # 合并所有天数
    total = hll_day1.merge(hll_day2).merge(hll_day3)
    print(f"\n三天总计 UV: {total.count():.0f}")
    print(f"实际总计: 5000 个独立用户")
    
    # 计算交集
    intersection = hll_day1.intersection_cardinality(hll_day2)
    print(f"\n第一天和第二天的交集: {intersection:.0f}")
    print(f"实际交集: 2000 (用户 1000-2999)")
    
    # 计算 Jaccard 相似度
    jaccard = hll_day1.jaccard_similarity(hll_day2)
    print(f"Jaccard 相似度: {jaccard:.2f}")


def example_hyperloglog_plusplus():
    """HyperLogLog++ 示例"""
    print("\n" + "=" * 60)
    print("示例 5: HyperLogLog++ (Google 改进版)")
    print("=" * 60)
    
    # 创建 HyperLogLog++
    hll = HyperLogLogPlusPlus(precision=14)
    
    print("初始状态: 稀疏模式")
    print(f"  is_sparse: {hll.is_sparse}")
    
    # 添加少量元素
    for i in range(50):
        hll.add(f"small_{i}")
    
    print(f"\n添加 50 个元素后:")
    print(f"  is_sparse: {hll.is_sparse}")
    print(f"  估计基数: {hll.count():.0f}")
    
    # 添加大量元素触发转换
    for i in range(10000):
        hll.add(f"large_{i}")
    
    print(f"\n添加 10000 个元素后:")
    print(f"  is_sparse: {hll.is_sparse}")
    print(f"  估计基数: {hll.count():.0f}")
    
    # 统计信息
    stats = hll.get_stats()
    print(f"\n统计信息:")
    print(f"  模式: {'密集' if not stats['is_sparse'] else '稀疏'}")
    print(f"  精度: {stats['precision']}")
    print(f"  内存使用: {stats['memory_bytes']} 字节")


def example_sparse_hll():
    """稀疏 HyperLogLog 示例"""
    print("\n" + "=" * 60)
    print("示例 6: 稀疏 HyperLogLog")
    print("=" * 60)
    
    # 创建稀疏 HyperLogLog，从小精度开始
    shll = SparseHyperLogLog(initial_precision=6, max_precision=16)
    
    print(f"初始精度: {shll.precision}")
    print(f"最大精度: {shll.max_precision}")
    
    # 添加少量元素
    for i in range(100):
        shll.add(f"start_{i}")
    
    print(f"\n添加 100 个元素:")
    print(f"  当前精度: {shll.precision}")
    print(f"  is_dense: {shll.is_dense}")
    print(f"  估计基数: {shll.count():.0f}")
    
    # 添加大量元素以触发升级
    for i in range(50000):
        shll.add(f"grow_{i}")
    
    print(f"\n添加 50000 个元素后:")
    print(f"  当前精度: {shll.precision}")
    print(f"  is_dense: {shll.is_dense}")
    print(f"  估计基数: {shll.count():.0f}")
    
    stats = shll.get_stats()
    print(f"  内存使用: {stats['memory_bytes']} 字节")


def example_serialization():
    """序列化示例"""
    print("\n" + "=" * 60)
    print("示例 7: 序列化和持久化")
    print("=" * 60)
    
    # 创建并填充数据
    hll = HyperLogLog(precision=12)
    for i in range(1000):
        hll.add(f"persist_{i}")
    
    # 序列化为字节
    data = hll.to_bytes()
    print(f"序列化大小: {len(data)} 字节")
    
    # 反序列化
    restored = HyperLogLog.from_bytes(data)
    print(f"恢复后估计: {restored.count():.0f}")
    
    # 保存到文件
    import tempfile
    import os
    
    with tempfile.NamedTemporaryFile(delete=False, suffix='.hll') as f:
        temp_path = f.name
    
    try:
        hll.save(temp_path)
        print(f"已保存到文件: {temp_path}")
        print(f"文件大小: {os.path.getsize(temp_path)} 字节")
        
        # 从文件加载
        loaded = HyperLogLog.load(temp_path)
        print(f"从文件加载后估计: {loaded.count():.0f}")
    finally:
        os.unlink(temp_path)


def example_builder():
    """构建器示例"""
    print("\n" + "=" * 60)
    print("示例 8: 使用构建器 API")
    print("=" * 60)
    
    # 使用流畅 API 构建
    hll = (HyperLogLogBuilder()
           .precision(12)
           .with_hash('murmur')
           .with_items(['apple', 'banana', 'cherry', 'date', 'elderberry'])
           .build())
    
    print(f"估计基数: {hll.count():.0f}")
    print(f"精度: {hll.precision}")


def example_precision_comparison():
    """精度比较示例"""
    print("\n" + "=" * 60)
    print("示例 9: 不同精度比较")
    print("=" * 60)
    
    # 创建测试数据
    items = [f"precision_test_{i}" for i in range(1000)]
    
    # 比较不同精度
    results = compare_precision(items, precisions=[8, 10, 12, 14, 16])
    
    print("\n精度比较结果:")
    print("-" * 60)
    print(f"{'精度':<8}{'估计值':<12}{'误差%':<10}{'内存(KB)':<12}{'时间(us)':<10}")
    print("-" * 60)
    
    for p, data in results.items():
        print(f"{p:<8}{data['estimated']:<12.0f}{data['error_percent']:<10.2f}"
              f"{data['memory_bytes']/1024:<12.2f}{data['avg_add_us']:<10.3f}")


def example_memory_estimation():
    """内存估算示例"""
    print("\n" + "=" * 60)
    print("示例 10: 内存使用估算")
    print("=" * 60)
    
    print("\n不同精度的内存使用和误差:")
    print("-" * 60)
    print(f"{'精度':<8}{'寄存器数':<12}{'内存(KB)':<12}{'误差%':<10}")
    print("-" * 60)
    
    for p in [4, 6, 8, 10, 12, 14, 16]:
        info = estimate_memory(p)
        print(f"{p:<8}{info['num_registers']:<12}{info['kilobytes']:<12}"
              f"{info['relative_error_percent']:<10.2f}")
    
    print("\n选择精度建议:")
    print("  - 精度 10-12: 适合一般应用，内存 < 4KB")
    print("  - 精度 14-16: 高精度应用，误差 < 1%")


def example_set_operations():
    """集合操作示例"""
    print("\n" + "=" * 60)
    print("示例 11: 集合操作")
    print("=" * 60)
    
    # 创建两个数据集
    hll_a = HyperLogLog(precision=12)
    hll_b = HyperLogLog(precision=12)
    
    # 集合 A: 0-800
    for i in range(800):
        hll_a.add(f"set_a_{i}")
    
    # 集合 B: 400-1200（交集是 400-800）
    for i in range(400, 1200):
        hll_b.add(f"set_a_{i}")  # 共享部分
        if i >= 800:
            hll_b.add(f"set_b_{i}")  # B 特有部分
    
    print(f"集合 A 估计: {hll_a.count():.0f}")
    print(f"集合 B 估计: {hll_b.count():.0f}")
    
    # 并集
    union = hll_a.merge(hll_b)
    print(f"\n并集估计: {union.count():.0f}")
    
    # 交集
    intersection = hll_a.intersection_cardinality(hll_b)
    print(f"交集估计: {intersection:.0f}")
    
    # Jaccard 相似度
    jaccard = hll_a.jaccard_similarity(hll_b)
    print(f"Jaccard 相似度: {jaccard:.3f}")


def example_real_world_usage():
    """实际应用场景示例"""
    print("\n" + "=" * 60)
    print("示例 12: 实际应用场景")
    print("=" * 60)
    
    print("\n场景 1: API 调用统计")
    api_hll = HyperLogLog(precision=12)
    
    # 模拟不同 API 被不同用户调用
    apis = ['/api/users', '/api/products', '/api/orders', '/api/search']
    for api in apis:
        for user in range(100):
            api_hll.add(f"{api}:user_{user}")
    
    print(f"  总调用量: {len(apis) * 100}")
    print(f"  独立调用组合: {api_hll.count():.0f}")
    
    print("\n场景 2: 地理位置统计")
    geo_hll = HyperLogLog(precision=14)
    
    cities = ['北京', '上海', '广州', '深圳', '杭州', '成都', '武汉']
    for city in cities:
        for user in range(1000):
            geo_hll.add(f"{city}:{user}")
    
    print(f"  城市-用户组合: {geo_hll.count():.0f}")
    print(f"  实际组合数: {len(cities) * 1000}")
    
    print("\n场景 3: 搜索词统计")
    search_hll = HyperLogLog(precision=12)
    
    keywords = ['手机', '电脑', '衣服', '食品', '图书', '家电', '家具']
    for keyword in keywords:
        for variation in range(100):
            search_hll.add(f"{keyword}_v{variation}")
    
    print(f"  搜索词组合: {search_hll.count():.0f}")


def main():
    """运行所有示例"""
    print("=" * 60)
    print("HyperLogLog Utils 使用示例")
    print("=" * 60)
    
    example_basic_usage()
    example_uv_counting()
    example_large_scale()
    example_merge()
    example_hyperloglog_plusplus()
    example_sparse_hll()
    example_serialization()
    example_builder()
    example_precision_comparison()
    example_memory_estimation()
    example_set_operations()
    example_real_world_usage()
    
    print("\n" + "=" * 60)
    print("所有示例完成!")
    print("=" * 60)


if __name__ == '__main__':
    main()
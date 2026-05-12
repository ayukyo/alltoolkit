"""
T-Digest 使用示例

演示各种使用场景和功能
"""

import sys
sys.path.insert(0, '..')
from mod import (
    TDigest,
    create_digest,
    quantiles,
    percentile_summary
)
import random


def example_basic_usage():
    """基本使用示例"""
    print("=" * 60)
    print("基本使用示例")
    print("=" * 60)
    
    # 创建 T-Digest
    td = TDigest(compression=100)
    
    print(f"\n创建 T-Digest: {td}")
    
    # 添加数据
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    td.batch_add(data)
    
    print(f"添加了 {len(data)} 个数据点")
    print(f"质心数量: {td.size()}")
    
    # 计算分位数
    print("\n分位数统计:")
    print(f"  最小值: {td.min_val}")
    print(f"  10th 百分位: {td.percentile(10):.2f}")
    print(f"  中位数: {td.median():.2f}")
    print(f"  90th 百分位: {td.percentile(90):.2f}")
    print(f"  最大值: {td.max_val}")


def example_large_dataset():
    """大数据集示例"""
    print("\n" + "=" * 60)
    print("大数据集示例 - 100 万数据点")
    print("=" * 60)
    
    td = TDigest(compression=200)
    
    # 生成正态分布数据
    random.seed(42)
    print("\n生成 1,000,000 个正态分布数据点...")
    
    batch_size = 10000
    for _ in range(100):
        batch = [random.gauss(100, 15) for _ in range(batch_size)]
        td.batch_add(batch)
    
    print(f"数据点数: {len(td)}")
    print(f"质心数量: {td.size()}")
    print(f"压缩比: {len(td) / td.size():.0f}x")
    
    print("\n统计摘要:")
    print(f"  均值: {td.mean():.2f}")
    print(f"  标准差: {td.std_dev():.2f}")
    print(f"  中位数: {td.median():.2f}")
    print(f"  IQR: {td.iqr():.2f}")
    
    print("\n百分位数:")
    for p in [50, 75, 90, 95, 99]:
        print(f"  P{p}: {td.percentile(p):.2f}")


def example_latency_monitoring():
    """API 延迟监控示例"""
    print("\n" + "=" * 60)
    print("API 延迟监控示例")
    print("=" * 60)
    
    # 模拟 API 延迟数据
    random.seed(42)
    
    # 创建 T-Digest 用于延迟监控
    latency_td = TDigest(compression=100)
    
    # 模拟 1 小时的 API 请求延迟 (毫秒)
    print("\n模拟 1 小时的 API 请求...")
    
    for _ in range(10000):
        # 大多数请求很快，少数请求很慢
        if random.random() < 0.95:
            # 95% 的请求：正常延迟
            latency = random.gauss(50, 10)
        else:
            # 5% 的请求：慢请求
            latency = random.gauss(200, 50)
        
        latency_td.add(max(1, latency))  # 确保延迟为正
    
    print(f"\n请求总数: {len(latency_td)}")
    print("\n延迟统计:")
    print(f"  最小延迟: {latency_td.min_val:.2f} ms")
    print(f"  平均延迟: {latency_td.mean():.2f} ms")
    print(f"  中位延迟 (P50): {latency_td.median():.2f} ms")
    print(f"  P95 延迟: {latency_td.percentile(95):.2f} ms")
    print(f"  P99 延迟: {latency_td.percentile(99):.2f} ms")
    print(f"  最大延迟: {latency_td.max_val:.2f} ms")
    
    # 判断服务等级
    p99 = latency_td.percentile(99)
    if p99 < 100:
        level = "优秀 ⭐⭐⭐"
    elif p99 < 200:
        level = "良好 ⭐⭐"
    else:
        level = "需要优化 ⭐"
    
    print(f"\n服务等级: {level}")


def example_distributed_merge():
    """分布式合并示例"""
    print("\n" + "=" * 60)
    print("分布式合并示例")
    print("=" * 60)
    
    # 模拟多个节点分别收集数据
    random.seed(42)
    
    print("\n模拟 3 个节点收集数据...")
    
    # 节点 1: 东部数据中心
    td_east = TDigest(compression=100)
    td_east.batch_add([random.gauss(100, 15) for _ in range(3000)])
    
    # 节点 2: 西部数据中心
    td_west = TDigest(compression=100)
    td_west.batch_add([random.gauss(105, 12) for _ in range(3000)])
    
    # 节点 3: 欧洲数据中心
    td_eu = TDigest(compression=100)
    td_eu.batch_add([random.gauss(95, 18) for _ in range(3000)])
    
    print(f"\n节点统计:")
    print(f"  东部: {len(td_east)} 数据点, 中位数 = {td_east.median():.2f}")
    print(f"  西部: {len(td_west)} 数据点, 中位数 = {td_west.median():.2f}")
    print(f"  欧洲: {len(td_eu)} 数据点, 中位数 = {td_eu.median():.2f}")
    
    # 合并所有节点
    td_global = td_east.merge(td_west).merge(td_eu)
    
    print(f"\n合并后全局统计:")
    print(f"  总数据点: {len(td_global)}")
    print(f"  质心数量: {td_global.size()}")
    print(f"  全局中位数: {td_global.median():.2f}")
    print(f"  全局均值: {td_global.mean():.2f}")
    print(f"  全局标准差: {td_global.std_dev():.2f}")


def example_realtime_streaming():
    """实时流处理示例"""
    print("\n" + "=" * 60)
    print("实时流处理示例")
    print("=" * 60)
    
    random.seed(42)
    
    # 创建 T-Digest 用于实时监控
    td = TDigest(compression=50)
    
    print("\n模拟实时数据流...")
    
    # 模拟数据流
    for i in range(100):
        # 添加新数据点
        value = random.gauss(50, 10)
        td.add(value)
        
        # 每 20 个数据点输出一次统计
        if (i + 1) % 20 == 0:
            print(f"\n  [{i+1} 个数据点]")
            print(f"    当前中位数: {td.median():.2f}")
            print(f"    当前均值: {td.mean():.2f}")
            print(f"    质心数量: {td.size()}")


def example_serialization():
    """序列化示例"""
    print("\n" + "=" * 60)
    print("序列化示例")
    print("=" * 60)
    
    # 创建并填充 T-Digest
    td1 = TDigest(compression=100)
    td1.batch_add([random.gauss(100, 15) for _ in range(1000)])
    
    print(f"\n原始 T-Digest:")
    print(f"  数据点: {len(td1)}")
    print(f"  质心数量: {td1.size()}")
    print(f"  中位数: {td1.median():.2f}")
    
    # 序列化为字典
    data = td1.to_dict()
    
    print(f"\n序列化后:")
    print(f"  压缩参数: {data['compression']}")
    print(f"  质心数: {len(data['centroids'])}")
    print(f"  总权重: {data['total_weight']}")
    
    # 反序列化
    td2 = TDigest.from_dict(data)
    
    print(f"\n反序列化后:")
    print(f"  数据点: {len(td2)}")
    print(f"  质心数量: {td2.size()}")
    print(f"  中位数: {td2.median():.2f}")
    
    # 验证一致性
    print(f"\n中位数差异: {abs(td1.median() - td2.median()):.6f}")


def example_percentile_summary():
    """百分位数摘要示例"""
    print("\n" + "=" * 60)
    print("百分位数摘要示例")
    print("=" * 60)
    
    random.seed(42)
    data = [random.gauss(100, 15) for _ in range(1000)]
    
    summary = percentile_summary(data)
    
    print(f"\n数据摘要 ({summary['count']} 个数据点):")
    print(f"  最小值: {summary['min']:.2f}")
    print(f"  最大值: {summary['max']:.2f}")
    print(f"  均值: {summary['mean']:.2f}")
    print(f"  标准差: {summary['std_dev']:.2f}")
    print(f"\n百分位数:")
    print(f"  P10: {summary['p10']:.2f}")
    print(f"  P25: {summary['p25']:.2f}")
    print(f"  P50 (中位数): {summary['median']:.2f}")
    print(f"  P75: {summary['p75']:.2f}")
    print(f"  P90: {summary['p90']:.2f}")
    print(f"  P95: {summary['p95']:.2f}")
    print(f"  P99: {summary['p99']:.2f}")
    print(f"\n  IQR: {summary['iqr']:.2f}")
    print(f"  质心数量: {summary['centroids']}")


def example_ab_testing():
    """A/B 测试分析示例"""
    print("\n" + "=" * 60)
    print("A/B 测试分析示例")
    print("=" * 60)
    
    random.seed(42)
    
    # 模拟 A 组和 B 组的用户留存时间（秒）
    print("\n模拟两组用户的页面停留时间...")
    
    # A 组：旧设计
    td_a = TDigest(compression=100)
    td_a.batch_add([random.gauss(60, 20) for _ in range(1000)])
    
    # B 组：新设计
    td_b = TDigest(compression=100)
    td_b.batch_add([random.gauss(75, 18) for _ in range(1000)])
    
    print("\nA 组（旧设计）:")
    print(f"  用户数: {len(td_a)}")
    print(f"  平均停留: {td_a.mean():.1f} 秒")
    print(f"  中位停留: {td_a.median():.1f} 秒")
    print(f"  P95 停留: {td_a.percentile(95):.1f} 秒")
    
    print("\nB 组（新设计）:")
    print(f"  用户数: {len(td_b)}")
    print(f"  平均停留: {td_b.mean():.1f} 秒")
    print(f"  中位停留: {td_b.median():.1f} 秒")
    print(f"  P95 停留: {td_b.percentile(95):.1f} 秒")
    
    # 计算改进
    mean_improvement = (td_b.mean() - td_a.mean()) / td_a.mean() * 100
    median_improvement = (td_b.median() - td_a.median()) / td_a.median() * 100
    
    print(f"\n改进效果:")
    print(f"  平均停留提升: {mean_improvement:+.1f}%")
    print(f"  中位停留提升: {median_improvement:+.1f}%")


def main():
    """运行所有示例"""
    example_basic_usage()
    example_large_dataset()
    example_latency_monitoring()
    example_distributed_merge()
    example_realtime_streaming()
    example_serialization()
    example_percentile_summary()
    example_ab_testing()
    
    print("\n" + "=" * 60)
    print("所有示例完成!")
    print("=" * 60)


if __name__ == "__main__":
    main()
"""
Delta Encoding 工具模块使用示例

演示各种差分编码场景的实际应用
"""

import os
import sys

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime, timedelta
from mod import (
    DeltaEncoder,
    FloatDeltaEncoder,
    TimestampDeltaEncoder,
    DictionaryEncoder,
    DeltaEncodingStats,
    delta_encode,
    delta_decode,
    dict_encode,
    dict_decode
)


def example_01_basic_integer_encoding():
    """示例 01：基本整数差分编码"""
    print("=" * 60)
    print("示例 01：基本整数差分编码")
    print("=" * 60)
    
    # 场景：传感器读数序列（温度、湿度等）
    temperature_readings = [25, 26, 27, 26, 28, 29, 27, 26]
    
    print(f"原始温度读数: {temperature_readings}")
    print(f"原始数据大小: {len(temperature_readings) * 8} 字节 (假设 64位整数)")
    
    encoder = DeltaEncoder()
    encoded = encoder.encode(temperature_readings)
    print(f"差分编码结果: {encoded}")
    
    # 分析压缩效果
    stats = DeltaEncodingStats.analyze_integers(temperature_readings)
    print(f"编码后大小估算: {stats['encoded_size_bytes']} 字节")
    print(f"压缩比: {stats['compression_ratio']:.2f}x")
    print(f"平均差分: {stats['avg_delta']:.2f}")
    print(f"最大差分: {stats['max_delta']}, 最小差分: {stats['min_delta']}")
    
    # 解码验证
    decoded = encoder.decode(encoded)
    print(f"解码验证: {decoded}")
    assert decoded == temperature_readings, "解码结果不一致！"
    print("✓ 解码验证成功")


def example_02_stock_price_encoding():
    """示例 02：股票价格序列编码"""
    print("\n" + "=" * 60)
    print("示例 02：股票价格序列编码（浮点数 XOR 差分）")
    print("=" * 60)
    
    # 场景：股票价格时间序列
    prices = [
        100.50, 100.50, 100.75, 100.75, 100.75,  # 相似价格
        101.00, 101.25, 101.25, 100.75, 100.50   # 波动
    ]
    
    print(f"原始价格序列: {prices}")
    
    encoder = FloatDeltaEncoder()
    compact = encoder.encode_compact(prices)
    
    print(f"紧凑编码:")
    print(f"  首值 (整数表示): {compact['first_value']}")
    print(f"  XOR 差分序列: {compact['xor_deltas'][:5]}... (共 {len(compact['xor_deltas'])} 个)")
    
    # 分析 XOR 差分的特点
    xor_deltas = compact['xor_deltas']
    zero_count = sum(1 for x in xor_deltas if x == 0)
    print(f"  零 XOR 数量: {zero_count} ({zero_count/len(xor_deltas)*100:.1f}%)")
    print(f"  注: XOR=0 表示价格与前值相同，压缩效果显著")
    
    # 解码
    decoded = encoder.decode_compact(compact)
    print(f"解码结果: {decoded}")
    
    # 验证精度
    for i, (p1, p2) in enumerate(zip(prices, decoded)):
        if p1 != p2:
            print(f"警告: 位置 {i} 精度差异: {p1} vs {p2}")
    print("✓ 所有价格精确匹配")


def example_03_time_series_encoding():
    """示例 03：时间序列数据编码"""
    print("\n" + "=" * 60)
    print("示例 03：时间序列数据编码")
    print("=" * 60)
    
    # 场景：日志事件时间戳（近似等间隔）
    base_time = datetime(2024, 1, 15, 10, 0, 0)
    events = [
        base_time,
        base_time + timedelta(seconds=10),
        base_time + timedelta(seconds=20),
        base_time + timedelta(seconds=30),
        base_time + timedelta(seconds=40),
        base_time + timedelta(seconds=50),
        base_time + timedelta(seconds=60)
    ]
    
    print(f"事件时间序列 (7个事件，间隔10秒):")
    for i, t in enumerate(events):
        print(f"  [{i}] {t.strftime('%H:%M:%S')}")
    
    encoder = TimestampDeltaEncoder(unit='ms')
    
    # 一阶差分编码
    base_ts, deltas = encoder.encode(events)
    print(f"\n一阶差分编码:")
    print(f"  基准时间戳: {base_ts} ms")
    print(f"  差分序列: {deltas}")
    print(f"  差分特点: 全部为 10000ms (10秒间隔)")
    
    # 二阶差分编码（Delta-of-Delta）
    dod_encoded = encoder.encode_with_delta_of_delta(events)
    print(f"\n二阶差分编码 (Delta-of-Delta):")
    print(f"  基准时间戳: {dod_encoded['base_ts']}")
    print(f"  首差分: {dod_encoded['first_delta']}")
    print(f"  二阶差分: {dod_encoded['dod']}")
    print(f"  特点: 等间隔时，二阶差分几乎全为 0，压缩极高效")
    
    # 解码验证
    decoded = encoder.decode_with_delta_of_delta(dod_encoded)
    print(f"\n解码验证:")
    for i, t in enumerate(decoded[:3]):
        print(f"  [{i}] {t.strftime('%H:%M:%S')}")
    assert decoded == events, "解码结果不一致！"
    print("✓ 解码验证成功")


def example_04_irregular_timestamps():
    """示例 04：不等间隔时间戳"""
    print("\n" + "=" * 60)
    print("示例 04：不等间隔时间戳（突发事件）")
    print("=" * 60)
    
    # 场景：突发事件，间隔变化大
    base = datetime(2024, 1, 15, 14, 30, 0)
    burst_events = [
        base,
        base + timedelta(seconds=1),
        base + timedelta(seconds=2),
        base + timedelta(seconds=3),
        base + timedelta(minutes=5),
        base + timedelta(minutes=5, seconds=1),
        base + timedelta(hours=1)
    ]
    
    print("突发事件时间戳:")
    for i, t in enumerate(burst_events):
        print(f"  [{i}] {t.strftime('%H:%M:%S')}")
    
    encoder = TimestampDeltaEncoder()
    dod_encoded = encoder.encode_with_delta_of_delta(burst_events)
    
    print(f"\n二阶差分分析:")
    print(f"  首差分 (ms): {dod_encoded['first_delta']}")
    
    # 分析间隔变化
    dod = dod_encoded['dod']
    print(f"  二阶差分序列: {dod[:4]}... (共 {len(dod)} 个)")
    
    # 找出间隔突变点
    large_changes = [i for i, d in enumerate(dod) if abs(d) > 1000]
    print(f"  间隔突变点索引: {large_changes}")
    
    # 解码
    decoded = encoder.decode_with_delta_of_delta(dod_encoded)
    assert decoded == burst_events
    print("✓ 解码验证成功")


def example_05_log_message_encoding():
    """示例 05：日志消息字典编码"""
    print("\n" + "=" * 60)
    print("示例 05：日志消息字典编码")
    print("=" * 60)
    
    # 场景：系统日志，重复消息多
    log_messages = [
        "User login successful",
        "Connection established",
        "User login successful",
        "Query executed",
        "User login successful",
        "Connection established",
        "User login successful",
        "Cache hit",
        "Query executed",
        "User login successful"
    ]
    
    print(f"日志消息序列 (共 {len(log_messages)} 条):")
    unique_messages = set(log_messages)
    print(f"  唯一消息数: {len(unique_messages)}")
    print(f"  消息类型: {list(unique_messages)}")
    
    # 字典编码
    ids, dictionary = dict_encode(log_messages)
    
    print(f"\n字典编码结果:")
    print(f"  ID 序列: {ids}")
    print(f"  字典映射:")
    for msg, id_ in dictionary.items():
        count = log_messages.count(msg)
        print(f"    '{msg}' -> {id_} (出现 {count} 次)")
    
    # 分析压缩效果
    stats = DeltaEncodingStats.analyze_strings(log_messages)
    print(f"\n压缩效果:")
    print(f"  原始大小: {stats['original_size_bytes']} 字节")
    print(f"  编码大小: {stats['encoded_size_bytes']} 字节")
    print(f"  压缩比: {stats['compression_ratio']:.2f}x")
    print(f"  冗余率: {stats['redundancy_ratio']:.1%}")
    
    # 解码
    decoded = dict_decode(ids, dictionary)
    assert decoded == log_messages
    print("✓ 解码验证成功")


def example_06_combined_encoding():
    """示例 06：组合编码 - 时间序列 + 值"""
    print("\n" + "=" * 60)
    print("示例 06：组合编码（时间戳 + 数值）")
    print("=" * 60)
    
    # 场景：完整的时间序列数据点
    base_time = datetime(2024, 1, 20, 8, 0, 0)
    
    # 创建数据点
    data_points = []
    for i in range(10):
        timestamp = base_time + timedelta(minutes=i)
        value = 100 + i * 5 + (i % 3)  # 基本递增 + 小波动
        data_points.append((timestamp, value))
    
    print("原始数据点:")
    for i, (t, v) in enumerate(data_points[:5]):
        print(f"  [{i}] {t.strftime('%H:%M')} -> {v}")
    
    # 分离时间戳和值
    timestamps = [p[0] for p in data_points]
    values = [p[1] for p in data_points]
    
    # 分别编码
    ts_encoder = TimestampDeltaEncoder()
    ts_encoded = ts_encoder.encode_with_delta_of_delta(timestamps)
    
    val_encoder = DeltaEncoder()
    val_encoded = val_encoder.encode(values)
    
    print(f"\n组合编码结果:")
    print(f"  时间戳:")
    print(f"    基准: {ts_encoded['base_ts']}")
    print(f"    首差分: {ts_encoded['first_delta']}")
    print(f"    二阶差分: {ts_encoded['dod']}")
    
    print(f"  数值:")
    print(f"    差分编码: {val_encoded}")
    
    # 解码组合
    decoded_timestamps = ts_encoder.decode_with_delta_of_delta(ts_encoded)
    decoded_values = val_encoder.decode(val_encoded)
    
    decoded_points = list(zip(decoded_timestamps, decoded_values))
    
    print(f"\n解码验证:")
    for i, (t, v) in enumerate(decoded_points[:3]):
        print(f"  [{i}] {t.strftime('%H:%M')} -> {v}")
    
    assert decoded_points == data_points
    print("✓ 组合解码验证成功")


def example_07_negative_deltas():
    """示例 07：处理负差分"""
    print("\n" + "=" * 60)
    print("示例 07：处理负差分（ZigZag 编码）")
    print("=" * 60)
    
    # 场景：股票价格波动（包含下跌）
    stock_changes = [100, 105, 98, 102, 95, 110, 108, 115, 105]
    
    print(f"价格序列 (包含下跌): {stock_changes}")
    
    # 计算原始差分
    raw_deltas = [stock_changes[i] - stock_changes[i-1] for i in range(1, len(stock_changes))]
    print(f"原始差分: {raw_deltas} (包含负数)")
    
    # 使用 ZigZag 编码
    encoder_zigzag = DeltaEncoder(use_zigzag=True)
    encoded_zigzag = encoder_zigzag.encode(stock_changes)
    print(f"ZigZag 编码差分: {encoded_zigzag[1:]} (全为正数)")
    
    # 不使用 ZigZag（保留负数）
    encoder_raw = DeltaEncoder(use_zigzag=False)
    encoded_raw = encoder_raw.encode(stock_changes)
    print(f"原始差分编码: {encoded_raw[1:]} (保留负数)")
    
    # ZigZag 编码优势解释
    print(f"\nZigZag 编码优势:")
    print(f"  -1 -> 1  (负数映射到正奇数)")
    print(f"  -7 -> 13 (更小的负数映射到更大的正奇数)")
    print(f"  适用于变长整数编码，正数通常编码效率更高")
    
    # 解码验证
    decoded_zigzag = encoder_zigzag.decode(encoded_zigzag)
    decoded_raw = encoder_raw.decode(encoded_raw)
    
    assert decoded_zigzag == stock_changes
    assert decoded_raw == stock_changes
    print("✓ 两种编码方式解码均成功")


def example_08_compression_comparison():
    """示例 08：压缩效果对比"""
    print("\n" + "=" * 60)
    print("示例 08：不同数据模式的压缩效果对比")
    print("=" * 60)
    
    test_cases = [
        ("常量序列", [100, 100, 100, 100, 100, 100, 100, 100]),
        ("线性递增", [100, 101, 102, 103, 104, 105, 106, 107]),
        ("小幅波动", [100, 102, 99, 101, 103, 98, 102, 100]),
        ("大幅跳跃", [100, 500, 1000, 5000, 10000, 50000, 100000]),
        ("随机波动", [100, 95, 110, 85, 120, 75, 130, 65])
    ]
    
    print("\n压缩效果对比表:")
    print("-" * 60)
    print(f"{'数据类型':<12} {'原始大小':<10} {'编码大小':<10} {'压缩比':<10} {'平均差分':<10}")
    print("-" * 60)
    
    for name, values in test_cases:
        stats = DeltaEncodingStats.analyze_integers(values)
        print(f"{name:<12} {stats['original_size_bytes']:<10} "
              f"{stats['encoded_size_bytes']:<10} "
              f"{stats['compression_ratio']:<10.2f} "
              f"{stats['avg_delta']:<10.1f}")
    
    print("-" * 60)
    print("\n结论:")
    print("  - 常量序列：压缩效果最佳（差分全为 0）")
    print("  - 线性递增：压缩效果好（差分相同）")
    print("  - 小幅波动：压缩效果较好")
    print("  - 大幅跳跃：压缩效果差")
    print("  - 随机波动：压缩效果最差")


def main():
    """运行所有示例"""
    example_01_basic_integer_encoding()
    example_02_stock_price_encoding()
    example_03_time_series_encoding()
    example_04_irregular_timestamps()
    example_05_log_message_encoding()
    example_06_combined_encoding()
    example_07_negative_deltas()
    example_08_compression_comparison()
    
    print("\n" + "=" * 60)
    print("所有示例运行完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
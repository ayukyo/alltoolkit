"""
考拉兹猜想工具模块使用示例

考拉兹猜想（3n+1问题）是数学中最著名的未解问题之一。
本示例展示如何使用 collatz_utils 工具模块探索这个有趣的数学现象。
"""

import os
import sys
# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mod import (
    collatz_step,
    generate_sequence,
    get_steps_to_one,
    get_max_value,
    analyze,
    find_longest_sequence,
    find_highest_value,
    verify_conjecture,
    format_sequence,
    get_statistics,
    CollatzSequence,
    get_stopping_time,
    get_eta,
)


def example_basic_operations():
    """示例1：基本操作"""
    print("\n" + "=" * 60)
    print("示例1：基本考拉兹变换")
    print("=" * 60)
    
    # 单步变换
    print("\n单步考拉兹变换:")
    numbers = [1, 2, 3, 5, 7, 10, 20]
    for n in numbers:
        result = collatz_step(n)
        parity = "偶数" if n % 2 == 0 else "奇数"
        operation = "n/2" if n % 2 == 0 else "3n+1"
        print(f"  {n} ({parity}) → {result} ({operation})")
    
    # 生成完整序列
    print("\n生成完整序列:")
    for n in [6, 7, 10]:
        seq = generate_sequence(n)
        print(f"  从 {n} 开始: {len(seq)} 步 → {format_sequence(n)}")


def example_famous_number_27():
    """示例2：著名的数字27"""
    print("\n" + "=" * 60)
    print("示例2：著名的数字27（最长序列之一）")
    print("=" * 60)
    
    # 数字27是考拉兹研究中的著名例子
    result = analyze(27)
    
    print(f"\n数字 27 的考拉兹序列分析:")
    print(f"  • 起始值: {result['start_value']}")
    print(f"  • 到达1的步数: {result['steps']} 步")
    print(f"  • 序列长度: {result['sequence_length']} 个数字")
    print(f"  • 最大值: {result['max_value']}")
    print(f"  • 最大值出现位置: 第 {result['max_value_step']} 步")
    print(f"  • 奇数操作次数: {result['odd_count']}")
    print(f"  • 偶数操作次数: {result['even_count']}")
    
    print(f"\n  序列前20个数字: {result['sequence'][:20]}...")
    print(f"  序列最后10个数字: ...{result['sequence'][-10:]}")


def example_sequence_comparison():
    """示例3：序列比较"""
    print("\n" + "=" * 60)
    print("示例3：不同数字的序列比较")
    print("=" * 60)
    
    print("\n比较 1-20 范围内的考拉兹序列:")
    print(f"{'数字':<6} {'步数':<6} {'最大值':<10} {'序列长度':<10}")
    print("-" * 40)
    
    for n in range(1, 21):
        steps = get_steps_to_one(n)
        max_val = get_max_value(n)
        seq_len = len(generate_sequence(n))
        print(f"{n:<6} {steps:<6} {max_val:<10} {seq_len:<10}")


def example_find_records():
    """示例4：寻找记录"""
    print("\n" + "=" * 60)
    print("示例4：寻找考拉兹记录")
    print("=" * 60)
    
    # 找最长序列
    limit = 1000
    n, steps = find_longest_sequence(limit)
    print(f"\n在 1-{limit} 范围内:")
    print(f"  • 最长序列起始数: {n}")
    print(f"  • 所需步数: {steps} 步")
    
    # 找最高值
    n, val = find_highest_value(limit)
    print(f"\n  • 产生最高值的起始数: {n}")
    print(f"  • 达到的最高值: {val}")
    
    # 扩大范围
    limit = 10000
    n, steps = find_longest_sequence(limit)
    print(f"\n在 1-{limit} 范围内:")
    print(f"  • 最长序列起始数: {n}")
    print(f"  • 所需步数: {steps} 步")


def example_verify_conjecture():
    """示例5：验证猜想"""
    print("\n" + "=" * 60)
    print("示例5：验证考拉兹猜想")
    print("=" * 60)
    
    print("\n考拉兹猜想：对于任意正整数 n，")
    print("经过有限步考拉兹变换后，最终都会到达 1。")
    
    # 验证不同范围
    for limit in [100, 1000, 10000, 100000]:
        verified, count = verify_conjecture(limit)
        status = "✓ 通过" if verified else "✗ 发现反例！"
        print(f"\n验证 1-{limit} 范围: {status} ({count} 个数)")


def example_statistics():
    """示例6：统计分析"""
    print("\n" + "=" * 60)
    print("示例6：考拉兹序列统计")
    print("=" * 60)
    
    # 获取统计信息
    stats = get_statistics(100)
    print(f"\n1-100 范围内的考拉兹序列统计:")
    print(f"  • 总数字数: {stats['total_numbers']}")
    print(f"  • 平均步数: {stats['average_steps']:.2f}")
    print(f"  • 最大步数: {stats['max_steps']} (数字 {stats['max_steps_number']})")
    print(f"  • 最大峰值: {stats['max_value']} (数字 {stats['max_value_number']})")
    print(f"  • 奇数操作总次数: {stats['total_odd_operations']}")
    print(f"  • 偶数操作总次数: {stats['total_even_operations']}")
    print(f"  • 奇偶操作比例: {stats['odd_even_ratio']:.4f}")


def example_class_interface():
    """示例7：使用类接口"""
    print("\n" + "=" * 60)
    print("示例7：使用 CollatzSequence 类")
    print("=" * 60)
    
    print("\nCollatzSequence 提供更优雅的接口:")
    
    # 创建序列对象
    seq = CollatzSequence(27)
    
    print(f"\n  创建序列: seq = CollatzSequence(27)")
    print(f"  • 起始值: seq.start = {seq.start}")
    print(f"  • 步数: seq.steps = {seq.steps}")
    print(f"  • 最大值: seq.max_value = {seq.max_value}")
    print(f"  • 序列长度: len(seq) = {len(seq)}")
    
    print(f"\n  迭代访问:")
    print(f"  • 前5个: {list(seq[:5])}")
    print(f"  • 最后3个: {list(seq[-3:])}")
    
    print(f"\n  字符串表示:")
    print(f"  • repr(seq) = {repr(seq)}")
    print(f"  • str(seq) = {str(seq)[:50]}...")


def example_special_measures():
    """示例8：特殊度量"""
    print("\n" + "=" * 60)
    print("示例8：考拉兹特殊度量")
    print("=" * 60)
    
    print("\n停止时间 (Stopping Time):")
    print("定义：首次降到起始值以下所需的步数")
    
    for n in [6, 7, 15, 27]:
        st = get_stopping_time(n)
        print(f"  数字 {n} 的停止时间: {st}")
    
    print("\nEta (扩充时间):")
    print("定义：序列达到最大值所需的步数")
    
    for n in [6, 27, 100]:
        eta = get_eta(n)
        max_val = get_max_value(n)
        print(f"  数字 {n}: Eta = {eta}, 最大值 = {max_val}")


def example_visual_pattern():
    """示例9：视觉模式"""
    print("\n" + "=" * 60)
    print("示例9：考拉兹序列的视觉模式")
    print("=" * 60)
    
    print("\n序列上升和下降的模式:")
    
    for n in [6, 27, 100]:
        seq = generate_sequence(n)
        
        # 分析上升和下降段落
        rising_count = 0
        falling_count = 0
        
        for i in range(1, len(seq)):
            if seq[i] > seq[i-1]:
                rising_count += 1
            else:
                falling_count += 1
        
        print(f"\n  数字 {n}:")
        print(f"    • 序列: {format_sequence(n)[:50]}...")
        print(f"    • 上升次数: {rising_count}")
        print(f"    • 下降次数: {falling_count}")
        print(f"    • 上升/下降比例: {rising_count/falling_count:.2f}")


def example_power_of_two():
    """示例10：2的幂次"""
    print("\n" + "=" * 60)
    print("示例10：2的幂次的特殊性质")
    print("=" * 60)
    
    print("\n2的幂次有最短的考拉兹序列（直接除以2到底）:")
    
    for i in range(1, 11):
        n = 2 ** i
        seq = generate_sequence(n)
        steps = get_steps_to_one(n)
        
        print(f"  2^{i} = {n:>4}: {steps} 步 → {format_sequence(n)}")


if __name__ == "__main__":
    print("考拉兹猜想工具模块使用示例")
    print("=" * 60)
    
    # 运行所有示例
    example_basic_operations()
    example_famous_number_27()
    example_sequence_comparison()
    example_find_records()
    example_verify_conjecture()
    example_statistics()
    example_class_interface()
    example_special_measures()
    example_visual_pattern()
    example_power_of_two()
    
    print("\n" + "=" * 60)
    print("示例结束")
    print("=" * 60)
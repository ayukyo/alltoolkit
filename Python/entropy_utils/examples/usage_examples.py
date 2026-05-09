#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - 熵计算工具使用示例
Entropy Utilities Usage Examples

@module: entropy_utils
"""

import sys
import os

# 添加模块路径（从examples目录向上到模块目录）
module_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, module_dir)

from mod import (
    EntropyUtils, PasswordEntropy, DataEntropyAnalyzer,
    shannon_entropy, analyze_password, entropy_report
)


def example_1_basic_entropy():
    """示例1: 基本熵计算"""
    print("\n" + "=" * 60)
    print("示例1: 基本熵计算")
    print("=" * 60)
    
    test_cases = [
        "Hello, World!",
        "aaaaaa",           # 低熵
        "abcdef",           # 中熵
        "aB1!xY2@",         # 高熵（混合字符）
        "密码测试123",       # Unicode
        bytes(range(256)),  # 所有字节值
    ]
    
    for data in test_cases:
        if isinstance(data, bytes):
            shannon = EntropyUtils.shannon_entropy(data)
            min_ent = EntropyUtils.min_entropy(data)
            print(f"\n字节数据(0-255):")
        else:
            shannon = EntropyUtils.shannon_entropy(data)
            min_ent = EntropyUtils.min_entropy(data)
            print(f"\n字符串: '{data}'")
        
        print(f"  香农熵: {shannon:.4f} bits/符号")
        print(f"  最小熵: {min_ent:.4f} bits")
        print(f"  基尼不纯度: {EntropyUtils.gini_impurity(data):.4f}")
        print(f"  归一化熵: {EntropyUtils.shannon_entropy_normalized(data):.4f}")


def example_2_password_analysis():
    """示例2: 密码强度分析"""
    print("\n" + "=" * 60)
    print("示例2: 密码强度分析")
    print("=" * 60)
    
    analyzer = PasswordEntropy()
    passwords = [
        "123456",
        "password",
        "qwerty",
        "abc123",
        "MyPassword",
        "MyP@ssw0rd",
        "Tr0ub4dor&3",
        "CorrectHorseBatteryStaple",
        "密码测试!@#$2024",
    ]
    
    print(f"\n{'密码':<30} {'熵(bits)':<12} {'强度':<10} {'破解时间':<20}")
    print("-" * 72)
    
    for pwd in passwords:
        result = analyzer.analyze(pwd)
        # 隐藏部分密码字符
        display_pwd = pwd[:15] + "..." if len(pwd) > 15 else pwd
        print(f"{display_pwd:<30} {result.entropy:<12.2f} {result.strength:<10} {result.crack_time_estimate:<20}")
    
    # 详细分析一个密码
    print("\n" + "-" * 60)
    print("详细分析: 'MyP@ssw0rd!'")
    result = analyzer.analyze("MyP@ssw0rd!")
    print(f"  长度: {result.length}")
    print(f"  熵值: {result.entropy} bits")
    print(f"  每字符熵: {result.entropy_per_char} bits")
    print(f"  字符集大小: {result.charset_size}")
    print(f"  包含小写: {result.has_lowercase}")
    print(f"  包含大写: {result.has_uppercase}")
    print(f"  包含数字: {result.has_digits}")
    print(f"  包含特殊字符: {result.has_special}")
    print(f"  是常见密码: {result.is_common}")
    print(f"  强度评级: {result.strength}")
    print(f"  预估破解时间: {result.crack_time_estimate}")
    if result.suggestions:
        print(f"  改进建议:")
        for s in result.suggestions:
            print(f"    - {s}")


def example_3_data_analysis():
    """示例3: 数据分布分析"""
    print("\n" + "=" * 60)
    print("示例3: 数据分布分析")
    print("=" * 60)
    
    # 示例数据
    datasets = {
        "英文文本": "The quick brown fox jumps over the lazy dog. " * 5,
        "重复模式": "abcabcabcabcabc",
        "低熵数据": "aaaaaaaaaaaa",
        "随机字符": "xK9#mP2$vL5@nQ8&wR3!",
        "数字序列": "12345678901234567890",
    }
    
    for name, data in datasets.items():
        print(f"\n【{name}】")
        print(f"  数据: '{data[:30]}...'" if len(data) > 30 else f"  数据: '{data}'")
        
        analysis = EntropyUtils.analyze_distribution(data)
        print(f"  香农熵: {analysis['shannon_entropy']} bits/符号")
        print(f"  最小熵: {analysis['min_entropy']} bits")
        print(f"  最大可能熵: {analysis['max_entropy']} bits")
        print(f"  熵效率: {analysis['normalized_entropy'] * 100:.1f}%")
        print(f"  基尼不纯度: {analysis['gini_impurity']}")
        print(f"  唯一符号数: {analysis['unique_count']}")
        print(f"  总符号数: {analysis['total_count']}")
        print(f"  压缩潜力: {analysis['compression_potential'] * 100:.1f}%")
        print(f"  随机性得分: {analysis['randomness_score']:.4f}")
        print(f"  最常见符号: {analysis['top_symbols'][:3]}")


def example_4_information_theory():
    """示例4: 信息论计算"""
    print("\n" + "=" * 60)
    print("示例4: 信息论计算")
    print("=" * 60)
    
    # 互信息
    print("\n【互信息】")
    x = [1, 1, 2, 2, 3, 3, 4, 4]
    y = [1, 2, 1, 2, 3, 4, 3, 4]  # 部分相关
    z = [1, 2, 3, 4, 5, 6, 7, 8]  # 与x不同
    
    mi_xy = EntropyUtils.mutual_information(x, y)
    mi_xz = EntropyUtils.mutual_information(x, z)
    
    print(f"  X = {x}")
    print(f"  Y = {y}")
    print(f"  Z = {z}")
    print(f"  I(X;Y) = {mi_xy:.4f} bits")
    print(f"  I(X;Z) = {mi_xz:.4f} bits")
    
    # 条件熵
    print("\n【条件熵】")
    h_x = EntropyUtils.shannon_entropy(x)
    h_y = EntropyUtils.shannon_entropy(y)
    h_xy = EntropyUtils.joint_entropy(x, y)
    h_x_given_y = EntropyUtils.conditional_entropy(x, y)
    
    print(f"  H(X) = {h_x:.4f} bits")
    print(f"  H(Y) = {h_y:.4f} bits")
    print(f"  H(X,Y) = {h_xy:.4f} bits")
    print(f"  H(X|Y) = {h_x_given_y:.4f} bits")
    
    # KL散度
    print("\n【KL散度】")
    p = {'A': 0.4, 'B': 0.3, 'C': 0.2, 'D': 0.1}
    q = {'A': 0.25, 'B': 0.25, 'C': 0.25, 'D': 0.25}
    
    kl_pq = EntropyUtils.kl_divergence(p, q)
    kl_qp = EntropyUtils.kl_divergence(q, p)
    
    print(f"  P = {p}")
    print(f"  Q = {q}")
    print(f"  KL(P||Q) = {kl_pq:.4f} bits")
    print(f"  KL(Q||P) = {kl_qp:.4f} bits")
    print(f"  (注意KL散度的非对称性)")
    
    # 交叉熵
    print("\n【交叉熵】")
    ce_pq = EntropyUtils.cross_entropy(p, q)
    ce_pp = EntropyUtils.cross_entropy(p, p)
    
    print(f"  H(P,Q) = {ce_pq:.4f} bits")
    print(f"  H(P,P) = {ce_pp:.4f} bits (等于H(P))")


def example_5_renyi_entropy():
    """示例5: Rényi熵家族"""
    print("\n" + "=" * 60)
    print("示例5: Rényi熵家族")
    print("=" * 60)
    
    data = "aabbcc"
    print(f"\n数据: '{data}'")
    print(f"分布: p(a)=p(b)=p(c)=1/3")
    
    alphas = [0, 0.25, 0.5, 0.75, 1, 1.5, 2, 3, 4, float('inf')]
    
    print(f"\n{'α':<8} {'熵类型':<15} {'熵值':<10} {'说明'}")
    print("-" * 70)
    
    for alpha in alphas:
        if alpha == float('inf'):
            continue
        elif alpha == 0:
            name = "Hartley熵"
            desc = "log(|X|)"
        elif alpha == 1:
            name = "香农熵"
            desc = "H(X) = -Σp·log(p)"
        elif alpha == 2:
            name = "碰撞熵"
            desc = "用于随机性检验"
        else:
            name = f"Rényi熵(α={alpha})"
            desc = ""
        
        if alpha == 1:
            entropy = EntropyUtils.shannon_entropy(data)
        else:
            entropy = EntropyUtils.renyi_entropy(data, alpha)
        
        print(f"{alpha:<8.2f} {name:<15} {entropy:<10.4f} {desc}")
    
    # 最小熵
    min_ent = EntropyUtils.min_entropy(data)
    print(f"{'∞':<8} {'最小熵':<15} {min_ent:<10.4f} 最保守的熵度量")


def example_6_randomness_evaluation():
    """示例6: 随机性评估"""
    print("\n" + "=" * 60)
    print("示例6: 随机性评估")
    print("=" * 60)
    
    test_strings = [
        ("完全重复", "aaaaaaaaaa"),
        ("交替模式", "ababababab"),
        ("递增序列", "0123456789"),
        ("键盘模式", "qwertyuiop"),
        ("伪随机", "x7Km9Pq2Lz"),
        ("高熵数据", "aB3!xY7@qW2#"),
    ]
    
    print(f"\n{'类型':<12} {'数据':<15} {'香农熵':<10} {'随机性':<10} {'压缩潜力':<10}")
    print("-" * 60)
    
    for name, data in test_strings:
        shannon = EntropyUtils.shannon_entropy(data)
        random = EntropyUtils.randomness_score(data)
        compress = EntropyUtils.compression_potential(data)
        print(f"{name:<12} {data:<15} {shannon:<10.4f} {random:<10.4f} {compress:<10.4f}")


def example_7_data_entropy_analyzer():
    """示例7: 数据熵分析器"""
    print("\n" + "=" * 60)
    print("示例7: 数据熵分析器")
    print("=" * 60)
    
    # 创建分析器
    analyzer = DataEntropyAnalyzer(window_size=64)
    
    # 模拟数据：重复部分 + 随机部分 + 重复部分
    data = b"A" * 128 + bytes(range(256)) + b"B" * 128
    
    print(f"数据长度: {len(data)} bytes")
    print("数据结构: 128字节'A' + 256字节随机(0-255) + 128字节'B'")
    
    # 滑动窗口分析
    print("\n【滑动窗口熵分析】")
    results = analyzer.sliding_window_entropy(data, step=64)
    
    print(f"\n{'位置':<10} {'窗口熵值':<15} {'特征'}")
    print("-" * 40)
    for pos, entropy in results:
        if entropy < 1:
            feature = "低熵(重复)"
        elif entropy < 6:
            feature = "中熵"
        else:
            feature = "高熵(随机)"
        print(f"{pos:<10} {entropy:<15.4f} {feature}")
    
    # 检测高熵区域
    print("\n【高熵区域检测】")
    regions = analyzer.find_high_entropy_regions(data, threshold=7.0, min_length=32)
    
    if regions:
        print(f"\n发现 {len(regions)} 个高熵区域:")
        for start, end, avg_entropy in regions:
            print(f"  位置 {start}-{end}: 平均熵 {avg_entropy:.4f}")
    else:
        print("未检测到高熵区域")


def example_8_file_entropy():
    """示例8: 文件熵分析"""
    print("\n" + "=" * 60)
    print("示例8: 文件熵分析")
    print("=" * 60)
    
    import tempfile
    import os
    
    # 创建测试文件
    test_files = []
    
    # 1. 低熵文件（重复数据）
    with tempfile.NamedTemporaryFile(mode='wb', delete=False) as f:
        f.write(b"AAAAAAAAAA" * 1000)
        test_files.append(("重复数据", f.name))
    
    # 2. 高熵文件（伪随机）
    with tempfile.NamedTemporaryFile(mode='wb', delete=False) as f:
        import random
        random.seed(42)
        f.write(bytes([random.randint(0, 255) for _ in range(10000)]))
        test_files.append(("伪随机数据", f.name))
    
    # 3. 文本文件
    with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8') as f:
        f.write("Hello, World! " * 500)
        test_files.append(("文本数据", f.name))
    
    # 分析文件
    print(f"\n{'文件类型':<15} {'熵值':<15} {'说明'}")
    print("-" * 50)
    
    for name, filepath in test_files:
        try:
            entropy = EntropyUtils.file_entropy(filepath)
            if entropy < 2:
                desc = "高度重复，可压缩性好"
            elif entropy < 5:
                desc = "中等熵，有一定规律"
            elif entropy < 7:
                desc = "较高熵，随机性较强"
            else:
                desc = "高熵，接近随机数据"
            
            print(f"{name:<15} {entropy:<15.4f} {desc}")
        finally:
            os.unlink(filepath)


def example_9_convenience_functions():
    """示例9: 便捷函数使用"""
    print("\n" + "=" * 60)
    print("示例9: 便捷函数使用")
    print("=" * 60)
    
    # 香农熵
    print("\n【shannon_entropy() - 计算香农熵】")
    data = "hello world"
    entropy = shannon_entropy(data)
    print(f"  数据: '{data}'")
    print(f"  香农熵: {entropy:.4f} bits/符号")
    
    # 密码分析
    print("\n【analyze_password() - 分析密码】")
    result = analyze_password("MyP@ssw0rd123!")
    print(f"  密码长度: {result.length}")
    print(f"  熵值: {result.entropy} bits")
    print(f"  强度: {result.strength}")
    print(f"  破解时间: {result.crack_time_estimate}")
    
    # 熵报告
    print("\n【entropy_report() - 生成熵分析报告】")
    report = entropy_report("The quick brown fox jumps")
    print(f"  香农熵: {report['shannon_entropy']}")
    print(f"  最小熵: {report['min_entropy']}")
    print(f"  唯一符号: {report['unique_count']}")
    print(f"  压缩潜力: {report['compression_potential']}")
    print(f"  随机性得分: {report['randomness_score']}")


def example_10_password_strength_comparison():
    """示例10: 密码强度对比"""
    print("\n" + "=" * 60)
    print("示例10: 密码强度对比分析")
    print("=" * 60)
    
    analyzer = PasswordEntropy()
    
    passwords = [
        ("弱密码 - 纯数字", "123456"),
        ("弱密码 - 常见词", "password"),
        ("中等 - 混合字符", "Password1"),
        ("强 - 复杂组合", "P@ssw0rd!2024"),
        ("强 - 长密码", "correct-horse-battery-staple"),
        ("很强 - 高熵随机", "xK9#mP2$vL5@nQ8&wR3!zY6"),
    ]
    
    print(f"\n{'描述':<25} {'长度':<6} {'熵值':<12} {'强度':<10} {'破解时间'}")
    print("-" * 80)
    
    for desc, pwd in passwords:
        result = analyzer.analyze(pwd)
        print(f"{desc:<25} {result.length:<6} {result.entropy:<12.2f} {result.strength:<10} {result.crack_time_estimate}")
    
    print("\n" + "-" * 80)
    print("建议:")
    print("  1. 密码长度至少12个字符")
    print("  2. 混合使用大小写字母、数字、特殊字符")
    print("  3. 避免使用常见密码和字典词汇")
    print("  4. 熵值最好超过60 bits")
    print("  5. 考虑使用密码短语 (passphrase)")


def main():
    """运行所有示例"""
    print("=" * 60)
    print("AllToolkit - 熵计算工具使用示例")
    print("Entropy Utilities Usage Examples")
    print("=" * 60)
    
    example_1_basic_entropy()
    example_2_password_analysis()
    example_3_data_analysis()
    example_4_information_theory()
    example_5_renyi_entropy()
    example_6_randomness_evaluation()
    example_7_data_entropy_analyzer()
    example_8_file_entropy()
    example_9_convenience_functions()
    example_10_password_strength_comparison()
    
    print("\n" + "=" * 60)
    print("所有示例运行完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
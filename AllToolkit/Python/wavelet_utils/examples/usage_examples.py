"""
Wavelet Utils 使用示例

演示小波变换工具模块的各种应用场景。
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import math
import random
from mod import (
    WaveletBase,
    DiscreteWaveletTransform,
    WaveletPacketTransform,
    WaveletDenoiser,
    WaveletEnergyAnalyzer,
    WaveletCoefficients,
    dwt_decompose,
    dwt_reconstruct,
    denoise_signal,
    analyze_energy
)


def example_basic_dwt():
    """基本 DWT 分解与重构示例"""
    print("=" * 50)
    print("示例 1: 基本 DWT 分解与重构")
    print("=" * 50)
    
    # 创建信号
    signal = [1, 2, 3, 4, 5, 6, 7, 8]
    print(f"原始信号: {signal}")
    
    # 使用 Haar 小波分解
    dwt = DiscreteWaveletTransform('haar')
    coeffs = dwt.decompose(signal, levels=3)
    
    print(f"\n分解结果 (3层):")
    print(f"  近似系数 (低频): {coeffs.approximation}")
    for i, detail in enumerate(coeffs.details):
        print(f"  第{i+1}层细节 (高频): {detail}")
    
    # 重构
    reconstructed = dwt.reconstruct(coeffs)
    print(f"\n重构信号: {[round(x, 4) for x in reconstructed]}")
    
    # 计算误差
    error = sum(abs(a - b) for a, b in zip(signal, reconstructed))
    print(f"重构误差: {error:.6f}")


def example_different_wavelets():
    """不同小波类型比较"""
    print("\n" + "=" * 50)
    print("示例 2: 不同小波类型比较")
    print("=" * 50)
    
    signal = list(range(1, 17))
    print(f"测试信号: {signal}")
    
    wavelets = ['haar', 'db2', 'db4']
    
    for wavelet in wavelets:
        dwt = DiscreteWaveletTransform(wavelet)
        coeffs = dwt.decompose(signal, levels=2)
        reconstructed = dwt.reconstruct(coeffs)
        
        error = sum(abs(a - b) for a, b in zip(signal, reconstructed))
        print(f"\n{wavelet} 小波:")
        print(f"  滤波器长度: {len(dwt._low_pass)}")
        print(f"  重构误差: {error:.6f}")


def example_wavelet_filters():
    """小波滤波器系数"""
    print("\n" + "=" * 50)
    print("示例 3: 小波滤波器系数")
    print("=" * 50)
    
    wavelets = ['haar', 'db2', 'db4']
    
    for wavelet in wavelets:
        low, high = WaveletBase.get_wavelet(wavelet)
        print(f"\n{wavelet} 小波滤波器:")
        print(f"  低通滤波器: {[round(x, 4) for x in low]}")
        print(f"  高通滤波器: {[round(x, 4) for x in high]}")
        
        # 正交性验证
        orthogonality = sum(l * h for l, h in zip(low, high))
        print(f"  正交性检验: {orthogonality:.6f} (接近0表示正交)")


def example_signal_denoising():
    """信号去噪示例"""
    print("\n" + "=" * 50)
    print("示例 4: 信号去噪")
    print("=" * 50)
    
    # 创建纯净信号（正弦波）
    n = 64
    clean_signal = [math.sin(2 * math.pi * i / 16) for i in range(n)]
    
    # 添加噪声
    noisy_signal = [x + random.gauss(0, 0.3) for x in clean_signal]
    
    print(f"信号长度: {n}")
    print(f"纯净信号前8个值: {[round(x, 3) for x in clean_signal[:8]]}")
    print(f"含噪信号前8个值: {[round(x, 3) for x in noisy_signal[:8]]}")
    
    # 噪声估计
    denoiser = WaveletDenoiser('haar', 'soft', 'universal')
    noise_level = denoiser.get_noise_estimate(noisy_signal)
    print(f"\n估计噪声水平: {noise_level:.4f}")
    
    # 软阈值去噪
    denoised_soft = denoiser.denoise(noisy_signal)
    
    # 硬阈值去噪
    denoiser_hard = WaveletDenoiser('haar', 'hard', 'universal')
    denoised_hard = denoiser_hard.denoise(noisy_signal)
    
    print(f"软阈值去噪前8个值: {[round(x, 3) for x in denoised_soft[:8]]}")
    print(f"硬阈值去噪前8个值: {[round(x, 3) for x in denoised_hard[:8]]}")
    
    # 计算去噪效果
    mse_noisy = sum((n - c)**2 for n, c in zip(noisy_signal, clean_signal)) / n
    mse_soft = sum((d - c)**2 for d, c in zip(denoised_soft, clean_signal)) / n
    mse_hard = sum((d - c)**2 for d, c in zip(denoised_hard, clean_signal)) / n
    
    print(f"\nMSE (均方误差):")
    print(f"  含噪信号: {mse_noisy:.4f}")
    print(f"  软阈值去噪: {mse_soft:.4f}")
    print(f"  硬阈值去噪: {mse_hard:.4f}")


def example_energy_analysis():
    """能量分布分析"""
    print("\n" + "=" * 50)
    print("示例 5: 能量分布分析")
    print("=" * 50)
    
    # 创建低频为主的信号
    low_freq_signal = [math.sin(2 * math.pi * i / 64) for i in range(64)]
    
    # 创建高频为主的信号
    high_freq_signal = [math.sin(2 * math.pi * i / 4) + 
                        math.sin(2 * math.pi * i / 2) for i in range(64)]
    
    analyzer = WaveletEnergyAnalyzer('haar')
    
    print("\n低频信号能量分布:")
    energy_low = analyzer.analyze_energy_distribution(low_freq_signal, levels=3)
    print(f"  总能量: {energy_low['total_energy']:.2f}")
    print(f"  近似系数占比: {energy_low['approximation']:.2%}")
    for level, pct in energy_low['details'].items():
        print(f"  {level}: {pct:.2%}")
    
    print("\n高频信号能量分布:")
    energy_high = analyzer.analyze_energy_distribution(high_freq_signal, levels=3)
    print(f"  总能量: {energy_high['total_energy']:.2f}")
    print(f"  近似系数占比: {energy_high['approximation']:.2%}")
    for level, pct in energy_high['details'].items():
        print(f"  {level}: {pct:.2%}")


def example_wavelet_packet():
    """小波包变换示例"""
    print("\n" + "=" * 50)
    print("示例 6: 小波包变换")
    print("=" * 50)
    
    signal = [1, 2, 3, 4, 5, 6, 7, 8]
    print(f"原始信号: {signal}")
    
    wpt = WaveletPacketTransform('haar')
    tree = wpt.decompose(signal, levels=2)
    
    print(f"\n小波包树节点 ({len(tree)} 个):")
    for path in sorted(tree.keys(), key=lambda x: (len(x), x)):
        data = tree[path]
        print(f"  节点 '{path}': {[round(x, 3) for x in data]}")
    
    # 寻找最佳基
    best_basis = wpt.find_best_basis(tree, cost_func='entropy')
    print(f"\n最佳基节点 (按熵排序): {best_basis[:4]}")
    
    # 从根节点重构
    reconstructed = wpt.reconstruct_node(tree, '')
    print(f"\n重构信号: {[round(x, 4) for x in reconstructed]}")


def example_signal_compression():
    """信号压缩示例"""
    print("\n" + "=" * 50)
    print("示例 7: 信号压缩（阈值压缩）")
    print("=" * 50)
    
    # 创建信号
    n = 128
    signal = [math.sin(2 * math.pi * i / 16) + 
              0.5 * math.sin(2 * math.pi * i / 8) for i in range(n)]
    
    print(f"原始信号长度: {n}")
    
    # DWT 分解
    dwt = DiscreteWaveletTransform('haar')
    coeffs = dwt.decompose(signal, levels=4)
    
    total_coeffs = coeffs.get_total_coefficients()
    print(f"总系数数量: {total_coeffs}")
    
    # 阈值压缩（保留大于阈值的系数）
    threshold = 0.1
    compressed_coeffs = WaveletCoefficients(
        approximation=[c if abs(c) > threshold else 0 for c in coeffs.approximation],
        details=[[c if abs(c) > threshold else 0 for c in d] for d in coeffs.details],
        levels=coeffs.levels,
        wavelet_type=coeffs.wavelet_type
    )
    
    # 计算保留的系数数量
    non_zero = sum(1 for c in compressed_coeffs.approximation if abs(c) > 0)
    for detail in compressed_coeffs.details:
        non_zero += sum(1 for c in detail if abs(c) > 0)
    
    compression_ratio = (total_coeffs - non_zero) / total_coeffs
    print(f"保留系数数量: {non_zero}")
    print(f"压缩比率: {compression_ratio:.2%}")
    
    # 重构压缩信号
    reconstructed = dwt.reconstruct(compressed_coeffs)
    
    # 计算重构误差
    mse = sum((a - b)**2 for a, b in zip(signal, reconstructed)) / n
    print(f"重构 MSE: {mse:.6f}")


def example_anomaly_detection():
    """异常检测示例"""
    print("\n" + "=" * 50)
    print("示例 8: 异常检测")
    print("=" * 50)
    
    # 创建正常信号
    n = 64
    normal_signal = [math.sin(2 * math.pi * i / 16) for i in range(n)]
    
    # 添加异常点
    anomaly_signal = normal_signal.copy()
    anomaly_positions = [10, 25, 40]
    for pos in anomaly_positions:
        anomaly_signal[pos] += 2.0  # 大偏差
    
    print(f"异常位置: {anomaly_positions}")
    
    analyzer = WaveletEnergyAnalyzer('haar')
    
    # 检测异常
    detected = analyzer.detect_anomalies(anomaly_signal, threshold_ratio=2.0)
    
    print(f"检测到的异常位置: {detected}")
    
    # 计算检测准确性
    correct = sum(1 for p in anomaly_positions if p in detected or p-1 in detected or p+1 in detected)
    print(f"检测准确率: {correct}/{len(anomaly_positions)} = {correct/len(anomaly_positions):.0%}")


def example_multiresolution():
    """多分辨率分析示例"""
    print("\n" + "=" * 50)
    print("示例 9: 多分辨率分析")
    print("=" * 50)
    
    # 创建复杂信号
    n = 64
    signal = [math.sin(2 * math.pi * i / 32) +    # 低频成分
              0.3 * math.sin(2 * math.pi * i / 8) + # 中频成分
              0.1 * math.sin(2 * math.pi * i / 4)   # 高频成分
              for i in range(n)]
    
    print(f"信号长度: {n}")
    print(f"信号成分: 低频 + 中频 + 高频")
    
    dwt = DiscreteWaveletTransform('haar')
    coeffs = dwt.decompose(signal, levels=3)
    
    print("\n各分辨率层级分析:")
    print(f"  近似系数 (最低频): {len(coeffs.approximation)} 个")
    print(f"    前4个值: {[round(x, 3) for x in coeffs.approximation[:4]]}")
    
    for i, detail in enumerate(coeffs.details):
        freq_band = f"第{i+1}层细节"
        print(f"  {freq_band}: {len(detail)} 个系数")
        print(f"    前4个值: {[round(x, 3) for x in detail[:4]]}")
        energy = sum(x*x for x in detail)
        print(f"    能量: {energy:.2f}")


def example_convenience_functions():
    """便捷函数示例"""
    print("\n" + "=" * 50)
    print("示例 10: 便捷函数")
    print("=" * 50)
    
    signal = [1, 2, 3, 4, 5, 6, 7, 8]
    
    # 快速分解
    coeffs = dwt_decompose(signal, wavelet='haar', levels=2)
    print(f"快速分解结果:")
    print(f"  近似: {coeffs.approximation}")
    print(f"  细节: {coeffs.details}")
    
    # 快速重构
    reconstructed = dwt_reconstruct(coeffs, wavelet='haar')
    print(f"快速重构: {[round(x, 4) for x in reconstructed]}")
    
    # 快速去噪
    noisy = [x + random.uniform(-0.5, 0.5) for x in signal]
    denoised = denoise_signal(noisy, wavelet='haar', method='soft')
    print(f"\n快速去噪:")
    print(f"  含噪: {[round(x, 2) for x in noisy]}")
    print(f"  去噪: {[round(x, 2) for x in denoised]}")
    
    # 快速能量分析
    energy = analyze_energy(signal, wavelet='haar')
    print(f"\n快速能量分析:")
    print(f"  总能量: {energy['total_energy']:.2f}")
    print(f"  近似占比: {energy['approximation']:.2%}")


def main():
    """运行所有示例"""
    print("\n" + "=" * 60)
    print("Wavelet Utils - 小波变换工具模块使用示例")
    print("=" * 60)
    
    example_basic_dwt()
    example_different_wavelets()
    example_wavelet_filters()
    example_signal_denoising()
    example_energy_analysis()
    example_wavelet_packet()
    example_signal_compression()
    example_anomaly_detection()
    example_multiresolution()
    example_convenience_functions()
    
    print("\n" + "=" * 60)
    print("示例运行完成!")
    print("=" * 60)


if __name__ == "__main__":
    main()
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ant Colony Optimization (ACO) Utils 使用示例
=============================================

展示蚁群优化算法的各种使用场景。

作者: AllToolkit 自动化生成
日期: 2026-05-28
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ant_colony_optimization_utils.mod import (
    ACOConfig,
    ACOVariant,
    ACOResult,
    TSPProblem,
    AntColonyOptimizer,
    ACOUtils,
    solve_tsp,
    solve_random_tsp,
    compare_aco_variants,
    get_tsp_lower_bound,
    nearest_neighbor_tour,
)


def example_basic_tsp():
    """示例1: 基本TSP求解"""
    print("\n" + "=" * 60)
    print("示例1: 基本TSP求解")
    print("=" * 60)
    
    # 定义简单的矩形城市布局
    coords = [(0, 0), (10, 0), (10, 10), (0, 10)]
    print(f"城市坐标: {coords}")
    
    # 求解TSP
    result = solve_tsp(coords, num_ants=10, num_iterations=50)
    
    print(f"\n结果:")
    print(f"  最佳路径: {result.best_tour}")
    print(f"  路径长度: {result.best_length:.2f}")
    print(f"  执行时间: {result.execution_time:.3f}s")
    print(f"  改进率: {result.improvement_rate:.2f}%")
    
    # 可视化路径
    visualization = ACOUtils.visualize_tour_ascii(coords, result.best_tour)
    print(f"\n路径可视化:")
    print(visualization)


def example_different_variants():
    """示例2: 比较不同算法变体"""
    print("\n" + "=" * 60)
    print("示例2: 比较不同算法变体")
    print("=" * 60)
    
    # 定义中等规模问题
    coords = [(0, 0), (20, 10), (40, 0), (30, 20), 
              (10, 30), (50, 15), (25, 25), (5, 15)]
    print(f"城市数量: {len(coords)}")
    
    # 比较三种变体
    results = compare_aco_variants(coords, num_iterations=30)
    
    print("\n算法变体性能对比:")
    print("-" * 40)
    
    for name, result in results.items():
        variant_name = {
            'ant_system': 'Ant System (AS)',
            'ant_colony_system': 'Ant Colony System (ACS)',
            'max_min_ant_system': 'Max-Min Ant System (MMAS)'
        }.get(name, name)
        
        print(f"{variant_name}:")
        print(f"  最佳长度: {result.best_length:.2f}")
        print(f"  执行时间: {result.execution_time:.3f}s")
        print(f"  收敛迭代: {result.convergence_iteration}")
        print()


def example_large_scale_tsp():
    """示例3: 大规模TSP问题"""
    print("\n" + "=" * 60)
    print("示例3: 大规模TSP问题")
    print("=" * 60)
    
    num_cities = 30
    print(f"城市数量: {num_cities}")
    
    # 生成随机问题并求解
    result = solve_random_tsp(num_cities, 
                               num_ants=40, 
                               num_iterations=100, 
                               seed=42)
    
    print(f"\n求解结果:")
    print(f"  最佳路径长度: {result.best_length:.2f}")
    print(f"  执行时间: {result.execution_time:.3f}s")
    print(f"  改进率: {result.improvement_rate:.2f}%")
    
    # 计算下界估计
    problem = TSPProblem.random_problem(num_cities, seed=42)
    coords = [(n.x, n.y) for n in problem.nodes]
    bound = get_tsp_lower_bound(coords)
    
    print(f"\n质量评估:")
    print(f"  理论下界估计: {bound:.2f}")
    print(f"  解与下界比值: {(result.best_length / bound):.2f}")
    print(f"  (理想情况下比值接近1.0)")


def example_custom_configuration():
    """示例4: 自定义参数配置"""
    print("\n" + "=" * 60)
    print("示例4: 自定义参数配置")
    print("=" * 60)
    
    coords = [(0, 0), (10, 0), (20, 5), (15, 15), (5, 10), (25, 10)]
    
    # 自定义配置
    config = ACOConfig(
        num_ants=30,
        num_iterations=80,
        alpha=2.0,        # 信息素重要性较高
        beta=4.0,         # 启发信息更重要
        rho=0.2,          # 低挥发率，保留更多历史信息
        variant=ACOVariant.MMAS,
        tau_min=0.1,
        tau_max=5.0,
        adaptive=True,
        seed=42
    )
    
    print("自定义参数:")
    print(f"  蚂蚁数量: {config.num_ants}")
    print(f"  迭代次数: {config.num_iterations}")
    print(f"  α (信息素权重): {config.alpha}")
    print(f"  β (启发权重): {config.beta}")
    print(f"  ρ (挥发率): {config.rho}")
    print(f"  算法变体: {config.variant.value}")
    print(f"  自适应: {config.adaptive}")
    
    problem = TSPProblem.from_coordinates(coords)
    optimizer = AntColonyOptimizer(problem, config)
    result = optimizer.run()
    
    print(f"\n求解结果:")
    print(f"  最佳路径: {result.best_tour}")
    print(f"  路径长度: {result.best_length:.2f}")
    print(f"  停滞检测: {result.stagnation_detected}")


def example_heuristic_comparison():
    """示例5: 与启发式算法对比"""
    print("\n" + "=" * 60)
    print("示例5: ACO与启发式算法对比")
    print("=" * 60)
    
    coords = [(0, 0), (20, 0), (40, 0), (40, 20), 
              (20, 20), (0, 20), (10, 10), (30, 10)]
    
    print(f"城市数量: {len(coords)}")
    
    # ACO求解
    aco_result = solve_tsp(coords, num_ants=20, num_iterations=50, seed=42)
    
    # 最近邻启发式
    nn_tour, nn_length = nearest_neighbor_tour(coords)
    
    # 下界估计
    bound = get_tsp_lower_bound(coords)
    
    print("\n算法对比:")
    print("-" * 40)
    print(f"蚁群优化 (ACO):")
    print(f"  路径长度: {aco_result.best_length:.2f}")
    print(f"  执行时间: {aco_result.execution_time:.3f}s")
    
    print(f"\n最近邻启发式:")
    print(f"  路径长度: {nn_length:.2f}")
    print(f"  路径: {nn_tour}")
    
    print(f"\n理论下界估计: {bound:.2f}")
    
    # 计算相对改进
    improvement_vs_nn = (nn_length - aco_result.best_length) / nn_length * 100
    print(f"\nACO相比最近邻改进: {improvement_vs_nn:.2f}%")


def example_convergence_analysis():
    """示例6: 收敛分析"""
    print("\n" + "=" * 60)
    print("示例6: 收敛过程分析")
    print("=" * 60)
    
    coords = [(0, 0), (10, 0), (20, 5), (15, 15), (5, 10)]
    
    config = ACOConfig(num_ants=15, num_iterations=30, seed=42)
    problem = TSPProblem.from_coordinates(coords)
    optimizer = AntColonyOptimizer(problem, config)
    result = optimizer.run()
    
    print("迭代过程分析:")
    print("-" * 50)
    print(f"{'迭代':>6} {'最佳':>10} {'平均':>10} {'差距':>10}")
    print("-" * 50)
    
    # 显示前10代和后10代
    for i in [0, 1, 2, 3, 4, 5, 10, 15, 20, 25, 29]:
        if i < len(result.iteration_best):
            best = result.iteration_best[i]
            avg = result.avg_length[i]
            diff = avg - best
            print(f"{i:>6} {best:>10.2f} {avg:>10.2f} {diff:>10.2f}")
    
    print("-" * 50)
    print(f"收敛迭代: {result.convergence_iteration}")
    print(f"最终最佳: {result.best_length:.2f}")


def example_problem_instance():
    """示例7: 创建问题实例"""
    print("\n" + "=" * 60)
    print("示例7: 创建和操作问题实例")
    print("=" * 60)
    
    # 方法1: 从坐标列表创建
    coords = [(0, 0), (10, 0), (10, 10), (0, 10)]
    problem1 = TSPProblem.from_coordinates(coords)
    print(f"方法1: 从坐标创建 - {problem1.num_nodes}个节点")
    
    # 方法2: 随机生成
    problem2 = TSPProblem.random_problem(8, seed=42)
    print(f"方法2: 随机生成 - {problem2.num_nodes}个节点")
    
    # 查看节点信息
    print("\n节点坐标:")
    for node in problem2.nodes[:5]:
        print(f"  节点{node.id}: ({node.x:.2f}, {node.y:.2f})")
    
    # 计算特定距离
    d = problem2.get_distance(0, 1)
    print(f"\n节点0到节点1的距离: {d:.2f}")
    
    # 计算特定路径长度
    tour = [0, 1, 2, 3]
    length = problem2.compute_tour_length(tour)
    print(f"路径[0,1,2,3]长度: {length:.2f}")


def run_all_examples():
    """运行所有示例"""
    print("=" * 60)
    print("Ant Colony Optimization (ACO) Utils - 使用示例")
    print("=" * 60)
    
    example_basic_tsp()
    example_different_variants()
    example_large_scale_tsp()
    example_custom_configuration()
    example_heuristic_comparison()
    example_convergence_analysis()
    example_problem_instance()
    
    print("\n" + "=" * 60)
    print("示例运行完成")
    print("=" * 60)


if __name__ == '__main__':
    run_all_examples()
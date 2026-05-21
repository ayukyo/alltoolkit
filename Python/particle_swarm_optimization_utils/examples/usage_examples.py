"""
粒子群优化算法 (PSO) 使用示例

本示例展示如何使用 particle_swarm_optimization_utils 模块
解决各类优化问题。
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    ParticleSwarmOptimizer,
    PSOConfig,
    InertiaWeightStrategy,
    BoundaryHandling,
    optimize,
    optimize_with_constraints,
    sphere,
    rastrigin,
    rosenbrock,
    ackley,
    griewank,
    schwefel,
    levy,
    calculate_convergence_rate,
    calculate_diversity,
    get_best_solutions
)
import math


def example_1_basic_optimization():
    """
    示例 1: 基本优化
    
    使用便捷函数 optimize() 快速求解 Sphere 函数最小值。
    Sphere 函数是最简单的凸函数，全局最优在原点。
    """
    print("\n" + "=" * 60)
    print("示例 1: 基本优化 - Sphere 函数")
    print("=" * 60)
    
    # 使用便捷函数进行优化
    result = optimize(
        objective_func=sphere,           # 目标函数
        bounds=[(-5, 5)] * 5,            # 5维空间，每维范围 [-5, 5]
        swarm_size=30,                    # 粒子数量
        max_iterations=100,               # 最大迭代次数
        seed=42                           # 随机种子（可复现）
    )
    
    print(f"\n优化结果:")
    print(f"  最优位置: {[round(x, 6) for x in result.best_position]}")
    print(f"  最优值: {result.best_fitness:.6e}")
    print(f"  迭代次数: {result.iteration_count}")
    print(f"  理论最优: 0 (在原点)")


def example_2_custom_objective():
    """
    示例 2: 自定义目标函数
    
    定义自己的目标函数进行优化。
    """
    print("\n" + "=" * 60)
    print("示例 2: 自定义目标函数")
    print("=" * 60)
    
    # 自定义目标函数：寻找函数最小值
    def my_function(x):
        """
        自定义函数: f(x) = (x0-2)² + (x1+3)² + sin(x0*x1)
        最优解在 (2, -3) 附近
        """
        return (x[0] - 2) ** 2 + (x[1] + 3) ** 2 + math.sin(x[0] * x[1])
    
    result = optimize(
        objective_func=my_function,
        bounds=[(-10, 10)] * 2,
        swarm_size=40,
        max_iterations=100
    )
    
    print(f"\n目标函数: (x0-2)² + (x1+3)² + sin(x0*x1)")
    print(f"  最优位置: ({result.best_position[0]:.4f}, {result.best_position[1]:.4f})")
    print(f"  最优值: {result.best_fitness:.6f}")
    print(f"  理论最优位置: (2, -3)")


def example_3_advanced_config():
    """
    示例 3: 高级配置
    
    使用 PSOConfig 配置详细的算法参数。
    """
    print("\n" + "=" * 60)
    print("示例 3: 高级配置 - Rastrigin 函数")
    print("=" * 60)
    
    # 创建详细配置
    config = PSOConfig(
        swarm_size=50,                                        # 粒子数量
        max_iterations=200,                                   # 最大迭代次数
        inertia_weight=0.7,                                   # 惯性权重
        cognitive_coeff=1.5,                                  # 认知系数 c1
        social_coeff=1.5,                                      # 社会系数 c2
        inertia_strategy=InertiaWeightStrategy.LINEAR_DECREASING,  # 惯性策略
        min_inertia=0.4,                                      # 最小惯性权重
        max_inertia=0.9,                                      # 最大惯性权重
        velocity_clamp=2.0,                                   # 速度限制
        early_stop_patience=30,                               # 早停耐心值
        early_stop_threshold=1e-8,                           # 早停阈值
        seed=123                                             # 随机种子
    )
    
    # 创建优化器
    optimizer = ParticleSwarmOptimizer(
        objective_func=rastrigin,
        bounds=[(-5.12, 5.12)] * 5,
        config=config
    )
    
    # 执行优化（带进度输出）
    result = optimizer.optimize(verbose=True)
    
    print(f"\n最终结果:")
    print(f"  最优位置: {[round(x, 4) for x in result.best_position]}")
    print(f"  最优值: {result.best_fitness:.6f}")
    print(f"  收敛速率: {calculate_convergence_rate(result.convergence_history):.6f}")


def example_4_inertia_strategies():
    """
    示例 4: 不同惯性权重策略比较
    
    展示各种惯性权重策略的效果。
    """
    print("\n" + "=" * 60)
    print("示例 4: 惯性权重策略比较")
    print("=" * 60)
    
    strategies = [
        ("固定权重", InertiaWeightStrategy.CONSTANT),
        ("线性递减", InertiaWeightStrategy.LINEAR_DECREASING),
        ("指数递减", InertiaWeightStrategy.EXPONENTIAL),
        ("随机权重", InertiaWeightStrategy.RANDOM),
        ("自适应", InertiaWeightStrategy.ADAPTIVE),
    ]
    
    print(f"\n优化函数: Ackley (4维)")
    print("-" * 50)
    
    for name, strategy in strategies:
        config = PSOConfig(
            swarm_size=30,
            max_iterations=150,
            inertia_strategy=strategy,
            seed=42
        )
        
        optimizer = ParticleSwarmOptimizer(
            objective_func=ackley,
            bounds=[(-5, 5)] * 4,
            config=config
        )
        
        result = optimizer.optimize()
        
        print(f"  {name:12s}: 最优值 = {result.best_fitness:.6e}, 迭代 = {result.iteration_count}")


def example_5_boundary_handling():
    """
    示例 5: 边界处理策略
    
    展示不同边界处理策略的效果。
    """
    print("\n" + "=" * 60)
    print("示例 5: 边界处理策略")
    print("=" * 60)
    
    # 目标函数：最优解在边界外
    def outside_boundary(x):
        return (x[0] - 10) ** 2 + (x[1] - 10) ** 2
    
    strategies = [
        ("截断", BoundaryHandling.CLAMP),
        ("反弹", BoundaryHandling.REFLECT),
        ("周期性", BoundaryHandling.PERIODIC),
        ("随机重置", BoundaryHandling.RANDOM),
    ]
    
    print(f"\n目标: 最优解在 (10, 10)，但边界限制在 [-5, 5]")
    print("-" * 50)
    
    for name, strategy in strategies:
        config = PSOConfig(
            swarm_size=30,
            max_iterations=100,
            boundary_handling=strategy,
            seed=42
        )
        
        optimizer = ParticleSwarmOptimizer(
            objective_func=outside_boundary,
            bounds=[(-5, 5), (-5, 5)],
            config=config
        )
        
        result = optimizer.optimize()
        
        print(f"  {name:10s}: 最优位置 = ({result.best_position[0]:.4f}, {result.best_position[1]:.4f}), "
              f"最优值 = {result.best_fitness:.4f}")


def example_6_constraint_optimization():
    """
    示例 6: 约束优化
    
    使用惩罚函数法处理约束条件。
    """
    print("\n" + "=" * 60)
    print("示例 6: 约束优化")
    print("=" * 60)
    
    # 目标函数
    def objective(x):
        return x[0] * x[1]
    
    # 约束条件
    def constraint1(x):
        """x0 + x1 <= 10"""
        return x[0] + x[1] <= 10
    
    def constraint2(x):
        """x0 >= 2"""
        return x[0] >= 2
    
    def constraint3(x):
        """x1 >= 2"""
        return x[1] >= 2
    
    result = optimize_with_constraints(
        objective_func=objective,
        bounds=[(0, 15), (0, 15)],
        constraints=[constraint1, constraint2, constraint3],
        swarm_size=40,
        max_iterations=150,
        penalty_factor=1000,
        seed=42
    )
    
    x0, x1 = result.best_position
    
    print(f"\n目标函数: x0 * x1")
    print(f"约束条件:")
    print(f"  x0 + x1 <= 10")
    print(f"  x0 >= 2")
    print(f"  x1 >= 2")
    print(f"\n结果:")
    print(f"  最优位置: ({x0:.4f}, {x1:.4f})")
    print(f"  最优值: {result.best_fitness:.4f}")
    print(f"  约束检查:")
    print(f"    x0 + x1 = {x0 + x1:.4f} <= 10? {x0 + x1 <= 10}")
    print(f"    x0 >= 2? {x0 >= 2}")
    print(f"    x1 >= 2? {x1 >= 2}")
    print(f"\n  理论最优: x0 = x1 = 5, 最优值 = 25")


def example_7_maximization():
    """
    示例 7: 最大化问题
    
    PSO 默认求最小值，通过设置 minimize=False 求最大值。
    """
    print("\n" + "=" * 60)
    print("示例 7: 最大化问题")
    print("=" * 60)
    
    def negative_sphere(x):
        """取反的 Sphere 函数，最优为原点的最大值 0"""
        return -sum(xi ** 2 for xi in x)
    
    result = optimize(
        objective_func=negative_sphere,
        bounds=[(-3, 3)] * 3,
        swarm_size=30,
        max_iterations=100,
        minimize=False,  # 最大化
        seed=42
    )
    
    print(f"\n目标: 最大化 -Σx² (在原点取最大值 0)")
    print(f"  最优位置: {[round(x, 6) for x in result.best_position]}")
    print(f"  最优值: {result.best_fitness:.6f}")


def example_8_high_dimensional():
    """
    示例 8: 高维优化
    
    解决高维优化问题。
    """
    print("\n" + "=" * 60)
    print("示例 8: 高维优化 (50维)")
    print("=" * 60)
    
    config = PSOConfig(
        swarm_size=100,
        max_iterations=300,
        inertia_strategy=InertiaWeightStrategy.LINEAR_DECREASING,
        seed=42
    )
    
    optimizer = ParticleSwarmOptimizer(
        objective_func=sphere,
        bounds=[(-10, 10)] * 50,  # 50 维
        config=config
    )
    
    result = optimizer.optimize()
    
    print(f"\n优化结果:")
    print(f"  维度: 50")
    print(f"  粒子数: 100")
    print(f"  最优值: {result.best_fitness:.6e}")
    print(f"  迭代次数: {result.iteration_count}")
    
    # 分析收敛
    rate = calculate_convergence_rate(result.convergence_history)
    print(f"  收敛速率: {rate:.6f}")


def example_9_analyze_results():
    """
    示例 9: 结果分析
    
    分析优化结果的各项指标。
    """
    print("\n" + "=" * 60)
    print("示例 9: 结果分析")
    print("=" * 60)
    
    result = optimize(
        objective_func=rosenbrock,
        bounds=[(-5, 10)] * 4,
        swarm_size=50,
        max_iterations=200,
        seed=42
    )
    
    print(f"\n优化结果分析:")
    print(f"  最优位置: {[round(x, 4) for x in result.best_position]}")
    print(f"  最优值: {result.best_fitness:.6f}")
    print(f"  迭代次数: {result.iteration_count}")
    
    # 收敛速率
    conv_rate = calculate_convergence_rate(result.convergence_history)
    print(f"\n收敛分析:")
    print(f"  收敛速率: {conv_rate:.6f}")
    
    # 多样性
    diversity = calculate_diversity(result.swarm)
    print(f"  粒子群多样性: {diversity:.4f}")
    
    # 最优解
    top_5 = get_best_solutions(result, top_k=5)
    print(f"\n最优 5 个解:")
    for i, (pos, fit) in enumerate(top_5, 1):
        print(f"  {i}. 适应度 = {fit:.6e}")


def example_10_real_world_application():
    """
    示例 10: 实际应用 - 曲线拟合
    
    使用 PSO 进行曲线参数拟合。
    """
    print("\n" + "=" * 60)
    print("示例 10: 实际应用 - 曲线拟合")
    print("=" * 60)
    
    # 生成带噪声的测试数据
    # 真实模型: y = a * exp(-b * x) + c
    import random
    random.seed(42)
    
    true_a, true_b, true_c = 5.0, 0.5, 1.0
    
    data_points = []
    for x in [i * 0.5 for i in range(20)]:
        noise = random.gauss(0, 0.2)
        y = true_a * math.exp(-true_b * x) + true_c + noise
        data_points.append((x, y))
    
    # 定义目标函数：最小化残差平方和
    def curve_fitting(params):
        a, b, c = params
        error = sum((y - (a * math.exp(-b * x) + c)) ** 2 for x, y in data_points)
        return error
    
    # 优化拟合参数
    result = optimize(
        objective_func=curve_fitting,
        bounds=[(0, 10), (0, 2), (-5, 5)],  # a, b, c 的范围
        swarm_size=50,
        max_iterations=200,
        seed=42
    )
    
    fit_a, fit_b, fit_c = result.best_position
    
    print(f"\n真实参数: a={true_a}, b={true_b}, c={true_c}")
    print(f"拟合参数: a={fit_a:.4f}, b={fit_b:.4f}, c={fit_c:.4f}")
    print(f"残差平方和: {result.best_fitness:.6f}")
    
    # 计算拟合精度
    errors = [
        abs(fit_a - true_a) / true_a,
        abs(fit_b - true_b) / true_b,
        abs(fit_c - true_c) / true_c
    ]
    print(f"相对误差: a={errors[0]*100:.2f}%, b={errors[1]*100:.2f}%, c={errors[2]*100:.2f}%")


def example_11_multimodal():
    """
    示例 11: 多峰函数优化
    
    测试 PSO 在多峰函数上的表现。
    """
    print("\n" + "=" * 60)
    print("示例 11: 多峰函数优化 - Rastrigin")
    print("=" * 60)
    
    print("\nRastrigin 函数具有大量局部最优，是测试优化算法的经典函数。")
    
    dimensions = [2, 5, 10]
    
    for dim in dimensions:
        result = optimize(
            objective_func=rastrigin,
            bounds=[(-5.12, 5.12)] * dim,
            swarm_size=30 * dim,  # 粒子数随维度增加
            max_iterations=200,
            inertia_strategy=InertiaWeightStrategy.LINEAR_DECREASING,
            seed=42
        )
        
        print(f"  {dim}维: 最优值 = {result.best_fitness:.4f}, 理论最优 = 0")


def run_all_examples():
    """运行所有示例"""
    print("\n" + "=" * 60)
    print("粒子群优化算法 (PSO) 使用示例集")
    print("=" * 60)
    
    examples = [
        example_1_basic_optimization,
        example_2_custom_objective,
        example_3_advanced_config,
        example_4_inertia_strategies,
        example_5_boundary_handling,
        example_6_constraint_optimization,
        example_7_maximization,
        example_8_high_dimensional,
        example_9_analyze_results,
        example_10_real_world_application,
        example_11_multimodal,
    ]
    
    for example in examples:
        try:
            example()
        except Exception as e:
            print(f"\n示例执行出错: {e}")
    
    print("\n" + "=" * 60)
    print("所有示例执行完成!")
    print("=" * 60)


if __name__ == "__main__":
    run_all_examples()
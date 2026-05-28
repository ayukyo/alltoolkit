#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ant Colony Optimization (ACO) Utils 测试文件
=============================================

测试蚁群优化算法的所有功能。

运行方式:
    python ant_colony_optimization_utils_test.py
    pytest ant_colony_optimization_utils_test.py -v

作者: AllToolkit 自动化生成
日期: 2026-05-28
"""

import pytest
import sys
import os

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ant_colony_optimization_utils.mod import (
    AntColonyOptimizer,
    ACOConfig,
    ACOVariant,
    ACOResult,
    TSPProblem,
    Node,
    Ant,
    ACOUtils,
    solve_tsp,
    solve_random_tsp,
    compare_aco_variants,
    get_tsp_lower_bound,
    nearest_neighbor_tour,
)


class TestTSPProblem:
    """TSP问题类测试"""
    
    def test_create_from_coordinates(self):
        """测试从坐标创建TSP问题"""
        coords = [(0, 0), (10, 0), (10, 10), (0, 10)]
        problem = TSPProblem.from_coordinates(coords)
        
        assert problem.num_nodes == 4
        assert len(problem.nodes) == 4
        assert problem.symmetric == True
    
    def test_create_random_problem(self):
        """测试创建随机TSP问题"""
        problem = TSPProblem.random_problem(10, seed=42)
        
        assert problem.num_nodes == 10
        assert len(problem.nodes) == 10
        
        # 验证节点在范围内
        for node in problem.nodes:
            assert 0.0 <= node.x <= 100.0
            assert 0.0 <= node.y <= 100.0
    
    def test_distance_matrix(self):
        """测试距离矩阵计算"""
        coords = [(0, 0), (10, 0), (10, 10)]
        problem = TSPProblem.from_coordinates(coords)
        
        # 对角线应为0
        assert problem.get_distance(0, 0) == 0.0
        assert problem.get_distance(1, 1) == 0.0
        
        # 测试距离值
        d01 = problem.get_distance(0, 1)
        assert abs(d01 - 10.0) < 0.001
        
        d02 = problem.get_distance(0, 2)
        assert abs(d02 - 14.142) < 0.1  # sqrt(200)
        
        # 对称性
        assert problem.get_distance(0, 1) == problem.get_distance(1, 0)
    
    def test_heuristic_matrix(self):
        """测试启发信息矩阵"""
        coords = [(0, 0), (10, 0)]
        problem = TSPProblem.from_coordinates(coords)
        
        # η = 1/d
        h = problem.get_heuristic(0, 1)
        assert abs(h - 0.1) < 0.001
        
        # 对角线应为0
        assert problem.get_heuristic(0, 0) == 0.0
    
    def test_compute_tour_length(self):
        """测试路径长度计算"""
        coords = [(0, 0), (10, 0), (10, 10), (0, 10)]
        problem = TSPProblem.from_coordinates(coords)
        
        # 正方形路径 0 -> 1 -> 2 -> 3 -> 0
        tour = [0, 1, 2, 3]
        length = problem.compute_tour_length(tour)
        assert abs(length - 40.0) < 0.001
        
        # 反方向路径
        tour = [0, 3, 2, 1]
        length = problem.compute_tour_length(tour)
        assert abs(length - 40.0) < 0.001
        
        # 单节点路径
        tour = [0]
        length = problem.compute_tour_length(tour)
        assert length == 0.0
    
    def test_empty_problem(self):
        """测试空问题"""
        problem = TSPProblem.from_coordinates([])
        assert problem.num_nodes == 0
    
    def test_single_node(self):
        """测试单节点问题"""
        problem = TSPProblem.from_coordinates([(5, 5)])
        assert problem.num_nodes == 1
        assert problem.compute_tour_length([0]) == 0.0


class TestACOConfig:
    """ACO配置类测试"""
    
    def test_default_config(self):
        """测试默认配置"""
        config = ACOConfig()
        
        assert config.num_ants == 20
        assert config.num_iterations == 100
        assert config.alpha == 1.0
        assert config.beta == 2.0
        assert config.rho == 0.5
        assert config.variant == ACOVariant.AS
    
    def test_custom_config(self):
        """测试自定义配置"""
        config = ACOConfig(
            num_ants=50,
            num_iterations=200,
            alpha=2.0,
            beta=3.0,
            rho=0.3,
            variant=ACOVariant.ACS,
            seed=123
        )
        
        assert config.num_ants == 50
        assert config.num_iterations == 200
        assert config.alpha == 2.0
        assert config.beta == 3.0
        assert config.rho == 0.3
        assert config.variant == ACOVariant.ACS
        assert config.seed == 123
    
    def test_mmas_config(self):
        """测试MMAS配置"""
        config = ACOConfig(
            variant=ACOVariant.MMAS,
            tau_min=0.01,
            tau_max=5.0
        )
        
        assert config.variant == ACOVariant.MMAS
        assert config.tau_min == 0.01
        assert config.tau_max == 5.0


class TestAntColonyOptimizer:
    """蚁群优化器测试"""
    
    def test_run_simple_tsp(self):
        """测试简单TSP求解"""
        coords = [(0, 0), (10, 0), (10, 10), (0, 10)]
        problem = TSPProblem.from_coordinates(coords)
        config = ACOConfig(num_ants=5, num_iterations=10, seed=42)
        
        optimizer = AntColonyOptimizer(problem, config)
        result = optimizer.run()
        
        assert isinstance(result, ACOResult)
        assert len(result.best_tour) == 4
        assert result.best_length > 0
        assert result.best_length <= 40.0  # 正方形最优解
        assert result.total_iterations == 10
    
    def test_run_with_different_variants(self):
        """测试不同算法变体"""
        coords = [(0, 0), (10, 0), (10, 10), (0, 10)]
        problem = TSPProblem.from_coordinates(coords)
        
        results = {}
        for variant in [ACOVariant.AS, ACOVariant.ACS, ACOVariant.MMAS]:
            config = ACOConfig(num_ants=5, num_iterations=10, variant=variant, seed=42)
            optimizer = AntColonyOptimizer(problem, config)
            result = optimizer.run()
            results[variant.value] = result
            
            assert result.best_length > 0
            assert result.best_length <= 45.0
    
    def test_random_problem(self):
        """测试随机问题求解"""
        problem = TSPProblem.random_problem(5, seed=42)
        config = ACOConfig(num_ants=5, num_iterations=10, seed=42)
        
        optimizer = AntColonyOptimizer(problem, config)
        result = optimizer.run()
        
        assert len(result.best_tour) == 5
        assert result.best_length > 0
        assert result.execution_time > 0
    
    def test_iteration_statistics(self):
        """测试迭代统计数据"""
        coords = [(0, 0), (10, 0), (10, 10)]
        problem = TSPProblem.from_coordinates(coords)
        config = ACOConfig(num_iterations=5, seed=42)
        
        optimizer = AntColonyOptimizer(problem, config)
        result = optimizer.run()
        
        assert len(result.iteration_best) == 5
        assert len(result.avg_length) == 5
        
        # 每代最佳应该非负
        for length in result.iteration_best:
            assert length > 0
        
        for length in result.avg_length:
            assert length > 0
    
    def test_convergence(self):
        """测试收敛检测"""
        coords = [(0, 0), (10, 0)]
        problem = TSPProblem.from_coordinates(coords)
        config = ACOConfig(num_iterations=10, seed=42)
        
        optimizer = AntColonyOptimizer(problem, config)
        result = optimizer.run()
        
        # 两节点问题最优解是固定值
        assert result.best_length == 20.0  # 往返距离
    
    def test_pheromone_matrix(self):
        """测试信息素矩阵"""
        coords = [(0, 0), (10, 0), (10, 10)]
        problem = TSPProblem.from_coordinates(coords)
        config = ACOConfig(num_iterations=1, seed=42)
        
        optimizer = AntColonyOptimizer(problem, config)
        optimizer.run()
        
        pheromone = optimizer.get_pheromone_matrix()
        
        assert len(pheromone) == 3
        assert len(pheromone[0]) == 3
        
        # 对角线应为0
        for i in range(3):
            assert pheromone[i][i] == 0.0
    
    def test_stagnation_detection(self):
        """测试停滞检测"""
        coords = [(0, 0), (10, 0)]
        problem = TSPProblem.from_coordinates(coords)
        config = ACOConfig(
            num_iterations=20,
            stagnation_threshold=5,
            seed=42
        )
        
        optimizer = AntColonyOptimizer(problem, config)
        result = optimizer.run()
        
        # 两节点问题容易停滞
        assert isinstance(result.stagnation_detected, bool)
    
    def test_adaptive_parameters(self):
        """测试自适应参数"""
        coords = [(0, 0), (10, 0), (10, 10), (0, 10)]
        problem = TSPProblem.from_coordinates(coords)
        config = ACOConfig(
            num_iterations=10,
            adaptive=True,
            stagnation_threshold=3,
            seed=42
        )
        
        optimizer = AntColonyOptimizer(problem, config)
        result = optimizer.run()
        
        assert result.parameters_used is not None


class TestACOUtils:
    """ACOUtils便捷类测试"""
    
    def test_solve_tsp(self):
        """测试TSP求解便捷函数"""
        coords = [(0, 0), (10, 0), (10, 10), (0, 10)]
        result = ACOUtils.solve_tsp(coords, num_ants=10, num_iterations=20)
        
        assert isinstance(result, ACOResult)
        assert len(result.best_tour) == 4
        assert result.best_length > 0
    
    def test_solve_tsp_variants(self):
        """测试不同变体求解"""
        coords = [(0, 0), (10, 0), (10, 10), (0, 10)]
        
        for variant in ["as", "acs", "mmas"]:
            result = ACOUtils.solve_tsp(coords, variant=variant)
            assert result.best_length > 0
    
    def test_solve_random_tsp(self):
        """测试随机TSP求解"""
        result = ACOUtils.solve_random_tsp(8, num_ants=10, num_iterations=20, seed=42)
        
        assert isinstance(result, ACOResult)
        assert len(result.best_tour) == 8
    
    def test_compare_variants(self):
        """测试变体比较"""
        coords = [(0, 0), (10, 5), (20, 0), (15, 10)]
        results = ACOUtils.compare_variants(coords, num_iterations=10)
        
        assert len(results) == 3
        for name, result in results.items():
            assert isinstance(result, ACOResult)
    
    def test_visualize_tour_ascii(self):
        """测试ASCII可视化"""
        coords = [(0, 0), (10, 0), (10, 10), (0, 10)]
        tour = [0, 1, 2, 3]
        
        visualization = ACOUtils.visualize_tour_ascii(coords, tour)
        
        assert isinstance(visualization, str)
        assert 'S' in visualization  # 起点标记
        assert '*' in visualization  # 路径标记
    
    def test_format_result(self):
        """测试结果格式化"""
        coords = [(0, 0), (10, 0)]
        result = ACOUtils.solve_tsp(coords, num_iterations=5)
        
        formatted = ACOUtils.format_result(result)
        
        assert "蚁群优化算法结果" in formatted
        assert "最佳路径长度" in formatted
        assert "执行时间" in formatted


class TestConvenienceFunctions:
    """便捷函数测试"""
    
    def test_solve_tsp_function(self):
        """测试solve_tsp函数"""
        coords = [(0, 0), (10, 0), (10, 10)]
        result = solve_tsp(coords, num_ants=5, num_iterations=10)
        
        assert result.best_length > 0
        assert len(result.best_tour) == 3
    
    def test_solve_random_tsp_function(self):
        """测试solve_random_tsp函数"""
        result = solve_random_tsp(6, seed=42)
        
        assert len(result.best_tour) == 6
    
    def test_compare_variants_function(self):
        """测试compare_aco_variants函数"""
        coords = [(0, 0), (20, 10), (40, 0)]
        results = compare_aco_variants(coords, num_iterations=5)
        
        assert len(results) == 3
        assert all(isinstance(r, ACOResult) for r in results.values())
    
    def test_get_tsp_lower_bound(self):
        """测试下界估计"""
        coords = [(0, 0), (10, 0), (10, 10), (0, 10)]
        bound = get_tsp_lower_bound(coords)
        
        assert bound > 0
        assert bound <= 40.0  # 下界不超过最优解
    
    def test_nearest_neighbor_tour(self):
        """测试最近邻启发式"""
        coords = [(0, 0), (10, 0), (10, 10), (0, 10)]
        tour, length = nearest_neighbor_tour(coords)
        
        assert len(tour) == 4
        assert length > 0
        assert length <= 40.0
    
    def test_nearest_neighbor_with_start(self):
        """测试指定起点的最近邻"""
        coords = [(0, 0), (10, 0), (10, 10), (0, 10)]
        tour, length = nearest_neighbor_tour(coords, start=2)
        
        assert tour[0] == 2
        assert length > 0


class TestACOResult:
    """ACO结果类测试"""
    
    def test_result_properties(self):
        """测试结果属性"""
        coords = [(0, 0), (10, 0)]
        result = solve_tsp(coords, num_iterations=5)
        
        assert hasattr(result, 'best_tour')
        assert hasattr(result, 'best_length')
        assert hasattr(result, 'iteration_best')
        assert hasattr(result, 'avg_length')
        assert hasattr(result, 'convergence_iteration')
        assert hasattr(result, 'total_iterations')
        assert hasattr(result, 'execution_time')
        assert hasattr(result, 'improvement_rate')
        assert hasattr(result, 'stagnation_detected')
        assert hasattr(result, 'parameters_used')
    
    def test_improvement_rate(self):
        """测试改进率计算"""
        coords = [(0, 0), (10, 0), (10, 10), (0, 10)]
        result = solve_tsp(coords, num_ants=20, num_iterations=50)
        
        # 改进率应在合理范围
        assert 0 <= result.improvement_rate <= 100


class TestEdgeCases:
    """边界情况测试"""
    
    def test_two_nodes_problem(self):
        """测试两节点问题"""
        coords = [(0, 0), (10, 10)]
        result = solve_tsp(coords, num_iterations=5)
        
        # 两节点最优解是往返距离
        expected_length = 2 * 14.142  # 2 * sqrt(200)
        assert abs(result.best_length - expected_length) < 1
    
    def test_large_problem(self):
        """测试较大规模问题"""
        result = solve_random_tsp(20, num_ants=30, num_iterations=50, seed=42)
        
        assert len(result.best_tour) == 20
        assert result.best_length > 0
    
    def test_single_node_problem(self):
        """测试单节点问题"""
        coords = [(5, 5)]
        result = solve_tsp(coords, num_iterations=1)
        
        assert len(result.best_tour) == 1
        assert result.best_length == 0.0
    
    def test_zero_iterations(self):
        """测试零迭代"""
        coords = [(0, 0), (10, 0)]
        config = ACOConfig(num_iterations=0, seed=42)
        problem = TSPProblem.from_coordinates(coords)
        optimizer = AntColonyOptimizer(problem, config)
        result = optimizer.run()
        
        assert result.total_iterations == 0
    
    def test_seed_reproducibility(self):
        """测试随机种子可重现性"""
        coords = [(0, 0), (10, 0), (10, 10), (0, 10)]
        
        result1 = solve_tsp(coords, num_iterations=10, seed=123)
        result2 = solve_tsp(coords, num_iterations=10, seed=123)
        
        # 同样种子应产生相同结果
        assert result1.best_tour == result2.best_tour
        assert abs(result1.best_length - result2.best_length) < 0.001


class TestDataStructures:
    """数据结构测试"""
    
    def test_node(self):
        """测试Node数据结构"""
        node = Node(id=0, x=10.5, y=20.3)
        
        assert node.id == 0
        assert node.x == 10.5
        assert node.y == 20.3
    
    def test_ant(self):
        """测试Ant数据结构"""
        ant = Ant(
            tour=[0, 1, 2],
            visited={0, 1, 2},
            tour_length=30.0,
            current_node=2
        )
        
        assert ant.tour == [0, 1, 2]
        assert len(ant.visited) == 3
        assert ant.tour_length == 30.0
        assert ant.current_node == 2


def run_tests():
    """运行所有测试"""
    print("=" * 60)
    print("Ant Colony Optimization (ACO) Utils 测试")
    print("=" * 60)
    
    # 运行 pytest
    exit_code = pytest.main([__file__, "-v", "--tb=short"])
    
    if exit_code == 0:
        print("\n所有测试通过！ ✓")
    else:
        print("\n部分测试失败！ ✗")
    
    return exit_code


if __name__ == '__main__':
    run_tests()
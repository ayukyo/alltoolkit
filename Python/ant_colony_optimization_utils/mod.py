#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ant Colony Optimization (ACO) Utils - 蚁群优化算法工具库
==========================================================

蚁群优化算法是一种模拟蚂蚁觅食行为的元启发式优化算法，
广泛应用于组合优化问题，如旅行商问题(TSP)、车辆路径问题(VRP)等。

功能列表:
- Ant System (AS) - 基本蚁群算法
- Ant Colony System (ACS) - 蚁群系统
- Max-Min Ant System (MMAS) - 最大最小蚁群系统
- TSP求解器 (旅行商问题)
- 参数调优工具
- 收敛分析
- 自适应参数调整

特点:
- 零外部依赖，纯Python实现
- 支持自定义问题求解
- 提供多种变体算法
- 完善的参数配置

作者: AllToolkit 自动化生成
日期: 2026-05-28
"""

from typing import List, Tuple, Dict, Any, Optional, Callable, Set
from dataclasses import dataclass, field
from enum import Enum
import math
import random
import time


class ACOVariant(Enum):
    """蚁群算法变体"""
    AS = "ant_system"           # 基本蚁群系统
    ACS = "ant_colony_system"   # 蚁群系统
    MMAS = "max_min_ant_system" # 最大最小蚁群系统


@dataclass
class ACOConfig:
    """蚁群算法配置参数"""
    num_ants: int = 20                  # 蚂蚁数量
    num_iterations: int = 100           # 迭代次数
    alpha: float = 1.0                  # 信息素重要程度因子
    beta: float = 2.0                   # 启发信息重要程度因子
    rho: float = 0.5                    # 信息素挥发系数
    q0: float = 0.9                     # ACS: 探索/利用平衡参数
    tau_min: float = 0.1                # MMAS: 最小信息素
    tau_max: float = 10.0               # MMAS: 最大信息素
    initial_tau: float = 1.0            # 初始信息素浓度
    variant: ACOVariant = ACOVariant.AS # 算法变体
    seed: Optional[int] = None          # 随机种子
    elite_weight: int = 1               # 精英蚂蚁权重
    stagnation_threshold: int = 10      # 停滞检测阈值
    adaptive: bool = False              # 是否启用自适应参数


@dataclass
class Ant:
    """蚂蚁个体"""
    tour: List[int] = field(default_factory=list)  # 访问路径
    visited: Set[int] = field(default_factory=set) # 已访问节点
    tour_length: float = 0.0                       # 路径长度
    current_node: int = -1                         # 当前位置


@dataclass
class ACOResult:
    """蚁群算法结果"""
    best_tour: List[int]                    # 最佳路径
    best_length: float                      # 最佳路径长度
    iteration_best: List[float]             # 每代最佳长度
    avg_length: List[float]                 # 每代平均长度
    convergence_iteration: int              # 收敛迭代次数
    total_iterations: int                   # 总迭代次数
    execution_time: float                   # 执行时间(秒)
    improvement_rate: float                 # 改进率
    stagnation_detected: bool               # 是否检测到停滞
    parameters_used: Dict[str, Any]         # 使用的参数


@dataclass
class Node:
    """节点数据"""
    id: int
    x: float
    y: float


class TSPProblem:
    """TSP问题定义"""
    
    def __init__(self, nodes: List[Node], symmetric: bool = True):
        """
        初始化TSP问题
        
        Args:
            nodes: 节点列表
            symmetric: 是否对称TSP (默认True)
        """
        self.nodes = nodes
        self.num_nodes = len(nodes)
        self.symmetric = symmetric
        self._distance_matrix = self._compute_distance_matrix()
        self._heuristic_matrix = self._compute_heuristic_matrix()
    
    def _compute_distance_matrix(self) -> List[List[float]]:
        """计算距离矩阵"""
        matrix = [[0.0] * self.num_nodes for _ in range(self.num_nodes)]
        for i in range(self.num_nodes):
            for j in range(self.num_nodes):
                if i != j:
                    dx = self.nodes[i].x - self.nodes[j].x
                    dy = self.nodes[i].y - self.nodes[j].y
                    matrix[i][j] = math.sqrt(dx * dx + dy * dy)
        return matrix
    
    def _compute_heuristic_matrix(self) -> List[List[float]]:
        """计算启发信息矩阵 (η = 1/d)"""
        matrix = [[0.0] * self.num_nodes for _ in range(self.num_nodes)]
        for i in range(self.num_nodes):
            for j in range(self.num_nodes):
                if i != j and self._distance_matrix[i][j] > 0:
                    matrix[i][j] = 1.0 / self._distance_matrix[i][j]
        return matrix
    
    def get_distance(self, i: int, j: int) -> float:
        """获取节点间距离"""
        return self._distance_matrix[i][j]
    
    def get_heuristic(self, i: int, j: int) -> float:
        """获取启发信息"""
        return self._heuristic_matrix[i][j]
    
    def compute_tour_length(self, tour: List[int]) -> float:
        """计算路径长度"""
        if len(tour) < 2:
            return 0.0
        length = 0.0
        for i in range(len(tour) - 1):
            length += self._distance_matrix[tour[i]][tour[i + 1]]
        # 回到起点
        length += self._distance_matrix[tour[-1]][tour[0]]
        return length
    
    @classmethod
    def from_coordinates(cls, coordinates: List[Tuple[float, float]]) -> 'TSPProblem':
        """从坐标列表创建TSP问题"""
        nodes = [Node(id=i, x=coord[0], y=coord[1]) 
                 for i, coord in enumerate(coordinates)]
        return cls(nodes)
    
    @classmethod
    def random_problem(cls, num_nodes: int, 
                       min_coord: float = 0.0, 
                       max_coord: float = 100.0,
                       seed: Optional[int] = None) -> 'TSPProblem':
        """生成随机TSP问题"""
        if seed is not None:
            random.seed(seed)
        nodes = [Node(id=i, 
                      x=random.uniform(min_coord, max_coord), 
                      y=random.uniform(min_coord, max_coord))
                 for i in range(num_nodes)]
        return cls(nodes)


class AntColonyOptimizer:
    """蚁群优化器核心类"""
    
    def __init__(self, problem: TSPProblem, config: Optional[ACOConfig] = None):
        """
        初始化蚁群优化器
        
        Args:
            problem: TSP问题实例
            config: 配置参数
        """
        self.problem = problem
        self.config = config or ACOConfig()
        
        if self.config.seed is not None:
            random.seed(self.config.seed)
        
        # 初始化信息素矩阵
        self._pheromone = self._init_pheromone()
        
        # 统计数据
        self._best_tour: List[int] = []
        self._best_length: float = float('inf')
        self._iteration_best_lengths: List[float] = []
        self._avg_lengths: List[float] = []
        self._stagnation_count: int = 0
        self._last_best_length: float = float('inf')
    
    def _init_pheromone(self) -> List[List[float]]:
        """初始化信息素矩阵"""
        n = self.problem.num_nodes
        tau = self.config.initial_tau
        
        if self.config.variant == ACOVariant.MMAS:
            tau = self.config.tau_max
        
        return [[tau if i != j else 0.0 for j in range(n)] for i in range(n)]
    
    def _create_ants(self) -> List[Ant]:
        """创建蚂蚁群"""
        ants = []
        for _ in range(self.config.num_ants):
            start_node = random.randint(0, self.problem.num_nodes - 1)
            ant = Ant(
                tour=[start_node],
                visited={start_node},
                current_node=start_node
            )
            ants.append(ant)
        return ants
    
    def _select_next_node_as(self, ant: Ant) -> int:
        """Ant System: 基于概率选择下一节点"""
        current = ant.current_node
        unvisited = [i for i in range(self.problem.num_nodes) 
                     if i not in ant.visited]
        
        if not unvisited:
            return -1
        
        # 计算选择概率
        probabilities = []
        total = 0.0
        
        for node in unvisited:
            tau = self._pheromone[current][node] ** self.config.alpha
            eta = self.problem.get_heuristic(current, node) ** self.config.beta
            prob = tau * eta
            probabilities.append(prob)
            total += prob
        
        # 归一化概率
        if total > 0:
            probabilities = [p / total for p in probabilities]
        else:
            probabilities = [1.0 / len(unvisited) for _ in unvisited]
        
        # 轮盘赌选择
        r = random.random()
        cumsum = 0.0
        for i, prob in enumerate(probabilities):
            cumsum += prob
            if r <= cumsum:
                return unvisited[i]
        
        return unvisited[-1]
    
    def _select_next_node_acs(self, ant: Ant) -> int:
        """Ant Colony System: 混合探索与利用策略"""
        current = ant.current_node
        unvisited = [i for i in range(self.problem.num_nodes) 
                     if i not in ant.visited]
        
        if not unvisited:
            return -1
        
        q = random.random()
        
        if q <= self.config.q0:
            # 利用: 选择信息素和启发信息乘积最大的节点
            best_node = unvisited[0]
            best_value = -float('inf')
            
            for node in unvisited:
                tau = self._pheromone[current][node]
                eta = self.problem.get_heuristic(current, node)
                value = tau * eta
                if value > best_value:
                    best_value = value
                    best_node = node
            
            return best_node
        else:
            # 探索: 基于概率选择 (同AS)
            return self._select_next_node_as(ant)
    
    def _select_next_node(self, ant: Ant) -> int:
        """根据算法变体选择下一节点"""
        if self.config.variant == ACOVariant.ACS:
            return self._select_next_node_acs(ant)
        else:
            return self._select_next_node_as(ant)
    
    def _construct_tours(self, ants: List[Ant]) -> None:
        """构建蚂蚁路径"""
        for ant in ants:
            while len(ant.tour) < self.problem.num_nodes:
                next_node = self._select_next_node(ant)
                if next_node == -1:
                    break
                ant.tour.append(next_node)
                ant.visited.add(next_node)
                ant.current_node = next_node
            
            # 计算路径长度
            ant.tour_length = self.problem.compute_tour_length(ant.tour)
    
    def _update_pheromone_as(self, ants: List[Ant]) -> None:
        """Ant System: 全局信息素更新"""
        n = self.problem.num_nodes
        rho = self.config.rho
        
        # 信息素挥发
        for i in range(n):
            for j in range(n):
                if i != j:
                    self._pheromone[i][j] *= (1 - rho)
        
        # 信息素增强 (所有蚂蚁)
        for ant in ants:
            if ant.tour_length > 0:
                delta = 1.0 / ant.tour_length
                for i in range(len(ant.tour) - 1):
                    from_node = ant.tour[i]
                    to_node = ant.tour[i + 1]
                    self._pheromone[from_node][to_node] += delta
                    if self.problem.symmetric:
                        self._pheromone[to_node][from_node] += delta
                
                # 回到起点
                self._pheromone[ant.tour[-1]][ant.tour[0]] += delta
                if self.problem.symmetric:
                    self._pheromone[ant.tour[0]][ant.tour[-1]] += delta
        
        # 精英蚂蚁额外增强
        if self._best_tour and self._best_length > 0:
            elite_delta = self.config.elite_weight / self._best_length
            for i in range(len(self._best_tour) - 1):
                from_node = self._best_tour[i]
                to_node = self._best_tour[i + 1]
                self._pheromone[from_node][to_node] += elite_delta
                if self.problem.symmetric:
                    self._pheromone[to_node][from_node] += elite_delta
            self._pheromone[self._best_tour[-1]][self._best_tour[0]] += elite_delta
            if self.problem.symmetric:
                self._pheromone[self._best_tour[0]][self._best_tour[-1]] += elite_delta
    
    def _update_pheromone_acs(self, ants: List[Ant]) -> None:
        """Ant Colony System: 局部+全局信息素更新"""
        n = self.problem.num_nodes
        rho = self.config.rho
        
        # 找出最佳蚂蚁
        best_ant = min(ants, key=lambda a: a.tour_length)
        
        # 全局更新: 仅最佳蚂蚁贡献
        for i in range(n):
            for j in range(n):
                if i != j:
                    self._pheromone[i][j] *= (1 - rho)
        
        # 最佳蚂蚁路径增强
        if best_ant.tour_length > 0:
            delta = rho / best_ant.tour_length
            for i in range(len(best_ant.tour) - 1):
                from_node = best_ant.tour[i]
                to_node = best_ant.tour[i + 1]
                self._pheromone[from_node][to_node] += delta
                if self.problem.symmetric:
                    self._pheromone[to_node][from_node] += delta
            self._pheromone[best_ant.tour[-1]][best_ant.tour[0]] += delta
            if self.problem.symmetric:
                self._pheromone[best_ant.tour[0]][best_ant.tour[-1]] += delta
    
    def _update_pheromone_mmas(self, ants: List[Ant]) -> None:
        """Max-Min Ant System: 信息素限制"""
        n = self.problem.num_nodes
        rho = self.config.rho
        tau_min = self.config.tau_min
        tau_max = self.config.tau_max
        
        # 信息素挥发
        for i in range(n):
            for j in range(n):
                if i != j:
                    self._pheromone[i][j] *= (1 - rho)
                    # 应用边界限制
                    self._pheromone[i][j] = max(tau_min, 
                                                  min(tau_max, 
                                                      self._pheromone[i][j]))
        
        # 仅最佳蚂蚁增强
        best_ant = min(ants, key=lambda a: a.tour_length)
        if best_ant.tour_length > 0:
            delta = 1.0 / best_ant.tour_length
            
            for i in range(len(best_ant.tour) - 1):
                from_node = best_ant.tour[i]
                to_node = best_ant.tour[i + 1]
                self._pheromone[from_node][to_node] += delta
                if self.problem.symmetric:
                    self._pheromone[to_node][from_node] += delta
                # 再次应用边界限制
                self._pheromone[from_node][to_node] = min(tau_max, 
                                                           self._pheromone[from_node][to_node])
                if self.problem.symmetric:
                    self._pheromone[to_node][from_node] = min(tau_max, 
                                                               self._pheromone[to_node][from_node])
            
            self._pheromone[best_ant.tour[-1]][best_ant.tour[0]] += delta
            if self.problem.symmetric:
                self._pheromone[best_ant.tour[0]][best_ant.tour[-1]] += delta
    
    def _update_pheromone(self, ants: List[Ant]) -> None:
        """根据算法变体更新信息素"""
        if self.config.variant == ACOVariant.AS:
            self._update_pheromone_as(ants)
        elif self.config.variant == ACOVariant.ACS:
            self._update_pheromone_acs(ants)
        elif self.config.variant == ACOVariant.MMAS:
            self._update_pheromone_mmas(ants)
    
    def _check_stagnation(self) -> bool:
        """检测算法停滞"""
        if abs(self._best_length - self._last_best_length) < 1e-6:
            self._stagnation_count += 1
        else:
            self._stagnation_count = 0
            self._last_best_length = self._best_length
        
        return self._stagnation_count >= self.config.stagnation_threshold
    
    def _adaptive_adjustment(self) -> None:
        """自适应参数调整"""
        if self._stagnation_count > 0:
            # 增加探索能力
            self.config.alpha = max(0.5, self.config.alpha * 0.95)
            self.config.beta = min(5.0, self.config.beta * 1.05)
            self.config.rho = min(0.8, self.config.rho * 1.1)
            
            # MMAS: 放宽信息素限制
            if self.config.variant == ACOVariant.MMAS:
                self.config.tau_min *= 0.9
                self.config.tau_max *= 1.1
    
    def run(self) -> ACOResult:
        """
        运行蚁群优化算法
        
        Returns:
            ACOResult: 优化结果
        """
        start_time = time.time()
        
        # 初始化最优解
        initial_tour = list(range(self.problem.num_nodes))
        random.shuffle(initial_tour)
        self._best_tour = initial_tour
        self._best_length = self.problem.compute_tour_length(initial_tour)
        
        convergence_iteration = -1
        
        for iteration in range(self.config.num_iterations):
            # 创建蚂蚁群
            ants = self._create_ants()
            
            # 构建路径
            self._construct_tours(ants)
            
            # 更新最优解
            iteration_best_ant = min(ants, key=lambda a: a.tour_length)
            if iteration_best_ant.tour_length < self._best_length:
                self._best_tour = iteration_best_ant.tour.copy()
                self._best_length = iteration_best_ant.tour_length
                convergence_iteration = iteration
            
            # 记录统计数据
            avg_length = sum(a.tour_length for a in ants) / len(ants)
            self._iteration_best_lengths.append(iteration_best_ant.tour_length)
            self._avg_lengths.append(avg_length)
            
            # 更新信息素
            self._update_pheromone(ants)
            
            # 检测停滞
            stagnation = self._check_stagnation()
            
            # 自适应调整
            if self.config.adaptive and stagnation:
                self._adaptive_adjustment()
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # 计算改进率
        initial_length = self._iteration_best_lengths[0] if self._iteration_best_lengths else 0
        improvement_rate = 0.0
        if initial_length > 0:
            improvement_rate = (initial_length - self._best_length) / initial_length * 100
        
        return ACOResult(
            best_tour=self._best_tour,
            best_length=self._best_length,
            iteration_best=self._iteration_best_lengths,
            avg_length=self._avg_lengths,
            convergence_iteration=convergence_iteration,
            total_iterations=self.config.num_iterations,
            execution_time=execution_time,
            improvement_rate=improvement_rate,
            stagnation_detected=self._stagnation_count >= self.config.stagnation_threshold,
            parameters_used={
                'variant': self.config.variant.value,
                'num_ants': self.config.num_ants,
                'alpha': self.config.alpha,
                'beta': self.config.beta,
                'rho': self.config.rho,
            }
        )
    
    def get_pheromone_matrix(self) -> List[List[float]]:
        """获取当前信息素矩阵"""
        return self._pheromone


class ACOUtils:
    """蚁群优化便捷工具类"""
    
    @staticmethod
    def solve_tsp(coordinates: List[Tuple[float, float]], 
                  num_ants: int = 20,
                  num_iterations: int = 100,
                  variant: str = "as",
                  seed: Optional[int] = None) -> ACOResult:
        """
        快速求解TSP问题
        
        Args:
            coordinates: 节点坐标列表 [(x1, y1), (x2, y2), ...]
            num_ants: 蚂蚁数量
            num_iterations: 迭代次数
            variant: 算法变体 ("as", "acs", "mmas")
            seed: 随机种子
            
        Returns:
            ACOResult: 优化结果
        """
        problem = TSPProblem.from_coordinates(coordinates)
        
        variant_map = {
            "as": ACOVariant.AS,
            "acs": ACOVariant.ACS,
            "mmas": ACOVariant.MMAS,
        }
        
        config = ACOConfig(
            num_ants=num_ants,
            num_iterations=num_iterations,
            variant=variant_map.get(variant.lower(), ACOVariant.AS),
            seed=seed
        )
        
        optimizer = AntColonyOptimizer(problem, config)
        return optimizer.run()
    
    @staticmethod
    def solve_random_tsp(num_nodes: int,
                         num_ants: int = 20,
                         num_iterations: int = 100,
                         seed: Optional[int] = None) -> ACOResult:
        """
        求解随机生成的TSP问题
        
        Args:
            num_nodes: 节点数量
            num_ants: 蚂蚁数量
            num_iterations: 迭代次数
            seed: 随机种子
            
        Returns:
            ACOResult: 优化结果
        """
        problem = TSPProblem.random_problem(num_nodes, seed=seed)
        config = ACOConfig(
            num_ants=num_ants,
            num_iterations=num_iterations,
            seed=seed
        )
        optimizer = AntColonyOptimizer(problem, config)
        return optimizer.run()
    
    @staticmethod
    def compare_variants(coordinates: List[Tuple[float, float]],
                         num_iterations: int = 50) -> Dict[str, ACOResult]:
        """
        比较不同算法变体的性能
        
        Args:
            coordinates: 节点坐标
            num_iterations: 迭代次数
            
        Returns:
            各变体的结果字典
        """
        results = {}
        problem = TSPProblem.from_coordinates(coordinates)
        
        for variant in ACOVariant:
            config = ACOConfig(num_iterations=num_iterations, variant=variant)
            optimizer = AntColonyOptimizer(problem, config)
            results[variant.value] = optimizer.run()
        
        return results
    
    @staticmethod
    def visualize_tour_ascii(coordinates: List[Tuple[float, float]],
                             tour: List[int],
                             width: int = 40,
                             height: int = 20) -> str:
        """
        ASCII可视化路径
        
        Args:
            coordinates: 坐标列表
            tour: 路径
            width: 显示宽度
            height: 显示高度
            
        Returns:
            ASCII字符串
        """
        if not coordinates or not tour:
            return ""
        
        # 找出坐标范围
        min_x = min(c[0] for c in coordinates)
        max_x = max(c[0] for c in coordinates)
        min_y = min(c[1] for c in coordinates)
        max_y = max(c[1] for c in coordinates)
        
        # 防止除零
        x_range = max_x - min_x or 1
        y_range = max_y - min_y or 1
        
        # 创建画布
        canvas = [[' ' for _ in range(width)] for _ in range(height)]
        
        # 绘制节点和路径
        for i in range(len(tour)):
            node_idx = tour[i]
            next_idx = tour[(i + 1) % len(tour)]
            
            # 当前节点坐标
            x1, y1 = coordinates[node_idx]
            x2, y2 = coordinates[next_idx]
            
            # 转换到画布坐标
            cx1 = int((x1 - min_x) / x_range * (width - 1))
            cy1 = int((y1 - min_y) / y_range * (height - 1))
            cx2 = int((x2 - min_x) / x_range * (width - 1))
            cy2 = int((y2 - min_y) / y_range * (height - 1))
            
            # 绘制节点
            canvas[cy1][cx1] = '*'
            
            # 绘制路径线段 (简化: 只画终点)
            canvas[cy2][cx2] = '*'
        
        # 绘制起点标记
        start_idx = tour[0]
        sx = int((coordinates[start_idx][0] - min_x) / x_range * (width - 1))
        sy = int((coordinates[start_idx][1] - min_y) / y_range * (height - 1))
        canvas[sy][sx] = 'S'
        
        # 转换为字符串
        lines = [''.join(row) for row in canvas]
        return '\n' + '\n'.join(lines) + '\n'
    
    @staticmethod
    def format_result(result: ACOResult) -> str:
        """
        格式化输出结果
        
        Args:
            result: ACO结果
            
        Returns:
            格式化字符串
        """
        lines = [
            "=" * 50,
            "蚁群优化算法结果",
            "=" * 50,
            f"最佳路径长度: {result.best_length:.2f}",
            f"最佳路径: {result.best_tour[:10]}{'...' if len(result.best_tour) > 10 else ''}",
            f"收敛迭代: {result.convergence_iteration}",
            f"执行时间: {result.execution_time:.3f}秒",
            f"改进率: {result.improvement_rate:.2f}%",
            f"停滞检测: {result.stagnation_detected}",
            "-" * 50,
            "参数配置:",
        ]
        
        for key, value in result.parameters_used.items():
            lines.append(f"  {key}: {value}")
        
        lines.append("=" * 50)
        return '\n'.join(lines)


# =============================================================================
# 便捷函数
# =============================================================================

def solve_tsp(coordinates: List[Tuple[float, float]],
              num_ants: int = 20,
              num_iterations: int = 100,
              variant: str = "as",
              seed: Optional[int] = None) -> ACOResult:
    """
    求解TSP问题（便捷函数）
    
    Args:
        coordinates: 坐标列表 [(x, y), ...]
        num_ants: 蚂蚁数量
        num_iterations: 迭代次数
        variant: 算法变体 ("as", "acs", "mmas")
        seed: 随机种子
        
    Returns:
        ACOResult: 结果对象
        
    Example:
        >>> coords = [(0, 0), (10, 0), (10, 10), (0, 10)]
        >>> result = solve_tsp(coords)
        >>> print(result.best_length)
    """
    return ACOUtils.solve_tsp(coordinates, num_ants, num_iterations, variant, seed)


def solve_random_tsp(num_nodes: int,
                     num_ants: int = 20,
                     num_iterations: int = 100,
                     seed: Optional[int] = None) -> ACOResult:
    """
    求解随机TSP问题（便捷函数）
    
    Args:
        num_nodes: 节点数量
        num_ants: 蚂蚁数量
        num_iterations: 迭代次数
        seed: 随机种子
        
    Returns:
        ACOResult: 结果对象
        
    Example:
        >>> result = solve_random_tsp(20, seed=42)
        >>> print(result.best_length)
    """
    return ACOUtils.solve_random_tsp(num_nodes, num_ants, num_iterations, seed)


def compare_aco_variants(coordinates: List[Tuple[float, float]],
                         num_iterations: int = 50) -> Dict[str, ACOResult]:
    """
    比较不同ACO变体（便捷函数）
    
    Args:
        coordinates: 节点坐标
        num_iterations: 迭代次数
        
    Returns:
        各变体结果字典
        
    Example:
        >>> coords = [(0, 0), (10, 10), (20, 5), (15, 15)]
        >>> results = compare_aco_variants(coords)
        >>> for name, result in results.items():
        >>>     print(f"{name}: {result.best_length}")
    """
    return ACOUtils.compare_variants(coordinates, num_iterations)


def get_tsp_lower_bound(coordinates: List[Tuple[float, float]]) -> float:
    """
    计算TSP问题的下界估计（最近邻启发）
    
    Args:
        coordinates: 坐标列表
        
    Returns:
        下界估计值
        
    Example:
        >>> coords = [(0, 0), (10, 0), (10, 10), (0, 10)]
        >>> bound = get_tsp_lower_bound(coords)
        >>> print(bound)  # 约40.0 (矩形周长)
    """
    if len(coordinates) < 2:
        return 0.0
    
    # 计算所有边长的总和的下界
    # 对于每个节点，取到最近邻的距离之和
    total = 0.0
    n = len(coordinates)
    
    for i in range(n):
        min_dist = float('inf')
        for j in range(n):
            if i != j:
                dx = coordinates[i][0] - coordinates[j][0]
                dy = coordinates[i][1] - coordinates[j][1]
                dist = math.sqrt(dx * dx + dy * dy)
                if dist < min_dist:
                    min_dist = dist
        total += min_dist
    
    return total / 2  # 每条边被计算两次


def nearest_neighbor_tour(coordinates: List[Tuple[float, float]],
                          start: int = 0) -> Tuple[List[int], float]:
    """
    最近邻启发式算法求初始解
    
    Args:
        coordinates: 坐标列表
        start: 起始节点
        
    Returns:
        (路径, 长度)
        
    Example:
        >>> coords = [(0, 0), (10, 0), (10, 10), (0, 10)]
        >>> tour, length = nearest_neighbor_tour(coords)
        >>> print(tour, length)
    """
    if len(coordinates) < 2:
        return [0], 0.0
    
    n = len(coordinates)
    tour = [start]
    visited = {start}
    current = start
    total_length = 0.0
    
    while len(tour) < n:
        best_next = -1
        best_dist = float('inf')
        
        for j in range(n):
            if j not in visited:
                dx = coordinates[current][0] - coordinates[j][0]
                dy = coordinates[current][1] - coordinates[j][1]
                dist = math.sqrt(dx * dx + dy * dy)
                if dist < best_dist:
                    best_dist = dist
                    best_next = j
        
        tour.append(best_next)
        visited.add(best_next)
        total_length += best_dist
        current = best_next
    
    # 回到起点
    dx = coordinates[current][0] - coordinates[start][0]
    dy = coordinates[current][1] - coordinates[start][1]
    total_length += math.sqrt(dx * dx + dy * dy)
    
    return tour, total_length


# =============================================================================
# 主函数
# =============================================================================

if __name__ == '__main__':
    print("=" * 60)
    print("Ant Colony Optimization (ACO) Utils - 蚁群优化算法示例")
    print("=" * 60)
    
    # 示例1: 简单矩形TSP
    print("\n【示例1: 简单矩形TSP】")
    rectangle_coords = [(0, 0), (10, 0), (10, 10), (0, 10)]
    result = solve_tsp(rectangle_coords, num_ants=10, num_iterations=50)
    print(ACOUtils.format_result(result))
    
    # 最近邻启发式对比
    nn_tour, nn_length = nearest_neighbor_tour(rectangle_coords)
    print(f"最近邻启发式结果: {nn_length:.2f}")
    
    # 示例2: 随机TSP问题
    print("\n【示例2: 随机TSP问题(10节点)】")
    random_result = solve_random_tsp(10, num_ants=15, num_iterations=100, seed=42)
    print(ACOUtils.format_result(random_result))
    
    # 示例3: 比较算法变体
    print("\n【示例3: 比较不同算法变体】")
    test_coords = [(0, 0), (20, 10), (40, 0), (30, 20), (10, 30), (50, 15)]
    comparison = compare_aco_variants(test_coords, num_iterations=30)
    
    print("变体性能对比:")
    for name, res in comparison.items():
        print(f"  {name:20s}: 最佳长度 {res.best_length:.2f}, "
              f"时间 {res.execution_time:.3f}s")
    
    # 示例4: TSP下界估计
    print("\n【示例4: 下界估计】")
    bound = get_tsp_lower_bound(test_coords)
    best_result = min(comparison.values(), key=lambda r: r.best_length)
    print(f"理论下界估计: {bound:.2f}")
    print(f"实际最优解: {best_result.best_length:.2f}")
    print(f"解质量: {(bound / best_result.best_length * 100):.1f}% (相对于下界)")
    
    print("\n" + "=" * 60)
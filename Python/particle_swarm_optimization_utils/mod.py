"""
粒子群优化算法工具模块 (Particle Swarm Optimization Utils)

提供完整的粒子群优化算法实现，支持：
- 连续空间优化问题
- 多种惯性权重策略
- 约束处理
- 并行评估
- 自适应参数调整
- 收敛性分析

零外部依赖，纯 Python 标准库实现。
"""

import random
import math
import copy
from typing import List, Callable, Tuple, Optional, Dict, Any, Union
from dataclasses import dataclass, field
from enum import Enum


class InertiaWeightStrategy(Enum):
    """惯性权重策略枚举"""
    CONSTANT = "constant"           # 固定权重
    LINEAR_DECREASING = "linear"    # 线性递减
    EXPONENTIAL = "exponential"     # 指数递减
    RANDOM = "random"               # 随机权重
    ADAPTIVE = "adaptive"           # 自适应权重


class BoundaryHandling(Enum):
    """边界处理策略枚举"""
    CLAMP = "clamp"                 # 截断到边界
    REFLECT = "reflect"             # 反弹
    PERIODIC = "periodic"           # 周期性边界
    RANDOM = "random"              # 随机重置


@dataclass
class PSOConfig:
    """PSO 算法配置"""
    swarm_size: int = 30                       # 粒子数量
    max_iterations: int = 100                  # 最大迭代次数
    inertia_weight: float = 0.729              # 惯性权重
    cognitive_coeff: float = 1.49445          # 认知系数 (c1)
    social_coeff: float = 1.49445               # 社会系数 (c2)
    inertia_strategy: InertiaWeightStrategy = InertiaWeightStrategy.CONSTANT
    boundary_handling: BoundaryHandling = BoundaryHandling.CLAMP
    min_inertia: float = 0.4                   # 最小惯性权重
    max_inertia: float = 0.9                   # 最大惯性权重
    velocity_clamp: Optional[float] = None     # 速度限制
    early_stop_patience: int = 20              # 早停耐心值
    early_stop_threshold: float = 1e-8         # 早停阈值
    seed: Optional[int] = None                 # 随机种子


@dataclass
class Particle:
    """粒子类"""
    position: List[float]                      # 当前位置
    velocity: List[float]                       # 当前速度
    best_position: List[float] = field(default_factory=list)  # 个体最优位置
    best_fitness: float = float('inf')         # 个体最优适应度
    current_fitness: float = float('inf')       # 当前适应度
    
    def __post_init__(self):
        if not self.best_position:
            self.best_position = copy.copy(self.position)


@dataclass
class OptimizationResult:
    """优化结果"""
    best_position: List[float]                 # 全局最优位置
    best_fitness: float                         # 全局最优适应度
    convergence_history: List[float]            # 收敛历史
    iteration_count: int                         # 迭代次数
    swarm: List[Particle] = field(default_factory=list)  # 最终粒子群
    metadata: Dict[str, Any] = field(default_factory=dict)  # 元数据


class ParticleSwarmOptimizer:
    """
    粒子群优化器
    
    实现标准 PSO 算法及多种变体，支持：
    - 自定义目标函数
    - 多维度优化
    - 边界约束
    - 多种参数策略
    
    使用示例：
    >>> def sphere(x):
    ...     return sum(xi**2 for xi in x)
    >>> optimizer = ParticleSwarmOptimizer(
    ...     objective_func=sphere,
    ...     bounds=[(-5, 5)] * 10,
    ...     config=PSOConfig(swarm_size=50, max_iterations=200)
    ... )
    >>> result = optimizer.optimize()
    >>> print(f"最优值: {result.best_fitness}")
    """
    
    def __init__(
        self,
        objective_func: Callable[[List[float]], float],
        bounds: List[Tuple[float, float]],
        config: Optional[PSOConfig] = None,
        minimize: bool = True
    ):
        """
        初始化粒子群优化器
        
        Args:
            objective_func: 目标函数，接受位置向量，返回适应度值
            bounds: 每个维度的边界 [(min, max), ...]
            config: PSO 配置，None 则使用默认配置
            minimize: True 为最小化问题，False 为最大化问题
        """
        self.objective_func = objective_func
        self.bounds = bounds
        self.config = config or PSOConfig()
        self.minimize = minimize
        self.dimensions = len(bounds)
        
        # 设置随机种子
        if self.config.seed is not None:
            random.seed(self.config.seed)
        
        # 状态变量
        self.swarm: List[Particle] = []
        self.global_best_position: List[float] = []
        self.global_best_fitness: float = float('inf') if minimize else float('-inf')
        self.convergence_history: List[float] = []
        self.iteration: int = 0
        
        # 验证参数
        self._validate_config()
    
    def _validate_config(self):
        """验证配置参数"""
        if self.config.swarm_size < 1:
            raise ValueError("粒子数量必须大于 0")
        if self.config.max_iterations < 1:
            raise ValueError("最大迭代次数必须大于 0")
        if self.config.cognitive_coeff < 0 or self.config.social_coeff < 0:
            raise ValueError("认知系数和社会系数必须非负")
    
    def _initialize_swarm(self):
        """初始化粒子群"""
        self.swarm = []
        
        for _ in range(self.config.swarm_size):
            # 随机初始化位置
            position = [
                random.uniform(self.bounds[d][0], self.bounds[d][1])
                for d in range(self.dimensions)
            ]
            
            # 随机初始化速度（基于边界范围）
            velocity = []
            for d in range(self.dimensions):
                range_d = self.bounds[d][1] - self.bounds[d][0]
                max_vel = range_d * 0.1  # 最大速度为范围的 10%
                velocity.append(random.uniform(-max_vel, max_vel))
            
            self.swarm.append(Particle(
                position=position,
                velocity=velocity
            ))
    
    def _evaluate_fitness(self, position: List[float]) -> float:
        """评估适应度"""
        fitness = self.objective_func(position)
        if not self.minimize:
            fitness = -fitness  # 最大化转为最小化处理
        return fitness
    
    def _update_inertia_weight(self) -> float:
        """根据策略更新惯性权重"""
        strategy = self.config.inertia_strategy
        
        if strategy == InertiaWeightStrategy.CONSTANT:
            return self.config.inertia_weight
        
        elif strategy == InertiaWeightStrategy.LINEAR_DECREASING:
            progress = self.iteration / self.config.max_iterations
            return self.config.max_inertia - \
                   (self.config.max_inertia - self.config.min_inertia) * progress
        
        elif strategy == InertiaWeightStrategy.EXPONENTIAL:
            progress = self.iteration / self.config.max_iterations
            return self.config.max_inertia * \
                   math.pow(self.config.min_inertia / self.config.max_inertia, progress)
        
        elif strategy == InertiaWeightStrategy.RANDOM:
            return random.uniform(self.config.min_inertia, self.config.max_inertia)
        
        elif strategy == InertiaWeightStrategy.ADAPTIVE:
            # 自适应权重：基于收敛程度
            if len(self.convergence_history) < 2:
                return self.config.max_inertia
            
            # 计算最近改进程度
            recent_improvement = abs(
                self.convergence_history[-1] - self.convergence_history[-2]
            )
            avg_fitness = abs(sum(self.convergence_history[-5:]) / min(5, len(self.convergence_history)))
            
            if avg_fitness > 0:
                improvement_ratio = recent_improvement / avg_fitness
                # 改进大则减小惯性，改进小则增大惯性
                if improvement_ratio > 0.01:
                    return self.config.min_inertia
                else:
                    return self.config.max_inertia
            return self.config.inertia_weight
        
        return self.config.inertia_weight
    
    def _apply_boundary(self, position: List[float]) -> List[float]:
        """应用边界约束"""
        result = []
        
        for d in range(self.dimensions):
            min_b, max_b = self.bounds[d]
            value = position[d]
            
            if self.config.boundary_handling == BoundaryHandling.CLAMP:
                result.append(max(min_b, min(max_b, value)))
            
            elif self.config.boundary_handling == BoundaryHandling.REFLECT:
                while value < min_b or value > max_b:
                    if value < min_b:
                        value = min_b + (min_b - value)
                    if value > max_b:
                        value = max_b - (value - max_b)
                result.append(max(min_b, min(max_b, value)))
            
            elif self.config.boundary_handling == BoundaryHandling.PERIODIC:
                if value < min_b:
                    value = max_b - ((min_b - value) % (max_b - min_b))
                elif value > max_b:
                    value = min_b + ((value - max_b) % (max_b - min_b))
                result.append(value)
            
            elif self.config.boundary_handling == BoundaryHandling.RANDOM:
                if value < min_b or value > max_b:
                    result.append(random.uniform(min_b, max_b))
                else:
                    result.append(value)
            
            else:
                result.append(max(min_b, min(max_b, value)))
        
        return result
    
    def _clamp_velocity(self, velocity: List[float]) -> List[float]:
        """限制速度"""
        if self.config.velocity_clamp is None:
            return velocity
        
        max_vel = self.config.velocity_clamp
        return [max(-max_vel, min(max_vel, v)) for v in velocity]
    
    def _update_particle(self, particle: Particle, inertia_weight: float):
        """更新单个粒子"""
        r1 = [random.random() for _ in range(self.dimensions)]
        r2 = [random.random() for _ in range(self.dimensions)]
        
        new_velocity = []
        for d in range(self.dimensions):
            # PSO 速度更新公式
            # v = w*v + c1*r1*(pbest - x) + c2*r2*(gbest - x)
            v = (inertia_weight * particle.velocity[d] +
                 self.config.cognitive_coeff * r1[d] * 
                 (particle.best_position[d] - particle.position[d]) +
                 self.config.social_coeff * r2[d] * 
                 (self.global_best_position[d] - particle.position[d]))
            new_velocity.append(v)
        
        # 限制速度
        particle.velocity = self._clamp_velocity(new_velocity)
        
        # 更新位置
        new_position = [
            particle.position[d] + particle.velocity[d]
            for d in range(self.dimensions)
        ]
        
        # 应用边界约束
        particle.position = self._apply_boundary(new_position)
        
        # 评估新位置的适应度
        particle.current_fitness = self._evaluate_fitness(particle.position)
        
        # 更新个体最优
        if particle.current_fitness < particle.best_fitness:
            particle.best_fitness = particle.current_fitness
            particle.best_position = copy.copy(particle.position)
    
    def _update_global_best(self):
        """更新全局最优"""
        for particle in self.swarm:
            if particle.best_fitness < self.global_best_fitness:
                self.global_best_fitness = particle.best_fitness
                self.global_best_position = copy.copy(particle.best_position)
    
    def _check_early_stop(self) -> bool:
        """检查是否满足早停条件"""
        if len(self.convergence_history) < self.config.early_stop_patience:
            return False
        
        recent = self.convergence_history[-self.config.early_stop_patience:]
        improvement = abs(recent[-1] - recent[0])
        
        return improvement < self.config.early_stop_threshold
    
    def optimize(self, verbose: bool = False) -> OptimizationResult:
        """
        执行优化
        
        Args:
            verbose: 是否打印进度信息
        
        Returns:
            OptimizationResult: 优化结果
        """
        # 初始化
        self._initialize_swarm()
        self.convergence_history = []
        self.iteration = 0
        
        # 初始评估
        for particle in self.swarm:
            particle.current_fitness = self._evaluate_fitness(particle.position)
            particle.best_fitness = particle.current_fitness
            particle.best_position = copy.copy(particle.position)
        
        # 初始化全局最优
        best_particle = min(self.swarm, key=lambda p: p.best_fitness)
        self.global_best_position = copy.copy(best_particle.best_position)
        self.global_best_fitness = best_particle.best_fitness
        self.convergence_history.append(self.global_best_fitness)
        
        if verbose:
            print(f"迭代 0: 最优适应度 = {self.global_best_fitness:.6e}")
        
        # 主循环
        for self.iteration in range(1, self.config.max_iterations + 1):
            # 计算当前惯性权重
            inertia_weight = self._update_inertia_weight()
            
            # 更新每个粒子
            for particle in self.swarm:
                self._update_particle(particle, inertia_weight)
            
            # 更新全局最优
            self._update_global_best()
            self.convergence_history.append(self.global_best_fitness)
            
            if verbose and self.iteration % 10 == 0:
                print(f"迭代 {self.iteration}: 最优适应度 = {self.global_best_fitness:.6e}")
            
            # 检查早停
            if self._check_early_stop():
                if verbose:
                    print(f"早停于迭代 {self.iteration}")
                break
        
        # 构建结果
        result = OptimizationResult(
            best_position=self.global_best_position,
            best_fitness=self.global_best_fitness if self.minimize else -self.global_best_fitness,
            convergence_history=self.convergence_history,
            iteration_count=self.iteration,
            swarm=copy.deepcopy(self.swarm),
            metadata={
                'config': self.config.__dict__,
                'dimensions': self.dimensions,
                'final_inertia_weight': self._update_inertia_weight() if self.iteration > 0 else self.config.inertia_weight
            }
        )
        
        return result


# ============================================================
# 便捷函数
# ============================================================

def optimize(
    objective_func: Callable[[List[float]], float],
    bounds: List[Tuple[float, float]],
    swarm_size: int = 30,
    max_iterations: int = 100,
    minimize: bool = True,
    **kwargs
) -> OptimizationResult:
    """
    快速优化函数
    
    Args:
        objective_func: 目标函数
        bounds: 每个维度的边界
        swarm_size: 粒子数量
        max_iterations: 最大迭代次数
        minimize: 是否最小化
        **kwargs: 其他 PSOConfig 参数
    
    Returns:
        OptimizationResult: 优化结果
    
    使用示例：
    >>> def sphere(x):
    ...     return sum(xi**2 for xi in x)
    >>> result = optimize(sphere, [(-5, 5)] * 5, swarm_size=20, max_iterations=50)
    >>> print(f"最优值: {result.best_fitness:.6f}")
    """
    config = PSOConfig(
        swarm_size=swarm_size,
        max_iterations=max_iterations,
        **kwargs
    )
    optimizer = ParticleSwarmOptimizer(
        objective_func=objective_func,
        bounds=bounds,
        config=config,
        minimize=minimize
    )
    return optimizer.optimize()


def optimize_with_constraints(
    objective_func: Callable[[List[float]], float],
    bounds: List[Tuple[float, float]],
    constraints: List[Callable[[List[float]], bool]],
    penalty_factor: float = 1e6,
    **kwargs
) -> OptimizationResult:
    """
    带约束的优化
    
    Args:
        objective_func: 目标函数
        bounds: 边界
        constraints: 约束函数列表，每个函数返回 True 表示满足约束
        penalty_factor: 违反约束的惩罚因子
        **kwargs: 其他参数
    
    Returns:
        OptimizationResult: 优化结果
    """
    def penalized_objective(x):
        fitness = objective_func(x)
        for constraint in constraints:
            if not constraint(x):
                fitness += penalty_factor
        return fitness
    
    return optimize(penalized_objective, bounds, **kwargs)


def multi_objective_pareto(
    objective_funcs: List[Callable[[List[float]], float]],
    bounds: List[Tuple[float, float]],
    swarm_size: int = 100,
    max_iterations: int = 200,
    **kwargs
) -> List[OptimizationResult]:
    """
    多目标优化的简单 Pareto 前沿搜索
    
    Args:
        objective_funcs: 多个目标函数列表
        bounds: 边界
        swarm_size: 粒子数量
        max_iterations: 最大迭代次数
        **kwargs: 其他参数
    
    Returns:
        List[OptimizationResult]: Pareto 前沿上的解
    """
    # 为每个目标函数运行独立优化
    results = []
    for i, obj_func in enumerate(objective_funcs):
        result = optimize(
            obj_func, bounds,
            swarm_size=swarm_size,
            max_iterations=max_iterations,
            seed=kwargs.get('seed', 42) + i if kwargs.get('seed') else None,
            **{k: v for k, v in kwargs.items() if k != 'seed'}
        )
        results.append(result)
    
    return results


# ============================================================
# 经典测试函数
# ============================================================

def sphere(x: List[float]) -> float:
    """Sphere 函数 - 简单凸函数"""
    return sum(xi ** 2 for xi in x)


def rastrigin(x: List[float]) -> float:
    """Rastrigin 函数 - 多峰函数"""
    A = 10
    n = len(x)
    return A * n + sum(xi ** 2 - A * math.cos(2 * math.pi * xi) for xi in x)


def rosenbrock(x: List[float]) -> float:
    """Rosenbrock 函数 - 香蕉函数"""
    return sum(
        100 * (x[i + 1] - x[i] ** 2) ** 2 + (1 - x[i]) ** 2
        for i in range(len(x) - 1)
    )


def ackley(x: List[float]) -> float:
    """Ackley 函数 - 复杂多峰函数"""
    n = len(x)
    sum1 = sum(xi ** 2 for xi in x)
    sum2 = sum(math.cos(2 * math.pi * xi) for xi in x)
    
    return (-20 * math.exp(-0.2 * math.sqrt(sum1 / n)) -
            math.exp(sum2 / n) + 20 + math.e)


def griewank(x: List[float]) -> float:
    """Griewank 函数"""
    sum_part = sum(xi ** 2 for xi in x) / 4000
    # 手动计算乘积（兼容 Python 3.7）
    prod_part = 1.0
    for i, xi in enumerate(x):
        prod_part *= math.cos(xi / math.sqrt(i + 1))
    return sum_part - prod_part + 1


def schwefel(x: List[float]) -> float:
    """Schwefel 函数"""
    n = len(x)
    return 418.9829 * n - sum(xi * math.sin(math.sqrt(abs(xi))) for xi in x)


def levy(x: List[float]) -> float:
    """Levy 函数"""
    w = [1 + (xi - 1) / 4 for xi in x]
    
    term1 = math.sin(math.pi * w[0]) ** 2
    term3 = (w[-1] - 1) ** 2 * (1 + math.sin(2 * math.pi * w[-1]) ** 2)
    
    term2 = sum(
        (wi - 1) ** 2 * (1 + 10 * math.sin(math.pi * wi + 1) ** 2)
        for wi in w[:-1]
    )
    
    return term1 + term2 + term3


# ============================================================
# 辅助函数
# ============================================================

def calculate_convergence_rate(history: List[float]) -> float:
    """
    计算收敛速率
    
    Args:
        history: 收敛历史
    
    Returns:
        float: 平均每代改进率
    """
    if len(history) < 2:
        return 0.0
    
    improvements = []
    for i in range(1, len(history)):
        if history[i-1] != 0:
            improvements.append(abs(history[i] - history[i-1]) / abs(history[i-1]))
    
    return sum(improvements) / len(improvements) if improvements else 0.0


def calculate_diversity(swarm: List[Particle]) -> float:
    """
    计算粒子群多样性
    
    Args:
        swarm: 粒子群
    
    Returns:
        float: 多样性指标
    """
    if not swarm:
        return 0.0
    
    n = len(swarm)
    dim = len(swarm[0].position)
    
    # 计算平均位置
    mean_pos = [
        sum(p.position[d] for p in swarm) / n
        for d in range(dim)
    ]
    
    # 计算平均距离
    avg_dist = sum(
        math.sqrt(sum((p.position[d] - mean_pos[d]) ** 2 for d in range(dim)))
        for p in swarm
    ) / n
    
    return avg_dist


def get_best_solutions(result: OptimizationResult, top_k: int = 5) -> List[Tuple[List[float], float]]:
    """
    获取最优的 k 个解
    
    Args:
        result: 优化结果
        top_k: 数量
    
    Returns:
        List of (position, fitness) tuples
    """
    sorted_particles = sorted(result.swarm, key=lambda p: p.best_fitness)
    return [(p.best_position, p.best_fitness) for p in sorted_particles[:top_k]]


# ============================================================
# 模块信息
# ============================================================

__version__ = "1.0.0"
__author__ = "AllToolkit"

__all__ = [
    # 类
    'ParticleSwarmOptimizer',
    'Particle',
    'PSOConfig',
    'OptimizationResult',
    'InertiaWeightStrategy',
    'BoundaryHandling',
    
    # 函数
    'optimize',
    'optimize_with_constraints',
    'multi_objective_pareto',
    'calculate_convergence_rate',
    'calculate_diversity',
    'get_best_solutions',
    
    # 测试函数
    'sphere',
    'rastrigin',
    'rosenbrock',
    'ackley',
    'griewank',
    'schwefel',
    'levy',
]
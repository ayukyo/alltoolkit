"""
Hungarian Algorithm Utils - 解决分配问题的最优算法

匈牙利算法（Hungarian Algorithm），又称 Munkres 算法，用于解决分配问题：
- 给定 n 个工人和 n 个任务
- 每个工人完成每个任务有一个成本
- 目标：找到使总成本最小的分配方案

时间复杂度: O(n³)
空间复杂度: O(n²)

应用场景：
- 任务分配
- 资源调度
- 匹配问题
- 工作排班
- 目标跟踪
"""

from typing import List, Tuple, Optional


class HungarianAlgorithm:
    """匈牙利算法实现类 - 使用简化的 Kuhn-Munkres 算法"""
    
    def __init__(self, cost_matrix: List[List[float]]):
        """
        初始化匈牙利算法
        
        Args:
            cost_matrix: n×n 成本矩阵，cost_matrix[i][j] 表示工人 i 完成任务 j 的成本
        """
        if not cost_matrix or not cost_matrix[0]:
            raise ValueError("成本矩阵不能为空")
        
        self.original_matrix = [row[:] for row in cost_matrix]
        self.n = len(cost_matrix)
        
        # 检查是否为方阵
        for row in cost_matrix:
            if len(row) != self.n:
                raise ValueError("成本矩阵必须是方阵")
        
        # 结果
        self._result: Optional[List[Tuple[int, int]]] = None
        self._total_cost: Optional[float] = None
    
    def solve(self) -> List[Tuple[int, int]]:
        """
        求解分配问题
        
        Returns:
            分配方案列表，每个元素为 (工人索引, 任务索引) 元组
        """
        n = self.n
        INF = float('inf')
        
        # 复制成本矩阵
        cost = [row[:] for row in self.original_matrix]
        
        # 工人和任务的势值
        u = [0] * (n + 1)
        v = [0] * (n + 1)
        
        # 匹配结果: p[j] = i 表示任务 j 分配给工人 i
        p = [0] * (n + 1)
        
        # 辅助数组
        way = [0] * (n + 1)
        minv = [INF] * (n + 1)
        used = [False] * (n + 1)
        
        # Kuhn-Munkres 算法
        for i in range(1, n + 1):
            p[0] = i
            j0 = 0
            
            for k in range(n + 1):
                minv[k] = INF
                used[k] = False
            
            while True:
                used[j0] = True
                i0 = p[j0]
                delta = INF
                j1 = 0
                
                for j in range(1, n + 1):
                    if not used[j]:
                        cur = cost[i0 - 1][j - 1] - u[i0] - v[j]
                        if cur < minv[j]:
                            minv[j] = cur
                            way[j] = j0
                        if minv[j] < delta:
                            delta = minv[j]
                            j1 = j
                
                for j in range(n + 1):
                    if used[j]:
                        u[p[j]] += delta
                        v[j] -= delta
                    else:
                        minv[j] -= delta
                
                j0 = j1
                
                if p[j0] == 0:
                    break
            
            # 增广路径
            while True:
                j1 = way[j0]
                p[j0] = p[j1]
                j0 = j1
                if j0 == 0:
                    break
        
        # 构建结果
        self._result = []
        self._total_cost = 0
        
        for j in range(1, n + 1):
            if p[j] != 0:
                worker = p[j] - 1
                task = j - 1
                self._result.append((worker, task))
                self._total_cost += self.original_matrix[worker][task]
        
        return self._result
    
    def get_total_cost(self) -> float:
        """
        获取最优分配的总成本
        
        Returns:
            总成本
        """
        if self._total_cost is None:
            raise RuntimeError("请先调用 solve() 方法")
        return self._total_cost
    
    def get_assignment_matrix(self) -> List[List[int]]:
        """
        获取分配矩阵
        
        Returns:
            n×n 分配矩阵，1 表示分配，0 表示未分配
        """
        if self._result is None:
            raise RuntimeError("请先调用 solve() 方法")
        
        result = [[0] * self.n for _ in range(self.n)]
        for i, j in self._result:
            result[i][j] = 1
        return result


def hungarian(cost_matrix: List[List[float]]) -> Tuple[List[Tuple[int, int]], float]:
    """
    使用匈牙利算法求解分配问题（便捷函数）
    
    Args:
        cost_matrix: n×n 成本矩阵
    
    Returns:
        (分配方案, 总成本) 元组
        分配方案是 [(工人索引, 任务索引), ...] 列表
    
    Example:
        >>> costs = [[4, 1, 3], [2, 0, 5], [3, 2, 2]]
        >>> assignment, total = hungarian(costs)
        >>> print(assignment)  # [(0, 1), (1, 0), (2, 2)]
        >>> print(total)  # 5.0
    """
    solver = HungarianAlgorithm(cost_matrix)
    assignment = solver.solve()
    total_cost = solver.get_total_cost()
    return assignment, total_cost


def solve_assignment(cost_matrix: List[List[float]]) -> List[Tuple[int, int]]:
    """
    求解分配问题，返回分配方案
    
    Args:
        cost_matrix: n×n 成本矩阵
    
    Returns:
        分配方案列表 [(工人索引, 任务索引), ...]
    
    Example:
        >>> costs = [[10, 19, 8, 15], [10, 18, 7, 17], 
        ...          [13, 16, 9, 14], [12, 19, 8, 11]]
        >>> assignment = solve_assignment(costs)
    """
    solver = HungarianAlgorithm(cost_matrix)
    return solver.solve()


def max_weight_matching(weight_matrix: List[List[float]]) -> Tuple[List[Tuple[int, int]], float]:
    """
    求解最大权重匹配问题
    
    将权重取负转换为成本，然后用匈牙利算法求解
    
    Args:
        weight_matrix: n×n 权重矩阵
    
    Returns:
        (匹配方案, 总权重) 元组
    """
    n = len(weight_matrix)
    # 找最大值用于转换
    max_weight = max(max(row) for row in weight_matrix)
    # 转换为成本（越大越好 -> 成本越小越好）
    cost_matrix = [[max_weight - weight_matrix[i][j] for j in range(n)] for i in range(n)]
    
    assignment, total_cost = hungarian(cost_matrix)
    # 转回权重
    total_weight = n * max_weight - total_cost
    
    return assignment, total_weight


def rectangular_assignment(cost_matrix: List[List[float]]) -> List[Tuple[int, int]]:
    """
    处理非方阵的分配问题（工人数 ≠ 任务数）
    
    如果工人少于任务：添加虚拟工人（成本为大值）
    如果任务少于工人：添加虚拟任务（成本为大值）
    
    Args:
        cost_matrix: m×n 成本矩阵（不一定是方阵）
    
    Returns:
        分配方案列表 [(工人索引, 任务索引), ...]
             只返回真实工人和真实任务的分配
    """
    if not cost_matrix or not cost_matrix[0]:
        return []
    
    m = len(cost_matrix)
    n = len(cost_matrix[0])
    
    if m == n:
        return solve_assignment(cost_matrix)
    
    # 找最大成本
    max_cost = max(max(row) for row in cost_matrix)
    fill_cost = abs(max_cost) * max(m, n) + 1
    
    # 构造方阵
    size = max(m, n)
    square_matrix = [[fill_cost] * size for _ in range(size)]
    
    for i in range(m):
        for j in range(n):
            square_matrix[i][j] = cost_matrix[i][j]
    
    assignment, _ = hungarian(square_matrix)
    
    # 过滤掉虚拟分配
    return [(i, j) for i, j in assignment if i < m and j < n]


class AssignmentProblem:
    """
    分配问题辅助类
    
    提供更友好的 API 来构建和求解分配问题
    """
    
    def __init__(self):
        self.workers: List[str] = []
        self.tasks: List[str] = []
        self.costs: List[List[float]] = []
    
    def add_worker(self, name: str) -> 'AssignmentProblem':
        """添加工人"""
        self.workers.append(name)
        return self
    
    def add_task(self, name: str) -> 'AssignmentProblem':
        """添加任务"""
        self.tasks.append(name)
        return self
    
    def set_cost(self, worker_idx: int, task_idx: int, cost: float) -> 'AssignmentProblem':
        """设置工人完成任务的成 本"""
        # 确保成本矩阵足够大
        while len(self.costs) <= worker_idx:
            self.costs.append([])
        while len(self.costs[worker_idx]) <= task_idx:
            self.costs[worker_idx].append(0)
        self.costs[worker_idx][task_idx] = cost
        return self
    
    def solve(self) -> List[Tuple[str, str, float]]:
        """
        求解分配问题
        
        Returns:
            [(工人名称, 任务名称, 成本), ...] 列表
        """
        if not self.costs:
            return []
        
        assignment = rectangular_assignment(self.costs)
        
        result = []
        for worker_idx, task_idx in assignment:
            if worker_idx < len(self.workers) and task_idx < len(self.tasks):
                cost = self.costs[worker_idx][task_idx] if worker_idx < len(self.costs) and task_idx < len(self.costs[worker_idx]) else 0
                result.append((self.workers[worker_idx], self.tasks[task_idx], cost))
        
        return result


# 导出接口
__all__ = [
    'HungarianAlgorithm',
    'hungarian',
    'solve_assignment',
    'max_weight_matching',
    'rectangular_assignment',
    'AssignmentProblem',
]
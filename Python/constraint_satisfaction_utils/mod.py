"""
约束满足问题工具模块 (Constraint Satisfaction Utilities)

提供约束满足问题（CSP）的求解工具，包括：
- 变量和域定义
- 约束定义（一元、二元、全局约束）
- 回溯搜索算法
- 前向检查
- 约束传播（AC-3）
- 变量选择启发式（MRV、度启发式）
- 值选择启发式（最少约束值）

应用场景：
- 调度问题
- 配置问题
- 资源分配
- N皇后问题
- 图着色
- 数独求解

零外部依赖，纯 Python 实现。

作者: AllToolkit
日期: 2026-05-17
"""

from typing import Dict, List, Set, Tuple, Optional, Any, Callable, Generic, TypeVar
from dataclasses import dataclass, field
from copy import deepcopy
from collections import defaultdict

T = TypeVar('T')  # 变量类型
V = TypeVar('V')  # 值类型


@dataclass
class Constraint(Generic[T, V]):
    """
    约束基类
    
    表示变量之间的约束关系。
    """
    variables: List[T]
    
    def is_satisfied(self, assignment: Dict[T, V]) -> bool:
        """
        检查约束是否满足
        
        Args:
            assignment: 变量赋值字典
        
        Returns:
            约束是否满足
        """
        raise NotImplementedError
    
    def get_conflicts(self, assignment: Dict[T, V]) -> List[Tuple[T, T]]:
        """
        获取冲突的变量对
        
        Args:
            assignment: 变量赋值字典
        
        Returns:
            冲突的变量对列表
        """
        return []


class UnaryConstraint(Constraint[T, V]):
    """一元约束：对单个变量的约束"""
    
    def __init__(self, variable: T, predicate: Callable[[V], bool]):
        super().__init__([variable])
        self.variable = variable
        self.predicate = predicate
    
    def is_satisfied(self, assignment: Dict[T, V]) -> bool:
        if self.variable not in assignment:
            return True
        return self.predicate(assignment[self.variable])


class BinaryConstraint(Constraint[T, V]):
    """二元约束：两个变量之间的约束"""
    
    def __init__(self, var1: T, var2: T, predicate: Callable[[V, V], bool]):
        super().__init__([var1, var2])
        self.var1 = var1
        self.var2 = var2
        self.predicate = predicate
    
    def is_satisfied(self, assignment: Dict[T, V]) -> bool:
        if self.var1 not in assignment or self.var2 not in assignment:
            return True
        return self.predicate(assignment[self.var1], assignment[self.var2])
    
    def get_conflicts(self, assignment: Dict[T, V]) -> List[Tuple[T, T]]:
        if self.var1 in assignment and self.var2 in assignment:
            if not self.predicate(assignment[self.var1], assignment[self.var2]):
                return [(self.var1, self.var2)]
        return []


class AllDifferentConstraint(Constraint[T, V]):
    """全局约束：所有变量取值不同"""
    
    def __init__(self, variables: List[T]):
        super().__init__(variables)
    
    def is_satisfied(self, assignment: Dict[T, V]) -> bool:
        assigned_values = [assignment[v] for v in self.variables if v in assignment]
        return len(assigned_values) == len(set(assigned_values))
    
    def get_conflicts(self, assignment: Dict[T, V]) -> List[Tuple[T, T]]:
        conflicts = []
        value_to_vars = defaultdict(list)
        for v in self.variables:
            if v in assignment:
                value_to_vars[assignment[v]].append(v)
        
        for val, vars_with_val in value_to_vars.items():
            if len(vars_with_val) > 1:
                for i in range(len(vars_with_val)):
                    for j in range(i + 1, len(vars_with_val)):
                        conflicts.append((vars_with_val[i], vars_with_val[j]))
        return conflicts


class AllEqualConstraint(Constraint[T, V]):
    """全局约束：所有变量取值相同"""
    
    def __init__(self, variables: List[T]):
        super().__init__(variables)
    
    def is_satisfied(self, assignment: Dict[T, V]) -> bool:
        assigned_values = [assignment[v] for v in self.variables if v in assignment]
        if not assigned_values:
            return True
        return len(set(assigned_values)) == 1


class SumConstraint(Constraint[T, V]):
    """全局约束：变量值之和等于目标值"""
    
    def __init__(self, variables: List[T], target: int):
        super().__init__(variables)
        self.target = target
    
    def is_satisfied(self, assignment: Dict[T, V]) -> bool:
        assigned_sum = sum(assignment[v] for v in self.variables if v in assignment)
        unassigned_count = sum(1 for v in self.variables if v not in assignment)
        
        # 如果全部已赋值，检查总和
        if unassigned_count == 0:
            return assigned_sum == self.target
        
        # 如果部分未赋值，暂时认为满足
        return True


class MaxValueConstraint(Constraint[T, V]):
    """全局约束：最大值约束"""
    
    def __init__(self, variables: List[T], max_value: V):
        super().__init__(variables)
        self.max_value = max_value
    
    def is_satisfied(self, assignment: Dict[T, V]) -> bool:
        for v in self.variables:
            if v in assignment and assignment[v] > self.max_value:
                return False
        return True


@dataclass
class CSP(Generic[T, V]):
    """
    约束满足问题（CSP）
    
    属性:
        variables: 变量列表
        domains: 每个变量的取值域
        constraints: 约束列表
    """
    variables: List[T]
    domains: Dict[T, List[V]]
    constraints: List[Constraint[T, V]] = field(default_factory=list)
    
    # 用于快速查找变量相关的约束
    _constraints_map: Dict[T, List[Constraint[T, V]]] = field(default_factory=dict, repr=False)
    
    def __post_init__(self):
        self._build_constraints_map()
    
    def _build_constraints_map(self):
        """构建变量到约束的映射"""
        self._constraints_map = defaultdict(list)
        for constraint in self.constraints:
            for var in constraint.variables:
                self._constraints_map[var].append(constraint)
    
    def add_constraint(self, constraint: Constraint[T, V]):
        """添加约束"""
        self.constraints.append(constraint)
        for var in constraint.variables:
            self._constraints_map[var].append(constraint)
    
    def get_constraints(self, variable: T) -> List[Constraint[T, V]]:
        """获取与变量相关的所有约束"""
        return self._constraints_map.get(variable, [])
    
    def is_consistent(self, variable: T, value: V, assignment: Dict[T, V]) -> bool:
        """
        检查赋值是否与约束一致
        
        Args:
            variable: 待赋值变量
            value: 值
            assignment: 当前赋值
        
        Returns:
            是否一致
        """
        # 创建临时赋值
        temp_assignment = assignment.copy()
        temp_assignment[variable] = value
        
        # 检查所有相关约束
        for constraint in self.get_constraints(variable):
            if not constraint.is_satisfied(temp_assignment):
                return False
        return True
    
    def get_conflicts(self, assignment: Dict[T, V]) -> List[Tuple[T, T]]:
        """获取当前赋值中的所有冲突"""
        conflicts = []
        for constraint in self.constraints:
            conflicts.extend(constraint.get_conflicts(assignment))
        return conflicts


class CSPSolver(Generic[T, V]):
    """
    CSP 求解器
    
    支持多种求解策略：
    - 简单回溯
    - 前向检查
    - 约束传播（AC-3）
    - 各种启发式
    """
    
    def __init__(
        self,
        csp: CSP[T, V],
        var_heuristic: str = 'mrv',
        value_heuristic: str = 'lcv',
        inference: str = 'forward_checking'
    ):
        """
        初始化求解器
        
        Args:
            csp: 约束满足问题
            var_heuristic: 变量选择启发式 ('none', 'mrv', 'degree', 'mrv_degree')
            value_heuristic: 值选择启发式 ('none', 'lcv')
            inference: 推理方法 ('none', 'forward_checking', 'ac3')
        """
        self.csp = csp
        self.var_heuristic = var_heuristic
        self.value_heuristic = value_heuristic
        self.inference = inference
        self.nodes_explored = 0
        self.backtracks = 0
    
    def solve(self) -> Optional[Dict[T, V]]:
        """
        求解 CSP
        
        Returns:
            解决方案（变量赋值），如果无解则返回 None
        """
        self.nodes_explored = 0
        self.backtracks = 0
        assignment = {}
        domains = {var: list(self.csp.domains[var]) for var in self.csp.variables}
        return self._backtrack(assignment, domains)
    
    def _backtrack(
        self,
        assignment: Dict[T, V],
        domains: Dict[T, List[V]]
    ) -> Optional[Dict[T, V]]:
        """回溯搜索"""
        self.nodes_explored += 1
        
        # 检查是否完成
        if len(assignment) == len(self.csp.variables):
            return assignment
        
        # 选择变量
        var = self._select_unassigned_variable(assignment, domains)
        
        # 按顺序尝试值
        for value in self._order_domain_values(var, assignment, domains):
            if self.csp.is_consistent(var, value, assignment):
                assignment[var] = value
                
                # 保存域副本
                old_domains = {v: list(d) for v, d in domains.items()}
                
                # 推理
                if self._inference(var, value, assignment, domains):
                    result = self._backtrack(assignment, domains)
                    if result is not None:
                        return result
                
                # 回溯
                del assignment[var]
                domains = old_domains
                self.backtracks += 1
        
        return None
    
    def _select_unassigned_variable(
        self,
        assignment: Dict[T, V],
        domains: Dict[T, List[V]]
    ) -> T:
        """选择下一个未赋值变量"""
        unassigned = [v for v in self.csp.variables if v not in assignment]
        
        if self.var_heuristic == 'none':
            return unassigned[0]
        
        if self.var_heuristic == 'mrv':
            # 最小剩余值：选择域最小的变量
            return min(unassigned, key=lambda v: len(domains[v]))
        
        if self.var_heuristic == 'degree':
            # 度启发式：选择约束最多的变量
            return max(unassigned, key=lambda v: len(self.csp.get_constraints(v)))
        
        if self.var_heuristic == 'mrv_degree':
            # MRV + 度启发式：先用 MRV，再用度打破平局
            min_domain_size = min(len(domains[v]) for v in unassigned)
            mrv_vars = [v for v in unassigned if len(domains[v]) == min_domain_size]
            if len(mrv_vars) == 1:
                return mrv_vars[0]
            return max(mrv_vars, key=lambda v: len(self.csp.get_constraints(v)))
        
        return unassigned[0]
    
    def _order_domain_values(
        self,
        var: T,
        assignment: Dict[T, V],
        domains: Dict[T, List[V]]
    ) -> List[V]:
        """排序变量的取值域"""
        if self.value_heuristic == 'none':
            return domains[var]
        
        if self.value_heuristic == 'lcv':
            # 最少约束值：选择对其他变量影响最小的值
            return sorted(domains[var], key=lambda v: self._count_conflicts(var, v, assignment))
        
        return domains[var]
    
    def _count_conflicts(self, var: T, value: V, assignment: Dict[T, V]) -> int:
        """计算赋值对其他变量的影响"""
        count = 0
        temp_assignment = assignment.copy()
        temp_assignment[var] = value
        
        for constraint in self.csp.get_constraints(var):
            for other_var in constraint.variables:
                if other_var != var and other_var not in assignment:
                    # 检查其他变量的每个可能值是否被排除
                    if constraint.is_satisfied(temp_assignment):
                        pass
                    else:
                        count += 1
        
        return count
    
    def _inference(
        self,
        var: T,
        value: V,
        assignment: Dict[T, V],
        domains: Dict[T, List[V]]
    ) -> bool:
        """执行推理"""
        if self.inference == 'none':
            return True
        
        if self.inference == 'forward_checking':
            return self._forward_checking(var, value, assignment, domains)
        
        if self.inference == 'ac3':
            return self._ac3(domains, [(var, other) for other in self.csp.variables if other != var])
        
        return True
    
    def _forward_checking(
        self,
        var: T,
        value: V,
        assignment: Dict[T, V],
        domains: Dict[T, List[V]]
    ) -> bool:
        """前向检查"""
        for constraint in self.csp.get_constraints(var):
            for other_var in constraint.variables:
                if other_var != var and other_var not in assignment:
                    # 检查其他变量的每个可能值
                    to_remove = []
                    for other_value in domains[other_var]:
                        temp_assignment = assignment.copy()
                        temp_assignment[var] = value
                        temp_assignment[other_var] = other_value
                        
                        if not constraint.is_satisfied(temp_assignment):
                            to_remove.append(other_value)
                    
                    # 移除不一致的值
                    for v in to_remove:
                        domains[other_var].remove(v)
                    
                    # 如果域为空，失败
                    if not domains[other_var]:
                        return False
        
        return True
    
    def _ac3(
        self,
        domains: Dict[T, List[V]],
        initial_queue: Optional[List[Tuple[T, T]]] = None
    ) -> bool:
        """AC-3 算法（弧一致性）"""
        # 初始化队列
        queue = []
        if initial_queue:
            queue = list(initial_queue)
        else:
            for var1 in self.csp.variables:
                for var2 in self.csp.variables:
                    if var1 != var2:
                        queue.append((var1, var2))
        
        while queue:
            xi, xj = queue.pop(0)
            
            if self._revise(domains, xi, xj):
                if not domains[xi]:
                    return False
                
                # 添加新的弧到队列
                for xk in self.csp.variables:
                    if xk != xi and xk != xj:
                        queue.append((xk, xi))
        
        return True
    
    def _revise(self, domains: Dict[T, List[V]], xi: T, xj: T) -> bool:
        """检查并移除不一致的值"""
        revised = False
        
        # 找到连接 xi 和 xj 的约束
        constraints = []
        for c in self.csp.get_constraints(xi):
            if xj in c.variables:
                constraints.append(c)
        
        if not constraints:
            return False
        
        to_remove = []
        for vi in domains[xi]:
            # 检查是否存在使所有约束满足的 vj
            has_support = False
            for vj in domains[xj]:
                satisfies_all = True
                for c in constraints:
                    if not c.is_satisfied({xi: vi, xj: vj}):
                        satisfies_all = False
                        break
                if satisfies_all:
                    has_support = True
                    break
            
            if not has_support:
                to_remove.append(vi)
                revised = True
        
        for v in to_remove:
            domains[xi].remove(v)
        
        return revised
    
    def find_all_solutions(self, max_solutions: int = 100) -> List[Dict[T, V]]:
        """
        找到所有解
        
        Args:
            max_solutions: 最大解数量
        
        Returns:
            所有解的列表
        """
        self.nodes_explored = 0
        self.backtracks = 0
        solutions = []
        assignment = {}
        domains = {var: list(self.csp.domains[var]) for var in self.csp.variables}
        self._backtrack_all(assignment, domains, solutions, max_solutions)
        return solutions
    
    def _backtrack_all(
        self,
        assignment: Dict[T, V],
        domains: Dict[T, List[V]],
        solutions: List[Dict[T, V]],
        max_solutions: int
    ):
        """回溯搜索所有解"""
        if len(solutions) >= max_solutions:
            return
        
        self.nodes_explored += 1
        
        if len(assignment) == len(self.csp.variables):
            solutions.append(assignment.copy())
            return
        
        var = self._select_unassigned_variable(assignment, domains)
        
        for value in self._order_domain_values(var, assignment, domains):
            if self.csp.is_consistent(var, value, assignment):
                assignment[var] = value
                old_domains = {v: list(d) for v, d in domains.items()}
                
                if self._inference(var, value, assignment, domains):
                    self._backtrack_all(assignment, domains, solutions, max_solutions)
                
                del assignment[var]
                domains = old_domains
                self.backtracks += 1


# =============================================================================
# 预定义问题
# =============================================================================

def create_n_queens_csp(n: int) -> CSP[int, int]:
    """
    创建 N 皇后问题 CSP
    
    Args:
        n: 棋盘大小
    
    Returns:
        CSP 模型
    """
    variables = list(range(n))
    domains = {var: list(range(n)) for var in variables}
    
    constraints = []
    
    # 所有皇后在不同行（变量本身保证）
    # 所有皇后在不同列（AllDifferentConstraint）
    constraints.append(AllDifferentConstraint(variables))
    
    # 所有皇后在不同对角线
    for i in range(n):
        for j in range(i + 1, n):
            # |row_i - row_j| != |col_i - col_j|
            constraints.append(BinaryConstraint(
                i, j,
                lambda ri, rj, i=i, j=j: abs(ri - rj) != abs(i - j)
            ))
    
    return CSP(variables, domains, constraints)


def create_sudoku_csp(grid: List[List[int]]) -> CSP[Tuple[int, int], int]:
    """
    创建数独问题 CSP
    
    Args:
        grid: 9x9 数独网格，0 表示空格
    
    Returns:
        CSP 模型
    """
    variables = [(i, j) for i in range(9) for j in range(9)]
    
    # 构建域
    domains = {}
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                domains[(i, j)] = list(range(1, 10))
            else:
                domains[(i, j)] = [grid[i][j]]
    
    constraints = []
    
    # 行约束
    for i in range(9):
        row_vars = [(i, j) for j in range(9)]
        constraints.append(AllDifferentConstraint(row_vars))
    
    # 列约束
    for j in range(9):
        col_vars = [(i, j) for i in range(9)]
        constraints.append(AllDifferentConstraint(col_vars))
    
    # 3x3 宫格约束
    for box_i in range(3):
        for box_j in range(3):
            box_vars = []
            for i in range(3):
                for j in range(3):
                    box_vars.append((box_i * 3 + i, box_j * 3 + j))
            constraints.append(AllDifferentConstraint(box_vars))
    
    return CSP(variables, domains, constraints)


def create_graph_coloring_csp(
    vertices: List[T],
    edges: List[Tuple[T, T]],
    colors: List[V]
) -> CSP[T, V]:
    """
    创建图着色问题 CSP
    
    Args:
        vertices: 顶点列表
        edges: 边列表
        colors: 颜色列表
    
    Returns:
        CSP 模型
    """
    domains = {v: list(colors) for v in vertices}
    
    constraints = []
    for (v1, v2) in edges:
        constraints.append(BinaryConstraint(v1, v2, lambda c1, c2: c1 != c2))
    
    return CSP(vertices, domains, constraints)


def create_scheduling_csp(
    tasks: List[T],
    resources: List[V],
    constraints_list: List[Tuple[T, T]]
) -> CSP[T, V]:
    """
    创建调度问题 CSP
    
    Args:
        tasks: 任务列表
        resources: 资源列表
        constraints_list: 不能同时执行的任务对
    
    Returns:
        CSP 模型
    """
    domains = {task: list(resources) for task in tasks}
    
    constraints = []
    for (t1, t2) in constraints_list:
        constraints.append(BinaryConstraint(t1, t2, lambda r1, r2: r1 != r2))
    
    return CSP(tasks, domains, constraints)


# =============================================================================
# 便捷函数
# =============================================================================

def solve_n_queens(n: int, inference: str = 'ac3') -> Optional[Dict[int, int]]:
    """
    求解 N 皇后问题
    
    Args:
        n: 棋盘大小
        inference: 推理方法
    
    Returns:
        解（列 -> 行映射），如果无解则返回 None
    """
    csp = create_n_queens_csp(n)
    solver = CSPSolver(csp, inference=inference)
    return solver.solve()


def solve_sudoku(grid: List[List[int]], inference: str = 'ac3') -> Optional[List[List[int]]]:
    """
    求解数独
    
    Args:
        grid: 9x9 数独网格
        inference: 推理方法
    
    Returns:
        解数独网格，如果无解则返回 None
    """
    csp = create_sudoku_csp(grid)
    solver = CSPSolver(csp, inference=inference)
    solution = solver.solve()
    
    if solution is None:
        return None
    
    result = [[0] * 9 for _ in range(9)]
    for (i, j), val in solution.items():
        result[i][j] = val
    
    return result


def solve_graph_coloring(
    vertices: List[T],
    edges: List[Tuple[T, T]],
    colors: List[V],
    inference: str = 'ac3'
) -> Optional[Dict[T, V]]:
    """
    求解图着色问题
    
    Args:
        vertices: 顶点列表
        edges: 边列表
        colors: 颜色列表
        inference: 推理方法
    
    Returns:
        解（顶点 -> 颜色映射），如果无解则返回 None
    """
    csp = create_graph_coloring_csp(vertices, edges, colors)
    solver = CSPSolver(csp, inference=inference)
    return solver.solve()


def count_n_queens_solutions(n: int) -> int:
    """
    计算 N 皇后问题的解的数量
    
    Args:
        n: 棋盘大小
    
    Returns:
        解的数量
    """
    csp = create_n_queens_csp(n)
    solver = CSPSolver(csp)
    solutions = solver.find_all_solutions(max_solutions=100000)
    return len(solutions)


def print_n_queens_solution(solution: Dict[int, int], n: int) -> str:
    """
    打印 N 皇后解
    
    Args:
        solution: 解（列 -> 行映射）
        n: 棋盘大小
    
    Returns:
        字符串表示
    """
    board = [['.'] * n for _ in range(n)]
    for col, row in solution.items():
        board[row][col] = 'Q'
    
    return '\n'.join(' '.join(row) for row in board)


def print_sudoku_solution(grid: List[List[int]]) -> str:
    """
    打印数独解
    
    Args:
        grid: 9x9 数独网格
    
    Returns:
        字符串表示
    """
    lines = []
    for i in range(9):
        if i > 0 and i % 3 == 0:
            lines.append('-' * 21)
        row = []
        for j in range(9):
            if j > 0 and j % 3 == 0:
                row.append('|')
            row.append(str(grid[i][j]))
        lines.append(' '.join(row))
    return '\n'.join(lines)
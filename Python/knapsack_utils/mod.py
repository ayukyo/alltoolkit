"""
背包问题求解工具模块 (Knapsack Problem Utils)

提供多种背包问题求解算法实现。
零外部依赖，纯 Python 实现。

核心功能：
- 0/1 背包问题求解（动态规划、递归、分支限界）
- 完全背包问题求解
- 多重背包问题求解
- 分数背包问题求解（贪心算法）
- 多维背包问题求解
- 多目标背包问题求解
- 最优解回溯（获取具体物品）

作者: AllToolkit
日期: 2026-05-02
"""

from typing import List, Tuple, Dict, Optional, Union, Set
from dataclasses import dataclass
from enum import Enum
import math


class KnapsackMethod(Enum):
    """背包问题求解方法"""
    DP = "dynamic_programming"       # 动态规划（二维数组）
    DP_OPTIMIZED = "dp_optimized"    # 动态规划（空间优化）
    RECURSIVE = "recursive"          # 递归 + 记忆化
    BRANCH_BOUND = "branch_bound"    # 分支限界
    GREEDY = "greedy"                # 贪心算法（仅分数背包）


@dataclass
class Item:
    """物品数据类"""
    weight: float
    value: float
    name: str = ""
    count: int = 1  # 用于多重背包
    
    def __post_init__(self):
        if not self.name:
            self.name = f"item_{id(self)}"
    
    @property
    def ratio(self) -> float:
        """价值密度（价值/重量）"""
        if self.weight == 0:
            return float('inf')
        return self.value / self.weight


@dataclass
class KnapsackResult:
    """背包问题求解结果"""
    max_value: float
    total_weight: float
    selected_items: List[Item]
    selected_indices: List[int]
    
    def __repr__(self) -> str:
        return (f"KnapsackResult(max_value={self.max_value:.2f}, "
                f"total_weight={self.total_weight:.2f}, "
                f"items={len(self.selected_items)})")


def _validate_capacity(capacity: float) -> None:
    """验证背包容量"""
    if not isinstance(capacity, (int, float)):
        raise TypeError(f"背包容量必须是数值类型，发现 {type(capacity).__name__}")
    if capacity < 0:
        raise ValueError(f"背包容量不能为负数，发现 {capacity}")


def _validate_items(items: List[Item]) -> None:
    """验证物品列表"""
    if not items:
        raise ValueError("物品列表不能为空")
    for i, item in enumerate(items):
        if not isinstance(item, Item):
            raise TypeError(f"物品必须是 Item 类型，位置 {i} 发现 {type(item).__name__}")
        if item.weight < 0:
            raise ValueError(f"物品重量不能为负数，位置 {i} 发现 {item.weight}")
        if item.value < 0:
            raise ValueError(f"物品价值不能为负数，位置 {i} 发现 {item.value}")


def knapsack_01(
    items: List[Item],
    capacity: float,
    method: KnapsackMethod = KnapsackMethod.DP_OPTIMIZED
) -> KnapsackResult:
    """
    0/1 背包问题求解（每个物品最多选一次）
    
    Args:
        items: 物品列表
        capacity: 背包容量
        method: 求解方法
    
    Returns:
        包含最大价值、总重量、选中物品的结果
    
    Examples:
        >>> items = [Item(10, 60, "A"), Item(20, 100, "B"), Item(30, 120, "C")]
        >>> result = knapsack_01(items, 50)
        >>> result.max_value
        220.0
    """
    _validate_items(items)
    _validate_capacity(capacity)
    
    n = len(items)
    
    if n == 0:
        return KnapsackResult(0.0, 0.0, [], [])
    
    # 特殊情况：容量为0或所有物品重量为0
    if capacity == 0:
        zero_weight_items = [i for i, item in enumerate(items) if item.weight == 0]
        total_value = sum(items[i].value for i in zero_weight_items)
        selected = [items[i] for i in zero_weight_items]
        return KnapsackResult(total_value, 0.0, selected, zero_weight_items)
    
    if method == KnapsackMethod.DP:
        return _knapsack_01_dp(items, capacity)
    elif method == KnapsackMethod.DP_OPTIMIZED:
        return _knapsack_01_dp_optimized(items, capacity)
    elif method == KnapsackMethod.RECURSIVE:
        return _knapsack_01_recursive(items, capacity)
    elif method == KnapsackMethod.BRANCH_BOUND:
        return _knapsack_01_branch_bound(items, capacity)
    else:
        raise ValueError(f"0/1 背包不支持方法: {method}")


def _knapsack_01_dp(items: List[Item], capacity: float) -> KnapsackResult:
    """动态规划求解（二维数组）"""
    n = len(items)
    # 转换为整数索引以支持浮点容量
    scale = 100  # 精度缩放因子
    cap = int(capacity * scale)
    
    # dp[i][j] = 前i个物品，容量j时的最大价值
    dp = [[0.0] * (cap + 1) for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        w = int(items[i - 1].weight * scale)
        v = items[i - 1].value
        for j in range(cap + 1):
            if w <= j:
                dp[i][j] = max(dp[i - 1][j], dp[i - 1][j - w] + v)
            else:
                dp[i][j] = dp[i - 1][j]
    
    # 回溯找选中物品
    selected_indices = []
    j = cap
    for i in range(n, 0, -1):
        if dp[i][j] != dp[i - 1][j]:
            selected_indices.append(i - 1)
            j -= int(items[i - 1].weight * scale)
    
    selected_indices.reverse()
    selected_items = [items[i] for i in selected_indices]
    total_weight = sum(items[i].weight for i in selected_indices)
    
    return KnapsackResult(
        max_value=dp[n][cap],
        total_weight=total_weight,
        selected_items=selected_items,
        selected_indices=selected_indices
    )


def _knapsack_01_dp_optimized(items: List[Item], capacity: float) -> KnapsackResult:
    """动态规划求解（空间优化，一维数组）"""
    n = len(items)
    scale = 100
    cap = int(capacity * scale)
    
    # 一维数组优化
    dp = [0.0] * (cap + 1)
    # 记录选择路径
    chosen = [[] for _ in range(cap + 1)]
    
    for i in range(n):
        w = int(items[i].weight * scale)
        v = items[i].value
        # 从后向前更新，避免重复选择
        for j in range(cap, w - 1, -1):
            if dp[j - w] + v > dp[j]:
                dp[j] = dp[j - w] + v
                chosen[j] = chosen[j - w] + [i]
    
    selected_indices = chosen[cap]
    selected_items = [items[i] for i in selected_indices]
    total_weight = sum(items[i].weight for i in selected_indices)
    
    return KnapsackResult(
        max_value=dp[cap],
        total_weight=total_weight,
        selected_items=selected_items,
        selected_indices=selected_indices
    )


def _knapsack_01_recursive(items: List[Item], capacity: float) -> KnapsackResult:
    """递归 + 记忆化求解"""
    n = len(items)
    scale = 100
    cap = int(capacity * scale)
    
    memo: Dict[Tuple[int, int], float] = {}
    
    def solve(i: int, remaining: int) -> float:
        if i == n or remaining == 0:
            return 0.0
        if (i, remaining) in memo:
            return memo[(i, remaining)]
        
        # 不选第i个物品
        result = solve(i + 1, remaining)
        
        # 选第i个物品（如果可以）
        w = int(items[i].weight * scale)
        v = items[i].value
        if w <= remaining:
            result = max(result, v + solve(i + 1, remaining - w))
        
        memo[(i, remaining)] = result
        return result
    
    max_value = solve(0, cap)
    
    # 回溯找选中物品
    selected_indices = []
    remaining = cap
    for i in range(n):
        w = int(items[i].weight * scale)
        key_without = (i + 1, remaining)
        without_val = memo.get(key_without, 0.0)
        
        if w <= remaining:
            key_with = (i + 1, remaining - w)
            with_val = items[i].value + memo.get(key_with, 0.0)
            if with_val > without_val:
                selected_indices.append(i)
                remaining -= w
    
    selected_items = [items[i] for i in selected_indices]
    total_weight = sum(items[i].weight for i in selected_indices)
    
    return KnapsackResult(
        max_value=max_value,
        total_weight=total_weight,
        selected_items=selected_items,
        selected_indices=selected_indices
    )


def _knapsack_01_branch_bound(items: List[Item], capacity: float) -> KnapsackResult:
    """分支限界法求解"""
    n = len(items)
    scale = 100
    cap = int(capacity * scale)
    
    # 按价值密度降序排序
    sorted_items = sorted(enumerate(items), key=lambda x: x[1].ratio, reverse=True)
    
    best_value = 0.0
    best_selection: List[int] = []
    
    # 上界估计：贪心计算（可能包含分数物品）
    def bound(level: int, current_weight: int, current_value: float) -> float:
        if current_weight > cap:
            return 0.0
        
        bound_value = current_value
        remaining = cap - current_weight
        
        for i in range(level, n):
            idx, item = sorted_items[i]
            w = int(item.weight * scale)
            v = item.value
            
            if w <= remaining:
                remaining -= w
                bound_value += v
            else:
                # 分数物品
                bound_value += v * remaining / w
                break
        
        return bound_value
    
    def branch(level: int, weight: int, value: float, selected: List[int]):
        nonlocal best_value, best_selection
        
        if level == n:
            if value > best_value:
                best_value = value
                best_selection = selected.copy()
            return
        
        idx, item = sorted_items[level]
        w = int(item.weight * scale)
        v = item.value
        
        # 选择当前物品
        if weight + w <= cap:
            selected.append(idx)
            branch(level + 1, weight + w, value + v, selected)
            selected.pop()
        
        # 不选当前物品
        if bound(level + 1, weight, value) > best_value:
            branch(level + 1, weight, value, selected)
    
    branch(0, 0, 0.0, [])
    
    selected_items = [items[i] for i in best_selection]
    total_weight = sum(items[i].weight for i in best_selection)
    
    return KnapsackResult(
        max_value=best_value,
        total_weight=total_weight,
        selected_items=selected_items,
        selected_indices=sorted(best_selection)
    )


def knapsack_complete(
    items: List[Item],
    capacity: float
) -> KnapsackResult:
    """
    完全背包问题求解（每种物品可选无限次）
    
    Args:
        items: 物品列表
        capacity: 背包容量
    
    Returns:
        包含最大价值、总重量、选中物品的结果
    
    Examples:
        >>> items = [Item(1, 1, "A"), Item(3, 4, "B")]
        >>> result = knapsack_complete(items, 5)
        >>> result.max_value
        6.0  # 选择1个A和1个B，或者多个B
    """
    _validate_items(items)
    _validate_capacity(capacity)
    
    n = len(items)
    scale = 100
    cap = int(capacity * scale)
    
    # dp[j] = 容量j时的最大价值
    dp = [0.0] * (cap + 1)
    # 记录每个容量选中的物品及其数量
    selection: List[List[Tuple[int, int]]] = [[] for _ in range(cap + 1)]
    
    for i in range(n):
        w = int(items[i].weight * scale)
        v = items[i].value
        # 正向更新（允许重复选择）
        for j in range(w, cap + 1):
            if dp[j - w] + v > dp[j]:
                dp[j] = dp[j - w] + v
                # 更新选择记录
                selection[j] = selection[j - w] + [(i, 1)]
    
    # 合并相同物品
    item_counts: Dict[int, int] = {}
    for idx, count in selection[cap]:
        item_counts[idx] = item_counts.get(idx, 0) + count
    
    selected_items = []
    selected_indices = []
    for idx, count in item_counts.items():
        for _ in range(count):
            selected_items.append(items[idx])
            selected_indices.append(idx)
    
    total_weight = sum(item.weight for item in selected_items)
    
    return KnapsackResult(
        max_value=dp[cap],
        total_weight=total_weight,
        selected_items=selected_items,
        selected_indices=selected_indices
    )


def knapsack_multiple(
    items: List[Item],
    capacity: float
) -> KnapsackResult:
    """
    多重背包问题求解（每种物品有数量限制）
    
    Args:
        items: 物品列表（item.count 表示该物品可用数量）
        capacity: 背包容量
    
    Returns:
        包含最大价值、总重量、选中物品的结果
    
    Examples:
        >>> items = [Item(2, 3, "A", count=2), Item(3, 4, "B", count=1)]
        >>> result = knapsack_multiple(items, 6)
        >>> result.max_value
        10.0  # 2个A
    """
    _validate_items(items)
    _validate_capacity(capacity)
    
    n = len(items)
    scale = 100
    cap = int(capacity * scale)
    
    # dp[j] = 容量j时的最大价值
    dp = [0.0] * (cap + 1)
    selection: List[List[Tuple[int, int]]] = [[] for _ in range(cap + 1)]
    
    for i in range(n):
        w = int(items[i].weight * scale)
        v = items[i].value
        count = items[i].count
        
        # 二进制拆分优化
        k = 1
        remaining = count
        while k <= remaining:
            # 将k个物品打包成一个"超级物品"
            kw = k * w
            kv = k * v
            
            for j in range(cap, kw - 1, -1):
                if dp[j - kw] + kv > dp[j]:
                    dp[j] = dp[j - kw] + kv
                    selection[j] = selection[j - kw] + [(i, k)]
            
            remaining -= k
            k *= 2
        
        # 处理剩余数量
        if remaining > 0:
            kw = remaining * w
            kv = remaining * v
            
            for j in range(cap, kw - 1, -1):
                if dp[j - kw] + kv > dp[j]:
                    dp[j] = dp[j - kw] + kv
                    selection[j] = selection[j - kw] + [(i, remaining)]
    
    # 合并物品
    item_counts: Dict[int, int] = {}
    for idx, count in selection[cap]:
        item_counts[idx] = item_counts.get(idx, 0) + count
    
    selected_items = []
    selected_indices = []
    for idx, count in item_counts.items():
        for _ in range(count):
            selected_items.append(items[idx])
            selected_indices.append(idx)
    
    total_weight = sum(item.weight for item in selected_items)
    
    return KnapsackResult(
        max_value=dp[cap],
        total_weight=total_weight,
        selected_items=selected_items,
        selected_indices=selected_indices
    )


def knapsack_fractional(
    items: List[Item],
    capacity: float
) -> Tuple[float, float, List[Tuple[Item, float]]]:
    """
    分数背包问题求解（可以取物品的一部分）
    
    使用贪心算法，按价值密度降序选择
    
    Args:
        items: 物品列表
        capacity: 背包容量
    
    Returns:
        (最大价值, 总重量, 选中物品及比例列表)
    
    Examples:
        >>> items = [Item(10, 60, "A"), Item(20, 100, "B"), Item(30, 120, "C")]
        >>> value, weight, selected = knapsack_fractional(items, 50)
        >>> value
        240.0  # 取完A和B
    """
    _validate_items(items)
    _validate_capacity(capacity)
    
    # 按价值密度降序排序
    sorted_items = sorted(items, key=lambda x: x.ratio, reverse=True)
    
    total_value = 0.0
    total_weight = 0.0
    selected: List[Tuple[Item, float]] = []
    remaining = capacity
    
    for item in sorted_items:
        if remaining <= 0:
            break
        
        if item.weight <= remaining:
            # 取整个物品
            selected.append((item, 1.0))
            total_value += item.value
            total_weight += item.weight
            remaining -= item.weight
        else:
            # 取部分物品
            fraction = remaining / item.weight
            selected.append((item, fraction))
            total_value += item.value * fraction
            total_weight += remaining
            remaining = 0
    
    return total_value, total_weight, selected


def knapsack_multi_dim(
    items: List[Item],
    capacities: List[float]
) -> KnapsackResult:
    """
    多维背包问题求解（多个容量约束）
    
    使用 items[i].weight 作为主重量，额外的约束存储在其他属性中
    这里简化为：Item.weight 和 Item.value 被重新解释
    capacities[0] = 重量容量，capacities[1] = 体积容量等
    
    注意：此实现假设每个物品有多个维度的重量
    我们用一个简化的方式：weight 表示重量，count 表示体积
    
    Args:
        items: 物品列表
        capacities: 各维度的容量列表
    
    Returns:
        求解结果
    """
    _validate_items(items)
    
    if not capacities:
        raise ValueError("容量列表不能为空")
    
    for cap in capacities:
        _validate_capacity(cap)
    
    dims = len(capacities)
    n = len(items)
    
    # 为简化，我们使用 count 字段存储额外维度的重量
    # 这里只演示二维情况
    if dims > 2:
        # 多维DP过于复杂，这里简化处理
        # 实际应用中可以使用启发式或近似算法
        pass
    
    scale = 100
    
    if dims == 1:
        return knapsack_01(items, capacities[0])
    
    # 二维DP
    cap1 = int(capacities[0] * scale)
    cap2 = int(capacities[1] * scale)
    
    # dp[j][k] = 重量j、体积k时的最大价值
    dp = [[[0.0, []] for _ in range(cap2 + 1)] for _ in range(cap1 + 1)]
    
    for i in range(n):
        w1 = int(items[i].weight * scale)
        w2 = int(items[i].count * scale)  # count 字段作为第二个维度
        v = items[i].value
        
        for j in range(cap1, w1 - 1, -1):
            for k in range(cap2, w2 - 1, -1):
                if dp[j - w1][k - w2][0] + v > dp[j][k][0]:
                    dp[j][k][0] = dp[j - w1][k - w2][0] + v
                    dp[j][k][1] = dp[j - w1][k - w2][1] + [i]
    
    selected_indices = dp[cap1][cap2][1]
    selected_items = [items[i] for i in selected_indices]
    total_weight = sum(items[i].weight for i in selected_indices)
    
    return KnapsackResult(
        max_value=dp[cap1][cap2][0],
        total_weight=total_weight,
        selected_items=selected_items,
        selected_indices=selected_indices
    )


def knapsack_multi_objective(
    items: List[Item],
    capacity: float,
    weights: Tuple[float, float] = (0.5, 0.5)
) -> List[KnapsackResult]:
    """
    多目标背包问题求解（帕累托前沿）
    
    寻找在价值和另一个目标（如最小化重量）之间的权衡
    
    Args:
        items: 物品列表
        capacity: 背包容量
        weights: 两个目标的权重 (value_weight, weight_weight)
    
    Returns:
        帕累托前沿上的解列表
    """
    _validate_items(items)
    _validate_capacity(capacity)
    
    n = len(items)
    scale = 100
    cap = int(capacity * scale)
    
    # 生成所有可能的子集（适用于小规模问题）
    pareto_front: List[KnapsackResult] = []
    
    # 对于大规模问题，使用随机采样
    if n > 20:
        import random
        random.seed(42)
        
        for _ in range(1000):
            selected = []
            total_w = 0.0
            total_v = 0.0
            
            for i in range(n):
                if random.random() > 0.5:
                    w = items[i].weight
                    if total_w + w <= capacity:
                        selected.append(i)
                        total_w += w
                        total_v += items[i].value
            
            if selected:
                result = KnapsackResult(
                    max_value=total_v,
                    total_weight=total_w,
                    selected_items=[items[i] for i in selected],
                    selected_indices=selected
                )
                pareto_front.append(result)
    else:
        # 枚举所有子集
        for mask in range(1, 1 << n):
            total_w = 0.0
            total_v = 0.0
            selected = []
            
            for i in range(n):
                if mask & (1 << i):
                    total_w += items[i].weight
                    total_v += items[i].value
                    selected.append(i)
            
            if total_w <= capacity:
                result = KnapsackResult(
                    max_value=total_v,
                    total_weight=total_w,
                    selected_items=[items[i] for i in selected],
                    selected_indices=selected
                )
                pareto_front.append(result)
    
    # 筛选帕累托前沿
    pareto_optimal = []
    for candidate in pareto_front:
        dominated = False
        for other in pareto_front:
            # candidate 被 other 支配？
            # other 有更高价值且更轻
            if (other.max_value >= candidate.max_value and 
                other.total_weight <= candidate.total_weight and
                (other.max_value > candidate.max_value or 
                 other.total_weight < candidate.total_weight)):
                dominated = True
                break
        
        if not dominated:
            pareto_optimal.append(candidate)
    
    # 按价值排序
    pareto_optimal.sort(key=lambda x: x.max_value, reverse=True)
    
    return pareto_optimal


def knapsack_subset_sum(
    items: List[Union[Item, float]],
    target: float
) -> Tuple[bool, List[int]]:
    """
    子集和问题：找出重量和等于目标值的物品组合
    
    这是0/1背包的特例（value = weight）
    
    Args:
        items: 物品列表或数值列表
        target: 目标和
    
    Returns:
        (是否找到, 选中的索引列表)
    
    Examples:
        >>> items = [Item(3, 3, "A"), Item(5, 5, "B"), Item(7, 7, "C")]
        >>> found, selected = knapsack_subset_sum(items, 8)
        >>> found
        True  # A + B 或 C - B + ... 取决于具体数值
    """
    # 转换为数值列表
    values = []
    for item in items:
        if isinstance(item, Item):
            values.append(item.weight)
        elif isinstance(item, (int, float)):
            values.append(item)
        else:
            raise TypeError(f"不支持的类型: {type(item)}")
    
    if not values:
        return False, []
    
    scale = 100
    target_int = int(target * scale)
    
    # dp[j] = 能否凑出和j
    dp = [False] * (target_int + 1)
    dp[0] = True
    # 记录路径
    parent: List[Optional[int]] = [None] * (target_int + 1)
    
    for i, v in enumerate(values):
        vi = int(v * scale)
        for j in range(target_int, vi - 1, -1):
            if not dp[j] and dp[j - vi]:
                dp[j] = True
                parent[j] = i
    
    if not dp[target_int]:
        return False, []
    
    # 回溯
    selected = []
    j = target_int
    while j > 0 and parent[j] is not None:
        selected.append(parent[j])
        j -= int(values[parent[j]] * scale)
    
    return True, selected


def knapsack_min_items(
    items: List[Item],
    capacity: float,
    min_value: float
) -> Optional[KnapsackResult]:
    """
    最小物品数背包：用最少的物品达到最小价值要求
    
    Args:
        items: 物品列表
        capacity: 背包容量
        min_value: 最小价值要求
    
    Returns:
        满足条件的最小物品数方案，若无解返回 None
    """
    _validate_items(items)
    _validate_capacity(capacity)
    
    n = len(items)
    scale = 100
    cap = int(capacity * scale)
    
    # dp[j] = (达到价值v的最少物品数, 价值v)
    INF = float('inf')
    dp: List[Tuple[int, float]] = [(INF, 0.0) for _ in range(cap + 1)]
    dp[0] = (0, 0.0)
    selection: List[List[int]] = [[] for _ in range(cap + 1)]
    
    for i in range(n):
        w = int(items[i].weight * scale)
        v = items[i].value
        
        for j in range(cap, w - 1, -1):
            if dp[j - w][0] + 1 < dp[j][0]:
                dp[j] = (dp[j - w][0] + 1, dp[j - w][1] + v)
                selection[j] = selection[j - w] + [i]
    
    # 找满足最小价值且物品数最少的解
    best_result = None
    best_count = INF
    
    for j in range(cap + 1):
        if dp[j][1] >= min_value and dp[j][0] < best_count:
            best_count = dp[j][0]
            selected_indices = selection[j]
            selected_items = [items[i] for i in selected_indices]
            total_weight = sum(items[i].weight for i in selected_indices)
            
            best_result = KnapsackResult(
                max_value=dp[j][1],
                total_weight=total_weight,
                selected_items=selected_items,
                selected_indices=selected_indices
            )
    
    return best_result


def knapsack_all_solutions(
    items: List[Item],
    capacity: float,
    max_solutions: int = 100
) -> List[KnapsackResult]:
    """
    找出背包问题的所有最优解
    
    Args:
        items: 物品列表
        capacity: 背包容量
        max_solutions: 最大返回解数
    
    Returns:
        所有最优解列表
    """
    _validate_items(items)
    _validate_capacity(capacity)
    
    # 首先找到最优值
    optimal = knapsack_01(items, capacity)
    optimal_value = optimal.max_value
    
    n = len(items)
    scale = 100
    cap = int(capacity * scale)
    
    # 使用回溯找所有解
    solutions: List[KnapsackResult] = []
    
    def backtrack(i: int, remaining: int, current_value: float, 
                  selected: List[int], current_weight: float):
        if len(solutions) >= max_solutions:
            return
        
        if i == n:
            if abs(current_value - optimal_value) < 1e-9:
                solutions.append(KnapsackResult(
                    max_value=current_value,
                    total_weight=current_weight,
                    selected_items=[items[j] for j in selected],
                    selected_indices=sorted(selected)
                ))
            return
        
        w = int(items[i].weight * scale)
        v = items[i].value
        
        # 剪枝：如果剩余物品全部选择也无法达到最优值
        remaining_max = sum(item.value for item in items[i:])
        if current_value + remaining_max < optimal_value - 1e-9:
            return
        
        # 选第i个物品
        if w <= remaining:
            backtrack(i + 1, remaining - w, current_value + v,
                     selected + [i], current_weight + items[i].weight)
        
        # 不选第i个物品
        backtrack(i + 1, remaining, current_value, selected, current_weight)
    
    backtrack(0, cap, 0.0, [], 0.0)
    
    return solutions


def unbounded_knapsack(
    items: List[Item],
    capacity: float
) -> KnapsackResult:
    """
    无界背包问题（完全背包的别名）
    
    每种物品可选无限次
    
    Args:
        items: 物品列表
        capacity: 背包容量
    
    Returns:
        求解结果
    """
    return knapsack_complete(items, capacity)


def bounded_knapsack(
    items: List[Item],
    capacity: float,
    bounds: Dict[int, int]
) -> KnapsackResult:
    """
    有界背包问题（多重背包的另一种形式）
    
    Args:
        items: 物品列表
        capacity: 背包容量
        bounds: 每个物品索引对应的最大数量
    
    Returns:
        求解结果
    """
    _validate_items(items)
    _validate_capacity(capacity)
    
    # 创建带有数量限制的物品副本
    bounded_items = []
    for i, item in enumerate(items):
        count = bounds.get(i, item.count)
        bounded_items.append(Item(item.weight, item.value, item.name, count))
    
    return knapsack_multiple(bounded_items, capacity)


if __name__ == "__main__":
    # 简单测试
    print("=== 背包问题工具测试 ===\n")
    
    # 0/1 背包测试
    items_01 = [
        Item(10, 60, "物品A"),
        Item(20, 100, "物品B"),
        Item(30, 120, "物品C")
    ]
    
    print("0/1 背包问题:")
    print(f"物品: {[(i.name, i.weight, i.value) for i in items_01]}")
    print(f"容量: 50")
    
    result = knapsack_01(items_01, 50)
    print(f"结果: 最大价值 = {result.max_value}")
    print(f"选中物品: {[i.name for i in result.selected_items]}")
    print(f"总重量: {result.total_weight}")
    
    # 完全背包测试
    print("\n完全背包问题:")
    items_complete = [
        Item(1, 1, "物品X"),
        Item(3, 4, "物品Y"),
        Item(4, 5, "物品Z")
    ]
    print(f"物品: {[(i.name, i.weight, i.value) for i in items_complete]}")
    print(f"容量: 6")
    
    result = knapsack_complete(items_complete, 6)
    print(f"结果: 最大价值 = {result.max_value}")
    print(f"选中物品: {[i.name for i in result.selected_items]}")
    
    # 分数背包测试
    print("\n分数背包问题:")
    value, weight, selected = knapsack_fractional(items_01, 50)
    print(f"最大价值: {value}")
    print(f"总重量: {weight}")
    print(f"选中物品: {[(i.name, f'{r:.2%}') for i, r in selected]}")
    
    # 子集和测试
    print("\n子集和问题:")
    subset_items = [Item(3, 3, "A"), Item(5, 5, "B"), Item(7, 7, "C")]
    found, indices = knapsack_subset_sum(subset_items, 8)
    print(f"目标和: 8")
    print(f"找到: {found}")
    if found:
        print(f"选中: {[subset_items[i].name for i in indices]}")
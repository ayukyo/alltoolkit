"""
汉诺塔工具模块 (Tower of Hanoi Utils)

提供汉诺塔问题的完整解决方案，包括：
- 递归求解算法
- 非递归（迭代）求解算法
- 最少步数计算
- 移动验证
- 状态可视化
- 多柱汉诺塔（Frame-Stewart算法）

零外部依赖，纯Python实现。
"""

from typing import List, Tuple, Optional, Generator
from dataclasses import dataclass
from enum import Enum


class MoveError(Exception):
    """移动错误异常"""
    pass


@dataclass
class Move:
    """表示一次移动"""
    disk: int          # 盘子编号（1最小，越大越底）
    from_peg: int      # 起始柱子
    to_peg: int        # 目标柱子
    
    def __str__(self) -> str:
        return f"移动盘子 {self.disk} 从柱 {self.from_peg} 到柱 {self.to_peg}"
    
    def to_tuple(self) -> Tuple[int, int, int]:
        return (self.disk, self.from_peg, self.to_peg)


class HanoiState:
    """汉诺塔状态表示"""
    
    def __init__(self, num_disks: int, num_pegs: int = 3):
        """
        初始化汉诺塔状态
        
        Args:
            num_disks: 盘子数量
            num_pegs: 柱子数量（默认3）
        """
        if num_disks < 0:
            raise ValueError("盘子数量必须非负")
        if num_pegs < 3:
            raise ValueError("柱子数量至少为3")
        
        self.num_disks = num_disks
        self.num_pegs = num_pegs
        # 每个柱子是一个列表，存储盘子（从底到顶，数字越大盘越大）
        self.pegs: List[List[int]] = [[] for _ in range(num_pegs)]
        # 初始状态：所有盘子在第一根柱子
        for disk in range(num_disks, 0, -1):
            self.pegs[0].append(disk)
    
    def copy(self) -> 'HanoiState':
        """复制当前状态"""
        new_state = HanoiState.__new__(HanoiState)
        new_state.num_disks = self.num_disks
        new_state.num_pegs = self.num_pegs
        new_state.pegs = [peg[:] for peg in self.pegs]
        return new_state
    
    def is_valid_move(self, from_peg: int, to_peg: int) -> bool:
        """
        检查移动是否合法
        
        Args:
            from_peg: 起始柱子索引（0-based）
            to_peg: 目标柱子索引（0-based）
        
        Returns:
            移动是否合法
        """
        if from_peg < 0 or from_peg >= self.num_pegs:
            return False
        if to_peg < 0 or to_peg >= self.num_pegs:
            return False
        if from_peg == to_peg:
            return False
        if not self.pegs[from_peg]:
            return False
        
        from_disk = self.pegs[from_peg][-1]
        if self.pegs[to_peg]:
            to_disk = self.pegs[to_peg][-1]
            return from_disk < to_disk
        return True
    
    def move(self, from_peg: int, to_peg: int) -> Move:
        """
        执行移动
        
        Args:
            from_peg: 起始柱子索引
            to_peg: 目标柱子索引
        
        Returns:
            Move对象
        
        Raises:
            MoveError: 移动不合法时抛出
        """
        if not self.is_valid_move(from_peg, to_peg):
            raise MoveError(f"非法移动：从柱 {from_peg} 到柱 {to_peg}")
        
        disk = self.pegs[from_peg].pop()
        self.pegs[to_peg].append(disk)
        return Move(disk, from_peg, to_peg)
    
    def is_solved(self, target_peg: Optional[int] = None) -> bool:
        """
        检查是否已解决（所有盘子在目标柱子上）
        
        Args:
            target_peg: 目标柱子，默认为最后一根柱子
        
        Returns:
            是否已解决
        """
        if target_peg is None:
            target_peg = self.num_pegs - 1
        return (len(self.pegs[target_peg]) == self.num_disks and
                self.pegs[target_peg] == list(range(self.num_disks, 0, -1)))
    
    def get_top_disk(self, peg: int) -> Optional[int]:
        """获取柱子顶部的盘子编号"""
        if 0 <= peg < self.num_pegs and self.pegs[peg]:
            return self.pegs[peg][-1]
        return None
    
    def __str__(self) -> str:
        """可视化当前状态"""
        max_width = self.num_disks * 2 + 1 if self.num_disks > 0 else 1
        
        lines = []
        # 从顶部到底部
        for level in range(self.num_disks - 1, -1, -1):
            row = []
            for peg in self.pegs:
                if level < len(peg):
                    disk = peg[level]
                    disk_str = '█' * (disk * 2 - 1)
                    row.append(disk_str.center(max_width))
                else:
                    row.append('│'.center(max_width))
            lines.append('  '.join(row))
        
        # 底部
        bottom = '─' * max_width
        lines.append('  '.join([bottom] * self.num_pegs))
        
        # 柱子编号
        labels = '  '.join([str(i).center(max_width) for i in range(self.num_pegs)])
        lines.append(labels)
        
        return '\n'.join(lines)


def solve_recursive(num_disks: int, from_peg: int = 0, to_peg: int = 2, 
                    aux_peg: int = 1) -> List[Move]:
    """
    递归求解汉诺塔问题
    
    Args:
        num_disks: 盘子数量
        from_peg: 起始柱子
        to_peg: 目标柱子
        aux_peg: 辅助柱子
    
    Returns:
        移动序列
    """
    moves = []
    
    def _solve(n: int, src: int, dst: int, aux: int):
        if n == 0:
            return
        # 将n-1个盘子从src移动到aux
        _solve(n - 1, src, aux, dst)
        # 移动最大的盘子
        moves.append(Move(n, src, dst))
        # 将n-1个盘子从aux移动到dst
        _solve(n - 1, aux, dst, src)
    
    _solve(num_disks, from_peg, to_peg, aux_peg)
    return moves


def solve_iterative(num_disks: int, from_peg: int = 0, to_peg: int = 2,
                    aux_peg: int = 1) -> List[Move]:
    """
    迭代（非递归）求解汉诺塔问题
    
    使用栈模拟递归过程。
    
    Args:
        num_disks: 盘子数量
        from_peg: 起始柱子
        to_peg: 目标柱子
        aux_peg: 辅助柱子
    
    Returns:
        移动序列
    """
    if num_disks == 0:
        return []
    
    moves = []
    stack = [(num_disks, from_peg, to_peg, aux_peg, False)]
    
    while stack:
        n, src, dst, aux, done_first = stack.pop()
        if n == 0:
            continue
        if n == 1:
            moves.append(Move(1, src, dst))
        elif done_first:
            moves.append(Move(n, src, dst))
            stack.append((n - 1, aux, dst, src, False))
        else:
            stack.append((n, src, dst, aux, True))
            stack.append((n - 1, src, aux, dst, False))
    
    return moves


def solve_generator(num_disks: int, from_peg: int = 0, to_peg: int = 2,
                    aux_peg: int = 1) -> Generator[Move, None, None]:
    """
    生成器方式求解汉诺塔（节省内存）
    
    Args:
        num_disks: 盘子数量
        from_peg: 起始柱子
        to_peg: 目标柱子
        aux_peg: 辅助柱子
    
    Yields:
        每次移动
    """
    if num_disks == 0:
        return
    
    stack = [(num_disks, from_peg, to_peg, aux_peg, False)]
    
    while stack:
        n, src, dst, aux, done_first = stack.pop()
        if n == 0:
            continue
        if n == 1:
            yield Move(1, src, dst)
        elif done_first:
            yield Move(n, src, dst)
            stack.append((n - 1, aux, dst, src, False))
        else:
            stack.append((n, src, dst, aux, True))
            stack.append((n - 1, src, aux, dst, False))


def min_moves(num_disks: int) -> int:
    """
    计算汉诺塔最少移动次数
    
    对于3柱汉诺塔，最少移动次数为 2^n - 1
    
    Args:
        num_disks: 盘子数量
    
    Returns:
        最少移动次数
    """
    if num_disks < 0:
        raise ValueError("盘子数量必须非负")
    return (1 << num_disks) - 1  # 2^n - 1


def min_moves_frame_stewart(num_disks: int, num_pegs: int) -> int:
    """
    多柱汉诺塔最少移动次数估计（Frame-Stewart算法）
    
    对于4柱及以上，使用Frame-Stewart算法估计最少移动次数。
    注：该算法未被证明最优，但被认为是目前最好的估计。
    
    Args:
        num_disks: 盘子数量
        num_pegs: 柱子数量
    
    Returns:
        估计的最少移动次数
    """
    if num_disks < 0:
        raise ValueError("盘子数量必须非负")
    if num_pegs < 3:
        raise ValueError("柱子数量至少为3")
    if num_pegs == 3:
        return min_moves(num_disks)
    if num_disks == 0:
        return 0
    if num_disks == 1:
        return 1
    
    # 使用动态规划
    # dp[n][p] = n个盘子，p个柱子的最少移动次数
    INF = float('inf')
    dp = [[0] * (num_pegs + 1) for _ in range(num_disks + 1)]
    
    # 初始化
    for p in range(3, num_pegs + 1):
        dp[0][p] = 0
        dp[1][p] = 1
    
    for n in range(num_disks + 1):
        dp[n][3] = (1 << n) - 1  # 3柱情况
    
    # 递推
    for n in range(2, num_disks + 1):
        for p in range(4, num_pegs + 1):
            dp[n][p] = INF
            for k in range(1, n):
                # 将上面k个盘子用p个柱子移到中间
                # 将下面n-k个盘子用p-1个柱子移到目标
                moves = 2 * dp[k][p] + dp[n - k][p - 1]
                dp[n][p] = min(dp[n][p], moves)
    
    return dp[num_disks][num_pegs]


def solve_frame_stewart(num_disks: int, num_pegs: int = 4,
                        from_peg: int = 0, to_peg: int = None) -> List[Move]:
    """
    多柱汉诺塔求解（Frame-Stewart算法）
    
    Args:
        num_disks: 盘子数量
        num_pegs: 柱子数量（默认4）
        from_peg: 起始柱子
        to_peg: 目标柱子（默认最后一根）
    
    Returns:
        移动序列
    """
    if num_pegs < 3:
        raise ValueError("柱子数量至少为3")
    if to_peg is None:
        to_peg = num_pegs - 1
    
    moves = []
    state = HanoiState(num_disks, num_pegs)
    
    def _solve(n: int, src: int, dst: int, available_pegs: List[int]):
        if n == 0:
            return
        if n == 1:
            m = state.move(src, dst)
            moves.append(m)
            return
        
        p = len(available_pegs) + 2  # 总柱子数
        
        if p == 3:
            # 标准3柱递归
            aux = available_pegs[0]
            _solve(n - 1, src, aux, [dst])
            m = state.move(src, dst)
            moves.append(m)
            _solve(n - 1, aux, dst, [src])
            return
        
        # 找到最优的k值
        best_k = 1
        best_moves = float('inf')
        for k in range(1, n):
            # 估算移动次数
            moves_k = 2 * min_moves_frame_stewart(k, p) + min_moves_frame_stewart(n - k, p - 1)
            if moves_k < best_moves:
                best_moves = moves_k
                best_k = k
        
        # 选择中间柱子（取第一个可用的）
        intermediate = available_pegs[0]
        remaining_pegs = available_pegs[1:]
        
        # 步骤1：将上面k个盘子移到中间柱
        _solve(best_k, src, intermediate, [dst] + remaining_pegs)
        
        # 步骤2：将下面n-k个盘子移到目标（少用一个柱子）
        _solve(n - best_k, src, dst, remaining_pegs)
        
        # 步骤3：将k个盘子从中间移到目标
        _solve(best_k, intermediate, dst, [src] + remaining_pegs)
    
    available = [i for i in range(num_pegs) if i != from_peg and i != to_peg]
    _solve(num_disks, from_peg, to_peg, available)
    
    return moves


def validate_solution(num_disks: int, moves: List[Move], 
                      num_pegs: int = 3, target_peg: int = None) -> bool:
    """
    验证解的正确性
    
    Args:
        num_disks: 盘子数量
        moves: 移动序列
        num_pegs: 柱子数量
        target_peg: 目标柱子
    
    Returns:
        解是否正确
    """
    if target_peg is None:
        target_peg = num_pegs - 1
    
    state = HanoiState(num_disks, num_pegs)
    
    try:
        for move in moves:
            state.move(move.from_peg, move.to_peg)
        return state.is_solved(target_peg)
    except MoveError:
        return False


def visualize_moves(num_disks: int, moves: List[Move], 
                    num_pegs: int = 3) -> Generator[str, None, None]:
    """
    生成可视化的移动步骤
    
    Args:
        num_disks: 盘子数量
        moves: 移动序列
        num_pegs: 柱子数量
    
    Yields:
        每一步的可视化字符串
    """
    state = HanoiState(num_disks, num_pegs)
    yield f"初始状态:\n{state}\n"
    
    for i, move in enumerate(moves, 1):
        state.move(move.from_peg, move.to_peg)
        yield f"第 {i} 步: {move}\n{state}\n"


def get_disk_sequence(moves: List[Move]) -> List[int]:
    """
    获取移动的盘子序列
    
    Args:
        moves: 移动序列
    
    Returns:
        盘子编号序列
    """
    return [move.disk for move in moves]


def analyze_moves(moves: List[Move]) -> dict:
    """
    分析移动序列
    
    Args:
        moves: 移动序列
    
    Returns:
        分析结果字典
    """
    if not moves:
        return {
            'total_moves': 0,
            'unique_disks': 0,
            'moves_per_disk': {},
            'peg_usage': {}
        }
    
    moves_per_disk = {}
    peg_usage = {}
    
    for move in moves:
        # 统计每个盘子的移动次数
        moves_per_disk[move.disk] = moves_per_disk.get(move.disk, 0) + 1
        # 统计柱子使用次数
        peg_usage[move.from_peg] = peg_usage.get(move.from_peg, 0) + 1
        peg_usage[move.to_peg] = peg_usage.get(move.to_peg, 0) + 1
    
    return {
        'total_moves': len(moves),
        'unique_disks': len(moves_per_disk),
        'moves_per_disk': moves_per_disk,
        'peg_usage': peg_usage,
        'min_disk': min(moves_per_disk.keys()),
        'max_disk': max(moves_per_disk.keys())
    }


def is_optimal_solution(num_disks: int, moves: List[Move]) -> bool:
    """
    判断解是否为最优解（移动次数最少）
    
    Args:
        num_disks: 盘子数量
        moves: 移动序列
    
    Returns:
        是否为最优解
    """
    return len(moves) == min_moves(num_disks)


def count_moves_for_pattern(num_disks: int, pattern: str = 'sequential') -> int:
    """
    计算特定模式的移动次数
    
    Args:
        num_disks: 盘子数量
        pattern: 模式名称
            - 'sequential': 顺序移动（标准解法）
            - 'alternating': 交替模式
    
    Returns:
        移动次数
    """
    if pattern == 'sequential':
        return min_moves(num_disks)
    elif pattern == 'alternating':
        # 交替模式（不是最优解，仅供参考）
        return num_disks * (num_disks + 1) // 2
    else:
        raise ValueError(f"未知模式: {pattern}")


def get_move_direction(from_peg: int, to_peg: int, num_pegs: int = 3) -> str:
    """
    获取移动方向的描述
    
    Args:
        from_peg: 起始柱子
        to_peg: 目标柱子
        num_pegs: 总柱子数
    
    Returns:
        方向描述
    """
    if num_pegs == 3:
        labels = ['左', '中', '右']
        return f"{labels[from_peg]} -> {labels[to_peg]}"
    return f"柱{from_peg} -> 柱{to_peg}"


class HanoiSolver:
    """汉诺塔求解器类（面向对象接口）"""
    
    def __init__(self, num_disks: int, num_pegs: int = 3):
        """
        初始化求解器
        
        Args:
            num_disks: 盘子数量
            num_pegs: 柱子数量
        """
        self.num_disks = num_disks
        self.num_pegs = num_pegs
        self._moves: Optional[List[Move]] = None
    
    def solve(self, method: str = 'recursive') -> List[Move]:
        """
        求解汉诺塔
        
        Args:
            method: 求解方法 ('recursive' 或 'iterative')
        
        Returns:
            移动序列
        """
        if self.num_pegs == 3:
            if method == 'recursive':
                self._moves = solve_recursive(self.num_disks)
            elif method == 'iterative':
                self._moves = solve_iterative(self.num_disks)
            else:
                raise ValueError(f"未知方法: {method}")
        else:
            self._moves = solve_frame_stewart(self.num_disks, self.num_pegs)
        
        return self._moves
    
    @property
    def moves(self) -> List[Move]:
        """获取移动序列（如未求解则先求解）"""
        if self._moves is None:
            self.solve()
        return self._moves
    
    @property
    def move_count(self) -> int:
        """获取移动次数"""
        return len(self.moves)
    
    def is_optimal(self) -> bool:
        """判断当前解是否最优"""
        if self.num_pegs == 3:
            return self.move_count == min_moves(self.num_disks)
        return self.move_count == min_moves_frame_stewart(self.num_disks, self.num_pegs)
    
    def simulate(self) -> Generator[HanoiState, None, None]:
        """
        模拟每一步的状态
        
        Yields:
            每一步的状态
        """
        state = HanoiState(self.num_disks, self.num_pegs)
        yield state.copy()
        
        for move in self.moves:
            state.move(move.from_peg, move.to_peg)
            yield state.copy()
    
    def print_solution(self, show_state: bool = False) -> None:
        """
        打印解
        
        Args:
            show_state: 是否显示每一步的状态
        """
        print(f"汉诺塔解法（{self.num_disks}个盘子，{self.num_pegs}根柱子）")
        print(f"最少移动次数: {min_moves(self.num_disks) if self.num_pegs == 3 else min_moves_frame_stewart(self.num_disks, self.num_pegs)}")
        print(f"实际移动次数: {self.move_count}")
        print("-" * 50)
        
        if show_state:
            for i, (state, move) in enumerate(zip(self.simulate(), [None] + self.moves)):
                if move:
                    print(f"第 {i} 步: {move}")
                print(state)
                print()
        else:
            for i, move in enumerate(self.moves, 1):
                print(f"第 {i} 步: {move}")


# 便捷函数
def hanoi(num_disks: int, method: str = 'recursive') -> List[Move]:
    """
    快速求解汉诺塔
    
    Args:
        num_disks: 盘子数量
        method: 求解方法
    
    Returns:
        移动序列
    """
    if method == 'recursive':
        return solve_recursive(num_disks)
    elif method == 'iterative':
        return solve_iterative(num_disks)
    else:
        raise ValueError(f"未知方法: {method}")


def hanoi_demo(num_disks: int = 3) -> str:
    """
    生成汉诺塔演示
    
    Args:
        num_disks: 盘子数量
    
    Returns:
        演示字符串
    """
    moves = solve_recursive(num_disks)
    output = []
    output.append(f"汉诺塔演示（{num_disks}个盘子）")
    output.append(f"最少移动次数: 2^{num_disks} - 1 = {min_moves(num_disks)}")
    output.append("=" * 40)
    
    state = HanoiState(num_disks)
    output.append(str(state))
    
    for i, move in enumerate(moves, 1):
        state.move(move.from_peg, move.to_peg)
        output.append(f"\n第 {i} 步: {move}")
        output.append(str(state))
    
    return '\n'.join(output)
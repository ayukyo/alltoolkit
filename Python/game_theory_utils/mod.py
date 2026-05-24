"""
Game Theory Utils - 游戏理论工具模块
====================================

提供经典博弈论算法和工具，包括：
- 纳什均衡求解器
- 囚徒困境模拟器
- 极小化极大算法（带Alpha-Beta剪枝）
- 支付矩阵分析
- 拍卖机制（维克瑞、英式、荷式）
- 博弈树表示
- 优势策略检测
- 帕累托效率分析

零外部依赖，纯Python实现。
"""

from typing import List, Tuple, Dict, Optional, Callable, Any, Set
from dataclasses import dataclass, field
from enum import Enum
from abc import ABC, abstractmethod
import random
import math
from copy import deepcopy


class GameType(Enum):
    """博弈类型枚举"""
    ZERO_SUM = "zero_sum"          # 零和博弈
    NON_ZERO_SUM = "non_zero_sum"  # 非零和博弈
    COOPERATIVE = "cooperative"    # 合作博弈
    SEQUENTIAL = "sequential"      # 序贯博弈
    SIMULTANEOUS = "simultaneous"  # 同时博弈


class StrategyType(Enum):
    """策略类型枚举"""
    PURE = "pure"      # 纯策略
    MIXED = "mixed"    # 混合策略
    DOMINANT = "dominant"  # 优势策略
    DOMINATED = "dominated"  # 劣势策略


@dataclass
class PayoffMatrix:
    """
    支付矩阵类
    
    用于表示两人博弈的支付结构。
    支持任意大小的策略空间。
    """
    player1_payoffs: List[List[float]]  # 玩家1的支付矩阵
    player2_payoffs: List[List[float]]  # 玩家2的支付矩阵
    player1_strategies: List[str] = field(default_factory=list)
    player2_strategies: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        """初始化策略名称"""
        rows = len(self.player1_payoffs)
        cols = len(self.player1_payoffs[0]) if rows > 0 else 0
        
        if not self.player1_strategies:
            self.player1_strategies = [f"S1_{i}" for i in range(rows)]
        if not self.player2_strategies:
            self.player2_strategies = [f"S2_{j}" for j in range(cols)]
    
    @property
    def rows(self) -> int:
        """获取行数（玩家1的策略数）"""
        return len(self.player1_payoffs)
    
    @property
    def cols(self) -> int:
        """获取列数（玩家2的策略数）"""
        return len(self.player1_payoffs[0]) if self.rows > 0 else 0
    
    def get_payoff(self, p1_strategy: int, p2_strategy: int) -> Tuple[float, float]:
        """获取特定策略组合下的支付"""
        return (
            self.player1_payoffs[p1_strategy][p2_strategy],
            self.player2_payoffs[p1_strategy][p2_strategy]
        )
    
    def is_zero_sum(self, tolerance: float = 1e-9) -> bool:
        """检查是否为零和博弈"""
        for i in range(self.rows):
            for j in range(self.cols):
                p1, p2 = self.get_payoff(i, j)
                if abs(p1 + p2) > tolerance:
                    return False
        return True
    
    def to_dict(self) -> Dict:
        """转换为字典表示"""
        return {
            "player1_strategies": self.player1_strategies,
            "player2_strategies": self.player2_strategies,
            "player1_payoffs": self.player1_payoffs,
            "player2_payoffs": self.player2_payoffs,
            "is_zero_sum": self.is_zero_sum()
        }


@dataclass
class NashEquilibrium:
    """纳什均衡结果"""
    player1_strategy: Optional[int] = None  # 纯策略索引
    player2_strategy: Optional[int] = None
    player1_mixed: Optional[List[float]] = None  # 混合策略概率
    player2_mixed: Optional[List[float]] = None
    payoff: Tuple[float, float] = (0.0, 0.0)
    is_pure: bool = True
    
    def to_dict(self) -> Dict:
        return {
            "player1_strategy": self.player1_strategy,
            "player2_strategy": self.player2_strategy,
            "player1_mixed": self.player1_mixed,
            "player2_mixed": self.player2_mixed,
            "payoff": self.payoff,
            "is_pure": self.is_pure
        }


class NashEquilibriumSolver:
    """
    纳什均衡求解器
    
    支持：
    - 纯策略纳什均衡
    - 2x2博弈的混合策略纳什均衡
    """
    
    @staticmethod
    def find_pure_nash(matrix: PayoffMatrix) -> List[NashEquilibrium]:
        """
        寻找所有纯策略纳什均衡
        
        通过检查每个策略组合是否满足纳什均衡条件：
        没有任何玩家能通过单方面改变策略获得更高支付。
        """
        equilibria = []
        
        for i in range(matrix.rows):
            for j in range(matrix.cols):
                p1_payoff, p2_payoff = matrix.get_payoff(i, j)
                
                # 检查玩家1是否有偏离动机
                p1_best_response = True
                for i2 in range(matrix.rows):
                    if matrix.player1_payoffs[i2][j] > p1_payoff:
                        p1_best_response = False
                        break
                
                # 检查玩家2是否有偏离动机
                p2_best_response = True
                for j2 in range(matrix.cols):
                    if matrix.player2_payoffs[i][j2] > p2_payoff:
                        p2_best_response = False
                        break
                
                if p1_best_response and p2_best_response:
                    equilibria.append(NashEquilibrium(
                        player1_strategy=i,
                        player2_strategy=j,
                        payoff=(p1_payoff, p2_payoff),
                        is_pure=True
                    ))
        
        return equilibria
    
    @staticmethod
    def find_mixed_nash_2x2(matrix: PayoffMatrix) -> Optional[NashEquilibrium]:
        """
        计算2x2博弈的混合策略纳什均衡
        
        对于2x2博弈，使用解析方法计算混合策略。
        """
        if matrix.rows != 2 or matrix.cols != 2:
            return None
        
        a = matrix.player1_payoffs[0][0]  # (U, L)时玩家1的支付
        b = matrix.player1_payoffs[0][1]  # (U, R)时玩家1的支付
        c = matrix.player1_payoffs[1][0]  # (D, L)时玩家1的支付
        d = matrix.player1_payoffs[1][1]  # (D, R)时玩家1的支付
        
        e = matrix.player2_payoffs[0][0]  # (U, L)时玩家2的支付
        f = matrix.player2_payoffs[0][1]  # (U, R)时玩家2的支付
        g = matrix.player2_payoffs[1][0]  # (D, L)时玩家2的支付
        h = matrix.player2_payoffs[1][1]  # (D, R)时玩家2的支付
        
        # 计算玩家2玩L的概率q，使得玩家1在U和D之间无差异
        # E[U] = E[D]
        # a*q + b*(1-q) = c*q + d*(1-q)
        denom1 = (a - b) - (c - d)
        
        # 计算玩家1玩U的概率p，使得玩家2在L和R之间无差异
        # E[L] = E[R]
        denom2 = (e - g) - (f - h)
        
        if abs(denom1) < 1e-9 or abs(denom2) < 1e-9:
            return None  # 存在纯策略均衡
        
        q = (d - c) / denom1  # 玩家2玩L的概率
        p = (h - g) / denom2  # 玩家1玩U的概率
        
        # 验证概率在[0,1]范围内
        if not (0 <= p <= 1 and 0 <= q <= 1):
            return None
        
        # 计算期望支付
        expected_p1 = p * (a * q + b * (1 - q)) + (1 - p) * (c * q + d * (1 - q))
        expected_p2 = q * (e * p + g * (1 - p)) + (1 - q) * (f * p + h * (1 - p))
        
        return NashEquilibrium(
            player1_mixed=[p, 1 - p],
            player2_mixed=[q, 1 - q],
            payoff=(expected_p1, expected_p2),
            is_pure=False
        )
    
    @staticmethod
    def find_all_nash(matrix: PayoffMatrix) -> List[NashEquilibrium]:
        """寻找所有纳什均衡（纯策略 + 混合策略）"""
        equilibria = NashEquilibriumSolver.find_pure_nash(matrix)
        
        # 对于2x2博弈，尝试寻找混合策略均衡
        if matrix.rows == 2 and matrix.cols == 2:
            mixed = NashEquilibriumSolver.find_mixed_nash_2x2(matrix)
            if mixed:
                equilibria.append(mixed)
        
        return equilibria


class PrisonersDilemma:
    """
    囚徒困境模拟器
    
    经典博弈论问题：两名囚犯被捕，
    每人都有合作（保持沉默）或背叛（供出对方）的选择。
    """
    
    # 标准囚徒困境支付矩阵
    STANDARD_PAYOFFS = PayoffMatrix(
        player1_payoffs=[
            [-1, -10],  # 合作
            [0, -5]     # 背叛
        ],
        player2_payoffs=[
            [-1, 0],
            [-10, -5]
        ],
        player1_strategies=["合作", "背叛"],
        player2_strategies=["合作", "背叛"]
    )
    
    def __init__(self, 
                 temptation: float = 0,
                 reward: float = -1,
                 punishment: float = -5,
                 sucker: float = -10):
        """
        初始化囚徒困境
        
        Args:
            temptation: 背叛诱惑收益 (T)
            reward: 双方合作收益 (R)
            punishment: 双方背叛惩罚 (P)
            sucker: 被背叛的冤大头收益 (S)
        
        囚徒困境条件：T > R > P > S
        """
        self.payoff_matrix = PayoffMatrix(
            player1_payoffs=[
                [reward, sucker],
                [temptation, punishment]
            ],
            player2_payoffs=[
                [reward, temptation],
                [sucker, punishment]
            ],
            player1_strategies=["合作", "背叛"],
            player2_strategies=["合作", "背叛"]
        )
        self.temptation = temptation
        self.reward = reward
        self.punishment = punishment
        self.sucker = sucker
    
    def is_valid_dilemma(self) -> bool:
        """检查是否满足囚徒困境条件"""
        return (self.temptation > self.reward > 
                self.punishment > self.sucker)
    
    def analyze(self) -> Dict:
        """分析囚徒困境"""
        equilibria = NashEquilibriumSolver.find_all_nash(self.payoff_matrix)
        
        return {
            "is_valid_dilemma": self.is_valid_dilemma(),
            "payoffs": {
                "temptation": self.temptation,
                "reward": self.reward,
                "punishment": self.punishment,
                "sucker": self.sucker
            },
            "nash_equilibria": [eq.to_dict() for eq in equilibria],
            "pareto_optimal": self._find_pareto_optimal(),
            "dominant_strategy": "背叛" if self.is_valid_dilemma() else None
        }
    
    def _find_pareto_optimal(self) -> List[Tuple[int, int]]:
        """寻找帕累托最优策略组合"""
        pareto_optimal = []
        
        for i in range(2):
            for j in range(2):
                p1, p2 = self.payoff_matrix.get_payoff(i, j)
                
                # 检查是否有其他策略组合帕累托优于当前组合
                is_pareto = True
                for i2 in range(2):
                    for j2 in range(2):
                        if i == i2 and j == j2:
                            continue
                        p1_new, p2_new = self.payoff_matrix.get_payoff(i2, j2)
                        
                        # 如果新组合至少有一人更好且没有人更差
                        if (p1_new >= p1 and p2_new >= p2 and 
                            (p1_new > p1 or p2_new > p2)):
                            is_pareto = False
                            break
                    if not is_pareto:
                        break
                
                if is_pareto:
                    pareto_optimal.append((i, j))
        
        return pareto_optimal
    
    @staticmethod
    def simulate_repeated(rounds: int = 10,
                         strategy1: str = "tit_for_tat",
                         strategy2: str = "always_defect",
                         temptation: float = 5,
                         reward: float = 3,
                         punishment: float = 1,
                         sucker: float = 0) -> Dict:
        """
        模拟重复囚徒困境
        
        Args:
            rounds: 回合数
            strategy1: 玩家1策略
            strategy2: 玩家2策略
        """
        game = PrisonersDilemma(temptation, reward, punishment, sucker)
        
        history1 = []  # 玩家1的历史选择 (0=合作, 1=背叛)
        history2 = []  # 玩家2的历史选择
        
        total_payoff1 = 0
        total_payoff2 = 0
        
        strategies = {
            "always_cooperate": lambda h1, h2: 0,
            "always_defect": lambda h1, h2: 1,
            "random": lambda h1, h2: random.randint(0, 1),
            "tit_for_tat": lambda h1, h2: 0 if len(h2) == 0 else h2[-1],
            "grim_trigger": lambda h1, h2: 0 if 1 not in h2 else 1,
            "pavlov": lambda h1, h2: 0 if len(h1) == 0 else (h1[-1] if h1[-1] == h2[-1] else 1 - h1[-1]),
        }
        
        s1 = strategies.get(strategy1, strategies["random"])
        s2 = strategies.get(strategy2, strategies["random"])
        
        for _ in range(rounds):
            move1 = s1(history1, history2)
            move2 = s2(history2, history1)
            
            p1, p2 = game.payoff_matrix.get_payoff(move1, move2)
            total_payoff1 += p1
            total_payoff2 += p2
            
            history1.append(move1)
            history2.append(move2)
        
        return {
            "rounds": rounds,
            "strategy1": strategy1,
            "strategy2": strategy2,
            "total_payoff1": total_payoff1,
            "total_payoff2": total_payoff2,
            "average_payoff1": total_payoff1 / rounds,
            "average_payoff2": total_payoff2 / rounds,
            "history1": history1,
            "history2": history2
        }


@dataclass
class GameTreeNode:
    """博弈树节点"""
    player: int  # 当前决策玩家 (0或1)
    children: Dict[int, 'GameTreeNode'] = field(default_factory=dict)  # 行动 -> 子节点
    payoff: Optional[Tuple[float, float]] = None  # 叶节点的支付
    is_terminal: bool = False
    info: str = ""  # 节点描述
    
    def add_child(self, action: int, child: 'GameTreeNode'):
        """添加子节点"""
        self.children[action] = child
    
    def is_leaf(self) -> bool:
        """是否为叶节点"""
        return self.is_terminal or len(self.children) == 0


class MinimaxSolver:
    """
    极小化极大算法求解器
    
    用于解决完全信息零和博弈。
    支持Alpha-Beta剪枝优化。
    """
    
    def __init__(self, max_depth: int = 10):
        """
        初始化求解器
        
        Args:
            max_depth: 最大搜索深度
        """
        self.max_depth = max_depth
        self.nodes_evaluated = 0
    
    def solve(self, node: GameTreeNode, 
              maximizing_player: int = 0,
              alpha: float = float('-inf'),
              beta: float = float('inf')) -> Tuple[float, Optional[int]]:
        """
        使用Minimax算法（带Alpha-Beta剪枝）求解
        
        Args:
            node: 当前博弈树节点
            maximizing_player: 最大化玩家（0或1）
            alpha: Alpha值（最大化玩家的当前最优）
            beta: Beta值（最小化玩家的当前最优）
        
        Returns:
            (最优值, 最优行动)
        """
        self.nodes_evaluated += 1
        
        if node.is_leaf() or node.payoff is not None:
            return node.payoff[maximizing_player], None
        
        if node.player == maximizing_player:
            # 最大化玩家
            max_eval = float('-inf')
            best_action = None
            
            for action, child in node.children.items():
                eval_score, _ = self.solve(child, maximizing_player, alpha, beta)
                
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_action = action
                
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break  # Beta剪枝
            
            return max_eval, best_action
        else:
            # 最小化玩家
            min_eval = float('inf')
            best_action = None
            
            for action, child in node.children.items():
                eval_score, _ = self.solve(child, maximizing_player, alpha, beta)
                
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_action = action
                
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break  # Alpha剪枝
            
            return min_eval, best_action
    
    def reset_counter(self):
        """重置节点计数器"""
        self.nodes_evaluated = 0


class TicTacToe:
    """
    井字棋游戏
    
    使用Minimax算法实现AI对手。
    """
    
    def __init__(self):
        self.board = [[0, 0, 0] for _ in range(3)]  # 0=空, 1=X, 2=O
        self.current_player = 1  # X先手
    
    def clone(self) -> 'TicTacToe':
        """克隆游戏状态"""
        new_game = TicTacToe()
        new_game.board = [row[:] for row in self.board]
        new_game.current_player = self.current_player
        return new_game
    
    def get_valid_moves(self) -> List[Tuple[int, int]]:
        """获取所有有效移动"""
        return [(i, j) for i in range(3) for j in range(3) if self.board[i][j] == 0]
    
    def make_move(self, row: int, col: int) -> bool:
        """执行移动"""
        if self.board[row][col] != 0:
            return False
        
        self.board[row][col] = self.current_player
        self.current_player = 3 - self.current_player  # 切换玩家
        return True
    
    def check_winner(self) -> int:
        """
        检查获胜者
        
        Returns:
            0: 游戏进行中或平局
            1: X获胜
            2: O获胜
        """
        # 检查行
        for row in self.board:
            if row[0] == row[1] == row[2] != 0:
                return row[0]
        
        # 检查列
        for j in range(3):
            if self.board[0][j] == self.board[1][j] == self.board[2][j] != 0:
                return self.board[0][j]
        
        # 检查对角线
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != 0:
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != 0:
            return self.board[0][2]
        
        return 0
    
    def is_game_over(self) -> bool:
        """游戏是否结束"""
        return self.check_winner() != 0 or len(self.get_valid_moves()) == 0
    
    def minimax(self, depth: int, is_maximizing: bool, 
                alpha: float = float('-inf'), 
                beta: float = float('inf')) -> int:
        """Minimax评估函数"""
        winner = self.check_winner()
        
        if winner == 1:
            return 10 - depth
        elif winner == 2:
            return depth - 10
        elif len(self.get_valid_moves()) == 0:
            return 0
        
        if is_maximizing:
            max_eval = float('-inf')
            for move in self.get_valid_moves():
                game = self.clone()
                game.make_move(move[0], move[1])
                eval_score = game.minimax(depth + 1, False, alpha, beta)
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in self.get_valid_moves():
                game = self.clone()
                game.make_move(move[0], move[1])
                eval_score = game.minimax(depth + 1, True, alpha, beta)
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
            return min_eval
    
    def get_best_move(self) -> Optional[Tuple[int, int]]:
        """获取AI最佳移动"""
        best_move = None
        best_score = float('-inf') if self.current_player == 1 else float('inf')
        
        for move in self.get_valid_moves():
            game = self.clone()
            game.make_move(move[0], move[1])
            score = game.minimax(0, self.current_player == 2)
            
            if self.current_player == 1:
                if score > best_score:
                    best_score = score
                    best_move = move
            else:
                if score < best_score:
                    best_score = score
                    best_move = move
        
        return best_move
    
    def to_string(self) -> str:
        """转换为字符串表示"""
        symbols = {0: ' ', 1: 'X', 2: 'O'}
        lines = []
        for row in self.board:
            lines.append('|' + '|'.join(symbols[cell] for cell in row) + '|')
        return '\n'.join(lines)


class AuctionMechanism(ABC):
    """拍卖机制抽象基类"""
    
    @abstractmethod
    def run(self, bids: List[float]) -> Dict:
        """
        运行拍卖
        
        Args:
            bids: 所有竞拍者的出价列表
        
        Returns:
            拍卖结果字典
        """
        pass


class VickreyAuction(AuctionMechanism):
    """
    维克瑞拍卖（第二价格密封拍卖）
    
    获胜者支付第二高价，鼓励真实出价。
    """
    
    def __init__(self, reserve_price: float = 0):
        """
        Args:
            reserve_price: 保留价格（底价）
        """
        self.reserve_price = reserve_price
    
    def run(self, bids: List[float]) -> Dict:
        """
        运行维克瑞拍卖
        
        Returns:
            {
                "winner": 获胜者索引,
                "winning_bid": 获胜出价,
                "payment": 支付金额（第二高价或保留价）,
                "second_highest": 第二高价,
                "revenue": 拍卖收入,
                "bids": 所有出价
            }
        """
        if not bids:
            return {
                "winner": None,
                "winning_bid": None,
                "payment": None,
                "second_highest": None,
                "revenue": 0,
                "bids": bids
            }
        
        # 过滤低于保留价的出价
        valid_bids = [(i, b) for i, b in enumerate(bids) if b >= self.reserve_price]
        
        if not valid_bids:
            return {
                "winner": None,
                "winning_bid": None,
                "payment": None,
                "second_highest": None,
                "revenue": 0,
                "bids": bids
            }
        
        # 按出价排序
        sorted_bids = sorted(valid_bids, key=lambda x: x[1], reverse=True)
        
        winner = sorted_bids[0][0]
        winning_bid = sorted_bids[0][1]
        
        # 支付第二高价或保留价（取较高者）
        if len(sorted_bids) > 1:
            second_highest = sorted_bids[1][1]
        else:
            second_highest = self.reserve_price
        
        payment = max(second_highest, self.reserve_price)
        
        return {
            "winner": winner,
            "winning_bid": winning_bid,
            "payment": payment,
            "second_highest": second_highest,
            "revenue": payment,
            "bids": bids,
            "reserve_price": self.reserve_price
        }


class EnglishAuction(AuctionMechanism):
    """
    英式拍卖（公开增价拍卖）
    
    模拟英式拍卖的动态过程。
    """
    
    def __init__(self, reserve_price: float = 0, 
                 increment: float = 1,
                 max_rounds: int = 100):
        """
        Args:
            reserve_price: 起拍价（保留价）
            increment: 每次加价幅度
            max_rounds: 最大轮次
        """
        self.reserve_price = reserve_price
        self.increment = increment
        self.max_rounds = max_rounds
    
    def run(self, bids: List[float]) -> Dict:
        """
        模拟英式拍卖
        
        假设每个竞拍者有最高心理价位（即其密封出价）。
        """
        if not bids:
            return {
                "winner": None,
                "final_price": None,
                "rounds": 0,
                "bids": bids
            }
        
        current_price = self.reserve_price
        active_bidders = list(range(len(bids)))
        bid_history = []
        
        for round_num in range(self.max_rounds):
            # 找出愿意在当前价格出价的竞拍者
            willing = [i for i in active_bidders if bids[i] >= current_price]
            
            if len(willing) == 0:
                break
            elif len(willing) == 1:
                # 只剩一人愿意出价，拍卖结束
                winner = willing[0]
                bid_history.append({
                    "round": round_num,
                    "price": current_price,
                    "active_bidders": willing
                })
                return {
                    "winner": winner,
                    "final_price": current_price,
                    "winning_bid": bids[winner],
                    "rounds": round_num + 1,
                    "bid_history": bid_history,
                    "bids": bids
                }
            
            # 多人愿意出价，提高价格
            bid_history.append({
                "round": round_num,
                "price": current_price,
                "active_bidders": willing
            })
            current_price += self.increment
        
        # 达到最大轮次，最高出价者获胜
        sorted_bidders = sorted(active_bidders, key=lambda i: bids[i], reverse=True)
        winner = sorted_bidders[0]
        
        return {
            "winner": winner,
            "final_price": current_price,
            "winning_bid": bids[winner],
            "rounds": self.max_rounds,
            "bid_history": bid_history,
            "bids": bids
        }


class DutchAuction(AuctionMechanism):
    """
    荷式拍卖（公开降价拍卖）
    
    价格从高到低递减，第一个接受的竞拍者获胜。
    """
    
    def __init__(self, start_price: float, 
                 decrement: float = 1,
                 reserve_price: float = 0):
        """
        Args:
            start_price: 起始价格
            decrement: 每次降价幅度
            reserve_price: 保留价格
        """
        self.start_price = start_price
        self.decrement = decrement
        self.reserve_price = reserve_price
    
    def run(self, bids: List[float]) -> Dict:
        """
        模拟荷式拍卖
        
        假设竞拍者会在价格降到其心理价位时接受。
        第一个接受的人获胜。
        """
        if not bids:
            return {
                "winner": None,
                "winning_price": None,
                "bids": bids
            }
        
        current_price = self.start_price
        price_history = []
        
        while current_price >= self.reserve_price:
            # 找出愿意接受当前价格的竞拍者
            willing = [(i, bids[i]) for i in range(len(bids)) 
                      if bids[i] >= current_price]
            
            price_history.append({
                "price": current_price,
                "willing_count": len(willing)
            })
            
            if willing:
                # 第一个愿意接受的获胜
                # 随机选择一个（模拟第一个反应）
                winner = random.choice(willing)[0]
                return {
                    "winner": winner,
                    "winning_price": current_price,
                    "winning_bid": bids[winner],
                    "price_history": price_history,
                    "bids": bids
                }
            
            current_price -= self.decrement
        
        return {
            "winner": None,
            "winning_price": None,
            "price_history": price_history,
            "bids": bids
        }


class DominantStrategyDetector:
    """优势策略检测器"""
    
    @staticmethod
    def find_dominant_strategies(matrix: PayoffMatrix, 
                                  player: int) -> Dict:
        """
        寻找优势策略
        
        Args:
            matrix: 支付矩阵
            player: 玩家编号 (0或1)
        
        Returns:
            {
                "dominant": 优势策略列表,
                "dominated": 劣势策略列表,
                "strategy_types": 各策略类型
            }
        """
        if player == 0:
            payoffs = matrix.player1_payoffs
            num_strategies = matrix.rows
            opponent_strategies = matrix.cols
        else:
            payoffs = matrix.player2_payoffs
            num_strategies = matrix.cols
            opponent_strategies = matrix.rows
        
        dominant = []
        dominated = []
        strategy_types = {}
        
        for s1 in range(num_strategies):
            is_dominant = True
            is_dominated = True
            
            for s2 in range(num_strategies):
                if s1 == s2:
                    continue
                
                # 检查s1是否支配s2
                s1_dominates_s2 = True
                s2_dominates_s1 = True
                
                for opp in range(opponent_strategies):
                    if player == 0:
                        payoff_s1 = payoffs[s1][opp]
                        payoff_s2 = payoffs[s2][opp]
                    else:
                        payoff_s1 = payoffs[opp][s1]
                        payoff_s2 = payoffs[opp][s2]
                    
                    if payoff_s1 < payoff_s2:
                        s1_dominates_s2 = False
                    if payoff_s2 < payoff_s1:
                        s2_dominates_s1 = False
                
                if s2_dominates_s1:
                    is_dominant = False
                if s1_dominates_s2:
                    is_dominated = False
            
            if is_dominant:
                dominant.append(s1)
                strategy_types[s1] = StrategyType.DOMINANT.value
            elif is_dominated:
                dominated.append(s1)
                strategy_types[s1] = StrategyType.DOMINATED.value
            else:
                strategy_types[s1] = StrategyType.PURE.value
        
        return {
            "dominant": dominant,
            "dominated": dominated,
            "strategy_types": strategy_types
        }
    
    @staticmethod
    def iterated_elimination(matrix: PayoffMatrix) -> PayoffMatrix:
        """
        迭代消除劣势策略
        
        返回简化后的支付矩阵。
        """
        current_matrix = deepcopy(matrix)
        
        while True:
            eliminated = False
            
            # 检查玩家1的劣势策略
            result1 = DominantStrategyDetector.find_dominant_strategies(
                current_matrix, 0)
            
            if result1["dominated"]:
                # 消除第一个劣势策略
                idx = result1["dominated"][0]
                current_matrix.player1_payoffs.pop(idx)
                current_matrix.player1_strategies.pop(idx)
                eliminated = True
                continue
            
            # 检查玩家2的劣势策略
            result2 = DominantStrategyDetector.find_dominant_strategies(
                current_matrix, 1)
            
            if result2["dominated"]:
                idx = result2["dominated"][0]
                for row in current_matrix.player1_payoffs:
                    row.pop(idx)
                current_matrix.player2_strategies.pop(idx)
                eliminated = True
                continue
            
            if not eliminated:
                break
        
        return current_matrix


class ParetoAnalyzer:
    """帕累托效率分析器"""
    
    @staticmethod
    def find_pareto_optimal(matrix: PayoffMatrix) -> List[Tuple[int, int]]:
        """
        寻找所有帕累托最优策略组合
        
        帕累托最优：没有任何其他组合能让所有玩家至少一样好，且至少一人更好。
        """
        pareto_optimal = []
        all_payoffs = []
        
        # 收集所有支付组合
        for i in range(matrix.rows):
            for j in range(matrix.cols):
                all_payoffs.append(((i, j), matrix.get_payoff(i, j)))
        
        # 检查每个组合
        for (strategy, payoff) in all_payoffs:
            is_pareto = True
            
            for (_, other_payoff) in all_payoffs:
                # 检查other_payoff是否帕累托优于payoff
                if (other_payoff[0] >= payoff[0] and 
                    other_payoff[1] >= payoff[1] and
                    (other_payoff[0] > payoff[0] or 
                     other_payoff[1] > payoff[1])):
                    is_pareto = False
                    break
            
            if is_pareto:
                pareto_optimal.append(strategy)
        
        return pareto_optimal
    
    @staticmethod
    def find_pareto_frontier(matrix: PayoffMatrix) -> List[Tuple[float, float]]:
        """
        找出帕累托前沿（支付空间中的帕累托最优点）
        """
        pareto_strategies = ParetoAnalyzer.find_pareto_optimal(matrix)
        frontier = [matrix.get_payoff(i, j) for i, j in pareto_strategies]
        
        # 按玩家1的支付排序
        frontier.sort(key=lambda x: x[0])
        
        return frontier


class ShapleyValue:
    """
    夏普利值计算器
    
    用于合作博弈中公平分配收益。
    """
    
    @staticmethod
    def calculate(players: List[str], 
                   characteristic_function: Callable[[Set[str]], float]) -> Dict[str, float]:
        """
        计算每个玩家的夏普利值
        
        Args:
            players: 玩家列表
            characteristic_function: 特征函数，给定联盟返回联盟价值
        
        Returns:
            每个玩家的夏普利值
        """
        from itertools import permutations
        
        n = len(players)
        shapley_values = {p: 0 for p in players}
        
        # 遍历所有排列
        for perm in permutations(players):
            coalition = set()
            for i, player in enumerate(perm):
                # 计算边际贡献
                value_without = characteristic_function(coalition)
                coalition.add(player)
                value_with = characteristic_function(coalition)
                marginal_contribution = value_with - value_without
                shapley_values[player] += marginal_contribution
        
        # 平均
        factorial_n = math.factorial(n)
        for player in players:
            shapley_values[player] /= factorial_n
        
        return shapley_values
    
    @staticmethod
    def calculate_simple(players: List[str],
                         contributions: Dict[Tuple[str, ...], float]) -> Dict[str, float]:
        """
        简化版夏普利值计算（使用预定义的联盟贡献值）
        
        Args:
            players: 玩家列表
            contributions: 联盟到价值的映射（键为联盟元组）
        """
        from itertools import combinations
        
        n = len(players)
        shapley_values = {p: 0 for p in players}
        
        for player in players:
            # 计算该玩家的夏普利值
            other_players = [p for p in players if p != player]
            
            for size in range(len(other_players) + 1):
                for coalition in combinations(other_players, size):
                    coalition_set = set(coalition)
                    
                    # 联盟大小为size
                    weight = math.factorial(size) * math.factorial(n - size - 1) / math.factorial(n)
                    
                    coalition_key = tuple(sorted(coalition))
                    coalition_with_player_key = tuple(sorted(coalition + (player,)))
                    
                    value_without = contributions.get(coalition_key, 0)
                    value_with = contributions.get(coalition_with_player_key, 0)
                    
                    shapley_values[player] += weight * (value_with - value_without)
        
        return shapley_values


# 便捷函数
def create_prisoners_dilemma() -> PrisonersDilemma:
    """创建标准囚徒困境"""
    return PrisonersDilemma()


def solve_nash(matrix: PayoffMatrix) -> List[NashEquilibrium]:
    """求解纳什均衡的便捷函数"""
    return NashEquilibriumSolver.find_all_nash(matrix)


def analyze_game(matrix: PayoffMatrix) -> Dict:
    """
    全面分析博弈
    
    包含纳什均衡、帕累托最优、优势策略等。
    """
    nash_equilibria = NashEquilibriumSolver.find_all_nash(matrix)
    pareto_optimal = ParetoAnalyzer.find_pareto_optimal(matrix)
    dominant_p1 = DominantStrategyDetector.find_dominant_strategies(matrix, 0)
    dominant_p2 = DominantStrategyDetector.find_dominant_strategies(matrix, 1)
    
    return {
        "nash_equilibria": [eq.to_dict() for eq in nash_equilibria],
        "pareto_optimal": [
            {
                "strategy": (i, j),
                "payoff": matrix.get_payoff(i, j)
            }
            for i, j in pareto_optimal
        ],
        "player1_dominant_strategies": dominant_p1,
        "player2_dominant_strategies": dominant_p2,
        "is_zero_sum": matrix.is_zero_sum(),
        "game_info": {
            "player1_strategies": matrix.player1_strategies,
            "player2_strategies": matrix.player2_strategies,
            "num_strategies": (matrix.rows, matrix.cols)
        }
    }


if __name__ == "__main__":
    # 快速测试
    print("=== 囚徒困境分析 ===")
    pd = PrisonersDilemma()
    print(f"是否有效囚徒困境: {pd.is_valid_dilemma()}")
    print(f"分析结果: {pd.analyze()}")
    
    print("\n=== 纳什均衡求解 ===")
    matrix = PayoffMatrix(
        player1_payoffs=[[3, 0], [5, 1]],
        player2_payoffs=[[3, 5], [0, 1]],
        player1_strategies=["合作", "背叛"],
        player2_strategies=["合作", "背叛"]
    )
    equilibria = solve_nash(matrix)
    for eq in equilibria:
        print(f"均衡: {eq.to_dict()}")
    
    print("\n=== 井字棋AI ===")
    game = TicTacToe()
    game.make_move(0, 0)  # X
    game.make_move(1, 1)  # O
    print(game.to_string())
    print(f"最佳移动: {game.get_best_move()}")
    
    print("\n=== 维克瑞拍卖 ===")
    auction = VickreyAuction(reserve_price=10)
    result = auction.run([25, 18, 30, 22])
    print(f"拍卖结果: {result}")
"""
Game Theory Utils 测试模块
==========================

测试所有博弈论工具功能。
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    PayoffMatrix, NashEquilibrium, NashEquilibriumSolver,
    PrisonersDilemma, GameTreeNode, MinimaxSolver,
    TicTacToe, VickreyAuction, EnglishAuction, DutchAuction,
    DominantStrategyDetector, ParetoAnalyzer, ShapleyValue,
    solve_nash, analyze_game, create_prisoners_dilemma
)


def test_payoff_matrix():
    """测试支付矩阵"""
    print("=== 测试支付矩阵 ===")
    
    # 创建简单的支付矩阵
    matrix = PayoffMatrix(
        player1_payoffs=[[3, 0], [5, 1]],
        player2_payoffs=[[3, 5], [0, 1]],
        player1_strategies=["上", "下"],
        player2_strategies=["左", "右"]
    )
    
    assert matrix.rows == 2
    assert matrix.cols == 2
    assert matrix.get_payoff(0, 0) == (3, 3)
    assert matrix.get_payoff(1, 1) == (1, 1)
    assert not matrix.is_zero_sum()
    
    # 测试零和博弈
    zero_sum = PayoffMatrix(
        player1_payoffs=[[1, -1], [-1, 1]],
        player2_payoffs=[[-1, 1], [1, -1]]
    )
    assert zero_sum.is_zero_sum()
    
    print("✓ 支付矩阵测试通过")


def test_nash_equilibrium():
    """测试纳什均衡求解"""
    print("\n=== 测试纳什均衡求解 ===")
    
    # 测试囚徒困境
    pd_matrix = PayoffMatrix(
        player1_payoffs=[[-1, -10], [0, -5]],
        player2_payoffs=[[-1, 0], [-10, -5]],
        player1_strategies=["合作", "背叛"],
        player2_strategies=["合作", "背叛"]
    )
    
    pure_nash = NashEquilibriumSolver.find_pure_nash(pd_matrix)
    assert len(pure_nash) == 1
    assert pure_nash[0].player1_strategy == 1  # 背叛
    assert pure_nash[0].player2_strategy == 1  # 背叛
    print(f"囚徒困境纳什均衡: {pure_nash[0].to_dict()}")
    
    # 测试协调博弈（两个纯策略均衡）
    coordination = PayoffMatrix(
        player1_payoffs=[[2, 0], [0, 1]],
        player2_payoffs=[[2, 0], [0, 1]],
        player1_strategies=["歌剧", "足球"],
        player2_strategies=["歌剧", "足球"]
    )
    
    equilibria = NashEquilibriumSolver.find_pure_nash(coordination)
    assert len(equilibria) == 2
    print(f"协调博弈均衡数量: {len(equilibria)}")
    
    # 测试混合策略均衡（匹配硬币）
    matching = PayoffMatrix(
        player1_payoffs=[[1, -1], [-1, 1]],
        player2_payoffs=[[-1, 1], [1, -1]]
    )
    
    mixed = NashEquilibriumSolver.find_mixed_nash_2x2(matching)
    assert mixed is not None
    assert abs(mixed.player1_mixed[0] - 0.5) < 0.01
    assert abs(mixed.player2_mixed[0] - 0.5) < 0.01
    print(f"匹配硬币混合策略: {mixed.to_dict()}")
    
    print("✓ 纳什均衡测试通过")


def test_prisoners_dilemma():
    """测试囚徒困境"""
    print("\n=== 测试囚徒困境 ===")
    
    pd = create_prisoners_dilemma()
    analysis = pd.analyze()
    
    assert analysis["is_valid_dilemma"]
    assert len(analysis["nash_equilibria"]) == 1
    assert analysis["dominant_strategy"] == "背叛"
    
    print(f"囚徒困境分析: {analysis}")
    
    # 测试重复博弈
    result = PrisonersDilemma.simulate_repeated(
        rounds=10,
        strategy1="tit_for_tat",
        strategy2="always_defect"
    )
    
    assert result["rounds"] == 10
    assert result["strategy1"] == "tit_for_tat"
    assert result["strategy2"] == "always_defect"
    print(f"重复囚徒困境结果: 玩家1={result['total_payoff1']}, 玩家2={result['total_payoff2']}")
    
    # Tit-for-tat vs Always Cooperate
    result2 = PrisonersDilemma.simulate_repeated(
        rounds=10,
        strategy1="tit_for_tat",
        strategy2="always_cooperate"
    )
    print(f"Tit-for-tat vs Always Cooperate: 玩家1={result2['total_payoff1']}, 玩家2={result2['total_payoff2']}")
    
    print("✓ 囚徒困境测试通过")


def test_minimax():
    """测试极小化极大算法"""
    print("\n=== 测试极小化极大算法 ===")
    
    # 构建简单的博弈树
    #      根节点 (玩家0)
    #     /        \
    #   A(玩家1)    B(玩家1)
    #   /    \      /    \
    #  3,2   1,4   2,1   4,3
    
    root = GameTreeNode(player=0, info="Root")
    
    node_a = GameTreeNode(player=1, info="A")
    node_a.children[0] = GameTreeNode(player=1, payoff=(3, 2), is_terminal=True)
    node_a.children[1] = GameTreeNode(player=1, payoff=(1, 4), is_terminal=True)
    
    node_b = GameTreeNode(player=1, info="B")
    node_b.children[0] = GameTreeNode(player=1, payoff=(2, 1), is_terminal=True)
    node_b.children[1] = GameTreeNode(player=1, payoff=(4, 3), is_terminal=True)
    
    root.children[0] = node_a
    root.children[1] = node_b
    
    solver = MinimaxSolver()
    value, action = solver.solve(root, maximizing_player=0)
    
    print(f"最优值: {value}, 最优行动: {action}")
    print(f"评估节点数: {solver.nodes_evaluated}")
    
    print("✓ 极小化极大测试通过")


def test_tic_tac_toe():
    """测试井字棋"""
    print("\n=== 测试井字棋 ===")
    
    game = TicTacToe()
    
    # 玩几步
    assert game.make_move(0, 0)  # X
    assert game.make_move(1, 1)  # O
    assert game.make_move(0, 1)  # X
    assert game.make_move(2, 2)  # O
    assert game.make_move(0, 2)  # X 获胜
    
    assert game.check_winner() == 1  # X获胜
    
    print(game.to_string())
    print(f"获胜者: X")
    
    # 测试AI
    game2 = TicTacToe()
    game2.make_move(0, 0)  # X
    game2.make_move(1, 1)  # O
    
    best_move = game2.get_best_move()
    print(f"AI推荐移动: {best_move}")
    assert best_move is not None
    
    print("✓ 井字棋测试通过")


def test_vickrey_auction():
    """测试维克瑞拍卖"""
    print("\n=== 测试维克瑞拍卖 ===")
    
    auction = VickreyAuction(reserve_price=10)
    
    # 测试正常拍卖
    result = auction.run([25, 18, 30, 22])
    assert result["winner"] == 2  # 出价30的获胜
    assert result["winning_bid"] == 30
    assert result["payment"] == 25  # 第二高价
    print(f"维克瑞拍卖结果: 获胜者={result['winner']}, 支付={result['payment']}")
    
    # 测试低于保留价
    result2 = auction.run([5, 8, 9])
    assert result2["winner"] is None
    print(f"低于保留价: {result2}")
    
    # 测试只有一个有效出价
    result3 = auction.run([5, 15])
    assert result3["winner"] == 1
    assert result3["payment"] == 10  # 保留价
    print(f"单一有效出价: 支付保留价={result3['payment']}")
    
    print("✓ 维克瑞拍卖测试通过")


def test_english_auction():
    """测试英式拍卖"""
    print("\n=== 测试英式拍卖 ===")
    
    auction = EnglishAuction(reserve_price=10, increment=5)
    
    result = auction.run([25, 18, 30, 22])
    assert result["winner"] is not None
    assert result["final_price"] >= 10
    print(f"英式拍卖结果: 获胜者={result['winner']}, 最终价格={result['final_price']}")
    print(f"竞拍轮次: {result['rounds']}")
    
    print("✓ 英式拍卖测试通过")


def test_dutch_auction():
    """测试荷式拍卖"""
    print("\n=== 测试荷式拍卖 ===")
    
    auction = DutchAuction(start_price=100, decrement=10, reserve_price=10)
    
    result = auction.run([25, 45, 30, 50])
    assert result["winner"] is not None
    print(f"荷式拍卖结果: 获胜者={result['winner']}, 获胜价格={result['winning_price']}")
    
    print("✓ 荷式拍卖测试通过")


def test_dominant_strategy():
    """测试优势策略检测"""
    print("\n=== 测试优势策略检测 ===")
    
    # 囚徒困境（背叛是优势策略）
    pd_matrix = PayoffMatrix(
        player1_payoffs=[[-1, -10], [0, -5]],
        player2_payoffs=[[-1, 0], [-10, -5]]
    )
    
    result = DominantStrategyDetector.find_dominant_strategies(pd_matrix, 0)
    assert 1 in result["dominant"]  # 背叛（索引1）是优势策略
    assert 0 in result["dominated"]  # 合作（索引0）是劣势策略
    print(f"囚徒困境玩家1优势策略: {result}")
    
    # 测试迭代消除
    reduced = DominantStrategyDetector.iterated_elimination(pd_matrix)
    print(f"消除劣势策略后: {reduced.player1_strategies}, {reduced.player2_strategies}")
    
    print("✓ 优势策略测试通过")


def test_pareto_analyzer():
    """测试帕累托分析"""
    print("\n=== 测试帕累托分析 ===")
    
    # 协调博弈
    matrix = PayoffMatrix(
        player1_payoffs=[[2, 0], [0, 1]],
        player2_payoffs=[[2, 0], [0, 1]]
    )
    
    pareto = ParetoAnalyzer.find_pareto_optimal(matrix)
    print(f"帕累托最优策略组合: {pareto}")
    
    frontier = ParetoAnalyzer.find_pareto_frontier(matrix)
    print(f"帕累托前沿: {frontier}")
    
    print("✓ 帕累托分析测试通过")


def test_shapley_value():
    """测试夏普利值"""
    print("\n=== 测试夏普利值 ===")
    
    # 三人合作博弈
    # 特征函数: 空集=0, 单人=0, 双人=100, 三人=150
    def char_func(coalition):
        coalition = frozenset(coalition)
        if len(coalition) == 0:
            return 0
        elif len(coalition) == 1:
            return 0
        elif len(coalition) == 2:
            return 100
        else:  # len == 3
            return 150
    
    players = ["A", "B", "C"]
    shapley = ShapleyValue.calculate(players, char_func)
    
    # 每个玩家的夏普利值应该相等（对称性）
    print(f"夏普利值: {shapley}")
    assert abs(shapley["A"] - shapley["B"]) < 0.01
    assert abs(shapley["A"] - shapley["C"]) < 0.01
    
    # 简化版计算
    contributions = {
        (): 0,
        ("A",): 0, ("B",): 0, ("C",): 0,
        ("A", "B"): 100, ("A", "C"): 100, ("B", "C"): 100,
        ("A", "B", "C"): 150
    }
    shapley2 = ShapleyValue.calculate_simple(players, contributions)
    print(f"简化版夏普利值: {shapley2}")
    
    print("✓ 夏普利值测试通过")


def test_analyze_game():
    """测试全面博弈分析"""
    print("\n=== 测试全面博弈分析 ===")
    
    matrix = PayoffMatrix(
        player1_payoffs=[[3, 0], [5, 1]],
        player2_payoffs=[[3, 5], [0, 1]],
        player1_strategies=["合作", "背叛"],
        player2_strategies=["合作", "背叛"]
    )
    
    analysis = analyze_game(matrix)
    
    assert "nash_equilibria" in analysis
    assert "pareto_optimal" in analysis
    assert "player1_dominant_strategies" in analysis
    assert "player2_dominant_strategies" in analysis
    
    print(f"博弈分析结果:")
    print(f"  纳什均衡: {analysis['nash_equilibria']}")
    print(f"  帕累托最优: {analysis['pareto_optimal']}")
    print(f"  是否零和: {analysis['is_zero_sum']}")
    
    print("✓ 全面分析测试通过")


def run_all_tests():
    """运行所有测试"""
    print("=" * 50)
    print("Game Theory Utils 测试套件")
    print("=" * 50)
    
    test_payoff_matrix()
    test_nash_equilibrium()
    test_prisoners_dilemma()
    test_minimax()
    test_tic_tac_toe()
    test_vickrey_auction()
    test_english_auction()
    test_dutch_auction()
    test_dominant_strategy()
    test_pareto_analyzer()
    test_shapley_value()
    test_analyze_game()
    
    print("\n" + "=" * 50)
    print("✓ 所有测试通过！")
    print("=" * 50)


if __name__ == "__main__":
    run_all_tests()
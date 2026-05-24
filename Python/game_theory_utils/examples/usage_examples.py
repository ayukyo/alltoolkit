"""
Game Theory Utils 使用示例
==========================

展示博弈论工具的各种应用场景。
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    PayoffMatrix, NashEquilibriumSolver, PrisonersDilemma,
    MinimaxSolver, GameTreeNode, TicTacToe,
    VickreyAuction, EnglishAuction, DutchAuction,
    DominantStrategyDetector, ParetoAnalyzer, ShapleyValue,
    analyze_game
)


def example_1_prisoners_dilemma():
    """示例1: 囚徒困境分析"""
    print("=" * 60)
    print("示例1: 囚徒困境分析")
    print("=" * 60)
    
    # 创建标准囚徒困境
    # 支付: (合作, 背叛)
    # 诱惑=0, 奖励=-1, 惩罚=-5, 冤大头=-10
    pd = PrisonersDilemma(
        temptation=0,     # 背叛诱惑
        reward=-1,        # 双方合作
        punishment=-5,    # 双方背叛
        sucker=-10        # 被背叛
    )
    
    print("\n囚徒困境支付矩阵:")
    print("              玩家2")
    print("           合作    背叛")
    print("玩家1 合作  (-1,-1)  (-10,0)")
    print("       背叛  (0,-10)  (-5,-5)")
    
    analysis = pd.analyze()
    print(f"\n是否满足囚徒困境条件: {analysis['is_valid_dilemma']}")
    print(f"优势策略: {analysis['dominant_strategy']}")
    print(f"纳什均衡: {analysis['nash_equilibria']}")
    print(f"帕累托最优组合: {analysis['pareto_optimal']}")
    
    print("\n洞察: 虽然合作对双方都更好，但理性选择是背叛！")
    print("这就是囚徒困境的核心矛盾。")


def example_2_repeated_prisoners_dilemma():
    """示例2: 重复囚徒困境"""
    print("\n" + "=" * 60)
    print("示例2: 重复囚徒困境 - 策略对比")
    print("=" * 60)
    
    strategies = [
        "always_cooperate",
        "always_defect",
        "tit_for_tat",
        "grim_trigger",
        "random"
    ]
    
    print("\n各策略10回合对抗结果:\n")
    print(f"{'策略1':<18} {'策略2':<18} {'得分1':>8} {'得分2':>8} {'胜者':>10}")
    print("-" * 70)
    
    for s1 in strategies:
        for s2 in strategies:
            if s1 >= s2:  # 避免重复
                continue
            result = PrisonersDilemma.simulate_repeated(
                rounds=10,
                strategy1=s1,
                strategy2=s2,
                temptation=5,
                reward=3,
                punishment=1,
                sucker=0
            )
            
            winner = "平局" if result['total_payoff1'] == result['total_payoff2'] else \
                     (s1.split('_')[0] if result['total_payoff1'] > result['total_payoff2'] 
                      else s2.split('_')[0])
            
            print(f"{s1:<18} {s2:<18} {result['total_payoff1']:>8.1f} {result['total_payoff2']:>8.1f} {winner:>10}")
    
    print("\n结论: Tit-for-tat（以牙还牙）在长期博弈中表现优异！")


def example_3_coordination_game():
    """示例3: 协调博弈（性别大战）"""
    print("\n" + "=" * 60)
    print("示例3: 协调博弈 - 性别大战")
    print("=" * 60)
    
    # 经典的性别大战博弈
    # 两人想一起活动，但对活动类型有不同偏好
    matrix = PayoffMatrix(
        player1_payoffs=[[2, 0], [0, 1]],
        player2_payoffs=[[1, 0], [0, 2]],
        player1_strategies=["歌剧", "足球"],
        player2_strategies=["歌剧", "足球"]
    )
    
    print("\n性别大战支付矩阵:")
    print("              玩家2")
    print("           歌剧    足球")
    print("玩家1 歌剧  (2,1)   (0,0)")
    print("       足球  (0,0)   (1,2)")
    
    analysis = analyze_game(matrix)
    
    print(f"\n纳什均衡数量: {len(analysis['nash_equilibria'])}")
    for i, eq in enumerate(analysis['nash_equilibria'], 1):
        if eq['is_pure'] and eq['player1_strategy'] is not None:
            print(f"  均衡{i}: 玩家1选择'{matrix.player1_strategies[eq['player1_strategy']]}'，"
                  f"玩家2选择'{matrix.player2_strategies[eq['player2_strategy']]}'")
            print(f"        支付: {eq['payoff']}")
        else:
            print(f"  均衡{i}: 混合策略")
            if eq['player1_mixed']:
                print(f"        玩家1混合: {eq['player1_mixed']}")
            if eq['player2_mixed']:
                print(f"        玩家2混合: {eq['player2_mixed']}")
    
    print("\n洞察: 存在两个纯策略纳什均衡，但双方偏好不同！")
    print("这展示了协调博弈的困境。")


def example_4_matching_pennies():
    """示例4: 匹配硬币博弈"""
    print("\n" + "=" * 60)
    print("示例4: 匹配硬币 - 混合策略均衡")
    print("=" * 60)
    
    # 零和博弈的经典例子
    matrix = PayoffMatrix(
        player1_payoffs=[[1, -1], [-1, 1]],
        player2_payoffs=[[-1, 1], [1, -1]],
        player1_strategies=["正面", "反面"],
        player2_strategies=["正面", "反面"]
    )
    
    print("\n匹配硬币支付矩阵:")
    print("              玩家2")
    print("           正面    反面")
    print("玩家1 正面  (1,-1)  (-1,1)")
    print("       反面  (-1,1)  (1,-1)")
    
    print(f"\n是否零和博弈: {matrix.is_zero_sum()}")
    
    # 纯策略均衡
    pure_nash = NashEquilibriumSolver.find_pure_nash(matrix)
    print(f"纯策略纳什均衡: {len(pure_nash)} 个")
    
    # 混合策略均衡
    mixed_nash = NashEquilibriumSolver.find_mixed_nash_2x2(matrix)
    print(f"\n混合策略纳什均衡:")
    print(f"  玩家1: 正面概率={mixed_nash.player1_mixed[0]:.2f}, 反面概率={mixed_nash.player1_mixed[1]:.2f}")
    print(f"  玩家2: 正面概率={mixed_nash.player2_mixed[0]:.2f}, 反面概率={mixed_nash.player2_mixed[1]:.2f}")
    print(f"  期望支付: {mixed_nash.payoff}")
    
    print("\n洞察: 零和博弈没有纯策略均衡，最佳策略是随机选择！")


def example_5_auction_comparison():
    """示例5: 拍卖机制对比"""
    print("\n" + "=" * 60)
    print("示例5: 拍卖机制对比")
    print("=" * 60)
    
    bids = [100, 80, 120, 95, 110]
    print(f"\n竞拍者出价: {bids}")
    
    # 维克瑞拍卖
    vickrey = VickreyAuction(reserve_price=50)
    vickrey_result = vickrey.run(bids)
    print(f"\n维克瑞拍卖（第二价格密封拍卖）:")
    print(f"  获胜者: 竞拍者{vickrey_result['winner']} (出价{vickrey_result['winning_bid']})")
    print(f"  支付金额: {vickrey_result['payment']} (第二高价)")
    
    # 英式拍卖
    english = EnglishAuction(reserve_price=50, increment=5)
    english_result = english.run(bids)
    print(f"\n英式拍卖（公开增价）:")
    print(f"  获胜者: 竞拍者{english_result['winner']}")
    print(f"  最终价格: {english_result['final_price']}")
    print(f"  竞拍轮次: {english_result['rounds']}")
    
    # 荷式拍卖
    dutch = DutchAuction(start_price=150, decrement=5, reserve_price=50)
    dutch_result = dutch.run(bids)
    print(f"\n荷式拍卖（公开降价）:")
    print(f"  获胜者: 竞拍者{dutch_result['winner']}")
    print(f"  获胜价格: {dutch_result['winning_price']}")
    
    print("\n洞察: 不同拍卖机制产生不同结果，各有利弊！")


def example_6_dominant_strategy():
    """示例6: 优势策略与迭代消除"""
    print("\n" + "=" * 60)
    print("示例6: 优势策略分析")
    print("=" * 60)
    
    # 一个有劣势策略的博弈
    matrix = PayoffMatrix(
        player1_payoffs=[
            [3, 2, 1],
            [4, 3, 2],
            [2, 1, 0]
        ],
        player2_payoffs=[
            [3, 4, 2],
            [2, 3, 1],
            [1, 2, 0]
        ],
        player1_strategies=["上", "中", "下"],
        player2_strategies=["左", "中", "右"]
    )
    
    print("\n原始博弈矩阵:")
    print("玩家1支付:")
    for i, row in enumerate(matrix.player1_payoffs):
        print(f"  {matrix.player1_strategies[i]}: {row}")
    
    # 检测优势策略
    p1_result = DominantStrategyDetector.find_dominant_strategies(matrix, 0)
    p2_result = DominantStrategyDetector.find_dominant_strategies(matrix, 1)
    
    print(f"\n玩家1策略分析:")
    print(f"  优势策略: {[matrix.player1_strategies[i] for i in p1_result['dominant']]}")
    print(f"  劣势策略: {[matrix.player1_strategies[i] for i in p1_result['dominated']]}")
    
    print(f"\n玩家2策略分析:")
    print(f"  优势策略: {[matrix.player2_strategies[i] for i in p2_result['dominant']]}")
    print(f"  劣势策略: {[matrix.player2_strategies[i] for i in p2_result['dominated']]}")
    
    # 迭代消除
    reduced = DominantStrategyDetector.iterated_elimination(matrix)
    print(f"\n迭代消除劣势策略后:")
    print(f"  玩家1剩余策略: {reduced.player1_strategies}")
    print(f"  玩家2剩余策略: {reduced.player2_strategies}")


def example_7_pareto_efficiency():
    """示例7: 帕累托效率分析"""
    print("\n" + "=" * 60)
    print("示例7: 帕累托效率分析")
    print("=" * 60)
    
    # 一个有多个帕累托最优结果的博弈
    matrix = PayoffMatrix(
        player1_payoffs=[
            [1, 4, 2],
            [3, 2, 4],
            [2, 3, 1]
        ],
        player2_payoffs=[
            [2, 1, 4],
            [1, 4, 2],
            [3, 2, 4]
        ],
        player1_strategies=["A", "B", "C"],
        player2_strategies=["X", "Y", "Z"]
    )
    
    print("\n支付矩阵:")
    for i in range(matrix.rows):
        print(f"  {matrix.player1_strategies[i]}: ", end="")
        for j in range(matrix.cols):
            p1, p2 = matrix.get_payoff(i, j)
            print(f"({p1},{p2}) ", end="")
        print()
    
    pareto_optimal = ParetoAnalyzer.find_pareto_optimal(matrix)
    print(f"\n帕累托最优策略组合:")
    for i, j in pareto_optimal:
        p1, p2 = matrix.get_payoff(i, j)
        print(f"  ({matrix.player1_strategies[i]}, {matrix.player2_strategies[j]}): 支付 ({p1}, {p2})")
    
    frontier = ParetoAnalyzer.find_pareto_frontier(matrix)
    print(f"\n帕累托前沿（支付空间）: {frontier}")
    
    print("\n洞察: 帕累托最优意味着无法在不损害他人的情况下改善自己。")


def example_8_shapley_value():
    """示例8: 夏普利值 - 合作博弈收益分配"""
    print("\n" + "=" * 60)
    print("示例8: 夏普利值 - 公平分配合作收益")
    print("=" * 60)
    
    # 机场跑道成本分摊问题
    # 三个航空公司需要不同长度的跑道
    # A需要小型跑道，B需要中型，C需要大型
    # 成本: 小型=100, 中型=150, 大型=200
    
    print("\n机场跑道成本分摊问题:")
    print("  航空公司A: 需要小型跑道，成本100")
    print("  航空公司B: 需要中型跑道，成本150")
    print("  航空公司C: 需要大型跑道，成本200")
    print("  联合建设大型跑道成本200（可满足所有需求）")
    
    # 定义联盟成本函数
    def airport_cost(coalition):
        coalition = frozenset(coalition)
        if "C" in coalition:
            return 200  # 需要大型跑道
        elif "B" in coalition:
            return 150  # 需要中型跑道
        elif "A" in coalition:
            return 100  # 需要小型跑道
        else:
            return 0  # 空联盟
    
    players = ["A", "B", "C"]
    shapley = ShapleyValue.calculate(players, airport_cost)
    
    print(f"\n夏普利值分摊:")
    print(f"  航空公司A应支付: {shapley['A']:.2f}")
    print(f"  航空公司B应支付: {shapley['B']:.2f}")
    print(f"  航空公司C应支付: {shapley['C']:.2f}")
    print(f"  总计: {sum(shapley.values()):.2f}")
    
    print("\n洞察: 夏普利值提供了公平的成本分摊方案！")


def example_9_tictactoe_ai():
    """示例9: 井字棋AI对战"""
    print("\n" + "=" * 60)
    print("示例9: 井字棋AI对战演示")
    print("=" * 60)
    
    game = TicTacToe()
    moves = [(0, 0), (1, 1), (0, 1), (2, 2), (0, 2)]
    
    print("\n人类(X) vs AI(O):")
    print("人类策略: 占领第一行")
    
    for i, move in enumerate(moves):
        if game.is_game_over():
            break
        
        if game.current_player == 1:  # X (人类)
            game.make_move(move[0], move[1])
            print(f"\n人类走: ({move[0]}, {move[1]})")
        else:  # O (AI)
            ai_move = game.get_best_move()
            if ai_move:
                game.make_move(ai_move[0], ai_move[1])
                print(f"AI走: ({ai_move[0]}, {ai_move[1]})")
        
        print(game.to_string())
    
    winner = game.check_winner()
    if winner == 1:
        print("\n人类(X)获胜！")
    elif winner == 2:
        print("\nAI(O)获胜！")
    else:
        print("\n平局！")


def example_10_minimax_game_tree():
    """示例10: Minimax算法演示"""
    print("\n" + "=" * 60)
    print("示例10: Minimax算法 - 博弈树搜索")
    print("=" * 60)
    
    # 构建一个简单的博弈树
    #         根(玩家0最大化)
    #        /          \
    #       A(玩家1最小化) B(玩家1最小化)
    #      /  \         /     \
    #    3    5       2       9
    
    root = GameTreeNode(player=0, info="根节点")
    
    node_a = GameTreeNode(player=1, info="节点A")
    node_a.children[0] = GameTreeNode(player=1, payoff=(3, -3), is_terminal=True)
    node_a.children[1] = GameTreeNode(player=1, payoff=(5, -5), is_terminal=True)
    
    node_b = GameTreeNode(player=1, info="节点B")
    node_b.children[0] = GameTreeNode(player=1, payoff=(2, -2), is_terminal=True)
    node_b.children[1] = GameTreeNode(player=1, payoff=(9, -9), is_terminal=True)
    
    root.children[0] = node_a
    root.children[1] = node_b
    
    print("\n博弈树结构:")
    print("         根(玩家0-最大化)")
    print("        /          \\")
    print("       A(玩家1)    B(玩家1)")
    print("      /  \\        /    \\")
    print("    叶3   叶5    叶2    叶9")
    
    solver = MinimaxSolver()
    
    print("\n无剪枝搜索:")
    solver.reset_counter()
    value1, action1 = solver.solve(root, maximizing_player=0, 
                                    alpha=float('-inf'), beta=float('inf'))
    nodes1 = solver.nodes_evaluated
    print(f"  最优值: {value1}, 最优行动: 选择{['A', 'B'][action1]}")
    print(f"  评估节点数: {nodes1}")
    
    print("\n算法解释:")
    print("  玩家0选择B → 玩家1选择最小值2")
    print("  结果: 最优值=2")


def main():
    """运行所有示例"""
    example_1_prisoners_dilemma()
    example_2_repeated_prisoners_dilemma()
    example_3_coordination_game()
    example_4_matching_pennies()
    example_5_auction_comparison()
    example_6_dominant_strategy()
    example_7_pareto_efficiency()
    example_8_shapley_value()
    example_9_tictactoe_ai()
    example_10_minimax_game_tree()
    
    print("\n" + "=" * 60)
    print("所有示例演示完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
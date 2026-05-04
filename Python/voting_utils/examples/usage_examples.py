"""
投票工具使用示例
展示各种投票方法的应用场景
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from voting_utils.mod import (
    PluralityVoting, RankedChoiceVoting, BordaCount,
    ApprovalVoting, CondorcetVoting, SingleTransferableVote,
    ScoreVoting, VotingSimulator
)


def example_1_simple_election():
    """
    示例1：简单选举
    使用简单多数投票决定获胜者
    """
    print("=" * 50)
    print("示例1：简单选举（简单多数投票）")
    print("=" * 50)
    
    # 模拟班级投票：选择班长
    candidates = ['张三', '李四', '王五', '赵六']
    ballots = [
        '张三', '张三', '李四', '张三',
        '李四', '王五', '张三', '李四',
        '王五', '王五', '赵六', '张三',
        '李四', '张三', '王五', '赵六',
    ]
    
    print(f"\n候选人: {candidates}")
    print(f"选票数: {len(ballots)}")
    
    winner, counts = PluralityVoting.vote(ballots)
    
    print(f"\n投票结果:")
    for candidate, votes in sorted(counts.items(), key=lambda x: -x[1]):
        bar = '█' * votes
        print(f"  {candidate}: {votes}票 {bar}")
    
    print(f"\n🏆 获胜者: {winner}")
    
    # 处理平局
    print("\n--- 平局处理示例 ---")
    tie_ballots = ['张三', '李四', '张三', '李四']
    winner, counts, ties = PluralityVoting.vote_with_tiebreaker(
        tie_ballots, 
        tiebreaker='alphabetical'
    )
    print(f"选票: {tie_ballots}")
    print(f"平局候选人: {ties}")
    print(f"获胜者（字母顺序）: {winner}")


def example_2_ranked_choice_election():
    """
    示例2：排序选择投票
    用于需要表达偏好的选举
    """
    print("\n" + "=" * 50)
    print("示例2：排序选择投票（即时决选）")
    print("=" * 50)
    
    # 模拟学生会选举
    candidates = ['小红', '小明', '小华', '小强']
    
    # 选民按偏好排序候选人
    ballots = [
        ['小红', '小明', '小华', '小强'],  # 选民1
        ['小红', '小华', '小明', '小强'],  # 选民2
        ['小明', '小华', '小红', '小强'],  # 选民3
        ['小华', '小明', '小红', '小强'],  # 选民4
        ['小明', '小红', '小华', '小强'],  # 选民5
        ['小红', '小明', '小华', '小强'],  # 选民6
        ['小强', '小华', '小明', '小红'],  # 选民7
        ['小华', '小明', '小红', '小强'],  # 选民8
    ]
    
    print(f"\n候选人: {candidates}")
    print(f"选票数: {len(ballots)}")
    
    winner, rounds = RankedChoiceVoting.vote(ballots, candidates)
    
    print(f"\n投票过程:")
    for i, round_info in enumerate(rounds, 1):
        print(f"\n  第 {i} 轮:")
        for candidate, votes in sorted(round_info['counts'].items(), key=lambda x: -x[1]):
            percentage = votes / round_info['total'] * 100
            bar = '█' * int(percentage / 5)
            print(f"    {candidate}: {votes}票 ({percentage:.1f}%) {bar}")
        if round_info['eliminated']:
            print(f"    已淘汰: {round_info['eliminated']}")
    
    print(f"\n🏆 最终获胜者: {winner}")


def example_3_borda_count():
    """
    示例3：波达计数
    用于体育比赛排名、学术评审等
    """
    print("\n" + "=" * 50)
    print("示例3：波达计数（排名积分制）")
    print("=" * 50)
    
    # 模拟评委打分
    candidates = ['项目A', '项目B', '项目C', '项目D']
    
    # 5位评委的排名
    ballots = [
        ['项目A', '项目B', '项目C', '项目D'],  # 评委1
        ['项目B', '项目A', '项目C', '项目D'],  # 评委2
        ['项目A', '项目C', '项目B', '项目D'],  # 评委3
        ['项目C', '项目A', '项目B', '项目D'],  # 评委4
        ['项目B', '项目C', '项目A', '项目D'],  # 评委5
    ]
    
    print(f"\n候选项目: {candidates}")
    print(f"评委数: {len(ballots)}")
    
    winner, scores, details = BordaCount.vote(ballots, candidates)
    
    print(f"\n计分方式: 标准波达（n-1, n-2, ..., 0）")
    print(f"候选人数量: {len(candidates)}")
    print(f"\n各项目总分:")
    for candidate, score in sorted(scores.items(), key=lambda x: -x[1]):
        bar = '█' * int(score / 2)
        print(f"  {candidate}: {score}分 {bar}")
    
    print(f"\n🏆 最高分: {winner}")
    
    # 道达尔制（Nauru制）
    print("\n--- 道达尔制（分数递减：1, 1/2, 1/3...）---")
    winner_d, scores_d, _ = BordaCount.vote(ballots, candidates, scoring='dowdall')
    for candidate, score in sorted(scores_d.items(), key=lambda x: -x[1]):
        print(f"  {candidate}: {score:.2f}分")
    print(f"🏆 最高分: {winner_d}")


def example_4_approval_voting():
    """
    示例4：批准投票
    用于选出多个合格候选人
    """
    print("\n" + "=" * 50)
    print("示例4：批准投票（可多选）")
    print("=" * 50)
    
    # 模拟选择最佳员工
    candidates = ['员工甲', '员工乙', '员工丙', '员工丁']
    
    # 每个评委可以批准多个候选人
    ballots = [
        ['员工甲', '员工乙'],           # 评委1
        ['员工乙', '员工丙'],           # 评委2
        ['员工甲', '员工丙', '员工丁'], # 评委3
        ['员工乙'],                    # 评委4
        ['员工甲', '员工乙', '员工丁'], # 评委5
        ['员工丙', '员工丁'],          # 评委6
    ]
    
    print(f"\n候选员工: {candidates}")
    print(f"评委数: {len(ballots)}")
    
    winner, approvals = ApprovalVoting.vote(ballots, candidates)
    
    print(f"\n各员工批准数:")
    for candidate, votes in sorted(approvals.items(), key=lambda x: -x[1]):
        bar = '█' * votes
        print(f"  {candidate}: {votes}票 {bar}")
    
    print(f"\n🏆 最高批准: {winner}")
    
    # 选出所有达到阈值的员工
    print("\n--- 选出批准数≥3的员工 ---")
    winners, _ = ApprovalVoting.vote_with_threshold(ballots, threshold=3)
    print(f"达标员工: {winners}")


def example_5_condorcet_voting():
    """
    示例5：孔多塞投票
    用于需要公平比较的场景
    """
    print("\n" + "=" * 50)
    print("示例5：孔多塞投票（一对一对决）")
    print("=" * 50)
    
    # 模拟政策选择
    candidates = ['方案A', '方案B', '方案C']
    
    ballots = [
        ['方案A', '方案B', '方案C'],
        ['方案A', '方案C', '方案B'],
        ['方案B', '方案A', '方案C'],
        ['方案B', '方案C', '方案A'],
        ['方案C', '方案A', '方案B'],
        ['方案C', '方案B', '方案A'],
    ]
    
    print(f"\n候选方案: {candidates}")
    print(f"选票数: {len(ballots)}")
    
    # 先检查是否有孔多塞赢家
    condorcet_winner = CondorcetVoting.find_condorcet_winner(ballots)
    print(f"\n孔多塞赢家检查: {condorcet_winner if condorcet_winner else '无（存在循环偏好）'}")
    
    # 使用Schulze方法
    winner, preferences, ranking = CondorcetVoting.vote(ballots)
    
    print(f"\n一对一对决矩阵:")
    print("      ", end="")
    for c in candidates:
        print(f"{c:>6}", end="")
    print()
    
    for c1 in candidates:
        print(f"{c1:>6}", end="")
        for c2 in candidates:
            if c1 == c2:
                print(f"{'-':>6}", end="")
            else:
                pref = preferences.get((c1, c2), 0)
                print(f"{pref:>6}", end="")
        print()
    
    print(f"\n📊 Schulze排名: {' > '.join(ranking)}")
    print(f"🏆 获胜者: {winner}")
    
    # 另一个场景：明确的孔多塞赢家
    print("\n--- 明确孔多塞赢家示例 ---")
    clear_ballots = [
        ['方案A', '方案B', '方案C'],
        ['方案A', '方案C', '方案B'],
        ['方案B', '方案A', '方案C'],
        ['方案C', '方案A', '方案B'],
    ]
    # 方案A vs 方案B: 3-1
    # 方案A vs 方案C: 3-1
    # 方案B vs 方案C: 2-2
    
    winner = CondorcetVoting.find_condorcet_winner(clear_ballots)
    print(f"孔多塞赢家: {winner}")


def example_6_stv():
    """
    示例6：单记可转移投票（STV）
    用于多席位选举
    """
    print("\n" + "=" * 50)
    print("示例6：STV（多席位选举）")
    print("=" * 50)
    
    # 模拟董事会选举：3个席位
    candidates = ['候选人A', '候选人B', '候选人C', '候选人D', '候选人E']
    
    ballots = [
        ['候选人A', '候选人B', '候选人C'],
        ['候选人A', '候选人B', '候选人D'],
        ['候选人A', '候选人C', '候选人E'],
        ['候选人B', '候选人A', '候选人D'],
        ['候选人B', '候选人C', '候选人E'],
        ['候选人C', '候选人D', '候选人E'],
        ['候选人C', '候选人E', '候选人D'],
        ['候选人D', '候选人E', '候选人C'],
        ['候选人E', '候选人D', '候选人C'],
    ]
    
    print(f"\n候选人数: {len(candidates)}")
    print(f"席位: 3")
    print(f"选票数: {len(ballots)}")
    
    winners, stats = SingleTransferableVote.vote(ballots, seats=3)
    
    print(f"\nDroop配额: {stats['quota']}票（当选所需票数）")
    
    print(f"\n投票过程:")
    for i, round_info in enumerate(stats['rounds'], 1):
        print(f"\n  第 {i} 轮:")
        for candidate, votes in sorted(round_info['counts'].items(), key=lambda x: -x[1]):
            status = "✓" if candidate in round_info['elected'] else ""
            print(f"    {candidate}: {votes}票 {status}")
        if round_info['eliminated']:
            print(f"    已淘汰: {round_info['eliminated']}")
        if round_info['elected']:
            print(f"    已当选: {round_info['elected']}")
    
    print(f"\n🏆 当选者: {winners}")


def example_7_score_voting():
    """
    示例7：评分投票
    用于需要精细评价的场景
    """
    print("\n" + "=" * 50)
    print("示例7：评分投票（范围投票）")
    print("=" * 50)
    
    # 模拟产品评分
    products = ['产品A', '产品B', '产品C']
    
    # 用户打分（0-10分）
    ballots = [
        {'产品A': 9, '产品B': 7, '产品C': 5},
        {'产品A': 8, '产品B': 9, '产品C': 6},
        {'产品A': 7, '产品B': 8, '产品C': 8},
        {'产品A': 9, '产品B': 6, '产品C': 7},
        {'产品A': 6, '产品B': 8, '产品C': 9},
        {'产品A': 8, '产品B': 7, '产品C': 6},
    ]
    
    print(f"\n产品: {products}")
    print(f"评分范围: 0-10")
    print(f"评价者数: {len(ballots)}")
    
    winner, totals, avg = ScoreVoting.vote(ballots, max_score=10)
    
    print(f"\n各产品得分:")
    print(f"{'产品':<8} {'总分':<8} {'平均分':<8}")
    print("-" * 24)
    for candidate in sorted(totals.keys(), key=lambda x: -totals[x]):
        print(f"{candidate:<8} {totals[candidate]:<8} {avg[candidate]:.2f}")
    
    print(f"\n🏆 最高总分: {winner}")
    
    # 按平均分排名
    winner_avg, avg_scores = ScoreVoting.vote_by_average(ballots, max_score=10)
    print(f"🏆 最高平均分: {winner_avg}")


def example_8_compare_methods():
    """
    示例8：比较不同投票方法
    展示同一组选民偏好在不同方法下的结果
    """
    print("\n" + "=" * 50)
    print("示例8：不同投票方法比较")
    print("=" * 50)
    
    candidates = ['甲', '乙', '丙']
    
    # 选民偏好
    ranked_ballots = [
        ['甲', '乙', '丙']] * 35 + [
        ['乙', '丙', '甲']] * 25 + [
        ['丙', '乙', '甲']] * 40
    ]
    
    # 转换为其他格式
    plurality_ballots = [b[0] for b in ranked_ballots]
    approval_ballots = [b[:2] for b in ranked_ballots]  # 批准前两名
    
    print(f"\n选民偏好分布:")
    print(f"  35%: 甲 > 乙 > 丙")
    print(f"  25%: 乙 > 丙 > 甲")
    print(f"  40%: 丙 > 乙 > 甲")
    
    results = VotingSimulator.compare_methods(
        plurality_ballots,
        ranked_ballots,
        approval_ballots,
        [{}] * 100,  # 评分投票需要单独生成
        candidates
    )
    
    print(f"\n各方法结果:")
    method_names = {
        'plurality': '简单多数',
        'ranked_choice': '排序选择',
        'borda': '波达计数',
        'approval': '批准投票',
        'condorcet': '孔多塞',
        'score': '评分投票'
    }
    
    for method, winner in results.items():
        print(f"  {method_names.get(method, method)}: {winner if winner else '无'}")
    
    print("\n分析:")
    print("  - 简单多数：丙获胜（40%第一选择票）")
    print("  - 排序选择：乙获胜（甲淘汰后，乙获得丙的第二选择票）")
    print("  - 波达计数：乙获胜（综合排名最高）")
    print("  - 批准投票：乙或丙获胜（批准数最多）")


def example_9_simulate_large_election():
    """
    示例9：模拟大规模选举
    使用投票模拟器生成大规模数据
    """
    print("\n" + "=" * 50)
    print("示例9：模拟大规模选举")
    print("=" * 50)
    
    candidates = ['候选人A', '候选人B', '候选人C', '候选人D']
    
    print(f"\n候选人: {candidates}")
    print("选民数: 10000")
    
    # 生成正态分布偏好（中间候选人更受欢迎）
    plurality_ballots = VotingSimulator.generate_ballots_plurality(
        10000, candidates, 'normal', seed=42
    )
    
    ranked_ballots = VotingSimulator.generate_ballots_ranked(
        10000, candidates, 'normal', seed=42
    )
    
    # 简单多数结果
    winner_p, counts_p = PluralityVoting.vote(plurality_ballots)
    print(f"\n简单多数结果:")
    for c, v in sorted(counts_p.items(), key=lambda x: -x[1]):
        pct = v / 10000 * 100
        print(f"  {c}: {v}票 ({pct:.1f}%)")
    print(f"  获胜者: {winner_p}")
    
    # 排序选择结果
    winner_rc, rounds = RankedChoiceVoting.vote(ranked_ballots, candidates)
    print(f"\n排序选择结果:")
    print(f"  轮次: {len(rounds)}")
    print(f"  获胜者: {winner_rc}")
    
    # 孔多塞结果
    winner_c, _, ranking = CondorcetVoting.vote(ranked_ballots, candidates)
    print(f"\n孔多塞结果:")
    print(f"  获胜者: {winner_c}")
    print(f"  完整排名: {' > '.join(ranking)}")


def main():
    """运行所有示例"""
    print("=" * 60)
    print("投票工具使用示例")
    print("=" * 60)
    
    example_1_simple_election()
    example_2_ranked_choice_election()
    example_3_borda_count()
    example_4_approval_voting()
    example_5_condorcet_voting()
    example_6_stv()
    example_7_score_voting()
    example_8_compare_methods()
    example_9_simulate_large_election()
    
    print("\n" + "=" * 60)
    print("所有示例运行完成!")
    print("=" * 60)


if __name__ == '__main__':
    main()
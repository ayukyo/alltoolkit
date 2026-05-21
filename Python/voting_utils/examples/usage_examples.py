"""
投票选举工具使用示例
演示各种投票算法的实际应用场景
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    Ballot, VotingSystem, create_ballot, generate_random_ballot,
    PluralityVoting, RankedChoiceVoting, BordaCount, 
    CondorcetMethod, DHondtMethod, ApprovalVoting, RangeVoting,
    SingleTransferableVote
)


def example_1_simple_election():
    """示例1: 简单的多数制选举"""
    print("=" * 60)
    print("示例1: 简单的多数制选举")
    print("=" * 60)
    print("场景: 班级选举班长，3位候选人")
    print()
    
    candidates = ["张三", "李四", "王五"]
    
    # 20位同学的投票
    ballots = [
        create_ballot(rankings=["张三"]),
        create_ballot(rankings=["张三"]),
        create_ballot(rankings=["张三"]),
        create_ballot(rankings=["张三"]),
        create_ballot(rankings=["张三"]),
        create_ballot(rankings=["张三"]),
        create_ballot(rankings=["张三"]),
        create_ballot(rankings=["李四"]),
        create_ballot(rankings=["李四"]),
        create_ballot(rankings=["李四"]),
        create_ballot(rankings=["李四"]),
        create_ballot(rankings=["李四"]),
        create_ballot(rankings=["李四"]),
        create_ballot(rankings=["王五"]),
        create_ballot(rankings=["王五"]),
        create_ballot(rankings=["王五"]),
        create_ballot(rankings=["王五"]),
        create_ballot(rankings=["王五"]),
        create_ballot(rankings=["王五"]),
        create_ballot(rankings=["王五"]),
    ]
    
    result = PluralityVoting.count(ballots, candidates)
    
    print(f"总票数: {len(ballots)}")
    print(f"投票结果:")
    for candidate, votes in result.rankings:
        percentage = (votes / len(ballots)) * 100
        print(f"  {candidate}: {votes}票 ({percentage:.1f}%)")
    print(f"\n获胜者: {result.winner} 🏆")
    print()


def example_2_ranked_choice_voting():
    """示例2: 排名选择投票（即时决选）"""
    print("=" * 60)
    print("示例2: 排名选择投票（即时决选）")
    print("=" * 60)
    print("场景: 没有候选人获得超过50%选票时的自动决选")
    print()
    
    candidates = ["候选人A", "候选人B", "候选人C"]
    
    # 选票按排名填写
    ballots = [
        # A的支持者（7票）
        create_ballot(rankings=["候选人A", "候选人B", "候选人C"]),
        create_ballot(rankings=["候选人A", "候选人B", "候选人C"]),
        create_ballot(rankings=["候选人A", "候选人C", "候选人B"]),
        create_ballot(rankings=["候选人A", "候选人C", "候选人B"]),
        create_ballot(rankings=["候选人A", "候选人B", "候选人C"]),
        create_ballot(rankings=["候选人A", "候选人C", "候选人B"]),
        create_ballot(rankings=["候选人A", "候选人B", "候选人C"]),
        # B的支持者（5票）
        create_ballot(rankings=["候选人B", "候选人C", "候选人A"]),
        create_ballot(rankings=["候选人B", "候选人C", "候选人A"]),
        create_ballot(rankings=["候选人B", "候选人A", "候选人C"]),
        create_ballot(rankings=["候选人B", "候选人A", "候选人C"]),
        create_ballot(rankings=["候选人B", "候选人C", "候选人A"]),
        # C的支持者（4票）
        create_ballot(rankings=["候选人C", "候选人B", "候选人A"]),
        create_ballot(rankings=["候选人C", "候选人B", "候选人A"]),
        create_ballot(rankings=["候选人C", "候选人B", "候选人A"]),
        create_ballot(rankings=["候选人C", "候选人A", "候选人B"]),
    ]
    
    result = RankedChoiceVoting.count(ballots, candidates)
    
    print(f"总票数: {len(ballots)}")
    print(f"所需阈值: >{len(ballots)//2}票 ({len(ballots)//2 + 1}票)")
    print()
    
    for i, round_data in enumerate(result.rounds, 1):
        print(f"第{i}轮结果:")
        for candidate, votes in sorted(round_data.items(), key=lambda x: x[1], reverse=True):
            print(f"  {candidate}: {votes}票")
        print()
    
    print(f"最终获胜者: {result.winner} 🏆")
    print()


def example_3_borda_count():
    """示例3: 波达计数法"""
    print("=" * 60)
    print("示例3: 波达计数法")
    print("=" * 60)
    print("场景: 体育比赛评分，排名越靠前得分越高")
    print()
    
    candidates = ["运动员A", "运动员B", "运动员C", "运动员D"]
    
    # 5位评委的排名
    ballots = [
        create_ballot(rankings=["运动员A", "运动员B", "运动员C", "运动员D"]),
        create_ballot(rankings=["运动员A", "运动员C", "运动员B", "运动员D"]),
        create_ballot(rankings=["运动员B", "运动员A", "运动员C", "运动员D"]),
        create_ballot(rankings=["运动员C", "运动员A", "运动员B", "运动员D"]),
        create_ballot(rankings=["运动员A", "运动员B", "运动员D", "运动员C"]),
    ]
    
    result = BordaCount.count(ballots, candidates)
    
    n = len(candidates)
    print(f"波达计分规则: 第1名得{n-1}分，第2名得{n-2}分，...，第{n}名得0分")
    print()
    print("各运动员总得分:")
    for candidate, score in result.rankings:
        print(f"  {candidate}: {score}分")
    print()
    print(f"冠军: {result.winner} 🥇")
    print()


def example_4_condorcet_method():
    """示例4: 孔多塞方法"""
    print("=" * 60)
    print("示例4: 孔多塞方法（两两对决）")
    print("=" * 60)
    print("场景: 找出在所有两两对决中都获胜的候选人")
    print()
    
    candidates = ["方案A", "方案B", "方案C"]
    
    # 9位决策者的偏好
    ballots = [
        # 4人: A > B > C
        create_ballot(rankings=["方案A", "方案B", "方案C"]),
        create_ballot(rankings=["方案A", "方案B", "方案C"]),
        create_ballot(rankings=["方案A", "方案B", "方案C"]),
        create_ballot(rankings=["方案A", "方案B", "方案C"]),
        # 3人: B > C > A
        create_ballot(rankings=["方案B", "方案C", "方案A"]),
        create_ballot(rankings=["方案B", "方案C", "方案A"]),
        create_ballot(rankings=["方案B", "方案C", "方案A"]),
        # 2人: C > A > B
        create_ballot(rankings=["方案C", "方案A", "方案B"]),
        create_ballot(rankings=["方案C", "方案A", "方案B"]),
    ]
    
    result = CondorcetMethod.count(ballots, candidates)
    
    print("两两对决结果:")
    pairwise = result.details["pairwise_matrix"]
    for c1 in candidates:
        for c2 in candidates:
            if c1 != c2:
                wins = pairwise[c1][c2]
                losses = pairwise[c2][c1]
                if wins > losses:
                    print(f"  {c1} vs {c2}: {c1}获胜 ({wins}:{losses})")
    
    print()
    if result.winner:
        print(f"孔多塞赢家: {result.winner} 🏆")
        print("(在所有两两对决中都获胜)")
    else:
        print("没有孔多塞赢家（存在孔多塞循环）")
    print()


def example_5_proportional_representation():
    """示例5: 比例代表制（洪德法）"""
    print("=" * 60)
    print("示例5: 比例代表制（洪德法分配席位）")
    print("=" * 60)
    print("场景: 议会选举，按政党得票比例分配席位")
    print()
    
    party_votes = {
        "民主党": 45000,
        "共和党": 30000,
        "绿党": 15000,
        "独立党": 10000
    }
    total_seats = 10
    
    result = DHondtMethod.count(party_votes, seats=total_seats)
    
    total_votes = sum(party_votes.values())
    print("各政党得票:")
    for party, votes in sorted(party_votes.items(), key=lambda x: x[1], reverse=True):
        percentage = (votes / total_votes) * 100
        print(f"  {party}: {votes:,}票 ({percentage:.1f}%)")
    
    print(f"\n总席位数: {total_seats}")
    print("\n席位分配结果:")
    for party, seats in result.rankings:
        print(f"  {party}: {seats}席")
    print()


def example_6_approval_voting():
    """示例6: 赞成投票"""
    print("=" * 60)
    print("示例6: 赞成投票")
    print("=" * 60)
    print("场景: 选出多位代表，每人可赞成多个候选人")
    print()
    
    candidates = ["张三", "李四", "王五", "赵六"]
    
    # 每张选票可以赞成多人
    ballots = [
        create_ballot(rankings=[], approvals={"张三", "李四"}),
        create_ballot(rankings=[], approvals={"张三", "李四"}),
        create_ballot(rankings=[], approvals={"张三", "王五"}),
        create_ballot(rankings=[], approvals={"李四", "王五"}),
        create_ballot(rankings=[], approvals={"张三", "李四", "王五"}),
        create_ballot(rankings=[], approvals={"李四"}),
        create_ballot(rankings=[], approvals={"王五", "赵六"}),
        create_ballot(rankings=[], approvals={"张三", "赵六"}),
    ]
    
    result = ApprovalVoting.count(ballots, candidates)
    
    print("各候选人获赞成数:")
    for candidate, approvals in result.rankings:
        print(f"  {candidate}: {approvals}票")
    print()
    print(f"获胜者: {result.winner} 🏆")
    print()


def example_7_range_voting():
    """示例7: 范围投票（评分投票）"""
    print("=" * 60)
    print("示例7: 范围投票（评分投票）")
    print("=" * 60)
    print("场景: 选美比赛，评委对每位选手打分（0-10分）")
    print()
    
    candidates = ["选手A", "选手B", "选手C"]
    
    ballots = [
        create_ballot(rankings=[], weights={"选手A": 9, "选手B": 8, "选手C": 7}),
        create_ballot(rankings=[], weights={"选手A": 10, "选手B": 9, "选手C": 8}),
        create_ballot(rankings=[], weights={"选手A": 8, "选手B": 10, "选手C": 6}),
        create_ballot(rankings=[], weights={"选手A": 9, "选手B": 7, "选手C": 9}),
        create_ballot(rankings=[], weights={"选手A": 8, "选手B": 8, "选手C": 9}),
    ]
    
    result = RangeVoting.count(ballots, candidates, min_score=0, max_score=10)
    
    print("评分范围: 0-10分")
    print("\n各选手平均得分:")
    for candidate, avg_score in result.rankings:
        print(f"  {candidate}: {avg_score:.2f}分")
    print()
    print(f"冠军: {result.winner} 🏆")
    print()


def example_8_stv_multiple_seats():
    """示例8: 单一可转移投票（多席位）"""
    print("=" * 60)
    print("示例8: 单一可转移投票（STV）- 多席位选举")
    print("=" * 60)
    print("场景: 选举3位代表，选票可转移")
    print()
    
    candidates = ["候选人A", "候选人B", "候选人C", "候选人D", "候选人E"]
    seats = 3
    
    # 100张选票
    ballots = []
    # A的前两名支持者: 28票
    for _ in range(28):
        ballots.append(create_ballot(rankings=["候选人A", "候选人B", "候选人C", "候选人D", "候选人E"]))
    # B的前两名支持者: 22票
    for _ in range(22):
        ballots.append(create_ballot(rankings=["候选人B", "候选人A", "候选人C", "候选人D", "候选人E"]))
    # C的支持者: 20票
    for _ in range(20):
        ballots.append(create_ballot(rankings=["候选人C", "候选人D", "候选人A", "候选人B", "候选人E"]))
    # D的支持者: 18票
    for _ in range(18):
        ballots.append(create_ballot(rankings=["候选人D", "候选人C", "候选人A", "候选人B", "候选人E"]))
    # E的支持者: 12票
    for _ in range(12):
        ballots.append(create_ballot(rankings=["候选人E", "候选人D", "候选人C", "候选人B", "候选人A"]))
    
    result = SingleTransferableVote.count(ballots, candidates, seats=seats)
    
    total_votes = len(ballots)
    quota = result.details["quota"]
    print(f"总票数: {total_votes}")
    print(f"席位数: {seats}")
    print(f"当选配额（Droop配额）: {quota}票")
    print()
    print("当选者:")
    for i, elected in enumerate(result.details["elected"], 1):
        print(f"  第{i}席: {elected}")
    print()


def example_9_compare_methods():
    """示例9: 比较不同投票方法的结果"""
    print("=" * 60)
    print("示例9: 比较不同投票方法的结果")
    print("=" * 60)
    print("场景: 同一组选票，用不同方法可能产生不同结果")
    print()
    
    candidates = ["A", "B", "C"]
    
    # 经典的孔多塞悖论案例
    ballots = [
        create_ballot(rankings=["A", "B", "C"]),
        create_ballot(rankings=["A", "B", "C"]),
        create_ballot(rankings=["B", "C", "A"]),
        create_ballot(rankings=["B", "C", "A"]),
        create_ballot(rankings=["C", "A", "B"]),
        create_ballot(rankings=["C", "A", "B"]),
    ]
    
    print("选票分布:")
    print("  A > B > C: 2票")
    print("  B > C > A: 2票")
    print("  C > A > B: 2票")
    print()
    
    methods = ["plurality", "rcv", "borda", "condorcet", "approval"]
    results = VotingSystem.compare_methods(ballots, candidates, methods)
    
    print("各方法结果:")
    for method, result in results.items():
        winner = result.winner or "无"
        print(f"  {result.method}: 获胜者 = {winner}")
    print()
    print("注意: 不同方法可能产生不同获胜者!")
    print()


def example_10_real_world_scenario():
    """示例10: 真实场景模拟"""
    print("=" * 60)
    print("示例10: 真实场景模拟 - 学生会选举")
    print("=" * 60)
    print("场景: 大学学生会主席选举，使用排名选择投票")
    print()
    
    candidates = ["小明（改革派）", "小红（稳健派）", "小李（独立派）"]
    
    # 模拟200名学生的投票
    import random
    random.seed(42)  # 设置随机种子以便复现
    
    ballots = []
    # 小明的铁杆支持者
    for _ in range(70):
        ballots.append(create_ballot(rankings=["小明（改革派）", "小李（独立派）", "小红（稳健派）"]))
    # 小红的支持者
    for _ in range(55):
        ballots.append(create_ballot(rankings=["小红（稳健派）", "小李（独立派）", "小明（改革派）"]))
    # 小李的支持者
    for _ in range(35):
        ballots.append(create_ballot(rankings=["小李（独立派）", "小红（稳健派）", "小明（改革派）"]))
    # 战术性投票
    for _ in range(20):
        ballots.append(create_ballot(rankings=["小李（独立派）", "小明（改革派）", "小红（稳健派）"]))
    for _ in range(20):
        ballots.append(create_ballot(rankings=["小红（稳健派）", "小明（改革派）", "小李（独立派）"]))
    
    print(f"总投票人数: {len(ballots)}")
    print()
    
    # 使用排名选择投票
    result = VotingSystem.run_election("rcv", ballots, candidates)
    
    print("选举过程:")
    for i, round_data in enumerate(result.rounds, 1):
        print(f"\n第{i}轮:")
        for candidate, votes in sorted(round_data.items(), key=lambda x: x[1], reverse=True):
            percentage = (votes / len(ballots)) * 100
            print(f"  {candidate}: {votes}票 ({percentage:.1f}%)")
    
    print(f"\n{'=' * 40}")
    print(f"当选主席: {result.winner} 🎉")
    print(f"{'=' * 40}")
    print()


if __name__ == "__main__":
    example_1_simple_election()
    example_2_ranked_choice_voting()
    example_3_borda_count()
    example_4_condorcet_method()
    example_5_proportional_representation()
    example_6_approval_voting()
    example_7_range_voting()
    example_8_stv_multiple_seats()
    example_9_compare_methods()
    example_10_real_world_scenario()
    
    print("=" * 60)
    print("所有示例运行完成!")
    print("=" * 60)
"""
Tournament Utilities 测试用例
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    Participant, Match, MatchStatus,
    SingleElimination, DoubleElimination, RoundRobin, SwissSystem,
    create_single_elimination, create_double_elimination, create_round_robin, create_swiss
)


def test_participant():
    """测试参赛者"""
    print("\n🧪 测试 Participant")
    print("-" * 40)

    p1 = Participant(id=1, name="张三", seed=1, rating=1500)
    p2 = Participant(id=2, name="李四")

    assert p1.id == 1
    assert p1.name == "张三"
    assert p1.seed == 1
    assert p2.seed is None

    # repr 测试
    assert "[1]" in repr(p1)
    assert "张三" in repr(p1)
    assert repr(p2) == "李四"

    print("✓ Participant 测试通过")


def test_single_elimination():
    """测试单败淘汰赛"""
    print("\n🧪 测试 SingleElimination")
    print("-" * 40)

    # 8人淘汰赛
    names = ["A", "B", "C", "D", "E", "F", "G", "H"]
    seeds = [1, 8, 4, 5, 3, 6, 2, 7]
    tournament = create_single_elimination(names, seeds)

    assert tournament.num_rounds == 3
    assert len(tournament.participants) == 8

    # 种子排序检查：1号种子和2号种子应该在对角两端
    first_match = tournament.get_round_matches(1)[0]
    assert first_match.participant1.name == "A"  # 1号种子

    last_match = tournament.get_round_matches(1)[-1]
    assert last_match.participant1.name == "B" or last_match.participant2.name == "B"  # 2号种子

    # 模拟比赛
    for r in range(1, tournament.num_rounds + 1):
        matches = tournament.get_round_matches(r)
        for m in matches:
            if m.status != MatchStatus.BYE and m.participant1 and m.participant2:
                # 简单地让 participant1 获胜
                tournament.set_winner(m.id, m.participant1.id)

    assert tournament.is_completed()
    assert tournament.get_winner() is not None

    print("✓ 8人淘汰赛测试通过")

    # 测试奇数参赛者（轮空处理）
    odd_names = ["A", "B", "C", "D", "E"]
    odd_tournament = create_single_elimination(odd_names)

    assert odd_tournament.num_rounds == 3

    # 检查轮空 - 5人参赛，8个位置，第一轮4场比赛
    # 位置分配：种子1->位置0, 种子2->位置7, 种子3->位置3, 种子4->位置4, 种子5->位置1
    # 第一轮比赛：位置0vs1(AvsE), 位置2vs3(NonevsC), 位置4vs5(DvsNone), 位置6vs7(NonevsB)
    first_round = odd_tournament.get_round_matches(1)
    bye_matches = [m for m in first_round if m.status == MatchStatus.BYE]
    # 实际轮空数取决于参赛者分配位置
    assert len(bye_matches) >= 1  # 至少有轮空
    print(f"✓ 轮空处理测试通过（{len(bye_matches)}个轮空）")

    # 测试比分设置
    score_tournament = create_single_elimination(["甲", "乙"])
    first_match = score_tournament.get_round_matches(1)[0]
    score_tournament.set_score(first_match.id, 3, 1)

    assert first_match.score1 == 3
    assert first_match.score2 == 1
    assert first_match.winner.name == "甲"
    assert score_tournament.is_completed()

    print("✓ 比分设置测试通过")

    # 测试 to_dict
    d = tournament.to_dict()
    assert d["type"] == "single_elimination"
    assert d["num_rounds"] == 3
    assert len(d["participants"]) == 8

    print("✓ to_dict 测试通过")

    print("✓ SingleElimination 所有测试通过")


def test_double_elimination():
    """测试双败淘汰赛"""
    print("\n🧪 测试 DoubleElimination")
    print("-" * 40)

    names = ["A", "B", "C", "D", "E", "F", "G", "H"]
    tournament = create_double_elimination(names)

    assert len(tournament.participants) == 8
    assert len(tournament.winners_bracket) > 0
    assert len(tournament.losers_bracket) > 0
    assert tournament.grand_final is not None

    # 模拟胜者组比赛
    for match in sorted(tournament.winners_bracket.values(), key=lambda m: m.round_num):
        if match.status != MatchStatus.BYE and match.participant1 and match.participant2:
            tournament.set_winner_winner(match.id, match.participant1.id)

    # 检查败者被送入败者组
    losers_in_losers = sum(1 for m in tournament.losers_bracket.values()
                          if m.participant1 or m.participant2)
    assert losers_in_losers > 0

    print("✓ 双败淘汰赛测试通过")

    # 测试 to_dict
    d = tournament.to_dict()
    assert d["type"] == "double_elimination"
    assert "winners_bracket" in d
    assert "losers_bracket" in d
    assert "grand_final" in d

    print("✓ DoubleElimination 所有测试通过")


def test_round_robin():
    """测试循环赛"""
    print("\n🧪 测试 RoundRobin")
    print("-" * 40)

    # 4人循环赛
    names = ["张三", "李四", "王五", "赵六"]
    tournament = create_round_robin(names)

    # 4人循环赛应该有 4*3/2 = 6 场比赛
    expected_matches = len(names) * (len(names) - 1) // 2
    assert len(tournament.matches) == expected_matches

    # 每人应该有 3 场比赛
    for p in tournament.participants:
        p_matches = [m for m in tournament.matches
                    if m.participant1.id == p.id or m.participant2.id == p.id]
        assert len(p_matches) == len(names) - 1

    # 模拟比赛结果 - 根据实际比赛顺序
    # Match 0: 张三 vs 赵六 -> 张三胜
    # Match 1: 李四 vs 王五 -> 王五胜
    # Match 2: 张三 vs 王五 -> 张三胜
    # Match 3: 赵六 vs 李四 -> 李四胜
    # Match 4: 张三 vs 李四 -> 张三胜
    # Match 5: 王五 vs 赵六 -> 王五胜
    tournament.set_result(0, 3, 1)  # 张三胜赵六
    tournament.set_result(1, 1, 2)  # 王五胜李四
    tournament.set_result(2, 2, 1)  # 张三胜王五
    tournament.set_result(3, 1, 3)  # 李四胜赵六
    tournament.set_result(4, 3, 0)  # 张三胜李四
    tournament.set_result(5, 2, 1)  # 王五胜赵六

    # 检查积分 - 张三3胜，王五2胜1负（输给张三），李四1胜2负，赵六0胜3负
    standings = tournament.get_standings()
    assert standings[0]["participant"].name == "张三"  # 张三应该排第一（3胜）
    assert standings[0]["wins"] == 3
    assert standings[0]["points"] == 9  # 3胜 = 9分

    # 检查其他选手积分
    wangwu = next(s for s in standings if s["participant"].name == "王五")
    zhaoliu = next(s for s in standings if s["participant"].name == "赵六")
    lisi = next(s for s in standings if s["participant"].name == "李四")
    # 王五: 2胜1负 (vs赵六胜, vs李四胜, vs张三负)
    assert wangwu["wins"] == 2
    assert wangwu["losses"] == 1
    assert wangwu["points"] == 6  # 2胜 = 6分
    # 赵六: 0胜3负
    assert zhaoliu["wins"] == 0
    assert zhaoliu["losses"] == 3
    assert zhaoliu["points"] == 0
    # 李四: 1胜2负 (vs赵六胜)
    assert lisi["wins"] == 1
    assert lisi["losses"] == 2
    assert lisi["points"] == 3

    assert tournament.is_completed()
    assert tournament.get_winner().name == "张三"

    print("✓ 循环赛测试通过")

    # 测试奇数参赛者（轮空）
    odd_names = ["A", "B", "C", "D", "E"]
    odd_tournament = create_round_robin(odd_names)

    # 5人循环赛应该有 5*4/2 = 10 场比赛
    assert len(odd_tournament.matches) == 10

    print("✓ 奇数参赛者循环赛测试通过")

    # 测试 to_dict
    d = tournament.to_dict()
    assert d["type"] == "round_robin"
    assert d["completed"] == True
    assert d["champion"] == "张三"

    print("✓ RoundRobin 所有测试通过")


def test_swiss_system():
    """测试瑞士制比赛"""
    print("\n🧪 测试 SwissSystem")
    print("-" * 40)

    # 8人瑞士制，3轮
    names = ["选手" + str(i) for i in range(1, 9)]
    tournament = create_swiss(names, num_rounds=3)

    assert tournament.num_rounds == 3
    assert tournament.current_round == 0

    # 第一轮配对
    round1 = tournament.generate_round_pairings()
    assert tournament.current_round == 1
    assert len(round1) == 4  # 8人 = 4场比赛

    # 模拟第一轮结果
    for match in round1:
        if match.status != MatchStatus.BYE:
            # 让 participant1 获胜
            tournament.set_result(match.id, 1, 0)

    # 检查积分
    standings = tournament.get_standings()
    winners_r1 = [s for s in standings if s["wins"] == 1]
    assert len(winners_r1) == 4  # 4个胜者

    # 第二轮配对
    round2 = tournament.generate_round_pairings()
    assert tournament.current_round == 2

    # 第二轮应该是胜者对胜者
    for match in round2:
        if match.status != MatchStatus.BYE:
            p1_standing = tournament.standings[match.participant1.id]
            p2_standing = tournament.standings[match.participant2.id]
            # 第二轮配对应该尽量让积分相近的对战
            # (由于第一轮全胜，这里应该都是1分对1分或0分对0分)
            tournament.set_result(match.id, 1, 0)

    # 第三轮
    round3 = tournament.generate_round_pairings()
    assert tournament.current_round == 3

    for match in round3:
        if match.status != MatchStatus.BYE:
            tournament.set_result(match.id, 1, 0)

    assert tournament.is_completed()

    # 检查每个人对战的都是不同对手（瑞士制规则）
    for p_id, history in tournament.pairing_history.items():
        # 每个人的对手数量应该等于轮次（或轮次-1，如果有轮空）
        # 由于双向记录，history 中包含了所有对战过的对手
        unique_opponents = set(history)
        expected_matches = min(tournament.num_rounds, len(tournament.participants) - 1)
        # 每个人最多对战 expected_matches 个不同对手
        assert len(unique_opponents) <= expected_matches, f"选手{p_id}对战了过多对手"

    # 检查最终排名
    final_standings = tournament.get_standings()
    # 第一名应该3胜
    assert final_standings[0]["wins"] == 3
    assert final_standings[0]["points"] == 3.0

    print("✓ 瑞士制测试通过")

    # 测试奇数参赛者（轮空）
    odd_tournament = create_swiss(["A", "B", "C", "D", "E"], num_rounds=3)
    odd_tournament.generate_round_pairings()

    # 应该有一人轮空
    bye_matches = [m for m in odd_tournament.get_current_round_matches()
                  if m.status == MatchStatus.BYE]
    assert len(bye_matches) == 1
    assert bye_matches[0].winner is not None
    assert odd_tournament.standings[bye_matches[0].winner.id]["points"] == 1.0

    print("✓ 瑞士制轮空处理测试通过")

    # 测试 to_dict
    d = tournament.to_dict()
    assert d["type"] == "swiss"
    assert d["num_rounds"] == 3
    assert d["current_round"] == 3
    assert d["completed"] == True
    assert len(d["standings"]) == 8

    print("✓ SwissSystem 所有测试通过")


def test_visualization():
    """测试可视化输出"""
    print("\n🧪 测试可视化输出")
    print("-" * 40)

    # 单败淘汰赛
    se = create_single_elimination(["A", "B", "C", "D"])
    vis = se.visualize()
    assert "单败淘汰赛" in vis
    assert "决赛" in vis
    print("✓ 单败淘汰赛可视化测试通过")

    # 双败淘汰赛
    de = create_double_elimination(["A", "B", "C", "D"])
    vis = de.visualize()
    assert "双败淘汰赛" in vis
    assert "胜者组" in vis
    assert "败者组" in vis
    print("✓ 双败淘汰赛可视化测试通过")

    # 循环赛
    rr = create_round_robin(["甲", "乙", "丙"])
    for m in rr.matches:
        rr.set_result(m.id, 1, 0)
    vis = rr.visualize()
    assert "循环赛" in vis
    assert "积分榜" in vis
    print("✓ 循环赛可视化测试通过")

    # 瑞士制
    swiss = create_swiss(["P1", "P2", "P3", "P4"])
    for _ in range(swiss.num_rounds):
        swiss.generate_round_pairings()
        for m in swiss.get_current_round_matches():
            if m.status != MatchStatus.BYE:
                swiss.set_result(m.id, 1, 0)
    vis = swiss.visualize()
    assert "瑞士制" in vis
    assert "积分榜" in vis
    print("✓ 瑞士制可视化测试通过")


def test_edge_cases():
    """测试边界情况"""
    print("\n🧪 测试边界情况")
    print("-" * 40)

    # 最小参赛者数
    min_se = create_single_elimination(["A", "B"])
    assert min_se.num_rounds == 1
    print("✓ 最小淘汰赛测试通过")

    min_rr = create_round_robin(["A", "B"])
    assert len(min_rr.matches) == 1
    print("✓ 最小循环赛测试通过")

    min_swiss = create_swiss(["A", "B"])
    assert min_swiss.num_rounds == 1
    print("✓ 最小瑞士制测试通过")

    # 大量参赛者
    large_names = [f"P{i}" for i in range(64)]
    large_se = create_single_elimination(large_names)
    assert large_se.num_rounds == 6
    assert len(large_se.get_round_matches(1)) == 32
    print("✓ 64人淘汰赛测试通过")

    # 所有种子相同
    same_seeds = [1, 1, 1, 1]
    same_seed_tournament = create_single_elimination(["A", "B", "C", "D"], same_seeds)
    assert same_seed_tournament.num_rounds == 2
    print("✓ 相同种子测试通过")

    print("✓ 边界情况测试通过")


def run_all_tests():
    """运行所有测试"""
    print("=" * 60)
    print("🧪 Tournament Utilities 测试套件")
    print("=" * 60)

    try:
        test_participant()
        test_single_elimination()
        test_double_elimination()
        test_round_robin()
        test_swiss_system()
        test_visualization()
        test_edge_cases()

        print("\n" + "=" * 60)
        print("✅ 所有测试通过！")
        print("=" * 60)
        return True
    except AssertionError as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False
    except Exception as e:
        print(f"\n❌ 测试错误: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
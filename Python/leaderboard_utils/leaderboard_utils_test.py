"""
Leaderboard Utils 测试模块

测试排行榜工具的所有核心功能。
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime, timedelta
import random
import math

from mod import (
    Leaderboard, LeaderboardEntry, LeaderboardStats, RankedEntry,
    RankingMethod, SortOrder, TieBreakRule,
    MultiLeaderboard, LeaderboardBuilder,
    create_leaderboard
)


def test_basic_operations():
    """测试基本操作"""
    print("测试基本操作...")
    
    lb = Leaderboard("测试排行榜")
    
    # 添加条目
    lb.add_entry("p1", "玩家1", 100)
    lb.add_entry("p2", "玩家2", 200)
    lb.add_entry("p3", "玩家3", 150)
    
    # 验证数量
    assert lb.count() == 3, "条目数量应为 3"
    
    # 获取排名
    top = lb.get_top(10)
    assert len(top) == 3, "应返回 3 个条目"
    
    # 验证排序（降序）
    assert top[0].entry.score == 200, "最高分应为 200"
    assert top[0].entry.name == "玩家2", "第一名应为玩家2"
    
    # 获取单个条目排名
    rank = lb.get_rank("p1")
    assert rank == 3, "玩家1应排第3"
    
    rank = lb.get_rank("p2")
    assert rank == 1, "玩家2应排第1"
    
    print("✓ 基本操作测试通过")


def test_ranking_methods():
    """测试不同排名方式"""
    print("\n测试排名方式...")
    
    # 创建测试数据
    scores = [100, 100, 90, 80, 80, 80, 70]
    
    # 密集排名
    lb = Leaderboard("密集排名", ranking_method=RankingMethod.DENSE)
    for i, score in enumerate(scores):
        lb.add_entry(f"p{i}", f"玩家{i}", score)
    
    top = lb.get_top(10)
    ranks = [int(re.rank) for re in top]
    assert ranks == [1, 1, 2, 3, 3, 3, 4], f"密集排名应为 [1, 1, 2, 3, 3, 3, 4]，实际: {ranks}"
    print("✓ 密集排名测试通过")
    
    # 竞争排名
    lb = Leaderboard("竞争排名", ranking_method=RankingMethod.COMPETITION)
    for i, score in enumerate(scores):
        lb.add_entry(f"p{i}", f"玩家{i}", score)
    
    top = lb.get_top(10)
    ranks = [int(re.rank) for re in top]
    assert ranks == [1, 1, 3, 4, 4, 4, 7], f"竞争排名应为 [1, 1, 3, 4, 4, 4, 7]，实际: {ranks}"
    print("✓ 竞争排名测试通过")
    
    # 顺序排名
    lb = Leaderboard("顺序排名", ranking_method=RankingMethod.ORDINAL)
    for i, score in enumerate(scores):
        lb.add_entry(f"p{i}", f"玩家{i}", score)
    
    top = lb.get_top(10)
    ranks = [int(re.rank) for re in top]
    assert ranks == [1, 2, 3, 4, 5, 6, 7], f"顺序排名应为 [1, 2, 3, 4, 5, 6, 7]，实际: {ranks}"
    print("✓ 顺序排名测试通过")
    
    # 分数排名
    lb = Leaderboard("分数排名", ranking_method=RankingMethod.FRACTIONAL)
    for i, score in enumerate(scores):
        lb.add_entry(f"p{i}", f"玩家{i}", score)
    
    top = lb.get_top(10)
    ranks = [re.rank for re in top]
    # 前两个平均排名为 1.5
    assert ranks[0] == ranks[1] == 1.5, f"前两个平均排名应为 1.5，实际: {ranks[0]}, {ranks[1]}"
    print("✓ 分数排名测试通过")


def test_tie_breaking():
    """测试平局决胜"""
    print("\n测试平局决胜...")
    
    lb = Leaderboard(
        "决胜排行榜",
        tie_break_rules=[
            TieBreakRule("level", SortOrder.DESC),  # 等级高者优先
            TieBreakRule("time", SortOrder.ASC),    # 时间早者优先
        ]
    )
    
    # 添加相同分数但不同等级的条目
    lb.add_entry("p1", "玩家1", 100, {"level": 10, "time": 100})
    lb.add_entry("p2", "玩家2", 100, {"level": 20, "time": 100})
    lb.add_entry("p3", "玩家3", 100, {"level": 20, "time": 50})  # 等级高且时间早
    
    top = lb.get_top(3)
    
    # p3 应该第一（等级高，时间早）
    # p2 应该第二（等级高）
    # p1 应该第三
    assert top[0].entry.id == "p3", "p3 应该第一"
    assert top[1].entry.id == "p2", "p2 应该第二"
    assert top[2].entry.id == "p1", "p1 应该第三"
    
    print("✓ 平局决胜测试通过")


def test_score_updates():
    """测试分数更新"""
    print("\n测试分数更新...")
    
    lb = Leaderboard("更新测试")
    lb.add_entry("p1", "玩家1", 100)
    lb.add_entry("p2", "玩家2", 200)
    
    # 更新分数
    lb.update_score("p1", 300)
    
    top = lb.get_top(2)
    assert top[0].entry.id == "p1", "更新后 p1 应该第一"
    assert top[0].entry.score == 300, "分数应为 300"
    
    # 增量更新
    lb.increment_score("p1", 50)
    entry = lb.get_entry("p1")
    assert entry.score == 350, "增量后分数应为 350"
    
    # 检查历史记录
    assert len(entry.score_history) >= 2, "应有历史记录"
    
    print("✓ 分数更新测试通过")


def test_rank_changes():
    """测试排名变化追踪"""
    print("\n测试排名变化追踪...")
    
    lb = Leaderboard("排名变化测试")
    lb.add_entry("p1", "玩家1", 100)
    lb.add_entry("p2", "玩家2", 200)
    
    # 获取初始排名
    top = lb.get_top(2)
    assert top[0].entry.id == "p2"
    assert top[0].entry.previous_rank is None  # 首次排名
    
    # 更新分数导致排名变化
    lb.update_score("p1", 300)
    top = lb.get_top(2)
    
    p1_entry = [re for re in top if re.entry.id == "p1"][0]
    assert p1_entry.entry.rank_change == 1, "p1 应该从第2升到第1（变化 +1）"
    
    print("✓ 排名变化追踪测试通过")


def test_pagination():
    """测试分页"""
    print("\n测试分页...")
    
    lb = Leaderboard("分页测试")
    for i in range(25):
        lb.add_entry(f"p{i}", f"玩家{i}", i * 10)
    
    # 第一页
    page1, total_pages, total = lb.get_page(1, 10)
    assert len(page1) == 10, "第一页应有 10 条"
    assert total_pages == 3, "总共应有 3 页"
    assert total == 25, "总共 25 条"
    
    # 最后一页
    page3, _, _ = lb.get_page(3, 10)
    assert len(page3) == 5, "最后一页应有 5 条"
    
    # 超出范围
    page4, _, _ = lb.get_page(4, 10)
    assert len(page4) == 0, "超出范围应返回空"
    
    print("✓ 分页测试通过")


def test_around_rank():
    """测试周围排名获取"""
    print("\n测试周围排名获取...")
    
    lb = Leaderboard("周围排名测试")
    for i in range(10):
        lb.add_entry(f"p{i}", f"玩家{i}", i * 10)
    
    # 获取第5名周围的排名
    around = lb.get_around("p4", radius=2)
    assert len(around) == 5, "应返回 5 条（2前+自己+2后）"
    
    print("✓ 周围排名获取测试通过")


def test_statistics():
    """测试统计功能"""
    print("\n测试统计功能...")
    
    lb = Leaderboard("统计测试")
    scores = [10, 20, 30, 40, 50]
    for i, score in enumerate(scores):
        lb.add_entry(f"p{i}", f"玩家{i}", score)
    
    stats = lb.get_stats()
    
    assert stats.total_entries == 5, "总条目数应为 5"
    assert stats.total_score == 150, "总分应为 150"
    assert stats.average_score == 30, "平均分应为 30"
    assert stats.max_score == 50, "最高分应为 50"
    assert stats.min_score == 10, "最低分应为 10"
    assert stats.median_score == 30, "中位数应为 30"
    
    print("✓ 统计功能测试通过")


def test_search():
    """测试搜索功能"""
    print("\n测试搜索功能...")
    
    lb = Leaderboard("搜索测试")
    lb.add_entry("p1", "张三", 100, {"guild": "龙之谷"})
    lb.add_entry("p2", "李四", 200, {"guild": "凤之翼"})
    lb.add_entry("p3", "张五", 150, {"guild": "龙之谷"})
    
    # 按名称搜索
    results = lb.search("张")
    assert len(results) == 2, "应找到 2 个张姓玩家"
    
    # 按 metadata 搜索
    results = lb.search("龙之谷", field="guild")
    assert len(results) == 2, "应找到 2 个龙之谷成员"
    
    print("✓ 搜索功能测试通过")


def test_export_import():
    """测试导出导入"""
    print("\n测试导出导入...")
    
    lb1 = Leaderboard("导出测试")
    lb1.add_entry("p1", "玩家1", 100, {"level": 10})
    lb1.add_entry("p2", "玩家2", 200, {"level": 20})
    
    # 导出
    data = lb1.to_dict()
    assert "name" in data
    assert "entries" in data
    assert len(data["entries"]) == 2
    
    # 导入
    lb2 = Leaderboard.from_dict(data)
    assert lb2.name == "导出测试"
    assert lb2.count() == 2
    
    print("✓ 导出导入测试通过")


def test_multi_leaderboard():
    """测试多排行榜管理"""
    print("\n测试多排行榜管理...")
    
    mlb = MultiLeaderboard()
    
    # 创建多个排行榜
    daily = mlb.create("daily", "每日排行榜")
    weekly = mlb.create("weekly", "每周排行榜")
    
    # 添加条目
    mlb.add_entry("daily", "p1", "玩家1", 100)
    mlb.add_entry("daily", "p2", "玩家2", 200)
    mlb.add_entry("weekly", "p1", "玩家1", 1000)
    mlb.add_entry("weekly", "p3", "玩家3", 500)
    
    # 验证
    assert len(mlb.list()) == 2
    assert mlb.get("daily").count() == 2
    assert mlb.get("weekly").count() == 2
    
    # 跨排行榜获取
    top_across = mlb.get_top_across(5)
    assert len(top_across) == 4  # 只有 4 条记录
    
    print("✓ 多排行榜管理测试通过")


def test_builder_pattern():
    """测试构建器模式"""
    print("\n测试构建器模式...")
    
    lb = (LeaderboardBuilder("构建器测试")
          .with_ranking_method(RankingMethod.COMPETITION)
          .with_sort_order(SortOrder.ASC)
          .add_tie_breaker("level", SortOrder.DESC)
          .with_history(True)
          .build())
    
    assert lb.name == "构建器测试"
    assert lb.ranking_method == RankingMethod.COMPETITION
    assert lb.sort_order == SortOrder.ASC
    assert len(lb.tie_break_rules) == 1
    
    print("✓ 构建器模式测试通过")


def test_convenience_function():
    """测试便捷函数"""
    print("\n测试便捷函数...")
    
    lb = create_leaderboard("快速测试", method="competition", descending=False)
    
    assert lb.name == "快速测试"
    assert lb.ranking_method == RankingMethod.COMPETITION
    assert lb.sort_order == SortOrder.ASC
    
    print("✓ 便捷函数测试通过")


def test_large_dataset():
    """测试大数据集性能"""
    print("\n测试大数据集性能...")
    
    lb = Leaderboard("大数据测试")
    
    # 添加 10000 条记录
    start = datetime.now()
    for i in range(10000):
        lb.add_entry(f"p{i}", f"玩家{i}", random.randint(0, 10000))
    add_time = (datetime.now() - start).total_seconds()
    
    # 获取排名
    start = datetime.now()
    top = lb.get_top(100)
    rank_time = (datetime.now() - start).total_seconds()
    
    # 获取统计
    start = datetime.now()
    stats = lb.get_stats()
    stats_time = (datetime.now() - start).total_seconds()
    
    assert len(top) == 100
    assert stats.total_entries == 10000
    
    print(f"  添加 10000 条: {add_time:.3f}s")
    print(f"  获取前 100: {rank_time:.3f}s")
    print(f"  计算统计: {stats_time:.3f}s")
    print("✓ 大数据集性能测试通过")


def test_edge_cases():
    """测试边界情况"""
    print("\n测试边界情况...")
    
    # 空排行榜
    lb = Leaderboard("空测试")
    assert lb.count() == 0
    assert lb.get_top(10) == []
    assert lb.get_rank("nonexistent") is None
    
    stats = lb.get_stats()
    assert stats.total_entries == 0
    assert stats.average_score == 0
    
    # 单条目
    lb.add_entry("p1", "唯一玩家", 100)
    assert lb.get_rank("p1") == 1
    assert lb.get_top(1)[0].entry.id == "p1"
    
    # 相同分数
    lb2 = Leaderboard("相同分数测试")
    lb2.add_entry("p1", "玩家1", 100)
    lb2.add_entry("p2", "玩家2", 100)
    lb2.add_entry("p3", "玩家3", 100)
    
    top = lb2.get_top(3)
    for re in top:
        assert re.tied, "所有条目应该 tied=True"
        assert re.tied_count == 3, "应该有 3 个平局"
    
    print("✓ 边界情况测试通过")


def test_bottom():
    """测试获取后 N 名"""
    print("\n测试获取后 N 名...")
    
    lb = Leaderboard("后排名测试")
    for i in range(5):
        lb.add_entry(f"p{i}", f"玩家{i}", i * 10)
    
    bottom = lb.get_bottom(2)
    assert len(bottom) == 2
    assert bottom[0].entry.score == 10
    assert bottom[1].entry.score == 0
    
    print("✓ 获取后 N 名测试通过")


def test_remove():
    """测试移除条目"""
    print("\n测试移除条目...")
    
    lb = Leaderboard("移除测试")
    lb.add_entry("p1", "玩家1", 100)
    lb.add_entry("p2", "玩家2", 200)
    
    assert lb.count() == 2
    
    # 移除存在条目
    result = lb.remove_entry("p1")
    assert result == True
    assert lb.count() == 1
    assert lb.get_entry("p1") is None
    
    # 移除不存在条目
    result = lb.remove_entry("nonexistent")
    assert result == False
    
    print("✓ 移除条目测试通过")


def test_get_score_rank():
    """测试获取分数排名"""
    print("\n测试获取分数排名...")
    
    lb = Leaderboard("分数排名测试")
    lb.add_entry("p1", "玩家1", 100)
    lb.add_entry("p2", "玩家2", 80)
    lb.add_entry("p3", "玩家3", 60)
    
    # 获取分数排名
    rank = lb.get_score_rank(90)  # 不存在的分数
    assert rank == 2, "90分应该排第2（在100和80之间）"
    
    rank = lb.get_score_rank(100)
    assert rank == 1, "100分应该排第1"
    
    rank = lb.get_score_rank(50)
    assert rank == 4, "50分应该排第4（在所有分数之后）"
    
    print("✓ 获取分数排名测试通过")


def run_all_tests():
    """运行所有测试"""
    print("=" * 60)
    print("Leaderboard Utils 测试套件")
    print("=" * 60)
    
    tests = [
        test_basic_operations,
        test_ranking_methods,
        test_tie_breaking,
        test_score_updates,
        test_rank_changes,
        test_pagination,
        test_around_rank,
        test_statistics,
        test_search,
        test_export_import,
        test_multi_leaderboard,
        test_builder_pattern,
        test_convenience_function,
        test_large_dataset,
        test_edge_cases,
        test_bottom,
        test_remove,
        test_get_score_rank,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"✗ {test.__name__} 失败: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {test.__name__} 异常: {e}")
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"测试结果: {passed} 通过, {failed} 失败")
    print("=" * 60)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
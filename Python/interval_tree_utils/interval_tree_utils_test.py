"""
区间树工具测试模块
==================

测试 IntervalTree 的所有核心功能。
"""

import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from interval_tree_utils.interval_tree import IntervalTree, Interval


class TestInterval(unittest.TestCase):
    """测试 Interval 类"""

    def test_create_interval(self):
        """测试创建区间"""
        interval = Interval(1, 5)
        self.assertEqual(interval.start, 1)
        self.assertEqual(interval.end, 5)
        self.assertIsNone(interval.value)

    def test_create_interval_with_value(self):
        """测试创建带值的区间"""
        interval = Interval(1, 5, value="test")
        self.assertEqual(interval.value, "test")

    def test_invalid_interval(self):
        """测试无效区间"""
        with self.assertRaises(ValueError):
            Interval(5, 1)  # start > end

    def test_overlaps(self):
        """测试重叠检测"""
        a = Interval(1, 5)
        b = Interval(3, 8)
        c = Interval(6, 10)
        d = Interval(10, 15)

        self.assertTrue(a.overlaps(b))  # 重叠
        self.assertTrue(a.overlaps(a))  # 自重叠
        self.assertFalse(a.overlaps(c))  # 不重叠
        self.assertFalse(a.overlaps(d))  # 完全分离

    def test_contains_interval(self):
        """测试区间包含"""
        outer = Interval(1, 10)
        inner = Interval(3, 7)
        partial = Interval(5, 15)

        self.assertTrue(outer.contains(inner))
        self.assertFalse(inner.contains(outer))
        self.assertFalse(outer.contains(partial))

    def test_contains_point(self):
        """测试点包含"""
        interval = Interval(1, 5)

        self.assertTrue(interval.contains_point(1))  # 边界
        self.assertTrue(interval.contains_point(3))  # 内部
        self.assertTrue(interval.contains_point(5))  # 边界
        self.assertFalse(interval.contains_point(0))  # 外部
        self.assertFalse(interval.contains_point(6))  # 外部

    def test_intersection(self):
        """测试区间交集"""
        a = Interval(1, 5)
        b = Interval(3, 8)
        c = Interval(10, 15)

        result = a.intersection(b)
        self.assertEqual(result.start, 3)
        self.assertEqual(result.end, 5)

        result = a.intersection(c)
        self.assertIsNone(result)

    def test_union(self):
        """测试区间并集"""
        a = Interval(1, 5)
        b = Interval(3, 8)
        c = Interval(10, 15)

        result = a.union(b)
        self.assertEqual(result.start, 1)
        self.assertEqual(result.end, 8)

        result = a.union(c)
        self.assertIsNone(result)  # 不相交也不相邻

    def test_length(self):
        """测试区间长度"""
        interval = Interval(1, 5)
        self.assertEqual(interval.length, 4)
        self.assertEqual(len(interval), 4)

    def test_center(self):
        """测试区间中心"""
        interval = Interval(1, 5)
        self.assertEqual(interval.center, 3.0)

    def test_in_operator(self):
        """测试 in 操作符"""
        interval = Interval(1, 5)

        self.assertIn(3, interval)  # 点包含
        self.assertNotIn(6, interval)

        inner = Interval(2, 4)
        outer = Interval(0, 10)

        self.assertIn(inner, interval)  # 区间包含
        self.assertNotIn(outer, interval)

    def test_comparison(self):
        """测试区间比较"""
        a = Interval(1, 5)
        b = Interval(2, 6)
        c = Interval(1, 3)

        self.assertTrue(a < b)  # 按起点比较
        self.assertTrue(c < a)  # 起点相同，按终点比较
        self.assertFalse(a < c)

    def test_equality_and_hash(self):
        """测试相等性和哈希"""
        a = Interval(1, 5)
        b = Interval(1, 5)
        c = Interval(1, 5, value="test")

        self.assertEqual(a, b)
        self.assertNotEqual(a, c)

        # 可以作为字典键
        d = {a: "value"}
        self.assertEqual(d[b], "value")


class TestIntervalTree(unittest.TestCase):
    """测试 IntervalTree 类"""

    def test_create_empty_tree(self):
        """测试创建空树"""
        tree = IntervalTree()
        self.assertEqual(len(tree), 0)
        self.assertTrue(tree.is_empty())

    def test_create_tree_with_intervals(self):
        """测试使用初始区间创建树"""
        intervals = [Interval(1, 5), Interval(3, 8)]
        tree = IntervalTree(intervals)

        self.assertEqual(len(tree), 2)

    def test_insert_and_query_point(self):
        """测试插入和点查询"""
        tree = IntervalTree()

        tree.insert(Interval(1, 5, value="a"))
        tree.insert(Interval(3, 8, value="b"))
        tree.insert(Interval(10, 15, value="c"))

        # 查询点 3
        results = tree.query_point(3)
        self.assertEqual(len(results), 2)
        values = {r.value for r in results}
        self.assertIn("a", values)
        self.assertIn("b", values)

        # 查询点 12
        results = tree.query_point(12)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].value, "c")

        # 查询点 9（无覆盖）
        results = tree.query_point(9)
        self.assertEqual(len(results), 0)

    def test_query_overlaps(self):
        """测试区间重叠查询"""
        tree = IntervalTree()

        tree.insert(Interval(1, 5))
        tree.insert(Interval(3, 8))
        tree.insert(Interval(10, 15))
        tree.insert(Interval(12, 18))

        # 查询与 [4, 13] 重叠的区间
        # [1,5] 重叠, [3,8] 重叠, [10,15] 重叠, [12,18] 重叠
        results = tree.query_overlaps(Interval(4, 13))
        self.assertEqual(len(results), 4)

        starts = {r.start for r in results}
        self.assertIn(1, starts)  # [1,5]
        self.assertIn(3, starts)  # [3,8]
        self.assertIn(10, starts)  # [10,15]
        self.assertIn(12, starts)  # [12,18] 也与 [4,13] 重叠

        # 测试不重叠的情况
        results = tree.query_overlaps(Interval(20, 25))
        self.assertEqual(len(results), 0)

    def test_query_contains(self):
        """测试查询包含指定区间的区间"""
        tree = IntervalTree()

        tree.insert(Interval(1, 20, value="outer"))
        tree.insert(Interval(5, 15, value="middle"))
        tree.insert(Interval(8, 12, value="inner"))

        results = tree.query_contains(Interval(10, 11))
        self.assertEqual(len(results), 3)

        results = tree.query_contains(Interval(6, 14))
        self.assertEqual(len(results), 2)  # outer 和 middle

    def test_query_contained_by(self):
        """测试查询被指定区间包含的区间"""
        tree = IntervalTree()

        tree.insert(Interval(5, 10, value="a"))
        tree.insert(Interval(15, 20, value="b"))
        tree.insert(Interval(3, 25, value="outer"))

        results = tree.query_contained_by(Interval(1, 30))
        self.assertEqual(len(results), 3)

        results = tree.query_contained_by(Interval(4, 22))
        self.assertEqual(len(results), 2)  # a 和 b，不包含 outer

    def test_remove(self):
        """测试移除区间"""
        tree = IntervalTree()

        interval1 = Interval(1, 5)
        interval2 = Interval(3, 8)

        tree.insert(interval1)
        tree.insert(interval2)

        self.assertEqual(len(tree), 2)

        # 移除一个区间
        result = tree.remove(interval1)
        self.assertTrue(result)
        self.assertEqual(len(tree), 1)

        # 查询确认移除
        results = tree.query_point(2)
        self.assertEqual(len(results), 0)  # interval1 已移除

        # 移除不存在的区间
        result = tree.remove(Interval(10, 15))
        self.assertFalse(result)

    def test_find_first_overlapping(self):
        """测试查找第一个重叠区间"""
        tree = IntervalTree()

        tree.insert(Interval(1, 5))
        tree.insert(Interval(10, 15))

        result = tree.find_first_overlapping(Interval(3, 7))
        self.assertIsNotNone(result)
        self.assertEqual(result.start, 1)

        result = tree.find_first_overlapping(Interval(20, 25))
        self.assertIsNone(result)

    def test_find_all_gaps(self):
        """测试查找空白区域"""
        tree = IntervalTree()

        tree.insert(Interval(1, 5))
        tree.insert(Interval(10, 15))
        tree.insert(Interval(20, 25))

        gaps = tree.find_all_gaps(0, 30)

        self.assertEqual(len(gaps), 4)
        self.assertIn(Interval(0, 0), gaps)
        self.assertIn(Interval(6, 9), gaps)
        self.assertIn(Interval(16, 19), gaps)
        self.assertIn(Interval(26, 30), gaps)

    def test_iteration(self):
        """测试迭代所有区间"""
        tree = IntervalTree()

        intervals = [Interval(1, 5), Interval(3, 8), Interval(10, 15)]
        for iv in intervals:
            tree.insert(iv)

        all_intervals = list(tree)
        self.assertEqual(len(all_intervals), 3)

    def test_from_tuples(self):
        """测试从元组创建树"""
        tuples = [(1, 5, "a"), (3, 8, "b"), (10, 15, "c")]
        tree = IntervalTree.from_tuples(tuples)

        self.assertEqual(len(tree), 3)

        results = tree.query_point(4)
        self.assertEqual(len(results), 2)

    def test_clear(self):
        """测试清空树"""
        tree = IntervalTree()

        tree.insert(Interval(1, 5))
        tree.insert(Interval(3, 8))

        self.assertEqual(len(tree), 2)

        tree.clear()

        self.assertEqual(len(tree), 0)
        self.assertTrue(tree.is_empty())

    def test_to_list(self):
        """测试转为列表"""
        tree = IntervalTree()

        intervals = [Interval(1, 5), Interval(10, 15)]
        for iv in intervals:
            tree.insert(iv)

        result = tree.to_list()
        self.assertEqual(len(result), 2)

    def test_get_statistics(self):
        """测试获取统计信息"""
        tree = IntervalTree()

        for i in range(5):
            tree.insert(Interval(i * 10, i * 10 + 5))

        stats = tree.get_statistics()

        self.assertEqual(stats['size'], 5)
        self.assertFalse(stats['is_empty'])
        self.assertGreater(stats['height'], 0)

    def test_float_intervals(self):
        """测试浮点数区间"""
        tree = IntervalTree()

        tree.insert(Interval(1.5, 5.5))
        tree.insert(Interval(3.0, 8.0))

        results = tree.query_point(4.0)
        self.assertEqual(len(results), 2)

        results = tree.query_point(1.6)
        self.assertEqual(len(results), 1)

    def test_large_scale_insertion(self):
        """测试大规模插入"""
        tree = IntervalTree()

        # 插入 1000 个随机区间
        import random
        random.seed(42)

        for _ in range(1000):
            start = random.randint(0, 10000)
            end = start + random.randint(1, 100)
            tree.insert(Interval(start, end))

        self.assertEqual(len(tree), 1000)

        # 验证查询功能正常
        results = tree.query_point(5000)
        self.assertGreater(len(results), 0)

    def test_contains_operator(self):
        """测试 __contains__ 操作符"""
        tree = IntervalTree()

        interval = Interval(1, 5)
        tree.insert(interval)

        self.assertIn(interval, tree)
        self.assertNotIn(Interval(10, 15), tree)

    def test_bool_operator(self):
        """测试布尔值"""
        tree = IntervalTree()

        self.assertFalse(tree)  # 空树

        tree.insert(Interval(1, 5))
        self.assertTrue(tree)  # 非空树

    def test_repr(self):
        """测试字符串表示"""
        interval = Interval(1, 5)
        self.assertIn("1", repr(interval))
        self.assertIn("5", repr(interval))

        tree = IntervalTree()
        tree.insert(interval)
        self.assertIn("size=1", repr(tree))


class TestEdgeCases(unittest.TestCase):
    """测试边界情况"""

    def test_single_point_interval(self):
        """测试单点区间"""
        tree = IntervalTree()

        interval = Interval(5, 5)
        tree.insert(interval)

        results = tree.query_point(5)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0], interval)

    def test_adjacent_intervals(self):
        """测试相邻区间"""
        tree = IntervalTree()

        tree.insert(Interval(1, 5))
        tree.insert(Interval(6, 10))

        # 点 5 不应该与第二个区间重叠
        results = tree.query_point(5)
        self.assertEqual(len(results), 1)

        # 点 6 只应该与第二个区间重叠
        results = tree.query_point(6)
        self.assertEqual(len(results), 1)

    def test_identical_intervals(self):
        """测试相同区间"""
        tree = IntervalTree()

        interval1 = Interval(1, 5, value="a")
        interval2 = Interval(1, 5, value="b")

        tree.insert(interval1)
        tree.insert(interval2)

        results = tree.query_point(3)
        self.assertEqual(len(results), 2)

    def test_negative_intervals(self):
        """测试负数区间"""
        tree = IntervalTree()

        tree.insert(Interval(-10, -5))
        tree.insert(Interval(-3, 3))
        tree.insert(Interval(5, 10))

        results = tree.query_point(-7)
        self.assertEqual(len(results), 1)

        results = tree.query_point(0)
        self.assertEqual(len(results), 1)


if __name__ == '__main__':
    unittest.main()
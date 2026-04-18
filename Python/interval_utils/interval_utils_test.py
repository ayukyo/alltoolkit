"""
区间操作工具模块测试

测试覆盖：
- Interval 类：创建、比较、运算
- IntervalSet 类：增删改查、集合运算
- 便捷函数：合并、交集、差集等
- IntervalMap 类：区间映射
- RangeSet 类：范围集合
"""

import unittest
from mod import (
    Interval, IntervalSet, IntervalMap, RangeSet,
    merge_intervals, interval_intersection, interval_difference,
    interval_union, find_gaps, is_covered, find_containing_interval,
    get_total_coverage
)


class TestInterval(unittest.TestCase):
    """Interval 类测试"""
    
    def test_create_interval(self):
        """测试创建区间"""
        i = Interval(1, 5)
        self.assertEqual(i.start, 1)
        self.assertEqual(i.end, 5)
        self.assertEqual(i.length, 5)
    
    def test_invalid_interval(self):
        """测试无效区间"""
        with self.assertRaises(ValueError):
            Interval(5, 1)
    
    def test_contains(self):
        """测试包含判断"""
        i = Interval(1, 5)
        self.assertIn(1, i)
        self.assertIn(3, i)
        self.assertIn(5, i)
        self.assertNotIn(0, i)
        self.assertNotIn(6, i)
    
    def test_len(self):
        """测试长度"""
        self.assertEqual(len(Interval(1, 5)), 5)
        self.assertEqual(len(Interval(0, 0)), 1)
        self.assertEqual(len(Interval(10, 20)), 11)
    
    def test_overlaps(self):
        """测试重叠判断"""
        i1 = Interval(1, 5)
        i2 = Interval(3, 8)
        i3 = Interval(6, 10)
        i4 = Interval(0, 0)
        
        self.assertTrue(i1.overlaps(i2))
        self.assertTrue(i2.overlaps(i1))
        self.assertFalse(i1.overlaps(i3))
        self.assertFalse(i1.overlaps(i4))
    
    def test_adjacent(self):
        """测试相邻判断"""
        i1 = Interval(1, 5)
        i2 = Interval(6, 10)
        i3 = Interval(0, 0)  # 与 i1 相邻 (0+1=1)
        i4 = Interval(7, 12)
        i5 = Interval(20, 25)  # 不相邻
        
        self.assertTrue(i1.adjacent(i2))
        self.assertTrue(i2.adjacent(i1))
        self.assertTrue(i1.adjacent(i3))  # (0,0) 和 (1,5) 相邻
        self.assertFalse(i1.adjacent(i4))
        self.assertFalse(i1.adjacent(i5))
    
    def test_merge(self):
        """测试合并"""
        i1 = Interval(1, 5)
        i2 = Interval(3, 8)
        i3 = Interval(6, 10)  # 与 i1 相邻
        i4 = Interval(0, 0)   # 与 i1 相邻 (0+1=1)
        i5 = Interval(20, 30) # 不相邻也不重叠
        
        merged = i1.merge(i2)
        self.assertEqual(merged.start, 1)
        self.assertEqual(merged.end, 8)
        
        merged = i1.merge(i3)
        self.assertEqual(merged.start, 1)
        self.assertEqual(merged.end, 10)
        
        merged = i1.merge(i4)  # 相邻区间可以合并
        self.assertEqual(merged.start, 0)
        self.assertEqual(merged.end, 5)
        
        with self.assertRaises(ValueError):
            i1.merge(i5)  # 不相邻也不重叠的不能合并
    
    def test_intersection(self):
        """测试交集"""
        i1 = Interval(1, 5)
        i2 = Interval(3, 8)
        i3 = Interval(6, 10)
        
        inter = i1.intersection(i2)
        self.assertEqual(inter.start, 3)
        self.assertEqual(inter.end, 5)
        
        inter = i1.intersection(i3)
        self.assertIsNone(inter)
    
    def test_difference(self):
        """测试差集"""
        i1 = Interval(1, 10)
        i2 = Interval(3, 5)
        i3 = Interval(8, 15)
        i4 = Interval(0, 20)
        
        # 中间减去
        diff = i1.difference(i2)
        self.assertEqual(len(diff), 2)
        self.assertEqual(diff[0], Interval(1, 2))
        self.assertEqual(diff[1], Interval(6, 10))
        
        # 末尾减去
        diff = i1.difference(i3)
        self.assertEqual(len(diff), 1)
        self.assertEqual(diff[0], Interval(1, 7))
        
        # 完全被覆盖
        diff = i1.difference(i4)
        self.assertEqual(len(diff), 0)
        
        # 无重叠
        diff = i1.difference(Interval(20, 30))
        self.assertEqual(len(diff), 1)
        self.assertEqual(diff[0], Interval(1, 10))
    
    def test_to_tuple(self):
        """测试转换为元组"""
        i = Interval(1, 5)
        self.assertEqual(i.to_tuple(), (1, 5))
        
        i2 = Interval.from_tuple((10, 20))
        self.assertEqual(i2.start, 10)
        self.assertEqual(i2.end, 20)
    
    def test_equality(self):
        """测试相等判断"""
        i1 = Interval(1, 5)
        i2 = Interval(1, 5)
        i3 = Interval(1, 6)
        
        self.assertEqual(i1, i2)
        self.assertNotEqual(i1, i3)
    
    def test_hash(self):
        """测试哈希"""
        i1 = Interval(1, 5)
        i2 = Interval(1, 5)
        
        s = {i1, i2}
        self.assertEqual(len(s), 1)
    
    def test_comparison(self):
        """测试比较"""
        i1 = Interval(1, 5)
        i2 = Interval(2, 3)
        i3 = Interval(1, 10)
        
        self.assertLess(i1, i2)  # 1 < 2
        self.assertLess(i1, i3)  # same start, but 5 < 10


class TestIntervalSet(unittest.TestCase):
    """IntervalSet 类测试"""
    
    def test_empty_set(self):
        """测试空集合"""
        s = IntervalSet()
        self.assertEqual(len(s), 0)
        self.assertFalse(s)
        self.assertTrue(s.is_empty)
        self.assertEqual(s.total_length, 0)
    
    def test_add_single(self):
        """测试添加单个区间"""
        s = IntervalSet()
        s.add(Interval(1, 5))
        
        self.assertEqual(len(s), 1)
        self.assertEqual(s.total_length, 5)
        self.assertTrue(s.contains(3))
        self.assertFalse(s.contains(6))
    
    def test_add_merge(self):
        """测试添加时自动合并"""
        s = IntervalSet()
        s.add(Interval(1, 5))
        s.add(Interval(3, 8))  # 重叠
        s.add(Interval(10, 15))
        s.add(Interval(7, 12))  # 连接两个区间
        
        self.assertEqual(len(s), 1)
        self.assertEqual(s.total_length, 15)
    
    def test_add_adjacent(self):
        """测试添加相邻区间"""
        s = IntervalSet()
        s.add(Interval(1, 5))
        s.add(Interval(6, 10))
        
        self.assertEqual(len(s), 1)
        self.assertEqual(s.min_value, 1)
        self.assertEqual(s.max_value, 10)
    
    def test_remove(self):
        """测试移除区间"""
        s = IntervalSet()
        s.add(Interval(1, 20))
        s.remove(Interval(5, 10))
        
        self.assertEqual(len(s), 2)
        self.assertTrue(s.contains(3))
        self.assertFalse(s.contains(7))
        self.assertTrue(s.contains(15))
    
    def test_remove_all(self):
        """测试完全移除"""
        s = IntervalSet()
        s.add(Interval(5, 10))
        s.remove(Interval(1, 20))
        
        self.assertEqual(len(s), 0)
        self.assertTrue(s.is_empty)
    
    def test_find_overlapping(self):
        """测试查找重叠区间"""
        s = IntervalSet()
        s.add(Interval(1, 5))
        s.add(Interval(10, 15))
        s.add(Interval(20, 25))
        
        overlapping = s.find_overlapping(Interval(4, 12))
        self.assertEqual(len(overlapping), 2)
        
        overlapping = s.find_overlapping(Interval(30, 40))
        self.assertEqual(len(overlapping), 0)
    
    def test_find_containing(self):
        """测试查找包含值的区间"""
        s = IntervalSet()
        s.add(Interval(1, 5))
        s.add(Interval(10, 15))
        
        result = s.find_containing(3)
        self.assertEqual(result, Interval(1, 5))
        
        result = s.find_containing(7)
        self.assertIsNone(result)
    
    def test_contains_interval(self):
        """测试区间是否被完全覆盖"""
        s = IntervalSet()
        s.add(Interval(1, 20))
        
        self.assertTrue(s.contains_interval(Interval(5, 10)))
        self.assertFalse(s.contains_interval(Interval(0, 10)))
        self.assertFalse(s.contains_interval(Interval(15, 25)))
    
    def test_union(self):
        """测试并集"""
        s1 = IntervalSet([Interval(1, 5), Interval(10, 15)])
        s2 = IntervalSet([Interval(3, 8), Interval(12, 20)])
        
        result = s1.union(s2)
        self.assertEqual(len(result), 2)
        self.assertEqual(result.total_length, 19)  # [1,8]=8 + [10,20]=11
    
    def test_intersection(self):
        """测试交集"""
        s1 = IntervalSet([Interval(1, 10), Interval(20, 30)])
        s2 = IntervalSet([Interval(5, 25), Interval(28, 35)])
        
        result = s1.intersection(s2)
        self.assertEqual(len(result), 3)  # [5,10], [20,25], [28,30]
    
    def test_difference(self):
        """测试差集"""
        s1 = IntervalSet([Interval(1, 20)])
        s2 = IntervalSet([Interval(5, 10), Interval(15, 18)])
        
        result = s1.difference(s2)
        self.assertEqual(len(result), 3)  # [1,4], [11,14], [19,20]
    
    def test_gaps(self):
        """测试空隙"""
        s = IntervalSet([Interval(1, 5), Interval(10, 15), Interval(20, 25)])
        gaps = s.gaps()
        
        self.assertEqual(len(gaps), 2)
        self.assertIn(Interval(6, 9), gaps)
        self.assertIn(Interval(16, 19), gaps)
    
    def test_cover_range(self):
        """测试范围覆盖"""
        s = IntervalSet([Interval(1, 5), Interval(10, 15)])
        
        covered = s.cover_range(3, 12)
        self.assertEqual(len(covered), 2)  # [3,5], [10,12]
        
        uncovered = s.uncovered_range(3, 12)
        self.assertEqual(len(uncovered), 1)  # [6,9]
    
    def test_iteration(self):
        """测试迭代"""
        s = IntervalSet([Interval(1, 5), Interval(10, 15)])
        intervals = list(s)
        
        self.assertEqual(len(intervals), 2)
        self.assertEqual(intervals[0], Interval(1, 5))
        self.assertEqual(intervals[1], Interval(10, 15))
    
    def test_copy(self):
        """测试复制"""
        s1 = IntervalSet([Interval(1, 5)])
        s2 = s1.copy()
        
        s2.add(Interval(10, 15))
        self.assertEqual(len(s1), 1)
        self.assertEqual(len(s2), 2)
    
    def test_clear(self):
        """测试清空"""
        s = IntervalSet([Interval(1, 5), Interval(10, 15)])
        s.clear()
        
        self.assertTrue(s.is_empty)


class TestConvenienceFunctions(unittest.TestCase):
    """便捷函数测试"""
    
    def test_merge_intervals(self):
        """测试合并区间函数"""
        data = [(1, 3), (2, 6), (8, 10), (9, 12), (15, 15)]
        result = merge_intervals(data)
        
        self.assertEqual(len(result), 3)
        self.assertIn((1, 6), result)
        self.assertIn((8, 12), result)
        self.assertIn((15, 15), result)
    
    def test_merge_intervals_with_gaps(self):
        """测试相邻区间合并"""
        data = [(1, 3), (4, 6)]  # 相邻
        result = merge_intervals(data)
        
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], (1, 6))
    
    def test_interval_intersection(self):
        """测试区间交集函数"""
        set1 = [(1, 10), (20, 30)]
        set2 = [(5, 25), (28, 35)]
        
        result = interval_intersection(set1, set2)
        self.assertEqual(len(result), 3)
    
    def test_interval_difference(self):
        """测试区间差集函数"""
        set1 = [(1, 20)]
        set2 = [(5, 10), (15, 18)]
        
        result = interval_difference(set1, set2)
        self.assertEqual(len(result), 3)
    
    def test_interval_union(self):
        """测试区间并集函数"""
        set1 = [(1, 5), (10, 15)]
        set2 = [(3, 8), (12, 20)]
        
        result = interval_union(set1, set2)
        self.assertEqual(len(result), 2)
    
    def test_find_gaps(self):
        """测试查找空隙函数"""
        data = [(1, 5), (10, 15), (20, 25)]
        gaps = find_gaps(data)
        
        self.assertEqual(len(gaps), 2)
        self.assertIn((6, 9), gaps)
        self.assertIn((16, 19), gaps)
    
    def test_is_covered(self):
        """测试值覆盖检测函数"""
        intervals = [(1, 5), (10, 15)]
        
        self.assertTrue(is_covered(intervals, 3))
        self.assertTrue(is_covered(intervals, 12))
        self.assertFalse(is_covered(intervals, 7))
    
    def test_find_containing_interval(self):
        """测试查找包含区间函数"""
        intervals = [(1, 5), (10, 15)]
        
        result = find_containing_interval(intervals, 3)
        self.assertEqual(result, (1, 5))
        
        result = find_containing_interval(intervals, 7)
        self.assertIsNone(result)
    
    def test_get_total_coverage(self):
        """测试总覆盖计算函数"""
        intervals = [(1, 5), (3, 8), (10, 15)]
        total = get_total_coverage(intervals)
        
        self.assertEqual(total, 14)  # [1,8]=8 + [10,15]=6


class TestIntervalMap(unittest.TestCase):
    """IntervalMap 类测试"""
    
    def test_set_and_get(self):
        """测试设置和获取"""
        m = IntervalMap()
        m.set(1, 10, "A")
        
        self.assertEqual(m.get(5), "A")
        self.assertIsNone(m.get(15))
    
    def test_overwrite(self):
        """测试覆盖写入"""
        m = IntervalMap()
        m.set(1, 10, "A")
        m.set(5, 15, "B")
        
        self.assertEqual(m.get(3), "A")
        self.assertEqual(m.get(8), "B")
        self.assertEqual(m.get(12), "B")  # 在 [5,15] 区间内
        self.assertIsNone(m.get(16))
    
    def test_remove(self):
        """测试移除"""
        m = IntervalMap()
        m.set(1, 20, "A")
        m.remove(5, 10)
        
        self.assertEqual(m.get(3), "A")
        self.assertIsNone(m.get(7))
        self.assertEqual(m.get(15), "A")
    
    def test_get_range(self):
        """测试范围查询"""
        m = IntervalMap()
        m.set(1, 5, "A")
        m.set(10, 15, "B")
        
        result = m.get_range(3, 12)
        self.assertEqual(len(result), 2)
    
    def test_items(self):
        """测试获取所有项"""
        m = IntervalMap()
        m.set(1, 5, "A")
        m.set(10, 15, "B")
        
        items = m.items()
        self.assertEqual(len(items), 2)
    
    def test_clear(self):
        """测试清空"""
        m = IntervalMap()
        m.set(1, 10, "A")
        m.clear()
        
        self.assertEqual(len(m), 0)


class TestRangeSet(unittest.TestCase):
    """RangeSet 类测试"""
    
    def test_create_empty(self):
        """测试创建空集合"""
        rs = RangeSet()
        self.assertEqual(len(rs), 0)
    
    def test_add_single(self):
        """测试添加单个值"""
        rs = RangeSet()
        rs.add(5)
        
        self.assertIn(5, rs)
        self.assertNotIn(4, rs)
        self.assertNotIn(6, rs)
    
    def test_add_range(self):
        """测试添加范围"""
        rs = RangeSet()
        rs.add_range(1, 10)
        
        self.assertEqual(len(rs), 10)
        for i in range(1, 11):
            self.assertIn(i, rs)
    
    def test_update(self):
        """测试批量添加"""
        rs = RangeSet()
        rs.update([1, 2, 3, 5, 6, 8])
        
        self.assertEqual(len(rs), 6)
    
    def test_remove(self):
        """测试移除"""
        rs = RangeSet()
        rs.add_range(1, 10)
        rs.remove(5)
        
        self.assertNotIn(5, rs)
        self.assertIn(4, rs)
        self.assertIn(6, rs)
    
    def test_remove_range(self):
        """测试移除范围"""
        rs = RangeSet()
        rs.add_range(1, 20)
        rs.remove_range(5, 10)
        
        self.assertEqual(len(rs), 14)  # 20 - 6 = 14
    
    def test_set_operations(self):
        """测试集合运算"""
        rs1 = RangeSet()
        rs1.add_range(1, 10)
        
        rs2 = RangeSet()
        rs2.add_range(5, 15)
        
        # 并集
        union = rs1.union(rs2)
        self.assertEqual(len(union), 15)
        
        # 交集
        inter = rs1.intersection(rs2)
        self.assertEqual(len(inter), 6)  # 5-10
        
        # 差集
        diff = rs1.difference(rs2)
        self.assertEqual(len(diff), 4)  # 1-4
        
        # 对称差集
        sym_diff = rs1.symmetric_difference(rs2)
        self.assertEqual(len(sym_diff), 9)  # 1-4 + 11-15
    
    def test_subset_superset(self):
        """测试子集超集"""
        rs1 = RangeSet()
        rs1.add_range(1, 10)
        
        rs2 = RangeSet()
        rs2.add_range(3, 7)
        
        self.assertTrue(rs2.issubset(rs1))
        self.assertTrue(rs1.issuperset(rs2))
        self.assertFalse(rs1.issubset(rs2))
    
    def test_isdisjoint(self):
        """测试无交集"""
        rs1 = RangeSet()
        rs1.add_range(1, 10)
        
        rs2 = RangeSet()
        rs2.add_range(20, 30)
        
        self.assertTrue(rs1.isdisjoint(rs2))
        
        rs3 = RangeSet()
        rs3.add_range(5, 15)
        
        self.assertFalse(rs1.isdisjoint(rs3))
    
    def test_iteration(self):
        """测试迭代"""
        rs = RangeSet()
        rs.add_range(1, 5)
        rs.add_range(10, 12)
        
        values = list(rs)
        self.assertEqual(values, [1, 2, 3, 4, 5, 10, 11, 12])
    
    def test_min_max(self):
        """测试最小最大值"""
        rs = RangeSet()
        rs.add_range(5, 10)
        rs.add_range(20, 30)
        
        self.assertEqual(rs.min_value, 5)
        self.assertEqual(rs.max_value, 30)
    
    def test_from_range(self):
        """测试从范围创建"""
        rs = RangeSet.from_range(1, 10)
        
        self.assertEqual(len(rs), 10)
        for i in range(1, 11):
            self.assertIn(i, rs)
    
    def test_copy(self):
        """测试复制"""
        rs1 = RangeSet.from_range(1, 10)
        rs2 = rs1.copy()
        
        rs2.remove(5)
        self.assertIn(5, rs1)
        self.assertNotIn(5, rs2)
    
    def test_discard(self):
        """测试安全移除"""
        rs = RangeSet.from_range(1, 10)
        
        rs.discard(5)  # 存在
        self.assertNotIn(5, rs)
        
        rs.discard(100)  # 不存在，不报错


class TestEdgeCases(unittest.TestCase):
    """边界情况测试"""
    
    def test_single_point_interval(self):
        """测试单点区间"""
        i = Interval(5, 5)
        self.assertEqual(len(i), 1)
        self.assertIn(5, i)
    
    def test_large_numbers(self):
        """测试大数"""
        s = IntervalSet()
        s.add(Interval(1, 1000000))
        
        self.assertEqual(s.total_length, 1000000)
        self.assertTrue(s.contains(500000))
    
    def test_negative_numbers(self):
        """测试负数"""
        s = IntervalSet()
        s.add(Interval(-10, -5))
        s.add(Interval(-3, 3))
        
        self.assertTrue(s.contains(-7))
        self.assertTrue(s.contains(0))
        self.assertFalse(s.contains(-4))
    
    def test_empty_operations(self):
        """测试空集合操作"""
        s1 = IntervalSet()
        s2 = IntervalSet([Interval(1, 10)])
        
        # 空集合并集
        result = s1.union(s2)
        self.assertEqual(len(result), 1)
        
        # 空集合交集
        result = s1.intersection(s2)
        self.assertTrue(result.is_empty)
        
        # 空集合差集
        result = s2.difference(s1)
        self.assertEqual(len(result), 1)
    
    def test_adjacent_merge_chain(self):
        """测试连续相邻合并"""
        s = IntervalSet()
        for i in range(0, 100, 2):
            s.add(Interval(i, i + 1))
        
        # 所有区间都应该合并成一个
        self.assertEqual(len(s), 1)
        self.assertEqual(s.min_value, 0)
        self.assertEqual(s.max_value, 99)


if __name__ == "__main__":
    unittest.main(verbosity=2)
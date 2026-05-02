"""
背包问题工具模块测试

测试所有背包问题求解功能
"""

import unittest
from mod import (
    Item,
    KnapsackResult,
    KnapsackMethod,
    knapsack_01,
    knapsack_complete,
    knapsack_multiple,
    knapsack_fractional,
    knapsack_multi_dim,
    knapsack_multi_objective,
    knapsack_subset_sum,
    knapsack_min_items,
    knapsack_all_solutions,
    unbounded_knapsack,
    bounded_knapsack
)


class TestItem(unittest.TestCase):
    """测试 Item 类"""
    
    def test_item_creation(self):
        """测试物品创建"""
        item = Item(10, 60, "A")
        self.assertEqual(item.weight, 10)
        self.assertEqual(item.value, 60)
        self.assertEqual(item.name, "A")
        self.assertEqual(item.count, 1)
    
    def test_item_ratio(self):
        """测试价值密度计算"""
        item = Item(10, 60)
        self.assertEqual(item.ratio, 6.0)
    
    def test_item_zero_weight(self):
        """测试零重量物品"""
        item = Item(0, 60)
        self.assertEqual(item.ratio, float('inf'))
    
    def test_item_auto_name(self):
        """测试自动命名"""
        item = Item(10, 60)
        self.assertTrue(item.name.startswith("item_"))


class TestKnapsack01(unittest.TestCase):
    """测试 0/1 背包问题"""
    
    def setUp(self):
        self.items = [
            Item(10, 60, "A"),
            Item(20, 100, "B"),
            Item(30, 120, "C")
        ]
        self.capacity = 50
    
    def test_basic_knapsack(self):
        """测试基本 0/1 背包"""
        result = knapsack_01(self.items, self.capacity)
        
        # 最优解：B+C = 20+30=50重量，价值100+120=220
        self.assertEqual(result.max_value, 220.0)
        self.assertIn("B", [i.name for i in result.selected_items])
        self.assertIn("C", [i.name for i in result.selected_items])
    
    def test_dp_method(self):
        """测试动态规划方法"""
        result = knapsack_01(self.items, self.capacity, KnapsackMethod.DP)
        self.assertEqual(result.max_value, 220.0)
    
    def test_dp_optimized_method(self):
        """测试空间优化动态规划"""
        result = knapsack_01(self.items, self.capacity, KnapsackMethod.DP_OPTIMIZED)
        self.assertEqual(result.max_value, 220.0)
    
    def test_recursive_method(self):
        """测试递归方法"""
        result = knapsack_01(self.items, self.capacity, KnapsackMethod.RECURSIVE)
        self.assertEqual(result.max_value, 220.0)
    
    def test_branch_bound_method(self):
        """测试分支限界法"""
        result = knapsack_01(self.items, self.capacity, KnapsackMethod.BRANCH_BOUND)
        self.assertEqual(result.max_value, 220.0)
    
    def test_zero_capacity(self):
        """测试零容量"""
        result = knapsack_01(self.items, 0)
        self.assertEqual(result.max_value, 0.0)
    
    def test_small_capacity(self):
        """测试小容量"""
        result = knapsack_01(self.items, 15)
        self.assertEqual(result.max_value, 60.0)
    
    def test_large_capacity(self):
        """测试大容量"""
        result = knapsack_01(self.items, 100)
        self.assertEqual(result.max_value, 280.0)  # 选所有
    
    def test_single_item(self):
        """测试单个物品"""
        items = [Item(10, 60, "A")]
        result = knapsack_01(items, 15)
        self.assertEqual(result.max_value, 60.0)
    
    def test_zero_weight_item(self):
        """测试零重量物品"""
        items = [Item(0, 100, "Free"), Item(10, 60, "A")]
        result = knapsack_01(items, 0)
        self.assertEqual(result.max_value, 100.0)
    
    def test_invalid_capacity(self):
        """测试无效容量"""
        with self.assertRaises(ValueError):
            knapsack_01(self.items, -10)
    
    def test_empty_items(self):
        """测试空物品列表"""
        with self.assertRaises(ValueError):
            knapsack_01([], 50)
    
    def test_negative_weight_item(self):
        """测试负重量物品"""
        items = [Item(-10, 60, "A")]
        with self.assertRaises(ValueError):
            knapsack_01(items, 50)
    
    def test_negative_value_item(self):
        """测试负价值物品"""
        items = [Item(10, -60, "A")]
        with self.assertRaises(ValueError):
            knapsack_01(items, 50)
    
    def test_float_capacity(self):
        """测试浮点容量"""
        result = knapsack_01(self.items, 50.5)
        self.assertGreater(result.max_value, 0)
    
    def test_consistency_across_methods(self):
        """测试不同方法结果一致性"""
        methods = [
            KnapsackMethod.DP,
            KnapsackMethod.DP_OPTIMIZED,
            KnapsackMethod.RECURSIVE,
            KnapsackMethod.BRANCH_BOUND
        ]
        
        results = [knapsack_01(self.items, self.capacity, m) for m in methods]
        
        # 所有方法应该得到相同的最大价值
        values = [r.max_value for r in results]
        self.assertEqual(len(set(values)), 1, f"不同方法得到不同结果: {values}")


class TestKnapsackComplete(unittest.TestCase):
    """测试完全背包问题"""
    
    def test_basic_complete(self):
        """测试基本完全背包"""
        items = [Item(1, 1, "X"), Item(3, 4, "Y"), Item(4, 5, "Z")]
        result = knapsack_complete(items, 6)
        
        # 最优解：2个Y（重量6，价值8）
        # 或6个X（重量6，价值6）
        self.assertEqual(result.max_value, 8.0)
    
    def test_multiple_same_item(self):
        """测试选择多个相同物品"""
        items = [Item(1, 2, "Coin")]
        result = knapsack_complete(items, 5)
        
        self.assertEqual(result.max_value, 10.0)  # 5个硬币
        self.assertEqual(len(result.selected_items), 5)
    
    def test_capacity_not_divisible(self):
        """测试容量不能整除物品重量"""
        items = [Item(3, 5, "A")]
        result = knapsack_complete(items, 7)
        
        # 只能选2个（重量6）
        self.assertEqual(result.max_value, 10.0)
    
    def test_compare_with_01(self):
        """测试与0/1背包的比较"""
        items = [Item(5, 10, "A")]
        
        result_01 = knapsack_01(items, 15)
        result_complete = knapsack_complete(items, 15)
        
        # 完全背包可以选多次
        self.assertEqual(result_01.max_value, 10.0)
        self.assertEqual(result_complete.max_value, 30.0)


class TestKnapsackMultiple(unittest.TestCase):
    """测试多重背包问题"""
    
    def test_basic_multiple(self):
        """测试基本多重背包"""
        items = [
            Item(2, 3, "A", count=2),
            Item(3, 4, "B", count=1)
        ]
        result = knapsack_multiple(items, 6)
        
        # 可以选2个A（价值6）或1A+1B（价值7）或2个B不行（只有1个B）
        self.assertEqual(result.max_value, 7.0)
    
    def test_limited_by_count(self):
        """测试数量限制"""
        items = [Item(1, 10, "Rare", count=1)]
        result = knapsack_multiple(items, 100)
        
        # 虽然容量够，但只能选1个
        self.assertEqual(result.max_value, 10.0)
        self.assertEqual(len(result.selected_items), 1)
    
    def test_unlimited_equals_complete(self):
        """测试大数量等同于完全背包"""
        items = [Item(1, 2, "A", count=100)]  # count足够大
        
        result_multiple = knapsack_multiple(items, 5)
        result_complete = knapsack_complete([Item(1, 2, "A")], 5)
        
        self.assertEqual(result_multiple.max_value, result_complete.max_value)


class TestKnapsackFractional(unittest.TestCase):
    """测试分数背包问题"""
    
    def test_basic_fractional(self):
        """测试基本分数背包"""
        items = [
            Item(10, 60, "A"),
            Item(20, 100, "B"),
            Item(30, 120, "C")
        ]
        value, weight, selected = knapsack_fractional(items, 50)
        
        # 按价值密度：A(6), B(5), C(4)
        # 选A(10) + B(20) = 30重量，价值160
        # 还剩20，选C的20/30 = 2/3
        self.assertEqual(value, 240.0)  # 60 + 100 + 120*(20/30) = 240
        self.assertEqual(weight, 50.0)
    
    def test_full_items(self):
        """测试完全装下物品"""
        items = [Item(5, 10, "A"), Item(5, 10, "B")]
        value, weight, selected = knapsack_fractional(items, 20)
        
        # 可以完全装下
        self.assertEqual(value, 20.0)
        self.assertEqual(weight, 10.0)
    
    def test_fractional_selection(self):
        """测试部分选择"""
        items = [Item(100, 50, "Big")]
        value, weight, selected = knapsack_fractional(items, 50)
        
        # 只能选一半
        self.assertEqual(value, 25.0)
        self.assertEqual(weight, 50.0)
        self.assertEqual(len(selected), 1)
        self.assertAlmostEqual(selected[0][1], 0.5, places=2)
    
    def test_zero_capacity(self):
        """测试零容量"""
        items = [Item(10, 60, "A")]
        value, weight, selected = knapsack_fractional(items, 0)
        
        self.assertEqual(value, 0.0)
        self.assertEqual(weight, 0.0)
        self.assertEqual(len(selected), 0)


class TestKnapsackMultiDim(unittest.TestCase):
    """测试多维背包问题"""
    
    def test_2d_knapsack(self):
        """测试二维背包"""
        # weight 作为重量，count 作为体积
        items = [
            Item(2, 3, "A", count=2),  # 重量2，体积2
            Item(3, 4, "B", count=3)   # 重量3，体积3
        ]
        capacities = [5, 5]  # 重量容量5，体积容量5
        
        result = knapsack_multi_dim(items, capacities)
        
        self.assertGreater(result.max_value, 0)
        # 检查约束满足
        total_weight = sum(items[i].weight for i in result.selected_indices)
        total_volume = sum(items[i].count for i in result.selected_indices)
        self.assertLessEqual(total_weight, capacities[0])
        self.assertLessEqual(total_volume, capacities[1])
    
    def test_1d_fallback(self):
        """测试一维退化为普通背包"""
        items = [Item(10, 60, "A")]
        result = knapsack_multi_dim(items, [50])
        
        self.assertEqual(result.max_value, 60.0)
    
    def test_empty_capacities(self):
        """测试空容量列表"""
        items = [Item(10, 60, "A")]
        with self.assertRaises(ValueError):
            knapsack_multi_dim(items, [])


class TestKnapsackMultiObjective(unittest.TestCase):
    """测试多目标背包问题"""
    
    def test_pareto_front(self):
        """测试帕累托前沿"""
        items = [
            Item(1, 10, "Light"),
            Item(10, 100, "Heavy")
        ]
        results = knapsack_multi_objective(items, 15)
        
        # 应该找到帕累托最优解
        self.assertGreater(len(results), 0)
        
        # 验证帕累托最优性
        for result in results:
            self.assertLessEqual(result.total_weight, 15)
    
    def test_single_item(self):
        """测试单物品"""
        items = [Item(5, 10, "A")]
        results = knapsack_multi_objective(items, 10)
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].max_value, 10.0)


class TestKnapsackSubsetSum(unittest.TestCase):
    """测试子集和问题"""
    
    def test_find_subset(self):
        """测试找到子集"""
        items = [Item(3, 3, "A"), Item(5, 5, "B"), Item(7, 7, "C")]
        found, indices = knapsack_subset_sum(items, 8)
        
        self.assertTrue(found)
        total = sum(items[i].weight for i in indices)
        self.assertEqual(total, 8)
    
    def test_no_subset(self):
        """测试无解"""
        items = [Item(3, 3, "A"), Item(5, 5, "B")]
        found, indices = knapsack_subset_sum(items, 4)
        
        self.assertFalse(found)
    
    def test_with_numbers(self):
        """测试纯数值输入"""
        found, indices = knapsack_subset_sum([3, 5, 7], 8)
        self.assertTrue(found)
    
    def test_zero_target(self):
        """测试目标和为零"""
        items = [Item(3, 3, "A"), Item(5, 5, "B")]
        found, indices = knapsack_subset_sum(items, 0)
        
        self.assertTrue(found)
        self.assertEqual(len(indices), 0)


class TestKnapsackMinItems(unittest.TestCase):
    """测试最小物品数背包"""
    
    def test_min_items(self):
        """测试最小物品数"""
        items = [
            Item(5, 50, "High"),
            Item(2, 20, "Medium"),
            Item(1, 10, "Low")
        ]
        result = knapsack_min_items(items, 10, 60)
        
        self.assertIsNotNone(result)
        self.assertGreaterEqual(result.max_value, 60)
    
    def test_impossible(self):
        """测试无法达到最小价值"""
        items = [Item(5, 10, "A")]
        result = knapsack_min_items(items, 10, 100)
        
        self.assertIsNone(result)
    
    def test_zero_min_value(self):
        """测试零最小价值"""
        items = [Item(5, 10, "A")]
        result = knapsack_min_items(items, 10, 0)
        
        # 当 min_value=0 时，最少物品方案是选0个物品
        self.assertIsNotNone(result)
        self.assertEqual(result.max_value, 0.0)
        self.assertEqual(len(result.selected_items), 0)


class TestKnapsackAllSolutions(unittest.TestCase):
    """测试所有最优解"""
    
    def test_multiple_solutions(self):
        """测试多个最优解"""
        # 构造一个有多个最优解的案例
        items = [
            Item(5, 10, "A"),
            Item(5, 10, "B"),
            Item(5, 10, "C")
        ]
        solutions = knapsack_all_solutions(items, 10, max_solutions=10)
        
        self.assertGreater(len(solutions), 0)
        
        # 所有解的价值应该相同
        values = [s.max_value for s in solutions]
        self.assertEqual(len(set(values)), 1)
    
    def test_unique_solution(self):
        """测试唯一解"""
        items = [
            Item(10, 60, "Best"),
            Item(5, 20, "Worse")
        ]
        solutions = knapsack_all_solutions(items, 10)
        
        self.assertEqual(len(solutions), 1)
        self.assertEqual(solutions[0].max_value, 60.0)


class TestUnboundedKnapsack(unittest.TestCase):
    """测试无界背包（完全背包别名）"""
    
    def test_unbounded_equals_complete(self):
        """测试无界背包等于完全背包"""
        items = [Item(1, 2, "Coin")]
        
        result_unbounded = unbounded_knapsack(items, 5)
        result_complete = knapsack_complete(items, 5)
        
        self.assertEqual(result_unbounded.max_value, result_complete.max_value)


class TestBoundedKnapsack(unittest.TestCase):
    """测试有界背包"""
    
    def test_bounded(self):
        """测试有界背包"""
        items = [Item(1, 10, "A"), Item(2, 20, "B")]
        bounds = {0: 3, 1: 1}  # A最多3个，B最多1个
        
        result = bounded_knapsack(items, 10, bounds)
        
        self.assertGreater(result.max_value, 0)


class TestEdgeCases(unittest.TestCase):
    """测试边缘情况"""
    
    def test_large_values(self):
        """测试较大数值"""
        items = [Item(100, 500, "Big")]
        result = knapsack_01(items, 200)
        
        self.assertEqual(result.max_value, 500.0)
    
    def test_many_items(self):
        """测试大量物品"""
        items = [Item(i % 10 + 1, i * 2, f"Item_{i}") for i in range(1, 51)]
        result = knapsack_01(items, 100)
        
        self.assertGreater(result.max_value, 0)
    
    def test_float_weights(self):
        """测试浮点重量"""
        items = [Item(1.5, 10, "A"), Item(2.3, 15, "B")]
        result = knapsack_01(items, 3.0)
        
        self.assertGreater(result.max_value, 0)
    
    def test_all_same_weight(self):
        """测试所有物品重量相同"""
        items = [Item(5, 10, "A"), Item(5, 20, "B"), Item(5, 30, "C")]
        result = knapsack_01(items, 10)
        
        self.assertEqual(result.max_value, 50.0)  # 选B和C
    
    def test_all_same_value(self):
        """测试所有物品价值相同"""
        items = [Item(5, 10, "A"), Item(10, 10, "B"), Item(15, 10, "C")]
        result = knapsack_01(items, 15)
        
        # 应该选重量最小的组合
        self.assertEqual(result.max_value, 20.0)  # 选A和B或只选C


class TestResultFormat(unittest.TestCase):
    """测试结果格式"""
    
    def test_result_fields(self):
        """测试结果字段"""
        items = [Item(10, 60, "A"), Item(20, 100, "B")]
        result = knapsack_01(items, 30)
        
        self.assertIsInstance(result.max_value, float)
        # total_weight may be int or float depending on input
        self.assertIsInstance(result.total_weight, (int, float))
        self.assertIsInstance(result.selected_items, list)
        self.assertIsInstance(result.selected_indices, list)
    
    def test_result_repr(self):
        """测试结果字符串表示"""
        items = [Item(10, 60, "A")]
        result = knapsack_01(items, 15)
        
        repr_str = repr(result)
        self.assertIn("max_value", repr_str)
        self.assertIn("total_weight", repr_str)


if __name__ == "__main__":
    unittest.main(verbosity=2)
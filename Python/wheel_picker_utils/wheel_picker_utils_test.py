"""
wheel_picker_utils 测试文件
"""

import unittest
import sys
import os

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from wheel_picker_utils.mod import (
    WheelPicker,
    create_simple_wheel,
    create_weighted_wheel,
    quick_pick,
    weighted_pick,
    pair_up,
    group_items,
    round_robin_picker,
    deterministic_pick,
    shuffle_with_seed,
    generate_rotation_schedule,
    TournamentWheel,
    PrizeWheel,
    DecisionWheel
)


class TestWheelPicker(unittest.TestCase):
    """测试 WheelPicker 类"""
    
    def test_create_simple_wheel(self):
        """测试创建简单转盘"""
        items = ["A", "B", "C", "D"]
        wheel = WheelPicker(items)
        
        self.assertEqual(len(wheel.items), 4)
        self.assertEqual(len(wheel.weights), 4)
        self.assertEqual(len(wheel.colors), 4)
        
        # 检查等权重
        for weight in wheel.weights:
            self.assertAlmostEqual(weight, 0.25)
    
    def test_create_weighted_wheel(self):
        """测试创建加权转盘"""
        items = ["A", "B", "C"]
        weights = [1, 2, 3]
        wheel = WheelPicker(items, weights=weights)
        
        self.assertEqual(len(wheel.items), 3)
        self.assertAlmostEqual(wheel.weights[0], 1/6)
        self.assertAlmostEqual(wheel.weights[1], 2/6)
        self.assertAlmostEqual(wheel.weights[2], 3/6)
    
    def test_spin_returns_valid_item(self):
        """测试旋转返回有效项"""
        items = ["A", "B", "C", "D"]
        wheel = WheelPicker(items)
        
        result = wheel.spin()
        
        self.assertIn(result["item"], items)
        self.assertIn("probability", result)
        self.assertIn("color", result)
        self.assertIn("timestamp", result)
    
    def test_spin_multiple(self):
        """测试多次旋转"""
        items = ["A", "B", "C", "D"]
        wheel = WheelPicker(items)
        
        results = wheel.spin_multiple(3, unique=True)
        
        self.assertEqual(len(results), 3)
        
        # 检查所有结果都是有效项
        for result in results:
            self.assertIn(result["item"], items)
        
        # 检查唯一性
        selected_items = [r["item"] for r in results]
        self.assertEqual(len(selected_items), len(set(selected_items)))
    
    def test_spin_with_exclusion(self):
        """测试排除选择"""
        items = ["A", "B", "C", "D"]
        wheel = WheelPicker(items)
        
        # 选择几次，排除之前选择的
        results = []
        for _ in range(4):
            result = wheel.spin(exclude_previous=True)
            results.append(result)
        
        # 每次选择应该是不同的
        selected_items = [r["item"] for r in results]
        self.assertEqual(len(set(selected_items)), 4)
    
    def test_deterministic_spin(self):
        """测试确定性选择"""
        items = ["A", "B", "C", "D"]
        wheel = WheelPicker(items)
        
        # 相同种子应该产生相同结果
        result1 = wheel.spin(deterministic=True, seed="test_seed")
        result2 = wheel.spin(deterministic=True, seed="test_seed")
        
        # 注意：由于历史记录的影响，第二次选择可能不同
        # 但我们重置历史后再测试
        wheel.reset_history()
        result1 = wheel.spin(deterministic=True, seed="test_seed")
        wheel.reset_history()
        result2 = wheel.spin(deterministic=True, seed="test_seed")
        
        self.assertEqual(result1["item"], result2["item"])
    
    def test_history_tracking(self):
        """测试历史记录"""
        items = ["A", "B", "C", "D"]
        wheel = WheelPicker(items)
        
        for _ in range(5):
            wheel.spin()
        
        history = wheel.get_history()
        self.assertEqual(len(history), 5)
        
        # 测试限制数量
        limited_history = wheel.get_history(limit=3)
        self.assertEqual(len(limited_history), 3)
    
    def test_statistics(self):
        """测试统计功能"""
        items = ["A", "B", "C", "D"]
        wheel = WheelPicker(items)
        
        # 进行大量选择以测试统计
        for _ in range(100):
            wheel.spin()
        
        stats = wheel.get_statistics()
        
        self.assertEqual(stats["total_spins"], 100)
        self.assertIn("distribution", stats)
        self.assertIn("most_frequent", stats)
        self.assertIn("least_frequent", stats)
    
    def test_reset_history(self):
        """测试重置历史"""
        items = ["A", "B", "C", "D"]
        wheel = WheelPicker(items)
        
        for _ in range(5):
            wheel.spin()
        
        wheel.reset_history()
        history = wheel.get_history()
        self.assertEqual(len(history), 0)
    
    def test_add_item(self):
        """测试添加项目"""
        items = ["A", "B", "C"]
        wheel = WheelPicker(items)
        
        wheel.add_item("D")
        
        self.assertEqual(len(wheel.items), 4)
        self.assertIn("D", wheel.items)
    
    def test_remove_item(self):
        """测试移除项目"""
        items = ["A", "B", "C"]
        wheel = WheelPicker(items)
        
        wheel.remove_item("B")
        
        self.assertEqual(len(wheel.items), 2)
        self.assertNotIn("B", wheel.items)
    
    def test_update_weight(self):
        """测试更新权重"""
        items = ["A", "B", "C"]
        weights = [1, 1, 1]
        wheel = WheelPicker(items, weights=weights)
        
        wheel.update_weight("A", 2)
        
        # A 的权重应该增加
        self.assertGreater(wheel.weights[wheel.items.index("A")], 1/4)
    
    def test_wheel_config(self):
        """测试转盘配置"""
        items = ["A", "B", "C", "D"]
        wheel = WheelPicker(items)
        
        config = wheel.get_wheel_config()
        
        self.assertEqual(config["title"], "选择转盘")
        self.assertEqual(config["item_count"], 4)
        self.assertEqual(len(config["segments"]), 4)
    
    def test_empty_items_raises_error(self):
        """测试空列表抛出错误"""
        with self.assertRaises(ValueError):
            WheelPicker([])
    
    def test_mismatched_weights_raises_error(self):
        """测试权重数量不匹配抛出错误"""
        items = ["A", "B", "C"]
        weights = [1, 2]  # 只有2个权重
        
        with self.assertRaises(ValueError):
            WheelPicker(items, weights=weights)


class TestUtilityFunctions(unittest.TestCase):
    """测试工具函数"""
    
    def test_create_simple_wheel(self):
        """测试创建简单转盘函数"""
        items = ["A", "B", "C"]
        wheel = create_simple_wheel(items)
        
        self.assertIsInstance(wheel, WheelPicker)
        self.assertEqual(len(wheel.items), 3)
    
    def test_create_weighted_wheel(self):
        """测试创建加权转盘函数"""
        items = ["A", "B", "C"]
        weights = [1, 2, 3]
        wheel = create_weighted_wheel(items, weights)
        
        self.assertIsInstance(wheel, WheelPicker)
        self.assertEqual(len(wheel.items), 3)
    
    def test_quick_pick(self):
        """测试快速选择"""
        items = ["A", "B", "C", "D", "E"]
        
        result = quick_pick(items, count=3, unique=True)
        
        self.assertEqual(len(result), 3)
        for item in result:
            self.assertIn(item, items)
        
        # 测试唯一性
        self.assertEqual(len(result), len(set(result)))
    
    def test_quick_pick_non_unique(self):
        """测试非唯一快速选择"""
        items = ["A", "B", "C"]
        
        result = quick_pick(items, count=5, unique=False)
        
        self.assertEqual(len(result), 5)
        # 可能包含重复项
    
    def test_weighted_pick(self):
        """测试加权选择"""
        items = ["A", "B", "C"]
        weights = [1, 2, 3]
        
        result = weighted_pick(items, weights, count=1)
        
        self.assertEqual(len(result), 1)
        self.assertIn(result[0], items)
    
    def test_weighted_pick_unique(self):
        """测试加权唯一选择"""
        items = ["A", "B", "C", "D"]
        weights = [1, 2, 3, 4]
        
        result = weighted_pick(items, weights, count=3, unique=True)
        
        self.assertEqual(len(result), 3)
        self.assertEqual(len(result), len(set(result)))
    
    def test_pair_up(self):
        """测试配对"""
        items = ["A", "B", "C", "D", "E"]
        
        pairs = pair_up(items, randomize=True)
        
        # 5个项目应该产生2个完整配对 + 1个单
        self.assertEqual(len(pairs), 3)
        
        # 检查所有项目都被分配
        all_items = set()
        for p1, p2 in pairs:
            all_items.add(p1)
            if p2:
                all_items.add(p2)
        
        self.assertEqual(len(all_items), 5)
    
    def test_group_items(self):
        """测试分组"""
        items = ["A", "B", "C", "D", "E", "F"]
        
        groups = group_items(items, group_count=3, balance=True)
        
        self.assertEqual(len(groups), 3)
        
        # 检查所有项目都被分配
        all_items = set()
        for group in groups:
            all_items.update(group)
        
        self.assertEqual(len(all_items), 6)
    
    def test_round_robin_picker(self):
        """测试轮转选择"""
        items = ["A", "B", "C"]
        
        result = round_robin_picker(items, rounds=2)
        
        self.assertEqual(len(result), 6)
        self.assertEqual(result, ["A", "B", "C", "A", "B", "C"])
    
    def test_deterministic_pick(self):
        """测试确定性选择"""
        items = ["A", "B", "C", "D"]
        
        # 相同种子应该产生相同结果
        result1 = deterministic_pick(items, "test_seed")
        result2 = deterministic_pick(items, "test_seed")
        
        self.assertEqual(result1, result2)
    
    def test_shuffle_with_seed(self):
        """测试种子打乱"""
        items = ["A", "B", "C", "D", "E"]
        
        # 相同种子应该产生相同打乱结果
        result1 = shuffle_with_seed(items, "test_seed")
        result2 = shuffle_with_seed(items, "test_seed")
        
        self.assertEqual(result1, result2)
        self.assertEqual(set(result1), set(items))
    
    def test_generate_rotation_schedule(self):
        """测试生成轮转排班表"""
        items = ["A", "B", "C"]
        
        schedule = generate_rotation_schedule(items, days=7, start_date="2024-01-01", shuffle=False)
        
        self.assertEqual(len(schedule), 7)
        
        # 检查日期连续
        for i, entry in enumerate(schedule):
            self.assertEqual(entry["rotation_position"], i % 3)


class TestTournamentWheel(unittest.TestCase):
    """测试锦标赛转盘"""
    
    def test_create_tournament(self):
        """测试创建锦标赛"""
        participants = ["A", "B", "C", "D"]
        tournament = TournamentWheel(participants)
        
        self.assertEqual(len(tournament.participants), 4)
    
    def test_generate_matches(self):
        """测试生成对阵"""
        participants = ["A", "B", "C", "D"]
        tournament = TournamentWheel(participants)
        
        matches = tournament.generate_matches(rounds=1, randomize=True)
        
        self.assertEqual(len(matches), 2)  # 4个参与者 -> 2场对阵
    
    def test_pick_winner(self):
        """测试选择赢家"""
        participants = ["A", "B", "C", "D"]
        tournament = TournamentWheel(participants)
        tournament.generate_matches(rounds=1)
        
        winner = tournament.pick_winner(1, 1)
        
        self.assertIn(winner, ["A", "B", "C", "D"])
    
    def test_get_bracket(self):
        """测试获取对阵图"""
        participants = ["A", "B", "C", "D"]
        tournament = TournamentWheel(participants)
        tournament.generate_matches(rounds=1)
        
        bracket = tournament.get_bracket()
        
        self.assertEqual(bracket["participant_count"], 4)
        self.assertIn("matches", bracket)


class TestPrizeWheel(unittest.TestCase):
    """测试奖品转盘"""
    
    def test_create_prize_wheel(self):
        """测试创建奖品转盘"""
        prizes = ["一等奖", "二等奖", "三等奖", "未中奖"]
        wheel = PrizeWheel(prizes)
        
        self.assertEqual(len(wheel.available_prizes), 4)
    
    def test_draw(self):
        """测试抽奖"""
        prizes = ["一等奖", "二等奖", "三等奖"]
        wheel = PrizeWheel(prizes)
        
        result = wheel.draw("张三")
        
        self.assertIn("prize", result)
        self.assertEqual(result["participant"], "张三")
        self.assertTrue(result["success"])
    
    def test_draw_multiple(self):
        """测试多人抽奖"""
        prizes = ["一等奖", "二等奖", "三等奖"]
        participants = ["张三", "李四", "王五"]
        
        wheel = PrizeWheel(prizes)
        results = wheel.draw_multiple(participants)
        
        self.assertEqual(len(results), 3)
    
    def test_prize_exhaustion(self):
        """测试奖品耗尽"""
        prizes = ["一等奖", "二等奖"]
        wheel = PrizeWheel(prizes, allow_repeat=False)
        
        wheel.draw()
        wheel.draw()
        
        # 所有奖品已抽完
        result = wheel.draw()
        
        self.assertFalse(result["success"])
    
    def test_allow_repeat(self):
        """测试允许重复"""
        prizes = ["一等奖", "二等奖"]
        wheel = PrizeWheel(prizes, allow_repeat=True)
        
        # 可以重复抽取
        for _ in range(10):
            result = wheel.draw()
            self.assertTrue(result["success"])


class TestDecisionWheel(unittest.TestCase):
    """测试决策转盘"""
    
    def test_create_with_options(self):
        """测试使用选项创建"""
        options = ["A", "B", "C"]
        wheel = DecisionWheel(options=options)
        
        self.assertEqual(len(wheel.options), 3)
    
    def test_create_with_preset(self):
        """测试使用预设创建"""
        wheel = DecisionWheel(preset="food")
        
        self.assertEqual(len(wheel.options), 8)
        self.assertIn("火锅", wheel.options)
    
    def test_invalid_preset(self):
        """测试无效预设"""
        with self.assertRaises(ValueError):
            DecisionWheel(preset="invalid_preset")
    
    def test_make_decision(self):
        """测试做出决策"""
        wheel = DecisionWheel(preset="food")
        
        result = wheel.make_decision(person="张三")
        
        self.assertIn("decision", result)
        self.assertIn(result["decision"], wheel.options)
        self.assertEqual(result["person"], "张三")
    
    def test_decision_with_exclusion(self):
        """测试带排除的决策"""
        wheel = DecisionWheel(preset="food")
        
        # 连续决策，排除最近的选择
        decisions = []
        for _ in range(5):
            decision = wheel.make_decision(exclude_recent=3)
            decisions.append(decision["decision"])
        
        # 检查有足够的变化
        unique_count = len(set(decisions))
        self.assertGreater(unique_count, 1)
    
    def test_add_remove_option(self):
        """测试添加移除选项"""
        wheel = DecisionWheel(preset="food")
        
        original_count = len(wheel.options)
        
        wheel.add_option("新选项")
        self.assertEqual(len(wheel.options), original_count + 1)
        
        wheel.remove_option("火锅")
        self.assertNotIn("火锅", wheel.options)
    
    def test_get_presets(self):
        """测试获取预设"""
        presets = DecisionWheel(preset="food").get_presets()
        
        self.assertIn("food", presets)
        self.assertIn("movie_genre", presets)
    
    def test_decision_stats(self):
        """测试决策统计"""
        wheel = DecisionWheel(preset="food")
        
        for _ in range(20):
            wheel.make_decision()
        
        stats = wheel.get_decision_stats()
        
        self.assertEqual(stats["total_decisions"], 20)
        self.assertIn("distribution", stats)


class TestWeightedDistribution(unittest.TestCase):
    """测试加权分布"""
    
    def test_weighted_distribution_accuracy(self):
        """测试加权分布准确性"""
        items = ["A", "B", "C"]
        weights = [1, 2, 7]  # A: 10%, B: 20%, C: 70%
        wheel = WheelPicker(items, weights=weights)
        
        # 大量测试
        counts = {"A": 0, "B": 0, "C": 0}
        for _ in range(1000):
            result = wheel.spin()
            counts[result["item"]] += 1
        
        # 检查分布大致正确（C应该出现最多）
        self.assertGreater(counts["C"], counts["B"])
        self.assertGreater(counts["B"], counts["A"])
        
        # C应该占约70%
        c_ratio = counts["C"] / 1000
        self.assertGreater(c_ratio, 0.6)  # 允许一定误差
        self.assertLess(c_ratio, 0.8)


class TestColorGeneration(unittest.TestCase):
    """测试颜色生成"""
    
    def test_auto_color_generation(self):
        """测试自动颜色生成"""
        items = ["A", "B", "C", "D"]
        wheel = WheelPicker(items)
        
        # 应该有颜色
        self.assertEqual(len(wheel.colors), 4)
        
        # 颜色应该是有效的十六进制格式
        for color in wheel.colors:
            self.assertTrue(color.startswith("#"))
            self.assertEqual(len(color), 7)
    
    def test_many_items_color_generation(self):
        """测试多项目颜色生成"""
        items = [f"Item{i}" for i in range(20)]
        wheel = WheelPicker(items)
        
        self.assertEqual(len(wheel.colors), 20)
        
        # 颜色应该都是唯一的（或接近唯一）
        unique_colors = len(set(wheel.colors))
        self.assertGreater(unique_colors, 10)


class TestEdgeCases(unittest.TestCase):
    """测试边界情况"""
    
    def test_single_item(self):
        """测试单个项目"""
        items = ["Only"]
        wheel = WheelPicker(items)
        
        result = wheel.spin()
        self.assertEqual(result["item"], "Only")
    
    def test_all_zero_weights_except_one(self):
        """测试只有一个有效权重"""
        items = ["A", "B", "C"]
        weights = [0, 0, 1]
        
        wheel = WheelPicker(items, weights=weights)
        result = wheel.spin()
        
        self.assertEqual(result["item"], "C")
    
    def test_very_large_number_of_spins(self):
        """测试大量旋转"""
        items = ["A", "B", "C"]
        wheel = WheelPicker(items)
        
        # 重置历史后测试
        wheel.reset_history()
        
        for _ in range(1000):
            result = wheel.spin()
            self.assertIn(result["item"], items)
        
        # 历史记录应该增长
        history = wheel.get_history()
        self.assertEqual(len(history), 1000)


def run_tests():
    """运行所有测试"""
    unittest.main(verbosity=2)


if __name__ == "__main__":
    run_tests()
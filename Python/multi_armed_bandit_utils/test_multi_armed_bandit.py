"""
Multi-Armed Bandit 工具模块测试

测试覆盖：
- 各算法的基本选择和更新功能
- 探索-利用权衡行为
- 统计计算正确性
- 边界条件处理
- 实验框架功能
"""

import math
import random
import unittest
from typing import List

# 导入模块
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    BanditAlgorithm,
    BaseBandit,
    Arm,
    EpsilonGreedyBandit,
    UCB1Bandit,
    ThompsonSamplingBandit,
    SoftmaxBandit,
    ExponentialWeightBandit,
    create_bandit,
    BanditExperiment,
    quick_ab_test
)


class TestArm(unittest.TestCase):
    """测试 Arm 类"""
    
    def test_arm_creation(self):
        """测试臂的创建"""
        arm = Arm(name="test_arm")
        self.assertEqual(arm.name, "test_arm")
        self.assertEqual(arm.reward_sum, 0.0)
        self.assertEqual(arm.pull_count, 0)
        self.assertEqual(arm.alpha, 1.0)
        self.assertEqual(arm.beta, 1.0)
    
    def test_arm_update(self):
        """测试臂的更新"""
        arm = Arm(name="test")
        arm.update(1.0)
        self.assertEqual(arm.pull_count, 1)
        self.assertEqual(arm.reward_sum, 1.0)
        
        arm.update(0.5)
        self.assertEqual(arm.pull_count, 2)
        self.assertEqual(arm.reward_sum, 1.5)
    
    def test_arm_average_reward(self):
        """测试平均奖励计算"""
        arm = Arm(name="test")
        self.assertEqual(arm.average_reward, 0.0)
        
        arm.update(1.0)
        arm.update(0.5)
        arm.update(0.5)
        self.assertAlmostEqual(arm.average_reward, 2.0 / 3, places=5)
    
    def test_arm_binary_update(self):
        """测试二值奖励更新（Thompson Sampling 参数）"""
        arm = Arm(name="test")
        
        # 成功
        arm.update(1.0, is_binary=True)
        self.assertEqual(arm.alpha, 2.0)
        self.assertEqual(arm.beta, 1.0)
        
        # 失败
        arm.update(0.0, is_binary=True)
        self.assertEqual(arm.alpha, 2.0)
        self.assertEqual(arm.beta, 2.0)


class TestEpsilonGreedyBandit(unittest.TestCase):
    """测试 Epsilon-Greedy 算法"""
    
    def test_creation(self):
        """测试创建"""
        bandit = EpsilonGreedyBandit(["A", "B", "C"])
        self.assertEqual(len(bandit.arms), 3)
        self.assertEqual(bandit.epsilon, 0.1)
    
    def test_invalid_epsilon(self):
        """测试无效 epsilon 值"""
        with self.assertRaises(ValueError):
            EpsilonGreedyBandit(["A"], epsilon=-0.1)
        with self.assertRaises(ValueError):
            EpsilonGreedyBandit(["A"], epsilon=1.5)
    
    def test_select_exploration(self):
        """测试探索行为（高 epsilon 时应随机选择）"""
        bandit = EpsilonGreedyBandit(["A", "B"], epsilon=0.5)
        
        # 多次选择，应该有一定的分布
        selections = {"A": 0, "B": 0}
        for _ in range(1000):
            arm = bandit.select()
            selections[arm] += 1
        
        # 由于高探索率，两边应该都有选择
        self.assertGreater(selections["A"], 100)
        self.assertGreater(selections["B"], 100)
    
    def test_select_exploitation(self):
        """测试利用行为（低 epsilon 时应选择最优臂）"""
        bandit = EpsilonGreedyBandit(["A", "B"], epsilon=0.0)
        
        # A 的平均奖励更高
        bandit.update("A", 1.0)
        bandit.update("A", 1.0)
        bandit.update("B", 0.0)
        bandit.update("B", 0.0)
        
        # 应该总是选择 A
        for _ in range(100):
            self.assertEqual(bandit.select(), "A")
    
    def test_epsilon_decay(self):
        """测试 epsilon 衰减"""
        bandit = EpsilonGreedyBandit(
            ["A", "B"],
            epsilon=0.5,
            epsilon_decay=0.9,
            min_epsilon=0.01
        )
        
        initial_epsilon = bandit.epsilon
        bandit.update("A", 1.0)
        self.assertLess(bandit.epsilon, initial_epsilon)
    
    def test_reset(self):
        """测试重置功能"""
        bandit = EpsilonGreedyBandit(["A", "B"], epsilon=0.5)
        bandit.update("A", 1.0)
        bandit.update("B", 0.5)
        
        bandit.reset()
        
        self.assertEqual(bandit.total_pulls, 0)
        self.assertEqual(bandit.cumulative_reward, 0.0)
        for arm in bandit.arms.values():
            self.assertEqual(arm.pull_count, 0)


class TestUCB1Bandit(unittest.TestCase):
    """测试 UCB1 算法"""
    
    def test_creation(self):
        """测试创建"""
        bandit = UCB1Bandit(["A", "B", "C"])
        self.assertEqual(len(bandit.arms), 3)
    
    def test_select_unexplored(self):
        """测试未探索臂的优先选择"""
        bandit = UCB1Bandit(["A", "B", "C"])
        
        # 未探索的臂 UCB 值为无穷大，应优先选择
        selected = set()
        for _ in range(10):
            arm = bandit.select()
            selected.add(arm)
            bandit.update(arm, random.random())
        
        # 应该选择过所有臂
        self.assertEqual(len(selected), 3)
    
    def test_ucb_value_calculation(self):
        """测试 UCB 值计算"""
        bandit = UCB1Bandit(["A", "B"])
        
        # 更新一些数据
        bandit.update("A", 1.0)
        bandit.update("A", 1.0)
        bandit.update("B", 0.0)
        
        # A 的 UCB 值应该更高
        ucb_a = bandit._ucb_value(bandit.arms["A"])
        ucb_b = bandit._ucb_value(bandit.arms["B"])
        
        self.assertGreater(ucb_a, ucb_b)
    
    def test_exploration_bonus(self):
        """测试探索奖励随臂探索次数增加而递减"""
        bandit = UCB1Bandit(["A"])
        
        bandit.update("A", 0.5)
        ucb1 = bandit._ucb_value(bandit.arms["A"])
        pull_count_1 = bandit.arms["A"].pull_count
        
        bandit.update("A", 0.5)
        bandit.update("A", 0.5)
        bandit.update("A", 0.5)
        bandit.update("A", 0.5)
        ucb2 = bandit._ucb_value(bandit.arms["A"])
        pull_count_2 = bandit.arms["A"].pull_count
        
        # 更多探索后，该臂的探索奖励应减小（因为 n 增加）
        exploration_bonus_1 = math.sqrt(2 * math.log(bandit.total_pulls) / pull_count_1)
        exploration_bonus_2 = math.sqrt(2 * math.log(bandit.total_pulls) / pull_count_2)
        
        # pull_count 增加后，分母变大，探索奖励减小
        self.assertLess(exploration_bonus_2, exploration_bonus_1)


class TestThompsonSamplingBandit(unittest.TestCase):
    """测试 Thompson Sampling 算法"""
    
    def test_creation(self):
        """测试创建"""
        bandit = ThompsonSamplingBandit(["A", "B"])
        self.assertEqual(len(bandit.arms), 2)
    
    def test_binary_rewards(self):
        """测试二值奖励行为"""
        bandit = ThompsonSamplingBandit(["A", "B"], is_binary=True)
        
        # A 总是成功，B 总是失败
        for _ in range(50):
            bandit.update("A", 1.0, is_binary=True)
            bandit.update("B", 0.0, is_binary=True)
        
        # A 的 alpha 应该很高
        self.assertGreater(bandit.arms["A"].alpha, bandit.arms["A"].beta)
        # B 的 beta 应该很高
        self.assertGreater(bandit.arms["B"].beta, bandit.arms["B"].alpha)
    
    def test_selection_distribution(self):
        """测试选择分布倾向于更优臂"""
        bandit = ThompsonSamplingBandit(["A", "B"])
        
        # 给 A 更多成功
        for _ in range(100):
            bandit.update("A", 1.0, is_binary=True)
        for _ in range(100):
            bandit.update("B", 0.0, is_binary=True)
        
        # 统计选择分布
        selections = {"A": 0, "B": 0}
        for _ in range(1000):
            arm = bandit.select()
            selections[arm] += 1
        
        # A 应该被选择更多次
        self.assertGreater(selections["A"], selections["B"])
    
    def test_continuous_rewards(self):
        """测试连续奖励"""
        bandit = ThompsonSamplingBandit(["A"], is_binary=False)
        
        bandit.update("A", 0.8)
        bandit.update("A", 0.9)
        
        # 应该能处理连续奖励
        self.assertEqual(bandit.arms["A"].pull_count, 2)


class TestSoftmaxBandit(unittest.TestCase):
    """测试 Softmax 算法"""
    
    def test_creation(self):
        """测试创建"""
        bandit = SoftmaxBandit(["A", "B"], temperature=1.0)
        self.assertEqual(len(bandit.arms), 2)
        self.assertEqual(bandit.temperature, 1.0)
    
    def test_invalid_temperature(self):
        """测试无效温度值"""
        with self.assertRaises(ValueError):
            SoftmaxBandit(["A"], temperature=0)
        with self.assertRaises(ValueError):
            SoftmaxBandit(["A"], temperature=-1)
    
    def test_probability_distribution(self):
        """测试概率分布"""
        bandit = SoftmaxBandit(["A", "B"], temperature=1.0)
        
        bandit.update("A", 1.0)
        bandit.update("B", 0.0)
        
        probs = bandit._compute_probabilities()
        
        # 概率和应为 1
        self.assertAlmostEqual(sum(probs.values()), 1.0, places=5)
        
        # A 的概率应该更高
        self.assertGreater(probs["A"], probs["B"])
    
    def test_high_temperature_randomness(self):
        """测试高温度时更随机"""
        bandit = SoftmaxBandit(["A", "B"], temperature=100.0)
        
        bandit.update("A", 1.0)
        bandit.update("B", 0.0)
        
        probs = bandit._compute_probabilities()
        
        # 高温度时概率应该接近均匀分布（约各50%）
        self.assertAlmostEqual(probs["A"], 0.5, delta=0.1)
        self.assertAlmostEqual(probs["B"], 0.5, delta=0.1)
    
    def test_low_temperature_greedy(self):
        """测试低温度时更贪婪"""
        bandit = SoftmaxBandit(["A", "B"], temperature=0.01)
        
        bandit.update("A", 1.0)
        bandit.update("B", 0.0)
        
        probs = bandit._compute_probabilities()
        
        # 低温度时 A 的概率应该接近 1（高奖励的臂）
        self.assertGreater(probs["A"], 0.99)
    
    def test_temperature_decay(self):
        """测试温度衰减"""
        bandit = SoftmaxBandit(
            ["A", "B"],
            temperature=1.0,
            temperature_decay=0.9,
            min_temperature=0.1
        )
        
        initial_temp = bandit.temperature
        bandit.update("A", 1.0)
        
        self.assertLess(bandit.temperature, initial_temp)


class TestExponentialWeightBandit(unittest.TestCase):
    """测试 Exponential-weight 算法"""
    
    def test_creation(self):
        """测试创建"""
        bandit = ExponentialWeightBandit(["A", "B"])
        self.assertEqual(len(bandit.arms), 2)
        self.assertEqual(bandit.gamma, 0.1)
    
    def test_invalid_gamma(self):
        """测试无效 gamma 值"""
        with self.assertRaises(ValueError):
            ExponentialWeightBandit(["A"], gamma=-0.1)
        with self.assertRaises(ValueError):
            ExponentialWeightBandit(["A"], gamma=1.5)
    
    def test_weight_update(self):
        """测试权重更新"""
        bandit = ExponentialWeightBandit(["A", "B"])
        
        initial_weight_a = bandit.arms["A"].weight
        
        bandit.update("A", 1.0)
        
        # 成功的臂权重应该增加
        self.assertGreater(bandit.arms["A"].weight, initial_weight_a)
    
    def test_selection_distribution(self):
        """测试选择分布"""
        bandit = ExponentialWeightBandit(["A", "B"])
        
        # 让 A 更成功
        for _ in range(100):
            bandit.update("A", 1.0)
        for _ in range(100):
            bandit.update("B", 0.0)
        
        # A 应该更常被选择
        selections = {"A": 0, "B": 0}
        for _ in range(1000):
            arm = bandit.select()
            selections[arm] += 1
        
        self.assertGreater(selections["A"], selections["B"])


class TestFactoryFunction(unittest.TestCase):
    """测试工厂函数"""
    
    def test_create_all_types(self):
        """测试创建所有类型的 bandit"""
        arm_names = ["A", "B", "C"]
        
        for algo in BanditAlgorithm:
            bandit = create_bandit(algo, arm_names)
            self.assertIsInstance(bandit, BaseBandit)
            self.assertEqual(len(bandit.arms), 3)
    
    def test_create_with_kwargs(self):
        """测试带参数创建"""
        bandit = create_bandit(
            BanditAlgorithm.EPSILON_GREEDY,
            ["A", "B"],
            epsilon=0.2,
            epsilon_decay=0.95
        )
        self.assertEqual(bandit.epsilon, 0.2)
    
    def test_invalid_algorithm(self):
        """测试无效算法类型"""
        with self.assertRaises(ValueError):
            create_bandit("invalid_algo", ["A", "B"])


class TestBanditExperiment(unittest.TestCase):
    """测试实验框架"""
    
    def test_experiment_run(self):
        """测试实验运行"""
        true_rewards = {"A": 0.8, "B": 0.3, "C": 0.5}
        
        experiment = BanditExperiment(
            arm_names=["A", "B", "C"],
            true_rewards=true_rewards,
            algorithms=[BanditAlgorithm.EPSILON_GREEDY, BanditAlgorithm.UCB1]
        )
        
        results = experiment.run(rounds=100)
        
        self.assertEqual(len(results), 2)
        self.assertIn("epsilon_greedy", results)
        self.assertIn("ucb1", results)
    
    def test_experiment_statistics(self):
        """测试实验统计"""
        true_rewards = {"A": 0.9, "B": 0.1}
        
        experiment = BanditExperiment(
            arm_names=["A", "B"],
            true_rewards=true_rewards,
            algorithms=[BanditAlgorithm.THOMPSON_SAMPLING]
        )
        
        results = experiment.run(rounds=1000)
        
        # 应该发现 A 是最优臂
        best_arm = results["thompson_sampling"]["best_arm_found"]
        self.assertEqual(best_arm, "A")
    
    def test_experiment_ranking(self):
        """测试算法排名"""
        true_rewards = {"A": 0.7, "B": 0.3}
        
        experiment = BanditExperiment(
            arm_names=["A", "B"],
            true_rewards=true_rewards,
            algorithms=list(BanditAlgorithm)
        )
        
        experiment.run(rounds=500)
        ranking = experiment.get_ranking()
        
        # 排名应该有结果
        self.assertEqual(len(ranking), len(BanditAlgorithm))
        
        # 第一个应该是累计奖励最高的
        self.assertIsInstance(ranking[0][1]["cumulative_reward"], float)


class TestQuickABTest(unittest.TestCase):
    """测试快速 A/B 测试"""
    
    def test_basic_ab_test(self):
        """测试基本 A/B 测试"""
        rewards = {
            "control": [1, 1, 0, 1, 0, 1, 1, 0, 1, 1],  # 70%
            "variant": [1, 1, 1, 1, 1, 1, 0, 1, 1, 1],  # 90%
        }
        
        result = quick_ab_test(
            variant_names=["control", "variant"],
            rewards=rewards
        )
        
        self.assertIn("best_variant", result)
        self.assertIn("variant_stats", result)
        self.assertEqual(result["algorithm"], "thompson_sampling")
    
    def test_different_algorithms(self):
        """测试不同算法"""
        rewards = {
            "A": [1, 0, 1],
            "B": [1, 1, 1],
        }
        
        for algo in [BanditAlgorithm.UCB1, BanditAlgorithm.EPSILON_GREEDY]:
            result = quick_ab_test(
                variant_names=["A", "B"],
                rewards=rewards,
                algorithm=algo
            )
            self.assertIn("best_variant", result)


class TestEdgeCases(unittest.TestCase):
    """测试边界条件"""
    
    def test_single_arm(self):
        """测试单臂"""
        for algo in BanditAlgorithm:
            bandit = create_bandit(algo, ["only_one"])
            
            # 总是选择唯一的臂
            self.assertEqual(bandit.select(), "only_one")
            
            bandit.update("only_one", 1.0)
            self.assertEqual(bandit.get_best_arm(), "only_one")
    
    def test_many_arms(self):
        """测试多臂"""
        arms = [f"arm_{i}" for i in range(100)]
        bandit = EpsilonGreedyBandit(arms, epsilon=0.1)
        
        # 应该能正常工作
        for _ in range(1000):
            arm = bandit.select()
            bandit.update(arm, random.random())
        
        self.assertEqual(bandit.total_pulls, 1000)
    
    def test_zero_reward(self):
        """测试零奖励"""
        bandit = EpsilonGreedyBandit(["A", "B"])
        
        for _ in range(10):
            bandit.update("A", 0.0)
            bandit.update("B", 0.0)
        
        self.assertEqual(bandit.cumulative_reward, 0.0)
    
    def test_high_reward(self):
        """测试高奖励"""
        bandit = EpsilonGreedyBandit(["A", "B"])
        
        for _ in range(10):
            bandit.update("A", 1000.0)
        
        self.assertEqual(bandit.cumulative_reward, 10000.0)
    
    def test_negative_reward(self):
        """测试负奖励"""
        bandit = EpsilonGreedyBandit(["A", "B"])
        
        bandit.update("A", -1.0)
        bandit.update("B", 1.0)
        
        self.assertEqual(bandit.cumulative_reward, 0.0)
        self.assertEqual(bandit.get_best_arm(), "B")
    
    def test_empty_arm_names(self):
        """测试空臂数组"""
        with self.assertRaises(ValueError):
            EpsilonGreedyBandit([])


class TestStatistics(unittest.TestCase):
    """测试统计功能"""
    
    def test_arm_stats(self):
        """测试臂统计"""
        bandit = EpsilonGreedyBandit(["A", "B"])
        
        bandit.update("A", 1.0)
        bandit.update("A", 0.0)
        bandit.update("B", 1.0)
        
        stats_a = bandit.get_arm_stats("A")
        
        self.assertEqual(stats_a["name"], "A")
        self.assertEqual(stats_a["pull_count"], 2)
        self.assertEqual(stats_a["reward_sum"], 1.0)
        self.assertEqual(stats_a["average_reward"], 0.5)
    
    def test_all_stats(self):
        """测试全部统计"""
        bandit = EpsilonGreedyBandit(["A", "B"])
        
        bandit.update("A", 1.0)
        bandit.update("B", 1.0)
        
        all_stats = bandit.get_all_stats()
        
        self.assertEqual(len(all_stats), 2)
        self.assertIn("A", all_stats)
        self.assertIn("B", all_stats)
    
    def test_history(self):
        """测试历史记录"""
        bandit = EpsilonGreedyBandit(["A", "B"])
        
        bandit.update("A", 1.0)
        bandit.update("B", 0.5)
        bandit.update("A", 0.8)
        
        history = bandit.history
        
        self.assertEqual(len(history), 3)
        self.assertEqual(history[0]["arm"], "A")
        self.assertEqual(history[0]["reward"], 1.0)
        self.assertEqual(history[1]["arm"], "B")
        self.assertEqual(history[2]["total_pulls"], 3)


class TestIntegration(unittest.TestCase):
    """集成测试"""
    
    def test_real_world_scenario(self):
        """测试真实场景：A/B 测试模拟"""
        random.seed(42)
        
        # 模拟三种广告的点击率
        true_ctr = {
            "ad_A": 0.05,
            "ad_B": 0.08,  # 最佳
            "ad_C": 0.03,
        }
        
        bandit = ThompsonSamplingBandit(
            list(true_ctr.keys()),
            is_binary=True
        )
        
        # 运行 10000 次展示
        total_reward = 0
        optimal_reward = 0.08 * 10000
        
        for _ in range(10000):
            arm = bandit.select()
            reward = 1.0 if random.random() < true_ctr[arm] else 0.0
            bandit.update(arm, reward, is_binary=True)
            total_reward += reward
        
        # 累计奖励应该接近最优
        regret = optimal_reward - total_reward
        
        # 遗憾应该相对较小（Thompson Sampling 效果好）
        self.assertLess(regret, 150)  # 遗憾 < 1.5%
    
    def test_comparison_all_algorithms(self):
        """比较所有算法性能"""
        random.seed(42)
        
        true_rewards = {"A": 0.9, "B": 0.1}
        
        results = {}
        rounds = 1000
        
        for algo in BanditAlgorithm:
            random.seed(42)  # 重置随机种子
            bandit = create_bandit(algo, list(true_rewards.keys()))
            
            for _ in range(rounds):
                arm = bandit.select()
                reward = 1.0 if random.random() < true_rewards[arm] else 0.0
                bandit.update(arm, reward, is_binary=True)
            
            results[algo.value] = bandit.cumulative_reward
        
        # 所有算法应该都能获得不错的奖励
        for algo, reward in results.items():
            self.assertGreater(reward, rounds * 0.5, 
                f"{algo} should get more than 50% optimal reward")


if __name__ == "__main__":
    unittest.main(verbosity=2)
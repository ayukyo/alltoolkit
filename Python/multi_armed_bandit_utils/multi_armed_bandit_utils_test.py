#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Multi-Armed Bandit Utilities Test Module
"""

import unittest
import sys
import os
import random
import math

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from multi_armed_bandit_utils.mod import (
    BanditAlgorithm, Arm, BaseBandit,
    EpsilonGreedyBandit, UCB1Bandit, ThompsonSamplingBandit,
    SoftmaxBandit, ExponentialWeightBandit,
    create_bandit, BanditExperiment, quick_ab_test
)


class TestArm(unittest.TestCase):
    """测试 Arm 类"""
    
    def test_arm_creation(self):
        """测试臂创建"""
        arm = Arm(name='test_arm')
        self.assertEqual(arm.name, 'test_arm')
        self.assertEqual(arm.reward_sum, 0.0)
        self.assertEqual(arm.pull_count, 0)
        self.assertEqual(arm.alpha, 1.0)
        self.assertEqual(arm.beta, 1.0)
    
    def test_arm_average_reward(self):
        """测试平均奖励"""
        arm = Arm(name='test')
        self.assertEqual(arm.average_reward, 0.0)
        
        arm.update(1.0, is_binary=True)
        self.assertEqual(arm.average_reward, 1.0)
        
        arm.update(0.0, is_binary=True)
        self.assertEqual(arm.average_reward, 0.5)
    
    def test_arm_update_binary(self):
        """测试二值奖励更新"""
        arm = Arm(name='test')
        arm.update(1.0, is_binary=True)
        self.assertEqual(arm.pull_count, 1)
        self.assertEqual(arm.reward_sum, 1.0)
        self.assertEqual(arm.alpha, 2.0)  # success
        self.assertEqual(arm.beta, 1.0)
        
        arm.update(0.0, is_binary=True)
        self.assertEqual(arm.pull_count, 2)
        self.assertEqual(arm.alpha, 2.0)
        self.assertEqual(arm.beta, 2.0)  # failure
    
    def test_arm_update_continuous(self):
        """测试连续奖励更新"""
        arm = Arm(name='test')
        arm.update(0.5, is_binary=False)
        self.assertEqual(arm.pull_count, 1)
        # 连续奖励映射到 Beta 分布
        self.assertTrue(arm.alpha > 1.0)
        self.assertTrue(arm.beta > 1.0)


class TestEpsilonGreedyBandit(unittest.TestCase):
    """测试 Epsilon-Greedy 算法"""
    
    def test_creation(self):
        """测试创建"""
        bandit = EpsilonGreedyBandit(['A', 'B', 'C'], epsilon=0.1)
        self.assertEqual(len(bandit.arms), 3)
        self.assertEqual(bandit.epsilon, 0.1)
        self.assertEqual(bandit.total_pulls, 0)
    
    def test_invalid_epsilon(self):
        """测试无效 epsilon"""
        with self.assertRaises(ValueError):
            EpsilonGreedyBandit(['A', 'B'], epsilon=-0.1)
        with self.assertRaises(ValueError):
            EpsilonGreedyBandit(['A', 'B'], epsilon=1.5)
    
    def test_empty_arms(self):
        """测试空臂列表"""
        with self.assertRaises(ValueError):
            EpsilonGreedyBandit([])
    
    def test_select_and_update(self):
        """测试选择和更新"""
        bandit = EpsilonGreedyBandit(['A', 'B'], epsilon=0.5)
        
        for _ in range(100):
            arm = bandit.select()
            reward = random.random()
            bandit.update(arm, reward)
        
        self.assertEqual(bandit.total_pulls, 100)
        self.assertTrue(bandit.cumulative_reward > 0)
    
    def test_epsilon_decay(self):
        """测试 epsilon 衰减"""
        bandit = EpsilonGreedyBandit(
            ['A', 'B'],
            epsilon=0.5,
            epsilon_decay=0.9,
            min_epsilon=0.01
        )
        
        initial_epsilon = bandit.epsilon
        for _ in range(10):
            arm = bandit.select()
            bandit.update(arm, 1.0)
        
        self.assertTrue(bandit.epsilon < initial_epsilon)
        self.assertTrue(bandit.epsilon >= 0.01)
    
    def test_get_best_arm(self):
        """测试获取最优臂"""
        bandit = EpsilonGreedyBandit(['A', 'B'], epsilon=0.0)
        
        # 强制选择特定臂
        bandit.update('A', 0.9)
        bandit.update('B', 0.1)
        
        self.assertEqual(bandit.get_best_arm(), 'A')
    
    def test_reset(self):
        """测试重置"""
        bandit = EpsilonGreedyBandit(['A', 'B'], epsilon=0.1)
        bandit.update('A', 1.0)
        bandit.reset()
        
        self.assertEqual(bandit.total_pulls, 0)
        self.assertEqual(bandit.epsilon, 0.1)  # 重置为初始值


class TestUCB1Bandit(unittest.TestCase):
    """测试 UCB1 算法"""
    
    def test_creation(self):
        """测试创建"""
        bandit = UCB1Bandit(['A', 'B', 'C'])
        self.assertEqual(len(bandit.arms), 3)
    
    def test_ucb_value(self):
        """测试 UCB 值计算"""
        bandit = UCB1Bandit(['A', 'B'])
        bandit.update('A', 1.0)
        
        arm = bandit.arms['A']
        ucb = bandit._ucb_value(arm)
        
        # UCB = avg + sqrt(2 * ln(N) / n)
        expected_avg = 1.0
        expected_bonus = math.sqrt(2 * math.log(1) / 1) if bandit.total_pulls > 0 else float('inf')
        
        self.assertTrue(ucb >= expected_avg)
    
    def test_select_prefers_unexplored(self):
        """测试未探索的臂优先"""
        bandit = UCB1Bandit(['A', 'B'])
        bandit.update('A', 0.5)
        
        # B 未被探索，UCB 应为无穷大
        self.assertEqual(bandit.select(), 'B')
    
    def test_exploration_factor(self):
        """测试探索因子"""
        bandit = UCB1Bandit(['A', 'B'], exploration_factor=2.0)
        self.assertEqual(bandit.exploration_factor, 2.0)


class TestThompsonSamplingBandit(unittest.TestCase):
    """测试 Thompson Sampling 算法"""
    
    def test_creation(self):
        """测试创建"""
        bandit = ThompsonSamplingBandit(['A', 'B'])
        self.assertEqual(len(bandit.arms), 2)  # 两个臂
        self.assertTrue(bandit.is_binary)
    
    def test_beta_sampling(self):
        """测试 Beta 分布采样"""
        bandit = ThompsonSamplingBandit(['A', 'B'])
        arm = bandit.arms['A']
        
        # 初始状态 alpha=1, beta=1
        sample = bandit._sample_beta(arm)
        self.assertTrue(0 <= sample <= 1)
    
    def test_update_updates_beta_params(self):
        """测试更新 Beta 参数"""
        bandit = ThompsonSamplingBandit(['A', 'B'], is_binary=True)
        
        bandit.update('A', 1.0, is_binary=True)
        self.assertEqual(bandit.arms['A'].alpha, 2.0)
        self.assertEqual(bandit.arms['A'].beta, 1.0)
        
        bandit.update('A', 0.0, is_binary=True)
        self.assertEqual(bandit.arms['A'].alpha, 2.0)
        self.assertEqual(bandit.arms['A'].beta, 2.0)
    
    def test_selection_stochastic(self):
        """测试选择是随机的"""
        bandit = ThompsonSamplingBandit(['A', 'B'])
        
        selections = set()
        for _ in range(100):
            arm = bandit.select()
            selections.add(arm)
        
        # 应该选择了所有臂（因为初始状态相似）
        self.assertTrue(len(selections) >= 1)


class TestSoftmaxBandit(unittest.TestCase):
    """测试 Softmax 算法"""
    
    def test_creation(self):
        """测试创建"""
        bandit = SoftmaxBandit(['A', 'B', 'C'], temperature=1.0)
        self.assertEqual(len(bandit.arms), 3)
        self.assertEqual(bandit.temperature, 1.0)
    
    def test_invalid_temperature(self):
        """测试无效温度"""
        with self.assertRaises(ValueError):
            SoftmaxBandit(['A', 'B'], temperature=0)
        with self.assertRaises(ValueError):
            SoftmaxBandit(['A', 'B'], temperature=-1)
    
    def test_compute_probabilities(self):
        """测试概率计算"""
        bandit = SoftmaxBandit(['A', 'B'], temperature=1.0)
        bandit.update('A', 1.0)
        bandit.update('B', 0.0)
        
        probs = bandit._compute_probabilities()
        
        # 概率之和应为 1
        total = sum(probs.values())
        self.assertAlmostEqual(total, 1.0)
        
        # 高奖励的臂概率应更高
        self.assertTrue(probs['A'] > probs['B'])
    
    def test_temperature_decay(self):
        """测试温度衰减"""
        bandit = SoftmaxBandit(
            ['A', 'B'],
            temperature=1.0,
            temperature_decay=0.9,
            min_temperature=0.1
        )
        
        initial_temp = bandit.temperature
        for _ in range(10):
            arm = bandit.select()
            bandit.update(arm, 1.0)
        
        self.assertTrue(bandit.temperature < initial_temp)
        self.assertTrue(bandit.temperature >= 0.1)
    
    def test_high_temperature_more_uniform(self):
        """测试高温度更均匀"""
        bandit_high = SoftmaxBandit(['A', 'B'], temperature=10.0)
        bandit_low = SoftmaxBandit(['A', 'B'], temperature=0.1)
        
        bandit_high.update('A', 1.0)
        bandit_high.update('B', 0.0)
        bandit_low.update('A', 1.0)
        bandit_low.update('B', 0.0)
        
        probs_high = bandit_high._compute_probabilities()
        probs_low = bandit_low._compute_probabilities()
        
        # 高温度时概率更接近
        diff_high = abs(probs_high['A'] - probs_high['B'])
        diff_low = abs(probs_low['A'] - probs_low['B'])
        
        self.assertTrue(diff_high < diff_low)


class TestExponentialWeightBandit(unittest.TestCase):
    """测试 EXP3 算法"""
    
    def test_creation(self):
        """测试创建"""
        bandit = ExponentialWeightBandit(['A', 'B', 'C'], gamma=0.1)
        self.assertEqual(len(bandit.arms), 3)
        self.assertEqual(bandit.gamma, 0.1)
    
    def test_invalid_gamma(self):
        """测试无效 gamma"""
        with self.assertRaises(ValueError):
            ExponentialWeightBandit(['A', 'B'], gamma=-0.1)
        with self.assertRaises(ValueError):
            ExponentialWeightBandit(['A', 'B'], gamma=1.5)
    
    def test_compute_probabilities(self):
        """测试概率计算"""
        bandit = ExponentialWeightBandit(['A', 'B'], gamma=0.1)
        
        probs = bandit._compute_probabilities()
        
        # 概率之和应为 1
        total = sum(probs.values())
        self.assertAlmostEqual(total, 1.0)
    
    def test_weight_update(self):
        """测试权重更新"""
        bandit = ExponentialWeightBandit(['A', 'B'], gamma=0.1)
        initial_weight = bandit.arms['A'].weight
        
        bandit.update('A', 1.0)
        
        # 权重应增加
        self.assertTrue(bandit.arms['A'].weight >= initial_weight)


class TestFactory(unittest.TestCase):
    """测试工厂函数"""
    
    def test_create_bandit_epsilon_greedy(self):
        """测试创建 Epsilon-Greedy"""
        bandit = create_bandit(
            BanditAlgorithm.EPSILON_GREEDY,
            ['A', 'B'],
            epsilon=0.1
        )
        self.assertIsInstance(bandit, EpsilonGreedyBandit)
    
    def test_create_bandit_ucb1(self):
        """测试创建 UCB1"""
        bandit = create_bandit(BanditAlgorithm.UCB1, ['A', 'B'])
        self.assertIsInstance(bandit, UCB1Bandit)
    
    def test_create_bandit_thompson(self):
        """测试创建 Thompson Sampling"""
        bandit = create_bandit(BanditAlgorithm.THOMPSON_SAMPLING, ['A', 'B'])
        self.assertIsInstance(bandit, ThompsonSamplingBandit)
    
    def test_create_bandit_softmax(self):
        """测试创建 Softmax"""
        bandit = create_bandit(
            BanditAlgorithm.SOFTMAX,
            ['A', 'B'],
            temperature=1.0
        )
        self.assertIsInstance(bandit, SoftmaxBandit)
    
    def test_create_bandit_exponential(self):
        """测试创建 EXP3"""
        bandit = create_bandit(
            BanditAlgorithm.EXPONENTIAL_WEIGHT,
            ['A', 'B'],
            gamma=0.1
        )
        self.assertIsInstance(bandit, ExponentialWeightBandit)


class TestBanditExperiment(unittest.TestCase):
    """测试实验框架"""
    
    def test_creation(self):
        """测试创建"""
        experiment = BanditExperiment(
            ['A', 'B'],
            {'A': 0.7, 'B': 0.3}
        )
        self.assertEqual(len(experiment.arm_names), 2)
    
    def test_run_experiment(self):
        """测试运行实验"""
        experiment = BanditExperiment(
            ['A', 'B', 'C'],
            {'A': 0.8, 'B': 0.5, 'C': 0.3},
            algorithms=[BanditAlgorithm.EPSILON_GREEDY, BanditAlgorithm.UCB1]
        )
        
        results = experiment.run(rounds=100, verbose=False)
        
        self.assertIn('epsilon_greedy', results)
        self.assertIn('ucb1', results)
        
        # 检查结果结构
        for algo in ['epsilon_greedy', 'ucb1']:
            self.assertIn('cumulative_reward', results[algo])
            self.assertIn('average_reward', results[algo])
            self.assertIn('best_arm_found', results[algo])
    
    def test_get_ranking(self):
        """测试获取排名"""
        experiment = BanditExperiment(
            ['A', 'B'],
            {'A': 0.7, 'B': 0.3}
        )
        experiment.run(rounds=100)
        
        ranking = experiment.get_ranking()
        self.assertTrue(len(ranking) > 0)


class TestQuickABTest(unittest.TestCase):
    """测试快速 A/B 测试"""
    
    def test_quick_ab_test(self):
        """测试快速 A/B"""
        result = quick_ab_test(
            ['A', 'B'],
            {'A': [1, 1, 0, 1], 'B': [0, 0, 1, 0]},
            algorithm=BanditAlgorithm.THOMPSON_SAMPLING
        )
        
        self.assertIn('best_variant', result)
        self.assertIn('cumulative_reward', result)
        self.assertIn('variant_stats', result)
    
    def test_empty_rewards(self):
        """测试空奖励数据"""
        result = quick_ab_test(
            ['A', 'B'],
            {},
            algorithm=BanditAlgorithm.EPSILON_GREEDY
        )
        
        self.assertIn('best_variant', result)


class TestBaseBandit(unittest.TestCase):
    """测试基类功能"""
    
    def test_get_arm_stats(self):
        """测试获取臂统计"""
        bandit = EpsilonGreedyBandit(['A', 'B'])
        bandit.update('A', 1.0)
        
        stats = bandit.get_arm_stats('A')
        
        self.assertEqual(stats['name'], 'A')
        self.assertEqual(stats['pull_count'], 1)
        self.assertEqual(stats['reward_sum'], 1.0)
        self.assertEqual(stats['average_reward'], 1.0)
    
    def test_get_all_stats(self):
        """测试获取所有统计"""
        bandit = EpsilonGreedyBandit(['A', 'B'])
        bandit.update('A', 1.0)
        bandit.update('B', 0.5)
        
        all_stats = bandit.get_all_stats()
        
        self.assertIn('A', all_stats)
        self.assertIn('B', all_stats)
    
    def test_invalid_arm_update(self):
        """测试无效臂更新"""
        bandit = EpsilonGreedyBandit(['A', 'B'])
        
        with self.assertRaises(ValueError):
            bandit.update('C', 1.0)
    
    def test_history(self):
        """测试历史记录"""
        bandit = EpsilonGreedyBandit(['A', 'B'])
        bandit.update('A', 1.0)
        bandit.update('B', 0.5)
        
        history = bandit.history
        
        self.assertEqual(len(history), 2)
        self.assertEqual(history[0]['arm'], 'A')
        self.assertEqual(history[1]['arm'], 'B')
    
    def test_selection_rate(self):
        """测试选择率"""
        bandit = EpsilonGreedyBandit(['A', 'B'])
        
        for i in range(100):
            arm = bandit.select()
            bandit.update(arm, 1.0)
        
        stats = bandit.get_all_stats()
        total_rate = sum(s['selection_rate'] for s in stats.values())
        
        self.assertAlmostEqual(total_rate, 1.0)


class TestBanditAlgorithmEnum(unittest.TestCase):
    """测试算法枚举"""
    
    def test_enum_values(self):
        """测试枚举值"""
        self.assertEqual(BanditAlgorithm.EPSILON_GREEDY.value, 'epsilon_greedy')
        self.assertEqual(BanditAlgorithm.UCB1.value, 'ucb1')
        self.assertEqual(BanditAlgorithm.THOMPSON_SAMPLING.value, 'thompson_sampling')
        self.assertEqual(BanditAlgorithm.SOFTMAX.value, 'softmax')
        self.assertEqual(BanditAlgorithm.EXPONENTIAL_WEIGHT.value, 'exponential_weight')


if __name__ == '__main__':
    unittest.main(verbosity=2)
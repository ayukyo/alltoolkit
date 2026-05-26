"""
Multi-Armed Bandit Algorithms
多臂老虎机算法模块

实现多种决策优化算法，用于探索-利用权衡问题：
- Epsilon-Greedy: ε-贪婪算法
- UCB1: Upper Confidence Bound 上置信界算法
- Thompson Sampling: 汤普森采样算法
- Softmax: 柔性最大值算法
- Exponential-weight: 指数权重算法

应用场景：
- A/B 测试
- 推荐系统
- 在线广告投放
- 临床试验
- 资源分配优化
"""

import math
import random
from typing import List, Optional, Dict, Any, Callable
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from enum import Enum


class BanditAlgorithm(Enum):
    """支持的算法类型"""
    EPSILON_GREEDY = "epsilon_greedy"
    UCB1 = "ucb1"
    THOMPSON_SAMPLING = "thompson_sampling"
    SOFTMAX = "softmax"
    EXPONENTIAL_WEIGHT = "exponential_weight"


@dataclass
class Arm:
    """老虎机的臂（动作选项）"""
    name: str
    reward_sum: float = 0.0
    pull_count: int = 0
    
    # Thompson Sampling 参数 (Beta分布)
    alpha: float = 1.0  # 成功次数 + 1
    beta: float = 1.0    # 失败次数 + 1
    
    # 指数权重参数
    weight: float = 1.0
    
    @property
    def average_reward(self) -> float:
        """平均奖励"""
        if self.pull_count == 0:
            return 0.0
        return self.reward_sum / self.pull_count
    
    def update(self, reward: float, is_binary: bool = False):
        """更新臂数据"""
        self.reward_sum += reward
        self.pull_count += 1
        
        # 更新 Thompson Sampling 参数
        if is_binary:
            if reward > 0.5:
                self.alpha += 1
            else:
                self.beta += 1
        else:
            # 对于连续奖励，将其映射到 [0, 1]
            normalized_reward = max(0, min(1, (reward + 1) / 2))
            self.alpha += normalized_reward
            self.beta += 1 - normalized_reward


class BaseBandit(ABC):
    """老虎机算法基类"""
    
    def __init__(self, arm_names: List[str]):
        if not arm_names:
            raise ValueError("At least one arm is required")
        self.arms: Dict[str, Arm] = {name: Arm(name=name) for name in arm_names}
        self.total_pulls = 0
        self._history: List[Dict[str, Any]] = []
    
    @abstractmethod
    def select(self) -> str:
        """选择一个臂"""
        pass
    
    def update(self, arm_name: str, reward: float, is_binary: bool = False):
        """更新指定臂的奖励"""
        if arm_name not in self.arms:
            raise ValueError(f"Unknown arm: {arm_name}")
        
        self.arms[arm_name].update(reward, is_binary)
        self.total_pulls += 1
        
        self._history.append({
            "arm": arm_name,
            "reward": reward,
            "total_pulls": self.total_pulls
        })
    
    def get_arm_stats(self, arm_name: str) -> Dict[str, Any]:
        """获取臂的统计信息"""
        if arm_name not in self.arms:
            raise ValueError(f"Unknown arm: {arm_name}")
        
        arm = self.arms[arm_name]
        return {
            "name": arm.name,
            "pull_count": arm.pull_count,
            "reward_sum": arm.reward_sum,
            "average_reward": arm.average_reward,
            "selection_rate": arm.pull_count / max(1, self.total_pulls)
        }
    
    def get_all_stats(self) -> Dict[str, Dict[str, Any]]:
        """获取所有臂的统计信息"""
        return {name: self.get_arm_stats(name) for name in self.arms}
    
    def get_best_arm(self) -> str:
        """获取当前最优臂"""
        return max(self.arms.values(), key=lambda a: a.average_reward).name
    
    def reset(self):
        """重置所有数据"""
        for arm in self.arms.values():
            arm.reward_sum = 0.0
            arm.pull_count = 0
            arm.alpha = 1.0
            arm.beta = 1.0
            arm.weight = 1.0
        self.total_pulls = 0
        self._history = []
    
    @property
    def cumulative_reward(self) -> float:
        """累计奖励"""
        return sum(arm.reward_sum for arm in self.arms.values())
    
    @property
    def history(self) -> List[Dict[str, Any]]:
        """获取历史记录"""
        return self._history.copy()


class EpsilonGreedyBandit(BaseBandit):
    """
    Epsilon-Greedy 算法
    
    以 ε 概率随机探索，以 (1-ε) 概率选择当前最优臂。
    
    参数:
        arm_names: 臂名称列表
        epsilon: 探索概率 (0-1)
        epsilon_decay: 衰减因子 (每轮后 epsilon *= decay)
        min_epsilon: 最小 epsilon 值
    """
    
    def __init__(
        self, 
        arm_names: List[str],
        epsilon: float = 0.1,
        epsilon_decay: float = 1.0,
        min_epsilon: float = 0.01
    ):
        super().__init__(arm_names)
        if not 0 <= epsilon <= 1:
            raise ValueError("Epsilon must be between 0 and 1")
        self.epsilon = epsilon
        self.initial_epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.min_epsilon = min_epsilon
    
    def select(self) -> str:
        """选择一个臂"""
        # 探索：随机选择
        if random.random() < self.epsilon:
            return random.choice(list(self.arms.keys()))
        
        # 利用：选择平均奖励最高的臂
        best_arm = None
        best_avg = float('-inf')
        
        for name, arm in self.arms.items():
            if arm.pull_count == 0:
                # 优先探索未尝试的臂
                return name
            if arm.average_reward > best_avg:
                best_avg = arm.average_reward
                best_arm = name
        
        return best_arm or list(self.arms.keys())[0]
    
    def update(self, arm_name: str, reward: float, is_binary: bool = False):
        """更新并衰减 epsilon"""
        super().update(arm_name, reward, is_binary)
        self.epsilon = max(
            self.min_epsilon,
            self.epsilon * self.epsilon_decay
        )
    
    def reset(self):
        """重置"""
        super().reset()
        self.epsilon = self.initial_epsilon


class UCB1Bandit(BaseBandit):
    """
    UCB1 (Upper Confidence Bound 1) 算法
    
    使用上置信界来平衡探索与利用。
    UCB值 = 平均奖励 + sqrt(2 * ln(N) / n)
    
    参数:
        arm_names: 臂名称列表
        exploration_factor: 探索因子（默认为 sqrt(2)）
    """
    
    def __init__(self, arm_names: List[str], exploration_factor: float = 1.414):
        super().__init__(arm_names)
        self.exploration_factor = exploration_factor
    
    def _ucb_value(self, arm: Arm) -> float:
        """计算 UCB 值"""
        if arm.pull_count == 0:
            return float('inf')
        
        exploration_bonus = math.sqrt(
            2 * math.log(max(1, self.total_pulls)) / arm.pull_count
        )
        return arm.average_reward + self.exploration_factor * exploration_bonus
    
    def select(self) -> str:
        """选择 UCB 值最大的臂"""
        best_arm = None
        best_ucb = float('-inf')
        
        for name, arm in self.arms.items():
            ucb = self._ucb_value(arm)
            if ucb > best_ucb:
                best_ucb = ucb
                best_arm = name
        
        return best_arm or list(self.arms.keys())[0]


class ThompsonSamplingBandit(BaseBandit):
    """
    Thompson Sampling 汤普森采样算法
    
    使用 Beta 分布对每个臂的成功概率建模，
    通过从后验分布中采样来选择臂。
    
    参数:
        arm_names: 臂名称列表
        is_binary: 奖励是否为二值（成功/失败）
    """
    
    def __init__(self, arm_names: List[str], is_binary: bool = True):
        super().__init__(arm_names)
        self.is_binary = is_binary
    
    def _sample_beta(self, arm: Arm) -> float:
        """从 Beta 分布中采样"""
        return random.betavariate(arm.alpha, arm.beta)
    
    def select(self) -> str:
        """选择采样值最大的臂"""
        best_arm = None
        best_sample = float('-inf')
        
        for name, arm in self.arms.items():
            sample = self._sample_beta(arm)
            if sample > best_sample:
                best_sample = sample
                best_arm = name
        
        return best_arm or list(self.arms.keys())[0]
    
    def update(self, arm_name: str, reward: float, is_binary: bool = False):
        """更新 Beta 分布参数"""
        super().update(arm_name, reward, is_binary or self.is_binary)


class SoftmaxBandit(BaseBandit):
    """
    Softmax (Boltzmann) 算法
    
    使用 Softmax 函数将平均奖励转换为选择概率。
    P(arm) = exp(temperature * avg_reward) / sum(exp(temperature * avg))
    
    参数:
        arm_names: 臂名称列表
        temperature: 温度参数（越高越随机，越低越贪婪）
        temperature_decay: 温度衰减因子
        min_temperature: 最小温度值
    """
    
    def __init__(
        self,
        arm_names: List[str],
        temperature: float = 1.0,
        temperature_decay: float = 1.0,
        min_temperature: float = 0.1
    ):
        super().__init__(arm_names)
        if temperature <= 0:
            raise ValueError("Temperature must be positive")
        self.temperature = temperature
        self.initial_temperature = temperature
        self.temperature_decay = temperature_decay
        self.min_temperature = min_temperature
    
    def _compute_probabilities(self) -> Dict[str, float]:
        """计算各臂的选择概率
        
        Softmax 公式：P(arm) = exp(avg/temperature) / sum(exp(avg/temperature))
        - 高温度 → 更均匀分布（更多探索）
        - 低温度 → 更贪婪（更多利用）
        """
        # 使用平均奖励，未探索的使用默认值
        rewards = {}
        for name, arm in self.arms.items():
            if arm.pull_count > 0:
                rewards[name] = arm.average_reward
            else:
                rewards[name] = 0.0
        
        # Softmax 计算（注意：温度是除法，不是乘法）
        max_reward = max(rewards.values())
        exp_values = {
            name: math.exp((r - max_reward) / self.temperature)
            for name, r in rewards.items()
        }
        total = sum(exp_values.values())
        
        return {name: v / total for name, v in exp_values.items()}
    
    def select(self) -> str:
        """根据概率分布随机选择臂"""
        probs = self._compute_probabilities()
        
        # 轮盘赌选择
        r = random.random()
        cumsum = 0.0
        for name, prob in probs.items():
            cumsum += prob
            if r <= cumsum:
                return name
        
        return list(self.arms.keys())[-1]
    
    def update(self, arm_name: str, reward: float, is_binary: bool = False):
        """更新并衰减温度"""
        super().update(arm_name, reward, is_binary)
        self.temperature = max(
            self.min_temperature,
            self.temperature * self.temperature_decay
        )
    
    def reset(self):
        """重置"""
        super().reset()
        self.temperature = self.initial_temperature


class ExponentialWeightBandit(BaseBandit):
    """
    Exponential-weight (EXP3) 算法
    
    使用指数权重进行臂选择，适用于对抗性环境。
    
    参数:
        arm_names: 臂名称列表
        gamma: 探索参数 (0-1)
    """
    
    def __init__(self, arm_names: List[str], gamma: float = 0.1):
        super().__init__(arm_names)
        if not 0 <= gamma <= 1:
            raise ValueError("Gamma must be between 0 and 1")
        self.gamma = gamma
    
    def _compute_probabilities(self) -> Dict[str, float]:
        """计算选择概率"""
        total_weight = sum(arm.weight for arm in self.arms.values())
        n = len(self.arms)
        
        probs = {}
        for name, arm in self.arms.items():
            probs[name] = (1 - self.gamma) * (arm.weight / total_weight) + self.gamma / n
        
        return probs
    
    def select(self) -> str:
        """根据概率选择臂"""
        probs = self._compute_probabilities()
        
        r = random.random()
        cumsum = 0.0
        for name, prob in probs.items():
            cumsum += prob
            if r <= cumsum:
                return name
        
        return list(self.arms.keys())[-1]
    
    def update(self, arm_name: str, reward: float, is_binary: bool = False):
        """更新权重"""
        super().update(arm_name, reward, is_binary)
        
        # 估算奖励（假设奖励范围 [0, 1]）
        probs = self._compute_probabilities()
        estimated_reward = reward / probs[arm_name]
        
        # 更新权重
        self.arms[arm_name].weight *= math.exp(
            self.gamma * estimated_reward / len(self.arms)
        )


def create_bandit(
    algorithm: BanditAlgorithm,
    arm_names: List[str],
    **kwargs
) -> BaseBandit:
    """
    工厂函数：创建指定类型的老虎机算法
    
    参数:
        algorithm: 算法类型
        arm_names: 臂名称列表
        **kwargs: 传递给具体算法的参数
    
    返回:
        对应的老虎机算法实例
    """
    bandit_classes = {
        BanditAlgorithm.EPSILON_GREEDY: EpsilonGreedyBandit,
        BanditAlgorithm.UCB1: UCB1Bandit,
        BanditAlgorithm.THOMPSON_SAMPLING: ThompsonSamplingBandit,
        BanditAlgorithm.SOFTMAX: SoftmaxBandit,
        BanditAlgorithm.EXPONENTIAL_WEIGHT: ExponentialWeightBandit,
    }
    
    if algorithm not in bandit_classes:
        raise ValueError(f"Unknown algorithm: {algorithm}")
    
    return bandit_classes[algorithm](arm_names, **kwargs)


class BanditExperiment:
    """
    多臂老虎机实验框架
    
    用于比较不同算法的性能。
    """
    
    def __init__(
        self,
        arm_names: List[str],
        true_rewards: Dict[str, float],
        algorithms: Optional[List[BanditAlgorithm]] = None
    ):
        """
        参数:
            arm_names: 臂名称列表
            true_rewards: 真实奖励概率（用于模拟）
            algorithms: 要比较的算法列表
        """
        self.arm_names = arm_names
        self.true_rewards = true_rewards
        self.algorithms = algorithms or list(BanditAlgorithm)
        self.results: Dict[str, Dict[str, Any]] = {}
    
    def _simulate_reward(self, arm_name: str) -> float:
        """模拟奖励（伯努利分布）"""
        return 1.0 if random.random() < self.true_rewards.get(arm_name, 0.5) else 0.0
    
    def run(
        self,
        rounds: int = 1000,
        verbose: bool = False
    ) -> Dict[str, Dict[str, Any]]:
        """
        运行实验
        
        参数:
            rounds: 实验轮数
            verbose: 是否打印进度
        
        返回:
            各算法的实验结果
        """
        self.results = {}
        
        for algo_type in self.algorithms:
            bandit = create_bandit(algo_type, self.arm_names)
            rewards = []
            
            for _ in range(rounds):
                arm = bandit.select()
                reward = self._simulate_reward(arm)
                bandit.update(arm, reward, is_binary=True)
                rewards.append(reward)
            
            self.results[algo_type.value] = {
                "cumulative_reward": bandit.cumulative_reward,
                "average_reward": bandit.cumulative_reward / rounds,
                "best_arm_found": bandit.get_best_arm(),
                "arm_stats": bandit.get_all_stats()
            }
            
            if verbose:
                print(f"{algo_type.value}: "
                      f"Cumulative Reward = {bandit.cumulative_reward:.2f}, "
                      f"Best Arm = {bandit.get_best_arm()}")
        
        return self.results
    
    def get_ranking(self) -> List[tuple]:
        """获取算法排名"""
        ranking = sorted(
            self.results.items(),
            key=lambda x: x[1]["cumulative_reward"],
            reverse=True
        )
        return ranking


# 便捷函数
def quick_ab_test(
    variant_names: List[str],
    rewards: Dict[str, List[float]],
    algorithm: BanditAlgorithm = BanditAlgorithm.THOMPSON_SAMPLING
) -> Dict[str, Any]:
    """
    快速 A/B 测试
    
    参数:
        variant_names: 变体名称列表
        rewards: 历史奖励数据 {variant: [rewards]}
        algorithm: 使用的算法
    
    返回:
        测试结果统计
    """
    bandit = create_bandit(algorithm, variant_names)
    
    # 获取最大长度
    max_len = max(len(r) for r in rewards.values()) if rewards else 0
    
    # 按时间步更新
    for i in range(max_len):
        for variant in variant_names:
            if variant in rewards and i < len(rewards[variant]):
                bandit.update(variant, rewards[variant][i], is_binary=True)
    
    return {
        "algorithm": algorithm.value,
        "best_variant": bandit.get_best_arm(),
        "cumulative_reward": bandit.cumulative_reward,
        "variant_stats": bandit.get_all_stats()
    }
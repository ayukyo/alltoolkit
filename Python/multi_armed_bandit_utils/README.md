# Multi-Armed Bandit Utils

多臂老虎机算法模块 - 解决探索与利用权衡问题的完整工具集。

## 功能特性

支持 5 种经典算法：

| 算法 | 描述 | 适用场景 |
|------|------|---------|
| **Epsilon-Greedy** | ε-贪婪算法，以 ε 概率随机探索 | 简单场景，需要精确控制探索率 |
| **UCB1** | 上置信界算法，自动平衡探索利用 | 统计意义重要的场景，有理论保证 |
| **Thompson Sampling** | 汤普森采样，基于贝叶斯后验采样 | A/B 测试，二值奖励，实践中最优 |
| **Softmax** | 柔性最大值，输出概率分布 | 需要概率输出的场景 |
| **Exponential-weight (EXP3)** | 指数权重算法 | 对抗性环境，非平稳奖励 |

## 安装

```python
# 零外部依赖，直接导入使用
from multi_armed_bandit_utils.mod import (
    EpsilonGreedyBandit,
    UCB1Bandit,
    ThompsonSamplingBandit,
    SoftmaxBandit,
    ExponentialWeightBandit,
    create_bandit,
    BanditAlgorithm,
    BanditExperiment,
    quick_ab_test
)
```

## 快速开始

### 基本使用

```python
from multi_armed_bandit_utils.mod import ThompsonSamplingBandit

# 创建 bandit（多个选项）
bandit = ThompsonSamplingBandit(["选项A", "选项B", "选项C"])

# 选择并更新
for _ in range(100):
    arm = bandit.select()              # 选择一个选项
    reward = get_user_feedback(arm)   # 获取奖励（0 或 1）
    bandit.update(arm, reward, is_binary=True)

# 查看结果
print(f"最佳选项: {bandit.get_best_arm()}")
print(f"累计奖励: {bandit.cumulative_reward}")
```

### 工厂函数

```python
from multi_armed_bandit_utils.mod import create_bandit, BanditAlgorithm

# 创建任意类型的 bandit
bandit = create_bandit(
    BanditAlgorithm.UCB1,
    arm_names=["A", "B", "C"],
    exploration_factor=1.414
)
```

### A/B 测试

```python
from multi_armed_bandit_utils.mod import quick_ab_test, BanditAlgorithm

# 使用历史数据快速分析
result = quick_ab_test(
    variant_names=["control", "treatment_A", "treatment_B"],
    rewards={
        "control": [1, 0, 1, 1, 0, 1, ...],
        "treatment_A": [1, 1, 0, 1, 1, 1, ...],
        "treatment_B": [0, 0, 1, 0, 0, 1, ...],
    },
    algorithm=BanditAlgorithm.THOMPSON_SAMPLING
)

print(f"最优版本: {result['best_variant']}")
```

### 实验比较

```python
from multi_armed_bandit_utils.mod import BanditExperiment, BanditAlgorithm

experiment = BanditExperiment(
    arm_names=["A", "B", "C"],
    true_rewards={"A": 0.3, "B": 0.5, "C": 0.8},  # 用于模拟
    algorithms=[BanditAlgorithm.EPSILON_GREEDY, BanditAlgorithm.UCB1]
)

results = experiment.run(rounds=1000)
ranking = experiment.get_ranking()

for algo, data in ranking:
    print(f"{algo}: {data['cumulative_reward']} 奖励")
```

## API 参考

### EpsilonGreedyBandit

```python
bandit = EpsilonGreedyBandit(
    arm_names=["A", "B", "C"],
    epsilon=0.1,           # 探索概率
    epsilon_decay=1.0,     # 衰减因子
    min_epsilon=0.01       # 最小 epsilon
)
```

### UCB1Bandit

```python
bandit = UCB1Bandit(
    arm_names=["A", "B", "C"],
    exploration_factor=1.414  # sqrt(2)
)
```

### ThompsonSamplingBandit

```python
bandit = ThompsonSamplingBandit(
    arm_names=["A", "B", "C"],
    is_binary=True  # 奖励是否为二值
)
```

### SoftmaxBandit

```python
bandit = SoftmaxBandit(
    arm_names=["A", "B", "C"],
    temperature=1.0,        # 温度参数
    temperature_decay=1.0,  # 衰减因子
    min_temperature=0.1     # 最小温度
)
```

### ExponentialWeightBandit

```python
bandit = ExponentialWeightBandit(
    arm_names=["A", "B", "C"],
    gamma=0.1  # 探索参数
)
```

### 通用方法

所有 bandit 都继承自 `BaseBandit`，提供以下方法：

| 方法 | 描述 |
|------|------|
| `select()` | 选择一个臂并返回其名称 |
| `update(arm_name, reward, is_binary=False)` | 更新指定臂的奖励 |
| `get_best_arm()` | 获取当前最优臂 |
| `get_arm_stats(arm_name)` | 获取单个臂的统计信息 |
| `get_all_stats()` | 获取所有臂的统计信息 |
| `cumulative_reward` | 累计奖励（属性） |
| `history` | 历史记录（属性） |
| `reset()` | 重置所有数据 |

## 应用场景

- **A/B 测试优化** - 快速找到最佳版本
- **推荐系统** - 内容/商品推荐
- **广告投放** - 选择最佳广告位
- **临床试验** - 治疗方案选择
- **资源分配** - 计算资源调度
- **动态定价** - 价格优化

## 运行测试

```bash
python -m pytest test_multi_armed_bandit.py -v
# 或
python test_multi_armed_bandit.py
```

## 运行示例

```bash
python examples.py
```

## 算法选择指南

| 场景 | 推荐算法 |
|------|---------|
| A/B 测试 | Thompson Sampling |
| 需要理论保证 | UCB1 |
| 简单易理解 | Epsilon-Greedy |
| 需要概率输出 | Softmax |
| 对抗性环境 | Exponential-weight |

## 许可证

MIT License
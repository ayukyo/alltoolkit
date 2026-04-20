# Markov Chain Utils - 马尔可夫链工具集

零外部依赖的马尔可夫链实现，支持文本生成、序列预测、转移矩阵分析等功能。

## 功能特性

- **MarkovChain**: 通用马尔可夫链实现，支持任意阶数
- **MarkovTextGenerator**: 文本生成器，支持单词级/字符级，温度参数控制
- **SequencePredictor**: 序列预测器，支持异常检测、概率分布预测
- **TransitionMatrix**: 转移矩阵工具，支持稳态分布、互通类分析

## 安装使用

```python
from markov_chain_utils import (
    MarkovChain,
    MarkovTextGenerator,
    SequencePredictor,
    TransitionMatrix
)
```

## 快速示例

### MarkovChain - 马尔可夫链

```python
from markov_chain_utils import MarkovChain

# 创建一阶马尔可夫链
mc = MarkovChain(order=1)

# 训练天气序列
mc.train(['S', 'S', 'R', 'S', 'C', 'S', 'S', 'R'])

# 获取转移概率
print(mc.get_transition_probability(('S',), 'R'))  # 0.25

# 预测下一个状态
print(mc.predict_next(('S',)))  # 'S'

# 生成序列
generated = mc.generate(start=('S',), steps=10)
```

### MarkovTextGenerator - 文本生成

```python
from markov_chain_utils import MarkovTextGenerator

# 创建生成器
gen = MarkovTextGenerator(order=2, mode='word')

# 训练
gen.train("The cat sat on the mat. The cat was happy.")

# 生成文本
text = gen.generate(start="The cat", max_length=20)

# 生成句子
sentence = gen.generate_sentence()

# 不同温度控制随机性
text = gen.generate(temperature=0.5)  # 更确定性
text = gen.generate(temperature=1.5)  # 更随机
```

### SequencePredictor - 序列预测

```python
from markov_chain_utils import SequencePredictor

# 创建预测器
sp = SequencePredictor(order=2)

# 训练用户行为序列
sp.train(['login', 'view', 'edit', 'save', 'logout'])

# 预测
prediction, probability = sp.predict_with_probability(['login', 'view'])

# 多步预测
sequence = sp.predict_sequence(['login'], steps=3)

# 异常检测
anomalies = sp.detect_anomaly(['login', 'delete', 'logout'], threshold=0.1)
```

### TransitionMatrix - 转移矩阵

```python
from markov_chain_utils import TransitionMatrix

# 创建转移矩阵
tm = TransitionMatrix()

# 添加转移
tm.add_transition('A', 'B', count=3)
tm.add_transition('A', 'C', count=1)

# 获取概率
print(tm.get_probability('A', 'B'))  # 0.75

# 计算稳态分布
stationary = tm.get_stationary_distribution()

# 获取吸收态
absorbing = tm.get_absorbing_states()
```

## API 参考

### MarkovChain

| 方法 | 说明 |
|------|------|
| `train(sequence)` | 训练马尔可夫链 |
| `train_multiple(sequences)` | 多序列训练 |
| `get_transition_probability(current, next)` | 获取转移概率 |
| `get_possible_next_states(current)` | 获取可能的下一状态 |
| `predict_next(current)` | 预测最可能的下一状态 |
| `sample_next(current)` | 概率采样 |
| `generate(start, steps)` | 生成序列 |

### MarkovTextGenerator

| 方法 | 说明 |
|------|------|
| `train(text)` | 训练文本 |
| `train_from_file(filepath)` | 从文件训练 |
| `generate(start, max_length, temperature)` | 生成文本 |
| `generate_sentence()` | 生成句子 |
| `generate_paragraph(num_sentences)` | 生成段落 |
| `get_continuations(prefix, top_n)` | 获取续写预测 |

### SequencePredictor

| 方法 | 说明 |
|------|------|
| `train(sequence)` | 训练序列 |
| `predict(context)` | 单步预测 |
| `predict_with_probability(context)` | 带概率预测 |
| `predict_distribution(context)` | 概率分布 |
| `predict_sequence(context, steps)` | 多步预测 |
| `detect_anomaly(sequence, threshold)` | 异常检测 |
| `evaluate(test_sequence)` | 评估准确率 |

### TransitionMatrix

| 方法 | 说明 |
|------|------|
| `add_transition(from, to, count)` | 添加转移 |
| `add_sequence(sequence)` | 从序列添加 |
| `get_probability(from, to)` | 获取概率 |
| `get_row(from_state)` | 获取行概率 |
| `get_stationary_distribution()` | 稳态分布 |
| `get_absorbing_states()` | 吸收态 |
| `get_communicating_classes()` | 互通类 |

## 应用场景

- **文本生成**: 基于 n-gram 的随机文本生成
- **行为预测**: 用户行为序列预测
- **异常检测**: 系统日志异常检测
- **音乐生成**: 基于音符序列的旋律生成
- **页面预测**: 网站用户导航路径预测
- **天气预测**: 基于历史天气序列预测

## 测试

```bash
python -m pytest test_markov_chain.py -v
```

## 作者

AllToolkit 自动生成
日期: 2026-04-21
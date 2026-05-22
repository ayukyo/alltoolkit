# Reaction Time Utilities

反应时间计算与分析工具，用于评估和追踪反应速度表现。

## 功能特性

- **统计分析**: 平均值、中位数、标准差、百分位数、变异系数
- **表现评估**: 年龄基准对比、游戏/运动/驾驶专项评估
- **趋势分析**: 训练进度追踪、改善速率计算、预测
- **疲劳分析**: 疲劳效应检测、恢复时间估算
- **驾驶安全**: 反应时间安全评估、理论制动距离计算
- **训练计划**: 个性化训练方案生成

## 零外部依赖

纯 Python 实现，无需安装任何第三方库。

## 快速使用

```python
from mod import calculate_statistics, assess_performance

# 计算统计数据
times = [180, 195, 200, 210, 220]
stats = calculate_statistics(times)
print(f"平均: {stats.mean} ms, 标准差: {stats.std} ms")

# 评估表现
assessment = assess_performance(times, age=25)
print(f"等级: {assessment.level.value}, 得分: {assessment.score}")
```

## 评估类型

| 类型 | 说明 |
|------|------|
| 一般评估 | 基于年龄基准的通用评估 |
| 游戏评估 | FPS/Racing/Rhythm/MOBA 等 |
| 运动评估 | 乒乓球/拳击/网球/足球等 |
| 驾驶评估 | 正常/紧急/高速/夜间场景 |

## 基准数据

- 年龄基准: 10-75岁各年龄段平均值和阈值
- 游戏基准: 各游戏类型优秀/良好/平均/慢速阈值
- 运动基准: 各运动项目专业级基准
- 驾驶基准: 安全/警示/危险阈值

## 文件结构

```
reaction_time_utils/
├── mod.py                   # 主模块
├── reaction_time_utils_test.py  # 测试文件
├── examples/
│   └── usage_examples.py    # 使用示例
└── README.md
```

## 运行测试

```bash
python -m pytest reaction_time_utils_test.py -v
```

## 运行示例

```bash
python examples/usage_examples.py
```

## 应用场景

- 游戏玩家反应速度评估
- 运动员反应能力测试
- 驾驶员安全评估
- 认知功能监测
- 训练效果追踪
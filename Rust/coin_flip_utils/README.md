# 抛硬币模拟工具 (coin_flip_utils)

## 概述

零外部依赖的抛硬币模拟工具库，提供完整的抛硬币模拟、概率统计、可视化分析功能。

## 核心功能

### 1. 基本抛硬币
- 单次抛掷
- 多次抛掷
- 自定义硬币

### 2. 硬币类型
- 标准硬币（正面/反面）
- 人民币一元（国徽/菊花）
- 美元25美分（华盛顿/鹰）
- 欧元1元（欧洲地图/成员国图案）
- 比特币（₿/白皮书）
- 自定义标签硬币

### 3. 统计分析
- 正/反面计数和比例
- 连续序列统计
- ASCII 可视化图表
- Z分数检验
- 均匀性检验

### 4. 特殊功能
- 三局两胜决斗
- 决策辅助
- 连续抛掷挑战
- 蒙特卡洛模拟

### 5. 可重复性
- 可设置随机种子
- 完全可重复的实验

## 使用示例

```rust
use coin_flip_utils::*;

// 基本抛硬币
let result = flip();
println!("结果: {}", result.name());

// 多次抛掷
let stats = flip_n(100);
println!("正面比例: {:.2}%", stats.heads_ratio() * 100);

// 使用抛硬币器
let mut flipper = CoinFlipper::fair();
flipper.flip_n(10);
println!("{}", flipper.stats().analyze());

// 自定义硬币
let coin = Coin::new("选择硬币", "YES", "NO");
let mut flipper = CoinFlipper::new(coin);
let result = flipper.flip();
println!("选择: {}", result.label);

// 有偏差的硬币
let biased = Coin::biased("作弊硬币", "赢", "输", 0.8);
let mut flipper = CoinFlipper::new(biased);
// 正面概率为 80%

// 蒙特卡洛模拟
let result = monte_carlo(100000);
println!("{}", result.report());
```

## 测试覆盖

- 31个单元测试
- 100% 通过率
- 涵盖所有核心功能

## 随机数生成

使用 XorShift64 算法实现简单伪随机数生成器，零外部依赖。

## 作者

AllToolkit 自动化生成工具 - 2026-05-25
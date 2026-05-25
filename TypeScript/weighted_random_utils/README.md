# Weighted Random Utils - TypeScript

零依赖的加权随机选择工具库，支持多种算法实现。

## ✨ 特性

- **零依赖** - 仅使用 TypeScript 标准库
- **多算法支持** - 线性扫描、Alias Method、动态拒绝采样
- **O(1) 采样** - Alias Method 实现高效采样
- **动态更新** - 支持实时添加、删除、更新选项
- **完整测试** - 覆盖边界值和性能场景
- **统计分析** - 熵计算、频率分布统计

## 📦 安装

```typescript
import { WeightedRandomPicker, AliasPicker } from "./mod.ts";
```

## 🚀 快速开始

### 基本用法

```typescript
import { WeightedRandomPicker } from "./mod.ts";

// 创建加权选项
const colors = [
  { value: "red", weight: 10 },
  { value: "green", weight: 30 },
  { value: "blue", weight: 60 },
];

// 创建选择器
const picker = new WeightedRandomPicker(colors);

// 单次选择
const color = picker.pick(); // "blue" 更可能被选中

// 多次选择
const colors5 = picker.pickMultiple(5);

// 唯一选择（无放回）
const unique = picker.pickUnique(2);
```

### 不同构造方式

```typescript
// 使用 Map
const weightsMap = new Map<string, number>();
weightsMap.set("optionA", 25);
weightsMap.set("optionB", 75);
const picker = new WeightedRandomPicker(weightsMap);

// 使用对象
const picker = new WeightedRandomPicker<string>({
  optionA: 25,
  optionB: 75,
});
```

### Alias Method - O(1) 采样

```typescript
import { AliasPicker } from "./mod.ts";

// 大数据集使用 Alias Method
const largeDataset = [];
for (let i = 0; i < 1000; i++) {
  largeDataset.push({ value: `item-${i}`, weight: Math.random() + 0.1 });
}

const aliasPicker = new AliasPicker(largeDataset);

// O(1) 时间复杂度采样
const item = aliasPicker.pick();
```

### 动态选择器

```typescript
import { DynamicWeightedPicker } from "./mod.ts";

const dynamicPicker = new DynamicWeightedPicker<string>();

// 动态添加选项
dynamicPicker.set("server-A", 30);
dynamicPicker.set("server-B", 50);
dynamicPicker.set("server-C", 20);

// 选择
const server = dynamicPicker.pick();

// 更新权重
dynamicPicker.set("server-A", 60);

// 删除选项
dynamicPicker.delete("server-C");
```

### 确定性随机（种子）

```typescript
import { createSeededRandom } from "./mod.ts";

// 相同种子产生相同结果
const picker = new WeightedRandomPicker(
  [{ value: "a", weight: 1 }, { value: "b", weight: 1 }],
  { random: createSeededRandom(42) }
);

const results = picker.pickMultiple(5);
// 结果可复现
```

## 📊 统计信息

```typescript
const picker = new WeightedRandomPicker([
  { value: "low", weight: 1 },
  { value: "medium", weight: 5 },
  { value: "high", weight: 10 },
]);

const stats = picker.getStatistics();

console.log("总选项:", stats.totalOptions);
console.log("最小权重:", stats.minWeight);
console.log("最大权重:", stats.maxWeight);
console.log("熵:", stats.entropy, "bits");
```

### 批量统计

```typescript
const batchResult = picker.pickWithStats(1000);

console.log("选择次数:", batchResult.selections.length);
console.log("频率分布:", batchResult.frequencies);
```

## 🛠️ 辅助函数

```typescript
import {
  weightedShuffle,
  weightedSample,
  calculateEntropy,
  normalizeWeights,
  createWeightedOptions,
  validateWeights,
  weightedPick,
} from "./mod.ts";

// 加权洗牌（高权重更可能在前）
const shuffled = weightedShuffle([
  { value: "popular", weight: 100 },
  { value: "rare", weight: 5 },
]);

// 加权采样（无放回）
const sampled = weightedSample(items, 3);

// 计算熵
const entropy = calculateEntropy([1, 2, 3]);

// 归一化权重
const normalized = normalizeWeights([10, 20, 70]);

// 快速单次选择
const picked = weightedPick(items);
```

## 📈 实际应用

### A/B 测试

```typescript
const abTestPicker = new WeightedRandomPicker({
  "control-group": 70,
  "variant-A": 15,
  "variant-B": 15,
});

const group = abTestPicker.pick();
```

### 负载均衡

```typescript
const serverPicker = new DynamicWeightedPicker<string>();
serverPicker.set("high-capacity", 100);
serverPicker.set("medium-capacity", 50);
serverPicker.set("low-capacity", 20);

const server = serverPicker.pick();
```

### 游戏抽奖

```typescript
const lotteryPicker = new WeightedRandomPicker([
  { value: "grand-prize", weight: 1 },
  { value: "second-prize", weight: 10 },
  { value: "nothing", weight: 1000 },
]);

const prize = lotteryPicker.pick();
```

## 🔧 API 参考

### WeightedRandomPicker<T>

| 方法 | 描述 | 时间复杂度 |
|------|------|------------|
| `pick()` | 选择一个选项 | O(log n) 二分查找 |
| `pickMultiple(count)` | 选择多个选项（有放回） | O(count × log n) |
| `pickUnique(count)` | 选择不重复选项 | O(count × n) |
| `pickWithStats(count)` | 选择并统计 | O(count × log n) |
| `getWeight(value)` | 获取选项权重 | O(n) |
| `getProbability(value)` | 获取选择概率 | O(n) |
| `getOptions()` | 获取所有选项 | O(n) |
| `getStatistics()` | 获取统计信息 | O(n) |
| `setRandom(random)` | 设置随机数生成器 | O(1) |

### AliasPicker<T>

| 方法 | 描述 | 时间复杂度 |
|------|------|------------|
| `pick()` | O(1) 选择 | **O(1)** |
| `pickMultiple(count)` | 多次选择 | O(count) |
| `size` | 选项数量 | O(1) |

### DynamicWeightedPicker<T>

| 方法 | 描述 |
|------|------|
| `set(value, weight)` | 添加/更新选项 |
| `delete(value)` | 删除选项 |
| `pick()` | 选择一个选项 |
| `pickMultiple(count)` | 多次选择 |
| `has(value)` | 检查选项是否存在 |
| `getWeight(value)` | 获取权重 |
| `clear()` | 清空所有选项 |

## 🧪 测试

```bash
deno test weighted_random_utils_test.ts
```

测试覆盖：
- 基本选择功能
- 边界值（空数组、单选项、极小/极大权重）
- 权重分布正确性
- 性能测试（大数据集）
- 确定性随机验证

## 📝 熵与随机性

熵（Entropy）衡量分布的不确定性：

- **均匀分布**：熵最大，随机性最高
- **极端分布**：熵接近 0，几乎确定性

```typescript
// 均匀分布熵 = log2(n)
calculateEntropy([1, 1, 1, 1]); // ≈ 2 bits

// 偏斜分布熵更低
calculateEntropy([10, 1, 1, 1]); // ≈ 1.2 bits

// 单选项熵 = 0
calculateEntropy([1]); // 0 bits
```

## 📄 许可证

MIT License
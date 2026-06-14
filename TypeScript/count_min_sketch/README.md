# Count-Min Sketch (TypeScript)

概率论数据结构，用于频率估计和流式数据统计。零外部依赖，纯 TypeScript 实现。

## 功能特性

- **频率估计** - 估算任意元素的近似出现次数
- **优化的深度/宽度** - 根据精度 (ε) 和置信度 (δ) 自动计算最优参数
- **合并操作** - 支持合并多个 sketch
- **序列化** - 支持 toBytes() 持久化
- **零依赖** - 仅使用 TypeScript 标准库

## 安装

```typescript
import { CountMinSketch } from './count_min_sketch/src/index';
```

## 快速使用

### 基本频率估计

```typescript
const sketch = new CountMinSketch<string>(5, 100);

sketch.increment('hello');
sketch.increment('hello');
sketch.increment('world');

console.log(sketch.estimate('hello')); // >= 2
console.log(sketch.estimate('world')); // >= 1
console.log(sketch.estimate('other')); // 0
```

### 使用 factory 方法

```typescript
// 根据精度和置信度创建
const epsilon = 0.01;  // 精度
const delta = 0.01;    // 置信度 (1% 错误概率)

const sketch = CountMinSketch.withRate<string>(epsilon, delta);
sketch.increment('item');
```

### 批量更新

```typescript
const sketch = new CountMinSketch<string>(5, 100);

sketch.update('item', 5);  // 一次增加 5
sketch.update('item', 3);  // 再增加 3

console.log(sketch.estimate('item')); // >= 8
```

### 合并多个 Sketch

```typescript
const sketch1 = new CountMinSketch<string>(5, 100);
const sketch2 = new CountMinSketch<string>(5, 100);

sketch1.increment('a');
sketch2.increment('b');
sketch2.increment('b');

sketch1.merge(sketch2);

console.log(sketch1.estimate('a')); // >= 1
console.log(sketch1.estimate('b')); // >= 2
```

### 序列化

```typescript
const sketch = new CountMinSketch<string>(5, 100);
sketch.increment('data');

const bytes = sketch.toBytes();
// bytes 可用于持久化存储
```

## API 文档

### CountMinSketch 类

```typescript
new CountMinSketch<T>(depth: number, width: number, seed?: number)
```

**构造函数参数：**

- `depth` - Sketch 深度（哈希函数数量），越多越精确但越占用空间
- `width` - Sketch 宽度，每行桶的数量，越多越精确
- `seed` - 随机种子（可选，默认 0xDEADBEEF）

### 静态方法

| 方法 | 描述 |
|------|------|
| `optimal(epsilon, delta)` | 根据精度和置信度计算最优 depth/width |
| `withRate<T>(epsilon, delta)` | 创建配置好参数的 sketch 实例 |

### 实例方法

| 方法 | 描述 |
|------|------|
| `increment(item)` | 将 item 的计数加 1 |
| `update(item, delta)` | 将 item 的计数增加 delta |
| `estimate(item)` | 估计 item 的出现次数（下界） |
| `totalCount()` | 返回所有计数之和 |
| `dimensions()` | 返回 [depth, width] |
| `merge(other)` | 合并另一个同尺寸的 sketch |
| `toBytes()` | 序列化为 Uint8Array |
| `clear()` | 清空所有计数 |

### CountMinConfig

```typescript
interface CountMinConfig {
  depth: number;    // 深度
  width: number;    // 宽度
  seed: number;     // 种子
}
```

## 精度说明

Count-Min Sketch 是一种概率数据结构，`estimate()` 返回的是真实计数的**下界估计**（never underestimate but may overestimate）。

- 误差概率：δ（创建时指定）
- 误差范围：ε × total_count（创建时指定）

例如：epsilon=0.01, delta=0.01 表示误差不超过 1% 的计数，概率为 99%。

## 测试

```bash
npx ts-node --transpile-only count_min_sketch.test.ts
```

## 作者

AllToolkit Generator

## 日期

2026-06-15
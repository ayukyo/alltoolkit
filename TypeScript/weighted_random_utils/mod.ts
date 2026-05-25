/**
 * Weighted Random Utils - TypeScript Implementation
 * 
 * 提供加权随机选择功能，支持多种算法实现
 * - 线性扫描法：适合小规模数据集
 * - 别名方法（Alias Method）：O(1) 时间复杂度的采样
 * - 拒绝采样法：适合动态权重场景
 * 
 * 零外部依赖，仅使用 TypeScript 标准库
 */

/**
 * 带权重的选项
 */
export interface WeightedOption<T> {
  /** 选项值 */
  value: T;
  /** 权重（必须为非负数） */
  weight: number;
}

/**
 * 加权随机选择器配置
 */
export interface WeightedRandomConfig {
  /** 是否自动归一化权重（默认 true） */
  normalize?: boolean;
  /** 随机数生成器（默认 Math.random） */
  random?: () => number;
  /** 精度阈值（用于浮点数比较） */
  epsilon?: number;
}

/**
 * 别名表的条目
 */
interface AliasEntry {
  /** 概率值 */
  prob: number;
  /** 别名索引 */
  alias: number;
}

/**
 * 统计信息
 */
export interface Statistics {
  /** 总选项数 */
  totalOptions: number;
  /** 总权重 */
  totalWeight: number;
  /** 最小权重 */
  minWeight: number;
  /** 最大权重 */
  maxWeight: number;
  /** 平均权重 */
  avgWeight: number;
  /** 权重标准差 */
  stdWeight: number;
  /** 有效熵（bits） */
  entropy: number;
}

/**
 * 批量选择结果
 */
export interface BatchResult<T> {
  /** 选择的选项数组 */
  selections: T[];
  /** 每个选项被选择的次数 */
  counts: Map<T, number>;
  /** 每个选项的实际选择频率 */
  frequencies: Map<T, number>;
}

/**
 * 加权随机选择器基类
 */
export class WeightedRandomPicker<T> {
  protected options: WeightedOption<T>[] = [];
  protected weights: number[] = [];
  protected cumulative: number[] = [];
  protected totalWeight: number = 0;
  protected random: () => number;
  protected epsilon: number;

  /**
   * 创建加权随机选择器
   * @param items 选项数组或权重映射
   * @param config 配置选项
   */
  constructor(
    items: WeightedOption<T>[] | Map<T, number> | Record<string, number>,
    config: WeightedRandomConfig = {}
  ) {
    this.random = config.random || Math.random;
    this.epsilon = config.epsilon ?? 1e-10;

    if (Array.isArray(items)) {
      this.options = [...items];
    } else if (items instanceof Map) {
      this.options = Array.from(items.entries()).map(([value, weight]) => ({
        value,
        weight,
      }));
    } else {
      this.options = Object.entries(items).map(([key, weight]) => ({
        value: key as unknown as T,
        weight,
      }));
    }

    this.validateOptions();

    if (config.normalize !== false) {
      this.normalizeWeights();
    }

    this.buildCumulative();
  }

  /**
   * 验证选项有效性
   */
  protected validateOptions(): void {
    if (this.options.length === 0) {
      throw new Error("Options array cannot be empty");
    }

    for (let i = 0; i < this.options.length; i++) {
      const opt = this.options[i];
      if (typeof opt.weight !== "number" || isNaN(opt.weight)) {
        throw new Error(`Invalid weight at index ${i}: must be a number`);
      }
      if (opt.weight < 0) {
        throw new Error(`Invalid weight at index ${i}: weight cannot be negative`);
      }
    }

    const totalWeight = this.options.reduce((sum, opt) => sum + opt.weight, 0);
    if (totalWeight <= 0) {
      throw new Error("Total weight must be positive");
    }
  }

  /**
   * 归一化权重
   */
  protected normalizeWeights(): void {
    const total = this.options.reduce((sum, opt) => sum + opt.weight, 0);
    if (total > 0) {
      for (const opt of this.options) {
        opt.weight = opt.weight / total;
      }
    }
  }

  /**
   * 构建累积权重数组（用于线性扫描）
   */
  protected buildCumulative(): void {
    this.weights = this.options.map((opt) => opt.weight);
    this.cumulative = [];
    let sum = 0;

    for (const w of this.weights) {
      sum += w;
      this.cumulative.push(sum);
    }

    this.totalWeight = sum;
  }

  /**
   * 选择一个选项（线性扫描法）
   * 时间复杂度: O(n)
   */
  pick(): T {
    const r = this.random() * this.totalWeight;

    // 二分查找优化
    let left = 0;
    let right = this.cumulative.length - 1;

    while (left < right) {
      const mid = Math.floor((left + right) / 2);
      if (this.cumulative[mid] < r) {
        left = mid + 1;
      } else {
        right = mid;
      }
    }

    return this.options[left].value;
  }

  /**
   * 选择多个选项（有放回）
   * @param count 选择数量
   */
  pickMultiple(count: number): T[] {
    if (count < 0) {
      throw new Error("Count must be non-negative");
    }
    const results: T[] = [];
    for (let i = 0; i < count; i++) {
      results.push(this.pick());
    }
    return results;
  }

  /**
   * 选择多个不重复的选项（无放回）
   * @param count 选择数量
   */
  pickUnique(count: number): T[] {
    if (count < 0) {
      throw new Error("Count must be non-negative");
    }
    if (count > this.options.length) {
      throw new Error(
        `Cannot pick ${count} unique items from ${this.options.length} options`
      );
    }

    // 创建副本以避免修改原始数据
    const remaining = this.options.map((opt, i) => ({
      value: opt.value,
      weight: this.weights[i],
      originalWeight: opt.weight,
    }));

    const results: T[] = [];

    for (let i = 0; i < count; i++) {
      const totalWeight = remaining.reduce((sum, opt) => sum + opt.weight, 0);
      let r = this.random() * totalWeight;

      let selectedIdx = 0;
      for (let j = 0; j < remaining.length; j++) {
        r -= remaining[j].weight;
        if (r <= this.epsilon) {
          selectedIdx = j;
          break;
        }
        selectedIdx = j;
      }

      results.push(remaining[selectedIdx].value);
      remaining.splice(selectedIdx, 1);
    }

    return results;
  }

  /**
   * 批量选择并统计结果
   * @param count 选择次数
   */
  pickWithStats(count: number): BatchResult<T> {
    const selections = this.pickMultiple(count);
    const counts = new Map<T, number>();

    for (const item of selections) {
      counts.set(item, (counts.get(item) || 0) + 1);
    }

    const frequencies = new Map<T, number>();
    for (const [item, cnt] of counts) {
      frequencies.set(item, cnt / count);
    }

    return { selections, counts, frequencies };
  }

  /**
   * 获取指定选项的权重
   */
  getWeight(value: T): number | undefined {
    const idx = this.options.findIndex((opt) => opt.value === value);
    return idx >= 0 ? this.weights[idx] : undefined;
  }

  /**
   * 获取指定选项的选择概率
   */
  getProbability(value: T): number {
    const weight = this.getWeight(value);
    return weight !== undefined ? weight / this.totalWeight : 0;
  }

  /**
   * 获取所有选项及其权重
   */
  getOptions(): WeightedOption<T>[] {
    return this.options.map((opt, i) => ({
      value: opt.value,
      weight: this.weights[i],
    }));
  }

  /**
   * 获取选项数量
   */
  get size(): number {
    return this.options.length;
  }

  /**
   * 获取统计信息
   */
  getStatistics(): Statistics {
    const weights = this.weights;
    const n = weights.length;
    const total = this.totalWeight;
    const min = Math.min(...weights);
    const max = Math.max(...weights);
    const avg = total / n;

    // 计算标准差
    const variance =
      weights.reduce((sum, w) => sum + Math.pow(w - avg, 2), 0) / n;
    const std = Math.sqrt(variance);

    // 计算熵
    let entropy = 0;
    for (const w of weights) {
      if (w > this.epsilon) {
        const p = w / total;
        entropy -= p * Math.log2(p);
      }
    }

    return {
      totalOptions: n,
      totalWeight: total,
      minWeight: min,
      maxWeight: max,
      avgWeight: avg,
      stdWeight: std,
      entropy,
    };
  }

  /**
   * 重新设置随机数生成器
   */
  setRandom(random: () => number): void {
    this.random = random;
  }
}

/**
 * 基于 Alias Method 的 O(1) 加权随机选择器
 * 
 * 预处理时间: O(n)
 * 采样时间: O(1)
 * 空间复杂度: O(n)
 */
export class AliasPicker<T> {
  private options: T[] = [];
  private aliasTable: AliasEntry[] = [];
  private random: () => number;

  /**
   * 创建 Alias 选择器
   * @param items 选项数组或权重映射
   * @param random 自定义随机数生成器
   */
  constructor(
    items: WeightedOption<T>[] | Map<T, number> | Record<string, number>,
    random?: () => number
  ) {
    this.random = random || Math.random;

    // 处理输入
    if (Array.isArray(items)) {
      this.options = items.map((opt) => opt.value);
      this.buildAliasTable(items.map((opt) => opt.weight));
    } else if (items instanceof Map) {
      const entries = Array.from(items.entries());
      this.options = entries.map(([value]) => value);
      this.buildAliasTable(entries.map(([, weight]) => weight));
    } else {
      const entries = Object.entries(items);
      this.options = entries.map(([key]) => key as unknown as T);
      this.buildAliasTable(entries.map(([, weight]) => weight));
    }
  }

  /**
   * 构建 Alias 表
   * 使用 Vose 算法
   */
  private buildAliasTable(weights: number[]): void {
    const n = weights.length;

    if (n === 0) {
      throw new Error("Options array cannot be empty");
    }

    // 验证权重
    const totalWeight = weights.reduce((sum, w) => sum + w, 0);
    if (totalWeight <= 0) {
      throw new Error("Total weight must be positive");
    }

    // 归一化并缩放到 n
    const scaledWeights = weights.map((w) => (w / totalWeight) * n);

    // 初始化表
    this.aliasTable = scaledWeights.map((w) => ({
      prob: w,
      alias: -1,
    }));

    // 分割为大组和小组
    const small: number[] = [];
    const large: number[] = [];

    for (let i = 0; i < n; i++) {
      if (scaledWeights[i] < 1) {
        small.push(i);
      } else {
        large.push(i);
      }
    }

    // 构建 alias 表
    while (small.length > 0 && large.length > 0) {
      const s = small.pop()!;
      const l = large.pop()!;

      this.aliasTable[s].alias = l;

      // 更新 l 的概率
      const newProb = scaledWeights[l] + scaledWeights[s] - 1;
      scaledWeights[l] = newProb;
      this.aliasTable[l].prob = newProb;

      if (newProb < 1) {
        small.push(l);
      } else {
        large.push(l);
      }
    }

    // 处理剩余的大组（由于浮点精度，可能需要设置概率为 1）
    while (large.length > 0) {
      const l = large.pop()!;
      this.aliasTable[l].prob = 1;
    }

    // 处理剩余的小组（由于浮点精度，可能需要设置概率为 1）
    while (small.length > 0) {
      const s = small.pop()!;
      this.aliasTable[s].prob = 1;
    }
  }

  /**
   * O(1) 选择一个选项
   */
  pick(): T {
    const n = this.options.length;
    const i = Math.floor(this.random() * n);
    const r = this.random();

    const entry = this.aliasTable[i];
    if (r < entry.prob) {
      return this.options[i];
    } else {
      return this.options[entry.alias];
    }
  }

  /**
   * 选择多个选项
   */
  pickMultiple(count: number): T[] {
    const results: T[] = [];
    for (let i = 0; i < count; i++) {
      results.push(this.pick());
    }
    return results;
  }

  /**
   * 获取选项数量
   */
  get size(): number {
    return this.options.length;
  }
}

/**
 * 动态加权随机选择器
 * 
 * 支持动态添加、删除、更新选项
 * 使用拒绝采样法实现
 */
export class DynamicWeightedPicker<T> {
  private options: Map<T, number> = new Map();
  private maxWeight: number = 0;
  private totalWeight: number = 0;
  private random: () => number;

  /**
   * 创建动态选择器
   * @param random 自定义随机数生成器
   */
  constructor(random?: () => number) {
    this.random = random || Math.random;
  }

  /**
   * 添加或更新选项
   */
  set(value: T, weight: number): this {
    if (weight < 0) {
      throw new Error("Weight cannot be negative");
    }

    const oldWeight = this.options.get(value) || 0;
    this.options.set(value, weight);
    this.totalWeight += weight - oldWeight;
    this.updateMaxWeight();

    return this;
  }

  /**
   * 删除选项
   */
  delete(value: T): boolean {
    const weight = this.options.get(value);
    if (weight !== undefined) {
      this.options.delete(value);
      this.totalWeight -= weight;
      this.updateMaxWeight();
      return true;
    }
    return false;
  }

  /**
   * 更新最大权重
   */
  private updateMaxWeight(): void {
    this.maxWeight = 0;
    for (const weight of this.options.values()) {
      if (weight > this.maxWeight) {
        this.maxWeight = weight;
      }
    }
  }

  /**
   * 使用拒绝采样选择一个选项
   * 期望时间复杂度: O(n * maxWeight / totalWeight)
   */
  pick(): T | undefined {
    if (this.options.size === 0 || this.maxWeight <= 0) {
      return undefined;
    }

    // 拒绝采样
    let attempts = 0;
    const maxAttempts = this.options.size * 10;

    while (attempts < maxAttempts) {
      const entries = Array.from(this.options.entries());
      const idx = Math.floor(this.random() * entries.length);
      const [value, weight] = entries[idx];

      // 以 weight/maxWeight 的概率接受
      if (this.random() * this.maxWeight < weight) {
        return value;
      }

      attempts++;
    }

    // 如果拒绝采样失败，回退到线性扫描
    return this.pickByLinearScan();
  }

  /**
   * 线性扫描（回退方案）
   */
  private pickByLinearScan(): T | undefined {
    if (this.options.size === 0) {
      return undefined;
    }

    const r = this.random() * this.totalWeight;
    let sum = 0;

    for (const [value, weight] of this.options) {
      sum += weight;
      if (r <= sum) {
        return value;
      }
    }

    // 返回最后一个
    const entries = Array.from(this.options.entries());
    return entries[entries.length - 1][0];
  }

  /**
   * 选择多个选项
   */
  pickMultiple(count: number): (T | undefined)[] {
    const results: (T | undefined)[] = [];
    for (let i = 0; i < count; i++) {
      results.push(this.pick());
    }
    return results;
  }

  /**
   * 检查是否包含选项
   */
  has(value: T): boolean {
    return this.options.has(value);
  }

  /**
   * 获取选项权重
   */
  getWeight(value: T): number | undefined {
    return this.options.get(value);
  }

  /**
   * 获取选项数量
   */
  get size(): number {
    return this.options.size;
  }

  /**
   * 获取总权重
   */
  get total(): number {
    return this.totalWeight;
  }

  /**
   * 清空所有选项
   */
  clear(): void {
    this.options.clear();
    this.maxWeight = 0;
    this.totalWeight = 0;
  }

  /**
   * 获取所有选项
   */
  entries(): IterableIterator<[T, number]> {
    return this.options.entries();
  }
}

/**
 * 加权随机洗牌
 * 高权重元素更可能出现在前面
 * @param items 选项数组
 * @param random 随机数生成器
 */
export function weightedShuffle<T>(
  items: WeightedOption<T>[],
  random?: () => number
): T[] {
  const rand = random || Math.random;
  const result: T[] = [];
  const remaining = [...items];

  while (remaining.length > 0) {
    const totalWeight = remaining.reduce((sum, opt) => sum + opt.weight, 0);
    let r = rand() * totalWeight;

    for (let i = 0; i < remaining.length; i++) {
      r -= remaining[i].weight;
      if (r <= 0) {
        result.push(remaining[i].value);
        remaining.splice(i, 1);
        break;
      }
    }
  }

  return result;
}

/**
 * 加权随机采样（无放回）
 * @param items 选项数组
 * @param count 采样数量
 * @param random 随机数生成器
 */
export function weightedSample<T>(
  items: WeightedOption<T>[],
  count: number,
  random?: () => number
): T[] {
  if (count > items.length) {
    throw new Error("Sample count cannot exceed population size");
  }

  const picker = new WeightedRandomPicker(items, { random, normalize: false });
  return picker.pickUnique(count);
}

/**
 * 计算加权随机分布的熵
 * @param weights 权重数组
 */
export function calculateEntropy(weights: number[]): number {
  const total = weights.reduce((sum, w) => sum + w, 0);
  if (total <= 0) return 0;

  let entropy = 0;
  const epsilon = 1e-10;

  for (const w of weights) {
    if (w > epsilon) {
      const p = w / total;
      entropy -= p * Math.log2(p);
    }
  }

  return entropy;
}

/**
 * 计算归一化权重
 * @param weights 权重数组
 */
export function normalizeWeights(weights: number[]): number[] {
  const total = weights.reduce((sum, w) => sum + w, 0);
  if (total <= 0) {
    throw new Error("Total weight must be positive");
  }
  return weights.map((w) => w / total);
}

/**
 * 从值和权重数组创建选项
 * @param values 值数组
 * @param weights 权重数组
 */
export function createWeightedOptions<T>(
  values: T[],
  weights: number[]
): WeightedOption<T>[] {
  if (values.length !== weights.length) {
    throw new Error("Values and weights must have the same length");
  }
  return values.map((value, i) => ({ value, weight: weights[i] }));
}

/**
 * 验证权重数组
 * @param weights 权重数组
 */
export function validateWeights(weights: number[]): boolean {
  if (weights.length === 0) return false;
  const total = weights.reduce((sum, w) => {
    if (typeof w !== "number" || isNaN(w) || w < 0) return NaN;
    return sum + w;
  }, 0);
  return !isNaN(total) && total > 0;
}

/**
 * 执行加权随机选择（快速函数式API）
 * @param items 选项数组
 * @param random 随机数生成器
 */
export function weightedPick<T>(
  items: WeightedOption<T>[],
  random?: () => number
): T {
  const picker = new WeightedRandomPicker(items, { random, normalize: false });
  return picker.pick();
}

/**
 * 创建确定性随机数生成器（基于种子）
 * 使用线性同余生成器（LCG）
 * @param seed 种子值
 */
export function createSeededRandom(seed: number): () => number {
  let s = seed;
  return () => {
    s = (s * 1103515245 + 12345) & 0x7fffffff;
    return s / 0x7fffffff;
  };
}

export default {
  WeightedRandomPicker,
  AliasPicker,
  DynamicWeightedPicker,
  weightedShuffle,
  weightedSample,
  calculateEntropy,
  normalizeWeights,
  createWeightedOptions,
  validateWeights,
  weightedPick,
  createSeededRandom,
};
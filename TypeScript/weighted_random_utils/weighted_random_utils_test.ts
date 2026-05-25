/**
 * Weighted Random Utils - 测试文件
 * 
 * 测试加权随机选择工具的所有功能
 */

import {
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
  WeightedOption,
} from "./mod.ts";

// 测试结果收集
let passed = 0;
let failed = 0;
const failures: string[] = [];

function test(name: string, fn: () => void): void {
  try {
    fn();
    passed++;
    console.log(`✅ ${name}`);
  } catch (error) {
    failed++;
    const msg = error instanceof Error ? error.message : String(error);
    failures.push(`${name}: ${msg}`);
    console.log(`❌ ${name}: ${msg}`);
  }
}

function assertEqual<T>(actual: T, expected: T, msg?: string): void {
  if (actual !== expected) {
    throw new Error(
      msg || `Expected ${expected}, got ${actual}`
    );
  }
}

function assertApprox(actual: number, expected: number, epsilon: number = 0.001, msg?: string): void {
  if (Math.abs(actual - expected) > epsilon) {
    throw new Error(
      msg || `Expected ${expected} ± ${epsilon}, got ${actual}`
    );
  }
}

function assertTrue(condition: boolean, msg?: string): void {
  if (!condition) {
    throw new Error(msg || "Expected true");
  }
}

function assertThrows(fn: () => void, expectedMsg?: string): void {
  let thrown = false;
  try {
    fn();
  } catch (e) {
    thrown = true;
    if (expectedMsg && e instanceof Error) {
      assertTrue(
        e.message.includes(expectedMsg),
        `Expected error to include "${expectedMsg}", got "${e.message}"`
      );
    }
  }
  if (!thrown) {
    throw new Error("Expected function to throw");
  }
}

console.log("\n🧪 Weighted Random Utils Tests\n");
console.log("=".repeat(60));

// ========================================
// WeightedRandomPicker Tests
// ========================================
console.log("\n📦 WeightedRandomPicker Tests\n");

test("WeightedRandomPicker - 基本选择", () => {
  const items: WeightedOption<string>[] = [
    { value: "a", weight: 1 },
    { value: "b", weight: 2 },
    { value: "c", weight: 3 },
  ];
  const picker = new WeightedRandomPicker(items);
  const result = picker.pick();
  assertTrue(["a", "b", "c"].includes(result));
});

test("WeightedRandomPicker - 使用 Map 构造", () => {
  const weights = new Map<string, number>();
  weights.set("a", 1);
  weights.set("b", 2);
  weights.set("c", 3);

  const picker = new WeightedRandomPicker(weights);
  const result = picker.pick();
  assertTrue(["a", "b", "c"].includes(result));
});

test("WeightedRandomPicker - 使用对象构造", () => {
  const picker = new WeightedRandomPicker<string>({ a: 1, b: 2, c: 3 });
  const result = picker.pick();
  assertTrue(["a", "b", "c"].includes(result));
});

test("WeightedRandomPicker - 空数组抛出错误", () => {
  assertThrows(
    () => new WeightedRandomPicker<string>([]),
    "empty"
  );
});

test("WeightedRandomPicker - 负权重抛出错误", () => {
  assertThrows(
    () => new WeightedRandomPicker([{ value: "a", weight: -1 }]),
    "negative"
  );
});

test("WeightedRandomPicker - 零总权重抛出错误", () => {
  assertThrows(
    () => new WeightedRandomPicker([{ value: "a", weight: 0 }]),
    "positive"
  );
});

test("WeightedRandomPicker - 归一化权重", () => {
  const items: WeightedOption<string>[] = [
    { value: "a", weight: 10 },
    { value: "b", weight: 20 },
    { value: "c", weight: 70 },
  ];
  const picker = new WeightedRandomPicker(items);
  const options = picker.getOptions();
  
  assertApprox(options[0].weight, 0.1);
  assertApprox(options[1].weight, 0.2);
  assertApprox(options[2].weight, 0.7);
});

test("WeightedRandomPicker - 禁用归一化", () => {
  const items: WeightedOption<string>[] = [
    { value: "a", weight: 10 },
    { value: "b", weight: 20 },
    { value: "c", weight: 70 },
  ];
  const picker = new WeightedRandomPicker(items, { normalize: false });
  const options = picker.getOptions();
  
  assertEqual(options[0].weight, 10);
  assertEqual(options[1].weight, 20);
  assertEqual(options[2].weight, 70);
});

test("WeightedRandomPicker - 多次选择", () => {
  const items: WeightedOption<string>[] = [
    { value: "a", weight: 1 },
    { value: "b", weight: 1 },
    { value: "c", weight: 1 },
  ];
  const picker = new WeightedRandomPicker(items);
  const results = picker.pickMultiple(10);
  assertEqual(results.length, 10);
  for (const r of results) {
    assertTrue(["a", "b", "c"].includes(r));
  }
});

test("WeightedRandomPicker - 负数选择数量抛出错误", () => {
  const picker = new WeightedRandomPicker([{ value: "a", weight: 1 }]);
  assertThrows(() => picker.pickMultiple(-1), "non-negative");
});

test("WeightedRandomPicker - 唯一选择", () => {
  const items: WeightedOption<string>[] = [
    { value: "a", weight: 1 },
    { value: "b", weight: 1 },
    { value: "c", weight: 1 },
  ];
  const picker = new WeightedRandomPicker(items);
  const results = picker.pickUnique(2);
  assertEqual(results.length, 2);
  
  // 确保不重复
  const set = new Set(results);
  assertEqual(set.size, 2);
});

test("WeightedRandomPicker - 唯一选择超出范围抛出错误", () => {
  const picker = new WeightedRandomPicker([
    { value: "a", weight: 1 },
    { value: "b", weight: 1 },
  ]);
  assertThrows(() => picker.pickUnique(3), "Cannot pick");
});

test("WeightedRandomPicker - 带统计的选择", () => {
  const items: WeightedOption<string>[] = [
    { value: "a", weight: 1 },
    { value: "b", weight: 1 },
    { value: "c", weight: 1 },
  ];
  const picker = new WeightedRandomPicker(items);
  const result = picker.pickWithStats(1000);
  
  assertEqual(result.selections.length, 1000);
  assertTrue(result.counts.size <= 3);
  assertTrue(result.frequencies.size <= 3);
  
  // 验证频率之和约为 1
  let totalFreq = 0;
  for (const freq of result.frequencies.values()) {
    totalFreq += freq;
  }
  assertApprox(totalFreq, 1, 0.001);
});

test("WeightedRandomPicker - 获取权重", () => {
  const picker = new WeightedRandomPicker([
    { value: "a", weight: 1 },
    { value: "b", weight: 2 },
  ]);
  
  const weightA = picker.getWeight("a");
  const weightB = picker.getWeight("b");
  const weightC = picker.getWeight("c");
  
  assertApprox(weightA!, 0.333, 0.01);
  assertApprox(weightB!, 0.666, 0.01);
  assertEqual(weightC, undefined);
});

test("WeightedRandomPicker - 获取概率", () => {
  const picker = new WeightedRandomPicker([
    { value: "a", weight: 1 },
    { value: "b", weight: 2 },
  ], { normalize: false });
  
  assertApprox(picker.getProbability("a"), 0.333, 0.01);
  assertApprox(picker.getProbability("b"), 0.666, 0.01);
  assertEqual(picker.getProbability("c"), 0);
});

test("WeightedRandomPicker - size 属性", () => {
  const picker = new WeightedRandomPicker([
    { value: "a", weight: 1 },
    { value: "b", weight: 2 },
  ]);
  assertEqual(picker.size, 2);
});

test("WeightedRandomPicker - 统计信息", () => {
  const picker = new WeightedRandomPicker([
    { value: "a", weight: 1 },
    { value: "b", weight: 2 },
    { value: "c", weight: 3 },
  ]);
  
  const stats = picker.getStatistics();
  assertEqual(stats.totalOptions, 3);
  assertApprox(stats.totalWeight, 1, 0.001);
  assertApprox(stats.minWeight, 0.166, 0.01);
  assertApprox(stats.maxWeight, 0.5, 0.01);
  assertApprox(stats.avgWeight, 0.333, 0.01);
  assertTrue(stats.entropy > 0);
});

test("WeightedRandomPicker - 自定义随机数生成器", () => {
  const fixedRandom = createSeededRandom(42);
  const picker = new WeightedRandomPicker(
    [{ value: "a", weight: 1 }, { value: "b", weight: 1 }],
    { random: fixedRandom }
  );
  
  // 使用相同种子应该产生相同结果
  const picker2 = new WeightedRandomPicker(
    [{ value: "a", weight: 1 }, { value: "b", weight: 1 }],
    { random: createSeededRandom(42) }
  );
  
  assertEqual(picker.pick(), picker2.pick());
});

test("WeightedRandomPicker - setRandom 方法", () => {
  const picker = new WeightedRandomPicker([
    { value: "a", weight: 1 },
    { value: "b", weight: 1 },
  ]);
  
  picker.setRandom(createSeededRandom(123));
  const result = picker.pick();
  assertTrue(["a", "b"].includes(result));
});

// ========================================
// AliasPicker Tests
// ========================================
console.log("\n⚡ AliasPicker Tests\n");

test("AliasPicker - 基本选择", () => {
  const items: WeightedOption<string>[] = [
    { value: "a", weight: 1 },
    { value: "b", weight: 2 },
    { value: "c", weight: 3 },
  ];
  const picker = new AliasPicker(items);
  const result = picker.pick();
  assertTrue(["a", "b", "c"].includes(result));
});

test("AliasPicker - 使用 Map 构造", () => {
  const weights = new Map<string, number>();
  weights.set("a", 1);
  weights.set("b", 2);
  weights.set("c", 3);

  const picker = new AliasPicker(weights);
  const result = picker.pick();
  assertTrue(["a", "b", "c"].includes(result));
});

test("AliasPicker - 使用对象构造", () => {
  const picker = new AliasPicker<string>({ a: 1, b: 2, c: 3 });
  const result = picker.pick();
  assertTrue(["a", "b", "c"].includes(result));
});

test("AliasPicker - 空数组抛出错误", () => {
  assertThrows(() => new AliasPicker([]), "empty");
});

test("AliasPicker - 零总权重抛出错误", () => {
  assertThrows(
    () => new AliasPicker([{ value: "a", weight: 0 }]),
    "positive"
  );
});

test("AliasPicker - 多次选择", () => {
  const picker = new AliasPicker([
    { value: "a", weight: 1 },
    { value: "b", weight: 1 },
    { value: "c", weight: 1 },
  ]);
  const results = picker.pickMultiple(100);
  assertEqual(results.length, 100);
  for (const r of results) {
    assertTrue(["a", "b", "c"].includes(r));
  }
});

test("AliasPicker - size 属性", () => {
  const picker = new AliasPicker([
    { value: "a", weight: 1 },
    { value: "b", weight: 2 },
  ]);
  assertEqual(picker.size, 2);
});

test("AliasPicker - 权重分布正确", () => {
  // 使用确定性随机测试分布
  const seed = 12345;
  const picker = new AliasPicker(
    [
      { value: "a", weight: 1 },
      { value: "b", weight: 9 },
    ],
    createSeededRandom(seed)
  );
  
  // 多次采样验证 b 的频率远高于 a
  const counts = { a: 0, b: 0 };
  for (let i = 0; i < 1000; i++) {
    counts[picker.pick() as keyof typeof counts]++;
  }
  
  assertTrue(counts.b > counts.a);
});

// ========================================
// DynamicWeightedPicker Tests
// ========================================
console.log("\n🔄 DynamicWeightedPicker Tests\n");

test("DynamicWeightedPicker - 空选择器返回 undefined", () => {
  const picker = new DynamicWeightedPicker<string>();
  assertEqual(picker.pick(), undefined);
});

test("DynamicWeightedPicker - 添加选项后选择", () => {
  const picker = new DynamicWeightedPicker<string>();
  picker.set("a", 1).set("b", 2);
  const result = picker.pick();
  assertTrue(["a", "b"].includes(result!));
});

test("DynamicWeightedPicker - 删除选项", () => {
  const picker = new DynamicWeightedPicker<string>();
  picker.set("a", 1).set("b", 2);
  assertTrue(picker.delete("a"));
  assertEqual(picker.size, 1);
  assertEqual(picker.pick(), "b");
});

test("DynamicWeightedPicker - 删除不存在的选项", () => {
  const picker = new DynamicWeightedPicker<string>();
  picker.set("a", 1);
  assertEqual(picker.delete("b"), false);
});

test("DynamicWeightedPicker - 更新权重", () => {
  const picker = new DynamicWeightedPicker<string>();
  picker.set("a", 1);
  picker.set("a", 10);
  assertEqual(picker.getWeight("a"), 10);
});

test("DynamicWeightedPicker - 负权重抛出错误", () => {
  const picker = new DynamicWeightedPicker<string>();
  assertThrows(() => picker.set("a", -1), "negative");
});

test("DynamicWeightedPicker - has 方法", () => {
  const picker = new DynamicWeightedPicker<string>();
  picker.set("a", 1);
  assertTrue(picker.has("a"));
  assertTrue(!picker.has("b"));
});

test("DynamicWeightedPicker - size 和 total 属性", () => {
  const picker = new DynamicWeightedPicker<string>();
  picker.set("a", 1).set("b", 2).set("c", 3);
  assertEqual(picker.size, 3);
  assertEqual(picker.total, 6);
});

test("DynamicWeightedPicker - 清空", () => {
  const picker = new DynamicWeightedPicker<string>();
  picker.set("a", 1).set("b", 2);
  picker.clear();
  assertEqual(picker.size, 0);
  assertEqual(picker.total, 0);
  assertEqual(picker.pick(), undefined);
});

test("DynamicWeightedPicker - 多次选择", () => {
  const picker = new DynamicWeightedPicker<string>();
  picker.set("a", 1).set("b", 1);
  const results = picker.pickMultiple(10);
  assertEqual(results.length, 10);
  for (const r of results) {
    assertTrue(["a", "b"].includes(r!));
  }
});

test("DynamicWeightedPicker - entries 方法", () => {
  const picker = new DynamicWeightedPicker<string>();
  picker.set("a", 1).set("b", 2);
  const entries = Array.from(picker.entries());
  assertEqual(entries.length, 2);
});

// ========================================
// Helper Functions Tests
// ========================================
console.log("\n🛠️ Helper Functions Tests\n");

test("weightedShuffle - 基本洗牌", () => {
  const items: WeightedOption<string>[] = [
    { value: "a", weight: 1 },
    { value: "b", weight: 1 },
    { value: "c", weight: 1 },
  ];
  const result = weightedShuffle(items);
  assertEqual(result.length, 3);
  assertTrue(result.includes("a"));
  assertTrue(result.includes("b"));
  assertTrue(result.includes("c"));
});

test("weightedShuffle - 高权重元素更可能在前", () => {
  const items: WeightedOption<string>[] = [
    { value: "low", weight: 1 },
    { value: "high", weight: 100 },
  ];
  
  // 多次实验验证 high 更可能出现在第一个
  let highFirst = 0;
  for (let i = 0; i < 100; i++) {
    const result = weightedShuffle(items);
    if (result[0] === "high") highFirst++;
  }
  assertTrue(highFirst > 90); // high 权重大，应该几乎总是在前
});

test("weightedSample - 基本采样", () => {
  const items: WeightedOption<string>[] = [
    { value: "a", weight: 1 },
    { value: "b", weight: 1 },
    { value: "c", weight: 1 },
  ];
  const result = weightedSample(items, 2);
  assertEqual(result.length, 2);
  
  // 不重复
  const set = new Set(result);
  assertEqual(set.size, 2);
});

test("weightedSample - 超出数量抛出错误", () => {
  const items: WeightedOption<string>[] = [
    { value: "a", weight: 1 },
    { value: "b", weight: 1 },
  ];
  assertThrows(() => weightedSample(items, 3), "exceed");
});

test("calculateEntropy - 计算熵", () => {
  // 均匀分布熵最大
  const uniform = [1, 1, 1, 1];
  const skewed = [10, 1, 1, 1];
  const single = [1];
  
  const entropyUniform = calculateEntropy(uniform);
  const entropySkewed = calculateEntropy(skewed);
  const entropySingle = calculateEntropy(single);
  
  assertEqual(entropySingle, 0); // 单选项熵为 0
  assertTrue(entropyUniform > entropySkewed); // 均匀分布熵更大
});

test("calculateEntropy - 空数组返回 0", () => {
  assertEqual(calculateEntropy([]), 0);
});

test("calculateEntropy - 零权重数组返回 0", () => {
  assertEqual(calculateEntropy([0, 0, 0]), 0);
});

test("normalizeWeights - 基本归一化", () => {
  const weights = [1, 2, 3];
  const normalized = normalizeWeights(weights);
  
  assertApprox(normalized[0], 0.166, 0.01);
  assertApprox(normalized[1], 0.333, 0.01);
  assertApprox(normalized[2], 0.5, 0.01);
});

test("normalizeWeights - 零总权重抛出错误", () => {
  assertThrows(() => normalizeWeights([0, 0]), "positive");
});

test("createWeightedOptions - 创建选项", () => {
  const values = ["a", "b", "c"];
  const weights = [1, 2, 3];
  const options = createWeightedOptions(values, weights);
  
  assertEqual(options.length, 3);
  assertEqual(options[0].value, "a");
  assertEqual(options[0].weight, 1);
  assertEqual(options[2].value, "c");
  assertEqual(options[2].weight, 3);
});

test("createWeightedOptions - 长度不匹配抛出错误", () => {
  assertThrows(
    () => createWeightedOptions(["a", "b"], [1]),
    "same length"
  );
});

test("validateWeights - 有效权重", () => {
  assertTrue(validateWeights([1, 2, 3]));
  assertTrue(validateWeights([0.1, 0.2, 0.3]));
  assertTrue(validateWeights([1])); // 单元素
});

test("validateWeights - 无效权重", () => {
  assertTrue(!validateWeights([])); // 空数组
  assertTrue(!validateWeights([0, 0, 0])); // 零权重
  assertTrue(!validateWeights([-1, 2, 3])); // 负权重
  assertTrue(!validateWeights([1, NaN, 3])); // NaN
});

test("weightedPick - 快速选择", () => {
  const items: WeightedOption<string>[] = [
    { value: "a", weight: 1 },
    { value: "b", weight: 2 },
    { value: "c", weight: 3 },
  ];
  const result = weightedPick(items);
  assertTrue(["a", "b", "c"].includes(result));
});

test("createSeededRandom - 确定性随机", () => {
  const random1 = createSeededRandom(42);
  const random2 = createSeededRandom(42);
  
  // 相同种子应产生相同序列
  for (let i = 0; i < 10; i++) {
    assertEqual(random1(), random2());
  }
});

test("createSeededRandom - 值在 0-1 范围内", () => {
  const random = createSeededRandom(12345);
  for (let i = 0; i < 100; i++) {
    const value = random();
    assertTrue(value >= 0 && value < 1);
  }
});

// ========================================
// Edge Cases Tests
// ========================================
console.log("\n⚠️ Edge Cases Tests\n");

test("单选项选择", () => {
  const picker = new WeightedRandomPicker([{ value: "only", weight: 1 }]);
  assertEqual(picker.pick(), "only");
  assertEqual(picker.pickMultiple(5).every((x) => x === "only"), true);
});

test("极小权重", () => {
  const picker = new WeightedRandomPicker([
    { value: "small", weight: 0.0000001 },
    { value: "large", weight: 1 },
  ]);
  // 应该能正常工作
  const result = picker.pick();
  assertTrue(["small", "large"].includes(result));
});

test("极大权重", () => {
  const picker = new WeightedRandomPicker([
    { value: "a", weight: 1000000 },
    { value: "b", weight: 1000000 },
  ]);
  const result = picker.pick();
  assertTrue(["a", "b"].includes(result));
});

test("浮点权重", () => {
  const picker = new WeightedRandomPicker([
    { value: "a", weight: 0.1 },
    { value: "b", weight: 0.2 },
    { value: "c", weight: 0.7 },
  ]);
  const result = picker.pick();
  assertTrue(["a", "b", "c"].includes(result));
});

test("权重一致性测试", () => {
  // 测试选择频率与权重成比例
  const items: WeightedOption<string>[] = [
    { value: "a", weight: 1 },
    { value: "b", weight: 2 },
    { value: "c", weight: 3 },
  ];
  const picker = new WeightedRandomPicker(items);
  
  const counts: Record<string, number> = { a: 0, b: 0, c: 0 };
  const iterations = 10000;
  
  for (let i = 0; i < iterations; i++) {
    counts[picker.pick()]++;
  }
  
  // c 应该大约是 a 的 3 倍
  const ratio = counts.c / counts.a;
  assertTrue(ratio > 2.5 && ratio < 3.5, `Ratio should be ~3, got ${ratio}`);
});

// ========================================
// Performance Tests
// ========================================
console.log("\n🚀 Performance Tests\n");

test("WeightedRandomPicker - 大数据集性能", () => {
  const items: WeightedOption<number>[] = [];
  for (let i = 0; i < 1000; i++) {
    items.push({ value: i, weight: Math.random() + 0.1 });
  }
  
  const picker = new WeightedRandomPicker(items);
  const start = Date.now();
  
  for (let i = 0; i < 1000; i++) {
    picker.pick();
  }
  
  const elapsed = Date.now() - start;
  assertTrue(elapsed < 100, `Should be fast, took ${elapsed}ms`);
});

test("AliasPicker - 大数据集性能", () => {
  const items: WeightedOption<number>[] = [];
  for (let i = 0; i < 1000; i++) {
    items.push({ value: i, weight: Math.random() + 0.1 });
  }
  
  const picker = new AliasPicker(items);
  const start = Date.now();
  
  for (let i = 0; i < 10000; i++) {
    picker.pick();
  }
  
  const elapsed = Date.now() - start;
  assertTrue(elapsed < 50, `Should be very fast, took ${elapsed}ms`);
});

// ========================================
// Summary
// ========================================
console.log("\n" + "=".repeat(60));
console.log(`\n📊 测试结果: ${passed} passed, ${failed} failed\n`);

if (failed > 0) {
  console.log("❌ Failed tests:");
  failures.forEach((f) => console.log(`   - ${f}`));
  Deno.exit(1);
} else {
  console.log("✅ All tests passed!");
}
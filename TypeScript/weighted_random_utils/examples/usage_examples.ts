/**
 * Weighted Random Utils - 使用示例
 * 
 * 展示加权随机选择工具的各种用法
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
} from "../mod.ts";

console.log("=".repeat(60));
console.log("📊 Weighted Random Utils - 使用示例");
console.log("=".repeat(60));

// ========================================
// 1. 基本用法
// ========================================
console.log("\n📌 1. 基本用法\n");

// 创建加权选项
const colors = [
  { value: "red", weight: 10 },
  { value: "green", weight: 30 },
  { value: "blue", weight: 60 },
];

// 创建选择器
const picker = new WeightedRandomPicker(colors);
console.log("随机选择颜色:", picker.pick());

// 多次选择
console.log("选择 5 个颜色:", picker.pickMultiple(5));

// ========================================
// 2. 不同构造方式
// ========================================
console.log("\n📌 2. 不同构造方式\n");

// 使用 Map
const weightsMap = new Map<string, number>();
weightsMap.set("optionA", 25);
weightsMap.set("optionB", 75);

const mapPicker = new WeightedRandomPicker(weightsMap);
console.log("从 Map 选择:", mapPicker.pick());

// 使用对象
const objPicker = new WeightedRandomPicker<string>({
  optionA: 25,
  optionB: 75,
});
console.log("从对象选择:", objPicker.pick());

// ========================================
// 3. 统计信息
// ========================================
console.log("\n📌 3. 统计信息\n");

const items = [
  { value: "low", weight: 1 },
  { value: "medium", weight: 5 },
  { value: "high", weight: 10 },
];

const statsPicker = new WeightedRandomPicker(items);
const stats = statsPicker.getStatistics();

console.log("选项数量:", stats.totalOptions);
console.log("总权重:", stats.totalWeight.toFixed(4));
console.log("最小权重:", stats.minWeight.toFixed(4));
console.log("最大权重:", stats.maxWeight.toFixed(4));
console.log("平均权重:", stats.avgWeight.toFixed(4));
console.log("标准差:", stats.stdWeight.toFixed(4));
console.log("熵:", stats.entropy.toFixed(4), "bits");

// ========================================
// 4. 批量选择统计
// ========================================
console.log("\n📌 4. 批量选择统计\n");

const diceItems = [
  { value: "1", weight: 1 },
  { value: "2", weight: 1 },
  { value: "3", weight: 1 },
  { value: "4", weight: 1 },
  { value: "5", weight: 1 },
  { value: "6", weight: 1 },
];

const dicePicker = new WeightedRandomPicker(diceItems);
const batchResult = dicePicker.pickWithStats(1000);

console.log("掷骰子 1000 次:");
console.log("选择结果:", batchResult.selections.slice(0, 10), "...");

for (const [value, count] of batchResult.counts) {
  console.log(
    `  ${value}: ${count} 次 (${batchResult.frequencies.get(value)!.toFixed(2)}%)`
  );
}

// ========================================
// 5. 唯一选择（无放回）
// ========================================
console.log("\n📌 5. 唯一选择（无放回）\n");

const lotteryItems = [
  { value: "grand-prize", weight: 1 },
  { value: "second-prize", weight: 10 },
  { value: "third-prize", weight: 50 },
  { value: " consolation", weight: 100 },
  { value: "nothing", weight: 500 },
];

const lotteryPicker = new WeightedRandomPicker(lotteryItems);
console.log("抽奖（无放回，3 个奖项）:", lotteryPicker.pickUnique(3));

// ========================================
// 6. Alias Method - O(1) 采样
// ========================================
console.log("\n📌 6. Alias Method - O(1) 高效采样\n");

const largeDataset = [];
for (let i = 0; i < 1000; i++) {
  largeDataset.push({ value: `item-${i}`, weight: Math.random() + 0.1 });
}

console.log("创建包含 1000 个选项的 Alias 选择器...");
const aliasPicker = new AliasPicker(largeDataset);

const startAlias = Date.now();
const aliasResults = aliasPicker.pickMultiple(10000);
const aliasTime = Date.now() - startAlias;

console.log(`AliasPicker 采样 10000 次: ${aliasTime}ms`);
console.log("部分结果:", aliasResults.slice(0, 5));

// ========================================
// 7. 动态选择器
// ========================================
console.log("\n📌 7. 动态加权选择器\n");

const dynamicPicker = new DynamicWeightedPicker<string>();

// 动态添加选项
dynamicPicker.set("server-A", 30);
dynamicPicker.set("server-B", 50);
dynamicPicker.set("server-C", 20);

console.log("负载均衡 - 选择服务器:", dynamicPicker.pick());
console.log("当前选项数:", dynamicPicker.size);
console.log("总权重:", dynamicPicker.total);

// 更新权重（模拟服务器负载变化）
dynamicPicker.set("server-A", 60); // 增加权重
dynamicPicker.set("server-C", 5); // 降低权重

console.log("\n调整权重后:");
console.log("server-A 权重:", dynamicPicker.getWeight("server-A"));
console.log("选择服务器:", dynamicPicker.pick());

// 删除服务器
dynamicPicker.delete("server-C");
console.log("\n删除 server-C 后:");
console.log("选择服务器:", dynamicPicker.pick());

// ========================================
// 8. 加权洗牌
// ========================================
console.log("\n📌 8. 加权洗牌\n");

const playlist = [
  { value: "song-popular", weight: 100 },
  { value: "song-medium", weight: 30 },
  { value: "song-rare", weight: 5 },
  { value: "song-new", weight: 20 },
];

const shuffledPlaylist = weightedShuffle(playlist);
console.log("按热度洗牌播放列表:", shuffledPlaylist);

// ========================================
// 9. 加权采样
// ========================================
console.log("\n📌 9. 加权采样（无放回）\n");

const candidates = [
  { value: "candidate-A", weight: 40 },
  { value: "candidate-B", weight: 30 },
  { value: "candidate-C", weight: 20 },
  { value: "candidate-D", weight: 10 },
];

const selectedCandidates = weightedSample(candidates, 2);
console.log("加权随机抽样候选人:", selectedCandidates);

// ========================================
// 10. 熵计算
// ========================================
console.log("\n📌 10. 熵计算\n");

const uniformWeights = [1, 1, 1, 1];
const skewedWeights = [10, 1, 1, 1];
const extremeWeights = [100, 1];

console.log("均匀分布熵:", calculateEntropy(uniformWeights).toFixed(4), "bits");
console.log("偏斜分布熵:", calculateEntropy(skewedWeights).toFixed(4), "bits");
console.log("极端分布熵:", calculateEntropy(extremeWeights).toFixed(4), "bits");

console.log("\n💡 熵越高，随机性越大");

// ========================================
// 11. 确定性随机（种子）
// ========================================
console.log("\n📌 11. 确定性随机（种子）\n");

// 相同种子产生相同结果
const seededPicker1 = new WeightedRandomPicker(
  [{ value: "a", weight: 1 }, { value: "b", weight: 1 }, { value: "c", weight: 1 }],
  { random: createSeededRandom(42) }
);

const seededPicker2 = new WeightedRandomPicker(
  [{ value: "a", weight: 1 }, { value: "b", weight: 1 }, { value: "c", weight: 1 }],
  { random: createSeededRandom(42) }
);

console.log("使用种子 42:");
const picks1 = seededPicker1.pickMultiple(5);
const picks2 = seededPicker2.pickMultiple(5);

console.log("Picker 1:", picks1);
console.log("Picker 2:", picks2);
console.log("结果一致:", picks1.every((v, i) => v === picks2[i]));

// ========================================
// 12. 实际应用：A/B 测试
// ========================================
console.log("\n📌 12. 实际应用：A/B 测试\n");

const abTestPicker = new WeightedRandomPicker({
  "control-group": 70,
  "variant-A": 15,
  "variant-B": 15,
});

console.log("A/B 测试分组分配:");
const groupCounts: Record<string, number> = {
  "control-group": 0,
  "variant-A": 0,
  "variant-B": 0,
};

for (let i = 0; i < 100; i++) {
  const group = abTestPicker.pick();
  groupCounts[group]++;
}

for (const [group, count] of Object.entries(groupCounts)) {
  console.log(`  ${group}: ${count}%`);
}

// ========================================
// 13. 实际应用：负载均衡
// ========================================
console.log("\n📌 13. 实际应用：负载均衡\n");

const serverPicker = new DynamicWeightedPicker<string>();

// 根据服务器容量设置权重
serverPicker.set("high-capacity", 100);
serverPicker.set("medium-capacity", 50);
serverPicker.set("low-capacity", 20);

console.log("负载均衡 - 分配请求:");
const serverCounts: Record<string, number> = {};

for (let i = 0; i < 20; i++) {
  const server = serverPicker.pick()!;
  serverCounts[server] = (serverCounts[server] || 0) + 1;
}

for (const [server, count] of Object.entries(serverCounts)) {
  console.log(`  ${server}: ${count} 个请求`);
}

// ========================================
// 14. 快速函数式 API
// ========================================
console.log("\n📌 14. 快速函数式 API\n");

const quickItems = [
  { value: "gold", weight: 1 },
  { value: "silver", weight: 10 },
  { value: "bronze", weight: 50 },
];

console.log("快速单次选择:", weightedPick(quickItems));

const normalizedWeights = normalizeWeights([1, 2, 3]);
console.log("归一化权重:", normalizedWeights.map((w) => w.toFixed(4)));

const options = createWeightedOptions(["x", "y", "z"], [1, 2, 3]);
console.log("创建选项:", options);

console.log("验证权重:", validateWeights([1, 2, 3]));

// ========================================
// 15. 禁用归一化
// ========================================
console.log("\n📌 15. 禁用归一化\n");

const rawWeightsPicker = new WeightedRandomPicker(
  [
    { value: "a", weight: 10 },
    { value: "b", weight: 20 },
    { value: "c", weight: 70 },
  ],
  { normalize: false }
);

const rawOptions = rawWeightsPicker.getOptions();
console.log("原始权重（未归一化）:");
for (const opt of rawOptions) {
  console.log(`  ${opt.value}: ${opt.weight}`);
}

console.log("\n" + "=".repeat(60));
console.log("✅ 示例完成");
console.log("=".repeat(60));
#!/usr/bin/env lua
---
-- Math Utils Basic Examples
-- 基础使用示例
--
-- 运行：lua examples/basic_examples.lua

local path = arg and arg[0] and arg[0]:match("(.*/)") or ""
local MathUtils = dofile(path .. "../mod.lua")

print("🧮 AllToolkit Lua Math Utils - Basic Examples")
print(string.rep("=", 50))

-- 1. 基础计算
print("\n📐 基础计算:")
print(string.format("  四舍五入：%.2f → %.2f", 3.14159, MathUtils.round(3.14159, 2)))
print(string.format("  限制范围：15 在 [0,10] → %d", MathUtils.clamp(15, 0, 10)))
print(string.format("  线性插值：lerp(0, 100, 0.5) = %.1f", MathUtils.lerp(0, 100, 0.5)))
print(string.format("  安全除法：10 / 0 = %d (默认值)", MathUtils.safe_divide(10, 0, -1)))

-- 2. 统计计算
print("\n📊 统计计算:")
local data = {12, 15, 18, 22, 25, 28, 30}
print(string.format("  数据集：%s", table.concat(data, ", ")))
print(string.format("  总和：%d", MathUtils.sum(data)))
print(string.format("  平均值：%.2f", MathUtils.average(data)))
print(string.format("  中位数：%d", MathUtils.median(data)))
print(string.format("  标准差：%.2f", MathUtils.stddev(data)))
print(string.format("  最小值：%d", MathUtils.min(data)))
print(string.format("  最大值：%d", MathUtils.max(data)))

-- 3. 数论
print("\n🔢 数论:")
print(string.format("  GCD(48, 18) = %d", MathUtils.gcd(48, 18)))
print(string.format("  LCM(4, 6) = %d", MathUtils.lcm(4, 6)))
print(string.format("  17 是质数吗？%s", MathUtils.is_prime(17) and "是" or "否"))
print(string.format("  100 以内的最大质数：%d", MathUtils.prev_prime(100)))
print(string.format("  10 的阶乘：%d", MathUtils.factorial(10)))
print(string.format("  C(52, 5) = %d (扑克牌组合)", MathUtils.combinations(52, 5)))

-- 4. 三角函数
print("\n📐 三角函数 (角度版):")
print(string.format("  sin(30°) = %.2f", MathUtils.sin_deg(30)))
print(string.format("  cos(60°) = %.2f", MathUtils.cos_deg(60)))
print(string.format("  tan(45°) = %.2f", MathUtils.tan_deg(45)))
print(string.format("  90° = %.4f 弧度", MathUtils.deg_to_rad(90)))

-- 5. 格式化
print("\n💰 格式化:")
print(string.format("  1234567 → %s", MathUtils.format_thousands(1234567)))
print(string.format("  1048576 bytes → %s", MathUtils.format_bytes(1048576)))
print(string.format("  1234.56 美元 → %s", MathUtils.format_currency(1234.56, "$")))
print(string.format("  123456789 → %s", MathUtils.format_scientific(123456789, 2)))

-- 6. 随机数
print("\n🎲 随机数:")
print(string.format("  随机整数 (1-100): %d", MathUtils.random_int(1, 100)))
print(string.format("  随机浮点数 (0-1): %.4f", MathUtils.random_float(0, 1)))
print(string.format("  随机选择：{苹果，香蕉，橙子} → %s", 
    MathUtils.random_choice({"苹果", "香蕉", "橙子"})))
print(string.format("  UUID: %s", MathUtils.uuid()))

-- 7. 向量
print("\n🔷 向量操作:")
local v1 = {1, 2, 3}
local v2 = {4, 5, 6}
local sum_v = MathUtils.vector_add(v1, v2)
print(string.format("  (%d,%d,%d) + (%d,%d,%d) = (%d,%d,%d)", 
    v1[1], v1[2], v1[3], v2[1], v2[2], v2[3], sum_v[1], sum_v[2], sum_v[3]))
print(string.format("  点积：%d", MathUtils.dot_product(v1, v2)))
print(string.format("  向量 (3,4) 的长度：%.1f", MathUtils.vector_length({3, 4})))
print(string.format("  点 (0,0) 到 (3,4) 的距离：%.1f", MathUtils.distance({0, 0}, {3, 4})))

-- 8. 序列
print("\n🔗 序列生成:")
local fibs = MathUtils.fibonacci(10)
print(string.format("  斐波那契数列 (前 10 项): %s", table.concat(fibs, ", ")))
print(string.format("  第 20 个斐波那契数：%d", MathUtils.fib(20)))
print(string.format("  range_seq(0, 10, 2): %s", table.concat(MathUtils.range_seq(0, 10, 2), ", ")))

-- 9. 特殊函数
print("\n✨ 特殊函数:")
print(string.format("  ln(e) = %.6f", MathUtils.ln(MathUtils.E)))
print(string.format("  log₂(1024) = %.0f", MathUtils.log2(1024)))
print(string.format("  √144 = %.0f", MathUtils.sqrt(144)))
print(string.format("  ³√27 = %.0f", MathUtils.cbrt(27)))
print(string.format("  2¹⁰ = %.0f", MathUtils.power(2, 10)))
print(string.format("  sign(-42) = %d", MathUtils.sign(-42)))
print(string.format("  12345 的位数：%d", MathUtils.digit_count(12345)))
print(string.format("  12345 反转：%d", MathUtils.reverse_number(12345)))
print(string.format("  12345 各位和：%d", MathUtils.digit_sum(12345)))

-- 10. 实际应用示例
print("\n🎯 实际应用:")

-- 计算成绩统计
local scores = {85, 92, 78, 90, 88, 76, 95, 89, 84, 91}
print("\n  📝 学生成绩分析:")
print(string.format("     平均分：%.1f", MathUtils.average(scores)))
print(string.format("     最高分：%d", MathUtils.max(scores)))
print(string.format("     最低分：%d", MathUtils.min(scores)))
print(string.format("     标准差：%.2f (反映成绩离散程度)", MathUtils.stddev(scores)))

-- 计算增长率
local revenue_2024 = 1000000
local revenue_2025 = 1350000
print("\n  💹 收入增长分析:")
print(string.format("     2024 年：$%s", MathUtils.format_thousands(revenue_2024)))
print(string.format("     2025 年：$%s", MathUtils.format_thousands(revenue_2025)))
print(string.format("     增长率：%.1f%%", MathUtils.growth_rate(revenue_2024, revenue_2025)))

-- 判断质数（密码学应用）
print("\n  🔐 密码学应用:")
local test_nums = {97, 98, 99, 100, 101}
for _, n in ipairs(test_nums) do
    if MathUtils.is_prime(n) then
        print(string.format("     %d 是质数 ✓ (可用于加密)", n))
    end
end

print("\n" .. string.rep("=", 50))
print("✅ 示例完成!")

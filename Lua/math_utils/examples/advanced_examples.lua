#!/usr/bin/env lua
---
-- Math Utils Advanced Examples
-- 高级应用示例 - 矩阵、向量、数据分析
--
-- 运行：lua examples/advanced_examples.lua

local path = arg and arg[0] and arg[0]:match("(.*/)") or ""
local MathUtils = dofile(path .. "../mod.lua")

print("🧮 AllToolkit Lua Math Utils - Advanced Examples")
print(string.rep("=", 50))

-------------------------------------------------------------------------------
-- 1. 2D 图形变换
-------------------------------------------------------------------------------
print("\n🎨 2D 图形变换:")

-- 旋转矩阵 (逆时针旋转 θ 角度)
local function rotation_matrix(angle_deg)
    local rad = MathUtils.deg_to_rad(angle_deg)
    local cos_a = MathUtils.cos_deg(angle_deg)
    local sin_a = MathUtils.sin_deg(angle_deg)
    return {
        {cos_a, -sin_a},
        {sin_a, cos_a}
    }
end

-- 缩放矩阵
local function scale_matrix(sx, sy)
    return {
        {sx, 0},
        {0, sy}
    }
end

local point = {1, 0}  -- 点 (1, 0)
print(string.format("  原始点：(%.1f, %.1f)", point[1], point[2]))

-- 旋转 90 度
local rot_90 = rotation_matrix(90)
local rotated = MathUtils.matrix_vector_multiply(rot_90, point)
print(string.format("  旋转 90° 后：(%.2f, %.2f)", rotated[1], rotated[2]))

-- 旋转 180 度
local rot_180 = rotation_matrix(180)
rotated = MathUtils.matrix_vector_multiply(rot_180, point)
print(string.format("  旋转 180° 后：(%.2f, %.2f)", rotated[1], rotated[2]))

-- 缩放 2 倍
local scale = scale_matrix(2, 2)
local scaled = MathUtils.matrix_vector_multiply(scale, point)
print(string.format("  缩放 2 倍后：(%.1f, %.1f)", scaled[1], scaled[2]))

-------------------------------------------------------------------------------
-- 2. 3D 向量计算
-------------------------------------------------------------------------------
print("\n🔷 3D 向量计算:")

-- 两个 3D 向量
local v1 = {1, 2, 3}
local v2 = {4, 5, 6}

print(string.format("  向量 A: (%d, %d, %d)", v1[1], v1[2], v1[3]))
print(string.format("  向量 B: (%d, %d, %d)", v2[1], v2[2], v2[3]))

-- 点积
local dot = MathUtils.dot_product(v1, v2)
print(string.format("  点积 A·B: %d", dot))

-- 向量长度
local len1 = MathUtils.vector_length(v1)
local len2 = MathUtils.vector_length(v2)
print(string.format("  |A| = %.2f", len1))
print(string.format("  |B| = %.2f", len2))

-- 夹角 (使用点积公式：A·B = |A||B|cos(θ))
local cos_theta = dot / (len1 * len2)
local angle = MathUtils.acos_deg(cos_theta)
print(string.format("  夹角：%.2f°", angle))

-- 单位向量
local unit1 = MathUtils.normalize(v1)
local unit2 = MathUtils.normalize(v2)
print(string.format("  A 的单位向量：(%.3f, %.3f, %.3f)", unit1[1], unit1[2], unit1[3]))

-- 距离
local dist = MathUtils.distance(v1, v2)
print(string.format("  A 到 B 的距离：%.2f", dist))

-------------------------------------------------------------------------------
-- 3. 数据分析示例
-------------------------------------------------------------------------------
print("\n📈 数据分析示例:")

-- 模拟销售数据
local monthly_sales = {
    125000, 138000, 142000, 156000, 168000, 175000,
    182000, 195000, 188000, 205000, 218000, 235000
}

print("  📊 年度销售分析:")
print(string.format("     月平均销售额：$%s", MathUtils.format_thousands(MathUtils.average(monthly_sales))))
print(string.format("     最高月份：$%s", MathUtils.format_thousands(MathUtils.max(monthly_sales))))
print(string.format("     最低月份：$%s", MathUtils.format_thousands(MathUtils.min(monthly_sales))))
print(string.format("     波动范围：$%s", MathUtils.format_thousands(MathUtils.range(monthly_sales))))
print(string.format("     标准差：$%s (反映波动程度)", MathUtils.format_thousands(MathUtils.stddev(monthly_sales), 0)))

-- 计算同比增长
local q1_avg = MathUtils.average({monthly_sales[1], monthly_sales[2], monthly_sales[3]})
local q4_avg = MathUtils.average({monthly_sales[10], monthly_sales[11], monthly_sales[12]})
local growth = MathUtils.growth_rate(q1_avg, q4_avg)
print(string.format("     Q1→Q4 增长：%.1f%%", growth))

-------------------------------------------------------------------------------
-- 4. 数论应用 - RSA 基础
-------------------------------------------------------------------------------
print("\n🔐 数论应用 (RSA 基础演示):")

-- 选择两个质数
local p = MathUtils.next_prime(100)
local q = MathUtils.next_prime(200)
print(string.format("  选择质数 p = %d, q = %d", p, q))

-- 计算 n 和 φ(n)
local n = p * q
local phi = (p - 1) * (q - 1)
print(string.format("  n = p × q = %d", n))
print(string.format("  φ(n) = (p-1)(q-1) = %d", phi))

-- 找 e (与 φ(n) 互质)
local e = 65537  -- 常用的 RSA 指数
if MathUtils.gcd(e, phi) ~= 1 then
    e = MathUtils.next_prime(1000)
end
print(string.format("  公钥指数 e = %d", e))

-- 分解质因数演示
local num = 84
local factors = MathUtils.prime_factorization(num)
local factor_str = ""
for prime, exp in pairs(factors) do
    if exp > 1 then
        factor_str = factor_str .. string.format("%d^%d × ", prime, exp)
    else
        factor_str = factor_str .. string.format("%d × ", prime)
    end
end
factor_str = factor_str:sub(1, -4)  -- 移除最后的 " × "
print(string.format("  %d 的质因数分解：%s", num, factor_str))

-------------------------------------------------------------------------------
-- 5. 斐波那契与黄金比例
-------------------------------------------------------------------------------
print("\n🌀 斐波那契与黄金比例:")

local fibs = MathUtils.fibonacci(15)
print("  斐波那契数列:")
print("    " .. table.concat(fibs, ", "))

print("\n  相邻项比值 (趋近黄金比例 φ):")
for i = 2, math.min(10, #fibs) do
    if fibs[i-1] > 0 then
        local ratio = fibs[i] / fibs[i-1]
        local diff = math.abs(ratio - MathUtils.PHI)
        print(string.format("    F(%d)/F(%d) = %.6f (与 φ 相差：%.6f)", i, i-1, ratio, diff))
    end
end
print(string.format("  黄金比例 φ = %.10f", MathUtils.PHI))

-------------------------------------------------------------------------------
-- 6. 矩阵运算 - 线性方程组
-------------------------------------------------------------------------------
print("\n🔢 矩阵运算:")

-- 创建矩阵
local a = {
    {1, 2, 3},
    {4, 5, 6},
    {7, 8, 9}
}

print("  矩阵 A:")
for i, row in ipairs(a) do
    print("    [" .. table.concat(row, ", ") .. "]")
end

-- 转置
local at = MathUtils.transpose(a)
print("\n  A 的转置 Aᵀ:")
for i, row in ipairs(at) do
    print("    [" .. table.concat(row, ", ") .. "]")
end

-- 单位矩阵
local identity = MathUtils.identity(3)
print("\n  3×3 单位矩阵 I:")
for i, row in ipairs(identity) do
    print("    [" .. table.concat(row, ", ") .. "]")
end

-------------------------------------------------------------------------------
-- 7. 概率与组合
-------------------------------------------------------------------------------
print("\n🎲 概率与组合:")

-- 扑克牌概率
local deck_size = 52
local hand_size = 5
local total_hands = MathUtils.combinations(deck_size, hand_size)
print(string.format("  从 52 张牌中选 5 张的组合数：%s", MathUtils.format_thousands(total_hands)))

-- 同花顺概率 (有 40 种同花顺)
local straight_flush = 40
local prob = MathUtils.percentage(straight_flush, total_hands)
print(string.format("  同花顺概率：%.6f%% (约 1/%.0f)", prob, 100/prob))

-- 排列数 - 密码强度
local charset_size = 62  -- 26 大写 + 26 小写 + 10 数字
local password_len = 8
local possible_passwords = MathUtils.power(charset_size, password_len)
print(string.format("\n  8 位字母数字密码的可能性：%s 种", MathUtils.format_scientific(possible_passwords, 2)))

-------------------------------------------------------------------------------
-- 8. 实用工具
-------------------------------------------------------------------------------
print("\n🛠️ 实用工具:")

-- 检查完全数
local function is_perfect_number(n)
    local divs = MathUtils.divisors(n)
    local sum = 0
    for _, d in ipairs(divs) do
        if d < n then
            sum = sum + d
        end
    end
    return sum == n
end

print("  1000 以内的完全数:")
for i = 1, 1000 do
    if is_perfect_number(i) then
        local divs = MathUtils.divisors(i)
        table.remove(divs)  -- 移除自身
        print(string.format("    %d = %s", i, table.concat(divs, " + ")))
    end
end

-- 阿姆斯特朗数 (水仙花数)
print("\n  三位水仙花数 (各位立方和等于自身):")
for i = 100, 999 do
    local sum = 0
    local temp = i
    while temp > 0 do
        local digit = temp % 10
        sum = sum + MathUtils.power(digit, 3)
        temp = math.floor(temp / 10)
    end
    if sum == i then
        print(string.format("    %d = %d³ + %d³ + %d³", 
            i, math.floor(i/100), math.floor((i%100)/10), i%10))
    end
end

-------------------------------------------------------------------------------
print("\n" .. string.rep("=", 50))
print("✅ 高级示例完成!")

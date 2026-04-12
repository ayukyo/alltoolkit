#!/usr/bin/env lua
---
-- Math Utilities Test Suite
-- 数学工具函数测试套件
--
-- 覆盖场景:
-- - 基础数学工具 (is_number, is_integer, safe_divide, round, clamp, lerp)
-- - 统计函数 (sum, average, median, mode, variance, stddev, min, max, range)
-- - 数论函数 (gcd, lcm, is_prime, factorial, combinations, permutations, divisors)
-- - 三角函数扩展 (deg_to_rad, sin_deg, cos_deg, tan_deg)
-- - 数值格式化 (format_thousands, format_bytes, format_currency)
-- - 随机数工具 (random_int, random_choice, shuffle, uuid)
-- - 向量操作 (vector_add, dot_product, normalize, distance)
-- - 序列生成 (range, fibonacci)
-- - 矩阵操作 (zeros, identity, transpose, matrix_multiply)
-- - 特殊函数 (log, sqrt, cbrt, power, sign)
--
-- Author: AllToolkit
-- Version: 1.0.0

local path = arg and arg[0] and arg[0]:match("(.*/)") or ""
local mod_path = path .. "mod.lua"

-- 加载模块
local MathUtils = dofile(mod_path)

-- 测试统计
local tests_run = 0
local tests_passed = 0
local tests_failed = 0
local failures = {}

--- 断言函数
local function assert_eq(actual, expected, message)
    tests_run = tests_run + 1
    if actual == expected then
        tests_passed = tests_passed + 1
        print("  ✓ " .. (message or tostring(expected)))
        return true
    else
        tests_failed = tests_failed + 1
        local msg = message or string.format("Expected %s, got %s", tostring(expected), tostring(actual))
        table.insert(failures, msg)
        print("  ❌ FAIL: " .. msg)
        return false
    end
end

--- 断言真值
local function assert_true(condition, message)
    tests_run = tests_run + 1
    if condition then
        tests_passed = tests_passed + 1
        print("  ✓ " .. (message or "true"))
        return true
    else
        tests_failed = tests_failed + 1
        local msg = message or "Expected true"
        table.insert(failures, msg)
        print("  ❌ FAIL: " .. msg)
        return false
    end
end

--- 断言假值
local function assert_false(condition, message)
    tests_run = tests_run + 1
    if not condition then
        tests_passed = tests_passed + 1
        print("  ✓ " .. (message or "false"))
        return true
    else
        tests_failed = tests_failed + 1
        local msg = message or "Expected false"
        table.insert(failures, msg)
        print("  ❌ FAIL: " .. msg)
        return false
    end
end

--- 断言近似相等（浮点数）
local function assert_approx(actual, expected, epsilon, message)
    epsilon = epsilon or 1e-6
    tests_run = tests_run + 1
    if math.abs(actual - expected) < epsilon then
        tests_passed = tests_passed + 1
        print("  ✓ " .. (message or string.format("%.6f ≈ %.6f", actual, expected)))
        return true
    else
        tests_failed = tests_failed + 1
        local msg = message or string.format("Expected ~%.6f, got %.6f", expected, actual)
        table.insert(failures, msg)
        print("  ❌ FAIL: " .. msg)
        return false
    end
end

--- 打印测试组标题
local function test_group(name)
    print("\n" .. string.rep("=", 60))
    print("📊 " .. name)
    print(string.rep("=", 60))
end

-------------------------------------------------------------------------------
-- 基础数学工具测试
-------------------------------------------------------------------------------

local function test_is_number()
    test_group("is_number / is_integer")
    assert_true(MathUtils.is_number(42), "42 is number")
    assert_true(MathUtils.is_number(3.14), "3.14 is number")
    assert_true(MathUtils.is_number(-100), "-100 is number")
    assert_false(MathUtils.is_number("42"), "string is not number")
    assert_false(MathUtils.is_number(nil), "nil is not number")
    assert_false(MathUtils.is_number({}), "table is not number")
    
    assert_true(MathUtils.is_integer(42), "42 is integer")
    assert_true(MathUtils.is_integer(0), "0 is integer")
    assert_true(MathUtils.is_integer(-5), "-5 is integer")
    assert_false(MathUtils.is_integer(3.14), "3.14 is not integer")
    assert_false(MathUtils.is_integer("42"), "string is not integer")
end

local function test_safe_divide()
    test_group("safe_divide / percentage / growth_rate")
    assert_eq(MathUtils.safe_divide(10, 2), 5, "10/2 = 5")
    assert_eq(MathUtils.safe_divide(7, 2), 3.5, "7/2 = 3.5")
    assert_eq(MathUtils.safe_divide(10, 0, -1), -1, "divide by zero returns default")
    assert_eq(MathUtils.safe_divide(10, 0), 0, "divide by zero returns 0")
    
    assert_approx(MathUtils.percentage(25, 100), 25, 1e-6, "25/100 = 25%")
    assert_approx(MathUtils.percentage(50, 200), 25, 1e-6, "50/200 = 25%")
    assert_eq(MathUtils.percentage(0, 0), 0, "0/0 = 0%")
    
    assert_approx(MathUtils.growth_rate(100, 150), 50, 1e-6, "100→150 = 50% growth")
    assert_approx(MathUtils.growth_rate(100, 50), -50, 1e-6, "100→50 = -50% growth")
end

local function test_round()
    test_group("round / floor_decimal / ceil_decimal / clamp / lerp")
    assert_eq(MathUtils.round(3.14159, 2), 3.14, "round to 2 decimals")
    assert_eq(MathUtils.round(3.145, 2), 3.15, "round 3.145 to 2 decimals")
    assert_eq(MathUtils.round(1234, -2), 1200, "round to hundreds")
    assert_eq(MathUtils.round(3.7), 4, "round to integer")
    
    assert_eq(MathUtils.floor_decimal(3.999, 2), 3.99, "floor to 2 decimals")
    assert_eq(MathUtils.ceil_decimal(3.001, 2), 3.01, "ceil to 2 decimals")
    
    assert_eq(MathUtils.clamp(5, 0, 10), 5, "5 in [0,10] = 5")
    assert_eq(MathUtils.clamp(-5, 0, 10), 0, "-5 in [0,10] = 0")
    assert_eq(MathUtils.clamp(15, 0, 10), 10, "15 in [0,10] = 10")
    
    assert_approx(MathUtils.lerp(0, 100, 0.5), 50, 1e-6, "lerp(0,100,0.5) = 50")
    assert_approx(MathUtils.lerp(10, 20, 0.25), 12.5, 1e-6, "lerp(10,20,0.25) = 12.5")
end

-------------------------------------------------------------------------------
-- 统计函数测试
-------------------------------------------------------------------------------

local function test_statistics()
    test_group("Statistics Functions")
    
    local nums = {1, 2, 3, 4, 5}
    assert_eq(MathUtils.sum(nums), 15, "sum([1,2,3,4,5]) = 15")
    assert_approx(MathUtils.average(nums), 3, 1e-6, "average([1,2,3,4,5]) = 3")
    assert_eq(MathUtils.median(nums), 3, "median([1,2,3,4,5]) = 3")
    assert_eq(MathUtils.median({1, 2, 3, 4}), 2.5, "median([1,2,3,4]) = 2.5")
    assert_eq(MathUtils.min(nums), 1, "min([1,2,3,4,5]) = 1")
    assert_eq(MathUtils.max(nums), 5, "max([1,2,3,4,5]) = 5")
    assert_eq(MathUtils.range(nums), 4, "range([1,2,3,4,5]) = 4")
    
    local with_mode = {1, 2, 2, 3, 4}
    assert_eq(MathUtils.mode(with_mode), 2, "mode([1,2,2,3,4]) = 2")
    
    -- 方差和标准差
    local variance_nums = {2, 4, 4, 4, 5, 5, 7, 9}
    assert_approx(MathUtils.variance(variance_nums), 4, 1e-6, "variance test")
    assert_approx(MathUtils.stddev(variance_nums), 2, 1e-6, "stddev test")
end

-------------------------------------------------------------------------------
-- 数论函数测试
-------------------------------------------------------------------------------

local function test_number_theory()
    test_group("Number Theory Functions")
    
    assert_eq(MathUtils.gcd(48, 18), 6, "gcd(48, 18) = 6")
    assert_eq(MathUtils.gcd(17, 13), 1, "gcd(17, 13) = 1")
    assert_eq(MathUtils.lcm(4, 6), 12, "lcm(4, 6) = 12")
    assert_eq(MathUtils.lcm(3, 5), 15, "lcm(3, 5) = 15")
    
    assert_true(MathUtils.is_prime(2), "2 is prime")
    assert_true(MathUtils.is_prime(3), "3 is prime")
    assert_true(MathUtils.is_prime(17), "17 is prime")
    assert_true(MathUtils.is_prime(97), "97 is prime")
    assert_false(MathUtils.is_prime(1), "1 is not prime")
    assert_false(MathUtils.is_prime(4), "4 is not prime")
    assert_false(MathUtils.is_prime(100), "100 is not prime")
    
    assert_eq(MathUtils.factorial(0), 1, "0! = 1")
    assert_eq(MathUtils.factorial(1), 1, "1! = 1")
    assert_eq(MathUtils.factorial(5), 120, "5! = 120")
    assert_eq(MathUtils.factorial(10), 3628800, "10! = 3628800")
    
    assert_eq(MathUtils.combinations(5, 2), 10, "C(5,2) = 10")
    assert_eq(MathUtils.combinations(10, 3), 120, "C(10,3) = 120")
    assert_eq(MathUtils.permutations(5, 2), 20, "P(5,2) = 20")
    assert_eq(MathUtils.permutations(4, 3), 24, "P(4,3) = 24")
    
    -- 因数
    local divs_12 = MathUtils.divisors(12)
    assert_eq(#divs_12, 6, "12 has 6 divisors")
    assert_eq(table.concat(divs_12, ","), "1,2,3,4,6,12", "divisors of 12")
    
    -- 质因数分解
    local factors_60 = MathUtils.prime_factorization(60)
    assert_eq(factors_60[2], 2, "60 = 2^2 * ...")
    assert_eq(factors_60[3], 1, "60 = ... * 3^1 * ...")
    assert_eq(factors_60[5], 1, "60 = ... * 5^1")
end

-------------------------------------------------------------------------------
-- 三角函数测试
-------------------------------------------------------------------------------

local function test_trig()
    test_group("Trigonometric Functions (Degrees)")
    
    assert_eq(MathUtils.deg_to_rad(180), math.pi, "180° = π rad")
    assert_eq(MathUtils.deg_to_rad(90), math.pi / 2, "90° = π/2 rad")
    assert_eq(MathUtils.rad_to_deg(math.pi), 180, "π rad = 180°")
    
    assert_approx(MathUtils.sin_deg(0), 0, 1e-6, "sin(0°) = 0")
    assert_approx(MathUtils.sin_deg(30), 0.5, 1e-6, "sin(30°) = 0.5")
    assert_approx(MathUtils.sin_deg(90), 1, 1e-6, "sin(90°) = 1")
    
    assert_approx(MathUtils.cos_deg(0), 1, 1e-6, "cos(0°) = 1")
    assert_approx(MathUtils.cos_deg(60), 0.5, 1e-6, "cos(60°) = 0.5")
    assert_approx(MathUtils.cos_deg(90), 0, 1e-6, "cos(90°) = 0")
    
    assert_approx(MathUtils.tan_deg(45), 1, 1e-6, "tan(45°) = 1")
end

-------------------------------------------------------------------------------
-- 格式化函数测试
-------------------------------------------------------------------------------

local function test_formatting()
    test_group("Formatting Functions")
    
    assert_eq(MathUtils.format_thousands(1234567), "1,234,567", "format thousands")
    assert_eq(MathUtils.format_thousands(1000, "."), "1.000", "format with dot separator")
    
    assert_eq(MathUtils.format_bytes(1024), "1.00 KB", "format 1024 bytes")
    assert_eq(MathUtils.format_bytes(1048576), "1.00 MB", "format 1 MB")
    assert_eq(MathUtils.format_bytes(1073741824), "1.00 GB", "format 1 GB")
    
    assert_eq(MathUtils.format_currency(1234.56, "$"), "$1,234.56", "format currency USD")
    assert_eq(MathUtils.format_currency(-99.99, "¥"), "-¥99.99", "format negative currency")
end

-------------------------------------------------------------------------------
-- 随机数测试
-------------------------------------------------------------------------------

local function test_random()
    test_group("Random Functions")
    
    local rand_int = MathUtils.random_int(1, 10)
    assert_true(rand_int >= 1 and rand_int <= 10, "random_int in range")
    
    local rand_float = MathUtils.random_float(0, 1)
    assert_true(rand_float >= 0 and rand_float <= 1, "random_float in range")
    
    local arr = {1, 2, 3, 4, 5}
    local choice = MathUtils.random_choice(arr)
    assert_true(choice >= 1 and choice <= 5, "random_choice from array")
    
    local shuffled = MathUtils.shuffle(arr)
    assert_eq(#shuffled, 5, "shuffle preserves length")
    
    local uid = MathUtils.uuid()
    assert_eq(#uid, 36, "UUID length is 36")
    -- 验证 UUID v4 格式：8-4-4-4-12，第 3 段以 4 开头
    assert_true(uid:match("^[0-9a-f]+-[0-9a-f]+-4[0-9a-f]+-[0-9a-f]+-[0-9a-f]+$"), "UUID format")
end

-------------------------------------------------------------------------------
-- 向量操作测试
-------------------------------------------------------------------------------

local function test_vectors()
    test_group("Vector Operations")
    
    local v1 = {1, 2, 3}
    local v2 = {4, 5, 6}
    
    local sum_v = MathUtils.vector_add(v1, v2)
    assert_eq(sum_v[1], 5, "vector_add x")
    assert_eq(sum_v[2], 7, "vector_add y")
    assert_eq(sum_v[3], 9, "vector_add z")
    
    assert_eq(MathUtils.dot_product(v1, v2), 32, "dot_product([1,2,3], [4,5,6]) = 32")
    assert_approx(MathUtils.vector_length({3, 4}), 5, 1e-6, "vector_length([3,4]) = 5")
    
    local unit = MathUtils.normalize({3, 4})
    assert_approx(unit[1], 0.6, 1e-6, "normalize x")
    assert_approx(unit[2], 0.8, 1e-6, "normalize y")
    
    assert_approx(MathUtils.distance({0, 0}, {3, 4}), 5, 1e-6, "distance([0,0], [3,4]) = 5")
end

-------------------------------------------------------------------------------
-- 序列生成测试
-------------------------------------------------------------------------------

local function test_sequences()
    test_group("Sequence Generation")
    
    local range_5 = MathUtils.range_seq(5)
    assert_eq(#range_5, 5, "range_seq(5) has 5 elements")
    assert_eq(range_5[1], 0, "range_seq starts at 0")
    assert_eq(range_5[5], 4, "range_seq ends at 4")
    
    local range_step = MathUtils.range_seq(0, 10, 2)
    assert_eq(#range_step, 5, "range_seq(0,10,2) has 5 elements")
    
    local fibs = MathUtils.fibonacci(10)
    assert_eq(#fibs, 10, "fibonacci(10) has 10 elements")
    assert_eq(table.concat(fibs, ","), "0,1,1,2,3,5,8,13,21,34", "fibonacci sequence")
    
    assert_eq(MathUtils.fib(10), 55, "fib(10) = 55")
    assert_eq(MathUtils.fib(20), 6765, "fib(20) = 6765")
end

-------------------------------------------------------------------------------
-- 矩阵操作测试
-------------------------------------------------------------------------------

local function test_matrices()
    test_group("Matrix Operations")
    
    local zeros = MathUtils.zeros(2, 3)
    assert_eq(#zeros, 2, "zeros rows")
    assert_eq(#zeros[1], 3, "zeros cols")
    assert_eq(zeros[1][1], 0, "zeros value")
    
    local identity = MathUtils.identity(3)
    assert_eq(identity[1][1], 1, "identity[1][1] = 1")
    assert_eq(identity[2][2], 1, "identity[2][2] = 1")
    assert_eq(identity[1][2], 0, "identity[1][2] = 0")
    
    local matrix = {{1, 2}, {3, 4}}
    local transposed = MathUtils.transpose(matrix)
    assert_eq(transposed[1][1], 1, "transpose[1][1]")
    assert_eq(transposed[1][2], 3, "transpose[1][2]")
    assert_eq(transposed[2][1], 2, "transpose[2][1]")
    assert_eq(transposed[2][2], 4, "transpose[2][2]")
    
    -- 矩阵乘法
    local a = {{1, 2}, {3, 4}}
    local b = {{5, 6}, {7, 8}}
    local result = MathUtils.matrix_multiply(a, b)
    assert_eq(result[1][1], 19, "matrix_multiply[1][1] = 1*5+2*7 = 19")
    assert_eq(result[1][2], 22, "matrix_multiply[1][2] = 1*6+2*8 = 22")
    assert_eq(result[2][1], 43, "matrix_multiply[2][1] = 3*5+4*7 = 43")
    assert_eq(result[2][2], 50, "matrix_multiply[2][2] = 3*6+4*8 = 50")
end

-------------------------------------------------------------------------------
-- 特殊函数测试
-------------------------------------------------------------------------------

local function test_special_functions()
    test_group("Special Functions")
    
    assert_approx(MathUtils.ln(MathUtils.E), 1, 1e-6, "ln(e) = 1")
    assert_eq(MathUtils.log10(100), 2, "log10(100) = 2")
    assert_eq(MathUtils.log2(8), 3, "log2(8) = 3")
    
    assert_eq(MathUtils.sqrt(16), 4, "sqrt(16) = 4")
    assert_approx(MathUtils.cbrt(27), 3, 1e-6, "cbrt(27) = 3")
    assert_eq(MathUtils.power(2, 10), 1024, "2^10 = 1024")
    
    assert_eq(MathUtils.abs(-5), 5, "abs(-5) = 5")
    assert_eq(MathUtils.sign(-10), -1, "sign(-10) = -1")
    assert_eq(MathUtils.sign(0), 0, "sign(0) = 0")
    assert_eq(MathUtils.sign(42), 1, "sign(42) = 1")
    
    assert_true(MathUtils.is_even(4), "4 is even")
    assert_true(MathUtils.is_odd(7), "7 is odd")
    
    assert_true(MathUtils.almost_equal(0.1 + 0.2, 0.3), "0.1+0.2 ≈ 0.3")
    
    assert_eq(MathUtils.digit_count(12345), 5, "digit_count(12345) = 5")
    assert_eq(MathUtils.reverse_number(12345), 54321, "reverse_number(12345) = 54321")
    assert_eq(MathUtils.digit_sum(12345), 15, "digit_sum(12345) = 15")
    
    assert_true(MathUtils.is_perfect_square(16), "16 is perfect square")
    assert_true(MathUtils.is_perfect_square(100), "100 is perfect square")
    assert_false(MathUtils.is_perfect_square(15), "15 is not perfect square")
    
    assert_true(MathUtils.is_perfect_cube(27), "27 is perfect cube")
    assert_true(MathUtils.is_perfect_cube(125), "125 is perfect cube")
    assert_false(MathUtils.is_perfect_cube(28), "28 is not perfect cube")
end

-------------------------------------------------------------------------------
-- 主测试运行器
-------------------------------------------------------------------------------

local function run_all_tests()
    print(string.rep("=", 60))
    print("🧮 AllToolkit Lua Math Utils Test Suite")
    print("Version: " .. MathUtils.VERSION)
    print(string.rep("=", 60))
    
    test_is_number()
    test_safe_divide()
    test_round()
    test_statistics()
    test_number_theory()
    test_trig()
    test_formatting()
    test_random()
    test_vectors()
    test_sequences()
    test_matrices()
    test_special_functions()
    
    -- 打印总结
    print("\n" .. string.rep("=", 60))
    print("📊 Test Summary")
    print(string.rep("=", 60))
    print(string.format("Total:  %d", tests_run))
    print(string.format("Passed: %d ✓", tests_passed))
    print(string.format("Failed: %d ❌", tests_failed))
    print(string.format("Rate:   %.1f%%", (tests_passed / tests_run) * 100))
    
    if tests_failed > 0 then
        print("\n❌ Failures:")
        for _, f in ipairs(failures) do
            print("  - " .. f)
        end
        os.exit(1)
    else
        print("\n✅ All tests passed!")
        os.exit(0)
    end
end

-- 运行测试
run_all_tests()

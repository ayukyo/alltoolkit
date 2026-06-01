---
-- Biorhythm Utils Tests
-- 生物节律工具测试
--
-- @author AllToolkit
-- @copyright MIT License

local BiorhythmUtils = require("mod")

-- 测试计数器
local total_tests = 0
local passed_tests = 0
local failed_tests = 0

--- 测试断言
local function assert(condition, message)
    total_tests = total_tests + 1
    if condition then
        passed_tests = passed_tests + 1
        print("  ✅ PASS: " .. (message or ""))
    else
        failed_tests = failed_tests + 1
        print("  ❌ FAIL: " .. (message or ""))
    end
end

--- 测试断言相等
local function assert_equal(actual, expected, message)
    total_tests = total_tests + 1
    if actual == expected then
        passed_tests = passed_tests + 1
        print("  ✅ PASS: " .. (message or ""))
    else
        failed_tests = failed_tests + 1
        print("  ❌ FAIL: " .. (message or (" - expected " .. tostring(expected) .. ", got " .. tostring(actual))))
    end
end

--- 测试断言近似相等（浮点数）
local function assert_almost_equal(actual, expected, tolerance, message)
    total_tests = total_tests + 1
    local diff = math.abs(actual - expected)
    if diff <= tolerance then
        passed_tests = passed_tests + 1
        print("  ✅ PASS: " .. (message or ""))
    else
        failed_tests = failed_tests + 1
        print("  ❌ FAIL: " .. (message or (" - expected ~" .. tostring(expected) .. ", got " .. tostring(actual))))
    end
end

--- 测试断言 nil
local function assert_nil(actual, message)
    total_tests = total_tests + 1
    if actual == nil then
        passed_tests = passed_tests + 1
        print("  ✅ PASS: " .. (message or ""))
    else
        failed_tests = failed_tests + 1
        print("  ❌ FAIL: " .. (message or (" - expected nil, got " .. tostring(actual))))
    end
end

--- 测试断言 not nil
local function assert_not_nil(actual, message)
    total_tests = total_tests + 1
    if actual ~= nil then
        passed_tests = passed_tests + 1
        print("  ✅ PASS: " .. (message or ""))
    else
        failed_tests = failed_tests + 1
        print("  ❌ FAIL: " .. (message or " - expected not nil"))
    end
end

print("========================================")
print("Biorhythm Utils Test Suite")
print("========================================")
print("")

-- ============================================================
-- 测试：版本和常量
-- ============================================================
print("【测试：版本和常量】")
assert_not_nil(BiorhythmUtils.VERSION, "VERSION should be defined")
assert_not_nil(BiorhythmUtils.CycleType, "CycleType should be defined")
assert_not_nil(BiorhythmUtils.CycleType.PHYSICAL, "CycleType.PHYSICAL should be 'physical'")
print("")

-- ============================================================
-- 测试：核心计算函数
-- ============================================================
print("【测试：核心计算函数】")

-- 测试 days_alive 函数
local days = BiorhythmUtils.days_alive(1990, 6, 15)
-- 1990-06-15 到今天应该大于 13000 天
assert(days > 13000, "days_alive should be > 13000 for birth 1990-06-15")

-- 测试 today 函数
local result = BiorhythmUtils.today(1990, 6, 15)
assert_not_nil(result, "today() should return a result")
assert_not_nil(result.birth_date, "birth_date should be present")
assert_not_nil(result.days_alive, "days_alive should be present")
assert(result.days_alive > 0, "days_alive should be positive")
print("")

-- ============================================================
-- 测试：calculate 函数
-- ============================================================
print("【测试：calculate 函数】")

-- 基本计算
local bio = BiorhythmUtils.calculate(1990, 6, 15, 2024, 1, 1)
assert_not_nil(bio, "calculate should return a result")
assert_equal(bio.birth_date, "1990-06-15", "birth_date should be formatted correctly")
assert_equal(bio.target_date, "2024-01-01", "target_date should be formatted correctly")
assert(bio.days_alive > 0, "days_alive should be positive")

-- 主要周期检查
assert_not_nil(bio.primary_cycles, "primary_cycles should exist")
assert_not_nil(bio.primary_cycles.physical, "physical cycle should exist")
assert_not_nil(bio.primary_cycles.emotional, "emotional cycle should exist")
assert_not_nil(bio.primary_cycles.intellectual, "intellectual cycle should exist")

-- 周期值范围检查 (-100 到 100)
local physical_value = bio.primary_cycles.physical.value
assert(physical_value >= -100 and physical_value <= 100, "physical value should be between -100 and 100")

local emotional_value = bio.primary_cycles.emotional.value
assert(emotional_value >= -100 and emotional_value <= 100, "emotional value should be between -100 and 100")

local intellectual_value = bio.primary_cycles.intellectual.value
assert(intellectual_value >= -100 and intellectual_value <= 100, "intellectual value should be between -100 and 100")

-- 综合能量检查
assert(bio.overall_energy >= -100 and bio.overall_energy <= 100, "overall_energy should be between -100 and 100")

-- 次要周期检查
local bio_with_secondary = BiorhythmUtils.calculate(1990, 6, 15, 2024, 1, 1, true)
assert_not_nil(bio_with_secondary.secondary_cycles, "secondary_cycles should exist when include_secondary=true")
assert_not_nil(bio_with_secondary.secondary_cycles.intuitive, "intuitive cycle should exist")
assert_not_nil(bio_with_secondary.secondary_cycles.aesthetic, "aesthetic cycle should exist")
print("")

-- ============================================================
-- 测试：周期相位计算
-- ============================================================
print("【测试：周期相位计算】")

-- 出生日（days=0）各周期值应为 0
local birth_result = BiorhythmUtils.calculate(1990, 1, 1, 1990, 1, 1)
assert_almost_equal(birth_result.primary_cycles.physical.value, 0, 0.01, "physical should be 0 at birth")
assert_almost_equal(birth_result.primary_cycles.emotional.value, 0, 0.01, "emotional should be 0 at birth")
assert_almost_equal(birth_result.primary_cycles.intellectual.value, 0, 0.01, "intellectual should be 0 at birth")

-- 23天后（一个体力周期），体力值应回到 0 附近
local physical_23 = BiorhythmUtils.calculate(1990, 1, 1, 1990, 1, 24)
assert_almost_equal(physical_23.primary_cycles.physical.value, 0, 0.01, "physical should be ~0 after 23 days")

-- 6天后（约1/4体力周期），体力值应接近 100
local physical_6 = BiorhythmUtils.calculate(1990, 1, 1, 1990, 1, 7)
assert_almost_equal(physical_6.primary_cycles.physical.value, 100, 1, "physical should be ~100 after 6 days")
print("")

-- ============================================================
-- 测试：find_critical_days 函数
-- ============================================================
print("【测试：find_critical_days 函数】")

local critical = BiorhythmUtils.find_critical_days(1990, 6, 15)
assert_not_nil(critical, "find_critical_days should return a result")
assert(#critical > 0, "should find at least some critical days in 30 days")

-- 检查返回结构
local first_critical = critical[1]
assert_not_nil(first_critical.date_offset, "critical day should have date_offset")
assert_not_nil(first_critical.cycle_type, "critical day should have cycle_type")
assert_not_nil(first_critical.direction, "critical day should have direction")
assert(first_critical.direction == "up" or first_critical.direction == "down", "direction should be 'up' or 'down'")

-- 验证排序
local sorted = true
for i = 2, #critical do
    if critical[i].date_offset < critical[i-1].date_offset then
        sorted = false
        break
    end
end
assert(sorted, "critical days should be sorted by date_offset")

-- 自定义天数
local critical_10 = BiorhythmUtils.find_critical_days(1990, 6, 15, nil, nil, nil, 10)
assert(#critical_10 <= 10, "should return at most 10 critical days when days=10")
print("")

-- ============================================================
-- 测试：find_peak_days 函数
-- ============================================================
print("【测试：find_peak_days 函数】")

local peaks = BiorhythmUtils.find_peak_days(1990, 6, 15)
assert_not_nil(peaks, "find_peak_days should return a result")
assert(#peaks > 0, "should find at least some peak days in 30 days")

-- 检查返回结构
local first_peak = peaks[1]
assert_not_nil(first_peak.date_offset, "peak day should have date_offset")
assert_not_nil(first_peak.cycle_type, "peak day should have cycle_type")
assert_not_nil(first_peak.is_peak, "peak day should have is_peak field")
assert(first_peak.is_peak == true or first_peak.is_peak == false, "is_peak should be boolean")

-- 验证排序
local peaks_sorted = true
for i = 2, #peaks do
    if peaks[i].date_offset < peaks[i-1].date_offset then
        peaks_sorted = false
        break
    end
end
assert(peaks_sorted, "peak days should be sorted by date_offset")
print("")

-- ============================================================
-- 测试：generate_chart 函数
-- ============================================================
print("【测试：generate_chart 函数】")

local chart = BiorhythmUtils.generate_chart(1990, 6, 15)
assert_not_nil(chart, "generate_chart should return a string")
assert(#chart > 0, "chart should not be empty")
assert(string.find(chart, "生物节律图表"), "chart should contain title")
assert(string.find(chart, "P=体力"), "chart should contain legend for physical")
assert(string.find(chart, "E=情绪"), "chart should contain legend for emotional")
assert(string.find(chart, "I=智力"), "chart should contain legend for intellectual")

-- 自定义参数
local chart_custom = BiorhythmUtils.generate_chart(1990, 6, 15, nil, nil, nil, 15, 40, 11)
assert_not_nil(chart_custom, "generate_chart with custom params should return a string")
print("")

-- ============================================================
-- 测试：compatibility 函数
-- ============================================================
print("【测试：compatibility 函数】")

local compat = BiorhythmUtils.compatibility(1990, 6, 15, 1992, 3, 20)
assert_not_nil(compat, "compatibility should return a result")
assert_not_nil(compat.physical, "physical compatibility should exist")
assert_not_nil(compat.emotional, "emotional compatibility should exist")
assert_not_nil(compat.intellectual, "intellectual compatibility should exist")
assert_not_nil(compat.overall, "overall compatibility should exist")
assert_not_nil(compat.interpretation, "interpretation should exist")

-- 契合度应该在 0-100 范围内
assert(compat.physical >= 0 and compat.physical <= 100, "physical compatibility should be 0-100")
assert(compat.emotional >= 0 and compat.emotional <= 100, "emotional compatibility should be 0-100")
assert(compat.intellectual >= 0 and compat.intellectual <= 100, "intellectual compatibility should be 0-100")
assert(compat.overall >= 0 and compat.overall <= 100, "overall compatibility should be 0-100")
print("")

-- ============================================================
-- 测试：get_zodiac 函数
-- ============================================================
print("【测试：get_zodiac 函数】")

local zodiac = BiorhythmUtils.get_zodiac(1990)
assert_not_nil(zodiac, "get_zodiac should return a result")
assert_not_nil(zodiac.animal_cn, "animal_cn should exist")
assert_not_nil(zodiac.animal_en, "animal_en should exist")
assert_not_nil(zodiac.earthly_branch, "earthly_branch should exist")
assert_not_nil(zodiac.element, "element should exist")
assert_not_nil(zodiac.description, "description should exist")

-- 1990年是马年（金马）
assert_equal(zodiac.animal_cn, "马", "1990 should be Horse")
assert_equal(zodiac.animal_en, "Horse", "animal_en should be 'Horse'")
assert_equal(zodiac.earthly_branch, "午", "earthly_branch should be '午'")
assert_equal(zodiac.element, "金", "1990 should be Metal")

-- 测试其他年份
local zodiac_2000 = BiorhythmUtils.get_zodiac(2000)
assert_equal(zodiac_2000.animal_cn, "龙", "2000 should be Dragon")

local zodiac_2024 = BiorhythmUtils.get_zodiac(2024)
assert_equal(zodiac_2024.animal_cn, "龙", "2024 should be Dragon")
print("")

-- ============================================================
-- 测试：get_daily_summary 函数
-- ============================================================
print("【测试：get_daily_summary 函数】")

local summary = BiorhythmUtils.get_daily_summary(1990, 6, 15)
assert_not_nil(summary, "get_daily_summary should return a string")
assert(#summary > 0, "summary should not be empty")
assert(string.find(summary, "生物节律日报"), "summary should contain header")
assert(string.find(summary, "体力"), "summary should mention physical")
assert(string.find(summary, "情绪"), "summary should mention emotional")
assert(string.find(summary, "智力"), "summary should mention intellectual")
print("")

-- ============================================================
-- 测试：周期状态判断
-- ============================================================
print("【测试：周期状态判断】")

-- 测试临界状态（值接近0）
local critical_bio = BiorhythmUtils.calculate(1990, 1, 1, 1990, 1, 12)
-- 第12天，体力值约为 sin(2π*12/23)*100 ≈ sin(6.28*12/23)*100 ≈ sin(3.28)*100 ≈ -12%
-- 不在临界点，测试正常状态

local normal_bio = BiorhythmUtils.calculate(1990, 1, 1, 1990, 1, 6)
-- 第6天，体力值约为 100%
-- 检查 is_peak
assert(normal_bio.primary_cycles.physical.is_peak == true or normal_bio.primary_cycles.physical.value > 90, "should detect peak around day 6")
print("")

-- ============================================================
-- 测试：边界条件
-- ============================================================
print("【测试：边界条件】")

-- 空参数应使用今日
local today_bio = BiorhythmUtils.calculate(1990, 6, 15)
local ty, tm, td = os.date("*t").year, os.date("*t").month, os.date("*t").day
local today_bio2 = BiorhythmUtils.calculate(1990, 6, 15, ty, tm, td)
-- 两次调用结果应该相近（在同一天内）
assert(math.abs(today_bio.days_alive - today_bio2.days_alive) <= 1, "today() calls should be similar")

-- 查找0天应返回空
local empty_critical = BiorhythmUtils.find_critical_days(1990, 6, 15, nil, nil, nil, 0)
assert(#empty_critical == 0, "0 days should return empty list")

local empty_peaks = BiorhythmUtils.find_peak_days(1990, 6, 15, nil, nil, nil, 0)
assert(#empty_peaks == 0, "0 days should return empty list")
print("")

-- ============================================================
-- 测试结果汇总
-- ============================================================
print("========================================")
print("Test Results")
print("========================================")
print(string.format("Total:  %d", total_tests))
print(string.format("Passed: %d", passed_tests))
print(string.format("Failed: %d", failed_tests))
print("")

if failed_tests == 0 then
    print("🎉 All tests passed!")
else
    print("⚠️  Some tests failed.")
end
print("========================================")

-- 返回测试结果
return {
    total = total_tests,
    passed = passed_tests,
    failed = failed_tests,
}

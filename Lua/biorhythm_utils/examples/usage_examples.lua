---
-- Biorhythm Utils Usage Examples
-- 生物节律工具使用示例
--
-- @author AllToolkit
-- @copyright MIT License

-- 加载模块
local BiorhythmUtils = require("mod")

print("========================================")
print("Biorhythm Utils Usage Examples")
print("========================================")
print("")

-- ============================================================
-- 示例1：基础使用 - 计算今日生物节律
-- ============================================================
print("【示例1：基础使用】")
print("计算生日 1990-06-15 的今日生物节律：")
print("")

local bio = BiorhythmUtils.today(1990, 6, 15)
print(string.format("已生活 %d 天", bio.days_alive))
print(string.format("综合能量: %.1f%%", bio.overall_energy))
print("")

for cycle, data in pairs(bio.primary_cycles) do
    local name = cycle:sub(1,1):upper()..cycle:sub(2)
    print(string.format("  %s: %+.1f%% (%s)", name, data.value, data.state))
end
print("")
print("----------------------------------------")
print("")

-- ============================================================
-- 示例2：完整报告 - 获取每日摘要
-- ============================================================
print("【示例2：完整报告】")
print("获取详细的每日生物节律报告：")
print("")

local summary = BiorhythmUtils.get_daily_summary(1990, 6, 15)
print(summary)
print("")
print("----------------------------------------")
print("")

-- ============================================================
-- 示例3：图表生成 - 生成 ASCII 图表
-- ============================================================
print("【示例3：图表生成】")
print("生成未来30天的生物节律图表：")
print("")

local chart = BiorhythmUtils.generate_chart(1990, 6, 15, nil, nil, nil, 30, 60, 13)
print(chart)
print("")
print("----------------------------------------")
print("")

-- ============================================================
-- 示例4：临界日查询 - 查找即将到来的临界日
-- ============================================================
print("【示例4：临界日查询】")
print("查找未来30天内的临界日（零点交叉日）：")
print("")

local critical = BiorhythmUtils.find_critical_days(1990, 6, 15, nil, nil, nil, 30)
for i, day in ipairs(critical) do
    local direction_str = day.direction == "up" and "上升" or "下降"
    print(string.format("  %d天后: %s - %s", day.date_offset, day.description, direction_str))
end
print("")
print("----------------------------------------")
print("")

-- ============================================================
-- 示例5：高峰日查询 - 查找即将到来的高峰日和低谷日
-- ============================================================
print("【示例5：高峰日查询】")
print("查找未来30天内的高峰日和低谷日：")
print("")

local peaks = BiorhythmUtils.find_peak_days(1990, 6, 15, nil, nil, nil, 30)
for i, day in ipairs(peaks) do
    local type_str = day.is_peak and "高峰" or "低谷"
    print(string.format("  %d天后: %s - %s", day.date_offset, type_str, day.cycle_type))
end
print("")
print("----------------------------------------")
print("")

-- ============================================================
-- 示例6：契合度分析 - 两人生物节律对比
-- ============================================================
print("【示例6：契合度分析】")
print("计算两人生物节律的契合度：")
print("")

local compat = BiorhythmUtils.compatibility(1990, 6, 15, 1992, 3, 20)
print(string.format("日期: %s", compat.date))
print("")
print(string.format("  体力契合度: %.1f%%", compat.physical))
print(string.format("  情绪契合度: %.1f%%", compat.emotional))
print(string.format("  智力契合度: %.1f%%", compat.intellectual))
print(string.format("  综合契合度: %.1f%%", compat.overall))
print("")
print("解读: " .. compat.interpretation)
print("")
print("----------------------------------------")
print("")

-- ============================================================
-- 示例7：生肖查询
-- ============================================================
print("【示例7：生肖查询】")
print("查询各年份的生肖信息：")
print("")

local years = {1990, 1992, 2000, 2008, 2020, 2024}
for _, year in ipairs(years) do
    local zodiac = BiorhythmUtils.get_zodiac(year)
    print(string.format("  %d年: %s (%s)", year, zodiac.description, zodiac.animal_en))
end
print("")
print("----------------------------------------")
print("")

-- ============================================================
-- 示例8：批量计算 - 分析日期范围
-- ============================================================
print("【示例8：批量计算】")
print("计算未来7天的生物节律变化：")
print("")

-- 使用 find_peak_days 模拟批量分析
local peaks_week = BiorhythmUtils.find_peak_days(1990, 6, 15, nil, nil, nil, 7)
if #peaks_week > 0 then
    print("本周重要日期：")
    for i, day in ipairs(peaks_week) do
        local type_str = day.is_peak and "📈高峰" or "📉低谷"
        print(string.format("  %d天后: %s - %s", day.date_offset, type_str, day.cycle_type))
    end
else
    print("本周没有高峰或低谷日")
end
print("")
print("----------------------------------------")
print("")

-- ============================================================
-- 示例9：次要周期分析
-- ============================================================
print("【示例9：次要周期分析】")
print("包含次要周期的完整生物节律分析：")
print("")

local bio_full = BiorhythmUtils.calculate(1990, 6, 15, nil, nil, nil, true)
print("主要周期：")
for cycle, data in pairs(bio_full.primary_cycles) do
    print(string.format("  %s: %+.1f%%", cycle, data.value))
end
print("")
print("次要周期：")
for cycle, data in pairs(bio_full.secondary_cycles) do
    print(string.format("  %s: %+.1f%%", cycle, data.value))
end
print("")
print("----------------------------------------")
print("")

-- ============================================================
-- 示例10：生命数字计算
-- ============================================================
print("【示例10：生命数字计算】")
print("计算出生后存活的天数（生命数字）：")
print("")

local days1 = BiorhythmUtils.days_alive(1990, 6, 15)
local days2 = BiorhythmUtils.days_alive(2000, 1, 1)
local days3 = BiorhythmUtils.days_alive(2010, 6, 15)

print(string.format("  1990-06-15 出生: %d 天", days1))
print(string.format("  2000-01-01 出生: %d 天", days2))
print(string.format("  2010-06-15 出生: %d 天", days3))
print("")
print("========================================")
print("Examples completed!")
print("========================================")

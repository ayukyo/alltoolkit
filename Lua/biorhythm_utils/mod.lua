---
-- Biorhythm Utilities Module
-- 生物节律工具函数库
--
-- 提供完整的生物节律计算和分析功能，支持体力、情绪、智力三大主要周期
-- 以及直觉、审美、意识、精神四个次要周期。
-- 仅使用 Lua 标准库，零依赖。
--
-- Features:
-- - 计算三大主要生物节律周期（体力23天、情绪28天、智力33天）
-- - 计算次要周期（直觉38天、审美43天、意识48天、精神53天）
-- - 查找临界日（零点交叉日）
-- - 查找高峰日和低谷日
-- - 生成 ASCII 生物节律图表
-- - 两人生物节律契合度分析
-- - 批量日期分析
-- - 生肖计算
--
-- @author AllToolkit
-- @version 1.0.0
-- @copyright MIT License

local BiorhythmUtils = {}
local BiorhythmUtilsMT = { __index = BiorhythmUtils }

--- 版本号
BiorhythmUtils.VERSION = "1.0.0"

--- 错误类型
BiorhythmUtils.Error = {
    InvalidPeriod = "Period must be positive",
    InvalidDate = "Invalid date: year, month, or day is out of range",
    FutureBirthDate = "Birth date cannot be in the future of target date",
    InvalidCycleType = "Invalid cycle type",
    InvalidDays = "Days must be positive",
    InvalidRange = "Start date must be before or equal to end date",
}

--- 周期类型枚举
BiorhythmUtils.CycleType = {
    PHYSICAL = "physical",
    EMOTIONAL = "emotional",
    INTELLECTUAL = "intellectual",
    INTUITIVE = "intuitive",
    AESTHETIC = "aesthetic",
    AWARENESS = "awareness",
    SPIRITUAL = "spiritual",
}

--- 主要周期配置（天数）
local PRIMARY_PERIODS = {
    physical = 23,
    emotional = 28,
    intellectual = 33,
}

--- 次要周期配置（天数）
local SECONDARY_PERIODS = {
    intuitive = 38,
    aesthetic = 43,
    awareness = 48,
    spiritual = 53,
}

--- 周期中文名称
local CYCLE_NAMES = {
    physical = "体力",
    emotional = "情绪",
    intellectual = "智力",
    intuitive = "直觉",
    aesthetic = "审美",
    awareness = "意识",
    spiritual = "精神",
}

--- 周期描述
local CYCLE_DESCRIPTIONS = {
    physical = "影响体力、耐力、精力、抵抗力",
    emotional = "影响情绪、心情、创造力、敏感度",
    intellectual = "影响思维能力、记忆力、逻辑分析",
    intuitive = "影响直觉、灵感、第六感",
    aesthetic = "影响审美、艺术感知、创造性表达",
    awareness = "影响意识水平、觉察能力、专注力",
    spiritual = "影响精神状态、内在平衡、心灵感悟",
}

-------------------------------------------------------------------------------
-- 工具函数
-------------------------------------------------------------------------------

--- 计算两个日期之间的天数差
--- @param year1 number 年份1
--- @param month1 number 月份1 (1-12)
--- @param day1 number 日期1
--- @param year2 number 年份2
--- @param month2 number 月份2 (1-12)
--- @param day2 number 日期2
--- @return number 天数差
local function days_between(year1, month1, day1, year2, month2, day2)
    -- 使用简化算法：将日期转换为天数
    -- 基于 1970-01-01 的偏移量
    local function date_to_days(year, month, day)
        local days = 0
        -- 累加年份
        for y = 1970, year - 1 do
            if (y % 4 == 0 and y % 100 ~= 0) or (y % 400 == 0) then
                days = days + 366
            else
                days = days + 365
            end
        end
        -- 累加月份
        local days_in_month_tbl = {31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31}
        if (year % 4 == 0 and year % 100 ~= 0) or (year % 400 == 0) then
            days_in_month_tbl[2] = 29
        end
        for m = 1, month - 1 do
            days = days + days_in_month_tbl[m]
        end
        -- 加上日期
        days = days + day - 1
        return days
    end
    
    return date_to_days(year2, month2, day2) - date_to_days(year1, month1, day1)
end

--- 获取当前日期（返回 year, month, day）
local function get_current_date()
    -- Lua 的 os.date 返回本地时间
    local t = os.date("*t")
    return t.year, t.month, t.day
end

--- 获取今日
local function today()
    return get_current_date()
end

-------------------------------------------------------------------------------
-- 核心计算函数
-------------------------------------------------------------------------------

--- 计算生物节律值
--- @param days number 出生后天数
--- @param period number 周期（天数）
--- @return number 生物节律值 (-100 到 100)
local function calculate_biorhythm(days, period)
    if period <= 0 then
        error(BiorhythmUtils.Error.InvalidPeriod)
    end
    -- 使用正弦函数：sin(2π * days / period) * 100
    return math.sin(2 * math.pi * days / period) * 100
end

--- 计算周期相位角（度）
--- @param days number 出生后天数
--- @param period number 周期
--- @return number 相位角 (0-360)
local function calculate_phase(days, period)
    return (days % period) / period * 360
end

--- 计算当前周期中的天数
--- @param days number 出生后天数
--- @param period number 周期
--- @return number 当前周期中的天数 (0 到 period-1)
local function calculate_days_in_cycle(days, period)
    return days % period
end

--- 获取生物节律值详情
--- @param cycle_type string 周期类型
--- @param days_alive number 出生后总天数
--- @return table 生物节律值详情
local function get_biorhythm_value(cycle_type, days_alive)
    local period
    if PRIMARY_PERIODS[cycle_type] then
        period = PRIMARY_PERIODS[cycle_type]
    elseif SECONDARY_PERIODS[cycle_type] then
        period = SECONDARY_PERIODS[cycle_type]
    else
        error(BiorhythmUtils.Error.InvalidCycleType)
    end
    
    local value = calculate_biorhythm(days_alive, period)
    local phase = calculate_phase(days_alive, period)
    local days_in_cycle = calculate_days_in_cycle(days_alive, period)
    
    -- 计算绝对值
    local abs_value = math.abs(value)
    
    -- 判断状态
    local is_critical = abs_value < 5
    local is_peak = value > 95
    local is_low = value < -95
    
    local state
    if is_critical then
        state = "critical"
    elseif is_peak then
        state = "high"
    elseif is_low then
        state = "low"
    elseif value > 0 then
        state = "normal_high"
    else
        state = "normal_low"
    end
    
    return {
        cycle_type = cycle_type,
        value = value,
        percentage = abs_value,
        phase = phase,
        days_in_cycle = days_in_cycle,
        is_critical = is_critical,
        is_peak = is_peak,
        is_low = is_low,
        state = state,
    }
end

-------------------------------------------------------------------------------
-- 主函数
-------------------------------------------------------------------------------

--- 计算所有生物节律值
--- @param birth_year number 出生年
--- @param birth_month number 出生月 (1-12)
--- @param birth_day number 出生日
--- @param target_year number 目标年（可选，默认今日）
--- @param target_month number 目标月 (1-12，可选）
--- @param target_day number 目标日（可选）
--- @param include_secondary boolean 是否包含次要周期（可选，默认 false）
--- @return table 生物节律结果
function BiorhythmUtils.calculate(birth_year, birth_month, birth_day, target_year, target_month, target_day, include_secondary)
    -- 参数处理
    if not target_year then
        target_year, target_month, target_day = get_current_date()
    end
    
    local birth_date_str = string.format("%04d-%02d-%02d", birth_year, birth_month, birth_day)
    local target_date_str = string.format("%04d-%02d-%02d", target_year, target_month, target_day)
    
    -- 检查日期有效性
    if birth_year < 1900 or birth_year > 2100 or birth_month < 1 or birth_month > 12 or birth_day < 1 or birth_day > 31 then
        error(BiorhythmUtils.Error.InvalidDate)
    end
    
    -- 计算 days_alive
    local days_alive = days_between(birth_year, birth_month, birth_day, target_year, target_month, target_day)
    
    if days_alive < 0 then
        error(BiorhythmUtils.Error.FutureBirthDate)
    end
    
    -- 计算主要周期
    local primary_cycles = {}
    for cycle_type, _ in pairs(PRIMARY_PERIODS) do
        primary_cycles[cycle_type] = get_biorhythm_value(cycle_type, days_alive)
    end
    
    -- 计算次要周期
    local secondary_cycles = {}
    if include_secondary then
        for cycle_type, _ in pairs(SECONDARY_PERIODS) do
            secondary_cycles[cycle_type] = get_biorhythm_value(cycle_type, days_alive)
        end
    end
    
    -- 计算综合能量（主要周期平均值）
    local overall_energy = 0
    local count = 0
    for _, v in pairs(primary_cycles) do
        overall_energy = overall_energy + v.value
        count = count + 1
    end
    overall_energy = overall_energy / count
    
    return {
        birth_date = birth_date_str,
        target_date = target_date_str,
        days_alive = days_alive,
        primary_cycles = primary_cycles,
        secondary_cycles = secondary_cycles,
        overall_energy = overall_energy,
    }
end

--- 查找临界日（零点交叉日）
--- @param birth_year number 出生年
--- @param birth_month number 出生月
--- @param birth_day number 出生日
--- @param start_year number 起始年（可选，默认今日）
--- @param start_month number 起始月（可选）
--- @param start_day number 起始日（可选）
--- @param days number 查询天数（可选，默认30）
--- @param cycle_types table 要检查的周期类型（可选，默认主要周期）
--- @return table 临界日列表
function BiorhythmUtils.find_critical_days(birth_year, birth_month, birth_day, start_year, start_month, start_day, days, cycle_types)
    -- 参数处理
    if not start_year then
        start_year, start_month, start_day = get_current_date()
    end
    if not days then
        days = 30
    end
    if days <= 0 then
        return {}
    end
    if not cycle_types then
        cycle_types = { "physical", "emotional", "intellectual" }
    end
    
    -- 计算基准 days_alive
    local start_days = days_between(birth_year, birth_month, birth_day, start_year, start_month, start_day)
    
    local critical_days = {}
    
    for _, cycle_type in ipairs(cycle_types) do
        local period
        if PRIMARY_PERIODS[cycle_type] then
            period = PRIMARY_PERIODS[cycle_type]
        elseif SECONDARY_PERIODS[cycle_type] then
            period = SECONDARY_PERIODS[cycle_type]
        else
            goto continue
        end
        
        -- 计算当前在周期中的位置
        local days_into_cycle = start_days % period
        
        -- 计算半周期位置
        local half_period = math.floor(period / 2)
        
        -- 计算到下一个上升零点和下降零点的时间
        local days_to_up_zero = (period - days_into_cycle) % period
        local days_to_down_zero = (half_period - days_into_cycle) % period
        
        -- 检查上升零点
        if days_to_up_zero > 0 and days_to_up_zero <= days then
            table.insert(critical_days, {
                date_offset = days_to_up_zero,
                cycle_type = cycle_type,
                direction = "up",
                description = CYCLE_NAMES[cycle_type] .. "周期上升零点",
            })
        end
        
        -- 检查下降零点
        if days_to_down_zero > 0 and days_to_down_zero <= days then
            table.insert(critical_days, {
                date_offset = days_to_down_zero,
                cycle_type = cycle_type,
                direction = "down",
                description = CYCLE_NAMES[cycle_type] .. "周期下降零点",
            })
        end
        
        ::continue::
    end
    
    -- 按日期排序
    table.sort(critical_days, function(a, b)
        return a.date_offset < b.date_offset
    end)
    
    return critical_days
end

--- 查找高峰日和低谷日
--- @param birth_year number 出生年
--- @param birth_month number 出生月
--- @param birth_day number 出生日
--- @param start_year number 起始年（可选，默认今日）
--- @param start_month number 起始月（可选）
--- @param start_day number 起始日（可选）
--- @param days number 查询天数（可选，默认30）
--- @param cycle_types table 要检查的周期类型（可选，默认主要周期）
--- @return table 高峰日和低谷日列表
function BiorhythmUtils.find_peak_days(birth_year, birth_month, birth_day, start_year, start_month, start_day, days, cycle_types)
    -- 参数处理
    if not start_year then
        start_year, start_month, start_day = get_current_date()
    end
    if not days then
        days = 30
    end
    if days <= 0 then
        return {}
    end
    if not cycle_types then
        cycle_types = { "physical", "emotional", "intellectual" }
    end
    
    local start_days = days_between(birth_year, birth_month, birth_day, start_year, start_month, start_day)
    
    local peak_days = {}
    
    for _, cycle_type in ipairs(cycle_types) do
        local period
        if PRIMARY_PERIODS[cycle_type] then
            period = PRIMARY_PERIODS[cycle_type]
        elseif SECONDARY_PERIODS[cycle_type] then
            period = SECONDARY_PERIODS[cycle_type]
        else
            goto continue
        end
        
        -- 高峰在 1/4 周期，低谷在 3/4 周期
        local peak_offset = math.floor(period / 4)
        local low_offset = math.floor(3 * period / 4)
        
        local days_into_cycle = start_days % period
        
        local days_to_peak = (peak_offset - days_into_cycle) % period
        local days_to_low = (low_offset - days_into_cycle) % period
        
        -- 添加高峰日
        if days_to_peak > 0 and days_to_peak <= days then
            table.insert(peak_days, {
                date_offset = days_to_peak,
                cycle_type = cycle_type,
                is_peak = true,
                value = 100.0,
            })
        end
        
        -- 添加低谷日
        if days_to_low > 0 and days_to_low <= days then
            table.insert(peak_days, {
                date_offset = days_to_low,
                cycle_type = cycle_type,
                is_peak = false,
                value = -100.0,
            })
        end
        
        ::continue::
    end
    
    -- 排序
    table.sort(peak_days, function(a, b)
        return a.date_offset < b.date_offset
    end)
    
    return peak_days
end

--- 生成 ASCII 生物节律图表
--- @param birth_year number 出生年
--- @param birth_month number 出生月
--- @param birth_day number 出生日
--- @param start_year number 起始年（可选，默认今日）
--- @param start_month number 起始月（可选）
--- @param start_day number 起始日（可选）
--- @param days number 显示天数（可选，默认30）
--- @param width number 图表宽度（可选，默认60）
--- @param height number 图表高度（可选，默认15）
--- @return string ASCII 图表字符串
function BiorhythmUtils.generate_chart(birth_year, birth_month, birth_day, start_year, start_month, start_day, days, width, height)
    -- 参数处理
    if not start_year then
        start_year, start_month, start_day = get_current_date()
    end
    if not days then
        days = 30
    end
    if not width then
        width = 60
    end
    if not height then
        height = 15
    end
    
    -- 边界检查
    if days <= 0 or width <= 0 or height <= 0 then
        return "(无效参数)"
    end
    
    -- 计算基准 days_alive
    local base_days_alive = days_between(birth_year, birth_month, birth_day, start_year, start_month, start_day)
    
    -- 创建图表网格
    local chart = {}
    for y = 1, height do
        chart[y] = {}
        for x = 1, width do
            chart[y][x] = " "
        end
    end
    
    -- 绘制中心线（零点线）
    local center = math.floor(height / 2) + 1
    for x = 1, width do
        chart[center][x] = "-"
    end
    
    -- 周期字符映射
    local cycle_chars = {
        physical = "P",
        emotional = "E",
        intellectual = "I",
    }
    
    local periods = {}
    for ct, _ in pairs(cycle_chars) do
        periods[ct] = PRIMARY_PERIODS[ct]
    end
    
    -- 计算并绘制每个周期的值
    for cycle_type, char in pairs(cycle_chars) do
        local period = periods[cycle_type]
        
        for x = 1, width do
            -- 计算日期偏移量
            local day_offset = math.floor((x - 1) / width * days)
            local days_alive = base_days_alive + day_offset
            
            local value = calculate_biorhythm(days_alive, period)
            
            -- 将值映射到 y 位置 (100 -> 0, -100 -> height-1)
            local y = math.floor(center - (value / 100) * (height / 2))
            y = math.max(1, math.min(height, y))
            
            -- 只在空位绘制
            if chart[y][x] == " " or chart[y][x] == "-" then
                chart[y][x] = char
            else
                chart[y][x] = "*"
            end
        end
    end
    
    -- 构建输出
    local lines = {}
    
    -- 计算结束日期
    local end_year, end_month, end_day = start_year, start_month, start_day
    -- 简化处理：直接使用开始日期 + days 天
    local total_start_days = days_between(1970, 1, 1, start_year, start_month, start_day)
    local end_total_days = total_start_days + days - 1
    
    -- 转换回日期
    local function days_to_date(total_days)
        local year = 1970
        while true do
            local days_in_year = ((year % 4 == 0 and year % 100 ~= 0) or (year % 400 == 0)) and 366 or 365
            if total_days < days_in_year then
                break
            end
            total_days = total_days - days_in_year
            year = year + 1
        end
        
        local days_in_month_tbl = {31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31}
        if (year % 4 == 0 and year % 100 ~= 0) or (year % 400 == 0) then
            days_in_month_tbl[2] = 29
        end
        
        local month = 1
        while total_days >= days_in_month_tbl[month] do
            total_days = total_days - days_in_month_tbl[month]
            month = month + 1
        end
        
        return year, month, total_days + 1
    end
    
    end_year, end_month, end_day = days_to_date(end_total_days)
    
    -- 标题
    table.insert(lines, string.format("生物节律图表 (%04d-%02d-%02d ~ %04d-%02d-%02d)", start_year, start_month, start_day, end_year, end_month, end_day))
    table.insert(lines, string.format("生日: %04d-%02d-%02d", birth_year, birth_month, birth_day))
    table.insert(lines, "")
    
    -- 图表
    table.insert(lines, "+100% |" .. table.concat(chart[1]))
    for y = 2, center - 1 do
        table.insert(lines, "      |" .. table.concat(chart[y]))
    end
    table.insert(lines, "   0% |" .. table.concat(chart[center]))
    for y = center + 1, height - 1 do
        table.insert(lines, "      |" .. table.concat(chart[y]))
    end
    table.insert(lines, "-100% |" .. table.concat(chart[height]))
    
    -- 图例
    table.insert(lines, "")
    table.insert(lines, "图例: P=体力 E=情绪 I=智力 *=重叠")
    
    return table.concat(lines, "\n")
end

--- 计算两人生物节律契合度
--- @param birth1_year number 第一人出生年
--- @param birth1_month number 第一人出生月
--- @param birth1_day number 第一人出生日
--- @param birth2_year number 第二人出生年
--- @param birth2_month number 第二人出生月
--- @param birth2_day number 第二人出生日
--- @param target_year number 目标年（可选，默认今日）
--- @param target_month number 目标月（可选）
--- @param target_day number 目标日（可选）
--- @return table 契合度分析结果
function BiorhythmUtils.compatibility(birth1_year, birth1_month, birth1_day, birth2_year, birth2_month, birth2_day, target_year, target_month, target_day)
    -- 参数处理
    if not target_year then
        target_year, target_month, target_day = get_current_date()
    end
    
    -- 计算两人的生物节律
    local bio1 = BiorhythmUtils.calculate(birth1_year, birth1_month, birth1_day, target_year, target_month, target_day)
    local bio2 = BiorhythmUtils.calculate(birth2_year, birth2_month, birth2_day, target_year, target_month, target_day)
    
    local compatibilities = {}
    
    for cycle_type, _ in pairs(PRIMARY_PERIODS) do
        local v1 = bio1.primary_cycles[cycle_type].value
        local v2 = bio2.primary_cycles[cycle_type].value
        
        -- 基于差值计算契合度
        local difference = math.abs(v1 - v2)
        
        -- 符号相同契合度高，符号相反契合度低
        local compatibility
        if (v1 >= 0 and v2 >= 0) or (v1 < 0 and v2 < 0) then
            compatibility = 100 - difference / 2
        else
            compatibility = 50 - difference / 4
        end
        
        compatibility = math.max(0, math.min(100, compatibility))
        compatibilities[cycle_type] = compatibility
    end
    
    -- 综合契合度
    local overall = (compatibilities.physical + compatibilities.emotional + compatibilities.intellectual) / 3
    
    -- 解读
    local interpretation
    if overall >= 80 then
        interpretation = "极佳同步！两人的节律高度一致，是互相支持的好时机。"
    elseif overall >= 60 then
        interpretation = "良好同步。大多数节律相近，适合合作与交流。"
    elseif overall >= 40 then
        interpretation = "一般同步。部分节律相近，可能需要互相理解。"
    else
        interpretation = "低同步。节律差异较大，建议多沟通理解。"
    end
    
    return {
        physical = compatibilities.physical,
        emotional = compatibilities.emotional,
        intellectual = compatibilities.intellectual,
        overall = overall,
        interpretation = interpretation,
        date = string.format("%04d-%02d-%02d", target_year, target_month, target_day),
    }
end

--- 获取生肖信息
--- @param birth_year number 出生年
--- @return table 生肖信息
function BiorhythmUtils.get_zodiac(birth_year)
    local zodiac_list = {
        { cn = "鼠", en = "Rat", branch = "子" },
        { cn = "牛", en = "Ox", branch = "丑" },
        { cn = "虎", en = "Tiger", branch = "寅" },
        { cn = "兔", en = "Rabbit", branch = "卯" },
        { cn = "龙", en = "Dragon", branch = "辰" },
        { cn = "蛇", en = "Snake", branch = "巳" },
        { cn = "马", en = "Horse", branch = "午" },
        { cn = "羊", en = "Goat", branch = "未" },
        { cn = "猴", en = "Monkey", branch = "申" },
        { cn = "鸡", en = "Rooster", branch = "酉" },
        { cn = "狗", en = "Dog", branch = "戌" },
        { cn = "猪", en = "Pig", branch = "亥" },
    }
    
    local elements = { "金", "木", "水", "火", "土" }
    
    -- 生肖索引
    local zodiac_index = (birth_year - 1900) % 12
    
    -- 五行索引
    local element_index = math.floor((birth_year % 10) / 2)
    
    local zodiac = zodiac_list[zodiac_index + 1]
    local element = elements[element_index + 1]
    
    return {
        animal_cn = zodiac.cn,
        animal_en = zodiac.en,
        earthly_branch = zodiac.branch,
        element = element,
        description = element .. zodiac.cn,
    }
end

--- 获取每日摘要
--- @param birth_year number 出生年
--- @param birth_month number 出生月
--- @param birth_day number 出生日
--- @param target_year number 目标年（可选，默认今日）
--- @param target_month number 目标月（可选）
--- @param target_day number 目标日（可选）
--- @return string 格式化摘要字符串
function BiorhythmUtils.get_daily_summary(birth_year, birth_month, birth_day, target_year, target_month, target_day)
    -- 参数处理
    if not target_year then
        target_year, target_month, target_day = get_current_date()
    end
    
    local result = BiorhythmUtils.calculate(birth_year, birth_month, birth_day, target_year, target_month, target_day, true)
    
    local lines = {}
    
    table.insert(lines, string.rep("=", 50))
    table.insert(lines, string.format("生物节律日报 - %s", result.target_date))
    table.insert(lines, string.format("生日: %s (已生活 %d 天)", result.birth_date, result.days_alive))
    table.insert(lines, string.rep("=", 50))
    table.insert(lines, "")
    
    table.insert(lines, "【主要周期】")
    for cycle_type, _ in pairs(PRIMARY_PERIODS) do
        local value = result.primary_cycles[cycle_type]
        local name = CYCLE_NAMES[cycle_type]
        local desc = CYCLE_DESCRIPTIONS[cycle_type]
        
        local bar = BiorhythmUtils._generate_value_bar(value.value)
        local status
        if value.value > 50 then
            status = "📈"
        elseif value.value < -50 then
            status = "📉"
        elseif value.is_critical then
            status = "⚠️ "
        else
            status = "➡️"
        end
        
        table.insert(lines, string.format("  %s: %s %+.1f%% %s", name, bar, value.value, status))
        table.insert(lines, string.format("    %s", desc))
        table.insert(lines, "")
    end
    
    table.insert(lines, "【次要周期】")
    for cycle_type, _ in pairs(SECONDARY_PERIODS) do
        local value = result.secondary_cycles[cycle_type]
        local name = CYCLE_NAMES[cycle_type]
        
        local bar = BiorhythmUtils._generate_value_bar(value.value)
        local status
        if value.value > 50 then
            status = "📈"
        elseif value.value < -50 then
            status = "📉"
        elseif value.is_critical then
            status = "⚠️ "
        else
            status = "➡️"
        end
        
        table.insert(lines, string.format("  %s: %s %+.1f%% %s", name, bar, value.value, status))
    end
    
    table.insert(lines, "")
    table.insert(lines, string.format("【综合能量】%.1f%%", result.overall_energy))
    table.insert(lines, "")
    
    -- 总结
    local high_cycles = {}
    local low_cycles = {}
    local critical_cycles = {}
    
    for cycle_type, v in pairs(result.primary_cycles) do
        if v.is_critical then
            table.insert(critical_cycles, CYCLE_NAMES[cycle_type])
        elseif v.value > 50 then
            table.insert(high_cycles, CYCLE_NAMES[cycle_type])
        elseif v.value < -50 then
            table.insert(low_cycles, CYCLE_NAMES[cycle_type])
        end
    end
    
    if #critical_cycles > 0 then
        table.insert(lines, string.format("⚠️ 临界日: %s", table.concat(critical_cycles, ", ")))
    end
    if #high_cycles > 0 then
        table.insert(lines, string.format("📈 高峰期: %s", table.concat(high_cycles, ", ")))
    end
    if #low_cycles > 0 then
        table.insert(lines, string.format("📉 低谷期: %s", table.concat(low_cycles, ", ")))
    end
    if #critical_cycles == 0 and #high_cycles == 0 and #low_cycles == 0 then
        table.insert(lines, "💪 各项指标平稳")
    end
    
    return table.concat(lines, "\n")
end

--- 生成值条形图（内部使用）
--- @param value number 数值 (-100 到 100)
--- @param width number 宽度（可选，默认20）
--- @return string 条形图字符串
function BiorhythmUtils._generate_value_bar(value, width)
    if not width then
        width = 20
    end
    
    local half_width = math.floor(width / 2)
    
    local bar
    if value >= 0 then
        local filled = math.floor((value / 100) * half_width)
        bar = string.rep("░", half_width - filled) .. string.rep("▓", filled) .. "│" .. string.rep("░", half_width)
    else
        local filled = math.floor((-value / 100) * half_width)
        bar = string.rep("░", half_width) .. "│" .. string.rep("▓", filled) .. string.rep("░", half_width - filled)
    end
    
    return bar
end

-------------------------------------------------------------------------------
-- 便捷函数
-------------------------------------------------------------------------------

--- 计算生物节律（使用今日作为目标日期）
--- @param birth_year number 出生年
--- @param birth_month number 出生月
--- @param birth_day number 出生日
--- @return table 生物节律结果
function BiorhythmUtils.today(birth_year, birth_month, birth_day)
    return BiorhythmUtils.calculate(birth_year, birth_month, birth_day)
end

--- 获取生命数字（出生后总天数）
--- @param birth_year number 出生年
--- @param birth_month number 出生月
--- @param birth_day number 出生日
--- @return number 生命数字
function BiorhythmUtils.days_alive(birth_year, birth_month, birth_day)
    local ty, tm, td = get_current_date()
    return days_between(birth_year, birth_month, birth_day, ty, tm, td)
end

return BiorhythmUtils

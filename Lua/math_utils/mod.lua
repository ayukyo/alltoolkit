---
-- Math Utilities Module
-- 数学工具函数库
--
-- 提供常用的数学计算功能，包括统计、数论、格式化、随机数等。
-- 仅使用 Lua 标准库，零依赖。
--
-- @author AllToolkit
-- @version 1.0.0
-- @copyright MIT License

local MathUtils = {}
local MathUtilsMT = { __index = MathUtils }

--- 版本号
MathUtils.VERSION = "1.0.0"

--- 常量
MathUtils.PI = math.pi
MathUtils.E = math.exp(1)
MathUtils.PHI = (1 + math.sqrt(5)) / 2  -- 黄金比例
MathUtils.SQRT2 = math.sqrt(2)

--- 错误处理
MathUtils.Error = {
    InvalidArgument = "Invalid argument",
    DivisionByZero = "Division by zero",
    OutOfRange = "Value out of range",
    EmptyTable = "Empty table",
}

-------------------------------------------------------------------------------
-- 基础数学工具
-------------------------------------------------------------------------------

--- 检查值是否为数字
-- @param n 要检查的值
-- @return boolean 如果是数字返回 true
function MathUtils.is_number(n)
    return type(n) == "number" and n == n  -- n == n 检查 NaN
end

--- 检查值是否为整数
-- @param n 要检查的值
-- @return boolean 如果是整数返回 true
function MathUtils.is_integer(n)
    if type(n) ~= "number" then return false end
    return n == math.floor(n)
end

--- 安全除法
-- @param a 被除数
-- @param b 除数
-- @param default 除数为 0 时的默认值
-- @return number 除法结果或默认值
function MathUtils.safe_divide(a, b, default)
    if b == 0 then
        return default or 0
    end
    return a / b
end

--- 计算百分比
-- @param part 部分值
-- @param total 总值
-- @return number 百分比 (0-100)
function MathUtils.percentage(part, total)
    if total == 0 then return 0 end
    return (part / total) * 100
end

--- 计算增长率
-- @param old 旧值
-- @param new 新值
-- @return number 增长率百分比
function MathUtils.growth_rate(old, new)
    if old == 0 then
        return new > 0 and 100 or (new < 0 and -100 or 0)
    end
    return ((new - old) / old) * 100
end

--- 四舍五入到指定位数
-- @param n 数字
-- @param decimals 小数位数
-- @return number 四舍五入后的数字
function MathUtils.round(n, decimals)
    decimals = decimals or 0
    local mult = 10 ^ decimals
    return math.floor(n * mult + 0.5) / mult
end

--- 向下取整到指定位数
-- @param n 数字
-- @param decimals 小数位数
-- @return number 向下取整后的数字
function MathUtils.floor_decimal(n, decimals)
    decimals = decimals or 0
    local mult = 10 ^ decimals
    return math.floor(n * mult) / mult
end

--- 向上取整到指定位数
-- @param n 数字
-- @param decimals 小数位数
-- @return number 向上取整后的数字
function MathUtils.ceil_decimal(n, decimals)
    decimals = decimals or 0
    local mult = 10 ^ decimals
    return math.ceil(n * mult) / mult
end

--- 限制数值范围
-- @param n 数字
-- @param min 最小值
-- @param max 最大值
-- @return number 限制后的数字
function MathUtils.clamp(n, min, max)
    if n < min then return min end
    if n > max then return max end
    return n
end

--- 线性插值
-- @param a 起始值
-- @param b 结束值
-- @param t 插值因子 (0-1)
-- @return number 插值结果
function MathUtils.lerp(a, b, t)
    t = MathUtils.clamp(t, 0, 1)
    return a + (b - a) * t
end

-------------------------------------------------------------------------------
-- 统计函数
-------------------------------------------------------------------------------

--- 计算数组总和
-- @param numbers 数字数组
-- @return number 总和
function MathUtils.sum(numbers)
    local total = 0
    for _, n in ipairs(numbers) do
        total = total + n
    end
    return total
end

--- 计算平均值
-- @param numbers 数字数组
-- @return number 平均值
function MathUtils.average(numbers)
    local count = #numbers
    if count == 0 then return 0 end
    return MathUtils.sum(numbers) / count
end

--- 计算中位数
-- @param numbers 数字数组
-- @return number 中位数
function MathUtils.median(numbers)
    if #numbers == 0 then return 0 end
    
    -- 复制并排序
    local sorted = {}
    for _, n in ipairs(numbers) do
        table.insert(sorted, n)
    end
    table.sort(sorted)
    
    local count = #sorted
    local mid = math.ceil(count / 2)
    
    if count % 2 == 0 then
        return (sorted[mid] + sorted[mid + 1]) / 2
    else
        return sorted[mid]
    end
end

--- 计算众数（出现最频繁的数）
-- @param numbers 数字数组
-- @return number 众数
function MathUtils.mode(numbers)
    if #numbers == 0 then return nil end
    
    local counts = {}
    for _, n in ipairs(numbers) do
        counts[n] = (counts[n] or 0) + 1
    end
    
    local mode_value = numbers[1]
    local mode_count = 0
    
    for n, count in pairs(counts) do
        if count > mode_count then
            mode_value = n
            mode_count = count
        end
    end
    
    return mode_value
end

--- 计算方差
-- @param numbers 数字数组
-- @return number 方差
function MathUtils.variance(numbers)
    local count = #numbers
    if count == 0 then return 0 end
    
    local avg = MathUtils.average(numbers)
    local sum_sq = 0
    
    for _, n in ipairs(numbers) do
        local diff = n - avg
        sum_sq = sum_sq + diff * diff
    end
    
    return sum_sq / count
end

--- 计算标准差
-- @param numbers 数字数组
-- @return number 标准差
function MathUtils.stddev(numbers)
    return math.sqrt(MathUtils.variance(numbers))
end

--- 计算最小值
-- @param numbers 数字数组
-- @return number 最小值
function MathUtils.min(numbers)
    if #numbers == 0 then return nil end
    local min_val = numbers[1]
    for i = 2, #numbers do
        if numbers[i] < min_val then
            min_val = numbers[i]
        end
    end
    return min_val
end

--- 计算最大值
-- @param numbers 数字数组
-- @return number 最大值
function MathUtils.max(numbers)
    if #numbers == 0 then return nil end
    local max_val = numbers[1]
    for i = 2, #numbers do
        if numbers[i] > max_val then
            max_val = numbers[i]
        end
    end
    return max_val
end

--- 计算范围（最大值 - 最小值）
-- @param numbers 数字数组
-- @return number 范围
function MathUtils.range(numbers)
    if #numbers == 0 then return 0 end
    return MathUtils.max(numbers) - MathUtils.min(numbers)
end

-------------------------------------------------------------------------------
-- 数论函数
-------------------------------------------------------------------------------

--- 计算最大公约数 (GCD)
-- @param a 第一个数
-- @param b 第二个数
-- @return number 最大公约数
function MathUtils.gcd(a, b)
    a = math.abs(a)
    b = math.abs(b)
    while b ~= 0 do
        a, b = b, a % b
    end
    return a
end

--- 计算最小公倍数 (LCM)
-- @param a 第一个数
-- @param b 第二个数
-- @return number 最小公倍数
function MathUtils.lcm(a, b)
    if a == 0 or b == 0 then return 0 end
    return math.abs(a * b) / MathUtils.gcd(a, b)
end

--- 判断是否为质数
-- @param n 要检查的数
-- @return boolean 如果是质数返回 true
function MathUtils.is_prime(n)
    if n <= 1 then return false end
    if n <= 3 then return true end
    if n % 2 == 0 or n % 3 == 0 then return false end
    
    local i = 5
    while i * i <= n do
        if n % i == 0 or n % (i + 2) == 0 then
            return false
        end
        i = i + 6
    end
    return true
end

--- 获取小于等于 n 的最大质数
-- @param n 上限
-- @return number 最大质数
function MathUtils.prev_prime(n)
    while n >= 2 do
        if MathUtils.is_prime(n) then
            return n
        end
        n = n - 1
    end
    return nil
end

--- 获取大于等于 n 的最小质数
-- @param n 下限
-- @return number 最小质数
function MathUtils.next_prime(n)
    if n <= 2 then return 2 end
    if n % 2 == 0 then n = n + 1 end
    while true do
        if MathUtils.is_prime(n) then
            return n
        end
        n = n + 2
    end
end

--- 计算阶乘
-- @param n 非负整数
-- @return number 阶乘结果
function MathUtils.factorial(n)
    if n < 0 then return nil end
    if n <= 1 then return 1 end
    local result = 1
    for i = 2, n do
        result = result * i
    end
    return result
end

--- 计算组合数 C(n, k)
-- @param n 总数
-- @param k 选择数
-- @return number 组合数
function MathUtils.combinations(n, k)
    if k < 0 or k > n then return 0 end
    if k == 0 or k == n then return 1 end
    if k > n / 2 then k = n - k end
    
    local result = 1
    for i = 1, k do
        result = result * (n - i + 1) / i
    end
    return result
end

--- 计算排列数 P(n, k)
-- @param n 总数
-- @param k 选择数
-- @return number 排列数
function MathUtils.permutations(n, k)
    if k < 0 or k > n then return 0 end
    if k == 0 then return 1 end
    
    local result = 1
    for i = 0, k - 1 do
        result = result * (n - i)
    end
    return result
end

--- 获取 n 的所有因数
-- @param n 数字
-- @return table 因数数组
function MathUtils.divisors(n)
    if n <= 0 then return {} end
    
    local divs = {}
    for i = 1, math.floor(math.sqrt(n)) do
        if n % i == 0 then
            table.insert(divs, i)
            if i ~= n / i then
                table.insert(divs, math.floor(n / i))
            end
        end
    end
    table.sort(divs)
    return divs
end

--- 获取 n 的质因数分解
-- @param n 数字
-- @return table 质因数及其指数的表 {factor = exponent}
function MathUtils.prime_factorization(n)
    if n <= 1 then return {} end
    
    local factors = {}
    local d = 2
    
    while d * d <= n do
        while n % d == 0 do
            factors[d] = (factors[d] or 0) + 1
            n = n / d
        end
        d = d + 1
    end
    
    if n > 1 then
        factors[n] = (factors[n] or 0) + 1
    end
    
    return factors
end

-------------------------------------------------------------------------------
-- 三角函数扩展（角度版本）
-------------------------------------------------------------------------------

--- 角度转弧度
-- @param degrees 角度
-- @return number 弧度
function MathUtils.deg_to_rad(degrees)
    return degrees * math.pi / 180
end

--- 弧度转角度
-- @param radians 弧度
-- @return number 角度
function MathUtils.rad_to_deg(radians)
    return radians * 180 / math.pi
end

--- 正弦函数（角度版）
-- @param degrees 角度
-- @return number 正弦值
function MathUtils.sin_deg(degrees)
    return math.sin(MathUtils.deg_to_rad(degrees))
end

--- 余弦函数（角度版）
-- @param degrees 角度
-- @return number 余弦值
function MathUtils.cos_deg(degrees)
    return math.cos(MathUtils.deg_to_rad(degrees))
end

--- 正切函数（角度版）
-- @param degrees 角度
-- @return number 正切值
function MathUtils.tan_deg(degrees)
    return math.tan(MathUtils.deg_to_rad(degrees))
end

--- 反正弦函数（角度版）
-- @param value 正弦值
-- @return number 角度
function MathUtils.asin_deg(value)
    return MathUtils.rad_to_deg(math.asin(value))
end

--- 反余弦函数（角度版）
-- @param value 余弦值
-- @return number 角度
function MathUtils.acos_deg(value)
    return MathUtils.rad_to_deg(math.acos(value))
end

--- 反正切函数（角度版）
-- @param value 正切值
-- @return number 角度
function MathUtils.atan_deg(value)
    return MathUtils.rad_to_deg(math.atan(value))
end

-------------------------------------------------------------------------------
-- 数值格式化
-------------------------------------------------------------------------------

--- 格式化数字为千分位字符串
-- @param n 数字
-- @param separator 千分位分隔符
-- @return string 格式化后的字符串
function MathUtils.format_thousands(n, separator)
    separator = separator or ","
    local formatted = tostring(math.floor(n))
    local len = #formatted
    local result = ""
    
    -- 从右到左处理，每 3 位添加分隔符
    local count = 0
    for i = len, 1, -1 do
        if count > 0 and count % 3 == 0 then
            result = separator .. result
        end
        result = formatted:sub(i, i) .. result
        count = count + 1
    end
    
    -- 添加小数部分
    local decimal = tostring(n):match("%.(.*)")
    if decimal then
        result = result .. "." .. decimal
    end
    
    return result
end

--- 格式化字节数为人类可读格式
-- @param bytes 字节数
-- @param precision 小数位数
-- @return string 格式化后的字符串 (如 "1.5 MB")
function MathUtils.format_bytes(bytes, precision)
    precision = precision or 2
    local units = {"B", "KB", "MB", "GB", "TB", "PB"}
    local unit_index = 1
    local size = bytes
    
    while size >= 1024 and unit_index < #units do
        size = size / 1024
        unit_index = unit_index + 1
    end
    
    return string.format("%." .. precision .. "f %s", size, units[unit_index])
end

--- 格式化数字为科学计数法
-- @param n 数字
-- @param precision 小数位数
-- @return string 科学计数法字符串
function MathUtils.format_scientific(n, precision)
    precision = precision or 2
    return string.format("%." .. precision .. "e", n)
end

--- 格式化数字为货币格式
-- @param amount 金额
-- @param currency 货币符号
-- @param precision 小数位数
-- @return string 货币格式字符串
function MathUtils.format_currency(amount, currency, precision)
    currency = currency or "$"
    precision = precision or 2
    local sign = amount < 0 and "-" or ""
    amount = math.abs(amount)
    
    local formatted = string.format("%." .. precision .. "f", amount)
    local parts = {}
    for part in formatted:gmatch("[^%.]+") do
        table.insert(parts, part)
    end
    
    local integer = parts[1] or "0"
    local decimal = parts[2] or string.rep("0", precision)
    
    -- 添加千分位（从右到左）
    local int_formatted = ""
    local len = #integer
    local count = 0
    for i = len, 1, -1 do
        if count > 0 and count % 3 == 0 then
            int_formatted = "," .. int_formatted
        end
        int_formatted = integer:sub(i, i) .. int_formatted
        count = count + 1
    end
    
    return sign .. currency .. int_formatted .. "." .. decimal
end

-------------------------------------------------------------------------------
-- 随机数工具
-------------------------------------------------------------------------------

--- 生成指定范围内的随机整数
-- @param min 最小值
-- @param max 最大值
-- @return number 随机整数
function MathUtils.random_int(min, max)
    return math.random(min, max)
end

--- 生成指定范围内的随机浮点数
-- @param min 最小值
-- @param max 最大值
-- @return number 随机浮点数
function MathUtils.random_float(min, max)
    return min + math.random() * (max - min)
end

--- 从数组中随机选择一个元素
-- @param array 数组
-- @return any 随机元素
function MathUtils.random_choice(array)
    if #array == 0 then return nil end
    return array[math.random(1, #array)]
end

--- 随机打乱数组
-- @param array 数组
-- @return table 打乱后的新数组
function MathUtils.shuffle(array)
    local shuffled = {}
    for _, v in ipairs(array) do
        table.insert(shuffled, v)
    end
    
    for i = #shuffled, 2, -1 do
        local j = math.random(1, i)
        shuffled[i], shuffled[j] = shuffled[j], shuffled[i]
    end
    
    return shuffled
end

--- 生成随机 UUID v4
-- @return string UUID 字符串
function MathUtils.uuid()
    local template = "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx"
    return string.gsub(template, "[xy]", function(c)
        local v = (c == "x") and math.random(0, 15) or math.random(8, 11)
        return string.format("%x", v)
    end)
end

-------------------------------------------------------------------------------
-- 向量操作
-------------------------------------------------------------------------------

--- 向量加法
-- @param a 向量 1
-- @param b 向量 2
-- @return table 结果向量
function MathUtils.vector_add(a, b)
    local result = {}
    for i = 1, math.min(#a, #b) do
        result[i] = a[i] + b[i]
    end
    return result
end

--- 向量减法
-- @param a 向量 1
-- @param b 向量 2
-- @return table 结果向量
function MathUtils.vector_sub(a, b)
    local result = {}
    for i = 1, math.min(#a, #b) do
        result[i] = a[i] - b[i]
    end
    return result
end

--- 向量点积
-- @param a 向量 1
-- @param b 向量 2
-- @return number 点积结果
function MathUtils.dot_product(a, b)
    local sum = 0
    for i = 1, math.min(#a, #b) do
        sum = sum + a[i] * b[i]
    end
    return sum
end

--- 向量长度（模）
-- @param v 向量
-- @return number 向量长度
function MathUtils.vector_length(v)
    local sum = 0
    for _, n in ipairs(v) do
        sum = sum + n * n
    end
    return math.sqrt(sum)
end

--- 向量归一化
-- @param v 向量
-- @return table 单位向量
function MathUtils.normalize(v)
    local len = MathUtils.vector_length(v)
    if len == 0 then return v end
    
    local result = {}
    for _, n in ipairs(v) do
        table.insert(result, n / len)
    end
    return result
end

--- 向量距离
-- @param a 向量 1
-- @param b 向量 2
-- @return number 欧几里得距离
function MathUtils.distance(a, b)
    local sum = 0
    for i = 1, math.min(#a, #b) do
        local diff = a[i] - b[i]
        sum = sum + diff * diff
    end
    return math.sqrt(sum)
end

-------------------------------------------------------------------------------
-- 序列生成
-------------------------------------------------------------------------------

--- 生成等差数列
-- @param start 起始值
-- @param stop 结束值
-- @param step 步长
-- @return table 数列数组
function MathUtils.range_seq(start, stop, step)
    if stop == nil then
        stop = start
        start = 0
    end
    step = step or 1
    
    local result = {}
    if step > 0 then
        for i = start, stop - step, step do
            table.insert(result, i)
        end
    else
        for i = start, stop - step, step do
            table.insert(result, i)
        end
    end
    return result
end

--- 生成斐波那契数列
-- @param count 项数
-- @return table 斐波那契数列
function MathUtils.fibonacci(count)
    if count <= 0 then return {} end
    if count == 1 then return {0} end
    
    local fibs = {0, 1}
    for i = 3, count do
        table.insert(fibs, fibs[i-1] + fibs[i-2])
    end
    return fibs
end

--- 获取第 n 个斐波那契数（使用 Binet 公式）
-- @param n 第 n 个
-- @return number 斐波那契数
function MathUtils.fib(n)
    if n <= 0 then return 0 end
    if n == 1 then return 1 end
    
    local sqrt5 = math.sqrt(5)
    local phi = (1 + sqrt5) / 2
    return math.floor((math.pow(phi, n) / sqrt5) + 0.5)
end

-------------------------------------------------------------------------------
-- 矩阵操作（基础）
-------------------------------------------------------------------------------

--- 创建零矩阵
-- @param rows 行数
-- @param cols 列数
-- @return table 零矩阵
function MathUtils.zeros(rows, cols)
    local matrix = {}
    for i = 1, rows do
        matrix[i] = {}
        for j = 1, cols do
            matrix[i][j] = 0
        end
    end
    return matrix
end

--- 创建单位矩阵
-- @param size 矩阵大小
-- @return table 单位矩阵
function MathUtils.identity(size)
    local matrix = MathUtils.zeros(size, size)
    for i = 1, size do
        matrix[i][i] = 1
    end
    return matrix
end

--- 矩阵转置
-- @param matrix 矩阵
-- @return table 转置后的矩阵
function MathUtils.transpose(matrix)
    local rows = #matrix
    local cols = #matrix[1]
    local result = MathUtils.zeros(cols, rows)
    
    for i = 1, rows do
        for j = 1, cols do
            result[j][i] = matrix[i][j]
        end
    end
    return result
end

--- 矩阵乘法
-- @param a 矩阵 A
-- @param b 矩阵 B
-- @return table 结果矩阵
function MathUtils.matrix_multiply(a, b)
    local a_rows = #a
    local a_cols = #a[1]
    local b_rows = #b
    local b_cols = #b[1]
    
    if a_cols ~= b_rows then
        error("Matrix dimensions incompatible for multiplication")
    end
    
    local result = MathUtils.zeros(a_rows, b_cols)
    
    for i = 1, a_rows do
        for j = 1, b_cols do
            local sum = 0
            for k = 1, a_cols do
                sum = sum + a[i][k] * b[k][j]
            end
            result[i][j] = sum
        end
    end
    return result
end

--- 矩阵与向量乘法
-- @param matrix 矩阵
-- @param vector 向量
-- @return table 结果向量
function MathUtils.matrix_vector_multiply(matrix, vector)
    local rows = #matrix
    local result = {}
    
    for i = 1, rows do
        local sum = 0
        for j = 1, #vector do
            sum = sum + matrix[i][j] * vector[j]
        end
        result[i] = sum
    end
    return result
end

-------------------------------------------------------------------------------
-- 特殊函数
-------------------------------------------------------------------------------

--- 计算自然对数
-- @param n 数字
-- @return number 自然对数
function MathUtils.ln(n)
    return math.log(n)
end

--- 计算以 10 为底的对数
-- @param n 数字
-- @return number 常用对数
function MathUtils.log10(n)
    return math.log10(n)
end

--- 计算以 2 为底的对数
-- @param n 数字
-- @return number 二进制对数
function MathUtils.log2(n)
    return math.log(n, 2)
end

--- 计算以任意底数的对数
-- @param n 数字
-- @param base 底数
-- @return number 对数
function MathUtils.log_base(n, base)
    return math.log(n) / math.log(base)
end

--- 计算平方根
-- @param n 数字
-- @return number 平方根
function MathUtils.sqrt(n)
    return math.sqrt(n)
end

--- 计算立方根
-- @param n 数字
-- @return number 立方根
function MathUtils.cbrt(n)
    if n >= 0 then
        return n ^ (1/3)
    else
        return -((-n) ^ (1/3))
    end
end

--- 计算幂
-- @param base 底数
-- @param exp 指数
-- @return number 幂结果
function MathUtils.power(base, exp)
    return base ^ exp
end

--- 计算绝对值
-- @param n 数字
-- @return number 绝对值
function MathUtils.abs(n)
    return math.abs(n)
end

--- 符号函数
-- @param n 数字
-- @return number -1, 0, 或 1
function MathUtils.sign(n)
    if n > 0 then return 1 end
    if n < 0 then return -1 end
    return 0
end

--- 判断是否为偶数
-- @param n 数字
-- @return boolean 如果是偶数返回 true
function MathUtils.is_even(n)
    return n % 2 == 0
end

--- 判断是否为奇数
-- @param n 数字
-- @return boolean 如果是奇数返回 true
function MathUtils.is_odd(n)
    return n % 2 ~= 0
end

-------------------------------------------------------------------------------
-- 工具函数
-------------------------------------------------------------------------------

--- 检查两个浮点数是否近似相等
-- @param a 第一个数
-- @param b 第二个数
-- @param epsilon 容差
-- @return boolean 是否近似相等
function MathUtils.almost_equal(a, b, epsilon)
    epsilon = epsilon or 1e-9
    return math.abs(a - b) < epsilon
end

--- 获取数字的位数
-- @param n 整数
-- @return number 位数
function MathUtils.digit_count(n)
    if n == 0 then return 1 end
    return math.floor(math.log10(math.abs(n))) + 1
end

--- 反转数字
-- @param n 整数
-- @return number 反转后的数字
function MathUtils.reverse_number(n)
    local negative = n < 0
    n = math.abs(n)
    
    local reversed = 0
    while n > 0 do
        reversed = reversed * 10 + n % 10
        n = math.floor(n / 10)
    end
    
    return negative and -reversed or reversed
end

--- 数字各位之和
-- @param n 整数
-- @return number 各位数字之和
function MathUtils.digit_sum(n)
    n = math.abs(n)
    local sum = 0
    while n > 0 do
        sum = sum + n % 10
        n = math.floor(n / 10)
    end
    return sum
end

--- 判断是否为完全平方数
-- @param n 数字
-- @return boolean 如果是完全平方数返回 true
function MathUtils.is_perfect_square(n)
    if n < 0 then return false end
    local root = math.sqrt(n)
    return root == math.floor(root)
end

--- 判断是否为完全立方数
-- @param n 数字
-- @return boolean 如果是完全立方数返回 true
function MathUtils.is_perfect_cube(n)
    if n < 0 then
        local root = MathUtils.cbrt(-n)
        local rounded = math.floor(root + 0.5)
        return math.abs(root - rounded) < 1e-6
    end
    local root = MathUtils.cbrt(n)
    local rounded = math.floor(root + 0.5)
    return math.abs(root - rounded) < 1e-6
end

return setmetatable(MathUtils, MathUtilsMT)

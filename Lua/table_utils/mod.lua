-- Table Utils 📦
-- Lua 表格工具模块 - 零依赖，生产就绪
-- 
-- 提供全面的表格操作功能：深度复制、合并、过滤、映射、排序、搜索等
-- 所有实现均使用 Lua 标准库，零外部依赖

local table_utils = {}

-- 版本号
table_utils._VERSION = "1.0.0"

--------------------------------------------------------------------------------
-- 基本操作
--------------------------------------------------------------------------------

--- 深度复制表格
-- @param original 要复制的表格
-- @param seen 内部使用，用于处理循环引用
-- @return 复制后的新表格
function table_utils.deepcopy(original, seen)
    seen = seen or {}
    
    -- 处理非表格类型
    if type(original) ~= "table" then
        return original
    end
    
    -- 检查循环引用
    if seen[original] then
        return seen[original]
    end
    
    local copy = {}
    seen[original] = copy
    
    -- 复制键值对
    for key, value in next, original, nil do
        copy[table_utils.deepcopy(key, seen)] = table_utils.deepcopy(value, seen)
    end
    
    -- 设置元表
    local mt = getmetatable(original)
    if mt then
        setmetatable(copy, table_utils.deepcopy(mt, seen))
    end
    
    return copy
end

--- 浅复制表格
-- @param original 要复制的表格
-- @return 复制后的新表格
function table_utils.shallowcopy(original)
    local copy = {}
    for key, value in pairs(original) do
        copy[key] = value
    end
    return copy
end

--- 获取表格大小（仅计算数组部分）
-- @param tbl 表格
-- @return 数组部分的大小
function table_utils.count(tbl)
    local count = 0
    for _ in pairs(tbl) do
        count = count + 1
    end
    return count
end

--- 获取数组长度（# 操作符的安全版本）
-- @param tbl 表格
-- @return 长度
function table_utils.length(tbl)
    return #tbl
end

--- 检查表格是否为空
-- @param tbl 表格
-- @return 如果为空返回 true
function table_utils.isempty(tbl)
    return next(tbl) == nil
end

--- 清空表格
-- @param tbl 要清空的表格
-- @return 原表格（已清空）
function table_utils.clear(tbl)
    for key in pairs(tbl) do
        tbl[key] = nil
    end
    return tbl
end

--------------------------------------------------------------------------------
-- 合并操作
--------------------------------------------------------------------------------

--- 合并多个表格（浅合并）
-- @param ... 要合并的表格
-- @return 合并后的新表格
function table_utils.merge(...)
    local result = {}
    local tables = {...}
    
    for _, tbl in ipairs(tables) do
        if type(tbl) == "table" then
            for key, value in pairs(tbl) do
                result[key] = value
            end
        end
    end
    
    return result
end

--- 深度合并多个表格
-- @param ... 要合并的表格
-- @return 深度合并后的新表格
function table_utils.deepmerge(...)
    local tables = {...}
    
    if #tables == 0 then
        return {}
    end
    
    local result = table_utils.deepcopy(tables[1])
    
    for i = 2, #tables do
        local tbl = tables[i]
        if type(tbl) == "table" then
            for key, value in pairs(tbl) do
                if type(value) == "table" and type(result[key]) == "table" then
                    result[key] = table_utils.deepmerge(result[key], value)
                else
                    result[key] = table_utils.deepcopy(value)
                end
            end
        end
    end
    
    return result
end

--- 更新表格（将 source 的值复制到 target）
-- @param target 目标表格
-- @param source 源表格
-- @return 更新后的目标表格
function table_utils.update(target, source)
    if type(target) ~= "table" or type(source) ~= "table" then
        return target
    end
    
    for key, value in pairs(source) do
        target[key] = value
    end
    
    return target
end

--------------------------------------------------------------------------------
-- 转换操作
--------------------------------------------------------------------------------

--- 将表格转换为键值对数组
-- @param tbl 表格
-- @return 包含 {key, value} 对的数组
function table_utils.topairs(tbl)
    local result = {}
    for key, value in pairs(tbl) do
        table.insert(result, {key = key, value = value})
    end
    return result
end

--- 将表格的键转换为数组
-- @param tbl 表格
-- @return 包含所有键的数组
function table_utils.keys(tbl)
    local result = {}
    for key in pairs(tbl) do
        table.insert(result, key)
    end
    return result
end

--- 将表格的值转换为数组
-- @param tbl 表格
-- @return 包含所有值的数组
function table_utils.values(tbl)
    local result = {}
    for _, value in pairs(tbl) do
        table.insert(result, value)
    end
    return result
end

--- 反转表格（键值互换）
-- @param tbl 表格
-- @return 键值互换后的新表格
function table_utils.invert(tbl)
    local result = {}
    for key, value in pairs(tbl) do
        result[value] = key
    end
    return result
end

--------------------------------------------------------------------------------
-- 过滤和映射
--------------------------------------------------------------------------------

--- 过滤表格
-- @param tbl 表格
-- @param predicate 谓词函数 (value, key) -> boolean
-- @return 过滤后的新表格
function table_utils.filter(tbl, predicate)
    local result = {}
    for key, value in pairs(tbl) do
        if predicate(value, key) then
            result[key] = value
        end
    end
    return result
end

--- 映射表格
-- @param tbl 表格
-- @param func 映射函数 (value, key) -> new_value
-- @return 映射后的新表格
function table_utils.map(tbl, func)
    local result = {}
    for key, value in pairs(tbl) do
        result[key] = func(value, key)
    end
    return result
end

--- 映射键
-- @param tbl 表格
-- @param func 映射函数 (key, value) -> new_key
-- @return 键映射后的新表格
function table_utils.mapkeys(tbl, func)
    local result = {}
    for key, value in pairs(tbl) do
        result[func(key, value)] = value
    end
    return result
end

--- 归约表格
-- @param tbl 表格
-- @param func 归约函数 (accumulator, value, key) -> new_accumulator
-- @param initial 初始值
-- @return 归约后的结果
function table_utils.reduce(tbl, func, initial)
    local accumulator = initial
    for key, value in pairs(tbl) do
        if accumulator == nil then
            accumulator = value
        else
            accumulator = func(accumulator, value, key)
        end
    end
    return accumulator
end

--- 查找表格中满足条件的第一个元素
-- @param tbl 表格
-- @param predicate 谓词函数 (value, key) -> boolean
-- @return 找到的值和键，如果未找到返回 nil
function table_utils.find(tbl, predicate)
    for key, value in pairs(tbl) do
        if predicate(value, key) then
            return value, key
        end
    end
    return nil
end

--- 检查表格是否包含满足条件的元素
-- @param tbl 表格
-- @param predicate 谓词函数 (value, key) -> boolean
-- @return 如果找到返回 true
function table_utils.some(tbl, predicate)
    for key, value in pairs(tbl) do
        if predicate(value, key) then
            return true
        end
    end
    return false
end

--- 检查表格所有元素是否满足条件
-- @param tbl 表格
-- @param predicate 谓词函数 (value, key) -> boolean
-- @return 如果所有元素都满足返回 true
function table_utils.every(tbl, predicate)
    for key, value in pairs(tbl) do
        if not predicate(value, key) then
            return false
        end
    end
    return true
end

--------------------------------------------------------------------------------
-- 数组操作（针对数组型表格）
--------------------------------------------------------------------------------

--- 推入数组末尾
-- @param tbl 表格
-- @param value 要推入的值
-- @return 新长度
function table_utils.push(tbl, value)
    table.insert(tbl, value)
    return #tbl
end

--- 从数组末尾弹出
-- @param tbl 表格
-- @return 弹出的值
function table_utils.pop(tbl)
    return table.remove(tbl)
end

--- 推入数组开头
-- @param tbl 表格
-- @param value 要推入的值
-- @return 新长度
function table_utils.unshift(tbl, value)
    table.insert(tbl, 1, value)
    return #tbl
end

--- 从数组开头弹出
-- @param tbl 表格
-- @return 弹出的值
function table_utils.shift(tbl)
    return table.remove(tbl, 1)
end

--- 连接多个数组
-- @param ... 要连接的数组
-- @return 连接后的新数组
function table_utils.concat(...)
    local result = {}
    local tables = {...}
    
    for _, tbl in ipairs(tables) do
        if type(tbl) == "table" then
            for _, value in ipairs(tbl) do
                table.insert(result, value)
            end
        end
    end
    
    return result
end

--- 切片数组
-- @param tbl 表格
-- @param start 起始索引（默认 1）
-- @param finish 结束索引（默认 #tbl）
-- @return 切片后的新数组
function table_utils.slice(tbl, start, finish)
    start = start or 1
    finish = finish or #tbl
    
    local result = {}
    for i = start, finish do
        if tbl[i] ~= nil then
            table.insert(result, tbl[i])
        end
    end
    return result
end

--- 拼接数组元素为字符串
-- @param tbl 表格
-- @param separator 分隔符（默认 ", "）
-- @param start 起始索引（默认 1）
-- @param finish 结束索引（默认 #tbl）
-- @return 拼接后的字符串
function table_utils.join(tbl, separator, start, finish)
    separator = separator or ", "
    start = start or 1
    finish = finish or #tbl
    
    local parts = {}
    for i = start, finish do
        if tbl[i] ~= nil then
            table.insert(parts, tostring(tbl[i]))
        end
    end
    return table.concat(parts, separator)
end

--- 数组去重
-- @param tbl 表格
-- @return 去重后的新数组
function table_utils.unique(tbl)
    local seen = {}
    local result = {}
    
    for _, value in ipairs(tbl) do
        if not seen[value] then
            seen[value] = true
            table.insert(result, value)
        end
    end
    
    return result
end

--- 数组展平
-- @param tbl 表格
-- @param depth 展平深度（默认 1，使用 math.huge 表示无限）
-- @return 展平后的新数组
function table_utils.flatten(tbl, depth)
    depth = depth or 1
    local result = {}
    
    local function flatten_recursive(t, d)
        for _, value in ipairs(t) do
            if type(value) == "table" and d > 0 then
                flatten_recursive(value, d - 1)
            else
                table.insert(result, value)
            end
        end
    end
    
    flatten_recursive(tbl, depth)
    return result
end

--- 数组压缩（移除 nil 值）
-- @param tbl 表格
-- @return 压缩后的新数组
function table_utils.compact(tbl)
    local result = {}
    -- 使用 pairs 遍历所有键，然后筛选数字键
    local keys = {}
    for key in pairs(tbl) do
        if type(key) == "number" then
            table.insert(keys, key)
        end
    end
    -- 排序键
    table.sort(keys)
    -- 按顺序收集非 nil 值
    for _, key in ipairs(keys) do
        if tbl[key] ~= nil then
            table.insert(result, tbl[key])
        end
    end
    return result
end

--------------------------------------------------------------------------------
-- 排序操作
--------------------------------------------------------------------------------

--- 对表格排序（返回新数组）
-- @param tbl 表格
-- @param comp 比较函数（可选）
-- @return 排序后的新数组
function table_utils.sort(tbl, comp)
    local result = table_utils.values(tbl)
    table.sort(result, comp)
    return result
end

--- 按指定键排序表格数组
-- @param tbl 表格数组
-- @param key 排序键
-- @param ascending 是否升序（默认 true）
-- @return 排序后的新数组
function table_utils.sortby(tbl, key, ascending)
    ascending = ascending == nil and true or ascending
    
    local result = table_utils.deepcopy(tbl)
    
    table.sort(result, function(a, b)
        if ascending then
            return a[key] < b[key]
        else
            return a[key] > b[key]
        end
    end)
    
    return result
end

--- 反转表格
-- @param tbl 表格
-- @return 反转后的新数组
function table_utils.reverse(tbl)
    local result = {}
    for i = #tbl, 1, -1 do
        table.insert(result, tbl[i])
    end
    return result
end

--------------------------------------------------------------------------------
-- 搜索和查找
--------------------------------------------------------------------------------

--- 查找值在数组中的索引
-- @param tbl 表格
-- @param value 要查找的值
-- @return 索引，未找到返回 nil
function table_utils.indexof(tbl, value)
    for i, v in ipairs(tbl) do
        if v == value then
            return i
        end
    end
    return nil
end

--- 查找值在数组中的最后一个索引
-- @param tbl 表格
-- @param value 要查找的值
-- @return 索引，未找到返回 nil
function table_utils.lastindexof(tbl, value)
    for i = #tbl, 1, -1 do
        if tbl[i] == value then
            return i
        end
    end
    return nil
end

--- 检查表格是否包含值
-- @param tbl 表格
-- @param value 要查找的值
-- @return 如果包含返回 true
function table_utils.includes(tbl, value)
    return table_utils.indexof(tbl, value) ~= nil
end

--- 检查表格是否包含键
-- @param tbl 表格
-- @param key 要查找的键
-- @return 如果包含返回 true
function table_utils.haskey(tbl, key)
    return tbl[key] ~= nil
end

--------------------------------------------------------------------------------
-- 集合操作
--------------------------------------------------------------------------------

--- 并集
-- @param tbl1 第一个表格
-- @param tbl2 第二个表格
-- @return 并集结果
function table_utils.union(tbl1, tbl2)
    local result = {}
    local seen = {}
    
    for _, value in ipairs(tbl1) do
        if not seen[value] then
            seen[value] = true
            table.insert(result, value)
        end
    end
    
    for _, value in ipairs(tbl2) do
        if not seen[value] then
            seen[value] = true
            table.insert(result, value)
        end
    end
    
    return result
end

--- 交集
-- @param tbl1 第一个表格
-- @param tbl2 第二个表格
-- @return 交集结果
function table_utils.intersection(tbl1, tbl2)
    local result = {}
    local seen = {}
    
    for _, value in ipairs(tbl2) do
        seen[value] = true
    end
    
    for _, value in ipairs(tbl1) do
        if seen[value] then
            table.insert(result, value)
        end
    end
    
    return result
end

--- 差集（tbl1 - tbl2）
-- @param tbl1 第一个表格
-- @param tbl2 第二个表格
-- @return 差集结果
function table_utils.difference(tbl1, tbl2)
    local result = {}
    local exclude = {}
    
    for _, value in ipairs(tbl2) do
        exclude[value] = true
    end
    
    for _, value in ipairs(tbl1) do
        if not exclude[value] then
            table.insert(result, value)
        end
    end
    
    return result
end

--------------------------------------------------------------------------------
-- 实用工具
--------------------------------------------------------------------------------

--- 创建范围数组
-- @param start 起始值
-- @param finish 结束值
-- @param step 步长（默认 1）
-- @return 范围数组
function table_utils.range(start, finish, step)
    step = step or 1
    local result = {}
    
    if step > 0 then
        for i = start, finish, step do
            table.insert(result, i)
        end
    else
        for i = start, finish, step do
            table.insert(result, i)
        end
    end
    
    return result
end

--- 创建填充数组
-- @param length 数组长度
-- @param value 填充值
-- @return 填充后的数组
function table_utils.fill(length, value)
    local result = {}
    for i = 1, length do
        result[i] = value
    end
    return result
end

--- 创建序列数组
-- @param length 数组长度
-- @param func 生成函数 (index) -> value
-- @return 序列数组
function table_utils.sequence(length, func)
    local result = {}
    for i = 1, length do
        result[i] = func(i)
    end
    return result
end

--- 分组表格
-- @param tbl 表格数组
-- @param keyfunc 分组函数 (value) -> group_key
-- @return 分组后的表格
function table_utils.groupby(tbl, keyfunc)
    local result = {}
    
    for _, value in ipairs(tbl) do
        local key = keyfunc(value)
        if not result[key] then
            result[key] = {}
        end
        table.insert(result[key], value)
    end
    
    return result
end

--- 分区表格
-- @param tbl 表格数组
-- @param predicate 分区函数 (value) -> boolean
-- @return 两个表格：满足条件的和不满足条件的
function table_utils.partition(tbl, predicate)
    local pass = {}
    local fail = {}
    
    for _, value in ipairs(tbl) do
        if predicate(value) then
            table.insert(pass, value)
        else
            table.insert(fail, value)
        end
    end
    
    return pass, fail
end

--------------------------------------------------------------------------------
-- 调试和输出
--------------------------------------------------------------------------------

--- 将表格转换为字符串表示
-- @param tbl 表格
-- @param indent 缩进（默认 0）
-- @return 字符串表示
function table_utils.tostring(tbl, indent)
    indent = indent or 0
    local padding = string.rep("  ", indent)
    local result = {"{\n"}
    
    for key, value in pairs(tbl) do
        local key_str = type(key) == "string" and string.format('["%s"]', key) or string.format("[%s]", tostring(key))
        
        if type(value) == "table" then
            table.insert(result, string.format("%s  %s = %s,\n", padding, key_str, table_utils.tostring(value, indent + 1)))
        else
            local value_str
            if type(value) == "string" then
                value_str = string.format('"%s"', value)
            else
                value_str = tostring(value)
            end
            table.insert(result, string.format("%s  %s = %s,\n", padding, key_str, value_str))
        end
    end
    
    table.insert(result, string.format("%s}", padding))
    return table.concat(result)
end

--- 打印表格（用于调试）
-- @param tbl 表格
-- @param name 表格名称（可选）
function table_utils.print(tbl, name)
    local prefix = name and name .. " = " or ""
    print(prefix .. table_utils.tostring(tbl))
end

--------------------------------------------------------------------------------
-- 路径操作（用于嵌套表格）
--------------------------------------------------------------------------------

--- 获取嵌套值
-- @param tbl 表格
-- @param path 路径（如 "a.b.c" 或 {"a", "b", "c"}）
-- @param default 默认值（如果路径不存在）
-- @return 值
function table_utils.get(tbl, path, default)
    if type(path) == "string" then
        local keys = {}
        for key in string.gmatch(path, "[^.]+") do
            table.insert(keys, key)
        end
        path = keys
    end
    
    local current = tbl
    for _, key in ipairs(path) do
        if type(current) ~= "table" then
            return default
        end
        current = current[key]
        if current == nil then
            return default
        end
    end
    
    return current
end

--- 设置嵌套值
-- @param tbl 表格
-- @param path 路径（如 "a.b.c" 或 {"a", "b", "c"}）
-- @param value 要设置的值
-- @return 原表格
function table_utils.set(tbl, path, value)
    if type(path) == "string" then
        local keys = {}
        for key in string.gmatch(path, "[^.]+") do
            table.insert(keys, key)
        end
        path = keys
    end
    
    local current = tbl
    for i = 1, #path - 1 do
        local key = path[i]
        if type(current[key]) ~= "table" then
            current[key] = {}
        end
        current = current[key]
    end
    
    current[path[#path]] = value
    return tbl
end

--- 删除嵌套值
-- @param tbl 表格
-- @param path 路径（如 "a.b.c" 或 {"a", "b", "c"}）
-- @return 删除的值
function table_utils.delete(tbl, path)
    if type(path) == "string" then
        local keys = {}
        for key in string.gmatch(path, "[^.]+") do
            table.insert(keys, key)
        end
        path = keys
    end
    
    local current = tbl
    for i = 1, #path - 1 do
        if type(current[path[i]]) ~= "table" then
            return nil
        end
        current = current[path[i]]
    end
    
    local key = path[#path]
    local value = current[key]
    current[key] = nil
    return value
end

--------------------------------------------------------------------------------
-- 验证
--------------------------------------------------------------------------------

--- 检查是否为数组（纯数字索引）
-- @param tbl 表格
-- @return 如果是数组返回 true
function table_utils.isarray(tbl)
    if type(tbl) ~= "table" then
        return false
    end
    
    local i = 0
    for _ in pairs(tbl) do
        i = i + 1
        if tbl[i] == nil then
            return false
        end
    end
    return true
end

--- 检查是否为关联数组
-- @param tbl 表格
-- @return 如果是关联数组返回 true
function table_utils.isassociative(tbl)
    if type(tbl) ~= "table" then
        return false
    end
    
    if next(tbl) == nil then
        return false
    end
    
    for key in pairs(tbl) do
        if type(key) ~= "number" or key < 1 or key ~= math.floor(key) then
            return true
        end
    end
    
    return false
end

return table_utils

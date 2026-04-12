-- Table Utils 数据处理示例
-- 展示实际数据处理场景中的应用

local table_utils = require("mod")

print("=== Table Utils 数据处理示例 ===\n")

--------------------------------------------------------------------------------
-- 场景 1: 用户数据分析和转换
--------------------------------------------------------------------------------

print("场景 1: 用户数据分析和转换\n")

local users = {
    {id = 1, name = "Alice", age = 25, email = "alice@example.com", active = true, score = 85},
    {id = 2, name = "Bob", age = 30, email = "bob@example.com", active = true, score = 92},
    {id = 3, name = "Charlie", age = 35, email = "charlie@example.com", active = false, score = 78},
    {id = 4, name = "David", age = 28, email = "david@example.com", active = true, score = 88},
    {id = 5, name = "Eve", age = 32, email = "eve@example.com", active = true, score = 95},
    {id = 6, name = "Frank", age = 45, email = "frank@example.com", active = false, score = 70},
    {id = 7, name = "Grace", age = 22, email = "grace@example.com", active = true, score = 91},
    {id = 8, name = "Henry", age = 38, email = "henry@example.com", active = true, score = 82}
}

-- 1. 筛选活跃用户
local active_users = table_utils.filter(users, function(u) return u.active end)
print("活跃用户数量:", #active_users)

-- 2. 计算平均分数
local total_score = table_utils.reduce(active_users, function(sum, u) 
    return sum + u.score 
end, 0)
local avg_score = total_score / #active_users
print(string.format("活跃用户平均分数：%.2f", avg_score))

-- 3. 按年龄段分组
local age_groups = table_utils.groupby(users, function(u)
    if u.age < 25 then return "青年 (<25)"
    elseif u.age < 35 then return "中年 (25-34)"
    elseif u.age < 45 then return "中老年 (35-44)"
    else return "老年 (45+)"
    end
end)

print("\n年龄分布:")
for group, members in pairs(age_groups) do
    print(string.format("  %s: %d 人", group, #members))
end

-- 4. 提取用户姓名列表
local names = table_utils.map(users, function(u) return u.name end)
print("\n所有用户:", table_utils.join(table_utils.values(names), ", "))

-- 5. 按分数排序
local sorted_by_score = table_utils.sortby(users, "score", false)  -- 降序
print("\n分数排名前三:")
for i = 1, math.min(3, #sorted_by_score) do
    local u = sorted_by_score[i]
    print(string.format("  %d. %s - %d 分", i, u.name, u.score))
end

-- 6. 查找最高分用户
local top_scorer = table_utils.find(users, function(u) 
    return u.score >= 95 
end)
print(string.format("\n最高分用户：%s (%d 分)", top_scorer.name, top_scorer.score))

-- 7. 检查是否有用户分数低于 75
local has_low_scorer = table_utils.some(users, function(u) 
    return u.score < 75 
end)
print("是否有用户分数低于 75:", has_low_scorer and "是" or "否")

-- 8. 检查所有活跃用户分数是否都大于 80
local all_active_high = table_utils.every(active_users, function(u) 
    return u.score > 80 
end)
print("所有活跃用户分数都大于 80:", all_active_high and "是" or "否")

-- 9. 创建用户摘要
local summary = table_utils.map(users, function(u)
    return {
        display_name = string.format("%s (%s)", u.name, u.active and "活跃" or " inactive"),
        age_group = u.age < 30 and "年轻" or "成熟",
        performance = u.score >= 90 and "优秀" or (u.score >= 80 and "良好" or "一般")
    }
end)

print("\n用户摘要（前 3 个）:")
for i = 1, 3 do
    local s = summary[i]
    print(string.format("  %s - %s - %s", s.display_name, s.age_group, s.performance))
end

--------------------------------------------------------------------------------
-- 场景 2: 订单数据处理
--------------------------------------------------------------------------------

print("\n\n场景 2: 订单数据处理\n")

local orders = {
    {id = "ORD001", customer = "Alice", amount = 150.00, status = "completed", items = 3},
    {id = "ORD002", customer = "Bob", amount = 89.50, status = "pending", items = 2},
    {id = "ORD003", customer = "Charlie", amount = 234.00, status = "completed", items = 5},
    {id = "ORD004", customer = "Alice", amount = 67.00, status = "cancelled", items = 1},
    {id = "ORD005", customer = "David", amount = 445.00, status = "completed", items = 8},
    {id = "ORD006", customer = "Eve", amount = 123.50, status = "pending", items = 3},
    {id = "ORD007", customer = "Bob", amount = 78.00, status = "completed", items = 2},
    {id = "ORD008", customer = "Frank", amount = 567.00, status = "completed", items = 10}
}

-- 1. 按状态分组
local orders_by_status = table_utils.groupby(orders, function(o) return o.status end)

print("订单状态分布:")
for status, order_list in pairs(orders_by_status) do
    local total = table_utils.reduce(order_list, function(sum, o) return sum + o.amount end, 0)
    print(string.format("  %s: %d 单，总金额 ¥%.2f", status, #order_list, total))
end

-- 2. 计算每个客户的总消费
local customer_totals = {}
for _, order in ipairs(orders) do
    if not customer_totals[order.customer] then
        customer_totals[order.customer] = 0
    end
    customer_totals[order.customer] = customer_totals[order.customer] + order.amount
end

print("\n客户消费排行:")
local sorted_customers = table_utils.sortby(
    table_utils.map(customer_totals, function(amount, name) 
        return {name = name, total = amount} 
    end),
    "total",
    false
)
for i, c in ipairs(sorted_customers) do
    print(string.format("  %d. %s: ¥%.2f", i, c.name, c.total))
end

-- 3. 筛选大额订单（>100）
local large_orders = table_utils.filter(orders, function(o) return o.amount > 100 end)
print(string.format("\n大额订单数量：%d", #large_orders))

-- 4. 计算平均订单金额
local total_amount = table_utils.reduce(orders, function(sum, o) return sum + o.amount end, 0)
local avg_amount = total_amount / #orders
print(string.format("平均订单金额：¥%.2f", avg_amount))

-- 5. 统计商品总数
local total_items = table_utils.reduce(orders, function(sum, o) return sum + o.items end, 0)
print(string.format("销售商品总数：%d 件", total_items))

--------------------------------------------------------------------------------
-- 场景 3: 日志数据分析
--------------------------------------------------------------------------------

print("\n\n场景 3: 日志数据分析\n")

local logs = {
    {time = "2024-01-01 10:00", level = "INFO", message = "Server started", source = "main"},
    {time = "2024-01-01 10:05", level = "DEBUG", message = "Loading config", source = "config"},
    {time = "2024-01-01 10:06", level = "INFO", message = "Config loaded", source = "config"},
    {time = "2024-01-01 10:10", level = "WARN", message = "High memory usage", source = "monitor"},
    {time = "2024-01-01 10:15", level = "ERROR", message = "Connection failed", source = "network"},
    {time = "2024-01-01 10:16", level = "INFO", message = "Retrying connection", source = "network"},
    {time = "2024-01-01 10:17", level = "INFO", message = "Connection established", source = "network"},
    {time = "2024-01-01 10:20", level = "DEBUG", message = "Processing request", source = "api"},
    {time = "2024-01-01 10:21", level = "INFO", message = "Request completed", source = "api"},
    {time = "2024-01-01 10:25", level = "ERROR", message = "Database timeout", source = "db"},
    {time = "2024-01-01 10:26", level = "WARN", message = "Fallback to cache", source = "db"},
    {time = "2024-01-01 10:30", level = "INFO", message = "Cache hit", source = "cache"}
}

-- 1. 按级别统计
local logs_by_level = table_utils.groupby(logs, function(l) return l.level end)

print("日志级别分布:")
for level, log_list in pairs(logs_by_level) do
    print(string.format("  %s: %d 条", level, #log_list))
end

-- 2. 按来源统计
local logs_by_source = table_utils.groupby(logs, function(l) return l.source end)

print("\n日志来源分布:")
for source, log_list in pairs(logs_by_source) do
    print(string.format("  %s: %d 条", source, #log_list))
end

-- 3. 提取错误和警告
local issues = table_utils.filter(logs, function(l) 
    return l.level == "ERROR" or l.level == "WARN" 
end)

print("\n问题日志:")
for _, log in ipairs(issues) do
    print(string.format("  [%s] %s: %s", log.level, log.source, log.message))
end

-- 4. 检查是否有错误
local has_errors = table_utils.some(logs, function(l) return l.level == "ERROR" end)
print(string.format("\n存在错误日志：%s", has_errors and "是" or "否"))

-- 5. 提取所有消息
local messages = table_utils.map(logs, function(l) return l.message end)
print(string.format("\n日志消息总数：%d", #messages))

--------------------------------------------------------------------------------
-- 场景 4: 数组数据处理
--------------------------------------------------------------------------------

print("\n\n场景 4: 数组数据处理\n")

local numbers = {5, 2, 8, 1, 9, 3, 7, 4, 6, 10}

print("原始数组:", table_utils.join(numbers, ", "))

-- 1. 排序
local sorted = table_utils.sort(numbers)
print("排序后:", table_utils.join(sorted, ", "))

-- 2. 反转
local reversed = table_utils.reverse(numbers)
print("反转后:", table_utils.join(reversed, ", "))

-- 3. 去重（虽然这里没有重复）
local with_dups = {1, 2, 2, 3, 3, 3, 4, 4, 5}
print("去重前:", table_utils.join(with_dups, ", "))
print("去重后:", table_utils.join(table_utils.unique(with_dups), ", "))

-- 4. 切片
print("切片 [3-6]:", table_utils.join(table_utils.slice(numbers, 3, 6), ", "))

-- 5. 展平嵌套数组
local nested = {1, {2, 3}, {4, {5, 6}}, {7, 8, {9, 10}}}
print("嵌套数组展平:", table_utils.join(table_utils.flatten(nested, 3), ", "))

-- 6. 创建范围
print("范围 1-10:", table_utils.join(table_utils.range(1, 10), ", "))
print("偶数范围:", table_utils.join(table_utils.range(0, 20, 2), ", "))

-- 7. 分区
local evens, odds = table_utils.partition(numbers, function(n) return n % 2 == 0 end)
print("偶数:", table_utils.join(evens, ", "))
print("奇数:", table_utils.join(odds, ", "))

-- 8. 查找
print("数字 5 的索引:", table_utils.indexof(numbers, 5))
print("是否包含 7:", table_utils.includes(numbers, 7) and "是" or "否")

-- 9. 集合操作
local set_a = {1, 2, 3, 4, 5}
local set_b = {4, 5, 6, 7, 8}
print("集合 A:", table_utils.join(set_a, ", "))
print("集合 B:", table_utils.join(set_b, ", "))
print("A ∪ B:", table_utils.join(table_utils.union(set_a, set_b), ", "))
print("A ∩ B:", table_utils.join(table_utils.intersection(set_a, set_b), ", "))
print("A - B:", table_utils.join(table_utils.difference(set_a, set_b), ", "))

print("\n=== 数据处理示例结束 ===")

-- Table Utils 基本用法示例
-- 展示最常用的功能

local table_utils = require("mod")

print("=== Table Utils 基本用法示例 ===\n")

--------------------------------------------------------------------------------
-- 1. 深度复制
--------------------------------------------------------------------------------

print("1. 深度复制")
local original = {
    name = "Alice",
    age = 30,
    skills = {"Lua", "Python", "JavaScript"},
    address = {
        city = "Beijing",
        district = "Chaoyang"
    }
}

local copy = table_utils.deepcopy(original)
copy.age = 31
copy.address.city = "Shanghai"

print("原表格:", original.age, original.address.city)  -- 30, Beijing
print("副本:", copy.age, copy.address.city)            -- 31, Shanghai
print()

--------------------------------------------------------------------------------
-- 2. 合并表格
--------------------------------------------------------------------------------

print("2. 合并表格")
local defaults = {
    host = "localhost",
    port = 8080,
    timeout = 30
}

local config = {
    port = 3000,
    debug = true
}

local merged = table_utils.merge(defaults, config)
print("合并后配置:")
table_utils.print(merged)
print()

--------------------------------------------------------------------------------
-- 3. 过滤和映射
--------------------------------------------------------------------------------

print("3. 过滤和映射")
local numbers = {a = 1, b = 2, c = 3, d = 4, e = 5, f = 6}

-- 过滤偶数
local evens = table_utils.filter(numbers, function(v) 
    return v % 2 == 0 
end)
print("偶数:", table_utils.join(table_utils.values(evens), ", "))

-- 映射：乘以 10
local times10 = table_utils.map(numbers, function(v) 
    return v * 10 
end)
print("乘以 10:", table_utils.join(table_utils.values(times10), ", "))

-- 归约：求和
local sum = table_utils.reduce(numbers, function(acc, v) 
    return acc + v 
end, 0)
print("总和:", sum)
print()

--------------------------------------------------------------------------------
-- 4. 数组操作
--------------------------------------------------------------------------------

print("4. 数组操作")
local arr = {1, 2, 2, 3, 3, 3, 4, 5}

print("原数组:", table_utils.join(arr, ", "))
print("去重后:", table_utils.join(table_utils.unique(arr), ", "))

local nested = {1, {2, 3}, {4, {5, 6}}}
print("展平 (1 层):", table_utils.join(table_utils.flatten(nested, 1), ", "))
print("展平 (2 层):", table_utils.join(table_utils.flatten(nested, 2), ", "))

local sliced = table_utils.slice(arr, 3, 5)
print("切片 [3-5]:", table_utils.join(sliced, ", "))
print()

--------------------------------------------------------------------------------
-- 5. 查找和搜索
--------------------------------------------------------------------------------

print("5. 查找和搜索")
local users = {
    {id = 1, name = "Alice", age = 25},
    {id = 2, name = "Bob", age = 30},
    {id = 3, name = "Charlie", age = 35},
    {id = 4, name = "David", age = 28}
}

-- 查找第一个年龄大于 28 的用户
local found = table_utils.find(users, function(u) 
    return u.age > 28 
end)
print("第一个年龄>28 的用户:", found and found.name or "未找到")

-- 检查是否包含某个 ID
local has_id_3 = table_utils.some(users, function(u) 
    return u.id == 3 
end)
print("是否存在 ID=3 的用户:", has_id_3)

-- 检查所有用户是否成年
local all_adults = table_utils.every(users, function(u) 
    return u.age >= 18 
end)
print("所有用户是否成年:", all_adults)
print()

--------------------------------------------------------------------------------
-- 6. 集合操作
--------------------------------------------------------------------------------

print("6. 集合操作")
local set1 = {1, 2, 3, 4, 5}
local set2 = {4, 5, 6, 7, 8}

print("集合 1:", table_utils.join(set1, ", "))
print("集合 2:", table_utils.join(set2, ", "))
print("并集:", table_utils.join(table_utils.union(set1, set2), ", "))
print("交集:", table_utils.join(table_utils.intersection(set1, set2), ", "))
print("差集 (1-2):", table_utils.join(table_utils.difference(set1, set2), ", "))
print()

--------------------------------------------------------------------------------
-- 7. 嵌套路径操作
--------------------------------------------------------------------------------

print("7. 嵌套路径操作")
local config_data = {
    database = {
        host = "localhost",
        port = 5432,
        credentials = {
            username = "admin",
            password = "secret"
        }
    },
    cache = {
        enabled = true,
        ttl = 3600
    }
}

-- 获取嵌套值
local db_host = table_utils.get(config_data, "database.host")
local username = table_utils.get(config_data, "database.credentials.username")
local missing = table_utils.get(config_data, "database.credentials.email", "N/A")

print("数据库主机:", db_host)
print("用户名:", username)
print("邮箱 (默认值):", missing)

-- 设置嵌套值
table_utils.set(config_data, "database.credentials.password", "new_secret")
table_utils.set(config_data, "logging.level", "debug")  -- 自动创建中间表格

print("\n更新后的配置:")
table_utils.print(config_data)
print()

--------------------------------------------------------------------------------
-- 8. 分组和分区
--------------------------------------------------------------------------------

print("8. 分组和分区")
local products = {
    {name = "Apple", category = "Fruit", price = 1.5},
    {name = "Banana", category = "Fruit", price = 0.8},
    {name = "Carrot", category = "Vegetable", price = 0.5},
    {name = "Broccoli", category = "Vegetable", price = 1.2},
    {name = "Milk", category = "Dairy", price = 2.0}
}

-- 按类别分组
local by_category = table_utils.groupby(products, function(p) 
    return p.category 
end)

print("按类别分组:")
for category, items in pairs(by_category) do
    local names = table_utils.map(items, function(i) return i.name end)
    print(string.format("  %s: %s", category, table_utils.join(table_utils.values(names), ", ")))
end

-- 分区：价格大于 1 和不大于 1
local expensive, cheap = table_utils.partition(products, function(p) 
    return p.price > 1 
end)

print("\n价格分区:")
print("  昂贵 (>1):", table_utils.join(table_utils.map(expensive, function(p) return p.name end), ", "))
print("  便宜 (≤1):", table_utils.join(table_utils.map(cheap, function(p) return p.name end), ", "))
print()

--------------------------------------------------------------------------------
-- 9. 实用工具
--------------------------------------------------------------------------------

print("9. 实用工具")
print("范围 1-5:", table_utils.join(table_utils.range(1, 5), ", "))
print("范围 0-10 步长 2:", table_utils.join(table_utils.range(0, 10, 2), ", "))
print("填充 5 个'x':", table_utils.join(table_utils.fill(5, "x"), ", "))
print("平方序列:", table_utils.join(table_utils.sequence(5, function(i) return i * i end), ", "))
print()

--------------------------------------------------------------------------------
-- 10. 类型检查
--------------------------------------------------------------------------------

print("10. 类型检查")
local array = {1, 2, 3, 4, 5}
local associative = {a = 1, b = 2, c = 3}

print("array 是数组吗？", table_utils.isarray(array))
print("array 是关联数组吗？", table_utils.isassociative(array))
print("associative 是数组吗？", table_utils.isarray(associative))
print("associative 是关联数组吗？", table_utils.isassociative(associative))
print()

print("=== 示例结束 ===")

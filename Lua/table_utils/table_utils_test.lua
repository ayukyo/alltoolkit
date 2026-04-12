-- Table Utils 测试套件
-- 全面的单元测试覆盖所有功能

local table_utils = require("mod")

-- 测试计数器
local tests_run = 0
local tests_passed = 0
local tests_failed = 0

-- 断言函数
local function assert_equal(expected, actual, message)
    tests_run = tests_run + 1
    if expected == actual then
        tests_passed = tests_passed + 1
        return true
    else
        tests_failed = tests_failed + 1
        print(string.format("❌ FAILED: %s", message or "Assertion failed"))
        print(string.format("   Expected: %s", tostring(expected)))
        print(string.format("   Actual:   %s", tostring(actual)))
        return false
    end
end

local function assert_true(condition, message)
    return assert_equal(true, condition, message)
end

local function assert_false(condition, message)
    return assert_equal(false, condition, message)
end

local function assert_nil(value, message)
    tests_run = tests_run + 1
    if value == nil then
        tests_passed = tests_passed + 1
        return true
    else
        tests_failed = tests_failed + 1
        print(string.format("❌ FAILED: %s", message or "Expected nil"))
        print(string.format("   Actual:   %s", tostring(value)))
        return false
    end
end

local function assert_table(expected, actual, message)
    tests_run = tests_run + 1
    local match = true
    
    if type(expected) ~= "table" or type(actual) ~= "table" then
        match = false
    else
        for k, v in pairs(expected) do
            if actual[k] ~= v then
                match = false
                break
            end
        end
        for k, v in pairs(actual) do
            if expected[k] ~= v then
                match = false
                break
            end
        end
    end
    
    if match then
        tests_passed = tests_passed + 1
        return true
    else
        tests_failed = tests_failed + 1
        print(string.format("❌ FAILED: %s", message or "Table assertion failed"))
        return false
    end
end

-- 打印测试标题
local function test_section(title)
    print(string.format("\n%s %s", string.rep("=", 60), title))
end

--------------------------------------------------------------------------------
-- 基本操作测试
--------------------------------------------------------------------------------

test_section("基本操作测试")

-- deepcopy 测试
do
    local original = {a = 1, b = {c = 2, d = {e = 3}}}
    local copy = table_utils.deepcopy(original)
    
    assert_equal(1, copy.a, "deepcopy 复制基本值")
    assert_equal(2, copy.b.c, "deepcopy 复制嵌套值")
    assert_equal(3, copy.b.d.e, "deepcopy 复制深层嵌套值")
    assert_true(original ~= copy, "deepcopy 创建新表格引用")
    assert_true(original.b ~= copy.b, "deepcopy 深度复制嵌套表格")
    
    -- 修改副本不应影响原表格
    copy.b.c = 999
    assert_equal(2, original.b.c, "deepcopy 修改副本不影响原表格")
end

-- shallowcopy 测试
do
    local original = {a = 1, b = {c = 2}}
    local copy = table_utils.shallowcopy(original)
    
    assert_equal(1, copy.a, "shallowcopy 复制基本值")
    assert_true(original.b == copy.b, "shallowcopy 嵌套表格共享引用")
end

-- isempty 测试
do
    assert_true(table_utils.isempty({}), "isempty 空表格返回 true")
    assert_false(table_utils.isempty({1, 2, 3}), "isempty 非空表格返回 false")
    assert_false(table_utils.isempty({a = 1}), "isempty 有关键值返回 false")
end

-- clear 测试
do
    local tbl = {a = 1, b = 2, c = 3}
    table_utils.clear(tbl)
    assert_true(table_utils.isempty(tbl), "clear 清空表格")
end

-- count 测试
do
    assert_equal(3, table_utils.count({a = 1, b = 2, c = 3}), "count 计算键值对数量")
    assert_equal(0, table_utils.count({}), "count 空表格返回 0")
end

--------------------------------------------------------------------------------
-- 合并操作测试
--------------------------------------------------------------------------------

test_section("合并操作测试")

-- merge 测试
do
    local t1 = {a = 1, b = 2}
    local t2 = {c = 3, d = 4}
    local t3 = {b = 99, e = 5}
    
    local result = table_utils.merge(t1, t2, t3)
    
    assert_equal(1, result.a, "merge 保留第一个表格的值")
    assert_equal(99, result.b, "merge 后面的表格覆盖前面的值")
    assert_equal(3, result.c, "merge 合并多个表格")
    assert_equal(5, result.e, "merge 包含所有键")
end

-- deepmerge 测试
do
    local t1 = {a = 1, b = {c = 2, d = 3}}
    local t2 = {b = {c = 99, e = 4}, f = 5}
    
    local result = table_utils.deepmerge(t1, t2)
    
    assert_equal(1, result.a, "deepmerge 保留顶层值")
    assert_equal(99, result.b.c, "deepmerge 深度合并嵌套表格")
    assert_equal(3, result.b.d, "deepmerge 保留未覆盖的嵌套值")
    assert_equal(4, result.b.e, "deepmerge 添加新的嵌套值")
    assert_equal(5, result.f, "deepmerge 添加顶层值")
end

-- update 测试
do
    local target = {a = 1, b = 2}
    local source = {b = 99, c = 3}
    
    table_utils.update(target, source)
    
    assert_equal(1, target.a, "update 保留原有值")
    assert_equal(99, target.b, "update 覆盖已有值")
    assert_equal(3, target.c, "update 添加新值")
end

--------------------------------------------------------------------------------
-- 转换操作测试
--------------------------------------------------------------------------------

test_section("转换操作测试")

-- keys 测试
do
    local tbl = {a = 1, b = 2, c = 3}
    local keys = table_utils.keys(tbl)
    
    assert_equal(3, #keys, "keys 返回所有键")
    assert_true(table_utils.includes(keys, "a"), "keys 包含键 a")
    assert_true(table_utils.includes(keys, "b"), "keys 包含键 b")
    assert_true(table_utils.includes(keys, "c"), "keys 包含键 c")
end

-- values 测试
do
    local tbl = {a = 1, b = 2, c = 3}
    local values = table_utils.values(tbl)
    
    assert_equal(3, #values, "values 返回所有值")
    assert_true(table_utils.includes(values, 1), "values 包含值 1")
    assert_true(table_utils.includes(values, 2), "values 包含值 2")
    assert_true(table_utils.includes(values, 3), "values 包含值 3")
end

-- invert 测试
do
    local tbl = {a = 1, b = 2, c = 3}
    local inverted = table_utils.invert(tbl)
    
    assert_equal("a", inverted[1], "invert 键值互换")
    assert_equal("b", inverted[2], "invert 键值互换")
    assert_equal("c", inverted[3], "invert 键值互换")
end

--------------------------------------------------------------------------------
-- 过滤和映射测试
--------------------------------------------------------------------------------

test_section("过滤和映射测试")

-- filter 测试
do
    local tbl = {a = 1, b = 2, c = 3, d = 4, e = 5}
    local filtered = table_utils.filter(tbl, function(v) return v % 2 == 1 end)
    
    assert_equal(1, filtered.a, "filter 保留奇数")
    assert_equal(3, filtered.c, "filter 保留奇数")
    assert_equal(5, filtered.e, "filter 保留奇数")
    assert_nil(filtered.b, "filter 移除偶数")
    assert_nil(filtered.d, "filter 移除偶数")
end

-- map 测试
do
    local tbl = {a = 1, b = 2, c = 3}
    local mapped = table_utils.map(tbl, function(v) return v * 2 end)
    
    assert_equal(2, mapped.a, "map 应用函数")
    assert_equal(4, mapped.b, "map 应用函数")
    assert_equal(6, mapped.c, "map 应用函数")
end

-- reduce 测试
do
    local tbl = {a = 1, b = 2, c = 3, d = 4}
    local sum = table_utils.reduce(tbl, function(acc, v) return acc + v end, 0)
    
    assert_equal(10, sum, "reduce 计算总和")
end

-- find 测试
do
    local tbl = {a = 1, b = 2, c = 3, d = 4}
    local value, key = table_utils.find(tbl, function(v) return v > 2 end)
    
    assert_equal(3, value, "find 找到第一个满足条件的值")
    assert_true(key == "c" or key == "d", "find 返回正确的键")
end

-- some 测试
do
    local tbl = {a = 1, b = 2, c = 3}
    assert_true(table_utils.some(tbl, function(v) return v > 2 end), "some 存在满足条件的值")
    assert_false(table_utils.some(tbl, function(v) return v > 10 end), "some 不存在满足条件的值")
end

-- every 测试
do
    local tbl = {a = 1, b = 2, c = 3}
    assert_true(table_utils.every(tbl, function(v) return v > 0 end), "every 所有值满足条件")
    assert_false(table_utils.every(tbl, function(v) return v > 1 end), "every 不是所有值满足条件")
end

--------------------------------------------------------------------------------
-- 数组操作测试
--------------------------------------------------------------------------------

test_section("数组操作测试")

-- push/pop 测试
do
    local tbl = {1, 2, 3}
    table_utils.push(tbl, 4)
    assert_equal(4, tbl[4], "push 添加元素到末尾")
    
    local popped = table_utils.pop(tbl)
    assert_equal(4, popped, "pop 移除并返回末尾元素")
    assert_equal(3, #tbl, "pop 后长度减少")
end

-- unshift/shift 测试
do
    local tbl = {2, 3, 4}
    table_utils.unshift(tbl, 1)
    assert_equal(1, tbl[1], "unshift 添加元素到开头")
    
    local shifted = table_utils.shift(tbl)
    assert_equal(1, shifted, "shift 移除并返回开头元素")
    assert_equal(2, tbl[1], "shift 后第二个元素变为第一个")
end

-- concat 测试
do
    local t1 = {1, 2, 3}
    local t2 = {4, 5, 6}
    local result = table_utils.concat(t1, t2)
    
    assert_equal(6, #result, "concat 连接两个数组")
    assert_equal(1, result[1], "concat 保留第一个数组的元素")
    assert_equal(6, result[6], "concat 保留第二个数组的元素")
end

-- slice 测试
do
    local tbl = {1, 2, 3, 4, 5}
    local sliced = table_utils.slice(tbl, 2, 4)
    
    assert_equal(3, #sliced, "slice 返回正确长度")
    assert_equal(2, sliced[1], "slice 从正确位置开始")
    assert_equal(4, sliced[3], "slice 在正确位置结束")
end

-- join 测试
do
    local tbl = {"a", "b", "c"}
    local result = table_utils.join(tbl, ", ")
    assert_equal("a, b, c", result, "join 用分隔符连接")
    
    result = table_utils.join(tbl, "-")
    assert_equal("a-b-c", result, "join 使用自定义分隔符")
end

-- unique 测试
do
    local tbl = {1, 2, 2, 3, 3, 3, 4}
    local result = table_utils.unique(tbl)
    
    assert_equal(4, #result, "unique 移除重复元素")
    assert_table({1, 2, 3, 4}, result, "unique 保留唯一值")
end

-- flatten 测试
do
    local tbl = {1, {2, 3}, {4, {5, 6}}}
    local result = table_utils.flatten(tbl, 1)
    -- 展平一层：{1, 2, 3, 4, {5, 6}}
    assert_equal(5, #result, "flatten 展平一层后长度正确")
    assert_equal(1, result[1], "flatten 保留非表格元素")
    assert_equal(2, result[2], "flatten 展平第一层嵌套")
    assert_equal(3, result[3], "flatten 展平第一层嵌套")
    assert_equal(4, result[4], "flatten 展平第一层嵌套")
    assert_true(type(result[5]) == "table", "flatten 保留第二层嵌套为表格")
    
    result = table_utils.flatten(tbl, 2)
    -- 展平两层：{1, 2, 3, 4, 5, 6}
    assert_equal(6, #result, "flatten 展平多层后长度正确")
    assert_equal(1, result[1], "flatten 展平多层")
    assert_equal(6, result[6], "flatten 展平多层")
end

-- compact 测试
do
    -- 构建一个带 nil 的数组
    local tbl = {1, 2, 3, 4, 5}
    tbl[3] = nil  -- 手动设置 nil
    local result = table_utils.compact(tbl)
    assert_equal(4, #result, "compact 移除 nil 值后长度正确")
    assert_equal(1, result[1], "compact 保留第一个元素")
    assert_equal(2, result[2], "compact 保留第二个元素")
    assert_equal(4, result[3], "compact 跳过 nil 后的元素")
    assert_equal(5, result[4], "compact 保留最后一个元素")
end

--------------------------------------------------------------------------------
-- 排序操作测试
--------------------------------------------------------------------------------

test_section("排序操作测试")

-- sort 测试
do
    local tbl = {3, 1, 4, 1, 5, 9, 2, 6}
    local result = table_utils.sort(tbl)
    
    assert_equal(1, result[1], "sort 升序排序")
    assert_equal(9, result[8], "sort 升序排序")
end

-- sortby 测试
do
    local tbl = {
        {name = "Alice", age = 30},
        {name = "Bob", age = 25},
        {name = "Charlie", age = 35}
    }
    
    local result = table_utils.sortby(tbl, "age")
    assert_equal(25, result[1].age, "sortby 按年龄升序")
    assert_equal(35, result[3].age, "sortby 按年龄升序")
    
    result = table_utils.sortby(tbl, "age", false)
    assert_equal(35, result[1].age, "sortby 按年龄降序")
end

-- reverse 测试
do
    local tbl = {1, 2, 3, 4, 5}
    local result = table_utils.reverse(tbl)
    
    assert_equal(5, result[1], "reverse 反转数组")
    assert_equal(1, result[5], "reverse 反转数组")
end

--------------------------------------------------------------------------------
-- 搜索和查找测试
--------------------------------------------------------------------------------

test_section("搜索和查找测试")

-- indexof 测试
do
    local tbl = {"a", "b", "c", "d"}
    assert_equal(1, table_utils.indexof(tbl, "a"), "indexof 找到第一个元素")
    assert_equal(3, table_utils.indexof(tbl, "c"), "indexof 找到中间元素")
    assert_nil(table_utils.indexof(tbl, "z"), "indexof 未找到返回 nil")
end

-- includes 测试
do
    local tbl = {1, 2, 3, 4, 5}
    assert_true(table_utils.includes(tbl, 3), "includes 找到元素")
    assert_false(table_utils.includes(tbl, 10), "includes 未找到元素")
end

-- haskey 测试
do
    local tbl = {a = 1, b = 2, c = 3}
    assert_true(table_utils.haskey(tbl, "b"), "haskey 找到键")
    assert_false(table_utils.haskey(tbl, "z"), "haskey 未找到键")
end

--------------------------------------------------------------------------------
-- 集合操作测试
--------------------------------------------------------------------------------

test_section("集合操作测试")

-- union 测试
do
    local t1 = {1, 2, 3, 4}
    local t2 = {3, 4, 5, 6}
    local result = table_utils.union(t1, t2)
    
    assert_equal(6, #result, "union 并集包含所有唯一元素")
    for i = 1, 6 do
        assert_true(table_utils.includes(result, i), "union 包含元素 " .. i)
    end
end

-- intersection 测试
do
    local t1 = {1, 2, 3, 4}
    local t2 = {3, 4, 5, 6}
    local result = table_utils.intersection(t1, t2)
    
    assert_equal(2, #result, "intersection 交集只包含共同元素")
    assert_true(table_utils.includes(result, 3), "intersection 包含 3")
    assert_true(table_utils.includes(result, 4), "intersection 包含 4")
end

-- difference 测试
do
    local t1 = {1, 2, 3, 4}
    local t2 = {3, 4, 5, 6}
    local result = table_utils.difference(t1, t2)
    
    assert_equal(2, #result, "difference 差集只包含 t1 独有的元素")
    assert_true(table_utils.includes(result, 1), "difference 包含 1")
    assert_true(table_utils.includes(result, 2), "difference 包含 2")
end

--------------------------------------------------------------------------------
-- 实用工具测试
--------------------------------------------------------------------------------

test_section("实用工具测试")

-- range 测试
do
    local result = table_utils.range(1, 5)
    assert_table({1, 2, 3, 4, 5}, result, "range 创建范围数组")
    
    result = table_utils.range(0, 10, 2)
    assert_table({0, 2, 4, 6, 8, 10}, result, "range 使用步长")
end

-- fill 测试
do
    local result = table_utils.fill(5, "x")
    assert_equal(5, #result, "fill 创建指定长度数组")
    for i = 1, 5 do
        assert_equal("x", result[i], "fill 填充相同值")
    end
end

-- groupby 测试
do
    local tbl = {
        {name = "Alice", group = "A"},
        {name = "Bob", group = "B"},
        {name = "Charlie", group = "A"},
        {name = "David", group = "B"}
    }
    
    local result = table_utils.groupby(tbl, function(item) return item.group end)
    
    assert_equal(2, #result.A, "groupby 正确分组 A")
    assert_equal(2, #result.B, "groupby 正确分组 B")
end

-- partition 测试
do
    local tbl = {1, 2, 3, 4, 5, 6}
    local pass, fail = table_utils.partition(tbl, function(v) return v % 2 == 0 end)
    
    assert_equal(3, #pass, "partition 偶数数组长度正确")
    assert_equal(3, #fail, "partition 奇数数组长度正确")
    assert_true(table_utils.includes(pass, 2), "partition 偶数在 pass 中")
    assert_true(table_utils.includes(fail, 1), "partition 奇数在 fail 中")
end

--------------------------------------------------------------------------------
-- 路径操作测试
--------------------------------------------------------------------------------

test_section("路径操作测试")

-- get 测试
do
    local tbl = {a = {b = {c = 123}}}
    
    assert_equal(123, table_utils.get(tbl, "a.b.c"), "get 获取嵌套值（字符串路径）")
    assert_equal(123, table_utils.get(tbl, {"a", "b", "c"}), "get 获取嵌套值（数组路径）")
    assert_equal("default", table_utils.get(tbl, "a.b.x", "default"), "get 路径不存在返回默认值")
end

-- set 测试
do
    local tbl = {a = {b = {}}}
    table_utils.set(tbl, "a.b.c", 123)
    assert_equal(123, tbl.a.b.c, "set 设置嵌套值")
    
    table_utils.set(tbl, "x.y.z", 456)
    assert_equal(456, tbl.x.y.z, "set 创建中间表格")
end

-- delete 测试
do
    local tbl = {a = {b = {c = 123, d = 456}}}
    local deleted = table_utils.delete(tbl, "a.b.c")
    
    assert_equal(123, deleted, "delete 返回删除的值")
    assert_nil(tbl.a.b.c, "delete 移除嵌套值")
    assert_equal(456, tbl.a.b.d, "delete 保留其他值")
end

--------------------------------------------------------------------------------
-- 类型检查测试
--------------------------------------------------------------------------------

test_section("类型检查测试")

-- isarray 测试
do
    assert_true(table_utils.isarray({1, 2, 3}), "isarray 纯数字索引返回 true")
    assert_false(table_utils.isarray({a = 1, b = 2}), "isarray 关联数组返回 false")
    assert_true(table_utils.isarray({}), "isarray 空表格返回 true")
end

-- isassociative 测试
do
    assert_true(table_utils.isassociative({a = 1, b = 2}), "isassociative 关联数组返回 true")
    assert_false(table_utils.isassociative({1, 2, 3}), "isassociative 数组返回 false")
    assert_false(table_utils.isassociative({}), "isassociative 空表格返回 false")
end

--------------------------------------------------------------------------------
-- 打印测试结果
--------------------------------------------------------------------------------

print("\n" .. string.rep("=", 60))
print("测试结果汇总")
print(string.rep("=", 60))
print(string.format("运行测试：%d", tests_run))
print(string.format("通过测试：%d ✅", tests_passed))
print(string.format("失败测试：%d ❌", tests_failed))
print(string.format("通过率：%.1f%%", (tests_passed / tests_run) * 100))

if tests_failed == 0 then
    print("\n🎉 所有测试通过！")
    os.exit(0)
else
    print("\n⚠️  存在失败的测试，请检查输出。")
    os.exit(1)
end

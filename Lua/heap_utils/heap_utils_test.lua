#!/usr/bin/env lua
--[[
    heap_utils 测试套件
]]

local heap_utils = require("mod")

local function assert_equal(a, b, msg)
    if a ~= b then
        error(string.format("FAILED: %s\nexpected: %s\ngot: %s", msg, tostring(b), tostring(a)))
    end
end

local function assert_true(cond, msg)
    if not cond then
        error(string.format("FAILED: %s", msg))
    end
end

print("=== 基本功能测试 ===")

-- max_heap
do
    local h = heap_utils.max_heap()
    h:push(3)
    h:push(1)
    h:push(5)
    h:push(2)
    h:push(4)

    assert_equal(h:top(), 5, "max_heap top")
    assert_equal(h:pop(), 5, "max_heap pop 1")
    assert_equal(h:pop(), 4, "max_heap pop 2")
    assert_equal(h:pop(), 3, "max_heap pop 3")
    assert_equal(h:pop(), 2, "max_heap pop 4")
    assert_equal(h:pop(), 1, "max_heap pop 5")
    assert_true(h:empty(), "max_heap empty")
    print("  max_heap: PASS")
end

-- min_heap
do
    local h = heap_utils.min_heap()
    h:push(3)
    h:push(1)
    h:push(5)
    h:push(2)
    h:push(4)

    assert_equal(h:top(), 1, "min_heap top")
    assert_equal(h:pop(), 1, "min_heap pop 1")
    assert_equal(h:pop(), 2, "min_heap pop 2")
    assert_equal(h:pop(), 3, "min_heap pop 3")
    assert_equal(h:pop(), 4, "min_heap pop 4")
    assert_equal(h:pop(), 5, "min_heap pop 5")
    assert_true(h:empty(), "min_heap empty")
    print("  min_heap: PASS")
end

-- heapify
do
    local arr = { 3, 1, 5, 2, 4 }
    local h = heap_utils.max_heapify(arr)
    assert_equal(h:top(), 5, "max_heapify top")
    assert_equal(h:pop(), 5, "max_heapify pop")
    print("  heapify: PASS")
end

-- heapsort
do
    local arr = { 3, 1, 5, 2, 4 }
    local sorted = heap_utils.heapsort_copy(arr)
    local expected = { 1, 2, 3, 4, 5 }
    for i = 1, 5 do
        assert_equal(sorted[i], expected[i], "heapsort element")
    end
    print("  heapsort: PASS")
end

print("\n=== 优先级队列测试 ===")

do
    local pq = heap_utils.priority_queue()
    pq:push(10)
    pq:push(5)
    pq:push(20)
    pq:push(1)

    assert_equal(pq:top(), 1, "pq top")
    assert_equal(pq:pop(), 1, "pq pop 1")
    assert_equal(pq:pop(), 5, "pq pop 2")
    assert_equal(pq:pop(), 10, "pq pop 3")
    assert_equal(pq:pop(), 20, "pq pop 4")
    print("  priority_queue: PASS")
end

print("\n=== K-th 元素测试 ===")

do
    local arr = { 7, 10, 4, 3, 20, 15 }
    local k3 = heap_utils.kth_largest(arr, 3)
    assert_equal(k3, 10, "kth_largest k=3 (3rd largest=10)")

    local k4 = heap_utils.kth_smallest(arr, 4)
    assert_equal(k4, 10, "kth_smallest k=4 (4th smallest=10)")
    print("  kth elements: PASS")
end

print("\n=== 自定义比较函数测试 ===")

do
    -- 字符串长度比较
    local h = heap_utils.max_heap(function(a, b)
        local la, lb = #a, #b
        if la < lb then return -1
        elseif la > lb then return 1
        else return 0 end
    end)

    h:push("hello")
    h:push("world")
    h:push("hi")
    h:push("lua")

    assert_equal(h:top(), "hello", "string heap top (longest)")
    assert_equal(h:pop(), "hello", "string heap pop")
    assert_equal(h:pop(), "world", "string heap pop")
    assert_equal(h:pop(), "lua", "string heap pop")
    print("  custom comparator: PASS")
end

print("\n=== 中位数测试 ===")

do
    local arr = { 12.0, 4.5, 6.4, 8.1, 1.9, 3.3 }
    local med = heap_utils.median(arr)
    assert_true(math.abs(med - 5.45) < 0.01, "median")
    print("  median: PASS")
end

print("\n=== 合并测试 ===")

do
    local h1 = heap_utils.min_heap()
    h1:push(1)
    h1:push(5)

    local h2 = heap_utils.min_heap()
    h2:push(2)
    h2:push(6)

    local merged = heap_utils.merge(h1, h2)
    assert_equal(merged:top(), 1, "merged top")
    assert_equal(merged:pop(), 1, "merged pop")
    assert_equal(merged:pop(), 2, "merged pop")
    print("  merge: PASS")
end

print("\n=== 边界情况测试 ===")

do
    local h = heap_utils.min_heap()

    -- 空堆
    assert_equal(h:top(), nil, "empty top")
    local v, ok = h:pop()
    assert_equal(v, nil, "empty pop")
    assert_true(not ok, "empty pop ok")

    -- 单元素
    h:push(42)
    assert_equal(h:top(), 42, "single top")
    assert_equal(h:pop(), 42, "single pop")
    assert_true(h:empty(), "single empty")
    print("  edge cases: PASS")
end

print("\n=== 全部测试通过 ===")
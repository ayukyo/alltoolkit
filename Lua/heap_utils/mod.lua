--[[
    heap_utils.lua - 堆数据结构实现

    提供最大堆、最小堆、堆排序和优先级队列功能。
    支持自定义比较函数和泛型类型。

    特性：
    - 最大堆和最小堆
    - 堆排序
    - 优先级队列
    - 自定义比较函数
    - 零外部依赖

    License: MIT
    Author: AllToolkit
    Version: 1.0.0
]]

local heap_utils = {}

heap_utils._VERSION = "1.0.0"

--------------------------------------------------------------------------------
-- 私有辅助函数
--------------------------------------------------------------------------------

--- 交换两个元素的位置
local function swap(data, a, b)
    data[a], data[b] = data[b], data[a]
end

--- 上浮操作 - 维护堆性质（sentinel = nil，不会被交换）
local function sift_up(data, size, compare, is_max)
    local index = size
    while index > 1 do
        local parent = math.floor(index / 2)
        local should_swap
        if is_max then
            should_swap = compare(data[index], data[parent]) > 0
        else
            should_swap = compare(data[index], data[parent]) < 0
        end
        if not should_swap then
            break
        end
        swap(data, index, parent)
        index = parent
    end
end

--- 下沉操作 - 维护堆性质
local function sift_down(data, index, heap_end, compare, is_max)
    while true do
        local left = 2 * index
        local right = 2 * index + 1
        local largest_or_smallest = index

        if left <= heap_end then
            if is_max then
                if compare(data[left], data[largest_or_smallest]) > 0 then
                    largest_or_smallest = left
                end
            else
                if compare(data[left], data[largest_or_smallest]) < 0 then
                    largest_or_smallest = left
                end
            end
        end

        if right <= heap_end then
            if is_max then
                if compare(data[right], data[largest_or_smallest]) > 0 then
                    largest_or_smallest = right
                end
            else
                if compare(data[right], data[largest_or_smallest]) < 0 then
                    largest_or_smallest = right
                end
            end
        end

        if largest_or_smallest ~= index then
            swap(data, index, largest_or_smallest)
            index = largest_or_smallest
        else
            break
        end
    end
end

--------------------------------------------------------------------------------
-- Heap 构造函数
--------------------------------------------------------------------------------

--- 创建堆实例（index 0 作为 sentinel，使用 nil）
local function new_heap(is_max, compare)
    local instance = {
        _data = { [0] = nil },  -- index 0 = sentinel (nil,不会被交换)
        _size = 0,
        _compare = compare or function(a, b)
            if a < b then return -1
            elseif a > b then return 1
            else return 0 end
        end,
        _is_max = is_max
    }

    function instance:push(value)
        self._size = self._size + 1
        self._data[self._size] = value
        sift_up(self._data, self._size, self._compare, self._is_max)
    end

    function instance:pop()
        if self._size == 0 then
            return nil, false
        end
        local top = self._data[1]
        self._data[1] = self._data[self._size]
        self._size = self._size - 1
        if self._size > 0 then
            sift_down(self._data, 1, self._size, self._compare, self._is_max)
        end
        return top, true
    end

    function instance:top()
        if self._size == 0 then
            return nil, false
        end
        return self._data[1], true
    end

    function instance:empty()
        return self._size == 0
    end

    function instance:size()
        return self._size
    end

    function instance:to_array()
        local result = {}
        for i = 1, self._size do
            result[i] = self._data[i]
        end
        return result
    end

    function instance:sort()
        local result = {}
        local size = self._size
        for i = 1, size do
            result[i] = self._data[1]
            self._data[1] = self._data[self._size]
            self._size = self._size - 1
            if self._size > 0 then
                sift_down(self._data, 1, self._size, self._compare, self._is_max)
            end
        end
        self._size = size
        return result
    end

    return instance
end

--------------------------------------------------------------------------------
-- 公共 API
--------------------------------------------------------------------------------

--- 创建最大堆
function heap_utils.max_heap(compare)
    return new_heap(true, compare)
end

--- 创建最小堆
function heap_utils.min_heap(compare)
    return new_heap(false, compare)
end

--- 从数组构建最大堆（Heapify，O(n)）
function heap_utils.max_heapify(arr, compare)
    local h = new_heap(true, compare or function(a, b)
        if a < b then return -1 elseif a > b then return 1 else return 0 end
    end)

    for i = 1, #arr do
        h._data[i] = arr[i]
    end
    h._size = #arr

    for i = math.floor(h._size / 2), 1, -1 do
        sift_down(h._data, i, h._size, h._compare, h._is_max)
    end

    return h
end

--- 从数组构建最小堆（Heapify，O(n)）
function heap_utils.min_heapify(arr, compare)
    local h = new_heap(false, compare or function(a, b)
        if a < b then return -1 elseif a > b then return 1 else return 0 end
    end)

    for i = 1, #arr do
        h._data[i] = arr[i]
    end
    h._size = #arr

    for i = math.floor(h._size / 2), 1, -1 do
        sift_down(h._data, i, h._size, h._compare, h._is_max)
    end

    return h
end

--- 堆排序（升序，使用最大堆）- 会修改原数组
function heap_utils.heapsort(arr, compare)
    if #arr <= 1 then
        return arr
    end

    local cmp = compare or function(a, b)
        if a < b then return -1 elseif a > b then return 1 else return 0 end
    end

    local n = #arr

    -- 构建最大堆
    for i = math.floor(n / 2), 1, -1 do
        sift_down(arr, i, n, cmp, true)
    end

    -- 逐个提取元素
    for i = n, 2, -1 do
        swap(arr, 1, i)
        sift_down(arr, 1, i - 1, cmp, true)
    end

    return arr
end

--- 堆排序（返回排序后的副本）
function heap_utils.heapsort_copy(arr, compare)
    local copy = {}
    for i = 1, #arr do
        copy[i] = arr[i]
    end
    return heap_utils.heapsort(copy, compare)
end

--- 创建优先级队列（基于最小堆）
function heap_utils.priority_queue(compare)
    return new_heap(false, compare or function(a, b)
        if a < b then return -1 elseif a > b then return 1 else return 0 end
    end)
end

--- 合并多个堆
function heap_utils.merge(...)
    local h = new_heap(false, function(a, b) return a - b end)
    for _, heap in ipairs({ ... }) do
        local arr = heap:to_array()
        for _, v in ipairs(arr) do
            h:push(v)
        end
    end
    return h
end

--- 获取第 K 大的元素（维护大小为 k 的最小堆）
function heap_utils.kth_largest(arr, k, compare)
    if k < 1 or k > #arr then
        return nil, false
    end

    local cmp = compare or function(a, b)
        if a < b then return -1 elseif a > b then return 1 else return 0 end
    end

    local h = new_heap(false, cmp)

    for i = 1, #arr do
        if h._size < k then
            h:push(arr[i])
        else
            if cmp(arr[i], h._data[1]) > 0 then
                h._data[1] = arr[i]
                sift_down(h._data, 1, h._size, h._compare, h._is_max)
            end
        end
    end

    return h:top()
end

--- 获取第 K 小的元素（维护大小为 k 的最大堆）
function heap_utils.kth_smallest(arr, k, compare)
    if k < 1 or k > #arr then
        return nil, false
    end

    local cmp = compare or function(a, b)
        if a < b then return -1 elseif a > b then return 1 else return 0 end
    end

    local h = new_heap(true, cmp)

    for i = 1, #arr do
        if h._size < k then
            h:push(arr[i])
        else
            if cmp(arr[i], h._data[1]) < 0 then
                h._data[1] = arr[i]
                sift_down(h._data, 1, h._size, h._compare, h._is_max)
            end
        end
    end

    return h:top()
end

--- 中位数查找（使用两个堆）
function heap_utils.median(arr)
    if #arr == 0 then
        return nil
    end

    local max_heap = new_heap(true, function(a, b) return a - b end)
    local min_heap = new_heap(false, function(a, b) return a - b end)

    for _, v in ipairs(arr) do
        max_heap:push(v)

        local max_top = max_heap:top()
        local min_top = min_heap:top()

        if min_heap:size() > 0 and max_heap._compare(max_top, min_top) > 0 then
            local val = max_heap:pop()
            min_heap:push(val)
        end

        if max_heap:size() < min_heap:size() then
            local val = min_heap:pop()
            max_heap:push(val)
        end
    end

    if max_heap:size() > min_heap:size() then
        return max_heap:top()
    else
        local a = max_heap:top()
        local b = min_heap:top()
        return (a + b) / 2
    end
end

--------------------------------------------------------------------------------
-- 导出
--------------------------------------------------------------------------------

return heap_utils
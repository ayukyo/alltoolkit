-- Queue Utils 📋
-- Lua 队列数据结构工具模块 - 零依赖，生产就绪
--
-- 提供全面的队列实现：普通队列、双端队列、优先队列、循环队列等
-- 所有实现均使用 Lua 标准库，零外部依赖
--
-- Author: AllToolkit
-- Version: 1.0.0
-- License: MIT

local queue_utils = {}

-- 版本号
queue_utils._VERSION = "1.0.0"

--------------------------------------------------------------------------------
-- Queue (普通队列 - FIFO)
--------------------------------------------------------------------------------

--- 创建普通队列
-- @return 队列对象
function queue_utils.new()
    local queue = {
        _items = {},
        _head = 1,
        _tail = 0,
        _size = 0
    }
    
    -- 方法绑定
    queue.push = queue_utils._queue_push
    queue.pop = queue_utils._queue_pop
    queue.peek = queue_utils._queue_peek
    queue.size = queue_utils._queue_size
    queue.is_empty = queue_utils._queue_is_empty
    queue.clear = queue_utils._queue_clear
    queue.to_array = queue_utils._queue_to_array
    queue.iterate = queue_utils._queue_iterate
    
    return queue
end

--- 向队列尾部添加元素
-- @param self 队列对象
-- @param value 要添加的值
-- @return 队列自身
function queue_utils._queue_push(self, value)
    self._tail = self._tail + 1
    self._items[self._tail] = value
    self._size = self._size + 1
    return self
end

--- 从队列头部移除元素
-- @param self 队列对象
-- @return 移除的元素，如果队列为空则返回 nil
function queue_utils._queue_pop(self)
    if self._size == 0 then
        return nil
    end
    
    local value = self._items[self._head]
    self._items[self._head] = nil
    self._head = self._head + 1
    self._size = self._size - 1
    
    -- 重置位置以避免内存泄漏
    if self._size == 0 then
        self._head = 1
        self._tail = 0
    end
    
    return value
end

--- 查看队列头部元素（不移除）
-- @param self 队列对象
-- @return 头部元素，如果队列为空则返回 nil
function queue_utils._queue_peek(self)
    if self._size == 0 then
        return nil
    end
    return self._items[self._head]
end

--- 获取队列大小
-- @param self 队列对象
-- @return 队列中的元素数量
function queue_utils._queue_size(self)
    return self._size
end

--- 检查队列是否为空
-- @param self 队列对象
-- @return 如果为空返回 true
function queue_utils._queue_is_empty(self)
    return self._size == 0
end

--- 清空队列
-- @param self 队列对象
-- @return 队列自身
function queue_utils._queue_clear(self)
    self._items = {}
    self._head = 1
    self._tail = 0
    self._size = 0
    return self
end

--- 将队列转换为数组
-- @param self 队列对象
-- @return 数组（保持顺序）
function queue_utils._queue_to_array(self)
    local result = {}
    for i = self._head, self._tail do
        result[#result + 1] = self._items[i]
    end
    return result
end

--- 迭代队列元素
-- @param self 队列对象
-- @return 迭代器函数
function queue_utils._queue_iterate(self)
    local current = self._head
    local max = self._tail
    
    return function()
        if current > max then
            return nil
        end
        local value = self._items[current]
        current = current + 1
        return current - self._head, value
    end
end

--------------------------------------------------------------------------------
-- Deque (双端队列)
--------------------------------------------------------------------------------

--- 创建双端队列
-- @return 双端队列对象
function queue_utils.new_deque()
    local deque = {
        _items = {},
        _head = 1,
        _tail = 0,
        _size = 0
    }
    
    -- 方法绑定
    deque.push_front = queue_utils._deque_push_front
    deque.push_back = queue_utils._deque_push_back
    deque.pop_front = queue_utils._deque_pop_front
    deque.pop_back = queue_utils._deque_pop_back
    deque.peek_front = queue_utils._deque_peek_front
    deque.peek_back = queue_utils._deque_peek_back
    deque.size = queue_utils._queue_size
    deque.is_empty = queue_utils._queue_is_empty
    deque.clear = queue_utils._queue_clear
    deque.to_array = queue_utils._queue_to_array
    deque.rotate = queue_utils._deque_rotate
    deque.reverse = queue_utils._deque_reverse
    
    return deque
end

--- 向双端队列头部添加元素
-- @param self 双端队列对象
-- @param value 要添加的值
-- @return 双端队列自身
function queue_utils._deque_push_front(self, value)
    self._head = self._head - 1
    self._items[self._head] = value
    self._size = self._size + 1
    return self
end

--- 向双端队列尾部添加元素
-- @param self 双端队列对象
-- @param value 要添加的值
-- @return 双端队列自身
function queue_utils._deque_push_back(self, value)
    return queue_utils._queue_push(self, value)
end

--- 从双端队列头部移除元素
-- @param self 双端队列对象
-- @return 移除的元素，如果为空则返回 nil
function queue_utils._deque_pop_front(self)
    return queue_utils._queue_pop(self)
end

--- 从双端队列尾部移除元素
-- @param self 双端队列对象
-- @return 移除的元素，如果为空则返回 nil
function queue_utils._deque_pop_back(self)
    if self._size == 0 then
        return nil
    end
    
    local value = self._items[self._tail]
    self._items[self._tail] = nil
    self._tail = self._tail - 1
    self._size = self._size - 1
    
    if self._size == 0 then
        self._head = 1
        self._tail = 0
    end
    
    return value
end

--- 查看双端队列头部元素
-- @param self 双端队列对象
-- @return 头部元素，如果为空则返回 nil
function queue_utils._deque_peek_front(self)
    return queue_utils._queue_peek(self)
end

--- 查看双端队列尾部元素
-- @param self 双端队列对象
-- @return 尾部元素，如果为空则返回 nil
function queue_utils._deque_peek_back(self)
    if self._size == 0 then
        return nil
    end
    return self._items[self._tail]
end

--- 旋转双端队列（将尾部元素移到头部）
-- @param self 双端队列对象
-- @param steps 旋转步数（正数向右，负数向左）
-- @return 双端队列自身
function queue_utils._deque_rotate(self, steps)
    if self._size == 0 then
        return self
    end
    
    steps = steps % self._size
    if steps == 0 then
        return self
    end
    
    local arr = self:to_array()
    self:clear()
    
    -- 将最后 steps 个元素移到前面
    for i = #arr - steps + 1, #arr do
        self:push_back(arr[i])
    end
    -- 将前面 size-steps 个元素移到后面
    for i = 1, #arr - steps do
        self:push_back(arr[i])
    end
    
    return self
end

--- 反转双端队列
-- @param self 双端队列对象
-- @return 双端队列自身
function queue_utils._deque_reverse(self)
    local arr = self:to_array()
    self:clear()
    
    for i = #arr, 1, -1 do
        self:push_back(arr[i])
    end
    
    return self
end

--------------------------------------------------------------------------------
-- Priority Queue (优先队列)
--------------------------------------------------------------------------------

--- 创建优先队列
-- @param compare_fn 比较函数（可选，默认为最小堆）
-- @return 优先队列对象
function queue_utils.new_priority(compare_fn)
    -- 默认比较函数：最小堆
    compare_fn = compare_fn or function(a, b)
        return a < b
    end
    
    local pq = {
        _items = {},
        _compare = compare_fn
    }
    
    -- 方法绑定
    pq.push = queue_utils._pq_push
    pq.pop = queue_utils._pq_pop
    pq.peek = queue_utils._pq_peek
    pq.size = queue_utils._pq_size
    pq.is_empty = queue_utils._pq_is_empty
    pq.clear = queue_utils._pq_clear
    pq.to_array = queue_utils._pq_to_array
    
    return pq
end

--- 向优先队列添加元素（使用堆插入）
-- @param self 优先队列对象
-- @param value 要添加的值
-- @return 优先队列自身
function queue_utils._pq_push(self, value)
    local items = self._items
    items[#items + 1] = value
    
    -- 上浮操作
    local idx = #items
    while idx > 1 do
        local parent = math.floor(idx / 2)
        if self._compare(items[idx], items[parent]) then
            items[idx], items[parent] = items[parent], items[idx]
            idx = parent
        else
            break
        end
    end
    
    return self
end

--- 从优先队列移除元素
-- @param self 优先队列对象
-- @return 移除的最高优先级元素，如果为空则返回 nil
function queue_utils._pq_pop(self)
    local items = self._items
    if #items == 0 then
        return nil
    end
    
    local result = items[1]
    items[1] = items[#items]
    items[#items] = nil
    
    -- 下沉操作
    local idx = 1
    while true do
        local left = 2 * idx
        local right = 2 * idx + 1
        local smallest = idx
        
        if left <= #items and self._compare(items[left], items[smallest]) then
            smallest = left
        end
        if right <= #items and self._compare(items[right], items[smallest]) then
            smallest = right
        end
        
        if smallest ~= idx then
            items[idx], items[smallest] = items[smallest], items[idx]
            idx = smallest
        else
            break
        end
    end
    
    return result
end

--- 查看优先队列顶部元素
-- @param self 优先队列对象
-- @return 最高优先级元素，如果为空则返回 nil
function queue_utils._pq_peek(self)
    return self._items[1]
end

--- 获取优先队列大小
-- @param self 优先队列对象
-- @return 元素数量
function queue_utils._pq_size(self)
    return #self._items
end

--- 检查优先队列是否为空
-- @param self 优先队列对象
-- @return 如果为空返回 true
function queue_utils._pq_is_empty(self)
    return #self._items == 0
end

--- 清空优先队列
-- @param self 优先队列对象
-- @return 优先队列自身
function queue_utils._pq_clear(self)
    self._items = {}
    return self
end

--- 将优先队列转换为数组（不保证顺序）
-- @param self 优先队列对象
-- @return 数组
function queue_utils._pq_to_array(self)
    local result = {}
    for i = 1, #self._items do
        result[i] = self._items[i]
    end
    return result
end

--------------------------------------------------------------------------------
-- Circular Queue (循环队列)
--------------------------------------------------------------------------------

--- 创建循环队列
-- @param capacity 队列容量
-- @return 循环队列对象
function queue_utils.new_circular(capacity)
    if capacity <= 0 then
        error("Capacity must be positive")
    end
    
    local cq = {
        _items = {},
        _capacity = capacity,
        _head = 0,
        _tail = 0,
        _size = 0
    }
    
    -- 方法绑定
    cq.push = queue_utils._cq_push
    cq.pop = queue_utils._cq_pop
    cq.peek = queue_utils._cq_peek
    cq.size = queue_utils._cq_size
    cq.capacity = queue_utils._cq_capacity
    cq.is_empty = queue_utils._cq_is_empty
    cq.is_full = queue_utils._cq_is_full
    cq.clear = queue_utils._cq_clear
    cq.to_array = queue_utils._cq_to_array
    
    return cq
end

--- 向循环队列添加元素
-- @param self 循环队列对象
-- @param value 要添加的值
-- @return true 如果成功添加，false 如果队列已满
function queue_utils._cq_push(self, value)
    if self._size == self._capacity then
        return false
    end
    
    self._items[self._tail] = value
    self._tail = (self._tail + 1) % self._capacity
    self._size = self._size + 1
    return true
end

--- 从循环队列移除元素
-- @param self 循环队列对象
-- @return 移除的元素，如果为空则返回 nil
function queue_utils._cq_pop(self)
    if self._size == 0 then
        return nil
    end
    
    local value = self._items[self._head]
    self._items[self._head] = nil
    self._head = (self._head + 1) % self._capacity
    self._size = self._size - 1
    
    return value
end

--- 查看循环队列头部元素
-- @param self 循环队列对象
-- @return 头部元素，如果为空则返回 nil
function queue_utils._cq_peek(self)
    if self._size == 0 then
        return nil
    end
    return self._items[self._head]
end

--- 获取循环队列大小
-- @param self 循环队列对象
-- @return 元素数量
function queue_utils._cq_size(self)
    return self._size
end

--- 获取循环队列容量
-- @param self 循环队列对象
-- @return 容量
function queue_utils._cq_capacity(self)
    return self._capacity
end

--- 检查循环队列是否为空
-- @param self 循环队列对象
-- @return 如果为空返回 true
function queue_utils._cq_is_empty(self)
    return self._size == 0
end

--- 检查循环队列是否已满
-- @param self 循环队列对象
-- @return 如果已满返回 true
function queue_utils._cq_is_full(self)
    return self._size == self._capacity
end

--- 清空循环队列
-- @param self 循环队列对象
-- @return 循环队列自身
function queue_utils._cq_clear(self)
    self._items = {}
    self._head = 0
    self._tail = 0
    self._size = 0
    return self
end

--- 将循环队列转换为数组
-- @param self 循环队列对象
-- @return 数组（保持顺序）
function queue_utils._cq_to_array(self)
    local result = {}
    for i = 0, self._size - 1 do
        local idx = (self._head + i) % self._capacity
        result[#result + 1] = self._items[idx]
    end
    return result
end

--------------------------------------------------------------------------------
-- Stack (栈 - LIFO)
--------------------------------------------------------------------------------

--- 创建栈
-- @return 栈对象
function queue_utils.new_stack()
    local stack = {
        _items = {}
    }
    
    -- 方法绑定
    stack.push = queue_utils._stack_push
    stack.pop = queue_utils._stack_pop
    stack.peek = queue_utils._stack_peek
    stack.size = queue_utils._stack_size
    stack.is_empty = queue_utils._stack_is_empty
    stack.clear = queue_utils._stack_clear
    stack.to_array = queue_utils._stack_to_array
    
    return stack
end

--- 向栈添加元素
-- @param self 栈对象
-- @param value 要添加的值
-- @return 栈自身
function queue_utils._stack_push(self, value)
    self._items[#self._items + 1] = value
    return self
end

--- 从栈移除元素
-- @param self 栈对象
-- @return 移除的元素，如果为空则返回 nil
function queue_utils._stack_pop(self)
    if #self._items == 0 then
        return nil
    end
    local value = self._items[#self._items]
    self._items[#self._items] = nil
    return value
end

--- 查看栈顶元素
-- @param self 栈对象
-- @return 栈顶元素，如果为空则返回 nil
function queue_utils._stack_peek(self)
    if #self._items == 0 then
        return nil
    end
    return self._items[#self._items]
end

--- 获取栈大小
-- @param self 栈对象
-- @return 元素数量
function queue_utils._stack_size(self)
    return #self._items
end

--- 检查栈是否为空
-- @param self 栈对象
-- @return 如果为空返回 true
function queue_utils._stack_is_empty(self)
    return #self._items == 0
end

--- 清空栈
-- @param self 栈对象
-- @return 栈自身
function queue_utils._stack_clear(self)
    self._items = {}
    return self
end

--- 将栈转换为数组
-- @param self 栈对象
-- @return 数组（栈底到栈顶）
function queue_utils._stack_to_array(self)
    local result = {}
    for i = 1, #self._items do
        result[i] = self._items[i]
    end
    return result
end

--------------------------------------------------------------------------------
-- Helper Functions
--------------------------------------------------------------------------------

--- 创建最小优先队列
-- @return 最小优先队列
function queue_utils.new_min_queue()
    return queue_utils.new_priority(function(a, b)
        return a < b
    end)
end

--- 创建最大优先队列
-- @return 最大优先队列
function queue_utils.new_max_queue()
    return queue_utils.new_priority(function(a, b)
        return a > b
    end)
end

--- 创建带优先级元素的优先队列
-- @return 优先队列（比较优先级字段）
function queue_utils.new_weighted_queue()
    return queue_utils.new_priority(function(a, b)
        return a.priority < b.priority
    end)
end

--- 从数组创建队列
-- @param arr 数组
-- @return 队列对象（包含所有数组元素）
function queue_utils.from_array(arr)
    local q = queue_utils.new()
    for i = 1, #arr do
        q:push(arr[i])
    end
    return q
end

--- 从数组创建栈
-- @param arr 数组
-- @return 栈对象
function queue_utils.stack_from_array(arr)
    local s = queue_utils.new_stack()
    for i = 1, #arr do
        s:push(arr[i])
    end
    return s
end

--- 检查值是否在队列中
-- @param q 队列对象
-- @param value 要查找的值
-- @return 如果存在返回 true
function queue_utils.contains(q, value)
    for k, v in q:iterate() do
        if v == value then
            return true
        end
    end
    return false
end

--- 获取队列中特定值的索引
-- @param q 阀列对象
-- @param value 要查找的值
-- @return 索引（从1开始），如果不存在返回 nil
function queue_utils.index_of(q, value)
    for k, v in q:iterate() do
        if v == value then
            return k
        end
    end
    return nil
end

--------------------------------------------------------------------------------
-- Module Export
--------------------------------------------------------------------------------

return queue_utils
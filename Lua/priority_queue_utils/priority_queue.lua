--- Priority Queue Implementation for Lua
--- A priority queue supports inserting elements with associated priorities
--- and removing the element with the highest (or lowest) priority.
--- Uses a binary heap for efficient O(log n) operations.
--- @class PriorityQueue
--- @field heap table The internal heap array
--- @field compare function The comparison function for ordering (compares priorities directly)
--- @field size number The current number of elements
local PriorityQueue = {}
PriorityQueue.__index = PriorityQueue

--- Creates a new PriorityQueue instance
--- @param is_min_heap boolean|nil If true, creates a min-heap (lowest priority first), 
---                                 if false/nil, creates a max-heap (highest priority first)
--- @return PriorityQueue A new priority queue instance
function PriorityQueue.new(is_min_heap)
    local self = setmetatable({}, PriorityQueue)
    self.heap = {}
    self.size = 0
    
    -- Set comparator based on heap type (compares priority values directly)
    if is_min_heap then
        self.compare = function(a, b) return a < b end
    else
        self.compare = function(a, b) return a > b end
    end
    
    return self
end

--- Creates a max-heap priority queue (highest priority first)
--- @return PriorityQueue A new max-heap priority queue
function PriorityQueue.max_heap()
    return PriorityQueue.new(false)
end

--- Creates a min-heap priority queue (lowest priority first)
--- @return PriorityQueue A new min-heap priority queue
function PriorityQueue.min_heap()
    return PriorityQueue.new(true)
end

--- Creates a priority queue with a custom comparator
--- @param compare function Custom comparison function(a, b) -> boolean
---                         Returns true if priority 'a' should come before 'b'
--- @return PriorityQueue A new priority queue with custom ordering
function PriorityQueue.with_comparator(compare)
    local self = setmetatable({}, PriorityQueue)
    self.heap = {}
    self.size = 0
    self.compare = compare
    return self
end

--- Swaps two elements in the heap
--- @param heap table The heap array
--- @param i number First index
--- @param j number Second index
local function swap(heap, i, j)
    heap[i], heap[j] = heap[j], heap[i]
end

--- Gets the parent index
--- @param i number Current index
--- @return number Parent index
local function parent(i)
    return math.floor(i / 2)
end

--- Gets the left child index
--- @param i number Current index
--- @return number Left child index
local function left_child(i)
    return 2 * i
end

--- Gets the right child index
--- @param i number Current index
--- @return number Right child index
local function right_child(i)
    return 2 * i + 1
end

--- Moves an element up the heap to maintain heap property
--- @param heap table The heap array
--- @param index number Starting index
--- @param compare function The comparison function (compares priorities)
local function heapify_up(heap, index, compare)
    while index > 1 do
        local p = parent(index)
        if compare(heap[index].priority, heap[p].priority) then
            swap(heap, index, p)
            index = p
        else
            break
        end
    end
end

--- Moves an element down the heap to maintain heap property
--- @param heap table The heap array
--- @param index number Starting index
--- @param size number Current heap size
--- @param compare function The comparison function (compares priorities)
local function heapify_down(heap, index, size, compare)
    while true do
        local l = left_child(index)
        local r = right_child(index)
        local extreme = index
        
        if l <= size and compare(heap[l].priority, heap[extreme].priority) then
            extreme = l
        end
        
        if r <= size and compare(heap[r].priority, heap[extreme].priority) then
            extreme = r
        end
        
        if extreme ~= index then
            swap(heap, index, extreme)
            index = extreme
        else
            break
        end
    end
end

--- Inserts an element with a given priority
--- @param value any The value to insert
--- @param priority number The priority of the element
--- @return PriorityQueue self (for method chaining)
function PriorityQueue:push(value, priority)
    self.size = self.size + 1
    self.heap[self.size] = { value = value, priority = priority }
    heapify_up(self.heap, self.size, self.compare)
    return self
end

--- Alias for push
--- @param value any The value to insert
--- @param priority number The priority of the element
--- @return PriorityQueue self
function PriorityQueue:enqueue(value, priority)
    return self:push(value, priority)
end

--- Removes and returns the element with highest priority
--- @return any value, number priority The value and priority of the removed element,
---                                      or nil if queue is empty
function PriorityQueue:pop()
    if self.size == 0 then
        return nil, nil
    end
    
    local root = self.heap[1]
    self.heap[1] = self.heap[self.size]
    self.heap[self.size] = nil
    self.size = self.size - 1
    
    if self.size > 0 then
        heapify_down(self.heap, 1, self.size, self.compare)
    end
    
    return root.value, root.priority
end

--- Alias for pop
--- @return any value, number priority
function PriorityQueue:dequeue()
    return self:pop()
end

--- Returns the element with highest priority without removing it
--- @return any value, number priority The value and priority of the top element,
---                                      or nil if queue is empty
function PriorityQueue:peek()
    if self.size == 0 then
        return nil, nil
    end
    return self.heap[1].value, self.heap[1].priority
end

--- Checks if the queue is empty
--- @return boolean True if empty, false otherwise
function PriorityQueue:is_empty()
    return self.size == 0
end

--- Returns the number of elements in the queue
--- @return number The size of the queue
function PriorityQueue:len()
    return self.size
end

--- Clears all elements from the queue
function PriorityQueue:clear()
    self.heap = {}
    self.size = 0
end

--- Converts the queue to a sorted array (without modifying the queue)
--- @return table Array of {value, priority} pairs in priority order
function PriorityQueue:to_sorted_array()
    local result = {}
    -- Collect all elements
    for i = 1, self.size do
        table.insert(result, { value = self.heap[i].value, priority = self.heap[i].priority })
    end
    
    -- Sort using the same comparison logic
    table.sort(result, function(a, b)
        return self.compare(a.priority, b.priority)
    end)
    
    return result
end

--- Updates the priority of an element
--- @param value any The value to find
--- @param new_priority number The new priority
--- @param equals function|nil Optional equality function(a, b) -> boolean
--- @return boolean True if element was found and updated, false otherwise
function PriorityQueue:update_priority(value, new_priority, equals)
    equals = equals or function(a, b) return a == b end
    
    for i = 1, self.size do
        if equals(self.heap[i].value, value) then
            local old_priority = self.heap[i].priority
            self.heap[i].priority = new_priority
            
            -- Determine if we need to heapify up or down
            if self.compare(new_priority, old_priority) then
                heapify_up(self.heap, i, self.compare)
            else
                heapify_down(self.heap, i, self.size, self.compare)
            end
            
            return true
        end
    end
    
    return false
end

--- Checks if a value exists in the queue
--- @param value any The value to find
--- @param equals function|nil Optional equality function
--- @return boolean True if found, false otherwise
function PriorityQueue:contains(value, equals)
    equals = equals or function(a, b) return a == b end
    
    for i = 1, self.size do
        if equals(self.heap[i].value, value) then
            return true
        end
    end
    
    return false
end

--- Removes a specific value from the queue
--- @param value any The value to remove
--- @param equals function|nil Optional equality function
--- @return boolean True if removed, false if not found
function PriorityQueue:remove(value, equals)
    equals = equals or function(a, b) return a == b end
    
    for i = 1, self.size do
        if equals(self.heap[i].value, value) then
            -- Replace with last element
            self.heap[i] = self.heap[self.size]
            self.heap[self.size] = nil
            self.size = self.size - 1
            
            if i <= self.size then
                -- Try both heapify directions
                heapify_up(self.heap, i, self.compare)
                heapify_down(self.heap, i, self.size, self.compare)
            end
            
            return true
        end
    end
    
    return false
end

--- Merges another priority queue into this one
--- @param other PriorityQueue Another priority queue to merge
--- @return PriorityQueue self (for method chaining)
function PriorityQueue:merge(other)
    for i = 1, other.size do
        self:push(other.heap[i].value, other.heap[i].priority)
    end
    return self
end

--- Returns the internal heap as an array (for debugging)
--- @return table The internal heap array
function PriorityQueue:debug_heap()
    local result = {}
    for i = 1, self.size do
        table.insert(result, { value = self.heap[i].value, priority = self.heap[i].priority })
    end
    return result
end

return PriorityQueue
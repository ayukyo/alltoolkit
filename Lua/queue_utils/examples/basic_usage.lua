-- Queue Utils Examples
-- 基础使用示例

local queue_utils = require("mod")

print("Queue Utils Examples")
print("====================")

--------------------------------------------------------------------------------
-- Example 1: Basic Queue (FIFO)
--------------------------------------------------------------------------------
print("\n1. Basic Queue (FIFO):")

local q = queue_utils.new()
q:push("first")
q:push("second")
q:push("third")

print("  Queue size:", q:size())
print("  Front element:", q:peek())

while not q:is_empty() do
    print("  Popped:", q:pop())
end

--------------------------------------------------------------------------------
-- Example 2: Deque (Double-ended Queue)
--------------------------------------------------------------------------------
print("\n2. Deque (Double-ended Queue):")

local d = queue_utils.new_deque()
d:push_back("A")
d:push_back("B")
d:push_front("X")
d:push_front("Y")

print("  Front:", d:peek_front())
print("  Back:", d:peek_back())

print("  Pop front:", d:pop_front())
print("  Pop back:", d:pop_back())

print("  Remaining:", table.concat(d:to_array(), ", "))

--------------------------------------------------------------------------------
-- Example 3: Priority Queue
--------------------------------------------------------------------------------
print("\n3. Priority Queue (Min):")

local min_q = queue_utils.new_min_queue()
min_q:push(50)
min_q:push(20)
min_q:push(80)
min_q:push(10)
min_q:push(30)

print("  Elements in order:")
while not min_q:is_empty() do
    print("    ", min_q:pop())
end

print("\n3b. Priority Queue (Max):")

local max_q = queue_utils.new_max_queue()
max_q:push(50)
max_q:push(20)
max_q:push(80)
max_q:push(10)
max_q:push(30)

print("  Elements in order:")
while not max_q:is_empty() do
    print("    ", max_q:pop())
end

--------------------------------------------------------------------------------
-- Example 4: Weighted Priority Queue
--------------------------------------------------------------------------------
print("\n4. Weighted Priority Queue (Task Scheduler):")

local task_q = queue_utils.new_weighted_queue()

-- Add tasks with different priorities (lower priority = more urgent)
task_q:push({name = "backup", priority = 5})
task_q:push({name = "email", priority = 2})
task_q:push({name = "critical", priority = 1})
task_q:push({name = "logs", priority = 10})

print("  Executing tasks in priority order:")
while not task_q:is_empty() do
    local task = task_q:pop()
    print("    Priority " .. task.priority .. ": " .. task.name)
end

--------------------------------------------------------------------------------
-- Example 5: Circular Queue
--------------------------------------------------------------------------------
print("\n5. Circular Queue (Fixed Capacity):")

local cq = queue_utils.new_circular(3)

print("  Adding elements:")
for i = 1, 5 do
    local success = cq:push(i)
    if success then
        print("    Added " .. i .. ", Size: " .. cq:size())
    else
        print("    Failed to add " .. i .. " (queue full)")
        local old = cq:pop()
        print("    Removed " .. old .. " to make space")
        cq:push(i)
        print("    Added " .. i .. ", Size: " .. cq:size())
    end
end

print("  Final contents:", table.concat(cq:to_array(), ", "))

--------------------------------------------------------------------------------
-- Example 6: Stack (LIFO)
--------------------------------------------------------------------------------
print("\n6. Stack (LIFO):")

local s = queue_utils.new_stack()
s:push("bottom")
s:push("middle")
s:push("top")

print("  Stack size:", s:size())
print("  Top element:", s:peek())

while not s:is_empty() do
    print("  Popped:", s:pop())
end

--------------------------------------------------------------------------------
-- Example 7: From Array and Search
--------------------------------------------------------------------------------
print("\n7. Create from Array and Search:")

local q = queue_utils.from_array({10, 20, 30, 40, 50})
print("  Queue from array:", table.concat(q:to_array(), ", "))

print("  Contains 30:", queue_utils.contains(q, 30))
print("  Contains 100:", queue_utils.contains(q, 100))
print("  Index of 30:", queue_utils.index_of(q, 30))

--------------------------------------------------------------------------------
-- Example 8: Iterator
--------------------------------------------------------------------------------
print("\n8. Using Iterator:")

local q = queue_utils.from_array({"apple", "banana", "cherry"})
print("  Iterating over queue:")
for i, value in q:iterate() do
    print("    Position " .. i .. ": " .. value)
end

print("\nDone!")
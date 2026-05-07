--- Example Usage of PriorityQueue
--- Run with: lua examples.lua

local PriorityQueue = dofile("priority_queue.lua")

print("=== PriorityQueue Examples ===\n")

-- Example 1: Task Scheduler (Max-Heap)
print("1. Task Scheduler (Max-Heap - Highest Priority First)")
print("-" .. string.rep("-", 49))
local scheduler = PriorityQueue.max_heap()
scheduler:push("Critical Bug Fix", 10)
scheduler:push("Feature Development", 5)
scheduler:push("Code Review", 3)
scheduler:push("Documentation", 2)
scheduler:push("Testing", 7)

print("Processing tasks in priority order:")
while not scheduler:is_empty() do
    local task, priority = scheduler:pop()
    print(string.format("  [Priority %2d] %s", priority, task))
end

-- Example 2: Dijkstra's Algorithm Support (Min-Heap)
print("\n2. Pathfinding (Min-Heap - Lowest Cost First)")
print("-" .. string.rep("-", 46))
local distances = PriorityQueue.min_heap()
distances:push("A", 0)      -- Start node
distances:push("B", 4)
distances:push("C", 2)
distances:push("D", 7)
distances:push("E", 1)

print("Processing nodes by distance:")
while not distances:is_empty() do
    local node, dist = distances:pop()
    print(string.format("  Node %s: distance %d", node, dist))
end

-- Example 3: Emergency Room Triage
print("\n3. Emergency Room Triage")
print("-" .. string.rep("-", 24))
local er = PriorityQueue.max_heap()
er:push({ name = "John", issue = "Headache" }, 1)
er:push({ name = "Mary", issue = "Broken leg" }, 5)
er:push({ name = "Bob", issue = "Chest pain" }, 10)
er:push({ name = "Alice", issue = "Fever" }, 3)

print("Triage order (severity 1-10):")
while not er:is_empty() do
    local patient, severity = er:pop()
    print(string.format("  [Severity %2d] %s - %s", severity, patient.name, patient.issue))
end

-- Example 4: Job Queue with Priority Updates
print("\n4. Job Queue with Dynamic Priority")
print("-" .. string.rep("-", 35))
local jobs = PriorityQueue.max_heap()
jobs:push("job_1", 5)
jobs:push("job_2", 3)
jobs:push("job_3", 8)

print("Initial queue:")
for i, job in ipairs(jobs:debug_heap()) do
    print(string.format("  %s: priority %d", job.value, job.priority))
end

print("\nUpdating job_2 priority to 10...")
jobs:update_priority("job_2", 10)

print("\nProcessing updated queue:")
while not jobs:is_empty() do
    local job, priority = jobs:pop()
    print(string.format("  [Priority %2d] %s", priority, job))
end

-- Example 5: Merge Multiple Queues
print("\n5. Merging Multiple Priority Queues")
print("-" .. string.rep("-", 37))
local urgent = PriorityQueue.max_heap()
urgent:push("Urgent Task 1", 8)
urgent:push("Urgent Task 2", 9)

local normal = PriorityQueue.max_heap()
normal:push("Normal Task 1", 4)
normal:push("Normal Task 2", 3)

local low = PriorityQueue.max_heap()
low:push("Low Task 1", 1)
low:push("Low Task 2", 2)

urgent:merge(normal):merge(low)

print("Merged queue (processing in order):")
while not urgent:is_empty() do
    local task, priority = urgent:pop()
    print(string.format("  [Priority %2d] %s", priority, task))
end

-- Example 6: Custom Comparator (Absolute Value Priority)
print("\n6. Custom Comparator (Closest to Zero First)")
print("-" .. string.rep("-", 45))
local closest = PriorityQueue.with_comparator(function(a, b)
    return math.abs(a) < math.abs(b)  -- Smaller absolute value = higher priority
end)

closest:push("value_a", -5)
closest:push("value_b", 3)
closest:push("value_c", -1)
closest:push("value_d", 8)
closest:push("value_e", 0)

print("Processing by distance from zero:")
while not closest:is_empty() do
    local name, value = closest:pop()
    print(string.format("  %s: %d (distance: %d)", name, value, math.abs(value)))
end

-- Example 7: Removing Specific Elements
print("\n7. Cancelled Tasks (Remove Specific Elements)")
print("-" .. string.rep("-", 46))
local tasks = PriorityQueue.max_heap()
tasks:push("Task A", 5)
tasks:push("Task B", 8)
tasks:push("Task C", 3)
tasks:push("Task D", 7)

print("Original tasks:")
print("  " .. table.concat({"Task B (8)", "Task D (7)", "Task A (5)", "Task C (3)"}, ", "))

print("\nCancelling Task D...")
tasks:remove("Task D")

print("Remaining tasks:")
while not tasks:is_empty() do
    local task, priority = tasks:pop()
    print(string.format("  [Priority %d] %s", priority, task))
end

-- Example 8: Contains Check
print("\n8. Checking for Specific Items")
print("-" .. string.rep("-", 31))
local inventory = PriorityQueue.min_heap()
inventory:push("Sword", 3)
inventory:push("Shield", 2)
inventory:push("Potion", 1)

print(string.format("Has Sword: %s", inventory:contains("Sword") and "Yes" or "No"))
print(string.format("Has Bow: %s", inventory:contains("Bow") and "Yes" or "No"))

-- Example 9: Complex Objects with Custom Equality
print("\n9. Complex Objects with Custom Equality")
print("-" .. string.rep("-", 37))
local by_id = function(a, b) return a.id == b.id end

local requests = PriorityQueue.max_heap()
requests:push({ id = 1, user = "Alice", request = "GET /api/users" }, 5)
requests:push({ id = 2, user = "Bob", request = "POST /api/data" }, 8)
requests:push({ id = 3, user = "Charlie", request = "GET /api/items" }, 3)

print("Has request with id 2: " .. (requests:contains({ id = 2 }, by_id) and "Yes" or "No"))
print("Updating priority of request 2 to 10...")
requests:update_priority({ id = 2 }, 10, by_id)

local top = requests:peek()
print(string.format("Top request: %s from %s", top.request, top.user))

print("\n=== All Examples Complete ===")
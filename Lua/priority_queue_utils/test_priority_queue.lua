--- Test suite for PriorityQueue
--- Run with: lua test_priority_queue.lua

local PriorityQueue = dofile("priority_queue.lua")

local tests_passed = 0
local tests_failed = 0

local function test(name, fn)
    local ok, err = pcall(fn)
    if ok then
        tests_passed = tests_passed + 1
        print("✓ " .. name)
    else
        tests_failed = tests_failed + 1
        print("✗ " .. name .. ": " .. tostring(err))
    end
end

local function assert_equal(a, b, msg)
    if a ~= b then
        error(msg .. " (expected: " .. tostring(b) .. ", got: " .. tostring(a) .. ")")
    end
end

local function assert_true(value, msg)
    if not value then
        error(msg .. " (expected true, got false)")
    end
end

local function assert_false(value, msg)
    if value then
        error(msg .. " (expected false, got true)")
    end
end

print("=== PriorityQueue Tests ===\n")

-- Test: Create max-heap
test("Create max-heap priority queue", function()
    local pq = PriorityQueue.max_heap()
    assert_true(pq:is_empty(), "Should be empty initially")
    assert_equal(pq:len(), 0, "Length should be 0")
end)

-- Test: Create min-heap
test("Create min-heap priority queue", function()
    local pq = PriorityQueue.min_heap()
    assert_true(pq:is_empty(), "Should be empty initially")
end)

-- Test: Push and pop single element
test("Push and pop single element", function()
    local pq = PriorityQueue.max_heap()
    pq:push("task1", 5)
    assert_equal(pq:len(), 1, "Length should be 1")
    assert_false(pq:is_empty(), "Should not be empty")
    
    local value, priority = pq:pop()
    assert_equal(value, "task1", "Value should be task1")
    assert_equal(priority, 5, "Priority should be 5")
    assert_true(pq:is_empty(), "Should be empty after pop")
end)

-- Test: Max-heap ordering
test("Max-heap ordering (highest priority first)", function()
    local pq = PriorityQueue.max_heap()
    pq:push("low", 1)
    pq:push("high", 10)
    pq:push("medium", 5)
    
    local v1, p1 = pq:pop()
    assert_equal(v1, "high", "First should be high priority")
    assert_equal(p1, 10, "Priority should be 10")
    
    local v2, p2 = pq:pop()
    assert_equal(v2, "medium", "Second should be medium priority")
    assert_equal(p2, 5, "Priority should be 5")
    
    local v3, p3 = pq:pop()
    assert_equal(v3, "low", "Third should be low priority")
    assert_equal(p3, 1, "Priority should be 1")
end)

-- Test: Min-heap ordering
test("Min-heap ordering (lowest priority first)", function()
    local pq = PriorityQueue.min_heap()
    pq:push("low", 1)
    pq:push("high", 10)
    pq:push("medium", 5)
    
    local v1, p1 = pq:pop()
    assert_equal(v1, "low", "First should be low priority")
    assert_equal(p1, 1, "Priority should be 1")
    
    local v2, p2 = pq:pop()
    assert_equal(v2, "medium", "Second should be medium priority")
    assert_equal(p2, 5, "Priority should be 5")
    
    local v3, p3 = pq:pop()
    assert_equal(v3, "high", "Third should be high priority")
    assert_equal(p3, 10, "Priority should be 10")
end)

-- Test: Peek
test("Peek returns top without removing", function()
    local pq = PriorityQueue.max_heap()
    pq:push("task1", 5)
    pq:push("task2", 10)
    
    local value, priority = pq:peek()
    assert_equal(value, "task2", "Should peek highest priority")
    assert_equal(priority, 10, "Priority should be 10")
    assert_equal(pq:len(), 2, "Length should still be 2")
    
    pq:pop()
    value, priority = pq:peek()
    assert_equal(value, "task1", "Should peek next element")
    assert_equal(priority, 5, "Priority should be 5")
end)

-- Test: Peek on empty queue
test("Peek on empty queue returns nil", function()
    local pq = PriorityQueue.max_heap()
    local value, priority = pq:peek()
    assert_equal(value, nil, "Value should be nil")
    assert_equal(priority, nil, "Priority should be nil")
end)

-- Test: Pop on empty queue
test("Pop on empty queue returns nil", function()
    local pq = PriorityQueue.max_heap()
    local value, priority = pq:pop()
    assert_equal(value, nil, "Value should be nil")
    assert_equal(priority, nil, "Priority should be nil")
end)

-- Test: Enqueue/dequeue aliases
test("Enqueue/dequeue aliases work correctly", function()
    local pq = PriorityQueue.max_heap()
    pq:enqueue("item", 5)
    assert_equal(pq:len(), 1, "Length should be 1")
    
    local value, priority = pq:dequeue()
    assert_equal(value, "item", "Value should be item")
    assert_equal(priority, 5, "Priority should be 5")
end)

-- Test: Clear
test("Clear removes all elements", function()
    local pq = PriorityQueue.max_heap()
    pq:push("a", 1)
    pq:push("b", 2)
    pq:push("c", 3)
    assert_equal(pq:len(), 3, "Length should be 3")
    
    pq:clear()
    assert_equal(pq:len(), 0, "Length should be 0 after clear")
    assert_true(pq:is_empty(), "Should be empty after clear")
end)

-- Test: Contains
test("Contains finds existing elements", function()
    local pq = PriorityQueue.max_heap()
    pq:push("apple", 1)
    pq:push("banana", 2)
    pq:push("cherry", 3)
    
    assert_true(pq:contains("apple"), "Should find apple")
    assert_true(pq:contains("banana"), "Should find banana")
    assert_false(pq:contains("grape"), "Should not find grape")
end)

-- Test: Contains with custom equality
test("Contains with custom equality function", function()
    local pq = PriorityQueue.max_heap()
    pq:push({ id = 1, name = "Alice" }, 5)
    pq:push({ id = 2, name = "Bob" }, 3)
    
    local custom_equals = function(a, b) return a.id == b.id end
    assert_true(pq:contains({ id = 1 }, custom_equals), "Should find by id")
    assert_false(pq:contains({ id = 3 }, custom_equals), "Should not find missing id")
end)

-- Test: Remove
test("Remove specific element", function()
    local pq = PriorityQueue.max_heap()
    pq:push("a", 1)
    pq:push("b", 2)
    pq:push("c", 3)
    
    assert_true(pq:remove("b"), "Should remove b")
    assert_equal(pq:len(), 2, "Length should be 2")
    assert_false(pq:contains("b"), "b should be removed")
    
    local v1 = pq:pop()
    local v2 = pq:pop()
    assert_true((v1 == "a" or v1 == "c") and (v2 == "a" or v2 == "c"), "Remaining elements should be a and c")
end)

-- Test: Remove non-existent
test("Remove non-existent element returns false", function()
    local pq = PriorityQueue.max_heap()
    pq:push("a", 1)
    assert_false(pq:remove("x"), "Should return false for non-existent")
end)

-- Test: Update priority
test("Update priority of existing element", function()
    local pq = PriorityQueue.max_heap()
    pq:push("task", 5)
    pq:push("other", 3)
    
    pq:update_priority("task", 10)
    local value, priority = pq:peek()
    assert_equal(value, "task", "task should now be at top")
    assert_equal(priority, 10, "Priority should be 10")
end)

-- Test: Update priority (decrease)
test("Update priority to lower value", function()
    local pq = PriorityQueue.max_heap()
    pq:push("high", 10)
    pq:push("low", 1)
    
    pq:update_priority("high", 0)
    local value, priority = pq:peek()
    assert_equal(value, "low", "low should now be at top")
    assert_equal(priority, 1, "Priority should be 1")
end)

-- Test: Update priority with custom equality
test("Update priority with custom equality", function()
    local pq = PriorityQueue.max_heap()
    pq:push({ id = 1, name = "Alice" }, 5)
    pq:push({ id = 2, name = "Bob" }, 3)
    
    local custom_equals = function(a, b) return a.id == b.id end
    assert_true(pq:update_priority({ id = 1 }, 10, custom_equals), "Should update by id")
    
    local top, _ = pq:peek()
    assert_equal(top.id, 1, "Alice should be at top")
end)

-- Test: Merge
test("Merge two priority queues", function()
    local pq1 = PriorityQueue.max_heap()
    pq1:push("a", 5)
    pq1:push("b", 3)
    
    local pq2 = PriorityQueue.max_heap()
    pq2:push("c", 10)
    pq2:push("d", 1)
    
    pq1:merge(pq2)
    assert_equal(pq1:len(), 4, "Length should be 4")
    
    local values = {}
    while not pq1:is_empty() do
        local v, _ = pq1:pop()
        table.insert(values, v)
    end
    assert_equal(values[1], "c", "First should be c (priority 10)")
    assert_equal(values[2], "a", "Second should be a (priority 5)")
    assert_equal(values[3], "b", "Third should be b (priority 3)")
    assert_equal(values[4], "d", "Fourth should be d (priority 1)")
end)

-- Test: To sorted array
test("To sorted array returns elements in order", function()
    local pq = PriorityQueue.max_heap()
    pq:push("low", 1)
    pq:push("high", 10)
    pq:push("medium", 5)
    
    local sorted = pq:to_sorted_array()
    assert_equal(#sorted, 3, "Should have 3 elements")
    assert_equal(sorted[1].value, "high", "First should be high")
    assert_equal(sorted[2].value, "medium", "Second should be medium")
    assert_equal(sorted[3].value, "low", "Third should be low")
    
    -- Original queue should not be modified
    assert_equal(pq:len(), 3, "Original queue should still have 3 elements")
end)

-- Test: Custom comparator
test("Custom comparator (reverse alphabetical)", function()
    local pq = PriorityQueue.with_comparator(function(a, b)
        return a > b -- Higher string value first (reverse alphabetical)
    end)
    
    -- Use string itself as priority (for custom ordering demonstration)
    pq:push("apple", "apple")
    pq:push("banana", "banana")
    pq:push("cherry", "cherry")
    
    assert_equal(pq:pop(), "cherry", "cherry should come first")
    assert_equal(pq:pop(), "banana", "banana should come second")
    assert_equal(pq:pop(), "apple", "apple should come last")
end)

-- Test: Large number of elements
test("Handle many elements correctly", function()
    local pq = PriorityQueue.min_heap()
    local count = 100
    
    for i = count, 1, -1 do
        pq:push("item" .. i, i)
    end
    
    assert_equal(pq:len(), count, "Should have " .. count .. " elements")
    
    for i = 1, count do
        local value, priority = pq:pop()
        assert_equal(priority, i, "Should pop in ascending order")
    end
    
    assert_true(pq:is_empty(), "Should be empty after all pops")
end)

-- Test: Same priority handling (stable-ish behavior)
test("Elements with same priority", function()
    local pq = PriorityQueue.max_heap()
    pq:push("first", 5)
    pq:push("second", 5)
    pq:push("third", 5)
    
    assert_equal(pq:len(), 3, "Should have 3 elements")
    
    -- All should have priority 5
    local _, p1 = pq:pop()
    local _, p2 = pq:pop()
    local _, p3 = pq:pop()
    
    assert_equal(p1, 5, "Priority should be 5")
    assert_equal(p2, 5, "Priority should be 5")
    assert_equal(p3, 5, "Priority should be 5")
end)

-- Test: Method chaining
test("Method chaining on push", function()
    local pq = PriorityQueue.max_heap()
        :push("a", 1)
        :push("b", 2)
        :push("c", 3)
    
    assert_equal(pq:len(), 3, "Should have 3 elements")
end)

print("\n=== Test Results ===")
print(string.format("Passed: %d", tests_passed))
print(string.format("Failed: %d", tests_failed))

if tests_failed == 0 then
    print("\n✓ All tests passed!")
else
    print("\n✗ Some tests failed.")
    os.exit(1)
end
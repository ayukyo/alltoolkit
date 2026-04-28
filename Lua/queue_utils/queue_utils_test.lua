-- Queue Utils Test Suite
-- 单元测试 - 验证所有队列功能

local queue_utils = require("mod")

local total_tests = 0
local passed_tests = 0
local failed_tests = 0

local function test(name, condition)
    total_tests = total_tests + 1
    if condition then
        passed_tests = passed_tests + 1
        print("[PASS] " .. name)
    else
        failed_tests = failed_tests + 1
        print("[FAIL] " .. name)
    end
end

local function test_equal(name, actual, expected)
    test(name, actual == expected)
end

local function test_array_equal(name, actual, expected)
    if #actual ~= #expected then
        test(name, false)
        return
    end
    for i = 1, #actual do
        if actual[i] ~= expected[i] then
            test(name, false)
            return
        end
    end
    test(name, true)
end

print("Running Queue Utils Tests...")
print("==============================")

--------------------------------------------------------------------------------
-- Queue Tests
--------------------------------------------------------------------------------
print("\n--- Queue Tests ---")

local q = queue_utils.new()
test("queue is_empty initially", q:is_empty())
test_equal("queue size initially", q:size(), 0)

q:push(1):push(2):push(3)
test("queue not empty after push", not q:is_empty())
test_equal("queue size after push", q:size(), 3)
test_equal("queue peek", q:peek(), 1)

local val = q:pop()
test_equal("queue pop first", val, 1)
test_equal("queue size after pop", q:size(), 2)
test_equal("queue peek after pop", q:peek(), 2)

q:pop()
q:pop()
test("queue empty after all pops", q:is_empty())
test_equal("queue pop empty returns nil", q:pop(), nil)

q:push(1):push(2):push(3)
test_array_equal("queue to_array", q:to_array(), {1, 2, 3})

q:clear()
test("queue is_empty after clear", q:is_empty())

--------------------------------------------------------------------------------
-- Deque Tests
--------------------------------------------------------------------------------
print("\n--- Deque Tests ---")

local d = queue_utils.new_deque()
test("deque is_empty initially", d:is_empty())

d:push_back(1)
d:push_back(2)
d:push_front(0)
test_equal("deque size", d:size(), 3)
test_equal("deque peek_front", d:peek_front(), 0)
test_equal("deque peek_back", d:peek_back(), 2)

test_equal("deque pop_front", d:pop_front(), 0)
test_equal("deque pop_back", d:pop_back(), 2)
test_equal("deque size after pops", d:size(), 1)

d:push_back(2):push_back(3):push_back(4)
d:reverse()
test_array_equal("deque reverse", d:to_array(), {4, 3, 2, 1})

d:rotate(2)
test_array_equal("deque rotate", d:to_array(), {2, 1, 4, 3})

--------------------------------------------------------------------------------
-- Priority Queue Tests
--------------------------------------------------------------------------------
print("\n--- Priority Queue Tests ---")

local min_q = queue_utils.new_min_queue()
min_q:push(5):push(2):push(8):push(1):push(9)
test_equal("min_queue peek", min_q:peek(), 1)
test_equal("min_queue pop", min_q:pop(), 1)
test_equal("min_queue pop second", min_q:pop(), 2)
test_equal("min_queue size", min_q:size(), 3)

local max_q = queue_utils.new_max_queue()
max_q:push(5):push(2):push(8):push(1):push(9)
test_equal("max_queue peek", max_q:peek(), 9)
test_equal("max_queue pop", max_q:pop(), 9)
test_equal("max_queue pop second", max_q:pop(), 8)

-- Weighted queue test
local wq = queue_utils.new_weighted_queue()
wq:push({value = "task1", priority = 3})
wq:push({value = "task2", priority = 1})
wq:push({value = "task3", priority = 2})

local top = wq:pop()
test_equal("weighted_queue pop priority", top.priority, 1)
test_equal("weighted_queue pop value", top.value, "task2")

--------------------------------------------------------------------------------
-- Circular Queue Tests
--------------------------------------------------------------------------------
print("\n--- Circular Queue Tests ---")

local cq = queue_utils.new_circular(3)
test_equal("circular_queue capacity", cq:capacity(), 3)
test("circular_queue is_empty", cq:is_empty())
test("circular_queue not full", not cq:is_full())

cq:push(1)
cq:push(2)
test("circular_queue push success", cq:push(3))
test("circular_queue is_full", cq:is_full())
test("circular_queue push fails when full", not cq:push(4))

test_equal("circular_queue pop", cq:pop(), 1)
test("circular_queue not full after pop", not cq:is_full())
cq:push(4)
test_array_equal("circular_queue to_array", cq:to_array(), {2, 3, 4})

--------------------------------------------------------------------------------
-- Stack Tests
--------------------------------------------------------------------------------
print("\n--- Stack Tests ---")

local s = queue_utils.new_stack()
test("stack is_empty initially", s:is_empty())

s:push(1):push(2):push(3)
test_equal("stack size", s:size(), 3)
test_equal("stack peek", s:peek(), 3)

test_equal("stack pop", s:pop(), 3)
test_equal("stack peek after pop", s:peek(), 2)
test_equal("stack size after pop", s:size(), 2)

s:clear()
test("stack is_empty after clear", s:is_empty())
test_equal("stack pop empty returns nil", s:pop(), nil)

--------------------------------------------------------------------------------
-- Helper Functions Tests
--------------------------------------------------------------------------------
print("\n--- Helper Functions Tests ---")

local q_arr = queue_utils.from_array({1, 2, 3, 4, 5})
test_equal("from_array size", q_arr:size(), 5)
test_equal("from_array peek", q_arr:peek(), 1)

local s_arr = queue_utils.stack_from_array({1, 2, 3})
test_equal("stack_from_array size", s_arr:size(), 3)
test_equal("stack_from_array peek", s_arr:peek(), 3)

q_arr:push(1):push(2):push(3)
test("contains true", queue_utils.contains(q_arr, 2))
test("contains false", not queue_utils.contains(q_arr, 10))

test_equal("index_of found", queue_utils.index_of(q_arr, 2), 2)
test_equal("index_of not found", queue_utils.index_of(q_arr, 10), nil)

--------------------------------------------------------------------------------
-- Summary
--------------------------------------------------------------------------------
print("\n==============================")
print("Total:  ", total_tests)
print("Passed: ", passed_tests)
print("Failed: ", failed_tests)

if failed_tests == 0 then
    print("\nAll tests passed!")
    os.exit(0)
else
    print("\nSome tests failed!")
    os.exit(1)
end
# Priority Queue Utils - Lua

A zero-dependency priority queue implementation for Lua using a binary heap. Supports both max-heap and min-heap variants with O(log n) insertion and extraction operations.

## Features

- **Max-Heap**: Highest priority first (default)
- **Min-Heap**: Lowest priority first
- **Custom Comparators**: Define your own ordering
- **Full API**: push, pop, peek, update, remove, merge, and more
- **Zero Dependencies**: Pure Lua, no external libraries required

## Installation

Simply copy `priority_queue.lua` to your project and require it:

```lua
local PriorityQueue = dofile("priority_queue.lua")
-- or use require if in package.path
```

## Quick Start

```lua
local PriorityQueue = dofile("priority_queue.lua")

-- Create a max-heap (highest priority first)
local pq = PriorityQueue.max_heap()

-- Add elements with priorities
pq:push("Critical Bug", 10)
pq:push("Feature Request", 5)
pq:push("Documentation", 2)

-- Process in priority order
while not pq:is_empty() do
    local value, priority = pq:pop()
    print(string.format("[%d] %s", priority, value))
end
-- Output:
-- [10] Critical Bug
-- [5] Feature Request
-- [2] Documentation
```

## API Reference

### Creation

```lua
-- Max-heap (highest priority first)
local pq = PriorityQueue.max_heap()

-- Min-heap (lowest priority first)
local pq = PriorityQueue.min_heap()

-- Custom comparator
local pq = PriorityQueue.with_comparator(function(a, b)
    return math.abs(a) < math.abs(b)  -- Smaller absolute value wins
end)
```

### Core Operations

| Method | Description | Time Complexity |
|--------|-------------|-----------------|
| `push(value, priority)` | Insert element with priority | O(log n) |
| `pop()` | Remove and return top element | O(log n) |
| `peek()` | View top element without removing | O(1) |
| `is_empty()` | Check if queue is empty | O(1) |
| `len()` | Get number of elements | O(1) |

### Additional Operations

| Method | Description | Time Complexity |
|--------|-------------|-----------------|
| `clear()` | Remove all elements | O(1) |
| `contains(value, equals_fn)` | Check if value exists | O(n) |
| `remove(value, equals_fn)` | Remove specific element | O(n) |
| `update_priority(value, new_priority, equals_fn)` | Update element's priority | O(n + log n) |
| `merge(other_queue)` | Merge another queue into this one | O(m log n) |
| `to_sorted_array()` | Get sorted array without modifying queue | O(n log n) |

### Aliases

- `enqueue()` = `push()`
- `dequeue()` = `pop()`

## Examples

### Task Scheduler

```lua
local scheduler = PriorityQueue.max_heap()
scheduler:push("Critical Bug Fix", 10)
scheduler:push("Feature Development", 5)
scheduler:push("Testing", 7)

-- Process highest priority first
while not scheduler:is_empty() do
    local task, priority = scheduler:pop()
    print(string.format("Priority %d: %s", priority, task))
end
```

### Pathfinding (Dijkstra-style)

```lua
local distances = PriorityQueue.min_heap()
distances:push("A", 0)   -- Start
distances:push("B", 4)
distances:push("C", 2)

-- Process shortest distance first
while not distances:is_empty() do
    local node, dist = distances:pop()
    print(string.format("Node %s at distance %d", node, dist))
end
```

### Complex Objects

```lua
local pq = PriorityQueue.max_heap()
pq:push({ id = 1, name = "Alice", role = "Admin" }, 10)
pq:push({ id = 2, name = "Bob", role = "User" }, 5)

-- Custom equality for contains/remove/update
local by_id = function(a, b) return a.id == b.id end

if pq:contains({ id = 1 }, by_id) then
    pq:update_priority({ id = 1 }, 15, by_id)
end

local user, priority = pq:peek()
print(string.format("%s (%s) has priority %d", user.name, user.role, priority))
```

### Method Chaining

```lua
local pq = PriorityQueue.max_heap()
    :push("Task A", 5)
    :push("Task B", 10)
    :push("Task C", 3)
```

### Merging Queues

```lua
local urgent = PriorityQueue.max_heap()
urgent:push("Urgent 1", 9)
urgent:push("Urgent 2", 8)

local normal = PriorityQueue.max_heap()
normal:push("Normal 1", 4)
normal:push("Normal 2", 3)

urgent:merge(normal)  -- Now urgent has all 4 items
```

## Running Tests

```bash
lua test_priority_queue.lua
```

## Running Examples

```bash
lua examples.lua
```

## Implementation Notes

- Uses a binary heap stored in a 1-indexed array
- Parent of node i: floor(i/2)
- Children of node i: 2*i and 2*i+1
- Heap property is maintained after every insert/delete
- No external dependencies required

## License

MIT License - Part of AllToolkit
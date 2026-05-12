---
-- Example 2: Traversal Algorithms
-- 遍历算法示例
--

local GraphUtils = dofile("mod.lua")

print("=" .. string.rep("=", 50))
print("Example 2: Traversal Algorithms")
print("=" .. string.rep("=", 50))
print()

-- 创建图
local g = GraphUtils.undirected()
g:addEdge("A", "B")
g:addEdge("A", "C")
g:addEdge("B", "D")
g:addEdge("B", "E")
g:addEdge("C", "F")
g:addEdge("D", "G")

print("Graph structure:")
print("        A")
print("       /|\\")
print("      B C |")
print("     /|\\  F")
print("    D E |")
print("    |   G")
print()

-- BFS 遍历
print("1. BFS traversal from A...")
local bfsOrder = g:bfs("A")
print("   BFS order:", table.concat(bfsOrder, " -> "))

-- BFS with depth
local depths = {}
g:bfs("A", function(vertex, depth)
    depths[vertex] = depth
end)
print("   Vertex depths:")
for v, d in pairs(depths) do
    print("      " .. v .. ": depth " .. d)
    end
print()

-- DFS 遍历 (迭代)
print("2. DFS traversal (iterative) from A...")
local dfsOrder = g:dfs("A")
print("   DFS order:", table.concat(dfsOrder, " -> "))
print()

-- DFS 遍历 (递归)
print("3. DFS traversal (recursive) from A...")
local dfsRecOrder = g:dfsRecursive("A")
print("   DFS order:", table.concat(dfsRecOrder, " -> "))
print()

-- 层序遍历
print("4. Level-order traversal...")
local levels = g:bfsLevelOrder("A")
for i, level in ipairs(levels) do
    print("   Level " .. (i-1) .. ": " .. table.concat(level, ", "))
end
print()

print("Example 2 completed!")
print()
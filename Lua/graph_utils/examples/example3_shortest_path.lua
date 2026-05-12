---
-- Example 3: Shortest Path Algorithms
-- 最短路径算法示例
--

local GraphUtils = dofile("mod.lua")

print("=" .. string.rep("=", 50))
print("Example 3: Shortest Path Algorithms")
print("=" .. string.rep("=", 50))
print()

-- 创建带权有向图
local g = GraphUtils.directed(true)
g:addEdge("A", "B", 4)
g:addEdge("A", "C", 2)
g:addEdge("B", "C", 3)
g:addEdge("B", "D", 2)
g:addEdge("B", "E", 3)
g:addEdge("C", "B", 1)
g:addEdge("C", "D", 4)
g:addEdge("C", "E", 5)
g:addEdge("E", "D", 1)

print("Weighted directed graph created")
print()

-- Dijkstra 算法
print("1. Dijkstra algorithm from A...")
local distances, predecessors = g:dijkstra("A")
print("   Shortest distances from A:")
for v, d in pairs(distances) do
    if d < math.huge then
        print("      A -> " .. v .. ": " .. d)
    end
end
print()

-- 获取最短路径
print("2. Get shortest path from A to E...")
local path, dist = g:getShortestPath("A", "E")
if path then
    print("   Path:", table.concat(path, " -> "))
    print("   Total distance:", dist)
else
    print("   No path found")
end
print()

-- Floyd-Warshall 全源最短路径
print("3. Floyd-Warshall (all pairs shortest paths)...")
local allDist = g:floydWarshall()
print("   Distance matrix:")
local vertices = g:getVertices()
table.sort(vertices)
print("   From A:")
for _, v in ipairs(vertices) do
    local d = allDist["A"][v]
    if d < math.huge then
        print("      -> " .. v .. ": " .. d)
    end
end
print()

-- Bellman-Ford 算法
print("4. Bellman-Ford algorithm from A...")
local bfDist, bfPred, hasNegCycle = g:bellmanFord("A")
print("   Has negative cycle:", hasNegCycle)
print("   Distances match Dijkstra:", bfDist["E"] == distances["E"])
print()

print("Example 3 completed!")
print()
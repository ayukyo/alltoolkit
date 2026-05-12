---
-- Example 6: Connectivity and Other Algorithms
-- 连通性和其他算法示例
--

local GraphUtils = dofile("mod.lua")

print("=" .. string.rep("=", 50))
print("Example 6: Connectivity and Other Algorithms")
print("=" .. string.rep("=", 50))
print()

-- 创建连通图
print("1. Creating connected graph...")
local connected = GraphUtils.undirected()
connected:addEdge("A", "B")
connected:addEdge("B", "C")
connected:addEdge("C", "D")
connected:addEdge("D", "A")

print("   Graph: A-B-C-D-A (square)")
print("   Is connected:", connected:isConnected())
print()

-- 连通分量
local components = connected:connectedComponents()
print("   Connected components:", #components)
print()

-- 创建不连通图
print("2. Creating disconnected graph...")
local disconnected = GraphUtils.undirected()
disconnected:addEdge("A", "B")
disconnected:addEdge("B", "C")
disconnected:addEdge("D", "E")  -- Separate component

print("   Graph has two separate components")
print("   Is connected:", disconnected:isConnected())

local comps = disconnected:connectedComponents()
print("   Connected components:", #comps)
for i, comp in ipairs(comps) do
    print("      Component " .. i .. ": " .. table.concat(comp, ", "))
end
print()

-- 强连通分量 (有向图)
print("3. Strongly connected components (directed graph)...")
local directed = GraphUtils.directed()
directed:addEdge("A", "B")
directed:addEdge("B", "C")
directed:addEdge("C", "A")  -- SCC: A, B, C
directed:addEdge("C", "D")
directed:addEdge("D", "E")
directed:addEdge("E", "D")  -- SCC: D, E

local sccs = directed:stronglyConnectedComponents()
print("   Strongly connected components:", #sccs)
for i, scc in ipairs(sccs) do
    print("      SCC " .. i .. ": " .. table.concat(scc, ", "))
end
print()

-- 二分图检测
print("4. Bipartite graph detection...")
local bipartite = GraphUtils.undirected()
bipartite:addEdge("A", "B")
bipartite:addEdge("A", "C")
bipartite:addEdge("B", "D")
bipartite:addEdge("C", "D")
bipartite:addEdge("B", "E")
bipartite:addEdge("C", "E")

local isBip, partitions = bipartite:isBipartite()
print("   Is bipartite:", isBip)
if partitions then
    print("   Left partition:", table.concat(partitions.left, ", "))
    print("   Right partition:", table.concat(partitions.right, ", "))
end
print()

-- 非二分图 (奇环)
print("5. Non-bipartite graph (odd cycle)...")
local nonBip = GraphUtils.undirected()
nonBip:addEdge("A", "B")
nonBip:addEdge("B", "C")
nonBip:addEdge("C", "A")  -- Triangle (odd cycle)

local isBip2 = nonBip:isBipartite()
print("   Is bipartite:", isBip2)
print("   Triangle makes graph non-bipartite")
print()

-- 图直径
print("6. Graph diameter...")
local diameterGraph = GraphUtils.undirected(true)
diameterGraph:addEdge("A", "B", 1)
diameterGraph:addEdge("B", "C", 2)
diameterGraph:addEdge("C", "D", 3)
diameterGraph:addEdge("D", "E", 4)

local diameter, info = diameterGraph:getDiameter()
print("   Graph diameter:", diameter)
if info then
    print("   Path:", info.from, "->", info.to, "distance:", info.distance)
end
print()

print("Example 6 completed!")
print()
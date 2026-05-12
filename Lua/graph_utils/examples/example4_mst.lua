---
-- Example 4: Minimum Spanning Tree
-- 最小生成树示例
--

local GraphUtils = dofile("mod.lua")

print("=" .. string.rep("=", 50))
print("Example 4: Minimum Spanning Tree")
print("=" .. string.rep("=", 50))
print()

-- 创建带权无向图
local g = GraphUtils.undirected(true)
g:addEdge("A", "B", 4)
g:addEdge("A", "C", 3)
g:addEdge("B", "C", 1)
g:addEdge("B", "D", 2)
g:addEdge("C", "D", 4)
g:addEdge("D", "E", 2)
g:addEdge("C", "E", 5)

print("Weighted undirected graph created")
print("Total vertices:", g.vertexCount)
print("Total edges:", g.edgeCount)
print()

-- Kruskal 算法
print("1. Kruskal's MST algorithm...")
local mst1, weight1, success1 = g:kruskal()
print("   MST found:", success1)
print("   MST edges:")
for _, edge in ipairs(mst1) do
    print("      " .. edge.from .. " - " .. edge.to .. " (weight: " .. edge.weight .. ")")
end
print("   Total weight:", weight1)
print()

-- Prim 算法
print("2. Prim's MST algorithm from A...")
local mst2, weight2, success2 = g:prim("A")
print("   MST found:", success2)
print("   MST edges:")
for _, edge in ipairs(mst2) do
    print("      " .. edge.from .. " - " .. edge.to .. " (weight: " .. edge.weight .. ")")
end
print("   Total weight:", weight2)
print()

-- 验证两种算法结果相同
print("3. Verify both algorithms produce same total weight...")
print("   Kruskal weight:", weight1)
print("   Prim weight:", weight2)
print("   Match:", weight1 == weight2)
print()

print("Example 4 completed!")
print()
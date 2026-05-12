---
-- Example 1: Basic Graph Operations
-- 基本图操作示例
--

local GraphUtils = dofile("mod.lua")

print("=" .. string.rep("=", 50))
print("Example 1: Basic Graph Operations")
print("=" .. string.rep("=", 50))
print()

-- 创建无向图
local g = GraphUtils.undirected()

-- 添加顶点和边
print("1. Creating graph...")
g:addEdge("A", "B")
g:addEdge("A", "C")
g:addEdge("B", "D")
g:addEdge("C", "D")
g:addEdge("B", "E")

print("   Graph created with 5 vertices and 5 edges")
print("   Vertices:", table.concat(g:getVertices(), ", "))
print("   Vertex count:", g.vertexCount)
print("   Edge count:", g.edgeCount)
print()

-- 查询邻居
print("2. Query neighbors...")
local neighborsA = g:getNeighbors("A")
print("   Neighbors of A:", table.concat(neighborsA, ", "))
local degreeA = g:getDegree("A")
print("   Degree of A:", degreeA)
print()

-- 检查边是否存在
print("3. Check edges...")
print("   Has edge A-B:", g:hasEdge("A", "B"))
print("   Has edge A-D:", g:hasEdge("A", "D"))
print()

-- 删除边
print("4. Remove edge B-E...")
g:removeEdge("B", "E")
print("   Edge count after removal:", g.edgeCount)
print("   Has edge B-E:", g:hasEdge("B", "E"))
print()

-- 克隆图
print("5. Clone graph...")
local g2 = g:clone()
print("   Cloned graph vertices:", g2.vertexCount)
print("   Cloned graph edges:", g2.edgeCount)
print()

print("Example 1 completed!")
print()
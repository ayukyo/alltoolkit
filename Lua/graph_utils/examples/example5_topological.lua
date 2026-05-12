---
-- Example 5: Topological Sort and Cycle Detection
-- 拓扑排序和环检测示例
--

local GraphUtils = dofile("mod.lua")

print("=" .. string.rep("=", 50))
print("Example 5: Topological Sort and Cycle Detection")
print("=" .. string.rep("=", 50))
print()

-- 创建 DAG
print("1. Creating a DAG (Directed Acyclic Graph)...")
local dag = GraphUtils.directed()
dag:addEdge("A", "B")
dag:addEdge("A", "C")
dag:addEdge("B", "D")
dag:addEdge("C", "D")
dag:addEdge("D", "E")

print("   Graph structure:")
print("      A -> B -> D -> E")
print("      A -> C -> D")
print()

-- 拓扑排序 (DFS)
print("2. Topological sort (DFS-based)...")
local topoOrder1 = dag:topologicalSort()
if topoOrder1 then
    print("   Topological order:", table.concat(topoOrder1, " -> "))
else
    print("   Graph has cycle!")
end
print()

-- Kahn 算法
print("3. Kahn's algorithm (BFS-based)...")
local topoOrder2 = dag:kahnSort()
if topoOrder2 then
    print("   Topological order:", table.concat(topoOrder2, " -> "))
else
    print("   Graph has cycle!")
end
print()

-- 检查 DAG
print("4. Check if graph is DAG...")
print("   Is DAG:", dag:isDAG())
print("   Has cycle:", dag:hasCycle())
print()

-- 创建有环图
print("5. Creating a graph with cycle...")
local cyclic = GraphUtils.directed()
cyclic:addEdge("A", "B")
cyclic:addEdge("B", "C")
cyclic:addEdge("C", "A")  -- Cycle!
cyclic:addEdge("C", "D")

print("   Graph: A -> B -> C -> A (cycle)")
print()

print("6. Cycle detection on cyclic graph...")
print("   Has cycle:", cyclic:hasCycle())
print("   Is DAG:", cyclic:isDAG())
print()

print("7. Topological sort on cyclic graph...")
local topoCyclic = cyclic:topologicalSort()
if topoCyclic then
    print("   Order:", table.concat(topoCyclic, " -> "))
else
    print("   Cannot topologically sort - graph has cycle!")
end
print()

-- 查找所有环
print("8. Find all cycles...")
local cycles = cyclic:findCycles()
for i, cycle in ipairs(cycles) do
    print("   Cycle " .. i .. ": " .. table.concat(cycle, " -> "))
end
print()

print("Example 5 completed!")
print()
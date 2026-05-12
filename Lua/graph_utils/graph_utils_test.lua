---
-- Graph Utilities Test Suite
-- 图算法工具库测试
--
-- 测试覆盖：
-- - 图创建和基本操作
-- - 遍历算法 (BFS, DFS)
-- - 最短路径算法 (Dijkstra, Bellman-Ford, Floyd-Warshall)
-- - 最小生成树 (Kruskal, Prim)
-- - 拓扑排序
-- - 连通性检测
-- - 环检测
-- - 其他算法 (二分图, 欧拉路径, 直径)
--

local GraphUtils = dofile("Lua/graph_utils/mod.lua")

-- 测试计数器
local testsPassed = 0
local testsFailed = 0
local totalTests = 0

--- 测试辅助函数
local function test(name, func)
    totalTests = totalTests + 1
    local ok, err = pcall(func)
    if ok then
        testsPassed = testsPassed + 1
        print("✓ " .. name)
    else
        testsFailed = testsFailed + 1
        print("✗ " .. name)
        print("  Error: " .. tostring(err))
    end
end

local function assertEquals(expected, actual, message)
    if expected ~= actual then
        error((message or "") .. " Expected: " .. tostring(expected) .. ", Got: " .. tostring(actual))
    end
end

local function assertNotNil(value, message)
    if value == nil then
        error((message or "") .. " Expected non-nil value")
    end
end

local function assertNil(value, message)
    if value ~= nil then
        error((message or "") .. " Expected nil, got: " .. tostring(value))
    end
end

local function assertTrue(value, message)
    if not value then
        error((message or "") .. " Expected true")
    end
end

local function assertFalse(value, message)
    if value then
        error((message or "") .. " Expected false")
    end
end

local function assertTableEquals(t1, t2, message)
    local function tableEq(a, b)
        if type(a) ~= "table" or type(b) ~= "table" then
            return a == b
        end
        for k, v in pairs(a) do
            if not tableEq(v, b[k]) then return false end
        end
        for k, v in pairs(b) do
            if not tableEq(v, a[k]) then return false end
        end
        return true
    end
    if not tableEq(t1, t2) then
        error((message or "") .. " Tables not equal")
    end
end

print("=" .. string.rep("=", 69))
print("Graph Utilities Test Suite")
print("=" .. string.rep("=", 69))
print()

-------------------------------------------------------------------------------
-- 测试 1: 图创建和基本操作
-------------------------------------------------------------------------------
print("[1] Graph Creation and Basic Operations")
print("-" .. string.rep("-", 69))

test("Create undirected graph", function()
    local g = GraphUtils.undirected()
    assertNotNil(g)
    assertEquals("undirected", g.graphType)
    assertFalse(g.weighted)
end)

test("Create directed graph", function()
    local g = GraphUtils.directed()
    assertNotNil(g)
    assertEquals("directed", g.graphType)
    assertFalse(g.weighted)
end)

test("Create weighted graph", function()
    local g = GraphUtils.directed(true)
    assertTrue(g.weighted)
end)

test("Add vertices", function()
    local g = GraphUtils.undirected()
    g:addVertex("A"):addVertex("B"):addVertex("C")
    assertEquals(3, g.vertexCount)
    assertTrue(g.vertices["A"])
    assertTrue(g.vertices["B"])
    assertTrue(g.vertices["C"])
end)

test("Remove vertex", function()
    local g = GraphUtils.undirected()
    g:addVertex("A"):addVertex("B")
    g:addEdge("A", "B")
    assertTrue(g:removeVertex("A"))
    assertEquals(1, g.vertexCount)
    assertFalse(g:hasEdge("A", "B"))
end)

test("Add edges", function()
    local g = GraphUtils.undirected()
    g:addEdge("A", "B")
    assertTrue(g:hasEdge("A", "B"))
    assertTrue(g:hasEdge("B", "A"))
    assertEquals(1, g.edgeCount)
end)

test("Add directed edges", function()
    local g = GraphUtils.directed()
    g:addEdge("A", "B")
    assertTrue(g:hasEdge("A", "B"))
    assertFalse(g:hasEdge("B", "A"))
end)

test("Add weighted edges", function()
    local g = GraphUtils.directed(true)
    g:addEdge("A", "B", 5)
    assertEquals(5, g:getWeight("A", "B"))
end)

test("Remove edge", function()
    local g = GraphUtils.undirected()
    g:addEdge("A", "B")
    assertTrue(g:removeEdge("A", "B"))
    assertFalse(g:hasEdge("A", "B"))
    assertEquals(0, g.edgeCount)
end)

test("Get neighbors", function()
    local g = GraphUtils.undirected()
    g:addEdge("A", "B"):addEdge("A", "C")
    local neighbors = g:getNeighbors("A")
    assertEquals(2, #neighbors)
end)

test("Get degree", function()
    local g = GraphUtils.undirected()
    g:addEdge("A", "B"):addEdge("A", "C"):addEdge("A", "D")
    assertEquals(3, g:getDegree("A"))
end)

test("Get in-degree (directed)", function()
    local g = GraphUtils.directed()
    g:addEdge("B", "A"):addEdge("C", "A"):addEdge("D", "A")
    assertEquals(3, g:getInDegree("A"))
end)

test("Is empty", function()
    local g = GraphUtils.undirected()
    assertTrue(g:isEmpty())
    g:addVertex("A")
    assertFalse(g:isEmpty())
end)

test("Clear graph", function()
    local g = GraphUtils.undirected()
    g:addEdge("A", "B")
    g:clear()
    assertEquals(0, g.vertexCount)
    assertEquals(0, g.edgeCount)
end)

test("Clone graph", function()
    local g = GraphUtils.directed(true)
    g:addEdge("A", "B", 3):addEdge("B", "C", 5)
    local clone = g:clone()
    assertEquals(g.vertexCount, clone.vertexCount)
    assertEquals(g.edgeCount, clone.edgeCount)
    assertTrue(clone:hasEdge("A", "B"))
    assertEquals(3, clone:getWeight("A", "B"))
end)

test("To table and from table", function()
    local g = GraphUtils.directed(true)
    g:addEdge("A", "B", 2):addEdge("B", "C", 3)
    local t = g:toTable()
    local g2 = GraphUtils.fromTable(t)
    assertEquals(g.vertexCount, g2.vertexCount)
    assertEquals(g.edgeCount, g2.edgeCount)
    assertTrue(g2:hasEdge("A", "B"))
    assertEquals(2, g2:getWeight("A", "B"))
end)

print()

-------------------------------------------------------------------------------
-- 测试 2: 遍历算法
-------------------------------------------------------------------------------
print("[2] Traversal Algorithms")
print("-" .. string.rep("-", 69))

test("BFS traversal", function()
    local g = GraphUtils.undirected()
    g:addEdge("A", "B"):addEdge("A", "C")
    g:addEdge("B", "D"):addEdge("C", "E")
    local result = g:bfs("A")
    assertEquals(5, #result)
    assertEquals("A", result[1])
end)

test("BFS with callback", function()
    local g = GraphUtils.undirected()
    g:addEdge("A", "B"):addEdge("B", "C")
    local count = 0
    local depths = {}
    g:bfs("A", function(vertex, depth)
        count = count + 1
        depths[vertex] = depth
    end)
    assertEquals(3, count)
    assertEquals(0, depths["A"])
    assertEquals(1, depths["B"])
    assertEquals(2, depths["C"])
end)

test("DFS traversal (iterative)", function()
    local g = GraphUtils.undirected()
    g:addEdge("A", "B"):addEdge("A", "C")
    g:addEdge("B", "D"):addEdge("C", "E")
    local result = g:dfs("A")
    assertEquals(5, #result)
    assertEquals("A", result[1])
end)

test("DFS traversal (recursive)", function()
    local g = GraphUtils.undirected()
    g:addEdge("A", "B"):addEdge("A", "C")
    g:addEdge("B", "D"):addEdge("C", "E")
    local result = g:dfsRecursive("A")
    assertEquals(5, #result)
    assertEquals("A", result[1])
end)

test("BFS level order", function()
    local g = GraphUtils.undirected()
    g:addEdge("A", "B"):addEdge("A", "C")
    g:addEdge("B", "D"):addEdge("C", "E")
    local levels = g:bfsLevelOrder("A")
    assertEquals(1, #levels[1])
    assertEquals(2, #levels[2])
    assertEquals(2, #levels[3])
end)

print()

-------------------------------------------------------------------------------
-- 测试 3: 最短路径算法
-------------------------------------------------------------------------------
print("[3] Shortest Path Algorithms")
print("-" .. string.rep("-", 69))

test("Dijkstra - simple path", function()
    local g = GraphUtils.directed(true)
    g:addEdge("A", "B", 1):addEdge("B", "C", 2)
    g:addEdge("A", "C", 5)
    local distances = g:dijkstra("A")
    assertEquals(0, distances["A"])
    assertEquals(1, distances["B"])
    assertEquals(3, distances["C"])
end)

test("Dijkstra - get shortest path", function()
    local g = GraphUtils.directed(true)
    g:addEdge("A", "B", 1):addEdge("B", "C", 2)
    g:addEdge("A", "C", 5)
    local path, dist = g:getShortestPath("A", "C")
    assertEquals(3, dist)
    assertEquals(3, #path)
    assertEquals("A", path[1])
    assertEquals("B", path[2])
    assertEquals("C", path[3])
end)

test("Dijkstra - unreachable vertex", function()
    local g = GraphUtils.directed(true)
    g:addEdge("A", "B", 1)
    g:addVertex("C")  -- 孤立顶点
    local distances = g:dijkstra("A")
    assertEquals(math.huge, distances["C"])
end)

test("Dijkstra - get shortest path unreachable", function()
    local g = GraphUtils.directed(true)
    g:addEdge("A", "B", 1)
    g:addVertex("C")
    local path, dist = g:getShortestPath("A", "C")
    assertNil(path)
    assertNil(dist)
end)

test("Bellman-Ford - basic", function()
    local g = GraphUtils.directed(true)
    g:addEdge("A", "B", 4):addEdge("B", "C", 2)
    g:addEdge("A", "C", 7)
    local distances, _, hasNegCycle = g:bellmanFord("A")
    assertFalse(hasNegCycle)
    assertEquals(0, distances["A"])
    assertEquals(4, distances["B"])
    assertEquals(6, distances["C"])
end)

test("Bellman-Ford - negative weight", function()
    local g = GraphUtils.directed(true)
    g:addEdge("A", "B", 1):addEdge("B", "C", -2)
    g:addEdge("A", "C", 2)
    local distances = g:dijkstra("A")  -- Dijkstra 不支持负权
    local distances2, _, hasNegCycle = g:bellmanFord("A")
    assertFalse(hasNegCycle)
    assertEquals(-1, distances2["C"])
end)

test("Bellman-Ford - detect negative cycle", function()
    local g = GraphUtils.directed(true)
    g:addEdge("A", "B", 1)
    g:addEdge("B", "C", -3)
    g:addEdge("C", "A", 1)  -- 负权环: A -> B -> C -> A = -1
    local _, _, hasNegCycle = g:bellmanFord("A")
    assertTrue(hasNegCycle)
end)

test("Floyd-Warshall - all pairs", function()
    local g = GraphUtils.directed(true)
    g:addEdge("A", "B", 1):addEdge("B", "C", 2)
    g:addEdge("A", "C", 5)
    local dist = g:floydWarshall()
    assertEquals(0, dist["A"]["A"])
    assertEquals(1, dist["A"]["B"])
    assertEquals(3, dist["A"]["C"])
end)

print()

-------------------------------------------------------------------------------
-- 测试 4: 最小生成树
-------------------------------------------------------------------------------
print("[4] Minimum Spanning Tree")
print("-" .. string.rep("-", 69))

test("Kruskal - simple MST", function()
    local g = GraphUtils.undirected(true)
    g:addEdge("A", "B", 1):addEdge("B", "C", 2)
    g:addEdge("A", "C", 3)
    local mst, weight, success = g:kruskal()
    assertTrue(success)
    assertEquals(2, #mst)  -- 2 edges for 3 vertices
    assertEquals(3, weight)
end)

test("Kruskal - disconnected graph", function()
    local g = GraphUtils.undirected(true)
    g:addEdge("A", "B", 1)
    g:addVertex("C")  -- 孤立顶点
    local mst, _, success = g:kruskal()
    assertFalse(success)
end)

test("Prim - simple MST", function()
    local g = GraphUtils.undirected(true)
    g:addEdge("A", "B", 1):addEdge("B", "C", 2)
    g:addEdge("A", "C", 3)
    local mst, weight, success = g:prim("A")
    assertTrue(success)
    assertEquals(2, #mst)  -- 2 edges for 3 vertices
    assertEquals(3, weight)
end)

test("Prim - with start vertex", function()
    local g = GraphUtils.undirected(true)
    g:addEdge("A", "B", 4):addEdge("B", "C", 3)
    g:addEdge("A", "C", 5)
    local mst, weight, success = g:prim("B")
    assertTrue(success)
    assertEquals(7, weight)
end)

print()

-------------------------------------------------------------------------------
-- 测试 5: 拓扑排序
-------------------------------------------------------------------------------
print("[5] Topological Sort")
print("-" .. string.rep("-", 69))

test("Topological sort - simple DAG", function()
    local g = GraphUtils.directed()
    g:addEdge("A", "B"):addEdge("A", "C")
    g:addEdge("B", "D"):addEdge("C", "D")
    local result = g:topologicalSort()
    assertNotNil(result)
    assertEquals(4, #result)
    -- A 应该在 B 和 C 之前
    local posA, posB, posC = 1, 1, 1
    for i, v in ipairs(result) do
        if v == "A" then posA = i
        elseif v == "B" then posB = i
        elseif v == "C" then posC = i
        end
    end
    assertTrue(posA < posB)
    assertTrue(posA < posC)
end)

test("Topological sort - graph with cycle", function()
    local g = GraphUtils.directed()
    g:addEdge("A", "B"):addEdge("B", "C")
    g:addEdge("C", "A")  -- 环
    local result = g:topologicalSort()
    assertNil(result)
end)

test("Kahn sort - simple DAG", function()
    local g = GraphUtils.directed()
    g:addEdge("A", "B"):addEdge("B", "C")
    local result = g:kahnSort()
    assertNotNil(result)
    assertEquals(3, #result)
end)

test("Kahn sort - graph with cycle", function()
    local g = GraphUtils.directed()
    g:addEdge("A", "B"):addEdge("B", "C")
    g:addEdge("C", "A")
    local result = g:kahnSort()
    assertNil(result)
end)

print()

-------------------------------------------------------------------------------
-- 测试 6: 连通性
-------------------------------------------------------------------------------
print("[6] Connectivity")
print("-" .. string.rep("-", 69))

test("Connected components - single component", function()
    local g = GraphUtils.undirected()
    g:addEdge("A", "B"):addEdge("B", "C")
    local components = g:connectedComponents()
    assertEquals(1, #components)
end)

test("Connected components - multiple components", function()
    local g = GraphUtils.undirected()
    g:addEdge("A", "B"):addEdge("C", "D")
    local components = g:connectedComponents()
    assertEquals(2, #components)
end)

test("Is connected - true", function()
    local g = GraphUtils.undirected()
    g:addEdge("A", "B"):addEdge("B", "C")
    assertTrue(g:isConnected())
end)

test("Is connected - false", function()
    local g = GraphUtils.undirected()
    g:addEdge("A", "B")
    g:addVertex("C")  -- 孤立顶点
    assertFalse(g:isConnected())
end)

test("Strongly connected components", function()
    local g = GraphUtils.directed()
    g:addEdge("A", "B"):addEdge("B", "C")
    g:addEdge("C", "A")  -- 强连通分量 A-B-C
    g:addEdge("C", "D")  -- D 是单独的 SCC
    local sccs = g:stronglyConnectedComponents()
    assertEquals(2, #sccs)
end)

print()

-------------------------------------------------------------------------------
-- 测试 7: 环检测
-------------------------------------------------------------------------------
print("[7] Cycle Detection")
print("-" .. string.rep("-", 69))

test("Has cycle - undirected with cycle", function()
    local g = GraphUtils.undirected()
    g:addEdge("A", "B"):addEdge("B", "C")
    g:addEdge("C", "A")  -- 环
    assertTrue(g:hasCycle())
end)

test("Has cycle - undirected without cycle", function()
    local g = GraphUtils.undirected()
    g:addEdge("A", "B"):addEdge("B", "C")
    assertFalse(g:hasCycle())
end)

test("Has cycle - directed with cycle", function()
    local g = GraphUtils.directed()
    g:addEdge("A", "B"):addEdge("B", "C")
    g:addEdge("C", "A")
    assertTrue(g:hasCycle())
end)

test("Has cycle - directed without cycle", function()
    local g = GraphUtils.directed()
    g:addEdge("A", "B"):addEdge("B", "C")
    assertFalse(g:hasCycle())
end)

test("Is DAG - true", function()
    local g = GraphUtils.directed()
    g:addEdge("A", "B"):addEdge("B", "C")
    assertTrue(g:isDAG())
end)

test("Is DAG - false", function()
    local g = GraphUtils.directed()
    g:addEdge("A", "B"):addEdge("B", "A")
    assertFalse(g:isDAG())
end)

test("Find cycles - directed", function()
    local g = GraphUtils.directed()
    g:addEdge("A", "B"):addEdge("B", "C")
    g:addEdge("C", "A")
    local cycles = g:findCycles()
    assertTrue(#cycles > 0)
end)

print()

-------------------------------------------------------------------------------
-- 测试 8: 其他算法
-------------------------------------------------------------------------------
print("[8] Other Algorithms")
print("-" .. string.rep("-", 69))

test("Is bipartite - true", function()
    local g = GraphUtils.undirected()
    g:addEdge("A", "B"):addEdge("B", "C")
    g:addEdge("C", "D"):addEdge("D", "A")
    local isBipartite, partitions = g:isBipartite()
    assertTrue(isBipartite)
    assertNotNil(partitions)
end)

test("Is bipartite - false (odd cycle)", function()
    local g = GraphUtils.undirected()
    g:addEdge("A", "B"):addEdge("B", "C")
    g:addEdge("C", "A")  -- 奇环
    local isBipartite = g:isBipartite()
    assertFalse(isBipartite)
end)

test("Get diameter", function()
    local g = GraphUtils.undirected(true)
    g:addEdge("A", "B", 1):addEdge("B", "C", 2)
    g:addEdge("C", "D", 3)
    local diameter, path = g:getDiameter()
    assertEquals(6, diameter)
    assertNotNil(path)
    assertEquals(6, path.distance)
end)

test("Get Eulerian path - exists", function()
    local g = GraphUtils.undirected()
    -- 所有顶点偶度 -> 欧拉回路存在
    -- 2 个奇度顶点 -> 欧拉路径存在
    -- 创建一个有欧拉路径的图（2 个奇度顶点）
    g:addEdge("A", "B"):addEdge("B", "C")
    g:addEdge("C", "A")  -- 三角形
    g:addEdge("A", "D")  -- D 是奇度顶点
    -- A: 度数 3 (奇), B: 度数 2 (偶), C: 度数 2 (偶), D: 度数 1 (奇)
    -- 有 2 个奇度顶点，存在欧拉路径
    local path = g:getEulerianPath()
    assertNotNil(path)
    assertTrue(#path > 0)
end)

print()

-------------------------------------------------------------------------------
-- 测试 9: 工厂函数
-------------------------------------------------------------------------------
print("[9] Factory Functions")
print("-" .. string.rep("-", 69))

test("fromEdgeList", function()
    local edges = {
        {"A", "B", 1},
        {"B", "C", 2},
        {"A", "C", 3},
    }
    local g = GraphUtils.fromEdgeList(edges, GraphUtils.GraphType.UNDIRECTED, true)
    assertEquals(3, g.vertexCount)
    assertEquals(3, g.edgeCount)
    assertTrue(g.weighted)
end)

test("fromAdjacencyMatrix", function()
    local matrix = {
        {0, 1, 2},
        {0, 0, 3},
        {0, 0, 0},
    }
    local g = GraphUtils.fromAdjacencyMatrix(matrix, {"A", "B", "C"})
    assertTrue(g:hasEdge("A", "B"))
    assertTrue(g:hasEdge("A", "C"))
    assertTrue(g:hasEdge("B", "C"))
    assertEquals(1, g:getWeight("A", "B"))
    assertEquals(2, g:getWeight("A", "C"))
end)

print()

-------------------------------------------------------------------------------
-- 测试 10: 边界情况
-------------------------------------------------------------------------------
print("[10] Edge Cases")
print("-" .. string.rep("-", 69))

test("Empty graph operations", function()
    local g = GraphUtils.undirected()
    assertEquals(0, g.vertexCount)
    assertEquals(0, g.edgeCount)
    assertTrue(g:isEmpty())
    assertEquals(0, #g:getVertices())
    assertEquals(0, #g:getEdges())
end)

test("Single vertex graph", function()
    local g = GraphUtils.undirected()
    g:addVertex("A")
    assertEquals(1, g.vertexCount)
    assertEquals(0, g:getDegree("A"))
    local components = g:connectedComponents()
    assertEquals(1, #components)
end)

test("Self-loop", function()
    local g = GraphUtils.directed()
    g:addEdge("A", "A")
    assertTrue(g:hasEdge("A", "A"))
    -- 有向图自环：出度 1，入度 1
    assertEquals(1, g:getDegree("A"))  -- 出度
    assertEquals(1, g:getInDegree("A"))  -- 入度
end)

test("BFS on single vertex", function()
    local g = GraphUtils.undirected()
    g:addVertex("A")
    local result = g:bfs("A")
    assertEquals(1, #result)
    assertEquals("A", result[1])
end)

test("DFS on single vertex", function()
    local g = GraphUtils.undirected()
    g:addVertex("A")
    local result = g:dfs("A")
    assertEquals(1, #result)
    assertEquals("A", result[1])
end)

test("Dijkstra on single vertex", function()
    local g = GraphUtils.directed(true)
    g:addVertex("A")
    local distances = g:dijkstra("A")
    assertEquals(0, distances["A"])
end)

test("Topological sort on single vertex", function()
    local g = GraphUtils.directed()
    g:addVertex("A")
    local result = g:topologicalSort()
    assertNotNil(result)
    assertEquals(1, #result)
end)

test("Large graph performance", function()
    local g = GraphUtils.directed(true)
    -- 创建一个较大的图
    for i = 1, 100 do
        for j = 1, 3 do
            local target = i + j
            if target <= 100 then
                g:addEdge(i, target, j)
            end
        end
    end
    assertEquals(100, g.vertexCount)
    -- BFS 应该能正常工作
    local result = g:bfs(1)
    assertEquals(100, #result)
end)

print()
print("=" .. string.rep("=", 69))
print(string.format("Tests completed: %d passed, %d failed, %d total",
    testsPassed, testsFailed, totalTests))
print("=" .. string.rep("=", 69))

if testsFailed > 0 then
    os.exit(1)
end
---
-- Graph Utilities Module
-- 图算法工具函数库
--
-- 提供完整的图数据结构和算法实现，支持有向图和无向图的常见操作。
-- 仅使用 Lua 标准库，零依赖。
--
-- Features:
-- - Graph types: directed, undirected, weighted
-- - Representations: adjacency list, adjacency matrix
-- - Traversal: bfs, dfs, dfs_recursive, bfs_level_order
-- - Shortest path: dijkstra, bellman_ford, floyd_warshall
-- - Minimum spanning tree: kruskal, prim
-- - Topology: topological_sort, kahn_sort
-- - Connectivity: connected_components, strongly_connected_components
-- - Cycle detection: has_cycle, find_cycles, is_dag
-- - Graph properties: is_bipartite, get_degree, get_eulerian_path
-- - Utility: add_edge, remove_edge, has_edge, get_neighbors
-- - Serialization: to_table, from_table, clone
--
-- @author AllToolkit
-- @version 1.0.0
-- @copyright MIT License

local GraphUtils = {}
local GraphUtilsMT = { __index = GraphUtils }

--- 版本号
GraphUtils.VERSION = "1.0.0"

--- 图类型
GraphUtils.GraphType = {
    UNDIRECTED = "undirected",   -- 无向图
    DIRECTED = "directed",       -- 有向图
}

--- 错误类型
GraphUtils.Error = {
    InvalidVertex = "Invalid vertex: vertex cannot be nil",
    InvalidEdge = "Invalid edge: vertices must be different",
    VertexNotFound = "Vertex not found in graph",
    EdgeNotFound = "Edge not found in graph",
    InvalidGraph = "Invalid graph object",
    InvalidWeight = "Invalid weight: must be a number",
    CycleDetected = "Cycle detected in graph",
    NotConnected = "Graph is not connected",
}

-------------------------------------------------------------------------------
-- Graph 类定义
-------------------------------------------------------------------------------

local Graph = {}
Graph.__index = Graph

--- 创建新的图
-- @param graphType 图类型 (GraphUtils.GraphType.UNDIRECTED 或 DIRECTED)
-- @param weighted 是否为带权图 (默认 false)
-- @return Graph 新图对象
function Graph.new(graphType, weighted)
    local g = {
        vertices = {},          -- 顶点集合 {vertex = true}
        adjacency = {},         -- 邻接表 {vertex = {neighbor = weight}}
        graphType = graphType or GraphUtils.GraphType.UNDIRECTED,
        weighted = weighted or false,
        vertexCount = 0,
        edgeCount = 0,
    }
    setmetatable(g, Graph)
    return g
end

--- 添加顶点
-- @param vertex 顶点
-- @return Graph self
function Graph:addVertex(vertex)
    if vertex == nil then
        error(GraphUtils.Error.InvalidVertex)
    end
    if not self.vertices[vertex] then
        self.vertices[vertex] = true
        self.adjacency[vertex] = {}
        self.vertexCount = self.vertexCount + 1
    end
    return self
end

--- 删除顶点
-- @param vertex 顶点
-- @return boolean 是否删除成功
function Graph:removeVertex(vertex)
    if not self.vertices[vertex] then
        return false
    end
    
    -- 删除所有与该顶点相关的边
    for v, _ in pairs(self.vertices) do
        if self.adjacency[v] and self.adjacency[v][vertex] then
            self.adjacency[v][vertex] = nil
            self.edgeCount = self.edgeCount - 1
        end
    end
    
    -- 统计该顶点的出边数
    if self.adjacency[vertex] then
        for _, _ in pairs(self.adjacency[vertex]) do
            self.edgeCount = self.edgeCount - 1
        end
    end
    
    self.vertices[vertex] = nil
    self.adjacency[vertex] = nil
    self.vertexCount = self.vertexCount - 1
    return true
end

--- 添加边
-- @param from 起点
-- @param to 终点
-- @param weight 权重 (可选，默认 1)
-- @return Graph self
function Graph:addEdge(from, to, weight)
    if from == nil or to == nil then
        error(GraphUtils.Error.InvalidEdge)
    end
    
    weight = weight or 1
    if self.weighted and type(weight) ~= "number" then
        error(GraphUtils.Error.InvalidWeight)
    end
    
    -- 确保顶点存在
    self:addVertex(from)
    self:addVertex(to)
    
    -- 检查边是否已存在
    local edgeExists = self.adjacency[from][to] ~= nil
    
    self.adjacency[from][to] = weight
    
    if self.graphType == GraphUtils.GraphType.UNDIRECTED then
        self.adjacency[to][from] = weight
        if not edgeExists then
            self.edgeCount = self.edgeCount + 1
        end
    else
        if not edgeExists then
            self.edgeCount = self.edgeCount + 1
        end
    end
    
    return self
end

--- 删除边
-- @param from 起点
-- @param to 终点
-- @return boolean 是否删除成功
function Graph:removeEdge(from, to)
    if not self.vertices[from] or not self.vertices[to] then
        return false
    end
    
    if self.adjacency[from] and self.adjacency[from][to] then
        self.adjacency[from][to] = nil
        if self.graphType == GraphUtils.GraphType.UNDIRECTED then
            self.adjacency[to][from] = nil
        end
        self.edgeCount = self.edgeCount - 1
        return true
    end
    
    return false
end

--- 检查边是否存在
-- @param from 起点
-- @param to 终点
-- @return boolean 边是否存在
function Graph:hasEdge(from, to)
    if not self.vertices[from] or not self.vertices[to] then
        return false
    end
    return self.adjacency[from] and self.adjacency[from][to] ~= nil
end

--- 获取边的权重
-- @param from 起点
-- @param to 终点
-- @return number|nil 权重，边不存在则返回 nil
function Graph:getWeight(from, to)
    if self.adjacency[from] then
        return self.adjacency[from][to]
    end
    return nil
end

--- 获取顶点的邻居
-- @param vertex 顶点
-- @return table 邻居列表 {neighbor, ...} 或 {neighbor=weight, ...}
function Graph:getNeighbors(vertex)
    if not self.vertices[vertex] then
        return {}
    end
    
    if self.weighted then
        -- 返回副本
        local result = {}
        for neighbor, weight in pairs(self.adjacency[vertex]) do
            result[neighbor] = weight
        end
        return result
    else
        local result = {}
        for neighbor, _ in pairs(self.adjacency[vertex]) do
            table.insert(result, neighbor)
        end
        return result
    end
end

--- 获取所有顶点
-- @return table 顶点列表
function Graph:getVertices()
    local result = {}
    for vertex, _ in pairs(self.vertices) do
        table.insert(result, vertex)
    end
    return result
end

--- 获取所有边
-- @return table 边列表 {{from, to, weight}, ...}
function Graph:getEdges()
    local result = {}
    local seen = {}
    
    for from, neighbors in pairs(self.adjacency) do
        for to, weight in pairs(neighbors) do
            local key
            if self.graphType == GraphUtils.GraphType.UNDIRECTED then
                -- 避免重复边
                key = from < to and (from .. ":" .. to) or (to .. ":" .. from)
                if not seen[key] then
                    seen[key] = true
                    table.insert(result, {from = from, to = to, weight = weight})
                end
            else
                table.insert(result, {from = from, to = to, weight = weight})
            end
        end
    end
    
    return result
end

--- 获取顶点度数
-- @param vertex 顶点
-- @return number 度数 (无向图) 或出度 (有向图)
function Graph:getDegree(vertex)
    if not self.vertices[vertex] then
        return 0
    end
    local degree = 0
    for _ in pairs(self.adjacency[vertex]) do
        degree = degree + 1
    end
    return degree
end

--- 获取入度 (仅用于有向图)
-- @param vertex 顶点
-- @return number 入度
function Graph:getInDegree(vertex)
    if not self.vertices[vertex] then
        return 0
    end
    local inDegree = 0
    for v, _ in pairs(self.vertices) do
        if self.adjacency[v] and self.adjacency[v][vertex] then
            inDegree = inDegree + 1
        end
    end
    return inDegree
end

--- 检查是否为空图
-- @return boolean
function Graph:isEmpty()
    return self.vertexCount == 0
end

--- 清空图
function Graph:clear()
    self.vertices = {}
    self.adjacency = {}
    self.vertexCount = 0
    self.edgeCount = 0
end

--- 克隆图
-- @return Graph 克隆后的图
function Graph:clone()
    local newGraph = Graph.new(self.graphType, self.weighted)
    
    -- 复制顶点
    for vertex, _ in pairs(self.vertices) do
        newGraph:addVertex(vertex)
    end
    
    -- 复制边
    for from, neighbors in pairs(self.adjacency) do
        for to, weight in pairs(neighbors) do
            newGraph:addEdge(from, to, weight)
        end
    end
    
    return newGraph
end

--- 导出为表
-- @return table 表表示
function Graph:toTable()
    return {
        vertices = self:getVertices(),
        edges = self:getEdges(),
        graphType = self.graphType,
        weighted = self.weighted,
    }
end

--- 从表导入
-- @param t 表
-- @return Graph 图对象
function Graph.fromTable(t)
    local g = Graph.new(t.graphType, t.weighted)
    for _, edge in ipairs(t.edges) do
        g:addEdge(edge.from, edge.to, edge.weight)
    end
    return g
end

-- 导出 Graph.fromTable 到模块
GraphUtils.Graph = Graph
GraphUtils.fromTable = Graph.fromTable

-------------------------------------------------------------------------------
-- 遍历算法
-------------------------------------------------------------------------------

--- 广度优先搜索 (BFS)
-- @param start 起始顶点
-- @param callback 访问回调函数 callback(vertex, depth)
-- @return table 访问顺序
function Graph:bfs(start, callback)
    if not self.vertices[start] then
        return {}
    end
    
    local visited = {}
    local queue = {{vertex = start, depth = 0}}
    local result = {}
    visited[start] = true
    
    while #queue > 0 do
        local current = table.remove(queue, 1)
        local vertex = current.vertex
        local depth = current.depth
        
        table.insert(result, vertex)
        
        if callback then
            callback(vertex, depth)
        end
        
        for neighbor, _ in pairs(self.adjacency[vertex]) do
            if not visited[neighbor] then
                visited[neighbor] = true
                table.insert(queue, {vertex = neighbor, depth = depth + 1})
            end
        end
    end
    
    return result
end

--- 深度优先搜索 (DFS) - 迭代版本
-- @param start 起始顶点
-- @param callback 访问回调函数 callback(vertex)
-- @return table 访问顺序
function Graph:dfs(start, callback)
    if not self.vertices[start] then
        return {}
    end
    
    local visited = {}
    local stack = {start}
    local result = {}
    
    while #stack > 0 do
        local vertex = table.remove(stack)
        
        if not visited[vertex] then
            visited[vertex] = true
            table.insert(result, vertex)
            
            if callback then
                callback(vertex)
            end
            
            -- 将邻居逆序入栈，保证访问顺序
            local neighbors = {}
            for neighbor, _ in pairs(self.adjacency[vertex]) do
                table.insert(neighbors, neighbor)
            end
            
            for i = #neighbors, 1, -1 do
                if not visited[neighbors[i]] then
                    table.insert(stack, neighbors[i])
                end
            end
        end
    end
    
    return result
end

--- 深度优先搜索 (DFS) - 递归版本
-- @param start 起始顶点
-- @param callback 访问回调函数 callback(vertex)
-- @return table 访问顺序
function Graph:dfsRecursive(start, callback)
    if not self.vertices[start] then
        return {}
    end
    
    local visited = {}
    local result = {}
    
    local function dfsHelper(vertex)
        visited[vertex] = true
        table.insert(result, vertex)
        
        if callback then
            callback(vertex)
        end
        
        for neighbor, _ in pairs(self.adjacency[vertex]) do
            if not visited[neighbor] then
                dfsHelper(neighbor)
            end
        end
    end
    
    dfsHelper(start)
    return result
end

--- 层序遍历 (按层返回)
-- @param start 起始顶点
-- @return table 每层的顶点列表 {{...}, {...}, ...}
function Graph:bfsLevelOrder(start)
    if not self.vertices[start] then
        return {}
    end
    
    local visited = {}
    local queue = {{vertex = start, depth = 0}}
    local result = {}
    visited[start] = true
    
    while #queue > 0 do
        local current = table.remove(queue, 1)
        local vertex = current.vertex
        local depth = current.depth
        
        if not result[depth + 1] then
            result[depth + 1] = {}
        end
        table.insert(result[depth + 1], vertex)
        
        for neighbor, _ in pairs(self.adjacency[vertex]) do
            if not visited[neighbor] then
                visited[neighbor] = true
                table.insert(queue, {vertex = neighbor, depth = depth + 1})
            end
        end
    end
    
    return result
end

-------------------------------------------------------------------------------
-- 最短路径算法
-------------------------------------------------------------------------------

--- Dijkstra 最短路径算法
-- @param start 起点
-- @return table 距离表 {vertex = distance}
-- @return table 前驱表 {vertex = predecessor}
function Graph:dijkstra(start)
    if not self.vertices[start] then
        return {}, {}
    end
    
    local distances = {}
    local predecessors = {}
    local visited = {}
    
    -- 初始化距离
    for vertex, _ in pairs(self.vertices) do
        distances[vertex] = math.huge
        predecessors[vertex] = nil
    end
    distances[start] = 0
    
    -- 简单优先队列 (最小堆可以优化)
    local function getMinVertex()
        local minDist = math.huge
        local minVertex = nil
        for vertex, _ in pairs(self.vertices) do
            if not visited[vertex] and distances[vertex] < minDist then
                minDist = distances[vertex]
                minVertex = vertex
            end
        end
        return minVertex
    end
    
    while true do
        local u = getMinVertex()
        if u == nil then
            break
        end
        
        visited[u] = true
        
        for v, weight in pairs(self.adjacency[u]) do
            local alt = distances[u] + weight
            if alt < distances[v] then
                distances[v] = alt
                predecessors[v] = u
            end
        end
    end
    
    return distances, predecessors
end

--- 获取从 start 到 target 的最短路径
-- @param start 起点
-- @param target 终点
-- @return table|nil 路径列表 {start, ..., target}，不可达则返回 nil
-- @return number|nil 总距离，不可达则返回 nil
function Graph:getShortestPath(start, target)
    local distances, predecessors = self:dijkstra(start)
    
    if distances[target] == math.huge then
        return nil, nil
    end
    
    local path = {}
    local current = target
    
    while current do
        table.insert(path, 1, current)
        current = predecessors[current]
    end
    
    return path, distances[target]
end

--- Bellman-Ford 最短路径算法 (支持负权边)
-- @param start 起点
-- @return table 距离表 {vertex = distance}
-- @return table 前驱表 {vertex = predecessor}
-- @return boolean 是否存在负权环
function Graph:bellmanFord(start)
    if not self.vertices[start] then
        return {}, {}, false
    end
    
    local distances = {}
    local predecessors = {}
    
    -- 初始化距离
    for vertex, _ in pairs(self.vertices) do
        distances[vertex] = math.huge
        predecessors[vertex] = nil
    end
    distances[start] = 0
    
    local edges = self:getEdges()
    
    -- 松弛 V-1 次
    for _ = 1, self.vertexCount - 1 do
        for _, edge in ipairs(edges) do
            if distances[edge.from] ~= math.huge then
                local alt = distances[edge.from] + edge.weight
                if alt < distances[edge.to] then
                    distances[edge.to] = alt
                    predecessors[edge.to] = edge.from
                end
            end
        end
    end
    
    -- 检测负权环
    for _, edge in ipairs(edges) do
        if distances[edge.from] ~= math.huge then
            if distances[edge.from] + edge.weight < distances[edge.to] then
                return distances, predecessors, true  -- 存在负权环
            end
        end
    end
    
    return distances, predecessors, false
end

--- Floyd-Warshall 全源最短路径算法
-- @return table 距离矩阵 {from = {to = distance}}
function Graph:floydWarshall()
    local dist = {}
    
    -- 初始化距离矩阵
    for v1, _ in pairs(self.vertices) do
        dist[v1] = {}
        for v2, _ in pairs(self.vertices) do
            if v1 == v2 then
                dist[v1][v2] = 0
            elseif self.adjacency[v1][v2] then
                dist[v1][v2] = self.adjacency[v1][v2]
            else
                dist[v1][v2] = math.huge
            end
        end
    end
    
    -- 动态规划更新
    for k, _ in pairs(self.vertices) do
        for i, _ in pairs(self.vertices) do
            for j, _ in pairs(self.vertices) do
                if dist[i][k] + dist[k][j] < dist[i][j] then
                    dist[i][j] = dist[i][k] + dist[k][j]
                end
            end
        end
    end
    
    return dist
end

-------------------------------------------------------------------------------
-- 最小生成树算法
-------------------------------------------------------------------------------

--- Kruskal 最小生成树算法
-- @return table 边列表 {{from, to, weight}, ...}
-- @return number 总权重
-- @return boolean 是否成功 (图是否连通)
function Graph:kruskal()
    if self.graphType == GraphUtils.GraphType.DIRECTED then
        error("Kruskal algorithm requires undirected graph")
    end
    
    -- 并查集
    local parent = {}
    local rank = {}
    
    local function find(x)
        if parent[x] ~= x then
            parent[x] = find(parent[x])  -- 路径压缩
        end
        return parent[x]
    end
    
    local function union(x, y)
        local px, py = find(x), find(y)
        if px == py then
            return false
        end
        
        -- 按秩合并
        if rank[px] < rank[py] then
            parent[px] = py
        elseif rank[px] > rank[py] then
            parent[py] = px
        else
            parent[py] = px
            rank[px] = rank[px] + 1
        end
        return true
    end
    
    -- 初始化并查集
    for vertex, _ in pairs(self.vertices) do
        parent[vertex] = vertex
        rank[vertex] = 0
    end
    
    -- 按权重排序边
    local edges = self:getEdges()
    table.sort(edges, function(a, b) return a.weight < b.weight end)
    
    local mst = {}
    local totalWeight = 0
    
    for _, edge in ipairs(edges) do
        if find(edge.from) ~= find(edge.to) then
            union(edge.from, edge.to)
            table.insert(mst, {from = edge.from, to = edge.to, weight = edge.weight})
            totalWeight = totalWeight + edge.weight
            
            if #mst == self.vertexCount - 1 then
                break
            end
        end
    end
    
    return mst, totalWeight, #mst == self.vertexCount - 1
end

--- Prim 最小生成树算法
-- @param start 起始顶点 (可选)
-- @return table 边列表 {{from, to, weight}, ...}
-- @return number 总权重
-- @return boolean 是否成功 (图是否连通)
function Graph:prim(start)
    if self.graphType == GraphUtils.GraphType.DIRECTED then
        error("Prim algorithm requires undirected graph")
    end
    
    if self:isEmpty() then
        return {}, 0, true
    end
    
    -- 选择起始顶点
    if not start then
        for vertex, _ in pairs(self.vertices) do
            start = vertex
            break
        end
    end
    
    if not self.vertices[start] then
        return {}, 0, false
    end
    
    local inMST = {}
    local mst = {}
    local totalWeight = 0
    
    inMST[start] = true
    local verticesInMST = 1
    
    while verticesInMST < self.vertexCount do
        local minEdge = nil
        local minWeight = math.huge
        
        -- 找到最小边
        for v, _ in pairs(inMST) do
            for neighbor, weight in pairs(self.adjacency[v]) do
                if not inMST[neighbor] and weight < minWeight then
                    minWeight = weight
                    minEdge = {from = v, to = neighbor, weight = weight}
                end
            end
        end
        
        if minEdge == nil then
            break  -- 图不连通
        end
        
        table.insert(mst, minEdge)
        totalWeight = totalWeight + minEdge.weight
        inMST[minEdge.to] = true
        verticesInMST = verticesInMST + 1
    end
    
    return mst, totalWeight, verticesInMST == self.vertexCount
end

-------------------------------------------------------------------------------
-- 拓扑排序算法
-------------------------------------------------------------------------------

--- DFS 拓扑排序
-- @return table|nil 拓扑排序结果，有环则返回 nil
function Graph:topologicalSort()
    if self.graphType == GraphUtils.GraphType.UNDIRECTED then
        error("Topological sort requires directed graph")
    end
    
    local visited = {}
    local inStack = {}
    local result = {}
    local hasCycle = false
    
    local function dfs(vertex)
        if hasCycle then
            return
        end
        
        visited[vertex] = true
        inStack[vertex] = true
        
        for neighbor, _ in pairs(self.adjacency[vertex]) do
            if inStack[neighbor] then
                hasCycle = true
                return
            elseif not visited[neighbor] then
                dfs(neighbor)
            end
        end
        
        inStack[vertex] = false
        table.insert(result, 1, vertex)
    end
    
    for vertex, _ in pairs(self.vertices) do
        if not visited[vertex] and not hasCycle then
            dfs(vertex)
        end
    end
    
    if hasCycle then
        return nil
    end
    
    return result
end

--- Kahn 拓扑排序 (BFS 版本)
-- @return table|nil 拓扑排序结果，有环则返回 nil
function Graph:kahnSort()
    if self.graphType == GraphUtils.GraphType.UNDIRECTED then
        error("Kahn sort requires directed graph")
    end
    
    local inDegree = {}
    for vertex, _ in pairs(self.vertices) do
        inDegree[vertex] = 0
    end
    
    -- 计算入度
    for from, neighbors in pairs(self.adjacency) do
        for to, _ in pairs(neighbors) do
            inDegree[to] = inDegree[to] + 1
        end
    end
    
    -- 将入度为0的顶点入队
    local queue = {}
    for vertex, degree in pairs(inDegree) do
        if degree == 0 then
            table.insert(queue, vertex)
        end
    end
    
    local result = {}
    
    while #queue > 0 do
        local vertex = table.remove(queue, 1)
        table.insert(result, vertex)
        
        for neighbor, _ in pairs(self.adjacency[vertex]) do
            inDegree[neighbor] = inDegree[neighbor] - 1
            if inDegree[neighbor] == 0 then
                table.insert(queue, neighbor)
            end
        end
    end
    
    if #result ~= self.vertexCount then
        return nil  -- 有环
    end
    
    return result
end

-------------------------------------------------------------------------------
-- 连通性算法
-------------------------------------------------------------------------------

--- 获取连通分量 (无向图)
-- @return table 连通分量列表 {{...}, {...}, ...}
function Graph:connectedComponents()
    local visited = {}
    local components = {}
    
    for vertex, _ in pairs(self.vertices) do
        if not visited[vertex] then
            local component = {}
            local stack = {vertex}
            
            while #stack > 0 do
                local v = table.remove(stack)
                
                if not visited[v] then
                    visited[v] = true
                    table.insert(component, v)
                    
                    for neighbor, _ in pairs(self.adjacency[v]) do
                        if not visited[neighbor] then
                            table.insert(stack, neighbor)
                        end
                    end
                end
            end
            
            table.insert(components, component)
        end
    end
    
    return components
end

--- 检查图是否连通
-- @return boolean
function Graph:isConnected()
    local components = self:connectedComponents()
    return #components == 1
end

--- 获取强连通分量 (有向图) - Kosaraju 算法
-- @return table 强连通分量列表 {{...}, {...}, ...}
function Graph:stronglyConnectedComponents()
    if self.graphType == GraphUtils.GraphType.UNDIRECTED then
        return self:connectedComponents()
    end
    
    -- 第一次 DFS，记录完成顺序
    local visited = {}
    local finishOrder = {}
    
    local function dfs1(vertex)
        visited[vertex] = true
        for neighbor, _ in pairs(self.adjacency[vertex]) do
            if not visited[neighbor] then
                dfs1(neighbor)
            end
        end
        table.insert(finishOrder, 1, vertex)
    end
    
    for vertex, _ in pairs(self.vertices) do
        if not visited[vertex] then
            dfs1(vertex)
        end
    end
    
    -- 构建转置图
    local transpose = Graph.new(GraphUtils.GraphType.DIRECTED, self.weighted)
    for from, neighbors in pairs(self.adjacency) do
        for to, weight in pairs(neighbors) do
            transpose:addEdge(to, from, weight)
        end
    end
    
    -- 第二次 DFS
    visited = {}
    local components = {}
    
    local function dfs2(vertex, component)
        visited[vertex] = true
        table.insert(component, vertex)
        for neighbor, _ in pairs(transpose.adjacency[vertex]) do
            if not visited[neighbor] then
                dfs2(neighbor, component)
            end
        end
    end
    
    for _, vertex in ipairs(finishOrder) do
        if not visited[vertex] then
            local component = {}
            dfs2(vertex, component)
            table.insert(components, component)
        end
    end
    
    return components
end

-------------------------------------------------------------------------------
-- 环检测算法
-------------------------------------------------------------------------------

--- 检测图是否有环
-- @return boolean
function Graph:hasCycle()
    if self.graphType == GraphUtils.GraphType.UNDIRECTED then
        -- 无向图：使用并查集
        local parent = {}
        
        local function find(x)
            if parent[x] ~= x then
                parent[x] = find(parent[x])
            end
            return parent[x]
        end
        
        for vertex, _ in pairs(self.vertices) do
            parent[vertex] = vertex
        end
        
        for from, neighbors in pairs(self.adjacency) do
            for to, _ in pairs(neighbors) do
                if from < to then  -- 避免重复检查
                    local pf, pt = find(from), find(to)
                    if pf == pt then
                        return true
                    end
                    parent[pf] = pt
                end
            end
        end
        
        return false
    else
        -- 有向图：使用 DFS 检测
        local visited = {}
        local inStack = {}
        
        local function dfs(vertex)
            visited[vertex] = true
            inStack[vertex] = true
            
            for neighbor, _ in pairs(self.adjacency[vertex]) do
                if inStack[neighbor] then
                    return true
                elseif not visited[neighbor] then
                    if dfs(neighbor) then
                        return true
                    end
                end
            end
            
            inStack[vertex] = false
            return false
        end
        
        for vertex, _ in pairs(self.vertices) do
            if not visited[vertex] then
                if dfs(vertex) then
                    return true
                end
            end
        end
        
        return false
    end
end

--- 查找图中的所有环
-- @return table 环列表 {{...}, {...}, ...}
function Graph:findCycles()
    if self.graphType == GraphUtils.GraphType.UNDIRECTED then
        -- 无向图找环比较复杂，这里返回所有环
        local cycles = {}
        local visited = {}
        local parent = {}
        local currentPath = {}
        
        local function dfs(vertex, par)
            visited[vertex] = true
            currentPath[vertex] = true
            parent[vertex] = par
            
            for neighbor, _ in pairs(self.adjacency[vertex]) do
                if not visited[neighbor] then
                    dfs(neighbor, vertex)
                elseif neighbor ~= par and currentPath[neighbor] then
                    -- 找到环
                    local cycle = {neighbor}
                    local current = vertex
                    while current ~= neighbor do
                        table.insert(cycle, current)
                        current = parent[current]
                    end
                    table.insert(cycle, neighbor)
                    table.insert(cycles, cycle)
                end
            end
            
            currentPath[vertex] = false
        end
        
        for vertex, _ in pairs(self.vertices) do
            if not visited[vertex] then
                dfs(vertex, nil)
            end
        end
        
        return cycles
    else
        -- 有向图
        local cycles = {}
        local visited = {}
        local inStack = {}
        local path = {}
        
        local function dfs(vertex)
            visited[vertex] = true
            inStack[vertex] = true
            table.insert(path, vertex)
            
            for neighbor, _ in pairs(self.adjacency[vertex]) do
                if inStack[neighbor] then
                    -- 找到环
                    local cycle = {}
                    local startIdx = 1
                    for i, v in ipairs(path) do
                        if v == neighbor then
                            startIdx = i
                            break
                        end
                    end
                    for i = startIdx, #path do
                        table.insert(cycle, path[i])
                    end
                    table.insert(cycle, neighbor)
                    table.insert(cycles, cycle)
                elseif not visited[neighbor] then
                    dfs(neighbor)
                end
            end
            
            table.remove(path)
            inStack[vertex] = false
        end
        
        for vertex, _ in pairs(self.vertices) do
            if not visited[vertex] then
                dfs(vertex)
            end
        end
        
        return cycles
    end
end

--- 检查是否为 DAG (有向无环图)
-- @return boolean
function Graph:isDAG()
    if self.graphType == GraphUtils.GraphType.UNDIRECTED then
        return false
    end
    return not self:hasCycle()
end

-------------------------------------------------------------------------------
-- 其他图算法
-------------------------------------------------------------------------------

--- 检查是否为二分图
-- @return boolean
-- @return table|nil 两个分区的顶点列表 {left = {...}, right = {...}}
function Graph:isBipartite()
    local color = {}
    local left = {}
    local right = {}
    
    for vertex, _ in pairs(self.vertices) do
        if color[vertex] == nil then
            local queue = {vertex}
            color[vertex] = 0
            table.insert(left, vertex)
            
            while #queue > 0 do
                local v = table.remove(queue, 1)
                
                for neighbor, _ in pairs(self.adjacency[v]) do
                    if color[neighbor] == nil then
                        color[neighbor] = 1 - color[v]
                        if color[neighbor] == 0 then
                            table.insert(left, neighbor)
                        else
                            table.insert(right, neighbor)
                        end
                        table.insert(queue, neighbor)
                    elseif color[neighbor] == color[v] then
                        return false, nil
                    end
                end
            end
        end
    end
    
    return true, {left = left, right = right}
end

--- 获取欧拉路径 (如果存在)
-- @return table|nil 欧拉路径顶点列表
function Graph:getEulerianPath()
    local start = nil
    
    if self.graphType == GraphUtils.GraphType.DIRECTED then
        -- 有向图欧拉路径
        local inDegree = {}
        local outDegree = {}
        
        for vertex, _ in pairs(self.vertices) do
            inDegree[vertex] = self:getInDegree(vertex)
            outDegree[vertex] = self:getDegree(vertex)
        end
        
        local startCandidates = 0
        local endCandidates = 0
        
        for vertex, _ in pairs(self.vertices) do
            local diff = outDegree[vertex] - inDegree[vertex]
            if diff == 1 then
                start = vertex
                startCandidates = startCandidates + 1
            elseif diff == -1 then
                endCandidates = endCandidates + 1
            elseif diff ~= 0 then
                return nil
            end
        end
        
        if startCandidates > 1 or endCandidates > 1 then
            return nil
        end
        
        if start == nil then
            for vertex, _ in pairs(self.vertices) do
                start = vertex
                break
            end
        end
    else
        -- 无向图欧拉路径
        local oddDegreeCount = 0
        
        for vertex, _ in pairs(self.vertices) do
            local deg = self:getDegree(vertex)
            if deg % 2 == 1 then
                oddDegreeCount = oddDegreeCount + 1
                start = vertex
            end
        end
        
        if oddDegreeCount ~= 0 and oddDegreeCount ~= 2 then
            return nil
        end
        
        if start == nil then
            for vertex, _ in pairs(self.vertices) do
                start = vertex
                break
            end
        end
    end
    
    if start == nil then
        return nil
    end
    
    -- Hierholzer 算法
    local tempGraph = self:clone()
    local stack = {start}
    local path = {}
    
    while #stack > 0 do
        local v = stack[#stack]
        
        -- 找到一条边
        local found = false
        for neighbor, _ in pairs(tempGraph.adjacency[v]) do
            table.insert(stack, neighbor)
            tempGraph:removeEdge(v, neighbor)
            found = true
            break
        end
        
        if not found then
            table.insert(path, table.remove(stack))
        end
    end
    
    return path
end

--- 获取直径 (最长最短路径)
-- @return number 直径长度
-- @return table|nil 直径路径 {from, to}
function Graph:getDiameter()
    local maxDist = 0
    local diameterPath = nil
    
    for v1, _ in pairs(self.vertices) do
        local distances, predecessors = self:dijkstra(v1)
        for v2, dist in pairs(distances) do
            if dist < math.huge and dist > maxDist then
                maxDist = dist
                diameterPath = {from = v1, to = v2, distance = dist}
            end
        end
    end
    
    return maxDist, diameterPath
end

-------------------------------------------------------------------------------
-- 模块函数
-------------------------------------------------------------------------------

--- 创建无向图
-- @param weighted 是否带权 (默认 false)
-- @return Graph
function GraphUtils.undirected(weighted)
    return Graph.new(GraphUtils.GraphType.UNDIRECTED, weighted)
end

--- 创建有向图
-- @param weighted 是否带权 (默认 false)
-- @return Graph
function GraphUtils.directed(weighted)
    return Graph.new(GraphUtils.GraphType.DIRECTED, weighted)
end

--- 从边列表创建图
-- @param edges 边列表 {{from, to, weight?}, ...}
-- @param graphType 图类型
-- @param weighted 是否带权
-- @return Graph
function GraphUtils.fromEdgeList(edges, graphType, weighted)
    local g = Graph.new(graphType or GraphUtils.GraphType.UNDIRECTED, weighted)
    for _, edge in ipairs(edges) do
        g:addEdge(edge[1], edge[2], edge[3] or 1)
    end
    return g
end

--- 从邻接矩阵创建图
-- @param matrix 邻接矩阵 {row = {col = weight, ...}, ...}
-- @param vertexNames 顶点名称列表 (可选)
-- @param graphType 图类型
-- @return Graph
function GraphUtils.fromAdjacencyMatrix(matrix, vertexNames, graphType)
    local n = #matrix
    local g = Graph.new(graphType or GraphUtils.GraphType.DIRECTED, true)
    
    for i = 1, n do
        for j = 1, n do
            if matrix[i][j] ~= 0 and matrix[i][j] ~= math.huge then
                local v1 = vertexNames and vertexNames[i] or i
                local v2 = vertexNames and vertexNames[j] or j
                g:addEdge(v1, v2, matrix[i][j])
            end
        end
    end
    
    return g
end

return GraphUtils
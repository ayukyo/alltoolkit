package topological_sort_utils

/**
 * 拓扑排序工具类
 *
 * 提供基于 Kahn 算法和 DFS 算法的拓扑排序实现
 * 零依赖，仅使用 Kotlin 标准库
 *
 * 应用场景：
 * - 任务调度和依赖解析
 * - 编译顺序确定
 * - 课程安排
 * - 包管理器依赖解析
 *
 * @author AllToolkit
 * @since 1.0.0
 */

// =============================================================================
// Exceptions
// =============================================================================

/**
 * 拓扑排序异常基类
 */
sealed class TopologicalSortException(message: String) : Exception(message)

/**
 * 循环依赖异常 - 当图中存在环时抛出
 */
class CycleDetectedException(
    message: String = "Graph contains a cycle, topological sort is not possible",
    val cycle: List<Any>? = null
) : TopologicalSortException(message)

/**
 * 节点不存在异常
 */
class NodeNotFoundException(node: Any) : TopologicalSortException("Node not found: $node")

// =============================================================================
// Graph Builder
// =============================================================================

/**
 * 有向图构建器
 *
 * 支持链式调用的图构建器
 */
class DirectedGraphBuilder<T> {
    private val nodes = mutableSetOf<T>()
    private val edges = mutableMapOf<T, MutableSet<T>>()

    /**
     * 添加节点
     */
    fun addNode(node: T): DirectedGraphBuilder<T> {
        nodes.add(node)
        return this
    }

    /**
     * 添加多个节点
     */
    fun addNodes(vararg nodes: T): DirectedGraphBuilder<T> {
        this.nodes.addAll(nodes)
        return this
    }

    /**
     * 添加边（from -> to，表示 from 依赖于 to）
     */
    fun addEdge(from: T, to: T): DirectedGraphBuilder<T> {
        nodes.add(from)
        nodes.add(to)
        edges.getOrPut(from) { mutableSetOf() }.add(to)
        return this
    }

    /**
     * 添加多条边
     */
    fun addEdges(vararg pairs: Pair<T, T>): DirectedGraphBuilder<T> {
        pairs.forEach { (from, to) -> addEdge(from, to) }
        return this
    }

    /**
     * 构建图
     */
    fun build(): DirectedGraph<T> = DirectedGraph(nodes.toSet(), edges.mapValues { it.value.toSet() })
}

/**
 * 有向图数据结构
 */
data class DirectedGraph<T>(
    val nodes: Set<T>,
    val edges: Map<T, Set<T>>
) {
    /**
     * 获取节点的所有后继（出边指向的节点）
     */
    fun successors(node: T): Set<T> = edges[node] ?: emptySet()

    /**
     * 获取节点的所有前驱（入边来源的节点）
     */
    fun predecessors(node: T): Set<T> {
        return nodes.filter { edges[it]?.contains(node) == true }.toSet()
    }

    /**
     * 获取入度
     */
    fun inDegree(node: T): Int = predecessors(node).size

    /**
     * 获取出度
     */
    fun outDegree(node: T): Int = successors(node).size

    /**
     * 获取所有入度为 0 的节点（源节点）
     */
    fun sources(): Set<T> = nodes.filter { inDegree(it) == 0 }.toSet()

    /**
     * 获取所有出度为 0 的节点（汇节点）
     */
    fun sinks(): Set<T> = nodes.filter { outDegree(it) == 0 }.toSet()

    /**
     * 检查节点是否存在
     */
    fun contains(node: T): Boolean = nodes.contains(node)

    /**
     * 图的大小（节点数）
     */
    val size: Int get() = nodes.size

    /**
     * 边的数量
     */
    val edgeCount: Int get() = edges.values.sumOf { it.size }

    companion object {
        /**
         * 创建图构建器
         */
        fun <T> builder(): DirectedGraphBuilder<T> = DirectedGraphBuilder()

        /**
         * 从边列表创建图
         */
        fun <T> fromEdges(vararg pairs: Pair<T, T>): DirectedGraph<T> {
            val builder = builder<T>()
            pairs.forEach { (from, to) -> builder.addEdge(from, to) }
            return builder.build()
        }

        /**
         * 从邻接表创建图
         */
        fun <T> fromAdjacencyList(adjacencyList: Map<T, Collection<T>>): DirectedGraph<T> {
            val builder = builder<T>()
            adjacencyList.forEach { (from, toList) ->
                builder.addNode(from)
                toList.forEach { to -> builder.addEdge(from, to) }
            }
            return builder.build()
        }
    }
}

// =============================================================================
// Topological Sort Algorithms
// =============================================================================

/**
 * 拓扑排序工具类
 */
object TopologicalSortUtils {

    // =========================================================================
    // Kahn 算法 (BFS)
    // =========================================================================

    /**
     * 使用 Kahn 算法进行拓扑排序
     *
     * 时间复杂度: O(V + E)
     * 空间复杂度: O(V + E)
     *
     * @param graph 有向图
     * @return 拓扑排序结果
     * @throws CycleDetectedException 如果图中存在环
     */
    @JvmStatic
    fun <T> kahnSort(graph: DirectedGraph<T>): List<T> {
        val result = mutableListOf<T>()
        val inDegreeMap = mutableMapOf<T, Int>()

        // 初始化入度
        graph.nodes.forEach { node ->
            inDegreeMap[node] = graph.inDegree(node)
        }

        // 找到所有入度为 0 的节点
        val queue = ArrayDeque<T>()
        graph.nodes.forEach { node ->
            if (inDegreeMap[node] == 0) {
                queue.add(node)
            }
        }

        // Kahn 算法主循环
        while (queue.isNotEmpty()) {
            val node = queue.removeFirst()
            result.add(node)

            // 减少所有后继的入度
            graph.successors(node).forEach { successor ->
                inDegreeMap[successor] = inDegreeMap[successor]!! - 1
                if (inDegreeMap[successor] == 0) {
                    queue.add(successor)
                }
            }
        }

        // 检查是否所有节点都已排序
        if (result.size != graph.nodes.size) {
            val cycleNodes = graph.nodes.filter { it !in result }
            throw CycleDetectedException(
                "Graph contains a cycle, topological sort is not possible",
                cycleNodes
            )
        }

        return result
    }

    /**
     * 使用 Kahn 算法进行拓扑排序（接受邻接表）
     *
     * @param adjacencyList 邻接表，key 为节点，value 为该节点依赖的节点列表
     * @return 拓扑排序结果
     * @throws CycleDetectedException 如果图中存在环
     */
    @JvmStatic
    fun <T> kahnSort(adjacencyList: Map<T, Collection<T>>): List<T> {
        return kahnSort(DirectedGraph.fromAdjacencyList(adjacencyList))
    }

    // =========================================================================
    // DFS 算法
    // =========================================================================

    /**
     * 使用 DFS 算法进行拓扑排序
     *
     * 时间复杂度: O(V + E)
     * 空间复杂度: O(V)
     *
     * @param graph 有向图
     * @return 拓扑排序结果
     * @throws CycleDetectedException 如果图中存在环
     */
    @JvmStatic
    fun <T> dfsSort(graph: DirectedGraph<T>): List<T> {
        val result = mutableListOf<T>()
        val visited = mutableSetOf<T>()
        val visiting = mutableSetOf<T>() // 用于检测环

        fun dfs(node: T) {
            if (node in visited) return

            if (node in visiting) {
                // 发现环
                throw CycleDetectedException("Graph contains a cycle detected at node: $node")
            }

            visiting.add(node)

            // 先访问所有后继
            graph.successors(node).forEach { successor ->
                dfs(successor)
            }

            visiting.remove(node)
            visited.add(node)
            result.add(node) // 后序添加
        }

        // 从所有节点开始 DFS
        graph.nodes.forEach { node ->
            if (node !in visited) {
                dfs(node)
            }
        }

        return result
    }

    /**
     * 使用 DFS 算法进行拓扑排序（接受邻接表）
     *
     * @param adjacencyList 邻接表
     * @return 拓扑排序结果
     * @throws CycleDetectedException 如果图中存在环
     */
    @JvmStatic
    fun <T> dfsSort(adjacencyList: Map<T, Collection<T>>): List<T> {
        return dfsSort(DirectedGraph.fromAdjacencyList(adjacencyList))
    }

    // =========================================================================
    // 安全版本（返回 Result）
    // =========================================================================

    /**
     * 安全的拓扑排序，返回 Result 类型
     *
     * @param graph 有向图
     * @return 成功返回排序结果，失败返回循环依赖信息
     */
    @JvmStatic
    fun <T> sortSafely(graph: DirectedGraph<T>): Result<List<T>> {
        return try {
            Result.success(kahnSort(graph))
        } catch (e: CycleDetectedException) {
            Result.failure(e)
        }
    }

    /**
     * 安全的拓扑排序（接受邻接表）
     *
     * @param adjacencyList 邻接表
     * @return 成功返回排序结果，失败返回循环依赖信息
     */
    @JvmStatic
    fun <T> sortSafely(adjacencyList: Map<T, Collection<T>>): Result<List<T>> {
        return try {
            Result.success(kahnSort(adjacencyList))
        } catch (e: CycleDetectedException) {
            Result.failure(e)
        }
    }

    // =========================================================================
    // 检测环
    // =========================================================================

    /**
     * 检测图中是否有环
     *
     * @param graph 有向图
     * @return 如果存在环则返回 true
     */
    @JvmStatic
    fun <T> hasCycle(graph: DirectedGraph<T>): Boolean {
        return try {
            kahnSort(graph)
            false
        } catch (e: CycleDetectedException) {
            true
        }
    }

    /**
     * 检测图中是否有环（接受邻接表）
     *
     * @param adjacencyList 邻接表
     * @return 如果存在环则返回 true
     */
    @JvmStatic
    fun <T> hasCycle(adjacencyList: Map<T, Collection<T>>): Boolean {
        return hasCycle(DirectedGraph.fromAdjacencyList(adjacencyList))
    }

    /**
     * 查找图中的环
     *
     * @param graph 有向图
     * @return 环的列表（如果存在），否则返回 null
     */
    @JvmStatic
    fun <T> findCycle(graph: DirectedGraph<T>): List<T>? {
        val visited = mutableSetOf<T>()
        val path = mutableListOf<T>()
        val pathSet = mutableSetOf<T>()

        fun dfs(node: T): List<T>? {
            if (node in visited) return null

            if (node in pathSet) {
                // 找到环，返回环的部分
                val cycleStart = path.indexOf(node)
                return path.subList(cycleStart, path.size) + node
            }

            path.add(node)
            pathSet.add(node)

            for (successor in graph.successors(node)) {
                val cycle = dfs(successor)
                if (cycle != null) return cycle
            }

            path.removeLast()
            pathSet.remove(node)
            visited.add(node)

            return null
        }

        for (node in graph.nodes) {
            if (node !in visited) {
                val cycle = dfs(node)
                if (cycle != null) return cycle
            }
        }

        return null
    }

    // =========================================================================
    // 分层拓扑排序
    // =========================================================================

    /**
     * 分层拓扑排序
     *
     * 将节点按层级分组，同一层级的节点之间没有依赖关系，可以并行处理
     *
     * @param graph 有向图
     * @return 分层的拓扑排序结果
     * @throws CycleDetectedException 如果图中存在环
     */
    @JvmStatic
    fun <T> layeredSort(graph: DirectedGraph<T>): List<Set<T>> {
        val result = mutableListOf<Set<T>>()
        val inDegreeMap = mutableMapOf<T, Int>()
        val remainingNodes = graph.nodes.toMutableSet()

        // 初始化入度
        graph.nodes.forEach { node ->
            inDegreeMap[node] = graph.inDegree(node)
        }

        while (remainingNodes.isNotEmpty()) {
            // 找到当前层所有入度为 0 的节点
            val currentLayer = remainingNodes.filter { inDegreeMap[it] == 0 }.toSet()

            if (currentLayer.isEmpty()) {
                throw CycleDetectedException("Graph contains a cycle")
            }

            result.add(currentLayer)

            // 移除当前层节点，更新入度
            currentLayer.forEach { node ->
                remainingNodes.remove(node)
                graph.successors(node).forEach { successor ->
                    if (successor in remainingNodes) {
                        inDegreeMap[successor] = inDegreeMap[successor]!! - 1
                    }
                }
            }
        }

        return result
    }

    /**
     * 分层拓扑排序（接受邻接表）
     *
     * @param adjacencyList 邻接表
     * @return 分层的拓扑排序结果
     * @throws CycleDetectedException 如果图中存在环
     */
    @JvmStatic
    fun <T> layeredSort(adjacencyList: Map<T, Collection<T>>): List<Set<T>> {
        return layeredSort(DirectedGraph.fromAdjacencyList(adjacencyList))
    }

    // =========================================================================
    // 最长路径
    // =========================================================================

    /**
     * 计算从任意源节点到每个节点的最长路径
     *
     * @param graph 有向图
     * @return 每个节点的最长路径长度
     * @throws CycleDetectedException 如果图中存在环
     */
    @JvmStatic
    fun <T> longestPath(graph: DirectedGraph<T>): Map<T, Int> {
        val topoOrder = kahnSort(graph)
        val distances = mutableMapOf<T, Int>()

        // 初始化：源节点距离为 0
        graph.sources().forEach { distances[it] = 0 }
        graph.nodes.forEach { if (it !in distances) distances[it] = Int.MIN_VALUE }

        // 按拓扑顺序更新距离
        for (node in topoOrder) {
            if (distances[node] != Int.MIN_VALUE) {
                for (successor in graph.successors(node)) {
                    if (distances[successor]!! < distances[node]!! + 1) {
                        distances[successor] = distances[node]!! + 1
                    }
                }
            }
        }

        return distances.mapValues { if (it.value == Int.MIN_VALUE) -1 else it.value }
    }

    // =========================================================================
    // 所有拓扑排序
    // =========================================================================

    /**
     * 获取所有可能的拓扑排序
     *
     * 注意：对于大型图，结果可能非常大
     *
     * @param graph 有向图
     * @param maxResults 最大结果数量限制
     * @return 所有可能的拓扑排序列表
     */
    @JvmStatic
    fun <T> allTopologicalSorts(graph: DirectedGraph<T>, maxResults: Int = Int.MAX_VALUE): List<List<T>> {
        val results = mutableListOf<List<T>>()
        val inDegreeMap = mutableMapOf<T, Int>()

        // 初始化入度
        graph.nodes.forEach { node ->
            inDegreeMap[node] = graph.inDegree(node)
        }

        fun backtrack(current: MutableList<T>, inDegrees: MutableMap<T, Int>) {
            if (current.size == graph.nodes.size) {
                results.add(current.toList())
                return
            }

            if (results.size >= maxResults) return

            // 找到所有可选的节点（入度为 0 且未访问）
            val candidates = graph.nodes.filter { 
                it !in current && inDegrees[it] == 0 
            }

            for (node in candidates) {
                current.add(node)
                
                // 更新入度
                val newInDegrees = inDegrees.toMutableMap()
                for (successor in graph.successors(node)) {
                    newInDegrees[successor] = newInDegrees[successor]!! - 1
                }
                
                backtrack(current, newInDegrees)
                current.removeLast()
            }
        }

        backtrack(mutableListOf(), inDegreeMap.toMutableMap())
        return results
    }

    // =========================================================================
    // 依赖解析
    // =========================================================================

    /**
     * 解析依赖并返回执行顺序
     *
     * @param dependencies 依赖映射，key 为项目，value 为其依赖的项目列表
     * @return 执行顺序
     * @throws CycleDetectedException 如果存在循环依赖
     */
    @JvmStatic
    fun <T> resolveDependencies(dependencies: Map<T, Collection<T>>): List<T> {
        return kahnSort(dependencies)
    }

    /**
     * 获取节点的层级（从源节点的距离）
     *
     * @param graph 有向图
     * @return 每个节点的层级
     */
    @JvmStatic
    fun <T> getNodeLevels(graph: DirectedGraph<T>): Map<T, Int> {
        val layers = layeredSort(graph)
        val levels = mutableMapOf<T, Int>()

        layers.forEachIndexed { level, nodes ->
            nodes.forEach { node ->
                levels[node] = level
            }
        }

        return levels
    }

    /**
     * 获取可以并行执行的节点组
     *
     * @param graph 有向图
     * @return 可并行执行的节点组列表
     */
    @JvmStatic
    fun <T> getParallelGroups(graph: DirectedGraph<T>): List<Set<T>> {
        return layeredSort(graph)
    }
}

// =============================================================================
// Extension Functions
// =============================================================================

/**
 * 图的扩展函数：拓扑排序
 */
fun <T> DirectedGraph<T>.topologicalSort(): List<T> = TopologicalSortUtils.kahnSort(this)

/**
 * 图的扩展函数：分层拓扑排序
 */
fun <T> DirectedGraph<T>.layeredTopologicalSort(): List<Set<T>> = TopologicalSortUtils.layeredSort(this)

/**
 * 图的扩展函数：检测环
 */
fun <T> DirectedGraph<T>.hasCycle(): Boolean = TopologicalSortUtils.hasCycle(this)

/**
 * 图的扩展函数：查找环
 */
fun <T> DirectedGraph<T>.findCycle(): List<T>? = TopologicalSortUtils.findCycle(this)

/**
 * 邻接表的扩展函数：拓扑排序
 */
fun <T> Map<T, Collection<T>>.topologicalSort(): List<T> = TopologicalSortUtils.kahnSort(this)

/**
 * 邻接表的扩展函数：分层拓扑排序
 */
fun <T> Map<T, Collection<T>>.layeredTopologicalSort(): List<Set<T>> = TopologicalSortUtils.layeredSort(this)

/**
 * 邻接表的扩展函数：检测环
 */
fun <T> Map<T, Collection<T>>.hasCycle(): Boolean = TopologicalSortUtils.hasCycle(this)
package topological_sort_utils

import org.junit.Assert.*
import org.junit.Test

/**
 * 拓扑排序工具类测试
 */
class TopologicalSortUtilsTest {

    // =========================================================================
    // Kahn 算法测试
    // =========================================================================

    @Test
    fun testKahnSortSimple() {
        // A -> B -> C
        //      \
        //       -> D
        val graph = DirectedGraph.builder<String>()
            .addEdge("B", "A")  // B 依赖 A
            .addEdge("C", "B")  // C 依赖 B
            .addEdge("D", "B")  // D 依赖 B
            .build()

        val result = TopologicalSortUtils.kahnSort(graph)
        
        // A 必须在 B 之前
        assertTrue(result.indexOf("A") < result.indexOf("B"))
        // B 必须在 C 和 D 之前
        assertTrue(result.indexOf("B") < result.indexOf("C"))
        assertTrue(result.indexOf("B") < result.indexOf("D"))
        assertEquals(4, result.size)
    }

    @Test
    fun testKahnSortWithMap() {
        val adjacencyList = mapOf(
            "B" to listOf("A"),
            "C" to listOf("B"),
            "D" to listOf("B"),
            "A" to emptyList<String>()
        )

        val result = TopologicalSortUtils.kahnSort(adjacencyList)
        
        assertTrue(result.indexOf("A") < result.indexOf("B"))
        assertTrue(result.indexOf("B") < result.indexOf("C"))
        assertTrue(result.indexOf("B") < result.indexOf("D"))
    }

    @Test
    fun testKahnSortEmptyGraph() {
        val graph = DirectedGraph.builder<String>().build()
        val result = TopologicalSortUtils.kahnSort(graph)
        assertTrue(result.isEmpty())
    }

    @Test
    fun testKahnSortSingleNode() {
        val graph = DirectedGraph.builder<String>()
            .addNode("A")
            .build()
        
        val result = TopologicalSortUtils.kahnSort(graph)
        assertEquals(listOf("A"), result)
    }

    @Test
    fun testKahnSortDisconnected() {
        // 两个独立的图: A -> B, C -> D
        val graph = DirectedGraph.builder<String>()
            .addEdge("B", "A")
            .addEdge("D", "C")
            .build()

        val result = TopologicalSortUtils.kahnSort(graph)
        assertEquals(4, result.size)
        assertTrue(result.indexOf("A") < result.indexOf("B"))
        assertTrue(result.indexOf("C") < result.indexOf("D"))
    }

    @Test(expected = CycleDetectedException::class)
    fun testKahnSortWithCycle() {
        // A -> B -> C -> A (cycle)
        val graph = DirectedGraph.builder<String>()
            .addEdge("B", "A")
            .addEdge("C", "B")
            .addEdge("A", "C")
            .build()

        TopologicalSortUtils.kahnSort(graph)
    }

    // =========================================================================
    // DFS 算法测试
    // =========================================================================

    @Test
    fun testDfsSortSimple() {
        val graph = DirectedGraph.builder<String>()
            .addEdge("B", "A")
            .addEdge("C", "B")
            .build()

        val result = TopologicalSortUtils.dfsSort(graph)
        
        assertTrue(result.indexOf("A") < result.indexOf("B"))
        assertTrue(result.indexOf("B") < result.indexOf("C"))
    }

    @Test
    fun testDfsSortEqualsKahnSort() {
        val graph = DirectedGraph.builder<Int>()
            .addEdge(2, 1)
            .addEdge(3, 2)
            .addEdge(4, 2)
            .addEdge(5, 3)
            .addNode(6)  // 独立节点
            .build()

        val kahnResult = TopologicalSortUtils.kahnSort(graph)
        val dfsResult = TopologicalSortUtils.dfsSort(graph)

        assertEquals(kahnResult.size, dfsResult.size)
        assertEquals(kahnResult.toSet(), dfsResult.toSet())
    }

    @Test(expected = CycleDetectedException::class)
    fun testDfsSortWithCycle() {
        val graph = DirectedGraph.builder<String>()
            .addEdge("A", "B")
            .addEdge("B", "C")
            .addEdge("C", "A")
            .build()

        TopologicalSortUtils.dfsSort(graph)
    }

    // =========================================================================
    // 安全版本测试
    // =========================================================================

    @Test
    fun testSortSafelySuccess() {
        val graph = DirectedGraph.builder<String>()
            .addEdge("B", "A")
            .build()

        val result = TopologicalSortUtils.sortSafely(graph)
        assertTrue(result.isSuccess)
        assertEquals(2, result.getOrNull()?.size)
    }

    @Test
    fun testSortSafelyWithCycle() {
        val graph = DirectedGraph.builder<String>()
            .addEdge("A", "B")
            .addEdge("B", "A")
            .build()

        val result = TopologicalSortUtils.sortSafely(graph)
        assertTrue(result.isFailure)
        assertTrue(result.exceptionOrNull() is CycleDetectedException)
    }

    // =========================================================================
    // 循环检测测试
    // =========================================================================

    @Test
    fun testHasCycleFalse() {
        val graph = DirectedGraph.builder<String>()
            .addEdge("B", "A")
            .addEdge("C", "B")
            .build()

        assertFalse(TopologicalSortUtils.hasCycle(graph))
    }

    @Test
    fun testHasCycleTrue() {
        val graph = DirectedGraph.builder<String>()
            .addEdge("A", "B")
            .addEdge("B", "C")
            .addEdge("C", "A")
            .build()

        assertTrue(TopologicalSortUtils.hasCycle(graph))
    }

    @Test
    fun testFindCycle() {
        val graph = DirectedGraph.builder<String>()
            .addEdge("A", "B")
            .addEdge("B", "C")
            .addEdge("C", "A")
            .build()

        val cycle = TopologicalSortUtils.findCycle(graph)
        assertNotNull(cycle)
        assertTrue(cycle!!.isNotEmpty())
    }

    @Test
    fun testFindCycleNone() {
        val graph = DirectedGraph.builder<String>()
            .addEdge("B", "A")
            .addEdge("C", "B")
            .build()

        val cycle = TopologicalSortUtils.findCycle(graph)
        assertNull(cycle)
    }

    // =========================================================================
    // 分层拓扑排序测试
    // =========================================================================

    @Test
    fun testLayeredSortSimple() {
        // A -> B -> D
        // A -> C -> D
        val graph = DirectedGraph.builder<String>()
            .addEdge("B", "A")  // B 依赖 A
            .addEdge("C", "A")  // C 依赖 A
            .addEdge("D", "B")  // D 依赖 B
            .addEdge("D", "C")  // D 依赖 C
            .build()

        val layers = TopologicalSortUtils.layeredSort(graph)
        
        assertEquals(3, layers.size)
        // 第一层: A
        assertTrue(layers[0].contains("A"))
        // 第二层: B, C (可以并行)
        assertTrue(layers[1].contains("B"))
        assertTrue(layers[1].contains("C"))
        // 第三层: D
        assertTrue(layers[2].contains("D"))
    }

    @Test
    fun testLayeredSortIndependent() {
        // 两个独立节点
        val graph = DirectedGraph.builder<String>()
            .addNode("A")
            .addNode("B")
            .build()

        val layers = TopologicalSortUtils.layeredSort(graph)
        
        assertEquals(1, layers.size)
        assertEquals(setOf("A", "B"), layers[0])
    }

    @Test(expected = CycleDetectedException::class)
    fun testLayeredSortWithCycle() {
        val graph = DirectedGraph.builder<String>()
            .addEdge("A", "B")
            .addEdge("B", "A")
            .build()

        TopologicalSortUtils.layeredSort(graph)
    }

    // =========================================================================
    // 最长路径测试
    // =========================================================================

    @Test
    fun testLongestPath() {
        // A -> B -> D
        // A -> C -> D
        val graph = DirectedGraph.builder<String>()
            .addEdge("B", "A")
            .addEdge("C", "A")
            .addEdge("D", "B")
            .addEdge("D", "C")
            .build()

        val distances = TopologicalSortUtils.longestPath(graph)
        
        assertEquals(0, distances["A"])
        assertEquals(1, distances["B"])
        assertEquals(1, distances["C"])
        assertEquals(2, distances["D"])
    }

    // =========================================================================
    // 所有拓扑排序测试
    // =========================================================================

    @Test
    fun testAllTopologicalSortsSimple() {
        // A -> C
        // B -> C
        val graph = DirectedGraph.builder<String>()
            .addEdge("C", "A")
            .addEdge("C", "B")
            .build()

        val allSorts = TopologicalSortUtils.allTopologicalSorts(graph)
        
        // 可能的排序: [A, B, C], [B, A, C]
        assertEquals(2, allSorts.size)
        
        for (sort in allSorts) {
            assertTrue(sort.indexOf("A") < sort.indexOf("C"))
            assertTrue(sort.indexOf("B") < sort.indexOf("C"))
        }
    }

    @Test
    fun testAllTopologicalSortsWithMaxResults() {
        val graph = DirectedGraph.builder<Int>()
            .addEdge(4, 1)
            .addEdge(4, 2)
            .addEdge(4, 3)
            .build()

        val allSorts = TopologicalSortUtils.allTopologicalSorts(graph, maxResults = 2)
        assertTrue(allSorts.size <= 2)
    }

    // =========================================================================
    // 依赖解析测试
    // =========================================================================

    @Test
    fun testResolveDependencies() {
        // 项目依赖: project1 依赖 common, project2 依赖 common 和 project1
        val dependencies = mapOf(
            "common" to emptyList<String>(),
            "project1" to listOf("common"),
            "project2" to listOf("common", "project1")
        )

        val order = TopologicalSortUtils.resolveDependencies(dependencies)
        
        assertTrue(order.indexOf("common") < order.indexOf("project1"))
        assertTrue(order.indexOf("common") < order.indexOf("project2"))
        assertTrue(order.indexOf("project1") < order.indexOf("project2"))
    }

    @Test
    fun testGetNodeLevels() {
        val graph = DirectedGraph.builder<String>()
            .addEdge("B", "A")
            .addEdge("C", "A")
            .addEdge("D", "B")
            .addEdge("D", "C")
            .build()

        val levels = TopologicalSortUtils.getNodeLevels(graph)
        
        assertEquals(0, levels["A"])
        assertEquals(1, levels["B"])
        assertEquals(1, levels["C"])
        assertEquals(2, levels["D"])
    }

    @Test
    fun testGetParallelGroups() {
        val graph = DirectedGraph.builder<String>()
            .addEdge("B", "A")
            .addEdge("C", "A")
            .build()

        val groups = TopologicalSortUtils.getParallelGroups(graph)
        
        assertEquals(2, groups.size)
        assertEquals(setOf("A"), groups[0])
        assertEquals(setOf("B", "C"), groups[1])
    }

    // =========================================================================
    // 图数据结构测试
    // =========================================================================

    @Test
    fun testGraphFromEdges() {
        val graph = DirectedGraph.fromEdges(
            "B" to "A",
            "C" to "B"
        )

        assertEquals(3, graph.size)
        assertEquals(2, graph.edgeCount)
    }

    @Test
    fun testGraphFromAdjacencyList() {
        val adjacencyList = mapOf(
            "A" to emptyList<String>(),
            "B" to listOf("A"),
            "C" to listOf("A", "B")
        )

        val graph = DirectedGraph.fromAdjacencyList(adjacencyList)
        
        assertEquals(3, graph.size)
        assertEquals(3, graph.edgeCount)
    }

    @Test
    fun testGraphSuccessors() {
        val graph = DirectedGraph.builder<String>()
            .addEdge("A", "B")
            .addEdge("A", "C")
            .build()

        val successors = graph.successors("A")
        assertEquals(setOf("B", "C"), successors)
    }

    @Test
    fun testGraphPredecessors() {
        val graph = DirectedGraph.builder<String>()
            .addEdge("B", "A")
            .addEdge("C", "A")
            .build()

        val predecessors = graph.predecessors("A")
        assertEquals(setOf("B", "C"), predecessors)
    }

    @Test
    fun testGraphSources() {
        val graph = DirectedGraph.builder<String>()
            .addEdge("B", "A")
            .addEdge("C", "B")
            .build()

        assertEquals(setOf("A"), graph.sources())
    }

    @Test
    fun testGraphSinks() {
        val graph = DirectedGraph.builder<String>()
            .addEdge("B", "A")
            .addEdge("C", "B")
            .build()

        assertEquals(setOf("C"), graph.sinks())
    }

    // =========================================================================
    // 扩展函数测试
    // =========================================================================

    @Test
    fun testExtensionTopologicalSort() {
        val graph = DirectedGraph.builder<Int>()
            .addEdge(2, 1)
            .addEdge(3, 2)
            .build()

        val result = graph.topologicalSort()
        assertEquals(listOf(1, 2, 3), result)
    }

    @Test
    fun testExtensionLayeredTopologicalSort() {
        val graph = DirectedGraph.builder<String>()
            .addEdge("B", "A")
            .addEdge("C", "A")
            .build()

        val layers = graph.layeredTopologicalSort()
        assertEquals(2, layers.size)
    }

    @Test
    fun testExtensionHasCycle() {
        val acyclic = DirectedGraph.builder<String>()
            .addEdge("B", "A")
            .build()
        assertFalse(acyclic.hasCycle())

        val cyclic = DirectedGraph.builder<String>()
            .addEdge("A", "B")
            .addEdge("B", "A")
            .build()
        assertTrue(cyclic.hasCycle())
    }

    @Test
    fun testMapExtensionTopologicalSort() {
        val adjacencyList = mapOf(
            "A" to emptyList<String>(),
            "B" to listOf("A"),
            "C" to listOf("B")
        )

        val result = adjacencyList.topologicalSort()
        assertEquals(listOf("A", "B", "C"), result)
    }

    @Test
    fun testMapExtensionHasCycle() {
        val acyclic = mapOf(
            "A" to emptyList<String>(),
            "B" to listOf("A")
        )
        assertFalse(acyclic.hasCycle())

        val cyclic = mapOf(
            "A" to listOf("B"),
            "B" to listOf("A")
        )
        assertTrue(cyclic.hasCycle())
    }

    // =========================================================================
    // 复杂场景测试
    // =========================================================================

    @Test
    fun testCourseSchedule() {
        // 课程安排问题: 课程 B 依赖课程 A
        val courses = mapOf(
            "math" to emptyList<String>(),
            "physics" to listOf("math"),
            "chemistry" to listOf("math"),
            "advanced_physics" to listOf("physics", "math"),
            "quantum_mechanics" to listOf("advanced_physics", "chemistry")
        )

        val schedule = TopologicalSortUtils.resolveDependencies(courses)
        
        // 验证依赖顺序
        assertTrue(schedule.indexOf("math") < schedule.indexOf("physics"))
        assertTrue(schedule.indexOf("math") < schedule.indexOf("chemistry"))
        assertTrue(schedule.indexOf("physics") < schedule.indexOf("advanced_physics"))
        assertTrue(schedule.indexOf("advanced_physics") < schedule.indexOf("quantum_mechanics"))
        assertTrue(schedule.indexOf("chemistry") < schedule.indexOf("quantum_mechanics"))
    }

    @Test
    fun testBuildSystem() {
        // 构建系统依赖
        val buildDeps = mapOf(
            "main" to listOf("utils", "core"),
            "core" to listOf("utils"),
            "utils" to emptyList<String>(),
            "tests" to listOf("main", "core")
        )

        val buildOrder = TopologicalSortUtils.resolveDependencies(buildDeps)
        
        assertTrue(buildOrder.indexOf("utils") < buildOrder.indexOf("core"))
        assertTrue(buildOrder.indexOf("utils") < buildOrder.indexOf("main"))
        assertTrue(buildOrder.indexOf("core") < buildOrder.indexOf("main"))
        assertTrue(buildOrder.indexOf("main") < buildOrder.indexOf("tests"))
    }

    @Test
    fun testPackageDependencies() {
        // 包管理器依赖解析
        val packages = mapOf(
            "express" to listOf("body-parser", "cookie-parser", "debug"),
            "body-parser" to listOf("bytes", "content-type"),
            "cookie-parser" to listOf("cookie"),
            "debug" to listOf("ms"),
            "bytes" to emptyList<String>(),
            "content-type" to emptyList<String>(),
            "cookie" to emptyList<String>(),
            "ms" to emptyList<String>()
        )

        val installOrder = TopologicalSortUtils.resolveDependencies(packages)
        
        // 验证基本依赖顺序
        assertTrue(installOrder.indexOf("bytes") < installOrder.indexOf("body-parser"))
        assertTrue(installOrder.indexOf("body-parser") < installOrder.indexOf("express"))
        assertTrue(installOrder.indexOf("cookie") < installOrder.indexOf("cookie-parser"))
        assertTrue(installOrder.indexOf("ms") < installOrder.indexOf("debug"))
    }

    @Test
    fun testParallelBuild() {
        // 测试并行构建场景
        val graph = DirectedGraph.builder<String>()
            .addEdge("libA", "common")
            .addEdge("libB", "common")
            .addEdge("libC", "common")
            .addEdge("app", "libA")
            .addEdge("app", "libB")
            .addEdge("app", "libC")
            .build()

        val groups = TopologicalSortUtils.getParallelGroups(graph)
        
        assertEquals(3, groups.size)
        // 第一层: common
        assertEquals(setOf("common"), groups[0])
        // 第二层: libA, libB, libC (可以并行构建)
        assertEquals(setOf("libA", "libB", "libC"), groups[1])
        // 第三层: app
        assertEquals(setOf("app"), groups[2])
    }

    @Test
    fun testLongestPathChain() {
        // 测试最长路径链
        val graph = DirectedGraph.builder<Int>()
            .addEdge(2, 1)
            .addEdge(3, 2)
            .addEdge(4, 3)
            .addEdge(5, 4)
            .build()

        val distances = TopologicalSortUtils.longestPath(graph)
        
        assertEquals(0, distances[1])
        assertEquals(1, distances[2])
        assertEquals(2, distances[3])
        assertEquals(3, distances[4])
        assertEquals(4, distances[5])
    }

    @Test
    fun testDiamondDependency() {
        // 菱形依赖
        //     A
        //    / \
        //   B   C
        //    \ /
        //     D
        val graph = DirectedGraph.builder<String>()
            .addEdge("B", "A")
            .addEdge("C", "A")
            .addEdge("D", "B")
            .addEdge("D", "C")
            .build()

        val result = TopologicalSortUtils.kahnSort(graph)
        
        assertEquals(4, result.size)
        assertTrue(result.indexOf("A") < result.indexOf("B"))
        assertTrue(result.indexOf("A") < result.indexOf("C"))
        assertTrue(result.indexOf("B") < result.indexOf("D"))
        assertTrue(result.indexOf("C") < result.indexOf("D"))
    }
}
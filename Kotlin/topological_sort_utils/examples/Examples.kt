package topological_sort_utils.examples

import topological_sort_utils.*

/**
 * 拓扑排序工具使用示例
 */
fun main() {
    println("=== Topological Sort Utils Examples ===")
    println()

    // 示例 1: 基本拓扑排序
    basicTopologicalSort()

    // 示例 2: 课程安排
    courseScheduleExample()

    // 示例 3: 构建系统依赖
    buildSystemExample()

    // 示例 4: 循环依赖检测
    cycleDetectionExample()

    // 示例 5: 分层排序（并行处理）
    layeredSortExample()

    // 示例 6: 查找所有可能的排序
    allTopologicalSortsExample()

    // 示例 7: 使用扩展函数
    extensionFunctionsExample()

    // 示例 8: 最长路径计算
    longestPathExample()
}

fun basicTopologicalSort() {
    println("--- Example 1: Basic Topological Sort ---")
    
    // 创建图: A -> B -> C, A -> D
    val graph = DirectedGraph.builder<String>()
        .addEdge("B", "A")  // B 依赖 A
        .addEdge("C", "B")  // C 依赖 B
        .addEdge("D", "A")  // D 依赖 A
        .build()

    println("Graph nodes: ${graph.nodes}")
    println("Graph edges: ${graph.edges}")
    
    val result = TopologicalSortUtils.kahnSort(graph)
    println("Topological order: $result")
    println()
}

fun courseScheduleExample() {
    println("--- Example 2: Course Schedule ---")
    
    // 课程依赖: 每门课程依赖其先修课程
    val courseDependencies = mapOf(
        "Calculus" to emptyList<String>(),
        "Linear Algebra" to emptyList<String>(),
        "Physics" to listOf("Calculus"),
        "Mechanics" to listOf("Physics", "Linear Algebra"),
        "Quantum Physics" to listOf("Mechanics", "Linear Algebra"),
        "Thermodynamics" to listOf("Physics")
    )

    println("Course dependencies: $courseDependencies")
    
    val schedule = TopologicalSortUtils.resolveDependencies(courseDependencies)
    println("Recommended course order: $schedule")
    
    // 获取可以同时学习的课程
    val parallelGroups = TopologicalSortUtils.getParallelGroups(
        DirectedGraph.fromAdjacencyList(courseDependencies)
    )
    println("Parallel study groups:")
    parallelGroups.forEachIndexed { index, group ->
        println("  Semester ${index + 1}: $group")
    }
    println()
}

fun buildSystemExample() {
    println("--- Example 3: Build System Dependencies ---")
    
    // 项目构建依赖
    val buildDeps = DirectedGraph.builder<String>()
        .addEdge("core", "utils")      // core 依赖 utils
        .addEdge("network", "utils")   // network 依赖 utils
        .addEdge("network", "core")    // network 依赖 core
        .addEdge("ui", "core")         // ui 依赖 core
        .addEdge("app", "ui")          // app 依赖 ui
        .addEdge("app", "network")     // app 依赖 network
        .build()

    println("Build dependencies:")
    buildDeps.edges.forEach { (from, toList) ->
        println("  $from depends on: $toList")
    }
    
    val buildOrder = TopologicalSortUtils.kahnSort(buildDeps)
    println("Build order: $buildOrder")
    
    val parallelBuilds = TopologicalSortUtils.layeredSort(buildDeps)
    println("Parallel build stages:")
    parallelBuilds.forEachIndexed { index, stage ->
        println("  Stage ${index + 1}: $stage (can build in parallel)")
    }
    println()
}

fun cycleDetectionExample() {
    println("--- Example 4: Cycle Detection ---")
    
    // 无循环依赖
    val validGraph = DirectedGraph.builder<String>()
        .addEdge("B", "A")
        .addEdge("C", "B")
        .build()

    println("Valid graph has cycle: ${TopologicalSortUtils.hasCycle(validGraph)}")
    
    // 有循环依赖
    val cyclicGraph = DirectedGraph.builder<String>()
        .addEdge("A", "B")
        .addEdge("B", "C")
        .addEdge("C", "A")
        .build()

    println("Cyclic graph has cycle: ${TopologicalSortUtils.hasCycle(cyclicGraph)}")
    
    val cycle = TopologicalSortUtils.findCycle(cyclicGraph)
    println("Found cycle: $cycle")
    
    // 安全排序
    val result = TopologicalSortUtils.sortSafely(cyclicGraph)
    println("Safe sort result: ${if (result.isSuccess) "Success: ${result.getOrNull()}" else "Failure: ${result.exceptionOrNull()?.message}"}")
    println()
}

fun layeredSortExample() {
    println("--- Example 5: Layered Topological Sort ---")
    
    // 软件包依赖
    val packageDeps = DirectedGraph.builder<String>()
        .addEdge("express", "body-parser")
        .addEdge("express", "cookie-parser")
        .addEdge("body-parser", "bytes")
        .addEdge("cookie-parser", "cookie")
        .addNode("bytes")
        .addNode("cookie")
        .build()

    val layers = TopologicalSortUtils.layeredSort(packageDeps)
    
    println("Package installation layers:")
    layers.forEachIndexed { index, layer ->
        println("  Layer ${index + 1}: $layer")
    }
    
    val levels = TopologicalSortUtils.getNodeLevels(packageDeps)
    println("Package levels: $levels")
    println()
}

fun allTopologicalSortsExample() {
    println("--- Example 6: All Possible Topological Sorts ---")
    
    // 简单图: A -> C, B -> C
    val graph = DirectedGraph.builder<String>()
        .addEdge("C", "A")
        .addEdge("C", "B")
        .build()

    val allSorts = TopologicalSortUtils.allTopologicalSorts(graph)
    
    println("Graph: A -> C, B -> C")
    println("All possible topological sorts (${allSorts.size}):")
    allSorts.forEach { sort ->
        println("  $sort")
    }
    println()
}

fun extensionFunctionsExample() {
    println("--- Example 7: Extension Functions ---")
    
    // 使用扩展函数
    val graph = DirectedGraph.builder<Int>()
        .addEdge(2, 1)
        .addEdge(3, 2)
        .addEdge(4, 3)
        .build()

    println("Graph: 1 -> 2 -> 3 -> 4")
    println("Topological sort (extension): ${graph.topologicalSort()}")
    println("Has cycle (extension): ${graph.hasCycle()}")
    println("Layered sort (extension): ${graph.layeredTopologicalSort()}")
    
    // 使用 Map 扩展函数
    val adjacencyList = mapOf(
        1 to emptyList<Int>(),
        2 to listOf(1),
        3 to listOf(2)
    )
    
    println("Adjacency list: $adjacencyList")
    println("Topological sort (map extension): ${adjacencyList.topologicalSort()}")
    println("Has cycle (map extension): ${adjacencyList.hasCycle()}")
    println()
}

fun longestPathExample() {
    println("--- Example 8: Longest Path Calculation ---")
    
    // DAG 中的最长路径（用于关键路径分析）
    val graph = DirectedGraph.builder<String>()
        .addEdge("B", "A")
        .addEdge("C", "A")
        .addEdge("D", "B")
        .addEdge("E", "C")
        .addEdge("F", "D")
        .addEdge("F", "E")
        .build()

    println("Graph for critical path analysis:")
    graph.edges.forEach { (from, toList) ->
        println("  $from depends on: $toList")
    }
    
    val distances = TopologicalSortUtils.longestPath(graph)
    println("Longest path distances from sources:")
    distances.forEach { (node, distance) ->
        println("  $node: $distance")
    }
    
    // 找到关键路径
    val maxDistance = distances.values.maxOrNull() ?: 0
    val criticalPathEnd = distances.filter { it.value == maxDistance }.keys
    println("Critical path endpoints: $criticalPathEnd (distance: $maxDistance)")
    println()
}
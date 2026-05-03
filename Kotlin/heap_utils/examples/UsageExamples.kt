/**
 * Heap Utilities Usage Examples
 * 
 * Demonstrates practical usage of various heap implementations.
 * 
 * @author AllToolkit
 * @date 2026-05-03
 */

package heap_utils.examples

import heap_utils.*

fun main() {
    println("=" * 60)
    println("Heap Utilities - Usage Examples")
    println("=" * 60)
    
    // =========================================================================
    // Example 1: MinHeap - Basic Usage
    // =========================================================================
    println("\n1. MinHeap - Basic Operations")
    println("-" * 40)
    
    val minHeap = MinHeap<Int>()
    
    // Insert elements
    minHeap.insert(50)
    minHeap.insert(30)
    minHeap.insert(70)
    minHeap.insert(10)
    minHeap.insert(40)
    
    println("Inserted: 50, 30, 70, 10, 40")
    println("Heap size: ${minHeap.size()}")
    println("Peek (minimum): ${minHeap.peek()}")
    
    // Extract in sorted order
    println("\nExtracting all elements:")
    while (!minHeap.isEmpty()) {
        println("  Extracted: ${minHeap.extract()}")
    }
    
    // =========================================================================
    // Example 2: MaxHeap - Basic Usage
    // =========================================================================
    println("\n2. MaxHeap - Basic Operations")
    println("-" * 40)
    
    val maxHeap = MaxHeap<Int>()
    
    // Insert elements
    maxHeap.insertAll(listOf(25, 15, 35, 5, 45))
    
    println("Inserted: 25, 15, 35, 5, 45")
    println("Heap size: ${maxHeap.size()}")
    println("Peek (maximum): ${maxHeap.peek()}")
    
    println("\nExtracting all elements:")
    while (!maxHeap.isEmpty()) {
        println("  Extracted: ${maxHeap.extract()}")
    }
    
    // =========================================================================
    // Example 3: PriorityQueue - Task Scheduling
    // =========================================================================
    println("\n3. PriorityQueue - Task Scheduling Example")
    println("-" * 40)
    
    data class Task(
        val priority: Int,
        val name: String,
        val description: String
    )
    
    val taskQueue = PriorityQueue<Task>(16, compareBy { it.priority })
    
    // Add tasks with different priorities
    taskQueue.enqueue(Task(5, "Low priority task", "Daily backup check"))
    taskQueue.enqueue(Task(1, "Critical task", "Fix production bug"))
    taskQueue.enqueue(Task(3, "Medium priority", "Review code changes"))
    taskQueue.enqueue(Task(2, "High priority", "Deploy hotfix"))
    taskQueue.enqueue(Task(4, "Normal task", "Update documentation"))
    
    println("Task queue size: ${taskQueue.size()}")
    
    println("\nProcessing tasks by priority:")
    while (!taskQueue.isEmpty()) {
        val task = taskQueue.dequeue()!!
        println("  [Priority ${task.priority}] ${task.name}: ${task.description}")
    }
    
    // =========================================================================
    // Example 4: BinaryHeap with Custom Comparator
    // =========================================================================
    println("\n4. BinaryHeap - Custom Comparator (String Length)")
    println("-" * 40)
    
    val stringLengthHeap = BinaryHeap<String>(16, compareBy { it.length })
    
    stringLengthHeap.insert("Supercalifragilisticexpialidocious")
    stringLengthHeap.insert("Hello")
    stringLengthHeap.insert("World")
    stringLengthHeap.insert("Kotlin")
    stringLengthHeap.insert("A")
    stringLengthHeap.insert("Programming")
    
    println("Strings inserted with varying lengths")
    println("Heap size: ${stringLengthHeap.size()}")
    
    println("\nExtracting by string length (shortest first):")
    while (!stringLengthHeap.size() > 0) {
        val str = stringLengthHeap.extract()
        if (str != null) {
            println("  '$str' (length: ${str.length})")
        } else break
    }
    
    // =========================================================================
    // Example 5: IndexedMinHeap - Dijkstra-like Algorithm
    // =========================================================================
    println("\n5. IndexedMinHeap - Graph Shortest Path Simulation")
    println("-" * 40)
    
    // Simulate Dijkstra's algorithm for shortest path
    val distanceHeap = IndexedMinHeap<Int>()
    
    // Node distances: (node_id -> distance)
    val nodeIndices = mutableMapOf<String, Int>()
    
    nodeIndices["A"] = distanceHeap.insert(0)    // Starting node
    nodeIndices["B"] = distanceHeap.insert(10)   // Initial distance estimates
    nodeIndices["C"] = distanceHeap.insert(5)
    nodeIndices["D"] = distanceHeap.insert(15)
    nodeIndices["E"] = distanceHeap.insert(20)
    
    println("Initial distances:")
    for ((node, idx) in nodeIndices) {
        println("  Node $node: distance ${distanceHeap.get(idx)}")
    }
    
    // Simulate updating distances as we find shorter paths
    println("\nUpdating distances (finding shorter paths):")
    distanceHeap.update(nodeIndices["B"]!!, 3)   // Found shorter path to B
    distanceHeap.update(nodeIndices["D"]!!, 8)   // Found shorter path to D
    
    println("After updates:")
    for ((node, idx) in nodeIndices) {
        println("  Node $node: distance ${distanceHeap.get(idx)}")
    }
    
    println("\nProcessing nodes by shortest distance:")
    while (!distanceHeap.isEmpty()) {
        val (idx, distance) = distanceHeap.extract()!!
        val node = nodeIndices.entries.find { it.value == idx }?.key ?: "Unknown"
        println("  Node $node: distance $distance")
    }
    
    // =========================================================================
    // Example 6: Heap Sort Algorithm
    // =========================================================================
    println("\n6. Heap Sort - Sorting a List")
    println("-" * 40)
    
    val unsortedList = mutableListOf(64, 34, 25, 12, 22, 11, 90, 45, 78, 33)
    
    println("Original list: $unsortedList")
    
    heapSort(unsortedList)
    
    println("Sorted (ascending): $unsortedList")
    
    // Sort descending
    val listForDesc = mutableListOf(64, 34, 25, 12, 22, 11, 90, 45, 78, 33)
    heapSortDescending(listForDesc)
    
    println("Sorted (descending): $listForDesc")
    
    // =========================================================================
    // Example 7: k-Smallest and k-Largest
    // =========================================================================
    println("\n7. k-Smallest and k-Largest Elements")
    println("-" * 40)
    
    val numbers = listOf(50, 23, 78, 12, 45, 89, 34, 67, 90, 11, 56, 3)
    
    println("Numbers: $numbers")
    
    val smallest3 = kSmallest(numbers, 3)
    println("3 smallest: $smallest3")
    
    val largest5 = kLargest(numbers, 5)
    println("5 largest: $largest5")
    
    val smallest10 = kSmallest(numbers, 10)
    println("10 smallest: $smallest10")
    
    // =========================================================================
    // Example 8: Merge Sorted Lists
    // =========================================================================
    println("\n8. Merge Sorted Lists")
    println("-" * 40)
    
    val sortedLists = listOf(
        listOf(1, 4, 7, 10),
        listOf(2, 5, 8, 11),
        listOf(3, 6, 9, 12),
        listOf(0, 13, 14, 15)
    )
    
    println("Input lists:")
    sortedLists.forEachIndexed { i, list ->
        println("  List $i: $list")
    }
    
    val merged = mergeSortedLists(sortedLists)
    
    println("Merged result: $merged")
    
    // =========================================================================
    // Example 9: Heapify - In-place Conversion
    // =========================================================================
    println("\n9. Heapify - In-place Heap Conversion")
    println("-" * 40)
    
    val arrayForMin = arrayOf(9, 4, 7, 1, 3, 6, 8, 2, 5)
    println("Original array: ${arrayForMin.joinToString(", ")}")
    
    heapifyMin(arrayForMin)
    println("After heapify (min-heap): ${arrayForMin.joinToString(", ")}")
    println("Is valid min-heap: ${isMinHeap(arrayForMin)}")
    println("Root (minimum): ${arrayForMin[0]}")
    
    val arrayForMax = arrayOf(9, 4, 7, 1, 3, 6, 8, 2, 5)
    heapifyMax(arrayForMax)
    println("After heapify (max-heap): ${arrayForMax.joinToString(", ")}")
    println("Is valid max-heap: ${isMaxHeap(arrayForMax)}")
    println("Root (maximum): ${arrayForMax[0]}")
    
    // =========================================================================
    // Example 10: Real-world Use Case - Top K Frequent Words
    // =========================================================================
    println("\n10. Real-world Example - Top K Frequent Words")
    println("-" * 40)
    
    val text = "the quick brown fox jumps over the lazy dog the fox is quick"
    val words = text.split(" ")
    
    // Count word frequencies
    val frequencies = words.groupingBy { it }.eachCount()
    
    println("Word frequencies:")
    frequencies.forEach { (word, count) ->
        println("  '$word': $count")
    }
    
    // Find top 3 most frequent words using max-heap
    val freqHeap = MaxHeap<Pair<String, Int>>()
    frequencies.forEach { (word, count) ->
        freqHeap.insert(Pair(word, count))
    }
    
    println("\nTop 3 most frequent words:")
    for (i in 1..3) {
        if (!freqHeap.isEmpty()) {
            val (word, count) = freqHeap.extract()!!
            println("  $i. '$word' appears $count times")
        }
    }
    
    // =========================================================================
    // Example 11: Real-world Use Case - Median Finding
    // =========================================================================
    println("\n11. Real-world Example - Running Median")
    println("-" * 40)
    
    val streamNumbers = listOf(5, 15, 1, 3, 8, 7, 9, 10, 20, 25)
    
    // Use two heaps: max-heap for lower half, min-heap for upper half
    val lowerHalf = MaxHeap<Int>()  // Stores smaller numbers
    val upperHalf = MinHeap<Int>()  // Stores larger numbers
    
    println("Processing stream and finding medians:")
    
    for (num in streamNumbers) {
        // Insert into appropriate heap
        if (lowerHalf.isEmpty() || num <= lowerHalf.peek()!!) {
            lowerHalf.insert(num)
        } else {
            upperHalf.insert(num)
        }
        
        // Balance heaps (size difference should be at most 1)
        while (lowerHalf.size() > upperHalf.size() + 1) {
            upperHalf.insert(lowerHalf.extract()!!)
        }
        while (upperHalf.size() > lowerHalf.size() + 1) {
            lowerHalf.insert(upperHalf.extract()!!)
        }
        
        // Calculate median
        val median = if (lowerHalf.size() == upperHalf.size()) {
            (lowerHalf.peek()!! + upperHalf.peek()!!) / 2.0
        } else if (lowerHalf.size() > upperHalf.size()) {
            lowerHalf.peek()!!.toDouble()
        } else {
            upperHalf.peek()!!.toDouble()
        }
        
        println("  After adding $num -> median: $median")
    }
    
    // =========================================================================
    // Example 12: Real-world Use Case - Task Scheduler Simulation
    // =========================================================================
    println("\n12. Real-world Example - CPU Task Scheduler")
    println("-" * 40)
    
    data class CPUTask(
        val id: Int,
        val burstTime: Int,
        val arrivalTime: Int
    )
    
    // Simulate Shortest Job First (SJF) scheduling
    val tasks = listOf(
        CPUTask(1, 6, 0),
        CPUTask(2, 8, 0),
        CPUTask(3, 7, 0),
        CPUTask(4, 3, 0)
    )
    
    val sjfQueue = PriorityQueue<CPUTask>(16, compareBy { it.burstTime })
    tasks.forEach { sjfQueue.enqueue(it) }
    
    println("Tasks (SJF scheduling):")
    tasks.forEach { println("  Task ${it.id}: burst=${it.burstTime}, arrival=${it.arrivalTime}") }
    
    var currentTime = 0
    var totalWaiting = 0
    var totalTurnaround = 0
    
    println("\nExecution order:")
    while (!sjfQueue.isEmpty()) {
        val task = sjfQueue.dequeue()!!
        val waiting = currentTime - task.arrivalTime
        val turnaround = waiting + task.burstTime
        
        totalWaiting += waiting
        totalTurnaround += turnaround
        
        println("  Task ${task.id}: starts at $currentTime, waits $waiting, finishes at ${currentTime + task.burstTime}")
        
        currentTime += task.burstTime
    }
    
    val avgWaiting = totalWaiting.toDouble() / tasks.size
    val avgTurnaround = totalTurnaround.toDouble() / tasks.size
    
    println("\nAverage waiting time: $avgWaiting")
    println("Average turnaround time: $avgTurnaround")
    
    println("\n" + "=" * 60)
    println("All examples completed successfully!")
    println("=" * 60)
}

// Helper extension for string multiplication
private operator fun String.times(n: Int): String = this.repeat(n)
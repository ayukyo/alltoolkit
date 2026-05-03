# Heap Utilities for Kotlin

A comprehensive heap implementation module with zero external dependencies.

## Features

### Heap Implementations

- **MinHeap**: Minimum heap with smallest element at root
- **MaxHeap**: Maximum heap with largest element at root  
- **BinaryHeap**: Generic heap with custom comparator
- **IndexedMinHeap**: Heap with index-based element updates (useful for algorithms like Dijkstra)
- **PriorityQueue**: Priority queue using binary heap

### Algorithm Functions

- **heapifyMin/heapifyMax**: In-place heap conversion (O(n))
- **heapSort/heapSortDescending**: Heap-based sorting (O(n log n))
- **kSmallest/kLargest**: Find k smallest/largest elements (O(n log k))
- **mergeSortedLists**: Merge multiple sorted lists (O(n log k))
- **isMinHeap/isMaxHeap**: Validate heap property

## Usage

### Basic MinHeap

```kotlin
import heap_utils.*

val heap = MinHeap<Int>()
heap.insert(5)
heap.insert(3)
heap.insert(1)

println(heap.peek())     // 1 (minimum)
println(heap.extract())  // 1
println(heap.extract())  // 3
println(heap.extract())  // 5
```

### Basic MaxHeap

```kotlin
val heap = MaxHeap<Int>()
heap.insertAll(listOf(5, 3, 1, 8, 2))

println(heap.peek())     // 8 (maximum)
println(heap.extract())  // 8
```

### PriorityQueue

```kotlin
data class Task(val priority: Int, val name: String)

val pq = PriorityQueue<Task>(16, compareBy { it.priority })
pq.enqueue(Task(5, "low priority"))
pq.enqueue(Task(1, "high priority"))
pq.enqueue(Task(3, "medium priority"))

// Tasks are processed by priority (lowest first)
while (!pq.isEmpty()) {
    println(pq.dequeue())  // high priority, medium priority, low priority
}
```

### Custom Comparator

```kotlin
// Heap ordered by string length (shortest first)
val heap = BinaryHeap<String>(16, compareBy { it.length })
heap.insert("hello")
heap.insert("hi")
heap.insert("supercalifragilisticexpialidocious")

println(heap.extract())  // "hi" (shortest)
```

### IndexedMinHeap (for Dijkstra-style algorithms)

```kotlin
val distances = IndexedMinHeap<Int>()
val nodeA = distances.insert(10)  // Returns index
val nodeB = distances.insert(5)

// Update distance
distances.update(nodeA, 3)  // Found shorter path

// Extract nodes by shortest distance
while (!distances.isEmpty()) {
    val (index, distance) = distances.extract()!!
    println("Node $index: distance $distance")
}
```

### Heap Sort

```kotlin
val list = mutableListOf(5, 3, 8, 1, 4, 9, 2)
heapSort(list)           // [1, 2, 3, 4, 5, 8, 9]
heapSortDescending(list) // [9, 8, 5, 4, 3, 2, 1]
```

### k-Smallest / k-Largest

```kotlin
val numbers = listOf(50, 23, 78, 12, 45, 89, 34, 67, 90, 11)

val smallest3 = kSmallest(numbers, 3)  // [11, 12, 23]
val largest5 = kLargest(numbers, 5)    // [90, 89, 78, 67, 50]
```

### Merge Sorted Lists

```kotlin
val lists = listOf(
    listOf(1, 4, 7),
    listOf(2, 5, 8),
    listOf(3, 6, 9)
)

val merged = mergeSortedLists(lists)  // [1, 2, 3, 4, 5, 6, 7, 8, 9]
```

## Time Complexity

| Operation        | MinHeap | MaxHeap | IndexedMinHeap |
|------------------|---------|---------|----------------|
| insert           | O(log n)| O(log n)| O(log n)       |
| extract          | O(log n)| O(log n)| O(log n)       |
| peek             | O(1)    | O(1)    | O(1)           |
| remove           | O(n)    | O(n)    | -              |
| contains         | O(n)    | O(n)    | -              |
| update (indexed) | -       | -       | O(log n)       |
| heapify          | O(n)    | O(n)    | -              |
| heapSort         | O(n log n) | - | -           |
| kSmallest/kLargest | O(n log k) | - | -         |

## Applications

- Priority queues for task scheduling
- Shortest path algorithms (Dijkstra)
- Sorting (heapsort)
- Finding median in streaming data
- Top-k element queries
- Merging sorted sequences
- Huffman encoding
- CPU scheduling (SJF algorithm)

## Testing

Run tests with:

```bash
kotlinc HeapUtilsTest.kt -include-runtime -d HeapUtilsTest.jar
kotlin -classpath HeapUtilsTest.jar HeapUtilsTest
```

Or use a testing framework like KotlinTest.

## License

MIT License - Part of AllToolkit project

## Author

AllToolkit Contributors
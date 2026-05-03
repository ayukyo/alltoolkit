/**
 * Heap Utilities for Kotlin
 * 
 * Provides efficient heap implementations with zero external dependencies.
 * Includes MinHeap, MaxHeap, BinaryHeap, and PriorityQueue with various
 * operations like insert, extract, heapify, and heapsort.
 * 
 * @author AllToolkit
 * @date 2026-05-03
 */

package heap_utils

import java.util.concurrent.atomic.AtomicInteger

/**
 * MinHeap - Minimum Heap implementation
 * Smallest element is always at the root
 */
class MinHeap<T : Comparable<T>>(initialCapacity: Int = 16) {
    private var data: Array<Any?> = arrayOfNulls(initialCapacity)
    private var size: Int = 0
    
    /**
     * Insert an element into the heap
     * Time complexity: O(log n)
     */
    fun insert(element: T) {
        ensureCapacity()
        data[size] = element
        siftUp(size)
        size++
    }
    
    /**
     * Insert all elements from a collection
     */
    fun insertAll(elements: Collection<T>) {
        elements.forEach { insert(it) }
    }
    
    /**
     * Get the minimum element without removing it
     * Time complexity: O(1)
     * @return The minimum element or null if heap is empty
     */
    fun peek(): T? {
        return if (size > 0) data[0] as T else null
    }
    
    /**
     * Extract and remove the minimum element
     * Time complexity: O(log n)
     * @return The minimum element or null if heap is empty
     */
    fun extract(): T? {
        if (size == 0) return null
        
        val min = data[0] as T
        size--
        
        if (size > 0) {
            data[0] = data[size]
            data[size] = null
            siftDown(0)
        } else {
            data[0] = null
        }
        
        return min
    }
    
    /**
     * Remove a specific element from the heap
     * Time complexity: O(n) for search + O(log n) for removal
     * @return true if element was found and removed
     */
    fun remove(element: T): Boolean {
        for (i in 0 until size) {
            if (data[i] == element) {
                size--
                if (i < size) {
                    data[i] = data[size]
                    data[size] = null
                    siftDown(i)
                    siftUp(i)
                } else {
                    data[i] = null
                }
                return true
            }
        }
        return false
    }
    
    /**
     * Check if the heap contains an element
     * Time complexity: O(n)
     */
    fun contains(element: T): Boolean {
        for (i in 0 until size) {
            if (data[i] == element) return true
        }
        return false
    }
    
    /**
     * Check if heap is empty
     */
    fun isEmpty(): Boolean = size == 0
    
    /**
     * Get the number of elements in the heap
     */
    fun size(): Int = size
    
    /**
     * Remove all elements from the heap
     */
    fun clear() {
        data = arrayOfNulls(16)
        size = 0
    }
    
    /**
     * Get all elements as a list (not sorted)
     */
    fun toList(): List<T> = (0 until size).map { data[it] as T }
    
    /**
     * Get elements in sorted order (ascending) without modifying the heap
     */
    fun toSortedList(): List<T> {
        val result = toList().toMutableList()
        heapSort(result)
        return result
    }
    
    private fun ensureCapacity() {
        if (size >= data.size) {
            data = data.copyOf(data.size * 2)
        }
    }
    
    private fun siftUp(index: Int) {
        var i = index
        while (i > 0) {
            val parent = (i - 1) / 2
            if ((data[i] as T) < (data[parent] as T)) {
                swap(i, parent)
                i = parent
            } else {
                break
            }
        }
    }
    
    private fun siftDown(index: Int) {
        var i = index
        while (true) {
            val left = 2 * i + 1
            val right = 2 * i + 2
            var smallest = i
            
            if (left < size && (data[left] as T) < (data[smallest] as T)) {
                smallest = left
            }
            if (right < size && (data[right] as T) < (data[smallest] as T)) {
                smallest = right
            }
            
            if (smallest != i) {
                swap(i, smallest)
                i = smallest
            } else {
                break
            }
        }
    }
    
    private fun swap(i: Int, j: Int) {
        val temp = data[i]
        data[i] = data[j]
        data[j] = temp
    }
}

/**
 * MaxHeap - Maximum Heap implementation
 * Largest element is always at the root
 */
class MaxHeap<T : Comparable<T>>(initialCapacity: Int = 16) {
    private var data: Array<Any?> = arrayOfNulls(initialCapacity)
    private var size: Int = 0
    
    /**
     * Insert an element into the heap
     * Time complexity: O(log n)
     */
    fun insert(element: T) {
        ensureCapacity()
        data[size] = element
        siftUp(size)
        size++
    }
    
    /**
     * Insert all elements from a collection
     */
    fun insertAll(elements: Collection<T>) {
        elements.forEach { insert(it) }
    }
    
    /**
     * Get the maximum element without removing it
     * Time complexity: O(1)
     * @return The maximum element or null if heap is empty
     */
    fun peek(): T? {
        return if (size > 0) data[0] as T else null
    }
    
    /**
     * Extract and remove the maximum element
     * Time complexity: O(log n)
     * @return The maximum element or null if heap is empty
     */
    fun extract(): T? {
        if (size == 0) return null
        
        val max = data[0] as T
        size--
        
        if (size > 0) {
            data[0] = data[size]
            data[size] = null
            siftDown(0)
        } else {
            data[0] = null
        }
        
        return max
    }
    
    /**
     * Remove a specific element from the heap
     * Time complexity: O(n)
     * @return true if element was found and removed
     */
    fun remove(element: T): Boolean {
        for (i in 0 until size) {
            if (data[i] == element) {
                size--
                if (i < size) {
                    data[i] = data[size]
                    data[size] = null
                    siftDown(i)
                    siftUp(i)
                } else {
                    data[i] = null
                }
                return true
            }
        }
        return false
    }
    
    /**
     * Check if the heap contains an element
     * Time complexity: O(n)
     */
    fun contains(element: T): Boolean {
        for (i in 0 until size) {
            if (data[i] == element) return true
        }
        return false
    }
    
    /**
     * Check if heap is empty
     */
    fun isEmpty(): Boolean = size == 0
    
    /**
     * Get the number of elements in the heap
     */
    fun size(): Int = size
    
    /**
     * Remove all elements from the heap
     */
    fun clear() {
        data = arrayOfNulls(16)
        size = 0
    }
    
    /**
     * Get all elements as a list (not sorted)
     */
    fun toList(): List<T> = (0 until size).map { data[it] as T }
    
    /**
     * Get elements in sorted order (descending) without modifying the heap
     */
    fun toSortedList(): List<T> {
        val result = toList().toMutableList()
        heapSortDescending(result)
        return result
    }
    
    private fun ensureCapacity() {
        if (size >= data.size) {
            data = data.copyOf(data.size * 2)
        }
    }
    
    private fun siftUp(index: Int) {
        var i = index
        while (i > 0) {
            val parent = (i - 1) / 2
            if ((data[i] as T) > (data[parent] as T)) {
                swap(i, parent)
                i = parent
            } else {
                break
            }
        }
    }
    
    private fun siftDown(index: Int) {
        var i = index
        while (true) {
            val left = 2 * i + 1
            val right = 2 * i + 2
            var largest = i
            
            if (left < size && (data[left] as T) > (data[largest] as T)) {
                largest = left
            }
            if (right < size && (data[right] as T) > (data[largest] as T)) {
                largest = right
            }
            
            if (largest != i) {
                swap(i, largest)
                i = largest
            } else {
                break
            }
        }
    }
    
    private fun swap(i: Int, j: Int) {
        val temp = data[i]
        data[i] = data[j]
        data[j] = temp
    }
}

/**
 * BinaryHeap - Generic Binary Heap with custom comparator
 * Can be configured as min-heap or max-heap
 */
class BinaryHeap<T>(
    initialCapacity: Int = 16,
    private val comparator: Comparator<T>
) {
    private var data: Array<Any?> = arrayOfNulls(initialCapacity)
    private var size: Int = 0
    
    /**
     * Insert an element into the heap
     */
    fun insert(element: T) {
        ensureCapacity()
        data[size] = element
        siftUp(size)
        size++
    }
    
    /**
     * Insert all elements from a collection
     */
    fun insertAll(elements: Collection<T>) {
        elements.forEach { insert(it) }
    }
    
    /**
     * Get the root element without removing it
     */
    fun peek(): T? = if (size > 0) data[0] as T else null
    
    /**
     * Extract and remove the root element
     */
    fun extract(): T? {
        if (size == 0) return null
        
        val root = data[0] as T
        size--
        
        if (size > 0) {
            data[0] = data[size]
            data[size] = null
            siftDown(0)
        } else {
            data[0] = null
        }
        
        return root
    }
    
    /**
     * Check if heap is empty
     */
    fun isEmpty(): Boolean = size == 0
    
    /**
     * Get the number of elements in the heap
     */
    fun size(): Int = size
    
    /**
     * Clear all elements
     */
    fun clear() {
        data = arrayOfNulls(16)
        size = 0
    }
    
    /**
     * Get all elements as a list
     */
    fun toList(): List<T> = (0 until size).map { data[it] as T }
    
    private fun ensureCapacity() {
        if (size >= data.size) {
            data = data.copyOf(data.size * 2)
        }
    }
    
    private fun siftUp(index: Int) {
        var i = index
        while (i > 0) {
            val parent = (i - 1) / 2
            if (comparator.compare(data[i] as T, data[parent] as T) < 0) {
                swap(i, parent)
                i = parent
            } else {
                break
            }
        }
    }
    
    private fun siftDown(index: Int) {
        var i = index
        while (true) {
            val left = 2 * i + 1
            val right = 2 * i + 2
            var extremum = i
            
            if (left < size && comparator.compare(data[left] as T, data[extremum] as T) < 0) {
                extremum = left
            }
            if (right < size && comparator.compare(data[right] as T, data[extremum] as T) < 0) {
                extremum = right
            }
            
            if (extremum != i) {
                swap(i, extremum)
                i = extremum
            } else {
                break
            }
        }
    }
    
    private fun swap(i: Int, j: Int) {
        val temp = data[i]
        data[i] = data[j]
        data[j] = temp
    }
    
    companion object {
        /**
         * Create a min-heap with custom comparator
         */
        fun <T> minHeap(comparator: Comparator<T>): BinaryHeap<T> = BinaryHeap(comparator = comparator)
        
        /**
         * Create a max-heap with custom comparator
         */
        fun <T> maxHeap(comparator: Comparator<T>): BinaryHeap<T> = BinaryHeap(comparator = comparator.reversed())
    }
}

/**
 * PriorityQueue - Priority Queue implementation using binary heap
 * Supports custom priority comparator
 */
class PriorityQueue<T>(
    initialCapacity: Int = 16,
    private val comparator: Comparator<T>
) {
    private val heap = BinaryHeap<T>(initialCapacity, comparator)
    
    /**
     * Enqueue an element with its priority determined by the comparator
     */
    fun enqueue(element: T) {
        heap.insert(element)
    }
    
    /**
     * Enqueue multiple elements
     */
    fun enqueueAll(elements: Collection<T>) {
        heap.insertAll(elements)
    }
    
    /**
     * Dequeue the highest priority element
     */
    fun dequeue(): T? = heap.extract()
    
    /**
     * Peek at the highest priority element without removing it
     */
    fun peek(): T? = heap.peek()
    
    /**
     * Check if queue is empty
     */
    fun isEmpty(): Boolean = heap.isEmpty()
    
    /**
     * Get the number of elements in the queue
     */
    fun size(): Int = heap.size()
    
    /**
     * Clear all elements
     */
    fun clear() = heap.clear()
    
    /**
     * Get all elements as a list (not in priority order)
     */
    fun toList(): List<T> = heap.toList()
    
    companion object {
        /**
         * Create a min-priority queue (smallest value has highest priority)
         */
        fun <T : Comparable<T>> minPriorityQueue(): PriorityQueue<T> {
            return PriorityQueue(16, naturalOrder())
        }
        
        /**
         * Create a max-priority queue (largest value has highest priority)
         */
        fun <T : Comparable<T>> maxPriorityQueue(): PriorityQueue<T> {
            return PriorityQueue(16, reverseOrder())
        }
    }
}

/**
 * IndexedHeap - Heap with support for updating elements by index/key
 * Useful for algorithms like Dijkstra's shortest path
 */
class IndexedMinHeap<T : Comparable<T>>(initialCapacity: Int = 16) {
    private var data: Array<Any?> = arrayOfNulls(initialCapacity)
    private val indexMap = mutableMapOf<Int, Int>() // external index -> heap index
    private var size: Int = 0
    private var nextIndex = AtomicInteger(0)
    
    /**
     * Insert an element and return its index
     * @return The index that can be used to update/remove this element
     */
    fun insert(element: T): Int {
        ensureCapacity()
        val idx = nextIndex.getAndIncrement()
        data[size] = Pair(idx, element)
        indexMap[idx] = size
        siftUp(size)
        size++
        return idx
    }
    
    /**
     * Get the minimum element without removing it
     */
    fun peek(): T? {
        return if (size > 0) (data[0] as Pair<*, T>).second else null
    }
    
    /**
     * Extract and remove the minimum element
     * @return Pair of (index, element)
     */
    fun extract(): Pair<Int, T>? {
        if (size == 0) return null
        
        val (idx, element) = data[0] as Pair<Int, T>
        size--
        indexMap.remove(idx)
        
        if (size > 0) {
            data[0] = data[size]
            data[size] = null
            val newIdx = (data[0] as Pair<Int, *>).first
            indexMap[newIdx] = 0
            siftDown(0)
        } else {
            data[0] = null
        }
        
        return Pair(idx, element)
    }
    
    /**
     * Update the value at a given index
     * @return true if update was successful
     */
    fun update(index: Int, newValue: T): Boolean {
        val heapIdx = indexMap[index] ?: return false
        val oldValue = (data[heapIdx] as Pair<Int, T>).second
        data[heapIdx] = Pair(index, newValue)
        
        if (newValue < oldValue) {
            siftUp(heapIdx)
        } else {
            siftDown(heapIdx)
        }
        return true
    }
    
    /**
     * Check if an index exists in the heap
     */
    fun containsIndex(index: Int): Boolean = indexMap.containsKey(index)
    
    /**
     * Get the value at a given index
     */
    fun get(index: Int): T? {
        val heapIdx = indexMap[index] ?: return null
        return (data[heapIdx] as Pair<Int, T>).second
    }
    
    /**
     * Check if heap is empty
     */
    fun isEmpty(): Boolean = size == 0
    
    /**
     * Get the number of elements in the heap
     */
    fun size(): Int = size
    
    private fun ensureCapacity() {
        if (size >= data.size) {
            data = data.copyOf(data.size * 2)
        }
    }
    
    private fun siftUp(index: Int) {
        var i = index
        while (i > 0) {
            val parent = (i - 1) / 2
            if ((data[i] as Pair<Int, T>).second < (data[parent] as Pair<Int, T>).second) {
                swap(i, parent)
                i = parent
            } else {
                break
            }
        }
    }
    
    private fun siftDown(index: Int) {
        var i = index
        while (true) {
            val left = 2 * i + 1
            val right = 2 * i + 2
            var smallest = i
            
            if (left < size && (data[left] as Pair<Int, T>).second < (data[smallest] as Pair<Int, T>).second) {
                smallest = left
            }
            if (right < size && (data[right] as Pair<Int, T>).second < (data[smallest] as Pair<Int, T>).second) {
                smallest = right
            }
            
            if (smallest != i) {
                swap(i, smallest)
                i = smallest
            } else {
                break
            }
        }
    }
    
    private fun swap(i: Int, j: Int) {
        val temp = data[i]
        data[i] = data[j]
        data[j] = temp
        
        // Update index map
        indexMap[(data[i] as Pair<Int, *>).first] = i
        indexMap[(data[j] as Pair<Int, *>).first] = j
    }
}

// =============================================================================
// Heap Algorithm Functions
// =============================================================================

/**
 * Heapify an array in-place to form a min-heap
 * Time complexity: O(n)
 */
fun <T : Comparable<T>> heapifyMin(array: Array<T>) {
    for (i in (array.size / 2 - 1) downTo 0) {
        siftDownMin(array, i, array.size)
    }
}

/**
 * Heapify an array in-place to form a max-heap
 * Time complexity: O(n)
 */
fun <T : Comparable<T>> heapifyMax(array: Array<T>) {
    for (i in (array.size / 2 - 1) downTo 0) {
        siftDownMax(array, i, array.size)
    }
}

/**
 * Heapify a list in-place to form a min-heap
 */
fun <T : Comparable<T>> heapifyMin(list: MutableList<T>) {
    for (i in (list.size / 2 - 1) downTo 0) {
        siftDownMin(list, i, list.size)
    }
}

/**
 * Heapify a list in-place to form a max-heap
 */
fun <T : Comparable<T>> heapifyMax(list: MutableList<T>) {
    for (i in (list.size / 2 - 1) downTo 0) {
        siftDownMax(list, i, list.size)
    }
}

/**
 * Perform heap sort on a list (ascending order)
 * Time complexity: O(n log n)
 */
fun <T : Comparable<T>> heapSort(list: MutableList<T>) {
    if (list.size <= 1) return
    
    // Build max heap
    heapifyMax(list)
    
    // Extract elements from heap one by one
    for (i in list.size - 1 downTo 1) {
        // Swap root (maximum) with last element
        val temp = list[0]
        list[0] = list[i]
        list[i] = temp
        
        // Heapify reduced heap
        siftDownMax(list, 0, i)
    }
}

/**
 * Perform heap sort on a list (descending order)
 */
fun <T : Comparable<T>> heapSortDescending(list: MutableList<T>) {
    if (list.size <= 1) return
    
    // Build min heap
    heapifyMin(list)
    
    // Extract elements from heap one by one
    for (i in list.size - 1 downTo 1) {
        // Swap root (minimum) with last element
        val temp = list[0]
        list[0] = list[i]
        list[i] = temp
        
        // Heapify reduced heap
        siftDownMin(list, 0, i)
    }
}

/**
 * Find the k smallest elements in a collection
 * Uses a max-heap of size k
 * Time complexity: O(n log k)
 */
fun <T : Comparable<T>> kSmallest(elements: Collection<T>, k: Int): List<T> {
    if (k <= 0) return emptyList()
    if (k >= elements.size) return elements.sorted()
    
    val maxHeap = MaxHeap<T>(k + 1)
    for (element in elements) {
        maxHeap.insert(element)
        if (maxHeap.size() > k) {
            maxHeap.extract()
        }
    }
    
    return maxHeap.toSortedList().reversed()
}

/**
 * Find the k largest elements in a collection
 * Uses a min-heap of size k
 * Time complexity: O(n log k)
 */
fun <T : Comparable<T>> kLargest(elements: Collection<T>, k: Int): List<T> {
    if (k <= 0) return emptyList()
    if (k >= elements.size) return elements.sortedDescending()
    
    val minHeap = MinHeap<T>(k + 1)
    for (element in elements) {
        minHeap.insert(element)
        if (minHeap.size() > k) {
            minHeap.extract()
        }
    }
    
    return minHeap.toSortedList().reversed()
}

/**
 * Merge multiple sorted lists using a min-heap
 * Time complexity: O(n log k) where n is total elements, k is number of lists
 */
fun <T : Comparable<T>> mergeSortedLists(lists: List<List<T>>): List<T> {
    if (lists.isEmpty()) return emptyList()
    
    val result = mutableListOf<T>()
    
    // Use a data class to wrap elements with their source information
    data class HeapEntry(val value: T, val listIdx: Int, val elemIdx: Int)
    
    val minHeap = BinaryHeap<HeapEntry>(16, compareBy { it.value })
    
    // Initialize heap with first element from each list
    lists.forEachIndexed { listIdx, list ->
        if (list.isNotEmpty()) {
            minHeap.insert(HeapEntry(list[0], listIdx, 0))
        }
    }
    
    while (minHeap.size() > 0) {
        val entry = minHeap.extract()!!
        result.add(entry.value)
        
        // Add next element from same list
        val nextIdx = entry.elemIdx + 1
        if (nextIdx < lists[entry.listIdx].size) {
            minHeap.insert(HeapEntry(lists[entry.listIdx][nextIdx], entry.listIdx, nextIdx))
        }
    }
    
    return result
}

/**
 * Check if an array satisfies the min-heap property
 */
fun <T : Comparable<T>> isMinHeap(array: Array<T>): Boolean {
    for (i in 0 until array.size / 2) {
        val left = 2 * i + 1
        val right = 2 * i + 2
        
        if (left < array.size && array[left] < array[i]) return false
        if (right < array.size && array[right] < array[i]) return false
    }
    return true
}

/**
 * Check if an array satisfies the max-heap property
 */
fun <T : Comparable<T>> isMaxHeap(array: Array<T>): Boolean {
    for (i in 0 until array.size / 2) {
        val left = 2 * i + 1
        val right = 2 * i + 2
        
        if (left < array.size && array[left] > array[i]) return false
        if (right < array.size && array[right] > array[i]) return false
    }
    return true
}

// =============================================================================
// Private Helper Functions
// =============================================================================

private fun <T : Comparable<T>> siftDownMin(array: Array<T>, index: Int, size: Int) {
    var i = index
    while (true) {
        val left = 2 * i + 1
        val right = 2 * i + 2
        var smallest = i
        
        if (left < size && array[left] < array[smallest]) smallest = left
        if (right < size && array[right] < array[smallest]) smallest = right
        
        if (smallest != i) {
            val temp = array[i]
            array[i] = array[smallest]
            array[smallest] = temp
            i = smallest
        } else {
            break
        }
    }
}

private fun <T : Comparable<T>> siftDownMax(array: Array<T>, index: Int, size: Int) {
    var i = index
    while (true) {
        val left = 2 * i + 1
        val right = 2 * i + 2
        var largest = i
        
        if (left < size && array[left] > array[largest]) largest = left
        if (right < size && array[right] > array[largest]) largest = right
        
        if (largest != i) {
            val temp = array[i]
            array[i] = array[largest]
            array[largest] = temp
            i = largest
        } else {
            break
        }
    }
}

private fun <T : Comparable<T>> siftDownMin(list: MutableList<T>, index: Int, size: Int) {
    var i = index
    while (true) {
        val left = 2 * i + 1
        val right = 2 * i + 2
        var smallest = i
        
        if (left < size && list[left] < list[smallest]) smallest = left
        if (right < size && list[right] < list[smallest]) smallest = right
        
        if (smallest != i) {
            val temp = list[i]
            list[i] = list[smallest]
            list[smallest] = temp
            i = smallest
        } else {
            break
        }
    }
}

private fun <T : Comparable<T>> siftDownMax(list: MutableList<T>, index: Int, size: Int) {
    var i = index
    while (true) {
        val left = 2 * i + 1
        val right = 2 * i + 2
        var largest = i
        
        if (left < size && list[left] > list[largest]) largest = left
        if (right < size && list[right] > list[largest]) largest = right
        
        if (largest != i) {
            val temp = list[i]
            list[i] = list[largest]
            list[largest] = temp
            i = largest
        } else {
            break
        }
    }
}
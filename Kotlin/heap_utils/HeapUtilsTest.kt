/**
 * Heap Utilities Test Suite
 * 
 * Comprehensive tests for all heap implementations.
 * Zero external dependencies - uses simple assertion functions.
 * 
 * @author AllToolkit
 * @date 2026-05-03
 */

package heap_utils

// Simple assertion functions (zero external dependencies)
fun assertEquals(expected: Any?, actual: Any?, message: String = "") {
    if (expected != actual) {
        throw AssertionError("Expected: $expected, Actual: $actual. $message")
    }
}

fun assertTrue(condition: Boolean, message: String = "") {
    if (!condition) {
        throw AssertionError("Expected true but was false. $message")
    }
}

fun assertFalse(condition: Boolean, message: String = "") {
    if (condition) {
        throw AssertionError("Expected false but was true. $message")
    }
}

fun assertNull(value: Any?, message: String = "") {
    if (value != null) {
        throw AssertionError("Expected null but was: $value. $message")
    }
}

fun assertNotNull(value: Any?, message: String = "") {
    if (value == null) {
        throw AssertionError("Expected non-null but was null. $message")
    }
}

/**
 * Test runner class
 */
object HeapUtilsTest {
    
    private var testsPassed = 0
    private var testsFailed = 0
    
    fun runTest(name: String, test: () -> Unit) {
        try {
            test()
            testsPassed++
            println("  ✓ $name")
        } catch (e: AssertionError) {
            testsFailed++
            println("  ✗ $name")
            println("    Error: ${e.message}")
        } catch (e: Exception) {
            testsFailed++
            println("  ✗ $name")
            println("    Exception: ${e.message}")
        }
    }
    
    fun runAllTests() {
        println("=" * 60)
        println("Heap Utilities Test Suite")
        println("=" * 60)
        
        // =========================================================================
        // MinHeap Tests
        // =========================================================================
        println("\nMinHeap Tests")
        println("-" * 40)
        
        runTest("insertAndExtract") { testMinHeapInsertAndExtract() }
        runTest("peek") { testMinHeapPeek() }
        runTest("insertAll") { testMinHeapInsertAll() }
        runTest("remove") { testMinHeapRemove() }
        runTest("contains") { testMinHeapContains() }
        runTest("clear") { testMinHeapClear() }
        runTest("toSortedList") { testMinHeapToSortedList() }
        runTest("withStrings") { testMinHeapWithStrings() }
        
        // =========================================================================
        // MaxHeap Tests
        // =========================================================================
        println("\nMaxHeap Tests")
        println("-" * 40)
        
        runTest("insertAndExtract") { testMaxHeapInsertAndExtract() }
        runTest("peek") { testMaxHeapPeek() }
        runTest("insertAll") { testMaxHeapInsertAll() }
        runTest("remove") { testMaxHeapRemove() }
        runTest("withStrings") { testMaxHeapWithStrings() }
        
        // =========================================================================
        // BinaryHeap Tests
        // =========================================================================
        println("\nBinaryHeap Tests")
        println("-" * 40)
        
        runTest("customComparator") { testBinaryHeapWithCustomComparator() }
        runTest("maxHeap") { testBinaryHeapMaxHeap() }
        runTest("minHeap") { testBinaryHeapMinHeap() }
        
        // =========================================================================
        // PriorityQueue Tests
        // =========================================================================
        println("\nPriorityQueue Tests")
        println("-" * 40)
        
        runTest("minPriorityQueue") { testMinPriorityQueue() }
        runTest("maxPriorityQueue") { testMaxPriorityQueue() }
        runTest("peek") { testPriorityQueuePeek() }
        runTest("enqueueAll") { testPriorityQueueEnqueueAll() }
        runTest("customComparator") { testPriorityQueueCustomComparator() }
        
        // =========================================================================
        // IndexedMinHeap Tests
        // =========================================================================
        println("\nIndexedMinHeap Tests")
        println("-" * 40)
        
        runTest("basic") { testIndexedMinHeapBasic() }
        runTest("updateToSmaller") { testIndexedMinHeapUpdate() }
        runTest("updateToLarger") { testIndexedMinHeapUpdateToLarger() }
        runTest("get") { testIndexedMinHeapGet() }
        
        // =========================================================================
        // Heap Algorithm Tests
        // =========================================================================
        println("\nHeap Algorithm Tests")
        println("-" * 40)
        
        runTest("heapifyMin") { testHeapifyMin() }
        runTest("heapifyMax") { testHeapifyMax() }
        runTest("heapifyMinList") { testHeapifyMinList() }
        runTest("heapifyMaxList") { testHeapifyMaxList() }
        runTest("heapSort") { testHeapSort() }
        runTest("heapSortDescending") { testHeapSortDescending() }
        runTest("heapSortEmpty") { testHeapSortEmptyList() }
        runTest("heapSortSingle") { testHeapSortSingleElement() }
        runTest("kSmallest") { testKSmallest() }
        runTest("kSmallestKEqualsSize") { testKSmallestKEqualsSize() }
        runTest("kSmallestKZero") { testKSmallestKZero() }
        runTest("kLargest") { testKLargest() }
        runTest("kLargestKEqualsSize") { testKLargestKEqualsSize() }
        runTest("mergeSortedLists") { testMergeSortedLists() }
        runTest("mergeSortedListsEmpty") { testMergeSortedListsEmptyLists() }
        runTest("mergeSortedListsSingle") { testMergeSortedListsSingleList() }
        runTest("isMinHeap") { testIsMinHeap() }
        runTest("isMaxHeap") { testIsMaxHeap() }
        runTest("isMinHeapEmpty") { testIsMinHeapEmpty() }
        runTest("isMaxHeapEmpty") { testIsMaxHeapEmpty() }
        
        // =========================================================================
        // Edge Case Tests
        // =========================================================================
        println("\nEdge Case Tests")
        println("-" * 40)
        
        runTest("negativeNumbers") { testMinHeapWithNegativeNumbers() }
        runTest("duplicateValues") { testMinHeapWithDuplicateValues() }
        runTest("maxHeapDuplicates") { testMaxHeapWithDuplicateValues() }
        runTest("complexObjects") { testPriorityQueueWithComplexObjects() }
        runTest("capacityGrowth") { testHeapCapacityGrowth() }
        runTest("largeDataset") { testHeapLargeDataset() }
        runTest("kLargeDataset") { testKLargeDataset() }
        runTest("mergeLargeLists") { testMergeLargeSortedLists() }
        
        // =========================================================================
        // Stress Tests
        // =========================================================================
        println("\nStress Tests")
        println("-" * 40)
        
        runTest("minHeapStress") { testMinHeapStressTest() }
        runTest("maxHeapStress") { testMaxHeapStressTest() }
        runTest("heapSortStress") { testHeapSortStressTest() }
        
        // =========================================================================
        // Summary
        // =========================================================================
        println("\n" + "=" * 60)
        println("Test Summary: $testsPassed passed, $testsFailed failed")
        println("=" * 60)
        
        if (testsFailed > 0) {
            println("\n❌ Some tests failed!")
            System.exit(1)
        } else {
            println("\n✅ All tests passed!")
        }
    }
    
    // =========================================================================
    // MinHeap Test Functions
    // =========================================================================
    
    fun testMinHeapInsertAndExtract() {
        val heap = MinHeap<Int>()
        heap.insert(5)
        heap.insert(3)
        heap.insert(7)
        heap.insert(1)
        heap.insert(9)
        
        assertEquals(5, heap.size())
        
        assertEquals(1, heap.extract())
        assertEquals(3, heap.extract())
        assertEquals(5, heap.extract())
        assertEquals(7, heap.extract())
        assertEquals(9, heap.extract())
        assertNull(heap.extract())
    }
    
    fun testMinHeapPeek() {
        val heap = MinHeap<Int>()
        assertNull(heap.peek())
        
        heap.insert(10)
        assertEquals(10, heap.peek())
        
        heap.insert(5)
        assertEquals(5, heap.peek())
        
        heap.insert(20)
        assertEquals(5, heap.peek())
        
        assertEquals(5, heap.extract())
        assertEquals(10, heap.peek())
    }
    
    fun testMinHeapInsertAll() {
        val heap = MinHeap<Int>()
        heap.insertAll(listOf(5, 3, 8, 1, 4))
        
        val sorted = heap.toSortedList()
        assertEquals(listOf(1, 3, 4, 5, 8), sorted)
    }
    
    fun testMinHeapRemove() {
        val heap = MinHeap<Int>()
        heap.insertAll(listOf(5, 3, 8, 1, 4))
        
        assertTrue(heap.remove(3))
        assertFalse(heap.remove(3))
        
        assertEquals(4, heap.size())
        
        assertEquals(1, heap.extract())
        assertEquals(4, heap.extract())
        assertEquals(5, heap.extract())
        assertEquals(8, heap.extract())
    }
    
    fun testMinHeapContains() {
        val heap = MinHeap<Int>()
        heap.insertAll(listOf(5, 3, 8))
        
        assertTrue(heap.contains(5))
        assertTrue(heap.contains(3))
        assertTrue(heap.contains(8))
        assertFalse(heap.contains(1))
        assertFalse(heap.contains(10))
    }
    
    fun testMinHeapClear() {
        val heap = MinHeap<Int>()
        heap.insertAll(listOf(5, 3, 8, 1, 4))
        
        heap.clear()
        
        assertTrue(heap.isEmpty())
        assertEquals(0, heap.size())
        assertNull(heap.peek())
        assertNull(heap.extract())
    }
    
    fun testMinHeapToSortedList() {
        val heap = MinHeap<Int>()
        heap.insertAll(listOf(5, 3, 8, 1, 4, 9, 2, 7, 6))
        
        val sorted = heap.toSortedList()
        assertEquals(listOf(1, 2, 3, 4, 5, 6, 7, 8, 9), sorted)
        
        assertEquals(9, heap.size())
    }
    
    fun testMinHeapWithStrings() {
        val heap = MinHeap<String>()
        heap.insertAll(listOf("apple", "banana", "cherry", "date", "elderberry"))
        
        assertEquals("apple", heap.extract())
        assertEquals("banana", heap.extract())
        assertEquals("cherry", heap.extract())
    }
    
    // =========================================================================
    // MaxHeap Test Functions
    // =========================================================================
    
    fun testMaxHeapInsertAndExtract() {
        val heap = MaxHeap<Int>()
        heap.insert(5)
        heap.insert(3)
        heap.insert(7)
        heap.insert(1)
        heap.insert(9)
        
        assertEquals(5, heap.size())
        
        assertEquals(9, heap.extract())
        assertEquals(7, heap.extract())
        assertEquals(5, heap.extract())
        assertEquals(3, heap.extract())
        assertEquals(1, heap.extract())
        assertNull(heap.extract())
    }
    
    fun testMaxHeapPeek() {
        val heap = MaxHeap<Int>()
        assertNull(heap.peek())
        
        heap.insert(10)
        assertEquals(10, heap.peek())
        
        heap.insert(5)
        assertEquals(10, heap.peek())
        
        heap.insert(20)
        assertEquals(20, heap.peek())
    }
    
    fun testMaxHeapInsertAll() {
        val heap = MaxHeap<Int>()
        heap.insertAll(listOf(5, 3, 8, 1, 4))
        
        val sorted = heap.toSortedList()
        assertEquals(listOf(8, 5, 4, 3, 1), sorted)
    }
    
    fun testMaxHeapRemove() {
        val heap = MaxHeap<Int>()
        heap.insertAll(listOf(5, 3, 8, 1, 4))
        
        assertTrue(heap.remove(5))
        assertFalse(heap.remove(5))
        
        assertEquals(4, heap.size())
        
        assertEquals(8, heap.extract())
        assertEquals(4, heap.extract())
        assertEquals(3, heap.extract())
        assertEquals(1, heap.extract())
    }
    
    fun testMaxHeapWithStrings() {
        val heap = MaxHeap<String>()
        heap.insertAll(listOf("apple", "banana", "cherry", "date"))
        
        assertEquals("date", heap.extract())
        assertEquals("cherry", heap.extract())
        assertEquals("banana", heap.extract())
        assertEquals("apple", heap.extract())
    }
    
    // =========================================================================
    // BinaryHeap Test Functions
    // =========================================================================
    
    fun testBinaryHeapWithCustomComparator() {
        // Use a comparator that first compares by length, then by string (for stability)
        val heap = BinaryHeap<String>(16, compareBy<String> { it.length }.thenBy { it })
        heap.insert("apple")
        heap.insert("banana")
        heap.insert("kiwi")
        heap.insert("cherry")
        heap.insert("date")
        
        assertEquals("date", heap.extract())
        assertEquals("kiwi", heap.extract())
        assertEquals("apple", heap.extract())
        assertEquals("banana", heap.extract())
        assertEquals("cherry", heap.extract())
    }
    
    fun testBinaryHeapMaxHeap() {
        val heap = BinaryHeap.maxHeap<Int>(naturalOrder())
        heap.insertAll(listOf(5, 3, 8, 1, 4))
        
        assertEquals(8, heap.extract())
        assertEquals(5, heap.extract())
        assertEquals(4, heap.extract())
        assertEquals(3, heap.extract())
        assertEquals(1, heap.extract())
    }
    
    fun testBinaryHeapMinHeap() {
        val heap = BinaryHeap.minHeap<Int>(naturalOrder())
        heap.insertAll(listOf(5, 3, 8, 1, 4))
        
        assertEquals(1, heap.extract())
        assertEquals(3, heap.extract())
        assertEquals(4, heap.extract())
        assertEquals(5, heap.extract())
        assertEquals(8, heap.extract())
    }
    
    // =========================================================================
    // PriorityQueue Test Functions
    // =========================================================================
    
    fun testMinPriorityQueue() {
        val pq = PriorityQueue.minPriorityQueue<Int>()
        pq.enqueue(5)
        pq.enqueue(3)
        pq.enqueue(7)
        pq.enqueue(1)
        
        assertEquals(1, pq.dequeue())
        assertEquals(3, pq.dequeue())
        assertEquals(5, pq.dequeue())
        assertEquals(7, pq.dequeue())
        assertNull(pq.dequeue())
    }
    
    fun testMaxPriorityQueue() {
        val pq = PriorityQueue.maxPriorityQueue<Int>()
        pq.enqueue(5)
        pq.enqueue(3)
        pq.enqueue(7)
        pq.enqueue(1)
        
        assertEquals(7, pq.dequeue())
        assertEquals(5, pq.dequeue())
        assertEquals(3, pq.dequeue())
        assertEquals(1, pq.dequeue())
        assertNull(pq.dequeue())
    }
    
    fun testPriorityQueuePeek() {
        val pq = PriorityQueue.minPriorityQueue<Int>()
        assertNull(pq.peek())
        
        pq.enqueue(10)
        assertEquals(10, pq.peek())
        
        pq.enqueue(5)
        assertEquals(5, pq.peek())
        
        assertEquals(5, pq.peek())
        assertEquals(2, pq.size())
    }
    
    fun testPriorityQueueEnqueueAll() {
        val pq = PriorityQueue.maxPriorityQueue<Int>()
        pq.enqueueAll(listOf(1, 2, 3, 4, 5))
        
        assertEquals(5, pq.size())
        
        assertEquals(5, pq.dequeue())
        assertEquals(4, pq.dequeue())
        assertEquals(3, pq.dequeue())
        assertEquals(2, pq.dequeue())
        assertEquals(1, pq.dequeue())
    }
    
    fun testPriorityQueueCustomComparator() {
        val pq = PriorityQueue<String>(16, compareBy { it.length })
        
        pq.enqueue("aaaaaaaaa")
        pq.enqueue("bbb")
        pq.enqueue("cccccc")
        pq.enqueue("d")
        
        assertEquals("d", pq.dequeue())
        assertEquals("bbb", pq.dequeue())
        assertEquals("cccccc", pq.dequeue())
        assertEquals("aaaaaaaaa", pq.dequeue())
    }
    
    // =========================================================================
    // IndexedMinHeap Test Functions
    // =========================================================================
    
    fun testIndexedMinHeapBasic() {
        val heap = IndexedMinHeap<Int>()
        
        val idx1 = heap.insert(10)
        val idx2 = heap.insert(5)
        val idx3 = heap.insert(20)
        
        assertTrue(heap.containsIndex(idx1))
        assertTrue(heap.containsIndex(idx2))
        assertTrue(heap.containsIndex(idx3))
        
        assertEquals(5, heap.peek())
        
        val extracted = heap.extract()!!
        assertEquals(5, extracted.second)
        assertEquals(idx2, extracted.first)
        
        assertFalse(heap.containsIndex(idx2))
        
        assertEquals(10, heap.peek())
    }
    
    fun testIndexedMinHeapUpdate() {
        val heap = IndexedMinHeap<Int>()
        
        val idx1 = heap.insert(10)
        val idx2 = heap.insert(5)
        val idx3 = heap.insert(20)
        
        assertTrue(heap.update(idx1, 2))
        
        assertEquals(2, heap.peek())
        assertEquals(2, heap.get(idx1))
        
        assertEquals(2, heap.extract()?.second)
        assertEquals(5, heap.extract()?.second)
        assertEquals(20, heap.extract()?.second)
    }
    
    fun testIndexedMinHeapUpdateToLarger() {
        val heap = IndexedMinHeap<Int>()
        
        val idx1 = heap.insert(5)
        val idx2 = heap.insert(10)
        
        assertTrue(heap.update(idx1, 15))
        
        assertEquals(10, heap.peek())
        
        assertEquals(10, heap.extract()?.second)
        assertEquals(15, heap.extract()?.second)
    }
    
    fun testIndexedMinHeapGet() {
        val heap = IndexedMinHeap<Int>()
        
        val idx1 = heap.insert(10)
        val idx2 = heap.insert(5)
        
        assertEquals(10, heap.get(idx1))
        assertEquals(5, heap.get(idx2))
        assertNull(heap.get(999))
    }
    
    // =========================================================================
    // Heap Algorithm Test Functions
    // =========================================================================
    
    fun testHeapifyMin() {
        val array = arrayOf(5, 3, 8, 1, 4, 9, 2)
        heapifyMin(array)
        
        assertTrue(isMinHeap(array))
        assertEquals(1, array[0])
    }
    
    fun testHeapifyMax() {
        val array = arrayOf(5, 3, 8, 1, 4, 9, 2)
        heapifyMax(array)
        
        assertTrue(isMaxHeap(array))
        assertEquals(9, array[0])
    }
    
    fun testHeapifyMinList() {
        val list = mutableListOf(5, 3, 8, 1, 4, 9, 2)
        heapifyMin(list)
        
        assertEquals(1, list[0])
    }
    
    fun testHeapifyMaxList() {
        val list = mutableListOf(5, 3, 8, 1, 4, 9, 2)
        heapifyMax(list)
        
        assertEquals(9, list[0])
    }
    
    fun testHeapSort() {
        val list = mutableListOf(5, 3, 8, 1, 4, 9, 2, 7, 6)
        heapSort(list)
        
        assertEquals(listOf(1, 2, 3, 4, 5, 6, 7, 8, 9), list)
    }
    
    fun testHeapSortDescending() {
        val list = mutableListOf(5, 3, 8, 1, 4, 9, 2, 7, 6)
        heapSortDescending(list)
        
        assertEquals(listOf(9, 8, 7, 6, 5, 4, 3, 2, 1), list)
    }
    
    fun testHeapSortEmptyList() {
        val list = mutableListOf<Int>()
        heapSort(list)
        assertTrue(list.isEmpty())
    }
    
    fun testHeapSortSingleElement() {
        val list = mutableListOf(42)
        heapSort(list)
        assertEquals(listOf(42), list)
    }
    
    fun testKSmallest() {
        val elements = listOf(9, 3, 8, 1, 4, 7, 2, 6, 5)
        
        val smallest3 = kSmallest(elements, 3)
        assertEquals(listOf(1, 2, 3), smallest3)
        
        val smallest5 = kSmallest(elements, 5)
        assertEquals(listOf(1, 2, 3, 4, 5), smallest5)
    }
    
    fun testKSmallestKEqualsSize() {
        val elements = listOf(5, 3, 8, 1)
        val result = kSmallest(elements, 4)
        assertEquals(listOf(1, 3, 5, 8), result)
    }
    
    fun testKSmallestKZero() {
        val elements = listOf(5, 3, 8, 1)
        val result = kSmallest(elements, 0)
        assertTrue(result.isEmpty())
    }
    
    fun testKLargest() {
        val elements = listOf(9, 3, 8, 1, 4, 7, 2, 6, 5)
        
        val largest3 = kLargest(elements, 3)
        assertEquals(listOf(9, 8, 7), largest3)
        
        val largest5 = kLargest(elements, 5)
        assertEquals(listOf(9, 8, 7, 6, 5), largest5)
    }
    
    fun testKLargestKEqualsSize() {
        val elements = listOf(5, 3, 8, 1)
        val result = kLargest(elements, 4)
        assertEquals(listOf(8, 5, 3, 1), result)
    }
    
    fun testMergeSortedLists() {
        val lists = listOf(
            listOf(1, 4, 7),
            listOf(2, 5, 8),
            listOf(3, 6, 9)
        )
        
        val merged = mergeSortedLists(lists)
        assertEquals(listOf(1, 2, 3, 4, 5, 6, 7, 8, 9), merged)
    }
    
    fun testMergeSortedListsEmptyLists() {
        val lists = listOf(
            emptyList<Int>(),
            listOf(1, 2, 3),
            emptyList<Int>()
        )
        
        val merged = mergeSortedLists(lists)
        assertEquals(listOf(1, 2, 3), merged)
    }
    
    fun testMergeSortedListsSingleList() {
        val lists = listOf(listOf(1, 2, 3))
        val merged = mergeSortedLists(lists)
        assertEquals(listOf(1, 2, 3), merged)
    }
    
    fun testIsMinHeap() {
        val validMinHeap = arrayOf(1, 3, 2, 5, 4, 9, 7)
        assertTrue(isMinHeap(validMinHeap))
        
        val invalidMinHeap = arrayOf(5, 3, 8, 1, 4)
        assertFalse(isMinHeap(invalidMinHeap))
    }
    
    fun testIsMaxHeap() {
        val validMaxHeap = arrayOf(9, 7, 8, 5, 4, 2, 1)
        assertTrue(isMaxHeap(validMaxHeap))
        
        val invalidMaxHeap = arrayOf(5, 3, 8, 1, 4)
        assertFalse(isMaxHeap(invalidMaxHeap))
    }
    
    fun testIsMinHeapEmpty() {
        val emptyArray = emptyArray<Int>()
        assertTrue(isMinHeap(emptyArray))
    }
    
    fun testIsMaxHeapEmpty() {
        val emptyArray = emptyArray<Int>()
        assertTrue(isMaxHeap(emptyArray))
    }
    
    // =========================================================================
    // Edge Case Test Functions
    // =========================================================================
    
    fun testMinHeapWithNegativeNumbers() {
        val heap = MinHeap<Int>()
        heap.insertAll(listOf(-5, 3, -8, 1, -4, 10))
        
        assertEquals(-8, heap.extract())
        assertEquals(-5, heap.extract())
        assertEquals(-4, heap.extract())
        assertEquals(1, heap.extract())
        assertEquals(3, heap.extract())
        assertEquals(10, heap.extract())
    }
    
    fun testMinHeapWithDuplicateValues() {
        val heap = MinHeap<Int>()
        heap.insertAll(listOf(5, 3, 5, 3, 5))
        
        assertEquals(3, heap.extract())
        assertEquals(3, heap.extract())
        assertEquals(5, heap.extract())
        assertEquals(5, heap.extract())
        assertEquals(5, heap.extract())
    }
    
    fun testMaxHeapWithDuplicateValues() {
        val heap = MaxHeap<Int>()
        heap.insertAll(listOf(5, 5, 3, 3, 8))
        
        assertEquals(8, heap.extract())
        assertEquals(5, heap.extract())
        assertEquals(5, heap.extract())
        assertEquals(3, heap.extract())
        assertEquals(3, heap.extract())
    }
    
    fun testPriorityQueueWithComplexObjects() {
        data class Task(val priority: Int, val name: String)
        
        val pq = PriorityQueue<Task>(16, compareBy { it.priority })
        
        pq.enqueue(Task(5, "low priority"))
        pq.enqueue(Task(1, "high priority"))
        pq.enqueue(Task(3, "medium priority"))
        
        assertEquals(Task(1, "high priority"), pq.dequeue())
        assertEquals(Task(3, "medium priority"), pq.dequeue())
        assertEquals(Task(5, "low priority"), pq.dequeue())
    }
    
    fun testHeapCapacityGrowth() {
        val heap = MinHeap<Int>(2)
        
        for (i in 1..20) {
            heap.insert(i)
        }
        
        assertEquals(20, heap.size())
        
        for (i in 1..20) {
            assertEquals(i, heap.extract())
        }
        
        assertTrue(heap.isEmpty())
    }
    
    fun testHeapLargeDataset() {
        val heap = MinHeap<Int>()
        
        val elements = (1..1000).reversed().toList()
        heap.insertAll(elements)
        
        for (i in 1..1000) {
            assertEquals(i, heap.extract())
        }
        
        assertTrue(heap.isEmpty())
    }
    
    fun testKLargeDataset() {
        val elements = (1000 downTo 1).toList()
        
        val smallest10 = kSmallest(elements, 10)
        assertEquals((1..10).toList(), smallest10)
        
        val largest10 = kLargest(elements, 10)
        assertEquals((1000 downTo 991).toList(), largest10)
    }
    
    fun testMergeLargeSortedLists() {
        val lists = listOf(
            (0..99 step 3).toList(),
            (1..99 step 3).toList(),
            (2..99 step 3).toList()
        )
        
        val merged = mergeSortedLists(lists)
        
        assertEquals((0..99).toList(), merged)
    }
    
    // =========================================================================
    // Stress Test Functions
    // =========================================================================
    
    fun testMinHeapStressTest() {
        val heap = MinHeap<Int>()
        val count = 10000
        
        for (i in count downTo 1) {
            heap.insert(i)
        }
        assertEquals(count, heap.size())
        
        for (i in 1..count) {
            assertEquals(i, heap.extract())
        }
        assertTrue(heap.isEmpty())
    }
    
    fun testMaxHeapStressTest() {
        val heap = MaxHeap<Int>()
        val count = 10000
        
        for (i in 1..count) {
            heap.insert(i)
        }
        assertEquals(count, heap.size())
        
        for (i in count downTo 1) {
            assertEquals(i, heap.extract())
        }
        assertTrue(heap.isEmpty())
    }
    
    fun testHeapSortStressTest() {
        val list = (10000 downTo 1).toMutableList()
        heapSort(list)
        
        for (i in 1..10000) {
            assertEquals(i, list[i - 1])
        }
    }
}

// Helper extension for string multiplication
private operator fun String.times(n: Int): String = this.repeat(n)

/**
 * Main entry point
 */
fun main() {
    HeapUtilsTest.runAllTests()
}
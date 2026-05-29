package priorityqueue

import (
	"fmt"
)

// Example_basicUsage demonstrates basic priority queue operations
func Example_basicUsage() {
	// Create a new min-heap priority queue
	pq := NewPriorityQueue()

	// Enqueue items with priorities
	pq.Enqueue("low priority task", 1.0)
	pq.Enqueue("high priority task", 10.0)
	pq.Enqueue("medium priority task", 5.0)

	fmt.Println("Queue size:", pq.Size())

	// Dequeue items (lowest priority first in min-heap)
	for !pq.IsEmpty() {
		item, _ := pq.Dequeue()
		fmt.Printf("Dequeued: %v (priority: %.1f)\n", item.Value, item.Priority)
	}
	// Output:
	// Queue size: 3
	// Dequeued: low priority task (priority: 1.0)
	// Dequeued: medium priority task (priority: 5.0)
	// Dequeued: high priority task (priority: 10.0)
}

// Example_maxHeap demonstrates max-heap priority queue
func Example_maxHeap() {
	// Create a max-heap priority queue
	pq := NewMaxPriorityQueue()

	// Enqueue items
	pq.Enqueue("task A", 1.0)
	pq.Enqueue("task B", 10.0)
	pq.Enqueue("task C", 5.0)

	// Dequeue items (highest priority first in max-heap)
	for !pq.IsEmpty() {
		item, _ := pq.Dequeue()
		fmt.Printf("Dequeued: %v (priority: %.1f)\n", item.Value, item.Priority)
	}
	// Output:
	// Dequeued: task B (priority: 10.0)
	// Dequeued: task C (priority: 5.0)
	// Dequeued: task A (priority: 1.0)
}

// Example_updatePriority demonstrates updating item priority
func Example_updatePriority() {
	pq := NewPriorityQueue()

	item1 := pq.Enqueue("task 1", 1.0)
	pq.Enqueue("task 2", 2.0)
	pq.Enqueue("task 3", 3.0)

	fmt.Println("Before update:")
	fmt.Println(pq.DebugString())

	// Update priority of item1
	pq.UpdatePriority(item1, 10.0)

	fmt.Println("\nAfter update:")
	fmt.Println(pq.DebugString())
}

// Example_findItems demonstrates finding items in the queue
func Example_findItems() {
	pq := NewPriorityQueue()

	pq.Enqueue("apple", 1.0)
	pq.Enqueue("banana", 2.0)
	pq.Enqueue("cherry", 3.0)
	pq.Enqueue("date", 2.5)

	// Find by value
	item := pq.FindByValue("banana")
	fmt.Printf("Found: %v\n", item.Value)

	// Find by priority range
	items := pq.FindAllByPriorityRange(2.0, 3.0)
	fmt.Printf("Items in range [2.0, 3.0]: %d\n", len(items))

	// Check if value exists
	fmt.Printf("Contains 'cherry': %v\n", pq.Contains("cherry"))
	fmt.Printf("Contains 'grape': %v\n", pq.Contains("grape"))
	// Output:
	// Found: banana
	// Items in range [2.0, 3.0]: 3
	// Contains 'cherry': true
	// Contains 'grape': false
}

// Example_bulkOperations demonstrates batch operations
func Example_bulkOperations() {
	pq := NewPriorityQueue()

	// Batch enqueue
	items := []struct {
		Value    interface{}
		Priority float64
	}{
		{"task A", 3.0},
		{"task B", 1.0},
		{"task C", 2.0},
		{"task D", 5.0},
		{"task E", 4.0},
	}
	pq.EnqueueBatch(items)
	fmt.Printf("Enqueued %d items\n", pq.Size())

	// Dequeue top N items
	top3, _ := pq.DequeueN(3)
	fmt.Println("Top 3 items:")
	for _, item := range top3 {
		fmt.Printf("  %v (priority: %.1f)\n", item.Value, item.Priority)
	}

	// Remaining items
	fmt.Printf("Remaining: %d items\n", pq.Size())
	// Output:
	// Enqueued 5 items
	// Top 3 items:
	//   task B (priority: 1.0)
	//   task C (priority: 2.0)
	//   task A (priority: 3.0)
	// Remaining: 2 items
}

// Example_statistics demonstrates getting queue statistics
func Example_statistics() {
	pq := NewPriorityQueue()

	for i := 1; i <= 5; i++ {
		pq.Enqueue(i, float64(i*10))
	}

	stats := pq.GetStats()
	fmt.Printf("Queue Statistics:\n")
	fmt.Printf("  Size: %d\n", stats.Size)
	fmt.Printf("  Min Priority: %.1f\n", stats.MinPriority)
	fmt.Printf("  Max Priority: %.1f\n", stats.MaxPriority)
	fmt.Printf("  Avg Priority: %.1f\n", stats.AvgPriority)
	fmt.Printf("  Sum Priority: %.1f\n", stats.SumPriority)
	fmt.Printf("  Is Max-Heap: %v\n", stats.IsMaxHeap)
	// Output:
	// Queue Statistics:
	//   Size: 5
	//   Min Priority: 10.0
	//   Max Priority: 50.0
	//   Avg Priority: 30.0
	//   Sum Priority: 150.0
	//   Is Max-Heap: false
}

// Example_mergeQueues demonstrates merging two queues
func Example_mergeQueues() {
	pq1 := NewPriorityQueue()
	pq1.Enqueue("A1", 1.0)
	pq1.Enqueue("A2", 3.0)

	pq2 := NewPriorityQueue()
	pq2.Enqueue("B1", 2.0)
	pq2.Enqueue("B2", 4.0)

	merged := Merge(pq1, pq2)
	fmt.Printf("Merged queue size: %d\n", merged.Size())

	fmt.Println("Items in priority order:")
	for !merged.IsEmpty() {
		item, _ := merged.Dequeue()
		fmt.Printf("  %v (priority: %.1f)\n", item.Value, item.Priority)
	}
	// Output:
	// Merged queue size: 4
	// Items in priority order:
	//   A1 (priority: 1.0)
	//   B1 (priority: 2.0)
	//   A2 (priority: 3.0)
	//   B2 (priority: 4.0)
}

// Example_taskScheduler demonstrates a simple task scheduler
func Example_taskScheduler() {
	type Task struct {
		name     string
		priority float64
	}

	// Create a max-heap for task scheduling (highest priority first)
	scheduler := NewMaxPriorityQueue()

	// Add tasks
	tasks := []Task{
		{"Check email", 1.0},
		{"Fix critical bug", 10.0},
		{"Write documentation", 3.0},
		{"Code review", 5.0},
		{"Update dependencies", 2.0},
	}

	for _, task := range tasks {
		scheduler.Enqueue(task.name, task.priority)
	}

	fmt.Println("Task execution order:")
	for !scheduler.IsEmpty() {
		item, _ := scheduler.Dequeue()
		fmt.Printf("  [%s]\n", item.Value)
	}
	// Output:
	// Task execution order:
	//   [Fix critical bug]
	//   [Code review]
	//   [Write documentation]
	//   [Update dependencies]
	//   [Check email]
}

// Example_typedQueue demonstrates typed priority queues
func Example_typedQueue() {
	// Integer priority queue
	intPQ := NewIntPriorityQueue()
	intPQ.Enqueue(100, 3)
	intPQ.Enqueue(200, 1)
	intPQ.Enqueue(300, 2)

	fmt.Println("Integer queue:")
	for !intPQ.IsEmpty() {
		val, _ := intPQ.Dequeue()
		fmt.Printf("  %d\n", val)
	}

	// String priority queue
	strPQ := NewStringPriorityQueue()
	strPQ.Enqueue("urgent", 3.0)
	strPQ.Enqueue("normal", 2.0)
	strPQ.Enqueue("low", 1.0)

	fmt.Println("\nString queue:")
	for !strPQ.IsEmpty() {
		val, _ := strPQ.Dequeue()
		fmt.Printf("  %s\n", val)
	}
	// Output:
	// Integer queue:
	//   200
	//   300
	//   100
	//
	// String queue:
	//   low
	//   normal
	//   urgent
}

// Example_dijkstra demonstrates using priority queue for Dijkstra's algorithm
func Example_dijkstra() {
	// Graph represented as adjacency list
	graph := map[string]map[string]float64{
		"A": {"B": 1, "C": 4},
		"B": {"A": 1, "C": 2, "D": 5},
		"C": {"A": 4, "B": 2, "D": 1},
		"D": {"B": 5, "C": 1},
	}

	start := "A"
	dist := make(map[string]float64)
	visited := make(map[string]bool)

	// Initialize distances
	for node := range graph {
		dist[node] = float64(1<<63 - 1) // infinity
	}
	dist[start] = 0

	// Use priority queue (min-heap)
	pq := NewPriorityQueue()
	pq.Enqueue(start, 0)

	for !pq.IsEmpty() {
		item, _ := pq.Dequeue()
		node := item.Value.(string)
		distance := item.Priority

		if visited[node] {
			continue
		}
		visited[node] = true

		for neighbor, weight := range graph[node] {
			newDist := distance + weight
			if newDist < dist[neighbor] {
				dist[neighbor] = newDist
				pq.Enqueue(neighbor, newDist)
			}
		}
	}

	fmt.Println("Shortest distances from A:")
	nodes := []string{"A", "B", "C", "D"}
	for _, node := range nodes {
		fmt.Printf("  %s: %.0f\n", node, dist[node])
	}
	// Output:
	// Shortest distances from A:
	//   A: 0
	//   B: 1
	//   C: 3
	//   D: 4
}
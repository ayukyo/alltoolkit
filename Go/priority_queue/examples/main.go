// Example usage of priority_queue package
package main

import (
	"fmt"
	"time"

	pq "github.com/ayukyo/alltoolkit/Go/priority_queue"
)

func main() {
	fmt.Println("=== Priority Queue Examples ===\n")

	// Example 1: Basic MinHeap
	fmt.Println("--- Example 1: Basic MinHeap ---")
	minHeap := pq.MinHeap[string]()
	minHeap.PushItem("Task A", 5)
	minHeap.PushItem("Task B", 1)
	minHeap.PushItem("Task C", 3)
	minHeap.PushItem("Task D", 2)

	fmt.Println("Processing tasks by priority (min-heap: lower number = higher priority):")
	for !minHeap.IsEmpty() {
		val, pri, _ := minHeap.PopItem()
		fmt.Printf("  Priority %d: %s\n", pri, val)
	}
	fmt.Println()

	// Example 2: Basic MaxHeap
	fmt.Println("--- Example 2: Basic MaxHeap ---")
	maxHeap := pq.MaxHeap[string]()
	maxHeap.PushItem("Low priority", 1)
	maxHeap.PushItem("Critical task", 100)
	maxHeap.PushItem("High priority", 75)
	maxHeap.PushItem("Normal task", 50)

	fmt.Println("Processing tasks by priority (max-heap: higher number = higher priority):")
	for !maxHeap.IsEmpty() {
		val, pri, _ := maxHeap.PopItem()
		fmt.Printf("  Priority %d: %s\n", pri, val)
	}
	fmt.Println()

	// Example 3: Using PriorityLevel constants
	fmt.Println("--- Example 3: Using PriorityLevel Constants ---")
	taskQueue := pq.MaxHeap[string]()
	taskQueue.PushItem("Bug fix", int(pq.PriorityHigh))
	taskQueue.PushItem("Feature request", int(pq.PriorityNormal))
	taskQueue.PushItem("Critical outage", int(pq.PriorityCritical))
	taskQueue.PushItem("Documentation", int(pq.PriorityLow))

	fmt.Println("Tasks with named priorities:")
	for !taskQueue.IsEmpty() {
		val, pri, _ := taskQueue.PopItem()
		level := pq.PriorityLevel(pri)
		fmt.Printf("  [%s] %s\n", level.String(), val)
	}
	fmt.Println()

	// Example 4: Peek and Update
	fmt.Println("--- Example 4: Peek and Update ---")
	updateHeap := pq.MinHeap[string]()
	item1 := updateHeap.PushItem("First", 5)
	item2 := updateHeap.PushItem("Second", 3)
	_ = updateHeap.PushItem("Third", 1)

	// Peek at the highest priority item
	val, pri, ok := updateHeap.Peek()
	if ok {
		fmt.Printf("Peek: %s (priority %d)\n", val, pri)
	}

	// Update an item's priority
	fmt.Println("Updating 'First' priority from 5 to 0...")
	updateHeap.Update(item1, "First (urgent)", 0)

	// Peek again
	val, pri, ok = updateHeap.Peek()
	if ok {
		fmt.Printf("After update, peek: %s (priority %d)\n", val, pri)
	}
	fmt.Println()

	// Example 5: Find and Contains
	fmt.Println("--- Example 5: Find and Contains ---")
	findHeap := pq.MinHeap[int]()
	findHeap.PushItem(10, 1)
	findHeap.PushItem(20, 2)
	findHeap.PushItem(30, 3)

	// Check if value exists
	contains := findHeap.Contains(func(a, b int) bool { return a == b }, 20)
	fmt.Printf("Contains 20: %v\n", contains)

	contains = findHeap.Contains(func(a, b int) bool { return a == b }, 99)
	fmt.Printf("Contains 99: %v\n", contains)

	// Find by predicate
	item, found := findHeap.Find(func(n int) bool { return n > 15 })
	if found {
		fmt.Printf("Found item with value > 15: %d (priority %d)\n", item.Value, item.Priority)
	}
	fmt.Println()

	// Example 6: Thread-Safe Priority Queue
	fmt.Println("--- Example 6: Thread-Safe Priority Queue ---")
	threadSafe := pq.NewThreadSafeMaxHeap[int]()

	// Simulate concurrent access
	done := make(chan bool)
	go func() {
		for i := 0; i < 5; i++ {
			threadSafe.PushItem(i, i*10)
		}
		done <- true
	}()
	go func() {
		for i := 0; i < 3; i++ {
			time.Sleep(10 * time.Millisecond)
			if val, pri, ok := threadSafe.PopItem(); ok {
				fmt.Printf("  Popped: %d (priority %d)\n", val, pri)
			}
		}
		done <- true
	}()

	<-done
	<-done
	fmt.Printf("Remaining items: %d\n\n", threadSafe.Size())

	// Example 7: Bounded Priority Queue
	fmt.Println("--- Example 7: Bounded Priority Queue ---")
	bounded := pq.NewBoundedMaxHeap[string](3)
	bounded.SetEvictCallback(func(val string, pri int) {
		fmt.Printf("  Evicted: %s (priority %d)\n", val, pri)
	})

	fmt.Println("Adding items to bounded queue (max 3):")
	bounded.PushItem("Item A", 10)
	bounded.PushItem("Item B", 30)
	bounded.PushItem("Item C", 20)
	fmt.Printf("Queue size: %d\n", bounded.Size())

	fmt.Println("Adding higher priority item (should evict lowest):")
	bounded.PushItem("Item D", 40)
	fmt.Printf("Queue size: %d\n\n", bounded.Size())

	// Example 8: Custom Struct with Priority Queue
	fmt.Println("--- Example 8: Custom Struct ---")
	type Job struct {
		ID     int
		Name   string
		Status string
	}

	jobQueue := pq.MinHeap[Job]()
	jobQueue.PushItem(Job{ID: 1, Name: "Deploy", Status: "pending"}, 1)
	jobQueue.PushItem(Job{ID: 2, Name: "Test", Status: "pending"}, 3)
	jobQueue.PushItem(Job{ID: 3, Name: "Build", Status: "pending"}, 2)

	fmt.Println("Processing jobs:")
	for !jobQueue.IsEmpty() {
		job, pri, _ := jobQueue.PopItem()
		fmt.Printf("  Priority %d: Job #%d - %s (%s)\n", pri, job.ID, job.Name, job.Status)
	}
	fmt.Println()

	// Example 9: Clone a Priority Queue
	fmt.Println("--- Example 9: Clone a Priority Queue ---")
	original := pq.MinHeap[int]()
	original.PushItem(1, 5)
	original.PushItem(2, 3)
	original.PushItem(3, 1)

	cloned := original.Clone()

	fmt.Println("Original queue:")
	for !original.IsEmpty() {
		val, pri, _ := original.PopItem()
		fmt.Printf("  Value %d (priority %d)\n", val, pri)
	}

	fmt.Println("Cloned queue (still has all items):")
	for !cloned.IsEmpty() {
		val, pri, _ := cloned.PopItem()
		fmt.Printf("  Value %d (priority %d)\n", val, pri)
	}
	fmt.Println()

	// Example 10: Batch Operations
	fmt.Println("--- Example 10: Batch Operations ---")
	batchHeap := pq.MinHeap[int]()
	for i := 1; i <= 10; i++ {
		batchHeap.PushItem(i*10, i)
	}

	fmt.Printf("Total items: %d\n", batchHeap.Size())

	// Get all values
	values := batchHeap.Values()
	fmt.Printf("All values: %v\n", values)

	// Find items by priority
	items := batchHeap.FindByPriority(5)
	fmt.Printf("Items with priority 5: %d items\n", len(items))

	// Pop all items
	fmt.Println("Popping all items:")
	for !batchHeap.IsEmpty() {
		val, pri, _ := batchHeap.PopItem()
		fmt.Printf("  %d ", val)
		if pri%2 == 0 {
			batchHeap.PushItem(val*100, pri)
		}
	}
	fmt.Println("\n")

	fmt.Println("=== All Examples Complete ===")
}
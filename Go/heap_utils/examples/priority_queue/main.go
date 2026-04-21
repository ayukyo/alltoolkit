// Example: Priority Queue for task scheduling
package main

import (
	"fmt"
	heap_utils "github.com/ayukyo/alltoolkit/Go/heap_utils"
)

type Task struct {
	ID       int
	Name     string
	Priority float64
}

func main() {
	fmt.Println("=== Priority Queue: Higher Priority First ===")
	
	// Create a priority queue where higher priority values come out first
	pq := heap_utils.NewPriorityQueue[Task](true)
	
	// Add tasks with different priorities
	pq.Push(Task{ID: 1, Name: "Low priority task"}, 1)
	pq.Push(Task{ID: 2, Name: "Critical task"}, 100)
	pq.Push(Task{ID: 3, Name: "Medium task"}, 50)
	pq.Push(Task{ID: 4, Name: "Urgent task"}, 75)
	
	fmt.Println("Processing tasks by priority:")
	for !pq.IsEmpty() {
		item := pq.Pop()
		fmt.Printf("  [Priority %.0f] Task %d: %s\n", 
			item.Priority, item.Value.ID, item.Value.Name)
	}
	
	fmt.Println("\n=== Priority Queue: Lower Priority First ===")
	
	// Create a priority queue where lower priority values come out first
	pqLow := heap_utils.NewPriorityQueue[Task](false)
	
	pqLow.Push(Task{ID: 1, Name: "Task A"}, 3)
	pqLow.Push(Task{ID: 2, Name: "Task B"}, 1)
	pqLow.Push(Task{ID: 3, Name: "Task C"}, 2)
	
	fmt.Println("Processing tasks (lowest priority first):")
	for !pqLow.IsEmpty() {
		item := pqLow.Pop()
		fmt.Printf("  [Priority %.0f] Task %d: %s\n",
			item.Priority, item.Value.ID, item.Value.Name)
	}
	
	fmt.Println("\n=== Dynamic Priority Update ===")
	
	pqUpdate := heap_utils.NewPriorityQueue[string](true)
	
	task1 := pqUpdate.Push("Download file", 10)
	task2 := pqUpdate.Push("Send email", 5)
	task3 := pqUpdate.Push("Process data", 8)
	
	fmt.Println("Initial order:")
	for i := 0; i < 3; i++ {
		item := pqUpdate.Peek()
		fmt.Printf("  [%.0f] %s\n", item.Priority, item.Value)
		pqUpdate.Pop()
	}
	
	// Re-add and update priority
	pqUpdate.Push("Download file", 10)
	task2 = pqUpdate.Push("Send email", 5)
	pqUpdate.Push("Process data", 8)
	
	// Boost "Send email" to highest priority
	pqUpdate.Update(task2, 100)
	
	fmt.Println("\nAfter boosting 'Send email' priority:")
	for !pqUpdate.IsEmpty() {
		item := pqUpdate.Pop()
		fmt.Printf("  [%.0f] %s\n", item.Priority, item.Value)
	}
}
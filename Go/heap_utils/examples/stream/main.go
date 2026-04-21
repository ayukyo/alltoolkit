// Example: Real-time data stream processing with heaps
package main

import (
	"fmt"
	heap_utils "github.com/ayukyo/alltoolkit/Go/heap_utils"
)

type SensorReading struct {
	SensorID string
	Value    float64
	Timestamp int
}

func main() {
	fmt.Println("=== Real-time Median Tracking ===")
	
	// Simulating a data stream and tracking median
	stream := []float64{5, 15, 1, 3, 8, 20, 12, 25, 7, 18}
	
	// Use two heaps to track median in real-time
	lowHeap := heap_utils.NewMaxHeap[float64]()  // lower half
	highHeap := heap_utils.NewMinHeap[float64]() // upper half
	
	fmt.Println("Processing stream and tracking median:")
	for i, val := range stream {
		// Add to appropriate heap
		if lowHeap.Len() == 0 {
			lowHeap.Push(val)
		} else {
			top, _ := lowHeap.Peek()
			if val <= top {
				lowHeap.Push(val)
			} else {
				highHeap.Push(val)
			}
		}
		
		// Balance heaps
		for lowHeap.Len() > highHeap.Len()+1 {
			highHeap.Push(lowHeap.Pop())
		}
		for highHeap.Len() > lowHeap.Len() {
			lowHeap.Push(highHeap.Pop())
		}
		
		// Get median
		var median float64
		if (i+1)%2 == 1 {
			median, _ = lowHeap.Peek()
		} else {
			l, _ := lowHeap.Peek()
			h, _ := highHeap.Peek()
			median = (l + h) / 2
		}
		
		fmt.Printf("  After %5.1f: median = %.2f (low=%d, high=%d)\n",
			val, median, lowHeap.Len(), highHeap.Len())
	}
	
	fmt.Println("\n=== Top-K Frequent Items in Stream ===")
	
	// Track most frequent words in a stream
	wordCounts := make(map[string]int)
	words := []string{"apple", "banana", "apple", "cherry", "banana",
		"apple", "date", "banana", "apple", "elderberry",
		"cherry", "fig", "apple", "banana"}
	
	for _, word := range words {
		wordCounts[word]++
	}
	
	// Use heap to find top 3 most frequent
	type wordCount struct {
		word  string
		count int
	}
	
	topHeap := heap_utils.NewGenericHeap(func(a, b wordCount) bool {
		return a.count < b.count // min-heap, keep smallest count at root
	})
	
	k := 3
	for word, count := range wordCounts {
		wc := wordCount{word, count}
		if topHeap.Len() < k {
			topHeap.Push(wc)
		} else {
			top, _ := topHeap.Peek()
			if count > top.count {
				topHeap.Pop()
				topHeap.Push(wc)
			}
		}
	}
	
	fmt.Printf("Top %d most frequent words:\n", k)
	result := make([]wordCount, k)
	for i := k - 1; i >= 0; i-- {
		result[i] = topHeap.Pop()
	}
	for i, wc := range result {
		fmt.Printf("  %d. %s: %d occurrences\n", i+1, wc.word, wc.count)
	}
	
	fmt.Println("\n=== Sliding Window Maximum ===")
	
	// Find maximum in sliding window of size 3
	data := []int{1, 3, -1, -3, 5, 3, 6, 7}
	windowSize := 3
	
	fmt.Printf("Data: %v\n", data)
	fmt.Printf("Sliding window maximum (window=%d):\n", windowSize)
	
	for i := 0; i <= len(data)-windowSize; i++ {
		window := data[i : i+windowSize]
		maxHeap := heap_utils.NewMaxHeap(window...)
		maxVal, _ := maxHeap.Peek()
		fmt.Printf("  Window %v -> max = %d\n", window, maxVal)
	}
	
	fmt.Println("\n=== Priority-based Task Scheduling ===")
	
	// Simulate real-time task scheduler
	pq := heap_utils.NewPriorityQueue[SensorReading](true)
	
	// Tasks arrive with different priorities
	readings := []SensorReading{
		{"temp-01", 23.5, 1},
		{"alarm-01", 99.9, 2},
		{"temp-02", 24.1, 3},
		{"pressure-01", 101.3, 4},
		{"alarm-02", 100.0, 5},
	}
	
	// Assign priority based on sensor type (alarms get higher priority)
	for _, r := range readings {
		priority := 1.0
		if r.SensorID[:5] == "alarm" {
			priority = 10.0
		} else if r.SensorID[:4] == "temp" {
			priority = 3.0
		}
		pq.Push(r, priority)
	}
	
	fmt.Println("Processing sensor readings by priority:")
	for !pq.IsEmpty() {
		item := pq.Pop()
		r := item.Value
		fmt.Printf("  [%s] %s: %.1f (priority=%.0f)\n",
			r.SensorID[:5], r.SensorID, r.Value, item.Priority)
	}
}
// Example application demonstrating interval tree usage
package main

import (
	"fmt"
	intervaltree "github.com/ayukyo/alltoolkit/Go/interval_tree_utils"
)

func main() {
	fmt.Println("=== Interval Tree Utils Demo ===")
	fmt.Println()
	
	// Example 1: Meeting Room Scheduler
	fmt.Println("--- Example 1: Meeting Room Scheduler ---")
	meetingRoomDemo()
	fmt.Println()
	
	// Example 2: Memory Allocator Simulation
	fmt.Println("--- Example 2: Memory Allocator Simulation ---")
	memoryAllocatorDemo()
	fmt.Println()
	
	// Example 3: Time Slot Finder
	fmt.Println("--- Example 3: Time Slot Finder ---")
	timeSlotDemo()
	fmt.Println()
	
	// Example 4: Overlapping Events Detector
	fmt.Println("--- Example 4: Overlapping Events Detector ---")
	overlappingEventsDemo()
}

func meetingRoomDemo() {
	tree := intervaltree.NewIntervalTree()
	
	// Book meeting rooms (time in hours, e.g., 9.5 = 9:30 AM)
	meetings := []struct {
		start, end float64
		title      string
	}{
		{9, 10, "Team Standup"},
		{10.5, 12, "Product Review"},
		{13, 14, "Lunch & Learn"},
		{14, 16, "Client Demo"},
		{15, 17, "Interview"},
	}
	
	for _, m := range meetings {
		tree.Insert(intervaltree.NewInterval(
			int(m.start*100), // Convert to int for storage
			int(m.end*100),
			m.title,
		))
	}
	
	// Check availability at different times
	times := []float64{9.5, 10, 11, 13.5, 15.5}
	
	fmt.Println("Checking meeting room availability:")
	for _, t := range times {
		point := int(t * 100)
		results := tree.QueryPoint(point)
		if len(results) == 0 {
			fmt.Printf("  %.2f: Room is available ✓\n", t)
		} else {
			for _, iv := range results {
				fmt.Printf("  %.2f: Booked - %s\n", t, iv.Data)
			}
		}
	}
	
	// Find all meetings in a time window
	fmt.Println("\nMeetings between 10:00 and 16:00:")
	query := intervaltree.NewInterval(1000, 1600, nil)
	overlaps := tree.QueryOverlaps(query)
	for _, iv := range overlaps {
		fmt.Printf("  [%.1f - %.1f]: %s\n", 
			float64(iv.Start)/100, 
			float64(iv.End)/100, 
			iv.Data)
	}
}

func memoryAllocatorDemo() {
	tree := intervaltree.NewIntervalTree()
	
	// Simulate allocated memory blocks
	allocations := []struct {
		start, end int
		name       string
	}{
		{0, 100, "Block A"},
		{200, 350, "Block B"},
		{400, 600, "Block C"},
		{700, 850, "Block D"},
	}
	
	for _, a := range allocations {
		tree.Insert(intervaltree.NewInterval(a.start, a.end, a.name))
	}
	
	// Check if specific memory addresses are allocated
	addresses := []int{50, 150, 250, 500, 650}
	
	fmt.Println("Memory allocation status:")
	for _, addr := range addresses {
		results := tree.QueryPoint(addr)
		if len(results) == 0 {
			fmt.Printf("  Address %d: Free\n", addr)
		} else {
			fmt.Printf("  Address %d: Allocated in %s\n", addr, results[0].Data)
		}
	}
	
	// Find free blocks
	fmt.Println("\nFree memory blocks in range [0-1000]:")
	gaps := tree.FindGaps(0, 1000)
	for i, gap := range gaps {
		fmt.Printf("  Gap %d: [%d, %d) - %d bytes\n", i+1, gap.Start, gap.End, gap.Length())
	}
	
	// Check if a new allocation would conflict
	newBlock := intervaltree.NewInterval(300, 450, "New Block")
	if tree.HasOverlap(newBlock) {
		fmt.Println("\nCannot allocate [300, 450): overlaps with existing block")
	}
	
	newBlock2 := intervaltree.NewInterval(600, 700, "New Block")
	if !tree.HasOverlap(newBlock2) {
		fmt.Println("\nCan allocate [600, 700): no conflicts")
	}
}

func timeSlotDemo() {
	tree := intervaltree.NewIntervalTree()
	
	// Busy time slots (in minutes from midnight)
	busySlots := []struct {
		start, end int
		activity   string
	}{
		{540, 600, "Morning Exercise"},  // 9:00 - 10:00
		{720, 780, "Team Meeting"},       // 12:00 - 13:00
		{900, 960, "Client Call"},        // 15:00 - 16:00
		{1020, 1080, "Training"},         // 17:00 - 18:00
	}
	
	for _, s := range busySlots {
		tree.Insert(intervaltree.NewInterval(s.start, s.end, s.activity))
	}
	
	// Find available 1-hour slots between 8:00 and 18:00
	fmt.Println("Available 1-hour slots (8:00 - 18:00):")
	
	// Get gaps in the working hours
	gaps := tree.FindGaps(480, 1080) // 8:00 - 18:00
	
	for _, gap := range gaps {
		// Find 1-hour slots within each gap
		for start := gap.Start; start+60 <= gap.End; start += 30 {
			fmt.Printf("  %02d:%02d - %02d:%02d\n", 
				start/60, start%60, 
				(start+60)/60, (start+60)%60)
		}
	}
}

func overlappingEventsDemo() {
	// Detect overlapping events in a schedule
	events := []intervaltree.Interval{
		intervaltree.NewInterval(1, 5, "Event A"),
		intervaltree.NewInterval(3, 7, "Event B"),
		intervaltree.NewInterval(6, 10, "Event C"),
		intervaltree.NewInterval(8, 12, "Event D"),
		intervaltree.NewInterval(15, 20, "Event E"),
	}
	
	fmt.Println("Checking for overlapping events:")
	
	// Method 1: Using interval tree
	tree := intervaltree.NewIntervalTree()
	for _, e := range events {
		overlaps := tree.QueryOverlaps(e)
		if len(overlaps) > 0 {
			fmt.Printf("  %s overlaps with: ", e.Data)
			for _, o := range overlaps {
				fmt.Printf("%s ", o.Data)
			}
			fmt.Println()
		}
		tree.Insert(e)
	}
	
	// Method 2: Merge overlapping intervals
	fmt.Println("\nMerged intervals (union of overlapping):")
	merged := intervaltree.MergeOverlapping(events)
	for _, m := range merged {
		fmt.Printf("  [%d, %d) - length: %d\n", m.Start, m.End, m.Length())
	}
	
	// Calculate total coverage
	coverage := intervaltree.Coverage(events)
	fmt.Printf("\nTotal coverage: %d time units\n", coverage)
	
	// Intersection example
	a := intervaltree.NewInterval(1, 5, nil)
	b := intervaltree.NewInterval(3, 7, nil)
	intersection, ok := intervaltree.Intersection(a, b)
	if ok {
		fmt.Printf("\nIntersection of [1,5) and [3,7): [%d, %d)\n", 
			intersection.Start, intersection.End)
	}
	
	// Union example
	union, ok := intervaltree.Union(a, b)
	if ok {
		fmt.Printf("Union of [1,5) and [3,7): [%d, %d)\n", union.Start, union.End)
	}
}
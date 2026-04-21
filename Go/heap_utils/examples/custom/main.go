// Example: GenericHeap with custom comparator
package main

import (
	"fmt"
	heap_utils "github.com/ayukyo/alltoolkit/Go/heap_utils"
)

type Employee struct {
	Name   string
	Salary int
	Level  int
}

func main() {
	fmt.Println("=== Custom Heap: Sort by Salary ===")
	
	employees := []Employee{
		{"Alice", 50000, 3},
		{"Bob", 75000, 4},
		{"Charlie", 60000, 3},
		{"Diana", 90000, 5},
		{"Eve", 45000, 2},
	}
	
	// Create heap ordered by salary (ascending)
	salaryHeap := heap_utils.NewGenericHeap(
		func(a, b Employee) bool { return a.Salary < b.Salary },
		employees...,
	)
	
	fmt.Println("Employees by salary (ascending):")
	for !salaryHeap.IsEmpty() {
		e := salaryHeap.Pop()
		fmt.Printf("  %s: $%d (Level %d)\n", e.Name, e.Salary, e.Level)
	}
	
	fmt.Println("\n=== Custom Heap: Sort by Level then Name ===")
	
	// Create heap ordered by level (primary) then name (secondary)
	levelHeap := heap_utils.NewGenericHeap(
		func(a, b Employee) bool {
			if a.Level != b.Level {
				return a.Level < b.Level
			}
			return a.Name < b.Name
		},
		employees...,
	)
	
	fmt.Println("Employees by level then name:")
	for !levelHeap.IsEmpty() {
		e := levelHeap.Pop()
		fmt.Printf("  Level %d: %s ($%d)\n", e.Level, e.Name, e.Salary)
	}
	
	fmt.Println("\n=== Custom Heap: Max-Heap by Salary ===")
	
	// Max-heap by salary (highest first)
	maxSalaryHeap := heap_utils.NewGenericHeap(
		func(a, b Employee) bool { return a.Salary > b.Salary },
		employees...,
	)
	
	fmt.Println("Top earners:")
	count := 0
	for !maxSalaryHeap.IsEmpty() && count < 3 {
		e := maxSalaryHeap.Pop()
		fmt.Printf("  %s: $%d\n", e.Name, e.Salary)
		count++
	}
	
	fmt.Println("\n=== Dynamic Comparator Example ===")
	
	// Heap that keeps track of smallest absolute value
	numbers := []int{-5, 3, -2, 8, -1, 4}
	
	absHeap := heap_utils.NewGenericHeap(
		func(a, b int) bool {
			absA := a
			if a < 0 {
				absA = -a
			}
			absB := b
			if b < 0 {
				absB = -b
			}
			return absA < absB
		},
		numbers...,
	)
	
	fmt.Printf("Numbers: %v\n", numbers)
	fmt.Print("Sorted by absolute value: ")
	for !absHeap.IsEmpty() {
		fmt.Printf("%d ", absHeap.Pop())
	}
	fmt.Println()
}
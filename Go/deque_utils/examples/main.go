package main

import (
	"fmt"
	deque "deque_utils"
)

func main() {
	fmt.Println("=== Deque Utils Examples ===")
	fmt.Println()
	
	// Example 1: Basic Operations
	fmt.Println("1. Basic Operations")
	d := deque.NewDeque[int]()
	d.PushBack(1)
	d.PushBack(2)
	d.PushBack(3)
	d.PushFront(0)
	fmt.Printf("   Deque: %s\n", d.String())
	fmt.Printf("   Length: %d\n", d.Len())
	
	front, _ := d.PopFront()
	fmt.Printf("   PopFront: %d\n", front)
	
	back, _ := d.PopBack()
	fmt.Printf("   PopBack: %d\n", back)
	
	fmt.Printf("   After pops: %s\n", d.String())
	fmt.Println()
	
	// Example 2: From Slice
	fmt.Println("2. From Slice")
	slice := []int{10, 20, 30, 40, 50}
	d2 := deque.NewDequeFromSlice(slice)
	fmt.Printf("   Deque from slice: %s\n", d2.String())
	fmt.Println()
	
	// Example 3: Search Operations
	fmt.Println("3. Search Operations")
	d3 := deque.NewDequeFromSlice([]int{1, 2, 3, 4, 5, 6, 7, 8, 9, 10})
	
	// Find
	val, err := d3.Find(func(x int) bool { return x > 5 })
	if err == nil {
		fmt.Printf("   Find first > 5: %d\n", val)
	}
	
	// FindAll
	evens := d3.FindAll(func(x int) bool { return x%2 == 0 })
	fmt.Printf("   All even numbers: %v\n", evens)
	
	// Count
	count := d3.Count(func(x int) bool { return x%2 == 0 })
	fmt.Printf("   Count of evens: %d\n", count)
	
	// Contains
	equals := func(a, b int) bool { return a == b }
	fmt.Printf("   Contains 5: %v\n", d3.Contains(5, equals))
	fmt.Printf("   Contains 100: %v\n", d3.Contains(100, equals))
	fmt.Println()
	
	// Example 4: Transformation
	fmt.Println("4. Transformation")
	d4 := deque.NewDequeFromSlice([]int{1, 2, 3, 4, 5})
	
	// Map
	doubled := deque.Map(d4, func(x int) int { return x * 2 })
	fmt.Printf("   Original: %s\n", d4.String())
	fmt.Printf("   Mapped (x*2): %s\n", doubled.String())
	
	// Filter
	evensDeque := d4.Filter(func(x int) bool { return x%2 == 0 })
	fmt.Printf("   Filtered (evens): %s\n", evensDeque.String())
	
	// Reduce
	sum := deque.Reduce(d4, 0, func(acc, x int) int { return acc + x })
	product := deque.Reduce(d4, 1, func(acc, x int) int { return acc * x })
	fmt.Printf("   Reduce (sum): %d\n", sum)
	fmt.Printf("   Reduce (product): %d\n", product)
	fmt.Println()
	
	// Example 5: Reverse and Rotate
	fmt.Println("5. Reverse and Rotate")
	d5 := deque.NewDequeFromSlice([]int{1, 2, 3, 4, 5})
	fmt.Printf("   Original: %s\n", d5.String())
	
	d5.Reverse()
	fmt.Printf("   Reversed: %s\n", d5.String())
	
	d5.Reverse() // Back to original
	d5.RotateLeft(2)
	fmt.Printf("   RotateLeft(2): %s\n", d5.String())
	
	d5.RotateRight(3)
	fmt.Printf("   RotateRight(3): %s\n", d5.String())
	fmt.Println()
	
	// Example 6: Min/Max
	fmt.Println("6. Min/Max")
	d6 := deque.NewDequeFromSlice([]int{5, 3, 9, 1, 7, 2, 8})
	less := func(a, b int) bool { return a < b }
	
	min, _ := d6.Min(less)
	max, _ := d6.Max(less)
	fmt.Printf("   Deque: %s\n", d6.String())
	fmt.Printf("   Min: %d\n", min)
	fmt.Printf("   Max: %d\n", max)
	fmt.Println()
	
	// Example 7: Bulk Operations
	fmt.Println("7. Bulk Operations")
	d7 := deque.NewDeque[int]()
	d7.PushBackAll([]int{1, 2, 3})
	fmt.Printf("   After PushBackAll: %s\n", d7.String())
	
	d7.PushFrontAll([]int{-1, 0})
	fmt.Printf("   After PushFrontAll: %s\n", d7.String())
	
	items, _ := d7.PopFrontN(2)
	fmt.Printf("   PopFrontN(2): %v\n", items)
	fmt.Printf("   Remaining: %s\n", d7.String())
	fmt.Println()
	
	// Example 8: Slice Operations
	fmt.Println("8. Slice Operations")
	d8 := deque.NewDequeFromSlice([]int{1, 2, 3, 4, 5, 6, 7, 8, 9, 10})
	
	slice := d8.ToSlice()
	fmt.Printf("   ToSlice: %v\n", slice)
	
	sub, _ := d8.SubDeque(2, 5)
	fmt.Printf("   SubDeque(2,5): %s\n", sub.String())
	
	take := d8.Take(3)
	fmt.Printf("   Take(3): %s\n", take.String())
	
	takeLast := d8.TakeLast(3)
	fmt.Printf("   TakeLast(3): %s\n", takeLast.String())
	
	skip := d8.Skip(3)
	fmt.Printf("   Skip(3): %s\n", skip.String())
	fmt.Println()
	
	// Example 9: String Deque
	fmt.Println("9. String Deque")
	d9 := deque.NewDeque[string]()
	d9.PushBack("Hello")
	d9.PushBack("World")
	d9.PushFront("Greeting:")
	
	fmt.Printf("   String deque: %s\n", d9.String())
	fmt.Println()
	
	// Example 10: Custom Type
	fmt.Println("10. Custom Type (Person)")
	type Person struct {
		Name string
		Age  int
	}
	
	d10 := deque.NewDeque[Person]()
	d10.PushBack(Person{"Alice", 30})
	d10.PushBack(Person{"Bob", 25})
	d10.PushBack(Person{"Charlie", 35})
	
	fmt.Printf("   Deque with Persons: %s\n", d10.String())
	
	// Find by predicate
	person, _ := d10.Find(func(p Person) bool { return p.Age == 25 })
	fmt.Printf("   Find Age=25: {%s, %d}\n", person.Name, person.Age)
	
	// Filter
	older := d10.Filter(func(p Person) bool { return p.Age > 28 })
	fmt.Printf("   Filter Age>28: %s\n", older.String())
	fmt.Println()
	
	// Example 11: Default Values
	fmt.Println("11. Default Values")
	emptyDeque := deque.NewDeque[int]()
	
	fmt.Printf("   Empty deque PopFrontOrDefault(100): %d\n", emptyDeque.PopFrontOrDefault(100))
	fmt.Printf("   Empty deque FrontOrDefault(999): %d\n", emptyDeque.FrontOrDefault(999))
	fmt.Println()
	
	// Example 12: Iterator
	fmt.Println("12. Iterator")
	d12 := deque.NewDequeFromSlice([]int{1, 2, 3, 4, 5})
	
	fmt.Print("   Iterator: ")
	for val := range d12.Iterator() {
		fmt.Printf("%d ", val)
	}
	fmt.Println()
	
	fmt.Print("   ReverseIterator: ")
	for val := range d12.ReverseIterator() {
		fmt.Printf("%d ", val)
	}
	fmt.Println()
	fmt.Println()
	
	// Example 13: Utility Functions
	fmt.Println("13. Utility Functions")
	d13 := deque.NewDequeFromSlice([]int{1, 2, 3})
	d14 := deque.NewDequeFromSlice([]int{4, 5, 6})
	
	d13.Append(d14)
	fmt.Printf("   Append: %s\n", d13.String())
	
	d15 := deque.NewDequeFromSlice([]int{7, 8, 9})
	d16 := deque.NewDequeFromSlice([]int{1, 2, 3})
	d15.Prepend(d16)
	fmt.Printf("   Prepend: %s\n", d15.String())
	
	clone := d15.Clone()
	fmt.Printf("   Clone: %s\n", clone.String())
	
	// Swap
	d15.Swap(0, 5)
	fmt.Printf("   After Swap(0,5): %s\n", d15.String())
	fmt.Println()
	
	// Example 14: All/Any
	fmt.Println("14. All/Any")
	d14a := deque.NewDequeFromSlice([]int{2, 4, 6, 8, 10})
	
	allEven := d14a.All(func(x int) bool { return x%2 == 0 })
	fmt.Printf("   All even? %v\n", allEven)
	
	d14a.PushBack(11)
	allEven = d14a.All(func(x int) bool { return x%2 == 0 })
	fmt.Printf("   All even after adding 11? %v\n", allEven)
	
	anyOdd := d14a.Any(func(x int) bool { return x%2 != 0 })
	fmt.Printf("   Any odd? %v\n", anyOdd)
	fmt.Println()
	
	// Example 15: First/Last
	fmt.Println("15. First/Last (by predicate)")
	d15a := deque.NewDequeFromSlice([]int{1, 2, 3, 4, 5, 6})
	
	first, _ := d15a.First(func(x int) bool { return x > 2 })
	fmt.Printf("   First > 2: %d\n", first)
	
	last, _ := d15a.Last(func(x int) bool { return x < 5 })
	fmt.Printf("   Last < 5: %d\n", last)
}
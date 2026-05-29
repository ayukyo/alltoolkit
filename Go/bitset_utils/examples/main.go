// Example usage of bitset_utils package
package main

import (
	"fmt"
	"bitset_utils"
)

func main() {
	fmt.Println("=== BitSet Utils Examples ===")
	fmt.Println()

	// Example 1: Creating and basic operations
	fmt.Println("1. Creating and Basic Operations")
	fmt.Println("--------------------------------")
	bs := bitset_utils.NewBitSet(64)
	fmt.Printf("Created BitSet with capacity %d\n", bs.Cap())

	bs.Set(0)
	bs.Set(5)
	bs.Set(10)
	bs.Set(63)
	fmt.Printf("Set bits 0, 5, 10, 63: %s\n", bs.String())
	fmt.Printf("Count of set bits: %d\n", bs.Count())
	fmt.Printf("Is bit 5 set? %v\n", bs.Test(5))
	fmt.Printf("Is bit 7 set? %v\n", bs.Test(7))
	fmt.Println()

	// Example 2: Set operations
	fmt.Println("2. Set Operations")
	fmt.Println("-----------------")
	bs1, _ := bitset_utils.NewBitSetFromString("1100")
	bs2, _ := bitset_utils.NewBitSetFromString("1010")
	fmt.Printf("bs1: %s\n", bs1.String())
	fmt.Printf("bs2: %s\n", bs2.String())
	fmt.Printf("bs1 AND bs2: %s\n", bs1.And(bs2).String())
	fmt.Printf("bs1 OR bs2: %s\n", bs1.Or(bs2).String())
	fmt.Printf("bs1 XOR bs2: %s\n", bs1.Xor(bs2).String())
	fmt.Printf("bs1 - bs2: %s\n", bs1.AndNot(bs2).String())
	fmt.Printf("NOT bs1: %s\n", bs1.Not().String())
	fmt.Println()

	// Example 3: Finding bits
	fmt.Println("3. Finding Set and Clear Bits")
	fmt.Println("-----------------------------")
	bs3 := bitset_utils.NewBitSet(100)
	bs3.Set(10)
	bs3.Set(25)
	bs3.Set(50)
	bs3.Set(75)

	fmt.Printf("Set bits in bs3: %v\n", bs3.SetBits())
	fmt.Printf("First set bit: %d\n", bs3.FirstSet())
	fmt.Printf("Last set bit: %d\n", bs3.LastSet())
	fmt.Printf("Next set bit after 10: %d\n", bs3.NextSet(11))
	fmt.Printf("Next set bit after 50: %d\n", bs3.NextSet(51))
	fmt.Println()

	// Example 4: Range operations
	fmt.Println("4. Range Operations")
	fmt.Println("-------------------")
	bs4 := bitset_utils.NewBitSet(32)
	bs4.SetRange(5, 15)
	fmt.Printf("Set range [5, 15): %s\n", bs4.String())
	fmt.Printf("Count after SetRange: %d\n", bs4.Count())

	bs4.ClearRange(8, 12)
	fmt.Printf("Clear range [8, 12): %s\n", bs4.String())
	fmt.Printf("Count after ClearRange: %d\n", bs4.Count())
	fmt.Println()

	// Example 5: Shift operations
	fmt.Println("5. Shift Operations")
	fmt.Println("-------------------")
	bs5, _ := bitset_utils.NewBitSetFromString("1011")
	fmt.Printf("Original: %s\n", bs5.String())

	bs5.ShiftLeft(2)
	fmt.Printf("Shift left by 2: %s\n", bs5.String())

	bs5.ShiftRight(1)
	fmt.Printf("Shift right by 1: %s\n", bs5.String())
	fmt.Println()

	// Example 6: Conversion
	fmt.Println("6. Conversion Operations")
	fmt.Println("------------------------")
	bs6, _ := bitset_utils.NewBitSetFromString("110101")
	fmt.Printf("BitSet: %s\n", bs6.String())
	fmt.Printf("To bytes: %v\n", bs6.ToBytes())
	fmt.Printf("To uint64 slice: %v\n", bs6.ToUint64Slice())
	fmt.Printf("Set positions: %v\n", bs6.SetBits())
	fmt.Println()

	// Example 7: Set properties
	fmt.Println("7. Set Properties")
	fmt.Println("-----------------")
	bs7, _ := bitset_utils.NewBitSetFromString("1110")
	bs8, _ := bitset_utils.NewBitSetFromString("1100")
	bs9, _ := bitset_utils.NewBitSetFromString("0011")

	fmt.Printf("bs7: %s\n", bs7.String())
	fmt.Printf("bs8: %s\n", bs8.String())
	fmt.Printf("bs9: %s\n", bs9.String())
	fmt.Printf("bs8 is subset of bs7: %v\n", bs8.Subset(bs7))
	fmt.Printf("bs9 intersects with bs7: %v\n", bs9.Intersects(bs7))
	fmt.Printf("bs7 equals bs8: %v\n", bs7.Equals(bs8))
	fmt.Println()

	// Example 8: Reverse and Truncate
	fmt.Println("8. Reverse and Truncate")
	fmt.Println("-----------------------")
	bs10, _ := bitset_utils.NewBitSetFromString("11001010")
	fmt.Printf("Original: %s\n", bs10.String())

	bs10.Reverse()
	fmt.Printf("Reversed: %s\n", bs10.String())

	bs10.Truncate(4)
	fmt.Printf("Truncated to 4 bits: %s\n", bs10.String())
	fmt.Println()

	// Example 9: SetAll, ClearAll, FlipAll
	fmt.Println("9. Bulk Operations")
	fmt.Println("------------------")
	bs11 := bitset_utils.NewBitSet(16)
	fmt.Printf("New BitSet (16 bits): %s\n", bs11.String())
	fmt.Printf("Is empty: %v\n", bs11.IsEmpty())

	bs11.SetAll()
	fmt.Printf("After SetAll: %s\n", bs11.String())
	fmt.Printf("Is full: %v\n", bs11.IsFull())

	bs11.FlipAll()
	fmt.Printf("After FlipAll: %s\n", bs11.String())
	fmt.Printf("Count: %d\n", bs11.Count())

	bs11.ClearAll()
	fmt.Printf("After ClearAll: %s\n", bs11.String())
	fmt.Printf("Is empty: %v\n", bs11.IsEmpty())
	fmt.Println()

	// Example 10: Range iteration
	fmt.Println("10. Range Iteration")
	fmt.Println("-------------------")
	bs12 := bitset_utils.NewBitSet(50)
	bs12.Set(5)
	bs12.Set(15)
	bs12.Set(25)
	bs12.Set(35)
	bs12.Set(45)

	fmt.Printf("Set bits: ")
	bs12.Range(func(pos int) bool {
		fmt.Printf("%d ", pos)
		return true
	})
	fmt.Println()

	fmt.Printf("First 3 set bits: ")
	count := 0
	bs12.Range(func(pos int) bool {
		fmt.Printf("%d ", pos)
		count++
		return count < 3
	})
	fmt.Println()
}
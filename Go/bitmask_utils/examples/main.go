// Example demonstrating bitmask_utils usage
package main

import (
	"fmt"
	"bitmask_utils"
)

func main() {
	fmt.Println("=== BitMask Utils Examples ===")
	fmt.Println()

	// Example 1: Basic operations
	fmt.Println("1. Basic Operations:")
	bm := bitmask_utils.NewBitMask(16)
	fmt.Printf("   Created bitmask with size: %d\n", bm.Size())
	
	bm.Set(5)
	bm.Set(10)
	bm.Set(15)
	fmt.Printf("   Set bits 5, 10, 15: %s\n", bm.ToBinaryString())
	fmt.Printf("   Is bit 5 set? %v\n", bm.IsSet(5))
	fmt.Printf("   Is bit 6 set? %v\n", bm.IsSet(6))
	fmt.Printf("   Count of set bits: %d\n", bm.CountOnes())
	fmt.Println()

	// Example 2: Toggle and Clear
	fmt.Println("2. Toggle and Clear:")
	bm.Toggle(5)
	fmt.Printf("   After toggling bit 5: %s\n", bm.ToBinaryString())
	bm.Clear(10)
	fmt.Printf("   After clearing bit 10: %s\n", bm.ToBinaryString())
	fmt.Println()

	// Example 3: Bitwise operations
	fmt.Println("3. Bitwise Operations:")
	bm1 := bitmask_utils.NewBitMaskFromUint64(0b1100)
	bm2 := bitmask_utils.NewBitMaskFromUint64(0b1010)
	fmt.Printf("   BM1: %s\n", bm1.ToBinaryString())
	fmt.Printf("   BM2: %s\n", bm2.ToBinaryString())
	
	bm1And := bm1.Clone()
	bm1And.And(bm2)
	fmt.Printf("   AND: %s\n", bm1And.ToBinaryString())
	
	bm1Or := bm1.Clone()
	bm1Or.Or(bm2)
	fmt.Printf("   OR:  %s\n", bm1Or.ToBinaryString())
	
	bm1Xor := bm1.Clone()
	bm1Xor.Xor(bm2)
	fmt.Printf("   XOR: %s\n", bm1Xor.ToBinaryString())
	fmt.Println()

	// Example 4: Shift and Rotate
	fmt.Println("4. Shift and Rotate:")
	bm = bitmask_utils.NewBitMaskFromUint64(0b1011)
	fmt.Printf("   Original: %s\n", bm.ToBinaryString())
	
	bm = bm.Clone()
	bm.LeftShift(2)
	fmt.Printf("   Left shift 2: %s\n", bm.ToBinaryString())
	
	bm = bitmask_utils.NewBitMaskFromUint64(0b101100)
	bm.RightShift(2)
	fmt.Printf("   Right shift 2: %s\n", bm.ToBinaryString())
	
	bm = bitmask_utils.NewBitMask(8)
	bm.Set(0)
	bm.Set(2)
	bm.RotateLeft(3)
	fmt.Printf("   Rotate left 3: %s\n", bm.ToBinaryString())
	fmt.Println()

	// Example 5: Find operations
	fmt.Println("5. Find Operations:")
	bm = bitmask_utils.NewBitMask(32)
	bm.Set(5)
	bm.Set(10)
	bm.Set(20)
	fmt.Printf("   Bitmask: %s\n", bm.ToBinaryString())
	fmt.Printf("   First set bit: %d\n", bm.FindFirstSet())
	fmt.Printf("   Last set bit: %d\n", bm.FindLastSet())
	fmt.Printf("   First clear bit: %d\n", bm.FindFirstClear())
	fmt.Printf("   All set bit positions: %v\n", bm.GetSetBits())
	fmt.Println()

	// Example 6: Range operations
	fmt.Println("6. Range Operations:")
	bm = bitmask_utils.NewBitMask(16)
	bm.SetRange(4, 8)
	fmt.Printf("   Set range [4,8): %s\n", bm.ToBinaryString())
	bm.ClearRange(5, 7)
	fmt.Printf("   Clear range [5,7): %s\n", bm.ToBinaryString())
	
	sub, _ := bm.GetRange(2, 10)
	fmt.Printf("   Get range [2,10): %s\n", sub.ToBinaryString())
	fmt.Println()

	// Example 7: Bulk operations
	fmt.Println("7. Bulk Operations:")
	bm = bitmask_utils.NewBitMask(16)
	bm.SetBits([]int{0, 3, 7, 15})
	fmt.Printf("   Set multiple bits: %s\n", bm.ToBinaryString())
	bm.ClearBits([]int{3, 7})
	fmt.Printf("   Clear multiple bits: %s\n", bm.ToBinaryString())
	bm.SetAll()
	fmt.Printf("   Set all: %s\n", bm.ToBinaryString())
	bm.ClearAll()
	fmt.Printf("   Clear all: %s\n", bm.ToBinaryString())
	fmt.Println()

	// Example 8: Set operations
	fmt.Println("8. Set Operations:")
	bm1 = bitmask_utils.NewBitMaskFromUint64(0b1000)
	bm2 = bitmask_utils.NewBitMaskFromUint64(0b1100)
	fmt.Printf("   BM1: %s\n", bm1.ToBinaryString())
	fmt.Printf("   BM2: %s\n", bm2.ToBinaryString())
	fmt.Printf("   Intersects: %v\n", bm1.Intersects(bm2))
	fmt.Printf("   BM1 subset of BM2: %v\n", bm1.SubsetOf(bm2))
	fmt.Printf("   BM2 subset of BM1: %v\n", bm2.SubsetOf(bm1))
	fmt.Println()

	// Example 9: Large bitmask
	fmt.Println("9. Large BitMask (256 bits):")
	bm = bitmask_utils.NewBitMask(256)
	bm.Set(0)
	bm.Set(64)
	bm.Set(128)
	bm.Set(255)
	fmt.Printf("   Size: %d\n", bm.Size())
	fmt.Printf("   Set bits: %v\n", bm.GetSetBits())
	fmt.Printf("   Count: %d\n", bm.CountOnes())
	fmt.Println()

	// Example 10: Reverse
	fmt.Println("10. Reverse:")
	bm = bitmask_utils.NewBitMask(8)
	bm.Set(0)
	bm.Set(3)
	bm.Set(7)
	fmt.Printf("    Before: %s\n", bm.ToBinaryString())
	bm.Reverse()
	fmt.Printf("    After:  %s\n", bm.ToBinaryString())
	fmt.Println()

	// Example 11: From uint64 and bytes
	fmt.Println("11. From uint64 and bytes:")
	bm = bitmask_utils.NewBitMaskFromUint64(0xDEADBEEF)
	fmt.Printf("    From uint64 0xDEADBEEF: %s\n", bm.ToBinaryString())
	
	data := []byte{0x12, 0x34, 0x56, 0x78}
	bm = bitmask_utils.NewBitMaskFromBytes(data)
	fmt.Printf("    From bytes [0x12, 0x34, 0x56, 0x78]: %s\n", bm.ToBinaryString())
	fmt.Println()

	// Example 12: Practical use case - Permission flags
	fmt.Println("12. Practical Example - Permission Flags:")
	type Permission int
	const (
		Read Permission = iota
		Write
		Execute
		Delete
		Admin
	)
	
	permissions := bitmask_utils.NewBitMask(5)
	permissions.Set(int(Read))
	permissions.Set(int(Write))
	permissions.Set(int(Execute))
	
	fmt.Printf("    Permissions: %s\n", permissions.ToBinaryString())
	fmt.Printf("    Can Read: %v\n", permissions.IsSet(int(Read)))
	fmt.Printf("    Can Write: %v\n", permissions.IsSet(int(Write)))
	fmt.Printf("    Can Delete: %v\n", permissions.IsSet(int(Delete)))
	fmt.Printf("    Is Admin: %v\n", permissions.IsSet(int(Admin)))
	fmt.Println()

	// Example 13: Practical use case - Feature flags
	fmt.Println("13. Practical Example - Feature Flags:")
	type Feature int
	const (
		DarkMode Feature = iota
		Notifications
		Analytics
		BetaFeatures
		AutoUpdate
	)
	
	features := bitmask_utils.NewBitMask(5)
	features.Set(int(DarkMode))
	features.Set(int(Analytics))
	features.Set(int(BetaFeatures))
	
	fmt.Printf("    Feature flags: %s\n", features.ToBinaryString())
	fmt.Printf("    DarkMode enabled: %v\n", features.IsSet(int(DarkMode)))
	fmt.Printf("    Notifications enabled: %v\n", features.IsSet(int(Notifications)))
	fmt.Printf("    Analytics enabled: %v\n", features.IsSet(int(Analytics)))
	fmt.Printf("    BetaFeatures enabled: %v\n", features.IsSet(int(BetaFeatures)))
	
	fmt.Println("\n=== Examples Complete ===")
}
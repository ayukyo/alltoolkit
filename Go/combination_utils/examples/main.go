// Example usage of combination_utils package
package main

import (
	"fmt"

	"github.com/ayukyo/alltoolkit/Go/combination_utils"
)

func main() {
	fmt.Println("=== 组合数学工具示例 ===")
	fmt.Println()

	// 1. 组合示例
	fmt.Println("【组合 Combinations】")
	nums := []int{1, 2, 3, 4, 5}
	fmt.Printf("从 %v 中选 3 个的组合:\n", nums)
	combos := combination_utils.Combinations(nums, 3)
	for i, c := range combos {
		fmt.Printf("  %d: %v\n", i+1, c)
	}
	fmt.Printf("共 %d 种组合\n\n", len(combos))

	// 2. 排列示例
	fmt.Println("【排列 Permutations】")
	colors := []string{"红", "绿", "蓝"}
	fmt.Printf("%v 的全排列:\n", colors)
	perms := combination_utils.Permutations(colors)
	for i, p := range perms {
		fmt.Printf("  %d: %v\n", i+1, p)
	}
	fmt.Printf("共 %d 种排列\n\n", len(perms))

	// 3. k-排列示例
	fmt.Println("【k-排列 PermutationsK】")
	digits := []int{1, 2, 3, 4}
	fmt.Printf("从 %v 中选 2 个排列:\n", digits)
	permK := combination_utils.PermutationsK(digits, 2)
	for i, p := range permK {
		fmt.Printf("  %d: %v\n", i+1, p)
	}
	fmt.Printf("共 %d 种 k-排列\n\n", len(permK))

	// 4. 重复组合示例
	fmt.Println("【重复组合 CombinationsWithRepetition】")
	items := []string{"A", "B"}
	fmt.Printf("从 %v 中选 3 个（可重复）:\n", items)
	combRep := combination_utils.CombinationsWithRepetition(items, 3)
	for i, c := range combRep {
		fmt.Printf("  %d: %v\n", i+1, c)
	}
	fmt.Printf("共 %d 种\n\n", len(combRep))

	// 5. 幂集示例
	fmt.Println("【幂集 PowerSet】")
	set := []string{"苹果", "香蕉"}
	fmt.Printf("%v 的所有子集:\n", set)
	powerSet := combination_utils.PowerSet(set)
	for i, s := range powerSet {
		fmt.Printf("  %d: %v\n", i+1, s)
	}
	fmt.Printf("共 %d 个子集\n\n", len(powerSet))

	// 6. 笛卡尔积示例
	fmt.Println("【笛卡尔积 CartesianProduct】")
	sizes := []string{"S", "M", "L"}
	colors2 := []string{"红", "蓝"}
	fmt.Printf("尺寸 %v × 颜色 %v:\n", sizes, colors2)
	cartProd := combination_utils.CartesianProduct(sizes, colors2)
	for i, c := range cartProd {
		fmt.Printf("  %d: %v\n", i+1, c)
	}
	fmt.Printf("共 %d 种组合\n\n", len(cartProd))

	// 7. 多重集排列示例
	fmt.Println("【多重集排列 MultiSetPermutation】")
	multiset := []string{"A", "A", "B"}
	fmt.Printf("%v 的唯一排列:\n", multiset)
	multiPerms := combination_utils.MultiSetPermutation(multiset)
	for i, p := range multiPerms {
		fmt.Printf("  %d: %v\n", i+1, p)
	}
	fmt.Printf("共 %d 种唯一排列\n\n", len(multiPerms))

	// 8. 计数函数示例
	fmt.Println("【计数函数】")

	// 二项式系数
	nCk, _ := combination_utils.BinomialCoefficient(10, 4)
	fmt.Printf("C(10, 4) = %d\n", nCk)

	// 阶乘
	fact, _ := combination_utils.Factorial(6)
	fmt.Printf("6! = %d\n", fact)

	// k-排列数
	nPk, _ := combination_utils.CountPermutations(8, 3)
	fmt.Printf("P(8, 3) = %d\n", nPk)

	// 幂集大小
	pwSize := combination_utils.CountPowerSet(4)
	fmt.Printf("4个元素的幂集大小 = %d (2^4)\n", pwSize)

	// 重复组合数
	repCount, _ := combination_utils.CombinationsWithRepetitionCount(3, 2)
	fmt.Printf("C'(3, 2) = %d\n", repCount)

	// 笛卡尔积大小
	cartCount, _ := combination_utils.CartesianProductCount(3, 4, 2)
	fmt.Printf("3×4×2 的笛卡尔积大小 = %d\n", cartCount)

	// 多重集排列数
	multiCount, _ := combination_utils.MultiSetPermutationCount(5, 2, 3)
	fmt.Printf("多重集(2个A, 3个B, 共5个)的排列数 = %d\n", multiCount)

	fmt.Println()

	// 9. 通道生成器示例（大数据集）
	fmt.Println("【通道生成器（内存友好）】")
	fmt.Println("使用通道处理 C(6,3)=20 种组合:")
	count := 0
	for combo := range combination_utils.CombinationsChan([]int{1, 2, 3, 4, 5, 6}, 3) {
		count++
		if count <= 5 {
			fmt.Printf("  %d: %v\n", count, combo)
		} else if count == 6 {
			fmt.Println("  ... (更多组合)")
		}
	}
	fmt.Printf("共处理 %d 种组合\n\n", count)

	// 10. 实际应用示例
	fmt.Println("【实际应用：密码生成】")
	chars := []string{"A", "B", "C", "1", "2"}
	fmt.Printf("从 %v 中生成所有 3 位密码:\n", chars)
	passwords := combination_utils.PermutationsK(chars, 3)
	for i, p := range passwords {
		if i < 5 {
			fmt.Printf("  %s%s%s\n", p[0], p[1], p[2])
		} else if i == 5 {
			fmt.Printf("  ... 共 %d 种密码\n", len(passwords))
			break
		}
	}

	fmt.Println()
	fmt.Println("=== 示例结束 ===")
}
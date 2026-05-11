// Example usage of genetic_algorithm_utils
package main

import (
	"fmt"
	"math"
	"strings"
	"time"

	"github.com/ayukyo/alltoolkit/Go/genetic_algorithm_utils"
)

func main() {
	fmt.Println("=== 遗传算法工具库示例 ===")
	fmt.Println()

	// 示例 1: Sphere 函数优化
	example1SphereOptimization()

	// 示例 2: Rastrigin 多峰函数优化
	example2RastriginOptimization()

	// 示例 3: 自定义适应度函数
	example3CustomFitness()

	// 示例 4: 自定义交叉和变异方法
	example4CustomMethods()

	// 示例 5: 使用收敛条件和目标适应度
	example5StoppingConditions()

	// 示例 6: 不同基因边界
	example6PerGeneBounds()

	// 示例 7: 分析优化过程
	example7Analysis()

	// 示例 8: 多目标优化演示
	example8MultiObjective()

	// 示例 9: Rosenbrock 函数优化
	example9Rosenbrock()

	// 示例 10: 实际应用 - 寻找最优参数
	example10PracticalApplication()
}

func example1SphereOptimization() {
	fmt.Println("示例 1: Sphere 函数优化")
	fmt.Println("目标: 找到使 f(x) = Σx² 最小的 x")
	fmt.Println("理论最优解: x = [0, 0, 0, 0, 0]")

	config := genetica.Config{
		PopulationSize:  50,
		GeneCount:        5,
		Generations:      100,
		CrossoverRate:    0.8,
		MutationRate:     0.1,
		EliteCount:       2,
		TournamentSize:   3,
		GeneBounds:       genetica.Bound{Min: -5, Max: 5},
		Verbose:         false,
		RandomSeed:      42,
	}

	ga, err := genetica.New(config, genetica.SphereFunction)
	if err != nil {
		panic(err)
	}

	start := time.Now()
	result := ga.Run()
	elapsed := time.Since(start)

	fmt.Printf("最优解: %.4f\n", result.BestIndividual.Genes)
	fmt.Printf("最优适应度: %.6f (接近 0 表示最优)\n", result.BestFitness)
	fmt.Printf("运行时间: %v\n", elapsed)
	fmt.Println(strings.Repeat("-", 50))
}

func example2RastriginOptimization() {
	fmt.Println("示例 2: Rastrigin 多峰函数优化")
	fmt.Println("目标: 找到使 Rastrigin 函数最小的解")
	fmt.Println("理论最优解: x = [0, 0] (全局最小值 = 0)")
	fmt.Println("挑战: 函数有大量局部极小值")

	config := genetica.Config{
		PopulationSize:  100,
		GeneCount:        2,
		Generations:      200,
		CrossoverRate:    0.9,
		MutationRate:     0.05,
		EliteCount:       5,
		TournamentSize:   4,
		GeneBounds:       genetica.Bound{Min: -5.12, Max: 5.12},
		Verbose:         false,
		RandomSeed:      42,
	}

	ga, _ := genetica.New(config, genetica.RastriginFunction)
	result := ga.Run()

	fmt.Printf("最优解: %.4f\n", result.BestIndividual.Genes)
	fmt.Printf("最优适应度: %.6f\n", result.BestFitness)
	fmt.Printf("总代数: %d\n", result.TotalGenerations)
	fmt.Println(strings.Repeat("-", 50))
}

func example3CustomFitness() {
	fmt.Println("示例 3: 自定义适应度函数")
	fmt.Println("目标: 最大化 f(x,y) = sin(x)*cos(y) + x*y")

	customFitness := func(genes []float64) float64 {
		x, y := genes[0], genes[1]
		return math.Sin(x)*math.Cos(y) + x*y
	}

	config := genetica.Config{
		PopulationSize:  50,
		GeneCount:        2,
		Generations:      100,
		CrossoverRate:    0.8,
		MutationRate:     0.1,
		EliteCount:       3,
		TournamentSize:   3,
		GeneBounds:       genetica.Bound{Min: -5, Max: 5},
		Verbose:         false,
		RandomSeed:      42,
	}

	ga, _ := genetica.New(config, customFitness)
	result := ga.Run()

	x, y := result.BestIndividual.Genes[0], result.BestIndividual.Genes[1]
	fmt.Printf("最优解: x=%.4f, y=%.4f\n", x, y)
	fmt.Printf("最优值: f(x,y) = %.6f\n", result.BestFitness)
	fmt.Println(strings.Repeat("-", 50))
}

func example4CustomMethods() {
	fmt.Println("示例 4: 自定义交叉和变异方法")
	fmt.Println("使用算术交叉 + 多项式变异")

	config := genetica.Config{
		PopulationSize:  30,
		GeneCount:        3,
		Generations:      50,
		CrossoverRate:    0.8,
		MutationRate:     0.1,
		EliteCount:       2,
		TournamentSize:   3,
		GeneBounds:       genetica.Bound{Min: -5, Max: 5},
		Verbose:         false,
		RandomSeed:      42,
	}

	ga, _ := genetica.New(config, genetica.SphereFunction)

	// 使用自定义方法
	ga.CrossoverFunc = genetica.ArithmeticCrossover
	ga.MutationFunc = genetica.PolynomialMutation
	ga.SelectionFunc = genetica.RankSelection

	result := ga.Run()

	fmt.Printf("最优解: %.4f\n", result.BestIndividual.Genes)
	fmt.Printf("最优适应度: %.6f\n", result.BestFitness)
	fmt.Println(strings.Repeat("-", 50))
}

func example5StoppingConditions() {
	fmt.Println("示例 5: 使用停止条件")
	fmt.Println("设置目标适应度和收敛判定")

	config := genetica.Config{
		PopulationSize:  50,
		GeneCount:        5,
		Generations:      1000, // 高代数限制
		CrossoverRate:    0.8,
		MutationRate:     0.15,
		EliteCount:       2,
		TournamentSize:   3,
		GeneBounds:       genetica.Bound{Min: -5, Max: 5},
		ConvergenceGen:   30,   // 30 代无改进则停止
		MinFitness:       -0.01, // 达到目标则停止
		Verbose:         false,
		RandomSeed:      42,
	}

	ga, _ := genetica.New(config, genetica.SphereFunction)
	result := ga.Run()

	fmt.Printf("最优适应度: %.6f\n", result.BestFitness)
	fmt.Printf("总代数: %d (设置上限: 1000)\n", result.TotalGenerations)
	fmt.Printf("提前收敛: %v\n", result.Converged)
	fmt.Println(strings.Repeat("-", 50))
}

func example6PerGeneBounds() {
	fmt.Println("示例 6: 不同基因边界")
	fmt.Println("每个基因有独立的取值范围")

	config := genetica.Config{
		PopulationSize:  40,
		GeneCount:        3,
		Generations:      50,
		CrossoverRate:    0.8,
		MutationRate:     0.1,
		EliteCount:       2,
		TournamentSize:   3,
		Bounds: []genetica.Bound{
			{Min: -100, Max: -50},  // 基因 1: 负值范围
			{Min: 0, Max: 100},     // 基因 2: 正值范围
			{Min: -10, Max: 10},    // 基因 3: 小范围
		},
		Verbose:    false,
		RandomSeed: 42,
	}

	ga, _ := genetica.New(config, genetica.SphereFunction)
	result := ga.Run()

	fmt.Printf("基因边界:\n")
	fmt.Printf("  基因 1: [-100, -50], 结果: %.4f\n", result.BestIndividual.Genes[0])
	fmt.Printf("  基因 2: [0, 100],    结果: %.4f\n", result.BestIndividual.Genes[1])
	fmt.Printf("  基因 3: [-10, 10],   结果: %.4f\n", result.BestIndividual.Genes[2])
	fmt.Printf("最优适应度: %.6f\n", result.BestFitness)
	fmt.Println(strings.Repeat("-", 50))
}

func example7Analysis() {
	fmt.Println("示例 7: 分析优化过程")

	config := genetica.Config{
		PopulationSize:  30,
		GeneCount:        2,
		Generations:      50,
		CrossoverRate:    0.8,
		MutationRate:     0.1,
		EliteCount:       2,
		TournamentSize:   3,
		GeneBounds:       genetica.Bound{Min: -5, Max: 5},
		Verbose:         false,
		RandomSeed:      42,
	}

	ga, _ := genetica.New(config, genetica.SphereFunction)
	result := ga.Run()

	// 分析历史记录
	fmt.Println("适应度变化历史 (每 10 代):")
	for i := 0; i < len(result.FitnessHistory); i += 10 {
		best := result.FitnessHistory[i]
		avg := result.AvgFitnessHistory[i]
		fmt.Printf("  代 %d: 最佳=%.6f, 平均=%.6f\n", i, best, avg)
	}

	// 计算最终种群多样性
	diversity := genetica.CalculateDiversity(result.Population)
	fmt.Printf("最终种群多样性: %.4f\n", diversity)

	// 最优和最差个体
	best := genetica.GetBestIndividual(result.Population)
	worst := genetica.GetWorstIndividual(result.Population)
	fmt.Printf("种群最佳适应度: %.6f\n", best.Fitness)
	fmt.Printf("种群最差适应度: %.6f\n", worst.Fitness)
	fmt.Println(strings.Repeat("-", 50))
}

func example8MultiObjective() {
	fmt.Println("示例 8: 多目标优化演示")
	fmt.Println("目标: 同时最小化 f₁ = x² 和 f₂ = (x-2)²")
	fmt.Println("Pareto 最优解应在 x ∈ [0, 2]")

	// 创建多目标个体种群
	population := []*genetica.MultiObjectiveIndividual{}

	// 生成一些候选解
	for i := 0; i < 10; i++ {
		x := float64(i) * 0.5 // x 从 0 到 4.5
		population = append(population, &genetica.MultiObjectiveIndividual{
			Genes:      []float64{x},
			Objectives: []float64{x * x, (x - 2) * (x - 2)}, // f₁, f₂
		})
	}

	// 非支配排序
	fronts := genetica.FastNonDominatedSort(population)

	fmt.Println("Pareto 前沿 (第一层非支配解):")
	for _, ind := range fronts[0] {
		x := ind.Genes[0]
		f1 := ind.Objectives[0]
		f2 := ind.Objectives[1]
		fmt.Printf("  x=%.2f: f₁=%.4f, f₂=%.4f (Rank=%d)\n", x, f1, f2, ind.Rank)
	}

	// 计算拥挤距离
	if len(fronts[0]) > 0 {
		genetica.CalculateCrowdingDistance(fronts[0])
		fmt.Println("\n拥挤距离 (多样性指标):")
		for _, ind := range fronts[0] {
			x := ind.Genes[0]
			fmt.Printf("  x=%.2f: 拥挤距离=%.4f\n", x, ind.Crowding)
		}
	}

	fmt.Println(strings.Repeat("-", 50))
}

func example9Rosenbrock() {
	fmt.Println("示例 9: Rosenbrock 函数优化")
	fmt.Println("目标: 找到 Rosenbrock 函数最小值")
	fmt.Println("理论最优解: x = [1, 1, 1]")

	config := genetica.Config{
		PopulationSize:  100,
		GeneCount:        3,
		Generations:      200,
		CrossoverRate:    0.9,
		MutationRate:     0.1,
		EliteCount:       5,
		TournamentSize:   4,
		GeneBounds:       genetica.Bound{Min: -5, Max: 5},
		Verbose:         false,
		RandomSeed:      42,
	}

	ga, _ := genetica.New(config, genetica.RosenbrockFunction)
	result := ga.Run()

	fmt.Printf("最优解: %.4f (接近 [1, 1, 1])\n", result.BestIndividual.Genes)
	fmt.Printf("最优适应度: %.6f (接近 0)\n", result.BestFitness)

	// 计算与理论最优的距离
	optimal := []float64{1, 1, 1}
	distance := genetica.EuclideanDistance(result.BestIndividual.Genes, optimal)
	fmt.Printf("与理论最优的距离: %.6f\n", distance)
	fmt.Println(strings.Repeat("-", 50))
}

func example10PracticalApplication() {
	fmt.Println("示例 10: 实际应用 - 曲线参数拟合")
	fmt.Println("目标: 找到最佳参数 a, b, c 使 y = a*x² + b*x + c")
	fmt.Println("拟合数据点: (1, 2), (2, 5), (3, 10), (4, 17)")
	fmt.Println("理论参数: a=1, b=0, c=1")

	// 数据点
	dataPoints := []struct{ x, y float64 }{
		{1, 2}, {2, 5}, {3, 10}, {4, 17},
	}

	// 适应度函数: 最小化拟合误差
	fitFitness := func(genes []float64) float64 {
		a, b, c := genes[0], genes[1], genes[2]
		var error float64
		for _, p := range dataPoints {
			predicted := a*p.x*p.x + b*p.x + c
			error += (predicted - p.y) * (predicted - p.y)
		}
		return -error // 返回负误差以最大化
	}

	config := genetica.Config{
		PopulationSize:  50,
		GeneCount:        3, // a, b, c
		Generations:      100,
		CrossoverRate:    0.8,
		MutationRate:     0.1,
		EliteCount:       3,
		TournamentSize:   3,
		GeneBounds:       genetica.Bound{Min: -10, Max: 10},
		Verbose:         false,
		RandomSeed:      42,
	}

	ga, _ := genetica.New(config, fitFitness)
	result := ga.Run()

	a, b, c := result.BestIndividual.Genes[0], result.BestIndividual.Genes[1], result.BestIndividual.Genes[2]
	fmt.Printf("拟合参数: a=%.4f, b=%.4f, c=%.4f\n", a, b, c)
	fmt.Printf("拟合误差: %.6f\n", -result.BestFitness)

	// 显示拟合结果
	fmt.Println("\n拟合对比:")
	for _, p := range dataPoints {
		predicted := a*p.x*p.x + b*p.x + c
		fmt.Printf("  x=%.0f: 实际=%.0f, 预测=%.4f, 误差=%.4f\n", p.x, p.y, predicted, predicted-p.y)
	}

	fmt.Println(strings.Repeat("-", 50))
	fmt.Println("=== 所有示例完成 ===")
}
# Genetic Algorithm Utils

遗传算法工具库 - 提供完整的遗传算法实现，用于优化问题求解。

## 功能特性

### 核心算法
- **GeneticAlgorithm** - 遗传算法主体类，支持自定义配置
- **Population** - 种群管理，自动评估和进化
- **Individual** - 个体表示，支持基因编码和适应度计算

### 选择方法
- **TournamentSelection** - 锦标赛选择（最推荐）
- **RouletteWheelSelection** - 轮盘赌选择（适应度比例）
- **RankSelection** - 排名选择（基于排名而非适应度）

### 交叉方法
- **SinglePointCrossover** - 单点交叉
- **TwoPointCrossover** - 双点交叉
- **UniformCrossover** - 均匀交叉（默认）
- **ArithmeticCrossover** - 算术交叉（加权平均）
- **SBXCrossover** - 模拟二进制交叉（SBX）

### 变异方法
- **GaussianMutation** - 高斯变异（默认，正态分布）
- **UniformMutation** - 均匀变异（随机值）
- **PolynomialMutation** - 多项式变异（NSGA-II 推荐）
- **SwapMutation** - 交换变异（交换基因位置）
- **BoundaryMutation** - 边界变异（极值）

### 基准测试函数
- **SphereFunction** - 球形函数（简单凸函数）
- **RastriginFunction** - Rastrigin 函数（多峰函数）
- **RosenbrockFunction** - Rosenbrock 函数（香蕉函数）
- **AckleyFunction** - Ackley 函数（多峰函数）
- **GriewankFunction** - Griewank 函数（多峰函数）
- **SchwefelFunction** - Schwefel 函数（高度多峰）

### 多目标优化（NSGA-II）
- **MultiObjectiveIndividual** - 多目标个体
- **FastNonDominatedSort** - 快速非支配排序
- **CalculateCrowdingDistance** - 拥挤距离计算
- **ParetoFront** - Pareto 前沿

### 工具函数
- **CalculateDiversity** - 种群多样性计算
- **EuclideanDistance** - 欧氏距离
- **GetBestIndividual/GetWorstIndividual** - 最佳/最差个体

## 配置选项

```go
type Config struct {
    PopulationSize   int       // 种群大小
    GeneCount        int       // 每个个体的基因数量
    Generations      int       // 最大迭代代数
    CrossoverRate    float64   // 交叉概率 (0-1)
    MutationRate     float64   // 变异概率 (0-1)
    EliteCount       int       // 保留精英数量
    TournamentSize   int       // 锦标赛选择大小
    Bounds           []Bound   // 每个基因的边界范围
    GeneBounds       Bound     // 默认基因边界
    ConvergenceGen   int       // 收敛判定代数 (停止条件)
    MinFitness       float64   // 最小适应度目标 (停止条件)
    Verbose          bool      // 是否打印进度信息
    RandomSeed       int64     // 随机种子 (可复现性)
}
```

## 使用示例

### 基础用法 - Sphere 函数优化

```go
package main

import (
    "fmt"
    "github.com/yourrepo/genetica"
)

func main() {
    // 配置遗传算法
    config := genetica.Config{
        PopulationSize:  50,
        GeneCount:        5,
        Generations:      100,
        CrossoverRate:    0.8,
        MutationRate:     0.1,
        EliteCount:       2,
        TournamentSize:   3,
        GeneBounds:       genetica.Bound{Min: -5, Max: 5},
        Verbose:         true,
        RandomSeed:      42,
    }

    // 创建遗传算法实例
    ga, err := genetica.New(config, genetica.SphereFunction)
    if err != nil {
        panic(err)
    }

    // 运行算法
    result := ga.Run()

    // 输出结果
    fmt.Printf("最优解: %v\n", result.BestIndividual.Genes)
    fmt.Printf("最优适应度: %.6f\n", result.BestFitness)
    fmt.Printf("最优代数: %d\n", result.BestGeneration)
    fmt.Printf("总代数: %d\n", result.TotalGenerations)
}
```

### 自定义适应度函数

```go
// 自定义适应度函数
func myFitness(genes []float64) float64 {
    // 例如：最大化 x^2 + y^2（在范围 [-10, 10] 内）
    var sum float64
    for _, gene := range genes {
        sum += gene * gene
    }
    return sum // 直接返回正值表示最大化
}

config := genetica.Config{
    PopulationSize:  100,
    GeneCount:        2,
    Generations:      50,
    CrossoverRate:    0.9,
    MutationRate:     0.05,
    EliteCount:       5,
    GeneBounds:       genetica.Bound{Min: -10, Max: 10},
}

ga, _ := genetica.New(config, myFitness)
result := ga.Run()
```

### 使用自定义交叉和变异方法

```go
ga, _ := genetica.New(config, genetica.SphereFunction)

// 使用算术交叉
ga.CrossoverFunc = genetica.ArithmeticCrossover

// 使用多项式变异
ga.MutationFunc = genetica.PolynomialMutation

// 使用轮盘赌选择
ga.SelectionFunc = genetica.RouletteWheelSelection

result := ga.Run()
```

### 不同基因边界

```go
config := genetica.Config{
    PopulationSize:  50,
    GeneCount:        3,
    Generations:      100,
    CrossoverRate:    0.8,
    MutationRate:     0.1,
    EliteCount:       2,
    TournamentSize:   3,
    Bounds: []genetica.Bound{
        {Min: -100, Max: -50},  // 第一个基因范围
        {Min: 0, Max: 100},     // 第二个基因范围
        {Min: -10, Max: 10},    // 第三个基因范围
    },
}

ga, _ := genetica.New(config, myFitness)
result := ga.Run()
```

### 多目标优化（NSGA-II 基础）

```go
// 创建多目标个体种群
population := []*genetica.MultiObjectiveIndividual{
    {Genes: []float64{1}, Objectives: []float64{1, 5}},
    {Genes: []float64{2}, Objectives: []float64{2, 4}},
    {Genes: []float64{3}, Objectives: []float64{3, 3}},
}

// 非支配排序
fronts := genetica.FastNonDominatedSort(population)

// 计算拥挤距离
genetica.CalculateCrowdingDistance(fronts[0])

// Pareto 前沿是第一层
paretoFront := fronts[0]
```

## 返回结果

```go
type Result struct {
    BestIndividual   *Individual   // 最优个体
    BestFitness       float64       // 最优适应度
    BestGeneration    int           // 发现最优个体的代数
    TotalGenerations  int           // 总迭代代数
    FitnessHistory    []float64     // 每代最优适应度历史
    AvgFitnessHistory []float64     // 每代平均适应度历史
    Population        Population    // 最终种群
    Converged         bool          // 是否提前收敛
}
```

## 算法原理

遗传算法模拟自然进化过程：

1. **初始化** - 随机生成初始种群
2. **评估** - 计算每个个体的适应度
3. **选择** - 根据适应度选择优秀个体作为父代
4. **交叉** - 父代基因交叉产生后代
5. **变异** - 对后代基因进行随机变异
6. **精英保留** - 保留最优个体不参与变异
7. **迭代** - 重复步骤 2-6 直到满足终止条件

## 适用场景

- 函数优化（单峰/多峰函数）
- 参数调优
- 排列问题（TSP、调度）
- 机器学习超参数优化
- 游戏策略优化
- 神经网络权重训练
- 多目标优化问题

## 测试覆盖

- 配置验证测试
- 选择方法测试（锦标赛、轮盘赌、排名）
- 交叉方法测试（单点、双点、均匀、算术、SBX）
- 变异方法测试（高斯、均匀、多项式、交换、边界）
- 基准函数测试（Sphere、Rastrigin、Rosenbrock 等）
- 多目标优化测试（非支配排序、拥挤距离）
- 集成测试（完整优化流程）
- 边界条件测试（小种群、单基因、零变异等）
- 性能基准测试

## 时间复杂度

- 初始化种群：O(P × N)
- 适应度评估：O(P × F)，其中 F 为适应度函数复杂度
- 选择：O(P × T)，其中 T 为锦标赛大小
- 交叉：O(P × N)
- 变异：O(P × N)
- 每代总复杂度：O(P × (N + F))

## 零外部依赖

- 仅使用 Go 标准库
- 无第三方包依赖
- 纯 Go 实现

## 文件结构

```
genetic_algorithm_utils/
├── genetic_algorithm.go        # 主要实现
├── genetic_algorithm_test.go   # 测试文件
├── README.md                   # 说明文档
└── examples/
    └── main.go                 # 使用示例
``
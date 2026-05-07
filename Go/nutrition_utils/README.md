# Nutrition Utils

一个零外部依赖的 Go 语言营养计算和分析工具库。

## 功能特性

### 基础代谢率计算
- `CalculateBMR()` - 使用 Mifflin-St Jeor 公式计算 BMR
- `CalculateBMRHarrisBenedict()` - 使用 Harris-Benedict 公式计算 BMR
- 支持男性/女性不同公式

### 能量消耗计算
- `CalculateTDEE()` - 计算每日总能量消耗
- 支持多种活动级别：久坐、轻度活跃、中度活跃、高度活跃、极度活跃
- `CalculateCaloriesBurned()` - 计算各类运动消耗卡路里

### BMI 分析
- `CalculateBMI()` - 计算体重指数
- `GetBMICategory()` - 返回 BMI 分类（偏瘦/正常/超重/肥胖）
- `GetBMICategoryDetailed()` - 返回详细 BMI 分类
- `IsHealthyBMI()` - 检查 BMI 是否在健康范围

### 体重分析
- `CalculateIdealWeight()` - 使用 Devine 公式计算理想体重
- `CalculateIdealWeightRange()` - 基于 BMI 计算理想体重范围
- `WeightForBMI()` - 计算达到目标 BMI 所需体重
- `BMIForWeight()` - 计算给定体重的 BMI

### 水分摄入
- `CalculateWaterIntake()` - 计算每日推荐饮水量
- 根据体重和活动级别自动调整

### 营养素计算
- `CalculateMacro()` - 计算三大营养素分配
- `CalculateFiber()` - 计算推荐纤维摄入量
- `CalculateCaloriesFromMacro()` - 从营养素计算卡路里
- `CalculateMacroFromCalories()` - 从卡路里计算营养素克数

### 身体成分
- `LeanBodyMass()` - 计算去脂体重
- `BodyFatFromBMI()` - 从 BMI 估算体脂率

### 体重变化规划
- `CalculateRequiredDeficit()` - 计算达成目标所需的每日热量缺口
- `CalculateWeightLossTimeline()` - 计算达成目标的预计时间
- `WeightChangeRate()` - 计算每周体重变化率

### 饮食记录与分析
- `Food` 结构体 - 食物营养信息
- `Meal` 结构体 - 一餐的食物组合
- `DailyLog` 结构体 - 一天的饮食记录
- `CalculateMealNutrition()` - 计算一餐总营养
- `CalculateDailyNutrition()` - 计算一天总营养

### 食物评分
- `ScoreFood()` - 对食物进行营养评分
- 综合评估卡路里密度、蛋白质质量、宏观营养平衡、微量营养素
- 返回字母等级（A-F）

### 常见食物数据库
- 内置 15+ 种常见食物营养数据
- `GetFood()` - 查询食物数据库
- `AddFood()` - 添加自定义食物

## 安装

```bash
go get github.com/ayukyo/alltoolkit/Go/nutrition_utils
```

## 使用示例

```go
package main

import (
    "fmt"
    nutrition "github.com/ayukyo/alltoolkit/Go/nutrition_utils"
)

func main() {
    // 创建个人档案
    profile := nutrition.Profile{
        Weight:   70,    // kg
        Height:   175,   // cm
        Age:      30,    // years
        Gender:   nutrition.Male,
        Activity: nutrition.ModeratelyActive,
        Goal:     nutrition.MaintainWeight,
    }

    // 完整分析
    result, err := nutrition.AnalyzeProfile(profile)
    if err != nil {
        panic(err)
    }

    fmt.Printf("BMR: %.1f cal/day\n", result.BMR)
    fmt.Printf("TDEE: %.1f cal/day\n", result.TDEE)
    fmt.Printf("Target Calories: %.1f cal/day\n", result.TargetCalories)
    fmt.Printf("BMI: %.1f (%s)\n", result.BMI, result.BMICategory)
    fmt.Printf("Ideal Weight: %.1f kg\n", result.IdealWeight)
    fmt.Printf("Water Intake: %.1f L/day\n", result.WaterIntake)
    fmt.Printf("Protein: %.1f g/day\n", result.ProteinGrams)
    fmt.Printf("Carbs: %.1f g/day\n", result.CarbGrams)
    fmt.Printf("Fat: %.1f g/day\n", result.FatGrams)

    // 单独计算 BMR
    bmr, _ := nutrition.CalculateBMR(70, 175, 30, nutrition.Male)
    fmt.Printf("BMR: %.1f\n", bmr)

    // 单独计算 BMI
    bmi, _ := nutrition.CalculateBMI(70, 175)
    fmt.Printf("BMI: %.1f (%s)\n", bmi, nutrition.GetBMICategory(bmi))

    // 计算运动消耗
    calBurned := nutrition.CalculateCaloriesBurned("running", 70, 30)
    fmt.Printf("Running 30min: %.1f cal\n", calBurned)

    // 减重计划
    deficit := nutrition.CalculateRequiredDeficit(80, 75, 10)
    fmt.Printf("Daily deficit to lose 5kg in 10 weeks: %.1f cal\n", deficit)

    // 使用食物数据库
    chicken, ok := nutrition.GetFood("chicken_breast")
    if ok {
        fmt.Printf("Chicken breast: %.1f cal, %.1f g protein\n", 
            chicken.Calories, chicken.Protein)
    }

    // 食物评分
    score := nutrition.ScoreFood(chicken)
    fmt.Printf("Chicken nutrition score: %.1f (Grade: %s)\n", 
        score.Overall, score.Grade)

    // 创建一餐并计算营养
    meal := nutrition.Meal{
        Name: "Lunch",
        Foods: []nutrition.FoodItem{
            {Food: chicken, Quantity: 1.5},
            {Food: nutrition.CommonFoods["brown_rice"], Quantity: 2},
        },
    }
    mealNutrition := nutrition.CalculateMealNutrition(meal)
    fmt.Printf("Meal total: %.1f cal, %.1f g protein\n", 
        mealNutrition.Calories, mealNutrition.Protein)
}
```

## API 参考

### 类型

```go
type Gender string
const (
    Male   Gender = "M"
    Female Gender = "F"
)

type ActivityLevel int
const (
    Sedentary        // 无运动
    LightlyActive    // 轻度运动 1-3天/周
    ModeratelyActive // 中度运动 3-5天/周
    VeryActive       // 高强度运动 6-7天/周
    ExtraActive      // 极高强度运动 + 体力劳动
)

type Goal int
const (
    LoseWeight     // 减重
    MaintainWeight // 维持体重
    GainWeight     // 增重
    BuildMuscle    // 增肌
)

type Profile struct {
    Weight   float64       // 体重 (kg)
    Height   float64       // 身高 (cm)
    Age      int           // 年龄
    Gender   Gender        // 性别
    Activity ActivityLevel // 活动级别
    Goal     Goal          // 目标
    BodyFat  float64       // 体脂率 (可选)
}

type NutritionResult struct {
    BMR            float64   // 基础代谢率
    TDEE           float64   // 每日总能量消耗
    TargetCalories float64   // 目标卡路里
    BMI            float64   // 体重指数
    BMICategory    string    // BMI 分类
    IdealWeight    float64   // 理想体重
    WaterIntake    float64   // 饮水量 (L)
    ProteinGrams   float64   // 蛋白质 (g)
    CarbGrams      float64   // 碳水化合物 (g)
    FatGrams       float64   // 脂肪 (g)
    FiberGrams     float64   // 纤维 (g)
    MacroRatio     MacroRatio // 营养素比例
}

type Food struct {
    Name         string
    ServingSize  float64 // 份量大小 (g)
    Calories     float64 // 卡路里
    Protein      float64 // 蛋白质 (g)
    Carbs        float64 // 碳水 (g)
    Fat          float64 // 脂肪 (g)
    Fiber        float64 // 纯纤维 (g)
    Sugar        float64 // 糖 (g)
    Sodium       float64 // 钠 (mg)
    // ...
}

type NutrientScore struct {
    Overall       float64 // 总分 (0-100)
    Calorie       float64 // 卡路里密度评分
    Protein       float64 // 蛋白质评分
    Micronutrient float64 // 微量营养素评分
    Balance       float64 // 营养平衡评分
    Grade         string  // 字母等级 (A-F)
}
```

### 主要函数

```go
// BMR 计算
func CalculateBMR(weight, height float64, age int, gender Gender) (float64, error)
func CalculateBMRHarrisBenedict(weight, height float64, age int, gender Gender) (float64, error)

// TDEE 计算
func CalculateTDEE(bmr float64, activity ActivityLevel) (float64, error)

// BMI
func CalculateBMI(weight, height float64) (float64, error)
func GetBMICategory(bmi float64) string
func GetBMICategoryDetailed(bmi float64) string

// 体重分析
func CalculateIdealWeight(height float64, gender Gender) float64
func CalculateIdealWeightRange(height float64) (min, max float64)

// 水分
func CalculateWaterIntake(weight float64, activity ActivityLevel) float64

// 营养素
func CalculateMacro(calories float64, goal Goal) (protein, carbs, fat float64)
func CalculateFiber(calories float64) float64

// 运动消耗
func CalculateCaloriesBurned(activity string, weight, durationMinutes float64) float64

// 体重规划
func CalculateRequiredDeficit(current, target float64, weeks int) float64
func CalculateWeightLossTimeline(current, target, dailyDeficit float64) int

// 完整分析
func AnalyzeProfile(p Profile) (*NutritionResult, error)

// 饮食计算
func CalculateMealNutrition(meal Meal) Food
func CalculateDailyNutrition(log DailyLog) Food

// 食物评分
func ScoreFood(f Food) NutrientScore

// 食物数据库
func GetFood(name string) (Food, bool)
func AddFood(name string, f Food)
```

## 测试

```bash
cd Go/nutrition_utils
go test -v
```

## 性能测试

```bash
go test -bench=.
```

## 许可证

MIT License
# Grade Utils - 成绩计算工具

成绩计算与 GPA 处理工具，支持多种成绩制度转换、GPA 计算、成绩分析等功能。

## 功能特性

- **GPA 计算**: 支持 4.0 制、5.0 制等多种标准
- **成绩转换**: 百分制、字母等级、中文等级互转
- **加权计算**: 学分加权平均分、学分绩点
- **成绩分析**: 分布统计、趋势分析、排名计算
- **成绩预测**: 期末成绩预测、GPA 达成目标预测
- **成绩单格式化**: 摘要生成、课程列表格式化

## 快速开始

```python
from grade_utils.mod import (
    calculate_gpa,
    calculate_weighted_average,
    get_grade_level,
    GradeConverter,
    GPACalculator,
    GradeAnalyzer,
    GradePredictor,
)

# 快速计算 GPA
gpa = calculate_gpa([85, 90, 78, 92], credits=[3, 4, 2, 3])
print(f"GPA: {gpa}")

# 计算加权平均分
avg = calculate_weighted_average([85, 90, 78], credits=[3, 4, 2])
print(f"加权平均分: {avg}")

# 成绩等级转换
level = get_grade_level(85)  # "良好"
letter = get_letter_grade(85)  # "B"
```

## 核心类

### GradeConverter - 成绩转换器

```python
# 百分制转 GPA
gpa = GradeConverter.percentage_to_gpa(85, gpa_scale=4.0)  # 3.7

# 百分制转字母等级
letter = GradeConverter.percentage_to_letter(85)  # "B"

# 百分制转中文等级
chinese = GradeConverter.percentage_to_chinese(85)  # "良好"

# 字母等级转 GPA
gpa = GradeConverter.letter_to_gpa("A+")  # 4.0
```

### GPACalculator - GPA 计算器

```python
from grade_utils.mod import Course, GPACalculator

courses = [
    Course(name="数学", score=90, credit=4),
    Course(name="英语", score=85, credit=3),
    Course(name="物理", score=78, credit=2),
]

# 加权 GPA
gpa = GPACalculator.calculate_weighted_gpa(courses, gpa_scale=4.0)

# 加权平均分
avg = GPACalculator.calculate_weighted_average(courses)

# 学分绩点
points = GPACalculator.calculate_credit_points(courses)
```

### GradeAnalyzer - 成绩分析器

```python
# 成绩分布
dist = GradeAnalyzer.get_distribution(courses)
# {"优秀": 1, "良好": 1, "中等": 1, "及格": 0, "不及格": 0}

# 统计信息
stats = GradeAnalyzer.get_statistics(courses)
# {"max": 90, "min": 78, "mean": 84.33, "median": 85, "std": 6.03}

# 趋势分析（按学期）
semesters = {
    "2023-1": [Course("数学", 80, 4)],
    "2023-2": [Course("数学", 85, 4)],
}
trend = GradeAnalyzer.analyze_trend(semesters)
```

### GradePredictor - 成绩预测器

```python
# 期末成绩预测
result = GradePredictor.predict_final(
    current_score=75,
    target_score=80,
    final_weight=0.3
)
print(f"期末需要: {result['needed_final']}分")

# GPA 目标预测
result = GradePredictor.predict_gpa(
    current_gpa=3.0,
    remaining_credits=30,
    target_gpa=3.5,
    total_credits=120
)
```

## 成绩制度对照表

### GPA 4.0 制

| 百分制 | GPA | 字母等级 |
|--------|-----|----------|
| 90-100 | 4.0 | A |
| 85-89 | 3.7 | A- |
| 82-84 | 3.3 | B+ |
| 78-81 | 3.0 | B |
| 75-77 | 2.7 | B- |
| 72-74 | 2.3 | C+ |
| 68-71 | 2.0 | C |
| 64-67 | 1.5 | D+ |
| 60-63 | 1.0 | D |
| 0-59 | 0.0 | F |

### GPA 5.0 制

| 百分制 | GPA |
|--------|-----|
| 95-100 | 5.0 |
| 90-94 | 4.5 |
| 85-89 | 4.0 |
| 80-84 | 3.5 |
| 75-79 | 3.0 |
| 70-74 | 2.5 |
| 65-69 | 2.0 |
| 60-64 | 1.5 |
| 0-59 | 0.0 |

## 测试覆盖

30 个测试用例，覆盖：
- GPA 计算（4.0/5.0制）
- 成绩转换（百分制/字母/中文）
- 学分绩点计算
- 成绩分析统计
- 趋势预测
- 边界值处理

## 许可证

MIT License
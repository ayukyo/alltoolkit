# Stable Marriage Utils

稳定婚姻问题（Gale-Shapley 算法）工具库，包含多种稳定匹配算法的实现。

## 功能概述

本模块实现了三种经典的稳定匹配算法：

### 1. Stable Marriage Problem（稳定婚姻问题）
- **Gale-Shapley 算法** - O(n²) 时间复杂度
- 保证产生稳定匹配（不存在阻塞配对）
- 支持求解男性最优和女性最优匹配
- 验证匹配稳定性
- 计算满意度指标
- 查找所有可能的稳定匹配

### 2. Stable Roommates Problem（稳定室友问题）
- **Irving 算法** - O(n²) 时间复杂度
- 单边匹配问题（所有人互相匹配）
- 注意：某些情况可能无稳定解

### 3. Hospital/Residents Problem（医院/居民问题）
- 多对一匹配问题
- 支持容量限制
- 居民最优和医院最优版本
- 应用于医学院匹配、大学录取等场景

## 安装使用

```python
from stable_marriage_utils.mod import (
    StableMarriage, StableRoommates, HospitalResidents,
    stable_marriage, stable_roommates, hospital_residents
)
```

## 快速示例

### 稳定婚姻问题

```python
# 定义偏好列表
men = {
    'A': ['Y', 'X', 'Z'],
    'B': ['X', 'Y', 'Z'],
    'C': ['Y', 'X', 'Z']
}
women = {
    'X': ['A', 'B', 'C'],
    'Y': ['B', 'A', 'C'],
    'Z': ['A', 'B', 'C']
}

# 求解
sm = StableMarriage(men, women)
result = sm.solve()  # {'A': 'Y', 'B': 'X', 'C': 'Z'}

# 验证稳定性
sm.is_stable(result)  # True

# 计算满意度
satisfaction = sm.calculate_satisfaction(result)
```

### 大学录取匹配

```python
students = {
    'S1': ['MIT', 'Stanford', 'Berkeley'],
    'S2': ['Stanford', 'MIT', 'Berkeley'],
    'S3': ['Berkeley', 'MIT', 'Stanford']
}
colleges = {
    'MIT': (2, ['S1', 'S2', 'S3']),      # 容量 2
    'Stanford': (1, ['S2', 'S1', 'S3']), # 容量 1
    'Berkeley': (1, ['S3', 'S1', 'S2'])  # 容量 1
}

hr = HospitalResidents(students, colleges)
result = hr.solve()
```

### 稳定室友问题

```python
preferences = {
    'A': ['B', 'C', 'D'],
    'B': ['A', 'D', 'C'],
    'C': ['D', 'A', 'B'],
    'D': ['C', 'B', 'A']
}

sr = StableRoommates(preferences)
result = sr.solve()  # {'A': 'B', 'B': 'A', 'C': 'D', 'D': 'C'}
```

## API 文档

### StableMarriage 类

| 方法 | 说明 |
|------|------|
| `solve()` | 求解男性最优稳定匹配 |
| `solve_women_optimal()` | 求解女性最优稳定匹配 |
| `is_stable(matching)` | 验证匹配是否稳定 |
| `find_blocking_pairs(matching)` | 查找阻塞配对 |
| `calculate_satisfaction(matching)` | 计算满意度指标 |
| `count_stable_matchings()` | 计算稳定匹配数量（小规模） |
| `find_all_stable_matchings()` | 查找所有稳定匹配（小规模） |

### StableRoommates 类

| 方法 | 说明 |
|------|------|
| `solve()` | 求解稳定室友匹配，无解返回 None |
| `is_stable(matching)` | 验证匹配是否稳定 |

### HospitalResidents 类

| 方法 | 说明 |
|------|------|
| `solve()` | 居民最优匹配（居民提出申请） |
| `solve_hospital_optimal()` | 医院最优匹配（医院发出邀请） |
| `is_stable(matching)` | 验证匹配是否稳定 |

## 应用场景

- 🎓 大学录取匹配系统
- 🏥 医学院住院医师匹配（NRMP）
- 💼 求职招聘匹配
- 🏠 宿舍室友分配
- 🎮 游戏配对系统
- 📊 资源分配优化

## 理论背景

### Gale-Shapley 算法（1962）

由 David Gale 和 Lloyd Shapley 发明，解决稳定婚姻问题：
1. 所有男性依次向偏好女性提出申请
2. 女性接受或拒绝申请（保留最优者）
3. 被拒绝的男性继续向下一偏好提出申请
4. 直到所有人匹配完毕

**关键性质**：
- 保证产生稳定匹配
- 男性最优：每个男性获得所有稳定匹配中最好的伴侣
- 女性最优：每个女性获得所有稳定匹配中最好的伴侣

### Irving 算法（1985）

解决稳定室友问题：
- 两阶段算法：第一阶段建立初步匹配，第二阶段消除循环
- 注意：不是所有偏好配置都有稳定解

## 参考文献

- Gale, D. and Shapley, L. S. (1962). "College Admissions and the Stability of Marriage"
- Irving, R. W. (1985). "An Efficient Algorithm for the 'Stable Roommates' Problem"
- National Resident Matching Program (NRMP)

## 测试

```bash
python stable_marriage_utils_test.py
```

## 示例

```bash
python examples/usage_examples.py
```

---

**作者**: AllToolkit 自动化开发系统
**日期**: 2026-05-26
**版本**: 1.0.0
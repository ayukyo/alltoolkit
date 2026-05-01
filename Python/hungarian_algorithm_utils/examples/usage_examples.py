"""
匈牙利算法使用示例

展示如何使用 Hungarian Algorithm 解决各种分配问题
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from hungarian_algorithm_utils.mod import (
    hungarian,
    solve_assignment,
    max_weight_matching,
    rectangular_assignment,
    AssignmentProblem
)


def example_basic_usage():
    """基本用法示例"""
    print("=" * 60)
    print("示例 1: 基本用法 - 任务分配")
    print("=" * 60)
    
    # 3 个工人，3 个任务
    # cost_matrix[i][j] = 工人 i 完成任务 j 的成本
    cost_matrix = [
        [4, 1, 3],  # 工人 0 的成本
        [2, 0, 5],  # 工人 1 的成本
        [3, 2, 2]   # 工人 2 的成本
    ]
    
    print("\n成本矩阵:")
    print("        任务0  任务1  任务2")
    for i, row in enumerate(cost_matrix):
        print(f"工人{i}:   {row}")
    
    # 求解
    assignment, total_cost = hungarian(cost_matrix)
    
    print(f"\n最优分配方案:")
    for worker, task in assignment:
        cost = cost_matrix[worker][task]
        print(f"  工人{worker} -> 任务{task} (成本: {cost})")
    
    print(f"\n总成本: {total_cost}")
    print()


def example_job_assignment():
    """工作分配示例"""
    print("=" * 60)
    print("示例 2: 公司项目分配")
    print("=" * 60)
    
    workers = ["张三", "李四", "王五", "赵六"]
    projects = ["项目A", "项目B", "项目C", "项目D"]
    
    # 每个工人完成每个项目所需的天数
    days_matrix = [
        [14, 5, 8, 7],   # 张三
        [2, 12, 6, 5],   # 李四
        [7, 8, 3, 9],    # 王五
        [2, 4, 6, 10]    # 赵六
    ]
    
    print("\n完成项目所需天数:")
    print("         ", end="")
    for p in projects:
        print(f"{p:8s}", end="")
    print()
    
    for i, name in enumerate(workers):
        print(f"{name:8s}", end="")
        for d in days_matrix[i]:
            print(f"{d:8d}", end="")
        print()
    
    assignment, total_days = hungarian(days_matrix)
    
    print(f"\n最优分配方案:")
    for worker_idx, project_idx in assignment:
        days = days_matrix[worker_idx][project_idx]
        print(f"  {workers[worker_idx]} -> {projects[project_idx]} ({days}天)")
    
    print(f"\n总天数: {total_days}天")
    print()


def example_max_weight():
    """最大权重匹配示例"""
    print("=" * 60)
    print("示例 3: 效率最大化 - 最大化总产出")
    print("=" * 60)
    
    # 机器生产不同产品的效率（每小时产量）
    machines = ["机器A", "机器B", "机器C"]
    products = ["产品X", "产品Y", "产品Z"]
    
    efficiency_matrix = [
        [10, 15, 8],   # 机器A
        [12, 10, 14],  # 机器B
        [8, 11, 13]    # 机器C
    ]
    
    print("\n生产效率（每小时产量）:")
    print("         ", end="")
    for p in products:
        print(f"{p:8s}", end="")
    print()
    
    for i, m in enumerate(machines):
        print(f"{m:8s}", end="")
        for e in efficiency_matrix[i]:
            print(f"{e:8d}", end="")
        print()
    
    assignment, total_efficiency = max_weight_matching(efficiency_matrix)
    
    print(f"\n最优分配方案（最大化效率）:")
    for machine_idx, product_idx in assignment:
        eff = efficiency_matrix[machine_idx][product_idx]
        print(f"  {machines[machine_idx]} -> {products[product_idx]} (效率: {eff}/小时)")
    
    print(f"\n总效率: {total_efficiency}/小时")
    print()


def example_rectangular():
    """非方阵分配示例"""
    print("=" * 60)
    print("示例 4: 工人数 ≠ 任务数")
    print("=" * 60)
    
    workers = ["程序员A", "程序员B"]
    tasks = ["前端", "后端", "测试", "运维"]
    
    # 程序员对不同任务的熟练度分数（越低越好，表示需要的时间）
    cost_matrix = [
        [2, 5, 3, 8],  # 程序员A
        [6, 3, 4, 5]   # 程序员B
    ]
    
    print("\n任务成本矩阵:")
    print("         ", end="")
    for t in tasks:
        print(f"{t:6s}", end="")
    print()
    
    for i, w in enumerate(workers):
        print(f"{w:10s}", end="")
        for c in cost_matrix[i]:
            print(f"{c:6d}", end="")
        print()
    
    assignment = rectangular_assignment(cost_matrix)
    
    print(f"\n分配方案（每个程序员最多做一项任务）:")
    total_cost = 0
    for worker_idx, task_idx in assignment:
        cost = cost_matrix[worker_idx][task_idx]
        total_cost += cost
        print(f"  {workers[worker_idx]} -> {tasks[task_idx]} (成本: {cost})")
    
    print(f"\n总成本: {total_cost}")
    print(f"注: {len(tasks) - len(workers)} 个任务未被分配")
    print()


def example_assignment_problem_class():
    """使用 AssignmentProblem 类"""
    print("=" * 60)
    print("示例 5: 使用 AssignmentProblem 类（更友好的 API）")
    print("=" * 60)
    
    # 创建分配问题
    problem = AssignmentProblem()
    
    # 添加工人
    for name in ["小明", "小红", "小刚"]:
        problem.add_worker(name)
    
    # 添加任务
    for task in ["打扫", "做饭", "洗衣"]:
        problem.add_task(task)
    
    # 设置成本（时间/小时）
    costs = [
        [2, 3, 1.5],  # 小明
        [2.5, 2, 2],  # 小红
        [1.5, 4, 1]   # 小刚
    ]
    
    print("\n家务成本矩阵（小时）:")
    for i, worker in enumerate(["小明", "小红", "小刚"]):
        print(f"  {worker}: 打扫={costs[i][0]}h, 做饭={costs[i][1]}h, 洗衣={costs[i][2]}h")
    
    for i, row in enumerate(costs):
        for j, cost in enumerate(row):
            problem.set_cost(i, j, cost)
    
    # 求解
    result = problem.solve()
    
    print(f"\n最优分配方案:")
    total_hours = 0
    for worker, task, cost in result:
        print(f"  {worker} -> {task} ({cost}小时)")
        total_hours += cost
    
    print(f"\n总时间: {total_hours}小时")
    print()


def example_sports_team():
    """体育团队位置分配"""
    print("=" * 60)
    print("示例 6: 篮球队位置分配")
    print("=" * 60)
    
    players = ["球员A", "球员B", "球员C", "球员C", "球员E"]
    positions = ["控球后卫", "得分后卫", "小前锋", "大前锋", "中锋"]
    
    # 每个球员在每个位置的评分（1-10，越高越好）
    ratings = [
        [9, 8, 5, 3, 2],   # 球员A 擅长后卫
        [7, 9, 6, 4, 3],   # 球员B 擅长得分后卫
        [5, 6, 8, 7, 6],   # 球员C 比较全面
        [3, 4, 6, 8, 8],   # 球员D 擅长内线
        [2, 3, 5, 6, 9]    # 球员E 擅长中锋
    ]
    
    print("\n球员评分矩阵（越高越好）:")
    print("         ", end="")
    for p in positions:
        print(f"{p:8s}", end="")
    print()
    
    for i, name in enumerate(players):
        print(f"{name:8s}", end="")
        for r in ratings[i]:
            print(f"{r:8d}", end="")
        print()
    
    # 转换为成本（10-评分，因为 hungarian 最小化）
    cost_matrix = [[10 - r for r in row] for row in ratings]
    
    assignment, _ = hungarian(cost_matrix)
    
    print(f"\n最优位置分配:")
    total_rating = 0
    for player_idx, position_idx in assignment:
        rating = ratings[player_idx][position_idx]
        total_rating += rating
        print(f"  {players[player_idx]} -> {positions[position_idx]} (评分: {rating})")
    
    print(f"\n团队总评分: {total_rating}/50")
    print()


def main():
    """运行所有示例"""
    example_basic_usage()
    example_job_assignment()
    example_max_weight()
    example_rectangular()
    example_assignment_problem_class()
    example_sports_team()
    
    print("=" * 60)
    print("所有示例运行完成!")
    print("=" * 60)


if __name__ == "__main__":
    main()
"""
背包问题工具模块使用示例

展示各种背包问题的求解方法和实际应用场景
"""

import sys
sys.path.insert(0, '..')

from mod import (
    Item,
    KnapsackMethod,
    knapsack_01,
    knapsack_complete,
    knapsack_multiple,
    knapsack_fractional,
    knapsack_multi_dim,
    knapsack_multi_objective,
    knapsack_subset_sum,
    knapsack_min_items,
    knapsack_all_solutions,
    unbounded_knapsack,
    bounded_knapsack
)


def example_01_basic_knapsack():
    """示例1: 基本 0/1 背包问题"""
    print("\n=== 示例1: 基本 0/1 背包问题 ===")
    
    # 定义物品
    items = [
        Item(weight=10, value=60, name="书籍"),
        Item(weight=20, value=100, name="笔记本电脑"),
        Item(weight=30, value=120, name="相机"),
        Item(weight=5, value=50, name="耳机"),
        Item(weight=15, value=70, name="平板电脑")
    ]
    
    print("物品列表:")
    for item in items:
        print(f"  {item.name}: 重量={item.weight}, 价值={item.value}, 密度={item.ratio:.2f}")
    
    capacity = 50
    print(f"\n背包容量: {capacity}")
    
    # 使用不同方法求解
    print("\n--- 使用动态规划求解 ---")
    result = knapsack_01(items, capacity, KnapsackMethod.DP)
    print(f"最大价值: {result.max_value}")
    print(f"总重量: {result.total_weight}")
    print(f"选中物品: {', '.join([i.name for i in result.selected_items])}")
    
    print("\n--- 使用分支限界法求解 ---")
    result = knapsack_01(items, capacity, KnapsackMethod.BRANCH_BOUND)
    print(f"最大价值: {result.max_value}")
    print(f"选中物品: {', '.join([i.name for i in result.selected_items])}")


def example_02_complete_knapsack():
    """示例2: 完全背包问题（物品可选无限次）"""
    print("\n=== 示例2: 完全背包问题 ===")
    
    # 投资场景：可以多次购买同一种投资产品
    investments = [
        Item(weight=1, value=1.5, name="短期债券"),   # 每单位成本1，收益1.5
        Item(weight=3, value=4, name="中期基金"),      # 每单位成本3，收益4
        Item(weight=4, value=5.5, name="长期股票")     # 每单位成本4，收益5.5
    ]
    
    print("投资产品:")
    for inv in investments:
        print(f"  {inv.name}: 成本={inv.weight}, 收益={inv.value}, 收益率={inv.ratio:.2f}")
    
    budget = 10  # 预算10单位
    print(f"\n预算: {budget}")
    
    result = knapsack_complete(investments, budget)
    print(f"\n最大收益: {result.max_value}")
    print(f"总投资: {result.total_weight}")
    
    # 统计每种产品购买次数
    purchase_counts = {}
    for item in result.selected_items:
        purchase_counts[item.name] = purchase_counts.get(item.name, 0) + 1
    
    print("购买方案:")
    for name, count in purchase_counts.items():
        print(f"  {name}: {count}份")


def example_03_multiple_knapsack():
    """示例3: 多重背包问题（物品数量有限）"""
    print("\n=== 示例3: 多重背包问题 ===")
    
    # 超市购物场景：每种商品有库存限制
    products = [
        Item(weight=2, value=3, name="苹果", count=5),
        Item(weight=3, value=5, name="牛奶", count=3),
        Item(weight=1, value=2, name="面包", count=10),
        Item(weight=5, value=8, name="肉类", count=2)
    ]
    
    print("商品列表:")
    for p in products:
        print(f"  {p.name}: 重量={p.weight}, 价值={p.value}, 库存={p.count}")
    
    bag_capacity = 15
    print(f"\n购物袋容量: {bag_capacity}")
    
    result = knapsack_multiple(products, bag_capacity)
    print(f"\n最大价值: {result.max_value}")
    print(f"总重量: {result.total_weight}")
    
    # 统计购买数量
    purchase_counts = {}
    for item in result.selected_items:
        purchase_counts[item.name] = purchase_counts.get(item.name, 0) + 1
    
    print("购物清单:")
    for name, count in purchase_counts.items():
        print(f"  {name}: {count}个")


def example_04_fractional_knapsack():
    """示例4: 分数背包问题（可以取物品的一部分）"""
    print("\n=== 示例4: 分数背包问题 ===")
    
    # 装货场景：可以装载货物的一部分
    cargo = [
        Item(weight=50, value=100, name="金矿"),
        Item(weight=30, value=60, name="银矿"),
        Item(weight=20, value=40, name="铜矿")
    ]
    
    print("货物:")
    for c in cargo:
        print(f"  {c.name}: 重量={c.weight}吨, 价值={c.value}万, 单价={c.ratio:.2f}万/吨")
    
    truck_capacity = 60  # 卡车容量60吨
    print(f"\n卡车容量: {truck_capacity}吨")
    
    value, weight, selected = knapsack_fractional(cargo, truck_capacity)
    
    print(f"\n最大价值: {value}万")
    print(f"装载重量: {weight}吨")
    print("\n装载方案:")
    for item, fraction in selected:
        loaded = item.weight * fraction
        print(f"  {item.name}: {loaded:.1f}吨 ({fraction:.1%})")


def example_05_subset_sum():
    """示例5: 子集和问题"""
    print("\n=== 示例5: 子集和问题 ===")
    
    # 找零问题：找出等于目标金额的硬币组合
    coins = [Item(weight=1, value=1, name="1元"),
             Item(weight=2, value=2, name="2元"),
             Item(weight=5, value=5, name="5元"),
             Item(weight=10, value=10, name="10元")]
    
    target = 17  # 需要17元
    
    print(f"可用硬币: {[c.name for c in coins]}")
    print(f"目标金额: {target}元")
    
    found, indices = knapsack_subset_sum(coins, target)
    
    if found:
        print(f"\n找到组合!")
        print("使用的硬币:")
        for i in indices:
            print(f"  {coins[i].name}")
        print(f"总额: {sum(coins[i].weight for i in indices)}元")
    else:
        print("\n无法凑出目标金额")


def example_06_multi_objective():
    """示例6: 多目标背包问题"""
    print("\n=== 示例6: 多目标背包问题 ===")
    
    # 同时考虑价值和重量
    items = [
        Item(weight=2, value=100, name="高价值物品A"),
        Item(weight=10, value=150, name="中等物品B"),
        Item(weight=5, value=80, name="轻物品C"),
        Item(weight=8, value=120, name="平衡物品D")
    ]
    
    print("物品:")
    for item in items:
        print(f"  {item.name}: 重量={item.weight}, 价值={item.value}")
    
    capacity = 20
    print(f"\n容量: {capacity}")
    
    # 寻找帕累托最优解
    pareto_front = knapsack_multi_objective(items, capacity)
    
    print("\n帕累托最优解（价值vs重量权衡）:")
    print("-" * 50)
    for result in pareto_front:
        print(f"价值: {result.max_value:.1f}, 重量: {result.total_weight:.1f}")
        print(f"物品: {', '.join([i.name for i in result.selected_items])}")
        print("-" * 50)


def example_07_all_solutions():
    """示例7: 找出所有最优解"""
    print("\n=== 示例7: 找出所有最优解 ===")
    
    # 当有多种选择方案时，找出所有最优解
    items = [
        Item(weight=5, value=10, name="物品A"),
        Item(weight=5, value=10, name="物品B"),
        Item(weight=5, value=10, name="物品C"),
        Item(weight=5, value=10, name="物品D")
    ]
    
    print("物品（所有物品重量和价值相同）:")
    for item in items:
        print(f"  {item.name}: 重量={item.weight}, 价值={item.value}")
    
    capacity = 10
    print(f"\n容量: {capacity}（可以选2个物品）")
    
    solutions = knapsack_all_solutions(items, capacity, max_solutions=10)
    
    print(f"\n找到 {len(solutions)} 个最优解:")
    for i, sol in enumerate(solutions):
        print(f"\n方案{i+1}:")
        print(f"  物品: {', '.join([i.name for i in sol.selected_items])}")


def example_08_min_items():
    """示例8: 最小物品数背包"""
    print("\n=== 示例8: 最小物品数背包 ===")
    
    # 追求用最少物品达到最小价值要求
    items = [
        Item(weight=10, value=100, name="大物品A"),
        Item(weight=5, value=50, name="中物品B"),
        Item(weight=2, value=20, name="小物品C"),
        Item(weight=1, value=10, name="微物品D")
    ]
    
    print("物品:")
    for item in items:
        print(f"  {item.name}: 重量={item.weight}, 价值={item.value}")
    
    capacity = 30
    min_value = 100
    
    print(f"\n容量: {capacity}, 最小价值要求: {min_value}")
    
    result = knapsack_min_items(items, capacity, min_value)
    
    if result:
        print(f"\n找到满足条件的最少物品方案:")
        print(f"物品数量: {len(result.selected_items)}")
        print(f"总价值: {result.max_value}")
        print(f"总重量: {result.total_weight}")
        print(f"选中物品: {', '.join([i.name for i in result.selected_items])}")
    else:
        print("\n无法满足最小价值要求")


def example_09_resource_allocation():
    """示例9: 实际应用 - 项目资源分配"""
    print("\n=== 示例9: 项目资源分配 ===")
    
    # 公司预算分配给不同项目
    projects = [
        Item(weight=100, value=150, name="研发项目"),
        Item(weight=80, value=120, name="市场推广"),
        Item(weight=50, value=70, name="基础设施"),
        Item(weight=30, value=40, name="员工培训"),
        Item(weight=20, value=25, name="办公设备")
    ]
    
    print("项目列表:")
    for p in projects:
        print(f"  {p.name}: 预算={p.weight}万, ROI={p.value}万")
    
    total_budget = 200
    print(f"\n总预算: {total_budget}万")
    
    result = knapsack_01(projects, total_budget)
    
    print(f"\n最优分配方案:")
    print(f"预计总收益: {result.max_value}万")
    print(f"使用预算: {result.total_weight}万")
    print("\n投资的项目:")
    for item in result.selected_items:
        print(f"  {item.name}: 预算{item.weight}万, 预期收益{item.value}万")


def example_10_vending_machine():
    """示例10: 实际应用 - 自动售货机填充"""
    print("\n=== 示例10: 自动售货机填充 ===")
    
    # 填充售货机，最大化利润
    # 每种商品有库存限制
    snacks = [
        Item(weight=2, value=3, name="薯片", count=50),
        Item(weight=1, value=2, name="糖果", count=100),
        Item(weight=3, value=4, name="饼干", count=30),
        Item(weight=2, value=5, name="巧克力", count=20),
        Item(weight=4, value=6, name="坚果", count=15)
    ]
    
    print("零食列表:")
    for s in snacks:
        print(f"  {s.name}: 占位={s.weight}, 利润={s.value}, 库存={s.count}")
    
    shelf_space = 50  # 货架空间（格子数）
    print(f"\n货架空间: {shelf_space}")
    
    result = knapsack_multiple(snacks, shelf_space)
    
    print(f"\n最优填充方案:")
    print(f"预计利润: {result.max_value}")
    print(f"使用空间: {result.total_weight}")
    
    # 统计每种商品数量
    snack_counts = {}
    for item in result.selected_items:
        snack_counts[item.name] = snack_counts.get(item.name, 0) + 1
    
    print("\n填充数量:")
    for name, count in snack_counts.items():
        print(f"  {name}: {count}个")


def main():
    """运行所有示例"""
    print("=" * 60)
    print("背包问题工具模块 - 使用示例")
    print("=" * 60)
    
    example_01_basic_knapsack()
    example_02_complete_knapsack()
    example_03_multiple_knapsack()
    example_04_fractional_knapsack()
    example_05_subset_sum()
    example_06_multi_objective()
    example_07_all_solutions()
    example_08_min_items()
    example_09_resource_allocation()
    example_10_vending_machine()
    
    print("\n" + "=" * 60)
    print("所有示例完成!")
    print("=" * 60)


if __name__ == "__main__":
    main()
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Inventory Utils Test - 库存管理工具测试

测试模块：inventory_utils
测试用例数：50+
测试覆盖：库存项管理、安全库存、再订货点、EOQ、ABC分析、周转率、统计
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    InventoryManager, InventoryItem, InventorySummary,
    StockStatus, ABCClass,
    create_inventory_manager,
    calculate_reorder_point, calculate_safety_stock, calculate_eoq,
    classify_inventory
)
from datetime import datetime, timedelta


def test_result_collector():
    """测试结果收集器"""
    results = []
    
    def add_result(test_name: str, passed: bool, message: str = ""):
        results.append({
            "name": test_name,
            "passed": passed,
            "message": message
        })
    
    return results, add_result


def test_inventory_item(results, add_result):
    """测试库存项"""
    item = InventoryItem(
        sku="SKU001",
        name="Widget",
        current_stock=100,
        unit_cost=10.0,
        unit_price=15.0,
        lead_time_days=7,
        daily_demand_avg=5.0
    )
    
    # test 1: 基础属性
    add_result("InventoryItem basic", 
               item.sku == "SKU001" and item.name == "Widget")
    
    # test 2: stock_value
    add_result("InventoryItem stock_value", 
               item.stock_value == 1000.0, f"Expected 1000, got {item.stock_value}")
    
    # test 3: potential_revenue
    add_result("InventoryItem potential_revenue", 
               item.potential_revenue == 1500.0, f"Expected 1500, got {item.potential_revenue}")
    
    # test 4: profit_margin
    expected_margin = ((15 - 10) / 10) * 100  # 50%
    add_result("InventoryItem profit_margin", 
               abs(item.profit_margin - expected_margin) < 0.1, 
               f"Expected {expected_margin}, got {item.profit_margin}")
    
    # test 5: 零成本利润率
    item_zero_cost = InventoryItem(
        sku="SKU002",
        name="Free Item",
        current_stock=10,
        unit_cost=0,
        unit_price=0
    )
    add_result("InventoryItem zero cost margin", item_zero_cost.profit_margin == 0)


def test_inventory_manager(results, add_result):
    """测试库存管理器"""
    manager = InventoryManager()
    
    item = InventoryItem(
        sku="SKU001",
        name="Widget",
        current_stock=100,
        unit_cost=10.0,
        unit_price=15.0
    )
    
    # test 6: 添加项
    manager.add_item(item)
    add_result("InventoryManager add_item", len(manager.items) == 1)
    
    # test 7: 获取项
    retrieved = manager.get_item("SKU001")
    add_result("InventoryManager get_item", retrieved == item)
    
    # test 8: 移除项
    removed = manager.remove_item("SKU001")
    add_result("InventoryManager remove_item", removed and len(manager.items) == 0)
    
    # test 9: 移除不存在项
    removed_again = manager.remove_item("SKU001")
    add_result("InventoryManager remove nonexistent", not removed_again)
    
    # test 10: 获取不存在项
    nonexistent = manager.get_item("SKU999")
    add_result("InventoryManager get nonexistent", nonexistent is None)


def test_update_stock(results, add_result):
    """测试库存更新"""
    manager = InventoryManager()
    item = InventoryItem(
        sku="SKU001",
        name="Widget",
        current_stock=100,
        unit_cost=10.0,
        unit_price=15.0
    )
    manager.add_item(item)
    
    # test 11: 减少库存
    manager.update_stock("SKU001", -10)
    add_result("update_stock decrease", 
               manager.get_item("SKU001").current_stock == 90)
    
    # test 12: 增加库存
    manager.update_stock("SKU001", 20)
    add_result("update_stock increase", 
               manager.get_item("SKU001").current_stock == 110)
    
    # test 13: 更新不存在项
    updated = manager.update_stock("SKU999", 10)
    add_result("update_stock nonexistent", not updated)


def test_safety_stock(results, add_result):
    """测试安全库存计算"""
    manager = InventoryManager(service_level=0.95)
    
    item = InventoryItem(
        sku="SKU001",
        name="Widget",
        current_stock=100,
        unit_cost=10.0,
        unit_price=15.0,
        lead_time_days=7,
        daily_demand_std=2.0
    )
    manager.add_item(item)
    
    # test 14: 安全库存计算
    safety = manager.calculate_safety_stock("SKU001")
    add_result("calculate_safety_stock", safety > 0, f"Expected positive, got {safety}")
    
    # test 15: 不存在项异常
    try:
        manager.calculate_safety_stock("SKU999")
        add_result("calculate_safety_stock nonexistent exception", False, "Should raise ValueError")
    except ValueError:
        add_result("calculate_safety_stock nonexistent exception", True)
    
    # test 16: 便捷函数
    quick_safety = calculate_safety_stock(2.0, 7, 0.95)
    add_result("calculate_safety_stock convenience", quick_safety > 0)


def test_reorder_point(results, add_result):
    """测试再订货点计算"""
    manager = InventoryManager()
    
    item = InventoryItem(
        sku="SKU001",
        name="Widget",
        current_stock=100,
        unit_cost=10.0,
        unit_price=15.0,
        lead_time_days=7,
        daily_demand_avg=5.0,
        daily_demand_std=2.0
    )
    manager.add_item(item)
    
    # test 17: 再订货点计算
    rop = manager.calculate_reorder_point("SKU001")
    expected_min = 5 * 7  # 35 (demand * lead time)
    add_result("calculate_reorder_point", rop >= expected_min, 
               f"Expected >= {expected_min}, got {rop}")
    
    # test 18: 便捷函数
    quick_rop = calculate_reorder_point(5.0, 7, 10)
    add_result("calculate_reorder_point convenience", quick_rop == 45)


def test_eoq(results, add_result):
    """测试 EOQ 计算"""
    manager = InventoryManager()
    
    item = InventoryItem(
        sku="SKU001",
        name="Widget",
        current_stock=100,
        unit_cost=10.0,
        unit_price=15.0,
        daily_demand_avg=10.0  # 3650 per year
    )
    manager.add_item(item)
    
    # test 19: EOQ 计算
    eoq = manager.calculate_eoq("SKU001", ordering_cost=50, holding_cost_rate=0.25)
    add_result("calculate_eoq", eoq > 0, f"Expected positive, got {eoq}")
    
    # test 20: EOQ 便捷函数
    quick_eoq = calculate_eoq(3650, 50, 10, 0.25)
    add_result("calculate_eoq convenience", quick_eoq > 0)


def test_stock_status(results, add_result):
    """测试库存状态"""
    manager = InventoryManager()
    
    item = InventoryItem(
        sku="SKU001",
        name="Widget",
        current_stock=100,
        unit_cost=10.0,
        unit_price=15.0,
        lead_time_days=7,
        daily_demand_avg=5.0,
        daily_demand_std=2.0
    )
    manager.add_item(item)
    
    # test 21: 正常状态
    status = manager.get_stock_status("SKU001")
    add_result("get_stock_status normal", status == StockStatus.NORMAL)
    
    # test 22: 低库存状态
    manager.update_stock("SKU001", -70)  # 30 remaining
    status_low = manager.get_stock_status("SKU001")
    add_result("get_stock_status low", 
               status_low in [StockStatus.LOW, StockStatus.CRITICAL])
    
    # test 23: 过量库存状态
    item_overstocked = InventoryItem(
        sku="SKU002",
        name="Overstocked",
        current_stock=1000,
        unit_cost=10.0,
        unit_price=15.0,
        daily_demand_avg=5.0,
        max_stock=500
    )
    manager.add_item(item_overstocked)
    status_over = manager.get_stock_status("SKU002")
    add_result("get_stock_status overstocked", status_over == StockStatus.OVERSTOCKED)


def test_abc_analysis(results, add_result):
    """测试 ABC 分析"""
    manager = InventoryManager()
    
    # 添加多个不同价值的项
    items_data = [
        {"sku": "A001", "value": 10000},
        {"sku": "A002", "value": 8000},
        {"sku": "B001", "value": 1000},
        {"sku": "B002", "value": 800},
        {"sku": "C001", "value": 100},
        {"sku": "C002", "value": 50},
    ]
    
    for data in items_data:
        item = InventoryItem(
            sku=data["sku"],
            name=f"Item {data['sku']}",
            current_stock=data["value"] / 10,  # Assume unit_cost = 10
            unit_cost=10.0,
            unit_price=15.0
        )
        manager.add_item(item)
    
    # test 24: ABC 分析
    classifications = manager.abc_analysis()
    add_result("abc_analysis", len(classifications) == 6)
    
    # test 25: A 类包含高价值项
    add_result("abc_analysis A class", 
               classifications.get("A001") == ABCClass.A or classifications.get("A002") == ABCClass.A)
    
    # test 26: 便捷函数
    items_for_classify = [{"sku": f"SKU{i}", "value": 1000 - i*100} for i in range(10)]
    quick_class = classify_inventory(items_for_classify)
    add_result("classify_inventory convenience", len(quick_class) == 10)


def test_turnover(results, add_result):
    """测试周转率"""
    manager = InventoryManager()
    
    item = InventoryItem(
        sku="SKU001",
        name="Widget",
        current_stock=100,
        unit_cost=10.0,
        unit_price=15.0,
        daily_demand_avg=10.0
    )
    manager.add_item(item)
    
    # test 27: 周转率计算
    turnover = manager.calculate_turnover("SKU001")
    add_result("calculate_turnover", turnover > 0, f"Expected positive, got {turnover}")
    
    # test 28: 零库存周转率
    item_zero = InventoryItem(
        sku="SKU002",
        name="Zero Stock",
        current_stock=0,
        unit_cost=10.0,
        unit_price=15.0,
        daily_demand_avg=5.0
    )
    manager.add_item(item_zero)
    turnover_zero = manager.calculate_turnover("SKU002")
    add_result("calculate_turnover zero stock", turnover_zero == 0)


def test_days_of_stock(results, add_result):
    """测试库存天数"""
    manager = InventoryManager()
    
    item = InventoryItem(
        sku="SKU001",
        name="Widget",
        current_stock=100,
        unit_cost=10.0,
        unit_price=15.0,
        daily_demand_avg=5.0
    )
    manager.add_item(item)
    
    # test 29: 库存天数计算
    days = manager.calculate_days_of_stock("SKU001")
    expected = 100 / 5  # 20 days
    add_result("calculate_days_of_stock", days == 20, f"Expected 20, got {days}")
    
    # test 30: 零需求无限天数
    item_no_demand = InventoryItem(
        sku="SKU002",
        name="No Demand",
        current_stock=50,
        unit_cost=10.0,
        unit_price=15.0,
        daily_demand_avg=0
    )
    manager.add_item(item_no_demand)
    days_infinite = manager.calculate_days_of_stock("SKU002")
    add_result("calculate_days_of_stock no demand", days_infinite == float('inf'))


def test_stockout_risk(results, add_result):
    """测试缺货风险"""
    manager = InventoryManager()
    
    item = InventoryItem(
        sku="SKU001",
        name="Widget",
        current_stock=100,
        unit_cost=10.0,
        unit_price=15.0,
        daily_demand_avg=5.0,
        daily_demand_std=2.0
    )
    manager.add_item(item)
    
    # test 31: 缺货风险计算
    risk = manager.calculate_stockout_risk("SKU001", days_ahead=30)
    add_result("calculate_stockout_risk", 0 <= risk <= 1, f"Expected 0-1, got {risk}")
    
    # test 32: 低库存高风险
    manager.update_stock("SKU001", -80)  # 20 remaining
    risk_high = manager.calculate_stockout_risk("SKU001", days_ahead=30)
    add_result("calculate_stockout_risk low stock", risk_high > 0.5)


def test_restock_recommendations(results, add_result):
    """测试补货建议"""
    manager = InventoryManager()
    
    item = InventoryItem(
        sku="SKU001",
        name="Widget",
        current_stock=20,  # Low stock
        unit_cost=10.0,
        unit_price=15.0,
        lead_time_days=7,
        daily_demand_avg=5.0,
        daily_demand_std=2.0
    )
    manager.add_item(item)
    
    # test 33: 补货建议
    recommendations = manager.get_restock_recommendations()
    add_result("get_restock_recommendations", len(recommendations) > 0)
    
    # test 34: 建议包含 SKU
    add_result("get_restock_recommendations contains sku", 
               any(r["sku"] == "SKU001" for r in recommendations))


def test_summary(results, add_result):
    """测试库存汇总"""
    manager = InventoryManager()
    
    items = [
        InventoryItem(sku="SKU001", name="Item1", current_stock=100, unit_cost=10, unit_price=15, daily_demand_avg=5),
        InventoryItem(sku="SKU002", name="Item2", current_stock=50, unit_cost=20, unit_price=30, daily_demand_avg=3),
        InventoryItem(sku="SKU003", name="Item3", current_stock=200, unit_cost=5, unit_price=8, daily_demand_avg=10),
    ]
    
    for item in items:
        manager.add_item(item)
    
    summary = manager.get_summary()
    
    # test 35: 总项数
    add_result("get_summary total_items", summary.total_items == 3)
    
    # test 36: 总库存价值
    expected_value = 100*10 + 50*20 + 200*5  # 1000 + 1000 + 1000 = 3000
    add_result("get_summary total_stock_value", 
               summary.total_stock_value == expected_value)
    
    # test 37: 转换为字典
    summary_dict = summary.to_dict()
    add_result("InventorySummary to_dict", 
               summary_dict["total_items"] == 3)


def test_carrying_cost(results, add_result):
    """测试持有成本"""
    manager = InventoryManager()
    
    item = InventoryItem(
        sku="SKU001",
        name="Widget",
        current_stock=100,
        unit_cost=10.0,
        unit_price=15.0
    )
    manager.add_item(item)
    
    # test 38: 持有成本计算
    costs = manager.calculate_carrying_cost("SKU001", holding_cost_rate=0.25)
    add_result("calculate_carrying_cost", costs["annual_carrying_cost"] > 0)
    
    # test 39: 单位持有成本
    expected_per_unit = 10 * 0.25  # 2.5
    add_result("calculate_carrying_cost per unit", 
               costs["cost_per_unit_per_year"] == expected_per_unit)


def test_optimize_order_quantity(results, add_result):
    """测试订单量优化"""
    manager = InventoryManager()
    
    item = InventoryItem(
        sku="SKU001",
        name="Widget",
        current_stock=100,
        unit_cost=10.0,
        unit_price=15.0,
        daily_demand_avg=10.0
    )
    manager.add_item(item)
    
    # test 40: 订单量优化
    optimization = manager.optimize_order_quantity("SKU001")
    add_result("optimize_order_quantity eoq", optimization["eoq"] > 0)
    
    # test 41: 成本比较
    add_result("optimize_order_quantity cost_comparison", 
               len(optimization["cost_comparison"]) > 0)


def test_demand_recording(results, add_result):
    """测试需求记录"""
    manager = InventoryManager()
    
    item = InventoryItem(
        sku="SKU001",
        name="Widget",
        current_stock=100,
        unit_cost=10.0,
        unit_price=15.0
    )
    manager.add_item(item)
    
    # test 42: 记录需求
    manager.record_demand("SKU001", 10)
    manager.record_demand("SKU001", 15)
    manager.record_demand("SKU001", 20)
    
    add_result("record_demand", len(manager._demand_history["SKU001"]) == 3)


def test_create_inventory_manager(results, add_result):
    """测试便捷创建函数"""
    items_data = [
        {"sku": "SKU001", "name": "Widget", "current_stock": 100, "unit_cost": 10},
        {"sku": "SKU002", "name": "Gadget", "current_stock": 50, "unit_cost": 20},
    ]
    
    # test 43: 从列表创建管理器
    manager = create_inventory_manager(items_data)
    add_result("create_inventory_manager", len(manager.items) == 2)


def test_reorder_quantity_methods(results, add_result):
    """测试不同订货量方法"""
    manager = InventoryManager()
    
    item = InventoryItem(
        sku="SKU001",
        name="Widget",
        current_stock=100,
        unit_cost=10.0,
        unit_price=15.0,
        daily_demand_avg=10.0,
        max_stock=500
    )
    manager.add_item(item)
    
    # test 44: EOQ 方法
    qty_eoq = manager.calculate_reorder_quantity("SKU001", method="eoq")
    add_result("calculate_reorder_quantity eoq", qty_eoq > 0)
    
    # test 45: 固定方法
    qty_fixed = manager.calculate_reorder_quantity("SKU001", method="fixed", fixed_qty=100)
    add_result("calculate_reorder_quantity fixed", qty_fixed == 100)
    
    # test 46: min_max 方法
    qty_minmax = manager.calculate_reorder_quantity("SKU001", method="min_max")
    add_result("calculate_reorder_quantity min_max", qty_minmax > 0)


def test_enums(results, add_result):
    """测试枚举类型"""
    # test 47: StockStatus
    add_result("StockStatus values", 
               StockStatus.CRITICAL.value == "critical" and StockStatus.NORMAL.value == "normal")
    
    # test 48: ABCClass
    add_result("ABCClass values", 
               ABCClass.A.value == "A" and ABCClass.B.value == "B" and ABCClass.C.value == "C")


def test_z_score(results, add_result):
    """测试 Z 分数"""
    # test 49: 常见服务水平的 Z 分数
    z_90 = InventoryManager._get_z_score(0.90)
    z_95 = InventoryManager._get_z_score(0.95)
    add_result("_get_z_score", z_90 < z_95, f"Higher service level should have higher z-score")


def test_normal_cdf(results, add_result):
    """测试正态分布 CDF"""
    # test 50: CDF 值范围
    cdf_0 = InventoryManager._normal_cdf(0)
    cdf_1 = InventoryManager._normal_cdf(1)
    cdf_neg1 = InventoryManager._normal_cdf(-1)
    
    add_result("_normal_cdf center", abs(cdf_0 - 0.5) < 0.1, f"Expected ~0.5, got {cdf_0}")
    add_result("_normal_cdf positive", cdf_1 > cdf_0, f"Positive z should be > 0.5")
    add_result("_normal_cdf negative", cdf_neg1 < cdf_0, f"Negative z should be < 0.5")


def main():
    """运行所有测试"""
    results, add_result = test_result_collector()
    
    # 运行各测试组
    test_inventory_item(results, add_result)
    test_inventory_manager(results, add_result)
    test_update_stock(results, add_result)
    test_safety_stock(results, add_result)
    test_reorder_point(results, add_result)
    test_eoq(results, add_result)
    test_stock_status(results, add_result)
    test_abc_analysis(results, add_result)
    test_turnover(results, add_result)
    test_days_of_stock(results, add_result)
    test_stockout_risk(results, add_result)
    test_restock_recommendations(results, add_result)
    test_summary(results, add_result)
    test_carrying_cost(results, add_result)
    test_optimize_order_quantity(results, add_result)
    test_demand_recording(results, add_result)
    test_create_inventory_manager(results, add_result)
    test_reorder_quantity_methods(results, add_result)
    test_enums(results, add_result)
    test_z_score(results, add_result)
    test_normal_cdf(results, add_result)
    
    # 输出结果
    passed = sum(1 for r in results if r["passed"])
    total = len(results)
    
    print("=" * 60)
    print("Inventory Utils Test Results")
    print("=" * 60)
    
    for r in results:
        status = "✅" if r["passed"] else "❌"
        print(f"{status} {r['name']}: {r['message']}")
    
    print("-" * 60)
    print(f"Summary: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    print("=" * 60)
    
    return passed, total


if __name__ == "__main__":
    passed, total = main()
    sys.exit(0 if passed == total else 1)
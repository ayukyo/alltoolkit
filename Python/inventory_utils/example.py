#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Inventory Management Utilities - Usage Examples

Demonstrates common use cases for the inventory management toolkit.
"""

from mod import (
    InventoryManager,
    InventoryItem,
    StockStatus,
    ABCClass,
    create_inventory_manager,
    calculate_reorder_point,
    calculate_safety_stock,
    calculate_eoq,
    classify_inventory,
)


def example_basic_usage():
    """Basic inventory management example"""
    print("\n" + "="*60)
    print("Example 1: Basic Inventory Management")
    print("="*60)
    
    # Create inventory manager
    manager = InventoryManager(service_level=0.95)
    
    # Add items
    items = [
        InventoryItem(
            sku="LAPTOP-001",
            name="Business Laptop",
            current_stock=25,
            unit_cost=800.0,
            unit_price=1200.0,
            lead_time_days=14,
            daily_demand_avg=2.0,
            daily_demand_std=0.5
        ),
        InventoryItem(
            sku="PHONE-001",
            name="Smartphone",
            current_stock=50,
            unit_cost=300.0,
            unit_price=500.0,
            lead_time_days=7,
            daily_demand_avg=5.0,
            daily_demand_std=1.2
        ),
        InventoryItem(
            sku="TABLET-001",
            name="Tablet Device",
            current_stock=8,
            unit_cost=400.0,
            unit_price=600.0,
            lead_time_days=10,
            daily_demand_avg=1.5,
            daily_demand_std=0.3
        ),
    ]
    
    for item in items:
        manager.add_item(item)
    
    # Calculate safety stock and reorder points
    print("\n--- Stock Status Analysis ---")
    for sku in ["LAPTOP-001", "PHONE-001", "TABLET-001"]:
        item = manager.get_item(sku)
        safety_stock = manager.calculate_safety_stock(sku)
        reorder_point = manager.calculate_reorder_point(sku)
        status = manager.get_stock_status(sku)
        
        print(f"\n{item.name} ({sku}):")
        print(f"  Current Stock: {item.current_stock} units")
        print(f"  Daily Demand: {item.daily_demand_avg} units/day")
        print(f"  Lead Time: {item.lead_time_days} days")
        print(f"  Safety Stock: {safety_stock:.1f} units")
        print(f"  Reorder Point: {reorder_point:.1f} units")
        print(f"  Stock Status: {status.value}")
        print(f"  Days of Stock: {manager.calculate_days_of_stock(sku):.1f} days")


def example_abc_analysis():
    """ABC inventory classification example"""
    print("\n" + "="*60)
    print("Example 2: ABC Analysis")
    print("="*60)
    
    # Create manager with varying value items
    manager = InventoryManager()
    
    # High value items (Class A)
    manager.add_item(InventoryItem(
        sku="VIP-001", name="Premium Product A", current_stock=5,
        unit_cost=500.0, unit_price=800.0, daily_demand_avg=0.5
    ))
    manager.add_item(InventoryItem(
        sku="VIP-002", name="Premium Product B", current_stock=8,
        unit_cost=450.0, unit_price=700.0, daily_demand_avg=0.8
    ))
    
    # Medium value items (Class B)
    manager.add_item(InventoryItem(
        sku="STD-001", name="Standard Product A", current_stock=50,
        unit_cost=50.0, unit_price=80.0, daily_demand_avg=3.0
    ))
    manager.add_item(InventoryItem(
        sku="STD-002", name="Standard Product B", current_stock=40,
        unit_cost=45.0, unit_price=75.0, daily_demand_avg=2.5
    ))
    
    # Low value items (Class C)
    manager.add_item(InventoryItem(
        sku="COM-001", name="Common Product A", current_stock=200,
        unit_cost=5.0, unit_price=10.0, daily_demand_avg=15.0
    ))
    manager.add_item(InventoryItem(
        sku="COM-002", name="Common Product B", current_stock=150,
        unit_cost=3.0, unit_price=8.0, daily_demand_avg=20.0
    ))
    manager.add_item(InventoryItem(
        sku="COM-003", name="Common Product C", current_stock=300,
        unit_cost=2.0, unit_price=5.0, daily_demand_avg=30.0
    ))
    
    # Perform ABC analysis
    classifications = manager.abc_analysis()
    
    print("\n--- ABC Classification Results ---")
    print("\nClass A Items (High Value - Tight Control):")
    for sku, cls in classifications.items():
        if cls == ABCClass.A:
            item = manager.get_item(sku)
            print(f"  {sku}: {item.name} - Value: ${item.stock_value:.0f}")
    
    print("\nClass B Items (Medium Value - Moderate Control):")
    for sku, cls in classifications.items():
        if cls == ABCClass.B:
            item = manager.get_item(sku)
            print(f"  {sku}: {item.name} - Value: ${item.stock_value:.0f}")
    
    print("\nClass C Items (Low Value - Simple Control):")
    for sku, cls in classifications.items():
        if cls == ABCClass.C:
            item = manager.get_item(sku)
            print(f"  {sku}: {item.name} - Value: ${item.stock_value:.0f}")
    
    # Summary
    summary = manager.get_summary()
    print("\n--- Inventory Summary ---")
    print(f"  Total Items: {summary.total_items}")
    print(f"  Total Stock Value: ${summary.total_stock_value:.2f}")
    print(f"  ABC Distribution: A={summary.abc_distribution['A']}, "
          f"B={summary.abc_distribution['B']}, C={summary.abc_distribution['C']}")


def example_eoq_optimization():
    """Economic Order Quantity example"""
    print("\n" + "="*60)
    print("Example 3: EOQ Optimization")
    print("="*60)
    
    manager = InventoryManager()
    manager.add_item(InventoryItem(
        sku="COMP-001",
        name="Electronic Component",
        current_stock=100,
        unit_cost=25.0,
        unit_price=40.0,
        daily_demand_avg=10.0,  # ~3650/year
        min_order_qty=50
    ))
    
    # Calculate EOQ with different parameters
    print("\n--- EOQ Analysis ---")
    
    optimization = manager.optimize_order_quantity(
        "COMP-001",
        annual_demand=3650,
        ordering_cost=75.0,  # Cost to place an order
        holding_cost_rate=0.25  # 25% annual holding cost
    )
    
    print(f"\nItem: Electronic Component (COMP-001)")
    print(f"  Annual Demand: {optimization['annual_demand']} units")
    print(f"  Economic Order Quantity: {optimization['eoq']:.0f} units")
    print(f"  Orders per Year: {optimization['orders_per_year']:.1f}")
    print(f"  Days Between Orders: {optimization['days_between_orders']:.0f} days")
    print(f"  Annual Total Cost: ${optimization['total_annual_cost']:.2f}")
    print(f"    - Holding Cost: ${optimization['holding_cost_at_eoq']:.2f}")
    print(f"    - Ordering Cost: ${optimization['ordering_cost_at_eoq']:.2f}")
    
    print("\n--- Cost Comparison at Different Order Quantities ---")
    for comparison in optimization['cost_comparison']:
        qty = comparison['quantity']
        total = comparison['total_cost']
        print(f"  Order Qty: {qty:.0f} units → Total Cost: ${total:.2f}")


def example_restock_recommendations():
    """Restock recommendations example"""
    print("\n" + "="*60)
    print("Example 4: Restock Recommendations")
    print("="*60)
    
    # Create inventory with various stock levels
    manager = InventoryManager(service_level=0.95)
    
    # Well stocked items
    manager.add_item(InventoryItem(
        sku="GOOD-001", name="Well Stocked Item", current_stock=500,
        unit_cost=10.0, unit_price=20.0, daily_demand_avg=10.0,
        lead_time_days=7
    ))
    
    # Below reorder point
    manager.add_item(InventoryItem(
        sku="LOW-001", name="Low Stock Item", current_stock=30,
        unit_cost=50.0, unit_price=80.0, daily_demand_avg=5.0,
        daily_demand_std=1.0, lead_time_days=14
    ))
    
    # Critical stock
    manager.add_item(InventoryItem(
        sku="CRIT-001", name="Critical Stock Item", current_stock=5,
        unit_cost=100.0, unit_price=150.0, daily_demand_avg=2.0,
        daily_demand_std=0.3, lead_time_days=21
    ))
    
    # Get recommendations
    recommendations = manager.get_restock_recommendations()
    
    print("\n--- Items Needing Restock ---")
    for rec in recommendations:
        print(f"\n{rec['name']} ({rec['sku']}):")
        print(f"  Status: {rec['status']} (Urgency: {rec['urgency']})")
        print(f"  Current Stock: {rec['current_stock']:.0f} units")
        print(f"  Reorder Point: {rec['reorder_point']:.1f} units")
        print(f"  Safety Stock: {rec['safety_stock']:.1f} units")
        print(f"  Recommended Order: {rec['recommended_qty']:.0f} units")
        print(f"  Estimated Cost: ${rec['estimated_cost']:.2f}")
        print(f"  Days Until Stockout: {rec['days_until_stockout']:.1f} days")


def example_carrying_cost_analysis():
    """Carrying cost analysis example"""
    print("\n" + "="*60)
    print("Example 5: Carrying Cost Analysis")
    print("="*60)
    
    manager = InventoryManager()
    manager.add_item(InventoryItem(
        sku="WARE-001",
        name="Warehouse Item",
        current_stock=1000,
        unit_cost=20.0,
        unit_price=35.0,
        daily_demand_avg=20.0
    ))
    
    costs = manager.calculate_carrying_cost(
        "WARE-001",
        holding_cost_rate=0.30,  # 30% holding cost
        period_days=365
    )
    
    print("\n--- Carrying Cost Analysis ---")
    print(f"\nItem: Warehouse Item (WARE-001)")
    print(f"  Average Inventory: {costs['average_inventory']} units")
    print(f"  Average Inventory Value: ${costs['average_inventory_value']:.2f}")
    print(f"  Holding Cost Rate: {costs['holding_cost_rate']:.1%}")
    print(f"  Annual Carrying Cost: ${costs['annual_carrying_cost']:.2f}")
    print(f"  Cost per Unit per Year: ${costs['cost_per_unit_per_year']:.2f}")
    
    # Breakdown interpretation
    print("\n--- Cost Components ---")
    print("  Holding costs typically include:")
    print("    - Storage space costs")
    print("    - Insurance")
    print("    - Obsolescence risk")
    print("    - Capital cost (opportunity cost)")
    print("    - Handling and maintenance")


def example_stockout_risk():
    """Stockout risk analysis example"""
    print("\n" + "="*60)
    print("Example 6: Stockout Risk Assessment")
    print("="*60)
    
    manager = InventoryManager(service_level=0.95)
    
    # Stable demand item
    manager.add_item(InventoryItem(
        sku="STABLE-001", name="Stable Demand Item",
        current_stock=100, unit_cost=10.0, unit_price=20.0,
        daily_demand_avg=5.0, daily_demand_std=0.5, lead_time_days=7
    ))
    
    # Variable demand item
    manager.add_item(InventoryItem(
        sku="VARIABLE-001", name="Variable Demand Item",
        current_stock=100, unit_cost=10.0, unit_price=20.0,
        daily_demand_avg=5.0, daily_demand_std=3.0, lead_time_days=7
    ))
    
    print("\n--- Stockout Risk Comparison ---")
    
    for sku in ["STABLE-001", "VARIABLE-001"]:
        item = manager.get_item(sku)
        risk_7d = manager.calculate_stockout_risk(sku, days_ahead=7)
        risk_14d = manager.calculate_stockout_risk(sku, days_ahead=14)
        risk_30d = manager.calculate_stockout_risk(sku, days_ahead=30)
        
        print(f"\n{item.name} (Demand Std: {item.daily_demand_std}):")
        print(f"  7-day stockout risk: {risk_7d:.1%}")
        print(f"  14-day stockout risk: {risk_14d:.1%}")
        print(f"  30-day stockout risk: {risk_30d:.1%}")
        
        if risk_30d > 0.5:
            print("  ⚠️ HIGH RISK: Consider increasing safety stock")
        elif risk_30d > 0.2:
            print("  ⚡ MODERATE RISK: Monitor closely")
        else:
            print("  ✓ LOW RISK: Current levels adequate")


def example_quick_functions():
    """Quick helper functions example"""
    print("\n" + "="*60)
    print("Example 7: Quick Helper Functions")
    print("="*60)
    
    # Reorder point
    rop = calculate_reorder_point(
        daily_demand=10,
        lead_time_days=7,
        safety_stock=20
    )
    print(f"\nReorder Point Calculation:")
    print(f"  Daily Demand: 10 units/day")
    print(f"  Lead Time: 7 days")
    print(f"  Safety Stock: 20 units")
    print(f"  → Reorder Point: {rop} units")
    
    # Safety stock
    ss = calculate_safety_stock(
        daily_demand_std=2.0,
        lead_time_days=7,
        service_level=0.95
    )
    print(f"\nSafety Stock Calculation:")
    print(f"  Demand Std Dev: 2.0 units")
    print(f"  Lead Time: 7 days")
    print(f"  Service Level: 95%")
    print(f"  → Safety Stock: {ss:.1f} units")
    
    # EOQ
    eoq = calculate_eoq(
        annual_demand=3650,
        ordering_cost=50,
        unit_cost=20,
        holding_cost_rate=0.25
    )
    print(f"\nEOQ Calculation:")
    print(f"  Annual Demand: 3650 units")
    print(f"  Ordering Cost: $50")
    print(f"  Unit Cost: $20")
    print(f"  Holding Cost Rate: 25%")
    print(f"  → Optimal Order Quantity: {eoq:.0f} units")
    
    # ABC Classification
    items = [
        {"sku": "A", "value": 8000},
        {"sku": "B", "value": 1500},
        {"sku": "C", "value": 500},
    ]
    classifications = classify_inventory(items)
    print(f"\nQuick ABC Classification:")
    for sku, cls in classifications.items():
        print(f"  Item {sku}: Class {cls.value}")


def example_factory_function():
    """Factory function example"""
    print("\n" + "="*60)
    print("Example 8: Create Inventory from Data")
    print("="*60)
    
    # Simulate loading from database or API
    items_data = [
        {
            "sku": "PROD-A",
            "name": "Product Alpha",
            "current_stock": 150,
            "unit_cost": 25.0,
            "unit_price": 45.0,
            "daily_demand_avg": 5.0,
            "daily_demand_std": 1.0,
            "lead_time_days": 10,
            "category": "Electronics"
        },
        {
            "sku": "PROD-B",
            "name": "Product Beta",
            "current_stock": 80,
            "unit_cost": 50.0,
            "unit_price": 90.0,
            "daily_demand_avg": 3.0,
            "lead_time_days": 14,
            "category": "Appliances"
        },
        {
            "sku": "PROD-C",
            "name": "Product Gamma",
            "current_stock": 200,
            "unit_cost": 10.0,
            "unit_price": 20.0,
            "daily_demand_avg": 15.0,
            "lead_time_days": 5,
            "category": "Accessories"
        },
    ]
    
    # Create manager from data
    manager = create_inventory_manager(items_data, service_level=0.95)
    
    print("\n--- Created Inventory Manager ---")
    print(f"  Loaded {len(manager.items)} items")
    
    summary = manager.get_summary()
    print(f"\n  Summary:")
    print(f"    Total Stock Value: ${summary.total_stock_value:.2f}")
    print(f"    Potential Revenue: ${summary.total_potential_revenue:.2f}")
    print(f"    Items Below Reorder: {summary.items_below_reorder}")
    print(f"    Critical Items: {summary.items_critical}")
    
    # Show item details
    print("\n  Item Details:")
    for sku, item in manager.items.items():
        print(f"    {sku}: {item.name} - {item.current_stock} units @ ${item.unit_cost}")


def run_all_examples():
    """Run all examples"""
    example_basic_usage()
    example_abc_analysis()
    example_eoq_optimization()
    example_restock_recommendations()
    example_carrying_cost_analysis()
    example_stockout_risk()
    example_quick_functions()
    example_factory_function()
    
    print("\n" + "="*60)
    print("All examples completed successfully!")
    print("="*60)


if __name__ == "__main__":
    run_all_examples()
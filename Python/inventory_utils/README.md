# Inventory Management Utilities

A comprehensive inventory management toolkit for Python with zero external dependencies.

## Features

- **Stock Level Tracking**: Monitor current stock levels and status
- **Reorder Point Calculation**: Calculate when to reorder based on demand and lead time
- **Safety Stock Calculation**: Determine buffer stock for demand variability
- **Economic Order Quantity (EOQ)**: Optimize order quantities to minimize costs
- **ABC Analysis**: Classify inventory by value contribution (A/B/C categories)
- **Inventory Turnover**: Calculate how quickly inventory sells
- **Days of Stock**: Estimate days until stockout
- **Stockout Risk Assessment**: Calculate probability of running out of stock
- **Carrying Cost Analysis**: Analyze inventory holding costs
- **Order Optimization**: Detailed EOQ optimization with cost comparisons
- **Restock Recommendations**: Prioritized list of items needing reorder

## Installation

No installation required - this module uses only Python standard library.

```python
from inventory_utils.mod import InventoryManager, InventoryItem
```

## Quick Start

### Basic Usage

```python
from mod import InventoryManager, InventoryItem

# Create manager
manager = InventoryManager(service_level=0.95)

# Add item
item = InventoryItem(
    sku="LAPTOP-001",
    name="Business Laptop",
    current_stock=25,
    unit_cost=800.0,
    unit_price=1200.0,
    lead_time_days=14,
    daily_demand_avg=2.0,
    daily_demand_std=0.5
)
manager.add_item(item)

# Calculate safety stock
safety_stock = manager.calculate_safety_stock("LAPTOP-001")

# Calculate reorder point
reorder_point = manager.calculate_reorder_point("LAPTOP-001")

# Check stock status
status = manager.get_stock_status("LAPTOP-001")  # Returns: CRITICAL, LOW, NORMAL, OVERSTOCKED
```

### Quick Functions

```python
from mod import calculate_reorder_point, calculate_safety_stock, calculate_eoq

# Reorder point = (Daily Demand × Lead Time) + Safety Stock
rop = calculate_reorder_point(daily_demand=10, lead_time_days=7, safety_stock=20)

# Safety stock = Z-score × Std Dev × √Lead Time
ss = calculate_safety_stock(daily_demand_std=2.0, lead_time_days=7, service_level=0.95)

# EOQ = √(2 × Annual Demand × Order Cost / Holding Cost)
eoq = calculate_eoq(annual_demand=3650, ordering_cost=50, unit_cost=20, holding_cost_rate=0.25)
```

### Create from Data

```python
from mod import create_inventory_manager

items_data = [
    {
        "sku": "PROD-001",
        "name": "Product One",
        "current_stock": 100,
        "unit_cost": 25.0,
        "unit_price": 45.0,
        "daily_demand_avg": 5.0,
        "lead_time_days": 10
    },
    # ... more items
]

manager = create_inventory_manager(items_data, service_level=0.95)
```

## Key Methods

### InventoryManager Class

| Method | Description |
|--------|-------------|
| `add_item(item)` | Add an inventory item |
| `remove_item(sku)` | Remove an item by SKU |
| `get_item(sku)` | Get item by SKU |
| `update_stock(sku, qty)` | Add/remove stock |
| `calculate_safety_stock(sku)` | Calculate safety stock quantity |
| `calculate_reorder_point(sku)` | Calculate reorder point |
| `calculate_eoq(sku)` | Calculate optimal order quantity |
| `get_stock_status(sku)` | Get status (CRITICAL/LOW/NORMAL/OVERSTOCKED) |
| `abc_analysis()` | Perform ABC classification |
| `calculate_turnover(sku)` | Calculate inventory turnover rate |
| `calculate_days_of_stock(sku)` | Days until stockout |
| `calculate_stockout_risk(sku, days)` | Probability of stockout |
| `get_restock_recommendations()` | List items needing reorder |
| `get_summary()` | Get inventory summary statistics |
| `optimize_order_quantity(sku)` | Detailed EOQ optimization |

## ABC Analysis

Classifies inventory items by value contribution:

- **Class A**: High-value items (~80% of value, ~20% of items)
  - Tight control, frequent review
- **Class B**: Medium-value items (~15% of value, ~30% of items)
  - Moderate control, periodic review
- **Class C**: Low-value items (~5% of value, ~50% of items)
  - Simple control, bulk ordering

```python
classifications = manager.abc_analysis()

for sku, cls in classifications.items():
    print(f"{sku}: Class {cls.value}")  # A, B, or C
```

## Formulas

### Safety Stock
```
SS = Z × σ × √L
```
- Z = Z-score for service level (95% → 1.645)
- σ = Standard deviation of daily demand
- L = Lead time in days

### Reorder Point
```
ROP = (D × L) + SS
```
- D = Average daily demand
- L = Lead time in days
- SS = Safety stock

### Economic Order Quantity
```
EOQ = √(2DS/H)
```
- D = Annual demand
- S = Ordering cost per order
- H = Holding cost per unit per year

### Inventory Turnover
```
Turnover = COGS / Average Inventory Value
```

## Example Output

```
--- Restock Recommendations ---
Product Alpha (PROD-001):
  Status: critical (Urgency: critical)
  Current Stock: 5 units
  Reorder Point: 21.7 units
  Safety Stock: 6.7 units
  Recommended Order: 85 units
  Estimated Cost: $2125.00
  Days Until Stockout: 2.5 days

--- Inventory Summary ---
  Total Items: 150
  Total Stock Value: $125,000.00
  Items Below Reorder: 12
  Critical Items: 3
  ABC Distribution: A=30, B=45, C=75
```

## License

MIT License - Part of AllToolkit

## Author

AllToolkit Automated Generation
Date: 2026-05-15
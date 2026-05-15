"""
Inventory Management Utilities
================================

A comprehensive inventory management toolkit with zero external dependencies.

Features:
- Stock level tracking and monitoring
- Reorder point calculation
- Safety stock calculation
- Economic Order Quantity (EOQ)
- ABC analysis for inventory classification
- Inventory turnover calculation
- Lead time management
- Demand forecasting
- Stockout risk assessment
- Carrying cost analysis
- Order quantity optimization

Author: AllToolkit
Date: 2026-05-15
"""

import math
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta
from collections import defaultdict


class StockStatus(Enum):
    """Stock level status"""
    CRITICAL = "critical"      # Below safety stock
    LOW = "low"               # Below reorder point
    NORMAL = "normal"         # Above reorder point
    OVERSTOCKED = "overstocked"  # Excessive inventory


class ABCClass(Enum):
    """ABC classification for inventory items"""
    A = "A"  # High value, low quantity (80% value, 20% items)
    B = "B"  # Medium value, medium quantity (15% value, 30% items)
    C = "C"  # Low value, high quantity (5% value, 50% items)


@dataclass
class InventoryItem:
    """Inventory item data structure"""
    sku: str                          # Stock Keeping Unit
    name: str                         # Item name
    current_stock: float              # Current stock level
    unit_cost: float                  # Cost per unit
    unit_price: float                 # Selling price per unit
    lead_time_days: int = 7          # Days from order to delivery
    daily_demand_avg: float = 0.0    # Average daily demand
    daily_demand_std: float = 0.0    # Standard deviation of demand
    safety_stock: float = 0.0        # Safety stock level
    reorder_point: float = 0.0       # Reorder point
    reorder_quantity: float = 0.0    # Suggested reorder quantity
    max_stock: Optional[float] = None  # Maximum stock level
    min_order_qty: float = 1.0       # Minimum order quantity
    category: str = ""               # Item category
    abc_class: Optional[ABCClass] = None  # ABC classification
    last_restock_date: Optional[datetime] = None
    last_sale_date: Optional[datetime] = None
    
    @property
    def stock_value(self) -> float:
        """Total value of current stock"""
        return self.current_stock * self.unit_cost
    
    @property
    def potential_revenue(self) -> float:
        """Potential revenue if all stock sold"""
        return self.current_stock * self.unit_price
    
    @property
    def profit_margin(self) -> float:
        """Profit margin percentage"""
        if self.unit_cost == 0:
            return 0.0
        return ((self.unit_price - self.unit_cost) / self.unit_cost) * 100


@dataclass
class InventorySummary:
    """Inventory summary statistics"""
    total_items: int
    total_stock_value: float
    total_potential_revenue: float
    items_below_reorder: int
    items_critical: int
    items_overstocked: int
    average_turnover: float
    abc_distribution: Dict[str, int]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "total_items": self.total_items,
            "total_stock_value": round(self.total_stock_value, 2),
            "total_potential_revenue": round(self.total_potential_revenue, 2),
            "items_below_reorder": self.items_below_reorder,
            "items_critical": self.items_critical,
            "items_overstocked": self.items_overstocked,
            "average_turnover": round(self.average_turnover, 2),
            "abc_distribution": self.abc_distribution
        }


class InventoryManager:
    """
    Main inventory management class.
    
    Provides methods for stock tracking, reorder calculations,
    ABC analysis, and inventory optimization.
    """
    
    def __init__(self, service_level: float = 0.95):
        """
        Initialize inventory manager.
        
        Args:
            service_level: Target service level for safety stock (0.0-1.0)
        """
        self.items: Dict[str, InventoryItem] = {}
        self.service_level = service_level
        self._demand_history: Dict[str, List[Tuple[datetime, float]]] = defaultdict(list)
    
    def add_item(self, item: InventoryItem) -> None:
        """Add an item to inventory"""
        self.items[item.sku] = item
    
    def remove_item(self, sku: str) -> bool:
        """Remove an item from inventory"""
        if sku in self.items:
            del self.items[sku]
            return True
        return False
    
    def get_item(self, sku: str) -> Optional[InventoryItem]:
        """Get an item by SKU"""
        return self.items.get(sku)
    
    def update_stock(self, sku: str, quantity: float) -> bool:
        """
        Update stock level for an item.
        
        Args:
            sku: Item SKU
            quantity: Quantity to add (positive) or remove (negative)
            
        Returns:
            True if successful, False if item not found
        """
        item = self.items.get(sku)
        if item is None:
            return False
        item.current_stock += quantity
        if quantity < 0:
            item.last_sale_date = datetime.now()
        elif quantity > 0:
            item.last_restock_date = datetime.now()
        return True
    
    def record_demand(self, sku: str, quantity: float, date: Optional[datetime] = None) -> None:
        """
        Record demand for an item (for forecasting).
        
        Args:
            sku: Item SKU
            quantity: Quantity demanded
            date: Date of demand (defaults to now)
        """
        if date is None:
            date = datetime.now()
        self._demand_history[sku].append((date, quantity))
    
    def calculate_safety_stock(
        self, 
        sku: str, 
        lead_time_days: Optional[int] = None,
        service_level: Optional[float] = None
    ) -> float:
        """
        Calculate safety stock for an item.
        
        Uses the formula: Safety Stock = Z × σd × √L
        
        Where:
        - Z = Z-score for desired service level
        - σd = Standard deviation of daily demand
        - L = Lead time in days
        
        Args:
            sku: Item SKU
            lead_time_days: Lead time (uses item's lead time if not specified)
            service_level: Service level (uses manager's default if not specified)
            
        Returns:
            Safety stock quantity
        """
        item = self.items.get(sku)
        if item is None:
            raise ValueError(f"Item {sku} not found")
        
        lead_time = lead_time_days or item.lead_time_days
        service = service_level or self.service_level
        
        # Get demand standard deviation
        demand_std = item.daily_demand_std
        
        # If no std provided, estimate from history
        if demand_std == 0 and sku in self._demand_history:
            demands = [q for _, q in self._demand_history[sku]]
            if len(demands) > 1:
                mean = sum(demands) / len(demands)
                variance = sum((d - mean) ** 2 for d in demands) / (len(demands) - 1)
                demand_std = math.sqrt(variance)
        
        # Z-score for service level
        z_score = self._get_z_score(service)
        
        # Safety stock = Z × σ × √L
        safety_stock = z_score * demand_std * math.sqrt(lead_time)
        
        return max(0, safety_stock)
    
    def calculate_reorder_point(
        self, 
        sku: str, 
        lead_time_days: Optional[int] = None,
        service_level: Optional[float] = None
    ) -> float:
        """
        Calculate reorder point for an item.
        
        Reorder Point = (Average Daily Demand × Lead Time) + Safety Stock
        
        Args:
            sku: Item SKU
            lead_time_days: Lead time (uses item's lead time if not specified)
            service_level: Service level for safety stock calculation
            
        Returns:
            Reorder point quantity
        """
        item = self.items.get(sku)
        if item is None:
            raise ValueError(f"Item {sku} not found")
        
        lead_time = lead_time_days or item.lead_time_days
        safety_stock = self.calculate_safety_stock(sku, lead_time, service_level)
        
        # ROP = D × L + SS
        reorder_point = (item.daily_demand_avg * lead_time) + safety_stock
        
        return reorder_point
    
    def calculate_eoq(
        self, 
        sku: str, 
        annual_demand: Optional[float] = None,
        ordering_cost: float = 50.0,
        holding_cost_rate: float = 0.25
    ) -> float:
        """
        Calculate Economic Order Quantity (EOQ).
        
        EOQ = √(2DS/H)
        
        Where:
        - D = Annual demand
        - S = Ordering cost per order
        - H = Annual holding cost per unit
        
        Args:
            sku: Item SKU
            annual_demand: Annual demand (calculated from daily demand if not provided)
            ordering_cost: Cost per order
            holding_cost_rate: Holding cost as percentage of unit cost
            
        Returns:
            Optimal order quantity
        """
        item = self.items.get(sku)
        if item is None:
            raise ValueError(f"Item {sku} not found")
        
        # Calculate annual demand if not provided
        if annual_demand is None:
            annual_demand = item.daily_demand_avg * 365
        
        # Holding cost per unit per year
        holding_cost = item.unit_cost * holding_cost_rate
        
        if holding_cost == 0:
            return annual_demand
        
        # EOQ formula
        eoq = math.sqrt((2 * annual_demand * ordering_cost) / holding_cost)
        
        # Round up to minimum order quantity
        return max(item.min_order_qty, math.ceil(eoq))
    
    def calculate_reorder_quantity(
        self, 
        sku: str,
        method: str = "eoq",
        **kwargs
    ) -> float:
        """
        Calculate suggested reorder quantity.
        
        Args:
            sku: Item SKU
            method: Calculation method ("eoq", "fixed", "min_max")
            **kwargs: Additional parameters for specific methods
            
        Returns:
            Suggested reorder quantity
        """
        item = self.items.get(sku)
        if item is None:
            raise ValueError(f"Item {sku} not found")
        
        if method == "eoq":
            return self.calculate_eoq(sku, **kwargs)
        elif method == "fixed":
            return kwargs.get("fixed_qty", item.daily_demand_avg * 30)
        elif method == "min_max":
            max_stock = kwargs.get("max_stock", item.max_stock or item.daily_demand_avg * 60)
            return max_stock - item.current_stock
        else:
            return self.calculate_eoq(sku, **kwargs)
    
    def get_stock_status(self, sku: str) -> StockStatus:
        """
        Get stock status for an item.
        
        Args:
            sku: Item SKU
            
        Returns:
            StockStatus enum value
        """
        item = self.items.get(sku)
        if item is None:
            raise ValueError(f"Item {sku} not found")
        
        # Calculate if not set
        if item.safety_stock == 0:
            item.safety_stock = self.calculate_safety_stock(sku)
        if item.reorder_point == 0:
            item.reorder_point = self.calculate_reorder_point(sku)
        
        # Check max stock if defined
        if item.max_stock and item.current_stock > item.max_stock:
            return StockStatus.OVERSTOCKED
        
        if item.current_stock <= item.safety_stock:
            return StockStatus.CRITICAL
        elif item.current_stock <= item.reorder_point:
            return StockStatus.LOW
        else:
            return StockStatus.NORMAL
    
    def abc_analysis(
        self, 
        value_threshold_a: float = 0.80,
        value_threshold_b: float = 0.95
    ) -> Dict[str, ABCClass]:
        """
        Perform ABC analysis on inventory.
        
        Classifies items based on their contribution to total inventory value:
        - Class A: High value items (typically 80% of value, 20% of items)
        - Class B: Medium value items (typically 15% of value, 30% of items)
        - Class C: Low value items (typically 5% of value, 50% of items)
        
        Args:
            value_threshold_a: Cumulative value threshold for Class A (default 80%)
            value_threshold_b: Cumulative value threshold for Class B (default 95%)
            
        Returns:
            Dictionary mapping SKU to ABC classification
        """
        # Calculate total value and sort items by value
        items_with_value = [
            (sku, item.stock_value) 
            for sku, item in self.items.items()
        ]
        
        # Sort by value descending
        items_with_value.sort(key=lambda x: x[1], reverse=True)
        
        total_value = sum(value for _, value in items_with_value)
        
        if total_value == 0:
            return {sku: ABCClass.C for sku in self.items}
        
        classifications = {}
        cumulative_value = 0.0
        
        for sku, value in items_with_value:
            cumulative_value += value
            cumulative_pct = cumulative_value / total_value
            
            if cumulative_pct <= value_threshold_a:
                classifications[sku] = ABCClass.A
                self.items[sku].abc_class = ABCClass.A
            elif cumulative_pct <= value_threshold_b:
                classifications[sku] = ABCClass.B
                self.items[sku].abc_class = ABCClass.B
            else:
                classifications[sku] = ABCClass.C
                self.items[sku].abc_class = ABCClass.C
        
        return classifications
    
    def calculate_turnover(
        self, 
        sku: str, 
        period_days: int = 365
    ) -> float:
        """
        Calculate inventory turnover rate.
        
        Turnover = Cost of Goods Sold / Average Inventory
        
        Args:
            sku: Item SKU
            period_days: Period in days for calculation
            
        Returns:
            Turnover rate (times per period)
        """
        item = self.items.get(sku)
        if item is None:
            raise ValueError(f"Item {sku} not found")
        
        # Estimate COGS from demand
        cogs = item.daily_demand_avg * period_days * item.unit_cost
        
        # Average inventory value
        avg_inventory = item.current_stock * item.unit_cost
        
        if avg_inventory == 0:
            return 0.0
        
        return cogs / avg_inventory
    
    def calculate_days_of_stock(
        self, 
        sku: str
    ) -> float:
        """
        Calculate days of stock remaining.
        
        Days of Stock = Current Stock / Average Daily Demand
        
        Args:
            sku: Item SKU
            
        Returns:
            Number of days until stockout at current demand rate
        """
        item = self.items.get(sku)
        if item is None:
            raise ValueError(f"Item {sku} not found")
        
        if item.daily_demand_avg == 0:
            return float('inf')
        
        return item.current_stock / item.daily_demand_avg
    
    def calculate_stockout_risk(
        self, 
        sku: str,
        days_ahead: int = 30
    ) -> float:
        """
        Calculate probability of stockout within specified days.
        
        Uses normal distribution approximation.
        
        Args:
            sku: Item SKU
            days_ahead: Number of days to project
            
        Returns:
            Probability of stockout (0.0 to 1.0)
        """
        item = self.items.get(sku)
        if item is None:
            raise ValueError(f"Item {sku} not found")
        
        if item.daily_demand_avg == 0:
            return 0.0
        
        # Expected demand over period
        expected_demand = item.daily_demand_avg * days_ahead
        demand_std = item.daily_demand_std * math.sqrt(days_ahead)
        
        if demand_std == 0:
            # No variability
            return 1.0 if item.current_stock < expected_demand else 0.0
        
        # Z-score for current stock level
        z = (item.current_stock - expected_demand) / demand_std
        
        # Probability of stockout (demand exceeds stock)
        stockout_prob = 1.0 - self._normal_cdf(z)
        
        return max(0.0, min(1.0, stockout_prob))
    
    def get_restock_recommendations(self) -> List[Dict[str, Any]]:
        """
        Get restock recommendations for items below reorder point.
        
        Returns:
            List of dictionaries with restock recommendations
        """
        recommendations = []
        
        for sku, item in self.items.items():
            status = self.get_stock_status(sku)
            
            if status in [StockStatus.LOW, StockStatus.CRITICAL]:
                qty = self.calculate_reorder_quantity(sku)
                
                recommendations.append({
                    "sku": sku,
                    "name": item.name,
                    "current_stock": item.current_stock,
                    "reorder_point": item.reorder_point,
                    "safety_stock": item.safety_stock,
                    "recommended_qty": qty,
                    "status": status.value,
                    "urgency": "critical" if status == StockStatus.CRITICAL else "normal",
                    "estimated_cost": qty * item.unit_cost,
                    "days_until_stockout": self.calculate_days_of_stock(sku)
                })
        
        # Sort by urgency and days until stockout
        recommendations.sort(key=lambda x: (
            0 if x["urgency"] == "critical" else 1,
            x["days_until_stockout"]
        ))
        
        return recommendations
    
    def get_summary(self) -> InventorySummary:
        """
        Get inventory summary statistics.
        
        Returns:
            InventorySummary with key metrics
        """
        total_value = sum(item.stock_value for item in self.items.values())
        total_revenue = sum(item.potential_revenue for item in self.items.values())
        
        items_below_reorder = 0
        items_critical = 0
        items_overstocked = 0
        
        abc_dist = {"A": 0, "B": 0, "C": 0}
        
        turnovers = []
        
        for sku, item in self.items.items():
            status = self.get_stock_status(sku)
            
            if status == StockStatus.CRITICAL:
                items_critical += 1
                items_below_reorder += 1
            elif status == StockStatus.LOW:
                items_below_reorder += 1
            elif status == StockStatus.OVERSTOCKED:
                items_overstocked += 1
            
            if item.abc_class:
                abc_dist[item.abc_class.value] += 1
            
            if item.daily_demand_avg > 0:
                turnovers.append(self.calculate_turnover(sku))
        
        avg_turnover = sum(turnovers) / len(turnovers) if turnovers else 0.0
        
        return InventorySummary(
            total_items=len(self.items),
            total_stock_value=total_value,
            total_potential_revenue=total_revenue,
            items_below_reorder=items_below_reorder,
            items_critical=items_critical,
            items_overstocked=items_overstocked,
            average_turnover=avg_turnover,
            abc_distribution=abc_dist
        )
    
    def calculate_carrying_cost(
        self, 
        sku: str, 
        holding_cost_rate: float = 0.25,
        period_days: int = 365
    ) -> Dict[str, float]:
        """
        Calculate carrying costs for an item.
        
        Carrying Cost = Average Inventory × Unit Cost × Holding Cost Rate × (Period / 365)
        
        Args:
            sku: Item SKU
            holding_cost_rate: Annual holding cost as percentage of unit cost
            period_days: Period for calculation
            
        Returns:
            Dictionary with cost breakdown
        """
        item = self.items.get(sku)
        if item is None:
            raise ValueError(f"Item {sku} not found")
        
        # Assume average inventory is current stock (simplified)
        avg_inventory = item.current_stock
        avg_inventory_value = avg_inventory * item.unit_cost
        
        annual_carrying_cost = avg_inventory_value * holding_cost_rate
        period_carrying_cost = annual_carrying_cost * (period_days / 365)
        
        return {
            "average_inventory": avg_inventory,
            "average_inventory_value": avg_inventory_value,
            "holding_cost_rate": holding_cost_rate,
            "annual_carrying_cost": annual_carrying_cost,
            "period_carrying_cost": period_carrying_cost,
            "cost_per_unit_per_year": item.unit_cost * holding_cost_rate
        }
    
    def optimize_order_quantity(
        self, 
        sku: str,
        annual_demand: Optional[float] = None,
        ordering_cost: float = 50.0,
        holding_cost_rate: float = 0.25
    ) -> Dict[str, Any]:
        """
        Optimize order quantity with detailed analysis.
        
        Args:
            sku: Item SKU
            annual_demand: Annual demand
            ordering_cost: Cost per order
            holding_cost_rate: Holding cost rate
            
        Returns:
            Dictionary with optimization analysis
        """
        item = self.items.get(sku)
        if item is None:
            raise ValueError(f"Item {sku} not found")
        
        if annual_demand is None:
            annual_demand = item.daily_demand_avg * 365
        
        eoq = self.calculate_eoq(sku, annual_demand, ordering_cost, holding_cost_rate)
        
        # Calculate costs at EOQ
        holding_cost_per_unit = item.unit_cost * holding_cost_rate
        total_holding_cost = (eoq / 2) * holding_cost_per_unit
        total_ordering_cost = (annual_demand / eoq) * ordering_cost
        total_cost = total_holding_cost + total_ordering_cost
        
        # Calculate costs at different quantities for comparison
        quantities = [
            max(item.min_order_qty, eoq * 0.5),
            max(item.min_order_qty, eoq * 0.75),
            eoq,
            eoq * 1.25,
            eoq * 1.5
        ]
        
        cost_comparison = []
        for qty in quantities:
            qty = max(item.min_order_qty, math.ceil(qty))
            hc = (qty / 2) * holding_cost_per_unit
            oc = (annual_demand / qty) * ordering_cost
            cost_comparison.append({
                "quantity": qty,
                "holding_cost": hc,
                "ordering_cost": oc,
                "total_cost": hc + oc
            })
        
        return {
            "sku": sku,
            "annual_demand": annual_demand,
            "eoq": eoq,
            "orders_per_year": annual_demand / eoq,
            "days_between_orders": 365 / (annual_demand / eoq) if annual_demand > 0 else 0,
            "total_annual_cost": total_cost,
            "holding_cost_at_eoq": total_holding_cost,
            "ordering_cost_at_eoq": total_ordering_cost,
            "cost_comparison": cost_comparison,
            "savings_vs_current": None  # Would need current order quantity
        }
    
    # Helper methods
    @staticmethod
    def _get_z_score(service_level: float) -> float:
        """Get Z-score for service level using approximation."""
        # Common service levels and their Z-scores
        z_scores = {
            0.80: 0.842,
            0.85: 1.036,
            0.90: 1.282,
            0.92: 1.405,
            0.95: 1.645,
            0.97: 1.881,
            0.98: 2.054,
            0.99: 2.326,
            0.995: 2.576,
            0.999: 3.090,
        }
        
        # Find closest service level
        closest = min(z_scores.keys(), key=lambda x: abs(x - service_level))
        return z_scores[closest]
    
    @staticmethod
    def _normal_cdf(z: float) -> float:
        """Approximate standard normal CDF using error function."""
        # Approximation using Abramowitz and Stegun formula
        a1 = 0.254829592
        a2 = -0.284496736
        a3 = 1.421413741
        a4 = -1.453152027
        a5 = 1.061405429
        p = 0.3275911
        
        sign = 1 if z >= 0 else -1
        z = abs(z) / math.sqrt(2)
        
        t = 1.0 / (1.0 + p * z)
        y = 1.0 - (((((a5 * t + a4) * t) + a3) * t + a2) * t + a1) * t * math.exp(-z * z)
        
        return 0.5 * (1.0 + sign * y)


def create_inventory_manager(
    items: List[Dict[str, Any]], 
    service_level: float = 0.95
) -> InventoryManager:
    """
    Create an InventoryManager from a list of item dictionaries.
    
    Args:
        items: List of item dictionaries with keys:
               - sku, name, current_stock, unit_cost, unit_price
               - Optional: lead_time_days, daily_demand_avg, daily_demand_std, etc.
        service_level: Target service level
        
    Returns:
        Configured InventoryManager
    """
    manager = InventoryManager(service_level=service_level)
    
    for item_data in items:
        item = InventoryItem(
            sku=item_data["sku"],
            name=item_data["name"],
            current_stock=item_data["current_stock"],
            unit_cost=item_data["unit_cost"],
            unit_price=item_data.get("unit_price", item_data["unit_cost"] * 1.5),
            lead_time_days=item_data.get("lead_time_days", 7),
            daily_demand_avg=item_data.get("daily_demand_avg", 0.0),
            daily_demand_std=item_data.get("daily_demand_std", 0.0),
            max_stock=item_data.get("max_stock"),
            min_order_qty=item_data.get("min_order_qty", 1.0),
            category=item_data.get("category", "")
        )
        manager.add_item(item)
    
    return manager


def calculate_reorder_point(
    daily_demand: float,
    lead_time_days: int,
    safety_stock: float = 0
) -> float:
    """
    Quick function to calculate reorder point.
    
    Args:
        daily_demand: Average daily demand
        lead_time_days: Lead time in days
        safety_stock: Safety stock quantity
        
    Returns:
        Reorder point
    """
    return (daily_demand * lead_time_days) + safety_stock


def calculate_safety_stock(
    daily_demand_std: float,
    lead_time_days: int,
    service_level: float = 0.95
) -> float:
    """
    Quick function to calculate safety stock.
    
    Args:
        daily_demand_std: Standard deviation of daily demand
        lead_time_days: Lead time in days
        service_level: Target service level
        
    Returns:
        Safety stock quantity
    """
    z_score = InventoryManager._get_z_score(service_level)
    return z_score * daily_demand_std * math.sqrt(lead_time_days)


def calculate_eoq(
    annual_demand: float,
    ordering_cost: float,
    unit_cost: float,
    holding_cost_rate: float = 0.25
) -> float:
    """
    Quick function to calculate Economic Order Quantity.
    
    Args:
        annual_demand: Annual demand in units
        ordering_cost: Cost per order
        unit_cost: Unit cost
        holding_cost_rate: Holding cost as percentage of unit cost
        
    Returns:
        Optimal order quantity
    """
    holding_cost = unit_cost * holding_cost_rate
    if holding_cost == 0:
        return annual_demand
    return math.sqrt((2 * annual_demand * ordering_cost) / holding_cost)


def classify_inventory(
    items: List[Dict[str, Any]],
    value_threshold_a: float = 0.80,
    value_threshold_b: float = 0.95
) -> Dict[str, ABCClass]:
    """
    Quick ABC classification of inventory items.
    
    Args:
        items: List of dictionaries with 'sku' and 'value' keys
        value_threshold_a: Cumulative value threshold for Class A
        value_threshold_b: Cumulative value threshold for Class B
        
    Returns:
        Dictionary mapping SKU to ABC classification
    """
    # Sort by value descending
    sorted_items = sorted(items, key=lambda x: x.get("value", 0), reverse=True)
    
    total_value = sum(item.get("value", 0) for item in items)
    if total_value == 0:
        return {item["sku"]: ABCClass.C for item in items}
    
    classifications = {}
    cumulative = 0.0
    
    for item in sorted_items:
        cumulative += item.get("value", 0)
        pct = cumulative / total_value
        
        if pct <= value_threshold_a:
            classifications[item["sku"]] = ABCClass.A
        elif pct <= value_threshold_b:
            classifications[item["sku"]] = ABCClass.B
        else:
            classifications[item["sku"]] = ABCClass.C
    
    return classifications


# Export public API
__all__ = [
    "InventoryManager",
    "InventoryItem",
    "InventorySummary",
    "StockStatus",
    "ABCClass",
    "create_inventory_manager",
    "calculate_reorder_point",
    "calculate_safety_stock",
    "calculate_eoq",
    "classify_inventory",
]
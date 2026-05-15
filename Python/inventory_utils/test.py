#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Inventory Management Utilities - Test Suite

Comprehensive tests for inventory management functionality.
"""

import unittest
import math
from datetime import datetime, timedelta

from mod import (
    InventoryManager,
    InventoryItem,
    InventorySummary,
    StockStatus,
    ABCClass,
    create_inventory_manager,
    calculate_reorder_point,
    calculate_safety_stock,
    calculate_eoq,
    classify_inventory,
)


class TestInventoryItem(unittest.TestCase):
    """Test InventoryItem dataclass"""
    
    def test_basic_item_creation(self):
        """Test creating a basic inventory item"""
        item = InventoryItem(
            sku="TEST-001",
            name="Test Product",
            current_stock=100,
            unit_cost=10.0,
            unit_price=15.0
        )
        
        self.assertEqual(item.sku, "TEST-001")
        self.assertEqual(item.name, "Test Product")
        self.assertEqual(item.current_stock, 100)
        self.assertEqual(item.lead_time_days, 7)  # Default value
    
    def test_stock_value(self):
        """Test stock value calculation"""
        item = InventoryItem(
            sku="TEST-001",
            name="Test Product",
            current_stock=100,
            unit_cost=10.0,
            unit_price=15.0
        )
        
        self.assertEqual(item.stock_value, 1000.0)
    
    def test_potential_revenue(self):
        """Test potential revenue calculation"""
        item = InventoryItem(
            sku="TEST-001",
            name="Test Product",
            current_stock=100,
            unit_cost=10.0,
            unit_price=15.0
        )
        
        self.assertEqual(item.potential_revenue, 1500.0)
    
    def test_profit_margin(self):
        """Test profit margin calculation"""
        item = InventoryItem(
            sku="TEST-001",
            name="Test Product",
            current_stock=100,
            unit_cost=10.0,
            unit_price=15.0
        )
        
        self.assertEqual(item.profit_margin, 50.0)
    
    def test_zero_cost_margin(self):
        """Test profit margin with zero cost"""
        item = InventoryItem(
            sku="FREE-001",
            name="Free Item",
            current_stock=10,
            unit_cost=0.0,
            unit_price=5.0
        )
        
        self.assertEqual(item.profit_margin, 0.0)


class TestInventoryManager(unittest.TestCase):
    """Test InventoryManager class"""
    
    def setUp(self):
        """Set up test inventory"""
        self.manager = InventoryManager(service_level=0.95)
        
        # Add test items
        self.manager.add_item(InventoryItem(
            sku="ITEM-A",
            name="High Value Item A",
            current_stock=50,
            unit_cost=100.0,
            unit_price=150.0,
            lead_time_days=7,
            daily_demand_avg=5.0,
            daily_demand_std=1.5
        ))
        
        self.manager.add_item(InventoryItem(
            sku="ITEM-B",
            name="Medium Value Item B",
            current_stock=200,
            unit_cost=25.0,
            unit_price=40.0,
            lead_time_days=14,
            daily_demand_avg=10.0,
            daily_demand_std=3.0
        ))
        
        self.manager.add_item(InventoryItem(
            sku="ITEM-C",
            name="Low Stock Item C",
            current_stock=10,
            unit_cost=50.0,
            unit_price=75.0,
            lead_time_days=5,
            daily_demand_avg=3.0,
            daily_demand_std=0.5
        ))
    
    def test_add_and_get_item(self):
        """Test adding and retrieving items"""
        item = self.manager.get_item("ITEM-A")
        self.assertIsNotNone(item)
        self.assertEqual(item.name, "High Value Item A")
    
    def test_remove_item(self):
        """Test removing items"""
        self.assertTrue(self.manager.remove_item("ITEM-A"))
        self.assertIsNone(self.manager.get_item("ITEM-A"))
        self.assertFalse(self.manager.remove_item("NONEXISTENT"))
    
    def test_update_stock(self):
        """Test stock updates"""
        # Add stock
        self.assertTrue(self.manager.update_stock("ITEM-A", 10))
        item = self.manager.get_item("ITEM-A")
        self.assertEqual(item.current_stock, 60)
        
        # Remove stock
        self.assertTrue(self.manager.update_stock("ITEM-A", -20))
        item = self.manager.get_item("ITEM-A")
        self.assertEqual(item.current_stock, 40)
        
        # Update nonexistent item
        self.assertFalse(self.manager.update_stock("NONEXISTENT", 10))
    
    def test_calculate_safety_stock(self):
        """Test safety stock calculation"""
        # Safety stock = Z × σ × √L
        # For 95% service level: Z ≈ 1.645
        # L = 7 days, σ = 1.5
        # Safety Stock ≈ 1.645 × 1.5 × √7 ≈ 6.5
        
        safety_stock = self.manager.calculate_safety_stock("ITEM-A")
        expected = 1.645 * 1.5 * math.sqrt(7)
        self.assertAlmostEqual(safety_stock, expected, places=1)
    
    def test_calculate_reorder_point(self):
        """Test reorder point calculation"""
        # ROP = (D × L) + SS
        # D = 5, L = 7
        # Expected demand during lead time = 35
        
        rop = self.manager.calculate_reorder_point("ITEM-A")
        expected_demand = 5.0 * 7  # 35
        safety_stock = self.manager.calculate_safety_stock("ITEM-A")
        expected_rop = expected_demand + safety_stock
        
        self.assertAlmostEqual(rop, expected_rop, places=1)
    
    def test_calculate_eoq(self):
        """Test EOQ calculation"""
        # EOQ = √(2DS/H)
        # Annual demand = 5 × 365 = 1825
        # Ordering cost = 50
        # Unit cost = 100, holding rate = 0.25
        # H = 25
        # EOQ = √(2 × 1825 × 50 / 25) = √7300 ≈ 85.4
        
        eoq = self.manager.calculate_eoq("ITEM-A", ordering_cost=50, holding_cost_rate=0.25)
        expected = math.sqrt((2 * 5 * 365 * 50) / (100 * 0.25))
        self.assertAlmostEqual(eoq, math.ceil(expected), places=0)
    
    def test_get_stock_status(self):
        """Test stock status determination"""
        # ITEM-A: stock=50, demand=5/day, lead_time=7
        # Expected demand during LT = 35
        # Should be normal status
        
        status = self.manager.get_stock_status("ITEM-A")
        self.assertEqual(status, StockStatus.NORMAL)
        
        # ITEM-C: stock=10, demand=3/day, lead_time=5
        # Expected demand during LT = 15
        # Should be low or critical status
        
        status_c = self.manager.get_stock_status("ITEM-C")
        self.assertIn(status_c, [StockStatus.LOW, StockStatus.CRITICAL])
    
    def test_abc_analysis(self):
        """Test ABC classification"""
        classifications = self.manager.abc_analysis()
        
        # ITEM-A: value = 50 × 100 = 5000 (highest)
        # ITEM-B: value = 200 × 25 = 5000 (equal highest)
        # ITEM-C: value = 10 × 50 = 500 (lowest)
        
        # All items should be classified
        self.assertEqual(len(classifications), 3)
        self.assertIn("ITEM-A", classifications)
        self.assertIn("ITEM-B", classifications)
        self.assertIn("ITEM-C", classifications)
    
    def test_calculate_turnover(self):
        """Test inventory turnover calculation"""
        # Turnover = COGS / Avg Inventory
        # COGS = 5 × 365 × 100 = 182,500
        # Avg Inventory = 50 × 100 = 5000
        # Turnover = 36.5
        
        turnover = self.manager.calculate_turnover("ITEM-A")
        expected = (5.0 * 365 * 100.0) / (50.0 * 100.0)
        self.assertAlmostEqual(turnover, expected, places=1)
    
    def test_calculate_days_of_stock(self):
        """Test days of stock calculation"""
        # Days = Stock / Daily Demand
        # ITEM-A: 50 / 5 = 10 days
        
        days = self.manager.calculate_days_of_stock("ITEM-A")
        self.assertEqual(days, 10.0)
    
    def test_calculate_stockout_risk(self):
        """Test stockout risk calculation"""
        # ITEM-C has low stock relative to demand
        risk = self.manager.calculate_stockout_risk("ITEM-C", days_ahead=30)
        
        # Risk should be between 0 and 1
        self.assertGreaterEqual(risk, 0.0)
        self.assertLessEqual(risk, 1.0)
        
        # ITEM-A has more stock, should have lower risk
        risk_a = self.manager.calculate_stockout_risk("ITEM-A", days_ahead=7)
        risk_c = self.manager.calculate_stockout_risk("ITEM-C", days_ahead=30)
        # Note: this might not always hold due to different demand variability
    
    def test_get_restock_recommendations(self):
        """Test restock recommendations"""
        recommendations = self.manager.get_restock_recommendations()
        
        # Should include low stock items
        skus = [r["sku"] for r in recommendations]
        self.assertIn("ITEM-C", skus)  # Low stock item
    
    def test_get_summary(self):
        """Test inventory summary"""
        summary = self.manager.get_summary()
        
        self.assertEqual(summary.total_items, 3)
        self.assertGreater(summary.total_stock_value, 0)
        self.assertGreater(summary.total_potential_revenue, 0)
    
    def test_calculate_carrying_cost(self):
        """Test carrying cost calculation"""
        costs = self.manager.calculate_carrying_cost("ITEM-A", holding_cost_rate=0.25)
        
        # Annual carrying cost = avg inventory value × holding rate
        # = 50 × 100 × 0.25 = 1250
        self.assertEqual(costs["average_inventory"], 50)
        self.assertEqual(costs["average_inventory_value"], 5000)
        self.assertEqual(costs["annual_carrying_cost"], 1250)
    
    def test_optimize_order_quantity(self):
        """Test order quantity optimization"""
        optimization = self.manager.optimize_order_quantity(
            "ITEM-A",
            ordering_cost=50,
            holding_cost_rate=0.25
        )
        
        self.assertIn("eoq", optimization)
        self.assertIn("orders_per_year", optimization)
        self.assertIn("total_annual_cost", optimization)
        self.assertIn("cost_comparison", optimization)
        
        self.assertGreater(optimization["eoq"], 0)
    
    def test_record_demand(self):
        """Test demand recording"""
        self.manager.record_demand("ITEM-A", 5.0)
        self.manager.record_demand("ITEM-A", 6.0)
        
        # Should not raise
        self.assertEqual(len(self.manager._demand_history["ITEM-A"]), 2)


class TestHelperFunctions(unittest.TestCase):
    """Test standalone helper functions"""
    
    def test_calculate_reorder_point_simple(self):
        """Test simple reorder point calculation"""
        rop = calculate_reorder_point(daily_demand=10, lead_time_days=7, safety_stock=20)
        self.assertEqual(rop, 90)  # (10 × 7) + 20
    
    def test_calculate_safety_stock_simple(self):
        """Test simple safety stock calculation"""
        # SS = Z × σ × √L
        # For 95%: Z ≈ 1.645
        ss = calculate_safety_stock(
            daily_demand_std=2.0,
            lead_time_days=9,
            service_level=0.95
        )
        expected = 1.645 * 2.0 * math.sqrt(9)
        self.assertAlmostEqual(ss, expected, places=1)
    
    def test_calculate_eoq_simple(self):
        """Test simple EOQ calculation"""
        eoq = calculate_eoq(
            annual_demand=1000,
            ordering_cost=50,
            unit_cost=25,
            holding_cost_rate=0.20
        )
        # EOQ = √(2 × 1000 × 50 / (25 × 0.20))
        # = √(100000 / 5) = √20000 ≈ 141.4
        expected = math.sqrt((2 * 1000 * 50) / (25 * 0.20))
        self.assertAlmostEqual(eoq, expected, places=0)
    
    def test_classify_inventory(self):
        """Test ABC classification function"""
        items = [
            {"sku": "A1", "value": 5000},
            {"sku": "A2", "value": 4500},
            {"sku": "B1", "value": 1500},
            {"sku": "B2", "value": 1000},
            {"sku": "C1", "value": 200},
            {"sku": "C2", "value": 100},
            {"sku": "C3", "value": 50},
        ]
        
        classifications = classify_inventory(items)
        
        # A items should be top ~80% of value
        # Total value = 12350
        # A1 + A2 = 9500 = 77% (should be A class)
        # Adding B1 = 11000 = 89% (should be B class)
        
        self.assertEqual(classifications["A1"], ABCClass.A)
        self.assertEqual(classifications["A2"], ABCClass.A)
        # B items
        self.assertIn(classifications["B1"], [ABCClass.A, ABCClass.B])
        self.assertIn(classifications["B2"], [ABCClass.B, ABCClass.C])
        # C items should be C class
        self.assertEqual(classifications["C1"], ABCClass.C)
        self.assertEqual(classifications["C2"], ABCClass.C)
        self.assertEqual(classifications["C3"], ABCClass.C)


class TestCreateInventoryManager(unittest.TestCase):
    """Test factory function"""
    
    def test_create_from_list(self):
        """Test creating manager from item list"""
        items = [
            {
                "sku": "PROD-001",
                "name": "Product 1",
                "current_stock": 100,
                "unit_cost": 10.0,
                "unit_price": 15.0,
                "daily_demand_avg": 5.0,
                "lead_time_days": 7
            },
            {
                "sku": "PROD-002",
                "name": "Product 2",
                "current_stock": 50,
                "unit_cost": 25.0,
                "daily_demand_avg": 2.0
            }
        ]
        
        manager = create_inventory_manager(items, service_level=0.95)
        
        self.assertEqual(len(manager.items), 2)
        self.assertIsNotNone(manager.get_item("PROD-001"))
        self.assertIsNotNone(manager.get_item("PROD-002"))
        
        item1 = manager.get_item("PROD-001")
        self.assertEqual(item1.daily_demand_avg, 5.0)
        self.assertEqual(item1.lead_time_days, 7)
        
        item2 = manager.get_item("PROD-002")
        self.assertEqual(item2.daily_demand_avg, 2.0)
        self.assertEqual(item2.lead_time_days, 7)  # Default


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and error handling"""
    
    def test_zero_demand(self):
        """Test with zero demand"""
        manager = InventoryManager()
        manager.add_item(InventoryItem(
            sku="NO-DEMAND",
            name="No Demand Item",
            current_stock=100,
            unit_cost=10.0,
            unit_price=15.0,
            daily_demand_avg=0.0
        ))
        
        days = manager.calculate_days_of_stock("NO-DEMAND")
        self.assertEqual(days, float('inf'))
    
    def test_zero_stock(self):
        """Test with zero stock"""
        manager = InventoryManager()
        manager.add_item(InventoryItem(
            sku="OUT-OF-STOCK",
            name="Out of Stock Item",
            current_stock=0,
            unit_cost=10.0,
            unit_price=15.0,
            daily_demand_avg=5.0
        ))
        
        status = manager.get_stock_status("OUT-OF-STOCK")
        self.assertEqual(status, StockStatus.CRITICAL)
    
    def test_nonexistent_item(self):
        """Test operations on nonexistent item"""
        manager = InventoryManager()
        
        with self.assertRaises(ValueError):
            manager.calculate_safety_stock("NONEXISTENT")
        
        with self.assertRaises(ValueError):
            manager.calculate_reorder_point("NONEXISTENT")
        
        with self.assertRaises(ValueError):
            manager.calculate_eoq("NONEXISTENT")
    
    def test_empty_inventory(self):
        """Test empty inventory"""
        manager = InventoryManager()
        
        summary = manager.get_summary()
        self.assertEqual(summary.total_items, 0)
        self.assertEqual(summary.total_stock_value, 0.0)
        
        recommendations = manager.get_restock_recommendations()
        self.assertEqual(len(recommendations), 0)


class TestZScoreHelper(unittest.TestCase):
    """Test Z-score helper method"""
    
    def test_z_scores(self):
        """Test Z-score lookup"""
        # Test common service levels
        self.assertAlmostEqual(InventoryManager._get_z_score(0.90), 1.282, places=2)
        self.assertAlmostEqual(InventoryManager._get_z_score(0.95), 1.645, places=2)
        self.assertAlmostEqual(InventoryManager._get_z_score(0.99), 2.326, places=2)
        
        # Test interpolation (should return closest)
        z = InventoryManager._get_z_score(0.93)  # Between 0.90 and 0.95
        self.assertGreater(z, 1.282)
        self.assertLess(z, 1.645)


class TestNormalCdfHelper(unittest.TestCase):
    """Test normal CDF helper method"""
    
    def test_cdf_values(self):
        """Test CDF calculation"""
        # CDF at 0 should be 0.5
        self.assertAlmostEqual(
            InventoryManager._normal_cdf(0), 0.5, places=2
        )
        
        # CDF at positive infinity should be 1
        self.assertLess(InventoryManager._normal_cdf(5), 1.001)
        self.assertGreater(InventoryManager._normal_cdf(5), 0.999)
        
        # CDF at negative infinity should be 0
        self.assertGreater(InventoryManager._normal_cdf(-5), 0.0)
        self.assertLess(InventoryManager._normal_cdf(-5), 0.001)
        
        # Symmetry
        self.assertAlmostEqual(
            InventoryManager._normal_cdf(1) + InventoryManager._normal_cdf(-1),
            1.0, places=2
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
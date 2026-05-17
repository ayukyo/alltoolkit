"""
Tests for Caffeine Metabolism Utils
"""

import unittest
from datetime import datetime, timedelta
import math
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    CaffeineMetabolismTracker,
    CaffeineEntry,
    BEVERAGE_DATABASE,
    calculate_caffeine_decay,
    calculate_half_life_from_data,
    estimate_caffeine_sensitivity,
    caffeine_equivalent
)


class TestCaffeineEntry(unittest.TestCase):
    """Test CaffeineEntry class."""
    
    def test_create_entry(self):
        """Test creating a basic entry."""
        now = datetime.now()
        entry = CaffeineEntry(100, now, "test_coffee", 45)
        
        self.assertEqual(entry.amount_mg, 100)
        self.assertEqual(entry.timestamp, now)
        self.assertEqual(entry.source, "test_coffee")
        self.assertEqual(entry.absorption_delay_minutes, 45)
    
    def test_entry_to_dict(self):
        """Test serialization to dict."""
        now = datetime.now()
        entry = CaffeineEntry(150, now, "espresso", 30)
        data = entry.to_dict()
        
        self.assertEqual(data["amount_mg"], 150)
        self.assertEqual(data["source"], "espresso")
        self.assertEqual(data["absorption_delay_minutes"], 30)
        self.assertIn("timestamp", data)
    
    def test_entry_from_dict(self):
        """Test deserialization from dict."""
        now = datetime.now()
        data = {
            "amount_mg": 200,
            "timestamp": now.isoformat(),
            "source": "energy_drink",
            "absorption_delay_minutes": 20
        }
        entry = CaffeineEntry.from_dict(data)
        
        self.assertEqual(entry.amount_mg, 200)
        self.assertEqual(entry.source, "energy_drink")
        self.assertEqual(entry.absorption_delay_minutes, 20)
    
    def test_entry_from_dict_defaults(self):
        """Test deserialization with missing optional fields."""
        now = datetime.now()
        data = {
            "amount_mg": 100,
            "timestamp": now.isoformat()
        }
        entry = CaffeineEntry.from_dict(data)
        
        self.assertEqual(entry.source, "custom")
        self.assertEqual(entry.absorption_delay_minutes, 45)


class TestCaffeineMetabolismTracker(unittest.TestCase):
    """Test CaffeineMetabolismTracker class."""
    
    def test_create_tracker(self):
        """Test creating a tracker with default settings."""
        tracker = CaffeineMetabolismTracker()
        
        self.assertEqual(tracker.half_life_hours, 5.0)
        self.assertEqual(tracker.sleep_safe_threshold_mg, 25)
        self.assertEqual(len(tracker.entries), 0)
    
    def test_create_tracker_custom(self):
        """Test creating a tracker with custom settings."""
        tracker = CaffeineMetabolismTracker(
            half_life_hours=6.0,
            sleep_safe_threshold_mg=50
        )
        
        self.assertEqual(tracker.half_life_hours, 6.0)
        self.assertEqual(tracker.sleep_safe_threshold_mg, 50)
    
    def test_invalid_half_life(self):
        """Test that invalid half-life raises error."""
        with self.assertRaises(ValueError):
            CaffeineMetabolismTracker(half_life_hours=0)
        
        with self.assertRaises(ValueError):
            CaffeineMetabolismTracker(half_life_hours=-1)
    
    def test_consume(self):
        """Test logging a caffeine consumption."""
        tracker = CaffeineMetabolismTracker()
        entry = tracker.consume(100)
        
        self.assertEqual(len(tracker.entries), 1)
        self.assertEqual(entry.amount_mg, 100)
        self.assertEqual(entry.source, "custom")
    
    def test_consume_invalid_amount(self):
        """Test that invalid amount raises error."""
        tracker = CaffeineMetabolismTracker()
        
        with self.assertRaises(ValueError):
            tracker.consume(0)
        
        with self.assertRaises(ValueError):
            tracker.consume(-50)
    
    def test_consume_beverage(self):
        """Test consuming a predefined beverage."""
        tracker = CaffeineMetabolismTracker()
        entry = tracker.consume_beverage("drip_coffee_medium")
        
        self.assertEqual(entry.amount_mg, 165)
        self.assertEqual(entry.source, "drip_coffee_medium")
    
    def test_consume_beverage_custom_amount(self):
        """Test consuming a beverage with custom amount."""
        tracker = CaffeineMetabolismTracker()
        entry = tracker.consume_beverage("drip_coffee_medium", custom_amount_mg=200)
        
        self.assertEqual(entry.amount_mg, 200)
    
    def test_consume_beverage_unknown(self):
        """Test that unknown beverage raises error."""
        tracker = CaffeineMetabolismTracker()
        
        with self.assertRaises(ValueError):
            tracker.consume_beverage("unknown_beverage")
    
    def test_get_current_level_immediate(self):
        """Test level immediately after consumption (during absorption)."""
        tracker = CaffeineMetabolismTracker()
        now = datetime.now()
        
        tracker.consume(100, timestamp=now)
        level = tracker.get_current_level(now)
        
        # At time 0, absorption is at 0
        self.assertAlmostEqual(level, 0, places=1)
    
    def test_get_current_level_after_absorption(self):
        """Test level after absorption phase."""
        tracker = CaffeineMetabolismTracker()
        now = datetime.now()
        
        # Default absorption is 45 minutes
        tracker.consume(100, timestamp=now)
        
        # After 45 minutes, should be at full amount
        after_absorption = now + timedelta(minutes=45)
        level = tracker.get_current_level(after_absorption)
        
        self.assertAlmostEqual(level, 100, places=1)
    
    def test_get_current_level_decay(self):
        """Test caffeine decay over time."""
        tracker = CaffeineMetabolismTracker(half_life_hours=5.0)
        now = datetime.now()
        
        tracker.consume(100, timestamp=now)
        
        # After one half-life (5 hours), should be at 50%
        after_half_life = now + timedelta(minutes=45) + timedelta(hours=5)
        level = tracker.get_current_level(after_half_life)
        
        self.assertAlmostEqual(level, 50, places=1)
    
    def test_get_current_level_multiple_entries(self):
        """Test level with multiple caffeine entries."""
        tracker = CaffeineMetabolismTracker()
        now = datetime.now()
        
        tracker.consume(100, timestamp=now)
        tracker.consume(50, timestamp=now + timedelta(hours=1))
        
        # After both are fully absorbed (first entry at now+45min, second at now+1hr45min)
        # At now+2hr45min: first entry has decayed ~2hr, second entry just absorbed
        later = now + timedelta(hours=2, minutes=45)
        level = tracker.get_current_level(later)
        
        # First entry: 100mg decayed for ~2hr = ~76mg (with 5hr half-life)
        # Second entry: 50mg just absorbed
        # Total ~126mg
        self.assertGreater(level, 100)
        self.assertLess(level, 150)
    
    def test_get_current_level_future_entry(self):
        """Test that future entries are not included."""
        tracker = CaffeineMetabolismTracker()
        now = datetime.now()
        
        tracker.consume(100, timestamp=now)
        tracker.consume(50, timestamp=now + timedelta(hours=10))
        
        level_now = tracker.get_current_level(now + timedelta(minutes=45))
        
        # Should only include the first entry
        self.assertAlmostEqual(level_now, 100, places=1)
    
    def test_time_until_threshold(self):
        """Test calculation of time until safe level."""
        tracker = CaffeineMetabolismTracker(
            half_life_hours=5.0,
            sleep_safe_threshold_mg=25
        )
        now = datetime.now()
        
        tracker.consume(100, timestamp=now)
        
        time_safe = tracker.time_until_threshold(from_time=now + timedelta(minutes=45))
        
        # With 100mg and threshold 25mg (1/4), need 2 half-lives = 10 hours
        self.assertIsNotNone(time_safe)
        # Should be approximately 10 hours
        self.assertGreater(time_safe.total_seconds(), 9 * 3600)
        self.assertLess(time_safe.total_seconds(), 11 * 3600)
    
    def test_time_until_threshold_already_safe(self):
        """Test when already below threshold."""
        tracker = CaffeineMetabolismTracker(sleep_safe_threshold_mg=100)
        
        tracker.consume(50)
        
        time_safe = tracker.time_until_threshold()
        self.assertIsNone(time_safe)
    
    def test_get_sleep_recommendation(self):
        """Test sleep recommendation generation."""
        tracker = CaffeineMetabolismTracker()
        now = datetime.now()
        
        tracker.consume(100, timestamp=now)
        
        bedtime = now + timedelta(hours=12)
        rec = tracker.get_sleep_recommendation(target_bedtime=bedtime, from_time=now)
        
        self.assertIn("current_level_mg", rec)
        self.assertIn("bedtime_level_mg", rec)
        self.assertIn("is_safe_to_sleep", rec)
        self.assertIn("recommended_bedtime", rec)
    
    def test_get_daily_total(self):
        """Test daily total calculation."""
        tracker = CaffeineMetabolismTracker()
        now = datetime.now()
        
        tracker.consume(100, timestamp=now)
        tracker.consume(50, timestamp=now + timedelta(hours=2))
        
        # Add entry for yesterday
        yesterday = now - timedelta(days=1)
        tracker.consume(200, timestamp=yesterday)
        
        total, entries = tracker.get_daily_total(now)
        
        self.assertEqual(total, 150)
        self.assertEqual(len(entries), 2)
    
    def test_get_status(self):
        """Test comprehensive status report."""
        tracker = CaffeineMetabolismTracker()
        now = datetime.now()
        
        tracker.consume(150, timestamp=now)
        tracker.consume(100, timestamp=now + timedelta(hours=1))
        
        status = tracker.get_status(now + timedelta(hours=2))
        
        self.assertEqual(status["daily_entries_count"], 2)
        self.assertTrue(status["within_daily_limit"])
        self.assertEqual(status["total_entries"], 2)
    
    def test_clear_old_entries(self):
        """Test clearing old entries."""
        tracker = CaffeineMetabolismTracker()
        now = datetime.now()
        
        tracker.consume(100, timestamp=now)
        tracker.consume(50, timestamp=now - timedelta(hours=50))
        
        removed = tracker.clear_old_entries(older_than_hours=48)
        
        self.assertEqual(removed, 1)
        self.assertEqual(len(tracker.entries), 1)
    
    def test_export_import_data(self):
        """Test exporting and importing data."""
        tracker1 = CaffeineMetabolismTracker()
        now = datetime.now()
        
        tracker1.consume(100, timestamp=now, source="coffee")
        tracker1.consume(50, timestamp=now + timedelta(hours=1), source="tea")
        
        data = tracker1.export_data()
        
        tracker2 = CaffeineMetabolismTracker()
        imported = tracker2.import_data(data)
        
        self.assertEqual(imported, 2)
        self.assertEqual(len(tracker2.entries), 2)
    
    def test_get_beverage_list(self):
        """Test getting beverage list."""
        beverages = CaffeineMetabolismTracker.get_beverage_list()
        
        self.assertIn("drip_coffee_medium", beverages)
        self.assertIn("espresso_single", beverages)
        self.assertGreater(len(beverages), 30)
    
    def test_search_beverages(self):
        """Test beverage search."""
        results = CaffeineMetabolismTracker.search_beverages("coffee")
        
        # Should find entries with "coffee" in the name
        self.assertIn("drip_coffee_small", results)
        self.assertIn("drip_coffee_medium", results)
        # cold_brew doesn't contain "coffee", won't match
        self.assertNotIn("cold_brew_small", results)
        
        # Search for "brew" should find cold brew
        brew_results = CaffeineMetabolismTracker.search_beverages("brew")
        self.assertIn("cold_brew_small", brew_results)
    
    def test_get_level_history(self):
        """Test level history generation."""
        tracker = CaffeineMetabolismTracker()
        now = datetime.now()
        
        tracker.consume(100, timestamp=now)
        
        start = now
        end = now + timedelta(hours=2)
        
        history = tracker.get_level_history(start, end, interval_minutes=30)
        
        # Should have 5 points (0, 30, 60, 90, 120 min)
        self.assertEqual(len(history), 5)
        self.assertIn("timestamp", history[0])
        self.assertIn("level_mg", history[0])


class TestHelperFunctions(unittest.TestCase):
    """Test standalone helper functions."""
    
    def test_calculate_caffeine_decay(self):
        """Test simple decay calculation."""
        # 100mg after 5 hours (one half-life) should be ~50mg
        result = calculate_caffeine_decay(100, 5, 5)
        self.assertAlmostEqual(result, 50, places=1)
        
        # After 10 hours (two half-lives), should be ~25mg
        result = calculate_caffeine_decay(100, 10, 5)
        self.assertAlmostEqual(result, 25, places=1)
    
    def test_calculate_half_life_from_data(self):
        """Test half-life calculation from observations."""
        # If 100mg becomes 50mg after 5 hours, half-life should be 5
        half_life = calculate_half_life_from_data(100, 50, 5)
        self.assertAlmostEqual(half_life, 5, places=2)
        
        # If 100mg becomes 25mg after 10 hours, half-life should be 5
        half_life = calculate_half_life_from_data(100, 25, 10)
        self.assertAlmostEqual(half_life, 5, places=2)
    
    def test_calculate_half_life_invalid(self):
        """Test half-life calculation with invalid inputs."""
        with self.assertRaises(ValueError):
            calculate_half_life_from_data(0, 50, 5)
        
        with self.assertRaises(ValueError):
            calculate_half_life_from_data(100, 0, 5)
        
        with self.assertRaises(ValueError):
            calculate_half_life_from_data(100, 150, 5)
    
    def test_estimate_caffeine_sensitivity(self):
        """Test sensitivity estimation."""
        result = estimate_caffeine_sensitivity("poor", 4)
        self.assertEqual(result["sensitivity"], "high")
        self.assertEqual(result["estimated_half_life"], 7.0)
        
        result = estimate_caffeine_sensitivity("moderate", 6)
        self.assertEqual(result["sensitivity"], "moderate")
        
        result = estimate_caffeine_sensitivity("good", 2)
        self.assertEqual(result["sensitivity"], "low")
    
    def test_caffeine_equivalent(self):
        """Test caffeine equivalent calculation."""
        result = caffeine_equivalent(330, "drip_coffee_medium")
        
        self.assertEqual(result["input_mg"], 330)
        self.assertEqual(result["reference_caffeine_mg"], 165)
        self.assertAlmostEqual(result["equivalent_units"], 2, places=1)
        self.assertIn("closest_beverages", result)
    
    def test_caffeine_equivalent_unknown_beverage(self):
        """Test equivalent with unknown beverage (should use default)."""
        result = caffeine_equivalent(100, "unknown_beverage")
        
        self.assertEqual(result["input_mg"], 100)
        self.assertEqual(result["reference_beverage"], "drip_coffee_medium")


class TestBeverageDatabase(unittest.TestCase):
    """Test beverage database consistency."""
    
    def test_all_positive_values(self):
        """Test that all caffeine values are positive."""
        for name, mg in BEVERAGE_DATABASE.items():
            self.assertGreater(mg, 0, f"{name} has invalid caffeine value")
    
    def test_database_not_empty(self):
        """Test that database has entries."""
        self.assertGreater(len(BEVERAGE_DATABASE), 30)
    
    def test_reasonable_caffeine_range(self):
        """Test that all values are in reasonable range."""
        for name, mg in BEVERAGE_DATABASE.items():
            self.assertGreater(mg, 0, f"{name} too low")
            self.assertLess(mg, 1000, f"{name} too high")


if __name__ == "__main__":
    unittest.main(verbosity=2)
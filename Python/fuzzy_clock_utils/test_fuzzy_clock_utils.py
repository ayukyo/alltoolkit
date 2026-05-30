# Fuzzy Clock Utils Test

import sys
import os
import unittest
from datetime import datetime, time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fuzzy_clock_utils.mod import (
    FuzzyClock,
    fuzzy_time,
    colloquial_time,
    time_range,
    approximate_time,
    relative_time,
)


class TestFuzzyClock(unittest.TestCase):
    """Test FuzzyClock class."""

    def test_init_defaults(self):
        """Test default initialization."""
        clock = FuzzyClock()
        self.assertEqual(clock.language, "zh")
        self.assertEqual(clock.precision, "fuzzy")
    
    def test_init_custom(self):
        """Test custom initialization."""
        clock = FuzzyClock(language="en", precision="exact")
        self.assertEqual(clock.language, "en")
        self.assertEqual(clock.precision, "exact")


class TestFuzzyTime(unittest.TestCase):
    """Test fuzzy_time function."""

    def test_fuzzy_time_chinese(self):
        """Test Chinese fuzzy time."""
        result = fuzzy_time(hour=3, minute=0, language="zh", precision="fuzzy")
        self.assertIn("点", result)
        self.assertIn("整", result)
    
    def test_fuzzy_time_english(self):
        """Test English fuzzy time."""
        result = fuzzy_time(hour=3, minute=0, language="en", precision="fuzzy")
        self.assertIn("o'clock", result)
    
    def test_fuzzy_time_with_datetime(self):
        """Test fuzzy time with datetime object."""
        dt = datetime(2024, 1, 1, 14, 30)
        result = fuzzy_time(dt=dt, language="zh")
        self.assertIsInstance(result, str)


class TestColloquialTime(unittest.TestCase):
    """Test colloquial_time function."""

    def test_colloquial_morning(self):
        """Test morning colloquial time."""
        result = colloquial_time(hour=8, minute=30, language="zh")
        self.assertIn("早上", result)
    
    def test_colloquial_evening(self):
        """Test evening colloquial time."""
        result = colloquial_time(hour=19, minute=30, language="zh")
        self.assertIn("晚上", result)
    
    def test_colloquial_night(self):
        """Test night colloquial time."""
        result = colloquial_time(hour=23, minute=0, language="zh")
        self.assertIn("夜", result)


class TestTimeRange(unittest.TestCase):
    """Test time_range function."""

    def test_time_range_morning(self):
        """Test morning time range."""
        result = time_range(hour=9, minute=0, language="zh")
        self.assertEqual(result, "上午")
    
    def test_time_range_afternoon(self):
        """Test afternoon time range."""
        result = time_range(hour=15, minute=0, language="zh")
        self.assertEqual(result, "下午")
    
    def test_time_range_evening(self):
        """Test evening time range."""
        result = time_range(hour=18, minute=0, language="zh")
        self.assertEqual(result, "傍晚")
    
    def test_time_range_night(self):
        """Test night time range."""
        result = time_range(hour=23, minute=0, language="zh")
        self.assertEqual(result, "深夜")


class TestApproximateTime(unittest.TestCase):
    """Test approximate_time function."""

    def test_approximate_time_just_after(self):
        """Test just after approximate time."""
        result = approximate_time(hour=10, minute=3, language="zh")
        self.assertIn("刚过", result)
    
    def test_approximate_time_around(self):
        """Test around approximate time."""
        result = approximate_time(hour=10, minute=15, language="zh")
        self.assertIn("左右", result)
    
    def test_approximate_time_almost(self):
        """Test almost approximate time."""
        result = approximate_time(hour=10, minute=55, language="zh")
        self.assertIn("快", result)


class TestRelativeTime(unittest.TestCase):
    """Test relative_time function."""

    def test_relative_time_past(self):
        """Test relative time for past."""
        from datetime import datetime, timedelta
        past = datetime.now() - timedelta(days=2)
        result = relative_time(dt=past, language="zh")
        self.assertIn("天前", result)
    
    def test_relative_time_future(self):
        """Test relative time for future."""
        from datetime import datetime, timedelta
        future = datetime.now() + timedelta(hours=2)
        result = relative_time(dt=future, language="zh")
        self.assertIn("小时后", result)


class TestFuzzyClockPrecision(unittest.TestCase):
    """Test different precision levels."""

    def test_precision_exact(self):
        """Test exact precision."""
        clock = FuzzyClock(language="zh", precision="exact")
        result = clock.fuzzy_time(hour=10, minute=7)
        self.assertIsInstance(result, str)
    
    def test_precision_fuzzy(self):
        """Test fuzzy precision."""
        clock = FuzzyClock(language="zh", precision="fuzzy")
        result = clock.fuzzy_time(hour=10, minute=15)
        self.assertIn("一刻", result)
    
    def test_precision_approximate(self):
        """Test approximate precision."""
        clock = FuzzyClock(language="zh", precision="approximate")
        result = clock.fuzzy_time(hour=10, minute=30)
        self.assertIn("半", result)


class TestHourDisplay(unittest.TestCase):
    """Test hour display functionality."""

    def test_hour_12_format(self):
        """Test 12-hour format."""
        clock = FuzzyClock(language="zh")
        hour = clock._get_hour_display(0, twelve_hour=True)
        self.assertEqual(hour, "十二")
        
        hour = clock._get_hour_display(12, twelve_hour=True)
        self.assertEqual(hour, "十二")
    
    def test_hour_24_to_12(self):
        """Test 24-hour to 12-hour conversion."""
        clock = FuzzyClock(language="zh")
        hour = clock._get_hour_display(13, twelve_hour=True)
        self.assertEqual(hour, "一")


if __name__ == '__main__':
    unittest.main()
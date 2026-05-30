"""
Tests for Fiscal Year Utils
"""

import unittest
from datetime import date, datetime
from fiscal_year_utils.mod import (
    FiscalYearConfig,
    US_FISCAL,
    UK_FISCAL,
    US_NGO_FISCAL,
    RETAIL_FISCAL,
    CALENDAR_FISCAL,
    get_fiscal_year,
    get_fiscal_quarter,
)


class TestFiscalYearConfig(unittest.TestCase):

    def test_us_fiscal_october_start(self):
        """US federal fiscal year starts Oct 1."""
        config = US_FISCAL
        # FY2024 spans Oct 1, 2023 - Sep 30, 2024
        self.assertEqual(config.get_fiscal_year(date(2023, 10, 1)), 2024)
        self.assertEqual(config.get_fiscal_year(date(2024, 9, 30)), 2024)
        # Sep 30, 2023 is still FY2023
        self.assertEqual(config.get_fiscal_year(date(2023, 9, 30)), 2023)
        # Oct 1, 2024 is start of FY2025
        self.assertEqual(config.get_fiscal_year(date(2024, 10, 1)), 2025)

    def test_us_fiscal_quarters(self):
        """US fiscal quarter calculation."""
        config = US_FISCAL
        # FY2024 Q1: Oct-Dec 2023
        self.assertEqual(config.get_fiscal_quarter(date(2023, 10, 15)), 1)
        self.assertEqual(config.get_fiscal_quarter(date(2023, 12, 15)), 1)
        # FY2024 Q2: Jan-Mar 2024
        self.assertEqual(config.get_fiscal_quarter(date(2024, 1, 15)), 2)
        self.assertEqual(config.get_fiscal_quarter(date(2024, 3, 15)), 2)
        # FY2024 Q3: Apr-Jun 2024
        self.assertEqual(config.get_fiscal_quarter(date(2024, 4, 15)), 3)
        self.assertEqual(config.get_fiscal_quarter(date(2024, 6, 15)), 3)
        # FY2024 Q4: Jul-Sep 2024
        self.assertEqual(config.get_fiscal_quarter(date(2024, 7, 15)), 4)
        self.assertEqual(config.get_fiscal_quarter(date(2024, 9, 15)), 4)

    def test_uk_fiscal_april_start(self):
        """UK tax year starts Apr 6."""
        config = UK_FISCAL
        # FY2024: Apr 6, 2023 - Apr 5, 2024
        self.assertEqual(config.get_fiscal_year(date(2023, 4, 6)), 2024)
        self.assertEqual(config.get_fiscal_year(date(2024, 4, 5)), 2024)
        # Apr 5, 2023 is still FY2023
        self.assertEqual(config.get_fiscal_year(date(2023, 4, 5)), 2023)
        # Apr 6, 2024 is FY2025
        self.assertEqual(config.get_fiscal_year(date(2024, 4, 6)), 2025)

    def test_calendar_fiscal(self):
        """Calendar fiscal: FY is identified by ending year (Dec 31)."""
        config = CALENDAR_FISCAL
        # FY2024 spans Jan 1, 2023 - Dec 31, 2023
        self.assertEqual(config.get_fiscal_year(date(2023, 6, 15)), 2024)
        self.assertEqual(config.get_fiscal_year(date(2023, 12, 31)), 2024)
        # FY2025 spans Jan 1, 2024 - Dec 31, 2024
        self.assertEqual(config.get_fiscal_year(date(2024, 6, 15)), 2025)

    def test_fiscal_year_dates(self):
        """Test start/end date calculation."""
        config = US_FISCAL
        # FY2024: Oct 1, 2023 - Sep 30, 2024
        start, end = config.get_fiscal_year_dates(2024)
        self.assertEqual(start, date(2023, 10, 1))
        self.assertEqual(end, date(2024, 9, 30))

    def test_fiscal_quarter_dates(self):
        """Test fiscal quarter date ranges."""
        config = US_FISCAL
        # FY2024 Q1: Oct 1 - Dec 31, 2023
        q1_start, q1_end = config.get_fiscal_quarter_dates(2024, 1)
        self.assertEqual(q1_start, date(2023, 10, 1))
        self.assertEqual(q1_end, date(2023, 12, 31))
        # FY2024 Q2: Jan 1 - Mar 31, 2024
        q2_start, q2_end = config.get_fiscal_quarter_dates(2024, 2)
        self.assertEqual(q2_start, date(2024, 1, 1))
        self.assertEqual(q2_end, date(2024, 3, 31))

    def test_retail_fiscal_february_start(self):
        """Retail fiscal year starts Feb 1."""
        config = RETAIL_FISCAL
        # FY2024: Feb 1, 2023 - Jan 31, 2024
        self.assertEqual(config.get_fiscal_year(date(2024, 1, 31)), 2024)
        # FY2025: Feb 1, 2024 - Jan 31, 2025
        self.assertEqual(config.get_fiscal_year(date(2024, 2, 1)), 2025)

    def test_invalid_start_month(self):
        """Test invalid start_month raises ValueError."""
        with self.assertRaises(ValueError):
            FiscalYearConfig(start_month=13)

    def test_invalid_year_mode(self):
        """Test invalid year_mode raises ValueError."""
        with self.assertRaises(ValueError):
            FiscalYearConfig(year_mode="invalid")

    def test_format_fiscal_year(self):
        """Test fiscal year formatting."""
        config = US_FISCAL
        self.assertEqual(config.format_fiscal_year(2024), "FY2024")

    def test_datetime_input(self):
        """Test that datetime objects are accepted."""
        config = US_FISCAL
        self.assertEqual(config.get_fiscal_year(datetime(2024, 3, 15)), 2024)

    def test_starting_year_mode(self):
        """Test year_mode='starting' identifies FY by its start year."""
        config = FiscalYearConfig(start_month=10, start_day=1, year_mode="starting")
        # FY2024 starts Oct 1, 2024
        self.assertEqual(config.get_fiscal_year(date(2024, 10, 1)), 2024)
        self.assertEqual(config.get_fiscal_year(date(2025, 3, 15)), 2024)
        self.assertEqual(config.get_fiscal_year(date(2024, 9, 30)), 2023)


class TestConvenienceFunctions(unittest.TestCase):

    def test_get_fiscal_year_convenience(self):
        """Test convenience function."""
        # Oct 1, 2023 - Sep 30, 2024 is FY2024
        result = get_fiscal_year(date(2024, 6, 15), start_month=10, start_day=1)
        self.assertEqual(result, 2024)

    def test_get_fiscal_quarter_convenience(self):
        """Test convenience function."""
        # Oct-start fiscal: Q3 = Apr-Jun
        result = get_fiscal_quarter(date(2024, 4, 15), start_month=10, start_day=1)
        self.assertEqual(result, 3)


if __name__ == "__main__":
    unittest.main()
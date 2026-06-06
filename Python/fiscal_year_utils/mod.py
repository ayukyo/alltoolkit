"""
Fiscal Year Utils - Utilities for fiscal year calculations and conversions

This module provides utilities for:
- Determining fiscal year for a given date
- Converting between fiscal year formats (US, UK, custom)
- Calculating fiscal year start/end dates
- Working with fiscal quarters
"""

from datetime import date, datetime, timedelta
from typing import Optional, Tuple


class FiscalYearConfig:
    """Configuration for a fiscal year."""

    def __init__(
        self,
        start_month: int = 1,
        start_day: int = 1,
        year_mode: str = "ending",
        year_anchor: Optional[int] = None,
    ):
        """
        Initialize fiscal year configuration.

        Args:
            start_month: Month when fiscal year starts (1-12).
            start_day: Day of month when fiscal year starts (1-31).
            year_mode: Whether the fiscal year is identified by its
                ending year ("ending") or starting year ("starting").
            year_anchor: If set, forces the fiscal year to end no later
                than this month/day, adjusting the start accordingly.
        """
        if not (1 <= start_month <= 12):
            raise ValueError("start_month must be between 1 and 12")
        if not (1 <= start_day <= 31):
            raise ValueError("start_day must be between 1 and 31")
        if year_mode not in ("ending", "starting"):
            raise ValueError("year_mode must be 'ending' or 'starting'")
        self.start_month = start_month
        self.start_day = start_day
        self.year_mode = year_mode
        self.year_anchor = year_anchor

    def _normalize_day(self, year: int, month: int, day: int) -> int:
        """Clamp day to valid range for the given month/year."""
        if month == 12:
            last_day = 31
        else:
            last_day = (date(year, month + 1, 1) - timedelta(days=1)).day
        return min(day, last_day)

    def _make_date(self, year: int, month: int, day: int) -> date:
        """Create a date, normalizing day if needed."""
        d = self._normalize_day(year, month, day)
        return date(year, month, d)

    def _add_months(self, d: date, months: int) -> date:
        """Add months to a date, adjusting day if necessary."""
        total_months = d.year * 12 + d.month + months - 1
        year = total_months // 12
        month = total_months % 12 + 1
        day = min(d.day, _days_in_month(year, month))
        return date(year, month, day)

    def _add_days(self, d: date, days: int) -> date:
        """Add days to a date."""
        return d + timedelta(days=days)

    def get_fiscal_year(self, dt: Optional[date] = None) -> int:
        """
        Get the fiscal year for a given date.

        Args:
            dt: Date to check. Defaults to today.

        Returns:
            The fiscal year number.
        """
        if dt is None:
            dt = date.today()
        if isinstance(dt, datetime):
            dt = dt.date()

        # Direct computation avoids potentially infinite loop
        dt_tuple = (dt.month, dt.day)
        start_tuple = (self.start_month, self.start_day)
        is_before_fy_start = dt_tuple < start_tuple

        if self.year_mode == "ending":
            return dt.year if is_before_fy_start else dt.year + 1
        else:
            return dt.year if not is_before_fy_start else dt.year - 1

    def _get_start_for_year(self, year: int) -> date:
        """
        Get the start date of the fiscal year with the given number.
        - ending mode: the year is the ending year, so start is 1 year before
        - starting mode: the year is the starting year
        """
        if self.year_mode == "ending":
            # FY Y ends on (Y, start_month, start_day). It starts 1 year before.
            return self._make_date(year - 1, self.start_month, self.start_day)
        else:
            # FY Y starts on (Y, start_month, start_day)
            return self._make_date(year, self.start_month, self.start_day)

    def get_fiscal_quarter(self, dt: Optional[date] = None) -> int:
        """
        Get the fiscal quarter (1-4) for a given date.

        Args:
            dt: Date to check. Defaults to today.

        Returns:
            Fiscal quarter number (1-4).
        """
        if dt is None:
            dt = date.today()
        if isinstance(dt, datetime):
            dt = dt.date()

        fy_year = self.get_fiscal_year(dt)
        fy_start = self._get_start_for_year(fy_year)

        # Count months since fy_start
        months_since_start = (dt.year - fy_start.year) * 12 + (dt.month - fy_start.month)
        if dt.day < fy_start.day:
            months_since_start -= 1
        quarter = (months_since_start // 3)
        return (quarter % 4) + 1

    def get_fiscal_quarter_dates(
        self, fy_year: int, quarter: int
    ) -> Tuple[date, date]:
        """
        Get the start and end dates for a fiscal quarter.

        Args:
            fy_year: Fiscal year.
            quarter: Quarter number (1-4).

        Returns:
            Tuple of (start_date, end_date).
        """
        if quarter not in (1, 2, 3, 4):
            raise ValueError("quarter must be between 1 and 4")

        fy_start = self._get_start_for_year(fy_year)
        q_start = self._add_months(fy_start, (quarter - 1) * 3)
        q_end = self._add_days(self._add_months(q_start, 3), -1)
        return q_start, q_end

    def get_fiscal_year_dates(self, fy_year: Optional[int] = None) -> Tuple[date, date]:
        """
        Get the start and end dates for a fiscal year.

        Args:
            fy_year: Fiscal year number. Defaults to current fiscal year.

        Returns:
            Tuple of (start_date, end_date).
        """
        if fy_year is None:
            fy_year = self.get_fiscal_year()
        fy_start = self._get_start_for_year(fy_year)
        fy_end = self._add_days(self._add_months(fy_start, 12), -1)
        return fy_start, fy_end

    def format_fiscal_year(self, fy_year: Optional[int] = None) -> str:
        """
        Format fiscal year as a string like "FY2024" or "FY24".

        Args:
            fy_year: Fiscal year number. Defaults to current fiscal year.

        Returns:
            Formatted fiscal year string.
        """
        if fy_year is None:
            fy_year = self.get_fiscal_year()
        return f"FY{fy_year}"


def _days_in_month(year: int, month: int) -> int:
    """Return number of days in a month."""
    if month == 12:
        return 31
    return (date(year, month + 1, 1) - date(year, month, 1)).days


# Preset configurations
US_FISCAL = FiscalYearConfig(start_month=10, start_day=1, year_mode="ending")
"""US federal government fiscal year: Oct 1 – Sep 30"""

UK_FISCAL = FiscalYearConfig(start_month=4, start_day=6, year_mode="ending")
"""UK tax year: Apr 6 – Apr 5"""

US_NGO_FISCAL = FiscalYearConfig(start_month=7, start_day=1, year_mode="ending")
"""US nonprofit fiscal year: Jul 1 – Jun 30"""

RETAIL_FISCAL = FiscalYearConfig(start_month=2, start_day=1, year_mode="ending")
"""Retail fiscal year: Feb 1 – Jan 31"""

CALENDAR_FISCAL = FiscalYearConfig(start_month=1, start_day=1, year_mode="ending")
"""Calendar year fiscal (same as calendar year): Jan 1 – Dec 31"""


def get_fiscal_year(
    dt: Optional[date] = None,
    start_month: int = 1,
    start_day: int = 1,
    year_mode: str = "ending",
) -> int:
    """
    Convenience function to get fiscal year for a date.

    Args:
        dt: Date to check. Defaults to today.
        start_month: Month when fiscal year starts (1-12).
        start_day: Day of month when fiscal year starts (1-31).
        year_mode: Whether fiscal year is identified by ending or starting year.

    Returns:
        The fiscal year number.
    """
    config = FiscalYearConfig(start_month=start_month, start_day=start_day, year_mode=year_mode)
    return config.get_fiscal_year(dt)


def get_fiscal_quarter(
    dt: Optional[date] = None,
    start_month: int = 1,
    start_day: int = 1,
) -> int:
    """
    Convenience function to get fiscal quarter for a date.

    Args:
        dt: Date to check. Defaults to today.
        start_month: Month when fiscal year starts (1-12).
        start_day: Day of month when fiscal year starts (1-31).

    Returns:
        The fiscal quarter (1-4).
    """
    config = FiscalYearConfig(start_month=start_month, start_day=start_day)
    return config.get_fiscal_quarter(dt)
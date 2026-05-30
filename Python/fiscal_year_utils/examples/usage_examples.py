"""
Usage Examples for Fiscal Year Utils
"""

from datetime import date
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


def main():
    print("=== Fiscal Year Utils Examples ===\n")

    # Example 1: US Federal Fiscal Year
    print("1. US Federal Fiscal Year (Oct 1 - Sep 30, ending year mode)")
    print("   FY number = the year it ends in")
    test_dates = [
        date(2023, 10, 1),   # start of FY2024
        date(2024, 6, 15),
        date(2024, 9, 30),   # end of FY2024
        date(2024, 10, 1),   # start of FY2025
    ]
    for d in test_dates:
        fy = US_FISCAL.get_fiscal_year(d)
        fq = US_FISCAL.get_fiscal_quarter(d)
        print(f"   {d} -> FY{fy} Q{fq}")

    print()

    # Example 2: Custom Fiscal Year
    print("2. Custom Fiscal Year (Apr 1 - Mar 31)")
    custom = FiscalYearConfig(start_month=4, start_day=1, year_mode="ending")
    dates2 = [date(2024, 3, 31), date(2024, 4, 1), date(2025, 3, 31), date(2025, 4, 1)]
    for d in dates2:
        fy = custom.get_fiscal_year(d)
        fq = custom.get_fiscal_quarter(d)
        print(f"   {d} -> FY{fy} Q{fq}")

    print()

    # Example 3: Fiscal Year Date Ranges
    print("3. Fiscal Year Date Ranges for FY2025 (US Federal)")
    start, end = US_FISCAL.get_fiscal_year_dates(2025)
    print(f"   FY2025: {start} to {end}")

    print()
    print("4. Fiscal Quarter Date Ranges for FY2025 Q2")
    q_start, q_end = US_FISCAL.get_fiscal_quarter_dates(2025, 2)
    print(f"   Q2: {q_start} to {q_end}")

    print()

    # Example 5: UK Tax Year
    print("5. UK Tax Year (Apr 6 - Apr 5, ending year mode)")
    print("   FY ends Apr 5, starts previous Apr 6")
    uk_dates = [
        date(2023, 4, 5), date(2023, 4, 6),
        date(2024, 4, 5), date(2024, 4, 6),
        date(2025, 4, 5), date(2025, 4, 6),
    ]
    for d in uk_dates:
        fy = UK_FISCAL.get_fiscal_year(d)
        print(f"   {d} -> FY{fy}")

    print()

    # Example 6: Convenience functions
    print("6. Convenience Functions")
    d = date(2024, 6, 15)
    fy = get_fiscal_year(d, start_month=7, start_day=1)
    fq = get_fiscal_quarter(d, start_month=7, start_day=1)
    print(f"   FY from Jul 1 start: FY{fy} Q{fq}")

    print()

    # Example 7: Retail Fiscal Year
    print("7. Retail Fiscal Year (Feb 1 - Jan 31)")
    print(f"   Jan 31, 2024 -> FY{RETAIL_FISCAL.get_fiscal_year(date(2024, 1, 31))}")
    print(f"   Feb 1, 2024 -> FY{RETAIL_FISCAL.get_fiscal_year(date(2024, 2, 1))}")

    print()
    print("=== All Examples Complete ===")


if __name__ == "__main__":
    main()
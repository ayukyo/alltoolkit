#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - SLA Calculator Utilities Examples
===============================================
Demonstration of sla_utils module capabilities.

Run: python examples/usage_examples.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    TimeUnit,
    SLATier,
    calculate_uptime_percent,
    calculate_downtime_from_uptime,
    calculate_sla_compliance,
    format_downtime,
    compare_sla_tiers,
    calculate_mttr,
    calculate_incident_impact,
    uptime_to_nines,
    nines_to_uptime,
    calculate_annual_cost_of_downtime,
    verify_sla_met,
)


def example_basic_uptime_calculation():
    """Calculate uptime percentage from downtime."""
    print("=== Basic Uptime Calculation ===")

    # 99.9% uptime for one day means only 86.4 seconds downtime
    uptime = calculate_uptime_percent(86400, 86.4)
    print(f"Uptime with 86.4s downtime in 24h: {uptime:.2f}%")  # ~99.9%

    # Full uptime
    uptime = calculate_uptime_percent(86400, 0)
    print(f"Uptime with 0s downtime: {uptime:.2f}%")


def example_downtime_calculation():
    """Calculate allowed downtime from uptime percentage."""
    print("\n=== Downtime Calculation ===")

    # Calculate allowed downtime for 99.9% uptime over different periods
    for unit in [TimeUnit.DAY, TimeUnit.MONTH, TimeUnit.YEAR]:
        downtime = calculate_downtime_from_uptime(99.9, unit)
        print(f"99.9% downtime per {unit.name.lower()}: {format_downtime(downtime)}")


def example_sla_tier_comparison():
    """Compare different SLA tiers."""
    print("\n=== SLA Tier Comparison ===")

    tiers = [
        SLATier("Bronze", 99.0, 7200, 86400),    # 99.0% uptime, 2h response, 24h resolution
        SLATier("Silver", 99.9, 3600, 43200),    # 99.9% uptime, 1h response, 12h resolution
        SLATier("Gold", 99.99, 1800, 21600),     # 99.99% uptime, 30min response, 6h resolution
        SLATier("Platinum", 99.999, 900, 7200),  # 99.999% uptime, 15min response, 2h resolution
    ]

    result = compare_sla_tiers(tiers)

    print(f"Best tier: {result['best_tier'].name} ({result['best_tier'].uptime_percent}%)")
    print(f"Worst tier: {result['worst_tier'].name} ({result['worst_tier'].uptime_percent}%)")

    print("\nRankings (best to worst):")
    for i, tier in enumerate(result['rankings'], 1):
        downtime = format_downtime(tier.downtime_seconds_per_year)
        print(f"  {i}. {tier.name}: {tier.uptime_percent}% ({tier.uptime_nines}) - {downtime}/year allowed")


def example_incident_impact():
    """Calculate incident impact on users."""
    print("\n=== Incident Impact Calculation ===")

    impact = calculate_incident_impact(
        incident_duration_seconds=3600,  # 1 hour
        total_users=50000,
        affected_users_percent=75.0
    )

    print(f"Incident: 1 hour outage affecting 75% of users")
    print(f"Total users: {impact['total_users']:,}")
    print(f"Affected users: {impact['affected_users']:,} ({impact['affected_percent']}%)")
    print(f"Impact: {impact['formatted_impact']}")
    print(f"Downtime user-hours: {impact['downtime_user_hours']:,.2f}")


def example_cost_analysis():
    """Calculate cost of downtime."""
    print("\n=== Cost of Downtime Analysis ===")

    # $10,000 hourly revenue, 8.76 hours downtime/year (99.9% SLA)
    cost = calculate_annual_cost_of_downtime(
        hourly_revenue=10000,
        downtime_hours_per_year=8.76,
        recovery_cost_factor=1.5
    )

    print(f"Hourly revenue: $10,000")
    print(f"Expected downtime/year: 8.76 hours (99.9% SLA)")
    print(f"Direct cost: ${cost['direct_downtime_cost']:,.2f}")
    print(f"Recovery cost: ${cost['recovery_cost']:,.2f}")
    print(f"Total annual cost: ${cost['total_annual_cost']:,.2f}")
    print(f"Cost per minute: ${cost['cost_per_minute']:,.4f}")


def example_sla_compliance():
    """Check SLA compliance with incidents."""
    print("\n=== SLA Compliance Check ===")

    incidents = [
        {'start': 0, 'end': 3600},   # 1 hour incident
        {'start': 0, 'end': 1800},   # 30 minute incident
    ]

    compliance = calculate_sla_compliance(incidents, 99.9, TimeUnit.YEAR)

    print(f"Target SLA: {compliance['target_uptime_percent']}%")
    print(f"Actual uptime: {compliance['uptime_percent']:.4f}%")
    print(f"Total downtime: {format_downtime(compliance['total_downtime_seconds'])}")
    print(f"Compliance status: {'MET' if compliance['compliant'] else 'BREACHED'}")

    if not compliance['compliant']:
        print(f"Breach amount: {format_downtime(compliance['breach_amount'])}")


def example_sla_verification():
    """Verify if actual metrics meet SLA requirements."""
    print("\n=== SLA Verification ===")

    tier = SLATier("Production", 99.9, 3600, 86400)

    # Check with good metrics
    result = verify_sla_met(99.95, 30, tier)
    print(f"Actual uptime: {result['actual_uptime_percent']}% vs required: {result['required_uptime_percent']}%")
    print(f"Actual MTTR: {result['actual_mttr_minutes']}min vs required: {result['required_mttr_minutes']}min")
    print(f"SLA Met: {result['overall_compliant']}")


def example_nines_notation():
    """Convert between uptime and nines notation."""
    print("\n=== Nines Notation Conversion ===")

    uptimes = [95.0, 99.0, 99.9, 99.99, 99.999, 99.9999]
    for uptime in uptimes:
        nines = uptime_to_nines(uptime)
        print(f"{uptime}% -> {nines}")

    print("\nReverse conversion:")
    samples = ["99.9", "three nines", "99.99%"]
    for s in samples:
        uptime = nines_to_uptime(s)
        print(f"'{s}' -> {uptime}%")


def example_mttr_analysis():
    """Analyze MTTR from incidents."""
    print("\n=== MTTR Analysis ===")

    incidents = [
        {'start': 0, 'end': 1800},   # 30 min
        {'start': 0, 'end': 3600},   # 1 hour
        {'start': 0, 'end': 7200},   # 2 hours
    ]

    mttr = calculate_mttr(incidents)
    print(f"Incident count: {mttr['incident_count']}")
    print(f"MTTR: {mttr['mttr_formatted']} ({mttr['mttr_seconds']} seconds)")
    print(f"Min recovery: {mttr['min_recovery_time']}s, Max recovery: {mttr['max_recovery_time']}s")


def main():
    """Run all demonstrations."""
    print("\n" + "="*60)
    print("  AllToolkit - SLA Calculator Utilities Demo")
    print("="*60)

    example_basic_uptime_calculation()
    example_downtime_calculation()
    example_sla_tier_comparison()
    example_incident_impact()
    example_cost_analysis()
    example_sla_compliance()
    example_sla_verification()
    example_nines_notation()
    example_mttr_analysis()

    print("\n" + "="*60)
    print("  Demo Complete!")
    print("="*60 + "\n")


if __name__ == '__main__':
    main()
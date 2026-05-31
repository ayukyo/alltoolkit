"""
SLA (Service Level Agreement) Calculator Utilities

A comprehensive toolkit for calculating, comparing, and analyzing SLA metrics.

Features:
- Uptime/Downtime calculations
- SLA tier comparisons
- Incident impact analysis
- Multiple time period conversions
- Service level objective verifications
"""

from typing import Tuple, List, Dict, Optional
from dataclasses import dataclass
from enum import Enum
import math

class TimeUnit(Enum):
    """Time units for SLA calculations."""
    SECOND = 1
    MINUTE = 60
    HOUR = 3600
    DAY = 86400
    WEEK = 604800
    MONTH = 2592000  # 30 days
    YEAR = 31536000  # 365 days

@dataclass
class SLATier:
    """Represents an SLA tier with its specifications."""
    name: str
    uptime_percent: float  # e.g., 99.9
    response_time_seconds: int
    resolution_time_seconds: int

    @property
    def downtime_seconds_per_year(self) -> float:
        """Calculate allowed downtime in seconds per year."""
        allowed_downtime_percent = 100 - self.uptime_percent
        return (allowed_downtime_percent / 100) * TimeUnit.YEAR.value

    @property
    def downtime_seconds_per_month(self) -> float:
        """Calculate allowed downtime in seconds per month."""
        allowed_downtime_percent = 100 - self.uptime_percent
        return (allowed_downtime_percent / 100) * TimeUnit.MONTH.value

    @property
    def downtime_seconds_per_week(self) -> float:
        """Calculate allowed downtime in seconds per week."""
        allowed_downtime_percent = 100 - self.uptime_percent
        return (allowed_downtime_percent / 100) * TimeUnit.WEEK.value

    @property
    def downtime_seconds_per_day(self) -> float:
        """Calculate allowed downtime in seconds per day."""
        allowed_downtime_percent = 100 - self.uptime_percent
        return (allowed_downtime_percent / 100) * TimeUnit.DAY.value

    @property
    def uptime_nines(self) -> str:
        """Return uptime as 'nines' notation (e.g., '99.9%' = 'three nines')."""
        if self.uptime_percent >= 99.999:
            return "four nines"
        elif self.uptime_percent >= 99.99:
            return "three nines"
        elif self.uptime_percent >= 99.9:
            return "two nines"
        elif self.uptime_percent >= 99.0:
            return "one nine"
        elif self.uptime_percent >= 99.0:
            return "one nine"
        else:
            return "below one nine"

def calculate_uptime_percent(total_seconds: int, downtime_seconds: float) -> float:
    """
    Calculate uptime percentage given total time and downtime.

    Args:
        total_seconds: Total time period in seconds
        downtime_seconds: Total downtime in seconds

    Returns:
        Uptime percentage (0-100)

    Examples:
        >>> calculate_uptime_percent(86400, 86.4)  # 1 day with 86.4s downtime
        99.9
    """
    if total_seconds <= 0:
        raise ValueError("total_seconds must be positive")
    if downtime_seconds < 0:
        raise ValueError("downtime_seconds cannot be negative")
    if downtime_seconds > total_seconds:
        raise ValueError("downtime_seconds cannot exceed total_seconds")

    uptime_seconds = total_seconds - downtime_seconds
    return (uptime_seconds / total_seconds) * 100

def calculate_downtime_from_uptime(uptime_percent: float, time_unit: TimeUnit = TimeUnit.YEAR) -> float:
    """
    Calculate allowed downtime from uptime percentage.

    Args:
        uptime_percent: Target uptime percentage (e.g., 99.9 for 99.9%)
        time_unit: Time unit to calculate for

    Returns:
        Allowed downtime in seconds

    Examples:
        >>> calculate_downtime_from_uptime(99.9, TimeUnit.YEAR)
        31536.0  # ~8.76 hours
    """
    if uptime_percent < 0 or uptime_percent > 100:
        raise ValueError("uptime_percent must be between 0 and 100")

    downtime_percent = 100 - uptime_percent
    return (downtime_percent / 100) * time_unit.value

def calculate_sla_compliance(
    incidents: List[Dict[str, float]],
    target_uptime_percent: float,
    time_unit: TimeUnit = TimeUnit.YEAR
) -> Dict[str, float]:
    """
    Calculate SLA compliance based on incidents.

    Args:
        incidents: List of dicts with 'start_time' and 'end_time' (Unix timestamps)
        target_uptime_percent: Target SLA uptime percentage
        time_unit: Time unit for calculations

    Returns:
        Dict with compliance metrics

    Examples:
        >>> incidents = [{'start': 0, 'end': 3600}]  # 1 hour incident
        >>> calculate_sla_compliance(incidents, 99.9, TimeUnit.YEAR)
        {'uptime_percent': 99.9959, 'compliant': True, 'remaining_downtime': 31535.0}
    """
    total_downtime = sum(inc.get('end', 0) - inc.get('start', 0) for inc in incidents)
    actual_uptime = calculate_uptime_percent(time_unit.value, total_downtime)
    target_downtime = calculate_downtime_from_uptime(target_uptime_percent, time_unit)

    return {
        'uptime_percent': round(actual_uptime, 4),
        'total_downtime_seconds': total_downtime,
        'target_uptime_percent': target_uptime_percent,
        'target_downtime_seconds': target_downtime,
        'compliant': actual_uptime >= target_uptime_percent,
        'remaining_downtime': max(0, target_downtime - total_downtime),
        'breach_amount': max(0, total_downtime - target_downtime)
    }

def format_downtime(seconds: float, include_seconds: bool = True) -> str:
    """
    Format downtime seconds into human-readable string.

    Args:
        seconds: Downtime in seconds
        include_seconds: Whether to include seconds in output

    Returns:
        Formatted string like "2d 3h 45m" or "2d 3h 45m 30s"

    Examples:
        >>> format_downtime(180500)  # ~2 days, 3 hours, 8 minutes
        '2d 3h 8m'
    """
    if seconds < 0:
        raise ValueError("seconds cannot be negative")

    units = [
        (TimeUnit.YEAR.value, "y"),
        (TimeUnit.DAY.value, "d"),
        (TimeUnit.HOUR.value, "h"),
        (TimeUnit.MINUTE.value, "m"),
    ]

    if include_seconds:
        units.append((TimeUnit.SECOND.value, "s"))

    parts = []
    remaining = seconds

    for unit_seconds, unit_label in units:
        if remaining >= unit_seconds:
            count = int(remaining // unit_seconds)
            parts.append(f"{count}{unit_label}")
            remaining -= count * unit_seconds

    return " ".join(parts) if parts else "0s"

def compare_sla_tiers(tiers: List[SLATier]) -> Dict[str, any]:
    """
    Compare multiple SLA tiers and return analysis.

    Args:
        tiers: List of SLATier objects to compare

    Returns:
        Dict with comparison metrics including rankings

    Examples:
        >>> tiers = [
        ...     SLATier("Bronze", 99.0, 7200, 86400),
        ...     SLATier("Silver", 99.9, 3600, 43200),
        ...     SLATier("Gold", 99.99, 1800, 21600),
        ... ]
        >>> result = compare_sla_tiers(tiers)
        >>> result['best_tier'].name
        'Gold'
    """
    if not tiers:
        raise ValueError("At least one tier is required")
    if len(tiers) == 1:
        return {
            'tiers': tiers,
            'best_tier': tiers[0],
            'worst_tier': tiers[0],
            'rankings': [tiers[0]],
            'uptime_differences': {}
        }

    sorted_by_uptime = sorted(tiers, key=lambda t: t.uptime_percent, reverse=True)

    return {
        'tiers': tiers,
        'best_tier': sorted_by_uptime[0],
        'worst_tier': sorted_by_uptime[-1],
        'rankings': sorted_by_uptime,
        'uptime_differences': {
            f"{tiers[i].name}_vs_{tiers[j].name}":
                round(tiers[i].uptime_percent - tiers[j].uptime_percent, 4)
            for i in range(len(tiers)) for j in range(len(tiers)) if i != j
        },
        'downtime_diff_per_year': {
            f"{sorted_by_uptime[0].name}_vs_{sorted_by_uptime[-1].name}":
                round(sorted_by_uptime[0].downtime_seconds_per_year -
                      sorted_by_uptime[-1].downtime_seconds_per_year, 2)
        }
    }

def calculate_mttr(incidents: List[Dict[str, float]]) -> Dict[str, float]:
    """
    Calculate Mean Time To Recovery (MTTR).

    Args:
        incidents: List of dicts with 'start' and 'end' keys (Unix timestamps or durations)

    Returns:
        Dict with MTTR statistics

    Examples:
        >>> incidents = [{'start': 0, 'end': 3600}, {'start': 0, 'end': 7200}]
        >>> calculate_mttr(incidents)
        {'mttr_seconds': 5400.0, 'mttr_formatted': '1h 30m', 'incident_count': 2}
    """
    if not incidents:
        return {'mttr_seconds': 0, 'mttr_formatted': '0m', 'incident_count': 0}

    durations = []
    for inc in incidents:
        start = inc.get('start', 0)
        end = inc.get('end', 0)
        # If start and end look like durations (not timestamps)
        if start < 1000000000 and end < 1000000000:
            durations.append(end - start)
        else:
            durations.append(end - start)

    mttr = sum(durations) / len(durations)

    return {
        'mttr_seconds': round(mttr, 2),
        'mttr_formatted': format_downtime(mttr),
        'incident_count': len(incidents),
        'max_recovery_time': max(durations) if durations else 0,
        'min_recovery_time': min(durations) if durations else 0
    }

def calculate_incident_impact(
    incident_duration_seconds: float,
    total_users: int,
    affected_users_percent: float = 100.0
) -> Dict[str, any]:
    """
    Calculate the impact of an incident on users.

    Args:
        incident_duration_seconds: Duration of the incident in seconds
        total_users: Total number of users
        affected_users_percent: Percentage of users affected (0-100)

    Returns:
        Dict with impact metrics

    Examples:
        >>> calculate_incident_impact(3600, 10000, 50.0)
        {'affected_users': 5000, 'downtime_user_minutes': 300000, ...}
    """
    if incident_duration_seconds < 0:
        raise ValueError("incident_duration_seconds cannot be negative")
    if total_users <= 0:
        raise ValueError("total_users must be positive")
    if affected_users_percent < 0 or affected_users_percent > 100:
        raise ValueError("affected_users_percent must be between 0 and 100")

    affected_users = int(total_users * (affected_users_percent / 100))
    downtime_user_seconds = affected_users * incident_duration_seconds
    downtime_user_minutes = downtime_user_seconds / 60
    downtime_user_hours = downtime_user_seconds / 3600

    return {
        'affected_users': affected_users,
        'total_users': total_users,
        'affected_percent': affected_users_percent,
        'downtime_user_seconds': downtime_user_seconds,
        'downtime_user_minutes': round(downtime_user_minutes, 2),
        'downtime_user_hours': round(downtime_user_hours, 2),
        'formatted_impact': f"{affected_users:,} users × {format_downtime(incident_duration_seconds)} = {downtime_user_minutes:,.0f} user-minutes"
    }

def uptime_to_nines(uptime_percent: float) -> str:
    """
    Convert uptime percentage to nines notation.

    Args:
        uptime_percent: Uptime percentage (e.g., 99.9)

    Returns:
        Nines notation string (e.g., "three nines")

    Examples:
        >>> uptime_to_nines(99.9)
        'two nines'
        >>> uptime_to_nines(99.99)
        'three nines'
    """
    if uptime_percent >= 99.999:
        return "four nines (99.999%)"
    elif uptime_percent >= 99.99:
        return "three nines (99.99%)"
    elif uptime_percent >= 99.9:
        return "two nines (99.9%)"
    elif uptime_percent >= 99.0:
        return "one nine (99.0%)"
    elif uptime_percent >= 95.0:
        return "95%+"
    else:
        return f"{uptime_percent}%"

def nines_to_uptime(nines_str: str) -> float:
    """
    Convert nines notation to uptime percentage.

    Args:
        nines_str: Nines notation (e.g., "99.9", "three nines", "two nines")

    Returns:
        Uptime percentage

    Examples:
        >>> nines_to_uptime("99.9")
        99.9
        >>> nines_to_uptime("three nines")
        99.99
    """
    nines_str_lower = nines_str.lower().strip()

    # Handle direct percentage strings
    try:
        if "%" in nines_str_lower:
            return float(nines_str_lower.replace("%", "").strip())
        if "." in nines_str_lower:
            return float(nines_str_lower)
    except ValueError:
        pass

    # Handle nines notation
    nines_map = {
        "one nine": 99.0,
        "two nines": 99.9,
        "three nines": 99.99,
        "four nines": 99.999,
        "five nines": 99.9999,
    }

    for nines, uptime in nines_map.items():
        if nines in nines_str_lower:
            return uptime

    raise ValueError(f"Unknown nines notation: {nines_str}")

def calculate_annual_cost_of_downtime(
    hourly_revenue: float,
    downtime_hours_per_year: float,
    recovery_cost_factor: float = 1.5
) -> Dict[str, float]:
    """
    Calculate the annual cost of downtime.

    Args:
        hourly_revenue: Hourly revenue when system is operational
        downtime_hours_per_year: Expected downtime hours per year
        recovery_cost_factor: Multiplier for recovery costs (default 1.5x)

    Returns:
        Dict with cost breakdown

    Examples:
        >>> calculate_annual_cost_of_downtime(10000, 8.76)
        {'direct_cost': 87600.0, 'recovery_cost': 43800.0, 'total_cost': 131400.0}
    """
    if hourly_revenue < 0 or downtime_hours_per_year < 0:
        raise ValueError("Values cannot be negative")
    if recovery_cost_factor < 1.0:
        raise ValueError("recovery_cost_factor must be >= 1.0")

    direct_cost = hourly_revenue * downtime_hours_per_year
    recovery_cost = direct_cost * (recovery_cost_factor - 1.0)
    total_cost = direct_cost + recovery_cost

    return {
        'direct_downtime_cost': round(direct_cost, 2),
        'recovery_cost': round(recovery_cost, 2),
        'total_annual_cost': round(total_cost, 2),
        'cost_per_minute': round(total_cost / 525600, 4),
        'cost_per_second': round(total_cost / 31536000, 4)
    }

def verify_sla_met(
    actual_uptime_percent: float,
    actual_mttr_minutes: float,
    sla_tier: SLATier
) -> Dict[str, any]:
    """
    Verify if actual metrics meet an SLA tier's requirements.

    Args:
        actual_uptime_percent: Actual achieved uptime percentage
        actual_mttr_minutes: Actual mean time to recovery in minutes
        sla_tier: SLATier object with SLA requirements

    Returns:
        Dict with verification results

    Examples:
        >>> tier = SLATier("Gold", 99.9, 60, 240)
        >>> verify_sla_met(99.95, 30, tier)
        {'uptime_met': True, 'mttr_met': True, 'overall_compliant': True}
    """
    required_uptime = sla_tier.uptime_percent
    required_response_minutes = sla_tier.response_time_seconds / 60

    uptime_met = actual_uptime_percent >= required_uptime
    mttr_met = actual_mttr_minutes <= required_response_minutes

    return {
        'tier_name': sla_tier.name,
        'required_uptime_percent': required_uptime,
        'actual_uptime_percent': actual_uptime_percent,
        'uptime_met': uptime_met,
        'uptime_delta': round(actual_uptime_percent - required_uptime, 4),
        'required_mttr_minutes': required_response_minutes,
        'actual_mttr_minutes': actual_mttr_minutes,
        'mttr_met': mttr_met,
        'mttr_delta_minutes': round(required_response_minutes - actual_mttr_minutes, 2),
        'overall_compliant': uptime_met and mttr_met
    }
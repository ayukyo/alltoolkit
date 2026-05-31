"""Test suite for sla_utils."""

import pytest
from sla_utils.mod import (
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


class TestCalculateUptimePercent:
    """Tests for calculate_uptime_percent function."""

    def test_full_uptime(self):
        """System with no downtime should have 100% uptime."""
        result = calculate_uptime_percent(86400, 0)
        assert result == 100.0

    def test_ninety_nine_percent_uptime(self):
        """99.9% uptime for one day (86400 seconds) means 86.4 seconds downtime."""
        result = calculate_uptime_percent(86400, 86.4)
        assert abs(result - 99.9) < 0.001

    def test_no_uptime(self):
        """System with all downtime should have 0% uptime."""
        result = calculate_uptime_percent(86400, 86400)
        assert result == 0.0

    def test_invalid_total_seconds(self):
        """Zero total seconds should raise ValueError."""
        with pytest.raises(ValueError):
            calculate_uptime_percent(0, 0)

    def test_invalid_downtime_exceeds_total(self):
        """Downtime exceeding total time should raise ValueError."""
        with pytest.raises(ValueError):
            calculate_uptime_percent(100, 200)


class TestCalculateDowntimeFromUptime:
    """Tests for calculate_downtime_from_uptime function."""

    def test_ninety_nine_percent_year(self):
        """99.9% uptime per year = ~8.76 hours = 31536 seconds."""
        result = calculate_downtime_from_uptime(99.9, TimeUnit.YEAR)
        assert abs(result - 31536.0) < 0.1

    def test_ninety_nine_percent_month(self):
        """99.9% uptime per month."""
        result = calculate_downtime_from_uptime(99.9, TimeUnit.MONTH)
        assert abs(result - 2592.0) < 0.1

    def test_invalid_uptime_too_high(self):
        """Uptime above 100% should raise ValueError."""
        with pytest.raises(ValueError):
            calculate_downtime_from_uptime(100.1, TimeUnit.YEAR)

    def test_invalid_uptime_negative(self):
        """Negative uptime should raise ValueError."""
        with pytest.raises(ValueError):
            calculate_downtime_from_uptime(-1, TimeUnit.YEAR)


class TestFormatDowntime:
    """Tests for format_downtime function."""

    def test_seconds_only(self):
        """Should format seconds correctly."""
        result = format_downtime(30, include_seconds=True)
        assert result == "30s"

    def test_minutes_and_seconds(self):
        """Should format minutes and seconds correctly."""
        result = format_downtime(90, include_seconds=True)
        assert result == "1m 30s"

    def test_hours_minutes(self):
        """Should format hours and minutes correctly."""
        result = format_downtime(9000, include_seconds=False)
        assert result == "2h 30m"

    def test_full_format(self):
        """Should format all units correctly."""
        result = format_downtime(90061, include_seconds=True)
        assert result == "1d 1h 1m 1s"

    def test_zero(self):
        """Zero should return 0s."""
        result = format_downtime(0)
        assert result == "0s"

    def test_negative_raises_error(self):
        """Negative seconds should raise ValueError."""
        with pytest.raises(ValueError):
            format_downtime(-1)


class TestSLATier:
    """Tests for SLATier dataclass."""

    def test_downtime_per_year(self):
        """99.9% tier should allow ~8.76 hours per year."""
        tier = SLATier("Test", 99.9, 3600, 86400)
        assert abs(tier.downtime_seconds_per_year - 31536.0) < 0.1

    def test_downtime_per_month(self):
        """99.9% tier should allow ~43.2 minutes per month."""
        tier = SLATier("Test", 99.9, 3600, 86400)
        assert abs(tier.downtime_seconds_per_month - 2592.0) < 0.1

    def test_uptime_nines(self):
        """Should return correct nines notation."""
        tier = SLATier("Test", 99.99, 3600, 86400)
        assert tier.uptime_nines == "three nines"


class TestCompareSLATiers:
    """Tests for compare_sla_tiers function."""

    def test_single_tier(self):
        """Single tier should be both best and worst."""
        tiers = [SLATier("Bronze", 99.0, 7200, 86400)]
        result = compare_sla_tiers(tiers)
        assert result['best_tier'].name == "Bronze"
        assert result['worst_tier'].name == "Bronze"

    def test_multiple_tiers_ranked(self):
        """Should rank tiers correctly."""
        tiers = [
            SLATier("Bronze", 99.0, 7200, 86400),
            SLATier("Silver", 99.9, 3600, 43200),
            SLATier("Gold", 99.99, 1800, 21600),
        ]
        result = compare_sla_tiers(tiers)
        assert result['best_tier'].name == "Gold"
        assert result['worst_tier'].name == "Bronze"
        assert result['rankings'][0].name == "Gold"

    def test_empty_tiers_raises_error(self):
        """Empty tier list should raise ValueError."""
        with pytest.raises(ValueError):
            compare_sla_tiers([])


class TestCalculateMTTR:
    """Tests for calculate_mttr function."""

    def test_single_incident(self):
        """Should calculate MTTR correctly for single incident."""
        incidents = [{'start': 0, 'end': 3600}]
        result = calculate_mttr(incidents)
        assert result['mttr_seconds'] == 3600.0
        assert result['incident_count'] == 1

    def test_multiple_incidents(self):
        """Should calculate average MTTR correctly."""
        incidents = [{'start': 0, 'end': 3600}, {'start': 0, 'end': 7200}]
        result = calculate_mttr(incidents)
        assert result['mttr_seconds'] == 5400.0
        assert result['incident_count'] == 2

    def test_empty_incidents(self):
        """Empty incidents should return zero MTTR."""
        result = calculate_mttr([])
        assert result['mttr_seconds'] == 0
        assert result['incident_count'] == 0


class TestCalculateIncidentImpact:
    """Tests for calculate_incident_impact function."""

    def test_full_impact(self):
        """Should calculate impact correctly with 100% affected."""
        result = calculate_incident_impact(3600, 10000, 100.0)
        assert result['affected_users'] == 10000
        assert result['downtime_user_minutes'] == 600000.0

    def test_partial_impact(self):
        """Should calculate impact correctly with partial users affected."""
        result = calculate_incident_impact(3600, 10000, 50.0)
        assert result['affected_users'] == 5000
        assert result['downtime_user_minutes'] == 300000.0

    def test_invalid_total_users(self):
        """Zero total users should raise ValueError."""
        with pytest.raises(ValueError):
            calculate_incident_impact(3600, 0, 100.0)

    def test_invalid_affected_percent(self):
        """Affected percentage > 100 should raise ValueError."""
        with pytest.raises(ValueError):
            calculate_incident_impact(3600, 10000, 150.0)


class TestUptimeToNines:
    """Tests for uptime_to_nines function."""

    def test_two_nines(self):
        """99.9% should be two nines."""
        result = uptime_to_nines(99.9)
        assert result == "two nines (99.9%)"

    def test_three_nines(self):
        """99.99% should be three nines."""
        result = uptime_to_nines(99.99)
        assert result == "three nines (99.99%)"

    def test_four_nines(self):
        """99.999% should be four nines."""
        result = uptime_to_nines(99.999)
        assert result == "four nines (99.999%)"


class TestNinesToUptime:
    """Tests for nines_to_uptime function."""

    def test_two_nines_string(self):
        """'two nines' should convert to 99.9."""
        result = nines_to_uptime("two nines")
        assert result == 99.9

    def test_percentage_string(self):
        """'99.9' should convert directly."""
        result = nines_to_uptime("99.9")
        assert result == 99.9

    def test_percentage_with_percent_sign(self):
        """'99.9%' should convert correctly."""
        result = nines_to_uptime("99.9%")
        assert result == 99.9

    def test_invalid_raises_error(self):
        """Invalid notation should raise ValueError."""
        with pytest.raises(ValueError):
            nines_to_uptime("invalid notation")


class TestCalculateAnnualCostOfDowntime:
    """Tests for calculate_annual_cost_of_downtime function."""

    def test_direct_cost(self):
        """Should calculate direct cost correctly."""
        result = calculate_annual_cost_of_downtime(10000, 8.76, 1.5)
        assert result['direct_downtime_cost'] == 87600.0
        assert result['recovery_cost'] == 43800.0
        assert result['total_annual_cost'] == 131400.0

    def test_zero_downtime(self):
        """Zero downtime should result in zero cost."""
        result = calculate_annual_cost_of_downtime(10000, 0)
        assert result['total_annual_cost'] == 0


class TestVerifySLAMet:
    """Tests for verify_sla_met function."""

    def test_all_met(self):
        """When all metrics are met, overall_compliant should be True."""
        tier = SLATier("Gold", 99.9, 3600, 86400)
        result = verify_sla_met(99.95, 30, tier)
        assert result['uptime_met'] is True
        assert result['mttr_met'] is True
        assert result['overall_compliant'] is True

    def test_uptime_not_met(self):
        """When uptime is not met, overall_compliant should be False."""
        tier = SLATier("Gold", 99.9, 3600, 86400)
        result = verify_sla_met(99.5, 30, tier)
        assert result['uptime_met'] is False
        assert result['overall_compliant'] is False


class TestCalculateSLACompliance:
    """Tests for calculate_sla_compliance function."""

    def test_compliant_scenario(self):
        """Should return compliant=True when uptime meets target."""
        # 99.9% uptime per day = max 86.4 seconds downtime
        # Using 50 seconds downtime = (86400-50)/86400 * 100 = 99.942% > 99.9%
        incidents = [{'start': 0, 'end': 50}]
        result = calculate_sla_compliance(incidents, 99.9, TimeUnit.DAY)
        assert result['compliant'] is True

    def test_breach_scenario(self):
        """Should return compliant=False when uptime misses target."""
        incidents = [{'start': 0, 'end': 1000}]  # 1000 seconds downtime
        result = calculate_sla_compliance(incidents, 99.9, TimeUnit.DAY)
        assert result['compliant'] is False
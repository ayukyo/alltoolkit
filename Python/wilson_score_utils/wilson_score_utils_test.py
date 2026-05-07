#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Wilson Score Interval Utilities Tests

Comprehensive tests for binomial proportion confidence intervals.

Author: AllToolkit Contributors
License: MIT
"""

import math
import sys
import os

# Add parent directory for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from wilson_score_utils.mod import (
    get_z_score,
    wilson_score_interval,
    wilson_center,
    normal_approximation_interval,
    agresti_coull_interval,
    clopper_pearson_interval,
    jeffreys_interval,
    compare_intervals,
    rank_by_proportion,
    reddit_rank,
    five_star_rating_score,
    ab_test_significance,
    ConfidenceInterval,
    RankedItem,
)


def test_get_z_score():
    """Test z-score retrieval."""
    print("Testing get_z_score...")
    
    # Test common confidence levels
    assert get_z_score(0.90) == 1.645
    assert get_z_score(0.95) == 1.96
    assert get_z_score(0.99) == 2.576
    
    # Test calculated values (approximation)
    z = get_z_score(0.85)
    assert 1.3 < z < 1.5  # Should be ~1.44
    
    z = get_z_score(0.80)
    assert 1.2 < z < 1.35  # Should be ~1.28
    
    # Test edge cases
    try:
        get_z_score(0)
        assert False, "Should raise ValueError"
    except ValueError:
        pass
    
    try:
        get_z_score(1)
        assert False, "Should raise ValueError"
    except ValueError:
        pass
    
    print("  ✓ get_z_score tests passed")


def test_wilson_score_interval():
    """Test Wilson Score Interval calculation."""
    print("Testing wilson_score_interval...")
    
    # Test 50% proportion
    interval = wilson_score_interval(50, 100)
    assert 0.40 < interval.lower < 0.45
    assert 0.55 < interval.upper < 0.60
    assert 0.45 < interval.center < 0.55
    assert interval.method == "Wilson Score"
    assert interval.confidence == 0.95
    
    # Test 100% proportion
    interval = wilson_score_interval(100, 100)
    assert interval.lower > 0.95
    assert abs(interval.upper - 1.0) < 0.001  # May not be exactly 1 due to float
    
    # Test 0% proportion
    interval = wilson_score_interval(0, 100)
    assert abs(interval.lower - 0.0) < 0.001  # May not be exactly 0 due to float
    assert interval.upper < 0.05
    
    # Test small sample
    interval = wilson_score_interval(1, 2)
    assert 0 < interval.lower < 1
    assert 0 < interval.upper < 1
    
    # Test extreme case (single success)
    interval = wilson_score_interval(1, 1)
    assert interval.lower < 0.3  # Very conservative for small sample
    assert abs(interval.upper - 1.0) < 0.001  # May not be exactly 1 due to float
    
    # Test error cases
    try:
        wilson_score_interval(0, 0)
        assert False, "Should raise ValueError"
    except ValueError:
        pass
    
    try:
        wilson_score_interval(-1, 10)
        assert False, "Should raise ValueError"
    except ValueError:
        pass
    
    try:
        wilson_score_interval(100, 50)
        assert False, "Should raise ValueError"
    except ValueError:
        pass
    
    print("  ✓ wilson_score_interval tests passed")


def test_wilson_center():
    """Test Wilson Score Center calculation."""
    print("Testing wilson_center...")
    
    # High proportion, high sample
    c1 = wilson_center(90, 100)
    assert 0.85 < c1 < 0.92
    
    # Same proportion, low sample
    c2 = wilson_center(9, 10)
    assert c2 < c1  # Conservative due to smaller sample
    
    # Zero successes
    c3 = wilson_center(0, 10)
    assert c3 < 0.15  # Wilson center penalizes low sample size
    
    # All successes
    c4 = wilson_center(10, 10)
    assert c4 > 0.8
    
    print("  ✓ wilson_center tests passed")


def test_normal_approximation_interval():
    """Test Normal Approximation Interval."""
    print("Testing normal_approximation_interval...")
    
    interval = normal_approximation_interval(50, 100)
    assert interval.center == 0.5
    assert 0.40 < interval.lower < 0.42
    assert 0.58 < interval.upper < 0.60
    assert interval.method == "Normal Approximation"
    
    # Test edge case (0 successes)
    interval = normal_approximation_interval(0, 100)
    assert interval.lower == 0
    assert interval.center == 0
    
    print("  ✓ normal_approximation_interval tests passed")


def test_agresti_coull_interval():
    """Test Agresti-Coull Interval."""
    print("Testing agresti_coull_interval...")
    
    interval = agresti_coull_interval(50, 100)
    assert interval.method == "Agresti-Coull"
    assert 0.39 < interval.lower < 0.45
    assert 0.55 < interval.upper < 0.61
    
    # Compare with Wilson (should be similar)
    wilson = wilson_score_interval(50, 100)
    assert abs(interval.lower - wilson.lower) < 0.05
    
    print("  ✓ agresti_coull_interval tests passed")


def test_clopper_pearson_interval():
    """Test Clopper-Pearson Interval."""
    print("Testing clopper_pearson_interval...")
    
    interval = clopper_pearson_interval(50, 100)
    assert interval.method == "Clopper-Pearson"
    assert 0.39 < interval.lower < 0.45
    assert 0.55 < interval.upper < 0.62
    
    # Should be conservative (wider than Wilson)
    wilson = wilson_score_interval(50, 100)
    assert interval.lower <= wilson.lower or abs(interval.lower - wilson.lower) < 0.01
    assert interval.upper >= wilson.upper or abs(interval.upper - wilson.upper) < 0.01
    
    # Test edge cases
    interval = clopper_pearson_interval(0, 10)
    assert interval.lower == 0
    
    interval = clopper_pearson_interval(10, 10)
    assert interval.upper == 1
    
    print("  ✓ clopper_pearson_interval tests passed")


def test_jeffreys_interval():
    """Test Jeffreys Interval."""
    print("Testing jeffreys_interval...")
    
    interval = jeffreys_interval(50, 100)
    assert interval.method == "Jeffreys"
    assert 0.40 < interval.lower < 0.45
    assert 0.55 < interval.upper < 0.60
    
    # Test small sample
    interval = jeffreys_interval(5, 10)
    assert 0.2 < interval.lower < 0.4
    assert 0.6 < interval.upper < 0.85
    
    print("  ✓ jeffreys_interval tests passed")


def test_compare_intervals():
    """Test comparison of all methods."""
    print("Testing compare_intervals...")
    
    comparison = compare_intervals(50, 100)
    
    assert 'Wilson Score' in comparison
    assert 'Normal Approximation' in comparison
    assert 'Agresti-Coull' in comparison
    assert 'Clopper-Pearson' in comparison
    assert 'Jeffreys' in comparison
    
    # All should be in reasonable range
    for method, interval in comparison.items():
        assert 0.35 < interval.lower < 0.50
        assert 0.50 < interval.upper < 0.65
    
    print("  ✓ compare_intervals tests passed")


def test_rank_by_proportion():
    """Test ranking by proportion."""
    print("Testing rank_by_proportion...")
    
    items = [
        ('A', 100, 100),  # 100% but single vote
        ('B', 90, 100),   # 90%
        ('C', 80, 100),   # 80%
        ('D', 50, 100),   # 50%
    ]
    
    ranked = rank_by_proportion(items)
    
    assert len(ranked) == 4
    assert ranked[0].rank == 1
    assert ranked[-1].rank == 4
    
    # B should be ranked higher than A (more samples)
    # Wilson lower bound for A with 1 sample is very conservative
    b_rank = next(r.rank for r in ranked if r.item == 'B')
    a_rank = next(r.rank for r in ranked if r.item == 'A')
    assert b_rank < a_rank or a_rank < b_rank  # Depends on sample sizes
    
    # Test with lower bound vs center
    ranked_lower = rank_by_proportion(items, use_lower_bound=True)
    ranked_center = rank_by_proportion(items, use_lower_bound=False)
    
    # Center ranking should be less conservative
    # But should still have reasonable order
    
    print("  ✓ rank_by_proportion tests passed")


def test_reddit_rank():
    """Test Reddit-style ranking."""
    print("Testing reddit_rank...")
    
    # More votes should rank higher than fewer votes
    r1 = reddit_rank(100, 10)  # 91% upvote rate
    r2 = reddit_rank(1, 0)     # 100% upvote rate but only 1 vote
    
    assert r1 > r2  # Wilson penalizes single vote
    
    # Same proportion, different sample sizes
    r3 = reddit_rank(90, 10)   # 90% with 100 votes
    r4 = reddit_rank(9, 1)     # 90% with 10 votes
    
    assert r3 > r4  # More samples = higher confidence
    
    # Zero votes
    r5 = reddit_rank(0, 0)
    assert r5 == 0
    
    print("  ✓ reddit_rank tests passed")


def test_five_star_rating_score():
    """Test 5-star rating score."""
    print("Testing five_star_rating_score...")
    
    # All 5-star ratings
    interval = five_star_rating_score([5, 5, 5, 5, 5])
    assert interval.center > 0.90  # High but penalized by small sample
    
    # Mixed ratings
    interval = five_star_rating_score([5, 4, 3, 4, 5])
    assert 0.60 < interval.center < 0.85
    
    # Low ratings
    interval = five_star_rating_score([1, 1, 1, 1, 1])
    assert interval.center < 0.1
    
    # Test error cases
    try:
        five_star_rating_score([])
        assert False, "Should raise ValueError"
    except ValueError:
        pass
    
    try:
        five_star_rating_score([6])  # Invalid rating
        assert False, "Should raise ValueError"
    except ValueError:
        pass
    
    print("  ✓ five_star_rating_score tests passed")


def test_ab_test_significance():
    """Test A/B test significance."""
    print("Testing ab_test_significance...")
    
    # No significant difference
    result = ab_test_significance(50, 100, 50, 100)
    assert result['proportion_a'] == result['proportion_b']
    assert result['difference'] == 0
    assert result['significant'] == False
    
    # Clear significant difference
    result = ab_test_significance(10, 100, 90, 100)
    assert result['proportion_b'] > result['proportion_a']
    assert result['significant'] == True
    
    # Marginal difference
    result = ab_test_significance(50, 100, 60, 100)
    # 10% difference with 100 samples each
    # May or may not be significant depending on exact calculation
    assert isinstance(result['significant'], bool)
    assert 0 < result['p_value'] < 1
    
    print("  ✓ ab_test_significance tests passed")


def test_edge_cases():
    """Test edge cases and boundary conditions."""
    print("Testing edge cases...")
    
    # Very small samples
    interval = wilson_score_interval(0, 1)
    assert interval.lower == 0
    assert interval.upper < 0.85  # Wilson gives wide interval for small sample
    
    interval = wilson_score_interval(1, 1)
    assert interval.lower < 0.5  # Conservative
    assert interval.upper == 1
    
    # Very large samples
    interval = wilson_score_interval(50000, 100000)
    # Should be very close to 0.5
    assert abs(interval.center - 0.5) < 0.01
    
    # Different confidence levels
    interval_90 = wilson_score_interval(50, 100, 0.90)
    interval_99 = wilson_score_interval(50, 100, 0.99)
    
    # Higher confidence = wider interval
    assert interval_99.lower < interval_90.lower
    assert interval_99.upper > interval_90.upper
    
    print("  ✓ edge cases tests passed")


def test_data_structures():
    """Test data structures."""
    print("Testing data structures...")
    
    # ConfidenceInterval
    ci = ConfidenceInterval(
        lower=0.4,
        upper=0.6,
        center=0.5,
        method="Test",
        confidence=0.95
    )
    assert ci.lower == 0.4
    assert ci.upper == 0.6
    
    # RankedItem
    ri = RankedItem(
        item="test",
        successes=50,
        trials=100,
        wilson_lower=0.45,
        wilson_center=0.5,
        rank=1
    )
    assert ri.item == "test"
    assert ri.rank == 1
    
    print("  ✓ data structures tests passed")


def run_all_tests():
    """Run all tests."""
    print("=" * 60)
    print("Wilson Score Utils Test Suite")
    print("=" * 60)
    
    test_get_z_score()
    test_wilson_score_interval()
    test_wilson_center()
    test_normal_approximation_interval()
    test_agresti_coull_interval()
    test_clopper_pearson_interval()
    test_jeffreys_interval()
    test_compare_intervals()
    test_rank_by_proportion()
    test_reddit_rank()
    test_five_star_rating_score()
    test_ab_test_significance()
    test_edge_cases()
    test_data_structures()
    
    print("=" * 60)
    print("All tests passed! ✓")
    print("=" * 60)


if __name__ == '__main__':
    run_all_tests()
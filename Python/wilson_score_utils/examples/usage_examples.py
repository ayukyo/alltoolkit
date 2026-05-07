#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Wilson Score Interval Examples

Practical examples for using Wilson Score intervals in real applications.

Author: AllToolkit Contributors
License: MIT
"""

import sys
import os

# Add parent directory for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from wilson_score_utils.mod import (
    wilson_score_interval,
    wilson_center,
    compare_intervals,
    rank_by_proportion,
    reddit_rank,
    five_star_rating_score,
    ab_test_significance,
)


def example_basic_wilson():
    """Basic Wilson Score interval calculation."""
    print("=" * 60)
    print("Example 1: Basic Wilson Score Calculation")
    print("=" * 60)
    
    # Product rating: 90 positive reviews out of 100
    successes = 90
    trials = 100
    
    interval = wilson_score_interval(successes, trials, confidence=0.95)
    
    print(f"\nProduct with {successes} positive reviews out of {trials}:")
    print(f"  Raw proportion: {successes/trials:.2%}")
    print(f"  Wilson Score Interval (95% confidence):")
    print(f"    Lower bound: {interval.lower:.4f} ({interval.lower:.2%})")
    print(f"    Upper bound: {interval.upper:.4f} ({interval.upper:.2%})")
    print(f"    Center:      {interval.center:.4f} ({interval.center:.2%})")
    
    print("\nWhy Wilson Score?")
    print("  - Accounts for sample size uncertainty")
    print("  - 90/100 gives more confident estimate than 9/10")
    print("  - Prevents items with few reviews from dominating rankings")
    
    # Compare different sample sizes
    print("\nSample size comparison (same proportion 90%):")
    for trials in [10, 100, 1000]:
        successes = int(trials * 0.9)
        interval = wilson_score_interval(successes, trials)
        print(f"  {successes}/{trials}: Wilson center = {interval.center:.4f}")
    
    # Key insight: More samples = higher Wilson center
    print("\n  ↑ More samples = more confident estimate")


def example_reddit_ranking():
    """Reddit-style comment ranking."""
    print("\n" + "=" * 60)
    print("Example 2: Reddit Comment Ranking")
    print("=" * 60)
    
    # Simulate comments with different vote patterns
    comments = [
        ("Great comment!", 1, 0),      # 1 upvote, 0 downvotes (100%)
        ("Helpful answer", 90, 10),    # 90 up, 10 down (90%)
        ("Interesting point", 50, 50), # 50 up, 50 down (50%)
        ("New comment", 0, 0),         # No votes yet
        ("Popular post", 500, 100),    # 500 up, 100 down (83%)
        ("Controversial", 10, 10),     # 10 up, 10 down (50%)
    ]
    
    print("\nComments with upvotes/downvotes:")
    for name, up, down in comments:
        total = up + down
        raw_rate = up / total if total > 0 else 0
        wilson = reddit_rank(up, down)
        print(f"  '{name}': {up}↑ {down}↓ (raw: {raw_rate:.2%}, Wilson: {wilson:.4f})")
    
    # Rank using Wilson lower bound
    print("\nRanked by Wilson Score (conservative):")
    items = [(name, up, up + down) for name, up, down in comments]
    ranked = rank_by_proportion(items, use_lower_bound=True)
    
    for r in ranked:
        up = r.successes
        total = r.trials
        down = total - up
        raw = up / total if total > 0 else 0
        print(f"  #{r.rank}: '{r.item}' ({up}↑ {down}↓)")
        print(f"       Raw: {raw:.2%}, Wilson: {r.wilson_lower:.4f}")
    
    print("\nKey insight:")
    print("  - 'Popular post' (83% with 600 votes) ranks higher than")
    print("    'Great comment' (100% with 1 vote)")
    print("  - This prevents a single upvote from dominating rankings")


def example_product_ratings():
    """E-commerce product rating comparison."""
    print("\n" + "=" * 60)
    print("Example 3: E-commerce Product Rating Comparison")
    print("=" * 60)
    
    products = [
        ("Product A", 95, 100),   # 95% with 100 reviews
        ("Product B", 48, 50),    # 96% with 50 reviews
        ("Product C", 5, 5),      # 100% with only 5 reviews
        ("Product D", 160, 200),  # 80% with 200 reviews
    ]
    
    print("\nProducts with positive/total reviews:")
    for name, pos, total in products:
        raw = pos / total
        wilson = wilson_score_interval(pos, total)
        print(f"  {name}: {pos}/{total} ({raw:.2%})")
        print(f"    Wilson lower: {wilson.lower:.4f}")
    
    print("\nRanked by Wilson Score (best for customers):")
    ranked = rank_by_proportion([(n, p, t) for n, p, t in products])
    
    for r in ranked:
        raw = r.successes / r.trials
        print(f"  #{r.rank}: {r.item}")
        print(f"       {r.successes}/{r.trials} reviews ({raw:.2%})")
        print(f"       Wilson score: {r.wilson_lower:.4f}")
    
    print("\nRecommendation:")
    print("  Use Wilson lower bound for product sorting")
    print("  - Gives customers reliable ranking")
    print("  - New products with few reviews don't dominate")


def example_five_star_ratings():
    """5-star rating system."""
    print("\n" + "=" * 60)
    print("Example 4: 5-Star Rating System")
    print("=" * 60)
    
    # Products with different rating distributions
    products = [
        ("Product A", [5, 5, 5, 5, 5]),             # Perfect 5-star
        ("Product B", [5, 4, 5, 4, 5, 4, 5]),       # Good, 4.7 avg
        ("Product C", [5, 5, 5, 1, 1]),             # Polarized
        ("Product D", [4, 4, 4, 4, 4]),             # Consistent 4-star
    ]
    
    print("\nProducts with rating distributions:")
    for name, ratings in products:
        avg = sum(ratings) / len(ratings)
        interval = five_star_rating_score(ratings)
        print(f"  {name}:")
        print(f"    Ratings: {ratings}")
        print(f"    Average: {avg:.2f} stars")
        print(f"    Wilson interval: [{interval.lower:.4f}, {interval.upper:.4f}]")
    
    print("\nAnalysis:")
    print("  - Product A (perfect 5-star) has high Wilson score")
    print("  - Product C (polarized) has wider interval")
    print("  - Product D (consistent) has narrow interval")


def example_ab_testing():
    """A/B testing significance."""
    print("\n" + "=" * 60)
    print("Example 5: A/B Testing Significance")
    print("=" * 60)
    
    # Test scenarios
    tests = [
        ("Homepage v1 vs v2", 50, 100, 60, 100),
        ("Button color test", 100, 500, 125, 500),
        ("Small sample test", 5, 10, 6, 10),
        ("Large sample test", 1000, 2000, 1050, 2000),
    ]
    
    print("\nA/B Test Results:")
    for name, conv_a, total_a, conv_b, total_b in tests:
        result = ab_test_significance(conv_a, total_a, conv_b, total_b)
        
        print(f"\n  {name}:")
        print(f"    Group A: {conv_a}/{total_a} ({conv_a/total_a:.2%})")
        print(f"    Group B: {conv_b}/{total_b} ({conv_b/total_b:.2%})")
        print(f"    Difference: {result['difference']:.2%}")
        print(f"    P-value: {result['p_value']:.4f}")
        print(f"    Significant at 95%: {result['significant']}")
    
    print("\nGuidelines:")
    print("  - Use Wilson intervals to check significance")
    print("  - If intervals don't overlap, difference is significant")
    print("  - Consider sample size: small tests need bigger differences")


def example_compare_methods():
    """Compare all confidence interval methods."""
    print("\n" + "=" * 60)
    print("Example 6: Comparing All Methods")
    print("=" * 60)
    
    scenarios = [
        (50, 100),   # Balanced
        (10, 100),   # Low proportion
        (90, 100),   # High proportion
        (5, 10),     # Small sample
        (0, 10),     # Zero successes
    ]
    
    for successes, trials in scenarios:
        print(f"\nProportion: {successes}/{trials} ({successes/trials:.2%})")
        comparison = compare_intervals(successes, trials)
        
        print("  Method comparisons:")
        for method, interval in comparison.items():
            width = interval.upper - interval.lower
            print(f"    {method}:")
            print(f"      [{interval.lower:.4f}, {interval.upper:.4f}] (width: {width:.4f})")
    
    print("\nMethod selection guide:")
    print("  - Wilson Score: Best for ranking, small samples")
    print("  - Agresti-Coull: Simple, good for most cases")
    print("  - Clopper-Pearson: Conservative, guaranteed coverage")
    print("  - Jeffreys: Bayesian, good for small samples")
    print("  - Normal Approx: Simple but problematic for extremes")


def example_confidence_levels():
    """Effect of different confidence levels."""
    print("\n" + "=" * 60)
    print("Example 7: Confidence Level Effects")
    print("=" * 60)
    
    successes, trials = 50, 100
    confidence_levels = [0.80, 0.90, 0.95, 0.99]
    
    print(f"\nProportion: {successes}/{trials} ({successes/trials:.2%})")
    print("\nInterval width at different confidence levels:")
    
    for conf in confidence_levels:
        interval = wilson_score_interval(successes, trials, conf)
        width = interval.upper - interval.lower
        print(f"  {conf:.0%} confidence:")
        print(f"    [{interval.lower:.4f}, {interval.upper:.4f}]")
        print(f"    Width: {width:.4f}")
    
    print("\nInsight:")
    print("  - Higher confidence = wider interval")
    print("  - 95% is standard for most applications")
    print("  - 99% for critical decisions")


def example_practical_recommendations():
    """Practical recommendations."""
    print("\n" + "=" * 60)
    print("Example 8: Practical Recommendations")
    print("=" * 60)
    
    print("\nWhen to use Wilson Score:")
    print("  1. Ranking products/reviews by rating")
    print("  2. Reddit-style comment ranking")
    print("  3. A/B test result comparison")
    print("  4. Any proportion ranking with varying sample sizes")
    
    print("\nBest practices:")
    print("  - Use Wilson LOWER bound for conservative ranking")
    print("  - Use Wilson CENTER for balanced ranking")
    print("  - Consider minimum sample threshold (e.g., 5 votes)")
    print("  - Display confidence intervals to users")
    
    print("\nImplementation tips:")
    print("  - Pre-compute Wilson scores for all items")
    print("  - Cache results to avoid repeated calculation")
    print("  - Use 95% confidence as default")
    print("  - Handle edge cases (0 votes, 100% votes)")
    
    print("\nExample ranking code:")
    print("""
    # Python
    from wilson_score_utils import wilson_center
    
    def rank_items(items):
        return sorted(items, 
                     key=lambda x: wilson_center(x.upvotes, x.total),
                     reverse=True)
    """)


def main():
    """Run all examples."""
    print("=" * 60)
    print("Wilson Score Interval - Practical Examples")
    print("=" * 60)
    
    example_basic_wilson()
    example_reddit_ranking()
    example_product_ratings()
    example_five_star_ratings()
    example_ab_testing()
    example_compare_methods()
    example_confidence_levels()
    example_practical_recommendations()
    
    print("\n" + "=" * 60)
    print("Examples completed!")
    print("=" * 60)


if __name__ == '__main__':
    main()
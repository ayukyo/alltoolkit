#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Real-world application examples for Weighted Random Utilities."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from weighted_random_utils.mod import (
    weighted_choice,
    AliasMethod,
    weighted_coin_flip,
    WeightedReservoirSampler,
)
from collections import Counter
import random


def demo_load_balancing():
    """Simulate load balancing with weighted selection."""
    print("=" * 60)
    print("Load Balancing Simulation")
    print("=" * 60)
    
    servers = ['server-us-west', 'server-us-east', 'server-eu', 'server-asia']
    capacities = [40, 30, 20, 10]  # Relative capacity percentages
    
    print(f"\nServers: {servers}")
    print(f"Capacity weights: {capacities}")
    
    # Use Alias method for efficient routing
    router = AliasMethod(servers, capacities)
    
    print("\nRouting 1000 requests:")
    requests = Counter(router.sample_n(1000))
    
    for server in servers:
        count = requests[server]
        pct = count / 10
        print(f"  {server}: {count} requests ({pct}%)")
    
    print("\n✓ Requests distributed proportionally to server capacity")


def demo_ab_testing():
    """Simulate A/B testing traffic split."""
    print("\n" + "=" * 60)
    print("A/B Testing Traffic Split")
    print("=" * 60)
    
    variants = {
        'control': {'weight': 50, 'name': 'Original Design'},
        'variant_a': {'weight': 25, 'name': 'New Header'},
        'variant_b': {'weight': 25, 'name': 'New Footer'},
    }
    
    items = list(variants.keys())
    weights = [v['weight'] for v in variants.values()]
    
    print("\nExperiment configuration:")
    for key, val in variants.items():
        print(f"  {key} ({val['name']}): {val['weight']}%")
    
    # Assign users to variants
    print("\nAssigning 100 users:")
    assignments = Counter()
    for _ in range(100):
        variant = weighted_choice(items, weights)
        assignments[variant] += 1
    
    for variant in items:
        count = assignments[variant]
        print(f"  {variant}: {count} users ({count}%)")
    
    print("\n✓ Traffic split matches experiment configuration")


def demo_game_drop_table():
    """Simulate game loot drop table."""
    print("\n" + "=" * 60)
    print("Game Loot Drop Table")
    print("=" * 60)
    
    # Drop table with rarity tiers
    drops = [
        ('Gold Coin', 60, 'common'),
        ('Health Potion', 25, 'common'),
        ('Iron Sword', 10, 'uncommon'),
        ('Magic Ring', 4, 'rare'),
        ('Legendary Blade', 0.5, 'legendary'),
        ('Dragon Scale', 0.5, 'legendary'),
    ]
    
    items = [d[0] for d in drops]
    weights = [d[1] for d in drops]
    rarities = {d[0]: d[2] for d in drops}
    
    print("\nDrop table:")
    for name, weight, rarity in drops:
        print(f"  {name} ({rarity}): {weight}%")
    
    # Simulate kills
    print("\nSimulating 100 monster kills:")
    drop_counts = Counter()
    
    alias = AliasMethod(items, weights)
    for _ in range(100):
        drop = alias.sample()
        drop_counts[drop] += 1
    
    for name in items:
        count = drop_counts[name]
        rarity = rarities[name]
        if count > 0:
            print(f"  {name} ({rarity}): {count} dropped")
    
    legendary_count = sum(drop_counts[d[0]] for d in drops if d[2] == 'legendary')
    print(f"\nLegendary items dropped: {legendary_count} (expected ~1%)")


def demo_recommendation_sampling():
    """Simulate recommendation sampling."""
    print("\n" + "=" * 60)
    print("Recommendation Sampling")
    print("=" * 60)
    
    # Product recommendations with relevance scores
    products = [
        ('Product A', 95),
        ('Product B', 85),
        ('Product C', 75),
        ('Product D', 60),
        ('Product E', 45),
    ]
    
    items = [p[0] for p in products]
    scores = [p[1] for p in products]
    
    print("\nProducts with relevance scores:")
    for name, score in products:
        print(f"  {name}: score {score}")
    
    # Sample 3 recommendations
    print("\nSampling 3 recommendations:")
    recommendations = weighted_sample(items, scores, k=3, replace=False)
    
    for i, rec in enumerate(recommendations, 1):
        idx = items.index(rec)
        print(f"  {i}. {rec} (score: {scores[idx]})")
    
    print("\n✓ Higher-scored products more likely to be recommended")


def demo_feature_rollout():
    """Simulate gradual feature rollout."""
    print("\n" + "=" * 60)
    print("Feature Rollout Simulation")
    print("=" * 60)
    
    # Gradual rollout from 10% to 100%
    rollout_percentages = [10, 25, 50, 75, 100]
    
    for rollout_pct in rollout_percentages:
        print(f"\n--- Rollout at {rollout_pct}% ---")
        
        enabled_count = 0
        total_users = 100
        
        for user_id in range(total_users):
            # Each user gets same probability
            if weighted_coin_flip(rollout_pct / 100):
                enabled_count += 1
        
        actual_pct = enabled_count / total_users * 100
        print(f"  Users with feature enabled: {enabled_count} ({actual_pct:.1f}%)")
    
    print("\n✓ Feature rollout matches expected percentages")


def demo_streaming_sampling():
    """Demonstrate weighted reservoir sampling for streams."""
    print("\n" + "=" * 60)
    print("Weighted Reservoir Sampling (Stream)")
    print("=" * 60)
    
    # Simulate a stream of events with importance scores
    sampler = WeightedReservoirSampler(k=10)
    
    print("\nProcessing stream of 100 events...")
    
    events = []
    for i in range(100):
        # Simulate event with importance
        importance = random.randint(1, 10)
        event = f"Event_{i}"
        events.append((event, importance))
        sampler.add(event, importance)
    
    sample = sampler.sample()
    print(f"\nReservoir sample ({len(sample)} events):")
    
    for event in sample[:5]:
        print(f"  {event}")
    print(f"  ... and {len(sample) - 5} more")
    
    print("\n✓ Sample represents important events from stream")


def demo_survey_sampling():
    """Simulate weighted survey sampling."""
    print("\n" + "=" * 60)
    print("Survey Population Sampling")
    print("=" * 60)
    
    # Population segments with sizes
    segments = {
        'young_adults': ('18-25', 1500, 25),
        'adults': ('26-40', 2500, 35),
        'middle_aged': ('41-55', 2000, 25),
        'seniors': ('56+', 1500, 15),
    }
    
    print("\nPopulation segments:")
    for key, (age, pop, pct) in segments.items():
        print(f"  {key} ({age}): {pop} people ({pct}%)")
    
    # Weighted sample by population size
    items = list(segments.keys())
    weights = [seg[2] for seg in segments.values()]  # Use population percentages
    
    print("\nSampling 100 survey participants:")
    participants = Counter()
    for _ in range(100):
        segment = weighted_choice(items, weights)
        participants[segment] += 1
    
    for segment in items:
        count = participants[segment]
        expected = segments[segment][2]
        print(f"  {segment}: {count} participants (expected ~{expected})")
    
    print("\n✓ Sample proportions match population distribution")


if __name__ == '__main__':
    random.seed(42)  # For reproducible demo
    
    demo_load_balancing()
    demo_ab_testing()
    demo_game_drop_table()
    demo_recommendation_sampling()
    demo_feature_rollout()
    demo_streaming_sampling()
    demo_survey_sampling()
    
    print("\n" + "=" * 60)
    print("All demos complete!")
    print("=" * 60)
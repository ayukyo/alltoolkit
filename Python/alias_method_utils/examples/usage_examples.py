"""
Alias Method Utils - Usage Examples

This file demonstrates practical use cases for Walker's Alias Method,
an algorithm for O(1) weighted random sampling.

Applications:
1. Game Development - Loot tables, spawn rates, weighted NPCs
2. A/B Testing - Traffic splitting with weighted variants
3. Load Balancing - Weighted server selection
4. Monte Carlo Simulations - Sampling from discrete distributions
5. Natural Language Processing - Word sampling, text generation
"""

import random
from mod import (
    AliasMethod,
    WeightedRandomPicker,
    AliasMethodBuilder,
    create_alias_from_dict,
    sample_with_weights,
    weighted_shuffle,
)


def example_basic_sampling():
    """Example 1: Basic weighted random sampling."""
    print("=" * 60)
    print("Example 1: Basic Weighted Random Sampling")
    print("=" * 60)
    
    # Create a distribution where:
    # - Index 0 has 10% probability
    # - Index 1 has 30% probability
    # - Index 2 has 60% probability
    weights = [1, 3, 6]
    alias = AliasMethod(weights)
    
    print(f"Weights: {weights}")
    print(f"Probabilities: {[f'{p:.2%}' for p in alias.probabilities]}")
    
    # Sample multiple times
    print("\nSampling 20 times:")
    samples = [alias.sample() for _ in range(20)]
    print(f"Samples: {samples}")
    
    # Count distribution
    samples = [alias.sample() for _ in range(10000)]
    counts = {}
    for s in samples:
        counts[s] = counts.get(s, 0) + 1
    
    print("\nDistribution after 10000 samples:")
    for i in range(3):
        expected = weights[i] / sum(weights)
        actual = counts.get(i, 0) / 10000
        print(f"  Index {i}: expected {expected:.2%}, actual {actual:.2%}")


def example_game_loot_table():
    """Example 2: Game loot table with weighted drops."""
    print("\n" + "=" * 60)
    print("Example 2: Game Loot Table")
    print("=" * 60)
    
    # Define loot items with drop weights
    loot_table = {
        'Common Sword': 100,
        'Health Potion': 80,
        'Iron Shield': 50,
        'Magic Ring': 20,
        'Rare Gem': 10,
        'Legendary Sword': 1,
    }
    
    # Create picker from dictionary
    loot_picker = create_alias_from_dict(loot_table)
    
    print("Loot Table (weights):")
    for item, weight in loot_table.items():
        print(f"  {item}: {weight}")
    
    print("\nProbabilities:")
    for item, prob in zip(loot_picker.items, loot_picker.probabilities):
        print(f"  {item}: {prob:.2%}")
    
    # Simulate opening 10 chests
    print("\nOpening 10 treasure chests:")
    for i in range(10):
        item = loot_picker.pick()
        print(f"  Chest {i+1}: {item}")
    
    # Simulate many drops to verify distribution
    print("\nDrops after 10000 chests:")
    drops = {}
    for _ in range(10000):
        item = loot_picker.pick()
        drops[item] = drops.get(item, 0) + 1
    
    for item in sorted(loot_table.keys(), key=lambda x: loot_table[x], reverse=True):
        actual = drops.get(item, 0) / 10000
        expected = loot_table[item] / sum(loot_table.values())
        print(f"  {item}: expected {expected:.2%}, actual {actual:.2%}")


def example_ab_testing():
    """Example 3: A/B testing traffic splitting."""
    print("\n" + "=" * 60)
    print("Example 3: A/B Testing Traffic Splitting")
    print("=" * 60)
    
    # Define test variants with traffic percentages
    variants = [
        ('control', 'Original design', 50),      # 50% traffic
        ('variant_a', 'New button color', 25),   # 25% traffic
        ('variant_b', 'New layout', 20),         # 20% traffic
        ('variant_c', 'New headline', 5),        # 5% traffic
    ]
    
    # Create picker
    variant_names = [v[0] for v in variants]
    variant_weights = [v[2] for v in variants]
    picker = WeightedRandomPicker(variant_names, variant_weights)
    
    print("Test Variants:")
    for name, desc, weight in variants:
        print(f"  {name}: {desc} ({weight}% traffic)")
    
    # Assign 20 users to variants
    print("\nAssigning 20 users to variants:")
    for i in range(20):
        variant = picker.pick()
        print(f"  User {i+1}: {variant}")
    
    # Verify distribution
    print("\nTraffic distribution after 10000 users:")
    assignments = {}
    for _ in range(10000):
        variant = picker.pick()
        assignments[variant] = assignments.get(variant, 0) + 1
    
    for name, _, expected in variants:
        actual = assignments.get(name, 0) / 100
        print(f"  {name}: expected {expected}%, actual {actual:.1f}%")


def example_load_balancing():
    """Example 4: Weighted load balancing."""
    print("\n" + "=" * 60)
    print("Example 4: Weighted Load Balancing")
    print("=" * 60)
    
    # Server pool with capacities (weights)
    servers = {
        'server-high-capacity-1': 100,  # Can handle 100 requests/sec
        'server-high-capacity-2': 100,  # Can handle 100 requests/sec
        'server-medium-1': 50,          # Can handle 50 requests/sec
        'server-medium-2': 50,          # Can handle 50 requests/sec
        'server-low-1': 20,             # Can handle 20 requests/sec
    }
    
    lb = create_alias_from_dict(servers)
    
    print("Server Pool:")
    for server, capacity in servers.items():
        print(f"  {server}: {capacity} req/s")
    
    total_capacity = sum(servers.values())
    
    print("\nSimulating 15 requests:")
    for i in range(15):
        server = lb.pick()
        print(f"  Request {i+1} -> {server}")
    
    # Verify distribution
    print("\nRequest distribution after 10000 requests:")
    distribution = {}
    for _ in range(10000):
        server = lb.pick()
        distribution[server] = distribution.get(server, 0) + 1
    
    for server in servers:
        expected = servers[server] / total_capacity * 100
        actual = distribution.get(server, 0) / 100
        print(f"  {server}: expected {expected:.1f}%, actual {actual:.1f}%")


def example_builder_pattern():
    """Example 5: Using the builder pattern for dynamic construction."""
    print("\n" + "=" * 60)
    print("Example 5: Builder Pattern for Dynamic Construction")
    print("=" * 60)
    
    # Build incrementally
    builder = AliasMethodBuilder()
    
    print("Building distribution incrementally...")
    
    builder.add('Apple', 3)
    print("  Added Apple (weight: 3)")
    
    builder.add('Banana', 2)
    print("  Added Banana (weight: 2)")
    
    builder.add('Cherry', 1)
    print("  Added Cherry (weight: 1)")
    
    builder.add('Date', 4)
    print("  Added Date (weight: 4)")
    
    print(f"\nTotal items: {builder.size}")
    
    # Build the picker
    picker = builder.build_picker()
    
    print("\nProbabilities:")
    for item, prob in zip(picker.items, picker.probabilities):
        print(f"  {item}: {prob:.2%}")
    
    print("\nSampling 10 times:")
    for _ in range(10):
        print(f"  {picker.pick()}")


def example_weighted_shuffle():
    """Example 6: Weighted shuffle for prioritized ordering."""
    print("\n" + "=" * 60)
    print("Example 6: Weighted Shuffle")
    print("=" * 60)
    
    # Tasks with priority weights (higher = more urgent)
    tasks = ['Check email', 'Review code', 'Fix bug', 'Write docs', 'Meeting']
    priorities = [1, 3, 5, 2, 1]  # 'Fix bug' has highest priority
    
    print("Tasks with priorities:")
    for task, priority in zip(tasks, priorities):
        print(f"  {task}: priority {priority}")
    
    print("\nShuffled 5 times (higher priority more likely first):")
    for i in range(5):
        shuffled = weighted_shuffle(tasks, priorities)
        print(f"  Shuffle {i+1}: {shuffled}")
    
    # Verify: count how often 'Fix bug' appears in first position
    first_count = 0
    trials = 10000
    for _ in range(trials):
        shuffled = weighted_shuffle(tasks, priorities)
        if shuffled[0] == 'Fix bug':
            first_count += 1
    
    expected = priorities[2] / sum(priorities)
    actual = first_count / trials
    print(f"\n'Fix bug' in first position:")
    print(f"  Expected: {expected:.2%}")
    print(f"  Actual: {actual:.2%}")


def example_monte_carlo():
    """Example 7: Monte Carlo simulation with discrete distribution."""
    print("\n" + "=" * 60)
    print("Example 7: Monte Carlo Simulation")
    print("=" * 60)
    
    # Simulate rolling a weighted die
    # Faces: 1, 2, 3, 4, 5, 6
    # Weights: standard die is fair, but let's make it loaded
    faces = [1, 2, 3, 4, 5, 6]
    weights = [1, 1, 1, 1, 1, 2]  # 6 is twice as likely
    
    picker = WeightedRandomPicker(faces, weights)
    
    print("Loaded Die (6 is twice as likely):")
    print(f"  Faces: {faces}")
    print(f"  Weights: {weights}")
    
    # Roll many times and compute statistics
    rolls = [picker.pick() for _ in range(100000)]
    
    avg = sum(rolls) / len(rolls)
    counts = {}
    for r in rolls:
        counts[r] = counts.get(r, 0) + 1
    
    print("\nRoll statistics (100,000 rolls):")
    print(f"  Average: {avg:.4f}")
    print("  Distribution:")
    for face in faces:
        expected = weights[face-1] / sum(weights)
        actual = counts.get(face, 0) / len(rolls)
        print(f"    Face {face}: expected {expected:.2%}, actual {actual:.2%}")


def example_text_generation():
    """Example 8: Simple text generation with weighted word selection."""
    print("\n" + "=" * 60)
    print("Example 8: Weighted Text Generation")
    print("=" * 60)
    
    # Word categories with weights
    subjects = {
        'The cat': 30,
        'The dog': 30,
        'A bird': 20,
        'My friend': 15,
        'The wizard': 5,
    }
    
    verbs = {
        'jumps over': 25,
        'runs around': 25,
        'flies past': 15,
        'walks beside': 20,
        'teleports past': 5,
        'dances with': 10,
    }
    
    objects = {
        'the fence': 30,
        'a tree': 25,
        'the house': 20,
        'the moon': 10,
        'a rainbow': 15,
    }
    
    # Create pickers
    subject_picker = create_alias_from_dict(subjects)
    verb_picker = create_alias_from_dict(verbs)
    object_picker = create_alias_from_dict(objects)
    
    print("Generating 10 sentences:")
    for i in range(10):
        sentence = f"{subject_picker.pick()} {verb_picker.pick()} {object_picker.pick()}."
        print(f"  {i+1}. {sentence}")


def example_sampling_without_replacement():
    """Example 9: Sampling without replacement."""
    print("\n" + "=" * 60)
    print("Example 9: Sampling Without Replacement")
    print("=" * 60)
    
    # Lottery with different ticket weights
    participants = ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve', 'Frank']
    tickets = [5, 3, 2, 8, 1, 4]  # Diana has the most tickets
    
    picker = WeightedRandomPicker(participants, tickets)
    
    print("Lottery Participants:")
    for name, ticket_count in zip(participants, tickets):
        print(f"  {name}: {ticket_count} tickets")
    
    # Draw 3 winners without replacement
    print("\nDrawing 3 winners (no repeats):")
    winners = picker.pick_n(3, replace=False)
    for i, winner in enumerate(winners, 1):
        print(f"  {i}st place: {winner}")
    
    # Run many lotteries to see win rates
    print("\nWin rate distribution (10000 lotteries):")
    win_counts = {name: 0 for name in participants}
    for _ in range(10000):
        winners = picker.pick_n(3, replace=False)
        for winner in winners:
            win_counts[winner] += 1
    
    for name, tickets_count in sorted(zip(participants, tickets), 
                                       key=lambda x: x[1], reverse=True):
        win_rate = win_counts[name] / 10000
        print(f"  {name} ({tickets_count} tickets): won {win_rate:.2%} of lotteries")


def example_performance_comparison():
    """Example 10: Performance comparison."""
    print("\n" + "=" * 60)
    print("Example 10: Performance Comparison")
    print("=" * 60)
    
    import time
    
    # Create large distribution
    n = 100000
    weights = list(range(1, n + 1))
    
    print(f"Creating distribution with {n} items...")
    
    # Measure construction time
    start = time.time()
    alias = AliasMethod(weights)
    construction_time = time.time() - start
    print(f"  Construction time: {construction_time*1000:.2f} ms")
    
    # Measure sampling time
    samples_count = 1000000
    print(f"\nSampling {samples_count:,} times...")
    start = time.time()
    for _ in range(samples_count):
        alias.sample()
    sampling_time = time.time() - start
    
    print(f"  Total time: {sampling_time:.4f} seconds")
    print(f"  Per sample: {sampling_time/samples_count*1e6:.2f} microseconds")
    print(f"  Samples/second: {samples_count/sampling_time:,.0f}")


def main():
    """Run all examples."""
    example_basic_sampling()
    example_game_loot_table()
    example_ab_testing()
    example_load_balancing()
    example_builder_pattern()
    example_weighted_shuffle()
    example_monte_carlo()
    example_text_generation()
    example_sampling_without_replacement()
    example_performance_comparison()
    
    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60)


if __name__ == '__main__':
    main()
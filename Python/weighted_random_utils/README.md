# Weighted Random Utilities

A comprehensive Python module for weighted random selection with zero external dependencies.

## Features

- **Basic Weighted Selection**: `weighted_choice()`, `weighted_sample()`
- **O(1) Selection**: Alias method for efficient repeated sampling
- **Streaming Sampling**: Weighted reservoir sampling for data streams
- **Weight Utilities**: Normalization, softmax, exponential decay
- **Distribution Functions**: Inverse transform, rejection sampling
- **Probability Utilities**: KL divergence, entropy, effective sample size

## Installation

No installation required! Just copy the `mod.py` file to your project.

## Quick Start

```python
from weighted_random_utils.mod import weighted_choice, AliasMethod

# Basic weighted selection
items = ['apple', 'banana', 'cherry', 'date']
weights = [1, 2, 3, 4]

result = weighted_choice(items, weights)
print(result)  # Randomly selected based on weights

# Efficient repeated sampling with Alias method
alias = AliasMethod(items, weights)
samples = alias.sample_n(1000)  # 1000 samples in O(1) each
```

## Core Functions

### Basic Selection

```python
from weighted_random_utils.mod import (
    weighted_choice,
    weighted_choice_with_index,
    weighted_sample,
    weighted_shuffle
)

items = ['a', 'b', 'c', 'd']
weights = [1, 2, 3, 4]

# Single selection
item = weighted_choice(items, weights)

# Selection with index
item, index = weighted_choice_with_index(items, weights)

# Multiple samples (with replacement)
samples = weighted_sample(items, weights, k=10)

# Multiple samples (without replacement)
samples = weighted_sample(items, weights, k=3, replace=False)

# Weighted shuffle (higher weights more likely to appear earlier)
shuffled = weighted_shuffle(items, weights)
```

### Alias Method (O(1) Selection)

Ideal when making many selections from the same distribution:

```python
from weighted_random_utils.mod import AliasMethod

items = ['common', 'rare', 'legendary']
weights = [70, 25, 5]

# Preprocessing: O(n)
alias = AliasMethod(items, weights)

# Each selection: O(1)
for _ in range(10000):
    item = alias.sample()  # Very fast!
```

### Weighted Reservoir Sampling

For sampling from streaming data:

```python
from weighted_random_utils.mod import WeightedReservoirSampler

sampler = WeightedReservoirSampler(k=100)

# Process stream
for item, weight in data_stream:
    sampler.add(item, weight)

# Get sample
sample = sampler.sample()
```

### Weight Utilities

```python
from weighted_random_utils.mod import (
    normalize_weights,
    cumulative_weights,
    softmax_weights,
    exponential_weights
)

weights = [1, 2, 3, 4]

# Normalize to probabilities
probs = normalize_weights(weights)  # [0.1, 0.2, 0.3, 0.4]

# Cumulative sum
cumulative = cumulative_weights(weights)  # [1, 3, 6, 10]

# Softmax transformation
softmax_probs = softmax_weights([1, 2, 3], temperature=1.0)

# Exponential decay
decayed = exponential_weights(weights, decay=0.5)
```

### Probability Utilities

```python
from weighted_random_utils.mod import (
    kl_divergence,
    entropy,
    effective_size
)

# KL divergence between distributions
p = [0.5, 0.3, 0.2]
q = [0.4, 0.4, 0.2]
div = kl_divergence(p, q)

# Shannon entropy
e = entropy(p)  # In bits

# Effective sample size (for importance sampling)
weights = [1, 2, 2, 1]
ess = effective_size(weights)
```

### Distribution Functions

```python
from weighted_random_utils.mod import (
    inverse_transform_sample,
    rejection_sample
)

# Inverse transform sampling from CDF
cdf = [0.1, 0.3, 0.6, 1.0]
values = ['a', 'b', 'c', 'd']
result = inverse_transform_sample(cdf, values)

# Rejection sampling
import random
proposal = lambda: random.random()  # Uniform [0, 1]
acceptance = lambda x: x  # Higher values more likely
samples = rejection_sample(proposal, acceptance, n=100)
```

### Convenience Functions

```python
from weighted_random_utils.mod import (
    weighted_coin_flip,
    weighted_random_range,
    batch_weighted_choice
)

# Weighted coin flip
result = weighted_coin_flip(0.7)  # True with 70% probability

# Weighted integer range
weights = [1, 2, 3, 4]
num = weighted_random_range(0, 4, weights)  # 0-3 with weights

# Batch sampling (more efficient for large batches)
samples = batch_weighted_choice(items, weights, n=10000)
```

## Reproducibility

All functions accept a `random_instance` parameter for reproducible results:

```python
import random

rng = random.Random(42)
result1 = weighted_choice(items, weights, random_instance=rng)

rng = random.Random(42)
result2 = weighted_choice(items, weights, random_instance=rng)

assert result1 == result2  # Same seed = same result
```

## Performance

| Operation | Time Complexity | Space Complexity |
|-----------|-----------------|------------------|
| `weighted_choice` | O(n) | O(1) |
| `AliasMethod` construction | O(n) | O(n) |
| `AliasMethod.sample` | O(1) | O(1) |
| `WeightedReservoirSampler.add` | O(log k) | O(k) |
| `weighted_shuffle` | O(n²) | O(n) |

For repeated sampling from the same distribution, `AliasMethod` is recommended.

## Error Handling

The module provides specific exceptions:

```python
from weighted_random_utils.mod import (
    EmptyWeightsError,
    InvalidWeightError,
    TotalWeightZeroError
)

try:
    weighted_choice([], [])
except EmptyWeightsError:
    print("Items or weights are empty")

try:
    weighted_choice(['a', 'b'], [1, -1])
except InvalidWeightError:
    print("Weight cannot be negative")

try:
    weighted_choice(['a', 'b'], [0, 0])
except TotalWeightZeroError:
    print("Total weight cannot be zero")
```

## Use Cases

### Load Balancing
```python
servers = ['server1', 'server2', 'server3']
capacities = [10, 20, 30]  # Relative capacities

alias = AliasMethod(servers, capacities)
selected_server = alias.sample()
```

### A/B Testing
```python
variants = ['control', 'variant_a', 'variant_b']
traffic_split = [50, 25, 25]  # 50-25-25 split

user_variant = weighted_choice(variants, traffic_split)
```

### Game Drop Tables
```python
items = ['common', 'uncommon', 'rare', 'legendary']
drop_rates = [60, 25, 12, 3]

drop = weighted_choice(items, drop_rates)
```

### Recommendation Sampling
```python
items = recommendations
relevance_scores = [r.score for r in recommendations]

# Sample based on relevance
sampled = weighted_sample(items, relevance_scores, k=10)
```

## Testing

Run the test suite:

```bash
python weighted_random_utils_test.py
```

## License

MIT License - Part of AllToolkit
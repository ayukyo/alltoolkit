# Caffeine Metabolism Utils

Track caffeine consumption and metabolism over time. Zero external dependencies.

## Features

- **Caffeine Level Tracking**: Calculate current caffeine levels based on consumption history
- **Half-Life Modeling**: Accurate pharmacokinetic model with customizable half-life
- **Sleep Timing Recommendations**: Find optimal bedtime based on caffeine levels
- **Beverage Database**: 50+ predefined beverages with caffeine content
- **Sensitivity Analysis**: Estimate personal caffeine metabolism
- **Data Export/Import**: Save and restore consumption logs

## Quick Start

```python
from caffeine_metabolism_utils.mod import CaffeineMetabolismTracker

# Create tracker
tracker = CaffeineMetabolismTracker()

# Log consumption
tracker.consume_beverage("drip_coffee_medium")  # 165mg
tracker.consume(100, source="custom_supplement")  # Custom amount

# Check current level
print(f"Current caffeine: {tracker.get_current_level():.1f}mg")

# Get sleep recommendation
rec = tracker.get_sleep_recommendation()
print(f"Safe to sleep at 10pm: {rec['is_safe_to_sleep']}")
```

## API Reference

### CaffeineMetabolismTracker

Main class for tracking caffeine consumption.

#### Constructor

```python
tracker = CaffeineMetabolismTracker(
    half_life_hours=5.0,        # Caffeine half-life (default 5 hours)
    sleep_safe_threshold_mg=25  # Level safe for sleep
)
```

#### Methods

| Method | Description |
|--------|-------------|
| `consume(amount_mg, timestamp?, source?, absorption_delay_minutes?)` | Log caffeine consumption |
| `consume_beverage(beverage_key, timestamp?, custom_amount_mg?)` | Log using predefined beverage |
| `get_current_level(at_time?)` | Get current caffeine level |
| `get_level_at(target_time)` | Get level at specific time |
| `get_level_history(start, end, interval_minutes?)` | Get level timeline |
| `time_until_threshold(threshold_mg?, from_time?)` | Time until level drops below threshold |
| `get_sleep_recommendation(target_bedtime?, from_time?)` | Get sleep timing advice |
| `get_daily_total(date?)` | Get total consumed today |
| `get_status(at_time?)` | Get comprehensive status |
| `clear_old_entries(older_than_hours?)` | Remove old entries |
| `export_data()` | Export entries as list |
| `import_data(list)` | Import entries from list |

### Helper Functions

```python
# Simple decay calculation
remaining = calculate_caffeine_decay(100, hours=5, half_life_hours=5.0)

# Estimate half-life from observations
half_life = calculate_half_life_from_data(
    initial_mg=100,
    remaining_mg=50,
    hours_elapsed=5
)

# Get sensitivity estimate
sensitivity = estimate_caffeine_sensitivity("poor", hours_before_bed=4)

# Find caffeine equivalents
equiv = caffeine_equivalent(200, as_beverage="espresso_single")
```

## Beverage Database

Available beverages include:

**Coffee**: espresso_single (63mg), espresso_double (125mg), drip_coffee_medium (165mg), cold_brew_medium (300mg), latte, cappuccino, americano

**Tea**: black_tea (47mg), green_tea (28mg), white_tea (25mg), matcha (70mg), chai_tea

**Energy Drinks**: red_bull_small (80mg), monster_small (160mg), bang_energy (300mg), celcius

**Soda**: coke_can (34mg), pepsi_can (38mg), mountain_dew_can (54mg)

**Other**: dark_chocolate_bar, pre_workout, energy_shot

```python
# List all beverages
beverages = CaffeineMetabolismTracker.get_beverage_list()

# Search beverages
matches = CaffeineMetabolismTracker.search_beverages("coffee")
```

## Examples

### Track Daily Intake

```python
from datetime import datetime, timedelta

tracker = CaffeineMetabolismTracker()
now = datetime.now()

# Morning coffee
tracker.consume_beverage("drip_coffee_medium", timestamp=now.replace(hour=7))

# Afternoon pick-me-up
tracker.consume_beverage("espresso_single", timestamp=now.replace(hour=14))

# Check status
status = tracker.get_status()
print(f"Daily total: {status['daily_total_mg']}mg")
print(f"Within limit (400mg): {status['within_daily_limit']}")
```

### Custom Metabolism

```python
# Person with slower caffeine metabolism
tracker = CaffeineMetabolismTracker(
    half_life_hours=7.0,  # Extended half-life
    sleep_safe_threshold_mg=15  # More sensitive
)

tracker.consume_beverage("cold_brew_medium")
time_safe = tracker.time_until_threshold()
print(f"Wait {time_safe} before sleep")
```

### Level History

```python
start = datetime.now().replace(hour=6)
end = start + timedelta(hours=16)

history = tracker.get_level_history(start, end, interval_minutes=60)
for point in history:
    print(f"{point['timestamp']}: {point['level_mg']}mg")
```

## Pharmacokinetic Model

This module uses a first-order elimination model:

- **Absorption Phase**: Linear increase over 45 minutes (default)
- **Elimination Phase**: Exponential decay with half-life (default 5 hours)

Formula: `C(t) = C₀ × e^(-kt)` where `k = ln(2) / t½`

## Running Tests

```bash
python caffeine_metabolism_utils_test.py
```

## Running Examples

```bash
python examples/usage_examples.py
```

## License

MIT License
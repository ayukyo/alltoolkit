# Circadian Rhythm Utils

A comprehensive Python library for calculating optimal sleep/wake times, analyzing biological rhythms, and managing energy patterns throughout the day. Based on established circadian science principles.

**Zero external dependencies** - uses only Python standard library.

## Features

- 🌅 **Optimal Sleep Calculator** - Find best wake times based on 90-minute REM cycles
- ⏰ **Bedtime Optimizer** - Calculate ideal bedtimes for target wake times
- ⚡ **Alertness Prediction** - Model energy levels throughout the day
- 🦉 **Chronotype Support** - Lark, Owl, and Intermediate types
- 📅 **Activity Recommendations** - Best times for focus, exercise, social activities
- ✈️ **Jet Lag Recovery** - Estimate adjustment time after travel
- 😴 **Sleep Debt Analysis** - Calculate performance impact from sleep deprivation
- 💤 **Nap Recommendations** - When and how long to nap
- 🌙 **Melatonin Schedule** - Natural hormone production timing

## Quick Start

```python
from datetime import datetime
from circadian_rhythm_utils import (
    CircadianRhythmCalculator,
    Chronotype,
    get_best_wake_times,
    get_best_bedtimes,
    get_current_alertness,
)

# Quick functions
wake_times = get_best_wake_times(datetime(2026, 5, 15, 23, 0))
print(wake_times)
# [{'wake_time': '06:45', 'duration': '7h 45m', 'quality': 82.5, 'rem_cycles': 5}, ...]

bed_times = get_best_bedtimes(datetime(2026, 5, 16, 7, 0), Chronotype.OWL)
print(bed_times)
# [{'bedtime': '23:15', 'duration': '7h 45m', 'quality': 80.0, 'rem_cycles': 5}, ...]

alertness = get_current_alertness()
print(alertness)
# {'alertness_level': 'HIGH', 'alertness_score': 75.2, 'current_phase': 'Peak Performance'}
```

## Full API Usage

```python
from datetime import datetime, time
from circadian_rhythm_utils import (
    CircadianRhythmCalculator,
    Chronotype,
)

# Create calculator with your chronotype and age
calc = CircadianRhythmCalculator(Chronotype.OWL, age=28)

# Find optimal wake times for a bedtime
bedtime = datetime(2026, 5, 15, 23, 30)
windows = calc.calculate_optimal_wake_time(bedtime)

for window in windows[:3]:  # Top 3 options
    print(f"Wake at {window.wake_time.strftime('%H:%M')}")
    print(f"  Duration: {window.duration_hours:.1f} hours")
    print(f"  Quality: {window.quality_score:.0f}%")
    print(f"  REM cycles: {window.rem_cycles}")

# Get current circadian phase
phase = calc.get_current_phase()
print(f"Current phase: {phase.name}")
print(f"Alertness: {phase.alertness.name}")

# Get activity recommendations
recommendations = calc.get_activity_recommendations()
for rec in recommendations:
    print(f"{rec.time.strftime('%H:%M')} - {rec.activity}")

# Analyze sleep debt impact
impact = calc.get_sleep_debt_impact(5)  # Only 5 hours sleep
print(f"Cognitive performance: {impact['cognitive_performance']:.0f}%")
print(f"Overall functioning: {impact['overall']:.0f}%")

# Estimate your chronotype from preferences
chronotype = calc.estimate_chronotype(
    preferred_wake_time=time(8, 30),
    preferred_bedtime=time(0, 0)
)
print(f"Your chronotype: {chronotype.value}")
```

## Chronotypes

| Type | Natural Wake Time | Characteristics |
|------|------------------|-----------------|
| Extreme Lark | 4-5 AM | Very early riser, peak morning energy |
| Lark | 6-7 AM | Early riser, morning person |
| Intermediate | 7-8 AM | Average, flexible |
| Owl | 8-9 AM | Late riser, evening energy peak |
| Extreme Owl | 10+ AM | Very late riser, night owl |

## Sleep Quality Scoring

Sleep quality is calculated based on:

1. **Duration Alignment** - How close to recommended sleep duration
2. **Circadian Alignment** - Bedtime matches natural rhythm
3. **Wake Time Alertness** - Natural alertness at wake time

Scores range from 0-100, with higher being better.

## Alertness Model

The alertness model uses:

- **Sinusoidal circadian component** - Based on core body temperature rhythm
- **Evening peak** - Secondary alertness peak in early evening
- **Sleep pressure** - Builds throughout the day
- **Chronotype offset** - Adjusted for individual differences

## Installation

```python
# Just import - no external dependencies!
from circadian_rhythm_utils import CircadianRhythmCalculator
```

## Files

```
circadian_rhythm_utils/
├── __init__.py              # Package exports
├── circadian_rhythm.py      # Main implementation
├── test_circadian_rhythm.py # Comprehensive tests
├── example.py               # Usage examples
└── README.md                # This file
```

## Running Tests

```bash
python -m pytest test_circadian_rhythm.py -v
# Or
python test_circadian_rhythm.py
```

## Running Examples

```bash
python example.py
```

## License

MIT License - Part of AllToolkit
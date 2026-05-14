# Jet Lag Calculator Utils

A comprehensive Python utility for calculating jet lag severity, recovery time, and providing personalized sleep schedule recommendations for travelers.

## Features

- **Jet Lag Severity Calculation** - Scientific scoring based on time zone changes
- **Recovery Time Estimation** - Using evidence-based phase shift rates
- **Direction Awareness** - Eastward travel is harder than westward
- **Personalized Factors** - Age and chronotype (morning lark/night owl) affect recovery
- **Sleep Schedule Recommendations** - Gradual bedtime adjustments
- **Light Exposure Timing** - Optimal times for bright light and darkness
- **Recovery Timeline** - Day-by-day adjustment progress
- **Popular Routes** - Pre-configured common travel corridors

## Installation

Zero external dependencies - pure Python standard library.

```python
from jet_lag_calculator_utils.mod import (
    JetLagCalculator,
    calculate_jet_lag,
    quick_estimate,
    analyze_route,
)
```

## Quick Start

### Simple Calculation

```python
from jet_lag_calculator_utils.mod import calculate_jet_lag

# Calculate jet lag from New York (UTC-5) to Tokyo (UTC+9)
result = calculate_jet_lag(
    origin_offset=-5,
    destination_offset=9,
    age=30,
    sleep_type="intermediate"
)

print(f"Time difference: {result.time_difference} hours")
print(f"Direction: {result.direction.value}")
print(f"Severity: {result.severity_level}")
print(f"Recovery: {result.estimated_recovery_days} days")
```

### Quick Estimate

```python
from jet_lag_calculator_utils.mod import quick_estimate

# Quick check for a 5-hour time difference
estimate = quick_estimate(5)

print(f"Needs adjustment: {estimate['needs_adjustment']}")
print(f"Recovery: {estimate['estimated_recovery_days']} days")
```

### Popular Routes

```python
from jet_lag_calculator_utils.mod import analyze_route

# Analyze NYC to London route
route = analyze_route("NYC", "LHR", age=35)

print(f"Route: {route['route_name']}")
print(f"Severity: {route['severity']}")
print(f"Recovery: {route['recovery_days']} days")
for rec in route['key_recommendations']:
    print(f"  - {rec}")
```

## Advanced Usage

### Full Calculator with Personalization

```python
from jet_lag_calculator_utils.mod import (
    JetLagCalculator,
    TimezoneInfo,
    SleepType,
)
from datetime import time

# Create personalized calculator
calc = JetLagCalculator(
    age=45,
    sleep_type=SleepType.NIGHT_OWL,  # Night owls struggle more going east
    typical_bed_time=time(0, 30),      # 12:30 AM
    typical_wake_time=time(8, 30)      # 8:30 AM
)

# Define timezones
origin = TimezoneInfo(name="Los Angeles", utc_offset=-8)
dest = TimezoneInfo(name="London", utc_offset=0)

# Calculate
result = calc.calculate(origin, dest)

print(f"Severity Score: {result.severity_score}/100")
print(f"Estimated Recovery: {result.estimated_recovery_days} days")
print(f"Adjustment Rate: {result.adjustment_per_day} hours/day")
```

### Light Exposure Recommendations

```python
# Get optimal light exposure times
result = calc.calculate(origin, dest)

print("Light Exposure Timing:")
for period, advice in result.light_exposure_times.items():
    print(f"  {period}: {advice}")

# Output example (eastward travel):
# morning: Seek bright light (preferably sunlight) immediately after waking...
# evening: Avoid bright light 2-3 hours before bed...
# peak_bright: 6:00 - 10:00 AM local time
# avoid_bright: 8:00 PM - midnight local time
```

### Sleep Schedule Adjustments

```python
# Get recommended sleep schedule adjustments
schedule = result.optimal_sleep_schedule

for day, advice in schedule.items():
    print(f"{day}: {advice}")

# Output example:
# day_1: Bedtime: 22:30 (earlier by 30 min)
# day_2: Bedtime: 22:00 (cumulative earlier shift)
# strategy: Gradually shift bedtime earlier
# target: Adjust to destination bedtime over 5 days
```

### Recovery Timeline

```python
from datetime import datetime

# Get day-by-day recovery timeline
result = calc.calculate(origin, dest)
timeline = calc.get_recovery_timeline(result, start_date=datetime.now())

for day in timeline:
    print(f"Day {day['day']}: {day['date']}")
    print(f"  Remaining shift: {day['remaining_shift_hours']} hours")
    print(f"  Progress: {day['percent_recovered']:.0f}%")
    print(f"  Status: {day['status']}")
```

## Available Routes

Pre-configured popular travel corridors:

| Route | Time Diff | Direction |
|-------|-----------|-----------|
| LAX → JFK | 3h | East |
| NYC → LHR | 5h | East |
| LHR → NYC | 5h | West |
| NYC → TYO | 14h | East |
| TYO → NYC | 14h | West |
| SYD → LHR | 10h | West |
| LHR → SYD | 10h | East |
| SFO → HKG | 16h | West |
| DXB → SYD | 6h | East |
| SIN → LAX | 16h | East |

## Common Timezones

```python
from jet_lag_calculator_utils.mod import get_common_timezones

tz = get_common_timezones()
print(tz)
# {'UTC': 0, 'PST': -8, 'EST': -5, 'JST': 9, 'AEST': 10, ...}
```

## Science Behind It

### Phase Shift Rates

- **Eastward travel (phase advance)**: ~0.8 hours/day
- **Westward travel (phase delay)**: ~1.2 hours/day

Going east is harder because your body prefers to delay (stay up later) rather than advance (go to bed earlier).

### Factors Affecting Recovery

1. **Direction**: East > West in difficulty
2. **Age**: Younger people recover faster
3. **Chronotype**: Night owls struggle more going east; morning larks struggle more going west
4. **Time zones crossed**: More zones = longer recovery

### Light Timing Strategy

- **Eastward**: Morning light advances your clock → seek bright light in AM
- **Westward**: Evening light delays your clock → seek bright light in PM

## API Reference

### `JetLagCalculator`

```python
JetLagCalculator(
    age: int = 30,
    sleep_type: SleepType = SleepType.INTERMEDIATE,
    typical_bed_time: time = time(23, 0),
    typical_wake_time: time = time(7, 0)
)
```

#### Methods

- `calculate(origin, dest, travel_date, flight_duration)` → `JetLagResult`
- `get_recovery_timeline(result, start_date)` → `List[Dict]`

### `JetLagResult`

| Field | Type | Description |
|-------|------|-------------|
| `time_difference` | float | Hours between zones |
| `direction` | TravelDirection | EAST, WEST, or NONE |
| `severity_score` | float | 0-100 severity |
| `severity_level` | str | Minimal/Mild/Moderate/Severe/Extreme |
| `estimated_recovery_days` | float | Days to full adjustment |
| `adjustment_per_day` | float | Hours body adjusts daily |
| `recommendations` | List[str] | Personalized tips |
| `optimal_sleep_schedule` | Dict | Bedtime adjustments |
| `light_exposure_times` | Dict | Light timing advice |
| `phase_shift_needed` | float | Total hours to shift |

### Convenience Functions

```python
calculate_jet_lag(origin_offset, dest_offset, age, sleep_type) → JetLagResult
quick_estimate(hours_diff) → Dict
analyze_route(origin_code, dest_code, age) → Dict
get_common_timezones() → Dict[str, float]
```

## Running Tests

```bash
python -m jet_lag_calculator_utils.test
```

Or:

```bash
cd Python/jet_lag_calculator_utils
python test.py
```

## Example Output

```
NYC → Tokyo (14h east):
  Severity: Extreme (87/100)
  Recovery: 17.5 days
  Recommendations:
    - Start adjusting your sleep schedule 3-5 days before departure...
    - Seek bright light in the morning at your destination...
    - Consider melatonin (0.5-3mg) at local bedtime...
    - Avoid bright light 2-3 hours before bed...
    - Stay hydrated during the flight...
```

## License

MIT License - Part of AllToolkit

## Contributing

Contributions welcome! Please ensure all tests pass and maintain zero external dependencies.
# Cycling Utilities

Comprehensive cycling calculation toolkit with zero external dependencies.

## Features

- **Speed/Distance/Time Calculations**: Calculate speed, time needed, or distance covered
- **Power Estimation**: Estimate required power based on speed, gradient, and conditions
- **Calorie Expenditure**: Calculate calories burned from power or heart rate
- **Gear Ratio Analysis**: Calculate gear ratios, development, and cadence-speed conversions
- **Climbing Metrics**: Gradient, elevation gain, VAM, and difficulty scores
- **Training Analysis**: Normalized Power (NP), Training Stress Score (TSS), Intensity Factor (IF)

## Installation

No installation required - pure Python standard library implementation.

```python
from cycling_utils.mod import CyclingUtils, RiderProfile, GearConfig
```

## Quick Start

### Basic Speed/Time/Distance

```python
from cycling_utils.mod import calculate_speed, calculate_time, calculate_distance

# Calculate speed from distance and time
speed = calculate_speed(100, 4)  # 100km in 4h = 25 km/h

# Calculate time needed for a distance
time = calculate_time(100, 25)  # 100km at 25km/h = 4 hours

# Calculate distance covered
distance = calculate_distance(25, 4)  # 25km/h for 4h = 100 km
```

### Power Calculations

```python
from cycling_utils.mod import CyclingUtils, RiderProfile

rider = RiderProfile(weight_kg=75, ftp_watts=250)
utils = CyclingUtils(rider=rider)

# Calculate power needed for 30 km/h on flat
power = utils.calculate_power(30, gradient_percent=0)
print(f"Power needed: {power.value:.0f}W")

# Calculate power needed for climbing
power = utils.calculate_power(15, gradient_percent=5)
print(f"Power for 5% climb: {power.value:.0f}W")

# Estimate speed achievable at 200W
speed = utils.estimate_speed_from_power(200)
print(f"Speed at 200W: {speed.value:.1f}km/h")

# Power-to-weight ratio
ratio = utils.calculate_power_to_weight_ratio(300)
print(f"Power/kg: {ratio.value:.2f}W/kg")

# Training zones
zone, name, desc = utils.get_training_zone(275)
print(f"Zone {zone}: {name} - {desc}")
```

### Calorie Calculations

```python
from cycling_utils.mod import CyclingUtils, RiderProfile

utils = CyclingUtils()

# Calculate calories from power
calories = utils.calculate_calories(200, 2)  # 200W for 2 hours
print(f"Calories burned: {calories.value:.0f}kcal")

# Estimate calories from heart rate
rider = RiderProfile(weight_kg=70, age_years=30, gender='male')
utils = CyclingUtils(rider=rider)
calories = utils.estimate_calories_from_hr(150, 1.5)
print(f"Calories from HR: {calories.value:.0f}kcal")
```

### Gear Calculations

```python
from cycling_utils.mod import CyclingUtils, GearConfig

# Default: Compact crank (50/34) with 11-28 cassette
utils = CyclingUtils()

# Calculate gear ratio
ratio = utils.calculate_gear_ratio(50, 11)
print(f"50×11 ratio: {ratio.value:.2f}")

# Calculate development (distance per crank revolution)
dev = utils.calculate_development(50, 14)
print(f"50×14 development: {dev.value:.2f}m/rev")

# Calculate speed from cadence
speed = utils.calculate_speed_from_cadence(90, 50, 14)
print(f"Speed at 90rpm: {speed.value:.1f}km/h")

# Calculate cadence needed for target speed
cadence = utils.calculate_cadence_from_speed(30, 50, 14)
print(f"Cadence for 30km/h: {cadence.value:.0f}rpm")

# Get all gear ratios
all_ratios = utils.get_all_gear_ratios()
for front, rear, ratio in all_ratios[:5]:
    print(f"{front}×{rear}: {ratio:.2f}")

# Custom gear configuration
mtb_config = GearConfig(
    front_teeth=[32],  # Single chainring
    rear_teeth=[10, 12, 14, 16, 18, 21, 24, 28, 32, 36],
    wheel_diameter_mm=622,  # 29er
    tire_width_mm=60  # 2.4" tire
)
utils = CyclingUtils(gear_config=mtb_config)
```

### Climbing Metrics

```python
from cycling_utils.mod import CyclingUtils

utils = CyclingUtils()

# Calculate gradient
gradient = utils.calculate_gradient(10, 1000)  # 10km, 1000m gain
print(f"Gradient: {gradient.value:.1f}%")

# Calculate elevation gain
elevation = utils.calculate_elevation_gain(10, 8)  # 10km at 8%
print(f"Elevation gain: {elevation.value:.0f}m")

# Calculate VAM (climbing speed in m/h)
vam = utils.calculate_vam(1000, 1)  # 1000m in 1h
print(f"VAM: {vam.value:.0f}m/h")

# Climbing difficulty score
difficulty = utils.calculate_climbing_difficulty(14, 1120)
print(f"Difficulty score: {difficulty.value:.1f}")
```

### Training Analysis

```python
from cycling_utils.mod import CyclingUtils, RiderProfile

rider = RiderProfile(weight_kg=75, ftp_watts=250)
utils = CyclingUtils(rider=rider)

# Normalized Power from ride data
power_samples = [200, 210, 180, 250, 230, ...] * 100
np = utils.calculate_np(power_samples)
print(f"Normalized Power: {np.value:.0f}W")

# Training Stress Score
tss = utils.calculate_tss(250, 1.5)  # NP = 250W for 1.5h
print(f"TSS: {tss.value:.0f}")

# Intensity Factor
if_val = utils.calculate_if(250)  # NP / FTP
print(f"Intensity Factor: {if_val.value:.2f}")
```

## Riding Positions

Aerodynamic drag varies by riding position:

| Position | Cd (Drag Coefficient) | Description |
|----------|----------------------|-------------|
| TOPS | 1.15 | Hands on top of handlebars |
| HOODS | 1.00 | Hands on brake hoods (default) |
| DROPS | 0.88 | Hands in drop position |
| AERO | 0.75 | Aerodynamic/Triathlon position |

## Training Zones

| Zone | % FTP | Name | Description |
|------|--------|------|-------------|
| 1 | 0-55% | Active Recovery | Very easy, conversational |
| 2 | 55-75% | Endurance | Comfortable, all-day pace |
| 3 | 75-90% | Tempo | Moderately hard, sustained |
| 4 | 90-105% | Threshold | Hard, race pace |
| 5 | 105-120% | VO2 Max | Very hard, 3-8 min efforts |
| 6 | 120-150% | Anaerobic | Extremely hard, 30s-3min |
| 7 | >150% | Sprint | Maximum effort |

## Surface Rolling Resistance

| Surface | Rolling Resistance (Crr) |
|---------|-------------------------|
| Track | 0.002 |
| Concrete | 0.003 |
| Asphalt | 0.004 (default) |
| Gravel | 0.012 |
| Offroad | 0.020 |
| Grass | 0.025 |
| Sand | 0.050 |

## Power Model

The power calculation uses the cycling power equation:

```
P = P_air + P_roll + P_grav

P_air = 0.5 × ρ × Cd × A × v² × (v + v_wind)
P_roll = m × g × Crr × v
P_grav = m × g × slope × v
```

Where:
- ρ = air density (1.225 kg/m³)
- Cd = drag coefficient
- A = frontal area
- v = speed
- m = total mass (rider + bike)
- g = gravitational acceleration (9.80665 m/s²)
- Crr = rolling resistance coefficient

## API Reference

### Classes

#### `CyclingUtils(rider=None, bike_weight_kg=8.5, gear_config=None)`
Main utility class.

#### `RiderProfile(weight_kg, height_cm=None, age_years=None, gender=None, ftp_watts=None)`
Rider physical profile for personalized calculations.

#### `GearConfig(front_teeth, rear_teeth, crank_length_mm=172.5, wheel_diameter_mm=622, tire_width_mm=25)`
Bicycle gear configuration.

### Methods

| Method | Parameters | Returns |
|--------|------------|---------|
| `calculate_speed` | distance_km, time_hours | Speed in km/h |
| `calculate_time` | distance_km, speed_kmh | Time in hours |
| `calculate_distance` | speed_kmh, time_hours | Distance in km |
| `pace_to_speed` | pace_min_km | Speed in km/h |
| `speed_to_pace` | speed_kmh | Pace in min/km |
| `calculate_power` | speed_kmh, gradient_percent, ... | Power in watts |
| `estimate_speed_from_power` | power_watts, ... | Speed in km/h |
| `calculate_calories` | power_watts, duration_hours | Calories in kcal |
| `estimate_calories_from_hr` | avg_hr, duration_hours | Calories in kcal |
| `calculate_gear_ratio` | front_teeth, rear_teeth | Gear ratio |
| `calculate_development` | front_teeth, rear_teeth | Development in m |
| `calculate_speed_from_cadence` | cadence_rpm, front, rear | Speed in km/h |
| `calculate_cadence_from_speed` | speed_kmh, front, rear | Cadence in rpm |
| `calculate_gradient` | distance_km, elevation_m | Gradient in % |
| `calculate_vam` | elevation_m, time_hours | VAM in m/h |
| `calculate_np` | power_samples | Normalized Power |
| `calculate_tss` | np, duration_hours, ftp | TSS |
| `calculate_if` | np, ftp | Intensity Factor |
| `get_training_zone` | power_watts | Zone number, name, description |

## License

MIT License - Part of AllToolkit project.
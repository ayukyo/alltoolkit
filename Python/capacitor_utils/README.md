# Capacitor Utilities

A comprehensive capacitor calculation and code decoding library for Python with zero external dependencies.

## Features

- **Capacitor Code Decoding**: 3-digit, 4-digit, and R-notation codes
- **Capacitor Code Encoding**: Generate capacitor codes from values
- **Unit Conversion**: pF, nF, uF, mF, F conversions
- **Energy Calculation**: Calculate stored energy in capacitors
- **RC Time Constant**: Calculate tau, charge/discharge times
- **Capacitive Reactance**: Calculate Xc at any frequency
- **Series/Parallel**: Calculate equivalent capacitance
- **Voltage Divider**: Capacitive divider calculations
- **Charge/Discharge Curves**: Calculate voltage over time
- **E-Series Standards**: E3, E6, E12, E24 standard values
- **Supercapacitor**: Backup time and energy density calculations
- **Ripple Current**: Power loss and current ratings
- **Lifetime Estimation**: Temperature and voltage effects
- **Color Band Decoding**: Vintage/ceramic capacitor colors

## Installation

No external dependencies required. Uses only Python standard library.

```python
from capacitor_utils import decode_capacitor_code, encode_capacitor_code
```

## Quick Start

### Decode Capacitor Codes

```python
# 3-digit code: 104 = 10 * 10^4 pF = 100nF
result = decode_capacitor_code("104")
print(result['capacitance_str'])  # "100 nF"

# 4-digit code: 4753 = 475 * 10^3 pF = 475nF
result = decode_capacitor_code("4753")
print(result['capacitance_str'])  # "475 nF"

# R-notation: 4R7 = 4.7pF
result = decode_capacitor_code("4R7")
print(result['capacitance_str'])  # "4.7 pF"

# With unit: 100n
result = decode_capacitor_code("100n")
print(result['capacitance_str'])  # "100 nF"
```

### Encode Capacitance to Codes

```python
# Encode 100nF
code = encode_capacitor_code(1e-7)  # "104"

# Encode 10uF
code = encode_capacitor_code(1e-5)  # "106"

# Encode 4.7pF with R-notation
code = encode_capacitor_code(4.7e-12, "R-notation")  # "4R7"
```

### Unit Conversion

```python
# Convert 1uF to nF
value = convert_capacitance(1, "uF", "nF")  # 1000.0

# Convert 1000pF to nF
value = convert_capacitance(1000, "pF", "nF")  # 1.0

# Format capacitance
formatted = format_capacitance(1e-6)  # "1 uF"
```

### RC Time Constant

```python
# 1kΩ resistor, 1uF capacitor
result = rc_time_constant(1000, 1e-6)
print(result['tau_ms'])        # 1.0 ms
print(result['five_tau_ms'])   # 5.0 ms (99.3% charged)
```

### Capacitive Reactance

```python
# 1uF at 1kHz
result = capacitor_reactance(1e-6, 1000)
print(result['reactance_ohms'])  # ~159 Ω

# 100uF at 50Hz ( mains frequency)
result = capacitor_reactance(1e-4, 50)
print(result['reactance_ohms'])  # ~32 Ω
```

### Energy Storage

```python
# 1000uF at 5V
result = capacitor_energy(1e-3, 5)
print(result['energy_joules'])     # 0.0125 J
print(result['energy_watthours'])  # 3.47 µWh
```

### Series and Parallel

```python
# Parallel: C_total = C1 + C2 + ...
result = parallel_capacitance([1e-6, 2e-6, 3e-6])
print(result)  # 6e-6 (6uF)

# Series: 1/C_total = 1/C1 + 1/C2 + ...
result = series_capacitance([1e-6, 1e-6])
print(result)  # 5e-7 (0.5uF)
```

### Voltage Divider

```python
# 1uF + 1uF divider with 10V input
result = capacitor_divider_voltage(1e-6, 1e-6, 10)
print(result['vout'])  # 5V
```

### Charge/Discharge Curves

```python
# Charging: 1uF, 1kΩ, 0V initial, 5V target, after 1ms
v = capacitor_charge_voltage(1e-6, 1000, 0, 5, 0.001)
print(v)  # ~3.16V (63.2% of target)

# Discharging: 1uF, 1kΩ, 5V initial, after 1ms
v = capacitor_discharge_voltage(1e-6, 1000, 5, 0.001)
print(v)  # ~1.84V (36.8% of initial)

# Time to charge to 99.3%
t = time_to_charge(1e-6, 1000, 99.3)
print(t)  # 0.005 seconds (5 tau)
```

### E-Series Standard Values

```python
# Get E12 series values
e12 = get_capacitor_series("E12")  # [10, 12, 15, 18, 22, ...]

# Find nearest standard value
result = find_nearest_standard(8.5e-6, "E12")
print(result['nearest_str'])      # "8.2 uF"
print(result['error_percent'])    # 3.5%
```

### Supercapacitor Backup

```python
# 1F supercap, 5V to 3V cutoff, 1mA load
result = supercap_backup_time(1.0, 5.0, 3.0, 0.001)
print(result['time_minutes'])  # ~33 minutes

# Energy density
result = supercap_energy_density(100, 2.7, weight_kg=0.05)
print(result['specific_energy_wh_kg'])  # ~2 Wh/kg
```

### Ripple Current

```python
# 100uF, 100kHz, 0.1Ω ESR
result = ripple_current_rating(100e-6, 100000, 0.1)
print(result['max_ripple_current_arms'])  # ~2.2A

# Power loss from ripple
result = capacitor_power_loss(100e-6, 0.5, 100000, 0.1)
print(result['power_loss_w'])  # Power dissipated in ESR
```

### Lifetime Estimation

```python
# 2000h @ 105°C rated, operating at 65°C, 80% voltage
result = capacitor_lifetime(2000, 105, 65, 0.8)
print(result['estimated_hours'])   # Much longer than 2000h
print(result['estimated_years'])   # Lifetime in years
```

### Color Band Decoding (Vintage Capacitors)

```python
# Brown-Black-Orange = 10nF
result = decode_capacitor_colors(['brown', 'black', 'orange'])
print(result['capacitance_str'])  # "10 nF"

# With tolerance: Brown-Black-Red-White = 1nF, 10%
result = decode_capacitor_colors(['brown', 'black', 'red', 'white'])
print(result['tolerance_percent'])  # 10.0
```

## Capacitor Code Reference

### 3-Digit Code
```
[Significant][Significant][Multiplier as power of 10]
Example: 104 = 10 × 10^4 pF = 100nF = 0.1µF
Example: 103 = 10 × 10^3 pF = 10nF
Example: 475 = 47 × 10^5 pF = 4.7µF
```

### 4-Digit Code
```
[Significant][Significant][Significant][Multiplier]
Example: 1000 = 100 × 10^0 pF = 100pF
Example: 4753 = 475 × 10^3 pF = 475nF
```

### R-Notation (Small Values)
```
[R marks decimal point, values in pF]
Example: 4R7 = 4.7pF
Example: R47 = 0.47pF
Example: 2R2 = 2.2pF
```

## Color Band Reference

| Color    | Value | Multiplier | Tolerance | Voltage |
|----------|-------|------------|-----------|---------|
| Black    | 0     | 1          | 20%       | -       |
| Brown    | 1     | 10         | 1%        | 100V    |
| Red      | 2     | 100        | 2%        | 250V    |
| Orange   | 3     | 1000       | -         | 300V    |
| Yellow   | 4     | 10000      | -         | 400V    |
| Green    | 5     | 100000     | 0.5%      | 500V    |
| Blue     | 6     | -          | -         | 600V    |
| Violet   | 7     | -          | -         | 700V    |
| Gray     | 8     | -          | -         | 800V    |
| White    | 9     | -          | 10%       | 900V    |
| Gold     | -     | -          | 5%        | -       |
| Silver   | -     | -          | 10%       | -       |

## E-Series Standard Values

| Series | Values |
|--------|--------|
| E3     | 10, 22, 47 |
| E6     | 10, 15, 22, 33, 47, 68 |
| E12    | 10, 12, 15, 18, 22, 27, 33, 39, 47, 56, 68, 82 |
| E24    | 10, 11, 12, 13, 15, 16, 18, 20, 22, 24, 27, 30, 33, 36, 39, 43, 47, 51, 56, 62, 68, 75, 82, 91 |

## API Reference

### Code Functions
- `decode_capacitor_code(code)` - Decode 3/4-digit, R-notation, unit codes
- `encode_capacitor_code(value, code_type)` - Encode to capacitor code
- `decode_capacitor_colors(colors)` - Decode color bands

### Conversion Functions
- `convert_capacitance(value, from_unit, to_unit)` - Unit conversion
- `format_capacitance(farads)` - Format with appropriate unit
- `parse_capacitance_string(string)` - Parse to farads

### Electrical Functions
- `capacitor_energy(capacitance, voltage)` - Calculate stored energy
- `capacitor_charge(capacitance, voltage)` - Calculate charge
- `rc_time_constant(resistance, capacitance)` - Calculate tau
- `capacitor_reactance(capacitance, frequency)` - Calculate Xc
- `capacitive_impedance(capacitance, frequency)` - Complex impedance

### Series/Parallel Functions
- `parallel_capacitance(capacitances)` - Parallel equivalent
- `series_capacitance(capacitances)` - Series equivalent
- `capacitor_divider_voltage(c1, c2, vin)` - Voltage divider

### Charge/Discharge Functions
- `capacitor_charge_voltage(C, R, V_initial, V_target, time)` - Charging
- `capacitor_discharge_voltage(C, R, V_initial, time)` - Discharging
- `time_to_charge(C, R, percent)` - Time to reach charge level

### E-Series Functions
- `get_capacitor_series(series)` - Get standard values
- `find_nearest_standard(value, series)` - Find closest standard value

### Supercapacitor Functions
- `supercap_backup_time(capacitance, V_initial, V_cutoff, current)` - Backup time
- `supercap_energy_density(capacitance, voltage, weight, volume)` - Energy density

### Ripple Current Functions
- `ripple_current_rating(C, frequency, ESR, max_temp, thermal_R)` - Current rating
- `capacitor_power_loss(C, ripple_V, frequency, ESR)` - Power dissipation

### Lifetime Functions
- `capacitor_lifetime(hours, rated_temp, operating_temp, voltage_ratio)` - Estimate life

### Utility Functions
- `is_valid_capacitor_code(code)` - Validate code
- `get_capacitor_info(capacitance)` - Get value information

## Examples

See `examples/usage_examples.py` for comprehensive usage examples.

## License

MIT License - Part of AllToolkit
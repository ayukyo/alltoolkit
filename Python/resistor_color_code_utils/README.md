# Resistor Color Code Utilities

A comprehensive resistor color code calculator for Python with zero external dependencies.

## Features

- **Color Band Decoding**: Convert color bands to resistance value (3, 4, 5, 6 bands)
- **Color Band Encoding**: Convert resistance value to color bands
- **SMD Resistor Codes**: Decode/encode 3-digit, 4-digit, and R-notation codes
- **EIA-96 Codes**: Support for precision SMD resistor codes
- **Standard E-Series**: E6, E12, E24, E96, E192 standard values
- **Nearest Standard Value Finder**: Find closest standard resistor value
- **Circuit Calculations**: Parallel, series, voltage divider, LED resistor
- **Temperature Coefficient**: Support for 6-band resistors with tempco

## Installation

No external dependencies required. Uses only Python standard library.

```python
from resistor_color_code_utils import decode_4band, encode_4band
```

## Quick Start

### Decode Color Bands

```python
# 4-band resistor: Brown-Black-Red-Gold = 1kΩ ±5%
result = decode_4band(['brown', 'black', 'red', 'gold'])
print(result['resistance_str'])  # "1 kΩ"
print(result['tolerance'])       # 5.0

# Automatic detection
result = decode_resistor(['red', 'violet', 'yellow', 'gold'])  # 4-band
print(result['bands'])           # 4
print(result['resistance'])      # 270000.0
```

### Encode Resistance to Colors

```python
# Encode 4.7kΩ ±5% to color bands
result = encode_4band(4700, 5)
print(result['colors'])  # ['yellow', 'violet', 'red', 'gold']

# High precision: 4.7kΩ ±1%
result = encode_5band(4700, 1)
print(result['colors'])  # ['yellow', 'violet', 'black', 'brown', 'brown']
```

### SMD Resistor Codes

```python
# Decode SMD codes
result = decode_smd('103')   # 10kΩ
result = decode_smd('4R7')   # 4.7Ω
result = decode_smd('4701')  # 4.7kΩ (4-digit)

# Encode to SMD code
result = encode_smd(10000)   # '103'
result = encode_smd(4.7)     # '4R7'
```

### Circuit Calculations

```python
# Parallel resistors
r_parallel = parallel_resistance([100, 100])  # 50Ω

# Series resistors  
r_series = series_resistance([100, 200])      # 300Ω

# Voltage divider
vout = voltage_divider(10000, 10000, 5)       # 2.5V

# LED resistor (5V supply, 2V LED, 20mA)
r_led = led_resistor(5, 2, 0.02)              # 150Ω
```

### E-Series Values

```python
# Get standard E-series values
e12_values = get_e_series('E12')  # [10, 12, 15, 18, 22, ...]

# Find nearest standard value
nearest = find_nearest_standard(5000, 'E12')
print(nearest['nearest'])      # 4700.0
print(nearest['error_percent']) # 6.0

# Check if value is standard
is_standard_value(4700, 'E12')  # True
is_standard_value(4800, 'E12')  # False
```

## Color Band Reference

| Color    | Value | Multiplier | Tolerance | TempCo (ppm/°C) |
|----------|-------|------------|-----------|-----------------|
| Black    | 0     | 1          | -         | 250             |
| Brown    | 1     | 10         | ±1%       | 100             |
| Red      | 2     | 100        | ±2%       | 50              |
| Orange   | 3     | 1,000      | -         | 15              |
| Yellow   | 4     | 10,000     | -         | 25              |
| Green    | 5     | 100,000    | ±0.5%     | 20              |
| Blue     | 6     | 1,000,000  | ±0.25%    | 10              |
| Violet   | 7     | 10,000,000 | ±0.1%     | 5               |
| Gray     | 8     | -          | ±0.05%    | 1               |
| White    | 9     | -          | -         | -               |
| Gold     | -     | 0.1        | ±5%       | -               |
| Silver   | -     | 0.01       | ±10%      | -               |

## Band Configuration

### 3-Band (20% tolerance default)
```
[Significant][Significant][Multiplier]
Example: Brown-Black-Red = 1kΩ ±20%
```

### 4-Band (Most common)
```
[Significant][Significant][Multiplier][Tolerance]
Example: Brown-Black-Red-Gold = 1kΩ ±5%
```

### 5-Band (Higher precision)
```
[Significant][Significant][Significant][Multiplier][Tolerance]
Example: Brown-Black-Black-Red-Brown = 10kΩ ±1%
```

### 6-Band (Precision + Temperature coefficient)
```
[Significant][Significant][Significant][Multiplier][Tolerance][TempCo]
Example: Red-Red-Black-Orange-Brown-Red = 220kΩ ±1% 50ppm/°C
```

## SMD Code Formats

### 3-Digit Code
```
[Significant digits][Multiplier as power of 10]
Example: 103 = 10 × 10³ = 10kΩ
```

### 4-Digit Code (Higher precision)
```
[Significant digits][Multiplier as power of 10]
Example: 4701 = 470 × 10¹ = 4.7kΩ
```

### R-Notation (Small values)
```
[R marks decimal point]
Example: 4R7 = 4.7Ω, R47 = 0.47Ω
```

### EIA-96 Code (1% precision)
```
[2-digit code][Multiplier letter]
Multiplier letters: A=1, B=10, C=100, D=1000, ...
Example: 01C = 100 × 100 = 10kΩ
```

## API Reference

### Decoding Functions

- `decode_3band(colors)` - Decode 3-band resistor
- `decode_4band(colors)` - Decode 4-band resistor
- `decode_5band(colors)` - Decode 5-band resistor
- `decode_6band(colors)` - Decode 6-band resistor
- `decode_resistor(colors)` - Auto-detect and decode

### Encoding Functions

- `encode_4band(resistance, tolerance)` - Encode to 4-band
- `encode_5band(resistance, tolerance)` - Encode to 5-band
- `encode_6band(resistance, tolerance, tempco)` - Encode to 6-band

### SMD Functions

- `decode_smd(code)` - Decode SMD resistor code
- `encode_smd(resistance, code_type)` - Encode to SMD code

### E-Series Functions

- `get_e_series(series)` - Get standard E-series values
- `find_nearest_standard(value, series)` - Find nearest standard value
- `is_standard_value(value, series, tolerance)` - Check if standard

### Circuit Functions

- `parallel_resistance(resistances)` - Calculate parallel equivalent
- `series_resistance(resistances)` - Calculate series equivalent
- `voltage_divider(r1, r2, vin)` - Calculate divider output
- `led_resistor(supply_v, led_v, current)` - Calculate LED resistor

### Utility Functions

- `is_valid_color(color)` - Check if color is valid
- `get_color_info(color)` - Get color band properties

## Examples

See `examples/usage_examples.py` for comprehensive usage examples.

## License

MIT License - Part of AllToolkit
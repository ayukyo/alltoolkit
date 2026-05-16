# Unit Converter Utils

A comprehensive unit conversion library for JavaScript with zero external dependencies.

## Features

- **11 Unit Categories**: Temperature, Length, Weight, Volume, Area, Speed, Time, Data, Pressure, Angle, Fuel Consumption
- **Zero Dependencies**: Pure JavaScript implementation
- **Comprehensive Aliases**: Supports both full names and short aliases (e.g., `meter`, `m`, `kilometer`, `km`)
- **Generic Convert**: Auto-detects unit categories for easy conversion
- **Utility Functions**: Format numbers, check conversions, list available units

## Installation

```bash
# Copy the module to your project
cp -r unit_converter_utils your-project/utils/
```

## Quick Start

```javascript
const { convert, convertTemperature, convertLength } = require('./unit_converter_utils/mod.js');

// Generic convert (auto-detects category)
convert(100, 'celsius', 'fahrenheit');  // 212
convert(1, 'km', 'mile');                // 0.621371
convert(1, 'kg', 'lb');                  // 2.20462

// Specific converters
convertTemperature(0, 'C', 'F');         // 32
convertLength(1, 'meter', 'foot');       // 3.28084
convertWeight(1, 'pound', 'kg');         // 0.453592
```

## Supported Units

### Temperature
| Full Name | Alias |
|-----------|-------|
| celsius | C |
| fahrenheit | F |
| kelvin | K |
| rankine | R |

### Length
| Full Name | Alias |
|-----------|-------|
| nanometer | nm |
| micrometer | um |
| millimeter | mm |
| centimeter | cm |
| meter | m |
| kilometer | km |
| inch | in |
| foot | ft |
| yard | yd |
| mile | mi |
| nautical_mile | nmi |
| astronomical_unit | au |
| light_year | ly |
| parsec | pc |

### Weight/Mass
| Full Name | Alias |
|-----------|-------|
| milligram | mg |
| gram | g |
| kilogram | kg |
| metric_ton | t |
| ounce | oz |
| pound | lb, lbs |
| stone | st |

### Volume
| Full Name | Alias |
|-----------|-------|
| milliliter | ml |
| liter | l |
| cubic_meter | m3 |
| fluid_ounce_us | floz_us |
| cup_us | cup |
| pint_us | pt_us |
| quart_us | qt_us |
| gallon_us | gal_us |
| tablespoon | tbsp |
| teaspoon | tsp |

### Area
| Full Name | Alias |
|-----------|-------|
| square_meter | m2 |
| square_kilometer | km2 |
| hectare | ha |
| square_inch | in2 |
| square_foot | ft2 |
| square_yard | yd2 |
| acre | - |

### Speed
| Full Name | Alias |
|-----------|-------|
| meters_per_second | mps, m_s |
| kilometers_per_hour | kmh, km_h |
| miles_per_hour | mph |
| feet_per_second | fps, ft_s |
| knots | kn |
| mach | - |
| speed_of_light | c |

### Time
| Full Name | Alias |
|-----------|-------|
| millisecond | ms |
| second | s, sec |
| minute | min |
| hour | h, hr |
| day | d |
| week | w |
| month | mo |
| year | y, yr |
| decade | - |
| century | - |

### Data
| Full Name | Alias |
|-----------|-------|
| byte | b |
| kibibyte | kib |
| mebibyte | mib |
| gibibyte | gib |
| tebibyte | tib |
| kilobyte | kb |
| megabyte | mb |
| gigabyte | gb |
| terabyte | tb |
| bit | - |
| kilobit | - |
| megabit | - |

### Pressure
| Full Name | Alias |
|-----------|-------|
| pascal | pa |
| kilopascal | kpa |
| bar | - |
| millibar | mbar |
| psi | - |
| atmosphere | atm |
| torr | - |
| mmhg | - |

### Angle
| Full Name | Alias |
|-----------|-------|
| degree | deg, ° |
| radian | rad |
| gradian | gon |
| arcminute | arcmin, ' |
| arcsecond | arcsec, " |

### Fuel Consumption
| Full Name | Alias |
|-----------|-------|
| km_per_liter | kml, km_l |
| liters_per_100km | l_100km |
| miles_per_gallon_us | mpg, mpg_us |
| miles_per_gallon_uk | mpg_uk |

## API Reference

### Specific Converters

Each category has its own dedicated function:

```javascript
convertTemperature(value, from, to)
convertLength(value, from, to)
convertWeight(value, from, to)
convertVolume(value, from, to)
convertArea(value, from, to)
convertSpeed(value, from, to)
convertTime(value, from, to)
convertData(value, from, to)
convertPressure(value, from, to)
convertAngle(value, from, to)
convertFuel(value, from, to)
```

### Generic Converter

```javascript
convert(value, from, to)
```

Auto-detects the category and performs the conversion. Throws an error if units are incompatible.

### Utility Functions

```javascript
// Get the category of a unit
getUnitCategory('meter')  // 'length'
getUnitCategory('kg')     // 'weight'

// Get all units in a category
getAvailableUnits('temperature')  // ['celsius', 'fahrenheit', ...]

// Get all categories
getCategories()  // ['temperature', 'length', ...]

// Check if conversion is valid
canConvert('meter', 'foot')     // true
canConvert('meter', 'kilogram') // false

// Format numbers nicely
formatNumber(3.14159, 2)  // '3.14'
formatNumber(10000000000) // '1.00e+10' (scientific notation)
```

## Error Handling

All functions throw descriptive errors for invalid inputs:

```javascript
convert(1, 'meter', 'unknown')  // Error: Unknown length unit: unknown
convert(1, 'meter', 'kilogram') // Error: Cannot convert between length and weight
```

## Testing

```bash
node unit_converter_utils_test.js
```

## License

MIT
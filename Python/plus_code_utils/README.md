# Plus Code (Open Location Code) Utilities

Plus Code (also known as Open Location Code) is a geocoding system developed by Google that encodes latitude and longitude into a short alphanumeric string. It provides a universal addressing solution for locations without traditional street addresses.

## Features

- **Encode** coordinates to Plus Code with configurable precision
- **Decode** Plus Code back to geographic coordinates
- **Shorten** codes using reference locations for local use
- **Recover** full codes from shortened codes
- **Validate** and clean Plus Code strings
- **Calculate** distances between codes
- **Find** neighboring code areas

## Usage Examples

### Basic Encoding

```python
from plus_code_utils.mod import encode

# Encode coordinates to Plus Code
result = encode(47.365590, 8.524030)
print(result.full_code)  # e.g., "8FVC2222+"
```

### Different Precision Levels

```python
# 10-digit code (~50m precision)
result = encode(47.365590, 8.524030, 10)

# 12-digit code (~5m precision)
result = encode(47.365590, 8.524030, 12)

# 6-digit code (~5km precision)
result = encode(47.365590, 8.524030, 6)
```

### Decoding

```python
from plus_code_utils.mod import decode

area = decode("8FVC2222+")
print(f"Center: ({area.latitude_center}, {area.longitude_center})")
print(f"Bounds: [{area.latitude_lo}, {area.longitude_lo}] to [{area.latitude_hi}, {area.longitude_hi}]")
```

### Shortening for Local Use

```python
from plus_code_utils.mod import shorten

full_code = "8FVC2222+22"

# Shorten using local reference
short_code = shorten(full_code, 47.37, 8.52)
print(short_code)  # e.g., "2222+22"
```

### Recovery from Short Code

```python
from plus_code_utils.mod import recover_nearest

short_code = "2222+22"
full_code = recover_nearest(short_code, 47.37, 8.52)
print(full_code)  # e.g., "8FVC2222+22"
```

### Validation

```python
from plus_code_utils.mod import is_valid_code, clean_code

# Validate
is_valid_code("8FVC2222+")  # True
is_valid_code("invalid")     # False

# Clean user input
clean_code("  8fvc-2222+  ")  # "8FVC2222+"
```

## Code Precision

| Code Length | Area Size | Use Case |
|-------------|-----------|----------|
| 4 digits | ~100 km | Country/Region level |
| 6 digits | ~5 km | City/Town level |
| 8 digits | ~500 m | Neighborhood level |
| 10 digits | ~50 m | Building level |
| 12 digits | ~5 m | Entrance/Door level |
| 14 digits | ~1 m | Specific point |

## Common Use Cases

1. **Addressing remote locations**: Provide addresses for areas without street names
2. **Delivery services**: Precise location for package delivery
3. **Emergency services**: Communicate exact location to responders
4. **Event venues**: Share precise meeting locations
5. **Travel guides**: Mark specific points of interest

## Implementation Notes

- Pure Python implementation with zero external dependencies
- Works worldwide, including polar regions
- Handles longitude wrapping automatically
- Supports OCR-friendly character set (no ambiguous characters like I, O)

## References

- [Google Open Location Code Specification](https://github.com/google/open-location-code)
- [Plus Codes Official Website](https://plus.codes/)
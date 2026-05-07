# Verhoeff Algorithm Utilities

Verhoeff check digit algorithm implementation - a powerful checksum formula that detects all single-digit errors and all transposition errors in numeric identifiers.

## Features

- **Complete error detection**: Catches ALL single-digit substitution errors and ALL adjacent transposition errors
- **Zero dependencies**: Pure Python implementation
- **Comprehensive API**: Validation, generation, error analysis, batch operations
- **Educational**: Detailed explanations and step-by-step computation visualization

## Installation

```python
from verhoeff_utils import (
    compute_check_digit,
    validate,
    append_check_digit,
    analyze_error,
)
```

## Quick Start

```python
# Compute check digit
check = compute_check_digit("12345")  # Returns 1

# Append check digit
full = append_check_digit("12345")    # Returns "123451"

# Validate
is_valid = validate("123451")         # Returns True
is_valid = validate("123450")         # Returns False

# Error analysis
analysis = analyze_error("123451", "123351")
# Returns: {'error_type': 'single_substitution', 'position': 3, ...}
```

## Why Verhoeff?

Verhoeff is superior to Luhn algorithm:

| Error Type | Luhn | Verhoeff |
|------------|------|----------|
| Single digit substitution | 90% | **100%** |
| Adjacent transposition | ~97% | **100%** |
| Twin errors (aa→bb) | ~90% | ~95% |
| Jump transpositions | ~80% | ~94% |

## API Reference

### Core Functions

- `compute_check_digit(number)` - Compute check digit for a string
- `compute_check_digit_int(number)` - Compute check digit for an integer
- `validate(number)` - Validate a string with check digit
- `validate_int(number)` - Validate an integer with check digit
- `append_check_digit(number)` - Append check digit to string
- `append_check_digit_int(number)` - Append check digit to integer

### Error Detection

- `detect_single_error(original, modified)` - Detect single substitution
- `detect_transposition_error(original, modified)` - Detect transposition
- `analyze_error(original, modified)` - Comprehensive error analysis

### Batch Operations

- `validate_batch(numbers)` - Validate multiple numbers
- `generate_with_check_digits(numbers)` - Generate multiple with check digits

### Educational

- `explain_algorithm()` - Algorithm explanation
- `show_computation_steps(number)` - Step-by-step computation

## Mathematical Background

The Verhoeff algorithm uses:
- **Dihedral group D5**: Symmetry group of a regular pentagon (10 elements)
- **Position-dependent permutations**: Different permutations for each digit position
- **Group multiplication**: Combines elements using D5 operation table

## License

MIT License - Part of AllToolkit
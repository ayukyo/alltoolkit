# Abbreviation & Acronym Utilities

A comprehensive Python utility module for handling abbreviations and acronyms with zero external dependencies.

## Features

- **Abbreviation Expansion**: Expand common abbreviations (NASA, CEO, API, etc.)
- **Acronym Detection**: Detect abbreviations/acronyms in text
- **Abbreviation Creation**: Create abbreviations from text (acronym, truncation, hybrid styles)
- **Information Retrieval**: Get detailed info about abbreviations (category, type, etc.)
- **Location Codes**: Handle US state and country code abbreviations
- **Text Processing**: Expand all abbreviations in text, with optional preservation
- **Custom Abbreviations**: Add your own abbreviations dynamically
- **Statistics**: Count abbreviation occurrences in text

## Installation

No external dependencies required. Pure Python standard library implementation.

```python
from abbreviation_utils import expand, abbreviate, detect
```

## Quick Start

### Expand Abbreviations

```python
from abbreviation_utils import expand, expand_text

# Expand single abbreviation
expand("NASA")  # "National Aeronautics and Space Administration"
expand("CEO")   # "Chief Executive Officer"
expand("API")   # "Application Programming Interface"

# Expand in text
expand_text("NASA launched a rocket.")
# "National Aeronautics and Space Administration launched a rocket."

# Keep original abbreviation
expand_text("NASA announced", keep_original=True)
# "National Aeronautics and Space Administration (NASA) announced"
```

### Create Abbreviations

```python
from abbreviation_utils import abbreviate

# Acronym style (first letters)
abbreviate("International Business Machines")
# "IBM"

abbreviate("Department of Motor Vehicles")
# "DMV"

# Truncation style
abbreviate("Department", style="truncation")
# "Dept."

# With max length
abbreviate("Very Long Organization Name", max_length=4)
# "VLON"
```

### Detect Abbreviations

```python
from abbreviation_utils import detect, get_info

# Detect in text
detected = detect("NASA and FBI work together")
for info in detected:
    print(f"{info.abbreviation}: {info.expansion}")
    print(f"Category: {info.category}")
    print(f"Is Acronym: {info.is_acronym}")

# Get specific info
info = get_info("NASA")
print(info.abbreviation)    # "NASA"
print(info.expansion)       # "National Aeronautics and Space Administration"
print(info.is_acronym)      # True
print(info.is_initialism)   # False
print(info.category)        # "organization"
```

### State & Country Codes

```python
from abbreviation_utils import expand_state, abbreviate_state, expand_country, abbreviate_country

# US States
expand_state("CA")          # "California"
abbreviate_state("Texas")   # "TX"

# Countries
expand_country("US")        # "United States"
abbreviate_country("Japan") # "JP"
```

### Categories

```python
from abbreviation_utils import get_categories, get_all_by_category

# Get all categories
categories = get_categories()
# ['academic', 'business', 'common', 'government', 'location', 'medical', 'organization', 'technology']

# Get by category
tech_abbrevs = get_all_by_category("technology")
# {'API': 'Application Programming Interface', 'URL': '...', ...}
```

### Custom Abbreviations

```python
from abbreviation_utils import add_custom, expand

# Add your own
add_custom("MYCO", "My Custom Organization", "custom")
expand("MYCO")  # "My Custom Organization"
```

### Count Abbreviations

```python
from abbreviation_utils import count_abbreviations

counts = count_abbreviations("NASA and NASA work with FBI")
# {'NASA': 2, 'FBI': 1}
```

## Supported Categories

- **Organization**: NASA, FBI, UN, NATO, etc.
- **Technology**: API, URL, HTTP, CPU, RAM, etc.
- **Business**: CEO, CFO, ROI, B2B, etc.
- **Medical**: MRI, ICU, DNA, CPR, etc.
- **Academic**: PhD, MBA, GPA, SAT, etc.
- **Government**: US, UK, EPA, DOD, etc.
- **Common**: etc, e.g., i.e., approx, etc.
- **Location**: State codes (CA, NY), Country codes (US, CN)

## Acronym vs Initialism

- **Acronym**: Pronounced as a word (NASA, NATO, RAM)
- **Initialism**: Pronounced letter-by-letter (FBI, CIA, URL)

The module automatically detects which type an abbreviation is.

## API Reference

### Functions

| Function | Description |
|----------|-------------|
| `expand(abbreviation)` | Expand abbreviation to full form |
| `expand_text(text, keep_original)` | Expand all abbreviations in text |
| `abbreviate(text, max_length, style)` | Create abbreviation from text |
| `detect(text)` | Detect abbreviations in text |
| `get_info(abbreviation)` | Get detailed info about abbreviation |
| `is_abbreviation(text)` | Check if text is known abbreviation |
| `find_abbreviation_for(expansion)` | Find abbreviation for expansion |
| `expand_state(code)` | Expand US state code |
| `abbreviate_state(name)` | Get US state abbreviation |
| `expand_country(code)` | Expand country code |
| `abbreviate_country(name)` | Get country abbreviation |
| `get_categories()` | Get all available categories |
| `get_all_by_category(category)` | Get abbreviations by category |
| `add_custom(abbrev, expansion, category)` | Add custom abbreviation |
| `count_abbreviations(text)` | Count abbreviation occurrences |

### Classes

| Class | Description |
|-------|-------------|
| `AbbreviationUtils` | Main utility class with all methods |
| `AbbreviationInfo` | Data class for abbreviation information |

## License

MIT License - Part of AllToolkit project.
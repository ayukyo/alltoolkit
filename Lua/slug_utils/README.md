# slug_utils - URL Friendly String Generator

A lightweight, zero-dependency Lua module for converting strings into URL-friendly slugs.

## Features

- Unicode to ASCII transliteration (Latin, Cyrillic, Greek, German)
- Special character handling
- Configurable separator
- Case conversion options
- Duplicate separator removal
- Leading/trailing separator trimming
- Slug validation
- Slug parsing
- Unique slug generation
- Slug truncation

## Installation

Copy `slug.lua` to your project and require it:

```lua
local slug_utils = require("slug")
```

## Basic Usage

```lua
local slug_utils = require("slug")

-- Basic slug generation
print(slug_utils.slug("Hello World"))           -- "hello-world"
print(slug_utils.slug("Café"))                   -- "cafe"
print(slug_utils.slug("Привет мир"))             -- "privet-mir"

-- Custom separator
print(slug_utils.slug("Hello World", { separator = "_" }))  -- "hello_world"
print(slug_utils.slug_with_separator("Hello World", "."))   -- "hello.world"

-- Preserve case
print(slug_utils.slug_preserve_case("Hello World"))  -- "Hello-World"

-- Underscore separator shortcut
print(slug_utils.slug_underscore("Hello World"))     -- "hello_world"
```

## Advanced Usage

### Slug Validation

```lua
local slug_utils = require("slug")

print(slug_utils.is_valid_slug("hello-world"))       -- true
print(slug_utils.is_valid_slug("Hello World"))       -- false (contains space)
print(slug_utils.is_valid_slug("-hello-world"))      -- false (leading separator)
print(slug_utils.is_valid_slug("hello--world"))      -- false (consecutive separators)

-- With custom separator
print(slug_utils.is_valid_slug("hello_world", "_"))  -- true
```

### Slug Parsing

```lua
local slug_utils = require("slug")

local words = slug_utils.parse_slug("hello-world-test")
-- words = {"hello", "world", "test"}

-- With custom separator
local words2 = slug_utils.parse_slug("hello_world_test", "_")
-- words2 = {"hello", "world", "test"}
```

### Unique Slugs

```lua
local slug_utils = require("slug")

-- With custom suffix
print(slug_utils.slug_unique("Hello World", "123"))  -- "hello-world-123"

-- With random suffix
print(slug_utils.slug_unique("Hello World"))         -- "hello-world-8472" (random)
```

### Slug Truncation

```lua
local slug_utils = require("slug")

print(slug_utils.truncate_slug("hello-world-test", 10))  -- "hello"
print(slug_utils.truncate_slug("hello", 10))              -- "hello" (unchanged)
```

## API Reference

### `slug(str, options)`

Convert a string to a URL-friendly slug.

**Parameters:**
- `str` (string): Input string
- `options` (table, optional):
  - `separator` (string): Word separator (default: "-")
  - `lowercase` (boolean): Convert to lowercase (default: true)
  - `trim` (boolean): Trim leading/trailing separators (default: true)
  - `transliterate` (boolean): Transliterate Unicode (default: true)

**Returns:** string - URL-friendly slug

### `slug_with_separator(str, separator)`

Generate a slug with custom separator.

### `slug_preserve_case(str)`

Generate a slug preserving original case.

### `slug_underscore(str)`

Generate a slug with underscore separator.

### `is_valid_slug(str, separator)`

Check if a string is a valid slug.

### `parse_slug(slug, separator)`

Parse a slug into words.

### `slug_unique(str, suffix, options)`

Generate a slug with a unique suffix.

### `truncate_slug(slug, max_length, separator)`

Truncate a slug to maximum length (preserves word boundaries).

## Transliteration Support

Supports transliteration from:
- Latin extended (à, é, ñ, etc.)
- German umlauts (ä, ö, ü, ß)
- Cyrillic (Russian)
- Greek

## Zero Dependencies

This module uses only Lua standard library functions:
- `string` module
- `table` module
- `math` module (for random suffix)

## Running Tests

```bash
cd Lua/slug_utils
lua test_slug.lua
```

## License

MIT
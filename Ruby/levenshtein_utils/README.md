# Levenshtein Distance Utilities

A pure Ruby implementation of string similarity algorithms with zero external dependencies.

## Features

- **Classic Levenshtein distance** - Minimum edit operations between strings
- **Damerau-Levenshtein** - Includes transposition detection
- **Similarity scores** - Normalized 0.0 to 1.0 values
- **Fuzzy matching** - Find closest matches with thresholds
- **Edit operations** - Track how to transform one string to another
- **Jaro-Winkler** - Better for short strings and names
- **Hamming distance** - For equal-length strings
- **Custom costs** - Weight insert/delete/substitute differently
- **Case sensitivity** - Optional case-insensitive comparison

## Usage

```ruby
require_relative 'levenshtein'

# Basic distance
LevenshteinUtils.distance("kitten", "sitting")  #=> 3

# Similarity score
LevenshteinUtils.similarity("hello", "hallo")   #=> 0.8

# Damerau-Levenshtein (catches transpositions)
LevenshteinUtils.damerau_distance("teh", "the") #=> 1

# Find closest match (spell checker)
candidates = ["apple", "banana", "cherry"]
LevenshteinUtils.closest_match("aple", candidates)
#=> [{string: "apple", distance: 1, similarity: 0.8}]

# Multiple suggestions with threshold
LevenshteinUtils.closest_match("wrld", candidates, limit: 3, threshold: 0.4)

# Case insensitive
LevenshteinUtils.distance("Hello", "hello", case_sensitive: false) #=> 0

# Custom operation costs
LevenshteinUtils.distance("abc", "abd", substitution_cost: 5) #=> 2

# Get edit operations
LevenshteinUtils.edit_operations("kitten", "sitting")
#=> [{type: :substitute, position: 0, ...}, ...]

# Jaro-Winkler (better for names)
LevenshteinUtils.jaro_winkler("MARTHA", "MARHTA") #=> 0.961

# Find all within distance
LevenshteinUtils.find_within("cat", ["bat", "rat", "dog"], 1)
#=> ["bat", "rat"]

# Hamming distance (equal-length only)
LevenshteinUtils.hamming_distance("karolin", "kathrin") #=> 3
```

## API Reference

### `distance(str1, str2, options)`
Returns the minimum edit distance between two strings.

Options:
- `:case_sensitive` - Default: `true`
- `:insertion_cost` - Default: `1`
- `:deletion_cost` - Default: `1`
- `:substitution_cost` - Default: `1`

### `similarity(str1, str2, options)`
Returns normalized similarity (0.0 to 1.0).

### `damerau_distance(str1, str2, options)`
Damerau-Levenshtein distance with transposition support.

### `closest_match(target, candidates, options)`
Find closest match(es) from a list.

Options:
- `:threshold` - Minimum similarity (default: 0.0)
- `:limit` - Max results (default: 1)
- `:use_damerau` - Use Damerau-Levenshtein

### `edit_operations(str1, str2, options)`
Returns array of edit operations to transform str1 to str2.

### `jaro_winkler(str1, str2, options)`
Jaro-Winkler similarity (prefers matching prefixes).

### `hamming_distance(str1, str2, options)`
For equal-length strings only.

## Running Tests

```bash
ruby test_levenshtein.rb
```

## Running Examples

```bash
ruby examples.rb
```

## License

MIT License - Part of AllToolkit project.
#!/usr/bin/env ruby
# Number Utilities Example
# Demonstrates usage of the NumberUtils module

require_relative '../number_utils/mod'

include AllToolkit

puts "=" * 60
puts "Number Utilities Example"
puts "=" * 60

# ============================================================================
# Number Formatting
# ============================================================================
puts "\n--- Number Formatting ---"

# Basic formatting with thousands separator
puts "Format: #{NumberUtils.format(1234567.89)}"                    # => 1,234,567.89
puts "Format (no decimals): #{NumberUtils.format(1234567.89, precision: 0)}"  # => 1,234,568
puts "Format (custom): #{NumberUtils.format(1234567.89, separator: ' ', decimal: ',')}"  # => 1 234 567,89

# Currency formatting
puts "\nCurrency:"
puts "USD: #{NumberUtils.currency(1234.5)}"                         # => $1,234.50
puts "EUR: #{NumberUtils.currency(1234.5, symbol: '€')}"            # => €1,234.50
puts "JPY: #{NumberUtils.currency(1234.5, symbol: '¥', precision: 0)}"  # => ¥1,235

# Percentage formatting
puts "\nPercentage:"
puts "Default: #{NumberUtils.percentage(0.1567)}"                   # => 16%
puts "With precision: #{NumberUtils.percentage(0.1567, precision: 2)}"  # => 15.67%
puts "Without symbol: #{NumberUtils.percentage(0.1567, precision: 1, symbol: false)}"  # => 15.7

# Compact notation (K, M, B, T)
puts "\nCompact Notation:"
puts "1,500 => #{NumberUtils.compact(1500)}"                        # => 1.5K
puts "1,500,000 => #{NumberUtils.compact(1_500_000)}"               # => 1.5M
puts "1,500,000,000 => #{NumberUtils.compact(1_500_000_000)}"       # => 1.5B
puts "1,500,000,000,000 => #{NumberUtils.compact(1_500_000_000_000)}"  # => 1.5T
puts "-1,500 => #{NumberUtils.compact(-1500)}"                      # => -1.5K

# Ordinal numbers
puts "\nOrdinal Numbers:"
puts "1 => #{NumberUtils.ordinal(1)}"                               # => 1st
puts "2 => #{NumberUtils.ordinal(2)}"                               # => 2nd
puts "3 => #{NumberUtils.ordinal(3)}"                               # => 3rd
puts "11 => #{NumberUtils.ordinal(11)}"                             # => 11th
puts "21 => #{NumberUtils.ordinal(21)}"                             # => 21st

# Number to words
puts "\nNumber to Words:"
puts "0 => #{NumberUtils.to_words(0)}"                              # => zero
puts "21 => #{NumberUtils.to_words(21)}"                            # => twenty-one
puts "123 => #{NumberUtils.to_words(123)}"                          # => one hundred twenty-three
puts "1234 => #{NumberUtils.to_words(1234)}"                        # => one thousand two hundred thirty-four
puts "-5 => #{NumberUtils.to_words(-5)}"                            # => negative five

# ============================================================================
# Number Conversion
# ============================================================================
puts "\n--- Number Conversion ---"

# Roman numerals
puts "\nRoman Numerals:"
puts "2024 => #{NumberUtils.to_roman(2024)}"                        # => MMXXIV
puts "MMXXIV => #{NumberUtils.from_roman('MMXXIV')}"                # => 2024
puts "49 => #{NumberUtils.to_roman(49)}"                            # => XLIX

# Binary, Hex, Octal
puts "\nBase Conversions:"
puts "255 to binary: #{NumberUtils.to_binary(255)}"                 # => 11111111
puts "255 to binary (prefixed): #{NumberUtils.to_binary(255, prefix: true)}"  # => 0b11111111
puts "255 to hex: #{NumberUtils.to_hex(255)}"                       # => ff
puts "255 to hex (uppercase): #{NumberUtils.to_hex(255, uppercase: true)}"  # => FF
puts "255 to octal: #{NumberUtils.to_octal(255)}"                   # => 377

# ============================================================================
# Mathematical Functions
# ============================================================================
puts "\n--- Mathematical Functions ---"

# Clamp
puts "\nClamp:"
puts "clamp(10, 0, 5) => #{NumberUtils.clamp(10, 0, 5)}"            # => 5
puts "clamp(-5, 0, 5) => #{NumberUtils.clamp(-5, 0, 5)}"            # => 0
puts "clamp(3, 0, 5) => #{NumberUtils.clamp(3, 0, 5)}"              # => 3

# Linear interpolation (lerp)
puts "\nLinear Interpolation:"
puts "lerp(0, 100, 0.5) => #{NumberUtils.lerp(0, 100, 0.5)}"        # => 50.0
puts "lerp(0, 100, 0.25) => #{NumberUtils.lerp(0, 100, 0.25)}"      # => 25.0

# Map range
puts "\nMap Range:"
puts "map_range(5, 0, 10, 0, 100) => #{NumberUtils.map_range(5, 0, 10, 0, 100)}"  # => 50.0
puts "map_range(32, 0, 100, 0, 1) => #{NumberUtils.map_range(32, 0, 100, 0, 1)}"  # => 0.32

# Approximate equality
puts "\nApproximate Equality:"
puts "approx_equal?(1.0, 1.000000001) => #{NumberUtils.approx_equal?(1.0, 1.000000001)}"  # => true
puts "approx_equal?(1.0, 2.0) => #{NumberUtils.approx_equal?(1.0, 2.0)}"  # => false

# ============================================================================
# Statistical Functions
# ============================================================================
puts "\n--- Statistical Functions ---"

data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
puts "\nData: #{data.inspect}"
puts "Mean: #{NumberUtils.mean(data)}"                              # => 5.5
puts "Median: #{NumberUtils.median(data)}"                          # => 5.5
puts "Mode: #{NumberUtils.mode([1, 2, 2, 3, 3, 3]).inspect}"        # => [3]
puts "Std Dev: #{NumberUtils.std_dev(data).round(4)}"               # => ~2.8723
puts "Range: #{NumberUtils.range(data)}"                            # => 9

# ============================================================================
# Number Validation
# ============================================================================
puts "\n--- Number Validation ---"

puts "\nType Checks:"
puts "number?(42) => #{NumberUtils.number?(42)}"                     # => true
puts "number?('42') => #{NumberUtils.number?('42')}"                 # => false
puts "integer?(42) => #{NumberUtils.integer?(42)}"                   # => true
puts "integer?(3.14) => #{NumberUtils.integer?(3.14)}"               # => false

puts "\nParity Checks:"
puts "even?(4) => #{NumberUtils.even?(4)}"                           # => true
puts "odd?(5) => #{NumberUtils.odd?(5)}"                             # => true

puts "\nSign Checks:"
puts "positive?(5) => #{NumberUtils.positive?(5)}"                   # => true
puts "negative?(-5) => #{NumberUtils.negative?(-5)}"                 # => true
puts "zero?(0) => #{NumberUtils.zero?(0)}"                           # => true

puts "\nRange Checks:"
puts "between?(3, 1, 5) => #{NumberUtils.between?(3, 1, 5)}"         # => true
puts "prime?(7) => #{NumberUtils.prime?(7)}"                         # => true
puts "prime?(4) => #{NumberUtils.prime?(4)}"                         # => false
puts "perfect_square?(16) => #{NumberUtils.perfect_square?(16)}"     # => true

# ============================================================================
# Number Parsing
# ============================================================================
puts "\n--- Number Parsing ---"

puts "\nParse:"
puts "parse('42') => #{NumberUtils.parse('42')}"                     # => 42
puts "parse('3.14') => #{NumberUtils.parse('3.14')}"                 # => 3.14
puts "parse('1,000') => #{NumberUtils.parse('1,000')}"               # => 1000
puts "parse('invalid') => #{NumberUtils.parse('invalid').inspect}"   # => nil

puts "\nParse with default:"
puts "parse('invalid', default: 0) => #{NumberUtils.parse('invalid', default: 0)}"  # => 0

# ============================================================================
# Utility Functions
# ============================================================================
puts "\n--- Utility Functions ---"

puts "\nGCD and LCM:"
puts "gcd(24, 36) => #{NumberUtils.gcd(24, 36)}"                      # => 12
puts "lcm(24, 36) => #{NumberUtils.lcm(24, 36)}"                      # => 72

puts "\nFactorial and Fibonacci:"
puts "factorial(5) => #{NumberUtils.factorial(5)}"                  # => 120
puts "fibonacci(10) => #{NumberUtils.fibonacci(10)}"                # => 55

puts "\nRoots:"
puts "sqrt(16) => #{NumberUtils.sqrt(16)}"                          # => 4.0
puts "nth_root(27, 3) => #{NumberUtils.nth_root(27, 3)}"            # => 3.0

puts "\nAngle Conversion:"
puts "to_radians(180) => #{NumberUtils.to_radians(180)}"            # => 3.14159...
puts "to_degrees(PI) => #{NumberUtils.to_degrees(Math::PI)}"        # => 180.0
puts "normalize_angle(450) => #{NumberUtils.normalize_angle(450)}"  # => 90.0

puts "\nDigit Operations:"
puts "sum_of_digits(123) => #{NumberUtils.sum_of_digits(123)}"      # => 6
puts "reverse_digits(123) => #{NumberUtils.reverse_digits(123)}"    # => 321
puts "palindrome?(121) => #{NumberUtils.palindrome?(121)}"          # => true

# ============================================================================
# Random Number Generation
# ============================================================================
puts "\n--- Random Number Generation ---"

puts "\nRandom:"
puts "random(min: 0, max: 100) => #{NumberUtils.random(min: 0, max: 100).round(2)}"
puts "random_int(min: 1, max: 6) => #{NumberUtils.random_int(min: 1, max: 6)}"
puts "random_normal(mean: 0, std_dev: 1) => #{NumberUtils.random_normal(mean: 0, std_dev: 1).round(4)}"

# ============================================================================
# Convenience Methods
# ============================================================================
puts "\n--- Convenience Methods ---"

puts "\nShort forms:"
puts "fmt(1234567.89) => #{NumberUtils.fmt(1234567.89)}"              # Same as format
puts "cur(1234.5) => #{NumberUtils.cur(1234.5)}"                      # Same as currency
puts "pct(0.1567) => #{NumberUtils.pct(0.1567)}"                      # Same as percentage

puts "\n" + "=" * 60
puts "Example completed!"
puts "=" * 60
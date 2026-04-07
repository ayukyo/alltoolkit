#!/usr/bin/perl
# Number Utilities Example
# Demonstrates usage of NumberUtils module

use strict;
use warnings;
use utf8;
use lib '../number_utils';
use NumberUtils;

print "=== NumberUtils Examples ===\n\n";

# ============================================================================
# Formatting Examples
# ============================================================================
print "--- Formatting Examples ---\n";

# Number formatting
print "Number formatting:\n";
print "  format_number(1234567.89) = " . format_number(1234567.89) . "\n";
print "  format_number(1234567.89, '.', ',', 2) = " . format_number(1234567.89, '.', ',', 2) . " (German)\n";
print "\n";

# Currency formatting
print "Currency formatting:\n";
print "  format_currency(1234.5) = " . format_currency(1234.5) . "\n";
print "  format_currency(1234.5, '€', 2) = " . format_currency(1234.5, '€', 2) . "\n";
print "  format_currency(999999.99, '¥', 0) = " . format_currency(999999.99, '¥', 0) . "\n";
print "\n";

# Percentage formatting
print "Percentage formatting:\n";
print "  format_percentage(0.1567) = " . format_percentage(0.1567) . "\n";
print "  format_percentage(0.1567, 2) = " . format_percentage(0.1567, 2) . "\n";
print "  format_percentage(0.9999, 1) = " . format_percentage(0.9999, 1) . "\n";
print "\n";

# Compact notation
print "Compact notation:\n";
print "  format_compact(1234) = " . format_compact(1234) . "\n";
print "  format_compact(1500000) = " . format_compact(1500000) . "\n";
print "  format_compact(2500000000) = " . format_compact(2500000000) . "\n";
print "\n";

# Ordinal formatting
print "Ordinal formatting:\n";
for my $n (1, 2, 3, 4, 11, 12, 13, 21, 22, 23, 100) {
    print "  format_ordinal($n) = " . format_ordinal($n) . "\n";
}
print "\n";

# Number to words
print "Number to words:\n";
for my $n (0, 1, 21, 100, 1000, 1234, -42) {
    print "  number_to_words($n) = " . number_to_words($n) . "\n";
}
print "\n";

# ============================================================================
# Conversion Examples
# ============================================================================
print "--- Conversion Examples ---\n";

# Roman numerals
print "Roman numerals:\n";
for my $n (1, 4, 5, 9, 49, 2024, 3999) {
    my $roman = to_roman($n);
    my $back = from_roman($roman);
    print "  $n -> $roman -> $back\n";
}
print "\n";

# Binary, Hex, Octal
print "Number base conversions:\n";
for my $n (0, 1, 15, 16, 255, 256) {
    print "  $n: binary=" . to_binary($n) . 
          ", hex=" . to_hex($n) . 
          ", octal=" . to_octal($n) . "\n";
}
print "\n";

# With prefixes
print "With prefixes:\n";
print "  to_binary(255, 1) = " . to_binary(255, 1) . "\n";
print "  to_hex(255, 1, 1) = " . to_hex(255, 1, 1) . "\n";
print "  to_octal(64, 1) = " . to_octal(64, 1) . "\n";
print "\n";

# ============================================================================
# Mathematical Examples
# ============================================================================
print "--- Mathematical Examples ---\n";

# Clamp
print "Clamp:\n";
print "  clamp(5, 0, 10) = " . clamp(5, 0, 10) . " (within range)\n";
print "  clamp(-5, 0, 10) = " . clamp(-5, 0, 10) . " (below min)\n";
print "  clamp(15, 0, 10) = " . clamp(15, 0, 10) . " (above max)\n";
print "\n";

# Lerp (Linear interpolation)
print "Linear interpolation:\n";
for my $t (0, 0.25, 0.5, 0.75, 1) {
    print "  lerp(0, 100, $t) = " . lerp(0, 100, $t) . "\n";
}
print "\n";

# Map range
print "Map range:\n";
print "  map_range(5, 0, 10, 0, 100) = " . map_range(5, 0, 10, 0, 100) . "\n";
print "  map_range(32, 0, 100, 0, 1) = " . map_range(32, 0, 100, 0, 1) . " (percentage)\n";
print "\n";

# Rounding
print "Rounding:\n";
print "  round_to_multiple(23, 5) = " . round_to_multiple(23, 5) . "\n";
print "  round_to_multiple(22, 5) = " . round_to_multiple(22, 5) . "\n";
print "  round_to_places(3.14159, 2) = " . round_to_places(3.14159, 2) . "\n";
print "\n";

# ============================================================================
# Statistical Examples
# ============================================================================
print "--- Statistical Examples ---\n";

my @data = (12, 45, 23, 67, 34, 89, 45, 23, 45, 67);
print "Data: @data\n";
print "  mean = " . mean(@data) . "\n";
print "  median = " . median(@data) . "\n";
print "  mode = " . mode(@data) . "\n";
print "  std_dev (population) = " . std_dev(@data) . "\n";
print "  std_dev (sample) = " . std_dev(@data, 1) . "\n";
print "  range = " . range(@data) . "\n";
print "  sum_of_squares = " . sum_of_squares(@data) . "\n";
print "\n";

# ============================================================================
# Validation Examples
# ============================================================================
print "--- Validation Examples ---\n";

# Number validation
print "Number validation:\n";
for my $val (42, 3.14, -5, "abc", undef) {
    my $v = defined $val ? $val : 'undef';
    print "  is_number($v) = " . (is_number($val) ? 'true' : 'false') . "\n";
}
print "\n";

# Integer validation
print "Integer validation:\n";
for my $val (42, 3.14, 0) {
    print "  is_integer($val) = " . (is_integer($val) ? 'true' : 'false') . "\n";
}
print "\n";

# Prime numbers
print "Prime numbers (1-20):\n";
for my $n (1..20) {
    if (is_prime($n)) {
        print "  $n is prime\n";
    }
}
print "\n";

# Perfect squares
print "Perfect squares (1-50):\n";
for my $n (1..50) {
    if (is_perfect_square($n)) {
        my $root = int(sqrt($n));
        print "  $n = $root²\n";
    }
}
print "\n";

# Range checking
print "Range checking:\n";
print "  is_between(5, 0, 10) = " . (is_between(5, 0, 10) ? 'true' : 'false') . "\n";
print "  is_between(15, 0, 10) = " . (is_between(15, 0, 10) ? 'true' : 'false') . "\n";
print "\n";

# ============================================================================
# Parsing Examples
# ============================================================================
print "--- Parsing Examples ---\n";

my @inputs = ("42", "3.14", "1,234.56", "abc");
for my $input (@inputs) {
    print "parse_number('$input') = ";
    my $result = parse_number($input);
    print defined $result ? $result : 'undef';
    print "\n";
}
print "\n";

# ============================================================================
# Utility Examples
# ============================================================================
print "--- Utility Examples ---\n";

# GCD and LCM
print "GCD and LCM:\n";
print "  gcd(24, 36) = " . gcd(24, 36) . "\n";
print "  lcm(4, 6) = " . lcm(4, 6) . "\n";
print "\n";

# Factorial
print "Factorial:\n";
for my $n (0, 1, 5, 10) {
    print "  factorial($n) = " . factorial($n) . "\n";
}
print "\n";

# Fibonacci
print "Fibonacci sequence:\n";
for my $n (0..10) {
    print "  fibonacci($n) = " . fibonacci($n);
    print ", " if $n < 10;
}
print "\n\n";

# Roots
print "Roots:\n";
print "  sqrt(16) = " . sqrt(16) . "\n";
print "  sqrt(2) = " . sqrt(2) . "\n";
print "  nth_root(27, 3) = " . nth_root(27, 3) . "\n";
print "  nth_root(16, 4) = " . nth_root(16, 4) . "\n";
print "\n";

# Angle conversion
print "Angle conversion:\n";
print "  to_radians(180) = " . to_radians(180) . " radians\n";
print "  to_degrees(3.14159) = " . to_degrees(3.14159) . " degrees\n";
print "\n";

# Digit manipulation
print "Digit manipulation:
";
print "  sum_of_digits(12345) = " . sum_of_digits(12345) . "\n";
print "  reverse_digits(12345) = " . reverse_digits(12345) . "\n";
print "  is_palindrome(121) = " . (is_palindrome(121) ? 'true' : 'false') . "\n";
print "  is_palindrome(123) = " . (is_palindrome(123) ? 'true' : 'false') . "\n";
print "\n";

# ============================================================================
# Random Examples
# ============================================================================
print "--- Random Examples ---\n";

print "Random numbers:\n";
print "  random() = " . random() . "\n";
print "  random(10, 20) = " . random(10, 20) . "\n";
print "  random_int(1, 100) = " . random_int(1, 100) . "\n";
print "  random_normal() = " . random_normal() . "\n";
print "\n";

# ============================================================================
# Practical Use Cases
# ============================================================================
print "--- Practical Use Cases ---\n";

# 1. Grade calculator
print "1. Grade calculator:\n";
my @grades = (85, 92, 78, 95, 88);
my $avg = mean(@grades);
my $grade = $avg >= 90 ? 'A' : $avg >= 80 ? 'B' : $avg >= 70 ? 'C' : 'D';
print "   Grades: @grades\n";
print "   Average: " . format_number($avg, ',', '.', 1) . " -> Grade: $grade\n";
print "\n";

# 2. Sales report
print "2. Sales report:\n";
my @sales = (1250, 2300, 1890, 3200, 2750);
print "   Daily sales:\n";
for my $sale (@sales) {
    print "     " . format_currency($sale) . "\n";
}
print "   Total: " . format_currency(0 + @sales * mean(@sales)) . "\n";
print "   Average: " . format_currency(mean(@sales)) . "\n";
print "   Best day: " . format_currency(89) . "\n";  # Max would need separate function
print "\n";

# 3. Progress calculation
print "3. Progress calculation:\n";
my $completed = 73;
my $total = 100;
my $progress = $completed / $total;
print "   Completed: $completed / $total\n";
print "   Progress: " . format_percentage($progress, 1) . "\n";
print "   Visual: [" . ("#" x int($progress * 20)) . (" " x (20 - int($progress * 20))) . "]\n";
print "\n";

# 4. File size formatting
print "4. File size formatting:\n";
my @sizes = (512, 1024, 1536000, 2097152, 1073741824);
for my $size (@sizes) {
    print "   $size bytes = " . format_compact($size) . "B\n";
}
print "\n";

print "=== End of Examples ===\n";

#!/usr/bin/perl
# Number Utilities Test Suite
# Comprehensive tests for NumberUtils module

use strict;
use warnings;
use utf8;
use lib '.';
use NumberUtils;

# Test counter
my $tests_run = 0;
my $tests_passed = 0;

# Test helper
sub test {
    my ($name, $condition) = @_;
    $tests_run++;
    if ($condition) {
        $tests_passed++;
        print "✓ $name\n";
    } else {
        print "✗ $name\n";
    }
}

sub test_eq {
    my ($name, $got, $expected) = @_;
    $tests_run++;
    
    my $match;
    if (!defined $got && !defined $expected) {
        $match = 1;
    } elsif (!defined $got || !defined $expected) {
        $match = 0;
    } elsif (is_number($got) && is_number($expected)) {
        $match = approx_equal($got, $expected, 1e-6);
    } else {
        $match = $got eq $expected;
    }
    
    if ($match) {
        $tests_passed++;
        print "✓ $name\n";
    } else {
        print "✗ $name (got: ", (defined $got ? $got : 'undef'), 
              ", expected: ", (defined $expected ? $expected : 'undef'), ")\n";
    }
}

print "=== NumberUtils Test Suite ===\n\n";

# ============================================================================
# Formatting Tests
# ============================================================================
print "--- Formatting Tests ---\n";

# format_number
test_eq("format_number basic", format_number(1234567.89), "1,234,567.89");
test_eq("format_number integer", format_number(1000), "1,000");
test_eq("format_number negative", format_number(-1234.56), "-1,234.56");
test_eq("format_number with precision", format_number(1234.5678, ',', '.', 2), "1,234.57");
test_eq("format_number zero", format_number(0), "0");
test_eq("format_number german style", format_number(1234.56, '.', ',', 2), "1.234,56");

# format_currency
test_eq("format_currency default", format_currency(1234.5), "$1,234.50");
test_eq("format_currency euro", format_currency(1234.5, '€', 2), "€1,234.50");
test_eq("format_currency zero", format_currency(0), "$0.00");
test_eq("format_currency negative", format_currency(-99.99), "$-99.99");

# format_percentage
test_eq("format_percentage default", format_percentage(0.1567), "16%");
test_eq("format_percentage with precision", format_percentage(0.1567, 2), "15.67%");
test_eq("format_percentage without symbol", format_percentage(0.5, 0, 0), "50");
test_eq("format_percentage zero", format_percentage(0), "0%");
test_eq("format_percentage one", format_percentage(1), "100%");

# format_compact
test_eq("format_compact K", format_compact(1234), "1.2K");
test_eq("format_compact M", format_compact(1500000), "1.5M");
test_eq("format_compact B", format_compact(2500000000), "2.5B");
test_eq("format_compact zero", format_compact(0), "0");
test_eq("format_compact negative", format_compact(-1500), "-1.5K");
test_eq("format_compact small", format_compact(999), "999");

# format_ordinal
test_eq("format_ordinal 1st", format_ordinal(1), "1st");
test_eq("format_ordinal 2nd", format_ordinal(2), "2nd");
test_eq("format_ordinal 3rd", format_ordinal(3), "3rd");
test_eq("format_ordinal 4th", format_ordinal(4), "4th");
test_eq("format_ordinal 11th", format_ordinal(11), "11th");
test_eq("format_ordinal 12th", format_ordinal(12), "12th");
test_eq("format_ordinal 13th", format_ordinal(13), "13th");
test_eq("format_ordinal 21st", format_ordinal(21), "21st");
test_eq("format_ordinal negative", format_ordinal(-1), "-1st");

# number_to_words
test_eq("number_to_words zero", number_to_words(0), "zero");
test_eq("number_to_words one", number_to_words(1), "one");
test_eq("number_to_words twenty-one", number_to_words(21), "twenty-one");
test_eq("number_to_words hundred", number_to_words(100), "one hundred");
test_eq("number_to_words thousand", number_to_words(1000), "one thousand");
test_eq("number_to_words negative", number_to_words(-42), "negative forty-two");

print "\n";

# ============================================================================
# Conversion Tests
# ============================================================================
print "--- Conversion Tests ---\n";

# to_roman / from_roman
test_eq("to_roman 1", to_roman(1), "I");
test_eq("to_roman 4", to_roman(4), "IV");
test_eq("to_roman 5", to_roman(5), "V");
test_eq("to_roman 9", to_roman(9), "IX");
test_eq("to_roman 10", to_roman(10), "X");
test_eq("to_roman 49", to_roman(49), "XLIX");
test_eq("to_roman 2024", to_roman(2024), "MMXXIV");
test_eq("to_roman 3999", to_roman(3999), "MMMCMXCIX");
test_eq("to_roman out of range", to_roman(4000), undef);
test_eq("to_roman negative", to_roman(-1), undef);

test_eq("from_roman I", from_roman("I"), 1);
test_eq("from_roman IV", from_roman("IV"), 4);
test_eq("from_roman MMXXIV", from_roman("MMXXIV"), 2024);
test_eq("from_roman lowercase", from_roman("mmxxiv"), 2024);
test_eq("from_roman invalid", from_roman("ABC"), undef);

# to_binary
test_eq("to_binary 0", to_binary(0), "0");
test_eq("to_binary 1", to_binary(1), "1");
test_eq("to_binary 255", to_binary(255), "11111111");
test_eq("to_binary with prefix", to_binary(255, 1), "0b11111111");
test_eq("to_binary with min_width", to_binary(5, 0, 8), "00000101");
test_eq("to_binary negative", to_binary(-1), undef);

# to_hex
test_eq("to_hex 0", to_hex(0), "0");
test_eq("to_hex 255", to_hex(255), "ff");
test_eq("to_hex uppercase", to_hex(255, 0, 1), "FF");
test_eq("to_hex with prefix", to_hex(255, 1), "0xff");
test_eq("to_hex with min_width", to_hex(15, 0, 0, 4), "000f");

# to_octal
test_eq("to_octal 0", to_octal(0), "0");
test_eq("to_octal 64", to_octal(64), "100");
test_eq("to_octal with prefix", to_octal(64, 1), "0100");

print "\n";

# ============================================================================
# Mathematical Tests
# ============================================================================
print "--- Mathematical Tests ---\n";

# clamp
test_eq("clamp within range", clamp(5, 0, 10), 5);
test_eq("clamp below min", clamp(-5, 0, 10), 0);
test_eq("clamp above max", clamp(15, 0, 10), 10);
test_eq("clamp at min", clamp(0, 0, 10), 0);
test_eq("clamp at max", clamp(10, 0, 10), 10);

# lerp
test_eq("lerp 0", lerp(0, 100, 0), 0);
test_eq("lerp 0.5", lerp(0, 100, 0.5), 50);
test_eq("lerp 1", lerp(0, 100, 1), 100);
test_eq("lerp clamped below", lerp(0, 100, -0.5), 0);
test_eq("lerp clamped above", lerp(0, 100, 1.5), 100);

# map_range
test_eq("map_range center", map_range(5, 0, 10, 0, 100), 50);
test_eq("map_range min", map_range(0, 0, 10, 0, 100), 0);
test_eq("map_range max", map_range(10, 0, 10, 0, 100), 100);
test_eq("map_range negative", map_range(-5, -10, 0, 0, 100), 50);

# approx_equal
test("approx_equal true", approx_equal(0.1 + 0.2, 0.3));
test("approx_equal false", !approx_equal(0.1, 0.2));
test("approx_equal with epsilon", approx_equal(1.0, 1.0000001, 1e-6));

# round_to_multiple
test_eq("round_to_multiple 23 to 5", round_to_multiple(23, 5), 25);
test_eq("round_to_multiple 22 to 5", round_to_multiple(22, 5), 20);
test_eq("round_to_multiple 25 to 5", round_to_multiple(25, 5), 25);
test_eq("round_to_multiple zero", round_to_multiple(0, 5), 0);

# round_to_places
test_eq("round_to_places 2", round_to_places(3.14159, 2), 3.14);
test_eq("round_to_places 0", round_to_places(3.14159, 0), 3);
test_eq("round_to_places round up", round_to_places(3.14159, 3), 3.142);

print "\n";

# ============================================================================
# Statistical Tests
# ============================================================================
print "--- Statistical Tests ---\n";

# mean
test_eq("mean basic", mean(1, 2, 3, 4, 5), 3);
test_eq("mean single", mean(5), 5);
test_eq("mean negative", mean(-5, 5), 0);
test_eq("mean empty", mean(), undef);

# median
test_eq("median odd", median(1, 2, 3, 4, 5), 3);
test_eq("median even", median(1, 2, 3, 4), 2.5);
test_eq("median single", median(5), 5);
test_eq("median empty", median(), undef);

# mode
test_eq("mode basic", mode(1, 2, 2, 3, 3, 3), 3);
test_eq("mode single", mode(1, 2, 3), 1);
test_eq("mode empty", mode(), undef);

# std_dev
test_eq("std_dev population", std_dev(1, 2, 3, 4, 5), 1.4142135623730951);
test_eq("std_dev sample", std_dev(1, 2, 3, 4, 5, 1), 1.5811388300841898);
test_eq("std_dev single", std_dev(5), undef);
test_eq("std_dev empty", std_dev(), undef);

# sum_of_squares
test_eq("sum_of_squares", sum_of_squares(1, 2, 3), 14);
test_eq("sum_of_squares empty", sum_of_squares(), 0);

# range
test_eq("range basic", range(1, 2, 3, 4, 5), 4);
test_eq("range empty", range(), undef);

print "\n";

# ============================================================================
# Validation Tests
# ============================================================================
print "--- Validation Tests ---\n";

# is_number
test("is_number integer", is_number(42));
test("is_number float", is_number(3.14));
test("is_number negative", is_number(-5));
test("is_number string", !is_number("abc"));
test("is_number undef", !is_number(undef));
test("is_number scientific", is_number("1.5e10"));

# is_integer
test("is_integer positive", is_integer(42));
test("is_integer negative", is_integer(-42));
test("is_integer zero", is_integer(0));
test("is_integer float", !is_integer(3.14));
test("is_integer string", !is_integer("42"));

# is_float
test("is_float positive", is_float(3.14));
test("is_float scientific", is_float(1e10));
test("is_float integer", !is_float(42));
test("is_float string", !is_float("3.14"));

# is_even / is_odd
test("is_even true", is_even(4));
test("is_even false", !is_even(5));
test("is_even zero", is_even(0));
test("is_odd true", is_odd(5));
test("is_odd false", !is_odd(4));

# is_positive / is_negative / is_zero
test("is_positive true", is_positive(5));
test("is_positive false", !is_positive(-5));
test("is_positive zero", !is_positive(0));
test("is_negative true", is_negative(-5));
test("is_negative false", !is_negative(5));
test("is_negative zero", !is_negative(0));
test("is_zero true", is_zero(0));
test("is_zero false", !is_zero(5));

# is_between
test("is_between inclusive", is_between(5, 0, 10));
test("is_between at min", is_between(0, 0, 10));
test("is_between at max", is_between(10, 0, 10));
test("is_between outside", !is_between(15, 0, 10));

# is_prime
test("is_prime 2", is_prime(2));
test("is_prime 3", is_prime(3));
test("is_prime 4", !is_prime(4));
test("is_prime 17", is_prime(17));
test("is_prime 1", !is_prime(1));
test("is_prime negative", !is_prime(-5));

# is_perfect_square
test("is_perfect_square 4", is_perfect_square(4));
test("is_perfect_square 16", is_perfect_square(16));
test("is_perfect_square 5", !is_perfect_square(5));
test("is_perfect_square 0", is_perfect_square(0));
test("is_perfect_square negative", !is_perfect_square(-4));

print "\n";

# ============================================================================
# Parsing Tests
# ============================================================================
print "--- Parsing Tests ---\n";

# parse_number
test_eq("parse_number integer", parse_number("42"), 42);
test_eq("parse_number float", parse_number("3.14"), 3.14);
test_eq("parse_number with comma", parse_number("1,234.56"), 1234.56);
test_eq("parse_number negative", parse_number("-5"), -5);
test_eq("parse_number invalid", parse_number("abc"), undef);
test_eq("parse_number with default", parse_number("abc", 0), 0);

# parse_int
test_eq("parse_int basic", parse_int("42"), 42);
test_eq("parse_int negative", parse_int("-5"), -5);
test_eq("parse_int with comma", parse_int("1,000"), 1000);
test_eq("parse_int invalid", parse_int("abc", -1), -1);

# parse_float
test_eq("parse_float basic", parse_float("3.14"), 3.14);
test_eq("parse_float integer", parse_float("42"), 42.0);
test_eq("parse_float invalid", parse_float("abc", 0.0), 0.0);

print "\n";

# ============================================================================
# Utility Tests
# ============================================================================
print "--- Utility Tests ---\n";

# gcd
test_eq("gcd basic", gcd(24, 36), 12);
test_eq("gcd coprime", gcd(7, 13), 1);
test_eq("gcd same", gcd(10, 10), 10);
test_eq("gcd negative", gcd(-24, 36), 12);

# lcm
test_eq("lcm basic", lcm(4, 6), 12);
test_eq("lcm same", lcm(10, 10), 10);
test_eq("lcm zero", lcm(0, 5), 0);

# factorial
test_eq("factorial 0", factorial(0), 1);
test_eq("factorial 1", factorial(1), 1);
test_eq("factorial 5", factorial(5), 120);
test_eq("factorial negative", factorial(-1), undef);

# fibonacci
test_eq("fibonacci 0", fibonacci(0), 0);
test_eq("fibonacci 1", fibonacci(1), 1);
test_eq("fibonacci 10", fibonacci(10), 55);
test_eq("fibonacci negative", fibonacci(-1), undef);

# sqrt
test_eq("sqrt 4", sqrt(4), 2);
test_eq("sqrt 2", sqrt(2), 1.4142135623730951);
test_eq("sqrt 0", sqrt(0), 0);
test_eq("sqrt negative", sqrt(-1), undef);

# nth_root
test_eq("nth_root cube", nth_root(27, 3), 3);
test_eq("nth_root square", nth_root(16, 2), 4);
test_eq("nth_root negative odd", nth_root(-27, 3), -3);
test_eq("nth_root negative even", nth_root(-16, 2), undef);

# to_radians / to_degrees
test_eq("to_radians 180", to_radians(180), 3.141592653589793);
test_eq("to_degrees pi", to_degrees(3.141592653589793), 180);

# normalize_angle
test_eq("normalize_angle 360", normalize_angle(360), 0);
test_eq("normalize_angle 450", normalize_angle(450), 90);
test_eq("normalize_angle -90", normalize_angle(-90), 270);

# sum_of_digits
test_eq("sum_of_digits 12345", sum_of_digits(12345), 15);
test_eq("sum_of_digits negative", sum_of_digits(-123), 6);
test_eq("sum_of_digits 0", sum_of_digits(0), 0);

# reverse_digits
test_eq("reverse_digits 12345", reverse_digits(12345), 54321);
test_eq("reverse_digits negative", reverse_digits(-123), -321);
test_eq("reverse_digits 0", reverse_digits(0), 0);

# is_palindrome
test("is_palindrome true", is_palindrome(121));
test("is_palindrome false", !is_palindrome(123));
test("is_palindrome single", is_palindrome(5));

print "\n";

# ============================================================================
# Random Tests (basic validation)
# ============================================================================
print "--- Random Tests ---\n";

my $r = random();
test("random basic", is_number($r) && $r >= 0 && $r < 1);

$r = random(10, 20);
test("random range", is_number($r) && $r >= 10 && $r < 20);

my $ri = random_int(1, 10);
test("random_int", is_integer($ri) && $ri >= 1 && $ri <= 10);

my $rn = random_normal();
test("random_normal", is_number($rn));

print "\n";

# ============================================================================
# Summary
# ============================================================================
print "=== Test Summary ===\n";
print "Tests run: $tests_run\n";
print "Tests passed: $tests_passed\n";
print "Tests failed: " . ($tests_run - $tests_passed) . "\n";

if ($tests_passed == $tests_run) {
    print "\nAll tests passed! ✓\n";
    exit 0;
} else {
    print "\nSome tests failed! ✗\n";
    exit 1;
}

print "--- Statistical Tests ---\n";

# mean
test_eq("mean basic", mean(1, 2, 3, 4, 5), 3);
test_eq("mean single", mean(5), 5);
test_eq("mean negative", mean(-5, 5), 0);
test_eq("mean empty", mean(), undef);

# median
test_eq("median odd", median(1, 2, 3, 4, 5), 3);
test_eq("median even", median(1, 2, 3, 4), 2.5);
test_eq("median single", median(5), 5);
test_eq("median empty", median(), undef);

# mode
test_eq("mode basic", mode(1, 2, 2, 3, 3, 3), 3);
test_eq("mode single", mode(1, 2, 3), 1);
test_eq("mode empty", mode(), undef);

# std_dev
test_eq("std_dev population", std_dev(1, 2, 3, 4, 5), 1.4142135623730951);
test_eq("std_dev sample", std_dev(1, 2, 3, 4, 5, 1), 1.5811388300841898);
test_eq("std_dev single", std_dev(5), undef);
test_eq("std_dev empty", std_dev(), undef);

# sum_of_squares
test_eq("sum_of_squares", sum_of_squares(1, 2, 3), 14);
test_eq("sum_of_squares empty", sum_of_squares(), 0);

# range
test_eq("range basic", range(1, 2, 3, 4, 5), 4);
test_eq("range empty", range(), undef);

print "\n";

# ============================================================================
# Validation Tests
# ============================================================================
print "--- Validation Tests ---\n";

# is_number
test("is_number integer", is_number(42));
test("is_number float", is_number(3.14));
test("is_number negative", is_number(-5));
test("is_number string", !is_number("abc"));
test("is_number undef", !is_number(undef));
test("is_number scientific", is_number("1.5e10"));

# is_integer
test("is_integer positive", is_integer(42));
test("is_integer negative", is_integer(-42));
test("is_integer zero", is_integer(0));
test("is_integer float", !is_integer(3.14));
test("is_integer string", !is_integer("42"));

# is_float
test("is_float positive", is_float(3.14));
test("is_float scientific", is_float(1e10));
test("is_float integer", !is_float(42));
test("is_float string", !is_float("3.14"));

# is_even / is_odd
test("is_even true", is_even(4));
test("is_even false", !is_even(5));
test("is_even zero", is_even(0));
test("is_odd true", is_odd(5));
test("is_odd false", !is_odd(4));

# is_positive / is_negative / is_zero
test("is_positive true", is_positive(5));
test("is_positive false", !is_positive(-5));
test("is_positive zero", !is_positive(0));
test("is_negative true", is_negative(-5));
test("is_negative false", !is_negative(5));
test("is_negative zero", !is_negative(0));
test("is_zero true", is_zero(0));
test("is_zero false", !is_zero(5));

# is_between
test("is_between inclusive", is_between(5, 0, 10));
test("is_between at min", is_between(0, 0, 10));
test("is_between at max", is_between(10, 0, 10));
test("is_between outside", !is_between(15, 0, 10));

# is_prime
test("is_prime 2", is_prime(2));
test("is_prime 3", is_prime(3));
test("is_prime 4", !is_prime(4));
test("is_prime 17", is_prime(17));
test("is_prime 1", !is_prime(1));
test("is_prime negative", !is_prime(-5));

# is_perfect_square
test("is_perfect_square 4", is_perfect_square(4));
test("is_perfect_square 16", is_perfect_square(16));
test("is_perfect_square 5", !is_perfect_square(5));
test("is_perfect_square 0", is_perfect_square(0));
test("is_perfect_square negative", !is_perfect_square(-4));

print "\n";

# ============================================================================
# Parsing Tests
# ============================================================================
print "--- Parsing Tests ---\n";

# parse_number
test_eq("parse_number integer", parse_number("42"), 42);
test_eq("parse_number float", parse_number("3.14"), 3.14);
test_eq("parse_number with comma", parse_number("1,234.56"), 1234.56);
test_eq("parse_number negative", parse_number("-5"), -5);
test_eq("parse_number invalid", parse_number("abc"), undef);
test_eq("parse_number with default", parse_number("abc", 0), 0);

# parse_int
test_eq("parse_int basic", parse_int("42"), 42);
test_eq("parse_int negative", parse_int("-5"), -5);
test_eq("parse_int with comma", parse_int("1,000"), 1000);
test_eq("parse_int invalid", parse_int("abc", -1), -1);

# parse_float
test_eq("parse_float basic", parse_float("3.14"), 3.14);
test_eq("parse_float integer", parse_float("42"), 42.0);
test_eq("parse_float invalid", parse_float("abc", 0.0), 0.0);

print "\n";

# ============================================================================
# Utility Tests
# ============================================================================
print "--- Utility Tests ---\n";

# gcd
test_eq("gcd basic", gcd(24, 36), 12);
test_eq("gcd coprime", gcd(7, 13), 1);
test_eq("gcd same", gcd(10, 10), 10);
test_eq("gcd negative", gcd(-24, 36), 12);

# lcm
test_eq("lcm basic", lcm(4, 6), 12);
test_eq("lcm same", lcm(10, 10), 10);
test_eq("lcm zero", lcm(0, 5), 0);

# factorial
test_eq("factorial 0", factorial(0), 1);
test_eq("factorial 1", factorial(1), 1);
test_eq("factorial 5", factorial(5), 120);
test_eq("factorial negative", factorial(-1), undef);

# fibonacci
test_eq("fibonacci 0", fibonacci(0), 0);
test_eq("fibonacci 1", fibonacci(1), 1);
test_eq("fibonacci 10", fibonacci(10), 55);
test_eq("fibonacci negative", fibonacci(-1), undef);

# sqrt
test_eq("sqrt 4", sqrt(4), 2);
test_eq("sqrt 2", sqrt(2), 1.4142135623730951);
test_eq("sqrt 0", sqrt(0), 0);
test_eq("sqrt negative", sqrt(-1), undef);

# nth_root
test_eq("nth_root cube", nth_root(27, 3), 3);
test_eq("nth_root square", nth_root(16, 2), 4);
test_eq("nth_root negative odd", nth_root(-27, 3), -3);
test_eq("nth_root negative even", nth_root(-16, 2), undef);

# to_radians / to_degrees
test_eq("to_radians 180", to_radians(180), 3.141592653589793);
test_eq("to_degrees pi", to_degrees(3.141592653589793), 180);

# normalize_angle
test_eq("normalize_angle 360", normalize_angle(360), 0);
test_eq("normalize_angle 450", normalize_angle(450), 90);
test_eq("normalize_angle -90", normalize_angle(-90), 270);

# sum_of_digits
test_eq("sum_of_digits 12345", sum_of_digits(12345), 15);
test_eq("sum_of_digits negative", sum_of_digits(-123), 6);
test_eq("sum_of_digits 0", sum_of_digits(0), 0);

# reverse_digits
test_eq("reverse_digits 12345", reverse_digits(12345), 54321);
test_eq("reverse_digits negative", reverse_digits(-123), -321);
test_eq("reverse_digits 0", reverse_digits(0), 0);

# is_palindrome
test("is_palindrome true", is_palindrome(121));
test("is_palindrome false", !is_palindrome(123));
test("is_palindrome single", is_palindrome(5));

print "\n";

# ============================================================================
# Random Tests (basic validation)
# ============================================================================
print "--- Random Tests ---\n";

my $r = random();
test("random basic", is_number($r) && $r >= 0 && $r < 1);

$r = random(10, 20);
test("random range", is_number($r) && $r >= 10 && $r < 20);

my $ri = random_int(1, 10);
test("random_int", is_integer($ri) && $ri >= 1 && $ri <= 10);

my $rn = random_normal();
test("random_normal", is_number($rn));

print "\n";

# ============================================================================
# Summary
# ============================================================================
print "=== Test Summary ===\n";
print "Tests run: $tests_run\n";
print "Tests passed: $tests_passed\n";
print "Tests failed: " . ($tests_run - $tests_passed) . "\n";

if ($tests_passed == $tests_run) {
    print "\nAll tests passed! ✓\n";
    exit 0;
} else {
    print "\nSome tests failed! ✗\n";
    exit 1;
}

#!/usr/bin/perl
# Number Utilities Module for Perl
# Provides comprehensive number manipulation, formatting, validation, and mathematical functions
# Zero dependencies - uses only Perl standard library

package NumberUtils;

use strict;
use warnings;
use utf8;
use Exporter qw(import);

# Export all functions
our @EXPORT = qw(
    format_number format_currency format_percentage format_compact
    format_ordinal number_to_words
    to_roman from_roman to_binary to_hex to_octal
    clamp lerp map_range approx_equal round_to_multiple round_to_places
    mean median mode std_dev sum_of_squares range
    is_number is_integer is_float is_even is_odd
    is_positive is_negative is_zero is_between is_prime is_perfect_square
    parse_number parse_int parse_float
    gcd lcm factorial fibonacci sqrt nth_root
    to_radians to_degrees normalize_angle sum_of_digits reverse_digits is_palindrome
    random random_int random_normal
);

our $VERSION = '1.0.0';

# Roman numeral mappings
my %ROMAN_MAP = (
    'I' => 1, 'V' => 5, 'X' => 10, 'L' => 50,
    'C' => 100, 'D' => 500, 'M' => 1000
);

my @ROMAN_PAIRS = (
    [1000, 'M'], [900, 'CM'], [500, 'D'], [400, 'CD'],
    [100, 'C'], [90, 'XC'], [50, 'L'], [40, 'XL'],
    [10, 'X'], [9, 'IX'], [5, 'V'], [4, 'IV'], [1, 'I']
);

# Number words for conversion
my @ONES = qw(zero one two three four five six seven eight nine);
my @TEENS = qw(ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen);
my @TENS = qw(twenty thirty forty fifty sixty seventy eighty ninety);
my @SCALES = ('', 'thousand', 'million', 'billion', 'trillion');

# ============================================================================
# Formatting Functions
# ============================================================================

=head2 format_number

Format a number with thousands separator and optional decimal places.

Parameters:
    $number     - The number to format
    $separator  - Thousands separator (default: ',')
    $decimal    - Decimal point (default: '.')
    $precision  - Number of decimal places (default: undef, no rounding)

Returns:
    Formatted number string

Example:
    format_number(1234567.89)              # "1,234,567.89"
    format_number(1234567.89, '.', ',', 2) # "1.234.567,89" (German style)
=cut

sub format_number {
    my ($number, $separator, $decimal, $precision) = @_;
    $separator //= ',';
    $decimal   //= '.';
    
    return undef unless defined $number;
    
    # Round if precision specified
    if (defined $precision) {
        $number = sprintf("%.${precision}f", $number);
    }
    
    my $is_negative = $number < 0;
    $number = abs($number);
    
    my ($int_part, $dec_part) = split /\./, $number;
    $int_part //= 0;
    
    # Add thousands separators
    $int_part =~ s/(\d)(?=(\d{3})+$)/$1$separator/g;
    
    my $result = $int_part;
    $result .= $decimal . $dec_part if defined $dec_part;
    $result = '-' . $result if $is_negative;
    
    return $result;
}

=head2 format_currency

Format a number as currency.

Parameters:
    $number     - The number to format
    $symbol     - Currency symbol (default: '$')
    $precision  - Decimal places (default: 2)

Returns:
    Formatted currency string

Example:
    format_currency(1234.5)           # "$1,234.50"
    format_currency(1234.5, '€', 2)   # "€1,234.50"
=cut

sub format_currency {
    my ($number, $symbol, $precision) = @_;
    $symbol     //= '$';
    $precision  //= 2;
    
    return undef unless defined $number;
    
    # Format with proper decimal places
    my $is_negative = $number < 0;
    $number = abs($number);
    
    my $factor = 10 ** $precision;
    my $rounded = int($number * $factor + 0.5) / $factor;
    
    my $int_part = int($rounded);
    my $dec_part = int(($rounded - $int_part) * $factor + 0.5);
    $dec_part = sprintf("%0${precision}d", $dec_part);
    
    # Add thousands separators
    my $int_str = $int_part;
    $int_str =~ s/(\d)(?=(\d{3})+$)/$1,/g;
    
    my $result = $symbol . $int_str . '.' . $dec_part;
    $result = '-' . $result if $is_negative;
    
    return $result;
}

=head2 format_percentage

Format a number as percentage.

Parameters:
    $number     - The number to format (0.15 = 15%)
    $precision  - Decimal places (default: 0)
    $show_symbol - Whether to show % symbol (default: 1)

Returns:
    Formatted percentage string

Example:
    format_percentage(0.1567)         # "16%"
    format_percentage(0.1567, 2)      # "15.67%"
=cut

sub format_percentage {
    my ($number, $precision, $show_symbol) = @_;
    $precision   //= 0;
    $show_symbol //= 1;
    
    return undef unless defined $number;
    
    my $percent = $number * 100;
    my $formatted = format_number($percent, ',', '.', $precision);
    $formatted .= '%' if $show_symbol;
    
    return $formatted;
}

=head2 format_compact

Format a number in compact notation (K, M, B, T).

Parameters:
    $number     - The number to format
    $precision  - Decimal places (default: 1)

Returns:
    Compact formatted string

Example:
    format_compact(1500000)           # "1.5M"
    format_compact(1234)              # "1.2K"
=cut

sub format_compact {
    my ($number, $precision) = @_;
    $precision //= 1;
    
    return undef unless defined $number;
    return '0' if $number == 0;
    
    my $abs_num = abs($number);
    my $sign = $number < 0 ? '-' : '';
    
    my @suffixes = ('', 'K', 'M', 'B', 'T');
    my $tier = 0;
    
    while ($abs_num >= 1000 && $tier < @suffixes - 1) {
        $abs_num /= 1000;
        $tier++;
    }
    
    my $formatted = sprintf("%.${precision}f", $abs_num);
    $formatted =~ s/\.?0+$// unless $precision > 0;  # Remove trailing zeros
    
    return $sign . $formatted . $suffixes[$tier];
}

=head2 format_ordinal

Convert a number to its ordinal form.

Parameters:
    $number - The number to convert

Returns:
    Ordinal string (1st, 2nd, 3rd, etc.)

Example:
    format_ordinal(1)     # "1st"
    format_ordinal(21)    # "21st"
=cut

sub format_ordinal {
    my ($number) = @_;
    
    return undef unless defined $number && is_integer($number);
    
    my $abs_num = abs($number);
    my $last_digit = $abs_num % 10;
    my $last_two = $abs_num % 100;
    
    my $suffix;
    if ($last_two >= 11 && $last_two <= 13) {
        $suffix = 'th';
    } elsif ($last_digit == 1) {
        $suffix = 'st';
    } elsif ($last_digit == 2) {
        $suffix = 'nd';
    } elsif ($last_digit == 3) {
        $suffix = 'rd';
    } else {
        $suffix = 'th';
    }
    
    return $number . $suffix;
}

=head2 number_to_words

Convert a number to English words.

Parameters:
    $number - The number to convert (supports up to trillions)

Returns:
    Number in words

Example:
    number_to_words(123)      # "one hundred twenty-three"
    number_to_words(1001)     # "one thousand one"
=cut

sub number_to_words {
    my ($number) = @_;
    
    return undef unless defined $number && is_integer($number);
    return 'zero' if $number == 0;
    
    my $is_negative = $number < 0;
    $number = abs($number);
    
    my @parts;
    my $scale_idx = 0;
    
    while ($number > 0) {
        my $chunk = $number % 1000;
        $number = int($number / 1000);
        
        if ($chunk > 0) {
            my $chunk_words = _chunk_to_words($chunk);
            $chunk_words .= ' ' . $SCALES[$scale_idx] if $scale_idx > 0;
            unshift @parts, $chunk_words;
        }
        $scale_idx++;
    }
    
    my $result = join ', ', @parts;
    $result = 'negative ' . $result if $is_negative;
    
    return $result;
}

# Helper: convert a 0-999 chunk to words
sub _chunk_to_words {
    my ($num) = @_;
    
    return '' if $num == 0;
    
    my @words;
    
    # Hundreds
    if ($num >= 100) {
        push @words, $ONES[int($num / 100)] . ' hundred';
        $num %= 100;
    }
    
    # Tens and ones
    if ($num >= 20) {
        my $tens_word = $TENS[int($num / 10) - 2];
        $num %= 10;
        if ($num > 0) {
            $tens_word .= '-' . $ONES[$num];
        }
        push @words, $tens_word;
    } elsif ($num >= 10) {
        push @words, $TEENS[$num - 10];
    } elsif ($num > 0) {
        push @words, $ONES[$num];
    }
    
    return join ' ', @words;
}

# ============================================================================
# Conversion Functions
# ============================================================================

=head2 to_roman

Convert an integer to Roman numeral.

Parameters:
    $number - Integer to convert (1-3999)

Returns:
    Roman numeral string or undef if out of range

Example:
    to_roman(2024)    # "MMXXIV"
=cut

sub to_roman {
    my ($number) = @_;
    
    return undef unless defined $number && is_integer($number);
    return undef if $number < 1 || $number > 3999;
    
    my $result = '';
    
    for my $pair (@ROMAN_PAIRS) {
        my ($value, $symbol) = @$pair;
        while ($number >= $value) {
            $result .= $symbol;
            $number -= $value;
        }
    }
    
    return $result;
}

=head2 from_roman

Convert a Roman numeral to integer.

Parameters:
    $roman - Roman numeral string

Returns:
    Integer value or undef if invalid

Example:
    from_roman("MMXXIV")    # 2024
=cut

sub from_roman {
    my ($roman) = @_;
    
    return undef unless defined $roman;
    $roman = uc($roman);
    
    return undef unless $roman =~ /^[IVXLCDM]+$/;
    
    my $result = 0;
    my $prev_value = 0;
    
    # Process from right to left
    for my $char (reverse split //, $roman) {
        my $value = $ROMAN_MAP{$char};
        return undef unless defined $value;
        
        if ($value < $prev_value) {
            $result -= $value;
        } else {
            $result += $value;
        }
        $prev_value = $value;
    }
    
    # Validate: convert back and compare
    my $check = to_roman($result);
    return undef unless defined $check && uc($check) eq $roman;
    
    return $result;
}

=head2 to_binary

Convert a number to binary string.

Parameters:
    $number     - Number to convert
    $prefix     - Whether to add '0b' prefix (default: 0)
    $min_width  - Minimum width with leading zeros (default: undef)

Returns:
    Binary string

Example:
    to_binary(255)           # "11111111"
    to_binary(255, 1)        # "0b11111111"
=cut

sub to_binary {
    my ($number, $prefix, $min_width) = @_;
    $prefix //= 0;
    
    return undef unless defined $number && is_integer($number);
    return undef if $number < 0;
    
    return '0' . ($prefix ? 'b' : '') if $number == 0;
    
    my $binary = sprintf("%b", $number);
    
    if (defined $min_width && length($binary) < $min_width) {
        $binary = '0' x ($min_width - length($binary)) . $binary;
    }
    
    return ($prefix ? '0b' : '') . $binary;
}

=head2 to_hex

Convert a number to hexadecimal string.

Parameters:
    $number     - Number to convert
    $prefix     - Whether to add '0x' prefix (default: 0)
    $uppercase  - Use uppercase letters (default: 0)
    $min_width  - Minimum width with leading zeros (default: undef)

Returns:
    Hexadecimal string

Example:
    to_hex(255)              # "ff"
    to_hex(255, 1, 1)        # "0xFF"
=cut

sub to_hex {
    my ($number, $prefix, $uppercase, $min_width) = @_;
    $prefix    //= 0;
    $uppercase //= 0;
    
    return undef unless defined $number && is_integer($number);
    return undef if $number < 0;
    
    my $hex = sprintf("%x", $number);
    $hex = uc($hex) if $uppercase;
    
    if (defined $min_width && length($hex) < $min_width) {
        $hex = '0' x ($min_width - length($hex)) . $hex;
    }
    
    return ($prefix ? '0x' : '') . $hex;
}

=head2 to_octal

Convert a number to octal string.

Parameters:
    $number - Number to convert
    $prefix - Whether to add '0' prefix (default: 0)

Returns:
    Octal string

Example:
    to_octal(64)      # "100"
    to_octal(64, 1)   # "0100"
=cut

sub to_octal {
    my ($number, $prefix) = @_;
    $prefix //= 0;
    
    return undef unless defined $number && is_integer($number);
    return undef if $number < 0;
    
    my $octal = sprintf("%o", $number);
    
    return ($prefix ? '0' : '') . $octal;
}

# ============================================================================
# Mathematical Functions
# ============================================================================

=head2 clamp

Clamp a value between min and max.

Parameters:
    $value - Value to clamp
    $min   - Minimum value
    $max   - Maximum value

Returns:
    Clamped value

Example:
    clamp(10, 0, 5)    # 5
    clamp(-5, 0, 10)   # 0
=cut

sub clamp {
    my ($value, $min, $max) = @_;
    
    return undef unless defined $value && defined $min && defined $max;
    
    return $min if $value < $min;
    return $max if $value > $max;
    return $value;
}

=head2 lerp

Linear interpolation between two values.

Parameters:
    $start  - Start value
    $finish - End value
    $t      - Interpolation factor (0.0 to 1.0)

Returns:
    Interpolated value

Example:
    lerp(0, 100, 0.5)    # 50
=cut

sub lerp {
    my ($start, $finish, $t) = @_;
    
    return undef unless defined $start && defined $finish && defined $t;
    
    $t = clamp($t, 0, 1);
    return $start + ($finish - $start) * $t;
}

=head2 map_range

Map a value from one range to another.

Parameters:
    $value  - Value to map
    $in_min - Input range minimum
    $in_max - Input range maximum
    $out_min - Output range minimum
    $out_max - Output range maximum

Returns:
    Mapped value

Example:
    map_range(5, 0, 10, 0, 100)    # 50
=cut

sub map_range {
    my ($value, $in_min, $in_max, $out_min, $out_max) = @_;
    
    return undef unless defined $value && defined $in_min && defined $in_max 
                        && defined $out_min && defined $out_max;
    
    return undef if $in_max == $in_min;
    
    my $t = ($value - $in_min) / ($in_max - $in_min);
    return $out_min + $t * ($out_max - $out_min);
}

=head2 approx_equal

Check if two numbers are approximately equal.

Parameters:
    $a       - First number
    $b       - Second number
    $epsilon - Tolerance (default: 1e-9)

Returns:
    1 if approximately equal, 0 otherwise

Example:
    approx_equal(0.1 + 0.2, 0.3)    # 1 (true)
=cut

sub approx_equal {
    my ($a, $b, $epsilon) = @_;
    $epsilon //= 1e-9;
    
    return undef unless defined $a && defined $b;
    
    return abs($a - $b) < $epsilon;
}

=head2 round_to_multiple

Round a number to the nearest multiple.

Parameters:
    $number  - Number to round
    $multiple - Multiple to round to

Returns:
    Rounded number

Example:
    round_to_multiple(23, 5)    # 25
=cut

sub round_to_multiple {
    my ($number, $multiple) = @_;
    
    return undef unless defined $number && defined $multiple;
    return undef if $multiple == 0;
    
    return int($number / $multiple + 0.5) * $multiple;
}

=head2 round_to_places

Round a number to specified decimal places.

Parameters:
    $number  - Number to round
    $places  - Number of decimal places

Returns:
    Rounded number

Example:
    round_to_places(3.14159, 2)    # 3.14
=cut

sub round_to_places {
    my ($number, $places) = @_;
    
    return undef unless defined $number && defined $places;
    
    my $factor = 10 ** $places;
    return int($number * $factor + 0.5) / $factor;
}

# ============================================================================
# Statistical Functions
# ============================================================================

=head2 mean

Calculate the arithmetic mean of a list of numbers.

Parameters:
    @numbers - List of numbers

Returns:
    Mean value or undef if empty list

Example:
    mean(1, 2, 3, 4, 5)    # 3
=cut

sub mean {
    my (@numbers) = @_;
    
    return undef unless @numbers;
    
    my $sum = 0;
    $sum += $_ for @numbers;
    
    return $sum / scalar(@numbers);
}

=head2 median

Calculate the median of a list of numbers.

Parameters:
    @numbers - List of numbers

Returns:
    Median value or undef if empty list

Example:
    median(1, 2, 3, 4, 5)    # 3
=cut

sub median {
    my (@numbers) = @_;
    
    return undef unless @numbers;
    
    my @sorted = sort { $a <=> $b } @numbers;
    my $count = scalar(@sorted);
    
    if ($count % 2 == 1) {
        return $sorted[int($count / 2)];
    } else {
        return ($sorted[$count / 2 - 1] + $sorted[$count / 2]) / 2;
    }
}

=head2 mode

Calculate the mode (most frequent value) of a list of numbers.

Parameters:
    @numbers - List of numbers

Returns:
    Mode value or undef if empty list

Example:
    mode(1, 2, 2, 3, 3, 3)    # 3
=cut

sub mode {
    my (@numbers) = @_;
    
    return undef unless @numbers;
    
    my %counts;
    $counts{$_}++ for @numbers;
    
    my $max_count = 0;
    my $mode;
    
    for my $num (keys %counts) {
        if ($counts{$num} > $max_count) {
            $max_count = $counts{$num};
            $mode = $num;
        }
    }
    
    return $mode;
}

=head2 std_dev

Calculate the standard deviation of a list of numbers.

Parameters:
    @numbers - List of numbers
    $sample  - Use sample standard deviation (default: 0, population)

Returns:
    Standard deviation or undef if insufficient data

Example:
    std_dev(1, 2, 3, 4, 5)    # ~1.414
=cut

sub std_dev {
    my (@numbers) = @_;
    my $sample = (@numbers && !is_number($numbers[-1])) ? pop(@numbers) : 0;
    
    return undef unless @numbers >= 2;
    
    my $mean_val = mean(@numbers);
    return undef unless defined $mean_val;
    
    my $sum_squared_diff = 0;
    $sum_squared_diff += ($_ - $mean_val) ** 2 for @numbers;
    
    my $divisor = $sample ? scalar(@numbers) - 1 : scalar(@numbers);
    return undef if $divisor == 0;
    
    return sqrt($sum_squared_diff / $divisor);
}

=head2 sum_of_squares

Calculate the sum of squares of a list of numbers.

Parameters:
    @numbers - List of numbers

Returns:
    Sum of squares

Example:
    sum_of_squares(1, 2, 3)    # 14 (1 + 4 + 9)
=cut

sub sum_of_squares {
    my (@numbers) = @_;
    
    my $sum = 0;
    $sum += $_ ** 2 for @numbers;
    
    return $sum;
}

=head2 range

Calculate the range (max - min) of a list of numbers.

Parameters:
    @numbers - List of numbers

Returns:
    Range value or undef if empty list

Example:
    range(1, 2, 3, 4, 5)    # 4
=cut

sub range {
    my (@numbers) = @_;
    
    return undef unless @numbers;
    
    my $min = $numbers[0];
    my $max = $numbers[0];
    
    for my $num (@numbers) {
        $min = $num if $num < $min;
        $max = $num if $num > $max;
    }
    
    return $max - $min;
}

# ============================================================================
# Validation Functions
# ============================================================================

=head2 is_number

Check if a value is a number.

Parameters:
    $value - Value to check

Returns:
    1 if number, 0 otherwise
=cut

sub is_number {
    my ($value) = @_;
    
    return 0 unless defined $value;
    return 0 if ref($value);
    
    return $value =~ /^-?[\d.]+([eE][+-]?\d+)?$/ ? 1 : 0;
}

=head2 is_integer

Check if a value is an integer.

Parameters:
    $value - Value to check

Returns:
    1 if integer, 0 otherwise
=cut

sub is_integer {
    my ($value) = @_;
    
    return 0 unless defined $value;
    return 0 if ref($value);
    
    # Check if it's a number first
    return 0 unless is_number($value);
    
    # Check if it has no decimal part
    return $value == int($value) ? 1 : 0;
}

=head2 is_float

Check if a value is a floating point number.

Parameters:
    $value - Value to check

Returns:
    1 if float, 0 otherwise
=cut

sub is_float {
    my ($value) = @_;
    
    return 0 unless is_number($value);
    return 0 if ref($value);
    
    # Check if it has decimal part or is in scientific notation
    my $str = "$value";
    return ($str =~ /\./ || $str =~ /[eE]/) ? 1 : 0;
}

=head2 is_even

Check if a number is even.

Parameters:
    $number - Number to check

Returns:
    1 if even, 0 otherwise
=cut

sub is_even {
    my ($number) = @_;
    
    return 0 unless is_integer($number);
    return $number % 2 == 0 ? 1 : 0;
}

=head2 is_odd

Check if a number is odd.

Parameters:
    $number - Number to check

Returns:
    1 if odd, 0 otherwise
=cut

sub is_odd {
    my ($number) = @_;
    
    return 0 unless is_integer($number);
    return $number % 2 != 0 ? 1 : 0;
}

=head2 is_positive

Check if a number is positive.

Parameters:
    $number - Number to check

Returns:
    1 if positive, 0 otherwise
=cut

sub is_positive {
    my ($number) = @_;
    
    return 0 unless is_number($number);
    return $number > 0 ? 1 : 0;
}

=head2 is_negative

Check if a number is negative.

Parameters:
    $number - Number to check

Returns:
    1 if negative, 0 otherwise
=cut

sub is_negative {
    my ($number) = @_;
    
    return 0 unless is_number($number);
    return $number < 0 ? 1 : 0;
}

=head2 is_zero

Check if a number is zero.

Parameters:
    $number - Number to check

Returns:
    1 if zero, 0 otherwise
=cut

sub is_zero {
    my ($number) = @_;
    
    return 0 unless is_number($number);
    return $number == 0 ? 1 : 0;
}

=head2 is_between

Check if a number is within a range (inclusive).

Parameters:
    $number - Number to check
    $min    - Minimum value
    $max    - Maximum value

Returns:
    1 if in range, 0 otherwise
=cut

sub is_between {
    my ($number, $min, $max) = @_;
    
    return 0 unless is_number($number) && is_number($min) && is_number($max);
    return ($number >= $min && $number <= $max) ? 1 : 0;
}

=head2 is_prime

Check if a number is prime.

Parameters:
    $number - Number to check

Returns:
    1 if prime, 0 otherwise
=cut

sub is_prime {
    my ($number) = @_;
    
    return 0 unless is_integer($number);
    return 0 if $number < 2;
    return 1 if $number == 2;
    return 0 if is_even($number);
    
    for (my $i = 3; $i <= sqrt($number); $i += 2) {
        return 0 if $number % $i == 0;
    }
    
    return 1;
}

=head2 is_perfect_square

Check if a number is a perfect square.

Parameters:
    $number - Number to check

Returns:
    1 if perfect square, 0 otherwise
=cut

sub is_perfect_square {
    my ($number) = @_;
    
    return 0 unless is_integer($number);
    return 0 if $number < 0;
    
    my $sqrt_val = int(sqrt($number));
    return $sqrt_val * $sqrt_val == $number ? 1 : 0;
}

# ============================================================================
# Parsing Functions
# ============================================================================

=head2 parse_number

Parse a string to a number.

Parameters:
    $str     - String to parse
    $default - Default value if parsing fails (default: undef)

Returns:
    Parsed number or default value
=cut

sub parse_number {
    my ($str, $default) = @_;
    
    return $default unless defined $str;
    
    # Remove thousands separators and normalize decimal
    $str =~ s/,//g;
    
    return $default unless $str =~ /^-?[\d.]+([eE][+-]?\d+)?$/;
    
    return $str + 0;  # Force numeric context
}

=head2 parse_int

Parse a string to an integer.

Parameters:
    $str     - String to parse
    $default - Default value if parsing fails (default: undef)
    $base    - Number base (default: 10)

Returns:
    Parsed integer or default value
=cut

sub parse_int {
    my ($str, $default, $base) = @_;
    $base //= 10;
    
    return $default unless defined $str;
    
    # Remove thousands separators
    $str =~ s/,//g;
    
    # Check if it's a valid integer string
    return $default unless $str =~ /^-?\d+$/;
    
    my $result = eval { int($str) };
    return $default if $@;
    return defined $result ? $result : $default;
}

=head2 parse_float

Parse a string to a floating point number.

Parameters:
    $str     - String to parse
    $default - Default value if parsing fails (default: undef)

Returns:
    Parsed float or default value
=cut

sub parse_float {
    my ($str, $default) = @_;
    
    return $default unless defined $str;
    
    # Remove thousands separators
    $str =~ s/,//g;
    
    my $result = eval { $str + 0.0 };
    return defined $result ? $result : $default;
}

# ============================================================================
# Utility Functions
# ============================================================================

=head2 gcd

Calculate the greatest common divisor of two numbers.

Parameters:
    $a - First number
    $b - Second number

Returns:
    GCD value

Example:
    gcd(24, 36)    # 12
=cut

sub gcd {
    my ($a, $b) = @_;
    
    return undef unless is_integer($a) && is_integer($b);
    
    $a = abs($a);
    $b = abs($b);
    
    while ($b != 0) {
        my $temp = $b;
        $b = $a % $b;
        $a = $temp;
    }
    
    return $a;
}

=head2 lcm

Calculate the least common multiple of two numbers.

Parameters:
    $a - First number
    $b - Second number

Returns:
    LCM value

Example:
    lcm(4, 6)    # 12
=cut

sub lcm {
    my ($a, $b) = @_;
    
    return undef unless is_integer($a) && is_integer($b);
    return 0 if $a == 0 || $b == 0;
    
    return abs($a * $b) / gcd($a, $b);
}

=head2 factorial

Calculate the factorial of a number.

Parameters:
    $n - Non-negative integer

Returns:
    Factorial value or undef if invalid

Example:
    factorial(5)    # 120
=cut

sub factorial {
    my ($n) = @_;
    
    return undef unless is_integer($n);
    return undef if $n < 0;
    return 1 if $n == 0;
    
    my $result = 1;
    $result *= $_ for (1 .. $n);
    
    return $result;
}

=head2 fibonacci

Calculate the nth Fibonacci number.

Parameters:
    $n - Index (0-based)

Returns:
    Fibonacci number or undef if invalid

Example:
    fibonacci(10)    # 55
=cut

sub fibonacci {
    my ($n) = @_;
    
    return undef unless is_integer($n);
    return undef if $n < 0;
    return $n if $n <= 1;
    
    my ($a, $b) = (0, 1);
    for (2 .. $n) {
        ($a, $b) = ($b, $a + $b);
    }
    
    return $b;
}

=head2 sqrt

Calculate the square root of a number.

Parameters:
    $number - Number to calculate

Returns:
    Square root or undef if negative
=cut

sub sqrt {
    my ($number) = @_;
    
    return undef unless is_number($number);
    return undef if $number < 0;
    
    return CORE::sqrt($number);
}

=head2 nth_root

Calculate the nth root of a number.

Parameters:
    $number - Number to calculate
    $n      - Root degree

Returns:
    Nth root or undef if invalid

Example:
    nth_root(27, 3)    # 3
=cut

sub nth_root {
    my ($number, $n) = @_;
    
    return undef unless is_number($number) && is_integer($n);
    return undef if $n == 0;
    return undef if $number < 0 && $n % 2 == 0;
    
    # Handle negative numbers with odd roots
    if ($number < 0) {
        return -((-$number) ** (1 / $n));
    }
    
    return $number ** (1 / $n);
}

=head2 to_radians

Convert degrees to radians.

Parameters:
    $degrees - Angle in degrees

Returns:
    Angle in radians
=cut

sub to_radians {
    my ($degrees) = @_;
    
    return undef unless is_number($degrees);
    return $degrees * 3.14159265358979323846 / 180;
}

=head2 to_degrees

Convert radians to degrees.

Parameters:
    $radians - Angle in radians

Returns:
    Angle in degrees
=cut

sub to_degrees {
    my ($radians) = @_;
    
    return undef unless is_number($radians);
    return $radians * 180 / 3.14159265358979323846;
}

=head2 normalize_angle

Normalize an angle to 0-360 degrees.

Parameters:
    $degrees - Angle in degrees

Returns:
    Normalized angle (0-360)
=cut

sub normalize_angle {
    my ($degrees) = @_;
    
    return undef unless is_number($degrees);
    
    my $normalized = $degrees % 360;
    $normalized += 360 if $normalized < 0;
    
    return $normalized;
}

=head2 sum_of_digits

Calculate the sum of digits of a number.

Parameters:
    $number - Number to process

Returns:
    Sum of digits

Example:
    sum_of_digits(12345)    # 15
=cut

sub sum_of_digits {
    my ($number) = @_;
    
    return undef unless is_integer($number);
    
    my $sum = 0;
    my $n = abs($number);
    
    while ($n > 0) {
        $sum += $n % 10;
        $n = int($n / 10);
    }
    
    return $sum;
}

=head2 reverse_digits

Reverse the digits of a number.

Parameters:
    $number - Number to process

Returns:
    Reversed number

Example:
    reverse_digits(12345)    # 54321
=cut

sub reverse_digits {
    my ($number) = @_;
    
    return undef unless is_integer($number);
    
    my $is_negative = $number < 0;
    my $n = abs($number);
    my $reversed = 0;
    
    while ($n > 0) {
        $reversed = $reversed * 10 + ($n % 10);
        $n = int($n / 10);
    }
    
    return $is_negative ? -$reversed : $reversed;
}

=head2 is_palindrome

Check if a number is a palindrome.

Parameters:
    $number - Number to check

Returns:
    1 if palindrome, 0 otherwise

Example:
    is_palindrome(121)    # 1 (true)
=cut

sub is_palindrome {
    my ($number) = @_;
    
    return 0 unless is_integer($number);
    return $number == reverse_digits($number) ? 1 : 0;
}

# ============================================================================
# Random Generation
# ============================================================================

=head2 random

Generate a random float between min and max.

Parameters:
    $min - Minimum value (default: 0)
    $max - Maximum value (default: 1)

Returns:
    Random float
=cut

sub random {
    my ($min, $max) = @_;
    $min //= 0;
    $max //= 1;
    
    return $min + rand() * ($max - $min);
}

=head2 random_int

Generate a random integer between min and max (inclusive).

Parameters:
    $min - Minimum value
    $max - Maximum value

Returns:
    Random integer
=cut

sub random_int {
    my ($min, $max) = @_;
    
    return undef unless is_integer($min) && is_integer($max);
    return undef if $min > $max;
    
    return $min + int(rand($max - $min + 1));
}

=head2 random_normal

Generate a random number from normal distribution.

Parameters:
    $mean    - Mean value (default: 0)
    $std_dev - Standard deviation (default: 1)

Returns:
    Random number from normal distribution
=cut

sub random_normal {
    my ($mean, $std_dev) = @_;
    $mean    //= 0;
    $std_dev //= 1;
    
    # Box-Muller transform
    my $u1 = rand();
    my $u2 = rand();
    
    my $z = sqrt(-2 * log($u1)) * cos(2 * 3.14159265358979323846 * $u2);
    
    return $mean + $std_dev * $z;
}

1;

__END__

=head1 NAME

NumberUtils - Comprehensive number manipulation utilities for Perl

=head1 SYNOPSIS

    use NumberUtils;
    
    # Formatting
    my $formatted = format_number(1234567.89);
    my $currency = format_currency(1234.5, '$', 2);
    my $percent = format_percentage(0.1567, 2);
    
    # Conversion
    my $roman = to_roman(2024);           # "MMXXIV"
    my $number = from_roman("MMXXIV");    # 2024
    my $binary = to_binary(255);          # "11111111"
    
    # Mathematics
    my $clamped = clamp(10, 0, 5);        # 5
    my $lerped = lerp(0, 100, 0.5);       # 50
    
    # Statistics
    my $avg = mean(1, 2, 3, 4, 5);        # 3
    my $med = median(1, 2, 3, 4, 5);      # 3
    
    # Validation
    if (is_prime(17)) { ... }
    if (is_between($x, 0, 100)) { ... }

=head1 DESCRIPTION

NumberUtils provides a comprehensive set of number manipulation, formatting,
conversion, validation, and mathematical functions for Perl with zero dependencies.

=head1 FUNCTIONS

See inline documentation for detailed function descriptions.

=head1 AUTHOR

AllToolkit Contributors

=head1 LICENSE

MIT License

=cut

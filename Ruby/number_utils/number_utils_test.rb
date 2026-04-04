#!/usr/bin/env ruby
# Number Utilities Test Suite
# Run with: ruby number_utils_test.rb

require_relative 'mod'

class NumberUtilsTest
  def initialize
    @tests = 0
    @passed = 0
    @failed = 0
  end

  def run
    puts "Running NumberUtils Test Suite..."
    puts "=" * 60

    test_formatting
    test_conversion
    test_mathematical
    test_statistical
    test_validation
    test_parsing
    test_utility

    puts "=" * 60
    puts "Results: #{@passed} passed, #{@failed} failed, #{@tests} total"
    exit(@failed > 0 ? 1 : 0)
  end

  private

  def assert_equal(expected, actual, message = nil)
    @tests += 1
    if expected == actual
      @passed += 1
      print "."
    else
      @failed += 1
      puts "\nFAILED: #{message || 'Assertion failed'}"
      puts "  Expected: #{expected.inspect}"
      puts "  Actual:   #{actual.inspect}"
    end
  end

  def assert_true(actual, message = nil)
    assert_equal(true, actual, message)
  end

  def assert_false(actual, message = nil)
    assert_equal(false, actual, message)
  end

  def assert_nil(actual, message = nil)
    assert_equal(nil, actual, message)
  end

  def test_formatting
    puts "\nTesting Formatting..."

    assert_equal("1,234,567.89", AllToolkit::NumberUtils.format(1234567.89), "format")
    assert_equal("1 234 567,89", AllToolkit::NumberUtils.format(1234567.89, separator: ' ', decimal: ','), "format custom")
    assert_equal("1,234,568", AllToolkit::NumberUtils.format(1234567.89, precision: 0), "format precision")
    assert_nil(AllToolkit::NumberUtils.format(nil), "format nil")

    assert_equal("$1,234.50", AllToolkit::NumberUtils.currency(1234.5), "currency")
    assert_equal("€1,234.50", AllToolkit::NumberUtils.currency(1234.5, symbol: '€'), "currency euro")
    assert_nil(AllToolkit::NumberUtils.currency(nil), "currency nil")

    assert_equal("16%", AllToolkit::NumberUtils.percentage(0.1567), "percentage")
    assert_equal("15.67%", AllToolkit::NumberUtils.percentage(0.1567, precision: 2), "percentage precision")
    assert_nil(AllToolkit::NumberUtils.percentage(nil), "percentage nil")

    assert_equal("1.5K", AllToolkit::NumberUtils.compact(1500), "compact K")
    assert_equal("1.5M", AllToolkit::NumberUtils.compact(1_500_000), "compact M")
    assert_equal("1.5B", AllToolkit::NumberUtils.compact(1_500_000_000), "compact B")
    assert_equal("-1.5K", AllToolkit::NumberUtils.compact(-1500), "compact negative")
    assert_equal("0", AllToolkit::NumberUtils.compact(0), "compact zero")

    assert_equal("1st", AllToolkit::NumberUtils.ordinal(1), "ordinal 1st")
    assert_equal("2nd", AllToolkit::NumberUtils.ordinal(2), "ordinal 2nd")
    assert_equal("3rd", AllToolkit::NumberUtils.ordinal(3), "ordinal 3rd")
    assert_equal("11th", AllToolkit::NumberUtils.ordinal(11), "ordinal 11th")
    assert_equal("21st", AllToolkit::NumberUtils.ordinal(21), "ordinal 21st")
    assert_nil(AllToolkit::NumberUtils.ordinal(nil), "ordinal nil")

    assert_equal("zero", AllToolkit::NumberUtils.to_words(0), "words zero")
    assert_equal("one", AllToolkit::NumberUtils.to_words(1), "words one")
    assert_equal("twenty-one", AllToolkit::NumberUtils.to_words(21), "words 21")
    assert_equal("one hundred twenty-three", AllToolkit::NumberUtils.to_words(123), "words 123")
    assert_equal("negative five", AllToolkit::NumberUtils.to_words(-5), "words negative")
  end

  def test_conversion
    puts "\nTesting Conversion..."

    assert_equal("I", AllToolkit::NumberUtils.to_roman(1), "roman 1")
    assert_equal("IV", AllToolkit::NumberUtils.to_roman(4), "roman 4")
    assert_equal("MMXXIV", AllToolkit::NumberUtils.to_roman(2024), "roman 2024")
    assert_equal(1, AllToolkit::NumberUtils.from_roman("I"), "from roman I")
    assert_equal(2024, AllToolkit::NumberUtils.from_roman("MMXXIV"), "from roman MMXXIV")
    assert_nil(AllToolkit::NumberUtils.to_roman(0), "roman 0")
    assert_nil(AllToolkit::NumberUtils.from_roman("INVALID"), "from roman invalid")

    assert_equal("1010", AllToolkit::NumberUtils.to_binary(10), "binary")
    assert_equal("0b1010", AllToolkit::NumberUtils.to_binary(10, prefix: true), "binary prefix")
    assert_nil(AllToolkit::NumberUtils.to_binary(nil), "binary nil")

    assert_equal("ff", AllToolkit::NumberUtils.to_hex(255), "hex")
    assert_equal("FF", AllToolkit::NumberUtils.to_hex(255, uppercase: true), "hex upper")
    assert_equal("0xff", AllToolkit::NumberUtils.to_hex(255, prefix: true), "hex prefix")

    assert_equal("377", AllToolkit::NumberUtils.to_octal(255), "octal")
  end

  def test_mathematical
    puts "\nTesting Mathematical Functions..."

    assert_equal(5, AllToolkit::NumberUtils.clamp(10, 0, 5), "clamp upper")
    assert_equal(0, AllToolkit::NumberUtils.clamp(-5, 0, 5), "clamp lower")
    assert_equal(3, AllToolkit::NumberUtils.clamp(3, 0, 5), "clamp middle")
    assert_nil(AllToolkit::NumberUtils.clamp(nil, 0, 5), "clamp nil")

    assert_equal(50.0, AllToolkit::NumberUtils.lerp(0, 100, 0.5), "lerp")
    assert_nil(AllToolkit::NumberUtils.lerp(nil, 100, 0.5), "lerp nil")

    assert_equal(50.0, AllToolkit::NumberUtils.map_range(5, 0, 10, 0, 100), "map_range")
    assert_nil(AllToolkit::NumberUtils.map_range(nil, 0, 10, 0, 100), "map_range nil")

    assert_true(AllToolkit::NumberUtils.approx_equal?(1.0, 1.000000001), "approx_equal")
    assert_false(AllToolkit::NumberUtils.approx_equal?(1.0, 2.0), "approx_equal false")

    assert_equal(10, AllToolkit::NumberUtils.round_to_multiple(12, 5), "round_to_multiple")
    assert_equal(3.14, AllToolkit::NumberUtils.round_to_places(3.14159, 2), "round_to_places")
  end

  def test_statistical
    puts "\nTesting Statistical Functions..."

    assert_equal(3.0, AllToolkit::NumberUtils.mean([1, 2, 3, 4, 5]), "mean")
    assert_nil(AllToolkit::NumberUtils.mean([]), "mean empty")

    assert_equal(3, AllToolkit::NumberUtils.median([1, 2, 3, 4, 5]), "median odd")
    assert_equal(3.5, AllToolkit::NumberUtils.median([1, 2, 4, 5]), "median even")
    assert_nil(AllToolkit::NumberUtils.median([]), "median empty")

    assert_equal([2], AllToolkit::NumberUtils.mode([1, 2, 2, 3]), "mode")
    assert_nil(AllToolkit::NumberUtils.mode([]), "mode empty")

    assert_true(AllToolkit::NumberUtils.std_dev([1, 2, 3, 4, 5]) > 1.4, "std_dev")
    assert_nil(AllToolkit::NumberUtils.std_dev([]), "std_dev empty")

    assert_equal(4, AllToolkit::NumberUtils.range([1, 2, 3, 5]), "range")
    assert_nil(AllToolkit::NumberUtils.range([]), "range empty")
  end

  def test_validation
    puts "\nTesting Validation Functions..."

    assert_true(AllToolkit::NumberUtils.number?(42), "number? int")
    assert_true(AllToolkit::NumberUtils.number?(3.14), "number? float")
    assert_false(AllToolkit::NumberUtils.number?("42"), "number? string")

    assert_true(AllToolkit::NumberUtils.integer?(42), "integer?")
    assert_false(AllToolkit::NumberUtils.integer?(3.14), "integer? false")

    assert_true(AllToolkit::NumberUtils.even?(4), "even?")
    assert_false(AllToolkit::NumberUtils.even?(5), "even? false")

    assert_true(AllToolkit::NumberUtils.odd?(5), "odd?")
    assert_false(AllToolkit::NumberUtils.odd?(4), "odd? false")

    assert_true(AllToolkit::NumberUtils.positive?(5), "positive?")
    assert_false(AllToolkit::NumberUtils.positive?(-5), "positive? false")

    assert_true(AllToolkit::NumberUtils.negative?(-5), "negative?")
    assert_false(AllToolkit::NumberUtils.negative?(5), "negative? false")

    assert_true(AllToolkit::NumberUtils.zero?(0), "zero?")
    assert_false(AllToolkit::NumberUtils.zero?(5), "zero? false")

    assert_true(AllToolkit::NumberUtils.between?(3, 1, 5), "between?")
    assert_false(AllToolkit::NumberUtils.between?(10, 1, 5), "between? false")

    assert_true(AllToolkit::NumberUtils.prime?(7), "prime?")
    assert_false(AllToolkit::NumberUtils.prime?(4), "prime? false")
    assert_false(AllToolkit::NumberUtils.prime?(1), "prime? 1")

    assert_true(AllToolkit::NumberUtils.perfect_square?(16), "perfect_square?")
    assert_false(AllToolkit::NumberUtils.perfect_square?(15), "perfect_square? false")
  end

  def test_parsing
    puts "\nTesting Parsing Functions..."

    assert_equal(42, AllToolkit::NumberUtils.parse("42"), "parse int")
    assert_equal(3.14, AllToolkit::NumberUtils.parse("3.14"), "parse float")
    assert_equal(1000, AllToolkit::NumberUtils.parse("1,000"), "parse with comma")
    assert_nil(AllToolkit::NumberUtils.parse("invalid"), "parse invalid")
    assert_nil(AllToolkit::NumberUtils.parse(nil), "parse nil")

    assert_equal(42, AllToolkit::NumberUtils.parse_int("42"), "parse_int")
    assert_nil(AllToolkit::NumberUtils.parse_int("3.14"), "parse_int float")

    assert_equal(3.14, AllToolkit::NumberUtils.parse_float("3.14"), "parse_float")
    assert_nil(AllToolkit::NumberUtils.parse_float(nil), "parse_float nil")
  end

  def test_utility
    puts "\nTesting Utility Functions..."

    assert_equal(12, AllToolkit::NumberUtils.gcd(24, 36), "gcd")
    assert_equal(72, AllToolkit::NumberUtils.lcm(24, 36), "lcm")

    assert_equal(120, AllToolkit::NumberUtils.factorial(5), "factorial")
    assert_nil(AllToolkit::NumberUtils.factorial(-1), "factorial negative")

    assert_equal(8, AllToolkit::NumberUtils.fibonacci(6), "fibonacci")
    assert_equal(0, AllToolkit::NumberUtils.fibonacci(0), "fibonacci 0")

    assert_equal(4.0, AllToolkit::NumberUtils.sqrt(16), "sqrt")
    assert_nil(AllToolkit::NumberUtils.sqrt(-1), "sqrt negative")

    assert_equal(2.0, AllToolkit::NumberUtils.nth_root(8, 3), "nth_root")

    assert_equal(Math::PI, AllToolkit::NumberUtils.to_radians(180), "to_radians")
    assert_equal(180.0, AllToolkit::NumberUtils.to_degrees(Math::PI), "to_degrees")

    assert_equal(90.0, AllToolkit::NumberUtils.normalize_angle(450), "normalize_angle")

    assert_equal(6, AllToolkit::NumberUtils.sum_of_digits(123), "sum_of_digits")
    assert_equal(321, AllToolkit::NumberUtils.reverse_digits(123), "reverse_digits")

    assert_true(AllToolkit::NumberUtils.palindrome?(121), "palindrome?")
    assert_false(AllToolkit::NumberUtils.palindrome?(123), "palindrome? false")
  end
end

# Run tests if executed directly
if __FILE__ == $0
  NumberUtilsTest.new.run
end

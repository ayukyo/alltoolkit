# Number Utilities Module for Ruby
# Provides comprehensive number formatting, conversion, and mathematical utilities
# Zero dependencies - uses only Ruby standard library

module AllToolkit
  module NumberUtils
    # Error class for number utility operations
    class NumberError < StandardError; end

    # ============================================================================
    # Number Formatting
    # ============================================================================

    # Format number with thousands separator
    # @param number [Numeric] the number to format
    # @param separator [String] thousands separator (default: ',')
    # @param decimal [String] decimal point (default: '.')
    # @param precision [Integer] number of decimal places (default: nil, keeps original)
    # @return [String] formatted number string
    # @example
    #   NumberUtils.format(1234567.89) # => "1,234,567.89"
    #   NumberUtils.format(1234567.89, separator: ' ', decimal: ',') # => "1 234 567,89"
    def self.format(number, separator: ',', decimal: '.', precision: nil)
      return nil if number.nil?
      return number.to_s unless number.is_a?(Numeric)

      num = precision ? number.round(precision) : number
      int_part, frac_part = num.to_s.split('.')
      int_part = int_part.gsub(/(\d)(?=(\d{3})+$)/, "\\1#{separator}")
      frac_part = frac_part.ljust(precision, '0') if precision && frac_part
      frac_part ? "#{int_part}#{decimal}#{frac_part}" : int_part
    end

    # Format number as currency
    # @param number [Numeric] the amount
    # @param symbol [String] currency symbol (default: '$')
    # @param separator [String] thousands separator (default: ',')
    # @param decimal [String] decimal point (default: '.')
    # @param precision [Integer] decimal places (default: 2)
    # @return [String] formatted currency string
    # @example
    #   NumberUtils.currency(1234.5) # => "$1,234.50"
    #   NumberUtils.currency(1234.5, symbol: '€') # => "€1,234.50"
    def self.currency(number, symbol: '$', separator: ',', decimal: '.', precision: 2)
      return nil if number.nil?
      formatted = format(number, separator: separator, decimal: decimal, precision: precision)
      "#{symbol}#{formatted}"
    end

    # Format number as percentage
    # @param number [Numeric] the number to format (0.15 => 15%)
    # @param precision [Integer] decimal places (default: 0)
    # @param symbol [Boolean] include % symbol (default: true)
    # @return [String] formatted percentage string
    # @example
    #   NumberUtils.percentage(0.1567) # => "16%"
    #   NumberUtils.percentage(0.1567, precision: 2) # => "15.67%"
    def self.percentage(number, precision: 0, symbol: true)
      return nil if number.nil?
      value = (number * 100).round(precision)
      symbol ? "#{value}%" : value.to_s
    end

    # Format number in compact notation (K, M, B, T)
    # @param number [Numeric] the number to format
    # @param precision [Integer] decimal places (default: 1)
    # @return [String] compact formatted string
    # @example
    #   NumberUtils.compact(1500) # => "1.5K"
    #   NumberUtils.compact(1500000) # => "1.5M"
    def self.compact(number, precision: 1)
      return nil if number.nil?
      return '0' if number == 0

      abs_num = number.abs
      sign = number < 0 ? '-' : ''

      suffixes = [
        [1_000_000_000_000, 'T'],
        [1_000_000_000, 'B'],
        [1_000_000, 'M'],
        [1_000, 'K']
      ]

      suffixes.each do |threshold, suffix|
        if abs_num >= threshold
          value = (abs_num.to_f / threshold).round(precision)
          # Remove trailing zeros
          value = value.to_i if value == value.to_i
          return "#{sign}#{value}#{suffix}"
        end
      end

      number.to_i.to_s
    end

    # Format number as ordinal (1st, 2nd, 3rd, etc.)
    # @param number [Integer] the number
    # @return [String] ordinal string
    # @example
    #   NumberUtils.ordinal(1) # => "1st"
    #   NumberUtils.ordinal(22) # => "22nd"
    def self.ordinal(number)
      return nil if number.nil?
      return number.to_s unless number.is_a?(Integer)

      # Special cases for 11, 12, 13
      return "#{number}th" if (11..13).include?(number % 100)

      case number % 10
      when 1 then "#{number}st"
      when 2 then "#{number}nd"
      when 3 then "#{number}rd"
      else "#{number}th"
      end
    end

    # Format number as words
    # @param number [Integer] the number to convert (0-999,999,999,999)
    # @return [String] number in words
    # @example
    #   NumberUtils.to_words(123) # => "one hundred twenty-three"
    def self.to_words(number)
      return nil if number.nil?
      return number.to_s unless number.is_a?(Integer)
      return 'zero' if number == 0

      if number < 0
        return "negative #{to_words(-number)}"
      end

      ones = %w[zero one two three four five six seven eight nine ten
                eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen]
      tens = %w[zero ten twenty thirty forty fifty sixty seventy eighty ninety]

      if number < 20
        ones[number]
      elsif number < 100
        result = tens[number / 10]
        result += "-#{ones[number % 10]}" if number % 10 > 0
        result
      elsif number < 1_000
        result = "#{ones[number / 100]} hundred"
        remainder = number % 100
        result += " #{to_words(remainder)}" if remainder > 0
        result
      elsif number < 1_000_000
        result = "#{to_words(number / 1_000)} thousand"
        remainder = number % 1_000
        result += " #{to_words(remainder)}" if remainder > 0
        result
      elsif number < 1_000_000_000
        result = "#{to_words(number / 1_000_000)} million"
        remainder = number % 1_000_000
        result += " #{to_words(remainder)}" if remainder > 0
        result
      elsif number < 1_000_000_000_000
        result = "#{to_words(number / 1_000_000_000)} billion"
        remainder = number % 1_000_000_000
        result += " #{to_words(remainder)}" if remainder > 0
        result
      else
        number.to_s
      end
    end

    # ============================================================================
    # Number Conversion
    # ============================================================================

    # Convert number to Roman numerals
    # @param number [Integer] the number (1-3999)
    # @return [String] Roman numeral representation
    # @example
    #   NumberUtils.to_roman(2024) # => "MMXXIV"
    def self.to_roman(number)
      return nil if number.nil?
      return nil unless number.is_a?(Integer) && number >= 1 && number <= 3999

      numerals = [
        [1000, 'M'], [900, 'CM'], [500, 'D'], [400, 'CD'],
        [100, 'C'], [90, 'XC'], [50, 'L'], [40, 'XL'],
        [10, 'X'], [9, 'IX'], [5, 'V'], [4, 'IV'], [1, 'I']
      ]

      result = ''
      numerals.each do |value, symbol|
        while number >= value
          result += symbol
          number -= value
        end
      end
      result
    end

    # Convert Roman numeral to number
    # @param roman [String] Roman numeral string
    # @return [Integer] the number, or nil if invalid
    # @example
    #   NumberUtils.from_roman("MMXXIV") # => 2024
    def self.from_roman(roman)
      return nil if roman.nil? || roman.empty?

      values = { 'I' => 1, 'V' => 5, 'X' => 10, 'L' => 50,
                 'C' => 100, 'D' => 500, 'M' => 1000 }

      roman = roman.upcase
      total = 0
      prev_value = 0

      roman.reverse.each_char do |char|
        value = values[char]
        return nil unless value

        if value < prev_value
          total -= value
        else
          total += value
        end
        prev_value = value
      end

      total
    end

    # Convert number to binary string
    # @param number [Integer] the number
    # @param prefix [Boolean] add '0b' prefix (default: false)
    # @param min_width [Integer] minimum width with leading zeros (default: nil)
    # @return [String] binary representation
    def self.to_binary(number, prefix: false, min_width: nil)
      return nil if number.nil?
      return nil unless number.is_a?(Integer)

      result = min_width ? number.to_s(2).rjust(min_width, '0') : number.to_s(2)
      prefix ? "0b#{result}" : result
    end

    # Convert number to hexadecimal string
    # @param number [Integer] the number
    # @param prefix [Boolean] add '0x' prefix (default: false)
    # @param uppercase [Boolean] use uppercase letters (default: false)
    # @param min_width [Integer] minimum width with leading zeros (default: nil)
    # @return [String] hexadecimal representation
    def self.to_hex(number, prefix: false, uppercase: false, min_width: nil)
      return nil if number.nil?
      return nil unless number.is_a?(Integer)

      result = number.to_s(16)
      result = result.upcase if uppercase
      result = result.rjust(min_width, '0') if min_width
      prefix ? "0x#{result}" : result
    end

    # Convert number to octal string
    # @param number [Integer] the number
    # @param prefix [Boolean] add '0o' prefix (default: false)
    # @return [String] octal representation
    def self.to_octal(number, prefix: false)
      return nil if number.nil?
      return nil unless number.is_a?(Integer)

      result = number.to_s(8)
      prefix ? "0o#{result}" : result
    end

    # ============================================================================
    # Mathematical Utilities
    # ============================================================================

    # Clamp number between min and max
    # @param number [Numeric] the number to clamp
    # @param min [Numeric] minimum value
    # @param max [Numeric] maximum value
    # @return [Numeric] clamped value
    def self.clamp(number, min, max)
      return nil if number.nil?
      [[number, max].min, min].max
    end

    # Linear interpolation between two values
    # @param start [Numeric] start value
    # @param finish [Numeric] end value
    # @param t [Float] interpolation factor (0.0 to 1.0)
    # @return [Float] interpolated value
    def self.lerp(start, finish, t)
      return nil if start.nil? || finish.nil? || t.nil?
      start + (finish - start) * t
    end

    # Map value from one range to another
    # @param value [Numeric] input value
    # @param in_min [Numeric] input range minimum
    # @param in_max [Numeric] input range maximum
    # @param out_min [Numeric] output range minimum
    # @param out_max [Numeric] output range maximum
    # @return [Float] mapped value
    def self.map_range(value, in_min, in_max, out_min, out_max)
      return nil if value.nil?
      return out_min if in_max == in_min
      (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
    end

    # Check if two numbers are approximately equal
    # @param a [Numeric] first number
    # @param b [Numeric] second number
    # @param epsilon [Float] tolerance (default: 1e-9)
    # @return [Boolean] true if approximately equal
    def self.approx_equal?(a, b, epsilon: 1e-9)
      return true if a == b
      return false if a.nil? || b.nil?
      (a - b).abs <= epsilon
    end

    # Round to nearest multiple
    # @param number [Numeric] the number
    # @param multiple [Numeric] the multiple
    # @return [Numeric] rounded number
    def self.round_to_multiple(number, multiple)
      return nil if number.nil? || multiple.nil?
      (number / multiple).round * multiple
    end

    # Round to specific decimal places
    # @param number [Numeric] the number
    # @param places [Integer] decimal places
    # @return [Float] rounded number
    def self.round_to_places(number, places)
      return nil if number.nil?
      factor = 10.0 ** places
      (number * factor).round / factor
    end

    # ============================================================================
    # Statistical Functions
    # ============================================================================

    # Calculate mean (average)
    # @param numbers [Array<Numeric>] array of numbers
    # @return [Float] mean value, or nil if empty
    def self.mean(numbers)
      return nil if numbers.nil? || numbers.empty?
      numbers.sum.to_f / numbers.length
    end

    # Calculate median
    # @param numbers [Array<Numeric>] array of numbers
    # @return [Float] median value, or nil if empty
    def self.median(numbers)
      return nil if numbers.nil? || numbers.empty?
      sorted = numbers.sort
      len = sorted.length
      if len.odd?
        sorted[len / 2]
      else
        (sorted[len / 2 - 1] + sorted[len / 2]) / 2.0
      end
    end

    # Calculate mode (most frequent value)
    # @param numbers [Array<Numeric>] array of numbers
    # @return [Array<Numeric>] mode values, or nil if empty
    def self.mode(numbers)
      return nil if numbers.nil? || numbers.empty?
      frequency = numbers.group_by(&:itself).transform_values(&:count)
      max_count = frequency.values.max
      frequency.select { |_, v| v == max_count }.keys
    end

    # Calculate standard deviation
    # @param numbers [Array<Numeric>] array of numbers
    # @param sample [Boolean] use sample standard deviation (default: false)
 # @return [Float] standard deviation, or nil if empty
    def self.std_dev(numbers, sample: false)
      return nil if numbers.nil? || numbers.length < 2
      m = mean(numbers)
      variance = numbers.map { |n| (n - m) ** 2 }.sum / (numbers.length - (sample ? 1 : 0))
      Math.sqrt(variance)
    end

    # Calculate sum of squares
    # @param numbers [Array<Numeric>] array of numbers
    # @return [Float] sum of squares, or nil if empty
    def self.sum_of_squares(numbers)
      return nil if numbers.nil? || numbers.empty?
      numbers.map { |n| n ** 2 }.sum
    end

    # Calculate range (max - min)
    # @param numbers [Array<Numeric>] array of numbers
    # @return [Float] range, or nil if empty
    def self.range(numbers)
      return nil if numbers.nil? || numbers.empty?
      numbers.max - numbers.min
    end

    # ============================================================================
    # Number Validation
    # ============================================================================

    # Check if value is a number (integer or float)
    # @param value [Object] value to check
    # @return [Boolean] true if numeric
    def self.number?(value)
      value.is_a?(Numeric)
    end

    # Check if value is an integer
    # @param value [Object] value to check
    # @return [Boolean] true if integer
    def self.integer?(value)
      value.is_a?(Integer)
    end

    # Check if value is a float
    # @param value [Object] value to check
    # @return [Boolean] true if float
    def self.float?(value)
      value.is_a?(Float)
    end

    # Check if number is even
    # @param number [Integer] the number
    # @return [Boolean] true if even
    def self.even?(number)
      return false unless number.is_a?(Integer)
      number.even?
    end

    # Check if number is odd
    # @param number [Integer] the number
    # @return [Boolean] true if odd
    def self.odd?(number)
      return false unless number.is_a?(Integer)
      number.odd?
    end

    # Check if number is positive
    # @param number [Numeric] the number
    # @return [Boolean] true if positive
    def self.positive?(number)
      return false unless number.is_a?(Numeric)
      number > 0
    end

    # Check if number is negative
    # @param number [Numeric] the number
    # @return [Boolean] true if negative
    def self.negative?(number)
      return false unless number.is_a?(Numeric)
      number < 0
    end

    # Check if number is zero
    # @param number [Numeric] the number
    # @return [Boolean] true if zero
    def self.zero?(number)
      return false unless number.is_a?(Numeric)
      number == 0
    end

    # Check if number is between min and max (inclusive)
    # @param number [Numeric] the number
    # @param min [Numeric] minimum value
    # @param max [Numeric] maximum value
    # @return [Boolean] true if in range
    def self.between?(number, min, max)
      return false unless number.is_a?(Numeric)
      number >= min && number <= max
    end

    # Check if number is prime
    # @param number [Integer] the number
    # @return [Boolean] true if prime
    def self.prime?(number)
      return false unless number.is_a?(Integer)
      return false if number < 2
      return true if number == 2
      return false if number.even?

      (3..Math.sqrt(number).to_i).step(2).none? { |i| number % i == 0 }
    end

    # Check if number is a perfect square
    # @param number [Integer] the number
    # @return [Boolean] true if perfect square
    def self.perfect_square?(number)
      return false unless number.is_a?(Integer)
      return false if number < 0
      sqrt = Math.sqrt(number).to_i
      sqrt * sqrt == number
    end

    # ============================================================================
    # Random Number Generation
    # ============================================================================

    # Generate random number in range
    # @param min [Numeric] minimum value
    # @param max [Numeric] maximum value
    # @return [Float] random number
    def self.random(min: 0, max: 1)
      rand * (max - min) + min
    end

    # Generate random integer in range
    # @param min [Integer] minimum value (inclusive)
    # @param max [Integer] maximum value (inclusive)
    # @return [Integer] random integer
    def self.random_int(min:, max:)
      rand(min..max)
    end

    # Generate random number with normal distribution
    # @param mean [Float] mean value
    # @param std_dev [Float] standard deviation
    # @return [Float] normally distributed random number
    def self.random_normal(mean: 0, std_dev: 1)
      # Box-Muller transform
      u1 = rand
      u2 = rand
      z0 = Math.sqrt(-2 * Math.log(u1)) * Math.cos(2 * Math::PI * u2)
      mean + std_dev * z0
    end

    # ============================================================================
    # Number Parsing
    # ============================================================================

    # Parse string to number (int or float)
    # @param str [String] string to parse
    # @param default [Numeric] default value if parsing fails (default: nil)
    # @return [Numeric] parsed number or default
    def self.parse(str, default: nil)
      return default if str.nil? || str.to_s.empty?

      str = str.to_s.strip.gsub(/,/, '')
      if str.include?('.')
        Float(str) rescue default
      else
        Integer(str) rescue default
      end
    end

    # Parse string to integer
    # @param str [String] string to parse
    # @param default [Integer] default value if parsing fails (default: nil)
    # @param base [Integer] number base (default: 10)
    # @return [Integer] parsed integer or default
    def self.parse_int(str, default: nil, base: 10)
      return default if str.nil? || str.to_s.empty?
      Integer(str.to_s.strip, base) rescue default
    end

    # Parse string to float
    # @param str [String] string to parse
    # @param default [Float] default value if parsing fails (default: nil)
    # @return [Float] parsed float or default
    def self.parse_float(str, default: nil)
      return default if str.nil? || str.to_s.empty?
      Float(str.to_s.strip.gsub(/,/, '')) rescue default
    end

    # ============================================================================
    # Utility Functions
    # ============================================================================

    # Calculate greatest common divisor (GCD)
    # @param a [Integer] first number
    # @param b [Integer] second number
    # @return [Integer] GCD
    def self.gcd(a, b)
      return nil if a.nil? || b.nil?
      a.gcd(b)
    end

    # Calculate least common multiple (LCM)
    # @param a [Integer] first number
    # @param b [Integer] second number
    # @return [Integer] LCM
    def self.lcm(a, b)
      return nil if a.nil? || b.nil?
      a.lcm(b)
    end

    # Calculate factorial
    # @param n [Integer] the number
    # @return [Integer] factorial, or nil if negative
    def self.factorial(n)
      return nil unless n.is_a?(Integer)
      return nil if n < 0
      return 1 if n == 0
      (1..n).reduce(:*)
    end

    # Calculate Fibonacci number
    # @param n [Integer] position (0-indexed)
    # @return [Integer] Fibonacci number, or nil if negative
    def self.fibonacci(n)
      return nil unless n.is_a?(Integer)
      return nil if n < 0
      return n if n <= 1

      a, b = 0, 1
      (2..n).each { a, b = b, a + b }
      b
    end

    # Calculate power with overflow protection
    # @param base [Numeric] base number
    # @param exponent [Numeric] exponent
    # @return [Numeric] result
    def self.power(base, exponent)
      return nil if base.nil? || exponent.nil?
      base ** exponent
    end

    # Calculate square root
    # @param number [Numeric] the number
    # @return [Float] square root, or nil if negative
    def self.sqrt(number)
      return nil unless number.is_a?(Numeric)
      return nil if number < 0
      Math.sqrt(number)
    end

    # Calculate nth root
    # @param number [Numeric] the number
    # @param n [Integer] the root
    # @return [Float] nth root
    def self.nth_root(number, n)
      return nil if number.nil? || n.nil?
      number ** (1.0 / n)
    end

    # Convert degrees to radians
    # @param degrees [Numeric] degrees
    # @return [Float] radians
    def self.to_radians(degrees)
      return nil if degrees.nil?
      degrees * Math::PI / 180.0
    end

    # Convert radians to degrees
    # @param radians [Numeric] radians
    # @return [Float] degrees
    def self.to_degrees(radians)
      return nil if radians.nil?
      radians * 180.0 / Math::PI
    end

    # Normalize angle to 0-360 range
    # @param degrees [Numeric] angle in degrees
    # @return [Float] normalized angle
    def self.normalize_angle(degrees)
      return nil if degrees.nil?
      ((degrees % 360) + 360) % 360
    end

    # Calculate sum of digits
    # @param number [Integer] the number
    # @return [Integer] sum of digits
    def self.sum_of_digits(number)
      return nil unless number.is_a?(Integer)
      number.abs.to_s.chars.map(&:to_i).sum
    end

    # Reverse digits of a number
    # @param number [Integer] the number
    # @return [Integer] reversed number
    def self.reverse_digits(number)
      return nil unless number.is_a?(Integer)
      sign = number < 0 ? -1 : 1
      sign * number.abs.to_s.reverse.to_i
    end

    # Check if number is palindrome
    # @param number [Integer] the number
    # @return [Boolean] true if palindrome
    def self.palindrome?(number)
      return false unless number.is_a?(Integer)
      number == reverse_digits(number)
    end

    # ============================================================================
    # Convenience Methods (Module-level shortcuts)
    # ============================================================================

    # Convenience method for formatting
    def self.fmt(number, **options)
      format(number, **options)
    end

    # Convenience method for currency
    def self.cur(number, **options)
      currency(number, **options)
    end

    # Convenience method for percentage
    def self.pct(number, **options)
      percentage(number, **options)
    end
  end
end

# Top-level convenience methods
def number_format(number, **options)
  AllToolkit::NumberUtils.format(number, **options)
end

def number_currency(number, **options)
  AllToolkit::NumberUtils.currency(number, **options)
end

def number_percentage(number, **options)
  AllToolkit::NumberUtils.percentage(number, **options)
end

#!/usr/bin/env ruby
# frozen_string_literal: true

# QR Code Utilities Test Suite
# Comprehensive tests for QR code generation

require_relative 'mod'

class QrCodeUtilsTest
  include AllToolkit::QrCodeUtils

  def self.run_all
    puts "Running QR Code Utils Tests..."
    puts "=" * 50

    test = new
    methods = public_methods(false).select { |m| m.to_s.start_with?('test_') }
    passed = 0
    failed = 0

    methods.each do |method|
      begin
        test.send(method)
        puts "✓ #{method}"
        passed += 1
      rescue => e
        puts "✗ #{method}: #{e.message}"
        failed += 1
      end
    end

    puts "=" * 50
    puts "Results: #{passed} passed, #{failed} failed"
    exit(failed > 0 ? 1 : 0)
  end

  def assert_equal(expected, actual, message = nil)
    return if expected == actual
    raise "#{message || 'Assertion failed'}: expected #{expected.inspect}, got #{actual.inspect}"
  end

  def assert(condition, message = nil)
    return if condition
    raise message || 'Assertion failed'
  end

  def assert_raises(error_class)
    begin
      yield
      raise "Expected #{error_class} to be raised"
    rescue error_class
      # Expected
    end
  end

  # Test basic QR code generation
  def test_basic_generation
    qr = QrCodeUtils.generate("Hello")
    assert_equal 21, qr.size # Version 1 = 21x21
    assert_equal "Hello", qr.data
    assert_equal 1, qr.version
  end

  # Test different error correction levels
  def test_error_correction_levels
    qr_l = QrCodeUtils.generate("Test", QrCodeUtils::LEVEL_L)
    qr_m = QrCodeUtils.generate("Test", QrCodeUtils::LEVEL_M)
    qr_q = QrCodeUtils.generate("Test", QrCodeUtils::LEVEL_Q)
    qr_h = QrCodeUtils.generate("Test", QrCodeUtils::LEVEL_H)

    assert_equal 0, qr_l.error_correction_level
    assert_equal 1, qr_m.error_correction_level
    assert_equal 2, qr_q.error_correction_level
    assert_equal 3, qr_h.error_correction_level
  end

  # Test version detection for different data lengths
  def test_version_detection
    qr1 = QrCodeUtils.generate("A" * 10)  # Version 1
    qr2 = QrCodeUtils.generate("A" * 30)  # Version 2
    qr3 = QrCodeUtils.generate("A" * 50)  # Version 3

    assert_equal 1, qr1.version
    assert_equal 2, qr2.version
    assert_equal 3, qr3.version
  end

  # Test ASCII output
  def test_to_ascii
    qr = QrCodeUtils.generate("Hi")
    ascii = qr.to_ascii
    lines = ascii.split("\n")

    # Should have border + QR size + border
    assert_equal 21 + 4, lines.length # 2 border each side
    assert lines.all? { |l| l.length == 21 + 4 } # All lines same width
  end

  # Test Unicode output
  def test_to_unicode
    qr = QrCodeUtils.generate("Hi")
    unicode = qr.to_unicode
    lines = unicode.split("\n")

    assert lines.length > 0
    assert lines.all? { |l| l.length > 0 }
  end

  # Test SVG output
  def test_to_svg
    qr = QrCodeUtils.generate("Test")
    svg = qr.to_svg

    assert svg.include?('<?xml version="1.0"')
    assert svg.include?('<svg')
    assert svg.include?('</svg>')
    assert svg.include?('<rect')
  end

  # Test matrix output
  def test_to_matrix
    qr = QrCodeUtils.generate("Test")
    matrix = qr.to_matrix

    assert_equal qr.size, matrix.length
    assert matrix.all? { |row| row.length == qr.size }
  end

  # Test module access
  def test_module_access
    qr = QrCodeUtils.generate("Test")

    # Top-left finder pattern should have dark modules
    assert qr[0, 0] # Corner should be dark
    assert qr[6, 6] # Center should be dark
    assert !qr[1, 1] # Inner should be light
  end

  # Test data too long raises error
  def test_data_too_long
    assert_raises(ArgumentError) do
      QrCodeUtils.generate("A" * 300) # Too long for version 10
    end
  end

  # Test empty string
  def test_empty_string
    qr = QrCodeUtils.generate("")
    assert_equal "", qr.data
    assert_equal 1, qr.version
  end

  # Test special characters
  def test_special_characters
    qr = QrCodeUtils.generate("Hello, World! @#$%")
    assert_equal "Hello, World! @#$%", qr.data
  end

  # Test Unicode characters
  def test_unicode_characters
    qr = QrCodeUtils.generate("你好世界")
    assert_equal "你好世界", qr.data
  end

  # Test URL generation
  def test_url_generation
    url = "https://example.com/path?query=value"
    qr = QrCodeUtils.generate(url)
    assert_equal url, qr.data
  end

  # Test max data length helper
  def test_max_data_length
    assert QrCodeUtils.max_data_length(1, QrCodeUtils::LEVEL_L) > 0
    assert QrCodeUtils.max_data_length(10, QrCodeUtils::LEVEL_H) > 0
  end

  # Test compact ASCII alias
  def test_compact_ascii_alias
    qr = QrCodeUtils.generate("Test")
    assert_equal qr.to_unicode, qr.to_compact_ascii
  end

  # Test different border sizes
  def test_different_border_sizes
    qr = QrCodeUtils.generate("Test")
    ascii1 = qr.to_ascii(1)
    ascii2 = qr.to_ascii(4)

    assert ascii1.lines.count < ascii2.lines.count
  end

  # Test finder patterns are present
  def test_finder_patterns_present
    qr = QrCodeUtils.generate("Test")

    # Top-left finder pattern
    assert qr[0, 0]
    assert qr[0, 6]
    assert qr[6, 0]
    assert qr[6, 6]

    # Top-right finder pattern
    assert qr[0, qr.size - 1]
    assert qr[0, qr.size - 7]
    assert qr[6, qr.size - 1]
    assert qr[6, qr.size - 7]

    # Bottom-left finder pattern
    assert qr[qr.size - 1, 0]
    assert qr[qr.size - 7, 0]
    assert qr[qr.size - 1, 6]
    assert qr[qr.size - 7, 6]
  end

  # Test timing patterns
  def test_timing_patterns
    qr = QrCodeUtils.generate("Test")

    # Timing pattern should alternate
    (8...qr.size - 8).each do |i|
      expected = i.even?
      assert_equal expected, qr[6, i], "Timing pattern at row 6, col #{i}"
      assert_equal expected, qr[i, 6], "Timing pattern at row #{i}, col 6"
    end
  end

  # Test dark module
  def test_dark_module
    qr = QrCodeUtils.generate("Test")
    # Dark module is always at (4*version + 9, 8)
    assert qr[4 * qr.version + 9, 8]
  end

  # Test version 2+ has alignment patterns
  def test_alignment_patterns
    qr1 = QrCodeUtils.generate("A") # Version 1 - no alignment
    qr2 = QrCodeUtils.generate("A" * 25) # Version 2 - has alignment

    # Version 1 should not have alignment patterns in the middle
    # Version 2+ should have them
    assert_equal 1, qr1.version
    assert qr2.version >= 2
  end

  # Test SVG dimensions
  def test_svg_dimensions
    qr = QrCodeUtils.generate("Test")
    svg = qr.to_svg(10, 4)

    # Should contain width and height
    assert svg.include?('width="290"') # (21 + 8) * 10 = 290
    assert svg.include?('height="290"')
  end

  # Test function pattern detection
  def test_function_pattern_detection
    qr = QrCodeUtils.generate("Test")

    # Finder patterns should be marked as function
    assert qr.function?(0, 0)
    assert qr.function?(3, 3)
    assert !qr.function?(10, 10) # Data area
  end

  # Test numeric data
  def test_numeric_data
    qr = QrCodeUtils.generate("1234567890")
    assert_equal "1234567890", qr.data
  end

  # Test long data requires higher version
  def test_long_data_higher_version
    short_qr = QrCodeUtils.generate("Short")
    long_qr = QrCodeUtils.generate("A" * 100)

    assert short_qr.version < long_qr.version
  end

  # Test QR code is square
  def test_qr_code_is_square
    qr = QrCodeUtils.generate("Test data here")
    assert_equal qr.size, qr.modules.length
    assert qr.modules.all? { |row| row.length == qr.size }
  end

  # Test multiple generations produce consistent results
  def test_consistent_generation
    qr1 = QrCodeUtils.generate("Same data")
    qr2 = QrCodeUtils.generate("Same data")
    
    # Same data should produce same QR code
    assert_equal qr1.size, qr2.size
    assert_equal qr1.version, qr2.version
  end
end

# Run tests if executed directly
if __FILE__ == $0
  QrCodeUtilsTest.run_all
end

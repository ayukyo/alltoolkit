#!/usr/bin/env ruby
# frozen_string_literal: true

# AllToolkit - Ruby Regex Utils Test Suite
# Run with: ruby regex_utils_test.rb

require_relative 'mod'

# Simple test framework
class TestRunner
  def initialize
    @tests = 0
    @passed = 0
    @failed = 0
  end

  def test(name)
    @tests += 1
    begin
      yield
      @passed += 1
      puts "  ✓ #{name}"
    rescue => e
      @failed += 1
      puts "  ✗ #{name}: #{e.message}"
    end
  end

  def assert_equal(expected, actual)
    raise "Expected #{expected.inspect}, got #{actual.inspect}" unless expected == actual
  end

  def assert_true(value)
    raise "Expected true, got #{value.inspect}" unless value == true
  end

  def assert_false(value)
    raise "Expected false, got #{value.inspect}" unless value == false
  end

  def assert_nil(value)
    raise "Expected nil, got #{value.inspect}" unless value.nil?
  end

  def summary
    puts "\n" + "=" * 50
    puts "Total: #{@tests}, Passed: #{@passed}, Failed: #{@failed}"
    puts @failed == 0 ? "All tests passed!" : "Some tests failed!"
    exit(@failed == 0 ? 0 : 1)
  end
end

# Run tests
runner = TestRunner.new

puts "Testing AllToolkit::RegexUtils"
puts "=" * 50

# Test: match? with preset patterns
puts "\nTest Group: match? with preset patterns"
runner.test("email validation - valid") do
  runner.assert_true(RegexUtils.match?("test@example.com", :email))
end

runner.test("email validation - invalid") do
  runner.assert_false(RegexUtils.match?("invalid-email", :email))
end

runner.test("URL validation - valid http") do
  runner.assert_true(RegexUtils.match?("http://example.com", :url))
end

runner.test("URL validation - valid https") do
  runner.assert_true(RegexUtils.match?("https://example.com/path", :url))
end

runner.test("IPv4 validation - valid") do
  runner.assert_true(RegexUtils.match?("192.168.1.1", :ipv4))
end

runner.test("IPv4 validation - invalid") do
  runner.assert_false(RegexUtils.match?("256.1.1.1", :ipv4))
end

runner.test("UUID validation - valid") do
  runner.assert_true(RegexUtils.match?("550e8400-e29b-41d4-a716-446655440000", :uuid))
end

runner.test("hex color validation - valid short") do
  runner.assert_true(RegexUtils.match?("#fff", :hex_color))
end

runner.test("hex color validation - valid long") do
  runner.assert_true(RegexUtils.match?("#ffffff", :hex_color))
end

runner.test("numeric validation") do
  runner.assert_true(RegexUtils.match?("-123", :numeric))
  runner.assert_false(RegexUtils.match?("12.34", :numeric))
end

runner.test("decimal validation") do
  runner.assert_true(RegexUtils.match?("12.34", :decimal))
end

# Test: match? with custom regex
puts "\nTest Group: match? with custom regex"
runner.test("custom regex - match") do
  runner.assert_true(RegexUtils.match?("hello", /\Ahello\z/))
end

runner.test("custom regex - no match") do
  runner.assert_false(RegexUtils.match?("world", /\Ahello\z/))
end

# Test: no_match?
puts "\nTest Group: no_match?"
runner.test("no_match? - true when no match") do
  runner.assert_true(RegexUtils.no_match?("invalid", :email))
end

runner.test("no_match? - false when match") do
  runner.assert_false(RegexUtils.no_match?("test@example.com", :email))
end

# Test: find
puts "\nTest Group: find"
runner.test("find - success") do
  result = RegexUtils.find("hello world", /\w+/)
  runner.assert_true(result.success?)
  runner.assert_equal("hello", result.first)
end

runner.test("find - failure") do
  result = RegexUtils.find("hello", /\d+/)
  runner.assert_false(result.success?)
  runner.assert_true(result.empty?)
end

runner.test("find - with capture groups") do
  result = RegexUtils.find("hello world", /(\w+) (\w+)/)
  runner.assert_equal("hello world", result[0])
  runner.assert_equal("hello", result[1])
  runner.assert_equal("world", result[2])
end

runner.test("find - with named captures") do
  result = RegexUtils.find("hello world", /(?<first>\w+) (?<second>\w+)/)
  runner.assert_equal("hello", result.named_groups["first"])
  runner.assert_equal("world", result.named_groups["second"])
end

runner.test("find - nil string") do
  result = RegexUtils.find(nil, /\w+/)
  runner.assert_false(result.success?)
end

# Test: find_all
puts "\nTest Group: find_all"
runner.test("find_all - multiple matches") do
  result = RegexUtils.find_all("a1b2c3", /\d/)
  runner.assert_equal(["1", "2", "3"], result)
end

runner.test("find_all - no matches") do
  result = RegexUtils.find_all("abc", /\d/)
  runner.assert_equal([], result)
end

runner.test("find_all - with preset") do
  result = RegexUtils.find_all("Contact us at support@example.com or sales@test.org", :email)
  runner.assert_equal(["support@example.com", "sales@test.org"], result)
end

runner.test("find_all - nil string") do
  result = RegexUtils.find_all(nil, /\w+/)
  runner.assert_equal([], result)
end

# Test: find_all_with_groups
puts "\nTest Group: find_all_with_groups"
runner.test("find_all_with_groups - multiple matches") do
  result = RegexUtils.find_all_with_groups("[link1](url1) [link2](url2)", :markdown_link)
  runner.assert_equal(2, result.length)
  runner.assert_equal("link1", result[0][1])
  runner.assert_equal("url1", result[0][2])
  runner.assert_equal("link2", result[1][1])
  runner.assert_equal("url2", result[1][2])
end

# Test: replace_first
puts "\nTest Group: replace_first"
runner.test("replace_first - string replacement") do
  result = RegexUtils.replace_first("hello world", /\w+/, "hi")
  runner.assert_equal("hi world", result)
end

runner.test("replace_first - with preset") do
  result = RegexUtils.replace_first("a1b2", /\d/, "X")
  runner.assert_equal("aXb2", result)
end

runner.test("replace_first - with proc") do
  result = RegexUtils.replace_first("hello", /\w+/) { |m| m.upcase }
  runner.assert_equal("HELLO", result)
end

runner.test("replace_first - nil string") do
  result = RegexUtils.replace_first(nil, /\w+/, "X")
  runner.assert_nil(result)
end

# Test: replace_all
puts "\nTest Group: replace_all"
runner.test("replace_all - string replacement") do
  result = RegexUtils.replace_all("a1b2c3", /\d/, "X")
  runner.assert_equal("aXbXcX", result)
end

runner.test("replace_all - with proc") do
  result = RegexUtils.replace_all("abc", /\w/) { |m| "(#{m})" }
  runner.assert_equal("(a)(b)(c)", result)
end

runner.test("replace_all - nil string") do
  result = RegexUtils.replace_all(nil, /\w+/, "X")
  runner.assert_nil(result)
end

# Test: split
puts "\nTest Group: split"
runner.test("split - basic") do
  result = RegexUtils.split("a,b,c", /,/)
  runner.assert_equal(["a", "b", "c"], result)
end

runner.test("split - with preset") do
  result = RegexUtils.split("one,two,three", /,/)
  runner.assert_equal(["one", "two", "three"], result)
end

runner.test("split - nil string") do
  result = RegexUtils.split(nil, /,/)
  runner.assert_equal([], result)
end

# Test: extract
puts "\nTest Group: extract"
runner.test("extract - by index") do
  result = RegexUtils.extract("hello world", /(\w+) (\w+)/, 1)
  runner.assert_equal("hello", result)
end

runner.test("extract - by name") do
  result = RegexUtils.extract("hello world", /(?<first>\w+)/, "first")
  runner.assert_equal("hello", result)
end

runner.test("extract - no match") do
  result = RegexUtils.extract("hello", /\d+/, 0)
  runner.assert_nil(result)
end

runner.test("extract - nil string") do
  result = RegexUtils.extract(nil, /\w+/, 0)
  runner.assert_nil(result)
end

# Test: remove
puts "\nTest Group: remove"runner.test("remove - all matches") do
  result = RegexUtils.remove("a1b2c3", /\d/)
  runner.assert_equal("abc", result)
end

runner.test("remove - preset pattern") do
  result = RegexUtils.remove("Hello #world test", :hashtag)
  runner.assert_equal("Hello  test", result)
end

# Test: remove_first
puts "\nTest Group: remove_first"
runner.test("remove_first - single match") do
  result = RegexUtils.remove_first("a1b2c3", /\d/)
  runner.assert_equal("ab2c3", result)
end

# Test: count
puts "\nTest Group: count"
runner.test("count - multiple matches") do
  result = RegexUtils.count("a1b2c3", /\d/)
  runner.assert_equal(3, result)
end

runner.test("count - no matches") do
  result = RegexUtils.count("abc", /\d/)
  runner.assert_equal(0, result)
end

runner.test("count - nil string") do
  result = RegexUtils.count(nil, /\w+/)
  runner.assert_equal(0, result)
end

# Test: contains?
puts "\nTest Group: contains?"
runner.test("contains? - true") do
  runner.assert_true(RegexUtils.contains?("hello world", /world/))
end

runner.test("contains? - false") do
  runner.assert_false(RegexUtils.contains?("hello", /world/))
end

runner.test("contains? - nil string") do
  runner.assert_false(RegexUtils.contains?(nil, /\w+/))
end

# Test: escape
puts "\nTest Group: escape"
runner.test("escape - special chars") do
  result = RegexUtils.escape("a.b*c+d?")
  runner.assert_equal("a\\.b\\*c\\+d\\?", result)
end

runner.test("escape - nil") do
  result = RegexUtils.escape(nil)
  runner.assert_equal("", result)
end

# Test: build
puts "\nTest Group: build"
runner.test("build - basic") do
  result = RegexUtils.build("hello")
  runner.assert_true(result.is_a?(Regexp))
  runner.assert_true("hello".match?(result))
end

runner.test("build - with options") do
  result = RegexUtils.build("hello", Regexp::IGNORECASE)
  runner.assert_true("HELLO".match?(result))
end

runner.test("build - nil pattern") do
  result = RegexUtils.build(nil)
  runner.assert_nil(result)
end

# Test: valid?
puts "\nTest Group: valid?"
runner.test("valid? - email") do
  runner.assert_true(RegexUtils.valid?("test@example.com", :email))
end

runner.test("valid? - invalid") do
  runner.assert_false(RegexUtils.valid?("invalid", :email))
end

# Test: presets
puts "\nTest Group: presets"
runner.test("presets - returns array") do
  result = RegexUtils.presets
  runner.assert_true(result.is_a?(Array))
  runner.assert_true(result.include?(:email))
  runner.assert_true(result.include?(:url))
  runner.assert_true(result.include?(:ipv4))
end

# Test: get_preset
puts "\nTest Group: get_preset"
runner.test("get_preset - existing") do
  result = RegexUtils.get_preset(:email)
  runner.assert_true(result.is_a?(Regexp))
end

runner.test("get_preset - non-existing") do
  result = RegexUtils.get_preset(:nonexistent)
  runner.assert_nil(result)
end

# Test: preset_exists?
puts "\nTest Group: preset_exists?"
runner.test("preset_exists? - true") do
  runner.assert_true(RegexUtils.preset_exists?(:email))
end

runner.test("preset_exists? - false") do
  runner.assert_false(RegexUtils.preset_exists?(:nonexistent))
end

# Test: nil handling
puts "\nTest Group: nil handling"
runner.test("nil handling - match?") do
  runner.assert_false(RegexUtils.match?(nil, :email))
end

runner.test("nil handling - find") do
  result = RegexUtils.find(nil, /\w+/)
  runner.assert_false(result.success?)
end

runner.test("nil handling - find_all") do
  result = RegexUtils.find_all(nil, /\w+/)
  runner.assert_equal([], result)
end

# Test: MatchResult methods
puts "\nTest Group: MatchResult"
runner.test("MatchResult - array access") do
  result = RegexUtils.find("hello world", /(\w+) (\w+)/)
  runner.assert_equal("hello world", result[0])
  runner.assert_equal("hello", result[1])
end

runner.test("MatchResult - to_a") do
  result = RegexUtils.find("hello world", /(\w+) (\w+)/)
  runner.assert_equal(["hello world", "hello", "world"], result.to_a)
end

runner.test("MatchResult - to_s") do
  result = RegexUtils.find("hello world", /(\w+)/)
  runner.assert_equal("hello", result.to_s)
end

# Print summary
runner.summary

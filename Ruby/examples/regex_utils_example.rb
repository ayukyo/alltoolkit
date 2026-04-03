#!/usr/bin/env ruby
# frozen_string_literal: true

# AllToolkit - Ruby Regex Utils Example
# Demonstrates usage of the RegexUtils module
#
# Run with: ruby regex_utils_example.rb

require_relative '../regex_utils/mod'

puts "=" * 60
puts "AllToolkit Ruby RegexUtils - Usage Examples"
puts "=" * 60

# Example 1: Email Validation
puts "\n1. Email Validation"
puts "-" * 40
emails = [
  "user@example.com",
  "invalid-email",
  "test.name+tag@example.co.uk",
  "@example.com"
]

emails.each do |email|
  valid = RegexUtils.match?(email, :email)
  puts "  #{email.ljust(30)} => #{valid ? '✓ Valid' : '✗ Invalid'}"
end

# Example 2: URL Validation
puts "\n2. URL Validation"
puts "-" * 40
urls = [
  "https://www.example.com",
  "http://localhost:8080/path",
  "not-a-url",
  "ftp://files.example.com"
]

urls.each do |url|
  valid = RegexUtils.match?(url, :url)
  puts "  #{url.ljust(30)} => #{valid ? '✓ Valid' : '✗ Invalid'}"
end

# Example 3: IP Address Validation
puts "\n3. IP Address Validation"
puts "-" * 40
ips = [
  "192.168.1.1",
  "10.0.0.1",
  "256.1.1.1",
  "2001:0db8:85a3:0000:0000:8a2e:0370:7334"
]

ips.each do |ip|
  if RegexUtils.match?(ip, :ipv4)
    puts "  #{ip.ljust(30)} => ✓ Valid IPv4"
  elsif RegexUtils.match?(ip, :ipv6)
    puts "  #{ip.ljust(30)} => ✓ Valid IPv6"
  else
    puts "  #{ip.ljust(30)} => ✗ Invalid IP"
  end
end

# Example 4: Finding Matches
puts "\n4. Finding Matches"
puts "-" * 40
text = "The year 2024 will be followed by 2025 and 2026."
puts "  Text: #{text}"
puts "  Pattern: /\\d{4}/"

result = RegexUtils.find(text, /\d{4}/)
if result.success?
  puts "  First match: #{result.first}"
  puts "  All captures: #{result.to_a.inspect}"
else
  puts "  No match found"
end

# Example 5: Finding All Matches
puts "\n5. Finding All Matches"
puts "-" * 40
text = "Prices: $10, $20, $30, $45"
puts "  Text: #{text}"
matches = RegexUtils.find_all(text, /\d+/)
puts "  All numbers: #{matches.inspect}"

# Example 6: Extracting with Capture Groups
puts "\n6. Extracting with Capture Groups"
puts "-" * 40
text = "Name: John Doe, Age: 30"
puts "  Text: #{text}"

result = RegexUtils.find(text, /Name:\s*(\w+)\s+(\w+)/)
if result.success?
  puts "  Full match: #{result[0]}"
  puts "  First name: #{result[1]}"
  puts "  Last name: #{result[2]}"
end

# Example 7: Named Capture Groups
puts "\n7. Named Capture Groups"
puts "-" * 40
text = "2024-03-15"
puts "  Text: #{text}"

result = RegexUtils.find(text, /(?<year>\d{4})-(?<month>\d{2})-(?<day>\d{2})/)
if result.success?
  puts "  Year:  #{result.named_groups['year']}"
  puts "  Month: #{result.named_groups['month']}"
  puts "  Day:   #{result.named_groups['day']}"
end

# Example 8: String Replacement
puts "\n8. String Replacement"
puts "-" * 40
text = "Hello world, hello Ruby!"
puts "  Original: #{text}"

# Replace first occurrence
result = RegexUtils.replace_first(text, /hello/i, "Hi")
puts "  Replace first: #{result}"

# Replace all occurrences
result = RegexUtils.replace_all(text, /hello/i, "Hi")
puts "  Replace all: #{result}"

# Replace with a block
result = RegexUtils.replace_all(text, /\w+/) { |word| word.upcase }
puts "  Uppercase all: #{result}"

# Example 9: Removing Patterns
puts "\n9. Removing Patterns"
puts "-" * 40
text = "Hello #world this is a #test"
puts "  Original: #{text}"

result = RegexUtils.remove(text, :hashtag)
puts "  Remove hashtags: #{result}"

result = RegexUtils.remove_first(text, :hashtag)
puts "  Remove first hashtag: #{result}"

# Example 10: Splitting Strings
puts "\n10. Splitting Strings"
puts "-" * 40
csv_line = "apple,banana,cherry,date"
puts "  CSV: #{csv_line}"

parts = RegexUtils.split(csv_line, /,/)
puts "  Parts: #{parts.inspect}"

# Example 11: Counting Matches
puts "\n11. Counting Matches"
puts "-" * 40
text = "The quick brown fox jumps over the lazy dog."
puts "  Text: #{text}"

count = RegexUtils.count(text, /\w+/)
puts "  Word count: #{count}"

count = RegexUtils.count(text, /[aeiou]/)
puts "  Vowel count: #{count}"

# Example 12: Checking if Contains Pattern
puts "\n12. Checking if Contains Pattern"
puts "-" * 40
text = "user@example.com sent an email"
puts "  Text: #{text}"

if RegexUtils.contains?(text, :email)
  puts "  ✓ Contains an email address"
else
  puts "  ✗ No email address found"
end

# Example 13: Extracting Specific Groups
puts "\n13. Extracting Specific Groups"
puts "-" * 40
text = "File: document.pdf, Size: 1024KB"
puts "  Text: #{text}"

filename = RegexUtils.extract(text, /File:\s*(\S+)/, 1)
extension = RegexUtils.extract(text, :file_extension, 1)
puts "  Filename: #{filename}"
puts "  Extension: #{extension}"

# Example 14: UUID Generation and Validation
puts "\n14. UUID Validation"
puts "-" * 40
uuids = [
  "550e8400-e29b-41d4-a716-446655440000",
  "not-a-uuid",
  "550e8400e29b41d4a716446655440000"
]

uuids.each do |uuid|
  valid_standard = RegexUtils.match?(uuid, :uuid)
  valid_compact = RegexUtils.match?(uuid, :uuid_compact)
  if valid_standard
    puts "  #{uuid} => ✓ Valid standard UUID"
  elsif valid_compact
    puts "  #{uuid} => ✓ Valid compact UUID"
  else
    puts "  #{uuid} => ✗ Invalid UUID"
  end
end

# Example 15: Hex Color Validation
puts "\n15. Hex Color Validation"
puts "-" * 40
colors = ["#fff", "#ffffff", "#123abc", "not-a-color", "#ggg"]

colors.each do |color|
  valid = RegexUtils.match?(color, :hex_color)
  puts "  #{color.ljust(15)} => #{valid ? '✓ Valid' : '✗ Invalid'}"
end

# Example 16: Markdown Link Parsing
puts "\n16. Markdown Link Parsing"
puts "-" * 40
markdown = "Check out [AllToolkit](https://github.com/ayukyo/alltoolkit) and [Ruby](https://ruby-lang.org)"
puts "  Markdown: #{markdown}"

links = RegexUtils.find_all_with_groups(markdown, :markdown_link)
puts "  Found #{links.length} links:"
links.each_with_index do |link, i|
  puts "    #{i + 1}. #{link[1]} => #{link[2]}"
end

# Example 17: Escaping Special Characters
puts "\n17. Escaping Special Characters"
puts "-" * 40
pattern = "a.b*c+d?"
escaped = RegexUtils.escape(pattern)
puts "  Original: #{pattern}"
puts "  Escaped:  #{escaped}"
puts "  Can match 'a.b*c+d?': #{RegexUtils.match?('a.b*c+d?', Regexp.new(escaped))}"

# Example 18: Building Regex Patterns
puts "\n18. Building Regex Patterns"
puts "-" * 40
pattern = RegexUtils.build("hello", Regexp::IGNORECASE)
puts "  Pattern: #{pattern.inspect}"
puts "  Matches 'HELLO': #{RegexUtils.match?('HELLO', pattern)}"
puts "  Matches 'hello': #{RegexUtils.match?('hello', pattern)}"

# Example 19: Phone Number Validation
puts "\n19. Phone Number Validation"
puts "-" * 40
phones = [
  "+1-555-123-4567",
  "+44 20 7946 0958",
  "(555) 123-4567",
  "12345"
]

phones.each do |phone|
  valid = RegexUtils.valid?(phone, :phone)
  puts "  #{phone.ljust(20)} => #{valid ? '✓ Valid' : '✗ Invalid'}"
end

# Example 20: Using Presets
puts "\n20. Available Presets"
puts "-" * 40
puts "  Available presets: #{RegexUtils.presets.length}"
puts "  First 10: #{RegexUtils.presets.first(10).inspect}"

# Check if preset exists
[:email, :url, :custom].each do |preset|
  exists = RegexUtils.preset_exists?(preset)
  puts "  Preset :#{preset} => #{exists ? 'exists' : 'not found'}"
end

puts "\n" + "=" * 60
puts "Examples completed!"
puts "=" * 60

#!/usr/bin/env ruby
# frozen_string_literal: true

# QR Code Utilities Example
# Demonstrates various QR code generation and output formats

require_relative '../qr_code_utils/mod'

puts "=" * 60
puts "QR Code Utilities Examples"
puts "=" * 60
puts

# Example 1: Basic QR code generation
puts "Example 1: Basic QR Code Generation"
puts "-" * 40
qr = AllToolkit::QrCodeUtils.generate("Hello, World!")
puts "Data: #{qr.data}"
puts "Version: #{qr.version}"
puts "Size: #{qr.size}x#{qr.size} modules"
puts

# Example 2: ASCII art output
puts "Example 2: ASCII Art Output"
puts "-" * 40
qr = AllToolkit::QrCodeUtils.generate("Hello")
puts qr.to_ascii
puts

# Example 3: Compact Unicode output
puts "Example 3: Compact Unicode Output (Half Height)"
puts "-" * 40
qr = AllToolkit::QrCodeUtils.generate("Hi there")
puts qr.to_unicode
puts

# Example 4: Different error correction levels
puts "Example 4: Error Correction Levels"
puts "-" * 40
[
  ["L (~7% recovery)", AllToolkit::QrCodeUtils::LEVEL_L],
  ["M (~15% recovery)", AllToolkit::QrCodeUtils::LEVEL_M],
  ["Q (~25% recovery)", AllToolkit::QrCodeUtils::LEVEL_Q],
  ["H (~30% recovery)", AllToolkit::QrCodeUtils::LEVEL_H]
].each do |name, level|
  qr = AllToolkit::QrCodeUtils.generate("Test", level)
  puts "#{name}: Version #{qr.version}, Size #{qr.size}x#{qr.size}"
end
puts

# Example 5: URL QR code
puts "Example 5: URL QR Code"
puts "-" * 40
url = "https://github.com/ayukyo/alltoolkit"
qr = AllToolkit::QrCodeUtils.generate(url)
puts "URL: #{url}"
puts "QR Code (compact):"
puts qr.to_unicode(1)
puts

# Example 6: WiFi QR code
puts "Example 6: WiFi Connection QR Code"
puts "-" * 40
# WiFi format: WIFI:T:WPA;S:network;P:password;;
wifi_data = "WIFI:T:WPA;S:MyNetwork;P:MyPassword;;"
qr = AllToolkit::QrCodeUtils.generate(wifi_data)
puts "WiFi Data: #{wifi_data}"
puts "QR Code:"
puts qr.to_unicode
puts

# Example 7: Contact card (vCard) QR code
puts "Example 7: Contact Card QR Code"
puts "-" * 40
vcard = "BEGIN:VCARD\nVERSION:3.0\nFN:John Doe\nTEL:1234567890\nEMAIL:john@example.com\nEND:VCARD"
qr = AllToolkit::QrCodeUtils.generate(vcard)
puts "vCard data length: #{vcard.length} characters"
puts "QR Code (compact):"
puts qr.to_compact_ascii
puts

# Example 8: Email QR code
puts "Example 8: Email QR Code"
puts "-" * 40
# mailto format
email_data = "mailto:test@example.com?subject=Hello&body=This is a test"
qr = AllToolkit::QrCodeUtils.generate(email_data)
puts "Email: #{email_data}"
puts qr.to_unicode(1)
puts

# Example 9: Phone number QR code
puts "Example 9: Phone Number QR Code"
puts "-" * 40
phone = "tel:+1234567890"
qr = AllToolkit::QrCodeUtils.generate(phone)
puts "Phone: #{phone}"
puts qr.to_unicode(1)
puts

# Example 10: SVG output
puts "Example 10: SVG Output"
puts "-" * 40
qr = AllToolkit::QrCodeUtils.generate("SVG Test")
svg = qr.to_svg(10, 4)
puts "SVG length: #{svg.length} characters"
puts "First 200 chars:"
puts svg[0..200]
puts "..."
puts

# Example 11: Matrix access
puts "Example 11: Matrix Access"
puts "-" * 40
qr = AllToolkit::QrCodeUtils.generate("Matrix")
matrix = qr.to_matrix
puts "Matrix dimensions: #{matrix.length}x#{matrix[0].length}"
puts "Top-left corner (finder pattern):"
7.times do |row|
  line = ""
  7.times do |col|
    line += matrix[row][col] ? "██" : "  "
  end
  puts line
end
puts

# Example 12: Different data lengths
puts "Example 12: Different Data Lengths"
puts "-" * 40
test_data = [
  ["Very short", "Hi"],
  ["Short", "Hello, World!"],
  ["Medium", "A" * 50],
  ["Long", "B" * 100]
]
test_data.each do |name, data|
  qr = AllToolkit::QrCodeUtils.generate(data)
  puts "#{name} (#{data.length} chars): Version #{qr.version}, #{qr.size}x#{qr.size}"
end
puts

# Example 13: Custom border sizes
puts "Example 13: Custom Border Sizes"
puts "-" * 40
qr = AllToolkit::QrCodeUtils.generate("Border")
puts "No border (0):"
puts qr.to_ascii(0)[0..50] + "..."
puts "\nSmall border (1):"
puts qr.to_ascii(1)[0..60] + "..."
puts "\nLarge border (4):"
puts qr.to_ascii(4)[0..80] + "..."
puts

# Example 14: Max data length helper
puts "Example 14: Max Data Length by Version"
puts "-" * 40
(1..10).each do |version|
  max_l = AllToolkit::QrCodeUtils.max_data_length(version, AllToolkit::QrCodeUtils::LEVEL_L)
  max_h = AllToolkit::QrCodeUtils.max_data_length(version, AllToolkit::QrCodeUtils::LEVEL_H)
  puts "Version #{version}: Level L=#{max_l}, Level H=#{max_h}"
end
puts

# Example 15: Check finder patterns
puts "Example 15: Verify Finder Patterns"
puts "-" * 40
qr = AllToolkit::QrCodeUtils.generate("Verify")
puts "Top-left finder pattern corners:"
puts "(0,0): #{qr[0, 0] ? 'dark' : 'light'}"
puts "(0,6): #{qr[0, 6] ? 'dark' : 'light'}"
puts "(6,0): #{qr[6, 0] ? 'dark' : 'light'}"
puts "(6,6): #{qr[6, 6] ? 'dark' : 'light'}"
puts "(3,3): #{qr[3, 3] ? 'dark' : 'light'} (should be dark - center)"
puts

puts "=" * 60
puts "Examples completed!"
puts "=" * 60

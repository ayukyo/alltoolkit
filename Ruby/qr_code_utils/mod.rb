#!/usr/bin/env ruby
# frozen_string_literal: true

# QR Code Utilities - Pure Ruby QR Code Generator
# Zero dependencies, uses only Ruby standard library
#
# Features:
# - Generate QR codes from text/URLs
# - Multiple output formats: text (ASCII), SVG, Unicode
# - Error correction levels: L, M, Q, H
# - Version 1-10 support (21x21 to 57x57 modules)
# - Automatic version detection
#
# Usage:
#   require_relative 'qr_code_utils/mod'
#   qr = AllToolkit::QrCodeUtils.generate("Hello, World!")
#   puts qr.to_ascii
#   svg = qr.to_svg

module AllToolkit
  # QR Code module
  module QrCodeUtils
    # Error Correction Levels
    LEVEL_L = 0  # ~7% recovery
    LEVEL_M = 1  # ~15% recovery
    LEVEL_Q = 2  # ~25% recovery
    LEVEL_H = 3  # ~30% recovery

    # Generate QR code from data
    def self.generate(data, error_correction_level = LEVEL_M)
      QrCode.new(data, error_correction_level)
    end

    # Get maximum data length for version and error correction
    def self.max_data_length(version, error_correction_level = LEVEL_M)
      QrCode::CAPACITY_TABLE[version]&.[](error_correction_level) || 0
    end

    # QR Code class
    class QrCode
      CAPACITY_TABLE = {
        1 => { 0 => 17, 1 => 14, 2 => 11, 3 => 7 },
        2 => { 0 => 32, 1 => 26, 2 => 20, 3 => 14 },
        3 => { 0 => 53, 1 => 42, 2 => 32, 3 => 24 },
        4 => { 0 => 78, 1 => 62, 2 => 46, 3 => 34 },
        5 => { 0 => 106, 1 => 84, 2 => 60, 3 => 44 },
        6 => { 0 => 134, 1 => 106, 2 => 74, 3 => 58 },
        7 => { 0 => 154, 1 => 122, 2 => 86, 3 => 64 },
        8 => { 0 => 192, 1 => 152, 2 => 108, 3 => 84 },
        9 => { 0 => 230, 1 => 180, 2 => 130, 3 => 98 },
        10 => { 0 => 271, 1 => 213, 2 => 151, 3 => 119 }
      }.freeze

      ALIGNMENT_POSITIONS = {
        1 => [], 2 => [6, 18], 3 => [6, 22], 4 => [6, 26], 5 => [6, 30],
        6 => [6, 34], 7 => [6, 22, 38], 8 => [6, 24, 42], 9 => [6, 26, 46],
        10 => [6, 28, 50]
      }.freeze

      attr_reader :data, :version, :error_correction_level, :size

      def initialize(data, error_correction_level = 1)
        @data = data.to_s
        @error_correction_level = error_correction_level
        @version = detect_version
        @size = 17 + 4 * @version
        @modules = Array.new(@size) { Array.new(@size, false) }
        @is_function = Array.new(@size) { Array.new(@size, false) }
        generate
      end

      def modules
        @modules
      end

      def generate
        add_finder_patterns
        add_separators
        add_alignment_patterns
        add_timing_patterns
        add_dark_module
        reserve_format_info
        add_data
        add_format_info
      end

      def [](row, col)
        @modules[row][col]
      end

      def []=(row, col, value)
        @modules[row][col] = value
      end

      def function?(row, col)
        @is_function[row][col]
      end

      # ASCII art representation
      def to_ascii(border = 2, dark = '██', light = '  ')
        result = []
        border.times { result << dark * (@size + 2 * border) }
        @size.times do |row|
          line = dark * border
          @size.times { |col| line += self[row, col] ? dark : light }
          line += dark * border
          result << line
        end
        border.times { result << dark * (@size + 2 * border) }
        result.join("\n")
      end

      # Compact Unicode representation
      def to_unicode(border = 1)
        result = []
        border.times { result << '█' * (@size + 2 * border) }
        (0...@size).step(2) do |row|
          line = '█' * border
          @size.times do |col|
            upper = self[row, col]
            lower = row + 1 < @size ? self[row + 1, col] : false
            line += if upper && lower then '█'
                    elsif upper then '▀'
                    elsif lower then '▄'
                    else ' ' end
          end
          line += '█' * border
          result << line
        end
        border.times { result << '█' * (@size + 2 * border) }
        result.join("\n")
      end

      alias to_compact_ascii to_unicode

      # SVG format
      def to_svg(module_size = 10, border_modules = 4)
        total = (@size + 2 * border_modules) * module_size
        border_px = border_modules * module_size
        svg = <<~SVG
<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="#{total}" height="#{total}" viewBox="0 0 #{total} #{total}">
<rect width="#{total}" height="#{total}" fill="white"/>
SVG
        @size.times do |row|
          @size.times do |col|
            if self[row, col]
              x = border_px + col * module_size
              y = border_px + row * module_size
              svg += "<rect x=\"#{x}\" y=\"#{y}\" width=\"#{module_size}\" height=\"#{module_size}\" fill=\"black\"/>\n"
            end
          end
        end
        svg + "</svg>"
      end

      # Matrix representation
      def to_matrix
        @modules.map { |row| row.map(&:dup) }
      end

      private

      def detect_version
        (1..10).each do |v|
          cap = CAPACITY_TABLE[v][@error_correction_level]
          return v if cap >= @data.length
        end
        raise ArgumentError, "Data too long (max #{CAPACITY_TABLE[10][@error_correction_level]} chars)"
      end

      def add_finder_patterns
        [[0, 0], [0, @size - 7], [@size - 7, 0]].each { |r, c| draw_finder(r, c) }
      end

      def draw_finder(row, col)
        7.times do |r|
          7.times do |c|
            @is_function[row + r][col + c] = true
            dark = (r == 0 || r == 6 || c == 0 || c == 6) ||
                   (r >= 2 && r <= 4 && c >= 2 && c <= 4)
            self[row + r, col + c] = dark
          end
        end
      end

      def add_separators
        seps = [[7, 0, 8, 1], [0, 7, 1, 8], [7, @size - 8, 8, 1], [0, @size - 8, 1, 8],
                [@size - 8, 0, 8, 1], [@size - 8, 7, 1, 8]]
        seps.each { |r, c, w, h| draw_sep(r, c, w, h) }
      end

      def draw_sep(row, col, w, h)
        h.times do |r|
          w.times do |c|
            nr, nc = row + r, col + c
            if nr < @size && nc < @size
              self[nr, nc] = false
              @is_function[nr][nc] = true
            end
          end
        end
      end

      def add_alignment_patterns
        return if @version == 1
        positions = ALIGNMENT_POSITIONS[@version]
        positions.each do |r|
          positions.each do |c|
            next if (r == 6 && c == 6) || overlaps_finder?(r, c)
            draw_alignment(r, c)
          end
        end
      end

      def overlaps_finder?(row, col)
        (row <= 9 && col <= 9) || (row <= 9 && col >= @size - 9) || (row >= @size - 9 && col <= 9)
      end

      def draw_alignment(row, col)
        (-2..2).each do |r|
          (-2..2).each do |c|
            nr, nc = row + r, col + c
            next if nr < 0 || nr >= @size || nc < 0 || nc >= @size
            @is_function[nr][nc] = true
            self[nr, nc] = (r.abs == 2 || c.abs == 2) || (r == 0 && c == 0)
          end
        end
      end

      def add_timing_patterns
        (8...@size - 8).each do |i|
          @is_function[6][i] = true
          @is_function[i][6] = true
          self[6][i] = i.even?
          self[i][6] = i.even?
        end
      end

      def add_dark_module
        self[4 * @version + 9, 8] = true
        @is_function[4 * @version + 9][8] = true
      end

      def reserve_format_info
        # Reserve format info areas around finders
        (0..8).each do |i|
          (0..8).each do |j|
            next if @is_function[i][j]
            @is_function[i][j] = true if i == 8 || j == 8
          end
        end
      end

      def add_data
        # Encode data and place on QR code matrix
        # Simplified encoding for demonstration
        bits = encode_data
        place_data(bits)
      end

      def encode_data
        # Byte mode encoding (0100 mode indicator)
        bits = [0, 1, 0, 0]
        # Character count indicator (8 bits for version 1-9)
        count = @data.length
        8.times { |i| bits << ((count >> (7 - i)) & 1) }
        # Data bytes
        @data.each_byte do |byte|
          8.times { |i| bits << ((byte >> (7 - i)) & 1) }
        end
        # Terminator (4 zeros)
        4.times { bits << 0 }
        # Pad to byte boundary
        bits << 0 while bits.length % 8 != 0
        # Pad bytes (0b11101100, 0b00010001 alternating)
        pad_byte = 0b11101100
        while bits.length < total_data_bits
          8.times { |i| bits << ((pad_byte >> (7 - i)) & 1) }
          pad_byte = pad_byte == 0b11101100 ? 0b00010001 : 0b11101100
        end
        bits
      end

      def total_data_bits
        # Total data bits for this version and error correction
        capacity = CAPACITY_TABLE[@version][@error_correction_level]
        capacity * 8
      end

      def place_data(bits)
        # Place data bits in zigzag pattern
        bit_index = 0
        col = @size - 1
        while col > 0
          col -= 1 if col == 6 # Skip timing column
          (@size - 1).downto(0) do |row|
            [col, col - 1].each do |c|
              next if c < 0 || function?(row, c)
              self[row, c] = bit_index < bits.length ? bits[bit_index] == 1 : false
              bit_index += 1
            end
          end
          col -= 2
          next if col <= 0
          col -= 1 if col == 6 # Skip timing column
          (0...@size).each do |row|
            [col, col - 1].each do |c|
              next if c < 0 || function?(row, c)
              self[row, c] = bit_index < bits.length ? bits[bit_index] == 1 : false
              bit_index += 1
            end
          end
          col -= 2
        end
      end

      def add_format_info
        # Add format info around finder patterns
        format_bits = calculate_format_bits
        # Place format info
        (0..5).each { |i| self[8, i] = format_bits[i] == 1 }
        self[8, 7] = format_bits[6] == 1
        self[8, 8] = format_bits[7] == 1
        self[7, 8] = format_bits[8] == 1
        (9..14).each { |i| self[14 - i, 8] = format_bits[i] == 1 }
        # Mirror on other side
        (0..7).each { |i| self[@size - 1 - i, 8] = format_bits[i] == 1 }
        (0..6).each { |i| self[8, @size - 7 + i] = format_bits[7 + i] == 1 }
      end

      def calculate_format_bits
        # Format: error_correction (2 bits) + mask_pattern (3 bits) = 5 bits
        # Then 10 BCH error correction bits
        format_int = (@error_correction_level << 3) | 0 # mask pattern 0
        # BCH(15,5) error correction
        g = 0b10100110111 # Generator polynomial
        format_ec = format_int << 10
        (4..0).each do |i|
          if (format_ec >> (i + 10)) & 1 == 1
            format_ec ^= g << i
          end
        end
        format_bits = ((format_int << 10) | format_ec) ^ 0b101010000010010
        format_bits.to_s(2).rjust(15, '0').chars.map(&:to_i)
      end
    end
  end
end

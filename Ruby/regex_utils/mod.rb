# frozen_string_literal: true

# AllToolkit - Ruby Regex Utilities
# A comprehensive regular expression utility module for Ruby
#
# Features:
# - Zero dependencies, uses only Ruby standard library
# - Pattern matching and extraction
# - Validation helpers
# - String manipulation with regex
# - Named capture group support
# - Common pattern presets
#
# @author AllToolkit Contributors
# @version 1.0.0

module AllToolkit
  # Regular Expression Utilities Module
  module RegexUtils
    # Common regex patterns for validation
    PATTERNS = {
      # Email pattern (RFC 5322 compliant, simplified)
      email: /\A[\w+\-.]+@[a-z\d\-]+(\.[a-z\d\-]+)*\.[a-z]+\z/i,

      # URL pattern (http/https)
      url: /\Ahttps?:\/\/(?:[\w-]+\.)*[\w-]+(?:\:\d+)?(?:\/[^\s]*)?\z/i,

      # IPv4 address
      ipv4: /\A(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\z/,

      # IPv6 address (simplified)
      ipv6: /\A(?:[0-9a-fA-F]{1,4}\:){7}[0-9a-fA-F]{1,4}\z/,

      # Phone number (international format)
      phone: /\A\+?[\d\s\-\(\)]{7,20}\z/,

      # Credit card (basic pattern)
      credit_card: /\A(?:\d{4}[-\s]?){3}\d{4}\z/,

      # Hex color (#RGB or #RRGGBB)
      hex_color: /\A#(?:[\da-fA-F]{3}){1,2}\z/,

      # Date: YYYY-MM-DD
      date_iso: /\A\d{4}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12]\d|3[01])\z/,

      # Date: MM/DD/YYYY
      date_us: /\A(?:0[1-9]|1[0-2])\/(?:0[1-9]|[12]\d|3[01])\/\d{4}\z/,

      # Date: DD/MM/YYYY
      date_uk: /\A(?:0[1-9]|[12]\d|3[01])\/(?:0[1-9]|1[0-2])\/\d{4}\z/,

      # Time: HH:MM:SS
      time: /\A(?:[01]?\d|2[0-3]):[0-5]\d(?::[0-5]\d)?\z/,

      # UUID v4
      uuid: /\A[\da-f]{8}-[\da-f]{4}-4[\da-f]{3}-[89ab][\da-f]{3}-[\da-f]{12}\z/i,

      # UUID (any version, compact format)
      uuid_compact: /\A[\da-f]{32}\z/i,

      # Alphanumeric only
      alphanumeric: /\A[\da-zA-Z]+\z/,

      # Alphabetic only
      alpha: /\A[a-zA-Z]+\z/,

      # Numeric only
      numeric: /\A-?\d+\z/,

      # Decimal number
      decimal: /\A-?\d+(?:\.\d+)?\z/,

      # Whitespace only
      whitespace: /\A\s*\z/,

      # HTML tag
      html_tag: /<\/?[\w\s="']*>/,

      # Markdown link
      markdown_link: /\[([^\]]+)\]\(([^\)]+)\)/,

      # File extension
      file_extension: /\.(\w+)$/,

      # Twitter handle
      twitter_handle: /\A@?[\w_]{1,15}\z/,

      # Hashtag
      hashtag: /#\w+/,

      # MAC address
      mac_address: /\A(?:[\da-fA-F]{2}[:-]){5}[\da-fA-F]{2}\z/,

      # Postal code (US ZIP)
      zip_code: /\A\d{5}(?:-\d{4})?\z/,

      # SSN (US format)
      ssn: /\A\d{3}-\d{2}-\d{4}\z/
    }.freeze

    # Match result class
    class MatchResult
      attr_reader :success, :matches, :named_groups, :original

      def initialize(success:, matches:, named_groups:, original:)
        @success = success
        @matches = matches
        @named_groups = named_groups
        @original = original
      end

      def success?
        @success
      end

      def [](index)
        @matches[index]
      end

      def first
        @matches.first
      end

      def last
        @matches.last
      end

      def empty?
        @matches.empty?
      end

      def to_a
        @matches
      end

      def to_s
        @matches.join(', ')
      end
    end

    # Check if string matches pattern
    #
    # @param str [String] The string to check
    # @param pattern [Regexp, Symbol] The regex pattern or preset symbol
    # @return [Boolean] true if matches, false otherwise
    #
    # @example
    #   RegexUtils.match?("test@example.com", :email) # => true
    #   RegexUtils.match?("hello", /\Ahello\z/) # => true
    def self.match?(str, pattern)
      return false if str.nil?

      regex = pattern.is_a?(Symbol) ? PATTERNS[pattern] : pattern
      return false unless regex

      regex.match?(str.to_s)
    end

    # Check if string does not match pattern
    #
    # @param str [String] The string to check
    # @param pattern [Regexp, Symbol] The regex pattern or preset symbol
    # @return [Boolean] true if does not match, false otherwise
    def self.no_match?(str, pattern)
      !match?(str, pattern)
    end

    # Find first match in string
    #
    # @param str [String] The string to search
    # @param pattern [Regexp, Symbol] The regex pattern or preset symbol
    # @return [MatchResult] Match result object
    #
    # @example
    #   result = RegexUtils.find("hello world", /\w+/)
    #   result.success? # => true
    #   result.first # => "hello"
    def self.find(str, pattern)
      return MatchResult.new(success: false, matches: [], named_groups: {}, original: str) if str.nil?

      regex = pattern.is_a?(Symbol) ? PATTERNS[pattern] : pattern
      return MatchResult.new(success: false, matches: [], named_groups: {}, original: str) unless regex

      match = regex.match(str.to_s)
      if match
        matches = match.to_a
        named_groups = match.named_captures || {}
        MatchResult.new(success: true, matches: matches, named_groups: named_groups, original: str)
      else
        MatchResult.new(success: false, matches: [], named_groups: {}, original: str)
      end
    end

    # Find all matches in string
    #
    # @param str [String] The string to search
    # @param pattern [Regexp, Symbol] The regex pattern or preset symbol
    # @return [Array<String>] Array of all matches
    #
    # @example
    #   RegexUtils.find_all("a1b2c3", /\d+/) # => ["1", "2", "3"]
    def self.find_all(str, pattern)
      return [] if str.nil?

      regex = pattern.is_a?(Symbol) ? PATTERNS[pattern] : pattern
      return [] unless regex

      str.to_s.scan(regex).flatten
    end

    # Find all matches with capture groups
    #
    # @param str [String] The string to search
    # @param pattern [Regexp, Symbol] The regex pattern or preset symbol
    # @return [Array<MatchResult>] Array of match results
    def self.find_all_with_groups(str, pattern)
      return [] if str.nil?

      regex = pattern.is_a?(Symbol) ? PATTERNS[pattern] : pattern
      return [] unless regex

      str.to_s.to_enum(:scan, regex).map do
        match = Regexp.last_match
        MatchResult.new(
          success: true,
          matches: match.to_a,
          named_groups: match.named_captures || {},
          original: str
        )
      end
    end

    # Replace first occurrence
    #
    # @param str [String] The string to modify
    # @param pattern [Regexp, Symbol] The regex pattern or preset symbol
    # @param replacement [String, Proc] The replacement string or block
    # @return [String] Modified string
    #
    # @example
    #   RegexUtils.replace_first("hello world", /\w+/, "hi") # => "hi world"
    def self.replace_first(str, pattern, replacement)
      return str if str.nil?

      regex = pattern.is_a?(Symbol) ? PATTERNS[pattern] : pattern
      return str unless regex

      if replacement.is_a?(Proc)
        str.to_s.sub(regex) { |match| replacement.call(match) }
      else
        str.to_s.sub(regex, replacement.to_s)
      end
    end

    # Replace all occurrences
    #
    # @param str [String] The string to modify
    # @param pattern [Regexp, Symbol] The regex pattern or preset symbol
    # @param replacement [String, Proc] The replacement string or block
    # @return [String] Modified string
    #
    # @example
    #   RegexUtils.replace_all("a1b2c3", /\d/, "X") # => "aXbXcX"
    def self.replace_all(str, pattern, replacement)
      return str if str.nil?

      regex = pattern.is_a?(Symbol) ? PATTERNS[pattern] : pattern
      return str unless regex

      if replacement.is_a?(Proc)
        str.to_s.gsub(regex) { |match| replacement.call(match) }
      else
        str.to_s.gsub(regex, replacement.to_s)
      end
    end

    # Split string by pattern
    #
    # @param str [String] The string to split
    # @param pattern [Regexp, Symbol] The regex pattern or preset symbol
    # @return [Array<String>] Array of split parts
    #
    # @example
    #   RegexUtils.split("a,b,c", /,/) # => ["a", "b", "c"]
    def self.split(str, pattern)
      return [] if str.nil?

      regex = pattern.is_a?(Symbol) ? PATTERNS[pattern] : pattern
      return [str.to_s] unless regex

      str.to_s.split(regex)
    end

    # Extract specific capture group
    #
    # @param str [String] The string to search
    # @param pattern [Regexp, Symbol] The regex pattern or preset symbol
    # @param group [Integer, String] The capture group index or name
    # @return [String, nil] The captured group or nil
    #
    # @example
    #   RegexUtils.extract("hello world", /(\w+) (\w+)/, 1) # => "hello"
    #   RegexUtils.extract("hello world", /(?<first>\w+)/, "first") # => "hello"
    def self.extract(str, pattern, group = 0)
      return nil if str.nil?

      regex = pattern.is_a?(Symbol) ? PATTERNS[pattern] : pattern
      return nil unless regex

      match = regex.match(str.to_s)
      return nil unless match

      if group.is_a?(String)
        match[group]
      else
        match[group]
      end
    end

    # Remove all matches from string
    #
    # @param str [String] The string to modify
    # @param pattern [Regexp, Symbol] The regex pattern or preset symbol
    # @return [String] Modified string with matches removed
    #
    # @example
    #   RegexUtils.remove("a1b2c3", /\d/) # => "abc"
    def self.remove(str, pattern)
      replace_all(str, pattern, "")
    end

    # Remove first match from string
    #
    # @param str [String] The string to modify
    # @param pattern [Regexp, Symbol] The regex pattern or preset symbol
    # @return [String] Modified string with first match removed
    def self.remove_first(str, pattern)
      replace_first(str, pattern, "")
    end

    # Count matches in string
    #
    # @param str [String] The string to search
    # @param pattern [Regexp, Symbol] The regex pattern or preset symbol
    # @return [Integer] Number of matches
    #
    # @example
    #   RegexUtils.count("a1b2c3", /\d/) # => 3
    def self.count(str, pattern)
      find_all(str, pattern).length
    end

    # Check if string contains pattern
    #
    # @param str [String] The string to check
    # @param pattern [Regexp, Symbol] The regex pattern or preset symbol
    # @return [Boolean] true if contains, false otherwise
    #
    # @example
    #   RegexUtils.contains?("hello world", /world/) # => true
    def self.contains?(str, pattern)
      return false if str.nil?

      regex = pattern.is_a?(Symbol) ? PATTERNS[pattern] : pattern
      return false unless regex

      str.to_s.match?(regex)
    end

    # Escape special regex characters in string
    #
    # @param str [String] The string to escape
    # @return [String] Escaped string
    #
    # @example
    #   RegexUtils.escape("a.b") # => "a\\.b"
    def self.escape(str)
      return "" if str.nil?

      Regexp.escape(str.to_s)
    end

    # Build regex from pattern string
    #
    # @param pattern [String] The pattern string
    # @param options [Integer] Regex options (Regexp::IGNORECASE, etc.)
    # @return [Regexp] Compiled regex
    #
    # @example
    #   RegexUtils.build("hello", Regexp::IGNORECASE) # => /hello/i
    def self.build(pattern, options = 0)
      return nil if pattern.nil?

      Regexp.new(pattern.to_s, options)
    end

    # Validate using preset pattern
    #
    # @param str [String] The string to validate
    # @param preset [Symbol] The preset pattern name
    # @return [Boolean] true if valid, false otherwise
    #
    # @example
    #   RegexUtils.valid?("test@example.com", :email) # => true
    #   RegexUtils.valid?("192.168.1.1", :ipv4) # => true
    def self.valid?(str, preset)
      match?(str, preset)
    end

    # Get list of available pattern presets
    #
    # @return [Array<Symbol>] Array of preset names
    def self.presets
      PATTERNS.keys
    end

    # Get pattern by preset name
    #
    # @param name [Symbol] The preset name
    # @return [Regexp, nil] The regex pattern or nil
    def self.get_preset(name)
      PATTERNS[name]
    end

    # Check if preset exists
    #
    # @param name [Symbol] The preset name
    # @return [Boolean] true if exists, false otherwise
    def self.preset_exists?(name)
      PATTERNS.key?(name)
    end
  end
end

# Convenience alias
RegexUtils = AllToolkit::RegexUtils

# frozen_string_literal: true

##
# Levenshtein Distance Utilities
# 
# A pure Ruby implementation of the Levenshtein distance algorithm for
# measuring the difference between two strings. Zero external dependencies.
#
# Features:
# - Classic Levenshtein distance calculation
# - Normalized similarity score (0.0 to 1.0)
# - Damerau-Levenshtein distance (with transpositions)
# - Optimal alignment tracing
# - Fuzzy matching helpers
# - Batch comparison utilities
#
# @author AllToolkit
# @version 1.0.0
##

module LevenshteinUtils
  # Calculate the Levenshtein distance between two strings
  # 
  # The Levenshtein distance is the minimum number of single-character edits
  # (insertions, deletions, or substitutions) required to change one string
  # into the other.
  #
  # @param str1 [String] First string
  # @param str2 [String] Second string
  # @param options [Hash] Options for calculation
  # @option options [Integer] :insertion_cost (1) Cost of inserting a character
  # @option options [Integer] :deletion_cost (1) Cost of deleting a character
  # @option options [Integer] :substitution_cost (1) Cost of substituting a character
  # @option options [Boolean] :case_sensitive (true) Whether to consider case
  #
  # @return [Integer] The Levenshtein distance
  #
  # @example Basic usage
  #   LevenshteinUtils.distance("kitten", "sitting") #=> 3
  #
  # @example Case insensitive
  #   LevenshteinUtils.distance("Hello", "hello", case_sensitive: false) #=> 0
  #
  # @example With custom costs
  #   LevenshteinUtils.distance("abc", "abd", substitution_cost: 2) #=> 2
  ##
  def self.distance(str1, str2, options = {})
    return 0 if str1 == str2
    return str2.length if str1.empty?
    return str1.length if str2.empty?

    # Handle case sensitivity (default: case sensitive)
    str1 = str1.to_s.downcase if options[:case_sensitive] == false
    str2 = str2.to_s.downcase if options[:case_sensitive] == false

    # Get cost options
    ins_cost = options[:insertion_cost] || 1
    del_cost = options[:deletion_cost] || 1
    sub_cost = options[:substitution_cost] || 1

    # Optimize by using the shorter string as the inner loop
    if str1.length < str2.length
      str1, str2 = str2, str1
      ins_cost, del_cost = del_cost, ins_cost
    end

    len1 = str1.length
    len2 = str2.length

    # Use two rows instead of full matrix for memory efficiency
    prev_row = Array.new(len2 + 1) { |i| i * ins_cost }
    curr_row = Array.new(len2 + 1, 0)

    (1..len1).each do |i|
      curr_row[0] = i * del_cost
      
      (1..len2).each do |j|
        if str1[i - 1] == str2[j - 1]
          curr_row[j] = prev_row[j - 1]
        else
          curr_row[j] = [
            prev_row[j] + del_cost,           # deletion
            curr_row[j - 1] + ins_cost,       # insertion
            prev_row[j - 1] + sub_cost        # substitution
          ].min
        end
      end
      
      prev_row, curr_row = curr_row, prev_row
    end

    prev_row[len2]
  end

  # Calculate normalized similarity between two strings
  # 
  # Returns a value between 0.0 (completely different) and 1.0 (identical).
  # The similarity is calculated as: 1 - (distance / max_length)
  #
  # @param str1 [String] First string
  # @param str2 [String] Second string
  # @param options [Hash] Options passed to distance calculation
  #
  # @return [Float] Similarity score between 0.0 and 1.0
  #
  # @example
  #   LevenshteinUtils.similarity("hello", "hallo") #=> 0.8
  #   LevenshteinUtils.similarity("cat", "dog")     #=> 0.0
  ##
  def self.similarity(str1, str2, options = {})
    return 1.0 if str1 == str2
    return 0.0 if str1.empty? || str2.empty?

    max_len = [str1.length, str2.length].max
    return 1.0 if max_len.zero?

    dist = distance(str1, str2, options)
    1.0 - (dist.to_f / max_len)
  end

  # Calculate Damerau-Levenshtein distance
  # 
  # Includes transposition as a valid operation (swapping adjacent characters).
  # This is useful for catching common typing errors like "teh" vs "the".
  #
  # @param str1 [String] First string
  # @param str2 [String] Second string
  # @param options [Hash] Options for calculation
  # @option options [Boolean] :case_sensitive (true) Whether to consider case
  # @option options [Integer] :transposition_cost (1) Cost of transposing adjacent chars
  #
  # @return [Integer] The Damerau-Levenshtein distance
  #
  # @example
  #   LevenshteinUtils.damerau_distance("ca", "abc") #=> 2
  #   LevenshteinUtils.damerau_distance("teh", "the") #=> 1 (transposition)
  ##
  def self.damerau_distance(str1, str2, options = {})
    return 0 if str1 == str2
    return str2.length if str1.empty?
    return str1.length if str2.empty?

    str1 = str1.to_s.downcase if options[:case_sensitive] == false
    str2 = str2.to_s.downcase if options[:case_sensitive] == false

    trans_cost = options[:transposition_cost] || 1

    len1 = str1.length
    len2 = str2.length

    # Use a full matrix for Damerau-Levenshtein
    matrix = Array.new(len1 + 1) { Array.new(len2 + 1, 0) }

    # Initialize first column and row
    (0..len1).each { |i| matrix[i][0] = i }
    (0..len2).each { |j| matrix[0][j] = j }

    (1..len1).each do |i|
      (1..len2).each do |j|
        cost = str1[i - 1] == str2[j - 1] ? 0 : 1

        matrix[i][j] = [
          matrix[i - 1][j] + 1,      # deletion
          matrix[i][j - 1] + 1,      # insertion
          matrix[i - 1][j - 1] + cost # substitution
        ].min

        # Check for transposition
        if i > 1 && j > 1 && 
           str1[i - 1] == str2[j - 2] && 
           str1[i - 2] == str2[j - 1]
          matrix[i][j] = [matrix[i][j], matrix[i - 2][j - 2] + trans_cost].min
        end
      end
    end

    matrix[len1][len2]
  end

  # Find the closest match from a list of candidates
  # 
  # @param target [String] The string to match
  # @param candidates [Array<String>] List of candidate strings
  # @param options [Hash] Options for calculation
  # @option options [Float] :threshold (0.0) Minimum similarity threshold
  # @option options [Integer] :limit (1) Maximum number of results to return
  # @option options [Boolean] :use_damerau (false) Use Damerau-Levenshtein
  #
  # @return [Array<Hash>] Array of matches with :string, :distance, :similarity
  #
  # @example Basic usage
  #   LevenshteinUtils.closest_match("aple", ["apple", "orange", "grape"])
  #   #=> [{string: "apple", distance: 1, similarity: 0.8}]
  #
  # @example With threshold
  #   LevenshteinUtils.closest_match("xxx", ["apple", "orange"], threshold: 0.5)
  #   #=> []
  ##
  def self.closest_match(target, candidates, options = {})
    threshold = options[:threshold] || 0.0
    limit = options[:limit] || 1
    use_damerau = options[:use_damerau] || false

    results = candidates.map do |candidate|
      dist = use_damerau ? 
        damerau_distance(target, candidate, options) : 
        distance(target, candidate, options)
      sim = similarity(target, candidate, options.merge(
        use_damerau ? { transposition_cost: 1 } : {}
      ))
      
      # Recalculate similarity manually for damerau
      if use_damerau
        max_len = [target.length, candidate.length].max
        sim = max_len.zero? ? 1.0 : 1.0 - (dist.to_f / max_len)
      end
      
      { string: candidate, distance: dist, similarity: sim }
    end

    # Filter by threshold and sort by similarity (descending)
    results
      .select { |r| r[:similarity] >= threshold }
      .sort_by { |r| [-r[:similarity], r[:distance]] }
      .take(limit)
  end

  # Check if two strings are within a given edit distance
  # 
  # @param str1 [String] First string
  # @param str2 [String] Second string
  # @param max_distance [Integer] Maximum allowed edit distance
  # @param options [Hash] Options passed to distance calculation
  #
  # @return [Boolean] True if distance <= max_distance
  #
  # @example
  #   LevenshteinUtils.within_distance?("hello", "hallo", 1) #=> true
  #   LevenshteinUtils.within_distance?("hello", "world", 2) #=> false
  ##
  def self.within_distance?(str1, str2, max_distance, options = {})
    distance(str1, str2, options) <= max_distance
  end

  # Get the edit operations to transform str1 into str2
  # 
  # @param str1 [String] Source string
  # @param str2 [String] Target string
  # @param options [Hash] Options for calculation
  #
  # @return [Array<Hash>] Array of operations with :type, :position, :char
  #
  # @example
  #   LevenshteinUtils.edit_operations("kitten", "sitting")
  #   #=> [
  #     {type: :substitute, position: 0, char: "s", old_char: "k"},
  #     {type: :substitute, position: 4, char: "i", old_char: "e"},
  #     {type: :insert, position: 6, char: "g"}
  #   ]
  ##
  def self.edit_operations(str1, str2, options = {})
    str1 = str1.to_s.downcase if options[:case_sensitive] == false
    str2 = str2.to_s.downcase if options[:case_sensitive] == false

    len1 = str1.length
    len2 = str2.length

    return str2.chars.each_with_index.map { |c, i| { type: :insert, position: i, char: c } } if len1.zero?
    return str1.chars.each_with_index.map { |c, i| { type: :delete, position: i, char: c } } if len2.zero?

    # Build full matrix for backtracking
    matrix = Array.new(len1 + 1) { Array.new(len2 + 1, 0) }

    (0..len1).each { |i| matrix[i][0] = i }
    (0..len2).each { |j| matrix[0][j] = j }

    (1..len1).each do |i|
      (1..len2).each do |j|
        cost = str1[i - 1] == str2[j - 1] ? 0 : 1
        matrix[i][j] = [
          matrix[i - 1][j] + 1,      # deletion
          matrix[i][j - 1] + 1,      # insertion
          matrix[i - 1][j - 1] + cost # substitution
        ].min
      end
    end

    # Backtrack to find operations
    operations = []
    i, j = len1, len2

    while i > 0 || j > 0
      if i > 0 && j > 0 && str1[i - 1] == str2[j - 1]
        i -= 1
        j -= 1
        next
      end

      current = matrix[i][j]
      
      if j > 0 && current == matrix[i][j - 1] + 1
        operations.unshift({ type: :insert, position: i, char: str2[j - 1] })
        j -= 1
      elsif i > 0 && current == matrix[i - 1][j] + 1
        operations.unshift({ type: :delete, position: i - 1, char: str1[i - 1] })
        i -= 1
      elsif i > 0 && j > 0
        operations.unshift({ 
          type: :substitute, 
          position: i - 1, 
          char: str2[j - 1],
          old_char: str1[i - 1]
        })
        i -= 1
        j -= 1
      end
    end

    operations
  end

  # Calculate the Levenshtein distance ratio (0.0 to 1.0)
  # Alias for similarity method
  #
  # @param str1 [String] First string
  # @param str2 [String] Second string
  # @param options [Hash] Options passed to distance calculation
  #
  # @return [Float] Ratio between 0.0 and 1.0
  ##
  def self.ratio(str1, str2, options = {})
    similarity(str1, str2, options)
  end

  # Find all strings within a maximum distance from target
  # 
  # @param target [String] The target string
  # @param candidates [Array<String>] List of candidate strings
  # @param max_distance [Integer] Maximum edit distance
  # @param options [Hash] Options passed to distance calculation
  #
  # @return [Array<String>] Strings within the maximum distance
  #
  # @example
  #   LevenshteinUtils.find_within("cat", ["cat", "bat", "rat", "car", "dog"], 1)
  #   #=> ["cat", "bat", "rat", "car"]
  ##
  def self.find_within(target, candidates, max_distance, options = {})
    candidates.select do |candidate|
      distance(target, candidate, options) <= max_distance
    end
  end

  # Calculate Jaro-Winkler similarity
  # 
  # Jaro-Winkler gives higher weight to strings that match from the beginning.
  # More suitable for comparing short strings like names.
  #
  # @param str1 [String] First string
  # @param str2 [String] Second string
  # @param options [Hash] Options for calculation
  # @option options [Boolean] :case_sensitive (true) Whether to consider case
  # @option options [Float] :scaling_factor (0.1) Weight for common prefix
  #
  # @return [Float] Jaro-Winkler similarity (0.0 to 1.0)
  #
  # @example
  #   LevenshteinUtils.jaro_winkler("MARTHA", "MARHTA") #=> ~0.961
  #   LevenshteinUtils.jaro_winkler("hello", "hallo")   #=> ~0.867
  ##
  def self.jaro_winkler(str1, str2, options = {})
    str1 = str1.to_s.downcase if options[:case_sensitive] == false
    str2 = str2.to_s.downcase if options[:case_sensitive] == false

    return 1.0 if str1 == str2
    return 0.0 if str1.empty? || str2.empty?

    len1 = str1.length
    len2 = str2.length

    # Maximum distance for matching characters
    match_distance = ([len1, len2].max / 2) - 1
    match_distance = 0 if match_distance < 0

    str1_matches = Array.new(len1, false)
    str2_matches = Array.new(len2, false)

    matches = 0
    transpositions = 0

    # Find matching characters
    (0...len1).each do |i|
      start = [0, i - match_distance].max
      finish = [i + match_distance + 1, len2].min

      (start...finish).each do |j|
        next if str2_matches[j] || str1[i] != str2[j]

        str1_matches[i] = true
        str2_matches[j] = true
        matches += 1
        break
      end
    end

    return 0.0 if matches.zero?

    # Count transpositions
    k = 0
    (0...len1).each do |i|
      next unless str1_matches[i]

      k += 1 until str2_matches[k]
      transpositions += 1 if str1[i] != str2[k]
      k += 1
    end

    # Calculate Jaro similarity
    jaro = (
      matches.to_f / len1 +
      matches.to_f / len2 +
      (matches - transpositions / 2.0) / matches
    ) / 3.0

    # Calculate Jaro-Winkler similarity
    scaling_factor = options[:scaling_factor] || 0.1
    prefix_length = 0

    (0...[len1, len2, 4].min).each do |i|
      break if str1[i] != str2[i]
      prefix_length += 1
    end

    jaro + prefix_length * scaling_factor * (1 - jaro)
  end

  # Hamming distance for equal-length strings
  # 
  # Counts the number of positions at which the corresponding symbols differ.
  # Only defined for strings of equal length.
  #
  # @param str1 [String] First string (must be same length as str2)
  # @param str2 [String] Second string (must be same length as str1)
  # @param options [Hash] Options for calculation
  # @option options [Boolean] :case_sensitive (true) Whether to consider case
  #
  # @return [Integer] Hamming distance
  # @raise [ArgumentError] If strings have different lengths
  #
  # @example
  #   LevenshteinUtils.hamming_distance("karolin", "kathrin") #=> 3
  #   LevenshteinUtils.hamming_distance("1011101", "1001001")  #=> 2
  ##
  def self.hamming_distance(str1, str2, options = {})
    str1 = str1.to_s.downcase if options[:case_sensitive] == false
    str2 = str2.to_s.downcase if options[:case_sensitive] == false

    raise ArgumentError, "Strings must be of equal length" if str1.length != str2.length

    str1.chars.zip(str2.chars).count { |a, b| a != b }
  end

  # Optimal string alignment (OSA) distance
  # A restricted version of Damerau-Levenshtein
  #
  # @param str1 [String] First string
  # @param str2 [String] Second string
  # @param options [Hash] Options for calculation
  #
  # @return [Integer] OSA distance
  ##
  def self.osa_distance(str1, str2, options = {})
    return 0 if str1 == str2
    return str2.length if str1.empty?
    return str1.length if str2.empty?

    str1 = str1.to_s.downcase if options[:case_sensitive] == false
    str2 = str2.to_s.downcase if options[:case_sensitive] == false

    len1 = str1.length
    len2 = str2.length

    matrix = Array.new(len1 + 1) { Array.new(len2 + 1, 0) }

    (0..len1).each { |i| matrix[i][0] = i }
    (0..len2).each { |j| matrix[0][j] = j }

    (1..len1).each do |i|
      (1..len2).each do |j|
        cost = str1[i - 1] == str2[j - 1] ? 0 : 1

        matrix[i][j] = [
          matrix[i - 1][j] + 1,
          matrix[i][j - 1] + 1,
          matrix[i - 1][j - 1] + cost
        ].min

        # Allow transposition only if adjacent characters match in cross pattern
        if i > 1 && j > 1 && 
           str1[i - 1] == str2[j - 2] && 
           str1[i - 2] == str2[j - 1]
          matrix[i][j] = [matrix[i][j], matrix[i - 2][j - 2] + 1].min
        end
      end
    end

    matrix[len1][len2]
  end
end
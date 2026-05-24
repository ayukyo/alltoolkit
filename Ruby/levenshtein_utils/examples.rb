#!/usr/bin/env ruby
# frozen_string_literal: true

require_relative 'levenshtein'

##
# LevenshteinUtils Examples
# Demonstrates various use cases for string similarity calculations.
##

puts "=" * 60
puts "LevenshteinUtils Examples"
puts "=" * 60

# 1. Basic distance calculation
puts "\n[1] Basic Levenshtein Distance"
puts "-" * 40
puts "kitten -> sitting: #{LevenshteinUtils.distance('kitten', 'sitting')}"
puts "hello -> hallo: #{LevenshteinUtils.distance('hello', 'hallo')}"
puts "apple -> orange: #{LevenshteinUtils.distance('apple', 'orange')}"

# 2. Similarity scores
puts "\n[2] Similarity Scores (0.0 to 1.0)"
puts "-" * 40
puts "hello vs hallo: #{LevenshteinUtils.similarity('hello', 'hallo').round(3)}"
puts "kitten vs sitting: #{LevenshteinUtils.similarity('kitten', 'sitting').round(3)}"
puts "identical strings: #{LevenshteinUtils.similarity('test', 'test')}"
puts "completely different: #{LevenshteinUtils.similarity('abc', 'xyz')}"

# 3. Case sensitivity
puts "\n[3] Case Sensitivity"
puts "-" * 40
puts "Hello vs hello (sensitive): #{LevenshteinUtils.distance('Hello', 'hello')}"
puts "Hello vs hello (insensitive): #{LevenshteinUtils.distance('Hello', 'hello', case_sensitive: false)}"

# 4. Damerau-Levenshtein (with transpositions)
puts "\n[4] Damerau-Levenshtein (catches transpositions)"
puts "-" * 40
puts "teh vs the (standard): #{LevenshteinUtils.distance('teh', 'the')}"
puts "teh vs the (damerau): #{LevenshteinUtils.damerau_distance('teh', 'the')}"
puts "ab vs ba (standard): #{LevenshteinUtils.distance('ab', 'ba')}"
puts "ab vs ba (damerau): #{LevenshteinUtils.damerau_distance('ab', 'ba')}"

# 5. Fuzzy matching - closest match
puts "\n[5] Fuzzy Matching - Find Closest Match"
puts "-" * 40
candidates = ['apple', 'banana', 'cherry', 'grape', 'orange']
misspelled = 'aple'

result = LevenshteinUtils.closest_match(misspelled, candidates)
puts "Typo '#{misspelled}' -> Best match: '#{result[0][:string]}'"
puts "  Distance: #{result[0][:distance]}, Similarity: #{result[0][:similarity].round(3)}"

# Multiple suggestions
puts "\nTop 3 suggestions for '#{misspelled}':"
results = LevenshteinUtils.closest_match(misspelled, candidates, limit: 3)
results.each do |r|
  puts "  #{r[:string]} (dist: #{r[:distance]}, sim: #{r[:similarity].round(2)})"
end

# 6. Spell checker example
puts "\n[6] Spell Checker Example"
puts "-" * 40
dictionary = ['the', 'hello', 'world', 'ruby', 'python', 'java', 'code', 'test']
typos = ['teh', 'wrld', 'rubie', 'pyton']

typos.each do |typo|
  match = LevenshteinUtils.closest_match(typo, dictionary, threshold: 0.6)
  if match.any?
    puts "'#{typo}' -> '#{match[0][:string]}' (did you mean?)"
  else
    puts "'#{typo}' -> No close match found"
  end
end

# 7. Edit operations
puts "\n[7] Edit Operations (how to transform)"
puts "-" * 40
ops = LevenshteinUtils.edit_operations('kitten', 'sitting')
puts "Transform 'kitten' to 'sitting':"
ops.each do |op|
  case op[:type]
  when :insert
    puts "  Insert '#{op[:char]}' at position #{op[:position]}"
  when :delete
    puts "  Delete '#{op[:char]}' at position #{op[:position]}"
  when :substitute
    puts "  Substitute '#{op[:old_char]}' with '#{op[:char]}' at position #{op[:position]}"
  end
end

# 8. Jaro-Winkler similarity (better for short strings/names)
puts "\n[8] Jaro-Winkler Similarity"
puts "-" * 40
puts "MARTHA vs MARHTA: #{LevenshteinUtils.jaro_winkler('MARTHA', 'MARHTA').round(4)}"
puts "DWAYNE vs DUANE: #{LevenshteinUtils.jaro_winkler('DWAYNE', 'DUANE').round(4)}"
puts "John vs Jon: #{LevenshteinUtils.jaro_winkler('John', 'Jon').round(4)}"

# 9. Hamming distance (for equal-length strings)
puts "\n[9] Hamming Distance"
puts "-" * 40
puts "karolin vs kathrin: #{LevenshteinUtils.hamming_distance('karolin', 'kathrin')}"
puts "1011101 vs 1001001: #{LevenshteinUtils.hamming_distance('1011101', '1001001')}"

# 10. Custom costs
puts "\n[10] Custom Operation Costs"
puts "-" * 40
puts "abc vs abd (default substitution: 1): #{LevenshteinUtils.distance('abc', 'abd')}"
puts "abc vs abd (substitution cost: 5): #{LevenshteinUtils.distance('abc', 'abd', substitution_cost: 5)}"
puts "a vs ab (default insertion: 1): #{LevenshteinUtils.distance('a', 'ab')}"
puts "a vs ab (insertion cost: 10): #{LevenshteinUtils.distance('a', 'ab', insertion_cost: 10)}"

# 11. Batch filtering
puts "\n[11] Find All Within Distance"
puts "-" * 40
words = ['cat', 'bat', 'rat', 'car', 'dog', 'hat', 'mat', 'can']
puts "Words within 1 edit of 'cat': #{LevenshteinUtils.find_within('cat', words, 1).inspect}"

# 12. Real-world: Duplicate detection
puts "\n[12] Duplicate Detection Example"
puts "-" * 40
names = ['John Smith', 'Jon Smith', 'John Smyth', 'Jane Smith', 'John Doe']
target = 'John Smith'
puts "Finding similar names to '#{target}':"
matches = names.select do |name|
  LevenshteinUtils.similarity(target, name) > 0.8
end
puts "  Potential duplicates: #{matches.inspect}"

puts "\n" + "=" * 60
puts "End of Examples"
puts "=" * 60
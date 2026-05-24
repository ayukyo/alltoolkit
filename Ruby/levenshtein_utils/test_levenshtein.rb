#!/usr/bin/env ruby
# frozen_string_literal: true

require_relative 'levenshtein'

##
# Test suite for LevenshteinUtils
# Run with: ruby test_levenshtein.rb
##

class TestLevenshteinUtils
  def initialize
    @passed = 0
    @failed = 0
    @errors = []
  end

  def assert_equal(expected, actual, test_name)
    if expected == actual
      puts "  ✓ #{test_name}"
      @passed += 1
    else
      puts "  ✗ #{test_name}"
      puts "    Expected: #{expected.inspect}"
      puts "    Actual:   #{actual.inspect}"
      @failed += 1
      @errors << test_name
    end
  end

  def assert_in_delta(expected, actual, delta, test_name)
    if (expected - actual).abs <= delta
      puts "  ✓ #{test_name}"
      @passed += 1
    else
      puts "  ✗ #{test_name}"
      puts "    Expected: #{expected} (±#{delta})"
      puts "    Actual:   #{actual}"
      @failed += 1
      @errors << test_name
    end
  end

  def assert_raises(exception_class, test_name)
    begin
      yield
      puts "  ✗ #{test_name}"
      puts "    Expected exception: #{exception_class}"
      @failed += 1
      @errors << test_name
    rescue exception_class
      puts "  ✓ #{test_name}"
      @passed += 1
    end
  end

  def run_tests
    puts "\n" + "=" * 60
    puts "LevenshteinUtils Test Suite"
    puts "=" * 60 + "\n"

    test_distance
    test_similarity
    test_damerau_distance
    test_closest_match
    test_within_distance
    test_edit_operations
    test_find_within
    test_jaro_winkler
    test_hamming_distance
    test_case_sensitivity
    test_custom_costs
    test_edge_cases

    puts "\n" + "-" * 60
    puts "Results: #{@passed} passed, #{@failed} failed"
    
    if @failed > 0
      puts "\nFailed tests:"
      @errors.each { |e| puts "  - #{e}" }
      exit 1
    else
      puts "All tests passed!"
    end
  end

  def test_distance
    puts "\n[test_distance]"
    
    assert_equal(3, LevenshteinUtils.distance("kitten", "sitting"), "kitten -> sitting")
    assert_equal(1, LevenshteinUtils.distance("hello", "hallo"), "hello -> hallo")
    assert_equal(0, LevenshteinUtils.distance("same", "same"), "identical strings")
    assert_equal(5, LevenshteinUtils.distance("", "hello"), "empty to string")
    assert_equal(5, LevenshteinUtils.distance("hello", ""), "string to empty")
    assert_equal(2, LevenshteinUtils.distance("book", "back"), "book -> back")
    assert_equal(4, LevenshteinUtils.distance("abcd", "dcba"), "abcd -> dcba")
    assert_equal(1, LevenshteinUtils.distance("a", "b"), "single char substitution")
    assert_equal(1, LevenshteinUtils.distance("", "a"), "single char insertion")
    assert_equal(1, LevenshteinUtils.distance("a", ""), "single char deletion")
  end

  def test_similarity
    puts "\n[test_similarity]"
    
    assert_in_delta(1.0, LevenshteinUtils.similarity("hello", "hello"), 0.001, "identical strings")
    assert_in_delta(0.0, LevenshteinUtils.similarity("abc", "xyz"), 0.001, "completely different")
    assert_in_delta(0.8, LevenshteinUtils.similarity("hello", "hallo"), 0.001, "hello vs hallo")
    assert_in_delta(0.571, LevenshteinUtils.similarity("kitten", "sitting"), 0.01, "kitten vs sitting")
    assert_in_delta(0.0, LevenshteinUtils.similarity("", "hello"), 0.001, "empty string similarity")
    assert_in_delta(0.0, LevenshteinUtils.similarity("ab", "cd"), 0.001, "two chars different (both changed)")
  end

  def test_damerau_distance
    puts "\n[test_damerau_distance]"
    
    # Transposition should count as 1, not 2
    assert_equal(1, LevenshteinUtils.damerau_distance("teh", "the"), "teh -> the (transposition)")
    assert_equal(1, LevenshteinUtils.damerau_distance("ab", "ba"), "ab -> ba (swap)")
    assert_equal(3, LevenshteinUtils.damerau_distance("kitten", "sitting"), "kitten -> sitting")
    assert_equal(3, LevenshteinUtils.damerau_distance("ca", "abc"), "ca -> abc")
  end

  def test_closest_match
    puts "\n[test_closest_match]"
    
    result = LevenshteinUtils.closest_match("aple", ["apple", "orange", "grape"])
    assert_equal("apple", result[0][:string], "find closest match - apple")
    assert_equal(1, result[0][:distance], "distance to closest")
    
    # Test with threshold
    result = LevenshteinUtils.closest_match("xxx", ["apple", "orange", "grape"], threshold: 0.3)
    assert_equal(0, result.length, "no matches below threshold")
    
    # Test with limit
    result = LevenshteinUtils.closest_match("aple", ["apple", "apply", "ample", "orange"], limit: 2)
    assert_equal(2, result.length, "limit number of results")
    
    # Test with damerau
    result = LevenshteinUtils.closest_match("teh", ["the", "tea", "ten"], use_damerau: true)
    assert_equal("the", result[0][:string], "damerau catches transposition")
  end

  def test_within_distance
    puts "\n[test_within_distance]"
    
    assert_equal(true, LevenshteinUtils.within_distance?("hello", "hallo", 1), "within 1")
    assert_equal(true, LevenshteinUtils.within_distance?("hello", "hallo", 2), "within 2")
    assert_equal(false, LevenshteinUtils.within_distance?("hello", "world", 2), "not within 2")
    assert_equal(true, LevenshteinUtils.within_distance?("test", "test", 0), "identical within 0")
  end

  def test_edit_operations
    puts "\n[test_edit_operations]"
    
    ops = LevenshteinUtils.edit_operations("kitten", "sitting")
    assert_equal(3, ops.length, "kitten -> sitting operations count")
    
    ops = LevenshteinUtils.edit_operations("", "abc")
    assert_equal(3, ops.length, "empty -> abc insertions")
    assert_equal(:insert, ops[0][:type], "operation type is insert")
    
    ops = LevenshteinUtils.edit_operations("abc", "")
    assert_equal(3, ops.length, "abc -> empty deletions")
    assert_equal(:delete, ops[0][:type], "operation type is delete")
  end

  def test_find_within
    puts "\n[test_find_within]"
    
    candidates = ["cat", "bat", "rat", "car", "dog", "hat"]
    result = LevenshteinUtils.find_within("cat", candidates, 1)
    assert_equal(5, result.length, "find within distance 1 (cat, bat, rat, car, hat)")
    assert_equal(true, result.include?("cat"), "includes exact match")
    assert_equal(true, result.include?("bat"), "includes bat")
    assert_equal(false, result.include?("dog"), "excludes dog")
    
    result = LevenshteinUtils.find_within("cat", candidates, 0)
    assert_equal(1, result.length, "find within distance 0")
    assert_equal("cat", result[0], "only exact match")
  end

  def test_jaro_winkler
    puts "\n[test_jaro_winkler]"
    
    # Jaro-Winkler gives higher scores for matching prefixes
    assert_in_delta(0.961, LevenshteinUtils.jaro_winkler("MARTHA", "MARHTA"), 0.01, "MARTHA vs MARHTA")
    assert_in_delta(0.84, LevenshteinUtils.jaro_winkler("DWAYNE", "DUANE"), 0.01, "DWAYNE vs DUANE")
    assert_in_delta(1.0, LevenshteinUtils.jaro_winkler("hello", "hello"), 0.001, "identical")
    assert_in_delta(0.0, LevenshteinUtils.jaro_winkler("", "hello"), 0.001, "empty string")
  end

  def test_hamming_distance
    puts "\n[test_hamming_distance]"
    
    assert_equal(3, LevenshteinUtils.hamming_distance("karolin", "kathrin"), "karolin vs kathrin")
    assert_equal(3, LevenshteinUtils.hamming_distance("karolin", "kerstin"), "karolin vs kerstin")
    assert_equal(2, LevenshteinUtils.hamming_distance("1011101", "1001001"), "binary strings")
    assert_equal(0, LevenshteinUtils.hamming_distance("same", "same"), "identical strings")
    
    assert_raises(ArgumentError, "different lengths raises error") do
      LevenshteinUtils.hamming_distance("abc", "abcd")
    end
  end

  def test_case_sensitivity
    puts "\n[test_case_sensitivity]"
    
    # Case sensitive (default)
    assert_equal(1, LevenshteinUtils.distance("Hello", "hello"), "case sensitive by default")
    assert_equal(0, LevenshteinUtils.distance("Hello", "hello", case_sensitive: false), "case insensitive")
    
    # With other methods
    assert_in_delta(1.0, LevenshteinUtils.similarity("TEST", "test", case_sensitive: false), 0.001, "similarity case insensitive")
    assert_equal(1, LevenshteinUtils.damerau_distance("Teh", "the", case_sensitive: false), "damerau case insensitive")
  end

  def test_custom_costs
    puts "\n[test_custom_costs]"
    
    # Default costs
    assert_equal(1, LevenshteinUtils.distance("abc", "abd"), "default substitution cost 1")
    
    # Higher substitution cost
    assert_equal(2, LevenshteinUtils.distance("abc", "abd", substitution_cost: 2), "higher substitution cost")
    
    # Different insertion/deletion costs
    dist1 = LevenshteinUtils.distance("a", "ab", insertion_cost: 2)
    assert_equal(2, dist1, "custom insertion cost")
    
    dist2 = LevenshteinUtils.distance("ab", "a", deletion_cost: 2)
    assert_equal(2, dist2, "custom deletion cost")
  end

  def test_edge_cases
    puts "\n[test_edge_cases]"
    
    # Empty strings
    assert_equal(0, LevenshteinUtils.distance("", ""), "empty to empty")
    assert_in_delta(1.0, LevenshteinUtils.similarity("", ""), 0.001, "empty similarity (both empty = identical)")
    
    # Single character
    assert_equal(0, LevenshteinUtils.distance("x", "x"), "single identical char")
    assert_equal(1, LevenshteinUtils.distance("x", "y"), "single different char")
    
    # Unicode support
    assert_equal(4, LevenshteinUtils.distance("café", "coffee"), "unicode strings")
    assert_equal(1, LevenshteinUtils.distance("日本", "日本語"), "Japanese characters")
    
    # Very different strings
    assert_equal(11, LevenshteinUtils.distance("abcdefghijk", "xyz"), "very different strings")
    
    # Longest common subsequence type cases
    assert_equal(3, LevenshteinUtils.distance("abc", "xyz"), "no common chars")
    assert_equal(0, LevenshteinUtils.distance("abcdef", "abcdef"), "full match")
  end
end

# Run tests
TestLevenshteinUtils.new.run_tests
#!/usr/bin/env ruby
# frozen_string_literal: true

# example.rb - CacheUtils Usage Examples
#
# Run with: ruby example.rb
#
# Author: AllToolkit
# Date: 2026-04-20

require_relative 'cache_utils'

puts "=" * 60
puts "CacheUtils Examples"
puts "=" * 60

# Example 1: Basic Operations
puts "\n--- Example 1: Basic Operations ---"
cache = CacheUtils::LRUCache.new(max_size: 100)

cache.set(:name, "Alice")
cache.set(:age, 30)
cache[:city] = "Beijing"

puts "Name: #{cache.get(:name)}"
puts "Age: #{cache[:age]}"
puts "City: #{cache[:city]}"
puts "Has name? #{cache.has_key?(:name)}"
puts "Has country? #{cache.has_key?(:country)}"
puts "Cache size: #{cache.size}"

# Example 2: TTL (Time To Live)
puts "\n--- Example 2: TTL (Time To Live) ---"
ttl_cache = CacheUtils::LRUCache.new(default_ttl: 2) # 2 seconds default
ttl_cache.set(:session, { user_id: 123 })

puts "Session: #{ttl_cache.get(:session)}"
puts "Waiting 2.5 seconds..."
sleep(2.5)
puts "Session after TTL: #{ttl_cache.get(:session)}" # nil (expired)

# Example 3: Fetch with Block
puts "\n--- Example 3: Fetch with Block ---"
fetch_cache = CacheUtils::LRUCache.new

# First call - executes block
result1 = fetch_cache.fetch(:computed) do
  puts "  Computing value..."
  sleep(0.1)
  42
end
puts "First fetch result: #{result1}"

# Second call - returns cached value
result2 = fetch_cache.fetch(:computed) do
  puts "  This won't be printed!"
  0
end
puts "Second fetch result: #{result2}"

# Example 4: LRU Eviction
puts "\n--- Example 4: LRU Eviction ---"
small_cache = CacheUtils::LRUCache.new(max_size: 3)

small_cache.set(:a, 1)
small_cache.set(:b, 2)
small_cache.set(:c, 3)
puts "Added a, b, c. Size: #{small_cache.size}"

small_cache.set(:d, 4) # Evicts :a (least recently used)
puts "Added d. Size: #{small_cache.size}"
puts "a: #{small_cache.get(:a)}" # nil (evicted)
puts "b: #{small_cache.get(:b)}" # 2
puts "c: #{small_cache.get(:c)}" # 3
puts "d: #{small_cache.get(:d)}" # 4

# Example 5: Access Order Affects Eviction
puts "\n--- Example 5: Access Order Affects Eviction ---"
lru_cache = CacheUtils::LRUCache.new(max_size: 3)

lru_cache.set(:x, 1)
lru_cache.set(:y, 2)
lru_cache.set(:z, 3)

lru_cache.get(:x) # Access :x, making it most recently used

lru_cache.set(:w, 4) # Evicts :y (not :x)
puts "x (should exist): #{lru_cache.get(:x)}" # 1
puts "y (should be nil): #{lru_cache.get(:y)}" # nil

# Example 6: Statistics
puts "\n--- Example 6: Statistics ---"
stats_cache = CacheUtils::LRUCache.new(max_size: 5)

stats_cache.set(:key1, "value1")
stats_cache.set(:key2, "value2")

stats_cache.get(:key1)  # hit
stats_cache.get(:key1)  # hit
stats_cache.get(:key2)  # hit
stats_cache.get(:key3)  # miss
stats_cache.get(:key4)  # miss

stats = stats_cache.stats
puts "Hits: #{stats[:hits]}"
puts "Misses: #{stats[:misses]}"
puts "Hit rate: #{(stats_cache.hit_rate * 100).round(2)}%"

# Example 7: Counters
puts "\n--- Example 7: Counters ---"
counter_cache = CacheUtils::LRUCache.new

counter_cache.increment(:views)
counter_cache.increment(:views)
counter_cache.increment(:views, 5)
puts "Views: #{counter_cache.get(:views)}" # 7

counter_cache.decrement(:views, 2)
puts "Views after decrement: #{counter_cache.get(:views)}" # 5

# Example 8: Multi Operations
puts "\n--- Example 8: Multi Operations ---"
multi_cache = CacheUtils::LRUCache.new

multi_cache.set_multi({ apples: 5, oranges: 3, bananas: 8 })
puts "Keys: #{multi_cache.keys.sort}"
puts "Values: #{multi_cache.values.sort}"

fruits = multi_cache.get_multi(:apples, :oranges, :pears)
puts "Selected fruits: #{fruits}"

# Example 9: Entry Info
puts "\n--- Example 9: Entry Info ---"
info_cache = CacheUtils::LRUCache.new
info_cache.set(:temp, "data", ttl: 60)

info = info_cache.entry_info(:temp)
puts "Entry info:"
puts "  Key: #{info[:key]}"
puts "  Value: #{info[:value]}"
puts "  Age: #{info[:age]} seconds"
puts "  Remaining TTL: #{info[:remaining_ttl]} seconds"
puts "  Expired: #{info[:expired]}"

# Example 10: SimpleCache vs LRUCache
puts "\n--- Example 10: SimpleCache (FIFO) ---"
simple_cache = CacheUtils::SimpleCache.new(max_size: 3)

simple_cache.set(:a, 1)
simple_cache.set(:b, 2)
simple_cache.set(:c, 3)
simple_cache.get(:a) # Access doesn't change order in SimpleCache

simple_cache.set(:d, 4) # Evicts :a (FIFO - first in, first out)
puts "SimpleCache - a should be nil: #{simple_cache.get(:a)}"

# Example 11: Global Cache
puts "\n--- Example 11: Global Cache (Module Methods) ---"
CacheUtils.set(:global_key, "global_value")
puts "Global cache value: #{CacheUtils.get(:global_key)}"

CacheUtils.fetch(:expensive_op) { "computed" }
puts "Fetch result: #{CacheUtils.get(:expensive_op)}"

# Example 12: Factory Methods
puts "\n--- Example 12: Factory Methods ---"
factory_lru = CacheUtils.create_lru_cache(max_size: 50)
factory_simple = CacheUtils.create_simple_cache(max_size: 50)

puts "Created LRU cache with max_size: #{factory_lru.max_size}"
puts "Created Simple cache with max_size: #{factory_simple.max_size}"

puts "\n" + "=" * 60
puts "All examples completed!"
puts "=" * 60
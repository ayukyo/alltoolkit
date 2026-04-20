# frozen_string_literal: true

# cache_utils_test.rb - Test Suite for CacheUtils
#
# Run with: ruby cache_utils_test.rb
#
# Author: AllToolkit
# Date: 2026-04-20

require_relative 'cache_utils'
require 'minitest/autorun'

class LRUCacheTest < Minitest::Test
  def setup
    @cache = CacheUtils::LRUCache.new(max_size: 3)
  end

  def test_basic_set_and_get
    @cache.set(:a, 1)
    assert_equal 1, @cache.get(:a)
  end

  def test_bracket_accessors
    @cache[:a] = 1
    assert_equal 1, @cache[:a]
  end

  def test_missing_key_returns_nil
    assert_nil @cache.get(:nonexistent)
  end

  def test_delete
    @cache.set(:a, 1)
    assert_equal 1, @cache.delete(:a)
    assert_nil @cache.get(:a)
  end

  def test_has_key
    @cache.set(:a, 1)
    assert @cache.has_key?(:a)
    refute @cache.has_key?(:b)
  end

  def test_lru_eviction
    @cache.set(:a, 1)
    @cache.set(:b, 2)
    @cache.set(:c, 3)
    @cache.set(:d, 4) # Should evict :a

    assert_nil @cache.get(:a)
    assert_equal 2, @cache.get(:b)
    assert_equal 3, @cache.get(:c)
    assert_equal 4, @cache.get(:d)
  end

  def test_lru_order_on_access
    @cache.set(:a, 1)
    @cache.set(:b, 2)
    @cache.set(:c, 3)
    
    @cache.get(:a) # Access :a, makes it most recent
    
    @cache.set(:d, 4) # Should evict :b (not :a)

    assert_equal 1, @cache.get(:a)
    assert_nil @cache.get(:b)
    assert_equal 3, @cache.get(:c)
    assert_equal 4, @cache.get(:d)
  end

  def test_update_existing_key
    @cache.set(:a, 1)
    @cache.set(:a, 2)
    
    assert_equal 2, @cache.get(:a)
    assert_equal 1, @cache.size
  end

  def test_size
    @cache.set(:a, 1)
    @cache.set(:b, 2)
    assert_equal 2, @cache.size
  end

  def test_clear
    @cache.set(:a, 1)
    @cache.set(:b, 2)
    @cache.clear
    
    assert_equal 0, @cache.size
    assert_nil @cache.get(:a)
  end

  def test_keys
    @cache.set(:a, 1)
    @cache.set(:b, 2)
    assert_equal [:a, :b].sort, @cache.keys.sort
  end

  def test_values
    @cache.set(:a, 1)
    @cache.set(:b, 2)
    assert_equal [1, 2].sort, @cache.values.sort
  end
end

class TTLTest < Minitest::Test
  def test_expiration
    cache = CacheUtils::LRUCache.new
    cache.set(:a, 1, ttl: 0.1)
    
    assert_equal 1, cache.get(:a)
    sleep(0.15)
    assert_nil cache.get(:a)
  end

  def test_default_ttl
    cache = CacheUtils::LRUCache.new(default_ttl: 0.1)
    cache.set(:a, 1)
    
    assert_equal 1, cache.get(:a)
    sleep(0.15)
    assert_nil cache.get(:a)
  end

  def test_has_key_with_expired
    cache = CacheUtils::LRUCache.new
    cache.set(:a, 1, ttl: 0.1)
    
    assert cache.has_key?(:a)
    sleep(0.15)
    refute cache.has_key?(:a)
  end

  def test_remaining_ttl
    cache = CacheUtils::LRUCache.new
    cache.set(:a, 1, ttl: 10)
    
    info = cache.entry_info(:a)
    assert info[:remaining_ttl] > 9
    assert info[:remaining_ttl] <= 10
  end

  def test_entry_info
    cache = CacheUtils::LRUCache.new
    cache.set(:a, 1, ttl: 10)
    
    info = cache.entry_info(:a)
    assert_equal :a, info[:key]
    assert_equal 1, info[:value]
    assert info[:age] >= 0
    refute info[:expired]
  end
end

class FetchTest < Minitest::Test
  def setup
    @cache = CacheUtils::LRUCache.new
  end

  def test_fetch_with_cached_value
    @cache.set(:a, 1)
    block_called = false
    
    result = @cache.fetch(:a) do
      block_called = true
      2
    end
    
    assert_equal 1, result
    refute block_called
  end

  def test_fetch_with_missing_value
    result = @cache.fetch(:a) { 2 }
    
    assert_equal 2, result
    assert_equal 2, @cache.get(:a)
  end

  def test_fetch_with_ttl
    @cache.fetch(:a, ttl: 0.1) { 1 }
    
    assert_equal 1, @cache.get(:a)
    sleep(0.15)
    assert_nil @cache.get(:a)
  end
end

class StatsTest < Minitest::Test
  def setup
    @cache = CacheUtils::LRUCache.new(max_size: 2)
  end

  def test_hit_miss_stats
    @cache.set(:a, 1)
    
    @cache.get(:a) # hit
    @cache.get(:b) # miss
    @cache.get(:a) # hit
    
    stats = @cache.stats
    assert_equal 2, stats[:hits]
    assert_equal 1, stats[:misses]
  end

  def test_hit_rate
    @cache.set(:a, 1)
    
    @cache.get(:a) # hit
    @cache.get(:b) # miss
    
    assert_in_delta 0.5, @cache.hit_rate, 0.01
  end

  def test_eviction_stats
    @cache.set(:a, 1)
    @cache.set(:b, 2)
    @cache.set(:c, 3)
    @cache.set(:d, 4) # evicts :a
    
    assert_equal 1, @cache.stats[:evictions]
  end
end

class IncrementTest < Minitest::Test
  def setup
    @cache = CacheUtils::LRUCache.new
  end

  def test_increment_new_key
    result = @cache.increment(:counter)
    assert_equal 1, result
    assert_equal 1, @cache.get(:counter)
  end

  def test_increment_existing_key
    @cache.set(:counter, 5)
    result = @cache.increment(:counter, 3)
    assert_equal 8, result
  end

  def test_decrement
    @cache.set(:counter, 10)
    result = @cache.decrement(:counter, 3)
    assert_equal 7, result
  end
end

class MultiTest < Minitest::Test
  def setup
    @cache = CacheUtils::LRUCache.new
  end

  def test_get_multi
    @cache.set(:a, 1)
    @cache.set(:b, 2)
    @cache.set(:c, 3)
    
    result = @cache.get_multi(:a, :c, :d)
    
    assert_equal({ a: 1, c: 3 }, result)
  end

  def test_set_multi
    @cache.set_multi({ a: 1, b: 2, c: 3 })
    
    assert_equal 1, @cache.get(:a)
    assert_equal 2, @cache.get(:b)
    assert_equal 3, @cache.get(:c)
  end
end

class SimpleCacheTest < Minitest::Test
  def setup
    @cache = CacheUtils::SimpleCache.new(max_size: 3)
  end

  def test_basic_operations
    @cache.set(:a, 1)
    assert_equal 1, @cache.get(:a)
    assert @cache.has_key?(:a)
  end

  def test_eviction
    @cache.set(:a, 1)
    @cache.set(:b, 2)
    @cache.set(:c, 3)
    @cache.set(:d, 4) # Evicts :a (FIFO)
    
    assert_nil @cache.get(:a)
    assert_equal 4, @cache.get(:d)
  end

  def test_ttl
    @cache.set(:a, 1, ttl: 0.1)
    
    assert_equal 1, @cache.get(:a)
    sleep(0.15)
    assert_nil @cache.get(:a)
  end

  def test_fetch
    result = @cache.fetch(:a) { 1 }
    assert_equal 1, result
    assert_equal 1, @cache.get(:a)
  end

  def test_stats
    @cache.set(:a, 1)
    @cache.get(:a)  # hit
    @cache.get(:b)  # miss
    
    assert_equal 1, @cache.stats[:hits]
    assert_equal 1, @cache.stats[:misses]
  end

  def test_hit_rate
    @cache.set(:a, 1)
    @cache.get(:a)
    @cache.get(:b)
    
    assert_in_delta 0.5, @cache.hit_rate, 0.01
  end
end

class ConvenienceMethodsTest < Minitest::Test
  def setup
    CacheUtils.reset_default_cache!
  end

  def test_module_level_get_set
    CacheUtils.set(:a, 1)
    assert_equal 1, CacheUtils.get(:a)
  end

  def test_module_level_fetch
    result = CacheUtils.fetch(:b) { 2 }
    assert_equal 2, result
    assert_equal 2, CacheUtils.get(:b)
  end

  def test_module_level_delete
    CacheUtils.set(:c, 3)
    CacheUtils.delete(:c)
    assert_nil CacheUtils.get(:c)
  end

  def test_module_level_clear
    CacheUtils.set(:a, 1)
    CacheUtils.set(:b, 2)
    CacheUtils.clear
    assert_nil CacheUtils.get(:a)
  end
end

class FactoryTest < Minitest::Test
  def test_create_lru_cache
    cache = CacheUtils.create_lru_cache(max_size: 100, default_ttl: 60)
    assert_instance_of CacheUtils::LRUCache, cache
    assert_equal 100, cache.max_size
  end

  def test_create_simple_cache
    cache = CacheUtils.create_simple_cache(max_size: 50)
    assert_instance_of CacheUtils::SimpleCache, cache
    assert_equal 50, cache.max_size
  end
end

class ThreadSafetyTest < Minitest::Test
  def test_concurrent_access
    cache = CacheUtils::LRUCache.new(max_size: 1000)
    threads = []
    errors = []

    10.times do |i|
      threads << Thread.new do
        begin
          100.times do |j|
            key = "key_#{i}_#{j}"
            cache.set(key, j)
            cache.get(key)
            cache.has_key?(key)
          end
        rescue => e
          errors << e
        end
      end
    end

    threads.each(&:join)
    assert_empty errors
  end
end

class TouchTest < Minitest::Test
  def test_touch_updates_ttl
    cache = CacheUtils::LRUCache.new
    cache.set(:a, 1, ttl: 0.1)
    
    sleep(0.05)
    result = cache.touch(:a, ttl: 10)
    assert result
    
    sleep(0.1) # Original TTL would have expired
    assert_equal 1, cache.get(:a) # Still there because TTL was extended
  end
end

# Run tests
puts "Running CacheUtils Tests..."
puts "=" * 50
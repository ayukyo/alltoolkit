# frozen_string_literal: true

# cache_utils.rb - Memory Cache with LRU Eviction Policy
# 
# A lightweight, zero-dependency memory cache implementation for Ruby
# with TTL support, LRU eviction, and thread safety.
#
# Features:
# - LRU (Least Recently Used) eviction policy
# - TTL (Time To Live) support for cache entries
# - Maximum capacity limits
# - Thread-safe operations
# - Statistics tracking (hits, misses, evictions)
# - Zero external dependencies
#
# Author: AllToolkit
# Date: 2026-04-20

require 'thread'

module CacheUtils
  # Cache entry representing a single cached item
  class Entry
    attr_accessor :key, :value, :created_at, :expires_at, :prev, :next

    def initialize(key:, value:, ttl: nil)
      @key = key
      @value = value
      @created_at = Time.now
      @expires_at = ttl ? @created_at + ttl : nil
      @prev = nil
      @next = nil
    end

    def expired?
      @expires_at && Time.now > @expires_at
    end

    def remaining_ttl
      return nil unless @expires_at
      [@expires_at - Time.now, 0].max
    end

    def age
      Time.now - @created_at
    end
  end

  # LRU Cache implementation with TTL support
  class LRUCache
    attr_reader :max_size, :stats

    def initialize(max_size: 1000, default_ttl: nil)
      @max_size = max_size
      @default_ttl = default_ttl
      @cache = {} # key => Entry
      @head = nil # Most recently used
      @tail = nil # Least recently used
      @mutex = Mutex.new
      reset_stats
    end

    # Get a value from the cache
    def get(key)
      @mutex.synchronize do
        entry = @cache[key]
        
        if entry.nil?
          increment_misses
          return nil
        end

        if entry.expired?
          remove_entry(entry)
          @cache.delete(key)
          increment_misses
          increment_evictions
          return nil
        end

        # Move to front (most recently used)
        move_to_front(entry)
        increment_hits
        entry.value
      end
    end

    # Alias for get
    def [](key)
      get(key)
    end

    # Set a value in the cache
    def set(key, value, ttl: nil)
      @mutex.synchronize do
        ttl ||= @default_ttl

        # If key exists, update and move to front
        if @cache.key?(key)
          entry = @cache[key]
          entry.value = value
          entry.created_at = Time.now
          entry.expires_at = ttl ? entry.created_at + ttl : nil
          move_to_front(entry)
          return value
        end

        # Evict if at capacity
        evict_lru while @cache.size >= @max_size

        # Create new entry
        entry = Entry.new(key: key, value: value, ttl: ttl)
        @cache[key] = entry
        add_to_front(entry)
        value
      end
    end

    # Alias for set
    def []=(key, value)
      set(key, value)
    end

    # Check if key exists and is not expired
    def has_key?(key)
      @mutex.synchronize do
        entry = @cache[key]
        return false if entry.nil?
        
        if entry.expired?
          remove_entry(entry)
          @cache.delete(key)
          return false
        end
        
        true
      end
    end

    # Alias for has_key?
    def key?(key)
      has_key?(key)
    end

    # Delete a key from the cache
    def delete(key)
      @mutex.synchronize do
        entry = @cache[key]
        return nil if entry.nil?
        
        remove_entry(entry)
        @cache.delete(key)
        entry.value
      end
    end

    # Get or compute - fetch from cache or execute block
    def fetch(key, ttl: nil)
      value = get(key)
      return value unless value.nil?

      if block_given?
        value = yield
        set(key, value, ttl: ttl)
        value
      else
        nil
      end
    end

    # Clear all cache entries
    def clear
      @mutex.synchronize do
        @cache.clear
        @head = nil
        @tail = nil
        reset_stats
        true
      end
    end

    # Get current cache size
    def size
      @mutex.synchronize do
        cleanup_expired
        @cache.size
      end
    end

    # Get all keys
    def keys
      @mutex.synchronize do
        cleanup_expired
        @cache.keys
      end
    end

    # Get all values
    def values
      @mutex.synchronize do
        cleanup_expired
        @cache.values.map(&:value)
      end
    end

    # Get cache statistics
    def stats
      @mutex.synchronize do
        @stats.dup
      end
    end

    # Get hit rate (0.0 to 1.0)
    def hit_rate
      @mutex.synchronize do
        total = @stats[:hits] + @stats[:misses]
        return 0.0 if total.zero?
        @stats[:hits].to_f / total
      end
    end

    # Cleanup expired entries
    def cleanup
      @mutex.synchronize do
        cleanup_expired
      end
    end

    # Get entry info (without affecting LRU order)
    def entry_info(key)
      @mutex.synchronize do
        entry = @cache[key]
        return nil if entry.nil?

        {
          key: key,
          value: entry.value,
          age: entry.age.round(2),
          remaining_ttl: entry.remaining_ttl&.round(2),
          expired: entry.expired?
        }
      end
    end

    # Update TTL for an existing key
    def touch(key, ttl: nil)
      @mutex.synchronize do
        entry = @cache[key]
        return false if entry.nil?

        entry.expires_at = ttl ? Time.now + ttl : nil
        move_to_front(entry)
        true
      end
    end

    # Increment a numeric value (atomic)
    def increment(key, delta = 1, ttl: nil)
      @mutex.synchronize do
        entry = @cache[key]
        
        if entry.nil?
          set_internal(key, delta, ttl: ttl)
          return delta
        end

        entry.value = entry.value.to_i + delta
        move_to_front(entry)
        entry.value
      end
    end

    # Decrement a numeric value (atomic)
    def decrement(key, delta = 1, ttl: nil)
      increment(key, -delta, ttl: ttl)
    end

    # Get multiple values at once
    def get_multi(*keys)
      @mutex.synchronize do
        result = {}
        keys.each do |key|
          entry = @cache[key]
          if entry && !entry.expired?
            move_to_front(entry)
            result[key] = entry.value
            increment_hits
          else
            increment_misses
          end
        end
        result
      end
    end

    # Set multiple values at once
    def set_multi(hash, ttl: nil)
      @mutex.synchronize do
        hash.each do |key, value|
          set_internal(key, value, ttl: ttl)
        end
        true
      end
    end

    private

    def set_internal(key, value, ttl: nil)
      ttl ||= @default_ttl

      if @cache.key?(key)
        entry = @cache[key]
        entry.value = value
        entry.created_at = Time.now
        entry.expires_at = ttl ? entry.created_at + ttl : nil
        move_to_front(entry)
        return value
      end

      evict_lru while @cache.size >= @max_size

      entry = Entry.new(key: key, value: value, ttl: ttl)
      @cache[key] = entry
      add_to_front(entry)
      value
    end

    def move_to_front(entry)
      return if entry == @head
      
      remove_entry(entry)
      add_to_front(entry)
    end

    def add_to_front(entry)
      entry.prev = nil
      entry.next = @head

      @head.prev = entry if @head
      @head = entry
      @tail ||= entry
    end

    def remove_entry(entry)
      if entry.prev
        entry.prev.next = entry.next
      else
        @head = entry.next
      end

      if entry.next
        entry.next.prev = entry.prev
      else
        @tail = entry.prev
      end
    end

    def evict_lru
      return unless @tail

      entry = @tail
      remove_entry(entry)
      @cache.delete(entry.key)
      increment_evictions
    end

    def cleanup_expired
      keys_to_delete = []
      @cache.each do |key, entry|
        keys_to_delete << key if entry.expired?
      end

      keys_to_delete.each do |key|
        entry = @cache.delete(key)
        remove_entry(entry) if entry
      end

      keys_to_delete.size
    end

    def reset_stats
      @stats = {
        hits: 0,
        misses: 0,
        evictions: 0
      }
    end

    def increment_hits
      @stats[:hits] += 1
    end

    def increment_misses
      @stats[:misses] += 1
    end

    def increment_evictions
      @stats[:evictions] += 1
    end
  end

  # Simple cache without LRU (faster for small caches)
  class SimpleCache
    attr_reader :max_size, :stats

    def initialize(max_size: 1000, default_ttl: nil)
      @max_size = max_size
      @default_ttl = default_ttl
      @cache = {}
      @mutex = Mutex.new
      reset_stats
    end

    def get(key)
      @mutex.synchronize do
        entry = @cache[key]
        
        if entry.nil?
          increment_misses
          return nil
        end

        if entry[:expires_at] && Time.now > entry[:expires_at]
          @cache.delete(key)
          increment_misses
          increment_evictions
          return nil
        end

        increment_hits
        entry[:value]
      end
    end

    def [](key)
      get(key)
    end

    def set(key, value, ttl: nil)
      @mutex.synchronize do
        ttl ||= @default_ttl

        # Simple FIFO eviction when at capacity
        if @cache.size >= @max_size && !@cache.key?(key)
          @cache.shift # Remove first (oldest) entry
          increment_evictions
        end

        @cache[key] = {
          value: value,
          created_at: Time.now,
          expires_at: ttl ? Time.now + ttl : nil
        }
        value
      end
    end

    def []=(key, value)
      set(key, value)
    end

    def has_key?(key)
      @mutex.synchronize do
        entry = @cache[key]
        return false if entry.nil?
        
        if entry[:expires_at] && Time.now > entry[:expires_at]
          @cache.delete(key)
          return false
        end
        
        true
      end
    end

    def delete(key)
      @mutex.synchronize do
        entry = @cache.delete(key)
        entry&.dig(:value)
      end
    end

    def fetch(key, ttl: nil)
      value = get(key)
      return value unless value.nil?

      if block_given?
        value = yield
        set(key, value, ttl: ttl)
        value
      else
        nil
      end
    end

    def clear
      @mutex.synchronize do
        @cache.clear
        reset_stats
        true
      end
    end

    def size
      @mutex.synchronize { @cache.size }
    end

    def keys
      @mutex.synchronize { @cache.keys }
    end

    def values
      @mutex.synchronize { @cache.values.map { |e| e[:value] } }
    end

    def stats
      @mutex.synchronize { @stats.dup }
    end

    def hit_rate
      total = @stats[:hits] + @stats[:misses]
      return 0.0 if total.zero?
      @stats[:hits].to_f / total
    end

    private

    def reset_stats
      @stats = { hits: 0, misses: 0, evictions: 0 }
    end

    def increment_hits
      @stats[:hits] += 1
    end

    def increment_misses
      @stats[:misses] += 1
    end

    def increment_evictions
      @stats[:evictions] += 1
    end
  end

  # Factory method for creating caches
  def self.create_lru_cache(max_size: 1000, default_ttl: nil)
    LRUCache.new(max_size: max_size, default_ttl: default_ttl)
  end

  def self.create_simple_cache(max_size: 1000, default_ttl: nil)
    SimpleCache.new(max_size: max_size, default_ttl: default_ttl)
  end

  # Global default cache instance
  @default_cache = nil

  def self.default_cache
    @default_cache ||= LRUCache.new
  end

  def self.reset_default_cache!
    @default_cache = nil
  end

  # Convenience methods using default cache
  def self.get(key)
    default_cache.get(key)
  end

  def self.set(key, value, ttl: nil)
    default_cache.set(key, value, ttl: ttl)
  end

  def self.fetch(key, ttl: nil)
    default_cache.fetch(key, ttl: ttl) { yield if block_given? }
  end

  def self.delete(key)
    default_cache.delete(key)
  end

  def self.clear
    default_cache.clear
  end
end
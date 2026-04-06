# cache_utils_test.R
# Test suite for R cache_utils module
# Run with: Rscript cache_utils_test.R

source("mod.R")

# Test counter
tests_passed <- 0
tests_failed <- 0

#' Run a test
test <- function(name, expr) {
  tryCatch({
    expr
    cat("[PASS]", name, "\n")
    tests_passed <<- tests_passed + 1
  }, error = function(e) {
    cat("[FAIL]", name, "-", conditionMessage(e), "\n")
    tests_failed <<- tests_failed + 1
  })
}

#' Assert equal
assert_equal <- function(actual, expected) {
  if (!identical(actual, expected)) {
    stop(paste("Expected:", deparse(expected), "Got:", deparse(actual)))
  }
}

#' Assert true
assert_true <- function(x) {
  if (!isTRUE(x)) {
    stop(paste("Expected TRUE, got:", deparse(x)))
  }
}

#' Assert false
assert_false <- function(x) {
  if (!identical(x, FALSE)) {
    stop(paste("Expected FALSE, got:", deparse(x)))
  }
}

#' Assert null
assert_null <- function(x) {
  if (!is.null(x)) {
    stop(paste("Expected NULL, got:", deparse(x)))
  }
}

#' Assert not null
assert_not_null <- function(x) {
  if (is.null(x)) {
    stop("Expected non-NULL value")
  }
}

cat("Running Cache Utils Tests\n")
cat("=========================\n\n")

# Test 1: Basic cache creation
test("Cache creation", {
  cache <- cache_create()
  assert_not_null(cache)
  assert_true("set" %in% names(cache))
  assert_true("get" %in% names(cache))
})

# Test 2: Set and get
test("Set and get", {
  cache <- cache_create()
  cache$set("key1", "value1")
  assert_equal(cache$get("key1"), "value1")
})

# Test 3: Get with default
test("Get with default", {
  cache <- cache_create()
  assert_equal(cache$get("nonexistent", "default"), "default")
  assert_null(cache$get("nonexistent"))
})

# Test 4: Has key
test("Has key", {
  cache <- cache_create()
  cache$set("key1", "value1")
  assert_true(cache$has("key1"))
  assert_false(cache$has("nonexistent"))
})

# Test 5: Delete key
test("Delete key", {
  cache <- cache_create()
  cache$set("key1", "value1")
  assert_true(cache$delete("key1"))
  assert_false(cache$has("key1"))
  assert_false(cache$delete("nonexistent"))
})

# Test 6: Clear cache
test("Clear cache", {
  cache <- cache_create()
  cache$set("key1", "value1")
  cache$set("key2", "value2")
  cache$clear()
  assert_false(cache$has("key1"))
  assert_false(cache$has("key2"))
  assert_equal(cache$size(), 0)
})

# Test 7: Cache size
test("Cache size", {
  cache <- cache_create()
  assert_equal(cache$size(), 0)
  cache$set("key1", "value1")
  assert_equal(cache$size(), 1)
  cache$set("key2", "value2")
  assert_equal(cache$size(), 2)
})

# Test 8: Keys list
test("Keys list", {
  cache <- cache_create()
  cache$set("key1", "value1")
  cache$set("key2", "value2")
  keys <- cache$keys()
  assert_true("key1" %in% keys)
  assert_true("key2" %in% keys)
})

# Test 9: TTL expiration
test("TTL expiration", {
  cache <- cache_create()
  cache$set("key1", "value1", ttl = 0.1)  # 100ms TTL
  assert_true(cache$has("key1"))
  Sys.sleep(0.2)  # Wait for expiration
  assert_false(cache$has("key1"))
  assert_null(cache$get("key1"))
})

# Test 10: TTL remaining
test("TTL remaining", {
  cache <- cache_create()
  cache$set("key1", "value1", ttl = 60)
  remaining <- cache$ttl("key1")
  assert_true(remaining > 50 && remaining <= 60)
  
  cache$set("key2", "value2")  # No TTL
  assert_null(cache$ttl("key2"))
  
  assert_equal(cache$ttl("nonexistent"), -1)
})

# Test 11: Statistics
test("Statistics", {
  cache <- cache_create()
  cache$set("key1", "value1")
  cache$get("key1")  # hit
  cache$get("key1")  # hit
  cache$get("nonexistent")  # miss
  
  stats <- cache$get_stats()
  assert_equal(stats$hits, 2)
  assert_equal(stats$misses, 1)
  assert_equal(stats$sets, 1)
  assert_true(stats$hit_rate > 0.6)
})

# Test 12: Reset statistics
test("Reset statistics", {
  cache <- cache_create()
  cache$set("key1", "value1")
  cache$get("key1")
  cache$reset_stats()
  
  stats <- cache$get_stats()
  assert_equal(stats$hits, 0)
  assert_equal(stats$misses, 0)
})

# Test 13: LRU eviction
test("LRU eviction", {
  cache <- cache_create(max_size = 3)
  cache$set("key1", "value1")
  cache$set("key2", "value2")
  cache$set("key3", "value3")
  cache$set("key4", "value4")  # Should evict key1
  
  assert_false(cache$has("key1"))
  assert_true(cache$has("key2"))
  assert_true(cache$has("key3"))
  assert_true(cache$has("key4"))
  
  stats <- cache$get_stats()
  assert_true(stats$evictions >= 1)
})

# Test 14: Get or set (memoization)
test("Get or set", {
  cache <- cache_create()
  counter <- 0
  factory <- function() {
    counter <<- counter + 1
    paste("computed", counter)
  }
  
  result1 <- cache$get_or_set("key1", factory)
  result2 <- cache$get_or_set("key1", factory)
  
  assert_equal(result1, "computed 1")
  assert_equal(result2, "computed 1")  # Should return cached value
  assert_equal(counter, 1)  # Factory only called once
})

# Test 15: Multiple operations
test("Multiple operations", {
  cache <- cache_create()
  
  # Set multiple
  cache$set_multiple(list(a = 1, b = 2, c = 3))
  assert_equal(cache$get("a"), 1)
  assert_equal(cache$get("b"), 2)
  assert_equal(cache$get("c"), 3)
  
  # Get multiple
  results <- cache$get_multiple(c("a", "b", "nonexistent"))
  assert_equal(results$a, 1)
  assert_equal(results$b, 2)
  assert_null(results$nonexistent)
  
  # Delete multiple
  deleted <- cache$delete_multiple(c("a", "b", "nonexistent"))
  assert_equal(deleted, 2)
  assert_false(cache$has("a"))
  assert_false(cache$has("b"))
  assert_true(cache$has("c"))
})

# Test 16: Increment/Decrement
test("Increment and decrement", {
  cache <- cache_create()
  
  assert_equal(cache$increment("counter"), 1)
  assert_equal(cache$increment("counter", 5), 6)
  assert_equal(cache$decrement("counter", 2), 4)
  assert_equal(cache$get("counter"), 4)
})

# Test 17: Different data types
test("Different data types", {
  cache <- cache_create()
  
  # String
  cache$set("str", "hello")
  assert_equal(cache$get("str"), "hello")
  
  # Number
  cache$set("num", 42)
  assert_equal(cache$get("num"), 42)
  
  # Vector
  cache$set("vec", c(1, 2, 3))
  assert_equal(cache$get("vec"), c(1, 2, 3))
  
  # List
  cache$set("list", list(a = 1, b = 2))
  result <- cache$get("list")
  assert_equal(result$a, 1)
  assert_equal(result$b, 2)
  
  # Data frame
  df <- data.frame(x = 1:3, y = letters[1:3])
  cache$set("df", df)
  assert_equal(cache$get("df")$x, c(1, 2, 3))
})

# Test 18: Cache configuration
test("Cache configuration", {
  cache <- cache_create(max_size = 500, default_ttl = 3600)
  config <- cache$get_config()
  assert_equal(config$max_size, 500)
  assert_equal(config$default_ttl, 3600)
})

# Test 19: Default TTL
test("Default TTL", {
  cache <- cache_create(default_ttl = 0.1)
  cache$set("key1", "value1")  # Uses default TTL
  assert_true(cache$has("key1"))
  Sys.sleep(0.2)
  assert_false(cache$has("key1"))
})

# Test 20: Update existing key
test("Update existing key", {
  cache <- cache_create()
  cache$set("key1", "old_value")
  cache$set("key1", "new_value")
  assert_equal(cache$get("key1"), "new_value")
})

cat("\n=========================\n")
cat("Tests passed:", tests_passed, "\n")
cat("Tests failed:", tests_failed, "\n")

if (tests_failed > 0) {
  quit(status = 1)
} else {
  cat("\nAll tests passed!\n")
}

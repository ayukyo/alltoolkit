# cache_utils_example.R
# Example usage of R cache_utils module
# Run with: Rscript cache_utils_example.R

source("../cache_utils/mod.R")

cat("R Cache Utilities Examples")
cat("==========================\n\n")

# Example 1: Basic cache operations
cat("1. Basic Cache Operations\n")
cat("---------------------------\n")
cache <- cache_create(max_size = 100)

# Set values
cache$set("user:123", list(name = "Alice", age = 30))
cache$set("user:456", list(name = "Bob", age = 25))

# Get values
user1 <- cache$get("user:123")
cat("User 123:", user1$name, ",", user1$age, "years old\n")

user2 <- cache$get("user:456")
cat("User 456:", user2$name, ",", user2$age, "years old\n")

# Check existence
cat("Has user:123?", cache$has("user:123"), "\n")
cat("Has user:999?", cache$has("user:999"), "\n")

# Get with default
result <- cache$get("user:999", default = list(name = "Unknown"))
cat("User 999 (with default):", result$name, "\n")
cat("\n")

# Example 2: TTL (Time To Live)
cat("2. TTL (Time To Live)\n")
cat("---------------------\n")
cache2 <- cache_create()

# Set with TTL of 2 seconds
cache2$set("session_token", "abc123xyz", ttl = 2)
cat("Session token set with 2 second TTL\n")
cat("Has session_token?", cache2$has("session_token"), "\n")
cat("TTL remaining:", cache2$ttl("session_token"), "seconds\n")

cat("Waiting 3 seconds...\n")
Sys.sleep(3)

cat("Has session_token after expiration?", cache2$has("session_token"), "\n")
cat("\n")

# Example 3: Cache Statistics
cat("3. Cache Statistics\n")
cat("-------------------\n")
cache3 <- cache_create()

# Generate some cache activity
for (i in 1:10) {
  cache3$set(paste0("key", i), paste0("value", i))
}

# Access some keys (hits)
for (i in 1:5) {
  cache3$get(paste0("key", i))
}

# Try to access non-existent keys (misses)
for (i in 11:15) {
  cache3$get(paste0("key", i))
}

stats <- cache3$get_stats()
cat("Cache Statistics:\n")
cat("  Hits:", stats$hits, "\n")
cat("  Misses:", stats$misses, "\n")
cat("  Hit Rate:", round(stats$hit_rate * 100, 2), "%\n")
cat("  Sets:", stats$sets, "\n")
cat("  Current Size:", stats$current_size, "/", stats$max_size, "\n")
cat("\n")

# Example 4: LRU Eviction
cat("4. LRU (Least Recently Used) Eviction\n")
cat("--------------------------------------\n")
cache4 <- cache_create(max_size = 3)

cache4$set("a", "1")
cache4$set("b", "2")
cache4$set("c", "3")
cat("Cache size after 3 inserts:", cache4$size(), "\n")

# Access 'a' to make it recently used
cache4$get("a")

# Add 'd', should evict 'b' (least recently used)
cache4$set("d", "4")
cat("Cache size after adding 'd':", cache4$size(), "\n")
cat("Has 'a'?", cache4$has("a"), "(accessed recently)\n")
cat("Has 'b'?", cache4$has("b"), "(evicted - LRU)\n")
cat("Has 'c'?", cache4$has("c"), "\n")
cat("Has 'd'?", cache4$has("d"), "\n")

stats <- cache4$get_stats()
cat("Evictions:", stats$evictions, "\n")
cat("\n")

# Example 5: Get or Set (Memoization Pattern)
cat("5. Get or Set (Memoization)\n")
cat("----------------------------\n")
cache5 <- cache_create()

# Simulate expensive computation
expensive_function <- function(x) {
  cat("  Computing for", x, "...\n")
  Sys.sleep(0.1)  # Simulate work
  return(x * x)
}

cat("First call (will compute):\n")
result1 <- cache5$get_or_set("square:5", function() expensive_function(5))
cat("Result:", result1, "\n")

cat("Second call (cached, no computation):\n")
result2 <- cache5$get_or_set("square:5", function() expensive_function(5))
cat("Result:", result2, "\n")

cat("Different key (will compute):\n")
result3 <- cache5$get_or_set("square:10", function() expensive_function(10))
cat("Result:", result3, "\n")
cat("\n")

# Example 6: Multiple Operations
cat("6. Multiple Operations\n")
cat("----------------------\n")
cache6 <- cache_create()

# Set multiple values at once
cache6$set_multiple(list(
  product_1 = list(name = "Laptop", price = 999),
  product_2 = list(name = "Mouse", price = 29),
  product_3 = list(name = "Keyboard", price = 79)
))

# Get multiple values at once
results <- cache6$get_multiple(c("product_1", "product_2", "product_99"))
cat("Product 1:", results$product_1$name, "- $", results$product_1$price, "\n")
cat("Product 2:", results$product_2$name, "- $", results$product_2$price, "\n")
cat("Product 99 (not found):", is.null(results$product_99), "\n")

# Delete multiple
deleted <- cache6$delete_multiple(c("product_1", "product_2", "product_99"))
cat("Deleted", deleted, "items\n")
cat("Remaining keys:", paste(cache6$keys(), collapse = ", "), "\n")
cat("\n")

# Example 7: Increment/Decrement
cat("7. Increment/Decrement\n")
cat("----------------------\n")
cache7 <- cache_create()

# Counter operations
cache7$increment("views", 1)
cache7$increment("views", 1)
cache7$increment("views", 1)
cat("Views after 3 increments:", cache7$get("views"), "\n")

cache7$decrement("views", 1)
cat("Views after 1 decrement:", cache7$get("views"), "\n")

# Custom increment amount
cache7$increment("score", 100)
cache7$increment("score", 50)
cat("Score after increments:", cache7$get("score"), "\n")
cat("\n")

# Example 8: Different Data Types
cat("8. Different Data Types\n")
cat("-----------------------\n")
cache8 <- cache_create()

# Store various R data types
cache8$set("string", "Hello, World!")
cache8$set("number", 3.14159)
cache8$set("integer", 42L)
cache8$set("logical", TRUE)
cache8$set("vector", c(1, 2, 3, 4, 5))
cache8$set("matrix", matrix(1:9, nrow = 3))
cache8$set("data_frame", data.frame(
  name = c("Alice", "Bob"),
  age = c(30, 25),
  active = c(TRUE, FALSE)
))
cache8$set("list", list(
  nested = list(
    deeply = list(
      value = "found me!"
    )
  )
))

# Retrieve and display
cat("String:", cache8$get("string"), "\n")
cat("Number:", cache8$get("number"), "\n")
cat("Integer:", cache8$get("integer"), "\n")
cat("Logical:", cache8$get("logical"), "\n")
cat("Vector:", paste(cache8$get("vector"), collapse = ", "), "\n")
cat("Matrix:\n")
print(cache8$get("matrix"))
cat("Data Frame:\n")
print(cache8$get("data_frame"))
nested <- cache8$get("list")
cat("Nested list value:", nested$nested$deeply$value, "\n")
cat("\n")

# Example 9: Cache with Default TTL
cat("9. Cache with Default TTL\n")
cat("--------------------------\n")
cache9 <- cache_create(max_size = 100, default_ttl = 1)  # 1 second default TTL

cache9$set("temp1", "value1")  # Uses default TTL
cache9$set("temp2", "value2", ttl = 5)  # Override with 5 seconds
cache9$set("permanent", "value3", ttl = NULL)  # No expiration

cat("Initial state:\n")
cat("  Has temp1?", cache9$has("temp1"), "\n")
cat("  Has temp2?", cache9$has("temp2"), "\n")
cat("  Has permanent?", cache9$has("permanent"), "\n")

cat("Waiting 1.5 seconds...\n")
Sys.sleep(1.5)

cat("After 1.5 seconds:\n")
cat("  Has temp1 (expired)?", cache9$has("temp1"), "\n")
cat("  Has temp2 (still valid)?", cache9$has("temp2"), "\n")
cat("  Has permanent (never expires)?", cache9$has("permanent"), "\n")
cat("\n")

# Example 10: Practical Use Case - API Response Caching
cat("10. Practical Use Case: API Response Caching\n")
cat("---------------------------------------------\n")

# Simulate an API client with caching
api_cache <- cache_create(max_size = 50, default_ttl = 300)  # 5 minute cache

fetch_user_data <- function(user_id) {
  # Check cache first
  cache_key <- paste0("user:", user_id)
  cached <- api_cache$get(cache_key)
  
  if (!is.null(cached)) {
    cat("  [CACHE HIT] Returning cached data for user", user_id, "\n")
    return(cached)
  }
  
  # Simulate API call
  cat("  [API CALL] Fetching user", user_id, "from API...\n")
  Sys.sleep(0.2)  # Simulate network delay
  
  # Return mock data
  user_data <- list(
    id = user_id,
    name = paste("User", user_id),
    email = paste0("user", user_id, "@example.com"),
    created_at = Sys.time()
  )
  
  # Cache the result
  api_cache$set(cache_key, user_data)
  cat("  [CACHE SET] Stored user", user_id, "in cache\n")
  
  return(user_data)
}

cat("Fetching user 101:\n")
user1 <- fetch_user_data(101)
cat("  Name:", user1$name, "\n\n")

cat("Fetching user 101 again (should be cached):\n")
user1_cached <- fetch_user_data(101)
cat("  Name:", user1_cached$name, "\n\n")

cat("Fetching user 102:\n")
user2 <- fetch_user_data(102)
cat("  Name:", user2$name, "\n\n")

# Show cache stats
stats <- api_cache$get_stats()
cat("API Cache Statistics:\n")
cat("  Hits:", stats$hits, "\n")
cat("  Misses:", stats$misses, "\n")
cat("  Hit Rate:", round(stats$hit_rate * 100, 2), "%\n")
cat("\n")

# Print the cache object (uses custom print method)
cat("Cache object summary:\n")
print(api_cache)

cat("\n==========================\n")
cat("Examples completed!\n")

# cache_utils/mod.R
# A comprehensive caching utility module for R with zero dependencies.
# Provides in-memory key-value storage with TTL (Time To Live) support,
# LRU (Least Recently Used) eviction policy, and cache statistics.
#
# Features:
# - Zero dependencies, uses only R standard library
# - TTL support for automatic expiration
# - LRU eviction policy when cache reaches capacity
# - Cache statistics (hits, misses, hit rate)
# - Multiple data types support
#
# Author: AllToolkit
# Version: 1.0.0

#' Create a new cache instance
#'
#' @param max_size Maximum number of items in cache (default: 1000)
#' @param default_ttl Default TTL in seconds (NULL means no expiration)
#' @return A cache object (list with methods)
#' @export
cache_create <- function(max_size = 1000, default_ttl = NULL) {
  if (!is.numeric(max_size) || max_size < 1) {
    stop("max_size must be a positive number")
  }
  
  # Private data storage
  data <- new.env(parent = emptyenv())
  access_order <- character(0)
  
  # Statistics
  stats <- list(
    hits = 0,
    misses = 0,
    evictions = 0,
    expirations = 0,
    sets = 0,
    deletes = 0
  )
  
  # Cache configuration
  config <- list(
    max_size = as.integer(max_size),
    default_ttl = default_ttl
  )
  
  # Check if a key is expired
  is_expired <- function(key) {
    if (!exists(key, envir = data)) {
      return(TRUE)
    }
    entry <- get(key, envir = data)
    if (is.null(entry$expires_at)) {
      return(FALSE)
    }
    return(Sys.time() > entry$expires_at)
  }
  
  # Remove expired entries
  purge_expired <- function() {
    keys <- ls(envir = data)
    expired_count <- 0
    for (k in keys) {
      if (is_expired(k)) {
        rm(list = k, envir = data)
        access_order <<- access_order[access_order != k]
        expired_count <- expired_count + 1
      }
    }
    stats$expirations <<- stats$expirations + expired_count
    return(expired_count)
  }
  
  # Evict least recently used item
  evict_lru <- function() {
    if (length(access_order) == 0) {
      return(FALSE)
    }
    lru_key <- access_order[1]
    rm(list = lru_key, envir = data)
    access_order <<- access_order[-1]
    stats$evictions <<- stats$evictions + 1
    return(TRUE)
  }
  
  # Update access order for LRU
  touch <- function(key) {
    access_order <<- c(access_order[access_order != key], key)
  }
  
  # Return cache object with methods
  structure(list(
    # Set a value in the cache
    set = function(key, value, ttl = NULL) {
      if (!is.character(key) || length(key) != 1) {
        stop("key must be a single character string")
      }
      
      if (is.null(ttl)) {
        ttl <- config$default_ttl
      }
      
      expires_at <- if (is.null(ttl)) NULL else Sys.time() + ttl
      
      if (stats$sets %% 100 == 0) {
        purge_expired()
      }
      
      if (length(ls(envir = data)) >= config$max_size && !exists(key, envir = data)) {
        evict_lru()
      }
      
      entry <- list(
        value = value,
        created_at = Sys.time(),
        expires_at = expires_at,
        access_count = 1
      )
      assign(key, entry, envir = data)
      touch(key)
      stats$sets <<- stats$sets + 1
      invisible(NULL)
    },
    
    # Get a value from the cache
    get = function(key, default = NULL) {
      if (!is.character(key) || length(key) != 1) {
        stop("key must be a single character string")
      }
      
      if (!exists(key, envir = data) || is_expired(key)) {
        if (exists(key, envir = data) && is_expired(key)) {
          rm(list = key, envir = data)
          access_order <<- access_order[access_order != key]
          stats$expirations <<- stats$expirations + 1
        }
        stats$misses <<- stats$misses + 1
        return(default)
      }
      
      entry <- get(key, envir = data)
      entry$access_count <- entry$access_count + 1
      assign(key, entry, envir = data)
      touch(key)
      stats$hits <<- stats$hits + 1
      return(entry$value)
    },
    
    # Check if a key exists and is not expired
    has = function(key) {
      if (!is.character(key) || length(key) != 1) {
        stop("key must be a single character string")
      }
      return(exists(key, envir = data) && !is_expired(key))
    },
    
    # Delete a key from the cache
    delete = function(key) {
      if (!is.character(key) || length(key) != 1) {
        stop("key must be a single character string")
      }
      
      if (exists(key, envir = data)) {
        rm(list = key, envir = data)
        access_order <<- access_order[access_order != key]
        stats$deletes <<- stats$deletes + 1
        return(TRUE)
      }
      return(FALSE)
    },
    
    # Get all keys in the cache (excluding expired)
    keys = function() {
      all_keys <- ls(envir = data)
      valid_keys <- all_keys[!vapply(all_keys, is_expired, logical(1))]
      return(valid_keys)
    },
    
    # Get the number of items in cache
    size = function() {
      purge_expired()
      return(length(ls(envir = data)))
    },
    
    # Clear all items from cache
    clear = function() {
      all_keys <- ls(envir = data)
      for (k in all_keys) {
        rm(list = k, envir = data)
      }
      access_order <<- character(0)
      invisible(NULL)
    },
    
    # Get cache statistics
    get_stats = function() {
      total_requests <- stats$hits + stats$misses
      hit_rate <- if (total_requests > 0) stats$hits / total_requests else 0
      
      list(
        hits = stats$hits,
        misses = stats$misses,
        hit_rate = hit_rate,
        evictions = stats$evictions,
        expirations = stats$expirations,
        sets = stats$sets,
        deletes = stats$deletes,
        current_size = length(ls(envir = data)),
        max_size = config$max_size
      )
    },
    
    # Reset statistics
    reset_stats = function() {
      stats <<- list(
        hits = 0,
        misses = 0,
        evictions = 0,
        expirations = 0,
        sets = 0,
        deletes = 0
      )
      invisible(NULL)
    },
    
    # Get TTL remaining for a key
    ttl = function(key) {
      if (!is.character(key) || length(key) != 1) {
        stop("key must be a single character string")
      }
      
      if (!exists(key, envir = data)) {
        return(-1)
      }
      
      entry <- get(key, envir = data)
      if (is.null(entry$expires_at)) {
        return(NULL)
      }
      if (is_expired(key)) {
        return(-1)
      }
      
      remaining <- as.numeric(entry$expires_at - Sys.time(), units = "secs")
      return(max(0, remaining))
    },
    
    # Get or compute a value (memoization pattern)
    get_or_set = function(key, factory, ttl = NULL) {
      if (has(key)) {
        return(get(key))
      }
      value <- factory()
      set(key, value, ttl)
      return(value)
    },
    
    # Get multiple keys at once
    get_multiple = function(keys, default = NULL) {
      if (!is.character(keys)) {
        stop("keys must be a character vector")
      }
      result <- list()
      for (k in keys) {
        result[[k]] <- get(k, default)
      }
      return(result)
    },
    
    # Set multiple key-value pairs at once
    set_multiple = function(key_values, ttl = NULL) {
      if (!is.list(key_values)) {
        stop("key_values must be a named list")
      }
      for (k in names(key_values)) {
        set(k, key_values[[k]], ttl)
      }
      invisible(NULL)
    },
    
    # Delete multiple keys at once
    delete_multiple = function(keys) {
      if (!is.character(keys)) {
        stop("keys must be a character vector")
      }
      deleted <- 0
      for (k in keys) {
        if (delete(k)) {
          deleted <- deleted + 1
        }
      }
      return(deleted)
    },
    
    # Increment a numeric value
    increment = function(key, amount = 1, default_ttl = NULL) {
      if (!is.character(key) || length(key) != 1) {
        stop("key must be a single character string")
      }
      if (!is.numeric(amount)) {
        stop("amount must be numeric")
      }
      
      current <- get(key, 0)
      if (!is.numeric(current)) {
        current <- 0
      }
      new_value <- current + amount
      set(key, new_value, default_ttl)
      return(new_value)
    },
    
    # Decrement a numeric value
    decrement = function(key, amount = 1, default_ttl = NULL) {
      return(increment(key, -amount, default_ttl))
    },
    
    # Get cache configuration
    get_config = function() {
      return(config)
    }
  ), class = "cache")
}

#' Memoize a function using cache
#'
#' @param fn The function to memoize
#' @param max_size Maximum cache size
#' @param ttl TTL in seconds
#' @param key_fn Optional function to generate cache key from arguments
#' @return A memoized function
#' @export
memoize <- function(fn, max_size = 100, ttl = NULL, key_fn = NULL) {
  cache <- cache_create(max_size = max_size, default_ttl = ttl)
  
  function(...) {
    args <- list(...)
    if (is.null(key_fn)) {
      key <- digest::digest(args)
    } else {
      key <- key_fn(...)
    }
    cache$get_or_set(key, function() fn(...), ttl)
  }
}

#' Create a simple key-value cache with get/set interface
#'
#' @param max_size Maximum number of items
#' @param ttl Default TTL in seconds
#' @return A simple cache object
#' @export
cache_simple <- function(max_size = 1000, ttl = NULL) {
  cache_create(max_size = max_size, default_ttl = ttl)
}

#' Print method for cache objects
#'
#' @param x Cache object
#' @param ... Additional arguments
#' @export
print.cache <- function(x, ...) {
  stats <- x$get_stats()
  cat("Cache (", stats$current_size, "/", stats$max_size, " items)\n", sep = "")
  cat("  Hit rate: ", round(stats$hit_rate * 100, 2), "% (", stats$hits, " hits, ", stats$misses, " misses)\n", sep = "")
  cat("  Evictions: ", stats$evictions, ", Expirations: ", stats$expirations, "\n", sep = "")
  invisible(x)
}
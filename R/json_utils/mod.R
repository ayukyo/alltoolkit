# JSON Utilities for R
# A comprehensive JSON parsing and generation utility module
# Zero dependencies - uses only R standard library
#
# Author: AllToolkit
# Version: 1.0.0

# ============================================================================
# Core JSON Functions
# ============================================================================

#' Parse JSON string to R object
json_parse <- function(json_string) {
  if (is.null(json_string) || json_string == "") {
    stop("JSON string cannot be NULL or empty")
  }
  json_string <- trimws(json_string)
  first_char <- substr(json_string, 1, 1)
  
  if (first_char == "{") {
    return(parse_object(json_string))
  } else if (first_char == "[") {
    return(parse_array(json_string))
  } else if (first_char == '"') {
    return(parse_string(json_string))
  } else if (json_string == "null") {
    return(NULL)
  } else if (json_string == "true") {
    return(TRUE)
  } else if (json_string == "false") {
    return(FALSE)
  } else {
    return(parse_number(json_string))
  }
}

#' Parse JSON string safely, return default on error
json_parse_or_null <- function(json_string, default = NULL) {
  tryCatch({
    json_parse(json_string)
  }, error = function(e) {
    default
  })
}

#' Check if string is valid JSON
json_is_valid <- function(json_string) {
  if (is.null(json_string) || !is.character(json_string)) {
    return(FALSE)
  }
  tryCatch({
    json_parse(json_string)
    TRUE
  }, error = function(e) FALSE)
}

#' Convert R object to JSON string
json_encode <- function(obj, pretty = FALSE, indent = 0) {
  if (is.null(obj)) {
    return("null")
  } else if (is.logical(obj) && length(obj) == 1) {
    return(ifelse(obj, "true", "false"))
  } else if (is.numeric(obj) && length(obj) == 1) {
    if (is.nan(obj)) return("NaN")
    if (is.infinite(obj)) return(ifelse(obj > 0, "Infinity", "-Infinity"))
    return(format(obj, scientific = FALSE, trim = TRUE))
  } else if (is.character(obj) && length(obj) == 1) {
    return(encode_string(obj))
  } else if (is.list(obj)) {
    return(encode_list(obj, pretty, indent))
  } else if (is.vector(obj) && !is.list(obj)) {
    return(encode_vector(obj, pretty, indent))
  } else {
    return(encode_string(as.character(obj)))
  }
}

#' Pretty print JSON string
json_pretty <- function(json_string) {
  obj <- json_parse(json_string)
  json_encode(obj, pretty = TRUE)
}

#' Minify JSON string
json_minify <- function(json_string) {
  obj <- json_parse(json_string)
  json_encode(obj, pretty = FALSE)
}

# ============================================================================
# Type Checking Functions
# ============================================================================

json_is_null <- function(value) is.null(value)
json_is_object <- function(value) is.list(value) && !is.null(names(value))
json_is_array <- function(value) {
  (is.list(value) && is.null(names(value))) || 
    (is.vector(value) && !is.list(value) && length(value) > 1)
}
json_is_string <- function(value) is.character(value) && length(value) == 1
json_is_number <- function(value) is.numeric(value) && length(value) == 1
json_is_boolean <- function(value) is.logical(value) && length(value) == 1

# ============================================================================
# Safe Access Functions
# ============================================================================

json_get <- function(obj, key, default = NULL) {
  if (!is.list(obj) || is.null(names(obj))) return(default)
  if (key %in% names(obj)) {
    val <- obj[[key]]
    if (is.null(val)) return(default)
    return(val)
  }
  return(default)
}

json_get_string <- function(obj, key, default = "") {
  val <- json_get(obj, key, default)
  if (is.character(val) && length(val) == 1) return(val)
  return(default)
}

json_get_number <- function(obj, key, default = 0) {
  val <- json_get(obj, key, default)
  if (is.numeric(val) && length(val) == 1) return(val)
  return(default)
}

json_get_int <- function(obj, key, default = 0L) {
  as.integer(json_get_number(obj, key, default))
}

json_get_bool <- function(obj, key, default = FALSE) {
  val <- json_get(obj, key, default)
  if (is.logical(val) && length(val) == 1) return(val)
  return(default)
}

json_get_path <- function(obj, path, default = NULL) {
  keys <- strsplit(path, "\\.")[[1]]
  current <- obj
  for (key in keys) {
    if (!is.list(current) || !(key %in% names(current))) return(default)
    current <- current[[key]]
    if (is.null(current)) return(default)
  }
  return(current)
}

json_keys <- function(obj) {
  if (!is.list(obj) || is.null(names(obj))) return(character(0))
  return(names(obj))
}

json_has_key <- function(obj, key) {
  if (!is.list(obj) || is.null(names(obj))) return(FALSE)
  return(key %in% names(obj))
}

# ============================================================================
# File I/O Functions
# ============================================================================

json_read_file <- function(filepath) {
  if (!file.exists(filepath)) {
    stop(paste("File not found:", filepath))
  }
  content <- readLines(filepath, warn = FALSE)
  json_parse(paste(content, collapse = "\n"))
}

json_write_file <- function(filepath, obj, pretty = TRUE) {
  json_str <- json_encode(obj, pretty = pretty)
  writeLines(json_str, filepath)
  invisible(TRUE)
}

# ============================================================================
# Internal Helper Functions
# ============================================================================

parse_object <- function(json_string) {
  json_string <- trimws(json_string)
  if (substr(json_string, 1, 1) != "{" || substr(json_string, nchar(json_string), nchar(json_string)) != "}") {
    stop("Invalid JSON object")
  }
  content <- substr(json_string, 2, nchar(json_string) - 1)
  content <- trimws(content)
  if (content == "") return(list())
  
  result <- list()
  pairs <- split_json_pairs(content)
  for (pair in pairs) {
    pair <- trimws(pair)
    colon_pos <- find_colon_outside_strings(pair)
    if (colon_pos == 0) stop("Invalid JSON object pair")
    key_str <- trimws(substr(pair, 1, colon_pos - 1))
    value_str <- trimws(substr(pair, colon_pos + 1, nchar(pair)))
    key <- parse_string(key_str)
    value <- json_parse(value_str)
    result[[key]] <- value
  }
  return(result)
}

parse_array <- function(json_string) {
  json_string <- trimws(json_string)
  if (substr(json_string, 1, 1) != "[" || substr(json_string, nchar(json_string), nchar(json_string)) != "]") {
    stop("Invalid JSON array")
  }
  content <- substr(json_string, 2, nchar(json_string) - 1)
  content <- trimws(content)
  if (content == "") return(list())
  
  elements <- split_json_elements(content)
  result <- lapply(elements, function(e) json_parse(trimws(e)))
  
  if (length(result) > 0) {
    all_numeric <- all(sapply(result, is.numeric))
    all_character <- all(sapply(result, is.character))
    all_logical <- all(sapply(result, is.logical))
    if (all_numeric && !any(sapply(result, function(x) length(x) > 1))) {
      return(unlist(result))
    } else if (all_character && !any(sapply(result, function(x) length(x) > 1))) {
      return(unlist(result))
    } else if (all_logical && !any(sapply(result, function(x) length(x) > 1))) {
      return(unlist(result))
    }
  }
  return(result)
}

parse_string <- function(json_string) {
  json_string <- trimws(json_string)
  n <- nchar(json_string)
  if (n < 2 || substr(json_string, 1, 1) != '"' || substr(json_string, n, n) != '"') {
    stop("Invalid JSON string")
  }
  content <- substr(json_string, 2, n - 1)
  
  # Handle escape sequences
  content <- gsub('\\\\"', '"', content, fixed = TRUE)
  content <- gsub("\\\\n", "\n", content, fixed = TRUE)
  content <- gsub("\\\\t", "\t", content, fixed = TRUE)
  content <- gsub("\\\\r", "\r", content, fixed = TRUE)
  content <- gsub("\\\\\\\\", "\\", content, fixed = TRUE)
  content <- gsub("\\\\b", "\b", content, fixed = TRUE)
  content <- gsub("\\\\f", "\f", content, fixed = TRUE)
  
  return(content)
}

parse_number <- function(json_string) {
  json_string <- trimws(json_string)
  num <- suppressWarnings(as.numeric(json_string))
  if (is.na(num)) {
    stop(paste("Invalid JSON number:", json_string))
  }
  return(num)
}

encode_string <- function(str) {
  if (is.null(str)) return("null")
  str <- as.character(str)
  str <- gsub("\\", "\\\\", str, fixed = TRUE)
  str <- gsub('"', '\\"', str, fixed = TRUE)
  str <- gsub("\n", "\\n", str, fixed = TRUE)
  str <- gsub("\t", "\\t", str, fixed = TRUE)
  str <- gsub("\r", "\\r", str, fixed = TRUE)
  str <- gsub("\b", "\\b", str, fixed = TRUE)
  str <- gsub("\f", "\\f", str, fixed = TRUE)
  return(paste0('"', str, '"'))
}

encode_list <- function(obj, pretty, indent) {
  if (is.null(names(obj))) {
    return(encode_vector(unlist(obj), pretty, indent))
  }
  
  indent_str <- if (pretty) paste0(rep("  ", indent), collapse = "") else ""
  next_indent_str <- if (pretty) paste0(rep("  ", indent + 1), collapse = "") else ""
  newline <- if (pretty) "\n" else ""
  
  if (length(obj) == 0) return("{}")
  
  parts <- c()
  for (key in names(obj)) {
    value <- obj[[key]]
    encoded_value <- json_encode(value, pretty, indent + 1)
    if (pretty) {
      parts <- c(parts, paste0(next_indent_str, encode_string(key), ": ", encoded_value))
    } else {
      parts <- c(parts, paste0(encode_string(key), ":", encoded_value))
    }
  }
  
  if (pretty) {
    return(paste0("{", newline, paste(parts, collapse = paste0(",", newline)), newline, indent_str, "}"))
  } else {
    return(paste0("{", paste(parts, collapse = ","), "}"))
  }
}

encode_vector <- function(obj, pretty, indent) {
  if (length(obj) == 0) return("[]")
  
  indent_str <- if (pretty) paste0(rep("  ", indent), collapse = "") else ""
  next_indent_str <- if (pretty) paste0(rep("  ", indent + 1), collapse = "") else ""
  newline <- if (pretty) "\n" else ""
  
  parts <- sapply(obj, function(x) json_encode(x, pretty, indent + 1))
  
  if (pretty) {
    return(paste0("[", newline, next_indent_str, paste(parts, collapse = paste0(",", newline, next_indent_str)), newline, indent_str, "]"))
  } else {
    return(paste0("[", paste(parts, collapse = ","), "]"))
  }
}

split_json_pairs <- function(content) {
  pairs <- c()
  current <- ""
  depth <- 0
  in_string <- FALSE
  escape_next <- FALSE
  
  for (i in 1:nchar(content)) {
    char <- substr(content, i, i)
    
    if (escape_next) {
      current <- paste0(current, char)
      escape_next <- FALSE
      next
    }
    
    if (char == "\\") {
      current <- paste0(current, char)
      escape_next <- TRUE
      next
    }
    
    if (char == '"' && !escape_next) {
      in_string <- !in_string
      current <- paste0(current, char)
      next
    }
    
    if (!in_string) {
      if (char %in% c("{", "[")) {
        depth <- depth + 1
      } else if (char %in% c("}", "]")) {
        depth <- depth - 1
      } else if (char == "," && depth == 0) {
        pairs <- c(pairs, current)
        current <- ""
        next
      }
    }
    
    current <- paste0(current, char)
  }
  
  if (current != "") {
    pairs <- c(pairs, current)
  }
  
  return(pairs)
}

split_json_elements <- function(content) {
  split_json_pairs(content)
}

find_colon_outside_strings <- function(str) {
  in_string <- FALSE
  escape_next <- FALSE
  
  for (i in 1:nchar(str)) {
    char <- substr(str, i, i)
    
    if (escape_next) {
      escape_next <- FALSE
      next
    }
    
    if (char == "\\") {
      escape_next <- TRUE
      next
    }
    
    if (char == '"' && !escape_next) {
      in_string <- !in_string
      next
    }
    
    if (char == ":" && !in_string) {
      return(i)
    }
  }
  
  return(0)
}

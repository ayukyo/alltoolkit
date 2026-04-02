# HTTP Utilities Test Suite for R
# Run with: Rscript http_utils_test.R

# Load the module
source("mod.R")

# Test counter
tests_passed <- 0
tests_failed <- 0

#' Run a test and report results
test <- function(name, expression) {
  result <- tryCatch({
    eval(expression)
  }, error = function(e) {
    message(paste("ERROR in", name, ":", conditionMessage(e)))
    return(FALSE)
  })

  if (isTRUE(result)) {
    cat(paste0("[PASS] ", name, "\n"))
    tests_passed <<- tests_passed + 1
  } else {
    cat(paste0("[FAIL] ", name, "\n"))
    tests_failed <<- tests_failed + 1
  }
}

#' Assert equals
assert_equal <- function(actual, expected) {
  return(identical(actual, expected))
}

#' Assert true
assert_true <- function(value) {
  return(isTRUE(value))
}

#' Assert false
assert_false <- function(value) {
  return(isTRUE(!isTRUE(value)))
}

#' Assert not null
assert_not_null <- function(value) {
  return(!is.null(value))
}

#' Assert null
assert_null <- function(value) {
  return(is.null(value))
}

#' Assert contains
assert_contains <- function(haystack, needle) {
  return(grepl(needle, haystack, fixed = TRUE))
}

# ==================== URL ENCODING TESTS ====================

test("url_encode: simple string", {
  assert_equal(url_encode("hello"), "hello")
})

test("url_encode: string with spaces", {
  assert_equal(url_encode("hello world"), "hello%20world")
})

test("url_encode: special characters", {
  assert_equal(url_encode("a+b=c"), "a%2Bb%3Dc")
})

test("url_encode: Chinese characters", {
  result <- url_encode("中文")
  assert_true(grepl("%", result))
})

test("url_encode: empty string", {
  assert_equal(url_encode(""), "")
})

test("url_encode: null value", {
  assert_equal(url_encode(NULL), "")
})

# ==================== URL DECODING TESTS ====================

test("url_decode: simple string", {
  assert_equal(url_decode("hello"), "hello")
})

test("url_decode: encoded spaces", {
  assert_equal(url_decode("hello%20world"), "hello world")
})

test("url_decode: plus sign to space", {
  assert_equal(url_decode("hello+world"), "hello world")
})

test("url_decode: special characters", {
  assert_equal(url_decode("a%2Bb%3Dc"), "a+b=c")
})

test("url_decode: empty string", {
  assert_equal(url_decode(""), "")
})

# ==================== BUILD URL TESTS ====================

test("build_url: no parameters", {
  assert_equal(build_url("https://example.com"), "https://example.com")
})

test("build_url: with parameters", {
  result <- build_url("https://api.example.com/users", list(page = 1, limit = 10))
  assert_true(grepl("https://api.example.com/users", result))
  assert_true(grepl("page=1", result))
  assert_true(grepl("limit=10", result))
})

test("build_url: with existing query", {
  result <- build_url("https://example.com?existing=1", list(new = 2))
  assert_true(grepl("existing=1", result))
  assert_true(grepl("new=2", result))
})

test("build_url: empty parameters", {
  assert_equal(build_url("https://example.com", list()), "https://example.com")
})

# ==================== PARSE URL TESTS ====================

test("parse_url: full URL", {
  parsed <- parse_url("https://api.example.com:8080/users?page=1#section")
  assert_equal(parsed$scheme, "https")
  assert_equal(parsed$host, "api.example.com")
  assert_equal(parsed$port, 8080)
  assert_equal(parsed$path, "/users")
  assert_equal(parsed$query, "page=1")
  assert_equal(parsed$fragment, "section")
})

test("parse_url: simple URL", {
  parsed <- parse_url("https://example.com")
  assert_equal(parsed$scheme, "https")
  assert_equal(parsed$host, "example.com")
})

test("parse_url: default port for HTTP", {
  parsed <- parse_url("http://example.com/path")
  assert_equal(parsed$port, 80)
})

test("parse_url: default port for HTTPS", {
  parsed <- parse_url("https://example.com/path")
  assert_equal(parsed$port, 443)
})

test("parse_url: null URL", {
  assert_null(parse_url(NULL))
})

test("parse_url: empty URL", {
  assert_null(parse_url(""))
})

# ==================== PARSE QUERY STRING TESTS ====================

test("parse_query_string: simple parameters", {
  result <- parse_query_string("page=1&limit=10")
  assert_equal(result$page, "1")
  assert_equal(result$limit, "10")
})

test("parse_query_string: empty string", {
  result <- parse_query_string("")
  assert_equal(length(result), 0)
})

test("parse_query_string: null value", {
  result <- parse_query_string(NULL)
  assert_equal(length(result), 0)
})

test("parse_query_string: encoded values", {
  result <- parse_query_string("name=hello%20world")
  assert_equal(result$name, "hello world")
})

# ==================== BUILD QUERY STRING TESTS ====================

test("build_query_string: simple parameters", {
  result <- build_query_string(list(page = 1, limit = 10))
  assert_true(grepl("page=1", result))
  assert_true(grepl("limit=10", result))
})

test("build_query_string: empty list", {
  assert_equal(build_query_string(list()), "")
})

test("build_query_string: with special characters", {
  result <- build_query_string(list(name = "hello world"))
  assert_true(grepl("name=hello%20world", result))
})

# ==================== JSON ENCODE TESTS ====================

test("json_encode: null", {
  assert_equal(json_encode(NULL), "null")
})

test("json_encode: true", {
  assert_equal(json_encode(TRUE), "true")
})

test("json_encode: false", {
  assert_equal(json_encode(FALSE), "false")
})

test("json_encode: number", {
  assert_equal(json_encode(42), "42")
})

test("json_encode: float", {
  result <- json_encode(3.14)
  assert_true(grepl("3.14", result))
})

test("json_encode: string", {
  assert_equal(json_encode("hello"), '"hello"')
})

test("json_encode: string with quotes", {
  result <- json_encode('say "hello"')
  assert_true(grepl('\\"', result))
})

test("json_encode: empty list", {
  assert_equal(json_encode(list()), "{}")
})

test("json_encode: named list", {
  result <- json_encode(list(name = "test", value = 123))
  assert_true(grepl('"name":"test"', result))
  assert_true(grepl('"value":123', result))
})

test("json_encode: vector", {
  result <- json_encode(c(1, 2, 3))
  assert_equal(result, "[1,2,3]")
})

# ==================== JSON DECODE TESTS ====================

test("json_decode: null", {
  assert_null(json_decode("null"))
})

test("json_decode: true", {
  assert_equal(json_decode("true"), TRUE)
})

test("json_decode: false", {
  assert_equal(json_decode("false"), FALSE)
})

test("json_decode: number", {
  assert_equal(json_decode("42"), 42)
})

test("json_decode: float", {
  result <- json_decode("3.14")
  assert_true(abs(result - 3.14) < 0.001)
})

test("json_decode: string", {
  assert_equal(json_decode('"hello"'), "hello")
})

test("json_decode: empty array", {
  result <- json_decode("[]")
  assert_equal(length(result), 0)
})

test("json_decode: array of numbers", {
  result <- json_decode("[1,2,3]")
  assert_equal(result[[1]], 1)
  assert_equal(result[[2]], 2)
  assert_equal(result[[3]], 3)
})

test("json_decode: empty object", {
  result <- json_decode("{}")
  assert_equal(length(result), 0)
})

test("json_decode: simple object", {
  result <- json_decode('{"name":"test","value":123}')
  assert_equal(result$name, "test")
  assert_equal(result$value, 123)
})

test("json_decode: nested object", {
  result <- json_decode('{"user":{"name":"John","age":30}}')
  assert_equal(result$user$name, "John")
  assert_equal(result$user$age, 30)
})

## ==================== URL VALIDATION TESTS ====================

test("is_valid_url: valid HTTPS URL", {
  assert_true(is_valid_url("https://example.com"))
})

test("is_valid_url: valid HTTP URL", {
  assert_true(is_valid_url("http://example.com"))
})

test("is_valid_url: valid URL with path", {
  assert_true(is_valid_url("https://api.example.com/v1/users"))
})

test("is_valid_url: invalid URL", {
  assert_false(is_valid_url("not a url"))
})

test("is_valid_url: empty string", {
  assert_false(is_valid_url(""))
})

test("is_valid_url: null value", {
  assert_false(is_valid_url(NULL))
})

# ==================== DOMAIN EXTRACTION TESTS ====================

test("get_domain: simple URL", {
  assert_equal(get_domain("https://example.com"), "example.com")
})

test("get_domain: with subdomain", {
  assert_equal(get_domain("https://api.example.com/users"), "api.example.com")
})

test("get_domain: with port", {
  assert_equal(get_domain("https://example.com:8080"), "example.com")
})

test("get_domain: null URL", {
  assert_null(get_domain(NULL))
})

# ==================== PATH EXTRACTION TESTS ====================

test("get_path: simple path", {
  assert_equal(get_path("https://example.com/api/users"), "/api/users")
})

test("get_path: root path", {
  assert_equal(get_path("https://example.com"), "/")
})

test("get_path: with query", {
  assert_equal(get_path("https://example.com/api?page=1"), "/api")
})

# ==================== TIMEOUT TESTS ====================

test("get_http_timeout: default value", {
  assert_equal(get_http_timeout(), 30)
})

test("set_http_timeout: change value", {
  old <- set_http_timeout(60)
  assert_equal(get_http_timeout(), 60)
  set_http_timeout(old)  # Restore
  assert_equal(get_http_timeout(), 30)
})

# ==================== PRINT SUMMARY ====================

cat("\n========================================\n")
cat(paste0("Tests Passed: ", tests_passed, "\n"))
cat(paste0("Tests Failed: ", tests_failed, "\n"))
cat(paste0("Total Tests:  ", tests_passed + tests_failed, "\n"))
cat("========================================\n")

if (tests_failed > 0) {
  quit(status = 1)
} else {
  cat("All tests passed!\n")
}

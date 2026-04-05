# JSON Utilities Test Suite for R
source("mod.R")

tests_passed <- 0
tests_failed <- 0

run_test <- function(test_name, test_fn) {
  result <- tryCatch({
    test_fn()
    TRUE
  }, error = function(e) {
    cat(paste("FAIL:", test_name, "-", conditionMessage(e), "\n"))
    FALSE
  })
  if (result) {
    tests_passed <<- tests_passed + 1
    cat(paste("PASS:", test_name, "\n"))
  } else {
    tests_failed <<- tests_failed + 1
  }
}

assert_equal <- function(actual, expected) {
  if (!identical(actual, expected)) {
    stop(paste("Expected:", deparse(expected), "Got:", deparse(actual)))
  }
}

assert_true <- function(value) {
  if (!isTRUE(value)) stop(paste("Expected TRUE, got:", deparse(value)))
}

assert_false <- function(value) {
  if (!identical(value, FALSE)) stop(paste("Expected FALSE, got:", deparse(value)))
}

cat("Running JSON Utils Tests...\n\n")

run_test("Parse null", function() { assert_equal(json_parse("null"), NULL) })
run_test("Parse true", function() { assert_equal(json_parse("true"), TRUE) })
run_test("Parse false", function() { assert_equal(json_parse("false"), FALSE) })
run_test("Parse number", function() { 
  assert_equal(json_parse("42"), 42)
  assert_equal(json_parse("3.14"), 3.14)
})
run_test("Parse string", function() { assert_equal(json_parse('"hello"'), "hello") })
run_test("Parse empty object", function() { assert_equal(json_parse("{}"), list()) })
run_test("Parse simple object", function() {
  result <- json_parse('{"name": "John", "age": 30}')
  assert_equal(result$name, "John")
  assert_equal(result$age, 30)
})
run_test("Parse empty array", function() { assert_equal(json_parse("[]"), list()) })
run_test("Parse numeric array", function() { assert_equal(json_parse("[1, 2, 3]"), c(1, 2, 3)) })
run_test("Parse string array", function() { assert_equal(json_parse('["a", "b", "c"]'), c("a", "b", "c")) })
run_test("Parse nested object", function() {
  result <- json_parse('{"user": {"name": "John"}}')
  assert_equal(result$user$name, "John")
})
run_test("Encode null", function() { assert_equal(json_encode(NULL), "null") })
run_test("Encode boolean", function() {
  assert_equal(json_encode(TRUE), "true")
  assert_equal(json_encode(FALSE), "false")
})
run_test("Encode number", function() { assert_equal(json_encode(42), "42") })
run_test("Encode string", function() { assert_equal(json_encode("hello"), '"hello"') })
run_test("Encode vector", function() { assert_equal(json_encode(c(1, 2, 3)), "[1,2,3]") })
run_test("Is valid JSON", function() {
  assert_true(json_is_valid('{"a": 1}'))
  assert_false(json_is_valid("invalid"))
})
run_test("Parse or null", function() {
  assert_equal(json_parse_or_null("invalid", "default"), "default")
  assert_equal(json_parse_or_null('"valid"', "default"), "valid")
})
run_test("Type checking", function() {
  assert_true(json_is_null(NULL))
  assert_true(json_is_object(list(a = 1)))
  assert_true(json_is_array(c(1, 2, 3)))
})
run_test("Safe get", function() {
  obj <- json_parse('{"name": "John"}')
  assert_equal(json_get(obj, "name"), "John")
  assert_equal(json_get(obj, "missing", "default"), "default")
})
run_test("Get string", function() {
  obj <- json_parse('{"name": "John"}')
  assert_equal(json_get_string(obj, "name"), "John")
})
run_test("Get number", function() {
  obj <- json_parse('{"age": 30}')
  assert_equal(json_get_number(obj, "age"), 30)
})
run_test("Get bool", function() {
  obj <- json_parse('{"active": true}')
  assert_equal(json_get_bool(obj, "active"), TRUE)
})
run_test("Get path", function() {
  obj <- json_parse('{"user": {"name": "John"}}')
  assert_equal(json_get_path(obj, "user.name"), "John")
})
run_test("Keys", function() {
  obj <- json_parse('{"a": 1, "b": 2}')
  keys <- json_keys(obj)
  assert_true("a" %in% keys)
})
run_test("Has key", function() {
  obj <- json_parse('{"a": 1}')
  assert_true(json_has_key(obj, "a"))
  assert_false(json_has_key(obj, "b"))
})
run_test("Escape sequences", function() {
  result <- json_parse('"hello\\nworld"')
  assert_equal(result, "hello\nworld")
})
run_test("Empty string", function() { assert_equal(json_parse('""'), "") })
run_test("Unicode string", function() {
  result <- json_encode("你好")
  assert_true(grepl("你好", result))
})

cat(paste("\n========================================\n"))
cat(paste("Tests passed:", tests_passed, "\n"))
cat(paste("Tests failed:", tests_failed, "\n"))
cat(paste("Total tests:", tests_passed + tests_failed, "\n"))

if (tests_failed > 0) {
  quit(status = 1)
}

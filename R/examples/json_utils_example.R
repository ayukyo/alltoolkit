# JSON Utilities Example for R
# Demonstrates usage of json_utils module

source("../json_utils/mod.R")

cat("=== JSON Utilities Examples ===\n\n")

# Example 1: Basic parsing
cat("1. Basic Parsing:\n")
json_str <- '{"name": "John Doe", "age": 30, "active": true}'
parsed <- json_parse(json_str)
cat("Parsed:", json_str, "\n")
cat("Name:", parsed$name, "\n")
cat("Age:", parsed$age, "\n")
cat("Active:", parsed$active, "\n\n")

# Example 2: Arrays
cat("2. Arrays:\n")
arr_json <- '[1, 2, 3, 4, 5]'
arr <- json_parse(arr_json)
cat("Array:", arr_json, "\n")
cat("Sum:", sum(arr), "\n\n")

# Example 3: Nested objects
cat("3. Nested Objects:\n")
nested <- '{"user": {"profile": {"name": "Alice", "city": "Beijing"}}}'
obj <- json_parse(nested)
cat("City:", json_get_path(obj, "user.profile.city"), "\n\n")

# Example 4: Encoding
cat("4. Encoding R objects:\n")
data <- list(
  product = "Laptop",
  price = 999.99,
  tags = c("electronics", "computers"),
  in_stock = TRUE
)
encoded <- json_encode(data)
cat("Encoded:", encoded, "\n\n")

# Example 5: Pretty printing
cat("5. Pretty Printing:\n")
pretty <- json_pretty('{"a":1,"b":2}')
cat("Pretty:\n", pretty, "\n\n")

# Example 6: Safe access
cat("6. Safe Access with Defaults:\n")
config <- json_parse('{"host": "localhost"}')
cat("Host:", json_get_string(config, "host"), "\n")
cat("Port (default 8080):", json_get_int(config, "port", 8080), "\n")
cat("Timeout (default 30):", json_get_int(config, "timeout", 30), "\n\n")

# Example 7: Type checking
cat("7. Type Checking:\n")
value <- json_parse('123')
cat("Is number:", json_is_number(value), "\n")
value <- json_parse('"hello"')
cat("Is string:", json_is_string(value), "\n")
value <- json_parse('[1,2,3]')
cat("Is array:", json_is_array(value), "\n\n")

# Example 8: Validation
cat("8. Validation:\n")
cat("Valid JSON:", json_is_valid('{"valid": true}'), "\n")
cat("Invalid JSON:", json_is_valid('not json'), "\n\n")

# Example 9: Working with files
cat("9. File I/O:\n")
test_data <- list(
  users = list(
    list(name = "John", age = 30),
    list(name = "Jane", age = 25)
  ),
  count = 2
)
temp_file <- tempfile(fileext = ".json")
json_write_file(temp_file, test_data)
cat("Written to:", temp_file, "\n")
loaded <- json_read_file(temp_file)
cat("Loaded users count:", loaded$count, "\n")
file.remove(temp_file)
cat("File cleaned up\n\n")

# Example 10: Complex structure
cat("10. Complex Structure:\n")
complex <- list(
  company = "Tech Corp",
  employees = list(
    list(name = "Alice", department = "Engineering", skills = c("R", "Python", "SQL")),
    list(name = "Bob", department = "Marketing", skills = c("SEO", "Content"))
  ),
  metrics = list(
    revenue = 1000000.50,
    growth = 0.25,
    active = TRUE
  )
)
json_output <- json_encode(complex, pretty = TRUE)
cat(json_output, "\n")

cat("\n=== Examples Complete ===\n")

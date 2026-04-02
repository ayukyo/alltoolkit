# HTTP Utilities Example for R
# Demonstrates usage of the HTTP utilities module
#
# Run with: Rscript http_utils_example.R

# Load the module
source("../http_utils/mod.R")

cat("========================================\n")
cat("R HTTP Utilities - Usage Examples\n")
cat("========================================\n\n")

# ==================== URL BUILDING ====================

cat("1. Building URLs with Query Parameters\n")
cat("--------------------------------------\n")

base_url <- "https://api.example.com/users"
params <- list(page = 1, limit = 10, sort = "name")
full_url <- build_url(base_url, params)
cat(paste0("Base URL: ", base_url, "\n"))
cat(paste0("Parameters: page=1, limit=10, sort=name\n"))
cat(paste0("Full URL: ", full_url, "\n\n"))

# ==================== URL PARSING ====================

cat("2. Parsing URLs\n")
cat("---------------\n")

url <- "https://api.example.com:8080/v1/users?page=1&limit=10#details"
parsed <- parse_url(url)
cat(paste0("URL: ", url, "\n"))
cat(paste0("  Scheme:  ", parsed$scheme, "\n"))
cat(paste0("  Host:    ", parsed$host, "\n"))
cat(paste0("  Port:    ", parsed$port, "\n"))
cat(paste0("  Path:    ", parsed$path, "\n"))
cat(paste0("  Query:   ", parsed$query, "\n"))
cat(paste0("  Fragment:", parsed$fragment, "\n\n"))

# ==================== URL ENCODING/DECODING ====================

cat("3. URL Encoding and Decoding\n")
cat("-----------------------------\n")

original <- "hello world! special chars: @#$%"
encoded <- url_encode(original)
decoded <- url_decode(encoded)

cat(paste0("Original: ", original, "\n"))
cat(paste0("Encoded:  ", encoded, "\n"))
cat(paste0("Decoded:  ", decoded, "\n"))
cat(paste0("Match:    ", identical(original, decoded), "\n\n"))

# ==================== QUERY STRING PARSING ====================

cat("4. Parsing Query Strings\n")
cat("------------------------\n")

query <- "name=John%20Doe&age=30&city=New%20York"
parsed_query <- parse_query_string(query)
cat(paste0("Query string: ", query, "\n"))
cat(paste0("Parsed:\n"))
cat(paste0("  name: ", parsed_query$name, "\n"))
cat(paste0("  age:  ", parsed_query$age, "\n"))
cat(paste0("  city: ", parsed_query$city, "\n\n"))

# ==================== JSON ENCODING ====================

cat("5. JSON Encoding\n")
cat("----------------\n")

# Simple values
cat(paste0("NULL -> ", json_encode(NULL), "\n"))
cat(paste0("TRUE -> ", json_encode(TRUE), "\n"))
cat(paste0("42 -> ", json_encode(42), "\n"))
cat(paste0('"hello" -> ', json_encode("hello"), "\n"))

# Named list (object)
data <- list(
  name = "John Doe",
  age = 30,
  email = "john@example.com",
  active = TRUE
)
cat(paste0("Object: ", json_encode(data), "\n"))

# Vector (array)
numbers <- c(1, 2, 3, 4, 5)
cat(paste0("Array:  ", json_encode(numbers), "\n\n"))

# ==================== JSON DECODING ====================

cat("6. JSON Decoding\n")
cat("----------------\n")

json_str <- '{"name":"Jane Doe","age":25,"hobbies":["reading","coding"]}'
decoded <- json_decode(json_str)
cat(paste0("JSON: ", json_str, "\n"))
cat(paste0("Decoded:\n"))
cat(paste0("  name:    ", decoded$name, "\n"))
cat(paste0("  age:     ", decoded$age, "\n"))
cat(paste0("  hobbies: ", paste(decoded$hobbies, collapse = ", "), "\n\n"))

# ==================== URL VALIDATION ====================

cat("7. URL Validation\n")
cat("-----------------\n")

urls <- c(
  "https://example.com",
  "http://localhost:3000",
  "ftp://files.example.com",
  "not a valid url",
  ""
)

for (u in urls) {
  valid <- is_valid_url(u)
  cat(paste0('"', u, '" -> ', if (valid) "VALID" else "INVALID", "\n"))
}
cat("\n")

# ==================== DOMAIN AND PATH EXTRACTION ====================

cat("8. Domain and Path Extraction\n")
cat("-------------------------------\n")

test_url <- "https://api.example.com/v1/users?page=1"
cat(paste0("URL:    ", test_url, "\n"))
cat(paste0("Domain: ", get_domain(test_url), "\n"))
cat(paste0("Path:   ", get_path(test_url), "\n\n"))

# ==================== HTTP REQUESTS (Examples with httpbin.org) ====================

cat("9. HTTP Requests (if curl is available)\n")
cat("---------------------------------------\n")

# Check if curl is available
if (nzchar(Sys.which("curl"))) {
  cat("Curl is available. Running HTTP examples...\n\n")

  # GET request
  cat("GET Request:\n")
  response <- http_get("https://httpbin.org/get")
  cat(paste0("  Status: ", response$status_code, " ", response$status_message, "\n"))
  cat(paste0("  Success: ", response$success, "\n"))
  cat(paste0("  Body length: ", nchar(response$body), " characters\n\n"))

  # POST JSON request
  cat("POST JSON Request:\n")
  post_data <- list(name = "test", value = 123)
  response <- http_post_json("https://httpbin.org/post", post_data)
  cat(paste0("  Status: ", response$status_code, " ", response$status_message, "\n"))
  cat(paste0("  Success: ", response$success, "\n"))
  if (response$success) {
    # Parse the response
    response_data <- json_decode(response$body)
    if (!is.null(response_data$json)) {
      cat(paste0("  Echoed data: ", json_encode(response_data$json), "\n"))
    }
  }
  cat("\n")

  # POST Form request
  cat("POST Form Request:\n")
  form_data <- list(username = "admin", password = "secret123")
  response <- http_post_form("https://httpbin.org/post", form_data)
  cat(paste0("  Status: ", response$status_code, " ", response$status_message, "\n"))
  cat(paste0("  Success: ", response$success, "\n\n"))

} else {
  cat("Curl is not available. HTTP examples skipped.\n")
  cat("Install curl to use HTTP request functions.\n\n")
}

# ==================== TIMEOUT CONFIGURATION ====================

cat("10. Timeout Configuration\n")
cat("-------------------------\n")

cat(paste0("Default timeout: ", get_http_timeout(), " seconds\n"))
old_timeout <- set_http_timeout(60)
cat(paste0("New timeout:     ", get_http_timeout(), " seconds\n"))
set_http_timeout(old_timeout)  # Restore
cat(paste0("Restored to:     ", get_http_timeout(), " seconds\n\n"))

# ==================== COMPLETE WORKFLOW EXAMPLE ====================

cat("11. Complete Workflow Example\n")
cat("-----------------------------\n")

cat("Scenario: Fetch user data from an API\n\n")

# Step 1: Build the URL
api_base <- "https://httpbin.org/get"
request_params <- list(
  userId = "12345",
  includeDetails = "true"
)
request_url <- build_url(api_base, request_params)
cat(paste0("1. Built URL: ", request_url, "\n"))

# Step 2: Set custom headers
request_headers <- list(
  `User-Agent` = "R-HTTP-Utils/1.0",
  `Accept` = "application/json"
)
cat("2. Set custom headers\n")

# Step 3: Make the request (if curl available)
if (nzchar(Sys.which("curl"))) {
  cat("3. Making GET request...\n")
  response <- http_get(request_url, request_headers)

  cat(paste0("4. Response received:\n"))
  cat(paste0("   Status: ", response$status_code, "\n"))
  cat(paste0("   Success: ", response$success, "\n"))

  if (response$success) {
    cat("5. Response body (first 200 chars):\n")
    cat(paste0("   ", substr(response$body, 1, 200), "...\n"))
  }
} else {
  cat("3. Skipped (curl not available)\n")
}

cat("\n========================================\n")
cat("Examples completed!\n")
cat("========================================\n")

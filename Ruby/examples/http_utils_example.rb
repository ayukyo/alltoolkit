#!/usr/bin/env ruby
# frozen_string_literal: true

# HTTP Utils Example
# Demonstrates usage of the HTTP utilities module

require_relative '../http_utils/mod'

puts "=" * 60
puts "HTTP Utils Examples"
puts "=" * 60

# ============================================================================
# Example 1: URL Encoding/Decoding
# ============================================================================
puts "\n--- Example 1: URL Encoding/Decoding ---"

original = "hello world! special chars: &=?#"
encoded = HttpUtils.url_encode(original)
decoded = HttpUtils.url_decode(encoded)

puts "Original: #{original}"
puts "Encoded:  #{encoded}"
puts "Decoded:  #{decoded}"

# ============================================================================
# Example 2: Building Query Strings
# ============================================================================
puts "\n--- Example 2: Building Query Strings ---"

params = {
  'search' => 'ruby programming',
  'page' => '1',
  'limit' => '10'
}

query_string = HttpUtils.build_query_string(params)
puts "Query string: #{query_string}"

# ============================================================================
# Example 3: Building URLs with Parameters
# ============================================================================
puts "\n--- Example 3: Building URLs with Parameters ---"

base_url = 'https://api.example.com/search'
url = HttpUtils.build_url(base_url, params)
puts "Full URL: #{url}"

# Adding to existing query
existing_url = 'https://api.example.com/search?sort=date'
new_url = HttpUtils.build_url(existing_url, { 'page' => '2' })
puts "Updated URL: #{new_url}"

# ============================================================================
# Example 4: Parsing URLs
# ============================================================================
puts "\n--- Example 4: Parsing URLs ---"

url = 'https://user:pass@api.example.com:8080/v1/users?id=123#section'
parsed = HttpUtils.parse_url(url)

if parsed
  puts "Parsed URL components:"
  puts "  Scheme:   #{parsed[:scheme]}"
  puts "  Host:     #{parsed[:host]}"
  puts "  Port:     #{parsed[:port]}"
  puts "  Path:     #{parsed[:path]}"
  puts "  Query:    #{parsed[:query]}"
  puts "  Fragment: #{parsed[:fragment]}"
  puts "  Userinfo: #{parsed[:userinfo]}"
else
  puts "Failed to parse URL"
end

# ============================================================================
# Example 5: Parsing Query Strings
# ============================================================================
puts "\n--- Example 5: Parsing Query Strings ---"

query = 'name=John+Doe&age=30&city=New+York'
parsed_query = HttpUtils.parse_query_string(query)

puts "Parsed query parameters:"
parsed_query.each do |key, value|
  puts "  #{key}: #{value}"
end

# ============================================================================
# Example 6: URL Validation
# ============================================================================
puts "\n--- Example 6: URL Validation ---"

urls_to_test = [
  'https://example.com',
  'http://localhost:3000',
  'ftp://files.example.com',
  'not a url',
  'example.com'
]

urls_to_test.each do |test_url|
  valid = HttpUtils.valid_url?(test_url)
  puts "  #{test_url.ljust(30)} -> #{valid ? 'Valid' : 'Invalid'}"
end

# ============================================================================
# Example 7: Extracting URL Components
# ============================================================================
puts "\n--- Example 7: Extracting URL Components ---"

test_urls = [
  'https://api.github.com/users/octocat',
  'https://www.example.com:8080/path/to/resource',
  'invalid url here'
]

test_urls.each do |test_url|
  domain = HttpUtils.get_domain(test_url)
  path = HttpUtils.get_path(test_url)
  puts "  URL: #{test_url}"
  puts "    Domain: #{domain || 'N/A'}"
  puts "    Path:   #{path || 'N/A'}"
end

# ============================================================================
# Example 8: HTTP Request Options
# ============================================================================
puts "\n--- Example 8: HTTP Request Options ---"

options = HttpUtils::Options.new
options.timeout = 60
options.headers = {
  'Authorization' => 'Bearer token123',
  'Accept' => 'application/json'
}
options.verify_ssl = true

puts "Request options:"
puts "  Timeout:          #{options.timeout} seconds"
puts "  Headers:          #{options.headers.inspect}"
puts "  Follow redirects: #{options.follow_redirects}"
puts "  Max redirects:    #{options.max_redirects}"
puts "  Verify SSL:       #{options.verify_ssl}"

# ============================================================================
# Example 9: Creating a Response Object (for testing)
# ============================================================================
puts "\n--- Example 9: Response Object ---"

response = HttpUtils::Response.new(
  status_code: 200,
  status_message: 'OK',
  headers: {
    'Content-Type' => 'application/json',
    'X-Request-ID' => 'abc123'
  },
  body: '{"status":"success","data":{"id":1,"name":"Test"}}',
  url: 'https://api.example.com/users',
  response_time: 150
)

puts "Response details:"
puts "  Status code:    #{response.status_code}"
puts "  Status message: #{response.status_message}"
puts "  Success:        #{response.success?}"
puts "  Response time:  #{response.response_time}ms"
puts "  Content-Type:   #{response.header('content-type')}"

if response.json?
  puts "  Parsed JSON:    #{response.json.inspect}"
end

# ============================================================================
# Example 10: Practical URL Manipulation
# ============================================================================
puts "\n--- Example 10: Practical URL Manipulation ---"

# Building a search URL
base = 'https://search.example.com'
search_params = {
  'q' => 'ruby http client',
  'category' => 'programming',
  'sort' => 'relevance',
  'page' => '1'
}

search_url = HttpUtils.build_url(base, search_params)
puts "Search URL: #{search_url}"

# Adding pagination
next_page_url = HttpUtils.add_query_params(search_url, { 'page' => '2' })
puts "Next page:  #{next_page_url}"

# ============================================================================
# Example 11: Working with Form Data
# ============================================================================
puts "\n--- Example 11: Simulating Form Submission ---"

form_data = {
  'username' => 'john_doe',
  'email' => 'john@example.com',
  'message' => 'Hello, this is a test message!'
}

# This is how post_form would encode the data
encoded_form = HttpUtils.build_query_string(form_data)
puts "Form data encoded: #{encoded_form}"

# ============================================================================
# Summary
# ============================================================================
puts "\n" + "=" * 60
puts "Examples completed!"
puts "=" * 60
puts "\nNote: Actual HTTP requests require network access."
puts "Use HttpUtils.get(), HttpUtils.post(), etc. for real requests."

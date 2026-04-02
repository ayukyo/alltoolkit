# HTTP Utilities for R
# A zero-dependency HTTP client using only R standard library
#
# Author: AllToolkit
# License: MIT

#' Build URL with query parameters
#'
#' @param base_url The base URL
#' @param params A named list of query parameters
#' @return A complete URL with query string
#' @examples
#' build_url("https://api.example.com/users", list(page = 1, limit = 10))
#' # Returns: "https://api.example.com/users?page=1&limit=10"
build_url <- function(base_url, params = list()) {
  if (length(params) == 0) {
    return(base_url)
  }

  # Build query string
  query_parts <- character(0)
  for (name in names(params)) {
    value <- params[[name]]
    if (!is.null(value) && !is.na(value)) {
      encoded_value <- url_encode(as.character(value))
      query_parts <- c(query_parts, paste0(name, "=", encoded_value))
    }
  }

  if (length(query_parts) == 0) {
    return(base_url)
  }

  query_string <- paste(query_parts, collapse = "&")
  separator <- if (grepl("\\?", base_url)) "&" else "?"

  return(paste0(base_url, separator, query_string))
}

#' URL encode a string
#'
#' @param str The string to encode
#' @return URL-encoded string
#' @examples
#' url_encode("hello world")
#' # Returns: "hello%20world"
url_encode <- function(str) {
  if (is.null(str) || length(str) == 0) {
    return("")
  }

  str <- as.character(str)

  # Characters that don't need encoding
  safe_chars <- "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_.~"

  result <- character(nchar(str))
  for (i in 1:nchar(str)) {
    char <- substr(str, i, i)
    if (char %in% strsplit(safe_chars, "")[[1]]) {
      result[i] <- char
    } else {
      bytes <- charToRaw(char)
      encoded <- paste0("%", toupper(format(bytes, "02x")), collapse = "")
      result[i] <- encoded
    }
  }

  return(paste(result, collapse = ""))
}

#' URL decode a string
#'
#' @param str The URL-encoded string
#' @return Decoded string
#' @examples
#' url_decode("hello%20world")
#' # Returns: "hello world"
url_decode <- function(str) {
  if (is.null(str) || length(str) == 0) {
    return("")
  }

  str <- as.character(str)

  # Replace + with space
  str <- gsub("\\+", " ", str)

  # Decode percent-encoded characters
  while (grepl("%[0-9A-Fa-f]{2}", str)) {
    matches <- gregexpr("%[0-9A-Fa-f]{2}", str)[[1]]
    if (matches[1] == -1) break

    pos <- matches[1]
    hex <- substr(str, pos + 1, pos + 2)
    byte <- as.raw(as.integer(paste0("0x", hex)))
    char <- rawToChar(byte)
    str <- paste0(substr(str, 1, pos - 1), char, substr(str, pos + 3, nchar(str)))
  }

  return(str)
}

#' Parse URL into components
#'
#' @param url The URL to parse
#' @return A list containing URL components: scheme, host, port, path, query, fragment
#' @examples
#' parse_url("https://api.example.com:8080/users?page=1#section")
#' # Returns list with scheme="https", host="api.example.com", port=8080, etc.
parse_url <- function(url) {
  if (is.null(url) || nchar(url) == 0) {
    return(NULL)
  }

  result <- list(
    scheme = NULL,
    host = NULL,
    port = NULL,
    path = NULL,
    query = NULL,
    fragment = NULL,
    userinfo = NULL
  )

  # Extract fragment
  if (grepl("#", url)) {
    parts <- strsplit(url, "#", fixed = TRUE)[[1]]
    url <- parts[1]
    result$fragment <- parts[2]
  }

  # Extract query string
  if (grepl("\\?", url)) {
    parts <- strsplit(url, "\\?", fixed = FALSE)[[1]]
    url <- parts[1]
    result$query <- parts[2]
  }

  # Extract scheme
  if (grepl("://", url)) {
    parts <- strsplit(url, "://", fixed = TRUE)[[1]]
    result$scheme <- tolower(parts[1])
    url <- parts[2]
  }

  # Extract path
  if (grepl("/", url)) {
    parts <- strsplit(url, "/", fixed = TRUE)[[1]]
    result$host <- parts[1]
    result$path <- paste0("/", paste(parts[-1], collapse = "/"))
  } else {
    result$host <- url
    result$path <- "/"
  }

  # Extract port from host
  if (grepl(":", result$host)) {
    parts <- strsplit(result$host, ":", fixed = TRUE)[[1]]
    result$host <- parts[1]
    result$port <- as.integer(parts[2])
  } else if (!is.null(result$scheme)) {
    # Default ports
    if (result$scheme == "http") result$port <- 80
    else if (result$scheme == "https") result$port <- 443
    else if (result$scheme == "ftp") result$port <- 21
  }

  # Extract userinfo
  if (grepl("@", result$host)) {
    parts <- strsplit(result$host, "@", fixed = TRUE)[[1]]
    result$userinfo <- parts[1]
    result$host <- parts[2]
  }

  return(result)
}

#' Parse query string into a list
#'
#' @param query_string The query string (without leading ?)
#' @return A named list of parameters
#' @examples
#' parse_query_string("page=1&limit=10&sort=name")
#' # Returns: list(page="1", limit="10", sort="name")
parse_query_string <- function(query_string) {
  if (is.null(query_string) || nchar(query_string) == 0) {
    return(list())
  }

  params <- list()
  pairs <- strsplit(query_string, "&", fixed = TRUE)[[1]]

  for (pair in pairs) {
    if (grepl("=", pair)) {
      parts <- strsplit(pair, "=", fixed = TRUE)[[1]]
      name <- url_decode(parts[1])
      value <- if (length(parts) > 1) url_decode(parts[2]) else ""
      params[[name]] <- value
    }
  }

  return(params)
}

#' Perform HTTP GET request
#'
#' @param url The URL to request
#' @param headers A named list of HTTP headers
#' @param timeout Request timeout in seconds (default: 30)
#' @return A list containing status_code, status_message, headers, body, and url
#' @examples
#' response <- http_get("https://httpbin.org/get")
#' if (response$status_code == 200) {
#'   cat(response$body)
#' }
http_get <- function(url, headers = list(), timeout = 30) {
  return(http_request("GET", url, NULL, headers, timeout))
}

#' Perform HTTP POST request
#'
#' @param url The URL to request
#' @param body The request body (string)
#' @param headers A named list of HTTP headers
#' @param timeout Request timeout in seconds (default: 30)
#' @return A list containing status_code, status_message, headers, body, and url
#' @examples
#' response <- http_post("https://httpbin.org/post", '{"name":"test"}',
#'                       list(`Content-Type` = "application/json"))
http_post <- function(url, body = NULL, headers = list(), timeout = 30) {
  return(http_request("POST", url, body, headers, timeout))
}

#' Perform HTTP POST request with JSON body
#'
#' @param url The URL to request
#' @param data A list or vector to be serialized as JSON
#' @param headers A named list of HTTP headers
#' @param timeout Request timeout in seconds (default: 30)
#' @return A list containing status_code, status_message, headers, body, and url
#' @examples
#' response <- http_post_json("https://httpbin.org/post", list(name = "test", value = 123))
http_post_json <- function(url, data, headers = list(), timeout = 30) {
  json_body <- json_encode(data)
  headers[["Content-Type"]] <- "application/json"
  return(http_request("POST", url, json_body, headers, timeout))
}

#' Perform HTTP POST request with form data
#'
#' @param url The URL to request
#' @param data A named list of form fields
#' @param headers A named list of HTTP headers
#' @param timeout Request timeout in seconds (default: 30)
#' @return A list containing status_code, status_message, headers, body, and url
#' @examples
#' response <- http_post_form("https://httpbin.org/post", list(username = "admin", password = "secret"))
http_post_form <- function(url, data, headers = list(), timeout = 30) {
  form_body <- build_query_string(data)
  headers[["Content-Type"]] <- "application/x-www-form-urlencoded"
  return(http_request("POST", url, form_body, headers, timeout))
}

#'
#' Perform HTTP PUT request
#'
#' @param url The URL to request
#' @param body The request body (string)
#' @param headers A named list of HTTP headers
#' @param timeout Request timeout in seconds (default: 30)
#' @return A list containing status_code, status_message, headers, body, and url
http_put <- function(url, body = NULL, headers = list(), timeout = 30) {
  return(http_request("PUT", url, body, headers, timeout))
}

#' Perform HTTP PUT request with JSON body
#'
#' @param url The URL to request
#' @param data A list or vector to be serialized as JSON
#' @param headers A named list of HTTP headers
#' @param timeout Request timeout in seconds (default: 30)
#' @return A list containing status_code, status_message, headers, body, and url
http_put_json <- function(url, data, headers = list(), timeout = 30) {
  json_body <- json_encode(data)
  headers[["Content-Type"]] <- "application/json"
  return(http_request("PUT", url, json_body, headers, timeout))
}

#' Perform HTTP DELETE request
#'
#' @param url The URL to request
#' @param headers A named list of HTTP headers
#' @param timeout Request timeout in seconds (default: 30)
#' @return A list containing status_code, status_message, headers, body, and url
http_delete <- function(url, headers = list(), timeout = 30) {
  return(http_request("DELETE", url, NULL, headers, timeout))
}

#' Perform HTTP PATCH request
#'
#' @param url The URL to request
#' @param body The request body (string)
#' @param headers A named list of HTTP headers
#' @param timeout Request timeout in seconds (default: 30)
#' @return A list containing status_code, status_message, headers, body, and url
http_patch <- function(url, body = NULL, headers = list(), timeout = 30) {
  return(http_request("PATCH", url, body, headers, timeout))
}

#' Perform HTTP HEAD request
#'
#' @param url The URL to request
#' @param headers A named list of HTTP headers
#' @param timeout Request timeout in seconds (default: 30)
#' @return A list containing status_code, status_message, headers, body, and url
http_head <- function(url, headers = list(), timeout = 30) {
  return(http_request("HEAD", url, NULL, headers, timeout))
}

#' Internal function to perform HTTP requests
#'
#' @param method HTTP method (GET, POST, PUT, DELETE, PATCH, HEAD)
#' @param url The URL to request
#' @param body The request body (string or NULL)
#' @param headers A named list of HTTP headers
#' @param timeout Request timeout in seconds
#' @return A list containing status_code, status_message, headers, body, and url
http_request <- function(method, url, body = NULL, headers = list(), timeout = 30) {
  # Initialize result
  result <- list(
    status_code = 0,
    status_message = "",
    headers = list(),
    body = "",
    url = url,
    success = FALSE
  )

  # Check if curl is available (preferred method)
  if (nzchar(Sys.which("curl"))) {
    return(http_request_curl(method, url, body, headers, timeout))
  }

  # Fallback to wget
  if (nzchar(Sys.which("wget"))) {
    return(http_request_wget(method, url, body, headers, timeout))
  }

  # Try using R's built-in url() function for simple GET requests
  if (method == "GET") {
    return(http_request_builtin(url, headers, timeout))
  }

  result$status_message <- "No HTTP client available (curl or wget required for non-GET requests)"
  return(result)
}

#' Perform HTTP request using curl command
#'
#' @param method HTTP method
#' @param url The URL
#' @param body Request body
#' @param headers HTTP headers
#' @param timeout Timeout in seconds
#' @return Response list
http_request_curl <- function(method, url, body, headers, timeout) {
  result <- list(
    status_code = 0,
    status_message = "",
    headers = list(),
    body = "",
    url = url,
    success = FALSE
  )

  # Build curl command
  args <- c("-s", "-i", "--max-time", as.character(timeout))

  # Add method
  if (method != "GET") {
    args <- c(args, "-X", method)
  }

  # Add headers
  for (name in names(headers)) {
    args <- c(args, "-H", paste0(name, ": ", headers[[name]]))
  }

  # Add body for POST/PUT/PATCH
  if (!is.null(body) && method %in% c("POST", "PUT", "PATCH")) {
    args <- c(args, "-d", body)
  }

  # Add URL
  args <- c(args, url)

  # Execute curl
  output <- tryCatch({
    system2("curl", args, stdout = TRUE, stderr = TRUE)
  }, error = function(e) {
    result$status_message <<- paste("Curl error:", conditionMessage(e))
    return(NULL)
  })

  if (is.null(output)) {
    return(result)
  }

  # Parse response
  output_text <- paste(output, collapse = "\n")
  return(parse_http_response(output_text, url))
}

#' Perform HTTP request using wget command
#'
#' @param method HTTP method (only GET and POST fully supported)
#' @param url The URL
#' @param body Request body
#' @param headers HTTP headers
#' @param timeout Timeout in seconds
#' @return Response list
http_request_wget <- function(method, url, body, headers, timeout) {
  result <- list(
    status_code = 0,
    status_message = "",
    headers = list(),
    body = "",
    url = url,
    success = FALSE
  )

  # wget only supports GET and POST well
  if (!method %in% c("GET", "POST")) {
    result$status_message <- paste("wget does not support", method, "method")
    return(result)
  }

  # Build wget command
  args <- c("-q", "-O", "-", "--timeout", as.character(timeout), "--server-response")

  # Add headers
  for (name in names(headers)) {
    args <- c(args, "--header", paste0(name, ": ", headers[[name]]))
  }

  # Add body for POST
  if (!is.null(body) && method == "POST") {
    args <- c(args, "--post-data", body)
  }

  # Add URL
  args <- c(args, url)

  # Execute wget
  output <- tryCatch({
    system2("wget", args, stdout = TRUE, stderr = TRUE)
  }, error = function(e) {
    result$status_message <<- paste("Wget error:", conditionMessage(e))
    return(NULL)
  })

  if (is.null(output)) {
    return(result)
  }

  # Parse response (wget outputs headers to stderr)
  output_text <- paste(output, collapse = "\n")
  return(parse_http_response(output_text, url))
}

#' Perform simple HTTP GET using R built-in functions
#'
#' @param url The URL
#' @param headers HTTP headers
#' @param timeout Timeout in seconds
#' @return Response list
http_request_builtin <- function(url, headers, timeout) {
  result <- list(
    status_code = 0,
    status_message = "",
    headers = list(),
    body = "",
    url = url,
    success = FALSE
  )

  con <- tryCatch({
    url(url, open = "r", headers = headers)
  }, error = function(e) {
    result$status_message <<- conditionMessage(e)
    return(NULL)
  })

  if (is.null(con)) {
    return(result)
  }

  on.exit(close(con))

  # Read response body
  result$body <- tryCatch({
    paste(readLines(con, warn = FALSE), collapse = "\n")
  }, error = function(e) {
    result$status_message <<- conditionMessage(e)
    return("")
  })

  # Try to get status
  info <- summary(con)
  result$status_code <- 200  # Built-in doesn't expose status easily
  result$success <- nchar(result$body) > 0

  return(result)
}

#' Parse HTTP response
#'
#' @param response_text Raw response text
#' @param url Original request URL
#' @return Parsed response list
parse_http_response <- function(response_text, url) {
  result <- list(
    status_code = 0,
    status_message = "",
    headers = list(),
    body = "",
    url = url,
    success = FALSE
  )

  if (nchar(response_text) == 0) {
    result$status_message <- "Empty response"
    return(result)
  }

  # Split headers and body
  parts <- strsplit(response_text, "\r\n\r\n|\n\n", perl = TRUE)[[1]]

  if (length(parts) < 1) {
    result$body <- response_text
    return(result)
  }

  header_text <- parts[1]
  result$body <- if (length(parts) > 1) paste(parts[-1], collapse = "\n\n") else ""

  # Parse status line
  lines <- strsplit(header_text, "\r\n|\n")[[1]]
  if (length(lines) > 0) {
    status_line <- lines[1]
    status_match <- regmatches(status_line, regexec("^HTTP/\\d\\.\\d\\s+(\\d+)\\s+(.*)$", status_line))[[1]]
    if (length(status_match) >= 3) {
      result$status_code <- as.integer(status_match[2])
      result$status_message <- status_match[3]
      result$success <- result$status_code >= 200 && result$status_code < 300
    }

    # Parse headers
    for (i in 2:length(lines)) {
      line <- lines[i]
      if (grepl(":", line)) {
        colon_pos <- regexpr(":", line)
        if (colon_pos > 0) {
          name <- trimws(substr(line, 1, colon_pos - 1))
          value <- trimws(substr(line, colon_pos + 1, nchar(line)))
          result$headers[[tolower(name)]] <- value
        }
      }
    }
  }

  return(result)
}

#' Simple JSON encoder (converts R objects to JSON strings)
#'
#' @param x R object to encode (list, vector, or primitive)
#' @return JSON string
#' @examples
#' json_encode(list(name = "test", value = 123))
#' # Returns: '{"name":"test","value":123}'
json_encode <- function(x) {
  if (is.null(x)) {
    return("null")
  }

  if (is.logical(x)) {
    return(tolower(as.character(x)))
  }

  if (is.numeric(x)) {
    if (length(x) == 1) {
      return(as.character(x))
    }
  }

  if (is.character(x)) {
    if (length(x) == 1) {
      escaped <- gsub('\\\\', '\\\\\\\\', x)
      escaped <- gsub('"', '\\\\"', escaped)
      escaped <- gsub('\n', '\\\\n', escaped)
      escaped <- gsub('\r', '\\\\r', escaped)
      escaped <- gsub('\t', '\\\\t', escaped)
      return(paste0('"', escaped, '"'))
    }
  }

  if (is.list(x)) {
    if (length(x) == 0) {
      return("{}")
    }

    # Check if it's a named list (object) or unnamed list (array)
    if (!is.null(names(x)) && any(names(x) != "")) {
      # Named list -> JSON object
      pairs <- character(length(x))
      for (i in seq_along(x)) {
        name <- names(x)[i]
        if (is.null(name) || name == "") {
          name <- as.character(i - 1)
        }
        pairs[i] <- paste0('"', name, '":', json_encode(x[[i]]))
      }
      return(paste0("{", paste(pairs, collapse = ","), "}"))
    } else {
      # Unnamed list -> JSON array
      if (length(x) == 0) {
        return("[]")
      }
      elements <- sapply(x, json_encode)
      return(paste0("[", paste(elements, collapse = ","), "]"))
    }
  }

  if (is.vector(x) && !is.list(x)) {
    if (length(x) == 0) {
      return("[]")
    }
    elements <- sapply(x, json_encode)
    return(paste0("[", paste(elements, collapse = ","), "]"))
  }

  # Default: convert to string
  return(json_encode(as.character(x)))
}

#' Simple JSON decoder (parses JSON strings to R objects)
#'
#' @param json JSON string to parse
#' @return R object (list, vector, or primitive)
#' @examples
#' json_decode('{"name":"test","value":123}')
#' # Returns: list(name = "test", value = 123)
json_decode <- function(json) {
  if (is.null(json) || nchar(trimws(json)) == 0) {
    return(NULL)
  }

  json <- trimws(json)

  # null
  if (json == "null") {
    return(NULL)
  }

  # true/false
  if (json == "true") return(TRUE)
  if (json == "false") return(FALSE)

  # number
  if (grepl("^-?\\d+(\\.\\d+)?([eE][+-]?\\d+)?$", json)) {
    if (grepl("[.eE]", json)) {
      return(as.numeric(json))
    } else {
      return(as.integer(json))
    }
  }

  # string
  if (grepl('^"', json) && grepl('"$', json)) {
    content <- substr(json, 2, nchar(json) - 1)
    # Unescape
    content <- gsub('\\\\n', '\n', content)
    content <- gsub('\\\\r', '\r', content)
    content <- gsub('\\\\t', '\t', content)
    content <- gsub('\\\\"', '"', content)
    content <- gsub('\\\\\\\\', '\\\\', content)
    return(content)
  }

  # array
  if (grepl('^\\[', json) && grepl('\\]$', json)) {
    content <- substr(json, 2, nchar(json) - 1)
    if (nchar(trimws(content)) == 0) {
      return(list())
    }
    elements <- json_split_elements(content)
    return(lapply(elements, json_decode))
  }

  # object
  if (grepl('^\\{', json) && grepl('\\}$', json)) {
    content <- substr(json, 2, nchar(json) - 1)
    if (nchar(trimws(content)) == 0) {
      return(list())
    }
    pairs <- json_split_elements(content)
    result <- list()
    for (pair in pairs) {
      colon_pos <- regexpr('":', pair)
      if (colon_pos > 0) {
        key <- substr(pair, 2, colon_pos - 1)
        value_str <- trimws(substr(pair, colon_pos + 2, nchar(pair)))
        result[[key]] <- json_decode(value_str)
      }
    }
    return(result)
  }

  # Fallback: return as-is
  return(json)
}

#' Split JSON elements (helper for json_decode)
#'
#' @param content JSON content without outer brackets
#' @return Vector of element strings
json_split_elements <- function(content) {
  elements <- character(0)
  current <- ""
  depth <- 0
  in_string <- FALSE
  escape_next <- FALSE

  chars <- strsplit(content, "")[[1]]

  for (char in chars) {
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
      if (char %in% c("[", "{")) {
        depth <- depth + 1
      } else if (char %in% c("]", "}")) {
        depth <- depth - 1
      } else if (char == "," && depth == 0) {
        if (nchar(trimws(current)) > 0) {
          elements <- c(elements, trimws(current))
        }
        current <- ""
        next
      }
    }

    current <- paste0(current, char)
  }

  if (nchar(trimws(current)) > 0) {
    elements <- c(elements, trimws(current))
  }

  return(elements)
}

#' Validate if a string is a valid URL
#'
#' @param url The URL to validate
#' @return TRUE if valid, FALSE otherwise
#' @examples
#' is_valid_url("https://example.com")
#' # Returns: TRUE
#' is_valid_url("not a url")
#' # Returns: FALSE
is_valid_url <- function(url) {
  if (is.null(url) || !is.character(url) || length(url) != 1) {
    return(FALSE)
  }

  pattern <- "^(https?|ftp)://[\\w\\-]+(\\.[\\w\\-]+)+([\\w\\-.,@?^=%&:/~+#]*[\\w\\-@?^=%&/~+#])?$"
  return(grepl(pattern, url, ignore.case = TRUE))
}

#' Get domain from URL
#'
#' @param url The URL
#' @return Domain name (host)
#' @examples
#' get_domain("https://api.example.com/users")
#' # Returns: "api.example.com"
get_domain <- function(url) {
  parsed <- parse_url(url)
  if (is.null(parsed)) {
    return(NULL)
  }
  return(parsed$host)
}

#' Get path from URL
#'
#' @param url The URL
#' @return Path component
#' @examples
#' get_path("https://example.com/api/users?page=1")
#' # Returns: "/api/users"
get_path <- function(url) {
  parsed <- parse_url(url)
  if (is.null(parsed)) {
    return(NULL)
  }
  return(parsed$path)
}

#' Build query string from parameters
#'
#' @param params A named list of parameters
#' @return Query string (without leading ?)
#' @examples
#' build_query_string(list(page = 1, limit = 10))
#' # Returns: "page=1&limit=10"
build_query_string <- function(params) {
  if (length(params) == 0) {
    return("")
  }

  parts <- character(0)
  for (name in names(params)) {
    value <- params[[name]]
    if (!is.null(value) && !is.na(value))
    {
      encoded_value <- url_encode(as.character(value))
      parts <- c(parts, paste0(name, "=", encoded_value))
    }
  }

  return(paste(parts, collapse = "&"))
}

#' Set default timeout for HTTP requests
#'
#' @param seconds Timeout in seconds
#' @return Previous timeout value (invisibly)
set_http_timeout <- function(seconds) {
  old <- getOption("http_utils_timeout", 30)
  options(http_utils_timeout = seconds)
  invisible(old)
}

#' Get current HTTP timeout setting
#'
#' @return Timeout in seconds
get_http_timeout <- function() {
  return(getOption("http_utils_timeout", 30))
}

# url_utils - URL Processing Utilities

A comprehensive Go package for URL processing, normalization, and manipulation with zero external dependencies.

## Features

- **URL Parsing** - Parse URLs with detailed information extraction (scheme, host, port, path, query, fragment, domain, subdomain, TLD)
- **URL Normalization** - Normalize URLs with multiple customizable options
- **Query Parameter Handling** - Parse, build, get, set, add, and remove query parameters
- **URL Building** - Build URLs from scratch or modify existing URLs
- **URL Validation** - Validate URLs and check for HTTP/HTTPS compatibility
- **URL Comparison** - Compare URLs for equality and detect differences
- **URL Extraction** - Extract domain, subdomain, path, query, fragment, file extensions
- **URL Transformations** - Convert schemes, add timestamps, cache busters
- **Special URL Detection** - Detect UUIDs, slugs, and other patterns in URLs

## Installation

```go
import url_utils "github.com/ayukyo/alltoolkit/Go/url_utils"
```

## Quick Start

### Basic Parsing

```go
info, err := url_utils.Parse("https://sub.example.com:8080/api/v1?key=value#section")
if err != nil {
    // Handle error
}

// Access parsed information
fmt.Println(info.Scheme)       // "https"
fmt.Println(info.Host)         // "sub.example.com"
fmt.Println(info.Port)         // "8080"
fmt.Println(info.Path)         // "/api/v1"
fmt.Println(info.Domain)       // "example"
fmt.Println(info.TLD)          // "com"
fmt.Println(info.Subdomain)    // "sub"
fmt.Println(info.IsHTTPS)      // true
fmt.Println(info.IsIP)         // false
fmt.Println(info.IsDefaultPort)// false
```

### URL Normalization

```go
// Default normalization
normalized, _ := url_utils.Normalize("HTTP://EXAMPLE.COM:80/path/")

// Custom normalization options
normalized, _ := url_utils.NormalizeWithOptions(url, url_utils.NormalizeOptions{
    url_utils.NormalizeLowercaseScheme,
    url_utils.NormalizeLowercaseHost,
    url_utils.NormalizeRemoveWWW,
    url_utils.NormalizeRemoveTrailingSlash,
})

// Available options:
// - NormalizeLowercaseScheme
// - NormalizeLowercaseHost
// - NormalizeRemoveDefaultPort
// - NormalizeRemoveWWW / NormalizeAddWWW
// - NormalizeRemoveTrailingSlash / NormalizeAddTrailingSlash
// - NormalizeSortQuery
// - NormalizeRemoveFragment
// - NormalizeRemoveDuplicateSlashes
// - NormalizeDecodeUnreserved
// - NormalizeEncodeReserved
// - NormalizeRemoveIndexPage
// - NormalizeRemoveUTM
```

### Canonical URL

```go
canonical, _ := url_utils.Canonical("HTTPS://WWW.EXAMPLE.COM:443/?utm_source=x&a=2&b=1#section")
// Result: http://example.com?a=1&b=2
```

### Query Parameters

```go
// Get parameter
value, _ := url_utils.GetQueryParam("https://example.com?key=value", "key")

// Set parameter (replaces existing)
url, _ := url_utils.SetQueryParam(url, "key", "newValue")

// Add parameter (appends to existing)
url, _ := url_utils.AddQueryParam(url, "newKey", "value")

// Remove parameter
url, _ := url_utils.RemoveQueryParam(url, "keyToRemove")

// QueryBuilder
qb := url_utils.NewQueryBuilder()
qb.Add("search", "golang")
qb.Add("page", "1")
qb.Add("limit", "10")
query := qb.BuildSorted() // Deterministic order: "limit=10&page=1&search=golang"

// Parse existing query string
qb, _ := url_utils.ParseQuery("a=1&b=2&c=3")
```

### URL Builder

```go
// Build from scratch
url := url_utils.NewURLBuilder()
    .SetScheme("https")
    .SetHost("api.example.com")
    .SetPath("/v1/users")
    .AddQueryParam("id", "123")
    .SetFragment("profile")
    .Build()

// Modify existing URL
builder, _ := url_utils.FromURL("https://example.com:8080/path")
builder.SetScheme("http")
builder.SetPort("3000")
builder.SetQueryParam("key", "value")
url := builder.Build()

// With authentication
url := url_utils.NewURLBuilder()
    .SetScheme("https")
    .SetHost("api.example.com")
    .SetUser("admin")
    .SetPassword("secret")
    .Build()
```

### URL Extraction

```go
domain, _ := url_utils.ExtractDomain("https://sub.example.com/path")    // "example.com"
rootDomain, _ := url_utils.ExtractRootDomain(url)                        // "example.com"
subdomain, _ := url_utils.ExtractSubdomain(url)                          // "sub"
path, _ := url_utils.ExtractPath(url)                                    // "/path"
query, _ := url_utils.ExtractQuery(url)                                  // "key=value"
fragment, _ := url_utils.ExtractFragment(url)                            // "section"
ext, _ := url_utils.GetFileExtension("https://example.com/file.png")     // "png"
scheme, _ := url_utils.GetScheme(url)                                    // "https"
host, _ := url_utils.GetHost(url)                                        // "example.com"
port, _ := url_utils.GetPort("https://example.com:8080")                 // "8080"
```

### URL Validation

```go
err := url_utils.Validate(url)           // Returns error if invalid
valid := url_utils.IsValid(url)          // Returns bool
validHTTP := url_utils.IsValidHTTP(url)  // Checks HTTP/HTTPS only
secure := url_utils.IsSecure(url)        // Checks HTTPS
absolute := url_utils.IsAbsolute(url)    // Has scheme
relative := url_utils.IsRelative(url)    // No scheme
```

### URL Comparison

```go
// Check equality (after normalization)
equal, _ := url_utils.Equals("HTTP://example.com", "http://example.com:80")

// Detailed comparison
diff, _ := url_utils.Compare(url1, url2)
// diff.SchemeDiff, diff.HostDiff, diff.PathDiff, diff.QueryDiff, diff.FragmentDiff

// Same domain/host checks
sameDomain, _ := url_utils.IsSameDomain(url1, url2)
sameHost, _ := url_utils.IsSameHost(url1, url2)
```

### URL Transformations

```go
https, _ := url_utils.ToHTTPS("http://example.com")
http, _ := url_utils.ToHTTP("https://example.com")

// Add timestamp for freshness
url, _ := url_utils.AddTimestamp(url)

// Add cache buster
url, _ := url_utils.AddCacheBuster(url)

// Clean URL (remove UTM, fragments, index pages, etc.)
clean, _ := url_utils.Clean(url)
```

### URL Join and Resolve

```go
// Join paths
url, _ := url_utils.Join("https://example.com/api", "v1", "users")

// Resolve relative URL
url, _ := url_utils.Resolve("https://example.com/base", "/path")
```

### Special URL Checks

```go
// Check for UUID in path
hasUUID := url_utils.IsUUID("https://example.com/users/550e8400-e29b-41d4-a716-446655440000")

// Check for slug in last path segment
isSlug := url_utils.IsSlug("https://example.com/blog/my-awesome-post")
```

### File Extension Handling

```go
ext, _ := url_utils.GetFileExtension("https://example.com/script.js")
url, _ := url_utils.RemoveFileExtension("https://example.com/page.html")
```

## API Reference

### Parsing Functions

| Function | Description |
|----------|-------------|
| `Parse(rawURL)` | Parse URL and return detailed URLInfo |
| `ParseString(rawURL)` | Parse URL and return standard url.URL |

### Normalization Functions

| Function | Description |
|----------|-------------|
| `Normalize(rawURL)` | Normalize with default options |
| `NormalizeWithOptions(rawURL, options)` | Normalize with custom options |
| `Canonical(rawURL)` | Return canonical URL form |
| `Clean(rawURL)` | Clean URL (remove tracking, fragments, etc.) |

### Query Parameter Functions

| Function | Description |
|----------|-------------|
| `GetQueryParam(rawURL, key)` | Get single query parameter |
| `GetQueryParams(rawURL, key)` | Get all values for a key |
| `SetQueryParam(rawURL, key, value)` | Set query parameter |
| `AddQueryParam(rawURL, key, value)` | Add query parameter |
| `RemoveQueryParam(rawURL, key)` | Remove query parameter |
| `NewQueryBuilder()` | Create query builder |
| `ParseQuery(query)` | Parse query string |

### URL Builder Functions

| Function | Description |
|----------|-------------|
| `NewURLBuilder()` | Create URL builder |
| `FromURL(rawURL)` | Create builder from existing URL |

### Validation Functions

| Function | Description |
|----------|-------------|
| `Validate(rawURL)` | Validate URL (returns error) |
| `IsValid(rawURL)` | Check if URL is valid |
| `IsValidHTTP(rawURL)` | Check if HTTP/HTTPS URL |
| `IsAbsolute(rawURL)` | Check if absolute URL |
| `IsRelative(rawURL)` | Check if relative URL |
| `IsSecure(rawURL)` | Check if HTTPS URL |

### Extraction Functions

| Function | Description |
|----------|-------------|
| `ExtractDomain(rawURL)` | Extract domain |
| `ExtractRootDomain(rawURL)` | Extract root domain |
| `ExtractSubdomain(rawURL)` | Extract subdomain |
| `ExtractPath(rawURL)` | Extract path |
| `ExtractQuery(rawURL)` | Extract query string |
| `ExtractFragment(rawURL)` | Extract fragment |
| `GetScheme(rawURL)` | Get scheme |
| `GetHost(rawURL)` | Get host |
| `GetPort(rawURL)` | Get port |
| `GetFileExtension(rawURL)` | Get file extension |

### Comparison Functions

| Function | Description |
|----------|-------------|
| `Equals(url1, url2)` | Check equality (normalized) |
| `Compare(url1, url2)` | Detailed comparison |
| `IsSameDomain(url1, url2)` | Check same domain |
| `IsSameHost(url1, url2)` | Check same host |

### Transformation Functions

| Function | Description |
|----------|-------------|
| `ToHTTPS(rawURL)` | Convert to HTTPS |
| `ToHTTP(rawURL)` | Convert to HTTP |
| `AddTimestamp(rawURL)` | Add timestamp parameter |
| `AddCacheBuster(rawURL)` | Add cache buster parameter |
| `Resolve(base, relative)` | Resolve relative URL |
| `Join(base, segments...)` | Join path segments |

### Utility Functions

| Function | Description |
|----------|-------------|
| `IsUUID(rawURL)` | Check for UUID in path |
| `IsSlug(rawURL)` | Check for slug in path |
| `RemoveFileExtension(rawURL)` | Remove file extension |

## Types

### URLInfo

```go
type URLInfo struct {
    Scheme        string
    Host          string
    Port          string
    Path          string
    Query         url.Values
    Fragment      string
    User          string
    Password      string
    IsDefaultPort bool
    IsIP          bool
    IsHTTPS       bool
    Subdomain     string
    Domain        string
    TLD           string
}
```

### QueryBuilder

```go
qb := NewQueryBuilder()
qb.Add(key, value)     // Add parameter
qb.Set(key, value)     // Set parameter (replace)
qb.Del(key)            // Delete parameter
qb.Get(key)            // Get first value
qb.GetAll(key)         // Get all values
qb.Has(key)            // Check if exists
qb.Build()             // Build query string
qb.BuildSorted()       // Build sorted query string
```

### URLBuilder

```go
b := NewURLBuilder()
b.SetScheme(scheme)
b.SetHost(host)
b.SetPort(port)
b.SetPath(path)
b.AddPath(segments...)
b.SetFragment(fragment)
b.SetUser(user)
b.SetPassword(password)
b.AddQueryParam(key, value)
b.SetQueryParam(key, value)
b.Build()
```

### URLDiff

```go
type URLDiff struct {
    SchemeDiff   bool
    HostDiff     bool
    PortDiff     bool
    PathDiff     bool
    QueryDiff    bool
    FragmentDiff bool
    UserDiff     bool
}
```

## Default Port Mappings

| Scheme | Default Port |
|--------|-------------|
| http | 80 |
| https | 443 |
| ftp | 21 |
| sftp/ssh | 22 |
| smtp | 25 |
| mysql | 3306 |
| postgresql | 5432 |
| redis | 6379 |
| mongodb | 27017 |

## Zero Dependencies

This package uses only Go's standard library:
- `net/url` for URL parsing
- `strconv` for conversions
- `strings` for string operations
- `regexp` for pattern matching
- `sort` for query sorting
- `time` for timestamps
- `encoding/hex` for hex operations

## License

MIT License
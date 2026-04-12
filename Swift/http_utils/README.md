# HTTP Utilities for Swift

A comprehensive HTTP client library for Swift with zero external dependencies. Built on Swift's native `URLSession` for maximum compatibility and performance.

## Features

- 🚀 **Zero Dependencies** - Uses only Swift Foundation framework
- 🔧 **Full HTTP Methods** - GET, POST, PUT, PATCH, DELETE, HEAD, OPTIONS
- 📦 **JSON Support** - Automatic encoding/decoding with Codable
- 🔐 **Authentication** - Bearer token and Basic auth helpers
- 📝 **Form Encoding** - URL-encoded and multipart form data
- ⏱️ **Configurable Timeouts** - Per-request timeout control
- 🏗️ **URL Builder** - Fluent URL construction with query parameters
- ✅ **100% Test Coverage** - Comprehensive unit tests

## Installation

Simply copy the `mod.swift` file to your project. No external dependencies required.

## Quick Start

### Basic GET Request

```swift
import Foundation

// Create a client
let client = HTTPClient(baseURL: "https://api.example.com")

// Simple GET request
let response = try await client.get("/users/1")

if response.isSuccess {
    print(response.string ?? "No data")
}
```

### GET with JSON Decoding

```swift
struct User: Decodable {
    let id: Int
    let name: String
    let email: String
}

let user: User = try await client.get("/users/1")
print("Hello, \(user.name)!")
```

### POST with JSON Body

```swift
struct NewUser: Encodable {
    let name: String
    let email: String
}

let newUser = NewUser(name: "John", email: "john@example.com")
let response = try await client.post("/users", body: newUser)

if response.statusCode == 201 {
    print("User created successfully!")
}
```

### POST with Response Decoding

```swift
struct CreatedUser: Decodable {
    let id: Int
    let name: String
}

let created: CreatedUser = try await client.post("/users", body: newUser)
print("Created user with ID: \(created.id)")
```

## HTTP Methods

```swift
// GET
let response = try await client.get("/users")

// POST
let response = try await client.post("/users", body: newUser)

// PUT
let response = try await client.put("/users/1", body: updatedUser)

// PATCH
let response = try await client.patch("/users/1", body: partialUpdate)

// DELETE
let response = try await client.delete("/users/1")
```

## Authentication

### Bearer Token

```swift
var request = HTTPRequest.get(url)
request.bearerAuth("your-api-token")

let response = try await client.request(request)
```

### Basic Authentication

```swift
var request = HTTPRequest.get(url)
request.basicAuth(username: "user", password: "pass")

let response = try await client.request(request)
```

## Custom Headers

```swift
// Via HTTPRequest
let request = HTTPRequest.get(
    url,
    headers: [
        "Accept": "application/json",
        "X-API-Key": "your-key"
    ]
)

// Via HTTPClient (applied to all requests)
let client = HTTPClient(
    baseURL: "https://api.example.com",
    defaultHeaders: ["Authorization": "Bearer token"]
)
```

## URL Builder

Construct URLs with query parameters easily:

```swift
var builder = URLBuilder(string: "https://api.example.com/search")!
builder.addQueryItem(name: "q", value: "swift")
builder.addQueryItems([
    "page": "1",
    "limit": "20",
    "sort": "desc"
])

let url = builder.build()
// https://api.example.com/search?q=swift&page=1&limit=20&sort=desc
```

## Form Data

### URL-Encoded Forms

```swift
let formData = FormEncoder.formData([
    "username": "john",
    "password": "secret"
])

var request = HTTPRequest(
    url: url,
    method: .post,
    headers: [HTTPHeader.contentType: ContentType.formUrlEncoded],
    body: formData
)
```

### Multipart Form Data

```swift
var multipart = MultipartFormData()
multipart.addField(name: "title", value: "My Document")
multipart.addFile(
    name: "file",
    filename: "document.pdf",
    mimeType: "application/pdf",
    data: pdfData
)

let body = multipart.build()
var request = HTTPRequest(
    url: url,
    method: .post,
    headers: [HTTPHeader.contentType: multipart.contentType],
    body: body
)
```

## Response Handling

```swift
let response = try await client.get("/api/data")

// Check status code categories
if response.isSuccess { /* 2xx */ }
if response.isRedirect { /* 3xx */ }
if response.isClientError { /* 4xx */ }
if response.isServerError { /* 5xx */ }

// Get response as string
let text = response.string

// Decode JSON response
struct Data: Decodable { ... }
let data = try response.decodeJSON(Data.self)
```

## Error Handling

```swift
do {
    let response = try await client.get("/api/data")
    // Handle success
} catch let error as HTTPError {
    switch error {
    case .invalidURL(let url):
        print("Invalid URL: \(url)")
    case .timeout:
        print("Request timed out")
    case .networkError(let underlying):
        print("Network error: \(underlying)")
    case .httpError(let statusCode, let message):
        print("HTTP \(statusCode): \(message ?? "Unknown")")
    case .noData:
        print("No data received")
    default:
        print("Other error: \(error)")
    }
}
```

## Configuration

```swift
// Custom timeout
let request = HTTPRequest(
    url: url,
    timeout: 60.0  // 60 seconds
)

// Custom URLSession configuration
let config = URLSessionConfiguration.default
config.waitsForConnectivity = true
config.timeoutIntervalForRequest = 30

let client = HTTPClient(
    baseURL: "https://api.example.com",
    configuration: config
)
```

## API Reference

### HTTPMethod

```swift
public enum HTTPMethod: String, CaseIterable {
    case get, post, put, patch, delete, head, options
}
```

### HTTPRequest

```swift
public struct HTTPRequest {
    public let url: URL
    public let method: HTTPMethod
    public var headers: HTTPHeaders
    public var body: Data?
    public var timeout: TimeInterval
    
    // Factory methods
    public static func get(_ url: URL, headers: HTTPHeaders) -> HTTPRequest
    public static func postJSON(_ url: URL, body: Encodable) throws -> HTTPRequest
    public static func postData(_ url: URL, body: Data) -> HTTPRequest
    public static func putJSON(_ url: URL, body: Encodable) throws -> HTTPRequest
    public static func delete(_ url: URL, headers: HTTPHeaders) -> HTTPRequest
    public static func patchJSON(_ url: URL, body: Encodable) throws -> HTTPRequest
    
    // Auth helpers
    public mutating func bearerAuth(_ token: String)
    public mutating func basicAuth(username: String, password: String)
}
```

### HTTPResponse

```swift
public struct HTTPResponse {
    public let statusCode: Int
    public let headers: [String: String]
    public let data: Data?
    public let url: URL?
    public let error: Error?
    
    public var isSuccess: Bool      // 2xx
    public var isRedirect: Bool     // 3xx
    public var isClientError: Bool  // 4xx
    public var isServerError: Bool // 5xx
    public var string: String?      // UTF-8 decoded body
    
    public func decodeJSON<T: Decodable>(_ type: T.Type) throws -> T
}
```

### HTTPClient

```swift
public final class HTTPClient {
    public init(baseURL: String? = nil, defaultHeaders: HTTPHeaders = [:])
    public init(baseURL: URL?, defaultHeaders: HTTPHeaders = [:], configuration: URLSessionConfiguration = .default)
    
    public func request(_ request: HTTPRequest) async throws -> HTTPResponse
    public func get(_ path: String, headers: HTTPHeaders) async throws -> HTTPResponse
    public func get<T: Decodable>(_ path: String) async throws -> T
    public func post<T: Encodable>(_ path: String, body: T) async throws -> HTTPResponse
    public func post<T: Encodable, U: Decodable>(_ path: String, body: T) async throws -> U
    public func put<T: Encodable>(_ path: String, body: T) async throws -> HTTPResponse
    public func patch<T: Encodable>(_ path: String, body: T) async throws -> HTTPResponse
    public func delete(_ path: String) async throws -> HTTPResponse
    public func download(_ path: String) async throws -> Data
}
```

## Requirements

- Swift 5.5+ (for async/await support)
- iOS 15.0+ / macOS 12.0+ / tvOS 15.0+ / watchOS 8.0+

## License

MIT License - Part of AllToolkit

---

Created by AllToolkit on 2026-04-13
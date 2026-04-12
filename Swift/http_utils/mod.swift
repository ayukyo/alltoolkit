//
//  HTTPUtils.swift
//  AllToolkit - HTTP Utilities for Swift
//
//  A comprehensive HTTP client library with zero external dependencies.
//  Built on Swift's native URLSession for maximum compatibility.
//
//  Created by AllToolkit on 2026-04-13.
//

import Foundation

// MARK: - HTTP Method

/// Represents HTTP request methods
public enum HTTPMethod: String, CaseIterable {
    case get = "GET"
    case post = "POST"
    case put = "PUT"
    case patch = "PATCH"
    case delete = "DELETE"
    case head = "HEAD"
    case options = "OPTIONS"
}

// MARK: - HTTP Headers

/// Type alias for HTTP headers dictionary
public typealias HTTPHeaders = [String: String]

/// Common HTTP header constants
public struct HTTPHeader {
    public static let contentType = "Content-Type"
    public static let authorization = "Authorization"
    public static let accept = "Accept"
    public static let userAgent = "User-Agent"
    public static let cacheControl = "Cache-Control"
    public static let contentLength = "Content-Length"
    
    private init() {}
}

/// Common content type values
public struct ContentType {
    public static let json = "application/json"
    public static let xml = "application/xml"
    public static let html = "text/html"
    public static let text = "text/plain"
    public static let formUrlEncoded = "application/x-www-form-urlencoded"
    public static let multipartForm = "multipart/form-data"
    public static let octetStream = "application/octet-stream"
    
    private init() {}
}

// MARK: - HTTP Request

/// Represents an HTTP request
public struct HTTPRequest {
    public let url: URL
    public let method: HTTPMethod
    public var headers: HTTPHeaders
    public var body: Data?
    public var timeout: TimeInterval
    
    public init(
        url: URL,
        method: HTTPMethod = .get,
        headers: HTTPHeaders = [:],
        body: Data? = nil,
        timeout: TimeInterval = 30.0
    ) {
        self.url = url
        self.method = method
        self.headers = headers
        self.body = body
        self.timeout = timeout
    }
    
    /// Create a GET request
    public static func get(_ url: URL, headers: HTTPHeaders = [:]) -> HTTPRequest {
        HTTPRequest(url: url, method: .get, headers: headers)
    }
    
    /// Create a POST request with JSON body
    public static func postJSON(_ url: URL, body: Encodable, headers: HTTPHeaders = [:]) throws -> HTTPRequest {
        let data = try JSONEncoder().encode(body)
        var mergedHeaders = headers
        mergedHeaders[HTTPHeader.contentType] = ContentType.json
        return HTTPRequest(url: url, method: .post, headers: mergedHeaders, body: data)
    }
    
    /// Create a POST request with raw data
    public static func postData(_ url: URL, body: Data, contentType: String = ContentType.octetStream, headers: HTTPHeaders = [:]) -> HTTPRequest {
        var mergedHeaders = headers
        mergedHeaders[HTTPHeader.contentType] = contentType
        return HTTPRequest(url: url, method: .post, headers: mergedHeaders, body: body)
    }
    
    /// Create a PUT request
    public static func putJSON(_ url: URL, body: Encodable, headers: HTTPHeaders = [:]) throws -> HTTPRequest {
        let data = try JSONEncoder().encode(body)
        var mergedHeaders = headers
        mergedHeaders[HTTPHeader.contentType] = ContentType.json
        return HTTPRequest(url: url, method: .put, headers: mergedHeaders, body: data)
    }
    
    /// Create a DELETE request
    public static func delete(_ url: URL, headers: HTTPHeaders = [:]) -> HTTPRequest {
        HTTPRequest(url: url, method: .delete, headers: headers)
    }
    
    /// Create a PATCH request
    public static func patchJSON(_ url: URL, body: Encodable, headers: HTTPHeaders = [:]) throws -> HTTPRequest {
        let data = try JSONEncoder().encode(body)
        var mergedHeaders = headers
        mergedHeaders[HTTPHeader.contentType] = ContentType.json
        return HTTPRequest(url: url, method: .patch, headers: mergedHeaders, body: data)
    }
    
    /// Add a header to the request
    public mutating func addHeader(_ key: String, value: String) {
        headers[key] = value
    }
    
    /// Add authorization header (Bearer token)
    public mutating func bearerAuth(_ token: String) {
        headers[HTTPHeader.authorization] = "Bearer \(token)"
    }
    
    /// Add basic authentication
    public mutating func basicAuth(username: String, password: String) {
        let credentials = "\(username):\(password)"
        if let data = credentials.data(using: .utf8) {
            let base64 = data.base64EncodedString()
            headers[HTTPHeader.authorization] = "Basic \(base64)"
        }
    }
}

// MARK: - HTTP Response

/// Represents an HTTP response
public struct HTTPResponse {
    public let statusCode: Int
    public let headers: [String: String]
    public let data: Data?
    public let url: URL?
    public let error: Error?
    
    public init(
        statusCode: Int,
        headers: [String: String] = [:],
        data: Data? = nil,
        url: URL? = nil,
        error: Error? = nil
    ) {
        self.statusCode = statusCode
        self.headers = headers
        self.data = data
        self.url = url
        self.error = error
    }
    
    /// Check if the response is successful (2xx status code)
    public var isSuccess: Bool {
        (200...299).contains(statusCode)
    }
    
    /// Check if the response is a redirect (3xx status code)
    public var isRedirect: Bool {
        (300...399).contains(statusCode)
    }
    
    /// Check if the response is a client error (4xx status code)
    public var isClientError: Bool {
        (400...499).contains(statusCode)
    }
    
    /// Check if the response is a server error (5xx status code)
    public var isServerError: Bool {
        (500...599).contains(statusCode)
    }
    
    /// Get the response body as a string
    public var string: String? {
        guard let data = data else { return nil }
        return String(data: data, encoding: .utf8)
    }
    
    /// Decode the response body as JSON
    public func decodeJSON<T: Decodable>(_ type: T.Type) throws -> T {
        guard let data = data else {
            throw HTTPError.noData
        }
        return try JSONDecoder().decode(type, from: data)
    }
    
    /// Decode the response body as JSON with custom decoder
    public func decodeJSON<T: Decodable>(_ type: T.Type, decoder: JSONDecoder) throws -> T {
        guard let data = data else {
            throw HTTPError.noData
        }
        return try decoder.decode(type, from: data)
    }
}

// MARK: - HTTP Error

/// HTTP-related errors
public enum HTTPError: Error, LocalizedError {
    case invalidURL(String)
    case noData
    case decodingError(Error)
    case networkError(Error)
    case timeout
    case invalidResponse
    case httpError(statusCode: Int, message: String?)
    case cancelled
    
    public var errorDescription: String? {
        switch self {
        case .invalidURL(let url):
            return "Invalid URL: \(url)"
        case .noData:
            return "No data in response"
        case .decodingError(let error):
            return "Failed to decode response: \(error.localizedDescription)"
        case .networkError(let error):
            return "Network error: \(error.localizedDescription)"
        case .timeout:
            return "Request timed out"
        case .invalidResponse:
            return "Invalid response from server"
        case .httpError(let statusCode, let message):
            return "HTTP error \(statusCode): \(message ?? "Unknown error")"
        case .cancelled:
            return "Request was cancelled"
        }
    }
}

// MARK: - HTTP Client

/// HTTP Client for making network requests
public final class HTTPClient {
    
    // MARK: - Properties
    
    private let session: URLSession
    private let baseURL: URL?
    private let defaultHeaders: HTTPHeaders
    private let defaultTimeout: TimeInterval
    
    // MARK: - Initialization
    
    public init(
        baseURL: URL? = nil,
        defaultHeaders: HTTPHeaders = [:],
        defaultTimeout: TimeInterval = 30.0,
        configuration: URLSessionConfiguration = .default
    ) {
        self.baseURL = baseURL
        self.defaultHeaders = defaultHeaders
        self.defaultTimeout = defaultTimeout
        self.session = URLSession(configuration: configuration)
    }
    
    /// Convenience initializer with default configuration
    public convenience init(baseURL: String? = nil, defaultHeaders: HTTPHeaders = [:]) {
        let url = baseURL.flatMap { URL(string: $0) }
        self.init(baseURL: url, defaultHeaders: defaultHeaders)
    }
    
    // MARK: - Request Methods
    
    /// Perform an HTTP request
    public func request(_ request: HTTPRequest) async throws -> HTTPResponse {
        var urlRequest = try buildURLRequest(request)
        
        do {
            let (data, urlResponse) = try await session.data(for: urlRequest)
            
            guard let httpResponse = urlResponse as? HTTPURLResponse else {
                throw HTTPError.invalidResponse
            }
            
            let headers = httpResponse.allHeaderFields.reduce(into: [String: String]()) { result, pair in
                if let key = pair.key as? String, let value = pair.value as? String {
                    result[key] = value
                }
            }
            
            return HTTPResponse(
                statusCode: httpResponse.statusCode,
                headers: headers,
                data: data,
                url: httpResponse.url
            )
        } catch let error as URLError {
            switch error.code {
            case .timedOut:
                throw HTTPError.timeout
            case .cancelled:
                throw HTTPError.cancelled
            default:
                throw HTTPError.networkError(error)
            }
        }
    }
    
    /// Perform a GET request
    public func get(_ path: String, headers: HTTPHeaders = [:]) async throws -> HTTPResponse {
        let url = try resolveURL(path)
        let request = HTTPRequest.get(url, headers: mergeHeaders(headers))
        return try await request(request)
    }
    
    /// Perform a GET request and decode JSON response
    public func get<T: Decodable>(_ path: String, headers: HTTPHeaders = [:], decoder: JSONDecoder = JSONDecoder()) async throws -> T {
        let response = try await get(path, headers: headers)
        return try response.decodeJSON(T.self, decoder: decoder)
    }
    
    /// Perform a POST request with JSON body
    public func post<T: Encodable>(_ path: String, body: T, headers: HTTPHeaders = [:]) async throws -> HTTPResponse {
        let url = try resolveURL(path)
        let request = try HTTPRequest.postJSON(url, body: body, headers: mergeHeaders(headers))
        return try await request(request)
    }
    
    /// Perform a POST request with JSON body and decode JSON response
    public func post<T: Encodable, U: Decodable>(_ path: String, body: T, headers: HTTPHeaders = [:], decoder: JSONDecoder = JSONDecoder()) async throws -> U {
        let response = try await post(path, body: body, headers: headers)
        return try response.decodeJSON(U.self, decoder: decoder)
    }
    
    /// Perform a PUT request with JSON body
    public func put<T: Encodable>(_ path: String, body: T, headers: HTTPHeaders = [:]) async throws -> HTTPResponse {
        let url = try resolveURL(path)
        let request = try HTTPRequest.putJSON(url, body: body, headers: mergeHeaders(headers))
        return try await request(request)
    }
    
    /// Perform a PATCH request with JSON body
    public func patch<T: Encodable>(_ path: String, body: T, headers: HTTPHeaders = [:]) async throws -> HTTPResponse {
        let url = try resolveURL(path)
        let request = try HTTPRequest.patchJSON(url, body: body, headers: mergeHeaders(headers))
        return try await request(request)
    }
    
    /// Perform a DELETE request
    public func delete(_ path: String, headers: HTTPHeaders = [:]) async throws -> HTTPResponse {
        let url = try resolveURL(path)
        let request = HTTPRequest.delete(url, headers: mergeHeaders(headers))
        return try await request(request)
    }
    
    /// Download data from a URL
    public func download(_ path: String) async throws -> Data {
        let url = try resolveURL(path)
        let request = HTTPRequest.get(url)
        let response = try await request(request)
        
        guard let data = response.data else {
            throw HTTPError.noData
        }
        
        return data
    }
    
    // MARK: - Helper Methods
    
    private func buildURLRequest(_ request: HTTPRequest) throws -> URLRequest {
        var urlRequest = URLRequest(url: request.url)
        urlRequest.httpMethod = request.method.rawValue
        urlRequest.timeoutInterval = request.timeout
        urlRequest.httpBody = request.body
        
        for (key, value) in defaultHeaders {
            urlRequest.setValue(value, forHTTPHeaderField: key)
        }
        
        for (key, value) in request.headers {
            urlRequest.setValue(value, forHTTPHeaderField: key)
        }
        
        return urlRequest
    }
    
    private func resolveURL(_ path: String) throws -> URL {
        if let baseURL = baseURL {
            return baseURL.appendingPathComponent(path)
        } else if let url = URL(string: path) {
            return url
        } else {
            throw HTTPError.invalidURL(path)
        }
    }
    
    private func mergeHeaders(_ headers: HTTPHeaders) -> HTTPHeaders {
        defaultHeaders.merging(headers) { (_, new) in new }
    }
}

// MARK: - URL Builder

/// URL builder for constructing URLs with query parameters
public struct URLBuilder {
    private var components: URLComponents
    
    public init?(string: String) {
        guard let components = URLComponents(string: string) else {
            return nil
        }
        self.components = components
    }
    
    public init(url: URL) {
        self.components = URLComponents(url: url, resolvingAgainstBaseURL: false) ?? URLComponents()
    }
    
    /// Add a query parameter
    public mutating func addQueryItem(name: String, value: String) {
        let item = URLQueryItem(name: name, value: value)
        if components.queryItems == nil {
            components.queryItems = [item]
        } else {
            components.queryItems?.append(item)
        }
    }
    
    /// Add multiple query parameters
    public mutating func addQueryItems(_ items: [String: String]) {
        for (name, value) in items {
            addQueryItem(name: name, value: value)
        }
    }
    
    /// Set the path
    public mutating func setPath(_ path: String) {
        components.path = path
    }
    
    /// Build the final URL
    public func build() -> URL? {
        return components.url
    }
}

// MARK: - Form Encoding

/// URL form encoding utilities
public struct FormEncoder {
    
    /// Encode a dictionary to form URL encoded string
    public static func encode(_ parameters: [String: String]) -> String {
        parameters.map { key, value in
            let encodedKey = key.addingPercentEncoding(withAllowedCharacters: .urlQueryAllowed) ?? key
            let encodedValue = value.addingPercentEncoding(withAllowedCharacters: .urlQueryAllowed) ?? value
            return "\(encodedKey)=\(encodedValue)"
        }.joined(separator: "&")
    }
    
    /// Create form data from a dictionary
    public static func formData(_ parameters: [String: String]) -> Data? {
        encode(parameters).data(using: .utf8)
    }
}

// MARK: - Multipart Form Data

/// Multipart form data builder
public class MultipartFormData {
    private var data: Data
    private let boundary: String
    
    public init(boundary: String? = nil) {
        self.boundary = boundary ?? "Boundary-\(UUID().uuidString)"
        self.data = Data()
    }
    
    /// Add a text field
    public func addField(name: String, value: String) {
        data.append("\r\n--\(boundary)\r\n".data(using: .utf8)!)
        data.append("Content-Disposition: form-data; name=\"\(name)\"\r\n\r\n".data(using: .utf8)!)
        data.append(value.data(using: .utf8)!)
    }
    
    /// Add a file field
    public func addFile(name: String, filename: String, mimeType: String, data: Data) {
        self.data.append("\r\n--\(boundary)\r\n".data(using: .utf8)!)
        self.data.append("Content-Disposition: form-data; name=\"\(name)\"; filename=\"\(filename)\"\r\n".data(using: .utf8)!)
        self.data.append("Content-Type: \(mimeType)\r\n\r\n".data(using: .utf8)!)
        self.data.append(data)
    }
    
    /// Build the final data
    public func build() -> Data {
        var finalData = data
        finalData.append("\r\n--\(boundary)--\r\n".data(using: .utf8)!)
        return finalData
    }
    
    /// Get the content type header value
    public var contentType: String {
        return "multipart/form-data; boundary=\(boundary)"
    }
}
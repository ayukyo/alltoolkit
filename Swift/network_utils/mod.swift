import Foundation

public final class NetworkUtils {
    
    public enum HTTPMethod: String {
        case get = "GET"
        case post = "POST"
        case put = "PUT"
        case delete = "DELETE"
        case patch = "PATCH"
        case head = "HEAD"
    }
    
    public struct HTTPResponse {
        public let statusCode: Int
        public let statusMessage: String
        public let headers: [String: String]
        public let body: Data?
        public let bodyString: String?
        public let url: URL
        public let responseTime: TimeInterval
        public let error: Error?
        
        public var isSuccess: Bool { statusCode >= 200 && statusCode < 300 }
        
        public var isJson: Bool {
            guard let contentType = headers["Content-Type"] ?? headers["content-type"] else { return false }
            return contentType.contains("application/json")
        }
        
        public func json<T: Decodable>(as type: T.Type) throws -> T {
            guard let body = body else { throw NetworkError.noData }
            return try JSONDecoder().decode(T.self, from: body)
        }
        
        public func jsonDictionary() -> [String: Any]? {
            guard let body = body else { return nil }
            return try? JSONSerialization.jsonObject(with: body, options: []) as? [String: Any]
        }
        
        public func jsonArray() -> [Any]? {
            guard let body = body else { return nil }
            return try? JSONSerialization.jsonObject(with: body, options: []) as? [Any]
        }
        
        public func header(_ name: String) -> String? {
            let lowerName = name.lowercased()
            for (key, value) in headers {
                if key.lowercased() == lowerName { return value }
            }
            return nil
        }
    }
    
    public enum NetworkError: Error, LocalizedError {
        case invalidURL
        case noData
        case encodingFailed
        case decodingFailed
        case timeout
        case cancelled
        case serverError(Int)
        case clientError(Int)
        case unknown(Error)
        
        public var errorDescription: String? {
            switch self {
            case .invalidURL: return "Invalid URL"
            case .noData: return "No data received"
            case .encodingFailed: return "Failed to encode request body"
            case .decodingFailed: return "Failed to decode response"
            case .timeout: return "Request timed out"
            case .cancelled: return "Request was cancelled"
            case .serverError(let code): return "Server error: \(code)"
            case .clientError(let code): return "Client error: \(code)"
            case .unknown(let error): return error.localizedDescription
            }
        }
    }
    
    public struct RequestOptions {
        public var headers: [String: String]
        public var timeout: TimeInterval
        public var cachePolicy: URLRequest.CachePolicy
        public var allowsCellularAccess: Bool
        public var httpShouldHandleCookies: Bool
        public var retryCount: Int
        public var retryDelay: TimeInterval
        
        public init(headers: [String: String] = [:], timeout: TimeInterval = 30.0, cachePolicy: URLRequest.CachePolicy = .useProtocolCachePolicy, allowsCellularAccess: Bool = true, httpShouldHandleCookies: Bool = true, retryCount: Int = 0, retryDelay: TimeInterval = 1.0) {
            self.headers = headers
            self.timeout = timeout
            self.cachePolicy = cachePolicy
            self.allowsCellularAccess = allowsCellularAccess
            self.httpShouldHandleCookies = httpShouldHandleCookies
            self.retryCount = retryCount
            self.retryDelay = retryDelay
        }
        
        public static let `default` = RequestOptions()
    }
    
    public struct ParsedURL {
        public var scheme: String
        public var host: String
        public var port: Int?
        public var path: String
        public var query: [String: String]
        public var fragment: String?
        public var username: String?
        public var password: String?
        
        public init(scheme: String = "https", host: String = "", port: Int? = nil, path: String = "", query: [String: String] = [:], fragment: String? = nil, username: String? = nil, password: String? = nil) {
            self.scheme = scheme; self.host = host; self.port = port; self.path = path
            self.query = query; self.fragment = fragment; self.username = username; self.password = password
        }
        
        public func build() -> String {
            var url = "\(scheme)://"
            if let username = username {
                url += username
                if let password = password { url += ":\(password)" }
                url += "@"
            }
            url += host
            if let port = port { url += ":\(port)" }
            if !path.hasPrefix("/") { url += "/" }
            url += path
            if !query.isEmpty {
                url += "?" + query.map { "\($0)=\($1.addingPercentEncoding(withAllowedCharacters: .urlQueryAllowed) ?? $1)" }.joined(separator: "&")
            }
            if let fragment = fragment { url += "#\(fragment)" }
            return url
        }
    }
    
    @discardableResult
    public static func get(_ url: String, options: RequestOptions = .default) async throws -> HTTPResponse {
        return try await request(url: url, method: .get, body: nil, contentType: nil, options: options)
    }
    
    @discardableResult
    public static func post(_ url: String, body: Data? = nil, contentType: String? = nil, options: RequestOptions = .default) async throws -> HTTPResponse {
        return try await request(url: url, method: .post, body: body, contentType: contentType, options: options)
    }
    
    @discardableResult
    public static func postJSON<T: Encodable>(_ url: String, data: T, options: RequestOptions = .default) async throws -> HTTPResponse {
        let body = try JSONEncoder().encode(data)
        var opts = options
        opts.headers["Content-Type"] = "application/json"
        return try await request(url: url, method: .post, body: body, contentType: "application/json", options: opts)
    }
    
    @discardableResult
    public static func postForm(_ url: String, data: [String: String], options: RequestOptions = .default) async throws -> HTTPResponse {
        let bodyString = data.map { "\($0)=\($1.addingPercentEncoding(withAllowedCharacters: .urlQueryAllowed) ?? $1)" }.joined(separator: "&")
        let body = bodyString.data(using: .utf8)
        var opts = options
        opts.headers["Content-Type"] = "application/x-www-form-urlencoded"
        return try await request(url: url, method: .post, body: body, contentType: "application/x-www-form-urlencoded", options: opts)
    }
    
    @discardableResult
    public static func put(_ url: String, body: Data? = nil, contentType: String? = nil, options: RequestOptions = .default) async throws -> HTTPResponse {
        return try await request(url: url, method: .put, body: body, contentType: contentType, options: options)
    }
    
    @discardableResult
    public static func putJSON<T: Encodable>(_ url: String, data: T, options: RequestOptions = .default) async throws -> HTTPResponse {
        let body = try JSONEncoder().encode(data)
        var opts = options
        opts.headers["Content-Type"] = "application/json"
        return try await request(url: url, method: .put, body: body, contentType: "application/json", options: opts)
    }
    
    @discardableResult
    public static func delete(_ url: String, options: RequestOptions = .default) async throws -> HTTPResponse
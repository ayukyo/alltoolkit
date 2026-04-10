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
        public var isClientError: Bool { statusCode >= 400 && statusCode < 500 }
        public var isServerError: Bool { statusCode >= 500 && statusCode < 600 }
        public var isRedirect: Bool { statusCode >= 300 && statusCode < 400 }
        
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
            return headers.first { $0.key.lowercased() == lowerName }?.value
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
        
        public init(
            headers: [String: String] = [:],
            timeout: TimeInterval = 30.0,
            cachePolicy: URLRequest.CachePolicy = .useProtocolCachePolicy,
            allowsCellularAccess: Bool = true,
            httpShouldHandleCookies: Bool = true,
            retryCount: Int = 0,
            retryDelay: TimeInterval = 1.0
        ) {
            self.headers = headers
            self.timeout = timeout
            self.cachePolicy = cachePolicy
            self.allowsCellularAccess = allowsCellularAccess
            self.httpShouldHandleCookies = httpShouldHandleCookies
            self.retryCount = max(0, retryCount)
            self.retryDelay = max(0.1, retryDelay)
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
        
        public init(
            scheme: String = "https",
            host: String = "",
            port: Int? = nil,
            path: String = "",
            query: [String: String] = [:],
            fragment: String? = nil,
            username: String? = nil,
            password: String? = nil
        ) {
            self.scheme = scheme
            self.host = host
            self.port = port
            self.path = path
            self.query = query
            self.fragment = fragment
            self.username = username
            self.password = password
        }
        
        public func build() -> String {
            var components = URLComponents()
            components.scheme = scheme
            components.host = host
            components.port = port
            components.path = path.hasPrefix("/") ? path : "/" + path
            components.queryItems = query.isEmpty ? nil : query.map { URLQueryItem(name: $0.key, value: $0.value) }
            components.fragment = fragment
            
            if let username = username {
                components.user = username
                components.password = password
            }
            
            return components.string ?? ""
        }
    }
    
    // MARK: - HTTP Methods
    
    @discardableResult
    public static func get(_ url: String, options: RequestOptions = .default) async throws -> HTTPResponse {
        try await request(url: url, method: .get, body: nil, contentType: nil, options: options)
    }
    
    @discardableResult
    public static func post(_ url: String, body: Data? = nil, contentType: String? = nil, options: RequestOptions = .default) async throws -> HTTPResponse {
        try await request(url: url, method: .post, body: body, contentType: contentType, options: options)
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
        var components = URLComponents()
        components.queryItems = data.map { URLQueryItem(name: $0.key, value: $0.value) }
        let bodyString = components.percentEncodedQuery ?? ""
        let body = bodyString.data(using: .utf8)
        var opts = options
        opts.headers["Content-Type"] = "application/x-www-form-urlencoded"
        return try await request(url: url, method: .post, body: body, contentType: "application/x-www-form-urlencoded", options: opts)
    }
    
    @discardableResult
    public static func put(_ url: String, body: Data? = nil, contentType: String? = nil, options: RequestOptions = .default) async throws -> HTTPResponse {
        try await request(url: url, method: .put, body: body, contentType: contentType, options: options)
    }
    
    @discardableResult
    public static func putJSON<T: Encodable>(_ url: String, data: T, options:
    @discardableResult
    public static func delete(_ url: String, options: RequestOptions = .default) async throws -> HTTPResponse {
        try await request(url: url, method: .delete, body: nil, contentType: nil, options: options)
    }
    
    @discardableResult
    public static func patch(_ url: String, body: Data? = nil, contentType: String? = nil, options: RequestOptions = .default) async throws -> HTTPResponse {
        try await request(url: url, method: .patch, body: body, contentType: contentType, options: options)
    }
    
    @discardableResult
    public static func head(_ url: String, options: RequestOptions = .default) async throws -> HTTPResponse {
        try await request(url: url, method: .head, body: nil, contentType: nil, options: options)
    }
    
    // MARK: - Private Request Method
    
    private static func request(url: String, method: HTTPMethod, body: Data?, contentType: String?, options: RequestOptions) async throws -> HTTPResponse {
        guard let urlObj = URL(string: url) else {
            throw NetworkError.invalidURL
        }
        
        var request = URLRequest(url: urlObj)
        request.httpMethod = method.rawValue
        request.timeoutInterval = options.timeout
        request.cachePolicy = options.cachePolicy
        request.allowsCellularAccess = options.allowsCellularAccess
        request.httpShouldHandleCookies = options.httpShouldHandleCookies
        
        // Add headers
        for (key, value) in options.headers {
            request.setValue(value, forHTTPHeaderField: key)
        }
        
        // Add body
        if let body = body {
            request.httpBody = body
        }
        
        // Add content type if provided
        if let contentType = contentType {
            request.setValue(contentType, forHTTPHeaderField: "Content-Type")
        }
        
        let startTime = Date()
        
        // Perform request with retry logic
        var lastError: Error?
        for attempt in 0...options.retryCount {
            do {
                let (data, response) = try await URLSession.shared.data(for: request)
                let responseTime = Date().timeIntervalSince(startTime)
                
                guard let httpResponse = response as? HTTPURLResponse else {
                    throw NetworkError.noData
                }
                
                var headers: [String: String] = [:]
                for (key, value) in httpResponse.allHeaderFields {
                    if let key = key as? String, let value = value as? String {
                        headers[key] = value
                    }
                }
                
                return HTTPResponse(
                    statusCode: httpResponse.statusCode,
                    statusMessage: HTTPURLResponse.localizedString(forStatusCode: httpResponse.statusCode),
                    headers: headers,
                    body: data,
                    bodyString: String(data: data, encoding: .utf8),
                    url: urlObj,
                    responseTime: responseTime,
                    error: nil
                )
            } catch {
                lastError = error
                if attempt < options.retryCount {
                    try await Task.sleep(nanoseconds: UInt64(options.retryDelay * 1_000_000_000))
                }
            }
        }
        
        throw lastError.map { NetworkError.unknown($0) } ?? NetworkError.unknown(NSError(domain: "NetworkUtils", code: -1))
    }
}

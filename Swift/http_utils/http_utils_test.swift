//
//  HTTPUtilsTest.swift
//  AllToolkit - HTTP Utilities Tests
//
//  Comprehensive tests for HTTP utilities module
//

import XCTest
@testable import HTTPUtils

final class HTTPMethodTests: XCTestCase {
    
    func testHTTPMethodRawValues() {
        XCTAssertEqual(HTTPMethod.get.rawValue, "GET")
        XCTAssertEqual(HTTPMethod.post.rawValue, "POST")
        XCTAssertEqual(HTTPMethod.put.rawValue, "PUT")
        XCTAssertEqual(HTTPMethod.patch.rawValue, "PATCH")
        XCTAssertEqual(HTTPMethod.delete.rawValue, "DELETE")
        XCTAssertEqual(HTTPMethod.head.rawValue, "HEAD")
        XCTAssertEqual(HTTPMethod.options.rawValue, "OPTIONS")
    }
    
    func testHTTPMethodCaseIterable() {
        let allMethods = HTTPMethod.allCases
        XCTAssertEqual(allMethods.count, 7)
        XCTAssertTrue(allMethods.contains(.get))
        XCTAssertTrue(allMethods.contains(.post))
        XCTAssertTrue(allMethods.contains(.put))
    }
}

final class HTTPHeaderTests: XCTestCase {
    
    func testHeaderConstants() {
        XCTAssertEqual(HTTPHeader.contentType, "Content-Type")
        XCTAssertEqual(HTTPHeader.authorization, "Authorization")
        XCTAssertEqual(HTTPHeader.accept, "Accept")
        XCTAssertEqual(HTTPHeader.userAgent, "User-Agent")
        XCTAssertEqual(HTTPHeader.cacheControl, "Cache-Control")
        XCTAssertEqual(HTTPHeader.contentLength, "Content-Length")
    }
    
    func testContentTypeConstants() {
        XCTAssertEqual(ContentType.json, "application/json")
        XCTAssertEqual(ContentType.xml, "application/xml")
        XCTAssertEqual(ContentType.html, "text/html")
        XCTAssertEqual(ContentType.text, "text/plain")
        XCTAssertEqual(ContentType.formUrlEncoded, "application/x-www-form-urlencoded")
        XCTAssertEqual(ContentType.multipartForm, "multipart/form-data")
        XCTAssertEqual(ContentType.octetStream, "application/octet-stream")
    }
}

final class HTTPRequestTests: XCTestCase {
    
    func testBasicRequest() {
        let url = URL(string: "https://example.com/api")!
        let request = HTTPRequest(url: url)
        
        XCTAssertEqual(request.url, url)
        XCTAssertEqual(request.method, .get)
        XCTAssertTrue(request.headers.isEmpty)
        XCTAssertNil(request.body)
        XCTAssertEqual(request.timeout, 30.0)
    }
    
    func testRequestWithCustomValues() {
        let url = URL(string: "https://example.com/api")!
        let headers: HTTPHeaders = ["Custom-Header": "value"]
        let body = "test".data(using: .utf8)!
        
        let request = HTTPRequest(
            url: url,
            method: .post,
            headers: headers,
            body: body,
            timeout: 60.0
        )
        
        XCTAssertEqual(request.method, .post)
        XCTAssertEqual(request.headers["Custom-Header"], "value")
        XCTAssertEqual(request.body, body)
        XCTAssertEqual(request.timeout, 60.0)
    }
    
    func testGetRequest() {
        let url = URL(string: "https://example.com/api")!
        let headers: HTTPHeaders = ["Accept": "application/json"]
        let request = HTTPRequest.get(url, headers: headers)
        
        XCTAssertEqual(request.method, .get)
        XCTAssertEqual(request.headers["Accept"], "application/json")
        XCTAssertNil(request.body)
    }
    
    func testPostJSONRequest() throws {
        struct TestBody: Encodable {
            let name: String
            let value: Int
        }
        
        let url = URL(string: "https://example.com/api")!
        let body = TestBody(name: "test", value: 42)
        let request = try HTTPRequest.postJSON(url, body: body)
        
        XCTAssertEqual(request.method, .post)
        XCTAssertEqual(request.headers[HTTPHeader.contentType], ContentType.json)
        XCTAssertNotNil(request.body)
        
        let decodedBody = try JSONDecoder().decode(TestBody.self, from: request.body!)
        XCTAssertEqual(decodedBody.name, "test")
        XCTAssertEqual(decodedBody.value, 42)
    }
    
    func testPostDataRequest() {
        let url = URL(string: "https://example.com/upload")!
        let data = "file content".data(using: .utf8)!
        let request = HTTPRequest.postData(url, body: data, contentType: ContentType.octetStream)
        
        XCTAssertEqual(request.method, .post)
        XCTAssertEqual(request.headers[HTTPHeader.contentType], ContentType.octetStream)
        XCTAssertEqual(request.body, data)
    }
    
    func testPutJSONRequest() throws {
        struct UpdateBody: Encodable {
            let id: Int
            let status: String
        }
        
        let url = URL(string: "https://example.com/api/1")!
        let body = UpdateBody(id: 1, status: "active")
        let request = try HTTPRequest.putJSON(url, body: body)
        
        XCTAssertEqual(request.method, .put)
        XCTAssertEqual(request.headers[HTTPHeader.contentType], ContentType.json)
        XCTAssertNotNil(request.body)
    }
    
    func testDeleteRequest() {
        let url = URL(string: "https://example.com/api/1")!
        let request = HTTPRequest.delete(url)
        
        XCTAssertEqual(request.method, .delete)
        XCTAssertNil(request.body)
    }
    
    func testPatchJSONRequest() throws {
        struct PatchBody: Encodable {
            let status: String
        }
        
        let url = URL(string: "https://example.com/api/1")!
        let body = PatchBody(status: "updated")
        let request = try HTTPRequest.patchJSON(url, body: body)
        
        XCTAssertEqual(request.method, .patch)
        XCTAssertEqual(request.headers[HTTPHeader.contentType], ContentType.json)
        XCTAssertNotNil(request.body)
    }
    
    func testAddHeader() {
        var request = HTTPRequest(url: URL(string: "https://example.com")!)
        request.addHeader("X-Custom", value: "test")
        
        XCTAssertEqual(request.headers["X-Custom"], "test")
    }
    
    func testBearerAuth() {
        var request = HTTPRequest(url: URL(string: "https://example.com")!)
        request.bearerAuth("my-token")
        
        XCTAssertEqual(request.headers[HTTPHeader.authorization], "Bearer my-token")
    }
    
    func testBasicAuth() {
        var request = HTTPRequest(url: URL(string: "https://example.com")!)
        request.basicAuth(username: "user", password: "pass")
        
        // "user:pass" base64 encoded is "dXNlcjpwYXNz"
        XCTAssertEqual(request.headers[HTTPHeader.authorization], "Basic dXNlcjpwYXNz")
    }
}

final class HTTPResponseTests: XCTestCase {
    
    func testSuccessfulResponse() {
        let data = "success".data(using: .utf8)!
        let response = HTTPResponse(
            statusCode: 200,
            data: data
        )
        
        XCTAssertTrue(response.isSuccess)
        XCTAssertFalse(response.isRedirect)
        XCTAssertFalse(response.isClientError)
        XCTAssertFalse(response.isServerError)
        XCTAssertNil(response.error)
    }
    
    func testCreatedResponse() {
        let response = HTTPResponse(statusCode: 201)
        XCTAssertTrue(response.isSuccess)
    }
    
    func testRedirectResponse() {
        let response = HTTPResponse(statusCode: 301)
        XCTAssertFalse(response.isSuccess)
        XCTAssertTrue(response.isRedirect)
    }
    
    func testClientErrorResponse() {
        let response = HTTPResponse(statusCode: 404)
        XCTAssertFalse(response.isSuccess)
        XCTAssertTrue(response.isClientError)
    }
    
    func testServerErrorResponse() {
        let response = HTTPResponse(statusCode: 500)
        XCTAssertFalse(response.isSuccess)
        XCTAssertTrue(response.isServerError)
    }
    
    func testStringProperty() {
        let data = "hello world".data(using: .utf8)!
        let response = HTTPResponse(statusCode: 200, data: data)
        
        XCTAssertEqual(response.string, "hello world")
    }
    
    func testStringPropertyWithNilData() {
        let response = HTTPResponse(statusCode: 200, data: nil)
        XCTAssertNil(response.string)
    }
    
    func testDecodeJSON() throws {
        struct TestModel: Decodable {
            let name: String
            let count: Int
        }
        
        let json = #"{"name":"test","count":42}"#.data(using: .utf8)!
        let response = HTTPResponse(statusCode: 200, data: json)
        
        let decoded = try response.decodeJSON(TestModel.self)
        XCTAssertEqual(decoded.name, "test")
        XCTAssertEqual(decoded.count, 42)
    }
    
    func testDecodeJSONWithNilDataThrows() {
        struct TestModel: Decodable {
            let name: String
        }
        
        let response = HTTPResponse(statusCode: 200, data: nil)
        
        XCTAssertThrowsError(try response.decodeJSON(TestModel.self)) { error in
            XCTAssertTrue(error is HTTPError)
            if case HTTPError.noData = error {
                // Expected
            } else {
                XCTFail("Expected noData error")
            }
        }
    }
    
    func testDecodeJSONWithCustomDecoder() throws {
        struct TestModel: Decodable {
            let date: Date
        }
        
        let decoder = JSONDecoder()
        decoder.dateDecodingStrategy = .iso8601
        
        let json = #"{"date":"2024-01-15T00:00:00Z"}"#.data(using: .utf8)!
        let response = HTTPResponse(statusCode: 200, data: json)
        
        let decoded = try response.decodeJSON(TestModel.self, decoder: decoder)
        XCTAssertNotNil(decoded.date)
    }
}

final class HTTPErrorTests: XCTestCase {
    
    func testInvalidURLError() {
        let error = HTTPError.invalidURL("not a url")
        XCTAssertEqual(error.errorDescription, "Invalid URL: not a url")
    }
    
    func testNoDataError() {
        let error = HTTPError.noData
        XCTAssertEqual(error.errorDescription, "No data in response")
    }
    
    func testTimeoutError() {
        let error = HTTPError.timeout
        XCTAssertEqual(error.errorDescription, "Request timed out")
    }
    
    func testInvalidResponseError() {
        let error = HTTPError.invalidResponse
        XCTAssertEqual(error.errorDescription, "Invalid response from server")
    }
    
    func testHTTPErrorWithMessage() {
        let error = HTTPError.httpError(statusCode: 404, message: "Not Found")
        XCTAssertEqual(error.errorDescription, "HTTP error 404: Not Found")
    }
    
    func testHTTPErrorWithoutMessage() {
        let error = HTTPError.httpError(statusCode: 500, message: nil)
        XCTAssertEqual(error.errorDescription, "HTTP error 500: Unknown error")
    }
    
    func testCancelledError() {
        let error = HTTPError.cancelled
        XCTAssertEqual(error.errorDescription, "Request was cancelled")
    }
}

final class HTTPClientTests: XCTestCase {
    
    var client: HTTPClient!
    
    override func setUp() {
        super.setUp()
        client = HTTPClient(baseURL: "https://jsonplaceholder.typicode.com")
    }
    
    func testClientInitialization() {
        XCTAssertNotNil(client)
        XCTAssertEqual(client.baseURL, URL(string: "https://jsonplaceholder.typicode.com"))
    }
    
    func testClientWithDefaultHeaders() {
        let headers: HTTPHeaders = ["X-API-Key": "test-key"]
        let clientWithHeaders = HTTPClient(baseURL: "https://example.com", defaultHeaders: headers)
        
        XCTAssertNotNil(clientWithHeaders)
    }
    
    func testClientWithNilBaseURL() {
        let client = HTTPClient(baseURL: nil as String?)
        XCTAssertNil(client.baseURL)
    }
    
    // MARK: - Integration Tests (require network)
    
    func testGETRequest() async throws {
        // This is an integration test that requires network
        let response = try await client.get("/posts/1")
        
        XCTAssertTrue(response.isSuccess)
        XCTAssertNotNil(response.data)
        XCTAssertNotNil(response.string)
    }
    
    func testGETRequestWithDecoding() async throws {
        struct Post: Decodable {
            let id: Int
            let title: String
            let body: String
            let userId: Int
        }
        
        let post: Post = try await client.get("/posts/1")
        
        XCTAssertEqual(post.id, 1)
        XCTAssertFalse(post.title.isEmpty)
    }
    
    func testPOSTRequest() async throws {
        struct NewPost: Encodable {
            let title: String
            let body: String
            let userId: Int
        }
        
        let post = NewPost(title: "Test", body: "Test body", userId: 1)
        let response = try await client.post("/posts", body: post)
        
        XCTAssertTrue(response.isSuccess || response.statusCode == 201)
    }
    
    func testDELETERequest() async throws {
        let response = try await client.delete("/posts/1")
        
        XCTAssertTrue(response.isSuccess)
    }
    
    func testInvalidPath() async {
        do {
            let _ = try await client.get("invalid url with spaces")
            XCTFail("Should have thrown an error")
        } catch {
            // Expected
        }
    }
}

final class URLBuilderTests: XCTestCase {
    
    func testInitWithString() {
        let builder = URLBuilder(string: "https://example.com/api")
        XCTAssertNotNil(builder)
    }
    
    func testInitWithInvalidString() {
        let builder = URLBuilder(string: "not a valid url")
        XCTAssertNotNil(builder) // URLComponents can parse some invalid strings
    }
    
    func testInitWithURL() {
        let url = URL(string: "https://example.com/api")!
        let builder = URLBuilder(url: url)
        XCTAssertNotNil(builder)
    }
    
    func testAddQueryItem() {
        var builder = URLBuilder(string: "https://example.com/api")!
        builder.addQueryItem(name: "page", value: "1")
        
        let url = builder.build()
        XCTAssertEqual(url?.query, "page=1")
    }
    
    func testAddMultipleQueryItems() {
        var builder = URLBuilder(string: "https://example.com/api")!
        builder.addQueryItems([
            "page": "1",
            "limit": "10",
            "sort": "desc"
        ])
        
        let url = builder.build()
        XCTAssertNotNil(url)
        XCTAssertTrue(url!.absoluteString.contains("page=1"))
        XCTAssertTrue(url!.absoluteString.contains("limit=10"))
        XCTAssertTrue(url!.absoluteString.contains("sort=desc"))
    }
    
    func testSetPath() {
        var builder = URLBuilder(string: "https://example.com")!
        builder.setPath("/api/v1/users")
        
        let url = builder.build()
        XCTAssertEqual(url?.path, "/api/v1/users")
    }
    
    func testBuildWithExistingQuery() {
        var builder = URLBuilder(string: "https://example.com/api?existing=value")!
        builder.addQueryItem(name: "new", value: "param")
        
        let url = builder.build()
        XCTAssertNotNil(url)
        XCTAssertTrue(url!.absoluteString.contains("existing=value"))
        XCTAssertTrue(url!.absoluteString.contains("new=param"))
    }
}

final class FormEncoderTests: XCTestCase {
    
    func testEncodeSimpleDictionary() {
        let params = ["name": "John", "age": "30"]
        let encoded = FormEncoder.encode(params)
        
        XCTAssertTrue(encoded.contains("name=John"))
        XCTAssertTrue(encoded.contains("age=30"))
        XCTAssertTrue(encoded.contains("&"))
    }
    
    func testEncodeEmptyDictionary() {
        let params: [String: String] = [:]
        let encoded = FormEncoder.encode(params)
        
        XCTAssertEqual(encoded, "")
    }
    
    func testEncodeSpecialCharacters() {
        let params = ["query": "hello world", "filter": "a&b=c"]
        let encoded = FormEncoder.encode(params)
        
        XCTAssertTrue(encoded.contains("query=hello%20world"))
        XCTAssertTrue(encoded.contains("filter=a%26b%3Dc"))
    }
    
    func testFormData() {
        let params = ["key": "value"]
        let data = FormEncoder.formData(params)
        
        XCTAssertNotNil(data)
        XCTAssertEqual(String(data: data!, encoding: .utf8), "key=value")
    }
}

final class MultipartFormDataTests: XCTestCase {
    
    func testAddField() {
        var multipart = MultipartFormData()
        multipart.addField(name: "username", value: "john")
        
        let data = multipart.build()
        let str = String(data: data, encoding: .utf8)
        
        XCTAssertNotNil(str)
        XCTAssertTrue(str!.contains("name=\"username\""))
        XCTAssertTrue(str!.contains("john"))
    }
    
    func testAddFile() {
        var multipart = MultipartFormData()
        let fileData = "file content".data(using: .utf8)!
        multipart.addFile(
            name: "file",
            filename: "test.txt",
            mimeType: "text/plain",
            data: fileData
        )
        
        let data = multipart.build()
        let str = String(data: data, encoding: .utf8)
        
        XCTAssertNotNil(str)
        XCTAssertTrue(str!.contains("name=\"file\""))
        XCTAssertTrue(str!.contains("filename=\"test.txt\""))
        XCTAssertTrue(str!.contains("Content-Type: text/plain"))
    }
    
    func testContentType() {
        let multipart = MultipartFormData()
        let contentType = multipart.contentType
        
        XCTAssertTrue(contentType.hasPrefix("multipart/form-data; boundary="))
    }
    
    func testMultipleFields() {
        var multipart = MultipartFormData()
        multipart.addField(name: "name", value: "John")
        multipart.addField(name: "email", value: "john@example.com")
        
        let data = multipart.build()
        let str = String(data: data, encoding: .utf8)
        
        XCTAssertNotNil(str)
        XCTAssertTrue(str!.contains("John"))
        XCTAssertTrue(str!.contains("john@example.com"))
    }
    
    func testCustomBoundary() {
        let multipart = MultipartFormData(boundary: "CustomBoundary123")
        let contentType = multipart.contentType
        
        XCTAssertEqual(contentType, "multipart/form-data; boundary=CustomBoundary123")
    }
}

// MARK: - Additional Edge Case Tests

final class EdgeCaseTests: XCTestCase {
    
    func testEmptyBodyPost() {
        let url = URL(string: "https://example.com/api")!
        let request = HTTPRequest(url: url, method: .post)
        
        XCTAssertEqual(request.method, .post)
        XCTAssertNil(request.body)
    }
    
    func testLargeTimeout() {
        let url = URL(string: "https://example.com")!
        let request = HTTPRequest(url: url, timeout: 3600.0)
        
        XCTAssertEqual(request.timeout, 3600.0)
    }
    
    func testUnicodeInURL() {
        let url = URL(string: "https://example.com/搜索?q=测试")!
        let request = HTTPRequest.get(url)
        
        XCTAssertNotNil(request.url)
    }
    
    func testHTTPHeaderCaseSensitivity() {
        var request = HTTPRequest(url: URL(string: "https://example.com")!)
        request.addHeader("content-type", value: "application/json")
        
        // Both keys should be present (HTTP headers are case-insensitive)
        XCTAssertNotNil(request.headers["content-type"])
    }
    
    func testMultipleHeadersWithSameKey() {
        var request = HTTPRequest(url: URL(string: "https://example.com")!)
        request.addHeader("X-Custom", value: "value1")
        request.addHeader("X-Custom", value: "value2")
        
        // Last value should win
        XCTAssertEqual(request.headers["X-Custom"], "value2")
    }
    
    func testResponseStatusCodeBoundaries() {
        // Test all status code category boundaries
        XCTAssertTrue(HTTPResponse(statusCode: 199).isServerError == false)
        XCTAssertFalse(HTTPResponse(statusCode: 199).isSuccess)
        
        XCTAssertTrue(HTTPResponse(statusCode: 200).isSuccess)
        XCTAssertTrue(HTTPResponse(statusCode: 299).isSuccess)
        XCTAssertFalse(HTTPResponse(statusCode: 300).isSuccess)
        
        XCTAssertTrue(HTTPResponse(statusCode: 300).isRedirect)
        XCTAssertTrue(HTTPResponse(statusCode: 399).isRedirect)
        XCTAssertFalse(HTTPResponse(statusCode: 400).isRedirect)
        
        XCTAssertTrue(HTTPResponse(statusCode: 400).isClientError)
        XCTAssertTrue(HTTPResponse(statusCode: 499).isClientError)
        XCTAssertFalse(HTTPResponse(statusCode: 500).isClientError)
        
        XCTAssertTrue(HTTPResponse(statusCode: 500).isServerError)
        XCTAssertTrue(HTTPResponse(statusCode: 599).isServerError)
        XCTAssertFalse(HTTPResponse(statusCode: 600).isServerError)
    }
    
    func testEmptyResponseData() {
        let response = HTTPResponse(statusCode: 204, data: nil)
        
        XCTAssertNil(response.string)
        XCTAssertNil(response.data)
    }
    
    func testBinaryResponseData() {
        let binaryData = Data([0x00, 0x01, 0x02, 0xFF, 0xFE])
        let response = HTTPResponse(statusCode: 200, data: binaryData)
        
        XCTAssertNotNil(response.data)
        XCTAssertEqual(response.data?.count, 5)
    }
}

// MARK: - Codable Test Models

struct CodableTestModel: Codable {
    let id: Int
    let name: String
    let isActive: Bool
    let tags: [String]
}

struct NestedCodableModel: Codable {
    let user: User
    let metadata: Metadata
    
    struct User: Codable {
        let id: Int
        let email: String
    }
    
    struct Metadata: Codable {
        let createdAt: String
        let updatedAt: String
    }
}

final class CodableTests: XCTestCase {
    
    func testEncodeDecodeRoundtrip() throws {
        let model = CodableTestModel(
            id: 1,
            name: "Test",
            isActive: true,
            tags: ["tag1", "tag2"]
        )
        
        let url = URL(string: "https://example.com/api")!
        let request = try HTTPRequest.postJSON(url, body: model)
        
        let decoded = try JSONDecoder().decode(CodableTestModel.self, from: request.body!)
        
        XCTAssertEqual(decoded.id, model.id)
        XCTAssertEqual(decoded.name, model.name)
        XCTAssertEqual(decoded.isActive, model.isActive)
        XCTAssertEqual(decoded.tags, model.tags)
    }
    
    func testNestedModelEncoding() throws {
        let model = NestedCodableModel(
            user: NestedCodableModel.User(id: 1, email: "test@example.com"),
            metadata: NestedCodableModel.Metadata(
                createdAt: "2024-01-01",
                updatedAt: "2024-01-15"
            )
        )
        
        let url = URL(string: "https://example.com/api")!
        let request = try HTTPRequest.postJSON(url, body: model)
        
        let decoded = try JSONDecoder().decode(NestedCodableModel.self, from: request.body!)
        
        XCTAssertEqual(decoded.user.email, "test@example.com")
        XCTAssertEqual(decoded.metadata.createdAt, "2024-01-01")
    }
}
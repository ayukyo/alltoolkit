//
//  HTTPUtilsExamples.swift
//  AllToolkit - HTTP Utilities Usage Examples
//
//  Practical examples demonstrating all features of the HTTP utilities module.
//

import Foundation

// MARK: - Example 1: Basic GET Request

func exampleBasicGET() async {
    print("=== Example 1: Basic GET Request ===")
    
    let client = HTTPClient(baseURL: "https://jsonplaceholder.typicode.com")
    
    do {
        let response = try await client.get("/posts/1")
        
        print("Status: \(response.statusCode)")
        print("Success: \(response.isSuccess)")
        
        if let body = response.string {
            print("Body: \(body)")
        }
    } catch {
        print("Error: \(error)")
    }
}

// MARK: - Example 2: GET with JSON Decoding

struct Post: Decodable {
    let userId: Int
    let id: Int
    let title: String
    let body: String
}

func exampleGETWithDecoding() async {
    print("=== Example 2: GET with JSON Decoding ===")
    
    let client = HTTPClient(baseURL: "https://jsonplaceholder.typicode.com")
    
    do {
        let post: Post = try await client.get("/posts/1")
        print("Post ID: \(post.id)")
        print("Title: \(post.title)")
        print("Author: User \(post.userId)")
    } catch {
        print("Error: \(error)")
    }
}

// MARK: - Example 3: POST Request

struct NewPost: Encodable {
    let title: String
    let body: String
    let userId: Int
}

func examplePOSTRequest() async {
    print("=== Example 3: POST Request ===")
    
    let client = HTTPClient(baseURL: "https://jsonplaceholder.typicode.com")
    let newPost = NewPost(
        title: "My New Post",
        body: "This is the content of my post.",
        userId: 1
    )
    
    do {
        let response = try await client.post("/posts", body: newPost)
        print("Created! Status: \(response.statusCode)")
        
        if let created = response.string {
            print("Response: \(created)")
        }
    } catch {
        print("Error: \(error)")
    }
}

// MARK: - Example 4: PUT Request to Update

struct UpdatePost: Encodable {
    let id: Int
    let title: String
    let body: String
    let userId: Int
}

func examplePUTRequest() async {
    print("=== Example 4: PUT Request ===")
    
    let client = HTTPClient(baseURL: "https://jsonplaceholder.typicode.com")
    let update = UpdatePost(
        id: 1,
        title: "Updated Title",
        body: "Updated content",
        userId: 1
    )
    
    do {
        let response = try await client.put("/posts/1", body: update)
        print("Updated! Status: \(response.statusCode)")
    } catch {
        print("Error: \(error)")
    }
}

// MARK: - Example 5: DELETE Request

func exampleDELETERequest() async {
    print("=== Example 5: DELETE Request ===")
    
    let client = HTTPClient(baseURL: "https://jsonplaceholder.typicode.com")
    
    do {
        let response = try await client.delete("/posts/1")
        print("Deleted! Status: \(response.statusCode)")
    } catch {
        print("Error: \(error)")
    }
}

// MARK: - Example 6: Bearer Token Authentication

func exampleBearerAuth() async {
    print("=== Example 6: Bearer Token Authentication ===")
    
    let client = HTTPClient(baseURL: "https://api.example.com")
    let token = "your-jwt-token-here"
    
    var request = HTTPRequest.get(
        URL(string: "https://api.example.com/protected")!,
        headers: [HTTPHeader.accept: ContentType.json]
    )
    request.bearerAuth(token)
    
    do {
        let response = try await client.request(request)
        print("Status: \(response.statusCode)")
    } catch {
        print("Error: \(error)")
    }
}

// MARK: - Example 7: Basic Authentication

func exampleBasicAuth() async {
    print("=== Example 7: Basic Authentication ===")
    
    let client = HTTPClient()
    
    var request = HTTPRequest.get(URL(string: "https://api.example.com/login")!)
    request.basicAuth(username: "myuser", password: "mypassword")
    
    do {
        let response = try await client.request(request)
        print("Status: \(response.statusCode)")
    } catch {
        print("Error: \(error)")
    }
}

// MARK: - Example 8: Custom Headers

func exampleCustomHeaders() async {
    print("=== Example 8: Custom Headers ===")
    
    let client = HTTPClient(
        baseURL: "https://api.example.com",
        defaultHeaders: [
            HTTPHeader.userAgent: "MyApp/1.0",
            HTTPHeader.accept: ContentType.json
        ]
    )
    
    do {
        let response = try await client.get(
            "/users",
            headers: ["X-Custom-Header": "custom-value"]
        )
        print("Status: \(response.statusCode)")
    } catch {
        print("Error: \(error)")
    }
}

// MARK: - Example 9: URL Builder for Query Parameters

func exampleURLBuilder() {
    print("=== Example 9: URL Builder ===")
    
    var builder = URLBuilder(string: "https://api.example.com/search")!
    
    builder.addQueryItems([
        "q": "swift programming",
        "page": "1",
        "limit": "20",
        "sort": "relevance"
    ])
    
    builder.addQueryItem(name: "filter", value: "active")
    
    if let url = builder.build() {
        print("Built URL: \(url.absoluteString)")
    }
}

// MARK: - Example 10: Form URL-Encoding

func exampleFormEncoding() async {
    print("=== Example 10: Form URL-Encoding ===")
    
    let formData = FormEncoder.formData([
        "username": "john_doe",
        "password": "secret123",
        "remember_me": "true"
    ])
    
    let client = HTTPClient()
    
    var request = HTTPRequest(
        url: URL(string: "https://api.example.com/login")!,
        method: .post,
        headers: [HTTPHeader.contentType: ContentType.formUrlEncoded],
        body: formData
    )
    
    do {
        let response = try await client.request(request)
        print("Login Status: \(response.statusCode)")
    } catch {
        print("Error: \(error)")
    }
}

// MARK: - Example 11: Multipart Form Data (File Upload)

func exampleMultipartUpload() async {
    print("=== Example 11: Multipart File Upload ===")
    
    var multipart = MultipartFormData()
    
    // Add text fields
    multipart.addField(name: "title", value: "My Document")
    multipart.addField(name: "description", value: "Important file upload")
    
    // Add file
    let fileContent = "This is the file content.".data(using: .utf8)!
    multipart.addFile(
        name: "document",
        filename: "document.txt",
        mimeType: "text/plain",
        data: fileContent
    )
    
    let body = multipart.build()
    
    let client = HTTPClient()
    var request = HTTPRequest(
        url: URL(string: "https://api.example.com/upload")!,
        method: .post,
        headers: [HTTPHeader.contentType: multipart.contentType],
        body: body
    )
    
    do {
        let response = try await client.request(request)
        print("Upload Status: \(response.statusCode)")
    } catch {
        print("Error: \(error)")
    }
}

// MARK: - Example 12: Error Handling

func exampleErrorHandling() async {
    print("=== Example 12: Error Handling ===")
    
    let client = HTTPClient(baseURL: "https://api.example.com")
    
    do {
        let response = try await client.get("/nonexistent")
        
        if response.isClientError {
            print("Client error: \(response.statusCode)")
        } else if response.isServerError {
            print("Server error: \(response.statusCode)")
        }
        
    } catch let error as HTTPError {
        switch error {
        case .invalidURL(let url):
            print("Invalid URL: \(url)")
        case .timeout:
            print("Request timed out")
        case .networkError(let underlying):
            print("Network error: \(underlying.localizedDescription)")
        case .httpError(let statusCode, let message):
            print("HTTP \(statusCode): \(message ?? "Unknown error")")
        case .noData:
            print("No data in response")
        case .decodingError(let decodeError):
            print("Decoding error: \(decodeError.localizedDescription)")
        case .invalidResponse:
            print("Invalid server response")
        case .cancelled:
            print("Request was cancelled")
        }
    } catch {
        print("Unexpected error: \(error)")
    }
}

// MARK: - Example 13: Response Status Checking

func exampleStatusChecking() async {
    print("=== Example 13: Response Status Checking ===")
    
    let client = HTTPClient(baseURL: "https://jsonplaceholder.typicode.com")
    
    do {
        let response = try await client.get("/posts/1")
        
        print("Status Code: \(response.statusCode)")
        print("Is Success (2xx): \(response.isSuccess)")
        print("Is Redirect (3xx): \(response.isRedirect)")
        print("Is Client Error (4xx): \(response.isClientError)")
        print("Is Server Error (5xx): \(response.isServerError)")
        
    } catch {
        print("Error: \(error)")
    }
}

// MARK: - Example 14: Download Data

func exampleDownload() async {
    print("=== Example 14: Download Data ===")
    
    let client = HTTPClient()
    
    do {
        let data = try await client.download("https://httpbin.org/bytes/1024")
        print("Downloaded \(data.count) bytes")
    } catch {
        print("Error: \(error)")
    }
}

// MARK: - Example 15: Custom Timeout

func exampleCustomTimeout() async {
    print("=== Example 15: Custom Timeout ===")
    
    let client = HTTPClient()
    
    // Request with 60 second timeout
    var request = HTTPRequest.get(URL(string: "https://api.example.com/slow-endpoint")!)
    request.timeout = 60.0
    
    do {
        let response = try await client.request(request)
        print("Status: \(response.statusCode)")
    } catch {
        print("Error: \(error)")
    }
}

// MARK: - Example 16: Multiple Requests with Shared Client

func exampleMultipleRequests() async {
    print("=== Example 16: Multiple Requests with Shared Client ===")
    
    let client = HTTPClient(
        baseURL: "https://jsonplaceholder.typicode.com",
        defaultHeaders: [HTTPHeader.accept: ContentType.json]
    )
    
    do {
        // Fetch multiple posts concurrently
        async let post1: Post = client.get("/posts/1")
        async let post2: Post = client.get("/posts/2")
        async let post3: Post = client.get("/posts/3")
        
        let results = try await (post1, post2, post3)
        
        print("Post 1: \(results.0.title)")
        print("Post 2: \(results.1.title)")
        print("Post 3: \(results.2.title)")
        
    } catch {
        print("Error: \(error)")
    }
}

// MARK: - Example 17: PATCH Request for Partial Update

struct PartialUpdate: Encodable {
    let title: String?
    let body: String?
    
    init(title: String? = nil, body: String? = nil) {
        self.title = title
        self.body = body
    }
}

func examplePATCHRequest() async {
    print("=== Example 17: PATCH Request ===")
    
    let client = HTTPClient(baseURL: "https://jsonplaceholder.typicode.com")
    let update = PartialUpdate(title: "Only updating the title")
    
    do {
        let response = try await client.patch("/posts/1", body: update)
        print("Patched! Status: \(response.statusCode)")
    } catch {
        print("Error: \(error)")
    }
}

// MARK: - Example 18: Complex Nested JSON

struct UserProfile: Decodable {
    let id: Int
    let username: String
    let profile: Profile
    let settings: Settings
    
    struct Profile: Decodable {
        let firstName: String
        let lastName: String
        let avatar: String?
    }
    
    struct Settings: Decodable {
        let notifications: Bool
        let theme: String
        let language: String
    }
}

func exampleNestedJSON() async {
    print("=== Example 18: Complex Nested JSON ===")
    
    // Note: This would work with an API that returns nested JSON
    // Using a mock response for demonstration
    
    let json = """
    {
        "id": 1,
        "username": "johndoe",
        "profile": {
            "firstName": "John",
            "lastName": "Doe",
            "avatar": "https://example.com/avatar.jpg"
        },
        "settings": {
            "notifications": true,
            "theme": "dark",
            "language": "en"
        }
    }
    """.data(using: .utf8)!
    
    do {
        let user = try JSONDecoder().decode(UserProfile.self, from: json)
        print("User: \(user.username)")
        print("Name: \(user.profile.firstName) \(user.profile.lastName)")
        print("Theme: \(user.settings.theme)")
    } catch {
        print("Decoding error: \(error)")
    }
}

// MARK: - Main Entry Point

@main
struct HTTPExamples {
    static func main() async {
        print("HTTP Utilities Examples")
        print("=======================\n")
        
        await exampleBasicGET()
        print("\n---\n")
        
        await exampleGETWithDecoding()
        print("\n---\n")
        
        await examplePOSTRequest()
        print("\n---\n")
        
        exampleURLBuilder()
        print("\n---\n")
        
        await exampleErrorHandling()
        print("\n---\n")
        
        await exampleStatusChecking()
        print("\n---\n")
        
        await exampleMultipleRequests()
        
        print("\n=== All examples completed ===")
    }
}
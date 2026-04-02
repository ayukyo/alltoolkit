import http_utils.mod;
import http_utils.mod.HttpResponse;

import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

/**
 * HTTP 工具模块使用示例
 *
 * 编译和运行:
 * javac -cp . http_utils/mod.java examples/http_utils_example.java
 * java -cp . examples.http_utils_example
 */
public class http_utils_example {

    public static void main(String[] args) {
        System.out.println("=== HTTP Utils Example ===\n");

        // 1. URL 编码解码示例
        demoUrlEncoding();

        // 2. 构建查询字符串示例
        demoQueryString();

        // 3. 模拟 HTTP 请求（实际网络请求需要可用网络）
        // 取消注释以下行以测试实际网络请求
        // demoHttpRequests();

        System.out.println("\n=== Example Completed ===");
    }

    /**
     * URL 编码解码演示
     */
    private static void demoUrlEncoding() {
        System.out.println("1. URL Encoding/Decoding Demo");
        System.out.println("------------------------------");

        String original = "hello world@example.com 中文测试";
        String encoded = mod.urlEncode(original);
        String decoded = mod.urlDecode(encoded);

        System.out.println("Original: " + original);
        System.out.println("Encoded:  " + encoded);
        System.out.println("Decoded:  " + decoded);
        System.out.println("Match: " + original.equals(decoded));
        System.out.println();
    }

    /**
     * 查询字符串构建演示
     */
    private static void demoQueryString() {
        System.out.println("2. Query String Building Demo");
        System.out.println("------------------------------");

        // 构建查询字符串
        Map<String, String> params = new HashMap<>();
        params.put("name", "张三");
        params.put("age", "25");
        params.put("city", "Beijing Shanghai");

        String queryString = mod.buildQueryString(params);
        System.out.println("Query String: " + queryString);

        // 构建完整 URL
        String baseUrl = "https://api.example.com/users";
        String fullUrl = mod.buildUrl(baseUrl, params);
        System.out.println("Full URL: " + fullUrl);

        // 向已有查询参数的 URL 添加参数
        String existingUrl = "https://api.example.com/search?q=java";
        Map<String, String> extraParams = new HashMap<>();
        extraParams.put("page", "1");
        extraParams.put("limit", "20");
        String appendedUrl = mod.buildUrl(existingUrl, extraParams);
        System.out.println("Appended URL: " + appendedUrl);
        System.out.println();
    }

    /**
     * HTTP 请求演示（需要网络连接）
     */
    private static void demoHttpRequests() {
        System.out.println("3. HTTP Requests Demo");
        System.out.println("----------------------");

        // GET 请求示例
        try {
            System.out.println("\n--- GET Request ---");
            HttpResponse getResp = mod.get("https://httpbin.org/get");
            System.out.println("Status: " + getResp.statusCode);
            System.out.println("Success: " + getResp.isSuccess());
            System.out.println("Body preview: " + getResp.body.substring(0, Math.min(200, getResp.body.length())) + "...");
        } catch (IOException e) {
            System.out.println("GET request failed: " + e.getMessage());
        }

        // 带请求头的 GET 请求
        try {
            System.out.println("\n--- GET with Headers ---");
            Map<String, String> headers = new HashMap<>();
            headers.put("Accept", "application/json");
            headers.put("X-Custom-Header", "MyValue");

            HttpResponse getResp = mod.get("https://httpbin.org/headers", headers);
            System.out.println("Status: " + getResp.statusCode);
            System.out.println("Body preview: " + getResp.body.substring(0, Math.min(200, getResp.body.length())) + "...");
        } catch (IOException e) {
            System.out.println("GET with headers failed: " + e.getMessage());
        }

        // POST JSON 请求
        try {
            System.out.println("\n--- POST JSON ---");
            String jsonBody = "{\"name\":\"张三\",\"age\":25,\"email\":\"zhangsan@example.com\"}";

            HttpResponse postResp = mod.postJson("https://httpbin.org/post", jsonBody);
            System.out.println("Status: " + postResp.statusCode);
            System.out.println("Success: " + postResp.isSuccess());
            System.out.println("Body preview: " + postResp.body.substring(0, Math.min(200, postResp.body.length())) + "...");
        } catch (IOException e) {
            System.out.println("POST JSON request failed: " + e.getMessage());
        }

        // POST 表单请求
        try {
            System.out.println("\n--- POST Form ---");
            Map<String, String> formData = new HashMap<>();
            formData.put("username", "admin");
            formData.put("password", "secret123");

            HttpResponse postResp = mod.postForm("https://httpbin.org/post", formData);
            System.out.println("Status: " + postResp.statusCode);
            System.out.println("Success: " + postResp.isSuccess());
        } catch (IOException e) {
            System.out.println("POST Form request failed: " + e.getMessage());
        }

        // PUT 请求
        try {
            System.out.println("\n--- PUT JSON ---");
            String jsonBody = "{\"id\":1,\"name\":\"Updated Name\"}";

            HttpResponse putResp = mod.putJson("https://httpbin.org/put", jsonBody);
            System.out.println("Status: " + putResp.statusCode);
            System.out.println("Success: " + putResp.isSuccess());
        } catch (IOException e) {
            System.out.println("PUT request failed: " + e.getMessage());
        }

        // DELETE 请求
        try {
            System.out.println("\n--- DELETE ---");
            HttpResponse delResp = mod.delete("https://httpbin.org/delete");
            System.out.println("Status: " + delResp.statusCode);
            System.out.println("Success: " + delResp.isSuccess());
        } catch (IOException e) {
            System.out.println("DELETE request failed: " + e.getMessage());
        }

        // 带自定义超时的请求
        try {
            System.out.println("\n--- Custom Timeout ---");
            HttpResponse resp = mod.get("https://httpbin.org/delay/1", null, 5000, 5000);
            System.out.println("Status: " + resp.statusCode);
            System.out.println("Success: " + resp.isSuccess());
        } catch (IOException e) {
            System.out.println("Custom timeout request failed: " + e.getMessage());
        }
    }
}

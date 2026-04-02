package http_utils;

import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

/**
 * HTTP 工具模块单元测试
 *
 * 运行方式:
 * javac -cp . http_utils/mod.java http_utils/http_utils_test.java
 * java -cp . http_utils.http_utils_test
 */
public class http_utils_test {

    private static int passed = 0;
    private static int failed = 0;

    public static void main(String[] args) {
        System.out.println("=== HTTP Utils Test Suite ===\n");

        testUrlEncode();
        testUrlDecode();
        testBuildQueryString();
        testBuildUrl();
        testHttpResponse();

        // 网络测试（可选，需要网络连接）
        // testHttpGet();

        System.out.println("\n=== Test Summary ===");
        System.out.println("Passed: " + passed);
        System.out.println("Failed: " + failed);
        System.out.println("Total: " + (passed + failed));

        if (failed > 0) {
            System.exit(1);
        }
    }

    private static void testUrlEncode() {
        System.out.println("Testing urlEncode...");

        // 基本编码
        assertEquals("hello%20world", mod.urlEncode("hello world"), "URL encode space");
        assertEquals("test%40example.com", mod.urlEncode("test@example.com"), "URL encode @");
        assertEquals("100%25", mod.urlEncode("100%"), "URL encode %");

        // 中文编码
        assertEquals("%E4%B8%AD%E6%96%87", mod.urlEncode("中文"), "URL encode Chinese");

        // null 处理
        assertEquals("", mod.urlEncode(null), "URL encode null");

        // 空字符串
        assertEquals("", mod.urlEncode(""), "URL encode empty");

        System.out.println("  urlEncode tests completed.\n");
    }

    private static void testUrlDecode() {
        System.out.println("Testing urlDecode...");

        // 基本解码
        assertEquals("hello world", mod.urlDecode("hello%20world"), "URL decode space");
        assertEquals("test@example.com", mod.urlDecode("test%40example.com"), "URL decode @");
        assertEquals("100%", mod.urlDecode("100%25"), "URL decode %");

        // 中文解码
        assertEquals("中文", mod.urlDecode("%E4%B8%AD%E6%96%87"), "URL decode Chinese");

        // null 处理
        assertEquals("", mod.urlDecode(null), "URL decode null");

        // 空字符串
        assertEquals("", mod.urlDecode(""), "URL decode empty");

        System.out.println("  urlDecode tests completed.\n");
    }

    private static void testBuildQueryString() {
        System.out.println("Testing buildQueryString...");

        // 空参数
        Map<String, String> empty = new HashMap<>();
        assertEquals("", mod.buildQueryString(empty), "Empty params");
        assertEquals("", mod.buildQueryString(null), "Null params");

        // 单个参数
        Map<String, String> single = new HashMap<>();
        single.put("key", "value");
        assertEquals("key=value", mod.buildQueryString(single), "Single param");

        // 多个参数
        Map<String, String> multi = new HashMap<>();
        multi.put("a", "1");
        multi.put("b", "2");
        String result = mod.buildQueryString(multi);
        assertTrue(result.contains("a=1") && result.contains("b=2"), "Multiple params");

        // 需要编码的参数
        Map<String, String> encoded = new HashMap<>();
        encoded.put("name", "张三");
        encoded.put("msg", "hello world");
        result = mod.buildQueryString(encoded);
        assertTrue(result.contains("hello%20world"), "Encoded space in value");

        System.out.println("  buildQueryString tests completed.\n");
    }

    private static void testBuildUrl() {
        System.out.println("Testing buildUrl...");

        // 无参数
        assertEquals("https://example.com/api", mod.buildUrl("https://example.com/api", null), "No params");

        // 添加参数
        Map<String, String> params = new HashMap<>();
        params.put("page", "1");
        params.put("size", "10");
        String url = mod.buildUrl("https://example.com/api", params);
        assertTrue(url.startsWith("https://example.com/api?"), "URL with params starts correctly");
        assertTrue(url.contains("page=1"), "URL contains page param");
        assertTrue(url.contains("size=10"), "URL contains size param");

        // 已有查询参数的 URL
        Map<String, String> extra = new HashMap<>();
        extra.put("sort", "desc");
        String url2 = mod.buildUrl("https://example.com/api?filter=active", extra);
        assertTrue(url2.contains("?filter=active&"), "URL appends to existing params");

        System.out.println("  buildUrl tests completed.\n");
    }

    private static void testHttpResponse() {
        System.out.println("Testing HttpResponse...");

        // 成功响应
        mod.HttpResponse success = new mod.HttpResponse(200, "OK", new HashMap<>());
        assertTrue(success.isSuccess(), "200 is success");
        assertEquals(200, success.statusCode, "Status code 200");
        assertEquals("OK", success.body, "Body OK");

        // 失败响应
        mod.HttpResponse notFound = new mod.HttpResponse(404, "Not Found", new HashMap<>());
        assertTrue(!notFound.isSuccess(), "404 is not success");

        // 边界值
        mod.HttpResponse created = new mod.HttpResponse(201, "Created", new HashMap<>());
        assertTrue(created.isSuccess(), "201 is success");

        mod.HttpResponse redirect = new mod.HttpResponse(301, "Redirect", new HashMap<>());
        assertTrue(!redirect.isSuccess(), "301 is not success");

        System.out.println("  HttpResponse tests completed.\n");
    }

    private static void testHttpGet() {
        System.out.println("Testing HTTP GET (requires network)...");

        try {
            // 测试 httpbin.org
            mod.HttpResponse resp = mod.get("https://httpbin.org/get");
            assertTrue(resp.isSuccess(), "GET request success");
            assertTrue(resp.body.contains("origin"), "Response contains expected content");
            System.out.println("  GET test passed.\n");
        } catch (IOException e) {
            System.out.println("  GET test skipped (network unavailable): " + e.getMessage() + "\n");
        }
    }

    // ============ 断言辅助方法 ============

    private static void assertEquals(Object expected, Object actual, String testName) {
        if ((expected == null && actual == null) ||
            (expected != null && expected.equals(actual))) {
            passed++;
            System.out.println("  [PASS] " + testName);
        } else {
            failed++;
            System.out.println("  [FAIL] " + testName + ": expected '" + expected + "' but got '" + actual + "'");
        }
    }

    private static void assertTrue(boolean condition, String testName) {
        if (condition) {
            passed++;
            System.out.println("  [PASS] " + testName);
        } else {
            failed++;
            System.out.println("  [FAIL] " + testName);
        }
    }
}

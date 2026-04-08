package http_utils;

import java.io.*;
import java.net.*;
import java.nio.charset.StandardCharsets;
import java.util.Map;
import java.util.HashMap;
import java.util.List;

/**
 * HTTP 请求工具类
 * 提供简洁的 HTTP GET/POST/PUT/DELETE 请求方法
 * 零第三方依赖，仅使用 Java 标准库
 *
 * @author AllToolkit
 * @version 1.0.0
 */
public class mod {

    /**
     * 默认连接超时时间（毫秒）
     */
    private static final int DEFAULT_CONNECT_TIMEOUT = 10000;

    /**
     * 默认读取超时时间（毫秒）
     */
    private static final int DEFAULT_READ_TIMEOUT = 30000;

    /**
     * HTTP 响应结果类
     */
    public static class HttpResponse {
        /** HTTP 状态码 */
        public final int statusCode;
        /** 响应体内容 */
        public final String body;
        /** 响应头 */
        public final Map<String, List<String>> headers;

        public HttpResponse(int statusCode, String body, Map<String, List<String>> headers) {
            this.statusCode = statusCode;
            this.body = body;
            this.headers = headers;
        }

        /**
         * 检查请求是否成功（2xx 状态码）
         * @return true 如果状态码在 200-299 范围内
         */
        public boolean isSuccess() {
            return statusCode >= 200 && statusCode < 300;
        }

        @Override
        public String toString() {
            return "HttpResponse{statusCode=" + statusCode + ", body='" + body + "'}";
        }
    }

    /**
     * 发送 GET 请求
     *
     * @param url 请求 URL
     * @return HttpResponse 响应对象
     * @throws IOException 当网络请求失败时抛出
     *
     * 示例:
     * <pre>
     * HttpResponse resp = mod.get("https://api.example.com/users");
     * System.out.println(resp.body);
     * </pre>
     */
    public static HttpResponse get(String url) throws IOException {
        return get(url, null, DEFAULT_CONNECT_TIMEOUT, DEFAULT_READ_TIMEOUT);
    }

    /**
     * 发送带请求头的 GET 请求
     *
     * @param url 请求 URL
     * @param headers 请求头 Map
     * @return HttpResponse 响应对象
     * @throws IOException 当网络请求失败时抛出
     */
    public static HttpResponse get(String url, Map<String, String> headers) throws IOException {
        return get(url, headers, DEFAULT_CONNECT_TIMEOUT, DEFAULT_READ_TIMEOUT);
    }

    /**
     * 发送带超时设置的 GET 请求
     *
     * @param url 请求 URL
     * @param headers 请求头 Map（可为 null）
     * @param connectTimeout 连接超时（毫秒）
     * @param readTimeout 读取超时（毫秒）
     * @return HttpResponse 响应对象
     * @throws IOException 当网络请求失败时抛出
     */
    public static HttpResponse get(String url, Map<String, String> headers,
                                    int connectTimeout, int readTimeout) throws IOException {
        HttpURLConnection conn = null;
        try {
            conn = createConnection(url, "GET", headers, connectTimeout, readTimeout);
            return readResponse(conn);
        } finally {
            if (conn != null) {
                conn.disconnect();
            }
        }
    }

    /**
     * 发送 POST 请求（表单数据）
     *
     * @param url 请求 URL
     * @param formData 表单数据 Map
     * @return HttpResponse 响应对象
     * @throws IOException 当网络请求失败时抛出
     *
     * 示例:
     * <pre>
     * Map&lt;String, String&gt; data = new HashMap&lt;&gt;();
     * data.put("username", "admin");
     * data.put("password", "123456");
     * HttpResponse resp = mod.postForm("https://api.example.com/login", data);
     * </pre>
     */
    public static HttpResponse postForm(String url, Map<String, String> formData) throws IOException {
        return postForm(url, formData, null);
    }

    /**
     * 发送带请求头的 POST 请求（表单数据）
     *
     * @param url 请求 URL
     * @param formData 表单数据 Map
     * @param headers 请求头 Map
     * @return HttpResponse 响应对象
     * @throws IOException 当网络请求失败时抛出
     */
    public static HttpResponse postForm(String url, Map<String, String> formData,
                                         Map<String, String> headers) throws IOException {
        String body = buildFormData(formData);
        Map<String, String> finalHeaders = headers != null ? new HashMap<>(headers) : new HashMap<>();
        finalHeaders.put("Content-Type", "application/x-www-form-urlencoded");
        return post(url, body, finalHeaders);
    }

    /**
     * 发送 POST 请求（JSON 数据）
     *
     * @param url 请求 URL
     * @param jsonBody JSON 字符串
     * @return HttpResponse 响应对象
     * @throws IOException 当网络请求失败时抛出
     *
     * 示例:
     * <pre>
     * String json = "{\"name\":\"张三\",\"age\":25}";
     * HttpResponse resp = mod.postJson("https://api.example.com/users", json);
     * </pre>
     */
    public static HttpResponse postJson(String url, String jsonBody) throws IOException {
        return postJson(url, jsonBody, null);
    }

    /**
     * 发送带请求头的 POST 请求（JSON 数据）
     *
     * @param url 请求 URL
     * @param jsonBody JSON 字符串
     * @param headers 请求头 Map
     * @return HttpResponse 响应对象
     * @throws IOException 当网络请求失败时抛出
     */
    public static HttpResponse postJson(String url, String jsonBody,
                                         Map<String, String> headers) throws IOException {
        Map<String, String> finalHeaders = headers != null ? new HashMap<>(headers) : new HashMap<>();
        finalHeaders.put("Content-Type", "application/json; charset=UTF-8");
        return post(url, jsonBody, finalHeaders);
    }

    /**
     * 发送 POST 请求
     *
     * @param url 请求 URL
     * @param body 请求体字符串
     * @param headers 请求头 Map
     * @return HttpResponse 响应对象
     * @throws IOException 当网络请求失败时抛出
     */
    public static HttpResponse post(String url, String body,
                                     Map<String, String> headers) throws IOException {
        return post(url, body, headers, DEFAULT_CONNECT_TIMEOUT, DEFAULT_READ_TIMEOUT);
    }

    /**
     * 发送带超时设置的 POST 请求
     *
     * @param url 请求 URL
     * @param body 请求体字符串
     * @param headers 请求头 Map
     * @param connectTimeout 连接超时（毫秒）
     * @param readTimeout 读取超时（毫秒）
     * @return HttpResponse 响应对象
     * @throws IOException 当网络请求失败时抛出
     */
    public static HttpResponse post(String url, String body,
                                     Map<String, String> headers,
                                     int connectTimeout, int readTimeout) throws IOException {
        HttpURLConnection conn = null;
        try {
            conn = createConnection(url, "POST", headers, connectTimeout, readTimeout);

            // 发送请求体
            if (body != null && !body.isEmpty()) {
                conn.setDoOutput(true);
                try (OutputStream os = conn.getOutputStream()) {
                    os.write(body.getBytes(StandardCharsets.UTF_8));
                }
            }

            return readResponse(conn);
        } finally {
            if (conn != null) {
                conn.disconnect();
            }
        }
    }

    /**
     * 发送 PUT 请求（JSON 数据）
     *
     * @param url 请求 URL
     * @param jsonBody JSON 字符串
     * @return HttpResponse 响应对象
     * @throws IOException 当网络请求失败时抛出
     */
    public static HttpResponse putJson(String url, String jsonBody) throws IOException {
        return putJson(url, jsonBody, null);
    }

    /**
     * 发送带请求头的 PUT 请求（JSON 数据）
     *
     * @param url 请求 URL
     * @param jsonBody JSON 字符串
     * @param headers 请求头 Map
     * @return HttpResponse 响应对象
     * @throws IOException 当网络请求失败时抛出
     */
    public static HttpResponse putJson(String url, String jsonBody,
                                        Map<String, String> headers) throws IOException {
        Map<String, String> finalHeaders = headers != null ? new HashMap<>(headers) : new HashMap<>();
        finalHeaders.put("Content-Type", "application/json; charset=UTF-8");
        return put(url, jsonBody, finalHeaders);
    }

    /**
     * 发送 PUT 请求
     *
     * @param     * @param url 请求 URL
     * @param body 请求体字符串
     * @param headers 请求头 Map
     * @return HttpResponse 响应对象
     * @throws IOException 当网络请求失败时抛出
     */
    public static HttpResponse put(String url, String body,
                                    Map<String, String> headers) throws IOException {
        return put(url, body, headers, DEFAULT_CONNECT_TIMEOUT, DEFAULT_READ_TIMEOUT);
    }

    /**
     * 发送带超时设置的 PUT 请求
     *
     * @param url 请求 URL
     * @param body 请求体字符串
     * @param headers 请求头 Map
     * @param connectTimeout 连接超时（毫秒）
     * @param readTimeout 读取超时（毫秒）
     * @return HttpResponse 响应对象
     * @throws IOException 当网络请求失败时抛出
     */
    public static HttpResponse put(String url, String body,
                                    Map<String, String> headers,
                                    int connectTimeout, int readTimeout) throws IOException {
        HttpURLConnection conn = null;
        try {
            conn = createConnection(url, "PUT", headers, connectTimeout, readTimeout);

            if (body != null && !body.isEmpty()) {
                conn.setDoOutput(true);
                try (OutputStream os = conn.getOutputStream()) {
                    os.write(body.getBytes(StandardCharsets.UTF_8));
                }
            }

            return readResponse(conn);
        } finally {
            if (conn != null) {
                conn.disconnect();
            }
        }
    }

    /**
     * 发送 DELETE 请求
     *
     * @param url 请求 URL
     * @return HttpResponse 响应对象
     * @throws IOException 当网络请求失败时抛出
     */
    public static HttpResponse delete(String url) throws IOException {
        return delete(url, null);
    }

    /**
     * 发送带请求头的 DELETE 请求
     *
     * @param url 请求 URL
     * @param headers 请求头 Map
     * @return HttpResponse 响应对象
     * @throws IOException 当网络请求失败时抛出
     */
    public static HttpResponse delete(String url, Map<String, String> headers) throws IOException {
        return delete(url, headers, DEFAULT_CONNECT_TIMEOUT, DEFAULT_READ_TIMEOUT);
    }

    /**
     * 发送带超时设置的 DELETE 请求
     *
     * @param url 请求 URL
     * @param headers 请求头 Map
     * @param connectTimeout 连接超时（毫秒）
     * @param readTimeout 读取超时（毫秒）
     * @return HttpResponse 响应对象
     * @throws IOException 当网络请求失败时抛出
     */
    public static HttpResponse delete(String url, Map<String, String> headers,
                                       int connectTimeout, int readTimeout) throws IOException {
        HttpURLConnection conn = null;
        try {
            conn = createConnection(url, "DELETE", headers, connectTimeout, readTimeout);
            return readResponse(conn);
        } finally {
            if (conn != null) {
                conn.disconnect();
            }
        }
    }

    /**
     * URL 编码
     *
     * @param value 待编码的字符串
     * @return 编码后的字符串
     */
    public static String urlEncode(String value) {
        if (value == null) {
            return "";
        }
        return URLEncoder.encode(value, StandardCharsets.UTF_8);
    }

    /**
     * URL 解码
     *
     * @param value 待解码的字符串
     * @return 解码后的字符串
     */
    public static String urlDecode(String value) {
        if (value == null) {
            return "";
        }
        return URLDecoder.decode(value, StandardCharsets.UTF_8);
    }

    /**
     * 构建 URL 查询字符串
     *
     * @param params 参数 Map
     * @return 查询字符串（如 "key1=value1&amp;key2=value2"）
     */
    public static String buildQueryString(Map<String, String> params) {
        if (params == null || params.isEmpty()) {
            return "";
        }
        StringBuilder sb = new StringBuilder();
        for (Map.Entry<String, String> entry : params.entrySet()) {
            if (sb.length() > 0) {
                sb.append("&");
            }
            sb.append(urlEncode(entry.getKey()));
            sb.append("=");
            sb.append(urlEncode(entry.getValue()));
        }
        return sb.toString();
    }

    /**
     * 构建完整 URL（带查询参数）
     *
     * @param baseUrl 基础 URL
     * @param params 查询参数 Map
     * @return 完整 URL
     */
    public static String buildUrl(String baseUrl, Map<String, String> params) {
        String query = buildQueryString(params);
        if (query.isEmpty()) {
            return baseUrl;
        }
        String separator = baseUrl.contains("?") ? "&" : "?";
        return baseUrl + separator + query;
    }

    // ============ 私有辅助方法 ============

    /**
     * 创建 HTTP 连接
     */
    private static HttpURLConnection createConnection(String url, String method,
                                                       Map<String, String> headers,
                                                       int connectTimeout, int readTimeout) throws IOException {
        URL urlObj = new URL(url);
        HttpURLConnection conn = (HttpURLConnection) urlObj.openConnection();

        conn.setRequestMethod(method);
        conn.setConnectTimeout(connectTimeout);
        conn.setReadTimeout(readTimeout);
        conn.setInstanceFollowRedirects(true);

        // 设置默认请求头
        conn.setRequestProperty("Accept", "*/*");
        conn.setRequestProperty("Accept-Charset", "UTF-8");
        conn.setRequestProperty("User-Agent", "AllToolkit-HTTP/1.0");

        // 设置自定义请求头
        if (headers != null) {
            for (Map.Entry<String, String> entry : headers.entrySet()) {
                conn.setRequestProperty(entry.getKey(), entry.getValue());
            }
        }

        return conn;
    }

    /**
     * 读取响应内容
     */
    private static HttpResponse readResponse(HttpURLConnection conn) throws IOException {
        int statusCode = conn.getResponseCode();

        // 获取响应头
        Map<String, List<String>> headers = new HashMap<>(conn.getHeaderFields());

        // 读取响应体
        InputStream is = null;
        try {
            // 2xx 状态码使用 getInputStream，其他使用 getErrorStream
            if (statusCode >= 200 && statusCode < 300) {
                is = conn.getInputStream();
            } else {
                is = conn.getErrorStream();
            }

            // 如果没有错误流，使用空字符串
            if (is == null) {
                return new HttpResponse(statusCode, "", headers);
            }

            String body = readStream(is);
            return new HttpResponse(statusCode, body, headers);
        } finally {
            if (is != null) {
                try {
                    is.close();
                } catch (IOException ignored) {
                }
            }
        }
    }

    /**
     * 读取输入流为字符串
     * 优化：使用固定大小缓冲区避免频繁字符串拼接，减少内存分配
     */
    private static String readStream(InputStream is) throws IOException {
        // 使用 StringBuilder 预分配合理容量（8KB）
        StringBuilder sb = new StringBuilder(8192);
        char[] buffer = new char[8192];
        
        try (BufferedReader reader = new BufferedReader(
                new InputStreamReader(is, StandardCharsets.UTF_8))) {
            int charsRead;
            while ((charsRead = reader.read(buffer, 0, buffer.length)) != -1) {
                sb.append(buffer, 0, charsRead);
            }
        }
        
        // 去除首尾空白，避免不必要的 trim() 调用
        int len = sb.length();
        if (len == 0) {
            return "";
        }
        
        int start = 0;
        int end = len;
        
        // 手动去除尾部换行符（HTTP 响应常见）
        while (end > start && (sb.charAt(end - 1) == '\n' || sb.charAt(end - 1) == '\r')) {
            end--;
        }
        
        // 去除前导空白
        while (start < end && Character.isWhitespace(sb.charAt(start))) {
            start++;
        }
        
        return (start == 0 && end == len) ? sb.toString() : sb.substring(start, end);
    }

    /**
     * 构建表单数据字符串
     */
    private static String buildFormData(Map<String, String> formData) {
        if (formData == null || formData.isEmpty()) {
            return "";
        }
        return buildQueryString(formData);
    }
}

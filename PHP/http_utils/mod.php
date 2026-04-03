<?php
/**
 * AllToolkit - PHP HTTP Utilities
 *
 * 一个零依赖的 PHP HTTP 请求工具库，支持多种 HTTP 方法、
 * URL 操作、请求头设置、超时控制等功能。
 *
 * @package AllToolkit\PHP\HttpUtils
 * @author AllToolkit Contributors
 * @license MIT
 */

namespace AllToolkit;

/**
 * HTTP 响应类
 * 封装 HTTP 响应的所有信息
 */
class HttpResponse
{
    public int $statusCode;
    public string $statusText;
    public array $headers;
    public string $body;
    public string $url;
    public bool $success;
    public float $responseTime;
    public ?string $error;

    public function __construct(
        int $statusCode,
        string $statusText,
        array $headers,
        string $body,
        string $url,
        float $responseTime,
        ?string $error = null
    ) {
        $this->statusCode = $statusCode;
        $this->statusText = $statusText;
        $this->headers = $headers;
        $this->body = $body;
        $this->url = $url;
        $this->success = $statusCode >= 200 && $statusCode < 300;
        $this->responseTime = $responseTime;
        $this->error = $error;
    }

    public function json(bool $assoc = true): mixed
    {
        $result = json_decode($this->body, $assoc);
        return json_last_error() === JSON_ERROR_NONE ? $result : null;
    }

    public function isJson(): bool
    {
        json_decode($this->body);
        return json_last_error() === JSON_ERROR_NONE;
    }
}

/**
 * HTTP 请求选项类
 */
class HttpOptions
{
    public array $headers = [];
    public int $timeout = 30;
    public bool $followRedirects = true;
    public int $maxRedirects = 10;
    public bool $verifySsl = true;
    public ?string $proxy = null;
    public ?string $username = null;
    public ?string $password = null;
    public array $curlOptions = [];

    public static function fromArray(array $options): self
    {
        $instance = new self();
        foreach ($options as $key => $value) {
            if (property_exists($instance, $key)) {
                $instance->$key = $value;
            }
        }
        return $instance;
    }
}

/**
 * HTTP 工具类
 */
class HttpUtils
{
    private const DEFAULT_USER_AGENT = 'AllToolkit-PHP-HTTP/1.0';

    public static function get(string $url, array|HttpOptions $options = []): HttpResponse
    {
        return self::request('GET', $url, null, $options);
    }

    public static function post(string $url, ?string $body = null, array|HttpOptions $options = []): HttpResponse
    {
        return self::request('POST', $url, $body, $options);
    }

    public static function postJson(string $url, mixed $data, array|HttpOptions $options = []): HttpResponse
    {
        $body = json_encode($data);
        $opts = is_array($options) ? $options : [];
        $opts['headers'] = array_merge($opts['headers'] ?? [], [
            'Content-Type' => 'application/json',
            'Accept' => 'application/json'
        ]);
        return self::post($url, $body, $opts);
    }

    public static function postForm(string $url, array $data, array|HttpOptions $options = []): HttpResponse
    {
        $body = http_build_query($data);
        $opts = is_array($options) ? $options : [];
        $opts['headers'] = array_merge($opts['headers'] ?? [], [
            'Content-Type' => 'application/x-www-form-urlencoded'
        ]);
        return self::post($url, $body, $opts);
    }

    public static function put(string $url, ?string $body = null, array|HttpOptions $options = []): HttpResponse
    {
        return self::request('PUT', $url, $body, $options);
    }

    public static function putJson(string $url, mixed $data, array|HttpOptions $options = []): HttpResponse
    {
        $body = json_encode($data);
        $opts = is_array($options) ? $options : [];
        $opts['headers'] = array_merge($opts['headers'] ?? [], [
            'Content-Type' => 'application/json',
            'Accept' => 'application/json'
        ]);
        return self::put($url, $body, $opts);
    }

    public static function delete(string $url, array|HttpOptions $options = []): HttpResponse
    {
        return self::request('DELETE', $url, null, $options);
    }

    public static function patch(string $url, ?string $body = null, array|HttpOptions $options = []): HttpResponse
    {
        return self::request('PATCH', $url, $body, $options);
    }

    public static function head(string $url, array|HttpOptions $options = []): HttpResponse
    {
        return self::request('HEAD', $url, null, $options);
    }

    public static function buildUrl(string $baseUrl, array $params = []): string
    {
        if (empty($params)) {
            return $baseUrl;
        }
        $query = http_build_query($params);
        $separator = strpos($baseUrl, '?') === false ? '?' : '&';
        return $baseUrl . $separator . $query;
    }

    public static function buildQueryString(array $params): string
    {
        return http_build_query($params);
    }

    public static function urlEncode(string $value): string
    {
        return urlencode($value);
    }

    public static function urlDecode(string $value): string
    {
        return urldecode($value);
    }

    public static function parseUrl(string $url): array
    {
        $parts = parse_url($url);
        if ($parts === false) {
            return [];
        }
        return [
            'scheme' => $parts['scheme'] ?? '',
            'host' => $parts['host'] ?? '',
            'port' => $parts['port'] ?? null,
            'path' => $parts['path'] ?? '',
            'query' => $parts['query'] ?? '',
            'fragment' => $parts['fragment'] ?? '',
            'user' => $parts['user'] ?? '',
            'pass' => $parts['pass'] ?? ''
        ];
    }

    public static function parseQueryString(string $queryString): array
    {
        $result = [];
        parse_str($queryString, $result);
        return $result;
    }

    public static function isValidUrl(string $url): bool
    {
        return filter_var($url, FILTER_VALIDATE_URL) !== false;
    }

    public static function getDomain(string $url): string
    {
        $parts = parse_url($url);
        return $parts['host'] ?? '';
    }

    public static function getPath(string $url): string
    {
        $parts = parse_url($url);
        return $parts['path'] ?? '';
    }

    public static function addQueryParams(string $url, array $params): string
    {
        return self::buildUrl($url, $params);
    }

    public static function removeQueryParams(string $url, array $keys): string
    {
        $parts = parse_url($url);
        if (!isset($parts['query'])) {
            return $url;
        }
        $query = self::parseQueryString($parts['query']);
        foreach ($keys as $key) {
            unset($query[$key]);
        }
        $newQuery = http_build_query($query);
        $result = $parts['scheme'] . '://' . $parts['host'];
        if (isset($parts['port'])) {
            $result .= ':' . $parts['port'];
        }
        $result .= $parts['path'] ?? '';
        if (!empty($newQuery)) {
            $result .= '?' . $newQuery;
        }
        if (isset($parts['fragment'])) {
            $result .= '#' . $parts['fragment'];
        }
        return $result;
    }

    private static function request(string $method, string $url, ?string $body, array|HttpOptions $options): HttpResponse
    {
        $opts = $options instanceof HttpOptions ? $options : HttpOptions::fromArray($options);
        $startTime = microtime(true);

        $ch = curl_init();
        if ($ch === false) {
            return new HttpResponse(0, 'CURL Error', [], '', $url, 0, 'Failed to initialize CURL');
        }

        curl_setopt($ch, CURLOPT_URL, $url);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_HEADER, true);
        curl_setopt($ch, CURLOPT_CUSTOMREQUEST, $method);
        curl_setopt($ch, CURLOPT_TIMEOUT, $opts->timeout);
        curl_setopt($ch, CURLOPT_FOLLOWLOCATION, $opts->followRedirects);
        curl_setopt($ch, CURLOPT_MAXREDIRS, $opts->maxRedirects);
        curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, $opts->verifySsl);
        curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, $opts->verifySsl ? 2 : 0);
        curl_setopt($ch, CURLOPT_USERAGENT, self::DEFAULT_USER_AGENT);

        $headers = [];
        foreach ($opts->headers as $key => $value) {
            $headers[] = "$key: $value";
        }
        if (!empty($headers)) {
            curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
        }

        if ($body !== null) {
            curl_setopt($ch, CURLOPT_POSTFIELDS, $body);
        }

        if ($opts->proxy !== null) {
            curl_setopt($ch, CURLOPT_PROXY, $opts->proxy);
        }

        if ($opts->username !== null && $opts->password !== null) {
            curl_setopt($ch, CURLOPT_USERPWD, $opts->username . ':' . $opts->password);
        }

        foreach ($opts->curlOptions as $opt => $val) {
            curl_setopt($ch, $opt, $val);
        }

        $response = curl_exec($ch);
        $responseTime = microtime(true) - $startTime;

        if ($response === false) {
            $error = curl_error($ch);
            curl_close($ch);
            return new HttpResponse(0, 'CURL Error', [], '', $url, $responseTime, $error);
        }

        $headerSize = curl_getinfo($ch, CURLINFO_HEADER_SIZE);
        $statusCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        curl_close($ch);

        $headerStr = substr($response, 0, $headerSize);
        $body = substr($response, $headerSize);

        $headers = self::parseHeaders($headerStr);
        $statusText = self::getStatusText($statusCode);

        return new HttpResponse($statusCode, $statusText, $headers, $body, $url, $responseTime, null);
    }

    private static function parseHeaders(string $headerStr): array
    {
        $headers = [];
        $lines = explode("\r\n", $headerStr);
        foreach ($lines as $line) {
            if (strpos($line, ':') !== false) {
                [$key, $value] = explode(':', $line, 2);
                $headers[trim($key)] = trim($value);
            }
        }
        return $headers;
    }

    private static function getStatusText(int $code): string
    {
        $statusTexts = [
            100 => 'Continue',
            200 => 'OK',
            201 => 'Created',
            204 => 'No Content',
            301 => 'Moved Permanently',
            302 => 'Found',
            304 => 'Not Modified',
            400 => 'Bad Request',
            401 => 'Unauthorized',
            403 => 'Forbidden',
            404 => 'Not Found',
            405 => 'Method Not Allowed',
            500 => 'Internal Server Error',
            502 => 'Bad Gateway',
            503 => 'Service Unavailable'
        ];
        return $statusTexts[$code] ?? 'Unknown';
    }
}
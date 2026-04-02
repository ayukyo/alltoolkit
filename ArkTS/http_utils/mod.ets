/**
 * HTTP Utilities Module for ArkTS
 * 
 * A comprehensive HTTP client utility for HarmonyOS applications.
 * Provides simplified HTTP request methods with Promise-based API.
 * 
 * @module http_utils
 * @version 1.0.0
 * @author AllToolkit
 */

import http from '@ohos.net.http';

/**
 * HTTP response structure
 */
export interface HttpResponse<T = string> {
  /** HTTP status code */
  statusCode: number;
  /** Response status message */
  statusMessage: string;
  /** Response headers */
  headers: Record<string, string>;
  /** Response body (parsed or raw) */
  body: T;
  /** Request URL */
  url: string;
  /** Whether request was successful (2xx status) */
  success: boolean;
  /** Response time in milliseconds */
  responseTime: number;
}

/**
 * HTTP request options
 */
export interface HttpRequestOptions {
  /** Request headers */
  headers?: Record<string, string>;
  /** Request timeout in milliseconds (default: 30000) */
  timeout?: number;
  /** Whether to parse response as JSON */
  parseJson?: boolean;
  /** Request body content type */
  contentType?: string;
}

/**
 * Default request options
 */
const DEFAULT_OPTIONS: HttpRequestOptions = {
  headers: {},
  timeout: 30000,
  parseJson: false,
  contentType: 'application/json'
};

/**
 * Create an HTTP client instance
 * @returns HTTP client instance
 */
function createHttpClient(): http.HttpRequest {
  return http.createHttp();
}

/**
 * Build URL with query parameters
 * @param baseUrl - Base URL
 * @param params - Query parameters object
 * @returns Complete URL with query string
 * @example
 * ```typescript
 * const url = buildUrl('https://api.example.com/users', { page: 1, limit: 10 });
 * // Result: 'https://api.example.com/users?page=1&limit=10'
 * ```
 */
export function buildUrl(baseUrl: string, params?: Record<string, string | number | boolean>): string {
  if (!params || Object.keys(params).length === 0) {
    return baseUrl;
  }
  
  const queryString = buildQueryString(params);
  const separator = baseUrl.includes('?') ? '&' : '?';
  return `${baseUrl}${separator}${queryString}`;
}

/**
 * Build query string from object
 * @param params - Parameters object
 * @returns URL-encoded query string
 * @example
 * ```typescript
 * const qs = buildQueryString({ name: 'John', age: 30 });
 * // Result: 'name=John&age=30'
 * ```
 */
export function buildQueryString(params: Record<string, string | number | boolean>): string {
  return Object.entries(params)
    .map(([key, value]) => `${encodeURIComponent(key)}=${encodeURIComponent(String(value))}`)
    .join('&');
}

/**
 * URL encode a string
 * @param value - String to encode
 * @returns URL-encoded string
 */
export function urlEncode(value: string): string {
  return encodeURIComponent(value);
}

/**
 * URL decode a string
 * @param value - String to decode
 * @returns URL-decoded string
 */
export function urlDecode(value: string): string {
  return decodeURIComponent(value);
}

/**
 * Send HTTP GET request
 * @param url - Request URL
 * @param options - Request options
 * @returns Promise resolving to HttpResponse
 * @example
 * ```typescript
 * const response = await httpGet('https://api.example.com/users');
 * if (response.success) {
 *   console.info(response.body);
 * }
 * ```
 */
export function httpGet<T = string>(url: string, options?: HttpRequestOptions): Promise<HttpResponse<T>> {
  return request<T>('GET', url, undefined, options);
}

/**
 * Send HTTP POST request
 * @param url - Request URL
 * @param body - Request body
 * @param options - Request options
 * @returns Promise resolving to HttpResponse
 * @example
 * ```typescript
 * const response = await httpPost('https://api.example.com/users', 
 *   JSON.stringify({ name: 'John', age: 30 }));
 * ```
 */
export function httpPost<T = string>(url: string, body?: string, options?: HttpRequestOptions): Promise<HttpResponse<T>> {
  return request<T>('POST', url, body, options);
}

/**
 * Send HTTP POST request with JSON data
 * @param url - Request URL
 * @param data - Data object to send as JSON
 * @param options - Request options
 * @returns Promise resolving to HttpResponse
 * @example
 * ```typescript
 * const response = await httpPostJson('https://api.example.com/users', 
 *   { name: 'John', age: 30 });
 * ```
 */
export function httpPostJson<T = unknown>(url: string, data: unknown, options?: HttpRequestOptions): Promise<HttpResponse<T>> {
  const body = JSON.stringify(data);
  const mergedOptions: HttpRequestOptions = {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options?.headers
    },
    parseJson: true
  };
  return request<T>('POST', url, body, mergedOptions);
}

/**
 * Send HTTP POST request with form data
 * @param url - Request URL
 * @param data - Form data object
 * @param options - Request options
 * @returns Promise resolving to HttpResponse
 * @example
 * ```typescript
 * const response = await httpPostForm('https://api.example.com/login', 
 *   { username: 'admin', password: 'secret' });
 * ```
 */
export function httpPostForm<T = string>(url: string, data: Record<string, string>, options?: HttpRequestOptions): Promise<HttpResponse<T>> {
  const body = buildQueryString(data);
  const mergedOptions: HttpRequestOptions = {
    ...options,
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
      ...options?.headers
    }
  };
  return request<T>('POST', url, body, mergedOptions);
}

/**
 * Send HTTP PUT request
 * @param url - Request URL
 * @param body - Request body
 * @param options - Request options
 * @returns Promise resolving to HttpResponse
 */
export function httpPut<T = string>(url: string, body?: string, options?: HttpRequestOptions): Promise<HttpResponse<T>> {
  return request<T>('PUT', url, body, options);
}

/**
 * Send HTTP PUT request with JSON data
 * @param url - Request URL
 * @param data - Data object to send as JSON
 * @param options - Request options
 * @returns Promise resolving to HttpResponse
 */
export function httpPutJson<T = unknown>(url: string, data: unknown, options?: HttpRequestOptions): Promise<HttpResponse<T>> {
  const body = JSON.stringify(data);
  const mergedOptions: HttpRequestOptions = {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options?.headers
    },
    parseJson: true
  };
  return request<T>('PUT', url, body, mergedOptions);
}

/**
 * Send HTTP DELETE request
 * @param url - Request URL
 * @param options - Request options
 * @returns Promise resolving to HttpResponse
 */
export function httpDelete<T = string>(url: string, options?: HttpRequestOptions): Promise<HttpResponse<T>> {
  return request<T>('DELETE', url, undefined, options);
}

/**
 * Send HTTP PATCH request
 * @param url - Request URL
 * @param body - Request body
 * @param options - Request options
 * @returns Promise resolving to HttpResponse
 */
export function httpPatch<T = string>(url: string, body?: string, options?: HttpRequestOptions): Promise<HttpResponse<T>> {
  return request<T>('PATCH', url, body, options);
}

/**
 * Send HTTP HEAD request
 * @param url - Request URL
 * @param options - Request options
 * @returns Promise resolving to HttpResponse (body will be empty)
 */
export function httpHead<T = string>(url: string, options?: HttpRequestOptions): Promise<HttpResponse<T>> {
  return request<T>('HEAD', url, undefined, options);
}

/**
 * Generic HTTP request function
 * @param method - HTTP method
 * @param url - Request URL
 * @param body - Request body (optional)
 * @param options - Request options
 * @returns Promise resolving to HttpResponse
 */
function request<T>(
  method: string,
  url: string,
  body?: string,
  options?: HttpRequestOptions
): Promise<HttpResponse<T>> {
  const opts = { ...DEFAULT_OPTIONS, ...options };
  const startTime = Date.now();

  return new Promise((resolve, reject) => {
    const client = createHttpClient();
    
    // Set timeout
    if (opts.timeout && opts.timeout > 0) {
      client.setTimeout(opts.timeout);
    }

    // Prepare request options
    const requestOptions: http.RequestOptions = {
      method: method as http.RequestMethod,
      header: opts.headers || {}
    };

    // Add content type header if body exists
    if (body && opts.contentType) {
      requestOptions.header['Content-Type'] = opts.contentType;
    }

    // Send request
    client.request(
      url,
      requestOptions,
      (err: Error, data: http.HttpResponse) => {
        if (err) {
          reject(err);
          return;
        }

        const responseTime = Date.now() - startTime;
        const statusCode = data.responseCode;
        const success = statusCode >= 200 && statusCode < 300;

        // Parse body if JSON is requested
        let parsedBody: T = data.result as T;
        if (opts.parseJson && typeof data.result === 'string') {
          try {
            parsedBody = JSON.parse(data.result) as T;
          } catch {
            parsedBody = data.result as T;
          }
        }

        const response: HttpResponse<T> = {
          statusCode,
          statusMessage: getStatusMessage(statusCode),
          headers: data.header || {},
          body: parsedBody,
          url,
          success,
          responseTime
        };

        resolve(response);
      }
    );
  });
}

/**
 * Get HTTP status message from status code
 * @param code - HTTP status code
 * @returns Status message
 */
function getStatusMessage(code: number): string {
  const messages: Record<number, string> = {
    200: 'OK',
    201: 'Created',
    204: 'No Content',
    301: 'Moved Permanently',
    302: 'Found',
    304: 'Not Modified',
    400: 'Bad Request',
    401: 'Unauthorized',
    403: 'Forbidden',
    404: 'Not Found',
    405: 'Method Not Allowed',
    408: 'Request Timeout',
    409: 'Conflict',
    422: 'Unprocessable Entity',
    429: 'Too Many Requests',
    500: 'Internal Server Error',
    501: 'Not Implemented',
    502: 'Bad Gateway',
    503: 'Service Unavailable',
    504: 'Gateway Timeout'
  };
  return messages[code] || 'Unknown Status';
}

/**
 * Parse URL into components
 * @param url - URL string
 * @returns URL components object
 * @example
 * ```typescript
 * const parts = parseUrl('https://api.example.com:8080/users?id=123');
 * // Returns: { protocol: 'https', host: 'api.example.com', port: '8080', ... }
 * ```
 */
export function parseUrl(url: string): {
  protocol: string;
  host: string;
  port: string;
  pathname: string;
  search: string;
  hash: string;
  hostname: string;
} {
  // Simple URL parsing for HarmonyOS environment
  const protocolMatch = url.match(/^([^:]+):\/\//);
  const protocol = protocolMatch ? protocolMatch[1] : 'http';
  
  const withoutProtocol = url.replace(/^[^:]+:\/\//, '');
  const hashMatch = withoutProtocol.match(/#(.*)$/);
  const hash = hashMatch ? hashMatch[1] : '';
  const withoutHash = withoutProtocol.replace(/#.*$/, '');
  
  const searchMatch = withoutHash.match(/\?(.*)$/);
  const search = searchMatch ? searchMatch[1] : '';
  const withoutSearch = withoutHash.replace(/\?.*$/, '');
  
  const pathMatch = withoutSearch.match(/\/(.+)$/);
  const pathname = pathMatch ? '/' + pathMatch[1] : '/';
  const hostPort = pathMatch ? withoutSearch.substring(0, withoutSearch.length - pathname.length + 1) : withoutSearch;
  
  const portMatch = hostPort.match(/:(\d+)$/);
  const port = portMatch ? portMatch[1] : (protocol === 'https' ? '443' : '80');
  const hostname = portMatch ? hostPort.substring(0, hostPort.length - port.length - 1) : hostPort;
  const host = hostname + (port !== '80' && port !== '443' ? ':' + port : '');

  return {
    protocol,
    host,
    port,
    pathname,
    search,
    hash,
    hostname
  };
}

/**
 * Extract domain from URL
 * @param url - URL string
 * @returns Domain name
 * @example
 * ```typescript
 * const domain = getDomain('https://api.example.com/users');
 * // Returns: 'api.example.com'
 * ```
 */
export function getDomain(url: string): string {
  const parts = parseUrl(url);
  return parts.hostname;
}

/**
 * Extract path from URL
 * @param url - URL string
 * @returns Path
 * @example
 * ```typescript
 * const path = getPath('https://api.example.com/users/123');
 * // Returns: '/users/123'
 * ```
 */
export function getPath(url: string): string {
  const parts = parseUrl(url);
  return parts.pathname;
}

/**
 * Validate if string is a valid URL
 * @param url - URL string to validate
 * @returns True if valid URL
 * @example
 * ```typescript
 * const isValid = isValidUrl('https://example.com');
 * // Returns: true
 * ```
 */
export function isValidUrl(url: string): boolean {
  if (!url || url.length === 0) {
    return false;
  }
  const pattern = /^(https?:\/\/)[\w.-]+(:\d+)?(\/[\w./-]*)?(\?[\w=&-]*)?(#[\w-]*)?$/i;
  return pattern.test(url);
}

/**
 * Parse query string into object
 * @param queryString - Query string (with or without leading ?)
 * @returns Parsed parameters object
 * @example
 * ```typescript
 * const params = parseQueryString('?name=John&age=30');
 * // Returns: { name: 'John', age: '30' }
 * ```
 */
export function parseQueryString(queryString: string): Record<string, string> {
  const result: Record<string, string> = {};
  if (!queryString) {
    return result;
  }
  
  const cleanQuery = queryString.startsWith('?') ? queryString.substring(1) : queryString;
  if (!cleanQuery) {
    return result;
  }
  
  const pairs = cleanQuery.split('&');
  for (const pair of pairs) {
    const [key, value] = pair.split('=');
    if (key) {
      result[urlDecode(key)] = value ? urlDecode(value) : '';
    }
  }
  
  return result;
}

/**
 * Add query parameters to existing URL
 * @param url - Original URL
 * @param params - Parameters to add
 * @returns Updated URL
 * @example
 * ```typescript
 * const newUrl = addQueryParams('https://api.example.com/users', { page: 2 });
 * // Returns: 'https://api.example.com/users?page=2'
 * ```
 */
export function addQueryParams(
  url: string, 
  params: Record<string, string | number | boolean>
): string {
  return buildUrl(url, params);
}

/**
 * Remove query parameters from URL
 * @param url - Original URL
 * @param keys - Keys to remove
 * @returns Updated URL
 * @example
 * ```typescript
 * const newUrl = removeQueryParams('https://api.example.com/users?page=1&sort=desc', ['page']);
 * // Returns: 'https://api.example.com/users?sort=desc'
 * ```
 */
export function removeQueryParams(url: string, keys: string[]): string {
  const parts = parseUrl(url);
  if (!parts.search) {
    return url;
  }
  
  const params = parseQueryString(parts.search);
  for (const key of keys) {
    delete params[key];
  }
  
  const baseUrl = url.split('?')[0];
  const newQuery = buildQueryString(params);
  
  return newQuery ? `${baseUrl}?${newQuery}` : baseUrl;
}

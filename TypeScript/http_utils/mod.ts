/**
 * HTTP Utilities - TypeScript
 * 
 * 一个零依赖的 HTTP 请求工具库，使用 TypeScript 原生 fetch API。
 * 支持 GET、POST、PUT、DELETE、PATCH 等常用 HTTP 方法。
 * 
 * @module http_utils
 * @version 1.0.0
 * @license MIT
 */

/**
 * HTTP 请求选项接口
 */
export interface HttpOptions {
  /** 请求头对象 */
  headers?: Record<string, string>;
  /** 超时时间（毫秒），默认 30000 */
  timeout?: number;
  /** 是否携带凭证（cookies） */
  credentials?: 'omit' | 'same-origin' | 'include';
  /** 请求模式 */
  mode?: 'cors' | 'no-cors' | 'same-origin';
  /** 重定向模式 */
  redirect?: 'follow' | 'error' | 'manual';
}

/**
 * HTTP 响应接口
 */
export interface HttpResponse<T = unknown> {
  /** HTTP 状态码 */
  status: number;
  /** 状态文本 */
  statusText: string;
  /** 响应数据 */
  data: T;
  /** 响应头 */
  headers: Record<string, string>;
  /** 是否成功（状态码 200-299） */
  ok: boolean;
  /** 响应 URL */
  url: string;
}

/**
 * HTTP 错误类
 */
export class HttpError extends Error {
  /** HTTP 状态码 */
  status: number;
  /** 响应数据 */
  data: unknown;
  /** 响应 URL */
  url: string;

  constructor(message: string, status: number, data: unknown, url: string) {
    super(message);
    this.name = 'HttpError';
    this.status = status;
    this.data = data;
    this.url = url;
  }
}

/**
 * 超时错误类
 */
export class TimeoutError extends Error {
  constructor(message: string = 'Request timeout') {
    super(message);
    this.name = 'TimeoutError';
  }
}

/**
 * 构建带查询参数的 URL
 * 
 * @param baseUrl - 基础 URL
 * @param params - 查询参数对象
 * @returns 完整的 URL 字符串
 * 
 * @example
 * ```typescript
 * const url = buildUrl('https://api.example.com/search', { q: 'test', page: 1 });
 * // 返回: 'https://api.example.com/search?q=test&page=1'
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
 * 构建查询参数字符串
 * 
 * @param params - 参数对象
 * @returns URL 编码的查询字符串
 * 
 * @example
 * ```typescript
 * const query = buildQueryString({ name: 'John Doe', age: 25 });
 * // 返回: 'name=John%20Doe&age=25'
 * ```
 */
export function buildQueryString(params: Record<string, string | number | boolean>): string {
  return Object.entries(params)
    .filter(([, value]) => value !== undefined && value !== null)
    .map(([key, value]) => `${encodeURIComponent(key)}=${encodeURIComponent(String(value))}`)
    .join('&');
}

/**
 * URL 编码
 * 
 * @param value - 要编码的字符串
 * @returns 编码后的字符串
 */
export function urlEncode(value: string): string {
  return encodeURIComponent(value);
}

/**
 * URL 解码
 * 
 * @param value - 要解码的字符串
 * @returns 解码后的字符串
 */
export function urlDecode(value: string): string {
  return decodeURIComponent(value);
}

/**
 * 解析响应头为对象
 * 
 * @param headers - Headers 对象
 * @returns 普通对象格式的响应头
 */
function parseHeaders(headers: Headers): Record<string, string> {
  const result: Record<string, string> = {};
  headers.forEach((value, key) => {
    result[key] = value;
  });
  return result;
}

/**
 * 带超时的 fetch 包装器
 * 
 * @param url - 请求 URL
 * @param options - fetch 选项
 * @param timeoutMs - 超时时间（毫秒）
 * @returns Response 对象
 */
async function fetchWithTimeout(
  url: string,
  options: RequestInit,
  timeoutMs: number = 30000
): Promise<Response> {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), timeoutMs);

  try {
    const response = await fetch(url, {
      ...options,
      signal: controller.signal,
    });
    clearTimeout(timeoutId);
    return response;
  } catch (error) {
    clearTimeout(timeoutId);
    if (error instanceof Error && error.name === 'AbortError') {
      throw new TimeoutError(`Request timeout after ${timeoutMs}ms`);
    }
    throw error;
  }
}

/**
 * 处理 HTTP 响应
 * 
 * @param response - fetch Response 对象
 * @returns 标准化的 HttpResponse 对象
 */
async function handleResponse<T>(response: Response): Promise<HttpResponse<T>> {
  const headers = parseHeaders(response.headers);
  let data: T;

  const contentType = headers['content-type'] || '';
  
  if (contentType.includes('application/json')) {
    data = await response.json() as T;
  } else {
    const text = await response.text();
    try {
      // 尝试解析为 JSON
      data = JSON.parse(text) as T;
    } catch {
      // 如果不是 JSON，返回文本
      data = text as unknown as T;
    }
  }

  const result: HttpResponse<T> = {
    status: response.status,
    statusText: response.statusText,
    data,
    headers,
    ok: response.ok,
    url: response.url,
  };

  if (!response.ok) {
    throw new HttpError(
      `HTTP ${response.status}: ${response.statusText}`,
      response.status,
      data,
      response.url
    );
  }

  return result;
}

/**
 * 发送 GET 请求
 * 
 * @param url - 请求 URL
 * @param options - 请求选项
 * @returns HTTP 响应对象
 * 
 * @example
 * ```typescript
 * const response = await get('https://api.example.com/users');
 * console.log(response.data);
 * ```
 */
export async function get<T = unknown>(url: string, options: HttpOptions = {}): Promise<HttpResponse<T>> {
  const response = await fetchWithTimeout(url, {
    method: 'GET',
    headers: options.headers,
    credentials: options.credentials,
    mode: options.mode,
    redirect: options.redirect,
  }, options.timeout);

  return handleResponse<T>(response);
}

/**
 * 发送 POST 请求
 * 
 * @param url - 请求 URL
 * @param body - 请求体
 * @param options - 请求选项
 * @returns HTTP 响应对象
 * 
 * @example
 * ```typescript
 * const response = await post('https://api.example.com/users', { name: 'John', age: 30 });
 * console.log(response.data);
 * ```
 */
export async function post<T = unknown>(
  url: string,
  body: unknown,
  options: HttpOptions = {}
): Promise<HttpResponse<T>> {
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...options.headers,
  };

  const response = await fetchWithTimeout(url, {
    method: 'POST',
    headers,
    body: typeof body === 'string' ? body : JSON.stringify(body),
    credentials: options.credentials,
    mode: options.mode,
    redirect: options.redirect,
  }, options.timeout);

  return handleResponse<T>(response);
}

/**
 * 发送 POST 请求（表单数据）
 * 
 * @param url - 请求 URL
 * @param formData - 表单数据对象
 * @param options - 请求选项
 * @returns HTTP 响应对象
 * 
 * @example
 * ```typescript
 * const response = await postForm('https://api.example.com/login', {
 *   username: 'john',
 *   password: 'secret'
 * });
 * ```
 */
export async function postForm<T = unknown>(
  url: string,
  formData: Record<string, string>,
  options: HttpOptions = {}
): Promise<HttpResponse<T>> {
  const body = buildQueryString(formData);
  const headers: Record<string, string> = {
    'Content-Type': 'application/x-www-form-urlencoded',
    ...options.headers,
  };

  const response = await fetchWithTimeout(url, {
    method: 'POST',
    headers,
    body,
    credentials: options.credentials,
    mode: options.mode,
    redirect: options.redirect,
  }, options.timeout);

  return handleResponse<T>(response);
}

/**
 * 发送 PUT 请求
 * 
 * @param url - 请求 URL
 * @param body - 请求体
 * @param options - 请求选项
 * @returns HTTP 响应对象
 * 
 * @example
 * ```typescript
 * const response = await put('https://api.example.com/users/1', { name: 'Jane' });
 * ```
 */
export async function put<T = unknown>(
  url: string,
  body: unknown,
  options: HttpOptions = {}
): Promise<HttpResponse<T>> {
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...options.headers,
  };

  const response = await fetchWithTimeout(url, {
    method: 'PUT',
    headers,
    body: typeof body === 'string' ? body : JSON.stringify(body),
    credentials: options.credentials,
    mode: options.mode,
    redirect: options.redirect,
  }, options.timeout);

  return handleResponse<T>(response);
}

/**
 * 发送 DELETE 请求
 * 
 * @param url - 请求 URL
 * @param options - 请求选项
 * @returns HTTP 响应对象
 * 
 * @example
 * ```typescript
 * const response = await del('https://api.example.com/users/1');
 * ```
 */
export async function del<T = unknown>(url: string, options: HttpOptions = {}): Promise<HttpResponse<T>> {
  const response = await fetchWithTimeout(url, {
    method: 'DELETE',
    headers: options.headers,
    credentials: options.credentials,
    mode: options.mode,
    redirect: options.redirect,
  }, options.timeout);

  return handleResponse<T>(response);
}

/**
 * 发送 PATCH 请求
 * 
 * @param url - 请求 URL
 * @param body - 请求体
 * @param options - 请求选项
 * @returns HTTP 响应对象
 * 
 * @example
 * ```typescript
 * const response = await patch('https://api.example.com/users/1', { email: 'new@example.com' });
 * ```
 */
export async function patch<T = unknown>(
  url: string,
  body: unknown,
  options: HttpOptions = {}
): Promise<HttpResponse<T>> {
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...options.headers,
  };

  const response = await fetchWithTimeout(url, {
    method: 'PATCH',
    headers,
    body: typeof body === 'string' ? body : JSON.stringify(body),
    credentials: options.credentials,
    mode: options.mode,
    redirect: options.redirect,
  }, options.timeout);

  return handleResponse<T>(response);
}

/**
 * 发送 HEAD 请求
 * 
 * @param url - 请求 URL
 * @param options - 请求选项
 * @returns HTTP 响应对象（无响应体）
 * 
 * @example
 * ```typescript
 * const response = await head('https://api.example.com/users/1');
 * console.log(response.headers['content-length']);
 * ```
 */
export async function head<T = unknown>(url: string, options: HttpOptions = {}): Promise<HttpResponse<T>> {
  const response = await fetchWithTimeout(url, {
    method: 'HEAD',
    headers: options.headers,
    credentials: options.credentials,
    mode: options.mode,
    redirect: options.redirect,
  }, options.timeout);

  const headers = parseHeaders(response.headers);
  
  return {
    status: response.status,
    statusText: response.statusText,
    data: null as unknown as T,
    headers,
    ok: response.ok,
    url: response.url,
  };
}

/**
 * 创建 HTTP 客户端实例（可复用配置）
 * 
 * @param defaultOptions - 默认请求选项
 * @returns HTTP 客户端方法集合
 * 
 * @example
 * ```typescript
 * const client = createClient({
 *   headers: { 'Authorization': 'Bearer token123' },
 *   timeout: 10000
 * });
 * 
 * const response = await client.get('https://api.example.com/users');
 * ```
 */
export function createClient(defaultOptions: HttpOptions = {}) {
  const mergeOptions = (options: HttpOptions = {}): HttpOptions => ({
    ...defaultOptions,
    ...options,
    headers: {
      ...defaultOptions.headers,
      ...options.headers,
    },
  });

  return {
    get: <T = unknown>(url: string, options?: HttpOptions) => get<T>(url, mergeOptions(options)),
    post: <T = unknown>(url: string, body: unknown, options?: HttpOptions) => post<T>(url, body, mergeOptions(options)),
    postForm: <T = unknown>(url: string, formData: Record<string, string>, options?: HttpOptions) => postForm<T>(url, formData, mergeOptions(options)),
    put: <T = unknown>(url: string, body: unknown, options?: HttpOptions) => put<T>(url, body, mergeOptions(options)),
    del: <T = unknown>(url: string, options?: HttpOptions) => del<T>(url, mergeOptions(options)),
    patch: <T = unknown>(url: string, body: unknown, options?: HttpOptions) => patch<T>(url, body, mergeOptions(options)),
    head: <T = unknown>(url: string, options?: HttpOptions) => head<T>(url, mergeOptions(options)),
  };
}

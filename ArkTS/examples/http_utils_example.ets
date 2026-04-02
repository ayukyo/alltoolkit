/**
 * HTTP Utils Example for ArkTS
 * 
 * This example demonstrates how to use the HTTP utilities module
 * in HarmonyOS applications.
 * 
 * @example
 * Run this example in a HarmonyOS project EntryAbility.ets or similar
 */

import {
  httpGet,
  httpPost,
  httpPostJson,
  httpPostForm,
  httpPut,
  httpPutJson,
  httpDelete,
  httpPatch,
  httpHead,
  buildUrl,
  buildQueryString,
  urlEncode,
  urlDecode,
  parseUrl,
  getDomain,
  getPath,
  isValidUrl,
  parseQueryString,
  addQueryParams,
  removeQueryParams,
  HttpResponse
} from '../http_utils/mod';

@Entry
@Component
struct HttpUtilsExample {
  @State message: string = 'HTTP Utils Demo';
  @State result: string = '';

  build() {
    Column({ space: 20 }) {
      Text(this.message)
        .fontSize(24)
        .fontWeight(FontWeight.Bold)

      Button('Test GET Request')
        .onClick(() => this.testGet())

      Button('Test POST JSON')
        .onClick(() => this.testPostJson())

      Button('Test URL Utils')
        .onClick(() => this.testUrlUtils())

      Scroll() {
        Text(this.result)
          .fontSize(14)
          .padding(16)
      }
      .height(300)
      .backgroundColor('#f5f5f5')
    }
    .width('100%')
    .height('100%')
    .padding(20)
  }

  /**
   * Example 1: Simple GET request
   */
  async testGet(): Promise<void> {
    try {
      // Example: Fetch user data from API
      const response = await httpGet('https://jsonplaceholder.typicode.com/users/1');
      
      this.result = `GET Request Result:\n` +
        `Status: ${response.statusCode} (${response.statusMessage})\n` +
        `Success: ${response.success}\n` +
        `Response Time: ${response.responseTime}ms\n` +
        `Body: ${response.body.substring(0, 200)}...`;
    } catch (error) {
      this.result = `GET Error: ${error.message}`;
    }
  }

  /**
   * Example 2: POST request with JSON data
   */
  async testPostJson(): Promise<void> {
    try {
      // Example: Create a new post
      const postData = {
        title: 'foo',
        body: 'bar',
        userId: 1
      };

      const response = await httpPostJson(
        'https://jsonplaceholder.typicode.com/posts',
        postData
      );

      this.result = `POST JSON Result:\n` +
        `Status: ${response.statusCode}\n` +
        `Success: ${response.success}\n` +
        `Body: ${JSON.stringify(response.body, null, 2)}`;
    } catch (error) {
      this.result = `POST Error: ${error.message}`;
    }
  }

  /**
   * Example 3: URL utilities demonstration
   */
  testUrlUtils(): void {
    const examples: string[] = [];

    // Build URL with parameters
    const url1 = buildUrl('https://api.example.com/search', {
      q: 'hello world',
      page: 1,
      limit: 10
    });
    examples.push(`buildUrl: ${url1}`);

    // Build query string
    const qs = buildQueryString({ name: 'John', age: 30, active: true });
    examples.push(`buildQueryString: ${qs}`);

    // URL encode/decode
    const encoded = urlEncode('hello world!');
    const decoded = urlDecode(encoded);
    examples.push(`urlEncode: ${encoded}`);
    examples.push(`urlDecode: ${decoded}`);

    // Parse URL
    const parsed = parseUrl('https://api.example.com:8080/users?id=123#section');
    examples.push(`parseUrl:\n  protocol: ${parsed.protocol}\n  host: ${parsed.host}\n  port: ${parsed.port}\n  pathname: ${parsed.pathname}`);

    // Get domain and path
    const domain = getDomain('https://api.example.com/users');
    const path = getPath('https://api.example.com/users/123');
    examples.push(`getDomain: ${domain}`);
    examples.push(`getPath: ${path}`);

    // Validate URL
    const valid1 = isValidUrl('https://example.com');
    const valid2 = isValidUrl('not a url');
    examples.push(`isValidUrl('https://example.com'): ${valid1}`);
    examples.push(`isValidUrl('not a url'): ${valid2}`);

    // Parse query string
    const params = parseQueryString('?name=John&age=30&city=NY');
    examples.push(`parseQueryString: ${JSON.stringify(params)}`);

    // Add query params
    const url2 = addQueryParams('https://api.example.com/users', { page: 2, limit: 20 });
    examples.push(`addQueryParams: ${url2}`);

    // Remove query params
    const url3 = removeQueryParams('https://api.example.com/users?page=1&sort=desc&limit=10', ['page']);
    examples.push(`removeQueryParams: ${url3}`);

    this.result = 'URL Utilities Examples:\n\n' + examples.join('\n\n');
  }
}

/**
 * Example 4: Using with custom headers and options
 */
async function exampleWithHeaders(): Promise<void> {
  const response = await httpGet('https://api.example.com/protected', {
    headers: {
      'Authorization': 'Bearer token123',
      'X-Custom-Header': 'value'
    },
    timeout: 10000,  // 10 seconds
    parseJson: true
  });

  if (response.success) {
    console.info('Data:', response.body);
  } else {
    console.error('Failed:', response.statusCode);
  }
}

/**
 * Example 5: Form submission
 */
async function exampleFormSubmission(): Promise<void> {
  const response = await httpPostForm('https://api.example.com/login', {
    username: 'admin',
    password: 'secret123'
  });

  console.info('Login result:', response.success);
}

/**
 * Example 6: PUT and DELETE operations
 */
async function examplePutAndDelete(): Promise<void> {
  // Update resource
  const putResponse = await httpPutJson(
    'https://api.example.com/users/1',
    { name: 'Updated Name', email: 'new@example.com' }
  );

  // Delete resource
  const deleteResponse = await httpDelete('https://api.example.com/users/1');

  console.info('PUT success:', putResponse.success);
  console.info('DELETE success:', deleteResponse.success);
}

/**
 * Example 7: Error handling
 */
async function exampleErrorHandling(): Promise<void> {
  try {
    const response = await httpGet('https://invalid-domain-that-does-not-exist.com');
    
    if (!response.success) {
      console.error(`Request failed with status ${response.statusCode}`);
    }
  } catch (error) {
    console.error('Network error:', error.message);
  }
}

/**
 * Example 8: Generic type usage
 */
interface User {
  id: number;
  name: string;
  email: string;
}

async function exampleWithTypes(): Promise<void> {
  // Specify expected response type
  const response = await httpGet<User>('https://api.example.com/users/1', {
    parseJson: true
  });

  if (response.success) {
    // TypeScript knows response.body is of type User
    console.info('User name:', response.body.name);
    console.info('User email:', response.body.email);
  }
}

/**
 * HTTP Utilities Example
 * 
 * 演示如何使用 http_utils 模块进行 HTTP 请求
 * 
 * 运行方式:
 * 1. 确保已安装 TypeScript: npm install -g typescript
 * 2. 编译: tsc http_utils_example.ts --esModuleInterop --target ES2020
 * 3. 运行: node http_utils_example.js
 * 
 * 或使用 ts-node 直接运行:
 * npx ts-node http_utils_example.ts
 */

import {
  get,
  post,
  postForm,
  put,
  del,
  patch,
  head,
  buildUrl,
  buildQueryString,
  urlEncode,
  urlDecode,
  createClient,
  HttpError,
  TimeoutError,
} from '../http_utils/mod';

// ==================== 基础用法示例 ====================

async function basicExamples() {
  console.log('=== 基础 HTTP 请求示例 ===\n');

  // GET 请求示例
  try {
    console.log('1. GET 请求 - 获取用户信息');
    const response = await get('https://jsonplaceholder.typicode.com/users/1');
    console.log('状态码:', response.status);
    console.log('用户名:', (response.data as { name: string }).name);
    console.log();
  } catch (error) {
    console.error('GET 请求失败:', error);
  }

  // POST 请求示例
  try {
    console.log('2. POST 请求 - 创建新用户');
    const response = await post('https://jsonplaceholder.typicode.com/users', {
      name: '张三',
      email: 'zhangsan@example.com',
      username: 'zhangsan',
    });
    console.log('状态码:', response.status);
    console.log('创建的用户 ID:', (response.data as { id: number }).id);
    console.log();
  } catch (error) {
    console.error('POST 请求失败:', error);
  }

  // PUT 请求示例
  try {
    console.log('3. PUT 请求 - 更新用户信息');
    const response = await put('https://jsonplaceholder.typicode.com/users/1', {
      name: '李四',
      email: 'lisi@example.com',
    });
    console.log('状态码:', response.status);
    console.log();
  } catch (error) {
    console.error('PUT 请求失败:', error);
  }

  // DELETE 请求示例
  try {
    console.log('4. DELETE 请求 - 删除用户');
    const response = await del('https://jsonplaceholder.typicode.com/users/1');
    console.log('状态码:', response.status);
    console.log('删除成功');
    console.log();
  } catch (error) {
    console.error('DELETE 请求失败:', error);
  }
}

// ==================== URL 工具示例 ====================

function urlUtilityExamples() {
  console.log('=== URL 工具函数示例 ===\n');

  // 构建查询字符串
  console.log('1. 构建查询字符串');
  const query = buildQueryString({
    search: 'TypeScript教程',
    page: 1,
    limit: 10,
    active: true,
  });
  console.log('查询字符串:', query);
  console.log();

  // 构建完整 URL
  console.log('2. 构建完整 URL');
  const url = buildUrl('https://api.example.com/search', {
    q: 'hello world',
    category: 'tech',
  });
  console.log('完整 URL:', url);
  console.log();

  // URL 编码和解码
  console.log('3. URL 编码和解码');
  const original = 'Hello World! 你好世界！@#$%';
  const encoded = urlEncode(original);
  const decoded = urlDecode(encoded);
  console.log('原始:', original);
  console.log('编码:', encoded);
  console.log('解码:', decoded);
  console.log();
}

// ==================== 高级用法示例 ====================

async function advancedExamples() {
  console.log('=== 高级用法示例 ===\n');

  // 带自定义请求头的请求
  try {
    console.log('1. 带自定义请求头的 GET 请求');
    const response = await get('https://jsonplaceholder.typicode.com/users', {
      headers: {
        'Accept': 'application/json',
        'X-Custom-Header': 'my-value',
      },
    });
    console.log('获取到', (response.data as unknown[]).length, '个用户');
    console.log();
  } catch (error) {
    console.error('请求失败:', error);
  }

  // 带超时的请求
  try {
    console.log('2. 带超时的请求（5秒）');
    const response = await get('https://jsonplaceholder.typicode.com/users', {
      timeout: 5000,
    });
    console.log('请求成功，状态码:', response.status);
    console.log();
  } catch (error) {
    if (error instanceof TimeoutError) {
      console.error('请求超时');
    } else {
      console.error('请求失败:', error);
    }
  }

  // 表单 POST 请求
  try {
    console.log('3. 表单 POST 请求');
    const response = await postForm('https://httpbin.org/post', {
      username: 'testuser',
      password: 'testpass',
    });
    console.log('表单提交成功');
    console.log();
  } catch (error) {
    console.error('表单提交失败:', error);
  }
}

// ==================== 客户端实例示例 ====================

async function clientExample() {
  console.log('=== HTTP 客户端实例示例 ===\n');

  // 创建带默认配置的客户端
  const apiClient = createClient({
    headers: {
      'Authorization': 'Bearer your-api-token-here',
      'Content-Type': 'application/json',
    },
    timeout: 10000,
  });

  try {
    console.log('使用客户端发送 GET 请求');
    const response = await apiClient.get('https://jsonplaceholder.typicode.com/posts/1');
    console.log('文章标题:', (response.data as { title: string }).title);
    console.log();
  } catch (error) {
    console.error('请求失败:', error);
  }

  try {
    console.log('使用客户端发送 POST 请求');
    const response = await apiClient.post('https://jsonplaceholder.typicode.com/posts', {
      title: '新文章',
      body: '这是文章内容',
      userId: 1,
    });
    console.log('创建的文章 ID:', (response.data as { id: number }).id);
    console.log();
  } catch (error) {
    console.error('请求失败:', error);
  }
}

// ==================== 错误处理示例 ====================

async function errorHandlingExample() {
  console.log('=== 错误处理示例 ===\n');

  // 处理 HTTP 错误
  try {
    console.log('请求不存在的资源（模拟 404 错误）');
    await get('https://jsonplaceholder.typicode.com/users/999999');
  } catch (error) {
    if (error instanceof HttpError) {
      console.log('捕获到 HTTP 错误:');
      console.log('  状态码:', error.status);
      console.log('  消息:', error.message);
      console.log('  URL:', error.url);
    } else if (error instanceof TimeoutError) {
      console.log('请求超时');
    } else {
      console.log('其他错误:', error);
    }
  }
  console.log();
}

// ==================== 泛型使用示例 ====================

interface User {
  id: number;
  name: string;
  email: string;
  username: string;
}

interface Post {
  userId: number;
  id: number;
  title: string;
  body: string;
}

async function genericExample() {
  console.log('=== 泛型使用示例 ===\n');

  // 使用泛型获取类型化的响应
  try {
    console.log('使用泛型获取用户数据');
    const response = await get<User>('https://jsonplaceholder.typicode.com/users/1');
    
    // response.data 现在是 User 类型，有完整的类型提示
    console.log('用户 ID:', response.data.id);
    console.log('用户名:', response.data.name);
    console.log('邮箱:', response.data.email);
    console.log('账号:', response.data.username);
    console.log();
  } catch (error) {
    console.error('请求失败:', error);
  }

  try {
    console.log('使用泛型获取文章数据');
    const response = await get<Post>('https://jsonplaceholder.typicode.com/posts/1');
    
    console.log('文章 ID:', response.data.id);
    console.log('标题:', response.data.title);
    console.log('内容预览:', response.data.body.substring(0, 50) + '...');
    console.log();
  } catch (error) {
    console.error('请求失败:', error);
  }
}

// ==================== 主程序 ====================

async function main() {
  console.log('╔════════════════════════════════════════════════════════╗');
  console.log('║     TypeScript HTTP Utilities - 使用示例              ║');
  console.log('╚════════════════════════════════════════════════════════╝\n');

  // URL 工具示例（同步）
  urlUtilityExamples();

  // 异步示例
  await basicExamples();
  await advancedExamples();
  await clientExample();
  await errorHandlingExample();
  await genericExample();

  console.log('所有示例执行完成！');
}

// 运行主程序
main().catch(console.error);

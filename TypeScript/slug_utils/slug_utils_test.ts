/**
 * Slug Utils 测试文件
 * 
 * @author AllToolkit
 * @date 2026-05-05
 */

import {
  SlugGenerator,
  slugify,
  slugifyUnique,
  isValidSlug,
  extractSlugFromUrl,
  slugifyBatch,
  slugToTitle,
} from './mod';

// 测试计数器
let passed = 0;
let failed = 0;

/**
 * 简单的测试断言函数
 */
function assertEqual(actual: any, expected: any, testName: string): void {
  if (actual === expected) {
    passed++;
    console.log(`✅ ${testName}`);
  } else {
    failed++;
    console.log(`❌ ${testName}`);
    console.log(`   Expected: "${expected}"`);
    console.log(`   Actual: "${actual}"`);
  }
}

/**
 * 断言为真
 */
function assertTrue(condition: boolean, testName: string): void {
  if (condition) {
    passed++;
    console.log(`✅ ${testName}`);
  } else {
    failed++;
    console.log(`❌ ${testName} - Expected: true, got: false`);
  }
}

/**
 * 断言为假
 */
function assertFalse(condition: boolean, testName: string): void {
  if (!condition) {
    passed++;
    console.log(`✅ ${testName}`);
  } else {
    failed++;
    console.log(`❌ ${testName} - Expected: false, got: true`);
  }
}

console.log('='.repeat(60));
console.log('Slug Utils 测试套件');
console.log('='.repeat(60));

// ========== 基础功能测试 ==========
console.log('\n📦 基础功能测试');

assertEqual(
  slugify('Hello World'),
  'hello-world',
  '基本字符串转换'
);

assertEqual(
  slugify('  Multiple   Spaces  '),
  'multiple-spaces',
  '处理多余空格'
);

assertEqual(
  slugify('Hello    World    Test'),
  'hello-world-test',
  '合并多个空格'
);

// ========== 分隔符测试 ==========
console.log('\n📦 分隔符测试');

assertEqual(
  slugify('Hello World', { separator: '_' }),
  'hello_world',
  '使用下划线分隔符'
);

assertEqual(
  slugify('Hello World', { separator: '.' }),
  'hello.world',
  '使用点分隔符'
);

assertEqual(
  slugify('Hello World', { separator: '~' }),
  'hello~world',
  '使用波浪号分隔符'
);

// ========== 大小写测试 ==========
console.log('\n📦 大小写测试');

assertEqual(
  slugify('HELLO WORLD'),
  'hello-world',
  '默认转小写'
);

assertEqual(
  slugify('Hello World', { lowercase: false }),
  'Hello-World',
  '保留原大小写'
);

// ========== 特殊字符测试 ==========
console.log('\n📦 特殊字符测试');

assertEqual(
  slugify('Hello!@#$%^&*World'),
  'hello-world',
  '移除特殊字符'
);

assertEqual(
  slugify('Hello (World) [Test]'),
  'hello-world-test',
  '处理括号'
);

assertEqual(
  slugify('Hello "World" \'Test\''),
  'hello-world-test',
  '处理引号'
);

assertEqual(
  slugify('a+b=c'),
  'a-b-c',
  '处理数学运算符'
);

// ========== 保留字符测试 ==========
console.log('\n📦 保留字符测试');

assertEqual(
  slugify('v1.0.0', { preserveChars: ['.'] }),
  'v1.0.0',
  '保留版本号中的点'
);

assertEqual(
  slugify('file_name.txt', { preserveChars: ['.', '_'] }),
  'file_name.txt',
  '保留文件名中的点和下划线'
);

// ========== 中文转换测试 ==========
console.log('\n📦 中文转换测试');

assertEqual(
  slugify('你好世界', { convertChinese: true }),
  'ni-hao-shi-jie',
  '中文转拼音'
);

assertEqual(
  slugify('Hello 你好 World', { convertChinese: true }),
  'hello-ni-hao-world',
  '中英文混合'
);

assertEqual(
  slugify('这是一篇文章标题', { convertChinese: true }),
  'zhe-shi-yi-pian-wen-zhang-biao-ti',
  '文章标题转拼音'
);

// ========== 长度限制测试 ==========
console.log('\n📦 长度限制测试');

assertEqual(
  slugify('This is a very long title that needs to be truncated', { maxLength: 20 }),
  'this-is-a-very-long',
  '截断长标题'
);

assertEqual(
  slugify('Hello World', { maxLength: 5 }),
  'hello',
  '短标题截断'
);

assertEqual(
  slugify('This-Is-A-Test', { maxLength: 10 }),
  'this-is-a',
  '在分隔符处截断'
);

// ========== 边界情况测试 ==========
console.log('\n📦 边界情况测试');

assertEqual(
  slugify(''),
  '',
  '空字符串'
);

assertEqual(
  slugify('   '),
  '',
  '纯空格字符串'
);

assertEqual(
  slugify('!@#$%^&*()'),
  '',
  '纯特殊字符'
);

assertEqual(
  slugify('---hello---world---'),
  'hello-world',
  '首尾有分隔符'
);

// ========== SlugGenerator 类测试 ==========
console.log('\n📦 SlugGenerator 类测试');

const generator = new SlugGenerator({
  separator: '_',
  lowercase: true,
});

assertEqual(
  generator.generate('Hello World'),
  'hello_world',
  '使用配置生成器'
);

const generator2 = new SlugGenerator({
  separator: '-',
  lowercase: false,
});

assertEqual(
  generator2.generate('hello world'),
  'Hello-World',
  '保留大小写的生成器'
);

// ========== 唯一 slug 测试 ==========
console.log('\n📦 唯一 slug 测试');

const existing = new Set(['hello-world', 'hello-world-1']);

assertEqual(
  slugifyUnique('Hello World', existing),
  'hello-world-2',
  '生成唯一 slug'
);

assertEqual(
  slugifyUnique('Unique Title', existing),
  'unique-title',
  '唯一标题无需后缀'
);

const existing2 = new Set(['test-slug', 'test-slug-1', 'test-slug-2']);

assertEqual(
  slugifyUnique('Test Slug', existing2),
  'test-slug-3',
  '连续计数器'
);

// ========== 验证 slug 测试 ==========
console.log('\n📦 验证 slug 测试');

assertTrue(
  isValidSlug('hello-world'),
  '有效 slug'
);

assertTrue(
  isValidSlug('hello_world', '_'),
  '使用下划线的有效 slug'
);

assertTrue(
  isValidSlug('test123'),
  '纯字母数字 slug'
);

assertFalse(
  isValidSlug(''),
  '空 slug 无效'
);

assertFalse(
  isValidSlug('-hello-world'),
  '首字符为分隔符无效'
);

assertFalse(
  isValidSlug('hello-world-'),
  '尾字符为分隔符无效'
);

assertFalse(
  isValidSlug('hello--world'),
  '连续分隔符无效'
);

assertFalse(
  isValidSlug('hello world'),
  '包含空格无效'
);

assertFalse(
  isValidSlug('hello@world'),
  '包含特殊字符无效'
);

// ========== URL 提取测试 ==========
console.log('\n📦 URL 提取测试');

assertEqual(
  extractSlugFromUrl('https://example.com/blog/my-article-title'),
  'my-article-title',
  '从 URL 路径提取 slug'
);

assertEqual(
  extractSlugFromUrl('https://example.com/products/12345'),
  '12345',
  '提取数字 ID'
);

assertEqual(
  extractSlugFromUrl('https://example.com/downloads/file.zip'),
  'file',
  '移除文件扩展名'
);

assertEqual(
  extractSlugFromUrl('https://example.com/'),
  '',
  '根 URL 返回空'
);

// ========== 批量生成测试 ==========
console.log('\n📦 批量生成测试');

const titles = ['Hello World', 'Test Article', 'My Blog Post'];
const slugs = slugifyBatch(titles);

assertEqual(
  slugs[0],
  'hello-world',
  '批量生成 - 第一项'
);

assertEqual(
  slugs[1],
  'test-article',
  '批量生成 - 第二项'
);

assertEqual(
  slugs[2],
  'my-blog-post',
  '批量生成 - 第三项'
);

assertEqual(
  slugs.length,
  3,
  '批量生成 - 长度正确'
);

// ========== Slug 转标题测试 ==========
console.log('\n📦 Slug 转标题测试');

assertEqual(
  slugToTitle('hello-world'),
  'Hello World',
  '转换标准 slug'
);

assertEqual(
  slugToTitle('my_blog_post', '_'),
  'My Blog Post',
  '转换下划线分隔的 slug'
);

assertEqual(
  slugToTitle('this-is-a-test'),
  'This Is A Test',
  '转换多词 slug'
);

assertEqual(
  slugToTitle(''),
  '',
  '空 slug 转标题'
);

// ========== 复杂场景测试 ==========
console.log('\n📦 复杂场景测试');

assertEqual(
  slugify('Hello World! How are you today?'),
  'hello-world-how-are-you-today',
  '复杂句子'
);

assertEqual(
  slugify('User\'s Guide: Chapter 1'),
  'users-guide-chapter-1',
  '带有撇号的标题'
);

assertEqual(
  slugify('100% Guaranteed! Buy Now!!!'),
  '100-guaranteed-buy-now',
  '营销文本'
);

assertEqual(
  slugify('React 18: What\'s New?'),
  'react-18-whats-new',
  '技术文章标题'
);

// ========== 性能测试 ==========
console.log('\n📦 性能测试');

const start = Date.now();
const iterations = 10000;
for (let i = 0; i < iterations; i++) {
  slugify(`Test Title ${i} with some special characters! @#$%`);
}
const duration = Date.now() - start;

console.log(`   执行 ${iterations} 次 slug 生成耗时: ${duration}ms`);
assertTrue(
  duration < 1000,
  `性能测试通过 (期望 <1000ms, 实际: ${duration}ms)`
);

// ========== 输出测试结果 ==========
console.log('\n' + '='.repeat(60));
console.log(`测试完成: ${passed} 通过, ${failed} 失败`);
console.log('='.repeat(60));

// 退出码
if (failed > 0) {
  process.exit(1);
}
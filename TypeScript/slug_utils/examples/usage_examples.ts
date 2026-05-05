/**
 * Slug Utils 使用示例
 * 
 * 本文件演示如何使用 slug_utils 工具库
 * 
 * @author AllToolkit
 * @date 2026-05-05
 */

import {
  slugify,
  slugifyUnique,
  isValidSlug,
  extractSlugFromUrl,
  slugifyBatch,
  slugToTitle,
  SlugGenerator,
} from '../mod';

console.log('='.repeat(60));
console.log('Slug Utils 使用示例');
console.log('='.repeat(60));

// ========== 示例 1: 基本用法 ==========
console.log('\n📝 示例 1: 基本 slug 生成');

const title1 = 'Hello World';
const slug1 = slugify(title1);
console.log(`输入: "${title1}"`);
console.log(`输出: "${slug1}"`);
// 输出: "hello-world"

// ========== 示例 2: 文章标题 ==========
console.log('\n📝 示例 2: 文章标题处理');

const titles = [
  '如何使用 TypeScript 开发大型应用',
  'React 18 新特性详解！',
  'Node.js 性能优化：10 个实用技巧',
  'Python vs JavaScript：2026 年该学哪个？',
];

titles.forEach((title, index) => {
  const slug = slugify(title, { convertChinese: true });
  console.log(`  ${index + 1}. "${title}" → "${slug}"`);
});

// ========== 示例 3: 自定义配置 ==========
console.log('\n📝 示例 3: 自定义配置');

const title3 = 'Product Catalog 2024';
const slug3a = slugify(title3, { separator: '_' });
const slug3b = slugify(title3, { lowercase: false, separator: '.' });

console.log(`输入: "${title3}"`);
console.log(`使用下划线: "${slug3a}"`);
console.log(`使用点分隔符 + 保留大小写: "${slug3b}"`);

// ========== 示例 4: 版本号处理 ==========
console.log('\n📝 示例 4: 保留版本号格式');

const versionTitle = 'Release v2.0.1-beta';
const versionSlug = slugify(versionTitle, { preserveChars: ['.'] });

console.log(`输入: "${versionTitle}"`);
console.log(`输出: "${versionSlug}"`);

// ========== 示例 5: 唯一 slug 生成 ==========
console.log('\n📝 示例 5: 避免重复 slug');

const existingSlugs = new Set([
  'my-first-post',
  'my-first-post-1',
  'my-second-post',
]);

console.log('现有 slug:', [...existingSlugs]);

const newSlug1 = slugifyUnique('My First Post', existingSlugs);
console.log(`"My First Post" → "${newSlug1}"`);

const newSlug2 = slugifyUnique('My Third Post', existingSlugs);
console.log(`"My Third Post" → "${newSlug2}"`);

// ========== 示例 6: 验证 slug ==========
console.log('\n📝 示例 6: 验证 slug 格式');

const testSlugs = [
  'valid-slug',
  '-invalid-slug',
  'invalid-slug-',
  'another--invalid',
  'valid_slug_123',
];

testSlugs.forEach(slug => {
  const isValid = isValidSlug(slug);
  console.log(`  "${slug}" → ${isValid ? '✅ 有效' : '❌ 无效'}`);
});

// ========== 示例 7: URL 处理 ==========
console.log('\n📝 示例 7: 从 URL 提取 slug');

const urls = [
  'https://blog.example.com/posts/how-to-learn-typescript',
  'https://shop.example.com/products/12345',
  'https://docs.example.com/api/v2.0.0/reference',
];

urls.forEach(url => {
  const slug = extractSlugFromUrl(url);
  console.log(`  URL: ${url}`);
  console.log(`  提取: "${slug}"\n`);
});

// ========== 示例 8: 批量处理 ==========
console.log('\n📝 示例 8: 批量生成 slug');

const blogTitles = [
  'Introduction to Machine Learning',
  'Data Structures and Algorithms',
  'Web Development Best Practices',
  'Security in Modern Applications',
];

const blogSlugs = slugifyBatch(blogTitles);

console.log('批量转换结果:');
blogSlugs.forEach((slug, index) => {
  console.log(`  ${index + 1}. "${blogTitles[index]}" → "${slug}"`);
});

// ========== 示例 9: Slug 转回标题 ==========
console.log('\n📝 示例 9: Slug 转回可读标题');

const slugsToConvert = [
  'hello-world',
  'introduction-to-typescript',
  'web-development-best-practices',
];

slugsToConvert.forEach(slug => {
  const title = slugToTitle(slug);
  console.log(`  "${slug}" → "${title}"`);
});

// ========== 示例 10: 使用 SlugGenerator 类 ==========
console.log('\n📝 示例 10: 使用 SlugGenerator 类');

// 创建自定义配置的生成器
const blogSlugGenerator = new SlugGenerator({
  separator: '-',
  lowercase: true,
  maxLength: 50,
  convertChinese: true,
});

const articleTitle = '这是一篇关于前端开发的深度解析文章';
const articleSlug = blogSlugGenerator.generate(articleTitle);

console.log(`文章标题: "${articleTitle}"`);
console.log(`生成 slug: "${articleSlug}"`);

// 创建保留版本号的生成器
const releaseSlugGenerator = new SlugGenerator({
  separator: '-',
  lowercase: true,
  preserveChars: ['.'],
  maxLength: 30,
});

const releaseTitle = 'App Framework v3.2.1 Release Notes';
const releaseSlug = releaseSlugGenerator.generate(releaseTitle);

console.log(`\n发布标题: "${releaseTitle}"`);
console.log(`生成 slug: "${releaseSlug}"`);

// ========== 示例 11: 实际应用场景 ==========
console.log('\n📝 示例 11: 实际应用场景');

// 博客文章系统
interface BlogPost {
  title: string;
  slug: string;
  author: string;
}

const posts: BlogPost[] = [
  { title: 'Getting Started with Docker', slug: '', author: 'Alice' },
  { title: 'Kubernetes for Beginners', slug: '', author: 'Bob' },
  { title: 'CI/CD Pipeline Best Practices', slug: '', author: 'Charlie' },
];

// 为每篇文章生成 slug
posts.forEach(post => {
  post.slug = slugify(post.title);
});

console.log('博客文章列表:');
posts.forEach(post => {
  console.log(`  [${post.author}] ${post.title} → /posts/${post.slug}`);
});

// ========== 示例 12: 中文内容处理 ==========
console.log('\n📝 示例 12: 中文内容处理');

const chineseTitles = [
  '人工智能的发展历程',
  '机器学习入门教程',
  '深度学习框架对比分析',
  '自然语言处理实战案例',
];

console.log('中文文章标题转换:');
chineseTitles.forEach((title, index) => {
  const slug = slugify(title, { convertChinese: true });
  console.log(`  ${index + 1}. "${title}" → "${slug}"`);
});

console.log('\n' + '='.repeat(60));
console.log('所有示例执行完成！');
console.log('='.repeat(60));
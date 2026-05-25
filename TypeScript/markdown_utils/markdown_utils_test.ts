/**
 * Markdown Utilities - Comprehensive Test Suite
 * Zero external dependencies
 * Run with: npx tsx markdown_utils_test.ts
 */

import {
  slugify,
  escapeHtml,
  unescapeHtml,
  countWords,
  calculateReadingTime,
  extractHeadings,
  extractLinks,
  extractImages,
  extractCodeBlocks,
  generateTOC,
  tocToMarkdown,
  toPlainText,
  toHtml,
  calculateStats,
  parseFrontMatter,
  validate,
  type Heading,
  type Link,
  type Image,
  type CodeBlock,
} from './mod.js';

// ============================================================================
// Test Utilities
// ============================================================================

let passCount = 0;
let failCount = 0;

function test(name: string, fn: () => void): void {
  try {
    fn();
    console.log(`✅ ${name}`);
    passCount++;
  } catch (error) {
    console.log(`❌ ${name}`);
    console.log(`   Error: ${error instanceof Error ? error.message : String(error)}`);
    failCount++;
  }
}

function assertEqual<T>(actual: T, expected: T, message?: string): void {
  if (JSON.stringify(actual) !== JSON.stringify(expected)) {
    throw new Error(
      `Assertion failed${message ? `: ${message}` : ''}\n` +
      `  Expected: ${JSON.stringify(expected)}\n` +
      `  Actual:   ${JSON.stringify(actual)}`
    );
  }
}

function assertTrue(condition: boolean, message?: string): void {
  if (!condition) {
    throw new Error(`Assertion failed${message ? `: ${message}` : ''}`);
  }
}

// ============================================================================
// Slugify Tests
// ============================================================================

test('slugify: basic text', () => {
  assertEqual(slugify('Hello World'), 'hello-world');
});

test('slugify: with special characters', () => {
  assertEqual(slugify('Hello! @World#'), 'hello-world');
});

test('slugify: multiple spaces', () => {
  assertEqual(slugify('Hello    World'), 'hello-world');
});

test('slugify: Chinese characters', () => {
  assertEqual(slugify('你好世界'), '你好世界');
});

test('slugify: mixed Chinese and English', () => {
  assertEqual(slugify('Hello 世界'), 'hello-世界');
});

test('slugify: leading/trailing hyphens', () => {
  assertEqual(slugify('-Hello World-'), 'hello-world');
});

test('slugify: trim whitespace', () => {
  assertEqual(slugify('  Hello World  '), 'hello-world');
});

// ============================================================================
// HTML Escape/Unescape Tests
// ============================================================================

test('escapeHtml: basic characters', () => {
  assertEqual(escapeHtml('<div>"test"&\'data\'</div>'), 
    '&lt;div&gt;&quot;test&quot;&amp;&#39;data&#39;&lt;/div&gt;');
});

test('escapeHtml: empty string', () => {
  assertEqual(escapeHtml(''), '');
});

test('escapeHtml: no special characters', () => {
  assertEqual(escapeHtml('Hello World'), 'Hello World');
});

test('unescapeHtml: basic entities', () => {
  assertEqual(unescapeHtml('&lt;div&gt;'), '<div>');
});

test('unescapeHtml: all entities', () => {
  assertEqual(unescapeHtml('&lt;div&gt;&quot;test&quot;&amp;&#39;data&#39;'), 
    '<div>"test"&\'data\'');
});

test('unescapeHtml: nbsp', () => {
  assertEqual(unescapeHtml('Hello&nbsp;World'), 'Hello World');
});

// ============================================================================
// Word Count Tests
// ============================================================================

test('countWords: English only', () => {
  assertEqual(countWords('Hello World'), 2);
});

test('countWords: Chinese only', () => {
  assertEqual(countWords('你好世界'), 4);
});

test('countWords: mixed Chinese and English', () => {
  assertEqual(countWords('Hello 世界'), 3);
});

test('countWords: with punctuation', () => {
  assertEqual(countWords('Hello, World! How are you?'), 5);
});

test('countWords: empty string', () => {
  assertEqual(countWords(''), 0);
});

test('countWords: numbers', () => {
  assertEqual(countWords('123 abc 456'), 3);
});

// ============================================================================
// Reading Time Tests
// ============================================================================

test('calculateReadingTime: small text', () => {
  assertEqual(calculateReadingTime(100), 1);
});

test('calculateReadingTime: medium text', () => {
  assertEqual(calculateReadingTime(225), 1);
});

test('calculateReadingTime: large text', () => {
  assertEqual(calculateReadingTime(450), 2);
});

test('calculateReadingTime: custom speed', () => {
  assertEqual(calculateReadingTime(300, 150), 2);
});

test('calculateReadingTime: zero words', () => {
  assertEqual(calculateReadingTime(0), 1);
});

// ============================================================================
// Heading Extraction Tests
// ============================================================================

test('extractHeadings: ATX style headings', () => {
  const markdown = `# Heading 1
## Heading 2
### Heading 3`;
  const headings = extractHeadings(markdown);
  assertEqual(headings.length, 3);
  assertEqual(headings[0].level, 1);
  assertEqual(headings[0].text, 'Heading 1');
  assertEqual(headings[1].level, 2);
  assertEqual(headings[2].level, 3);
});

test('extractHeadings: heading with trailing #', () => {
  const headings = extractHeadings('# Heading 1 #');
  assertEqual(headings.length, 1);
  assertEqual(headings[0].text, 'Heading 1');
});

test('extractHeadings: Setext style h1', () => {
  const markdown = `Heading 1
=========`;
  const headings = extractHeadings(markdown);
  assertEqual(headings.length, 1);
  assertEqual(headings[0].level, 1);
  assertEqual(headings[0].text, 'Heading 1');
});

test('extractHeadings: Setext style h2', () => {
  const markdown = `Heading 2
---------`;
  const headings = extractHeadings(markdown);
  assertEqual(headings.length, 1);
  assertEqual(headings[0].level, 2);
});

test('extractHeadings: no headings', () => {
  const headings = extractHeadings('Just some text\nNo headings here');
  assertEqual(headings.length, 0);
});

test('extractHeadings: generate slugs', () => {
  const headings = extractHeadings('# Hello World!');
  assertEqual(headings[0].slug, 'hello-world');
});

// ============================================================================
// Link Extraction Tests
// ============================================================================

test('extractLinks: basic link', () => {
  const links = extractLinks('[Click here](https://example.com)');
  assertEqual(links.length, 1);
  assertEqual(links[0].text, 'Click here');
  assertEqual(links[0].href, 'https://example.com');
});

test('extractLinks: link with title', () => {
  const links = extractLinks('[Click here](https://example.com "Example")');
  assertEqual(links.length, 1);
  assertEqual(links[0].title, 'Example');
});

test('extractLinks: multiple links', () => {
  const links = extractLinks('[Link 1](url1) and [Link 2](url2)');
  assertEqual(links.length, 2);
});

test('extractLinks: reference links', () => {
  const markdown = `[Click here][ref]

[ref]: https://example.com`;
  const links = extractLinks(markdown);
  assertEqual(links.length, 1);
  assertEqual(links[0].href, 'https://example.com');
});

test('extractLinks: no links', () => {
  const links = extractLinks('Just text, no links');
  assertEqual(links.length, 0);
});

test('extractLinks: not images', () => {
  const links = extractLinks('![Image](url) and [Link](url)');
  assertEqual(links.length, 1);
  assertEqual(links[0].text, 'Link');
});

// ============================================================================
// Image Extraction Tests
// ============================================================================

test('extractImages: basic image', () => {
  const images = extractImages('![Alt text](image.png)');
  assertEqual(images.length, 1);
  assertEqual(images[0].alt, 'Alt text');
  assertEqual(images[0].src, 'image.png');
});

test('extractImages: image with title', () => {
  const images = extractImages('![Alt](img.png "Title")');
  assertEqual(images.length, 1);
  assertEqual(images[0].title, 'Title');
});

test('extractImages: multiple images', () => {
  const images = extractImages('![A](a.png) and ![B](b.png)');
  assertEqual(images.length, 2);
});

test('extractImages: reference images', () => {
  const markdown = `![Alt][ref]

[ref]: image.png`;
  const images = extractImages(markdown);
  assertEqual(images.length, 1);
  assertEqual(images[0].src, 'image.png');
});

test('extractImages: not links', () => {
  const images = extractImages('[Link](url) and ![Image](img.png)');
  assertEqual(images.length, 1);
});

// ============================================================================
// Code Block Extraction Tests
// ============================================================================

test('extractCodeBlocks: fenced code block', () => {
  const markdown = '```javascript\nconsole.log("Hello");\n```';
  const blocks = extractCodeBlocks(markdown);
  assertEqual(blocks.length, 1);
  assertEqual(blocks[0].language, 'javascript');
  assertEqual(blocks[0].code, 'console.log("Hello");');
  assertEqual(blocks[0].isInline, false);
});

test('extractCodeBlocks: code block with tildes', () => {
  const markdown = '~~~python\nprint("Hello")\n~~~';
  const blocks = extractCodeBlocks(markdown);
  assertEqual(blocks.length, 1);
  assertEqual(blocks[0].language, 'python');
});

test('extractCodeBlocks: no language', () => {
  const markdown = '```\ncode\n```';
  const blocks = extractCodeBlocks(markdown);
  assertEqual(blocks[0].language, '');
});

test('extractCodeBlocks: inline code', () => {
  const blocks = extractCodeBlocks('Use `console.log` for debugging');
  assertEqual(blocks.length, 1);
  assertEqual(blocks[0].isInline, true);
  assertEqual(blocks[0].code, 'console.log');
});

test('extractCodeBlocks: multiple blocks', () => {
  const markdown = '```js\ncode1\n```\n\n```python\ncode2\n```';
  const blocks = extractCodeBlocks(markdown);
  assertEqual(blocks.length, 2);
});

test('extractCodeBlocks: indented code block', () => {
  const markdown = '    indented code\n    more code';
  const blocks = extractCodeBlocks(markdown);
  assertTrue(blocks.length >= 1);
  assertTrue(blocks.some(b => b.code.includes('indented code')));
});

// ============================================================================
// TOC Generation Tests
// ============================================================================

test('generateTOC: simple hierarchy', () => {
  const markdown = `# H1
## H2
### H3
## H2-2`;
  const toc = generateTOC(markdown);
  assertEqual(toc.length, 1);
  assertEqual(toc[0].text, 'H1');
  assertEqual(toc[0].children.length, 2);
  assertEqual(toc[0].children[0].text, 'H2');
  assertEqual(toc[0].children[0].children.length, 1);
  assertEqual(toc[0].children[0].children[0].text, 'H3');
});

test('generateTOC: multiple top level', () => {
  const markdown = `# First
# Second`;
  const toc = generateTOC(markdown);
  assertEqual(toc.length, 2);
});

test('generateTOC: max depth', () => {
  const markdown = `# H1
## H2
### H3
#### H4`;
  const toc = generateTOC(markdown, 2);
  assertEqual(toc.length, 1);
  assertEqual(toc[0].children.length, 1);
  assertEqual(toc[0].children[0].text, 'H2');
  assertEqual(toc[0].children[0].children.length, 0);
});

test('tocToMarkdown: generates valid markdown', () => {
  const markdown = `# Title
## Section 1
### Subsection`;
  const toc = generateTOC(markdown);
  const md = tocToMarkdown(toc);
  assertTrue(md.includes('- [Title](#title)'));
  assertTrue(md.includes('  - [Section 1](#section-1)'));
  assertTrue(md.includes('    - [Subsection](#subsection)'));
});

// ============================================================================
// Plain Text Conversion Tests
// ============================================================================

test('toPlainText: remove headings', () => {
  const text = toPlainText('# Heading\nContent');
  assertTrue(!text.includes('#'));
  assertTrue(text.includes('Heading'));
});

test('toPlainText: remove emphasis', () => {
  const text = toPlainText('*italic* and **bold**');
  assertTrue(!text.includes('*'));
  assertEqual(text.includes('italic'), true);
  assertEqual(text.includes('bold'), true);
});

test('toPlainText: remove links', () => {
  const text = toPlainText('[Click here](url)');
  assertEqual(text.trim(), 'Click here');
});

test('toPlainText: remove images', () => {
  const text = toPlainText('![Alt](img.png)');
  assertTrue(!text.includes('!['));
});

test('toPlainText: remove code blocks', () => {
  const text = toPlainText('```js\ncode\n```\nText');
  assertTrue(!text.includes('```'));
  assertTrue(text.includes('Text'));
});

test('toPlainText: remove inline code', () => {
  const text = toPlainText('Use `code` here');
  assertTrue(!text.includes('`'));
});

test('toPlainText: remove list markers', () => {
  const text = toPlainText('- Item 1\n- Item 2');
  assertTrue(!text.match(/^\s*-\s+/m));
});

test('toPlainText: remove blockquotes', () => {
  const text = toPlainText('> Quote');
  assertEqual(text.trim(), 'Quote');
});

// ============================================================================
// HTML Conversion Tests
// ============================================================================

test('toHtml: headings', () => {
  const html = toHtml('# Title\n## Subtitle');
  assertTrue(html.includes('<h1>Title</h1>'));
  assertTrue(html.includes('<h2>Subtitle</h2>'));
});

test('toHtml: emphasis', () => {
  const html = toHtml('*italic* **bold**');
  assertTrue(html.includes('<em>italic</em>'));
  assertTrue(html.includes('<strong>bold</strong>'));
});

test('toHtml: links', () => {
  const html = toHtml('[Link](url)');
  assertTrue(html.includes('<a href="url">Link</a>'));
});

test('toHtml: images', () => {
  const html = toHtml('![Alt](img.png)');
  assertTrue(html.includes('<img src="img.png" alt="Alt">'));
});

test('toHtml: code blocks', () => {
  const html = toHtml('```js\ncode\n```');
  assertTrue(html.includes('<pre><code'));
  assertTrue(html.includes('class="language-js"'));
});

test('toHtml: inline code', () => {
  const html = toHtml('Use `code` here');
  assertTrue(html.includes('<code>code</code>'));
});

test('toHtml: horizontal rule', () => {
  const html = toHtml('---');
  assertTrue(html.includes('<hr>'));
});

test('toHtml: blockquote', () => {
  const html = toHtml('> Quote');
  assertTrue(html.includes('<blockquote>Quote</blockquote>'));
});

test('toHtml: escapes HTML', () => {
  const html = toHtml('```html\n<div>\n```');
  assertTrue(html.includes('&lt;div&gt;'));
});

// ============================================================================
// Statistics Tests
// ============================================================================

test('calculateStats: basic stats', () => {
  const markdown = `# Title

This is a paragraph.

\`\`\`js
code
\`\`\`

[Link](url)

![Image](img.png)`;
  
  const stats = calculateStats(markdown);
  assertTrue(stats.words > 0);
  assertTrue(stats.lines > 0);
  assertEqual(stats.headings, 1);
  assertEqual(stats.links, 1);
  assertEqual(stats.images, 1);
  assertEqual(stats.codeBlocks, 1);
  assertTrue(stats.readingTimeMinutes >= 1);
});

test('calculateStats: empty document', () => {
  const stats = calculateStats('');
  assertEqual(stats.characters, 0);
  assertEqual(stats.words, 0);
  assertEqual(stats.lines, 1);
  assertEqual(stats.headings, 0);
});

// ============================================================================
// Front Matter Tests
// ============================================================================

test('parseFrontMatter: YAML front matter', () => {
  const markdown = `---
title: Hello World
author: Test
date: 2024-01-01
---

# Content`;
  
  const fm = parseFrontMatter(markdown);
  assertEqual(fm.format, 'yaml');
  assertEqual(fm.data['title'], 'Hello World');
  assertEqual(fm.data['author'], 'Test');
  assertTrue(fm.content.includes('# Content'));
});

test('parseFrontMatter: no front matter', () => {
  const markdown = '# No Front Matter';
  const fm = parseFrontMatter(markdown);
  assertEqual(fm.format, 'none');
  assertEqual(fm.content, markdown);
});

test('parseFrontMatter: TOML front matter', () => {
  const markdown = `+++
title = "Hello"
count = 42
+++

# Content`;
  
  const fm = parseFrontMatter(markdown);
  assertEqual(fm.format, 'toml');
  assertEqual(fm.data['title'], 'Hello');
  assertEqual(fm.data['count'], 42);
});

test('parseFrontMatter: boolean values', () => {
  const markdown = `---
published: true
draft: false
---

Content`;
  
  const fm = parseFrontMatter(markdown);
  assertEqual(fm.data['published'], true);
  assertEqual(fm.data['draft'], false);
});

test('parseFrontMatter: numeric values', () => {
  const markdown = `---
count: 42
price: 3.14
---

Content`;
  
  const fm = parseFrontMatter(markdown);
  assertEqual(fm.data['count'], 42);
  assertEqual(fm.data['price'], 3.14);
});

// ============================================================================
// Validation Tests
// ============================================================================

test('validate: missing space after #', () => {
  const errors = validate('#Heading');
  assertTrue(errors.some(e => e.message.includes('Missing space')));
});

test('validate: empty link text', () => {
  const errors = validate('[]()');
  assertTrue(errors.some(e => e.message.includes('Empty link text')));
});

test('validate: empty image alt', () => {
  const errors = validate('![]()');
  assertTrue(errors.some(e => e.message.includes('Empty image alt')));
});

test('validate: unclosed inline code', () => {
  const errors = validate('Use `code here');
  assertTrue(errors.some(e => e.message.includes('Unclosed inline code')));
});

test('validate: trailing whitespace', () => {
  const errors = validate('Hello   ');
  assertTrue(errors.some(e => e.message.includes('Trailing whitespace')));
});

test('validate: unclosed code block', () => {
  const errors = validate('```\nunclosed code');
  assertTrue(errors.some(e => e.message.includes('Unclosed code block')));
});

test('validate: long line', () => {
  const longLine = 'a'.repeat(150);
  const errors = validate(longLine);
  assertTrue(errors.some(e => e.message.includes('Line too long')));
});

test('validate: valid markdown', () => {
  const errors = validate('# Heading\n\nParagraph text\n\n- List item');
  assertTrue(errors.length === 0);
});

test('validate: ignores code blocks', () => {
  const markdown = '```markdown\n#Heading\n```';
  const errors = validate(markdown);
  // Should not report errors inside code blocks
  assertTrue(!errors.some(e => e.message.includes('Missing space')));
});

// ============================================================================
// Integration Tests
// ============================================================================

test('integration: full document parsing', () => {
  const markdown = `---
title: Test Document
author: Test Author
---

# Introduction

This is a **test** document with *formatting*.

## Features

- Links: [Example](https://example.com)
- Images: ![Logo](logo.png)
- Code: \`inline code\`

### Code Block

\`\`\`javascript
function hello() {
  console.log("Hello, World!");
}
\`\`\`

## Conclusion

> A wise man once said something.

---

The end.`;

  // Parse front matter
  const fm = parseFrontMatter(markdown);
  assertEqual(fm.format, 'yaml');
  assertEqual(fm.data['title'], 'Test Document');

  // Extract headings
  const headings = extractHeadings(fm.content);
  assertEqual(headings.length, 4);

  // Extract links
  const links = extractLinks(fm.content);
  assertEqual(links.length, 1);
  assertEqual(links[0].href, 'https://example.com');

  // Extract images
  const images = extractImages(fm.content);
  assertEqual(images.length, 1);

  // Generate TOC
  const toc = generateTOC(fm.content);
  assertEqual(toc.length, 1);
  assertEqual(toc[0].text, 'Introduction');

  // Calculate stats
  const stats = calculateStats(fm.content);
  assertTrue(stats.words > 10);
  assertTrue(stats.codeBlocks >= 1);
  assertEqual(stats.headings, 4);
});

// ============================================================================
// Summary
// ============================================================================

console.log('\n' + '='.repeat(50));
console.log('Markdown Utilities Test Results');
console.log('='.repeat(50));
console.log(`✅ Passed: ${passCount}`);
console.log(`❌ Failed: ${failCount}`);
console.log(`📊 Total:  ${passCount + failCount}`);
console.log('='.repeat(50));

if (failCount > 0) {
  process.exit(1);
}
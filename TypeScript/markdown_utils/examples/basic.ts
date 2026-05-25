/**
 * Markdown Utilities - Usage Examples
 * Run with: deno run examples/basic.ts
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
} from '../mod.ts';

// Sample markdown document
const sampleMarkdown = `---
title: Getting Started with Markdown
author: Documentation Team
date: 2024-01-15
tags: markdown, tutorial
---

# Getting Started with Markdown

This is a comprehensive guide to **Markdown** formatting.

## Introduction

Markdown is a *lightweight markup language* created by John Gruber.

### Why Markdown?

- Easy to learn
- Portable across platforms
- Human-readable
- Widely supported

## Basic Syntax

### Headings

Use \`#\` symbols for headings. More \`#\` means smaller heading.

### Links and Images

Here's a link to [Daring Fireball](https://daringfireball.net/projects/markdown/ "Official Markdown Site").

And an image:

![Markdown Logo](https://markdown-here.com/img/icon256.png "Markdown Icon")

### Code Examples

Inline code: \`const x = 42;\`

Code block:

\`\`\`typescript
function greet(name: string): string {
  return \`Hello, \${name}!\`;
}

console.log(greet('World'));
\`\`\`

## Advanced Features

### Tables

| Name  | Age | City     |
|-------|-----|----------|
| Alice | 30  | New York |
| Bob   | 25  | London   |

### Blockquotes

> The best way to predict the future is to invent it.
> — Alan Kay

---

## Conclusion

Markdown is simple yet powerful. Start writing and enjoy!

\`\`\`python
# Final code example
print("Happy Markdown writing!")
\`\`\`
`;

console.log('='.repeat(60));
console.log('Markdown Utilities - Examples');
console.log('='.repeat(60));

// 1. Slugify
console.log('\n📌 slugify()');
console.log('   Input: "Hello World!"');
console.log('   Output:', slugify('Hello World!'));
console.log('   Input: "你好世界"');
console.log('   Output:', slugify('你好世界'));

// 2. HTML Escape
console.log('\n📌 escapeHtml()');
const unsafe = '<script>alert("XSS")</script>';
console.log('   Input:', unsafe);
console.log('   Output:', escapeHtml(unsafe));

// 3. Word Count
console.log('\n📌 countWords()');
const text = 'Hello World 你好世界';
console.log('   Input:', text);
console.log('   Output:', countWords(text), 'words');

// 4. Reading Time
console.log('\n📌 calculateReadingTime()');
console.log('   1000 words:', calculateReadingTime(1000), 'minutes');
console.log('   5000 words:', calculateReadingTime(5000), 'minutes');

// 5. Extract Headings
console.log('\n📌 extractHeadings()');
const headings = extractHeadings(sampleMarkdown);
console.log('   Found', headings.length, 'headings:');
headings.forEach(h => {
  console.log(`   ${'  '.repeat(h.level - 1)}${'#'.repeat(h.level)} ${h.text} (${h.slug})`);
});

// 6. Extract Links
console.log('\n📌 extractLinks()');
const links = extractLinks(sampleMarkdown);
console.log('   Found', links.length, 'links:');
links.forEach(l => {
  console.log(`   - "${l.text}" → ${l.href}${l.title ? ` (${l.title})` : ''}`);
});

// 7. Extract Images
console.log('\n📌 extractImages()');
const images = extractImages(sampleMarkdown);
console.log('   Found', images.length, 'images:');
images.forEach(img => {
  console.log(`   - Alt: "${img.alt}", Src: ${img.src}`);
});

// 8. Extract Code Blocks
console.log('\n📌 extractCodeBlocks()');
const codeBlocks = extractCodeBlocks(sampleMarkdown);
console.log('   Found', codeBlocks.length, 'code blocks:');
codeBlocks.forEach((cb, i) => {
  if (!cb.isInline) {
    console.log(`   ${i + 1}. Language: ${cb.language || 'none'}`);
    console.log(`      Lines: ${cb.code.split('\n').length}`);
  }
});

// 9. Generate TOC
console.log('\n📌 generateTOC()');
const toc = generateTOC(sampleMarkdown);
console.log('   Table of Contents:');
console.log(tocToMarkdown(toc, '   '));

// 10. Plain Text Conversion
console.log('\n📌 toPlainText()');
const plainText = toPlainText(sampleMarkdown);
console.log('   First 200 chars:');
console.log('   ' + plainText.substring(0, 200).replace(/\n/g, '\n   ') + '...');

// 11. HTML Conversion
console.log('\n📌 toHtml()');
const html = toHtml(sampleMarkdown);
console.log('   Generated HTML (first 300 chars):');
console.log('   ' + html.substring(0, 300).replace(/\n/g, '\n   ') + '...');

// 12. Calculate Statistics
console.log('\n📌 calculateStats()');
const stats = calculateStats(sampleMarkdown);
console.log('   Document Statistics:');
console.log(`   - Characters: ${stats.characters}`);
console.log(`   - Words: ${stats.words}`);
console.log(`   - Lines: ${stats.lines}`);
console.log(`   - Paragraphs: ${stats.paragraphs}`);
console.log(`   - Headings: ${stats.headings}`);
console.log(`   - Links: ${stats.links}`);
console.log(`   - Images: ${stats.images}`);
console.log(`   - Code Blocks: ${stats.codeBlocks}`);
console.log(`   - Reading Time: ${stats.readingTimeMinutes} minute(s)`);

// 13. Parse Front Matter
console.log('\n📌 parseFrontMatter()');
const fm = parseFrontMatter(sampleMarkdown);
console.log('   Format:', fm.format);
console.log('   Data:', JSON.stringify(fm.data, null, 2).split('\n').join('\n   '));

// 14. Validation
console.log('\n📌 validate()');
const issues = validate(sampleMarkdown);
if (issues.length === 0) {
  console.log('   ✓ No issues found!');
} else {
  console.log(`   Found ${issues.length} issue(s):`);
  issues.forEach(issue => {
    console.log(`   - Line ${issue.line}: [${issue.severity}] ${issue.message}`);
  });
}

// Validation with errors example
console.log('\n📌 validate() - With errors');
const badMarkdown = `#Heading without space

[Empty link]()

\`Unclosed code

Very very very very very very very very very very very very very very very very very long line`;
const badIssues = validate(badMarkdown);
console.log('   Found', badIssues.length, 'issue(s):');
badIssues.forEach(issue => {
  console.log(`   - Line ${issue.line}: [${issue.severity}] ${issue.message}`);
});

console.log('\n' + '='.repeat(60));
console.log('All examples completed!');
console.log('='.repeat(60));
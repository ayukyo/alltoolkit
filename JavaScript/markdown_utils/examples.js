/**
 * Examples for markdown_utils
 */

const {
    MarkdownParser,
    parse,
    extractMetadata,
    generateTOC,
    htmlToMarkdown,
    countWords,
    estimateReadingTime,
    stripMarkdown
} = require('./markdown_utils.js');

console.log('=== Markdown Utils Examples ===\n');

// Example 1: Basic Markdown Parsing
console.log('1. Basic Markdown Parsing');
console.log('--------------------------');
const markdown = `# Getting Started

This is an introduction to **markdown** with *emphasis*.

## Features

- Easy to write
- Human readable
- \`code\` support

Here's a [link](https://example.com) and an image:

![Logo](logo.png)

\`\`\`javascript
function hello() {
    console.log("Hello, Markdown!");
}
\`\`\`

| Name | Value |
|------|-------|
| A    | 100   |
| B    | 200   |
`;

const html = parse(markdown);
console.log(html);
console.log('\n');

// Example 2: Extract Metadata
console.log('2. Extract Metadata');
console.log('-------------------');
const metadata = extractMetadata(markdown);
console.log('Headings:', JSON.stringify(metadata.headings, null, 2));
console.log('Links:', JSON.stringify(metadata.links, null, 2));
console.log('Images:', JSON.stringify(metadata.images, null, 2));
console.log('\n');

// Example 3: Generate Table of Contents
console.log('3. Generate Table of Contents');
console.log('-------------------------------');
const toc = generateTOC(markdown);
console.log(toc);
console.log('\n');

// Example 4: HTML to Markdown
console.log('4. HTML to Markdown Conversion');
console.log('------------------------------');
const htmlDoc = `
<h1>HTML Document</h1>
<p>This is a <strong>paragraph</strong> with <em>formatting</em>.</p>
<ul>
<li>Item 1</li>
<li>Item 2</li>
</ul>
<a href="https://example.com">Visit Example</a>
`;
const md = htmlToMarkdown(htmlDoc);
console.log(md);
console.log('\n');

// Example 5: Word Count and Reading Time
console.log('5. Word Count and Reading Time');
console.log('------------------------------');
const longDoc = `# Article

${'This is a sentence. '.repeat(100)}`;

const wordCount = countWords(longDoc);
const readingTime = estimateReadingTime(longDoc);
console.log(`Word count: ${wordCount}`);
console.log(`Reading time: ${readingTime.text} (${readingTime.minutes} minutes)`);
console.log('\n');

// Example 6: Strip Markdown Formatting
console.log('6. Strip Markdown Formatting');
console.log('---------------------------');
const formatted = `# Important Notice

This document contains **bold** and *italic* text.

Check out [our website](https://example.com) for more info.`;
const plainText = stripMarkdown(formatted);
console.log('Original:');
console.log(formatted);
console.log('\nStripped:');
console.log(plainText);
console.log('\n');

// Example 7: Custom Parser Options
console.log('7. Custom Parser Options');
console.log('------------------------');
const parser = new MarkdownParser({
    gfm: true,      // GitHub Flavored Markdown
    breaks: false,  // Don't convert \n to <br>
    sanitize: true   // Escape HTML
});

const unsafeMd = '# Title\n<script>alert("xss")</script>\n\n**Bold**';
const safeHtml = parser.parse(unsafeMd);
console.log('With sanitization:');
console.log(safeHtml);
console.log('\n');

// Example 8: GFM Features
console.log('8. GitHub Flavored Markdown Features');
console.log('-----------------------------------');
const gfmMd = `## Task List

- [x] Completed task
- [ ] Incomplete task
- [ ] Another task

## Strikethrough

This is ~~deleted~~ text.

## Table

| Feature | Status |
|---------|--------|
| Tables  | ✓      |
| Tasks   | ✓      |
`;
console.log(parse(gfmMd));
console.log('\n');

// Example 9: Complex Document Processing
console.log('9. Complex Document Processing');
console.log('-----------------------------');
const blogPost = `# Introduction to Markdown

Markdown is a lightweight markup language designed by John Gruber.

## Why Use Markdown?

1. **Simple**: Easy to learn and use
2. **Portable**: Works everywhere
3. **Readable**: Looks good as plain text

Check out the [official guide](https://www.markdownguide.org) for more.

![Markdown Logo](markdown.png)

\`\`\`
Example code block
\`\`\`
`;

console.log('Original Markdown:');
console.log(blogPost);
console.log('\n---\n');

console.log('Metadata:');
const blogMeta = extractMetadata(blogPost);
console.log('Headings:', blogMeta.headings.map(h => `${'#'.repeat(h.level)} ${h.text}`).join('\n'));
console.log('Links:', blogMeta.links.map(l => `- ${l.text} -> ${l.url}`).join('\n'));
console.log('\n---\n');

console.log('Table of Contents:');
console.log(generateTOC(blogPost, { numbered: true }));
console.log('\n---\n');

console.log('Statistics:');
const stats = estimateReadingTime(blogPost);
console.log(`- Words: ${stats.words}`);
console.log(`- Reading time: ${stats.text}`);

console.log('\n=== End of Examples ===');
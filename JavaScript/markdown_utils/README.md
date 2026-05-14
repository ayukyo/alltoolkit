# Markdown Utils

A comprehensive, zero-dependency markdown parser and converter for JavaScript.

## Features

- ✅ Parse markdown to HTML
- ✅ Convert HTML to markdown (basic)
- ✅ Extract metadata (headings, links, images)
- ✅ Generate table of contents
- ✅ GitHub Flavored Markdown (GFM) support
- ✅ Word count and reading time estimation
- ✅ Strip markdown formatting
- ✅ Zero external dependencies

## Installation

```javascript
const {
    parse,
    extractMetadata,
    generateTOC,
    htmlToMarkdown,
    countWords,
    estimateReadingTime,
    stripMarkdown
} = require('./markdown_utils.js');
```

## Usage

### Parse Markdown to HTML

```javascript
const { parse } = require('./markdown_utils.js');

const markdown = `
# Heading

This is **bold** and *italic* text.

- Item 1
- Item 2

[Link](https://example.com)
`;

const html = parse(markdown);
console.log(html);
```

### Extract Metadata

```javascript
const { extractMetadata } = require('./markdown_utils.js');

const md = `
# Main Title
## Section 1

[Link](url) and ![Image](img.png)
`;

const meta = extractMetadata(md);
console.log(meta.headings); // [{ level: 1, text: 'Main Title', line: 1 }, ...]
console.log(meta.links);    // [{ text: 'Link', url: 'url', position: 10 }]
console.log(meta.images);   // [{ alt: 'Image', url: 'img.png', position: ... }]
```

### Generate Table of Contents

```javascript
const { generateTOC } = require('./markdown_utils.js');

const md = `
# Introduction
## Getting Started
## Advanced Topics
### Configuration
### Deployment
`;

const toc = generateTOC(md);
// - [Introduction](#introduction)
//   - [Getting Started](#getting-started)
//   - [Advanced Topics](#advanced-topics)
//     - [Configuration](#configuration)
//     - [Deployment](#deployment)
```

### HTML to Markdown

```javascript
const { htmlToMarkdown } = require('./markdown_utils.js');

const html = `
<h1>Title</h1>
<p>This is <strong>bold</strong> text.</p>
<a href="url">Link</a>
`;

const md = htmlToMarkdown(html);
// # Title
// This is **bold** text.
// [Link](url)
```

### Word Count & Reading Time

```javascript
const { countWords, estimateReadingTime } = require('./markdown_utils.js');

const md = 'Your long document here...';

console.log(countWords(md)); // 1234

const time = estimateReadingTime(md);
console.log(time.words);    // 1234
console.log(time.minutes);  // 7
console.log(time.text);     // "7 min read"
```

### Strip Formatting

```javascript
const { stripMarkdown } = require('./markdown_utils.js');

const md = '# Title with **bold** and [link](url)';
const plainText = stripMarkdown(md);
// "Title with bold and link"
```

### Custom Parser Options

```javascript
const { MarkdownParser } = require('./markdown_utils.js');

const parser = new MarkdownParser({
    gfm: true,      // Enable GitHub Flavored Markdown (default: true)
    breaks: false,  // Don't convert \n to <br> (default: true)
    sanitize: true  // Escape HTML in markdown (default: false)
});

const html = parser.parse(markdown);
```

## Supported Markdown Elements

### Basic Syntax
- Headers (H1-H6)
- Paragraphs
- Bold and italic text
- Links and images
- Inline code and code blocks
- Blockquotes
- Horizontal rules
- Unordered and ordered lists

### GFM Extensions
- Tables
- Task lists
- Strikethrough
- Fenced code blocks with language

## API Reference

### `parse(markdown, options)`
Parse markdown to HTML.

### `extractMetadata(markdown)`
Extract headings, links, and images from markdown.

### `generateTOC(markdown, options)`
Generate a table of contents.

Options:
- `maxLevel`: Maximum heading level to include (default: 6)
- `numbered`: Add numbering to TOC items (default: false)

### `htmlToMarkdown(html)`
Convert basic HTML to markdown.

### `countWords(markdown)`
Count words in markdown (excluding syntax).

### `estimateReadingTime(markdown, wpm)`
Estimate reading time (default: 200 wpm).

### `stripMarkdown(markdown)`
Remove markdown formatting to get plain text.

## Running Tests

```bash
node test.js
```

## Running Examples

```bash
node examples.js
```

## License

MIT License - Feel free to use in any project.
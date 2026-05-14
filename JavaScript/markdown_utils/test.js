/**
 * Test suite for markdown_utils
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

// Test utilities
let passed = 0;
let failed = 0;

function test(name, fn) {
    try {
        fn();
        console.log(`✓ ${name}`);
        passed++;
    } catch (error) {
        console.log(`✗ ${name}`);
        console.log(`  Error: ${error.message}`);
        failed++;
    }
}

function assertEqual(actual, expected, message = '') {
    if (actual !== expected) {
        throw new Error(`${message}\n  Expected: ${JSON.stringify(expected)}\n  Actual: ${JSON.stringify(actual)}`);
    }
}

function assertContains(actual, expected, message = '') {
    if (!actual.includes(expected)) {
        throw new Error(`${message}\n  Expected to contain: ${JSON.stringify(expected)}\n  Actual: ${JSON.stringify(actual)}`);
    }
}

function assertArrayEqual(actual, expected, message = '') {
    if (JSON.stringify(actual) !== JSON.stringify(expected)) {
        throw new Error(`${message}\n  Expected: ${JSON.stringify(expected)}\n  Actual: ${JSON.stringify(actual)}`);
    }
}

// Tests
console.log('\n=== Markdown Parser Tests ===\n');

// Headers
test('Parse H1 header', () => {
    const result = parse('# Header 1');
    assertEqual(result, '<h1>Header 1</h1>');
});

test('Parse H2 header', () => {
    const result = parse('## Header 2');
    assertEqual(result, '<h2>Header 2</h2>');
});

test('Parse H6 header', () => {
    const result = parse('###### Header 6');
    assertEqual(result, '<h6>Header 6</h6>');
});

// Emphasis
test('Parse bold with **', () => {
    const result = parse('**bold text**');
    assertContains(result, '<strong>bold text</strong>');
});

test('Parse bold with __', () => {
    const result = parse('__bold text__');
    assertContains(result, '<strong>bold text</strong>');
});

test('Parse italic with *', () => {
    const result = parse('*italic text*');
    assertContains(result, '<em>italic text</em>');
});

test('Parse italic with _', () => {
    const result = parse('_italic text_');
    assertContains(result, '<em>italic text</em>');
});

test('Parse strikethrough (GFM)', () => {
    const result = parse('~~strikethrough~~');
    assertContains(result, '<del>strikethrough</del>');
});

// Links and Images
test('Parse link', () => {
    const result = parse('[Example](https://example.com)');
    assertContains(result, '<a href="https://example.com">Example</a>');
});

test('Parse image', () => {
    const result = parse('![Alt text](image.png)');
    assertContains(result, '<img src="image.png" alt="Alt text">');
});

// Code
test('Parse inline code', () => {
    const result = parse('Use `console.log()` for debugging');
    assertContains(result, '<code>console.log()</code>');
});

test('Parse code block', () => {
    const result = parse('```javascript\nconst x = 1;\n```');
    assertContains(result, '<pre><code');
    assertContains(result, 'language-javascript');
    assertContains(result, 'const x = 1;');
});

// Lists
test('Parse unordered list', () => {
    const result = parse('- Item 1\n- Item 2');
    assertContains(result, '<ul>');
    assertContains(result, '<li>Item 1</li>');
    assertContains(result, '<li>Item 2</li>');
    assertContains(result, '</ul>');
});

test('Parse ordered list', () => {
    const result = parse('1. First\n2. Second');
    assertContains(result, '<ol>');
    assertContains(result, '<li>First</li>');
    assertContains(result, '<li>Second</li>');
    assertContains(result, '</ol>');
});

// Blockquotes
test('Parse blockquote', () => {
    const result = parse('> This is a quote');
    assertContains(result, '<blockquote>This is a quote</blockquote>');
});

// Horizontal Rule
test('Parse horizontal rule with ---', () => {
    const result = parse('---');
    assertContains(result, '<hr>');
});

test('Parse horizontal rule with ***', () => {
    const result = parse('***');
    assertContains(result, '<hr>');
});

// Tables (GFM)
test('Parse table', () => {
    const md = '| Name | Age |\n|------|-----|\n| John | 25 |';
    const result = parse(md);
    assertContains(result, '<table>');
    assertContains(result, '<th>Name</th>');
    assertContains(result, '<td>John</td>');
});

// Task Lists (GFM)
test('Parse task list', () => {
    const result = parse('- [ ] Todo\n- [x] Done');
    assertContains(result, 'type="checkbox"');
    assertContains(result, 'checked');
});

// Metadata Extraction
console.log('\n=== Metadata Extraction Tests ===\n');

test('Extract headings', () => {
    const md = '# Header 1\n## Header 2\n### Header 3';
    const meta = extractMetadata(md);
    assertEqual(meta.headings.length, 3);
    assertEqual(meta.headings[0].level, 1);
    assertEqual(meta.headings[0].text, 'Header 1');
});

test('Extract links', () => {
    const md = '[Link 1](url1) and [Link 2](url2)';
    const meta = extractMetadata(md);
    assertEqual(meta.links.length, 2);
    assertEqual(meta.links[0].text, 'Link 1');
    assertEqual(meta.links[0].url, 'url1');
});

test('Extract images', () => {
    const md = '![Image 1](img1.png) and ![Image 2](img2.png)';
    const meta = extractMetadata(md);
    assertEqual(meta.images.length, 2);
    assertEqual(meta.images[0].alt, 'Image 1');
    assertEqual(meta.images[0].url, 'img1.png');
});

// Table of Contents
console.log('\n=== TOC Generation Tests ===\n');

test('Generate TOC', () => {
    const md = '# Main\n## Section 1\n## Section 2';
    const toc = generateTOC(md);
    assertContains(toc, '[Main](#main)');
    assertContains(toc, '[Section 1](#section-1)');
});

test('Generate TOC with max level', () => {
    const md = '# H1\n## H2\n### H3';
    const toc = generateTOC(md, { maxLevel: 2 });
    assertContains(toc, '[H1](#h1)');
    assertContains(toc, '[H2](#h2)');
    if (toc.includes('H3')) {
        throw new Error('H3 should not be in TOC with maxLevel=2');
    }
});

// HTML to Markdown
console.log('\n=== HTML to Markdown Tests ===\n');

test('Convert H1', () => {
    const result = htmlToMarkdown('<h1>Title</h1>');
    assertContains(result, '# Title');
});

test('Convert link', () => {
    const result = htmlToMarkdown('<a href="url">Text</a>');
    assertContains(result, '[Text](url)');
});

test('Convert bold', () => {
    const result = htmlToMarkdown('<strong>bold</strong>');
    assertContains(result, '**bold**');
});

test('Convert italic', () => {
    const result = htmlToMarkdown('<em>italic</em>');
    assertContains(result, '*italic*');
});

// Word Count
console.log('\n=== Word Count Tests ===\n');

test('Count words', () => {
    const md = '# Title\n\nThis is a paragraph with **bold** text.';
    const count = countWords(md);
    assertEqual(count, 8); // Title This is a paragraph with bold text
});

test('Count words ignoring code', () => {
    const md = 'Text `code` more text';
    const count = countWords(md);
    assertEqual(count, 3); // Text more text
});

// Reading Time
console.log('\n=== Reading Time Tests ===\n');

test('Estimate reading time', () => {
    const md = 'word '.repeat(400); // 400 words
    const time = estimateReadingTime(md);
    assertEqual(time.words, 400);
    assertEqual(time.minutes, 2); // 400 / 200 = 2
    assertContains(time.text, '2 min read');
});

// Strip Markdown
console.log('\n=== Strip Markdown Tests ===\n');

test('Strip headers', () => {
    const result = stripMarkdown('# Header');
    assertEqual(result, 'Header');
});

test('Strip links', () => {
    const result = stripMarkdown('[Link](url)');
    assertEqual(result, 'Link');
});

test('Strip emphasis', () => {
    const result = stripMarkdown('**bold** and *italic*');
    assertEqual(result, 'bold and italic');
});

test('Strip code', () => {
    const result = stripMarkdown('Text `code` here');
    assertEqual(result, 'Text  here');
});

// Edge Cases
console.log('\n=== Edge Case Tests ===\n');

test('Empty input', () => {
    assertEqual(parse(''), '');
    assertEqual(parse(null), '');
    assertEqual(parse(undefined), '');
});

test('Complex document', () => {
    const md = `# Main Title

This is a **paragraph** with *emphasis*.

## Features

- Feature 1
- Feature 2

\`\`\`javascript
const x = 1;
\`\`\`

[Link](https://example.com)`;
    
    const result = parse(md);
    assertContains(result, '<h1>Main Title</h1>');
    assertContains(result, '<strong>paragraph</strong>');
    assertContains(result, '<em>emphasis</em>');
    assertContains(result, '<ul>');
    assertContains(result, '<pre><code');
    assertContains(result, '<a href="https://example.com">Link</a>');
});

// Sanitization
console.log('\n=== Sanitization Tests ===\n');

test('HTML sanitization disabled by default', () => {
    const md = '<script>alert("xss")</script>';
    const result = parse(md);
    assertContains(result, '<script>');
});

test('HTML sanitization enabled', () => {
    const md = '<script>alert("xss")</script>';
    const result = parse(md, { sanitize: true });
    assertContains(result, '&lt;script&gt;');
});

// Summary
console.log('\n' + '='.repeat(50));
console.log(`Total: ${passed + failed} tests`);
console.log(`Passed: ${passed}`);
console.log(`Failed: ${failed}`);
console.log('='.repeat(50) + '\n');

if (failed > 0) {
    process.exit(1);
}
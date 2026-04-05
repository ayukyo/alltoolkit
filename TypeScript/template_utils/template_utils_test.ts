/**
 * Template Engine Test Suite
 * Comprehensive tests for the TypeScript Template Engine
 */

import { TemplateEngine, renderTemplate, BuiltInFilters } from './mod';

// Test utilities
function assertEqual(actual: any, expected: any, message: string): void {
    if (actual !== expected) {
        throw new Error(`FAIL: ${message}\n  Expected: ${expected}\n  Actual: ${actual}`);
    }
    console.log(`PASS: ${message}`);
}

// Test counters
let passed = 0;
let failed = 0;

function runTest(name: string, fn: () => void): void {
    try {
        fn();
        passed++;
    } catch (e: any) {
        failed++;
        console.error(`\nTEST FAILED: ${name}`);
        console.error(e.message);
    }
}

console.log('=== Template Engine Test Suite ===\n');

// Variable Interpolation Tests
runTest('Variable interpolation - simple', () => {
    const result = renderTemplate('Hello, {{ name }}!', { name: 'World' });
    assertEqual(result, 'Hello, World!', 'Simple variable interpolation');
});

runTest('Variable interpolation - nested object', () => {
    const result = renderTemplate('{{ user.name }}', { user: { name: 'Alice' } });
    assertEqual(result, 'Alice', 'Nested object access');
});

runTest('Variable interpolation - undefined', () => {
    const result = renderTemplate('Hello, {{ missing }}!', {});
    assertEqual(result, 'Hello, !', 'Undefined variable returns empty');
});

// Filter Tests
runTest('Filter - upper', () => {
    const result = renderTemplate('{{ name | upper }}', { name: 'hello' });
    assertEqual(result, 'HELLO', 'Uppercase filter');
});

runTest('Filter - lower', () => {
    const result = renderTemplate('{{ name | lower }}', { name: 'HELLO' });
    assertEqual(result, 'hello', 'Lowercase filter');
});

runTest('Filter - capitalize', () => {
    const result = renderTemplate('{{ name | capitalize }}', { name: 'hello world' });
    assertEqual(result, 'Hello world', 'Capitalize filter');
});

runTest('Filter - title', () => {
    const result = renderTemplate('{{ name | title }}', { name: 'hello world' });
    assertEqual(result, 'Hello World', 'Title case filter');
});

runTest('Filter - trim', () => {
    const result = renderTemplate('{{ text | trim }}', { text: '  hello  ' });
    assertEqual(result, 'hello', 'Trim filter');
});

runTest('Filter - escape', () => {
    const result = renderTemplate('{{ html | escape }}', { html: '<script>' });
    assertEqual(result, '&lt;script&gt;', 'Escape filter');
});

runTest('Filter - default', () => {
    const result = renderTemplate('{{ missing | default:N/A }}', {});
    assertEqual(result, 'N/A', 'Default filter');
});

runTest('Filter - join', () => {
    const result = renderTemplate('{{ items | join:, }}', { items: ['a', 'b', 'c'] });
    assertEqual(result, 'a,b,c', 'Join filter');
});

runTest('Filter - size', () => {
    const result = renderTemplate('{{ items | size }}', { items: [1, 2, 3] });
    assertEqual(result, '3', 'Size filter');
});

runTest('Filter chain', () => {
    const result = renderTemplate('{{ text | trim | upper }}', { text: '  hello  ' });
    assertEqual(result, 'HELLO', 'Filter chain');
});

// Conditional Tests
runTest('Conditional - if true', () => {
    const result = renderTemplate('{% if user %}Hello{% endif %}', { user: 'Alice' });
    assertEqual(result, 'Hello', 'If condition true');
});

runTest('Conditional - if false', () => {
    const result = renderTemplate('{% if user %}Hello{% endif %}', { user: '' });
    assertEqual(result, '', 'If condition false');
});

runTest('Conditional - if else', () => {
    const template = '{% if user %}Hello{% else %}Guest{% endif %}';
    assertEqual(renderTemplate(template, { user: 'Alice' }), 'Hello', 'If else - true');
    assertEqual(renderTemplate(template, {}), 'Guest', 'If else - false');
});

runTest('Conditional - equality', () => {
    const result = renderTemplate('{% if count == 5 %}Five{% endif %}', { count: 5 });
    assertEqual(result, 'Five', 'Equality operator');
});

runTest('Conditional - not operator', () => {
    const result = renderTemplate('{% if not user %}Guest{% endif %}', { user: '' });
    assertEqual(result, 'Guest', 'Not operator');
});

// Loop Tests
runTest('Loop - basic', () => {
    const result = renderTemplate('{% for item in items %}{{ item }}{% endfor %}', { items: ['a', 'b', 'c'] });
    assertEqual(result, 'abc', 'Basic loop');
});

runTest('Loop - with filter', () => {
    const template = '{% for item in items %}{{ item | upper }}{% endfor %}';
    const result = renderTemplate(template, { items: ['a', 'b', 'c'] });
    assertEqual(result, 'ABC', 'Loop with filter');
});

// Comment Tests
runTest('Comments - removed', () => {
    const result = renderTemplate('Hello {# this is a comment #} World', {});
    assertEqual(result, 'Hello  World', 'Comments are removed');
});

// Include Tests
runTest('Include - partial', () => {
    const partials = { header: '<h1>{{ title }}</h1>' };
    const result = renderTemplate('{% include "header" %}', { title: 'Page' }, partials);
    assertEqual(result, '<h1>Page</h1>', 'Include partial');
});

// Custom Filter Tests
runTest('Custom filter', () => {
    const engine = new TemplateEngine();
    engine.registerFilter('double', (n: number) => n * 2);
    const result = engine.render('{{ num | double }}', { num: 21 });
    assertEqual(result, '42', 'Custom filter');
});

// Nested Object Tests
runTest('Nested object - deep', () => {
    const result = renderTemplate('{{ a.b.c }}', { a: { b: { c: 'deep' } } });
    assertEqual(result, 'deep', 'Deep nested access');
});

// Summary
console.log('\n=== Test Summary ===');
console.log(`Passed: ${passed}`);
console.log(`Failed: ${failed}`);
console.log(`Total: ${passed + failed}`);

if (failed > 0) {
    process.exit(1);
}

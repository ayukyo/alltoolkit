/**
 * TypeScript Template Engine Example
 * Demonstrates usage of the Template Engine Utilities
 */

import { TemplateEngine, renderTemplate } from '../template_utils/mod';

console.log('=== TypeScript Template Engine Examples ===\n');

// Example 1: Basic Variable Interpolation
console.log('1. Basic Variable Interpolation');
console.log('-------------------------------');
const greeting = renderTemplate('Hello, {{ name }}!', { name: 'World' });
console.log(`Template: "Hello, {{ name }}!"`);
console.log(`Context: { name: 'World' }`);
console.log(`Result: "${greeting}"\n`);

// Example 2: Filters
console.log('2. Using Filters');
console.log('----------------');
const upperName = renderTemplate('{{ name | upper }}', { name: 'alice' });
console.log(`Uppercase: "${upperName}"`);

const titleName = renderTemplate('{{ name | title }}', { name: 'hello world' });
console.log(`Title case: "${titleName}"`);

const trimmed = renderTemplate('{{ text | trim }}', { text: '  hello  ' });
console.log(`Trimmed: "${trimmed}"`);

const escaped = renderTemplate('{{ html | escape }}', { html: '<script>alert("xss")</script>' });
console.log(`Escaped HTML: "${escaped}"\n`);

// Example 3: Filter Chains
console.log('3. Filter Chains');
console.log('----------------');
const chained = renderTemplate('{{ text | trim | upper }}', { text: '  hello world  ' });
console.log(`Template: "{{ text | trim | upper }}"`);
console.log(`Result: "${chained}"\n`);

// Example 4: Conditionals
console.log('4. Conditionals');
console.log('---------------');
const conditionalTemplate = `{% if user %}
Hello, {{ user }}!
{% else %}
Welcome, guest!
{% endif %}`;

console.log('With user:');
const withUser = renderTemplate(conditionalTemplate, { user: 'Alice' });
console.log(withUser.trim());

console.log('\nWithout user:');
const withoutUser = renderTemplate(conditionalTemplate, {});
console.log(withoutUser.trim());
console.log();

// Example 5: Loops
console.log('5. Loops');
console.log('--------');
const loopTemplate = `Items:
{% for item in items %}
- {{ item }}
{% endfor %}`;

const loopResult = renderTemplate(loopTemplate, { items: ['Apple', 'Banana', 'Cherry'] });
console.log(loopResult);

// Example 6: Array Filters
console.log('6. Array Filters');
console.log('----------------');
const joined = renderTemplate('{{ items | join:", " }}', { items: ['red', 'green', 'blue'] });
console.log(`Joined: "${joined}"`);

const firstItem = renderTemplate('First: {{ items | first }}', { items: ['a', 'b', 'c'] });
console.log(`First item: "${firstItem}"`);

const lastItem = renderTemplate('Last: {{ items | last }}', { items: ['a', 'b', 'c'] });
console.log(`Last item: "${lastItem}"`);

const size = renderTemplate('Count: {{ items | size }}', { items: [1, 2, 3, 4, 5] });
console.log(`Size: "${size}"\n`);

// Example 7: Number Filters
console.log('7. Number Filters');
console.log('-----------------');
const rounded = renderTemplate('Price: ${{ price | round:2 }}', { price: 19.999 });
console.log(`Rounded: "${rounded}"`);

const absolute = renderTemplate('Absolute: {{ num | abs }}', { num: -42 });
console.log(`Absolute: "${absolute}"\n`);

// Example 8: Default Values
console.log('8. Default Values');
console.log('-----------------');
const withDefault = renderTemplate('Name: {{ name | default:Anonymous }}', {});
console.log(`With default: "${withDefault}"`);

const withValue = renderTemplate('Name: {{ name | default:Anonymous }}', { name: 'Alice' });
console.log(`With value: "${withValue}"\n`);

// Example 9: Partials (Includes)
console.log('9. Partials (Includes)');
console.log('----------------------');
const partials = {
    header: '<header><h1>{{ title }}</h1></header>',
    footer: '<footer>Copyright {{ year }}</footer>'
};

const pageTemplate = `{% include "header" %}
<main>Welcome to {{ site }}</main>
{% include "footer" %}`;

const pageResult = renderTemplate(pageTemplate, { title: 'My Site', site: 'example.com', year: 2024 }, partials);
console.log(pageResult);
console.log();

// Example 10: Custom Filters
console.log('10. Custom Filters');
console.log('------------------');
const engine = new TemplateEngine();
engine.registerFilter('double', (n: number) => n * 2);
engine.registerFilter('exclaim', (s: string) => s + '!!!');

const customResult = engine.render('{{ num | double }} and {{ text | exclaim }}', { num: 21, text: 'hello' });
console.log(`Custom filters result: "${customResult}"\n`);

// Example 11: Nested Objects
console.log('11. Nested Objects');
console.log('------------------');
const nestedTemplate = `User: {{ user.name }}
Email: {{ user.email }}
City: {{ user.address.city }}`;

const nestedContext = {
    user: {
        name: 'Alice',
        email: 'alice@example.com',
        address: {
            city: 'New York',
            country: 'USA'
        }
    }
};

const nestedResult = renderTemplate(nestedTemplate, nestedContext);
console.log(nestedResult);
console.log();

// Example 12: Comments
console.log('12. Comments');
console.log('------------');
const withComments = renderTemplate('Hello {# this is ignored #} World', {});
console.log(`Template with comments: "${withComments}"\n`);

// Example 13: Comparison Operators
console.log('13. Comparison Operators');
console.log('------------------------');
const eqResult = renderTemplate('{% if count == 5 %}Exactly five{% endif %}', { count: 5 });
console.log(`Equal: "${eqResult}"`);

const gtResult = renderTemplate('{% if count > 5 %}More than five{% endif %}', { count: 10 });
console.log(`Greater than: "${gtResult}"`);

const notResult = renderTemplate('{% if not user %}Guest{% endif %}', { user: '' });
console.log(`Not operator: "${notResult}"\n`);

// Example 14: URL Encoding
console.log('14. URL Encoding');
console.log('----------------');
const urlEncoded = renderTemplate('{{ text | url_encode }}', { text: 'hello world & more' });
console.log(`URL encoded: "${urlEncoded}"\n`);

// Example 15: Email Template Example
console.log('15. Email Template');
console.log('------------------');
const emailTemplate = `Subject: {{ subject | upper }}

Dear {{ user.name | title }},

Thank you for your order of {{ items | size }} items:
{% for item in items %}
- {{ item.name }} (x{{ item.quantity }}) - ${{ item.price }}
{% endfor %}

Total: ${{ total | round:2 }}

{% if discount > 0 %}
You saved ${{ discount | round:2 }}!
{% endif %}

Best regards,
The Team`;

const emailContext = {
    subject: 'order confirmation',
    user: { name: 'john doe' },
    items: [
        { name: 'Widget', quantity: 2, price: 29.99 },
        { name: 'Gadget', quantity: 1, price: 49.99 }
    ],
    total: 109.97,
    discount: 10.00
};

const emailResult = renderTemplate(emailTemplate, emailContext);
console.log(emailResult);

console.log('\n=== All Examples Complete ===');

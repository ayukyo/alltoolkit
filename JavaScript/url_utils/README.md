# URL Utilities for JavaScript

Zero-dependency URL parsing, manipulation, and validation utilities for JavaScript.

## Installation

```javascript
const urlUtils = require('./mod.js');
```

## Features

- **URL Parsing**: Parse URLs into structured components
- **Query String Handling**: Parse and build query strings with full encoding support
- **URL Building**: Construct URLs from components
- **URL Validation**: Validate URLs with customizable rules
- **Path Operations**: Join paths, get segments
- **URL Resolution**: Resolve relative URLs
- **URL Normalization**: Normalize URLs for comparison
- **Domain Operations**: Extract domain, TLD, subdomain
- **Query Manipulation**: Add, remove, update query parameters
- **File Information**: Extract filename and extension
- **URL Templates**: Build URLs from templates with parameter substitution
- **Zero Dependencies**: Pure JavaScript implementation

## API Reference

### Parsing & Building

#### `parse(url)`
Parse a URL into its components.

```javascript
const parsed = urlUtils.parse('https://user:pass@example.com:8080/path?key=value#hash');
// Returns: {
//   protocol: 'https',
//   username: 'user',
//   password: 'pass',
//   hostname: 'example.com',
//   port: '8080',
//   path: '/path',
//   query: { key: 'value' },
//   hash: 'hash',
//   origin: 'https://example.com:8080',
//   href: '...'
// }
```

#### `build(components)`
Build a URL from components.

```javascript
const url = urlUtils.build({
    protocol: 'https',
    hostname: 'example.com',
    path: '/api/users',
    query: { page: 1 }
});
// 'https://example.com/api/users?page=1'
```

### Query String Operations

#### `parseQuery(queryString)`
Parse a query string into an object.

```javascript
const params = urlUtils.parseQuery('?page=1&limit=10');
// { page: '1', limit: '10' }
```

#### `buildQuery(params, options)`
Build a query string from an object.

```javascript
const query = urlUtils.buildQuery({ a: 1, b: 2 });
// '?a=1&b=2'

// With options
const sorted = urlUtils.buildQuery({ z: 1, a: 2 }, { sort: true });
// '?a=2&z=1'
```

### Validation

#### `isValid(url, options)`
Check if a URL is valid.

```javascript
urlUtils.isValid('https://example.com'); // true
urlUtils.isValid('not a url'); // false

// Custom validation
urlUtils.isValid('ftp://example.com', { protocols: ['ftp'] }); // true
urlUtils.isValid('example.com', { requireProtocol: false }); // true
```

### Path Operations

#### `joinPaths(...parts)`
Join URL path segments.

```javascript
urlUtils.joinPaths('api', 'v1', 'users');
// 'api/v1/users'

// With full URL
urlUtils.joinPaths('https://example.com/', 'api', 'users');
// 'https://example.com/api/users'
```

#### `getPathSegments(url)`
Extract path segments.

```javascript
urlUtils.getPathSegments('https://example.com/api/v1/users/123');
// ['api', 'v1', 'users', '123']
```

### Resolution & Normalization

#### `resolve(base, relative)`
Resolve a URL against a base URL.

```javascript
urlUtils.resolve('https://example.com/page', '/api/data');
// 'https://example.com/api/data'
```

#### `normalize(url)`
Normalize a URL (lowercase hostname, remove default ports, sort query params).

```javascript
urlUtils.normalize('HTTPS://EXAMPLE.COM:443/path/?b=2&a=1');
// 'https://example.com/path/?a=1&b=2'
```

#### `toAbsolute(relative, base)`
Convert relative URL to absolute.

```javascript
urlUtils.toAbsolute('/api/users', 'https://example.com/dashboard');
// 'https://example.com/api/users'
```

### Domain Operations

#### `getDomain(url)`
Extract domain from URL.

```javascript
urlUtils.getDomain('https://blog.example.com:8080/path');
// 'blog.example.com'
```

#### `getTLD(url)`
Extract top-level domain.

```javascript
urlUtils.getTLD('https://example.co.uk');
// 'uk'
```

#### `getSubdomain(url)`
Extract subdomain.

```javascript
urlUtils.getSubdomain('https://api.v1.example.com');
// 'api.v1'
```

### Query Manipulation

#### `addQuery(url, params)`
Add or update query parameters.

```javascript
urlUtils.addQuery('https://example.com', { page: 1, limit: 20 });
// 'https://example.com/?page=1&limit=20'
```

#### `removeQuery(url, keys)`
Remove query parameters.

```javascript
urlUtils.removeQuery('https://example.com?a=1&b=2&c=3', ['b']);
// 'https://example.com/?a=1&c=3'
```

### File Information

#### `getExtension(url)`
Extract file extension from URL.

```javascript
urlUtils.getExtension('https://example.com/file.pdf');
// 'pdf'
```

#### `getFilename(url)`
Extract filename from URL.

```javascript
urlUtils.getFilename('https://example.com/docs/report.pdf');
// 'report.pdf'
```

### Comparison

#### `areEquivalent(url1, url2)`
Check if two URLs are equivalent after normalization.

```javascript
urlUtils.areEquivalent(
    'HTTPS://EXAMPLE.COM/path/?b=2&a=1',
    'https://example.com/path?a=1&b=2'
); // true
```

#### `isAbsolute(url)`
Check if URL is absolute.

```javascript
urlUtils.isAbsolute('https://example.com'); // true
urlUtils.isAbsolute('/path'); // false
```

#### `isRelative(url)`
Check if URL is relative.

```javascript
urlUtils.isRelative('/path'); // true
urlUtils.isRelative('https://example.com'); // false
```

### URL Templates

#### `fromTemplate(template, params)`
Build URL from template with parameter substitution.

```javascript
urlUtils.fromTemplate('/api/users/:id/posts/:postId', { id: '123', postId: '456' });
// '/api/users/123/posts/456'
```

#### `parseTemplate(template)`
Extract parameter names from a URL template.

```javascript
urlUtils.parseTemplate('/api/users/:userId/posts/:postId');
// ['userId', 'postId']
```

## Running Tests

```bash
node url_utils_test.js
```

## Examples

See `examples/usage_examples.js` for comprehensive usage examples.

## License

MIT
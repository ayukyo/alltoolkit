/**
 * URL Utilities - Usage Examples
 * Demonstrates all features of the url_utils module
 */

const urlUtils = require('./mod.js');

console.log('=== URL Utilities Usage Examples ===\n');

// ============================================================
// 1. URL Parsing
// ============================================================
console.log('--- 1. URL Parsing ---');

const parsedUrl = urlUtils.parse('https://user:pass@example.com:8080/api/users?id=123#profile');
console.log('Parsed URL:', JSON.stringify(parsedUrl, null, 2));
/*
{
  protocol: 'https',
  username: 'user',
  password: 'pass',
  hostname: 'example.com',
  port: '8080',
  path: '/api/users',
  query: { id: '123' },
  hash: 'profile',
  origin: 'https://example.com:8080',
  href: 'https://user:pass@example.com:8080/api/users?id=123#profile'
}
*/

// ============================================================
// 2. Query String Operations
// ============================================================
console.log('\n--- 2. Query String Operations ---');

// Parse query string
const queryParams = urlUtils.parseQuery('?page=1&limit=10&sort=name');
console.log('Parsed query:', queryParams);
// { page: '1', limit: '10', sort: 'name' }

// Parse query with duplicate keys
const duplicateQuery = urlUtils.parseQuery('tag=javascript&tag=nodejs&tag=tutorial');
console.log('Duplicate keys become array:', duplicateQuery);
// { tag: ['javascript', 'nodejs', 'tutorial'] }

// Build query string
const builtQuery = urlUtils.buildQuery({ name: 'John Doe', age: '30', active: 'true' });
console.log('Built query:', builtQuery);
// ?name=John%20Doe&age=30&active=true

// Build sorted query
const sortedQuery = urlUtils.buildQuery({ z: 'last', a: 'first', m: 'middle' }, { sort: true });
console.log('Sorted query:', sortedQuery);
// ?a=first&m=middle&z=last

// ============================================================
// 3. URL Building
// ============================================================
console.log('\n--- 3. URL Building ---');

const builtUrl = urlUtils.build({
    protocol: 'https',
    hostname: 'api.example.com',
    port: '443',
    path: '/v1/users',
    query: { page: '1', limit: '20' },
    hash: 'results'
});
console.log('Built URL:', builtUrl);
// https://api.example.com:443/v1/users?page=1&limit=20#results

// ============================================================
// 4. URL Validation
// ============================================================
console.log('\n--- 4. URL Validation ---');

console.log('Valid HTTPS:', urlUtils.isValid('https://example.com')); // true
console.log('Valid HTTP:', urlUtils.isValid('http://example.com'));   // true
console.log('Invalid URL:', urlUtils.isValid('not a url'));          // false
console.log('Invalid protocol:', urlUtils.isValid('ftp://example.com')); // false
console.log('Custom protocol:', urlUtils.isValid('ftp://example.com', { protocols: ['ftp'] })); // true
console.log('URL without protocol:', urlUtils.isValid('example.com', { requireProtocol: false })); // true

// ============================================================
// 5. Path Operations
// ============================================================
console.log('\n--- 5. Path Operations ---');

// Join paths
console.log('Join paths:', urlUtils.joinPaths('api', 'v1', 'users'));
// api/v1/users

// Join paths with full URL
console.log('Join with URL:', urlUtils.joinPaths('https://example.com/', 'api', 'users'));
// https://example.com/api/users

// Get path segments
const segments = urlUtils.getPathSegments('https://example.com/api/v1/users/123');
console.log('Path segments:', segments);
// ['api', 'v1', 'users', '123']

// ============================================================
// 6. URL Resolution
// ============================================================
console.log('\n--- 6. URL Resolution ---');

const resolved = urlUtils.resolve('https://example.com/page', '../api/data');
console.log('Resolved URL:', resolved);
// https://example.com/api/data

const absolute = urlUtils.toAbsolute('/api/users', 'https://example.com/dashboard');
console.log('To absolute:', absolute);
// https://example.com/api/users

// ============================================================
// 7. URL Normalization
// ============================================================
console.log('\n--- 7. URL Normalization ---');

const normalized = urlUtils.normalize('HTTPS://EXAMPLE.COM:443/path/?b=2&a=1');
console.log('Normalized URL:', normalized);
// https://example.com/path/?a=1&b=2

// ============================================================
// 8. Domain Operations
// ============================================================
console.log('\n--- 8. Domain Operations ---');

const url = 'https://blog.api.example.co.uk:8080/posts';

console.log('Domain:', urlUtils.getDomain(url));
// blog.api.example.co.uk

console.log('TLD:', urlUtils.getTLD(url));
// uk

console.log('Subdomain:', urlUtils.getSubdomain(url));
// blog.api

// ============================================================
// 9. Query Parameter Manipulation
// ============================================================
console.log('\n--- 9. Query Parameter Manipulation ---');

// Add query parameters
const withNewQuery = urlUtils.addQuery('https://example.com/search', { q: 'test', page: '1' });
console.log('With added query:', withNewQuery);
// https://example.com/search?q=test&page=1

// Update existing parameter
const updatedQuery = urlUtils.addQuery('https://example.com?page=1', { page: '2', limit: '10' });
console.log('Updated query:', updatedQuery);
// https://example.com/?page=2&limit=10

// Remove query parameters
const removedQuery = urlUtils.removeQuery('https://example.com?a=1&b=2&c=3', ['b']);
console.log('With removed query:', removedQuery);
// https://example.com/?a=1&c=3

// ============================================================
// 10. File Information
// ============================================================
console.log('\n--- 10. File Information ---');

const fileUrl = 'https://example.com/documents/report.pdf?v=2';

console.log('Extension:', urlUtils.getExtension(fileUrl));
// pdf

console.log('Filename:', urlUtils.getFilename(fileUrl));
// report.pdf

// ============================================================
// 11. URL Comparison
// ============================================================
console.log('\n--- 11. URL Comparison ---');

const url1 = 'HTTPS://EXAMPLE.COM/path/?b=2&a=1';
const url2 = 'https://example.com/path/?a=1&b=2';

console.log('Are equivalent:', urlUtils.areEquivalent(url1, url2));
// true

// ============================================================
// 12. URL Templates
// ============================================================
console.log('\n--- 12. URL Templates ---');

// Parse template parameters
const templateParams = urlUtils.parseTemplate('/api/users/:userId/posts/:postId');
console.log('Template params:', templateParams);
// ['userId', 'postId']

// Build URL from template
const templateUrl = urlUtils.fromTemplate('/api/users/:userId/posts/:postId', {
    userId: '123',
    postId: '456'
});
console.log('Built from template:', templateUrl);
// /api/users/123/posts/456

// ============================================================
// 13. Practical Use Cases
// ============================================================
console.log('\n--- 13. Practical Use Cases ---');

// API Request URL Builder
function buildApiUrl(baseUrl, endpoint, params = {}) {
    return urlUtils.addQuery(urlUtils.joinPaths(baseUrl, endpoint), params);
}

const apiUrl = buildApiUrl('https://api.example.com', '/v1/users', {
    page: 1,
    limit: 20,
    sort: 'created_at'
});
console.log('API URL:', apiUrl);

// URL Comparison for Caching
function isSameResource(url1, url2) {
    // Normalize and compare - useful for caching
    return urlUtils.areEquivalent(url1, url2);
}

console.log('Same resource:', isSameResource(
    'https://api.example.com/users?page=1',
    'https://API.EXAMPLE.COM/users/?page=1'
));

// Extract Resource ID from URL Path
function extractResourceId(url) {
    const segments = urlUtils.getPathSegments(url);
    return segments[segments.length - 1] || null;
}

console.log('Resource ID:', extractResourceId('https://api.example.com/users/123'));
// 123

// Build Pagination URLs
function buildPaginationLinks(baseUrl, currentPage, totalPages) {
    const links = {
        first: urlUtils.addQuery(baseUrl, { page: 1 }),
        last: urlUtils.addQuery(baseUrl, { page: totalPages })
    };
    
    if (currentPage > 1) {
        links.prev = urlUtils.addQuery(baseUrl, { page: currentPage - 1 });
    }
    if (currentPage < totalPages) {
        links.next = urlUtils.addQuery(baseUrl, { page: currentPage + 1 });
    }
    
    return links;
}

const pagination = buildPaginationLinks('https://api.example.com/users', 3, 10);
console.log('Pagination links:', pagination);

// Clean and Normalize User-Input URLs
function cleanUserUrl(userInput) {
    if (!userInput) return null;
    
    // Add protocol if missing
    let url = userInput.trim();
    if (!urlUtils.isAbsolute(url)) {
        url = 'https://' + url;
    }
    
    // Validate
    if (!urlUtils.isValid(url)) {
        return null;
    }
    
    // Normalize
    return urlUtils.normalize(url);
}

console.log('Cleaned URL:', cleanUserUrl('EXAMPLE.COM/path/'));
// https://example.com/path

console.log('\n=== Examples Complete ===');
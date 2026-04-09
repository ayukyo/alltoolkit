/**
 * String Utils - Encoding Examples
 * 
 * Demonstrates Base64, URL encoding, and other transformations.
 */

import {
  toBase64,
  fromBase64,
  toBase64Url,
  fromBase64Url,
  encodeUrl,
  decodeUrl,
  escapeJson,
  unescapeJson,
  escapeHtml,
  unescapeHtml,
  escapeXml,
  escapeSql,
} from '../mod.ts';

console.log('📝 String Utils - Encoding Examples\n');
console.log('=' .repeat(50));

// Base64 Encoding
console.log('\n1️⃣  Base64 Encoding:');
console.log('-' .repeat(30));

const originalText = 'Hello, World! 你好，世界！';
const base64Encoded = toBase64(originalText);
const base64Decoded = fromBase64(base64Encoded);

console.log(`Original:  ${originalText}`);
console.log(`Base64:    ${base64Encoded}`);
console.log(`Decoded:   ${base64Decoded}`);
console.log(`Match:     ${originalText === base64Decoded ? '✅' : '❌'}`);

// URL-safe Base64
console.log('\n2️⃣  URL-safe Base64:');
console.log('-' .repeat(30));

const binaryLike = 'Data with + / and = characters';
const base64Std = toBase64(binaryLike);
const base64UrlSafe = toBase64Url(binaryLike);
const base64UrlDecoded = fromBase64Url(base64UrlSafe);

console.log(`Original:     ${binaryLike}`);
console.log(`Standard:     ${base64Std}`);
console.log(`URL-safe:     ${base64UrlSafe}`);
console.log(`No + or /:    ${!base64UrlSafe.includes('+') && !base64UrlSafe.includes('/') ? '✅' : '❌'}`);
console.log(`No padding:   ${!base64UrlSafe.includes('=') ? '✅' : '❌'}`);
console.log(`Decoded:      ${base64UrlDecoded}`);

// Use case: JWT-like tokens
console.log('\n3️⃣  Token Generation (JWT-like):');
console.log('-' .repeat(30));

const payload = {
  userId: 12345,
  username: 'john_doe',
  role: 'admin',
};

const payloadJson = JSON.stringify(payload);
const payloadBase64 = toBase64Url(payloadJson);

console.log(`Payload:     ${payloadJson}`);
console.log(`Token:       ${payloadBase64}`);
console.log(`Token Length: ${payloadBase64.length} chars`);

// URL Encoding
console.log('\n4️⃣  URL Encoding:');
console.log('-' .repeat(30));

const searchQuery = 'TypeScript & JavaScript comparison';
const urlEncoded = encodeUrl(searchQuery);
const urlDecoded = decodeUrl(urlEncoded);

console.log(`Original:  ${searchQuery}`);
console.log(`Encoded:   ${urlEncoded}`);
console.log(`Decoded:   ${urlDecoded}`);

// Build a search URL
const baseUrl = 'https://example.com/search';
const fullUrl = `${baseUrl}?q=${urlEncoded}&lang=ts`;
console.log(`\nFull URL:  ${fullUrl}`);

// JSON Escaping
console.log('\n5️⃣  JSON Escaping:');
console.log('-' .repeat(30));

const specialChars = 'Line 1\nLine 2\tTabbed"Quoted\\Backslash';
const jsonEscaped = escapeJson(specialChars);
const jsonUnescaped = unescapeJson(jsonEscaped);

console.log(`Original:  ${JSON.stringify(specialChars)}`);
console.log(`Escaped:   ${jsonEscaped}`);
console.log(`Unescaped: ${JSON.stringify(jsonUnescaped)}`);
console.log(`Match:     ${specialChars === jsonUnescaped ? '✅' : '❌'}`);

// Embed in JSON
const data = {
  message: specialChars,
  escaped: jsonEscaped,
};
console.log(`\nJSON Object:`);
console.log(JSON.stringify(data, null, 2));

// HTML Escaping (XSS Prevention)
console.log('\n6️⃣  HTML Escaping (XSS Prevention):');
console.log('-' .repeat(30));

const maliciousInputs = [
  '<script>alert("XSS")</script>',
  '<img src=x onerror=alert(1)>',
  'javascript:alert(1)',
  '" onclick="alert(1)',
  'Tom & Jerry <cats>',
];

console.log('Malicious Input → Escaped Output:\n');
maliciousInputs.forEach(input => {
  const escaped = escapeHtml(input);
  console.log(`Input:   ${input}`);
  console.log(`Escaped: ${escaped}`);
  console.log(`Safe:    ${!escaped.includes('<script') && !escaped.includes('onerror') ? '✅' : '⚠️'}`);
  console.log();
});

// Safe HTML rendering example
console.log('Safe HTML Output:');
const userInput = '<b>Bold</b> & <i>Italic</i>';
const safeOutput = escapeHtml(userInput);
console.log(`User Input:  ${userInput}`);
console.log(`Safe Output: ${safeOutput}`);
console.log(`Rendered:    &lt;b&gt;Bold&lt;/b&gt; &amp; &lt;i&gt;Italic&lt;/i&gt;`);

// XML Escaping
console.log('\n7️⃣  XML Escaping:');
console.log('-' .repeat(30));

const xmlContent = 'Tom & Jerry\'s "adventures" <in> the park';
const xmlEscaped = escapeXml(xmlContent);

console.log(`Original:  ${xmlContent}`);
console.log(`Escaped:   ${xmlEscaped}`);
console.log(`XML Safe:  ${!xmlEscaped.includes('&') || xmlEscaped.includes('&amp;') ? '✅' : '❌'}`);

// Build XML element
const xmlElement = `<message>${xmlEscaped}</message>`;
console.log(`\nXML Element:\n${xmlElement}`);

// SQL Escaping (Basic)
console.log('\n8️⃣  SQL Escaping (Basic Protection):');
console.log('-' .repeat(30));

const sqlInputs = [
  "O'Reilly",
  "Robert'); DROP TABLE users; --",
  "admin'--",
  "1' OR '1'='1",
];

console.log('SQL Injection Prevention:\n');
sqlInputs.forEach(input => {
  const escaped = escapeSql(input);
  console.log(`Input:    ${input}`);
  console.log(`Escaped:  ${escaped}`);
  console.log(`Query:    SELECT * FROM users WHERE name='${escaped}'`);
  console.log();
});

console.log('⚠️  Note: escapeSql provides basic protection only.');
console.log('   For production, use parameterized queries!\n');

// Real-world Example: API Request Builder
console.log('9️⃣  Real-world Example - API Request Builder:');
console.log('-' .repeat(30));

interface ApiRequest {
  endpoint: string;
  params: Record<string, string>;
  body?: Record<string, unknown>;
}

function buildApiRequest(request: ApiRequest): {
  url: string;
  options: RequestInit;
} {
  // Build query string
  const queryString = Object.entries(request.params)
    .map(([key, value]) => `${encodeUrl(key)}=${encodeUrl(value)}`)
    .join('&');
  
  const url = queryString 
    ? `${request.endpoint}?${queryString}`
    : request.endpoint;
  
  // Build body
  const options: RequestInit = {
    method: request.body ? 'POST' : 'GET',
    headers: {
      'Content-Type': 'application/json',
    },
  };
  
  if (request.body) {
    // Escape any string values in the body
    const escapedBody = JSON.stringify(request.body, (key, value) => {
      if (typeof value === 'string') {
        return escapeJson(value);
      }
      return value;
    });
    options.body = escapedBody;
  }
  
  return { url, options };
}

const apiRequest: ApiRequest = {
  endpoint: 'https://api.example.com/users',
  params: {
    search: 'John & Jane',
    filter: '<active>',
  },
  body: {
    username: "O'Connor",
    bio: 'Developer\nEngineer\t"Expert"',
  },
};

const { url, options } = buildApiRequest(apiRequest);

console.log('Request Configuration:');
console.log(`URL:     ${url}`);
console.log(`Method:  ${options.method}`);
console.log(`Body:    ${options.body}`);

console.log('\n' + '=' .repeat(50));
console.log('✅ Examples completed!\n');

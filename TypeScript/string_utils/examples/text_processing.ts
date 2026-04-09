/**
 * String Utils - Text Processing Examples
 * 
 * Demonstrates text extraction, analysis, and transformation.
 */

import {
  extractUrls,
  extractEmails,
  extractHashtags,
  extractMentions,
  extractNumbers,
  extractBetween,
  analyzeChars,
  countOccurrences,
  removeSpecialChars,
  removeWhitespace,
  escapeHtml,
  unescapeHtml,
} from '../mod.ts';

console.log('📝 String Utils - Text Processing Examples\n');
console.log('=' .repeat(50));

// Text Extraction
console.log('\n1️⃣  Text Extraction:');
console.log('-' .repeat(30));

const socialMediaPost = `
  Check out our new product at https://example.com/product!
  Contact us at support@example.com or sales@example.com.
  Call us at 123-456-7890 or (555) 987-6543.
  
  #NewProduct #Launch #Tech #Innovation
  
  Thanks to @john_doe and @jane_smith for their help!
  
  Rating: 4.5/5 stars from 128 reviews.
`;

console.log('Social Media Post:');
console.log(socialMediaPost);

console.log('\nExtracted Data:');
console.log(`  URLs:       ${JSON.stringify(extractUrls(socialMediaPost))}`);
console.log(`  Emails:     ${JSON.stringify(extractEmails(socialMediaPost))}`);
console.log(`  Hashtags:   ${JSON.stringify(extractHashtags(socialMediaPost))}`);
console.log(`  Mentions:   ${JSON.stringify(extractMentions(socialMediaPost))}`);
console.log(`  Numbers:    ${JSON.stringify(extractNumbers(socialMediaPost))}`);
console.log(`  Floats:     ${JSON.stringify(extractNumbers(socialMediaPost, true))}`);

// Text Between Delimiters
console.log('\n2️⃣  Extract Between Delimiters:');
console.log('-' .repeat(30));

const htmlContent = `
  <div class="content">
    <title>Page Title</title>
    <p>First paragraph</p>
    <p>Second paragraph</p>
  </div>
`;

const titles = extractBetween(htmlContent, '<title>', '</title>');
const paragraphs = extractBetween(htmlContent, '<p>', '</p>');

console.log('HTML Content:');
console.log(`  Titles:      ${JSON.stringify(titles)}`);
console.log(`  Paragraphs:  ${JSON.stringify(paragraphs)}`);

// Character Analysis
console.log('\n3️⃣  Character Analysis:');
console.log('-' .repeat(30));

const sampleText = 'Hello, World! 你好世界！123';
const analysis = analyzeChars(sampleText);

console.log(`Text: "${sampleText}"`);
console.log(`  Total:        ${analysis.total}`);
console.log(`  Letters:      ${analysis.letters}`);
console.log(`  Digits:       ${analysis.digits}`);
console.log(`  Spaces:       ${analysis.spaces}`);
console.log(`  Punctuation:  ${analysis.punctuation}`);
console.log(`  Uppercase:    ${analysis.uppercase}`);
console.log(`  Lowercase:    ${analysis.lowercase}`);
console.log(`  Unicode:      ${analysis.unicode}`);

// Text Cleaning
console.log('\n4️⃣  Text Cleaning:');
console.log('-' .repeat(30));

const dirtyText = '  Hello!   World@123#  \n\t  ';
console.log(`Original:  "${dirtyText}"`);
console.log(`  Trimmed:        "${dirtyText.trim()}"`);
console.log(`  No Special:     "${removeSpecialChars(dirtyText)}"`);
console.log(`  No Whitespace:  "${removeWhitespace(dirtyText)}"`);

// Count Occurrences
console.log('\n5️⃣  Count Occurrences:');
console.log('-' .repeat(30));

const longText = 'The quick brown fox jumps over the lazy dog. The fox was quick.';
const word = 'fox';
const count = countOccurrences(longText, word, false);

console.log(`Text: "${longText}"`);
console.log(`Word "${word}" appears ${count} times (case-insensitive)`);

// HTML Escaping
console.log('\n6️⃣  HTML Escaping (XSS Prevention):');
console.log('-' .repeat(30));

const userInput = '<script>alert("XSS Attack!")</script>';
const safeHtml = escapeHtml(userInput);

console.log(`User Input:  ${userInput}`);
console.log(`Escaped:     ${safeHtml}`);
console.log(`Unescaped:   ${unescapeHtml(safeHtml)}`);

// Real-world Example: Content Moderation
console.log('\n7️⃣  Real-world Example - Content Moderation:');
console.log('-' .repeat(30));

interface PostMetrics {
  urlCount: number;
  emailCount: number;
  hashtagCount: number;
  mentionCount: number;
  isSpam: boolean;
}

function analyzePost(content: string): PostMetrics {
  const urls = extractUrls(content);
  const emails = extractEmails(content);
  const hashtags = extractHashtags(content);
  const mentions = extractMentions(content);
  
  // Simple spam detection: too many URLs or emails
  const isSpam = urls.length > 3 || emails.length > 2;
  
  return {
    urlCount: urls.length,
    emailCount: emails.length,
    hashtagCount: hashtags.length,
    mentionCount: mentions.length,
    isSpam,
  };
}

const testPosts = [
  'Check out my photo! #photography',
  'Buy now at http://spam.com! Contact spam@spam.com',
  'Great article https://news.com @author #news',
];

testPosts.forEach((post, index) => {
  const metrics = analyzePost(post);
  console.log(`\nPost ${index + 1}: "${post.slice(0, 40)}..."`);
  console.log(`  URLs: ${metrics.urlCount}, Emails: ${metrics.emailCount}`);
  console.log(`  Hashtags: ${metrics.hashtagCount}, Mentions: ${metrics.mentionCount}`);
  console.log(`  Spam: ${metrics.isSpam ? '⚠️ Yes' : '✅ No'}`);
});

console.log('\n' + '=' .repeat(50));
console.log('✅ Examples completed!\n');

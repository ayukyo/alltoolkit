# slug_utils - URL-Friendly Slug Generation Module

**JavaScript Slug Utilities - Zero Dependencies, Production Ready**

---

## 📖 Overview

`slug_utils` is a comprehensive JavaScript module for generating URL-friendly slugs. It provides features like multi-language transliteration, custom separators, case conversion, stopword removal, and more. Zero external dependencies - uses only built-in JavaScript APIs.

### ✨ Features

- **Zero Dependencies** - Pure JavaScript, no external libraries
- **Multi-Language Support** - Chinese, Japanese, Korean, Russian, Arabic, Thai, Vietnamese, and more
- **Custom Separators** - Configure separator character (-, _, ., etc.)
- **Case Options** - Preserve case or convert to lowercase
- **Stopword Removal** - Optional removal of common stopwords
- **Max Length** - Automatic truncation at word boundaries
- **Unique Slug Generation** - Automatically resolve collisions
- **Validation** - Full slug validation with detailed error messages
- **TypeScript Ready** - JSDoc annotations for IDE support

---

## 📦 Installation

No installation needed! Just copy `mod.js` to your project.

```bash
# Clone the repository
git clone https://github.com/ayukyo/alltoolkit.git

# Or copy directly
cp alltoolkit/JavaScript/slug_utils/mod.js your_project/
```

---

## 🚀 Quick Start

```javascript
const { slugify, validateSlug, uniqueSlugify } = require('./mod.js');

// Basic usage
slugify('Hello World!');
// Output: 'hello-world'

// Custom separator
slugify('Hello World', '_');
// Output: 'hello_world'

// Preserve case
slugify('Hello World', { lowercase: false });
// Output: 'Hello-World'

// Chinese characters
slugify('你好世界');
// Output: 'ni-hao-shi-jie'
```

---

## 📚 API Reference

### Core Functions

#### `slugify(text, options?)`

Generate a URL-friendly slug from text.

```javascript
// Basic
slugify('Hello World!')           // 'hello-world'

// Custom separator
slugify('Hello World', '_')        // 'hello_world'
slugify('Hello World', { separator: '.' }) // 'hello.world'

// Preserve case
slugify('Hello World', { lowercase: false }) // 'Hello-World'

// Max length with word boundary truncation
slugify('Hello World Example', { maxLength: 11 }) // 'hello-worl'

// Remove stopwords
slugify('The Hello World', { removeStopwords: true }) // 'hello-world'

// Custom replacements
slugify('C++ Programming', { customReplacements: { 'C++': 'cpp' } })
// Output: 'cpp-programming'

// Strict mode (removes all non-word chars)
slugify('file.txt', { strict: true }) // 'filetxt'
```

**Options:**

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `separator` | string | `-` | Separator character |
| `lowercase` | boolean | `true` | Convert to lowercase |
| `maxLength` | number | `null` | Maximum slug length |
| `trim` | boolean | `true` | Trim leading/trailing separators |
| `removeStopwords` | boolean | `false` | Remove common stopwords |
| `stopwords` | string[] | `['a', 'an', 'the', ...]` | Custom stopwords list |
| `strict` | boolean | `false` | Remove all non-word characters |
| `customReplacements` | object | `{}` | Custom character replacements |

---

#### `validateSlug(slug, options?)`

Validate a slug and return validation result.

```javascript
const result = validateSlug('hello-world');
// { valid: true, errors: [] }

const invalid = validateSlug('-hello');
// { valid: false, errors: ['Slug should not start with separators'] }

const tooLong = validateSlug('a'.repeat(300), { maxLength: 255 });
// { valid: false, errors: ['Slug exceeds maximum length of 255 characters'] }
```

---

#### `uniqueSlugify(text, isUnique, options?)`

Generate a unique slug, appending numbers to avoid collisions.

```javascript
// Synchronous
const existingSlugs = ['hello-world', 'hello-world-2'];
const isUnique = (slug) => !existingSlugs.includes(slug);
uniqueSlugifySync('Hello World', isUnique);
// Output: 'hello-world-3'

// Asynchronous
const isUniqueAsync = async (slug) => !existingSlugs.includes(slug);
await uniqueSlugify('Hello World', isUniqueAsync);
// Output: 'hello-world-3'
```

---

#### `unslugify(slug, options?)`

Convert a slug back to a readable title.

```javascript
unslugify('hello-world')           // 'Hello World'
unslugify('hello_world', { separator: '_' }) // 'Hello World'
```

---

#### `extractSlugs(text, options?)`

Extract slug-like strings from text.

```javascript
extractSlugs('Check out hello-world and amazing-post')
// ['hello-world', 'amazing-post']
```

---

#### `joinSlug(...parts)`

Create a slug from multiple parts.

```javascript
joinSlug('Hello', 'World')         // 'hello-world'
joinSlug(['foo', 'bar'], 'baz')    // 'foo-bar-baz'
```

---

#### `parseSlug(slug, options?)`

Parse a slug into its component parts.

```javascript
parseSlug('hello-world')           // ['hello', 'world']
parseSlug('foo_bar_baz', { separator: '_' }) // ['foo', 'bar', 'baz']
```

---

## 🌍 Multi-Language Support

```javascript
// Chinese
slugify('你好世界')           // 'ni-hao-shi-jie'
slugify('北京')               // 'bei-jing'

// Japanese
slugify('こんにちは')         // 'konnichiwa'
slugify('東京')               // 'dong-jing'

// Korean
slugify('안녕하세요')         // 'annyeonghaseyo'
slugify('서울')               // 'seoul'

// Russian
slugify('Привет мир')        // 'privet-mir'

// French
slugify('Café')              // 'cafe'
slugify('ça va')             // 'ca-va'

// German
slugify('München')           // 'munchen'
slugify('Über')              // 'uber'

// Spanish
slugify('España')           // 'espana'
slugify('¿Qué tal?')        // 'que-tal'

// Vietnamese
slugify('Xin chào')         // 'xin-chao'
slugify('Tiếng Việt')       // 'tieng-viet'

// Arabic
slugify('مرحبا')            // 'marhaba'

// Thai
slugify('สวัสดี')           // 'sawatdi'
```

---

## 🧪 Running Tests

```bash
cd JavaScript/slug_utils
node slug_utils_test.js
```

---

## 📄 License

MIT License - feel free to use in any project.

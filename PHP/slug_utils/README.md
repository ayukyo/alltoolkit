# Slug Utils - PHP

URL-friendly slug generation utilities for PHP. Zero external dependencies.

## Features

- 🌍 **International Support** - Transliteration for 20+ languages (Latin, Cyrillic, Greek, Chinese, Japanese, Arabic, Hebrew, etc.)
- 🔧 **Customizable** - Configurable separators, length limits, and lowercase handling
- ✅ **Validation** - Validate and sanitize existing slugs
- 🔄 **Conversion** - Convert slugs to title case, camelCase, snake_case
- 📊 **Comparison** - Calculate similarity between slugs
- 🎯 **Unique Generation** - Generate unique slugs with numeric suffixes
- ⚡ **Helper Functions** - Quick functions for common use cases

## Installation

Copy the `slug_utils.php` file to your project and include it:

```php
require_once 'slug_utils.php';
```

## Quick Start

```php
use SlugUtils\SlugGenerator;
use SlugUtils\SlugHelper;

// Using the generator
$generator = new SlugGenerator();
echo $generator->generate('Hello World!'); // hello-world

// Using helper functions
echo SlugHelper::slug('My Blog Post Title!'); // my-blog-post-title
```

## Usage

### Basic Slug Generation

```php
$generator = new SlugGenerator();

$generator->generate('Hello World');           // hello-world
$generator->generate('PHP & MySQL Tutorial');  // php-mysql-tutorial
$generator->generate('Café Français');         // cafe-francais
$generator->generate('Привет мир');            // privet-mir
```

### Custom Configuration

```php
// Underscore separator
$generator = new SlugGenerator(['separator' => '_']);
$generator->generate('Hello World'); // hello_world

// Max length
$generator = new SlugGenerator(['max_length' => 20]);
$generator->generate('Very Long Title Here'); // very-long-title

// Reserved words
$generator = new SlugGenerator(['reserved_words' => ['admin', 'root']]);
$generator->generate('Admin'); // admin-1
```

### Unique Slugs

```php
$generator = new SlugGenerator();
$existing = ['my-post', 'my-post-1'];

$slug = $generator->generateUnique('My Post', $existing);
// Returns: my-post-2
```

### Validation & Sanitization

```php
$generator = new SlugGenerator();

// Validation
$generator->isValid('hello-world');  // true
$generator->isValid('Hello World');   // false

// Sanitization
$generator->sanitize('--hello---world--'); // hello-world
```

### Slug Conversion

```php
$generator = new SlugGenerator();
$slug = 'hello-world';

$generator->toTitle($slug);     // Hello World
$generator->toCamelCase($slug); // helloWorld
$generator->toSnakeCase($slug); // hello_world
$generator->parse($slug);       // ['hello', 'world']
```

### Helper Functions

```php
// Quick slug
SlugHelper::slug('Hello World!'); // hello-world

// Underscore separator
SlugHelper::underscore('Variable Name'); // variable_name

// Filename generation
SlugHelper::filename('My Document', 'pdf'); // my-document.pdf

// Blog post slug (SEO optimized, max 60 chars)
SlugHelper::titleSlug('Long Blog Post Title Here...'); // long-blog-post-title

// Product slug with SKU
SlugHelper::productSlug('Wireless Headphones', 'WH-123'); // wireless-headphones-wh-123

// Username (avoids reserved words)
SlugHelper::usernameSlug('Admin'); // admin-1

// Random ID
SlugHelper::id('user'); // user-a7b2c9d1
```

## Supported Languages

| Language   | Example Input | Output     |
|------------|---------------|------------|
| French     | Café Français | cafe-francais |
| German     | Grüße         | grusse     |
| Spanish    | Niño          | nino       |
| Portuguese | Coração       | coracao    |
| Russian    | Привет        | privet     |
| Greek      | Γειά          | geia       |
| Chinese    | 你好          | ni-hao     |
| Japanese   | こんにちは    | konnichiha |
| Arabic     | مرحبا         | mrhba      |
| Hebrew     | שלום          | slm        |

## API Reference

### SlugGenerator Class

| Method | Description |
|--------|-------------|
| `generate(string $text)` | Generate a slug from text |
| `generateUnique(string $text, array $existing)` | Generate unique slug avoiding conflicts |
| `generateFromParts(array $parts)` | Generate slug from multiple parts |
| `generateWithTimestamp(string $text, ?string $ts)` | Generate slug with date suffix |
| `generateWithRandomSuffix(string $text, int $length)` | Generate slug with random suffix |
| `isValid(string $slug)` | Check if slug is valid |
| `sanitize(string $slug)` | Clean up malformed slug |
| `toTitle(string $slug)` | Convert to title case |
| `toCamelCase(string $slug)` | Convert to camelCase |
| `toSnakeCase(string $slug)` | Convert to snake_case |
| `parse(string $slug)` | Split slug into word array |
| `similarity(string $a, string $b)` | Calculate similarity (0.0-1.0) |

### SlugHelper Class

| Method | Description |
|--------|-------------|
| `slug(string $text)` | Quick slug with defaults |
| `underscore(string $text)` | Slug with underscore separator |
| `filename(string $text, string $ext)` | Generate safe filename |
| `id(string $prefix, int $length)` | Generate random ID |
| `titleSlug(string $title, int $max)` | SEO-friendly blog slug |
| `productSlug(string $name, ?string $sku)` | E-commerce product slug |
| `usernameSlug(string $name)` | Safe username (avoids reserved) |

## Running Tests

```bash
php slug_utils_test.php
```

## Running Examples

```bash
php examples.php
```

## License

MIT License
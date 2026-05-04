# Pagination Utils (PHP)

A comprehensive PHP pagination library with zero dependencies. Supports offset-based, cursor-based, and GraphQL-style pagination with flexible output formats.

## Features

- ✅ **Offset-based pagination** - Classic page-based navigation
- ✅ **Cursor-based pagination** - Efficient for large datasets
- ✅ **GraphQL-style pagination** - First/After/Before/Last pattern
- ✅ **Infinite scroll helper** - For modern web apps
- ✅ **Bootstrap-compatible HTML** - Ready-to-use pagination UI
- ✅ **Query parameter preservation** - Keeps existing filters
- ✅ **Page validation** - Handles edge cases gracefully
- ✅ **Array slicing** - Direct data manipulation
- ✅ **Zero dependencies** - Pure PHP implementation

## Installation

```php
require_once 'Paginator.php';

use PaginationUtils\Paginator;
use PaginationUtils\CursorPaginator;
use PaginationUtils\InfiniteScroll;
use PaginationUtils\SimplePageInfo;
use PaginationUtils\PaginationHelper;
```

## Quick Start

### Basic Pagination

```php
// Create paginator: 100 items, 10 per page, current page 3
$paginator = new Paginator(100, 10, 3);

// Get offset and limit for SQL query
echo $paginator->getOffset(); // 20
echo $paginator->getLimit();  // 10

// Query: SELECT * FROM items LIMIT 10 OFFSET 20
```

### With HTML Output

```php
$paginator = new Paginator(100, 10, 5, '/products?page={page}');
echo $paginator->renderHtml(); // Bootstrap-style pagination

// Entry summary
echo $paginator->renderSummary(); // "Showing 41 to 50 of 100 entries"
```

### With Query Parameters

```php
$paginator = new Paginator(100, 10, 3, '/search?page={page}');
$paginator->setQueryParams(['q' => 'php', 'sort' => 'date']);
echo $paginator->getPageUrl(4); // /search?page=4&q=php&sort=date
```

## Usage

### Paginator Class

#### Constructor

```php
$paginator = new Paginator(
    int $totalItems,       // Total number of items
    int $itemsPerPage = 10, // Items per page
    int $currentPage = 1,   // Current page (1-indexed)
    string $urlPattern = '?page={page}' // URL with {page} placeholder
);
```

#### Core Methods

```php
// Pagination calculations
$paginator->getOffset();           // Offset for LIMIT/OFFSET
$paginator->getLimit();            // Items per page
$paginator->getCurrentPage();      // Current page number
$paginator->getTotalPages();       // Total number of pages

// Navigation
$paginator->hasPreviousPage();     // Check previous page exists
$paginator->hasNextPage();         // Check next page exists
$paginator->getPreviousPage();     // Previous page number (or null)
$paginator->getNextPage();         // Next page number (or null)

// URLs
$paginator->getPageUrl(5);         // Generate URL for page 5

// Item ranges
$paginator->getStartItemNumber();  // First item on page (1-indexed)
$paginator->getEndItemNumber();    // Last item on page

// Metadata
$paginator->getMetadata();         // Full pagination data array
```

#### Page Links

```php
// Get array of page numbers/ellipsis to display
$paginator->getPages();            // [1, 'ellipsis', 3, 4, 5, 'ellipsis', 10]

// Get detailed link structure
$paginator->getLinks();            // Array with type, url, text, active/disabled
```

#### Output Methods

```php
// Bootstrap 5 compatible HTML
$paginator->renderHtml([
    'ul_class' => 'pagination',
    'li_class' => 'page-item',
    'a_class' => 'page-link',
    'active_class' => 'active',
    'disabled_class' => 'disabled',
]);

// Summary text
$paginator->renderSummary('Showing {start}-{end} of {total}');
```

#### Utility Methods

```php
// Slice an array for current page
$paginator->slice($array);

// Set preserved query params
$paginator->setQueryParams(['category' => 'books']);

// Set navigation button text
$paginator->setNavTexts('Previous', 'Next');

// Set ellipsis text
$paginator->setEllipsisText('···');

// Create from request ($_GET)
$paginator = Paginator::fromRequest(100, 10, 'page', ['sort' => 'date']);
```

### CursorPaginator Class

For large datasets where counting total items is expensive.

```php
// Fetch items with LIMIT + 1 (e.g., 10 + 1 = 11) to detect hasMore
$items = fetchFromDatabase(11); // Fetch 11 items

$cursorPaginator = new CursorPaginator($items, 10);

// Get items for current page
$cursorPaginator->getItems();       // Returns 10 items

// Check for more
$cursorPaginator->hasNextPage();    // true if 11th item exists

// Get cursor for next page
$cursorPaginator->getNextCursor();  // Base64 encoded cursor

// Decode cursor from request
$decoded = CursorPaginator::decodeCursor($cursor);

// API response format
$cursorPaginator->toApiResponse(['request_id' => 'abc123']);
// Returns: { data: [...], pagination: { has_next, next_cursor, ... }, request_id: 'abc123' }
```

### InfiniteScroll Class

Helper for infinite scroll UI.

```php
$paginator = new Paginator(500, 20, 1);
$infinite = new InfiniteScroll($paginator);

// Check if more items available
$infinite->hasMore();               // true/false

// Get next page URL
$infinite->getNextUrl();

// Render load more button
$infinite->renderLoadMoreButton();

// Get data attributes for JS
$infinite->renderDataAttributes();
// data-has-more="true" data-next-url="/items?page=2"

// Customize text
$infinite->setLoadMoreText('Load More');
$infinite->setLoadingText('Loading...');
$infinite->setNoMoreText('No more items');
```

### SimplePageInfo Class

GraphQL-style pagination with cursors.

```php
$items = range(1, 50);

// Get first 10 items
$result = SimplePageInfo::create($items, 10);
// ['items' => [1..10], 'pageInfo' => ['hasNextPage' => true, 'endCursor' => '...', ...]]

// Get 5 items after cursor
$afterCursor = base64_encode('10');
$result = SimplePageInfo::create($items, 5, $afterCursor);
// ['items' => [11..15], ...]

// Get last 5 items
$result = SimplePageInfo::create($items, null, null, null, 5);
// ['items' => [46..50], ...]
```

### PaginationHelper Class

Utility functions.

```php
// Validate page number
PaginationHelper::validatePage(-5, 10);  // Returns 1
PaginationHelper::validatePage(15, 10);  // Returns 10

// Calculate offset and limit
PaginationHelper::calculateOffsetLimit(3, 10);
// ['offset' => 20, 'limit' => 10]

// Calculate total pages
PaginationHelper::calculateTotalPages(100, 10); // 10

// Generate page range
PaginationHelper::generatePageRange(5, 10, 2); // [3, 4, 5, 6, 7]

// Build URL
PaginationHelper::buildUrl('/items', 'page', 3, ['sort' => 'date']);
// /items?page=3&sort=date
```

## Complete Example

```php
<?php
require_once 'Paginator.php';
use PaginationUtils\Paginator;

// Get total count from database
$totalItems = 247;

// Create paginator from request
$paginator = Paginator::fromRequest($totalItems, 20);
$paginator->setQueryParams(['category' => 'electronics', 'sort' => 'price']);

// Build SQL query
$sql = "SELECT * FROM products 
        WHERE category = 'electronics' 
        ORDER BY price DESC 
        LIMIT {$paginator->getLimit()} OFFSET {$paginator->getOffset()}";

// Fetch items and display
$items = $db->query($sql)->fetchAll();

// Render pagination
echo '<h1>Products</h1>';
echo '<ul class="products">';
foreach ($items as $item) {
    echo '<li>' . $item['name'] . '</li>';
}
echo '</ul>';

echo $paginator->renderSummary();
echo $paginator->renderHtml();

// For API response
header('Content-Type: application/json');
echo json_encode([
    'data' => $items,
    'pagination' => $paginator->getMetadata(),
]);
```

## API Reference

### Paginator

| Method | Return Type | Description |
|--------|-------------|-------------|
| `getOffset()` | int | Database query offset |
| `getLimit()` | int | Database query limit |
| `getCurrentPage()` | int | Current page (1-indexed) |
| `getTotalPages()` | int | Total number of pages |
| `hasPreviousPage()` | bool | Previous page exists |
| `hasNextPage()` | bool | Next page exists |
| `getPreviousPage()` | int|null | Previous page number |
| `getNextPage()` | int|null | Next page number |
| `getStartItemNumber()` | int | First item number on page |
| `getEndItemNumber()` | int | Last item number on page |
| `getPageUrl(int $page)` | string | URL for given page |
| `getPages()` | array | Pages to display (with ellipsis) |
| `getLinks()` | array | Detailed link structure |
| `getMetadata()` | array | Full pagination metadata |
| `renderHtml(array $options)` | string | Bootstrap HTML |
| `renderSummary(string $template)` | string | Entry summary text |
| `slice(array $items)` | array | Slice array for current page |

### CursorPaginator

| Method | Return Type | Description |
|--------|-------------|-------------|
| `getItems()` | array | Items for current page |
| `hasNextPage()` | bool | Next page exists |
| `hasPreviousPage()` | bool | Previous page exists |
| `getNextCursor()` | string|null | Cursor for next page |
| `getPreviousCursor()` | string|null | Cursor for previous page |
| `getMetadata()` | array | Pagination metadata |
| `toApiResponse(array $data)` | array | API response format |
| `decodeCursor(string $cursor)` | array|null | Static: decode cursor |

## License

MIT License - Free for personal and commercial use.

## Part of AllToolkit

This module is part of the AllToolkit collection - zero-dependency utility libraries for multiple programming languages.
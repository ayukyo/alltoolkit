<?php

/**
 * Pagination Utils Usage Examples
 * 
 * This file demonstrates how to use the pagination utilities.
 * Run with: php examples.php
 * 
 * @package PaginationUtils
 */

require_once __DIR__ . '/Paginator.php';

use PaginationUtils\Paginator;
use PaginationUtils\CursorPaginator;
use PaginationUtils\InfiniteScroll;
use PaginationUtils\SimplePageInfo;
use PaginationUtils\PaginationHelper;

echo "=== Pagination Utils Examples ===\n\n";

// ============================================
// Example 1: Basic Offset Pagination
// ============================================
echo "--- Example 1: Basic Offset Pagination ---\n\n";

// Create a paginator for 100 items, 10 per page, on page 3
$paginator = new Paginator(100, 10, 3, '/products?page={page}');

// Get pagination metadata
echo "Metadata:\n";
print_r($paginator->getMetadata());

// Get offset and limit for database queries
echo "\nFor SQL query:\n";
echo "SELECT * FROM products LIMIT {$paginator->getLimit()} OFFSET {$paginator->getOffset()};\n";

// Get page URLs
echo "\nPage URLs:\n";
echo "First page: {$paginator->getPageUrl(1)}\n";
echo "Current page: {$paginator->getPageUrl(3)}\n";
echo "Next page: {$paginator->getPageUrl($paginator->getNextPage())}\n";

// ============================================
// Example 2: Generating Page Links
// ============================================
echo "\n--- Example 2: Generating Page Links ---\n\n";

$paginator = new Paginator(100, 10, 5, '/items?page={page}');
$paginator->setMaxPagesToShow(5);

echo "Pages to display: ";
print_r($paginator->getPages());

echo "\nFull link structure:\n";
foreach ($paginator->getLinks() as $link) {
    if ($link['type'] === 'ellipsis') {
        echo "  [{$link['text']}]\n";
    } else {
        $active = isset($link['active']) && $link['active'] ? '✓' : '';
        $disabled = isset($link['disabled']) && $link['disabled'] ? '✗' : '';
        echo "  {$link['type']}: {$link['url']} {$active}{$disabled}\n";
    }
}

// ============================================
// Example 3: HTML Pagination Output
// ============================================
echo "\n--- Example 3: HTML Pagination Output ---\n\n";

$paginator = new Paginator(100, 10, 5);
echo "Bootstrap-style pagination:\n";
echo $paginator->renderHtml();
echo "\n\n";

echo "Entry summary:\n";
echo $paginator->renderSummary();
echo "\n";

// ============================================
// Example 4: Preserving Query Parameters
// ============================================
echo "\n--- Example 4: Preserving Query Parameters ---\n\n";

$paginator = new Paginator(100, 10, 3, '/search?page={page}');
$paginator->setQueryParams([
    'q' => 'php pagination',
    'sort' => 'date',
    'category' => 'tutorials'
]);

echo "URL with preserved params:\n";
echo $paginator->getPageUrl(4);
echo "\n";

// ============================================
// Example 5: Array Slicing
// ============================================
echo "\n--- Example 5: Array Slicing ---\n\n";

$products = [
    ['id' => 1, 'name' => 'Product A', 'price' => 10],
    ['id' => 2, 'name' => 'Product B', 'price' => 20],
    ['id' => 3, 'name' => 'Product C', 'price' => 30],
    ['id' => 4, 'name' => 'Product D', 'price' => 40],
    ['id' => 5, 'name' => 'Product E', 'price' => 50],
    ['id' => 6, 'name' => 'Product F', 'price' => 60],
    ['id' => 7, 'name' => 'Product G', 'price' => 70],
    ['id' => 8, 'name' => 'Product H', 'price' => 80],
    ['id' => 9, 'name' => 'Product I', 'price' => 90],
    ['id' => 10, 'name' => 'Product J', 'price' => 100],
    ['id' => 11, 'name' => 'Product K', 'price' => 110],
    ['id' => 12, 'name' => 'Product L', 'price' => 120],
];

$paginator = new Paginator(12, 4, 2);
$pageItems = $paginator->slice($products);

echo "Items on page 2 (4 per page):\n";
print_r($pageItems);

// ============================================
// Example 6: Cursor-Based Pagination
// ============================================
echo "\n--- Example 6: Cursor-Based Pagination ---\n\n";

// Simulating API response items
$apiItems = [
    ['id' => 101, 'title' => 'First Post'],
    ['id' => 102, 'title' => 'Second Post'],
    ['id' => 103, 'title' => 'Third Post'],
    ['id' => 104, 'title' => 'Fourth Post'],
    ['id' => 105, 'title' => 'Fifth Post'],
];

// Create cursor paginator (fetch limit + 1 to detect hasMore)
$cursorPaginator = new CursorPaginator($apiItems, 3);

echo "Current page items:\n";
print_r($cursorPaginator->getItems());

echo "\nCursor metadata:\n";
print_r($cursorPaginator->getMetadata());

echo "\nAPI response format:\n";
print_r($cursorPaginator->toApiResponse(['request_id' => 'abc123']));

// ============================================
// Example 7: Cursor Decoding
// ============================================
echo "\n--- Example 7: Cursor Decoding ---\n\n";

// Example cursor from API
$exampleCursor = base64_encode(json_encode(['id' => 102]));
echo "Encoded cursor: {$exampleCursor}\n";

$decoded = CursorPaginator::decodeCursor($exampleCursor);
echo "Decoded cursor:\n";
print_r($decoded);

// ============================================
// Example 8: Infinite Scroll Helper
// ============================================
echo "\n--- Example 8: Infinite Scroll Helper ---\n\n";

$paginator = new Paginator(500, 20, 1, '/api/posts?page={page}');
$infiniteScroll = new InfiniteScroll($paginator);

$infiniteScroll->setLoadMoreText('Load More Posts')
               ->setLoadingText('Loading...')
               ->setNoMoreText('All posts loaded');

echo "Has more items: " . ($infiniteScroll->hasMore() ? 'Yes' : 'No') . "\n";
echo "Next URL: {$infiniteScroll->getNextUrl()}\n\n";

echo "Load more button:\n";
echo $infiniteScroll->renderLoadMoreButton();
echo "\n\n";

echo "Data attributes:\n";
echo $infiniteScroll->renderDataAttributes();
echo "\n";

// ============================================
// Example 9: GraphQL-style Pagination
// ============================================
echo "\n--- Example 9: GraphQL-style Pagination ---\n\n";

$allPosts = range(1, 50);

// Get first 10 posts
$result = SimplePageInfo::create($allPosts, 10);
echo "First 10 posts:\n";
echo "Items: " . implode(', ', $result['items']) . "\n";
echo "PageInfo:\n";
print_r($result['pageInfo']);

// Get 5 posts after cursor (position 10)
$afterCursor = base64_encode('10');
$result = SimplePageInfo::create($allPosts, 5, $afterCursor);
echo "\n5 posts after position 10:\n";
echo "Items: " . implode(', ', $result['items']) . "\n";

// Get last 5 posts
$result = SimplePageInfo::create($allPosts, null, null, null, 5);
echo "\nLast 5 posts:\n";
echo "Items: " . implode(', ', $result['items']) . "\n";

// ============================================
// Example 10: Helper Functions
// ============================================
echo "\n--- Example 10: Helper Functions ---\n\n";

// Validate page number
echo "Validating pages:\n";
echo "  -5 → " . PaginationHelper::validatePage(-5, 10) . "\n";
echo "  0 → " . PaginationHelper::validatePage(0, 10) . "\n";
echo "  5 → " . PaginationHelper::validatePage(5, 10) . "\n";
echo "  15 → " . PaginationHelper::validatePage(15, 10) . "\n";

// Calculate offset and limit
echo "\nOffset/Limit for page 5, 20 per page:\n";
$result = PaginationHelper::calculateOffsetLimit(5, 20);
print_r($result);

// Calculate total pages
echo "\nTotal pages calculations:\n";
echo "  100 items, 10 per page → " . PaginationHelper::calculateTotalPages(100, 10) . " pages\n";
echo "  99 items, 10 per page → " . PaginationHelper::calculateTotalPages(99, 10) . " pages\n";
echo "  5 items, 10 per page → " . PaginationHelper::calculateTotalPages(5, 10) . " pages\n";

// Generate page range
echo "\nPage range around page 10 of 50:\n";
$range = PaginationHelper::generatePageRange(10, 50, 3);
echo implode(', ', $range) . "\n";

// Build URL
echo "\nURL with page and extra params:\n";
echo PaginationHelper::buildUrl('/api/users', 'page', 3, ['sort' => 'name', 'filter' => 'active']);
echo "\n";

// ============================================
// Example 11: Custom Styling
// ============================================
echo "\n--- Example 11: Custom HTML Styling ---\n\n";

$paginator = new Paginator(100, 10, 5);

// Custom Bootstrap 4 style
$html = $paginator->renderHtml([
    'ul_class' => 'pagination justify-content-center mt-4',
    'li_class' => 'page-item',
    'a_class' => 'page-link bg-primary text-white',
    'active_class' => 'active',
    'disabled_class' => 'disabled',
]);

echo "Custom styled pagination:\n";
echo $html;
echo "\n";

// ============================================
// Example 12: Full Workflow Example
// ============================================
echo "\n--- Example 12: Full Pagination Workflow ---\n\n";

// Simulate a full pagination workflow for a web page

// 1. Get total count from database
$totalItems = 247; // SELECT COUNT(*) FROM products

// 2. Create paginator
$paginator = new Paginator($totalItems, 20, 5, '/products?page={page}');
$paginator->setQueryParams(['category' => 'electronics']);

// 3. Build SQL query
$sql = "SELECT * FROM products WHERE category = 'electronics' 
        ORDER BY created_at DESC 
        LIMIT {$paginator->getLimit()} OFFSET {$paginator->getOffset()}";
echo "SQL Query:\n{$sql}\n\n";

// 4. Get pagination metadata for JSON response
$metadata = $paginator->getMetadata();
echo "Pagination metadata:\n";
print_r($metadata);

// 5. Generate pagination links
echo "\nPagination HTML:\n";
echo $paginator->renderHtml();
echo "\n\n";

// 6. Show "Showing X to Y of Z entries"
echo $paginator->renderSummary('Showing {start}-{end} of {total} products');
echo "\n";

echo "\n=== All Examples Complete ===\n";
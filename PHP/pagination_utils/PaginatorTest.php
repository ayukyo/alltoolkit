<?php

/**
 * Pagination Utils Test Suite
 * 
 * Run with: php PaginatorTest.php
 * 
 * @package PaginationUtils
 */

require_once __DIR__ . '/Paginator.php';

use PaginationUtils\Paginator;
use PaginationUtils\CursorPaginator;
use PaginationUtils\InfiniteScroll;
use PaginationUtils\SimplePageInfo;
use PaginationUtils\PaginationHelper;

class PaginatorTest
{
    private int $passed = 0;
    private int $failed = 0;
    
    /**
     * Run all tests.
     */
    public function run(): void
    {
        echo "=== Pagination Utils Test Suite ===\n\n";
        
        // Paginator tests
        $this->testBasicPagination();
        $this->testOffsetAndLimit();
        $this->testPageNavigation();
        $this->testEdgeCases();
        $this->testGetPages();
        $this->testLinks();
        $this->testHtmlRendering();
        $this->testSummary();
        $this->testSlice();
        $this->testFromRequest();
        
        // CursorPaginator tests
        $this->testCursorPagination();
        $this->testCursorMetadata();
        $this->testCursorApiResponse();
        
        // InfiniteScroll tests
        $this->testInfiniteScroll();
        
        // SimplePageInfo tests
        $this->testSimplePageInfo();
        
        // Helper tests
        $this->testHelperFunctions();
        
        echo "\n=== Test Results ===\n";
        echo "Passed: {$this->passed}\n";
        echo "Failed: {$this->failed}\n";
        echo "Total: " . ($this->passed + $this->failed) . "\n";
        
        if ($this->failed === 0) {
            echo "\n✅ All tests passed!\n";
        } else {
            echo "\n❌ Some tests failed.\n";
        }
    }
    
    /**
     * Assert helper.
     */
    private function assert(bool $condition, string $message): void
    {
        if ($condition) {
            $this->passed++;
            echo "✓ {$message}\n";
        } else {
            $this->failed++;
            echo "✗ {$message}\n";
        }
    }
    
    /**
     * Assert equal helper.
     */
    private function assertEquals($expected, $actual, string $message): void
    {
        $this->assert($expected === $actual, "{$message} (expected: " . json_encode($expected) . ", got: " . json_encode($actual) . ")");
    }
    
    /**
     * Test basic pagination.
     */
    private function testBasicPagination(): void
    {
        echo "\n--- Basic Pagination Tests ---\n";
        
        $paginator = new Paginator(100, 10, 1);
        
        $this->assertEquals(100, $paginator->getMetadata()['total_items'], 'Total items is correct');
        $this->assertEquals(10, $paginator->getMetadata()['items_per_page'], 'Items per page is correct');
        $this->assertEquals(1, $paginator->getCurrentPage(), 'Current page is correct');
        $this->assertEquals(10, $paginator->getTotalPages(), 'Total pages is correct');
    }
    
    /**
     * Test offset and limit calculations.
     */
    private function testOffsetAndLimit(): void
    {
        echo "\n--- Offset and Limit Tests ---\n";
        
        $paginator = new Paginator(100, 10, 1);
        $this->assertEquals(0, $paginator->getOffset(), 'Offset for page 1 is 0');
        $this->assertEquals(10, $paginator->getLimit(), 'Limit is items per page');
        
        $paginator = new Paginator(100, 10, 3);
        $this->assertEquals(20, $paginator->getOffset(), 'Offset for page 3 is 20');
        
        $paginator = new Paginator(100, 10, 10);
        $this->assertEquals(90, $paginator->getOffset(), 'Offset for page 10 is 90');
    }
    
    /**
     * Test page navigation.
     */
    private function testPageNavigation(): void
    {
        echo "\n--- Page Navigation Tests ---\n";
        
        $paginator = new Paginator(100, 10, 5);
        
        $this->assert($paginator->hasPreviousPage(), 'Page 5 has previous page');
        $this->assert($paginator->hasNextPage(), 'Page 5 has next page');
        $this->assertEquals(4, $paginator->getPreviousPage(), 'Previous page is 4');
        $this->assertEquals(6, $paginator->getNextPage(), 'Next page is 6');
        
        // First page
        $paginator = new Paginator(100, 10, 1);
        $this->assert(!$paginator->hasPreviousPage(), 'First page has no previous');
        $this->assert($paginator->hasNextPage(), 'First page has next');
        
        // Last page
        $paginator = new Paginator(100, 10, 10);
        $this->assert($paginator->hasPreviousPage(), 'Last page has previous');
        $this->assert(!$paginator->hasNextPage(), 'Last page has no next');
    }
    
    /**
     * Test edge cases.
     */
    private function testEdgeCases(): void
    {
        echo "\n--- Edge Case Tests ---\n";
        
        // Empty dataset
        $paginator = new Paginator(0, 10, 1);
        $this->assertEquals(0, $paginator->getTotalPages(), 'Empty dataset has 0 pages');
        $this->assertEquals(0, $paginator->getStartItemNumber(), 'Empty dataset start is 0');
        $this->assertEquals(0, $paginator->getEndItemNumber(), 'Empty dataset end is 0');
        
        // Single item
        $paginator = new Paginator(1, 10, 1);
        $this->assertEquals(1, $paginator->getTotalPages(), 'Single item has 1 page');
        $this->assertEquals(1, $paginator->getStartItemNumber(), 'Single item start is 1');
        $this->assertEquals(1, $paginator->getEndItemNumber(), 'Single item end is 1');
        
        // Page beyond range
        $paginator = new Paginator(50, 10, 100);
        $this->assertEquals(5, $paginator->getCurrentPage(), 'Page beyond range is clamped');
        
        // Zero items per page (should default to 1)
        $paginator = new Paginator(100, 0, 1);
        $this->assertEquals(1, $paginator->getLimit(), 'Zero items per page defaults to 1');
    }
    
    /**
     * Test getPages method.
     */
    private function testGetPages(): void
    {
        echo "\n--- Get Pages Tests ---\n";
        
        // Small page count
        $paginator = new Paginator(30, 10, 2);
        $pages = $paginator->getPages();
        $this->assertEquals([1, 2, 3], $pages, 'Small page count shows all pages');
        
        // Large page count - middle page
        $paginator = new Paginator(100, 10, 5);
        $pages = $paginator->getPages();
        $this->assert(in_array(1, $pages), 'First page is included');
        $this->assert(in_array(10, $pages), 'Last page is included');
        $this->assert(in_array(5, $pages), 'Current page is included');
        $this->assert(in_array('ellipsis', $pages), 'Ellipsis is present for large ranges');
        
        // Near start
        $paginator = new Paginator(100, 10, 2);
        $pages = $paginator->getPages();
        $this->assertEquals(1, $pages[0], 'First page is 1');
    }
    
    /**
     * Test links generation.
     */
    private function testLinks(): void
    {
        echo "\n--- Links Tests ---\n";
        
        $paginator = new Paginator(100, 10, 5, '/items?page={page}');
        $links = $paginator->getLinks();
        
        $prevLink = $links[0];
        $this->assertEquals('prev', $prevLink['type'], 'First link is previous');
        $this->assertEquals('/items?page=4', $prevLink['url'], 'Previous URL is correct');
        
        $nextLink = end($links);
        $this->assertEquals('next', $nextLink['type'], 'Last link is next');
        $this->assertEquals('/items?page=6', $nextLink['url'], 'Next URL is correct');
        
        // With query params
        $paginator = new Paginator(100, 10, 5, '/items?page={page}');
        $paginator->setQueryParams(['category' => 'books', 'sort' => 'date']);
        $links = $paginator->getLinks();
        $this->assert(strpos($links[0]['url'], 'category=books') !== false, 'Query params are preserved');
    }
    
    /**
     * Test HTML rendering.
     */
    private function testHtmlRendering(): void
    {
        echo "\n--- HTML Rendering Tests ---\n";
        
        $paginator = new Paginator(100, 10, 5);
        $html = $paginator->renderHtml();
        
        $this->assert(strpos($html, '<ul') !== false, 'HTML contains ul element');
        $this->assert(strpos($html, 'pagination') !== false, 'HTML contains pagination class');
        $this->assert(strpos($html, 'page-item') !== false, 'HTML contains page-item class');
        $this->assert(strpos($html, 'page-link') !== false, 'HTML contains page-link class');
        
        // Test summary
        $summary = $paginator->renderSummary();
        $this->assert(strpos($summary, '41') !== false, 'Summary shows start item');
        $this->assert(strpos($summary, '50') !== false, 'Summary shows end item');
        $this->assert(strpos($summary, '100') !== false, 'Summary shows total items');
    }
    
    /**
     * Test slice method.
     */
    private function testSlice(): void
    {
        echo "\n--- Slice Tests ---\n";
        
        $items = range(1, 100);
        $paginator = new Paginator(100, 10, 3);
        $sliced = $paginator->slice($items);
        
        $this->assertEquals(10, count($sliced), 'Slice returns correct count');
        $this->assertEquals(21, $sliced[0], 'Slice starts at correct item');
        $this->assertEquals(30, $sliced[9], 'Slice ends at correct item');
    }
    
    /**
     * Test fromRequest method.
     */
    private function testFromRequest(): void
    {
        echo "\n--- From Request Tests ---\n";
        
        // Mock $_GET
        $_GET['page'] = 3;
        
        $paginator = Paginator::fromRequest(100, 10);
        $this->assertEquals(3, $paginator->getCurrentPage(), 'Current page from request is correct');
        
        unset($_GET['page']);
    }
    
    /**
     * Test cursor pagination.
     */
    private function testCursorPagination(): void
    {
        echo "\n--- Cursor Pagination Tests ---\n";
        
        $items = [
            ['id' => 1, 'name' => 'Item 1'],
            ['id' => 2, 'name' => 'Item 2'],
            ['id' => 3, 'name' => 'Item 3'],
            ['id' => 4, 'name' => 'Item 4'],
            ['id' => 5, 'name' => 'Item 5'],
        ];
        
        // Test with 2 items per page, pass 3 items (2 + 1 to check hasMore)
        $paginator = new CursorPaginator(array_slice($items, 0, 3), 2);
        
        $this->assertEquals(2, count($paginator->getItems()), 'Returns correct number of items');
        $this->assert($paginator->hasNextPage(), 'Has next page');
        $this->assert(!$paginator->hasPreviousPage(), 'No previous page initially');
        $this->assert($paginator->getNextCursor() !== null, 'Next cursor is generated');
    }
    
    /**
     * Test cursor metadata.
     */
    private function testCursorMetadata(): void
    {
        echo "\n--- Cursor Metadata Tests ---\n";
        
        $items = [
            ['id' => 1, 'name' => 'Item 1'],
            ['id' => 2, 'name' => 'Item 2'],
            ['id' => 3, 'name' => 'Item 3'],
        ];
        
        $paginator = new CursorPaginator($items, 2);
        $meta = $paginator->getMetadata();
        
        $this->assertEquals(2, $meta['items_per_page'], 'Items per page is correct');
        $this->assertEquals(2, $meta['item_count'], 'Item count is correct');
        $this->assert($meta['has_next'], 'Has next is true');
    }
    
    /**
     * Test cursor API response.
     */
    private function testCursorApiResponse(): void
    {
        echo "\n--- Cursor API Response Tests ---\n";
        
        $items = [
            ['id' => 1, 'name' => 'Item 1'],
            ['id' => 2, 'name' => 'Item 2'],
        ];
        
        $paginator = new CursorPaginator($items, 10);
        $response = $paginator->toApiResponse(['meta' => 'test']);
        
        $this->assert(isset($response['data']), 'Response has data');
        $this->assert(isset($response['pagination']), 'Response has pagination');
        $this->assertEquals('test', $response['meta'], 'Additional data is merged');
        
        // Cursor decoding
        $cursor = $paginator->getNextCursor();
        if ($cursor) {
            $decoded = CursorPaginator::decodeCursor($cursor);
            $this->assert(isset($decoded['id']), 'Cursor can be decoded');
        } else {
            $this->assert(true, 'No cursor to decode (no next page)');
        }
    }
    
    /**
     * Test infinite scroll helper.
     */
    private function testInfiniteScroll(): void
    {
        echo "\n--- Infinite Scroll Tests ---\n";
        
        $paginator = new Paginator(100, 10, 1);
        $infinite = new InfiniteScroll($paginator);
        
        $this->assert($infinite->hasMore(), 'Has more items');
        $this->assert($infinite->getNextUrl() !== null, 'Has next URL');
        
        $button = $infinite->renderLoadMoreButton();
        $this->assert(strpos($button, 'button') !== false, 'Render button contains button element');
        
        $attrs = $infinite->renderDataAttributes();
        $this->assert(strpos($attrs, 'data-has-more') !== false, 'Has data attributes');
    }
    
    /**
     * Test SimplePageInfo.
     */
    private function testSimplePageInfo(): void
    {
        echo "\n--- Simple Page Info Tests ---\n";
        
        $items = range(1, 20);
        
        // Test 'first' parameter
        $result = SimplePageInfo::create($items, 5);
        $this->assertEquals(5, count($result['items']), 'First parameter limits items');
        $this->assert($result['pageInfo']['hasNextPage'], 'Has next page');
        $this->assert(!$result['pageInfo']['hasPreviousPage'], 'No previous page');
        
        // Test 'after' parameter
        $result = SimplePageInfo::create($items, 5, base64_encode('5'));
        $this->assertEquals(6, $result['items'][0], 'After cursor works');
        
        // Test 'last' parameter
        $result = SimplePageInfo::create($items, null, null, null, 3);
        $this->assertEquals(3, count($result['items']), 'Last parameter limits items');
        $this->assertEquals(18, $result['items'][2], 'Last returns from end');
    }
    
    /**
     * Test helper functions.
     */
    private function testHelperFunctions(): void
    {
        echo "\n--- Helper Function Tests ---\n";
        
        // validatePage
        $this->assertEquals(1, PaginationHelper::validatePage(-5, 10), 'Negative page clamped to 1');
        $this->assertEquals(1, PaginationHelper::validatePage(0, 10), 'Zero page clamped to 1');
        $this->assertEquals(5, PaginationHelper::validatePage(5, 10), 'Valid page unchanged');
        $this->assertEquals(10, PaginationHelper::validatePage(15, 10), 'Page beyond max clamped');
        
        // calculateOffsetLimit
        $result = PaginationHelper::calculateOffsetLimit(3, 10);
        $this->assertEquals(20, $result['offset'], 'Offset calculated correctly');
        $this->assertEquals(10, $result['limit'], 'Limit calculated correctly');
        
        // calculateTotalPages
        $this->assertEquals(10, PaginationHelper::calculateTotalPages(100, 10), '100 items, 10 per page = 10 pages');
        $this->assertEquals(11, PaginationHelper::calculateTotalPages(101, 10), '101 items, 10 per page = 11 pages');
        $this->assertEquals(1, PaginationHelper::calculateTotalPages(5, 10), '5 items, 10 per page = 1 page');
        
        // generatePageRange
        $range = PaginationHelper::generatePageRange(5, 10, 2);
        $this->assertEquals([3, 4, 5, 6, 7], $range, 'Page range centered on current');
        
        // buildUrl
        $url = PaginationHelper::buildUrl('/items', 'page', 3, ['sort' => 'desc']);
        $this->assert(strpos($url, 'page=3') !== false, 'URL contains page param');
        $this->assert(strpos($url, 'sort=desc') !== false, 'URL contains extra param');
    }
}

// Run tests
$test = new PaginatorTest();
$test->run();
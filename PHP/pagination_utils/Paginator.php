<?php

/**
 * Pagination Utils - A comprehensive PHP pagination library with zero dependencies.
 * 
 * Features:
 * - Offset-based pagination
 * - Cursor-based pagination
 * - Page link generation
 * - Metadata generation (total pages, next/prev, etc.)
 * - Bootstrap-compatible HTML output
 * - Customizable templates
 * 
 * @package   PaginationUtils
 * @author    AllToolkit
 * @version   1.0.0
 * @license   MIT
 */

namespace PaginationUtils;

/**
 * Paginator class for offset-based pagination.
 */
class Paginator
{
    /** @var int Total number of items */
    protected int $totalItems;
    
    /** @var int Items per page */
    protected int $itemsPerPage;
    
    /** @var int Current page (1-indexed) */
    protected int $currentPage;
    
    /** @var int Maximum number of page links to show */
    protected int $maxPagesToShow;
    
    /** @var string URL pattern with {page} placeholder */
    protected string $urlPattern;
    
    /** @var array Query parameters to preserve */
    protected array $queryParams = [];
    
    /** @var int Number of pages on each side of current page */
    protected int $pagesOnSide = 2;
    
    /** @var int Number of pages at start/end */
    protected int $pagesAtEnds = 1;
    
    /** @var string Previous button text */
    protected string $prevText = '&laquo;';
    
    /** @var string Next button text */
    protected string $nextText = '&raquo;';
    
    /** @var string Ellipsis text */
    protected string $ellipsisText = '...';
    
    /**
     * Create a new Paginator instance.
     *
     * @param int $totalItems Total number of items
     * @param int $itemsPerPage Items per page (default: 10)
     * @param int $currentPage Current page number, 1-indexed (default: 1)
     * @param string $urlPattern URL pattern with {page} placeholder
     */
    public function __construct(
        int $totalItems,
        int $itemsPerPage = 10,
        int $currentPage = 1,
        string $urlPattern = '?page={page}'
    ) {
        $this->totalItems = max(0, $totalItems);
        $this->itemsPerPage = max(1, $itemsPerPage);
        $this->currentPage = max(1, $currentPage);
        $this->urlPattern = $urlPattern;
        $this->maxPagesToShow = 5;
    }
    
    /**
     * Calculate the offset for database queries.
     *
     * @return int Offset value
     */
    public function getOffset(): int
    {
        return ($this->getCurrentPage() - 1) * $this->itemsPerPage;
    }
    
    /**
     * Get the limit for database queries.
     *
     * @return int Limit value
     */
    public function getLimit(): int
    {
        return $this->itemsPerPage;
    }
    
    /**
     * Get the current page number.
     *
     * @return int Current page (1-indexed)
     */
    public function getCurrentPage(): int
    {
        return min($this->currentPage, max(1, $this->getTotalPages()));
    }
    
    /**
     * Get total number of pages.
     *
     * @return int Total pages
     */
    public function getTotalPages(): int
    {
        return (int) ceil($this->totalItems / $this->itemsPerPage);
    }
    
    /**
     * Check if there is a previous page.
     *
     * @return bool
     */
    public function hasPreviousPage(): bool
    {
        return $this->getCurrentPage() > 1;
    }
    
    /**
     * Check if there is a next page.
     *
     * @return bool
     */
    public function hasNextPage(): bool
    {
        return $this->getCurrentPage() < $this->getTotalPages();
    }
    
    /**
     * Get the previous page number.
     *
     * @return int|null Previous page or null if on first page
     */
    public function getPreviousPage(): ?int
    {
        return $this->hasPreviousPage() ? $this->getCurrentPage() - 1 : null;
    }
    
    /**
     * Get the next page number.
     *
     * @return int|null Next page or null if on last page
     */
    public function getNextPage(): ?int
    {
        return $this->hasNextPage() ? $this->getCurrentPage() + 1 : null;
    }
    
    /**
     * Get the first page number (always 1).
     *
     * @return int
     */
    public function getFirstPage(): int
    {
        return 1;
    }
    
    /**
     * Get the last page number.
     *
     * @return int
     */
    public function getLastPage(): int
    {
        return $this->getTotalPages();
    }
    
    /**
     * Get the starting item number for the current page.
     *
     * @return int Starting item number (1-indexed)
     */
    public function getStartItemNumber(): int
    {
        return $this->totalItems > 0 ? $this->getOffset() + 1 : 0;
    }
    
    /**
     * Get the ending item number for the current page.
     *
     * @return int Ending item number
     */
    public function getEndItemNumber(): int
    {
        return min($this->getOffset() + $this->itemsPerPage, $this->totalItems);
    }
    
    /**
     * Generate a URL for a specific page.
     *
     * @param int $page Page number
     * @return string Generated URL
     */
    public function getPageUrl(int $page): string
    {
        $url = str_replace('{page}', (string) $page, $this->urlPattern);
        
        if (!empty($this->queryParams)) {
            $separator = strpos($url, '?') !== false ? '&' : '?';
            $url .= $separator . http_build_query($this->queryParams);
        }
        
        return $url;
    }
    
    /**
     * Generate an array of page numbers to display.
     * Handles ellipsis for large page ranges.
     *
     * @return array Array of page numbers and ellipsis markers
     */
    public function getPages(): array
    {
        $totalPages = $this->getTotalPages();
        $currentPage = $this->getCurrentPage();
        
        if ($totalPages <= 1) {
            return [];
        }
        
        $pages = [];
        
        // If total pages is small, show all
        if ($totalPages <= $this->maxPagesToShow + 2) {
            for ($i = 1; $i <= $totalPages; $i++) {
                $pages[] = $i;
            }
            return $pages;
        }
        
        // Always show first page
        $pages[] = 1;
        
        // Calculate range around current page
        $start = max(2, $currentPage - $this->pagesOnSide);
        $end = min($totalPages - 1, $currentPage + $this->pagesOnSide);
        
        // Add ellipsis after first if needed
        if ($start > 2) {
            $pages[] = 'ellipsis';
        }
        
        // Add pages around current
        for ($i = $start; $i <= $end; $i++) {
            $pages[] = $i;
        }
        
        // Add ellipsis before last if needed
        if ($end < $totalPages - 1) {
            $pages[] = 'ellipsis';
        }
        
        // Always show last page
        if ($totalPages > 1) {
            $pages[] = $totalPages;
        }
        
        return $pages;
    }
    
    /**
     * Get pagination metadata as an array.
     *
     * @return array Pagination metadata
     */
    public function getMetadata(): array
    {
        return [
            'total_items' => $this->totalItems,
            'items_per_page' => $this->itemsPerPage,
            'current_page' => $this->getCurrentPage(),
            'total_pages' => $this->getTotalPages(),
            'has_previous' => $this->hasPreviousPage(),
            'has_next' => $this->hasNextPage(),
            'previous_page' => $this->getPreviousPage(),
            'next_page' => $this->getNextPage(),
            'first_page' => $this->getFirstPage(),
            'last_page' => $this->getLastPage(),
            'start_item' => $this->getStartItemNumber(),
            'end_item' => $this->getEndItemNumber(),
            'offset' => $this->getOffset(),
            'limit' => $this->getLimit(),
        ];
    }
    
    /**
     * Generate pagination links as an array.
     *
     * @return array Array of link data
     */
    public function getLinks(): array
    {
        $links = [];
        $pages = $this->getPages();
        $currentPage = $this->getCurrentPage();
        
        // Previous link
        if ($this->hasPreviousPage()) {
            $links[] = [
                'type' => 'prev',
                'page' => $this->getPreviousPage(),
                'url' => $this->getPageUrl($this->getPreviousPage()),
                'text' => $this->prevText,
                'disabled' => false,
            ];
        } else {
            $links[] = [
                'type' => 'prev',
                'page' => null,
                'url' => '#',
                'text' => $this->prevText,
                'disabled' => true,
            ];
        }
        
        // Page links
        foreach ($pages as $page) {
            if ($page === 'ellipsis') {
                $links[] = [
                    'type' => 'ellipsis',
                    'text' => $this->ellipsisText,
                ];
            } else {
                $links[] = [
                    'type' => 'page',
                    'page' => $page,
                    'url' => $this->getPageUrl($page),
                    'text' => (string) $page,
                    'active' => $page === $currentPage,
                ];
            }
        }
        
        // Next link
        if ($this->hasNextPage()) {
            $links[] = [
                'type' => 'next',
                'page' => $this->getNextPage(),
                'url' => $this->getPageUrl($this->getNextPage()),
                'text' => $this->nextText,
                'disabled' => false,
            ];
        } else {
            $links[] = [
                'type' => 'next',
                'page' => null,
                'url' => '#',
                'text' => $this->nextText,
                'disabled' => true,
            ];
        }
        
        return $links;
    }
    
    /**
     * Render pagination as HTML (Bootstrap 5 compatible).
     *
     * @param array $options HTML options
     * @return string HTML string
     */
    public function renderHtml(array $options = []): string
    {
        $links = $this->getLinks();
        
        if (empty($links)) {
            return '';
        }
        
        $ulClass = $options['ul_class'] ?? 'pagination justify-content-center';
        $liClass = $options['li_class'] ?? 'page-item';
        $aClass = $options['a_class'] ?? 'page-link';
        $activeClass = $options['active_class'] ?? 'active';
        $disabledClass = $options['disabled_class'] ?? 'disabled';
        
        $html = '<ul class="' . htmlspecialchars($ulClass) . '">';
        
        foreach ($links as $link) {
            $liClasses = [$liClass];
            $aAttributes = [];
            
            if ($link['type'] === 'ellipsis') {
                $liClasses[] = $disabledClass;
                $html .= '<li class="' . implode(' ', $liClasses) . '">';
                $html .= '<span class="' . htmlspecialchars($aClass) . '">' . $this->ellipsisText . '</span>';
                $html .= '</li>';
            } else {
                if (isset($link['active']) && $link['active']) {
                    $liClasses[] = $activeClass;
                }
                if (isset($link['disabled']) && $link['disabled']) {
                    $liClasses[] = $disabledClass;
                }
                
                $html .= '<li class="' . implode(' ', $liClasses) . '">';
                
                if (isset($link['disabled']) && $link['disabled']) {
                    $html .= '<span class="' . htmlspecialchars($aClass) . '">' . $link['text'] . '</span>';
                } else {
                    $html .= '<a class="' . htmlspecialchars($aClass) . '" href="' . htmlspecialchars($link['url']) . '">';
                    $html .= $link['text'];
                    $html .= '</a>';
                }
                
                $html .= '</li>';
            }
        }
        
        $html .= '</ul>';
        
        return $html;
    }
    
    /**
     * Render "Showing X to Y of Z entries" text.
     *
     * @param string $template Template with {start}, {end}, {total} placeholders
     * @return string Rendered text
     */
    public function renderSummary(string $template = 'Showing {start} to {end} of {total} entries'): string
    {
        if ($this->totalItems === 0) {
            return 'Showing 0 entries';
        }
        
        return str_replace(
            ['{start}', '{end}', '{total}'],
            [$this->getStartItemNumber(), $this->getEndItemNumber(), $this->totalItems],
            $template
        );
    }
    
    /**
     * Set query parameters to preserve in URLs.
     *
     * @param array $params Query parameters
     * @return self
     */
    public function setQueryParams(array $params): self
    {
        $this->queryParams = $params;
        return $this;
    }
    
    /**
     * Set the URL pattern.
     *
     * @param string $pattern URL pattern with {page} placeholder
     * @return self
     */
    public function setUrlPattern(string $pattern): self
    {
        $this->urlPattern = $pattern;
        return $this;
    }
    
    /**
     * Set the maximum number of page links to show.
     *
     * @param int $max Maximum pages to show
     * @return self
     */
    public function setMaxPagesToShow(int $max): self
    {
        $this->maxPagesToShow = max(1, $max);
        return $this;
    }
    
    /**
     * Set navigation button texts.
     *
     * @param string $prev Previous button text
     * @param string $next Next button text
     * @return self
     */
    public function setNavTexts(string $prev, string $next): self
    {
        $this->prevText = $prev;
        $this->nextText = $next;
        return $this;
    }
    
    /**
     * Set ellipsis text.
     *
     * @param string $text Ellipsis text
     * @return self
     */
    public function setEllipsisText(string $text): self
    {
        $this->ellipsisText = $text;
        return $this;
    }
    
    /**
     * Create a paginator from current request parameters.
     *
     * @param int $totalItems Total number of items
     * @param int $itemsPerPage Items per page
     * @param string $pageParam Page parameter name
     * @param array $queryParams Additional query params to preserve
     * @return self
     */
    public static function fromRequest(
        int $totalItems,
        int $itemsPerPage = 10,
        string $pageParam = 'page',
        array $queryParams = []
    ): self {
        $currentPage = isset($_GET[$pageParam]) ? max(1, (int) $_GET[$pageParam]) : 1;
        
        // Build URL pattern
        $params = array_merge($queryParams, [$pageParam => '{page}']);
        $urlPattern = '?' . http_build_query($params);
        
        $paginator = new self($totalItems, $itemsPerPage, $currentPage, $urlPattern);
        $paginator->setQueryParams($queryParams);
        
        return $paginator;
    }
    
    /**
     * Slice an array to get items for the current page.
     *
     * @param array $items Full array of items
     * @return array Sliced array
     */
    public function slice(array $items): array
    {
        if (empty($items)) {
            return [];
        }
        
        return array_slice($items, $this->getOffset(), $this->getLimit());
    }
}

/**
 * CursorPaginator class for cursor-based pagination.
 * More efficient for large datasets as it doesn't count total items.
 */
class CursorPaginator
{
    /** @var array Items for current page */
    protected array $items;
    
    /** @var int Items per page */
    protected int $itemsPerPage;
    
    /** @var string|null Cursor for the next page */
    protected ?string $nextCursor = null;
    
    /** @var string|null Cursor for the previous page */
    protected ?string $prevCursor = null;
    
    /** @var bool Has next page */
    protected bool $hasNext = false;
    
    /** @var bool Has previous page */
    protected bool $hasPrevious = false;
    
    /** @var callable Function to generate cursor from item */
    protected $cursorGenerator;
    
    /**
     * Create a new CursorPaginator instance.
     *
     * @param array $items Items for current page (fetch limit + 1)
     * @param int $itemsPerPage Items per page
     * @param callable|null $cursorGenerator Function to generate cursor from item
     */
    public function __construct(
        array $items,
        int $itemsPerPage = 10,
        ?callable $cursorGenerator = null
    ) {
        $this->itemsPerPage = max(1, $itemsPerPage);
        $this->cursorGenerator = $cursorGenerator ?? [$this, 'defaultCursorGenerator'];
        
        // Check if we have more items
        if (count($items) > $this->itemsPerPage) {
            $this->hasNext = true;
            $this->items = array_slice($items, 0, $this->itemsPerPage);
        } else {
            $this->items = $items;
        }
        
        // Generate next cursor if we have items and more pages
        if (!empty($this->items) && $this->hasNext) {
            $lastItem = end($this->items);
            $this->nextCursor = ($this->cursorGenerator)($lastItem);
        }
    }
    
    /**
     * Default cursor generator using JSON encoding.
     *
     * @param mixed $item Item to generate cursor for
     * @return string Cursor string
     */
    protected function defaultCursorGenerator($item): string
    {
        if (is_array($item)) {
            if (isset($item['id'])) {
                return base64_encode(json_encode(['id' => $item['id']]));
            }
            return base64_encode(json_encode($item));
        }
        if (is_object($item)) {
            if (isset($item->id)) {
                return base64_encode(json_encode(['id' => $item->id]));
            }
            return base64_encode(json_encode($item));
        }
        return base64_encode(json_encode(['value' => $item]));
    }
    
    /**
     * Get items for current page.
     *
     * @return array
     */
    public function getItems(): array
    {
        return $this->items;
    }
    
    /**
     * Check if there is a next page.
     *
     * @return bool
     */
    public function hasNextPage(): bool
    {
        return $this->hasNext;
    }
    
    /**
     * Check if there is a previous page.
     *
     * @return bool
     */
    public function hasPreviousPage(): bool
    {
        return $this->hasPrevious;
    }
    
    /**
     * Get the next page cursor.
     *
     * @return string|null
     */
    public function getNextCursor(): ?string
    {
        return $this->nextCursor;
    }
    
    /**
     * Get the previous page cursor.
     *
     * @return string|null
     */
    public function getPreviousCursor(): ?string
    {
        return $this->prevCursor;
    }
    
    /**
     * Set the previous cursor.
     *
     * @param string|null $cursor Previous cursor
     * @return self
     */
    public function setPreviousCursor(?string $cursor): self
    {
        $this->prevCursor = $cursor;
        $this->hasPrevious = $cursor !== null;
        return $this;
    }
    
    /**
     * Decode a cursor string.
     *
     * @param string $cursor Encoded cursor
     * @return array|null Decoded cursor data or null if invalid
     */
    public static function decodeCursor(string $cursor): ?array
    {
        $decoded = base64_decode($cursor, true);
        if ($decoded === false) {
            return null;
        }
        
        $data = json_decode($decoded, true);
        if (json_last_error() !== JSON_ERROR_NONE) {
            return null;
        }
        
        return $data;
    }
    
    /**
     * Get pagination metadata.
     *
     * @return array
     */
    public function getMetadata(): array
    {
        return [
            'items_per_page' => $this->itemsPerPage,
            'item_count' => count($this->items),
            'has_next' => $this->hasNext,
            'has_previous' => $this->hasPrevious,
            'next_cursor' => $this->nextCursor,
            'previous_cursor' => $this->prevCursor,
        ];
    }
    
    /**
     * Render as API response format.
     *
     * @param array $additionalData Additional data to include
     * @return array
     */
    public function toApiResponse(array $additionalData = []): array
    {
        $response = [
            'data' => $this->items,
            'pagination' => [
                'per_page' => $this->itemsPerPage,
                'count' => count($this->items),
                'has_next' => $this->hasNext,
                'has_previous' => $this->hasPrevious,
            ],
        ];
        
        if ($this->nextCursor !== null) {
            $response['pagination']['next_cursor'] = $this->nextCursor;
        }
        
        if ($this->prevCursor !== null) {
            $response['pagination']['previous_cursor'] = $this->prevCursor;
        }
        
        return array_merge($response, $additionalData);
    }
}

/**
 * InfiniteScroll helper for infinite scroll pagination.
 */
class InfiniteScroll
{
    /** @var Paginator|CursorPaginator */
    protected $paginator;
    
    /** @var string Load more button text */
    protected string $loadMoreText = 'Load More';
    
    /** @var string Loading text */
    protected string $loadingText = 'Loading...';
    
    /** @var string No more items text */
    protected string $noMoreText = 'No more items';
    
    /** @var string CSS class for container */
    protected string $containerClass = 'infinite-scroll-container';
    
    /** @var string CSS class for item */
    protected string $itemClass = 'infinite-scroll-item';
    
    /**
     * Create a new InfiniteScroll helper.
     *
     * @param Paginator|CursorPaginator $paginator Paginator instance
     */
    public function __construct($paginator)
    {
        $this->paginator = $paginator;
    }
    
    /**
     * Check if there are more items to load.
     *
     * @return bool
     */
    public function hasMore(): bool
    {
        if ($this->paginator instanceof Paginator) {
            return $this->paginator->hasNextPage();
        }
        return $this->paginator->hasNextPage();
    }
    
    /**
     * Get the next URL.
     *
     * @return string|null
     */
    public function getNextUrl(): ?string
    {
        if ($this->paginator instanceof Paginator) {
            $nextPage = $this->paginator->getNextPage();
            return $nextPage !== null ? $this->paginator->getPageUrl($nextPage) : null;
        }
        
        $cursor = $this->paginator->getNextCursor();
        return $cursor !== null ? '?cursor=' . urlencode($cursor) : null;
    }
    
    /**
     * Render the load more button HTML.
     *
     * @return string
     */
    public function renderLoadMoreButton(): string
    {
        if (!$this->hasMore()) {
            return '<div class="' . htmlspecialchars($this->containerClass) . '-empty">';
            return '<span>' . htmlspecialchars($this->noMoreText) . '</span></div>';
        }
        
        $nextUrl = $this->getNextUrl();
        
        $html = '<button class="' . htmlspecialchars($this->containerClass) . '-button" ';
        $html .= 'data-next-url="' . htmlspecialchars($nextUrl) . '" ';
        $html .= 'data-loading-text="' . htmlspecialchars($this->loadingText) . '">';
        $html .= htmlspecialchars($this->loadMoreText);
        $html .= '</button>';
        
        return $html;
    }
    
    /**
     * Render data attributes for JavaScript.
     *
     * @return string
     */
    public function renderDataAttributes(): string
    {
        $attrs = [];
        
        if ($this->hasMore()) {
            $attrs[] = 'data-has-more="true"';
            $attrs[] = 'data-next-url="' . htmlspecialchars($this->getNextUrl()) . '"';
        } else {
            $attrs[] = 'data-has-more="false"';
        }
        
        return implode(' ', $attrs);
    }
    
    /**
     * Set load more button text.
     *
     * @param string $text Button text
     * @return self
     */
    public function setLoadMoreText(string $text): self
    {
        $this->loadMoreText = $text;
        return $this;
    }
    
    /**
     * Set loading text.
     *
     * @param string $text Loading text
     * @return self
     */
    public function setLoadingText(string $text): self
    {
        $this->loadingText = $text;
        return $this;
    }
    
    /**
     * Set no more items text.
     *
     * @param string $text No more text
     * @return self
     */
    public function setNoMoreText(string $text): self
    {
        $this->noMoreText = $text;
        return $this;
    }
    
    /**
     * Set CSS classes.
     *
     * @param string $container Container class
     * @param string $item Item class
     * @return self
     */
    public function setClasses(string $container, string $item = ''): self
    {
        $this->containerClass = $container;
        if ($item !== '') {
            $this->itemClass = $item;
        }
        return $this;
    }
}

/**
 * SimplePageInfo for GraphQL-style pagination.
 */
class SimplePageInfo
{
    /**
     * Create page info for a dataset.
     *
     * @param array $items All items
     * @param int $first Number of items to take from start
     * @param string|null $after Cursor to start after
     * @param string|null $before Cursor to end before
     * @param int|null $last Number of items to take from end
     * @param callable|null $cursorGenerator Function to generate cursor from item
     * @return array PageInfo and items
     */
    public static function create(
        array $items,
        ?int $first = null,
        ?string $after = null,
        ?string $before = null,
        ?int $last = null,
        ?callable $cursorGenerator = null
    ): array {
        $generator = $cursorGenerator ?? function ($item, $index) {
            return base64_encode((string) $index);
        };
        
        $totalItems = count($items);
        $startIndex = 0;
        $endIndex = $totalItems;
        
        // Handle 'after' cursor
        if ($after !== null) {
            $afterIndex = (int) base64_decode($after);
            $startIndex = $afterIndex + 1;
        }
        
        // Handle 'before' cursor
        if ($before !== null) {
            $beforeIndex = (int) base64_decode($before);
            $endIndex = $beforeIndex;
        }
        
        // Slice items
        $slicedItems = array_slice($items, $startIndex, $endIndex - $startIndex, true);
        
        // Apply 'first' or 'last' limit
        if ($first !== null) {
            $slicedItems = array_slice($slicedItems, 0, $first, true);
        } elseif ($last !== null) {
            $slicedItems = array_slice($slicedItems, -$last, null, true);
        }
        
        $slicedItems = array_values($slicedItems);
        $itemCount = count($slicedItems);
        
        // Generate cursors
        $hasPreviousPage = $startIndex > 0 || ($last !== null && $itemCount < $totalItems);
        $hasNextPage = $endIndex < $totalItems || ($first !== null && $itemCount >= $first);
        
        $startCursor = $itemCount > 0 ? $generator($slicedItems[0], $startIndex) : null;
        $endCursor = $itemCount > 0 ? $generator($slicedItems[$itemCount - 1], $startIndex + $itemCount - 1) : null;
        
        return [
            'items' => $slicedItems,
            'pageInfo' => [
                'hasPreviousPage' => $hasPreviousPage,
                'hasNextPage' => $hasNextPage,
                'startCursor' => $startCursor,
                'endCursor' => $endCursor,
                'totalCount' => $totalItems,
            ],
        ];
    }
}

/**
 * Helper functions for common pagination tasks.
 */
class PaginationHelper
{
    /**
     * Validate page number.
     *
     * @param mixed $page Page number to validate
     * @param int $totalPages Total pages
     * @return int Valid page number
     */
    public static function validatePage($page, int $totalPages): int
    {
        $page = (int) $page;
        
        if ($page < 1) {
            return 1;
        }
        
        if ($totalPages > 0 && $page > $totalPages) {
            return $totalPages;
        }
        
        return $page;
    }
    
    /**
     * Calculate offset and limit from page and per page.
     *
     * @param int $page Page number (1-indexed)
     * @param int $perPage Items per page
     * @return array ['offset' => int, 'limit' => int]
     */
    public static function calculateOffsetLimit(int $page, int $perPage): array
    {
        return [
            'offset' => max(0, ($page - 1) * $perPage),
            'limit' => max(1, $perPage),
        ];
    }
    
    /**
     * Calculate total pages from total items and per page.
     *
     * @param int $totalItems Total number of items
     * @param int $perPage Items per page
     * @return int Total pages
     */
    public static function calculateTotalPages(int $totalItems, int $perPage): int
    {
        return (int) ceil($totalItems / max(1, $perPage));
    }
    
    /**
     * Generate page range for display.
     *
     * @param int $currentPage Current page
     * @param int $totalPages Total pages
     * @param int $range Pages on each side of current
     * @return array Array of page numbers
     */
    public static function generatePageRange(int $currentPage, int $totalPages, int $range = 2): array
    {
        if ($totalPages <= 1) {
            return [];
        }
        
        $pages = [];
        $start = max(1, $currentPage - $range);
        $end = min($totalPages, $currentPage + $range);
        
        // Adjust range if at edges
        if ($currentPage - $range < 1) {
            $end = min($totalPages, $end + (1 - ($currentPage - $range)));
        }
        if ($currentPage + $range > $totalPages) {
            $start = max(1, $start - (($currentPage + $range) - $totalPages));
        }
        
        for ($i = $start; $i <= $end; $i++) {
            $pages[] = $i;
        }
        
        return $pages;
    }
    
    /**
     * Build pagination URL.
     *
     * @param string $baseUrl Base URL
     * @param string $paramName Parameter name
     * @param int $page Page number
     * @param array $extraParams Additional parameters
     * @return string Full URL
     */
    public static function buildUrl(string $baseUrl, string $paramName, int $page, array $extraParams = []): string
    {
        $params = array_merge($extraParams, [$paramName => $page]);
        $separator = strpos($baseUrl, '?') !== false ? '&' : '?';
        return $baseUrl . $separator . http_build_query($params);
    }
}
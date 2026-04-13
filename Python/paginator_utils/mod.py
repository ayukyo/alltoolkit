"""
AllToolkit - Python Paginator Utilities

A zero-dependency, production-ready pagination utility module.
Supports offset pagination, cursor pagination, and infinite scroll helpers.
Works with any iterable and provides rich metadata.

Author: AllToolkit
License: MIT
"""

from typing import (
    Generic, TypeVar, Iterator, Optional, List, Dict, Any, 
    Callable, Iterable, Tuple, Union
)
from dataclasses import dataclass, field
from math import ceil
import hashlib
import json

T = TypeVar('T')


@dataclass
class PageMetadata:
    """Pagination metadata for a page."""
    current_page: int
    per_page: int
    total_items: int
    total_pages: int
    has_previous: bool
    has_next: bool
    previous_page: Optional[int]
    next_page: Optional[int]
    start_index: int
    end_index: int
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'current_page': self.current_page,
            'per_page': self.per_page,
            'total_items': self.total_items,
            'total_pages': self.total_pages,
            'has_previous': self.has_previous,
            'has_next': self.has_next,
            'previous_page': self.previous_page,
            'next_page': self.next_page,
            'start_index': self.start_index,
            'end_index': self.end_index,
        }


@dataclass
class PageResult(Generic[T]):
    """Result of a paginated query."""
    items: List[T]
    metadata: PageMetadata
    
    def __iter__(self):
        return iter(self.items)
    
    def __len__(self):
        return len(self.items)
    
    def __getitem__(self, index):
        return self.items[index]
    
    def to_dict(self, item_serializer: Optional[Callable[[T], Any]] = None) -> Dict[str, Any]:
        """Convert to dictionary with optional item serialization."""
        items = self.items
        if item_serializer:
            items = [item_serializer(item) for item in items]
        return {
            'items': items,
            'metadata': self.metadata.to_dict(),
        }


@dataclass
class CursorMetadata:
    """Cursor pagination metadata."""
    has_previous: bool
    has_next: bool
    start_cursor: Optional[str]
    end_cursor: Optional[str]
    per_page: int
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'has_previous': self.has_previous,
            'has_next': self.has_next,
            'start_cursor': self.start_cursor,
            'end_cursor': self.end_cursor,
            'per_page': self.per_page,
        }


@dataclass
class CursorResult(Generic[T]):
    """Result of a cursor-based paginated query."""
    items: List[T]
    metadata: CursorMetadata
    
    def __iter__(self):
        return iter(self.items)
    
    def __len__(self):
        return len(self.items)
    
    def __getitem__(self, index):
        return self.items[index]
    
    def to_dict(self, item_serializer: Optional[Callable[[T], Any]] = None) -> Dict[str, Any]:
        """Convert to dictionary with optional item serialization."""
        items = self.items
        if item_serializer:
            items = [item_serializer(item) for item in items]
        return {
            'items': items,
            'metadata': self.metadata.to_dict(),
        }


class Paginator(Generic[T]):
    """
    Offset-based paginator for any iterable.
    
    Supports both materialized (known total) and unmaterialized (unknown total) modes.
    Thread-safe for read operations.
    
    Example:
        >>> items = list(range(100))
        >>> paginator = Paginator(items, per_page=10)
        >>> page = paginator.page(1)
        >>> print(page.items)  # [0, 1, 2, ..., 9]
    """
    
    def __init__(
        self,
        items: Iterable[T],
        per_page: int = 20,
        total: Optional[int] = None,
    ):
        """
        Initialize paginator.
        
        Args:
            items: Iterable to paginate over
            per_page: Number of items per page (default: 20)
            total: Total number of items (optional, computed if not provided)
        """
        if per_page < 1:
            raise ValueError("per_page must be at least 1")
        
        self._items = items
        self._per_page = per_page
        self._total = total
        self._materialized: Optional[List[T]] = None
    
    def _materialize(self) -> List[T]:
        """Materialize items into a list if needed."""
        if self._materialized is None:
            self._materialized = list(self._items)
            if self._total is None:
                self._total = len(self._materialized)
        return self._materialized
    
    @property
    def total(self) -> int:
        """Get total number of items."""
        if self._total is not None:
            return self._total
        return len(self._materialize())
    
    @property
    def total_pages(self) -> int:
        """Get total number of pages."""
        return max(1, ceil(self.total / self._per_page))
    
    @property
    def per_page(self) -> int:
        """Get items per page."""
        return self._per_page
    
    def page(self, page_number: int) -> PageResult[T]:
        """
        Get a specific page.
        
        Args:
            page_number: 1-based page number
            
        Returns:
            PageResult with items and metadata
        """
        if page_number < 1:
            raise ValueError("page_number must be at least 1")
        
        items = self._materialize()
        total = len(items)
        total_pages = max(1, ceil(total / self._per_page))
        
        # Clamp to last page
        page_number = min(page_number, total_pages)
        
        start = (page_number - 1) * self._per_page
        end = min(start + self._per_page, total)
        
        page_items = items[start:end]
        
        metadata = PageMetadata(
            current_page=page_number,
            per_page=self._per_page,
            total_items=total,
            total_pages=total_pages,
            has_previous=page_number > 1,
            has_next=page_number < total_pages,
            previous_page=page_number - 1 if page_number > 1 else None,
            next_page=page_number + 1 if page_number < total_pages else None,
            start_index=start + 1 if page_items else 0,
            end_index=end if page_items else 0,
        )
        
        return PageResult(items=page_items, metadata=metadata)
    
    def first(self) -> PageResult[T]:
        """Get first page."""
        return self.page(1)
    
    def last(self) -> PageResult[T]:
        """Get last page."""
        return self.page(self.total_pages)
    
    def __iter__(self) -> Iterator[PageResult[T]]:
        """Iterate over all pages."""
        for page_num in range(1, self.total_pages + 1):
            yield self.page(page_num)
    
    def __len__(self) -> int:
        """Return total number of pages."""
        return self.total_pages
    
    def __getitem__(self, page_number: int) -> PageResult[T]:
        """Get a specific page using bracket notation."""
        return self.page(page_number)


class CursorPaginator(Generic[T]):
    """
    Cursor-based paginator for efficient pagination.
    
    Useful for large datasets and infinite scroll scenarios.
    Does not require knowledge of total items.
    
    Example:
        >>> items = list(range(100))
        >>> paginator = CursorPaginator(
        ...     items, 
        ...     per_page=10,
        ...     cursor_encoder=lambda x: str(x)
        ... )
        >>> result = paginator.first()
        >>> next_result = paginator.after(result.metadata.end_cursor)
    """
    
    def __init__(
        self,
        items: Iterable[T],
        per_page: int = 20,
        cursor_encoder: Optional[Callable[[T], str]] = None,
        cursor_decoder: Optional[Callable[[str], T]] = None,
        key_extractor: Optional[Callable[[T], Any]] = None,
    ):
        """
        Initialize cursor paginator.
        
        Args:
            items: Iterable to paginate over
            per_page: Number of items per page (default: 20)
            cursor_encoder: Function to encode an item as a cursor
            cursor_decoder: Function to decode a cursor back to an item
            key_extractor: Function to extract a unique key from an item
        """
        if per_page < 1:
            raise ValueError("per_page must be at least 1")
        
        self._items = items
        self._per_page = per_page
        self._materialized: Optional[List[T]] = None
        
        # Default encoder/decoder using JSON
        if cursor_encoder is None:
            def default_encoder(item: T) -> str:
                data = json.dumps(item, default=str, sort_keys=True)
                return hashlib.md5(data.encode()).hexdigest()[:16]
            cursor_encoder = default_encoder
        
        self._cursor_encoder = cursor_encoder
        self._cursor_decoder = cursor_decoder
        self._key_extractor = key_extractor
    
    def _materialize(self) -> List[T]:
        """Materialize items into a list if needed."""
        if self._materialized is None:
            self._materialized = list(self._items)
        return self._materialized
    
    @property
    def per_page(self) -> int:
        """Get items per page."""
        return self._per_page
    
    def first(self) -> CursorResult[T]:
        """Get first page."""
        return self.after(None)
    
    def after(self, cursor: Optional[str]) -> CursorResult[T]:
        """
        Get page after a cursor.
        
        Args:
            cursor: Cursor to start after (None for first page)
            
        Returns:
            CursorResult with items and metadata
        """
        items = self._materialize()
        
        # Find start index
        start_index = 0
        if cursor is not None:
            if self._cursor_decoder is None:
                # Fallback: scan for matching cursor
                for i, item in enumerate(items):
                    if self._cursor_encoder(item) == cursor:
                        start_index = i + 1
                        break
            else:
                # Use decoder to find item
                try:
                    target = self._cursor_decoder(cursor)
                    for i, item in enumerate(items):
                        if item == target:
                            start_index = i + 1
                            break
                except Exception:
                    pass
        
        # Get slice
        end_index = min(start_index + self._per_page, len(items))
        page_items = items[start_index:end_index]
        
        # Build cursors
        start_cursor = None
        end_cursor = None
        if page_items:
            start_cursor = self._cursor_encoder(page_items[0])
            end_cursor = self._cursor_encoder(page_items[-1])
        
        metadata = CursorMetadata(
            has_previous=start_index > 0,
            has_next=end_index < len(items),
            start_cursor=start_cursor,
            end_cursor=end_cursor,
            per_page=self._per_page,
        )
        
        return CursorResult(items=page_items, metadata=metadata)
    
    def before(self, cursor: Optional[str]) -> CursorResult[T]:
        """
        Get page before a cursor (for bidirectional pagination).
        
        Args:
            cursor: Cursor to start before
            
        Returns:
            CursorResult with items and metadata
        """
        items = self._materialize()
        
        # Find end index
        end_index = len(items)
        if cursor is not None:
            if self._cursor_decoder is None:
                for i, item in enumerate(items):
                    if self._cursor_encoder(item) == cursor:
                        end_index = i
                        break
            else:
                try:
                    target = self._cursor_decoder(cursor)
                    for i, item in enumerate(items):
                        if item == target:
                            end_index = i
                            break
                except Exception:
                    pass
        
        # Get slice
        start_index = max(0, end_index - self._per_page)
        page_items = items[start_index:end_index]
        
        # Build cursors
        start_cursor = None
        end_cursor = None
        if page_items:
            start_cursor = self._cursor_encoder(page_items[0])
            end_cursor = self._cursor_encoder(page_items[-1])
        
        metadata = CursorMetadata(
            has_previous=start_index > 0,
            has_next=end_index < len(items),
            start_cursor=start_cursor,
            end_cursor=end_cursor,
            per_page=self._per_page,
        )
        
        return CursorResult(items=page_items, metadata=metadata)


class InfinitePaginator(Generic[T]):
    """
    Paginator for infinite/unknown-length iterables.
    
    Useful for generators, streams, and APIs where total count is unknown.
    
    Example:
        >>> def generate_items():
        ...     for i in range(100):
        ...         yield i
        >>> paginator = InfinitePaginator(generate_items(), per_page=10)
        >>> batch1 = paginator.next_batch()
        >>> batch2 = paginator.next_batch()
    """
    
    def __init__(
        self,
        iterable: Iterable[T],
        per_page: int = 20,
    ):
        """
        Initialize infinite paginator.
        
        Args:
            iterable: Iterable to paginate over (can be generator)
            per_page: Number of items per batch (default: 20)
        """
        if per_page < 1:
            raise ValueError("per_page must be at least 1")
        
        self._iterator = iter(iterable)
        self._per_page = per_page
        self._exhausted = False
        self._batch_count = 0
        self._total_yielded = 0
    
    @property
    def per_page(self) -> int:
        """Get items per page."""
        return self._per_page
    
    @property
    def exhausted(self) -> bool:
        """Check if iterable is exhausted."""
        return self._exhausted
    
    @property
    def batch_count(self) -> int:
        """Get number of batches yielded so far."""
        return self._batch_count
    
    @property
    def total_yielded(self) -> int:
        """Get total number of items yielded so far."""
        return self._total_yielded
    
    def next_batch(self) -> List[T]:
        """
        Get next batch of items.
        
        Returns:
            List of items (may be empty if exhausted)
        """
        if self._exhausted:
            return []
        
        batch = []
        for _ in range(self._per_page):
            try:
                item = next(self._iterator)
                batch.append(item)
            except StopIteration:
                self._exhausted = True
                break
        
        self._batch_count += 1
        self._total_yielded += len(batch)
        return batch
    
    def __iter__(self) -> Iterator[List[T]]:
        """Iterate over all batches."""
        while not self._exhausted:
            batch = self.next_batch()
            if batch:
                yield batch


class Chunker(Generic[T]):
    """
    Split iterables into chunks of a specific size.
    
    Simple utility for batch processing operations.
    
    Example:
        >>> items = list(range(10))
        >>> for chunk in Chunker(items, 3):
        ...     print(chunk)
        [0, 1, 2]
        [3, 4, 5]
        [6, 7, 8]
        [9]
    """
    
    def __init__(self, iterable: Iterable[T], chunk_size: int):
        """
        Initialize chunker.
        
        Args:
            iterable: Iterable to chunk
            chunk_size: Size of each chunk
        """
        if chunk_size < 1:
            raise ValueError("chunk_size must be at least 1")
        
        self._iterable = iterable
        self._chunk_size = chunk_size
    
    @property
    def chunk_size(self) -> int:
        """Get chunk size."""
        return self._chunk_size
    
    def __iter__(self) -> Iterator[List[T]]:
        """Iterate over chunks."""
        chunk = []
        for item in self._iterable:
            chunk.append(item)
            if len(chunk) == self._chunk_size:
                yield chunk
                chunk = []
        if chunk:
            yield chunk
    
    def to_list(self) -> List[List[T]]:
        """Convert all chunks to a list."""
        return list(self)


def paginate(
    items: Iterable[T],
    page: int = 1,
    per_page: int = 20,
    total: Optional[int] = None,
) -> PageResult[T]:
    """
    Convenience function for one-off pagination.
    
    Args:
        items: Iterable to paginate over
        page: Page number (1-based)
        per_page: Items per page
        total: Total count (optional)
        
    Returns:
        PageResult with items and metadata
    """
    paginator = Paginator(items, per_page=per_page, total=total)
    return paginator.page(page)


def chunk(items: Iterable[T], chunk_size: int) -> List[List[T]]:
    """
    Convenience function for chunking an iterable.
    
    Args:
        items: Iterable to chunk
        chunk_size: Size of each chunk
        
    Returns:
        List of chunks
    """
    return Chunker(items, chunk_size).to_list()


def slice_iterable(
    items: Iterable[T],
    start: int,
    length: int,
) -> List[T]:
    """
    Slice an iterable with start and length.
    
    Useful for database-like offset/limit operations.
    
    Args:
        items: Iterable to slice
        start: Start index (0-based)
        length: Number of items to return
        
    Returns:
        List of items in the slice
    """
    if start < 0:
        raise ValueError("start must be non-negative")
    if length < 0:
        raise ValueError("length must be non-negative")
    
    result = []
    iterator = iter(items)
    
    # Skip to start
    try:
        for _ in range(start):
            next(iterator)
    except StopIteration:
        return []
    
    # Get length items
    try:
        for _ in range(length):
            result.append(next(iterator))
    except StopIteration:
        pass
    
    return result


class PaginatedResponse(Generic[T]):
    """
    Helper for building paginated API responses.
    
    Example:
        >>> response = PaginatedResponse(
        ...     items=[1, 2, 3],
        ...     page=1,
        ...     per_page=10,
        ...     total=100,
        ...     base_url='https://api.example.com/items'
        ... )
        >>> response.to_json()
        {
            'data': [1, 2, 3],
            'pagination': {
                'page': 1,
                'per_page': 10,
                'total': 100,
                'total_pages': 10,
                'has_next': True,
                'has_previous': False
            },
            'links': {
                'first': '...?page=1',
                'last': '...?page=10',
                'next': '...?page=2',
                'prev': None
            }
        }
    """
    
    def __init__(
        self,
        items: List[T],
        page: int,
        per_page: int,
        total: int,
        base_url: Optional[str] = None,
        page_param: str = 'page',
        per_page_param: str = 'per_page',
    ):
        """
        Initialize paginated response.
        
        Args:
            items: Items for current page
            page: Current page number
            per_page: Items per page
            total: Total number of items
            base_url: Base URL for generating links
            page_param: Query parameter name for page
            per_page_param: Query parameter name for per_page
        """
        self.items = items
        self.page = page
        self.per_page = per_page
        self.total = total
        self.base_url = base_url
        self.page_param = page_param
        self.per_page_param = per_page_param
    
    @property
    def total_pages(self) -> int:
        """Get total pages."""
        return max(1, ceil(self.total / self.per_page))
    
    @property
    def has_next(self) -> bool:
        """Check if there's a next page."""
        return self.page < self.total_pages
    
    @property
    def has_previous(self) -> bool:
        """Check if there's a previous page."""
        return self.page > 1
    
    def _build_url(self, page: Optional[int]) -> Optional[str]:
        """Build URL for a specific page."""
        if page is None or self.base_url is None:
            return None
        
        separator = '&' if '?' in self.base_url else '?'
        return f"{self.base_url}{separator}{self.page_param}={page}&{self.per_page_param}={self.per_page}"
    
    def to_dict(
        self, 
        item_serializer: Optional[Callable[[T], Any]] = None
    ) -> Dict[str, Any]:
        """Convert to dictionary."""
        items = self.items
        if item_serializer:
            items = [item_serializer(item) for item in items]
        
        result = {
            'data': items,
            'pagination': {
                'page': self.page,
                'per_page': self.per_page,
                'total': self.total,
                'total_pages': self.total_pages,
                'has_next': self.has_next,
                'has_previous': self.has_previous,
            },
        }
        
        if self.base_url:
            result['links'] = {
                'first': self._build_url(1),
                'last': self._build_url(self.total_pages),
                'next': self._build_url(self.page + 1) if self.has_next else None,
                'prev': self._build_url(self.page - 1) if self.has_previous else None,
            }
        
        return result
    
    def to_json(self, **kwargs) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict(), **kwargs)


# Utility functions for common pagination scenarios

def calculate_offset(page: int, per_page: int) -> int:
    """
    Calculate offset for database queries.
    
    Args:
        page: Page number (1-based)
        per_page: Items per page
        
    Returns:
        Offset value for database query
    """
    if page < 1:
        raise ValueError("page must be at least 1")
    return (page - 1) * per_page


def calculate_total_pages(total: int, per_page: int) -> int:
    """
    Calculate total number of pages.
    
    Args:
        total: Total number of items
        per_page: Items per page
        
    Returns:
        Total number of pages
    """
    if per_page < 1:
        raise ValueError("per_page must be at least 1")
    return max(1, ceil(total / per_page))


def validate_page(page: int, total_pages: int) -> int:
    """
    Validate and clamp page number to valid range.
    
    Args:
        page: Requested page number
        total_pages: Total number of pages
        
    Returns:
        Valid page number
    """
    if page < 1:
        return 1
    if page > total_pages:
        return total_pages
    return page


def page_range(
    current_page: int,
    total_pages: int,
    window: int = 2,
) -> Tuple[int, int, List[int]]:
    """
    Calculate page range with ellipsis support.
    
    Useful for rendering pagination UI.
    
    Args:
        current_page: Current page number
        total_pages: Total number of pages
        window: Number of pages to show on each side
        
    Returns:
        Tuple of (start_page, end_page, list_of_pages)
        
    Example:
        >>> page_range(5, 10, 2)
        (3, 7, [3, 4, 5, 6, 7])
        
        >>> page_range(1, 10, 2)
        (1, 3, [1, 2, 3])
        
        >>> page_range(10, 10, 2)
        (8, 10, [8, 9, 10])
    """
    start = max(1, current_page - window)
    end = min(total_pages, current_page + window)
    
    pages = list(range(start, end + 1))
    
    return start, end, pages


def ellipsis_pages(
    current_page: int,
    total_pages: int,
    window: int = 2,
) -> List[Union[int, str]]:
    """
    Generate page list with ellipsis markers.
    
    Useful for rendering pagination UI with large page counts.
    
    Args:
        current_page: Current page number
        total_pages: Total number of pages
        window: Number of pages to show on each side
        
    Returns:
        List of page numbers and '...' for ellipsis
        
    Example:
        >>> ellipsis_pages(5, 20, 2)
        [1, '...', 3, 4, 5, 6, 7, '...', 20]
    """
    if total_pages <= 7:
        return list(range(1, total_pages + 1))
    
    result = []
    
    # Always show first page
    result.append(1)
    
    start, end, pages = page_range(current_page, total_pages, window)
    
    # Add ellipsis if needed before the window
    if start > 2:
        result.append('...')
    elif start == 2:
        # Show 2 without ellipsis
        pass
    
    # Add pages in window
    for page in pages:
        if page != 1 and page != total_pages:
            result.append(page)
    
    # Add ellipsis if needed after the window
    if end < total_pages - 1:
        result.append('...')
    elif end == total_pages - 1:
        # Show n-1 without ellipsis
        result.append(total_pages - 1)
    
    # Always show last page
    if total_pages > 1:
        result.append(total_pages)
    
    return result
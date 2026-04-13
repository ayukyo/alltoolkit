"""
AllToolkit - Paginator Utilities Examples

This file demonstrates various usage patterns for the paginator utilities.
"""

import sys
sys.path.insert(0, '..')
from mod import (
    Paginator, CursorPaginator, InfinitePaginator, Chunker,
    PaginatedResponse, paginate, chunk, slice_iterable,
    calculate_offset, calculate_total_pages, page_range, ellipsis_pages,
)


def example_basic_pagination():
    """Basic offset pagination example."""
    print("=== Basic Pagination ===\n")
    
    # Create a list of items
    items = list(range(1, 101))  # Items 1-100
    
    # Create paginator with 10 items per page
    paginator = Paginator(items, per_page=10)
    
    print(f"Total items: {paginator.total}")
    print(f"Total pages: {len(paginator)}")
    print()
    
    # Get first page
    page = paginator.first()
    print(f"Page {page.metadata.current_page}:")
    print(f"  Items: {page.items}")
    print(f"  Has previous: {page.metadata.has_previous}")
    print(f"  Has next: {page.metadata.has_next}")
    print()
    
    # Get specific page
    page = paginator.page(5)
    print(f"Page {page.metadata.current_page}:")
    print(f"  Items: {page.items}")
    print(f"  Start index: {page.metadata.start_index}")
    print(f"  End index: {page.metadata.end_index}")


def example_cursor_pagination():
    """Cursor-based pagination for infinite scroll."""
    print("\n=== Cursor Pagination ===\n")
    
    items = [f"item_{i}" for i in range(50)]
    
    # Create cursor paginator
    paginator = CursorPaginator(items, per_page=10)
    
    # Get first page
    result = paginator.first()
    print(f"First page: {result.items}")
    print(f"End cursor: {result.metadata.end_cursor}")
    print()
    
    # Get next page using cursor
    result = paginator.after(result.metadata.end_cursor)
    print(f"Second page: {result.items}")
    print(f"Start cursor: {result.metadata.start_cursor}")
    print()
    
    # Navigate backward
    result = paginator.before(result.metadata.start_cursor)
    print(f"Back to first: {result.items}")


def example_infinite_pagination():
    """Pagination for generators/streams."""
    print("\n=== Infinite Pagination ===\n")
    
    # Simulate a data stream
    def data_stream():
        for i in range(25):
            yield {"id": i, "data": f"record_{i}"}
    
    paginator = InfinitePaginator(data_stream(), per_page=10)
    
    # Fetch batches
    batch_num = 1
    while not paginator.exhausted:
        batch = paginator.next_batch()
        if batch:
            print(f"Batch {batch_num}: {[item['id'] for item in batch]}")
            batch_num += 1
    
    print(f"\nTotal items yielded: {paginator.total_yielded}")


def example_chunking():
    """Chunking for batch processing."""
    print("\n=== Chunking ===\n")
    
    items = list(range(15))
    
    # Process in chunks of 4
    for i, chunk_result in enumerate(Chunker(items, 4), 1):
        print(f"Chunk {i}: {chunk_result}")
    
    # Using convenience function
    print("\nUsing chunk() function:")
    all_chunks = chunk(items, 5)
    print(f"All chunks: {all_chunks}")


def example_api_response():
    """Building paginated API responses."""
    print("\n=== API Response ===\n")
    
    # Simulate database results
    items = [
        {"id": 1, "name": "Alice", "email": "alice@example.com"},
        {"id": 2, "name": "Bob", "email": "bob@example.com"},
        {"id": 3, "name": "Charlie", "email": "charlie@example.com"},
    ]
    
    response = PaginatedResponse(
        items=items,
        page=1,
        per_page=10,
        total=100,
        base_url='https://api.example.com/users',
    )
    
    # Convert to dict for JSON response
    result = response.to_dict()
    
    print("Paginated API Response:")
    print(f"  Data: {result['data']}")
    print(f"  Pagination: {result['pagination']}")
    print(f"  Links: {result['links']}")
    
    # As JSON string
    print("\nAs JSON:")
    print(response.to_json(indent=2))


def example_database_pagination():
    """Simulating database pagination."""
    print("\n=== Database Pagination ===\n")
    
    # Calculate OFFSET and LIMIT for SQL queries
    page = 3
    per_page = 20
    total_items = 150
    
    offset = calculate_offset(page, per_page)
    total_pages = calculate_total_pages(total_items, per_page)
    
    print(f"Page {page} of {total_pages}")
    print(f"SQL: SELECT * FROM users LIMIT {per_page} OFFSET {offset}")
    print(f"Showing items {offset + 1} to {offset + per_page}")


def example_pagination_ui():
    """Generating pagination UI components."""
    print("\n=== Pagination UI ===\n")
    
    current_page = 5
    total_pages = 20
    
    # Get page range with window
    start, end, pages = page_range(current_page, total_pages, window=2)
    print(f"Current page: {current_page}")
    print(f"Visible pages: {pages}")
    
    # Generate with ellipsis
    ellipsis_result = ellipsis_pages(current_page, total_pages, window=2)
    print(f"With ellipsis: {ellipsis_result}")
    
    # Edge cases
    print("\nNear start:")
    print(f"  Page 2 of 20: {ellipsis_pages(2, 20, 2)}")
    
    print("\nNear end:")
    print(f"  Page 19 of 20: {ellipsis_pages(19, 20, 2)}")


def example_custom_cursor():
    """Custom cursor encoding for complex objects."""
    print("\n=== Custom Cursor ===\n")
    
    items = [
        {"id": i, "name": f"User_{i}", "score": i * 100}
        for i in range(20)
    ]
    
    # Custom encoder/decoder using id
    def encode_cursor(item):
        return f"id:{item['id']}"
    
    def decode_cursor(cursor):
        return {"id": int(cursor.split(":")[1])}
    
    paginator = CursorPaginator(
        items,
        per_page=5,
        cursor_encoder=encode_cursor,
        cursor_decoder=decode_cursor,
    )
    
    result = paginator.first()
    print(f"First page: {[item['name'] for item in result.items]}")
    print(f"Cursor: {result.metadata.end_cursor}")
    
    result = paginator.after(result.metadata.end_cursor)
    print(f"Next page: {[item['name'] for item in result.items]}")


def example_convenience_functions():
    """Quick one-off pagination."""
    print("\n=== Convenience Functions ===\n")
    
    items = list(range(100))
    
    # Quick pagination
    result = paginate(items, page=5, per_page=10)
    print(f"Page 5 items: {result.items}")
    
    # Quick slicing
    subset = slice_iterable(items, 50, 10)
    print(f"Items 50-59: {subset}")


def example_iteration_patterns():
    """Different iteration patterns."""
    print("\n=== Iteration Patterns ===\n")
    
    items = list(range(30))
    
    # Iterate over all pages
    print("All pages:")
    paginator = Paginator(items, per_page=10)
    for page in paginator:
        print(f"  Page {page.metadata.current_page}: {page.items}")
    
    # Batch processing
    print("\nProcessing in batches:")
    for i, batch in enumerate(Chunker(items, 7), 1):
        print(f"  Batch {i}: {batch}")


if __name__ == '__main__':
    example_basic_pagination()
    example_cursor_pagination()
    example_infinite_pagination()
    example_chunking()
    example_api_response()
    example_database_pagination()
    example_pagination_ui()
    example_custom_cursor()
    example_convenience_functions()
    example_iteration_patterns()
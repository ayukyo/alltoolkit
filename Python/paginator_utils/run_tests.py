"""Simple test runner without pytest dependency."""
import sys
import traceback

# Import the module
from mod import (
    Paginator, CursorPaginator, InfinitePaginator, Chunker,
    PageResult, PageMetadata, CursorResult, CursorMetadata,
    PaginatedResponse, paginate, chunk, slice_iterable,
    calculate_offset, calculate_total_pages, validate_page,
    page_range, ellipsis_pages,
)

test_count = 0
pass_count = 0
fail_count = 0

def assert_equal(a, b, msg=""):
    global test_count
    test_count += 1
    if a != b:
        raise AssertionError(f"Expected {b}, got {a}. {msg}")

def assert_true(condition, msg=""):
    global test_count
    test_count += 1
    if not condition:
        raise AssertionError(f"Expected True. {msg}")

def assert_raises(exception_type, func, *args, **kwargs):
    global test_count
    test_count += 1
    try:
        func(*args, **kwargs)
        raise AssertionError(f"Expected {exception_type.__name__} to be raised")
    except exception_type:
        pass

def run_test(name, func):
    global pass_count, fail_count
    try:
        func()
        pass_count += 1
        print(f"  ✓ {name}")
    except Exception as e:
        fail_count += 1
        print(f"  ✗ {name}")
        print(f"    Error: {e}")

# Tests
def test_basic_pagination():
    items = list(range(100))
    paginator = Paginator(items, per_page=10)
    assert_equal(paginator.total, 100)
    assert_equal(paginator.total_pages, 10)
    assert_equal(paginator.per_page, 10)

def test_first_page():
    items = list(range(100))
    paginator = Paginator(items, per_page=10)
    page = paginator.first()
    assert_equal(len(page.items), 10)
    assert_equal(page.items, list(range(10)))
    assert_equal(page.metadata.current_page, 1)
    assert_true(not page.metadata.has_previous)
    assert_true(page.metadata.has_next)
    assert_equal(page.metadata.previous_page, None)
    assert_equal(page.metadata.next_page, 2)

def test_last_page():
    items = list(range(100))
    paginator = Paginator(items, per_page=10)
    page = paginator.last()
    assert_equal(len(page.items), 10)
    assert_equal(page.items, list(range(90, 100)))
    assert_equal(page.metadata.current_page, 10)
    assert_true(page.metadata.has_previous)
    assert_true(not page.metadata.has_next)

def test_specific_page():
    items = list(range(100))
    paginator = Paginator(items, per_page=10)
    page = paginator.page(5)
    assert_equal(page.items, list(range(40, 50)))
    assert_equal(page.metadata.current_page, 5)

def test_page_out_of_range():
    items = list(range(100))
    paginator = Paginator(items, per_page=10)
    page = paginator.page(100)
    assert_equal(page.metadata.current_page, 10)
    assert_equal(page.items, list(range(90, 100)))

def test_invalid_page_number():
    items = list(range(100))
    paginator = Paginator(items, per_page=10)
    assert_raises(ValueError, paginator.page, 0)
    assert_raises(ValueError, paginator.page, -1)

def test_invalid_per_page():
    items = list(range(100))
    assert_raises(ValueError, Paginator, items, per_page=0)
    assert_raises(ValueError, Paginator, items, per_page=-1)

def test_empty_items():
    paginator = Paginator([], per_page=10)
    assert_equal(paginator.total, 0)
    assert_equal(paginator.total_pages, 1)
    page = paginator.first()
    assert_equal(len(page.items), 0)

def test_partial_last_page():
    items = list(range(95))
    paginator = Paginator(items, per_page=10)
    assert_equal(paginator.total_pages, 10)
    page = paginator.page(10)
    assert_equal(len(page.items), 5)
    assert_equal(page.items, list(range(90, 95)))

def test_iteration():
    items = list(range(25))
    paginator = Paginator(items, per_page=10)
    all_items = []
    for page in paginator:
        all_items.extend(page.items)
    assert_equal(all_items, items)

def test_bracket_notation():
    items = list(range(100))
    paginator = Paginator(items, per_page=10)
    page = paginator[3]
    assert_equal(page.metadata.current_page, 3)
    assert_equal(page.items, list(range(20, 30)))

def test_len():
    items = list(range(100))
    paginator = Paginator(items, per_page=10)
    assert_equal(len(paginator), 10)

def test_metadata_to_dict():
    items = list(range(100))
    paginator = Paginator(items, per_page=10)
    page = paginator.page(1)
    meta_dict = page.metadata.to_dict()
    assert_equal(meta_dict['current_page'], 1)
    assert_equal(meta_dict['per_page'], 10)
    assert_equal(meta_dict['total_items'], 100)
    assert_equal(meta_dict['total_pages'], 10)

def test_page_result_to_dict():
    items = list(range(100))
    paginator = Paginator(items, per_page=10)
    page = paginator.page(1)
    result_dict = page.to_dict()
    assert_true('items' in result_dict)
    assert_true('metadata' in result_dict)
    assert_equal(result_dict['items'], list(range(10)))

def test_cursor_basic():
    items = list(range(100))
    paginator = CursorPaginator(items, per_page=10)
    result = paginator.first()
    assert_equal(len(result.items), 10)
    assert_equal(result.items, list(range(10)))
    assert_true(not result.metadata.has_previous)
    assert_true(result.metadata.has_next)

def test_cursor_after():
    items = list(range(100))
    paginator = CursorPaginator(items, per_page=10)
    first = paginator.first()
    second = paginator.after(first.metadata.end_cursor)
    assert_equal(second.items, list(range(10, 20)))
    assert_true(second.metadata.has_previous)

def test_cursor_last_page():
    items = list(range(25))
    paginator = CursorPaginator(items, per_page=10)
    first = paginator.first()
    second = paginator.after(first.metadata.end_cursor)
    third = paginator.after(second.metadata.end_cursor)
    assert_equal(len(third.items), 5)
    assert_true(not third.metadata.has_next)

def test_infinite_paginator():
    items = range(100)
    paginator = InfinitePaginator(items, per_page=10)
    batch1 = paginator.next_batch()
    assert_equal(len(batch1), 10)
    assert_equal(batch1, list(range(10)))
    assert_true(not paginator.exhausted)

def test_infinite_exhausted():
    items = range(25)
    paginator = InfinitePaginator(items, per_page=10)
    paginator.next_batch()
    paginator.next_batch()
    paginator.next_batch()
    batch4 = paginator.next_batch()
    assert_equal(len(batch4), 0)
    assert_true(paginator.exhausted)

def test_chunker():
    items = list(range(10))
    chunks = list(Chunker(items, 3))
    assert_equal(chunks, [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]])

def test_chunker_to_list():
    items = list(range(10))
    chunks = Chunker(items, 3).to_list()
    assert_equal(chunks, [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]])

def test_invalid_chunk_size():
    assert_raises(ValueError, Chunker, [], 0)
    assert_raises(ValueError, Chunker, [], -1)

def test_paginate_function():
    items = list(range(100))
    result = paginate(items, page=3, per_page=10)
    assert_equal(result.items, list(range(20, 30)))
    assert_equal(result.metadata.current_page, 3)

def test_chunk_function():
    items = list(range(10))
    chunks = chunk(items, 3)
    assert_equal(chunks, [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]])

def test_slice_iterable():
    items = list(range(100))
    result = slice_iterable(items, 10, 5)
    assert_equal(result, list(range(10, 15)))

def test_calculate_offset():
    assert_equal(calculate_offset(1, 10), 0)
    assert_equal(calculate_offset(2, 10), 10)
    assert_equal(calculate_offset(3, 20), 40)

def test_calculate_offset_invalid():
    assert_raises(ValueError, calculate_offset, 0, 10)

def test_calculate_total_pages():
    assert_equal(calculate_total_pages(100, 10), 10)
    assert_equal(calculate_total_pages(95, 10), 10)
    assert_equal(calculate_total_pages(10, 10), 1)
    assert_equal(calculate_total_pages(5, 10), 1)

def test_validate_page():
    assert_equal(validate_page(5, 10), 5)
    assert_equal(validate_page(0, 10), 1)
    assert_equal(validate_page(-1, 10), 1)
    assert_equal(validate_page(15, 10), 10)

def test_page_range():
    start, end, pages = page_range(5, 10, 2)
    assert_equal(pages, [3, 4, 5, 6, 7])

def test_ellipsis_pages():
    pages = ellipsis_pages(5, 7, 2)
    assert_equal(pages, [1, 2, 3, 4, 5, 6, 7])
    
    pages = ellipsis_pages(5, 20, 2)
    assert_equal(pages, [1, '...', 3, 4, 5, 6, 7, '...', 20])

def test_paginated_response():
    response = PaginatedResponse(
        items=[1, 2, 3],
        page=1,
        per_page=10,
        total=100,
    )
    assert_equal(response.total_pages, 10)
    assert_true(response.has_next)
    assert_true(not response.has_previous)

def test_paginated_response_to_dict():
    response = PaginatedResponse(
        items=[1, 2, 3],
        page=2,
        per_page=10,
        total=25,
    )
    result = response.to_dict()
    assert_equal(result['data'], [1, 2, 3])
    assert_equal(result['pagination']['page'], 2)
    assert_equal(result['pagination']['total_pages'], 3)

def test_paginated_response_with_links():
    response = PaginatedResponse(
        items=[1, 2, 3],
        page=2,
        per_page=10,
        total=100,
        base_url='https://api.example.com/items',
    )
    result = response.to_dict()
    assert_true('links' in result)
    assert_equal(result['links']['first'], 'https://api.example.com/items?page=1&per_page=10')
    assert_equal(result['links']['last'], 'https://api.example.com/items?page=10&per_page=10')

def test_paginated_response_to_json():
    response = PaginatedResponse(
        items=[1, 2, 3],
        page=1,
        per_page=10,
        total=25,
    )
    json_str = response.to_json()
    assert_true('"data"' in json_str)
    assert_true('"pagination"' in json_str)

def test_precomputed_total():
    items = range(1000)
    paginator = Paginator(items, per_page=10, total=1000)
    assert_equal(paginator.total, 1000)
    assert_equal(paginator.total_pages, 100)

def test_page_result_iteration():
    items = list(range(10))
    paginator = Paginator(items, per_page=5)
    page = paginator.page(1)
    result = list(page)
    assert_equal(result, [0, 1, 2, 3, 4])

def test_page_result_index():
    items = list(range(10))
    paginator = Paginator(items, per_page=5)
    page = paginator.page(1)
    assert_equal(page[0], 0)
    assert_equal(page[2], 2)
    assert_equal(page[-1], 4)

# Run all tests
if __name__ == '__main__':
    tests = [
        ("basic_pagination", test_basic_pagination),
        ("first_page", test_first_page),
        ("last_page", test_last_page),
        ("specific_page", test_specific_page),
        ("page_out_of_range", test_page_out_of_range),
        ("invalid_page_number", test_invalid_page_number),
        ("invalid_per_page", test_invalid_per_page),
        ("empty_items", test_empty_items),
        ("partial_last_page", test_partial_last_page),
        ("iteration", test_iteration),
        ("bracket_notation", test_bracket_notation),
        ("len", test_len),
        ("metadata_to_dict", test_metadata_to_dict),
        ("page_result_to_dict", test_page_result_to_dict),
        ("cursor_basic", test_cursor_basic),
        ("cursor_after", test_cursor_after),
        ("cursor_last_page", test_cursor_last_page),
        ("infinite_paginator", test_infinite_paginator),
        ("infinite_exhausted", test_infinite_exhausted),
        ("chunker", test_chunker),
        ("chunker_to_list", test_chunker_to_list),
        ("invalid_chunk_size", test_invalid_chunk_size),
        ("paginate_function", test_paginate_function),
        ("chunk_function", test_chunk_function),
        ("slice_iterable", test_slice_iterable),
        ("calculate_offset", test_calculate_offset),
        ("calculate_offset_invalid", test_calculate_offset_invalid),
        ("calculate_total_pages", test_calculate_total_pages),
        ("validate_page", test_validate_page),
        ("page_range", test_page_range),
        ("ellipsis_pages", test_ellipsis_pages),
        ("paginated_response", test_paginated_response),
        ("paginated_response_to_dict", test_paginated_response_to_dict),
        ("paginated_response_with_links", test_paginated_response_with_links),
        ("paginated_response_to_json", test_paginated_response_to_json),
        ("precomputed_total", test_precomputed_total),
        ("page_result_iteration", test_page_result_iteration),
        ("page_result_index", test_page_result_index),
    ]
    
    print(f"\n{'='*50}")
    print("AllToolkit - Paginator Utilities Tests")
    print(f"{'='*50}\n")
    
    for name, func in tests:
        run_test(name, func)
    
    print(f"\n{'='*50}")
    print(f"Results: {pass_count}/{len(tests)} passed, {fail_count} failed")
    print(f"{'='*50}\n")
    
    sys.exit(0 if fail_count == 0 else 1)

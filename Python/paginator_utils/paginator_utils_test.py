"""
AllToolkit - Paginator Utilities Tests

Comprehensive tests for pagination utilities.
Run with: python paginator_utils_test.py
"""

from typing import List
from mod import (
    Paginator, CursorPaginator, InfinitePaginator, Chunker,
    PageResult, PageMetadata, CursorResult, CursorMetadata,
    PaginatedResponse, paginate, chunk, slice_iterable,
    calculate_offset, calculate_total_pages, validate_page,
    page_range, ellipsis_pages,
)


class TestPaginator:
    """Tests for Paginator class."""
    
    def test_basic_pagination(self):
        """Test basic pagination functionality."""
        items = list(range(100))
        paginator = Paginator(items, per_page=10)
        
        assert paginator.total == 100
        assert paginator.total_pages == 10
        assert paginator.per_page == 10
    
    def test_first_page(self):
        """Test getting first page."""
        items = list(range(100))
        paginator = Paginator(items, per_page=10)
        page = paginator.first()
        
        assert len(page.items) == 10
        assert page.items == list(range(10))
        assert page.metadata.current_page == 1
        assert page.metadata.has_previous is False
        assert page.metadata.has_next is True
        assert page.metadata.previous_page is None
        assert page.metadata.next_page == 2
    
    def test_last_page(self):
        """Test getting last page."""
        items = list(range(100))
        paginator = Paginator(items, per_page=10)
        page = paginator.last()
        
        assert len(page.items) == 10
        assert page.items == list(range(90, 100))
        assert page.metadata.current_page == 10
        assert page.metadata.has_previous is True
        assert page.metadata.has_next is False
    
    def test_specific_page(self):
        """Test getting a specific page."""
        items = list(range(100))
        paginator = Paginator(items, per_page=10)
        page = paginator.page(5)
        
        assert page.items == list(range(40, 50))
        assert page.metadata.current_page == 5
    
    def test_page_out_of_range(self):
        """Test page number beyond total pages."""
        items = list(range(100))
        paginator = Paginator(items, per_page=10)
        page = paginator.page(100)  # Beyond range
        
        # Should return last page
        assert page.metadata.current_page == 10
        assert page.items == list(range(90, 100))
    
    def test_invalid_page_number(self):
        """Test invalid page number raises error."""
        items = list(range(100))
        paginator = Paginator(items, per_page=10)
        
        with pytest.raises(ValueError):
            paginator.page(0)
        
        with pytest.raises(ValueError):
            paginator.page(-1)
    
    def test_invalid_per_page(self):
        """Test invalid per_page value."""
        items = list(range(100))
        
        with pytest.raises(ValueError):
            Paginator(items, per_page=0)
        
        with pytest.raises(ValueError):
            Paginator(items, per_page=-1)
    
    def test_empty_items(self):
        """Test pagination with empty items."""
        paginator = Paginator([], per_page=10)
        
        assert paginator.total == 0
        assert paginator.total_pages == 1  # At least 1 page
        
        page = paginator.first()
        assert len(page.items) == 0
    
    def test_partial_last_page(self):
        """Test partial last page."""
        items = list(range(95))
        paginator = Paginator(items, per_page=10)
        
        assert paginator.total_pages == 10
        
        page = paginator.page(10)
        assert len(page.items) == 5
        assert page.items == list(range(90, 95))
    
    def test_iteration(self):
        """Test iterating over all pages."""
        items = list(range(25))
        paginator = Paginator(items, per_page=10)
        
        all_items = []
        for page in paginator:
            all_items.extend(page.items)
        
        assert all_items == items
    
    def test_bracket_notation(self):
        """Test bracket notation for page access."""
        items = list(range(100))
        paginator = Paginator(items, per_page=10)
        
        page = paginator[3]
        assert page.metadata.current_page == 3
        assert page.items == list(range(20, 30))
    
    def test_len(self):
        """Test len returns total pages."""
        items = list(range(100))
        paginator = Paginator(items, per_page=10)
        
        assert len(paginator) == 10
    
    def test_metadata_to_dict(self):
        """Test metadata serialization."""
        items = list(range(100))
        paginator = Paginator(items, per_page=10)
        page = paginator.page(1)
        
        meta_dict = page.metadata.to_dict()
        
        assert meta_dict['current_page'] == 1
        assert meta_dict['per_page'] == 10
        assert meta_dict['total_items'] == 100
        assert meta_dict['total_pages'] == 10
        assert meta_dict['has_previous'] is False
        assert meta_dict['has_next'] is True
    
    def test_page_result_to_dict(self):
        """Test PageResult serialization."""
        items = list(range(100))
        paginator = Paginator(items, per_page=10)
        page = paginator.page(1)
        
        result_dict = page.to_dict()
        
        assert 'items' in result_dict
        assert 'metadata' in result_dict
        assert result_dict['items'] == list(range(10))
    
    def test_page_result_with_serializer(self):
        """Test PageResult with custom serializer."""
        items = [{'id': i, 'name': f'item_{i}'} for i in range(10)]
        paginator = Paginator(items, per_page=5)
        page = paginator.page(1)
        
        result_dict = page.to_dict(item_serializer=lambda x: {'id': x['id']})
        
        assert result_dict['items'][0] == {'id': 0}
    
    def test_precomputed_total(self):
        """Test with precomputed total."""
        items = range(1000)  # Lazy range
        paginator = Paginator(items, per_page=10, total=1000)
        
        assert paginator.total == 1000
        assert paginator.total_pages == 100


class TestCursorPaginator:
    """Tests for CursorPaginator class."""
    
    def test_basic_cursor_pagination(self):
        """Test basic cursor pagination."""
        items = list(range(100))
        paginator = CursorPaginator(items, per_page=10)
        
        result = paginator.first()
        
        assert len(result.items) == 10
        assert result.items == list(range(10))
        assert result.metadata.has_previous is False
        assert result.metadata.has_next is True
    
    def test_pagination_after_cursor(self):
        """Test pagination after a cursor."""
        items = list(range(100))
        paginator = CursorPaginator(items, per_page=10)
        
        first = paginator.first()
        assert first.metadata.end_cursor is not None
        
        second = paginator.after(first.metadata.end_cursor)
        assert second.items == list(range(10, 20))
        assert second.metadata.has_previous is True
        assert second.metadata.has_next is True
    
    def test_pagination_before_cursor(self):
        """Test pagination before a cursor."""
        items = list(range(100))
        paginator = CursorPaginator(items, per_page=10)
        
        first = paginator.first()
        second = paginator.after(first.metadata.end_cursor)
        
        # Go back to first page
        back = paginator.before(second.metadata.start_cursor)
        assert back.items == list(range(10))
    
    def test_last_page(self):
        """Test cursor pagination at last page."""
        items = list(range(25))
        paginator = CursorPaginator(items, per_page=10)
        
        first = paginator.first()
        second = paginator.after(first.metadata.end_cursor)
        third = paginator.after(second.metadata.end_cursor)
        
        assert len(third.items) == 5
        assert third.metadata.has_next is False
    
    def test_empty_items(self):
        """Test cursor pagination with empty items."""
        paginator = CursorPaginator([], per_page=10)
        
        result = paginator.first()
        
        assert len(result.items) == 0
        assert result.metadata.has_previous is False
        assert result.metadata.has_next is False
        assert result.metadata.start_cursor is None
        assert result.metadata.end_cursor is None
    
    def test_custom_cursor_encoder(self):
        """Test with custom cursor encoder."""
        items = list(range(100))
        
        def encoder(x):
            return f"cursor_{x}"
        
        def decoder(x):
            return int(x.replace("cursor_", ""))
        
        paginator = CursorPaginator(
            items, 
            per_page=10,
            cursor_encoder=encoder,
            cursor_decoder=decoder,
        )
        
        first = paginator.first()
        assert first.metadata.start_cursor == "cursor_0"
        assert first.metadata.end_cursor == "cursor_9"
        
        second = paginator.after(first.metadata.end_cursor)
        assert second.items == list(range(10, 20))
    
    def test_cursor_metadata_to_dict(self):
        """Test cursor metadata serialization."""
        items = list(range(100))
        paginator = CursorPaginator(items, per_page=10)
        result = paginator.first()
        
        meta_dict = result.metadata.to_dict()
        
        assert meta_dict['has_previous'] is False
        assert meta_dict['has_next'] is True
        assert meta_dict['per_page'] == 10
    
    def test_cursor_result_iteration(self):
        """Test cursor result iteration."""
        items = list(range(25))
        paginator = CursorPaginator(items, per_page=10)
        
        result = paginator.first()
        
        # Test iteration
        items_list = list(result)
        assert items_list == list(range(10))
        
        # Test len
        assert len(result) == 10


class TestInfinitePaginator:
    """Tests for InfinitePaginator class."""
    
    def test_basic_infinite_pagination(self):
        """Test basic infinite pagination."""
        items = range(100)
        paginator = InfinitePaginator(items, per_page=10)
        
        batch1 = paginator.next_batch()
        assert len(batch1) == 10
        assert batch1 == list(range(10))
        assert paginator.exhausted is False
        assert paginator.batch_count == 1
    
    def test_pagination_until_exhausted(self):
        """Test pagination until exhausted."""
        items = range(25)
        paginator = InfinitePaginator(items, per_page=10)
        
        batch1 = paginator.next_batch()
        batch2 = paginator.next_batch()
        batch3 = paginator.next_batch()
        batch4 = paginator.next_batch()  # Should be empty
        
        assert len(batch1) == 10
        assert len(batch2) == 10
        assert len(batch3) == 5
        assert len(batch4) == 0
        assert paginator.exhausted is True
    
    def test_iteration_over_batches(self):
        """Test iterating over all batches."""
        items = range(25)
        paginator = InfinitePaginator(items, per_page=10)
        
        all_items = []
        for batch in paginator:
            all_items.extend(batch)
        
        assert all_items == list(range(25))
    
    def test_with_generator(self):
        """Test with generator input."""
        def generate_items():
            for i in range(15):
                yield i
        
        paginator = InfinitePaginator(generate_items(), per_page=5)
        
        batch1 = paginator.next_batch()
        batch2 = paginator.next_batch()
        batch3 = paginator.next_batch()
        
        assert batch1 == [0, 1, 2, 3, 4]
        assert batch2 == [5, 6, 7, 8, 9]
        assert batch3 == [10, 11, 12, 13, 14]
    
    def test_total_yielded(self):
        """Test total_yielded counter."""
        items = range(25)
        paginator = InfinitePaginator(items, per_page=10)
        
        paginator.next_batch()
        assert paginator.total_yielded == 10
        
        paginator.next_batch()
        assert paginator.total_yielded == 20
        
        paginator.next_batch()
        assert paginator.total_yielded == 25


class TestChunker:
    """Tests for Chunker class."""
    
    def test_basic_chunking(self):
        """Test basic chunking."""
        items = list(range(10))
        chunks = list(Chunker(items, 3))
        
        assert chunks == [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]]
    
    def test_even_chunks(self):
        """Test chunking with even division."""
        items = list(range(12))
        chunks = list(Chunker(items, 3))
        
        assert chunks == [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9, 10, 11]]
    
    def test_empty_items(self):
        """Test chunking empty items."""
        chunks = list(Chunker([], 5))
        assert chunks == []
    
    def test_single_chunk(self):
        """Test with chunk size larger than items."""
        items = list(range(5))
        chunks = list(Chunker(items, 10))
        
        assert chunks == [[0, 1, 2, 3, 4]]
    
    def test_invalid_chunk_size(self):
        """Test invalid chunk size."""
        with pytest.raises(ValueError):
            Chunker([], 0)
        
        with pytest.raises(ValueError):
            Chunker([], -1)
    
    def test_to_list(self):
        """Test to_list method."""
        items = list(range(10))
        chunks = Chunker(items, 3).to_list()
        
        assert chunks == [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]]
    
    def test_chunk_size_property(self):
        """Test chunk_size property."""
        chunker = Chunker(list(range(10)), 5)
        assert chunker.chunk_size == 5


class TestUtilityFunctions:
    """Tests for utility functions."""
    
    def test_paginate_function(self):
        """Test paginate convenience function."""
        items = list(range(100))
        result = paginate(items, page=3, per_page=10)
        
        assert result.items == list(range(20, 30))
        assert result.metadata.current_page == 3
    
    def test_chunk_function(self):
        """Test chunk convenience function."""
        items = list(range(10))
        chunks = chunk(items, 3)
        
        assert chunks == [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]]
    
    def test_slice_iterable(self):
        """Test slice_iterable function."""
        items = list(range(100))
        
        result = slice_iterable(items, 10, 5)
        assert result == list(range(10, 15))
    
    def test_slice_iterable_from_start(self):
        """Test slice_iterable from start."""
        items = list(range(100))
        result = slice_iterable(items, 0, 10)
        assert result == list(range(10))
    
    def test_slice_iterable_beyond_range(self):
        """Test slice_iterable beyond range."""
        items = list(range(10))
        result = slice_iterable(items, 5, 10)
        assert result == [5, 6, 7, 8, 9]
    
    def test_slice_iterable_invalid(self):
        """Test slice_iterable with invalid inputs."""
        with pytest.raises(ValueError):
            slice_iterable([], -1, 5)
        
        with pytest.raises(ValueError):
            slice_iterable([], 0, -1)
    
    def test_calculate_offset(self):
        """Test calculate_offset function."""
        assert calculate_offset(1, 10) == 0
        assert calculate_offset(2, 10) == 10
        assert calculate_offset(3, 20) == 40
    
    def test_calculate_offset_invalid(self):
        """Test calculate_offset with invalid page."""
        with pytest.raises(ValueError):
            calculate_offset(0, 10)
    
    def test_calculate_total_pages(self):
        """Test calculate_total_pages function."""
        assert calculate_total_pages(100, 10) == 10
        assert calculate_total_pages(95, 10) == 10
        assert calculate_total_pages(10, 10) == 1
        assert calculate_total_pages(5, 10) == 1
    
    def test_calculate_total_pages_invalid(self):
        """Test calculate_total_pages with invalid per_page."""
        with pytest.raises(ValueError):
            calculate_total_pages(100, 0)
    
    def test_validate_page(self):
        """Test validate_page function."""
        assert validate_page(5, 10) == 5
        assert validate_page(0, 10) == 1
        assert validate_page(-1, 10) == 1
        assert validate_page(15, 10) == 10
    
    def test_page_range(self):
        """Test page_range function."""
        start, end, pages = page_range(5, 10, 2)
        assert pages == [3, 4, 5, 6, 7]
        
        start, end, pages = page_range(1, 10, 2)
        assert pages == [1, 2, 3]
        
        start, end, pages = page_range(10, 10, 2)
        assert pages == [8, 9, 10]
    
    def test_ellipsis_pages(self):
        """Test ellipsis_pages function."""
        # Small total - no ellipsis
        pages = ellipsis_pages(5, 7, 2)
        assert pages == [1, 2, 3, 4, 5, 6, 7]
        
        # Large total with ellipsis
        pages = ellipsis_pages(5, 20, 2)
        assert pages == [1, '...', 3, 4, 5, 6, 7, '...', 20]
        
        # Near start
        pages = ellipsis_pages(2, 20, 2)
        assert pages == [1, 2, 3, 4, '...', 20]
        
        # Near end
        pages = ellipsis_pages(18, 20, 2)
        assert pages == [1, '...', 16, 17, 18, 19, 20]


class TestPaginatedResponse:
    """Tests for PaginatedResponse class."""
    
    def test_basic_response(self):
        """Test basic paginated response."""
        response = PaginatedResponse(
            items=[1, 2, 3],
            page=1,
            per_page=10,
            total=100,
        )
        
        assert response.total_pages == 10
        assert response.has_next is True
        assert response.has_previous is False
    
    def test_to_dict(self):
        """Test response serialization."""
        response = PaginatedResponse(
            items=[1, 2, 3],
            page=1,
            per_page=10,
            total=25,
        )
        
        result = response.to_dict()
        
        assert result['data'] == [1, 2, 3]
        assert result['pagination']['page'] == 1
        assert result['pagination']['total'] == 25
        assert result['pagination']['total_pages'] == 3
    
    def test_to_dict_with_links(self):
        """Test response with links."""
        response = PaginatedResponse(
            items=[1, 2, 3],
            page=2,
            per_page=10,
            total=100,
            base_url='https://api.example.com/items',
        )
        
        result = response.to_dict()
        
        assert 'links' in result
        assert result['links']['first'] == 'https://api.example.com/items?page=1&per_page=10'
        assert result['links']['last'] == 'https://api.example.com/items?page=10&per_page=10'
        assert result['links']['next'] == 'https://api.example.com/items?page=3&per_page=10'
        assert result['links']['prev'] == 'https://api.example.com/items?page=1&per_page=10'
    
    def test_to_json(self):
        """Test JSON serialization."""
        response = PaginatedResponse(
            items=[1, 2, 3],
            page=1,
            per_page=10,
            total=25,
        )
        
        json_str = response.to_json()
        
        assert '"data"' in json_str
        assert '"pagination"' in json_str
    
    def test_with_custom_serializer(self):
        """Test with custom item serializer."""
        response = PaginatedResponse(
            items=[{'id': i, 'name': f'item_{i}'} for i in range(3)],
            page=1,
            per_page=10,
            total=100,
        )
        
        result = response.to_dict(item_serializer=lambda x: {'id': x['id']})
        
        assert result['data'][0] == {'id': 0}


class TestPageResultIteration:
    """Tests for PageResult iteration behavior."""
    
    def test_iterate_page_result(self):
        """Test iterating over PageResult items."""
        items = list(range(10))
        paginator = Paginator(items, per_page=5)
        page = paginator.page(1)
        
        result = list(page)
        assert result == [0, 1, 2, 3, 4]
    
    def test_index_page_result(self):
        """Test indexing PageResult."""
        items = list(range(10))
        paginator = Paginator(items, per_page=5)
        page = paginator.page(1)
        
        assert page[0] == 0
        assert page[2] == 2
        assert page[-1] == 4
    
    def test_len_page_result(self):
        """Test len of PageResult."""
        items = list(range(10))
        paginator = Paginator(items, per_page=5)
        page = paginator.page(1)
        
        assert len(page) == 5


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
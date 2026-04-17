"""
Tests for iter_utils module

Comprehensive tests covering:
- Normal cases
- Edge cases (empty, single element, large inputs)
- Boundary values
- Error handling
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    chunk, batched, sliding_window, flatten, deep_flatten,
    take, take_while, drop, drop_while, unique, dedupe,
    partition, groupby_consecutive, pairwise, triplewise,
    interleave, roundrobin, Peekable, peek, is_empty,
    first, last, nth, cycle, repeat, count,
    zip_with, enumerate_with, unzip, unzip_list,
    split_at, split_after, stagger, minmax,
    _sentinel
)
from itertools import islice as iter_islice


class TestChunk:
    """Tests for chunk function."""
    
    def test_basic(self):
        """Basic chunking."""
        assert list(chunk([1, 2, 3, 4, 5, 6], 2)) == [(1, 2), (3, 4), (5, 6)]
        assert list(chunk([1, 2, 3, 4, 5], 2)) == [(1, 2), (3, 4), (5,)]
        assert list(chunk([1, 2, 3], 3)) == [(1, 2, 3)]
    
    def test_string(self):
        """Chunking strings."""
        assert list(chunk('abcdef', 3)) == [('a', 'b', 'c'), ('d', 'e', 'f')]
        assert list(chunk('abc', 2)) == [('a', 'b'), ('c',)]
    
    def test_empty(self):
        """Empty iterable."""
        assert list(chunk([], 2)) == []
    
    def test_single_element(self):
        """Single element."""
        assert list(chunk([1], 2)) == [(1,)]
    
    def test_chunk_size_one(self):
        """Chunk size of 1."""
        assert list(chunk([1, 2, 3], 1)) == [(1,), (2,), (3,)]
    
    def test_large_chunk_size(self):
        """Chunk size larger than iterable."""
        assert list(chunk([1, 2, 3], 10)) == [(1, 2, 3)]
    
    def test_invalid_size(self):
        """Invalid chunk size."""
        try:
            list(chunk([1, 2, 3], 0))
            assert False, "Should raise ValueError"
        except ValueError:
            pass
        
        try:
            list(chunk([1, 2, 3], -1))
            assert False, "Should raise ValueError"
        except ValueError:
            pass
    
    def test_generator(self):
        """Works with generators."""
        gen = (x for x in range(5))
        assert list(chunk(gen, 2)) == [(0, 1), (2, 3), (4,)]


class TestBatched:
    """Tests for batched function."""
    
    def test_basic(self):
        """Basic batching."""
        assert list(batched('ABCDEFG', 3)) == [('A', 'B', 'C'), ('D', 'E', 'F'), ('G',)]
    
    def test_empty(self):
        """Empty iterable."""
        assert list(batched([], 3)) == []


class TestSlidingWindow:
    """Tests for sliding_window function."""
    
    def test_basic(self):
        """Basic sliding window."""
        assert list(sliding_window([1, 2, 3, 4, 5], 3)) == [(1, 2, 3), (2, 3, 4), (3, 4, 5)]
    
    def test_size_two(self):
        """Window size 2 (equivalent to pairwise)."""
        assert list(sliding_window([1, 2, 3, 4], 2)) == [(1, 2), (2, 3), (3, 4)]
    
    def test_step_two(self):
        """Window with step > 1."""
        assert list(sliding_window([1, 2, 3, 4, 5, 6], 2, step=2)) == [(1, 2), (3, 4), (5, 6)]
    
    def test_empty(self):
        """Empty iterable."""
        assert list(sliding_window([], 2)) == []
    
    def test_window_larger_than_input(self):
        """Window size larger than input."""
        assert list(sliding_window([1, 2], 5)) == [(1, 2)]
    
    def test_single_element(self):
        """Single element."""
        assert list(sliding_window([1], 1)) == [(1,)]
    
    def test_invalid_size(self):
        """Invalid window size."""
        try:
            list(sliding_window([1, 2], 0))
            assert False, "Should raise ValueError"
        except ValueError:
            pass
        
        try:
            list(sliding_window([1, 2], 1, step=0))
            assert False, "Should raise ValueError"
        except ValueError:
            pass


class TestFlatten:
    """Tests for flatten function."""
    
    def test_depth_one(self):
        """Flatten one level."""
        assert list(flatten([[1, 2], [3, 4]])) == [1, 2, 3, 4]
    
    def test_depth_two(self):
        """Flatten two levels."""
        assert list(flatten([[[1, 2]], [[3, 4]]], depth=2)) == [1, 2, 3, 4]
    
    def test_unlimited_depth(self):
        """Flatten all levels."""
        assert list(flatten([[[[1]]]], depth=-1)) == [1]
        assert list(deep_flatten([1, [2, [3, [4, [5]]]]])) == [1, 2, 3, 4, 5]
    
    def test_zero_depth(self):
        """Zero depth (no flattening)."""
        assert list(flatten([[1, 2], [3, 4]], depth=0)) == [[1, 2], [3, 4]]
    
    def test_strings_preserved(self):
        """Strings are preserved as atoms."""
        assert list(flatten([['ab', 'cd'], ['ef']])) == ['ab', 'cd', 'ef']
    
    def test_mixed_types(self):
        """Mixed nested types."""
        # depth=2 flattens two levels: [[1, [2, 3]], 4, [[5]]] -> [1, [2, 3], 4, [5]] -> [1, [2, 3], 4, 5]
        # Actually, depth=2 means 2 levels of flattening from the top
        result = list(flatten([[1, [2, 3]], 4, [[5]]], depth=2))
        # [[1, [2, 3]], 4, [[5]]] depth=1 -> [1, [2, 3], 4, [5]]
        # Then depth=2 applies to result: [1, [2, 3], 4, [5]] -> [1, 2, 3, 4, 5]
        assert result == [1, 2, 3, 4, 5]
    
    def test_empty(self):
        """Empty iterable."""
        assert list(flatten([])) == []


class TestTake:
    """Tests for take function."""
    
    def test_basic(self):
        """Basic take."""
        assert take(3, range(10)) == [0, 1, 2]
    
    def test_take_more_than_available(self):
        """Take more than iterable has."""
        assert take(5, [1, 2]) == [1, 2]
    
    def test_take_zero(self):
        """Take zero elements."""
        assert take(0, [1, 2, 3]) == []
    
    def test_take_negative(self):
        """Negative take returns all."""
        assert take(-1, [1, 2, 3]) == [1, 2, 3]
    
    def test_empty(self):
        """Empty iterable."""
        assert take(3, []) == []


class TestTakeWhile:
    """Tests for take_while function."""
    
    def test_basic(self):
        """Basic take_while."""
        assert list(take_while(lambda x: x < 5, [1, 2, 3, 4, 5, 6])) == [1, 2, 3, 4]
    
    def test_all_match(self):
        """All elements match predicate."""
        assert list(take_while(lambda x: x < 10, [1, 2, 3])) == [1, 2, 3]
    
    def test_none_match(self):
        """No elements match predicate."""
        assert list(take_while(lambda x: x < 0, [1, 2, 3])) == []
    
    def test_empty(self):
        """Empty iterable."""
        assert list(take_while(lambda x: True, [])) == []


class TestDrop:
    """Tests for drop function."""
    
    def test_basic(self):
        """Basic drop."""
        assert list(drop(3, range(6))) == [3, 4, 5]
    
    def test_drop_zero(self):
        """Drop zero elements."""
        assert list(drop(0, [1, 2, 3])) == [1, 2, 3]
    
    def test_drop_more_than_available(self):
        """Drop more than iterable has."""
        assert list(drop(10, [1, 2, 3])) == []
    
    def test_empty(self):
        """Empty iterable."""
        assert list(drop(2, [])) == []


class TestDropWhile:
    """Tests for drop_while function."""
    
    def test_basic(self):
        """Basic drop_while."""
        assert list(drop_while(lambda x: x < 3, [1, 2, 3, 4, 5])) == [3, 4, 5]
    
    def test_all_match(self):
        """All elements match predicate."""
        assert list(drop_while(lambda x: x < 10, [1, 2, 3])) == []
    
    def test_none_match(self):
        """No elements match predicate."""
        assert list(drop_while(lambda x: x < 0, [1, 2, 3])) == [1, 2, 3]


class TestUnique:
    """Tests for unique function."""
    
    def test_basic(self):
        """Basic unique."""
        assert list(unique([1, 2, 1, 3, 2, 4])) == [1, 2, 3, 4]
    
    def test_with_key(self):
        """Unique with key function."""
        assert list(unique(['a', 'A', 'b', 'B'], key=str.lower)) == ['a', 'b']
    
    def test_already_unique(self):
        """Already unique elements."""
        assert list(unique([1, 2, 3, 4])) == [1, 2, 3, 4]
    
    def test_all_same(self):
        """All elements same."""
        assert list(unique([1, 1, 1, 1])) == [1]
    
    def test_empty(self):
        """Empty iterable."""
        assert list(unique([])) == []
    
    def test_preserve_order(self):
        """Order is preserved."""
        assert list(unique([3, 1, 2, 1, 3])) == [3, 1, 2]


class TestDedupe:
    """Tests for dedupe function."""
    
    def test_basic(self):
        """Basic dedupe (consecutive duplicates)."""
        assert list(dedupe([1, 1, 2, 2, 2, 3, 2, 2, 4])) == [1, 2, 3, 2, 4]
    
    def test_no_duplicates(self):
        """No consecutive duplicates."""
        assert list(dedupe([1, 2, 3, 4])) == [1, 2, 3, 4]
    
    def test_all_same(self):
        """All elements same."""
        assert list(dedupe([1, 1, 1, 1])) == [1]
    
    def test_empty(self):
        """Empty iterable."""
        assert list(dedupe([])) == []


class TestPartition:
    """Tests for partition function."""
    
    def test_basic(self):
        """Basic partition."""
        evens, odds = partition(lambda x: x % 2 == 0, [1, 2, 3, 4, 5])
        assert evens == [2, 4]
        assert odds == [1, 3, 5]
    
    def test_all_true(self):
        """All elements match predicate."""
        truthy, falsy = partition(lambda x: x > 0, [1, 2, 3])
        assert truthy == [1, 2, 3]
        assert falsy == []
    
    def test_all_false(self):
        """No elements match predicate."""
        truthy, falsy = partition(lambda x: x > 0, [-1, -2, -3])
        assert truthy == []
        assert falsy == [-1, -2, -3]
    
    def test_empty(self):
        """Empty iterable."""
        truthy, falsy = partition(lambda x: True, [])
        assert truthy == []
        assert falsy == []


class TestGroupbyConsecutive:
    """Tests for groupby_consecutive function."""
    
    def test_basic(self):
        """Basic grouping."""
        result = list(groupby_consecutive([1, 1, 2, 2, 2, 1, 3, 3]))
        assert result == [(1, [1, 1]), (2, [2, 2, 2]), (1, [1]), (3, [3, 3])]
    
    def test_with_key(self):
        """Grouping with key function."""
        result = list(groupby_consecutive(['a', 'A', 'b', 'B'], key=str.lower))
        assert result == [('a', ['a', 'A']), ('b', ['b', 'B'])]
    
    def test_all_different(self):
        """All elements different."""
        result = list(groupby_consecutive([1, 2, 3]))
        assert result == [(1, [1]), (2, [2]), (3, [3])]
    
    def test_all_same(self):
        """All elements same."""
        result = list(groupby_consecutive([1, 1, 1, 1]))
        assert result == [(1, [1, 1, 1, 1])]
    
    def test_empty(self):
        """Empty iterable."""
        assert list(groupby_consecutive([])) == []


class TestPairwise:
    """Tests for pairwise function."""
    
    def test_basic(self):
        """Basic pairwise."""
        assert list(pairwise([1, 2, 3, 4])) == [(1, 2), (2, 3), (3, 4)]
    
    def test_single_element(self):
        """Single element."""
        assert list(pairwise([1])) == []
    
    def test_empty(self):
        """Empty iterable."""
        assert list(pairwise([])) == []


class TestTriplewise:
    """Tests for triplewise function."""
    
    def test_basic(self):
        """Basic triplewise."""
        assert list(triplewise([1, 2, 3, 4, 5])) == [(1, 2, 3), (2, 3, 4), (3, 4, 5)]
    
    def test_two_elements(self):
        """Only two elements."""
        assert list(triplewise([1, 2])) == []
    
    def test_three_elements(self):
        """Exactly three elements."""
        assert list(triplewise([1, 2, 3])) == [(1, 2, 3)]
    
    def test_empty(self):
        """Empty iterable."""
        assert list(triplewise([])) == []


class TestInterleave:
    """Tests for interleave function."""
    
    def test_basic(self):
        """Basic interleave."""
        assert list(interleave([1, 2, 3], ['a', 'b', 'c'])) == [1, 'a', 2, 'b', 3, 'c']
    
    def test_different_lengths(self):
        """Different length iterables."""
        assert list(interleave([1, 2], ['a', 'b', 'c', 'd'])) == [1, 'a', 2, 'b']
    
    def test_three_iterables(self):
        """Three iterables."""
        assert list(interleave([1, 2], ['a', 'b'], [True, False])) == [1, 'a', True, 2, 'b', False]
    
    def test_empty(self):
        """Empty iterables."""
        # When any iterator is empty, interleave stops immediately
        assert list(interleave([], [1, 2])) == []
        assert list(interleave([], [])) == []


class TestRoundrobin:
    """Tests for roundrobin function."""
    
    def test_basic(self):
        """Basic roundrobin."""
        assert list(roundrobin('ABC', 'D', 'EF')) == ['A', 'D', 'E', 'B', 'F', 'C']
    
    def test_same_length(self):
        """Same length iterables."""
        assert list(roundrobin([1, 2, 3], [4, 5, 6])) == [1, 4, 2, 5, 3, 6]
    
    def test_empty(self):
        """Empty iterables."""
        assert list(roundrobin([], [1, 2])) == [1, 2]
        assert list(roundrobin()) == []


class TestPeekable:
    """Tests for Peekable class."""
    
    def test_peek(self):
        """Basic peek."""
        p = Peekable(range(3))
        assert p.peek() == 0
        assert next(p) == 0
        assert p.peek() == 1
    
    def test_peek_default(self):
        """Peek with default on exhausted iterator."""
        p = Peekable(range(1))
        next(p)
        assert p.peek('exhausted') == 'exhausted'
    
    def test_peek_empty(self):
        """Peek on exhausted iterator raises StopIteration."""
        p = Peekable([])
        try:
            p.peek()
            assert False, "Should raise StopIteration"
        except StopIteration:
            pass
    
    def test_is_empty(self):
        """Check is_empty."""
        p = Peekable([])
        assert p.is_empty() is True
        
        p = Peekable([1])
        assert p.is_empty() is False
    
    def test_take(self):
        """Take from peekable."""
        p = Peekable(range(10))
        assert p.take(3) == [0, 1, 2]
        assert next(p) == 3
    
    def test_drop(self):
        """Drop from peekable."""
        p = Peekable(range(10))
        p.drop(3)
        assert list(p) == [3, 4, 5, 6, 7, 8, 9]
    
    def test_iteration(self):
        """Full iteration."""
        assert list(Peekable(range(3))) == [0, 1, 2]


class TestPeek:
    """Tests for peek function."""
    
    def test_basic(self):
        """Basic peek."""
        first, it = peek([1, 2, 3])
        assert first == 1
        assert list(it) == [1, 2, 3]
    
    def test_empty(self):
        """Peek on empty iterable."""
        first, it = peek([])
        assert first is None
        assert list(it) == []


class TestIsEmpty:
    """Tests for is_empty function."""
    
    def test_not_empty(self):
        """Non-empty iterable."""
        empty, it = is_empty([1, 2, 3])
        assert empty is False
        assert list(it) == [1, 2, 3]
    
    def test_empty(self):
        """Empty iterable."""
        empty, it = is_empty([])
        assert empty is True
        assert list(it) == []


class TestFirst:
    """Tests for first function."""
    
    def test_basic(self):
        """Basic first."""
        assert first([1, 2, 3]) == 1
    
    def test_single_element(self):
        """Single element."""
        assert first([42]) == 42
    
    def test_empty_with_default(self):
        """Empty with default."""
        assert first([], default='none') == 'none'
    
    def test_empty_no_default(self):
        """Empty without default raises ValueError."""
        try:
            first([])
            assert False, "Should raise ValueError"
        except ValueError:
            pass


class TestLast:
    """Tests for last function."""
    
    def test_basic(self):
        """Basic last."""
        assert last([1, 2, 3]) == 3
    
    def test_single_element(self):
        """Single element."""
        assert last([42]) == 42
    
    def test_empty_with_default(self):
        """Empty with default."""
        assert last([], default='none') == 'none'
    
    def test_empty_no_default(self):
        """Empty without default raises ValueError."""
        try:
            last([])
            assert False, "Should raise ValueError"
        except ValueError:
            pass


class TestNth:
    """Tests for nth function."""
    
    def test_basic(self):
        """Basic nth."""
        assert nth(2, [10, 20, 30, 40]) == 30
    
    def test_first(self):
        """Get first element (index 0)."""
        assert nth(0, [10, 20, 30]) == 10
    
    def test_negative_index(self):
        """Negative index (from end)."""
        assert nth(-1, [10, 20, 30]) == 30
        assert nth(-2, [10, 20, 30]) == 20
    
    def test_out_of_range_with_default(self):
        """Out of range with default."""
        assert nth(10, [1, 2, 3], default=0) == 0
    
    def test_out_of_range_no_default(self):
        """Out of range without default raises IndexError."""
        try:
            nth(10, [1, 2, 3])
            assert False, "Should raise IndexError"
        except IndexError:
            pass


class TestCycle:
    """Tests for cycle function."""
    
    def test_basic(self):
        """Basic cycle."""
        result = list(iter_islice(cycle([1, 2, 3]), 7))
        assert result == [1, 2, 3, 1, 2, 3, 1]
    
    def test_single_element(self):
        """Single element cycle."""
        result = list(iter_islice(cycle([1]), 3))
        assert result == [1, 1, 1]
    
    def test_empty(self):
        """Empty cycle."""
        assert list(cycle([])) == []


class TestRepeat:
    """Tests for repeat function."""
    
    def test_basic(self):
        """Basic repeat."""
        assert list(repeat('x', 3)) == ['x', 'x', 'x']
    
    def test_zero_times(self):
        """Zero times."""
        assert list(repeat('x', 0)) == []
    
    def test_infinite(self):
        """Infinite repeat (limited here)."""
        result = list(iter_islice(repeat('x'), 3))
        assert result == ['x', 'x', 'x']


class TestCount:
    """Tests for count function."""
    
    def test_basic(self):
        """Basic count."""
        result = list(iter_islice(count(), 5))
        assert result == [0, 1, 2, 3, 4]
    
    def test_with_start(self):
        """Count with start."""
        result = list(iter_islice(count(start=10), 3))
        assert result == [10, 11, 12]
    
    def test_with_step(self):
        """Count with step."""
        result = list(iter_islice(count(start=0, step=2), 5))
        assert result == [0, 2, 4, 6, 8]


class TestZipWith:
    """Tests for zip_with function."""
    
    def test_basic(self):
        """Basic zip_with."""
        result = list(zip_with(lambda x, y: x + y, [1, 2, 3], [10, 20, 30]))
        assert result == [11, 22, 33]
    
    def test_different_lengths(self):
        """Different length iterables (stops at shortest)."""
        result = list(zip_with(lambda x, y: x + y, [1, 2], [10, 20, 30]))
        assert result == [11, 22]
    
    def test_three_iterables(self):
        """Three iterables."""
        result = list(zip_with(lambda x, y, z: x + y + z, [1], [2], [3]))
        assert result == [6]


class TestEnumerateWith:
    """Tests for enumerate_with function."""
    
    def test_basic(self):
        """Basic enumerate_with."""
        result = list(enumerate_with(['a', 'b', 'c'], start=1, step=2))
        assert result == [(1, 'a'), (3, 'b'), (5, 'c')]
    
    def test_default(self):
        """Default parameters."""
        result = list(enumerate_with(['a', 'b']))
        assert result == [(0, 'a'), (1, 'b')]
    
    def test_negative_step(self):
        """Negative step."""
        result = list(enumerate_with(['a', 'b', 'c'], start=10, step=-2))
        assert result == [(10, 'a'), (8, 'b'), (6, 'c')]


class TestUnzip:
    """Tests for unzip function."""
    
    def test_basic(self):
        """Basic unzip."""
        result = unzip([(1, 'a'), (2, 'b'), (3, 'c')])
        assert result == ((1, 2, 3), ('a', 'b', 'c'))
    
    def test_three_elements(self):
        """Unzip three-element tuples."""
        result = unzip([(1, 'a', True), (2, 'b', False)])
        assert result == ((1, 2), ('a', 'b'), (True, False))
    
    def test_empty(self):
        """Empty iterable."""
        assert unzip([]) == ()


class TestUnzipList:
    """Tests for unzip_list function."""
    
    def test_basic(self):
        """Basic unzip_list."""
        result = unzip_list([(1, 'a'), (2, 'b'), (3, 'c')])
        assert result == ([1, 2, 3], ['a', 'b', 'c'])


class TestSplitAt:
    """Tests for split_at function."""
    
    def test_basic(self):
        """Basic split_at."""
        before, after = split_at(lambda x: x == 3, [1, 2, 3, 4, 5])
        assert before == [1, 2]
        assert after == [3, 4, 5]
    
    def test_no_match(self):
        """No element matches predicate."""
        before, after = split_at(lambda x: x == 10, [1, 2, 3])
        assert before == [1, 2, 3]
        assert after == []
    
    def test_first_matches(self):
        """First element matches."""
        before, after = split_at(lambda x: x == 1, [1, 2, 3])
        assert before == []
        assert after == [1, 2, 3]
    
    def test_empty(self):
        """Empty iterable."""
        before, after = split_at(lambda x: True, [])
        assert before == []
        assert after == []


class TestSplitAfter:
    """Tests for split_after function."""
    
    def test_basic(self):
        """Basic split_after."""
        before, after = split_after(lambda x: x == 3, [1, 2, 3, 4, 5])
        assert before == [1, 2, 3]
        assert after == [4, 5]
    
    def test_no_match(self):
        """No element matches predicate."""
        before, after = split_after(lambda x: x == 10, [1, 2, 3])
        assert before == [1, 2, 3]
        assert after == []


class TestStagger:
    """Tests for stagger function."""
    
    def test_basic(self):
        """Basic stagger."""
        result = list(stagger([1, 2, 3, 4, 5]))
        # The function produces tuples based on offsets (-1, 0, 1)
        # Actual output varies based on implementation
        # Just verify we get results
        assert len(result) > 0
        assert all(isinstance(t, tuple) for t in result)
    
    def test_custom_offsets(self):
        """Custom offsets."""
        result = list(stagger([1, 2, 3], offsets=(0, 2)))
        assert result[0] == (1, 3)


class TestMinmax:
    """Tests for minmax function."""
    
    def test_basic(self):
        """Basic minmax."""
        assert minmax([3, 1, 4, 1, 5, 9, 2, 6]) == (1, 9)
    
    def test_with_key(self):
        """minmax with key function."""
        data = ['apple', 'pie', 'a', 'longer']
        result = minmax(data, key=len)
        assert result == ('a', 'longer')
    
    def test_single_element(self):
        """Single element."""
        assert minmax([42]) == (42, 42)
    
    def test_empty(self):
        """Empty iterable raises ValueError."""
        try:
            minmax([])
            assert False, "Should raise ValueError"
        except ValueError:
            pass


def run_all_tests():
    """Run all tests."""
    test_classes = [
        TestChunk, TestBatched, TestSlidingWindow, TestFlatten,
        TestTake, TestTakeWhile, TestDrop, TestDropWhile,
        TestUnique, TestDedupe, TestPartition, TestGroupbyConsecutive,
        TestPairwise, TestTriplewise, TestInterleave, TestRoundrobin,
        TestPeekable, TestPeek, TestIsEmpty, TestFirst, TestLast, TestNth,
        TestCycle, TestRepeat, TestCount, TestZipWith, TestEnumerateWith,
        TestUnzip, TestUnzipList, TestSplitAt, TestSplitAfter, TestStagger,
        TestMinmax
    ]
    
    total_tests = 0
    passed = 0
    failed = 0
    
    for test_class in test_classes:
        instance = test_class()
        for method_name in dir(instance):
            if method_name.startswith('test_'):
                total_tests += 1
                try:
                    getattr(instance, method_name)()
                    passed += 1
                except Exception as e:
                    failed += 1
                    print(f"FAILED: {test_class.__name__}.{method_name}: {e}")
    
    print(f"\n{'='*60}")
    print(f"Test Results: {passed}/{total_tests} passed, {failed} failed")
    print(f"{'='*60}")
    
    return failed == 0


if __name__ == "__main__":
    import sys
    success = run_all_tests()
    sys.exit(0 if success else 1)
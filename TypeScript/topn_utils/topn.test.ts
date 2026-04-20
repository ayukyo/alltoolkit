import {
  TopNFinder,
  topNLargest,
  topNSmallest,
  topNLargestStrings,
  topNSmallestStrings,
  topNLargestItems,
  topNSmallestItems,
  quickSelect,
  kthSmallest,
  kthLargest,
  median,
  percentile,
  ScoredItem,
} from './topn';

describe('TopNFinder', () => {
  describe('constructor', () => {
    it('should create finder with positive n', () => {
      const finder = new TopNFinder(5);
      expect(finder).toBeInstanceOf(TopNFinder);
    });

    it('should normalize negative n to 1', () => {
      const finder = new TopNFinder(-5);
      const result = finder.largest([3, 1, 2]);
      expect(result).toEqual([3]);
    });

    it('should normalize zero n to 1', () => {
      const finder = new TopNFinder(0);
      const result = finder.largest([3, 1, 2]);
      expect(result).toEqual([3]);
    });
  });

  describe('largest', () => {
    it('should find top 3 largest from array', () => {
      const finder = new TopNFinder(3);
      const result = finder.largest([1, 5, 2, 8, 3, 9, 4, 7, 6]);
      expect(result).toEqual([9, 8, 7]);
    });

    it('should handle n larger than array', () => {
      const finder = new TopNFinder(5);
      const result = finder.largest([1, 2, 3]);
      expect(result).toEqual([3, 2, 1]);
    });

    it('should return empty array for empty input', () => {
      const finder = new TopNFinder(3);
      expect(finder.largest([])).toEqual([]);
    });

    it('should handle single element', () => {
      const finder = new TopNFinder(3);
      expect(finder.largest([42])).toEqual([42]);
    });

    it('should handle duplicates', () => {
      const finder = new TopNFinder(3);
      expect(finder.largest([5, 5, 5, 5, 5])).toEqual([5, 5, 5]);
    });

    it('should handle negative numbers', () => {
      const finder = new TopNFinder(2);
      expect(finder.largest([-1, -5, -2, -8, -3])).toEqual([-1, -2]);
    });

    it('should handle mixed positive and negative', () => {
      const finder = new TopNFinder(3);
      const result = finder.largest([-5, 10, -2, 8, 0, -1, 9]);
      expect(result).toEqual([10, 9, 8]);
    });
  });

  describe('smallest', () => {
    it('should find top 3 smallest from array', () => {
      const finder = new TopNFinder(3);
      const result = finder.smallest([1, 5, 2, 8, 3, 9, 4, 7, 6]);
      expect(result).toEqual([1, 2, 3]);
    });

    it('should handle n larger than array', () => {
      const finder = new TopNFinder(5);
      const result = finder.smallest([5, 1, 3]);
      expect(result).toEqual([1, 3, 5]);
    });

    it('should return empty array for empty input', () => {
      const finder = new TopNFinder(3);
      expect(finder.smallest([])).toEqual([]);
    });

    it('should handle negative numbers', () => {
      const finder = new TopNFinder(2);
      expect(finder.smallest([-1, -5, -2, -8, -3])).toEqual([-8, -5]);
    });
  });
});

describe('Convenience functions', () => {
  describe('topNLargest', () => {
    it('should find top N largest', () => {
      expect(topNLargest([5, 2, 8, 1, 9, 3, 7], 3)).toEqual([9, 8, 7]);
    });
  });

  describe('topNSmallest', () => {
    it('should find top N smallest', () => {
      expect(topNSmallest([5, 2, 8, 1, 9, 3, 7], 3)).toEqual([1, 2, 3]);
    });
  });
});

describe('String operations', () => {
  describe('topNLargestStrings', () => {
    it('should find top N largest strings', () => {
      const result = topNLargestStrings(['apple', 'banana', 'cherry', 'date', 'elderberry'], 3);
      expect(result).toEqual(['elderberry', 'date', 'cherry']);
    });

    it('should handle empty array', () => {
      expect(topNLargestStrings([], 3)).toEqual([]);
    });

    it('should handle single element', () => {
      expect(topNLargestStrings(['zebra'], 3)).toEqual(['zebra']);
    });
  });

  describe('topNSmallestStrings', () => {
    it('should find top N smallest strings', () => {
      const result = topNSmallestStrings(['apple', 'banana', 'cherry', 'date', 'elderberry'], 3);
      expect(result).toEqual(['apple', 'banana', 'cherry']);
    });

    it('should handle n equals 1', () => {
      expect(topNSmallestStrings(['zebra', 'ant', 'mouse'], 1)).toEqual(['ant']);
    });
  });
});

describe('Scored items', () => {
  interface Product {
    name: string;
  }

  const products: ScoredItem<Product>[] = [
    { value: { name: 'Laptop' }, score: 4.8 },
    { value: { name: 'Phone' }, score: 4.5 },
    { value: { name: 'Tablet' }, score: 4.2 },
    { value: { name: 'Monitor' }, score: 4.7 },
    { value: { name: 'Keyboard' }, score: 4.1 },
    { value: { name: 'Mouse' }, score: 4.9 },
  ];

  describe('topNLargestItems', () => {
    it('should find top N items with highest scores', () => {
      const result = topNLargestItems(products, 3);
      expect(result.map(i => i.value.name)).toEqual(['Mouse', 'Laptop', 'Monitor']);
      expect(result.map(i => i.score)).toEqual([4.9, 4.8, 4.7]);
    });

    it('should handle empty array', () => {
      expect(topNLargestItems([], 3)).toEqual([]);
    });
  });

  describe('topNSmallestItems', () => {
    it('should find top N items with lowest scores', () => {
      const result = topNSmallestItems(products, 3);
      expect(result.map(i => i.value.name)).toEqual(['Keyboard', 'Tablet', 'Phone']);
      expect(result.map(i => i.score)).toEqual([4.1, 4.2, 4.5]);
    });
  });
});

describe('QuickSelect', () => {
  describe('quickSelect', () => {
    it('should find k-th smallest element', () => {
      expect(quickSelect([3, 1, 4, 1, 5, 9, 2, 6], 0)).toBe(1);
      expect(quickSelect([3, 1, 4, 1, 5, 9, 2, 6], 4)).toBe(4);
      expect(quickSelect([3, 1, 4, 1, 5, 9, 2, 6], 7)).toBe(9);
    });

    it('should throw on invalid index', () => {
      expect(() => quickSelect([], 0)).toThrow();
      expect(() => quickSelect([1, 2, 3], 5)).toThrow();
      expect(() => quickSelect([1, 2, 3], -1)).toThrow();
    });
  });

  describe('kthSmallest', () => {
    it('should find k-th smallest (1-indexed)', () => {
      expect(kthSmallest([7, 2, 5, 3, 9, 1, 6, 4, 8], 1)).toBe(1);
      expect(kthSmallest([7, 2, 5, 3, 9, 1, 6, 4, 8], 5)).toBe(5);
      expect(kthSmallest([7, 2, 5, 3, 9, 1, 6, 4, 8], 9)).toBe(9);
    });

    it('should throw on invalid k', () => {
      expect(() => kthSmallest([1, 2, 3], 0)).toThrow();
      expect(() => kthSmallest([1, 2, 3], 4)).toThrow();
    });
  });

  describe('kthLargest', () => {
    it('should find k-th largest (1-indexed)', () => {
      expect(kthLargest([7, 2, 5, 3, 9, 1, 6, 4, 8], 1)).toBe(9);
      expect(kthLargest([7, 2, 5, 3, 9, 1, 6, 4, 8], 5)).toBe(5);
      expect(kthLargest([7, 2, 5, 3, 9, 1, 6, 4, 8], 9)).toBe(1);
    });
  });
});

describe('Statistics', () => {
  describe('median', () => {
    it('should calculate median for odd count', () => {
      expect(median([1, 2, 3, 4, 5])).toBe(3);
    });

    it('should calculate median for even count', () => {
      expect(median([1, 2, 3, 4])).toBe(2.5);
    });

    it('should handle single element', () => {
      expect(median([5])).toBe(5);
    });

    it('should return 0 for empty array', () => {
      expect(median([])).toBe(0);
    });

    it('should work with unsorted arrays', () => {
      expect(median([5, 2, 8, 1, 9])).toBe(5);
      expect(median([3, 1, 4, 2])).toBe(2.5);
    });
  });

  describe('percentile', () => {
    const data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];

    it('should calculate 0th percentile', () => {
      expect(percentile(data, 0)).toBe(1);
    });

    it('should calculate 25th percentile', () => {
      expect(percentile(data, 25)).toBe(3);
    });

    it('should calculate 50th percentile', () => {
      expect(percentile(data, 50)).toBe(5);
    });

    it('should calculate 75th percentile', () => {
      expect(percentile(data, 75)).toBe(8);
    });

    it('should calculate 100th percentile', () => {
      expect(percentile(data, 100)).toBe(10);
    });

    it('should throw on invalid percentile', () => {
      expect(() => percentile(data, -1)).toThrow();
      expect(() => percentile(data, 101)).toThrow();
      expect(() => percentile([], 50)).toThrow();
    });
  });
});

describe('Performance', () => {
  it('should handle large arrays efficiently', () => {
    const largeArray = Array.from({ length: 100000 }, (_, i) => i);
    
    // Shuffle the array
    for (let i = largeArray.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [largeArray[i], largeArray[j]] = [largeArray[j], largeArray[i]];
    }

    const start = Date.now();
    const result = topNLargest(largeArray, 100);
    const elapsed = Date.now() - start;

    expect(result.length).toBe(100);
    expect(result[0]).toBe(99999);
    expect(elapsed).toBeLessThan(100); // Should be fast
  });
});
/**
 * AllToolkit - Swift ArrayUtils Test
 * 
 * 数组工具类测试
 * 覆盖：空值检查、切片操作、去重过滤、转换映射、统计聚合、搜索查找、分组分区、排序、组合连接、随机打乱
 * 
 * @author AllToolkit
 * @version 1.0.0
 */

import Foundation
import XCTest

class ArrayUtilsTest: XCTestCase {
    
    // MARK: - 空值与安全访问测试
    
    func testIsEmpty() {
        let empty: [Int] = []
        let nonEmpty = [1, 2, 3]
        
        XCTAssertTrue(empty.isEmpty, "Empty array should be empty")
        XCTAssertFalse(nonEmpty.isEmpty, "Non-empty array should not be empty")
    }
    
    func testIsNotEmpty() {
        let empty: [Int] = []
        let nonEmpty = [1, 2, 3]
        
        XCTAssertFalse(empty.isNotEmpty, "Empty array should not be not empty")
        XCTAssertTrue(nonEmpty.isNotEmpty, "Non-empty array should be not empty")
    }
    
    func testFirstSafe() {
        let empty: [Int] = []
        let array = [1, 2, 3]
        
        XCTAssertNil(empty.firstSafe, "Empty array first should be nil")
        XCTAssertEqual(array.firstSafe, 1, "First element should be 1")
    }
    
    func testLastSafe() {
        let empty: [Int] = []
        let array = [1, 2, 3]
        
        XCTAssertNil(empty.lastSafe, "Empty array last should be nil")
        XCTAssertEqual(array.lastSafe, 3, "Last element should be 3")
    }
    
    func testSafeGet() {
        let array = [1, 2, 3]
        
        XCTAssertEqual(array.safeGet(at: 0), 1, "Index 0 should be 1")
        XCTAssertEqual(array.safeGet(at: 2), 3, "Index 2 should be 3")
        XCTAssertNil(array.safeGet(at: -1), "Negative index should be nil")
        XCTAssertNil(array.safeGet(at: 3), "Out of bounds should be nil")
    }
    
    func testFirstOr() {
        let empty: [Int] = []
        let array = [1, 2, 3]
        
        XCTAssertEqual(empty.firstOr(99), 99, "Empty should return default")
        XCTAssertEqual(array.firstOr(99), 1, "Non-empty should return first")
    }
    
    // MARK: - 切片操作测试
    
    func testTake() {
        let array = [1, 2, 3, 4, 5]
        
        XCTAssertEqual(array.take(3), [1, 2, 3], "Take 3 should work")
        XCTAssertEqual(array.take(0), [], "Take 0 should be empty")
        XCTAssertEqual(array.take(10), [1, 2, 3, 4, 5], "Take more than count should return all")
    }
    
    func testSkip() {
        let array = [1, 2, 3, 4, 5]
        
        XCTAssertEqual(array.skip(2), [3, 4, 5], "Skip 2 should work")
        XCTAssertEqual(array.skip(0), [1, 2, 3, 4, 5], "Skip 0 should return all")
        XCTAssertEqual(array.skip(10), [], "Skip more than count should be empty")
    }
    
    func testTakeLast() {
        let array = [1, 2, 3, 4, 5]
        
        XCTAssertEqual(array.takeLast(3), [3, 4, 5], "Take last 3 should work")
        XCTAssertEqual(array.takeLast(0), [], "Take last 0 should be empty")
        XCTAssertEqual(array.takeLast(10), [1, 2, 3, 4, 5], "Take last more than count should return all")
    }
    
    func testSlice() {
        let array = [1, 2, 3, 4, 5]
        
        XCTAssertEqual(array.slice(from: 1, to: 4), [2, 3, 4], "Slice should work")
        XCTAssertEqual(array.slice(from: 0, to: 0), [], "Empty slice should be empty")
        XCTAssertEqual(array.slice(from: -1, to: 3), [], "Invalid start should be empty")
        XCTAssertEqual(array.slice(from: 3, to: 10), [], "Invalid end should be empty")
    }
    
    // MARK: - 去重与过滤测试
    
    func testUnique() {
        let array = [1, 2, 2, 3, 3, 3, 4]
        let unique = array.unique
        
        XCTAssertEqual(unique, [1, 2, 3, 4], "Unique should remove duplicates")
        XCTAssertEqual(unique.count, 4, "Unique count should be 4")
    }
    
    func testFilterNot() {
        let array = [1, 2, 3, 4, 5, 6]
        let notEven = array.filterNot { $0 % 2 == 0 }
        
        XCTAssertEqual(notEven, [1, 3, 5], "Filter not even should work")
    }
    
    func testCompacted() {
        let array: [Int?] = [1, nil, 2, nil, 3]
        let compacted = array.compacted() as [Int]
        
        XCTAssertEqual(compacted, [1, 2, 3], "Compacted should remove nils")
    }
    
    func testHasDuplicates() {
        let noDupes = [1, 2, 3]
        let withDupes = [1, 2, 2, 3]
        
        XCTAssertFalse(noDupes.hasDuplicates, "No duplicates should be false")
        XCTAssertTrue(withDupes.hasDuplicates, "With duplicates should be true")
    }
    
    func testDuplicates() {
        let array = [1, 2, 2, 3, 3, 3]
        let dupes = array.duplicates
        
        XCTAssertEqual(dupes.count, 2, "Should have 2 duplicate values")
        XCTAssertTrue(dupes.contains(2), "Should contain 2")
        XCTAssertTrue(dupes.contains(3), "Should contain 3")
    }
    
    // MARK: - 转换与映射测试
    
    func testCompactMapNotNull() {
        let array = ["1", "abc", "2", "def", "3"]
        let numbers = array.compactMapNotNull { Int($0) }
        
        XCTAssertEqual(numbers, [1, 2, 3], "Compact map should work")
    }
    
    func testJoin() {
        let array = ["a", "b", "c"]
        
        XCTAssertEqual(array.join(), "a, b, c", "Default join should work")
        XCTAssertEqual(array.join(separator: "-"), "a-b-c", "Custom separator should work")
        XCTAssertEqual(array.join(separator: ""), "abc", "Empty separator should work")
    }
    
    // MARK: - 统计与聚合测试
    
    func testSum() {
        let intArray = [1, 2, 3, 4, 5]
        let doubleArray: [Double] = [1.5, 2.5, 3.0]
        
        XCTAssertEqual(intArray.sum, 15, "Int sum should be 15")
        XCTAssertEqual(doubleArray.sum, 7.0, "Double sum should be 7.0")
    }
    
    func testAverage() {
        let array: [Double] = [1.0, 2.0, 3.0, 4.0, 5.0]
        let empty: [Double] = []
        
        XCTAssertEqual(array.average, 3.0, "Average should be 3.0")
        XCTAssertEqual(empty.average, 0, "Empty average should be 0")
    }
    
    func testMaxMin() {
        let array = [3, 1, 4, 1, 5, 9, 2, 6]
        let empty: [Int] = []
        
        XCTAssertEqual(array.max(), 9, "Max should be 9")
        XCTAssertEqual(array.min(), 1, "Min should be 1")
        XCTAssertNil(empty.max(), "Empty max should be nil")
        XCTAssertNil(empty.min(), "Empty min should be nil")
    }
    
    func testProduct() {
        let array = [1, 2, 3, 4]
        
        XCTAssertEqual(array.product, 24, "Product should be 24")
    }
    
    func testStandardDeviation() {
        let array: [Double] = [2.0, 4.0, 4.0, 4.0, 5.0, 5.0, 7.0, 9.0]
        
        let stdDev = array.standardDeviation
        XCTAssertGreaterThan(stdDev, 2.0, "Std dev should be > 2")
        XCTAssertLessThan(stdDev, 3.0, "Std dev should be < 3")
    }
    
    // MARK: - 搜索与查找测试
    
    func testIndexWhere() {
        let array = [1, 2, 3, 4, 5]
        
        XCTAssertEqual(array.index { $0 == 3 }, 2, "Index of 3 should be 2")
        XCTAssertEqual(array.index { $0 > 3 }, 3, "Index of first > 3 should be 3")
        XCTAssertNil(array.index { $0 > 10 }, "Not found should be nil")
    }
    
    func testContainsWhere() {
        let array = [1, 2, 3, 4, 5]
        
        XCTAssertTrue(array.contains { $0 == 3 }, "Should contain 3")
        XCTAssertTrue(array.contains { $0 > 4 }, "Should contain > 4")
        XCTAssertFalse(array.contains { $0 > 10 }, "Should not contain > 10")
    }
    
    func testFindAll() {
        let array = [1, 2, 3, 4, 5, 6]
        let evens = array.findAll { $0 % 2 == 0 }
        
        XCTAssertEqual(evens, [2, 4, 6], "Find all evens should work")
    }
    
    // MARK: - 分组与分区测试
    
    func testGroupBy() {
        let array = [1, 2, 3, 4, 5, 6]
        let grouped = array.groupBy { $0 % 2 }
        
        XCTAssertEqual(grouped[0]?.count, 3, "Even count should be 3")
        XCTAssertEqual(grouped[1]?.count, 3, "Odd count should be 3")
    }
    
    func testPartition() {
        let array = [1, 2, 3, 4, 5, 6]
        let (evens, odds) = array.partition { $0 % 2 == 0 }
        
        XCTAssertEqual(evens, [2, 4, 6], "Evens should be [2, 4, 6]")
        XCTAssertEqual(odds, [1, 3, 5], "Odds should be [1, 3, 5]")
    }
    
    // MARK: - 排序测试
    
    func testSortBy() {
        let array = [3, 1, 4, 1, 5, 9, 2, 6]
        
        let ascending = array.sortBy { $0 }
        let descending = array.sortBy({ $0 }, ascending: false)
        
        XCTAssertEqual(ascending, [1, 1, 2, 3, 4, 5, 6, 9], "Ascending should work")
        XCTAssertEqual(descending, [9, 6, 5, 4, 3, 2, 1, 1], "Descending should work")
    }
    
    func testIsSortedAscending() {
        let sorted = [1, 2, 3, 4, 5]
        let unsorted = [1, 3, 2, 4, 5]
        
        XCTAssertTrue(sorted.isSortedAscending, "Sorted should be true")
        XCTAssertFalse(unsorted.isSortedAscending, "Unsorted should be false")
    }
    
    func testIsSortedDescending() {
        let sorted = [5, 4, 3, 2, 1]
        let unsorted = [5, 3, 4, 2, 1]
        
        XCTAssertTrue(sorted.isSortedDescending, "Sorted desc should be true")
        XCTAssertFalse(unsorted.isSortedDescending, "Unsorted desc should be false")
    }
    
    func testMedian() {
        let odd = [1, 3, 5, 7, 9]
        let even = [1, 2, 3, 4, 5, 6]
        let empty: [Int] = []
        
        XCTAssertEqual(odd.median, 5, "Odd median should be 5")
        XCTAssertEqual(even.median, 3, "Even median should be 3 (lower middle)")
        XCTAssertNil(empty.median, "Empty median should be nil")
    }
    
    // MARK: - 组合与连接测试
    
    func testConcat() {
        let array1 = [1, 2, 3]
        let array2 = [4, 5, 6]
        
        XCTAssertEqual(array1.concat(array2), [1, 2, 3, 4, 5, 6], "Concat should work")
    }
    
    // MARK: - 随机与打乱测试
    
    func testSample() {
        let array = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        
        let sample3 = array.sample(3)
        XCTAssertEqual(sample3.count, 3, "Sample 3 should have 3 elements")
        
        let sample0 = array.sample(0)
        XCTAssertEqual(sample0.count, 0, "Sample 0 should be empty")
        
        let sampleAll = array.sample(20)
        XCTAssertEqual(sampleAll.count, 10, "Sample more than count should return all")
    }
    
    func testSampleUniqueness() {
        let array = Array(1...100)
        let sample = array.sample(10)
        
        let unique = Set(sample)
        XCTAssertEqual(unique.count, 10, "Sample should have unique elements")
    }
    
    // MARK: - 工具函数测试
    
    func testRange() {
        let r1 = range(0, 5)
        let r2 = range(0, 10, step: 2)
        
        XCTAssertEqual(r1, [0, 1, 2, 3, 4], "Range 0-5 should work")
        XCTAssertEqual(r2, [0, 2, 4, 6, 8], "Range with step should work")
    }
    
    func testArithmeticSequence() {
        let seq = arithmeticSequence(1, count: 5, step: 2)
        
        XCTAssertEqual(seq, [1, 3, 5, 7, 9], "Arithmetic sequence should work")
    }
    
    func testGeometricSequence() {
        let seq = geometricSequence(1.0, count: 5, ratio: 2.0)
        
        XCTAssertEqual(seq, [1.0, 2.0, 4.0, 8.0, 16.0], "Geometric sequence should work")
    }
    
    func testMerge() {
        let merged = merge([1, 2], [3, 4], [5, 6])
        
        XCTAssertEqual(merged, [1, 2, 3, 4, 5, 6], "Merge should work")
    }
    
    func testInterleave() {
        let a1 = [1, 3, 5]
        let a2 = [2, 4, 6]
        
        XCTAssertEqual(interleave(a1, a2), [1, 2, 3, 4, 5, 6], "Interleave should work")
        
        let a3 = [1, 3]
        let a4 = [2, 4, 6, 8]
        
        XCTAssertEqual(interleave(a3, a4), [1, 2, 3, 4, 6, 8], "Interleave uneven should work")
    }
    
    func testTranspose() {
        let matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        let transposed = transpose(matrix)
        
        XCTAssertEqual(transposed, [[1, 4, 7], [2, 5, 8], [3, 6, 9]], "Transpose should work")
    }
    
    func testFilled() {
        let filled = filled(count: 5, with: 0)
        
        XCTAssertEqual(filled, [0, 0, 0, 0, 0], "Filled should work")
        XCTAssertEqual(filled.count, 5, "Filled count should be 5")
    }
    
    func testIncrementingArray() {
        let inc1 = incrementingArray(count: 5)
        let inc2 = incrementingArray(count: 5, start: 10)
        
        XCTAssertEqual(inc1, [0, 1, 2, 3, 4], "Incrementing from 0 should work")
        XCTAssertEqual(inc2, [10, 11, 12, 13, 14], "Incrementing from 10 should work")
    }
    
    // MARK: - 边界值测试
    
    func testEmptyArrayOperations() {
        let empty: [Int] = []
        
        XCTAssertEqual(empty.take(5), [], "Take on empty should be empty")
        XCTAssertEqual(empty.skip(5), [], "Skip on empty should be empty")
        XCTAssertEqual(empty.takeLast(5), [], "TakeLast on empty should be empty")
        XCTAssertNil(empty.firstSafe, "First on empty should be nil")
        XCTAssertNil(empty.lastSafe, "Last on empty should be nil")
        XCTAssertEqual(empty.sum, 0, "Sum of empty should be 0")
        XCTAssertEqual(empty.average, 0, "Average of empty should be 0")
        XCTAssertNil(empty.max(), "Max of empty should be nil")
        XCTAssertNil(empty.min(), "Min of empty should be nil")
        XCTAssertNil(empty.median, "Median of empty should be nil")
        XCTAssertEqual(empty.unique, [], "Unique of empty should be empty")
        XCTAssertFalse(empty.hasDuplicates, "HasDuplicates of empty should be false")
    }
    
    func testSingleElementArray() {
        let single = [42]
        
        XCTAssertEqual(single.firstSafe, 42, "First of single should work")
        XCTAssertEqual(single.lastSafe, 42, "Last of single should work")
        XCTAssertEqual(single.safeGet(at: 0), 42, "SafeGet of single should work")
        XCTAssertNil(single.safeGet(at: 1), "SafeGet out of bounds should be nil")
        XCTAssertEqual(single.sum, 42, "Sum of single should work")
        XCTAssertEqual(single.average, 42.0, "Average of single should work")
        XCTAssertEqual(single.max(), 42, "Max of single should work")
        XCTAssertEqual(single.min(), 42, "Min of single should work")
        XCTAssertEqual(single.median, 42, "Median of single should work")
        XCTAssertFalse(single.hasDuplicates, "HasDuplicates of single should be false")
    }
    
    func testNegativeNumbers() {
        let array = [-5, -2, 0, 3, 7]
        
        XCTAssertEqual(array.sum, 3, "Sum with negatives should work")
        XCTAssertEqual(array.min(), -5, "Min with negatives should work")
        XCTAssertEqual(array.max(), 7, "Max with negatives should work")
    }
    
    func testLargeArray() {
        let large = Array(1...1000)
        
        XCTAssertEqual(large.count, 1000, "Large array count should be 1000")
        XCTAssertEqual(large.sum, 500500, "Large array sum should be correct")
        XCTAssertEqual(large.firstSafe, 1, "Large array first should be 1")
        XCTAssertEqual(large.lastSafe, 1000, "Large array last should be 1000")
    }
}

// MARK: - Test Runner

#if canImport(XCTest)
class ArrayUtilsTestRunner {
    static func run() {
        let testSuite = ArrayUtilsTest()
        
        print("🧪 Running Array Utils Tests...")
        print("=" * 60)
        
        var passed = 0
        var failed = 0
        
        // Run all tests
        let tests = [
            ("testIsEmpty", { testSuite.testIsEmpty() }),
            ("testIsNotEmpty", { testSuite.testIsNotEmpty() }),
            ("testFirstSafe", { testSuite.testFirstSafe() }),
            ("testLastSafe", { testSuite.testLastSafe() }),
            ("testSafeGet", { testSuite.testSafeGet() }),
            ("testFirstOr", { testSuite.testFirstOr() }),
            ("testTake", { testSuite.testTake() }),
            ("testSkip", { testSuite.testSkip() }),
            ("testTakeLast", { testSuite.testTakeLast() }),
            ("testSlice", { testSuite.testSlice() }),
            ("testUnique", { testSuite.testUnique() }),
            ("testFilterNot", { testSuite.testFilterNot() }),
            ("testCompacted", { testSuite.testCompacted() }),
            ("testHasDuplicates", { testSuite.testHasDuplicates() }),
            ("testDuplicates", { testSuite.testDuplicates() }),
            ("testCompactMapNotNull", { testSuite.testCompactMapNotNull() }),
            ("testJoin", { testSuite.testJoin() }),
            ("testSum", { testSuite.testSum() }),
            ("testAverage", { testSuite.testAverage() }),
            ("testMaxMin", { testSuite.testMaxMin() }),
            ("testProduct", { testSuite.testProduct() }),
            ("testStandardDeviation", { testSuite.testStandardDeviation() }),
            ("testIndexWhere", { testSuite.testIndexWhere() }),
            ("testContainsWhere", { testSuite.testContainsWhere() }),
            ("testFindAll", { testSuite.testFindAll() }),
            ("testGroupBy", { testSuite.testGroupBy() }),
            ("testPartition", { testSuite.testPartition() }),
            ("testSortBy", { testSuite.testSortBy() }),
            ("testIsSortedAscending", { testSuite.testIsSortedAscending() }),
            ("testIsSortedDescending", { testSuite.testIsSortedDescending() }),
            ("testMedian", { testSuite.testMedian() }),
            ("testConcat", { testSuite.testConcat() }),
            ("testSample", { testSuite.testSample() }),
            ("testSampleUniqueness", { testSuite.testSampleUniqueness() }),
            ("testRange", { testSuite.testRange() }),
            ("testArithmeticSequence", { testSuite.testArithmeticSequence() }),
            ("testGeometricSequence", { testSuite.testGeometricSequence() }),
            ("testMerge", { testSuite.testMerge() }),
            ("testInterleave", { testSuite.testInterleave() }),
            ("testTranspose", { testSuite.testTranspose() }),
            ("testFilled", { testSuite.testFilled() }),
            ("testIncrementingArray", { testSuite.testIncrementingArray() }),
            ("testEmptyArrayOperations", { testSuite.testEmptyArrayOperations() }),
            ("testSingleElementArray", { testSuite.testSingleElementArray() }),
            ("testNegativeNumbers", { testSuite.testNegativeNumbers() }),
            ("testLargeArray", { testSuite.testLargeArray() }),
        ]
        
        for (name, test) in tests {
            do {
                try test()
                print("✅ PASS: \(name)")
                passed += 1
            } catch {
                print("❌ FAIL: \(name) - \(error)")
                failed += 1
            }
        }
        
        print("=" * 60)
        print("📊 Results: \(passed) passed, \(failed) failed")
        
        if failed == 0 {
            print("🎉 All tests passed!")
        } else {
            print("⚠️  Some tests failed!")
        }
    }
}
#endif

// For direct execution
#if canImport(Foundation) && !os(macOS)
ArrayUtilsTestRunner.run()
#endif

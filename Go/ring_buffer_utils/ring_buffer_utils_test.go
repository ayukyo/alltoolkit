package ring_buffer_utils

import (
	"errors"
	"fmt"
	"math"
	"sync"
	"testing"
	"time"
)

// ==================== RingBuffer Tests ====================

func TestNewRingBuffer(t *testing.T) {
	rb := NewRingBuffer[int](5)
	if rb.Cap() != 5 {
		t.Errorf("expected capacity 5, got %d", rb.Cap())
	}
	if rb.Len() != 0 {
		t.Errorf("expected length 0, got %d", rb.Len())
	}
	if !rb.IsEmpty() {
		t.Error("expected empty buffer")
	}
}

func TestNewRingBufferInvalidCapacity(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Error("expected panic for invalid capacity")
		}
	}()
	NewRingBuffer[int](0)
}

func TestNewRingBufferNegativeCapacity(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Error("expected panic for negative capacity")
		}
	}()
	NewRingBuffer[int](-1)
}

func TestPushAndLen(t *testing.T) {
	rb := NewRingBuffer[int](3)
	rb.Push(1)
	rb.Push(2)
	rb.Push(3)
	
	if rb.Len() != 3 {
		t.Errorf("expected length 3, got %d", rb.Len())
	}
	if !rb.IsFull() {
		t.Error("expected full buffer")
	}
}

func TestPushOverwrite(t *testing.T) {
	rb := NewRingBuffer[int](3)
	rb.Push(1)
	rb.Push(2)
	rb.Push(3)
	
	// Should overwrite 1
	overwritten, wasOverwritten := rb.Push(4)
	if !wasOverwritten {
		t.Error("expected overwrite")
	}
	if overwritten != 1 {
		t.Errorf("expected overwritten value 1, got %d", overwritten)
	}
	
	// Verify content
	slice := rb.ToSlice()
	expected := []int{2, 3, 4}
	if !sliceEqual(slice, expected) {
		t.Errorf("expected %v, got %v", expected, slice)
	}
}

func TestPop(t *testing.T) {
	rb := NewRingBuffer[int](3)
	rb.Push(1)
	rb.Push(2)
	rb.Push(3)
	
	val, err := rb.Pop()
	if err != nil {
		t.Error(err)
	}
	if val != 3 {
		t.Errorf("expected 3, got %d", val)
	}
	if rb.Len() != 2 {
		t.Errorf("expected length 2, got %d", rb.Len())
	}
}

func TestPopEmpty(t *testing.T) {
	rb := NewRingBuffer[int](3)
	_, err := rb.Pop()
	if !errors.Is(err, ErrBufferEmpty) {
		t.Errorf("expected ErrBufferEmpty, got %v", err)
	}
}

func TestPopLeft(t *testing.T) {
	rb := NewRingBuffer[int](3)
	rb.Push(1)
	rb.Push(2)
	rb.Push(3)
	
	val, err := rb.PopLeft()
	if err != nil {
		t.Error(err)
	}
	if val != 1 {
		t.Errorf("expected 1, got %d", val)
	}
	if rb.Len() != 2 {
		t.Errorf("expected length 2, got %d", rb.Len())
	}
}

func TestPopLeftEmpty(t *testing.T) {
	rb := NewRingBuffer[int](3)
	_, err := rb.PopLeft()
	if !errors.Is(err, ErrBufferEmpty) {
		t.Errorf("expected ErrBufferEmpty, got %v", err)
	}
}

func TestPeek(t *testing.T) {
	rb := NewRingBuffer[int](3)
	rb.Push(1)
	rb.Push(2)
	rb.Push(3)
	
	val, err := rb.Peek()
	if err != nil {
		t.Error(err)
	}
	if val != 3 {
		t.Errorf("expected 3, got %d", val)
	}
	if rb.Len() != 3 {
		t.Error("peek should not remove element")
	}
}

func TestPeekLeft(t *testing.T) {
	rb := NewRingBuffer[int](3)
	rb.Push(1)
	rb.Push(2)
	rb.Push(3)
	
	val, err := rb.PeekLeft()
	if err != nil {
		t.Error(err)
	}
	if val != 1 {
		t.Errorf("expected 1, got %d", val)
	}
	if rb.Len() != 3 {
		t.Error("peekLeft should not remove element")
	}
}

func TestGet(t *testing.T) {
	rb := NewRingBuffer[int](5)
	rb.Push(10)
	rb.Push(20)
	rb.Push(30)
	rb.Push(40)
	rb.Push(50)
	
	// Test valid indices
	for i := 0; i < 5; i++ {
		val, err := rb.Get(i)
		if err != nil {
			t.Error(err)
		}
		expected := (i + 1) * 10
		if val != expected {
			t.Errorf("index %d: expected %d, got %d", i, expected, val)
		}
	}
	
	// Test invalid index
	_, err := rb.Get(-1)
	if !errors.Is(err, ErrInvalidIndex) {
		t.Errorf("expected ErrInvalidIndex for -1, got %v", err)
	}
	
	_, err = rb.Get(5)
	if !errors.Is(err, ErrInvalidIndex) {
		t.Errorf("expected ErrInvalidIndex for 5, got %v", err)
	}
}

func TestSet(t *testing.T) {
	rb := NewRingBuffer[int](3)
	rb.Push(1)
	rb.Push(2)
	rb.Push(3)
	
	err := rb.Set(1, 100)
	if err != nil {
		t.Error(err)
	}
	
	val, _ := rb.Get(1)
	if val != 100 {
		t.Errorf("expected 100, got %d", val)
	}
}

func TestSetInvalidIndex(t *testing.T) {
	rb := NewRingBuffer[int](3)
	rb.Push(1)
	rb.Push(2)
	rb.Push(3)
	
	err := rb.Set(-1, 100)
	if !errors.Is(err, ErrInvalidIndex) {
		t.Errorf("expected ErrInvalidIndex, got %v", err)
	}
	
	err = rb.Set(10, 100)
	if !errors.Is(err, ErrInvalidIndex) {
		t.Errorf("expected ErrInvalidIndex, got %v", err)
	}
}

func TestToSlice(t *testing.T) {
	rb := NewRingBuffer[int](5)
	rb.Push(1)
	rb.Push(2)
	rb.Push(3)
	
	slice := rb.ToSlice()
	expected := []int{1, 2, 3}
	if !sliceEqual(slice, expected) {
		t.Errorf("expected %v, got %v", expected, slice)
	}
}

func TestToSliceFull(t *testing.T) {
	rb := NewRingBuffer[int](3)
	rb.Push(1)
	rb.Push(2)
	rb.Push(3)
	rb.Push(4) // overwrites 1
	
	slice := rb.ToSlice()
	expected := []int{2, 3, 4}
	if !sliceEqual(slice, expected) {
		t.Errorf("expected %v, got %v", expected, slice)
	}
}

func TestToSliceEmpty(t *testing.T) {
	rb := NewRingBuffer[int](3)
	slice := rb.ToSlice()
	if len(slice) != 0 {
		t.Errorf("expected empty slice, got %v", slice)
	}
}

func TestClear(t *testing.T) {
	rb := NewRingBuffer[int](3)
	rb.Push(1)
	rb.Push(2)
	rb.Push(3)
	
	rb.Clear()
	
	if rb.Len() != 0 {
		t.Errorf("expected length 0, got %d", rb.Len())
	}
	if !rb.IsEmpty() {
		t.Error("expected empty buffer")
	}
}

func TestExtend(t *testing.T) {
	rb := NewRingBuffer[int](5)
	rb.Extend([]int{1, 2, 3, 4, 5})
	
	if rb.Len() != 5 {
		t.Errorf("expected length 5, got %d", rb.Len())
	}
	
	slice := rb.ToSlice()
	expected := []int{1, 2, 3, 4, 5}
	if !sliceEqual(slice, expected) {
		t.Errorf("expected %v, got %v", expected, slice)
	}
}

func TestExtendOverwrite(t *testing.T) {
	rb := NewRingBuffer[int](3)
	rb.Extend([]int{1, 2, 3, 4, 5})
	
	// Only last 3 should remain
	slice := rb.ToSlice()
	expected := []int{3, 4, 5}
	if !sliceEqual(slice, expected) {
		t.Errorf("expected %v, got %v", expected, slice)
	}
}

func TestForEach(t *testing.T) {
	rb := NewRingBuffer[int](5)
	rb.Extend([]int{1, 2, 3, 4, 5})
	
	sum := 0
	rb.ForEach(func(v int) bool {
		sum += v
		return true
	})
	
	if sum != 15 {
		t.Errorf("expected sum 15, got %d", sum)
	}
}

func TestForEachBreak(t *testing.T) {
	rb := NewRingBuffer[int](5)
	rb.Extend([]int{1, 2, 3, 4, 5})
	
	count := 0
	rb.ForEach(func(v int) bool {
		count++
		return count < 3
	})
	
	if count != 3 {
		t.Errorf("expected count 3, got %d", count)
	}
}

func TestContains(t *testing.T) {
	rb := NewRingBuffer[int](5)
	rb.Extend([]int{1, 2, 3, 4, 5})
	
	if !rb.Contains(3, intEqual) {
		t.Error("expected to contain 3")
	}
	if rb.Contains(6, intEqual) {
		t.Error("expected not to contain 6")
	}
}

func TestReverse(t *testing.T) {
	rb := NewRingBuffer[int](5)
	rb.Extend([]int{1, 2, 3, 4, 5})
	
	rev := rb.Reverse()
	expected := []int{5, 4, 3, 2, 1}
	if !sliceEqual(rev, expected) {
		t.Errorf("expected %v, got %v", expected, rev)
	}
}

func TestCopy(t *testing.T) {
	rb := NewRingBuffer[int](5)
	rb.Extend([]int{1, 2, 3, 4, 5})
	
	copyBuf := rb.Copy()
	
	if copyBuf.Len() != rb.Len() {
		t.Error("copy should have same length")
	}
	
	// Modify original
	rb.Push(6)
	
	// Copy should be unchanged
	if copyBuf.Len() != 5 {
		t.Error("copy should be unchanged")
	}
}

// ==================== Thread-Safe Tests ====================

func TestThreadSafeRingBuffer(t *testing.T) {
	rb := NewThreadSafeRingBuffer[int](100)
	
	var wg sync.WaitGroup
	numOps := 1000
	
	// Concurrent pushes
	wg.Add(numOps)
	for i := 0; i < numOps; i++ {
		go func(val int) {
			defer wg.Done()
			rb.Push(val)
		}(i)
	}
	
	wg.Wait()
	
	if rb.Len() != 100 {
		t.Errorf("expected length 100 (capacity limit), got %d", rb.Len())
	}
}

func TestThreadSafeReadWrite(t *testing.T) {
	rb := NewThreadSafeRingBuffer[int](50)
	
	var wg sync.WaitGroup
	
	// Writers
	wg.Add(10)
	for i := 0; i < 10; i++ {
		go func(start int) {
			defer wg.Done()
			for j := 0; j < 100; j++ {
				rb.Push(start + j)
			}
		}(i * 100)
	}
	
	// Readers
	wg.Add(10)
	for i := 0; i < 10; i++ {
		go func() {
			defer wg.Done()
			for j := 0; j < 100; j++ {
				rb.Len()
				rb.ToSlice()
				rb.Peek()
			}
		}()
	}
	
	wg.Wait()
}

// ==================== NumericRingBuffer Tests ====================

func TestNewNumericRingBuffer(t *testing.T) {
	nrb := NewNumericRingBuffer(5)
	if nrb.Cap() != 5 {
		t.Errorf("expected capacity 5, got %d", nrb.Cap())
	}
	if nrb.Len() != 0 {
		t.Errorf("expected length 0, got %d", nrb.Len())
	}
}

func TestNumericSum(t *testing.T) {
	nrb := NewNumericRingBuffer(5)
	nrb.Push(1.0)
	nrb.Push(2.0)
	nrb.Push(3.0)
	
	if nrb.Sum() != 6.0 {
		t.Errorf("expected sum 6.0, got %f", nrb.Sum())
	}
}

func TestNumericMean(t *testing.T) {
	nrb := NewNumericRingBuffer(5)
	nrb.Push(1.0)
	nrb.Push(2.0)
	nrb.Push(3.0)
	nrb.Push(4.0)
	nrb.Push(5.0)
	
	mean, err := nrb.Mean()
	if err != nil {
		t.Error(err)
	}
	if mean != 3.0 {
		t.Errorf("expected mean 3.0, got %f", mean)
	}
}

func TestNumericMeanEmpty(t *testing.T) {
	nrb := NewNumericRingBuffer(5)
	_, err := nrb.Mean()
	if !errors.Is(err, ErrBufferEmpty) {
		t.Errorf("expected ErrBufferEmpty, got %v", err)
	}
}

func TestNumericVariance(t *testing.T) {
	nrb := NewNumericRingBuffer(5)
	nrb.Push(1.0)
	nrb.Push(2.0)
	nrb.Push(3.0)
	nrb.Push(4.0)
	nrb.Push(5.0)
	
	variance, err := nrb.Variance()
	if err != nil {
		t.Error(err)
	}
	// Sample variance of [1,2,3,4,5] = 2.5
	expected := 2.5
	if math.Abs(variance-expected) > 0.0001 {
		t.Errorf("expected variance %.4f, got %.4f", expected, variance)
	}
}

func TestNumericStdDev(t *testing.T) {
	nrb := NewNumericRingBuffer(5)
	nrb.Push(1.0)
	nrb.Push(2.0)
	nrb.Push(3.0)
	nrb.Push(4.0)
	nrb.Push(5.0)
	
	stdDev, err := nrb.StdDev()
	if err != nil {
		t.Error(err)
	}
	// sqrt(2.5) ≈ 1.5811
	expected := math.Sqrt(2.5)
	if math.Abs(stdDev-expected) > 0.0001 {
		t.Errorf("expected stdDev %.4f, got %.4f", expected, stdDev)
	}
}

func TestNumericMinMax(t *testing.T) {
	nrb := NewNumericRingBuffer(5)
	nrb.Push(1.0)
	nrb.Push(2.0)
	nrb.Push(3.0)
	nrb.Push(4.0)
	nrb.Push(5.0)
	
	min, err := nrb.Min()
	if err != nil {
		t.Error(err)
	}
	if min != 1.0 {
		t.Errorf("expected min 1.0, got %f", min)
	}
	
	max, err := nrb.Max()
	if err != nil {
		t.Error(err)
	}
	if max != 5.0 {
		t.Errorf("expected max 5.0, got %f", max)
	}
}

func TestNumericRange(t *testing.T) {
	nrb := NewNumericRingBuffer(5)
	nrb.Push(1.0)
	nrb.Push(5.0)
	
	rangeVal, err := nrb.Range()
	if err != nil {
		t.Error(err)
	}
	if rangeVal != 4.0 {
		t.Errorf("expected range 4.0, got %f", rangeVal)
	}
}

func TestNumericMovingAverage(t *testing.T) {
	nrb := NewNumericRingBuffer(10)
	nrb.Extend([]float64{1, 2, 3, 4, 5, 6, 7, 8, 9, 10})
	
	ma, err := nrb.MovingAverage(3)
	if err != nil {
		t.Error(err)
	}
	
	expected := []float64{2, 3, 4, 5, 6, 7, 8, 9}
	if !sliceFloatEqual(ma, expected, 0.001) {
		t.Errorf("expected %v, got %v", expected, ma)
	}
}

func TestNumericMovingAverageInvalidWindow(t *testing.T) {
	nrb := NewNumericRingBuffer(5)
	nrb.Extend([]float64{1, 2, 3})
	
	_, err := nrb.MovingAverage(5)
	if !errors.Is(err, ErrInsufficientData) {
		t.Errorf("expected ErrInsufficientData, got %v", err)
	}
	
	_, err = nrb.MovingAverage(-1)
	if !errors.Is(err, ErrInvalidSize) {
		t.Errorf("expected ErrInvalidSize, got %v", err)
	}
}

func TestNumericMedian(t *testing.T) {
	nrb := NewNumericRingBuffer(5)
	nrb.Extend([]float64{1, 2, 3, 4, 5})
	
	median, err := nrb.Median()
	if err != nil {
		t.Error(err)
	}
	if median != 3.0 {
		t.Errorf("expected median 3.0, got %f", median)
	}
}

func TestNumericMedianEven(t *testing.T) {
	nrb := NewNumericRingBuffer(4)
	nrb.Extend([]float64{1, 2, 3, 4})
	
	median, err := nrb.Median()
	if err != nil {
		t.Error(err)
	}
	// Median of [1,2,3,4] = 2.5
	if math.Abs(median-2.5) > 0.0001 {
		t.Errorf("expected median 2.5, got %f", median)
	}
}

func TestNumericPercentile(t *testing.T) {
	nrb := NewNumericRingBuffer(100)
	for i := 1; i <= 100; i++ {
		nrb.Push(float64(i))
	}
	
	p50, err := nrb.Percentile(50)
	if err != nil {
		t.Error(err)
	}
	if math.Abs(p50-50.5) > 0.1 {
		t.Errorf("expected p50 ~50.5, got %f", p50)
	}
	
	p25, err := nrb.Percentile(25)
	if err != nil {
		t.Error(err)
	}
	if math.Abs(p25-25.25) > 0.1 {
		t.Errorf("expected p25 ~25.25, got %f", p25)
	}
	
	p75, err := nrb.Percentile(75)
	if err != nil {
		t.Error(err)
	}
	if math.Abs(p75-75.75) > 0.1 {
		t.Errorf("expected p75 ~75.75, got %f", p75)
	}
}

func TestNumericPercentileBoundary(t *testing.T) {
	nrb := NewNumericRingBuffer(5)
	nrb.Extend([]float64{1, 2, 3, 4, 5})
	
	p0, err := nrb.Percentile(0)
	if err != nil {
		t.Error(err)
	}
	if p0 != 1 {
		t.Errorf("expected p0 = 1, got %f", p0)
	}
	
	p100, err := nrb.Percentile(100)
	if err != nil {
		t.Error(err)
	}
	if p100 != 5 {
		t.Errorf("expected p100 = 5, got %f", p100)
	}
}

func TestNumericPercentileInvalid(t *testing.T) {
	nrb := NewNumericRingBuffer(5)
	nrb.Extend([]float64{1, 2, 3, 4, 5})
	
	_, err := nrb.Percentile(-1)
	if err == nil {
		t.Error("expected error for negative percentile")
	}
	
	_, err = nrb.Percentile(101)
	if err == nil {
		t.Error("expected error for percentile > 100")
	}
}

func TestNumericClear(t *testing.T) {
	nrb := NewNumericRingBuffer(5)
	nrb.Extend([]float64{1, 2, 3, 4, 5})
	
	nrb.Clear()
	
	if nrb.Len() != 0 {
		t.Errorf("expected length 0, got %d", nrb.Len())
	}
	if nrb.Sum() != 0 {
		t.Errorf("expected sum 0, got %f", nrb.Sum())
	}
}

func TestNumericOverwriteStats(t *testing.T) {
	nrb := NewNumericRingBuffer(3)
	nrb.Push(1.0)
	nrb.Push(2.0)
	nrb.Push(3.0)
	
	// Push overwrites 1
	nrb.Push(4.0)
	
	sum := nrb.Sum()
	expectedSum := 9.0 // 2+3+4
	if math.Abs(sum-expectedSum) > 0.0001 {
		t.Errorf("expected sum %.4f, got %.4f", expectedSum, sum)
	}
}

// ==================== Utility Functions Tests ====================

func TestSlidingWindow(t *testing.T) {
	data := []int{1, 2, 3, 4, 5}
	windows := SlidingWindow(data, 3)
	
	expected := [][]int{{1, 2, 3}, {2, 3, 4}, {3, 4, 5}}
	if len(windows) != len(expected) {
		t.Errorf("expected %d windows, got %d", len(expected), len(windows))
	}
	
	for i, win := range windows {
		if !sliceEqual(win, expected[i]) {
			t.Errorf("window %d: expected %v, got %v", i, expected[i], win)
		}
	}
}

func TestSlidingWindowInvalidSize(t *testing.T) {
	data := []int{1, 2, 3}
	
	windows := SlidingWindow(data, 0)
	if windows != nil {
		t.Error("expected nil for window size 0")
	}
	
	windows = SlidingWindow(data, -1)
	if windows != nil {
		t.Error("expected nil for negative window size")
	}
	
	windows = SlidingWindow(data, 10)
	if windows != nil {
		t.Error("expected nil when window > data length")
	}
}

func TestBatch(t *testing.T) {
	data := []int{1, 2, 3, 4, 5, 6, 7}
	
	sums := Batch(data, 3, func(batch []int) int {
		sum := 0
		for _, v := range batch {
			sum += v
		}
		return sum
	})
	
	expected := []int{6, 15, 7} // [1+2+3], [4+5+6], [7]
	if !sliceEqual(sums, expected) {
		t.Errorf("expected %v, got %v", expected, sums)
	}
}

func TestBatchInvalidSize(t *testing.T) {
	data := []int{1, 2, 3}
	
	result := Batch(data, 0, func(batch []int) int { return 0 })
	if result != nil {
		t.Error("expected nil for batch size 0")
	}
	
	result = Batch(data, -1, func(batch []int) int { return 0 })
	if result != nil {
		t.Error("expected nil for negative batch size")
	}
}

// ==================== Edge Cases Tests ====================

func TestSingleElementBuffer(t *testing.T) {
	rb := NewRingBuffer[int](1)
	rb.Push(42)
	
	if rb.Len() != 1 {
		t.Errorf("expected length 1, got %d", rb.Len())
	}
	if !rb.IsFull() {
		t.Error("expected full buffer")
	}
	
	val, _ := rb.Peek()
	if val != 42 {
		t.Errorf("expected 42, got %d", val)
	}
	
	// Overwrite
	rb.Push(100)
	slice := rb.ToSlice()
	if slice[0] != 100 {
		t.Errorf("expected 100, got %d", slice[0])
	}
}

func TestLargeBuffer(t *testing.T) {
	size := 10000
	rb := NewRingBuffer[int](size)
	
	for i := 0; i < size; i++ {
		rb.Push(i)
	}
	
	if rb.Len() != size {
		t.Errorf("expected length %d, got %d", size, rb.Len())
	}
}

func TestNegativeValues(t *testing.T) {
	nrb := NewNumericRingBuffer(5)
	nrb.Extend([]float64{-5, -3, -1, 0, 2})
	
	min, _ := nrb.Min()
	if min != -5 {
		t.Errorf("expected min -5, got %f", min)
	}
	
	max, _ := nrb.Max()
	if max != 2 {
		t.Errorf("expected max 2, got %f", max)
	}
}

func TestFloatPrecision(t *testing.T) {
	nrb := NewNumericRingBuffer(5)
	nrb.Extend([]float64{0.1, 0.2, 0.3})
	
	sum := nrb.Sum()
	// 0.1 + 0.2 + 0.3 might not be exactly 0.6 due to float precision
	if math.Abs(sum-0.6) > 0.0001 {
		t.Errorf("expected sum ~0.6, got %f", sum)
	}
}

func TestZeroCapacity(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Error("expected panic for zero capacity")
		}
	}()
	NewRingBuffer[int](0)
}

func TestEmptyBufferOperations(t *testing.T) {
	rb := NewRingBuffer[int](5)
	
	// All operations on empty buffer should handle gracefully
	slice := rb.ToSlice()
	if len(slice) != 0 {
		t.Error("expected empty slice")
	}
	
	rb.ForEach(func(v int) bool {
		t.Error("ForEach should not call function on empty buffer")
		return true
	})
	
	rb.Clear() // Should work without error
}

func TestThreadSafeNumericBuffer(t *testing.T) {
	nrb := NewThreadSafeNumericRingBuffer(100)
	
	var wg sync.WaitGroup
	numOps := 1000
	
	wg.Add(numOps)
	for i := 0; i < numOps; i++ {
		go func(val float64) {
			defer wg.Done()
			nrb.Push(val)
		}(float64(i))
	}
	
	wg.Wait()
	
	if nrb.Len() != 100 {
		t.Errorf("expected length 100, got %d", nrb.Len())
	}
}

func TestThreadSafeStatistics(t *testing.T) {
	nrb := NewThreadSafeNumericRingBuffer(50)
	
	var wg sync.WaitGroup
	
	// Writers
	wg.Add(10)
	for i := 0; i < 10; i++ {
		go func(start float64) {
			defer wg.Done()
			for j := 0; j < 100; j++ {
				nrb.Push(start + float64(j))
			}
		}(float64(i * 100))
	}
	
	// Readers
	wg.Add(10)
	for i := 0; i < 10; i++ {
		go func() {
			defer wg.Done()
			for j := 0; j < 100; j++ {
				nrb.Mean()
				nrb.Sum()
				nrb.Min()
				nrb.Max()
			}
		}()
	}
	
	wg.Wait()
}

// ==================== Helper Functions ====================

func sliceEqual(a, b []int) bool {
	if len(a) != len(b) {
		return false
	}
	for i := range a {
		if a[i] != b[i] {
			return false
		}
	}
	return true
}

func sliceFloatEqual(a, b []float64, tolerance float64) bool {
	if len(a) != len(b) {
		return false
	}
	for i := range a {
		if math.Abs(a[i]-b[i]) > tolerance {
			return false
		}
	}
	return true
}

func intEqual(a, b int) bool {
	return a == b
}

// ==================== Benchmark Tests ====================

func BenchmarkPush(b *testing.B) {
	rb := NewRingBuffer[int](1000)
	for i := 0; i < b.N; i++ {
		rb.Push(i)
	}
}

func BenchmarkPop(b *testing.B) {
	rb := NewRingBuffer[int](b.N)
	for i := 0; i < b.N; i++ {
		rb.Push(i)
	}
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		rb.Pop()
	}
}

func BenchmarkToSlice(b *testing.B) {
	rb := NewRingBuffer[int](1000)
	for i := 0; i < 1000; i++ {
		rb.Push(i)
	}
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		rb.ToSlice()
	}
}

func BenchmarkThreadSafePush(b *testing.B) {
	rb := NewThreadSafeRingBuffer[int](1000)
	b.RunParallel(func(pb *testing.PB) {
		i := 0
		for pb.Next() {
			rb.Push(i)
			i++
		}
	})
}

func BenchmarkNumericPush(b *testing.B) {
	nrb := NewNumericRingBuffer(1000)
	for i := 0; i < b.N; i++ {
		nrb.Push(float64(i))
	}
}

func BenchmarkNumericMean(b *testing.B) {
	nrb := NewNumericRingBuffer(1000)
	for i := 0; i < 1000; i++ {
		nrb.Push(float64(i))
	}
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		nrb.Mean()
	}
}

func BenchmarkSlidingWindow(b *testing.B) {
	data := make([]int, 1000)
	for i := range data {
		data[i] = i
	}
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		SlidingWindow(data, 100)
	}
}

func BenchmarkBatch(b *testing.B) {
	data := make([]int, 1000)
	for i := range data {
		data[i] = i
	}
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		Batch(data, 100, func(batch []int) int {
			sum := 0
			for _, v := range batch {
				sum += v
			}
			return sum
		})
	}
}

// ==================== Example Tests ====================

func ExampleRingBuffer_basic() {
	rb := NewRingBuffer[int](3)
	rb.Push(1)
	rb.Push(2)
	rb.Push(3)
	
	// Buffer is full, next push overwrites
	rb.Push(4)
	
	fmt.Println(rb.ToSlice())
	// Output: [2 3 4]
}

func ExampleRingBuffer_iteration() {
	rb := NewRingBuffer[string](3)
	rb.Push("a")
	rb.Push("b")
	rb.Push("c")
	
	rb.ForEach(func(s string) bool {
		fmt.Println(s)
		return true
	})
	// Output:
	// a
	// b
	// c
}

func ExampleNumericRingBuffer_stats() {
	nrb := NewNumericRingBuffer(5)
	nrb.Extend([]float64{10, 20, 30, 40, 50})
	
	mean, _ := nrb.Mean()
	fmt.Printf("Mean: %.1f\n", mean)
	
	stdDev, _ := nrb.StdDev()
	fmt.Printf("StdDev: %.2f\n", stdDev)
	
	// Output:
	// Mean: 30.0
	// StdDev: 15.81
}

func ExampleSlidingWindow() {
	data := []int{1, 2, 3, 4, 5}
	windows := SlidingWindow(data, 3)
	
	for _, win := range windows {
		fmt.Println(win)
	}
	// Output:
	// [1 2 3]
	// [2 3 4]
	// [3 4 5]
}

func ExampleBatch() {
	data := []int{1, 2, 3, 4, 5, 6, 7}
	
	// Process in batches of 3
	results := Batch(data, 3, func(batch []int) int {
		sum := 0
		for _, v := range batch {
			sum += v
		}
		return sum
	})
	
	fmt.Println(results)
	// Output: [6 15 7]
}

func TestRaceCondition(t *testing.T) {
	rb := NewThreadSafeRingBuffer[int](1000)
	
	var wg sync.WaitGroup
	
	// Concurrent operations
	for i := 0; i < 100; i++ {
		wg.Add(4)
		
		// Push
		go func(val int) {
			defer wg.Done()
			rb.Push(val)
		}(i)
		
		// Pop
		go func() {
			defer wg.Done()
			rb.Pop()
		}()
		
		// Len
		go func() {
			defer wg.Done()
			rb.Len()
		}()
		
		// ToSlice
		go func() {
			defer wg.Done()
			rb.ToSlice()
		}()
	}
	
	wg.Wait()
}

func TestRaceConditionNumeric(t *testing.T) {
	nrb := NewThreadSafeNumericRingBuffer(500)
	
	var wg sync.WaitGroup
	
	// Concurrent operations
	for i := 0; i < 100; i++ {
		wg.Add(5)
		
		go func(val float64) {
			defer wg.Done()
			nrb.Push(val)
		}(float64(i))
		
		go func() {
			defer wg.Done()
			nrb.Mean()
		}()
		
		go func() {
			defer wg.Done()
			nrb.Sum()
		}()
		
		go func() {
			defer wg.Done()
			nrb.Min()
		}()
		
		go func() {
			defer wg.Done()
			nrb.Max()
		}()
	}
	
	wg.Wait()
}

// Test for memory efficiency
func TestMemoryEfficiency(t *testing.T) {
	rb := NewRingBuffer[int](1000000)
	
	for i := 0; i < 2000000; i++ {
		rb.Push(i)
	}
	
	// Should only have last 1M elements
	if rb.Len() != 1000000 {
		t.Errorf("expected length 1000000, got %d", rb.Len())
	}
	
	start := time.Now()
	slice := rb.ToSlice()
	elapsed := time.Since(start)
	
	if len(slice) != 1000000 {
		t.Errorf("expected slice length 1000000, got %d", len(slice))
	}
	
	t.Logf("ToSlice on 1M elements took %v", elapsed)
}
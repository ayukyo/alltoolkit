//! # Ring Buffer (Circular Buffer)
//!
//! A generic, zero-dependency circular buffer implementation in Rust.
//!
//! ## Features
//!
//! - Fixed-size circular buffer with efficient O(1) operations
//! - Generic type support for any element type
//! - Overflow handling modes: overwrite, error, or skip
//! - Iterator support for efficient traversal
//! - No external dependencies
//!
//! ## Example
//!
//! ```
//! use ring_buffer::RingBuffer;
//!
//! let mut buf = RingBuffer::new(3);
//! buf.push(1);
//! buf.push(2);
//! buf.push(3);
//! assert_eq!(buf.to_vec(), vec![1, 2, 3]);
//!
//! // Overwrites oldest element when full
//! buf.push(4);
//! assert_eq!(buf.to_vec(), vec![2, 3, 4]);
//! ```

use std::collections::VecDeque;

/// Overflow behavior when buffer is full
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum OverflowMode {
    /// Overwrite oldest element (default)
    Overwrite,
    /// Return error when buffer is full
    Error,
    /// Skip the push operation silently
    Skip,
}

/// A circular buffer (ring buffer) with configurable overflow behavior
#[derive(Debug, Clone)]
pub struct RingBuffer<T> {
    data: VecDeque<T>,
    capacity: usize,
    mode: OverflowMode,
}

impl<T> RingBuffer<T> {
    /// Creates a new empty ring buffer with given capacity
    ///
    /// # Panics
    ///
    /// Panics if capacity is 0
    ///
    /// # Example
    ///
    /// ```
    /// use ring_buffer::RingBuffer;
    ///
    /// let buf: RingBuffer<i32> = RingBuffer::new(5);
    /// assert!(buf.is_empty());
    /// ```
    pub fn new(capacity: usize) -> Self {
        if capacity == 0 {
            panic!("Ring buffer capacity must be greater than 0");
        }
        RingBuffer {
            data: VecDeque::with_capacity(capacity),
            capacity,
            mode: OverflowMode::Overwrite,
        }
    }

    /// Creates a new ring buffer with specific overflow mode
    ///
    /// # Example
    ///
    /// ```
    /// use ring_buffer::{RingBuffer, OverflowMode};
    ///
    /// let buf: RingBuffer<i32> = RingBuffer::with_mode(5, OverflowMode::Error);
    /// ```
    pub fn with_mode(capacity: usize, mode: OverflowMode) -> Self {
        let mut buf = Self::new(capacity);
        buf.mode = mode;
        buf
    }

    /// Returns the capacity of the buffer
    pub fn capacity(&self) -> usize {
        self.capacity
    }

    /// Returns the current number of elements
    pub fn len(&self) -> usize {
        self.data.len()
    }

    /// Returns true if the buffer is empty
    pub fn is_empty(&self) -> bool {
        self.data.is_empty()
    }

    /// Returns true if the buffer is full
    pub fn is_full(&self) -> bool {
        self.data.len() == self.capacity
    }

    /// Returns the overflow mode
    pub fn overflow_mode(&self) -> OverflowMode {
        self.mode
    }

    /// Sets the overflow mode
    pub fn set_overflow_mode(&mut self, mode: OverflowMode) {
        self.mode = mode;
    }

    /// Pushes an element to the back of the buffer
    ///
    /// Returns Ok(()) on success, or Err(()) if buffer is full in Error mode
    ///
    /// # Example
    ///
    /// ```
    /// use ring_buffer::{RingBuffer, OverflowMode};
    ///
    /// let mut buf = RingBuffer::with_mode(2, OverflowMode::Overwrite);
    /// buf.push(1).unwrap();
    /// buf.push(2).unwrap();
    /// buf.push(3).unwrap(); // Overwrites 1
    /// assert_eq!(buf.to_vec(), vec![2, 3]);
    ///
    /// let mut buf2 = RingBuffer::with_mode(2, OverflowMode::Error);
    /// buf2.push(1).unwrap();
    /// buf2.push(2).unwrap();
    /// assert!(buf2.push(3).is_err());
    /// ```
    pub fn push(&mut self, item: T) -> Result<(), ()> {
        if self.is_full() {
            match self.mode {
                OverflowMode::Overwrite => {
                    self.data.pop_front();
                }
                OverflowMode::Error => {
                    return Err(());
                }
                OverflowMode::Skip => {
                    return Ok(());
                }
            }
        }
        self.data.push_back(item);
        Ok(())
    }

    /// Pushes multiple elements at once
    ///
    /// # Example
    ///
    /// ```
    /// use ring_buffer::RingBuffer;
    ///
    /// let mut buf = RingBuffer::new(3);
    /// buf.extend(vec![1, 2, 3, 4, 5]);
    /// assert_eq!(buf.to_vec(), vec![3, 4, 5]);
    /// ```
    pub fn extend(&mut self, items: impl IntoIterator<Item = T>) {
        for item in items {
            let _ = self.push(item);
        }
    }

    /// Pops an element from the front of the buffer
    ///
    /// # Example
    ///
    /// ```
    /// use ring_buffer::RingBuffer;
    ///
    /// let mut buf = RingBuffer::new(3);
    /// buf.push(1);
    /// buf.push(2);
    /// assert_eq!(buf.pop(), Some(1));
    /// assert_eq!(buf.pop(), Some(2));
    /// assert_eq!(buf.pop(), None);
    /// ```
    pub fn pop(&mut self) -> Option<T> {
        self.data.pop_front()
    }

    /// Peeks at the front element without removing it
    ///
    /// # Example
    ///
    /// ```
    /// use ring_buffer::RingBuffer;
    ///
    /// let mut buf = RingBuffer::new(3);
    /// buf.push(1);
    /// assert_eq!(buf.peek(), Some(&1));
    /// assert_eq!(buf.len(), 1);
    /// ```
    pub fn peek(&self) -> Option<&T> {
        self.data.front()
    }

    /// Peeks at the back element without removing it
    ///
    /// # Example
    ///
    /// ```
    /// use ring_buffer::RingBuffer;
    ///
    /// let mut buf = RingBuffer::new(3);
    /// buf.push(1);
    /// buf.push(2);
    /// assert_eq!(buf.peek_back(), Some(&2));
    /// ```
    pub fn peek_back(&self) -> Option<&T> {
        self.data.back()
    }

    /// Clears all elements from the buffer
    ///
    /// # Example
    ///
    /// ```
    /// use ring_buffer::RingBuffer;
    ///
    /// let mut buf = RingBuffer::new(3);
    /// buf.push(1);
    /// buf.clear();
    /// assert!(buf.is_empty());
    /// ```
    pub fn clear(&mut self) {
        self.data.clear();
    }

    /// Returns the buffer contents as a Vec
    ///
    /// # Example
    ///
    /// ```
    /// use ring_buffer::RingBuffer;
    ///
    /// let mut buf = RingBuffer::new(3);
    /// buf.push(1);
    /// buf.push(2);
    /// assert_eq!(buf.to_vec(), vec![1, 2]);
    /// ```
    pub fn to_vec(&self) -> Vec<T>
    where
        T: Clone,
    {
        self.data.iter().cloned().collect()
    }

    /// Returns an iterator over the buffer elements
    ///
    /// # Example
    ///
    /// ```
    /// use ring_buffer::RingBuffer;
    ///
    /// let mut buf = RingBuffer::new(3);
    /// buf.push(1);
    /// buf.push(2);
    /// let sum: i32 = buf.iter().sum();
    /// assert_eq!(sum, 3);
    /// ```
    pub fn iter(&self) -> impl Iterator<Item = &T> {
        self.data.iter()
    }

    /// Gets an element by index (0 = oldest, len-1 = newest)
    ///
    /// # Example
    ///
    /// ```
    /// use ring_buffer::RingBuffer;
    ///
    /// let mut buf = RingBuffer::new(3);
    /// buf.push(10);
    /// buf.push(20);
    /// buf.push(30);
    /// assert_eq!(buf.get(0), Some(&10));
    /// assert_eq!(buf.get(2), Some(&30));
    /// assert_eq!(buf.get(3), None);
    /// ```
    pub fn get(&self, index: usize) -> Option<&T> {
        self.data.get(index)
    }

    /// Gets the most recently added element
    ///
    /// # Example
    ///
    /// ```
    /// use ring_buffer::RingBuffer;
    ///
    /// let mut buf = RingBuffer::new(3);
    /// buf.push(1);
    /// buf.push(2);
    /// assert_eq!(buf.latest(), Some(&2));
    /// ```
    pub fn latest(&self) -> Option<&T> {
        self.data.back()
    }

    /// Gets the oldest element
    ///
    /// # Example
    ///
    /// ```
    /// use ring_buffer::RingBuffer;
    ///
    /// let mut buf = RingBuffer::new(3);
    /// buf.push(1);
    /// buf.push(2);
    /// assert_eq!(buf.oldest(), Some(&1));
    /// ```
    pub fn oldest(&self) -> Option<&T> {
        self.data.front()
    }

    /// Creates a ring buffer from a Vec, taking at most capacity elements
    ///
    /// # Example
    ///
    /// ```
    /// use ring_buffer::RingBuffer;
    ///
    /// let buf = RingBuffer::from_vec(vec![1, 2, 3, 4, 5], 3);
    /// assert_eq!(buf.to_vec(), vec![3, 4, 5]);
    /// ```
    pub fn from_vec(vec: Vec<T>, capacity: usize) -> Self {
        let mut buf = Self::new(capacity);
        buf.extend(vec);
        buf
    }

    /// Returns available space in the buffer
    ///
    /// # Example
    ///
    /// ```
    /// use ring_buffer::RingBuffer;
    ///
    /// let mut buf = RingBuffer::new(5);
    /// buf.push(1);
    /// buf.push(2);
    /// assert_eq!(buf.available(), 3);
    /// ```
    pub fn available(&self) -> usize {
        self.capacity - self.data.len()
    }

    /// Drains all elements and returns them as a Vec
    ///
    /// # Example
    ///
    /// ```
    /// use ring_buffer::RingBuffer;
    ///
    /// let mut buf = RingBuffer::new(3);
    /// buf.push(1);
    /// buf.push(2);
    /// let drained = buf.drain();
    /// assert_eq!(drained, vec![1, 2]);
    /// assert!(buf.is_empty());
    /// ```
    pub fn drain(&mut self) -> Vec<T> {
        self.data.drain(..).collect()
    }

    /// Checks if the buffer contains an element
    ///
    /// # Example
    ///
    /// ```
    /// use ring_buffer::RingBuffer;
    ///
    /// let mut buf = RingBuffer::new(3);
    /// buf.push(1);
    /// buf.push(2);
    /// assert!(buf.contains(&1));
    /// assert!(!buf.contains(&3));
    /// ```
    pub fn contains(&self, item: &T) -> bool
    where
        T: PartialEq,
    {
        self.data.contains(item)
    }

    /// Returns the number of elements matching a predicate
    ///
    /// # Example
    ///
    /// ```
    /// use ring_buffer::RingBuffer;
    ///
    /// let mut buf = RingBuffer::new(10);
    /// buf.extend(vec![1, 2, 3, 4, 5]);
    /// assert_eq!(buf.count_if(|&x| x > 2), 3);
    /// ```
    pub fn count_if<F>(&self, predicate: F) -> usize
    where
        F: Fn(&T) -> bool,
    {
        self.data.iter().filter(|x| predicate(x)).count()
    }

    /// Reverses the buffer order in place
    ///
    /// # Example
    ///
    /// ```
    /// use ring_buffer::RingBuffer;
    ///
    /// let mut buf = RingBuffer::new(3);
    /// buf.extend(vec![1, 2, 3]);
    /// buf.reverse();
    /// assert_eq!(buf.to_vec(), vec![3, 2, 1]);
    /// ```
    pub fn reverse(&mut self) {
        let items: Vec<T> = self.drain().into_iter().rev().collect();
        self.extend(items);
    }

    /// Rotates the buffer left by n positions
    ///
    /// # Example
    ///
    /// ```
    /// use ring_buffer::RingBuffer;
    ///
    /// let mut buf = RingBuffer::new(5);
    /// buf.extend(vec![1, 2, 3, 4, 5]);
    /// buf.rotate_left(2);
    /// assert_eq!(buf.to_vec(), vec![3, 4, 5, 1, 2]);
    /// ```
    pub fn rotate_left(&mut self, n: usize) {
        if self.is_empty() || n == 0 {
            return;
        }
        let n = n % self.len();
        self.data.rotate_left(n);
    }

    /// Rotates the buffer right by n positions
    ///
    /// # Example
    ///
    /// ```
    /// use ring_buffer::RingBuffer;
    ///
    /// let mut buf = RingBuffer::new(5);
    /// buf.extend(vec![1, 2, 3, 4, 5]);
    /// buf.rotate_right(2);
    /// assert_eq!(buf.to_vec(), vec![4, 5, 1, 2, 3]);
    /// ```
    pub fn rotate_right(&mut self, n: usize) {
        if self.is_empty() || n == 0 {
            return;
        }
        let n = n % self.len();
        self.data.rotate_right(n);
    }
}

impl<T> Default for RingBuffer<T> {
    fn default() -> Self {
        Self::new(16)
    }
}

impl<T: Clone> FromIterator<T> for RingBuffer<T> {
    fn from_iter<I: IntoIterator<Item = T>>(iter: I) -> Self {
        let items: Vec<T> = iter.into_iter().collect();
        let capacity = items.len().max(1);
        Self::from_vec(items, capacity)
    }
}

impl<T> IntoIterator for RingBuffer<T> {
    type Item = T;
    type IntoIter = std::collections::vec_deque::IntoIter<T>;

    fn into_iter(self) -> Self::IntoIter {
        self.data.into_iter()
    }
}

/// A fixed-size ring buffer that stores the most recent N numeric values
/// and provides statistics like sum, average, min, max.
#[derive(Debug, Clone)]
pub struct NumericRingBuffer {
    buffer: RingBuffer<f64>,
}

impl NumericRingBuffer {
    /// Creates a new numeric ring buffer
    pub fn new(capacity: usize) -> Self {
        NumericRingBuffer {
            buffer: RingBuffer::new(capacity),
        }
    }

    /// Pushes a value to the buffer
    pub fn push(&mut self, value: f64) {
        let _ = self.buffer.push(value);
    }

    /// Returns the sum of all values
    pub fn sum(&self) -> f64 {
        self.buffer.iter().sum()
    }

    /// Returns the average of all values
    ///
    /// # Example
    ///
    /// ```
    /// use ring_buffer::NumericRingBuffer;
    ///
    /// let mut buf = NumericRingBuffer::new(5);
    /// buf.push(10.0);
    /// buf.push(20.0);
    /// buf.push(30.0);
    /// assert_eq!(buf.average(), Some(20.0));
    /// ```
    pub fn average(&self) -> Option<f64> {
        if self.buffer.is_empty() {
            None
        } else {
            Some(self.sum() / self.buffer.len() as f64)
        }
    }

    /// Returns the minimum value
    pub fn min(&self) -> Option<f64> {
        self.buffer.iter().copied().fold(None, |acc, x| {
            Some(acc.map_or(x, |m: f64| m.min(x)))
        })
    }

    /// Returns the maximum value
    pub fn max(&self) -> Option<f64> {
        self.buffer.iter().copied().fold(None, |acc, x| {
            Some(acc.map_or(x, |m: f64| m.max(x)))
        })
    }

    /// Returns the number of elements
    pub fn len(&self) -> usize {
        self.buffer.len()
    }

    /// Returns true if empty
    pub fn is_empty(&self) -> bool {
        self.buffer.is_empty()
    }

    /// Clears the buffer
    pub fn clear(&mut self) {
        self.buffer.clear();
    }

    /// Returns all values as a Vec
    pub fn to_vec(&self) -> Vec<f64> {
        self.buffer.to_vec()
    }

    /// Returns the variance of values (population variance)
    pub fn variance(&self) -> Option<f64> {
        let avg = self.average()?;
        let count = self.len() as f64;
        let sum_sq: f64 = self.buffer.iter().map(|&x| (x - avg).powi(2)).sum();
        Some(sum_sq / count)
    }

    /// Returns the standard deviation
    pub fn std_dev(&self) -> Option<f64> {
        self.variance().map(|v| v.sqrt())
    }

    /// Returns statistics summary
    pub fn stats(&self) -> Option<BufferStats> {
        if self.buffer.is_empty() {
            return None;
        }
        Some(BufferStats {
            count: self.len(),
            sum: self.sum(),
            average: self.average()?,
            min: self.min()?,
            max: self.max()?,
            variance: self.variance()?,
            std_dev: self.std_dev()?,
        })
    }
}

/// Statistics for a numeric ring buffer
#[derive(Debug, Clone, Copy)]
pub struct BufferStats {
    pub count: usize,
    pub sum: f64,
    pub average: f64,
    pub min: f64,
    pub max: f64,
    pub variance: f64,
    pub std_dev: f64,
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_basic_operations() {
        let mut buf = RingBuffer::new(3);
        assert!(buf.is_empty());
        assert_eq!(buf.len(), 0);
        assert_eq!(buf.capacity(), 3);

        buf.push(1).unwrap();
        buf.push(2).unwrap();
        assert_eq!(buf.len(), 2);
        assert!(!buf.is_full());

        buf.push(3).unwrap();
        assert!(buf.is_full());
    }

    #[test]
    fn test_overflow_overwrite() {
        let mut buf = RingBuffer::new(3);
        buf.push(1).unwrap();
        buf.push(2).unwrap();
        buf.push(3).unwrap();
        buf.push(4).unwrap(); // Should overwrite 1

        assert_eq!(buf.to_vec(), vec![2, 3, 4]);
    }

    #[test]
    fn test_overflow_error() {
        let mut buf = RingBuffer::with_mode(2, OverflowMode::Error);
        buf.push(1).unwrap();
        buf.push(2).unwrap();
        assert!(buf.push(3).is_err());
        assert_eq!(buf.to_vec(), vec![1, 2]);
    }

    #[test]
    fn test_overflow_skip() {
        let mut buf = RingBuffer::with_mode(2, OverflowMode::Skip);
        buf.push(1).unwrap();
        buf.push(2).unwrap();
        assert!(buf.push(3).is_ok()); // Silently skipped
        assert_eq!(buf.to_vec(), vec![1, 2]);
    }

    #[test]
    fn test_pop_and_peek() {
        let mut buf = RingBuffer::new(3);
        buf.push(1).unwrap();
        buf.push(2).unwrap();

        assert_eq!(buf.peek(), Some(&1));
        assert_eq!(buf.pop(), Some(1));
        assert_eq!(buf.peek(), Some(&2));
        assert_eq!(buf.pop(), Some(2));
        assert_eq!(buf.pop(), None);
    }

    #[test]
    fn test_extend() {
        let mut buf = RingBuffer::new(3);
        buf.extend(vec![1, 2, 3, 4, 5]);
        assert_eq!(buf.to_vec(), vec![3, 4, 5]);
    }

    #[test]
    fn test_rotate() {
        let mut buf = RingBuffer::new(5);
        buf.extend(vec![1, 2, 3, 4, 5]);

        buf.rotate_left(2);
        assert_eq!(buf.to_vec(), vec![3, 4, 5, 1, 2]);

        buf.rotate_right(2); // Rotate back by the same amount
        assert_eq!(buf.to_vec(), vec![1, 2, 3, 4, 5]);
    }

    #[test]
    fn test_contains_and_count_if() {
        let mut buf = RingBuffer::new(10);
        buf.extend(vec![1, 2, 3, 4, 5]);

        assert!(buf.contains(&3));
        assert!(!buf.contains(&6));
        assert_eq!(buf.count_if(|&x| x % 2 == 0), 2);
    }

    #[test]
    fn test_numeric_buffer() {
        let mut buf = NumericRingBuffer::new(5);
        buf.push(10.0);
        buf.push(20.0);
        buf.push(30.0);

        assert_eq!(buf.average(), Some(20.0));
        assert_eq!(buf.min(), Some(10.0));
        assert_eq!(buf.max(), Some(30.0));
        assert_eq!(buf.sum(), 60.0);

        let stats = buf.stats().unwrap();
        assert_eq!(stats.count, 3);
        assert_eq!(stats.average, 20.0);
    }

    #[test]
    fn test_from_iterator() {
        let buf: RingBuffer<i32> = (1..=5).collect();
        assert_eq!(buf.to_vec(), vec![1, 2, 3, 4, 5]);
    }

    #[test]
    fn test_into_iterator() {
        let mut buf = RingBuffer::new(3);
        buf.extend(vec![1, 2, 3]);

        let sum: i32 = buf.into_iter().sum();
        assert_eq!(sum, 6);
    }

    #[test]
    fn test_drain() {
        let mut buf = RingBuffer::new(3);
        buf.extend(vec![1, 2, 3]);

        let drained = buf.drain();
        assert_eq!(drained, vec![1, 2, 3]);
        assert!(buf.is_empty());
    }

    #[test]
    fn test_get_latest_oldest() {
        let mut buf = RingBuffer::new(3);
        buf.extend(vec![1, 2, 3]);

        assert_eq!(buf.get(0), Some(&1));
        assert_eq!(buf.get(2), Some(&3));
        assert_eq!(buf.get(3), None);
        assert_eq!(buf.oldest(), Some(&1));
        assert_eq!(buf.latest(), Some(&3));
    }

    #[test]
    fn test_variance_std_dev() {
        let mut buf = NumericRingBuffer::new(10);
        buf.push(2.0);
        buf.push(4.0);
        buf.push(4.0);
        buf.push(4.0);
        buf.push(5.0);
        buf.push(5.0);
        buf.push(7.0);
        buf.push(9.0);

        let stats = buf.stats().unwrap();
        // Verify the calculations
        assert!((stats.average - 5.0).abs() < 0.0001);
        assert!((stats.variance - 4.0).abs() < 0.0001);
        assert!((stats.std_dev - 2.0).abs() < 0.0001);
    }

    #[test]
    #[should_panic]
    fn test_zero_capacity_panics() {
        let _ = RingBuffer::<i32>::new(0);
    }
}
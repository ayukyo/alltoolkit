//! Basic usage examples for ring_buffer

use ring_buffer::{NumericRingBuffer, OverflowMode, RingBuffer};

fn main() {
    println!("=== Ring Buffer Examples ===\n");

    // Example 1: Basic circular buffer
    println!("1. Basic Ring Buffer:");
    let mut buf = RingBuffer::new(3);
    buf.push(1).unwrap();
    buf.push(2).unwrap();
    buf.push(3).unwrap();
    println!("   Buffer: {:?}", buf.to_vec());
    println!("   Is full: {}", buf.is_full());

    buf.push(4).unwrap(); // Overwrites oldest (1)
    println!("   After push(4): {:?}", buf.to_vec());
    buf.push(5).unwrap(); // Overwrites oldest (2)
    println!("   After push(5): {:?}", buf.to_vec());
    println!();

    // Example 2: Overflow modes
    println!("2. Overflow Modes:");
    
    // Overwrite mode (default)
    let mut overwrite = RingBuffer::new(2);
    overwrite.extend(vec![1, 2, 3]);
    println!("   Overwrite mode: {:?}", overwrite.to_vec());

    // Error mode
    let mut error_mode = RingBuffer::with_mode(2, OverflowMode::Error);
    error_mode.push(1).unwrap();
    error_mode.push(2).unwrap();
    match error_mode.push(3) {
        Ok(()) => println!("   Error mode: push succeeded"),
        Err(()) => println!("   Error mode: push failed (buffer full)"),
    }

    // Skip mode
    let mut skip_mode = RingBuffer::with_mode(2, OverflowMode::Skip);
    skip_mode.extend(vec![1, 2, 3]);
    println!("   Skip mode: {:?}", skip_mode.to_vec());
    println!();

    // Example 3: Numeric buffer with statistics
    println!("3. Numeric Ring Buffer (Statistics):");
    let mut num_buf = NumericRingBuffer::new(10);
    let values = vec![10.5, 20.3, 15.7, 18.2, 22.1, 19.8, 17.5];
    for v in &values {
        num_buf.push(*v);
    }
    println!("   Values: {:?}", num_buf.to_vec());
    if let Some(stats) = num_buf.stats() {
        println!("   Count: {}", stats.count);
        println!("   Sum: {:.2}", stats.sum);
        println!("   Average: {:.2}", stats.average);
        println!("   Min: {:.2}", stats.min);
        println!("   Max: {:.2}", stats.max);
        println!("   Std Dev: {:.2}", stats.std_dev);
    }
    println!();

    // Example 4: Rotation
    println!("4. Buffer Rotation:");
    let mut rotate_buf = RingBuffer::new(5);
    rotate_buf.extend(vec![1, 2, 3, 4, 5]);
    println!("   Original: {:?}", rotate_buf.to_vec());
    
    rotate_buf.rotate_left(2);
    println!("   Rotate left 2: {:?}", rotate_buf.to_vec());
    
    rotate_buf.rotate_right(3);
    println!("   Rotate right 3: {:?}", rotate_buf.to_vec());
    println!();

    // Example 5: Sliding window (moving average)
    println!("5. Moving Average Simulation:");
    let mut window = NumericRingBuffer::new(5);
    let data = vec![10.0, 11.0, 12.0, 13.0, 14.0, 15.0, 16.0, 17.0, 18.0, 19.0];
    
    println!("   Window size: 5");
    print!("   Values: ");
    for v in &data {
        window.push(*v);
        if window.len() == 5 {
            print!("({:.1}) ", window.average().unwrap());
        }
    }
    println!("\n   Final window: {:?}", window.to_vec());
    println!();

    // Example 6: Pop and peek operations
    println!("6. Pop and Peek Operations:");
    let mut queue = RingBuffer::new(10);
    queue.extend(vec![10, 20, 30, 40, 50]);
    println!("   Initial: {:?}", queue.to_vec());
    
    println!("   Peek front: {:?}", queue.peek());
    println!("   Peek back: {:?}", queue.peek_back());
    println!("   Pop: {:?}", queue.pop());
    println!("   After pop: {:?}", queue.to_vec());
    println!("   Drain all: {:?}", queue.drain());
    println!("   Is empty: {}", queue.is_empty());
}
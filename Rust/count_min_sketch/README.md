# Count-Min Sketch

A probabilistic data structure for frequency estimation in streaming data.

## Features

- **Zero external dependencies** - Pure Rust standard library
- **Configurable accuracy** - Trade-off between space and precision
- **Mergeable** - Combine sketches from distributed streams
- **Serializable** - Store and restore sketches from bytes

## Usage

```rust
use count_min_sketch::{CountMinSketch, CountMinConfig};

let mut sketch: CountMinSketch<&str> = CountMinSketch::new_default();

// Add items
sketch.increment("hello");
sketch.increment("hello");
sketch.increment("world");

// Estimate frequency (returns upper bound)
let hello_count = sketch.estimate("hello");  // >= 2
let world_count = sketch.estimate("world");   // >= 1
let missing = sketch.estimate("missing");    // == 0
```

## Configuration

```rust
// Default: depth=10, width=1000
let sketch: CountMinSketch<&str> = CountMinSketch::new_default();

// Optimal config for 1% error, 99% confidence
let sketch: CountMinSketch<&str> = CountMinSketch::with_rate(0.01, 0.01);

// Custom dimensions
let config = CountMinConfig::new(5, 100);
let sketch = CountMinSketch::new(config);
```

## Error Bounds

The Count-Min Sketch guarantees that the estimated count is at most the true count + ε * N with probability 1 - δ, where N is the total count and ε, δ are the error parameters.

## License

MIT
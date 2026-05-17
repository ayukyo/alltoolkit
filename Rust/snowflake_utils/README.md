# Snowflake Utils

Twitter Snowflake-like distributed unique ID generator for Rust.

## Features

- **Zero external dependencies** - Pure Rust implementation
- **Thread-safe** - Atomic operations for concurrent ID generation
- **Distributed** - Supports up to 1024 nodes
- **High throughput** - Up to 4096 IDs per millisecond per node
- **64-bit IDs** - Compact and sortable by time
- **Clock drift handling** - Graceful handling of clock movement

## ID Structure

```
| 1 bit |    41 bits     |  10 bits  |    12 bits    |
| sign  |   timestamp   |  node_id  |  sequence_id  |
```

- **Sign bit**: Always 0 (positive ID)
- **Timestamp**: Milliseconds since custom epoch (default: 2024-01-01)
- **Node ID**: 0-1023 (supports 1024 nodes)
- **Sequence ID**: 0-4095 (4096 IDs per millisecond per node)

## Installation

Add to your `Cargo.toml`:

```toml
[dependencies]
snowflake_utils = { path = "./snowflake_utils" }
```

## Usage

### Basic Usage

```rust
use snowflake_utils::{SnowflakeGenerator, DEFAULT_EPOCH};

// Create generator with node ID 1
let generator = SnowflakeGenerator::new(1, DEFAULT_EPOCH);

// Generate a unique ID
let id = generator.generate();
println!("Generated ID: {}", id);
```

### Parse ID Components

```rust
use snowflake_utils::{SnowflakeGenerator, DEFAULT_EPOCH};

let generator = SnowflakeGenerator::new(1, DEFAULT_EPOCH);
let id = generator.generate();

// Parse ID into components
let (timestamp_ms, node_id, sequence) = generator.parse_id(id);
println!("Timestamp: {} ms since epoch", timestamp_ms);
println!("Node ID: {}", node_id);
println!("Sequence: {}", sequence);
```

### Using SnowflakeId Helper

```rust
use snowflake_utils::{SnowflakeId, DEFAULT_EPOCH};

let sf = SnowflakeId::new(1234567890123456);

println!("ID: {}", sf);
println!("Hex: {}", sf.to_hex());
println!("Node ID: {}", sf.node_id_component());
println!("Sequence: {}", sf.sequence_component());

// Parse with epoch
let parsed = sf.parse_with_epoch(DEFAULT_EPOCH);
println!("Timestamp (ms): {}", parsed.timestamp_ms);
```

### Batch Generation

```rust
use snowflake_utils::{SnowflakeGenerator, DEFAULT_EPOCH};

let generator = SnowflakeGenerator::new(1, DEFAULT_EPOCH);

// Generate 100 IDs
let ids = generator.generate_batch(100);
println!("Generated {} IDs", ids.len());
```

### Distributed System

```rust
use snowflake_utils::{SnowflakeGenerator, DEFAULT_EPOCH};

// Each server gets a unique node ID
let server1 = SnowflakeGenerator::new(1, DEFAULT_EPOCH);
let server2 = SnowflakeGenerator::new(2, DEFAULT_EPOCH);
let server3 = SnowflakeGenerator::new(3, DEFAULT_EPOCH);

// IDs from different servers are guaranteed unique
let id1 = server1.generate();
let id2 = server2.generate();
let id3 = server3.generate();
```

### Custom Epoch

```rust
use snowflake_utils::SnowflakeGenerator;

// Use a custom epoch (e.g., 2020-01-01)
let custom_epoch = 1577836800000i64; // 2020-01-01 00:00:00 UTC
let generator = SnowflakeGenerator::new(1, custom_epoch);
```

## API Reference

### `SnowflakeGenerator`

| Method | Description |
|--------|-------------|
| `new(node_id, epoch)` | Create generator with node ID and custom epoch |
| `with_node_id(node_id)` | Create generator with default epoch |
| `generate()` | Generate a unique 64-bit ID |
| `generate_batch(count)` | Generate multiple IDs |
| `parse_id(id)` | Parse ID into (timestamp, node_id, sequence) |
| `get_timestamp(id)` | Get timestamp from ID |
| `get_node_id(id)` | Get node ID from ID (static) |
| `get_sequence(id)` | Get sequence from ID (static) |
| `node_id()` | Get generator's node ID |
| `epoch()` | Get generator's epoch |

### `SnowflakeId`

| Method | Description |
|--------|-------------|
| `new(id)` | Create from raw ID |
| `from_string(s)` | Parse from string |
| `from_hex(hex)` | Parse from hex string |
| `id()` | Get raw ID |
| `to_string()` | Convert to string |
| `to_hex()` | Convert to hex string |
| `node_id_component()` | Get node ID |
| `sequence_component()` | Get sequence |
| `parse_with_epoch(epoch)` | Parse with epoch |

## Constants

```rust
pub const DEFAULT_EPOCH: i64 = 1704067200000; // 2024-01-01 00:00:00 UTC
pub const MAX_NODE_ID: u64 = 1023;            // Maximum node ID
pub const MAX_SEQUENCE: u64 = 4095;           // Maximum sequence number
```

## Thread Safety

`SnowflakeGenerator` is thread-safe and can be shared across threads:

```rust
use std::sync::Arc;
use std::thread;

let generator = Arc::new(SnowflakeGenerator::new(1, DEFAULT_EPOCH));

let handles: Vec<_> = (0..10)
    .map(|_| {
        let gen = Arc::clone(&generator);
        thread::spawn(move || gen.generate())
    })
    .collect();

for handle in handles {
    println!("ID: {}", handle.join().unwrap());
}
```

## License

MIT
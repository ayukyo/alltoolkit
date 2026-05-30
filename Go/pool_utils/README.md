# pool_utils

A generic object pool with TTL, lazy creation, and concurrency-safe operations.

## Features

- Generic object pool for any type
- TTL (Time-To-Live) support for pooled objects
- Lazy creation via factory function
- LRU eviction when pool is full
- Thread-safe operations (sync.Mutex)
- Zero external dependencies

## Installation

```bash
go get github.com/ayukyo/alltoolkit/Go/pool_utils
```

## Quick Start

```go
factory := func() interface{} { return &bytes.Buffer{} }
pool := pool_utils.New(factory, 100, 0)

obj := pool.Get()
buf := obj.(*bytes.Buffer)
buf.Reset()
buf.WriteString("hello")
pool.Put(obj)
```

## API Reference

### New(factory, maxSize, ttl)

Creates a new Pool.

- `factory`: Function to create new objects when needed
- `maxSize`: Maximum number of objects in the pool
- `ttl`: Time-to-live for pooled objects (0 = no expiration)

### Pool.Get()

Retrieves an object from the pool. Returns a new object from the factory if the pool is empty. If the pool is at max capacity, returns a new object without pooling it.

### Pool.Put(obj)

Returns an object to the pool for reuse. Thread-safe.

### Pool.Stats()

Returns `(available, active, created)` tuple:

- `available`: Number of objects in the pool ready for reuse
- `active`: Number of objects currently checked out
- `created`: Total number of objects ever created by the factory

### Pool.Close()

Clears all objects and resets pool statistics.

### Pool.Purge()

Removes all available objects that have exceeded their TTL. Should be called periodically for TTL-enabled pools.

### Pool.ResetStats()

Resets the created counter to zero.

## Example: bytes.Buffer Pool

```go
package main

import (
    "bytes"
    "fmt"
    "sync"

    "github.com/ayukyo/alltoolkit/Go/pool_utils"
)

func main() {
    factory := func() interface{} { return &bytes.Buffer{} }
    pool := pool_utils.New(factory, 100, 0)

    var wg sync.WaitGroup
    for i := 0; i < 50; i++ {
        wg.Add(1)
        go func() {
            defer wg.Done()
            obj := pool.Get()
            buf := obj.(*bytes.Buffer)
            buf.Reset()
            buf.WriteString("task")
            pool.Put(obj)
        }()
    }
    wg.Wait()

    fmt.Println(pool.Stats())
}
```

## Example: Pool with TTL

```go
package main

import (
    "bytes"
    "fmt"
    "time"

    "github.com/ayukyo/alltoolkit/Go/pool_utils"
)

func main() {
    // Objects expire after 100ms
    factory := func() interface{} { return &bytes.Buffer{} }
    pool := pool_utils.New(factory, 10, 100*time.Millisecond)

    obj := pool.Get()
    pool.Put(obj)

    // Wait for TTL to expire
    time.Sleep(150 * time.Millisecond)
    pool.Purge()

    fmt.Println(pool.Stats()) // 0 available
}
```

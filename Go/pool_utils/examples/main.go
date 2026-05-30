package main

import (
	"bytes"
	"fmt"
	"sync"
	"time"

	"github.com/ayukyo/alltoolkit/Go/pool_utils"
)

func main() {
	factory := func() interface{} { return &bytes.Buffer{} }

	// Example 1: Basic usage
	fmt.Println("=== Basic Pool Usage ===")
	pool := pool_utils.New(factory, 100, 0)
	obj := pool.Get()
	buf := obj.(*bytes.Buffer)
	buf.Reset()
	buf.WriteString("Hello, Object Pool!")
	fmt.Printf("Buffer content: %s\n", buf.String())
	pool.Put(obj)
	avail, active, created := pool.Stats()
	fmt.Printf("Pool stats: available=%d, active=%d, created=%d\n", avail, active, created)
	fmt.Println()

	// Example 2: Reusing objects
	fmt.Println("=== Object Reuse ===")
	pool2 := pool_utils.New(factory, 10, 0)
	for i := 0; i < 3; i++ {
		obj := pool2.Get()
		buf := obj.(*bytes.Buffer)
		buf.Reset()
		buf.WriteString(fmt.Sprintf("Iteration %d", i+1))
		fmt.Printf("  Get: %s (ptr=%p)\n", buf.String(), buf)
		pool2.Put(obj)
	}
	obj = pool2.Get()
	buf = obj.(*bytes.Buffer)
	fmt.Printf("  Reused buffer (ptr=%p)\n", buf)
	pool2.Put(obj)
	fmt.Println()

	// Example 3: Pool with TTL
	fmt.Println("=== Pool with TTL ===")
	pool3 := pool_utils.New(factory, 10, 100*time.Millisecond)
	obj = pool3.Get()
	buf = obj.(*bytes.Buffer)
	buf.WriteString("Short-lived object")
	pool3.Put(obj)
	fmt.Println("  Waiting for TTL to expire...")
	time.Sleep(150 * time.Millisecond)
	pool3.Purge()
	avail, _, _ = pool3.Stats()
	fmt.Printf("  After TTL purge: available=%d\n", avail)
	fmt.Println()

	// Example 4: Concurrent usage
	fmt.Println("=== Concurrent Usage ===")
	pool4 := pool_utils.New(factory, 50, 0)
	var wg sync.WaitGroup
	for i := 0; i < 20; i++ {
		wg.Add(1)
		go func(id int) {
			defer wg.Done()
			obj := pool4.Get()
			buf := obj.(*bytes.Buffer)
			buf.Reset()
			buf.WriteString(fmt.Sprintf("Goroutine %d", id))
			time.Sleep(10 * time.Millisecond)
			pool4.Put(obj)
		}(i)
	}
	wg.Wait()
	avail, active, created = pool4.Stats()
	fmt.Printf("  Final stats: available=%d, active=%d, created=%d\n", avail, active, created)
	fmt.Println()

	// Example 5: Closing pool
	fmt.Println("=== Close Pool ===")
	pool5 := pool_utils.New(factory, 10, 0)
	for i := 0; i < 5; i++ {
		obj := pool5.Get()
		pool5.Put(obj)
	}
	avail, _, _ = pool5.Stats()
	fmt.Printf("  Before close: available=%d, active=%d\n", avail, 0)
	pool5.Close()
	avail, _, _ = pool5.Stats()
	fmt.Printf("  After close: available=%d, active=%d\n", avail, 0)
}

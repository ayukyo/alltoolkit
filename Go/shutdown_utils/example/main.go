// Package main demonstrates the shutdown_utils package for graceful shutdown.
package main

import (
	"context"
	"fmt"
	"net/http"
	"time"

	"github.com/ayukyo/alltoolkit/Go/shutdown_utils"
)

func main() {
	// Create a new shutdown manager with custom timeout
	shutdownMgr := shutdown.New(
		shutdown.WithTimeout(15*time.Second),
	)

	// Register shutdown hooks with priorities (lower runs first)
	
	// Priority 10: Stop accepting new connections
	shutdownMgr.RegisterFunc("stop-accepting", func(ctx context.Context) error {
		fmt.Println("🛑 Stopping to accept new connections...")
		return nil
	}, shutdown.WithPriority(10))

	// Priority 20: Close database connections
	shutdownMgr.RegisterFunc("close-database", func(ctx context.Context) error {
		fmt.Println("📦 Closing database connections...")
		select {
		case <-time.After(500 * time.Millisecond):
			fmt.Println("✅ Database connections closed")
		case <-ctx.Done():
			fmt.Println("⚠️ Database close timed out")
		}
		return nil
	}, shutdown.WithPriority(20), shutdown.WithHookTimeout(2*time.Second))

	// Priority 30: Flush caches
	shutdownMgr.RegisterFunc("flush-cache", func(ctx context.Context) error {
		fmt.Println("💾 Flushing caches...")
		time.Sleep(200 * time.Millisecond)
		fmt.Println("✅ Caches flushed")
		return nil
	}, shutdown.WithPriority(30))

	// Priority 40: Close HTTP server
	server := &http.Server{Addr: ":8080"}
	shutdownMgr.RegisterFunc("close-http-server", func(ctx context.Context) error {
		fmt.Println("🌐 Closing HTTP server...")
		return server.Shutdown(ctx)
	}, shutdown.WithPriority(40))

	// Start listening for shutdown signals (SIGINT, SIGTERM)
	fmt.Println("🚀 Server starting on :8080")
	fmt.Println("Press Ctrl+C to trigger graceful shutdown")
	
	// Listen returns a channel that closes when shutdown begins
	shutdownChan := shutdownMgr.Listen()

	// Simulate an HTTP server
	go func() {
		http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
			fmt.Fprintf(w, "Hello! Server is running.\n")
		})
		if err := server.ListenAndServe(); err != http.ErrServerClosed {
			fmt.Printf("HTTP server error: %v\n", err)
		}
	}()

	// Wait for shutdown signal
	<-shutdownChan
	fmt.Println("\n📡 Shutdown initiated, running hooks...")

	// Wait for all hooks to complete
	shutdownMgr.WaitForShutdown()
	fmt.Println("👋 Goodbye!")
}

// Example output:
// 🚀 Server starting on :8080
// Press Ctrl+C to trigger graceful shutdown
// ^C
// 📡 Shutdown signal received
// Running shutdown hook: stop-accepting
// 🛑 Stopping to accept new connections...
// Running shutdown hook: close-database
// 📦 Closing database connections...
// ✅ Database connections closed
// Running shutdown hook: flush-cache
// 💾 Flushing caches...
// ✅ Caches flushed
// Running shutdown hook: close-http-server
// 🌐 Closing HTTP server...
// Shutdown completed in 752ms
// 👋 Goodbye!
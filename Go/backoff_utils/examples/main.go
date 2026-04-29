// Example usage of backoff_utils package
package main

import (
	"context"
	"errors"
	"fmt"
	"time"

	"github.com/ayukyo/alltoolkit/Go/backoff_utils"
)

func main() {
	fmt.Println("=== Backoff Utils Examples ===\n")

	// Example 1: Basic Exponential Backoff
	exampleBasicExponential()

	// Example 2: Linear Backoff
	exampleLinearBackoff()

	// Example 3: Constant Backoff
	exampleConstantBackoff()

	// Example 4: Full Jitter Backoff
	exampleFullJitterBackoff()

	// Example 5: Equal Jitter Backoff
	exampleEqualJitterBackoff()

	// Example 6: Decorrelated Jitter Backoff
	exampleDecorrelatedJitterBackoff()

	// Example 7: Using Retrier
	exampleRetrier()

	// Example 8: Retrier with Timeout
	exampleRetrierWithTimeout()

	// Example 9: Retrier with Result
	exampleRetrierWithResult()

	// Example 10: Retrier with Context Cancellation
	exampleContextCancellation()

	// Example 11: Custom Retryable Check
	exampleCustomRetryableCheck()

	// Example 12: Calculator Utilities
	exampleCalculator()
}

func exampleBasicExponential() {
	fmt.Println("--- Example 1: Basic Exponential Backoff ---")

	config := backoff_utils.Config{
		BaseDelay:  100 * time.Millisecond,
		MaxDelay:   10 * time.Second,
		Multiplier: 2.0,
	}

	backoff := backoff_utils.NewExponentialBackoff(config)

	fmt.Println("Delays for first 6 attempts:")
	for i := 0; i < 6; i++ {
		delay := backoff.Next(i)
		fmt.Printf("  Attempt %d: %v\n", i, delay)
	}
	fmt.Println()
}

func exampleLinearBackoff() {
	fmt.Println("--- Example 2: Linear Backoff ---")

	config := backoff_utils.Config{
		BaseDelay: 100 * time.Millisecond,
		MaxDelay:  500 * time.Millisecond,
	}

	backoff := backoff_utils.NewLinearBackoff(config)

	fmt.Println("Delays for first 6 attempts:")
	for i := 0; i < 6; i++ {
		delay := backoff.Next(i)
		fmt.Printf("  Attempt %d: %v\n", i, delay)
	}
	fmt.Println()
}

func exampleConstantBackoff() {
	fmt.Println("--- Example 3: Constant Backoff ---")

	backoff := backoff_utils.NewConstantBackoff(200 * time.Millisecond)

	fmt.Println("Delays for first 4 attempts:")
	for i := 0; i < 4; i++ {
		delay := backoff.Next(i)
		fmt.Printf("  Attempt %d: %v\n", i, delay)
	}
	fmt.Println()
}

func exampleFullJitterBackoff() {
	fmt.Println("--- Example 4: Full Jitter Backoff ---")

	config := backoff_utils.Config{
		BaseDelay:  100 * time.Millisecond,
		MaxDelay:   1 * time.Second,
		Multiplier: 2.0,
	}

	backoff := backoff_utils.NewFullJitterBackoff(config)

	fmt.Println("Delays for first 4 attempts (randomized):")
	for i := 0; i < 4; i++ {
		delay := backoff.Next(i)
		fmt.Printf("  Attempt %d: %v\n", i, delay)
	}
	fmt.Println()
}

func exampleEqualJitterBackoff() {
	fmt.Println("--- Example 5: Equal Jitter Backoff ---")

	config := backoff_utils.Config{
		BaseDelay:  100 * time.Millisecond,
		MaxDelay:   1 * time.Second,
		Multiplier: 2.0,
	}

	backoff := backoff_utils.NewEqualJitterBackoff(config)

	fmt.Println("Delays for first 4 attempts (randomized):")
	for i := 0; i < 4; i++ {
		delay := backoff.Next(i)
		fmt.Printf("  Attempt %d: %v\n", i, delay)
	}
	fmt.Println()
}

func exampleDecorrelatedJitterBackoff() {
	fmt.Println("--- Example 6: Decorrelated Jitter Backoff ---")

	config := backoff_utils.Config{
		BaseDelay:  100 * time.Millisecond,
		MaxDelay:   1 * time.Second,
		Multiplier: 2.0,
	}

	backoff := backoff_utils.NewDecorrelatedJitterBackoff(config)

	fmt.Println("Delays for first 4 attempts (randomized):")
	for i := 0; i < 4; i++ {
		delay := backoff.Next(i)
		fmt.Printf("  Attempt %d: %v\n", i, delay)
	}

	// Reset and try again
	backoff.Reset()
	fmt.Println("After reset:")
	delay := backoff.Next(0)
	fmt.Printf("  Attempt 0: %v\n", delay)
	fmt.Println()
}

func exampleRetrier() {
	fmt.Println("--- Example 7: Using Retrier ---")

	config := backoff_utils.Config{
		BaseDelay:  50 * time.Millisecond,
		MaxDelay:   200 * time.Millisecond,
		MaxRetries: 3,
	}

	backoff := backoff_utils.NewExponentialBackoff(config)
	retrier := backoff_utils.NewRetrier(backoff, config)

	attempts := 0
	err := retrier.Do(context.Background(), func() error {
		attempts++
		if attempts < 2 {
			fmt.Printf("  Attempt %d failed, retrying...\n", attempts)
			return errors.New("temporary error")
		}
		fmt.Printf("  Attempt %d succeeded!\n", attempts)
		return nil
	})

	if err != nil {
		fmt.Printf("  Failed after all retries: %v\n", err)
	} else {
		fmt.Printf("  Operation completed successfully\n")
	}
	fmt.Println()
}

func exampleRetrierWithTimeout() {
	fmt.Println("--- Example 8: Retrier with Timeout ---")

	config := backoff_utils.Config{
		BaseDelay:  100 * time.Millisecond,
		MaxDelay:   500 * time.Millisecond,
		MaxRetries: 10,
	}

	backoff := backoff_utils.NewExponentialBackoff(config)
	retrier := backoff_utils.NewRetrier(backoff, config)

	attempts := 0
	err := retrier.RetryWithTimeout(func() error {
		attempts++
		fmt.Printf("  Attempt %d\n", attempts)
		return errors.New("still failing")
	}, 300*time.Millisecond)

	if err != nil {
		fmt.Printf("  Operation timed out or failed: %v\n", err)
	}
	fmt.Println()
}

func exampleRetrierWithResult() {
	fmt.Println("--- Example 9: Retrier with Result ---")

	config := backoff_utils.Config{
		BaseDelay:  50 * time.Millisecond,
		MaxDelay:   200 * time.Millisecond,
		MaxRetries: 3,
	}

	backoff := backoff_utils.NewExponentialBackoff(config)

	attempts := 0
	result, err := backoff_utils.DoWithResult(context.Background(), backoff, config, func() (string, error) {
		attempts++
		if attempts < 2 {
			fmt.Printf("  Attempt %d failed, retrying...\n", attempts)
			return "", errors.New("temporary error")
		}
		fmt.Printf("  Attempt %d succeeded!\n", attempts)
		return "Hello, World!", nil
	})

	if err != nil {
		fmt.Printf("  Failed: %v\n", err)
	} else {
		fmt.Printf("  Result: %s\n", result)
	}
	fmt.Println()
}

func exampleContextCancellation() {
	fmt.Println("--- Example 10: Context Cancellation ---")

	config := backoff_utils.Config{
		BaseDelay:  100 * time.Millisecond,
		MaxDelay:   5 * time.Second,
		MaxRetries: 10,
	}

	backoff := backoff_utils.NewExponentialBackoff(config)
	retrier := backoff_utils.NewRetrier(backoff, config)

	ctx, cancel := context.WithTimeout(context.Background(), 250*time.Millisecond)
	defer cancel()

	attempts := 0
	err := retrier.Do(ctx, func() error {
		attempts++
		fmt.Printf("  Attempt %d\n", attempts)
		return errors.New("always fails")
	})

	var retryErr *backoff_utils.RetryError
	if errors.As(err, &retryErr) {
		if errors.Is(retryErr.Err, backoff_utils.ErrContextCanceled) {
			fmt.Printf("  Context was cancelled after %d attempts\n", retryErr.Attempt)
		}
	}
	fmt.Println()
}

func exampleCustomRetryableCheck() {
	fmt.Println("--- Example 11: Custom Retryable Check ---")

	config := backoff_utils.Config{
		BaseDelay:  50 * time.Millisecond,
		MaxDelay:   200 * time.Millisecond,
		MaxRetries: 5,
	}

	backoff := backoff_utils.NewExponentialBackoff(config)
	retrier := backoff_utils.NewRetrier(backoff, config)

	temporaryErr := errors.New("temporary error")
	permanentErr := errors.New("permanent error")

	isRetryable := func(err error) bool {
		return err == temporaryErr
	}

	// Test with non-retryable error
	attempts := 0
	err := retrier.DoWithRetryableCheck(context.Background(), func() error {
		attempts++
		fmt.Printf("  Attempt %d with permanent error\n", attempts)
		return permanentErr
	}, isRetryable, config.MaxRetries)

	if err != nil {
		fmt.Printf("  Non-retryable error encountered after %d attempts (expected 1)\n", attempts)
	}
	fmt.Println()
}

func exampleCalculator() {
	fmt.Println("--- Example 12: Calculator Utilities ---")

	calc := backoff_utils.BackoffCalculator{}

	// Calculate exponential backoff
	fmt.Println("Exponential backoff calculation:")
	for i := 0; i < 5; i++ {
		delay := calc.CalculateExponential(100*time.Millisecond, 2.0, i)
		fmt.Printf("  Attempt %d: %v\n", i, delay)
	}

	// Calculate linear backoff
	fmt.Println("\nLinear backoff calculation:")
	for i := 0; i < 5; i++ {
		delay := calc.CalculateLinear(100*time.Millisecond, i)
		fmt.Printf("  Attempt %d: %v\n", i, delay)
	}

	// Cap delay
	fmt.Println("\nCap delay examples:")
	fmt.Printf("  Cap 2s at 1s: %v\n", calc.CapDelay(2*time.Second, 1*time.Second))
	fmt.Printf("  Cap 500ms at 1s: %v\n", calc.CapDelay(500*time.Millisecond, 1*time.Second))

	// Add jitter
	fmt.Println("\nWith jitter (randomized):")
	for i := 0; i < 3; i++ {
		delay := calc.CalculateWithJitter(100*time.Millisecond, 0.5, nil)
		fmt.Printf("  Sample %d: %v\n", i+1, delay)
	}
	fmt.Println()
}
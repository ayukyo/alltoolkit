// Example usage of progressbar package
// Run with: go run example.go
package main

import (
	"fmt"
	"time"

	pb "github.com/ayukyo/alltoolkit/Go/progress_bar_utils"
)

func main() {
	fmt.Println("=== Progress Bar Examples ===")
	fmt.Println()

	// Example 1: Basic progress bar
	fmt.Println("1. Basic Progress Bar:")
	basicExample()

	// Example 2: Progress bar with speed and ETA
	fmt.Println("\n2. Progress Bar with Speed and ETA:")
	speedExample()

	// Example 3: Custom styled progress bar
	fmt.Println("\n3. Custom Styled Progress Bar:")
	customExample()

	// Example 4: Spinner example
	fmt.Println("\n4. Spinner Animation:")
	spinnerExample()

	// Example 5: Multi-bar example
	fmt.Println("\n5. Multi Progress Bars:")
	multiBarExample()

	// Example 6: Countdown example
	fmt.Println("\n6. Countdown Timer (3 seconds):")
	countdownExample()
}

func basicExample() {
	bar := pb.New(100)
	
	for i := 0; i <= 100; i++ {
		bar.Set(int64(i))
		bar.Render()
		time.Sleep(20 * time.Millisecond)
	}
	bar.Finish()
	fmt.Println("\nDone!")
}

func speedExample() {
	bar := pb.New(1000,
		pb.WithWidth(30),
		pb.WithSpeed(true),
		pb.WithETA(true),
		pb.WithPrefix("Downloading"),
	)

	for i := 0; i <= 1000; i++ {
		bar.Set(int64(i))
		bar.Render()
		time.Sleep(5 * time.Millisecond)
	}
	bar.Finish()
	fmt.Println("\nDownload complete!")
}

func customExample() {
	bar := pb.New(50,
		pb.WithWidth(20),
		pb.WithCompleteChar("▓"),
		pb.WithIncompleteChar("░"),
		pb.WithPrefix("Processing"),
		pb.WithSuffix("items"),
	)

	for i := 0; i <= 50; i++ {
		bar.Set(int64(i))
		bar.Render()
		time.Sleep(30 * time.Millisecond)
	}
	bar.Finish()
	fmt.Println("\nProcessing complete!")
}

func spinnerExample() {
	spinner := pb.NewSpinner(
		pb.WithSpinnerPrefix("Loading... "),
		pb.WithSpinnerSuffix(" Please wait"),
	)

	for i := 0; i < 30; i++ {
		spinner.Render()
		time.Sleep(100 * time.Millisecond)
		spinner.Next()
	}
	spinner.Clear()
	fmt.Println("\rLoading complete!          ")
}

func multiBarExample() {
	mb := pb.NewMultiBar()

	// Add three progress bars
	bar1 := mb.Add(100)
	bar2 := mb.Add(200)
	bar3 := mb.Add(150)

	// Initial render to print empty bars
	fmt.Println()
	fmt.Println()
	fmt.Println()
	mb.RenderAll()

	for i := 0; i < 100; i++ {
		bar1.Set(int64(i))
		bar2.Set(int64(i * 2))
		bar3.Set(int64(i * 3 / 2))
		mb.RenderAll()
		time.Sleep(50 * time.Millisecond)
	}

	bar1.Finish()
	bar2.Finish()
	bar3.Finish()
}

func countdownExample() {
	countdown := pb.NewCountdown(3 * time.Second,
		pb.WithCountdownPrefix("Starting in: "),
	)
	countdown.Start()
	fmt.Println("Countdown complete!")
}
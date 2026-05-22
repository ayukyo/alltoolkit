// Example demonstrates progress bar usage
package progress_bar_test

import (
	"fmt"
	"time"

	progress "github.com/ayukyo/alltoolkit/Go/progress_bar"
)

func ExampleNew() {
	// Basic progress bar
	pb := progress.New(100)
	for i := 0; i < 100; i++ {
		pb.Increment()
		time.Sleep(10 * time.Millisecond)
	}
	pb.Finish()
}

func ExampleNewWithConfig() {
	// Customized progress bar
	pb := progress.NewWithConfig(progress.Config{
		Total:           1000,
		Width:           50,
		Style:           progress.StyleArrow,
		Description:     "Downloading",
		ShowPercentage:  true,
		ShowCount:       true,
		ShowETA:         true,
		ShowSpeed:       true,
		ShowElapsedTime: false,
		ColorComplete:   progress.ColorGreen,
		ColorIncomplete: progress.ColorWhite,
	})

	for i := 0; i < 1000; i++ {
		pb.Increment()
		time.Sleep(2 * time.Millisecond)
	}
	pb.Finish()
}

func ExampleStatic() {
	// Static progress bar (no animation)
	fmt.Println(progress.Static(0, 100, 40, progress.StyleDefault))
	fmt.Println(progress.Static(25, 100, 40, progress.StyleClassic))
	fmt.Println(progress.Static(50, 100, 40, progress.StyleArrow))
	fmt.Println(progress.Static(75, 100, 40, progress.StyleBlocks))
	fmt.Println(progress.Static(100, 100, 40, progress.StyleDots))
}

func ExampleStaticPercentage() {
	// Static progress bar with percentage
	bar := progress.StaticPercentage(75, 100, 30, progress.StyleClassic)
	fmt.Println(bar) // [=======================> ] 75.0%
}

func ExampleStaticFull() {
	// Full static progress bar
	bar := progress.StaticFull(75, 100, 30, progress.StyleClassic, "Upload")
	fmt.Println(bar) // Upload: [=======================> ] 75.0% (75/100)
}

func ExampleNewMultiBar() {
	// Multiple progress bars
	mb := progress.NewMultiBar()
	bar1 := mb.AddBar(100, "Task 1:")
	bar2 := mb.AddBar(200, "Task 2:")
	bar3 := mb.AddBar(50, "Task 3:")

	// Simulate progress
	for i := 0; i < 100; i++ {
		if i < 100 {
			bar1.Increment()
		}
		if i < 200 {
			bar2.Increment()
		}
		if i < 50 {
			bar3.Increment()
		}
		mb.Render()
		time.Sleep(20 * time.Millisecond)
	}
}

func ExampleNewSpinner() {
	// Animated spinner
	spinner := progress.NewSpinner("Loading").
		SetSuffix("Processing files...").
		SetInterval(80 * time.Millisecond)

	spinner.Start()
	time.Sleep(2 * time.Second)
	spinner.Stop()
}

func ExampleIterate() {
	// Iterate over a slice with progress
	items := []string{"apple", "banana", "cherry", "date", "elderberry"}

	err := progress.Iterate(items, "Processing fruits", func(i int, item string) error {
		fmt.Printf("  Processing: %s\n", item)
		time.Sleep(100 * time.Millisecond)
		return nil
	})

	if err != nil {
		fmt.Println("Error:", err)
	}
}

func ExampleFormatBytes() {
	// Format bytes into human-readable format
	fmt.Println(progress.FormatBytes(0))          // 0 B
	fmt.Println(progress.FormatBytes(1023))       // 1023 B
	fmt.Println(progress.FormatBytes(1024))       // 1.00 KB
	fmt.Println(progress.FormatBytes(1048576))    // 1.00 MB
	fmt.Println(progress.FormatBytes(1073741824)) // 1.00 GB
	fmt.Println(progress.FormatBytes(1099511627776)) // 1.00 TB
}

func ExampleFormatNumber() {
	// Format numbers with thousands separator
	fmt.Println(progress.FormatNumber(1000))      // 1,000
	fmt.Println(progress.FormatNumber(10000))     // 10,000
	fmt.Println(progress.FormatNumber(1000000))    // 1,000,000
	fmt.Println(progress.FormatNumber(1234567890)) // 1,234,567,890
}

func ExampleCalculateProgress() {
	// Calculate progress percentage safely
	fmt.Printf("%.1f%%\n", progress.CalculateProgress(50, 100))  // 50.0%
	fmt.Printf("%.1f%%\n", progress.CalculateProgress(25, 50))   // 50.0%
	fmt.Printf("%.1f%%\n", progress.CalculateProgress(150, 100))  // 100.0% (capped)
	fmt.Printf("%.1f%%\n", progress.CalculateProgress(0, 100))    // 0.0%
}

func ExampleEstimateTime() {
	// Estimate remaining time
	elapsed := 30 * time.Second
	current := int64(300)
	total := int64(1000)

	eta := progress.EstimateTime(elapsed, current, total)
	fmt.Printf("Estimated time remaining: %v\n", eta)
}

func ExampleProgressBar_Describe() {
	// Update description dynamically
	pb := progress.New(100)
	pb.Describe("Phase 1: Initializing")

	for i := 0; i < 100; i++ {
		if i == 30 {
			pb.Describe("Phase 2: Processing")
		}
		if i == 70 {
			pb.Describe("Phase 3: Finalizing")
		}
		pb.Increment()
		time.Sleep(10 * time.Millisecond)
	}
	pb.Finish()
}

func ExampleProgressBar_Reset() {
	// Reset progress bar for reuse
	pb := progress.New(100)

	// First run
	for i := 0; i < 100; i++ {
		pb.Increment()
		time.Sleep(5 * time.Millisecond)
	}
	pb.Finish()

	fmt.Println("Starting second run...")

	// Reset and reuse
	pb.Reset()
	for i := 0; i < 100; i++ {
		pb.Increment()
		time.Sleep(5 * time.Millisecond)
	}
	pb.Finish()
}

func Example_allStyles() {
	// Available progress bar styles
	fmt.Println("Default:", progress.Static(50, 100, 20, progress.StyleDefault))
	fmt.Println("Classic:", progress.Static(50, 100, 20, progress.StyleClassic))
	fmt.Println("Arrow:", progress.Static(50, 100, 20, progress.StyleArrow))
	fmt.Println("Blocks:", progress.Static(50, 100, 20, progress.StyleBlocks))
	fmt.Println("Dots:", progress.Static(50, 100, 20, progress.StyleDots))
	fmt.Println("Pipe:", progress.Static(50, 100, 20, progress.StylePipe))
	fmt.Println("Minimal:", progress.Static(50, 100, 20, progress.StyleMinimal))
	fmt.Println("Circle:", progress.Static(50, 100, 20, progress.StyleCircle))
}

func Example_withColors() {
	// Progress bar with colors
	pb := progress.NewWithConfig(progress.Config{
		Total:           100,
		Width:           40,
		Style:           progress.StyleDefault,
		ColorComplete:   progress.ColorGreen,
		ColorIncomplete: progress.ColorYellow,
		ShowPercentage:  true,
	})

	for i := 0; i < 100; i++ {
		pb.Increment()
		time.Sleep(10 * time.Millisecond)
	}
	pb.Finish()
}

func ExampleProgressBar_Speed() {
	// Get processing speed
	pb := progress.New(1000)

	for i := 0; i < 1000; i++ {
		pb.Increment()
		if i%100 == 0 {
			fmt.Printf("Speed: %.0f items/s\n", pb.Speed())
		}
		time.Sleep(time.Millisecond)
	}
	pb.Finish()
}

func ExampleProgressBar_ETA() {
	// Get estimated time remaining
	pb := progress.New(1000)

	for i := 0; i < 1000; i++ {
		pb.Increment()
		if i%100 == 0 {
			fmt.Printf("ETA: %v\n", pb.ETA())
		}
		time.Sleep(2 * time.Millisecond)
	}
	pb.Finish()
}

func ExampleProgressBar_Elapsed() {
	// Track elapsed time
	pb := progress.NewWithConfig(progress.Config{
		Total:           100,
		ShowElapsedTime: true,
	})

	for i := 0; i < 100; i++ {
		pb.Increment()
		time.Sleep(10 * time.Millisecond)
	}
	pb.Finish()

	fmt.Printf("Total time: %v\n", pb.Elapsed())
}
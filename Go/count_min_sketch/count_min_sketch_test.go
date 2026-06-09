package count_min_sketch

import (
	"testing"
)

func TestConfigOptimal(t *testing.T) {
	config := Optimal(0.01, 0.01)
	if config.Depth < 1 || config.Width < 2 {
		t.Errorf("Config invalid: depth=%d, width=%d", config.Depth, config.Width)
	}
}

func TestNew(t *testing.T) {
	sketch := New(5, 100)
	if sketch.depth != 5 || sketch.width != 100 {
		t.Errorf("Expected depth=5, width=100, got depth=%d, width=%d", sketch.depth, sketch.width)
	}
}

func TestNewEnforcesMinimums(t *testing.T) {
	sketch := New(0, 1)
	if sketch.depth != 1 {
		t.Errorf("Depth should be at least 1, got %d", sketch.depth)
	}
	if sketch.width != 2 {
		t.Errorf("Width should be at least 2, got %d", sketch.width)
	}
}

func TestIncrement(t *testing.T) {
	sketch := New(5, 100)
	sketch.Increment("hello")
	sketch.Increment("hello")
	sketch.Increment("world")

	if sketch.Estimate("hello") < 2 {
		t.Errorf("Expected hello >= 2, got %d", sketch.Estimate("hello"))
	}
	if sketch.Estimate("world") < 1 {
		t.Errorf("Expected world >= 1, got %d", sketch.Estimate("world"))
	}
	if sketch.Estimate("missing") != 0 {
		t.Errorf("Expected missing = 0, got %d", sketch.Estimate("missing"))
	}
}

func TestUpdate(t *testing.T) {
	sketch := New(5, 100)
	sketch.Update("item", 5)

	if sketch.Estimate("item") < 5 {
		t.Errorf("Expected item >= 5, got %d", sketch.Estimate("item"))
	}
}

func TestTotalCount(t *testing.T) {
	sketch := New(5, 100)
	sketch.Increment("a")
	sketch.Update("b", 3)
	sketch.Increment("c")

	if sketch.TotalCount() != 5 {
		t.Errorf("Expected total=5, got %d", sketch.TotalCount())
	}
}

func TestMerge(t *testing.T) {
	sketch1 := New(5, 100)
	sketch2 := New(5, 100)

	sketch1.Increment("hello")
	sketch2.Increment("world")
	sketch2.Increment("world")

	err := sketch1.Merge(sketch2)
	if err != nil {
		t.Errorf("Merge failed: %v", err)
	}

	if sketch1.Estimate("hello") < 1 {
		t.Errorf("Expected hello >= 1, got %d", sketch1.Estimate("hello"))
	}
	if sketch1.Estimate("world") < 2 {
		t.Errorf("Expected world >= 2, got %d", sketch1.Estimate("world"))
	}
}

func TestMergeError(t *testing.T) {
	sketch1 := New(5, 100)
	sketch2 := New(5, 200)

	sketch1.Increment("test")

	err := sketch1.Merge(sketch2)
	if err == nil {
		t.Errorf("Expected error for dimension mismatch")
	}
}

func TestSerialization(t *testing.T) {
	sketch := WithRate(0.01, 0.01)
	sketch.Increment("apple")
	sketch.Increment("banana")
	sketch.Increment("apple")

	bytes := sketch.ToBytes()
	restored, err := FromBytes(bytes)
	if err != nil {
		t.Errorf("FromBytes failed: %v", err)
	}

	if restored.Estimate("apple") < 2 {
		t.Errorf("Expected apple >= 2, got %d", restored.Estimate("apple"))
	}
	if restored.Estimate("banana") < 1 {
		t.Errorf("Expected banana >= 1, got %d", restored.Estimate("banana"))
	}
}

func TestClear(t *testing.T) {
	sketch := New(5, 100)
	sketch.Increment("test")

	if sketch.Estimate("test") == 0 {
		t.Errorf("Expected test > 0 before clear")
	}

	sketch.Clear()
	if sketch.Estimate("test") != 0 {
		t.Errorf("Expected test = 0 after clear")
	}
	if sketch.TotalCount() != 0 {
		t.Errorf("Expected total = 0 after clear")
	}
}

func TestDimensions(t *testing.T) {
	sketch := New(7, 200)
	depth, width := sketch.Dimensions()
	if depth != 7 || width != 200 {
		t.Errorf("Expected (7,200), got (%d,%d)", depth, width)
	}
}

func TestWithRate(t *testing.T) {
	sketch := WithRate(0.01, 0.01)
	depth, width := sketch.Dimensions()
	if depth < 1 || width < 2 {
		t.Errorf("Invalid dimensions: depth=%d, width=%d", depth, width)
	}
}

func TestLargeCounts(t *testing.T) {
	sketch := New(5, 100)
	sketch.Update("frequent", 1000000)

	if sketch.Estimate("frequent") < 1000000 {
		t.Errorf("Expected frequent >= 1000000, got %d", sketch.Estimate("frequent"))
	}
	if sketch.TotalCount() != 1000000 {
		t.Errorf("Expected total = 1000000, got %d", sketch.TotalCount())
	}
}
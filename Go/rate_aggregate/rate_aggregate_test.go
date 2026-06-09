package rate_aggregate

import (
	"encoding/json"
	"math"
	"testing"
	"time"
)

func TestBasicRecordAndCount(t *testing.T) {
	agg := New(time.Minute * 5)
	agg.Record(100)
	agg.Record(200)
	agg.Record(150)
	if agg.Count() != 3 {
		t.Errorf("expected count 3, got %d", agg.Count())
	}
}

func TestRateCalculation(t *testing.T) {
	agg := New(time.Second * 60)
	for i := 0; i < 60; i++ {
		agg.Record(1.0)
		time.Sleep(time.Millisecond)
	}
	rate := agg.RatePerSecond()
	if rate < 0.9 || rate > 1.1 {
		t.Errorf("expected rate ~1.0, got %f", rate)
	}
}

func TestPercentileCalculation(t *testing.T) {
	agg := New(time.Minute * 5)
	for i := 1; i <= 100; i++ {
		agg.Record(float64(i))
	}
	p50 := agg.Percentile(0.50)
	p90 := agg.Percentile(0.90)
	p99 := agg.Percentile(0.99)
	if p50 < 49 || p50 > 51 {
		t.Errorf("expected p50 ~50, got %f", p50)
	}
	if p90 < 89 || p90 > 91 {
		t.Errorf("expected p90 ~90, got %f", p90)
	}
	if p99 < 98 || p99 > 100 {
		t.Errorf("expected p99 ~99, got %f", p99)
	}
}

func TestHitMissRatio(t *testing.T) {
	agg := New(time.Minute * 5)
	agg.RecordHit()
	agg.RecordHit()
	agg.RecordMiss()
	agg.RecordHit()
	if agg.TotalHits() != 3 {
		t.Errorf("expected 3 hits, got %d", agg.TotalHits())
	}
	if agg.TotalMisses() != 1 {
		t.Errorf("expected 1 miss, got %d", agg.TotalMisses())
	}
	ratio := agg.HitRatio()
	if math.Abs(ratio-0.75) > 0.01 {
		t.Errorf("expected hit ratio 0.75, got %f", ratio)
	}
}

func TestMeanCalculation(t *testing.T) {
	agg := New(time.Minute * 5)
	agg.Record(10)
	agg.Record(20)
	agg.Record(30)
	mean := agg.Mean()
	if math.Abs(mean-20.0) > 0.01 {
		t.Errorf("expected mean 20.0, got %f", mean)
	}
}

func TestSumCalculation(t *testing.T) {
	agg := New(time.Minute * 5)
	agg.Record(10)
	agg.Record(20)
	agg.Record(30)
	sum := agg.Sum()
	if math.Abs(sum-60.0) > 0.01 {
		t.Errorf("expected sum 60.0, got %f", sum)
	}
}

func TestMinMax(t *testing.T) {
	agg := New(time.Minute * 5)
	agg.Record(10)
	agg.Record(30)
	agg.Record(20)
	min := agg.Min()
	max := agg.Max()
	if min != 10 {
		t.Errorf("expected min 10, got %f", min)
	}
	if max != 30 {
		t.Errorf("expected max 30, got %f", max)
	}
}

func TestEmptyAggregator(t *testing.T) {
	agg := New(time.Minute * 5)
	if agg.Count() != 0 {
		t.Errorf("expected count 0, got %d", agg.Count())
	}
	if agg.Percentile(0.99) != 0 {
		t.Errorf("expected percentile 0, got %f", agg.Percentile(0.99))
	}
	if agg.Mean() != 0 {
		t.Errorf("expected mean 0, got %f", agg.Mean())
	}
	if agg.HitRatio() != 0 {
		t.Errorf("expected hit ratio 0, got %f", agg.HitRatio())
	}
}

func TestMetricsStruct(t *testing.T) {
	agg := New(time.Minute * 5)
	agg.Record(100)
	agg.Record(200)
	metrics := agg.Metrics()
	if metrics.Count != 2 {
		t.Errorf("expected count 2, got %d", metrics.Count)
	}
	if math.Abs(metrics.Mean-150.0) > 0.01 {
		t.Errorf("expected mean 150.0, got %f", metrics.Mean)
	}
}

func TestBuilder(t *testing.T) {
	agg := NewBuilder().
		WindowSize(time.Hour).
		BucketCount(200).
		Precision(4).
		Build()
	if agg.Count() != 0 {
		t.Errorf("expected count 0, got %d", agg.Count())
	}
	if agg.WindowSize() != time.Hour {
		t.Errorf("expected window size hour, got %v", agg.WindowSize())
	}
}

func TestClear(t *testing.T) {
	agg := New(time.Minute * 5)
	agg.Record(100)
	if agg.Count() != 1 {
		t.Errorf("expected count 1, got %d", agg.Count())
	}
	agg.Clear()
	if agg.Count() != 0 {
		t.Errorf("expected count 0 after clear, got %d", agg.Count())
	}
}

func TestSerialization(t *testing.T) {
	agg := New(time.Minute * 10)
	agg.Record(100)
	agg.RecordHit()

	metrics := agg.Metrics()
	data, err := json.Marshal(metrics)
	if err != nil {
		t.Errorf("failed to marshal metrics: %v", err)
	}

	var restored Metrics
	if err := json.Unmarshal(data, &restored); err != nil {
		t.Errorf("failed to unmarshal metrics: %v", err)
	}
	if restored.Count != 2 {
		t.Errorf("expected count 2, got %d", restored.Count)
	}
}

func TestP50P90P95P99(t *testing.T) {
	agg := New(time.Minute * 5)
	for i := 1; i <= 100; i++ {
		agg.Record(float64(i))
	}
	if agg.P50() < 49 || agg.P50() > 51 {
		t.Errorf("expected p50 ~50, got %f", agg.P50())
	}
	if agg.P90() < 89 || agg.P90() > 91 {
		t.Errorf("expected p90 ~90, got %f", agg.P90())
	}
	if agg.P95() < 94 || agg.P95() > 96 {
		t.Errorf("expected p95 ~95, got %f", agg.P95())
	}
	if agg.P99() < 98 || agg.P99() > 100 {
		t.Errorf("expected p99 ~99, got %f", agg.P99())
	}
}

func TestStdDev(t *testing.T) {
	agg := New(time.Minute * 5)
	agg.Record(10)
	agg.Record(20)
	agg.Record(30)
	stdDev := agg.StdDev()
	// StdDev of [10,20,30] = sqrt((100+0+100)/3) = sqrt(66.67) ≈ 8.16
	if math.Abs(stdDev-8.16) > 0.1 {
		t.Errorf("expected stddev ~8.16, got %f", stdDev)
	}
}

func TestResetCounters(t *testing.T) {
	agg := New(time.Minute * 5)
	agg.RecordHit()
	agg.RecordHit()
	if agg.TotalHits() != 2 {
		t.Errorf("expected 2 hits, got %d", agg.TotalHits())
	}
	agg.ResetCounters()
	if agg.TotalHits() != 0 {
		t.Errorf("expected 0 hits after reset, got %d", agg.TotalHits())
	}
	// Events should still be there
	if agg.Count() != 2 {
		t.Errorf("expected 2 events after reset, got %d", agg.Count())
	}
}

func TestRatePerMinuteAndHour(t *testing.T) {
	agg := New(time.Minute * 5)
	for i := 0; i < 300; i++ {
		agg.Record(1.0)
	}
	rateMin := agg.RatePerMinute()
	rateHr := agg.RatePerHour()
	// Rate should be approximately 60/min and 3600/hr
	if rateMin < 59 || rateMin > 61 {
		t.Errorf("expected rate/min ~60, got %f", rateMin)
	}
	if rateHr < 3599 || rateHr > 3601 {
		t.Errorf("expected rate/hr ~3600, got %f", rateHr)
	}
}

func TestMissRatio(t *testing.T) {
	agg := New(time.Minute * 5)
	agg.RecordHit()
	agg.RecordMiss()
	missRatio := agg.MissRatio()
	if math.Abs(missRatio-0.5) > 0.01 {
		t.Errorf("expected miss ratio 0.5, got %f", missRatio)
	}
}

func TestToJSON(t *testing.T) {
	agg := New(time.Minute * 5)
	agg.Record(100)
	metrics := agg.Metrics()
	jsonData, err := metrics.ToJSON()
	if err != nil {
		t.Errorf("ToJSON failed: %v", err)
	}
	if len(jsonData) == 0 {
		t.Error("expected non-empty JSON")
	}
}
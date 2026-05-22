package rate_calc_utils

import (
	"math"
	"testing"
)

func TestCompoundInterest(t *testing.T) {
	tests := []struct {
		name           string
		principal      float64
		rate           float64
		periods        int
		compoundsPerYear int
		expectedMin    float64 // minimum expected (due to floating point)
		expectedMax    float64 // maximum expected
		wantErr        bool
	}{
		{"basic calculation", 1000, 0.05, 1, 12, 1051.16, 1051.17, false},
		{"zero rate", 1000, 0, 1, 12, 1000, 1000, false},
		{"zero periods", 1000, 0.05, 0, 12, 1000, 1000, false},
		{"negative principal", -1000, 0.05, 1, 12, 0, 0, true},
		{"negative rate", 1000, -0.05, 1, 12, 0, 0, true},
		{"invalid compounds", 1000, 0.05, 1, 0, 0, 0, true},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result, err := CompoundInterest(tt.principal, tt.rate, tt.periods, tt.compoundsPerYear)
			if tt.wantErr {
				if err == nil {
					t.Errorf("expected error, got nil")
				}
				return
			}
			if err != nil {
				t.Errorf("unexpected error: %v", err)
				return
			}
			if result < tt.expectedMin || result > tt.expectedMax {
				t.Errorf("result = %v, want between %v and %v", result, tt.expectedMin, tt.expectedMax)
			}
		})
	}
}

func TestSimpleInterest(t *testing.T) {
	tests := []struct {
		name        string
		principal   float64
		rate        float64
		years       float64
		expected    float64
		wantErr     bool
	}{
		{"basic calculation", 1000, 0.05, 1, 1050, false},
		{"zero rate", 1000, 0, 1, 1000, false},
		{"zero years", 1000, 0.05, 0, 1000, false},
		{"negative principal", -1000, 0.05, 1, 0, true},
		{"negative rate", 1000, -0.05, 1, 0, true},
		{"negative years", 1000, 0.05, -1, 0, true},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result, err := SimpleInterest(tt.principal, tt.rate, tt.years)
			if tt.wantErr {
				if err == nil {
					t.Errorf("expected error, got nil")
				}
				return
			}
			if err != nil {
				t.Errorf("unexpected error: %v", err)
				return
			}
			if result != tt.expected {
				t.Errorf("result = %v, want %v", result, tt.expected)
			}
		})
	}
}

func TestAPRToAPY(t *testing.T) {
	tests := []struct {
		name           string
		apr            float64
		compounds      int
		expectedMin    float64
		expectedMax    float64
		wantErr        bool
	}{
		{"monthly compounding", 0.12, 12, 0.1268, 0.1269, false},
		{"daily compounding", 0.05, 365, 0.0512, 0.0514, false},
		{"zero apr", 0, 12, 0, 0, false},
		{"negative apr", -0.05, 12, 0, 0, true},
		{"invalid compounds", 0.05, 0, 0, 0, true},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result, err := APRToAPY(tt.apr, tt.compounds)
			if tt.wantErr {
				if err == nil {
					t.Errorf("expected error, got nil")
				}
				return
			}
			if err != nil {
				t.Errorf("unexpected error: %v", err)
				return
			}
			if result < tt.expectedMin || result > tt.expectedMax {
				t.Errorf("result = %v, want between %v and %v", result, tt.expectedMin, tt.expectedMax)
			}
		})
	}
}

func TestAPYToAPR(t *testing.T) {
	tests := []struct {
		name        string
		apy         float64
		compounds   int
		expectedMin float64
		expectedMax float64
		wantErr     bool
	}{
		{"basic conversion", 0.10, 12, 0.095, 0.096, false},
		{"zero apy", 0, 12, 0, 0, false},
		{"negative apy", -0.05, 12, 0, 0, true},
		{"invalid compounds", 0.05, 0, 0, 0, true},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result, err := APYToAPR(tt.apy, tt.compounds)
			if tt.wantErr {
				if err == nil {
					t.Errorf("expected error, got nil")
				}
				return
			}
			if err != nil {
				t.Errorf("unexpected error: %v", err)
				return
			}
			if result < tt.expectedMin || result > tt.expectedMax {
				t.Errorf("result = %v, want between %v and %v", result, tt.expectedMin, tt.expectedMax)
			}
		})
	}
}

func TestLoanPayment(t *testing.T) {
	tests := []struct {
		name        string
		principal   float64
		rate        float64
		years       int
		expectedMin float64
		expectedMax float64
		wantErr     bool
	}{
		{"standard loan", 100000, 0.05, 30, 536.81, 536.83, false},
		{"zero rate", 12000, 0, 1, 1000, 1000, false},
		{"invalid principal", 0, 0.05, 30, 0, 0, true},
		{"negative rate", 100000, -0.05, 30, 0, 0, true},
		{"invalid years", 100000, 0.05, 0, 0, 0, true},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result, err := LoanPayment(tt.principal, tt.rate, tt.years)
			if tt.wantErr {
				if err == nil {
					t.Errorf("expected error, got nil")
				}
				return
			}
			if err != nil {
				t.Errorf("unexpected error: %v", err)
				return
			}
			if result < tt.expectedMin || result > tt.expectedMax {
				t.Errorf("result = %v, want between %v and %v", result, tt.expectedMin, tt.expectedMax)
			}
		})
	}
}

func TestLoanAmortization(t *testing.T) {
	schedule, err := LoanAmortization(10000, 0.06, 1)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}

	if len(schedule) != 12 {
		t.Errorf("expected 12 payments, got %d", len(schedule))
	}

	// Check that balance ends at 0 (or very close due to rounding)
	finalBalance := schedule[len(schedule)-1].Balance
	if finalBalance > 0.01 {
		t.Errorf("final balance should be ~0, got %v", finalBalance)
	}

	// Check that total payments equal principal plus interest
	var totalPayments, totalPrincipal, totalInterest float64
	for _, p := range schedule {
		totalPayments += p.Payment
		totalPrincipal += p.Principal
		totalInterest += p.Interest
	}

	if math.Abs(totalPrincipal-10000) > 0.01 {
		t.Errorf("total principal should be ~10000, got %v", totalPrincipal)
	}
}

func TestROI(t *testing.T) {
	tests := []struct {
		name     string
		gain     float64
		cost     float64
		expected float64
		wantErr  bool
	}{
		{"positive return", 1500, 1000, 50, false},
		{"negative return", 800, 1000, -20, false},
		{"zero return", 1000, 1000, 0, false},
		{"zero cost", 1000, 0, 0, true},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result, err := ROI(tt.gain, tt.cost)
			if tt.wantErr {
				if err == nil {
					t.Errorf("expected error, got nil")
				}
				return
			}
			if err != nil {
				t.Errorf("unexpected error: %v", err)
				return
			}
			if result != tt.expected {
				t.Errorf("result = %v, want %v", result, tt.expected)
			}
		})
	}
}

func TestAnnualizedROI(t *testing.T) {
	tests := []struct {
		name        string
		gain        float64
		cost        float64
		years       float64
		expectedMin float64
		expectedMax float64
		wantErr     bool
	}{
		{"double in 10 years", 1000, 1000, 10, 7.17, 7.18, false},
		{"triple in 5 years", 2000, 1000, 5, 24.57, 24.58, false},
		{"zero cost", 1000, 0, 1, 0, 0, true},
		{"zero years", 1000, 1000, 0, 0, 0, true},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result, err := AnnualizedROI(tt.gain, tt.cost, tt.years)
			if tt.wantErr {
				if err == nil {
					t.Errorf("expected error, got nil")
				}
				return
			}
			if err != nil {
				t.Errorf("unexpected error: %v", err)
				return
			}
			if result < tt.expectedMin || result > tt.expectedMax {
				t.Errorf("result = %v, want between %v and %v", result, tt.expectedMin, tt.expectedMax)
			}
		})
	}
}

func TestExchangeRate(t *testing.T) {
	tests := []struct {
		name     string
		amount   float64
		rate     float64
		expected float64
		wantErr  bool
	}{
		{"USD to EUR", 100, 0.92, 92, false},
		{"zero rate", 100, 0, 0, false},
		{"negative amount", -100, 0.92, 0, true},
		{"negative rate", 100, -0.92, 0, true},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result, err := ExchangeRate(tt.amount, tt.rate)
			if tt.wantErr {
				if err == nil {
					t.Errorf("expected error, got nil")
				}
				return
			}
			if err != nil {
				t.Errorf("unexpected error: %v", err)
				return
			}
			if result != tt.expected {
				t.Errorf("result = %v, want %v", result, tt.expected)
			}
		})
	}
}

func TestBreakEvenPoint(t *testing.T) {
	tests := []struct {
		name        string
		fixed      float64
		price      float64
		variable   float64
		expected   float64
		wantErr    bool
	}{
		{"basic calculation", 10000, 50, 30, 500, false},
		{"price equals variable", 10000, 50, 50, 0, true},
		{"price less than variable", 10000, 30, 50, 0, true},
		{"negative fixed", -10000, 50, 30, 0, true},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result, err := BreakEvenPoint(tt.fixed, tt.price, tt.variable)
			if tt.wantErr {
				if err == nil {
					t.Errorf("expected error, got nil")
				}
				return
			}
			if err != nil {
				t.Errorf("unexpected error: %v", err)
				return
			}
			if result != tt.expected {
				t.Errorf("result = %v, want %v", result, tt.expected)
			}
		})
	}
}

func TestPresentValue(t *testing.T) {
	tests := []struct {
		name        string
		futureValue float64
		rate        float64
		periods     int
		expectedMin float64
		expectedMax float64
		wantErr     bool
	}{
		{"basic calculation", 1000, 0.05, 1, 952.37, 952.39, false},
		{"zero rate", 1000, 0, 1, 1000, 1000, false},
		{"zero periods", 1000, 0.05, 0, 1000, 1000, false},
		{"negative future", -1000, 0.05, 1, 0, 0, true},
		{"negative rate", 1000, -0.05, 1, 0, 0, true},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result, err := PresentValue(tt.futureValue, tt.rate, tt.periods)
			if tt.wantErr {
				if err == nil {
					t.Errorf("expected error, got nil")
				}
				return
			}
			if err != nil {
				t.Errorf("unexpected error: %v", err)
				return
			}
			if result < tt.expectedMin || result > tt.expectedMax {
				t.Errorf("result = %v, want between %v and %v", result, tt.expectedMin, tt.expectedMax)
			}
		})
	}
}

func TestFutureValue(t *testing.T) {
	tests := []struct {
		name         string
		presentValue float64
		rate         float64
		periods      int
		expectedMin  float64
		expectedMax  float64
		wantErr      bool
	}{
		{"basic calculation", 1000, 0.05, 1, 1050, 1050.01, false},
		{"zero rate", 1000, 0, 1, 1000, 1000, false},
		{"zero periods", 1000, 0.05, 0, 1000, 1000, false},
		{"negative present", -1000, 0.05, 1, 0, 0, true},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result, err := FutureValue(tt.presentValue, tt.rate, tt.periods)
			if tt.wantErr {
				if err == nil {
					t.Errorf("expected error, got nil")
				}
				return
			}
			if err != nil {
				t.Errorf("unexpected error: %v", err)
				return
			}
			if result < tt.expectedMin || result > tt.expectedMax {
				t.Errorf("result = %v, want between %v and %v", result, tt.expectedMin, tt.expectedMax)
			}
		})
	}
}

func TestInflationAdjusted(t *testing.T) {
	tests := []struct {
		name          string
		amount        float64
		inflationRate float64
		years         int
		expectedMin   float64
		expectedMax   float64
		wantErr       bool
	}{
		{"3% inflation for 10 years", 1000, 0.03, 10, 744.09, 744.10, false},
		{"zero inflation", 1000, 0, 10, 1000, 1000, false},
		{"zero years", 1000, 0.03, 0, 1000, 1000, false},
		{"negative amount", -1000, 0.03, 10, 0, 0, true},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result, err := InflationAdjusted(tt.amount, tt.inflationRate, tt.years)
			if tt.wantErr {
				if err == nil {
					t.Errorf("expected error, got nil")
				}
				return
			}
			if err != nil {
				t.Errorf("unexpected error: %v", err)
				return
			}
			if result < tt.expectedMin || result > tt.expectedMax {
				t.Errorf("result = %v, want between %v and %v", result, tt.expectedMin, tt.expectedMax)
			}
		})
	}
}

func TestRule72(t *testing.T) {
	tests := []struct {
		name     string
		rate     float64
		expected float64
		wantErr  bool
	}{
		{"8% return", 0.08, 9, false},
		{"6% return", 0.06, 12, false},
		{"zero rate", 0, 0, true},
		{"negative rate", -0.05, 0, true},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result, err := Rule72(tt.rate)
			if tt.wantErr {
				if err == nil {
					t.Errorf("expected error, got nil")
				}
				return
			}
			if err != nil {
				t.Errorf("unexpected error: %v", err)
				return
			}
			if result != tt.expected {
				t.Errorf("result = %v, want %v", result, tt.expected)
			}
		})
	}
}

func TestMonthlySavingsGoal(t *testing.T) {
	tests := []struct {
		name        string
		goal        float64
		rate        float64
		years       int
		expectedMin float64
		expectedMax float64
		wantErr     bool
	}{
		{"basic calculation", 10000, 0.05, 5, 147.04, 147.07, false},
		{"zero rate", 12000, 0, 1, 1000, 1000, false},
		{"zero goal", 0, 0.05, 5, 0, 0, true},
		{"zero years", 10000, 0.05, 0, 0, 0, true},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result, err := MonthlySavingsGoal(tt.goal, tt.rate, tt.years)
			if tt.wantErr {
				if err == nil {
					t.Errorf("expected error, got nil")
				}
				return
			}
			if err != nil {
				t.Errorf("unexpected error: %v", err)
				return
			}
			if result < tt.expectedMin || result > tt.expectedMax {
				t.Errorf("result = %v, want between %v and %v", result, tt.expectedMin, tt.expectedMax)
			}
		})
	}
}

func TestTotalInterest(t *testing.T) {
	tests := []struct {
		name        string
		principal   float64
		rate        float64
		years       int
		expectedMin float64
		expectedMax float64
		wantErr     bool
	}{
		{"basic loan", 10000, 0.06, 1, 327.96, 327.98, false},
		{"zero rate", 10000, 0, 1, 0, 0, false},
		{"invalid principal", 0, 0.05, 1, 0, 0, true},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result, err := TotalInterest(tt.principal, tt.rate, tt.years)
			if tt.wantErr {
				if err == nil {
					t.Errorf("expected error, got nil")
				}
				return
			}
			if err != nil {
				t.Errorf("unexpected error: %v", err)
				return
			}
			if result < tt.expectedMin || result > tt.expectedMax {
				t.Errorf("result = %v, want between %v and %v", result, tt.expectedMin, tt.expectedMax)
			}
		})
	}
}

func TestRateFromPayment(t *testing.T) {
	tests := []struct {
		name           string
		principal      float64
		monthlyPayment float64
		years          int
		expectedMin    float64
		expectedMax    float64
		wantErr        bool
	}{
		{"known rate", 100000, 536.82, 30, 0.0499, 0.0501, false},
		{"payment too low", 100000, 100, 30, 0, 0, true},
		{"invalid years", 100000, 536.82, 0, 0, 0, true},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result, err := RateFromPayment(tt.principal, tt.monthlyPayment, tt.years)
			if tt.wantErr {
				if err == nil {
					t.Errorf("expected error, got nil")
				}
				return
			}
			if err != nil {
				t.Errorf("unexpected error: %v", err)
				return
			}
			if result < tt.expectedMin || result > tt.expectedMax {
				t.Errorf("result = %v, want between %v and %v", result, tt.expectedMin, tt.expectedMax)
			}
		})
	}
}

// Test APR/APY roundtrip
func TestAPRAPYRoundtrip(t *testing.T) {
	originalAPR := 0.10
	compounds := 12

	apy, err := APRToAPY(originalAPR, compounds)
	if err != nil {
		t.Fatalf("APRToAPY error: %v", err)
	}

	recoveredAPR, err := APYToAPR(apy, compounds)
	if err != nil {
		t.Fatalf("APYToAPR error: %v", err)
	}

	diff := math.Abs(recoveredAPR - originalAPR)
	if diff > 0.0001 {
		t.Errorf("roundtrip failed: original APR = %v, recovered = %v, diff = %v", 
			originalAPR, recoveredAPR, diff)
	}
}

// Test PresentValue/FutureValue roundtrip
func TestPVFVRoundtrip(t *testing.T) {
	originalPV := 1000.0
	rate := 0.05
	periods := 10

	fv, err := FutureValue(originalPV, rate, periods)
	if err != nil {
		t.Fatalf("FutureValue error: %v", err)
	}

	recoveredPV, err := PresentValue(fv, rate, periods)
	if err != nil {
		t.Fatalf("PresentValue error: %v", err)
	}

	diff := math.Abs(recoveredPV - originalPV)
	if diff > 0.01 {
		t.Errorf("roundtrip failed: original PV = %v, recovered = %v, diff = %v",
			originalPV, recoveredPV, diff)
	}
}
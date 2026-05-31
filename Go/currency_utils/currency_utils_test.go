package currency_utils

import (
	"fmt"
	"testing"
)

func TestGetCurrency(t *testing.T) {
	tests := []struct {
		code     Code
		wantName string
		wantSym  string
		wantDec  int
	}{
		{"USD", "US Dollar", "$", 2},
		{"EUR", "Euro", "€", 2},
		{"JPY", "Japanese Yen", "¥", 0},
		{"CNY", "Chinese Yuan", "¥", 2},
		{"GBP", "British Pound", "£", 2},
	}

	for _, tt := range tests {
		t.Run(string(tt.code), func(t *testing.T) {
			c, err := GetCurrency(tt.code)
			if err != nil {
				t.Fatalf("GetCurrency(%s) error: %v", tt.code, err)
			}
			if c.Name != tt.wantName {
				t.Errorf("Name = %s, want %s", c.Name, tt.wantName)
			}
			if c.Symbol != tt.wantSym {
				t.Errorf("Symbol = %s, want %s", c.Symbol, tt.wantSym)
			}
			if c.Decimals != tt.wantDec {
				t.Errorf("Decimals = %d, want %d", c.Decimals, tt.wantDec)
			}
		})
	}
}

func TestGetCurrencyInvalid(t *testing.T) {
	_, err := GetCurrency("XXX")
	if err == nil {
		t.Error("expected error for invalid currency code")
	}
}

func TestIsValid(t *testing.T) {
	if !IsValid("USD") {
		t.Error("USD should be valid")
	}
	if IsValid("XXX") {
		t.Error("XXX should be invalid")
	}
}

func TestListCurrencies(t *testing.T) {
	codes := ListCurrencies()
	if len(codes) < 20 {
		t.Errorf("expected at least 20 currencies, got %d", len(codes))
	}
	found := false
	for _, c := range codes {
		if c == "USD" {
			found = true
			break
		}
	}
	if !found {
		t.Error("USD not found in currency list")
	}
}

func TestFormat(t *testing.T) {
	tests := []struct {
		amount   float64
		code     Code
		expected string
	}{
		{1234.56, "USD", "$1,234.56"},
		{0.99, "USD", "$0.99"},
		{1000000, "USD", "$1,000,000.00"},
		{1234.56, "EUR", "1,234.56 €"},
		{1234, "JPY", "¥1,234"},
		{1234.56, "CNY", "¥1,234.56"},
	}

	for _, tt := range tests {
		t.Run(string(tt.code), func(t *testing.T) {
			result, err := Format(tt.amount, tt.code)
			if err != nil {
				t.Fatalf("Format error: %v", err)
			}
			if result != tt.expected {
				t.Errorf("Format(%v, %s) = %q, want %q", tt.amount, tt.code, result, tt.expected)
			}
		})
	}
}

func TestFormatNegative(t *testing.T) {
	result, err := Format(-1234.56, "USD")
	if err != nil {
		t.Fatalf("Format error: %v", err)
	}
	if result != "-$1,234.56" {
		t.Errorf("negative format = %q, want %q", result, "-$1,234.56")
	}
}

func TestFormatCompact(t *testing.T) {
	tests := []struct {
		amount   float64
		code     Code
		expected string
	}{
		{1500, "USD", "$1.50K USD"},
		{1500000, "USD", "$1.50M USD"},
		{1500000000, "USD", "$1.50B USD"},
		{1500000000000, "USD", "$1.50T USD"},
		{1234, "JPY", "¥1.23K JPY"},
	}

	for _, tt := range tests {
		t.Run(fmt.Sprintf("%v_%s", tt.amount, tt.code), func(t *testing.T) {
			result, err := FormatCompact(tt.amount, tt.code)
			if err != nil {
				t.Fatalf("FormatCompact error: %v", err)
			}
			if result != tt.expected {
				t.Errorf("FormatCompact(%v, %s) = %q, want %q", tt.amount, tt.code, result, tt.expected)
			}
		})
	}
}

func TestFormatCode(t *testing.T) {
	result, err := FormatCode(1234.56, "USD")
	if err != nil {
		t.Fatalf("FormatCode error: %v", err)
	}
	if result != "1,234.56 USD" {
		t.Errorf("FormatCode = %q, want %q", result, "1,234.56 USD")
	}
}

func TestFormatWithOptions(t *testing.T) {
	opts := FormatOptions{
		Symbol:         "USD",
		ShowSymbol:     true,
		ShowCode:       false,
		ThousandsSep:   ".",
		DecimalSep:     ",",
		DecimalPlaces:  2,
		SymbolPos:      SymbolSuffix,
		NegativeParens: true,
	}
	result, err := FormatWithOptions(-1234.56, "USD", opts)
	if err != nil {
		t.Fatalf("FormatWithOptions error: %v", err)
	}
	if result != "(1.234,56 USD)" {
		t.Errorf("FormatWithOptions = %q, want %q", result, "(1.234,56 USD)")
	}
}

func TestParse(t *testing.T) {
	tests := []struct {
		input    string
		expected *Money
	}{
		{"$1,234.56", &Money{1234.56, "USD"}},
		{"1,234.56 USD", &Money{1234.56, "USD"}},
		{"USD 1234.56", &Money{1234.56, "USD"}},
		{"CNY 1234.56", &Money{1234.56, "CNY"}},
		{"£1,234.56", &Money{1234.56, "GBP"}},
	}

	for _, tt := range tests {
		t.Run(tt.input, func(t *testing.T) {
			result, err := Parse(tt.input)
			if err != nil {
				t.Fatalf("Parse(%q) error: %v", tt.input, err)
			}
			if result.Amount != tt.expected.Amount {
				t.Errorf("Amount = %v, want %v", result.Amount, tt.expected.Amount)
			}
			if result.Currency != tt.expected.Currency {
				t.Errorf("Currency = %s, want %s", result.Currency, tt.expected.Currency)
			}
		})
	}
}

func TestParseInvalid(t *testing.T) {
	_, err := Parse("")
	if err == nil {
		t.Error("expected error for empty string")
	}
}

func TestParseAmount(t *testing.T) {
	tests := []struct {
		input    string
		expected float64
	}{
		{"1,234.56", 1234.56},
		{"1000", 1000},
	}

	for _, tt := range tests {
		t.Run(tt.input, func(t *testing.T) {
			result, err := ParseAmount(tt.input)
			if err != nil {
				t.Fatalf("ParseAmount(%q) error: %v", tt.input, err)
			}
			if absDiff(result, tt.expected) > 0.001 {
				t.Errorf("ParseAmount(%q) = %v, want %v", tt.input, result, tt.expected)
			}
		})
	}
}

func TestConvert(t *testing.T) {
	// 100 USD to EUR (rate ~1.08)
	money := Money{Amount: 100, Currency: "USD"}
	result, err := Convert(money, "EUR")
	if err != nil {
		t.Fatalf("Convert error: %v", err)
	}
	if result.Currency != "EUR" {
		t.Errorf("Currency = %s, want EUR", result.Currency)
	}
	if result.Amount <= 0 || result.Amount > 200 {
		t.Errorf("Amount = %v, seems incorrect", result.Amount)
	}
}

func TestConvertSame(t *testing.T) {
	money := Money{Amount: 100, Currency: "USD"}
	result, err := Convert(money, "USD")
	if err != nil {
		t.Fatalf("Convert error: %v", err)
	}
	if result.Amount != 100 {
		t.Errorf("Amount = %v, want 100", result.Amount)
	}
}

func TestConvertInvalid(t *testing.T) {
	money := Money{Amount: 100, Currency: "USD"}
	_, err := Convert(money, "XXX")
	if err == nil {
		t.Error("expected error for invalid target currency")
	}
}

func TestGetExchangeRate(t *testing.T) {
	rate, err := GetExchangeRate("USD", "EUR")
	if err != nil {
		t.Fatalf("GetExchangeRate error: %v", err)
	}
	if rate <= 0 {
		t.Errorf("Rate = %v, should be positive", rate)
	}
}

func TestAdd(t *testing.T) {
	m1 := Money{Amount: 100, Currency: "USD"}
	m2 := Money{Amount: 50, Currency: "USD"}
	result, err := Add(m1, m2)
	if err != nil {
		t.Fatalf("Add error: %v", err)
	}
	if result.Amount != 150 {
		t.Errorf("Add = %v, want 150", result.Amount)
	}
}

func TestAddDifferentCurrency(t *testing.T) {
	m1 := Money{Amount: 100, Currency: "USD"}
	m2 := Money{Amount: 50, Currency: "EUR"}
	result, err := Add(m1, m2)
	if err != nil {
		t.Fatalf("Add error: %v", err)
	}
	if result.Currency != "USD" {
		t.Errorf("Currency = %s, want USD", result.Currency)
	}
}

func TestSubtract(t *testing.T) {
	m1 := Money{Amount: 100, Currency: "USD"}
	m2 := Money{Amount: 30, Currency: "USD"}
	result, err := Subtract(m1, m2)
	if err != nil {
		t.Fatalf("Subtract error: %v", err)
	}
	if result.Amount != 70 {
		t.Errorf("Subtract = %v, want 70", result.Amount)
	}
}

func TestMultiply(t *testing.T) {
	m := Money{Amount: 100, Currency: "USD"}
	result := Multiply(m, 1.5)
	if result.Amount != 150 {
		t.Errorf("Multiply = %v, want 150", result.Amount)
	}
}

func TestDivide(t *testing.T) {
	m := Money{Amount: 100, Currency: "USD"}
	result, err := Divide(m, 4)
	if err != nil {
		t.Fatalf("Divide error: %v", err)
	}
	if absDiff(result.Amount, 25) > 0.001 {
		t.Errorf("Divide = %v, want 25", result.Amount)
	}
}

func TestDivideByZero(t *testing.T) {
	m := Money{Amount: 100, Currency: "USD"}
	_, err := Divide(m, 0)
	if err == nil {
		t.Error("expected error for divide by zero")
	}
}

func TestAllocate(t *testing.T) {
	m := Money{Amount: 100, Currency: "USD"}
	result, err := Allocate(m, 3)
	if err != nil {
		t.Fatalf("Allocate error: %v", err)
	}
	if len(result) != 3 {
		t.Errorf("length = %d, want 3", len(result))
	}
	total := 0.0
	for _, r := range result {
		total += r.Amount
	}
	if absDiff(total, 100) > 0.001 {
		t.Errorf("total = %v, want 100", total)
	}
}

func TestSplitRatio(t *testing.T) {
	result, err := SplitRatio(100, "USD", []int{1, 2, 3})
	if err != nil {
		t.Fatalf("SplitRatio error: %v", err)
	}
	if len(result) != 3 {
		t.Errorf("length = %d, want 3", len(result))
	}
	// 1+2+3=6, so 100*(1/6), 100*(2/6), 100*(3/6)
	if absDiff(result[0].Amount, 100/6.0) > 0.001 {
		t.Errorf("result[0] = %v, want %v", result[0].Amount, 100/6.0)
	}
	if absDiff(result[1].Amount, 200/6.0) > 0.001 {
		t.Errorf("result[1] = %v, want %v", result[1].Amount, 200/6.0)
	}
	if absDiff(result[2].Amount, 300/6.0) > 0.001 {
		t.Errorf("result[2] = %v, want %v", result[2].Amount, 300/6.0)
	}
}

func TestRound(t *testing.T) {
	tests := []struct {
		amount   float64
		code     Code
		decimals int
		expected float64
	}{
		{1.234, "USD", 2, 1.23},
		{1.235, "USD", 2, 1.24},
		{1.234, "JPY", 0, 1},
	}

	for _, tt := range tests {
		t.Run(string(tt.code), func(t *testing.T) {
			result := Round(tt.amount, tt.code)
			if absDiff(result, tt.expected) > 0.001 {
				t.Errorf("Round(%v, %s) = %v, want %v", tt.amount, tt.code, result, tt.expected)
			}
		})
	}
}

func TestFloor(t *testing.T) {
	if Floor(1.9) != 1 {
		t.Errorf("Floor(1.9) = %v, want 1", Floor(1.9))
	}
}

func TestCeil(t *testing.T) {
	if Ceil(1.1) != 2 {
		t.Errorf("Ceil(1.1) = %v, want 2", Ceil(1.1))
	}
}

func TestAbs(t *testing.T) {
	if Abs(-5) != 5 || Abs(5) != 5 {
		t.Error("Abs incorrect")
	}
}

func TestIsZero(t *testing.T) {
	if !IsZero(0) || IsZero(0.001) {
		t.Error("IsZero incorrect")
	}
}

func TestCompare(t *testing.T) {
	m1 := Money{Amount: 100, Currency: "USD"}
	m2 := Money{Amount: 200, Currency: "USD"}

	cmp, err := Compare(m1, m2)
	if err != nil {
		t.Fatalf("Compare error: %v", err)
	}
	if cmp != -1 {
		t.Errorf("Compare = %d, want -1", cmp)
	}

	cmp, _ = Compare(m2, m1)
	if cmp != 1 {
		t.Errorf("Compare = %d, want 1", cmp)
	}

	cmp, _ = Compare(m1, m1)
	if cmp != 0 {
		t.Errorf("Compare = %d, want 0", cmp)
	}
}

func TestMin(t *testing.T) {
	m1 := Money{Amount: 100, Currency: "USD"}
	m2 := Money{Amount: 200, Currency: "USD"}
	result, err := Min(m1, m2)
	if err != nil {
		t.Fatalf("Min error: %v", err)
	}
	if result.Amount != 100 {
		t.Errorf("Min = %v, want 100", result.Amount)
	}
}

func TestMax(t *testing.T) {
	m1 := Money{Amount: 100, Currency: "USD"}
	m2 := Money{Amount: 200, Currency: "USD"}
	result, err := Max(m1, m2)
	if err != nil {
		t.Fatalf("Max error: %v", err)
	}
	if result.Amount != 200 {
		t.Errorf("Max = %v, want 200", result.Amount)
	}
}

func TestClamp(t *testing.T) {
	min := Money{Amount: 50, Currency: "USD"}
	max := Money{Amount: 150, Currency: "USD"}
	m := Money{Amount: 200, Currency: "USD"}

	result, err := Clamp(m, min, max)
	if err != nil {
		t.Fatalf("Clamp error: %v", err)
	}
	if result.Amount != 150 {
		t.Errorf("Clamp = %v, want 150", result.Amount)
	}
}

func TestToWords(t *testing.T) {
	result, err := ToWords(1234.56, "USD")
	if err != nil {
		t.Fatalf("ToWords error: %v", err)
	}
	if result == "" {
		t.Error("ToWords returned empty string")
	}
}

func TestToWordsLong(t *testing.T) {
	result, err := ToWordsLong(1234.56, "USD")
	if err != nil {
		t.Fatalf("ToWordsLong error: %v", err)
	}
	if result == "" {
		t.Error("ToWordsLong returned empty string")
	}
}

func TestIntToWords(t *testing.T) {
	tests := []struct {
		input    int64
		expected string
	}{
		{0, "zero"},
		{1, "one"},
		{10, "ten"},
		{11, "eleven"},
		{20, "twenty"},
		{21, "twenty one"},
		{100, "one hundred"},
		{1000, "one thousand"},
		{123456789, "one hundred twenty three million four hundred fifty six thousand seven hundred eighty nine"},
	}

	for _, tt := range tests {
		t.Run(tt.expected, func(t *testing.T) {
			result := intToWords(tt.input)
			if result != tt.expected {
				t.Errorf("intToWords(%d) = %q, want %q", tt.input, result, tt.expected)
			}
		})
	}
}

func TestAllCurrenciesFormat(t *testing.T) {
	for _, code := range ListCurrencies() {
		amount := 1234.56
		result, err := Format(amount, code)
		if err != nil {
			t.Errorf("Format(%v, %s) error: %v", amount, code, err)
			continue
		}
		if result == "" {
			t.Errorf("Format(%v, %s) returned empty string", amount, code)
		}
	}
}

func TestAllCurrenciesParseConvert(t *testing.T) {
	codes := ListCurrencies()
	for _, fromCode := range codes {
		for _, toCode := range codes {
			money := Money{Amount: 100, Currency: fromCode}
			result, err := Convert(money, toCode)
			if err != nil {
				t.Errorf("Convert(%v %s -> %s) error: %v", money.Amount, fromCode, toCode, err)
				continue
			}
			if result.Currency != toCode {
				t.Errorf("Convert resulted in currency %s, want %s", result.Currency, toCode)
			}
		}
	}
}


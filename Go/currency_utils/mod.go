// Package currency_utils provides comprehensive currency formatting and conversion utilities.
// Zero external dependencies - uses only Go standard library.
package currency_utils

import (
	"errors"
	"fmt"
	"regexp"
	"strconv"
	"strings"
)

// Currency code (ISO 4217)
type Code string

// Currency represents a currency with metadata
type Currency struct {
	Code      Code
	Name      string
	Symbol    string
	Decimals  int
	SymbolPos SymbolPosition // 0: prefix, 1: suffix
}

// SymbolPosition defines where the currency symbol appears
type SymbolPosition int

const (
	SymbolPrefix SymbolPosition = iota
	SymbolSuffix
)

// Common errors
var (
	ErrInvalidAmount   = errors.New("invalid amount")
	ErrInvalidCurrency = errors.New("invalid or unsupported currency")
	ErrParseFailed     = errors.New("failed to parse currency string")
	ErrZeroAmount      = errors.New("amount cannot be zero")
	ErrNegativeAmount  = errors.New("amount cannot be negative")
)

// Money represents a money value with currency
type Money struct {
	Amount  float64
	Currency Code
}

// =============================================================================
// Currency Definitions (20+ currencies)
// =============================================================================

var currencies = map[Code]Currency{
	"USD": {Code: "USD", Name: "US Dollar", Symbol: "$", Decimals: 2, SymbolPos: SymbolPrefix},
	"EUR": {Code: "EUR", Name: "Euro", Symbol: "€", Decimals: 2, SymbolPos: SymbolSuffix},
	"GBP": {Code: "GBP", Name: "British Pound", Symbol: "£", Decimals: 2, SymbolPos: SymbolPrefix},
	"JPY": {Code: "JPY", Name: "Japanese Yen", Symbol: "¥", Decimals: 0, SymbolPos: SymbolPrefix},
	"CNY": {Code: "CNY", Name: "Chinese Yuan", Symbol: "¥", Decimals: 2, SymbolPos: SymbolPrefix},
	"CAD": {Code: "CAD", Name: "Canadian Dollar", Symbol: "C$", Decimals: 2, SymbolPos: SymbolPrefix},
	"CHF": {Code: "CHF", Name: "Swiss Franc", Symbol: "Fr", Decimals: 2, SymbolPos: SymbolSuffix},
	"KRW": {Code: "KRW", Name: "South Korean Won", Symbol: "₩", Decimals: 0, SymbolPos: SymbolPrefix},
	"INR": {Code: "INR", Name: "Indian Rupee", Symbol: "₹", Decimals: 2, SymbolPos: SymbolPrefix},
	"AUD": {Code: "AUD", Name: "Australian Dollar", Symbol: "A$", Decimals: 2, SymbolPos: SymbolPrefix},
	"HKD": {Code: "HKD", Name: "Hong Kong Dollar", Symbol: "HK$", Decimals: 2, SymbolPos: SymbolPrefix},
	"SGD": {Code: "SGD", Name: "Singapore Dollar", Symbol: "S$", Decimals: 2, SymbolPos: SymbolPrefix},
	"NZD": {Code: "NZD", Name: "New Zealand Dollar", Symbol: "NZ$", Decimals: 2, SymbolPos: SymbolPrefix},
	"SEK": {Code: "SEK", Name: "Swedish Krona", Symbol: "kr", Decimals: 2, SymbolPos: SymbolSuffix},
	"NOK": {Code: "NOK", Name: "Norwegian Krone", Symbol: "kr", Decimals: 2, SymbolPos: SymbolSuffix},
	"DKK": {Code: "DKK", Name: "Danish Krone", Symbol: "kr", Decimals: 2, SymbolPos: SymbolSuffix},
	"MXN": {Code: "MXN", Name: "Mexican Peso", Symbol: "$", Decimals: 2, SymbolPos: SymbolPrefix},
	"BRL": {Code: "BRL", Name: "Brazilian Real", Symbol: "R$", Decimals: 2, SymbolPos: SymbolPrefix},
	"RUB": {Code: "RUB", Name: "Russian Ruble", Symbol: "₽", Decimals: 2, SymbolPos: SymbolSuffix},
	"TRY": {Code: "TRY", Name: "Turkish Lira", Symbol: "₺", Decimals: 2, SymbolPos: SymbolPrefix},
	"ZAR": {Code: "ZAR", Name: "South African Rand", Symbol: "R", Decimals: 2, SymbolPos: SymbolPrefix},
	"THB": {Code: "THB", Name: "Thai Baht", Symbol: "฿", Decimals: 2, SymbolPos: SymbolPrefix},
	"PLN": {Code: "PLN", Name: "Polish Złoty", Symbol: "zł", Decimals: 2, SymbolPos: SymbolSuffix},
	"PHP": {Code: "PHP", Name: "Philippine Peso", Symbol: "₱", Decimals: 2, SymbolPos: SymbolPrefix},
	"IDR": {Code: "IDR", Name: "Indonesian Rupiah", Symbol: "Rp", Decimals: 0, SymbolPos: SymbolPrefix},
	"MYR": {Code: "MYR", Name: "Malaysian Ringgit", Symbol: "RM", Decimals: 2, SymbolPos: SymbolPrefix},
	"VND": {Code: "VND", Name: "Vietnamese Dong", Symbol: "₫", Decimals: 0, SymbolPos: SymbolSuffix},
	"TWD": {Code: "TWD", Name: "Taiwan Dollar", Symbol: "NT$", Decimals: 0, SymbolPos: SymbolPrefix},
	"AED": {Code: "AED", Name: "UAE Dirham", Symbol: "د.إ", Decimals: 2, SymbolPos: SymbolSuffix},
	"SAR": {Code: "SAR", Name: "Saudi Riyal", Symbol: "﷼", Decimals: 2, SymbolPos: SymbolSuffix},
	"ILS": {Code: "ILS", Name: "Israeli Shekel", Symbol: "₪", Decimals: 2, SymbolPos: SymbolPrefix},
	"CZK": {Code: "CZK", Name: "Czech Koruna", Symbol: "Kč", Decimals: 2, SymbolPos: SymbolSuffix},
	"HUF": {Code: "HUF", Name: "Hungarian Forint", Symbol: "Ft", Decimals: 0, SymbolPos: SymbolSuffix},
	"RON": {Code: "RON", Name: "Romanian Leu", Symbol: "lei", Decimals: 2, SymbolPos: SymbolSuffix},
}

// Exchange rates to USD (as of base reference)
var exchangeRatesToUSD = map[Code]float64{
	"USD": 1.0,
	"EUR": 1.08,
	"GBP": 1.27,
	"JPY": 0.0067,
	"CNY": 0.14,
	"CAD": 0.74,
	"CHF": 1.13,
	"KRW": 0.00075,
	"INR": 0.012,
	"AUD": 0.65,
	"HKD": 0.13,
	"SGD": 0.74,
	"NZD": 0.60,
	"SEK": 0.093,
	"NOK": 0.092,
	"DKK": 0.145,
	"MXN": 0.058,
	"BRL": 0.20,
	"RUB": 0.011,
	"TRY": 0.031,
	"ZAR": 0.054,
	"THB": 0.029,
	"PLN": 0.25,
	"PHP": 0.018,
	"IDR": 0.000063,
	"MYR": 0.21,
	"VND": 0.00004,
	"TWD": 0.031,
	"AED": 0.27,
	"SAR": 0.27,
	"ILS": 0.27,
	"CZK": 0.044,
	"HUF": 0.0028,
	"RON": 0.22,
}

// =============================================================================
// Currency Lookup
// =============================================================================

// GetCurrency returns currency metadata by code
func GetCurrency(code Code) (Currency, error) {
	if c, ok := currencies[code]; ok {
		return c, nil
	}
	return Currency{}, fmt.Errorf("%w: %s", ErrInvalidCurrency, code)
}

// MustGetCurrency returns currency, panics on error
func MustGetCurrency(code Code) Currency {
	c, err := GetCurrency(code)
	if err != nil {
		panic(err)
	}
	return c
}

// ListCurrencies returns all supported currency codes
func ListCurrencies() []Code {
	codes := make([]Code, 0, len(currencies))
	for code := range currencies {
		codes = append(codes, code)
	}
	return codes
}

// IsValid checks if a currency code is supported
func IsValid(code Code) bool {
	_, ok := currencies[code]
	return ok
}

// =============================================================================
// Formatting
// =============================================================================

// Format formats an amount with currency symbol
func Format(amount float64, code Code) (string, error) {
	c, err := GetCurrency(code)
	if err != nil {
		return "", err
	}
	return formatWithCurrency(amount, c), nil
}

// MustFormat formats an amount, panics on error
func MustFormat(amount float64, code Code) string {
	s, err := Format(amount, code)
	if err != nil {
		panic(err)
	}
	return s
}

// FormatCode formats amount with ISO currency code
func FormatCode(amount float64, code Code) (string, error) {
	c, err := GetCurrency(code)
	if err != nil {
		return "", err
	}
	return formatCodeWithCurrency(amount, c), nil
}

// FormatCompact formats amount in compact notation
func FormatCompact(amount float64, code Code) (string, error) {
	c, err := GetCurrency(code)
	if err != nil {
		return "", err
	}
	return formatCompactWithCurrency(amount, c), nil
}

// MustFormatCompact formats in compact notation, panics on error
func MustFormatCompact(amount float64, code Code) string {
	s, err := FormatCompact(amount, code)
	if err != nil {
		panic(err)
	}
	return s
}

// FormatWithOptions formats with custom options
type FormatOptions struct {
	Symbol       string
	ShowCode     bool
	ShowSymbol   bool
	ThousandsSep string
	DecimalSep   string
	DecimalPlaces int
	SymbolPos    SymbolPosition
	NegativeParens bool // use (100) instead of -100
}

// DefaultFormatOptions returns default formatting options
func DefaultFormatOptions(code Code) FormatOptions {
	c, _ := GetCurrency(code)
	return FormatOptions{
		Symbol:        c.Symbol,
		ShowCode:      false,
		ShowSymbol:    true,
		ThousandsSep:  ",",
		DecimalSep:    ".",
		DecimalPlaces: c.Decimals,
		SymbolPos:     c.SymbolPos,
		NegativeParens: false,
	}
}

// FormatWithOptions formats with custom options
func FormatWithOptions(amount float64, code Code, opts FormatOptions) (string, error) {
	_, err := GetCurrency(code)
	if err != nil {
		return "", err
	}
	if opts.DecimalPlaces < 0 {
		return "", ErrInvalidAmount
	}
	return formatCustom(amount, code, opts), nil
}

func formatWithCurrency(amount float64, c Currency) string {
	opts := DefaultFormatOptions(c.Code)
	opts.ShowSymbol = true
	opts.ShowCode = false
	return formatCustom(amount, c.Code, opts)
}

func formatCodeWithCurrency(amount float64, c Currency) string {
	opts := DefaultFormatOptions(c.Code)
	opts.ShowSymbol = false
	opts.ShowCode = true
	opts.SymbolPos = SymbolSuffix // code always after number
	return formatCustom(amount, c.Code, opts)
}

func formatCompactWithCurrency(amount float64, c Currency) string {
	absAmount := amount
	negative := amount < 0
	if negative {
		absAmount = -absAmount
	}

	var result string
	var suffix string

	switch {
	case absAmount >= 1e12:
		result = formatFloat(absAmount/1e12, 2)
		suffix = "T"
	case absAmount >= 1e9:
		result = formatFloat(absAmount/1e9, 2)
		suffix = "B"
	case absAmount >= 1e6:
		result = formatFloat(absAmount/1e6, 2)
		suffix = "M"
	case absAmount >= 1e3:
		result = formatFloat(absAmount/1e3, 2)
		suffix = "K"
	default:
		result = formatFloat(absAmount, c.Decimals)
	}

	if negative {
		result = "-" + result
	}

	if c.SymbolPos == SymbolPrefix {
		return c.Symbol + result + suffix + " " + string(c.Code)
	}
	return result + suffix + " " + string(c.Code) + " " + c.Symbol
}

func formatCustom(amount float64, code Code, opts FormatOptions) string {
	negative := amount < 0
	if negative {
		amount = -amount
	}

	// Format the number
	formatted := formatFloatWithSep(amount, opts.DecimalPlaces, opts.ThousandsSep, opts.DecimalSep)

	// Build symbol/code part
	var symbolPart string
	if opts.ShowSymbol && opts.Symbol != "" {
		symbolPart = opts.Symbol
	} else if opts.ShowCode {
		symbolPart = string(code)
	}

	var result string
	if opts.SymbolPos == SymbolPrefix {
		result = symbolPart + formatted
	} else {
		result = formatted + " " + symbolPart
	}

	// Handle negative
	if negative {
		if opts.NegativeParens {
			result = "(" + result + ")"
		} else {
			result = "-" + result
		}
	}

	return strings.Trim(result, " ")
}

// =============================================================================
// Parsing
// =============================================================================

var (
	// Matches: $1,234.56, €1.234,56, 1,234.56 USD, etc.
	parseRegex = regexp.MustCompile(`^([€£₽₺₹฿₱RpRMNT$﷼₪złFtKčlei kr\s]*)\s*(-?[\d',.\s]+)\s*([€£₽₺₹฿₱RpRMNT$﷼₪złFtKčlei kr\s]*)$|^(?:([A-Z]{3})\s+)?(-?[\d',.\s]+)(?:\s+([A-Z]{3}))?$`)
)

// Parse parses a currency string and returns Money
func Parse(s string) (*Money, error) {
	s = strings.TrimSpace(s)
	if s == "" {
		return nil, ErrParseFailed
	}

	// Try simple format: "1,234.56 USD"
	parts := strings.Fields(s)
	if len(parts) >= 2 {
		// Check if last part is a currency code
		lastPart := strings.ToUpper(parts[len(parts)-1])
		if _, ok := currencies[Code(lastPart)]; ok {
			numberPart := strings.Join(parts[:len(parts)-1], "")
			if amount, err := parseNumber(numberPart); err == nil {
				return &Money{Amount: amount, Currency: Code(lastPart)}, nil
			}
		}
		// Check if first part is a currency code
		firstPart := strings.ToUpper(parts[0])
		if _, ok := currencies[Code(firstPart)]; ok {
			numberPart := strings.Join(parts[1:], "")
			if amount, err := parseNumber(numberPart); err == nil {
				return &Money{Amount: amount, Currency: Code(firstPart)}, nil
			}
		}
	}

	// Try with symbol - for shared symbols, try priority currencies first
	_ = cleanCurrencyString(s)

	// Define symbol priority for symbols shared by multiple currencies
	symbolPriority := map[string][]Code{
		"$": {"USD", "MXN", "AUD", "NZD", "CAD", "HKD", "SGD"},
	}

	// Collect all currencies, putting priority codes first
	type codeWithPrio struct {
		code Code
		prio int
	}
	var orderedCodes []codeWithPrio
	for code := range currencies {
		prio := 999
		c := currencies[code]
		if priorityCodes, ok := symbolPriority[c.Symbol]; ok {
			for i, pc := range priorityCodes {
				if pc == code {
					prio = i
					break
				}
			}
		}
		orderedCodes = append(orderedCodes, codeWithPrio{code, prio})
	}
	// Sort by priority (lower = first)
	for i := 0; i < len(orderedCodes)-1; i++ {
		for j := i + 1; j < len(orderedCodes); j++ {
			if orderedCodes[j].prio < orderedCodes[i].prio {
				orderedCodes[i], orderedCodes[j] = orderedCodes[j], orderedCodes[i]
			}
		}
	}

	for _, cp := range orderedCodes {
		code := cp.code
		c := currencies[code]

		// Try prefix
		testPrefix := strings.TrimSpace(strings.Replace(s, c.Symbol, "", 1))
		if testPrefix != s {
			if amount, err := parseNumber(testPrefix); err == nil {
				return &Money{Amount: amount, Currency: code}, nil
			}
		}
		// Try suffix
		testSuffix := strings.TrimSpace(strings.TrimSuffix(s, c.Symbol))
		if testSuffix != s {
			if amount, err := parseNumber(testSuffix); err == nil {
				return &Money{Amount: amount, Currency: code}, nil
			}
		}
	}

	return nil, ErrParseFailed
}

// MustParse parses a currency string, panics on error
func MustParse(s string) *Money {
	m, err := Parse(s)
	if err != nil {
		panic(err)
	}
	return m
}

func cleanCurrencyString(s string) string {
	// Remove common currency symbols and spaces
	s = strings.ReplaceAll(s, "$", "")
	s = strings.ReplaceAll(s, "€", "")
	s = strings.ReplaceAll(s, "£", "")
	s = strings.ReplaceAll(s, "¥", "")
	s = strings.ReplaceAll(s, "₩", "")
	s = strings.ReplaceAll(s, "₹", "")
	s = strings.ReplaceAll(s, "₽", "")
	s = strings.ReplaceAll(s, "₺", "")
	s = strings.ReplaceAll(s, "฿", "")
	s = strings.ReplaceAll(s, "₱", "")
	s = strings.ReplaceAll(s, "Rp", "")
	s = strings.ReplaceAll(s, "RM", "")
	s = strings.ReplaceAll(s, "NT$", "")
	s = strings.ReplaceAll(s, "₫", "")
	s = strings.ReplaceAll(s, "₪", "")
	s = strings.ReplaceAll(s, "﷼", "")
	s = strings.ReplaceAll(s, "C$", "")
	s = strings.ReplaceAll(s, "A$", "")
	s = strings.ReplaceAll(s, "S$", "")
	s = strings.ReplaceAll(s, "NZ$", "")
	s = strings.ReplaceAll(s, "HK$", "")
	s = strings.ReplaceAll(s, "R$", "")
	s = strings.ReplaceAll(s, "zł", "")
	s = strings.ReplaceAll(s, "Ft", "")
	s = strings.ReplaceAll(s, "Kč", "")
	s = strings.ReplaceAll(s, "lei", "")
	s = strings.ReplaceAll(s, "kr", "")
	s = strings.ReplaceAll(s, " ", "")
	s = strings.ReplaceAll(s, ",", "")
	return strings.TrimSpace(s)
}

func parseNumber(s string) (float64, error) {
	s = strings.TrimSpace(s)
	// Remove currency symbols, letters (keep digits, dots, commas, minus, parens)
	var cleaned []rune
	for _, r := range s {
		if r == '-' || r == '(' || r == ')' || r == '.' || (r >= '0' && r <= '9') {
			cleaned = append(cleaned, r)
		}
	}
	s = string(cleaned)
	s = strings.ReplaceAll(s, ",", "")
	if strings.HasPrefix(s, "(") && strings.HasSuffix(s, ")") {
		s = "-" + s[1:len(s)-1]
	}
	amount, err := strconv.ParseFloat(s, 64)
	if err != nil {
		return 0, ErrParseFailed
	}
	return amount, nil
}

// ParseAmount parses just a number string (removes separators)
func ParseAmount(s string) (float64, error) {
	return parseNumber(s)
}

// =============================================================================
// Conversion
// =============================================================================

// Convert converts money to target currency using exchange rates
func Convert(money Money, targetCode Code) (*Money, error) {
	if _, err := GetCurrency(targetCode); err != nil {
		return nil, err
	}

	// Convert to USD first
	usdAmount := money.Amount * exchangeRatesToUSD[money.Currency]
	// Convert from USD to target
	targetAmount := usdAmount / exchangeRatesToUSD[targetCode]

	return &Money{Amount: targetAmount, Currency: targetCode}, nil
}

// MustConvert converts money, panics on error
func MustConvert(money Money, targetCode Code) *Money {
	m, err := Convert(money, targetCode)
	if err != nil {
		panic(err)
	}
	return m
}

// GetExchangeRate returns exchange rate from one currency to another
func GetExchangeRate(from, to Code) (float64, error) {
	fromRate, ok1 := exchangeRatesToUSD[from]
	toRate, ok2 := exchangeRatesToUSD[to]
	if !ok1 || !ok2 {
		return 0, ErrInvalidCurrency
	}
	return fromRate / toRate, nil
}

// ConvertAmount converts an amount directly (not Money struct)
func ConvertAmount(amount float64, from, to Code) (float64, error) {
	money := Money{Amount: amount, Currency: from}
	result, err := Convert(money, to)
	if err != nil {
		return 0, err
	}
	return result.Amount, nil
}

// =============================================================================
// Arithmetic
// =============================================================================

// Add adds two money values (must be same currency)
func Add(m1, m2 Money) (Money, error) {
	if m1.Currency != m2.Currency {
		m2converted, err := Convert(m2, m1.Currency)
		if err != nil {
			return Money{}, err
		}
		m2 = *m2converted
	}
	return Money{Amount: m1.Amount + m2.Amount, Currency: m1.Currency}, nil
}

// MustAdd adds two money values, panics on error
func MustAdd(m1, m2 Money) Money {
	m, err := Add(m1, m2)
	if err != nil {
		panic(err)
	}
	return m
}

// Subtract subtracts two money values
func Subtract(m1, m2 Money) (Money, error) {
	if m1.Currency != m2.Currency {
		m2converted, err := Convert(m2, m1.Currency)
		if err != nil {
			return Money{}, err
		}
		m2 = *m2converted
	}
	return Money{Amount: m1.Amount - m2.Amount, Currency: m1.Currency}, nil
}

// MustSubtract subtracts two money values, panics on error
func MustSubtract(m1, m2 Money) Money {
	m, err := Subtract(m1, m2)
	if err != nil {
		panic(err)
	}
	return m
}

// Multiply multiplies a money value by a factor
func Multiply(m Money, factor float64) Money {
	return Money{Amount: m.Amount * factor, Currency: m.Currency}
}

// Divide divides a money value by a divisor
func Divide(m Money, divisor float64) (Money, error) {
	if divisor == 0 {
		return Money{}, ErrZeroAmount
	}
	return Money{Amount: m.Amount / divisor, Currency: m.Currency}, nil
}

// MustDivide divides a money value, panics on error
func MustDivide(m Money, divisor float64) Money {
	result, err := Divide(m, divisor)
	if err != nil {
		panic(err)
	}
	return result
}

// Allocate allocates an amount among n recipients evenly (returns remainder handling)
func Allocate(m Money, n int) ([]Money, error) {
	if n <= 0 {
		return nil, errors.New("n must be positive")
	}
	if m.Amount < 0 {
		return nil, ErrNegativeAmount
	}

	base := Floor(m.Amount / float64(n))
	remainder := m.Amount - base*float64(n)

	result := make([]Money, n)
	for i := 0; i < n; i++ {
		result[i] = Money{Amount: base, Currency: m.Currency}
	}
	// Distribute remainder cents fairly: centsPerPerson each + first extraCents get +1 cent
	remainderCents := int(RoundToDecimal(remainder, 2) * 100)
	centsPerPerson := remainderCents / n
	extraCents := remainderCents % n

	for i := 0; i < n; i++ {
		result[i].Amount += float64(centsPerPerson) * 0.01
	}
	for i := 0; i < extraCents; i++ {
		result[i].Amount += 0.01
	}

	return result, nil
}

// SplitRatio splits amount by ratio (e.g., []int{1, 2, 3} for 1:2:3)
func SplitRatio(amount float64, code Code, ratios []int) ([]Money, error) {
	if len(ratios) == 0 {
		return nil, errors.New("ratios cannot be empty")
	}
	total := 0
	for _, r := range ratios {
		if r <= 0 {
			return nil, errors.New("ratios must be positive")
		}
		total += r
	}

	result := make([]Money, len(ratios))
	for i, r := range ratios {
		result[i] = Money{Amount: amount * float64(r) / float64(total), Currency: code}
	}
	return result, nil
}

// =============================================================================
// Utility
// =============================================================================

// Round rounds amount to currency's decimal places
func Round(amount float64, code Code) float64 {
	c, _ := GetCurrency(code)
	return RoundToDecimal(amount, c.Decimals)
}

// RoundToDecimal rounds amount to specified decimal places
func RoundToDecimal(amount float64, decimals int) float64 {
	pow := 1.0
	for i := 0; i < decimals; i++ {
		pow *= 10
	}
	return float64(int(amount*pow+0.5)) / pow
}

// Floor returns the floor of amount
func Floor(amount float64) float64 {
	return float64(int(amount))
}

// Ceil returns the ceiling of amount
func Ceil(amount float64) float64 {
	if amount == float64(int(amount)) {
		return amount
	}
	return float64(int(amount) + 1)
}

// Abs returns absolute value
func Abs(amount float64) float64 {
	if amount < 0 {
		return -amount
	}
	return amount
}

// IsZero checks if amount is zero
func IsZero(amount float64) bool {
	return absDiff(amount, 0) < 0.0001
}

// IsPositive checks if amount is positive
func IsPositive(amount float64) bool {
	return amount > 0.0001
}

// IsNegative checks if amount is negative
func IsNegative(amount float64) bool {
	return amount < -0.0001
}

func absDiff(a, b float64) float64 {
	d := a - b
	if d < 0 {
		return -d
	}
	return d
}

// Compare compares two money values (returns -1, 0, 1)
func Compare(m1, m2 Money) (int, error) {
	if m1.Currency != m2.Currency {
		m2converted, err := Convert(m2, m1.Currency)
		if err != nil {
			return 0, err
		}
		m2 = *m2converted
	}
	if m1.Amount < m2.Amount-0.0001 {
		return -1, nil
	}
	if m1.Amount > m2.Amount+0.0001 {
		return 1, nil
	}
	return 0, nil
}

// Min returns the smaller of two money values
func Min(m1, m2 Money) (Money, error) {
	cmp, err := Compare(m1, m2)
	if err != nil {
		return Money{}, err
	}
	if cmp <= 0 {
		return m1, nil
	}
	return m2, nil
}

// Max returns the larger of two money values
func Max(m1, m2 Money) (Money, error) {
	cmp, err := Compare(m1, m2)
	if err != nil {
		return Money{}, err
	}
	if cmp >= 0 {
		return m1, nil
	}
	return m2, nil
}

// Clamp clamps a money value between min and max
func Clamp(m, min, max Money) (Money, error) {
	cmp1, err := Compare(m, min)
	if err != nil {
		return Money{}, err
	}
	if cmp1 < 0 {
		return min, nil
	}
	cmp2, err := Compare(m, max)
	if err != nil {
		return Money{}, err
	}
	if cmp2 > 0 {
		return max, nil
	}
	return m, nil
}

// =============================================================================
// Number to Words
// =============================================================================

var units = []string{"", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"}
var teens = []string{"ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"}
var tens = []string{"", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"}
var scales = []string{"", "thousand", "million", "billion", "trillion", "quadrillion"}

func intToWords(n int64) string {
	if n == 0 {
		return "zero"
	}
	if n < 0 {
		return "negative " + intToWords(-n)
	}

	var words []string
	var scaleIdx int

	for n > 0 {
		if n%1000 != 0 {
			words = append([]string{scaleWord(int(n%1000), scaleIdx)}, words...)
		}
		n /= 1000
		scaleIdx++
	}

	result := words[0]
	for i := 1; i < len(words); i++ {
		result += " " + words[i]
	}
	return result
}

func scaleWord(n int, scale int) string {
	if n == 0 {
		return ""
	}
	var parts []string
	if n >= 100 {
		parts = append(parts, units[n/100]+" hundred")
		n %= 100
	}
	if n >= 10 && n <= 19 {
		parts = append(parts, teens[n-10])
	} else if n >= 20 {
		parts = append(parts, tens[n/10])
		if n%10 != 0 {
			parts = append(parts, units[n%10])
		}
	} else if n > 0 {
		parts = append(parts, units[n])
	}
	result := strings.Join(parts, " ")
	if scale > 0 && scale < len(scales) {
		result += " " + scales[scale]
	}
	return result
}

// ToWords converts amount to spoken words (for code)
func ToWords(amount float64, code Code) (string, error) {
	c, err := GetCurrency(code)
	if err != nil {
		return "", err
	}

	whole := int64(amount)
	frac := int64((amount - float64(whole)) * 100)

	result := intToWords(whole) + " " + string(c.Code)
	if frac > 0 {
		result += " and " + intToWords(frac) + "/100"
	}
	return result, nil
}

// ToWordsLong converts to full English words (e.g., "one hundred twenty-three dollars")
func ToWordsLong(amount float64, code Code) (string, error) {
	c, err := GetCurrency(code)
	if err != nil {
		return "", err
	}

	whole := int64(amount)
	frac := int64((amount - float64(whole)) * 100)

	result := intToWords(whole)
	if c.Code == "JPY" || c.Code == "KRW" || c.Code == "VND" || c.Code == "IDR" || c.Code == "HUF" {
		result += " " + strings.ToLower(string(c.Code))
	} else {
		result += " dollar"
		if whole != 1 {
			result += "s"
		}
	}
	if frac > 0 {
		result += " and " + intToWords(frac) + "/100"
	}
	return result, nil
}

// =============================================================================
// Internal Helpers
// =============================================================================

func formatFloat(v float64, decimals int) string {
	return formatFloatWithSep(v, decimals, ",", ".")
}

func formatFloatWithSep(v float64, decimals int, thousandsSep, decimalSep string) string {
	negative := v < 0
	if negative {
		v = -v
	}

	// Round to decimals
	pow := 1.0
	for i := 0; i < decimals; i++ {
		pow *= 10
	}
	v = float64(int(v*pow+0.5)) / pow

	// Split into integer and decimal parts
	whole := int64(v)
	frac := v - float64(whole)

	// Format whole part with thousands separator
	wholeStr := strconv.FormatInt(whole, 10)
	var result []byte
	n := len(wholeStr)
	for i := 0; i < n; i++ {
		result = append(result, wholeStr[i])
		if (n-i-1)%3 == 0 && i != n-1 {
			result = append(result, thousandsSep[0])
		}
	}

	wholeFormatted := string(result)
	if negative {
		wholeFormatted = "-" + wholeFormatted
	}

	if decimals > 0 {
		fracStr := strconv.FormatFloat(frac, 'f', decimals, 64)
		fracStr = fracStr[2:] // Remove "0."
		return wholeFormatted + decimalSep + fracStr
	}
	return wholeFormatted
}
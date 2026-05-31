package main

import (
	"fmt"

	currency "github.com/ayukyo/alltoolkit/Go/currency_utils"
)

func main() {
	// Format currencies
	fmt.Println("=== Format ===")
	fmt.Println(currency.MustFormat(1234.56, "USD"))
	fmt.Println(currency.MustFormat(1234.56, "EUR"))
	fmt.Println(currency.MustFormat(1234, "JPY"))
	fmt.Println(currency.MustFormat(1234.56, "CNY"))
	fmt.Println(currency.MustFormat(1234.56, "GBP"))
	fmt.Println(currency.MustFormat(1234.56, "KRW"))

	// Format compact
	fmt.Println("\n=== Format Compact ===")
	fmt.Println(currency.MustFormatCompact(1500000, "USD"))
	fmt.Println(currency.MustFormatCompact(1234567890, "EUR"))

	// Parse currency strings
	fmt.Println("\n=== Parse ===")
	m, _ := currency.Parse("$1,234.56 USD")
	fmt.Printf("Parsed: %.2f %s\n", m.Amount, m.Currency)

	m, _ = currency.Parse("1,234.56 EUR")
	fmt.Printf("Parsed: %.2f %s\n", m.Amount, m.Currency)

	m, _ = currency.Parse("¥1,234")
	fmt.Printf("Parsed: %.2f %s\n", m.Amount, m.Currency)

	// Conversion
	fmt.Println("\n=== Conversion ===")
	usd := currency.Money{Amount: 100, Currency: "USD"}
	eur, _ := currency.Convert(usd, "EUR")
	fmt.Printf("100 USD = %.2f EUR\n", eur.Amount)

	gbp, _ := currency.Convert(usd, "GBP")
	fmt.Printf("100 USD = %.2f GBP\n", gbp.Amount)

	jpy, _ := currency.Convert(usd, "JPY")
	fmt.Printf("100 USD = %.2f JPY\n", jpy.Amount)

	// Arithmetic
	fmt.Println("\n=== Arithmetic ===")
	m1 := currency.Money{Amount: 100, Currency: "USD"}
	m2 := currency.Money{Amount: 50, Currency: "USD"}
	sum, _ := currency.Add(m1, m2)
	fmt.Printf("100 + 50 = %.2f USD\n", sum.Amount)

	m3 := currency.Money{Amount: 50, Currency: "EUR"}
	mixedSum, _ := currency.Add(m1, m3)
	fmt.Printf("100 USD + 50 EUR = %.2f USD\n", mixedSum.Amount)

	mult := currency.Multiply(m1, 1.5)
	fmt.Printf("100 * 1.5 = %.2f USD\n", mult.Amount)

	// Allocate
	fmt.Println("\n=== Allocate ===")
	whole := currency.Money{Amount: 100, Currency: "USD"}
	parts, _ := currency.Allocate(whole, 3)
	fmt.Printf("Split 100 USD among 3: ")
	for i, p := range parts {
		fmt.Printf("  Person %d: %.2f\n", i+1, p.Amount)
	}

	// Split by ratio
	fmt.Println("\n=== Split Ratio ===")
	split, _ := currency.SplitRatio(100, "USD", []int{1, 2, 3})
	fmt.Printf("Split 100 USD by ratio 1:2:3: ")
	for _, p := range split {
		fmt.Printf("%.2f ", p.Amount)
	}
	fmt.Println()

	// Number to words
	fmt.Println("\n=== Number to Words ===")
	words, _ := currency.ToWords(1234.56, "USD")
	fmt.Println(words)
	wordsLong, _ := currency.ToWordsLong(1234.56, "USD")
	fmt.Println(wordsLong)

	// Round
	fmt.Println("\n=== Round ===")
	fmt.Printf("Round 1.234 USD: %.2f\n", currency.Round(1.234, "USD"))
	fmt.Printf("Round 1.235 USD: %.2f\n", currency.Round(1.235, "USD"))
	fmt.Printf("Round 1.235 JPY: %.0f\n", currency.Round(1.235, "JPY"))

	// Compare
	fmt.Println("\n=== Compare ===")
	m4 := currency.Money{Amount: 100, Currency: "USD"}
	m5 := currency.Money{Amount: 200, Currency: "USD"}
	cmp, _ := currency.Compare(m4, m5)
	fmt.Printf("Compare 100 vs 200 USD: %d\n", cmp)

	min, _ := currency.Min(m4, m5)
	max, _ := currency.Max(m4, m5)
	fmt.Printf("Min: %.2f USD, Max: %.2f USD\n", min.Amount, max.Amount)

	// Exchange rate
	fmt.Println("\n=== Exchange Rate ===")
	rate, _ := currency.GetExchangeRate("USD", "EUR")
	fmt.Printf("USD to EUR rate: %.4f\n", rate)

	// All currencies
	fmt.Println("\n=== All Supported Currencies ===")
	fmt.Printf("Total: %d currencies\n", len(currency.ListCurrencies()))
}
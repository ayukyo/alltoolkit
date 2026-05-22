// Example demonstrates the usage of rate_calc_utils package
package main

import (
	"fmt"
	"math"

	"github.com/ayukyo/alltoolkit/Go/rate_calc_utils"
)

func main() {
	fmt.Println("=== Rate Calculation Utilities Demo ===")
	fmt.Println()

	// 1. Compound Interest
	fmt.Println("1. Compound Interest")
	fmt.Println("   Principal: $10,000, Rate: 5%, Years: 5, Compounded Monthly")
	result, _ := rate_calc_utils.CompoundInterest(10000, 0.05, 5, 12)
	fmt.Printf("   Future Value: $%.2f\n", result)
	fmt.Printf("   Interest Earned: $%.2f\n", result-10000)
	fmt.Println()

	// 2. Simple Interest
	fmt.Println("2. Simple Interest")
	fmt.Println("   Principal: $10,000, Rate: 5%, Years: 5")
	result, _ = rate_calc_utils.SimpleInterest(10000, 0.05, 5)
	fmt.Printf("   Future Value: $%.2f\n", result)
	fmt.Println()

	// 3. APR to APY Conversion
	fmt.Println("3. APR to APY Conversion")
	fmt.Println("   APR: 12%, Compounded Monthly")
	apy, _ := rate_calc_utils.APRToAPY(0.12, 12)
	fmt.Printf("   APY: %.2f%%\n", apy*100)
	fmt.Println()

	// 4. Loan Payment Calculation
	fmt.Println("4. Monthly Loan Payment")
	fmt.Println("   Principal: $200,000, Rate: 4.5%, Term: 30 years")
	payment, _ := rate_calc_utils.LoanPayment(200000, 0.045, 30)
	fmt.Printf("   Monthly Payment: $%.2f\n", payment)
	fmt.Printf("   Total Payments: $%.2f\n", payment*360)
	fmt.Printf("   Total Interest: $%.2f\n", payment*360-200000)
	fmt.Println()

	// 5. Amortization Schedule (first 3 months)
	fmt.Println("5. Loan Amortization (First 3 Months)")
	fmt.Println("   Principal: $10,000, Rate: 6%, Term: 1 year")
	schedule, _ := rate_calc_utils.LoanAmortization(10000, 0.06, 1)
	fmt.Printf("   %-8s %-10s %-10s %-10s %-12s\n", "Month", "Payment", "Principal", "Interest", "Balance")
	for i := 0; i < 3 && i < len(schedule); i++ {
		p := schedule[i]
		fmt.Printf("   %-8d $%-9.2f $%-9.2f $%-9.2f $%-11.2f\n",
			p.PaymentNumber, p.Payment, p.Principal, p.Interest, p.Balance)
	}
	fmt.Println("   ...")
	fmt.Println()

	// 6. Return on Investment
	fmt.Println("6. Return on Investment")
	fmt.Println("   Investment: $1,000, Final Value: $1,500")
	roi, _ := rate_calc_utils.ROI(1500, 1000)
	fmt.Printf("   ROI: %.2f%%\n", roi)

	fmt.Println("   Investment: $1,000, Final Value: $2,000 over 5 years")
	annualROI, _ := rate_calc_utils.AnnualizedROI(1000, 1000, 5)
	fmt.Printf("   Annualized ROI: %.2f%%\n", annualROI)
	fmt.Println()

	// 7. Currency Exchange
	fmt.Println("7. Currency Exchange")
	fmt.Println("   Amount: $1,000 USD, Rate: 0.92 EUR/USD")
	eur, _ := rate_calc_utils.ExchangeRate(1000, 0.92)
	fmt.Printf("   Result: %.2f EUR\n", eur)
	fmt.Println()

	// 8. Break-Even Analysis
	fmt.Println("8. Break-Even Point")
	fmt.Println("   Fixed Costs: $10,000, Price: $50/unit, Variable Cost: $30/unit")
	breakEven, _ := rate_calc_utils.BreakEvenPoint(10000, 50, 30)
	fmt.Printf("   Break-Even Units: %.0f units\n", breakEven)
	fmt.Printf("   Break-Even Revenue: $%.2f\n", breakEven*50)
	fmt.Println()

	// 9. Present Value Calculation
	fmt.Println("9. Present Value")
	fmt.Println("   Future Value: $10,000, Rate: 5%, Years: 10")
	pv, _ := rate_calc_utils.PresentValue(10000, 0.05, 10)
	fmt.Printf("   Present Value: $%.2f\n", pv)
	fmt.Println()

	// 10. Future Value Calculation
	fmt.Println("10. Future Value")
	fmt.Println("   Present Value: $6,139.13, Rate: 5%, Years: 10")
	fv, _ := rate_calc_utils.FutureValue(6139.13, 0.05, 10)
	fmt.Printf("   Future Value: $%.2f\n", fv)
	fmt.Println()

	// 11. Inflation Adjustment
	fmt.Println("11. Inflation Adjustment")
	fmt.Println("   Amount: $100,000, Inflation: 3%, Years: 10")
	adjusted, _ := rate_calc_utils.InflationAdjusted(100000, 0.03, 10)
	fmt.Printf("   Adjusted Value: $%.2f\n", adjusted)
	fmt.Printf("   Purchasing Power Loss: $%.2f\n", 100000-adjusted)
	fmt.Println()

	// 12. Rule of 72
	fmt.Println("12. Rule of 72")
	rates := []float64{0.04, 0.06, 0.08, 0.10, 0.12}
	fmt.Println("   Years to double investment:")
	for _, r := range rates {
		years, _ := rate_calc_utils.Rule72(r)
		fmt.Printf("   At %.0f%%: %.1f years\n", r*100, years)
	}
	fmt.Println()

	// 13. Monthly Savings Goal
	fmt.Println("13. Monthly Savings Goal")
	fmt.Println("   Goal: $100,000, Expected Return: 7%, Years: 10")
	monthly, _ := rate_calc_utils.MonthlySavingsGoal(100000, 0.07, 10)
	fmt.Printf("   Monthly Savings Needed: $%.2f\n", monthly)
	fmt.Printf("   Total Contributions: $%.2f\n", monthly*120)
	fmt.Println()

	// 14. Total Interest on Loan
	fmt.Println("14. Total Interest on Loan")
	fmt.Println("   Principal: $200,000, Rate: 4.5%, Term: 30 years")
	totalInt, _ := rate_calc_utils.TotalInterest(200000, 0.045, 30)
	fmt.Printf("   Total Interest Paid: $%.2f\n", totalInt)
	fmt.Println()

	// 15. Reverse: Find Rate from Payment
	fmt.Println("15. Find Interest Rate from Payment")
	fmt.Println("   Principal: $200,000, Monthly Payment: $1,013.37, Term: 30 years")
	foundRate, _ := rate_calc_utils.RateFromPayment(200000, 1013.37, 30)
	fmt.Printf("   Calculated Rate: %.3f%%\n", foundRate*100)
	
	// Verify by calculating payment with found rate
	verifyPayment, _ := rate_calc_utils.LoanPayment(200000, foundRate, 30)
	fmt.Printf("   Verification Payment: $%.2f (should be ~$1,013.37)\n", verifyPayment)
	fmt.Println()

	// Bonus: Comparing Compound vs Simple Interest
	fmt.Println("=== Bonus: Compound vs Simple Interest ===")
	fmt.Printf("%-6s %-15s %-15s %-15s\n", "Year", "Compound", "Simple", "Difference")
	fmt.Println("--------------------------------------------------------")
	
	principal := 10000.0
	rate := 0.05
	for year := 0; year <= 10; year += 2 {
		compound, _ := rate_calc_utils.CompoundInterest(principal, rate, year, 12)
		simple, _ := rate_calc_utils.SimpleInterest(principal, rate, float64(year))
		diff := compound - simple
		fmt.Printf("%-6d $%-14.2f $%-14.2f $%-14.2f\n", year, compound, simple, diff)
	}
	fmt.Println()

	// Bonus: APY Comparison
	fmt.Println("=== Bonus: APY at Different Compounding Frequencies ===")
	fmt.Printf("APR: 5%%\n")
	fmt.Printf("%-20s %-15s\n", "Compounding", "APY")
	fmt.Println("------------------------------------")
	
	frequencies := []struct {
		name  string
		times int
	}{
		{"Annually", 1},
		{"Semi-annually", 2},
		{"Quarterly", 4},
		{"Monthly", 12},
		{"Daily", 365},
		{"Continuous", 365 * 24},
	}
	
	for _, f := range frequencies {
		apy, _ := rate_calc_utils.APRToAPY(0.05, f.times)
		fmt.Printf("%-20s %.4f%%\n", f.name, apy*100)
	}
	
	// Continuous compounding using formula: e^(r) - 1
	continuousAPY := math.Exp(0.05) - 1
	fmt.Printf("%-20s %.4f%%\n", "Continuous (exact)", continuousAPY*100)
}
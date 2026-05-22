// Package rate_calc_utils provides financial rate calculation utilities.
// It includes functions for compound interest, simple interest, loan payments,
// APR/APY conversions, and investment return calculations.
//
// All calculations use float64 for precision. Rates should be provided as
// decimal values (e.g., 0.05 for 5%).
package rate_calc_utils

import (
	"errors"
	"math"
)

// Common errors
var (
	ErrInvalidRate     = errors.New("invalid rate: must be non-negative")
	ErrInvalidPeriods  = errors.New("invalid periods: must be positive")
	ErrInvalidAmount   = errors.New("invalid amount: must be positive")
	ErrInvalidPayments = errors.New("invalid number of payments: must be positive")
)

// CompoundInterest calculates compound interest.
// principal: initial amount
// rate: annual interest rate (e.g., 0.05 for 5%)
// periods: number of compounding periods
// compoundsPerYear: number of times interest is compounded per year
func CompoundInterest(principal, rate float64, periods, compoundsPerYear int) (float64, error) {
	if principal < 0 {
		return 0, ErrInvalidAmount
	}
	if rate < 0 {
		return 0, ErrInvalidRate
	}
	if periods < 0 {
		return 0, ErrInvalidPeriods
	}
	if compoundsPerYear <= 0 {
		return 0, errors.New("compounds per year must be positive")
	}

	// A = P(1 + r/n)^(nt)
	ratePerCompound := rate / float64(compoundsPerYear)
	totalCompounds := compoundsPerYear * periods
	result := principal * math.Pow(1+ratePerCompound, float64(totalCompounds))
	return result, nil
}

// SimpleInterest calculates simple interest.
// principal: initial amount
// rate: annual interest rate (e.g., 0.05 for 5%)
// years: number of years
func SimpleInterest(principal, rate float64, years float64) (float64, error) {
	if principal < 0 {
		return 0, ErrInvalidAmount
	}
	if rate < 0 {
		return 0, ErrInvalidRate
	}
	if years < 0 {
		return 0, errors.New("years must be non-negative")
	}

	// A = P(1 + rt)
	result := principal * (1 + rate*years)
	return result, nil
}

// APRToAPY converts Annual Percentage Rate to Annual Percentage Yield.
// apr: annual percentage rate (e.g., 0.05 for 5%)
// compoundsPerYear: number of compounding periods per year
func APRToAPY(apr float64, compoundsPerYear int) (float64, error) {
	if apr < 0 {
		return 0, ErrInvalidRate
	}
	if compoundsPerYear <= 0 {
		return 0, errors.New("compounds per year must be positive")
	}

	// APY = (1 + APR/n)^n - 1
	ratePerCompound := apr / float64(compoundsPerYear)
	apy := math.Pow(1+ratePerCompound, float64(compoundsPerYear)) - 1
	return apy, nil
}

// APYToAPR converts Annual Percentage Yield to Annual Percentage Rate.
// apy: annual percentage yield (e.g., 0.05 for 5%)
// compoundsPerYear: number of compounding periods per year
func APYToAPR(apy float64, compoundsPerYear int) (float64, error) {
	if apy < 0 {
		return 0, ErrInvalidRate
	}
	if compoundsPerYear <= 0 {
		return 0, errors.New("compounds per year must be positive")
	}

	// APR = n * ((1 + APY)^(1/n) - 1)
	apr := float64(compoundsPerYear) * (math.Pow(1+apy, 1/float64(compoundsPerYear)) - 1)
	return apr, nil
}

// LoanPayment calculates the monthly payment for a loan.
// principal: loan amount
// annualRate: annual interest rate (e.g., 0.05 for 5%)
// years: loan term in years
func LoanPayment(principal, annualRate float64, years int) (float64, error) {
	if principal <= 0 {
		return 0, ErrInvalidAmount
	}
	if annualRate < 0 {
		return 0, ErrInvalidRate
	}
	if years <= 0 {
		return 0, ErrInvalidPeriods
	}

	months := years * 12
	monthlyRate := annualRate / 12

	// If rate is 0, simple division
	if monthlyRate == 0 {
		return principal / float64(months), nil
	}

	// M = P * [r(1+r)^n] / [(1+r)^n - 1]
	factor := math.Pow(1+monthlyRate, float64(months))
	payment := principal * (monthlyRate * factor) / (factor - 1)
	return payment, nil
}

// LoanAmortization returns a payment schedule for a loan.
type AmortizationEntry struct {
	PaymentNumber int
	Payment       float64
	Principal     float64
	Interest      float64
	Balance       float64
}

// LoanAmortization generates an amortization schedule.
// principal: loan amount
// annualRate: annual interest rate
// years: loan term in years
func LoanAmortization(principal, annualRate float64, years int) ([]AmortizationEntry, error) {
	if principal <= 0 {
		return nil, ErrInvalidAmount
	}
	if annualRate < 0 {
		return nil, ErrInvalidRate
	}
	if years <= 0 {
		return nil, ErrInvalidPeriods
	}

	monthlyPayment, err := LoanPayment(principal, annualRate, years)
	if err != nil {
		return nil, err
	}

	months := years * 12
	monthlyRate := annualRate / 12
	balance := principal
	schedule := make([]AmortizationEntry, months)

	for i := 0; i < months; i++ {
		interest := balance * monthlyRate
		principalPaid := monthlyPayment - interest
		balance -= principalPaid

		// Handle last payment rounding
		if i == months-1 {
			principalPaid += balance
			balance = 0
		} else if balance < 0 {
			balance = 0
		}

		schedule[i] = AmortizationEntry{
			PaymentNumber: i + 1,
			Payment:       monthlyPayment,
			Principal:     principalPaid,
			Interest:      interest,
			Balance:       balance,
		}
	}

	return schedule, nil
}

// ROI calculates Return on Investment as a percentage.
// gain: profit from investment
// cost: initial investment cost
func ROI(gain, cost float64) (float64, error) {
	if cost == 0 {
		return 0, errors.New("cost cannot be zero")
	}

	roi := (gain - cost) / cost * 100
	return roi, nil
}

// AnnualizedROI calculates annualized return on investment.
// gain: profit from investment
// cost: initial investment cost
// years: investment duration in years
func AnnualizedROI(gain, cost float64, years float64) (float64, error) {
	if cost <= 0 {
		return 0, errors.New("cost must be positive")
	}
	if years <= 0 {
		return 0, errors.New("years must be positive")
	}

	// CAGR formula: (Final Value / Initial Value)^(1/years) - 1
	totalReturn := (gain + cost) / cost
	annualized := (math.Pow(totalReturn, 1/years) - 1) * 100
	return annualized, nil
}

// ExchangeRate converts an amount from one currency to another.
// amount: the amount to convert
// rate: exchange rate (units of target currency per unit of source currency)
func ExchangeRate(amount, rate float64) (float64, error) {
	if amount < 0 {
		return 0, ErrInvalidAmount
	}
	if rate < 0 {
		return 0, ErrInvalidRate
	}

	return amount * rate, nil
}

// BreakEvenPoint calculates the break-even point in units.
// fixedCosts: total fixed costs
// pricePerUnit: selling price per unit
// variableCostPerUnit: variable cost per unit
func BreakEvenPoint(fixedCosts, pricePerUnit, variableCostPerUnit float64) (float64, error) {
	if pricePerUnit <= variableCostPerUnit {
		return 0, errors.New("price must be greater than variable cost")
	}
	if fixedCosts < 0 || pricePerUnit <= 0 || variableCostPerUnit < 0 {
		return 0, errors.New("invalid input values")
	}

	// Break-even units = Fixed Costs / (Price - Variable Cost)
	units := fixedCosts / (pricePerUnit - variableCostPerUnit)
	return units, nil
}

// PresentValue calculates the present value of a future amount.
// futureValue: future value amount
// rate: discount rate (e.g., 0.05 for 5%)
// periods: number of periods
func PresentValue(futureValue, rate float64, periods int) (float64, error) {
	if futureValue < 0 {
		return 0, ErrInvalidAmount
	}
	if rate < 0 {
		return 0, ErrInvalidRate
	}
	if periods < 0 {
		return 0, ErrInvalidPeriods
	}

	// PV = FV / (1 + r)^n
	pv := futureValue / math.Pow(1+rate, float64(periods))
	return pv, nil
}

// FutureValue calculates the future value of a present amount.
// presentValue: present value amount
// rate: interest rate (e.g., 0.05 for 5%)
// periods: number of periods
func FutureValue(presentValue, rate float64, periods int) (float64, error) {
	if presentValue < 0 {
		return 0, ErrInvalidAmount
	}
	if rate < 0 {
		return 0, ErrInvalidRate
	}
	if periods < 0 {
		return 0, ErrInvalidPeriods
	}

	// FV = PV * (1 + r)^n
	fv := presentValue * math.Pow(1+rate, float64(periods))
	return fv, nil
}

// InflationAdjusted calculates the inflation-adjusted value.
// amount: current amount
// inflationRate: annual inflation rate (e.g., 0.03 for 3%)
// years: number of years
func InflationAdjusted(amount, inflationRate float64, years int) (float64, error) {
	if amount < 0 {
		return 0, ErrInvalidAmount
	}
	if inflationRate < 0 {
		return 0, ErrInvalidRate
	}
	if years < 0 {
		return 0, ErrInvalidPeriods
	}

	// Adjusted = Amount / (1 + inflation)^years
	adjusted := amount / math.Pow(1+inflationRate, float64(years))
	return adjusted, nil
}

// Rule72 calculates the years to double an investment using the Rule of 72.
// rate: annual rate of return (e.g., 0.08 for 8%)
func Rule72(rate float64) (float64, error) {
	if rate <= 0 {
		return 0, ErrInvalidRate
	}

	return 72 / (rate * 100), nil
}

// EffectiveRate calculates the effective annual rate given a nominal rate
// and number of compounding periods.
// nominalRate: nominal annual rate
// compoundsPerYear: number of compounding periods per year
func EffectiveRate(nominalRate float64, compoundsPerYear int) (float64, error) {
	return APRToAPY(nominalRate, compoundsPerYear)
}

// MonthlySavingsGoal calculates required monthly savings to reach a goal.
// goal: target amount
// annualRate: expected annual return rate
// years: number of years to save
func MonthlySavingsGoal(goal, annualRate float64, years int) (float64, error) {
	if goal <= 0 {
		return 0, ErrInvalidAmount
	}
	if annualRate < 0 {
		return 0, ErrInvalidRate
	}
	if years <= 0 {
		return 0, ErrInvalidPeriods
	}

	months := years * 12
	monthlyRate := annualRate / 12

	// If rate is 0, simple division
	if monthlyRate == 0 {
		return goal / float64(months), nil
	}

	// PMT = FV * r / ((1+r)^n - 1)
	factor := math.Pow(1+monthlyRate, float64(months))
	monthly := goal * monthlyRate / (factor - 1)
	return monthly, nil
}

// TotalInterest calculates total interest paid over a loan term.
// principal: loan amount
// annualRate: annual interest rate
// years: loan term in years
func TotalInterest(principal, annualRate float64, years int) (float64, error) {
	monthlyPayment, err := LoanPayment(principal, annualRate, years)
	if err != nil {
		return 0, err
	}

	totalPayments := monthlyPayment * float64(years*12)
	totalInterest := totalPayments - principal
	return totalInterest, nil
}

// RateFromPayment calculates the annual rate given loan parameters.
// principal: loan amount
// monthlyPayment: monthly payment amount
// years: loan term in years
// Uses binary search for approximation.
func RateFromPayment(principal, monthlyPayment float64, years int) (float64, error) {
	if principal <= 0 || monthlyPayment <= 0 || years <= 0 {
		return 0, errors.New("invalid input parameters")
	}

	months := years * 12

	// Check if payment is sufficient for zero interest
	minPayment := principal / float64(months)
	if monthlyPayment < minPayment {
		return 0, errors.New("monthly payment too low for any interest rate")
	}

	// Binary search for rate
	low, high := 0.0, 1.0 // Search between 0% and 100%
	const tolerance = 0.0000001

	for high-low > tolerance {
		mid := (low + high) / 2
		testPayment, _ := LoanPayment(principal, mid, years)

		if testPayment < monthlyPayment {
			low = mid
		} else {
			high = mid
		}
	}

	return (low + high) / 2, nil
}
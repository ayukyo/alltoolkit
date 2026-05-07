# Investment Utils

A comprehensive, zero-dependency Python library for investment and financial calculations.

## Features

- **Compound Interest**: Calculate compound interest with various compounding frequencies
- **Simple Interest**: Basic simple interest calculations
- **SIP Returns**: Systematic Investment Plan calculations including step-up SIP
- **CAGR**: Compound Annual Growth Rate calculations
- **Present/Future Value**: Time value of money calculations
- **ROI**: Return on Investment with annualization
- **IRR/NPV**: Internal Rate of Return and Net Present Value
- **Payback Period**: Regular and discounted payback periods
- **Loan Calculations**: EMI, amortization schedules
- **Investment Comparison**: Compare multiple investment options
- **Inflation Adjustments**: Real returns adjusted for inflation
- **Depreciation**: Straight-line and declining balance methods

## Installation

No installation required! This is a zero-dependency library. Just copy the `investment_utils.py` file to your project.

## Quick Start

```python
from investment_utils import (
    compound_interest,
    sip_returns,
    cagr,
    roi,
    loan_payment,
    amortization_schedule
)

# Compound Interest
result = compound_interest(10000, 0.08, 5)
print(f"Maturity: ${result.total_amount:,.2f}")
# Output: Maturity: $14,898.46

# SIP Returns
sip = sip_returns(10000, 0.12, 10)  # 10000/month, 12% return, 10 years
print(f"Total Invested: ${sip.total_invested:,.2f}")
print(f"Maturity Value: ${sip.maturity_value:,.2f}")
print(f"Returns: ${sip.total_returns:,.2f}")

# CAGR
growth = cagr(10000, 20000, 5)
print(f"CAGR: {growth * 100:.2f}%")
# Output: CAGR: 14.87%

# Loan EMI
emi = loan_payment(100000, 0.06, 30)  # 100k, 6%, 30 years
print(f"Monthly EMI: ${emi:,.2f}")
# Output: Monthly EMI: $599.55
```

## Detailed Usage

### Compound Interest

```python
from investment_utils import compound_interest, compound_interest_continuous

# Monthly compounding (default)
result = compound_interest(10000, 0.08, 5)
print(f"Amount: ${result.total_amount:,.2f}")
print(f"Interest: ${result.total_interest:,.2f}")
print(f"Effective Rate: {result.effective_rate * 100:.2f}%")

# Annual compounding
result = compound_interest(10000, 0.08, 5, n=1)

# Quarterly compounding
result = compound_interest(10000, 0.08, 5, n=4)

# Continuous compounding
result = compound_interest_continuous(10000, 0.08, 5)
```

### SIP (Systematic Investment Plan)

```python
from investment_utils import sip_returns, sip_step_up

# Regular SIP
sip = sip_returns(10000, 0.12, 10)
print(f"Total Invested: ${sip.total_invested:,.2f}")
print(f"Maturity: ${sip.maturity_value:,.2f}")

# Step-up SIP (10% increase each year)
step_up = sip_step_up(10000, 0.10, 0.12, 10)
print(f"Total Invested: ${step_up['total_invested']:,.2f}")
print(f"Maturity: ${step_up['maturity_value']:,.2f}")
for year in step_up['yearly_breakdown']:
    print(f"Year {year['year']}: ${year['monthly_investment']:,.2f}/month")
```

### CAGR (Compound Annual Growth Rate)

```python
from investment_utils import cagr, cagr_from_returns

# From start and end values
growth = cagr(10000, 25000, 5)
print(f"CAGR: {growth * 100:.2f}%")

# From list of annual returns
returns = [0.10, 0.15, -0.05, 0.20, 0.08]
avg_growth = cagr_from_returns(returns)
print(f"Average CAGR: {avg_growth * 100:.2f}%")
```

### Present and Future Value

```python
from investment_utils import present_value, future_value, present_value_annuity

# Present value of future amount
pv = present_value(100000, 0.08, 5)
print(f"Present Value: ${pv:,.2f}")

# Future value of present amount
fv = future_value(10000, 0.08, 5)
print(f"Future Value: ${fv:,.2f}")

# Present value of annuity (series of payments)
pva = present_value_annuity(1000, 0.05, 10)
print(f"PV of Annuity: ${pva:,.2f}")
```

### ROI (Return on Investment)

```python
from investment_utils import roi, annualized_roi

# Basic ROI
return_rate = roi(10000, 15000)
print(f"ROI: {return_rate * 100:.2f}%")

# Annualized ROI (for 180 days)
ann_roi = annualized_roi(10000, 12000, 180)
print(f"Annualized ROI: {ann_roi * 100:.2f}%")
```

### IRR and NPV

```python
from investment_utils import irr, npv

# Internal Rate of Return
cash_flows = [-1000, 300, 300, 300, 300, 300]
rate = irr(cash_flows)
print(f"IRR: {rate * 100:.2f}%")

# Net Present Value
npv_value = npv([-1000, 300, 300, 300, 300, 300], 0.10)
print(f"NPV: ${npv_value:,.2f}")
```

### Payback Period

```python
from investment_utils import payback_period, discounted_payback_period

# Regular payback period
period = payback_period(1000, [200, 300, 400, 200])
print(f"Payback Period: {period} years")

# Discounted payback period
dpp = discounted_payback_period(1000, [300, 400, 400, 200], 0.10)
print(f"Discounted Payback: {dpp} years")
```

### Loan Calculations

```python
from investment_utils import loan_payment, amortization_schedule

# Monthly EMI
emi = loan_payment(100000, 0.06, 30)
print(f"Monthly Payment: ${emi:,.2f}")

# Full amortization schedule
schedule = amortization_schedule(100000, 0.06, 30)
print(f"{'Period':<8} {'Payment':<12} {'Principal':<12} {'Interest':<12} {'Balance':<12}")
for entry in schedule[:5]:  # First 5 months
    print(f"{entry.period:<8} ${entry.payment:<11,.2f} ${entry.principal:<11,.2f} ${entry.interest:<11,.2f} ${entry.balance:<11,.2f}")
```

### Investment Comparison

```python
from investment_utils import compare_investments

investments = [
    {'name': 'Stock A', 'initial': 10000, 'final': 15000, 'years': 3},
    {'name': 'Stock B', 'initial': 10000, 'final': 14000, 'years': 2},
    {'name': 'Bond', 'initial': 10000, 'final': 12000, 'years': 5}
]

result = compare_investments(investments)
print(f"Best Investment: {result['winner']['name']}")
print(f"CAGR: {result['winner']['cagr_percent']:.2f}%")

print("\nRankings:")
for inv in result['rankings']:
    print(f"{inv['name']}: ROI={inv['roi_percent']:.1f}%, CAGR={inv['cagr_percent']:.1f}%")
```

### Inflation Adjustments

```python
from investment_utils import inflation_adjusted_return, future_value_with_inflation

# Real return after inflation
nominal = 0.10  # 10% nominal return
inflation = 0.03  # 3% inflation
real = inflation_adjusted_return(nominal, inflation)
print(f"Real Return: {real * 100:.2f}%")

# Future value with inflation impact
result = future_value_with_inflation(10000, 0.10, 0.03, 10)
print(f"Nominal Value: ${result['nominal_value']:,.2f}")
print(f"Real Value: ${result['real_value']:,.2f}")
print(f"Purchasing Power: {result['purchasing_power']:.2f}x")
```

### Quick Rules

```python
from investment_utils import rule_of_72, rule_of_69

# Rule of 72 - Quick estimate
years = rule_of_72(0.08)  # 8% return
print(f"Years to double (approx): {years}")

# Rule of 69 - More precise
years = rule_of_69(0.08)
print(f"Years to double (precise): {years:.2f}")
```

### Time Calculations

```python
from investment_utils import time_to_target, required_rate

# Time to reach target
years = time_to_target(10000, 20000, 0.08)
print(f"Years to double at 8%: {years:.1f}")

# Required rate to reach target
rate = required_rate(10000, 50000, 10)
print(f"Required rate: {rate * 100:.2f}%")
```

### Depreciation

```python
from investment_utils import straight_line_depreciation, declining_balance_depreciation

# Straight-line depreciation
sl = straight_line_depreciation(10000, 1000, 5)
print(f"Annual Depreciation: ${sl['annual_depreciation']:,.2f}")
for entry in sl['schedule']:
    print(f"Year {entry['year']}: Book Value = ${entry['book_value']:,.2f}")

# Declining balance (double declining)
db = declining_balance_depreciation(10000, 1000, 5)
for entry in db:
    print(f"Year {entry['year']}: Depreciation = ${entry['depreciation']:,.2f}")
```

## API Reference

### Compound Interest Functions

| Function | Description |
|----------|-------------|
| `compound_interest(principal, rate, time, n=12)` | Calculate compound interest |
| `compound_interest_continuous(principal, rate, time)` | Continuous compounding |
| `simple_interest(principal, rate, time)` | Simple interest |

### SIP Functions

| Function | Description |
|----------|-------------|
| `sip_returns(monthly, rate, years)` | Regular SIP returns |
| `sip_step_up(initial, step_up, rate, years)` | Step-up SIP |

### CAGR Functions

| Function | Description |
|----------|-------------|
| `cagr(beginning, ending, years)` | Calculate CAGR |
| `cagr_from_returns(returns)` | CAGR from return list |

### Time Value Functions

| Function | Description |
|----------|-------------|
| `present_value(future, rate, periods)` | Present value |
| `future_value(present, rate, periods)` | Future value |
| `present_value_annuity(payment, rate, periods)` | PV of annuity |

### ROI Functions

| Function | Description |
|----------|-------------|
| `roi(initial, final)` | Basic ROI |
| `annualized_roi(initial, final, days)` | Annualized ROI |

### IRR/NPV Functions

| Function | Description |
|----------|-------------|
| `irr(cash_flows, guess=0.1)` | Internal rate of return |
| `npv(cash_flows, rate)` | Net present value |

### Payback Functions

| Function | Description |
|----------|-------------|
| `payback_period(investment, cash_flows)` | Regular payback |
| `discounted_payback_period(investment, cash_flows, rate)` | Discounted payback |

### Loan Functions

| Function | Description |
|----------|-------------|
| `loan_payment(principal, rate, years)` | Monthly payment |
| `amortization_schedule(principal, rate, years)` | Full schedule |

### Comparison Functions

| Function | Description |
|----------|-------------|
| `compare_investments(investments)` | Compare multiple investments |
| `inflation_adjusted_return(nominal, inflation)` | Real return |
| `future_value_with_inflation(present, nominal, inflation, years)` | Inflation-adjusted FV |

### Quick Rules

| Function | Description |
|----------|-------------|
| `rule_of_72(rate)` | Years to double (approx) |
| `rule_of_69(rate, continuous=False)` | Years to double (precise) |

### Time Functions

| Function | Description |
|----------|-------------|
| `time_to_target(present, target, rate)` | Years to reach target |
| `required_rate(present, target, years)` | Required growth rate |

### Depreciation Functions

| Function | Description |
|----------|-------------|
| `straight_line_depreciation(cost, salvage, life)` | Straight-line method |
| `declining_balance_depreciation(cost, salvage, life, rate=None)` | Declining balance method |

## Running Tests

```bash
# Using unittest
python -m pytest investment_utils_test.py -v

# Or directly
python investment_utils_test.py
```

## License

MIT License - Free to use for any purpose.
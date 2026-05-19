# Compound Interest Utilities

A zero-dependency, production-ready compound interest calculation module for Python.

## Features

- **Basic Compound Interest**: Calculate amounts and interest with various compounding frequencies
- **Continuous Compounding**: Support for continuous (e²) compounding
- **Rate Conversions**: Convert between nominal and effective rates, APR to APY
- **Doubling Time**: Calculate time to double, triple, or quadruple investments
- **Required Calculations**: Find required rate or principal to reach targets
- **Growth Schedules**: Generate detailed compound interest schedules
- **Regular Contributions**: Handle recurring investments
- **Inflation Adjustment**: Calculate real returns and purchasing power
- **Comparisons**: Compare different rates and compounding frequencies
- **Goal Analysis**: Analyze savings goals and required contributions

## Installation

No external dependencies! Uses only Python standard library.

```python
from compound_interest_utils.mod import *
```

## Quick Start

### Basic Compound Interest

```python
# Calculate final amount
amount = compound_amount(1000, 0.05, 10, 12)  # $1647.01

# Calculate interest earned
interest = compound_interest(1000, 0.05, 10, 12)  # $647.01

# Continuous compounding
amount = continuous_compound_amount(1000, 0.05, 10)  # $1648.72
```

### Rate Conversions

```python
# Convert nominal rate to effective annual rate (EAR)
ear = effective_annual_rate(0.12, 12)  # ~12.68%

# Convert EAR to nominal rate
nominal = nominal_rate_from_ear(0.1268, 12)  # ~12%

# Calculate APY
apy = annual_percentage_yield(0.12, 12)  # ~12.68%
```

### Doubling Time

```python
# Exact doubling time
time = doubling_time(0.07, 12)  # ~9.93 years

# Rule of 72 approximation
time = doubling_time_rule72(0.07)  # ~10.29 years

# Time to triple or quadruple
triple_time = tripling_time(0.07, 12)  # ~15.7 years
quad_time = quadrupling_time(0.07, 12)  # ~19.86 years
```

### Growth Schedules

```python
# Generate full schedule
schedule = compound_schedule(1000, 0.05, 1, 12)
for period in schedule:
    print(f"Period {period['period']}: ${period['ending_balance']:.2f}")

# Annual summary
annual = annual_compound_schedule(1000, 0.05, 5, 12)

# Formatted table
table = compound_interest_table(1000, 0.05, 5, 12)
print(table)
```

### Regular Contributions

```python
# Future value with monthly contributions
fv = future_value_with_contributions(1000, 0.07, 10, 100, 12)  # ~$19,596

# Required contribution to reach goal
contrib = required_contribution(100000, 10000, 0.07, 20, 12)  # ~$155/month
```

### Inflation Adjustment

```python
# Calculate real rate
real = real_rate(0.08, 0.03)  # ~4.85%

# Inflation-adjusted future value
real_value = inflation_adjusted_amount(1000, 0.08, 0.03, 10, 12)
```

### Comparisons

```python
# Compare compounding frequencies
results = compare_compounding_frequencies(1000, 0.05, 10)
# Returns: annually, semiannually, quarterly, monthly, daily, continuous

# Compare different rates
rates = compare_rates(1000, [0.03, 0.05, 0.07], 10, 12)
```

### Investment Summary

```python
# Comprehensive analysis
summary = investment_summary(
    principal=1000,
    rate=0.07,
    years=10,
    compounds_per_year=12,
    contribution=100,  # Monthly contribution
    inflation_rate=0.03  # Optional
)

print(f"Final amount: ${summary['final_amount']:.2f}")
print(f"Total interest: ${summary['total_interest']:.2f}")
print(f"Doubling time: {summary['doubling_time_years']:.1f} years")
```

### Savings Goal Analysis

```python
# Analyze how to reach a goal
analysis = savings_goal_analysis(
    goal=100000,
    principal=10000,
    rate=0.07,
    years=20,
    compounds_per_year=12
)

print(f"Required monthly contribution: ${analysis['required_contribution_per_month']:.2f}")
print(f"On track: {analysis['on_track']}")
```

## API Reference

### Basic Calculations

| Function | Description |
|----------|-------------|
| `compound_amount(principal, rate, time, compounds_per_year)` | Calculate final amount |
| `compound_interest(principal, rate, time, compounds_per_year)` | Calculate total interest |
| `continuous_compound_amount(principal, rate, time)` | Continuous compounding |
| `continuous_compound_interest(principal, rate, time)` | Interest with continuous compounding |

### Rate Conversions

| Function | Description |
|----------|-------------|
| `effective_annual_rate(nominal_rate, compounds_per_year)` | Convert to EAR |
| `nominal_rate_from_ear(ear, compounds_per_year)` | Convert EAR to nominal |
| `equivalent_rate(rate, from_freq, to_freq)` | Convert between frequencies |
| `annual_percentage_yield(nominal_rate, compounds_per_year)` | Calculate APY |

### Doubling Time

| Function | Description |
|----------|-------------|
| `doubling_time(rate, compounds_per_year)` | Exact doubling time |
| `doubling_time_rule72(rate)` | Rule of 72 estimate |
| `doubling_time_rule69(rate)` | Rule of 69 estimate |
| `tripling_time(rate, compounds_per_year)` | Time to triple |
| `quadrupling_time(rate, compounds_per_year)` | Time to quadruple |
| `time_to_reach_target(principal, target, rate, compounds_per_year)` | Custom target |

### Required Calculations

| Function | Description |
|----------|-------------|
| `required_rate(principal, target, time, compounds_per_year)` | Rate needed for target |
| `required_principal(target, rate, time, compounds_per_year)` | Principal needed |
| `required_contribution(target, principal, rate, years, compounds_per_year)` | Contribution needed |

### Schedules

| Function | Description |
|----------|-------------|
| `compound_schedule(principal, rate, years, compounds_per_year, contributions)` | Full schedule |
| `annual_compound_schedule(principal, rate, years, compounds_per_year, contributions)` | Annual summary |
| `compound_interest_table(principal, rate, years, compounds_per_year)` | Formatted table |

### Inflation

| Function | Description |
|----------|-------------|
| `real_rate(nominal_rate, inflation_rate)` | Real rate after inflation |
| `inflation_adjusted_amount(principal, nominal_rate, inflation_rate, time, compounds_per_year)` | Real future value |
| `purchasing_power(principal, inflation_rate, time)` | Purchasing power without investment |

### Helpers

| Function | Description |
|----------|-------------|
| `investment_summary(...)` | Comprehensive investment analysis |
| `savings_goal_analysis(...)` | Analyze savings goal |
| `compare_compounding_frequencies(principal, rate, time)` | Compare frequencies |
| `compare_rates(principal, rates, time, compounds_per_year)` | Compare rates |
| `get_compounding_frequency(name)` | Get frequency by name |

## Compounding Frequencies

Common frequencies available:

- `annual` / `annually` (1)
- `semiannual` / `semiannually` (2)
- `quarterly` (4)
- `monthly` (12)
- `weekly` (52)
- `daily` (365)
- `continuous` (None - special handling)

## Examples

### Example 1: Compare Investment Returns

```python
# $10,000 invested at different rates for 10 years
comparison = compare_rates(10000, [0.03, 0.05, 0.07, 0.10], 10, 12)

for rate, data in comparison.items():
    print(f"{rate*100:.0f}%: ${data['amount']:.2f} (Interest: ${data['interest']:.2f})")
```

### Example 2: Retirement Planning

```python
# Goal: $500,000 in 30 years with $50,000 initial investment
analysis = savings_goal_analysis(
    goal=500000,
    principal=50000,
    rate=0.07,
    years=30,
    compounds_per_year=12
)

print(f"Monthly contribution needed: ${analysis['required_contribution_per_month']:.2f}")
```

### Example 3: Real Returns After Inflation

```python
summary = investment_summary(
    principal=10000,
    rate=0.08,
    years=20,
    compounds_per_year=12,
    inflation_rate=0.03
)

print(f"Nominal final: ${summary['final_amount']:.2f}")
print(f"Real final (today's dollars): ${summary['real_final_value']:.2f}")
print(f"Purchasing power lost: ${summary['purchasing_power_loss']:.2f}")
```

## License

MIT License - Free for personal and commercial use.

## Author

AllToolkit
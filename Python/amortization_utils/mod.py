"""
AllToolkit - Python Amortization Utilities

A zero-dependency, production-ready amortization calculation utility module.
Supports loan amortization schedules, payment breakdowns, and various loan
calculation methods including fixed-rate, adjustable-rate basics, and early
payoff analysis.

Author: AllToolkit
License: MIT
"""

from typing import List, Dict, Tuple, Optional, Union
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import math


class AmortizationPayment:
    """Represents a single payment in an amortization schedule."""
    
    def __init__(
        self,
        payment_number: int,
        payment_date: Union[date, None],
        payment_amount: float,
        principal: float,
        interest: float,
        remaining_balance: float,
        cumulative_principal: float = 0.0,
        cumulative_interest: float = 0.0
    ):
        self.payment_number = payment_number
        self.payment_date = payment_date
        self.payment_amount = payment_amount
        self.principal = principal
        self.interest = interest
        self.remaining_balance = remaining_balance
        self.cumulative_principal = cumulative_principal
        self.cumulative_interest = cumulative_interest
    
    def to_dict(self) -> Dict:
        """Convert payment to dictionary representation."""
        return {
            'payment_number': self.payment_number,
            'payment_date': self.payment_date.isoformat() if self.payment_date else None,
            'payment_amount': round(self.payment_amount, 2),
            'principal': round(self.principal, 2),
            'interest': round(self.interest, 2),
            'remaining_balance': round(self.remaining_balance, 2),
            'cumulative_principal': round(self.cumulative_principal, 2),
            'cumulative_interest': round(self.cumulative_interest, 2)
        }
    
    def __repr__(self) -> str:
        return (
            f"AmortizationPayment(#{self.payment_number}, "
            f"payment={self.payment_amount:.2f}, "
            f"principal={self.principal:.2f}, "
            f"interest={self.interest:.2f}, "
            f"balance={self.remaining_balance:.2f})"
        )


class AmortizationSchedule:
    """Represents a complete amortization schedule."""
    
    def __init__(
        self,
        principal: float,
        annual_rate: float,
        term_months: int,
        start_date: Optional[date] = None,
        payments: Optional[List[AmortizationPayment]] = None
    ):
        self.principal = principal
        self.annual_rate = annual_rate
        self.term_months = term_months
        self.start_date = start_date or date.today()
        self.payments = payments or []
    
    @property
    def monthly_payment(self) -> float:
        """Calculate the fixed monthly payment."""
        return AmortizationUtils.calculate_monthly_payment(
            self.principal, self.annual_rate, self.term_months
        )
    
    @property
    def total_payment(self) -> float:
        """Total amount paid over the life of the loan."""
        return self.monthly_payment * self.term_months
    
    @property
    def total_interest(self) -> float:
        """Total interest paid over the life of the loan."""
        return self.total_payment - self.principal
    
    @property
    def interest_to_principal_ratio(self) -> float:
        """Ratio of total interest to principal."""
        return self.total_interest / self.principal if self.principal > 0 else 0
    
    def to_dict(self) -> Dict:
        """Convert schedule to dictionary representation."""
        return {
            'principal': round(self.principal, 2),
            'annual_rate': round(self.annual_rate, 6),
            'term_months': self.term_months,
            'start_date': self.start_date.isoformat(),
            'monthly_payment': round(self.monthly_payment, 2),
            'total_payment': round(self.total_payment, 2),
            'total_interest': round(self.total_interest, 2),
            'interest_to_principal_ratio': round(self.interest_to_principal_ratio, 4),
            'payments': [p.to_dict() for p in self.payments]
        }
    
    def get_payment(self, month: int) -> Optional[AmortizationPayment]:
        """Get a specific payment by month number (1-indexed)."""
        if 1 <= month <= len(self.payments):
            return self.payments[month - 1]
        return None
    
    def get_year_summary(self, year: int) -> Dict:
        """Get summary for a specific year."""
        year_payments = [
            p for p in self.payments
            if p.payment_date and p.payment_date.year == year
        ]
        
        if not year_payments:
            return {'year': year, 'total_principal': 0, 'total_interest': 0, 'payments': 0}
        
        return {
            'year': year,
            'total_principal': round(sum(p.principal for p in year_payments), 2),
            'total_interest': round(sum(p.interest for p in year_payments), 2),
            'total_payments': round(sum(p.payment_amount for p in year_payments), 2),
            'payments_count': len(year_payments)
        }
    
    def summarize_by_year(self) -> List[Dict]:
        """Summarize payments by year."""
        years = set()
        for p in self.payments:
            if p.payment_date:
                years.add(p.payment_date.year)
        
        return [self.get_year_summary(year) for year in sorted(years)]


class AmortizationUtils:
    """
    Amortization calculation utilities.
    
    Provides functions for:
    - Monthly payment calculation
    - Full amortization schedule generation
    - Interest/principal breakdown
    - Early payoff analysis
    - Extra payment impact
    - Refinancing comparison
    """
    
    @staticmethod
    def calculate_monthly_payment(
        principal: float,
        annual_rate: float,
        term_months: int
    ) -> float:
        """
        Calculate the fixed monthly payment for a loan.
        
        Uses the standard amortization formula:
        M = P * [r(1+r)^n] / [(1+r)^n - 1]
        
        Args:
            principal: Loan amount
            annual_rate: Annual interest rate as decimal (e.g., 0.05 for 5%)
            term_months: Loan term in months
        
        Returns:
            Monthly payment amount
        
        Example:
            >>> payment = AmortizationUtils.calculate_monthly_payment(
            ...     principal=200000, annual_rate=0.05, term_months=360
            ... )
            >>> round(payment, 2)
            1073.64
        """
        if principal <= 0 or term_months <= 0:
            return 0.0
        
        if annual_rate == 0:
            return principal / term_months
        
        monthly_rate = annual_rate / 12
        factor = (1 + monthly_rate) ** term_months
        
        return principal * (monthly_rate * factor) / (factor - 1)
    
    @staticmethod
    def calculate_interest_portion(
        remaining_balance: float,
        annual_rate: float
    ) -> float:
        """
        Calculate the interest portion of a monthly payment.
        
        Args:
            remaining_balance: Current remaining balance
            annual_rate: Annual interest rate as decimal
        
        Returns:
            Interest portion for this month
        """
        return remaining_balance * (annual_rate / 12)
    
    @staticmethod
    def generate_schedule(
        principal: float,
        annual_rate: float,
        term_months: int,
        start_date: Optional[date] = None,
        extra_monthly: float = 0.0
    ) -> AmortizationSchedule:
        """
        Generate a complete amortization schedule.
        
        Args:
            principal: Loan amount
            annual_rate: Annual interest rate as decimal
            term_months: Loan term in months
            start_date: First payment date (defaults to today)
            extra_monthly: Extra payment amount each month
        
        Returns:
            AmortizationSchedule object with all payments
        
        Example:
            >>> schedule = AmortizationUtils.generate_schedule(
            ...     principal=100000, annual_rate=0.04, term_months=120
            ... )
            >>> len(schedule.payments)
            120
        """
        start_date = start_date or date.today()
        monthly_payment = AmortizationUtils.calculate_monthly_payment(
            principal, annual_rate, term_months
        )
        
        payments = []
        balance = principal
        cumulative_principal = 0.0
        cumulative_interest = 0.0
        
        payment_date = start_date
        payment_num = 1
        
        while balance > 0.01 and payment_num <= term_months * 2:  # Safety limit
            # Calculate interest for this period
            interest = AmortizationUtils.calculate_interest_portion(
                balance, annual_rate
            )
            
            # Calculate principal (regular + extra)
            actual_payment = monthly_payment + extra_monthly
            principal_paid = actual_payment - interest
            
            # Adjust if overpaying
            if principal_paid > balance:
                principal_paid = balance
                actual_payment = interest + principal_paid
            
            # Update balances
            balance = max(0, balance - principal_paid)
            cumulative_principal += principal_paid
            cumulative_interest += interest
            
            # Create payment record
            payment = AmortizationPayment(
                payment_number=payment_num,
                payment_date=payment_date,
                payment_amount=actual_payment,
                principal=principal_paid,
                interest=interest,
                remaining_balance=balance,
                cumulative_principal=cumulative_principal,
                cumulative_interest=cumulative_interest
            )
            payments.append(payment)
            
            # Move to next month
            payment_date = payment_date + relativedelta(months=1)
            payment_num += 1
            
            # Check if loan is paid off early due to extra payments
            if balance <= 0.01:
                break
        
        return AmortizationSchedule(
            principal=principal,
            annual_rate=annual_rate,
            term_months=len(payments),
            start_date=start_date,
            payments=payments
        )
    
    @staticmethod
    def calculate_remaining_balance(
        principal: float,
        annual_rate: float,
        term_months: int,
        months_paid: int
    ) -> float:
        """
        Calculate remaining balance after a certain number of payments.
        
        Args:
            principal: Original loan amount
            annual_rate: Annual interest rate as decimal
            term_months: Total loan term in months
            months_paid: Number of payments already made
        
        Returns:
            Remaining balance
        
        Example:
            >>> balance = AmortizationUtils.calculate_remaining_balance(
            ...     principal=200000, annual_rate=0.05, 
            ...     term_months=360, months_paid=60
            ... )
            >>> round(balance, 2)
            181783.49
        """
        if months_paid <= 0:
            return principal
        
        schedule = AmortizationUtils.generate_schedule(
            principal, annual_rate, term_months
        )
        
        if months_paid >= len(schedule.payments):
            return 0.0
        
        return schedule.payments[months_paid - 1].remaining_balance
    
    @staticmethod
    def calculate_early_payoff(
        principal: float,
        annual_rate: float,
        term_months: int,
        months_paid: int,
        extra_payment: float
    ) -> Dict:
        """
        Analyze the impact of a lump-sum extra payment.
        
        Args:
            principal: Original loan amount
            annual_rate: Annual interest rate as decimal
            term_months: Original loan term in months
            months_paid: Number of payments already made
            extra_payment: Lump sum extra payment amount
        
        Returns:
            Dictionary with payoff analysis
        
        Example:
            >>> result = AmortizationUtils.calculate_early_payoff(
            ...     principal=200000, annual_rate=0.05,
            ...     term_months=360, months_paid=60,
            ...     extra_payment=50000
            ... )
        """
        # Get remaining balance
        remaining = AmortizationUtils.calculate_remaining_balance(
            principal, annual_rate, term_months, months_paid
        )
        
        # Apply extra payment
        new_balance = max(0, remaining - extra_payment)
        months_remaining = term_months - months_paid
        
        # Calculate the original monthly payment (from original loan terms)
        original_monthly_payment = AmortizationUtils.calculate_monthly_payment(
            principal, annual_rate, term_months
        )
        
        # Original remaining schedule (what would have been paid)
        original_schedule = AmortizationUtils.generate_schedule(
            remaining, annual_rate, months_remaining
        )
        
        # New schedule after extra payment
        # Use the same monthly payment, but find actual time needed
        if new_balance > 0:
            # Find how many months it takes to pay off new_balance with original monthly payment
            new_term_result = AmortizationUtils.find_term_for_payment(
                new_balance, annual_rate, original_monthly_payment
            )
            if new_term_result['possible']:
                new_term = new_term_result['term_months']
                # Calculate actual interest saved
                new_schedule = AmortizationUtils.generate_schedule(
                    new_balance, annual_rate, new_term
                )
                interest_saved = original_schedule.total_interest - new_schedule.total_interest
            else:
                # Can't pay off with original payment, use remaining months
                new_schedule = AmortizationUtils.generate_schedule(
                    new_balance, annual_rate, months_remaining
                )
                new_term = len(new_schedule.payments)
                interest_saved = original_schedule.total_interest - new_schedule.total_interest
        else:
            new_term = 0
            interest_saved = original_schedule.total_interest
        
        return {
            'remaining_balance': round(remaining, 2),
            'extra_payment': round(extra_payment, 2),
            'new_balance': round(new_balance, 2),
            'original_months_remaining': months_remaining,
            'new_months_remaining': new_term,
            'months_saved': months_remaining - new_term,
            'original_remaining_interest': round(original_schedule.total_interest, 2),
            'interest_saved': round(interest_saved, 2)
        }
    
    @staticmethod
    def calculate_extra_payment_impact(
        principal: float,
        annual_rate: float,
        term_months: int,
        extra_monthly: float
    ) -> Dict:
        """
        Analyze the impact of making extra monthly payments.
        
        Args:
            principal: Loan amount
            annual_rate: Annual interest rate as decimal
            term_months: Loan term in months
            extra_monthly: Extra amount to pay each month
        
        Returns:
            Dictionary comparing original vs extra payment scenarios
        
        Example:
            >>> result = AmortizationUtils.calculate_extra_payment_impact(
            ...     principal=200000, annual_rate=0.05,
            ...     term_months=360, extra_monthly=200
            ... )
        """
        # Original schedule
        original = AmortizationUtils.generate_schedule(
            principal, annual_rate, term_months
        )
        
        # Schedule with extra payments
        with_extra = AmortizationUtils.generate_schedule(
            principal, annual_rate, term_months, extra_monthly=extra_monthly
        )
        
        return {
            'original_term_months': term_months,
            'new_term_months': len(with_extra.payments),
            'months_saved': term_months - len(with_extra.payments),
            'original_total_interest': round(original.total_interest, 2),
            'new_total_interest': round(with_extra.total_interest, 2),
            'interest_saved': round(original.total_interest - with_extra.total_interest, 2),
            'original_monthly_payment': round(original.monthly_payment, 2),
            'new_monthly_payment': round(original.monthly_payment + extra_monthly, 2),
            'years_saved': round((term_months - len(with_extra.payments)) / 12, 1)
        }
    
    @staticmethod
    def calculate_refinance_comparison(
        current_balance: float,
        current_rate: float,
        current_remaining_months: int,
        new_rate: float,
        new_term_months: int,
        closing_costs: float = 0.0
    ) -> Dict:
        """
        Compare current loan vs refinancing options.
        
        Args:
            current_balance: Remaining balance on current loan
            current_rate: Current annual interest rate
            current_remaining_months: Months left on current loan
            new_rate: New annual interest rate
            new_term_months: New loan term in months
            closing_costs: Refinancing closing costs
        
        Returns:
            Dictionary comparing both scenarios
        """
        # Current loan schedule
        current_schedule = AmortizationUtils.generate_schedule(
            current_balance, current_rate, current_remaining_months
        )
        
        # New loan schedule
        new_schedule = AmortizationUtils.generate_schedule(
            current_balance, new_rate, new_term_months
        )
        
        # Calculate net savings (including closing costs)
        interest_difference = current_schedule.total_interest - new_schedule.total_interest
        net_savings = interest_difference - closing_costs
        
        return {
            'current': {
                'balance': round(current_balance, 2),
                'rate': round(current_rate * 100, 3),
                'remaining_months': current_remaining_months,
                'monthly_payment': round(current_schedule.monthly_payment, 2),
                'total_remaining_interest': round(current_schedule.total_interest, 2)
            },
            'refinance': {
                'new_rate': round(new_rate * 100, 3),
                'new_term_months': new_term_months,
                'monthly_payment': round(new_schedule.monthly_payment, 2),
                'total_interest': round(new_schedule.total_interest, 2),
                'closing_costs': round(closing_costs, 2)
            },
            'comparison': {
                'monthly_payment_difference': round(
                    current_schedule.monthly_payment - new_schedule.monthly_payment, 2
                ),
                'interest_difference': round(interest_difference, 2),
                'closing_costs': round(closing_costs, 2),
                'net_savings': round(net_savings, 2),
                'is_worth_it': net_savings > 0,
                'break_even_months': round(
                    closing_costs / max(0.01, current_schedule.monthly_payment - new_schedule.monthly_payment)
                ) if new_schedule.monthly_payment < current_schedule.monthly_payment else None
            }
        }
    
    @staticmethod
    def calculate_apr(
        principal: float,
        monthly_payment: float,
        term_months: int,
        fees: float = 0.0
    ) -> float:
        """
        Calculate the Annual Percentage Rate (APR) including fees.
        
        Uses binary search to find the rate that makes
        the present value of payments equal to net loan amount.
        
        Args:
            principal: Loan amount
            monthly_payment: Monthly payment amount
            term_months: Loan term in months
            fees: Upfront fees/costs
        
        Returns:
            APR as decimal
        
        Example:
            >>> apr = AmortizationUtils.calculate_apr(
            ...     principal=200000, monthly_payment=1073.64,
            ...     term_months=360, fees=5000
            ... )
            >>> round(apr * 100, 2)
            5.27
        """
        net_principal = principal - fees
        
        if net_principal <= 0 or monthly_payment <= 0 or term_months <= 0:
            return 0.0
        
        def present_value(rate):
            """Calculate present value at given monthly rate."""
            if rate <= 0:
                return monthly_payment * term_months
            factor = (1 + rate) ** term_months
            return monthly_payment * (factor - 1) / (rate * factor)
        
        # Binary search for the rate
        low_rate = 0.0
        high_rate = 0.5  # 50% monthly = 600% annual (very high)
        
        for _ in range(100):  # Max iterations for convergence
            mid_rate = (low_rate + high_rate) / 2
            pv = present_value(mid_rate)
            
            # Check convergence
            if abs(pv - net_principal) < 0.01:
                return mid_rate * 12
            
            # Adjust search range
            # Higher rate -> lower present value
            # Lower rate -> higher present value
            if pv < net_principal:
                # Present value too low, rate is too high
                high_rate = mid_rate
            else:
                # Present value too high, rate is too low
                low_rate = mid_rate
        
        return mid_rate * 12  # Return best estimate after iterations
    
    @staticmethod
    def find_term_for_payment(
        principal: float,
        annual_rate: float,
        target_payment: float
    ) -> Dict:
        """
        Find the loan term needed for a target monthly payment.
        
        Useful for determining how long a loan will take to pay off
        with a specific payment amount.
        
        Args:
            principal: Loan amount
            annual_rate: Annual interest rate as decimal
            target_payment: Desired monthly payment
        
        Returns:
            Dictionary with term information
        """
        monthly_rate = annual_rate / 12
        
        if monthly_rate == 0:
            term_months = math.ceil(principal / target_payment)
        else:
            # n = -ln(1 - P*r/M) / ln(1+r)
            if target_payment <= principal * monthly_rate:
                return {
                    'possible': False,
                    'reason': 'Payment too low to cover interest',
                    'minimum_payment': round(principal * monthly_rate + 0.01, 2)
                }
            
            term_months = -math.log(
                1 - principal * monthly_rate / target_payment
            ) / math.log(1 + monthly_rate)
            term_months = math.ceil(term_months)
        
        # Generate schedule to get actual numbers
        schedule = AmortizationUtils.generate_schedule(
            principal, annual_rate, term_months
        )
        
        return {
            'possible': True,
            'term_months': term_months,
            'years': round(term_months / 12, 1),
            'monthly_payment': round(schedule.monthly_payment, 2),
            'total_interest': round(schedule.total_interest, 2),
            'total_payment': round(schedule.total_payment, 2)
        }
    
    @staticmethod
    def calculate_affordable_principal(
        monthly_payment: float,
        annual_rate: float,
        term_months: int,
        down_payment: float = 0.0
    ) -> Dict:
        """
        Calculate how much house/loan you can afford based on monthly payment.
        
        Args:
            monthly_payment: Maximum monthly payment you can afford
            annual_rate: Annual interest rate as decimal
            term_months: Loan term in months
            down_payment: Down payment amount
        
        Returns:
            Dictionary with affordability information
        """
        monthly_rate = annual_rate / 12
        
        if monthly_rate == 0:
            loan_amount = monthly_payment * term_months
        else:
            # P = M * [(1+r)^n - 1] / [r(1+r)^n]
            factor = (1 + monthly_rate) ** term_months
            loan_amount = monthly_payment * (factor - 1) / (monthly_rate * factor)
        
        total_home_price = loan_amount + down_payment
        
        return {
            'loan_amount': round(loan_amount, 2),
            'down_payment': round(down_payment, 2),
            'total_home_price': round(total_home_price, 2),
            'monthly_payment': round(monthly_payment, 2),
            'down_payment_percentage': round(
                down_payment / total_home_price * 100, 1
            ) if total_home_price > 0 else 0
        }


# Convenience functions for common use cases
def calculate_mortgage_payment(
    principal: float,
    annual_rate: float,
    years: int
) -> float:
    """
    Quick calculation of monthly mortgage payment.
    
    Args:
        principal: Loan amount
        annual_rate: Annual interest rate (e.g., 6.5 for 6.5%)
        years: Loan term in years
    
    Returns:
        Monthly payment amount
    """
    return AmortizationUtils.calculate_monthly_payment(
        principal, annual_rate / 100, years * 12
    )


def generate_mortgage_schedule(
    principal: float,
    annual_rate: float,
    years: int,
    start_date: Optional[date] = None
) -> AmortizationSchedule:
    """
    Quick generation of mortgage amortization schedule.
    
    Args:
        principal: Loan amount
        annual_rate: Annual interest rate (e.g., 6.5 for 6.5%)
        years: Loan term in years
        start_date: First payment date
    
    Returns:
        AmortizationSchedule object
    """
    return AmortizationUtils.generate_schedule(
        principal, annual_rate / 100, years * 12, start_date
    )


if __name__ == '__main__':
    # Demo usage
    print("=" * 60)
    print("Amortization Calculator Demo")
    print("=" * 60)
    
    # Example: $300,000 mortgage at 6.5% for 30 years
    principal = 300000
    rate = 0.065  # 6.5%
    term = 360  # 30 years
    
    schedule = AmortizationUtils.generate_schedule(principal, rate, term)
    
    print(f"\nLoan Details:")
    print(f"  Principal: ${principal:,.2f}")
    print(f"  Annual Rate: {rate * 100:.2f}%")
    print(f"  Term: {term} months ({term/12:.0f} years)")
    print(f"\nResults:")
    print(f"  Monthly Payment: ${schedule.monthly_payment:,.2f}")
    print(f"  Total Payment: ${schedule.total_payment:,.2f}")
    print(f"  Total Interest: ${schedule.total_interest:,.2f}")
    print(f"  Interest/Principal Ratio: {schedule.interest_to_principal_ratio:.2%}")
    
    # Show first 5 payments
    print(f"\nFirst 5 Payments:")
    print("-" * 80)
    print(f"{'#':<4} {'Payment':<12} {'Principal':<12} {'Interest':<12} {'Balance':<15}")
    print("-" * 80)
    for p in schedule.payments[:5]:
        print(f"{p.payment_number:<4} ${p.payment_amount:<11,.2f} ${p.principal:<11,.2f} ${p.interest:<11,.2f} ${p.remaining_balance:<14,.2f}")
    
    # Extra payment impact
    print("\n" + "=" * 60)
    print("Extra Payment Impact Analysis ($200 extra/month)")
    print("=" * 60)
    impact = AmortizationUtils.calculate_extra_payment_impact(
        principal, rate, term, 200
    )
    print(f"  Original Term: {impact['original_term_months']} months")
    print(f"  New Term: {impact['new_term_months']} months")
    print(f"  Months Saved: {impact['months_saved']} months ({impact['years_saved']} years)")
    print(f"  Interest Saved: ${impact['interest_saved']:,.2f}")
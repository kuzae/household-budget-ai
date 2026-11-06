
"""
Financial calculation engine.

All monetary calculations are performed here rather
than delegated to the language model.

Amounts are represented as Decimal to avoid
floating-point precision errors.
"""

from decimal import Decimal, ROUND_HALF_UP
from typing import Iterable


# --------------------------------------------------
# Monetary utilities
# --------------------------------------------------

CENT = Decimal("0.01")

def money(value) -> Decimal:
    """
    Convert a value into a monetary Decimal.
    """
    return Decimal(str(value)).quantize(
        CENT,
        rounding=ROUND_HALF_UP
    )


def monthly_amount(amount, frequency: str) -> Decimal:
    """
    Convert income or expenses into monthly equivalents.

    Supported frequencies:
        weekly
        biweekly
        semimonthly
        monthly
        quarterly
        annually
    """

    amount = Decimal(str(amount))

    multipliers = {
        "weekly": Decimal("52") / Decimal("12"),
        "biweekly": Decimal("26") / Decimal("12"),
        "semimonthly": Decimal("2"),
        "monthly": Decimal("1"),
        "quarterly": Decimal("1") / Decimal("3"),
        "annually": Decimal("1") / Decimal("12"),
    }

    frequency = frequency.lower()

    if frequency not in multipliers:
        raise ValueError(
            f"Unsupported frequency: {frequency}"
        )

    return money(amount * multipliers[frequency])


# --------------------------------------------------
# Income calculations
# --------------------------------------------------

def calculate_total_income(incomes: Iterable[dict]) -> Decimal:
    """
    Calculate total normalized monthly income.

    Each income entry requires:
        amount
        frequency
    """

    total = Decimal("0")

    for income in incomes:
        total += monthly_amount(
            income["amount"],
            income["frequency"]
        )

    return money(total)


# --------------------------------------------------
# Expense calculations
# --------------------------------------------------

def calculate_total_expenses(
    expenses: Iterable[dict]
) -> Decimal:
    """
    Calculate total normalized monthly expenses.
    """

    total = Decimal("0")

    for expense in expenses:
        total += monthly_amount(
            expense["amount"],
            expense["frequency"]
        )

    return money(total)


# --------------------------------------------------
# Budget calculations
# --------------------------------------------------

def calculate_disposable_income(
    monthly_income,
    monthly_expenses
) -> Decimal:
    """
    Calculate income remaining after expenses.
    """

    return money(
        Decimal(str(monthly_income))
        - Decimal(str(monthly_expenses))
    )


def calculate_savings_rate(
    monthly_income,
    monthly_savings
) -> Decimal:
    """
    Calculate savings as a percentage of income.

    Returns zero when income is zero or negative.
    """

    income = Decimal(str(monthly_income))
    savings = Decimal(str(monthly_savings))

    if income <= 0:
        return Decimal("0.00")

    return (
        (savings / income) * Decimal("100")
    ).quantize(CENT, rounding=ROUND_HALF_UP)


def calculate_expense_ratio(
    monthly_income,
    monthly_expenses
) -> Decimal:
    """
    Calculate expenses as a percentage of income.
    """

    income = Decimal(str(monthly_income))
    expenses = Decimal(str(monthly_expenses))

    if income <= 0:
        return Decimal("0.00")

    return (
        (expenses / income) * Decimal("100")
    ).quantize(CENT, rounding=ROUND_HALF_UP)


# --------------------------------------------------
# Budget summary
# --------------------------------------------------

def generate_budget_summary(
    incomes: Iterable[dict],
    expenses: Iterable[dict],
    monthly_savings=0
) -> dict:
    """
    Generate a consolidated monthly budget summary.
    """

    total_income = calculate_total_income(incomes)

    total_expenses = calculate_total_expenses(expenses)

    savings = money(monthly_savings)

    remaining = calculate_disposable_income(
        total_income,
        total_expenses
    )

    remaining_after_savings = money(
        remaining - savings
    )

    return {
        "monthly_income": total_income,
        "monthly_expenses": total_expenses,
        "monthly_savings": savings,
        "disposable_income": remaining,
        "remaining_after_savings": remaining_after_savings,
        "savings_rate": calculate_savings_rate(
            total_income,
            savings
        ),
        "expense_ratio": calculate_expense_ratio(
            total_income,
            total_expenses
        ),
    }

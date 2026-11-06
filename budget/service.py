
from budget.calculations import (
    calculate_total_income,
    calculate_total_expenses,
    calculate_savings_rate,
    calculate_expense_ratio,
    calculate_disposable_income,
    money,
    monthly_amount,
)

from database.db import get_financial_records, get_household


def get_household_budget(household_id: int) -> dict:
    """
    Generate a complete monthly budget summary
    for a household.
    """

    household = get_household(household_id)

    if household is None:
        raise ValueError(f"Household {household_id} does not exist.")

    incomes = get_financial_records(household_id, "income")
    expenses = get_financial_records(household_id, "expenses")
    savings_records = get_financial_records(household_id, "savings")

    monthly_income = calculate_total_income(incomes)
    monthly_expenses = calculate_total_expenses(expenses)
    monthly_savings = calculate_total_income(savings_records)

    disposable_income = calculate_disposable_income(
        monthly_income,
        monthly_expenses,
    )

    remaining_after_savings = money(
        disposable_income - monthly_savings
    )

    return {
        "household": household["name"],
        "household_id": household_id,
        "monthly_income": monthly_income,
        "monthly_expenses": monthly_expenses,
        "monthly_savings": monthly_savings,
        "disposable_income": disposable_income,
        "remaining_after_savings": remaining_after_savings,
        "savings_rate": calculate_savings_rate(
            monthly_income,
            monthly_savings,
        ),
        "expense_ratio": calculate_expense_ratio(
            monthly_income,
            monthly_expenses,
        ),
        "income_records": incomes,
        "expense_records": expenses,
        "savings_records": savings_records,
    }


def get_expense_breakdown(household_id: int) -> dict:
    """Calculate monthly expenses grouped by category."""

    expenses = get_financial_records(household_id, "expenses")

    breakdown = {}

    for expense in expenses:
        category = expense["category"]

        monthly_value = money(
            expense["amount"]
        )


        monthly_value = monthly_amount(
            expense["amount"],
            expense["frequency"],
        )

        breakdown[category] = (
            breakdown.get(category, money(0)) + monthly_value
        )

    return dict(
        sorted(
            breakdown.items(),
            key=lambda item: item[1],
            reverse=True,
        )
    )


def get_monthly_cash_flow(household_id: int) -> dict:
    """Calculate monthly income, spending, and remaining cash."""

    budget = get_household_budget(household_id)

    return {
        "income": budget["monthly_income"],
        "expenses": budget["monthly_expenses"],
        "savings": budget["monthly_savings"],
        "remaining": budget["remaining_after_savings"],
    }


from decimal import Decimal

import pytest

from budget.calculations import (
    monthly_amount,
    calculate_total_income,
    calculate_total_expenses,
    calculate_disposable_income,
    calculate_savings_rate,
    generate_budget_summary,
)


def test_weekly_income_conversion():
    result = monthly_amount(1000, "weekly")

    assert result == Decimal("4333.33")


def test_monthly_income():
    incomes = [
        {"amount": 3000, "frequency": "monthly"},
        {"amount": 1000, "frequency": "weekly"},
    ]

    result = calculate_total_income(incomes)

    assert result == Decimal("7333.33")


def test_monthly_expenses():
    expenses = [
        {"amount": 1200, "frequency": "monthly"},
        {"amount": 100, "frequency": "weekly"},
    ]

    result = calculate_total_expenses(expenses)

    assert result == Decimal("1633.33")


def test_disposable_income():
    result = calculate_disposable_income(
        5000,
        3500
    )

    assert result == Decimal("1500.00")


def test_savings_rate():
    result = calculate_savings_rate(
        5000,
        1000
    )

    assert result == Decimal("20.00")


def test_zero_income_savings_rate():
    result = calculate_savings_rate(0, 100)

    assert result == Decimal("0.00")


def test_invalid_frequency():
    with pytest.raises(ValueError):
        monthly_amount(100, "daily")


def test_budget_summary():
    incomes = [
        {"amount": 5000, "frequency": "monthly"}
    ]

    expenses = [
        {"amount": 3000, "frequency": "monthly"}
    ]

    result = generate_budget_summary(
        incomes,
        expenses,
        monthly_savings=500
    )

    assert result["monthly_income"] == Decimal("5000.00")
    assert result["monthly_expenses"] == Decimal("3000.00")
    assert result["disposable_income"] == Decimal("2000.00")
    assert result["remaining_after_savings"] == Decimal("1500.00")
    assert result["savings_rate"] == Decimal("10.00")

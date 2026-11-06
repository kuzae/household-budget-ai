
import pytest
from decimal import Decimal

import database.db as db

from budget.service import (
    get_household_budget,
    get_expense_breakdown,
    get_monthly_cash_flow,
)


@pytest.fixture
def test_database(tmp_path, monkeypatch):
    database_path = tmp_path / "test_budget.db"

    monkeypatch.setattr(db, "DATABASE_PATH", database_path)
    monkeypatch.setattr(db, "DATA_DIR", tmp_path)

    db.initialize_database()

    return database_path


def test_household_budget_summary(test_database):
    household_id = db.create_household("Test Household")

    db.add_income(
        household_id, "Employment", 5000, "monthly"
    )

    db.add_expense(
        household_id, "Rent", "Housing", 1500, "monthly"
    )

    db.add_expense(
        household_id, "Groceries", "Groceries", 500, "monthly"
    )

    db.add_savings(
        household_id, "Emergency Fund", 500, "monthly"
    )

    budget = get_household_budget(household_id)

    assert budget["monthly_income"] == Decimal("5000.00")
    assert budget["monthly_expenses"] == Decimal("2000.00")
    assert budget["monthly_savings"] == Decimal("500.00")
    assert budget["remaining_after_savings"] == Decimal("2500.00")


def test_expense_breakdown(test_database):
    household_id = db.create_household("Test Household")

    db.add_expense(
        household_id, "Rent", "Housing", 1500, "monthly"
    )

    db.add_expense(
        household_id, "Groceries", "Groceries", 100, "weekly"
    )

    breakdown = get_expense_breakdown(household_id)

    assert breakdown["Housing"] == Decimal("1500.00")
    assert breakdown["Groceries"] == Decimal("433.33")


def test_monthly_cash_flow(test_database):
    household_id = db.create_household("Test Household")

    db.add_income(
        household_id, "Employment", 4000, "monthly"
    )

    db.add_expense(
        household_id, "Rent", "Housing", 1500, "monthly"
    )

    cash_flow = get_monthly_cash_flow(household_id)

    assert cash_flow["income"] == Decimal("4000.00")
    assert cash_flow["expenses"] == Decimal("1500.00")
    assert cash_flow["remaining"] == Decimal("2500.00")


def test_nonexistent_household(test_database):
    with pytest.raises(ValueError):
        get_household_budget(9999)

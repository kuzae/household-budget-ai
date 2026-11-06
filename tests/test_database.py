
import pytest

import database.db as db


@pytest.fixture
def test_database(tmp_path, monkeypatch):
    """Give each test its own temporary SQLite database."""
    database_path = tmp_path / "test_budget.db"

    monkeypatch.setattr(db, "DATABASE_PATH", database_path)
    monkeypatch.setattr(db, "DATA_DIR", tmp_path)

    db.initialize_database()

    return database_path


def test_initialize_database(test_database):
    assert test_database.exists()


def test_create_household(test_database):
    household_id = db.create_household("Test Household")

    households = db.get_households()

    assert household_id > 0
    assert len(households) == 1
    assert households[0]["name"] == "Test Household"


def test_create_household_rejects_empty_name(test_database):
    with pytest.raises(ValueError):
        db.create_household("")


def test_add_and_retrieve_income(test_database):
    household_id = db.create_household("Test Household")

    db.add_income(
        household_id,
        "Primary Employment",
        5000.00,
        "monthly"
    )

    records = db.get_financial_records(household_id, "income")

    assert len(records) == 1
    assert records[0]["description"] == "Primary Employment"
    assert str(records[0]["amount"]) == "5000"


def test_add_and_retrieve_expense(test_database):
    household_id = db.create_household("Test Household")

    db.add_expense(
        household_id,
        "Rent",
        "Housing",
        1500.00,
        "monthly"
    )

    records = db.get_financial_records(household_id, "expenses")

    assert len(records) == 1
    assert records[0]["description"] == "Rent"
    assert records[0]["category"] == "Housing"
    assert str(records[0]["amount"]) == "1500"


def test_add_and_retrieve_savings(test_database):
    household_id = db.create_household("Test Household")

    db.add_savings(
        household_id,
        "Emergency Fund",
        300.00,
        "monthly"
    )

    records = db.get_financial_records(household_id, "savings")

    assert len(records) == 1
    assert records[0]["description"] == "Emergency Fund"
    assert str(records[0]["amount"]) == "300"


def test_reject_negative_amount(test_database):
    household_id = db.create_household("Test Household")

    with pytest.raises(ValueError):
        db.add_income(
            household_id,
            "Invalid Income",
            -100,
            "monthly"
        )


def test_reject_invalid_table(test_database):
    household_id = db.create_household("Test Household")

    with pytest.raises(ValueError):
        db.get_financial_records(household_id, "invalid")


def test_reject_empty_expense_category(test_database):
    household_id = db.create_household("Test Household")

    with pytest.raises(ValueError):
        db.add_expense(
            household_id,
            "Rent",
            "",
            1500,
            "monthly"
        )


def test_update_income(test_database):
    household_id = db.create_household("Test Household")

    record_id = db.add_income(
        household_id, "Employment", 5000, "monthly"
    )

    result = db.update_financial_record(
        record_id,
        "income",
        amount=6000,
    )

    records = db.get_financial_records(household_id, "income")

    assert result is True
    assert str(records[0]["amount"]) == "6000"


def test_delete_expense(test_database):
    household_id = db.create_household("Test Household")

    record_id = db.add_expense(
        household_id, "Rent", "Housing", 1500, "monthly"
    )

    result = db.delete_financial_record(record_id, "expenses")

    records = db.get_financial_records(household_id, "expenses")

    assert result is True
    assert len(records) == 0


def test_delete_household(test_database):
    household_id = db.create_household("Test Household")

    db.add_income(household_id, "Employment", 5000, "monthly")

    result = db.delete_household(household_id)

    assert result is True
    assert db.get_household(household_id) is None
    assert db.get_financial_records(household_id, "income") == []

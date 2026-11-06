
from database.db import (
    initialize_database,
    create_household,
    add_income,
    add_expense,
    get_financial_records,
)

initialize_database()

household_id = create_household("Test Household")

add_income(
    household_id,
    "Primary Employment",
    5000.00,
    "monthly"
)

add_expense(
    household_id,
    "Rent",
    "Housing",
    1500.00,
    "monthly"
)

print("Income:")
print(get_financial_records(household_id, "income"))

print("Expenses:")
print(get_financial_records(household_id, "expenses"))

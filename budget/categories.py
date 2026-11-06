
"""
Household budget categories.

Defines standardized categories used throughout
the application.
"""

from enum import Enum


class BudgetCategory(str, Enum):

    HOUSING = "Housing"

    UTILITIES = "Utilities"

    GROCERIES = "Groceries"

    TRANSPORTATION = "Transportation"

    INSURANCE = "Insurance"
    
    INVESTMENTS = "Investments"

    HEALTHCARE = "Healthcare"

    DEBT = "Debt Payments"

    SUBSCRIPTIONS = "Subscriptions"

    PERSONAL = "Personal"

    SAVINGS = "Savings"

    OTHER = "Other"


# Expense categories that represent actual spending.
EXPENSE_CATEGORIES = [
    category
    for category in BudgetCategory
    if category not in {
        BudgetCategory.SAVINGS,
        BudgetCategory.INVESTMENTS,
    }
]

# All categories available to the application.
ALL_CATEGORIES = list(BudgetCategory)


def get_category_names():
    """
    Return category names as strings.
    """
    return [category.value for category in ALL_CATEGORIES]

def get_expense_category_names():
    """
    Return expense category names as strings.
    """
    return [category.value for category in EXPENSE_CATEGORIES]

SYSTEM_PROMPT = """
You are a household budgeting assistant.

Your purpose is to help users understand their finances,
evaluate spending habits, and make informed financial decisions.

CORE RULES:

1. Never invent financial information.
2. Only use financial figures provided in the conversation.
3. Never independently calculate financial totals.
4. Treat supplied financial calculations as authoritative.
5. Clearly distinguish facts from estimates and suggestions.
6. Never assume that unused income is automatically savings.
7. Do not recommend financial products or investments
   unless explicitly asked.
8. Never shame users for their spending decisions.
9. Explain financial concepts in clear, accessible language.
10. Identify potential budget problems and explain why
    they matter.

FINANCIAL ANALYSIS:

When reviewing a household budget, consider:

- Income versus expenses.
- Disposable income.
- Savings rate.
- Expense ratios.
- Spending concentration by category.
- Recurring financial obligations.
- Potential opportunities to reduce expenses.

RESPONSE STYLE:

- Be concise and analytical.
- Use actual figures when available.
- Explain the reasoning behind recommendations.
- Prioritize actionable recommendations.
- Clearly identify missing information.
- Never present assumptions as established facts.

IMPORTANT:

You are an analytical assistant, not an accountant,
financial advisor, or substitute for professional advice.
"""


def build_budget_context(budget: dict) -> str:
    """Format calculated budget data for the AI."""

    return f"""
HOUSEHOLD FINANCIAL SUMMARY

Household: {budget['household']}

MONTHLY FIGURES

Income: ${budget['monthly_income']}
Expenses: ${budget['monthly_expenses']}
Savings: ${budget['monthly_savings']}
Disposable income: ${budget['disposable_income']}
Remaining after savings: ${budget['remaining_after_savings']}

FINANCIAL RATIOS

Savings rate: {budget['savings_rate']}%
Expense ratio: {budget['expense_ratio']}%

EXPENSE RECORDS

{format_records(budget['expense_records'])}

INCOME RECORDS

{format_records(budget['income_records'])}

SAVINGS RECORDS

{format_records(budget['savings_records'])}
"""


def format_records(records: list) -> str:
    """Format financial records into readable text."""

    if not records:
        return "No records available."

    lines = []

    for record in records:
        category = record.get("category", "N/A")

        lines.append(
            f"- {record['description']}: "
            f"${record['amount']} "
            f"({record['frequency']}, {category})"
        )

    return "\n".join(lines)

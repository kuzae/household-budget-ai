
import streamlit as st

from database.db import (
    initialize_database,
    create_household,
    get_households,
    add_income,
    add_expense,
    add_savings,
)

from budget.service import (
    get_household_budget,
    get_expense_breakdown,
)

from budget.categories import get_expense_category_names
from ai.assistant import BudgetAssistant


# --------------------------------------------------
# Application setup
# --------------------------------------------------

st.set_page_config(
    page_title="Household Budget AI",
    page_icon="💰",
    layout="wide",
)

initialize_database()

FREQUENCIES = [
    "weekly",
    "biweekly",
    "semimonthly",
    "monthly",
    "quarterly",
    "annually",
]


def format_currency(value):
    return f"${value:,.2f}"


def display_records(records):
    if not records:
        st.info("No records added yet.")
        return

    display_data = []

    for record in records:
        item = {
            "Description": record["description"],
            "Amount": format_currency(record["amount"]),
            "Frequency": record["frequency"].capitalize(),
        }

        if "category" in record:
            item["Category"] = record["category"]

        display_data.append(item)

    st.dataframe(
        display_data,
        use_container_width=True,
        hide_index=True,
    )


# --------------------------------------------------
# Application header
# --------------------------------------------------

st.title("💰 Household Budget AI")
st.caption("Local household financial management and AI analysis")

households = get_households()


# --------------------------------------------------
# Household creation
# --------------------------------------------------

if not households:
    st.subheader("Create your first household")

    with st.form("create_household_form"):
        household_name = st.text_input("Household name")

        submitted = st.form_submit_button("Create Household")

        if submitted:
            if household_name.strip():
                create_household(household_name)
                st.success("Household created.")
                st.rerun()
            else:
                st.error("Please enter a household name.")

    st.stop()


# --------------------------------------------------
# Household selection
# --------------------------------------------------

household_lookup = {
    household["id"]: household["name"]
    for household in households
}

selected_household_id = st.sidebar.selectbox(
    "Select Household",
    options=list(household_lookup.keys()),
    format_func=lambda household_id: household_lookup[household_id],
)

if st.sidebar.button("Create Another Household"):
    st.session_state["show_household_form"] = True

if st.session_state.get("show_household_form", False):
    with st.sidebar.form("additional_household_form"):
        new_name = st.text_input("New household name")

        if st.form_submit_button("Create"):
            if new_name.strip():
                create_household(new_name)
                st.session_state["show_household_form"] = False
                st.rerun()
            else:
                st.error("Enter a household name.")


# --------------------------------------------------
# Retrieve financial information
# --------------------------------------------------

budget = get_household_budget(selected_household_id)

expense_breakdown = get_expense_breakdown(
    selected_household_id
)


# --------------------------------------------------
# Financial dashboard
# --------------------------------------------------

st.header(f"Overview: {budget['household']}")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Monthly Income",
    format_currency(budget["monthly_income"]),
)

col2.metric(
    "Monthly Expenses",
    format_currency(budget["monthly_expenses"]),
)

col3.metric(
    "Monthly Savings",
    format_currency(budget["monthly_savings"]),
)

col4.metric(
    "Remaining Cash",
    format_currency(budget["remaining_after_savings"]),
)

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("Financial Ratios")

    st.metric(
        "Savings Rate",
        f"{budget['savings_rate']}%",
    )

    st.metric(
        "Expense Ratio",
        f"{budget['expense_ratio']}%",
    )

with col2:
    st.subheader("Expense Breakdown")

    if expense_breakdown:
        st.bar_chart(expense_breakdown)
    else:
        st.info("Add expenses to see your spending breakdown.")


# --------------------------------------------------
# Financial record management
# --------------------------------------------------

st.divider()

st.header("Manage Finances")

income_tab, expense_tab, savings_tab = st.tabs(
    ["Income", "Expenses", "Savings"]
)


# --------------------------------------------------
# Income
# --------------------------------------------------

with income_tab:

    st.subheader("Add Income")

    with st.form("income_form"):

        description = st.text_input(
            "Income description",
            key="income_description",
        )

        amount = st.number_input(
            "Amount",
            min_value=0.01,
            step=0.01,
            key="income_amount",
        )

        frequency = st.selectbox(
            "Frequency",
            FREQUENCIES,
            key="income_frequency",
        )

        submitted = st.form_submit_button("Add Income")

        if submitted:
            if description.strip():
                add_income(
                    selected_household_id,
                    description,
                    amount,
                    frequency,
                )

                st.success("Income added.")
                st.rerun()
            else:
                st.error("Enter an income description.")

    st.subheader("Existing Income")
    display_records(budget["income_records"])


# --------------------------------------------------
# Expenses
# --------------------------------------------------

with expense_tab:

    st.subheader("Add Expense")

    with st.form("expense_form"):

        description = st.text_input(
            "Expense description",
            key="expense_description",
        )

        category = st.selectbox(
            "Category",
            get_expense_category_names(),
        )

        amount = st.number_input(
            "Amount",
            min_value=0.01,
            step=0.01,
            key="expense_amount",
        )

        frequency = st.selectbox(
            "Frequency",
            FREQUENCIES,
            key="expense_frequency",
        )

        submitted = st.form_submit_button("Add Expense")

        if submitted:
            if description.strip():
                add_expense(
                    selected_household_id,
                    description,
                    category,
                    amount,
                    frequency,
                )

                st.success("Expense added.")
                st.rerun()
            else:
                st.error("Enter an expense description.")

    st.subheader("Existing Expenses")
    display_records(budget["expense_records"])


# --------------------------------------------------
# Savings
# --------------------------------------------------

with savings_tab:

    st.subheader("Add Savings")

    with st.form("savings_form"):

        description = st.text_input(
            "Savings description",
            key="savings_description",
        )

        amount = st.number_input(
            "Amount",
            min_value=0.01,
            step=0.01,
            key="savings_amount",
        )

        frequency = st.selectbox(
            "Frequency",
            FREQUENCIES,
            key="savings_frequency",
        )

        submitted = st.form_submit_button("Add Savings")

        if submitted:
            if description.strip():
                add_savings(
                    selected_household_id,
                    description,
                    amount,
                    frequency,
                )

                st.success("Savings contribution added.")
                st.rerun()
            else:
                st.error("Enter a savings description.")

    st.subheader("Existing Savings")
    display_records(budget["savings_records"])


# --------------------------------------------------
# AI assistant
# --------------------------------------------------

st.divider()

st.header("AI Financial Assistant")

st.caption(
    "Ask questions about your household budget or request "
    "an analysis of your financial position."
)

assistant = BudgetAssistant()

if st.button("Analyze My Budget"):

    with st.spinner("Analyzing your finances..."):

        try:
            analysis = assistant.analyze_budget(budget)
            st.markdown(analysis)

        except RuntimeError as error:
            st.error(str(error))

with st.form("ai_question_form"):

    question = st.text_input(
        "Ask a financial question",
        placeholder="Where could I reduce my monthly expenses?",
    )

    submitted = st.form_submit_button("Ask AI")

    if submitted:

        if not question.strip():
            st.warning("Enter a question.")

        else:
            with st.spinner("Generating response..."):

                try:
                    answer = assistant.ask_question(
                        question,
                        budget,
                    )

                    st.markdown(answer)

                except RuntimeError as error:
                    st.error(str(error))


# --------------------------------------------------
# Footer
# --------------------------------------------------

st.divider()

st.caption(
    "Household Budget AI | Local financial management"
)

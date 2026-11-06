# Household Budget AI

A lightweight household budgeting application built with **Python, SQLite, Streamlit, and Ollama**. This MVP combines deterministic financial calculations with a locally hosted Llama language model to provide natural-language budget analysis and financial insights.

The application is designed to run locally, keeping household financial data and AI inference on the user's own machine.

## Overview

Household Budget AI provides a simple interface for organizing recurring household income, expenses, and savings. It calculates monthly financial summaries and uses a locally hosted LLM to help users understand their financial position.

### Key Features

- **Household Management** – Create and manage household budget profiles.
- **Income Tracking** – Record income with weekly, biweekly, semimonthly, monthly, quarterly, or annual frequencies.
- **Expense Tracking** – Organize recurring expenses by category.
- **Savings Tracking** – Record recurring savings contributions.
- **Budget Calculations** – Automatically normalize financial records into monthly amounts.
- **Financial Metrics** – Calculate disposable income, savings rate, and expense ratio.
- **Expense Breakdown** – Review spending distribution across categories.
- **Local AI Integration** – Use Ollama and a locally hosted Llama model for natural-language budget analysis and questions.
- **Local Data Storage** – Persist household records using SQLite.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application logic and backend |
| Streamlit | Interactive web interface |
| SQLite | Local relational database |
| Ollama | Local LLM runtime and API |
| Llama 3.1 | Natural-language financial analysis |
| Requests | HTTP communication with Ollama |
| Pytest | Automated testing |

## Architecture

The application uses a modular architecture that separates the user interface, business logic, database operations, and AI integration.

```text
household-budget-ai/
│
├── ai/
│   ├── assistant.py       # Ollama API integration
│   └── prompts.py         # System prompts and financial context
│
├── budget/
│   ├── calculations.py    # Financial calculations
│   ├── categories.py      # Budget categories
│   └── service.py         # Budget business logic
│
├── config/
│   └── settings.py        # Application configuration
│
├── database/
│   └── db.py              # SQLite operations and CRUD functions
│
├── data/                  # Local database storage
│
├── tests/                 # Automated tests
│
├── app.py                 # Streamlit application entry point
├── requirements.txt       # Python dependencies
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.10 or newer
- Git
- [Ollama](https://ollama.com/)
- A locally installed Llama model

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/household-budget-ai.git
cd household-budget-ai
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\activate
```

On Linux/macOS:

```bash
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Ollama

Install Ollama and download the Llama model:

```bash
ollama pull llama3.1:latest
```

Start the Ollama service if it is not already running:

```bash
ollama serve
```

The application communicates with Ollama through its local HTTP API at:

```text
http://localhost:11434
```

The default model configuration is `llama3.1:latest`.

### 5. Launch the Application

```bash
python -m streamlit run app.py
```

Streamlit will provide a local URL, typically:

```text
http://localhost:8501
```

## Financial Calculations

Financial records are normalized to monthly values to provide consistent budget comparisons across different payment frequencies.

The application calculates:

- **Monthly Income** – Total normalized household income.
- **Monthly Expenses** – Total normalized recurring expenses.
- **Monthly Savings** – Total normalized recurring savings contributions.
- **Disposable Income** – Monthly income minus monthly expenses.
- **Remaining After Savings** – Disposable income minus planned savings.
- **Savings Rate** – Savings as a percentage of monthly income.
- **Expense Ratio** – Expenses as a percentage of monthly income.

Financial calculations are handled by Python rather than delegated to the language model. This separates deterministic financial logic from probabilistic natural-language generation.

## Local AI Integration

The application uses Ollama to communicate with a locally hosted Llama model.

The AI assistant receives a structured summary of household financial information and provides natural-language analysis, including:

- General budget assessment.
- Major spending categories.
- Potential financial risks.
- Opportunities to improve savings.
- Practical budgeting recommendations.
- Answers to user questions about their budget.

The LLM is used as an analytical interface, not as the source of truth for financial calculations.

## Data Storage and Privacy

Household records are stored locally in a SQLite database.

AI inference is performed through the locally hosted Ollama service rather than a third-party hosted LLM API.

The local database is excluded from version control to prevent personal financial information from being published to GitHub.

## Testing

The project uses Pytest for automated testing of its calculation, database, service, and AI integration layers.

Run the test suite:

```bash
python -m pytest -v
```

## Current Scope

This project is an MVP focused on recurring household budgeting and local AI integration.

Potential future improvements include:

- Income and expense editing and deletion through the UI.
- Transaction history and actual-versus-budget comparisons.
- Data visualization and spending trends.
- CSV import and export.
- Improved input validation and error handling.
- Docker deployment.
- Raspberry Pi deployment for an always-on local budgeting assistant.

## Disclaimer

This application is an educational and personal budgeting tool. AI-generated analysis is informational and should not be treated as professional financial, tax, or investment advice.

---

**Built with Python, SQLite, Streamlit, and Ollama.**
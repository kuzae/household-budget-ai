
import pytest
from unittest.mock import Mock, patch

from ai.assistant import BudgetAssistant


@pytest.fixture
def assistant():
    return BudgetAssistant()


@pytest.fixture
def sample_budget():
    return {
        "household": "Test Household",
        "monthly_income": 5000,
        "monthly_expenses": 2500,
        "monthly_savings": 500,
        "disposable_income": 2500,
        "remaining_after_savings": 2000,
        "savings_rate": 10,
        "expense_ratio": 50,
        "income_records": [],
        "expense_records": [],
        "savings_records": [],
    }


def test_successful_ai_response(assistant):
    mock_response = Mock()
    mock_response.json.return_value = {
        "message": {
            "content": "Your budget is in good shape."
        }
    }

    with patch(
        "ai.assistant.requests.post",
        return_value=mock_response,
    ) as mock_post:

        result = assistant.generate_response("Analyze my budget.")

    assert result == "Your budget is in good shape."
    mock_post.assert_called_once()


def test_empty_prompt_rejected(assistant):
    with pytest.raises(ValueError):
        assistant.generate_response("")


def test_connection_failure(assistant):
    import requests

    with patch(
        "ai.assistant.requests.post",
        side_effect=requests.ConnectionError,
    ):
        with pytest.raises(RuntimeError, match="Could not connect"):
            assistant.generate_response("Hello")


def test_timeout(assistant):
    import requests

    with patch(
        "ai.assistant.requests.post",
        side_effect=requests.Timeout,
    ):
        with pytest.raises(RuntimeError, match="too long"):
            assistant.generate_response("Hello")


def test_http_error(assistant):
    import requests

    mock_response = Mock()
    mock_response.raise_for_status.side_effect = (
        requests.HTTPError("500 Server Error")
    )

    with patch(
        "ai.assistant.requests.post",
        return_value=mock_response,
    ):
        with pytest.raises(RuntimeError, match="HTTP error"):
            assistant.generate_response("Hello")


def test_invalid_response(assistant):
    mock_response = Mock()
    mock_response.json.return_value = {}

    with patch(
        "ai.assistant.requests.post",
        return_value=mock_response,
    ):
        with pytest.raises(RuntimeError, match="unexpected response"):
            assistant.generate_response("Hello")


def test_analyze_budget(assistant, sample_budget):
    with patch.object(
        assistant,
        "generate_response",
        return_value="Your savings rate is 10%.",
    ) as mock_generate:

        result = assistant.analyze_budget(sample_budget)

    assert result == "Your savings rate is 10%."
    mock_generate.assert_called_once()


def test_ask_question(assistant, sample_budget):
    with patch.object(
        assistant,
        "generate_response",
        return_value="You have $2,000 remaining.",
    ) as mock_generate:

        result = assistant.ask_question(
            "How much money remains?",
            sample_budget,
        )

    assert result == "You have $2,000 remaining."
    mock_generate.assert_called_once()


def test_empty_question_rejected(assistant, sample_budget):
    with pytest.raises(ValueError):
        assistant.ask_question("", sample_budget)


def test_connection_check_success(assistant):
    mock_response = Mock()

    with patch(
        "ai.assistant.requests.get",
        return_value=mock_response,
    ):
        assert assistant.check_connection() is True


def test_connection_check_failure(assistant):
    import requests

    with patch(
        "ai.assistant.requests.get",
        side_effect=requests.ConnectionError,
    ):
        assert assistant.check_connection() is False


import requests

from config.settings import (
    OLLAMA_HOST,
    OLLAMA_MODEL,
    OLLAMA_TIMEOUT,
)

from ai.prompts import SYSTEM_PROMPT, build_budget_context


class BudgetAssistant:
    def __init__(self):
        self.host = OLLAMA_HOST.rstrip("/")
        self.model = OLLAMA_MODEL
        self.timeout = OLLAMA_TIMEOUT

    def check_connection(self) -> bool:
        """Check whether the Ollama server is available."""

        try:
            response = requests.get(
                f"{self.host}/api/tags",
                timeout=10,
            )

            response.raise_for_status()
            return True

        except requests.RequestException:
            return False

    def generate_response(self, prompt: str) -> str:
        """Send a prompt to the local language model."""

        if not prompt.strip():
            raise ValueError("Prompt cannot be empty.")

        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT,
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            "stream": False,
        }

        try:
            response = requests.post(
                f"{self.host}/api/chat",
                json=payload,
                timeout=self.timeout,
            )

            response.raise_for_status()

            result = response.json()

            return result["message"]["content"].strip()

        except requests.Timeout as exc:
            raise RuntimeError(
                "The AI model took too long to respond."
            ) from exc

        except requests.ConnectionError as exc:
            raise RuntimeError(
                "Could not connect to Ollama. "
                "Make sure the Ollama server is running."
            ) from exc

        except requests.HTTPError as exc:
            raise RuntimeError(
                f"Ollama returned an HTTP error: {exc}"
            ) from exc

        except (KeyError, ValueError) as exc:
            raise RuntimeError(
                "Ollama returned an unexpected response."
            ) from exc

    def analyze_budget(self, budget: dict) -> str:
        """Generate an AI analysis of a household budget."""

        context = build_budget_context(budget)

        prompt = f"""
Analyze the following household budget.

Identify:
1. Overall financial position.
2. Major spending categories.
3. Potential financial risks.
4. Opportunities to improve savings.
5. Three practical recommendations.

Use only the supplied financial information.

{context}
"""

        return self.generate_response(prompt)

    def ask_question(self, question: str, budget: dict) -> str:
        """Answer a financial question using household context."""

        if not question.strip():
            raise ValueError("Question cannot be empty.")

        context = build_budget_context(budget)

        prompt = f"""
HOUSEHOLD FINANCIAL CONTEXT:

{context}

USER QUESTION:

{question}

Answer using the supplied financial information.
If information is missing, say so explicitly.
"""

        return self.generate_response(prompt)

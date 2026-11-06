
"""
Application configuration.

Centralizes environment-specific settings for the
Household Budget AI application.
"""

import os
from pathlib import Path


# --------------------------------------------------
# Project paths
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"

DATABASE_PATH = DATA_DIR / "household_budget.db"


# --------------------------------------------------
# Application settings
# --------------------------------------------------

APP_NAME = "Household Budget AI"

APP_VERSION = "0.1.0"

DEBUG = os.getenv("APP_DEBUG", "false").lower() == "true"


# --------------------------------------------------
# AI / Ollama configuration
# --------------------------------------------------

OLLAMA_HOST = os.getenv(
    "OLLAMA_HOST",
    "http://localhost:11434"
)

OLLAMA_MODEL = os.getenv(
    "OLLAMA_MODEL",
    "llama3.1:latest"
)

OLLAMA_TIMEOUT = int(
    os.getenv("OLLAMA_TIMEOUT", "120")
)


# --------------------------------------------------
# Financial settings
# --------------------------------------------------

DEFAULT_CURRENCY = os.getenv(
    "DEFAULT_CURRENCY",
    "USD"
)

DEFAULT_LOCALE = os.getenv(
    "DEFAULT_LOCALE",
    "en_US"
)


# --------------------------------------------------
# Initialization
# --------------------------------------------------

def initialize_directories():
    """
    Ensure required application directories exist.
    """
    DATA_DIR.mkdir(parents=True, exist_ok=True)

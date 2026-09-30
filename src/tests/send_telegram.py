"""
Send a test price drop message on Telegram, to check that the bot configuration works.

Usage (from the project root):
    python tests/send_telegram.py

The message is sent to TELEGRAM_CHAT_ID with the bot TELEGRAM_TOKEN (both from .env).

Author : Tao Serveaux
Date : 29/09/26
"""

import sys
from pathlib import Path

from dotenv import load_dotenv

# Make the "src" package importable when the script is run directly
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.utils.telegram import Telegram

SAMPLE_DATA = {
    "url": "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html",
    "title": "A Light in the Attic",
    "price": 47.50,
    "stock": 14,
}
THRESHOLD = 50.00
GRAPH = ROOT / "docs" / "demo_graph.png"


def main():
    """Load the .env file, send the test message and print the result."""

    load_dotenv(ROOT / ".env")

    telegram = Telegram()
    attachment = GRAPH if GRAPH.exists() else None

    if telegram.send(SAMPLE_DATA, THRESHOLD, attachment):
        print("Telegram message sent")
        return 0

    print(f"Telegram message not sent: {telegram.getError()}")
    return 1


if __name__ == "__main__":
    sys.exit(main())

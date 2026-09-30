"""
Send a test price drop email, to check that the email configuration works.

Usage (from the project root):
    python tests/send_mail.py [recipient]

If no recipient is given, the email is sent to MAIL_SENDER (yourself).

Author : Tao Serveaux
Date : 29/09/26
"""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv

# Make the "src" package importable when the script is run directly
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.utils.mail import Mail

SAMPLE_DATA = {
    "url": "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html",
    "title": "A Light in the Attic",
    "price": 47.50,
    "stock": 14,
}
THRESHOLD = 50.00
GRAPH = ROOT / "docs" / "demo_graph.png"


def main():
    """Load the .env file, send the test email and print the result."""

    load_dotenv(ROOT / ".env")

    recipient = sys.argv[1] if len(sys.argv) > 1 else os.getenv("MAIL_SENDER")
    if not recipient:
        print("No recipient: pass one as an argument or set MAIL_SENDER in .env")
        return 1

    mail = Mail(recipient)
    attachment = GRAPH if GRAPH.exists() else None

    if mail.send(SAMPLE_DATA, THRESHOLD, attachment):
        print(f"Email sent to {recipient}")
        return 0

    print(f"Email not sent: {mail.getError()}")
    return 1


if __name__ == "__main__":
    sys.exit(main())

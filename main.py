"""
Entry point of scrapPrice: loads the environment variables from the .env file.

Author : Tao Serveaux
Date : 28/09/26
"""

from dotenv import load_dotenv

# Load MAIL_SENDER, MAIL_PASSWORD, TELEGRAM_TOKEN and TELEGRAM_CHAT_ID from the .env file
load_dotenv()

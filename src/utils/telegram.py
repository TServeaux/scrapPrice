"""
Send price drop alerts through a Telegram bot.

Author : Tao Serveaux
Date : 28/09/26
"""

import os
from pathlib import Path

import requests

class Telegram:
    """Send price drop alerts through a Telegram bot."""

    def __init__(self, timeout=10):
        """
        Initialize the Telegram notifier.

        The bot token and the target chat are read from the TELEGRAM_TOKEN and
        TELEGRAM_CHAT_ID environment variables.

        Args:
            timeout (int | float): Maximum time in seconds to wait for the Telegram API.
        """

        self.__token = os.getenv("TELEGRAM_TOKEN")
        self.__chatId = os.getenv("TELEGRAM_CHAT_ID")
        self.__timeout = timeout
        self.__err = None

    def send(self, data, threshold=None, attachment=None):
        """
        Send a price drop message for a product.

        If an attachment is given, it is sent as a photo with the message as
        its caption; otherwise a plain text message is sent.

        Args:
            data (dict | None): Product data as returned by Extract.extractData().
            threshold (float | None): Alert threshold, mentioned in the message if provided.
            attachment (str | Path | None): Path to an image (e.g. the price graph) to send.

        Returns:
            bool: True if the message was sent, False otherwise (the reason can be
            retrieved with getError()).
        """

        self.__err = None

        if data is None or data.get("price") is None:
            self.__err = "Incomplete data, no message sent"
            return False

        if not self.__token or not self.__chatId:
            self.__err = "Missing TELEGRAM_TOKEN or TELEGRAM_CHAT_ID environment variables"
            return False

        text = f"Price drop: {data['title']}\n\n"
        text += f"New price: £{data['price']:.2f}\n"
        if threshold is not None:
            text += f"Alert threshold: £{threshold:.2f}\n"
        text += f"\n{data['url']}"

        baseUrl = f"https://api.telegram.org/bot{self.__token}"

        try:
            if attachment is not None:
                with open(Path(attachment), "rb") as photo:
                    res = requests.post(
                        f"{baseUrl}/sendPhoto",
                        data={"chat_id": self.__chatId, "caption": text},
                        files={"photo": photo},
                        timeout=self.__timeout
                    )
            else:
                res = requests.post(
                    f"{baseUrl}/sendMessage",
                    data={"chat_id": self.__chatId, "text": text},
                    timeout=self.__timeout
                )

            res.raise_for_status()

        except (requests.RequestException, OSError) as err:
            self.__err = err
            return False

        return True

    def getError(self):
        """
        Return the error of the last call to send().

        Returns:
            str | Exception | None: The last error, or None if the message was sent.
        """

        return self.__err

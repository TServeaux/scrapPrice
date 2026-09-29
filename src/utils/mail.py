"""
Send price drop alerts by email (SMTP over SSL).

Author : Tao Serveaux
Date : 28/09/26
"""

import os
import smtplib
from email.message import EmailMessage
from pathlib import Path

class Mail:
    """Send price drop alerts by email over SMTP with SSL."""

    def __init__(self, recipient, smtpServer="smtp.gmail.com", port=465):
        """
        Initialize the mailer.

        The sender address and password are read from the MAIL_SENDER and
        MAIL_PASSWORD environment variables.

        Args:
            recipient (str): Email address that will receive the alerts.
            smtpServer (str): Hostname of the SMTP server.
            port (int): SSL port of the SMTP server.
        """

        self.__recipient = recipient
        self.__smtpServer = smtpServer
        self.__port = port
        self.__sender = os.getenv("MAIL_SENDER")
        self.__password = os.getenv("MAIL_PASSWORD")
        self.__err = None

    def send(self, data, threshold=None, attachment=None):
        """
        Send a price drop email for a product.

        Args:
            data (dict | None): Product data as returned by Extract.extractData().
            threshold (float | None): Alert threshold, mentioned in the email if provided.
            attachment (str | Path | None): Path to a PNG image (e.g. the price graph) to attach.

        Returns:
            bool: True if the email was sent, False otherwise (the reason can be
            retrieved with getError()).
        """

        self.__err = None

        if data is None or data.get("price") is None:
            self.__err = "Incomplete data, no email sent"
            return False

        if not self.__sender or not self.__password:
            self.__err = "Missing MAIL_SENDER or MAIL_PASSWORD environment variables"
            return False

        msg = EmailMessage()
        msg["Subject"] = f"Price drop: {data['title']}"
        msg["From"] = self.__sender
        msg["To"] = self.__recipient

        text = f"The price of \"{data['title']}\" is now £{data['price']:.2f}.\n"
        if threshold is not None:
            text += f"Your alert threshold was set to £{threshold:.2f}.\n"
        text += f"\nProduct link: {data['url']}\n"
        msg.set_content(text)

        try:
            if attachment is not None:
                attachmentPath = Path(attachment)
                msg.add_attachment(
                    attachmentPath.read_bytes(),
                    maintype="image",
                    subtype="png",
                    filename=attachmentPath.name
                )

            with smtplib.SMTP_SSL(self.__smtpServer, self.__port, timeout=10) as server:
                server.login(self.__sender, self.__password)
                server.send_message(msg)

        except (smtplib.SMTPException, OSError) as err:
            self.__err = err
            return False

        return True

    def getError(self):
        """
        Return the error of the last call to send().

        Returns:
            str | Exception | None: The last error, or None if the email was sent.
        """

        return self.__err

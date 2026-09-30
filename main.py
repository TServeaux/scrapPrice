"""
Entry point of scrapPrice: loads the environment variables from the .env file.

Author : Tao Serveaux
Date : 28/09/26
"""

import json
import logging
import os
import time
from pathlib import Path

from dotenv import load_dotenv

# Load MAIL_SENDER, MAIL_PASSWORD, TELEGRAM_TOKEN and TELEGRAM_CHAT_ID from the .env file
load_dotenv()

from .src.core.scraper import Scraper
from .src.core.extract import Extract
from .src.utils.save import Save
from .src.core.render import Render
from .src.utils.mail import Mail
from .src.utils.telegram import Telegram

BASE_DIR = Path(__file__).resolve().parent
CONFIG_FILE = BASE_DIR / "products.json"
DATA_DIR = BASE_DIR / "data"
GRAPH_DIR = BASE_DIR / "graphs"
LOG_DIR = BASE_DIR / "logs"
DELAY_BETWEEN_REQUESTS = 1


def setupLogging():

    LOG_DIR.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(LOG_DIR / "tracker.log", encoding="utf-8"),
            logging.StreamHandler()
        ]
    )


def loadProducts():

    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def loadNotifiers():

    notifiers = []

    recipient = os.getenv("MAIL_RECIPIENT")
    if recipient:
        notifiers.append(("Email", Mail(recipient)))

    if os.getenv("TELEGRAM_TOKEN"):
        notifiers.append(("Telegram", Telegram()))

    if not notifiers:
        logging.warning("No notifier configured, alerts will only be logged")

    return notifiers


def shouldAlert(prices, threshold):

    if threshold is None or not prices or prices[-1] is None:
        return False

    current = prices[-1]
    previous = prices[-2] if len(prices) > 1 else None

    return current < threshold and (previous is None or previous >= threshold)


def processProduct(product, save, notifiers):

    url = product["url"]
    threshold = product.get("threshold")

    scraper = Scraper(url)
    soup = scraper.scraping()
    if soup is None:
        logging.error("Scraping failed for %s: %s", url, scraper.getError())
        return

    data = Extract(soup, url).extractData()
    if data is None or data.get("price") is None:
        logging.error("Could not extract the price from %s", url)
        return

    save.saveData(data)
    logging.info("Saved \"%s\": £%.2f (stock: %s)", data["title"], data["price"], data["stock"])

    history = save.getHistory(url)
    graphPath = Render(data["title"], history, "Date", "Price (£)", threshold, GRAPH_DIR).graph()

    if not shouldAlert(history["price"], threshold):
        return

    logging.info("Price below threshold for \"%s\", sending alerts", data["title"])

    for name, notifier in notifiers:
        if notifier.send(data, threshold, graphPath):
            logging.info("%s alert sent", name)
        else:
            logging.error("%s alert failed: %s", name, notifier.getError())


def main():

    load_dotenv(BASE_DIR / ".env")
    setupLogging()
    logging.info("Price tracker started")

    try:
        products = loadProducts()
    except (OSError, json.JSONDecodeError) as err:
        logging.error("Cannot load %s: %s", CONFIG_FILE, err)
        return

    notifiers = loadNotifiers()
    save = Save(DATA_DIR)

    try:
        for index, product in enumerate(products):
            if index > 0:
                time.sleep(DELAY_BETWEEN_REQUESTS)
            try:
                processProduct(product, save, notifiers)
            except Exception:
                logging.exception("Unexpected error while processing %s", product.get("url"))
    finally:
        save.closeSaving()

    logging.info("Price tracker finished")


if __name__ == "__main__":
    main()
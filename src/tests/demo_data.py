"""
Generate fake price history in data/data.db and draw the matching graphs, for demos.

Author : Tao Serveaux
Date : 29/09/26
"""

import random
import sqlite3
from datetime import datetime, timedelta

from src.core.render import Render
from src.utils.save import Save

DAYS = 30

# url, title, starting price, final price, starting stock, alert threshold
PRODUCTS = [
    ("https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html",
     "A Light in the Attic", 58.90, 47.50, 22, 50.00),
    ("https://books.toscrape.com/catalogue/tipping-the-velvet_999/index.html",
     "Tipping the Velvet", 53.74, 51.20, 20, 45.00),
    ("https://books.toscrape.com/catalogue/soumission_998/index.html",
     "Soumission", 49.99, 38.40, 20, 40.00),
]


def generateHistory(startPrice, endPrice, startStock):
    """
    Build a fake daily history going from startPrice to endPrice over DAYS days.

    Args:
        startPrice (float): Price on the first day.
        endPrice (float): Price on the last day (today).
        startStock (int): Stock on the first day; it then decreases randomly with occasional restocks.

    Returns:
        dict: History with the keys 'date' (ISO 8601 strings), 'price' and 'stock'.
    """

    today = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)
    history = {"date": [], "price": [], "stock": []}
    stock = startStock

    for day in range(DAYS):
        date = today - timedelta(days=DAYS - 1 - day)
        trend = startPrice + (endPrice - startPrice) * day / (DAYS - 1)
        price = endPrice if day == DAYS - 1 else round(trend + random.uniform(-1.2, 1.2), 2)

        if day > 0:
            stock -= random.choice([0, 0, 1, 1, 2])
            if stock <= 3:
                stock += random.randint(10, 15)

        history["date"].append(date.isoformat(timespec="seconds"))
        history["price"].append(price)
        history["stock"].append(stock)

    return history


def main():
    """Reset the demo tables, insert the fake histories and draw one graph per product."""

    random.seed(42)

    # Save creates data/ and the tables if needed
    Save("data").closeSaving()

    connexion = sqlite3.connect("data/data.db")
    connexion.execute("DELETE FROM price_history")
    connexion.execute("DELETE FROM products")

    for url, title, startPrice, endPrice, startStock, threshold in PRODUCTS:
        history = generateHistory(startPrice, endPrice, startStock)

        cursor = connexion.execute(
            "INSERT INTO products (url, title, threshold) VALUES (?, ?, ?)",
            (url, title, threshold)
        )
        productId = cursor.lastrowid

        connexion.executemany(
            "INSERT INTO price_history (product_id, price, stock, scraped_at) VALUES (?, ?, ?, ?)",
            [(productId, p, s, d) for d, p, s in zip(history["date"], history["price"], history["stock"])]
        )

        Render(title, history, "Date", "Price (£)", threshold=threshold).graph()
        print(f"{title}: {DAYS} entries, {history['price'][0]:.2f} -> {history['price'][-1]:.2f} (threshold {threshold:.2f})")

    connexion.commit()
    connexion.close()


if __name__ == "__main__":
    main()

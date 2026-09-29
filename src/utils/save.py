"""
Store products and their price history in a SQLite database.

Author : Tao Serveaux
Date : 28/09/26
"""

import sqlite3
from pathlib import Path
from datetime import datetime

class Save:
    """Store scraped products and their price history in a SQLite database."""

    def __init__(self, path):
        """
        Open (or create) the database.

        Args:
            path (str | Path): Directory containing the "data.db" file (created if missing).
        """

        self.__path = Path(path)
        self.__connexion =self.createTable()

    def saveData(self, data):
        """
        Save one scraping result.

        The product is added to the "products" table if its URL is not known
        yet, then a new row with the current price, stock and timestamp is
        appended to "price_history".

        Args:
            data (dict | None): Product data as returned by Extract.extractData().

        Returns:
            bool: True if the data was saved, False if data was None.
        """

        if data is None:

            return False

        self.__connexion.execute(
            "INSERT OR IGNORE INTO products (url, title) VALUES (?, ?)",
            (data["url"], data["title"])
        )

        curseur = self.__connexion.execute(
            "SELECT id FROM products WHERE url = ?",
            (data["url"],)
        )
        product_id = curseur.fetchone()[0]

        self.__connexion.execute(
            "INSERT INTO price_history (product_id, price, stock, scraped_at) VALUES (?, ?, ?, ?)",
            (product_id, data["price"], data["stock"], datetime.now().isoformat(timespec="seconds"))
        )

        self.__connexion.commit()

        return True

    def createTable(self):
        """
        Connect to the database and create the tables if they do not exist.

        Tables:
            products: one row per product (url, title, threshold).
            price_history: one row per scraping (product_id, price, stock, scraped_at).

        Returns:
            sqlite3.Connection: An open connection to the database.
        """

        self.__path.mkdir(parents=True, exist_ok=True)

        connexion = sqlite3.connect(self.__path / "data.db")
        connexion.execute("PRAGMA foreign_keys = ON;")
        connexion.executescript("""CREATE TABLE IF NOT EXISTS products (
                                    id        INTEGER PRIMARY KEY AUTOINCREMENT,
                                    url       TEXT NOT NULL UNIQUE,
                                    title     TEXT,
                                    threshold REAL
                                );

                                CREATE TABLE IF NOT EXISTS price_history (
                                    id         INTEGER PRIMARY KEY AUTOINCREMENT,
                                    product_id INTEGER NOT NULL,
                                    price      REAL,
                                    stock      INTEGER,
                                    scraped_at TEXT NOT NULL,
                                    FOREIGN KEY (product_id) REFERENCES products(id)
                                );
                                """)

        return connexion

    def closeSaving(self):
        """Close the database connection."""

        self.__connexion.close()

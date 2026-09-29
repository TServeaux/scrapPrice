"""
Author : Tao Serveaux
Date : 28/09/26
"""

import sqlite3
from pathlib import Path
from datetime import datetime

class Save:

    def __init__(self, path):
        
        self.__path = Path(path)
        self.__connexion =self.createTable()

    def saveData(self, data):
        
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
        
        self.__connexion.close()
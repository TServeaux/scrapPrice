"""
Extract the title, price and stock of a product from its parsed page.

Author : Tao Serveaux
Date : 28/09/26
"""

import re

class Extract:
    """Extract product information (title, price, stock) from a parsed product page."""

    def __init__(self, res, link):
        """
        Initialize the extractor.

        Args:
            res (BeautifulSoup | None): Parsed HTML of the product page, as returned by Scraper.scraping().
            link (str): URL of the product page, stored alongside the extracted data.
        """

        self.__res = res
        self.__link = link

    def extractData(self):
        """
        Extract the product data from the parsed page.

        The title comes from the <h1> tag, the price from <p class="price_color">
        (currency symbol removed) and the stock from the first number found in
        <p class="availability">. Any field that cannot be found is set to None.

        Returns:
            dict | None: A dictionary with the keys 'url', 'title', 'price' (float)
            and 'stock' (int), or None if no page was provided.
        """

        if self.__res is None :
            return None

        title = self.__res.find("h1")
        price = self.__res.find("p", class_="price_color")
        stock = self.__res.find("p", class_="availability")

        if title is not None:
            title = title.get_text(strip=True)

        if price is not None:
            price = float(price.get_text(strip=True).lstrip("$£€"))

        if stock is not None:
            stock = re.search(r"\d+", stock.get_text(strip=True))
            if stock is not None :
                stock = int(stock.group())

        data = {
            'url' : self.__link,
            'title' : title,
            'price' : price,
            'stock' : stock
        }

        return data

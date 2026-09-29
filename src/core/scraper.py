"""
Download a product page and parse its HTML with BeautifulSoup.

Author : Tao Serveaux
Date : 28/09/26
"""

import requests
from bs4 import BeautifulSoup

class Scraper :
    """Download a web page and parse it into a BeautifulSoup tree."""

    def __init__(self, link, timeout = 10):
        """
        Initialize the scraper.

        Args:
            link (str): URL of the page to scrape.
            timeout (int | float): Maximum time in seconds to wait for the HTTP response.
        """

        self.__link = link
        self.__err = None
        self.__timeout = timeout

    def scraping(self) :
        """
        Fetch the page and parse its HTML content.

        Any previous error is cleared before the request is made.

        Returns:
            BeautifulSoup | None: The parsed page, or None if the request failed
            (the error can then be retrieved with getError()).
        """

        self.__err = None

        try :

            res = requests.get(self.__link, timeout=self.__timeout)
            res.raise_for_status()
            res = BeautifulSoup(res.content, 'html.parser')

            return res

        except requests.RequestException as err:

            self.__err = err
            return None

    def getError(self):
        """
        Return the error raised by the last call to scraping().

        Returns:
            requests.RequestException | None: The last error, or None if it succeeded.
        """

        return self.__err

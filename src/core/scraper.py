"""
Author : Tao Serveaux
Date : 28/09/26
"""

import requests
from bs4 import BeautifulSoup

class Scraper :
    
    def __init__(self, link, timeout = 10):
        
        self.__link = link
        self.__err = None
        self.__timeout = timeout
    
    def scraping(self) :
        
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
        
        return self.__err
"""
Author : Tao Serveaux
Date : 28/09/26
"""

import re

class Extract:
    
    def __init__(self, res, link):
        
        self.__res = res
        self.__link = link
    
    def extractData(self):
        
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
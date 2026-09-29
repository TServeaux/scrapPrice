"""
Author : Tao Serveaux
Date : 28/09/26
"""

import re
from datetime import datetime
from pathlib import Path
import matplotlib.pyplot as plt

class Render :
    
    def __init__(self, name, data, xLabel, yLabel, threshold=None, outputDir="graphs"):
        
        self.__name = name
        self.__data = data
        self.__xLabel = xLabel
        self.__yLabel = yLabel
        self.__threshold = threshold
        self.__outputDir = Path(outputDir)
        
    def graph(self):
        
        dates = [datetime.fromisoformat(d) for d in self.__data["date"]]
        stocks = self.__data['stock']
        prices = self.__data['price']
        
        fig, (axPrice, axStock) = plt.subplots(2, 1, sharex=True, figsize=(10, 7))
        
        axPrice.plot(dates, prices, marker="o", label="Prix")
        if self.__threshold is not None:
            axPrice.axhline(self.__threshold, color="red", linestyle="--", label="Seuil d'alerte")
        axPrice.set_title(self.__name)
        axPrice.set_ylabel(self.__yLabel)
        axPrice.grid(True, alpha=0.3)
        axPrice.legend()

        axStock.plot(dates, stocks, marker="x", color="green", label="Stock")
        axStock.set_xlabel(self.__xLabel)
        axStock.set_ylabel("Stock (exemplaires)")
        axStock.grid(True, alpha=0.3)
        axStock.legend()

        fig.autofmt_xdate()

        self.__outputDir.mkdir(parents=True, exist_ok=True)
        fileName = re.sub(r"[^\w-]+", "_", self.__name).strip("_") + ".png"
        filePath = self.__outputDir / fileName

        fig.savefig(filePath, bbox_inches="tight")
        plt.close(fig)
import requests
from bs4 import BeautifulSoup
import json
import time
from datetime import timedelta


class TickerStocks:

    BASE_URL = "https://www.tickertape.in"
    TYPE = "stocks"

    def __init__(self, log: bool = False):
        self.log = log
        self.result = None
    
    # get webpage soup object
    def __getsoup(self, subdirectory: str):
        # url to the stock page
        url = self.BASE_URL + "/" + self.TYPE + "/" + subdirectory

        # hit the page and get html
        header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"
        }
        response = requests.get(url, headers=header)

        # give the webpage to Beautiful Soup using parsers: "html.parser" or "lxml"
        soup = BeautifulSoup(response.text, 'lxml')

        return soup

    def get_details(self, name: str, subdirectory: str) -> dict:
        try:
            # get soup
            soup = self.__getsoup(subdirectory)

            ######### extract html data from webpage and form output data #########
            data = {}

            ##### [1] Basics #####
            # company name
            htmlBlock = soup.find("h3", class_="security-name")
            data["name"] = htmlBlock.text if htmlBlock is not None else None

            # ticker name
            htmlBlock = soup.find("span", class_="ticker")
            data["ticker"] = htmlBlock.text if htmlBlock is not None else None
            
            # url
            data["url"] = self.BASE_URL + "/" + self.TYPE + "/" + subdirectory

            # type
            data["type"] = self.TYPE

            # current price
            htmlBlock = soup.find("span", class_="current-price")
            data["price"] = htmlBlock.text if htmlBlock is not None else None

            # marketcap, sector and risk
            htmlBlock = soup.find("div", class_="stock-labels")
            htmlBlock = htmlBlock.find_all("span", class_="stock-label-title")
            data["sector"] = htmlBlock[0].text if htmlBlock[0] is not None else None
            data["marketcap"] = htmlBlock[1].text if htmlBlock[1] is not None else None
            data["risk"] = htmlBlock[2].text if htmlBlock[2] is not None else None

            # profile
            htmlBlock = soup.find("div", class_="peers-card")
            value_h = htmlBlock.h2.text if htmlBlock.h2 is not None else ""
            value_p = htmlBlock.p.text if htmlBlock.p is not None else ""
            data["profile"] = value_h + ": " + value_p if (value_h + value_p) != "" else None

            ##### [2] Overview #####
            overview = {}

            # current price
            htmlBlock = soup.find("span", class_="current-price")
            overview["currentPrice"] = htmlBlock.text if htmlBlock is not None else None

            # change absolute-value
            htmlBlock = soup.find("span", class_="absolute-value")
            overview["absoluteChange"] = htmlBlock.text if htmlBlock is not None else None

            # change percentage-value
            htmlBlock = soup.find("span", class_="percentage-value")
            overview["percentageChange"] = str(htmlBlock.text).replace("(", "").replace(")", "").strip() if htmlBlock is not None else None

            # marketcap, sector and risk
            htmlBlock = soup.find("div", class_="stock-labels")
            title = htmlBlock.find_all("span", class_="stock-label-title")
            desc = htmlBlock.find_all("span", class_="stock-label-desc")

            overview["sectorType"] = title[0].text if title[0] is not None else None
            overview["sectorDesc"] = desc[0].text if desc[0] is not None else None

            overview["capType"] = title[1].text if title[1] is not None else None
            overview["capDesc"] = desc[1].text if desc[1] is not None else None

            overview["riskType"] = title[2].text if title[2] is not None else None
            overview["riskDesc"] = desc[2].text if desc[2] is not None else None

            # put overview into data
            data["overview"] = overview

            ##### [3] Investment Checklist #####
            investmentChecklist = {}

            # checklist carousel-item get all keys and values
            htmlBlock = soup.find("div", class_="carousel-item")
            for item in htmlBlock.childGenerator():
                key = item.find("span", class_="tooltip-holder").contents[0]
                key = key.title().replace(" ", "")
                key = key[0].lower() + key[1:]
                value = item.find("i")['class'][3].split("-")[1]
                investmentChecklist[key] = value

            # put investmentChecklist into data
            data["investmentChecklist"] = investmentChecklist

            ##### [4] Key Metrics #####
            keyMetrics = {}

            # PERatio, PBRatio, DividendYield, SectorPE, SectorPB, SectorDividendYield
            htmlBlock = soup.find("div", class_="ratios-card")
            keys = htmlBlock.select("span.ellipsis.desktop--only")
            values = htmlBlock.find_all("div", class_="value")
            for i in range(len(keys)):
                key = keys[i].text
                key = key.replace(" ", "")
                value = values[i].text
                value = None if str(value) == "—" else str(value)
                keyMetrics[key] = value

            # put keyMetrics into data
            data["keyMetrics"] = keyMetrics

            ##### [5] Forecast & Ratings #####
            forecasts = {}

            # Forecast
            htmlBlock = soup.find("div", class_="forecast-radial")
            value = htmlBlock.div.span.contents[0] if str(htmlBlock.div.span.contents[0]) != "—" else ""
            symbol = htmlBlock.div.span.span.text if htmlBlock.div.span.span is not None else ""
            forecasts["buyRecommendation"] = value + symbol if (value + symbol) != "" else None
            forecasts["forecast"] = htmlBlock.h4.text if htmlBlock.h4 is not None else None

            # put keyMetrics into data
            data["forecasts"] = forecasts

            # return the scraped data
            return data
        except Exception as e:
            print(e)
            return {}

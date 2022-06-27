import requests
from bs4 import BeautifulSoup
import json
import time
from datetime import timedelta


class TickerETFs:

    BASE_URL = "https://www.tickertape.in"
    TYPE = "etfs"

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
    
    def get_details(self, subdirectory: str) -> dict:
        try:
            # get soup
            soup = self.__getsoup(subdirectory)

            ######### extract html data from webpage and form output data #########
            data = {}

            ##### [1] Basics #####
            # etf name
            html_block = soup.find("h3", class_="security-name")
            data["name"] = html_block.text if html_block is not None else None

            # ticker name
            html_block = soup.find("span", class_="ticker")
            data["ticker"] = html_block.text if html_block is not None else None
            
            # url
            data["url"] = self.BASE_URL + "/" + self.TYPE + "/" + subdirectory

            # type
            data["type"] = self.TYPE

            # tracking
            html_block = soup.find("p", class_="mb12")
            data["tracking"] = html_block.text if html_block is not None else None

            # current price
            html_block = soup.find("span", class_="current-price")
            data["price"] = html_block.text if html_block is not None else None

            # category, sector and liquidity
            html_block = soup.find("div", class_="stock-labels")
            html_block = html_block.find_all("span", class_="stock-label-title")
            data["sector"] = html_block[0].text if html_block[0] is not None else None
            data["category"] = html_block[1].text if html_block[1] is not None else None
            data["liquidity"] = html_block[2].text if html_block[2] is not None else None

            # profile
            html_block = soup.find("div", class_="amc-profile")
            value_h = html_block.h2.text if html_block.h2 is not None else ""
            value_p = html_block.p.text if html_block.p is not None else ""
            data["profile"] = value_h + ": " + value_p if (value_h + value_p) != "" else None

            ##### [2] Overview #####
            overview = {}

            # current price
            html_block = soup.find("span", class_="current-price")
            overview["currentPrice"] = html_block.text if html_block is not None else None

            # change absolute-value
            html_block = soup.find("span", class_="absolute-value")
            overview["absoluteChange"] = html_block.text if html_block is not None else None

            # change percentage-value
            html_block = soup.find("span", class_="percentage-value")
            overview["percentageChange"] = str(html_block.text).replace("(", "").replace(")", "").strip() if html_block is not None else None

            # tracking
            html_block = soup.find("p", class_="mb12")
            data["tracking"] = html_block.text if html_block is not None else None

            # marketcap, sector and risk
            html_block = soup.find("div", class_="stock-labels")
            title = html_block.find_all("span", class_="stock-label-title")
            desc = html_block.find_all("span", class_="stock-label-desc")

            overview["sectorType"] = title[0].text if title[0] is not None else None
            overview["sectorDesc"] = desc[0].text if desc[0] is not None else None

            overview["capType"] = title[1].text if title[1] is not None else None
            overview["capDesc"] = desc[1].text if desc[1] is not None else None

            overview["riskType"] = title[2].text if title[2] is not None else None
            overview["riskDesc"] = desc[2].text if desc[2] is not None else None

            # put overview into data
            data["overview"] = overview

            ##### [3] Investment Checklist #####
            investment_checklist = {}

            # checklist carousel-item get all keys and values
            html_block = soup.find("div", class_="inv-chk-root")
            html_block = html_block.find_all("div", class_="commentary-item-root")
            for item in html_block:
                key = item.find("span", class_="tooltip-holder").contents[0]
                key = key.title().replace(" ", "")
                key = key[0].lower() + key[1:]
                key = "redFlagSafe" if "redflag" in key.lower() else key
                value = item.find("i")['class'][3].split("-")[1]
                investment_checklist[key] = value

            # put investmentChecklist into data
            data["investmentChecklist"] = investment_checklist

            ##### [4] Key Metrics #####
            keyMetrics = {}

            # Realtime NAV, AUM, Expense Ratio, Category Exp Ratio, Tracking Error, Category Tracking Err
            html_block = soup.find("div", class_="ratios-card")
            keys = html_block.select("span.ellipsis.desktop--only")
            values = html_block.find_all("div", class_="value")
            for i in range(len(keys)):
                key = keys[i].text
                key = key.title().replace(" ", "")
                key = key[0].lower() + key[1:]
                value = values[i].text
                value = None if str(value) == "—" else str(value)
                keyMetrics[key] = value

            # put keyMetrics into data
            data["keyMetrics"] = keyMetrics

            # return the scraped data
            return data
        except Exception as e:
            print(e)
            return {}

    def scrape(self, etfs_list: list) -> list:
        # let's scrape all the etf data!
        print("scraping etf data...")
        fulldata = []
        count = 0
        invalid_count = 0

        start_time = time.time()
        for companies in etfs_list:
            company_name = companies["name"]
            company_type = companies["type"]
            company_dir = companies["subdirectory"]

            if company_type != "etfs":
                invalid_count += 1
                continue
            
            if self.log:
                print("scraping data for:", company_name, "url: " + self.BASE_URL + "/" + company_type + "/" + company_dir)
            else:
                print('.', end='', flush=True)

            try:
                # get data from each page and append to data list
                data = self.get_details(company_dir)
                fulldata.append(data)
                count += 1
                if self.log:
                    print("successful!")
            except Exception as e:
                # some issue occured, catch exception
                if self.log:
                    print("failed!")
                    print(e)
        end_time = time.time()
        total_time = timedelta(seconds=(end_time - start_time))

        if self.log:
            print("all pages scraped successfully!")
            print(count, "/", len(etfs_list), self.TYPE, "data scraped successfully.")
            if invalid_count > 0:
                print(invalid_count, "other non", self.TYPE, "data found and ignored!")
            print("total time taken:", str(total_time))
        print()
        print("completed!")

        self.result = fulldata
        return fulldata

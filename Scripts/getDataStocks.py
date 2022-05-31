import requests
from bs4 import BeautifulSoup
import json
import time
from datetime import timedelta


def scrapeTickertape(name, stocktype, subdirectory):
    _url = "https://www.tickertape.in/" + stocktype + "/" + subdirectory
    _data = {}

    try:
        # hit the page and get html
        _header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"
        }
        _response = requests.get(_url, headers=_header)

        # give the webpage to Beautiful Soup using parsers: "html.parser" or "lxml"
        _soup = BeautifulSoup(_response.text, 'lxml')

        ######### extract html data from webpage and form output data #########

        ##### [1] Basics #####
        # company name
        _htmlBlock = _soup.find("h3", class_="security-name")
        _data["name"] = _htmlBlock.text if _htmlBlock is not None else None

        # ticker name
        _htmlBlock = _soup.find("span", class_="ticker")
        _data["ticker"] = _htmlBlock.text if _htmlBlock is not None else None
        
        # url
        _data["url"] = _url

        # type
        _data["type"] = stocktype

        # current price
        _htmlBlock = _soup.find("span", class_="current-price")
        _data["price"] = _htmlBlock.text if _htmlBlock is not None else None

        # marketcap, sector and risk
        _htmlBlock = _soup.find("div", class_="stock-labels")
        _htmlBlock = _htmlBlock.find_all("span", class_="stock-label-title")
        _data["sector"] = _htmlBlock[0].text if _htmlBlock[0] is not None else None
        _data["marketcap"] = _htmlBlock[1].text if _htmlBlock[1] is not None else None
        _data["risk"] = _htmlBlock[2].text if _htmlBlock[2] is not None else None

        # profile
        _htmlBlock = _soup.find("div", class_="peers-card")
        _value_h = _htmlBlock.h2.text if _htmlBlock.h2 is not None else ""
        _value_p = _htmlBlock.p.text if _htmlBlock.p is not None else ""
        _data["profile"] = _value_h + ": " + _value_p if (_value_h + _value_p) != "" else None

        ##### [2] Overview #####
        _overview = {}

        # current price
        _htmlBlock = _soup.find("span", class_="current-price")
        _overview["currentPrice"] = _htmlBlock.text if _htmlBlock is not None else None

        # change absolute-value
        _htmlBlock = _soup.find("span", class_="absolute-value")
        _overview["absoluteChange"] = _htmlBlock.text if _htmlBlock is not None else None

        # change percentage-value
        _htmlBlock = _soup.find("span", class_="percentage-value")
        _overview["percentageChange"] = str(_htmlBlock.text).replace("(", "").replace(")", "").strip() if _htmlBlock is not None else None

        # marketcap, sector and risk
        _htmlBlock = _soup.find("div", class_="stock-labels")
        _title = _htmlBlock.find_all("span", class_="stock-label-title")
        _desc = _htmlBlock.find_all("span", class_="stock-label-desc")

        _overview["sectorType"] = _title[0].text if _title[0] is not None else None
        _overview["sectorDesc"] = _desc[0].text if _desc[0] is not None else None

        _overview["capType"] = _title[1].text if _title[1] is not None else None
        _overview["capDesc"] = _desc[1].text if _desc[1] is not None else None

        _overview["riskType"] = _title[2].text if _title[2] is not None else None
        _overview["riskDesc"] = _desc[2].text if _desc[2] is not None else None

        # put overview into data
        _data["overview"] = _overview

        ##### [3] Investment Checklist #####
        _investmentChecklist = {}

        # checklist carousel-item get all keys and values
        _htmlBlock = _soup.find("div", class_="carousel-item")
        for _item in _htmlBlock.childGenerator():
            _key = _item.find("span", class_="tooltip-holder").contents[0]
            _key = _key.title().replace(" ", "")
            _key = _key[0].lower() + _key[1:]
            _value = _item.find("i")['class'][3].split("-")[1]
            _investmentChecklist[_key] = _value

        # put investmentChecklist into data
        _data["investmentChecklist"] = _investmentChecklist

        ##### [4] Key Metrics #####
        _keyMetrics = {}

        # PERatio, PBRatio, DividendYield, SectorPE, SectorPB, SectorDividendYield
        _htmlBlock = _soup.find("div", class_="ratios-card")
        _keys = _htmlBlock.select("span.ellipsis.desktop--only")
        _values = _htmlBlock.find_all("div", class_="value")
        for i in range(len(_keys)):
            _key = _keys[i].text
            _key = _key.replace(" ", "")
            _value = _values[i].text
            _value = None if str(_value) == "—" else str(_value)
            _keyMetrics[_key] = _value

        # put keyMetrics into data
        _data["keyMetrics"] = _keyMetrics

        ##### [5] Forecast & Ratings #####
        _forecasts = {}

        # Forecast
        _htmlBlock = _soup.find("div", class_="forecast-radial")
        _value = _htmlBlock.div.span.contents[0] if str(_htmlBlock.div.span.contents[0]) != "—" else ""
        _symbol = _htmlBlock.div.span.span.text if _htmlBlock.div.span.span is not None else ""
        _forecasts["buyRecommendation"] = _value + _symbol if (_value + _symbol) != "" else None
        _forecasts["forecast"] = _htmlBlock.h4.text if _htmlBlock.h4 is not None else None

        # put keyMetrics into data
        _data["forecasts"] = _forecasts

        # return the scraped data
        return _data
    except Exception as _e:
        print(_e)
        return []



# import full company list from the json
allcompanies = []
print("loading full-company-list.json")
try:    
    with open('data/full-company-list.json', 'r') as fp:
        allcompanies = json.load(fp)
except Exception as _e:
    print(_e)

# let's scrape all the stocks & etfs!
allStocksData = []
count = 0

start_time = time.time()
for companies in allcompanies:
    companyName = companies["name"]
    companyType = companies["type"]
    companyDir = companies["subdirectory"]

    if companyType != "stocks":
        continue

    print("scraping data for:", companyName, "url: https://www.tickertape.in/" + companyType + "/" + companyDir)
    try:
        # get data from each page and append to data list
        if companyType == "stocks":
            allStocksData.append(scrapeTickertape(companyName, companyType, companyDir))
            print("successful!")
            count += 1
    except Exception as _e:
        # some issue occured, catch exception
        print("failed!")
        print(_e)

end_time = time.time()
print("all pages scraped successfully!")
print(count, "/", len(allcompanies), "completed")
print("total time taken:", str(timedelta(seconds=(end_time - start_time))))
print()

print("saving the data in json format...")
with open("data/all-stocks-tickertape-data.json", "w") as outfile:
    json.dump(allStocksData, outfile)
print("completed!")

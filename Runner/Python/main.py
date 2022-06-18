from tickertapein.scraper_engine.list import TickerNames
import json
import time
import os


scraper = TickerNames(page_list=TickerNames.PAGE_LIST_ALL, include_type=TickerNames.TYPE_ALL, log=True)
data = scraper.scrape()

print("saving the data in json format...")

filename = "list_" + time.strftime("%Y_%m_%d_%H_%M_%S") + ".json"
dirpath = os.path.abspath("./tickertapein/data/Lists/")
filepath = os.path.join(dirpath, filename)

with open(filepath, "w") as outfile:
    json.dump(data, outfile)

print("completed!")

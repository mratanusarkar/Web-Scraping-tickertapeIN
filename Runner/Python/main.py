from scraper_engine.list import TickerNames
import json
import time


scraper = TickerNames(page_list=TickerNames.PAGE_LIST_ALL, include_type=TickerNames.TYPE_ALL)
data = scraper.scrape()

print("saving the data in json format...")
filename = time.strftime("%Y-%m-%d_%H:%M:%S")
with open("./data/Lists/" + filename + ".json", "w") as outfile:
    json.dump(data, outfile)
print("completed!")

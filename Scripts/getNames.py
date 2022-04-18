import requests
from bs4 import BeautifulSoup
import json
import time
from datetime import timedelta


def getNames(url_filter):

    ########## define custom functions: ##########

    # custom filter function
    def __filter_data_list_fn(listBlock):
        href = listBlock.a['href']
        return "etfs" in href or "stocks" in href
    
    # function to apply filter to htmlBlock and return the filtered htmlBlock 
    def __get_filtered_html_blocks_list(htmlBlock):
        filtered_html_blocks_list = []
        for block in htmlBlock:
            if __filter_data_list_fn(block):
                filtered_html_blocks_list.append(block)
        return filtered_html_blocks_list
    
    # function to map filtered html block to desired data json/dictionary
    def __map_html_block_list_to_data_list(filteredHtmlBlock):
        data_list = []
        for block in filteredHtmlBlock:
            data_obj = {
                "name": block.a.text,
                "type": block.a['href'].split('/')[1],
                "subdirectory": block.a['href'].split('/')[2]
            }
            data_list.append(data_obj)
        return data_list

    ########## get html data from webpage and transform to req data ##########
    try:
        # hit the page and get html
        _header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"
        }
        _response = requests.get("https://www.tickertape.in/stocks?filter="+url_filter, headers=_header)

        # give the webpage to Beautiful Soup using parsers: "html.parser" or "lxml"
        _soup = BeautifulSoup(_response.text, 'lxml')

        # find all li
        _htmlBlock = _soup.find_all("li")

        # filter out lis that doesn't contain our data
        _filteredHtmlBlock = __get_filtered_html_blocks_list(_htmlBlock)

        # get the data
        _data = __map_html_block_list_to_data_list(_filteredHtmlBlock)

        return _data
    except Exception as _e:
        print(_e)
        return []



# let's scrape all the pages!
tickertape_stocks_all = list("abcdefghijklmnopqrstuvwxyz") + ["others"]
fulldata = []

start_time = time.time()
for filter in tickertape_stocks_all:
    print("scraping page: https://www.tickertape.in/stocks?filter="+filter)
    try:
        # get data from each page and append to data list
        fulldata = fulldata + getNames(filter)
        print("successful!")
    except Exception as _e:
        # some issue occured, catch exception
        print("failed!")
        print(_e)

end_time = time.time()
print("all pages scraped successfully!")
print("total time taken:", str(timedelta(seconds=(end_time - start_time))))
print()


print("saving the data in json format...")
with open("data/full-company-list.json", "w") as outfile:
    json.dump(fulldata, outfile)
print("completed!")

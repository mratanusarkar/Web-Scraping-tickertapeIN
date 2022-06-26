import requests
from bs4 import BeautifulSoup
import time
from datetime import timedelta


class TickerNames:

    BASE_URL = "https://www.tickertape.in"

    PAGE_LIST_ALL = list("abcdefghijklmnopqrstuvwxyz") + ["others"]
    PAGE_LIST_TOP = ["top"]
    PAGE_LIST_A_Z = list("abcdefghijklmnopqrstuvwxyz")
    PAGE_LIST_OTH = ["others"]

    TYPE_ALL = "all"
    TYPE_ETF = "etfs"
    TYPE_STOCK = "stocks"

    def __init__(self, page_list: str, include_type: str, log: bool = False):
        self.page_list = page_list
        self.type = include_type
        self.log = log
        self.result = None

    # get webpage soup object
    def __get_soup(self, url_filter: str):
        # hit the page and get html
        header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"
        }
        response = requests.get(self.BASE_URL + "/stocks?filter=" + url_filter, headers=header)

        # give the webpage to Beautiful Soup using parsers: "html.parser" or "lxml"
        soup = BeautifulSoup(response.text, 'lxml')

        return soup

    # custom filter function
    def __filter_data_list_fn(self, list_block):
        href = list_block.a['href']
        return "etfs" in href or "stocks" in href

    # function to apply filter to htmlBlock and return the filtered htmlBlock 
    def __get_filtered_html_blocks_list(self, html_block):
        filtered_html_blocks_list = []
        for block in html_block:
            if self.__filter_data_list_fn(block):
                filtered_html_blocks_list.append(block)
        return filtered_html_blocks_list
    
    # function to map filtered html block to desired data json/dictionary
    def __map_html_block_list_to_data_list(self, filtered_html_block):
        data_list = []
        for block in filtered_html_block:
            data_obj = {
                "name": block.a.text,
                "type": block.a['href'].split('/')[1],
                "subdirectory": block.a['href'].split('/')[2],
                "url": self.BASE_URL + block.a['href']
            }
            if self.type == self.TYPE_ALL or self.type == data_obj['type']:
                data_list.append(data_obj)
        return data_list
    
    def get_names(self, url_filter: str) -> list:
        try:
            # get soup
            soup = self.__get_soup(url_filter)

            # find all li
            html_block = soup.find_all("li")

            # filter out lis that doesn't contain our data
            filtered_html_block = self.__get_filtered_html_blocks_list(html_block)

            # get the data
            data = self.__map_html_block_list_to_data_list(filtered_html_block)

            return data
        except Exception as e:
            print(e)
            return []
    
    def scrape(self) -> list:
        # let's scrape all the pages!
        print("scraping names list...")
        fulldata = []
        page_list = self.page_list

        start_time = time.time()
        for page in page_list:
            if self.log:
                print("scraping page: " + self.BASE_URL + "/stocks?filter=" + page)
            else:
                print('.', end='', flush=True)
                
            try:
                # get data from each page and append to data list
                fulldata = fulldata + self.get_names(page)
                if self.log:
                    print("successful!")
            except Exception as e:
                # some issue occurred, catch exception
                if self.log:
                    print("failed!")
                    print(e)
        end_time = time.time()
        total_time = timedelta(seconds=(end_time - start_time))

        if self.log:
            print("all pages scraped successfully!")
            print("total time taken:", str(total_time))
        print()
        print("completed!")

        self.result = fulldata
        return fulldata

    def filter_by_type(self, full_list: list, filter_type: str) -> list:
        return [data for data in full_list if data['type'] == filter_type]

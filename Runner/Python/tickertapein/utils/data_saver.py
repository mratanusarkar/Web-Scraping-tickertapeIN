import json
import time
import os


class DataSaver:

    SCRAPE_TYPE_LIST = "list"
    SCRAPE_TYPE_STOCK = "stock"
    SCRAPE_TYPE_ETF = "etf"

    FILE_FORMAT_JSON = "json"
    FILE_FORMAT_TEXT = "txt"

    def __init__(self, scrape_type: str = "", file_format: str = "json", log: bool = False):
        self.log = log
        self.scrape_type = scrape_type
        self.file_format = file_format

    def get_paths(self, scrape_type):
        if scrape_type == self.SCRAPE_TYPE_LIST:
            file_name = self.SCRAPE_TYPE_LIST + "_" + time.strftime("%Y_%m_%d_%H_%M_%S") + "." + self.file_format
            dir_path = os.path.abspath("../data/Lists")
        elif scrape_type == self.SCRAPE_TYPE_STOCK:
            file_name = self.SCRAPE_TYPE_STOCK + "_" + time.strftime("%Y_%m_%d_%H_%M_%S") + "." + self.file_format
            dir_path = os.path.abspath("../data/Stocks")
        elif scrape_type == self.SCRAPE_TYPE_ETF:
            file_name = self.SCRAPE_TYPE_ETF + "_" + time.strftime("%Y_%m_%d_%H_%M_%S") + "." + self.file_format
            dir_path = os.path.abspath("../data/ETFs")
        else:
            file_name = ""
            dir_path = ""

        file_path = os.path.join(dir_path, file_name)
        return dir_path, file_path, file_name

    def save(self, data, scrape_type: str):
        if scrape_type == "":
            print("scrape_type not declared. operation failed!")
            return

        if self.log:
            print("saving the data in " + self.file_format + " file format...")

        dir_path, file_path, file_name = self.get_paths(scrape_type)

        # save data
        with open(file_path, "w") as outfile:
            json.dump(data, outfile)

        # save log for tracking
        # TODO: type of data, pages, ticker type, count, datetime
        data = file_name
        with open(dir_path + "/track.json", "w") as outfile:
            json.dump(data, outfile)

        if self.log:
            print("data saved successfully!")

    def save(self, data):
        self.save(data, self.scrape_type)

    def clear(self, scrape_type: str):
        # TODO: delete saved data and update track.json
        print("function clear", scrape_type)

    def clear_all(self):
        # TODO: delete all saved data from all 3 folders and update all the track.json files
        print("function clear_all")

    def check(self) -> bool:
        # TODO: check history if past data is present
        print("function check")

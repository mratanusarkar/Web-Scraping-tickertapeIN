import json
import time
import glob
import os


class DataSaver:

    SCRAPE_TYPE_LIST = "list"
    SCRAPE_TYPE_NAMES = "list"
    SCRAPE_TYPE_STOCK = "stock"
    SCRAPE_TYPE_ETF = "etf"

    FILE_FORMAT_JSON = "json"
    FILE_FORMAT_TEXT = "txt"

    def __init__(self, file_format: str = "json", log: bool = False):
        self.dir_to_scrape_type_map = {
            'Lists': self.SCRAPE_TYPE_LIST,
            'Stocks': self.SCRAPE_TYPE_STOCK,
            'ETFs': self.SCRAPE_TYPE_ETF
        }
        self.file_format = file_format
        self.log = log

    def get_paths(self, scrape_type):
        if scrape_type == self.SCRAPE_TYPE_LIST:
            file_name = self.SCRAPE_TYPE_LIST + "_" + time.strftime("%Y_%m_%d_%H_%M_%S") + "." + self.file_format
            dir_path = os.path.abspath("./tickertapein/data/Lists")
        elif scrape_type == self.SCRAPE_TYPE_STOCK:
            file_name = self.SCRAPE_TYPE_STOCK + "_" + time.strftime("%Y_%m_%d_%H_%M_%S") + "." + self.file_format
            dir_path = os.path.abspath("./tickertapein/data/Stocks")
        elif scrape_type == self.SCRAPE_TYPE_ETF:
            file_name = self.SCRAPE_TYPE_ETF + "_" + time.strftime("%Y_%m_%d_%H_%M_%S") + "." + self.file_format
            dir_path = os.path.abspath("./tickertapein/data/ETFs")
        else:
            file_name = ""
            dir_path = ""

        file_path = os.path.join(dir_path, file_name)
        return dir_path, file_path, file_name

    def save(self, data, scrape_type: str):
        if self.log:
            print("saving " + scrape_type + " data in " + self.file_format + " file format...")

        dir_path, file_path, file_name = self.get_paths(scrape_type)

        # save data
        with open(file_path, "w") as outfile:
            json.dump(data, outfile)

        # save log for tracking
        # TODO: type of data, pages, ticker type, count, datetime
        data = {"datetime": time.strftime("%d-%m-%Y %I:%M:%S %p"), "scrape_type": scrape_type, "file_name": file_name}
        with open(dir_path + "/track.json", "w") as outfile:
            json.dump(data, outfile)

        if self.log:
            print("data saved successfully!")

    def clear(self, scrape_type: str, keep_history: bool = False):
        dir_path, _, _ = self.get_paths(scrape_type)
        for file_path in glob.glob(dir_path + '/*'):
            if not file_path.split('/')[-1] == 'track.json':
                os.remove(file_path)
                if self.log:
                    print('removing: ' + file_path)
                else:
                    print('.', end='', flush=True)
        if not keep_history:
            with open(dir_path + "/track.json", "w") as outfile:
                json.dump({}, outfile)
        if self.log:
            print('cleared all past ' + scrape_type + ' data successfully!')

    def clear_all(self, keep_history: bool = False):
        dir_path = os.path.abspath("./tickertapein/data")
        for folder_path in glob.glob(dir_path + '/*'):
            folder = folder_path.split('/')[-1]
            if self.log:
                print('clearing ' + folder + ' ...')
            self.clear(self.dir_to_scrape_type_map[folder], keep_history)


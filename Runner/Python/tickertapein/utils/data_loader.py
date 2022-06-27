import json
import glob
import os


class DataLoader:
    
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
    
    def get_paths(self, file_name, scrape_type):
        if scrape_type == self.SCRAPE_TYPE_LIST:
            dir_path = os.path.abspath("./tickertapein/data/Lists")
        elif scrape_type == self.SCRAPE_TYPE_STOCK:
            dir_path = os.path.abspath("./tickertapein/data/Stocks")
        elif scrape_type == self.SCRAPE_TYPE_ETF:
            dir_path = os.path.abspath("./tickertapein/data/ETFs")
        else:
            dir_path = ""

        file_path = os.path.join(dir_path, file_name)
        return dir_path, file_path, file_name

    def data_exists(self, scrape_type: str) -> bool:
        dir_path, _, _ = self.get_paths('', scrape_type)
        data_files_list = [name for name in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, name))]
        data_files_list.remove('track.json')
        data_count = len(data_files_list)
        return data_count > 0

    def get_history(self, scrape_type: str) -> dict:
        dir_path, _, _ = self.get_paths('', scrape_type)
        data = None
        with open(dir_path + "/track.json", "r") as readfile:
            data = json.load(readfile)
        return data

    def load_file(self, file_name: str, scrape_type: str) -> list:
        if self.log:
            print("loading " + scrape_type + " data from file with " + self.file_format + " file format...")

        dir_path, file_path, file_name = self.get_paths(file_name, scrape_type)

        # load data
        with open(file_path, "r") as readfile:
            data = json.load(readfile)

        if self.log:
            print("data loaded successfully!")
            
        return data

    def load(self, scrape_type: str) -> list:
        # load the history
        hist = self.get_history(scrape_type)
        if not hist:
            return []
        file_name = hist['file_name']
        data = self.load_file(file_name, scrape_type)
        return data

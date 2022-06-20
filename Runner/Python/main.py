from tickertapein.scraper_engine.list import TickerNames
from tickertapein.utils import DataSaver


scraper = TickerNames(page_list=TickerNames.PAGE_LIST_ALL, include_type=TickerNames.TYPE_ALL, log=True)
saver = DataSaver(log=True)

data = scraper.scrape()
saver.save(data, DataSaver.SCRAPE_TYPE_LIST)

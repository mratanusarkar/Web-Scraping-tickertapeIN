from tickertapein.scraper_engine.list import TickerNames
from tickertapein.scraper_engine.stock import TickerStocks
from tickertapein.utils import DataSaver


names = TickerNames(page_list=TickerNames.PAGE_LIST_TOP, include_type=TickerNames.TYPE_STOCK, log=True)
stock = TickerStocks(log=True)
saver = DataSaver(log=True)

stocks_list = names.scrape()
saver.save(stocks_list, saver.SCRAPE_TYPE_LIST)

data = stock.scrape(stocks_list)
saver.save(data, saver.SCRAPE_TYPE_STOCK)

saver.clear_all()

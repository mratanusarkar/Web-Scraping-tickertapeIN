from tickertapein.scraper_engine.list import TickerNames
from tickertapein.scraper_engine.stock import TickerStocks
from tickertapein.scraper_engine.etf import TickerETFs
from tickertapein.utils import DataSaver

# create all required scraper and utility objects
all_stock_names = TickerNames(page_list=TickerNames.PAGE_LIST_ALL, include_type=TickerNames.TYPE_STOCK, log=True)
all_etf_names = TickerNames(page_list=TickerNames.PAGE_LIST_ALL, include_type=TickerNames.TYPE_ETF, log=True)
stock = TickerStocks(log=True)
etf = TickerETFs(log=True)
saver = DataSaver(log=True)

# main process
stocks_list = all_stock_names.scrape()
etfs_list = all_etf_names.scrape()

saver.save(stocks_list, saver.SCRAPE_TYPE_LIST)
saver.save(etfs_list, saver.SCRAPE_TYPE_LIST)

# data = stock.scrape(stocks_list)
# saver.save(data, saver.SCRAPE_TYPE_STOCK)
data = etf.scrape(etfs_list)
saver.save(data, saver.SCRAPE_TYPE_ETF)

# saver.clear_all()

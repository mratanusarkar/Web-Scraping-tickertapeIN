from tickertapein.scraper_engine.list import TickerNames
from tickertapein.scraper_engine.stock import TickerStocks
from tickertapein.scraper_engine.etf import TickerETFs
from tickertapein.utils import DataLoader
from tickertapein.utils import DataSaver

# create all required scraper and utility objects
names = TickerNames(page_list=TickerNames.PAGE_LIST_ALL, include_type=TickerNames.TYPE_ALL, log=True)
stock = TickerStocks(log=True)
etf = TickerETFs(log=True)
loader = DataLoader(log=True)
saver = DataSaver(log=True)

# main process
if loader.data_exists(loader.SCRAPE_TYPE_LIST):
    full_list = loader.load(loader.SCRAPE_TYPE_LIST)
else:
    full_list = names.scrape()
    saver.save(full_list, saver.SCRAPE_TYPE_LIST)

stocks_list = names.filter_by_type(full_list, names.TYPE_STOCK)
etfs_list = names.filter_by_type(full_list, names.TYPE_ETF)

if loader.data_exists(loader.SCRAPE_TYPE_STOCK):
    stock_data = loader.load(loader.SCRAPE_TYPE_STOCK)
else:
    stock_data = stock.scrape(stocks_list)
    saver.save(stock_data, saver.SCRAPE_TYPE_STOCK)

if loader.data_exists(loader.SCRAPE_TYPE_ETF):
    etf_data = loader.load(loader.SCRAPE_TYPE_ETF)
else:
    etf_data = etf.scrape(etfs_list)
    saver.save(etf_data, saver.SCRAPE_TYPE_ETF)

print(loader.load(loader.SCRAPE_TYPE_LIST))
print(loader.load(loader.SCRAPE_TYPE_STOCK))
print(loader.load(loader.SCRAPE_TYPE_ETF))

saver.clear_all()

print(loader.load(loader.SCRAPE_TYPE_LIST))
print(loader.load(loader.SCRAPE_TYPE_STOCK))
print(loader.load(loader.SCRAPE_TYPE_ETF))

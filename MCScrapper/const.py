__author__ = 'nandi_000'
import time

LINKS_FILENAME = 'allLinks.txt'
SECTOR_LINKS_REPEAT_COUNT = 3
SYMBOL_LINKS_REPEAT_COUNT = 3
SECTOR_LINKS_ERROR_SLEEP_TIME = 5 #sleep time when we fail to fetch a sector
SYMBOL_LINKS_ERROR_SLEEP_TIME = 5 #sleep time when we fail to fetch the symbol details
PARENT_URL = 'http://www.moneycontrol.com/stocks/marketinfo/marketcap/bse/index.html'
TICKER_STATS_FILENAME = r'tickers.pkl'
DATE = time.strftime("%x");
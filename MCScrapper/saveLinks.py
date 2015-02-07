__author__ = 'nandi_000'
# Run this script before running the saveTickerDetails script

from MCScrapper import  AllStocks, const

parent_url = const.PARENT_URL
links = AllStocks.getAllTickerLinks( parent_url )
AllStocks.saveAllTickerLinks( links )

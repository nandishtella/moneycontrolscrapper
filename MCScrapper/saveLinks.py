__author__ = 'nandi_000'
# Run this script before running the saveTickerDetails script

from MCScrapper import utils, const

parent_url = const.PARENT_URL
links = utils.getAllTickerLinks( parent_url )
utils.saveAllTickerLinks( links )
